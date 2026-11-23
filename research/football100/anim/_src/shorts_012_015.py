"""Plan-led sequential PNG generation for Shorts 012–015."""
import sys
import shorts_004_010 as studio

studio.LOOKS.update({
    '012':('#c7d4ee','#454571','#ffd272','#e58699','#8ecfb3'),
    '013':('#efc7a6','#454168','#ffce75','#c779a3','#96c7be'),
    '014':('#bbd2d7','#3e4269','#f6cc71','#e6877a','#a7a5da'),
    '015':('#e9ccdf','#454374','#f7c36e','#c6819d','#96cda1'),
})
studio.HOOKS.update({
    '012':'Who’s taking the next penalty?',
    '013':'Is this really just a shirt?',
    '014':'Can you pick both sides?',
    '015':'Is Luka done yet?',
})
studio.COMICS.update({
    '012':[('net','ball','donut','card'),('office','door','clipboard','tag'),('cabinet','cup','cup','ball')],
    '013':[('runway','rack','shirt','tag'),('office','chair','chair','chair'),('office','note-box','envelope','tag')],
    '014':[('board','clipboard','eraser','mirror'),('door','flag','scarf','door'),('rack','shirt','shirt','shirt')],
    '015':[('scoreboard','cake','cake','flag'),('scoreboard','shirt','card','clock'),('calendar','suitcase','tag','boot')],
})
original=studio.prop
def prop(c,k,x,y,r,f,colors):
    _,dark,gold,warm,cool=colors
    def box(a,b,d,e,col,rr=8):c.box((x+a*r,y+b*r,x+d*r,y+e*r),col,rr)
    def oval(a,b,d,e,col,w=3):c.oval(x+a*r,y+b*r,d*r,e*r,col,w)
    def line(pts,col=studio.INK,w=4):c.line([(x+a*r,y+b*r) for a,b in pts],col,w)
    if k=='donut':
        oval(0,0,.82,.73,warm);oval(0,0,.27,.25,cool)
        for a,b in [(-.42,-.33),(.37,-.36),(.45,.22),(-.39,.36)]:
            line([(a,b),(a+.19,b+.06)],gold,5)
    elif k in ('door','office','mirror','note-box'):
        box(-.82,-.93,.84,.96,dark,14);box(-.65,-.79,.65,.79,cool)
        if k=='note-box':box(-.47,-.28,.47,-.11,dark)
        elif k=='mirror':line([(-.45,-.49),(-.2,-.68)],studio.WHITE,7)
        else:
            line([(0,-.7),(0,.73)],dark,5);oval(.16,.18,.09,.09,gold)
    elif k=='runway':
        c.shape([(x-r,y+r*.59),(x+r,y+r*.59),(x+.42*r,y-r*.56),(x-.42*r,y-r*.56)],warm)
        for j in (-.77,.77):oval(j,.42,.12,.10,gold)
    elif k in ('eraser','scarf'):
        box(-.63,-.31,.69,.27,warm)
        if k=='scarf':
            box(.35,.03,.69,.85,warm)
            for u in (-.44,-.13,.19,.50):line([(u,-.28),(u,.23)],gold,7)
    elif k=='cake':
        box(-.83,-.25,.84,.53,warm,16)
        oval(0,-.22,.84,.27,studio.WHITE)
        box(-.08,-.78,.09,-.26,gold,5)
        oval(.005,-.89,.09,.14,warm)
    elif k=='suitcase':
        box(-.26,-.64,.27,-.32,dark)
        box(-.79,-.40,.79,.51,warm,15)
        for u in (-.42,.42):line([(u,-.31),(u,.40)],gold,6)
    elif k=='boot':
        c.shape([(x-.68*r,y-r*.67),(x+.09*r,y-r*.55),(x+.17*r,y-r*.04),(x+.73*r,y+r*.06),(x+r*.76,y+r*.45),(x-.70*r,y+r*.44)],warm)
        for u in (-.32,-.1,.12):line([(u,-.31),(u+.14,-.12)],studio.WHITE,4)
    else:original(c,k,x,y,r,f,colors)
studio.prop=prop

if __name__=='__main__':
    for video in sys.argv[1:]:
        studio.main(video)
