"""Deterministic FLAT-POP code renders for the remaining video 002 sequences."""
import math, sys
from pathlib import Path
from PIL import Image
from toolkit import Canvas, Rig, INK, WHITE, icon, keys, transition, ticker, bubble, poll_bars
ROOT=Path(__file__).resolve().parents[2]
PINK,PLUM,DARK,CORAL,YELLOW,MINT,SKIN=('#dd9bb7','#8f557a','#322c52','#f37d72','#ffe080','#9bd3b2','#f6b481')
PLAYER=Rig(CORAL,SKIN,'#462d4b')
REPORTER=Rig(YELLOW,'#df9e6b','#3c324d')
CUTS={'s04':('net-ripple','confetti-burst'),'s05':('zoom-through-icon','whistle-pop'),'s06':('scribble-swipe','camera-flash'),'s07':('turf-slide','ball-roll')}

def stage(f, stadium=True):
    c=Canvas(PINK)
    # layered grandstand, crowd, pitch and light pools
    c.box((0,178,540,527),PLUM,0,0)
    for row in range(4):
        y=250+row*61
        for i in range(11):
            x=22+i*51+(row%2)*19
            c.oval(x,y+4*math.sin(f*.19+i),12,12,[YELLOW,MINT,CORAL,WHITE][(i+row)%4],0)
    c.shape([(0,528),(540,478),(540,960),(0,960)],'#579a78',0)
    for y in (595,688,781,874): c.line([(0,y),(540,y-48)],'#8cc69a',3)
    c.line([(30,940),(270,700),(510,940)],WHITE,4)
    for x in (54,486):
        c.line([(x,160),(x,412)],WHITE,6)
        for j in range(4): c.line([(x-35,177+j*8),(x+35,177+j*8)],YELLOW,7)
    return c

def cassette(c,x,y,w,f):
    h=w*.58
    c.box((x-w/2,y-h/2,x+w/2,y+h/2),DARK,10,5)
    c.box((x-w*.36,y-h*.2,x+w*.36,y+h*.17),WHITE,10,3)
    for sign in (-1,1):
        cx=x+sign*w*.23
        c.oval(cx,y,w*.088,w*.088,PINK,4)
        a=f*.3
        c.line([(cx,y),(cx+math.cos(a)*w*.06,y+math.sin(a)*w*.06)],DARK,3)
    c.line([(x-w*.3,y+h*.33),(x+w*.3,y+h*.33)],PLUM,5)

def comic2(f,n):
    c=stage(f)
    PLAYER.draw(c,230,711,425,f,gesture=keys(f,[(1,.15),(12,.26),(20,.8),(31,.65),(36,.3),(42,.7),(48,.55)]))
    cassette(c,390,627,239,f)
    # generic gold ball trophy
    c.oval(119,363,44,44,YELLOW,5); c.box((94,400,144,461),YELLOW,8,4); c.box((78,461,160,480),DARK,5,4)
    c.line([(79,346),(54,346),(54,395),(92,404)],YELLOW,8); c.line([(159,346),(184,346),(184,395),(146,404)],YELLOW,8)
    if f>=13:
        kiss=keys(f,[(13,0),(20,1),(26,.25),(31,1),(36,0),(48,0)],lambda t:t*t*(3-2*t))
        c.shape([(288,371),(311,350),(336,361),(316,377)],CORAL,4)
        for i in range(5):
            a=f*.14+i*math.tau/5
            c.line([(319+math.sin(a)*kiss*28,362+math.cos(a)*kiss*25),(319+math.sin(a)*kiss*42,362+math.cos(a)*kiss*39)],YELLOW,4)
    if 36<=f:
        # ticket emerging from cassette, safely centered in clear upper field
        yy=keys(f,[(36,557),(42,445),(48,445)])
        c.box((306,yy-54,492,yy+12),YELLOW,7,3)
        c.text(399,yy-29,['24 goals'],27,DARK,0)
    return c

def newsstats(f,n):
    c=stage(f)
    # 2003-04 season, 24-goal tally and Ballon d'Or cue
    c.box((43,222,497,337),DARK,20,4); c.text(270,267,['2003-04'],52,YELLOW,2)
    # bouncing ball and tally bars
    bounce=abs(math.sin(f*.34))
    icon(c,'ball',120,483-50*bounce,47,f)
    c.box((205,398,482,590),WHITE,20,4)
    c.text(344,424,['Serie A goals'],29,DARK,0)
    count=max(1,min(24,round(24*keys(f,[(1,0),(20,1),(30,1)]))))
    c.text(344,500,[str(count)],76,CORAL,2)
    c.box((65,656,475,784),YELLOW,20,4)
    c.oval(144,720,39,39,YELLOW,5); c.box((123,754,165,772),DARK,4,3)
    c.text(324,720,["Ballon d'Or"],36,DARK,0)
    for i in range(5):
        x=80+i*95
        c.oval(x,827+5*math.sin(f*.4+i),5,5,WHITE,0)
    return c

def interview(f,n):
    c=Canvas(PINK)
    c.box((0,180,540,586),PLUM,0,0)
    c.box((39,553,501,583),YELLOW,8,3)
    # studio lights and backdrop details
    for x in (84,456):
        c.oval(x,208,35,16,WHITE,0); c.line([(x,224),(x,339)],YELLOW,3)
    c.box((62,205,478,266),DARK,12,3); c.text(270,234,['REPORTER ASKS'],30,YELLOW,0)
    REPORTER.draw(c,151,770,320,f,gesture=.55+.12*math.sin(f*.3))
    PLAYER.draw(c,387,770,365,f,gesture=keys(f,[(1,.1),(20,.8),(31,.7),(36,.25),(42,.35)]))
    # generic microphone, held between them
    c.line([(238,545),(271,485),(306,545)],INK,16); c.line([(238,545),(271,485),(306,545)],DARK,10)
    c.oval(271,474,16,27,YELLOW,4)
    bubble(c,['The tape was right.'])
    icon(c,'ball',270,700+5*math.sin(f*.29),35,f,YELLOW)
    return c

def poll(f,n):
    c=Canvas(PINK)
    c.box((29,187,511,786),DARK,28,5)
    c.text(270,267,['Be kind,','rewind?'],52,YELLOW,2)
    # answer choices are exact phrases from narration
    c.box((72,388,468,470),CORAL,18,4); c.text(270,429,['Be kind'],40,WHITE,1)
    c.box((72,483,468,565),MINT,18,4); c.text(270,524,['Rewind'],40,DARK,1)
    p=keys(f,[(1,.02),(28,1)])
    # Separate vote bars sit below their labels, so the text remains clear.
    for i,value in enumerate((.5+.38*p,.5-.38*p)):
        y=590+i*49
        c.box((95,y,445,y+24),WHITE,10,2)
        c.box((95,y,96+348*value,y+24),(CORAL,MINT)[i],10,0)
    count=max(1,min(77,round(77*keys(f,[(1,0),(28,1)]))))
    c.box((155,708,385,758),WHITE,15,3); c.text(270,733,[str(count)],32,DARK,0)
    for i in range(4):
        a=f*.24+i*math.pi/2
        c.oval(270+math.cos(a)*198,339+math.sin(a)*17,6,6,YELLOW,0)
    return c

FUN={'s04':comic2,'s05':newsstats,'s06':interview,'s07':poll}
def main(seq):
    n={'s04':48,'s05':36,'s06':42,'s07':36}[seq]
    folder=ROOT/'anim/002'/seq; folder.mkdir(exist_ok=True)
    for f in range(1,n+1):
        c=FUN[seq](f,n)
        transition(c,f,n,*CUTS[seq],DARK,PLUM)
        c.finish().save(folder/f'f{f:04}.png',compress_level=2)
    print(f'{seq}: wrote {n} frames')
if __name__=='__main__':
    for seq in sys.argv[1:] or list(FUN): main(seq)
