"""Small deterministic 2D toolkit. Coordinates are on a 540×960 stage."""
from dataclasses import dataclass
from functools import lru_cache
import math
from PIL import Image, ImageDraw, ImageFont

SIZE = (540, 960)
INK, WHITE = '#211c32', '#fff8e4'
FONT = '/System/Library/Fonts/Supplemental/Arial Bold.ttf'

def clamp(t):
    return min(1, max(0, t))

def ease(t):
    t = clamp(t)
    return t*t*(3-2*t)

def back(t):
    t = clamp(t)-1
    return 1+2.7*t**3+1.7*t*t

def elastic(t):
    t = clamp(t)
    return 1-(1-t)**3*math.cos(3.5*math.pi*t)

def keys(f, points, curve=ease):
    for (a,x),(b,y) in zip(points,points[1:]):
        if f<=b:
            return x+(y-x)*curve((f-a)/(b-a))
    return points[-1][1]

@lru_cache
def font(size):
    return ImageFont.truetype(FONT,size)

class Canvas:
    def __init__(self,color):
        self.im=Image.new('RGB',SIZE,color)
        self.d=ImageDraw.Draw(self.im)

    def shape(self,points,color,w=3,edge=INK):
        self.d.polygon(points,fill=color)
        if w:self.d.line(points+[points[0]],fill=edge,width=w,joint='curve')

    def box(self,b,color,r=16,w=3):
        self.d.rounded_rectangle(b,r,fill=color,outline=INK if w else None,width=max(1,w))

    def oval(self,x,y,rx,ry,color,w=3):
        self.d.ellipse((x-rx,y-ry,x+rx,y+ry),fill=color,outline=INK if w else None,width=max(1,w))

    def line(self,points,color=INK,w=3):
        self.d.line(points,fill=color,width=w,joint='curve')

    def text(self,x,y,lines,size=49,color=WHITE,stroke=2):
        for j,s in enumerate(lines):
            p=(x,y+j*int(size*1.03))
            self.d.text((p[0]+2,p[1]+4),s,font=font(size),anchor='mm',fill=INK,stroke_width=stroke,stroke_fill=INK)
            self.d.text(p,s,font=font(size),anchor='mm',fill=color,stroke_width=stroke,stroke_fill=INK)

    def finish(self):
        return self.im.resize((1080,1920),Image.Resampling.LANCZOS)

def limb(c,p,color,w):
    c.line(p,INK,w+5)
    c.line(p,color,w)
    for x,y in p:
        c.oval(x,y,w/2,w/2,color,0)

@dataclass
class Rig:
    shirt: str
    skin: str
    hair: str
    crest: int=0

    def draw(self,c,x,y,h,f,gesture=0,sit=0,look=1):
        breath=1+.016*math.sin(f*.43)
        def p(a,b):return (x+a*h,y+b*h*breath)
        def el(a,b,rx,ry,col,w=3):
            xx,yy=p(a,b); c.oval(xx,yy,rx*h,ry*h,col,w)
        def poly(pts,col,w=3):c.shape([p(*pt) for pt in pts],col,w)
        def stroke(pts,col=INK,w=3):c.line([p(*pt) for pt in pts],col,w)
        def arm(pts,col,w):limb(c,[p(*pt) for pt in pts],col,max(4,round(w*h)))
        el(0,.012,.22,.036,'#564861',0)
        for side in (-1,1):
            toe=side*.16+.17*sit
            arm([(side*.09,-.30),(side*.12+.14*sit,-.165),(toe,-.054)],'#354366',.07)
            el(toe+.025,-.028,.072,.036,WHITE)
        poly([(-.17,-.55),(-.11,-.62),(.11,-.62),(.17,-.55),(.19,-.29),(-.18,-.29)],self.shirt)
        poly([(-.17,-.53),(-.11,-.44),(-.1,-.35),(.166,-.314),(.18,-.294),(-.17,-.294)],'#84518c',0)
        stroke([(-.066,-.607),(0,-.565),(.066,-.607)],WHITE,4)
        hand=(.25+.085*gesture,-.40-.17*gesture)
        arm([(-.14,-.54),(-.205,-.45),(-.20,-.35)],self.shirt,.064)
        arm([(.14,-.54),(.23,-.49),hand],self.shirt,.064)
        for u,v in [(-.20,-.35),hand]:el(u,v,.037,.035,self.skin)
        el(-.165,-.77,.044,.045,self.skin);el(.165,-.77,.044,.045,self.skin)
        el(0,-.78,.17,.176,self.skin)
        flutter=.018*math.sin(f*.64)
        poly([(-.166,-.805),(-.166,-.902),(-.107,-.948),(-.01,-.974-flutter),(.119,-.948),(.171,-.895),(.163,-.825),(.099,-.872),(-.059,-.887)],self.hair)
        stroke([(-.108,-.923),(-.028,-.946-flutter),(.076,-.93)],'#855960',4)
        for u in (-.058,.061):
            if f%29 in (19,20):stroke([(u-.039,-.784),(u+.031,-.784)],INK,3)
            else:
                el(u,-.789,.04,.05,WHITE)
                el(u+.016*look,-.789,.016,.025,INK,0)
        stroke([(.014,-.771),(.023,-.738),(.006,-.729)],INK,3)
        if gesture>.56:
            el(.004,-.68,.047,.034,INK)
        else:
            stroke([(-.049,-.702),(-.018,-.685),(.023,-.686),(.063,-.716)],INK,4)
        return p(*hand)

def icon(c,kind,x,y,r,f,accent='#ffd25d'):
    if kind=='ball':
        c.oval(x,y,r,r,WHITE)
        for j in range(5):
            a=f*.13+j*math.tau/5
            px,py=x+math.cos(a)*r*.77,y+math.sin(a)*r*.77
            c.line([(x,y),(px,py)],INK,3)
            c.oval(px,py,r*.13,r*.13,INK,0)
        c.oval(x,y,r*.25,r*.25,INK,0)
    elif kind=='whistle':
        c.oval(x-r*.35,y,r*.53,r*.53,accent)
        c.box((x-r*.26,y-r*.30,x+r*.9,y+r*.24),accent,8)
        c.oval(x-r*.46,y,r*.17,r*.17,INK,0)
    elif kind=='clock':
        c.oval(x,y,r*.84,r*.84,WHITE)
        c.box((x-r*.23,y-r,x+r*.23,y-r*.73),accent,5)
        a=f*.21
        c.line([(x,y),(x+math.cos(a)*r*.62,y+math.sin(a)*r*.62)],INK,4)
    elif kind=='net':
        c.box((x-r,y-r*.62,x+r,y+r*.62),accent,7)
        for j in (-.65,-.31,0,.31,.65):
            c.line([(x+j*r,y-r*.57),(x+j*r,y+r*.57)],WHITE,3)
        for j in (-.34,0,.34):
            c.line([(x-r*.95,y+j*r),(x+r*.95,y+j*r)],WHITE,3)
    else:
        c.shape([(x-r*.62,y-r*.45),(x+r*.62,y-r*.45),(x+r*.29,y+r*.2),(x+r*.12,y+r*.45),(x+r*.51,y+r*.65),(x-r*.51,y+r*.65),(x-r*.12,y+r*.45),(x-r*.29,y+r*.2)],accent)

def lower_third(c,lines):
    c.box((41,572,498,732),'#363454',22,4)
    c.text(270,610,lines,40)

def ticker(c,label,f):
    c.box((47,739,493,786),'#eac06d',12,3)
    c.text(270,762,[label],29,INK,0)
    x=56+(f*4)%425
    c.line([(x,778),(min(481,x+22),778)],WHITE,3)

def counter(start,end,t):
    return round(start+(end-start)*back(t))

def poll_bars(c,values,f):
    for i, value in enumerate(values):
        y=505+i*109
        c.box((65,y,475,y+55),WHITE)
        c.box((65,y,66+409*clamp(value),y+55),['#ec7b81','#93d5c7'][i],14)
        c.oval(77+7*math.sin(f*.3),y+28,7,7,INK,0)

def bubble(c,lines):
    c.shape([(120,409),(141,457),(177,409)],WHITE)
    c.box((51,252,489,421),WHITE,23)
    c.text(270,300,lines,43,INK,0)

def particles(c,f,x,y,strong=False):
    for i in range(8 if strong else 5):
        phase=(f*3.3+i*19)%106
        px=x+(i%2*2-1)*(34+phase)
        py=y-75+i*26+(phase*.32)
        r=2+i%3
        c.line([(px-r,py+r),(px+r,py-r)],'#ffda77',3)

def transition(c,f,n,entrance,exit,base,accent):
    incoming=f<=6
    if not incoming and f<=n-6:return
    q=(6-f)/6 if incoming else (f-(n-6))/6
    kind=entrance if incoming else exit
    if kind in ('ink-splash','whistle-pop'):
        radius=math.ceil(620*q)
        if radius:c.oval(270,452,radius,radius*.98,accent,0)
    elif kind=='ball-roll':
        if q:
            edge=540*q
            c.shape([(0,0),(edge,0),(edge,960),(0,960)],accent,0)
            icon(c,'ball',edge,460,55,f)
    elif kind=='camera-flash':
        inset=math.ceil(480*q)
        if inset:
            c.box((0,0,540,inset),WHITE,0,0)
            c.box((0,960-inset,540,960),WHITE,0,0)
    elif kind=='scribble-swipe':
        if q:
            for j in range(15):
                x=540-570*q
                y=j*68
                c.line([(x,y),(x+max(8,18*q),y+68),(600,y+4)],accent,74)
    elif kind in ('turf-slide','page-turn'):
        y=math.ceil(960*q)
        if y:c.shape([(0,0),(540,0),(540,y-40),(0,y)],accent,0)
    else:
        for i in range(8):
            x=540-(600*q)+i*69
            c.shape([(x,0),(x+55,0),(x+127,960),(x+73,960)],accent if i%2 else base,0)
