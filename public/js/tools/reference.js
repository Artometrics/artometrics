(function () {
  var AM = window.AM, h = AM.h;
  var root = AM.root();
  var store = root.dataset.store;
  var items = AM.load(store, []);
  var say;

  var kind = h("select", { "aria-label": "Type" }, ["Quote", "Link", "Note"].map(function (k) { return h("option", { value: k.toLowerCase(), text: k }); }));
  var text = h("textarea", { class: "tool-text", rows: "3", placeholder: "Paste a quote, a link, or a note", "aria-label": "Reference text" });
  var from = h("input", { type: "text", class: "tool-input", placeholder: "Where it is from (author, title, URL)", "aria-label": "Source" });
  var q = h("input", { type: "search", class: "tool-input", placeholder: "Filter the shelf", "aria-label": "Filter" });
  var list = h("div", { class: "tool-list" });

  function persist() { AM.save(store, items); }
  function render() {
    var term = q.value.trim().toLowerCase();
    list.textContent = "";
    var shown = items.filter(function (i) { return !term || (i.text + " " + i.from).toLowerCase().indexOf(term) >= 0; });
    if (!shown.length) return list.appendChild(h("p", { class: "tool-empty", text: items.length ? "Nothing matches." : "Your shelf is empty." }));
    shown.forEach(function (i) {
      var isUrl = /^https?:\/\//.test(i.text.trim());
      list.appendChild(h("article", { class: "tool-entry" },
        h("p", { class: "tool-entry__meta", text: i.kind + (i.from ? " · " + i.from : "") }),
        isUrl ? h("a", { href: i.text.trim(), rel: "noopener noreferrer", target: "_blank", text: i.text.trim() }) : h("p", { class: "tool-entry__body", text: i.text }),
        h("button", { type: "button", class: "tool-btn tool-btn--quiet", text: "Remove", onclick: function () {
          items = items.filter(function (x) { return x.id !== i.id; }); persist(); render();
        } })));
    });
  }
  q.addEventListener("input", render);

  root.appendChild(h("div", { class: "tool-panel" },
    h("div", { class: "tool-row" }, kind, from),
    text,
    h("div", { class: "tool-row" },
      h("button", { type: "button", class: "tool-btn", text: "Add to shelf", onclick: function () {
        if (!text.value.trim()) return say("Add some text first.");
        items.unshift({ id: AM.uid(), kind: kind.value, text: text.value.trim(), from: from.value.trim() });
        text.value = ""; from.value = ""; persist(); render();
      } }),
      h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "Export Markdown", onclick: function () {
        AM.download("twilda-reference.md", items.map(function (i) { return "- **" + i.kind + "**" + (i.from ? " (" + i.from + ")" : "") + ": " + i.text.replace(/\n+/g, " "); }).join("\n") + "\n", "text/markdown");
      } })),
    q));
  say = AM.status(root);
  root.appendChild(list);
  render();
})();
