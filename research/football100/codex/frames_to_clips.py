#!/usr/bin/env python3
"""flip/NNN_k/f01..f12.png -> clips/flip_NNN_k.mp4 (1080x1920, 30 fps, 12 drawings at 6/s = exactly 2.0 s, what build100.py plays).
Usage: frames_to_clips.py [NNN_k ...]   (no args = every flip/* folder with 12 frames; --force rebuilds existing clips)"""
import sys, os, glob, subprocess
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith("--")]; force = "--force" in sys.argv
dirs = [f"{H}/flip/{a}" for a in args] or sorted(glob.glob(f"{H}/flip/[0-9][0-9][0-9]_[0-9]"))
bad = []
for d in dirs:
    sc = os.path.basename(d); out = f"{H}/clips/flip_{sc}.mp4"
    fr = [f"{d}/f{i:02d}.png" for i in range(1, 13)]
    miss = [f for f in fr if not os.path.exists(f)]
    if miss: bad.append((sc, f"missing {len(miss)} frames, first {os.path.basename(miss[0])}")); continue
    if os.path.exists(out) and not force: continue
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "6", "-i", f"{d}/f%02d.png",
        "-vf", "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,format=yuv420p",
        "-c:v", "libx264", "-crf", "14", "-an", out], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]))
    print(f"{sc}: {dur:.2f} s -> {out}")
for sc, m in bad: print("SKIP", sc, m)
