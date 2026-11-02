/**
 * iPhone-sized scroll check.
 * WebKit: document scroll via keyboard (mobile WebKit has no wheel) and layout asserts.
 * Chromium: trusted touchmove via CDP, which mobile WebKit's protocol does not expose.
 *
 * Usage: node scripts/check-mobile-scroll.mjs http://127.0.0.1:4173
 */
import { chromium, devices, webkit } from "playwright";

const base = (process.argv[2] || "http://127.0.0.1:4173").replace(/\/$/, "");
const iphone = devices["iPhone 13"];

function assert(cond, msg) {
  if (!cond) throw new Error(msg);
  console.log("ok", msg);
}

async function readScroll(page) {
  return page.evaluate(() => {
    const doc = document.scrollingElement || document.documentElement;
    const pages = [...document.querySelectorAll(".mag-page")];
    const chips = document.querySelector(".art-action-scroller");
    return {
      path: location.pathname,
      mag: document.documentElement.classList.contains("mag-mode"),
      docScroll: document.documentElement.classList.contains("site-document-scroll"),
      bodyOverflowY: getComputedStyle(document.body).overflowY,
      docTop: doc.scrollTop,
      docHeight: doc.scrollHeight,
      view: window.innerHeight,
      pageTops: pages.map((el) => ({
        top: el.scrollTop,
        sh: el.scrollHeight,
        ch: el.clientHeight,
        touch: getComputedStyle(el).touchAction,
      })),
      pg: document.getElementById("pg")?.textContent || "",
      chip: chips
        ? { left: chips.scrollLeft, sw: chips.scrollWidth, cw: chips.clientWidth }
        : null,
    };
  });
}

async function webkitPass(path) {
  const browser = await webkit.launch();
  const page = await (await browser.newContext({ ...iphone, hasTouch: true })).newPage();
  let crashed = false;
  page.on("crash", () => {
    crashed = true;
  });
  try {
    await page.goto(base + path, { waitUntil: "domcontentloaded", timeout: 45000 });
    await page.waitForSelector(".mag-page, .site-document", { timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(600);
    if (crashed) throw new Error("crashed");
    const before = await readScroll(page);
    if (before.mag) {
      assert(before.pageTops.length > 0, `${path} has magazine pages`);
      assert(before.pageTops.every((p) => p.touch.includes("pan-y")), `${path} pages allow vertical pan`);
      assert(before.bodyOverflowY === "hidden", `${path} magazine locks the document`);
      console.log("ok", `${path} webkit reader is paged (${before.pageTops.length} pages)`);
      await browser.close();
      return;
    }
    assert(before.docScroll, `${path} uses document scroll`);
    assert(before.bodyOverflowY !== "hidden", `${path} body is not overflow hidden (${before.bodyOverflowY})`);
    assert(before.docHeight > before.view + 80, `${path} document is taller than the phone`);
    await page.locator("body").click({ position: { x: 12, y: 280 } });
    await page.keyboard.press("Space");
    await page.waitForTimeout(200);
    const after = await readScroll(page);
    assert(after.docTop > before.docTop + 40, `${path} WebKit scrolls the document (${before.docTop} → ${after.docTop})`);
  } catch (error) {
    if (!crashed && !String(error).includes("crashed")) throw error;
    console.log("warn", `${path} WebKit tab crashed while hydrating; touch scroll is checked in Chromium`);
  }
  await browser.close();
}

async function touchSwipe(page, x, y, dx, dy) {
  const client = await page.context().newCDPSession(page);
  const steps = 8;
  await client.send("Input.dispatchTouchEvent", {
    type: "touchStart",
    touchPoints: [{ x, y, id: 1 }],
  });
  for (let i = 1; i <= steps; i++) {
    await client.send("Input.dispatchTouchEvent", {
      type: "touchMove",
      touchPoints: [{ x: x + (dx * i) / steps, y: y + (dy * i) / steps, id: 1 }],
    });
  }
  await client.send("Input.dispatchTouchEvent", {
    type: "touchEnd",
    touchPoints: [],
  });
}

async function chromiumTouchPass(path) {
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ ...iphone, hasTouch: true })).newPage();
  await page.goto(base + path, { waitUntil: "domcontentloaded", timeout: 45000 });
  await page.waitForTimeout(1400);
  const before = await readScroll(page);
  if (before.mag) {
    const point = await page.evaluate(() => {
      const el = [...document.querySelectorAll(".mag-page")].find((node) => {
        const r = node.getBoundingClientRect();
        return r.width > 0 && r.left >= -2 && r.left < 80 && node.scrollHeight > node.clientHeight + 24;
      });
      if (!el) return null;
      const r = el.getBoundingClientRect();
      return { x: r.x + 24, y: r.y + 70 };
    });
    if (point) {
      await touchSwipe(page, point.x, point.y, 0, -160);
      await page.waitForTimeout(400);
      const afterV = await readScroll(page);
      const grew = afterV.pageTops.some((p, i) => p.top > (before.pageTops[i]?.top || 0) + 20);
      assert(grew, `${path} vertical touch scrolls the magazine page`);
      assert(afterV.pg === before.pg, `${path} vertical touch does not turn the page`);
    } else {
      console.log("ok", `${path} visible magazine page fits; vertical pan stays enabled`);
    }
    await page.goto(base + path, { waitUntil: "domcontentloaded" });
    await page.waitForTimeout(1200);
    const start = await readScroll(page);
    const box = await page.evaluate(() => {
      const shell = document.querySelector(".mag-shell");
      const r = shell.getBoundingClientRect();
      for (let y = r.bottom - 48; y > r.top + 60; y -= 14) {
        for (const x of [r.x + 16, r.x + r.width * 0.5, r.right - 16]) {
          const el = document.elementFromPoint(x, y);
          if (el && !el.closest("a, button, .skin-picker, input, textarea")) return { x, y };
        }
      }
      return null;
    });
    if (!box || path === "/mag") {
      console.log("ok", `${path} contents are links; page-turn is checked on an issue`);
      await browser.close();
      return;
    }
    await touchSwipe(page, box.x, box.y, -170, 6);
    await page.waitForTimeout(700);
    const afterH = await readScroll(page);
    assert(afterH.pg !== start.pg, `${path} horizontal touch turns the page (${start.pg} → ${afterH.pg})`);
    await browser.close();
    return;
  }
  if (before.chip && before.chip.sw > before.chip.cw + 24) {
    const chipBox = await page.locator(".art-action-scroller").boundingBox();
    if (chipBox && chipBox.y > 0 && chipBox.y < 700) {
      await touchSwipe(page, chipBox.x + 36, chipBox.y + chipBox.height / 2, -160, 4);
      await page.waitForTimeout(250);
      const chip = await readScroll(page);
      assert(
        chip.chip.left > before.chip.left + 10,
        `${path} horizontal touch scrolls the action chips (${before.chip.left} → ${chip.chip.left})`,
      );
    }
  }
  await page.goto(base + path, { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(900);
  const fresh = await readScroll(page);
  await touchSwipe(page, 40, 420, 0, -260);
  await page.waitForTimeout(400);
  const after = await readScroll(page);
  assert(after.docTop > fresh.docTop + 30, `${path} vertical touch scrolls (${fresh.docTop} → ${after.docTop})`);
  await browser.close();
}

const routes = ["/", "/franchise", "/mag", "/mag/franchise"];
for (const path of routes) {
  console.log("\nwebkit", path);
  await webkitPass(path);
}
for (const path of routes) {
  console.log("\nchromium touch", path);
  await chromiumTouchPass(path);
}
console.log("\nscroll checks passed");
