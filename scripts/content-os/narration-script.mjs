#!/usr/bin/env node
/**
 * Build a paste-ready narration script from a published report.
 *
 * Unlike cos:narrate (which calls the ElevenLabs API and truncates to one TTS
 * chunk), this emits the full article as plain text for manual narration:
 * charts, captions and figures are dropped, and notation that reads badly aloud
 * -- typographic quotes, "$3.9bn", "45 2/3" -- is expanded.
 *
 * The fact grid and the trailing method/references apparatus are dropped by
 * default -- the grid restates numbers the prose already carries, and reads as a
 * clipped list aloud.
 *
 *   npm run cos:narration-script -- --slug <slug>
 *   npm run cos:narration-script -- --slug <slug> --keep-facts --keep-method
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "../..");

const args = process.argv.slice(2);
const slug = valueOf("--slug");
const keepMethod = args.includes("--keep-method");
const keepFacts = args.includes("--keep-facts");
const outDirArg = valueOf("--out-dir");

function valueOf(flag) {
  const i = args.indexOf(flag);
  return i === -1 ? null : args[i + 1];
}

if (!slug) {
  console.error("Usage: npm run cos:narration-script -- --slug <slug> [--keep-method] [--out-dir <dir>]");
  process.exit(1);
}

// Trailing apparatus: printed in the report, not read aloud.
const TAIL_HEADINGS = new Set([
  "references",
  "editor's note",
  "editors note",
  "sources",
]);
const METHOD_HEADINGS = new Set(["data and method", "method", "data"]);
const FACT_HEADINGS = new Set([
  "the numbers behind the story",
  "fast facts",
  "the numbers",
]);

const FRACTIONS = {
  "½": " and a half",
  "⅓": " and a third",
  "⅔": " and two-thirds",
  "¼": " and a quarter",
  "¾": " and three-quarters",
  "⅕": " and a fifth",
  "⅖": " and two-fifths",
  "⅗": " and three-fifths",
  "⅘": " and four-fifths",
  "⅙": " and a sixth",
  "⅛": " and an eighth",
  "⅜": " and three-eighths",
  "⅝": " and five-eighths",
  "⅞": " and seven-eighths",
};

function speakable(text) {
  let out = text;
  // Typographic punctuation some voices read as an audible artifact.
  out = out
    .replace(/[\u2018\u2019\u201A\u201B]/g, "'")
    .replace(/[\u201C\u201D\u201E\u201F]/g, '"')
    .replace(/\u2026/g, "...")
    .replace(/\u00A0/g, " ");
  for (const [glyph, words] of Object.entries(FRACTIONS)) {
    out = out.split(glyph).join(words);
  }
  // Abbreviated magnitudes: "$3.9bn" -> "$3.9 billion", "$858m" -> "$858 million".
  out = out
    .replace(/\$(\d+(?:\.\d+)?)\s?(?:bn|b)\b/gi, "$$$1 billion")
    .replace(/\$(\d+(?:\.\d+)?)\s?(?:mm|m)\b/gi, "$$$1 million")
    .replace(/\$(\d+(?:\.\d+)?)\s?k\b/gi, "$$$1 thousand");
  // Bare magnitudes, e.g. "3.4m admissions".
  out = out.replace(/\b(\d+(?:\.\d+)?)m\b/g, "$1 million");
  out = out.replace(/(\d)\s?%/g, "$1 percent");
  return out.replace(/\s+/g, " ").trim();
}

function unwrapTags(html) {
  return decode(html.replace(/<[^>]+>/g, ""));
}

function decode(text) {
  return text
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&hellip;/g, "...");
}

const mdPath = path.join(ROOT, "src/content/blog", `${slug}.md`);
if (!fs.existsSync(mdPath)) {
  console.error(`Missing ${mdPath}`);
  process.exit(1);
}

const raw = fs.readFileSync(mdPath, "utf8");
const fmMatch = raw.match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
if (!fmMatch) {
  console.error(`No frontmatter in ${mdPath}`);
  process.exit(1);
}
const [, frontmatter, body] = fmMatch;
const titleMatch = frontmatter.match(/^title:\s*"((?:[^"\\]|\\.)*)"/m);
const title = titleMatch ? titleMatch[1].replace(/\\"/g, '"') : slug;

const lines = [speakable(title), ""];
let stopped = false;

for (const rawLine of body.split("\n")) {
  if (stopped) break;
  const line = rawLine.trim();
  if (!line) continue;

  // Fact-grid tiles read best as "<number>: <label>." Checked before the
  // container skip below, since each tile is its own <div>.
  if (line.includes('class="fact-box"')) {
    if (!keepFacts) continue;
    const number = line.match(/fact-number[^>]*>([\s\S]*?)<\/span>/i);
    const label = line.match(/fact-label[^>]*>([\s\S]*?)<\/span>/i);
    if (number && label) {
      const n = speakable(unwrapTags(number[1])).replace(/[.:]$/, "");
      const l = speakable(unwrapTags(label[1])).replace(/\.$/, "");
      lines.push(`${n}: ${l}.`);
    }
    continue;
  }

  // Charts, figures and their captions carry no audio.
  if (/^<\/?(figure|div|main|section)\b/i.test(line)) continue;
  if (/figcaption|art-chart|data-chart|chart-frame__title|data-carousel|carousel__/i.test(line)) continue;

  const heading = line.match(/^<h[23][^>]*>([\s\S]*?)<\/h[23]>$/i);
  if (heading) {
    const text = unwrapTags(heading[1]).trim();
    const key = text.toLowerCase().replace(/[.:]$/, "");
    if (TAIL_HEADINGS.has(key) || (!keepMethod && METHOD_HEADINGS.has(key))) {
      stopped = true;
      break;
    }
    // The fact grid restates numbers the prose already covers, so its heading
    // is dropped alongside the tiles unless they are explicitly kept.
    if (!keepFacts && FACT_HEADINGS.has(key)) continue;
    lines.push("", speakable(text).toUpperCase(), "");
    continue;
  }

  const item = line.match(/^<li[^>]*>([\s\S]*?)<\/li>$/i);
  if (item) {
    const text = speakable(unwrapTags(item[1]));
    if (text) lines.push(text, "");
    continue;
  }

  const para = line.match(/^<(p|blockquote)[^>]*>([\s\S]*?)<\/\1>$/i);
  if (para) {
    const text = speakable(unwrapTags(para[2]));
    if (text) lines.push(text, "");
    continue;
  }

  const quotedPara = line.match(/^<blockquote[^>]*><p[^>]*>([\s\S]*?)<\/p><\/blockquote>$/i);
  if (quotedPara) {
    const text = speakable(unwrapTags(quotedPara[1]));
    if (text) lines.push(text, "");
  }
}

const outDir = outDirArg
  ? path.resolve(ROOT, outDirArg)
  : path.join(ROOT, "public/exports/narration");
fs.mkdirSync(outDir, { recursive: true });
const outPath = path.join(outDir, `${slug}.txt`);
const text = `${lines.join("\n").replace(/\n{3,}/g, "\n\n").trim()}\n`;
fs.writeFileSync(outPath, text, "utf8");

const words = text.split(/\s+/).filter(Boolean).length;
console.log(
  `${path.relative(ROOT, outPath)} — ${words} words, ~${Math.round(words / 150)} min at 150 wpm`
);
