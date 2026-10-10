#!/usr/bin/env node
/**
 * Sync articles/<slug>/ assets into public/ for the Expo site.
 *
 * Usage:
 *   node scripts/sync-article.mjs --slug readmitted
 *   node scripts/sync-article.mjs --slug readmitted --render-readmitted
 */

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { execSync } from "node:child_process";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");

function arg(name) {
  const i = process.argv.indexOf(`--${name}`);
  return i === -1 ? null : process.argv[i + 1];
}

const slug = arg("slug");
const renderReadmitted = process.argv.includes("--render-readmitted");

if (!slug) {
  console.error("Usage: node scripts/sync-article.mjs --slug SLUG [--render-readmitted]");
  process.exit(1);
}

const ARTICLE = path.join(ROOT, "articles", slug);
const DATA_SRC = path.join(ARTICLE, "data");
const CHARTS_SRC = path.join(ARTICLE, "charts");

const PUBLIC_IMG = path.join(ROOT, "public/images/content/articles", slug, "charts");
const PUBLIC_HERO_DIR = path.join(ROOT, "public/images/content/articles", slug);
const PUBLIC_DATA = path.join(ROOT, "public/data/articles", slug);
const PUBLIC_CHARTS = path.join(PUBLIC_DATA, "charts");
const PUBLIC_CSV = path.join(PUBLIC_DATA, "data");

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function copyGlob(srcDir, destDir, pattern) {
  if (!fs.existsSync(srcDir)) return 0;
  ensureDir(destDir);
  const files = fs.readdirSync(srcDir).filter((name) => pattern.test(name));
  for (const name of files) {
    fs.copyFileSync(path.join(srcDir, name), path.join(destDir, name));
  }
  return files.length;
}

function copyDirFlat(srcDir, destDir, pattern) {
  if (!fs.existsSync(srcDir)) return 0;
  ensureDir(destDir);
  let n = 0;
  for (const name of fs.readdirSync(srcDir)) {
    const src = path.join(srcDir, name);
    if (!fs.statSync(src).isFile()) continue;
    if (pattern && !pattern.test(name)) continue;
    fs.copyFileSync(src, path.join(destDir, name));
    n++;
  }
  return n;
}

function copyHero() {
  let n = 0;
  for (const name of ["hero.jpg", "hero.png", "hero.webp"]) {
    const src = path.join(ARTICLE, name);
    if (fs.existsSync(src)) {
      ensureDir(PUBLIC_HERO_DIR);
      fs.copyFileSync(src, path.join(PUBLIC_HERO_DIR, name));
      n++;
    }
  }
  return n;
}

if (!fs.existsSync(ARTICLE)) {
  console.error(`Missing ${path.relative(ROOT, ARTICLE)} — run npm run materialize:articles`);
  process.exit(1);
}

if (renderReadmitted && slug === "readmitted") {
  console.log("Rendering READMITTED charts via R…");
  execSync("Rscript scripts/render-readmitted-charts.R", { cwd: ROOT, stdio: "inherit" });
}

ensureDir(PUBLIC_IMG);
ensureDir(PUBLIC_CHARTS);

let csvCount = 0;
if (slug === "anime") {
  // One public copy lives next to source.zip. The nested data/ folder duplicated it.
  if (fs.existsSync(PUBLIC_CSV)) fs.rmSync(PUBLIC_CSV, { recursive: true, force: true });
} else {
  ensureDir(PUBLIC_CSV);
  csvCount = copyGlob(DATA_SRC, PUBLIC_CSV, /\.csv$/i);
}
copyDirFlat(DATA_SRC, PUBLIC_DATA, /\.(csv|json|txt|qmd)$/i);

const pngImg = copyGlob(CHARTS_SRC, PUBLIC_IMG, /\.png$/i);
const jsonCount = copyGlob(CHARTS_SRC, PUBLIC_CHARTS, /\.plotly\.json$/i);
const pngData = copyGlob(CHARTS_SRC, PUBLIC_CHARTS, /\.png$/i);
const heroCount = copyHero();

console.log(
  `\n${slug} sync: ${csvCount} CSV to data/, ${pngImg} PNG to images, ${jsonCount} Plotly JSON, ${pngData} PNG in data/charts, ${heroCount} hero`,
);
console.log(`Published body: src/content/blog/${slug}.md (not overwritten by this sync)`);
