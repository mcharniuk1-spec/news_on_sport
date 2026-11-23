"""Deterministic interview insert for 001/s02. Run from any directory."""
import math
from pathlib import Path
from toolkit import Canvas, Rig, INK, WHITE, icon, particles, transition, keys

ROOT = Path(__file__).resolve().parents[2]
BASE_OUT = ROOT / 'anim/001'
SKY, MIST, DARK, PURPLE, PINK, YELLOW, TEAL = ('#a8cbdc','#7495ac','#363454','#7953a0','#ec7b81','#ffd173','#6cbdab')
SUBJECT = Rig(PURPLE, YELLOW, '#493044')
REPORTER = Rig(TEAL, YELLOW, '#503a46')


def scene(f):
    c = Canvas(SKY)
    # Mixed-zone interview set: three depth layers, a soft floor shadow, and moving light details.
    c.box((22,128,518,586), MIST, 42, 4)
    c.box((42,148,498,548), '#a6bdc9', 31, 3)
    for x in (72,170,270,370,468):
        c.line([(x,160),(x,530)], MIST, 4)
    c.box((0,548,540,960), TEAL, 0, 0)
    for j in range(5):
        y = 601 + j*66
        c.shape([(0,y),(540,y-28),(540,y+4),(0,y+32)], '#a6bdc9', 0)
    # Background lamps pulse subtly; people remain the clear foreground.
    for x in (92,448):
        c.line([(x,173),(x,268)], DARK, 5)
        c.box((x-38,148,x+38,188), DARK, 10, 3)
        for j in range(3):
            c.oval(x-20+j*20,168,5+math.sin(f*.22+j)*1.2,5, YELLOW, 0)
    c.oval(365,775,125,17,'#789f9a',0)
    c.oval(160,778,124,17,'#789f9a',0)
    # Subject and reporter use the same established SITCOM-YELLOW rigs as passed scenes.
    subj_h = 385 + 5*math.sin(f*.19)
    rep_h = 375 + 5*math.sin(f*.19 + .8)
    SUBJECT.draw(c,366,745,subj_h,f,gesture=.38+.12*math.sin(f*.17),look=-1)
    hand = REPORTER.draw(c,165,747,rep_h,f,gesture=.53+.08*math.sin(f*.21))
    # Plain, unbranded microphone between them; reporter holds it toward the subject.
    mx,my = 267 + 3*math.sin(f*.23), 550 + 2*math.sin(f*.37)
    c.line([(hand[0],hand[1]),(mx-6,my+45)],TEAL,17)
    c.oval(mx,my+34,17,22,DARK,0)
    c.box((mx-13,my-4,mx+13,my+39),INK,8,2)
    for dy in (6,14,22): c.line([(mx-8,my+dy),(mx+8,my+dy)],WHITE,2)
    # One grounded reporter question, with no invented answer or attributed quote.
    c.box((56,216,484,353), DARK, 24, 4)
    c.text(270,240,['REPORTER ASKS'],29,YELLOW,1)
    c.text(270,294,['Exactly the division?'],37,WHITE,1)
    # A wordless answer: an open palm and a small division-table icon.
    icon(c,'whistle',436,447+3*math.sin(f*.3),24,f,accent=YELLOW)
    particles(c,f,269,507)
    transition(c,f,42,'camera-flash','turf-slide',DARK,PURPLE)
    return c


def pitch(f):
    c = Canvas(SKY)
    for x in (66,474):
        c.line([(x,158),(x,350)],DARK,5)
        c.box((x-34,135,x+34,177),DARK,9,3)
        for j in range(3): c.oval(x-19+j*19,157,5,5,YELLOW,0)
    c.shape([(0,376),(180,340),(360,340),(540,376),(540,788),(0,788)],MIST,0)
    for j in range(4):
        c.shape([(0,436+j*86),(540,398+j*86),(540,437+j*86),(0,476+j*86)],'#9bb7c2',0)
    # Crowd and distant goal add depth behind the staged action.
    c.box((22,340,518,410),DARK,10,3)
    for row in range(2):
        for j in range(20): c.oval(37+j*24,353+row*24,8,7,[PURPLE,TEAL,YELLOW][(j+row)%3],0)
    return c


def comic2(f):
    c=pitch(f)
    for i,x in enumerate((145,270,395)):
        g=Rig((TEAL,PURPLE,PINK)[i],YELLOW,('#503a46','#493044','#573e43')[i])
        # Polite hand-off escalates as each player leans away from the giant ball.
        lean=math.sin(f*.24+i*2)*8 + (f-15)*.7 if 13<=f<=31 else 0
        size=(365 if i==1 else 245)
        g.draw(c,x+lean,760,size,f,gesture=.4+.25*math.sin(f*.31+i))
    bx=270+24*math.sin(f*.22)
    by=589+16*math.sin(f*.41)
    icon(c,'ball',bx,by,72,f)
    c.oval(270,680,130,20,'#789f9a',0)
    # The first chapter's armchair returns as the running prop in the background.
    c.box((35,485,145,624),PINK,20,4)
    c.box((29,547,151,644),'#bd5b82',15,4)
    c.oval(270,186,148,61,DARK,3)
    c.text(270,171,['73%'],51,YELLOW,2)
    c.box((159,703,381,765),DARK,15,3)
    if f>=37: c.text(270,716,['0-3'],31,WHITE,1)
    if f>=36:
        rival_x=keys(f,[(36,522),(41,360),(48,294)])
        rival=Rig('#d76a5f',YELLOW,'#393141')
        rival.draw(c,rival_x,744,260,f,gesture=.7)
        icon(c,'ball',rival_x+50,628-18*math.sin(f*.4),27,f)
    else:
        # Three small courtesy gestures build while the ball stays unshot.
        for j in range(3):
            a=(f+j*8)%36
            c.line([(120+j*150,502-a*.5),(137+j*150,495-a*.5)],YELLOW,4)
    transition(c,f,48,'ink-splash','net-ripple',DARK,PURPLE)
    return c


def stats(f):
    c=Canvas(SKY)
    c.box((24,148,516,785),MIST,34,4)
    c.box((45,171,495,759),'#a6bdc9',27,3)
    # Two narration-grounded counting cards, with active icons and a short graphic hand-off.
    phase=keys(f,[(1,0),(6,0),(16,1),(17,0),(22,0),(30,1),(36,1)])
    if f<=18:
        c.box((82,302,458,639),DARK,30,4)
        c.text(270,344,["Ballon d'Or"],42,WHITE,2)
        icon(c,'trophy',270,495+7*math.sin(f*.4),68,f,accent=YELLOW)
        c.text(270,585,['2004'],49,YELLOW,2)
    else:
        c.box((82,302,458,639),PURPLE,30,4)
        icon(c,'ball',158,501+10*math.sin(f*.4),42,f)
        icon(c,'clock',382,501,42,f)
        c.text(270,566,['Twenty-four goals'],28,YELLOW,1)
        c.text(270,608,['Thirty-two games'],28,YELLOW,1)
    # Scrolling accent ticks give each held layout motion without moving its labels.
    x=83+(f*12)%374
    c.line([(x,710),(min(x+42,457),710)],TEAL,7)
    transition(c,f,36,'zoom-through-icon','camera-flash',DARK,TEAL)
    return c


def comic3(f):
    c=Canvas(SKY)
    c.box((26,150,514,786),MIST,34,4)
    c.box((48,173,492,753),'#a6bdc9',27,3)
    c.box((142,484,424,510),DARK,6,3)
    c.box((163,535,403,561),DARK,6,3)
    c.box((184,586,382,612),DARK,6,3)
    # Three cups already on the shelf, plus the new generic trophy.
    for j in range(3):
        x=213+j*64
        c.box((x-12,431,x+12,471),YELLOW,7,2)
        c.line([(x-24,433),(x-11,433),(x-11,449),(x-21,449)],YELLOW,5)
        c.line([(x+24,433),(x+11,433),(x+11,449),(x+21,449)],YELLOW,5)
    shev=Rig(PURPLE,YELLOW,'#493044')
    yamal=Rig(TEAL,YELLOW,'#392f3d')
    shev.draw(c,154,759,395,f,gesture=.6 if f<31 else .26)
    yamal.draw(c,382,759,345,f,gesture=.25+.15*math.sin(f*.2))
    trophy_x=keys(f,[(1,227),(12,252),(20,290),(29,306),(36,306),(42,225),(48,188)])
    icon(c,'trophy',trophy_x,506+4*math.sin(f*.35),33,f,accent=YELLOW)
    # Callback to chapter one: a tiny armchair with the permitted League B label.
    c.box((46,269,112,344),PINK,12,3)
    c.box((40,306,118,358),'#bd5b82',10,3)
    c.box((50,244,109,264),DARK,6,2)
    c.text(80,248,['League B'],13,WHITE,0)
    if f>=36:
        c.box((274,351,439,389),YELLOW,8,2)
        c.text(355,361,['Seven points'],19,DARK,0)
        c.line([(353,390),(410,430)],INK,3)
        c.oval(409,430,5,5,INK,0)
    else:
        for j in range(4):
            yy=394+(j*23+f*2)%72
            c.line([(126+j*88,yy),(139+j*88,yy-5)],WHITE,2)
    transition(c,f,48,'page-turn','confetti-burst',DARK,PINK)
    return c


def poll(f):
    c=Canvas(SKY)
    c.box((28,153,512,784),MIST,32,4)
    c.box((48,173,492,759),'#a6bdc9',27,3)
    c.box((62,213,478,344),DARK,20,4)
    c.text(270,244,['Which tally sounds better?'],30,WHITE,1)
    c.box((76,390,464,480),PURPLE,18,4)
    c.box((76,535,464,625),TEAL,18,4)
    c.text(270,411,['Three Kopa trophies'],29,WHITE,1)
    c.text(270,556,['7 points, 6 games'],29,WHITE,1)
    # Animated poll bars, a tick counter and button pulse.
    for i,(y,col) in enumerate(((493,PINK),(638,YELLOW))):
        c.box((78,y,462,y+28),WHITE,10,2)
        fill=keys(f,[(1,16+i*7),(18,244+i*18),(30,310-i*20),(36,322-i*26)])
        c.box((80,y+2,80+fill,y+26),col,9,0)
    # The count cue is a moving stopwatch hand; no fabricated vote total is shown.
    icon(c,'clock',270,703,24,f)
    pulse=4+2*math.sin(f*.65)
    c.oval(437,198,pulse,pulse,PINK,0)
    transition(c,f,36,'ball-roll','whistle-pop',DARK,TEAL)
    return c


SEQUENCES={'s02':(42,scene),'s05':(48,comic2),'s06':(36,stats),'s07':(48,comic3),'s08':(36,poll)}


def main(seq):
    n,renderer=SEQUENCES[seq]
    folder=BASE_OUT/seq
    folder.mkdir(parents=True,exist_ok=True)
    # Refuse to replace any frame already present; passed or existing work is preserved.
    for f in range(1,n+1):
        path=folder/f'f{f:04}.png'
        if path.exists():
            raise FileExistsError(f'Won\'t overwrite existing output: {path}')
        renderer(f).finish().save(path,compress_level=2)

if __name__ == '__main__':
    import sys
    main(sys.argv[1])
