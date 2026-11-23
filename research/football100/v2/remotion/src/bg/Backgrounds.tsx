// BACKGROUNDS (>= 14): full-bleed 1080x1920 scenery in theme colours, always drifting (crowd bobs, clouds, lights, windows).
// <Background kind="stadium" shift={0} tint? />.  Add one: add the name to core/vocab.ts BGS and a function to BG below.
import React from 'react';
import {useScene} from '../core/ctx';
import {mix, shade, alpha} from '../core/color';
import {osc, TAU} from '../core/ease';
import {rand01} from '../core/rng';
import type {Palette} from '../theme/themes';

interface B { pal: Palette; t: number; sh: number; seed: number; line: number }
const W = 1080, H = 1920;

const Grad: React.FC<{ id: string; a: string; b: string; y0?: number; y1?: number }> = ({ id, a, b, y0 = 0, y1 = 1 }) => (
  <defs><linearGradient id={id} x1="0" y1={y0} x2="0" y2={y1}><stop offset="0" stopColor={a} /><stop offset="1" stopColor={b} /></linearGradient></defs>
);
const Cloud: React.FC<{ x: number; y: number; s: number; c: string }> = ({ x, y, s, c }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`} fill={c}><ellipse cx="0" cy="0" rx="90" ry="38" /><ellipse cx="-50" cy="12" rx="60" ry="30" /><ellipse cx="56" cy="14" rx="64" ry="28" /><ellipse cx="10" cy="-26" rx="52" ry="34" /></g>
);
const Clouds: React.FC<B & { y?: number; c?: string; n?: number }> = ({ t, seed, pal, y = 380, c, n = 4 }) => (
  <g opacity=".9">{[...Array(n)].map((_, i) => { const sp = 14 + i * 5; const x = ((rand01(seed, i) * 1400 + t * sp) % 1500) - 200; return <Cloud key={i} x={x} y={y + (i % 3) * 120 + rand01(seed, i + 9) * 60} s={0.9 + (i % 3) * 0.35} c={c || alpha(pal.white, 0.85)} />; })}</g>
);
const Crowd: React.FC<{ y: number; rows: number; gap: number; r: number; a: string; b: string; t: number; seed: number; ink: string; amp?: number }> = ({ y, rows, gap, r, a, b, t, seed, ink, amp = 5 }) => {
  const cols = Math.ceil(W / gap) + 2;
  const els: React.ReactNode[] = [];
  for (let j = 0; j < rows; j++) for (let i = 0; i < cols; i++) {
    const k = rand01(seed, i * 7 + j * 131);
    const bob = Math.sin(t * (2.2 + k * 2.5) + k * 20) * amp * (0.4 + k) - Math.max(0, Math.sin(i * 0.32 - t * 3.2 + j * 0.25)) * amp * 2.6; // + travelling crowd wave
    els.push(<g key={`${i}-${j}`} transform={`translate(${i * gap + (j % 2) * gap / 2 - gap} ${y + j * gap * 0.82 + bob})`}><circle r={r} fill={k > 0.5 ? a : b} /><circle cy={-r * 0.9} r={r * 0.62} fill={mix(k > 0.5 ? a : b, '#fff', 0.35)} /></g>);
  }
  return <g>{els}</g>;
};
const Flood: React.FC<{ x: number; y: number; t: number; pal: Palette; s?: number }> = ({ x, y, t, pal, s = 1 }) => (
  <g transform={`translate(${x} ${y}) scale(${s})`}><rect x="-7" y="0" width="14" height={500} fill={shade(pal.ink, -0.3)} /><rect x="-60" y="-70" width="120" height="76" rx="10" fill={pal.ink} />{[...Array(6)].map((_, i) => <circle key={i} cx={-42 + (i % 3) * 42} cy={-50 + Math.floor(i / 3) * 34} r="11" fill={pal.white} opacity={0.75 + 0.25 * osc(t, 1.6, i * 0.13)} />)}<ellipse cx="0" cy="-30" rx="150" ry="100" fill={pal.white} opacity={0.12 + 0.05 * osc(t, 1, x)} /></g>
);
const Stripes: React.FC<{ y0: number; y1: number; a: string; b: string; t: number; n?: number; persp?: number }> = ({ y0, y1, a, b, t, n = 9, persp = 1.5 }) => {
  // mow-stripes in perspective: bands wider near the bottom; slowly scrolling
  const out: React.ReactNode[] = [];
  const drift = (t * 0.06) % 2;
  for (let i = -1; i < n; i++) {
    const f0 = Math.pow(Math.max(0, (i + drift) / n), persp), f1 = Math.pow(Math.max(0, (i + 1 + drift) / n), persp);
    const yA = y0 + (y1 - y0) * Math.max(0, f0), yB = y0 + (y1 - y0) * Math.min(1, f1);
    if (yB <= y0) continue;
    out.push(<rect key={i} x="0" y={yA} width={W} height={yB - yA + 1} fill={((i % 2) + 2) % 2 ? a : b} />);
  }
  return <g>{out}</g>;
};
const Windows: React.FC<{ x: number; y: number; cols: number; rows: number; w: number; h: number; gx: number; gy: number; on: string; off: string; t: number; seed: number; p?: number }> = ({ x, y, cols, rows, w, h, gx, gy, on, off, t, seed, p = 0.5 }) => (
  <g>{[...Array(rows)].flatMap((_, r) => [...Array(cols)].map((__, c) => { const k = rand01(seed, r * 31 + c); const lit = k < p || (Math.sin(t * 0.8 + k * 40) > 0.96); return <rect key={r + '-' + c} x={x + c * gx} y={y + r * gy} width={w} height={h} rx="3" fill={lit ? on : off} />; }))}</g>
);
const Spot: React.FC<{ x: number; t: number; c: string; sp?: number; w?: number }> = ({ x, t, c, sp = 0.5, w = 220 }) => {
  const a = 14 * Math.sin(t * sp + x);
  return <g transform={`translate(${x} -40) rotate(${a})`} opacity=".16"><path d={`M -20 0 L 20 0 L ${w} 1500 L ${-w} 1500 Z`} fill={c} /></g>;
};

export const BG: Record<string, (b: B) => React.ReactElement> = {
  stadium: ({ pal, t, sh, seed, line }) => (
    <g>
      <Grad id="stSky" a={pal.skyTop} b={pal.skyBot} />
      <rect width={W} height="1100" fill="url(#stSky)" />
      <Clouds t={t} seed={seed} pal={pal} y={300} n={3} />
      <g transform={`translate(${sh * 0.3} 0)`}><Flood x={120} y={430} t={t} pal={pal} /><Flood x={960} y={430} t={t} pal={pal} /></g>
      <path d="M -20 760 L 1100 760 L 1100 1120 L -20 1120 Z" fill={shade(pal.wallDark, 0.35)} />
      <g transform={`translate(${sh * 0.6} 0)`}><Crowd y={800} rows={5} gap={52} r={20} a={pal.crowdA} b={pal.crowdB} t={t} seed={seed} ink={pal.ink} /></g>
      <rect y="1080" width={W} height="46" fill={pal.wallDark} /><rect y="1080" width={W} height="10" fill={mix(pal.wallDark, '#fff', 0.3)} />
      {[...Array(6)].map((_, i) => <rect key={i} x={i * 190 + ((t * 40) % 190) - 190} y="1086" width="95" height="34" fill={i % 2 ? pal.accent : pal.accent2} opacity=".85" />)}
      <rect y="1126" width={W} height={H - 1126} fill={pal.grassA} />
      <Stripes y0={1126} y1={H} a={pal.grassA} b={pal.grassB} t={t} n={7} />
      <path d={`M 0 1480 L ${W} 1480`} stroke="#fff" strokeWidth="8" opacity=".6" /><ellipse cx="540" cy="1460" rx="360" ry="90" fill="none" stroke="#fff" strokeWidth="8" opacity=".5" />
      {[...Array(14)].map((_, i) => <circle key={i} cx={rand01(seed, i + 50) * W} cy={780 + rand01(seed, i + 60) * 240} r="5" fill="#fff" opacity={Math.max(0, osc(t, 1.4, rand01(seed, i))) * 0.9} />)}
    </g>
  ),
  pitch: ({ pal, t, sh, seed }) => (
    <g>
      <Grad id="piSky" a={pal.skyTop} b={pal.skyBot} />
      <rect width={W} height="720" fill="url(#piSky)" /><Clouds t={t} seed={seed} pal={pal} y={260} n={3} />
      <path d="M -20 700 Q 300 620 540 650 Q 800 610 1100 700 L 1100 760 L -20 760 Z" fill={mix(pal.grassB, pal.skyBot, 0.4)} />
      <rect y="720" width={W} height={H - 720} fill={pal.grassA} />
      <Stripes y0={720} y1={H} a={pal.grassA} b={pal.grassB} t={t} n={9} persp={1.7} />
      <g stroke="#fff" strokeWidth="9" fill="none" opacity=".7"><path d="M 140 1000 L 940 1000 L 1100 1500 L -20 1500 Z" /><path d="M 330 880 L 750 880 L 820 1000 L 260 1000 Z" /><ellipse cx="540" cy="1400" rx="380" ry="120" /><path d="M -20 1250 L 1100 1250" /></g>
      <g transform={`translate(${sh * 0.2} 0)`}><rect x="380" y="738" width="320" height="10" fill="#fff" opacity=".8" /><path d="M 380 748 L 380 880 M 700 748 L 700 880" stroke="#fff" strokeWidth="9" opacity=".8" /></g>
    </g>
  ),
  tunnel: ({ pal, t, sh, seed }) => {
    const pulse = 0.85 + 0.15 * osc(t, 0.9);
    return (<g>
      <rect width={W} height={H} fill={shade(pal.floor, 0.4)} />
      {[...Array(9)].map((_, i) => { const k = 1 - i / 9; const w = 1100 * k, h = 1900 * k; return <path key={i} d={`M ${540 - w / 2} ${1000 + h * 0.25} L ${540 - w / 2} ${1000 - h * 0.1} Q ${540 - w / 2} ${1000 - h * 0.5} 540 ${1000 - h * 0.5} Q ${540 + w / 2} ${1000 - h * 0.5} ${540 + w / 2} ${1000 - h * 0.1} L ${540 + w / 2} ${1000 + h * 0.25} Z`} fill={mix(pal.floor, pal.wallDark, i / 9)} stroke={pal.ink} strokeWidth="5" opacity="1" />; })}
      <ellipse cx="540" cy="900" rx={110 * pulse} ry={150 * pulse} fill={pal.skyBot} /><ellipse cx="540" cy="900" rx={80 * pulse} ry={110 * pulse} fill="#fff" opacity=".9" />
      <path d={`M 0 1920 L 400 1180 L 680 1180 L 1080 1920 Z`} fill={shade(pal.floor, 0.2)} />
      {[...Array(6)].map((_, i) => { const k = (i + (t * 0.8) % 1) / 6; return <path key={i} d={`M ${540 - 140 - 400 * k} ${1180 + 740 * k} L ${540 + 140 + 400 * k} ${1180 + 740 * k}`} stroke={pal.white} strokeWidth={4 + 8 * k} opacity=".25" />; })}
      {[...Array(5)].map((_, i) => <rect key={i} x={140 + i * 190} y={120 + (i % 2) * 30} width="120" height="18" rx="9" fill={pal.white} opacity={0.6 + 0.4 * osc(t, 1.2, i * 0.2)} />)}
    </g>);
  },
  'dressing-room': ({ pal, t, sh, seed }) => (
    <g>
      <rect width={W} height="1300" fill={pal.wall} /><rect y="1300" width={W} height="620" fill={pal.floor} />
      {[...Array(5)].map((_, i) => <g key={i} transform={`translate(${40 + i * 205} 380)`}><rect width="180" height="780" rx="10" fill={mix(pal.wallDark, pal.wall, 0.15)} stroke={pal.ink} strokeWidth="6" /><rect x="14" y="30" width="152" height="360" rx="6" fill={shade(pal.wallDark, 0.1)} /><rect x="14" y="410" width="152" height="340" rx="6" fill={shade(pal.wallDark, 0.1)} />{[...Array(4)].map((_, k) => <rect key={k} x="40" y={60 + k * 14} width="100" height="5" fill={pal.ink} opacity=".4" />)}<circle cx="150" cy="400" r="9" fill={pal.gold} /><path d={`M 60 -10 L 90 -10 L ${90 + 6 * osc(t, 0.8, i * 0.2)} 60 L 50 60 Z`} fill={[pal.red, pal.blue, pal.gold, pal.green, pal.purple][i]} stroke={pal.ink} strokeWidth="4" /></g>)}
      <rect y="1250" width={W} height="40" fill={pal.brown} stroke={pal.ink} strokeWidth="5" />
      {[...Array(4)].map((_, i) => <rect key={i} x={i * 280 - 20 + 40} y="1300" width="260" height="620" fill="none" stroke={pal.ink} strokeWidth="4" opacity=".2" />)}
      {[...Array(3)].map((_, i) => <g key={i}><rect x={160 + i * 340} y="70" width="220" height="26" rx="13" fill={pal.white} /><ellipse cx={270 + i * 340} cy="200" rx="200" ry="150" fill="#fff" opacity={0.08 + 0.04 * osc(t, 1, i * 0.3)} /></g>)}
    </g>
  ),
  studio: ({ pal, t, sh, seed }) => (
    <g>
      <Grad id="stuG" a={shade(pal.board, 0.1)} b={mix(pal.board, pal.wallDark, 0.5)} />
      <rect width={W} height={H} fill="url(#stuG)" />
      {[...Array(5)].map((_, i) => <rect key={i} x={30 + i * 205} y={300} width="185" height="760" rx="26" fill={mix(pal.board, pal.accent, 0.1 + 0.07 * i)} opacity=".55" />)}
      {[...Array(5)].map((_, i) => <rect key={i} x={30 + i * 205} y={300 + 200 + 120 * Math.abs(osc(t, 0.6, i * 0.17))} width="185" height="10" fill={pal.accent} opacity=".7" />)}
      <Spot x={200} t={t} c={pal.white} /><Spot x={880} t={t} c={pal.white} sp={0.4} />
      <rect y="1180" width={W} height="740" fill={shade(pal.floor, 0.2)} /><rect y="1180" width={W} height="8" fill={pal.accent} opacity={0.7 + 0.3 * osc(t, 1.4)} />
      {[...Array(9)].map((_, i) => <circle key={i} cx={60 + i * 120} cy={110} r="9" fill={i % 2 ? pal.accent : pal.accent2} opacity={0.5 + 0.5 * Math.abs(osc(t, 1.5, i * 0.12))} />)}
      <path d="M 0 1500 Q 540 1420 1080 1500 L 1080 1920 L 0 1920 Z" fill={mix(pal.floor, '#fff', 0.1)} opacity=".6" />
    </g>
  ),
  street: ({ pal, t, sh, seed }) => (
    <g>
      <Grad id="strSky" a={pal.skyTop} b={pal.skyBot} /><rect width={W} height="1200" fill="url(#strSky)" /><Clouds t={t} seed={seed} pal={pal} y={300} n={3} />
      {[...Array(6)].map((_, i) => { const bw = 150 + (i % 3) * 40, bh = 380 + ((i * 97) % 5) * 70, x = i * 190 - 20 + sh * 0.2; return <g key={i}><rect x={x} y={1130 - bh} width={bw} height={bh} fill={mix(pal.wallDark, pal.skyBot, 0.35 + (i % 3) * 0.12)} stroke={pal.ink} strokeWidth="5" /><Windows x={x + 18} y={1130 - bh + 24} cols={Math.floor((bw - 20) / 40)} rows={Math.floor((bh - 40) / 52)} w={26} h={34} gx={40} gy={52} on={pal.gold} off={mix(pal.wall, pal.wallDark, 0.4)} t={t} seed={seed + i} p={0.3} /></g>; })}
      <rect y="1130" width={W} height="60" fill={mix(pal.wall, '#fff', 0.2)} /><rect y="1190" width={W} height="730" fill={shade(pal.floor, 0.15)} />
      {[...Array(5)].map((_, i) => <rect key={i} x={((i * 260 - (t * 160) % 260) )} y="1560" width="150" height="20" rx="6" fill={pal.white} opacity=".8" />)}
      {[170, 700].map((x, i) => <g key={i}><rect x={x} y="760" width="14" height="430" fill={pal.ink} /><circle cx={x + 7} cy="750" r="26" fill={pal.gold} /><ellipse cx={x + 7} cy="760" rx="100" ry="70" fill={pal.gold} opacity={0.1 + 0.04 * osc(t, 1, i)} /></g>)}
    </g>
  ),
  office: ({ pal, t, sh, seed }) => (
    <g>
      <rect width={W} height={H} fill={pal.wall} /><rect y="1350" width={W} height="570" fill={mix(pal.floor, pal.wall, 0.15)} />
      <rect x="120" y="360" width="840" height="620" rx="12" fill={pal.skyTop} stroke={pal.ink} strokeWidth="9" />
      <Grad id="offSky" a={pal.skyTop} b={pal.skyBot} /><rect x="130" y="370" width="820" height="600" fill="url(#offSky)" />
      {[0, 1, 2, 3, 4].map((i) => { const h = 150 + ((i * 83) % 4) * 60; return <rect key={i} x={140 + i * 160} y={970 - h} width="120" height={h} fill={mix(pal.wallDark, pal.skyBot, 0.45)} stroke={pal.ink} strokeWidth="4" />; })}
      <Clouds t={t} seed={seed} pal={pal} y={450} n={2} />
      <path d="M 540 370 L 540 980 M 130 670 L 950 670" stroke={pal.ink} strokeWidth="9" />
      <g transform="translate(980 220)"><circle r="64" fill={pal.white} stroke={pal.ink} strokeWidth="7" /><path d={`M 0 0 L ${36 * Math.sin(t * 0.6)} ${-36 * Math.cos(t * 0.6)} M 0 0 L ${24 * Math.sin(t * 0.05)} ${-24 * Math.cos(t * 0.05)}`} stroke={pal.ink} strokeWidth="7" strokeLinecap="round" /></g>
      {[...Array(3)].map((_, i) => <rect key={i} x={80 + i * 360} y="90" width="240" height="24" rx="12" fill="#fff" opacity=".9" />)}
      <rect y="1330" width={W} height="30" fill={pal.wallDark} />
    </g>
  ),
  'living-room': ({ pal, t, sh, seed }) => (
    <g>
      <rect width={W} height={H} fill={pal.wall} />
      {[...Array(14)].map((_, i) => <g key={i}>{[...Array(9)].map((__, j) => <circle key={j} cx={i * 80 + (j % 2) * 40} cy={j * 120 + 40 + ((t * 8) % 120) - 120} r="9" fill={mix(pal.wall, pal.wallDark, 0.18)} />)}</g>)}
      <rect y="1380" width={W} height="540" fill={pal.floor} /><rect y="1360" width={W} height="30" fill={pal.wallDark} />
      <g transform="translate(110 340)"><rect width="360" height="440" rx="10" fill={pal.skyTop} stroke={pal.ink} strokeWidth="9" /><rect x="10" y="10" width="340" height="420" fill={pal.skyBot} /><Cloud x={120 + ((t * 20) % 220)} y={150} s={0.7} c="#fff" /><path d="M 180 0 L 180 440 M 0 220 L 360 220" stroke={pal.ink} strokeWidth="8" /></g>
      <g transform="translate(700 400)"><rect width="260" height="190" rx="8" fill={pal.gold} stroke={pal.ink} strokeWidth="7" /><rect x="16" y="16" width="228" height="158" fill={mix(pal.accent2, '#fff', 0.2)} /></g>
      <g transform="translate(900 1000)"><path d="M 0 0 L 70 0 L 56 -70 L 14 -70 Z" fill={pal.gold} stroke={pal.ink} strokeWidth="6" /><rect x="-3" y="0" width="76" height="12" fill={pal.metal} /><ellipse cx="35" cy="-40" rx="140" ry="140" fill={pal.gold} opacity={0.12 + 0.05 * osc(t, 0.7)} /></g>
      <ellipse cx="540" cy="1700" rx="480" ry="110" fill={pal.accent2} opacity=".5" />
    </g>
  ),
  'press-room': ({ pal, t, sh, seed }) => (
    <g>
      <rect width={W} height={H} fill={pal.board} />
      {[...Array(9)].map((_, r) => [...Array(7)].map((__, c) => { const x = c * 170 + (r % 2) * 85 - 40 + ((t * 18) % 170), y = 240 + r * 150; const k = (r + c) % 3; return <g key={r + '-' + c} transform={`translate(${x} ${y})`}>{k === 0 ? <circle r="30" fill={pal.accent} opacity=".8" /> : k === 1 ? <rect x="-28" y="-28" width="56" height="56" rx="8" fill={pal.accent2} opacity=".8" /> : <polygon points="0,-34 32,26 -32,26" fill={pal.skyTop} opacity=".8" />}</g>; }))}
      <rect y="0" width={W} height="240" fill={shade(pal.board, 0.3)} /><rect y="1450" width={W} height="470" fill={shade(pal.floor, 0.25)} /><rect y="1440" width={W} height="16" fill={pal.accent} />
      <Spot x={260} t={t} c={pal.white} sp={0.6} w={260} /><Spot x={820} t={t} c={pal.white} sp={0.5} w={260} />
      {[...Array(7)].map((_, i) => { const k = (t * 1.2 + rand01(seed, i)) % 1.6; return k < 0.12 ? <circle key={i} cx={rand01(seed, i + 7) * W} cy={1500 + rand01(seed, i + 3) * 300} r={60 * (1 - k / 0.12) + 20} fill="#fff" opacity=".85" /> : null; })}
    </g>
  ),
  'night-city': ({ pal, t, sh, seed }) => (
    <g>
      <Grad id="ncSky" a={shade(pal.board, 0.55)} b={mix(pal.wallDark, pal.board, 0.5)} /><rect width={W} height={H} fill="url(#ncSky)" />
      {[...Array(36)].map((_, i) => <circle key={i} cx={rand01(seed, i) * W} cy={rand01(seed, i + 40) * 760} r={1.5 + rand01(seed, i + 80) * 3} fill="#fff" opacity={0.4 + 0.6 * Math.abs(osc(t, 0.7 + rand01(seed, i), rand01(seed, i + 3)))} />)}
      <circle cx="800" cy="320" r="90" fill={pal.gold} /><circle cx="770" cy="296" r="86" fill={mix(pal.board, pal.gold, 0.08)} opacity=".0" />
      {[...Array(7)].map((_, i) => { const bw = 150 + (i % 3) * 36, bh = 520 + ((i * 131) % 5) * 90, x = i * 168 - 30 + sh * 0.2; return <g key={i}><rect x={x} y={1260 - bh} width={bw} height={bh + 700} fill={shade(mix(pal.wallDark, pal.board, 0.55), i % 2 ? 0.1 : 0)} /><Windows x={x + 16} y={1260 - bh + 24} cols={Math.floor((bw - 12) / 34)} rows={Math.floor((bh - 40) / 50)} w={22} h={30} gx={34} gy={50} on={pal.gold} off={shade(pal.board, 0.2)} t={t} seed={seed + i * 3} p={0.45} /></g>; })}
      <rect y="1300" width={W} height="620" fill={shade(pal.board, 0.35)} />{[...Array(5)].map((_, i) => <rect key={i} x={((i * 260 - (t * 200) % 260))} y="1560" width="140" height="18" rx="6" fill={pal.gold} opacity=".85" />)}
    </g>
  ),
  podium: ({ pal, t, sh, seed }) => (
    <g>
      <Grad id="podG" a={shade(pal.board, 0.2)} b={mix(pal.board, pal.accent2, 0.35)} /><rect width={W} height={H} fill="url(#podG)" />
      <path d="M 0 0 Q 100 500 0 1300 L 0 0 Z M 1080 0 Q 980 500 1080 1300 L 1080 0 Z" fill={pal.red} opacity=".7" />
      <Spot x={300} t={t} c={pal.gold} w={300} sp={0.7} /><Spot x={780} t={t} c={pal.gold} w={300} sp={0.55} />
      {[...Array(40)].map((_, i) => { const k = (t * (0.25 + rand01(seed, i) * 0.3) + rand01(seed, i + 9)) % 1; return <rect key={i} x={rand01(seed, i + 3) * W + 30 * Math.sin(t * 2 + i)} y={-30 + k * 2000} width="14" height="26" fill={[pal.gold, pal.red, pal.blue, pal.white, pal.green][i % 5]} transform={`rotate(${t * 200 + i * 40} ${rand01(seed, i + 3) * W} ${k * 2000})`} opacity=".9" />; })}
      <rect y="1320" width={W} height="600" fill={shade(pal.board, 0.35)} />
      <path d="M 0 1320 L 1080 1320" stroke={pal.gold} strokeWidth="12" opacity={0.8 + 0.2 * osc(t, 1.5)} />
    </g>
  ),
  'bench-area': ({ pal, t, sh, seed }) => (
    <g>
      <Grad id="baSky" a={pal.skyTop} b={pal.skyBot} /><rect width={W} height="1000" fill="url(#baSky)" />
      <g transform={`translate(${sh * 0.4} 0)`}><Crowd y={440} rows={4} gap={54} r={20} a={pal.crowdA} b={pal.crowdB} t={t} seed={seed} ink={pal.ink} /></g>
      <rect y="880" width={W} height="400" fill={pal.grassA} /><Stripes y0={880} y1={H} a={pal.grassA} b={pal.grassB} t={t} n={6} />
      <path d="M -20 160 L 1100 100 L 1100 250 L -20 300 Z" fill={mix(pal.skyBot, pal.wallDark, 0.4)} opacity=".9" stroke={pal.ink} strokeWidth="6" /><rect y="250" width={W} height="40" fill={pal.metal} opacity="0" />
      <rect x="-20" y="1130" width="1120" height="24" fill={pal.metal} stroke={pal.ink} strokeWidth="6" /><rect x="40" y="1050" width="24" height="90" fill={pal.metal} stroke={pal.ink} strokeWidth="5" /><rect x="1010" y="1050" width="24" height="90" fill={pal.metal} stroke={pal.ink} strokeWidth="5" />
      <rect y="1130" width={W} height="790" fill={shade(pal.floor, 0.1)} />
      {[...Array(5)].map((_, i) => <rect key={i} x={i * 240 - 20} y="1130" width="12" height="790" fill={pal.ink} opacity=".12" />)}
    </g>
  ),
  training: ({ pal, t, sh, seed }) => (
    <g>
      <Grad id="trSky" a={pal.skyTop} b={pal.skyBot} /><rect width={W} height="900" fill="url(#trSky)" /><Clouds t={t} seed={seed} pal={pal} y={280} n={4} />
      <path d="M -20 820 Q 200 640 420 800 Q 660 600 900 780 Q 1040 700 1100 800 L 1100 900 L -20 900 Z" fill={mix(pal.grassB, pal.skyBot, 0.3)} />
      {[...Array(9)].map((_, i) => <g key={i} transform={`translate(${60 + i * 130} 840)`}><rect x="-4" y="0" width="8" height="70" fill={pal.brown} /><circle cy="-6" r="38" fill={mix(pal.green, pal.grassB, 0.5)} stroke={pal.ink} strokeWidth="4" /></g>)}
      <rect y="900" width={W} height={H - 900} fill={pal.grassA} /><Stripes y0={900} y1={H} a={pal.grassA} b={pal.grassB} t={t} n={9} persp={1.7} />
      {[[200, 1180], [420, 1260], [700, 1230], [880, 1340], [320, 1420]].map(([x, y], i) => <g key={i} transform={`translate(${x} ${y}) scale(0.55)`}><path d="M -14 -60 L 14 -60 L 48 40 L -48 40 Z" fill={pal.orange} stroke={pal.ink} strokeWidth="6" /><rect x="-60" y="38" width="120" height="16" rx="6" fill={shade(pal.orange, 0.15)} stroke={pal.ink} strokeWidth="6" /></g>)}
    </g>
  ),
  'plain-colour': ({ pal, t, sh, seed }) => (
    <g>
      <Grad id="plG" a={mix(pal.accent, '#fff', 0.2)} b={pal.accent2} /><rect width={W} height={H} fill="url(#plG)" opacity=".92" />
      {[...Array(5)].map((_, i) => <circle key={i} cx={(i * 280 + t * 24 * (1 + i * 0.2)) % 1400 - 160} cy={300 + i * 330} r={150 + (i % 2) * 70} fill="#fff" opacity=".1" />)}
      {[...Array(11)].map((_, r) => [...Array(7)].map((__, c) => <circle key={r + '-' + c} cx={c * 170 + (r % 2) * 85} cy={r * 190 + ((t * 30) % 190)} r={5 + 3 * Math.sin(t * 2 + r + c)} fill="#fff" opacity=".28" />))}
    </g>
  ),
  boardroom: ({ pal, t, sh, seed }) => (
    <g>
      <rect width={W} height={H} fill={pal.wall} /><rect y="1500" width={W} height="420" fill={shade(pal.floor, 0.1)} />
      <rect x="80" y="300" width="920" height="640" fill={pal.skyTop} stroke={pal.ink} strokeWidth="10" /><Grad id="brSky" a={pal.skyTop} b={pal.skyBot} /><rect x="90" y="310" width="900" height="620" fill="url(#brSky)" />
      {[0, 1, 2, 3, 4, 5].map((i) => { const h = 180 + ((i * 71) % 5) * 70; return <rect key={i} x={100 + i * 148} y={930 - h} width="110" height={h} fill={mix(pal.wallDark, pal.skyBot, 0.5)} stroke={pal.ink} strokeWidth="4" />; })}
      <path d="M 390 310 L 390 940 M 690 310 L 690 940" stroke={pal.ink} strokeWidth="8" />
      {[200, 540, 880].map((x, i) => <g key={i}><path d={`M ${x} 0 L ${x} 130`} stroke={pal.ink} strokeWidth="5" /><path d={`M ${x - 70} 190 Q ${x} 90 ${x + 70} 190 Z`} fill={pal.gold} stroke={pal.ink} strokeWidth="6" /><ellipse cx={x} cy="230" rx="100" ry="40" fill={pal.gold} opacity={0.15 + 0.05 * osc(t, 1, i)} /></g>)}
      <path d="M 0 1330 L 1080 1330 L 1080 1500 L 0 1500 Z" fill={pal.brown} stroke={pal.ink} strokeWidth="8" /><rect y="1330" width={W} height="22" fill={shade(pal.brown, -0.2)} />
      <g transform="translate(870 1010)"><rect width="140" height="190" fill={pal.white} stroke={pal.ink} strokeWidth="6" /><path d={`M 14 160 L 40 ${110 - 10 * osc(t, 0.5)} L 70 ${130} L 100 ${70 + 8 * osc(t, 0.5)} L 126 40`} fill="none" stroke={pal.red} strokeWidth="8" strokeLinejoin="round" /></g>
    </g>
  ),
  pub: ({ pal, t, sh, seed }) => (
    <g>
      <rect width={W} height={H} fill={mix(pal.brown, pal.ink, 0.35)} />
      {[...Array(14)].map((_, i) => <rect key={i} x={i * 80 - 6} y="0" width="6" height="1360" fill={pal.ink} opacity=".25" />)}
      <path d="M 0 190 Q 270 270 540 190 Q 810 270 1080 190" fill="none" stroke={pal.ink} strokeWidth="5" />{[...Array(12)].map((_, i) => { const x = 45 + i * 90, y = 190 + 40 * Math.sin((x / 1080) * TAU) * (0.8) + 20; return <g key={i}><circle cx={x} cy={y + 14} r="17" fill={[pal.gold, pal.red, pal.teal][i % 3]} /><circle cx={x} cy={y + 14} r="40" fill={pal.gold} opacity={0.12 + 0.1 * osc(t, 1.5, i * 0.17)} /></g>; })}
      <g transform="translate(130 420)"><rect width="320" height="380" rx="14" fill={pal.board} stroke={pal.ink} strokeWidth="8" /><rect x="20" y="20" width="280" height="340" fill={mix(pal.board, pal.accent, 0.2)} /><circle cx="160" cy="190" r="110" fill={pal.white} stroke={pal.ink} strokeWidth="5" /><circle cx="160" cy="190" r="70" fill={pal.red} /><circle cx="160" cy="190" r="30" fill={pal.green} /><circle cx="160" cy="190" r="8" fill={pal.ink} /></g>
      <g transform="translate(640 440)"><rect width="320" height="260" rx="12" fill={pal.ink} stroke={pal.ink} strokeWidth="8" /><rect x="16" y="16" width="288" height="228" fill={mix(pal.skyTop, '#fff', 0.15 + 0.12 * osc(t, 2))} /></g>
      <rect y="1360" width={W} height="40" fill={pal.brown} stroke={pal.ink} strokeWidth="6" /><rect y="1400" width={W} height="520" fill={shade(pal.brown, 0.3)} />
      {[...Array(5)].map((_, i) => <g key={i} transform={`translate(${120 + i * 210} 1300)`}><rect x="-14" y="-60" width="28" height="64" fill={pal.metal} stroke={pal.ink} strokeWidth="5" /><rect x="-6" y="0" width="12" height="46" fill={[pal.gold, pal.red, pal.teal, pal.orange, pal.blue][i]} stroke={pal.ink} strokeWidth="4" /></g>)}
    </g>
  ),
  sky: ({ pal, t, sh, seed }) => (
    <g>
      <Grad id="skG" a={pal.skyTop} b={pal.skyBot} /><rect width={W} height={H} fill="url(#skG)" />
      <g transform={`translate(880 360) rotate(${t * 8})`}>{[...Array(14)].map((_, i) => <path key={i} d="M -26 0 L 26 0 L 0 -900 Z" transform={`rotate(${i * (360 / 14)})`} fill="#fff" opacity=".12" />)}<circle r="96" fill={pal.gold} stroke={pal.ink} strokeWidth="6" /></g>
      <Clouds t={t} seed={seed} pal={pal} y={560} n={6} /><Clouds t={t * 1.3} seed={seed + 5} pal={pal} y={1100} n={5} c={pal.white} />
    </g>
  ),
  kitchen: ({ pal, t, sh, seed }) => (
    <g>
      <rect width={W} height={H} fill={pal.wall} />
      {[...Array(10)].map((_, r) => [...Array(7)].map((__, c) => <rect key={r + '-' + c} x={c * 160 - 10} y={r * 130 + 60} width="150" height="120" fill={mix(pal.wall, '#fff', 0.35)} stroke={pal.wallDark} strokeWidth="4" opacity=".7" />))}
      <rect x="60" y="120" width="420" height="300" rx="10" fill={pal.wallDark} stroke={pal.ink} strokeWidth="7" /><rect x="76" y="136" width="388" height="268" fill={pal.skyBot} /><Cloud x={160 + ((t * 24) % 260)} y={250} s={0.6} c="#fff" />
      <rect y="1260" width={W} height="60" fill={pal.metal} stroke={pal.ink} strokeWidth="7" /><rect y="1320" width={W} height="600" fill={pal.wallDark} stroke={pal.ink} strokeWidth="7" />
      {[...Array(4)].map((_, i) => <rect key={i} x={30 + i * 262} y="1350" width="236" height="520" rx="8" fill={mix(pal.wallDark, '#fff', 0.15)} stroke={pal.ink} strokeWidth="5" />)}
      {[...Array(4)].map((_, i) => <circle key={i} cx={150 + i * 262} cy="1400" r="10" fill={pal.gold} />)}
    </g>
  ),
};

export const Background: React.FC<{ kind?: string; shift?: number; style?: React.CSSProperties }> = ({ kind = 'plain-colour', shift = 0, style }) => {
  const sc = useScene();
  const f = BG[kind] || BG['plain-colour'];
  const seed = (sc.no * 977 + 13) % 997;
  return <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: 'absolute', left: 0, top: 0, ...style }}>{f({ pal: sc.theme.palette, t: sc.t, sh: shift, seed, line: sc.theme.line })}</svg>;
};
