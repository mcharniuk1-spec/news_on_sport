#!/usr/bin/env python3
"""Stage 4: select 110 Shorts + 110 long videos and fetch full public metadata (no media download)."""
import json, subprocess, os, re
from concurrent.futures import ThreadPoolExecutor
OUT = os.path.dirname(os.path.abspath(__file__))
P = {p["name"]: p for p in json.load(open(f"{OUT}/shorts_profiles.json"))}
P.setdefault("Schtein", {"cid": "UCDBPUSh5CCa8k2hTx7UlbXg"})
TR = json.load(open(f"{OUT}/trending_raw.json"))
SHORT_CH = ["FutVibes","Schtein","Messi & Ronaldo Plays","ADNANE JR","miko","Gau3am","Magical Football","Teo CRi","DX10HD3","Nost FC"]
LONG_CH = {"Messi & Ronaldo Plays":None,"Teo CRi":None,"Nost FC":None,"CTfootball":None,"DX10HD3":None,"Magical Football":None,
           "Sky Sports Premier League":None,"TNT Sports Football":None,"Sky Sports News":"UCcw05gGzjLIs5dnxGkQHMvw","Futcrunch":None}
def cid_of(n): return LONG_CH.get(n) or P[n]["cid"]
def flat(url, n=30):
    p = subprocess.run(["yt-dlp","--no-update","--ignore-errors","--flat-playlist","--playlist-end",str(n),"--print",
        "%(id)s\t%(view_count)s\t%(duration)s\t%(title)s", url], capture_output=True, text=True, timeout=240)
    rows=[]
    for l in p.stdout.splitlines():
        x=l.split("\t")
        if len(x)>=4 and x[1] not in("NA",""): rows.append(dict(id=x[0],views=int(x[1]),dur=float(x[2]) if x[2] not in("NA","") else 30.0,title=x[3]))
    return rows
def meta(vid):
    p = subprocess.run(["yt-dlp","--no-update","--ignore-errors","-J","--skip-download","--no-playlist",
        f"https://www.youtube.com/watch?v={vid}"], capture_output=True, text=True, timeout=240)
    try: d=json.loads(p.stdout)
    except Exception: return None
    return dict(id=vid, title=d.get("title"), channel=d.get("channel"), channel_id=d.get("channel_id"),
        subs=d.get("channel_follower_count"), views=d.get("view_count"), likes=d.get("like_count"),
        comments=d.get("comment_count"), duration=d.get("duration"), upload_date=d.get("upload_date"),
        description=(d.get("description") or "")[:600], tags=(d.get("tags") or [])[:15],
        has_subs=bool(d.get("subtitles")), has_auto=bool(d.get("automatic_captions")),
        width=d.get("width"), height=d.get("height"), url=f"https://www.youtube.com/watch?v={vid}")
sel = []  # (video_id, kind, source, rank)
def pick(kind, ch, url, minD, maxD):
    rows=[r for r in flat(url) if minD<=r["dur"]<=maxD]
    rows.sort(key=lambda r:-r["views"])
    return [(r["id"],kind,ch,"channel_top10_of_last30") for r in rows[:10]]
with ThreadPoolExecutor(8) as ex:
    fs=[ex.submit(pick,"short",n,f"https://www.youtube.com/channel/{P[n]['cid']}/"+("videos" if n=="Schtein" else "shorts"),1,61) for n in SHORT_CH]
    fs+=[ex.submit(pick,"long",n,f"https://www.youtube.com/channel/{cid_of(n)}/videos",90,1800) for n in LONG_CH]
    for f in fs: sel+=f.result()
chosen={s[0] for s in sel}
bad=re.compile(r"highlights|live|replay|full match|episode|watchalong|\bep\b|natok|reaccionando|REACTING TO", re.I)
def trend(kind, minD, maxD, own):
    c=[r for r in TR[kind].values() if minD<=r["dur"]<=maxD and r["id"] not in chosen and r["ch"] not in own and not bad.search(r["title"])]
    c.sort(key=lambda r:-r["views"]); return c[:30]
tcs=trend("short",1,61,SHORT_CH); tcl=trend("long",100,1500,set(LONG_CH))
ids=[s[0] for s in sel]+[r["id"] for r in tcs]+[r["id"] for r in tcl]
with ThreadPoolExecutor(8) as ex: M={m["id"]:m for m in ex.map(meta,ids) if m}
def recent(m): return m and (m["upload_date"] or "0")>="20261020"
final=[]
for vid,kind,ch,why in sel:
    if vid in M: final.append(dict(M[vid],kind=kind,source=ch,why=why))
for kind,cs in (("short",tcs),("long",tcl)):
    n=0
    for r in cs:
        m=M.get(r["id"])
        if recent(m) and n<10: final.append(dict(m,kind=kind,source="TRENDING_THIS_MONTH",why="trending_search_top_views")); n+=1
json.dump(final,open(f"{OUT}/videos.json","w"),ensure_ascii=False,indent=1)
import collections
print(collections.Counter((v["kind"],v["source"]=="TRENDING_THIS_MONTH") for v in final))
print(collections.Counter(v["source"] for v in final))
