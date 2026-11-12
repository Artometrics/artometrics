#!/usr/bin/env node
/**
 * Print-quality PDF of one article, rendered from the built site (dist/) in light mode.
 *
 *   npm run build && npm run render:pdf -- --slug franchise
 *
 * Output: public/exports/<slug>.pdf (then `npm run cos:downloads` lists it for the page).
 */
import { mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import { startStaticServer } from "./lib/static-server.mjs";
import { TAGLINE } from "../lib/tagline.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const args = process.argv.slice(2);
const slug = args[args.indexOf("--slug") + 1];
if (!slug || args.indexOf("--slug") < 0) {
  console.error("Usage: npm run render:pdf -- --slug <slug>");
  process.exit(1);
}

const { origin, close } = await startStaticServer(join(ROOT, "dist"));
const browser = await chromium.launch();
try {
  const context = await browser.newContext({ viewport: { width: 1000, height: 1400 }, reducedMotion: "reduce" });
  await context.addInitScript(() => {
    localStorage.setItem("artometrics-theme", "light");
  });
  const page = await context.newPage();
  await page.goto(`${origin}/${slug}`, { waitUntil: "networkidle" });
  await page.emulateMedia({ media: "print" });
  await page.evaluate(async () => {
    document.querySelectorAll("img[loading=lazy]").forEach((img) => img.setAttribute("loading", "eager"));
    await Promise.all(
      [...document.images].map((img) => (img.complete ? null : new Promise((done) => { img.onload = img.onerror = done; }))),
    );
    await document.fonts.ready;
    window.__fitText?.fitAll();
  });
  await page.waitForTimeout(400);
  const out = join(ROOT, "public", "exports", `${slug}.pdf`);
  mkdirSync(dirname(out), { recursive: true });
  await page.pdf({
    path: out,
    format: "A4",
    printBackground: true,
    displayHeaderFooter: true,
    margin: { top: "16mm", bottom: "18mm", left: "13mm", right: "13mm" },
    headerTemplate: "<span></span>",
    footerTemplate: `<div style="width:100%;font:8px 'DejaVu Sans',sans-serif;color:#5c5148;padding:0 13mm;display:flex;justify-content:space-between"><span>artometrics.com/${slug} &middot; ${TAGLINE}</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
  });
  console.log("wrote", out);
} finally {
  await browser.close();
  await close();
}
