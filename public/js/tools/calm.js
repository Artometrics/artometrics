(function () {
  var AM = window.AM, h = AM.h;
  var root = AM.root();

  var patterns = {
    box: { label: "Box (4-4-4-4)", steps: [["Breathe in", 4], ["Hold", 4], ["Breathe out", 4], ["Hold", 4]] },
    relax: { label: "Slow (4-7-8)", steps: [["Breathe in", 4], ["Hold", 7], ["Breathe out", 8]] },
  };
  var orb = h("div", { class: "breath__orb", "aria-hidden": "true" });
  var label = h("p", { class: "breath__label", role: "status", "aria-live": "polite", text: "Ready" });
  var picker = h("select", { "aria-label": "Breathing pattern" }, Object.keys(patterns).map(function (k) { return h("option", { value: k, text: patterns[k].label }); }));
  var timer = null;
  var toggle = h("button", { type: "button", class: "tool-btn", text: "Start" });

  function stop() {
    clearTimeout(timer);
    timer = null;
    toggle.textContent = "Start";
    label.textContent = "Ready";
    orb.style.transform = "scale(1)";
  }

  function run(steps, i) {
    var step = steps[i % steps.length];
    label.textContent = step[0] + " · " + step[1];
    var grow = step[0] === "Breathe in", shrink = step[0] === "Breathe out";
    orb.style.transitionDuration = AM.reduceMotion() ? "0s" : step[1] + "s";
    if (grow) orb.style.transform = "scale(1.55)";
    if (shrink) orb.style.transform = "scale(1)";
    timer = setTimeout(function () { run(steps, i + 1); }, step[1] * 1000);
  }

  toggle.addEventListener("click", function () {
    if (timer) return stop();
    toggle.textContent = "Stop";
    run(patterns[picker.value].steps, 0);
  });
  picker.addEventListener("change", function () { if (timer) { stop(); } });

  root.appendChild(h("section", { class: "tool-panel breath" },
    h("h2", { text: "Breathing pacer" }), orb, label,
    h("div", { class: "tool-row" }, picker, toggle)));

  var senses = [
    ["5", "things you can see"], ["4", "things you can feel"], ["3", "things you can hear"],
    ["2", "things you can smell"], ["1", "thing you can taste"],
  ];
  var key = "aftercare-grounding";
  var done = AM.load(key, []);
  var list = h("ul", { class: "ground" });
  senses.forEach(function (s, i) {
    var cb = h("input", { type: "checkbox", id: "g" + i });
    cb.checked = done.indexOf(i) >= 0;
    cb.addEventListener("change", function () {
      done = senses.map(function (_, n) { return n; }).filter(function (n) { return document.getElementById("g" + n).checked; });
      AM.save(key, done);
    });
    list.appendChild(h("li", null, h("label", { for: "g" + i }, cb, h("strong", { text: s[0] }), " " + s[1])));
  });
  root.appendChild(h("section", { class: "tool-panel" },
    h("h2", { text: "5-4-3-2-1 grounding" }),
    list,
    h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "Reset", onclick: function () {
      AM.save(key, []);
      Array.prototype.forEach.call(list.querySelectorAll("input"), function (c) { c.checked = false; });
    } }),
    h("p", { class: "tool-note", text: "These are self-care prompts, not medical advice. If you are in crisis, contact local emergency services or a crisis line." })
  ));
})();
