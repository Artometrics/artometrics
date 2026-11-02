import type { MagIssue, MagSource } from "@/lib/magazine";
import skinDefaults from "@/magazine/skin-defaults.json";

export type MagSkinTokens = {
  paper: string;
  ink: string;
  accent: string;
  accent2: string;
  rule: string;
};

export type MagSkin = {
  id: string;
  name: string;
  tokens: MagSkinTokens;
  fonts: { display: string; body: string; figures: string };
  ornaments: string[];
  closing: { name: string; style: string };
};

export const DEFAULT_SKINS = skinDefaults as MagSkin[];

/** Default reader. Dark ground, Anton, Tiffany, hot-pink rule — the site house, not cream paper. */
export const HOUSE_SKIN: MagSkin = {
  id: "house",
  name: "House",
  tokens: {
    paper: "#100e0c",
    ink: "#f4f7f6",
    accent: "#7fded6",
    accent2: "#ff3d8a",
    rule: "#ff3d8a",
  },
  fonts: {
    display: "Anton",
    body: "DM Sans",
    figures: "DM Mono",
  },
  ornaments: [],
  closing: { name: "House Style", style: "house" },
};

export const DEFAULT_MAG_SKIN_ID = HOUSE_SKIN.id;

/** House is always the first skin, so a fresh open is the dark edition. */
export function withHouseSkin(skins: MagSkin[]): MagSkin[] {
  const rest = skins.filter((skin) => skin.id !== HOUSE_SKIN.id);
  return [HOUSE_SKIN, ...rest];
}

const FONT_STACK: Record<string, string> = {
  Anton: '"Anton", Impact, sans-serif',
  "DM Sans": '"DM Sans", system-ui, sans-serif',
  "DM Mono": '"DM Mono", ui-monospace, monospace',
  Chomsky: '"Chomsky", Georgia, serif',
  "Libre Caslon Text": '"Libre Caslon Text", Georgia, "Iowan Old Style", serif',
  "Source Serif 4": '"Source Serif 4", Georgia, "Iowan Old Style", serif',
  "IBM Plex Mono": '"IBM Plex Mono", ui-monospace, monospace',
  "Dela Gothic One": '"Dela Gothic One", "Hiragino Sans", "Yu Gothic", sans-serif',
  Inter: "Inter, system-ui, sans-serif",
  "Space Mono": '"Space Mono", ui-monospace, monospace',
  Oswald: "Oswald, Impact, sans-serif",
  "Old Standard TT": '"Old Standard TT", Georgia, serif',
  Archivo: "Archivo, system-ui, sans-serif",
  Bungee: "Bungee, system-ui, sans-serif",
  "Space Grotesk": '"Space Grotesk", system-ui, sans-serif',
  "JetBrains Mono": '"JetBrains Mono", ui-monospace, monospace',
};

/** Skins Billboard, Streaming, and YouTube used before they had their own sets. A saved or shared link for one of these resolves to that issue's first skin. */
const RETIRED_SHARED_SKINS = new Set(["ledger", "box", "trade"]);

function retiredSharedSkin(slug: string, id: string): boolean {
  return (slug === "billboard" || slug === "streaming" || slug === "youtube") && RETIRED_SHARED_SKINS.has(id);
}

export function resolveSkinId(
  slug: string,
  skins: { id: string }[],
  query: string | null | undefined,
  saved: string | null | undefined,
): string {
  const ids = new Set(skins.map((skin) => skin.id));
  const fallback = skins[0]?.id || DEFAULT_MAG_SKIN_ID;
  const asked = (query || "").trim();
  if (retiredSharedSkin(slug, asked)) return fallback;
  if (asked && ids.has(asked)) return asked;
  const stored = (saved || "").trim();
  if (retiredSharedSkin(slug, stored)) return fallback;
  if (stored && ids.has(stored)) return stored;
  return fallback;
}

const MONTHS = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];

export function skinsForIssue(issue: { skins?: MagSkin[] | null }): MagSkin[] {
  const list = issue.skins;
  if (!Array.isArray(list) || list.length === 0) return withHouseSkin(DEFAULT_SKINS);
  const usable = list.filter(
    (skin) => skin && skin.id && skin.name && skin.tokens?.paper && skin.tokens?.ink && skin.closing?.name,
  );
  const base = usable.length === list.length ? list : usable.length ? usable : DEFAULT_SKINS;
  return withHouseSkin(base);
}

export function skinStorageKey(slug: string): string {
  return `artometrics-mag-skin:v2:${slug}`;
}

export function skinCssVars(skin: MagSkin): Record<string, string> {
  return {
    "--paper": skin.tokens.paper,
    "--ink": skin.tokens.ink,
    "--accent": skin.tokens.accent,
    "--accent2": skin.tokens.accent2,
    "--rule": skin.tokens.rule,
    "--blue": skin.tokens.accent,
    "--skin-display": FONT_STACK[skin.fonts.display] || `"${skin.fonts.display}", Georgia, serif`,
    "--skin-body": FONT_STACK[skin.fonts.body] || `"${skin.fonts.body}", Georgia, serif`,
    "--skin-figures": FONT_STACK[skin.fonts.figures] || `"${skin.fonts.figures}", ui-monospace, monospace`,
    backgroundColor: skin.tokens.paper,
    color: skin.tokens.ink,
  };
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
  if (trimmed.startsWith("/") && !trimmed.startsWith("//")) return trimmed;
  return null;
}

export function formatSkinDate(date: string | undefined): string {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(date || "");
  if (!match) return date || "";
  const month = MONTHS[Number(match[2]) - 1] || match[2];
  return `${month} ${Number(match[3])}, ${match[1]}`;
}

function named(ledger: string, box: string, trade: string): string {
  return `<span data-for="house">${ledger}</span><span data-for="ledger">${ledger}</span><span data-for="box">${box}</span><span data-for="trade">${trade}</span>`;
}

function ornaments(): string {
  return `<div class="skin-ornaments" aria-hidden="true">
<svg data-orn="tick" viewBox="0 0 24 24"><path d="M5 4h2v16H5zM10 12l3 3 6-7" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>
<svg data-orn="coins" viewBox="0 0 24 24"><ellipse cx="12" cy="7" rx="6" ry="2.4" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M6 7v4c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5V7M6 11v4c0 1.4 2.7 2.5 6 2.5s6-1.1 6-2.5v-4" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
<svg data-orn="tear" viewBox="0 0 24 24"><path d="M3 8h18M4 14l2 2 2-2 2 2 2-2 2 2 2-2 2 2" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
<svg data-orn="fist" viewBox="0 0 24 24"><path d="M4 12h8l2-2h3M14 12c2 2 6 2 7 0M8 12v5M11 12v4" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
<svg data-orn="tag" viewBox="0 0 24 24"><path d="M4 12l8-8h7v7l-8 8z" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="16.5" cy="7.5" r="1" fill="currentColor"/></svg>
<svg data-orn="card" viewBox="0 0 24 24"><path d="M4 5h16v14H4zM4 5l4 4M20 5l-4 4M4 19l4-4M20 19l-4-4" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
<svg data-orn="burst" viewBox="0 0 24 24"><path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z" fill="currentColor"/></svg>
<svg data-orn="barcode" viewBox="0 0 24 24"><path d="M4 6h1.2v12H4zM7 6h.6v12H7zM9 6h1.6v12H9zM12 6h.5v12H12zM14 6h1.4v12H14zM17 6h.7v12H17zM19.2 6H21v12h-1.8z" fill="currentColor"/></svg>
<svg data-orn="ticket" viewBox="0 0 24 24"><path d="M3 8a2 2 0 010 8v3h18v-3a2 2 0 010-8V5H3z" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M12 6v12" stroke="currentColor" stroke-dasharray="1.5 2"/></svg>
<svg data-orn="sprocket" viewBox="0 0 24 24"><circle cx="7" cy="6" r="1.4" fill="currentColor"/><circle cx="7" cy="12" r="1.4" fill="currentColor"/><circle cx="7" cy="18" r="1.4" fill="currentColor"/><circle cx="17" cy="6" r="1.4" fill="currentColor"/><circle cx="17" cy="12" r="1.4" fill="currentColor"/><circle cx="17" cy="18" r="1.4" fill="currentColor"/></svg>
<svg data-orn="bulbs" viewBox="0 0 24 24"><circle cx="4" cy="12" r="1.6" fill="currentColor"/><circle cx="10" cy="12" r="1.6" fill="currentColor"/><circle cx="16" cy="12" r="1.6" fill="currentColor"/><circle cx="22" cy="12" r="1.6" fill="currentColor"/></svg>
<svg data-orn="halftone" viewBox="0 0 24 24"><circle cx="6" cy="6" r="1.2" fill="currentColor"/><circle cx="12" cy="6" r="1.8" fill="currentColor"/><circle cx="18" cy="6" r="1.1" fill="currentColor"/><circle cx="6" cy="12" r="2" fill="currentColor"/><circle cx="12" cy="12" r="1.3" fill="currentColor"/><circle cx="18" cy="12" r="2.1" fill="currentColor"/><circle cx="6" cy="18" r="1.1" fill="currentColor"/><circle cx="12" cy="18" r="1.7" fill="currentColor"/><circle cx="18" cy="18" r="1.2" fill="currentColor"/></svg>
<svg data-orn="rank" viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M11 8.2h1.4V16M11 16h2.6" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
<svg data-orn="peak" viewBox="0 0 24 24"><path d="M12 4.5l6.5 13h-13z" fill="var(--accent2)"/></svg>
<svg data-orn="weeks" viewBox="0 0 24 24"><path d="M3 17h18M6 17V11M10 17V7M14 17V12M18 17V9" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
<svg data-orn="bullet" viewBox="0 0 24 24"><circle cx="12" cy="12" r="7.2" fill="none" stroke="currentColor" stroke-width="1.4"/><circle cx="12" cy="12" r="3" fill="var(--accent2)"/></svg>
<svg data-orn="spindle" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="1.5"/><circle cx="12" cy="12" r="1.7" fill="currentColor"/></svg>
<svg data-orn="grooves" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3" fill="none" stroke="currentColor" stroke-width="1.3"/><circle cx="12" cy="12" r="6.2" fill="none" stroke="currentColor" stroke-width="1.3"/><circle cx="12" cy="12" r="9.2" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>
<svg data-orn="flap" viewBox="0 0 24 24"><path d="M4 8h16v12H4z" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M4 8c2.4 3.2 13.6 3.2 16 0" fill="none" stroke="currentColor" stroke-width="1.4"/></svg>
<svg data-orn="center" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4.2" fill="var(--accent2)"/></svg>
<svg data-orn="play" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M10.2 8.8v6.4l5.4-3.2z" fill="currentColor"/></svg>
<svg data-orn="scrub" viewBox="0 0 24 24"><path d="M3 12h18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><circle cx="16" cy="12" r="2.5" fill="var(--accent2)"/></svg>
<svg data-orn="wave" viewBox="0 0 24 24"><path d="M4 15V9M8 17V7M12 19V5M16 17V7M20 15V9" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
<svg data-orn="queue" viewBox="0 0 24 24"><path d="M4 7h16M4 12h11M4 17h16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
<svg data-orn="spines" viewBox="0 0 24 24"><path d="M3 4h3.2v16H3zM9 12h3v8H9zM15 13.5h3v6.5h-3z" fill="currentColor"/></svg>
<svg data-orn="shelf-rule" viewBox="0 0 24 24"><path d="M2 17h20v2.2H2zM5 7h2.2v10H5zM10.5 11h2.2v6h-2.2zM16 12.5h2.2v4.5H16z" fill="currentColor"/></svg>
<svg data-orn="price-sticker" viewBox="0 0 24 24"><circle cx="12" cy="12" r="7" fill="var(--accent2)"/><circle cx="12" cy="12" r="1.3" fill="var(--paper)"/></svg>
<svg data-orn="tape-label" viewBox="0 0 24 24"><rect x="3" y="9" width="18" height="6" fill="var(--accent2)" transform="rotate(-8 12 12)"/></svg>
<svg data-orn="time-slot" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M3 9h18" stroke="var(--accent2)" stroke-width="2"/><path d="M7 14h6" stroke="currentColor" stroke-width="1.4"/></svg>
<svg data-orn="listing-grid" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16M9 4v16" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>
<svg data-orn="dot-leaders" viewBox="0 0 24 24"><circle cx="4" cy="12" r="1.3" fill="currentColor"/><circle cx="9" cy="12" r="1.3" fill="currentColor"/><circle cx="14" cy="12" r="1.3" fill="currentColor"/><circle cx="19" cy="12" r="1.3" fill="currentColor"/></svg>
<svg data-orn="clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="7.2" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M12 8v4.2l2.6 1.8" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><circle cx="12" cy="12" r="1.1" fill="var(--accent2)"/></svg>
<svg data-orn="scrubber" viewBox="0 0 24 24"><path d="M3 13h18" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M3 13h12" fill="none" stroke="var(--accent2)" stroke-width="1.6" stroke-linecap="round"/><circle cx="15" cy="13" r="2.3" fill="var(--accent2)"/></svg>
<svg data-orn="chapter-ticks" viewBox="0 0 24 24"><path d="M4 17V9M8 17v-5M12 17V7M16 17v-6M20 17v-3" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
<svg data-orn="play-triangle" viewBox="0 0 24 24"><path d="M8 6.2v11.6l10-5.8z" fill="currentColor"/></svg>
<svg data-orn="film-frame" viewBox="0 0 24 24"><path d="M5 9V5h4M15 5h4v4M19 15v4h-4M9 19H5v-4" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>
<svg data-orn="double-rules" viewBox="0 0 24 24"><path d="M3 8h18M3 11h18M3 16h18" fill="none" stroke="currentColor" stroke-width="1.3"/></svg>
<svg data-orn="dagger" viewBox="0 0 24 24"><path d="M12 3.5v13M8.2 7.2h7.6" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/><path d="M12 16.2l-2.4 4.3h4.8z" fill="var(--accent2)"/></svg>
<svg data-orn="brackets" viewBox="0 0 24 24"><path d="M8 4.5H4.5v15H8M16 4.5h3.5v15H16" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M11 12h2" stroke="var(--accent2)" stroke-width="2.2" stroke-linecap="round"/></svg>
<svg data-orn="page-tab" viewBox="0 0 24 24"><path d="M5 20V7h8l4 4v9z" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M13 7v4h4" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M8 15h6" stroke="var(--accent2)" stroke-width="1.6"/></svg>
<svg data-orn="share-bar" viewBox="0 0 24 24"><rect x="3" y="10" width="18" height="4" fill="none" stroke="currentColor" stroke-width="1.4"/><rect x="3" y="10" width="2.8" height="4" fill="var(--accent2)"/></svg>
<svg data-orn="screen-frame" viewBox="0 0 24 24"><rect x="3.5" y="4" width="17" height="12" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M9 20h6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
<svg data-orn="scan-line" viewBox="0 0 24 24"><path d="M3 6h18M3 10h18M3 14h18M3 18h18" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>
<svg data-orn="channel-tag" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M3 9.2h18" stroke="var(--accent2)" stroke-width="2"/><path d="M7 14.5h5" stroke="currentColor" stroke-width="1.4"/></svg>
<svg data-orn="lamp" viewBox="0 0 24 24"><rect x="4" y="6" width="16" height="12" fill="none" stroke="currentColor" stroke-width="1.4"/><circle cx="9" cy="12" r="2.2" fill="var(--accent2)"/><path d="M13 10.5h5M13 13.5h3.5" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/></svg>
<svg data-orn="grille" viewBox="0 0 24 24"><circle cx="4" cy="8" r="1.05" fill="currentColor"/><circle cx="8.5" cy="8" r="1.05" fill="currentColor"/><circle cx="13" cy="8" r="1.05" fill="currentColor"/><circle cx="17.5" cy="8" r="1.05" fill="currentColor"/><circle cx="4" cy="12.5" r="1.05" fill="currentColor"/><circle cx="8.5" cy="12.5" r="1.05" fill="currentColor"/><circle cx="13" cy="12.5" r="1.05" fill="currentColor"/><circle cx="17.5" cy="12.5" r="1.05" fill="currentColor"/><circle cx="4" cy="17" r="1.05" fill="currentColor"/><circle cx="8.5" cy="17" r="1.05" fill="currentColor"/><circle cx="13" cy="17" r="1.05" fill="currentColor"/><circle cx="17.5" cy="17" r="1.05" fill="currentColor"/></svg>
<svg data-orn="waveform" viewBox="0 0 24 24"><path d="M3 14V10M6.2 16.5V7.5M9.4 13V11M12.6 18V6M15.8 15V9M19 12.5V11.5M22 14.5V9.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
<svg data-orn="peak-mark" viewBox="0 0 24 24"><path d="M2 16h5.2l3.2-8 3.4 8H22" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><circle cx="10.4" cy="8" r="1.7" fill="var(--accent2)"/></svg>
</div>`;
}

function plates(): string {
  return `<figure class="skin-plate">
<img data-for="ledger" src="/images/skins/pacioli.jpg" width="960" height="800" alt="Portrait of Luca Pacioli, attributed to Jacopo de' Barbari, about 1495">
<img data-for="box" src="/images/skins/toy-shop.jpg" width="960" height="679" alt="Color print of a toy shop by Utagawa Sadahide, 1860">
<img data-for="trade" src="/images/skins/belasco-box-office.jpg" width="960" height="1189" alt="Belasco Theatre box office, published 1907">
<figcaption>${named(
    "Pacioli, c. 1495 · public domain",
    "Sadahide, toy shop, 1860 · CC0",
    "Belasco box office, 1907 · public domain",
  )}</figcaption>
</figure>`;
}

function dateline(issue: MagIssue): string {
  const date = formatSkinDate(issue.date);
  if (issue.slug === "franchise") return `${date} · 140 FRANCHISES · $1,448.1B`;
  return `${date}${issue.kicker ? ` · ${issue.kicker}` : ""}`;
}

function disclaimer(issue: MagIssue): string {
  if (issue.slug === "franchise") {
    return "Figures are Wikipedia editors' estimates of consumer spending in nominal dollars, not audited studio financials. “The US out-earns Japan” is a fact about this English-language list, not about national industries. Several Japanese totals were revised at the source (Hello Kitty $80.0B to $33.5B; Mario $35.0B to $9.74B); Sanrio and Nintendo reported no collapse.";
  }
  return "Artometrics data brief. Figures come from the sources below. Derived shares and editorial indices are not audited financials.";
}

function method(issue: MagIssue): string {
  if (issue.slug === "franchise") {
    return `Shares carry 95% bootstrap ranges (merchandise 44.0–66.2). The 2019 file was audited against Wikipedia revision 904026364 on a 40-franchise random sample (seed 20261012). <a href="/franchise-data-fix">What changed when we fixed the data</a>.`;
  }
  return "Numbers in this issue are the published figures. The skin changes type, rules, and chart color only.";
}

function alreadyListed(text: string, href: string | null, published: string): boolean {
  if (!published) return false;
  if (text.includes("904026364") && !published.includes("904026364")) return false;
  if (href && published.includes(href)) return true;
  const needles = ["10-K", "S004", "Hernández", "doi.org/10.3390/arts7030042", "2019-07-02", "1379832186", "tidytuesday", "CPI-U", "CPIAUCSL", "Jenkins", "Steinberg", "Robinson", "box_office_mojo"];
  for (const needle of needles) {
    if (text.includes(needle) && published.includes(needle)) return true;
  }
  const slice = text.slice(0, 42);
  return slice.length > 16 && published.includes(slice);
}

function sourceItem(source: MagSource): string {
  const href = safeHref(source.href);
  const text = esc(source.text);
  const body = href ? `<a href="${esc(href)}">${text}</a>` : text;
  return `<li><span class="role">Source</span>${body}</li>`;
}

function closingSources(issue: MagIssue, publishedInner: string): string {
  const items: string[] = [];
  const published = publishedInner.trim().replace(/<li>/g, '<li><span class="role">Source</span>');
  if (published) items.push(published);
  for (const source of issue.src || []) {
    const href = safeHref(source.href);
    if (alreadyListed(source.text || "", href, published)) continue;
    items.push(sourceItem(source));
  }
  const reportHref = `https://artometrics.com/${issue.slug}`;
  const joined = items.join("");
  if (!joined.includes(`artometrics.com/${issue.slug}`)) {
    items.push(
      `<li><span class="role">Report</span>Full report: <a href="${esc(reportHref)}">artometrics.com/${esc(issue.slug)}</a></li>`,
    );
  }
  return items.join("\n");
}

function credits(issue: MagIssue): string {
  const hero = issue.hero
    ? `<li class="hero-credit"><span class="role">Hero</span>Artometrics ${esc(issue.kicker || "report")} illustration.</li>`
    : "";
  return `${hero}
<li data-for="ledger"><span class="role">Plate</span><a href="https://commons.wikimedia.org/wiki/File:Pacioli.jpg">Portrait of Luca Pacioli</a>, attributed to Jacopo de' Barbari, c. 1495. Public domain, via Wikimedia Commons.</li>
<li data-for="box"><span class="role">Plate</span><a href="https://commons.wikimedia.org/wiki/File:Doban-e_J%C5%8Dgy%C5%8D_shiki-Color_Print_of_a_Copperplate_Picture_of_a_Toy_Shop_MET_DP147967.jpg">Color print of a toy shop</a>, Utagawa Sadahide, 1860. The Metropolitan Museum of Art, CC0, via Wikimedia Commons.</li>
<li data-for="trade"><span class="role">Plate</span><a href="https://commons.wikimedia.org/wiki/File:Belasco_Theatre_box_office.jpg">Belasco Theatre box office</a>, published November 1907 in Architects' and Builders' Magazine. Unknown photographer. Public domain, via Wikimedia Commons.</li>`;
}

function usesSharedPlates(issue: MagIssue): boolean {
  return skinsForIssue(issue).some((skin) => skin.id === "ledger" || skin.id === "box" || skin.id === "trade");
}

function billboardSourceItem(source: MagSource): string {
  const href = safeHref(source.href);
  const text = esc(source.text);
  const body = href ? `<a href="${esc(href)}">${text}</a>` : text;
  return `<li>${body}</li>`;
}

/** Title chrome only. The headline string stays the published title. */
function billboardPresentation(html: string): string {
  const title = '<h1 itemprop="headline">How Long Number-Ones Stay on Top</h1>';
  const stage = `<div class="bb-stage"><span class="bb-rank" aria-hidden="true">1</span><h1 class="skin-title" itemprop="headline">How Long Number-Ones Stay on Top</h1><span class="bb-hole" aria-hidden="true"></span><span class="bb-player" aria-hidden="true"><span class="bb-play"></span><span class="bb-track"><span class="bb-fill"></span></span><span class="bb-scale"><span>0</span><span>25 weeks</span></span></span></div>`;
  return html.includes(title) ? html.replace(title, stage) : html;
}

const STREAMING_TITLE = "Netflix's Top 10% of Titles Drew 68% of Viewing";

/** Title chrome only. The headline string stays the published title. */
function streamingPresentation(html: string): string {
  const lead = `<p class="kick">Streaming</p>\n<h1 itemprop="headline">${STREAMING_TITLE}</h1>`;
  const spines = `<svg class="st-spines" viewBox="0 0 340 86" aria-hidden="true" focusable="false" fill="currentColor"><rect x="0" y="76" width="340" height="8"/><rect x="6" y="4" width="24" height="72"/><rect x="44" y="40" width="18" height="36"/><rect x="76" y="40" width="20" height="36"/><rect x="110" y="40" width="16" height="36"/><rect x="140" y="40" width="20" height="36"/><rect x="174" y="40" width="18" height="36"/><rect x="206" y="40" width="20" height="36"/><rect x="240" y="40" width="16" height="36"/><rect x="270" y="40" width="20" height="36"/><rect x="304" y="40" width="18" height="36"/></svg>`;
  const stage = `<div class="st-stage"><span class="st-clip" aria-hidden="true"></span><span class="st-slot">JAN–JUN 2026</span><h1 class="skin-title" itemprop="headline">${STREAMING_TITLE}</h1><span class="st-leaders" aria-hidden="true"></span><p class="kick st-channel">Streaming</p>${spines}<div class="st-scrub"><span class="st-play" aria-hidden="true"></span><span class="st-track" aria-hidden="true"><span class="st-fill"></span></span><span class="st-scrub-label">top 10% of titles</span></div></div>`;
  return html.includes(lead) ? html.replace(lead, stage) : html;
}

const YOUTUBE_TITLE = "The Platform's $36B Engine and One Podcast's Borrowed Peak";

/** Title chrome only. The headline string stays the published title. */
function youtubePresentation(html: string): string {
  const lead = `<p class="kick">YouTube</p>\n<h1 itemprop="headline">${YOUTUBE_TITLE}</h1>`;
  const peak = `<svg class="yt-peak-line" viewBox="0 0 280 40" aria-hidden="true" focusable="false"><path d="M4 30h36l28-2 24-18 26 18h158" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><circle cx="92" cy="10" r="3.4" fill="var(--accent2)"/></svg>`;
  const wave = `<svg class="yt-wave" viewBox="0 0 240 24" aria-hidden="true" focusable="false"><path d="M4 14V10M16 18V6M28 13V11M40 20V4M52 15V9M64 16V8M76 17V7M88 19V5M100 14V10M112 11V13M124 18V6M136 15V9M148 17V7M160 20V4M172 16V8M184 13V11M196 18V6M208 14V10M220 16V8M232 13V11" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>`;
  const stage = `<div class="yt-stage"><p class="kick yt-kicker">YouTube</p><span class="yt-lamp"><span class="yt-lamp-dot" aria-hidden="true"></span><span class="yt-lamp-word">ON AIR</span></span><h1 class="skin-title" itemprop="headline">${YOUTUBE_TITLE}</h1><div class="yt-rev"><span class="yt-tab" aria-hidden="true">p.</span><span class="yt-rev-name">YouTube ads, FY2024</span><span class="yt-rev-sep">|</span><span class="yt-rev-amt">$36,147 million</span></div><div class="yt-share"><span class="yt-share-track" role="img" aria-label="15.8 percent"><span class="yt-share-fill"></span></span><span class="yt-share-label">of U.S. TV-screen time, August 2026 (Nielsen Gauge)</span></div><div class="yt-peak">${peak}<span class="yt-peak-label">the borrowed peak</span></div>${wave}</div>`;
  return html.includes(lead) ? html.replace(lead, stage) : html;
}

function youtubeClosing(issue: MagIssue): string {
  const names = skinsForIssue(issue)
    .map((skin) => `<span data-for="${esc(skin.id)}">${esc(skin.closing.name)}</span>`)
    .join("");
  const sources = (issue.src || []).map(billboardSourceItem).join("");
  return `<section class="closing" id="closing">
<p class="end">■ END</p>
<h2 class="closing-name">${names}</h2>
<ol class="src">${sources}</ol>
<p class="updated">Updated through: Nielsen Gauge, August 2026 (press release October 22, 2026)</p>
<p class="by skin-back"><a href="/">← Contents</a></p>
</section>`;
}

function streamingClosing(issue: MagIssue): string {
  const names = skinsForIssue(issue)
    .map((skin) => `<span data-for="${esc(skin.id)}">${esc(skin.closing.name)}</span>`)
    .join("");
  const sources = (issue.src || []).map(billboardSourceItem).join("");
  return `<section class="closing" id="closing">
<p class="end">■ END</p>
<h2 class="closing-name">${names}</h2>
<ol class="src">${sources}</ol>
<p class="updated">Updated through: weeks ending June 28, 2026</p>
<p class="by skin-back"><a href="/">← Contents</a></p>
</section>`;
}

function billboardClosing(issue: MagIssue): string {
  const names = skinsForIssue(issue)
    .map((skin) => `<span data-for="${esc(skin.id)}">${esc(skin.closing.name)}</span>`)
    .join("");
  const sources = (issue.src || []).map(billboardSourceItem).join("");
  return `<section class="closing" id="closing">
<p class="end">■ END</p>
<h2 class="closing-name">${names}</h2>
<ol class="src">${sources}</ol>
<p class="updated">Updated through: chart dated Oct 31, 2026</p>
<p class="hero-credit">Artometrics Billboard report illustration.</p>
<p class="by skin-back"><a href="/">← Contents</a></p>
</section>`;
}

function closingSection(issue: MagIssue, publishedInner: string): string {
  if (issue.slug === "billboard") return billboardClosing(issue);
  if (issue.slug === "streaming") return streamingClosing(issue);
  if (issue.slug === "youtube") return youtubeClosing(issue);
  const names = skinsForIssue(issue)
    .map((skin) => `<span data-for="${esc(skin.id)}">${esc(skin.closing.name)}</span>`)
    .join("");
  return `<section class="closing" id="closing">
<p class="end">■ END</p>
<h2 class="closing-name">${names}</h2>
<div class="close-warn"><h3>${named("Note", "Warnings", "Disclaimer")}</h3><p class="disclaimer">${esc(disclaimer(issue))}</p></div>
<div class="close-src"><h3>${named("Sources", "Contents", "Sources")}</h3><ol class="src">${closingSources(issue, publishedInner)}</ol></div>
<div class="close-method"><h3>${named("Method", "Assembly", "Method")}</h3><p class="method">${method(issue)}</p></div>
<div class="close-credit"><h3>${named("Plates", "Made by", "Image credits")}</h3><ul class="credits">${credits(issue)}</ul></div>
<p class="updated">Updated through ${esc(formatSkinDate(issue.date))}.</p>
<p class="by skin-back"><a href="/">← Contents</a></p>
</section>`;
}

function franchisePresentation(html: string): string {
  return html
    .replace(
      '<h1 itemprop="headline">Merchandise <em>owns</em> the ledger</h1>',
      '<h1 class="skin-title" itemprop="headline"><span class="deck">Merchandise</span> <span class="deck"><em>owns</em></span> <span class="deck">the ledger</span></h1>',
    )
    .replace("<h2>The cinema is the ad</h2>", '<h2 class="skin-accounts">The cinema is the ad</h2>')
    .replace("<h2>Pokémon, then everyone</h2>", '<h2 class="skin-running">Pokémon, then everyone</h2>')
    .replace(
      '<h2>Five parents, 58%</h2>\n<p class="big fade">58.2%</p>',
      '<h2 class="skin-balance">Five parents, 58%</h2>\n<p class="big fade skin-balance">58.2%</p>',
    )
    .replace("<h2>The flip</h2>", '<h2 class="skin-flip">The flip</h2>')
    .replace(
      '<h2 class="skin-flip">The flip</h2>\n<figure>',
      '<h2 class="skin-flip">The flip</h2>\n<figure class="skin-flip-fig">',
    )
    .replace(
      '<h2>A sequel chart</h2>\n<p class="big fade">9 of 10</p>',
      '<h2 class="skin-tally">A sequel chart</h2>\n<p class="big fade skin-tally">9 of 10</p>',
    )
    .replace("<h2>For a buyer</h2>", '<h2 class="skin-memo">For a buyer</h2>');
}

function splitAtEnd(html: string): { article: string; publishedInner: string } {
  const endAt = html.lastIndexOf('<p class="end">');
  if (endAt < 0) return { article: html, publishedInner: "" };
  const article = html.slice(0, endAt);
  const tail = html.slice(endAt);
  const list = tail.match(/<ol class="src">([\s\S]*?)<\/ol>/);
  return { article, publishedInner: list ? list[1] : "" };
}

export function decorateIssueHtml(issue: MagIssue, html: string): string {
  let body = html.replace(/<p>(<strong>What it means\.)/g, '<p class="means">$1');
  body = body.replace(/<img class="hero"/g, '<span class="hero-frame"><img class="hero"');
  body = body.replace(/<span class="hero-frame"><img class="hero"([^>]*)>/g, '<span class="hero-frame"><img class="hero"$1></span>');
  if (issue.slug === "franchise") body = franchisePresentation(body);
  if (issue.slug === "billboard") body = billboardPresentation(body);
  if (issue.slug === "streaming") body = streamingPresentation(body);
  if (issue.slug === "youtube") body = youtubePresentation(body);
  const { article, publishedInner } = splitAtEnd(body);
  const stamp =
    issue.slug === "franchise"
      ? '<p class="audit-stamp" aria-hidden="true">Audited · Oct 2026</p>'
      : "";
  const collect =
    issue.slug === "franchise"
      ? '<p class="collect-140" aria-hidden="true"><span></span><span></span><span></span> Collect all 140</p>'
      : "";
  const plate = usesSharedPlates(issue) ? plates() : "";
  const preface = `<div class="skin-top">${ornaments()}<div class="skin-top-row">${plate}<div class="skin-top-copy"><p class="skin-dateline">${esc(dateline(issue))}</p>${stamp}${collect}</div></div></div>`;
  return preface + article + closingSection(issue, publishedInner);
}
