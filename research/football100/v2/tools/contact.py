#!/usr/bin/env python3
"""contact.py NNN -> H/v2/review/NNN/contact.png : one row per sequence (H/v2/seq/NNN/*.mp4), 6 evenly spaced frames, 180x320 each, labelled."""
import os, subprocess, sys, tempfile, glob, json
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.abspath(os.path.join(HERE, '..'))
CW, CH, N = 180, 320, 6


def nframes(mp4):
    r = subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-select_streams', 'v:0', '-show_entries', 'stream=nb_read_packets', '-of', 'csv=p=0', mp4], capture_output=True, text=True)
    return int(r.stdout.strip() or 0)


def frames(mp4, idx, tmp):
    sel = '+'.join('eq(n\\,%d)' % i for i in idx)
    pat = os.path.join(tmp, 'f_%03d.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', mp4, '-vf', "select='%s',scale=%d:%d" % (sel, CW, CH), '-vsync', '0', pat], check=True)
    return [Image.open(p).convert('RGB') for p in sorted(glob.glob(os.path.join(tmp, 'f_*.png')))]


def main():
    if len(sys.argv) < 2:
        print('usage: contact.py NNN'); return 2
    nno = '%03d' % int(sys.argv[1])
    files = sorted(glob.glob(os.path.join(V2, 'seq', nno, 's*.mp4')))
    if not files:
        print('no mp4 in', os.path.join(V2, 'seq', nno)); return 1
    try:
        font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 15)
    except Exception:
        font = ImageFont.load_default()
    label_w = 70
    W = label_w + N * CW + (N + 1) * 4
    Hh = len(files) * (CH + 4) + 4
    sheet = Image.new('RGB', (W, Hh), (24, 24, 32))
    d = ImageDraw.Draw(sheet)
    for r, f in enumerate(files):
        n = nframes(f)
        idx = [round(i * (n - 1) / (N - 1)) for i in range(N)]
        with tempfile.TemporaryDirectory() as tmp:
            ims = frames(f, idx, tmp)
        y = 4 + r * (CH + 4)
        d.text((6, y + 4), os.path.basename(f)[:-4], fill=(255, 255, 255), font=font)
        d.text((6, y + 24), '%d fr' % n, fill=(200, 200, 120), font=font)
        for c, im in enumerate(ims):
            x = label_w + 4 + c * (CW + 4)
            sheet.paste(im, (x, y))
            d.text((x + 3, y + 2), str(idx[c]), fill=(255, 255, 0), font=font)
    out = os.path.join(V2, 'review', nno)
    os.makedirs(out, exist_ok=True)
    p = os.path.join(out, 'contact.png')
    sheet.save(p)
    print(p)
    return 0


if __name__ == '__main__':
    sys.exit(main())
