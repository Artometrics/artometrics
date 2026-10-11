#!/usr/bin/env node
/**
 * Render an Artometrics magazine edition from an article .qmd.
 *
 *   npm run magazine -- anime
 *
 * Writes articles/<slug>/magazine/<slug>-issue-01.pdf and .html.
 * The PDF is Typst. The HTML is the same .qmd paginated with paged.js.
 */

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const slug = process.argv[2];

if (!slug || slug.startsWith("-")) {
  console.error("Usage: npm run magazine -- <slug>");
  process.exit(1);
}

const articleDir = path.join(ROOT, "articles", slug);
const qmd = path.join(articleDir, `${slug}.qmd`);
const extension = path.join(ROOT, "articles", "_extensions", "artometrics-magazine");
const linkDir = path.join(articleDir, "_extensions");
const link = path.join(linkDir, "artometrics-magazine");
const outDir = path.join(articleDir, "magazine");

if (!fs.existsSync(qmd)) {
  console.error(`No article source at ${qmd}`);
  process.exit(1);
}
if (!fs.existsSync(path.join(extension, "_extension.yml"))) {
  console.error(`Missing extension at ${extension}`);
  process.exit(1);
}

fs.mkdirSync(linkDir, { recursive: true });
if (!fs.existsSync(link)) {
  fs.symlinkSync(path.relative(linkDir, extension), link);
}

const blogPath = path.join(ROOT, "src", "content", "blog", `${slug}.md`);
if (fs.existsSync(blogPath)) {
  const missing = missingNumbers(fs.readFileSync(blogPath, "utf8"), fs.readFileSync(qmd, "utf8"));
  if (missing.length) {
    console.error(`Magazine source is missing ${missing.length} figures from the published report:`);
    for (const token of missing.slice(0, 25)) console.error("  " + token);
    process.exit(1);
  }
  console.log("Number check: every published figure is in the .qmd");
}

fs.mkdirSync(outDir, { recursive: true });
const env = {
  ...process.env,
  TYPST_FONT_PATHS: path.join(extension, "fonts"),
};

function render(format, filename) {
  execFileSync(
    "quarto",
    ["render", path.basename(qmd), "--to", format, "--output-dir", "magazine", "--output", filename],
    { cwd: articleDir, env, stdio: "inherit" },
  );
}

render("artometrics-magazine-typst", `${slug}-issue-01.pdf`);
const polyfillSrc = path.join(extension, "paged.polyfill.js");
const polyfillBesideSource = path.join(articleDir, "paged.polyfill.js");
fs.copyFileSync(polyfillSrc, polyfillBesideSource);
try {
  render("artometrics-magazine-html", `${slug}-issue-01.html`);
} finally {
  fs.rmSync(polyfillBesideSource, { force: true });
}
fs.copyFileSync(polyfillSrc, path.join(outDir, "paged.polyfill.js"));

const pdf = path.join(outDir, `${slug}-issue-01.pdf`);
const info = execFileSync("pdfinfo", [pdf], { encoding: "utf8" });
const pages = info.match(/Pages:\s+(\d+)/)?.[1] ?? "?";
const fonts = execFileSync("pdffonts", [pdf], { encoding: "utf8" });
console.log(fonts);
console.log(`PDF ${pdf}`);
console.log(`Pages ${pages}`);

function visibleText(raw) {
  return raw
    .replace(/<script[\s\S]*?<\/script>/gi, " ")
    .replace(/<style[\s\S]*?<\/style>/gi, " ")
    .replace(/\sstyle="[^"]*"/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&nbsp;/g, " ")
    .replace(/&#39;/g, "'")
    .replace(/&quot;/g, '"');
}

function numberTokens(text) {
  const tokens = text.match(/\d[\d,]*(?:\.\d+)?%?/g) || [];
  return [...new Set(tokens)];
}

function publishedProse(blog) {
  const match = blog.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) return visibleText(blog);
  const fm = match[1];
  const keep = [];
  for (const key of ["title", "description", "tldr", "keyPoints"]) {
    const block = fm.match(new RegExp(`^${key}:\\s*>-\\s*\\n([\\s\\S]*?)(?=\\n[A-Za-z0-9_]+:|\\n---|$)`, "m"));
    if (block) keep.push(block[1]);
    const list = fm.match(new RegExp(`^${key}:\\s*\\n((?:\\s+-\\s+.*\\n)*)`, "m"));
    if (list) keep.push(list[1]);
    const line = fm.match(new RegExp(`^${key}:\\s*"([^"]*)"`, "m"));
    if (line) keep.push(line[1]);
  }
  return visibleText(keep.join("\n") + "\n" + match[2]);
}

function missingNumbers(blog, qmd) {
  const haystack = visibleText(qmd).replace(/&amp;/g, "&");
  return numberTokens(publishedProse(blog)).filter((token) => !haystack.includes(token));
}
