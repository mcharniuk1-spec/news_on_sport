#!/usr/bin/env python3
"""Plan v3 for videos 011-100: every interlude redrawn in ONE sitcom-yellow style, MORE interludes (extra micro-inserts in the free gaps) and a new poster per video.
Writes codex/v3/plan_v3.json, codex/v3/plan/NNN.md and codex/v3/PLAN_SUMMARY.md. Deterministic. Frame counts are multiples of 6 (24 fps)."""
import json, os, re
H = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); P3 = f"{H}/codex/v3"
V2 = json.load(open(f"{H}/codex/v2/plan.json"))
FIRST, LAST = 11, 100
MICRO = [("REACTION", 24), ("STICKER", 18), ("THOUGHT", 24), ("CROWD", 24), ("ZOOMFACE", 18), ("TICKER", 18)]
BRIEF = {
 "REACTION": "REACTION CUT-IN. Close-up of ONE cast character (use the video's recurring character) reacting to what the narrator just said: eyes widen, jaw drops, eyebrows jump, a sweat drop or a smug smirk. Big head filling 60 percent of the frame width, 3-4 distinct expression steps, a tiny sound word (WOW, OOF, HA) in a speech burst. Text: 1 short word only.",
 "STICKER": "STICKER POP. One bold number or 1-3 word fact from the allowed text on a chunky sticker that slams in with overshoot, spins slightly, shakes, then hits the screen edge. A simple icon (ball, boot, whistle, trophy, stopwatch, flag) bounces next to it. No characters needed.",
 "THOUGHT": "THOUGHT BUBBLE JOKE. A cast character stands in the middle; a big thought bubble pops above with a tiny cartoon of the joke implied by the narration (an icon or a 2-frame mini scene). He looks up, the bubble wobbles, then pops. Text: at most 3 words, from the allowed text.",
 "CROWD": "CROWD CUTAWAY. Four to six simple stadium fans in the foreground (yellow skin, scarves, foam fingers, bald head, cap) reacting in a wave: jump, gasp, cheer, facepalm. One fan holds a card with 1-3 allowed words. Loud, funny, readable.",
 "ZOOMFACE": "ZOOM FACE. Fast push-in on the face of the subject caricature (name label allowed) with a shake, flash and a hard stop. Eyes do a 3-step shift. Text: the name only.",
 "TICKER": "NEWS TICKER FLASH. A breaking-news strip sweeps across the middle (red BREAKING style label in plain words from the allowed text, no outlet logo), a small icon ball rolls along it, strip slides out. Text: the allowed card text only.",
}


def md_sections(txt):
    parts = re.split(r"(?m)^## ", txt)
    return {p.split(None, 1)[0]: "## " + p for p in parts[1:] if re.match(r"s\d\d\b", p)}


def narration_block(txt):
    m = re.search(r"## Narration.*?\n(.*?)\n## Sequences", txt, re.S)
    return m.group(1).strip() if m else ""


def allowed_line(txt):
    m = re.search(r"^- Allowed on-screen text.*$", txt, re.M)
    return m.group(0) if m else ""


def line_at(txt, t):
    best = None
    for m in re.finditer(r"^(\d+)\. \[\s*([\d.]+)s\] (.*)$", txt, re.M):
        if float(m.group(2)) <= t: best = (int(m.group(1)), m.group(3))
    return best


def build():
    os.makedirs(f"{P3}/plan", exist_ok=True); out = {}; summ = []
    for no in range(FIRST, LAST + 1):
        k = f"{no:03d}"; v = V2[k]; md = open(f"{H}/codex/v2/plan/{k}.md", encoding="utf-8").read()
        secs = md_sections(md); seqs = []
        for s in v["sequences"]:
            seqs.append({"id": s["id"], "kind": s["kind"], "type": s["type"], "frames": s["frames"], "start": s["start"], "end": s["end"], "origin": "v2"})
        # free gaps (>= 1.4 s) between sequences and before the last-line limit
        gaps = []; prev = 0.0
        for s in sorted(seqs, key=lambda x: x["start"]): gaps.append((prev, s["start"])); prev = s["end"]
        gaps.append((prev, v["usable_until"]))
        extra = []; n = 0; ti = (no * 2) % len(MICRO)
        for a, b in gaps:
            room = b - a
            t = a + 0.45
            while room >= 1.5 + 0.45 and len(extra) < 6:
                kind, fr = MICRO[ti % len(MICRO)]; ti += 1; d = fr / 24
                if t + d > b - 0.45: break
                n += 1; extra.append({"id": f"s{50 + n:02d}", "kind": kind, "type": "MICRO", "frames": fr, "start": round(t, 2), "end": round(t + d, 2), "origin": "v3"})
                t += d + 0.45; room = b - t
        allseq = sorted(seqs + extra, key=lambda x: x["start"])
        total = sum(s["frames"] for s in allseq)
        out[k] = {"no": no, "title": v["title"], "subject": v["subject"], "voice": v["voice"], "runtime": v["runtime"], "usable_until": v["usable_until"], "frames": total,
                  "seconds": round(total / 24, 1), "share": round(total / 24 / v["runtime"], 3), "style": "SITCOM-YELLOW", "sequences": allseq}
        try: meta = json.load(open(f"{H}/publish/metadata_v2/{k}.json"))
        except Exception: meta = {"title": v["title"], "description": ""}
        narr = narration_block(md); allowed = allowed_line(md)
        L = [f"# Video {k} (v3, sitcom-yellow redraw): {v['title']}", "",
             f"- Subject: {v['subject']}  |  Voice: {v['voice']}  |  Runtime: {v['runtime']} s",
             f"- Style: **SITCOM-YELLOW for every sequence and the poster** (see master prompt section 1). The older style label of the v2 plan ({v['style']}) is ignored.",
             f"- Animation budget: **{total} frames = {total / 24:.1f} s at 24 fps**, {len(allseq)} sequences ({len(seqs)} planned scenes + {len(extra)} new micro-inserts). Output: `anim3/{k}/sNN/f0001.png ...`",
             f"- Poster output: `poster3/{k}.png` (1080x1920). Brief below.", allowed, "",
             "## Poster brief", "",
             f"- Channel title (for the thesis, do not copy it verbatim): {meta['title']}",
             f"- Subject / players to make recognisable by prop, kit colour and name label: {v['subject']}",
             "- Pick the ONE thesis a scrolling viewer must get in one second, from the narration below. Main text: 2 to 7 words in total (big, chunky). Plus 2 or 3 tiny comment or emotion bubbles (1-3 words each, e.g. OOF, WAIT WHAT, HA) next to the characters.",
             "- Scene: the hero character (yellow skin, the video's recurring cast) in a large comic panel: the subject caricature in the middle, one hero prop that stands for the thesis, a second character reacting. Strong silhouette, high contrast, readable on a phone thumbnail.",
             "- Keep the top 12 percent and the bottom 20 percent free of text. No logos, no real crests, no photos.", "",
             "## Narration (for timing and facts)", "", narr, "", "## Sequences", "",
             "| id | type | start | frames | seconds | origin |", "|---|---|---|---|---|---|"]
        for s in allseq: L.append(f"| {s['id']} | {s.get('kind')} | {s['start']:.2f}s | {s['frames']} | {s['frames'] / 24:.2f} | {s['origin']} |")
        L.append("")
        for s in allseq:
            if s["origin"] == "v2" and s["id"] in secs:
                sec = secs[s["id"]].replace("anim/", "anim3/")
                sec = re.sub(r"^## (s\d\d) +(\S+)", lambda m: f"## {m.group(1)}  {m.group(2)}", sec, count=1)
                L.append(sec.rstrip() + "\n\n- Style override: draw it in SITCOM-YELLOW (master prompt section 1). Make the scene bolder and simpler: one idea, big characters, at most 7 words on screen.\n")
            else:
                ln = line_at(md, s["start"])
                L += [f"## {s['id']}  {s['kind']}  (micro-insert, {s['frames']} frames, start {s['start']:.2f}s)", "",
                      f"- Folder: `anim3/{k}/{s['id']}/`  f0001.png ... f{s['frames']:04d}.png",
                      f"- Frames 1-4 = transition IN, last 4 frames = transition OUT (any pair from the transition library; vary it).",
                      f"- Narration playing under it: \"{ln[1] if ln else ''}\"",
                      f"- Brief: {BRIEF[s['kind']]}", ""]
        open(f"{P3}/plan/{k}.md", "w", encoding="utf-8").write("\n".join(L))
        summ.append(f"| {k} | {v['runtime']} | {len(seqs)} + {len(extra)} | {total} | {total / 24:.1f} | {total / 24 / v['runtime'] * 100:.0f}% |")
    json.dump(out, open(f"{P3}/plan_v3.json", "w"), indent=1)
    tf = sum(x["frames"] for x in out.values()); ns = sum(len(x["sequences"]) for x in out.values())
    open(f"{P3}/PLAN_SUMMARY.md", "w").write("# Plan v3 summary (videos 011-100)\n\n" + f"{len(out)} videos, {ns} sequences, {tf} frames (24 fps) plus {len(out)} posters.\n\n| video | runtime s | scenes + micro | frames | seconds | share |\n|---|---|---|---|---|---|\n" + "\n".join(summ) + "\n")
    print(len(out), "videos", ns, "sequences", tf, "frames")


if __name__ == "__main__":
    build()
