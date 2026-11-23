import subprocess, sys, json, os
L=[ # name, src, ss, dur, mode ('x:NNN' crop 405x720 at x, or 'fill')
("r_walkout","pWDbmL8ovKw",14.0,2.0,"x:350"),("r_lineup","pWDbmL8ovKw",39.0,2.0,"x:420"),("r_ron10","pWDbmL8ovKw",48.0,1.5,"x:440"),
("r_celebrate","pWDbmL8ovKw",111.0,2.0,"x:560"),("r_hug","pWDbmL8ovKw",116.0,2.0,"x:300"),("r_clap","pWDbmL8ovKw",130.0,2.0,"x:380"),
("r_crowd","pWDbmL8ovKw",140.0,1.5,"x:400"),("r_board","pWDbmL8ovKw",227.0,2.5,"x:830"),
("f_run","GNiMxYb2oTA",12.0,2.0,"x:700"),("f_celebr","GNiMxYb2oTA",21.0,2.5,"x:380"),("f_seaman","GNiMxYb2oTA",28.5,2.5,"x:560"),("f_prep","GNiMxYb2oTA",40.5,2.0,"x:300"),("f_goalwide","GNiMxYb2oTA",38.0,3.0,"fill"),("f_hands","GNiMxYb2oTA",53.0,2.5,"x:460"),
("b_close1","Mb2-FS5NPdA",62.0,2.0,"x:420"),("b_smile","Mb2-FS5NPdA",155.0,2.0,"x:420"),("b_face","Mb2-FS5NPdA",186.0,2.0,"x:520"),("b_celebr","Mb2-FS5NPdA",196.0,2.0,"x:420"),
("u_trophy","Uf-6aRJk8q0",100.0,3.0,"x:600"),("u_stadium","Uf-6aRJk8q0",0.0,2.0,"fill"),
("y_kids","Y2YmbM5KgHg",0.0,2.5,"fill"),("y_skill","Y2YmbM5KgHg",9.0,3.0,"fill"),("y_dribble","Y2YmbM5KgHg",26.0,3.0,"fill"),("y_kid2","Y2YmbM5KgHg",36.0,3.0,"fill"),
("g_dunga","6Y9S3uj22a0",11.0,4.0,"fill"),
]
def run(n,src,ss,d,mode):
    out=f"lib/{n}.mp4"
    if os.path.exists(out): return
    if mode=="fill":
        vf="split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30,eq=brightness=-0.15[bg];[b]scale=1080:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,unsharp=3:3:0.5,fps=30,format=yuv420p"
    else:
        x=int(mode.split(":")[1]); vf=f"crop=405:720:{x}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.8,fps=30,format=yuv420p"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(d),"-i",f"src2/{src}.mp4","-an","-vf",vf,"-c:v","libx264","-crf","15","-preset","fast",out],check=True)
for l in L: run(*l)

from PIL import Image, ImageDraw
n=len(L); cols=12; W=Image.new("RGB",(110*cols*1,196*((n*3+cols-1)//cols)))
k=0
for l in L:
    for t in (0.1,l[3]/2,l[3]-0.2):
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(t),"-i",f"lib/{l[0]}.mp4","-frames:v","1","-vf","scale=110:196","/tmp/_f.png"]); im=Image.open("/tmp/_f.png").convert("RGB")
        if t==0.1: ImageDraw.Draw(im).text((2,2),l[0],fill=(255,255,0))
        W.paste(im,((k%cols)*110,(k//cols)*196)); k+=1
W.save("sheets/lib_check.png"); print(W.size)
