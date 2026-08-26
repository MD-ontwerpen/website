/* Header menu toggle, for the collapsed layout only.

   Visibility is driven by data-open rather than the `hidden` attribute, because
   `hidden` would also hide the inline nav above the breakpoint, where there is
   no toggle to bring it back. Above 900px these handlers still run but the CSS
   ignores data-open, so the nav stays inline. */
(function () {
  "use strict";

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("hoofdmenu");
  if (!toggle || !nav) return;

  function isOpen() {
    return nav.getAttribute("data-open") === "true";
  }

  function setOpen(open) {
    nav.setAttribute("data-open", String(open));
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Menu sluiten" : "Menu openen");
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

  /* Leaving the collapsed layout with the panel open would otherwise strand
     data-open="true" on the inline nav. */
  window.matchMedia("(min-width: 900px)").addEventListener("change", function (e) {
    if (e.matches) setOpen(false);
  });
})();
