"""Wave 1 art for video 001. Usage: python3 anim/_src/001.py s01."""
import json, math, sys
from pathlib import Path
from toolkit import Canvas, Rig, INK, WHITE, icon, particles, transition, lower_third, ticker, keys, back, elastic

ROOT=Path(__file__).resolve().parents[2]
PAL=('#a8cbdc','#7495ac','#363454','#7953a0','#ec7b81','#ffd173','#6cbdab')
SKY,MIST,DARK,PURPLE,PINK,YELLOW,TEAL=PAL
PLAYER=Rig(PURPLE,YELLOW,'#493044')
REPORTER=Rig(TEAL,YELLOW,'#503a46')
CUTS={'s01':('turf-slide','whistle-pop'),'s03':('ink-splash','net-ripple'),'s04':('page-turn','var-glitch')}

def stage(f,kind):
    c=Canvas(SKY)
    if kind=='studio':
        c.box((24,138,516,550),MIST,48)
        c.box((49,156,491,519),'#a6bdc9',38)
        for x in (93,185,276,366,455):
            c.line([(x,165),(x,493)],MIST,5)
    else:
        for x in (65,475):
            c.line([(x,163),(x,472)],DARK,5)
            c.box((x-35,135,x+35,180),DARK,9)
            for i in range(3):c.oval(x-20+i*20,157,6,6,WHITE,0)
        c.shape([(0,392),(180,349),(360,349),(540,392),(540,531),(0,531)],MIST,0)
        for row in range(4):
            for i in range(21):
                c.oval(9+i*26+(row%2)*7,402+row*27,12,10,[DARK,PURPLE,TEAL][(i+row)%3],0)
    c.box((0,517,540,752),TEAL if kind!='studio' else MIST,0,0)
    for i in range(4):
        y=555+i*61
        c.shape([(0,y),(540,y-22),(540,y+2),(0,y+23)],MIST if kind!='studio' else SKY,0)
    return c

def hook(f,n):
    c=stage(f,'pitch')
    h=keys(f,[(1,395),(6,430),(12,412),(24,421),(36,415)],back)
    PLAYER.draw(c,266,733,h,f,gesture=.28+.38*math.sin(f*.14))
    c.oval(426,604,55,14,MIST,0)
    icon(c,'ball',424,532+10*math.sin(f*.37),46,f)
    particles(c,f,420,525)
    if f>=4:
        y=141+keys(f,[(4,-15),(6,0),(n,0)])
        c.box((26,y,514,y+142),DARK,26,4)
        c.text(270,y+44,['Does Ukraine','belong here?'],49)
    return c

def armchair(c,y,compress):
    c.oval(306,y+4,143,18,DARK,0)
    c.box((181,y-194+compress,412,y-15),PINK,42,5)
    c.box((174,y-93,419,y-7),'#bd5b82',24,5)
    c.box((158,y-119,219,y-17),PINK,23,5)
    c.box((375,y-119,435,y-17),PINK,23,5)
    c.line([(198,y-8),(190,y+11)],INK,9)
    c.line([(396,y-8),(406,y+11)],INK,9)
    for x in (328,373):
        c.oval(x,y+46,21,9,PURPLE)
        c.line([(x-7,y+44),(x+8,y+44)],WHITE,3)

def comic(f,n):
    c=stage(f,'studio')
    settle=keys(f,[(1,0),(12,0),(18,1),(24,.88),(30,1),(48,1)],elastic)
    bounce=keys(f,[(1,0),(16,0),(20,24),(25,4),(30,11),(35,5),(48,5)])
    armchair(c,684,bounce)
    PLAYER.draw(c,449,685,303,f,gesture=.30 if f<32 else .10)
    rx=136+settle*132
    ry=684-bounce+(1-settle)*11
    hand=REPORTER.draw(c,rx,ry,397-35*settle,f,gesture=.38 if f<=12 else .09,sit=settle)
    if f<17:
        c.line([hand,(hand[0]+22,hand[1]-38)],DARK,9)
        c.oval(hand[0]+23,hand[1]-41,11,15,DARK)
    if 14<=f<=31:
        for j in range(3):
            off=(f*3+j*15)%39
            c.line([(429+off,605-j*16),(441+off,599-j*16)],WHITE,3)
    c.box((174,152,366,223),DARK,17,4)
    c.text(270,187,['League B'],43)
    if f>=36:
        y=keys(f,[(36,706),(40,750),(42,744),(48,744)],back)
        c.line([(261,689),(263,y-17)],INK,4)
        c.shape([(220,y-18),(300,y-18),(324,y),(302,y+21),(220,y+21)],YELLOW,4)
        c.oval(302,y,6,6,DARK,0)
    else:
        particles(c,f,315,511)
    return c

def news(f,n):
    c=stage(f,'pitch')
    PLAYER.draw(c,271,573,409,f,gesture=.17+.10*math.sin(f*.3))
    for j,k in enumerate(('ball','net','clock')):
        x=(90,449,448)[j]; y=(449,471,344)[j]
        icon(c,k,x,y+7*math.sin(f*.31+j),38,f)
    if f>=4:
        lower_third(c,['Andriy Shevchenko','73% ball, lost 0-3'])
        ticker(c,'73% ball, lost 0-3',f)
    return c

def main(seq,only):
    plan=json.loads((ROOT/'codex/v2/plan.json').read_text())
    spec=next(s for s in plan['001']['sequences'] if s['id']==seq)
    n=spec['frames']
    with __import__('PIL.Image',fromlist=['open']).open(ROOT/'anim/_sheets/SITCOM-YELLOW.png') as sheet:sheet.load()
    folder=ROOT/'anim/001'/seq
    folder.mkdir(exist_ok=True)
    for f in only or range(1,n+1):
        c={'s01':hook,'s03':comic,'s04':news}[seq](f,n)
        transition(c,f,n,*CUTS[seq],DARK,PURPLE)
        c.finish().save(folder/f'f{f:04}.png',compress_level=2)

if __name__=='__main__':main(sys.argv[1],list(map(int,sys.argv[2:])))
