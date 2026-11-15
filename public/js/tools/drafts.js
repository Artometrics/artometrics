(function () {
  var AM = window.AM, h = AM.h;
  var root = AM.root();
  var store = root.dataset.store;
  var docs = AM.load(store, []);
  var currentId = docs.length ? docs[0].id : null;
  var say;

  var title = h("input", { type: "text", class: "tool-input tool-input--title", placeholder: "Title", "aria-label": "Draft title" });
  var body = h("textarea", { class: "tool-text tool-text--draft", rows: "18", placeholder: "Start writing. Drafts save automatically in this browser.", "aria-label": "Draft text" });
  var count = h("p", { class: "tool-note" });
  var list = h("ul", { class: "draft-list" });

  function current() { return docs.filter(function (d) { return d.id === currentId; })[0]; }
  function persist() { if (!AM.save(store, docs)) say("Could not save: browser storage is full or blocked."); }

  function open(id) {
    currentId = id;
    var d = current();
    title.value = d ? d.title : "";
    body.value = d ? d.text : "";
    title.disabled = body.disabled = !d;
    refresh();
  }

  function refresh() {
    var d = current();
    count.textContent = d ? AM.words(d.text) + " words · saved " + AM.stamp(d.at) : "No draft open.";
    list.textContent = "";
    docs.forEach(function (doc) {
      list.appendChild(h("li", null, h("button", {
        type: "button", class: "draft-list__item" + (doc.id === currentId ? " is-active" : ""),
        "aria-current": doc.id === currentId ? "true" : false,
        onclick: function () { open(doc.id); },
      }, h("strong", { text: doc.title || "Untitled" }), h("span", { text: AM.words(doc.text) + " words" }))));
    });
  }

  var saveTimer;
  function edit() {
    var d = current();
    if (!d) return;
    d.title = title.value;
    d.text = body.value;
    d.at = new Date().toISOString();
    clearTimeout(saveTimer);
    saveTimer = setTimeout(function () { persist(); refresh(); }, 400);
    count.textContent = AM.words(d.text) + " words";
  }
  title.addEventListener("input", edit);
  body.addEventListener("input", edit);

  function create() {
    var d = { id: AM.uid(), title: "", text: "", at: new Date().toISOString() };
    docs.unshift(d);
    persist();
    open(d.id);
    title.focus();
  }

  var importer = h("input", { type: "file", accept: "application/json,.json", hidden: true, onchange: function () {
    var f = importer.files[0];
    if (!f) return;
    f.text().then(function (t) {
      var data = JSON.parse(t);
      if (!Array.isArray(data)) throw new Error("bad");
      data.forEach(function (d) { if (d && typeof d.text === "string") docs.unshift({ id: AM.uid(), title: String(d.title || ""), text: d.text, at: new Date().toISOString() }); });
      persist(); open(docs[0] && docs[0].id); say("Imported.");
    }).catch(function () { say("That file is not a Twilda export."); });
  } });

  root.appendChild(h("div", { class: "drafts" },
    h("aside", { class: "drafts__side" },
      h("button", { type: "button", class: "tool-btn", text: "New draft", onclick: create }),
      list,
      h("div", { class: "tool-row" },
        h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "Export all", onclick: function () { AM.download("twilda-drafts.json", JSON.stringify(docs, null, 2), "application/json"); } }),
        h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "Import", onclick: function () { importer.click(); } }),
        importer)),
    h("div", { class: "drafts__main" },
      title, body, count,
      h("div", { class: "tool-row" },
        h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "Export Markdown", onclick: function () {
          var d = current(); if (!d) return;
          AM.download(AM.slug(d.title) + ".md", "# " + (d.title || "Untitled") + "\n\n" + d.text + "\n", "text/markdown");
        } }),
        h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "Export text", onclick: function () {
          var d = current(); if (!d) return;
          AM.download(AM.slug(d.title) + ".txt", (d.title ? d.title + "\n\n" : "") + d.text + "\n", "text/plain");
        } }),
        h("button", { type: "button", class: "tool-btn tool-btn--quiet", text: "Delete draft", onclick: function () {
          var d = current(); if (!d) return;
          if (!window.confirm("Delete this draft? Export it first if you want a copy.")) return;
          docs = docs.filter(function (x) { return x.id !== d.id; });
          persist(); open(docs[0] && docs[0].id);
        } })))
  ));
  say = AM.status(root);
  open(currentId);
})();
