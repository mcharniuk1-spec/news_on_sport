import React, {createContext, useContext} from 'react';
import type {Theme} from '../theme/themes';

export interface Scene {
  theme: Theme;
  frame: number;
  fps: number;
  t: number;            // seconds since clip start
  dur: number;          // clip duration in seconds
  seed: string;         // `${no}-${seqId}`
  no: number;
  seqId: string;
  W: number; H: number;
  cast: Record<string, any>;
  prop?: string;        // recurring comic prop
}
export const SceneCtx = createContext<Scene | null>(null);
export const useScene = (): Scene => {
  const s = useContext(SceneCtx);
  if (!s) throw new Error('useScene outside <SceneCtx.Provider>');
  return s;
};
/** Safe zones in px (see spec section 2). */
export const SAFE = { top: 230, bottom: 1536, left: 40, right: 1040 };
export const W = 1080, H = 1920;
