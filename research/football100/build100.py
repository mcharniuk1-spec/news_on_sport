"""Build one Short in Palmier from scripts/NNN.json + voice + footage. Usage: build100.py NNN  -> builds/NNN_ids.json"""
import json, sys, os, glob, subprocess, time
VB="<PROJECT_ROOT>/research/video_build"; H="<PROJECT_ROOT>/research/football100"
sys.path.insert(0,VB); import mcp
no=int(sys.argv[1]); J=json.load(open(f"{H}/scripts/{no:03d}.json")); FPS=30; f=lambda s:int(round(s*FPS))
dur=lambda p: float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]))
L=J["lines"]; n=len(L)
# ---- voice: one full file + line starts
vf=f"{H}/voice/{no:03d}_full.wav"
if J["voice"]=="kokoro":
    ds=json.load(open(f"{H}/voice/{no:03d}.json")); GAP=0.3
    if not os.path.exists(vf):
        ins=sum([["-i",f"{H}/voice/{no:03d}_{i+1}.wav"] for i in range(n)],[])
        fc="".join(f"[{i}]apad=pad_dur={GAP}[a{i}];" for i in range(n))+"".join(f"[a{i}]" for i in range(n))+f"concat=n={n}:v=0:a=1[o]"
        subprocess.run(["ffmpeg","-v","error","-y",*ins,"-filter_complex",fc,"-map","[o]",vf],check=True)
    starts=[0.0]
    for d in ds[:-1]: starts.append(starts[-1]+d+GAP)
else:
    vf=glob.glob(f"{H}/voice/{no:03d}_el.*")[0]; tot=dur(vf); ch=[len(l["vo"]) for l in L]; c=sum(ch); starts=[]; acc=0
    for x in ch: starts.append(tot*acc/c); acc+=x
vtot=dur(vf); END=vtot+0.5; starts_e=starts+[END]
# ---- shots
clips=sorted(glob.glob(f"{H}/footage/{no:03d}/c*.mp4")); assert clips,"no footage"
cd={c:dur(c) for c in clips}; off={c:0.0 for c in clips}; shots=[]; ci=0; fspans=[]
flips={ins["after_line"]+1:f"{H}/clips/flip_{no:03d}_{k+1}.mp4" for k,ins in enumerate(J.get("inserts",[]))}
outro_d=max(2.8,END-starts[-1]); outro=f"{H}/clips/outro2_{int(outro_d*10)}.mp4"
if not os.path.exists(outro):
    subprocess.run(["ffmpeg","-v","error","-y","-i",f"{H}/clips/hf_outro.mp4","-vf",f"tpad=stop_mode=clone:stop_duration={max(0,outro_d-2.8)+0.4:.2f},fps=30","-t",f"{outro_d+0.4:.2f}","-an","-c:v","libx264","-crf","18",outro],check=True)
for i in range(n):
    a,b=starts_e[i],starts_e[i+1]
    if i==n-1: shots.append((outro,a,a+outro_d,0,"outro")); continue
    t=a
    if i in flips and os.path.exists(flips[i]): fspans.append((flips[i],t,min(t+2.0,b)))  # flip overlays the first 2.0 s of the line; the footage plan below stays the same as without flips
    span=b-t
    if span<=0.3: continue
    k=max(1,round(span/3.0)); L2=span/k
    for q in range(k):
        c=clips[ci%len(clips)]; ci+=1; w=L2+0.3
        if off[c]+w>cd[c]: off[c]=0.0
        shots.append((c,t+q*L2,t+(q+1)*L2,off[c],"foot")); off[c]+=w
# cut the flip spans out of the footage plan (underlying shots keep their clips and source offsets)
if fspans:
    out=[]
    for sh in shots:
        p_,a_,b_,o_,k_=sh
        if k_!="foot": out.append(sh); continue
        pieces=[(a_,b_,o_)]
        for _,fa,fb in fspans:
            nxt=[]
            for (x,y,oo) in pieces:
                if fb<=x or fa>=y: nxt.append((x,y,oo)); continue
                if fa>x: nxt.append((x,fa,oo))
                if fb<y: nxt.append((fb,y,oo+(fb-x)))
            pieces=nxt
        out+= [(p_,x,y,oo,"foot") for x,y,oo in pieces if y-x>0.05]
    out+=[(fp,fa,fb,0,"flip") for fp,fa,fb in fspans]
    out.sort(key=lambda z:z[1])
    for j in range(len(out)-1):   # close slivers: stretch a shot to the next start, never leave a hole
        if out[j+1][1]>out[j][2] and out[j][4]!="flip": out[j]=(out[j][0],out[j][1],out[j+1][1],out[j][3],out[j][4])
    shots=out
total=shots[-1][2]
# ---- project
s=mcp.session()
def call(nm,a):
    r=mcp.call(s,nm,a); t=r["result"]["content"][0]["text"]
    if r["result"].get("isError"): print("ERR",nm,t[:300]); sys.exit(1)
    return json.loads(t) if t.startswith("{") else t
P=call("manage_project",{"action":"create","name":f"F100 {no:03d} {time.strftime('%H%M%S')}","fps":30,"aspectRatio":"9:16","quality":"1080p"}); TL=P["timelines"][0]["timelineId"]; P=P["id"]
call("set_project_settings",{"projectId":P,"timelineId":TL,"width":1080,"height":1920})
M={}
def imp(p):
    if p not in M: M[p]=call("import_media",{"projectId":P,"source":{"path":os.path.abspath(p)},"name":os.path.basename(p)})["mediaRef"]
    return M[p]
OV=6  # dissolve overlap in frames
def place(idx):
    ents=[]
    for k in idx:
        p,a,b,o,kind=shots[k]; sa=f(a)-(OV if k>0 else 0)
        if kind=="foot": ents.append({"mediaRef":imp(p),"startFrame":sa,"source":[round(o,2),round(o+(f(b)-sa)/FPS,2)],"includeAudio":False})
        else: ents.append({"mediaRef":imp(p),"startFrame":sa,"endFrame":min(f(b),sa+int(dur(p)*FPS)-1),"includeAudio":False})
    return call("add_clips",{"projectId":P,"timelineId":TL,"entries":ents})["clips"]
ev=[k for k in range(len(shots)) if k%2==0]; od=[k for k in range(len(shots)) if k%2==1]
cev=place(ev); cod=place(od) if od else []
vid={}
for k,c in zip(ev,cev): vid[k]=c["id"]
for k,c in zip(od,cod): vid[k]=c["id"]
# camera moves + dissolves
for k,(p,a,b,o,kind) in enumerate(shots):
    d=f(b)-(f(a)-(OV if k>0 else 0))
    if kind=="foot" or kind=="flip":
        z0,z1=(1.0,1.22) if k%2==0 else (1.24,1.0)
        if k%5==3: z0,z1=1.0,1.4
        pp=lambda z:(1-z)/2
        call("set_keyframes",{"projectId":P,"timelineId":TL,"clipId":vid[k],"property":"scale","keyframes":[[0,z0,z0],[d,z1,z1]]})
        call("set_keyframes",{"projectId":P,"timelineId":TL,"clipId":vid[k],"property":"position","keyframes":[[0,pp(z0),pp(z0)],[d,pp(z1),pp(z1)]]})
    if k%2==1 and k>0:
        call("set_keyframes",{"projectId":P,"timelineId":TL,"clipId":vid[k],"property":"opacity","keyframes":[[0,0],[OV,1],[max(OV+1,d-OV),1],[d,0 if k<len(shots)-1 else 1]]})
real=[vid[k] for k,x in enumerate(shots) if x[4]=="foot"]
call("apply_effect",{"projectId":P,"timelineId":TL,"clipIds":real,"effects":[{"type":"stylize.grain","params":{"amount":0.12,"size":1.6}},{"type":"stylize.vignette","params":{"amount":0.28}},{"type":"blur.sharpen","params":{"amount":0.5}}]})
call("apply_color",{"projectId":P,"timelineId":TL,"clipIds":real,"contrast":1.1,"saturation":1.1})
# ---- audio
def audio(items):
    return [x["id"] for x in call("add_clips",{"projectId":P,"timelineId":TL,"entries":[{"mediaRef":imp(p),"startFrame":f(at)} for p,at in items]})["clips"]]
voice=audio([(vf,0.1)])
music=audio([(f"{VB}/music/phonk_full.wav",0.0)])
call("set_clip_properties",{"projectId":P,"timelineId":TL,"clipIds":music,"durationFrames":f(total)})
call("set_clip_properties",{"projectId":P,"timelineId":TL,"clipIds":music,"volumeDb":-20})
call("set_keyframes",{"projectId":P,"timelineId":TL,"clipId":music[0],"property":"volumeDb","keyframes":[[0,-20],[f(total)-24,-20],[f(total)-1,-42]]})
wh=f"{VB}/audio/whoosh.wav" if os.path.exists(f"{VB}/audio/whoosh.wav") else None
if wh:
    w=audio([(wh,max(0,shots[k][1]-0.1)) for k in range(1,len(shots)) if shots[k][4]!="outro" and k%2==0])
    if w: call("set_clip_properties",{"projectId":P,"timelineId":TL,"clipIds":w,"volumeDb":-17})
# ---- on-screen cards (appear when voiced, hold >= 2 s)
E=[]
cs={"fontName":"Impact","fontCase":"uppercase","color":"#FFC247","alignment":"center","fontSize":112,"outline":{"color":"#0D1B32","width":16,"enabled":True},"shadow":{"enabled":True,"color":"#000000","opacity":0.5,"blur":10,"offset":{"x":0,"y":8}}}
for i in range(n-1):
    if L[i].get("card"):
        a=starts[i]+0.15; b=min(a+max(2.2,0),starts_e[i+1]+0.9 if i<n-2 else total-outro_d)
        if b-a>=1.2: E.append({"content":L[i]["card"],"startFrame":f(a),"endFrame":f(b),"animation":"popIn","style":cs,"transform":{"x":0.5,"y":0.2}})
if E: call("add_texts",{"projectId":P,"timelineId":TL,"entries":E})
# ---- word-by-word captions: <=4 words, 2 lines, active word highlighted
call("add_captions",{"projectId":P,"timelineId":TL,"language":"en-GB","animation":"karaoke","highlightColor":"#FFC247","maxWords":4,"lines":2,"maximumGapSeconds":0.3,"endFrame":f(total-outro_d+0.4),
  "style":{"fontName":"Impact","fontCase":"uppercase","color":"#FFFFFF","fontSize":84,"alignment":"center","outline":{"color":"#000000","width":14,"enabled":True},"shadow":{"enabled":True,"color":"#000000","opacity":0.55,"blur":8,"offset":{"x":0,"y":6}}},
  "transform":{"x":0.5,"y":0.68}})
json.dump({"P":P,"TL":TL,"total":total,"no":no},open(f"{H}/builds/{no:03d}_ids.json","w")); print("built",no,round(total,1),"s",len(shots),"shots")
