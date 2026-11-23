// node gen_vocab.mjs  -> writes vocab.json (read by validate.py) and refreshes the generated lists in DSL.md
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const V = await import(path.join(here, 'src/core/vocab.ts'));
const posesSrc = fs.readFileSync(path.join(here, 'src/rig/poses.ts'), 'utf8');
const poses = [...posesSrc.matchAll(/^  ([a-z]+): P\(/gm)].map((m) => m[1]);
const out = {};
for (const [k, v] of Object.entries(V)) out[k] = [...v];
out.POSE_DEFS = poses;
fs.writeFileSync(path.join(here, 'vocab.json'), JSON.stringify(out, null, 1));
// refresh DSL.md blocks: <!--VOCAB:NAME-->...<!--/VOCAB-->
const dslPath = path.join(here, 'DSL.md');
if (fs.existsSync(dslPath)) {
  let s = fs.readFileSync(dslPath, 'utf8');
  s = s.replace(/<!--VOCAB:([A-Z_]+)-->[\s\S]*?<!--\/VOCAB-->/g, (m, name) => {
    const list = out[name];
    if (!list) return m;
    return `<!--VOCAB:${name}-->\n${list.map((x) => '`' + x + '`').join(', ')}  (${list.length})\n<!--/VOCAB-->`;
  });
  fs.writeFileSync(dslPath, s);
}
console.log(Object.entries(out).map(([k, v]) => `${k}:${v.length}`).join(' '));
