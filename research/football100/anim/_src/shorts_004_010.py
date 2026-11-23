"""Plan-led, sequential PNG renderer for Shorts 004–010."""
import json,re,sys,math
from pathlib import Path
from PIL import Image,ImageDraw
from toolkit import Canvas,Rig,INK,WHITE,font,icon,keys,ease,back,transition,particles
ROOT=Path(__file__).resolve().parents[2]
PLAN=json.loads((ROOT/'codex/v2/plan.json').read_text())
LOOKS={
'004':('#b8cce1','#665183','#f3ad7d','#ed7780','#a0d4c7'),
'005':('#f5bb8b','#3e4b7e','#ffd16a','#7272cd','#9bd7a8'),
'006':('#b4d7da','#354564','#f3c35f','#ec846f','#92c5a6'),
'007':('#e9c2ca','#484265','#ffe073','#8782cb','#9cd1bf'),
'008':('#bee1cd','#3c5a77','#ffdb62','#ef8d76','#a2a3e4'),
'009':('#b2c3e2','#514476','#f7be77','#e97986','#80cdc3'),
'010':('#eabac5','#403c65','#ffcc67','#ec775e','#92c8e0')}
HOOKS={'004':'A red card on debut?','005':'How did a two-goal lead vanish?','006':'Great defender, great coach?','007':'Why did Kaka cry?','008':'How much was Kaka worth?','009':'Is Benzema really leaving?','010':'Kart or Formula One?'}
COMICS={
'004': [('cabinet','chair','cup','envelope'),('board','chair','notebook','pen'),('monitor','ball','net','ball')],
'005': [('scoreboard','chair','ball','espresso'),('calendar','counter','espresso','espresso')],
'006': [('vending','ball','cup','ticket'),('stair','scroll','stair','cup'),('net','clipboard','ball','whistle')],
'007': [('flag','bucket','droplet','tap'),('locker','shirt','ball','envelope'),('monitor','card','headset','flag')],
'008': [('wheelbarrow','coin','coin','coin'),('clock','card','clock','watch')],
'009': [('rack','shirt','shirt','key'),('hat','whistle','cat','tag'),('clipboard','stamp','paper','heart')],
'010': [('track','car','car','cup'),('garage','phone','phone','key'),('track','car','phone','flag')]}
TYPES={'HOOK':'Question lands, hero reacts, prop answers visually.',
'NEWS':'Name and one narration fact lock while football icons follow through.',
'INTERVIEW':'Reporter offers the microphone; subject responds with a gesture and an icon.',
'PROVOC':'Two option bars animate without fabricated percentages or betting cues.',
'STATS':'Animated icon pairs resolve into the exact source figures.'}

def fit(c,x,y,copy,width=420,limit=44):
    size=limit
    while size>21 and any(font(size).getlength(x)>width for x in copy):
        size-=1
    c.text(x,y,copy,size)
def wrap(s,width=24):
    lines=['']
    for word in s.split():
        if len(lines[-1])+len(word)+1>width and lines[-1]:lines.append('')
        lines[-1]=(lines[-1]+' '+word).strip()
    return lines
def tag(c,x,y,copy,w=430,h=120,maxsize=44):
    c.box((x-w/2,y-h/2,x+w/2,y+h/2),INK,18,4)
    lines=wrap(copy,26)
    size=min(maxsize,int((h-14)/len(lines)))
    while size>21 and any(font(size).getlength(line)>w-28 for line in lines):size-=1
    c.text(x,y-(len(lines)-1)*size*.52,lines,size)

def prop(c,k,x,y,r,f,colors):
    _,dark,gold,warm,cool=colors
    def box(a,b,d,e,col,rr=8):c.box((x+a*r,y+b*r,x+d*r,y+e*r),col,rr)
    def oval(a,b,d,e,col,w=3):c.oval(x+a*r,y+b*r,d*r,e*r,col,w)
    def line(p,col=INK,w=4):c.line([(x+a*r,y+b*r) for a,b in p],col,w)
    def poly(p,col):c.shape([(x+a*r,y+b*r) for a,b in p],col)
    if k in ('clock','watch','ball','net','whistle','cup'):icon(c,{'watch':'clock'}.get(k,k),x,y,r,f,gold)
    elif k in ('cabinet','vending','locker','monitor','scoreboard','calendar','board','garage'):
        box(-1,-1,1,1,dark,15);box(-.85,-.83,.85,.66,cool,10)
        if k in ('cabinet','locker','vending'):
            for j in (-.43,.05,.54):line([(-.82,j),(.83,j)],dark)
            if k=='locker':oval(.62,-.09,.06,.10,gold)
            elif k=='cabinet':
                for u in (-.5,0,.5):icon(c,'cup',x+u*r,y-r*.60,r*.16,f,gold)
            else:
                for u in (-.5,0,.5):oval(u,-.28,.17,.17,gold)
        elif k in ('monitor','scoreboard'):
            for j in (-.42,.42):box(j-.28,-.45,j+.28,.02,gold)
        elif k=='calendar':
            box(-.83,-.82,.83,-.48,warm)
            for i in range(3):
                for j in range(4):oval(-.52+.35*j,-.29+i*.28,.075,.075,WHITE,0)
        elif k=='garage':
            for j in (-.60,-.28,.06,.42):line([(-.81,j),(.81,j)],dark)
        else:
            for j in (0,.18,.36):line([(-.48,j),(.58,j)],WHITE,3)
    elif k in ('paper','notebook','scroll','ticket','clipboard','envelope','tag','card','stamp'):
        box(-.82,-.63,.82,.62,gold if k in ('ticket','tag','card') else WHITE,7)
        if k=='envelope':line([(-.78,-.59),(0,.03),(.79,-.59)])
        elif k=='stamp':
            box(-.24,-.93,.24,-.40,dark)
            box(-.68,.22,.68,.59,warm)
        else:
            if k=='clipboard':box(-.32,-.73,.32,-.52,dark)
            for j in (-.11,.12,.34):line([(-.53,j),(.43,j)],dark,2)
    elif k in ('chair','counter','stair','rack'):
        if k=='chair':
            box(-.76,-.77,.17,.27,warm,16);box(-.71,.19,.81,.45,warm)
            line([(-.53,.39),(-.59,1)],INK,7);line([(.57,.39),(.67,1)],INK,7)
        elif k=='stair':
            poly([(-1,1),(-1,.62),(-.52,.62),(-.52,.19),(-.05,.19),(-.05,-.21),(.44,-.21),(.44,-.64),(1,-.64),(1,1)],gold)
        elif k=='rack':
            line([(-.86,.8),(-.86,-.72),(.86,-.72),(.86,.8)],INK,7)
            for j in (-.51,0,.51):prop(c,'shirt',x+j*r,y-r*.06,r*.34,f,colors)
        else:box(-1,-.1,1,.62,warm,10)
    elif k in ('car','wheelbarrow','track'):
        if k=='track':
            oval(0,0,1.1,.64,warm)
            oval(0,0,.83,.44,cool)
            oval(0,0,.96,.53,warm,1);oval(0,0,.76,.35,cool,1)
        elif k=='car':
            poly([(-1,.12),(-.80,-.21),(-.46,-.21),(-.19,-.56),(.31,-.55),(.50,-.24),(.89,-.11),(1,.31),(-1,.31)],warm)
            poly([(-.17,-.47),(.23,-.47),(.42,-.22),(-.37,-.22)],cool)
            for o in (-.61,.64):oval(o,.34,.23,.23,dark);oval(o,.34,.10,.10,WHITE)
        else:
            poly([(-.88,-.41),(.68,-.41),(.37,.23),(-.57,.23)],warm)
            line([(.55,-.39),(1,-.67)],INK,7);oval(-.25,.49,.30,.30,dark)
    elif k=='shirt':
        poly([(-.87,-.47),(-.43,-.77),(-.22,-.76),(0,-.55),(.25,-.76),(.47,-.74),(.89,-.46),(.66,-.13),(.44,-.25),(.44,.77),(-.47,.77),(-.47,-.25),(-.68,-.13)],warm)
    elif k in ('espresso','bucket','hat','headset'):
        if k=='hat':
            oval(0,.27,1,.27,warm);box(-.58,-.54,.58,.25,warm)
        elif k=='headset':
            oval(0,0,.75,.73,dark);oval(0,0,.54,.54,cool)
            box(-.83,-.18,-.56,.54,warm);box(.56,-.18,.83,.54,warm)
        else:
            oval(.63,.04,.32,.38,dark);poly([(-.7,-.45),(.66,-.45),(.49,.57),(-.47,.57)],WHITE if k=='espresso' else cool)
            oval(-.02,-.44,.68,.17,dark)
    elif k in ('coin','key','tap','droplet','heart'):
        if k=='coin':
            oval(0,0,.56+.22*math.sin(f*.18)**2,.73,gold);oval(0,0,.38,.54,warm,0)
        elif k=='key':
            oval(-.51,0,.37,.38,gold);oval(-.51,0,.13,.14,dark,0)
            line([(-.18,0),(.82,0),(.82,.31),(.54,.31)],gold,10)
        elif k=='tap':
            line([(-.82,.31),(-.22,.31),(-.22,-.31),(.62,-.31),(.62,.10)],dark,16)
            line([(-.49,-.48),(.03,-.48)],gold,9)
        elif k=='droplet':poly([(0,-.92),(-.59,-.02),(-.48,.53),(0,.78),(.48,.53),(.59,-.02)],cool)
        else:
            oval(-.30,-.20,.43,.43,warm,0);oval(.30,-.20,.43,.43,warm,0)
            c.shape([(x-.68*r,y-.12*r),(x+.68*r,y-.12*r),(x,y+.72*r)],warm,0)
    elif k in ('phone','pen','flag','cat'):
        if k=='phone':box(-.5,-.83,.5,.83,dark,13);box(-.36,-.65,.36,.53,cool)
        elif k=='pen':line([(-.63,.61),(.69,-.71)],warm,12)
        elif k=='flag':
            line([(-.57,1),(-.57,-1)],dark,7)
            poly([(-.56,-.96),(.85,-.95),(.53,-.42),(-.56,-.34)],warm)
        else:
            oval(0,.28,.66,.55,warm);oval(0,-.25,.53,.45,warm)
            for j in (-1,1):
                poly([(j*.49,-.28),(j*.45,-.82),(j*.11,-.54)],warm)
                oval(j*.19,-.26,.055,.085,dark,0)
    else:icon(c,'ball',x,y,r,f)

def background(colors,interior,variant):
    bg,dark,gold,warm,cool=colors
    c=Canvas(bg)
    if interior:
        c.box((22,149,518,568),cool,48,4)
        for i in range(4):c.line([(77+i*126,167),(77+i*126,548)],bg,4)
        c.box((0,562,540,770),dark,0,0)
        c.shape([(75,609),(465,610),(537,751),(4,750)],cool,0)
    else:
        for x in (53,484):
            c.line([(x,169),(x,477)],dark,5)
            c.box((x-30,150,x+30,183),dark,8,2)
            for j in range(3):c.oval(x-17+j*17,166,4,4,WHITE,0)
        for row in range(4):
            c.box((0,343+row*34,540,375+row*34),dark if row%2==0 else bg,0,0)
            for j in range(15):c.oval(11+j*37,354+row*35,9,7,[warm,cool,gold][(j+row+variant)%3],0)
        c.box((0,480,540,768),cool,0,0)
        for i in range(4):c.shape([(0,522+i*69),(540,507+i*69),(540,534+i*69),(0,548+i*69)],bg,0)
    return c

def source(vid,s):
    raw=(ROOT/f'codex/v2/plan/{vid}.md').read_text()
    block=re.search(r'^## '+s['id']+r'\s.*?\n(.*?)(?=^## |\Z)',raw,re.M|re.S)[1]
    allowed=re.search(r'^- Allowed on-screen text.*?: (.+)',raw,re.M)[1].split(' | ')
    narr=re.findall(r'^\d+\.\s+\[.*?\]\s+(.+?)\s+\(card: (.*?)\)\s*$',raw,re.M)
    line=s['line_from']
    fact=narr[min(line,len(narr)-1)][1] if narr else ''
    if fact not in allowed or re.search('bet|aboutfootball|injur|doping|crime',fact,re.I):
        fact=next((x for x in allowed if x!=PLAN[vid]['subject'] and not re.search('bet|aboutfootball|injur|doping|crime|incident|expelled',x,re.I)),'')
    return block,fact

def draw(vid,s,f,fact):
    colors=LOOKS[vid];bg,dark,gold,warm,cool=colors
    n=s['frames']; typ=s['type']; j=int(s['id'][1:]); name=PLAN[vid]['subject']
    wave=math.sin(f*.29); p=f/n
    skin=gold if PLAN[vid]['style']=='SITCOM-YELLOW' else '#efaf81'
    hero=Rig(warm,skin,'#453047'); co=Rig(cool,skin,'#56454d')
    case=int(s['kind'][-1])-1 if typ=='COMIC' else 0
    props=COMICS[vid][case] if typ=='COMIC' else None
    c=background(colors,typ in ('INTERVIEW','PROVOC') or (typ=='COMIC' and props[0] not in ('net','track','flag','scoreboard')),j)
    if typ=='HOOK':
        h=keys(f,[(1,399),(6,430),(12,414),(n,418)],back)
        hero.draw(c,235,727,h,f,.26+.22*wave)
        prop(c,COMICS[vid][0][2],415,580+13*wave,63,f,colors)
        particles(c,f,419,539)
        if f>=4:tag(c,270,190,HOOKS[vid],467,138,47)
    elif typ=='NEWS':
        hero.draw(c,250,573,416,f,.20+.15*wave)
        for k,r,x,y in [('ball',33,80,463),('clock',34,458,362),(COMICS[vid][0][2],43,455,489)]:
            prop(c,k,x,y+7*math.sin(f*.26+x),r,f,colors)
        if f>=4:
            tag(c,270,646,name,465,97,40)
            if fact:tag(c,270,735,fact,440,64,39)
            c.line([(55+(f*4)%401,773),(69+(f*4)%401,773)],gold,4)
    elif typ=='INTERVIEW':
        hand=co.draw(c,133,735,392,f,.68)
        hero.draw(c,379,731,428,f,.14+.23*wave)
        c.line([hand,(hand[0]+37,hand[1]-26)],INK,13)
        c.oval(hand[0]+42,hand[1]-30,15,12,dark)
        prop(c,'ball',273,410+15*wave,38,f,colors)
        if f>=5 and fact:tag(c,270,190,fact,450,125,44)
    elif typ=='PROVOC':
        hero.draw(c,268,685,399,f,.32+.24*wave)
        if f>=4:
            tag(c,270,188,HOOKS[vid],465,132,46)
            for k,(x,r) in enumerate(((77,.63),(293,.37))):
                c.box((x,715,x+169,767),WHITE,16,3)
                c.box((x,718,x+21+137*r*ease(p*1.7),764),warm if k==0 else cool,13,0)
                c.oval(x+11+4*wave,742,5,5,dark,0)
    elif typ=='STATS':
        for k,(kind,x,r) in enumerate((('cup',162,92),('ball',376,96))):
            y=426+23*math.sin(f*.22+k)
            c.oval(x,607,77,13,dark,0)
            prop(c,kind,x,y,r,f+k*4,colors)
            particles(c,f+k*2,x,y)
        if f>=4 and fact:tag(c,270,680,fact,467,137,48)
    else:
        b0,b1,b2,b3=props
        f0=max(8,round(n*.25)); f1=round(n*.64); f2=round(n*.74)
        gag=keys(f,[(1,0),(f0,0),(f0+6,.68),(f1,1),(f2,.14),(n,.06)])
        reveal=ease((f-f2)/5)
        idle=3*wave
        base_y=503+idle
        prop(c,b0,387,base_y,95,f,colors)
        hero.draw(c,176+45*gag,730-30*gag,414-15*gag,f,.25+.58*gag)
        if b1 not in ('ball','coin','droplet','car'):prop(c,b1,89,637+idle,50,f,colors)
        if b0 in ('cabinet','vending','wheelbarrow','flag','scoreboard','track'):
            total=max(1,round(5*gag))
            for k in range(total):
                t=(p*2.7+k*.20)%1
                prop(c,b2,360-119*t+14*k,488+163*t-70*math.sin(math.pi*t),29+k%2*4,f+k,colors)
        else:
            prop(c,b2,326-70*gag,650-147*gag+idle,46+14*gag,f,colors)
        if f>=f2:
            prop(c,b3,368+40*reveal,674-35*reveal+idle,42+18*reveal,f,colors)
        if f0<f<f1:particles(c,f,325,560,True)
    # Use different transition pairs by sequence. Preserve the first/middle/end distinction.
    modes=[('turf-slide','whistle-pop'),('ball-roll','scribble-swipe'),('page-turn','net-ripple'),('camera-flash','turf-slide'),
           ('whistle-pop','page-turn'),('ball-roll','turf-slide'),('ink-splash','var-glitch'),('camera-flash','scribble-swipe')]
    transition(c,f,n,*modes[(j-1)%len(modes)],dark,colors[1] if typ!='STATS' else warm)
    return c

def prepare(vid,s,fact,block):
    stage=ROOT/'anim'/vid
    stage.mkdir(exist_ok=True)
    kit=stage/'kit.json'
    if not kit.exists():
        kit.write_text(json.dumps({'palette':LOOKS[vid],'style':PLAN[vid]['style'],'font':'Arial Bold','characters':[PLAN[vid]['subject'],'generic reporter'],'recurring_prop':COMICS[vid][0][0]},indent=2)+'\n')
    doc=stage/'storyboard.md'
    if doc.exists() and f"## {s['id']} " in doc.read_text():return
    with doc.open('a') as out:
        out.write(f"\n## {s['id']} · {s['kind']}\n\n"+block+"\n\n")
        out.write('| Frames | Pose / fixed camera | Exact text used |\n|---|---|---|\n')
        n=s['frames']
        for f in range(1,n+1,6):
            state='IN reveal' if f==1 else 'OUT wipe' if f>=n-5 else TYPES.get(s['type'],'Progress prop action and hero reaction according to the current beat.')
            text=HOOKS[vid] if s['type'] in ('HOOK','PROVOC') else 'None' if s['type']=='COMIC' else fact
            if s['type']=='NEWS':text=PLAN[vid]['subject']+'; '+fact
            out.write(f'| {f}–{min(n,f+5)} | {state} | {text} |\n')
def main(vid):
    style=ROOT/'anim/_sheets'/f"{PLAN[vid]['style']}.png"
    with Image.open(style) as im:im.load()
    log=ROOT/'anim/PROGRESS.md'
    for s in PLAN[vid]['sequences']:
        path=ROOT/'anim'/vid/s['id']
        n=s['frames']; expected=[path/f'f{f:04}.png' for f in range(1,n+1)]
        if all(x.is_file() for x in expected):continue
        block,fact=source(vid,s)
        prepare(vid,s,fact,block)
        path.mkdir(exist_ok=True)
        for f,file in enumerate(expected,1):
            if file.exists():continue
            draw(vid,s,f,fact).finish().save(file,compress_level=1)
        with log.open('a') as out:
            out.write(f"{vid}/{s['id']} done, note: individually code-rendered PNGs; sequence check skipped per request\n")
        print(f"{vid}/{s['id']} {n} PNGs",flush=True)
if __name__=='__main__':
    for video in sys.argv[1:]:main(video)
