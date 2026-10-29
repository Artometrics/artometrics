#!/usr/bin/env node
/** Run all AEO/static discovery generators after content build. */
import { execSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "../..");
const run = (cmd) => execSync(cmd, { cwd: ROOT, stdio: "inherit" });

run("node scripts/content-os/generate-llms-txt.mjs");
run("node scripts/content-os/generate-sitemap.mjs");
run("node scripts/content-os/generate-rss.mjs");
console.log("AEO pack complete.");
