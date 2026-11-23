// PROVOC: two-option vote card. Question board, animated bars filling to the split, ticking percentages, pulsing winner, two reacting fans.
// content: { q (<=7 words), a, b (<=3 words), split:[n,m] (sum 100), mood, bg?, accent? }
import React from 'react';
import {useScene} from '../core/ctx';
import {Background} from '../bg/Backgrounds';
import {Actor} from '../rig/Actor';
import {Prop} from '../props/Prop';
import {Panel, PollBar} from '../ui/Boards';
import {FitText} from '../ui/Txt';
import {Sparkles, Shockwave, Burst, Confetti, shakeAt} from '../ui/Fx';
import {Stage, useBgKind, MOOD_EMOTE} from './common';
import {ease, prog, osc, clamp} from '../core/ease';

export const Provoc: React.FC<{ c: any }> = ({ c }) => {
  const sc = useScene();
  const { t, dur, theme: th } = sc, pal = th.palette;
  const bg = useBgKind('PROVOC', c.bg);
  const acc = c.accent || pal.accent;
  const [pa, pb] = c.split || [50, 50];
  const aWins = pa >= pb;
  const q = ease.outBack(prog(t, 0.08, 0.42), 1.8);
  const [em1, em2] = MOOD_EMOTE[c.mood || 'cheeky'] || MOOD_EMOTE.cheeky;
  const done = 0.18 + 0.75;
  const [sx, sy] = shakeAt(t, done, 8, 0.3);
  const fanK = ease.outBack(prog(t, 0.45, 0.85), 1.7);
  const BAR_X = 490, BAR_W = 880, BADGE_X = 985, wy0 = aWins ? 700 : 920;
  return (
    <>
      <Background kind={bg} shift={Math.sin(t * 0.9) * 22} />
      <Stage>
        <g transform={`translate(${sx} ${sy})`}>
          {/* winner effects first: they sit BEHIND the question board, the bars and every text */}
          {t > done && <Confetti n={18} t0={done} mode="burst" cx={540} />}
          <Sparkles n={6} cx={540} cy={1330} rx={200} ry={100} color={acc} t0={done} />
          {t > done && <Shockwave x={BAR_X} y={wy0} t0={done} r={300} color={pal.white} w={16} />}
          <g transform={`translate(540 395) scale(${Math.max(0.01, q)}) rotate(${(1 - q) * 6 + osc(t, 0.8) * 0.6})`}>
            <Panel x={0} y={0} w={960} h={300} fill={pal.board} r={th.radius}>
              <rect x="-470" y="-135" width="940" height="270" rx={th.radius * 0.6} fill="none" stroke={acc} strokeWidth="5" opacity=".9" />
              {[[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([a, b], i) => <circle key={i} cx={a * 440} cy={b * 118} r="8" fill={acc} opacity={0.5 + 0.5 * Math.abs(osc(t, 2, i * 0.25))} />)}
            </Panel>
            <FitText text={c.q || ''} x={0} y={0} w={840} h={230} max={118} maxLines={3} fill={pal.boardInk} />
          </g>
          <PollBar x={BAR_X} y={700} w={BAR_W} h={196} label={c.a || ''} letter="A" pct={pa} color={pal.red} t0={0.18} win={aWins} />
          <PollBar x={BAR_X} y={920} w={BAR_W} h={196} label={c.b || ''} letter="B" pct={pb} color={pal.blue} t0={0.3} win={!aWins} />
          {/* winner marker: ring around the bar + crown badge in its OWN space right of the bars (not on the board, not on the bar end) */}
          {t > done && <><rect x={BAR_X - BAR_W / 2 - 8} y={wy0 - 106} width={BAR_W + 16} height="212" rx={96} fill="none" stroke={acc} strokeWidth="10" opacity={0.6 + 0.4 * osc(t, 3)} /><Burst x={BADGE_X} y={wy0} r={52} t0={done} color={acc} rot={12} /><Prop kind="crown" x={BADGE_X} y={wy0} scale={0.3} anim="wobble" t0={done} /></>}
          {/* reacting fans: enter from the SIDES, feet settle at y 1500 (inside the safe zone) */}
          <Actor role="fan" id="fanA" pose={aWins && t > done ? 'cheer' : 'shrug'} emote={aWins && t > done ? 'happy' : em1} x={250 - (1 - fanK) * 600} y={1500} scale={0.82} t={t} look={[0.4, -0.3]} />
          <Actor role="fan" id="fanB" pose={!aWins && t > done ? 'cheer' : t > done ? 'facepalm' : 'point'} emote={!aWins && t > done ? 'happy' : em2} x={830 + (1 - fanK) * 600} y={1500} scale={0.82} flip t={t} look={[-0.4, -0.3]} />
        </g>
      </Stage>
    </>
  );
};
