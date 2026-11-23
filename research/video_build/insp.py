import json, mcp, base64, glob, os
from PIL import Image
P="515558C1"; TL="6317CE8E"; s=mcp.session()
for f in glob.glob("sheets/insp_*.jpg"): os.remove(f)
r=mcp.call(s,"inspect_timeline",{"projectId":P,"timelineId":TL,"startFrame":0,"endFrame":552,"maxFrames":12})
n=0
for blk in r["result"]["content"]:
    if blk["type"]=="image": open(f"sheets/insp_{n:02d}.jpg","wb").write(base64.b64decode(blk["data"])); n+=1
ims=[Image.open(f).convert("RGB") for f in sorted(glob.glob("sheets/insp_*.jpg"))]
w,h=ims[0].size; sc=360/h; ims=[i.resize((int(w*sc),360)) for i in ims]
W=Image.new("RGB",(sum(i.size[0] for i in ims[:6]),720)); x=0
for k,i in enumerate(ims):
    if k==6: x=0
    W.paste(i,(x,(k//6)*360)); x+=i.size[0]
W.save("sheets/insp_all.png")
