// Shared template helpers: deterministic defaults, emote/role pickers, SVG stage.
import React from 'react';
import {useScene} from '../core/ctx';
import {hashStr, pick} from '../core/rng';

export const Stage: React.FC<{ children: React.ReactNode; style?: React.CSSProperties }> = ({ children, style }) => (
  <svg width={1080} height={1920} viewBox="0 0 1080 1920" style={{ position: 'absolute', left: 0, top: 0, ...style }}>{children}</svg>
);
export const BG_BY_TYPE: Record<string, string[]> = {
  HOOK: ['stadium', 'studio', 'night-city', 'pitch', 'press-room', 'street'],
  NEWS: ['studio', 'stadium', 'press-room', 'street', 'office'],
  INTERVIEW: ['press-room', 'studio', 'tunnel', 'stadium'],
  PROVOC: ['plain-colour', 'night-city', 'podium', 'pub', 'sky'],
  STATS: ['plain-colour', 'sky', 'training', 'pitch'],
};
export const useBgKind = (type: string, explicit?: string) => {
  const sc = useScene();
  if (explicit) return explicit;
  const list = BG_BY_TYPE[type] || BG_BY_TYPE.HOOK;
  return list[(sc.no * 3 + hashStr(sc.seqId)) % list.length];
};
export const MOOD_EMOTE: Record<string, [string, string]> = {
  cheeky: ['wink', 'angry-cheeky'], smug: ['smug', 'sweat'], shock: ['shock', 'shock'], love: ['love', 'sad'], fun: ['happy', 'wink'], angry: ['angry-cheeky', 'sweat'], sleepy: ['sleepy', 'smug'],
};
export const ROLE_FOR_HOOK = ['fan', 'pundit', 'striker', 'reporter', 'coach', 'kid'];
export const pickKey = <T,>(arr: T[], k: string) => pick(arr, hashStr(k));

import {lookOf} from '../rig/Actor';
import {ROLE_DEFS} from '../rig/roles';
export interface CastFig { id: string; role: string; skin?: string; hair?: string; shirt?: string; number?: string | number }
/** Who is this figure? An explicit cast id wins; else a cast id equal to a word of `name` ("Luka Modric" -> cast.modric). The figure then looks EXACTLY like the comic character (same id => same hair style, colours, number). */
export const castFor = (cast: Record<string, any>, explicit?: string, name?: string): CastFig | null => {
  let id: string | undefined = explicit && cast[explicit] ? explicit : undefined;
  if (!id && name) {
    const words = name.toLowerCase().replace(/[^a-z0-9 ]+/g, ' ').split(/\s+/).filter(Boolean);
    id = words.slice().reverse().find((w) => cast[w]);
  }
  return id ? { id, role: cast[id].role || 'player', skin: cast[id].skin, hair: cast[id].hair, shirt: cast[id].shirt, number: cast[id].number } : null;
};
/** a second figure that must NOT resemble `other`: different skin, hair colour and hair style (used for the reporter next to the subject) */
export const distinctFrom = (th: any, no: number, id: string, role: string, other: { skin?: string; hair?: string; hairStyle: string }) => {
  const base = lookOf(th, no, id, role);
  const rd = ROLE_DEFS[role] || ROLE_DEFS.player;
  const skins: string[] = th.skins, hairs: string[] = th.hairs;
  const skin = skins.find((c) => c !== other.skin && c !== base.skin) || base.skin;
  const hair = hairs.find((c) => c !== other.hair && c !== base.hair) || base.hair;
  const hairStyle = rd.hair.find((st) => st !== other.hairStyle) || base.hairStyle;
  return { skin: base.skin !== other.skin ? base.skin : skin, hair: base.hair !== other.hair ? base.hair : hair, hairStyle: base.hairStyle !== other.hairStyle ? base.hairStyle : hairStyle };
};
