#!/usr/bin/env python3
"""validate.py -- strict safety net for authored content files.

    python3 validate.py H/v2/content/NNN.json [--strict] [--comics-only]

Prints `OK` (exit 0) or a list of precise errors (exit 1).  `todo` comics print a WARN (error with --strict).
Vocabularies come from vocab.json (generated from src/core/vocab.ts by `node gen_vocab.mjs`).
Sections: GENERAL, per-type validators (HOOK NEWS INTERVIEW PROVOC STATS), and a clearly separated COMIC hook (validate_comic).
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
H = os.path.abspath(os.path.join(HERE, '..', '..'))
V = json.load(open(os.path.join(HERE, 'vocab.json')))
S = {k: set(v) for k, v in V.items()}

BANNED = ['bet', 'bets', 'betting', 'bettor', 'odds', 'bookie', 'bookies', 'bookmaker', 'bookmakers', 'wager', 'gamble', 'gambling', 'stake', 'jackpot', 'casino',
          'injury', 'injuries', 'injured', 'ill', 'illness', 'sick', 'disease', 'cancer', 'drug', 'drugs', 'doping', 'cocaine', 'crime', 'criminal', 'arrest', 'arrested', 'prison', 'jail', 'police',
          'family', 'wife', 'husband', 'girlfriend', 'boyfriend', 'son', 'daughter', 'mother', 'father', 'divorce', 'politics', 'political', 'election', 'government', 'president', 'religion', 'religious', 'church', 'god', 'allah', 'war',
          'kill', 'killed', 'death', 'dead', 'die', 'died', 'violence', 'violent', 'attack', 'sex', 'sexy', 'nude', 'fuck', 'shit', 'cunt', 'idiot', 'stupid', 'fat', 'ugly']
UNITS = {'zero': 0, 'nil': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 'twelve': 12, 'thirteen': 13, 'fourteen': 14,
         'fifteen': 15, 'sixteen': 16, 'seventeen': 17, 'eighteen': 18, 'nineteen': 19, 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 'seventy': 70, 'eighty': 80, 'ninety': 90, 'hundred': 100,
         'once': 1, 'twice': 2, 'first': 1, 'second': 2, 'third': 3, 'fourth': 4, 'fifth': 5, 'sixth': 6, 'seventh': 7, 'eighth': 8, 'ninth': 9, 'tenth': 10, 'half': 0}
HEX = re.compile(r'^#[0-9a-fA-F]{6}$')


def norm(s):
    s = s.lower().replace("'", ' ').replace('’', ' ')
    s = re.sub(r'[^a-z0-9 ]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def words(s):
    return [w for w in re.split(r'\s+', s.strip()) if w]


def num_set(text):
    out = set(int(x) for x in re.findall(r'\d+', text))
    t = text.lower().replace('’', "'")
    toks = re.findall(r'[a-z]+(?:-[a-z]+)*', t)
    for tok in toks:
        parts = tok.split('-')
        vals = [UNITS[p] for p in parts if p in UNITS]
        for p in parts:
            if p in UNITS:
                out.add(UNITS[p])
        if len(parts) == 2 and parts[0] in UNITS and parts[1] in UNITS and UNITS[parts[0]] >= 20 and UNITS[parts[1]] < 10:
            out.add(UNITS[parts[0]] + UNITS[parts[1]])
        # ninety-first -> 91
        if len(parts) == 2 and parts[0] in UNITS and parts[1] in UNITS and UNITS[parts[0]] >= 20 and parts[1] in ('first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth'):
            out.add(UNITS[parts[0]] + UNITS[parts[1]])
    return out


class Ctx:
    pass


def load_ctx(path, d):
    c = Ctx()
    c.no = d.get('no') if isinstance(d.get('no'), int) else None
    nno = '%03d' % (c.no or 0)
    plan_all = json.load(open(os.path.join(H, 'codex/v2/plan.json')))
    c.plan = plan_all.get(nno)
    c.md = ''
    mdp = os.path.join(H, 'codex/v2/plan/%s.md' % nno)
    if os.path.exists(mdp):
        c.md = open(mdp, encoding='utf8').read()
    c.allowed = []
    m = re.search(r'Allowed on-screen text[^\n]*?\):\s*(.+)', c.md)
    if m:
        c.allowed = [a.strip() for a in m.group(1).split(' | ') if a.strip()]
    c.narration = ' '.join(re.findall(r'^\d+\. \[\s*[\d.]+s\]\s*(.*?)\s*\(card:', c.md, re.M))
    c.subject = (c.plan or {}).get('subject', '')
    c.n_allowed = [norm(a) for a in c.allowed]
    c.n_narr = norm(c.narration)
    c.n_all = ' ' + ' | '.join(c.n_allowed) + ' | ' + c.n_narr + ' '
    c.nums = num_set(' '.join(c.allowed) + ' ' + c.narration)
    return c


def in_source(text, c):
    n = norm(text)
    return bool(n) and (n in c.n_narr or n in c.n_allowed or any(n in a for a in c.n_allowed) or (' ' + n + ' ') in c.n_all)


def check_text_basic(errs, where, text, c, maxw, must_q=False, source=None):
    """source: 'strict' = must be copied from narration/allowed, 'free' = author-written (banned words + numbers only)."""
    if not isinstance(text, str) or not text.strip():
        errs.append('%s: must be a non-empty string' % where); return
    w = words(text)
    if len(w) > maxw:
        errs.append('%s: %d words (max %d): "%s"' % (where, len(w), maxw, text))
    if must_q and not text.strip().endswith('?'):
        errs.append('%s: must end with "?": "%s"' % (where, text))
    for bw in norm(text).split():
        if bw in BANNED:
            errs.append('%s: banned word "%s" (betting/injury/crime/family/politics/religion/violence/sex are not allowed)' % (where, bw))
    for n in re.findall(r'\d+', text):
        if int(n) not in c.nums:
            errs.append('%s: number %s does not appear in the narration / allowed text' % (where, n))
    if source == 'strict' and not in_source(text, c):
        errs.append('%s: "%s" is not copied from the narration or the allowed on-screen text' % (where, text))


def check_keys(errs, where, obj, required, optional):
    if not isinstance(obj, dict):
        errs.append('%s: must be an object' % where); return False
    for k in required:
        if k not in obj:
            errs.append('%s: missing field "%s"' % (where, k))
    for k in obj:
        if k not in required and k not in optional and k != 'type':
            errs.append('%s: unknown field "%s" (allowed: %s)' % (where, k, ', '.join(list(required) + list(optional))))
    return True


def check_enum(errs, where, val, name):
    if val not in S[name]:
        errs.append('%s: "%s" is not a valid %s (see DSL.md)' % (where, val, name))


COMMON_OPT = ['accent', 'bg']


def check_common(errs, where, e):
    if 'accent' in e and not (isinstance(e['accent'], str) and HEX.match(e['accent'])):
        errs.append('%s.accent: must be #rrggbb' % where)
    if 'bg' in e:
        check_enum(errs, where + '.bg', e['bg'], 'BGS')


# ------------------------------------------------------------------ per-type validators
def v_hook(errs, w, e, c):
    check_keys(errs, w, e, ['q', 'prop', 'emote', 'board'], ['role', 'prop_text'] + COMMON_OPT)
    check_common(errs, w, e)
    check_text_basic(errs, w + '.q', e.get('q'), c, 8, must_q=True)
    check_enum(errs, w + '.prop', e.get('prop'), 'PROPS')
    check_enum(errs, w + '.emote', e.get('emote'), 'EMOTES')
    check_enum(errs, w + '.board', e.get('board'), 'BOARDS')
    if 'role' in e: check_enum(errs, w + '.role', e['role'], 'ROLES')
    if 'prop_text' in e:
        if not re.match(r'^\d{1,2}[:\-]\d{1,2}$', str(e['prop_text'])): errs.append(w + '.prop_text: use "7:0" form')
        else:
            for n in re.findall(r'\d+', e['prop_text']):
                if int(n) not in c.nums: errs.append('%s.prop_text: number %s not in narration' % (w, n))
    q = e.get('q', '')
    if isinstance(q, str) and q.strip() and c.n_narr:
        sig = [x for x in norm(q).split() if len(x) >= 4]
        if sig and not any(x in c.n_all for x in sig):
            errs.append('%s.q: shares no content word with the narration (hook must be about this video)' % w)


def v_news(errs, w, e, c):
    check_keys(errs, w, e, ['name', 'fact', 'ticker', 'icons', 'role'], ['dateline', 'actor'] + COMMON_OPT + ['number'])
    check_common(errs, w, e)
    check_text_basic(errs, w + '.name', e.get('name'), c, 4)
    if isinstance(e.get('name'), str) and not (in_source(e['name'], c) or norm(e['name']) == norm(c.subject)):
        errs.append('%s.name: "%s" must be the subject, an allowed text or a phrase from the narration' % (w, e['name']))
    check_text_basic(errs, w + '.fact', e.get('fact'), c, 10, source='strict')
    t = e.get('ticker')
    if isinstance(t, str):
        if norm(t) not in c.n_allowed:
            errs.append('%s.ticker: "%s" must equal one of the allowed on-screen texts %s' % (w, t, c.allowed))
    else: errs.append(w + '.ticker: must be a string')
    ic = e.get('icons')
    if not (isinstance(ic, list) and len(ic) == 3): errs.append(w + '.icons: exactly 3 icon names')
    else:
        for i, x in enumerate(ic): check_enum(errs, '%s.icons[%d]' % (w, i), x, 'ICONS')
    check_enum(errs, w + '.role', e.get('role'), 'ROLES')
    if 'dateline' in e: check_text_basic(errs, w + '.dateline', e['dateline'], c, 4, source='strict')


def v_interview(errs, w, e, c):
    check_keys(errs, w, e, ['label', 'bubble', 'answer', 'subject'], ['reporter_role', 'subject_role', 'subject_cast'] + COMMON_OPT)
    check_common(errs, w, e)
    if e.get('label') != 'REPORTER ASKS': errs.append(w + '.label: must be exactly "REPORTER ASKS"')
    b = e.get('bubble')
    check_text_basic(errs, w + '.bubble', b, c, 9)
    if isinstance(b, str) and b.strip():
        if not (in_source(b, c) or b.strip().endswith('?')):
            errs.append('%s.bubble: must be a phrase from the narration of the window, or a reporter QUESTION ending in "?"' % w)
    a = e.get('answer')
    if check_keys(errs, w + '.answer', a, ['icon', 'gesture'], ['emote']):
        check_enum(errs, w + '.answer.icon', a.get('icon'), 'ICONS')
        check_enum(errs, w + '.answer.gesture', a.get('gesture'), 'GESTURES')
        if 'emote' in a: check_enum(errs, w + '.answer.emote', a['emote'], 'EMOTES')
    s = e.get('subject')
    check_text_basic(errs, w + '.subject', s, c, 4)
    if isinstance(s, str) and not (in_source(s, c) or norm(s) == norm(c.subject)):
        errs.append('%s.subject: "%s" must be the subject name / allowed text' % (w, s))
    for k in ('reporter_role', 'subject_role'):
        if k in e: check_enum(errs, '%s.%s' % (w, k), e[k], 'ROLES')


def v_provoc(errs, w, e, c):
    check_keys(errs, w, e, ['q', 'a', 'b', 'split', 'mood'], COMMON_OPT)
    check_common(errs, w, e)
    check_text_basic(errs, w + '.q', e.get('q'), c, 7, must_q=True)
    check_text_basic(errs, w + '.a', e.get('a'), c, 3)
    check_text_basic(errs, w + '.b', e.get('b'), c, 3)
    if isinstance(e.get('a'), str) and isinstance(e.get('b'), str) and norm(e['a']) == norm(e['b']): errs.append(w + ': options a and b are identical')
    sp = e.get('split')
    if not (isinstance(sp, list) and len(sp) == 2 and all(isinstance(x, int) and not isinstance(x, bool) for x in sp)): errs.append(w + '.split: [n, m] two integers')
    elif sum(sp) != 100: errs.append('%s.split: %s sums to %d, must be 100' % (w, sp, sum(sp)))
    elif min(sp) < 5: errs.append(w + '.split: each side must be >= 5')
    check_enum(errs, w + '.mood', e.get('mood'), 'MOODS')


def v_stats(errs, w, e, c):
    check_keys(errs, w, e, ['items'], COMMON_OPT)
    check_common(errs, w, e)
    it = e.get('items')
    if not (isinstance(it, list) and 2 <= len(it) <= 3): errs.append(w + '.items: 2 or 3 items'); return
    for i, x in enumerate(it):
        ww = '%s.items[%d]' % (w, i)
        if not check_keys(errs, ww, x, ['icon', 'value', 'label'], ['suffix']): continue
        check_enum(errs, ww + '.icon', x.get('icon'), 'ICONS')
        v = x.get('value')
        if not isinstance(v, str) or not re.match(r'^[0-9][0-9.,:/\-]{0,7}$', v): errs.append('%s.value: string of digits like "7", "2-1", "73" (max 8 chars)' % ww)
        else:
            for n in re.findall(r'\d+', v):
                if int(n) not in c.nums: errs.append('%s.value: number %s is not in the narration / allowed text' % (ww, n))
        check_text_basic(errs, ww + '.label', x.get('label'), c, 3, source='strict')
        if 'suffix' in x: check_enum(errs, ww + '.suffix', x['suffix'], 'SUFFIXES')


# ------------------------------------------------------------------ COMIC rules (agent B)  -- see DSL.md chapter COMIC
ROLE_SCALE = {'rookie': 0.9, 'keeper': 1.02, 'coach': 1.02, 'legend': 1.02, 'mascot': 1.08, 'kid': 0.78, 'boss': 1.04}
SYMBOL_BUBBLE = re.compile(r'^(\?|!|\?!|!\?|\.\.\.|\?\?|!!)$')
PANEL = (30, 234, 1050, 1532)   # x0, y0, x1, y1 of the comic panel (safe zone)
COMIC_ACTOR_OPT = ['pose', 'emote', 'flip', 'scale', 'hold', 'talk', 'look', 'lift', 'rot', 'label']
COMIC_PROP_OPT = ['scale', 'anim', 'rot', 'flip', 'text', 'face', 'layer', 'label']
FRAME_H = 1920.0
# --- geometry rules (keep in sync with templates/Comic.tsx: reachOf / FALL_BOX) ---
WIDE_POSES = {'cheer', 'celebrate', 'shock', 'jump', 'dance', 'wave', 'shrug', 'present', 'point', 'facepalm', 'thumbsup'}
FALL_BOX = (-200.0, 370.0, -335.0, -80.0)      # x0, x1, y0, y1 of a 'fall' pose around the feet point, units of scale x role scale (mirrored by flip)
EDGE = (70, 1010)                                # figures must stay inside this x range (panel 30..1050 minus 40 px), arms included
SFX_BOX = (54, 1026, 254, 1480)                  # a whole sfx burst (centre +- 1.12 r) must fit in this box


def fall_rect(a, S):
    x0, x1, y0, y1 = FALL_BOX
    if a.get('flip'): x0, x1 = -x1, -x0
    return (a['x'] + x0 * S, a['x'] + x1 * S, a['y'] + y0 * S, a['y'] + y1 * S)


def _rects_hit(p, q, gap=8):
    return p[0] < q[1] + gap and q[0] < p[1] + gap and p[2] < q[3] + gap and q[2] < p[3] + gap


def _num(errs, w, v, lo, hi, what):
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        errs.append('%s: %s must be a number' % (w, what)); return False
    if not (lo <= v <= hi):
        errs.append('%s: %s=%s outside %s..%s' % (w, what, v, lo, hi)); return False
    return True


def _check_comic_beat(errs, bw, b, c, ctx, i, prev):
    phase = b.get('phase')
    opt_ab = ['actors', 'props'] if phase == 'BEAT' else []
    req = ['phase', 't0', 't1'] + ([] if phase == 'BEAT' else ['actors', 'props'])
    check_keys(errs, bw, b, req, opt_ab + ['bg', 'sfx', 'bubble', 'cam', 'fx'])
    check_enum(errs, bw + '.phase', phase, 'PHASES')
    if 'bg' in b: check_enum(errs, bw + '.bg', b['bg'], 'BGS')
    if 'cam' in b: check_enum(errs, bw + '.cam', b['cam'], 'CAMS')
    actors = b.get('actors') if isinstance(b.get('actors'), list) else (prev['actors'] if prev else [])
    props = b.get('props') if isinstance(b.get('props'), list) else (prev['props'] if prev else [])
    if 'actors' in b and not isinstance(b['actors'], list): errs.append(bw + '.actors: must be a list'); actors = []
    if 'props' in b and not isinstance(b['props'], list): errs.append(bw + '.props: must be a list'); props = []
    if len(actors) > 4: errs.append('%s.actors: max 4 actors per beat (phone-size readability)' % bw)
    if len(props) > 7: errs.append('%s.props: max 7 props per beat' % bw)
    if phase != 'BEAT' and not actors: errs.append('%s.actors: at least one actor per beat' % bw)
    seen = set()
    hero = 0.0
    for j, a in enumerate(b.get('actors') or []):
        aw = '%s.actors[%d]' % (bw, j)
        if not check_keys(errs, aw, a, ['id', 'x', 'y'], COMIC_ACTOR_OPT): continue
        if a.get('id') not in ctx['cast']: errs.append('%s.id: "%s" is not in cast' % (aw, a.get('id')))
        if a.get('id') in seen: errs.append('%s.id: actor "%s" listed twice in this beat' % (aw, a.get('id')))
        seen.add(a.get('id'))
        _num(errs, aw, a.get('x'), 60, 1020, 'x (feet centre, canvas px)')
        _num(errs, aw, a.get('y'), 900, 1535, 'y (feet, canvas px)')
        if 'pose' in a: check_enum(errs, aw + '.pose', a['pose'], 'POSES')
        if 'emote' in a: check_enum(errs, aw + '.emote', a['emote'], 'EMOTES')
        if 'label' in a:
            check_text_basic(errs, aw + '.label', a['label'], c, 3, source='strict')
            # the name plate floats ABOVE the head (engine rule), so it must not collide with a speech bubble of the same actor
            bb0 = b.get('bubble') if isinstance(b.get('bubble'), dict) else None
            if bb0 and bb0.get('who') == a.get('id'): errs.append('%s.label: the name plate sits above the head, where the bubble of the same actor opens: move the label to another beat or drop the bubble' % aw)
        if 'flip' in a and not isinstance(a['flip'], bool): errs.append(aw + '.flip: true/false')
        if 'talk' in a and not isinstance(a['talk'], bool): errs.append(aw + '.talk: true/false')
        sc = a.get('scale', 1.3)
        if _num(errs, aw, sc, 0.6, 2.2, 'scale'):
            role = (ctx['cast'].get(a.get('id')) or {}).get('role', 'player')
            hero = max(hero, 505.0 * sc * ROLE_SCALE.get(role, 1.0))
        if 'lift' in a: _num(errs, aw, a['lift'], 0, 600, 'lift')
        if 'rot' in a: _num(errs, aw, a['rot'], -180, 180, 'rot')
        if 'look' in a:
            lk = a['look']
            if not (lk == 'cam' or lk in ctx['cast'] or lk in S['PROPS']): errs.append('%s.look: "cam", a cast id or a prop kind' % aw)
        if 'hold' in a:
            hd = a['hold']
            for h1 in (hd if isinstance(hd, list) else [hd]):
                if check_keys(errs, aw + '.hold', h1, ['kind'], ['hand', 'scale', 'rot', 'dx', 'dy', 'anim']):
                    check_enum(errs, aw + '.hold.kind', h1.get('kind'), 'PROPS')
                    if 'hand' in h1: check_enum(errs, aw + '.hold.hand', h1['hand'], 'HANDS')
                    if 'anim' in h1: check_enum(errs, aw + '.hold.anim', h1['anim'], 'ANIMS')
    # ---- geometry: figures inside the panel, FALL collision rule
    figs = []
    for a in (b.get('actors') or []):
        if not (isinstance(a, dict) and all(isinstance(a.get(k), (int, float)) and not isinstance(a.get(k), bool) for k in ('x', 'y'))): continue
        scl = a.get('scale', 1.3)
        if isinstance(scl, bool) or not isinstance(scl, (int, float)): continue
        Sc = scl * ROLE_SCALE.get((ctx['cast'].get(a.get('id')) or {}).get('role', 'player'), 1.0)
        if a.get('pose') == 'fall':
            figs.append(('fall', a, fall_rect(a, Sc)))
        else:
            rc = (165 if a.get('pose') in WIDE_POSES else 105) * Sc
            figs.append(('stand', a, (a['x'] - rc, a['x'] + rc, a['y'] - 505 * Sc, a['y'])))
    for kind, a, r in figs:
        if kind == 'fall' and (r[0] < EDGE[0] or r[1] > EDGE[1]):
            errs.append('%s.actors[%s]: the fallen body spans x %d..%d (a "fall" pose is x -200..+370 of the figure; mirrored by flip): keep it inside %d..%d (move it, set flip, or lower the scale)' % (bw, a.get('id'), r[0], r[1], EDGE[0], EDGE[1]))
        elif kind == 'stand' and (r[0] < EDGE[0] - 30 or r[1] > EDGE[1] + 30):
            ctx['warn'].append('%s.actors[%s]: arms/body reach x %d..%d: close to the panel edge (camera push may crop it)' % (bw, a.get('id'), r[0], r[1]))
    for i1 in range(len(figs)):
        for i2 in range(i1 + 1, len(figs)):
            k1, a1, r1 = figs[i1]; k2, a2, r2 = figs[i2]
            if 'fall' in (k1, k2) and _rects_hit(r1, r2):
                errs.append('%s.actors: "%s" and "%s" overlap (a fallen body lies tilted across x %d..%d / %d..%d, y %d..%d / %d..%d): space fallers so their boxes do not touch (>= 300 px apart is not enough at scale 1: put them in different depth rows y, alternate flip, or lower the scale)' % (bw, a1.get('id'), a2.get('id'), r1[0], r1[1], r2[0], r2[1], r1[2], r1[3], r2[2], r2[3]))
    if b.get('actors') and hero < 560:
        errs.append('%s: no hero figure big enough (the biggest actor must be >= 30%% of frame height: scale >= 1.15 for a normal role, >= 1.25 for a rookie); got %.0f px' % (bw, hero))
    counts = {}
    kinds = []
    for j, p in enumerate(b.get('props') or []):
        pw = '%s.props[%d]' % (bw, j)
        if not check_keys(errs, pw, p, ['kind', 'x', 'y'], COMIC_PROP_OPT): continue
        check_enum(errs, pw + '.kind', p.get('kind'), 'PROPS')
        k = p.get('kind'); kinds.append(k)
        counts[k] = counts.get(k, 0) + 1
        _num(errs, pw, p.get('x'), 30, 1050, 'x')
        _num(errs, pw, p.get('y'), 235, 1530, 'y')
        if 'scale' in p: _num(errs, pw, p['scale'], 0.3, 4.2, 'scale')
        if 'rot' in p: _num(errs, pw, p['rot'], -360, 360, 'rot')
        if 'anim' in p: check_enum(errs, pw + '.anim', p['anim'], 'ANIMS')
        if 'face' in p: check_enum(errs, pw + '.face', p['face'], 'EMOTES')
        if 'layer' in p and p['layer'] not in S['LAYERS']: errs.append('%s.layer: back|front' % pw)
        if 'label' in p: check_text_basic(errs, pw + '.label', p['label'], c, 3, source='strict')
        if 'text' in p:
            tx = p['text']
            if not (isinstance(tx, str) and re.match(r'^\d{1,3}([:\-]\d{1,3})?$', tx)): errs.append('%s.text: digits only, like "7:0" or "90"' % pw)
            else:
                for n in re.findall(r'\d+', tx):
                    if int(n) not in c.nums: errs.append('%s.text: number %s is not in the narration / allowed text' % (pw, n))
    if 'sfx' in b:
        sx = b['sfx']
        if check_keys(errs, bw + '.sfx', sx, ['text', 'x', 'y'], ['r']):
            if sx.get('text') not in S['SFX_WORDS']: errs.append('%s.sfx.text: must be one of %s' % (bw, sorted(S['SFX_WORDS'])))
            _num(errs, bw + '.sfx', sx.get('x'), 120, 960, 'x'); _num(errs, bw + '.sfx', sx.get('y'), 330, 1440, 'y')
            if 'r' in sx: _num(errs, bw + '.sfx', sx['r'], 90, 260, 'r')
            rr = sx.get('r', 190)
            if all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in (sx.get('x'), sx.get('y'), rr)):
                e = 1.12 * rr
                x0, x1, y0, y1 = SFX_BOX
                if sx['x'] - e < x0 or sx['x'] + e > x1 or sx['y'] - e < y0 or sx['y'] + e > y1:
                    errs.append('%s.sfx: the whole burst (centre %s,%s radius %s x1.12 = %d px) must fit inside x %d..%d, y %d..%d (it was clipped by the panel edge); move it in or use a smaller r' % (bw, sx['x'], sx['y'], rr, e, x0, x1, y0, y1))
                for kind, a, r in figs:
                    cx, cy = min(max(sx['x'], r[0]), r[1]), min(max(sx['y'], r[2]), r[3])
                    if (sx['x'] - cx) ** 2 + (sx['y'] - cy) ** 2 < (0.8 * rr) ** 2 and kind == 'fall':
                        errs.append('%s.sfx: the burst covers the falling figure "%s" (that is the gag): put it in the empty space above it' % (bw, a.get('id')))
    if 'fx' in b:
        if not isinstance(b['fx'], list): errs.append(bw + '.fx: list of {kind,x,y,size?}')
        else:
            for j, f in enumerate(b['fx']):
                fw = '%s.fx[%d]' % (bw, j)
                if check_keys(errs, fw, f, ['kind', 'x', 'y'], ['size']):
                    check_enum(errs, fw + '.kind', f.get('kind'), 'FX_KINDS')
                    _num(errs, fw, f.get('x'), 30, 1050, 'x'); _num(errs, fw, f.get('y'), 235, 1530, 'y')
                    if 'size' in f: _num(errs, fw, f['size'], 0.4, 2.5, 'size')
    if 'bubble' in b:
        bb = b['bubble']
        if check_keys(errs, bw + '.bubble', bb, ['who'], ['text', 'icon', 'thought']):
            who = bb.get('who')
            names = [a.get('id') for a in actors if isinstance(a, dict)] + [p.get('kind') for p in props if isinstance(p, dict)]
            if who not in names: errs.append('%s.bubble.who: "%s" must be an actor id or prop kind present in this beat' % (bw, who))
            if ('text' in bb) == ('icon' in bb): errs.append(bw + '.bubble: give exactly one of text / icon')
            if 'icon' in bb: check_enum(errs, bw + '.bubble.icon', bb['icon'], 'ICONS')
            if 'text' in bb:
                tx = bb['text']
                if not isinstance(tx, str) or not tx.strip(): errs.append(bw + '.bubble.text: non-empty string')
                elif not SYMBOL_BUBBLE.match(tx.strip()):
                    check_text_basic(errs, bw + '.bubble.text', tx, c, 4, source='strict')
                    if len(tx) > 28: errs.append('%s.bubble.text: max 28 characters' % bw)
            if 'thought' in bb and not isinstance(bb['thought'], bool): errs.append(bw + '.bubble.thought: true/false')
    return actors, props, kinds


def validate_comic(errs, w, e, c, ctx):
    """ctx = {'cast': {...}, 'prop': str|None, 'comics': [(id, entry)], 'kinds': {...}, 'warn': [...]}"""
    if e.get('todo'):
        ctx['warn'].append('%s: COMIC is a TODO placeholder (authoring pending)' % w); return
    # --- BEGIN COMIC RULES ---
    check_keys(errs, w, e, ['bg', 'beats'], ['callback', 'accent'])
    check_common(errs, w, e)
    beats = e.get('beats')
    if not (isinstance(beats, list) and 4 <= len(beats) <= 5):
        errs.append(w + '.beats: 4 or 5 beats: SETUP, GAG (1-2 steps), BEAT, TWIST'); return
    phases = [b.get('phase') if isinstance(b, dict) else None for b in beats]
    ok_order = phases[0] == 'SETUP' and phases[-1] == 'TWIST' and phases[-2] == 'BEAT' and all(p == 'GAG' for p in phases[1:-2]) and 1 <= len(phases) - 3 <= 2
    if not ok_order:
        errs.append('%s.beats: phase order must be SETUP, GAG, [GAG], BEAT, TWIST (got %s)' % (w, ', '.join(str(p) for p in phases)))
    last = 0.0
    all_kinds = set(); twist_kinds = set()
    prev = None
    for i, b in enumerate(beats):
        bw = '%s.beats[%d]' % (w, i)
        if not isinstance(b, dict): errs.append(bw + ': must be an object'); continue
        t0, t1 = b.get('t0'), b.get('t1')
        if not all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in (t0, t1)):
            errs.append(bw + ': t0/t1 must be numbers 0..1'); continue
        if abs(t0 - last) > 0.01: errs.append('%s: t0 %.2f must continue from previous t1 %.2f' % (bw, t0, last))
        if t1 <= t0: errs.append(bw + ': t1 must be > t0')
        last = t1
        ln, ph = t1 - t0, b.get('phase')
        if ph == 'SETUP' and not (0.18 <= t1 <= 0.34): errs.append('%s: SETUP must end between 0.18 and 0.34 (got %.2f): the first 0.25 s is the transition, show the situation by then' % (bw, t1))
        if ph == 'GAG' and ln < 0.08: errs.append('%s: GAG step too short (%.2f < 0.08 of the clip): it cannot be read' % (bw, ln))
        if ph == 'BEAT' and not (0.06 <= ln <= 0.16): errs.append('%s: silent BEAT must last 0.06-0.16 of the clip (got %.2f)' % (bw, ln))
        if ph == 'TWIST' and ln < 0.30: errs.append('%s: TWIST must hold >= 0.30 of the clip (got %.2f): the punchline needs time before the out-transition' % (bw, ln))
        if ph == 'BEAT':
            for k in ('sfx', 'fx', 'cam'):
                if k in b: errs.append('%s.%s: the silent BEAT has no %s (only breathing / blink / prop drift)' % (bw, k, k))
            if isinstance(prev, dict) and isinstance(b.get('actors'), list):
                pa = {a.get('id'): a for a in prev['actors'] if isinstance(a, dict)}
                ca = {a.get('id'): a for a in b['actors'] if isinstance(a, dict)}
                if set(pa) != set(ca): errs.append('%s.actors: the silent BEAT cannot add or remove actors' % bw)
                for k, a in ca.items():
                    q = pa.get(k)
                    if q and any(a.get(f) != q.get(f) for f in ('x', 'y', 'pose', 'emote')): errs.append('%s.actors[%s]: the silent BEAT freezes the action: same x, y, pose and emote as the previous beat' % (bw, k))
            if isinstance(prev, dict) and isinstance(b.get('props'), list):
                pp = sorted((p.get('kind'), p.get('x'), p.get('y')) for p in prev['props'] if isinstance(p, dict))
                cp = sorted((p.get('kind'), p.get('x'), p.get('y')) for p in b['props'] if isinstance(p, dict))
                if pp != cp: errs.append('%s.props: the silent BEAT cannot add, remove or move props (omit "props" to inherit them)' % bw)
        actors, props, kinds = _check_comic_beat(errs, bw, b, c, ctx, i, prev)
        prev = {'actors': actors, 'props': props}
        all_kinds |= set(kinds)
        if ph == 'TWIST': twist_kinds = set(kinds)
    if abs(last - 1.0) > 0.01: errs.append('%s: beats must end at t1 = 1 (got %.2f)' % (w, last))
    if ctx['prop']:
        if ctx['prop'] not in all_kinds: errs.append('%s: recurring prop "%s" must appear in this comic' % (w, ctx['prop']))
        elif ctx['prop'] not in twist_kinds: errs.append('%s: recurring prop "%s" must still be on screen in the TWIST beat' % (w, ctx['prop']))
    ctx['kinds'][w] = all_kinds
    ctx['used'] |= set(a.get('id') for b in beats if isinstance(b, dict) for a in (b.get('actors') or []) if isinstance(a, dict))
    # --- END COMIC RULES ---


def validate_comic_final(errs, ctx):
    """cross-comic rules: the last comic calls back to the first comic's prop; every cast member is used."""
    real = [(i, e) for i, e in ctx['comics'] if not e.get('todo')]
    if len(real) >= 2:
        first_id, last_id = real[0][0], real[-1][0]
        k_first = ctx['kinds'].get('sequences.' + first_id, set()) - {ctx['prop']}
        k_last = ctx['kinds'].get('sequences.' + last_id, set()) - {ctx['prop']}
        if not (k_first & k_last):
            errs.append('sequences.%s: the last comic must call back to the first comic: reuse at least one prop kind (other than the recurring prop) of sequences.%s, e.g. %s' % (last_id, first_id, sorted(k_first)[:4]))
    if real:
        for cid in ctx['cast']:
            if cid not in ctx['used']: ctx['warn'].append('cast.%s: never used in any comic (remove it or use it)' % cid)


VALID = {'HOOK': v_hook, 'NEWS': v_news, 'INTERVIEW': v_interview, 'PROVOC': v_provoc, 'STATS': v_stats}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    strict = '--strict' in sys.argv
    comics_only = '--comics-only' in sys.argv
    if not args:
        print('usage: validate.py CONTENT.json [--strict] [--comics-only]'); return 2
    path = args[0]
    errs, warns = [], []

    def dup_hook(pairs):
        seen = {}
        for k, v in pairs:
            if k in seen: errs.append('duplicate JSON key "%s"' % k)
            seen[k] = v
        return seen
    try:
        d = json.load(open(path, encoding='utf8'), object_pairs_hook=dup_hook)
    except Exception as ex:
        print('ERROR: cannot parse %s: %s' % (path, ex)); return 1
    if not isinstance(d, dict):
        print('ERROR: top level must be an object'); return 1
    for k in d:
        if k not in ('no', 'style', 'prop', 'cast', 'sequences', 'accent'): errs.append('top-level: unknown field "%s"' % k)
    for k in ('no', 'style', 'prop', 'cast', 'sequences'):
        if k not in d: errs.append('top-level: missing "%s"' % k)
    if not isinstance(d.get('no'), int): errs.append('no: integer video number'); print_out(errs, warns); return 1
    c = load_ctx(path, d)
    if not c.plan: errs.append('no: video %s is not in plan.json' % d.get('no')); print_out(errs, warns); return 1
    m = re.search(r'(\d{3})\.json$', path)
    if m and int(m.group(1)) != d['no']: errs.append('no: %s does not match file name %s' % (d['no'], os.path.basename(path)))
    if d.get('style') != c.plan['style']: errs.append('style: "%s" != plan style "%s"' % (d.get('style'), c.plan['style']))
    check_enum(errs, 'style', d.get('style'), 'STYLES')
    if 'accent' in d and not (isinstance(d['accent'], str) and HEX.match(d['accent'])): errs.append('accent: #rrggbb')
    prop = d.get('prop')
    if prop is not None: check_enum(errs, 'prop', prop, 'PROPS')
    cast = d.get('cast') if isinstance(d.get('cast'), dict) else {}
    if not isinstance(d.get('cast'), dict): errs.append('cast: object')
    for cid, cv in cast.items():
        if not check_keys(errs, 'cast.' + cid, cv, ['role'], ['skin', 'hair', 'shirt', 'number']): continue
        check_enum(errs, 'cast.%s.role' % cid, cv.get('role'), 'ROLES')
        for k in ('skin', 'hair', 'shirt'):
            if k in cv and not (isinstance(cv[k], str) and HEX.match(cv[k])): errs.append('cast.%s.%s: #rrggbb' % (cid, k))
        if 'number' in cv and not re.match(r'^\d{1,2}$', str(cv['number'])): errs.append('cast.%s.number: 1-2 digits' % cid)
    seqs = d.get('sequences') if isinstance(d.get('sequences'), dict) else {}
    plan_ids = [s['id'] for s in c.plan['sequences']]
    for sid in plan_ids:
        if sid not in seqs and not comics_only: errs.append('sequences: missing "%s" (plan ids: %s)' % (sid, ', '.join(plan_ids)))
    for sid in seqs:
        if sid not in plan_ids: errs.append('sequences: "%s" is not a sequence of this video' % sid)
    ctx = {'cast': cast, 'prop': prop, 'comics': [], 'kinds': {}, 'warn': warns, 'used': set()}
    n_comic = 0
    for ps in c.plan['sequences']:
        sid = ps['id']
        e = seqs.get(sid)
        if e is None: continue
        w = 'sequences.' + sid
        if not isinstance(e, dict): errs.append(w + ': must be an object'); continue
        ptype = ps['type']
        if e.get('type') != ptype: errs.append('%s.type: "%s" but plan says %s' % (w, e.get('type'), ptype))
        if ptype == 'COMIC':
            n_comic += 1
            ctx['comics'].append((sid, e))
            validate_comic(errs, w, e, c, ctx)
        elif ptype in VALID and not comics_only:
            VALID[ptype](errs, w, e, c)
    if n_comic and not prop: errs.append('prop: a recurring comic prop is required (this video has COMIC sequences)')
    validate_comic_final(errs, ctx)
    print_out(errs, warns)
    if errs: return 1
    if strict and warns: return 1
    return 0


def print_out(errs, warns):
    for wv in warns: print('WARN ' + wv)
    if errs:
        print('%d error(s):' % len(errs))
        for e in errs: print(' - ' + e)
    else:
        print('OK')


if __name__ == '__main__':
    sys.exit(main())
