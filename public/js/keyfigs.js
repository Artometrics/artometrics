/*
 * Fast facts: count the number up once when the box scrolls into view.
 * Skipped for prefers-reduced-motion, for years, and for values with more than one number.
 * The server-rendered text is always the final text; the figure is hidden until it scrolls into view,
 * then counts up to that text.
 */
(function () {
  if (window.__keyfigsCount) return;
  window.__keyfigsCount = true;
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || typeof IntersectionObserver !== "function") return;

  var PATTERN = /^([^0-9]*?)(\d[\d,]*(?:\.\d+)?)(\D*)$/;

  function parse(text) {
    var m = PATTERN.exec(text.trim());
    if (!m) return null;
    var raw = m[2];
    var plain = raw.replace(/,/g, "");
    var value = parseFloat(plain);
    if (!isFinite(value) || value === 0) return null;
    if (/^\d{4}$/.test(plain) && value >= 1500 && value <= 2100 && !m[1] && !m[3]) return null;
    var dot = raw.indexOf(".");
    return {
      prefix: m[1],
      suffix: m[3],
      value: value,
      decimals: dot === -1 ? 0 : raw.length - dot - 1,
      commas: raw.indexOf(",") !== -1,
      final: text,
    };
  }

  function format(parsed, n) {
    var fixed = n.toFixed(parsed.decimals);
    if (parsed.commas) {
      var parts = fixed.split(".");
      parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      fixed = parts.join(".");
    }
    return parsed.prefix + fixed + parsed.suffix;
  }

  function run(el, parsed) {
    var start = null;
    el.setAttribute("data-count-lock", "");
    el.textContent = format(parsed, 0);
    el.style.opacity = "";
    var duration = 1100;
    function frame(now) {
      if (start === null) start = now;
      var t = Math.min(1, (now - start) / duration);
      var eased = 1 - Math.pow(1 - t, 3);
      el.textContent = t >= 1 ? parsed.final : format(parsed, parsed.value * eased);
      if (t < 1) window.requestAnimationFrame(frame);
      else {
        el.style.minWidth = "";
        el.removeAttribute("data-count-lock");
      }
    }
    window.requestAnimationFrame(frame);
  }

  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        var parsed = entry.target.__count;
        if (parsed) run(entry.target, parsed);
      });
    },
    { threshold: 0.45 }
  );

  function init() {
    var els = document.querySelectorAll("[data-count]");
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      if (el.__count !== undefined) continue;
      var parsed = parse(el.textContent || "");
      el.__count = parsed;
      if (!parsed) continue;
      el.style.minWidth = el.getBoundingClientRect().width + "px";
      el.style.opacity = "0";
      io.observe(el);
    }
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
