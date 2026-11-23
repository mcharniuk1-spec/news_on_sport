#!/usr/bin/env python3
"""Football-clip channel scan via yt-dlp (no API key). Read-only metadata.
Usage: yt_scan.py discover  -> candidates.json
       yt_scan.py stats     -> channel_stats.json / .csv
"""
import json, subprocess, sys, statistics, csv, os
from concurrent.futures import ThreadPoolExecutor

OUT = os.path.dirname(os.path.abspath(__file__))
QUERIES = [
    "football vibes", "football edits shorts", "football clips compilation",
    "football skills moments shorts", "funny football moments", "football fails goals skills",
    "soccer clips shorts", "football edit capcut", "football best moments compilation",
    "messi ronaldo clips", "football reels edits", "football tiktok compilation",
    "lamine yamal clips", "football fan moments", "football aura edits",
]
PER_Q = 40
N_VIDEOS = 30  # per tab (within the 20-50 range)

def ytdlp(args, timeout=180):
    p = subprocess.run(["yt-dlp", "--no-update", "--ignore-errors", *args],
                       capture_output=True, text=True, timeout=timeout)
    return p.stdout

def discover():
    cands = {}
    def one(q):
        out = ytdlp(["--flat-playlist", "--print", "%(channel_id)s\t%(channel)s", f"ytsearch{PER_Q}:{q}"])
        return out.splitlines()
    with ThreadPoolExecutor(5) as ex:
        for lines in ex.map(one, QUERIES):
            for l in lines:
                if "\t" not in l: continue
                cid, name = l.split("\t", 1)
                if cid and cid != "NA":
                    cands.setdefault(cid, {"name": name, "hits": 0})["hits"] += 1
    json.dump(cands, open(f"{OUT}/candidates.json", "w"), indent=1, ensure_ascii=False)
    print(len(cands), "candidates")

def tab(cid, kind):
    out = ytdlp(["--flat-playlist", "--playlist-end", str(N_VIDEOS),
                 "--print", "%(id)s\t%(view_count)s\t%(duration)s\t%(title)s",
                 f"https://www.youtube.com/channel/{cid}/{kind}"], timeout=240)
    rows = []
    for l in out.splitlines():
        p = l.split("\t")
        if len(p) >= 4 and p[1] not in ("NA", ""):
            rows.append({"id": p[0], "views": int(p[1]), "title": p[3]})
    return rows

def stat(rows):
    v = [r["views"] for r in rows]
    return {"n": len(v), "avg": int(statistics.mean(v)) if v else 0,
            "median": int(statistics.median(v)) if v else 0}

def stats():
    cands = json.load(open(f"{OUT}/candidates.json"))
    def one(item):
        cid, meta = item
        sh, lo = tab(cid, "shorts"), tab(cid, "videos")
        return {"channel_id": cid, "name": meta["name"], "url": f"https://www.youtube.com/channel/{cid}",
                "shorts": stat(sh), "long": stat(lo),
                "top_shorts": sorted(sh, key=lambda r: -r["views"])[:3]}
    with ThreadPoolExecutor(6) as ex:
        top = sorted(cands.items(), key=lambda kv: -kv[1]["hits"])[:60]
        res = list(ex.map(one, top))
    json.dump(res, open(f"{OUT}/channel_stats.json", "w"), indent=1, ensure_ascii=False)
    with open(f"{OUT}/channel_stats.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "url", "shorts_n", "shorts_avg", "shorts_median", "long_n", "long_avg", "long_median"])
        for r in sorted(res, key=lambda r: -max(r["shorts"]["avg"], r["long"]["avg"])):
            w.writerow([r["name"], r["url"], r["shorts"]["n"], r["shorts"]["avg"], r["shorts"]["median"],
                        r["long"]["n"], r["long"]["avg"], r["long"]["median"]])

if __name__ == "__main__":
    {"discover": discover, "stats": stats}[sys.argv[1]]()
