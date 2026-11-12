#!/usr/bin/env node
/**
 * Browser checks on the built site (run `npm run build` first).
 * Phone (390x844) and desktop (1280x800), light and dark.
 *
 *   npm run test:browser
 */
import { existsSync, readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import sharp from "sharp";
import { startStaticServer } from "./lib/static-server.mjs";
import { collectContrastFailures } from "./lib/contrast.mjs";
import { TAGLINE } from "../lib/tagline.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const VIEWPORTS = [
  { name: "phone", width: 390, height: 844 },
  { name: "desktop", width: 1280, height: 800 },
];
const THEMES = ["light", "dark"];
let failed = 0;
let passed = 0;

function check(ok, message) {
  if (ok) {
    passed += 1;
  } else {
    failed += 1;
    console.error("FAIL", message);
  }
}

function ptDate(date) {
  return date.toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    year: "numeric",
    timeZone: "America/Los_Angeles",
  });
}

const { origin, close } = await startStaticServer(join(ROOT, "dist"));
const browser = await chromium.launch();

async function open(viewport, theme, path, options = {}) {
  const context = await browser.newContext({
    viewport: { width: viewport.width, height: viewport.height },
    reducedMotion: "reduce",
    timezoneId: options.timezoneId || "America/Los_Angeles",
    acceptDownloads: true,
  });
  await context.addInitScript((value) => localStorage.setItem("artometrics-theme", value), theme);
  const page = await context.newPage();
  if (options.fixedTime) await page.clock.setFixedTime(options.fixedTime);
  await page.goto(origin + path, { waitUntil: "networkidle" });
  return { context, page };
}

async function loadLazyImages(page) {
  await page.evaluate(async () => {
    document.querySelectorAll("img[loading=lazy]").forEach((img) => img.setAttribute("loading", "eager"));
    await Promise.all([...document.images].map((img) => (img.complete ? null : new Promise((done) => { img.onload = img.onerror = done; }))));
  });
}

/** Worst-case brightness behind a line of light type: sample the pixels with the text hidden. */
async function backdropContrast(page, selector) {
  const target = page.locator(selector).first();
  await target.scrollIntoViewIfNeeded();
  const box = await target.boundingBox();
  const color = await target.evaluate((el) => getComputedStyle(el).color);
  await target.evaluate((el) => { el.style.visibility = "hidden"; });
  const shot = await page.screenshot({ clip: box });
  await target.evaluate((el) => { el.style.visibility = ""; });
  const { data } = await sharp(shot).removeAlpha().raw().toBuffer({ resolveWithObject: true });
  const lum = (r, g, b) => {
    const f = (v) => { v /= 255; return v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4; };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  };
  const samples = [];
  for (let i = 0; i < data.length; i += 3) samples.push(lum(data[i], data[i + 1], data[i + 2]));
  samples.sort((a, b) => a - b);
  const p90 = samples[Math.floor(samples.length * 0.9)];
  const [r, g, b] = /rgba?\(([^)]+)\)/.exec(color)[1].split(/[,\s/]+/).map(Number);
  const text = lum(r, g, b);
  return (Math.max(p90, text) + 0.05) / (Math.min(p90, text) + 0.05);
}

for (const viewport of VIEWPORTS) {
  for (const theme of THEMES) {
    const tag = `${viewport.name} ${theme}`;

    {
      const { context, page } = await open(viewport, theme, "/");
      await page.waitForSelector("[data-fit-ready]");

      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      check(overflow <= 0, `${tag} home: no sideways scroll (${overflow}px)`);

      const banner = await page.evaluate(() => {
        const root = document.querySelector("[data-banner-carousel]");
        const slide = root.querySelector("[data-banner-slide]:not([hidden])");
        const copy = slide.querySelector(".desk-lead__copy");
        const word = slide.querySelector(".banner-carousel__kicker");
        const frame = slide.querySelector(".desk-lead__hit").getBoundingClientRect();
        const wordBox = word.getBoundingClientRect();
        const copyStyle = getComputedStyle(copy);
        return {
          controls: root.querySelectorAll("button, [role=button], [data-banner-prev], [data-banner-next], [data-banner-pause]").length,
          text: root.innerText,
          copyBg: copyStyle.backgroundColor,
          copyImage: copyStyle.backgroundImage,
          fill: wordBox.width / frame.width,
          wordPx: parseFloat(getComputedStyle(word).fontSize),
          wordLeft: wordBox.left - frame.left,
          wordRight: frame.right - wordBox.right,
          sub: slide.querySelector(".banner-carousel__sub")?.getBoundingClientRect() ?? null,
          subLeft: (slide.querySelector(".banner-carousel__sub")?.getBoundingClientRect().left ?? 0) - frame.left,
          frameWidth: frame.width,
        };
      });
      check(banner.controls === 0, `${tag} banner: no controls (${banner.controls})`);
      check(!/previous|pause|next|\d+ of \d+/i.test(banner.text), `${tag} banner: no PREVIOUS / PAUSE / NEXT / "n of m" text`);
      check(/rgba\(0, 0, 0, 0\)|transparent/.test(banner.copyBg) && banner.copyImage === "none", `${tag} banner: no dark box behind the title (${banner.copyBg}, ${banner.copyImage})`);
      check(banner.fill >= 0.9, `${tag} banner: the title runs border to border (${(banner.fill * 100).toFixed(0)}% of the width)`);
      check(banner.wordLeft >= -1 && banner.wordRight >= -1, `${tag} banner: the title stays inside the borders (${banner.wordLeft.toFixed(1)}, ${banner.wordRight.toFixed(1)})`);
      check(banner.wordPx >= (viewport.width < 600 ? 60 : 100), `${tag} banner: the title is big (${banner.wordPx.toFixed(0)}px)`);
      if (banner.sub) {
        check(Math.abs(banner.subLeft - banner.wordLeft) <= 3, `${tag} banner: the subtitle lines up with the title's left edge (${banner.subLeft.toFixed(1)} vs ${banner.wordLeft.toFixed(1)})`);
      }
      const bannerContrast = await backdropContrast(page, "[data-banner-slide]:not([hidden]) .banner-carousel__kicker");
      check(bannerContrast >= 3, `${tag} banner: title is readable on the picture (${bannerContrast.toFixed(2)}:1 at the 90th-percentile pixel)`);

      const tiles = await page.evaluate(() => [...document.querySelectorAll(".story-tile")].slice(0, 12).map((tile) => {
        const word = tile.querySelector("[data-fit]");
        const box = tile.getBoundingClientRect();
        const w = word?.getBoundingClientRect();
        return {
          text: tile.innerText.trim(),
          extra: [...tile.querySelectorAll("p, small, .story-tile__dek, .dek")].map((el) => el.textContent.trim()).filter(Boolean),
          fill: w ? w.width / box.width : 0,
          inside: w ? w.left >= box.left - 1 && w.right <= box.right + 1 : false,
          px: w ? parseFloat(getComputedStyle(word).fontSize) : 0,
        };
      }));
      check(tiles.length >= 8, `${tag} tiles: found ${tiles.length}`);
      check(tiles.every((tile) => tile.extra.length === 0), `${tag} tiles: no dek or subtitle text`);
      check(tiles.every((tile) => tile.text.split("\n").length <= 2), `${tag} tiles: title only`);
      check(tiles.every((tile) => tile.inside), `${tag} tiles: titles stay inside the tile`);
      check(tiles.filter((tile) => tile.fill >= 0.85).length >= tiles.length * 0.7, `${tag} tiles: titles fit the tile borders`);
      check(tiles.every((tile) => tile.px >= 18), `${tag} tiles: titles are big`);
      const tileContrast = await backdropContrast(page, ".story-tile [data-fit]");
      check(tileContrast >= 3, `${tag} tiles: title is readable on the picture (${tileContrast.toFixed(2)}:1)`);

      const header = await page.evaluate(() => ({
        tag: document.querySelector(".wordmark__tag")?.textContent?.trim(),
        tagVisible: (() => { const el = document.querySelector(".wordmark__tag"); return el ? getComputedStyle(el).display !== "none" && el.getBoundingClientRect().right <= innerWidth : false; })(),
        description: document.querySelector('meta[name="description"]')?.content || "",
        og: document.querySelector('meta[property="og:description"]')?.content || "",
        logoOverlap: (() => {
          const tagEl = document.querySelector(".wordmark__tag");
          const mark = document.querySelector(".wordmark img, .wordmark svg");
          if (!tagEl || !mark) return null;
          return tagEl.getBoundingClientRect().top - mark.getBoundingClientRect().bottom;
        })(),
      }));
      check(header.tag === TAGLINE, `${tag} tagline in the header`);
      check(header.tagVisible, `${tag} tagline visible and on screen`);
      check(header.logoOverlap === null || header.logoOverlap >= -1, `${tag} tagline does not overlap the logo (${header.logoOverlap})`);
      check(header.description.startsWith(TAGLINE), `${tag} meta description starts with the tagline`);
      check(header.og.startsWith(TAGLINE), `${tag} og:description starts with the tagline`);

      const contrast = await page.evaluate(`(${collectContrastFailures.toString()})()`);
      check(contrast.failures.length === 0, `${tag} home contrast: ${contrast.failures.length} failures ${JSON.stringify(contrast.failures.slice(0, 3))}`);
      await context.close();
    }

    {
      const { context, page } = await open(viewport, theme, "/about");
      const footer = await page.locator(".site-footer__tagline").first().textContent();
      check(footer?.trim() === TAGLINE, `${tag} tagline in the footer`);
      await context.close();
    }

    {
      const { context, page } = await open(viewport, theme, "/franchise");
      await loadLazyImages(page);

      const overflow = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      check(overflow <= 0, `${tag} franchise: no sideways scroll (${overflow}px)`);

      const top = await page.evaluate(() => {
        const banner = document.querySelector(".article-banner img");
        const h1 = document.querySelector(".preview-report h1");
        const kicker = h1.querySelector(".report-kicker");
        const range = document.createRange();
        const headline = [...h1.childNodes].find((node) => node.nodeType === 3 && node.textContent.trim());
        range.selectNodeContents(headline);
        const style = getComputedStyle(kicker);
        return {
          bannerBottom: banner?.getBoundingClientRect().bottom ?? null,
          bannerLoaded: banner ? banner.naturalWidth > 0 : false,
          h1Top: h1.getBoundingClientRect().top,
          kickerDisplay: style.display,
          gap: range.getBoundingClientRect().top - kicker.getBoundingClientRect().bottom,
        };
      });
      check(top.bannerLoaded, `${tag} article: banner image loads`);
      check(top.bannerBottom !== null && top.bannerBottom <= top.h1Top, `${tag} article: banner sits above the title`);
      check(top.kickerDisplay === "block" && top.gap >= 6, `${tag} article: space between the kicker and the headline (${top.gap.toFixed(1)}px)`);

      const figs = await page.evaluate(() => {
        const boxes = [...document.querySelectorAll(".keyfig")];
        return {
          count: boxes.length,
          shadow: boxes.every((box) => /\d+px \d+px 0px 0px|0px 0px/.test(getComputedStyle(box).boxShadow) && !/none/.test(getComputedStyle(box).boxShadow)),
          offset: boxes.map((box) => getComputedStyle(box).boxShadow.match(/(\d+)px (\d+)px/)?.slice(1, 3).map(Number) ?? [0, 0]),
          border: boxes.every((box) => parseFloat(getComputedStyle(box).borderTopWidth) >= 3),
          colors: new Set(boxes.map((box) => getComputedStyle(box).backgroundColor)).size,
          overflowing: boxes.filter((box) => box.querySelector(".keyfig__value").scrollWidth > box.clientWidth || box.scrollWidth > box.clientWidth + 1).length,
          columns: new Set(boxes.map((box) => Math.round(box.getBoundingClientRect().left))).size,
          valueSizes: boxes.map((box) => parseFloat(getComputedStyle(box.querySelector(".keyfig__value")).fontSize)),
          hasLabel: boxes.every((box) => box.querySelector(".keyfig__label")?.textContent.trim().length > 0),
          values: boxes.map((box) => box.querySelector(".keyfig__value").textContent.trim()),
        };
      });
      check(figs.count >= 5, `${tag} key figures: ${figs.count} boxes`);
      check(figs.shadow && figs.offset.every(([x, y]) => x >= 4 && y >= 4), `${tag} key figures: hard offset shadow`);
      check(figs.border, `${tag} key figures: thick border`);
      check(figs.colors >= 3, `${tag} key figures: bold brand colours (${figs.colors})`);
      check(figs.overflowing === 0, `${tag} key figures: numbers fit their boxes`);
      check(figs.hasLabel, `${tag} key figures: every box has a label`);
      check(figs.valueSizes.every((px) => px >= (viewport.width < 600 ? 18 : 26)), `${tag} key figures: big numbers (${figs.valueSizes.map((n) => n.toFixed(0))})`);
      check(figs.columns === (viewport.width < 600 ? 2 : 3), `${tag} key figures: responsive grid (${figs.columns} columns)`);
      check(figs.values.includes("$1,460.1B") && figs.values.includes("55.6%") && figs.values.includes("$130.7B"), `${tag} key figures: published numbers unchanged`);

      const slides = await page.evaluate(() => {
        const track = document.querySelector(".chartcar__track");
        const items = [...document.querySelectorAll(".chartcar__slide")];
        const charts = document.querySelectorAll(".artometrics-article-body figure.art-chart .art-chart-live").length;
        const visible = (img) => getComputedStyle(img).display !== "none";
        return {
          slides: items.length,
          charts,
          scrollable: track.scrollWidth > track.clientWidth + 20,
          described: items.every((item) => item.querySelector(".chartcar__text").textContent.trim().length > 8),
          links: items.every((item, i) => item.querySelector("a").getAttribute("href") === `#chart-${i + 1}`),
          anchors: items.every((_, i) => document.getElementById(`chart-${i + 1}`)),
          visibleSrc: [...items[0].querySelectorAll("img")].filter(visible).map((img) => img.getAttribute("src")),
          snap: getComputedStyle(track).scrollSnapType,
        };
      });
      check(slides.slides >= 15 && slides.slides === slides.charts, `${tag} carousel: every chart is a slide (${slides.slides} of ${slides.charts})`);
      check(slides.scrollable, `${tag} carousel: swipes sideways`);
      check(/x/.test(slides.snap), `${tag} carousel: slides snap`);
      check(slides.described, `${tag} carousel: each slide has its description`);
      check(slides.links && slides.anchors, `${tag} carousel: slides link to chart anchors`);
      check(slides.visibleSrc.length === 1 && slides.visibleSrc[0].endsWith(theme === "dark" ? "-dark.png" : ".png") && (theme === "dark" || !slides.visibleSrc[0].endsWith("-dark.png")), `${tag} carousel: thumbnail matches the theme (${slides.visibleSrc})`);

      const track = page.locator(".chartcar__track");
      await track.evaluate((el) => el.scrollBy({ left: el.clientWidth * 0.8 }));
      await page.waitForTimeout(150);
      check((await track.evaluate((el) => el.scrollLeft)) > 50, `${tag} carousel: scrolls`);

      const tapTarget = page.locator(".chartcar__slide a").nth(2);
      await tapTarget.scrollIntoViewIfNeeded();
      await tapTarget.click();
      await page.waitForTimeout(250);
      const jumped = await page.evaluate(() => {
        const rect = document.getElementById("chart-3").getBoundingClientRect();
        return { hash: location.hash, top: rect.top, inView: rect.top < innerHeight && rect.bottom > 0 };
      });
      check(jumped.hash === "#chart-3" && jumped.inView, `${tag} carousel: tap jumps to the chart (${jumped.hash}, top ${Math.round(jumped.top)})`);

      const charts = await page.evaluate(() => [...document.querySelectorAll(".art-chart-live--themed")].map((live) => {
        const light = live.querySelector(".art-chart-fallback--light");
        const dark = live.querySelector(".art-chart-fallback--dark");
        return {
          lightShown: getComputedStyle(light).display !== "none",
          darkShown: getComputedStyle(dark).display !== "none",
          loaded: light.naturalWidth > 0 && dark.naturalWidth > 0,
          filter: getComputedStyle(light).filter + getComputedStyle(dark).filter,
        };
      }));
      check(charts.length >= 15, `${tag} charts: ${charts.length} themed charts`);
      check(charts.every((chart) => chart.loaded), `${tag} charts: both renders load`);
      check(charts.every((chart) => (theme === "dark" ? chart.darkShown && !chart.lightShown : chart.lightShown && !chart.darkShown)), `${tag} charts: the ${theme} render is the one shown`);
      check(charts.every((chart) => !/invert/.test(chart.filter)), `${tag} charts: no invert hack`);

      const downloads = await page.evaluate(() => {
        const root = document.querySelector("[data-downloads]");
        const thumbs = [...root.querySelectorAll(".dl__thumb")];
        const buttons = [...root.querySelectorAll(".dl__btn")];
        return {
          thumbs: thumbs.length,
          loaded: thumbs.every((a) => a.querySelector("img").naturalWidth > 0),
          thumbDownload: thumbs.every((a) => a.hasAttribute("download")),
          thumbHrefsAreImages: thumbs.every((a) => /\.(webp|png|jpe?g)$/.test(a.getAttribute("href"))),
          buttons: buttons.map((a) => ({ label: a.querySelector(".dl__label").textContent.trim(), href: a.getAttribute("href"), target: a.getAttribute("target"), rel: a.getAttribute("rel"), download: a.hasAttribute("download"), icon: !!a.querySelector("svg") })),
          plainList: root.querySelectorAll(".preview-files").length,
        };
      });
      const byLabel = Object.fromEntries(downloads.buttons.map((button) => [button.label, button]));
      check(downloads.thumbs >= 4 && downloads.loaded, `${tag} downloads: ${downloads.thumbs} thumbnails of the real images`);
      check(downloads.thumbDownload && downloads.thumbHrefsAreImages, `${tag} downloads: thumbnails download the image`);
      check(byLabel.Dataset?.href.endsWith("wikipedia_franchise_revenue_2026.csv") && byLabel.Dataset.download && byLabel.Dataset.icon, `${tag} downloads: dataset CSV icon button downloads the 2026 file`);
      check(byLabel.Transcript?.download && byLabel.Transcript.icon, `${tag} downloads: transcript icon button downloads`);
      check(byLabel.PDF?.href === "/exports/franchise.pdf" && byLabel.PDF.target === "_blank" && /noopener/.test(byLabel.PDF.rel || "") && byLabel.PDF.icon, `${tag} downloads: PDF opens in a new tab with rel=noopener`);
      check(downloads.plainList === 0, `${tag} downloads: the plain link list is gone`);

      const before = page.url();
      const downloadPromise = page.waitForEvent("download", { timeout: 5000 });
      await page.locator('.dl__btn[href$=".csv"]').click();
      const file = await downloadPromise;
      check(file.suggestedFilename().endsWith(".csv") && page.url() === before, `${tag} downloads: the CSV downloads without leaving the page (${file.suggestedFilename()})`);

      const pages = context.pages().length;
      const popupPromise = context.waitForEvent("page", { timeout: 5000 });
      await page.locator('.dl__btn[href$=".pdf"]').click();
      const popup = await popupPromise;
      const served = await context.request.get(`${origin}/exports/franchise.pdf`);
      check(context.pages().length === pages + 1 && page.url() === before, `${tag} PDF: opens in a new tab and the article stays put`);
      check(served.ok() && /pdf/.test(served.headers()["content-type"] || ""), `${tag} PDF: the file is served as a PDF`);
      await popup.close();

      const cover = await page.evaluate(() => {
        const link = document.querySelector(".franchise-cover a");
        return { href: link?.getAttribute("href"), target: link?.getAttribute("target"), rel: link?.getAttribute("rel"), video: document.querySelectorAll("video").length, mag: [...document.querySelectorAll("a")].filter((a) => /\/mag(\/|$)/.test(a.getAttribute("href") || "")).length, tabs: document.body.innerText.match(/MAGAZINE|LEDGER|TRADE/g) };
      });
      check(cover.href === "/exports/franchise.pdf" && cover.target === "_blank" && /noopener/.test(cover.rel || ""), `${tag} cover: opens the PDF in a new tab`);
      check(cover.video === 0 && cover.mag === 0, `${tag} article: no cover video and no magazine links`);

      const contrast = await page.evaluate(`(${collectContrastFailures.toString()})()`);
      check(contrast.failures.length === 0, `${tag} franchise contrast: ${contrast.failures.length} failures ${JSON.stringify(contrast.failures.slice(0, 3))}`);
      await context.close();
    }
  }
}

{
  const { context, page } = await open(VIEWPORTS[0], "light", "/", { timezoneId: "Asia/Tokyo", fixedTime: new Date("2026-03-01T07:30:00Z") });
  const text = (await page.locator("[data-dateline]").first().textContent()).trim();
  check(text === "Sat, Feb 28, 2026", `date is the Pacific date, not the visitor's or the build's (${text})`);
  await context.close();
}
{
  const { context, page } = await open(VIEWPORTS[1], "dark", "/", { timezoneId: "Pacific/Auckland" });
  const text = (await page.locator("[data-dateline]").first().textContent()).trim();
  const expected = ptDate(new Date());
  check(text === expected, `date is today in Pacific time (${text} vs ${expected})`);
  await context.close();
}

{
  const hosting = JSON.parse(readFileSync(join(ROOT, "firebase.json"), "utf8")).hosting;
  const find = (source) => hosting.redirects.find((item) => item.source === source);
  check(find("/mag/franchise")?.destination === "/exports/franchise.pdf", "old /mag/franchise redirects to the PDF");
  check(find("/mag/:slug")?.destination === "/:slug", "other old /mag/<slug> URLs redirect to the article");
  check(find("/mag")?.destination === "/blog", "old /mag redirects to the reports list");
  check(!existsSync(join(ROOT, "dist/mag.html")) && !existsSync(join(ROOT, "dist/mag")), "the magazine routes are not built");
  check(existsSync(join(ROOT, "dist/exports/franchise.pdf")), "the PDF ships in dist");
  const pdf = readFileSync(join(ROOT, "public/exports/franchise.pdf"));
  check(pdf.subarray(0, 5).toString() === "%PDF-" && pdf.length > 200_000, "franchise.pdf is a real PDF");
}

await browser.close();
await close();
if (failed) {
  console.error(`\n${failed} failed, ${passed} passed`);
  process.exit(1);
}
console.log(`browser OK (${passed} checks)`);
