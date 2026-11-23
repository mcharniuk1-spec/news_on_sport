// TEXT BOARDS: sign, neon, stamp, typed, ticket, scoreboard  (<Board kind=... text=... x y w h t0/>)
// plus Panel, Bubble, LowerThird, Ticker, PollBar and countStr. Every text goes through FitText: it never overflows its box.
import React from 'react';
import {useScene} from '../core/ctx';
import {FitText, weightFor} from './Txt';
import {fitText, textWidth} from '../core/text';
import {ease, prog, osc, TAU, clamp} from '../core/ease';
import {mix, shade, alpha} from '../core/color';
import {rand01} from '../core/rng';
import {shakeAt, star} from './Fx';

export const Panel: React.FC<{ x: number; y: number; w: number; h: number; fill?: string; stroke?: string; r?: number; sw?: number; shadow?: boolean; rot?: number; children?: React.ReactNode; opacity?: number }> = ({ x, y, w, h, fill, stroke, r, sw, shadow = true, rot = 0, children, opacity = 1 }) => {
  const th = useScene().theme, pal = th.palette;
  const rr = r ?? th.radius, s = sw ?? th.uiLine;
  return (
    <g transform={`translate(${x} ${y}) rotate(${rot})`} opacity={opacity}>
      {shadow && th.shadowStyle !== 'none' && <rect x={-w / 2 + (th.shadowStyle === 'hard' ? 10 : 0)} y={-h / 2 + (th.shadowStyle === 'hard' ? 12 : 14)} width={w} height={h} rx={rr} fill={th.shadowStyle === 'hard' ? 'rgba(0,0,0,0.3)' : 'rgba(30,20,50,0.22)'} />}
      <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={rr} fill={fill || pal.board} stroke={stroke || pal.ink} strokeWidth={s} strokeLinejoin="round" />
      {children}
    </g>
  );
};

export interface BoardProps { kind: string; text: string; x: number; y: number; w: number; h: number; t0?: number; accent?: string; max?: number; maxLines?: number }
export const Board: React.FC<BoardProps> = ({ kind, text, x, y, w, h, t0 = 0, accent, max = 150, maxLines = 4 }) => {
  const sc = useScene();
  const th = sc.theme, pal = th.palette, t = sc.t, tl = t - t0;
  const acc = accent || pal.accent;
  const pad = 46;
  const tw = w - pad * 2, thh = h - pad * 1.6;
  const idle = 1 + 0.012 * osc(t, 1.1);
  if (kind === 'sign') {
    // SLAM by scale/squash (never translate from above: the top 12 % must stay free of text)
    const k = prog(tl, 0, 0.34);
    const sk = Math.max(0.01, ease.outBack(k, 1.5));
    const sqx = 1 + 0.16 * (1 - k) * Math.sin(k * 14), sqy = 1 - 0.16 * (1 - k) * Math.sin(k * 14);
    const ang = (tl > 0.28 ? 5 * Math.sin((tl - 0.28) * 9) * Math.exp(-(tl - 0.28) * 2.2) : 0) + 1.3 * osc(t, 0.8);
    const wire = 56;
    return (
      <g transform={`translate(${x} ${y}) scale(${sk * sqx} ${sk * sqy}) rotate(${ang} 0 ${-h / 2 - wire})`}>
        {[-1, 1].map((s) => <g key={s}><path d={`M ${s * w * 0.32} ${-h / 2 - wire} L ${s * w * 0.32} ${-h / 2 + 8}`} stroke={pal.ink} strokeWidth="14" strokeLinecap="round" /><path d={`M ${s * w * 0.32} ${-h / 2 - wire} L ${s * w * 0.32} ${-h / 2 + 8}`} stroke={pal.metal} strokeWidth="7" strokeDasharray="22 10" strokeLinecap="round" /></g>)}
        <Panel x={0} y={0} w={w} h={h} fill={pal.board}>
          <rect x={-w / 2 + 16} y={-h / 2 + 16} width={w - 32} height={h - 32} rx={Math.max(6, th.radius - 14)} fill="none" stroke={acc} strokeWidth="5" opacity=".85" />
          {[[-1, -1], [1, -1], [-1, 1], [1, 1]].map(([a, b], i) => <circle key={i} cx={a * (w / 2 - 36)} cy={b * (h / 2 - 36)} r="9" fill={pal.metal} stroke={pal.ink} strokeWidth="3" />)}
        </Panel>
        <FitText text={text} x={0} y={0} w={tw} h={thh} max={max} maxLines={maxLines} fill={pal.boardInk} />
      </g>
    );
  }
  if (kind === 'neon') {
    const letters = text.length;
    const on = Math.floor(clamp(tl / 0.28) * letters);
    const flick = tl < 0.3 ? (Math.sin(tl * 80) > -0.3 ? 1 : 0.35) : 0.92 + 0.08 * Math.sin(t * 31) * (Math.sin(t * 3.1) > 0.8 ? 3 : 1);
    const pop = ease.outBack(prog(tl, 0, 0.25), 1.5);
    const nc = mix(acc, '#ffffff', 0.15);
    return (
      <g transform={`translate(${x} ${y}) scale(${Math.max(0.01, pop) * idle})`}>
        <Panel x={0} y={0} w={w} h={h} fill={shade(pal.ink, -0.08)} stroke={pal.ink}>
          {[...Array(7)].map((_, r) => <path key={r} d={`M ${-w / 2 + 8} ${-h / 2 + 30 + r * (h / 7)} L ${w / 2 - 8} ${-h / 2 + 30 + r * (h / 7)}`} stroke="#fff" strokeWidth="2" opacity=".07" />)}
          <rect x={-w / 2 + 22} y={-h / 2 + 22} width={w - 44} height={h - 44} rx={th.radius} fill="none" stroke={nc} strokeWidth="9" opacity={0.85 * flick} style={{ filter: `drop-shadow(0 0 12px ${acc}) drop-shadow(0 0 28px ${acc})` }} />
        </Panel>
        <g opacity={flick} style={{ filter: `drop-shadow(0 0 10px ${acc}) drop-shadow(0 0 26px ${acc})` }}>
          <FitText text={text} x={0} y={0} w={tw - 20} h={thh - 20} max={max} maxLines={maxLines} fill={mix(acc, '#fff', 0.78)} stroke={nc} strokeW={5} chars={on} />
        </g>
      </g>
    );
  }
  if (kind === 'stamp') {
    const k = prog(tl, 0, 0.17);
    const s = 1 + 0.16 * Math.pow(1 - k, 2); // slam kept small: a board scaled up from its centre must not enter the top 12 %
    const [sx, sy] = shakeAt(t, t0 + 0.17, 18, 0.35);
    const rot = -5 + (1 - k) * 18;
    const ink = mix(pal.red, pal.ink, 0.12);
    const splats = [...Array(9)].map((_, i) => ({ a: rand01(sc.seed + 'st', i) * TAU, d: w * 0.5 + rand01(sc.seed + 'st', i + 20) * 70, r: 6 + rand01(sc.seed + 'st', i + 40) * 12 }));
    if (tl < 0) return null;
    return (
      <g transform={`translate(${x + sx} ${y + sy}) rotate(${rot}) scale(${s})`} opacity={clamp(k * 8)}>
        <rect x={-w / 2 - 18} y={-h / 2 - 18} width={w + 36} height={h + 36} rx={th.radius} fill="none" stroke={ink} strokeWidth="10" opacity=".9" />
        <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={th.radius * 0.6} fill={alpha(pal.white, 0.92)} stroke={ink} strokeWidth="12" />
        <rect x={-w / 2 + 20} y={-h / 2 + 20} width={w - 40} height={h - 40} rx={th.radius * 0.4} fill="none" stroke={ink} strokeWidth="4" />
        <FitText text={text} x={0} y={0} w={tw} h={thh} max={max} maxLines={maxLines} fill={ink} />
        {k >= 1 && splats.map((sp, i) => <circle key={i} cx={Math.cos(sp.a) * sp.d * 1.2} cy={Math.sin(sp.a) * sp.d * 0.55} r={sp.r * Math.min(1, (tl - 0.17) * 8)} fill={ink} opacity=".75" />)}
      </g>
    );
  }
  if (kind === 'typed') {
    const total = text.length;
    const cps = total / Math.max(0.25, Math.min(0.78, sc.dur * 0.5) - t0);
    const chars = clamp(tl, 0, 9) * cps;
    const fit = fitText(text, tw, thh, th.fonts.mono, { max: Math.min(max, 120), maxLines, weight: 'bold', lh: 1.15 });
    const shown = Math.floor(chars);
    // caret position (text is left-aligned inside the sheet so letters never jump while typing)
    let rem = shown, cl = 0, cx0 = 0;
    for (let i = 0; i < fit.lines.length; i++) { const L = fit.lines[i]; if (rem <= L.length + 1 || i === fit.lines.length - 1) { cl = i; cx0 = textWidth(L.slice(0, Math.max(0, rem)), th.fonts.mono, fit.fontSize, 'bold', 0); break; } rem -= L.length + 1; }
    const sl = ease.outBack(prog(tl, 0, 0.25), 1.2);
    const totalH = fit.lineHeight * fit.lines.length;
    const ty = -totalH / 2 + fit.lineHeight * (cl + 0.5);
    return (
      <g transform={`translate(${x} ${y}) rotate(${-2.5 + 0.6 * osc(t, 0.7) + (1 - sl) * 14}) scale(${idle * Math.max(0.02, sl)})`}>
        <Panel x={0} y={0} w={w} h={h} fill={pal.white} r={10} sw={th.uiLine}>
          {[...Array(Math.floor(h / 46))].map((_, i) => <path key={i} d={`M ${-w / 2 + 24} ${-h / 2 + 50 + i * 46} L ${w / 2 - 24} ${-h / 2 + 50 + i * 46}`} stroke={pal.skyTop} strokeWidth="2" opacity=".6" />)}
          <path d={`M ${-w / 2 + 60} ${-h / 2} L ${-w / 2 + 60} ${h / 2}`} stroke={pal.red} strokeWidth="3" opacity=".35" />
        </Panel>
        <FitText text={text} x={0} y={0} w={tw} h={thh} max={Math.min(max, 120)} maxLines={maxLines} fill={pal.ink} font={th.fonts.mono} upper={false} chars={shown} spacing={0} skew={0} align="start" />
        <rect x={-tw / 2 + cx0 + 2} y={ty - fit.fontSize * 0.5} width={fit.fontSize * 0.5} height={fit.fontSize} fill={pal.red} opacity={Math.floor(t * 5) % 2 ? 0.95 : 0.25} />
      </g>
    );
  }
  if (kind === 'ticket') {
    const k = prog(tl, 0, 0.4);
    const e = ease.outBack(k, 1.4);
    const tx = (1 - e) * 1200, rot = (1 - e) * 20 - 3 + 1.2 * osc(t, 0.9);
    const body = acc;
    const d = `M ${-w / 2} ${-h / 2} L ${w / 2} ${-h / 2} L ${w / 2} ${-h * 0.12} Q ${w / 2 - h * 0.12} 0 ${w / 2} ${h * 0.12} L ${w / 2} ${h / 2} L ${-w / 2} ${h / 2} L ${-w / 2} ${h * 0.12} Q ${-w / 2 + h * 0.12} 0 ${-w / 2} ${-h * 0.12} Z`;
    const shine = ((t * 0.7) % 1.6) - 0.3;
    return (
      <g transform={`translate(${x + tx} ${y}) rotate(${rot})`}>
        <path d={d} transform="translate(10 14)" fill="rgba(30,20,50,0.22)" />
        <path d={d} fill={body} stroke={pal.ink} strokeWidth={th.uiLine} strokeLinejoin="round" />
        <path d={`M ${-w / 2 + w * 0.2} ${-h / 2 + 8} L ${-w / 2 + w * 0.2} ${h / 2 - 8}`} stroke={pal.ink} strokeWidth="5" strokeDasharray="14 12" opacity=".7" />
        <polygon points={star(5, h * 0.18, h * 0.075)} transform={`translate(${-w / 2 + w * 0.1} 0) rotate(${t * 40})`} fill={pal.white} stroke={pal.ink} strokeWidth="4" />
        <clipPath id={'tkc' + x}><path d={d} /></clipPath>
        <g clipPath={`url(#tkc${x})`}><rect x={-w / 2 + shine * w} y={-h} width="70" height={h * 2} fill="#fff" opacity=".28" transform={`skewX(-20)`} /></g>
        <FitText text={text} x={w * 0.1} y={0} w={w * 0.7} h={thh} max={max} maxLines={maxLines} fill={pal.ink} />
      </g>
    );
  }
  // scoreboard
  const letters = text.length;
  const on = Math.floor(clamp(tl / 0.34) * letters);
  const k = ease.outBack(prog(tl, 0, 0.3), 1.6);
  const bulbs = Math.floor(w / 54);
  return (
    <g transform={`translate(${x} ${y}) scale(${Math.max(0.01, k) * idle})`}>
      <Panel x={0} y={0} w={w} h={h} fill={shade(pal.board, 0.15)} r={Math.min(th.radius, 24)}>
        <rect x={-w / 2 + 26} y={-h / 2 + 26} width={w - 52} height={h - 52} rx="10" fill={shade(pal.ink, -0.05)} stroke={pal.metal} strokeWidth="6" />
        {[...Array(bulbs)].map((_, i) => <circle key={i} cx={-w / 2 + 26 + (i + 0.5) * ((w - 52) / bulbs)} cy={-h / 2 + 14} r="7" fill={pal.gold} opacity={0.35 + 0.65 * Math.max(0, osc(t, 2, i / bulbs))} />)}
        {[...Array(bulbs)].map((_, i) => <circle key={i} cx={-w / 2 + 26 + (i + 0.5) * ((w - 52) / bulbs)} cy={h / 2 - 14} r="7" fill={pal.gold} opacity={0.35 + 0.65 * Math.max(0, osc(t, 2, -i / bulbs))} />)}
      </Panel>
      <FitText text={text} x={0} y={0} w={tw - 24} h={thh - 28} max={max} maxLines={maxLines} fill={pal.gold} font={th.fonts.display} chars={on} stroke={shade(pal.gold, 0.45)} strokeW={3} />
    </g>
  );
};

export const Bubble: React.FC<{ x: number; y: number; w: number; h: number; text: string; tail: [number, number]; t0?: number; thought?: boolean; fill?: string; max?: number; maxLines?: number; children?: React.ReactNode }> = ({ x, y, w, h, text, tail, t0 = 0, thought, fill, max = 70, maxLines = 4, children }) => {
  const sc = useScene();
  const th = sc.theme, pal = th.palette;
  const k = ease.outBack(prog(sc.t - t0, 0, 0.3), 2);
  if (sc.t < t0) return null;
  const [tx, ty] = tail;
  const ang = Math.atan2(ty - y, tx - x);
  const bx = x + Math.cos(ang) * (w / 2) * 0.55, by = y + Math.sin(ang) * (h / 2) * 0.75;
  const pul = 1 + 0.012 * osc(sc.t, 1.4);
  const dx = tx - bx, dy = ty - by, len = Math.hypot(dx, dy) || 1, nx = -dy / len, ny = dx / len;
  return (
    <g transform={`translate(${tx} ${ty}) scale(${Math.max(0.01, k) * pul}) translate(${-tx} ${-ty})`}>
      {thought ? <>{[0.3, 0.55, 0.78].map((f, i) => <circle key={i} cx={bx + dx * f} cy={by + dy * f} r={10 + (2 - i) * 6} fill={fill || pal.white} stroke={pal.ink} strokeWidth={th.uiLine * 0.7} />)}</> : (
        <path d={`M ${bx + nx * 30} ${by + ny * 30} L ${tx} ${ty} L ${bx - nx * 30} ${by - ny * 30} Z`} fill={fill || pal.white} stroke={pal.ink} strokeWidth={th.uiLine} strokeLinejoin="round" />
      )}
      <rect x={x - w / 2} y={y - h / 2} width={w} height={h} rx={Math.min(h / 2, th.radius + 16)} fill={fill || pal.white} stroke={pal.ink} strokeWidth={th.uiLine} />
      {!thought && <path d={`M ${bx + nx * 24} ${by + ny * 24} L ${bx - nx * 24} ${by - ny * 24}`} stroke={fill || pal.white} strokeWidth={th.uiLine + 3} />}
      {children ?? <FitText text={text} x={x} y={y} w={w - 56} h={h - 36} max={max} maxLines={maxLines} fill={pal.ink} font={th.fonts.body} upper={false} />}
    </g>
  );
};

export const LowerThird: React.FC<{ x: number; y: number; w: number; name: string; fact: string; t0?: number; accent?: string }> = ({ x, y, w, name, fact, t0 = 0, accent }) => {
  const sc = useScene();
  const th = sc.theme, pal = th.palette, t = sc.t, tl = t - t0;
  const acc = accent || pal.accent;
  const e1 = ease.outBack(prog(tl, 0, 0.32), 1.7), e2 = ease.outBack(prog(tl, 0.1, 0.44), 1.7);
  const shine = ((t * 0.9) % 1.8) - 0.4;
  const nh = 104, fh = 112;
  return (
    <g>
      <g transform={`translate(${x - (1 - e1) * 1200} ${y})`}>
        <path d={`M 0 0 L ${w} 0 L ${w - 26} ${nh} L -26 ${nh} Z`} transform="translate(8 12)" fill="rgba(30,20,50,0.25)" />
        <path d={`M 0 0 L ${w} 0 L ${w - 26} ${nh} L -26 ${nh} Z`} fill={acc} stroke={pal.ink} strokeWidth={th.uiLine} strokeLinejoin="round" />
        <clipPath id={'lt1' + sc.seed}><path d={`M 0 0 L ${w} 0 L ${w - 26} ${nh} L -26 ${nh} Z`} /></clipPath>
        <g clipPath={`url(#lt1${sc.seed})`}><rect x={shine * w} y={-10} width="60" height={nh + 20} fill="#fff" opacity=".4" transform="skewX(-20)" /></g>
        <FitText text={name} x={w / 2 - 12} y={nh / 2} w={w - 90} h={nh - 22} max={78} maxLines={1} fill={pal.ink} />
      </g>
      <g transform={`translate(${x + 30 + (1 - e2) * 1200} ${y + nh + 8})`}>
        <path d={`M 0 0 L ${w - 20} 0 L ${w - 46} ${fh} L -26 ${fh} Z`} transform="translate(8 12)" fill="rgba(30,20,50,0.25)" />
        <path d={`M 0 0 L ${w - 20} 0 L ${w - 46} ${fh} L -26 ${fh} Z`} fill={pal.board} stroke={pal.ink} strokeWidth={th.uiLine} strokeLinejoin="round" />
        <rect x="-4" y="0" width={14} height={fh} fill={pal.accent2} transform="skewX(-13)" />
        <FitText text={fact} x={(w - 20) / 2 - 20} y={fh / 2} w={w - 120} h={fh - 20} max={52} maxLines={2} fill={pal.boardInk} font={th.fonts.body} upper={false} />
      </g>
    </g>
  );
};

export const Ticker: React.FC<{ y: number; h?: number; text: string; speed?: number; fill?: string; ink?: string; t0?: number; from?: 'side' | 'below' }> = ({ y, h = 78, text, speed = 260, fill, ink, t0 = 0, from = 'side' }) => {
  const sc = useScene();
  const th = sc.theme, pal = th.palette;
  const f = fill || pal.accent2;
  const unit = fitText(text.toUpperCase() === text ? text : text, 2000, h - 20, th.fonts.body, { max: h - 24, min: 20, maxLines: 1, weight: 'bold' });
  const label = th.upper ? text.toUpperCase() : text;
  const wd = unit.width + 110;
  const off = (((sc.t - t0) * speed) % wd);
  const slide = ease.outCubic(prog(sc.t - t0, 0, 0.3));
  const reps = Math.ceil(1200 / wd) + 2;
  return (
    <g transform={from === 'below' ? `translate(0 ${(1 - slide) * 160})` : `translate(${(1 - slide) * -1200} 0)`}>
      <rect x="-20" y={y} width="1120" height={h} fill={f} stroke={pal.ink} strokeWidth={th.uiLine} />
      <clipPath id={'tk' + sc.seed}><rect x="0" y={y} width="1080" height={h} /></clipPath>
      <g clipPath={`url(#tk${sc.seed})`}>
        {[...Array(reps)].map((_, i) => (
          <g key={i} transform={`translate(${i * wd - off} ${y + h / 2})`}>
            <text x="0" y="0" dominantBaseline="central" fontFamily={th.fonts.body} fontWeight="bold" fontSize={unit.fontSize} fill={ink || pal.ink}>{label}</text>
            <polygon points={star(4, 18, 6)} transform={`translate(${unit.width + 54} 0) rotate(${sc.t * 120})`} fill={ink || pal.ink} />
          </g>
        ))}
      </g>
    </g>
  );
};

export const countStr = (value: string, k: number): string => value.replace(/\d+(\.\d+)?/g, (m) => { const n = parseFloat(m); const dec = m.includes('.') ? m.split('.')[1].length : 0; return (n * clamp(k)).toFixed(dec); });

export const PollBar: React.FC<{ x: number; y: number; w: number; h: number; label: string; letter: string; pct: number; color: string; t0?: number; win?: boolean }> = ({ x, y, w, h, label, letter, pct, color, t0 = 0, win }) => {
  const sc = useScene();
  const th = sc.theme, pal = th.palette, t = sc.t, tl = t - t0;
  const slide = ease.outBack(prog(tl, 0, 0.3), 1.6);
  const fill = ease.outBack(prog(tl, 0.18, 0.75), 1.25);
  const pw = Math.max(0, (w - 30) * (pct / 100) * fill);
  const pulse = win && tl > 0.8 ? 1 + 0.025 * osc(t, 3) : 1;
  const shown = countStr(String(pct), fill);
  return (
    <g transform={`translate(${x + (1 - slide) * (x < 540 ? -1200 : 1200)} ${y}) scale(${pulse})`}>
      <rect x={-w / 2 + 10} y={-h / 2 + 14} width={w} height={h} rx={h / 2.4} fill="rgba(30,20,50,0.22)" />
      <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={h / 2.4} fill={pal.white} stroke={pal.ink} strokeWidth={th.uiLine} />
      <clipPath id={'pb' + letter + sc.seed}><rect x={-w / 2} y={-h / 2} width={w} height={h} rx={h / 2.4} /></clipPath>
      <g clipPath={`url(#pb${letter}${sc.seed})`}>
        <rect x={-w / 2} y={-h / 2} width={15 + pw} height={h} fill={color} />
        <rect x={-w / 2 + ((t * 120) % 140) - 140 + pw * 0} y={-h / 2} width="40" height={h} fill="#fff" opacity=".22" transform="skewX(-20)" />
      </g>
      <rect x={-w / 2} y={-h / 2} width={w} height={h} rx={h / 2.4} fill="none" stroke={pal.ink} strokeWidth={th.uiLine} />
      <circle cx={-w / 2 + h / 2} cy="0" r={h * 0.34} fill={pal.board} stroke={pal.ink} strokeWidth={th.uiLine * 0.7} />
      <text x={-w / 2 + h / 2} y="2" textAnchor="middle" dominantBaseline="central" fontFamily={th.fonts.display} fontWeight={weightFor(th.fonts.display)} fontSize={h * 0.42} fill={pal.boardInk}>{letter}</text>
      <FitText text={label} x={-w / 2 + h * 1.0 + (w * 0.46) / 2 - 10} y={0} w={w * 0.46} h={h * 0.62} max={64} maxLines={2} fill={pal.ink} stroke={pal.white} strokeW={win ? 0 : 0} align="start" />
      <text x={w / 2 - 34} y="4" textAnchor="end" dominantBaseline="central" fontFamily={th.fonts.display} fontWeight={weightFor(th.fonts.display)} fontSize={h * 0.5} fill={pal.ink} stroke={pal.white} strokeWidth={h * 0.07} paintOrder="stroke">{shown}%</text>
    </g>
  );
};
