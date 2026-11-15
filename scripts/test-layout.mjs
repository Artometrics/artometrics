#!/usr/bin/env node
/**
 * Layout checks on the built site (run `npm run build` first).
 * Every article at 320, 390 and 1280: headings never break mid-word or overflow,
 * the cover leads the page, byline sits above the dek, share row sits under the cover,
 * key facts are four colored squares with any wide box last, and the page ends with the
 * category grid and the full footer.
 *
 *   npm run test:layout
 */
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { readFileSync } from "node:fs";
import { chromium } from "playwright";
import { startStaticServer } from "./lib/static-server.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const WIDTHS = [320, 390, 1280];
const blog = JSON.parse(readFileSync(join(ROOT, "src/generated/blog.json"), "utf8"));
const only = process.argv.slice(2).filter((a) => !a.startsWith("-"));
const slugs = blog.filter((p) => !p.draft).map((p) => p.slug).filter((s) => !only.length || only.includes(s));

let failed = 0;
let passed = 0;
function check(ok, message) {
  if (ok) passed += 1;
  else {
    failed += 1;
    console.error("FAIL", message);
  }
}

const { origin, close } = await startStaticServer(join(ROOT, "dist"));
const browser = await chromium.launch();

const inspect = () => {
  const rect = (el) => el.getBoundingClientRect();
  const words = (el) => {
    if (!el) return [];
    const out = [];
    const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
    for (let node = walker.nextNode(); node; node = walker.nextNode()) {
      const text = node.textContent;
      const re = /[^\s\u2013\u2014-]+/g;
      let m;
      while ((m = re.exec(text))) {
        const range = document.createRange();
        range.setStart(node, m.index);
        range.setEnd(node, m.index + m[0].length);
        const rects = [...range.getClientRects()].filter((r) => r.width > 0 && r.height > 0);
        out.push({ word: m[0], lines: new Set(rects.map((r) => Math.round(r.top))).size, right: Math.max(...rects.map((r) => r.right), 0) });
      }
    }
    return out;
  };
  const cover = document.querySelector("[data-cover]");
  const title = document.querySelector(".cover__title");
  const kicker = document.querySelector(".cover__kicker");
  const headline = document.querySelector(".cover__headline");
  const share = document.querySelector("[data-share-row]");
  const keyfigs = document.querySelector("[data-keyfigs]");
  const grid = document.querySelector("[data-category-grid]");
  const footer = document.querySelector(".site-footer");
  const byline = document.querySelector(".report-updated__line, .eg-byline");
  const dek = document.querySelector(".report-dek, .eg-dek");
  const vw = document.documentElement.clientWidth;
  const squares = [...document.querySelectorAll(".keyfigs__grid > .keyfig")];
  const wides = [...document.querySelectorAll(".keyfigs__wide > .keyfig")];
  const buttons = [...document.querySelectorAll("[data-share-row] a")];
  return {
    vw,
    scrollW: document.documentElement.scrollWidth,
    hasCover: Boolean(cover),
    baked: Boolean(cover?.classList.contains("cover--baked")),
    coverTop: cover ? rect(cover).top + scrollY : -1,
    coverBottom: cover ? rect(cover).bottom + scrollY : -1,
    headlineWords: words(headline).concat(words(kicker)),
    titleRight: title ? rect(title).right : 0,
    shareTop: share ? rect(share).top + scrollY : -1,
    shareBottom: share ? rect(share).bottom + scrollY : -1,
    shareRight: share ? Math.max(...buttons.map((b) => rect(b).right)) : 0,
    shareLabels: buttons.map((b) => b.getAttribute("aria-label") || ""),
    keyTop: keyfigs ? rect(keyfigs).top + scrollY : -1,
    keyBottom: keyfigs ? rect(keyfigs).bottom + scrollY : -1,
    squares: squares.length,
    wides: wides.length,
    squareLefts: new Set(squares.map((s) => Math.round(rect(s).left))).size,
    squareCentered: squares.every((s) => getComputedStyle(s.querySelector(".keyfig__value")).textAlign === "center"),
    wideAfterSquares: wides.every((w) => squares.every((s) => rect(w).top >= rect(s).bottom - 1)),
    keyOverflow: [...squares, ...wides].filter((s) => s.scrollWidth > s.clientWidth + 1).length,
    gridTop: grid ? rect(grid).top + scrollY : -1,
    gridTiles: grid ? grid.querySelectorAll("a").length : 0,
    footerTop: footer ? rect(footer).top + scrollY : -1,
    footerText: footer ? footer.textContent.replace(/\s+/g, " ") : "",
    footerLinks: footer ? [...footer.querySelectorAll("a")].map((a) => a.getAttribute("href")) : [],
    bylineTop: byline ? rect(byline).top + scrollY : null,
    dekTop: dek ? rect(dek).top + scrollY : null,
    bodyText: document.body.textContent,
  };
};

for (const width of WIDTHS) {
  const context = await browser.newContext({ viewport: { width, height: 800 }, reducedMotion: "reduce" });
  const page = await context.newPage();
  for (const slug of slugs) {
    const tag = `${width}px /${slug}`;
    await page.goto(`${origin}/${slug}`, { waitUntil: "load" });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(60);
    const r = await page.evaluate(inspect);
    check(r.scrollW <= r.vw + 1, `${tag}: no sideways scroll (${r.scrollW} > ${r.vw})`);
    const egEdition = slug === "franchise";
    check(r.hasCover || egEdition, `${tag}: cover renders`);
    const broken = r.baked ? [] : r.headlineWords.filter((w) => w.lines > 1 || w.right > r.vw + 1);
    check(broken.length === 0, `${tag}: headline words stay whole ${JSON.stringify(broken.slice(0, 3))}`);
    if (!egEdition) check(r.shareTop >= r.coverBottom - 1 && r.shareTop - r.coverBottom < 60, `${tag}: share row sits directly under the cover`);
    check(r.shareRight <= r.vw + 1, `${tag}: share row fits the viewport`);
    check(r.shareLabels.some((l) => /LinkedIn/.test(l)) && r.shareLabels.some((l) => /Reddit/.test(l)), `${tag}: share buttons present`);
    if (r.squares) {
      const total = r.squares + r.wides;
      const wantSquares = total >= 4 ? 4 : total === 3 ? 2 : total;
      check(r.squares === wantSquares, `${tag}: ${wantSquares} key-fact squares (${r.squares}) and ${r.wides} wide`);
      const cols = Math.min(width < 720 ? 2 : 4, r.squares);
      check(r.squareLefts === cols, `${tag}: squares in ${cols} columns (${r.squareLefts})`);
      check(r.squareCentered, `${tag}: key numbers centered`);
      check(r.wideAfterSquares, `${tag}: wide box sits after the squares`);
      check(r.keyOverflow === 0, `${tag}: key facts fit their boxes`);
    }
    check(r.gridTiles >= 16, `${tag}: category grid has tiles (${r.gridTiles})`);
    check(r.gridTop > r.coverBottom && r.footerTop > r.gridTop, `${tag}: category grid ends the article, above the footer`);
    for (const label of ["Reports", "Sources", "RSS", "About", "Legal", "Podcast"]) {
      check(new RegExp(label, "i").test(r.footerText), `${tag}: footer has ${label}`);
    }
    check(r.footerLinks.includes("/rss.xml") && r.footerLinks.some((h) => /github\.com/.test(h || "")), `${tag}: footer has RSS and GitHub links`);
    check(!/\bPublished\b/.test(r.bodyText.slice(0, 4000)), `${tag}: no "Published" label near the top`);
    if (r.bylineTop !== null && r.dekTop !== null) check(r.bylineTop < r.dekTop, `${tag}: byline above the dek`);
  }
  await context.close();
}

await browser.close();
await close();
if (failed) {
  console.error(`\n${failed} failed, ${passed} passed`);
  process.exit(1);
}
console.log(`layout OK (${passed} checks, ${slugs.length} articles x ${WIDTHS.length} widths)`);
