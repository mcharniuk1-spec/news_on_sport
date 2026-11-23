#!/usr/bin/env python3
"""Checker for the v3 art (own tool; not codex/check_anim.py).
  check_v3.py                  summary + writes anim3/_status.json
  check_v3.py --todo [--wave N] [--video NNN]   print ids that do not pass (poster3 ids as 'NNN/poster', sequences as 'NNN/sKK'), exit 1 if any
  check_v3.py --fix [--video NNN]               flatten alpha and resize 9:16 images to 1080x1920 before checking
Waves: 0 = poster + sheet, 1 = HOOK NEWS COMIC1 + micro, 2 = INTERVIEW PROVOC COMIC2, 3 = STATS COMIC3.
Per sequence: exact frame count f0001..fNNNN, PNG, 1080x1920, opaque, no identical neighbouring frames, no blank frame, first/middle/last differ.
Poster: exists, PNG, 1080x1920, opaque, not blank, top 12 % and bottom 20 % low-detail (text-free band check)."""
import json, os, sys
from concurrent.futures import ProcessPoolExecutor
from PIL import Image, ImageChops, ImageStat
H = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PLAN = json.load(open(f"{H}/codex/v3/plan_v3.json"))
args = sys.argv[1:]; FIX = "--fix" in args; TODO = "--todo" in args
wave = int(args[args.index("--wave") + 1]) if "--wave" in args else None
video = args[args.index("--video") + 1].zfill(3) if "--video" in args else None
W, Hh = 1080, 1920
WAVE = {"HOOK": 1, "NEWS": 1, "COMIC1": 1, "REACTION": 1, "STICKER": 1, "THOUGHT": 1, "CROWD": 1, "ZOOMFACE": 1, "TICKER": 1, "INTERVIEW": 2, "PROVOC": 2, "COMIC2": 2, "STATS": 3, "COMIC3": 3}


def norm(im, path):
    if im.mode in ("RGBA", "LA", "P"):
        im = im.convert("RGBA"); bg = Image.new("RGBA", im.size, (255, 255, 255, 255)); bg.alpha_composite(im); im = bg.convert("RGB")
    if im.size != (W, Hh) and abs(im.size[0] / im.size[1] - 9 / 16) < 0.01: im = im.resize((W, Hh), Image.LANCZOS)
    im.convert("RGB").save(path, "PNG"); return im


def small(im): return im.convert("L").resize((54, 96))


def check_poster(k):
    p = f"{H}/poster3/{k}.png"
    if not os.path.exists(p): return ["missing"]
    try: im = Image.open(p); im.load()
    except Exception as e: return [f"unreadable {e}"]
    if FIX and (im.mode != "RGB" or im.size != (W, Hh)): im = norm(im, p)
    e = []
    if im.format != "PNG": e.append(f"{im.format} not PNG")
    if im.size != (W, Hh): e.append(f"size {im.size[0]}x{im.size[1]}")
    if im.mode in ("RGBA", "LA") and im.getchannel("A").getextrema()[0] < 255: e.append("transparency")
    if e: return e
    g = im.convert("L"); m = ImageStat.Stat(g).mean[0]
    if m < 8 or m > 250: e.append("blank")
    for name, box in (("top 12%", (0, 0, W, 230)), ("bottom 20%", (0, 1536, W, Hh))):
        s = ImageStat.Stat(g.crop(box)).stddev[0]
        if s > 38: e.append(f"{name} band busy (stddev {s:.0f}): keep it plain, no text")
    return e


def check_seq(args_):
    k, sid, n = args_
    d = f"{H}/anim3/{k}/{sid}"; e = []
    have = sorted(f for f in os.listdir(d)) if os.path.isdir(d) else []
    want = [f"f{i:04d}.png" for i in range(1, n + 1)]
    miss = [w for w in want if w not in have]; extra = [h for h in have if h not in want and not h.startswith(".")]
    if miss: e.append(f"missing {len(miss)}/{n} (first {miss[0]})")
    if extra: e.append(f"extra files {extra[:3]}")
    if miss: return k, sid, e
    sm = []
    for w in want:
        p = f"{d}/{w}"
        try: im = Image.open(p); im.load()
        except Exception as ex: e.append(f"{w} unreadable"); continue
        if FIX and (im.mode != "RGB" or im.size != (W, Hh)): im = norm(im, p)
        if im.format != "PNG": e.append(f"{w} not PNG")
        if im.size != (W, Hh): e.append(f"{w} size {im.size[0]}x{im.size[1]}")
        if im.mode in ("RGBA", "LA") and im.getchannel("A").getextrema()[0] < 255: e.append(f"{w} transparency")
        sm.append(small(im))
    if e or len(sm) != n: return k, sid, e[:4]
    dup = sum(1 for i in range(n - 1) if ImageChops.difference(sm[i], sm[i + 1]).getbbox() is None)
    if dup: e.append(f"{dup} identical neighbouring frames")
    if any(ImageStat.Stat(s).mean[0] < 8 or ImageStat.Stat(s).mean[0] > 250 for s in sm): e.append("blank frame")
    if sum(ImageStat.Stat(ImageChops.difference(sm[0], sm[n // 2])).mean) < 1 or sum(ImageStat.Stat(ImageChops.difference(sm[n // 2], sm[-1])).mean) < 1: e.append("start/middle/end too similar")
    return k, sid, e


def main():
    ks = [video] if video else sorted(PLAN)
    items = [(k, s["id"], s["frames"], s["kind"]) for k in ks for s in PLAN[k]["sequences"]]
    if wave is not None: items = [i for i in items if WAVE.get(i[3]) == wave] if wave else []
    res = {}
    posters = {}
    if wave in (None, 0):
        for k in ks: posters[k] = check_poster(k)
    with ProcessPoolExecutor() as ex:
        for k, sid, e in ex.map(check_seq, [(a, b, c) for a, b, c, _ in items], chunksize=4): res[f"{k}/{sid}"] = e
    bad = [f"{k}/poster" for k, e in posters.items() if e] + [i for i, e in res.items() if e]
    if TODO:
        print("\n".join(bad)); sys.exit(1 if bad else 0)
    for k, e in posters.items():
        if e: print(f"FAIL {k}/poster: " + "; ".join(e))
    for i, e in res.items():
        if e: print(f"FAIL {i}: " + "; ".join(e))
    pn = sum(1 for e in posters.values() if not e); sn = sum(1 for e in res.values() if not e)
    fr = sum(s["frames"] for k in ks for s in PLAN[k]["sequences"] if not res.get(f"{k}/{s['id']}", ["x"]))
    tot = sum(s["frames"] for k in ks for s in PLAN[k]["sequences"])
    if wave is None and not video:
        print(f"{pn}/{len(posters)} posters, {sn}/{len(res)} sequences pass ({fr}/{tot} frames)")
        os.makedirs(f"{H}/anim3", exist_ok=True); json.dump({"fail": bad}, open(f"{H}/anim3/_status.json", "w"), indent=1)
    else: print(f"{pn}/{len(posters)} posters, {sn}/{len(res)} sequences pass")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
