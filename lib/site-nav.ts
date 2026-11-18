import { DOMAIN_META, DOMAIN_SLUGS } from "@/data/sections";

export type SiteNavItem = {
  href: string;
  label: string;
  /** Right-aligned hint in mobile nav overlay. */
  descriptor?: string;
  isActive: (pathname: string) => boolean;
};

function norm(path: string) {
  return path.replace(/\/$/, "") || "/";
}

/** Logo → home. No separate Home link. */
export const SITE_PRIMARY_NAV: SiteNavItem[] = [
  ...DOMAIN_SLUGS.map((slug) => ({
    href: `/topics/${slug}`,
    label: DOMAIN_META[slug].title.toUpperCase(),
    descriptor: DOMAIN_META[slug].navDescriptor,
    isActive: (pathname: string) => norm(pathname).startsWith(`/topics/${slug}`),
  })),
  {
    href: "/blog",
    label: "Index",
    descriptor: "All reports · desks",
    isActive: (pathname) => norm(pathname) === "/blog",
  },
];

export const SITE_OVERLAY_EXTRA: { href: string; label: string }[] = [];

/**
 * "Universe" — sibling Artometrics sites. External, so no isActive.
 * Only hosts that are live today on artometrics.com subdomains are listed;
 * Dawn, Pantheon and the books shelf join once Kyle decides whether they open.
 */
export const SITE_UNIVERSE_NAV: { href: string; label: string; descriptor: string }[] = [
  { href: "https://academy.artometrics.com", label: "Academy", descriptor: "Beginner guides" },
  { href: "https://glossary.artometrics.com", label: "Glossary", descriptor: "Terms · styles" },
  { href: "https://gotha.artometrics.com", label: "Gotha", descriptor: "Almanac of artifacts" },
];
