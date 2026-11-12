import { existsSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

export type ReportSource = {
  title: string;
  publisher?: string;
  year?: string | number;
  url: string;
  moreUrls?: { label: string; url: string }[];
  retrieved?: string | null;
  retrievedNote?: string;
  revision?: string | null;
  note?: string;
  listed?: boolean;
};

export type ChartMeta = {
  title: string;
  description: string;
  source: string;
  data?: { label: string; href: string }[];
};

export type ReportMeta = {
  updated?: string;
  whatChanged?: string;
  changelog?: { href: string; file: string };
  status?: {
    state: "current" | "earlier";
    label: string;
    note: string;
    links?: { label: string; href: string }[];
  };
  aliases?: Record<string, string>;
  sources?: Record<string, ReportSource>;
  method?: {
    pulled: string[];
    cleaned: string[];
    updated: string[];
    vintage: string[];
    caveats: string[];
    files?: { label: string; href: string }[];
  };
  charts?: Record<string, ChartMeta>;
};

const ROOT = process.cwd();

export function loadReportMeta(slug: string): ReportMeta | null {
  const file = join(ROOT, "src/content/blog", `${slug}.meta.json`);
  if (!existsSync(file)) return null;
  return JSON.parse(readFileSync(file, "utf8")) as ReportMeta;
}

export function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/&[a-z]+;/g, " ")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

export function stripTags(html: string): string {
  return html
    .replace(/<[^>]+>/g, "")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&rsquo;/g, "’")
    .replace(/&nbsp;/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

export function formatLongDate(iso: string): string {
  const d = new Date(`${iso.slice(0, 10)}T12:00:00Z`);
  return d.toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric", timeZone: "UTC" });
}

export function retrievedLabel(source: ReportSource): string {
  if (source.retrieved) {
    const base = formatLongDate(source.retrieved);
    return source.retrievedNote ? `${base} (${source.retrievedNote})` : base;
  }
  return source.retrievedNote || "Not recorded in the source registry";
}

function expandIds(token: string): string[] {
  const range = /^S(\d{3})\s*[–-]\s*S(\d{3})$/.exec(token);
  if (range) {
    const out: string[] = [];
    for (let n = Number(range[1]); n <= Number(range[2]); n += 1) out.push(`S${String(n).padStart(3, "0")}`);
    return out;
  }
  return /^S\d{3}$/.test(token) ? [token] : [];
}

function citeLink(id: string, sources: Record<string, ReportSource>, label = id): string {
  const source = sources[id];
  const tip = `${source.title}${source.revision ? `, revision ${source.revision}` : ""}. Tap to see the full source.`;
  return `<a class="cite-link" href="#src-${id}" data-cite="${id}" title="${escapeHtml(tip)}" aria-label="Source ${id}: ${escapeHtml(source.title)}">${label}</a>`;
}

/**
 * Turn source tokens (S017, S009–S012, [Jenkins, 2006]) in text into links to the
 * Sources section. Only text nodes are touched, never attributes, code or existing links.
 */
export function linkCitations(html: string, meta: ReportMeta | null): { html: string; used: string[] } {
  const sources = meta?.sources;
  if (!sources) return { html, used: [] };
  const aliases = meta?.aliases || {};
  const used = new Set<string>();
  const parts = html.split(/(<[^>]+>)/);
  let skip = 0;
  const pattern = /\[([^\[\]]{2,160})\]|\bS\d{3}(?:\s*[–-]\s*S\d{3})?\b/g;

  const resolve = (token: string): string[] => {
    const t = token.trim();
    const ids = expandIds(t);
    if (ids.length) return ids;
    const alias = aliases[t];
    return alias ? [alias] : [];
  };

  for (let i = 0; i < parts.length; i += 1) {
    const part = parts[i];
    if (part.startsWith("<")) {
      if (/^<(a|code|script|style|pre)\b/i.test(part)) skip += 1;
      else if (/^<\/(a|code|script|style|pre)>/i.test(part)) skip = Math.max(0, skip - 1);
      continue;
    }
    if (skip || !part) continue;
    parts[i] = part.replace(pattern, (full, inner?: string) => {
      if (inner !== undefined) {
        const tokens = inner.split(";");
        const resolved = tokens.map((token) => resolve(token));
        if (resolved.some((ids) => !ids.length || ids.some((id) => !sources[id]))) return full;
        const rendered = tokens.map((token, index) => {
          const ids = resolved[index];
          if (ids.length === 1 && !expandIds(token.trim()).length) {
            used.add(ids[0]);
            return citeLink(ids[0], sources, token.trim());
          }
          return ids
            .map((id) => {
              used.add(id);
              return citeLink(id, sources);
            })
            .join(", ");
        });
        return `<span class="cite">[${rendered.join("; ")}]</span>`;
      }
      const ids = expandIds(full.trim());
      if (!ids.length || ids.some((id) => !sources[id])) return full;
      return ids
        .map((id) => {
          used.add(id);
          return citeLink(id, sources);
        })
        .join(", ");
    });
  }
  return { html: parts.join(""), used: [...used] };
}

export type TocEntry = { id: string; text: string };

/** Ensure every H2 has an id, drop the legacy in-body contents list, return the H2 list. */
export function prepareHeadings(html: string): { html: string; toc: TocEntry[] } {
  const toc: TocEntry[] = [];
  const seen = new Set<string>();
  let out = html.replace(/<nav\b[^>]*id="TOC"[^>]*>[\s\S]*?<\/nav>/i, "");
  out = out.replace(/<h2\b([^>]*)>([\s\S]*?)<\/h2>/gi, (full, attrs: string, inner: string) => {
    const text = stripTags(inner);
    if (!text) return full;
    let id = /\bid="([^"]+)"/.exec(attrs)?.[1] || slugify(text);
    if (id === "toc-title") return full;
    while (seen.has(id)) id = `${id}-2`;
    seen.add(id);
    toc.push({ id, text });
    const nextAttrs = /\bid="/.test(attrs) ? attrs : `${attrs} id="${id}"`;
    return `<h2${nextAttrs}>${inner}</h2>`;
  });
  return { html: out, toc };
}

/**
 * Give every chart the same frame: heading, plain-language description, source line and data link.
 * Reports with a `charts` entry get the written copy; others reuse their existing caption.
 */
export function frameCharts(html: string, meta: ReportMeta | null, slug: string): string {
  return html.replace(/<figure class="art-chart">([\s\S]*?)<\/figure>/g, (full, inner: string) => {
    const chartPath = /data-chart="([^"]+)"/.exec(inner)?.[1] || "";
    const key = chartPath.split("/").pop()?.replace(/\.plotly\.json$/, "") || "";
    const live = /<div class="art-chart-live[\s\S]*?<\/div>/.exec(inner)?.[0] || "";
    if (!live) return full;
    const label = /aria-label="([^"]*)"/.exec(live)?.[1] || "Chart";
    const caption = /<figcaption[^>]*>([\s\S]*?)<\/figcaption>/.exec(inner)?.[1] || "";
    const written = meta?.charts?.[key];
    const title = written?.title || label;
    const description = written ? escapeHtml(written.description) : caption;
    const sourceLine = written?.source || /data-source="([^"]*)"/.exec(live)?.[1] || "";
    const data = written?.data?.length
      ? written.data
      : chartPath
        ? [{ label: "Chart data (JSON)", href: chartPath }]
        : [];
    const dataLinks = data
      .map((item) => `<a href="${escapeHtml(item.href)}" target="_blank" rel="noopener">${escapeHtml(item.label)}</a>`)
      .join(" · ");
    const headingId = `chart-${slugify(key || title)}`;
    return `<figure class="art-chart chart-frame" aria-labelledby="${headingId}">
<h3 class="chart-frame__title" id="${headingId}">${escapeHtml(title)}</h3>
<div class="chart-frame__plot">${live}<p class="chart-frame__hint">Swipe sideways inside the chart to read it at full size.</p></div>
<div class="chart-frame__copy">
<p class="chart-frame__desc">${description}</p>
<p class="chart-frame__meta"><span class="chart-frame__label">Source</span> ${sourceLine}</p>
<p class="chart-frame__meta"><span class="chart-frame__label">Data</span> ${dataLinks}</p>
</div>
</figure>`;
  });
}

export function fileSize(publicPath: string): string | null {
  if (!publicPath || /^https?:/.test(publicPath)) return null;
  const file = join(ROOT, "public", publicPath.replace(/^\//, ""));
  if (!existsSync(file)) return null;
  const bytes = statSync(file).size;
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export function formatKind(href: string): string {
  const ext = /\.([a-z0-9]+)(?:\?|$)/i.exec(href)?.[1]?.toUpperCase();
  return ext || "PAGE";
}
