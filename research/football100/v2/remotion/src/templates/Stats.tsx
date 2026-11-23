// STATS: 2-3 icon + number cards, numbers count up with bouncy easing, icons act (ball bounces, whistle wobbles, watch ticks).
// content: { items:[{icon, value, label, suffix?}], bg?, accent? }
import React from 'react';
import {useScene} from '../core/ctx';
import {Background} from '../bg/Backgrounds';
import {Prop} from '../props/Prop';
import {Panel, countStr} from '../ui/Boards';
import {FitText, weightFor} from '../ui/Txt';
import {Sparkles, Shockwave, Burst, shakeAt, star} from '../ui/Fx';
import {iconAnim} from './News';
import {Stage, useBgKind} from './common';
import {ease, prog, osc, clamp, TAU} from '../core/ease';
import {mix} from '../core/color';

export const Stats: React.FC<{ c: any }> = ({ c }) => {
  const sc = useScene();
  const { t, dur, theme: th } = sc, pal = th.palette;
  const bg = useBgKind('STATS', c.bg);
  const acc = c.accent || pal.accent;
  const items: any[] = (c.items || []).slice(0, 3);
  const n = items.length;
  const cardH = n === 3 ? 386 : 560, gap = n === 3 ? 38 : 70;
  const y0 = n === 3 ? 266 : 290; // 3 cards: y 266..1500, 2 cards: 290..1480 (bottom 20 % starts at y 1536, the push adds ~2.5 %)
  const tints = [pal.red, pal.blue, pal.teal];
  const step = Math.min(0.3, Math.max(0.2, (dur - 0.9) / Math.max(1, n)));
  return (
    <>
      <Background kind={bg} shift={Math.sin(t) * 20} />
      <Stage>
        {/* connector track */}
        <g opacity=".9">
          <rect x="530" y={y0} width="20" height={n * cardH + (n - 1) * gap} rx="10" fill={pal.ink} opacity=".25" />
          {[...Array(8)].map((_, i) => <polygon key={i} points="-20,0 20,0 0,26" transform={`translate(540 ${y0 + (((t * 600) + i * 190) % (n * cardH + (n - 1) * gap))})`} fill={acc} stroke={pal.ink} strokeWidth="3" />)}
        </g>
        {items.map((it, i) => {
          const t0 = 0.26 + i * step;
          const k = ease.outBack(prog(t, t0, t0 + 0.36), 1.7);
          const dir = i % 2 ? 1 : -1;
          const cy = y0 + i * (cardH + gap) + cardH / 2;
          const kc = ease.outBack(prog(t, t0 + 0.12, t0 + 0.72), 1.5);
          // a SCORE ("2-1") never counts through a wrong score (1-1 on the way to 2-1): it flips like a split-flap card from "?-?" to the final digits
          const isScore = /^\d+\s*[-:\/]\s*\d+$/.test(String(it.value));
          const fl = prog(kc, 0.3, 0.62);
          const val = isScore ? (fl < 0.5 ? String(it.value).replace(/\d+/g, '?') : String(it.value)) + (it.suffix || '') : countStr(String(it.value), kc) + (it.suffix || '');
          const valSy = isScore ? Math.max(0.06, Math.abs(Math.cos(fl * Math.PI))) : 1;
          const done = t0 + 0.72;
          const [sx, sy] = shakeAt(t, done, 6, 0.25);
          const tint = tints[i % 3];
          const iconS = n === 3 ? 1.28 : 1.75;
          return (
            <g key={i} transform={`translate(${sx} ${sy})`}>
              <g transform={`translate(${(1 - k) * dir * 1300} 0)`}>
                <Panel x={540} y={cy} w={960} h={cardH} fill={pal.white} r={th.radius + 6}>
                  <clipPath id={'stc' + i}><rect x="-480" y={-cardH / 2} width="960" height={cardH} rx={th.radius + 6} /></clipPath>
                  <g clipPath={`url(#stc${i})`}>
                    <rect x="-480" y={-cardH / 2} width={n === 3 ? 330 : 400} height={cardH} fill={tint} />
                    {[...Array(6)].map((_, q) => <rect key={q} x={-480 + ((q * 90 + t * 60) % 540) - 60} y={-cardH / 2} width="30" height={cardH} fill="#fff" opacity=".12" transform="skewX(-18)" />)}
                    <rect x="-480" y={cardH / 2 - 16} width={960 * clamp((t - t0) / 0.8)} height="16" fill={acc} />
                  </g>
                </Panel>
                <g transform={`translate(${540 - 480 + (n === 3 ? 165 : 200)} ${cy})`}>
                  <circle r={n === 3 ? 128 : 170} fill={pal.white} stroke={pal.ink} strokeWidth={th.uiLine} opacity=".95" />
                </g>
                <Prop kind={it.icon} x={540 - 480 + (n === 3 ? 165 : 200)} y={cy} scale={iconS * 0.78} anim={iconAnim(it.icon) || 'wobble'} t0={t0 + 0.1} amp={0.3} />
                {/* value + label */}
                <g transform={`translate(0 ${cy - (n === 3 ? 38 : 70)}) scale(1 ${valSy}) translate(0 ${-(cy - (n === 3 ? 38 : 70))})`}>
                <FitText text={val} x={540 + (n === 3 ? 170 : 200)} y={cy - (n === 3 ? 38 : 70)} w={n === 3 ? 560 : 520} h={n === 3 ? 190 : 270} max={n === 3 ? 190 : 250} min={60} maxLines={1} fill={pal.ink} font={th.fonts.display} upper={false} stroke={pal.white} strokeW={2} />
                </g>
                <FitText text={it.label || ''} x={540 + (n === 3 ? 170 : 200)} y={cy + (n === 3 ? 98 : 150)} w={n === 3 ? 560 : 520} h={n === 3 ? 90 : 120} max={n === 3 ? 72 : 92} maxLines={2} fill={shade2(tint)} font={th.fonts.body} upper={false} />
              </g>
              {t > done && t < done + 0.5 && <Shockwave x={780} y={cy - 40} t0={done} r={200} color={tint} w={14} />}
              {t > done && <Sparkles n={4} cx={780} cy={cy - 40} rx={260} ry={110} color={acc} t0={done} size={0.9} seed={sc.seed + i} />}
            </g>
          );
        })}
      </Stage>
    </>
  );
};
const shade2 = (c: string) => mix(c, '#15102a', 0.42);
