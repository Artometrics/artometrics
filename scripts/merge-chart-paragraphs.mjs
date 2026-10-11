#!/usr/bin/env node
/**
 * Merge consecutive <p class="art-p"> blocks adjacent to each <figure class="art-chart">
 * (immediately before and/or after the figure) into a single paragraph per chart.
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const blogDir = path.join(__dirname, "../src/content/blog");

const ART_P =
  /<p class="art-p">(?![^>]*\bart-lede\b)([\s\S]*?)<\/p>/;

function isBoundaryTail(text) {
  const tail = text.trimEnd();
  return (
    tail.endsWith("</h3>") ||
    tail.endsWith("</h2>") ||
    tail.endsWith("</figure>")
  );
}

function splitTrailingArtP(text) {
  const paras = [];
  let t = text;
  while (true) {
    const m = t.match(
      /(<p class="art-p">(?![^>]*\bart-lede\b)[\s\S]*?<\/p>)\s*$/
    );
    if (!m) break;
    paras.unshift(m[1]);
    t = t.slice(0, t.length - m[0].length);
    if (isBoundaryTail(t)) break;
  }
  return { paras, prefix: t };
}

function splitLeadingArtP(text) {
  const paras = [];
  let t = text;
  while (true) {
    const m = t.match(
      /^\s*(<p class="art-p">(?![^>]*\bart-lede\b)[\s\S]*?<\/p>)/
    );
    if (!m) break;
    paras.push(m[1]);
    t = t.slice(m[0].length);
  }
  return { paras, suffix: t };
}

function extractInner(pBlock) {
  const m = pBlock.match(ART_P);
  return m ? m[1].trim() : "";
}

function mergeChartParagraphsInBody(body) {
  let result = body;
  let merges = 0;
  let charts = 0;
  let searchEnd = result.length;

  while (true) {
    const figEnd = result.lastIndexOf("</figure>", searchEnd - 1);
    if (figEnd === -1) break;
    const figStart = result.lastIndexOf('<figure class="art-chart">', figEnd);
    if (figStart === -1) break;

    charts += 1;
    const figHtml = result.slice(figStart, figEnd + "</figure>".length);
    const before = result.slice(0, figStart);
    const after = result.slice(figStart + figHtml.length);

    const { paras: parasBefore, prefix: beforeKeep } = splitTrailingArtP(before);
    const { paras: parasAfter, suffix: afterKeep } = splitLeadingArtP(after);

    searchEnd = figStart;

    const all = [...parasBefore, ...parasAfter];
    if (all.length <= 1) continue;

    const mergedInner = all
      .map(extractInner)
      .filter(Boolean)
      .join(" ")
      .replace(/\s+/g, " ");

    const mergedBlock = `<p class="art-p">${mergedInner}</p>`;

    result =
      beforeKeep +
      figHtml +
      "\n" +
      mergedBlock +
      "\n" +
      afterKeep.replace(/^\n+/, "");

    merges += 1;
  }

  return { body: result, merges, charts };
}

function processFile(filePath) {
  const raw = fs.readFileSync(filePath, "utf8");
  const fmEnd = raw.indexOf("---", 3);
  if (fmEnd === -1) return null;
  const frontmatter = raw.slice(0, fmEnd + 3);
  const body = raw.slice(fmEnd + 3);

  const { body: newBody, merges, charts } = mergeChartParagraphsInBody(body);
  if (merges === 0) return { merges: 0, charts };

  fs.writeFileSync(filePath, frontmatter + newBody, "utf8");
  return { merges, charts };
}

let totalMerges = 0;
let totalCharts = 0;
let filesTouched = 0;

function publishedFromQmd(name) {
  const slug = name.replace(/\.md$/, "");
  const dir = path.join(__dirname, "../articles", slug);
  if (!fs.existsSync(dir)) return false;
  return fs.readdirSync(dir).some((file) => {
    if (!file.endsWith(".qmd")) return false;
    return fs.readFileSync(path.join(dir, file), "utf8").includes("publishBody: true");
  });
}

for (const name of fs.readdirSync(blogDir).sort()) {
  if (!name.endsWith(".md")) continue;
  if (publishedFromQmd(name)) {
    console.log(`${name}: skipped (published from the .qmd)`);
    continue;
  }
  const stats = processFile(path.join(blogDir, name));
  if (!stats) continue;
  totalCharts += stats.charts;
  if (stats.merges > 0) {
    totalMerges += stats.merges;
    filesTouched += 1;
    console.log(
      `${name}: ${stats.merges} chart section(s) merged (${stats.charts} charts)`
    );
  }
}

console.log(
  `\nDone: ${totalMerges} merges across ${filesTouched} files (${totalCharts} charts scanned).`
);
