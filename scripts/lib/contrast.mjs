/**
 * Runs inside the page. Returns text elements whose contrast against the effective
 * background is below WCAG AA (4.5, or 3 for large text). Text over images is skipped
 * and counted separately because the background pixels are not knowable from CSS.
 */
export function collectContrastFailures() {
  function parse(color) {
    const m = /rgba?\(([^)]+)\)/.exec(color);
    if (!m) return null;
    const parts = m[1].split(/[,\s/]+/).filter(Boolean).map(Number);
    return { r: parts[0], g: parts[1], b: parts[2], a: parts.length > 3 ? parts[3] : 1 };
  }
  function over(top, bottom) {
    const a = top.a + bottom.a * (1 - top.a);
    if (!a) return { r: 0, g: 0, b: 0, a: 0 };
    return {
      r: (top.r * top.a + bottom.r * bottom.a * (1 - top.a)) / a,
      g: (top.g * top.a + bottom.g * bottom.a * (1 - top.a)) / a,
      b: (top.b * top.a + bottom.b * bottom.a * (1 - top.a)) / a,
      a,
    };
  }
  function lum({ r, g, b }) {
    const f = (v) => {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b);
  }
  function ratio(a, b) {
    const l1 = lum(a);
    const l2 = lum(b);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  }
  function backdrop(el) {
    const layers = [];
    let node = el;
    let overImage = false;
    while (node && node.nodeType === 1) {
      const cs = getComputedStyle(node);
      if (cs.backgroundImage && cs.backgroundImage !== "none") overImage = true;
      const bg = parse(cs.backgroundColor);
      if (bg && bg.a > 0) layers.push(bg);
      if (bg && bg.a >= 1) break;
      node = node.parentElement;
    }
    let base = { r: 255, g: 255, b: 255, a: 1 };
    const rootBg = parse(getComputedStyle(document.documentElement).backgroundColor);
    if (rootBg && rootBg.a > 0) base = rootBg;
    for (let i = layers.length - 1; i >= 0; i--) base = over(layers[i], base);
    return { color: base, overImage };
  }
  function visible(el) {
    const r = el.getBoundingClientRect();
    if (r.width < 1 || r.height < 1) return false;
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const cs = getComputedStyle(n);
      if (cs.display === "none" || cs.visibility === "hidden") return false;
      if (n.hasAttribute("hidden")) return false;
    }
    return true;
  }
  function effectiveOpacity(el) {
    let o = 1;
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) o *= parseFloat(getComputedStyle(n).opacity);
    return o;
  }
  const failures = [];
  let skippedOverImage = 0;
  let checked = 0;
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  const seen = new Set();
  while (walker.nextNode()) {
    const textNode = walker.currentNode;
    const text = (textNode.textContent || "").replace(/\s+/g, " ").trim();
    if (!text) continue;
    const el = textNode.parentElement;
    if (!el || seen.has(el) || /^(SCRIPT|STYLE|NOSCRIPT)$/.test(el.tagName)) continue;
    seen.add(el);
    if (!visible(el)) continue;
    const cs = getComputedStyle(el);
    const bd = backdrop(el);
    if (bd.overImage || el.closest("[data-contrast-skip]")) {
      skippedOverImage += 1;
      continue;
    }
    const fg0 = parse(cs.color);
    if (!fg0) continue;
    const opacity = effectiveOpacity(el);
    const fg = over({ ...fg0, a: fg0.a * opacity }, bd.color);
    const size = parseFloat(cs.fontSize);
    const weight = parseInt(cs.fontWeight, 10) || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    const need = large ? 3 : 4.5;
    const got = ratio(fg, bd.color);
    checked += 1;
    if (got < need) {
      const cls = typeof el.className === "string" ? el.className : "";
      failures.push({
        text: text.slice(0, 60),
        tag: el.tagName.toLowerCase(),
        cls: cls.slice(0, 60),
        ratio: Math.round(got * 100) / 100,
        need,
        fg: cs.color,
        bg: `rgb(${Math.round(bd.color.r)}, ${Math.round(bd.color.g)}, ${Math.round(bd.color.b)})`,
        size,
      });
    }
  }
  return { checked, skippedOverImage, failures };
}
