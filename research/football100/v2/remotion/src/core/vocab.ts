// SINGLE SOURCE OF TRUTH for the authoring vocabulary.
// `node gen_vocab.mjs` turns this into vocab.json (read by validate.py) and fills DSL.md lists.
// Keep this file free of imports / TS-only runtime constructs so node can load it directly.
export const STYLES = ['SITCOM-YELLOW','CUTOUT-PAPER','INK-COMIC','ACTION-ANIME','RUBBER-SLAPSTICK','STRIP-MINIMAL','SCIFI-DEADPAN','CLEAR-LINE','FLAT-POP'] as const;
export const ROLES = ['striker','keeper','reporter','coach','referee','fan','legend','mascot','kid','pundit','boss','player','rookie','staff'] as const;
export const POSES = ['idle','kick','run','celebrate','shrug','point','sit','cry','shock','think','hold','fall','dance','sleep','wave','shush','facepalm','jump','bow','cheer','tired','present','headscratch','thumbsup','lean','crouch'] as const;
export const EMOTES = ['neutral','happy','shock','angry-cheeky','smug','sweat','sleepy','cry','love','dizzy','sad','wink'] as const;
export const PROPS = ['ball','trophy','shirt','boot','whistle','stopwatch','scoreboard','flag','cone','bench','armchair','sofa','goal','bucket','cake','car','cassette','bag','phone','camera','microphone','clipboard','card-red','card-yellow','coin','medal','crown','megaphone','tv','cup','pizza','door','key','calendar','tag','mug','umbrella','balloon','suitcase','rocket','clock','magnifier','lightbulb','crate','ladder','bin','paper-plane','ticket',
  'star','heart','fire','bolt','thumbs-up','thumbs-down','check','cross','question','exclaim','globe','chart-up','chart-down','gloves','suit','hanger','envelope','notepad','laptop','headphones','pen','hourglass','gift','donut','glasses','bell','siren','cap','scarf','newspaper','padlock','ribbon','boots','net','table','podium-box','shelf','sticker','speech-dots','heart-broken','sweat-drop','tie','chair','desk','plant','lamp','screen','arrow','pitch-board'] as const;
export const ICONS = PROPS; // every prop can be used as an icon (NEWS/STATS/INTERVIEW)
export const BGS = ['stadium','pitch','tunnel','dressing-room','studio','street','office','living-room','press-room','night-city','podium','bench-area','training','plain-colour','boardroom','pub','sky','kitchen'] as const;
export const ANIMS = ['drop','slide-l','slide-r','bounce','shake','grow','shrink','spin','float','arc','pulse','pop','wobble','orbit'] as const;
export const BOARDS = ['sign','neon','stamp','typed','ticket','scoreboard'] as const;
export const GESTURES = ['shrug','point','thumbsup','wave','think','shush','present','facepalm','cheer','headscratch','hold','idle'] as const;
export const MOODS = ['cheeky','smug','shock','love','fun','angry','sleepy'] as const;
export const CAMS = ['push','shake','pan','zoom-out'] as const;
export const PHASES = ['SETUP','GAG','BEAT','TWIST'] as const;
export const TYPES = ['HOOK','NEWS','INTERVIEW','PROVOC','STATS','COMIC'] as const;
export const TRANSITIONS = ['wipe-diag','iris','blinds','checker','ball-roll','panels','star-iris','dots','stripes','curtain','zigzag','flash-slam','ink-splat','hex-shutter','wave'] as const;
export const SFX_WORDS = ['BANG','POP','THUD','WHOOSH','CREAK','DING','CLANG'] as const;
export const SUFFIXES = ['%','+','x','k','m','s',"'"] as const;
export const FX_KINDS = ['smoke','sparkle','confetti','dust','speed'] as const;
export const LAYERS = ['back','front'] as const;
export const HANDS = ['R','L','both'] as const;
