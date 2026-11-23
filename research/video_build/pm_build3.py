import json, mcp
P="515558C1"; TL="6317CE8E"; s=mcp.session()
def c(name,a): 
    r=mcp.call(s,name,{"projectId":P,"timelineId":TL,**a}); t=r["result"]["content"][0]["text"]; print(name,("ERR " if r["result"].get("isError") else "ok  ")+t[:220]); return t
vid={"c01":("D1F6E13B",54),"c02":("5BAB75F6",48),"gen1":("ED632FD6",36),"c04":("28A56542",45),"c05":("FDE15973",42),"c06":("B4F52436",48),"c07":("9E2626AD",45),"c08":("7DE3A952",36),"card":("F8E5F3F9",60),"c10":("64FBA4C4",42),"gen2":("800B15E6",42),"c12":("A06851EC",54)}
ids=[v[0] for v in vid.values()]
c("apply_effect",{"clipIds":ids,"effects":[{"type":"stylize.grain","params":{"amount":0.22,"size":1.6}},{"type":"stylize.vignette","params":{"amount":0.35}},{"type":"blur.sharpen","params":{"amount":0.6}}]})
c("apply_effect",{"clipIds":[vid["c06"][0],vid["c12"][0],vid["gen1"][0]],"effects":[{"type":"stylize.glow","params":{"intensity":0.45,"radius":30,"threshold":0.55,"warmth":0.4}}]})
c("apply_effect",{"clipIds":[vid["c07"][0]],"effects":[{"type":"blur.motion","params":{"radius":6,"angle":0}}]})
real=[vid[k][0] for k in ("c01","c02","c04","c05","c06","c07","c08","c10","c12")]
c("apply_color",{"clipIds":real,"contrast":1.14,"saturation":1.18})
# zoom punches
for i,(k,(cid,d)) in enumerate(vid.items()):
    z0,z1=(1.0,1.2) if i%2==0 else (1.2,1.0)
    p=lambda z:(1-z)/2
    c("set_keyframes",{"clipId":cid,"property":"scale","keyframes":[[0,z0,z0],[d,z1,z1]]})
    c("set_keyframes",{"clipId":cid,"property":"position","keyframes":[[0,p(z0),p(z0)],[d,p(z1),p(z1)]]})
# shake on tackle + flares
c("set_keyframes",{"clipId":vid["c07"][0],"property":"rotation","keyframes":[[0,0,"hold"],[6,-2.5,"hold"],[9,2.5,"hold"],[12,-2,"hold"],[15,1.5,"hold"],[18,0,"hold"]]})
# flash matte
t=c("import_media",{"source":{"matte":{"hex":"#FFFFFF"}}})
