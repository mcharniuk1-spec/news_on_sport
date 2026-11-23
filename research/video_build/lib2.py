import subprocess, os
L=[("m_celtic_goal","fEic1OBV21Q",52.0,2.0,"c:400"),("m_celtic_celeb","fEic1OBV21Q",118.0,2.0,"c:300"),("m_celtic_wide","fEic1OBV21Q",59.0,2.0,"c:480"),
("m_leipzig_10","HH3nm10QatA",98.5,2.0,"c:380"),("m_leipzig_net","HH3nm10QatA",84.0,2.0,"c:330"),("m_leipzig_run","HH3nm10QatA",74.0,2.0,"c:400"),
("m_chelsea_43","40Y8CmFZOOU",12.0,2.0,"x:430"),("m_chelsea_run","40Y8CmFZOOU",33.0,2.0,"x:430"),("m_chelsea_bench","40Y8CmFZOOU",7.0,2.0,"x:430"),
("m_spurs_shirt","dCeVojfr5TA",187.0,2.5,"x:430"),("m_spurs_int","NAKVkMh0fs0",7.0,3.0,"x:440"),("m_spurs_port","NAKVkMh0fs0",13.0,2.5,"x:480"),("m_spurs_flag","NAKVkMh0fs0",74.0,2.5,"x:430"),
("m_spurs_int2","NAKVkMh0fs0",47.0,3.0,"x:440"),("m_celtic_85","fEic1OBV21Q",85.0,2.0,"c:350"),("m_leipzig_64","HH3nm10QatA",64.0,2.0,"c:350"),("m_leipzig_5","HH3nm10QatA",5.0,2.0,"c:300"),("m_chelsea_30","40Y8CmFZOOU",30.0,3.0,"x:430"),("m_chelsea_19","40Y8CmFZOOU",19.0,2.0,"x:430")]
def run(n,src,ss,d,mode):
    out=f"lib/{n}.mp4"
    if os.path.exists(out): return
    kind,x=mode.split(":"); x=int(x)
    if kind=="c": vf=f"crop=340:605:{x}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.8,fps=30,format=yuv420p"   # cuts off score bar
    else: vf=f"crop=405:720:{x}:0,scale=1080:1920:flags=lanczos,unsharp=5:5:0.8,fps=30,format=yuv420p"
    subprocess.run(["ffmpeg","-v","error","-y","-ss",str(ss),"-t",str(d),"-i",f"src2/{src}.mp4","-an","-vf",vf,"-c:v","libx264","-crf","15","-preset","fast",out],check=True)
for l in L: run(*l)
from PIL import Image, ImageDraw
cols=14; n=len(L); W=Image.new("RGB",(100*cols,178*((n*3+cols-1)//cols))); k=0
for l in L:
    for t in (0.1,l[3]/2,l[3]-0.2):
        subprocess.run(["ffmpeg","-v","error","-y","-ss",str(t),"-i",f"lib/{l[0]}.mp4","-frames:v","1","-vf","scale=100:178","/tmp/_f.png"]); im=Image.open("/tmp/_f.png").convert("RGB")
        if t==0.1: ImageDraw.Draw(im).text((2,2),l[0][2:],fill=(255,255,0))
        W.paste(im,((k%cols)*100,(k//cols)*178)); k+=1
W.save("sheets/lib2_check.png")
