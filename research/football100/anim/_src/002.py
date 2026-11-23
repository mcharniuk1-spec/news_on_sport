"""Wave 1 art for video 002."""
import json, math, sys
from pathlib import Path
from PIL import Image
from toolkit import Canvas, Rig, INK, WHITE, icon, keys, back, elastic, particles, transition, lower_third, ticker

ROOT=Path(__file__).resolve().parents[2]
PINK,PLUM,DARK,CORAL,YELLOW,MINT,SKIN=('#dd9bb7','#8f557a','#322c52','#f37d72','#ffe080','#9bd3b2','#f6b481')
SCOUT=Rig(MINT,SKIN,'#533b56')
PLAYER=Rig(CORAL,SKIN,'#462d4b')
CUTS={'s01':('ball-roll','scribble-swipe'),'s02':('camera-flash','turf-slide'),'s03':('whistle-pop','page-turn')}

def room():
    c=Canvas(PINK)
    c.box((0,550,540,755),PLUM,0,0)
    c.shape([(60,621),(475,605),(534,724),(0,739)],DARK,0)
    c.box((51,218,191,385),PLUM,26,4)
    c.box((63,229,179,374),MINT,19,3)
    c.line([(120,232),(120,373)],DARK,5)
    c.line([(65,298),(178,298)],DARK,5)
    c.box((364,228,490,325),PLUM,33,0)
    c.line([(431,303),(431,551)],DARK,6)
    c.shape([(405,247),(455,247),(481,300),(384,300)],YELLOW,4)
    return c

def cassette(c,x,y,w,f):
    h=w*.58
    c.box((x-w/2,y-h/2,x+w/2,y+h/2),DARK,max(8,round(w*.065)),5)
    c.box((x-w*.36,y-h*.20,x+w*.36,y+h*.17),WHITE,11,3)
    for sign in (-1,1):
        cx=x+sign*w*.23
        c.oval(cx,y,w*.088,w*.088,PINK,4)
        for k in range(3):
            a=f*.27+k*math.tau/3
            c.line([(cx,y),(cx+math.cos(a)*w*.065,y+math.sin(a)*w*.065)],DARK,3)
    c.line([(x-w*.30,y+h*.33),(x+w*.30,y+h*.33)],PLUM,5)

def hook(f,n):
    c=room()
    x=217+keys(f,[(1,-28),(6,3),(10,0),(36,0)],back)
    SCOUT.draw(c,x,733,421,f,gesture=.40+.23*math.sin(f*.18))
    y=545+14*math.sin(f*.26)
    c.oval(390,689,101,16,DARK,0)
    cassette(c,383,y,219,f)
    particles(c,f,386,550)
    if f>=4:
        y=144+keys(f,[(4,-15),(6,0),(n,0)])
        c.box((27,y,513,y+145),DARK,25,5)
        c.text(270,y+44,['Can VHS sign','a striker?'],50)
    return c

def comic(f,n):
    c=room()
    press=keys(f,[(1,0),(12,0),(18,1),(24,.88),(31,1),(36,.20),(48,.20)],elastic)
    c.oval(167,708,122,19,DARK,0)
    c.box((24,404,279,694),PLUM,57,5)
    c.box((19,580,283,705),CORAL,32,5)
    c.box((18,531,81,688),CORAL,22,4)
    c.box((227,531,292,688),CORAL,22,4)
    SCOUT.draw(c,144+39*press,684,395,f,gesture=.67 if f>=36 else .12,sit=1)
    c.box((320,493,505,696),DARK,27,5)
    c.box((335,511,490,650),MINT,19,4)
    c.oval(479,674,9,9,YELLOW,3)
    cassette(c,416,436,165,f)
    if f>=13:
        for j in range(3):
            a=math.sin(f*.46+j)
            PLAYER.draw(c,366+j*46,629+3*a,75,f+j*5,gesture=.35+.44*a)
    else:c.line([(352,580),(474,580)],WHITE,4)
    if 13<=f<=33:
        x=222+94*press
        c.line([(202,651),(x,664),(x+18,670)],INK,29)
        c.line([(202,651),(x,664),(x+18,670)],PLUM,22)
        c.oval(x+21,670,20,11,WHITE)
        if f<=31:particles(c,f,320,660)
    if f>=36:
        y=keys(f,[(36,361),(40,312),(43,319),(48,319)],back)
        c.box((91,y-105,449,y+12),YELLOW,19,4)
        c.text(270,y-72,['Be kind,','rewind'],43,INK,0)
    return c

def news(f,n):
    c=room()
    PLAYER.draw(c,268,573,416,f,gesture=.15+.12*math.sin(f*.30))
    cassette(c,416,464+8*math.sin(f*.27),180,f)
    icon(c,'clock',85,416+6*math.cos(f*.32),42,f,YELLOW)
    icon(c,'ball',445,337+6*math.sin(f*.30),29,f)
    if f>=4:
        lower_third(c,['Andriy Shevchenko','No scouts there'])
        ticker(c,'No scouts there',f)
    return c

def main(seq,only):
    plan=json.loads((ROOT/'codex/v2/plan.json').read_text())
    spec=next(s for s in plan['002']['sequences'] if s['id']==seq)
    n=spec['frames']
    with Image.open(ROOT/'anim/_sheets/FLAT-POP.png') as sheet:sheet.load()
    folder=ROOT/'anim/002'/seq
    folder.mkdir(exist_ok=True)
    for f in only or range(1,n+1):
        c={'s01':hook,'s02':comic,'s03':news}[seq](f,n)
        transition(c,f,n,*CUTS[seq],DARK,PLUM)
        c.finish().save(folder/f'f{f:04}.png',compress_level=2)

if __name__=='__main__':main(sys.argv[1],list(map(int,sys.argv[2:])))
