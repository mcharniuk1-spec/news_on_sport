// POSE DEFINITIONS for the character rig. Coordinates are in rig space: origin = feet centre on the ground, y up is NEGATIVE.
// Arms use IK: a hand target (x,y) in upper-body space (shoulders sit at (+-64,-270), arm reach 145).
// Legs use FK: [hipAngleDeg, kneeBendDeg]; angle 0 = straight down, positive = towards +x (facing direction, mirrored by `flip`).
// `cyc` adds periodic motion so no pose is ever static: hz, bob(px), lean(deg), hr(deg head roll), lift(px, |sin|),
// hL/hR: [ampX, ampY, phase01] added to hand targets; lL/lR: [ampHip, ampKnee, phase01] added to leg joints.
import {ease, lerp} from '../core/ease';

export interface PoseDef {
  lean: number; dy: number; hx: number; hy: number; hr: number; sy: number; rot: number; spread: number;
  hL: [number, number]; hR: [number, number];
  lL: [number, number]; lR: [number, number];
  front: number;           // 1 = arms drawn in front of the head (face-touching poses)
  thumb: number;           // 0 none, 1 right-thumb-up, -1 left-thumb-up
  eb: [number, number];    // elbow bend side per arm (+1 / -1)
  cyc?: { hz: number; bob?: number; lean?: number; hr?: number; lift?: number; hL?: [number, number, number]; hR?: [number, number, number]; lL?: [number, number, number]; lR?: [number, number, number]; hx?: number };
}
const D: PoseDef = { lean: 0, dy: 0, hx: 0, hy: 0, hr: 0, sy: 1, rot: 0, spread: 34, hL: [-96, -135], hR: [96, -135], lL: [-3, 0], lR: [3, 0], front: 0, thumb: 0, eb: [1, 1] };
const P = (o: Partial<PoseDef>): PoseDef => ({ ...D, ...o });

export const POSE_DEFS: Record<string, PoseDef> = {
  idle: P({ cyc: { hz: 0.7, bob: 2, hL: [3, 3, 0], hR: [3, 3, 0.4], hr: 1.2 } }),
  kick: P({ lean: -7, hL: [-150, -255], hR: [70, -170], lL: [-4, 6], lR: [80, 44], cyc: { hz: 1.4, lean: 2, hL: [8, 6, 0] } }),
  run: P({ lean: 9, hL: [-70, -190], hR: [70, -190], lL: [0, 0], lR: [0, 0], cyc: { hz: 2.4, bob: 10, hL: [38, 40, 0], hR: [38, 40, 0.5], lL: [44, 46, 0], lR: [44, 46, 0.5], lean: 2 } }),
  celebrate: P({ hL: [-125, -490], hR: [125, -490], lL: [-12, 0], lR: [12, 0], cyc: { hz: 2.4, bob: 8, lift: 22, hL: [10, 14, 0], hR: [10, 14, 0.5], hr: 4 } }),
  shrug: P({ hL: [-160, -300], hR: [160, -300], hr: 7, hy: 6, cyc: { hz: 1.1, bob: 3, hL: [4, 8, 0], hR: [4, 8, 0.1], hr: 2 } }),
  point: P({ hR: [210, -300], hL: [-96, -140], lean: 3, hx: 10, cyc: { hz: 1.6, hR: [6, 4, 0], bob: 2 } }),
  sit: P({ hL: [-72, -170], hR: [72, -170], lL: [84, 86], lR: [78, 82], spread: 30, lean: -3, cyc: { hz: 0.8, bob: 1.5, hL: [2, 2, 0] } }),
  cry: P({ hL: [-32, -396], hR: [32, -396], front: 1, hr: -5, hy: 12, sy: 0.98, cyc: { hz: 2.6, bob: 4, hL: [2, 3, 0], hR: [2, 3, 0.2], hr: 2.5 } }),
  shock: P({ hL: [-130, -330], hR: [130, -330], lean: -8, hy: -6, sy: 1.03, lL: [-8, 0], lR: [8, 0], cyc: { hz: 4, bob: 3, hL: [5, 4, 0], hR: [5, 4, 0.3], lean: 1.5 } }),
  think: P({ hR: [26, -330], hL: [34, -215], front: 1, hr: 8, hx: -6, cyc: { hz: 0.9, bob: 2, hR: [2, 3, 0], hr: 2 } }),
  hold: P({ hL: [-44, -215], hR: [44, -215], cyc: { hz: 0.8, bob: 2.5, hL: [3, 3, 0.1], hR: [3, 3, 0] } }),
  fall: P({ rot: 84, dy: 0, hL: [-175, -330], hR: [170, -190], lL: [28, 12], lR: [-26, 34], cyc: { hz: 1.2, bob: 2, hL: [7, 7, 0] } }),
  dance: P({ hL: [-135, -440], hR: [135, -250], lL: [-16, 0], lR: [14, 18], cyc: { hz: 2.2, bob: 12, lean: 8, hr: 5, hL: [12, 40, 0], hR: [12, 40, 0.5], lL: [10, 14, 0], lR: [10, 14, 0.5], hx: 6 } }),
  sleep: P({ hr: 12, hy: 26, lean: 5, sy: 0.97, hL: [34, -205], hR: [-34, -208], front: 0, cyc: { hz: 0.45, bob: 6, hr: 2.5, lean: 1.5 } }),
  wave: P({ hR: [150, -420], hL: [-96, -135], cyc: { hz: 2.4, hR: [34, 8, 0], hr: 2, bob: 2 } }),
  shush: P({ hR: [20, -338], hL: [-96, -135], front: 1, hy: 2, cyc: { hz: 1.1, hR: [3, 2, 0], bob: 2 } }),
  facepalm: P({ hR: [8, -420], hL: [-96, -135], front: 1, hr: 7, hy: 10, lean: 4, cyc: { hz: 1.0, bob: 3, hr: 1.5 } }),
  jump: P({ hL: [-125, -480], hR: [125, -480], lL: [-14, 36], lR: [14, 36], cyc: { hz: 1.4, lift: 90, hL: [8, 14, 0], hR: [8, 14, 0.3] } }),
  bow: P({ lean: 30, hy: 4, hL: [-110, -130], hR: [38, -200], cyc: { hz: 0.9, bob: 2, lean: 3 } }),
  cheer: P({ hL: [-120, -470], hR: [120, -470], lL: [-8, 0], lR: [8, 0], cyc: { hz: 3, bob: 5, hL: [18, 14, 0], hR: [18, 14, 0.5], hr: 3 } }),
  tired: P({ lean: 15, hy: 26, hr: 9, sy: 0.97, hL: [-76, -96], hR: [76, -96], lL: [6, 12], lR: [-6, 12], cyc: { hz: 1.2, bob: 7, hr: 2, lean: 2 } }),
  present: P({ hR: [180, -330], hL: [-96, -135], lean: -3, cyc: { hz: 1.0, hR: [6, 8, 0], bob: 2 } }),
  headscratch: P({ hR: [46, -468], hL: [-96, -135], front: 1, hr: 6, cyc: { hz: 4.2, hR: [14, 6, 0], hr: 3, bob: 2 } }),
  thumbsup: P({ hR: [128, -330], hL: [-96, -135], thumb: 1, cyc: { hz: 1.6, hR: [4, 8, 0], bob: 3 } }),
  lean: P({ lean: 13, hL: [-70, -190], hR: [76, -170], lL: [-14, 0], lR: [26, 0], cyc: { hz: 0.6, bob: 1.5 } }),
  crouch: P({ sy: 0.86, lean: 6, hL: [-120, -170], hR: [120, -170], lL: [-40, 78], lR: [40, 78], spread: 40, cyc: { hz: 1.5, bob: 3 } }),
};
export const POSE_NAMES = Object.keys(POSE_DEFS);

const NUM_KEYS = ['lean', 'dy', 'hx', 'hy', 'hr', 'sy', 'rot', 'spread', 'front', 'thumb'] as const;
const mixP = (a: number, b: number, k: number) => lerp(a, b, k);

export function blendPose(a: PoseDef, b: PoseDef, k: number): PoseDef {
  if (k === 0) return a; if (k === 1) return b;
  const o: any = {};
  for (const key of NUM_KEYS) o[key] = mixP((a as any)[key], (b as any)[key], k);
  for (const key of ['hL', 'hR', 'lL', 'lR', 'eb'] as const) o[key] = [mixP((a as any)[key][0], (b as any)[key][0], k), mixP((a as any)[key][1], (b as any)[key][1], k)];
  // cycles: cross-fade amplitude by blending numbers present in either
  const ca: any = a.cyc || { hz: b.cyc?.hz || 1 }, cb: any = b.cyc || { hz: a.cyc?.hz || 1 };
  const c: any = { hz: mixP(ca.hz || 1, cb.hz || 1, k) };
  for (const key of ['bob', 'lean', 'hr', 'lift', 'hx']) c[key] = mixP(ca[key] || 0, cb[key] || 0, k);
  for (const key of ['hL', 'hR', 'lL', 'lR']) {
    const va = ca[key] || [0, 0, 0], vb = cb[key] || [0, 0, 0];
    c[key] = [mixP(va[0], vb[0], k), mixP(va[1], vb[1], k), vb[2]];
  }
  o.cyc = c;
  return o as PoseDef;
}

/** A pose spec is a name, or a timeline [[name, startSeconds], ...] with blends of `blend` seconds (overshooting ease). */
export type PoseSpec = string | Array<[string, number]>;
export function resolvePose(spec: PoseSpec | undefined, t: number, blend = 0.22): PoseDef {
  if (!spec) return POSE_DEFS.idle;
  if (typeof spec === 'string') return POSE_DEFS[spec] || POSE_DEFS.idle;
  if (!Array.isArray(spec[0])) return POSE_DEFS[String(spec[0])] || POSE_DEFS.idle;
  let cur = POSE_DEFS[spec[0][0]] || POSE_DEFS.idle;
  for (let i = 1; i < spec.length; i++) {
    const [name, at] = spec[i];
    const next = POSE_DEFS[name] || POSE_DEFS.idle;
    if (t < at) break;
    const k = Math.min(1, (t - at) / blend);
    cur = k >= 1 ? next : blendPose(cur, next, ease.outBack(k, 1.4));
    if (k < 1) break;
  }
  return cur;
}
