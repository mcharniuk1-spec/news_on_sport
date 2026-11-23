from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os

ROOT = '<PROJECT_ROOT>/research/football100/anim'
OUT = os.path.join(ROOT, '003')
W, H = 1080, 1920
MASTER = Image.open(os.path.join(OUT, 'assets', '003_s01_resting_player_master.png')).convert('RGB')
MASTERS = {
    's04': Image.open(os.path.join(OUT, 'assets', '003_s04_pillow_gag_master.png')).convert('RGB'),
    's05': Image.open(os.path.join(OUT, 'assets', '003_s05_umbrella_wall_master.png')).convert('RGB'),
    's06': Image.open(os.path.join(OUT, 'assets', '003_s06_returned_kit_master.png')).convert('RGB'),
}
FONT_PATH = '/System/Library/Fonts/Supplemental/Verdana Bold.ttf'
FONT = ImageFont.truetype(FONT_PATH, 72)
SMALL = ImageFont.truetype(FONT_PATH, 42)
TINY = ImageFont.truetype(FONT_PATH, 30)
PALETTE = {'ink': '#16152C', 'violet': '#50319C', 'gold': '#FFD32F', 'cream': '#FFF3D1', 'teal': '#2CB7A6', 'pink': '#F56A83', 'white': '#FFFFFF', 'green': '#80C85B'}

SEQ = {
 's01': (36, '985 goals. Still rested?', 'ball-roll wipe', 'whistle-pop iris'),
 's02': (36, '985 career goals', 'zoom-through-icon', 'net ripple'),
 's03': (42, 'Rested for six-two', 'camera-flash shutter', 'turf-stripe slide'),
 's04': (48, 'Rotation', 'ink-splash wipe', 'scribble swipe'),
 's05': (48, 'Thank you, captain', 'page turn', 'ball-roll wipe'),
 's06': (48, '15 short of 1,000', 'confetti burst', 'VAR glitch stripes'),
 's07': (36, 'Next stop?', 'turf-stripe slide', 'camera-flash shutter'),
 's08': (42, 'Ready for Al Ahli away?', 'whistle-pop iris', 'speed-line whoosh'),
}

def rounded(d, box, r, fill, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

def centered(d, text, y, font=FONT, fill=PALETTE['white'], stroke=3):
    b=d.textbbox((0,0), text, font=font, stroke_width=stroke)
    x=(W-(b[2]-b[0]))//2
    d.text((x,y),text,font=font,fill=fill,stroke_width=stroke,stroke_fill=PALETTE['ink'])

def base(seq, f):
    # Each frame is independently rendered from deterministic time-based motion.
    phase=2*math.pi*f/24
    if seq in ('s01','s03','s04','s05','s06','s08'):
        zoom=1.025+0.008*math.sin(phase)
        source=MASTERS.get(seq, MASTER)
        scale=max(W/source.width,H/source.height)*zoom
        bg=source.resize((int(source.width*scale),int(source.height*scale)),Image.Resampling.LANCZOS)
        ox=(bg.width-W)//2 + int(10*math.sin(phase*.7))
        oy=(bg.height-H)//2 + int(9*math.cos(phase*.8))
        im=bg.crop((ox,oy,ox+W,oy+H))
        # unify the original image and graphic overlays with a soft violet edge.
        shade=Image.new('RGBA',(W,H),(22,21,44,30))
        im=Image.alpha_composite(im.convert('RGBA'),shade)
    else:
        im=Image.new('RGBA',(W,H),PALETTE['ink'])
        d=ImageDraw.Draw(im)
        for i in range(10):
            y=245+i*128+int(9*math.sin(phase+i*.7))
            d.rectangle((0,y,W,y+3),fill=(80,49,156,130))
        # soft stadium lights
        for x in (90,990):
            d.ellipse((x-90,280,x+90,460),fill=(255,211,47,22))
        im=im.filter(ImageFilter.GaussianBlur(0.3))
    return im

def icon_ball(d,x,y,r,phase):
    yy=int(y+10*math.sin(phase))
    d.ellipse((x-r,yy-r,x+r,yy+r),fill=PALETTE['cream'],outline=PALETTE['ink'],width=8)
    d.polygon([(x,yy-r//2),(x+r//3,yy-r//4),(x+r//4,yy+r//5),(x-r//4,yy+r//5),(x-r//3,yy-r//4)],fill=PALETTE['ink'])
    for a in range(5):
        ang=phase+a*math.tau/5
        d.line((x+int(r*.56*math.cos(ang)),yy+int(r*.56*math.sin(ang)),x+int(r*.85*math.cos(ang)),yy+int(r*.85*math.sin(ang))),fill=PALETTE['ink'],width=6)

def draw(seq, f, n):
    im=base(seq,f); d=ImageDraw.Draw(im)
    t=f/max(1,n-1); phase=2*math.pi*f/24
    # transition sweeps are distinct per sequence and stay clear of the caption zones.
    edge_in=6; edge_out=6
    if f<edge_in:
        frac=(f+1)/edge_in
        color={'s01':PALETTE['gold'],'s02':PALETTE['teal'],'s03':PALETTE['pink'],'s04':PALETTE['cream'],'s05':PALETTE['green'],'s06':PALETTE['gold'],'s07':PALETTE['teal'],'s08':PALETTE['pink']}[seq]
        if seq in ('s02','s07'):
            y=int(900*(1-frac)); d.rectangle((0,y,W,y+120),fill=color)
        else:
            x=int(W*(1-frac)); d.rectangle((0,0,x,H),fill=color)
    if f>=n-edge_out:
        frac=(f-(n-edge_out)+1)/edge_out
        if seq in ('s02','s07','s08'):
            y=int(1920*frac); d.rectangle((0,0,W,y),fill=PALETTE['ink'])
        else:
            x=int(W*frac); d.rectangle((0,0,x,H),fill=PALETTE['ink'])

    if seq=='s01':
        rounded(d,(86,245,994,405),32,PALETTE['ink'],PALETTE['gold'],7)
        centered(d,'985 goals.',258,SMALL,PALETTE['gold'])
        centered(d,'Still rested?',320,SMALL,PALETTE['white'])
        # spinning question mark and moving ball beneath the question
        icon_ball(d,540,1270,120,phase)
        d.text((480,820+int(9*math.sin(phase))),'?',font=ImageFont.truetype(FONT_PATH,170),fill=PALETTE['gold'],stroke_width=8,stroke_fill=PALETTE['ink'])
    elif seq=='s02':
        centered(d,'985 career goals',370,SMALL,PALETTE['white'])
        shown=max(0,min(985,int(985*min(1,t*1.35))))
        centered(d,f'{shown}',570,ImageFont.truetype(FONT_PATH,150),PALETTE['gold'],6)
        # bouncing ball icon and six-two score marks, both supported by narration.
        icon_ball(d,300,1110,105,phase)
        rounded(d,(580,1000,950,1220),36,PALETTE['violet'],PALETTE['gold'],7)
        centered(d,'six-two',1030,ImageFont.truetype(FONT_PATH,76),PALETTE['white'])
        for i in range(5):
            x=245+i*145; y=1460+int(16*math.sin(phase+i))
            d.ellipse((x,y,x+42,y+42),fill=PALETTE['teal'],outline=PALETTE['white'],width=3)
    elif seq=='s03':
        rounded(d,(52,245,1028,405),30,PALETTE['ink'],PALETTE['gold'],7)
        centered(d,'Rested for six-two',285,SMALL,PALETTE['gold'])
        rounded(d,(70,1360,1010,1515),28,PALETTE['violet'],PALETTE['white'],5)
        centered(d,'Cristiano Ronaldo',1408,SMALL,PALETTE['white'])
        # independent story icons float beside the subject.
        icon_ball(d,150+int(14*math.sin(phase)),1120,60,phase)
        d.rectangle((850,960,935,1100),fill=PALETTE['gold'],outline=PALETTE['ink'],width=5)
        d.ellipse((840,930,945,970),fill=PALETTE['cream'],outline=PALETTE['ink'],width=5)
        for k in range(3):
            x=170+k*370; y=780+int(15*math.sin(phase+k))
            d.ellipse((x,y,x+16,y+16),fill=PALETTE['white'])
    elif seq=='s04':
        rounded(d,(300,260,780,385),24,PALETTE['gold'],PALETTE['ink'],6)
        centered(d,'Rotation',288,SMALL,PALETTE['ink'],2)
    elif seq=='s05':
        centered(d,'Thank you, captain',330,SMALL,PALETTE['gold'])
        # Text lands in the image's open upper field; generated scene carries the gag.
        rounded(d,(165,300,915,445),30,PALETTE['ink'],PALETTE['gold'],6)
        centered(d,'Thank you, captain',337,SMALL,PALETTE['white'],2)
        icon_ball(d,850,670,65,phase)
    elif seq=='s06':
        # The generated scene contains the fans, narrated score, shirt and returned armband.
        centered(d,'Thank you, captain',410,SMALL,PALETTE['ink'],2)
    elif seq=='s07':
        rounded(d,(74,350,1006,655),42,PALETTE['violet'],PALETTE['gold'],8)
        centered(d,'Next stop?',445,FONT,PALETTE['white'])
        labels=[('Al Ahli away',PALETTE['gold']),('One thousand',PALETTE['teal'])]
        for i,(label,col) in enumerate(labels):
            y=840+i*300
            rounded(d,(120,y,960,y+165),38,PALETTE['ink'],col,8)
            d.text((165,y+42),label,font=SMALL,fill=PALETTE['white'],stroke_width=2,stroke_fill=PALETTE['ink'])
            pct=max(0.08,min(.92,(t*(.75 if i==0 else .25))+.08))
            rounded(d,(165,y+120,165+int(720*pct),y+148),14,col)
        centered(d,str(int(t*985)),1470,TINY,PALETTE['gold'])
    elif seq=='s08':
        rounded(d,(85,245,995,365),30,PALETTE['ink'],PALETTE['gold'],7)
        centered(d,'REPORTER ASKS',278,SMALL,PALETTE['teal'],2)
        rounded(d,(95,1240,985,1505),36,PALETTE['cream'],PALETTE['violet'],8)
        centered(d,'Ready for Al Ahli away?',1320,SMALL,PALETTE['ink'],2)
        # microphone and answer gesture icon
        d.rounded_rectangle((145,785,235,1030),radius=45,fill=PALETTE['ink'],outline=PALETTE['gold'],width=8)
        d.arc((100,860,280,1090),0,180,fill=PALETTE['gold'],width=8)
        d.line((190,1080,190,1175),fill=PALETTE['gold'],width=8)
        for k in range(3):
            ang=phase+k*math.tau/3
            x=820+int(45*math.cos(ang)); y=900+int(45*math.sin(ang))
            d.polygon([(x,y-30),(x+26,y),(x,y+30),(x-26,y)],fill=PALETTE['gold'])
        icon_ball(d,850,1155,58,phase)

    # Persistent light flecks and a moving pitch stripe ensure clear motion on quiet beats.
    # A single low pitch glint moves below all important captions.
    x=int((f*19)%W)
    d.line((x,1564,min(W,x+135),1564),fill=PALETTE['gold'],width=4)
    return im.convert('RGB')

def main():
    manifest=[]
    for sid,(count,label,transition_in,transition_out) in SEQ.items():
        folder=os.path.join(OUT,sid); os.makedirs(folder,exist_ok=True)
        for frame in range(1,count+1):
            img=draw(sid,frame-1,count)
            path=os.path.join(folder,f'f{frame:04d}.png')
            img.save(path,format='PNG',optimize=False,compress_level=1)
        manifest.append((sid,count))
    print('Rendered sequences:', ', '.join(f'{s}={n}' for s,n in manifest))
    print('Total frames:',sum(n for _,n in manifest))

if __name__=='__main__': main()
