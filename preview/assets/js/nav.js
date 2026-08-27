/* The menu button, at every width.

   It controls .site-menu, which is the whole navigation - separate from the
   contextual .site-nav in the header, which only ever shows the current
   level. Visibility is driven by data-open rather than the `hidden` attribute
   so the CSS decides how the panel presents itself. */
(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("hoofdmenu");
  if (!toggle || !nav) return;

  function isOpen() {
    return nav.getAttribute("data-open") === "true";
  }

  /* Read off the button rather than hardcoded: the site is served in Dutch and
     English from separate URLs, and a hardcoded string put "Menu sluiten" on
     the English pages. */
  var labelOpen = toggle.getAttribute("data-label-open") || toggle.getAttribute("aria-label");
  var labelClose = toggle.getAttribute("data-label-close") || labelOpen;

  function setOpen(open) {
    nav.setAttribute("data-open", String(open));
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? labelClose : labelOpen);
  }

  toggle.addEventListener("click", function () {
    setOpen(!isOpen());
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && isOpen()) {
      setOpen(false);
      toggle.focus();
    }
  });

  /* A click anywhere else closes the menu. */
  document.addEventListener("click", function (event) {
    if (!isOpen()) return;
    if (nav.contains(event.target) || toggle.contains(event.target)) return;
    setOpen(false);
  });

  /* Crossing the breakpoint relayouts the header underneath an open panel;
     closing it avoids leaving it anchored to a button that has moved. */
  window.matchMedia("(min-width: 1024px)").addEventListener("change", function () {
    setOpen(false);
  });
})();

/* Diagnostic, inert unless the URL carries ?debug. Prints the viewport the
   browser is actually using, which is the one thing that cannot be measured
   from here. */
(function () {
  "use strict";
  if (location.search.indexOf("debug") === -1) return;
  var box = document.createElement("div");
  box.style.cssText = "position:fixed;z-index:99;left:0;top:0;" +
    "background:#000;color:#fff;font:12px monospace;padding:6px 10px";
  function show() {
    box.textContent =
      "css " + window.innerWidth + "x" + window.innerHeight +
      "  dpr " + window.devicePixelRatio +
      "  doc " + document.documentElement.scrollWidth +
      "x" + document.documentElement.scrollHeight;
  }
  show();
  window.addEventListener("resize", show);
  document.addEventListener("DOMContentLoaded", function () {
    document.body.appendChild(box);
  });
  if (document.body) document.body.appendChild(box);
})();
