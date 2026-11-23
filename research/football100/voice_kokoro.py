"""Kokoro British voice (bm_george) for the Kokoro-assigned scripts. Usage: voice_kokoro.py [no ...]  (run with the kvenv python)"""
import json, os, sys, subprocess, glob, numpy as np, soundfile as sf
from kokoro import KPipeline
H="<PROJECT_ROOT>/research/football100"; os.makedirs(f"{H}/voice",exist_ok=True)
pipe=KPipeline(lang_code="b")
want=set(int(x) for x in sys.argv[1:])
for f in sorted(glob.glob(f"{H}/scripts/[0-9][0-9][0-9].json")):
    j=json.load(open(f))
    if j.get("voice")!="kokoro" or (want and j["no"] not in want): continue
    durs=[]
    for i,l in enumerate(j["lines"],1):
        raw=f"{H}/voice/{j['no']:03d}_{i}_raw.wav"; out=f"{H}/voice/{j['no']:03d}_{i}.wav"
        a=[x for _,_,x in pipe(l["vo"].replace("dot UK","dot U K"),voice="bm_george",speed=1.12)]
        sf.write(raw,np.concatenate(a),24000)
        subprocess.run(["ffmpeg","-v","error","-y","-i",raw,"-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo=1.08,acompressor=threshold=-18dB:ratio=3,loudnorm=I=-14:TP=-1.5:LRA=7,aresample=44100",out],check=True)
        os.remove(raw)
        durs.append(round(float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out])),2))
    json.dump(durs,open(f"{H}/voice/{j['no']:03d}.json","w")); print(j["no"],round(sum(durs),1),"s")
