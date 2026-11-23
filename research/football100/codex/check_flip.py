#!/usr/bin/env python3
"""Verify flipbook frames: flip/NNN_k/f01..f12.png for every scene listed in codex/scenes_batch_*.md.
  check_flip.py                 report all 261 scenes (writes flip/_status.json)
  check_flip.py --todo          print only scene ids that do NOT pass (one per line, resume list)
  check_flip.py --batch 07      only scenes of scenes_batch_07.md
  check_flip.py --fix           first normalise frames: flatten alpha to white, resize 9:16 images to 1080x1920 (Lanczos)
Checks per scene: exactly 12 files f01..f12.png, no extra files, real PNG, 1080x1920, opaque, no two neighbouring frames identical,
f01 differs from f12 (the action moved), mean brightness not near-black/near-white (blank frame guard).
Exit code 0 only if every checked scene passes."""
import glob, json, os, re, sys
from PIL import Image, ImageChops, ImageStat
H = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
fix = "--fix" in args; todo = "--todo" in args
batch = args[args.index("--batch") + 1].zfill(2) if "--batch" in args else None
files = sorted(glob.glob(f"{H}/codex/scenes_batch_{batch or '[0-9][0-9]'}.md"))
scenes = []
for f in files:
    scenes += re.findall(r"^## Scene (\d{3}_\d)", open(f, encoding="utf-8").read(), re.M)
W, Hh = 1080, 1920


def small(im): return im.convert("L").resize((54, 96))


def check(sc):
    d = f"{H}/flip/{sc}"; errs = []
    want = [f"f{i:02d}.png" for i in range(1, 13)]
    have = sorted(os.listdir(d)) if os.path.isdir(d) else []
    miss = [w for w in want if w not in have]; extra = [h for h in have if h not in want and not h.startswith(".")]
    if miss: errs.append(f"missing {len(miss)} ({miss[0]}..)")
    if extra: errs.append(f"extra files {extra[:3]}")
    if miss: return errs
    ims = []
    for w in want:
        p = f"{d}/{w}"
        try: im = Image.open(p); im.load()
        except Exception as e: errs.append(f"{w} unreadable: {e}"); continue
        if im.format != "PNG": errs.append(f"{w} is {im.format}, not PNG")
        if fix and (im.mode in ("RGBA", "LA", "P") or im.size != (W, Hh)):
            if im.mode in ("RGBA", "LA", "P"):
                im = im.convert("RGBA"); bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg.convert("RGB")
            if im.size != (W, Hh) and abs(im.size[0] / im.size[1] - 9 / 16) < 0.01: im = im.resize((W, Hh), Image.LANCZOS)
            im.convert("RGB").save(p, "PNG")
        if im.mode in ("RGBA", "LA"):
            if im.getchannel("A").getextrema()[0] < 255: errs.append(f"{w} has transparency")
        if im.size != (W, Hh): errs.append(f"{w} size {im.size[0]}x{im.size[1]} (need {W}x{Hh})")
        ims.append((w, im))
    if errs: return errs
    sm = [small(im) for _, im in ims]
    for i in range(11):
        if ImageChops.difference(sm[i], sm[i + 1]).getbbox() is None: errs.append(f"{ims[i][0]} == {ims[i + 1][0]} (duplicate)")
    if sum(ImageStat.Stat(ImageChops.difference(sm[0], sm[11])).mean) < 1.0: errs.append("f01 and f12 look the same (no action)")
    for (w, _), s in zip(ims, sm):
        m = ImageStat.Stat(s).mean[0]
        if m < 8 or m > 250: errs.append(f"{w} looks blank (mean {m:.0f})")
    return errs


res = {}
for sc in scenes:
    res[sc] = check(sc)
bad = {k: v for k, v in res.items() if v}
if todo:
    print("\n".join(bad)); sys.exit(1 if bad else 0)
for k, v in bad.items(): print(f"FAIL {k}: " + "; ".join(v))
ok = len(res) - len(bad)
print(f"{ok}/{len(res)} scenes pass" + (f" ({len(bad)} to do)" if bad else " - all good"))
if not batch:
    os.makedirs(f"{H}/flip", exist_ok=True)
    json.dump({"pass": [k for k, v in res.items() if not v], "fail": {k: v for k, v in bad.items()}}, open(f"{H}/flip/_status.json", "w"), indent=1)
sys.exit(1 if bad else 0)
