"""Download ElevenLabs takes: dl_el.py NO SESSION GEN SIG ... (groups of 4 args). Saves voice/NNN_el.mp3"""
import sys, subprocess
B="https://elevenlabsusercontent.com/database/workspace/309cdd7c69c54fb1b6b8789a7c7785d0/content_generation/{s}/{g}/content.mp3?Expires=1795269600&KeyName=assets-cdn-key-1&Signature={sig}"
a=sys.argv[1:]
for i in range(0,len(a),4):
    no,s,g,sig=a[i:i+4]
    out=f"voice/{int(no):03d}_el.mp3"
    subprocess.run(["curl","-s","-f","-o",out,B.format(s=s,g=g,sig=sig)])
    d=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out],capture_output=True,text=True).stdout.strip()
    print(no,d)
