// HOOK: one punchy question board (sign|neon|stamp|typed|ticket|scoreboard), a reacting cartoon + a big prop, hard graphic hit at the end.
// content: { q, prop, emote, board, role?, bg?, accent? }
import React from 'react';
import {useScene} from '../core/ctx';
import {Background} from '../bg/Backgrounds';
import {Actor} from '../rig/Actor';
import {Prop} from '../props/Prop';
import {Board} from '../ui/Boards';
import {Burst, Confetti, Shockwave, Sparkles, SpeedLines, shakeAt, star} from '../ui/Fx';
import {Stage, useBgKind, ROLE_FOR_HOOK, pickKey} from './common';
import {ease, prog, osc, clamp} from '../core/ease';

export const EMOTE_POSE: Record<string, string> = { neutral: 'idle', happy: 'cheer', shock: 'shock', 'angry-cheeky': 'point', smug: 'shrug', sweat: 'headscratch', sleepy: 'tired', cry: 'cry', love: 'cheer', dizzy: 'shock', sad: 'tired', wink: 'thumbsup' };
const BOARD_Y = 480, HERO_S = 1.6, HERO_Y = 1566; // board box 282..678 (>= 240 even with the push); hero head top 758, clear of the board
const LAND: Record<string, number> = { sign: 0.48, neon: 0.5, stamp: 0.42, typed: 0.3, ticket: 0.64, scoreboard: 0.52 };

export const Hook: React.FC<{ c: any }> = ({ c }) => {
  const sc = useScene();
  const { t, dur, theme: th } = sc, pal = th.palette;
  const bg = useBgKind('HOOK', c.bg);
  const board = c.board || 'sign';
  const role = c.role || pickKey(ROLE_FOR_HOOK, sc.seed);
  const emote = c.emote || 'shock';
  const acc = c.accent || pal.accent;
  const land = LAND[board] ?? 0.5;
  const hitT = Math.max(land + 0.3, dur - 0.55);
  const [sx, sy] = shakeAt(t, land, 14, 0.3);
  const [hx, hy] = shakeAt(t, hitT, 24, 0.3);
  const rise = ease.outBack(prog(t, 0.3, 0.72), 1.6);
  const slideL = (1 - rise) * 800;
  const talking = t > land && t < hitT;
  const propK = ease.outElastic(prog(t, 0.55, 1.0));
  const flash = clamp(1 - (t - hitT) / 0.12) * (t >= hitT ? 0.55 : 0);
  return (
    <>
      <Background kind={bg} shift={Math.sin(t) * 20} />
      <Stage style={{ transform: `translate(${sx + hx}px, ${sy + hy}px)` }}>
        <SpeedLines cx={540} cy={520} n={30} color={acc} opacity={0.22} r0={300} r1={1500} speed={0.7} />
        {t > hitT - 0.02 && <><Burst x={540} y={720} r={420} t0={hitT} color={acc} rot={-8} /><Shockwave x={540} y={720} t0={hitT} r={900} color={pal.white} w={26} /></>}
        {t > land && <Shockwave x={540} y={540} t0={land} r={560} color={acc} />}
        {/* prop spotlight disc */}
        <g transform={`translate(800 1170)`}>
          <circle r={280 * propK} fill={acc} opacity=".28" />
          <circle r={215 * propK * (1 + 0.04 * osc(t, 2.5))} fill={pal.white} opacity=".5" stroke={pal.ink} strokeWidth={th.uiLine} />
        </g>
        {/* sparkles live BEHIND the prop and the board text */}
        <Sparkles n={7} cx={800} cy={1160} rx={280} ry={280} color={acc} t0={0.6} size={1.2} />
        <Prop kind={c.prop || 'question'} x={800} y={1170} scale={2.2} anim="pop" t0={0.55} rot={-6} text={c.prop_text} />
        <Actor role={role} id="hook" pose={EMOTE_POSE[emote] || 'shock'} emote={emote} x={320} y={HERO_Y} scale={HERO_S} talk={talking ? 0.9 : 0} t={t} look={[0.5, -0.2]} flip={false} />
        {/* floating question marks react */}
        {[0, 1, 2].map((i) => <Prop key={i} kind="question" x={570 + i * 100} y={850 + (i % 2) * 40} scale={0.42} anim="orbit" t0={0.5 + i * 0.08} opacity={clamp((t - 0.5 - i * 0.08) * 6) * 0.95} />)}
        {t > hitT && <Confetti n={26} t0={hitT} mode="burst" cx={540} />}
        {/* the question board is drawn LAST (above hero, confetti, sparkles). Its settled box is y>=240, entry is a scale slam, never a drop from above */}
        <Board kind={board} text={c.q} x={540} y={BOARD_Y} w={board === 'stamp' ? 880 : 940} h={board === 'stamp' ? 380 : 396} t0={0.2} accent={acc} max={140} maxLines={4} />
        <rect width="1080" height="1920" fill="#fff" opacity={flash * 0.6} />
      </Stage>
    </>
  );
};
