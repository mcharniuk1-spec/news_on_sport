#!/usr/bin/env python3
"""Flipbook assembler (set KEY=1 if frames came on flat #FF00FF instead of transparency; no bg plate -> alpha .mov overlay). Usage: assemble_flipbook.py <scene> [drawings_per_second=15]
Reads gfx/flip/bg_<scene>.png (fixed background plate) and gfx/flip/<scene>/<scene>_NNN.png (transparent subject frames, sorted),
composites each frame over the plate, and writes clips/flip<scene>.mp4 (1080x1920, 30 fps, each drawing held 30/dps frames)."""
import sys, glob, os, subprocess, tempfile, shutil
from PIL import Image
sc=sys.argv[1]; dps=float(sys.argv[2]) if len(sys.argv)>2 else 15
R=os.path.dirname(os.path.abspath(__file__)); FB=os.environ.get("FLIPBASE","gfx/flip"); OP=os.environ.get("OUTPREFIX","flip")
bgp=f"{R}/{FB}/bg_{sc}.png"; bg=Image.open(bgp).convert("RGBA").resize((1080,1920)) if os.path.exists(bgp) else None
def key(im):
    px=im.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r,g,b,a=px[x,y]
            if r>200 and b>200 and g<90: px[x,y]=(0,0,0,0)
    return im
fr=sorted(glob.glob(f"{R}/{FB}/{sc}/{sc}_*.png"))
assert fr, "no frames"
tmp=tempfile.mkdtemp()
for i,f in enumerate(fr):
    im=Image.open(f).convert("RGBA").resize((1080,1920))
    if os.environ.get("KEY"): im=key(im)
    (Image.alpha_composite(bg,im).convert("RGB") if bg else im).save(f"{tmp}/{i:04d}.png")
out=f"{R}/clips/{OP}{sc}."+("mp4" if bg else "mov")
codec=["-vf","fps=30,format=yuv420p","-c:v","libx264","-crf","14"] if bg else ["-vf","fps=30,format=yuva444p10le","-c:v","prores_ks","-profile:v","4444"]
subprocess.run(["ffmpeg","-v","error","-y","-framerate",str(dps),"-i",f"{tmp}/%04d.png",*codec,out],check=True)
shutil.rmtree(tmp)
d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out]))
print(f"{sc}: {len(fr)} drawings at {dps}/s -> {d:.2f} s -> {out}")
