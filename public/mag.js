/* Page-flip reader for the Artometrics magazine edition.
   Boot/destroy so Expo client navigations do not stack listeners. */
(function () {
  var cleanups = [];
  var resizeTimer = 0;
  var hintTimer = 0;
  var suppressClick = false;

  function on(target, type, fn, opts) {
    target.addEventListener(type, fn, opts);
    cleanups.push(function () {
      target.removeEventListener(type, fn, opts);
    });
  }

  function destroy() {
    cleanups.splice(0).forEach(function (fn) {
      fn();
    });
    clearTimeout(resizeTimer);
    clearTimeout(hintTimer);
  }

  function boot() {
    destroy();
    var v = document.getElementById("view");
    var b = document.getElementById("book");
    var fold = document.getElementById("fold");
    var pg = document.getElementById("pg");
    var tot = document.getElementById("tot");
    var bar = document.getElementById("bar");
    var hint = document.getElementById("hint");
    if (!v || !b || !fold || !pg || !tot || !bar || !hint) return;

    var W = 0;
    var G = 40;
    var n = 1;
    var i = 0;

    function layout() {
      var keep = i / Math.max(1, n - 1);
      W = v.clientWidth;
      G = 40;
      var cs = getComputedStyle(b);
      var pad = parseFloat(cs.paddingLeft) + parseFloat(cs.paddingRight);
      b.style.columnWidth = W - pad + "px";
      b.style.columnGap = G + pad + "px";
      b.style.width = W + "px";
      b.classList.add("noanim");
      var last = b.lastElementChild;
      if (last) {
        n = Math.max(
          1,
          Math.ceil((last.getBoundingClientRect().right - b.getBoundingClientRect().left + 1) / (W + G)),
        );
      } else {
        n = Math.max(1, Math.round(b.scrollWidth / (W + G)));
      }
      i = Math.min(n - 1, Math.round(keep * (n - 1)) || 0);
      go(i, 0);
      requestAnimationFrame(function () {
        b.classList.remove("noanim");
      });
    }

    function reveal() {
      var L = b.getBoundingClientRect().left;
      b.querySelectorAll("figure,.fade").forEach(function (el) {
        var x = el.getBoundingClientRect().left - L;
        var p = Math.floor((x + 1) / (W + G));
        if (p === i) el.classList.add("on");
      });
    }

    function go(k, dir) {
      i = Math.max(0, Math.min(n - 1, k));
      b.style.transform = "translate3d(" + -i * (W + G) + "px,0,0)";
      pg.textContent = String(i + 1);
      tot.textContent = i + 1 + " / " + n;
      bar.style.width = ((i + 1) / n) * 100 + "%";
      if (dir) {
        fold.className = "";
        void fold.offsetWidth;
        fold.className = dir > 0 ? "go-n" : "go-p";
      }
      setTimeout(reveal, dir ? 380 : 50);
      try {
        history.replaceState(null, "", location.pathname + location.search + "#p" + (i + 1));
      } catch (e) {}
    }

    function next() {
      if (i < n - 1) {
        go(i + 1, 1);
        hide();
      }
    }
    function prev() {
      if (i > 0) go(i - 1, -1);
    }
    function hide() {
      hint.style.opacity = "0";
    }
    hint.style.opacity = "1";
    hintTimer = setTimeout(hide, 3500);

    var sx = 0;
    var sy = 0;
    var moved = false;
    var ignoreGesture = false;
    function fromChrome(target) {
      return target && target.closest && target.closest("a, button, .skin-picker, input, textarea");
    }
    on(
      document,
      "touchstart",
      function (e) {
        if (!e.target.closest || !e.target.closest(".mag-shell")) return;
        if (fromChrome(e.target)) {
          ignoreGesture = true;
          return;
        }
        ignoreGesture = false;
        var t = e.touches[0];
        sx = t.clientX;
        sy = t.clientY;
        moved = false;
      },
      { passive: true },
    );
    on(
      document,
      "touchmove",
      function (e) {
        if (ignoreGesture) return;
        if (!e.target.closest || !e.target.closest(".mag-shell")) return;
        var t = e.touches[0];
        if (Math.abs(t.clientX - sx) > 10) moved = true;
        if (Math.abs(t.clientX - sx) > Math.abs(t.clientY - sy)) e.preventDefault();
      },
      { passive: false },
    );
    on(
      document,
      "touchend",
      function (e) {
        if (ignoreGesture || fromChrome(e.target)) return;
        if (!e.target.closest || !e.target.closest(".mag-shell")) return;
        var t = e.changedTouches[0];
        var dx = t.clientX - sx;
        var dy = t.clientY - sy;
        suppressClick = true;
        setTimeout(function () {
          suppressClick = false;
        }, 700);
        if (Math.abs(dx) > 40 && Math.abs(dx) > Math.abs(dy)) {
          dx < 0 ? next() : prev();
          e.preventDefault();
          return;
        }
        if (!moved && e.target.closest("a")) return;
        if (!moved && Math.abs(dx) < 10 && Math.abs(dy) < 10) {
          e.preventDefault();
          t.clientX > innerWidth * 0.5 ? next() : prev();
        }
      },
      { passive: false },
    );
    on(document, "click", function (e) {
      if (suppressClick || e.pointerType === "touch") return;
      if (!e.target.closest || !e.target.closest(".mag-shell")) return;
      if (fromChrome(e.target)) return;
      e.clientX > innerWidth * 0.5 ? next() : prev();
    });
    on(document, "keydown", function (e) {
      if (!document.querySelector(".mag-shell")) return;
      if (fromChrome(e.target)) return;
      if (["ArrowRight", "PageDown", " "].indexOf(e.key) !== -1) {
        next();
        e.preventDefault();
      }
      if (["ArrowLeft", "PageUp"].indexOf(e.key) !== -1) {
        prev();
        e.preventDefault();
      }
    });

    on(window, "resize", function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(layout, 120);
    });

    var start = parseInt((location.hash.match(/p(\d+)/) || [])[1] || "1", 10) - 1;
    var ready = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
    ready.then(function () {
      layout();
      go(isNaN(start) ? 0 : start, 0);
    });
    b.querySelectorAll("img").forEach(function (im) {
      on(im, "load", function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(layout, 80);
      });
    });
  }

  window.ArtometricsMag = { boot: boot, destroy: destroy };
})();
