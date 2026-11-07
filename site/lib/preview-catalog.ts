import { existsSync, statSync } from "node:fs";
import downloadsJson from "@/src/generated/downloads.json";
import sourcesJson from "@/src/generated/sources.json";
import gutenberg from "../../public/data/reference/gutenberg/catalog.json";
import wikiart from "../../public/data/reference/wikiart/catalog.json";
import wikipedia from "../../public/data/reference/wikipedia/catalog.json";
import { DOMAIN_META, type DomainSlug } from "@/data/sections";
import { getBlogPosts, primarySection } from "@/lib/content";
import { DATASET_PACKS } from "@/data/datasets";

type DownloadPack = {
  slug: string;
  dataset?: string | null;
  pdf?: string | null;
  epub?: string | null;
  audio?: string | null;
  transcript?: string | null;
  html?: string | null;
  quarto?: string | null;
  github?: string | null;
};

const downloads = downloadsJson as Record<string, DownloadPack>;

export type FiledReport = {
  slug: string;
  title: string;
  href: string;
  desk: string;
  deskSlug: string;
  dataset: string | null;
  bytes: number | null;
  transcript: string | null;
  extras: { label: string; href: string }[];
  github: string | null;
  haystack: string;
};

export function formatBytes(bytes: number): string {
  if (bytes >= 1_000_000) return `${(bytes / 1_000_000).toFixed(1)} MB`;
  if (bytes >= 1_000) return `${Math.round(bytes / 1_000)} KB`;
  return `${bytes} B`;
}

export function filedReports(): FiledReport[] {
  const posts = new Map(getBlogPosts().map((post) => [post.slug, post]));
  return Object.values(downloads)
    .map((pack) => {
      const post = posts.get(pack.slug);
      const deskSlug = post ? primarySection(post.tags) || "" : "";
      const desk = deskSlug && deskSlug in DOMAIN_META ? DOMAIN_META[deskSlug as DomainSlug].title : "Report";
      const title = post?.title || pack.slug;
      let bytes: number | null = null;
      if (pack.dataset) {
        const path = new URL(`../../public${pack.dataset}`, import.meta.url);
        if (existsSync(path)) bytes = statSync(path).size;
      }
      const extras = [
        pack.pdf ? { label: "PDF", href: pack.pdf } : null,
        pack.epub ? { label: "EPUB", href: pack.epub } : null,
        pack.audio ? { label: "Audio", href: pack.audio } : null,
        pack.html ? { label: "HTML", href: pack.html } : null,
        pack.quarto ? { label: "Quarto", href: pack.quarto } : null,
      ].filter((item): item is { label: string; href: string } => Boolean(item));
      return {
        slug: pack.slug,
        title,
        href: `/${pack.slug}`,
        desk,
        deskSlug,
        dataset: pack.dataset || null,
        bytes,
        transcript: pack.transcript || null,
        extras,
        github: pack.github || null,
        haystack: `${title} ${desk} ${pack.slug}`.toLowerCase(),
      };
    })
    .sort((a, b) => a.title.localeCompare(b.title));
}

export function fileTotals(rows = filedReports()) {
  return {
    reports: rows.length,
    csv: rows.filter((row) => row.dataset).length,
    transcript: rows.filter((row) => row.transcript).length,
    pdf: rows.filter((row) => row.extras.some((item) => item.label === "PDF")).length,
    epub: rows.filter((row) => row.extras.some((item) => item.label === "EPUB")).length,
    audio: rows.filter((row) => row.extras.some((item) => item.label === "Audio")).length,
    missingCsv: rows.filter((row) => !row.dataset).length,
  };
}

type Citation = { text?: string; href?: string | null };
type SourceIssue = {
  slug: string;
  title: string;
  href: string;
  kicker?: string;
  updatedThrough?: string;
  datasets?: { title: string; href: string }[];
  citations?: Citation[];
};
type SourceTopic = { id: string; title: string; href: string; issues: SourceIssue[] };

const topics = (sourcesJson as { topics: SourceTopic[] }).topics;

export function citationCoverage() {
  const desks = topics.map((topic) => {
    let citations = 0;
    let linked = 0;
    for (const issue of topic.issues) {
      for (const citation of issue.citations || []) {
        citations += 1;
        if (citation.href) linked += 1;
      }
    }
    return {
      id: topic.id,
      title: topic.title,
      href: topic.href,
      issues: topic.issues.length,
      citations,
      linked,
      unlinked: citations - linked,
      withDataset: topic.issues.filter((issue) => issue.datasets?.length).length,
    };
  });
  const unlinked = topics.flatMap((topic) =>
    topic.issues.flatMap((issue) =>
      (issue.citations || [])
        .filter((citation) => !citation.href)
        .map((citation) => ({
          desk: topic.title,
          deskId: topic.id,
          title: issue.title,
          href: issue.href,
          text: citation.text || "Untitled citation",
          haystack: `${topic.title} ${issue.title} ${citation.text || ""}`.toLowerCase(),
        })),
    ),
  );
  return {
    desks,
    unlinked,
    issues: desks.reduce((sum, desk) => sum + desk.issues, 0),
    citations: desks.reduce((sum, desk) => sum + desk.citations, 0),
    linked: desks.reduce((sum, desk) => sum + desk.linked, 0),
    unlinkedCount: unlinked.length,
    withDataset: desks.reduce((sum, desk) => sum + desk.withDataset, 0),
  };
}

export type CatalogName = "Gutenberg" | "WikiArt" | "Wikipedia";

export type CatalogRow = {
  catalog: CatalogName;
  title: string;
  detail: string;
  href: string | null;
  image: string | null;
  imageAlt: string;
  license: string;
  haystack: string;
};

function text(value: unknown): string {
  return typeof value === "string" ? value : "";
}

export function referenceRows(): { generatedAt: string; source: string; license: string; catalog: CatalogName; rows: CatalogRow[] }[] {
  const groups = [
    ["WikiArt", wikiart],
    ["Wikipedia", wikipedia],
    ["Gutenberg", gutenberg],
  ] as const;
  return groups.map(([catalog, file]) => {
    const license = text(file.license);
    const rows: CatalogRow[] = file.items.map((item) => {
      if (catalog === "WikiArt") {
        const title = text(item.title);
        const artist = text(item.artist);
        const year = text(item.year);
        const style = text(item.style);
        return {
          catalog,
          title,
          detail: [artist, year, style, text(item.license)].filter(Boolean).join(" · "),
          href: null,
          image: text(item.imageUrl) || null,
          imageAlt: artist ? `${title} by ${artist}` : title,
          license,
          haystack: `${catalog} ${title} ${artist} ${style}`.toLowerCase(),
        };
      }
      if (catalog === "Wikipedia") {
        const title = text(item.label);
        return {
          catalog,
          title,
          detail: text(item.description),
          href: text(item.url) || null,
          image: text(item.thumbnail) || null,
          imageAlt: title,
          license,
          haystack: `${catalog} ${title} ${text(item.description)}`.toLowerCase(),
        };
      }
      const title = text(item.title);
      const authors = Array.isArray(item.authors) ? item.authors.map(String).slice(0, 2).join(", ") : "";
      const subjects = Array.isArray(item.subjects) ? item.subjects.map(String).slice(0, 2).join(", ") : "";
      return {
        catalog,
        title,
        detail: [authors, subjects].filter(Boolean).join(" · "),
        href: text(item.url) || null,
        image: null,
        imageAlt: "",
        license,
        haystack: `${catalog} ${title} ${authors} ${subjects}`.toLowerCase(),
      };
    });
    return {
      catalog,
      generatedAt: text(file.generatedAt),
      source: text(file.source),
      license,
      rows,
    };
  });
}

export const datasetPacks = DATASET_PACKS;
