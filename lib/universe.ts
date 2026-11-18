/**
 * The Artometrics "Universe": sibling sites that share the brand.
 * Only artometrics.com subdomains are listed here. Other projects stay
 * off the public nav until Kyle opens them (Go-Live plan, stream E).
 */
export type UniverseLink = { href: string; label: string; descriptor: string };

export const UNIVERSE_LINKS: UniverseLink[] = [
  { href: "https://gotha.artometrics.com", label: "Gotha", descriptor: "Almanac of artifacts" },
  { href: "https://academy.artometrics.com", label: "Academy", descriptor: "Beginner guides" },
  { href: "https://glossary.artometrics.com", label: "Glossary", descriptor: "Terms · styles · people" },
];
