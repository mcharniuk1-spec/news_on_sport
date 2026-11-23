#!/usr/bin/env python3
"""Build the v2 animation plan: codex/v2/plan.json + codex/v2/plan/NNN.md + codex/v2/PLAN_SUMMARY.md
24 fps animated cutaways, 30 percent of each video (240..396 frames), 7-8 sequences per video, times locked to the narration.
Deterministic: same inputs -> same plan. Re-run only if scripts/ or voice/ change (then tell the user: frame counts may shift)."""
import glob, json, os, re, subprocess, sys
H = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); P = f"{H}/codex/v2"
FPS = 24; GAP = 0.3
STYLE = {"simpsons": "SITCOM-YELLOW", "southpark_cutout": "CUTOUT-PAPER", "us_comic_book": "INK-COMIC", "shonen_anime": "ACTION-ANIME",
         "looney_slapstick": "RUBBER-SLAPSTICK", "peanuts_minimal": "STRIP-MINIMAL", "rickmorty_like": "SCIFI-DEADPAN", "ligne_claire": "CLEAR-LINE", None: "FLAT-POP"}
WAVE = {"HOOK": 1, "NEWS": 1, "COMIC1": 1, "INTERVIEW": 2, "PROVOC": 2, "COMIC2": 2, "STATS": 3, "COMIC3": 3}
W = {"HOOK": .11, "NEWS": .14, "INTERVIEW": .13, "PROVOC": .10, "STATS": .10}   # comics share the remaining 0.42
LIM = {"HOOK": (36, 60), "NEWS": (42, 72), "INTERVIEW": (42, 72), "PROVOC": (36, 54), "STATS": (36, 54), "COMIC": (48, 96)}
dur = lambda p: float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def timing(no, J):
    L = J["lines"]; n = len(L)
    if J["voice"] == "kokoro":
        ds = json.load(open(f"{H}/voice/{no:03d}.json")); starts = [0.0]
        for d in ds[:-1]: starts.append(starts[-1] + d + GAP)
        vtot = sum(ds) + GAP * n
    else:
        vf = glob.glob(f"{H}/voice/{no:03d}_el.*")[0]; vtot = dur(vf); ch = [len(l["vo"]) for l in L]; c = sum(ch); starts = []; acc = 0
        for x in ch: starts.append(vtot * acc / c); acc += x
    return starts, vtot + 0.5


def sents(t): return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t.strip()) if s.strip()]


def split_story(story):
    story = re.sub(r"South Park[- ]style ?", "", re.sub(r"^\s*Setup:\s*", "", story))
    m = re.search(r"\bTwist:\s*", story); tw = story[m.end():].strip() if m else ""; pre = story[:m.start()].strip() if m else story
    g = re.search(r"\bGag:\s*", pre)
    if g: setup, gag = pre[:g.start()].strip(), pre[g.end():].strip()
    else:
        ss = sents(pre); setup, gag = " ".join(ss[:-1]) or pre, ss[-1] if len(ss) > 1 else pre
    if not tw: ss = sents(gag); tw = ss[-1]; gag = " ".join(ss[:-1]) or gag
    return setup, gag, tw


def alloc(F, k):
    cw = (1 - sum(W.values())) / k
    kinds = ["HOOK", "NEWS", "INTERVIEW", "PROVOC", "STATS"] + [f"COMIC{i+1}" for i in range(k)]
    fr = {}
    for kd in kinds:
        w = W.get(kd, cw); lo, hi = LIM[re.sub(r"\d", "", kd)]
        fr[kd] = max(lo, min(hi, int(round(F * w / 6)) * 6))
    order = [f"COMIC{i+1}" for i in range(k)] + ["NEWS", "INTERVIEW", "HOOK", "PROVOC", "STATS"]
    guard = 0
    while sum(fr.values()) != F and guard < 400:
        guard += 1; diff = F - sum(fr.values()); step = 6 if diff > 0 else -6
        for kd in order:
            lo, hi = LIM[re.sub(r"\d", "", kd)]
            if lo <= fr[kd] + step <= hi: fr[kd] += step; break
        else: break
    return fr, sum(fr.values())


def relevance(kind, i, L, n):
    vo = L[i]["vo"].lower(); card = L[i].get("card", "")
    if kind == "INTERVIEW": return 2.0 if re.search(r"\b(said|says|told|admits|admitted|claims|claimed|called|compared|insists|revealed)\b", vo) else 0
    if kind == "STATS": return 2.0 if re.search(r"\d", card) else 0
    if kind == "PROVOC": return 2.0 if i >= n // 2 else 0
    if kind == "NEWS": return 1.0 if i <= n // 2 else 0
    return 0


def place(no, J, starts, end):
    L = J["lines"]; n = len(L); T = starts[-1] - 0.1
    k = len(J["inserts"]); F = max(240, min(396, int(round(0.30 * FPS * end / 6)) * 6)); fr, F = alloc(F, k)   # F becomes the true sum (length minimums can lift it above the 30% target)
    D = {kd: fr[kd] / FPS for kd in fr}; occ = []; res = {}
    def free(s, e, g): return s >= 0 and e <= T and all(e + g <= a or s >= b + g for a, b in occ)
    res["HOOK"] = (0.0, D["HOOK"]); occ.append(res["HOOK"])
    # comics: locked to the line they follow (after_line, 1-based -> start of 0-based line index after_line)
    for i, ins in enumerate(sorted(J["inserts"], key=lambda x: x["after_line"])):
        kd = f"COMIC{i+1}"; li = max(1, min(n - 2, ins["after_line"])); s = starts[li]; ok = False
        for j in list(range(li, n - 1)) + list(range(li - 1, 0, -1)):
            s = starts[j]
            if free(s, s + D[kd], 0.8): ok = True; break
        if not ok:
            for g in (0.5, 0.3):
                for j in range(1, n - 1):
                    s = starts[j]
                    if free(s, s + D[kd], g): ok = True; break
                if ok: break
        assert ok, f"video {no}: cannot place {kd}"
        res[kd] = (s, s + D[kd]); occ.append(res[kd])
    for kd in ["INTERVIEW", "STATS", "PROVOC", "NEWS"]:
        best = None
        for g in (0.8, 0.5, 0.3):
            t = 0.25
            while t + D[kd] <= T:
                s_ = t; e_ = t + D[kd]
                if free(s_, e_, g):
                    j = max([i for i in range(n - 1) if starts[i] <= s_ + 0.15] or [0]); snap = min(abs(s_ - starts[i]) for i in range(n - 1))
                    md = min([min(abs(s_ - b), abs(a - e_)) for a, b in occ] + [6.0])
                    sc = min(md, 6.0) + relevance(kd, j, L, n) + (0.4 if snap < 0.15 else 0)
                    if best is None or sc > best[0]: best = (sc, s_, e_)
                t += 0.25
            if best: break
        assert best, f"video {no}: cannot place {kd}"
        res[kd] = (best[1], best[2]); occ.append((best[1], best[2]))
    return F, fr, res, T


def window_lines(starts, end, s, e):
    n = len(starts); out = []
    for i in range(n):
        a = starts[i]; b = starts[i + 1] if i + 1 < n else end
        if a < e and b > s: out.append(i)
    return out


BRIEF = {
 "HOOK": "HOOK-QUESTION. Open the video with one punchy QUESTION card (max 8 words, ends with '?') that poses the video's central tension. It asks, it never asserts a fact that is not in the narration. Animate the question in (typed, stamped or slammed), a reacting cartoon head or icon underneath, one provocative visual prop. End on a hard graphic hit that cuts to footage.",
 "NEWS": "NEWS-EXPLAINER (player / story description). A cartoon news card: caricature or silhouette of the subject (or a generic cartoon player in the subject's role), a lower-third strip with the NAME plus ONE fact copied from the narration, a small ticker with the card text, 2-3 flat icons (ball, boot, trophy-generic, stopwatch, flag) that animate in step with the narration words. Information first, but alive: every element moves on its own timing.",
 "INTERVIEW": "INTERVIEW INSERT. A mixed-zone or studio mini-scene: generic cartoon reporter with a generic microphone (no logo) and the subject as a caricature. Speech bubble text may ONLY be a phrase that already appears in the narration of this window. If the narration holds no quote, show the reporter's QUESTION in the bubble and let the subject answer with a gesture and an icon, no words. Add a 'REPORTER ASKS' style label, never a real outlet logo.",
 "PROVOC": "PROVOCATION / POLL. A two-option vote card about a team, a decision, a stat or a trend (never a person's character, body or private life): big question (max 7 words), two buttons A and B (max 3 words each), animated bars filling to a split, a ticking counter, a pulsing button. Playful, a little cheeky, never abusive, never a betting prompt.",
 "STATS": "STATS-ICON MONTAGE. 2-3 icon + number pairs, numbers taken from the narration or card text, counting up with bouncy easing, icons that act (ball bounces, whistle blows, stopwatch ticks), linked by a fast graphic transition. Show only numbers that are in the allowed text.",
}


def beat_ranges(N):
    b = lambda p: max(1, int(round(N * p)))
    a, g, s = b(.25), b(.40), b(.08)
    return [("SETUP", 1, a), ("GAG", a + 1, a + g), ("SILENT BEAT", a + g + 1, a + g + s), ("TWIST", a + g + s + 1, N)]


def main():
    plan = {}; summ = []; allowed_cache = {}
    for p in sorted(glob.glob(f"{H}/scripts/[0-9][0-9][0-9].json")):
        no = int(os.path.basename(p)[:3])
        if no > 100: continue
        J = json.load(open(p)); L = J["lines"]; n = len(L)
        starts, end = timing(no, J); F, fr, res, T = place(no, J, starts, end)
        style = STYLE[J.get("style") if J.get("comic") else None]
        seqs = sorted(res.items(), key=lambda kv: kv[1][0]); out = []
        ins_sorted = sorted(J["inserts"], key=lambda x: x["after_line"])
        for idx, (kd, (s, e)) in enumerate(seqs, 1):
            base = re.sub(r"\d", "", kd); N = fr[kd]
            wl = window_lines(starts, end, s, e)
            seq = dict(id=f"s{idx:02d}", kind=kd, type=base, wave=WAVE[kd], frames=N, start=round(s, 3), end=round(s + N / FPS, 3), line_from=wl[0], line_to=wl[-1], style=style)
            if base == "COMIC":
                ins = ins_sorted[int(kd[5:]) - 1]; seq["story"] = ins["story"]; seq["characters"] = ins.get("characters", "")
            out.append(seq)
        plan[f"{no:03d}"] = dict(no=no, title=J["title"], subject=J["subject"], voice=J["voice"], style=style, runtime=round(end, 2), usable_until=round(T, 2),
                                 frames=F, seconds=round(F / FPS, 2), share=round(F / FPS / end, 3), sequences=out)
        # ---- per-video markdown
        allowed = sorted({l["card"] for l in L if l.get("card")} | {J["subject"]})
        m = [f"# Video {no:03d}: {J['title']}", "",
             f"- Subject: {J['subject']}  |  Style label: **{style}**  |  Voice: {J['voice']}  |  Runtime: {end:.1f} s",
             f"- Animation budget: **{F} frames = {F/FPS:.1f} s at 24 fps** ({F/FPS/end*100:.0f}% of runtime), {len(out)} sequences. Output: `anim/{no:03d}/sNN/f0001.png ...`",
             f"- Allowed on-screen text (copy exactly, nothing else unless a section below creates a question/poll): {' | '.join(allowed)}",
             "- Thread A = NEWS (facts, icons, interview, stats). Thread B = COMIC (the cartoon cast and their running gag). The two threads cut against each other.", ""]
        m += ["## Narration (for timing and facts)", ""] + [f"{i}. [{starts[i]:5.1f}s] {l['vo']}" + (f"  (card: {l['card']})" if l.get('card') else "") for i, l in enumerate(L)] + ["", "## Sequences", "",
              "| id | wave | type | start | frames | seconds | covers narration lines |", "|---|---|---|---|---|---|---|"]
        for s_ in out: m.append(f"| {s_['id']} | W{s_['wave']} | {s_['kind']} | {s_['start']:.2f}s | {s_['frames']} | {s_['frames']/FPS:.2f} | {s_['line_from']}-{s_['line_to']} |")
        m.append("")
        for s_ in out:
            N = s_["frames"]
            m += [f"## {s_['id']}  {s_['kind']}  (wave {s_['wave']}, {N} frames, start {s_['start']:.2f}s)", "", f"- Folder: `anim/{no:03d}/{s_['id']}/`  f0001.png ... f{N:04d}.png",
                  f"- Frames 1-6 = transition IN, frames {N-5}-{N} = transition OUT (pick a different pair from the transition library for each sequence).",
                  f"- Narration playing under this sequence: " + " / ".join(f'"{L[i]["vo"]}"' for i in range(s_["line_from"], s_["line_to"] + 1))]
            if s_["type"] == "COMIC":
                su, ga, tw = split_story(s_["story"]); br = beat_ranges(N)
                m += [f"- Characters: {s_['characters']}", f"- Thread: B (chapter {s_['kind'][5:]}) - same cast, same recurring prop as the other COMIC sequences of this video; the last COMIC calls back to the first one's prop.",
                      f"- Story: {s_['story']}", "", "| Frames | Phase | Beat |", "|---|---|---|",
                      f"| {br[0][1]}-{br[0][2]} | SETUP | {su} (first 6 frames are the transition) |", f"| {br[1][1]}-{br[1][2]} | GAG | {ga} (build in 3-4 escalating steps) |",
                      f"| {br[2][1]}-{br[2][2]} | SILENT BEAT | Freeze the action; characters look; only tiny breathing/blink/prop drift moves |", f"| {br[3][1]}-{br[3][2]} | TWIST | {tw} (hold the punchline pose, then transition OUT) |"]
            else:
                m += [f"- Brief: {BRIEF[s_['type']]}"]
                if s_["type"] in ("HOOK", "PROVOC"): m += ["- Text: you write the question/poll text. Use only facts present in the narration. Put the exact strings you chose into the storyboard."]
            m.append("")
        open(f"{P}/plan/{no:03d}.md", "w", encoding="utf-8").write("\n".join(m))
        summ.append((no, F, len(out), end))
    json.dump(plan, open(f"{P}/plan.json", "w"), indent=1)
    tot = sum(x[1] for x in summ); byw = {1: 0, 2: 0, 3: 0}; bykind = {}
    for v in plan.values():
        for s in v["sequences"]: byw[s["wave"]] += s["frames"]; bykind[s["type"]] = bykind.get(s["type"], 0) + s["frames"]
    o = [f"# Plan summary (24 fps)", "", f"- Videos: {len(summ)}  |  sequences: {sum(x[2] for x in summ)}  |  frames: **{tot}**  |  animation seconds: {tot/FPS:.0f}",
         f"- Per video: min {min(x[1] for x in summ)}, max {max(x[1] for x in summ)}, mean {tot/len(summ):.0f} frames",
         f"- By wave: W1 {byw[1]} frames, W2 {byw[2]} frames, W3 {byw[3]} frames", "- By type: " + ", ".join(f"{k} {v}" for k, v in sorted(bykind.items())), "",
         "| video | frames | seq | runtime s |", "|---|---|---|---|"] + [f"| {a:03d} | {b} | {c} | {d:.1f} |" for a, b, c, d in summ]
    open(f"{P}/PLAN_SUMMARY.md", "w").write("\n".join(o))
    print(f"videos {len(summ)}, sequences {sum(x[2] for x in summ)}, frames {tot}, per video {min(x[1] for x in summ)}..{max(x[1] for x in summ)}, waves {byw}")


if __name__ == "__main__": main()
