"""Caption + card sprites (PIL) for the ffmpeg assembler (this ffmpeg build has no libass/drawtext).
Captions: <=5 words, <=2 lines, karaoke highlight of the spoken word, bold uppercase with black outline, lower-middle zone (above the bottom 20 % UI band).
Cards: the per-line headline (script `card`) in the old Impact/yellow style, shown only where no interlude covers the screen."""
import os, re
from PIL import Image, ImageDraw, ImageFont, ImageFilter
FONT = "/System/Library/Fonts/Supplemental/Impact.ttf"
W = 1080; CAP_H = 300; CAP_Y = 1475     # strip y=1475..1775, text block centred near y=1625 (bottom band the interludes keep clear)
HI = (255, 194, 71, 255); WH = (255, 255, 255, 255); BK = (0, 0, 0, 255)
_fc = {}


def font(sz):
    if sz not in _fc: _fc[sz] = ImageFont.truetype(FONT, sz)
    return _fc[sz]


def tw(txt, f, stroke=0):
    b = f.getbbox(txt, stroke_width=stroke); return b[2] - b[0]


def chunks(words):
    """words: [{w,line,s,e}] -> list of chunks (list of word dicts)."""
    out = []; cur = []
    def flush():
        nonlocal cur
        if cur: out.append(cur); cur = []
    for k, w in enumerate(words):
        if cur and (w["line"] != cur[-1]["line"]): flush()
        cur.append(w)
        txt = " ".join(x["w"] for x in cur)
        end_sent = bool(re.search(r"[.?!]['\")]*$", w["w"]))
        end_comma = bool(re.search(r"[,;:]['\")]*$", w["w"]))
        nxt = words[k + 1] if k + 1 < len(words) else None
        if end_sent or len(cur) >= 5 or len(txt) >= 28 or (end_comma and len(cur) >= 3):
            flush()
        elif nxt and nxt["line"] == w["line"]:
            # avoid leaving a lone short word for the next chunk when only one word would remain after a long run
            rest = [x for x in words[k + 1:] if x["line"] == w["line"]]
            nsent = 0
            for x in rest:
                nsent += 1
                if re.search(r"[.?!]['\")]*$", x["w"]): break
            if len(cur) >= 3 and nsent == 1 and len(cur) + 1 > 5: flush()
    flush()
    # merge a lone trailing single-word chunk that is not sentence final into the previous chunk if it fits
    return out


def layout(ws, size=76):
    """Return font, lines (list of list of word indices) for a chunk, text uppercase without trailing comma."""
    txt = [re.sub(r"[,;:]+$", "", x["w"]).upper() for x in ws]
    while True:
        f = font(size); sp = tw(" ", f) + 2
        whole = sum(tw(t, f, 7) for t in txt) + sp * (len(txt) - 1)
        if whole <= 900 or len(txt) == 1:
            lines = [list(range(len(txt)))]
        else:
            best = None
            for cut in range(1, len(txt)):
                a = sum(tw(t, f, 7) for t in txt[:cut]) + sp * (cut - 1); b = sum(tw(t, f, 7) for t in txt[cut:]) + sp * (len(txt) - cut - 1)
                m = max(a, b)
                if best is None or m < best[0]: best = (m, cut)
            lines = [list(range(best[1])), list(range(best[1], len(txt)))]
        widest = max(sum(tw(txt[i], f, 7) for i in ln) + sp * (len(ln) - 1) for ln in lines)
        if widest <= 960 or size <= 48: return f, lines, txt, sp
        size -= 4


def sprite(ws, active, path):
    f, lines, txt, sp = layout(ws)
    im = Image.new("RGBA", (W, CAP_H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lh = int(f.size * 1.02); total_h = lh * len(lines); y0 = (CAP_H - total_h) // 2
    sh = Image.new("RGBA", (W, CAP_H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    pos = []
    for li, ln in enumerate(lines):
        wid = sum(tw(txt[i], f, 7) for i in ln) + sp * (len(ln) - 1); x = (W - wid) // 2; y = y0 + li * lh
        for i in ln:
            pos.append((i, x, y)); x += tw(txt[i], f, 7) + sp
    for i, x, y in pos: sd.text((x, y + 7), txt[i], font=f, fill=(0, 0, 0, 150), stroke_width=7, stroke_fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(5)); im.alpha_composite(sh)
    for i, x, y in pos:
        d.text((x, y), txt[i], font=f, fill=HI if i == active else WH, stroke_width=7, stroke_fill=BK)
    im.save(path)


def blank(path):
    Image.new("RGBA", (W, CAP_H), (0, 0, 0, 0)).save(path)


def caption_track(words, VO, cap_end, wdir):
    """Returns (list_file, n_sprites). Concat list covers [0, cap_end]. words are voice-relative."""
    os.makedirs(wdir, exist_ok=True); blank(f"{wdir}/blank.png")
    segs = []   # (path, t0, t1) in timeline seconds
    ch = chunks(words)
    for ci, ws in enumerate(ch):
        t_start = ws[0]["s"] + VO - 0.04
        nxt = ch[ci + 1][0]["s"] + VO - 0.04 if ci + 1 < len(ch) else None
        t_end = ws[-1]["e"] + VO + 0.14
        if nxt is not None: t_end = min(t_end, nxt) if nxt - t_end < 0.35 else t_end
        if nxt is not None and nxt - (ws[-1]["e"] + VO) < 0.35: t_end = nxt
        for k, w in enumerate(ws):
            a = t_start if k == 0 else w["s"] + VO - 0.02
            b = t_end if k == len(ws) - 1 else ws[k + 1]["s"] + VO - 0.02
            if b - a < 0.04: continue
            p = f"{wdir}/c{ci:03d}_{k}.png"
            if not os.path.exists(p): sprite(ws, k, p)
            segs.append((p, a, b))
    # build contiguous timeline 0..cap_end
    lst = []; t = 0.0
    for p, a, b in segs:
        a = max(a, t); b = min(b, cap_end)
        if b <= a: continue
        if a > t + 1e-3: lst.append((f"{wdir}/blank.png", a - t))
        lst.append((p, b - a)); t = b
    if cap_end > t: lst.append((f"{wdir}/blank.png", cap_end - t))
    lf = f"{wdir}/caps.txt"
    with open(lf, "w") as fh:
        for p, d in lst: fh.write(f"file '{p}'\nduration {d:.4f}\n")
        fh.write(f"file '{lst[-1][0]}'\n")
    return lf, len(segs)


def card_sprite(text, path):
    f = font(112); txt = text.upper()
    parts = [txt]
    if tw(txt, f, 16) > 960:
        ws = txt.split(); best = None
        for cut in range(1, len(ws)):
            a = " ".join(ws[:cut]); b = " ".join(ws[cut:]); m = max(tw(a, f, 16), tw(b, f, 16))
            if best is None or m < best[0]: best = (m, a, b)
        parts = [best[1], best[2]] if best else [txt]
        while max(tw(p_, f, 16) for p_ in parts) > 980 and f.size > 60: f = font(f.size - 6)
    H_ = 340; im = Image.new("RGBA", (W, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    lh = int(f.size * 1.08); y0 = (H_ - lh * len(parts)) // 2
    sh = Image.new("RGBA", (W, H_), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    for i, p_ in enumerate(parts):
        b = f.getbbox(p_, stroke_width=16); x = (W - (b[2] - b[0])) // 2 - b[0]; y = y0 + i * lh
        sd.text((x, y + 8), p_, font=f, fill=(0, 0, 0, 130), stroke_width=16, stroke_fill=(0, 0, 0, 130))
    sh = sh.filter(ImageFilter.GaussianBlur(7)); im.alpha_composite(sh)
    for i, p_ in enumerate(parts):
        b = f.getbbox(p_, stroke_width=16); x = (W - (b[2] - b[0])) // 2 - b[0]; y = y0 + i * lh
        d.text((x, y), p_, font=f, fill=(255, 194, 71, 255), stroke_width=16, stroke_fill=(13, 27, 50, 255))
    im.save(path)
