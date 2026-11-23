"""Make finished Shorts end to end for the given script numbers (Kokoro voice only). Usage: batch.py N N N ..."""
import sys, subprocess, json, re, os, shutil
from concurrent.futures import ThreadPoolExecutor
H="<PROJECT_ROOT>/research/football100"; PY=f"{H}/../video_build/kvenv/bin/python"
nums=[int(x) for x in sys.argv[1:]]
def prep(n):
    subprocess.run([PY,f"{H}/voice_kokoro.py",str(n)],capture_output=True,cwd=H)
    subprocess.run(["python3",f"{H}/fetch_footage.py",str(n)],capture_output=True,cwd=H)
    return n
def finish(n):
    r=subprocess.run(["python3","build100.py",str(n)],capture_output=True,text=True,cwd=H)
    if "built" not in r.stdout: print("BUILD FAIL",n,(r.stdout+r.stderr)[-200:],flush=True); return
    r=subprocess.run(["python3","export100.py",str(n)],capture_output=True,text=True,cwd=H)
    if "done" not in r.stdout: print("EXPORT FAIL",n,r.stdout[-200:],flush=True); return
    raw=f"{H}/builds/{n:03d}_raw.mp4"; fin=f"{H}/builds/{n:03d}_final.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",raw,"-c:v","copy","-af","alimiter=limit=0.8:level=disabled,loudnorm=I=-14.5:TP=-2:LRA=9,aresample=44100","-c:a","aac","-b:a","192k",fin])
    j=json.load(open(f"{H}/scripts/{n:03d}.json")); slug=re.sub(r"[^a-z0-9]+","_",j["subject"].lower())[:36].strip("_")
    dst=f"{H}/deliver/{n:03d}_{slug}.mp4"; shutil.copy(fin,dst)
    subprocess.run(["ffmpeg","-v","error","-y","-i",dst,"-c:v","libx264","-crf","26","-preset","medium","-c:a","copy",dst.replace(".mp4","_small.mp4")])
    print("DONE",n,dst.replace(".mp4","_small.mp4"),flush=True)
with ThreadPoolExecutor(3) as ex:
    for n in ex.map(prep,nums): finish(n)
