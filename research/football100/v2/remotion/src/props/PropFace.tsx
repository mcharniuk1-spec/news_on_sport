// PropFace: googly-eye + mouth overlay that gives ANY prop a face (comic "living objects": a scoreboard with a face).
// <Prop face="shock"/>; mood = any EMOTES name. Layout per prop kind (eyes sit on top of tall props, mouth near the bottom).
import React from 'react';
import {osc, clamp, TAU} from '../core/ease';
import type {Theme} from '../theme/themes';

const LAYOUT: Record<string, { ex: number; ey: number; er: number; my: number; mw: number }> = {
  scoreboard: { ex: 42, ey: -84, er: 27, my: 36, mw: 46 },
  stopwatch: { ex: 28, ey: -8, er: 20, my: 36, mw: 30 },
  clock: { ex: 28, ey: -8, er: 20, my: 36, mw: 30 },
  trophy: { ex: 26, ey: -52, er: 18, my: -16, mw: 24 },
  ball: { ex: 26, ey: -14, er: 20, my: 30, mw: 28 },
  tv: { ex: 40, ey: -8, er: 24, my: 40, mw: 36 },
  sticker: { ex: 26, ey: -6, er: 18, my: 18, mw: 24 },
  default: { ex: 30, ey: -10, er: 21, my: 34, mw: 32 },
};

export const PropFace: React.FC<{ kind: string; mood: string; t: number; th: Theme; look?: [number, number] }> = ({ kind, mood, t, th, look }) => {
  const L = LAYOUT[kind] || LAYOUT.default;
  const ink = th.palette.ink, white = '#ffffff';
  const sw = Math.max(4, th.line * 0.85);
  const blink = ((t + 0.37) % 3.2) < 0.1 ? 0.1 : 1;
  const lx = look ? look[0] : 0.5 * osc(t, 0.45), ly = look ? look[1] : 0.25 * osc(t, 0.35, 0.3);
  const wide = mood === 'shock' || mood === 'cry' || mood === 'dizzy';
  const lid = mood === 'smug' || mood === 'sleepy' || mood === 'angry-cheeky' || mood === 'sweat';
  const closed = mood === 'sleepy' || mood === 'happy' || mood === 'wink';
  const er = L.er * (wide ? 1.2 : 1);
  const pr = er * (wide ? 0.34 : 0.52);
  const off = er - pr - 3;
  const eye = (side: number) => {
    const cx = side * L.ex, cy = L.ey;
    if (closed && mood !== 'wink') return <path key={side} d={`M ${cx - er * 0.8} ${cy + er * 0.15} Q ${cx} ${cy - er * 0.8} ${cx + er * 0.8} ${cy + er * 0.15}`} fill="none" stroke={ink} strokeWidth={sw} strokeLinecap="round" />;
    if (mood === 'wink' && side > 0) return <path key={side} d={`M ${cx - er * 0.8} ${cy + er * 0.15} Q ${cx} ${cy - er * 0.8} ${cx + er * 0.8} ${cy + er * 0.15}`} fill="none" stroke={ink} strokeWidth={sw} strokeLinecap="round" />;
    if (mood === 'love') return <path key={side} transform={`translate(${cx} ${cy}) scale(${1 + 0.1 * osc(t, 2.5)})`} d={`M 0 ${er * 0.7} C ${-er * 1.3} ${-er * 0.2} ${-er * 0.5} ${-er * 1.1} 0 ${-er * 0.35} C ${er * 0.5} ${-er * 1.1} ${er * 1.3} ${-er * 0.2} 0 ${er * 0.7} Z`} fill={th.palette.red} stroke={ink} strokeWidth={sw * 0.7} />;
    return (
      <g key={side}>
        <ellipse cx={cx} cy={cy} rx={er} ry={er * blink} fill={white} stroke={ink} strokeWidth={sw * 0.8} />
        {mood === 'dizzy'
          ? <path d={`M ${cx} ${cy} m ${-er * 0.1} 0 a ${er * 0.2} ${er * 0.2} 0 1 1 ${er * 0.2} 0 a ${er * 0.4} ${er * 0.4} 0 1 1 ${-er * 0.4} 0 a ${er * 0.6} ${er * 0.6} 0 1 1 ${er * 0.6} 0`} fill="none" stroke={ink} strokeWidth={sw * 0.6} transform={`rotate(${t * 240} ${cx} ${cy})`} />
          : <circle cx={cx + clamp(lx, -1, 1) * off} cy={cy + clamp(ly, -1, 1) * off * blink} r={pr} fill={ink} />}
        {lid && <path d={`M ${cx - er - 2} ${cy - er * 0.05} L ${cx + er + 2} ${cy - er * 0.05} L ${cx + er + 2} ${cy - er - 4} L ${cx - er - 2} ${cy - er - 4} Z`} fill={th.palette.metal} stroke={ink} strokeWidth={sw * 0.7} clipPath="none" opacity="0.98" style={{ transformBox: 'fill-box' }} />}
      </g>
    );
  };
  const my = L.my, mw = L.mw;
  let mouth: React.ReactNode;
  const m = { fill: 'none', stroke: ink, strokeWidth: sw, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const };
  switch (mood) {
    case 'shock': mouth = <ellipse cx="0" cy={my} rx={mw * 0.34} ry={mw * (0.4 + 0.08 * osc(t, 5))} fill={ink} />; break;
    case 'sad': case 'cry': mouth = <path d={`M ${-mw * 0.7} ${my + 10} Q 0 ${my - 16} ${mw * 0.7} ${my + 10}`} {...m} />; break;
    case 'smug': case 'angry-cheeky': mouth = <path d={`M ${-mw * 0.7} ${my} Q ${-mw * 0.1} ${my + 8} ${mw * 0.8} ${my - 8}`} {...m} />; break;
    case 'sweat': case 'dizzy': mouth = <path d={`M ${-mw * 0.8} ${my} q ${mw * 0.4} -12 ${mw * 0.8} 0 t ${mw * 0.8} 0`} {...m} />; break;
    case 'sleepy': mouth = <ellipse cx="0" cy={my} rx={mw * 0.2} ry={mw * 0.16 * (1 + 0.5 * osc(t, 0.5))} fill={ink} />; break;
    case 'neutral': mouth = <path d={`M ${-mw * 0.6} ${my} L ${mw * 0.6} ${my}`} {...m} />; break;
    default: mouth = <path d={`M ${-mw * 0.8} ${my - 6} Q 0 ${my + 26} ${mw * 0.8} ${my - 6} Z`} fill={ink} stroke={ink} strokeWidth={sw * 0.6} strokeLinejoin="round" />; // happy grin
  }
  return (
    <g>
      {kind === 'scoreboard' && <rect x={-mw - 6} y={my - 14} width={mw * 2 + 12} height={36} rx={12} fill={th.palette.board} opacity={0.96} />}
      {mouth && kind === 'scoreboard' ? <g transform="translate(0 4)">{mouth}</g> : mouth}
      {eye(-1)}{eye(1)}
      {(mood === 'sweat' || mood === 'shock') && <path d={`M ${L.ex * 1.9} ${L.ey - 6 + 10 * ((t * 1.4) % 1)} q -9 14 0 22 q 9 -8 0 -22 Z`} fill="#8fd3ff" stroke={ink} strokeWidth={sw * 0.5} opacity={1 - ((t * 1.4) % 1) * 0.5} />}
    </g>
  );
};
