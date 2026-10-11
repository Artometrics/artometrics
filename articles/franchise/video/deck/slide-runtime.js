/**
 * Franchise deck slide runtime — count-ups, chart settle, AI image load, capture mode.
 * URL: ?capture=1&slide=s001  (Mac mini PNG export — no zoom, final frame state)
 */
(function () {
  const params = new URLSearchParams(window.location.search);
  const capture = params.get("capture") === "1";
  const slideId = params.get("slide") || (location.hash || "").replace(/^#/, "");
  const freeze = params.get("freeze") === "1" || capture;

  if (capture && slideId) {
    document.body.classList.add("deck--capture");
    const target = document.getElementById(slideId);
    if (target) target.classList.add("is-active");
  }

  const WORD_ONES = {
    zero: 0,
    one: 1,
    two: 2,
    three: 3,
    four: 4,
    five: 5,
    six: 6,
    seven: 7,
    eight: 8,
    nine: 9,
    ten: 10,
    eleven: 11,
    twelve: 12,
    thirteen: 13,
    fourteen: 14,
    fifteen: 15,
    sixteen: 16,
    seventeen: 17,
    eighteen: 18,
    nineteen: 19,
    twenty: 20,
    thirty: 30,
    forty: 40,
    fifty: 50,
    sixty: 60,
    seventy: 70,
    eighty: 80,
    ninety: 90,
  };

  function parseSpokenNumber(raw) {
    if (!raw || !raw.trim()) return null;
    const s = raw.trim().toLowerCase().replace(/,/g, "");
    if (/^\d+(\.\d+)?$/.test(s)) return parseFloat(s);
    const point = s.match(/^(.+?)\s+point\s+(.+)$/);
    if (point) {
      const whole = parseSpokenNumber(point[1]);
      const frac = parseSpokenNumber(point[2]);
      if (whole != null && frac != null) return whole + frac / Math.pow(10, String(frac).length);
    }
    if (s.includes("hundred")) {
      const parts = s.split(/\s+and\s+/);
      let total = 0;
      for (const part of parts) {
        const p = part.trim();
        const hm = p.match(/^(.+?)\s+hundred(?:\s+and\s+(.+))?$/);
        if (hm) {
          const mult = WORD_ONES[hm[1]] ?? (hm[1] === "one" ? 1 : parseFloat(hm[1]));
          if (mult == null || Number.isNaN(mult)) return null;
          total += mult * 100;
          if (hm[2]) {
            const rest = WORD_ONES[hm[2].trim()] ?? parseSpokenNumber(hm[2].trim());
            if (rest != null) total += rest;
          }
        } else {
          const w = WORD_ONES[p];
          if (w != null) total += w;
        }
      }
      return total || null;
    }
    if (WORD_ONES[s] != null) return WORD_ONES[s];
    return null;
  }

  function formatNumber(n) {
    if (Number.isInteger(n)) return n.toLocaleString("en-US");
    return n.toLocaleString("en-US", { maximumFractionDigits: 2 });
  }

  function runCountUps() {
    document.querySelectorAll(".count-up[data-count-up]").forEach((el) => {
      const raw = el.getAttribute("data-count-up");
      const target = parseSpokenNumber(raw);
      if (target == null) return;
      const duration = freeze ? 0 : 1400;
      const start = performance.now();
      function frame(now) {
        const t = duration === 0 ? 1 : Math.min(1, (now - start) / duration);
        const ease = 1 - Math.pow(1 - t, 3);
        el.textContent = formatNumber(target * ease);
        if (t < 1) requestAnimationFrame(frame);
        else el.textContent = formatNumber(target);
      }
      if (freeze) el.textContent = formatNumber(target);
      else requestAnimationFrame(frame);
    });
  }

  function bindAiImages() {
    document.querySelectorAll(".ai-image").forEach((img) => {
      img.addEventListener("load", () => img.classList.add("is-loaded"));
      img.addEventListener("error", () => img.classList.remove("is-loaded"));
      if (img.complete && img.naturalWidth > 0) img.classList.add("is-loaded");
    });
  }

  function waitChartsReady() {
    return new Promise((resolve) => {
      const iframes = document.querySelectorAll(".slide.is-active .chart-embed, .deck--capture .chart-embed");
      if (!iframes.length) {
        resolve();
        return;
      }
      const ms = freeze ? 1600 : 1800;
      setTimeout(resolve, ms);
    });
  }

  window.franchiseDeckReady = new Promise((resolve) => {
    document.addEventListener("DOMContentLoaded", () => {
      runCountUps();
      bindAiImages();
      waitChartsReady().then(() => {
        document.body.setAttribute("data-deck-ready", "1");
        resolve();
      });
    });
  });
})();
