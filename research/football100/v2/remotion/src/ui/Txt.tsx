// Text helpers: <FitText/> auto-fits text into a box (never overflows), theme-aware headline styling.
import React from 'react';
import {useScene} from '../core/ctx';
import {fitText, textWidth} from '../core/text';
import type {Theme} from '../theme/themes';

export const weightFor = (family: string) => (/^"?Impact/i.test(family) ? 'normal' : 'bold');
export const firstFont = (family: string) => family;

export interface FitTextProps {
  text: string; x: number; y: number; w: number; h: number; // box centre (x,y) and size
  font?: string; max?: number; min?: number; maxLines?: number; fill?: string; stroke?: string; strokeW?: number; align?: 'middle' | 'start' | 'end';
  upper?: boolean; lh?: number; skew?: number; spacing?: number; shadow?: string; opacity?: number; weight?: string; rot?: number; chars?: number; valign?: 'middle' | 'top';
}
export const FitText: React.FC<FitTextProps> = (p) => {
  const sc = useScene();
  const th = sc.theme;
  const font = p.font || th.fonts.display;
  const upper = p.upper ?? th.upper;
  const spacing = p.spacing ?? th.titleSpacing;
  const raw = upper ? p.text.toUpperCase() : p.text;
  const text = p.chars !== undefined ? raw.slice(0, Math.max(0, Math.floor(p.chars))) : raw;
  const weight = p.weight || weightFor(font);
  // fit on the FULL text so typing animations don't re-wrap
  const fit = fitText(raw, p.w, p.h, font, { max: p.max, min: p.min, maxLines: p.maxLines, weight, lh: p.lh ?? 1.04, spacing });
  // distribute the visible characters over the pre-wrapped lines
  let remaining = text.length;
  const lines = fit.lines.map((l, i) => { const take = Math.max(0, Math.min(l.length + (i < fit.lines.length - 1 ? 1 : 0), remaining)); remaining -= take; return l.slice(0, take); });
  const totalH = fit.lineHeight * fit.lines.length;
  const y0 = (p.valign === 'top' ? p.y : p.y - totalH / 2) + fit.lineHeight * 0.5;
  const anchor = p.align || 'middle';
  const tx = anchor === 'middle' ? p.x : anchor === 'start' ? p.x - p.w / 2 : p.x + p.w / 2;
  const sk = p.skew ?? th.titleSkew;
  return (
    <g transform={`rotate(${p.rot || 0} ${p.x} ${p.y})`} opacity={p.opacity ?? 1}>
      {lines.map((l, i) => {
        const ly = y0 + i * fit.lineHeight;
        const stableStart = p.chars !== undefined && anchor === 'middle';
        const lx = stableStart ? tx - textWidth(fit.lines[i], font, fit.fontSize, weight, spacing) / 2 : tx;
        return (
          <text key={i} x={lx} y={ly} textAnchor={stableStart ? 'start' : anchor} dominantBaseline="central" fontFamily={font} fontWeight={weight} fontSize={fit.fontSize} fill={p.fill || th.palette.boardInk}
            stroke={p.stroke} strokeWidth={p.strokeW} strokeLinejoin="round" paintOrder="stroke" letterSpacing={`${spacing}em`}
            transform={sk ? `translate(${lx} ${ly}) skewX(${sk}) translate(${-lx} ${-ly})` : undefined}>
            {l}
          </text>
        );
      })}
    </g>
  );
};
