// TRANSITION LIBRARY (15). Each draws an opaque graphic overlay for `cover` in 0..1 (1 = screen fully covered).
// IN  transition: cover goes 1 -> 0 over the first 0.25 s;  OUT transition: cover goes 0 -> 1 over the last 0.25 s.
// Add one: add its id to core/vocab.ts TRANSITIONS and a function to TR below -> (cover, {pal, mirror, seed}) => <g/>.
import React from 'react';
import type {Palette} from '../theme/themes';
import {clamp, ease, TAU, osc} from '../core/ease';
import {rand01} from '../core/rng';
import {mix, shade} from '../core/color';
import {star} from '../ui/Fx';

const W = 1080, H = 1920;
interface O { pal: Palette; mirror: boolean; seed: string; t: number; line: number }
const cols = (pal: Palette) => [pal.accent2, pal.accent, pal.board, pal.skyTop];

export const TR: Record<string, (c: number, o: O) => React.ReactElement> = {
  'wipe-diag': (c, { pal }) => {
    const sk = 0.45 * H;
    const X = -300 + (W + sk + 700) * c;
    const poly = (x: number, f: string, sw = 0) => <path d={`M -2400 0 L ${x} 0 L ${x - sk} ${H} L -2400 ${H} Z`} fill={f} stroke={pal.ink} strokeWidth={sw} strokeLinejoin="round" />;
    return <g>{poly(X, pal.accent2, 8)}{poly(X - 90, pal.accent, 8)}{poly(X - 190, pal.board, 8)}</g>;
  },
  iris: (c, { pal }) => {
    const r = (1 - c) * 1250;
    const d = `M -50 -50 H ${W + 50} V ${H + 50} H -50 Z M ${W / 2} ${H / 2 - r} a ${r} ${r} 0 1 0 0.01 0 Z`;
    return <g><path d={d} fillRule="evenodd" fill={pal.board} />{r > 4 && <circle cx={W / 2} cy={H / 2} r={r} fill="none" stroke={pal.accent} strokeWidth="26" />}{r > 4 && <circle cx={W / 2} cy={H / 2} r={r + 13} fill="none" stroke={pal.ink} strokeWidth="6" />}</g>;
  },
  blinds: (c, { pal }) => {
    const n = 10, hh = H / n;
    return <g>{[...Array(n)].map((_, i) => { const k = ease.outCubic(clamp(c * 1.7 - (i / n) * 0.7)); return <rect key={i} x="-10" y={i * hh + hh / 2 - (hh * k) / 2 - 0.5} width={W + 20} height={hh * k + 1} fill={cols(pal)[i % 3]} stroke={pal.ink} strokeWidth="5" />; })}</g>;
  },
  checker: (c, { pal }) => {
    const cw = 180, cx = 6, cy = 11;
    return <g>{[...Array(cx * cy)].map((_, i) => { const x = i % cx, y = Math.floor(i / cx); const d = (x / cx + y / cy) / 2; const k = ease.outBack(clamp(c * 2.1 - d * 1.1), 1.2); const s = Math.max(0, Math.min(1.12, k)); return <rect key={i} x={x * cw + cw / 2 - (cw * 1.05 * s) / 2} y={y * cw + cw / 2 - (cw * 1.05 * s) / 2} width={cw * 1.05 * s} height={cw * 1.05 * s} rx="14" fill={(x + y) % 2 ? pal.accent : pal.board} stroke={pal.ink} strokeWidth="5" />; })}</g>;
  },
  'ball-roll': (c, { pal, t }) => {
    const x = -340 + (W + 680) * c, r = 300;
    return <g><rect x="-1500" y="-10" width={x + 1500} height={H + 20} fill={pal.accent} /><rect x={x - 70} y="-10" width="70" height={H + 20} fill={pal.accent2} /><path d={`M ${x} -10 L ${x} ${H + 10}`} stroke={pal.ink} strokeWidth="8" />
      <g transform={`translate(${x} ${H / 2}) rotate(${x * 0.35})`}><circle r={r} fill={pal.white} stroke={pal.ink} strokeWidth="12" /><polygon points={star(5, 90, 90)} fill={pal.ink} />{[0, 1, 2, 3, 4].map((i) => <polygon key={i} points="-50,-210 50,-210 74,-262 0,-296 -74,-262" fill={pal.ink} transform={`rotate(${i * 72})`} />)}</g></g>;
  },
  panels: (c, { pal }) => {
    const n = 5, pw = W / n + 90;
    return <g>{[...Array(n)].map((_, i) => { const k = ease.outCubic(clamp(c * 1.8 - i * 0.16)); const dir = i % 2 ? 1 : -1; const y = dir * (1 - k) * 2300; return <path key={i} d={`M ${i * (W / n) - 45 + 60} ${y - 40} L ${i * (W / n) - 45 + pw + 60} ${y - 40} L ${i * (W / n) - 45 + pw - 60} ${y + H + 40} L ${i * (W / n) - 45 - 60} ${y + H + 40} Z`} fill={cols(pal)[i % 3]} stroke={pal.ink} strokeWidth="7" strokeLinejoin="round" />; })}</g>;
  },
  'star-iris': (c, { pal, t }) => {
    const r = (1 - c) * 1500;
    const pts = star(5, r, r * 0.5, -Math.PI / 2 + t * 2 + (1 - c) * 3);
    const d = `M -50 -50 H ${W + 50} V ${H + 50} H -50 Z M ${pts.split(' ').map((p, i) => (i ? 'L ' : '') + p.split(',').map((v, j) => (+v + (j ? H / 2 : W / 2)).toFixed(1)).join(' ')).join(' ')} Z`;
    return <g><path d={d} fillRule="evenodd" fill={pal.accent2} />{r > 6 && <polygon points={star(5, r, r * 0.5, -Math.PI / 2 + t * 2 + (1 - c) * 3)} transform={`translate(${W / 2} ${H / 2})`} fill="none" stroke={pal.ink} strokeWidth="10" strokeLinejoin="round" />}</g>;
  },
  dots: (c, { pal }) => {
    const sp = 120, nx = 10, ny = 17;
    return <g>{[...Array(nx * ny)].map((_, i) => { const x = i % nx, y = Math.floor(i / nx); const d = (x / nx + (ny - y) / ny) / 2; const k = clamp(c * 1.9 - d * 0.9); return <circle key={i} cx={x * sp + sp / 2} cy={y * sp + sp / 2} r={sp * 0.78 * ease.outCubic(k)} fill={(x + y) % 2 ? pal.accent2 : pal.board} />; })}{c > 0.9 && <rect width={W} height={H} fill={pal.board} opacity={(c - 0.9) * 10} />}</g>;
  },
  stripes: (c, { pal }) => {
    const n = 9, sw = W / n;
    return <g>{[...Array(n)].map((_, i) => { const k = ease.outCubic(clamp(c * 1.7 - Math.abs(i - 4) * 0.1)); const up = i % 2; return <rect key={i} x={i * sw - 1} y={up ? H - H * k : 0} width={sw + 2} height={H * k + 2} fill={i % 2 ? pal.grassB : pal.grassA} stroke={pal.ink} strokeWidth="4" />; })}</g>;
  },
  curtain: (c, { pal }) => {
    const k = ease.outCubic(c);
    const half = (W / 2 + 40) * k;
    const folds = (x0: number, dir: number) => [...Array(7)].map((_, i) => <path key={i} d={`M ${x0 + dir * (i + 0.5) * (half / 7)} 0 L ${x0 + dir * (i + 0.5) * (half / 7) + 12 * Math.sin(i + 1)} ${H}`} stroke={shade(pal.accent2, 0.35)} strokeWidth={22} opacity=".55" />);
    return <g><rect x={0} y="-10" width={half} height={H + 20} fill={pal.accent2} stroke={pal.ink} strokeWidth="8" />{folds(0, 1)}<rect x={W - half} y="-10" width={half} height={H + 20} fill={pal.accent2} stroke={pal.ink} strokeWidth="8" />{folds(W, -1)}<rect x="-10" y="-10" width={W + 20} height="46" fill={pal.gold} stroke={pal.ink} strokeWidth="6" opacity={k > 0.02 ? 1 : 0} /></g>;
  },
  zigzag: (c, { pal }) => {
    const base = H + 260 - (H + 560) * c, tooth = 90;
    const pts = [...Array(14)].map((_, i) => `${i * tooth - 20},${base + (i % 2 ? -50 : 50)}`).join(' L ');
    const mk = (off: number, f: string) => <path d={`M -20 ${H + 400} L ${pts.split(' L ').map((p) => { const [x, y] = p.split(',').map(Number); return `${x},${y + off}`; }).join(' L ')} L ${W + 20} ${H + 400} Z`} fill={f} stroke={pal.ink} strokeWidth="7" strokeLinejoin="round" />;
    return <g>{mk(0, pal.accent2)}{mk(90, pal.accent)}{mk(190, pal.board)}</g>;
  },
  'flash-slam': (c, { pal }) => {
    const k = ease.outBack(clamp(c * 1.25), 1.1);
    const fl = clamp((c - 0.55) * 4) * clamp((1 - c) * 6 + 0.0) ;
    return <g><rect x="-10" y={-H + H * Math.min(1.04, k)} width={W + 20} height={H + 40} fill={pal.accent} stroke={pal.ink} strokeWidth="10" /><rect x="-10" y={-H + H * Math.min(1.04, k) - 90} width={W + 20} height="90" fill={pal.accent2} stroke={pal.ink} strokeWidth="8" /><rect width={W} height={H} fill="#fff" opacity={Math.max(0, fl) * (c < 0.995 ? 0.9 : 0.0)} />{c > 0.94 && <rect width={W} height={H} fill={pal.accent} />}</g>;
  },
  'ink-splat': (c, { pal, seed }) => {
    const blobs = [[200, 300], [880, 260], [540, 700], [180, 1100], [900, 1150], [520, 1500], [150, 1700], [930, 1750], [540, 1000], [540, 250]];
    return <g>{blobs.map(([x, y], i) => { const k = ease.outBack(clamp(c * 1.6 - (i % 5) * 0.1), 1.3); const r = 560 * Math.max(0, k); return <g key={i}><circle cx={x} cy={y} r={r + 14} fill={pal.ink} /></g>; })}{blobs.map(([x, y], i) => { const k = ease.outBack(clamp(c * 1.6 - (i % 5) * 0.1), 1.3); const r = 560 * Math.max(0, k); return <circle key={i} cx={x} cy={y} r={r} fill={[pal.accent2, pal.accent, pal.board][i % 3]} />; })}</g>;
  },
  'hex-shutter': (c, { pal, t }) => {
    const r = (1 - c) * 1350;
    const pts = [...Array(6)].map((_, i) => { const a = (i / 6) * TAU + (1 - c) * 2.2; return `${(W / 2 + Math.cos(a) * r).toFixed(1)} ${(H / 2 + Math.sin(a) * r).toFixed(1)}`; });
    const d = `M -50 -50 H ${W + 50} V ${H + 50} H -50 Z M ${pts.join(' L ')} Z`;
    return <g><path d={d} fillRule="evenodd" fill={pal.board} />{r > 4 && <path d={`M ${pts.join(' L ')} Z`} fill="none" stroke={pal.accent} strokeWidth="22" strokeLinejoin="round" />}</g>;
  },
  wave: (c, { pal, t }) => {
    const mk = (off: number, f: string, amp: number, ph: number) => { const y0 = H + 200 - (H + 520) * clamp(c * 1.15 - off); let d = `M -20 ${H + 400} L -20 ${y0}`; for (let x = -20; x <= W + 40; x += 30) d += ` L ${x} ${y0 + Math.sin((x / W) * TAU * 1.6 + ph + t * 9) * amp}`; return <path d={d + ` L ${W + 40} ${H + 400} Z`} fill={f} stroke={pal.ink} strokeWidth="7" />; };
    return <g>{mk(0, pal.accent2, 70, 0)}{mk(0.06, pal.accent, 60, 1.2)}{mk(0.12, pal.board, 50, 2.4)}</g>;
  },
};

export const TransitionLayer: React.FC<{ id: string; phase: 'in' | 'out'; p: number; pal: Palette; seed: string; t: number; mirror?: boolean }> = ({ id, phase, p, pal, seed, t, mirror }) => {
  const k = clamp(p);
  // quad easing keeps every neighbouring frame visibly different, including the boundary frames (cover is 1 only on the very first / last frame)
  const cover = phase === 'in' ? 1 - ease.outQuad(k) : ease.inQuad(k);
  if (cover <= 0.001) return null;
  const f = TR[id] || TR['wipe-diag'];
  const flip = phase === 'in' ? !mirror : !!mirror;
  return (
    <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: 'absolute', left: 0, top: 0 }}>
      <g transform={flip ? `translate(${W} 0) scale(-1 1)` : undefined}>{f(cover, { pal, mirror: !!mirror, seed, t, line: 6 })}</g>
    </svg>
  );
};
