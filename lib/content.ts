import blogData from "@/src/generated/blog.json";
import podcastData from "@/src/generated/podcast.json";
import authorsData from "@/src/generated/authors.json";
import legalData from "@/src/generated/legal.json";
import {
  DOMAIN_META,
  SECTION_META,
  SECTION_SLUGS,
  SUBDOMAIN_META,
  primaryDomain,
  primarySubdomain,
  type SectionSlug,
} from "@/data/sections";

export type BlogPost = (typeof blogData)[number];
export type PodcastEpisode = (typeof podcastData)[number];
export type Author = (typeof authorsData)[number];
export type LegalPage = (typeof legalData)[number];

export function deckLine(description: string, maxWords = 18): string {
  const trimmed = description.trim();
  const match = trimmed.match(/^(.+?[.!?])(?:\s|$)/);
  const line = match ? match[1] : trimmed.split(/\s+/).slice(0, maxWords).join(" ");
  return /[.!?]$/.test(line) ? line : `${line.replace(/[.!?]+$/, "")}.`;
}

/** Split "SLUG: subtitle" report titles for hero styling (red slug + blue deck). */
export function splitReportHeadline(title: string): { slug: string; subtitle: string } | null {
  const idx = title.indexOf(":");
  if (idx === -1) return null;
  const slug = title.slice(0, idx).trim();
  const subtitle = title.slice(idx + 1).trim();
  if (!slug || !subtitle) return null;
  return { slug, subtitle };
}

const CARD_DECK_MIN_WORDS = 5;

/** Short hook for grid/stack cards (~5–8 words). Full `description` stays in SEO. */
export function cardDeckLine(description: string, maxWords = 8): string {
  const trimmed = description.trim();
  if (!trimmed) return "";
  const words = trimmed.split(/\s+/).filter(Boolean);
  const finish = (line: string) =>
    /[.!?]$/.test(line) ? line : `${line.replace(/[.!?]+$/, "")}.`;

  if (words.length <= maxWords) {
    return finish(words.join(" "));
  }

  const firstSentence = trimmed.match(/^(.+?[.!?])(?:\s|$)/)?.[1]?.trim();
  if (firstSentence) {
    const sentWords = firstSentence.split(/\s+/).filter(Boolean);
    if (sentWords.length >= CARD_DECK_MIN_WORDS && sentWords.length <= maxWords) {
      return finish(firstSentence);
    }
    if (sentWords.length > maxWords) {
      return finish(sentWords.slice(0, maxWords).join(" "));
    }
  }

  const target = Math.min(maxWords, Math.max(CARD_DECK_MIN_WORDS, 7));
  return finish(words.slice(0, target).join(" "));
}

export function formatAuthorName(slug: string) {
  const special: Record<string, string> = {
    "kyle-mcauliffe": "Kyle McAuliffe",
  };
  if (special[slug]) return special[slug];
  return slug
    .replace(/-/g, " ")
    .split(" ")
    .map((word) => {
      if (/^mc[a-z]/i.test(word)) {
        return `Mc${word.slice(2, 3).toUpperCase()}${word.slice(3)}`;
      }
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(" ");
}

export function formatDate(iso: string | null) {
  if (!iso) return "";
  return new Date(iso).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "UTC",
  });
}

/** Primary domain from tags (`arts` | `sports` | …). */
export function primarySection(tags: string[] | undefined): SectionSlug | null {
  if (!tags?.length) return null;
  return primaryDomain(tags);
}

/** Title-case a stored subject token for eyebrows (CSS may uppercase). */
export function formatSubjectLabel(subject: string): string {
  return subject
    .trim()
    .split(/\s+/)
    .map((word) =>
      word
        .split("-")
        .map((part) => (part ? part.charAt(0).toUpperCase() + part.slice(1).toLowerCase() : part))
        .join("-"),
    )
    .join(" ");
}

/** Desk eyebrow: "Arts · Film · Anime" when subdomain and subject are known. */
export function sectionLabel(
  tags: string[] | undefined,
  subject?: string | null,
): string | null {
  if (!tags?.length) return null;
  const domain = primaryDomain(tags);
  const sub = primarySubdomain(tags);
  const subjectPart =
    subject && subject.trim() ? formatSubjectLabel(subject) : null;
  const desk =
    sub && SUBDOMAIN_META[sub]
      ? `${DOMAIN_META[domain].title} · ${SUBDOMAIN_META[sub].title}`
      : DOMAIN_META[domain].title;
  if (!subjectPart) return desk;
  return `${desk} · ${subjectPart}`;
}

/** @deprecated Use primarySection */
export function primaryDesk(tags: string[] | undefined): SectionSlug | null {
  return primarySection(tags);
}

export function getBlogPosts(): BlogPost[] {
  return (blogData as BlogPost[])
    .filter((post) => !post.draft && post.pubDate)
    .filter((post) => !SECTION_SLUGS.includes(post.slug as SectionSlug))
    .sort((a, b) => new Date(b.pubDate!).getTime() - new Date(a.pubDate!).getTime());
}

export function getBlogPost(slug: string | undefined): BlogPost | undefined {
  if (!slug) return undefined;
  return getBlogPosts().find((p) => p.slug === slug);
}

export function getPodcastEpisodes(): PodcastEpisode[] {
  return (podcastData as PodcastEpisode[])
    .filter((ep) => ep.pubDate)
    .sort((a, b) => new Date(b.pubDate!).getTime() - new Date(a.pubDate!).getTime());
}

export function getPodcastEpisode(id: string | undefined): PodcastEpisode | undefined {
  if (!id) return undefined;
  return (podcastData as PodcastEpisode[]).find((ep) => ep.id === id);
}

export function getAuthors(): Author[] {
  return authorsData as Author[];
}

export function getAuthor(id: string | undefined): Author | undefined {
  if (!id) return undefined;
  return (authorsData as Author[]).find((a) => a.id === id);
}

export function getLegalPages(): LegalPage[] {
  return legalData as LegalPage[];
}

export function getLegalPage(id: string | undefined): LegalPage | undefined {
  if (!id) return undefined;
  return (legalData as LegalPage[]).find((p) => p.id === id);
}

export function getAdjacentPosts(currentSlug: string) {
  const sorted = getBlogPosts();
  const index = sorted.findIndex((p) => p.slug === currentSlug);
  if (index === -1) return { previous: null, next: null };
  const previous = index > 0 ? sorted[index - 1] : null;
  const next = index < sorted.length - 1 ? sorted[index + 1] : null;
  return {
    previous: previous
      ? { title: previous.title, href: `/${previous.slug}` }
      : null,
    next: next ? { title: next.title, href: `/${next.slug}` } : null,
  };
}

function relatedPostScore(current: BlogPost, candidate: BlogPost): number {
  let score = 0;
  const curDomain = primaryDomain(current.tags);
  const curSub = primarySubdomain(current.tags);
  const candDomain = primaryDomain(candidate.tags);
  const candSub = primarySubdomain(candidate.tags);
  if (curSub && candSub && curSub === candSub) score += 12;
  else if (curDomain === candDomain) score += 6;
  const curSubject = current.subject?.trim().toLowerCase();
  const candSubject = candidate.subject?.trim().toLowerCase();
  if (curSubject && candSubject && curSubject === candSubject) score += 10;
  const curTags = new Set((current.tags ?? []).map((t) => t.toLowerCase()));
  for (const tag of candidate.tags ?? []) {
    if (curTags.has(tag.toLowerCase())) score += 1;
  }
  return score;
}

/** Related reads: subdomain + subject first, then domain, then archive fill. */
export function getRelatedPosts(currentSlug: string, limit = 4): BlogPost[] {
  const current = getBlogPost(currentSlug);
  if (!current) return [];
  const candidates = getBlogPosts().filter((p) => p.slug !== currentSlug);
  const scored = candidates
    .map((p) => ({ post: p, score: relatedPostScore(current, p) }))
    .sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return new Date(b.post.pubDate!).getTime() - new Date(a.post.pubDate!).getTime();
    });
  const withSignal = scored.filter((s) => s.score > 0).map((s) => s.post);
  const picked = withSignal.slice(0, limit);
  if (picked.length >= limit) return picked;
  const pickedSlugs = new Set(picked.map((p) => p.slug));
  for (const { post } of scored) {
    if (picked.length >= limit) break;
    if (!pickedSlugs.has(post.slug)) {
      picked.push(post);
      pickedSlugs.add(post.slug);
    }
  }
  return picked;
}

/** Section-first recommended reads, filled from the wider archive. */
export function getRecommendedPosts(currentSlug: string, limit = 12): BlogPost[] {
  const related = getRelatedPosts(currentSlug, limit);
  if (related.length >= limit) return related;
  const all = getBlogPosts().filter((p) => p.slug !== currentSlug);
  const seen = new Set(related.map((p) => p.slug));
  const rest = all.filter((p) => !seen.has(p.slug));
  return [...related, ...rest].slice(0, limit);
}

export {
  DOMAIN_META,
  SECTION_META,
  SECTION_SLUGS,
  SUBDOMAIN_META,
  primaryDomain,
  primarySubdomain,
};
