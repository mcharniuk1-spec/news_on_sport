// Style texture overlays (halftone / paper grain / scanlines / speed lines) + soft vignette. Always drifting so frames differ.
import React from 'react';
import {useScene} from '../core/ctx';
import {SpeedLines} from './Fx';

const grainUri = (seed: number) => `url("data:image/svg+xml;utf8,${encodeURIComponent(`<svg xmlns='http://www.w3.org/2000/svg' width='300' height='300'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2' seed='${seed}' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 0.2  0 0 0 0 0.15  0 0 0 0 0.1  0 0 0 1.1 -0.35'/></filter><rect width='300' height='300' filter='url(%23n)'/></svg>`)}")`;

export const Texture: React.FC = () => {
  const sc = useScene();
  const th = sc.theme;
  const f = sc.frame;
  const base: React.CSSProperties = { position: 'absolute', inset: 0, pointerEvents: 'none' };
  const op = th.textureOpacity;
  return (
    <>
      {th.texture === 'halftone' && <div style={{ ...base, opacity: op, mixBlendMode: 'multiply', backgroundImage: 'radial-gradient(circle, rgba(0,0,0,0.9) 28%, transparent 31%)', backgroundSize: '24px 24px', backgroundPosition: `${(f * 1.5) % 24}px ${(f * 1.1) % 24}px`, WebkitMaskImage: 'linear-gradient(to top, #000 0%, transparent 45%, transparent 70%, #000 100%)', maskImage: 'linear-gradient(to top, #000 0%, transparent 45%, transparent 70%, #000 100%)' }} />}
      {th.texture === 'grain' && <div style={{ ...base, opacity: op, mixBlendMode: 'multiply', backgroundImage: grainUri(3 + (f % 3)), backgroundSize: '300px 300px', backgroundPosition: `${(f * 7) % 300}px ${(f * 5) % 300}px` }} />}
      {th.texture === 'scan' && <div style={{ ...base, opacity: op, backgroundImage: 'repeating-linear-gradient(to bottom, rgba(20,10,60,0.55) 0px, rgba(20,10,60,0.55) 2px, transparent 2px, transparent 6px)', backgroundPosition: `0 ${(f * 2) % 6}px` }} />}
      {th.texture === 'speed' && <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={base}><SpeedLines cx={540} cy={980} n={44} r0={620} r1={1700} opacity={op * 0.55} color="#ffffff" speed={0.5} /></svg>}
      <div style={{ ...base, background: 'radial-gradient(ellipse at 50% 46%, transparent 52%, rgba(20,10,40,0.22) 100%)' }} />
    </>
  );
};
