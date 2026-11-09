import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { INCOMING_COVER, INCOMING_SQUARE } from "../lib/article-assets.mjs";

const root = join(dirname(fileURLToPath(import.meta.url)), "..");
const posts = JSON.parse(readFileSync(join(root, "src/generated/blog.json"), "utf8"));
const issues = JSON.parse(readFileSync(join(root, "magazine/issues.json"), "utf8"));
const hosting = JSON.parse(readFileSync(join(root, "firebase.json"), "utf8"));
const domains = new Set(["arts", "sports", "science", "humanities", "civics", "culture"]);

function sectionOf(tags) {
  return (tags || []).find((tag) => domains.has(tag)) || "";
}
function subOf(tags) {
  return (tags || []).find((tag) => !domains.has(tag)) || "";
}
function has(slug, name) {
  return existsSync(join(root, "public/images/content/articles", slug, name));
}

const aliases = new Map();
for (const rule of hosting.hosting.redirects) {
  const dest = rule.destination;
  if (!dest.startsWith("/") || dest.includes("*") || dest.startsWith("/topics")) continue;
  const slug = dest.slice(1);
  if (!slug || slug.includes("/")) continue;
  const list = aliases.get(slug) || [];
  list.push(rule.source);
  aliases.set(slug, list);
}

const seen = new Set();
const rows = [];
for (const post of posts) {
  if (post.draft || !post.pubDate || domains.has(post.slug) || seen.has(post.slug)) continue;
  seen.add(post.slug);
  const squareText = has(post.slug, "square-text.webp");
  const squareArt = has(post.slug, "square-art.webp");
  const plain = has(post.slug, INCOMING_SQUARE);
  const cover = has(post.slug, "cover.webp");
  const coverTitle = has(post.slug, INCOMING_COVER);
  let currentSquare = "";
  let currentSquareTextStatus = "missing";
  if (plain) {
    currentSquare = `/images/content/articles/${post.slug}/${INCOMING_SQUARE}`;
    currentSquareTextStatus = "text-free";
  } else if (squareText) {
    currentSquare = `/images/content/articles/${post.slug}/square-text.webp`;
    currentSquareTextStatus = "text-bearing";
  } else if (post.heroImage) {
    currentSquare = post.heroImage;
    currentSquareTextStatus = "unknown";
  }
  rows.push({
    slug: post.slug,
    title: post.title,
    topic: sectionOf(post.tags),
    subdomain: subOf(post.tags),
    url: `https://artometrics.com/${post.slug}`,
    aliases: (aliases.get(post.slug) || []).join(" "),
    currentSquare,
    currentSquareTextStatus,
    priorSquareArt: squareArt ? `/images/content/articles/${post.slug}/square-art.webp` : "",
    priorSquareArtNote: squareArt
      ? "Prior 14-pack square-art file. Not the new sitewide text-free square, and not used as one unless square-plain.webp is delivered."
      : "",
    currentCover: coverTitle
      ? `/images/content/articles/${post.slug}/${INCOMING_COVER}`
      : cover
        ? `/images/content/articles/${post.slug}/cover.webp`
        : "",
    currentCoverTextStatus: cover || coverTitle ? "text-bearing" : "missing",
    hero: post.heroImage || "",
    incomingSquare: `/images/content/articles/${post.slug}/${INCOMING_SQUARE}`,
    incomingCover: `/images/content/articles/${post.slug}/${INCOMING_COVER}`,
    incomingSquarePresent: plain,
    incomingCoverPresent: coverTitle,
  });
}
rows.sort((a, b) => a.topic.localeCompare(b.topic) || a.slug.localeCompare(b.slug));

const blogSlugs = new Set(rows.map((row) => row.slug));
const magazineOnly = issues
  .filter((issue) => !blogSlugs.has(issue.slug))
  .map((issue) => issue.slug)
  .sort();

const payload = {
  generatedFrom: "src/generated/blog.json",
  canonicalCount: rows.length,
  note: "currentSquareTextStatus unknown means the file is a hero or other legacy image and is not certified text-free. text-bearing means baked lettering. text-free is only square-plain.webp.",
  incomingSquareName: INCOMING_SQUARE,
  incomingCoverName: INCOMING_COVER,
  magazineIssueSlugsNotInBlog: magazineOnly,
  articles: rows,
};

const docs = join(root, "docs/report-assets");
mkdirSync(docs, { recursive: true });
writeFileSync(join(docs, "article-asset-inventory.json"), JSON.stringify(payload, null, 2));
const header = Object.keys(rows[0]);
const csv = [
  header.join(","),
  ...rows.map((row) => header.map((key) => `"${String(row[key] ?? "").replaceAll('"', '""')}"`).join(",")),
].join("\n");
writeFileSync(join(docs, "article-asset-inventory.csv"), csv + "\n");
const artifact = "/opt/cursor/artifacts/article-inventory";
mkdirSync(artifact, { recursive: true });
writeFileSync(join(artifact, "article-asset-inventory.json"), JSON.stringify(payload, null, 2));
writeFileSync(join(artifact, "article-asset-inventory.csv"), csv + "\n");
console.log(`canonical ${rows.length}; magazine-only ${magazineOnly.length}`);
console.log(artifact);
