// <Interlude/> : the shared composition. inputProps {no, style, seqId, type, content, frames24, index, cast?, prop?}
//  - theme from style label (+ per-video variant), deterministic transitions IN/OUT (0.25 s each), slow camera push, style texture.
import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig} from 'remotion';
import {SceneCtx, Scene} from './core/ctx';
import {getTheme} from './theme/themes';
import {TEMPLATES} from './templates';
import {TransitionLayer} from './transitions/transitions';
import {TRANSITIONS} from './core/vocab';
import {Texture} from './ui/Texture';

export interface InterludeProps { no: number; style: string; seqId: string; type: string; content: any; frames24: number; index: number; cast?: Record<string, any>; prop?: string; accent?: string }
export const FPS = 30;
export const TRANS_FRAMES = 8; // 0.25 s (7.5 frames) rounded up so cover is exactly 0 / 1 on the boundary frames

export const transitionPair = (no: number, index: number) => {
  const n = TRANSITIONS.length;
  const a = (no * 2 + index * 4) % n;
  const b = (a + 7 + (no % 3)) % n;
  return [TRANSITIONS[a], TRANSITIONS[b], (no + index) % 2 === 1] as const;
};

export const Interlude: React.FC<InterludeProps> = (props) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const theme = getTheme(props.style, props.no, props.content?.accent || props.accent);
  const t = frame / FPS;
  const scene: Scene = { theme, frame, fps: FPS, t, dur: durationInFrames / FPS, seed: `${props.no}-${props.seqId}`, no: props.no, seqId: props.seqId, W: 1080, H: 1920, cast: props.cast || {}, prop: props.prop };
  const Tpl = TEMPLATES[props.type] || TEMPLATES.HOOK;
  const [tin, tout, mirror] = transitionPair(props.no, props.index);
  const inP = frame / (TRANS_FRAMES - 1);
  const outP = (frame - (durationInFrames - TRANS_FRAMES)) / (TRANS_FRAMES - 1);
  const push = 1 + 0.035 * (frame / Math.max(1, durationInFrames - 1)) + (frame < TRANS_FRAMES ? 0.05 * (1 - frame / TRANS_FRAMES) : 0);
  const boil = theme.boil;
  return (
    <SceneCtx.Provider value={scene}>
      <AbsoluteFill style={{ background: theme.palette.board, overflow: 'hidden' }}>
        {boil > 0 && (
          <svg width="0" height="0" style={{ position: 'absolute' }}>
            <filter id="boil" x="-2%" y="-2%" width="104%" height="104%"><feTurbulence type="turbulence" baseFrequency="0.014" numOctaves="2" seed={1 + (Math.floor(frame / 2) % 9)} result="n" /><feDisplacementMap in="SourceGraphic" in2="n" scale={boil * 2.2} xChannelSelector="R" yChannelSelector="G" /></filter>
          </svg>
        )}
        <div style={{ position: 'absolute', inset: 0, transform: `scale(${push})`, transformOrigin: '50% 46%', filter: boil > 0 ? 'url(#boil)' : undefined }}>
          <Tpl c={props.content || {}} />
        </div>
        <Texture />
        {frame < TRANS_FRAMES && <TransitionLayer id={tin} phase="in" p={inP} pal={theme.palette} seed={scene.seed} t={t} mirror={mirror} />}
        {frame >= durationInFrames - TRANS_FRAMES && <TransitionLayer id={tout} phase="out" p={outP} pal={theme.palette} seed={scene.seed} t={t} mirror={!mirror} />}
      </AbsoluteFill>
    </SceneCtx.Provider>
  );
};
