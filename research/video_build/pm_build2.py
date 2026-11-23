import json, mcp
P="515558C1"; TL="6317CE8E"; s=mcp.session(); f=lambda x: round(x*30)
base={"fontName":"Impact","italic":False,"fontCase":"uppercase","color":"#FFFFFF","alignment":"center",
 "outline":{"color":"#000000","width":16,"enabled":True},"shadow":{"enabled":True,"color":"#000000","opacity":0.7,"blur":6,"offset":{"x":0,"y":8}}}
def st(**k):
    d=json.loads(json.dumps(base)); d.update(k); return d
caps=[("RONALDINHO",0.0,0.9,100),("IS 46",0.9,1.8,170),("11 YEARS",1.8,2.6,130),("NO FOOTBALL",2.6,3.4,100),("A JOKE?!",3.45,4.6,140),
("THIRD\nDIVISION",4.6,6.1,110),("WHITE\nSHIRT",6.1,7.5,130),("FLARES",7.5,8.1,140),("SMOKE",8.1,8.6,140),("CHAOS",8.6,9.1,140),
("BRUTAL\nLEAGUE",9.1,10.6,120),("THEN...",10.6,11.8,150),("STILL\nGOT IT?",13.8,15.2,130),("RETIRED?\nNEVER.",15.2,16.6,105),("WHO'S NEXT?",16.6,17.5,105),("YOUR\nGRANDAD?",17.5,18.4,105)]
E=[{"content":c,"startFrame":f(a),"endFrame":f(b),"animation":"punchIn","style":st(fontSize=sz),"transform":{"x":0.5,"y":0.70}} for c,a,b,sz in caps]
# score card
E+= [{"content":"RAVENNA","startFrame":f(11.8),"endFrame":f(13.8),"animation":"slideUp","style":st(fontSize=105),"transform":{"x":0.5,"y":0.30}},
{"content":"2-0","startFrame":f(11.95),"endFrame":f(13.8),"animation":"popIn","style":st(fontSize=190,color="#FFD400",outline={"color":"#000000","width":20,"enabled":True}),"transform":{"x":0.5,"y":0.48}},
{"content":"FORLÌ","startFrame":f(12.1),"endFrame":f(13.8),"animation":"slideUp","style":st(fontSize=105),"transform":{"x":0.5,"y":0.66}},
{"content":"SERIE C","startFrame":f(12.4),"endFrame":f(13.8),"animation":"fadeIn","style":st(fontSize=80,color="#7CFF8A"),"transform":{"x":0.5,"y":0.78}},
{"content":"BREAKING","startFrame":0,"endFrame":f(3.4),"animation":"slideIn","style":st(fontSize=90,italic=False,background={"enabled":True,"color":"#E10600","opacity":1,"cornerRadius":10,"padding":{"x":40,"y":16}},outline={"color":"#000000","width":0,"enabled":False}),"transform":{"x":0.5,"y":0.1}},
{"content":"😂","startFrame":f(3.5),"endFrame":f(4.6),"animation":"popIn","style":{"fontSize":260},"transform":{"x":0.5,"y":0.3}},
{"content":"💀","startFrame":f(10.6),"endFrame":f(11.8),"animation":"popIn","style":{"fontSize":300},"transform":{"x":0.5,"y":0.35}},
{"content":"🔥","startFrame":f(8.1),"endFrame":f(9.1),"animation":"popIn","style":{"fontSize":240},"transform":{"x":0.8,"y":0.2}}]
r=mcp.call(s,"add_texts",{"projectId":P,"timelineId":TL,"entries":E}); print(json.dumps(r)[:1800])
