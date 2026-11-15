(function () {
  var AM = window.AM, h = AM.h;
  var root = AM.root();
  var say;
  var Ctx = window.AudioContext || window.webkitAudioContext;
  var ctx = null;
  var source = null;
  var buffer = null;
  var name = "sample";
  var recorder = null;
  var stream = null;

  function audio() { if (!ctx) ctx = new Ctx(); return ctx; }

  var wave = h("canvas", { class: "smp-wave", width: "900", height: "140", role: "img", "aria-label": "Waveform of the current take" });
  var info = h("p", { class: "tool-note", text: "No audio yet. Record or load a file." });
  var recBtn = h("button", { type: "button", class: "tool-btn", text: "Record" });
  var playBtn = h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "Play", disabled: true });
  var exportBtn = h("button", { type: "button", class: "tool-btn tool-btn--ghost", text: "Export WAV", disabled: true });

  function range(label, min, max, step, value, fmt) {
    var out = h("output", { text: fmt(value) });
    var input = h("input", { type: "range", min: String(min), max: String(max), step: String(step), value: String(value), "aria-label": label,
      oninput: function () { out.textContent = fmt(+input.value); draw(); } });
    return { input: input, node: h("label", { class: "tool-field" }, h("span", { text: label }), input, out) };
  }
  var start = range("Trim start", 0, 1000, 1, 0, function (v) { return (v / 10).toFixed(1) + "%"; });
  var end = range("Trim end", 0, 1000, 1, 1000, function (v) { return (v / 10).toFixed(1) + "%"; });
  var fadeIn = range("Fade in", 0, 2000, 10, 0, function (v) { return v + " ms"; });
  var fadeOut = range("Fade out", 0, 2000, 10, 0, function (v) { return v + " ms"; });
  var speed = range("Speed / pitch", 0.5, 2, 0.05, 1, function (v) { return v.toFixed(2) + "x"; });
  var reverse = h("input", { type: "checkbox", id: "smp-rev" });
  var normalize = h("input", { type: "checkbox", id: "smp-norm", checked: true });
  normalize.checked = true;

  function draw() {
    var c = wave.getContext("2d");
    var W = wave.width, H = wave.height;
    c.clearRect(0, 0, W, H);
    var style = getComputedStyle(document.documentElement);
    var ink = style.getPropertyValue("--ink").trim() || "#f3ead7";
    var pink = style.getPropertyValue("--pink").trim() || "#ff3d8a";
    c.fillStyle = "rgba(127,127,127,0.12)";
    c.fillRect(0, 0, W, H);
    if (!buffer) return;
    var data = buffer.getChannelData(0);
    var per = Math.max(1, Math.floor(data.length / W));
    var a = (start.input.value / 1000) * W, b = (end.input.value / 1000) * W;
    for (var x = 0; x < W; x++) {
      var lo = 0, hi = 0;
      for (var i = 0; i < per; i++) {
        var v = data[x * per + i] || 0;
        if (v < lo) lo = v;
        if (v > hi) hi = v;
      }
      c.fillStyle = x >= a && x <= b ? pink : ink;
      c.globalAlpha = x >= a && x <= b ? 1 : 0.35;
      c.fillRect(x, H / 2 + lo * (H / 2 - 4), 1, Math.max(1, (hi - lo) * (H / 2 - 4)));
    }
    c.globalAlpha = 1;
  }

  function process() {
    if (!buffer) return null;
    var n = buffer.length;
    var s = Math.floor((start.input.value / 1000) * n);
    var e = Math.max(s + 1, Math.floor((end.input.value / 1000) * n));
    var rate = buffer.sampleRate;
    var rateFactor = +speed.input.value;
    var chans = [];
    for (var ch = 0; ch < buffer.numberOfChannels; ch++) {
      var seg = buffer.getChannelData(ch).slice(s, e);
      if (reverse.checked) seg.reverse();
      if (rateFactor !== 1) {
        var outLen = Math.max(1, Math.floor(seg.length / rateFactor));
        var res = new Float32Array(outLen);
        for (var i = 0; i < outLen; i++) {
          var pos = i * rateFactor, i0 = Math.floor(pos), frac = pos - i0;
          res[i] = (seg[i0] || 0) * (1 - frac) + (seg[i0 + 1] || 0) * frac;
        }
        seg = res;
      }
      chans.push(seg);
    }
    var len = chans[0].length;
    var fi = Math.min(len, Math.floor((+fadeIn.input.value / 1000) * rate));
    var fo = Math.min(len, Math.floor((+fadeOut.input.value / 1000) * rate));
    var peak = 0;
    chans.forEach(function (d) {
      for (var i = 0; i < fi; i++) d[i] *= i / fi;
      for (var j = 0; j < fo; j++) d[len - 1 - j] *= j / fo;
      for (var k = 0; k < len; k++) { var a = Math.abs(d[k]); if (a > peak) peak = a; }
    });
    if (normalize.checked && peak > 0) {
      var g = 0.89 / peak;
      chans.forEach(function (d) { for (var k = 0; k < len; k++) d[k] *= g; });
    }
    return { rate: rate, chans: chans, length: len };
  }

  function wav(p) {
    var ch = p.chans.length, len = p.length, bytes = len * ch * 2;
    var view = new DataView(new ArrayBuffer(44 + bytes));
    function str(o, t) { for (var i = 0; i < t.length; i++) view.setUint8(o + i, t.charCodeAt(i)); }
    str(0, "RIFF"); view.setUint32(4, 36 + bytes, true); str(8, "WAVE"); str(12, "fmt ");
    view.setUint32(16, 16, true); view.setUint16(20, 1, true); view.setUint16(22, ch, true);
    view.setUint32(24, p.rate, true); view.setUint32(28, p.rate * ch * 2, true);
    view.setUint16(32, ch * 2, true); view.setUint16(34, 16, true); str(36, "data"); view.setUint32(40, bytes, true);
    var o = 44;
    for (var i = 0; i < len; i++) {
      for (var c = 0; c < ch; c++) {
        var v = Math.max(-1, Math.min(1, p.chans[c][i]));
        view.setInt16(o, v < 0 ? v * 0x8000 : v * 0x7fff, true);
        o += 2;
      }
    }
    return new Blob([view], { type: "audio/wav" });
  }

  function stopPlayback() {
    if (source) { try { source.stop(); } catch (e) {} source = null; }
    playBtn.textContent = "Play";
  }

  function setBuffer(buf, label) {
    buffer = buf;
    name = label;
    stopPlayback();
    start.input.value = 0; end.input.value = 1000;
    start.input.dispatchEvent(new Event("input")); end.input.dispatchEvent(new Event("input"));
    playBtn.disabled = exportBtn.disabled = false;
    info.textContent = label + " · " + buf.duration.toFixed(2) + " s · " + buf.numberOfChannels + " ch · " + buf.sampleRate + " Hz";
    draw();
  }

  function decode(arrayBuffer, label) {
    var c = audio();
    var done = function (buf) { setBuffer(buf, label); };
    var fail = function () { say("Could not decode that audio."); };
    var p = c.decodeAudioData(arrayBuffer, done, fail);
    if (p && p.catch) p.catch(fail);
  }

  playBtn.addEventListener("click", function () {
    if (source) return stopPlayback();
    var p = process();
    if (!p) return;
    var c = audio();
    if (c.state === "suspended") c.resume();
    var buf = c.createBuffer(p.chans.length, p.length, p.rate);
    p.chans.forEach(function (d, i) { buf.copyToChannel(d, i); });
    source = c.createBufferSource();
    source.buffer = buf;
    source.connect(c.destination);
    source.onended = function () { source = null; playBtn.textContent = "Play"; };
    source.start();
    playBtn.textContent = "Stop";
  });

  exportBtn.addEventListener("click", function () {
    var p = process();
    if (p) AM.download(AM.slug(name) + ".wav", wav(p), "audio/wav");
  });

  recBtn.addEventListener("click", function () {
    if (recorder) { recorder.stop(); return; }
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || typeof MediaRecorder === "undefined") {
      return say("Recording is not available in this browser. Load an audio file instead.");
    }
    navigator.mediaDevices.getUserMedia({ audio: true }).then(function (s) {
      stream = s;
      var chunks = [];
      recorder = new MediaRecorder(s);
      recorder.ondataavailable = function (e) { if (e.data.size) chunks.push(e.data); };
      recorder.onstop = function () {
        stream.getTracks().forEach(function (t) { t.stop(); });
        var blob = new Blob(chunks, { type: recorder.mimeType || "audio/webm" });
        recorder = null;
        recBtn.textContent = "Record";
        blob.arrayBuffer().then(function (ab) { decode(ab, "recording-" + new Date().toISOString().slice(0, 19).replace(/[:T]/g, "-")); });
      };
      recorder.start();
      recBtn.textContent = "Stop recording";
    }).catch(function () { say("Microphone access was blocked. You can still load an audio file."); });
  });

  var file = h("input", { type: "file", accept: "audio/*", "aria-label": "Load an audio file", onchange: function () {
    var f = file.files[0];
    if (!f) return;
    f.arrayBuffer().then(function (ab) { decode(ab, f.name.replace(/\.[^.]+$/, "")); });
  } });

  root.appendChild(h("div", { class: "tool-panel" },
    h("div", { class: "tool-row" }, recBtn, playBtn, exportBtn),
    h("label", { class: "tool-field" }, h("span", { text: "Or load a file" }), file),
    info, wave,
    start.node, end.node, fadeIn.node, fadeOut.node, speed.node,
    h("div", { class: "tool-row" },
      h("label", { class: "tool-check", for: "smp-rev" }, reverse, " Reverse"),
      h("label", { class: "tool-check", for: "smp-norm" }, normalize, " Normalize"))));
  [reverse, normalize].forEach(function (el) { el.addEventListener("change", draw); });
  say = AM.status(root);
  root.appendChild(h("p", { class: "tool-note", text: "Samples are made from your own recording or file. Only use audio you have the right to use." }));
  draw();
  if (root.dataset.mode === "record") recBtn.focus();
})();
