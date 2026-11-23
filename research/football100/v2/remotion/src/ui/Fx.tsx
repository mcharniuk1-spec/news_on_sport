// FX: confetti, sparkles, speed lines, smoke puffs, shockwave rings, burst stars. All deterministic from (seed, t).
import React from 'react';
import {useScene} from '../core/ctx';
import {rand01} from '../core/rng';
import {osc, prog, ease, TAU} from '../core/ease';

export const shakeAt = (t: number, t0: number, amp = 14, dur = 0.35, hz = 38): [number, number] => {
  const k = prog(t, t0, t0 + dur);
  if (k <= 0 || k >= 1) return [0, 0];
  const d = (1 - k) * (1 - k) * amp;
  return [Math.sin(t * hz * TAU * 0.4) * d, Math.cos(t * hz * TAU * 0.33 + 1) * d * 0.7];
};

export const Confetti: React.FC<{ n?: number; t0?: number; colors?: string[]; y0?: number; y1?: number; spread?: number; cx?: number; mode?: 'fall' | 'burst'; seed?: string }> = ({ n = 36, t0 = 0, colors, y0 = -50, y1 = 1970, cx = 540, spread = 1080, mode = 'fall', seed }) => {
  const sc = useScene();
  const pal = sc.theme.palette;
  const cols = colors || [pal.gold, pal.red, pal.blue, pal.white, pal.green, pal.pink];
  const tl = sc.t - t0;
  if (tl < 0) return null;
  const key = (seed || sc.seed) + 'cf';
  return (
    <g>
      {[...Array(n)].map((_, i) => {
        const r = rand01(key, i), r2 = rand01(key, i + 100), r3 = rand01(key, i + 200);
        let x: number, y: number;
        if (mode === 'fall') { const sp = 380 + r2 * 420; x = cx - spread / 2 + r * spread + Math.sin(tl * (2 + r3 * 3) + i) * 36; y = y0 + ((tl * sp + r3 * 1500) % (y1 - y0)); }
        else { const ang = r * TAU, v = 380 + r2 * 700; const k = Math.min(tl, 1.6); x = cx + Math.cos(ang) * v * k * 0.8; y = 700 + Math.sin(ang) * v * k * 0.8 + 520 * k * k; }
        const w = 12 + r2 * 16, h = 20 + r3 * 18;
        return <rect key={i} x={-w / 2} y={-h / 2} width={w} height={h} rx="3" fill={cols[i % cols.length]} transform={`translate(${x} ${y}) rotate(${tl * (160 + r * 300) + i * 40}) scale(${1} ${Math.cos(tl * (6 + r * 6) + i)})`} />;
      })}
    </g>
  );
};

export const Sparkles: React.FC<{ n?: number; cx?: number; cy?: number; rx?: number; ry?: number; color?: string; seed?: string; size?: number; t0?: number }> = ({ n = 8, cx = 540, cy = 900, rx = 420, ry = 500, color, seed, size = 1, t0 = 0 }) => {
  const sc = useScene();
  const col = color || sc.theme.palette.white;
  const key = (seed || sc.seed) + 'sp';
  return (
    <g>
      {[...Array(n)].map((_, i) => {
        const ph = rand01(key, i), x = cx + (rand01(key, i + 50) * 2 - 1) * rx, y = cy + (rand01(key, i + 90) * 2 - 1) * ry;
        const k = Math.max(0, Math.sin((sc.t - t0) * (3 + ph * 3) * 1 + ph * 20));
        const s = (14 + ph * 26) * size * k;
        return <path key={i} d={`M 0 ${-s} Q 0 0 ${s} 0 Q 0 0 0 ${s} Q 0 0 ${-s} 0 Q 0 0 0 ${-s} Z`} transform={`translate(${x} ${y}) rotate(${sc.t * 40 + i * 30})`} fill={col} opacity={0.9} />;
      })}
    </g>
  );
};

export const SpeedLines: React.FC<{ cx?: number; cy?: number; n?: number; color?: string; opacity?: number; r0?: number; r1?: number; speed?: number }> = ({ cx = 540, cy = 960, n = 36, color, opacity = 0.35, r0 = 380, r1 = 1500, speed = 1 }) => {
  const sc = useScene();
  const col = color || sc.theme.palette.white;
  const f = Math.floor(sc.frame * speed);
  return (
    <g opacity={opacity}>
      {[...Array(n)].map((_, i) => {
        const r = rand01(sc.seed + 'sl' + (f % 7), i);
        const a = (i / n) * TAU + r * 0.1, w = 0.012 + r * 0.02;
        const inner = r0 + r * 160, a1 = a - w, a2 = a + w;
        return <path key={i} d={`M ${cx + Math.cos(a) * inner} ${cy + Math.sin(a) * inner} L ${cx + Math.cos(a1) * r1} ${cy + Math.sin(a1) * r1} L ${cx + Math.cos(a2) * r1} ${cy + Math.sin(a2) * r1} Z`} fill={col} />;
      })}
    </g>
  );
};

export const Puffs: React.FC<{ x: number; y: number; n?: number; t0?: number; color?: string; size?: number; rise?: number }> = ({ x, y, n = 6, t0 = 0, color, size = 1, rise = 220 }) => {
  const sc = useScene();
  const col = color || sc.theme.palette.white;
  return (
    <g>
      {[...Array(n)].map((_, i) => {
        const k = (((sc.t - t0) * 0.9 + i / n) % 1 + 1) % 1;
        const dx = Math.sin(i * 2.3 + sc.t * 2) * 36 * k;
        return <circle key={i} cx={x + dx} cy={y - k * rise} r={(26 + i * 4) * size * (0.5 + k)} fill={col} opacity={0.75 * (1 - k)} stroke={sc.theme.palette.ink} strokeWidth="3" />;
      })}
    </g>
  );
};

export const Shockwave: React.FC<{ x: number; y: number; t0: number; dur?: number; r?: number; color?: string; w?: number }> = ({ x, y, t0, dur = 0.4, r = 400, color, w = 18 }) => {
  const sc = useScene();
  const k = prog(sc.t, t0, t0 + dur);
  if (k <= 0 || k >= 1) return null;
  return <circle cx={x} cy={y} r={r * ease.outCubic(k)} fill="none" stroke={color || sc.theme.palette.white} strokeWidth={w * (1 - k)} opacity={1 - k * 0.6} />;
};

export const star = (n: number, ro: number, ri: number, rot = -Math.PI / 2) => Array.from({ length: n * 2 }, (_, i) => { const a = rot + (i * Math.PI) / n, r = i % 2 ? ri : ro; return `${(Math.cos(a) * r).toFixed(1)},${(Math.sin(a) * r).toFixed(1)}`; }).join(' ');

/** SFX burst: spiky star with word (BANG/POP...) or empty. */
export const Burst: React.FC<{ x: number; y: number; r?: number; text?: string; t0?: number; color?: string; rot?: number }> = ({ x, y, r = 170, text, t0 = 0, color, rot = -8 }) => {
  const sc = useScene();
  const th = sc.theme, pal = th.palette;
  const k = sc.t - t0;
  if (k < 0) return null;
  const pop = ease.outElastic(prog(k, 0, 0.4));
  const pulse = 1 + 0.06 * osc(sc.t, 4);
  return (
    <g transform={`translate(${x} ${y}) rotate(${rot + osc(sc.t, 3) * 4}) scale(${pop * pulse})`}>
      <polygon points={star(12, r, r * 0.68)} fill={color || pal.gold} stroke={pal.ink} strokeWidth={th.uiLine + 2} strokeLinejoin="round" transform="rotate(7)" />
      <polygon points={star(12, r * 0.82, r * 0.56)} fill={pal.white} opacity=".35" />
      {text && <text textAnchor="middle" dominantBaseline="central" y="4" fontFamily={th.fonts.display} fontWeight={/Impact/i.test(th.fonts.display) ? 'normal' : 'bold'} fontSize={r * 0.5} fill={pal.red} stroke={pal.ink} strokeWidth={r * 0.06} paintOrder="stroke" strokeLinejoin="round">{text}</text>}
    </g>
  );
};
