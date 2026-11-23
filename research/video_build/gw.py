import sys, subprocess, numpy as np, wave, json
from faster_whisper import WhisperModel
m=WhisperModel("small",device="cpu",compute_type="int8")
out={}
for sec in sys.argv[1:]:
    t0=int(sec.split("-")[0]); f=f"g_{sec}.mp4"
    subprocess.run(["ffmpeg","-v","error","-y","-i",f,"-vn","-ac","1","-ar","16000",f"g_{sec}.wav"])
    w=wave.open(f"g_{sec}.wav"); a=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    seg,info=m.transcribe(a,beam_size=5,word_timestamps=False)
    print("##",sec,info.language)
    for s in seg: print(f"[{s.start+t0:7.1f}-{s.end+t0:7.1f}] {s.text.strip()}")
