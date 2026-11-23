import React from 'react';
import {Composition} from 'remotion';
import {Interlude, InterludeProps, FPS} from './Interlude';
import {RigSheet, PropSheet, BgSheet} from './dev/Sheets';

const defaults: InterludeProps = { no: 1, style: 'FLAT-POP', seqId: 's01', type: 'HOOK', content: { q: 'Is this the question?', prop: 'trophy', emote: 'shock', board: 'sign' }, frames24: 36, index: 0 };

export const Root: React.FC = () => (
  <>
    <Composition
      id="Interlude" component={Interlude as any} width={1080} height={1920} fps={FPS} durationInFrames={45}
      defaultProps={defaults as any}
      calculateMetadata={({ props }: any) => ({ durationInFrames: Math.max(8 * 2 + 1, Math.round((props.frames24 / 24) * FPS)), fps: FPS, width: 1080, height: 1920 })}
    />
    <Composition id="RigSheet" component={RigSheet} width={1080} height={1920} fps={FPS} durationInFrames={60} defaultProps={{}} />
    <Composition id="PropSheet" component={PropSheet} width={1080} height={1920} fps={FPS} durationInFrames={60} defaultProps={{}} />
    <Composition id="BgSheet" component={BgSheet} width={1080} height={1920} fps={FPS} durationInFrames={60} defaultProps={{}} />
  </>
);
