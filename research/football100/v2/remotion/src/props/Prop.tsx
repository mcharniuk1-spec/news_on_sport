// <Prop kind="trophy" x y scale rot anim t0 flip text/> : positioned, animated prop/icon (canvas px, centre anchored).
// <PropIcon kind t/> : the bare drawing (used by Actor.hold and anywhere you place props yourself).
import React from 'react';
import {useScene} from '../core/ctx';
import {DRAW} from './draw';
import {animTransform} from './anim';
import {hashStr} from '../core/rng';
import {PropFace} from './PropFace';

export const PropIcon: React.FC<{ kind: string; t?: number; anim?: string; text?: string }> = ({ kind, t, anim, text }) => {
  const sc = useScene();
  const th = sc.theme;
  const tt = t ?? sc.t;
  const d = DRAW[kind] || DRAW['question'];
  const w = Math.max(4, th.line * 0.85);
  const S = { stroke: th.palette.ink, strokeWidth: w, strokeLinejoin: 'round', strokeLinecap: 'round' };
  const at = animTransform(anim, tt, (hashStr(kind) % 100) / 100);
  return <g transform={`translate(${at.dx} ${at.dy}) rotate(${at.rot}) scale(${at.sx} ${at.sy})`} opacity={at.op}>{d({ pal: th.palette, th, ink: th.palette.ink, w, t: tt, text, S })}</g>;
};

export interface PropProps { kind: string; x: number; y: number; scale?: number; rot?: number; anim?: string; t0?: number; flip?: boolean; text?: string; opacity?: number; t?: number; shadow?: boolean; amp?: number; face?: string }
export const Prop: React.FC<PropProps> = ({ kind, x, y, scale = 1, rot = 0, anim, t0 = 0, flip, text, opacity = 1, t, shadow, amp = 1, face }) => {
  const sc = useScene();
  const tt = (t ?? sc.t);
  const tl = tt - t0;
  const d = DRAW[kind] || DRAW['question'];
  const th = sc.theme;
  const w = Math.max(4, th.line * 0.85);
  const S = { stroke: th.palette.ink, strokeWidth: w, strokeLinejoin: 'round', strokeLinecap: 'round' };
  const at = animTransform(anim, Math.max(0, tl), (hashStr(kind + sc.seed) % 100) / 100, amp);
  if (tl < 0 && (anim === 'drop' || anim === 'grow' || anim === 'pop' || anim === 'shrink')) return null;
  return (
    <g transform={`translate(${x + at.dx * scale} ${y + at.dy * scale}) rotate(${rot + at.rot}) scale(${scale * (flip ? -1 : 1) * at.sx} ${scale * at.sy})`} opacity={opacity * at.op} style={th.shadowStyle === 'hard' ? { filter: 'drop-shadow(6px 8px 0 rgba(0,0,0,0.22))' } : undefined}>
      {d({ pal: th.palette, th, ink: th.palette.ink, w, t: tt, text, S })}
      {face && <PropFace kind={kind} mood={face} t={tt} th={th} />}
    </g>
  );
};
