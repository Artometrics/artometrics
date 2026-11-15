import { existsSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import catalog from "@/src/generated/sources.json";
import downloads from "@/src/generated/downloads.json";
import { articleDataFiles, ebookFor, githubFolderFor, pdfFor, type DataFile } from "./article-links";

const ROOT = process.cwd();

type Catalog = typeof catalog;
type Issue = Catalog["topics"][number]["issues"][number];

export interface SourceEntry {
  slug: string;
  title: string;
  kicker: string;
  href: string;
  topic: { id: string; title: string; href: string };
  updatedThrough: string;
  issue: Issue;
}

export const SOURCE_ENTRIES: SourceEntry[] = catalog.topics.flatMap((topic) =>
  topic.issues.map((issue) => ({
    slug: issue.slug,
    title: issue.title,
    kicker: issue.kicker,
    href: issue.href,
    topic: { id: topic.id, title: topic.title, href: topic.href },
    updatedThrough: issue.updatedThrough,
    issue,
  })),
);

const bySlug = new Map(SOURCE_ENTRIES.map((entry) => [entry.slug, entry]));
const fixParent = new Map<string, string>();
for (const entry of SOURCE_ENTRIES) for (const fix of entry.issue.fixes || []) fixParent.set(fix.slug, entry.slug);

/** The sources page that covers an article. A data-fix report shares its parent's page. */
export function sourcesSlugFor(slug: string): string | null {
  if (bySlug.has(slug)) return slug;
  return fixParent.get(slug) || null;
}

export function hasSourcesPage(slug: string): boolean {
  return sourcesSlugFor(slug) !== null;
}

export function entryFor(slug: string): SourceEntry | undefined {
  return bySlug.get(slug);
}

export type Resource = { label: string; href: string; note?: string; external?: boolean };

function exists(path?: string | null): string | null {
  if (!path) return null;
  return existsSync(join(ROOT, "public", path.replace(/^\//, ""))) ? path : null;
}

function chartSpecs(slug: string): DataFile[] {
  const dir = join(ROOT, "public/data/articles", slug, "charts");
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((name) => /\.json$/i.test(name))
    .sort()
    .map((name) => ({
      href: `/data/articles/${slug}/charts/${name}`,
      name: `charts/${name}`,
      bytes: statSync(join(dir, name)).size,
      kind: "JSON",
    }));
}

export interface SourcePage {
  entry: SourceEntry;
  files: DataFile[];
  fixFiles: { title: string; href: string; files: DataFile[] }[];
  charts: DataFile[];
  resources: Resource[];
  datasetPacks: { id: string; title: string; href: string }[];
  notes: string[];
}

export function sourcePageFor(slug: string): SourcePage {
  const entry = bySlug.get(slug)!;
  const pack = (downloads as Record<string, any>)[slug] || {};
  const files = articleDataFiles(slug);
  const packDataset = exists(pack.dataset);
  if (packDataset && !files.some((file) => file.href === packDataset)) {
    const size = statSync(join(ROOT, "public", packDataset.replace(/^\//, ""))).size;
    files.unshift({ href: packDataset, name: packDataset.split("/").pop()!, bytes: size, kind: packDataset.split(".").pop()!.toUpperCase() });
  }

  const rank = (file: DataFile) => (/(^|\/)(dataset|data)\.csv$/i.test(file.name) ? 0 : file.kind === "CSV" ? 1 : file.kind === "TSV" ? 2 : file.kind === "XLSX" || file.kind === "XLS" ? 3 : file.kind === "JSON" ? 4 : 5);
  files.sort((a, b) => rank(a) - rank(b) || a.name.localeCompare(b.name));

  const resources: Resource[] = [{ label: "Read the report", href: entry.href }];
  const pdf = pdfFor(slug, pack.pdf);
  const epub = ebookFor(slug, pack.epub);
  const transcript = pack.transcript ? `/transcripts/${slug}` : null;
  if (pdf) resources.push({ label: "PDF", href: pdf, note: "Print edition" });
  if (epub) resources.push({ label: "EPUB", href: epub, note: "E-book edition" });
  if (transcript) resources.push({ label: "Transcript", href: transcript, note: "Plain text of the report" });
  const audio = exists(pack.audio);
  if (audio) resources.push({ label: "Narration (MP3)", href: audio });
  const html = exists(pack.html);
  if (html) resources.push({ label: "Rendered Quarto HTML", href: html });
  const folder = githubFolderFor(slug);
  if (folder) resources.push({ label: "Source folder on GitHub", href: folder, note: "Quarto project, data, and chart code", external: true });
  if (pack.github && /^https:\/\/github\.com\//.test(pack.github) && pack.github !== folder) {
    resources.push({ label: "Standalone repository", href: pack.github, external: true });
  }

  const fixFiles = (entry.issue.fixes || []).map((fix) => ({
    title: fix.title,
    href: fix.href,
    files: articleDataFiles(fix.slug),
  }));

  const notes: string[] = [];
  notes.push(`${entry.updatedThrough}.`);
  if (!files.length) {
    notes.push("This report has no public data file yet. Its figures are cited below, and the numbers are described in the report text.");
  }
  for (const fix of entry.issue.fixes || []) {
    notes.push(`Correction record: “${fix.title}” documents what changed in this report's data.`);
  }

  return {
    entry,
    files,
    fixFiles,
    charts: chartSpecs(slug),
    resources,
    datasetPacks: entry.issue.datasets || [],
    notes,
  };
}

const csvCell = (value: unknown) => `"${String(value ?? "").replace(/"/g, '""')}"`;

export function catalogCsv(origin = "https://artometrics.com"): string {
  const rows = [["report", "desk", "slug", "updated_through", "citation_number", "citation", "citation_url", "report_url", "sources_page"]];
  for (const entry of SOURCE_ENTRIES) {
    entry.issue.citations.forEach((citation, index) => {
      rows.push([
        entry.title,
        entry.topic.title,
        entry.slug,
        entry.updatedThrough,
        `S${index + 1}`,
        citation.text || "",
        citation.href || "",
        `${origin}${entry.href}`,
        `${origin}/sources/${entry.slug}`,
      ]);
    });
  }
  return rows.map((row) => row.map(csvCell).join(",")).join("\n") + "\n";
}
