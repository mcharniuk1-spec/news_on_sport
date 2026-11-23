import json, subprocess, numpy as np, soundfile as sf
from kokoro import KPipeline
S=json.load(open("v3/scripts.json")); pipe=KPipeline(lang_code="b")
for k in ("ron2","mud2","por"):
    for i,t in enumerate(S[k],1):
        a=[x for _,_,x in pipe(t,voice="bm_george",speed=1.12)]
        sf.write(f"v3/{k}_{i}_raw.wav",np.concatenate(a),24000)
        subprocess.run(["ffmpeg","-v","error","-y","-i",f"v3/{k}_{i}_raw.wav","-af","silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,atempo=1.08,acompressor=threshold=-18dB:ratio=3,loudnorm=I=-14:TP=-1.5:LRA=7,aresample=44100",f"v3/{k}_{i}.wav"],check=True)
        d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"v3/{k}_{i}.wav"])); print(k,i,round(d,2))
