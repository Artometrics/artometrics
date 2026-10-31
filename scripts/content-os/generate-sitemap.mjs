#!/usr/bin/env node
/**
 * Static sitemap.xml for Expo web export.
 */
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "../..");
const SITE = "https://artometrics.com";

const blog = JSON.parse(readFileSync(join(ROOT, "src/generated/blog.json"), "utf8"))
  .filter((p) => !p.draft && p.pubDate);
const podcast = existsSync(join(ROOT, "src/generated/podcast.json"))
  ? JSON.parse(readFileSync(join(ROOT, "src/generated/podcast.json"), "utf8"))
  : [];
const legal = existsSync(join(ROOT, "src/generated/legal.json"))
  ? JSON.parse(readFileSync(join(ROOT, "src/generated/legal.json"), "utf8"))
  : [];
const authors = existsSync(join(ROOT, "src/generated/authors.json"))
  ? JSON.parse(readFileSync(join(ROOT, "src/generated/authors.json"), "utf8"))
  : [];

const SECTIONS = [
  "arts",
  "sports",
  "science",
  "humanities",
  "civics",
  "culture",
];

const editions = existsSync(join(ROOT, "public/data/meta/editions.json"))
  ? JSON.parse(readFileSync(join(ROOT, "public/data/meta/editions.json"), "utf8"))
  : [];

const staticPaths = [
  "/",
  "/blog",
  "/sources",
  "/topics",
  ...SECTIONS.map((s) => `/topics/${s}`),
  "/podcast",
  "/about",
  "/contact",
  "/pricing",
  "/studio",
  "/library",
  "/library/reference",
  "/editions",
  ...editions.map((e) => `/editions/${e.id}`),
  "/authors",
];

/** Strip trailing slash from path (except root "/") for canonical URLs. */
function canonPath(path) {
  return path === "/" ? "/" : path.replace(/\/$/, "");
}

function url(path, lastmod, priority = "0.6") {
  const loc = `${SITE}${canonPath(path)}`;
  return `  <url>
    <loc>${loc}</loc>
    ${lastmod ? `<lastmod>${lastmod.slice(0, 10)}</lastmod>` : ""}
    <priority>${priority}</priority>
  </url>`;
}

const parts = [
  `<?xml version="1.0" encoding="UTF-8"?>`,
  `<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">`,
  ...staticPaths.map((p) => url(p, null, p === "/" ? "1.0" : "0.7")),
  ...blog.map((p) => url(`/${p.slug.replace(/\/$/, "")}`, p.pubDate, "0.8")),
  ...podcast.map((e) => url(`/podcast/interviews/${e.id}`, e.pubDate, "0.6")),
  ...authors.map((a) => url(`/authors/${a.id}`, null, "0.4")),
  ...legal.map((l) => url(`/legal/${l.id}`, l.pubDate, "0.3")),
  `</urlset>`,
  "",
];

writeFileSync(join(ROOT, "public/sitemap.xml"), parts.join("\n"));
console.log(`Wrote public/sitemap.xml (${blog.length} reports)`);
