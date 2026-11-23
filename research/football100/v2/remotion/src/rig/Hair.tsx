// Hair / headwear in head-local coordinates (origin = head centre, R = 100). `back` is drawn behind the head, `front` over it (clipped to head where needed).
import React from 'react';
import {shade} from '../core/color';

export const HAIR_STYLES = ['crop', 'side', 'spiky', 'curly', 'afro', 'bun', 'pony', 'bald', 'baldside', 'grey', 'slick', 'beanie', 'cap', 'headband'] as const;

interface HP { style: string; color: string; accent: string; ink: string; sw: number; clip: string }

export const HairBack: React.FC<HP> = ({ style, color, ink, sw }) => {
  const st = { stroke: ink, strokeWidth: sw, strokeLinejoin: 'round' as const };
  switch (style) {
    case 'afro': return <circle cx="0" cy="-30" r="132" fill={color} {...st} />;
    case 'curly': return <g fill={color} {...st}>{[...Array(9)].map((_, i) => { const a = Math.PI + (i / 8) * Math.PI; return <circle key={i} cx={Math.cos(a) * 94} cy={Math.sin(a) * 90 - 6} r="34" />; })}</g>;
    case 'bun': return <circle cx="0" cy="-118" r="34" fill={color} {...st} />;
    case 'pony': return <g><ellipse cx="-104" cy="14" rx="26" ry="52" fill={color} {...st} transform="rotate(14 -104 14)" /></g>;
    default: return null;
  }
};

export const HairFront: React.FC<HP> = ({ style, color, accent, ink, sw, clip }) => {
  const st = { stroke: ink, strokeWidth: sw, strokeLinejoin: 'round' as const };
  const hl = shade(color, -0.25);
  switch (style) {
    case 'crop': case 'grey': case 'bun': case 'pony': case 'headband':
      return <g>
        <g clipPath={`url(#${clip})`}><path d="M -110 -12 Q -108 -88 0 -108 Q 108 -88 110 -12 Q 78 -58 46 -50 Q 14 -66 -20 -52 Q -66 -58 -110 -12 Z" fill={color} {...st} /></g>
        {style === 'headband' && <g clipPath={`url(#${clip})`}><rect x="-110" y="-62" width="220" height="20" fill={accent} stroke={ink} strokeWidth={sw * 0.8} /></g>}
      </g>;
    case 'side': case 'slick':
      return <g clipPath={`url(#${clip})`}>
        <path d="M -110 -4 Q -112 -92 0 -108 Q 112 -84 110 -30 Q 70 -44 30 -56 Q -30 -34 -70 -14 Q -90 -10 -110 -4 Z" fill={color} {...st} />
        <path d="M -60 -78 Q -10 -88 40 -66" fill="none" stroke={hl} strokeWidth={sw * 0.9} strokeLinecap="round" />
      </g>;
    case 'spiky':
      return <g><path d="M -102 -14 L -118 -86 L -72 -62 L -66 -138 L -28 -80 L 0 -150 L 28 -80 L 66 -138 L 72 -62 L 118 -86 L 102 -14 Q 62 -54 0 -50 Q -62 -54 -102 -14 Z" fill={color} {...st} /></g>;
    case 'curly':
      return <g fill={color} {...st}>{[...Array(5)].map((_, i) => <circle key={i} cx={-60 + i * 30} cy={-62 + Math.abs(i - 2) * 6} r="24" />)}</g>;
    case 'afro':
      return <g clipPath={`url(#${clip})`}><path d="M -110 -20 Q -80 -80 0 -76 Q 80 -80 110 -20 Q 60 -54 0 -50 Q -60 -54 -110 -20 Z" fill={color} {...st} /></g>;
    case 'baldside':
      return <g fill={color} {...st}><path d="M -100 -30 Q -112 -4 -98 22 Q -92 0 -92 -22 Z" /><path d="M 100 -30 Q 112 -4 98 22 Q 92 0 92 -22 Z" /></g>;
    case 'beanie':
      return <g>
        <path d="M -106 -34 Q -112 -128 0 -132 Q 112 -128 106 -34 Q 0 -52 -106 -34 Z" fill={accent} {...st} />
        <rect x="-110" y="-52" width="220" height="30" rx="14" fill={shade(accent, 0.12)} {...st} />
        <circle cx="0" cy="-138" r="18" fill={shade(accent, -0.25)} {...st} />
      </g>;
    case 'cap':
      return <g>
        <path d="M -104 -30 Q -108 -122 0 -124 Q 108 -122 104 -30 Q 0 -48 -104 -30 Z" fill={accent} {...st} />
        <path d="M 40 -38 Q 130 -44 150 -20 Q 100 -16 40 -26 Z" fill={shade(accent, 0.2)} {...st} />
        <circle cx="0" cy="-126" r="9" fill={shade(accent, 0.2)} {...st} />
      </g>;
    default: return null;
  }
};
