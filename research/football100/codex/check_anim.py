#!/usr/bin/env python3
"""Verify v2 animation frames: anim/NNN/sKK/f0001..fNNNN.png for every sequence in codex/v2/plan.json.
  check_anim.py                    report all sequences (writes anim/_status.json)
  check_anim.py --todo             print ids (NNN/sKK) that do NOT pass, in wave order then video order (resume list)
  check_anim.py --todo --wave 1    only wave 1 (then 2, then 3)
  check_anim.py --video 7          only video 007
  check_anim.py --fix              first normalise frames: flatten alpha to white, resize 9:16 images to 1080x1920 (Lanczos)
Per sequence: exactly the planned frame count, f0001..fNNNN.png, real PNG, 1080x1920, opaque, NO two neighbouring frames identical
(24 distinct drawings per second), first frame differs from the middle and last frame, no blank frame. Warns (does not fail) on a big jump
between neighbours outside the 6-frame transition windows. Exit 0 only if every checked sequence passes."""
import json, os, sys
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageChops, ImageStat
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); W, Hh = 1080, 1920
A = sys.argv[1:]; fix = "--fix" in A; todo = "--todo" in A
wave = int(A[A.index("--wave") + 1]) if "--wave" in A else None; video = int(A[A.index("--video") + 1]) if "--video" in A else None
PLAN = json.load(open(f"{H}/codex/v2/plan.json"))


def small(im): return im.convert("L").resize((108, 192))


def check(job):
    vid, sid, N = job; d = f"{H}/anim/{vid}/{sid}"; errs = []; warns = []
    want = [f"f{i:04d}.png" for i in range(1, N + 1)]
    have = sorted(os.listdir(d)) if os.path.isdir(d) else []
    miss = [w for w in want if w not in have]; extra = [h for h in have if h not in want and not h.startswith(".")]
    if miss: errs.append(f"missing {len(miss)}/{N} (first {miss[0]})")
    if extra: errs.append(f"extra files {extra[:3]}")
    if miss: return f"{vid}/{sid}", errs, warns
    sm = []
    for i, w in enumerate(want, 1):
        p = f"{d}/{w}"
        try: im = Image.open(p); im.load()
        except Exception as e: errs.append(f"f{i:04d} unreadable: {e}"); sm.append(None); continue
        if im.format != "PNG": errs.append(f"f{i:04d} is {im.format}, not PNG")
        if fix and (im.mode in ("RGBA", "LA", "P") or im.size != (W, Hh)):
            if im.mode in ("RGBA", "LA", "P"):
                im = im.convert("RGBA"); bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg.convert("RGB")
            if im.size != (W, Hh) and abs(im.size[0] / im.size[1] - 9 / 16) < 0.01: im = im.resize((W, Hh), Image.LANCZOS)
            im.convert("RGB").save(p, "PNG")
        if im.mode in ("RGBA", "LA") and im.getchannel("A").getextrema()[0] < 255: errs.append(f"f{i:04d} has transparency")
        if im.size != (W, Hh): errs.append(f"f{i:04d} size {im.size[0]}x{im.size[1]} (need {W}x{Hh})")
        sm.append(small(im))
    if errs or any(s is None for s in sm): return f"{vid}/{sid}", errs[:8], warns
    dup = [i + 1 for i in range(N - 1) if ImageChops.difference(sm[i], sm[i + 1]).getbbox() is None]
    if dup: errs.append(f"{len(dup)} duplicate neighbours, redraw so each frame differs: f{dup[0]:04d}=f{dup[0]+1:04d}" + (f" ... f{dup[-1]:04d}" if len(dup) > 1 else ""))
    if sum(ImageStat.Stat(ImageChops.difference(sm[0], sm[N // 2])).mean) < 1.0 or sum(ImageStat.Stat(ImageChops.difference(sm[N // 2], sm[-1])).mean) < 1.0:
        errs.append("start, middle and end look the same (no action)")
    for i, s in enumerate(sm, 1):
        m = ImageStat.Stat(s).mean[0]
        if m < 6 or m > 252: errs.append(f"f{i:04d} looks blank (mean {m:.0f})"); break
    jumps = [i + 1 for i in range(6, N - 7) if ImageStat.Stat(ImageChops.difference(sm[i], sm[i + 1])).mean[0] > 70]
    if jumps: warns.append(f"big jump after f{jumps[0]:04d}" + (f" (+{len(jumps)-1} more)" if len(jumps) > 1 else ""))
    return f"{vid}/{sid}", errs, warns


def main():
    jobs = []
    for vid, v in PLAN.items():
        if video is not None and int(vid) != video: continue
        for s in v["sequences"]:
            if wave is not None and s["wave"] != wave: continue
            jobs.append((s["wave"], int(vid), vid, s["id"], s["frames"]))
    jobs.sort(key=lambda j: (j[0], j[1], j[3]))
    with ProcessPoolExecutor(max(2, (os.cpu_count() or 4) - 2)) as ex: res = list(ex.map(check, [(j[2], j[3], j[4]) for j in jobs], chunksize=4))
    bad = {k: e for k, e, w in res if e}; warn = {k: w for k, e, w in res if w and not e}
    if todo: print("\n".join(bad)); sys.exit(1 if bad else 0)
    for k, e in bad.items(): print(f"FAIL {k}: " + "; ".join(e))
    for k, w in warn.items(): print(f"warn {k}: " + "; ".join(w))
    okf = sum(j[4] for j, (k, e, w) in zip(jobs, res) if not e); tot = sum(j[4] for j in jobs)
    print(f"{len(res)-len(bad)}/{len(res)} sequences pass ({okf}/{tot} frames)" + (f", {len(bad)} to do" if bad else " - all good"))
    if wave is None and video is None:
        os.makedirs(f"{H}/anim", exist_ok=True)
        json.dump({"pass": [k for k, e, w in res if not e], "fail": bad, "warn": warn, "frames_ok": okf, "frames_total": tot}, open(f"{H}/anim/_status.json", "w"), indent=1)
    sys.exit(1 if bad else 0)


if __name__ == "__main__": main()
