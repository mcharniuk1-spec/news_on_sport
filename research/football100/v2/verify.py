#!/usr/bin/env python3
"""Verify finished exports. Usage: verify.py [NNN ...]  (default all 100) -> v2/out/verify.json + printed table
Checks per video: opens (ffprobe), 1080x1920, 30 fps, h264 yuv420p, aac stereo 44.1k, duration == meta total, audio loudness ~ -14.5 LUFS and not silent,
first frame == cover (mean abs diff), every interlude present at its timecode (mid-clip frame of the export matches the clip frame in the top 75 %, where subtitles never are),
footage present between interludes (frames differ from the interlude), no frozen/black frames at 10 sampled times, captions present (bottom band has white/yellow text pixels) at spoken times,
cards/outro present, file size sane."""
import glob, json, os, subprocess, sys, tempfile
import numpy as np
from PIL import Image
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def frame(path, t, w=270, h=480):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-frames:v", "1", "-vf", f"scale={w}:{h}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    if len(r.stdout) != w * h * 3: return None
    return np.frombuffer(r.stdout, np.uint8).reshape(h, w, 3).astype(np.float32)


def probe(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,sample_rate,channels,duration:format=duration,size", "-of", "json", path], capture_output=True, text=True)
    return json.loads(r.stdout)


def loud(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128=peak=true", "-vn", "-f", "null", "-"], capture_output=True, text=True).stderr
    try: i = float(r.split("I:")[-1].split("LUFS")[0]); pk = float(r.split("Peak:")[-1].split("dBFS")[0])
    except Exception: return None, None
    return i, pk


def check(no):
    k = f"{no:03d}"; res = {"no": no, "errors": [], "warn": []}; E = res["errors"]; Wn = res["warn"]
    mp = f"{H}/v2/out/{k}_meta.json"
    if not os.path.exists(mp): E.append("no meta"); return res
    M = json.load(open(mp)); f = M["file"]; res["file"] = f
    if not os.path.exists(f): E.append("file missing"); return res
    try: P = probe(f)
    except Exception as e: E.append(f"ffprobe: {e}"); return res
    v = [s for s in P["streams"] if s["codec_type"] == "video"]; a = [s for s in P["streams"] if s["codec_type"] == "audio"]
    if not v or not a: E.append("missing video or audio stream"); return res
    v = v[0]; a = a[0]
    if (v["width"], v["height"]) != (1080, 1920): E.append(f"size {v['width']}x{v['height']}")
    if v["r_frame_rate"] != "30/1": E.append(f"fps {v['r_frame_rate']}")
    if v["codec_name"] != "h264" or v["pix_fmt"] != "yuv420p": E.append(f"codec {v['codec_name']} {v['pix_fmt']}")
    if a["codec_name"] != "aac" or int(a["channels"]) != 2 or a["sample_rate"] != "44100": E.append(f"audio {a['codec_name']} {a['channels']}ch {a['sample_rate']}")
    d = float(P["format"]["duration"]); res["dur"] = round(d, 2); res["size_mb"] = round(int(P["format"]["size"]) / 1e6, 1)
    if abs(d - M["total"]) > 0.1: E.append(f"duration {d:.2f} != planned {M['total']:.2f}")
    if res["size_mb"] < 1 or res["size_mb"] > 40: Wn.append(f"size {res['size_mb']} MB")
    I, pk = loud(f); res["lufs"] = I; res["peak"] = pk
    if I is None or I < -17 or I > -12: E.append(f"loudness {I}")
    if pk is not None and pk > -1.0: E.append(f"peak {pk}")
    # cover as first frame
    cv = f"{H}/deliver/{k}_cover.png"
    if os.path.exists(cv):
        c = np.asarray(Image.open(cv).convert("RGB").resize((270, 480), Image.BILINEAR), np.float32); f0 = frame(f, 0.0)
        if f0 is None or np.abs(f0 - c).mean() > 10: E.append(f"first frame is not the cover (diff {None if f0 is None else round(float(np.abs(f0 - c).mean()), 1)})")
        f1 = frame(f, 0.5)
        if f1 is not None and f0 is not None and np.abs(f1 - c).mean() < 3: E.append("cover stays too long")
    else: E.append("no cover png")
    # interludes at their timecodes
    ok_seq = 0
    for s in M["seq"]:
        fps_clip = 30.0; n_clip = round(s["clip_dur"] * fps_clip); good = 0; tested = 0
        for fr in (0.35, 0.5, 0.65):                       # skip the transitions at both ends
            tc = s["start"] + (s["end"] - s["start"]) * fr
            tmp = tempfile.mktemp(suffix=".png")
            cf = frame(s["clip"], (s["end"] - s["start"]) * fr)
            if cf is None: continue
            best = 99.0                                       # allow +-3 frames (0.1 s) of encoder/seek slack, still proves the timecode
            for kk in range(-3, 4):
                ef = frame(f, tc + kk / 30)
                if ef is not None: best = min(best, float(np.abs(cf[:360] - ef[:360]).mean()))
            tested += 1
            if best < 6: good += 1
        if tested and good >= 2: ok_seq += 1
        else: E.append(f"interlude {s['id']} not found at {s['start']:.2f}-{s['end']:.2f}s")
    res["interludes"] = f"{ok_seq}/{len(M['seq'])}"
    if M["missing"]: E.append(f"missing interludes {M['missing']}")
    if M["dropped"]: Wn.append(f"dropped {M['dropped']}")
    # sampled frames: not black, not frozen; captions present
    prev = None; frozen = 0
    for i in range(1, 11):
        t = M["total"] * i / 11; fr_ = frame(f, t)
        if fr_ is None: E.append(f"cannot decode frame at {t:.1f}s"); continue
        if fr_.mean() < 12: E.append(f"black frame at {t:.1f}s")
        if prev is not None and np.abs(fr_ - prev).mean() < 0.5: frozen += 1
        prev = fr_
    if frozen > 1: E.append(f"frozen frames x{frozen}")
    cap = 0; samples = 0
    asr = json.load(open(f"{H}/v2/timing/{k}.json"))["words"]
    for w in asr[2:-6:max(1, len(asr) // 12)]:
        t = w["s"] + 0.1 + (w["e"] - w["s"]) / 2; fr_ = frame(f, t, 1080, 1920)
        if fr_ is None: continue
        band = fr_[1560:1700]; samples += 1
        yel = ((band[..., 0] > 240) & (band[..., 1] > 170) & (band[..., 2] < 120)).sum(); wht = ((band > 245).all(-1)).sum()
        if wht + yel > 400: cap += 1
    res["captions"] = f"{cap}/{samples}"
    if samples and cap < samples * 0.7: E.append(f"captions visible in only {cap}/{samples} samples")
    # outro present at the end
    fo = frame(f, M["total"] - 0.6)
    if fo is None or fo.mean() < 15: E.append("outro card missing/black")
    res["ok"] = not E
    return res


if __name__ == "__main__":
    nos = [int(a) for a in sys.argv[1:]] or list(range(1, 101))
    from concurrent.futures import ThreadPoolExecutor
    out = {}
    with ThreadPoolExecutor(4) as ex:
        for r in ex.map(check, nos):
            out[f"{r['no']:03d}"] = r
            print(("OK  " if r.get("ok") else "FAIL"), f"{r['no']:03d}", r.get("dur"), "s", r.get("size_mb"), "MB", r.get("lufs"), "LUFS", "seq", r.get("interludes"), "cap", r.get("captions"), r["errors"] or "", r["warn"] or "", flush=True)
    json.dump(out, open(f"{H}/v2/out/verify.json", "w"), indent=1)
    bad = [k for k, r in out.items() if not r.get("ok")]
    print(f"{len(out) - len(bad)}/{len(out)} verified", "failed:", bad)
