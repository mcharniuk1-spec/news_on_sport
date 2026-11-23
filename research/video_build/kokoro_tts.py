import sys, soundfile as sf, numpy as np
from kokoro import KPipeline
lines=["Ronaldinho. Forty-six years old!","Eleven years. No pro football.","Everyone said: it's a joke.","Third division. White shirt.","Flares! Smoke! Chaos!","Brutal league.","Ravenna two. Forlee nil.","Retired? Never!","Who's next? Your grandad?"]
pipe=KPipeline(lang_code="b")
for v in sys.argv[1:]:
    for i,t in enumerate(lines,1):
        a=[]
        for _,_,au in pipe(t,voice=v,speed=1.12): a.append(au)
        x=np.concatenate(a); sf.write(f"voice/{v}_{i}.wav",x,24000)
    print(v,"done")
