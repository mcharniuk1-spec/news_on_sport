// Dev helper: renders IN (frames 0..6) and OUT frames for all 15 transitions into one contact sheet folder. node tools/transgrid.mjs OUTDIR
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition, openBrowser} from '@remotion/renderer';
import fs from 'node:fs'; import path from 'node:path'; import {fileURLToPath} from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const out = process.argv[2]; fs.mkdirSync(out, { recursive: true });
const serveUrl = await bundle({ entryPoint: path.join(here, '../src/index.ts') });
const browser = await openBrowser('chrome', { browserExecutable: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
for (let index = 0; index < 15; index++) {
  const props = { no: 0, style: 'FLAT-POP', seqId: 's01', type: 'HOOK', content: { q: 'Is this a test?', prop: 'trophy', emote: 'shock', board: 'sign' }, frames24: 36, index, cast: {} };
  const comp = await selectComposition({ serveUrl, id: 'Interlude', inputProps: props, puppeteerInstance: browser });
  const N = comp.durationInFrames;
  for (const f of [0, 1, 2, 3, 4, 5, 6, 7, N - 7, N - 6, N - 5, N - 4, N - 3, N - 2, N - 1]) await renderStill({ composition: comp, serveUrl, output: path.join(out, `t${index}_${f - (f >= N - 7 ? N : 0)}.png`), frame: f, inputProps: props, puppeteerInstance: browser, scale: 0.25 });
}
await browser.close({ silent: true });
