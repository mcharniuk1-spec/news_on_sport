#!/usr/bin/env python3
"""Final pipeline stage: put the poster (cover) image into the video as its FIRST frames so every player/app that
takes frame 0 (or the first keyframe) as the preview shows the poster. Audio is copied untouched, so sync and length do not change.
  cover_frame.py [no ...] [--frames N]     default: all 100 + pilot, N=3 frames (0.1 s at 30 fps)
Input : deliver/NNN_*_small.mp4 (or pilot/...) + deliver/NNN_cover.png (or pilot/...)  -- clean, cover-less masters
Output: FINAL_100/videos/NNN_<slug>.mp4 (main) and FINAL_100/pilot_extra/NNN_*_small.mp4 (pilot split videos)
Re-run after any rebuild or new cover art (the masters in deliver/ are never modified)."""
import glob, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
H = os.path.dirname(os.path.abspath(__file__))
args = sys.argv[1:]; N = 3
if "--frames" in args: i = args.index("--frames"); N = int(args[i + 1]); del args[i:i + 2]
nos = [int(a) for a in args] or list(range(1, 101)) + [901, 902, 903, 904]


def paths(no):
    pil = no > 900
    v = (glob.glob(f"{H}/pilot/{no:03d}_*_small.mp4") if pil else glob.glob(f"{H}/deliver/{no:03d}_*_small.mp4"))
    c = f"{H}/pilot/{no:03d}_cover.png" if pil else f"{H}/deliver/{no:03d}_cover.png"
    if not v or not os.path.exists(c): return None
    name = os.path.basename(v[0])
    out = f"{H}/FINAL_100/pilot_extra/{name}" if pil else f"{H}/FINAL_100/videos/{name.replace('_small', '')}"
    return v[0], c, out


def run(no):
    p = paths(no)
    if not p: return no, "missing input"
    v, c, out = p; tmp = out + ".tmp.mp4"
    fc = f"[1:v]scale=1080:1920:flags=lanczos,format=yuv420p,setsar=1[c];[0:v]setsar=1[m];[m][c]overlay=enable='lt(n,{N})':shortest=1[v]"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", v, "-loop", "1", "-framerate", "30", "-i", c, "-filter_complex", fc, "-map", "[v]", "-map", "0:a",
           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-maxrate", "4M", "-bufsize", "8M", "-profile:v", "high", "-pix_fmt", "yuv420p", "-r", "30", "-g", "60",
           "-c:a", "copy", "-movflags", "+faststart", tmp]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode: return no, "ffmpeg: " + r.stderr[-300:]
    os.replace(tmp, out); return no, "ok"


if __name__ == "__main__":
    with ThreadPoolExecutor(3) as ex:
        for no, st in ex.map(run, nos): print(no, st, flush=True)
