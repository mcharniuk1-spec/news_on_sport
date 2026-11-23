// Auto-fit text: greedy word wrap measured with a canvas; shrinks the font until it fits box w x h.
let _ctx: CanvasRenderingContext2D | null = null;
const cache = new Map<string, FitResult>();
export interface FitResult { lines: string[]; fontSize: number; lineHeight: number; width: number; height: number }

const measure = (text: string, font: string, size: number, weight: string, spacing: number) => {
  if (!_ctx) _ctx = document.createElement('canvas').getContext('2d');
  const c = _ctx as CanvasRenderingContext2D;
  c.font = `${weight} ${size}px ${font}`;
  return c.measureText(text).width + spacing * size * Math.max(0, text.length - 1);
};

function wrap(words: string[], maxW: number, font: string, size: number, weight: string, spacing: number): string[] {
  const lines: string[] = [];
  let cur = '';
  for (const w of words) {
    const test = cur ? cur + ' ' + w : w;
    if (measure(test, font, size, weight, spacing) <= maxW || !cur) cur = test; else { lines.push(cur); cur = w; }
  }
  if (cur) lines.push(cur);
  return lines;
}

/** fitText('Does Croatia belong here?', 800, 380, FONT, {max:150, min:44, maxLines:3}) */
export function fitText(text: string, boxW: number, boxH: number, font: string, o: { max?: number; min?: number; maxLines?: number; weight?: string; lh?: number; spacing?: number } = {}): FitResult {
  const {max = 160, min = 30, maxLines = 4, weight = 'bold', lh = 1.05, spacing = 0} = o;
  const key = [text, boxW, boxH, font, max, min, maxLines, weight, lh, spacing].join('|');
  const hit = cache.get(key);
  if (hit) return hit;
  const words = text.split(/\s+/).filter(Boolean);
  let best: FitResult | null = null;
  for (let size = max; size >= min; size -= 2) {
    const lines = wrap(words, boxW, font, size, weight, spacing);
    if (lines.length > maxLines) continue;
    const widest = Math.max(...lines.map((l) => measure(l, font, size, weight, spacing)));
    const height = lines.length * size * lh;
    // a single over-long word must not overflow either
    if (widest <= boxW && height <= boxH) { best = {lines, fontSize: size, lineHeight: size * lh, width: widest, height}; break; }
  }
  if (!best) {
    const size = min;
    const lines = wrap(words, boxW, font, size, weight, spacing);
    const widest = Math.max(...lines.map((l) => measure(l, font, size, weight, spacing)));
    // last resort: scale down by shrinking font so width fits
    const k = Math.min(1, boxW / Math.max(1, widest), boxH / Math.max(1, lines.length * size * lh));
    const fs = Math.max(14, Math.floor(size * k));
    best = {lines: wrap(words, boxW, font, fs, weight, spacing), fontSize: fs, lineHeight: fs * lh, width: Math.min(widest, boxW), height: lines.length * fs * lh};
  }
  cache.set(key, best);
  return best;
}
export const textWidth = measure;
