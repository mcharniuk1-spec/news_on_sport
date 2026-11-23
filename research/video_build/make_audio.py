import numpy as np, wave
SR=44100
def save(name,x,gain=0.9):
    x=x/ max(1e-9,np.max(np.abs(x)))*gain
    w=wave.open(f"audio/{name}.wav","wb"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x*32767).astype(np.int16).tobytes()); w.close()
rng=np.random.default_rng(1)
def t(d): return np.arange(int(SR*d))/SR
# whoosh: noise, bandpass sweep via cumulative filtering (simple moving average with changing window approximated by amplitude env + lowpass)
d=0.5; n=rng.standard_normal(int(SR*d)); k=np.cumsum(n); 
x=n-np.convolve(n,np.ones(60)/60,'same'); env=np.sin(np.pi*t(d)/d)**2; save("whoosh",x*env)
# hit: sine drop + noise burst
d=0.6; tt=t(d); f=140*np.exp(-tt*9)+40; ph=2*np.pi*np.cumsum(f)/SR
x=np.sin(ph)*np.exp(-tt*5)+0.3*rng.standard_normal(len(tt))*np.exp(-tt*30); save("hit",x)
# glitch: stutter bursts
d=0.35; tt=t(d); x=np.sign(np.sin(2*np.pi*(800+3000*tt)*tt))*(np.sin(2*np.pi*40*tt)>0)*0.5; save("glitch",x)
# ding / airhorn-ish rise
d=0.8; tt=t(d); x=sum(np.sin(2*np.pi*f*tt) for f in (440,554,659))*np.exp(-tt*3); save("ding",x)
# sad trombone-ish (funny) 
d=1.2; tt=t(d); f=np.interp(tt,[0,.3,.6,1.2],[330,311,294,196]); x=np.sign(np.sin(2*np.pi*np.cumsum(f)/SR))*0.4*np.exp(-tt*1.2); x=np.convolve(x,np.ones(8)/8,'same'); save("womp",x)
# music: 140 bpm 4-on-floor + hat + bass, 18.6s
bpm=140; beat=60/bpm; D=18.6; m=np.zeros(int(SR*D))
def kick(): tt=t(0.25); f=120*np.exp(-tt*25)+45; return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-tt*10)
def hat(): tt=t(0.05); return rng.standard_normal(len(tt))*np.exp(-tt*80)*0.25
def bass(fr): tt=t(beat*0.9); return np.sign(np.sin(2*np.pi*fr*tt))*0.18*np.exp(-tt*3)
kk=kick(); hh=hat(); notes=[55,55,65.4,49]
b=0
while b*beat<D:
    s=int(b*beat*SR); m[s:s+len(kk)]+=kk[:len(m)-s]
    h=int((b+0.5)*beat*SR); 
    if h<len(m): m[h:h+len(hh)]+=hh[:len(m)-h]
    bs=bass(notes[(b//4)%4]); m[s:s+len(bs)]+=bs[:len(m)-s]
    b+=1
save("music",m,0.8)
print("ok")
