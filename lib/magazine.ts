import issuesData from "@/magazine/issues.json";
import type { MagSkin } from "@/lib/magazine-skins";
import { decorateIssueHtml } from "@/lib/magazine-skins";

export type MagSource = { href: string | null; text: string };
export type MagFigure = { src: string; cap?: string | null };
export type MagSection = {
  h: string | null;
  ps: string[];
  fig: MagFigure | null;
};
export type MagIssue = {
  slug: string;
  kicker: string;
  title: string;
  dek: string;
  author: string;
  date: string;
  pub: string;
  tags: string[];
  hero: string;
  kp: { n: string; l: string }[];
  sections: MagSection[];
  src: MagSource[];
  words: number;
  origWords?: number;
  isFix?: boolean;
  custom?: string;
  /** Reader skins. Omitted issues use the three shared defaults. */
  skins?: MagSkin[];
};

const DESKS = [
  { id: "arts", label: "Arts" },
  { id: "sports", label: "Sports" },
  { id: "science", label: "Science" },
  { id: "humanities", label: "Humanities" },
  { id: "civics", label: "Civics" },
  { id: "culture", label: "Culture" },
] as const;

/** Cover order from the October 2026 edition. */
const FEATURED = ["franchise", "anime", "padres", "youtube", "readmitted"];

const ALL = issuesData as MagIssue[];

export const MAGAZINE_SLUGS: string[] = ALL.map((issue) => issue.slug);

const BY_SLUG = new Map(ALL.map((issue) => [issue.slug, issue]));

export function magazineImg(src: string | null | undefined): string {
  if (!src) return "";
  return `/img${src.replace(/\.(png|webp|jpe?g)$/i, ".jpg")}`;
}

export function magazineMins(words: number): number {
  return Math.max(1, Math.round((Number(words) || 0) / 140));
}

export function magazineIssues(): MagIssue[] {
  const featured = FEATURED.map((slug) => BY_SLUG.get(slug)).filter(
    (issue): issue is MagIssue => Boolean(issue),
  );
  const rest = ALL.filter((issue) => !FEATURED.includes(issue.slug));
  return [...featured, ...rest];
}

export function magazineIssue(slug: string | undefined): MagIssue | undefined {
  if (!slug) return undefined;
  const key = slug.replace(/^\/+|\/+$/g, "");
  return BY_SLUG.get(key);
}

/** URL prefix for the page-flip magazine reader (not the default site chrome). */
export const MAGAZINE_HOME_PATH = "/mag";

export function magazineContentsHref(skinId?: string | null): string {
  if (!skinId || skinId === "house") return MAGAZINE_HOME_PATH;
  return `${MAGAZINE_HOME_PATH}?skin=${encodeURIComponent(skinId)}`;
}

export function magazineIssueHref(slug: string, skinId?: string | null): string {
  const base = `${MAGAZINE_HOME_PATH}/${encodeURIComponent(slug.replace(/^\/+|\/+$/g, ""))}`;
  if (!skinId || skinId === "house") return base;
  return `${base}?skin=${encodeURIComponent(skinId)}`;
}

/** `/mag` and `/mag/{slug}` render the page-flip edition without site chrome. */
export function isMagazinePath(pathname: string | undefined): boolean {
  const path = (pathname || "/").split("?")[0].split("#")[0].replace(/\/$/, "") || "/";
  if (path === MAGAZINE_HOME_PATH) return true;
  if (!path.startsWith(`${MAGAZINE_HOME_PATH}/`)) return false;
  const rest = path.slice(MAGAZINE_HOME_PATH.length + 1);
  if (!rest || rest.includes("/")) return false;
  return BY_SLUG.has(rest);
}

function esc(value: string | number | null | undefined): string {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function safeHref(href: string | null | undefined): string | null {
  if (!href) return null;
  const trimmed = href.trim();
  if (/^(https?:|mailto:)/i.test(trimmed)) return trimmed;
  return null;
}

function figureHtml(fig: MagFigure | null | undefined, caption: boolean): string {
  if (!fig?.src) return "";
  const cap = fig.cap ? esc(fig.cap) : "";
  const capHtml = caption && cap ? `<figcaption>${cap}</figcaption>` : "";
  return `<figure class="fig"><img src="${esc(magazineImg(fig.src))}" alt="${cap}"/>${capHtml}</figure>`;
}

export function renderIssueBody(issue: MagIssue): string {
  const minutes = magazineMins(issue.words);
  if (issue.custom) {
    return decorateIssueHtml(issue, issue.custom.replace(/· 5 min/g, `· ${minutes} min`));
  }
  const sections = issue.sections || [];
  const [first, ...rest] = sections;
  const hero = issue.hero
    ? `<img class="hero" src="${esc(magazineImg(issue.hero))}" alt="${esc(issue.kicker)} illustration from the Artometrics report">`
    : "";
  const lead = first
    ? `${first.h ? `<h2>${esc(first.h)}</h2>` : ""}${(first.ps || []).map((paragraph) => `<p>${paragraph}</p>`).join("")}`
    : "";
  const points = (issue.kp || [])
    .map(
      (point) =>
        `<div class="kp fade"><p class="big">${esc(point.n)}</p><p>${esc(point.l)}</p></div>`,
    )
    .join("");
  const restHtml = rest
    .map((section) => {
      const heading = section.h ? `<h2>${esc(section.h)}</h2>` : "";
      const paragraphs = (section.ps || []).map((paragraph) => `<p>${paragraph}</p>`).join("");
      return `${heading}${figureHtml(section.fig, true)}${paragraphs}`;
    })
    .join("");
  return decorateIssueHtml(
    issue,
    `<p class="kick">${esc(issue.kicker)}</p>
<h1 itemprop="headline">${esc(issue.title)}</h1>
<p class="dek" itemprop="description">${esc(issue.dek)}</p>
<p class="by">By <span itemprop="author">${esc(issue.author)}</span> · <time itemprop="dateModified" datetime="${esc(issue.date)}">${esc(issue.date)}</time> · ${minutes} min</p>
${hero}
${lead}
${points}
${figureHtml(first?.fig, true)}
${restHtml}`,
  );
}

export function renderContentsBody(issues: MagIssue[] = magazineIssues()): string {
  const [featured, ...rest] = issues;
  if (!featured) return `<p class="dek">No issues in this edition.</p>`;
  const groups = DESKS.map((desk) => ({
    ...desk,
    items: rest.filter((issue) => (issue.tags || []).includes(desk.id)),
  })).filter((desk) => desk.items.length);
  const lists = groups
    .map(
      (desk) => `<h2 class="toc-sec">${esc(desk.label)} · ${desk.items.length}</h2>
<ul class="toc">${desk.items
        .map(
          (issue) =>
            `<li><a href="${esc(magazineIssueHref(issue.slug))}"><img src="${esc(magazineImg(issue.hero))}" alt="" loading="lazy"><span><small>${esc(issue.kicker)}</small><b>${esc(issue.title)}</b><em>${magazineMins(issue.words)} min</em></span></a></li>`,
        )
        .join("")}</ul>`,
    )
    .join("");
  return `<p class="cv-mast">ARTOMETRICS</p><p class="cv-sub">Magazine · ${issues.length} issues · 5-minute reads</p>
<a class="cv-feat" href="${esc(magazineIssueHref(featured.slug))}"><img src="${esc(magazineImg(featured.hero))}" alt=""><p class="kick" style="margin-top:12px">${esc(featured.kicker)}</p><h3>${esc(featured.title)}</h3><p class="dek">${esc(featured.dek)}</p></a>
${lists}`;
}

export function issueJsonLd(issue: MagIssue): Record<string, unknown> {
  const minutes = magazineMins(issue.words);
  const image = magazineImg(issue.hero);
  return {
    "@context": "https://schema.org",
    "@type": "Article",
    headline: issue.title,
    description: issue.dek,
    author: { "@type": "Person", name: issue.author },
    publisher: {
      "@type": "Organization",
      name: "Artometrics",
      url: "https://artometrics.com",
    },
    datePublished: issue.pub,
    dateModified: issue.date,
    mainEntityOfPage: `https://artometrics.com${magazineIssueHref(issue.slug)}`,
    image: image ? [`https://artometrics.com${image}`] : undefined,
    wordCount: issue.words,
    timeRequired: `PT${minutes}M`,
    keywords: (issue.tags || []).join(", "),
    citation: (issue.src || []).map((source) => safeHref(source.href)).filter(Boolean),
  };
}

export function contentsJsonLd(issues: MagIssue[] = magazineIssues()): Record<string, unknown> {
  return {
    "@context": "https://schema.org",
    "@type": "CollectionPage",
    name: "Artometrics Magazine",
    url: "https://artometrics.com/mag",
    hasPart: issues.map((issue) => ({
      "@type": "Article",
      headline: issue.title,
      url: `https://artometrics.com${magazineIssueHref(issue.slug)}`,
    })),
  };
}
