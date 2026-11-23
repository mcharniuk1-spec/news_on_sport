#!/usr/bin/env python3
"""Comic-style cover: sunburst + halftone, comic-filtered hero frame in a tilted panel, hook headline, speech bubble with a joke line,
emoji reactions and a burst word, brand bar. Usage: cover.py <no>..."""
import glob, json, math, os, random, re, subprocess, sys, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance, ImageChops
H = os.path.dirname(os.path.abspath(__file__)); IMP = "/System/Library/Fonts/Supplemental/Impact.ttf"
EMO = "/System/Library/Fonts/Apple Color Emoji.ttc"
AMBER, RED, NAVY, WHITE = (255, 194, 71), (232, 52, 52), (14, 18, 44), (255, 255, 255)
BURSTS = ["WAIT, WHAT?!", "NO WAY!", "SERIOUSLY?!", "OH DEAR...", "BOOM!", "CHEEKY!", "HOW?!", "OUCH!"]
EMOJI = [["🤯", "😱", "😂", "🔥"], ["😳", "🤨", "😅", "💥"], ["🙈", "😬", "😂", "⚡"], ["🤔", "😮", "🤣", "🔥"]]
def F(s): return ImageFont.truetype(IMP, int(s))
def hook(j):
    t = (j.get("title") or "").strip()
    if not t or len(t.split()) > 11: t = j["lines"][0]["vo"].strip()
    return " ".join(t.split()[:9]).rstrip(".,;:")
def joke(j):
    for l in j["lines"][1:-1]:
        s = re.split(r"(?<=[.!?])\s", l["vo"].strip())[0].strip()
        if 3 <= len(s.split()) <= 11: return s
    s = j["lines"][min(1, len(j["lines"]) - 1)]["vo"].split(".")[0]; return " ".join(s.split()[:9])
def wrap(d, txt, font, w):
    out, cur = [], ""
    for wd in txt.split():
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= w: cur = t
        else: out.append(cur); cur = wd
    return out + [cur]
def comic(im):
    """v2 (readability): lift shadows, flat colour regions via 16-colour quantize (no posterize noise), few strong outlines only."""
    im = ImageOps.autocontrast(im, cutoff=2).point(lambda v: int(255 * (v / 255) ** 0.8))  # open up dark tones
    flat = im.filter(ImageFilter.MedianFilter(7)).filter(ImageFilter.SMOOTH_MORE)
    flat = ImageEnhance.Color(flat).enhance(1.45); flat = ImageEnhance.Contrast(flat).enhance(1.15)
    flat = flat.quantize(colors=16, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGB")
    g = im.convert("L").filter(ImageFilter.GaussianBlur(2.2)).filter(ImageFilter.FIND_EDGES)
    e = g.point(lambda v: 0 if v > 26 else 255).filter(ImageFilter.MedianFilter(3))  # only strong contours
    return ImageChops.multiply(flat, e.convert("RGB"))
def emoji(ch, size):
    t = Image.new("RGBA", (200, 200), (0, 0, 0, 0)); ImageDraw.Draw(t).text((0, 0), ch, font=ImageFont.truetype(EMO, 160), embedded_color=True)
    return t.resize((size, size))
def burst(d, cx, cy, r, fill, n=14, ang=0):
    pts = [(cx + (r if i % 2 == 0 else r * 0.68) * math.cos(ang + i * math.pi / n), cy + (r if i % 2 == 0 else r * 0.68) * math.sin(ang + i * math.pi / n)) for i in range(2 * n)]
    d.polygon(pts, fill=fill, outline=(0, 0, 0)); d.line(pts + [pts[0]], fill=(0, 0, 0), width=7)
def make(no):
    v = glob.glob(f"{H}/deliver/{no:03d}_*_small.mp4")
    if not v: return None
    j = json.load(open(f"{H}/scripts/{no:03d}.json")); out = f"{H}/deliver/{no:03d}_cover.png"; rnd = random.Random(no)
    fr = f"/tmp/cv_{no}.png"; best = -1
    for c in sorted(glob.glob(f"{H}/footage/{no:03d}/*.mp4"))[:5]:  # clean footage (no captions); keep the most detailed frame
        for t in ("1.0", "2.2"):
            p = f"/tmp/cv_{no}_t.png"; r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", c, "-frames:v", "1", p])
            if r.returncode or not os.path.exists(p): continue
            im0 = Image.open(p).convert("L").resize((270, 480)); sc = sum(ImageChops.difference(im0, im0.filter(ImageFilter.GaussianBlur(3))).tobytes())
            if sc > best: best = sc; os.replace(p, fr)
    if best < 0: subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "7", "-i", v[0], "-frames:v", "1", fr], check=True)
    hp = f"{H}/codex/hero/{no:03d}.png"  # optional Codex-drawn hero character: replaces the footage frame
    if os.path.exists(hp): fr = hp
    W, Hh = 1080, 1920; bg = Image.new("RGB", (W, Hh), NAVY); d = ImageDraw.Draw(bg)
    n = 24; off = rnd.random()
    for i in range(n):  # sunburst
        a0, a1 = (i + off) * 2 * math.pi / n, (i + off + 0.5) * 2 * math.pi / n
        d.polygon([(540, 900), (540 + 2600 * math.cos(a0), 900 + 2600 * math.sin(a0)), (540 + 2600 * math.cos(a1), 900 + 2600 * math.sin(a1))], fill=(RED if no % 2 else (255, 140, 40)))
    ht = Image.new("L", (W, Hh), 0); hd = ImageDraw.Draw(ht)  # halftone dots, fading to the top
    for y in range(0, Hh, 26):
        for x in range((y // 26 % 2) * 13, W, 26): r = 9 * (y / Hh) ** 1.3; hd.ellipse([x - r, y - r, x + r, y + r], fill=255)
    bg.paste(Image.new("RGB", (W, Hh), (0, 0, 0)), mask=ht.point(lambda v: v // 4))
    # hero panel
    hero = Image.open(fr).convert("RGB"); hw, hh = hero.size; s = 1000 / hh * 1.0
    hero = hero.crop((max(0, hw // 2 - int(hh * 0.56 / 1.0 * 0.5)), 0, min(hw, hw // 2 + int(hh * 0.56 * 0.5)), hh)) if hw > hh else hero
    hero = ImageOps.fit(hero, (940, 960), centering=(0.5, 0.4)); hero = hero.crop((80, 80, 860, 880)).resize((940, 960)).filter(ImageFilter.MedianFilter(5)); hero = hero if os.path.exists(hp) else comic(hero)
    panel = Image.new("RGBA", (1000, 1020), (0, 0, 0, 0)); pd = ImageDraw.Draw(panel)
    pd.rectangle([0, 0, 999, 1019], fill=(255, 255, 255)); panel.paste(hero, (30, 30)); pd.rectangle([0, 0, 999, 1019], outline=(0, 0, 0), width=14)
    pd.rectangle([30, 30, 969, 989], outline=(0, 0, 0), width=8)
    panel = panel.rotate(rnd.choice([-4, 4]), expand=True, resample=Image.BICUBIC)
    sh = Image.new("RGBA", panel.size, (0, 0, 0, 0)); sh.paste((0, 0, 0, 170), mask=panel.split()[3])
    bg = bg.convert("RGBA"); bg.alpha_composite(sh, (50 + 18, 430 + 18)); bg.alpha_composite(panel, (50, 430)); d = ImageDraw.Draw(bg)
    # headline banner
    txt = hook(j).upper(); size = 120
    while True:
        f = F(size); L = wrap(d, txt, f, 940)
        if len(L) <= 3 or size < 70: break
        size -= 6
    bh = len(L) * size * 1.05 + 50; ban = Image.new("RGBA", (1080, int(bh)), (0, 0, 0, 0)); bd = ImageDraw.Draw(ban)
    bd.polygon([(10, 12), (1070, 0), (1060, bh - 4), (0, bh)], fill=(250, 220, 40), outline=(0, 0, 0)); bd.line([(10, 12), (1070, 0), (1060, bh - 4), (0, bh), (10, 12)], fill=(0, 0, 0), width=10)
    for i, l in enumerate(L): bd.text((540, 25 + size * 1.05 * (i + 0.5)), l, font=f, fill=(20, 20, 20), anchor="mm")
    ban = ban.rotate(-2, expand=True, resample=Image.BICUBIC); bg.alpha_composite(ban, (0, 40)); d = ImageDraw.Draw(bg)
    # burst word (top-left over panel corner)
    bw = BURSTS[no % len(BURSTS)]; bl = Image.new("RGBA", (460, 460), (0, 0, 0, 0)); bd = ImageDraw.Draw(bl)
    burst(bd, 230, 230, 215, (255, 255, 255, 255), 12, 0.2); bd.text((230, 230), "\n".join(bw.split(" ")) if " " in bw and len(bw) > 8 else bw, font=F(78), fill=RED, anchor="mm", align="center", stroke_width=3, stroke_fill=(0, 0, 0))
    bg.alpha_composite(bl.rotate(12, resample=Image.BICUBIC), (600, 360 + int(bh) - 150))
    # speech bubble with joke
    jk = joke(j).upper(); f = F(58); L = wrap(d, jk, f, 640); bh2 = len(L) * 66 + 60; bx, by = 70, 1330
    bub = Image.new("RGBA", (760, bh2 + 70), (0, 0, 0, 0)); bd = ImageDraw.Draw(bub)
    bd.rounded_rectangle([0, 0, 740, bh2], radius=50, fill=WHITE, outline=(0, 0, 0), width=8)
    bd.polygon([(560, bh2 - 4), (640, bh2 + 70), (470, bh2 - 4)], fill=WHITE, outline=(0, 0, 0)); bd.line([(560, bh2 - 4), (640, bh2 + 70), (470, bh2 - 4)], fill=(0, 0, 0), width=8)
    bd.rectangle([478, bh2 - 12, 552, bh2 - 1], fill=WHITE)
    for i, l in enumerate(L): bd.text((370, 40 + 66 * i + 33), l, font=f, fill=(20, 20, 20), anchor="mm")
    bg.alpha_composite(bub, (bx, by - bh2 + 100)); d = ImageDraw.Draw(bg)
    # emoji reactions
    em = EMOJI[no % 4]
    for ch, (x, y, sz, rot) in zip(em, [(30, 520, 190, -15), (850, 1010, 200, 14), (880, 1480, 170, -10), (40, 1230, 160, 12)]):
        bg.alpha_composite(emoji(ch, sz).rotate(rot, expand=True, resample=Image.BICUBIC), (x, y))
    d.rectangle([0, 1720, W, Hh], fill=AMBER); d.line([(0, 1720), (W, 1720)], fill=(0, 0, 0), width=8)
    d.text((540, 1795), "ABOUTFOOTBALL.UK", font=F(92), fill=(15, 15, 25), anchor="mm")
    d.text((540, 1880), "BETTING TIPS · NEWS · PREDICTIONS · 18+", font=F(34), fill=(15, 15, 25), anchor="mm")
    bg.convert("RGB").save(out, quality=92); return out
if __name__ == "__main__":
    for n in sys.argv[1:]: print(make(int(n)))
