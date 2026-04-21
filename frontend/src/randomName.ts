const ADJECTIVES = [
  "curious",
  "mighty",
  "swift",
  "quiet",
  "bright",
  "gentle",
  "lucky",
  "clever",
] as const;

const ANIMALS = [
  "mouse",
  "moose",
  "fox",
  "heron",
  "badger",
  "otter",
  "lark",
  "bear",
] as const;

function randomInt(max: number): number {
  return Math.floor(Math.random() * max);
}

function randomSuffix(): string {
  const chars = "abcdefghijklmnopqrstuvwxyz0123456789";
  let s = "";
  for (let i = 0; i < 6; i += 1) {
    s += chars[randomInt(chars.length)]!;
  }
  return s;
}

export function randomDisplayName(): string {
  const adj = ADJECTIVES[randomInt(ADJECTIVES.length)]!;
  const animal = ANIMALS[randomInt(ANIMALS.length)]!;
  return `${adj}-${animal}-${randomSuffix()}`;
}
