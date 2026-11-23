import subprocess, os
L=[("p_young","KyyuE7ClNI0",0.0,2.0,"x:350"),("p_roar44","KyyuE7ClNI0",43.5,2.0,"x:450"),("p_stand113","KyyuE7ClNI0",113.0,2.0,"x:550"),("p_roar181","KyyuE7ClNI0",180.5,2.0,"x:420"),
("p_arms194","KyyuE7ClNI0",193.5,2.0,"x:450"),("p_close244","KyyuE7ClNI0",244.0,2.0,"x:520"),("p_arms250","KyyuE7ClNI0",249.5,2.0,"x:300"),
("p_hand16","kwbH2dm1AXo",15.5,2.0,"y:600"),("p_hug30","kwbH2dm1AXo",29.5,2.0,"y:500"),("p_laugh54","kwbH2dm1AXo",53.5,2.0,"y:300"),("p_kick49","kwbH2dm1AXo",48.5,2.0,"y:520"),
("p_sit106","kwbH2dm1AXo",106.0,2.0,"y:700"),("p_walk117","kwbH2dm1AXo",115.5,2.0,"y:450")]
def run(n,src,ss,d,mode):
    out=f"lib/{n}.mp4"
    if os.path.exists(out): return
    k,x=mode.split(":"); x=int(x)
    vf=f"crop=405:720:{x}:0" if k=="x" else f"crop=360:640:{x}:70"
    vf+=",scale=1080:1920:flags=lanczos,unsharp=5:5:0.8,fps=30,format=yuv420p"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(d),"-i",f"src2/{src}.mp4","-an","-vf",vf,"-c:v","libx264","-crf","15","-preset","fast",out],check=True)
for l in L: run(*l)
from PIL import Image, ImageDraw
cols=13; n=len(L); W=Image.new("RGB",(100*cols,178*((n*3+cols-1)//cols))); k=0
for l in L:
    for t in (0.1,l[3]/2,l[3]-0.2):
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(t),"-i",f"lib/{l[0]}.mp4","-frames:v","1","-vf","scale=100:178","/tmp/_f.png"]); im=Image.open("/tmp/_f.png").convert("RGB")
        if t==0.1: ImageDraw.Draw(im).text((2,2),l[0][2:],fill=(255,255,0))
        W.paste(im,((k%cols)*100,(k//cols)*178)); k+=1
W.save("sheets/lib3_check.png")
