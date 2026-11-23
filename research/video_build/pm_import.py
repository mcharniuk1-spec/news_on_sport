import json, os, glob, mcp
P="515558C1"; TL="6317CE8E"
s=mcp.session()
files=sorted(glob.glob("clips/*.mp4"))+["gfx/gen_01_cake.png","gfx/gen_02_boots.png","gfx/card_pitch.png"]+sorted(glob.glob("audio/*.wav"))
for f in files:
    r=mcp.call(s,"import_media",{"projectId":P,"source":{"path":os.path.abspath(f)},"name":os.path.basename(f)})
    print(f, r["result"]["content"][0]["text"][:160])
