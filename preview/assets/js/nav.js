/* Header menu toggle.

   The nav starts with the `hidden` attribute in the markup, so with JavaScript
   unavailable the menu is simply absent rather than stuck open over the page. */
(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("hoofdmenu");
  if (!toggle || !nav) return;

  function setOpen(open) {
    nav.hidden = !open;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Menu sluiten" : "Menu openen");
  }

  toggle.addEventListener("click", function () {
    setOpen(nav.hidden);
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !nav.hidden) {
      setOpen(false);
      toggle.focus();
    }
  });

  /* A click anywhere else closes the menu. */
  document.addEventListener("click", function (event) {
    if (nav.hidden) return;
    if (nav.contains(event.target) || toggle.contains(event.target)) return;
    setOpen(false);
  });
})();
