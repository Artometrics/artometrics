#!/usr/bin/env node
/**
 * Build a print-oriented PDF for one blog slug OR a special edition.
 *
 * Usage:
 *   npm run cos:pdf -- --slug readmitted
 *   npm run cos:pdf -- --edition music
 */
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import matter from "gray-matter";

const ROOT = process.cwd();
const args = process.argv.slice(2);
const slugIdx = args.indexOf("--slug");
const editionIdx = args.indexOf("--edition");
const slug = slugIdx >= 0 ? args[slugIdx + 1] : null;
const editionId = editionIdx >= 0 ? args[editionIdx + 1] : null;

if (!slug && !editionId) {
  console.error("Usage: npm run cos:pdf -- --slug <slug> | --edition <id>");
  process.exit(1);
}

function escapeHtml(s) {
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function which(bin) {
  const r = spawnSync("bash", ["-lc", `command -v ${bin}`], { encoding: "utf8" });
  return r.status === 0 ? r.stdout.trim() : "";
}

function chartsToImages(html, toFileUrl) {
  return html.replace(
    /<div class="art-chart-live"[^>]*data-fallback="([^"]+)"[^>]*>\s*<\/div>/g,
    (_match, src) => {
      const abs = path.join(ROOT, "public", src.replace(/^\//, ""));
      const url = toFileUrl ? `file://${abs}` : src;
      return `<img class="art-chart-fallback" src="${url}" alt="" />`;
    },
  );
}

function chapterHtml(s) {
  const mdPath = path.join(ROOT, "src/content/blog", `${s}.md`);
  if (!fs.existsSync(mdPath)) return null;
  const raw = fs.readFileSync(mdPath, "utf8");
  const { data, content } = matter(raw);
  if (data.draft) return null;
  return `<article class="edition-chapter"><h1>${escapeHtml(data.title || s)}</h1>${content}</article>`;
}

let title;
let outRel;
let bodyHtml;

if (slug) {
  const mdPath = path.join(ROOT, "src/content/blog", `${slug}.md`);
  if (!fs.existsSync(mdPath)) {
    console.error(`Missing ${mdPath}`);
    process.exit(1);
  }
  const raw = fs.readFileSync(mdPath, "utf8");
  const { data, content } = matter(raw);
  title = data.title || slug;
  outRel = `${slug}.pdf`;
  bodyHtml = chartsToImages(content, true);
  const description = data.description || "";
  const exportHtml = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>${escapeHtml(title)} — Artometrics</title>
<meta name="description" content="${escapeHtml(description)}" />
<link rel="stylesheet" href="/css/artometrics-article.css" />
<style>
  body { max-width: 720px; margin: 2rem auto; padding: 0 1.25rem; }
  img, .art-chart-fallback { max-width: 100%; height: auto; }
</style>
</head>
<body class="artometrics-article-body">
  <h1>${escapeHtml(title)}</h1>
  <p><em>${escapeHtml(description)}</em></p>
  ${chartsToImages(content, false)}
</body>
</html>`;
  fs.mkdirSync(path.join(ROOT, "public/exports"), { recursive: true });
  fs.writeFileSync(path.join(ROOT, "public/exports", `${slug}.html`), exportHtml, "utf8");
  console.log(`HTML → public/exports/${slug}.html`);
} else {
  const editionsPath = path.join(ROOT, "public/data/meta/editions.json");
  if (!fs.existsSync(editionsPath)) {
    console.error(`Missing ${editionsPath} — run npm run meta:editions`);
    process.exit(1);
  }
  const editions = JSON.parse(fs.readFileSync(editionsPath, "utf8"));
  const ed = editions.find((e) => e.id === editionId);
  if (!ed) {
    console.error(`Unknown edition: ${editionId}`);
    process.exit(1);
  }
  title = ed.title;
  outRel = path.join("editions", `${editionId}.pdf`);
  const parts = [];
  for (const s of ed.articleSlugs) {
    const html = chapterHtml(s);
    if (html) parts.push(html);
  }
  if (!parts.length) {
    console.error(`Edition ${editionId} has no live chapters`);
    process.exit(1);
  }
  bodyHtml = `<p class="edition-dek">${escapeHtml(ed.dek)}</p>` + parts.join("\n<hr/>\n");
}

const outDir = path.join(ROOT, "public/exports");
const outPdf = path.join(outDir, outRel);
const tmpHtml = path.join("/tmp", `artometrics-${editionId || slug}.html`);
fs.mkdirSync(path.dirname(outPdf), { recursive: true });

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>${escapeHtml(title)} — Artometrics</title>
<link rel="stylesheet" href="file://${path.join(ROOT, "public/css/artometrics-article.css")}" />
<style>
  body { max-width: 720px; margin: 2rem auto; padding: 0 1.25rem; }
  img, .art-chart-fallback { max-width: 100%; height: auto; }
  .art-chart-mode-switch, .art-chart-toolbar { display: none !important; }
  .edition-chapter { page-break-before: always; }
  .edition-chapter:first-of-type { page-break-before: auto; }
  @page { margin: 18mm 14mm; }
</style>
</head>
<body class="artometrics-article-body">
  <h1>${escapeHtml(title)}</h1>
  ${bodyHtml}
</body>
</html>`;

fs.writeFileSync(tmpHtml, html, "utf8");

let ok = false;
const pandoc = which("pandoc");
if (pandoc) {
  const r = spawnSync(
    pandoc,
    [tmpHtml, "-o", outPdf, "--pdf-engine=weasyprint"],
    { encoding: "utf8" },
  );
  if (r.status === 0 && fs.existsSync(outPdf)) ok = true;
}

if (!ok) {
  const weasy = which("weasyprint");
  if (weasy) {
    const r = spawnSync(weasy, [tmpHtml, outPdf], { encoding: "utf8" });
    if (r.status === 0 && fs.existsSync(outPdf)) ok = true;
  }
}

if (!ok) {
  console.error(
    "Could not build PDF. Install pandoc + weasyprint (npm run setup:pipeline) and retry.",
  );
  process.exit(1);
}

console.log(`PDF → ${path.relative(ROOT, outPdf)}`);
spawnSync("npm", ["run", "meta:editions"], { cwd: ROOT, stdio: "inherit" });
console.log("Tip: npm run cos:downloads  # refresh per-article download manifests");
