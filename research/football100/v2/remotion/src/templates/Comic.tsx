// COMIC engine (agent B). Interprets the beats DSL: SETUP -> GAG (x1-2) -> silent BEAT -> TWIST.
//
// content: { bg, beats: [{ phase, t0, t1, bg?, actors?, props?, sfx?, bubble?, cam?, fx? }] }  (see DSL.md, COMIC chapter)
//  * the comic is shown in a rounded PANEL (comic-strip frame) that lives inside the safe zone (y 248..1538);
//    the background and everything else is clipped to it, so camera moves (push / pan / shake / zoom-out) are camera moves INSIDE the panel.
//  * actors / props are TRACKS across beats: same actor id (or same prop kind + occurrence) in consecutive beats is tweened
//    (position, scale, rotation) with an overshooting ease, poses are blended by the rig; new ones enter, missing ones leave.
//  * BEAT = silent beat: actors/props are inherited (frozen), only breathing / blink / prop drift move, everybody looks at the gag prop.
//  * TWIST = punchline: white flash + camera punch + ring from the gag prop, then hold.
import React from 'react';
import {useScene} from '../core/ctx';
import {Background} from '../bg/Backgrounds';
import {Actor} from '../rig/Actor';
import {ROLE_DEFS} from '../rig/roles';
import {Prop} from '../props/Prop';
import {Bubble} from '../ui/Boards';
import {PropIcon} from '../props/Prop';
import {Burst, Confetti, Puffs, Shockwave, Sparkles, SpeedLines, shakeAt} from '../ui/Fx';
import {mix, alpha} from '../core/color';
import {textWidth} from '../core/text';
import {FitText} from '../ui/Txt';
import {ease, prog, lerp, clamp, osc} from '../core/ease';

// ---------------------------------------------------------------- constants
export const PANEL = { x: 30, y: 234, w: 1020, h: 1298 };
const BACK_KINDS = new Set(['bench', 'armchair', 'sofa', 'goal', 'door', 'desk', 'table', 'chair', 'ladder', 'shelf', 'podium-box', 'crate', 'net', 'lamp', 'plant', 'screen', 'tv', 'pitch-board', 'scoreboard']);
const ENTRANCE = new Set(['drop', 'slide-l', 'slide-r', 'grow', 'shrink', 'pop', 'arc']);
const WALKABLE = new Set(['idle', 'hold', 'present', 'point', 'thumbsup', 'wave', 'shrug', 'think', 'shush', 'headscratch', 'cheer', 'facepalm']);
const BW = 0.3;           // blend window (s) at the start of every beat: positions / scales tween over it
const EN = 0.38;          // entrance slide duration (s)
const DEFAULT_SCALE = 1.3;
export const ROLE_SCALE: Record<string, number> = { rookie: 0.9, keeper: 1.02, coach: 1.02, legend: 1.02, mascot: 1.08, kid: 0.78, boss: 1.04 };
/** horizontal reach of a standing figure from the feet centre, in px per unit of (scale x role scale): body + arms. Wide poses throw the arms out. Keep in sync with validate.py (REACH). */
const WIDE_POSES = new Set(['cheer', 'celebrate', 'shock', 'jump', 'dance', 'wave', 'shrug', 'present', 'point', 'facepalm', 'thumbsup']);
export const reachOf = (pose: string) => (WIDE_POSES.has(pose) ? 165 : 105);
/** FALL rig rule: the 'fall' pose lies tilted 84 degrees about the hips, so it occupies x -200..+370 and y -335..-80 (units of scale x role scale; mirrored by flip). Two fallers must not overlap and the whole body must stay inside the panel. */
export const FALL_BOX = { x0: -200, x1: 370, y0: -335, y1: -80 };
export const fallRect = (x: number, y: number, S: number, flip: boolean) => {
  const a = flip ? -FALL_BOX.x1 : FALL_BOX.x0, b = flip ? -FALL_BOX.x0 : FALL_BOX.x1;
  return { l: x + a * S, r: x + b * S, t: y + FALL_BOX.y0 * S, b: y + FALL_BOX.y1 * S };
};

interface AState { id: string; x: number; y: number; pose: string; emote: string; flip: boolean; scale: number; label?: string; hold?: any; talk?: boolean; look?: string; lift?: number; rot?: number }
interface PState { key: string; kind: string; x: number; y: number; scale: number; rot: number; flip: boolean; anim?: string; text?: string; layer: string; face?: string; label?: string }
interface RBeat { phase: string; s0: number; s1: number; bg: string; actors: AState[]; props: PState[]; sfx?: any; bubble?: any; cam?: string; fx: any[] }

/** caption plate (name board / label): popping rounded plate, text always auto-fitted */
const Plate: React.FC<{ x: number; y: number; text: string; t0: number }> = ({ x: x0, y, text, t0 }) => {
  let x = x0;
  const sc = useScene();
  const th = sc.theme, pal = th.palette;
  const k = ease.outBack(prog(sc.t - t0, 0, 0.3), 2);
  if (sc.t < t0) return null;
  const font = th.fonts.display;
  const w = Math.min(640, Math.max(190, textWidth(th.upper ? text.toUpperCase() : text, font, 50, /Impact/i.test(font) ? 'normal' : 'bold', th.titleSpacing) + 80));
  const yy = Math.min(y, PANEL.y + PANEL.h - 64);
  x = Math.max(PANEL.x + w / 2 + 40, Math.min(PANEL.x + PANEL.w - w / 2 - 40, x));
  return (
    <g transform={`translate(${x} ${yy}) scale(${Math.max(0.01, k)}) rotate(${osc(sc.t, 0.8) * 1.5})`}>
      {th.shadowStyle !== 'none' && <rect x={-w / 2 + 6} y={-38 + 8} width={w} height={76} rx={Math.min(th.radius, 24)} fill="rgba(0,0,0,0.3)" />}
      <rect x={-w / 2} y={-38} width={w} height={76} rx={Math.min(th.radius, 24)} fill={pal.accent} stroke={pal.ink} strokeWidth={th.uiLine} />
      <FitText text={text} x={0} y={2} w={w - 40} h={56} max={52} maxLines={1} fill={pal.ink} />
    </g>
  );
};

// ---------------------------------------------------------------- resolve the authored beats into absolute seconds + normalised states
function resolve(c: any, dur: number, defBg: string): RBeat[] {
  // (c.__cast is injected by <Comic/> so the role scale is known here)
  const beats: any[] = Array.isArray(c.beats) ? c.beats : [];
  const out: RBeat[] = [];
  beats.forEach((b, i) => {
    const prev = out[i - 1];
    const inherit = b.phase === 'BEAT';
    const actors: AState[] = (b.actors ?? (inherit && prev ? prev.actors.map((a) => ({ ...a })) : [])).map((a: any) => ({
      id: a.id, x: a.x, y: a.y, pose: a.pose || 'idle', emote: a.emote || 'neutral', flip: !!a.flip, scale: a.scale ?? DEFAULT_SCALE, label: a.label, hold: a.hold, talk: a.talk, look: a.look, lift: a.lift, rot: a.rot,
    }));
    // FALL rule: keep the tilted body inside the panel (author-side overlap is rejected by validate.py)
    actors.forEach((a) => {
      if (a.pose !== 'fall') return;
      const S = a.scale * (ROLE_SCALE[(c.__cast?.[a.id] || {}).role] ?? 1);
      const r = fallRect(a.x, a.y, S, a.flip);
      if (r.l < PANEL.x + 40) a.x += PANEL.x + 40 - r.l;
      else if (r.r > PANEL.x + PANEL.w - 40) a.x -= r.r - (PANEL.x + PANEL.w - 40);
    });
    const cnt: Record<string, number> = {};
    const props: PState[] = (b.props ?? (inherit && prev ? prev.props.map((p) => ({ ...p, kind: p.kind })) : [])).map((p: any) => {
      const n = (cnt[p.kind] = (cnt[p.kind] ?? -1) + 1);
      return { key: `${p.kind}#${n}`, kind: p.kind, x: p.x, y: p.y, scale: p.scale ?? 1.6, rot: p.rot ?? 0, flip: !!p.flip, anim: p.anim, text: p.text, face: p.face, label: p.label, layer: p.layer || (BACK_KINDS.has(p.kind) && p.kind !== 'scoreboard' ? 'back' : 'front') };
    });
    out.push({ phase: b.phase, s0: (b.t0 ?? 0) * dur, s1: (b.t1 ?? 1) * dur, bg: b.bg || (prev ? prev.bg : c.bg || defBg), actors, props, sfx: inherit ? undefined : b.sfx, bubble: b.bubble ?? (inherit && prev ? prev.bubble : undefined), cam: b.cam, fx: inherit ? [] : b.fx || [] });
  });
  return out;
}

const actorIds = (rb: RBeat[]) => { const ids: string[] = []; rb.forEach((b) => b.actors.forEach((a) => { if (!ids.includes(a.id)) ids.push(a.id); })); return ids; };
const propKeys = (rb: RBeat[]) => { const ks: string[] = []; rb.forEach((b) => b.props.forEach((p) => { if (!ks.includes(p.key)) ks.push(p.key); })); return ks; };
const aIn = (b: RBeat | undefined, id: string) => b?.actors.find((a) => a.id === id);
const pIn = (b: RBeat | undefined, key: string) => b?.props.find((p) => p.key === key);

/** pose timeline [[pose, seconds]...] for one actor over all beats (run while entering / leaving / travelling) */
function poseSpec(rb: RBeat[], id: string): Array<[string, number]> {
  const spec: Array<[string, number]> = [];
  const push = (n: string, t: number) => {
    if (spec.length && spec[spec.length - 1][0] === n) return;
    if (spec.length && t - spec[spec.length - 1][1] < 0.12) spec.pop();
    if (spec.length && spec[spec.length - 1][0] === n) return;
    spec.push([n, t]);
  };
  rb.forEach((b, j) => {
    const cur = aIn(b, id), prev = aIn(rb[j - 1], id);
    if (cur) {
      const dx = prev ? Math.abs(cur.x - prev.x) : 0;
      if (!prev && j > 0) { push('run', spec.length ? b.s0 : 0); push(cur.pose, b.s0 + EN - 0.04); }
      else if (prev && dx > 140 && WALKABLE.has(cur.pose) && !WALKABLE.has('xx')) { push('run', b.s0); push(cur.pose, b.s0 + BW * 0.9); }
      else push(cur.pose, spec.length ? b.s0 : 0);
    } else if (prev && j > 0) push('run', b.s0);
  });
  if (!spec.length) spec.push(['idle', 0]);
  spec[0][1] = 0;
  return spec;
}

// ---------------------------------------------------------------- camera
type Cam = { s: number; dx: number; dy: number };
const camAt = (kind: string | undefined, phase: string, p: number, t: number, par: number): Cam => {
  const k = kind || (phase === 'TWIST' ? 'push' : '');
  const slow = phase === 'TWIST' ? 0.5 : 1;
  switch (k) {
    case 'push': return { s: 1 + 0.1 * ease.outQuad(clamp(p)) * slow, dx: 0, dy: 0 };
    case 'zoom-out': return { s: 1.18 - 0.18 * ease.outCubic(clamp(p)), dx: 0, dy: 0 };
    case 'pan': return { s: 1.07, dx: (par ? -1 : 1) * lerp(54, -54, ease.inOutQuad(clamp(p))), dy: 0 };
    case 'shake': { const a = 16 * (1 - 0.5 * clamp(p)); return { s: 1.03, dx: Math.sin(t * 61) * a, dy: Math.cos(t * 53) * a * 0.7 }; }
    default: return { s: 1, dx: 0, dy: 0 };
  }
};

// ---------------------------------------------------------------- the component
export const Comic: React.FC<{ c: any }> = ({ c }) => {
  const sc = useScene();
  const { t, dur, theme: th } = sc, pal = th.palette;
  const rb = React.useMemo(() => resolve({ ...c, __cast: sc.cast }, dur, 'plain-colour'), [c, dur, sc.cast]);
  if (!rb.length) return <Background kind="plain-colour" />;
  let bi = 0;
  rb.forEach((b, j) => { if (t >= b.s0 - 1e-6) bi = j; });
  const cur = rb[bi], prevB = rb[bi - 1];
  const lt = t - cur.s0;
  const blen = cur.s1 - cur.s0;
  const bw = Math.min(BW, blen * 0.7);
  const par = sc.no % 2;
  const gagKind = sc.prop;
  const gag = cur.props.find((p) => p.kind === gagKind) || cur.props[0];
  const silent = cur.phase === 'BEAT';

  // ---- camera (continuous across beats)
  const pCur = clamp(lt / Math.max(0.01, blen));
  let cam = camAt(cur.cam, cur.phase, pCur, t, par);
  if (prevB && lt < 0.2) { const pc = camAt(prevB.cam, prevB.phase, 1, t, par); const k = ease.inOutQuad(lt / 0.2); cam = { s: lerp(pc.s, cam.s, k), dx: lerp(pc.dx, cam.dx, k), dy: lerp(pc.dy, cam.dy, k) }; }
  if (cur.phase === 'TWIST') cam.s *= 1 + 0.05 * Math.pow(Math.max(0, 1 - lt / 0.3), 2);
  const [sx, sy] = cur.sfx ? shakeAt(t, cur.s0 + 0.06, 18, 0.3) : [0, 0];
  const fpts: Array<[number, number]> = cur.actors.map((a) => [a.x, a.y - 330] as [number, number]);
  if (gag) fpts.push([gag.x, gag.y]);
  const ax = fpts.length ? fpts.reduce((s, q) => s + q[0], 0) / fpts.length : 540;
  const ay = fpts.length ? fpts.reduce((s, q) => s + q[1], 0) / fpts.length : 880;

  // ---- camera fit: a push / punch must never crop a figure or a prop at the panel edge (left/right), so the zoom is limited by the extents of everything on stage
  {
    const L = PANEL.x + 10, R = PANEL.x + PANEL.w - 10;
    const exts: number[] = [];
    cur.actors.forEach((a) => {
      const S = a.scale * (ROLE_DEFS[(sc.cast[a.id] || {}).role || 'player']?.scale ?? 1);
      if (a.pose === 'fall') { const r = fallRect(a.x, a.y, S, a.flip); exts.push(r.l, r.r); } else { const rc = reachOf(a.pose) * S; exts.push(a.x - rc, a.x + rc); }
    });
    cur.props.forEach((p) => { if (p.layer === 'front' || p.kind === 'scoreboard') { const rc = 100 * p.scale; exts.push(p.x - rc, p.x + rc); } });
    let smax = 9;
    exts.forEach((e) => {
      if (e > ax + 1) smax = Math.min(smax, (R - cam.dx - ax) / (e - ax));
      else if (e < ax - 1) smax = Math.min(smax, (ax + cam.dx - L) / (ax - e));
    });
    cam = { ...cam, s: Math.max(1, Math.min(cam.s, smax)) };
  }

  // ---- actors
  const ids = actorIds(rb);
  const actorEls: Array<{ y: number; el: React.ReactNode }> = [];
  const plates: React.ReactNode[] = [];
  ids.forEach((id) => {
    const a = aIn(cur, id), pa = aIn(prevB, id);
    const cast = sc.cast[id] || {};
    const role = cast.role || 'player';
    let x: number, y: number, scale: number, opacity = 1;
    let st: AState | undefined = a;
    if (!a) {
      // leaving: only drawn for a moment after the beat starts
      if (!pa || lt > 0.34) return;
      const side = pa.x < 540 ? -1 : 1;
      const k = ease.inCubic(prog(lt, 0, 0.32));
      x = lerp(pa.x, side < 0 ? -300 : 1380, k); y = pa.y; scale = pa.scale; st = pa;
    } else if (!pa && bi > 0) {
      const side = a.x < 540 ? -1 : 1;
      const k = ease.outCubic(prog(lt, 0, EN));
      x = lerp(side < 0 ? -300 : 1380, a.x, k); y = a.y; scale = a.scale;
    } else if (pa) {
      const k = ease.outBack(prog(lt, 0, bw), 1.1);
      x = lerp(pa.x, a!.x, k); y = lerp(pa.y, a!.y, k); scale = lerp(pa.scale, a!.scale, k);
    } else {
      x = a.x; y = a.y; scale = a.scale * (0.9 + 0.1 * ease.outBack(prog(t, 0, 0.28), 2));
      opacity = clamp(t / 0.05);
    }
    const s = st!;
    const spec = poseSpec(rb, id);
    // squash pulse when pose or emote changes at the start of a beat
    const changed = pa && a && (pa.pose !== a.pose || pa.emote !== a.emote);
    const squash = changed ? 0.5 * Math.exp(-lt * 9) * Math.cos(lt * 34) : 0;
    // gaze
    let look: [number, number] | undefined;
    const lk = s.look || ((silent || cur.phase === 'TWIST') && gag ? '@gag' : undefined);
    if (lk) {
      let tx: number | undefined, ty: number | undefined;
      if (lk === 'cam') { tx = x; ty = y - 150; }
      else if (lk === '@gag') { if (gag) { tx = gag.x; ty = gag.y; } }
      else { const oa = cur.actors.find((q) => q.id === lk); if (oa) { tx = oa.x; ty = oa.y - 300; } else { const op = cur.props.find((q) => q.kind === lk); if (op) { tx = op.x; ty = op.y; } } }
      if (tx !== undefined && ty !== undefined) { const dx = (tx - x) / 450, dy = (ty - (y - 300 * scale)) / 450; look = [clamp(dx * (s.flip ? -1 : 1), -1, 1), clamp(dy, -1, 1)]; }
    }
    const talking = !!(cur.bubble && cur.bubble.who === id && cur.bubble.text && t - cur.s0 > 0.12) || !!s.talk;
    if (a && a.label) {
      // the name plate floats ABOVE the head (never under the feet: there the camera push crops it at the panel border and it hides the boots)
      let f = bi; while (f > 0 && aIn(rb[f - 1], id)?.label === a.label) f--;
      const Sx = scale * (ROLE_DEFS[role]?.scale ?? 1);
      plates.push(<Plate key={'pl' + id} x={clamp(x, 200, 880)} y={Math.max(PANEL.y + 110, y - 560 * Sx - 52)} text={a.label} t0={rb[f].s0 + 0.25} />);
    }
    actorEls.push({ y, el: (
      <Actor key={id} id={id} role={role} skin={cast.skin} hair={cast.hair} shirt={cast.shirt} number={cast.number} pose={spec} blend={0.18} emote={s.emote}
        x={x} y={y} scale={scale} flip={s.flip} lift={s.lift} rot={s.rot} hold={s.hold} talk={talking ? 0.9 : 0} look={look} squash={squash} opacity={opacity} />
    ) });
  });
  actorEls.sort((p, q) => p.y - q.y);

  // ---- props
  const keys = propKeys(rb);
  const propEls: Record<string, React.ReactNode[]> = { back: [], front: [] };
  keys.forEach((key) => {
    const p = pIn(cur, key), pp = pIn(prevB, key);
    // find the first beat of the current uninterrupted presence (for the entrance t0)
    let first = bi; while (first > 0 && pIn(rb[first - 1], key)) first--;
    const firstB = rb[first];
    if (!p) {
      if (!pp || lt > 0.2) return;
      const k = ease.inCubic(prog(lt, 0, 0.18));
      propEls[pp.layer].push(<Prop key={key} face={pp.face} kind={pp.kind} x={pp.x} y={pp.y} scale={pp.scale * (1 - k)} rot={pp.rot + k * 90} flip={pp.flip} opacity={1 - k} text={pp.text} anim={pp.anim && !ENTRANCE.has(pp.anim) ? pp.anim : undefined} t0={firstB.s0} />);
      return;
    }
    if (p.label) { let f = bi; while (f > 0 && pIn(rb[f - 1], key)?.label === p.label) f--; plates.push(<Plate key={'pp' + key} x={clamp(p.x, 200, 880)} y={Math.min(p.y + 118 * p.scale + 36, 1400)} text={p.label} t0={rb[f].s0 + 0.25} />); }
    let x = p.x, y = p.y, scale = p.scale, rot = p.rot, text = p.text;
    let anim = p.anim, t0 = firstB.s0;
    if (pp) {
      const k = ease.outBack(prog(lt, 0, bw), 1.15);
      x = lerp(pp.x, p.x, k); y = lerp(pp.y, p.y, k); scale = lerp(pp.scale, p.scale, k); rot = lerp(pp.rot, p.rot, k);
      if (p.anim && ENTRANCE.has(p.anim)) anim = pp.anim && !ENTRANCE.has(pp.anim) ? pp.anim : undefined;
      if (p.anim !== pp.anim && anim) t0 = cur.s0; else if (anim && pp.anim === p.anim) { let f2 = bi; while (f2 > 0 && pIn(rb[f2 - 1], key)?.anim === p.anim) f2--; t0 = rb[f2].s0; }
      // text change -> card flip (scoreboard 7:0 -> 0:0)
      if (pp.text !== p.text) {
        const fk = prog(lt, 0, 0.3);
        const sy = Math.abs(Math.cos(fk * Math.PI));
        text = fk < 0.5 ? pp.text : p.text;
        propEls[p.layer].push(<g key={key} transform={`translate(${x} ${y}) scale(1 ${Math.max(0.06, sy)}) translate(${-x} ${-y})`}><Prop face={p.face} kind={p.kind} x={x} y={y} scale={scale} rot={rot} flip={p.flip} text={text} anim={anim} t0={t0} /></g>);
        return;
      }
    } else if (bi === 0) {
      anim = p.anim; t0 = 0;
    } else if (!p.anim) anim = 'pop';
    propEls[p.layer].push(<Prop key={key} face={p.face} kind={p.kind} x={x} y={y} scale={scale} rot={rot} flip={p.flip} text={text} anim={anim} t0={t0} />);
  });

  // ---- sfx / fx / bubble
  // sfx burst: the position is clamped so the burst (incl. shake) stays inside the VISIBLE panel after the camera zoom
  const sfx = cur.sfx && (() => {
    const q = cur.sfx, rr = (q.r ?? 190) * 1.14 * cam.s + 22;
    const lo = (e0: number, a0: number, d0: number) => a0 + (e0 - a0 - d0) / cam.s;
    const x = clamp(q.x, lo(PANEL.x + 14 + rr, ax, cam.dx), lo(PANEL.x + PANEL.w - 14 - rr, ax, cam.dx));
    const y = clamp(q.y, lo(PANEL.y + 14 + rr, ay, cam.dy), lo(PANEL.y + PANEL.h - 14 - rr, ay, cam.dy));
    return { ...q, x, y };
  })();
  const sfxT0 = cur.s0 + 0.06;
  const sfxLife = clamp(blen, 0.45, 0.9);
  const sfxOut = sfx ? 1 - ease.inCubic(prog(t, cur.s0 + sfxLife - 0.12, cur.s0 + sfxLife)) : 0;
  const fxEls = cur.fx.map((f: any, i: number) => {
    const k = clamp(lt / 0.12);
    const col = f.kind === 'smoke' ? mix(pal.metal, pal.ink, 0.35) : pal.white;
    if (f.kind === 'smoke') return <g key={i} opacity={k}><Puffs x={f.x} y={f.y} n={7} t0={cur.s0} color={col} size={(f.size ?? 1) * 1.1} rise={260 * (f.size ?? 1)} /></g>;
    if (f.kind === 'dust') return <g key={i} opacity={k}><Puffs x={f.x} y={f.y} n={5} t0={cur.s0} color={pal.white} size={(f.size ?? 1) * 0.8} rise={90} /></g>;
    if (f.kind === 'sparkle') return <g key={i}><Sparkles n={8} cx={f.x} cy={f.y} rx={240 * (f.size ?? 1)} ry={200 * (f.size ?? 1)} color={pal.gold} seed={sc.seed + 'f' + i} size={1.5} /></g>;
    if (f.kind === 'confetti') return <g key={i}><Confetti n={34} t0={cur.s0} y0={PANEL.y - 40} y1={PANEL.y + PANEL.h + 60} cx={f.x} spread={PANEL.w} seed={sc.seed + 'c' + i} /></g>;
    if (f.kind === 'speed') return <g key={i}><SpeedLines cx={f.x} cy={f.y} n={26} color={pal.white} opacity={0.3} r0={260} r1={1500} speed={0.8} /></g>;
    return null;
  });
  let bubbleEl: React.ReactNode = null;
  if (cur.bubble) {
    const bb = cur.bubble;
    const who = cur.actors.find((q) => q.id === bb.who) || (cur.actors[0]);
    if (who) {
      const rd = ROLE_DEFS[(sc.cast[who.id] || {}).role || 'player'] || ROLE_DEFS.player;
      // track the actor's blended position
      const pwho = aIn(prevB, who.id);
      const k = pwho ? ease.outBack(prog(lt, 0, bw), 1.1) : 1;
      const wx = pwho ? lerp(pwho.x, who.x, k) : who.x, wy = pwho ? lerp(pwho.y, who.y, k) : who.y;
      const headTop = wy - 505 * who.scale * rd.scale;
      const txt: string = bb.text || '';
      const icon = bb.icon as string | undefined;
      const short = txt.length <= 3;
      const w = icon ? 250 : short ? 220 : txt.length <= 12 ? txt.length * 44 + 110 : 600;
      const h = icon ? 250 : short ? 200 : txt.length <= 12 ? 170 : 250;
      const bx = clamp(wx, PANEL.x + w / 2 + 24, PANEL.x + PANEL.w - w / 2 - 24);
      const by = Math.max(PANEL.y + h / 2 + 30, headTop - h / 2 - 40);
      let fb = bi; while (fb > 0 && rb[fb - 1].bubble && rb[fb - 1].bubble.who === bb.who && rb[fb - 1].bubble.text === bb.text && rb[fb - 1].bubble.icon === bb.icon) fb--;
      const t0b = rb[fb].s0 + 0.06;
      bubbleEl = (
        <Bubble x={bx} y={by} w={w} h={h} text={icon ? ' ' : txt} tail={[clamp(wx, bx - w / 2 + 40, bx + w / 2 - 40), Math.min(headTop + 40, by + h / 2 + 140)]} t0={t0b} thought={!!bb.thought} max={short ? 130 : 78} maxLines={3}>
          {icon && <g transform={`translate(${bx} ${by}) scale(0.95)`}><PropIcon kind={icon} /></g>}
        </Bubble>
      );
    }
  }

  // ---- frame, overlays
  const bgPrev = prevB && prevB.bg !== cur.bg ? prevB.bg : null;
  const bgFade = bgPrev ? clamp(lt / 0.16) : 1;
  const focusP = gag ? { x: gag.x, y: gag.y } : { x: 540, y: 860 };
  const flash = cur.phase === 'TWIST' ? clamp(1 - lt / 0.12) * 0.55 : 0;
  const vign = silent ? ease.inOutQuad(prog(lt, 0, 0.1)) * 0.2 : cur.phase === 'TWIST' ? 0.2 * (1 - ease.outCubic(prog(lt, 0, 0.2))) : 0;
  const R = Math.min(th.radius + 10, 48);
  const outer = `M 0 0 H 1080 V 1920 H 0 Z`;
  const inner = `M ${PANEL.x + R} ${PANEL.y} H ${PANEL.x + PANEL.w - R} Q ${PANEL.x + PANEL.w} ${PANEL.y} ${PANEL.x + PANEL.w} ${PANEL.y + R} V ${PANEL.y + PANEL.h - R} Q ${PANEL.x + PANEL.w} ${PANEL.y + PANEL.h} ${PANEL.x + PANEL.w - R} ${PANEL.y + PANEL.h} H ${PANEL.x + R} Q ${PANEL.x} ${PANEL.y + PANEL.h} ${PANEL.x} ${PANEL.y + PANEL.h - R} V ${PANEL.y + R} Q ${PANEL.x} ${PANEL.y} ${PANEL.x + R} ${PANEL.y} Z`;
  const outerFill = mix(pal.board, pal.accent2, 0.18);
  const lineW = th.uiLine + 6;
  return (
    <>
      <div style={{ position: 'absolute', left: PANEL.x, top: PANEL.y, width: PANEL.w, height: PANEL.h, overflow: 'hidden', borderRadius: R, background: pal.board }}>
        <div style={{ position: 'absolute', left: -PANEL.x, top: -PANEL.y, width: 1080, height: 1920, transform: `translate(${cam.dx + sx}px, ${cam.dy + sy}px) translate(${ax}px, ${ay}px) scale(${cam.s}) translate(${-ax}px, ${-ay}px)`, transformOrigin: '0 0' }}>
          {bgPrev && <Background kind={bgPrev} shift={Math.sin(t) * 20} />}
          <Background kind={cur.bg} shift={Math.sin(t) * 20} style={{ opacity: bgFade }} />
          <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{ position: 'absolute', left: 0, top: 0 }}>
            {(cur.sfx || cur.cam === 'shake') && <SpeedLines cx={focusP.x} cy={focusP.y} n={22} color={pal.white} opacity={0.12} r0={320} r1={1500} speed={0.8} />}
            {propEls.back}
            {actorEls.map((e) => e.el)}
            {propEls.front}
            {plates}
            {fxEls}
            {cur.phase === 'TWIST' && lt < 0.45 && <Shockwave x={focusP.x} y={focusP.y} t0={cur.s0 + 0.02} dur={0.4} r={620} color={pal.accent} w={26} />}
            {sfx && t >= sfxT0 && sfxOut > 0.01 && <g transform={`translate(${sfx.x} ${sfx.y}) scale(${sfxOut}) translate(${-sfx.x} ${-sfx.y})`}><Burst x={sfx.x} y={sfx.y} r={sfx.r ?? 190} text={sfx.text} t0={sfxT0} color={pal.accent} rot={par ? 8 : -8} /></g>}
            {sfx && lt < 0.45 && <Shockwave x={sfx.x} y={sfx.y} t0={sfxT0} dur={0.35} r={420} color={pal.white} w={20} />}
            {bubbleEl}
          </svg>
          <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{ position: 'absolute', left: 0, top: 0, pointerEvents: 'none' }}>
            <defs><radialGradient id="cvig" cx="50%" cy="48%" r="75%"><stop offset="0.55" stopColor="#000" stopOpacity="0" /><stop offset="1" stopColor="#000" stopOpacity="1" /></radialGradient></defs>
            <rect width="1080" height="1920" fill="url(#cvig)" opacity={vign} />
            <rect width="1080" height="1920" fill="#fff" opacity={flash} />
          </svg>
        </div>
      </div>
      {/* panel border + surround (fixed: camera moves happen inside the panel) */}
      <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{ position: 'absolute', left: 0, top: 0, pointerEvents: 'none' }}>
        <path d={`${outer} ${inner}`} fillRule="evenodd" fill={outerFill} />
        {Array.from({ length: 10 }).map((_, r) => Array.from({ length: 7 }).map((__, q) => {
          const y = r * 190 + 30 + ((t * 24) % 190) - 190, x = q * 170 + (r % 2) * 85;
          if (y > PANEL.y - 20 && y < PANEL.y + PANEL.h + 20) return null;
          return <circle key={r + '-' + q} cx={x} cy={y} r={14 + 3 * Math.sin(t * 3 + r + q)} fill={alpha(pal.accent, 0.35)} />;
        }))}
        {th.shadowStyle !== 'none' && <path d={inner} transform="translate(8 12)" fill="none" stroke="rgba(0,0,0,0.28)" strokeWidth={lineW} />}
        <path d={inner} fill="none" stroke={pal.ink} strokeWidth={lineW} strokeLinejoin="round" />
        <path d={inner} fill="none" stroke={pal.white} strokeWidth={4} strokeLinejoin="round" transform={`translate(${PANEL.x + PANEL.w / 2} ${PANEL.y + PANEL.h / 2}) scale(${1 - 16 / PANEL.w} ${1 - 16 / PANEL.h}) translate(${-(PANEL.x + PANEL.w / 2)} ${-(PANEL.y + PANEL.h / 2)})`} opacity="0.45" />
      </svg>
    </>
  );
};
