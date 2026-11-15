(function () {
  var AM = window.AM, h = AM.h;
  var root = AM.root();
  var store = root.dataset.store;
  var rows = AM.load(store, []);
  var say;
  var today = new Date().toISOString().slice(0, 10);

  function slider(label, min, max, step, value) {
    var out = h("output", { text: String(value) });
    var input = h("input", { type: "range", min: String(min), max: String(max), step: String(step), value: String(value), "aria-label": label,
      oninput: function () { out.textContent = input.value; } });
    return { input: input, node: h("label", { class: "tool-field" }, h("span", { text: label }), input, out) };
  }
  var mood = slider("Mood (1 low, 5 bright)", 1, 5, 1, 3);
  var energy = slider("Energy (1 empty, 5 full)", 1, 5, 1, 3);
  var sleep = slider("Sleep last night (hours)", 0, 12, 0.5, 7);
  var note = h("input", { type: "text", class: "tool-input", placeholder: "One line (optional)", "aria-label": "Note", maxlength: "200" });
  var chart = h("div", { class: "track-chart", "aria-hidden": "true" });
  var table = h("div", { class: "tool-list" });

  function persist() { AM.save(store, rows); }

  function spark(key, max, color) {
    var pts = rows.slice(0, 30).reverse();
    if (pts.length < 2) return null;
    var w = 300, hgt = 56, step = w / (pts.length - 1);
    var d = pts.map(function (r, i) { return (i ? "L" : "M") + (i * step).toFixed(1) + " " + (hgt - (r[key] / max) * (hgt - 6) - 3).toFixed(1); }).join(" ");
    var ns = "http://www.w3.org/2000/svg";
    var svg = document.createElementNS(ns, "svg");
    svg.setAttribute("viewBox", "0 0 " + w + " " + hgt);
    svg.setAttribute("preserveAspectRatio", "none");
    var p = document.createElementNS(ns, "path");
    p.setAttribute("d", d);
    p.setAttribute("fill", "none");
    p.setAttribute("stroke", color);
    p.setAttribute("stroke-width", "2.5");
    p.setAttribute("vector-effect", "non-scaling-stroke");
    svg.appendChild(p);
    return svg;
  }

  function render() {
    chart.textContent = "";
    [["mood", 5, "Mood", "var(--pink)"], ["energy", 5, "Energy", "var(--blue-text)"], ["sleep", 12, "Sleep", "var(--muted)"]].forEach(function (c) {
      var svg = spark(c[0], c[1], c[2]);
      chart.appendChild(h("div", { class: "track-chart__row" }, h("span", { text: c[2] }), svg || h("em", { text: "Log two days to see a line." })));
    });
    table.textContent = "";
    if (!rows.length) return table.appendChild(h("p", { class: "tool-empty", text: "No check-ins yet." }));
    rows.slice(0, 30).forEach(function (r) {
      table.appendChild(h("p", { class: "tool-entry__meta track-line" },
        h("strong", { text: r.date }),
        " · mood " + r.mood + " · energy " + r.energy + " · sleep " + r.sleep + "h" + (r.note ? " · " + r.note : "")));
    });
  }

  root.appendChild(h("div", { class: "tool-panel" },
    mood.node, energy.node, sleep.node, note,
    h("div", { class: "tool-row" },
      h("button", { type: "button", class: "tool-btn", text: "Log today", onclick: function () {
        rows = rows.filter(function (r) { return r.date !== today; });
        rows.unshift({ date: today, mood: +mood.input.value, energy: +energy.input.value, sleep: +sleep.input.value, note: note.value.trim() });
        rows.sort(function (a, b) { return a.date < b.date ? 1 : -1; });
        persist(); render(); say("Logged for " + today + ".");
      } }),
      h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "Export CSV", onclick: function () {
        var csv = "date,mood,energy,sleep_hours,note\n" + rows.map(function (r) {
          return [r.date, r.mood, r.energy, r.sleep, '"' + String(r.note || "").replace(/"/g, '""') + '"'].join(",");
        }).join("\n") + "\n";
        AM.download("aftercare-track.csv", csv, "text/csv");
      } })
    )
  ));
  say = AM.status(root);
  root.appendChild(chart);
  root.appendChild(table);
  render();
})();
