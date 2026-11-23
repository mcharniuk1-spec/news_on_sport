#!/usr/bin/env python3
"""Stage 6: YouTube captions (manual or auto) -> cleaned text of first 60 s with timestamps."""
import json, subprocess, os, re, glob
from concurrent.futures import ThreadPoolExecutor
R = os.path.dirname(os.path.abspath(__file__))
V = json.load(open(f"{R}/videos.json"))
def ts(s):
    h, m, x = s.split(":"); return int(h)*3600 + int(m)*60 + float(x)
def fetch(v):
    vid = v["id"]
    if not glob.glob(f"{R}/subs/{vid}.*.vtt"):
        subprocess.run(["yt-dlp","--no-update","-q","--skip-download","--write-sub","--write-auto-sub","--sub-langs","en.*,en,uk,ru,es,pt,.*-orig",
            "--sub-format","vtt","-o",f"{R}/subs/%(id)s","--no-playlist",v["url"]], capture_output=True, text=True, timeout=120)
    fs = sorted(glob.glob(f"{R}/subs/{vid}.*.vtt"))
    if not fs: return vid, None
    lang = fs[0].split(".")[-2]; seen = set(); out = []
    for blk in open(fs[0], encoding="utf8").read().split("\n\n"):
        m = re.search(r"(\d+:\d+:\d+\.\d+) --> ", blk)
        if not m: continue
        t = ts(m.group(1))
        if t > 60: break
        txt = " ".join(re.sub(r"<[^>]+>", "", l).strip() for l in blk.splitlines()[1:] if "-->" not in l).strip()
        if txt and txt not in seen: seen.add(txt); out.append(f"[{t:.0f}s] {txt}")
    return vid, {"lang": lang, "text": "\n".join(out)}
with ThreadPoolExecutor(5) as ex: res = dict(ex.map(fetch, V))
json.dump(res, open(f"{R}/transcripts.json","w"), ensure_ascii=False, indent=1)
print(sum(1 for x in res.values() if x), "of", len(res), "with captions")
