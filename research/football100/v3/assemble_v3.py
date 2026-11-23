#!/usr/bin/env python3
"""Assemble one finished Short with ffmpeg only (no Palmier).
  assemble.py NNN [--out-dir DIR] [--keep]
Inputs : scripts/NNN.json, voice (v2/asr + v2/work/NNN/voice.wav), footage/NNN/c*.mp4, v2/seq/NNN/sKK.mp4 (interludes, 30 fps), deliver/NNN_cover.png,
         v2/timing/NNN.json (run tools/timing.py), music + whoosh from research/video_build.
Output : FINAL_100_v2/videos/NNN_<slug>.mp4 (cover = first 3 frames) + v2/out/NNN_meta.json (placements for verification).
Everything a video needs is written under v2/work/NNN (own folder per video, so videos can be built in parallel)."""
import glob, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../v2/tools")
import captions as CAP, timing as TM
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VB = os.path.dirname(H) + "/video_build"
FPS = 30; OV = 0.2; VO = TM.VO
q = lambda t: round(t * FPS) / FPS


def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def run(cmd, log):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        open(log, "w").write(r.stderr[-6000:]); raise RuntimeError(f"ffmpeg failed, see {log}: {r.stderr[-400:]}")


def plan_shots(no, starts_tl, END):
    clips = sorted(glob.glob(f"{H}/footage/{no:03d}/c*.mp4")); assert clips, "no footage"
    cd = {c: dur(c) for c in clips}; off = {c: 0.0 for c in clips}; n = len(starts_tl); shots = []; ci = 0
    outro_d = max(2.8, END - starts_tl[-1]); outro = f"{H}/clips/outro2_{int(outro_d * 10)}.mp4"
    if not os.path.exists(outro):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{H}/clips/hf_outro.mp4", "-vf", f"tpad=stop_mode=clone:stop_duration={max(0, outro_d - 2.8) + 0.4:.2f},fps=30", "-t", f"{outro_d + 0.4:.2f}", "-an", "-c:v", "libx264", "-crf", "18", outro], check=True)
    for i in range(n - 1):
        a = starts_tl[i] if i > 0 else 0.0; b = starts_tl[i + 1]; span = b - a
        if span <= 0.3: continue
        k = max(1, round(span / 3.0)); L2 = span / k
        for j in range(k):
            c = clips[ci % len(clips)]; ci += 1; w = L2 + 0.4
            if off[c] + w > cd[c]: off[c] = 0.0
            shots.append({"clip": c, "a": a + j * L2, "b": a + (j + 1) * L2, "off": off[c], "kind": "foot"}); off[c] += w
    shots.append({"clip": outro, "a": starts_tl[-1], "b": starts_tl[-1] + outro_d, "off": 0.0, "kind": "outro"})
    for s in shots: s["a"] = q(s["a"]); s["b"] = q(s["b"])
    for k in range(len(shots) - 1): shots[k]["b"] = shots[k + 1]["a"]       # contiguous, no holes
    shots[0]["a"] = 0.0
    return shots, outro_d, shots[-1]["b"]


def build_base(no, shots, W):
    cmd = ["ffmpeg", "-v", "error", "-y"]; fc = []; m = len(shots); starts = []
    for k, s in enumerate(shots):
        ost = s["a"] - (OV if k > 0 else 0.0); L = s["b"] - ost; starts.append(ost)
        so = max(0.0, s["off"] - (OV if k > 0 else 0.0))
        cmd += ["-ss", f"{so:.3f}", "-t", f"{L + 0.05:.3f}", "-i", s["clip"]]
        if s["kind"] == "foot":
            z0, z1 = (1.0, 1.22) if k % 2 == 0 else (1.24, 1.0)
            if k % 5 == 3: z0, z1 = 1.0, 1.4
            Z = f"({z0}+({z1 - z0})*t/{L:.3f})"
            fc.append(f"[{k}:v]setpts=PTS-STARTPTS,fps=30,scale=w='trunc(1080*{Z}/2)*2':h='trunc(1920*{Z}/2)*2':eval=frame,crop=1080:1920,eq=contrast=1.1:saturation=1.1,noise=alls=7:allf=t,vignette=angle=PI/5:eval=init,unsharp=3:3:0.5,format=yuv420p,setsar=1,trim=duration={L:.3f},setpts=PTS-STARTPTS[v{k}]")
        else:
            fc.append(f"[{k}:v]setpts=PTS-STARTPTS,fps=30,scale=1080:1920,format=yuv420p,setsar=1,trim=duration={L:.3f},setpts=PTS-STARTPTS[v{k}]")
    cur = "v0"
    for k in range(1, m):
        off = shots[k]["a"] - OV
        fc.append(f"[{cur}][v{k}]xfade=transition=fade:duration={OV}:offset={off:.3f}[x{k}]"); cur = f"x{k}"
    out = f"{W}/base.mp4"
    run(cmd + ["-filter_complex", ";".join(fc), "-map", f"[{cur}]", "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30", "-an", out], f"{W}/base.log")
    return out


def build(no, out_dir=None, keep=False):
    W = f"{H}/v2/work/{no:03d}"; os.makedirs(W, exist_ok=True); os.makedirs(f"{H}/v2/out", exist_ok=True)
    J = json.load(open(f"{H}/scripts/{no:03d}.json")); L = J["lines"]; n = len(L)
    tp = f"{H}/v2/timing/{no:03d}.json"
    if not os.path.exists(tp):
        T = TM.build(no); S, Wn = TM.place(no, T); T["seq"] = S; T["warn"] = Wn; json.dump(T, open(tp, "w"), indent=1)
    T = json.load(open(tp)); vtot = T["vtot"]; voice = json.load(open(f"{H}/v2/asr/{no:03d}.json"))["voice"]
    starts_tl = [x + VO for x in T["line_starts"]]; END = vtot + VO + 0.5
    shots, outro_d, total = plan_shots(no, starts_tl, END)
    total = q(total); outro_start = starts_tl[-1]
    base = f"{W}/base.mp4"
    if not os.path.exists(base) or "--rebase" in sys.argv: build_base(no, shots, W)
    # ---- interludes present on disk
    seqs = []; missing = []
    PV = json.load(open(f"{H}/codex/v3/plan_v3.json"))[f"{no:03d}"]["sequences"]
    tmap = {x["id"]: x for x in T["seq"]}; ps = sorted(PV, key=lambda x: x["start"]); last_shift = 0.0; merged = []
    for x in ps:
        if x["id"] in tmap: last_shift = tmap[x["id"]]["shift"]; merged.append({**tmap[x["id"]]})
        else: merged.append({"id": x["id"], "kind": x["kind"], "start": round(x["start"] + last_shift + VO, 3), "end": round(x["end"] + last_shift + VO, 3), "frames": x["frames"], "shift": last_shift})
    prev_end = -1.0; keep = []
    for x in merged:
        if x["start"] < prev_end + 0.12 or x["end"] > starts_tl[-1] - 0.1: continue
        keep.append(x); prev_end = x["end"]
    for s in keep:
        p = f"{H}/v3/seq/{no:03d}/{s['id']}.mp4"
        if not os.path.exists(p): p = f"{H}/v2/seq/{no:03d}/{s['id']}.mp4" if s["id"] in tmap else p
        if not os.path.exists(p): missing.append(s["id"]); continue
        d = dur(p); a = q(s["start"]); seqs.append({**s, "clip": p, "start": a, "end": q(a + d), "clip_dur": round(d, 3)})
    # ---- cards (headline text) outside interludes
    cards = []
    for i in range(n - 1):
        if not L[i].get("card"): continue
        a = starts_tl[i] + 0.15; b = min(a + 2.2, starts_tl[i + 1] + 0.9 if i < n - 2 else outro_start)
        wins = [(a, b)]
        for s in seqs:
            nw = []
            for x, y in wins:
                if s["end"] + 0.15 <= x or s["start"] - 0.15 >= y: nw.append((x, y)); continue
                if s["start"] - 0.15 > x: nw.append((x, s["start"] - 0.15))
                if s["end"] + 0.15 < y: nw.append((s["end"] + 0.15, y))
            wins = nw
        for x, y in wins:
            if y - x >= 1.0: cards.append((L[i]["card"], q(x), q(y)))
    # ---- sprites
    cap_end = q(outro_start + 0.4)
    lf, ncap = CAP.caption_track(T["words"], VO, cap_end, f"{W}/cap")
    cps = []
    for j, (txt, a, b) in enumerate(cards):
        p = f"{W}/card{j:02d}.png"; CAP.card_sprite(txt, p); cps.append((p, a, b))
    cover = f"{H}/v3/cover/{no:03d}.png"; has_cover = os.path.exists(cover)
    # ---- composite
    cmd = ["ffmpeg", "-v", "error", "-y", "-i", base]; fc = []; idx = 1; cur = "bs"; fc.append("[0:v]setsar=1,format=yuv420p[bs]")
    for k, s in enumerate(seqs):
        cmd += ["-i", s["clip"]]
        fc.append(f"[{idx}:v]fps=30,setpts=PTS-STARTPTS+{s['start']:.4f}/TB,format=yuv420p,setsar=1[q{k}]")
        fc.append(f"[{cur}][q{k}]overlay=enable='between(t,{s['start'] - 0.001:.4f},{s['end'] - 0.001:.4f})':eof_action=pass:repeatlast=0[o{k}]"); cur = f"o{k}"; idx += 1
    for j, (p, a, b) in enumerate(cps):
        d = b - a
        cmd += ["-loop", "1", "-framerate", "30", "-t", f"{d:.3f}", "-i", p]
        fc.append(f"[{idx}:v]format=rgba,fade=t=in:st=0:d=0.12:alpha=1,fade=t=out:st={d - 0.12:.3f}:d=0.12:alpha=1,setpts=PTS-STARTPTS+{a:.4f}/TB[k{j}]")
        fc.append(f"[{cur}][k{j}]overlay=x=0:y=210:enable='between(t,{a:.4f},{b - 0.001:.4f})':eof_action=pass:repeatlast=0[p{j}]"); cur = f"p{j}"; idx += 1
    cmd += ["-f", "concat", "-safe", "0", "-i", lf]
    fc.append(f"[{idx}:v]fps=30,format=rgba[cp]"); fc.append(f"[{cur}][cp]overlay=x=0:y={CAP.CAP_Y}:eof_action=pass:repeatlast=0[cc]"); cur = "cc"; idx += 1
    if has_cover:
        cmd += ["-loop", "1", "-framerate", "30", "-t", "0.5", "-i", cover]
        fc.append(f"[{idx}:v]scale=1080:1920:flags=lanczos,format=yuv420p,setsar=1[cv]"); fc.append(f"[{cur}][cv]overlay=enable='lt(n,3)':eof_action=pass:repeatlast=0[cvo]"); cur = "cvo"; idx += 1
    fc.append(f"[{cur}]format=yuv420p[vout]")
    # audio
    music = f"{VB}/music/phonk_full.wav"; whoosh = f"{VB}/audio/whoosh.wav" if os.path.exists(f"{VB}/audio/whoosh.wav") else f"{VB}/music/whoosh.wav"
    cmd += ["-i", voice]; vi = idx; idx += 1
    cmd += ["-i", music]; mi = idx; idx += 1
    wh_t = sorted({max(0.0, s["start"] - 0.1) for s in seqs} | {max(0.0, outro_start - 0.1)})
    use_wh = os.path.exists(whoosh) and wh_t
    if use_wh: cmd += ["-i", whoosh]; wi = idx; idx += 1
    A = [f"[{vi}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,adelay={int(VO * 1000)}|{int(VO * 1000)}[va]",
         f"[{mi}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,atrim=0:{total:.3f},asetpts=PTS-STARTPTS,volume=0.1,afade=t=out:st={total - 0.9:.3f}:d=0.9[ma]"]
    mix = ["[va]", "[ma]"]
    if use_wh:
        A.append(f"[{wi}:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,volume=0.14,asplit={len(wh_t)}" + "".join(f"[w{i}]" for i in range(len(wh_t))))
        for i, t in enumerate(wh_t): A.append(f"[w{i}]adelay={int(t * 1000)}|{int(t * 1000)}[wd{i}]"); mix.append(f"[wd{i}]")
    A.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=longest,atrim=0:{total:.3f},alimiter=limit=0.8:level=disabled,loudnorm=I=-14.5:TP=-2:LRA=9,aresample=44100[aout]")
    slug = re.sub(r"[^a-z0-9]+", "_", J["subject"].lower())[:36].strip("_")
    od = out_dir or f"{H}/FINAL_100_v3/videos"; os.makedirs(od, exist_ok=True)
    dst = f"{od}/{no:03d}_{slug}.mp4"; tmp = dst + ".tmp.mp4"
    cmd += ["-filter_complex", ";".join(fc + A), "-map", "[vout]", "-map", "[aout]", "-t", f"{total:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "4M", "-bufsize", "8M", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30", "-g", "60",
            "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", tmp]
    run(cmd, f"{W}/final.log"); os.replace(tmp, dst)
    meta = {"no": no, "file": dst, "total": total, "outro_start": round(outro_start, 3), "cover": has_cover, "seq": [{k: s[k] for k in ("id", "kind", "start", "end", "clip", "clip_dur", "frames")} for s in seqs],
            "missing": missing, "dropped": T.get("warn", []), "cards": [{"text": t, "a": a, "b": b} for t, a, b in cards], "caption_sprites": ncap, "whoosh": wh_t, "shots": len(shots)}
    json.dump(meta, open(f"{H}/v3/out/{no:03d}_meta.json", "w"), indent=1)
    print("built", no, dst, f"{total:.2f}s", "seq", len(seqs), "missing", missing, flush=True)
    return dst


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    od = None
    if "--out-dir" in sys.argv: od = sys.argv[sys.argv.index("--out-dir") + 1]; a = [x for x in a if x != od]
    for x in a: build(int(x), od)
