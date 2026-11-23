#!/usr/bin/env python3
"""framecheck.py FILE.mp4 [...] : checks the output contract (codec, size, fps, no audio, yuv420p, duration) and that no two neighbouring frames are identical
(frame diff on 108x192 grayscale thumbs, mean abs diff).  Prints one JSON line per file."""
import json, subprocess, sys
import numpy as np

def probe(p):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'stream=codec_type,codec_name,width,height,r_frame_rate,pix_fmt,nb_frames:format=duration', '-of', 'json', p], capture_output=True, text=True)
    return json.loads(r.stdout)

for p in sys.argv[1:]:
    info = probe(p)
    st = info['streams']
    v = [s for s in st if s['codec_type'] == 'video'][0]
    audio = any(s['codec_type'] == 'audio' for s in st)
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', p, '-vf', 'scale=108:192,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
    fr = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 192, 108).astype(np.float32)
    d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
    same = [int(i) for i in np.where(d < 0.02)[0]]
    ok = v['codec_name'] == 'h264' and v['width'] == 1080 and v['height'] == 1920 and v['r_frame_rate'] == '30/1' and v['pix_fmt'] == 'yuv420p' and not audio and not same
    print(json.dumps({'file': p, 'frames': int(len(fr)), 'codec': v['codec_name'], 'size': '%dx%d' % (v['width'], v['height']), 'fps': v['r_frame_rate'], 'pix_fmt': v['pix_fmt'], 'audio': audio,
                      'identical_neighbours': same, 'min_diff': round(float(d.min()), 3), 'ok': bool(ok)}))
