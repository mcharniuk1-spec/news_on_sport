// Template registry: type -> component. Agent B: replace the COMIC import with the real engine (./Comic) -- nothing else changes.
import {Hook} from './Hook';
import {News} from './News';
import {Interview} from './Interview';
import {Provoc} from './Provoc';
import {Stats} from './Stats';
import {Comic} from './Comic';

export const TEMPLATES: Record<string, React.FC<{ c: any }>> = { HOOK: Hook, NEWS: News, INTERVIEW: Interview, PROVOC: Provoc, STATS: Stats, COMIC: Comic };
