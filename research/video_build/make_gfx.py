from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
W,H=1080,1920
F="/System/Library/Fonts/Supplemental/Impact.ttf"
def burst(c1,c2,n=24):
    im=Image.new("RGB",(W,H),c1); d=ImageDraw.Draw(im); cx,cy=W//2,H//2
    for i in range(n):
        if i%2: continue
        a0=2*math.pi*i/n; a1=2*math.pi*(i+1)/n
        d.polygon([(cx,cy),(cx+2500*math.cos(a0),cy+2500*math.sin(a0)),(cx+2500*math.cos(a1),cy+2500*math.sin(a1))],fill=c2)
    return im
def outline(d,xy,fill,w=10,out=(10,10,10)):
    d.polygon(xy,fill=fill,outline=out,width=w)
# gen_01: cake with 46 candles
im=burst((255,214,10),(255,150,0)); d=ImageDraw.Draw(im)
d.rounded_rectangle((170,1000,910,1330),40,fill=(255,120,170),outline=(10,10,10),width=12)
d.rounded_rectangle((120,1250,960,1420),40,fill=(255,235,200),outline=(10,10,10),width=12)
for x in range(150,940,60): d.ellipse((x,985,x+70,1060),fill=(255,255,255),outline=(10,10,10),width=8)
for i,x in enumerate(range(220,880,66)):
    d.rectangle((x,800,x+26,1000),fill=(60,160,255),outline=(10,10,10),width=6)
    d.polygon([(x+13,700),(x-8,770),(x+13,790),(x+34,770)],fill=(255,70,20),outline=(10,10,10),width=5)
f=ImageFont.truetype(F,330); d.text((W//2,520),"46",font=f,anchor="mm",fill=(255,255,255),stroke_width=14,stroke_fill=(10,10,10))
f=ImageFont.truetype(F,70); d.text((W//2,1335),"PLACEHOLDER gen_01 (Codex replaces)",font=f,anchor="mm",fill=(10,10,10))
im.save("gfx/gen_01_cake.png")
# gen_02: slippers -> golden boots
im=burst((20,20,40),(60,20,120)); d=ImageDraw.Draw(im)
def shoe(x,y,col,toe=1.0,s=1.0):
    pts=[(x,y),(x+330*s,y),(x+330*s,y+90*s),(x+420*s,y+150*s*toe),(x+520*s,y+200*s),(x+520*s,y+260*s),(x,y+260*s)]
    d.polygon(pts,fill=col,outline=(10,10,10),width=10)
shoe(80,520,(150,110,80),0.8,0.7); d.text((250,880),"OLD",font=ImageFont.truetype(F,120),anchor="mm",fill=(255,255,255),stroke_width=8,stroke_fill=(10,10,10))
d.polygon([(480,700),(640,700),(640,640),(760,760),(640,880),(640,820),(480,820)],fill=(255,230,0),outline=(10,10,10),width=10)
shoe(560,1000,(255,205,30),1.0,1.5)
for i in range(7): d.rectangle((640+i*60,1010,660+i*60,1060),fill=(40,40,40))
d.text((W//2,1500),"GOLDEN BOOTS",font=ImageFont.truetype(F,170),anchor="mm",fill=(255,230,0),stroke_width=12,stroke_fill=(10,10,10))
d.text((W//2,1720),"PLACEHOLDER gen_02 (Codex replaces)",font=ImageFont.truetype(F,60),anchor="mm",fill=(255,255,255))
im.save("gfx/gen_02_boots.png")
# score card background: dark pitch
im=Image.new("RGB",(W,H),(8,30,18)); d=ImageDraw.Draw(im)
for i in range(0,H,160): d.rectangle((0,i,W,i+80),fill=(12,42,25))
d.ellipse((W//2-330,H//2-330,W//2+330,H//2+330),outline=(255,255,255),width=10); d.line((0,H//2,W,H//2),fill=(255,255,255),width=10)
im=im.filter(ImageFilter.GaussianBlur(2)); im.save("gfx/card_pitch.png")
print("ok")
