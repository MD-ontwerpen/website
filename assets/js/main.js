/* ==========================================================================
   MD-ontwerpen — Project filtering, scroll reveal, mobile nav
   ========================================================================== */

(function () {
  "use strict";

  /* ------------------------------------------------------------------------
     Project filtering
     ------------------------------------------------------------------------ */

  function initFilters() {
    var buttons = document.querySelectorAll("[data-filter]");
    var cards = document.querySelectorAll("[data-category]");
    var status = document.querySelector("[data-filter-status]");
    var empty = document.querySelector("[data-filter-empty]");
    if (!buttons.length || !cards.length) return;

    function applyFilter(value) {
      var shown = 0;

      cards.forEach(function (card) {
        var match = value === "all" || card.getAttribute("data-category") === value;
        // `hidden` keeps filtered-out cards out of the accessibility tree and
        // tab order, not just out of sight.
        card.hidden = !match;
        if (match) shown++;
      });

      buttons.forEach(function (btn) {
        btn.setAttribute(
          "aria-pressed",
          btn.getAttribute("data-filter") === value ? "true" : "false"
        );
      });

      if (empty) empty.hidden = shown > 0;

      // Announce the result — a purely visual change leaves screen reader
      // users with no idea the grid just changed.
      if (status) {
        var lang = window.mdI18n ? window.mdI18n.current() : "nl";
        status.textContent =
          lang === "nl"
            ? shown + (shown === 1 ? " project getoond" : " projecten getoond")
            : shown + (shown === 1 ? " project shown" : " projects shown");
      }
    }

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        applyFilter(btn.getAttribute("data-filter"));
      });
    });

    applyFilter("all");
  }

  /* ------------------------------------------------------------------------
     Scroll reveal
     ------------------------------------------------------------------------ */

  function initReveal() {
    var items = document.querySelectorAll(".reveal");
    if (!items.length) return;

    var reduced =
      window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    // No observer support, or the visitor asked for less motion: show everything.
    if (reduced || !("IntersectionObserver" in window)) {
      items.forEach(function (el) {
        el.classList.add("is-visible");
      });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target); // reveal once, then stop watching
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );

    items.forEach(function (el) {
      observer.observe(el);
    });
  }

  /* ------------------------------------------------------------------------
     Mobile navigation
     ------------------------------------------------------------------------ */

  function initMobileNav() {
    var toggle = document.querySelector("[data-nav-toggle]");
    var panel = document.querySelector("[data-nav-panel]");
    if (!toggle || !panel) return;

    function setOpen(open) {
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      panel.hidden = !open;
    }

    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });

    // Close after jumping to a section, so the panel doesn't cover the target
    panel.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        setOpen(false);
      });
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
        setOpen(false);
        toggle.focus(); // return focus rather than stranding it
      }
    });

    // Reset when crossing back to the desktop layout, where the panel is
    // always visible and the toggle is hidden.
    var mq = window.matchMedia("(min-width: 768px)");
    var onChange = function (e) {
      if (e.matches) setOpen(false);
    };
    if (mq.addEventListener) mq.addEventListener("change", onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }

  /* ------------------------------------------------------------------------
     Year stamp
     ------------------------------------------------------------------------ */

  function initYear() {
    var el = document.querySelector("[data-year]");
    if (el) el.textContent = String(new Date().getFullYear());
  }

  function init() {
    initFilters();
    initReveal();
    initMobileNav();
    initYear();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
