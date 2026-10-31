/**
 * Build the Sources page catalog from magazine/issues.json.
 *
 * Updated through, in order:
 * 1. Data coverage end, when a citation states one.
 * 2. Otherwise the latest citation date.
 * 3. Otherwise "not yet checked".
 * Editorial indexes say "editorial index" instead of a date.
 *
 * Data-fix issues nest under the parent slug (`anime-data-fix` → `anime`).
 * Dataset links are included only when data/datasets.ts already lists a pack
 * whose relatedReports include the issue slug.
 */
import { readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

export const TOPIC_ORDER = [
  { id: "arts", title: "Arts", description: "Design, music, film, theater, architecture, fashion, and language." },
  { id: "sports", title: "Sports", description: "Football, basketball, baseball, soccer, and the wider field of play." },
  { id: "science", title: "Science", description: "Chemistry through tech — the measurable world." },
  { id: "humanities", title: "Humanities", description: "History, philosophy, religion, and the study of people." },
  { id: "civics", title: "Civics", description: "Economics, business, politics, law, education, and communication." },
  { id: "culture", title: "Culture", description: "Travel, food, leisure, environment, and wellness." },
];

const MONTHS = {
  january: 1,
  february: 2,
  march: 3,
  april: 4,
  may: 5,
  june: 6,
  july: 7,
  august: 8,
  september: 9,
  october: 10,
  november: 11,
  december: 12,
};

const MONTH_NAME = [
  "",
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const MONTH_PATTERN = `(?:${Object.keys(MONTHS)
  .filter((name) => name.length > 3 || name === "may")
  .join("|")})`;

function stamp(year, month = 0, day = 0) {
  const y = Number(year);
  const m = Number(month) || 0;
  const d = Number(day) || 0;
  if (!Number.isInteger(y) || y < 1500 || y > 2100) return null;
  if (m && (m < 1 || m > 12)) return null;
  if (d && (d < 1 || d > 31)) return null;
  return { y, m, d, rank: y * 10000 + m * 100 + d };
}

function maxStamp(stamps) {
  return stamps.reduce((best, next) => (!best || next.rank > best.rank ? next : best), null);
}

export function formatStamp(value) {
  if (!value) return "";
  if (value.m && value.d) return `${MONTH_NAME[value.m]} ${value.d}, ${value.y}`;
  if (value.m) return `${MONTH_NAME[value.m]} ${value.y}`;
  return String(value.y);
}

function monthNumber(name) {
  return MONTHS[String(name || "").toLowerCase()] || 0;
}

function pushStamp(list, value) {
  if (value) list.push(value);
}

/** Dates that describe how far the underlying data runs. */
export function coverageStamps(line) {
  const out = [];
  const text = String(line || "");

  for (const match of text.matchAll(
    new RegExp(`snapshot\\s+((?:19|20)\\d{2})-(\\d{2})-(\\d{2})`, "gi"),
  )) {
    pushStamp(out, stamp(match[1], match[2], match[3]));
  }

  for (const match of text.matchAll(
    new RegExp(
      `weeks ending\\s+(?:${MONTH_PATTERN}\\s+\\d{1,2}\\s*[–—-]\\s*)?(${MONTH_PATTERN})\\s+(\\d{1,2}),\\s*((?:19|20)\\d{2})`,
      "gi",
    ),
  )) {
    pushStamp(out, stamp(match[3], monthNumber(match[1]), match[2]));
  }

  for (const match of text.matchAll(
    new RegExp(`\\bthrough\\s+(${MONTH_PATTERN})\\s+(\\d{1,2}),\\s*((?:19|20)\\d{2})`, "gi"),
  )) {
    pushStamp(out, stamp(match[3], monthNumber(match[1]), match[2]));
  }

  for (const match of text.matchAll(
    new RegExp(`\\bthrough\\s+(${MONTH_PATTERN})\\s+((?:19|20)\\d{2})\\b`, "gi"),
  )) {
    pushStamp(out, stamp(match[2], monthNumber(match[1])));
  }

  for (const match of text.matchAll(/\bthrough\s+((?:19|20)\d{2})\b/gi)) {
    pushStamp(out, stamp(match[1]));
  }

  for (const match of text.matchAll(
    new RegExp(
      `\\bspanning\\b[^.]{0,48}?((?:16|17|18|19|20)\\d{2})\\s*(?:[–—-]|to)\\s*((?:16|17|18|19|20)\\d{2})`,
      "gi",
    ),
  )) {
    pushStamp(out, stamp(match[2]));
  }

  for (const match of text.matchAll(
    /\bFY\s*((?:19|20)\d{2})\s*[–—-]\s*FY\s*((?:19|20)\d{2})\b/gi,
  )) {
    pushStamp(out, stamp(match[2]));
  }

  const coverageContext =
    /\b(database|dataset|tidytuesday|snapshot|extract|catalog|catalogue|ledger|census|coverage|figures|revenues)\b/i.test(
      text,
    );
  if (coverageContext) {
    for (const match of text.matchAll(
      /\b((?:1[6-9]|20)\d{2})\s*[–—-]\s*((?:1[6-9]|20)\d{2})\b/g,
    )) {
      pushStamp(out, stamp(match[2]));
    }
    for (const match of text.matchAll(
      /\b((?:1[6-9]|20)\d{2})\s+to\s+((?:1[6-9]|20)\d{2})\b/gi,
    )) {
      pushStamp(out, stamp(match[2]));
    }
    const withoutAccess = text
      .replace(
        new RegExp(
          `\\b(?:accessed|retrieved|file read)\\s+(?:${MONTH_PATTERN}\\s+\\d{1,2},\\s*)?(?:19|20)\\d{2}(?:-\\d{2}-\\d{2})?`,
          "gi",
        ),
        " ",
      );
    for (const match of withoutAccess.matchAll(/\b((?:19|20)\d{2})-(\d{2})-(\d{2})\b/g)) {
      pushStamp(out, stamp(match[1], match[2], match[3]));
    }
  }

  const season = text.match(
    /\b((?:19|20)\d{2})\s+(?:[A-Z][\w.'’-]*\s+){1,6}statistics\b/,
  );
  if (season) pushStamp(out, stamp(season[1]));

  if (/\b(api|database|dataset|catalog|catalogue|snapshot)\b/i.test(text)) {
    for (const match of text.matchAll(
      /\baccessed\s+((?:19|20)\d{2})-(\d{2})-(\d{2})\b/gi,
    )) {
      pushStamp(out, stamp(match[1], match[2], match[3]));
    }
    for (const match of text.matchAll(
      new RegExp(
        `\\baccessed\\s+(${MONTH_PATTERN})\\s+(\\d{1,2}),\\s*((?:19|20)\\d{2})`,
        "gi",
      ),
    )) {
      pushStamp(out, stamp(match[3], monthNumber(match[1]), match[2]));
    }
  }

  const gauge = text.match(
    new RegExp(
      `\\bgauge\\b[^.\\n]{0,48}?\\b(${MONTH_PATTERN})\\s+((?:19|20)\\d{2})\\b`,
      "i",
    ),
  );
  if (gauge) pushStamp(out, stamp(gauge[2], monthNumber(gauge[1])));

  return out;
}

/** Publication, access, and release dates on a citation line. */
export function citationStamps(line) {
  const text = String(line || "").trim();
  if (/^Related Artometrics report:/i.test(text)) return [];
  const out = [];

  for (const match of text.matchAll(/\b((?:19|20)\d{2})-(\d{2})-(\d{2})\b/g)) {
    pushStamp(out, stamp(match[1], match[2], match[3]));
  }
  for (const match of text.matchAll(
    new RegExp(`\\b(${MONTH_PATTERN})\\s+(\\d{1,2}),\\s*((?:19|20)\\d{2})\\b`, "gi"),
  )) {
    pushStamp(out, stamp(match[3], monthNumber(match[1]), match[2]));
  }
  for (const match of text.matchAll(
    new RegExp(`\\b(${MONTH_PATTERN})\\s+((?:19|20)\\d{2})\\b`, "gi"),
  )) {
    pushStamp(out, stamp(match[2], monthNumber(match[1])));
  }
  for (const match of text.matchAll(/\(((?:19|20)\d{2})(?:,\s*[A-Za-z]+)?\)/g)) {
    pushStamp(out, stamp(match[1]));
  }
  for (const match of text.matchAll(/\bpublished(?:\s+online)?\s+((?:19|20)\d{2})\b/gi)) {
    pushStamp(out, stamp(match[1]));
  }
  return out;
}

function plainSectionText(issue) {
  const chunks = [];
  if (issue.dek) chunks.push(issue.dek);
  for (const section of issue.sections || []) {
    if (section.h) chunks.push(section.h);
    for (const paragraph of section.ps || []) {
      chunks.push(String(paragraph).replace(/<[^>]+>/g, " "));
    }
  }
  return chunks.join("\n");
}

export function isEditorialIndex(issue) {
  const chunks = [plainSectionText(issue)];
  for (const source of issue.src || []) {
    const text = String(source.text || "").trim();
    if (/^Related Artometrics report:/i.test(text)) continue;
    chunks.push(text);
  }
  return /\beditorial indices?\b/i.test(chunks.join("\n"));
}

export function updatedThrough(issue) {
  if (isEditorialIndex(issue)) {
    return {
      kind: "editorial",
      label: "Updated through: editorial index",
    };
  }
  const lines = (issue.src || []).map((source) => source.text || "");
  const coverage = maxStamp(lines.flatMap((line) => coverageStamps(line)));
  if (coverage) {
    return { kind: "coverage", label: `Updated through ${formatStamp(coverage)}` };
  }
  const cited = maxStamp(lines.flatMap((line) => citationStamps(line)));
  if (cited) {
    return { kind: "citation", label: `Updated through ${formatStamp(cited)}` };
  }
  return { kind: "unchecked", label: "Updated through: not yet checked" };
}

export function citationHref(href) {
  if (typeof href !== "string") return null;
  const trimmed = href.trim();
  if (/^https?:\/\//i.test(trimmed)) return trimmed;
  return null;
}

export function isDataFix(issue) {
  return issue.isFix === true || /-data-fix$/.test(issue.slug || "");
}

export function parentSlug(issue) {
  return String(issue.slug || "").replace(/-data-fix$/, "");
}

export function topicId(tags) {
  for (const tag of tags || []) {
    if (TOPIC_ORDER.some((topic) => topic.id === tag)) return tag;
  }
  return "culture";
}

export function parseDatasetPacks(source) {
  const packs = [];
  const body = String(source);
  const start = body.indexOf("export const DATASET_PACKS");
  const slice = start >= 0 ? body.slice(start) : body;
  for (const block of slice.split(/\n  \{/)) {
    const id = block.match(/id:\s*"([^"]+)"/)?.[1];
    const title = block.match(/title:\s*"([^"]+)"/)?.[1];
    const related = block.match(/relatedReports:\s*\[([\s\S]*?)\]/)?.[1] || "";
    if (!id || !title) continue;
    const slugs = [...related.matchAll(/"([^"]+)"/g)].map((match) => match[1]);
    packs.push({ id, title, slugs });
  }
  return packs;
}

function datasetsFor(slug, packs) {
  return packs
    .filter((pack) => pack.slugs.includes(slug))
    .map((pack) => ({
      id: pack.id,
      title: pack.title,
      href: `/datasets/${pack.id}`,
    }));
}

function entryFromIssue(issue, packs) {
  const through = updatedThrough(issue);
  return {
    slug: issue.slug,
    title: issue.title,
    kicker: issue.kicker || "",
    href: `/${issue.slug}`,
    updatedThrough: through.label,
    updatedThroughKind: through.kind,
    datasets: datasetsFor(issue.slug, packs),
    citations: (issue.src || []).map((source) => ({
      text: String(source.text || "").replace(/\s+/g, " ").trim(),
      href: citationHref(source.href),
    })),
  };
}

export function buildSourcesCatalog(issues, packs) {
  const parents = new Map();
  const fixes = new Map();
  for (const issue of issues) {
    if (isDataFix(issue)) {
      const parent = parentSlug(issue);
      const list = fixes.get(parent) || [];
      list.push(issue);
      fixes.set(parent, list);
      continue;
    }
    parents.set(issue.slug, issue);
  }

  const grouped = new Map(TOPIC_ORDER.map((topic) => [topic.id, []]));
  for (const issue of parents.values()) {
    const topic = topicId(issue.tags);
    const entry = entryFromIssue(issue, packs);
    const notes = (fixes.get(issue.slug) || [])
      .slice()
      .sort((a, b) => a.slug.localeCompare(b.slug))
      .map((note) => entryFromIssue(note, packs));
    grouped.get(topic).push({ ...entry, fixes: notes });
  }

  const topics = TOPIC_ORDER.map((topic) => ({
    id: topic.id,
    title: topic.title,
    description: topic.description,
    href: `/topics/${topic.id}`,
    issues: grouped
      .get(topic.id)
      .slice()
      .sort((a, b) => a.title.localeCompare(b.title, "en", { numeric: true })),
  })).filter((topic) => topic.issues.length);

  const orphanFixes = [];
  for (const [parent, notes] of fixes) {
    if (!parents.has(parent)) orphanFixes.push(...notes.map((note) => note.slug));
  }

  return {
    generatedFrom: "magazine/issues.json",
    topics,
    orphanFixes,
  };
}

export function loadSourcesInputs(root) {
  const issues = JSON.parse(readFileSync(join(root, "magazine/issues.json"), "utf8"));
  const packs = parseDatasetPacks(readFileSync(join(root, "data/datasets.ts"), "utf8"));
  return { issues, packs };
}

export function writeSourcesCatalog(root) {
  const { issues, packs } = loadSourcesInputs(root);
  const catalog = buildSourcesCatalog(issues, packs);
  const out = join(root, "src/generated/sources.json");
  writeFileSync(out, `${JSON.stringify(catalog, null, 2)}\n`);
  const reports = catalog.topics.reduce((sum, topic) => sum + topic.issues.length, 0);
  console.log(
    `Wrote src/generated/sources.json (${reports} reports, ${catalog.topics.length} topics)`,
  );
  return catalog;
}
