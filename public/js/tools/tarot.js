(function () {
  var AM = window.AM, h = AM.h;
  var root = AM.root();
  var deck = JSON.parse(document.getElementById("tarot-deck").textContent);
  var out = h("div", { class: "tarot-spread" });
  var last = "";
  var say;

  function randInt(n) {
    var buf = new Uint32Array(1);
    var limit = Math.floor(4294967296 / n) * n;
    do { crypto.getRandomValues(buf); } while (buf[0] >= limit);
    return buf[0] % n;
  }

  function draw(positions) {
    var pool = deck.slice();
    for (var i = pool.length - 1; i > 0; i--) {
      var j = randInt(i + 1);
      var t = pool[i]; pool[i] = pool[j]; pool[j] = t;
    }
    out.textContent = "";
    var lines = [];
    positions.forEach(function (position, i) {
      var card = pool[i];
      var reversed = randInt(2) === 1;
      var meaning = reversed ? card.reversed : card.upright;
      lines.push(position + ": " + card.name + (reversed ? " (reversed)" : "") + " — " + meaning);
      out.appendChild(h("article", { class: "tarot-card" + (reversed ? " is-reversed" : "") },
        h("p", { class: "tool-entry__meta", text: position }),
        h("h2", { text: card.name }),
        h("p", { class: "tarot-card__dir", text: reversed ? "Reversed" : "Upright" }),
        h("p", { text: meaning })
      ));
    });
    last = lines.join("\n");
  }

  var spreads = { single: ["Today"], three: ["Past", "Present", "Future"], cross: ["Situation", "Challenge", "What helps", "Where it is heading", "Advice"] };
  var picker = h("select", { "aria-label": "Spread" },
    h("option", { value: "single", text: "One card" }),
    h("option", { value: "three", text: "Three cards (past, present, future)" }),
    h("option", { value: "cross", text: "Five cards (situation to advice)" }));

  root.appendChild(h("div", { class: "tool-panel" },
    h("div", { class: "tool-row" },
      picker,
      h("button", { type: "button", class: "tool-btn", text: "Draw", onclick: function () { draw(spreads[picker.value]); } }),
      h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "Save to journal", onclick: function () {
        if (!last) return say("Draw a spread first.");
        AM.save("aftercare-pending-reading", "Tarot reading\n" + last + "\n\nWhat it stirred up: ");
        window.location.href = "/tools/aftercare/journal";
      } })
    ),
    h("p", { class: "tool-note", text: "Cards are shuffled in your browser with the system random generator. A reading is a prompt for reflection, not a prediction." })
  ));
  say = AM.status(root);
  root.appendChild(out);
})();
