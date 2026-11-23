// PLACEHOLDER for type COMIC (agent B replaces this with the real comic engine; see templates/index.ts).
import React from 'react';
import {useScene} from '../core/ctx';
import {Background} from '../bg/Backgrounds';
import {Stage} from './common';
import {FitText} from '../ui/Txt';
import {Panel} from '../ui/Boards';
import {osc} from '../core/ease';

export const Comic: React.FC<{ c: any }> = ({ c }) => {
  const sc = useScene();
  const pal = sc.theme.palette;
  return (
    <>
      <Background kind="plain-colour" />
      <Stage>
        <g transform={`rotate(${osc(sc.t, 1.3) * 3} 540 960)`}>
          <Panel x={540} y={900} w={860} h={520} fill={pal.white} stroke={pal.red}>
            <FitText text="TODO COMIC" x={0} y={-60} w={760} h={220} max={170} maxLines={1} fill={pal.red} upper={false} />
            <FitText text={`${sc.seqId} - comic engine pending`} x={0} y={110} w={760} h={120} max={64} maxLines={2} fill={pal.ink} upper={false} />
          </Panel>
        </g>
      </Stage>
    </>
  );
};
