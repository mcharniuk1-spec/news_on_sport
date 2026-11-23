// Animation presets for props/icons (spec: drop, slide-l, slide-r, bounce, shake, grow, shrink, spin, float, arc, pulse, pop, wobble, orbit).
// animTransform(name, tl, seed) -> {dx,dy,sx,sy,rot,op}; tl = seconds since the prop's start. Entrances settle then idle-float (never static).
import {ease, prog, osc, TAU, clamp} from '../core/ease';

export interface AT { dx: number; dy: number; sx: number; sy: number; rot: number; op: number }
export const animTransform = (name: string | undefined, tl: number, ph = 0, amp = 1): AT => {
  const a: AT = { dx: 0, dy: 0, sx: 1, sy: 1, rot: 0, op: 1 };
  const idle = { dy: 6 * osc(tl, 0.9, ph), rot: 2.2 * osc(tl, 0.7, ph + 0.3), s: 1 + 0.015 * osc(tl, 1.3, ph) };
  let settled = true;
  switch (name) {
    case 'drop': { const k = prog(tl, 0, 0.55); const e = ease.outBounce(k); a.dy = -900 * (1 - e); const sq = k > 0.36 && k < 0.5 ? 0.18 : 0; a.sx = 1 + sq; a.sy = 1 - sq; a.op = tl < 0 ? 0 : 1; settled = k >= 1; break; }
    case 'slide-l': { const k = prog(tl, 0, 0.42); a.dx = -1000 * (1 - ease.outBack(k, 1.3)); a.rot = -14 * (1 - k); settled = k >= 1; break; }
    case 'slide-r': { const k = prog(tl, 0, 0.42); a.dx = 1000 * (1 - ease.outBack(k, 1.3)); a.rot = 14 * (1 - k); settled = k >= 1; break; }
    case 'bounce': { const u = Math.abs(Math.sin(tl * Math.PI * 1.7 + ph * 3)); a.dy = -70 * u; const sq = (1 - u) < 0.12 ? 0.14 * (1 - (1 - u) / 0.12) : 0; a.sx = 1 + sq; a.sy = 1 - sq; settled = false; break; }
    case 'shake': { a.dx = 9 * Math.sin(tl * 62 + ph) ; a.dy = 5 * Math.sin(tl * 47); a.rot = 5 * Math.sin(tl * 53); settled = false; break; }
    case 'grow': { const k = prog(tl, 0, 0.45); const e = ease.outBack(k, 2); a.sx = a.sy = Math.max(0, e); settled = k >= 1; break; }
    case 'shrink': { const k = prog(tl, 0, 0.35); const e = ease.outCubic(k); a.sx = a.sy = 1.9 - 0.9 * e; a.op = clamp(k * 4); settled = k >= 1; break; }
    case 'spin': { const k = prog(tl, 0, 0.5); a.rot = tl * 420; a.sx = a.sy = ease.outBack(k, 1.6); settled = false; break; }
    case 'float': { a.dy = 20 * osc(tl, 0.8, ph); a.dx = 8 * osc(tl, 0.55, ph + 0.2); a.rot = 5 * osc(tl, 0.6, ph); settled = false; break; }
    case 'arc': { const k = prog(tl, 0, 0.9); a.dx = -340 + 680 * ease.outQuad(k) - (k >= 1 ? 340 : 0) * 0; a.dx = (-340 + 340 * ease.outCubic(k)); a.dy = -260 * 4 * k * (1 - k) * (1 - k * 0.0); a.rot = 720 * k; settled = k >= 1; break; }
    case 'pulse': { const s = 1 + 0.14 * Math.max(0, osc(tl, 2.4, ph)); a.sx = a.sy = s; settled = false; break; }
    case 'pop': { const k = prog(tl, 0, 0.4); const e = ease.outElastic(k); a.sx = a.sy = Math.max(0, e); settled = k >= 1; break; }
    case 'wobble': { a.rot = 11 * osc(tl, 2.2, ph); a.sy = 1 + 0.05 * osc(tl, 4.4, ph); a.sx = 1 - 0.04 * osc(tl, 4.4, ph); settled = false; break; }
    case 'orbit': { a.dx = 70 * Math.cos(tl * 2.6 + ph * TAU); a.dy = 36 * Math.sin(tl * 2.6 + ph * TAU); a.rot = 10 * Math.sin(tl * 2.6); settled = false; break; }
    default: settled = true;
  }
  if (settled) { a.dy += idle.dy; a.rot += idle.rot; a.sx *= idle.s; a.sy *= idle.s; }
  if (amp !== 1) { a.dx *= amp; a.dy *= amp; }
  return a;
};
