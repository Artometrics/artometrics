(function () {
  var q = document.getElementById("src-q");
  var list = document.getElementById("src-list");
  if (!q || !list) return;
  var items = Array.prototype.slice.call(list.children);
  var count = document.getElementById("src-count");
  var empty = document.getElementById("src-empty");
  var desk = "";

  function apply() {
    var term = q.value.trim().toLowerCase();
    var shown = 0;
    items.forEach(function (li) {
      var ok = (!desk || li.dataset.desk === desk) && (!term || li.dataset.q.indexOf(term) >= 0);
      li.hidden = !ok;
      if (ok) shown++;
    });
    count.textContent = shown + (shown === 1 ? " report" : " reports");
    empty.hidden = shown !== 0;
  }

  q.addEventListener("input", apply);

  document.getElementById("src-chips").addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (!b) return;
    desk = b.dataset.desk;
    Array.prototype.forEach.call(this.children, function (c) { c.setAttribute("aria-pressed", c === b ? "true" : "false"); });
    apply();
  });

  var view = document.querySelector(".src-view");
  view.addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (!b) return;
    Array.prototype.forEach.call(view.children, function (c) { c.setAttribute("aria-pressed", c === b ? "true" : "false"); });
    document.querySelector(".src-index").classList.toggle("src-index--table", b.dataset.view === "table");
  });

  if (location.hash) {
    var id = location.hash.slice(1);
    var chip = document.querySelector('#src-chips [data-desk="' + id + '"]');
    if (chip) chip.click();
  }
})();
