(function () {
  var PREFIX = "artometrics:";
  var AM = (window.AM = {});

  AM.load = function (key, fallback) {
    try {
      var raw = localStorage.getItem(PREFIX + key);
      return raw ? JSON.parse(raw) : fallback;
    } catch (e) {
      return fallback;
    }
  };

  AM.save = function (key, value) {
    try {
      localStorage.setItem(PREFIX + key, JSON.stringify(value));
      return true;
    } catch (e) {
      return false;
    }
  };

  AM.uid = function () {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 7);
  };

  AM.h = function (tag, attrs) {
    var node = document.createElement(tag);
    attrs = attrs || {};
    Object.keys(attrs).forEach(function (name) {
      var value = attrs[name];
      if (value === false || value == null) return;
      if (name === "class") node.className = value;
      else if (name === "text") node.textContent = value;
      else if (name.slice(0, 2) === "on") node.addEventListener(name.slice(2), value);
      else node.setAttribute(name, value === true ? "" : value);
    });
    (function add(list) {
      for (var i = 0; i < list.length; i++) {
        var child = list[i];
        if (child == null || child === false) continue;
        if (Array.isArray(child)) add(child);
        else node.appendChild(typeof child === "string" ? document.createTextNode(child) : child);
      }
    })(Array.prototype.slice.call(arguments, 2));
    return node;
  };

  AM.download = function (name, data, type) {
    var blob = data instanceof Blob ? data : new Blob([data], { type: type || "text/plain" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1500);
  };

  AM.stamp = function (iso) {
    var d = new Date(iso);
    return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" }) +
      " · " + d.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
  };

  AM.slug = function (text) {
    return String(text || "untitled").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "") || "untitled";
  };

  AM.words = function (text) {
    var m = String(text || "").trim().match(/\S+/g);
    return m ? m.length : 0;
  };

  AM.status = function (root) {
    var el = AM.h("p", { class: "tool-status", role: "status", "aria-live": "polite" });
    root.appendChild(el);
    var timer;
    return function (message) {
      el.textContent = message;
      clearTimeout(timer);
      timer = setTimeout(function () { el.textContent = ""; }, 3500);
    };
  };

  AM.reduceMotion = function () {
    return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  };

  AM.root = function () {
    return document.querySelector("[data-mount]");
  };
})();
