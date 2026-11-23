import sys, subprocess, os, glob, math, shutil
from PIL import Image, ImageDraw
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]))
def sheet(vid, t0=0, t1=None, n=48, cols=8, w=200):
    p=f"src2/{vid}.mp4"; d=dur(p); t1=t1 or d; step=(t1-t0)/n
    tmp=f"/tmp/ms_{vid}"; shutil.rmtree(tmp,ignore_errors=True); os.makedirs(tmp)
    subprocess.run(["ffmpeg","-v","error","-ss",str(t0),"-t",str(t1-t0),"-i",p,"-vf",f"fps=1/{step},scale={w}:-2","-frames:v",str(n),f"{tmp}/%03d.png"])
    fs=sorted(glob.glob(f"{tmp}/*.png")); ims=[Image.open(f).convert("RGB") for f in fs]
    h=ims[0].size[1]; rows=math.ceil(len(ims)/cols); S=Image.new("RGB",(cols*w,rows*h))
    for i,im in enumerate(ims):
        d_=ImageDraw.Draw(im); t=t0+i*step; d_.rectangle((0,0,46,12),fill=(0,0,0)); d_.text((2,0),f"{t:.0f}s",fill=(255,255,0))
        S.paste(im,((i%cols)*w,(i//cols)*h))
    S.save(f"sheets2/{vid}.jpg",quality=80); print(vid,f"{d:.0f}s step {step:.1f}")

if __name__=="__main__":
    n=int(os.environ.get("N","48")); cols=int(os.environ.get("COLS","8")); w=int(os.environ.get("W","200"))
    for a in sys.argv[1:]: sheet(a,n=n,cols=cols,w=w)
