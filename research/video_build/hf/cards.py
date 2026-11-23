import os, shutil, subprocess, sys, json
H="~/.npm/_npx/0865b412d54fa5ea/node_modules/.bin/hyperframes"
CSS="""
:root{--ground:#07140c;--ink:#fff;--y:#FFD400;--g:#18c964;--red:#ff3b30}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--ground)}
#root{position:relative;width:1080px;height:1920px;font-family:Impact,'Arial Black',sans-serif;color:var(--ink);text-transform:uppercase;overflow:hidden;
 background:repeating-linear-gradient(0deg,#0b2214 0 120px,#0e2a19 120px 240px)}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,0) 40%,rgba(0,0,0,.65) 100%)}
.abs{position:absolute;left:0;width:1080px;text-align:center}
.big{font-size:230px;line-height:1;color:var(--y);-webkit-text-stroke:10px #000;paint-order:stroke fill}
.mid{font-size:100px;line-height:1.05;-webkit-text-stroke:8px #000;paint-order:stroke fill}
.small{font-size:60px;-webkit-text-stroke:6px #000;paint-order:stroke fill;color:#cfe}
.row{position:absolute;left:90px;width:900px;height:130px;border-radius:20px;background:#0a0a0a;border:6px solid var(--y);display:flex;align-items:center;padding:0 36px;font-size:62px}
.row b{color:var(--y);margin-left:auto;font-size:54px}
.tier{position:absolute;left:140px;width:800px;height:210px;border-radius:24px;background:#10331e;border:6px solid #2d6b45;display:flex;align-items:center;justify-content:center;font-size:84px}
.stamp{position:absolute;left:90px;width:900px;text-align:center;font-size:76px;line-height:1.05;color:#000;background:var(--y);padding:26px 20px;border-radius:18px;transform:rotate(-3deg)}
"""
def page(body,js,dur):
    return f"""<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script><style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">{body}<div class="vig"></div></div>
<script>const tl=gsap.timeline({{paused:true}});
function counter(sel,to,start,dur,fmt){{const o={{v:0}};const el=document.querySelector(sel);tl.to(o,{{v:to,duration:dur,ease:"power2.out",onUpdate:()=>{{el.textContent=fmt?fmt(o.v):Math.round(o.v)}}}},start)}}
{js}
window.__timelines["main"]=tl;tl.seek(0);</script></body></html>"""
def build(name,body,js,dur):
    d=f"{name}"; os.makedirs(d,exist_ok=True)
    for f in ("package.json","hyperframes.json","meta.json"):
        if not os.path.exists(f"{d}/{f}"): shutil.copy(f"t0/{f}",f"{d}/{f}")
    open(f"{d}/index.html","w").write(page(body,js,dur))
    r=subprocess.run([H,"render",d,"-o",f"../clips/hf_{name}.mp4","-q","standard","-f","30"],capture_output=True,text=True,timeout=600)
    print(name,"rc",r.returncode,(r.stdout+r.stderr)[-300:].replace("\n"," "))
cards={}
# R1 trophies
rows=["WORLD CUP|2002","COPA AMÉRICA|","CONFEDERATIONS CUP|","CHAMPIONS LEAGUE|2006","COPA LIBERTADORES|2013","BALLON D'OR|2005"]
body="".join(f'<div class="row" id="r{i}" style="top:{330+i*165}px;opacity:0"><span>{a}</span><b>{b}</b></div>' for i,(a,b) in enumerate(x.split("|") for x in rows))
body+='<div class="abs mid" style="top:150px">THE FULL SET</div><div class="stamp" id="st" style="top:1400px;opacity:0">ONLY PLAYER IN HISTORY TO WIN ALL SIX</div>'
js="".join(f'tl.fromTo("#r{i}",{{x:-1200,opacity:1}},{{x:0,duration:.35,ease:"back.out(1.4)"}},{0.3+i*0.55});' for i in range(6))
js+='tl.fromTo("#st",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.3,ease:"power4.out"},4.0);'
cards["trophies"]=(body,js,6)
# R2 youth
body='<div class="abs mid" style="top:240px">AGE</div><div class="abs big" id="age" style="top:340px;font-size:330px">0</div><div class="abs mid" style="top:760px" id="l1">HE SCORED</div><div class="abs big" id="goals" style="top:870px;font-size:420px">0</div><div class="abs mid" style="top:1330px" id="l2">GOALS IN A 23–0 WIN</div><div class="abs small" style="top:1520px" id="l3">"RONALDINHO" = "LITTLE RONALDO"</div>'
js='tl.from("#age",{scale:3,opacity:0,duration:.3,ease:"power4.out"},0.2);counter("#age",13,0.2,0.5);tl.from("#l1",{opacity:0,y:60,duration:.3},1.2);tl.from("#goals",{scale:2.5,opacity:0,duration:.3,ease:"power4.out"},1.5);counter("#goals",23,1.5,1.6);tl.from("#l2",{opacity:0,y:60,duration:.3},2.0);tl.from("#l3",{opacity:0,duration:.4},3.6);'
cards["youth"]=(body,js,5.2)
# R3 pyramid
body='<div class="abs mid" style="top:170px">ITALIAN FOOTBALL</div><div class="tier" id="t1" style="top:430px;opacity:0">SERIE A</div><div class="tier" id="t2" style="top:690px;opacity:0">SERIE B</div><div class="tier" id="t3" style="top:950px;opacity:0;background:#FFD400;color:#000;border-color:#000">SERIE C</div><div class="abs mid" id="pin" style="top:1210px;opacity:0">▲ RAVENNA</div><div class="abs small" id="ln" style="top:1380px;opacity:0">ITALY\'S THIRD DIVISION</div>'
js='tl.fromTo("#t1",{x:-1200,opacity:1},{x:0,duration:.35},0.2);tl.fromTo("#t2",{x:1200,opacity:1},{x:0,duration:.35},0.6);tl.fromTo("#t3",{x:-1200,opacity:1},{x:0,duration:.35,ease:"back.out(1.6)"},1.0);tl.fromTo("#pin",{y:80,opacity:0},{y:0,opacity:1,duration:.35},1.7);tl.fromTo("#ln",{opacity:0},{opacity:1,duration:.4},2.2);'
cards["pyramid"]=(body,js,4)
# R4 timeline
body='<div class="abs mid" style="top:170px">LAST PRO CLUB</div><div class="abs small" id="a1" style="top:330px;opacity:0;color:#fff">2015 · FLUMINENSE · 9 GAMES</div><div class="abs small" id="a2" style="top:430px;opacity:0;color:#fff">2018 · RETIRED</div><div class="abs small" id="a3" style="top:530px;opacity:0;color:var(--y)">2026 · RAVENNA</div><div class="abs big" id="yrs" style="top:760px;font-size:520px">0</div><div class="abs mid" id="yl" style="top:1340px;opacity:0">YEARS WITHOUT A PRO MATCH</div>'
js='tl.fromTo("#a1",{opacity:0,x:-200},{opacity:1,x:0,duration:.3},0.2);tl.fromTo("#a2",{opacity:0,x:-200},{opacity:1,x:0,duration:.3},0.9);tl.fromTo("#a3",{opacity:0,x:-200},{opacity:1,x:0,duration:.3},1.6);tl.from("#yrs",{scale:2.5,opacity:0,duration:.3,ease:"power4.out"},2.2);counter("#yrs",11,2.2,1.2);tl.to("#yl",{opacity:1,duration:.3},3.0);'
cards["years"]=(body,js,4.6)
# R5 score
body='<div class="abs mid" style="top:260px" id="h">RAVENNA</div><div class="abs big" id="sc" style="top:520px;font-size:420px">0–0</div><div class="abs mid" style="top:1080px" id="a">FORLÌ</div><div class="abs small" style="top:1330px;color:var(--g)" id="s">SERIE C · MATCHDAY 14</div>'
js='tl.from("#h",{y:-100,opacity:0,duration:.3},0.1);tl.from("#a",{y:100,opacity:0,duration:.3},0.2);tl.from("#sc",{scale:2.6,opacity:0,duration:.3,ease:"power4.out"},0.35);tl.call(()=>{document.getElementById("sc").textContent="1–0"},[],1.0);tl.call(()=>{document.getElementById("sc").textContent="2–0"},[],1.7);tl.fromTo("#sc",{scale:1.25},{scale:1,duration:.25,ease:"power3.out"},1.7);tl.from("#s",{opacity:0,duration:.4},0.9);'
cards["score"]=(body,js,3.6)
# M2 transfer
body='<div class="abs small" style="top:210px;color:#fff">SHAKHTAR → CHELSEA · JAN 2023</div><div class="abs big" id="n" style="top:360px;font-size:430px">€0M</div><div class="abs mid" id="b" style="top:900px;opacity:0">£62M UP FRONT</div><div class="abs mid" id="c" style="top:1050px;opacity:0;color:var(--y)">UP TO €100M</div><div class="stamp" id="st" style="top:1360px;opacity:0">MOST EXPENSIVE UKRAINIAN EVER</div>'
js='tl.from("#n",{scale:2.5,opacity:0,duration:.3,ease:"power4.out"},0.2);counter("#n",70,0.2,1.3,v=>"€"+Math.round(v)+"M");tl.to("#b",{opacity:1,duration:.3},1.5);tl.to("#c",{opacity:1,duration:.3},2.0);tl.fromTo("#st",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.3,ease:"power4.out"},2.7);'
cards["transfer"]=(body,js,4.4)
# M3 timeline
body='<div class="abs mid" style="top:170px">THE LONG WAIT</div><div class="abs small" id="a1" style="top:350px;opacity:0;color:#fff">17 DEC 2024 · PROVISIONALLY SUSPENDED</div><div class="abs small" id="a2" style="top:470px;opacity:0;color:#fff">31 JUL 2026 · ALL CHARGES DROPPED</div><div class="abs small" id="a3" style="top:590px;opacity:0;color:var(--y)">1 SEP 2026 · LOAN TO TOTTENHAM</div><div class="abs big" id="d" style="top:800px;font-size:430px">0</div><div class="abs mid" id="dl" style="top:1300px;opacity:0">DAYS BETWEEN COMPETITIVE MATCHES</div>'
js='tl.fromTo("#a1",{opacity:0,x:-200},{opacity:1,x:0,duration:.3},0.2);tl.fromTo("#a2",{opacity:0,x:-200},{opacity:1,x:0,duration:.3},0.9);tl.fromTo("#a3",{opacity:0,x:-200},{opacity:1,x:0,duration:.3},1.6);tl.from("#d",{scale:2.5,opacity:0,duration:.3,ease:"power4.out"},2.2);counter("#d",646,2.2,1.6);tl.to("#dl",{opacity:1,duration:.3},3.2);'
cards["wait"]=(body,js,5)

# P1 stats
body='<div class="abs mid" style="top:150px">PORTUGAL CAREER</div><div class="abs big" id="c" style="top:300px;font-size:380px">0</div><div class="abs mid" id="cl" style="top:700px;opacity:0">CAPS</div><div class="abs big" id="g" style="top:900px;font-size:380px">0</div><div class="abs mid" id="gl" style="top:1300px;opacity:0">GOALS</div><div class="stamp" id="st" style="top:1500px;opacity:0">BOTH WORLD RECORDS</div>'
js='tl.from("#c",{scale:2.5,opacity:0,duration:.3,ease:"power4.out"},0.2);counter("#c",234,0.2,1.3);tl.to("#cl",{opacity:1,duration:.3},1.0);tl.from("#g",{scale:2.5,opacity:0,duration:.3,ease:"power4.out"},1.6);counter("#g",146,1.6,1.3);tl.to("#gl",{opacity:1,duration:.3},2.4);tl.fromTo("#st",{scale:2.4,opacity:0},{scale:1,opacity:1,duration:.3,ease:"power4.out"},3.2);'
cards["stats"]=(body,js,4.4)
# P2 seven
body='<div class="abs small" style="top:200px;color:#fff" id="a">5 NOV 2026</div><div class="abs big" id="s" style="top:330px;font-size:900px">7</div><div class="abs mid" id="b" style="top:1330px;opacity:0">HANDED BACK</div>'
js='tl.from("#a",{opacity:0,y:-40,duration:.3},0.1);tl.from("#s",{scale:3,opacity:0,rotation:-12,duration:.4,ease:"power4.out"},0.3);tl.to("#s",{rotation:4,scale:0.94,duration:1.4,ease:"sine.inOut"},0.8);tl.to("#b",{opacity:1,duration:.3},1.6);'
cards["seven"]=(body,js,3.0)
only=sys.argv[1:] or list(cards)
for k in only: build(k,*cards[k])
