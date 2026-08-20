/* ==========================================================================
   MD-ontwerpen — Bilingual (NL/EN) content switching
   --------------------------------------------------------------------------
   Elements opt in with data-i18n="key" for text content, or
   data-i18n-attr="attribute:key" for attributes (aria-label, alt, content).
   The <html lang> attribute is updated alongside the copy so screen readers
   switch pronunciation, and the choice persists in localStorage.
   ========================================================================== */

(function () {
  "use strict";

  var STORAGE_KEY = "md-ontwerpen:lang";
  var DEFAULT_LANG = "nl";

  var translations = {
    nl: {
      "meta.title": "MD-ontwerpen — Grafisch ontwerp & visuele identiteit",
      "meta.description":
        "Studio voor grafisch ontwerp, merkidentiteit en digitaal ontwerp. Werk dat helder is, standhoudt en klopt.",

      "nav.skip": "Ga direct naar de inhoud",
      "nav.work": "Werk",
      "nav.about": "Over",
      "nav.contact": "Contact",
      "nav.reviews": "Referenties",
      "nav.menu": "Menu openen",

      "hero.eyebrow": "Ontwerpstudio — beschikbaar voor opdrachten",
      "hero.title": "Ontwerp dat blijft staan.",
      "hero.lead":
        "MD-ontwerpen is een studio voor merkidentiteit, drukwerk en digitaal ontwerp. Geen ruis, geen trucs — alleen werk dat doet wat het moet doen.",
      "hero.cta1": "Bekijk het werk",
      "hero.cta2": "Neem contact op",
      "hero.scroll": "Scroll",

      "work.eyebrow": "Geselecteerd werk",
      "work.title": "Projecten",
      "work.lead":
        "Een selectie uit recente opdrachten in identiteit, digitaal en drukwerk.",
      "work.filterLabel": "Filter projecten op categorie",
      "work.empty": "Geen projecten in deze categorie.",

      "filter.all": "Alles",
      "filter.branding": "Identiteit",
      "filter.web": "Digitaal",
      "filter.print": "Drukwerk",

      "p1.title": "Noordlicht Brouwerij",
      "p1.cat": "Identiteit",
      "p1.desc": "Volledige merkidentiteit en etiketontwerp voor een ambachtelijke brouwerij.",
      "p2.title": "Kade 14",
      "p2.cat": "Digitaal",
      "p2.desc": "Website en boekingssysteem voor een culturele broedplaats.",
      "p3.title": "Jaarverslag 2025",
      "p3.cat": "Drukwerk",
      "p3.desc": "Redactioneel ontwerp en infographics voor een non-profit.",
      "p4.title": "Studio Vlinder",
      "p4.cat": "Identiteit",
      "p4.desc": "Logo, typografisch systeem en huisstijl voor een fotograaf.",
      "p5.title": "Veldkeuken",
      "p5.cat": "Digitaal",
      "p5.desc": "Bestelplatform en menukaartsysteem voor een restaurantgroep.",
      "p6.title": "Tentoonstelling — Vorm",
      "p6.cat": "Drukwerk",
      "p6.desc": "Affiches, signage en catalogus voor een museumtentoonstelling.",
      "p.view": "Bekijk project",

      "about.eyebrow": "Over de studio",
      "about.title": "Klein, scherp, betrokken.",
      "about.p1":
        "MD-ontwerpen werkt direct met opdrachtgevers — zonder tussenlagen. Dat betekent korte lijnen, snelle beslissingen en een ontwerper die het hele traject kent.",
      "about.p2":
        "Elk project begint met de vraag waarom iets bestaat. Pas daarna komt de vorm. Die volgorde levert werk op dat over vijf jaar nog steeds klopt.",
      "about.servicesTitle": "Diensten",
      "about.s1": "Merkidentiteit & logo-ontwerp",
      "about.s2": "Websites & digitale producten",
      "about.s3": "Drukwerk & redactioneel ontwerp",
      "about.s4": "Signage & tentoonstellingsontwerp",
      "about.stat1": "Jaar ervaring",
      "about.stat2": "Projecten opgeleverd",
      "about.stat3": "Terugkerende klanten",

      "reviews.eyebrow": "Referenties",
      "reviews.title": "Wat klanten zeggen",
      "reviews.lead": "Een greep uit de reacties van opdrachtgevers.",
      // PLACEHOLDERS - vervang door echte quotes, met toestemming van de klant.
      "r1.quote": "[ Vervang dit door een echte quote van een klant ]",
      "r1.name": "[ Naam klant ]",
      "r1.role": "[ Functie, Bedrijf ]",
      "r2.quote": "[ Vervang dit door een echte quote van een klant ]",
      "r2.name": "[ Naam klant ]",
      "r2.role": "[ Functie, Bedrijf ]",
      "r3.quote": "[ Vervang dit door een echte quote van een klant ]",
      "r3.name": "[ Naam klant ]",
      "r3.role": "[ Functie, Bedrijf ]",

      "contact.eyebrow": "Contact",
      "contact.title": "Een project in gedachten?",
      "contact.lead":
        "Vertel kort waar het over gaat en wat de planning is. Ik reageer binnen twee werkdagen.",
      "contact.cta": "Stuur een e-mail",
      "contact.alt": "Of vind de studio hier:",
      "contact.location": "Gevestigd in Nederland — werkzaam in heel Europa.",

      "footer.rights": "Alle rechten voorbehouden.",
      "footer.top": "Terug naar boven",

      "aria.langNL": "Schakel naar Nederlands",
      "aria.langEN": "Schakel naar Engels",
      "aria.langGroup": "Taalkeuze",
    },

    en: {
      "meta.title": "MD-ontwerpen — Graphic design & visual identity",
      "meta.description":
        "A studio for graphic design, brand identity and digital design. Work that is clear, durable, and right.",

      "nav.skip": "Skip to main content",
      "nav.work": "Work",
      "nav.about": "About",
      "nav.contact": "Contact",
      "nav.reviews": "Reviews",
      "nav.menu": "Open menu",

      "hero.eyebrow": "Design studio — available for commissions",
      "hero.title": "Design that holds up.",
      "hero.lead":
        "MD-ontwerpen is a studio for brand identity, print and digital design. No noise, no tricks — just work that does what it needs to do.",
      "hero.cta1": "See the work",
      "hero.cta2": "Get in touch",
      "hero.scroll": "Scroll",

      "work.eyebrow": "Selected work",
      "work.title": "Projects",
      "work.lead":
        "A selection of recent commissions across identity, digital and print.",
      "work.filterLabel": "Filter projects by category",
      "work.empty": "No projects in this category.",

      "filter.all": "All",
      "filter.branding": "Identity",
      "filter.web": "Digital",
      "filter.print": "Print",

      "p1.title": "Noordlicht Brewery",
      "p1.cat": "Identity",
      "p1.desc": "Full brand identity and label design for a craft brewery.",
      "p2.title": "Kade 14",
      "p2.cat": "Digital",
      "p2.desc": "Website and booking system for a cultural venue.",
      "p3.title": "Annual Report 2025",
      "p3.cat": "Print",
      "p3.desc": "Editorial design and infographics for a non-profit.",
      "p4.title": "Studio Vlinder",
      "p4.cat": "Identity",
      "p4.desc": "Logo, type system and house style for a photographer.",
      "p5.title": "Veldkeuken",
      "p5.cat": "Digital",
      "p5.desc": "Ordering platform and menu system for a restaurant group.",
      "p6.title": "Exhibition — Form",
      "p6.cat": "Print",
      "p6.desc": "Posters, signage and catalogue for a museum exhibition.",
      "p.view": "View project",

      "about.eyebrow": "About the studio",
      "about.title": "Small, sharp, involved.",
      "about.p1":
        "MD-ontwerpen works directly with clients — no layers in between. That means short lines, fast decisions, and one designer who knows the whole project.",
      "about.p2":
        "Every project starts with why the thing exists. Form comes after. That order produces work that still makes sense five years on.",
      "about.servicesTitle": "Services",
      "about.s1": "Brand identity & logo design",
      "about.s2": "Websites & digital products",
      "about.s3": "Print & editorial design",
      "about.s4": "Signage & exhibition design",
      "about.stat1": "Years experience",
      "about.stat2": "Projects delivered",
      "about.stat3": "Returning clients",

      "reviews.eyebrow": "References",
      "reviews.title": "What clients say",
      "reviews.lead": "A few words from the people I have worked with.",
      // PLACEHOLDERS - replace with real quotes, used with the client's permission.
      "r1.quote": "[ Replace this with a real client quote ]",
      "r1.name": "[ Client name ]",
      "r1.role": "[ Role, Company ]",
      "r2.quote": "[ Replace this with a real client quote ]",
      "r2.name": "[ Client name ]",
      "r2.role": "[ Role, Company ]",
      "r3.quote": "[ Replace this with a real client quote ]",
      "r3.name": "[ Client name ]",
      "r3.role": "[ Role, Company ]",

      "contact.eyebrow": "Contact",
      "contact.title": "Got a project in mind?",
      "contact.lead":
        "Tell me briefly what it is and what the timeline looks like. I reply within two working days.",
      "contact.cta": "Send an email",
      "contact.alt": "Or find the studio here:",
      "contact.location": "Based in the Netherlands — working across Europe.",

      "footer.rights": "All rights reserved.",
      "footer.top": "Back to top",

      "aria.langNL": "Switch to Dutch",
      "aria.langEN": "Switch to English",
      "aria.langGroup": "Language selection",
    },
  };

  /** Resolve the starting language: saved choice → browser hint → default. */
  function initialLang() {
    var saved;
    try {
      saved = localStorage.getItem(STORAGE_KEY);
    } catch (e) {
      saved = null; // private mode / storage disabled
    }
    if (saved && translations[saved]) return saved;

    var nav = (navigator.language || "").toLowerCase();
    if (nav.indexOf("nl") === 0) return "nl";
    if (nav.indexOf("en") === 0) return "en";
    return DEFAULT_LANG;
  }

  function t(lang, key) {
    var dict = translations[lang] || translations[DEFAULT_LANG];
    return Object.prototype.hasOwnProperty.call(dict, key) ? dict[key] : null;
  }

  function apply(lang) {
    var dict = translations[lang];
    if (!dict) return;

    // Text nodes
    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var value = t(lang, el.getAttribute("data-i18n"));
      if (value !== null) el.textContent = value;
    });

    // Attributes: data-i18n-attr="aria-label:aria.themeToDark"
    document.querySelectorAll("[data-i18n-attr]").forEach(function (el) {
      el.getAttribute("data-i18n-attr")
        .split(";")
        .forEach(function (pair) {
          var parts = pair.split(":");
          if (parts.length !== 2) return;
          var attr = parts[0].trim();
          var value = t(lang, parts[1].trim());
          if (value !== null) el.setAttribute(attr, value);
        });
    });

    // Document-level metadata
    var title = t(lang, "meta.title");
    if (title) document.title = title;

    var desc = document.querySelector('meta[name="description"]');
    var descText = t(lang, "meta.description");
    if (desc && descText) desc.setAttribute("content", descText);

    // Tell assistive tech which language is being spoken
    document.documentElement.setAttribute("lang", lang);

    // Reflect state on the toggle buttons
    document.querySelectorAll("[data-lang-set]").forEach(function (btn) {
      btn.setAttribute(
        "aria-pressed",
        btn.getAttribute("data-lang-set") === lang ? "true" : "false"
      );
    });

    try {
      localStorage.setItem(STORAGE_KEY, lang);
    } catch (e) {
      /* not fatal — the page still works, the choice just won't persist */
    }
  }

  function init() {
    apply(initialLang());

    document.querySelectorAll("[data-lang-set]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        apply(btn.getAttribute("data-lang-set"));
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // Exposed so main.js can re-translate the filter's live region
  window.mdI18n = {
    t: t,
    current: function () {
      return document.documentElement.getAttribute("lang") || DEFAULT_LANG;
    },
  };
})();
