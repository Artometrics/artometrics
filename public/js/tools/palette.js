(function () {
  var AM = window.AM, h = AM.h;
  var root = AM.root();
  var say;
  var kits = AM.load("palette-kits", []);
  var colors = [];
  var imageName = "palette";

  function toHex(c) { return "#" + c.map(function (v) { return ("0" + v.toString(16)).slice(-2); }).join(""); }
  function lum(c) {
    var a = c.map(function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
    return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2];
  }
  function ratio(a, b) { var l1 = Math.max(lum(a), lum(b)), l2 = Math.min(lum(a), lum(b)); return (l1 + 0.05) / (l2 + 0.05); }

  function medianCut(pixels, n) {
    var boxes = [pixels];
    while (boxes.length < n) {
      var idx = -1, best = 0, chan = 0;
      boxes.forEach(function (box, i) {
        if (box.length < 2) return;
        for (var ch = 0; ch < 3; ch++) {
          var lo = 255, hi = 0;
          box.forEach(function (p) { if (p[ch] < lo) lo = p[ch]; if (p[ch] > hi) hi = p[ch]; });
          var range = (hi - lo) * Math.sqrt(box.length);
          if (range > best) { best = range; idx = i; chan = ch; }
        }
      });
      if (idx < 0) break;
      var box = boxes.splice(idx, 1)[0];
      box.sort(function (a, b) { return a[chan] - b[chan]; });
      var mid = box.length >> 1;
      boxes.push(box.slice(0, mid), box.slice(mid));
    }
    return boxes.map(function (box) {
      var s = [0, 0, 0];
      box.forEach(function (p) { s[0] += p[0]; s[1] += p[1]; s[2] += p[2]; });
      return { rgb: s.map(function (v) { return Math.round(v / box.length); }), weight: box.length };
    }).sort(function (a, b) { return b.weight - a.weight; });
  }

  var count = h("input", { type: "range", min: "3", max: "8", value: "5", "aria-label": "Number of colors" });
  var countOut = h("output", { text: "5" });
  var swatches = h("div", { class: "pal-swatches" });
  var preview = h("canvas", { class: "pal-preview", width: "10", height: "10", role: "img", "aria-label": "Your image" });
  var exportRow = h("div", { class: "tool-row", hidden: true });
  var kitList = h("div", { class: "tool-list" });
  var pixels = null;

  function analyse() {
    if (!pixels) return;
    countOut.textContent = count.value;
    colors = medianCut(pixels.slice(), +count.value);
    swatches.textContent = "";
    colors.forEach(function (c) {
      var hex = toHex(c.rgb);
      var onLight = ratio(c.rgb, [255, 255, 255]), onDark = ratio(c.rgb, [0, 0, 0]);
      var ink = onDark >= onLight ? "#000" : "#fff";
      swatches.appendChild(h("button", {
        type: "button", class: "pal-swatch", style: "background:" + hex + ";color:" + ink,
        "aria-label": "Copy " + hex,
        onclick: function () {
          if (navigator.clipboard) navigator.clipboard.writeText(hex).then(function () { say("Copied " + hex); }, function () { say(hex); });
          else say(hex);
        },
      }, h("strong", { text: hex.toUpperCase() }), h("span", { text: Math.round((c.weight / pixels.length) * 100) + "% of image" }),
        h("span", { text: "Text contrast " + Math.max(onLight, onDark).toFixed(1) + ":1" })));
    });
    exportRow.hidden = false;
  }

  function load(file) {
    if (!file || !/^image\//.test(file.type)) return say("Choose an image file.");
    imageName = AM.slug(file.name.replace(/\.[^.]+$/, ""));
    var url = URL.createObjectURL(file);
    var img = new Image();
    img.onload = function () {
      var scale = Math.min(1, 160 / Math.max(img.width, img.height));
      var w = Math.max(1, Math.round(img.width * scale)), hh = Math.max(1, Math.round(img.height * scale));
      var c = document.createElement("canvas");
      c.width = w; c.height = hh;
      var ctx = c.getContext("2d", { willReadFrequently: true });
      ctx.drawImage(img, 0, 0, w, hh);
      var data = ctx.getImageData(0, 0, w, hh).data;
      pixels = [];
      for (var i = 0; i < data.length; i += 4) if (data[i + 3] > 200) pixels.push([data[i], data[i + 1], data[i + 2]]);
      preview.width = w; preview.height = hh;
      preview.getContext("2d").drawImage(c, 0, 0);
      URL.revokeObjectURL(url);
      if (!pixels.length) return say("That image is fully transparent.");
      analyse();
    };
    img.onerror = function () { URL.revokeObjectURL(url); say("Could not read that image."); };
    img.src = url;
  }

  var file = h("input", { type: "file", accept: "image/*", "aria-label": "Choose an image", onchange: function () { load(file.files[0]); } });
  var drop = h("div", { class: "pal-drop" }, h("p", { text: "Drop an image here, or" }), file);
  ["dragover", "dragenter"].forEach(function (ev) { drop.addEventListener(ev, function (e) { e.preventDefault(); drop.classList.add("is-over"); }); });
  ["dragleave", "drop"].forEach(function (ev) { drop.addEventListener(ev, function () { drop.classList.remove("is-over"); }); });
  drop.addEventListener("drop", function (e) { e.preventDefault(); load(e.dataTransfer.files[0]); });
  count.addEventListener("input", analyse);

  function renderKits() {
    kitList.textContent = "";
    if (!kits.length) return;
    kitList.appendChild(h("h2", { text: "Saved kits (this browser)" }));
    kits.forEach(function (k) {
      kitList.appendChild(h("div", { class: "tool-entry" },
        h("p", { class: "tool-entry__meta", text: k.name }),
        h("div", { class: "pal-strip" }, k.hex.map(function (x) { return h("span", { style: "background:" + x, title: x }); })),
        h("button", { type: "button", class: "tool-btn tool-btn--quiet", text: "Delete", onclick: function () {
          kits = kits.filter(function (x) { return x.id !== k.id; }); AM.save("palette-kits", kits); renderKits();
        } })));
    });
  }

  function hexes() { return colors.map(function (c) { return toHex(c.rgb); }); }
  exportRow.appendChild(h("button", { type: "button", class: "tool-btn", text: "CSS variables", onclick: function () {
    AM.download(imageName + "-palette.css", ":root {\n" + hexes().map(function (x, i) { return "  --color-" + (i + 1) + ": " + x + ";"; }).join("\n") + "\n}\n", "text/css");
  } }));
  exportRow.appendChild(h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "JSON", onclick: function () {
    AM.download(imageName + "-palette.json", JSON.stringify({ source: imageName, colors: hexes() }, null, 2), "application/json");
  } }));
  exportRow.appendChild(h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "SVG strip", onclick: function () {
    var hx = hexes(), w = 120;
    var svg = '<svg xmlns="http://www.w3.org/2000/svg" width="' + hx.length * w + '" height="' + w + '" viewBox="0 0 ' + hx.length * w + " " + w + '">' +
      hx.map(function (x, i) { return '<rect x="' + i * w + '" width="' + w + '" height="' + w + '" fill="' + x + '"/>'; }).join("") + "</svg>";
    AM.download(imageName + "-palette.svg", svg, "image/svg+xml");
  } }));
  exportRow.appendChild(h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "Save kit", onclick: function () {
    kits.unshift({ id: AM.uid(), name: imageName, hex: hexes() });
    AM.save("palette-kits", kits.slice(0, 30)); renderKits(); say("Saved in this browser.");
  } }));

  root.appendChild(h("div", { class: "tool-panel" },
    drop,
    h("label", { class: "tool-field" }, h("span", { text: "Colors" }), count, countOut),
    preview, swatches, exportRow));
  say = AM.status(root);
  root.appendChild(kitList);
  renderKits();
})();
