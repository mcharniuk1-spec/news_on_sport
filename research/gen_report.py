#!/usr/bin/env python3
"""Stage 8: generate the linear frame-by-frame MD report from football_shorts.db."""
import sqlite3, os
R = os.path.dirname(os.path.abspath(__file__))
c = sqlite3.connect(f"{R}/football_shorts.db"); c.row_factory = sqlite3.Row
def esc(s): return (s or "").replace("|", "/").replace("\n", " ").strip()
def fmt(n): return f"{int(n):,}" if n is not None else "n/a"
o = []
o.append("# Football Shorts & Videos — frame-by-frame report (2026-11-20)\n")
o.append("Data: `football_shorts.db` (SQLite, MySQL-compatible schema). 110 Shorts + 110 long videos. Frames every 2 s; long videos analysed on the **first 60 s only**. Frame text descriptions are model-written from contact sheets: treat tile alignment as ±1–3 frames in dense videos; people are named only from titles/captions/overlays, not faces.\n")
o.append("## 1. Statistics by source\n")
for kind in ("short", "long"):
    o.append(f"### {kind.upper()} (views = avg of 10 selected videos; like% = likes/views; comments per 1k views; cuts = detected scene cuts in first 60 s)\n")
    o.append("| Source | Subs | Avg views | Like % | Comm/1k | Cuts | Avg dur s |\n|---|---|---|---|---|---|---|")
    for r in c.execute("""select source, max(subs) subs, avg(views) av, avg(like_rate)*100 lr, avg(comment_rate)*1000 cr, avg(cuts_in_first60) cu, avg(duration) d
        from videos v join channels using(channel_id) where kind=? group by source order by av desc""", (kind,)):
        o.append(f"| {r['source']} | {fmt(r['subs'])} | {fmt(r['av'])} | {r['lr']:.2f} | {r['cr']:.2f} | {r['cu']:.0f} | {r['d']:.0f} |")
    o.append("")
o.append("### Media type (analysed)\n\n| Kind | Media type | n | Avg views |\n|---|---|---|---|")
for r in c.execute("select kind, media_type, count(*) n, avg(views) av from videos group by 1,2 order by 1, n desc"):
    o.append(f"| {r['kind']} | {esc(r['media_type'])} | {r['n']} | {fmt(r['av'])} |")
o.append("\n### Frame types (4,942 frames)\n\n| Type | Frames |\n|---|---|")
for r in c.execute("select type, count(*) n from frames group by 1 order by 2 desc"): o.append(f"| {r['type']} | {r['n']} |")
o.append("\n### Reuse segments by rights risk\n\n| Risk | Segments |\n|---|---|")
for r in c.execute("select rights_risk, count(*) n from reuse_segments group by 1 order by 2 desc"): o.append(f"| {r['rights_risk']} | {r['n']} |")
o.append("\n## 2. Videos, linear walkthrough\n")
vids = c.execute("""select v.*, c.name cname, c.subs csubs from videos v join channels c using(channel_id)
    order by (kind='long'), (source='TRENDING_THIS_MONTH'), source, views desc""").fetchall()
cur = None
for v in vids:
    key = (v["kind"], v["source"])
    if key != cur:
        o.append(f"\n---\n# {v['kind'].upper()} — {v['source']}\n"); cur = key
    o.append(f"## {esc(v['title'])}\n")
    o.append(f"- **ID:** [{v['video_id']}]({v['url']}) · channel **{esc(v['cname'])}** ({fmt(v['csubs'])} subs) · uploaded {v['upload_date']} · {v['duration']} s")
    o.append(f"- **Stats:** {fmt(v['views'])} views · {fmt(v['likes'])} likes ({(v['like_rate'] or 0)*100:.2f}%) · {fmt(v['comments'])} comments · {v['cuts_in_first60']} cuts in first 60 s · captions: {'yes' if v['has_captions'] else 'no'}")
    o.append(f"- **Topic:** {esc(v['topic'])}")
    o.append(f"- **Hero / role:** {esc(v['hero'])} / {esc(v['hero_role'])}")
    o.append(f"- **Media:** {esc(v['media_type'])} · **Hook:** {esc(v['hook'])}")
    o.append(f"- **Subtitles:** {esc(v['subtitle_style'])} · **Overlays:** {esc(v['reaction_overlays'])}")
    o.append(f"- **Transitions:** {esc(v['transition_summary'])} · **Audio:** {esc(v['audio_note'])}")
    o.append(f"- **Contact sheet:** `sheets/{v['video_id']}.jpg`\n")
    o.append("| # | t | Type | Description | On-screen text | → next | Image |\n|---|---|---|---|---|---|---|")
    for f in c.execute("select * from frames where video_id=? order by idx", (v["video_id"],)):
        o.append(f"| {f['idx']} | {f['t_sec']}s | {esc(f['type'])} | {esc(f['description'])} | {esc(f['text_on_screen'])} | {esc(f['transition_to_next'])} | `{f['img_path']}` |")
    segs = c.execute("select * from reuse_segments where video_id=?", (v["video_id"],)).fetchall()
    if segs:
        o.append("\n**Reuse candidates:**\n")
        for s in segs: o.append(f"- {s['t0']}–{s['t1']} s · {esc(s['what'])} · origin: {esc(s['origin_guess'])} · rights risk: **{s['rights_risk']}** · {esc(s['how_to_reuse'])}")
    o.append("")
open(f"{R}/REPORT_frame_by_frame.md", "w").write("\n".join(o))
print(os.path.getsize(f"{R}/REPORT_frame_by_frame.md") // 1024, "KB")
