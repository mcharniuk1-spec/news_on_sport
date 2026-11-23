import json, os, mcp, sys
ids=json.load(open("v2_ids.json")); P=ids["P"]; TL=ids["TL"]; s=mcp.session(); f=lambda x: round(x*30)
def c(name,a,tl=None,quiet=False):
    r=mcp.call(s,name,{"projectId":P,"timelineId":tl or TL,**a}); t=r["result"]["content"][0]["text"]
    if r["result"].get("isError"): print("ERR",name,t[:300]); sys.exit(1)
    if not quiet: print("ok",name,t[:100])
    return json.loads(t) if t.startswith("{") else t
def imp(path,name=None,tl=None):
    a={"projectId":P,"source":{"path":os.path.abspath(path)},"name":name or os.path.basename(path)}
    r=mcp.call(s,"import_media",a); t=r["result"]["content"][0]["text"]
    if r["result"].get("isError"): print("ERR import",path,t); sys.exit(1)
    return json.loads(t)["mediaRef"]
M={}
for n in ["v2_c01","v2_c02","v2_flipA","v2_c04","v2_c05","v2_c06","v2_c07","v2_c08","v2_c10","v2_flipB","v2_c12C"]: M[n]=imp(f"clips/{n}.mp4")
M["card"]=imp("gfx/card_pitch.png")
for n in ["whoosh","hit","glitch","ding","womp","riser2"]: M[n]=imp(f"audio/{n}.wav")
M["music"]=imp("music/ph_35.wav")
for v in ("bm_george","bm_fable"):
    for i in range(1,10): M[f"{v}_{i}"]=imp(f"voice/p/{v}_{i}.wav")
M["white"]=json.loads(mcp.call(s,"import_media",{"projectId":P,"timelineId":TL,"source":{"matte":{"hex":"#FFFFFF"}}})["result"]["content"][0]["text"])["mediaRef"]
json.dump(M,open("v2_media.json","w"),indent=1)
shots=[("v2_c01",0,2),("v2_c02",2,4),("v2_flipA",4,6),("v2_c04",6,7.5),("v2_c05",7.5,9),("v2_c06",9,10.5),("v2_c07",10.5,12),("v2_c08",12,13),("card",13,15),("v2_c10",15,16),("v2_flipB",16,18),("v2_c12C",18,20)]
r=c("add_clips",{"entries":[{"mediaRef":M[n],"startFrame":f(a),"endFrame":f(b),"includeAudio":False} for n,a,b in shots]})
vid=[x["id"] for x in r["clips"]]
# audio tracks: music, voice, sfx1, sfx2
c("add_clips",{"entries":[{"mediaRef":M["music"],"startFrame":0,"endFrame":f(20)}]})
vst=[0.05,2.2,4.2,6.05,9.05,10.55,13.1,16.1,18.1]
c("add_clips",{"entries":[{"mediaRef":M[f"bm_george_{i+1}"],"startFrame":f(t)} for i,t in enumerate(vst)]})
x1=[(0.0,"hit"),(1.95,"whoosh"),(3.95,"whoosh"),(5.95,"whoosh"),(7.45,"whoosh"),(10.45,"whoosh"),(13.0,"hit"),(14.95,"whoosh"),(15.95,"whoosh"),(17.95,"whoosh")]
x2=[(4.3,"womp"),(9.0,"glitch"),(11.0,"riser2"),(15.0,"ding")]
for lst in (x1,x2): c("add_clips",{"entries":[{"mediaRef":M[n],"startFrame":f(t)} for t,n in lst]})
# texts
base={"fontName":"Impact","italic":False,"fontCase":"uppercase","color":"#FFFFFF","alignment":"center","outline":{"color":"#000000","width":16,"enabled":True},"shadow":{"enabled":True,"color":"#000000","opacity":0.7,"blur":6,"offset":{"x":0,"y":8}}}
def st(**k):
    d=json.loads(json.dumps(base)); d.update(k); return d
caps=[("RONALDINHO",0,1,100,.7),("IS 46",1,2,170,.7),("11 YEARS",2,3,130,.7),("NO FOOTBALL",3,4,100,.7),("A JOKE?!",4,6,140,.78),("THIRD\nDIVISION",6,7.5,110,.7),("WHITE\nSHIRT",7.5,9,130,.7),("FLARES",9,9.5,140,.7),("SMOKE",9.5,10,140,.7),("CHAOS",10,10.5,140,.7),("BRUTAL\nLEAGUE",10.5,12,120,.7),("THEN...",12,13,150,.7),("STILL\nGOT IT?",15,16,130,.7),("RETIRED?\nNEVER.",16,18,105,.78),("WHO'S NEXT?",18,19,105,.5),("YOUR\nGRANDAD?",19,20,105,.5)]
E=[{"content":t,"startFrame":f(a),"endFrame":f(b),"animation":"punchIn","style":st(fontSize=z),"transform":{"x":0.5,"y":y}} for t,a,b,z,y in caps]
E+=[{"content":"RAVENNA","startFrame":f(13),"endFrame":f(15),"animation":"slideUp","style":st(fontSize=105),"transform":{"x":0.5,"y":0.30}},
{"content":"2-0","startFrame":f(13.15),"endFrame":f(15),"animation":"popIn","style":st(fontSize=190,color="#FFD400",outline={"color":"#000000","width":20,"enabled":True}),"transform":{"x":0.5,"y":0.48}},
{"content":"FORLÌ","startFrame":f(13.3),"endFrame":f(15),"animation":"slideUp","style":st(fontSize=105),"transform":{"x":0.5,"y":0.66}},
{"content":"SERIE C","startFrame":f(13.6),"endFrame":f(15),"animation":"fadeIn","style":st(fontSize=80,color="#7CFF8A"),"transform":{"x":0.5,"y":0.78}},
{"content":"BREAKING","startFrame":0,"endFrame":f(4),"animation":"slideIn","style":st(fontSize=90,background={"enabled":True,"color":"#E10600","opacity":1,"cornerRadius":10,"padding":{"x":40,"y":16}},outline={"color":"#000000","width":0,"enabled":False}),"transform":{"x":0.5,"y":0.1}},
{"content":"TAG YOUR GRANDAD","startFrame":f(18.3),"endFrame":f(20),"animation":"popIn","style":st(fontSize=70,color="#000000",background={"enabled":True,"color":"#FFD400","opacity":1,"cornerRadius":10,"padding":{"x":30,"y":14}},outline={"color":"#000000","width":0,"enabled":False},shadow={"enabled":False}),"transform":{"x":0.5,"y":0.1}},
{"content":"😂","startFrame":f(4.5),"endFrame":f(6),"animation":"popIn","style":{"fontSize":200},"transform":{"x":0.8,"y":0.18}},
{"content":"💀","startFrame":f(12),"endFrame":f(13),"animation":"popIn","style":{"fontSize":300},"transform":{"x":0.5,"y":0.35}},
{"content":"🔥","startFrame":f(9.5),"endFrame":f(10.5),"animation":"popIn","style":{"fontSize":240},"transform":{"x":0.8,"y":0.2}}]
c("add_texts",{"entries":E})
# effects
ids_=vid
c("apply_effect",{"clipIds":ids_,"effects":[{"type":"stylize.grain","params":{"amount":0.2,"size":1.6}},{"type":"stylize.vignette","params":{"amount":0.3}},{"type":"blur.sharpen","params":{"amount":0.5}}]},quiet=True)
c("apply_effect",{"clipIds":[vid[5],vid[11]],"effects":[{"type":"stylize.glow","params":{"intensity":0.4,"radius":30,"threshold":0.55,"warmth":0.4}}]},quiet=True)
c("apply_effect",{"clipIds":[vid[6]],"effects":[{"type":"blur.motion","params":{"radius":6,"angle":0}}]},quiet=True)
real=[vid[i] for i in (0,1,3,4,5,6,7,9,11)]
c("apply_color",{"clipIds":real,"contrast":1.12,"saturation":1.15},quiet=True)
for i,(n,a,b) in enumerate(shots):
    d=f(b)-f(a)
    if n.startswith("v2_flip") or n=="card": z0,z1=1.0,1.1
    else: z0,z1=(1.0,1.2) if i%2==0 else (1.2,1.0)
    p=lambda z:(1-z)/2
    c("set_keyframes",{"clipId":vid[i],"property":"scale","keyframes":[[0,z0,z0],[d,z1,z1]]},quiet=True)
    c("set_keyframes",{"clipId":vid[i],"property":"position","keyframes":[[0,p(z0),p(z0)],[d,p(z1),p(z1)]]},quiet=True)
c("set_keyframes",{"clipId":vid[6],"property":"rotation","keyframes":[[0,0,"hold"],[6,-2.5,"hold"],[9,2.5,"hold"],[12,-2,"hold"],[15,1.5,"hold"],[18,0,"hold"]]},quiet=True)
# flash overlays on cuts
cuts=[f(b) for n,a,b in shots[:-1]]
r=c("add_clips",{"entries":[{"mediaRef":M["white"],"startFrame":x,"endFrame":x+5} for x in cuts]},quiet=True)
for k in r["clips"]: c("set_keyframes",{"clipId":k["id"],"property":"opacity","keyframes":[[0,0.85],[5,0]]},quiet=True)
# levels
tl=c("get_timeline",{},quiet=True); json.dump(tl,open("v2_timeline.json","w"))
by={t["label"]:[x["id"] for x in t["clips"]] for t in tl["tracks"] if t["type"]=="audio"}
print({k:len(v) for k,v in by.items()})
