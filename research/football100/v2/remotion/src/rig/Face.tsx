// Face: eyes, brows, mouth, blush, FX (sweat/zzz/hearts/tears/dizzy stars). Head-local coordinates: origin = head centre, R = 100.
import React from 'react';
import {TAU, osc, clamp} from '../core/ease';
import {shade, mix} from '../core/color';
import type {Theme} from '../theme/themes';

export interface EmoteDef {
  eyes: 'open' | 'arc-up' | 'arc-down' | 'squint' | 'heart' | 'spiral' | 'half' | 'wide' | 'side' | 'glossy';
  eyeR?: [string, string]; // optional per-eye override (wink)
  brow: [number, number, number, number]; // [lift, tiltL, tiltR, lift R extra] deg/px
  mouth: 'smile' | 'grin' | 'o' | 'smirk' | 'tongue' | 'wavy' | 'frown' | 'cry' | 'flat' | 'sleep' | 'big-o';
  blush?: boolean; sweat?: boolean; zzz?: boolean; tears?: boolean; stars?: boolean; hearts?: boolean; pupil?: number; lookBias?: [number, number];
}
export const EMOTE_DEFS: Record<string, EmoteDef> = {
  neutral: { eyes: 'open', brow: [0, 0, 0, 0], mouth: 'smile' },
  happy: { eyes: 'arc-up', brow: [-6, -4, 4, 0], mouth: 'grin', blush: true },
  shock: { eyes: 'wide', brow: [-26, -8, 8, 0], mouth: 'big-o', pupil: 0.55, sweat: true },
  'angry-cheeky': { eyes: 'half', brow: [10, 22, -22, 0], mouth: 'tongue' },
  smug: { eyes: 'half', brow: [-6, 0, -8, -10], mouth: 'smirk' },
  sweat: { eyes: 'side', brow: [-12, -14, 14, 0], mouth: 'wavy', sweat: true },
  sleepy: { eyes: 'arc-down', brow: [4, 4, -4, 0], mouth: 'sleep', zzz: true },
  cry: { eyes: 'squint', brow: [-6, -18, 18, 0], mouth: 'cry', tears: true },
  love: { eyes: 'heart', brow: [-8, -6, 6, 0], mouth: 'grin', blush: true, hearts: true },
  dizzy: { eyes: 'spiral', brow: [0, 0, 0, 0], mouth: 'wavy', stars: true },
  sad: { eyes: 'glossy', brow: [-8, -20, 20, 0], mouth: 'frown' },
  wink: { eyes: 'open', eyeR: ['open', 'arc-up'], brow: [-4, 0, -8, 0], mouth: 'tongue', blush: true },
};

interface Props {
  theme: Theme; emote: string; t: number; blink: number; talk: number; look: [number, number]; skin: string; seedPhase: number; ink: string;
}

const EYE_X = 37, EYE_Y = -6;

export const Face: React.FC<Props> = ({ theme, emote, t, blink, talk, look, skin, seedPhase, ink }) => {
  const def = EMOTE_DEFS[emote] || EMOTE_DEFS.neutral;
  const sw = Math.max(3, theme.line * 0.95);
  const st = { stroke: ink, strokeWidth: sw, strokeLinecap: 'round' as const, strokeLinejoin: 'round' as const, fill: 'none' };
  const style = theme.eye;
  const white = theme.palette.white;
  const eyeBase = style === 'big' || style === 'anime' ? 31 : style === 'tiny' ? 25 : style === 'pie' ? 29 : style === 'ink' ? 27 : 26;

  const eyeShape = (side: -1 | 1, kind: string) => {
    const cx = side * EYE_X, cy = EYE_Y;
    const r = eyeBase * (kind === 'wide' ? 1.22 : 1);
    const lookX = clamp(look[0] + (def.lookBias?.[0] || 0), -1, 1), lookY = clamp(look[1] + (def.lookBias?.[1] || 0), -1, 1);
    const open = Math.max(0.06, 1 - blink);
    const pupilBase = style === 'tiny' ? 5 : style === 'big' ? 14 : style === 'anime' ? 15 : style === 'pie' ? 17 : style === 'dots' || style === 'clear' ? 9 : style === 'ink' ? 11 : 10;
    const pr = pupilBase * (def.pupil || 1) * (kind === 'wide' ? 0.65 : 1);
    const maxOff = Math.max(2, r - pr - 2);
    let px = cx + lookX * maxOff, py = cy + lookY * maxOff;
    if (kind === 'side') px = cx + side * 0 + 11; // glance to the side (+x)
    if (kind === 'arc-up') return <path d={`M ${cx - r * 0.85} ${cy + 8} Q ${cx} ${cy - r * 1.0} ${cx + r * 0.85} ${cy + 8}`} {...st} strokeWidth={sw * 1.2} />;
    if (kind === 'arc-down') return <path d={`M ${cx - r * 0.85} ${cy - 2} Q ${cx} ${cy + r * 0.9} ${cx + r * 0.85} ${cy - 2}`} {...st} strokeWidth={sw * 1.2} />;
    if (kind === 'squint') return <path d={side < 0 ? `M ${cx - r * 0.7} ${cy - r * 0.7} L ${cx + r * 0.5} ${cy} L ${cx - r * 0.7} ${cy + r * 0.7}` : `M ${cx + r * 0.7} ${cy - r * 0.7} L ${cx - r * 0.5} ${cy} L ${cx + r * 0.7} ${cy + r * 0.7}`} {...st} strokeWidth={sw * 1.25} />;
    if (kind === 'heart') {
      const s = 1 + 0.14 * Math.max(0, osc(t, 2.4, seedPhase));
      return <g transform={`translate(${cx} ${cy}) scale(${s * 0.95})`}><path d="M0 18 C-34 -4 -22 -30 -8 -22 C-2 -18 0 -12 0 -10 C0 -12 2 -18 8 -22 C22 -30 34 -4 0 18 Z" fill="#ff4d79" stroke={ink} strokeWidth={sw * 0.8} strokeLinejoin="round" /><circle cx="-10" cy="-10" r="4" fill="#fff" opacity=".8" /></g>;
    }
    if (kind === 'spiral') {
      const ang = (t * 360 * 1.3) * (side < 0 ? 1 : -1);
      let d = ''; for (let i = 0; i <= 40; i++) { const a = (i / 40) * TAU * 2.4, rr = (i / 40) * (r * 0.95); d += `${i ? 'L' : 'M'} ${(Math.cos(a) * rr).toFixed(1)} ${(Math.sin(a) * rr).toFixed(1)} `; }
      return <g transform={`translate(${cx} ${cy}) rotate(${ang})`}><circle r={r} fill={white} stroke={ink} strokeWidth={sw * 0.8} /><path d={d} {...st} strokeWidth={sw * 0.7} /></g>;
    }
    // open-style eyes
    const ry = r * open * (kind === 'half' ? 0.62 : 1);
    if (style === 'dots' || style === 'clear') {
      return <g><ellipse cx={px} cy={cy + (kind === 'half' ? 5 : 0)} rx={pr} ry={Math.max(1.5, pr * open * (kind === 'half' ? 0.6 : 1))} fill={ink} />{kind === 'half' && <path d={`M ${cx - 16} ${cy - 3} L ${cx + 16} ${cy - 3}`} {...st} />}{style === 'clear' && open > 0.6 && <circle cx={px + 2.5} cy={cy - 3} r="2.6" fill="#fff" />}</g>;
    }
    const eyeW = style === 'ink' ? r * 1.05 : style === 'pie' ? r * 0.85 : r;
    const lidCut = kind === 'half' ? cy - r * 0.15 : null;
    return (
      <g>
        <ellipse cx={cx} cy={cy} rx={eyeW} ry={Math.max(2, ry)} fill={style === 'pie' ? '#fff' : white} stroke={ink} strokeWidth={sw * 0.85} />
        {open > 0.25 && (
          <g clipPath={undefined}>
            {style === 'anime' || style === 'big' ? (
              <g>
                <ellipse cx={px} cy={py + 1} rx={pr * 0.95} ry={Math.min(pr * 1.25, ry * 0.95)} fill={style === 'anime' ? mix(ink, '#3b8bff', 0.45) : ink} />
                <ellipse cx={px} cy={py + 3} rx={pr * 0.5} ry={Math.min(pr * 0.7, ry * 0.6)} fill={ink} />
                <circle cx={px - pr * 0.35} cy={py - pr * 0.45} r={pr * 0.3} fill="#fff" />
                <circle cx={px + pr * 0.35} cy={py + pr * 0.4} r={pr * 0.14} fill="#fff" opacity=".9" />
              </g>
            ) : style === 'pie' ? (
              <g><ellipse cx={px} cy={py} rx={pr} ry={Math.min(pr * 1.2, ry * 0.95)} fill={ink} /><path d={`M ${px} ${py} L ${px + pr * 0.9} ${py - pr * 0.3} L ${px + pr * 0.9} ${py + pr * 0.3} Z`} fill="#fff" /></g>
            ) : (
              <g><ellipse cx={px} cy={py} rx={pr} ry={Math.min(pr * 1.05, ry * 0.9)} fill={ink} /><circle cx={px - pr * 0.3} cy={py - pr * 0.35} r={Math.max(1.5, pr * 0.28)} fill="#fff" opacity=".85" /></g>
            )}
          </g>
        )}
        {lidCut !== null && <path d={`M ${cx - eyeW - 3} ${cy - r - 4} L ${cx + eyeW + 3} ${cy - r - 4} L ${cx + eyeW + 3} ${lidCut} L ${cx - eyeW - 3} ${lidCut} Z`} fill={skin} stroke="none" clipPath={undefined} />}
        {lidCut !== null && <path d={`M ${cx - eyeW} ${lidCut} L ${cx + eyeW} ${lidCut}`} {...st} />}
        {style === 'ink' && <path d={`M ${cx - eyeW} ${cy - ry * 0.6} Q ${cx} ${cy - ry * 1.5} ${cx + eyeW} ${cy - ry * 0.6}`} {...st} strokeWidth={sw * 1.3} />}
        {style === 'anime' && <path d={`M ${cx - eyeW - 2} ${cy - ry * 0.2} Q ${cx} ${cy - ry * 1.35} ${cx + eyeW + 2} ${cy - ry * 0.4}`} {...st} strokeWidth={sw * 1.5} />}
        {kind === 'glossy' && <ellipse cx={cx - 8} cy={cy - 8} rx="7" ry="5" fill="#fff" opacity=".9" />}
      </g>
    );
  };

  // brows
  const [lift, tL, tR, liftR] = def.brow;
  const browY = EYE_Y - eyeBase - 14 + lift * 0.5;
  const browW = style === 'ink' ? sw * 2.2 : style === 'anime' ? sw * 1.5 : sw * 1.1;
  const showBrows = style !== 'dots' || emote !== 'neutral';
  const brow = (side: -1 | 1) => {
    const tilt = (side < 0 ? tL : tR) * (style === 'anime' ? 1.2 : 1);
    const cx = side * EYE_X, y = browY + (side > 0 ? liftR : 0);
    return <g transform={`translate(${cx} ${y}) rotate(${side * tilt})`}><path d="M -20 3 Q 0 -6 20 3" {...st} strokeWidth={browW} /></g>;
  };

  // mouth
  const my = 46;
  const open = clamp(talk, 0, 1) * (0.55 + 0.45 * Math.abs(osc(t, 6.5, seedPhase)));
  const tone = '#c4415b';
  const mouth = (() => {
    const m = def.mouth;
    const wob = osc(t, 5, seedPhase) * 1.2;
    if (m === 'grin') return <g><path d={`M -44 ${my - 8} Q 0 ${my + 8} 44 ${my - 8} Q 40 ${my + 44 + open * 8} 0 ${my + 46 + open * 8} Q -40 ${my + 44 + open * 8} -44 ${my - 8} Z`} fill={shade('#7a1f3a', 0.1)} stroke={ink} strokeWidth={sw} strokeLinejoin="round" /><path d={`M -34 ${my - 4} Q 0 ${my + 8} 34 ${my - 4} L 30 ${my + 8} Q 0 ${my + 16} -30 ${my + 8} Z`} fill="#fff" /><ellipse cx="0" cy={my + 34 + open * 4} rx="20" ry="11" fill={tone} /></g>;
    if (m === 'o' || m === 'big-o') { const rx = m === 'big-o' ? 20 : 14, ry = (m === 'big-o' ? 28 : 18) + open * 8 + wob; return <ellipse cx="0" cy={my + 8} rx={rx} ry={ry} fill={shade('#7a1f3a', 0.1)} stroke={ink} strokeWidth={sw} />; }
    if (m === 'smirk') return <g><path d={`M -30 ${my + 6} Q 4 ${my + 14} 38 ${my - 12}`} {...st} />{open > 0.05 && <ellipse cx="4" cy={my + 10} rx="18" ry={4 + open * 14} fill={shade('#7a1f3a', 0.1)} stroke={ink} strokeWidth={sw * 0.8} />}</g>;
    if (m === 'tongue') return <g><path d={`M -38 ${my - 6} Q 0 ${my + 18} 38 ${my - 6}`} {...st} /><path d={`M -14 ${my + 8} Q -14 ${my + 40 + open * 10} 4 ${my + 40 + open * 10} Q 20 ${my + 40} 18 ${my + 6}`} fill={tone} stroke={ink} strokeWidth={sw * 0.9} strokeLinejoin="round" /></g>;
    if (m === 'wavy') return <path d={`M -34 ${my + 4} q 8.5 ${-12 + wob} 17 0 t 17 0 t 17 0 t 17 0`} {...st} />;
    if (m === 'frown') return <path d={`M -28 ${my + 16} Q 0 ${my - 6} 28 ${my + 16}`} {...st} />;
    if (m === 'cry') return <path d={`M -34 ${my + 30} Q 0 ${my - 20 + wob * 2} 34 ${my + 30} Q 0 ${my + 8} -34 ${my + 30} Z`} fill={shade('#7a1f3a', 0.1)} stroke={ink} strokeWidth={sw} strokeLinejoin="round" />;
    if (m === 'flat') return <path d={`M -22 ${my + 4} L 22 ${my + 4}`} {...st} />;
    if (m === 'sleep') { const s = 1 + 0.22 * osc(t, 0.55, seedPhase); return <ellipse cx="0" cy={my + 8} rx={13 * s} ry={9 * s} fill={shade('#7a1f3a', 0.1)} stroke={ink} strokeWidth={sw * 0.9} />; }
    // smile
    return <g><path d={`M -30 ${my - 6} Q 0 ${my + 16 + open * 10} 30 ${my - 6}`} {...st} />{open > 0.1 && <path d={`M -24 ${my - 3} Q 0 ${my + 14 + open * 10} 24 ${my - 3} Q 0 ${my + 4} -24 ${my - 3} Z`} fill={shade('#7a1f3a', 0.1)} stroke="none" />}</g>;
  })();

  const kindL = def.eyeR ? def.eyeR[0] : def.eyes;
  const kindR = def.eyeR ? def.eyeR[1] : def.eyes;
  const nose = style === 'dots' || style === 'tiny' ? null : <path d={style === 'clear' ? 'M -6 24 Q 0 30 8 24' : 'M -9 22 Q 0 32 10 22'} {...st} strokeWidth={sw * 0.8} />;

  return (
    <g>
      {def.blush && <g opacity=".55"><ellipse cx="-62" cy="28" rx="17" ry="10" fill="#ff8a9a" /><ellipse cx="62" cy="28" rx="17" ry="10" fill="#ff8a9a" /></g>}
      {eyeShape(-1, kindL)}
      {eyeShape(1, kindR)}
      {showBrows && brow(-1)}
      {showBrows && brow(1)}
      {nose}
      {mouth}
      {def.sweat && (() => { const k = ((t * 0.9 + seedPhase) % 1); return <g transform={`translate(${74} ${-48 + k * 56})`} opacity={1 - k * 0.5}><path d="M0 -22 C12 -2 14 8 0 16 C-14 8 -12 -2 0 -22 Z" fill="#8fd3ff" stroke={ink} strokeWidth={sw * 0.7} /><ellipse cx="-4" cy="4" rx="3" ry="5" fill="#fff" opacity=".8" /></g>; })()}
      {def.tears && [0, 1].map((i) => [-1, 1].map((sd) => { const k = ((t * 1.6 + i * 0.5 + seedPhase) % 1); return <ellipse key={`${i}${sd}`} cx={sd * (EYE_X + 6)} cy={14 + k * 70} rx={6 - k * 2} ry={9 - k * 3} fill="#8fd3ff" stroke={ink} strokeWidth={sw * 0.5} opacity={1 - k * 0.7} />; }))}
      {def.zzz && [0, 1, 2].map((i) => { const k = ((t * 0.7 + i / 3 + seedPhase) % 1); return <text key={i} x={80 + k * 40} y={-70 - k * 90} fontSize={34 + i * 10} fontFamily={theme.fonts.display} fontWeight="bold" fill="#fff" stroke={ink} strokeWidth="4" paintOrder="stroke" opacity={1 - k * k} transform={`rotate(${-10 + k * 20} ${80 + k * 40} ${-70 - k * 90})`}>Z</text>; })}
      {def.stars && [0, 1, 2].map((i) => { const a = t * 4.2 + (i / 3) * TAU; return <path key={i} d="M0 -14 L4 -4 L14 -4 L6 3 L9 13 L0 7 L-9 13 L-6 3 L-14 -4 L-4 -4 Z" transform={`translate(${Math.cos(a) * 92} ${-96 + Math.sin(a) * 18}) scale(${0.8 + 0.2 * Math.sin(a * 2)})`} fill={theme.palette.gold} stroke={ink} strokeWidth="3" strokeLinejoin="round" />; })}
      {def.hearts && [0, 1].map((i) => { const k = ((t * 0.9 + i * 0.5 + seedPhase) % 1); return <path key={i} d="M0 12 C-22 -2 -14 -20 -5 -14 C-1 -11 0 -7 0 -6 C0 -7 1 -11 5 -14 C14 -20 22 -2 0 12 Z" transform={`translate(${(i ? 84 : -84) + Math.sin(k * 6) * 8} ${-60 - k * 90}) scale(${0.9 - k * 0.3})`} fill="#ff4d79" stroke={ink} strokeWidth="3" opacity={1 - k * k} />; })}
    </g>
  );
};
