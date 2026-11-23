// NEWS: cartoon news card. figure of the story role, 3 acting icons, lower-third (name + fact), scrolling ticker.
// content: { name, fact, ticker, icons[3], role, dateline?, bg?, accent? }
import React from 'react';
import {useScene} from '../core/ctx';
import {Background} from '../bg/Backgrounds';
import {Actor} from '../rig/Actor';
import {Prop} from '../props/Prop';
import {Panel, LowerThird, Ticker} from '../ui/Boards';
import {FitText} from '../ui/Txt';
import {Sparkles, Shockwave, star, shakeAt} from '../ui/Fx';
import {Stage, useBgKind, castFor} from './common';
import {ease, prog, osc, clamp, TAU} from '../core/ease';

export const iconAnim = (kind: string): string | undefined => ({ ball: 'bounce', whistle: 'wobble', trophy: 'pulse', boot: 'wobble', flag: undefined, stopwatch: undefined, medal: 'wobble', coin: undefined, crown: 'pulse', star: 'pulse', heart: 'pulse', fire: undefined, rocket: 'float', megaphone: 'wobble', balloon: 'float', 'paper-plane': 'float', camera: 'wobble', phone: 'wobble' } as any)[kind];

export const News: React.FC<{ c: any }> = ({ c }) => {
  const sc = useScene();
  const { t, theme: th } = sc, pal = th.palette;
  const bg = useBgKind('NEWS', c.bg);
  const acc = c.accent || pal.accent;
  const who = castFor(sc.cast, c.actor, c.name); // the subject IS the comic character (cast.modric: same hair, shirt colour and number)
  const role = who?.role || c.role || 'player';
  const icons: string[] = (c.icons || ['ball', 'trophy', 'stopwatch']).slice(0, 3);
  const card = ease.outBack(prog(t, 0.1, 0.45), 1.5);
  const fig = ease.outBack(prog(t, 0.18, 0.58), 1.7);
  const [sx, sy] = shakeAt(t, 0.45, 6, 0.25);
  const cardTop = 240, cardH = 892; // card y 240..1132; ticker y 1384..1450 and lower third y 1146..1370 stay far above the bottom 20 % (y 1536)
  const cx = 540, cy = cardTop + cardH / 2;
  const iconCols = [pal.red, pal.blue, pal.teal];
  return (
    <>
      <Background kind={bg} shift={Math.sin(t * 0.8) * 24} />
      <Stage>
        <rect width="1080" height="1920" fill={pal.board} opacity=".38" />
        <g transform={`translate(${sx} ${sy})`}>
          <g transform={`translate(${cx} ${cy}) rotate(${(1 - card) * -4}) scale(${Math.max(0.01, card)}) translate(${-cx} ${-cy})`}>
            <Panel x={cx} y={cy} w={970} h={cardH} fill={pal.skyBot} r={th.radius + 8}>
              <clipPath id="newsclip"><rect x={-485} y={-cardH / 2} width="970" height={cardH} rx={th.radius + 8} /></clipPath>
              <g clipPath="url(#newsclip)">
                <g transform={`translate(110 80) rotate(${t * 9})`}>{[...Array(14)].map((_, i) => <path key={i} d="M 0 0 L -60 -1100 L 60 -1100 Z" transform={`rotate(${i * (360 / 14)})`} fill={i % 2 ? acc : pal.white} opacity=".3" />)}</g>
                <circle cx="130" cy="230" r={320 + 14 * osc(t, 1.2)} fill={pal.accent2} opacity=".25" />
                <g opacity=".55">{[...Array(9)].map((_, r) => [...Array(9)].map((__, q) => <circle key={r + '-' + q} cx={-480 + q * 120 + (r % 2) * 60 + ((t * 20) % 120)} cy={-cardH / 2 + 40 + r * 120} r="7" fill={pal.wallDark} opacity=".5" />))}</g>
              </g>
            </Panel>
          </g>
          {/* icons column */}
          {icons.map((ic, i) => {
            const t0 = 0.4 + i * 0.26;
            const k = ease.outElastic(prog(t, t0, t0 + 0.5));
            const y = 462 + i * 250;
            return (
              <g key={i} transform={`translate(190 ${y})`}>
                <g transform={`scale(${Math.max(0.01, k)}) rotate(${osc(t, 0.8, i * 0.3) * 4})`}>
                  <circle r="118" fill={iconCols[i % 3]} stroke={pal.ink} strokeWidth={th.uiLine} />
                  <circle r="118" fill="none" stroke="#fff" strokeWidth="6" opacity=".35" strokeDasharray="14 18" transform={`rotate(${t * 40})`} />
                </g>
                <Prop kind={ic} x={0} y={0} scale={0.98} anim={iconAnim(ic)} t0={t0 + 0.15} opacity={clamp((t - t0) * 8)} />
                {t > t0 && t < t0 + 0.5 && <Shockwave x={0} y={0} t0={t0} r={170} color={pal.white} w={14} />}
              </g>
            );
          })}
          <Sparkles n={9} cx={620} cy={620} rx={330} ry={380} color={pal.white} t0={0.5} />
          <Actor role={role} id={who?.id || 'news'} skin={who?.skin} hair={who?.hair} shirt={who?.shirt} number={who?.number} pose="present" emote="happy" x={655 + (1 - fig) * 700} y={1118} scale={1.6} talk={t > 0.5 ? 0.85 : 0} t={t} look={[-0.6, 0.1]} />
          <LowerThird x={110} y={1146} w={880} name={c.name || ''} fact={c.fact || ''} t0={0.42} accent={acc} />
          <Ticker y={1384} h={66} text={c.ticker || ''} t0={0.5} fill={pal.accent2} from="side" />
          {c.dateline && <g transform={`translate(${380 + (1 - card) * -300} 274)`}><Panel x={0} y={0} w={300} h={64} fill={pal.board} r={14}><FitText text={c.dateline} x={0} y={0} w={270} h={44} max={36} maxLines={1} fill={pal.boardInk} font={th.fonts.body} upper={false} /></Panel></g>}
        </g>
      </Stage>
    </>
  );
};
