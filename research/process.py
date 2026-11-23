#!/usr/bin/env python3
"""Stage 5: low-res download (shorts full, long first 60 s) -> frames every 2 s, contact sheet, scene cuts. Deletes media after."""
import json, subprocess, os, re, glob, shutil, sys
from concurrent.futures import ThreadPoolExecutor
R = os.path.dirname(os.path.abspath(__file__))
WORK, FR, SH = f"{R}/work", f"{R}/frames", f"{R}/sheets"
for d in (WORK, FR, SH, f"{R}/subs"): os.makedirs(d, exist_ok=True)
V = json.load(open(f"{R}/videos.json"))
def sh(cmd, t=300):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=t)
def one(v):
    vid, kind = v["id"], v["kind"]
    out = {"id": vid, "ok": False}
    if os.path.exists(f"{R}/frames/{vid}/meta.json"): return json.load(open(f"{R}/frames/{vid}/meta.json"))
    mp4 = f"{WORK}/{vid}.mp4"
    args = ["yt-dlp","--no-update","-q","--no-playlist","-f","bv*[height<=360]/b[height<=360]/worst","-o",mp4]
    if kind == "long": args[args.index("bv*[height<=360]/b[height<=360]/worst")] = "bv*[height<=240]/worst"
    sh(args + [v["url"]])
    files = glob.glob(f"{WORK}/{vid}.*")
    files = [f for f in files if not f.endswith(".part")]
    if not files: out["err"] = "download"; return out
    src = files[0]
    os.makedirs(f"{FR}/{vid}", exist_ok=True)
    w = 180 if kind == "short" else 240
    sh(["ffmpeg","-y","-v","error","-i",src,"-t","62","-vf",f"fps=0.5,scale={w}:-2","-q:v","9",f"{FR}/{vid}/f%02d.jpg"])
    n = len(glob.glob(f"{FR}/{vid}/f*.jpg"))
    # contact sheet, row-major, 6 columns, first tile = t0 (2 s step)
    rows = (n + 5) // 6
    sh(["ffmpeg","-y","-v","error","-i",src,"-t","62","-vf",f"fps=0.5,scale={w}:-2,tile=6x{max(rows,1)}","-frames:v","1","-q:v","5",f"{SH}/{vid}.jpg"])
    # scene cuts
    p = sh(["ffmpeg","-i",src,"-t","62","-vf","select='gt(scene,0.3)',showinfo","-an","-f","null","-"])
    cuts = [round(float(x), 1) for x in re.findall(r"pts_time:([0-9.]+)", p.stderr)]
    pr = sh(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height,r_frame_rate","-of","csv=p=0",src]).stdout.strip()
    out.update(ok=True, frames=n, cuts=cuts, probe=pr)
    json.dump(out, open(f"{FR}/{vid}/meta.json","w"))
    for f in files: os.remove(f)
    return out
with ThreadPoolExecutor(6) as ex:
    res = list(ex.map(one, V))
bad = [r for r in res if not r.get("ok")]
print("done", len(res), "failed", len(bad), [b["id"] for b in bad][:20])
