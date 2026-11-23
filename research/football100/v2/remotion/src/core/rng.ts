// Deterministic PRNG utilities (never Math.random at render time).
export const hashStr = (s: string): number => {
  let h = 2166136261 >>> 0;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
  return h >>> 0;
};
export const mulberry32 = (a: number) => () => {
  a |= 0; a = (a + 0x6d2b79f5) | 0;
  let t = Math.imul(a ^ (a >>> 15), 1 | a);
  t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
};
export const rngFor = (key: string) => mulberry32(hashStr(key));
/** pick deterministic element */
export const pick = <T,>(arr: T[], key: string | number): T => arr[(typeof key === 'number' ? key : hashStr(key)) % arr.length];
/** stable pseudo-random 0..1 from (key, i) */
export const rand01 = (key: string | number, i = 0) => {
  const h = typeof key === 'number' ? key : hashStr(key);
  return mulberry32((h + Math.imul(i + 1, 2654435761)) >>> 0)();
};
