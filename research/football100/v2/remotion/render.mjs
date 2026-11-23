#!/usr/bin/env node
// render.mjs -- node render.mjs --content H/v2/content/NNN.json [--only s01,s03] [--out H/v2/seq/NNN] [--concurrency 2]
// Bundles once, renders each requested sequence to <out>/sKK.mp4 (H.264 yuv420p 1080x1920 30fps, no audio, CRF 16, faststart),
// prints one JSON line per sequence: {"seq":"s01","frames":45,"sec":12.3,"ok":true}
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition, openBrowser} from '@remotion/renderer';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const H = path.resolve(here, '../..');                       // football100 root
const args = process.argv.slice(2);
const arg = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const contentPath = arg('content');
if (!contentPath) { console.error('usage: node render.mjs --content H/v2/content/NNN.json [--only s01,s03] [--out DIR] [--concurrency 2]'); process.exit(2); }
const content = JSON.parse(fs.readFileSync(path.resolve(contentPath), 'utf8'));
const no = content.no;
const nno = String(no).padStart(3, '0');
const outDir = path.resolve(arg('out', path.join(H, 'v2/seq', nno)));
const only = arg('only', '') ? arg('only').split(',') : null;
const concurrency = Number(arg('concurrency', '2'));
const crf = Number(arg('crf', '16'));
const plan = JSON.parse(fs.readFileSync(path.join(H, 'codex/v2/plan.json'), 'utf8'))[nno];
if (!plan) { console.error(`video ${nno} not in plan.json`); process.exit(2); }
fs.mkdirSync(outDir, { recursive: true });

const CHROME = process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const browserExecutable = fs.existsSync(CHROME) ? CHROME : undefined;
const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), `f100-${nno}-`));
const serveUrl = await bundle({ entryPoint: path.join(here, 'src/index.ts'), outDir: path.join(tmpRoot, 'bundle') });
const browser = await openBrowser('chrome', { browserExecutable, chromiumOptions: {}, chromeMode: undefined });

let failed = 0;
for (let index = 0; index < plan.sequences.length; index++) {
  const ps = plan.sequences[index];
  if (only && !only.includes(ps.id)) continue;
  const entry = content.sequences?.[ps.id];
  if (!entry) { console.log(JSON.stringify({ seq: ps.id, ok: false, error: 'missing in content' })); failed++; continue; }
  const inputProps = { no, style: plan.style, seqId: ps.id, type: ps.type, content: entry, frames24: ps.frames, index, cast: content.cast || {}, prop: content.prop, accent: content.accent };
  const t0 = Date.now();
  const tmpOut = path.join(tmpRoot, `${ps.id}.mp4`);
  try {
    const comp = await selectComposition({ serveUrl, id: 'Interlude', inputProps, puppeteerInstance: browser });
    await renderMedia({
      composition: comp, serveUrl, codec: 'h264', outputLocation: tmpOut, inputProps, puppeteerInstance: browser,
      crf, pixelFormat: 'yuv420p', colorSpace: 'bt709', muted: true, concurrency, x264Preset: 'medium', logLevel: 'error',
    });
    // faststart remux (stream copy; keeps pixel data untouched)
    const fin = path.join(outDir, `${ps.id}.mp4`);
    const tmpFinal = fin + '.part.mp4';
    const r = spawnSync('ffmpeg', ['-y', '-v', 'error', '-i', tmpOut, '-c', 'copy', '-an', '-movflags', '+faststart', tmpFinal]);
    if (r.status !== 0) throw new Error('ffmpeg remux failed: ' + r.stderr);
    fs.renameSync(tmpFinal, fin);
    console.log(JSON.stringify({ seq: ps.id, frames: comp.durationInFrames, sec: +((Date.now() - t0) / 1000).toFixed(1), ok: true }));
  } catch (e) {
    failed++;
    console.log(JSON.stringify({ seq: ps.id, ok: false, error: String(e && e.message ? e.message : e).slice(0, 400) }));
  }
}
await browser.close({ silent: true }).catch(() => {});
fs.rmSync(tmpRoot, { recursive: true, force: true });
process.exit(failed ? 1 : 0);
