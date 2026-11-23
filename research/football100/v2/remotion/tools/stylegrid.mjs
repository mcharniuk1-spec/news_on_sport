// Dev helper: one still per (style x type) with generic content -> proves the 9 themes differ. node tools/stylegrid.mjs OUTDIR [frame]
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition, openBrowser} from '@remotion/renderer';
import fs from 'node:fs'; import path from 'node:path'; import {fileURLToPath} from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const out = process.argv[2]; const frame = Number(process.argv[3] || 26); fs.mkdirSync(out, { recursive: true });
const styles = { 'SITCOM-YELLOW': 16, 'CUTOUT-PAPER': 43, 'INK-COMIC': 23, 'ACTION-ANIME': 30, 'RUBBER-SLAPSTICK': 35, 'STRIP-MINIMAL': 61, 'SCIFI-DEADPAN': 70, 'CLEAR-LINE': 93, 'FLAT-POP': 2 };
const C = {
  HOOK: { q: 'Who really owns the trophy?', prop: 'trophy', emote: 'smug', board: 'sign' },
  NEWS: { name: 'Test Player', fact: 'A short fact for the style test', ticker: 'Style test ticker', icons: ['ball', 'boot', 'flag'], role: 'striker' },
  INTERVIEW: { label: 'REPORTER ASKS', bubble: 'Is this a proper test?', answer: { icon: 'check', gesture: 'thumbsup' }, subject: 'Test Player' },
  PROVOC: { q: 'Paper or plastic ball?', a: 'Paper', b: 'Plastic', split: [58, 42], mood: 'fun' },
  STATS: { items: [{ icon: 'stopwatch', value: '90', label: 'Full match' }, { icon: 'ball', value: '3', label: 'Goals scored' }, { icon: 'whistle', value: '2', label: 'Cards shown' }] },
};
const serveUrl = await bundle({ entryPoint: path.join(here, '../src/index.ts') });
const browser = await openBrowser('chrome', { browserExecutable: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
for (const [style, no] of Object.entries(styles)) for (const type of Object.keys(C)) {
  const props = { no, style, seqId: 's01', type, content: C[type], frames24: 42, index: 1, cast: {} };
  const comp = await selectComposition({ serveUrl, id: 'Interlude', inputProps: props, puppeteerInstance: browser });
  await renderStill({ composition: comp, serveUrl, output: path.join(out, `${style}_${type}.png`), frame, inputProps: props, puppeteerInstance: browser });
}
await browser.close({ silent: true });
