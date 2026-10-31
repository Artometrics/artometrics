#!/usr/bin/env node
/**
 * Parse Artometrics markdown collections into JSON for the Expo app.
 * Also copies author/thumbnail images from src/images → public/images.
 */
import { mkdirSync, readdirSync, readFileSync, writeFileSync, cpSync, existsSync } from "node:fs";
import { writeSourcesCatalog } from "./lib/sources-catalog.mjs";
import { BLOG_SUBJECT_BY_SLUG } from "./blog-subjects.mjs";
import { join, dirname, extname, basename } from "node:path";
import { fileURLToPath } from "node:url";
import matter from "gray-matter";
import { marked } from "marked";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const OUT = join(ROOT, "src/generated");
const CONTENT = join(ROOT, "src/content");

mkdirSync(OUT, { recursive: true });

function listFiles(dir, exts = [".md", ".mdx"]) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((f) => exts.includes(extname(f)))
    .map((f) => join(dir, f));
}

function rewriteAssetUrl(url) {
  if (typeof url !== "string") return url;
  return url
    .replace(/^\/src\/images\//, "/images/")
    .replace(/^\.\.\/\.\.\/images\//, "/images/")
    .replace(/^\/src\//, "/");
}

function normalizeImageField(value) {
  if (!value) return value;
  if (typeof value === "string") return rewriteAssetUrl(value);
  if (typeof value === "object" && value.url) {
    return { ...value, url: rewriteAssetUrl(value.url) };
  }
  return value;
}

function copyDirIfExists(from, to) {
  if (!existsSync(from)) return;
  mkdirSync(dirname(to), { recursive: true });
  cpSync(from, to, { recursive: true });
}

// Expose author/thumbnail assets at public/images/*
copyDirIfExists(join(ROOT, "src/images/authors"), join(ROOT, "public/images/authors"));
copyDirIfExists(join(ROOT, "src/images/thumbnails"), join(ROOT, "public/images/thumbnails"));
copyDirIfExists(join(ROOT, "src/images/about"), join(ROOT, "public/images/about"));

const DOMAINS = new Set([
  "arts",
  "sports",
  "science",
  "humanities",
  "civics",
  "culture",
]);
const SUBDOMAINS = new Set([
  "design",
  "music",
  "film",
  "theater",
  "architecture",
  "fashion",
  "language",
  "football",
  "basketball",
  "baseball",
  "soccer",
  "hockey",
  "golf",
  "tennis",
  "fighting",
  "gaming",
  "motorsports",
  "chemistry",
  "physics",
  "biology",
  "astronomy",
  "geology",
  "math",
  "medicine",
  "engineering",
  "tech",
  "history",
  "philosophy",
  "religion",
  "psychology",
  "sociology",
  "anthropology",
  "economics",
  "business",
  "politics",
  "law",
  "education",
  "communication",
  "travel",
  "food",
  "leisure",
  "environment",
  "wellness",
]);
const SUBDOMAIN_PARENT = {
  design: "arts",
  music: "arts",
  film: "arts",
  theater: "arts",
  architecture: "arts",
  fashion: "arts",
  language: "arts",
  football: "sports",
  basketball: "sports",
  baseball: "sports",
  soccer: "sports",
  hockey: "sports",
  golf: "sports",
  tennis: "sports",
  fighting: "sports",
  gaming: "sports",
  motorsports: "sports",
  chemistry: "science",
  physics: "science",
  biology: "science",
  astronomy: "science",
  geology: "science",
  math: "science",
  medicine: "science",
  engineering: "science",
  tech: "science",
  history: "humanities",
  philosophy: "humanities",
  religion: "humanities",
  psychology: "humanities",
  sociology: "humanities",
  anthropology: "humanities",
  economics: "civics",
  business: "civics",
  politics: "civics",
  law: "civics",
  education: "civics",
  communication: "civics",
  travel: "culture",
  food: "culture",
  leisure: "culture",
  environment: "culture",
  wellness: "culture",
};
const LEGACY_TO_DOMAIN = {
  sports: "sports",
  "movies-tv": "arts",
  music: "arts",
  culture: "culture",
  galleries: "arts",
  "cities-travel": "culture",
  games: "sports",
  business: "civics",
  books: "arts",
  tech: "science",
  atlas: "culture",
  history: "humanities",
  persona: "humanities",
  power: "civics",
};

function resolveTaxonomy(slug, title, rawTags = []) {
  let subdomain = rawTags.find((t) => SUBDOMAINS.has(t)) || null;
  let domain =
    rawTags.find((t) => DOMAINS.has(t)) ||
    (subdomain ? SUBDOMAIN_PARENT[subdomain] : null) ||
    null;
  if (!domain) {
    for (const t of rawTags) {
      if (LEGACY_TO_DOMAIN[t]) {
        domain = LEGACY_TO_DOMAIN[t];
        break;
      }
    }
  }
  if (!domain || !subdomain) {
    // Lightweight fallback aligned with data/sections inferTaxonomy
    const hay = `${slug} ${title} ${rawTags.join(" ")}`.toLowerCase();
    const rules = [
      [/\b(yankees|dodgers|padres|giant|mlb|baseball)\b/, "sports", "baseball"],
      [/\b(celtics|lakers|warrior|nba|basketball)\b/, "sports", "basketball"],
      [/\b(cowboys|patriots|nfl|super.?bowl|football)\b/, "sports", "football"],
      [/\b(steam|pokemon|video.?game|gaming|board.?game)\b/, "sports", "gaming"],
      [/\b(anime|film|movie|oscar|emmy|horror|franchise|netflix|pixar|streaming|imdb|tv)\b/, "arts", "film"],
      [/\b(broadway|musical|theater)\b/, "arts", "theater"],
      [/\b(music|grammy|album|song|billboard|radio|musicbrainz)\b/, "arts", "music"],
      [/\b(lcsh|sherlock|novel|book|language|glottolog)\b/, "arts", "language"],
      [/\b(museum|heritage|architecture)\b/, "arts", "architecture"],
      [/\b(readmit|hospital|life.?expect|medicine)\b/, "science", "medicine"],
      [/\b(web.?page|medium|tech)\b/, "science", "tech"],
      [/\b(caesar|emperor|roman|imperial|pantheon|history)\b/, "humanities", "history"],
      [/\b(voter|politics|un.?vote)\b/, "civics", "politics"],
      [/\b(tuition|college|school|education)\b/, "civics", "education"],
      [/\b(ceo|export|wealth|economics|business)\b/, "civics", "economics"],
      [/\b(pizza|ramen|wine|beer|coffee|food|calorie|alcohol)\b/, "culture", "food"],
      [/\b(airline|park|travel|city|cities)\b/, "culture", "travel"],
      [/\b(plastic|hurricane|environment)\b/, "culture", "environment"],
      [/\b(exercise|wellness)\b/, "culture", "wellness"],
    ];
    for (const [re, d, s] of rules) {
      if (re.test(hay)) {
        domain = domain || d;
        subdomain = subdomain || s;
        break;
      }
    }
  }
  domain = domain || "culture";
  subdomain = subdomain || "leisure";
  if (SUBDOMAIN_PARENT[subdomain] && SUBDOMAIN_PARENT[subdomain] !== domain) {
    domain = SUBDOMAIN_PARENT[subdomain];
  }
  return { domain, subdomain, tags: [domain, subdomain] };
}

const blog = listFiles(join(CONTENT, "blog")).map((file) => {
  const raw = readFileSync(file, "utf8");
  const { data, content } = matter(raw);
  const id = basename(file, extname(file));
  const slug = data.slug ?? id;
  const rawTags = Array.isArray(data.tags) ? data.tags : [];
  const { domain, subdomain, tags } = resolveTaxonomy(slug, data.title ?? "", rawTags);
  const subjectRaw =
    typeof data.subject === "string" && data.subject.trim()
      ? data.subject.trim()
      : BLOG_SUBJECT_BY_SLUG[slug] ?? null;
  const keyPoints = Array.isArray(data.keyPoints)
    ? data.keyPoints.map(String).filter(Boolean)
    : [];
  const faq = Array.isArray(data.faq)
    ? data.faq
        .map((item) => ({
          question: String(item?.question ?? "").trim(),
          answer: String(item?.answer ?? "").trim(),
        }))
        .filter((item) => item.question && item.answer)
    : [];
  return {
    id,
    title: data.title,
    slug,
    pubDate: data.pubDate ? new Date(data.pubDate).toISOString() : null,
    description: data.description ?? "",
    heroImage: rewriteAssetUrl(data.heroImage ?? ""),
    tags,
    subject: subjectRaw,
    section: domain,
    subdomain,
    channels: [domain],
    author: data.author ?? null,
    draft: Boolean(data.draft),
    tldr: typeof data.tldr === "string" ? data.tldr.trim() : null,
    keyPoints,
    faq,
    audioSrc: data.audioSrc ? rewriteAssetUrl(String(data.audioSrc)) : null,
    body: content.trim(),
    bodyFormat: "html",
  };
});

const podcast = listFiles(join(CONTENT, "podcast")).map((file) => {
  const raw = readFileSync(file, "utf8");
  const { data, content } = matter(raw);
  const id = basename(file, extname(file));
  const isLocked = Boolean(data.isLocked);
  return {
    id,
    title: data.title,
    pubDate: data.pubDate ? new Date(data.pubDate).toISOString() : null,
    description: data.description ?? "",
    author: data.author ?? "",
    image: normalizeImageField(data.image),
    guestAvatar: normalizeImageField(data.guestAvatar),
    episodeNumber: data.episodeNumber ?? null,
    duration: data.duration ?? null,
    audioSrc: data.audioSrc ?? null,
    tags: data.tags ?? [],
    isRecent: Boolean(data.isRecent),
    isPopular: Boolean(data.isPopular),
    isLocked,
    // Locked transcripts ship via Supabase + /api/member-episode, not the static JSON.
    body: isLocked ? "" : marked.parse(content.trim(), { async: false }),
    bodyFormat: "html",
  };
});

const authors = listFiles(join(CONTENT, "authors"), [".md"]).map((file) => {
  const raw = readFileSync(file, "utf8");
  const { data, content } = matter(raw);
  const id = basename(file, extname(file));
  return {
    id,
    name: data.name,
    role: data.role ?? null,
    bio: data.bio ?? content.trim() ?? null,
    image: normalizeImageField(data.image),
    socials: data.socials ?? null,
  };
});

const legal = listFiles(join(CONTENT, "legal"), [".md"]).map((file) => {
  const raw = readFileSync(file, "utf8");
  const { data, content } = matter(raw);
  const id = basename(file, extname(file));
  return {
    id,
    page: data.page ?? id,
    pubDate: data.pubDate ? new Date(data.pubDate).toISOString() : null,
    body: marked.parse(content.trim(), { async: false }),
    bodyFormat: "html",
  };
});

writeFileSync(join(OUT, "blog.json"), JSON.stringify(blog, null, 2));
writeFileSync(join(OUT, "podcast.json"), JSON.stringify(podcast, null, 2));
writeFileSync(join(OUT, "authors.json"), JSON.stringify(authors, null, 2));
writeFileSync(join(OUT, "legal.json"), JSON.stringify(legal, null, 2));

const index = {
  blog: blog.length,
  podcast: podcast.length,
  authors: authors.length,
  legal: legal.length,
  generatedAt: new Date().toISOString(),
};
writeFileSync(join(OUT, "index.json"), JSON.stringify(index, null, 2));

const calendarPath = join(ROOT, "docs/content-os/content-calendar.csv");
function parseCalendarCsv(raw) {
  const lines = raw.trim().split(/\r?\n/).slice(1);
  return lines
    .map((line) => {
      const cols = [];
      let cur = "";
      let inQuotes = false;
      for (let i = 0; i < line.length; i++) {
        const ch = line[i];
        if (ch === '"') {
          inQuotes = !inQuotes;
          continue;
        }
        if (ch === "," && !inQuotes) {
          cols.push(cur);
          cur = "";
          continue;
        }
        cur += ch;
      }
      cols.push(cur);
      if (cols.length < 3) return null;
      return {
        releaseFriday: cols[0],
        slug: cols[1],
        title: cols[2].replace(/^'|'$/g, ""),
        desk: cols[3] ?? "",
        subdomain: cols[4] ?? "",
      };
    })
    .filter(Boolean);
}

if (existsSync(calendarPath)) {
  const calendar = parseCalendarCsv(readFileSync(calendarPath, "utf8"));
  writeFileSync(join(OUT, "content-calendar.json"), JSON.stringify(calendar, null, 2));
}

writeSourcesCatalog(ROOT);

console.log(
  `Content built → src/generated/ (${blog.length} blog, ${podcast.length} podcast, ${authors.length} authors, ${legal.length} legal)`,
);
