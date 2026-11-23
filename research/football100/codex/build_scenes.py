#!/usr/bin/env python3
"""Generate scenes_batch_NN.md (6 scenes each, ordered by video no, insert k) from scripts/NNN.json inserts."""
import json, os, re, glob
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); C = f"{H}/codex"
STYLE = {"simpsons":"SITCOM-YELLOW","southpark_cutout":"CUTOUT-PAPER","us_comic_book":"INK-COMIC","shonen_anime":"ACTION-ANIME",
 "looney_slapstick":"RUBBER-SLAPSTICK","peanuts_minimal":"STRIP-MINIMAL","rickmorty_like":"SCIFI-DEADPAN","ligne_claire":"CLEAR-LINE",None:"FLAT-POP"}
def clean(t): return re.sub(r"South Park[- ]style ?", "", t)
def sents(t): return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t.strip()) if s.strip()]
def cap(x): return x[:1].upper()+x[1:]
def split(story):
    story = re.sub(r"^\s*Setup:\s*", "", story)
    m = re.search(r"\bTwist:\s*", story); tw = story[m.end():].strip() if m else ""; pre = story[:m.start()].strip() if m else story
    g = re.search(r"\bGag:\s*", pre)
    if g: setup, gag = pre[:g.start()].strip(), pre[g.end():].strip()
    else:
        ss = sents(pre); setup, gag = " ".join(ss[:-1]) or pre, ss[-1] if len(ss) > 1 else pre
    if not tw: ss = sents(gag); tw = ss[-1]; gag = " ".join(ss[:-1]) or gag
    return setup, gag, tw
def beats(story):
    s, g, t = split(story); ss = sents(s) or [s]
    return [
     ("F01", "SETUP", f"Wide establishing shot, empty beat before action. {ss[0]}"),
     ("F02", "SETUP", ss[1] if len(ss) > 1 else "Characters step into position; fix the staging and the props that the gag will use."),
     ("F03", "SETUP", (ss[2] if len(ss) > 2 else "Hold the pose.") + " Anticipation: small wind-up or squash pose for the next action."),
     ("F04", "GAG", f"Gag starts. {cap(g)}"),
     ("F05", "GAG", "Gag escalates: bigger action, stretched or smeared pose, strongest silhouette so far."),
     ("F06", "GAG", "Gag keeps building: secondary reaction from the second character or prop."),
     ("F07", "GAG", "Near peak: exaggerated pose, the key prop clearly visible."),
     ("F08", "GAG", "Gag peak: the funniest drawing of the gag, held clean and readable."),
     ("F09", "TWIST", "One beat of silence: both characters freeze or look at each other (reaction, no new action)."),
     ("F10", "TWIST", f"Twist starts. {cap(t)}"),
     ("F11", "TWIST", "Twist peak: exaggerated surprise or deadpan pose. The reversal must be obvious without text."),
     ("F12", "TWIST", "Final hold on the punchline pose. Same background, same characters, clean last frame.")]
rows = []
A = json.load(open(f"{H}/scripts/assign.json"))
for a in sorted(A, key=lambda x: x["no"]):
    j = json.load(open(f"{H}/scripts/{a['no']:03d}.json"))
    for k, ins in enumerate(j["inserts"], 1):
        rows.append(dict(no=j["no"], k=k, style=STYLE[j.get("style") if j["comic"] else None], subj=j["subject"], title=j["title"],
                         chars=clean(ins.get("characters", "")), story=clean(ins["story"]), est=j["est_seconds"]))
for f in glob.glob(f"{C}/scenes_batch_*.md"): os.remove(f)
nb = (len(rows) + 5) // 6
for b in range(nb):
    chunk = rows[b*6:(b+1)*6]; out = [f"# Scenes batch {b+1:02d} of {nb:02d}", "",
      "Follow CODEX_MASTER_PROMPT.md. Output: 12 PNG frames per scene into flip/NNN_k/f01.png..f12.png. "
      f"Styles in this batch: {', '.join(sorted({r['style'] for r in chunk}))} (reuse the saved character sheet per style).", ""]
    for r in chunk:
        sc = f"{r['no']:03d}_{r['k']}"
        out += [f"## Scene {sc}  (video {r['no']}, insert {r['k']}, style {r['style']})", "",
          f"- Video: {r['title']}", f"- Output folder: flip/{sc}/  (f01.png ... f12.png, 1080x1920)", f"- Style: {r['style']}",
          f"- Characters: {r['chars']}", f"- Story: {r['story']}",
          "- On-screen text: only short words or numbers named in the story; otherwise none.", "", "| Frame | Phase | Beat |", "|---|---|---|"]
        out += [f"| {a} | {p} | {t} |" for a, p, t in beats(r["story"])] + [""]
    open(f"{C}/scenes_batch_{b+1:02d}.md", "w").write("\n".join(out))
print(len(rows), "scenes,", nb, "batches")
