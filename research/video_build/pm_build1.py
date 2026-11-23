import json, mcp
P="515558C1"; TL="6317CE8E"
M={"c01":"40E48735","c02":"517F3772","c04":"B7843925","c05":"BD76CD7E","c06":"3E20B80A","c07":"2E73DBDA","c08":"A3D45B4C","c10":"54248F02","c12":"71B7162F","gen1":"AEFDCE86","gen2":"90B1FB55","card":"9A204F31",
 "ding":"2176579E","glitch":"2184E237","hit":"A02BC4FE","music":"2791BF6A","vo1":"02F33D76","vo2":"C6838CA5","vo3":"AB1B7D19","vo4":"A4DA5FB8","vo5":"62EE63A3","vo6":"EFAC6469","vo7":"6CE5EB2D","vo8":"052E4258","vo9":"357CD786","whoosh":"3E07987D","womp":"462FDA86"}
f=lambda s:round(s*30)
shots=[("c01",0.0,1.8),("c02",1.8,3.4),("gen1",3.4,4.6),("c04",4.6,6.1),("c05",6.1,7.5),("c06",7.5,9.1),("c07",9.1,10.6),("c08",10.6,11.8),("card",11.8,13.8),("c10",13.8,15.2),("gen2",15.2,16.6),("c12",16.6,18.4)]
s=mcp.session()
V=[{"mediaRef":M[n],"startFrame":f(a),"endFrame":f(b),"trackIndex":0,"includeAudio":False} for n,a,b in shots]
def show(r): print(json.dumps(r)[:700])
show(mcp.call(s,"add_clips",{"projectId":P,"timelineId":TL,"entries":V}))
sfx=[(0.0,"hit"),(1.65,"whoosh"),(3.5,"womp"),(5.95,"whoosh"),(7.4,"glitch"),(9.0,"hit"),(10.45,"whoosh"),(11.7,"hit"),(13.65,"whoosh"),(15.1,"ding"),(16.5,"whoosh")]
vo=[(0.1,"vo1"),(1.9,"vo2"),(3.45,"vo3"),(4.7,"vo4"),(7.5,"vo5"),(9.2,"vo6"),(11.9,"vo7"),(15.3,"vo8"),(16.7,"vo9")]
for lst in ([(0.0,"music")],vo,sfx):
    show(mcp.call(s,"add_clips",{"projectId":P,"timelineId":TL,"entries":[{"mediaRef":M[n],"startFrame":f(t)} for t,n in lst]}))
