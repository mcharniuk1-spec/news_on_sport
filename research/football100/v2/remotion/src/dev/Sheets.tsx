// Dev-only contact sheets (not used in production renders): RigSheet, EmoteSheet, PropSheet, BgSheet.
import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {SceneCtx} from '../core/ctx';
import {getTheme} from '../theme/themes';
import {Actor} from '../rig/Actor';
import {Prop} from '../props/Prop';
import {POSE_NAMES} from '../rig/poses';
import {EMOTE_DEFS} from '../rig/Face';
import {PROPS, ROLES, BGS} from '../core/vocab';
import {Background} from '../bg/Backgrounds';

const useS = (style: string, no: number) => {
  const frame = useCurrentFrame();
  return { theme: getTheme(style, no), frame, fps: 30, t: frame / 30, dur: 2, seed: `${no}-dev`, no, seqId: 'dev', W: 1080, H: 1920, cast: {} } as any;
};

export const RigSheet: React.FC<any> = ({ style = 'FLAT-POP', no = 1, page = 0, mode = 'pose', cols = 4 }) => {
  const S = useS(style, no);
  const names: string[] = mode === 'pose' ? POSE_NAMES : mode === 'role' ? [...ROLES] : Object.keys(EMOTE_DEFS);
  const per = cols * Math.ceil(names.length / cols);
  const rows = Math.ceil(names.length / cols);
  const cw = 1080 / cols, ch = Math.min(1920 / rows, cw * 1.55);
  const scale = ch / 640;
  return (
    <SceneCtx.Provider value={S}>
      <AbsoluteFill style={{ background: S.theme.palette.skyBot }}>
        <svg width="1080" height="1920" viewBox="0 0 1080 1920">
          {names.map((n, i) => {
            const cx = (i % cols) * cw + cw / 2, cy = Math.floor(i / cols) * ch + ch * 0.86;
            const role = mode === 'role' ? n : ROLES[i % ROLES.length];
            return (
              <g key={n}>
                <Actor role={role} pose={mode === 'pose' ? n : mode === 'role' ? 'idle' : 'idle'} emote={mode === 'emote' ? n : mode === 'pose' ? (['happy', 'shock', 'smug', 'neutral'][i % 4]) : 'neutral'} x={cx} y={cy} scale={scale * 1.05} id={n} talk={mode === 'emote' && i % 2 === 0} />
                <text x={cx} y={cy + 24} textAnchor="middle" fontSize="22" fontFamily="Arial Black" fill="#000">{n}{mode === 'pose' ? ' / ' + role : ''}</text>
              </g>
            );
          })}
        </svg>
      </AbsoluteFill>
    </SceneCtx.Provider>
  );
};

export const PropSheet: React.FC<any> = ({ style = 'FLAT-POP', no = 1, page = 0, per = 48, cols = 6 }) => {
  const S = useS(style, no);
  const list = (PROPS as readonly string[]).slice(page * per, page * per + per);
  const cw = 1080 / cols, rows = Math.ceil(per / cols), ch = 1920 / rows;
  return (
    <SceneCtx.Provider value={S}>
      <AbsoluteFill style={{ background: S.theme.palette.skyBot }}>
        <svg width="1080" height="1920" viewBox="0 0 1080 1920">
          {list.map((n, i) => {
            const cx = (i % cols) * cw + cw / 2, cy = Math.floor(i / cols) * ch + ch * 0.45;
            return <g key={n}><Prop kind={n} x={cx} y={cy} scale={cw / 260} text={n === 'scoreboard' ? '7:0' : undefined} /><text x={cx} y={cy + ch * 0.38} textAnchor="middle" fontSize="20" fontFamily="Arial Black" fill="#000">{n}</text></g>;
          })}
        </svg>
      </AbsoluteFill>
    </SceneCtx.Provider>
  );
};

export const BgSheet: React.FC<any> = ({ style = 'FLAT-POP', no = 1, per = 6 , page = 0}) => {
  const S = useS(style, no);
  const list = (BGS as readonly string[]).slice(page * per, page * per + per);
  const cols = 3, rows = 2, cw = 1080 / cols, ch = 1920 / rows;
  return (
    <SceneCtx.Provider value={S}>
      <AbsoluteFill style={{ background: '#222' }}>
        {list.map((n, i) => (
          <div key={n} style={{ position: 'absolute', left: (i % cols) * cw, top: Math.floor(i / cols) * ch, width: cw, height: ch, overflow: 'hidden' }}>
            <div style={{ transform: `scale(${cw / 1080})`, transformOrigin: '0 0', width: 1080, height: 1920 }}><Background kind={n} /></div>
            <div style={{ position: 'absolute', left: 4, top: 4, font: '700 26px Arial Black', color: '#fff', background: '#000a', padding: '2px 8px' }}>{n}</div>
          </div>
        ))}
      </AbsoluteFill>
    </SceneCtx.Provider>
  );
};
