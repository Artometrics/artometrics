import downloadsJson from "@/src/generated/downloads.json";
import {
  DOMAIN_META,
  DOMAIN_SLUGS,
  SUBDOMAIN_META,
  type DomainSlug,
  type SubdomainSlug,
} from "@/data/sections";
import {
  formatDate,
  getBlogPosts,
  primarySection,
  primarySubdomain,
  type BlogPost,
} from "@/lib/content";

type DownloadPack = {
  dataset?: string | null;
  pdf?: string | null;
  html?: string | null;
  transcript?: string | null;
  epub?: string | null;
  audio?: string | null;
};

const downloads = downloadsJson as Record<string, DownloadPack>;

export type PreviewReportRow = {
  slug: string;
  title: string;
  href: string;
  desk: string;
  deskSlug: string;
  deskHref: string;
  subdomain: string;
  subSlug: string;
  dateLabel: string;
  dateValue: string;
  dataset: string | null;
  haystack: string;
};

export type PreviewFile = { label: string; href: string };

export function previewFiles(slug: string): PreviewFile[] {
  const pack = downloads[slug];
  if (!pack) return [];
  const files: PreviewFile[] = [];
  if (pack.dataset) files.push({ label: "Dataset CSV", href: pack.dataset });
  if (pack.pdf) files.push({ label: "PDF", href: pack.pdf });
  if (pack.html) files.push({ label: "HTML", href: pack.html });
  if (pack.transcript) files.push({ label: "Transcript", href: pack.transcript });
  if (pack.audio) files.push({ label: "Audio", href: pack.audio });
  return files;
}

export function toPreviewRow(post: BlogPost): PreviewReportRow {
  const deskSlug = primarySection(post.tags) || "";
  const subSlug = primarySubdomain(post.tags) || "";
  const desk = deskSlug && deskSlug in DOMAIN_META ? DOMAIN_META[deskSlug as DomainSlug].title : "Report";
  const subdomain =
    subSlug && subSlug in SUBDOMAIN_META ? SUBDOMAIN_META[subSlug as SubdomainSlug].title : "";
  const dateValue = (post.pubDate || "").slice(0, 10);
  const title = post.title;
  return {
    slug: post.slug,
    title,
    href: `/design-preview/reports/${post.slug}`,
    desk,
    deskSlug,
    deskHref: deskSlug ? `/design-preview/topics/${deskSlug}` : "/design-preview",
    subdomain,
    subSlug,
    dateLabel: formatDate(post.pubDate),
    dateValue,
    dataset: downloads[post.slug]?.dataset || null,
    haystack: `${title} ${desk} ${subdomain} ${dateValue} ${post.slug}`.toLowerCase(),
  };
}

export function previewReportRows(posts = getBlogPosts()): PreviewReportRow[] {
  return posts.map(toPreviewRow);
}

export function deskFilters() {
  return DOMAIN_SLUGS.map((slug) => ({
    id: slug,
    label: DOMAIN_META[slug].title,
  }));
}
