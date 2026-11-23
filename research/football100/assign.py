import json, glob, collections, random, sqlite3
random.seed(7)
HERE="<PROJECT_ROOT>/research/football100"
news=json.load(open(f"{HERE}/news/news_dedup.json"))
bo=[json.load(open(f)) for f in sorted(glob.glob(f"{HERE}/bo/*.json"))]
items=[]
# 1) Ballon d'Or winners: 2 videos each (A = latest and biggest stories, B = roast/praise mix)
names=[p["name"] for p in bo if p["name"]!="Harry Kane"]+["Harry Kane"]
for n in names:
    items.append(dict(kind="bo",subject=n,part="A",ref=n,angle="bo",hint="newest stories"))
    items.append(dict(kind="bo",subject=n,part="B",ref=n,angle="bo",hint="roast and praise mix, different stories from part A"))
# 2) news videos: quota by angle, entity diversity
quota={"scandal":13,"transfer":13,"coach":11,"win":11,"viral":13,"record":6,"business":2,"history":1}
need=100-len(items); tot=sum(quota.values()); 
def score(x): return (x["n_sources"]*3+x["n_domains"]*2+(2 if x["date"]>="2026-11-01" else 0))
cand=[x for x in news if not x.get("sensitive") and x.get("confidence") in("high","medium")]
cand.sort(key=score,reverse=True)
ent=collections.Counter(); got=collections.Counter(); pick=[]
bonames={n.split()[-1].lower() for n in names}
for x in cand:
    a=x["angle"]; 
    if got[a]>=quota.get(a,0): continue
    e=(x["entities"] or ["?"])[0]
    if ent[e]>=2: continue
    if any(b in x["headline"].lower() for b in bonames): continue   # BO winners are covered above
    pick.append(x); got[a]+=1; ent[e]+=1
    if len(pick)>=need: break
for x in cand:
    if len(pick)>=need: break
    if x not in pick and not any(b in x["headline"].lower() for b in bonames): pick.append(x)
for x in pick: items.append(dict(kind="news",subject=x["headline"],part="",ref=x["id"],angle=x["angle"],hint=""))
items=items[:100]
for i,it in enumerate(items,1): it["no"]=i
# 3) voices: 33 ElevenLabs (3 voices x 11) spread over the list, rest Kokoro
el_idx=[i for i in range(100) if i%3==1][:33]
for i,it in enumerate(items): it["voice"]="kokoro"
for k,i in enumerate(el_idx): items[i]["voice"]=["EL_A","EL_B","EL_C"][k%3]
# 4) comic videos: 40 Kokoro + 9 EL (3 per voice) chosen by comic potential
pot={"viral":9,"scandal":8,"bo":8,"transfer":6,"coach":6,"win":5,"record":4,"history":3,"business":2}
for it in items: it["pot"]=pot.get(it["angle"],3)+random.random()
kok=sorted([it for it in items if it["voice"]=="kokoro"],key=lambda z:-z["pot"])[:40]
for v in ("EL_A","EL_B","EL_C"):
    for it in sorted([z for z in items if z["voice"]==v],key=lambda z:-z["pot"])[:3]: it["comic"]=True
for it in kok: it["comic"]=True
styles=[("simpsons",15),("southpark_cutout",8),("shonen_anime",6),("us_comic_book",6),("looney_slapstick",5),("rickmorty_like",3),("peanuts_minimal",3),("ligne_claire",3)]
pref={"scandal":["southpark_cutout","simpsons"],"viral":["looney_slapstick","rickmorty_like","simpsons"],"win":["shonen_anime","us_comic_book"],
      "coach":["simpsons","peanuts_minimal"],"transfer":["us_comic_book","ligne_claire","simpsons"],"bo":["simpsons","us_comic_book","shonen_anime","looney_slapstick"],
      "record":["shonen_anime","us_comic_book"],"history":["ligne_claire","peanuts_minimal"],"business":["rickmorty_like","simpsons"]}
left=dict(styles)
for it in [z for z in items if z.get("comic")]:
    for s in pref.get(it["angle"],["simpsons"])+[k for k in left]:
        if left.get(s,0)>0: it["style"]=s; left[s]-=1; break
for it in items: it["comic"]=bool(it.get("comic")); it["limit_chars"]=600 if it["voice"].startswith("EL") else 1100
json.dump(items,open(f"{HERE}/scripts/assign.json","w"),indent=1,ensure_ascii=False)
c=collections.Counter(it["voice"] for it in items); print(len(items),dict(c),"comic",sum(it["comic"] for it in items),"comicEL",sum(1 for it in items if it["comic"] and it["voice"]!="kokoro"))
print(collections.Counter(it.get("style") for it in items if it["comic"])); print(collections.Counter(it["angle"] for it in items))
