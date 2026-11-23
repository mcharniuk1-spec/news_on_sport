// Role -> outfit / hair / accessory definitions. Colours come from the theme (+ per-cast overrides).
export interface RoleDef {
  outfit: 'kit' | 'keeper' | 'blazer' | 'track' | 'ref' | 'suit' | 'casual' | 'mascot';
  shirt: number; hair: string[]; acc: string[]; scale: number; head: number; shirtStyle: ('plain' | 'stripes' | 'hoops' | 'sash')[];
  number?: boolean; greyHair?: boolean;
}
export const ROLE_DEFS: Record<string, RoleDef> = {
  striker: { outfit: 'kit', shirt: 0, hair: ['spiky', 'crop', 'curly', 'side'], acc: [], scale: 1, head: 1, shirtStyle: ['plain', 'hoops', 'stripes'], number: true },
  player: { outfit: 'kit', shirt: 3, hair: ['crop', 'side', 'pony', 'curly'], acc: [], scale: 1, head: 1, shirtStyle: ['plain', 'stripes', 'sash'], number: true },
  rookie: { outfit: 'kit', shirt: 4, hair: ['crop', 'spiky'], acc: ['headband'], scale: 0.9, head: 1.06, shirtStyle: ['plain'], number: true },
  keeper: { outfit: 'keeper', shirt: 5, hair: ['crop', 'curly', 'side'], acc: ['gloves'], scale: 1.02, head: 1, shirtStyle: ['plain'], number: true },
  reporter: { outfit: 'blazer', shirt: 1, hair: ['pony', 'bun', 'side'], acc: ['lanyard'], scale: 1, head: 1, shirtStyle: ['plain'] },
  coach: { outfit: 'track', shirt: 4, hair: ['grey', 'baldside', 'crop'], acc: ['whistle'], scale: 1.02, head: 1, shirtStyle: ['plain'], greyHair: true },
  referee: { outfit: 'ref', shirt: 0, hair: ['crop', 'side', 'baldside'], acc: ['whistle'], scale: 1, head: 1, shirtStyle: ['plain'] },
  fan: { outfit: 'kit', shirt: 2, hair: ['beanie', 'curly', 'cap', 'crop'], acc: ['scarf'], scale: 0.98, head: 1.02, shirtStyle: ['stripes', 'hoops', 'plain'], number: false },
  legend: { outfit: 'blazer', shirt: 6, hair: ['grey', 'baldside'], acc: ['medal', 'glasses'], scale: 1.02, head: 1, shirtStyle: ['plain'], greyHair: true },
  mascot: { outfit: 'mascot', shirt: 4, hair: ['bald'], acc: ['ears'], scale: 1.08, head: 1.22, shirtStyle: ['plain'] },
  kid: { outfit: 'casual', shirt: 2, hair: ['crop', 'pony', 'cap'], acc: [], scale: 0.78, head: 1.14, shirtStyle: ['plain', 'stripes'] },
  pundit: { outfit: 'suit', shirt: 3, hair: ['slick', 'side'], acc: ['tie', 'headset'], scale: 1, head: 1, shirtStyle: ['plain'] },
  boss: { outfit: 'suit', shirt: 0, hair: ['baldside', 'slick'], acc: ['tie', 'glasses', 'moustache'], scale: 1.04, head: 1.02, shirtStyle: ['plain'] },
  staff: { outfit: 'casual', shirt: 1, hair: ['bun', 'side', 'crop', 'pony'], acc: ['lanyard'], scale: 1, head: 1, shirtStyle: ['plain', 'stripes'] },
};
