#!/usr/bin/env node
/**
 * Studio tools work with no account and no server: drive each one in a browser.
 * Run `npm run build` first.
 *
 *   npm run test:studio
 */
import { readFileSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { chromium } from "playwright";
import sharp from "sharp";
import { startStaticServer } from "./lib/static-server.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
let failed = 0;
let passed = 0;
const check = (ok, message) => {
  if (ok) passed += 1;
  else {
    failed += 1;
    console.error("FAIL", message);
  }
};

const { origin, close } = await startStaticServer(join(ROOT, "dist"));
const browser = await chromium.launch();
const context = await browser.newContext({ viewport: { width: 390, height: 844 }, acceptDownloads: true });
const page = await context.newPage();
const errors = [];
page.on("pageerror", (error) => errors.push(error.message));
const go = (path) => page.goto(origin + path, { waitUntil: "networkidle" });

const PATHS = [
  "/studio",
  "/tools/aftercare",
  "/tools/aftercare/journal",
  "/tools/aftercare/tarot",
  "/tools/aftercare/tools",
  "/tools/aftercare/track",
  "/tools/palette",
  "/tools/palette/analyze",
  "/tools/samples",
  "/tools/samples/record",
  "/tools/twilda",
  "/tools/twilda/journal",
  "/tools/twilda/reference",
];

for (const path of PATHS) {
  await go(path);
  const text = await page.locator("main, body").first().innerText();
  check(!/sign in|log in|login required/i.test(await page.locator(".tool-page, .page").first().innerText()), `${path} has no sign-in wall`);
  check(!(await page.locator('a[href^="/login"]').count()), `${path} links nowhere near /login`);
  const overflow = await page.evaluate(() => document.documentElement.scrollWidth - window.innerWidth);
  check(overflow <= 1, `${path} has no horizontal overflow at 390px (${overflow}px)`);
  if (path.startsWith("/tools/") && !path.endsWith("/aftercare")) {
    check((await page.locator("[data-mount] *").count()) > 3, `${path} mounts its tool`);
  }
  void text;
}

await go("/tools/aftercare/journal");
await page.fill("textarea", "Went well, but I am tired.");
await page.click('button:has-text("Save entry")');
check((await page.locator(".tool-entry").count()) === 1, "journal saves an entry");
await page.reload({ waitUntil: "networkidle" });
check((await page.locator(".tool-entry").count()) === 1, "journal entry survives a reload");

await go("/tools/aftercare/tarot");
await page.selectOption("select", "three");
await page.click("button:has-text('Draw')");
check((await page.locator(".tarot-card").count()) === 3, "tarot draws three cards");

await go("/tools/aftercare/track");
await page.click('button:has-text("Log today")');
check((await page.locator(".track-line").count()) === 1, "tracker logs today");

await go("/tools/aftercare/tools");
await page.click("button:has-text('Start')");
check(/breathe in/i.test(await page.locator(".breath__label").innerText()), "breathing pacer starts");
await page.click("button:has-text('Stop')");

await go("/tools/twilda");
await page.click('button:has-text("New draft")');
await page.fill(".tool-text--draft", "one two three four");
await page.waitForTimeout(600);
check(/4 words/.test(await page.locator(".drafts__main .tool-note").innerText()), "draft counts words");
const [md] = await Promise.all([page.waitForEvent("download"), page.click('button:has-text("Export Markdown")')]);
check(md.suggestedFilename().endsWith(".md"), "draft exports Markdown");

await go("/tools/twilda/reference");
await page.fill("textarea", "A line worth keeping");
await page.click('button:has-text("Add to shelf")');
check((await page.locator(".tool-entry").count()) === 1, "reference shelf stores an item");

await go("/tools/palette");
const png = await sharp({ create: { width: 64, height: 64, channels: 3, background: "#ff3d8a" } })
  .composite([{ input: await sharp({ create: { width: 32, height: 64, channels: 3, background: "#0047ff" } }).png().toBuffer(), left: 0, top: 0 }])
  .png()
  .toBuffer();
await page.setInputFiles('input[type="file"]', { name: "test.png", mimeType: "image/png", buffer: png });
await page.waitForSelector(".pal-swatch");
const swatchText = await page.locator(".pal-swatch").allInnerTexts();
check(swatchText.some((t) => /#0047FF/i.test(t)) && swatchText.some((t) => /#FF3D8A/i.test(t)), "palette finds the two real colors in the image");
const [css] = await Promise.all([page.waitForEvent("download"), page.click('button:has-text("CSS variables")')]);
check(css.suggestedFilename().endsWith(".css"), "palette exports CSS");

await go("/tools/samples");
const sr = 8000;
const wav = Buffer.alloc(44 + sr * 2);
wav.write("RIFF", 0); wav.writeUInt32LE(36 + sr * 2, 4); wav.write("WAVE", 8); wav.write("fmt ", 12);
wav.writeUInt32LE(16, 16); wav.writeUInt16LE(1, 20); wav.writeUInt16LE(1, 22); wav.writeUInt32LE(sr, 24);
wav.writeUInt32LE(sr * 2, 28); wav.writeUInt16LE(2, 32); wav.writeUInt16LE(16, 34); wav.write("data", 36); wav.writeUInt32LE(sr * 2, 40);
for (let i = 0; i < sr; i++) wav.writeInt16LE(Math.round(Math.sin((i / sr) * 440 * Math.PI * 2) * 12000), 44 + i * 2);
await page.setInputFiles('input[type="file"]', { name: "tone.wav", mimeType: "audio/wav", buffer: wav });
await page.waitForFunction(() => /1\.00 s/.test(document.querySelector("[data-mount]").textContent));
const [out] = await Promise.all([page.waitForEvent("download"), page.click('button:has-text("Export WAV")')]);
check(out.suggestedFilename() === "tone.wav", "sample maker exports a WAV");
const exported = readFileSync(await out.path());
check(exported.slice(0, 4).toString() === "RIFF" && exported.length > 8000, "exported WAV has audio data");

check(errors.length === 0, `no page errors: ${errors.join("; ")}`);
await browser.close();
await close();
console.log(`${passed} passed, ${failed} failed`);
process.exit(failed ? 1 : 0);
