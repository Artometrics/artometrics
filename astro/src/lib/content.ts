import { existsSync, readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import {
  DOMAIN_META,
  DOMAIN_SLUGS,
  SUBDOMAIN_META,
  primaryDomain,
  primarySubdomain,
  type DomainSlug,
} from "../data/sections";
import { EDITIONS, type EditionManifest } from "../data/editions";
import { DATASET_PACKS, type DatasetPack } from "../data/datasets";

const repoRoot = fileURLToPath(new URL("../../../", import.meta.url));

function readJson<T>(rel: string): T {
  return JSON.parse(readFileSync(path.join(repoRoot, rel), "utf8")) as T;
}

export type Faq = { question: string; answer: string };

export type Post = {
  id: string;
  title: string;
  slug: string;
  pubDate: string;
  description: string;
  heroImage?: string;
  tags?: string[];
  subject?: string;
  section?: string;
  subdomain?: string;
  author?: string;
  draft?: boolean;
  tldr?: string;
  keyPoints?: string[];
  faq?: Faq[];
  audioSrc?: string | null;
  body: string;
};

export type Author = {
  id: string;
  name: string;
  role?: string;
  bio?: string;
  image?: { url: string; alt?: string };
  socials?: Record<string, string>;
};

export type Episode = {
  id: string;
  title: string;
  pubDate: string;
  description: string;
  author?: string;
  image?: { url: string; alt?: string } | string;
  guestAvatar?: { url: string; alt?: string };
  episodeNumber?: number;
  duration?: string;
  audioSrc?: string;
  tags?: string[];
  isLocked?: boolean;
  body?: string;
};

export type LegalPage = {
  id: string;
  page: string;
  pubDate: string;
  body: string;
};

export type DownloadPack = {
  slug: string;
  dataset?: string | null;
  quarto?: string | null;
  html?: string | null;
  pdf?: string | null;
  epub?: string | null;
  audio?: string | null;
  transcript?: string | null;
  github?: string | null;
};

export type FunFact = {
  text: string;
  anchor?: string;
  slug: string;
  title: string;
  sourceHref: string;
  sourceLabel: string;
};

export type CalendarRow = {
  releaseFriday: string;
  slug: string;
  title: string;
  desk: string;
  subdomain: string;
};

type SourceCitation = { text: string; href: string | null };
type SourceEntry = {
  slug: string;
  title: string;
  kicker: string;
  href: string;
  updatedThrough: string;
  updatedThroughKind: string;
  datasets: { id: string; title: string; href: string }[];
  citations: SourceCitation[];
  fixes?: SourceEntry[];
};
export type SourceTopic = {
  id: string;
  title: string;
  description: string;
  href: string;
  issues: SourceEntry[];
};

const DOMAIN_SET = new Set<string>(DOMAIN_SLUGS);

const posts = (readJson<Post[]>("src/generated/blog.json") || [])
  .filter((post) => !post.draft && post.pubDate && !DOMAIN_SET.has(post.slug))
  .sort((a, b) => new Date(b.pubDate).getTime() - new Date(a.pubDate).getTime());

const authors = readJson<Author[]>("src/generated/authors.json");
const episodes = (readJson<Episode[]>("src/generated/podcast.json") || []).sort(
  (a, b) => new Date(b.pubDate).getTime() - new Date(a.pubDate).getTime(),
);
const legal = readJson<LegalPage[]>("src/generated/legal.json");
const downloads = readJson<Record<string, DownloadPack>>("src/generated/downloads.json");
const facts = readJson<FunFact[]>("lib/nav-fun-facts.json");
const calendar = readJson<CalendarRow[]>("src/generated/content-calendar.json");
const sourcesCatalog = readJson<{ topics: SourceTopic[] }>("src/generated/sources.json");

export function getPosts(): Post[] {
  return posts;
}

export function getPost(slug: string): Post | undefined {
  return posts.find((post) => post.slug === slug);
}

export function getAuthors(): Author[] {
  return authors;
}

export function getAuthor(id: string): Author | undefined {
  return authors.find((author) => author.id === id);
}

export function getEpisodes(): Episode[] {
  return episodes;
}

export function getEpisode(id: string): Episode | undefined {
  return episodes.find((episode) => episode.id === id);
}

export function getLegalPages(): LegalPage[] {
  return legal;
}

export function getLegal(id: string): LegalPage | undefined {
  return legal.find((page) => page.id === id);
}

export function getDownloads(slug: string): DownloadPack | undefined {
  return downloads[slug];
}

export function getFacts(): FunFact[] {
  return facts;
}

export function getEditions(): EditionManifest[] {
  return EDITIONS;
}

export function getEdition(id: string): EditionManifest | undefined {
  return EDITIONS.find((edition) => edition.id === id);
}

export function getDatasets(): DatasetPack[] {
  return DATASET_PACKS;
}

export function getDataset(id: string): DatasetPack | undefined {
  return DATASET_PACKS.find((pack) => pack.id === id);
}

export function getSourceTopics(): SourceTopic[] {
  return sourcesCatalog.topics;
}

export function domainTitle(slug: string): string {
  if (slug in DOMAIN_META) return DOMAIN_META[slug as DomainSlug].title;
  return slug;
}

export function sectionLabel(post: Pick<Post, "tags" | "subject">): string {
  const tags = post.tags ?? [];
  const domain = primaryDomain(tags);
  const sub = primarySubdomain(tags);
  const desk =
    sub && SUBDOMAIN_META[sub]
      ? `${DOMAIN_META[domain].title} · ${SUBDOMAIN_META[sub].title}`
      : DOMAIN_META[domain].title;
  return post.subject?.trim() ? `${desk} · ${post.subject.trim()}` : desk;
}

export function domainOf(post: Pick<Post, "tags">): DomainSlug {
  return primaryDomain(post.tags ?? []);
}

export function postsInDomain(domain: string): Post[] {
  return posts.filter((post) => domainOf(post) === domain);
}

export function relatedPosts(post: Post, limit = 3): Post[] {
  const domain = domainOf(post);
  return posts.filter((item) => item.slug !== post.slug && domainOf(item) === domain).slice(0, limit);
}

export function formatDate(iso: string | undefined): string {
  if (!iso) return "";
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return iso;
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC",
  });
}

export function deckLine(description: string, maxWords = 28): string {
  const trimmed = (description || "").trim();
  const match = trimmed.match(/^(.+?[.!?])(?:\s|$)/);
  const line = match ? match[1] : trimmed.split(/\s+/).slice(0, maxWords).join(" ");
  return /[.!?]$/.test(line) ? line : `${line.replace(/[.!?]+$/, "")}.`;
}

export function splitHeadline(title: string): { kicker: string; rest: string } | null {
  const idx = title.indexOf(":");
  if (idx < 1) return null;
  const kicker = title.slice(0, idx).trim();
  const rest = title.slice(idx + 1).trim();
  if (!kicker || !rest) return null;
  return { kicker, rest };
}

export function authorName(slug: string | undefined): string {
  if (!slug) return "Kyle McAuliffe";
  const known = authors.find((author) => author.id === slug);
  if (known) return known.name;
  if (slug === "kyle-mcauliffe") return "Kyle McAuliffe";
  return slug
    .split("-")
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function readingMinutes(html: string): number {
  const text = html.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  const words = text ? text.split(" ").length : 0;
  return Math.max(1, Math.round(words / 220));
}

export function imageUrl(image: Episode["image"] | Author["image"] | string | undefined): string {
  if (!image) return "";
  if (typeof image === "string") return image;
  return image.url || "";
}

function parseIsoDate(iso: string): Date {
  const [y, m, d] = iso.split("-").map(Number);
  return new Date(Date.UTC(y, (m || 1) - 1, d || 1));
}

function weekStartMondayUtc(date: Date): Date {
  const d = new Date(date);
  const day = d.getUTCDay();
  const diff = day === 0 ? -6 : 1 - day;
  d.setUTCDate(d.getUTCDate() + diff);
  d.setUTCHours(0, 0, 0, 0);
  return d;
}

export function issueWeek(now = new Date()): { label: string; thisWeek: CalendarRow[]; coming: CalendarRow[] } {
  const start = weekStartMondayUtc(now);
  const end = new Date(start);
  end.setUTCDate(end.getUTCDate() + 7);
  const labelEnd = new Date(start);
  labelEnd.setUTCDate(labelEnd.getUTCDate() + 6);
  const fmt = (d: Date) =>
    d.toLocaleDateString("en-US", { month: "short", day: "numeric", timeZone: "UTC" });
  const thisWeek = calendar
    .filter((row) => {
      const release = parseIsoDate(row.releaseFriday);
      return release >= start && release < end;
    })
    .slice(0, 3);
  const coming = calendar
    .filter((row) => parseIsoDate(row.releaseFriday) >= end)
    .sort((a, b) => parseIsoDate(a.releaseFriday).getTime() - parseIsoDate(b.releaseFriday).getTime())
    .slice(0, 3);
  return { label: `${fmt(start)} – ${fmt(labelEnd)}`, thisWeek, coming };
}

export function publicAssetExists(href: string | null | undefined): boolean {
  if (!href) return false;
  if (/^https?:\/\//i.test(href)) return true;
  if (!href.startsWith("/")) return false;
  return existsSync(path.join(repoRoot, "public", href.slice(1).split("?")[0]));
}

export function absoluteUrl(pathname: string): string {
  if (!pathname) return "https://artometrics.com/";
  if (/^https?:\/\//i.test(pathname)) return pathname;
  return `https://artometrics.com${pathname.startsWith("/") ? pathname : `/${pathname}`}`;
}

export const SITE = {
  name: "Artometrics",
  url: "https://artometrics.com",
  description: "Investigative data stories on arts, sports, science, humanities, civics, and culture.",
  og: "/images/brand/og-default.png",
};

export { DOMAIN_META, DOMAIN_SLUGS, SUBDOMAIN_META };
