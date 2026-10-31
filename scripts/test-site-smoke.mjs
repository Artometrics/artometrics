#!/usr/bin/env node
/**
 * HTTP smoke against a running Expo/Netlify preview.
 *
 * Usage:
 *   PREVIEW_URL=http://127.0.0.1:8082 npm run test:smoke
 *   PREVIEW_URL=https://artometrics.com npm run test:smoke
 */
const base = (process.env.PREVIEW_URL || "http://127.0.0.1:8082").replace(/\/$/, "");

const paths = [
  "/",
  "/newsletter",
  "/library",
  "/library/reference",
  "/tools/aftercare",
  "/studio",
  "/llms.txt",
  "/llms-full.txt",
  "/rss.xml",
  "/podcast.xml",
  "/robots.txt",
  "/resources",
  "/sources",
  "/press",
  "/downloads",
  "/welcome",
  "/blog",
  "/beyonce",
  "/trademarks",
  "/lyrics",
  "/caesar",
];

let failed = 0;
for (const p of paths) {
  const url = `${base}${p}`;
  try {
    const res = await fetch(url, { redirect: "follow" });
    const ok = res.status >= 200 && res.status < 400;
    console.log(ok ? "✓" : "✗", res.status, p);
    if (!ok) failed += 1;
  } catch (e) {
    console.log("✗", "ERR", p, e instanceof Error ? e.message : e);
    failed += 1;
  }
}

if (failed) {
  console.error(`smoke failures: ${failed} (is the server up at ${base}?)`);
  process.exit(1);
}
console.log("smoke OK", base);
