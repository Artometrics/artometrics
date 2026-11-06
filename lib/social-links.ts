/**
 * Outbound accounts for the design preview.
 *
 * Included only when the repository already publishes a real URL.
 * `https://github.com/Artometrics` is the organization `sameAs` on the home page.
 *
 * Not included:
 * - `twitter:site` = `@artometrics` is a meta handle with no profile URL.
 * - `src/content/authors/juliet-ramos.md` lists `https://twitter.com/artometrics`
 *   beside `linkedin: "#_"` and `email: "#_"`, so that file is a template, not a
 *   verified account list.
 * - Share-intent URLs (`twitter.com/intent/tweet`) are actions, not profiles.
 * - No official Instagram, YouTube, or LinkedIn URL was found.
 */

export type SocialLink = { label: string; href: string };

export const CONFIGURED_SOCIAL: SocialLink[] = [
  { label: "GitHub", href: "https://github.com/Artometrics" },
];

export const UNCONFIGURED_SOCIAL = ["X", "Instagram", "YouTube", "LinkedIn"] as const;
