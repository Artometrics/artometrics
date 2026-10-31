#!/usr/bin/env node
/**
 * Generate src/generated/sources.json from magazine/issues.json.
 * npm run content calls this. npm run sources rebuilds the catalog alone.
 */
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { writeSourcesCatalog } from "./lib/sources-catalog.mjs";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
writeSourcesCatalog(ROOT);
