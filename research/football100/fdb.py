#!/usr/bin/env python3
"""Compact knowledge DB for the football-100 project (SQLite, zstd blobs, contentless FTS5).

Why SQLite and not MySQL: one file, no server, smaller on disk, FTS5 search built in.
Long text (facts, transcripts, scripts, frame notes) is stored zstd-compressed; the search index is contentless
(it keeps only the index, not a second copy of the text).
Read with `q`/`get`: they print short rows, so an agent never loads whole JSON files into context.

  fdb.py init
  fdb.py ingest-news [news/news_dedup.json | news/lane_*.json]
  fdb.py ingest-bo           # bo/*.json
  fdb.py ingest-corpus       # corpus/corpus_all.json + subs/*.vtt
  fdb.py ingest-old          # ../football_shorts.db frame notes -> compressed per video
  fdb.py q "<fts terms>" [--t news|vids|scripts] [-n 8]
  fdb.py get news|bo|vid|script <id|name>
  fdb.py put-script <no> <json-file>
  fdb.py stats | pack            # pack = VACUUM + .zst archive
"""
import glob, json, os, re, sqlite3, struct, sys, zstandard

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(HERE, "db", "f100.sqlite")
os.makedirs(os.path.dirname(DB), exist_ok=True)
_cz, _dz = zstandard.ZstdCompressor(level=19), zstandard.ZstdDecompressor()

def z(obj):
    b = obj if isinstance(obj, bytes) else (obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, separators=(",", ":"))).encode()
    return _cz.compress(b)

def uz(b, js=True):
    if b is None: return None
    s = _dz.decompress(b).decode()
    return json.loads(s) if js else s

def conn():
    c = sqlite3.connect(DB)
    c.execute("pragma journal_mode=wal"); c.execute("pragma synchronous=normal")
    return c

SCHEMA = """
create table if not exists news(id integer primary key, headline text, date text, domain text, url text,
  angle text, sensitive int, conf text, entities text, n_src int, facts blob, background blob, terms text, used int default 0, unique(headline,date));
create virtual table if not exists news_fts using fts5(headline, entities, facts, content='', contentless_delete=1);
create table if not exists bo(name text primary key, years text, verified int, pack blob);
create table if not exists vids(id text primary key, kind text, channel text, title text, dur real, views int, likes int, comments int,
  date text, peak_t real, peak_v real, wps real, q_hook int, num_hook int, opening text, heat blob, has_cc int);
create virtual table if not exists vids_fts using fts5(title, opening, content='', contentless_delete=1);
create table if not exists tr(vid text primary key, text blob);
create table if not exists frames(vid text primary key, notes blob);
create table if not exists scripts(no integer primary key, subject text, title text, words int, chars int, status text, voice text, body blob);
create virtual table if not exists scripts_fts using fts5(subject, title, body, content='', contentless_delete=1);
create table if not exists kv(k text primary key, v blob);
"""

def init():
    c = conn(); c.executescript(SCHEMA); c.commit(); print("ok", DB)

def ingest_news(paths):
    c = conn(); c.executescript(SCHEMA)
    files = paths or [os.path.join(HERE, "news", "news_dedup.json")]
    files = [f for p in files for f in glob.glob(p)]
    n = 0
    for f in files:
        for it in json.load(open(f)):
            srcs = it.get("sources") or ([it["url"]] if it.get("url") else [])
            if not srcs: continue
            url = " ".join(srcs[:4])
            ents = "|".join(it.get("entities") or [])
            facts = it.get("facts") or []
            cur = c.execute("insert or ignore into news(headline,date,domain,url,angle,sensitive,conf,entities,n_src,facts,background,terms) values(?,?,?,?,?,?,?,?,?,?,?,?)",
                (it.get("headline"), it.get("date"), it.get("source_domain"), url, it.get("angle"), int(bool(it.get("sensitive"))),
                 it.get("confidence"), ents, it.get("n_sources", 1), z(facts), z(it.get("background") or ""), "|".join(it.get("footage_terms") or [])))
            if cur.rowcount:
                c.execute("insert into news_fts(rowid,headline,entities,facts) values(?,?,?,?)", (cur.lastrowid, it.get("headline"), ents, " ".join(facts)))
                n += 1
    c.commit(); print("news added", n)

def ingest_bo():
    c = conn(); c.executescript(SCHEMA); n = 0
    for f in glob.glob(os.path.join(HERE, "bo", "*.json")):
        j = json.load(open(f))
        c.execute("insert or replace into bo values(?,?,?,?)", (j.get("name"), str(j.get("years")), int("verification" in j), z(j))); n += 1
    c.commit(); print("bo packs", n)

def heat_pack(h):
    return bytes(min(255, int(v * 255)) for v in h) if h else None

def ingest_corpus():
    c = conn(); c.executescript(SCHEMA); n = 0
    rows = json.load(open(os.path.join(HERE, "corpus", "corpus_all.json")))
    c.execute("delete from vids"); c.execute("delete from tr"); c.execute("insert into vids_fts(vids_fts) values('delete-all')")
    for r in rows:
        pk = r.get("heatmap_peak") or {}
        c.execute("insert or replace into vids values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (r["id"], r["kind"], r.get("channel"), r.get("title"), r.get("duration"), r.get("views"), r.get("likes"), r.get("comments"),
             r.get("upload_date"), pk.get("start_time"), pk.get("value"), r.get("wps"), int(bool(r.get("q_in_first_25w"))),
             int(bool(r.get("digit_in_first_25w"))), r.get("opening"), heat_pack(r.get("heatmap")), int(bool(r.get("has_auto_en")))))
        p = os.path.join(HERE, "corpus", "subs", r["id"] + ".en.vtt")
        if os.path.exists(p):
            sys.path.insert(0, HERE); from corpus_harvest import vtt_text
            t = vtt_text(p); c.execute("insert or replace into tr values(?,?)", (r["id"], z(t)))
        c.execute("insert into vids_fts(rowid,title,opening) select rowid,title,coalesce(opening,'') from vids where id=?", (r["id"],))
        n += 1
    c.commit(); print("videos", n)

def ingest_old():
    old = sqlite3.connect(os.path.join(HERE, "..", "football_shorts.db")); c = conn(); c.executescript(SCHEMA)
    cur = old.execute("select video_id,idx,t_sec,type,description,text_on_screen,transition_to_next from frames order by video_id,idx")
    by = {}
    for v, i, t, ty, d, tx, tr_ in cur: by.setdefault(v, []).append([round(t or 0, 1), ty, d, tx, tr_])
    for v, rows in by.items(): c.execute("insert or replace into frames values(?,?)", (v, z(rows)))
    c.commit(); print("frame-note videos", len(by))

def fts_q(s): return " ".join('"%s"' % w.replace('"', "") for w in s.split() if w)

def q(term, table="news", n=8):
    c = conn()
    if table == "news":
        sql = "select n.id,n.date,n.angle,n.domain,substr(n.headline,1,90),n.url from news_fts f join news n on n.id=f.rowid where news_fts match ? order by rank limit ?"
    elif table == "vids":
        sql = "select v.id,v.kind,v.views,round(v.dur),substr(v.title,1,70),substr(v.opening,1,60) from vids_fts f join vids v on v.rowid=f.rowid where vids_fts match ? order by rank limit ?"
    else:
        sql = "select s.no,s.subject,s.words,s.status,substr(s.title,1,70) from scripts_fts f join scripts s on s.no=f.rowid where scripts_fts match ? order by rank limit ?"
    for r in c.execute(sql, (fts_q(term), n)): print("\t".join(str(x) for x in r))

def get(kind, key):
    c = conn()
    if kind == "news":
        r = c.execute("select headline,date,domain,url,angle,sensitive,entities,facts,background,terms from news where id=?", (key,)).fetchone()
        print(json.dumps(dict(zip("headline date domain url angle sensitive entities facts background terms".split(), r[:7] + (uz(r[7]), uz(r[8], False), r[9]))), ensure_ascii=False))
    elif kind == "bo":
        r = c.execute("select pack from bo where name like ?", (f"%{key}%",)).fetchone(); print(uz(r[0], False))
    elif kind == "vid":
        r = c.execute("select text from tr where vid=?", (key,)).fetchone(); print(uz(r[0], False) if r else "no transcript")
    elif kind == "script":
        r = c.execute("select body from scripts where no=?", (key,)).fetchone(); print(uz(r[0], False))

def put_script(no, path):
    c = conn(); c.executescript(SCHEMA); j = json.load(open(path))
    text = " ".join(l if isinstance(l, str) else l.get("vo", "") for l in j.get("lines", []))
    c.execute("insert or replace into scripts values(?,?,?,?,?,?,?,?)",
        (int(no), j.get("subject"), j.get("title"), len(text.split()), len(text), j.get("status", "draft"), j.get("voice", "kokoro"), z(j)))
    c.execute("delete from scripts_fts where rowid=?", (int(no),))
    c.execute("insert into scripts_fts(rowid,subject,title,body) values(?,?,?,?)", (int(no), j.get("subject"), j.get("title"), text))
    c.commit(); print("script", no, len(text.split()), "words", len(text), "chars")

def stats():
    c = conn()
    for t in ("news", "bo", "vids", "tr", "frames", "scripts"):
        print(t, c.execute(f"select count(*) from {t}").fetchone()[0])
    print("db MB", round(os.path.getsize(DB) / 1e6, 2))

def pack():
    c = conn(); c.execute("pragma wal_checkpoint(truncate)"); c.execute("vacuum"); c.close()
    raw = open(DB, "rb").read(); out = DB + ".zst"; open(out, "wb").write(zstandard.ZstdCompressor(level=19).compress(raw))
    print("db", round(len(raw) / 1e6, 2), "MB; archive", round(os.path.getsize(out) / 1e6, 2), "MB")

if __name__ == "__main__":
    a = sys.argv[1:]
    if not a: print(__doc__); sys.exit()
    cmd = a[0]
    if cmd == "init": init()
    elif cmd == "ingest-news": ingest_news(a[1:])
    elif cmd == "ingest-bo": ingest_bo()
    elif cmd == "ingest-corpus": ingest_corpus()
    elif cmd == "ingest-old": ingest_old()
    elif cmd == "q":
        t = "news"; n = 8; terms = []
        i = 1
        while i < len(a):
            if a[i] == "--t": t = a[i + 1]; i += 2
            elif a[i] == "-n": n = int(a[i + 1]); i += 2
            else: terms.append(a[i]); i += 1
        q(" ".join(terms), t, n)
    elif cmd == "get": get(a[1], a[2])
    elif cmd == "put-script": put_script(a[1], a[2])
    elif cmd == "stats": stats()
    elif cmd == "pack": pack()
