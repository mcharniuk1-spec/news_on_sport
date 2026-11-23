#!/usr/bin/env python3
"""Frame-exact placement check: decode the export around each interlude and the clip itself, match every clip frame (middle 60 %) to the nearest export frame,
report the median offset in frames (expected 0) and the median pixel diff. PASS = |offset| <= 3 frames and diff < 8 (top 75 % of the frame, subtitles excluded). Usage: verify_seq.py [NNN ...]"""
import json, subprocess, sys, numpy as np
from concurrent.futures import ThreadPoolExecutor
H = "/Volumes/MAXITO/Video Operations/research/football100"
W_, H_ = 108, 192
def frames(path, t0, n):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(t0,0):.4f}", "-i", path, "-frames:v", str(n), "-vf", f"scale={W_}:{H_}:flags=area", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return np.frombuffer(r, np.uint8).reshape(-1, H_, W_, 3).astype(np.float32)[:, :int(H_ * 0.75)]
def check(no):
    M = json.load(open(f"{H}/v3/out/{no:03d}_meta.json")); out = []
    for s in M["seq"]:
        C = frames(s["clip"], 0, 400); n = len(C); lo, hi = int(n * 0.2), int(n * 0.8)
        pre = min(0.5, s["start"]); E = frames(M["file"], s["start"] - pre, n + 45); base = int(round(pre * 30))
        offs = []; diffs = []
        for j in range(lo, hi, 2):
            d = np.abs(E - C[j]).mean((1, 2, 3)); i = int(np.argmin(d)); offs.append(i - base - j); diffs.append(float(d[i]))
        mo = float(np.median(offs)); md = float(np.median(diffs))
        out.append((s["id"], mo, md, abs(mo) <= 3 and md < 8))
    return no, out
if __name__ == "__main__":
    nos = [int(a) for a in sys.argv[1:]] or list(range(1, 101)); bad = []
    with ThreadPoolExecutor(4) as ex:
        for no, out in ex.map(check, nos):
            f = [o for o in out if not o[3]]; bad += [(no, o[0], round(o[1], 1), round(o[2], 1)) for o in f]
            print("OK  " if not f else "FAIL", f"{no:03d}", "offsets(frames)", [round(o[1], 1) for o in out], "diff", [round(o[2], 1) for o in out], flush=True)
    print(f"{len(nos) - len({b[0] for b in bad})}/{len(nos)} videos frame-exact; bad: {bad}")
