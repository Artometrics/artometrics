/*
 * Jump to #hash targets (citation links, "On this page", chart anchors) and stay on target.
 * Lazy images below the fold load after the jump and stretch the page, which pushes the
 * target away. We scroll, then re-correct on every layout change for a short window, and
 * stop as soon as the reader scrolls or presses a key.
 */
(function () {
  var SETTLE_MS = 700;
  var MAX_MS = 3000;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)");
  var session = null;

  function targetFor(hash) {
    if (!hash || hash.length < 2) return null;
    try {
      return document.getElementById(decodeURIComponent(hash.slice(1)));
    } catch (error) {
      return null;
    }
  }

  function align(el) {
    var margin = parseFloat(getComputedStyle(el).scrollMarginTop) || 0;
    var delta = el.getBoundingClientRect().top - margin;
    if (Math.abs(delta) > 1) window.scrollBy({ top: delta, left: 0, behavior: "instant" });
  }

  function highlight(el) {
    el.classList.remove("anchor-flash");
    void el.offsetWidth;
    el.classList.add("anchor-flash");
    window.setTimeout(function () { el.classList.remove("anchor-flash"); }, reduce.matches ? 2400 : 2000);
  }

  function stop() {
    if (!session) return;
    session.observer.disconnect();
    window.clearTimeout(session.settle);
    window.clearTimeout(session.cap);
    ["wheel", "touchstart", "keydown", "mousedown"].forEach(function (name) {
      window.removeEventListener(name, stop, true);
    });
    document.removeEventListener("load", onLoad, true);
    session = null;
  }

  function onLoad(event) {
    if (session && event.target && event.target.tagName === "IMG") session.fix();
  }

  function follow(el) {
    stop();
    var current = { observer: null, settle: 0, cap: 0, fix: null };
    session = current;
    current.fix = function () {
      if (session !== current) return;
      align(el);
      window.clearTimeout(current.settle);
      current.settle = window.setTimeout(stop, SETTLE_MS);
    };
    current.observer = new ResizeObserver(current.fix);
    current.observer.observe(document.body);
    current.cap = window.setTimeout(stop, MAX_MS);
    ["wheel", "touchstart", "keydown", "mousedown"].forEach(function (name) {
      window.addEventListener(name, stop, { capture: true, passive: true });
    });
    document.addEventListener("load", onLoad, true);
    current.fix();
  }

  function jump(el) {
    follow(el);
    highlight(el);
    if (!el.hasAttribute("tabindex")) el.setAttribute("tabindex", "-1");
    el.focus({ preventScroll: true });
  }

  document.addEventListener("click", function (event) {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    var link = event.target.closest && event.target.closest("a[href^='#']");
    if (!link) return;
    var el = targetFor(link.getAttribute("href"));
    if (!el) return;
    event.preventDefault();
    if (location.hash !== link.getAttribute("href")) history.pushState(null, "", link.getAttribute("href"));
    jump(el);
  });

  function onHash() {
    var el = targetFor(location.hash);
    if (el) jump(el);
  }

  window.addEventListener("hashchange", onHash);
  if (location.hash) {
    if (document.readyState === "complete") onHash();
    else window.addEventListener("load", onHash, { once: true });
  }
})();
