#!/usr/bin/env node
/**
 * Walk dist HTML and fail if an internal link or local asset is missing.
 * Firebase cleanUrls: /blog is dist/blog.html.
 */
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join, dirname, resolve, extname } from "node:path";

const root = resolve("dist");
const htmlFiles = [];

function walk(dir) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) walk(full);
    else if (name.endsWith(".html")) htmlFiles.push(full);
  }
}
walk(root);

function fileForPath(urlPath) {
  let clean = urlPath.split("#")[0].split("?")[0];
  if (clean.length > 1) clean = clean.replace(/\/+$/, "");
  if (!clean || clean === "/") return join(root, "index.html");
  const rel = clean.replace(/^\//, "");
  if (extname(rel)) return join(root, rel);
  return join(root, `${rel}.html`);
}

const missing = [];
const attr = /(?:href|src)="([^"]+)"/g;

for (const file of htmlFiles) {
  const html = readFileSync(file, "utf8");
  let match;
  while ((match = attr.exec(html))) {
    let raw = match[1].trim();
    if (!raw || raw.startsWith("#") || raw.startsWith("mailto:") || raw.startsWith("tel:") || raw.startsWith("data:") || raw.startsWith("javascript:")) continue;
    if (/^https?:\/\//i.test(raw)) continue;
    if (raw.startsWith("//")) continue;
    let path = raw;
    if (!path.startsWith("/")) {
      const base = dirname(file);
      path = "/" + resolve(base, path).slice(root.length).replaceAll("\\", "/").replace(/^\//, "");
    }
    const target = fileForPath(path);
    if (!existsSync(target)) {
      missing.push(`${file.slice(root.length)} -> ${raw}`);
    }
  }
}

const unique = [...new Set(missing)];
console.log(`Checked ${htmlFiles.length} HTML files`);
console.log(`Missing internal targets: ${unique.length}`);
for (const row of unique.slice(0, 80)) console.log(row);
if (unique.length > 80) console.log(`… ${unique.length - 80} more`);
if (unique.length) process.exit(1);
