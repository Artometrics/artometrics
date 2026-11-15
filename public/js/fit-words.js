/*
 * Headlines never break inside a word. [data-fit-words] starts at its CSS size and shrinks in small steps
 * until the longest word fits the box. Hyphenation is the last resort, only when the type is already
 * at its smallest allowed size. Balanced wrapping itself is CSS (text-wrap: balance).
 */
(function () {
  if (window.__fitWords) return;
  var STEP = 0.94;
  var MIN_RATIO = 0.62;

  function overflows(el) {
    return el.scrollWidth > el.clientWidth + 1;
  }

  function fit(el) {
    el.style.fontSize = "";
    el.style.hyphens = "";
    el.removeAttribute("data-hyphenated");
    var base = parseFloat(getComputedStyle(el).fontSize);
    if (!base || !el.clientWidth) return;
    var size = base;
    var guard = 0;
    while (overflows(el) && size > base * MIN_RATIO && guard < 16) {
      size *= STEP;
      el.style.fontSize = size + "px";
      guard += 1;
    }
    if (overflows(el)) {
      el.style.hyphens = "auto";
      el.setAttribute("data-hyphenated", "");
    }
  }

  function fitAll() {
    var els = document.querySelectorAll("[data-fit-words]");
    for (var i = 0; i < els.length; i++) fit(els[i]);
  }

  window.__fitWords = { fitAll: fitAll };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitAll);
  var timer = 0;
  window.addEventListener("resize", function () {
    window.clearTimeout(timer);
    timer = window.setTimeout(fitAll, 80);
  });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", fitAll);
  else fitAll();
  window.addEventListener("load", fitAll);
})();
