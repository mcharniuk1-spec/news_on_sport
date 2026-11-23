import subprocess, os, json
def sh(a): subprocess.run(a,check=True)
# interview clips: (name, segfile, segstart, start, end, [(t0,t1,x)...] default x)
IV=[("G1","g_910-1110",910,943.5,958.5,[(0,0.9,340)],560),
    ("G3","g_3200-3270",3200,3208.2,3222.4,[(0,1.5,340),(5.0,8.4,340)],560),
    ("G4","g_6110-6170",6110,6158.0,6168.5,[(0,8.2,340)],560),
    ("G5","g_4790-4815",4790,4789.0,4801.5,[(0,3.0,340),(4.4,7.2,340),(9.0,13,340)],560)]
for n,seg,s0,a,b,gor,dx in IV:
    out=f"lib/iv_{n}.mp4"
    if os.path.exists(out): continue
    expr=str(dx)
    for t0,t1,x in reversed(gor): expr=f"if(between(t,{t0},{t1}),{x},{expr})"
    # note: g_4790-4815 segment file starts at 4790 but G5 starts 4789 -> use the 4740-4795 file for the first second
    src=f"mud/{seg}.mp4"; ss=a-s0
    if ss<0: src="mud/g_4740-4795.mp4"; ss=a-4740; 
    sh(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(b-a),"-i",src,"-an","-vf",f"crop=w=405:h=720:x='{expr}':y=0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.8,fps=30,format=yuv420p","-c:v","libx264","-crf","15","-preset","fast",out])
    sh(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(b-a),"-i",src,"-vn","-af","highpass=f=80,loudnorm=I=-15:TP=-2:LRA=9,aresample=44100","-ac","2",f"lib/iv_{n}.wav"])
    print(n,"ok",round(b-a,1))
# music: ron (drop at 63.5) and mud (drop at 23.0)
def music(name,pre_src_start,pre_len,drops):
    parts=[]
    sh(["ffmpeg","-v","error","-y","-i","music/phonk_song.mp3","-ac","2","-ar","44100","music/phonk_full.wav"])
    def seg(ss,d,o): sh(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(d),"-i","music/phonk_full.wav",o]); return o
    files=[seg(pre_src_start,pre_len,f"music/{name}_a.wav")]
    for i in range(drops): files.append(seg(48.04,33.0,f"music/{name}_d{i}.wav"))
    open(f"music/{name}_list.txt","w").write("".join(f"file '{os.path.abspath(f)}'\n" for f in files))
    sh(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"music/{name}_list.txt","-af","afade=t=out:st=%s:d=2"%(pre_len+33*drops-2),f"music/{name}.wav"])
music("m_ron",0.0,63.5-0,1) if False else None
