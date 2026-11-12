/*
 * Fit a single line of display type to the width of its box.
 * <span data-fit data-fit-max="0.4"> inside a positioned parent: font-size is solved so the
 * text spans the parent's content width. data-fit-max caps the size as a fraction of the box width;
 * when the cap wins, letter-spacing is opened so the word still runs border to border.
 */
(function () {
  if (window.__fitText) return;
  var MAX_TRACK = 0.3;

  function box(el) {
    var parent = el.closest("[data-fit-box]") || el.parentElement;
    var cs = getComputedStyle(parent);
    return parent.clientWidth - parseFloat(cs.paddingLeft) - parseFloat(cs.paddingRight);
  }

  function fit(el) {
    var width = box(el);
    if (!width || width < 20) return;
    var cap = parseFloat(el.getAttribute("data-fit-max") || "0.6") * width;
    var floor = parseFloat(el.getAttribute("data-fit-min") || "10");
    el.style.letterSpacing = "0";
    el.style.marginRight = "0";
    el.style.whiteSpace = "nowrap";
    el.style.display = "inline-block";
    el.style.fontSize = "100px";
    var natural = el.getBoundingClientRect().width;
    if (!natural) return;
    var size = Math.max(floor, (100 * width) / natural);
    var capped = size > cap;
    if (capped) size = cap;
    el.style.fontSize = size + "px";
    if (capped && el.getAttribute("data-fit-track") !== "0") {
      var used = el.getBoundingClientRect().width;
      var chars = Math.max(1, (el.textContent || "").trim().length);
      var extra = (width - used) / chars;
      var track = Math.min(extra, MAX_TRACK * size);
      if (track > 0) {
        el.style.letterSpacing = track + "px";
        el.style.marginRight = -track + "px";
      }
    }
    el.setAttribute("data-fit-ready", "");
  }

  function fitAll(root) {
    if (!root || typeof root.querySelectorAll !== "function") root = document;
    var els = root.querySelectorAll("[data-fit]");
    for (var i = 0; i < els.length; i++) fit(els[i]);
  }

  var seen = typeof ResizeObserver === "function" ? new ResizeObserver(function (entries) {
    for (var i = 0; i < entries.length; i++) {
      var els = entries[i].target.querySelectorAll("[data-fit]");
      for (var j = 0; j < els.length; j++) fit(els[j]);
    }
  }) : null;

  function observe() {
    var els = document.querySelectorAll("[data-fit]");
    for (var i = 0; i < els.length; i++) {
      var parent = els[i].closest("[data-fit-box]") || els[i].parentElement;
      if (seen && !parent.__fitSeen) {
        parent.__fitSeen = true;
        seen.observe(parent);
      }
    }
    fitAll();
  }

  window.__fitText = { fitAll: fitAll };
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitAll);
  window.addEventListener("resize", function () { fitAll(); });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", observe);
  else observe();
  window.addEventListener("load", fitAll);
})();
