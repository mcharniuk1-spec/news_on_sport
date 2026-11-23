import os, re, shutil, subprocess
H="~/.npm/_npx/0865b412d54fa5ea/node_modules/.bin/hyperframes"
B="../brand"
body=open(f"{B}/mark-body.svg").read(); lines=open(f"{B}/mark-lines.svg").read()
inner=lambda s: re.sub(r'^<svg[^>]*>|</svg>$','',s.strip())
b=inner(body); b=re.sub(r'<title>.*?</title>','',b); b=re.sub(r'<rect width="256" height="256"[^>]*/>','',b,count=1)  # cut out only the tile background
l=re.sub(r'<title>.*?</title>','',inner(lines))
logo=f'<svg id="logo" xmlns="http://www.w3.org/2000/svg" viewBox="9.8 54 224.2 148" width="760" height="502"><g id="lines">{l}</g><g id="ball">{b}</g></svg>'
open("logo_mark.svg","w").write(logo)
CSS="""
:root{--navy:#0d1b32;--navy2:#14284a;--amber:#ffc247;--teal:#087f78;--pitch:#169b58}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1920px;overflow:hidden;background:var(--navy)}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:'Inter','Helvetica Neue',Arial,sans-serif;color:#fff;
 background:radial-gradient(ellipse 90% 55% at 50% 42%,#1b3a68 0%,var(--navy2) 38%,var(--navy) 78%)}
.arc{position:absolute;left:50%;top:790px;width:1500px;height:1500px;margin:-750px 0 0 -750px;border-radius:50%;border:3px solid rgba(255,194,71,.16)}
.arc.b{width:980px;height:980px;margin:-490px 0 0 -490px;border-color:rgba(8,127,120,.35)}
.grain{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.018) 0 2px,transparent 2px 6px)}
.mark{position:absolute;left:160px;top:560px;width:760px;height:502px}
.name{position:absolute;left:0;width:1080px;top:1160px;text-align:center;font-weight:900;font-size:108px;letter-spacing:-1px;line-height:1}
.name span{color:var(--amber)}
.tag{position:absolute;left:0;width:1080px;top:1310px;text-align:center;font-weight:800;font-size:40px;letter-spacing:.1em;color:#c9d6ea}
.cta{position:absolute;left:190px;width:700px;top:1440px;height:120px;border-radius:60px;background:var(--amber);color:var(--navy);font-weight:900;font-size:46px;display:flex;align-items:center;justify-content:center;box-shadow:0 18px 50px rgba(255,194,71,.35)}
.age{position:absolute;left:0;width:1080px;top:1640px;text-align:center;font-size:30px;font-weight:700;color:#8fa3ba;letter-spacing:.04em}
.vig{position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(0,0,0,0) 55%,rgba(0,0,0,.45) 100%)}
"""
html=f"""<!doctype html><html lang="en" data-resolution="portrait"><head><meta charset="UTF-8"/><meta name="viewport" content="width=1080, height=1920"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script><style>{CSS}</style></head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="2.8" data-width="1080" data-height="1920">
<div class="arc"></div><div class="arc b"></div><div class="grain"></div>
<div class="mark" id="mark">{logo}</div>
<div class="name" id="nm">about<span>football</span>.uk</div>
<div class="tag" id="tg">BETTING TIPS · MATCH NEWS · FORECASTS</div>
<div class="age">18+ · BeGambleAware.org · Gamble responsibly</div><div class="cta" id="cta">TIPS, NEWS, PREDICTIONS</div><div class="vig"></div></div>
<script>const tl=gsap.timeline({{paused:true}});
tl.from("#lines",{{x:-260,opacity:0,duration:.5,ease:"power3.out"}},0.15);
tl.from("#ball",{{x:240,rotation:-300,transformOrigin:"160px 128px",opacity:0,duration:.65,ease:"back.out(1.2)"}},0.05);
tl.from("#nm",{{y:60,opacity:0,duration:.45,ease:"power3.out"}},0.6);
tl.from("#tg",{{opacity:0,y:30,duration:.4}},0.85);
tl.from("#cta",{{scale:.6,opacity:0,duration:.45,ease:"back.out(1.6)"}},1.1);
tl.to("#cta",{{scale:1.04,duration:.5,yoyo:true,repeat:1,ease:"sine.inOut"}},1.7);
window.__timelines["main"]=tl;tl.seek(0);</script></body></html>"""
d="outro"; os.makedirs(d,exist_ok=True)
for f in ("package.json","hyperframes.json","meta.json"):
    if not os.path.exists(f"{d}/{f}"): shutil.copy(f"t0/{f}",f"{d}/{f}")
open(f"{d}/index.html","w").write(html)
os.makedirs("../clips",exist_ok=True)
r=subprocess.run([H,"render",d,"-o","../clips/hf_outro.mp4","-q","standard","-f","30"],capture_output=True,text=True,timeout=600)
print("rc",r.returncode,(r.stdout+r.stderr)[-300:].replace("\n"," "))
