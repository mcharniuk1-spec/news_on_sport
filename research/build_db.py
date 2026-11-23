#!/usr/bin/env python3
"""Stage 7: build compact SQLite DB (MySQL-compatible types; mysql/mariadb not installed) from videos + analysis."""
import json, sqlite3, os, glob
R = os.path.dirname(os.path.abspath(__file__))
DB = f"{R}/football_shorts.db"
if os.path.exists(DB): os.remove(DB)
c = sqlite3.connect(DB)
c.executescript("""
CREATE TABLE channels(channel_id TEXT PRIMARY KEY, name TEXT, subs INTEGER);
CREATE TABLE videos(video_id TEXT PRIMARY KEY, kind TEXT, source TEXT, channel_id TEXT, title TEXT, url TEXT,
  upload_date TEXT, duration INTEGER, views INTEGER, likes INTEGER, comments INTEGER, like_rate REAL, comment_rate REAL,
  has_captions INTEGER, cuts_in_first60 INTEGER, frames INTEGER, description TEXT, transcript TEXT,
  topic TEXT, hero TEXT, hero_role TEXT, media_type TEXT, hook TEXT, subtitle_style TEXT, reaction_overlays TEXT,
  transition_summary TEXT, audio_note TEXT);
CREATE TABLE frames(video_id TEXT, idx INTEGER, t_sec INTEGER, type TEXT, description TEXT, text_on_screen TEXT,
  transition_to_next TEXT, img_path TEXT, PRIMARY KEY(video_id, idx));
CREATE TABLE reuse_segments(video_id TEXT, t0 REAL, t1 REAL, what TEXT, origin_guess TEXT, rights_risk TEXT, how_to_reuse TEXT);
CREATE INDEX ix_v_kind ON videos(kind, source);
""")
V = json.load(open(f"{R}/videos.json")); T = json.load(open(f"{R}/transcripts.json"))
for v in V:
    vid = v["id"]; m = json.load(open(f"{R}/frames/{vid}/meta.json"))
    a = {}
    p = f"{R}/analysis/{vid}.json"
    if os.path.exists(p):
        try: a = json.load(open(p))
        except Exception: a = {}
    views = v["views"] or 0
    c.execute("INSERT OR IGNORE INTO channels VALUES(?,?,?)", (v["channel_id"], v["channel"], v["subs"]))
    c.execute("INSERT INTO videos VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (
        vid, v["kind"], v["source"], v["channel_id"], v["title"], v["url"], v["upload_date"], int(v["duration"] or 0), views,
        v["likes"], v["comments"], (v["likes"] or 0) / views if views else None, (v["comments"] or 0) / views if views else None,
        1 if T.get(vid) else 0, len(m["cuts"]), m["frames"], v["description"], (T.get(vid) or {}).get("text"),
        a.get("topic"), a.get("hero"), a.get("hero_role"), a.get("media_type_overall"), a.get("hook"), a.get("subtitle_style"),
        a.get("reaction_overlays"), a.get("transition_summary"), a.get("audio_note")))
    for f in a.get("frames", []):
        c.execute("INSERT OR REPLACE INTO frames VALUES(?,?,?,?,?,?,?,?)", (vid, f.get("idx"), f.get("t"), f.get("type"),
            f.get("desc"), f.get("text_on_screen"), f.get("transition_to_next"), f"frames/{vid}/f{int(f.get('idx')):02d}.jpg"))
    for s in a.get("reuse_segments", []):
        c.execute("INSERT INTO reuse_segments VALUES(?,?,?,?,?,?,?)", (vid, s.get("t0"), s.get("t1"), s.get("what"),
            s.get("origin_guess"), s.get("rights_risk"), s.get("how_to_reuse")))
c.commit()
for t in ("channels", "videos", "frames", "reuse_segments"):
    print(t, c.execute(f"select count(*) from {t}").fetchone()[0])
print("analysed videos:", c.execute("select count(*) from videos where topic is not null").fetchone()[0])
