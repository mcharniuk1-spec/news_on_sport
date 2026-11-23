// <Actor/> -- THE character rig. One parametric SVG figure used by every template (incl. the comic engine).
//
//   <Actor role="striker" pose="kick" emote="happy" x={540} y={1500} scale={1.5} flip={false} t={sceneSeconds} />
//
// Props
//   role     striker|keeper|reporter|coach|referee|fan|legend|mascot|kid|pundit|boss|player|rookie|staff
//   pose     name (see POSES) OR timeline [["idle",0],["kick",0.5]] -> blended with overshoot (blend=0.22 s)
//   emote    neutral|happy|shock|angry-cheeky|smug|sweat|sleepy|cry|love|dizzy|sad|wink
//   x,y      FEET position in canvas px (1080x1920);  scale 1 == 540 px tall figure;  flip mirrors horizontally
//   t        seconds (drives breathing, blink, cycles, lip flap). Defaults to scene time.
//   talk     0..1 lip-flap amount (true == 1);  look [-1..1,-1..1] pupil direction
//   hold     {kind, hand:'R'|'L'|'both', scale?, rot?, dx?, dy?, anim?} or an array: prop attached to the hand (follows the arm)
//   skin/hair/shirt/number  colour/number overrides (cast entries);  id  cast id (varies idle phase + picks colours)
//   squash   -1..1  (+ = stretch tall, - = squash flat), applied about the feet;  rot degrees about the feet;  lift px (airborne)
//   opacity, shadow (bool), bust (hide legs, for bust shots)
import React from 'react';
import {useScene} from '../core/ctx';
import {hashStr} from '../core/rng';
import {TAU, osc, clamp} from '../core/ease';
import {mix, shade} from '../core/color';
import {resolvePose, PoseSpec, PoseDef} from './poses';
import {Face} from './Face';
import {HairBack, HairFront} from './Hair';
import {ROLE_DEFS} from './roles';
import {PropIcon} from '../props/Prop';

export interface HoldSpec { kind: string; hand?: 'R' | 'L' | 'both'; scale?: number; rot?: number; dx?: number; dy?: number; anim?: string }
export interface ActorProps {
  role?: string; pose?: PoseSpec; emote?: string; x: number; y: number; scale?: number; flip?: boolean; t?: number;
  talk?: number | boolean; look?: [number, number]; hold?: HoldSpec | HoldSpec[]; skin?: string; hair?: string; shirt?: string; number?: string | number;
  id?: string; squash?: number; rot?: number; lift?: number; opacity?: number; shadow?: boolean; bust?: boolean; blink?: boolean; blend?: number; hairStyle?: string;
}

/** the resolved look (skin / hair colour / hair style / shirt) the Actor will use for (id, role, overrides): lets templates make two figures look DIFFERENT on purpose. */
export const lookOf = (th: any, no: number, id: string | undefined, role: string | undefined, ov: { skin?: string; hair?: string; shirt?: string; hairStyle?: string } = {}) => {
  const roleName = role && ROLE_DEFS[role] ? role : 'player';
  const rd = ROLE_DEFS[roleName];
  const h = hashStr((id || roleName) + '|' + no);
  return {
    skin: ov.skin || th.skins[h % th.skins.length] as string,
    hair: ov.hair || (rd.greyHair ? '#d6d2c6' : th.hairs[(h >>> 3) % th.hairs.length]) as string,
    shirt: ov.shirt || th.shirts[(rd.shirt + (id ? (h >>> 5) % th.shirts.length : 0)) % th.shirts.length] as string,
    hairStyle: ov.hairStyle || rd.hair[(h >>> 7) % rd.hair.length],
  };
};

export const ARM = [75, 70] as const;
export const LEG = [78, 72] as const;
const SH_X = 64, SH_Y = -270, HIP_Y = -150, HEAD_Y = -398, HEAD_R = 100;

function ik(side: number, tx: number, ty: number, bend: number) {
  const sx = side * SH_X, sy = SH_Y;
  let dx = tx - sx, dy = ty - sy;
  let d = Math.hypot(dx, dy) || 1e-3;
  const maxd = ARM[0] + ARM[1] - 0.8, mind = Math.abs(ARM[0] - ARM[1]) + 10;
  const k = d > maxd ? maxd / d : d < mind ? mind / d : 1;
  dx *= k; dy *= k; d = Math.hypot(dx, dy);
  const a = (ARM[0] * ARM[0] - ARM[1] * ARM[1] + d * d) / (2 * d);
  const h = Math.sqrt(Math.max(0, ARM[0] * ARM[0] - a * a));
  const mx = sx + (dx * a) / d, my = sy + (dy * a) / d;
  const px = -dy / d, py = dx / d;
  const c1: [number, number] = [mx + px * h, my + py * h], c2: [number, number] = [mx - px * h, my - py * h];
  const score = (c: [number, number]) => (c[0] - sx) * side * 0.6 + (c[1] - sy) * 0.8;
  let e = score(c1) >= score(c2) ? c1 : c2;
  if (bend < 0) e = e === c1 ? c2 : c1;
  return { s: [sx, sy] as [number, number], e, h: [sx + dx, sy + dy] as [number, number] };
}
function legPts(side: number, spread: number, phi: number, knee: number) {
  const hx = side * spread, hy = HIP_Y;
  const a = (phi * Math.PI) / 180, b = ((phi - knee) * Math.PI) / 180;
  const kx = hx + LEG[0] * Math.sin(a), ky = hy + LEG[0] * Math.cos(a);
  const fx = kx + LEG[1] * Math.sin(b), fy = ky + LEG[1] * Math.cos(b);
  return { h: [hx, hy] as [number, number], k: [kx, ky] as [number, number], f: [fx, fy] as [number, number], ang: phi - knee };
}
const cyc3 = (c: [number, number, number] | undefined, t: number, hz: number) => (c ? [c[0] * osc(t, hz, c[2]), c[1] * osc(t, hz, c[2] + 0.25)] : [0, 0]);

export const Actor: React.FC<ActorProps> = (p) => {
  const sc = useScene();
  const th = sc.theme, pal = th.palette;
  const uid = React.useId().replace(/[^a-zA-Z0-9]/g, '');
  const t = p.t ?? sc.t;
  const roleName = p.role && ROLE_DEFS[p.role] ? p.role : 'player';
  const rd = ROLE_DEFS[roleName];
  const key = (p.id || roleName) + '|' + sc.no;
  const h = hashStr(key);
  const phase = (h % 1000) / 1000;
  const L = th.line, ink = pal.ink;

  // colours
  const skin = p.skin || th.skins[h % th.skins.length];
  const hairCol = p.hair || (rd.greyHair ? '#d6d2c6' : th.hairs[(h >>> 3) % th.hairs.length]);
  const shirtCol = p.shirt || th.shirts[(rd.shirt + (p.id ? (h >>> 5) % th.shirts.length : 0)) % th.shirts.length];
  const hairStyle = p.hairStyle || rd.hair[(h >>> 7) % rd.hair.length];
  const shirtStyle = rd.shirtStyle[(h >>> 9) % rd.shirtStyle.length];
  const o = rd.outfit;

  let torso = shirtCol, shorts = mix(ink, shirtCol, 0.4), sock = shirtCol, boot = ink, sleeveLong = false, pants = shorts, trousers = false;
  if (o === 'kit') { shorts = mix(shirtCol, '#fff', 0.0) === shirtCol ? mix(shirtCol, ink, 0.55) : shorts; shorts = roleName === 'fan' ? mix(pal.blue, ink, 0.3) : mix(shirtCol, ink, 0.6); sock = shirtCol; boot = ink; }
  if (o === 'keeper') { torso = shirtCol; shorts = ink; sock = ink; sleeveLong = true; }
  if (o === 'blazer') { torso = shirtCol; trousers = true; pants = mix(ink, pal.wallDark, 0.35); sleeveLong = true; boot = shade(pants, 0.3); }
  if (o === 'track') { torso = shirtCol; trousers = true; pants = shade(shirtCol, 0.28); sleeveLong = true; boot = pal.white; }
  if (o === 'ref') { torso = ink; shorts = ink; sock = ink; boot = ink; }
  if (o === 'suit') { torso = mix(ink, pal.blue, 0.55); trousers = true; pants = shade(torso, 0.12); sleeveLong = true; boot = ink; }
  if (o === 'casual') { torso = shirtCol; trousers = true; pants = mix(pal.blue, ink, 0.25); boot = pal.white; }
  if (o === 'mascot') { torso = shirtCol; shorts = shade(shirtCol, 0.12); sock = shirtCol; boot = shade(shirtCol, 0.35); }
  const legThigh = trousers ? pants : shorts;
  const legShin = trousers ? pants : o === 'mascot' ? shirtCol : sock;
  const mascot = o === 'mascot';
  const hs = (p.role === 'mascot' ? rd.head : rd.head) * th.headScale;
  const R = HEAD_R * hs;

  // pose
  const base: PoseDef = resolvePose(p.pose, t, p.blend ?? 0.22);
  const cy = base.cyc;
  const hz = cy?.hz || 1;
  const ph = phase;
  const pose = (() => {
    const c = cy || ({ hz: 1 } as any);
    const [lhx, lhy] = cyc3(c.hL, t + ph, hz), [rhx, rhy] = cyc3(c.hR, t + ph, hz);
    const [llA, llK] = cyc3(c.lL, t + ph, hz), [lrA, lrK] = cyc3(c.lR, t + ph, hz);
    const mv = th.motion;
    return {
      lean: base.lean + (c.lean || 0) * osc(t + ph, hz) * mv.sway,
      bob: (c.bob || 0) * Math.abs(osc(t + ph, hz * 0.5 + 0.0001, 0)) * mv.sway,
      lift: (c.lift || 0) * Math.abs(osc(t + ph, hz * 0.5)),
      hx: base.hx + (c.hx || 0) * osc(t + ph, hz), hy: base.hy, hr: base.hr + (c.hr || 0) * osc(t + ph, hz * 1.0, 0.1) * mv.sway,
      hL: [base.hL[0] + lhx, base.hL[1] + lhy] as [number, number], hR: [base.hR[0] + rhx, base.hR[1] + rhy] as [number, number],
      lL: [base.lL[0] + llA, Math.max(0, base.lL[1] + llK)] as [number, number], lR: [base.lR[0] + lrA, Math.max(0, base.lR[1] + lrK)] as [number, number],
    };
  })();
  const breathe = 1 + 0.018 * osc(t + ph, 0.55) * th.motion.breathe + (base.sy - 1);
  const flipS = p.flip ? -1 : 1;

  // ground contact
  const lg = [legPts(-1, base.spread, pose.lL[0], pose.lL[1]), legPts(1, base.spread, pose.lR[0], pose.lR[1])];
  const maxFootY = Math.max(lg[0].f[1], lg[1].f[1]);
  const contact = base.rot ? 0 : -maxFootY * clamp(1 - Math.abs(base.rot) / 30);
  const bodyDy = base.dy + contact - pose.bob;
  const lift = (p.lift || 0) + pose.lift * (p.scale ?? 1) * rd.scale;

  // blink + talk
  const bt = (t + phase * 3.1) % 2.7;
  const blinkAmt = p.blink === false ? 0 : bt < 0.11 ? Math.sin((bt / 0.11) * Math.PI) : 0;
  const talk = typeof p.talk === 'boolean' ? (p.talk ? 1 : 0) : p.talk ?? 0;
  const look: [number, number] = p.look || [Math.sin(t * 0.8 + phase * 6) * 0.35, Math.cos(t * 0.6 + phase * 6) * 0.15];

  // arms
  const armR = ik(1, pose.hR[0], pose.hR[1], base.eb[1]);
  const armL = ik(-1, pose.hL[0], pose.hL[1], base.eb[0]);
  const rubber = th.limb === 'rubber';
  const handCol = rubber || roleName === 'keeper' ? pal.white : skin;
  const sleeveCol = sleeveLong ? torso : o === 'mascot' ? shirtCol : torso;
  const foreCol = sleeveLong || mascot ? torso : skin;
  const gloveBig = roleName === 'keeper';

  const Arm: React.FC<{ a: ReturnType<typeof ik> }> = ({ a }) => {
    const w = rubber ? 26 : 30;
    const pathAll = rubber ? `M ${a.s[0]} ${a.s[1]} Q ${a.e[0] + (a.e[0] - (a.s[0] + a.h[0]) / 2) * 0.35} ${a.e[1] + (a.e[1] - (a.s[1] + a.h[1]) / 2) * 0.35} ${a.h[0]} ${a.h[1]}` : `M ${a.s[0]} ${a.s[1]} L ${a.e[0]} ${a.e[1]} L ${a.h[0]} ${a.h[1]}`;
    return (
      <g>
        <path d={pathAll} fill="none" stroke={ink} strokeWidth={w + L * 2} strokeLinecap="round" strokeLinejoin="round" />
        {rubber ? <path d={pathAll} fill="none" stroke={skin} strokeWidth={w} strokeLinecap="round" strokeLinejoin="round" /> : <>
          <path d={`M ${a.s[0]} ${a.s[1]} L ${a.e[0]} ${a.e[1]}`} stroke={sleeveCol} strokeWidth={w} strokeLinecap="round" />
          <path d={`M ${a.e[0]} ${a.e[1]} L ${a.h[0]} ${a.h[1]}`} stroke={foreCol} strokeWidth={w - 2} strokeLinecap="round" />
        </>}
        <circle cx={a.h[0]} cy={a.h[1]} r={rubber ? 25 : gloveBig ? 25 : 20} fill={handCol} stroke={ink} strokeWidth={L} />
        {rubber && <path d={`M ${a.h[0] - 9} ${a.h[1] - 6} l 0 10 M ${a.h[0] + 2} ${a.h[1] - 8} l 0 12`} stroke={ink} strokeWidth={L * 0.6} strokeLinecap="round" />}
      </g>
    );
  };
  const Leg: React.FC<{ i: number }> = ({ i }) => {
    const g = lg[i];
    const w = rubber ? 26 : 34;
    const d = rubber ? `M ${g.h[0]} ${g.h[1]} Q ${g.k[0] + (i ? 8 : -8)} ${g.k[1]} ${g.f[0]} ${g.f[1]}` : `M ${g.h[0]} ${g.h[1]} L ${g.k[0]} ${g.k[1]} L ${g.f[0]} ${g.f[1]}`;
    const side = i ? 1 : -1;
    const toe = g.ang > 40 || Math.abs(pose.lL[0] - pose.lR[0]) > 30 ? 1 : 0.55;
    const bootR = rubber ? 36 : 30;
    return (
      <g>
        <path d={d} fill="none" stroke={ink} strokeWidth={w + L * 2} strokeLinecap="round" strokeLinejoin="round" />
        {rubber ? <path d={d} fill="none" stroke={legShin === sock ? skin : legShin} strokeWidth={w} strokeLinecap="round" /> : <>
          <path d={`M ${g.h[0]} ${g.h[1]} L ${g.k[0]} ${g.k[1]}`} stroke={legThigh} strokeWidth={w} strokeLinecap="round" />
          <path d={`M ${g.k[0]} ${g.k[1]} L ${g.f[0]} ${g.f[1]}`} stroke={legShin} strokeWidth={w - 2} strokeLinecap="round" />
          {!trousers && o !== 'mascot' && <path d={`M ${g.k[0] + (g.f[0] - g.k[0]) * 0.1} ${g.k[1] + (g.f[1] - g.k[1]) * 0.1} L ${g.k[0] + (g.f[0] - g.k[0]) * 0.34} ${g.k[1] + (g.f[1] - g.k[1]) * 0.34}`} stroke={skin} strokeWidth={w - 2} strokeLinecap="butt" opacity={0} />}
        </>}
        <g transform={`translate(${g.f[0]} ${g.f[1]}) rotate(${g.ang * 0.35})`}>
          <ellipse cx={(side * 10 * (1 - toe) + 14 * toe) * (p.flip ? 1 : 1)} cy="12" rx={bootR} ry={rubber ? 20 : 17} fill={rubber ? pal.ink : boot} stroke={ink} strokeWidth={L} />
          {!rubber && boot !== pal.white && <ellipse cx={(10 * (1 - toe) + 14 * toe)} cy="8" rx={bootR * 0.5} ry="5" fill="#fff" opacity=".18" />}
        </g>
      </g>
    );
  };

  // torso geometry (rounded trapezoid)
  const torsoPath = 'M -72 -280 Q -82 -280 -80 -262 L -66 -150 Q -64 -138 -52 -138 L 52 -138 Q 64 -138 66 -150 L 80 -262 Q 82 -280 72 -280 Q 0 -292 -72 -280 Z';
  const clipTorso = `tc${uid}`, clipHead = `hc${uid}`;
  const headCx = pose.hx, headCy = HEAD_Y + base.hy;
  const sx = 1 + (p.squash ? -0.35 * p.squash : 0), syy = 1 + (p.squash ? 0.35 * p.squash : 0);
  const shadowK = clamp(1 - lift / 400, 0.35, 1);
  const shadowFill = th.shadowStyle === 'hard' ? 'rgba(0,0,0,0.28)' : 'rgba(30,20,50,0.22)';

  const holds: HoldSpec[] = p.hold ? (Array.isArray(p.hold) ? p.hold : [p.hold]) : [];
  const handPos = (hand: string): [number, number] => hand === 'L' ? armL.h : hand === 'both' ? [(armL.h[0] + armR.h[0]) / 2, (armL.h[1] + armR.h[1]) / 2] : armR.h;

  const hairCommon = { color: hairCol, accent: shirtCol, ink, sw: L, clip: clipHead };
  const accs = rd.acc;
  const stripeC = mix(torso, '#ffffff', 0.35);

  return (
    <g transform={`translate(${p.x} ${p.y})`} opacity={p.opacity ?? 1} style={th.shadowStyle === 'hard' && th.cutout ? { filter: 'drop-shadow(5px 7px 0 rgba(0,0,0,0.25))' } : undefined}>
      {p.shadow !== false && <ellipse cx="0" cy="4" rx={(110 * shadowK) * (p.scale ?? 1) * rd.scale} ry={(20 * shadowK) * (p.scale ?? 1) * rd.scale} fill={shadowFill} />}
      <g transform={`translate(0 ${-lift * (p.scale ?? 1)}) rotate(${p.rot ?? 0}) scale(${flipS * (p.scale ?? 1) * rd.scale * sx} ${(p.scale ?? 1) * rd.scale * syy})`}>
        <g transform={base.rot ? `rotate(${base.rot} 0 ${HIP_Y})  translate(0 ${base.dy})` : undefined}>
          <g transform={`translate(0 ${bodyDy})`}>
            {!p.bust && <><Leg i={0} /><Leg i={1} /></>}
            <g transform={`rotate(${pose.lean} 0 ${HIP_Y}) translate(0 ${HIP_Y}) scale(1 ${breathe}) translate(0 ${-HIP_Y})`}>
              <defs>
                <clipPath id={clipTorso}><path d={torsoPath} /></clipPath>
              </defs>
              {/* waist / shorts */}
              {!trousers && !mascot && <path d="M -68 -176 L -68 -128 Q -68 -112 -52 -112 L 52 -112 Q 68 -112 68 -128 L 68 -176 Z" fill={shorts} stroke={ink} strokeWidth={L} strokeLinejoin="round" />}
              {trousers && <path d="M -68 -176 L -68 -126 Q -68 -112 -52 -112 L 52 -112 Q 68 -112 68 -126 L 68 -176 Z" fill={pants} stroke={ink} strokeWidth={L} strokeLinejoin="round" />}
              {mascot && <ellipse cx="0" cy="-205" rx="92" ry="92" fill={torso} stroke={ink} strokeWidth={L} />}
              {/* torso */}
              <path d={torsoPath} fill={torso} stroke={ink} strokeWidth={L} strokeLinejoin="round" />
              <g clipPath={`url(#${clipTorso})`}>
                {shirtStyle === 'stripes' && [-48, -16, 16, 48].map((x, i) => <rect key={i} x={x - 8} y="-300" width="16" height="170" fill={stripeC} opacity={i % 2 ? 0 : 0.85} />)}
                {shirtStyle === 'hoops' && [-250, -210, -170].map((y, i) => <rect key={i} x="-100" y={y} width="200" height="20" fill={stripeC} opacity=".8" />)}
                {shirtStyle === 'sash' && <path d="M -80 -280 L -30 -280 L 80 -150 L 40 -150 Z" fill={stripeC} opacity=".85" />}
                {o === 'ref' && <><rect x="-90" y="-282" width="180" height="12" fill={pal.gold} /><rect x="-90" y="-146" width="180" height="10" fill={pal.gold} /></>}
                {o === 'track' && <><path d="M 0 -282 L 0 -138" stroke={ink} strokeWidth="5" /><rect x="-90" y="-282" width="180" height="14" fill={shade(torso, 0.2)} /><rect x="-90" y="-200" width="180" height="10" fill={pal.white} opacity=".85" /></>}
                {(o === 'blazer' || o === 'suit') && <><path d="M -32 -282 L 0 -190 L 32 -282 Z" fill={pal.white} /><path d="M -34 -282 L -6 -150 M 34 -282 L 6 -150" stroke={ink} strokeWidth="4" fill="none" /><path d="M -66 -282 L -30 -240 L -42 -224 L -78 -262 Z M 66 -282 L 30 -240 L 42 -224 L 78 -262 Z" fill={shade(torso, 0.16)} stroke={ink} strokeWidth="3" /></>}
                {o === 'casual' && <path d="M -22 -284 Q 0 -250 22 -284" fill={skin} stroke={ink} strokeWidth={L * 0.8} />}
                {o === 'mascot' && <ellipse cx="0" cy="-205" rx="48" ry="58" fill={mix(torso, '#fff', 0.55)} opacity=".95" />}
              </g>
              {(o === 'kit' || o === 'keeper') && <path d="M -26 -284 Q 0 -246 26 -284" fill={skin} stroke={ink} strokeWidth={L * 0.8} />}
              {(o === 'kit' || o === 'keeper' || o === 'ref') && rd.number !== false && (p.number !== undefined || rd.number) && (
                <text x="0" y="-188" textAnchor="middle" fontFamily={th.fonts.display} fontWeight="bold" fontSize="62" fill={o === 'ref' ? pal.white : mix(shirtCol, '#fff', 0.88)} stroke={ink} strokeWidth="2" paintOrder="stroke" transform={`scale(${flipS} 1)`} opacity={roleName === 'fan' ? 0 : 0.95}>{p.number ?? (1 + (h % 11))}</text>
              )}
              {accs.includes('tie') && <g><path d="M -12 -276 L 12 -276 L 8 -250 L 22 -170 L 0 -150 L -22 -170 L -8 -250 Z" fill={pal.red} stroke={ink} strokeWidth={L * 0.7} strokeLinejoin="round" /></g>}
              {accs.includes('scarf') && <g><path d="M -52 -276 Q 0 -250 52 -276 L 56 -250 Q 0 -222 -56 -250 Z" fill={pal.accent} stroke={ink} strokeWidth={L * 0.8} /><path d="M 28 -246 L 44 -170 L 18 -166 L 12 -240 Z" fill={pal.accent} stroke={ink} strokeWidth={L * 0.8} /></g>}
              {accs.includes('lanyard') && <g><path d="M -26 -284 L 8 -190 M 26 -284 L 8 -190" stroke={pal.red} strokeWidth="7" fill="none" /><rect x="-6" y="-196" width="28" height="36" rx="5" fill={pal.white} stroke={ink} strokeWidth="3" /></g>}
              {accs.includes('medal') && <g><path d="M -22 -284 L 0 -214 L 22 -284" stroke={pal.red} strokeWidth="8" fill="none" /><circle cx="0" cy="-204" r="18" fill={pal.gold} stroke={ink} strokeWidth="4" /></g>}
              {accs.includes('whistle') && <g><path d="M -20 -284 Q 0 -236 20 -284" stroke={ink} strokeWidth="4" fill="none" /><rect x="-12" y="-244" width="30" height="16" rx="8" fill={pal.metal} stroke={ink} strokeWidth="3" /></g>}
              {/* back arm first when arms are behind the head */}
              {!base.front && <><Arm a={armL} /><Arm a={armR} /></>}
              {/* head */}
              <g transform={`translate(${headCx} ${headCy}) rotate(${pose.hr}) scale(${hs})`}>
                <g>
                  {/* ears */}
                  {!mascot && <><circle cx="-98" cy="6" r="21" fill={skin} stroke={ink} strokeWidth={L} /><circle cx="98" cy="6" r="21" fill={skin} stroke={ink} strokeWidth={L} /></>}
                  {mascot && <><circle cx="-76" cy="-84" r="38" fill={torso} stroke={ink} strokeWidth={L} /><circle cx="-76" cy="-84" r="20" fill={mix(torso, '#fff', 0.5)} /><circle cx="76" cy="-84" r="38" fill={torso} stroke={ink} strokeWidth={L} /><circle cx="76" cy="-84" r="20" fill={mix(torso, '#fff', 0.5)} /></>}
                  <HairBack style={mascot ? 'bald' : hairStyle} {...hairCommon} />
                  <circle cx="0" cy="0" r="100" fill={mascot ? torso : skin} stroke={ink} strokeWidth={L * 1.05} />
                  {mascot && <ellipse cx="0" cy="34" rx="62" ry="48" fill={mix(torso, '#fff', 0.6)} stroke={ink} strokeWidth={L * 0.8} />}
                  <g transform="translate(0 0)">
                    <defs><clipPath id={clipHead}><circle cx="0" cy="0" r="100" /></clipPath></defs>
                    {!mascot && (hairStyle !== 'bald') && <HairFront style={accs.includes('ears') ? 'bald' : hairStyle} {...hairCommon} />}
                    {rd.acc.includes('headband') && <rect x="-100" y="-58" width="200" height="16" fill={shirtCol} stroke={ink} strokeWidth={L * 0.8} clipPath={`url(#${clipHead})`} />}
                  </g>
                  <Face theme={th} emote={p.emote || 'neutral'} t={t} blink={blinkAmt} talk={talk} look={look} skin={skin} seedPhase={phase} ink={ink} />
                  {accs.includes('glasses') && <g fill="none" stroke={ink} strokeWidth={L}><circle cx="-37" cy="-6" r="33" fill="rgba(255,255,255,0.18)" /><circle cx="37" cy="-6" r="33" fill="rgba(255,255,255,0.18)" /><path d="M -4 -8 L 4 -8" /></g>}
                  {accs.includes('moustache') && <path d="M -36 28 Q -18 14 0 26 Q 18 14 36 28 Q 18 42 0 32 Q -18 42 -36 28 Z" fill={hairCol} stroke={ink} strokeWidth={L * 0.8} />}
                  {accs.includes('headset') && <g fill="none" stroke={ink} strokeWidth={L * 1.1}><path d="M -100 0 Q -96 -120 0 -118 Q 96 -120 100 0" stroke={pal.metal} strokeWidth="9" /><rect x="-120" y="-20" width="26" height="46" rx="10" fill={pal.red} /><rect x="94" y="-20" width="26" height="46" rx="10" fill={pal.red} /><path d="M -108 24 Q -90 80 -30 70" strokeWidth="5" /><circle cx="-26" cy="70" r="9" fill={ink} /></g>}
                  {accs.includes('ears') && <></>}
                </g>
              </g>
              {base.front ? <><Arm a={armL} /><Arm a={armR} /></> : null}
              {base.thumb ? <g transform={`translate(${(base.thumb > 0 ? armR : armL).h[0]} ${(base.thumb > 0 ? armR : armL).h[1]})`}><rect x="-6" y="-44" width="13" height="32" rx="6.5" fill={handCol} stroke={ink} strokeWidth={L * 0.9} /></g> : null}
              {holds.map((hd, i) => {
                const [hx, hy] = handPos(hd.hand || 'R');
                return <g key={i} transform={`translate(${hx + (hd.dx || 0) * 1} ${hy + (hd.dy || 0)}) rotate(${(hd.rot || 0) * flipS}) scale(${(hd.scale ?? 0.5) * flipS} ${hd.scale ?? 0.5})`}><PropIcon kind={hd.kind} t={t} anim={hd.anim} /></g>;
              })}
            </g>
          </g>
        </g>
      </g>
    </g>
  );
};

/** hand position of an actor in canvas px (so templates can attach FX/props); pose-resolved, no cycles. */
export const HEAD_TOP = -505;
