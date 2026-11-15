import { existsSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";

const ROOT = process.cwd();
export const REPO_URL = "https://github.com/Artometrics/artometrics";
export const SITE_URL = "https://artometrics.com";

/** Export files that were named for the long title, not the slug. */
const EXPORT_ALIASES: Record<string, string> = {
  beyonce: "beyonce-the-psychonomics-of-control",
  billboard: "billboard-hot-100",
  caesar: "caesar-the-psychonomics-of-emperor-julius",
  horror: "horror-movie-profit",
};

function publicFile(path: string | null | undefined): string | null {
  if (!path) return null;
  return existsSync(join(ROOT, "public", path.replace(/^\//, ""))) ? path : null;
}

function firstFile(candidates: (string | null | undefined)[]): string | null {
  for (const candidate of candidates) {
    const hit = publicFile(candidate);
    if (hit) return hit;
  }
  return null;
}

export function ebookFor(slug: string, packEpub?: string | null): string | null {
  const alias = EXPORT_ALIASES[slug];
  return firstFile([
    packEpub,
    `/data/articles/${slug}/article.epub`,
    `/exports/${slug}.epub`,
    alias ? `/exports/${alias}.epub` : null,
  ]);
}

export function pdfFor(slug: string, packPdf?: string | null): string | null {
  const alias = EXPORT_ALIASES[slug];
  return firstFile([
    packPdf,
    `/data/articles/${slug}/article.pdf`,
    `/exports/${slug}.pdf`,
    alias ? `/exports/${alias}.pdf` : null,
  ]);
}

/** The article's folder in the public repository, only when that folder exists and holds files. */
export function githubFolderFor(slug: string): string | null {
  const dir = join(ROOT, "articles", slug);
  return existsSync(dir) && statSync(dir).isDirectory() && readdirSync(dir).length ? `${REPO_URL}/tree/main/articles/${slug}` : null;
}

export type ArticleLinks = {
  download: { href: string; label: string } | null;
  book: string | null;
  data: string | null;
  github: string | null;
};

/**
 * Targets for the round buttons under the cover. A target that does not exist is null,
 * and the button is not rendered.
 */
export function articleLinks(
  slug: string,
  pack?: { pdf?: string | null; epub?: string | null; dataset?: string | null; github?: string | null } | null,
  sourcesSlug: string | null = slug,
): ArticleLinks {
  const pdf = pdfFor(slug, pack?.pdf);
  const dataset = publicFile(pack?.dataset);
  return {
    download: pdf ? { href: pdf, label: "Download the PDF" } : dataset ? { href: dataset, label: "Download the dataset (CSV)" } : null,
    book: ebookFor(slug, pack?.epub),
    data: sourcesSlug ? `/sources/${sourcesSlug}` : null,
    github: githubFolderFor(slug) || (sourcesSlug ? githubFolderFor(sourcesSlug) : null),
  };
}

export type ShareTargets = { linkedin: string; facebook: string; x: string; reddit: string; email: string };

export function shareTargets(url: string, title: string): ShareTargets {
  const u = encodeURIComponent(url);
  const t = encodeURIComponent(title);
  return {
    linkedin: `https://www.linkedin.com/sharing/share-offsite/?url=${u}`,
    facebook: `https://www.facebook.com/sharer/sharer.php?u=${u}`,
    x: `https://twitter.com/intent/tweet?url=${u}&text=${t}`,
    reddit: `https://www.reddit.com/submit?url=${u}&title=${t}`,
    email: `mailto:?subject=${t}&body=${encodeURIComponent(`${title}\n${url}`)}`,
  };
}

const DATA_EXT = /\.(csv|tsv|json|xlsx?|zip|parquet|txt)$/i;

export type DataFile = { href: string; name: string; bytes: number; kind: string };

/** Public data files for one article, excluding chart sidecars. Paths are site-relative. */
export function articleDataFiles(slug: string): DataFile[] {
  const base = join(ROOT, "public/data/articles", slug);
  if (!existsSync(base)) return [];
  const out: DataFile[] = [];
  const walk = (dir: string, rel: string) => {
    for (const name of readdirSync(dir).sort()) {
      const full = join(dir, name);
      const st = statSync(full);
      const nextRel = `${rel}/${name}`;
      if (st.isDirectory()) {
        if (name === "charts" || name === "node_modules") continue;
        walk(full, nextRel);
      } else if (DATA_EXT.test(name) && !/\.plotly\.json$/i.test(name)) {
        out.push({
          href: `/data/articles/${slug}${nextRel}`,
          name: nextRel.replace(/^\//, ""),
          bytes: st.size,
          kind: name.split(".").pop()!.toUpperCase(),
        });
      }
    }
  };
  walk(base, "");
  return out;
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`;
}
