#!/usr/bin/env python3
"""Codex PNG sequences (24 fps) -> v2/seq/NNN/sKK.mp4 (30 fps, H.264 yuv420p, opaque). Usage: anim_to_clips.py NNN ... [-j 4]"""
import glob, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = json.load(open(f"{H}/codex/v2/plan.json"))
args = sys.argv[1:]; J = 4
if "-j" in args: i = args.index("-j"); J = int(args[i + 1]); del args[i:i + 2]
jobs = []
for a in args:
    k = f"{int(a):03d}"
    for s in P[k]["sequences"]:
        src = f"{H}/anim/{k}/{s['id']}"; fs = sorted(glob.glob(src + "/f*.png"))
        if len(fs) != s["frames"]: print("SKIP", k, s["id"], len(fs), "/", s["frames"]); continue
        jobs.append((k, s["id"], src, s["frames"]))
def run(j):
    k, sid, src, n = j; os.makedirs(f"{H}/v2/seq/{k}", exist_ok=True); out = f"{H}/v2/seq/{k}/{sid}.mp4"
    if os.path.exists(out): return k, sid, "exists"
    r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "24", "-i", f"{src}/f%04d.png", "-vf", "fps=30,format=yuv420p,setsar=1", "-c:v", "libx264", "-crf", "13", "-preset", "medium", "-movflags", "+faststart", "-an", out], capture_output=True, text=True)
    return k, sid, ("ok" if r.returncode == 0 else r.stderr[-200:])
with ThreadPoolExecutor(J) as ex:
    for k, sid, st in ex.map(run, jobs):
        if st != "ok": print(k, sid, st)
print("done", len(jobs))
