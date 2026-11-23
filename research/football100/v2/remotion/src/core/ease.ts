// Easing + small math helpers. All pure, deterministic.
export const clamp = (x: number, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;
/** progress of t inside [a,b], clamped 0..1 */
export const prog = (t: number, a: number, b: number) => clamp((t - a) / Math.max(1e-6, b - a));
export const TAU = Math.PI * 2;
/** sine oscillator: osc(t, hz, phase01) in -1..1 */
export const osc = (t: number, hz = 1, phase = 0) => Math.sin((t * hz + phase) * TAU);

const c1 = 1.70158;
export const ease = {
  lin: (t: number) => t,
  inQuad: (t: number) => t * t,
  outQuad: (t: number) => 1 - (1 - t) * (1 - t),
  inOutQuad: (t: number) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2),
  outCubic: (t: number) => 1 - Math.pow(1 - t, 3),
  inCubic: (t: number) => t * t * t,
  inOutCubic: (t: number) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2),
  outExpo: (t: number) => (t >= 1 ? 1 : 1 - Math.pow(2, -10 * t)),
  inExpo: (t: number) => (t <= 0 ? 0 : Math.pow(2, 10 * t - 10)),
  outBack: (t: number, s = c1) => 1 + (s + 1) * Math.pow(t - 1, 3) + s * Math.pow(t - 1, 2),
  inBack: (t: number, s = c1) => (s + 1) * t * t * t - s * t * t,
  outElastic: (t: number) => (t <= 0 ? 0 : t >= 1 ? 1 : Math.pow(2, -10 * t) * Math.sin(((t * 10 - 0.75) * TAU) / 3) + 1),
  outBounce: (t: number) => {
    const n1 = 7.5625, d1 = 2.75;
    if (t < 1 / d1) return n1 * t * t;
    if (t < 2 / d1) return n1 * (t -= 1.5 / d1) * t + 0.75;
    if (t < 2.5 / d1) return n1 * (t -= 2.25 / d1) * t + 0.9375;
    return n1 * (t -= 2.625 / d1) * t + 0.984375;
  },
};
/** shorthand: pop-in with overshoot between times a..b (seconds) -> 0..1(+overshoot) */
export const popIn = (t: number, a: number, b: number, s = 2.2) => ease.outBack(prog(t, a, b), s);
/** spring-like settle: damped cosine from 0 to 1 */
export const spring = (t: number, a: number, dur = 0.5, damp = 7, freq = 2.2) => {
  const x = t - a;
  if (x <= 0) return 0;
  if (x >= dur * 3) return 1;
  return 1 - Math.exp(-damp * x) * Math.cos(freq * TAU * x);
};
/** triangle pulse 0..1..0 around centre c with half-width w */
export const bump = (t: number, c: number, w: number) => Math.max(0, 1 - Math.abs(t - c) / w);
/** squash & stretch factors from a vertical velocity-ish value v (-1..1) */
export const squash = (v: number) => ({ sx: 1 + 0.18 * v, sy: 1 - 0.18 * v });
