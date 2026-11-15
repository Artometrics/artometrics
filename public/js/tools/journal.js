(function () {
  var AM = window.AM, h = AM.h;
  var root = AM.root();
  var store = root.dataset.store;
  var entries = AM.load(store, []);
  var say;

  var area = h("textarea", { class: "tool-text", rows: "8", placeholder: "What happened? What do you want to remember? No one else sees this.", "aria-label": "New entry" });
  var mood = h("select", { "aria-label": "Mood" },
    h("option", { value: "", text: "Mood (optional)" }),
    ["Heavy", "Low", "Even", "Good", "Bright"].map(function (label, i) { return h("option", { value: String(i + 1), text: label }); }));
  var list = h("div", { class: "tool-list" });

  function persist() {
    if (!AM.save(store, entries)) say("Could not save: browser storage is full or blocked.");
  }

  function render() {
    list.textContent = "";
    if (!entries.length) {
      list.appendChild(h("p", { class: "tool-empty", text: "No entries yet." }));
      return;
    }
    entries.forEach(function (entry) {
      var body = h("p", { class: "tool-entry__body", text: entry.text });
      list.appendChild(
        h("article", { class: "tool-entry" },
          h("p", { class: "tool-entry__meta", text: AM.stamp(entry.at) + (entry.mood ? " · mood " + entry.mood + "/5" : "") }),
          body,
          h("button", {
            type: "button", class: "tool-btn tool-btn--quiet", text: "Delete",
            onclick: function () {
              if (!window.confirm("Delete this entry? This cannot be undone.")) return;
              entries = entries.filter(function (e) { return e.id !== entry.id; });
              persist();
              render();
            },
          })
        )
      );
    });
  }

  var compose = h("div", { class: "tool-panel" },
    area,
    h("div", { class: "tool-row" },
      mood,
      h("button", {
        type: "button", class: "tool-btn", text: "Save entry",
        onclick: function () {
          var text = area.value.trim();
          if (!text) return say("Write something first.");
          entries.unshift({ id: AM.uid(), at: new Date().toISOString(), text: text, mood: mood.value || null });
          area.value = "";
          mood.value = "";
          persist();
          render();
          say("Saved on this device.");
        },
      }),
      h("button", {
        type: "button", class: "tool-btn tool-btn--ghost", text: "Export all",
        onclick: function () {
          var md = entries.map(function (e) { return "## " + AM.stamp(e.at) + (e.mood ? " (mood " + e.mood + "/5)" : "") + "\n\n" + e.text + "\n"; }).join("\n");
          AM.download(store + ".md", md || "No entries yet.\n", "text/markdown");
        },
      })
    )
  );

  root.appendChild(compose);
  say = AM.status(root);
  root.appendChild(list);

  // Tarot readings saved from the tarot page land here when this is the Aftercare journal.
  var pending = AM.load("aftercare-pending-reading", null);
  if (pending && store === "aftercare-journal") {
    area.value = pending;
    AM.save("aftercare-pending-reading", null);
  }
  render();
})();
