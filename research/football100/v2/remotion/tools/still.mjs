// Dev helper: render stills of any registered composition. node tools/still.mjs --id RigSheet --props '{"mode":"pose"}' --frames 10,40 --out /tmp/x
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const a = process.argv.slice(2); const arg = (k, d) => { const i = a.indexOf('--' + k); return i >= 0 ? a[i + 1] : d; };
const id = arg('id', 'Interlude');
let props = JSON.parse(arg('props', '{}'));
const H = path.resolve(here, '../../..');
const seqArg = arg('seq', null);
const contentArg = arg('content', null);
if (contentArg && seqArg) {
  const ct = JSON.parse(fs.readFileSync(contentArg, 'utf8'));
  const nno = String(ct.no).padStart(3, '0');
  const plan = JSON.parse(fs.readFileSync(path.join(H, 'codex/v2/plan.json'), 'utf8'))[nno];
  const idx = plan.sequences.findIndex((s) => s.id === seqArg);
  const ps = plan.sequences[idx];
  props = { no: ct.no, style: plan.style, seqId: ps.id, type: ps.type, content: ct.sequences[ps.id], frames24: ps.frames, index: idx, cast: ct.cast || {}, prop: ct.prop, accent: ct.accent };
}
const frames = arg('frames', '10').split(',').map(Number);
const out = arg('out', '/tmp/still'); fs.mkdirSync(out, { recursive: true });
const name = arg('name', id);
const scale = Number(arg('scale', '1'));
const serveUrl = await bundle({ entryPoint: path.join(here, '../src/index.ts') });
const opts = { browserExecutable: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' };
const comp = await selectComposition({ serveUrl, id, inputProps: props, ...opts });
for (const f of frames) {
  const file = path.join(out, `${name}_${String(f).padStart(3, '0')}.png`);
  await renderStill({ composition: comp, serveUrl, output: file, frame: Math.min(f, comp.durationInFrames - 1), inputProps: props, scale, onBrowserLog: (l) => console.log('BROWSER', l.type, String(l.text).slice(0, 300)), ...opts });
  console.log(file);
}
