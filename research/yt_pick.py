#!/usr/bin/env python3
"""Stage 3: profile candidate channels' Shorts tabs (subs, avg views, sample titles)."""
import json, subprocess, os, statistics
from concurrent.futures import ThreadPoolExecutor
OUT = os.path.dirname(os.path.abspath(__file__))
cand = {}
for r in json.load(open(f"{OUT}/topic_shorts.json")):
    if r["cid"] != "NA": cand[r["cid"]] = r["channel"]
for cid, m in json.load(open(f"{OUT}/candidates.json")).items(): cand[cid] = m["name"]
cand["UCgfxjUYBKLUUjq0oE7DU-Iw"] = "FutVibes"
def prof(item):
    cid, name = item
    p = subprocess.run(["yt-dlp","--no-update","--ignore-errors","-J","--flat-playlist","--playlist-end","30",
        f"https://www.youtube.com/channel/{cid}/shorts"], capture_output=True, text=True, timeout=240)
    try: d = json.loads(p.stdout)
    except Exception: return None
    if not isinstance(d, dict): return None
    es = [e for e in d.get("entries") or [] if e and e.get("view_count") is not None]
    if len(es) < 10: return None
    v = [e["view_count"] for e in es]
    return dict(cid=cid, name=name, subs=d.get("channel_follower_count"), n=len(v), avg=int(statistics.mean(v)),
                med=int(statistics.median(v)), titles=[e["title"] for e in es[:8]], ids=[e["id"] for e in es])
with ThreadPoolExecutor(8) as ex:
    res = [r for r in ex.map(prof, cand.items()) if r]
json.dump(res, open(f"{OUT}/shorts_profiles.json","w"), indent=1, ensure_ascii=False)
for r in sorted(res, key=lambda r: -r["med"])[:45]:
    print(f"{r['name']} | subs {r['subs']} | med {r['med']} avg {r['avg']} | {r['cid']}")
    for t in r["titles"][:3]: print("    -", t[:90])
