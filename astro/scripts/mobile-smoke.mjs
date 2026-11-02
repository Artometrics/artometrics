import { chromium, devices } from "playwright";

const base = process.env.BASE_URL || "http://127.0.0.1:4321";
const iphone = devices["iPhone 13"];
const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ ...iphone });
const page = await context.newPage();
const notes = [];

async function shot(name) {
  const file = `/tmp/${name}.png`;
  await page.screenshot({ path: file, fullPage: false });
  notes.push(file);
}

page.on("pageerror", (error) => notes.push(`pageerror ${error.message}`));

await page.goto(base + "/", { waitUntil: "networkidle" });
const before = await page.evaluate(() => window.scrollY);
await page.evaluate(() => window.scrollTo(0, 900));
await page.waitForTimeout(200);
const after = await page.evaluate(() => window.scrollY);
if (after <= before) throw new Error(`home did not scroll (${before} -> ${after})`);
notes.push(`home scroll ${before} -> ${after}`);
await shot("astro-home-iphone");

const report = page.locator("a[href^='/']").filter({ hasText: /./ }).first();
await page.locator("a.btn-pink").click();
await page.waitForLoadState("networkidle");
const reportUrl = page.url();
if (!reportUrl.includes(base) || reportUrl === base + "/") throw new Error(`report tap stayed at ${reportUrl}`);
notes.push(`opened ${reportUrl}`);
await page.evaluate(() => window.scrollTo(0, 700));
await page.waitForTimeout(150);
const reportScroll = await page.evaluate(() => window.scrollY);
if (reportScroll < 200) throw new Error(`report did not scroll (${reportScroll})`);
notes.push(`report scroll ${reportScroll}`);
await shot("astro-report-iphone");

const ebook = page.locator("a.ebook-entry");
if (await ebook.count()) {
  await ebook.first().click();
  await page.waitForLoadState("domcontentloaded");
  notes.push(`ebook ${page.url()}`);
  await page.waitForFunction(() => (document.getElementById("tot")?.textContent || "").includes("/"), null, { timeout: 8000 });
  const beforePage = await page.locator("#pg").innerText();
  const box = await page.locator("#view").boundingBox();
  if (!box) throw new Error("magazine view missing");
  await page.touchscreen.tap(box.x + box.width * 0.8, box.y + box.height * 0.5);
  await page.waitForTimeout(400);
  let afterPage = await page.locator("#pg").innerText();
  if (afterPage === beforePage) {
    await page.keyboard.press("ArrowRight");
    await page.waitForTimeout(300);
    afterPage = await page.locator("#pg").innerText();
  }
  const scrollable = await page.evaluate(() => {
    const pageEl = document.querySelector(".mag-page");
    if (!pageEl) return "no-page";
    const style = getComputedStyle(pageEl);
    return `${style.overflowY} h=${pageEl.clientHeight} scroll=${pageEl.scrollHeight}`;
  });
  notes.push(`turn ${beforePage}->${afterPage} ${scrollable}`);
  if (afterPage === beforePage) throw new Error(`magazine page did not turn (${beforePage})`);
  await shot("astro-mag-iphone");
}

await page.goto(base + "/blog", { waitUntil: "domcontentloaded" });
const blogLinks = await page.locator("a[href^='/']").count();
if (blogLinks < 50) throw new Error(`blog index looks thin (${blogLinks} links)`);
notes.push(`blog links ${blogLinks}`);

await browser.close();
console.log(notes.join("\n"));
