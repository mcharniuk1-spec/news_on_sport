"""Fetch ~4-5 short 9:16 footage clips for script NNN with yt-dlp + ffmpeg (no audio). Usage: fetch_footage.py NNN"""
import json, sys, os, subprocess, re
H="<PROJECT_ROOT>/research/football100"; YT=os.path.expanduser("~/.agent-reach-venv/bin/yt-dlp")
no=int(sys.argv[1]); j=json.load(open(f"{H}/scripts/{no:03d}.json")); out=f"{H}/footage/{no:03d}"; os.makedirs(out,exist_ok=True)
BAD=re.compile(r"studio|pundit|soccer saturday|goals on sunday|transfer talk|sky sports news|live:|show|stream|analysis|debrief|talk|rant|review|predict|news today|breakdown|explained|tactical|watchalong|watch along|reaction|tier list|efootball|fifa \d|fc ?2\d|gameplay|pes |podcast|live stream|livestream|full match|compilation 20|shorts",re.I)
GOOD=re.compile(r"sky sports|tnt sports|bbc|espn|laliga|premier league|uefa|bundesliga|dazn|cbs sports|fifa|bein|talksport|official|serie a|ligue 1|efl|championship|fc bayern|barcelona|real madrid|liverpool|arsenal|chelsea|manchester|tottenham|newcastle|juventus|milan|inter|psg|ajax|olympique|sportstv|optus|stan sport|nbc sports|fox soccer|movistar|canal|rtve|dazn|ziggo|viaplay|premier sports|tv 2|nrk|bt sport|amazon prime",re.I)
HIGH=re.compile(r"highlights|goals?\b|\bvs?\b|match|press conference|interview|celebrat|training|full-time|extended",re.I)
terms=list(j.get("footage_terms") or [])[:4]+[j["subject"][:50]+" highlights",j["subject"][:50]+" interview"]
have=len([f for f in os.listdir(out) if f.endswith(".mp4")]); used=set(); k=have
def run(a,t=240):
    try: return subprocess.run(a,capture_output=True,text=True,timeout=t).stdout
    except Exception: return ""
for term in terms:
    if k>=5: break
    rows=[]
    for l in run([YT,"--no-update","--flat-playlist","--print","%(id)s\t%(duration)s\t%(view_count)s\t%(channel)s\t%(title)s",f"ytsearch8:{term}"]).splitlines():
        p=l.split("\t")
        if len(p)<5 or p[1] in("NA",""): continue
        try: d=float(p[1]); v=int(float(p[2])) if p[2]!="NA" else 0
        except: continue
        if 25<=d<=1500 and not BAD.search(p[4]) and p[0] not in used: rows.append((v+(10**9 if GOOD.search(p[3]) else 0)+(5*10**8 if HIGH.search(p[4]) else 0),p[0],d))
    for v,vid,d in sorted(rows,reverse=True)[:2]:
        if k>=5: break
        s=max(5,int(d*0.3)); tmp=f"{out}/tmp_{vid}.mp4"
        run([YT,"--no-update","-f","bv*[height<=720][ext=mp4]/bv*[height<=720]/b[height<=720]","--download-sections",f"*{s}-{s+15}","--force-keyframes-at-cuts","-o",tmp,f"https://www.youtube.com/watch?v={vid}"],300)
        if not os.path.exists(tmp):
            c=[x for x in os.listdir(out) if x.startswith(f"tmp_{vid}")]
            if c: tmp=f"{out}/{c[0]}"
            else: continue
        dst=f"{out}/c{k}.mp4"
        r=subprocess.run(["ffmpeg","-v","error","-y","-i",tmp,"-an","-t","14","-vf","split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=28:6[bg];[b]scale=1296:-2,crop=1080:ih[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2,fps=30,format=yuv420p","-c:v","libx264","-crf","21","-preset","fast",dst],capture_output=True)
        os.remove(tmp); used.add(vid)
        if r.returncode==0: k+=1
print(no,"clips",k)
