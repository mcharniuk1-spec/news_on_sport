import subprocess, re, sys
src,dst=sys.argv[1],sys.argv[2]
out=subprocess.run(["ffmpeg","-hide_banner","-i",src,"-vf","blackframe=amount=80:threshold=20","-an","-f","null","-"],capture_output=True,text=True).stderr
fr=sorted(int(x) for x in re.findall(r"frame:(\d+) pblack",out)); print(src,"black frames:",fr)
if not fr: subprocess.run(["cp",src,dst]); sys.exit()
chain=""; last="0:v"
for i,n in enumerate(fr):
    rep=n+1 if n==0 else n-1
    chain+=f"[{last}][0:v]freezeframes=first={n}:last={n}:replace={rep}[v{i}];"; last=f"v{i}"
subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-filter_complex",chain.rstrip(";"),"-map","["+last+"]","-map","0:a","-c:v","libx264","-crf","15","-preset","medium","-pix_fmt","yuv420p","-c:a","copy",dst],check=True)
out2=subprocess.run(["ffmpeg","-hide_banner","-i",dst,"-vf","blackframe=amount=80:threshold=20","-an","-f","null","-"],capture_output=True,text=True).stderr
print("after:",sorted(int(x) for x in re.findall(r"frame:(\d+) pblack",out2)))
