import json, os, sys, subprocess, math, mcp
which=sys.argv[1]; f=lambda x: round(x*30)
def dur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]))
def path(n):
    if n.startswith("hf_") or n.startswith("v2_") or n.startswith("flip2_"): return f"clips/{n}.mp4"
    return f"lib/{n}.mp4"
SPECS={
"ron":{"name":"Ronaldinho at 46 v3b","music":"music/m_ron.wav","blocks":[
 {"vo":"ron_1","clips":[("r_lineup",2.0),("r_ron10",1.5),("r_walkout",2.0),("r_crowd",1.5)],"caps":[("RONALDINHO",.2,2.5,92),("46 YEARS OLD",2.5,4.8,120),("SERIE C",4.8,7.0,150)],"sfx":[("whistle",0.0)]},
 {"vo":"ron_2","clips":[("f_celebr",2.0),("hf_trophies",6.0),("u_trophy",3.0)],"caps":[("WORLD CUP 2002",0.0,2.0,100)]},
 {"vo":"ron_3","clips":[("y_kids",2.5),("hf_youth",5.0),("SLOT:R1:y_skill",2.0),("y_kid2",3.0)],"caps":[("LITTLE RONALDO",.2,2.4,100),("TWENTY-THREE",7.7,9.7,110)]},
 {"vo":"ron_4","clips":[("f_run",2.0),("f_seaman",2.0),("SLOT:R2:f_hands",2.0),("f_hands",2.5),("f_prep",2.0),("f_goalwide",2.0)],"caps":[("WORLD CUP 2002",0.0,2.0,100),("40 YARDS",2.0,4.0,130),("THE CURL",4.0,6.0,130),("SENT OFF",8.5,11.0,130)],"sfx":[("kick1",4.0)]},
 {"vo":"ron_5","clips":[("b_close1",2.0),("b_celebr",2.0),("b_smile",2.0),("u_stadium",2.0),("u_trophy",2.5)],"caps":[("BARCELONA",0.0,2.0,110),("BALLON D'OR 2005",2.0,6.0,100),("BERNABÉU\nOVATION",6.0,10.5,110)],"sfx":[("goal_crowd",0.0)]},
 {"vo":"ron_6","clips":[("hf_years",4.5),("v2_c04",1.5),("v2_c10",1.0),("v2_c12",2.0),("v2_c08",1.0)],"caps":[("RETIRED 2018",6.0,9.5,110)]},
 {"vo":"ron_7","clips":[("hf_pyramid",4.0),("v2_c01",2.0),("v2_c02",2.0),("v2_c05",1.5),("r_hug",2.0),("v2_c06",1.5),("r_clap",2.0),("v2_c07",1.5),("r_crowd",1.5)],"caps":[("OWNER: CIPRIANI",4.0,7.0,100),("PLAYER +\nSHAREHOLDER",9.5,13.5,100),("GOAL NO. 300?",14.5,18.0,110)]},
 {"vo":"ron_8","clips":[("v2_c06",1.5),("r_celebrate",2.0),("r_board",2.5),("hf_score",3.0)],"caps":[("FLARES. SMOKE.",0.0,2.5,100),("CORNER: 19'",2.5,4.5,110)],"sfx":[("whistle",0.0),("goal_crowd",6.0)]},
 {"vo":"ron_9","clips":[("SLOT:R3:v2_c12",2.0),("v2_c12",2.0),("v2_c07",1.5),("r_crowd",1.5)],"caps":[("NO MORE EXCUSES",0.0,3.0,100),("SUNDAY LEAGUE",3.5,7.0,110)]}]},
"mud":{"name":"Mudryk and the dump truck v1c","music":"music/m_mud.wav","blocks":[
 {"vo":"mud_1","clips":[("m_celtic_celeb",2.0),("m_leipzig_10",2.0),("m_celtic_goal",2.0)],"caps":[("€100M?",.3,3.0,150),("A DUMP TRUCK",3.0,6.0,100)]},
 {"iv":"G1","clips":[("iv_G1",15.0)],"caps":[("It's like a dump truck pulling up\nwith all the pressure…",1.6,8.0),("…and slowly tipping it onto you.\nAnd you feel it.",8.0,15.0)],"credit":"INTERVIEW: DMYTRO GORDON, NOV 2026"},
 {"flip":True,"clips":[("SLOT:M3:m_chelsea_19",2.0)]},
 {"vo":"mud_2","clips":[("m_celtic_wide",2.0),("m_chelsea_43",2.0),("hf_transfer",4.5),("m_chelsea_run",2.0),("m_leipzig_net",1.0)],"caps":[("SHAKHTAR → CHELSEA",0.0,3.0,80)]},
 {"vo":"mud_3","clips":[("m_leipzig_run",2.0),("m_leipzig_64",2.0),("m_chelsea_30",2.0),("m_spurs_port",2.0)],"caps":[("PACE",.3,3.0,150),("FASTEST IN THE CL",3.5,8.0,90)]},
 {"iv":"G3","clips":[("iv_G3",14.2)],"caps":[("How fast do you run 100 metres?",0.0,1.5),("Never ran it.",1.6,3.5),("What's your speed record?",6.5,8.4),("37.4 kilometres an hour.",8.8,14.2)]},
 {"flip":True,"clips":[("SLOT:M1:m_leipzig_run",2.0)]},
 {"vo":"mud_4","clips":[("m_chelsea_bench",2.0),("m_chelsea_19",3.0)],"caps":[("£400K A MONTH",.3,5.0,100)]},
 {"iv":"G4","clips":[("iv_G4",10.5)],"caps":[("Reports say your Chelsea salary was\n£400,000 a month. Yes or no?",0.0,6.6),("That's gross.",8.6,10.5)]},
 {"vo":"mud_5","clips":[("m_spurs_port",2.0),("m_chelsea_43",1.5)],"caps":[("GROSS = BEFORE TAX",0.0,3.5,80)]},
 {"iv":"G5","clips":[("iv_G5",12.0)],"caps":[("…the millionaires are all\nrunning from England, right?",0.0,1.8),("Yes.",2.2,3.2),("How much tax, by the way?",3.8,5.6),("Forty-five percent.",6.5,7.8),("Forty-five percent.",8.0,9.2),("Inhuman.",9.8,11.5)]},
 {"flip":True,"clips":[("SLOT:M2:m_spurs_flag",2.0)]},
 {"vo":"mud_7","clips":[("hf_wait",5.0),("m_spurs_shirt",2.5),("m_spurs_int",2.5),("m_spurs_int2",2.0)],"caps":[("TOTTENHAM LOAN",5.0,8.0,90)]},
 {"vo":"mud_8","clips":[("m_leipzig_run",2.0),("m_spurs_int2",2.0),("m_chelsea_run",2.0),("m_celtic_goal",2.0),("m_spurs_flag",1.0)],"caps":[("45% TAX",0.0,3.0,130),("37.4 KM/H",3.0,6.0,110),("THE TAXMAN WINS",6.0,9.0,90)]}]}}

SPECS["ron2"]={"name":"Ronaldinho v4","music":"music/m_ron2.wav","blocks":[
 {"vo":"ron2_1","clips":[("r_lineup",2.0),("r_ron10",1.5),("r_walkout",2.0),("r_crowd",1.0)],"caps":[("RONALDINHO",.2,2.2,92),("46",2.2,4.0,200),("SERIE C",4.0,6.5,140)],"sfx":[("whistle",0.0)]},
 {"vo":"ron2_2","clips":[("f_celebr",1.5),("hf_trophies",5.0)],"caps":[("WORLD CUP",0.0,1.5,100)]},
 {"vo":"ron2_3","clips":[("y_kids",2.0),("SLOT:R1:y_skill",2.0),("y_skill",2.0)],"caps":[("AGE 13",0.2,2.0,120),("23–0",2.0,4.0,170)]},
 {"vo":"ron2_4","clips":[("f_run",1.5),("f_seaman",1.5),("SLOT:R2:f_hands",2.0),("f_hands",2.0),("f_prep",1.5),("f_goalwide",1.0)],"caps":[("2002 WORLD CUP",0.0,1.5,90),("40 YARDS",1.5,3.0,130),("THE CURL",3.0,5.0,130),("SENT OFF",6.5,9.5,130)],"sfx":[("kick1",3.0)]},
 {"vo":"ron2_5","clips":[("hf_years",4.5),("v2_c04",1.0),("v2_c10",1.0)],"caps":[]},
 {"vo":"ron2_6","clips":[("hf_pyramid",3.5),("v2_c01",2.0),("r_hug",2.0),("v2_c05",1.0),("v2_c06",1.0)],"caps":[("SHAREHOLDER + PLAYER",6.0,9.5,90)]},
 {"vo":"ron2_7","clips":[("v2_c06",1.5),("r_celebrate",2.0),("hf_score",2.5)],"caps":[("FLARES. SMOKE.",0.0,2.0,100),("CORNER: 19'",2.0,3.5,100)],"sfx":[("whistle",0.0),("goal_crowd",3.0)]},
 {"vo":"ron2_8","clips":[("SLOT:R3:v2_c12",2.0),("v2_c12",2.0),("v2_c07",1.5),("r_crowd",1.0)],"caps":[("NO MORE EXCUSES",0.0,3.0,100),("SUNDAY LEAGUE",3.5,6.5,110)]}]}
SPECS["mud2"]={"name":"Mudryk v2","music":"music/m_mud2.wav","blocks":[
 {"vo":"mud2_1","clips":[("m_celtic_celeb",2.0),("m_leipzig_10",2.0),("m_celtic_goal",1.0)],"caps":[("€100M?",.3,2.5,150),("A DUMP TRUCK",2.5,5.0,100)]},
 {"iv":"G1","clips":[("iv_G1",13.5)],"caps":[("It's like a dump truck pulling up\nwith all the pressure…",0.2,6.5),("…and slowly tipping it onto you.\nAnd you feel it.",6.5,13.5)],"credit":"INTERVIEW: DMYTRO GORDON, NOV 2026"},
 {"flip":True,"clips":[("SLOT:M3:m_chelsea_19",2.0)]},
 {"vo":"mud2_2","clips":[("m_celtic_wide",1.5),("hf_transfer",4.5),("m_chelsea_43",1.5)],"caps":[("SHAKHTAR → CHELSEA",0.0,1.5,70)]},
 {"vo":"mud2_3","clips":[("m_leipzig_64",1.5),("SLOT:M1:m_leipzig_run",2.0),("m_leipzig_run",2.0)],"caps":[("37.4 KM/H",.2,5.5,120)]},
 {"vo":"mud2_4","clips":[("m_chelsea_bench",2.0),("m_chelsea_19",2.0)],"caps":[("£400K A MONTH",.3,4.0,100)]},
 {"iv":"G4","clips":[("iv_G4",3.6)],"caps":[("Yes or no?",0.0,1.0),("That's gross.",1.7,3.6)]},
 {"vo":"mud2_5","clips":[("m_spurs_port",2.0)],"caps":[("TAX?",0.0,1.7,150)]},
 {"iv":"G5","clips":[("iv_G5",7.9)],"caps":[("How much tax, by the way?",0.2,1.9),("Forty-five percent.",2.9,4.1),("Forty-five percent.",4.5,5.7),("Inhuman.",6.1,7.9)]},
 {"flip":True,"clips":[("SLOT:M2:m_spurs_flag",2.0)]},
 {"vo":"mud2_6","clips":[("hf_wait",4.0),("m_spurs_shirt",2.0)],"caps":[("TOTTENHAM LOAN",4.0,6.0,90)]},
 {"vo":"mud2_7","clips":[("m_spurs_int",2.5),("m_chelsea_run",2.0),("m_celtic_goal",1.5),("m_spurs_int2",1.5)],"caps":[("45% TAX",0.0,2.5,130),("37.4 KM/H",2.5,5.0,110),("THE TAXMAN WINS",5.0,7.5,90)]}]}
SPECS["por"]={"name":"Ronaldo quits Portugal v1","music":"music/m_por.wav","blocks":[
 {"vo":"por_1","clips":[("p_roar181",1.5),("hf_stats",4.5),("hf_seven",3.0),("p_walk117",1.5)],"caps":[],"sfx":[("goal_crowd",0.0)]},
 {"vo":"por_2","clips":[("p_roar44",2.0),("p_kick49",2.0)],"caps":[("EURO 2016 CAPTAIN",0.2,2.0,80),("23 YEARS",2.0,4.0,130)]},
 {"vo":"por_3","clips":[("p_close244",2.0),("p_young",1.5),("p_laugh54",2.0),("p_roar44",1.5)],"caps":[("JORGE JESUS?",0.0,2.5,110),("REPORTED,\nNOT CONFIRMED",3.0,7.0,90)]},
 {"vo":"por_4","clips":[("p_walk117",2.0),("p_young",1.0)],"caps":[("STILL PLAYING",0.0,3.0,100)]},
 {"vo":"por_5","clips":[("p_laugh54",2.0),("p_roar181",2.0),("p_walk117",1.5)],"caps":[("WHO WEARS 7?",0.0,5.5,130)]}]}
S=SPECS[which]; ids={}
if os.path.exists(f"v3_{which}_ids.json"): os.remove(f"v3_{which}_ids.json")
s=mcp.session()
def call(n,a):
    r=mcp.call(s,n,a); t=r["result"]["content"][0]["text"]
    if r["result"].get("isError"): print("ERR",n,t[:300]); sys.exit(1)
    return json.loads(t) if t.startswith("{") else t
P=call("manage_project",{"action":"create","name":S["name"]+" "+__import__("time").strftime("%H%M%S"),"fps":30,"aspectRatio":"9:16","quality":"1080p"}); TL=P["timelines"][0]["timelineId"]; P=P["id"]
call("set_project_settings",{"projectId":P,"timelineId":TL,"width":1080,"height":1920})
M={}
def imp(p,name=None,tl=None):
    k=(p)
    if k in M: return M[k]
    a={"projectId":P,"source":{"path":os.path.abspath(p)},"name":name or os.path.basename(p)}
    M[k]=call("import_media",a)["mediaRef"]; return M[k]
# resolve blocks
t=0.0; shots=[]; vos=[]; ivs=[]; caps=[]; sfx=[]; bounds=[]; ivranges=[]
for bi,b in enumerate(S["blocks"]):
    start=t; bounds.append(start)
    for c,d in b["clips"]:
        name=c; 
        if c.startswith("SLOT:"):
            _,sid,fb=c.split(":"); fl=f"clips/flip2_{sid}.mp4"; name=f"flip2_{sid}" if os.path.exists(fl) else fb
        p=path(name); nat=dur(p); d2=min(d,nat) if not name.startswith("hf_") else min(d,nat)
        shots.append((p,round(t,2),round(t+d2,2),name)); t+=d2
    end=t
    if "vo" in b: vos.append((f"v3/{b['vo']}.wav",start+0.1))
    if "iv" in b: ivs.append((f"lib/iv_{b['iv']}.wav",start)); ivranges.append((start,end))
    for cap in b.get("caps",[]):
        if "iv" in b: caps.append((cap[0],start+cap[1],start+cap[2],62,0.82,False))
        else: caps.append((cap[0],start+cap[1],min(start+cap[2],end),cap[3],0.70,True))
    if b.get("credit"): caps.append((b["credit"],start,start+4,36,0.10,False))
    for n,off in b.get("sfx",[]): sfx.append((n,start+off))
    sfx.append(("whoosh",max(0,start-0.05)))
total=t; print("total",round(total,1),"s; blocks at",[round(x,1) for x in bounds])
# video
ents=[]
for p,a,b,name in shots: ents.append({"mediaRef":imp(p),"startFrame":f(a),"endFrame":f(b),"includeAudio":False})
r=call("add_clips",{"projectId":P,"timelineId":TL,"entries":ents}); vid=[x["id"] for x in r["clips"]]
def audio(files):
    r=call("add_clips",{"projectId":P,"timelineId":TL,"entries":[{"mediaRef":imp(p),"startFrame":f(at)} for p,at in files]}); return [x["id"] for x in r["clips"]]
music=audio([(S["music"],0.0)])
# trim music to total length
call("set_clip_properties",{"projectId":P,"timelineId":TL,"clipIds":music,"durationFrames":f(total)})
voice=audio(vos)
ivc=audio(ivs) if ivs else []
SFXF={"whoosh":"audio/whoosh.wav","hit":"audio/hit.wav","whistle":"sfx/whistle.wav","kick1":"sfx/kick1.mp3","goal_crowd":"sfx/goal_crowd.mp3","sansiro":"sfx/sansiro.mp3"}
sf=[]; goal=[(n,a) for n,a in sfx if n in ("goal_crowd","sansiro")]; other=[(n,a) for n,a in sfx if n not in ("goal_crowd","sansiro")]
# non-overlapping whoosh track: dedupe within 0.6s
other.sort(key=lambda x:x[1]); keep=[]; last=-9
for n,a in other:
    if a-last>=0.7 or n!="whoosh": keep.append((n,a)); last=a if True else last
sfx1=audio([(SFXF[n],a) for n,a in keep if n in ("whoosh",)]) 
sfx2=audio([(SFXF[n],a) for n,a in keep if n not in ("whoosh",)]) if any(n not in ("whoosh",) for n,a in keep) else []
crowd=audio([(SFXF[n],a) for n,a in goal]) if goal else []
amb=audio([("sfx/ambience.mp3",0.0)]); call("set_clip_properties",{"projectId":P,"timelineId":TL,"clipIds":amb,"durationFrames":f(total)})
# levels
def vol(ids,db):
    if ids: call("set_clip_properties",{"projectId":P,"timelineId":TL,"clipIds":ids,"volumeDb":db})
vol(music,-15); vol(voice,0); vol(ivc,-1); vol(sfx1,-14); vol(sfx2,-8); vol(crowd,-12); vol(amb,-27)
# crowd swell length cap
if crowd: call("set_clip_properties",{"projectId":P,"timelineId":TL,"clipIds":crowd,"durationFrames":f(5)})
# duck music during interviews
kf=[[0,-15]]
for a,b in ivranges:
    kf+= [[f(a)-6,-15],[f(a),-30],[f(b)-1,-30],[f(b)+8,-15]]
if ivranges: call("set_keyframes",{"projectId":P,"timelineId":TL,"clipId":music[0],"property":"volumeDb","keyframes":sorted(kf)})
# captions
base={"fontName":"Impact","italic":False,"fontCase":"uppercase","color":"#FFFFFF","alignment":"center","outline":{"color":"#000000","width":16,"enabled":True},"shadow":{"enabled":True,"color":"#000000","opacity":0.7,"blur":6,"offset":{"x":0,"y":8}}}
E=[]
for tx,a,b,sz,y,up in caps:
    st=json.loads(json.dumps(base)); st["fontSize"]=sz
    if not up: st["fontCase"]="mixed"; st["outline"]["width"]=9; st["bold"]=True
    if sz==36: st["fontCase"]="uppercase"; st["outline"]["width"]=5
    E.append({"content":tx,"startFrame":f(a),"endFrame":f(b),"animation":"punchIn" if up else "fadeIn","style":st,"transform":{"x":0.5,"y":y}})
if E: call("add_texts",{"projectId":P,"timelineId":TL,"entries":E})
# effects and zoom
real=[v for v,(p,a,b,n) in zip(vid,shots) if not n.startswith("hf_") and not n.startswith("flip2_")]
call("apply_effect",{"projectId":P,"timelineId":TL,"clipIds":vid,"effects":[{"type":"stylize.grain","params":{"amount":0.18,"size":1.6}},{"type":"stylize.vignette","params":{"amount":0.3}},{"type":"blur.sharpen","params":{"amount":0.5}}]})
call("apply_color",{"projectId":P,"timelineId":TL,"clipIds":real,"contrast":1.10,"saturation":1.12})
for i,(v,(p,a,b,n)) in enumerate(zip(vid,shots)):
    if n.startswith("hf_") or n.startswith("flip2_") or n.startswith("iv_"): continue
    d=f(b)-f(a); z0,z1=(1.0,1.15) if i%2==0 else (1.15,1.0); pp=lambda z:(1-z)/2
    call("set_keyframes",{"projectId":P,"timelineId":TL,"clipId":v,"property":"scale","keyframes":[[0,z0,z0],[d,z1,z1]]})
    call("set_keyframes",{"projectId":P,"timelineId":TL,"clipId":v,"property":"position","keyframes":[[0,pp(z0),pp(z0)],[d,pp(z1),pp(z1)]]})
# flash at block bounds
white=call("import_media",{"projectId":P,"timelineId":TL,"source":{"matte":{"hex":"#FFFFFF"}}})["mediaRef"]
r=call("add_clips",{"projectId":P,"timelineId":TL,"entries":[{"mediaRef":white,"startFrame":f(x),"endFrame":f(x)+4} for x in bounds[1:]]})
for k in r["clips"]: call("set_keyframes",{"projectId":P,"timelineId":TL,"clipId":k["id"],"property":"opacity","keyframes":[[0,0.55],[4,0]]})
json.dump({"P":P,"TL":TL,"total":total},open(f"v3_{which}_ids.json","w")); print("built",P,TL)
