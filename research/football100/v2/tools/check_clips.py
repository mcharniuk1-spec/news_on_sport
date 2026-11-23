#!/usr/bin/env python3
"""Own clip checker for v2/seq/NNN/sKK.mp4 (not the codex check_anim.py). Usage: check_clips.py [NNN ...] -> prints problems, exit 1 if any.
Per clip: exists, 1080x1920, 30 fps, h264 yuv420p, no audio, frames == floor(plan_frames/24*30 + 0.5) (round half up), no two neighbouring frames identical, no blank frame, first/middle/last differ."""
import json, os, subprocess, sys
import numpy as np
H = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = json.load(open(f"{H}/codex/v2/plan.json"))
def chk(k, s):
    p = f"{H}/v2/seq/{k}/{s['id']}.mp4"; e = []
    if not os.path.exists(p): return [f"{k}/{s['id']} missing"]
    r = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-show_entries", "stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,nb_read_frames", "-of", "json", p], capture_output=True, text=True)
    try: st = json.loads(r.stdout)["streams"]
    except Exception: return [f"{k}/{s['id']} unreadable"]
    v = [x for x in st if x["codec_type"] == "video"]
    if not v or any(x["codec_type"] == "audio" for x in st): return [f"{k}/{s['id']} stream layout"]
    v = v[0]; want = int(s["frames"] / 24 * 30 + 0.5)   # round HALF UP (Python round() is banker's: 52.5 -> 52, but Remotion/JS Math.round gives 53)
    if (v["width"], v["height"]) != (1080, 1920): e.append(f"size {v['width']}x{v['height']}")
    if v["r_frame_rate"] != "30/1": e.append(f"fps {v['r_frame_rate']}")
    if v["codec_name"] != "h264" or v["pix_fmt"] != "yuv420p": e.append(f"codec {v['codec_name']}/{v['pix_fmt']}")
    if abs(int(v["nb_read_frames"]) - want) > 1: e.append(f"frames {v['nb_read_frames']} != {want}")
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-vf", "scale=54:96:flags=area,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout
    n = len(raw) // (54 * 96)
    if n:
        a = np.frombuffer(raw[:n * 54 * 96], np.uint8).reshape(n, 96 * 54).astype(np.int16)
        dup = int((np.abs(a[1:] - a[:-1]).max(1) == 0).sum())
        allow = (int(k) <= 15) and int(want * 0.2 + 2)   # Codex PNGs are 24 fps; conforming to 30 fps repeats every 5th frame
        if dup > (allow or 0): e.append(f"{dup} identical neighbouring frames")
        if (a.mean(1) < 8).any() or (a.mean(1) > 250).any(): e.append("blank frame")
        if np.abs(a[0] - a[n // 2]).mean() < 1 or np.abs(a[n // 2] - a[-1]).mean() < 1: e.append("start/middle/end too similar")
    return [f"{k}/{s['id']}: " + "; ".join(e)] if e else []
if __name__ == "__main__":
    ks = [f"{int(a):03d}" for a in sys.argv[1:]] or sorted(P)
    from concurrent.futures import ThreadPoolExecutor
    jobs = [(k, s) for k in ks for s in P[k]["sequences"]]; bad = []
    with ThreadPoolExecutor(4) as ex:
        for r in ex.map(lambda j: chk(*j), jobs): bad += r
    for b in bad: print("FAIL", b)
    print(f"{len(jobs) - len(bad)}/{len(jobs)} clips pass"); sys.exit(1 if bad else 0)
