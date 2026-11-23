#!/usr/bin/env python3
"""Align the script words to ASR word times and place the planned interludes on the timeline.
  timing.py NNN ...   -> v2/timing/NNN.json
Voice-relative seconds everywhere except `seq[*].start/end` which are TIMELINE seconds (voice starts at VO=0.1 s on the timeline)."""
import difflib, glob, json, os, re, subprocess, sys
H = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VO = 0.1; GAP = 0.3


def norm(w): return re.sub(r"[^a-z0-9]", "", w.lower())


def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]))


def build(no):
    J = json.load(open(f"{H}/scripts/{no:03d}.json")); L = J["lines"]; n = len(L)
    A = json.load(open(f"{H}/v2/asr/{no:03d}.json")); vtot = A["dur"]
    # ---- estimated / exact line windows (same as build100)
    if J["voice"] == "kokoro":
        ds = json.load(open(f"{H}/voice/{no:03d}.json")); exact = []; t = 0.0
        for d in ds: exact.append((t, t + d)); t += d + GAP
        est = [a for a, _ in exact]
    else:
        exact = None; ch = [len(l["vo"]) for l in L]; c = sum(ch); est = []; acc = 0
        for x in ch: est.append(vtot * acc / c); acc += x
    # ---- script display words, sub-tokens for matching
    words = []; sub = []   # sub: (norm, word_index)
    for li, l in enumerate(L):
        for tok in l["vo"].split():
            wi = len(words); words.append({"w": tok, "line": li})
            for part in re.split(r"[-/]", tok):
                nn = norm(part)
                if nn: sub.append((nn, wi))
    asr = [(norm(w["w"]), w) for w in A["words"]]
    asr = [(k, w) for k, w in asr if k]
    sm = difflib.SequenceMatcher(None, [k for k, _ in sub], [k for k, _ in asr], autojunk=False)
    wt = [None] * len(words)   # [start,end] per display word from matched sub tokens
    pairs = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for k in range(i2 - i1): pairs.append((i1 + k, j1 + k))
    for i, j in pairs:
        wi = sub[i][1]; w = asr[j][1]
        if wt[wi] is None: wt[wi] = [w["s"], w["e"]]
        else: wt[wi][0] = min(wt[wi][0], w["s"]); wt[wi][1] = max(wt[wi][1], w["e"])
    matched = sum(1 for x in wt if x)
    # ---- interpolate unmatched words by character length between matched neighbours
    N = len(words); i = 0
    while i < N:
        if wt[i] is not None: i += 1; continue
        j = i
        while j < N and wt[j] is None: j += 1
        lo = wt[i - 1][1] if i > 0 else 0.0
        hi = wt[j][0] if j < N else vtot
        if hi < lo: hi = lo + 0.05 * (j - i)
        tot = sum(len(words[k]["w"]) + 1 for k in range(i, j)); acc = 0
        for k in range(i, j):
            a = lo + (hi - lo) * acc / tot; acc += len(words[k]["w"]) + 1; b = lo + (hi - lo) * acc / tot
            wt[k] = [a, b]
        i = j
    # ---- monotonic, non-overlapping, min width
    prev = 0.0
    for k in range(N):
        a, b = wt[k]; a = max(a, prev); b = max(b, a + 0.06); wt[k] = [a, b]; prev = a + 0.02
    # ---- kokoro: clamp each word into its exact line window
    if exact:
        for k, w in enumerate(words):
            a0, b0 = exact[w["line"]]; a, b = wt[k]
            a = min(max(a, a0), b0 - 0.05); b = min(max(b, a + 0.06), b0 + 0.05); wt[k] = [a, b]
    for k, w in enumerate(words): w["s"] = round(wt[k][0], 3); w["e"] = round(wt[k][1], 3)
    # ---- line starts / ends
    ls = []; le = []
    for li in range(n):
        ws = [w for w in words if w["line"] == li]
        a = exact[li][0] if exact else ws[0]["s"]
        b = exact[li][1] if exact else ws[-1]["e"]
        ls.append(round(a, 3)); le.append(round(b, 3))
    return {"no": no, "voice": J["voice"], "vtot": vtot, "matched": matched, "script_words": N, "line_starts": ls, "line_ends": le, "est_starts": [round(x, 3) for x in est], "words": words}


def place(no, T, clip_dir=None):
    """Timeline placement of the planned sequences. Returns list of dicts {id,kind,start,end,frames,clip?} in order."""
    P = json.load(open(f"{H}/codex/v2/plan.json"))[f"{no:03d}"]
    ls = T["line_starts"]; est = T["est_starts"]; last = ls[-1] + VO - 0.1
    out = []; prev_end = -0.3; warn = []
    for s in P["sequences"]:
        d = (s["end"] - s["start"])
        # keep the planned duration at 30 fps (round(frames/24*30) frames)
        d = round(s["frames"] / 24 * 30) / 30
        shift = ls[s["line_from"]] - est[s["line_from"]]
        a = s["start"] + shift + VO
        if a < prev_end + 0.3: a = prev_end + 0.3
        if a + d > last:
            a2 = last - d
            if a2 >= prev_end + 0.2: a = a2
            else: warn.append(f"{s['id']} dropped (no room)"); continue
        out.append({"id": s["id"], "kind": s["kind"], "start": round(a, 3), "end": round(a + d, 3), "frames": s["frames"], "line_from": s["line_from"], "shift": round(shift, 3)})
        prev_end = a + d
    return out, warn


if __name__ == "__main__":
    os.makedirs(f"{H}/v2/timing", exist_ok=True)
    for a in sys.argv[1:]:
        no = int(a); T = build(no); S, W = place(no, T); T["seq"] = S; T["warn"] = W
        json.dump(T, open(f"{H}/v2/timing/{no:03d}.json", "w"), indent=1)
        print(no, f"matched {T['matched']}/{T['script_words']}", "seq", len(S), "warn", W, flush=True)
