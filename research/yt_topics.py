#!/usr/bin/env python3
"""Stage 2: find Shorts by topic, rank channels by FutVibes-likeness. Read-only."""
import json, subprocess, os, collections
from concurrent.futures import ThreadPoolExecutor
OUT = os.path.dirname(os.path.abspath(__file__))
TOPIC_QUERIES = [
 "Lamine Yamal shorts", "Mbappe shorts news", "Haaland Real Madrid transfer shorts", "Neymar celebration shorts",
 "Endrick Real Madrid shorts", "Nico Paz Real Madrid return", "Man United January transfer shorts",
 "Pochettino Manchester United shorts", "Sesko Zirkzee shorts", "Lisandro Martinez red card shorts",
 "Liverpool sale Qatar shorts", "Ronaldo shorts news", "Messi shorts news", "Vinicius Junior shorts",
 "Bellingham shorts", "Dembele Ballon d'Or shorts", "football transfer news shorts", "football drama shorts",
 "football scandal shorts", "football beef conflict players shorts", "Arsenal Man City shorts",
 "Barcelona Real Madrid shorts news", "football news today shorts", "football fan reaction shorts",
 "Mbappe PSG lawsuit shorts", "January transfer window shorts", "Salah Liverpool shorts", "Cole Palmer shorts",
]
def run(q):
    p = subprocess.run(["yt-dlp","--no-update","--ignore-errors","--flat-playlist","--print",
      "%(id)s\t%(channel_id)s\t%(channel)s\t%(view_count)s\t%(duration)s\t%(title)s", f"ytsearch50:{q}"],
      capture_output=True, text=True, timeout=240)
    return q, p.stdout.splitlines()
rows = {}
with ThreadPoolExecutor(6) as ex:
    for q, lines in ex.map(run, TOPIC_QUERIES):
        for l in lines:
            p = l.split("\t")
            if len(p) < 6 or p[3] in ("NA","") or p[4] in ("NA",""): continue
            d = float(p[4])
            if d <= 61:
                rows[p[0]] = dict(id=p[0], cid=p[1], channel=p[2], views=int(p[3]), dur=d, title=p[5], q=q)
json.dump(list(rows.values()), open(f"{OUT}/topic_shorts.json","w"), indent=1, ensure_ascii=False)
by = collections.defaultdict(list)
for r in rows.values(): by[r["cid"]].append(r)
rank = sorted(by.items(), key=lambda kv: (-len({x["q"] for x in kv[1]}), -sum(x["views"] for x in kv[1])))
print(len(rows), "shorts,", len(by), "channels")
for cid, v in rank[:40]:
    print(cid, v[0]["channel"], "| topics", len({x["q"] for x in v}), "| hits", len(v), "| avg", int(sum(x["views"] for x in v)/len(v)))
