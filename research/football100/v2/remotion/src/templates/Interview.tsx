// INTERVIEW: mixed-zone mini scene. cartoon reporter (generic mic) asks, caricature subject answers with a gesture + icon, no words.
// content: { label:'REPORTER ASKS', bubble, answer:{icon, gesture}, subject (board name), reporter_role?, subject_role?, bg?, accent? }
import React from 'react';
import {useScene} from '../core/ctx';
import {Background} from '../bg/Backgrounds';
import {Actor, lookOf} from '../rig/Actor';
import {Prop} from '../props/Prop';
import {Panel, Bubble} from '../ui/Boards';
import {FitText} from '../ui/Txt';
import {Sparkles, Shockwave, Burst, shakeAt} from '../ui/Fx';
import {Stage, useBgKind, castFor, distinctFrom} from './common';
import {ease, prog, osc, clamp} from '../core/ease';

export const Interview: React.FC<{ c: any }> = ({ c }) => {
  const sc = useScene();
  const { t, dur, theme: th } = sc, pal = th.palette;
  const bg = useBgKind('INTERVIEW', c.bg);
  const acc = c.accent || pal.accent;
  const ans = c.answer || { icon: 'thumbs-up', gesture: 'shrug' };
  const tAns = Math.min(dur - 0.55, 0.95);
  const rep = ease.outBack(prog(t, 0.1, 0.5), 1.6), sub = ease.outBack(prog(t, 0.2, 0.6), 1.6);
  const iconK = ease.outElastic(prog(t, tAns, tAns + 0.5));
  const lab = ease.outBack(prog(t, 0.12, 0.45), 2);
  const [sx, sy] = shakeAt(t, tAns, 8, 0.3);
  const nameK = ease.outBack(prog(t, 0.3, 0.65), 1.8);
  // the subject IS the comic character (cast id from `subject_cast` or a word of the name board: "Luka Modric" -> cast.modric);
  // the reporter is deliberately a different-looking person (other hair colour/style/skin) so the roles never read swapped.
  const who = castFor(sc.cast, c.subject_cast, c.subject);
  const subRole = who?.role || c.subject_role || 'striker';
  const subId = who?.id || 'subject';
  const subLook = lookOf(th, sc.no, subId, subRole, { skin: who?.skin, hair: who?.hair, shirt: who?.shirt });
  const repRole = c.reporter_role || 'reporter';
  const repLook = distinctFrom(th, sc.no, 'reporter', repRole, subLook);
  const isQuestion = String(c.bubble || '').trim().endsWith('?');
  const quoteK = ease.outBack(prog(t, 0.42, 0.66), 2);
  const SUB_X = 790, FEET = 1372, NAME_Y = 1450;
  return (
    <>
      <Background kind={bg} shift={Math.sin(t * 0.7) * 30} />
      <Stage>
        <g transform={`translate(${sx} ${sy})`}>
          {/* label strip */}
          <g transform={`translate(540 ${300}) rotate(${-2 + osc(t, 0.7) * 0.6}) scale(${Math.max(0.01, lab)})`}>
            <Panel x={0} y={0} w={700} h={96} fill={acc} r={th.radius}><rect x="-340" y="-4" width="0" height="0" /></Panel>
            <FitText text={c.label || 'REPORTER ASKS'} x={0} y={0} w={640} h={70} max={66} maxLines={1} fill={pal.ink} />
          </g>
          {/* characters */}
          <Actor role={repRole} id="reporter" skin={repLook.skin} hair={repLook.hair} hairStyle={repLook.hairStyle} pose="present" emote="happy" x={250 - (1 - rep) * 700} y={FEET} scale={1.36} talk={t > 0.35 && t < tAns ? 0.9 : 0} hold={{ kind: 'microphone', hand: 'R', scale: 0.52, rot: 28, dy: -6 }} t={t} look={[0.6, 0]} />
          <Actor role={subRole} id={subId} skin={who?.skin} hair={who?.hair} shirt={who?.shirt} number={who?.number} pose={[['idle', 0], [ans.gesture || 'shrug', tAns]]} emote={t > tAns ? (ans.emote || 'smug') : 'neutral'} x={SUB_X + (1 - sub) * 700} y={FEET} scale={1.4} t={t} look={[-0.6, 0]} flip={false} talk={t > tAns + 0.2 ? 0.2 : 0} />
          <Bubble x={540} y={480} w={900} h={210} text={c.bubble || ''} tail={[290, 760]} t0={0.32} max={64} maxLines={3} />
          {!isQuestion && t > 0.4 && <g transform={`translate(82 376) scale(${Math.max(0.01, quoteK)})`}><circle r="42" fill={acc} stroke={pal.ink} strokeWidth={th.uiLine} /><text y="27" textAnchor="middle" fontFamily={th.fonts.display} fontWeight="bold" fontSize="92" fill={pal.ink}>{'\u201C'}</text></g>}
          {/* answer icon: floor space BETWEEN the figures, clear of the microphone and the tunnel light */}
          <g transform={`translate(540 ${1196 - 14 * osc(t, 1.2)})`}>
            {t > tAns && <>
              <circle r={142 * Math.max(0, iconK)} fill={pal.white} stroke={pal.ink} strokeWidth={th.uiLine} />
              <circle r={142 * Math.max(0, iconK)} fill={acc} opacity=".35" />
              <Prop kind={ans.icon} x={0} y={0} scale={1.15 * Math.max(0.01, iconK)} t0={tAns + 0.1} />
            </>}
          </g>
          {t > tAns && <><Shockwave x={540} y={1190} t0={tAns} r={280} color={pal.white} /><Sparkles n={6} cx={540} cy={1190} rx={190} ry={150} color={acc} t0={tAns} size={1.2} /></>}
          {/* subject name board: slides in from the SIDE, bottom edge y<=1493, fully inside x 40..1040 */}
          <g transform={`translate(${SUB_X + (1 - nameK) * 700} ${NAME_Y})`}>
            <Panel x={0} y={0} w={500} h={86} fill={pal.board} r={th.radius * 0.6}><rect x="-240" y="-34" width="10" height="68" fill={acc} /></Panel>
            <FitText text={c.subject || ''} x={10} y={0} w={420} h={62} max={52} maxLines={1} fill={pal.boardInk} font={th.fonts.body} upper={false} />
          </g>
        </g>
      </Stage>
    </>
  );
};
