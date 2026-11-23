#!/usr/bin/env python3
"""anim3 PNG sequences (24fps) -> v3/seq/NNN/sKK.mp4 (30fps)."""
import glob, json, os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = json.load(open(f"{H}/codex/v3/plan_v3.json"))
jobs = []
for a in sys.argv[1:]:
    k = f"{int(a):03d}"
    for s in P[k]["sequences"]:
        src = f"{H}/anim3/{k}/{s['id']}"; fs = sorted(glob.glob(src + "/f*.png"))
        if len(fs) != s["frames"]: print("SKIP", k, s["id"], len(fs), "/", s["frames"]); continue
        jobs.append((k, s["id"], src))
def run(j):
    k, sid, src = j; os.makedirs(f"{H}/v3/seq/{k}", exist_ok=True); out = f"{H}/v3/seq/{k}/{sid}.mp4"
    if os.path.exists(out): return k, sid, "ok"
    r = subprocess.run(["ffmpeg","-v","error","-y","-framerate","24","-i",f"{src}/f%04d.png","-vf","fps=30,format=yuv420p,setsar=1","-c:v","libx264","-crf","14","-preset","veryfast","-movflags","+faststart","-an",out],capture_output=True,text=True)
    return k, sid, ("ok" if r.returncode==0 else r.stderr[-200:])
with ThreadPoolExecutor(6) as ex:
    for k, sid, st in ex.map(run, jobs):
        if st != "ok": print(k, sid, st)
print("done", len(jobs))
