#!/usr/bin/env python3
"""Corpus harvest with yt-dlp (metadata only, no media download).

Targets
  SHORTS: 100 creators x 10 shorts (>=10, <=10 per creator)  -> corpus/shorts_meta.jsonl
  LONG  : 1000 videos, 60 < duration <= 150 s, <=10 per creator -> corpus/long_meta.jsonl
Every step is resumable (jsonl append + skip ids already done).

Usage:  python3 corpus_harvest.py discover | pick | enrich | captions | stats
"""
import json, os, re, subprocess, sys, time, random, collections, statistics
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, "corpus")
os.makedirs(C, exist_ok=True)
YT = os.path.expanduser("~/.agent-reach-venv/bin/yt-dlp")
PRIOR = os.path.join(HERE, "..", "candidates.json")   # channels from the earlier scan

SHORTS_Q = [
 "football shorts", "football edits", "football clips", "football skills shorts", "funny football moments",
 "football news shorts", "transfer news shorts", "football story shorts", "football facts shorts",
 "premier league shorts", "champions league shorts", "la liga shorts", "serie a shorts", "bundesliga shorts",
 "messi shorts", "ronaldo shorts", "mbappe shorts", "haaland shorts", "yamal shorts", "bellingham shorts",
 "football legends shorts", "football aura edit", "football scandal shorts", "football manager sacked shorts",
 "ballon d'or shorts", "world cup shorts", "football memes shorts", "football stats explained shorts",
 "football tactics shorts", "football rivalry shorts", "football documentary shorts", "football reaction shorts",
 "football interview shorts", "football press conference shorts", "football referee controversy shorts",
 "football fan reaction shorts", "football comeback shorts", "football history shorts", "football trivia shorts",
 "soccer shorts", "soccer storytime", "football commentary shorts", "football goals compilation shorts",
 "football pundit shorts", "arsenal shorts", "liverpool shorts", "manchester united shorts", "chelsea shorts",
 "manchester city shorts", "tottenham shorts", "barcelona shorts", "real madrid shorts", "psg shorts",
 "bayern shorts", "juventus shorts", "milan shorts", "inter shorts", "ukraine football shorts",
 "lionel messi story", "cristiano ronaldo story", "neymar story shorts", "zidane shorts", "ronaldinho shorts",
 "football quiz shorts", "football edit capcut", "football transfer rumour shorts", "football highlights shorts",
]
LONG_Q = [
 "football compilation", "football funny moments", "football skills compilation", "football story explained",
 "football news today", "transfer news explained", "football documentary short", "messi best moments",
 "ronaldo best moments", "ronaldinho skills", "ballon d'or winners story", "football scandal explained",
 "premier league moments", "champions league moments", "world cup moments", "football manager sacked",
 "football rivalry explained", "football legends tribute", "football interview moments", "football press conference funny",
 "football reaction compilation", "football fails compilation", "football goals of the week", "football edit montage",
 "football rumours explained", "football history short", "football stats explained", "football tactics explained short",
 "football storytime", "football memes", "football transfer saga", "football comeback story", "football aura",
 "football commentators moments", "football referee controversy", "football fan moments", "mbappe story", "haaland story",
 "yamal story", "bellingham story", "zidane story", "cristiano ronaldo news", "lionel messi news", "arsenal news",
 "liverpool news", "manchester united news", "chelsea news", "real madrid news", "barcelona news", "psg news",
 "bayern news", "ukraine football", "mudryk", "football 60 seconds", "football in 2 minutes", "football recap",
]

def run(args, timeout=240):
    try:
        p = subprocess.run([YT, "--no-update", "--ignore-errors", "--no-warnings", *args],
                           capture_output=True, text=True, timeout=timeout)
        return p.stdout
    except subprocess.TimeoutExpired:
        return ""

def jl_read(path):
    if not os.path.exists(path): return []
    return [json.loads(l) for l in open(path) if l.strip()]

def jl_append(path, row):
    with open(path, "a") as f: f.write(json.dumps(row, ensure_ascii=False) + "\n")

# ---------------------------------------------------------------- discover
def search_flat(q, n):
    out = run(["--flat-playlist", "--print",
               "%(id)s\t%(channel_id)s\t%(channel)s\t%(duration)s\t%(view_count)s\t%(title)s", f"ytsearch{n}:{q}"], 300)
    rows = []
    for l in out.splitlines():
        p = l.split("\t")
        if len(p) >= 6 and p[0] and p[1] not in ("NA", ""):
            rows.append(dict(id=p[0], channel_id=p[1], channel=p[2],
                             duration=None if p[3] == "NA" else float(p[3]),
                             views=None if p[4] == "NA" else int(float(p[4])), title=p[5]))
    return rows

def discover():
    # channels from many searches (shorts-flavoured), plus the earlier scan
    chans = collections.defaultdict(lambda: {"name": "", "hits": 0})
    if os.path.exists(PRIOR):
        for cid, m in json.load(open(PRIOR)).items():
            chans[cid]["name"] = m.get("name", ""); chans[cid]["hits"] += m.get("hits", 1)
    done = set(r["q"] for r in jl_read(f"{C}/search_log.jsonl"))
    def one(item):
        kind, q = item
        if (kind, q) in done: return None
        rows = search_flat(q, 80 if kind == "L" else 50)
        return kind, q, rows
    jobs = [("S", q) for q in SHORTS_Q] + [("L", q) for q in LONG_Q]
    done = set((r["kind"], r["q"]) for r in jl_read(f"{C}/search_log.jsonl"))
    with ThreadPoolExecutor(6) as ex:
        for res in ex.map(one, jobs):
            if not res: continue
            kind, q, rows = res
            jl_append(f"{C}/search_log.jsonl", {"kind": kind, "q": q, "n": len(rows)})
            for r in rows:
                if kind == "L":
                    jl_append(f"{C}/long_pool.jsonl", r)
                chans[r["channel_id"]]["name"] = r["channel"]; chans[r["channel_id"]]["hits"] += 1
            print(kind, q, len(rows), flush=True)
    json.dump(chans, open(f"{C}/channels_pool.json", "w"), indent=1, ensure_ascii=False)
    print(len(chans), "channels in pool")

# ---------------------------------------------------------------- pick
def shorts_tab(cid, n=30):
    out = run(["--flat-playlist", "--playlist-end", str(n), "--print",
               "%(id)s\t%(view_count)s\t%(duration)s\t%(title)s",
               f"https://www.youtube.com/channel/{cid}/shorts"], 240)
    rows = []
    for l in out.splitlines():
        p = l.split("\t")
        if len(p) >= 4 and p[1] not in ("NA", ""):
            rows.append(dict(id=p[0], views=int(float(p[1])), duration=None if p[2] == "NA" else float(p[2]), title=p[3]))
    return rows

def pick():
    chans = json.load(open(f"{C}/channels_pool.json"))
    order = sorted(chans.items(), key=lambda kv: -kv[1]["hits"])
    have = {r["channel_id"] for r in jl_read(f"{C}/shorts_pick.jsonl")}
    def one(item):
        cid, m = item
        if cid in have: return None
        rows = shorts_tab(cid, 30)
        return cid, m["name"], rows
    picked = len(have)
    with ThreadPoolExecutor(5) as ex:
        for res in ex.map(one, order[:260]):
            if not res: continue
            cid, name, rows = res
            if len(rows) < 10: continue
            top = sorted(rows, key=lambda r: -r["views"])[:10]
            jl_append(f"{C}/shorts_pick.jsonl", {"channel_id": cid, "channel": name, "videos": top,
                                                 "median_views": statistics.median(r["views"] for r in rows)})
            picked += 1
            print("picked", picked, name, flush=True)
    # long: <=10 per creator, 60<d<=150, football-looking pool already filtered by queries
    pool = {}
    for r in jl_read(f"{C}/long_pool.jsonl"):
        if r["duration"] and 60 < r["duration"] <= 150 and r["views"] is not None:
            pool[r["id"]] = r
    per = collections.defaultdict(list)
    for r in pool.values(): per[r["channel_id"]].append(r)
    longs = []
    for cid, v in per.items():
        longs += sorted(v, key=lambda r: -r["views"])[:10]
    longs = sorted(longs, key=lambda r: -r["views"])[:1000]
    json.dump(longs, open(f"{C}/long_pick.json", "w"), ensure_ascii=False)
    print("long pool", len(pool), "-> picked", len(longs), "channels", len({r['channel_id'] for r in longs}))

# ---------------------------------------------------------------- enrich
def enrich_one(vid, kind):
    out = run(["--skip-download", "--dump-single-json", f"https://www.youtube.com/watch?v={vid}"], 180)
    try:
        j = json.loads(out)
    except Exception:
        return None
    if not isinstance(j, dict): return None
    hm = j.get("heatmap") or []
    peak = max(hm, key=lambda h: h["value"]) if hm else None
    return {"id": vid, "kind": kind, "title": j.get("title"), "channel": j.get("channel"), "channel_id": j.get("channel_id"),
            "subs": j.get("channel_follower_count"), "duration": j.get("duration"), "views": j.get("view_count"),
            "likes": j.get("like_count"), "comments": j.get("comment_count"), "upload_date": j.get("upload_date"),
            "tags": (j.get("tags") or [])[:15], "description": (j.get("description") or "")[:600],
            "chapters": j.get("chapters"), "heatmap_peak": peak,
            "heatmap": [round(h["value"], 3) for h in hm] if hm else None,
            "has_auto_en": bool((j.get("automatic_captions") or {}).get("en") or (j.get("subtitles") or {}).get("en")),
            "width": j.get("width"), "height": j.get("height"), "fps": j.get("fps")}

def enrich():
    jobs = []
    for r in jl_read(f"{C}/shorts_pick.jsonl")[:100]:
        for v in r["videos"]: jobs.append((v["id"], "short"))
    for v in json.load(open(f"{C}/long_pick.json")): jobs.append((v["id"], "long"))
    for kind, path in (("short", f"{C}/shorts_meta.jsonl"), ("long", f"{C}/long_meta.jsonl")):
        done = {r["id"] for r in jl_read(path)}
        todo = [(i, k) for i, k in jobs if k == kind and i not in done]
        print(kind, "todo", len(todo), flush=True)
        def one(a):
            time.sleep(random.random() * 0.8)
            return enrich_one(*a)
        n = 0
        with ThreadPoolExecutor(6) as ex:
            for r in ex.map(one, todo):
                if r:
                    jl_append(path, r); n += 1
                    if n % 50 == 0: print(kind, n, "/", len(todo), flush=True)

# ---------------------------------------------------------------- captions
def captions():
    rows = jl_read(f"{C}/shorts_meta.jsonl") + jl_read(f"{C}/long_meta.jsonl")
    os.makedirs(f"{C}/subs", exist_ok=True)
    todo = [r for r in rows if r["has_auto_en"] and not os.path.exists(f"{C}/subs/{r['id']}.en.vtt")]
    print("captions todo", len(todo), flush=True)
    def one(r):
        time.sleep(random.random() * 0.6)
        run(["--skip-download", "--write-auto-subs", "--write-subs", "--sub-langs", "en.*,en", "--sub-format", "vtt",
             "-o", f"{C}/subs/%(id)s", f"https://www.youtube.com/watch?v={r['id']}"], 120)
        for f in os.listdir(f"{C}/subs"):
            if f.startswith(r["id"] + ".en") and f.endswith(".vtt") and f != f"{r['id']}.en.vtt":
                os.replace(f"{C}/subs/{f}", f"{C}/subs/{r['id']}.en.vtt"); break
    with ThreadPoolExecutor(6) as ex:
        list(ex.map(one, todo))

def vtt_text(path):
    out, last = [], ""
    for l in open(path, errors="ignore"):
        l = l.strip()
        if not l or "-->" in l or l.startswith(("WEBVTT", "Kind:", "Language:", "NOTE")): continue
        l = re.sub(r"<[^>]+>", "", l)
        if l and l != last: out.append(l); last = l
    return " ".join(out)

def stats():
    rows = jl_read(f"{C}/shorts_meta.jsonl") + jl_read(f"{C}/long_meta.jsonl")
    res = []
    for r in rows:
        p = f"{C}/subs/{r['id']}.en.vtt"
        if os.path.exists(p):
            t = vtt_text(p); w = len(t.split())
            r["transcript_words"] = w
            r["wps"] = round(w / r["duration"], 2) if r.get("duration") else None
            r["opening"] = " ".join(t.split()[:25])
            r["q_in_first_25w"] = "?" in " ".join(t.split()[:25])
            r["digit_in_first_25w"] = bool(re.search(r"\d", r["opening"]))
        res.append(r)
    json.dump(res, open(f"{C}/corpus_all.json", "w"), ensure_ascii=False)
    sh = [r for r in res if r["kind"] == "short"]; lo = [r for r in res if r["kind"] == "long"]
    print("shorts", len(sh), "creators", len({r["channel_id"] for r in sh}), "| long", len(lo), "creators", len({r["channel_id"] for r in lo}))
    print("with captions", sum(1 for r in res if r.get("transcript_words")), "with heatmap", sum(1 for r in res if r.get("heatmap")))


# ---------------------------------------------------------------- long videos from channel /videos tabs
def longchan():
    chans = json.load(open(f"{C}/channels_pool.json"))
    done = {r["channel_id"] for r in jl_read(f"{C}/longchan_log.jsonl")}
    order = [c for c, m in sorted(chans.items(), key=lambda kv: -kv[1]["hits"]) if c not in done]
    def one(cid):
        out = run(["--flat-playlist", "--playlist-end", "150", "--print",
                   "%(id)s\t%(duration)s\t%(view_count)s\t%(title)s", f"https://www.youtube.com/channel/{cid}/videos"], 300)
        n = 0
        for l in out.splitlines():
            p = l.split("\t")
            if len(p) < 4 or p[1] == "NA" or p[2] == "NA": continue
            d = float(p[1])
            if 60 < d <= 150:
                jl_append(f"{C}/long_pool.jsonl", dict(id=p[0], channel_id=cid, channel=chans[cid]["name"], duration=d, views=int(float(p[2])), title=p[3])); n += 1
        jl_append(f"{C}/longchan_log.jsonl", {"channel_id": cid, "n": n})
        return cid, n
    with ThreadPoolExecutor(4) as ex:
        for cid, n in ex.map(one, order):
            print("longchan", chans[cid]["name"], n, flush=True)

def picklong():
    pool = {}
    for r in jl_read(f"{C}/long_pool.jsonl"):
        if r.get("duration") and 60 < r["duration"] <= 150 and r.get("views") is not None: pool[r["id"]] = r
    per = collections.defaultdict(list)
    for r in pool.values(): per[r["channel_id"]].append(r)
    longs = []
    for cap in (10, 15, 25, 50):          # relax the per-creator cap only if needed to reach 1000
        longs = []
        for cid, v in per.items(): longs += sorted(v, key=lambda r: -r["views"])[:cap]
        if len(longs) >= 1000: break
    longs = sorted(longs, key=lambda r: -r["views"])[:1000]
    json.dump(longs, open(f"{C}/long_pick.json", "w"), ensure_ascii=False)
    cnt = collections.Counter(r["channel_id"] for r in longs)
    print("long pool", len(pool), "picked", len(longs), "creators", len(cnt), "max per creator", max(cnt.values()), "cap used", cap)

if __name__ == "__main__":
    {"discover": discover, "pick": pick, "enrich": enrich, "captions": captions, "stats": stats, "longchan": longchan, "picklong": picklong}[sys.argv[1]]()
