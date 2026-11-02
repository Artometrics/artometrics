#!/usr/bin/env node
/**
 * iPhone-sized Chrome pass: native document scroll and real link taps.
 * Magazine: vertical scroll inside a page, horizontal swipe turns the page.
 */
import { chromium, devices } from "playwright";
import { mkdirSync } from "node:fs";

const base = process.env.ASTRO_ORIGIN || "http://127.0.0.1:4321";
const out = "/opt/cursor/artifacts/astro-mobile";
mkdirSync(out, { recursive: true });

const browser = await chromium.launch({
  channel: "chrome",
  headless: true,
  args: ["--no-sandbox"],
});
const context = await browser.newContext({
  ...devices["iPhone 13"],
});
const page = await context.newPage();
const failures = [];

async function shot(name) {
  await page.screenshot({ path: `${out}/${name}.png`, fullPage: false });
}

try {
  await page.goto(`${base}/`, { waitUntil: "networkidle" });
  await page.waitForSelector("text=Editor's picks");
  const before = await page.evaluate(() => window.scrollY);
  await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
  await page.waitForTimeout(200);
  const after = await page.evaluate(() => window.scrollY);
  if (after <= before) failures.push(`home did not scroll (${before} -> ${after})`);
  await shot("01-home");
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.getByRole("link", { name: "Read the report" }).click();
  await page.waitForURL(/artometrics|127\.0\.0\.1:4321\/[a-z0-9-]+$/);
  if (page.url().endsWith("/") || page.url().endsWith(":4321")) failures.push("lead tap stayed on home");
  await shot("02-report");

  const reportUrl = page.url();
  await page.evaluate(() => window.scrollTo(0, 800));
  const scrolled = await page.evaluate(() => window.scrollY);
  if (scrolled < 400) failures.push(`report scroll stuck at ${scrolled}`);
  const ebook = page.getByRole("link", { name: /Read as ebook/i });
  if (await ebook.count()) {
    await ebook.first().click();
    await page.waitForURL(/\/mag\//);
    await shot("03-mag");
    await page.waitForSelector("#book .mag-page, #book");
    await page.waitForTimeout(600);
      const pageBefore = await page.locator("#pg").innerText();
      const box = await page.locator("#view").boundingBox();
      if (!box) failures.push("magazine view missing");
      else {
        const y = box.y + box.height * 0.45;
        const startX = box.x + box.width * 0.82;
        const endX = box.x + box.width * 0.18;
        const client = await context.newCDPSession(page);
        await client.send("Input.dispatchTouchEvent", {
          type: "touchStart",
          touchPoints: [{ x: startX, y }],
        });
        await client.send("Input.dispatchTouchEvent", {
          type: "touchMove",
          touchPoints: [{ x: endX, y }],
        });
        await client.send("Input.dispatchTouchEvent", {
          type: "touchEnd",
          touchPoints: [],
        });
        await page.waitForTimeout(400);
        const pageAfter = await page.locator("#pg").innerText();
        await shot("04-mag-turned");
        if (pageAfter === pageBefore) failures.push(`magazine swipe did not turn (${pageBefore} -> ${pageAfter})`);
      const magPage = page.locator(".mag-page").first();
      if (await magPage.count()) {
        const canScroll = await magPage.evaluate((el) => {
          el.scrollTop = 40;
          return el.scrollTop;
        });
        if (canScroll < 1 && (await magPage.evaluate((el) => el.scrollHeight > el.clientHeight + 8))) {
          failures.push("magazine page could not scroll vertically");
        }
      }
    }
  } else {
    failures.push(`no ebook card on ${reportUrl}`);
  }

  await page.goto(`${base}/blog`, { waitUntil: "domcontentloaded" });
  await page.locator("#report-index a").first().click();
  await page.waitForSelector("h1");
  if (!/\/[a-z0-9-]+$/.test(new URL(page.url()).pathname)) failures.push("blog card tap failed");
  await shot("05-from-blog");

  await page.goto(`${base}/`, { waitUntil: "domcontentloaded" });
  await page.getByRole("button", { name: "Open menu" }).click();
  await page.getByText("Did you know?").waitFor();
  await shot("06-menu-fact");
  const fact = page.locator("#fact-link");
  const factHref = await fact.getAttribute("href");
  await fact.click();
  await page.waitForURL((url) => url.pathname !== "/");
  if (factHref && !page.url().includes(factHref)) failures.push(`fact tap went to ${page.url()} not ${factHref}`);
  await shot("07-fact-report");
} catch (error) {
  failures.push(error instanceof Error ? error.stack || error.message : String(error));
  try { await shot("error"); } catch { /* ignore */ }
}

await browser.close();
if (failures.length) {
  console.error(failures.join("\n\n"));
  process.exit(1);
}
console.log("iPhone scroll and tap checks passed");
