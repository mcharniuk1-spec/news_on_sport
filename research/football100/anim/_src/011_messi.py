"""Deterministic FLAT-POP animation renders for video 011."""
import math, sys
from pathlib import Path
from PIL import Image
from toolkit import Canvas, Rig, INK, WHITE, icon, keys, transition, ticker, lower_third, bubble, particles
ROOT=Path(__file__).resolve().parents[2]
BLUE='#4c80b5'; NAVY='#243957'; GOLD='#ffd66e'; RED='#e87575'; MINT='#9bd3b2'; SKIN='#f6b481'; PALE='#d9e6ee'
MESSI=Rig('#71a9d8',SKIN,'#42334a'); COACH=Rig('#536e91','#d99c70','#526346'); REPORTER=Rig(GOLD,'#c98c69','#383044')
N={'s01':36,'s02':48,'s03':42,'s04':42,'s05':36,'s06':48,'s07':36}
CUTS={'s01':('whistle-pop','speed-line-whoosh'),'s02':('camera-flash','net-ripple'),'s03':('ball-roll','page-turn'),'s04':('scribble-swipe','confetti-burst'),'s05':('turf-slide','camera-flash'),'s06':('zoom-through-icon','net-ripple'),'s07':('ink-splash','whistle-pop')}

def background(f, studio=False):
    c=Canvas(PALE if studio else '#8eb8d6')
    if studio:
        c.box((0,160,540,610),BLUE,0,0)
        for x in (62,478): c.oval(x,190,38,20,GOLD,0)
        c.box((0,610,540,960),NAVY,0,0)
        for i in range(6): c.line([(i*110,610),(i*110+45,960)],'#354e70',4)
    else:
        c.box((0,195,540,524),NAVY,0,0)
        for row in range(4):
            for i in range(11): c.oval(23+i*50+(row%2)*17,248+row*58+4*math.sin(f*.2+i),10,10,[GOLD,RED,MINT,WHITE][(i+row)%4],0)
        c.shape([(0,525),(540,492),(540,960),(0,960)],'#5e9d79',0)
        for y in (615,710,805,900): c.line([(0,y),(540,y-34)],'#87bd8b',3)
        c.line([(25,944),(270,711),(515,944)],WHITE,4)
    # gently moving broadcast specks
    for i in range(5):
        x=(i*119+f*2)%540
        c.oval(x,174+(i%3)*15,3,3,WHITE,0)
    return c

def clipboard(c,x,y,scale=1,up=False):
    w=112*scale; h=146*scale
    c.box((x-w/2,y-h/2,x+w/2,y+h/2),GOLD,8,4)
    c.box((x-w*.31,y-h*.34,x+w*.31,y-h*.20),NAVY,4,2)
    for j in range(3): c.line([(x-w*.28,y-h*.02+j*21*scale),(x+w*.28,y-h*.02+j*21*scale)],BLUE,3)
    if up: c.line([(x-w*.35,y+h*.34),(x+w*.35,y-h*.34)],RED,5)

def boot(c,x,y,s,f):
    bob=3*math.sin(f*.25)
    c.shape([(x-s*.44,y-s*.16+bob),(x-s*.18,y-s*.25+bob),(x+s*.10,y+s*.11+bob),(x+s*.37,y+s*.18+bob),(x+s*.46,y+s*.30+bob),(x-s*.31,y+s*.30+bob),(x-s*.43,y+s*.18+bob)],GOLD,5)
    c.line([(x-s*.25,y+s*.01+bob),(x+s*.11,y+s*.10+bob)],WHITE,3)
    c.line([(x-s*.4,y+s*.30+bob),(x+s*.46,y+s*.30+bob)],NAVY,5)

def hook(f,n):
    c=background(f,True)
    MESSI.draw(c,270,746,425,f,gesture=.3+.3*math.sin(f*.22))
    clipboard(c,400,582,1.3,up=f%2==0)
    if f>=4:
        y=keys(f,[(4,185),(7,205),(n,205)])
        c.box((38,y,502,y+123),NAVY,22,4); c.text(270,y+61,['Staff job for Messi?'],42,GOLD,2)
    icon(c,'whistle',119,559+5*math.sin(f*.28),31,f,GOLD)
    return c

def comic1(f,n):
    c=background(f)
    # Coach and Messi with the recurring clipboard and whistle.
    COACH.draw(c,125,730,360,f,gesture=keys(f,[(1,.15),(12,.55),(22,.6),(31,.25),(48,.25)]))
    MESSI.draw(c,372,730,394,f,gesture=keys(f,[(1,.1),(12,.2),(18,.45),(28,.4),(36,.1),(42,.75),(48,.7)]))
    clipboard(c,265,517,1.05,up=True)
    c.line([(93,535),(112,580),(128,535)],GOLD,8); c.oval(111,576,11,11,GOLD,3)
    icon(c,'ball',453,628+7*math.sin(f*.24),34,f)
    # Upside-down study resolves into a football tucked under his arm.
    if f>=13:
        c.line([(327,483),(346,460),(368,484)],INK,8)
        if f>=20:
            c.oval(328,490,13,13,WHITE,3); c.oval(361,490,13,13,WHITE,3)
        if f>=30:
            icon(c,'ball',316,573+4*math.sin(f*.3),25,f)
    # Whistle rolls toward a pocket; then a small shrug.
    if f>=36:
        xx=keys(f,[(36,197),(44,260),(48,280)])
        icon(c,'whistle',xx,665+4*math.sin(f*.4),19,f,GOLD)
        if f>=42:
            for a in (-1,1): c.line([(375+a*26,526),(375+a*39,506)],GOLD,4)
    return c

def news(f,n):
    c=background(f)
    MESSI.draw(c,274,562,418,f,gesture=.18+.12*math.sin(f*.3))
    icon(c,'ball',91,416+5*math.sin(f*.3),32,f)
    icon(c,'clock',455,385+5*math.cos(f*.25),34,f,GOLD)
    if f>=3:
        lower_third(c,['Lionel Messi','Retired at 39'])
        ticker(c,'Retired at 39',f)
    return c

def interview(f,n):
    c=background(f,True)
    c.box((46,198,494,266),NAVY,12,3); c.text(270,231,['REPORTER ASKS'],29,GOLD,0)
    REPORTER.draw(c,154,769,320,f,gesture=.5+.15*math.sin(f*.29))
    MESSI.draw(c,389,769,362,f,gesture=keys(f,[(1,.15),(18,.8),(30,.65),(42,.45)]))
    c.line([(244,554),(275,486),(309,554)],INK,15); c.line([(244,554),(275,486),(309,554)],NAVY,9); c.oval(275,476,15,25,GOLD,3)
    bubble(c,['Messi is welcome'])
    icon(c,'ball',271,707+5*math.sin(f*.26),34,f,GOLD)
    return c

def poll(f,n):
    c=Canvas('#8eb8d6')
    c.box((31,178,509,790),NAVY,28,5)
    c.text(270,259,['Reply or stay','quiet?'],47,GOLD,2)
    c.box((74,378,466,460),RED,18,4); c.text(270,419,['Already said no'],31,WHITE,1)
    c.box((74,478,466,560),MINT,18,4); c.text(270,519,['Stay quiet'],34,NAVY,1)
    p=keys(f,[(1,.02),(29,1)])
    for i,val in enumerate((.5+.35*p,.5-.35*p)):
        y=584+i*48
        c.box((103,y,437,y+22),WHITE,9,2); c.box((103,y,104+332*val,y+22),(RED,MINT)[i],9,0)
    c.box((176,701,364,751),WHITE,12,3); c.text(270,726,[str(min(77,max(1,round(77*keys(f,[(1,0),(29,1)])))))],30,NAVY,0)
    for i in range(4):
        a=f*.22+i*math.pi/2; c.oval(270+math.cos(a)*198,333+math.sin(a)*19,6,6,GOLD,0)
    return c

def comic2(f,n):
    c=background(f)
    # Two matching generic golden boots as a callback pair.
    c.box((44,707,496,762),NAVY,8,4)
    boot(c,185,597,205,f); boot(c,354,597,205,f+3)
    MESSI.draw(c,269,712,363,f,gesture=keys(f,[(1,.6),(12,.72),(22,.3),(31,.4),(36,.8),(48,.82)]))
    # podium and clipboard offered as recurring prop callback
    c.box((62,760,478,820),GOLD,12,4)
    if f>=13:
        for i in range(2):
            x=81+i*378
            c.oval(x,565+4*math.sin(f*.3+i),32,32,SKIN,3)
            c.box((x-39,596,x+39,682),(RED,BLUE)[i],10,4)
            c.line([(x-24,682),(x-35,733)],NAVY,13); c.line([(x+24,682),(x+35,733)],NAVY,13)
    if f>=36:
        clipboard(c,160,461,1.0,up=False)
        # gold pointing rays call attention to the twin boots
        for x in (180,354):
            c.line([(269,518),(x,478)],GOLD,5)
    return c

def stats(f,n):
    c=background(f)
    c.box((44,216,496,334),NAVY,18,4); c.text(270,275,['Back-to-back'],42,GOLD,2)
    # Two animated golden boots; the second pair card uses a source-backed number.
    boot(c,173,470,180,f); boot(c,365,470,180,f+6)
    c.box((64,603,476,748),WHITE,18,4)
    c.text(270,649,['2'],76,RED,2)
    c.text(270,708,['Golden Boot'],35,NAVY,0)
    # First for MLS: one star and the allowed acronym.
    c.oval(268,827,26,26,GOLD,0)
    c.text(270,869,['MLS'],31,WHITE,2)
    return c

SCENES={'s01':hook,'s02':comic1,'s03':news,'s04':interview,'s05':poll,'s06':comic2,'s07':stats}
def main(seq):
    n=N[seq]; folder=ROOT/'anim/011'/seq; folder.mkdir(parents=True,exist_ok=True)
    for f in range(1,n+1):
        c=SCENES[seq](f,n)
        transition(c,f,n,*CUTS[seq],NAVY,BLUE)
        c.finish().save(folder/f'f{f:04}.png',compress_level=2)
    print(f'{seq}: wrote {n} frames')
if __name__=='__main__':
    for s in sys.argv[1:] or list(SCENES): main(s)
