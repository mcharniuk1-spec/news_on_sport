import subprocess, os
def sh(a): subprocess.run(a,check=True)
# name, srcfile, segstart, start, end, shots[(t0,t1,mode)] relative
IV=[("G1","mud/g_910-1110.mp4",910,945.0,958.5,[(0,13.5,"M")]),
    ("G4","mud/g_6110-6170.mp4",6110,6165.0,6168.6,[(0,3.6,"W")]),
    ("G5","mud/g_4790-4815.mp4",4790,4793.6,4801.5,[(0,0.6,"W"),(0.6,2.8,"G"),(2.8,4.5,"M"),(4.5,5.9,"G"),(5.9,7.9,"M")])]
VF={"G":"crop=405:720:340:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.8",
    "M":"crop=405:720:560:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.8",
    "W":"crop=1280:580:0:0,split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30,eq=brightness=-0.2[bg];[b]scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,unsharp=3:3:0.5"}
for n,src,s0,a,b,shots in IV:
    ss=a-s0; pieces=[]
    for i,(t0,t1,m) in enumerate(shots):
        p=f"lib/_iv_{n}_{i}.mp4"
        sh(["ffmpeg","-v","error","-y","-ss",str(ss+t0),"-t",str(t1-t0),"-i",src,"-an","-vf",VF[m]+",fps=30,format=yuv420p","-c:v","libx264","-crf","15","-preset","fast",p]); pieces.append(p)
    open(f"lib/_iv_{n}.txt","w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in pieces))
    sh(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"lib/_iv_{n}.txt","-c:v","libx264","-crf","15","-pix_fmt","yuv420p",f"lib/iv_{n}.mp4"])
    sh(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(b-a),"-i",src,"-vn","-af","highpass=f=80,loudnorm=I=-15:TP=-2:LRA=9,aresample=44100","-ac","2",f"lib/iv_{n}.wav"])
    print(n,round(float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"lib/iv_{n}.mp4"])),2))
