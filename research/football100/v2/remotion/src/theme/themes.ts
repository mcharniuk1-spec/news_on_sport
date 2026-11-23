// THEME SYSTEM: nine style labels -> palette, people colours, line weight, texture, motion personality, fonts.
// Every drawing component reads colours ONLY from the theme (via useScene().theme), so one rig / one prop library is re-skinned.
export type EyeStyle = 'dot' | 'big' | 'anime' | 'tiny' | 'dots' | 'pie' | 'ink' | 'clear';
export interface Palette {
  ink: string; white: string; gold: string; red: string; blue: string; green: string; purple: string; orange: string; pink: string; teal: string; brown: string;
  skyTop: string; skyBot: string; grassA: string; grassB: string; wall: string; wallDark: string; floor: string; crowdA: string; crowdB: string;
  board: string; boardInk: string; accent: string; accent2: string; metal: string;
}
export interface Theme {
  id: string;
  palette: Palette;
  skins: string[]; hairs: string[]; shirts: string[];
  line: number;            // outline width in design units (rig scale 1 == 540px tall figure)
  uiLine: number;          // outline width of boards/UI in px
  texture: 'none' | 'halftone' | 'grain' | 'scan' | 'speed' | 'lines';
  textureOpacity: number;
  eye: EyeStyle;
  limb: 'straight' | 'rubber';
  cutout: boolean;         // paper edge (white rim + drop shadow) instead of plain outline
  boil: number;            // px of hand-drawn line boil (feTurbulence displacement); 0 = off
  shadowStyle: 'soft' | 'hard' | 'none';
  radius: number;          // UI corner radius
  fonts: { display: string; body: string; mono: string };
  titleSkew: number;       // deg, italic feel for headline text
  titleSpacing: number;    // letter spacing (em)
  upper: boolean;          // uppercase headline text
  motion: { overshoot: number; speed: number; breathe: number; sway: number; squash: number; jitter: number; shake: number };
  headScale: number;       // rig head size multiplier
}

const base: Palette = {
  ink: '#211c32', white: '#fffaf0', gold: '#ffd66e', red: '#e87575', blue: '#4c80b5', green: '#7fcf9f', purple: '#7a5fb0', orange: '#f4a259', pink: '#f29cb3', teal: '#3fb8af', brown: '#8a5a3c',
  skyTop: '#8eb8d6', skyBot: '#cfe3ef', grassA: '#7fcf9f', grassB: '#6bbf8e', wall: '#cfe0f0', wallDark: '#4c80b5', floor: '#2e4a6b', crowdA: '#e87575', crowdB: '#ffd66e',
  board: '#2d2a4a', boardInk: '#ffffff', accent: '#ffd66e', accent2: '#e87575', metal: '#b8c2cc',
};
const P = (o: Partial<Palette>): Palette => ({ ...base, ...o });

export const FONT = {
  rounded: '"Arial Rounded MT Bold","Arial Black",Impact,sans-serif',
  black: '"Arial Black","Arial Bold",Impact,sans-serif',
  impact: 'Impact,"Haettenschweiler","Arial Black",sans-serif',
  din: '"DIN Condensed","DIN Alternate","Avenir Next Condensed",Impact,sans-serif',
  comic: '"Comic Sans MS","Marker Felt","Chalkboard SE",sans-serif',
  marker: '"Marker Felt","Comic Sans MS",sans-serif',
  slab: 'Rockwell,"Rockwell Extra Bold","Georgia",serif',
  serif: 'Georgia,"Times New Roman",serif',
  trebuchet: '"Trebuchet MS","Verdana",sans-serif',
  mono: '"Courier New",Courier,Menlo,monospace',
};

const SKIN_MIX = ['#ffd88a', '#f6b481', '#e3a373', '#b97a4f', '#8d5a3b', '#f2c6a0'];
const HAIR_MIX = ['#3a2a2a', '#1e1b2b', '#7a4a2a', '#c98b3a', '#d9d4c7', '#a03a2a', '#2b3a5a'];

export const THEMES: Record<string, Theme> = {
  'FLAT-POP': {
    id: 'FLAT-POP', palette: base,
    skins: SKIN_MIX, hairs: HAIR_MIX, shirts: ['#7a5fb0', '#3fb8af', '#e87575', '#4c80b5', '#f4a259', '#f29cb3', '#ffd66e'],
    line: 6, uiLine: 6, texture: 'none', textureOpacity: 0, eye: 'dot', limb: 'straight', cutout: false, boil: 0, shadowStyle: 'soft', radius: 36,
    fonts: { display: FONT.black, body: FONT.rounded, mono: FONT.mono }, titleSkew: 0, titleSpacing: 0, upper: false,
    motion: { overshoot: 1.0, speed: 1, breathe: 1, sway: 1, squash: 1, jitter: 0, shake: 1 }, headScale: 1,
  },
  'SITCOM-YELLOW': {
    id: 'SITCOM-YELLOW',
    palette: P({ skyTop: '#9fd3f2', skyBot: '#e6f4fb', grassA: '#9fdc7a', grassB: '#8ccf68', wall: '#f7e7b2', wallDark: '#e8b04a', floor: '#6a8fb8', board: '#2f3a63', gold: '#ffd23f', red: '#f0645c', blue: '#4f8fd6', green: '#7ccf5f', purple: '#8a6fd0', orange: '#ff9a3c', accent: '#ffd23f', accent2: '#f0645c', crowdA: '#f0645c', crowdB: '#4f8fd6' }),
    skins: ['#ffd23f', '#ffd23f', '#ffd23f', '#ffd23f', '#ffd23f', '#ffd23f'], hairs: ['#6b4a2a', '#2a2a3a', '#d9a05a', '#8d5a3b', '#c9c9d0', '#a84a2a', '#1e1b2b'],
    shirts: ['#e8505b', '#4f8fd6', '#7ccf5f', '#8a6fd0', '#ff9a3c', '#3fb8af', '#f6f1e3'],
    line: 5, uiLine: 6, texture: 'none', textureOpacity: 0, eye: 'dot', limb: 'straight', cutout: false, boil: 0, shadowStyle: 'soft', radius: 40,
    fonts: { display: FONT.rounded, body: FONT.rounded, mono: FONT.mono }, titleSkew: 0, titleSpacing: 0, upper: false,
    motion: { overshoot: 1.2, speed: 1, breathe: 1, sway: 1, squash: 1.1, jitter: 0, shake: 1 }, headScale: 1.04,
  },
  'CUTOUT-PAPER': {
    id: 'CUTOUT-PAPER',
    palette: P({ ink: '#3a2e2a', white: '#fbf3e0', skyTop: '#e9d9b4', skyBot: '#f4ead0', grassA: '#8fae78', grassB: '#7e9d68', wall: '#efe0bd', wallDark: '#c9743f', floor: '#8a6a4a', board: '#c9743f', boardInk: '#fbf3e0', gold: '#e9b949', red: '#cf5a43', blue: '#4f7f9c', green: '#7e9d68', purple: '#8a6a8f', orange: '#d98a3a', pink: '#dc8f8a', teal: '#4a9a8a', brown: '#8a6a4a', crowdA: '#cf5a43', crowdB: '#4f7f9c', accent: '#e9b949', accent2: '#cf5a43', metal: '#b9b09c' }),
    skins: ['#f0c8a0', '#e0a97c', '#c58a5e', '#a06a46'], hairs: ['#4a3426', '#2a2220', '#8a5a34', '#c8a05a', '#d8d0c0'],
    shirts: ['#cf5a43', '#4f7f9c', '#e9b949', '#4a9a8a', '#8a6a8f', '#d98a3a'],
    line: 3, uiLine: 4, texture: 'grain', textureOpacity: 0.22, eye: 'dots', limb: 'straight', cutout: true, boil: 1.6, shadowStyle: 'hard', radius: 14,
    fonts: { display: FONT.slab, body: FONT.slab, mono: FONT.mono }, titleSkew: 0, titleSpacing: 0.01, upper: false,
    motion: { overshoot: 0.5, speed: 0.9, breathe: 0.7, sway: 0.7, squash: 0.3, jitter: 1, shake: 0.7 }, headScale: 1,
  },
  'INK-COMIC': {
    id: 'INK-COMIC',
    palette: P({ ink: '#0d0d14', white: '#fffdf2', skyTop: '#2a62d6', skyBot: '#8fc2ff', grassA: '#2fae5f', grassB: '#27994f', wall: '#ffd21f', wallDark: '#d62a2a', floor: '#1a1a2e', board: '#0d0d14', boardInk: '#ffd21f', gold: '#ffd21f', red: '#e0262a', blue: '#1f58d6', green: '#2fae5f', purple: '#7a3fb8', orange: '#ff8a1f', pink: '#ff6fa3', teal: '#1fb5c0', crowdA: '#e0262a', crowdB: '#1f58d6', accent: '#ffd21f', accent2: '#e0262a', metal: '#aab4c2' }),
    skins: ['#f5c9a0', '#e4a577', '#c98255', '#9a6240'], hairs: ['#0d0d14', '#3a2418', '#8a4a1a', '#d4b040', '#e8e8e8'],
    shirts: ['#e0262a', '#1f58d6', '#ffd21f', '#2fae5f', '#7a3fb8', '#ff8a1f'],
    line: 9, uiLine: 9, texture: 'halftone', textureOpacity: 0.3, eye: 'ink', limb: 'straight', cutout: false, boil: 0, shadowStyle: 'hard', radius: 10,
    fonts: { display: FONT.impact, body: FONT.impact, mono: FONT.mono }, titleSkew: -6, titleSpacing: 0.02, upper: true,
    motion: { overshoot: 1.1, speed: 1.2, breathe: 0.8, sway: 1, squash: 0.7, jitter: 0, shake: 1.4 }, headScale: 0.96,
  },
  'ACTION-ANIME': {
    id: 'ACTION-ANIME',
    palette: P({ ink: '#14122b', white: '#ffffff', skyTop: '#1c1f5e', skyBot: '#ff5fa8', grassA: '#2fd3a0', grassB: '#22b88a', wall: '#2a2f8a', wallDark: '#14122b', floor: '#1b1e5a', board: '#14122b', boardInk: '#ffffff', gold: '#ffe14a', red: '#ff3b5c', blue: '#3b8bff', green: '#2fd3a0', purple: '#8a4bff', orange: '#ff8a3b', pink: '#ff7bb5', teal: '#27d3e0', crowdA: '#ff3b5c', crowdB: '#3b8bff', accent: '#ffe14a', accent2: '#ff3b5c', metal: '#c4ccff' }),
    skins: ['#ffe0c8', '#f6c8a0', '#e0a278', '#b57e56'], hairs: ['#ff3b5c', '#3b8bff', '#ffe14a', '#2fd3a0', '#14122b', '#8a4bff', '#ffffff'],
    shirts: ['#ff3b5c', '#3b8bff', '#ffe14a', '#2fd3a0', '#8a4bff', '#ff8a3b'],
    line: 6, uiLine: 6, texture: 'speed', textureOpacity: 0.5, eye: 'anime', limb: 'straight', cutout: false, boil: 0, shadowStyle: 'none', radius: 18,
    fonts: { display: FONT.din, body: FONT.din, mono: FONT.mono }, titleSkew: -10, titleSpacing: 0.03, upper: true,
    motion: { overshoot: 0.8, speed: 1.4, breathe: 0.6, sway: 1.3, squash: 0.5, jitter: 0, shake: 1.6 }, headScale: 0.98,
  },
  'RUBBER-SLAPSTICK': {
    id: 'RUBBER-SLAPSTICK',
    palette: P({ ink: '#2a1d14', white: '#fff6e0', skyTop: '#f2d9a0', skyBot: '#fbeccb', grassA: '#8bb35a', grassB: '#7ba34a', wall: '#f3dca8', wallDark: '#b8532f', floor: '#7a4a2a', board: '#7a2f20', boardInk: '#fff6e0', gold: '#f2b83a', red: '#d9452f', blue: '#3a7ab0', green: '#7ba34a', purple: '#8a5a8f', orange: '#e8802f', pink: '#e8908a', teal: '#3a9a8a', brown: '#7a4a2a', crowdA: '#d9452f', crowdB: '#f2b83a', accent: '#f2b83a', accent2: '#d9452f', metal: '#b8aa90' }),
    skins: ['#ffe3c4', '#ffe3c4', '#ffd8b0', '#f0c090'], hairs: ['#2a1d14', '#2a1d14', '#7a4a2a', '#c8a050', '#2a1d14'],
    shirts: ['#d9452f', '#3a7ab0', '#f2b83a', '#7ba34a', '#8a5a8f', '#e8802f'],
    line: 8, uiLine: 8, texture: 'grain', textureOpacity: 0.12, eye: 'pie', limb: 'rubber', cutout: false, boil: 0.8, shadowStyle: 'soft', radius: 28,
    fonts: { display: FONT.black, body: FONT.comic, mono: FONT.mono }, titleSkew: 0, titleSpacing: 0, upper: false,
    motion: { overshoot: 1.8, speed: 1.1, breathe: 1.2, sway: 1.4, squash: 1.8, jitter: 0, shake: 1.2 }, headScale: 1.02,
  },
  'STRIP-MINIMAL': {
    id: 'STRIP-MINIMAL',
    palette: P({ ink: '#2b2b33', white: '#fbf8ef', skyTop: '#f3efe6', skyBot: '#f3efe6', grassA: '#dfead0', grassB: '#d4e2c4', wall: '#f3efe6', wallDark: '#cfd8e0', floor: '#e4ded0', board: '#fbf8ef', boardInk: '#2b2b33', gold: '#f2d27a', red: '#e58a7a', blue: '#8ab0d6', green: '#a8cfa0', purple: '#b8a8d6', orange: '#f0b27a', pink: '#f0b8c4', teal: '#8acfc4', brown: '#b09478', crowdA: '#e58a7a', crowdB: '#8ab0d6', accent: '#f2d27a', accent2: '#e58a7a', metal: '#cfd0d4' }),
    skins: ['#fbf3e4', '#f6e8d2', '#efdcc2'], hairs: ['#2b2b33', '#2b2b33', '#6b5a4a', '#2b2b33'],
    shirts: ['#e58a7a', '#8ab0d6', '#f2d27a', '#a8cfa0', '#b8a8d6'],
    line: 4, uiLine: 4, texture: 'grain', textureOpacity: 0.1, eye: 'dots', limb: 'straight', cutout: false, boil: 2.4, shadowStyle: 'none', radius: 8,
    fonts: { display: FONT.comic, body: FONT.comic, mono: FONT.mono }, titleSkew: 0, titleSpacing: 0, upper: false,
    motion: { overshoot: 0.35, speed: 0.8, breathe: 0.6, sway: 0.6, squash: 0.2, jitter: 0.6, shake: 0.5 }, headScale: 0.94,
  },
  'SCIFI-DEADPAN': {
    id: 'SCIFI-DEADPAN',
    palette: P({ ink: '#2a2540', white: '#f4f1ff', skyTop: '#b9a8f0', skyBot: '#e7e0ff', grassA: '#8fe0b8', grassB: '#7ad0a8', wall: '#d8d0f5', wallDark: '#6a5fb8', floor: '#3a3470', board: '#2a2540', boardInk: '#9ff5d0', gold: '#f5d36a', red: '#ff7f9c', blue: '#6aa8ff', green: '#8fe0b8', purple: '#9a7aff', orange: '#ffa86a', pink: '#ffb0d0', teal: '#5adbd0', crowdA: '#ff7f9c', crowdB: '#6aa8ff', accent: '#9ff5d0', accent2: '#ff7f9c', metal: '#c4c0e0' }),
    skins: ['#f0d8c8', '#c8e8d8', '#e8c8e8', '#d8d8f0', '#f5e0a8'], hairs: ['#2a2540', '#6a5fb8', '#5adbd0', '#ff7f9c', '#f4f1ff'],
    shirts: ['#6aa8ff', '#ff7f9c', '#f5d36a', '#8fe0b8', '#9a7aff', '#ffa86a'],
    line: 4, uiLine: 5, texture: 'scan', textureOpacity: 0.18, eye: 'tiny', limb: 'straight', cutout: false, boil: 2.0, shadowStyle: 'soft', radius: 22,
    fonts: { display: FONT.din, body: FONT.trebuchet, mono: FONT.mono }, titleSkew: 0, titleSpacing: 0.05, upper: true,
    motion: { overshoot: 0.5, speed: 0.85, breathe: 0.8, sway: 0.8, squash: 0.3, jitter: 0.4, shake: 0.6 }, headScale: 1.05,
  },
  'CLEAR-LINE': {
    id: 'CLEAR-LINE',
    palette: P({ ink: '#1d2a3a', white: '#fff9ec', skyTop: '#8cc8e8', skyBot: '#e9f3e8', grassA: '#8cc07a', grassB: '#7bb06a', wall: '#f2e6c4', wallDark: '#c24a3a', floor: '#9a7a5a', board: '#1d3a5a', boardInk: '#fff9ec', gold: '#e8b83a', red: '#c24a3a', blue: '#2a6aa8', green: '#6aa85a', purple: '#7a5a9a', orange: '#e08a3a', pink: '#e0908a', teal: '#3a9a98', brown: '#8a6a4a', crowdA: '#c24a3a', crowdB: '#2a6aa8', accent: '#e8b83a', accent2: '#c24a3a', metal: '#b0b8c0' }),
    skins: ['#f7d2b0', '#f0c09a', '#e0a880', '#a87a58'], hairs: ['#d89a3a', '#5a3a22', '#1d2a3a', '#a0522d', '#d0c8b8'],
    shirts: ['#c24a3a', '#2a6aa8', '#e8b83a', '#3a9a98', '#7a5a9a', '#e08a3a'],
    line: 4, uiLine: 5, texture: 'none', textureOpacity: 0, eye: 'clear', limb: 'straight', cutout: false, boil: 0, shadowStyle: 'none', radius: 12,
    fonts: { display: FONT.serif, body: FONT.serif, mono: FONT.mono }, titleSkew: 0, titleSpacing: 0.01, upper: false,
    motion: { overshoot: 0.6, speed: 0.9, breathe: 0.8, sway: 0.8, squash: 0.4, jitter: 0, shake: 0.7 }, headScale: 0.98,
  },
};

// Per-video variety for the big FLAT-POP family (and subtle for others): override palette tokens by (no % n).
const FLAT_POP_VARIANTS: Partial<Palette>[] = [
  {},
  { skyTop: '#b9a9e8', skyBot: '#e3dcf7', wall: '#e3dcf7', wallDark: '#7a5fb0', floor: '#3b2f63', board: '#33285a', accent: '#ffd66e', grassA: '#9ad6a8', grassB: '#86c898' },
  { skyTop: '#f5b69a', skyBot: '#fde3d3', wall: '#fde3d3', wallDark: '#d9704f', floor: '#6b3a33', board: '#4a2a34', accent: '#ffe08a', grassA: '#a4d68a', grassB: '#92c878' },
  { skyTop: '#8fd6c0', skyBot: '#d3f0e5', wall: '#d3f0e5', wallDark: '#2f8f7c', floor: '#1f4b47', board: '#1f3b44', accent: '#ffd66e', crowdA: '#f29cb3', crowdB: '#ffd66e' },
  { skyTop: '#ffd66e', skyBot: '#fff0b8', wall: '#fff0b8', wallDark: '#e8a43a', floor: '#5a4630', board: '#3a2f4a', accent: '#e87575', grassA: '#9ad67a', grassB: '#86c868' },
  { skyTop: '#6f8fe0', skyBot: '#c4d2f7', wall: '#c4d2f7', wallDark: '#3a52a8', floor: '#1e2a5a', board: '#1e2250', accent: '#ffd66e', crowdA: '#ff8a8a', crowdB: '#9bd3b2' },
];

export function getTheme(style: string, no: number, accent?: string): Theme {
  let th = THEMES[style] || THEMES['FLAT-POP'];
  if (th.id === 'FLAT-POP') {
    const v = FLAT_POP_VARIANTS[no % FLAT_POP_VARIANTS.length];
    th = { ...th, palette: { ...th.palette, ...v } };
  }
  if (accent) th = { ...th, palette: { ...th.palette, accent } };
  return th;
}
