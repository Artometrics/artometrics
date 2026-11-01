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

    if (!b._magSource || !b.querySelector(".mag-page")) b._magSource = b.innerHTML;
    var sourceHTML = b._magSource;
    var layoutPasses = 0;

    function fits(page) {
      return page.scrollHeight <= page.clientHeight + 1;
    }

    function paginate() {
      W = v.clientWidth;
      G = 0;
      var pageH = v.clientHeight;
      var nodes = Array.from(b.childNodes).filter(function (node) {
        return node.nodeType === 1 || (node.nodeType === 3 && node.textContent.trim());
      });
      b.textContent = "";
      b.classList.add("mag-paged");
      var page = null;

      function makePage() {
        page = document.createElement("div");
        page.className = "mag-page";
        page.style.width = W + "px";
        page.style.height = pageH + "px";
        b.appendChild(page);
        return page;
      }

      function add(node) {
        page.appendChild(node);
        if (fits(page)) return;
        if ((node.tagName === "UL" || node.tagName === "OL") && node.children.length) {
          var items = Array.from(node.children);
          items.forEach(function (li) {
            li.remove();
          });
          var list = node;
          items.forEach(function (li) {
            list.appendChild(li);
            if (fits(page)) return;
            list.removeChild(li);
            if (!list.children.length) {
              if (page.childElementCount === 1) {
                list.appendChild(li);
                page = makePage();
                list = node.cloneNode(false);
                page.appendChild(list);
                return;
              }
              list.remove();
            }
            page = makePage();
            list = node.cloneNode(false);
            page.appendChild(list);
            list.appendChild(li);
          });
          return;
        }
        if (page.childElementCount > 1) {
          page.removeChild(node);
          // height is fixed, so scrollHeight never drops below the page.
          // Measure the lead-in itself and keep a short one with the next block.
          var fixed = page.style.height;
          page.style.alignSelf = "flex-start";
          page.style.height = "auto";
          var lead = page.scrollHeight;
          page.style.height = fixed;
          page.style.alignSelf = "";
          if (lead < page.clientHeight * 0.72) {
            page.appendChild(node);
            return;
          }
          page = makePage();
          add(node);
        }
      }

      makePage();
      nodes.forEach(add);
      var pages = b.querySelectorAll(".mag-page");
      if (pages.length > 1) {
        var last = pages[pages.length - 1];
        if (!last.textContent.trim() && !last.querySelector("img")) last.remove();
      }
      n = Math.max(1, b.querySelectorAll(".mag-page").length);
    }

    function layout() {
      var keep = n > 1 ? i / Math.max(1, n - 1) : 0;
      b.classList.add("noanim");
      b.innerHTML = sourceHTML;
      paginate();
      i = Math.min(n - 1, Math.round(keep * (n - 1)) || 0);
      go(i, 0);
      requestAnimationFrame(function () {
        b.classList.remove("noanim");
      });
    }

    function reveal() {
      var page = b.children[i];
      if (!page) return;
      page.querySelectorAll("figure,.fade").forEach(function (el) {
        el.classList.add("on");
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
        var params = new URLSearchParams(location.search);
        var asked = params.get("skin");
        var shell = document.querySelector(".mag-shell");
        var active = shell && shell.getAttribute("data-skin");
        if (asked && active && asked !== active) params.delete("skin");
        var search = params.toString();
        history.replaceState(null, "", location.pathname + (search ? "?" + search : "") + "#p" + (i + 1));
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
    on(
      b,
      "scroll",
      function (e) {
        if (e.target && e.target.classList && e.target.classList.contains("mag-page")) hide();
      },
      true,
    );
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
        if (Math.abs(t.clientX - sx) > 10 || Math.abs(t.clientY - sy) > 10) moved = true;
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

    function bindImages() {
      b.querySelectorAll("img").forEach(function (im) {
        if (im.complete) return;
        on(im, "load", function () {
          if (layoutPasses > 6) return;
          clearTimeout(resizeTimer);
          resizeTimer = setTimeout(function () {
            layoutPasses += 1;
            layout();
            bindImages();
          }, 80);
        });
      });
    }

    var start = parseInt((location.hash.match(/p(\d+)/) || [])[1] || "1", 10) - 1;
    var ready = document.fonts && document.fonts.ready ? document.fonts.ready : Promise.resolve();
    ready.then(function () {
      layout();
      go(isNaN(start) ? 0 : start, 0);
      bindImages();
    });
  }

  window.ArtometricsMag = { boot: boot, destroy: destroy };
})();
