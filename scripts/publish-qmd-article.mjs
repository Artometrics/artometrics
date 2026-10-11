#!/usr/bin/env node
/**
 * Publish a Quarto article body to src/content/blog/<slug>.md.
 *
 * The .qmd is the source. The blog file is the live page. They drifted when
 * sync copied charts and left the body alone, and later shell passes then
 * spliced whatever paragraphs were left. A qmd with `publishBody: true`
 * regenerates the live page, including chart figures, so that split cannot
 * recur.
 *
 * Usage: node scripts/publish-qmd-article.mjs --slug padres
 */
import { readFileSync, writeFileSync, readdirSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import matter from "gray-matter";
import { marked } from "marked";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

function arg(name) {
  const index = process.argv.indexOf(`--${name}`);
  return index === -1 ? null : process.argv[index + 1];
}

function slugify(value) {
  return String(value)
    .toLowerCase()
    .replace(/<[^>]+>/g, "")
    .replace(/&amp;/g, "and")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

function yamlQuote(value) {
  return `"${String(value).replace(/\\/g, "\\\\").replace(/"/g, '\\"')}"`;
}

function dateStamp(value) {
  if (value instanceof Date) return value.toISOString().slice(0, 10);
  return String(value).slice(0, 10);
}

function findQmd(slug) {
  const dir = join(ROOT, "articles", slug);
  if (!existsSync(dir)) throw new Error(`Missing articles/${slug}`);
  const files = readdirSync(dir).filter((name) => name.endsWith(".qmd"));
  const marked = files.filter((name) => {
    const parsed = matter(readFileSync(join(dir, name), "utf8"));
    return parsed.data.publishBody === true;
  });
  if (marked.length === 1) return join(dir, marked[0]);
  if (files.length === 1) return join(dir, files[0]);
  throw new Error(`Could not choose a .qmd in articles/${slug}`);
}

function attr(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;");
}

function chartFigure(slug, href, alt, source) {
  const file = href.split("/").pop().replace(/\.png$/, "");
  const credit = source || "Lahman Baseball Database, 2025 (CC BY-SA). Artometrics.";
  return [
    '<figure class="art-chart">',
    `  <div class="art-chart-live" data-chart="/data/articles/${slug}/charts/${file}.plotly.json" data-fallback="/images/content/articles/${slug}/charts/${file}.png" data-source="${attr(credit)}" role="img" aria-label="${attr(alt)}"></div>`,
    `  <figcaption class="art-chart-caption art-chart-caption--visible">${alt}</figcaption>`,
    "</figure>",
  ].join("\n");
}

function renderBody(slug, markdown) {
  const renderer = new marked.Renderer();
  renderer.image = function ({ href, text, title }) {
    if (href && /charts\/.+\.png$/.test(href)) {
      return chartFigure(slug, href, text || "", title || "");
    }
    const alt = text || "";
    return `<img src="${href}" alt="${attr(alt)}" />`;
  };
  renderer.paragraph = function ({ tokens }) {
    const text = this.parser.parseInline(tokens);
    if (
      text.includes('class="art-chart"') ||
      text.includes("<figure") ||
      /^\s*<(div|table|blockquote|nav)/.test(text)
    ) {
      return `${text}\n`;
    }
    return `<p class="art-p">${text}</p>\n`;
  };
  renderer.heading = function ({ tokens, depth }) {
    const text = this.parser.parseInline(tokens);
    const id = slugify(text);
    if (depth === 2) return `<h2 id="${id}" class="anchored">${text}</h2>\n`;
    if (depth === 3) return `<h3 id="${id}" class="anchored">${text}</h3>\n`;
    return `<h${depth} id="${id}">${text}</h${depth}>\n`;
  };
  renderer.blockquote = function ({ text }) {
    return `<blockquote>${text}</blockquote>\n`;
  };
  renderer.html = function ({ text }) {
    return text;
  };

  return marked.parse(markdown, { renderer, gfm: true });
}

function toc(html) {
  const items = [];
  const re = /<h2 id="([^"]+)"[^>]*>(.*?)<\/h2>/g;
  let match;
  while ((match = re.exec(html))) {
    const label = match[2].replace(/<[^>]+>/g, "");
    items.push(`<li><a href="#${match[1]}">${label}</a></li>`);
  }
  if (!items.length) return "";
  return [
    '<nav id="TOC" role="doc-toc">',
    '<h2 id="toc-title" class="anchored">IN THIS REPORT</h2>',
    "<ul>",
    ...items,
    "</ul>",
    "</nav>",
  ].join("\n");
}

function frontmatter(data, slug) {
  const tags = Array.isArray(data.tags) ? data.tags : ["sports", "baseball"];
  const lines = [
    "---",
    `title: ${yamlQuote(data.title)}`,
    `slug: ${slug}`,
    `author: ${data.author || "kyle-mcauliffe"}`,
    `pubDate: ${dateStamp(data.date || data.pubDate)}T00:00:00.000Z`,
    `description: ${yamlQuote(data.description)}`,
    `heroImage: ${data.heroImage || `/images/content/articles/${slug}/hero.png`}`,
    `audioSrc: ${data.audioSrc || ""}`,
    "draft: false",
    "tags:",
    ...tags.map((tag) => `  - ${tag}`),
    `subject: ${data.subject || "Padres"}`,
  ];
  if (data.tldr) lines.push(`tldr: ${yamlQuote(data.tldr)}`);
  if (Array.isArray(data.keyPoints)) {
    lines.push("keyPoints:");
    for (const point of data.keyPoints) lines.push(`  - ${yamlQuote(point)}`);
  }
  if (Array.isArray(data.faq)) {
    lines.push("faq:");
    for (const item of data.faq) {
      lines.push(`  - question: ${yamlQuote(item.question)}`);
      lines.push(`    answer: ${yamlQuote(item.answer)}`);
    }
  }
  lines.push("---");
  return lines.join("\n");
}

const slug = arg("slug");
if (!slug) {
  console.error("Usage: node scripts/publish-qmd-article.mjs --slug padres");
  process.exit(1);
}

const qmdPath = findQmd(slug);
const parsed = matter(readFileSync(qmdPath, "utf8"));
if (parsed.data.publishBody !== true) {
  console.log(`${slug}: publishBody is not set; leaving src/content/blog/${slug}.md alone`);
  process.exit(0);
}

let markdown = parsed.content.trim();
// Editor notes live in the .qmd; they must not ship in the static HTML body.
markdown = markdown.replace(/<!--\s*TODO Kyle:[\s\S]*?-->\s*/g, "");

let html = renderBody(slug, markdown);
html = html.replace(/<p class="art-p">\s*(<figure[\s\S]*?<\/figure>)\s*<\/p>/g, "$1\n");
html = html.replace(/<p class="art-p">\s*(<div[\s\S]*?<\/div>)\s*<\/p>/g, "$1\n");

const page = [
  frontmatter(parsed.data, slug),
  '<div id="quarto-content">',
  toc(html),
  '<main class="art-article-main">',
  html.trim(),
  "</main>",
  "</div>",
  "",
].join("\n");

const out = join(ROOT, "src/content/blog", `${slug}.md`);
writeFileSync(out, page);
console.log(`Published ${qmdPath.replace(ROOT + "/", "")} → src/content/blog/${slug}.md`);
