import facts from "@/lib/nav-fun-facts.json";

export type NavFunFact = {
  text: string;
  slug: string;
  title: string;
  href: `/${string}`;
  sourceHref: string;
  sourceLabel: string;
};

type RawFact = {
  text: string;
  anchor: string;
  slug: string;
  title: string;
  sourceHref: string;
  sourceLabel: string;
};

const POOL = facts as RawFact[];
let lastIndex = -1;

/**
 * One Snapple-cap fact for the nav overlay.
 * A new open picks at random, and skips the fact just shown.
 */
export function getNavFunFact(rng: () => number = Math.random): NavFunFact | null {
  if (POOL.length === 0) return null;
  let idx = Math.floor(rng() * POOL.length);
  if (idx < 0 || idx >= POOL.length) idx = 0;
  if (POOL.length > 1 && idx === lastIndex) idx = (idx + 1) % POOL.length;
  lastIndex = idx;
  const fact = POOL[idx];
  return {
    text: fact.text,
    slug: fact.slug,
    title: fact.title,
    href: `/${fact.slug}`,
    sourceHref: fact.sourceHref,
    sourceLabel: fact.sourceLabel,
  };
}
