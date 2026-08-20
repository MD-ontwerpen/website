# MD-ontwerpen — portfolio site

Static, bilingual (NL/EN) portfolio site. No build step, no dependencies to install.

```
website/
├── index.html              # the whole page
├── assets/
│   ├── css/styles.css      # design tokens + custom styles
│   └── js/
│       ├── i18n.js         # NL/EN switching
│       └── main.js         # theme, filtering, reveal, mobile nav
└── README.md
```

## Running it

Open `index.html` directly in a browser, or serve it locally:

```bash
python -m http.server 5510 --directory website
```

Then visit <http://localhost:5510>.

## Before it goes live — replace the placeholder content

Everything below is invented filler. It needs your real details.

| What | Where | Currently |
|------|-------|-----------|
| Email address | `index.html`, two `mailto:` links in the Contact section | `hallo@md-ontwerpen.nl` |
| The six projects | `assets/js/i18n.js`, keys `p1.*` … `p6.*` (both `nl` and `en`) | Invented studio work |
| Project thumbnails | `index.html`, the inline `<svg class="project-thumb">` in each card | Geometric placeholders |
| Statistics | `index.html`, the `<dl>` in the About section | 12 / 140+ / 68% |
| About copy | `assets/js/i18n.js`, keys `about.p1`, `about.p2` | Generic studio text |

Swapping a placeholder SVG for a real image:

```html
<img class="project-thumb" src="assets/img/project-1.webp"
     alt="Label design for Noordlicht Brewery" width="400" height="300" loading="lazy" />
```

Keep `width`/`height` so the space is reserved before the image loads, and write a real `alt`
describing the work — the SVG placeholders are `aria-hidden` because they carry no meaning, but
actual project images do.

## Adding a project

1. Copy a `<li class="project-card …">` block in `index.html`.
2. Set `data-category` to `branding`, `web`, or `print` — filtering keys off this.
3. Point its `data-i18n` attributes at new keys (`p7.title`, `p7.cat`, `p7.desc`).
4. Add those keys to **both** `nl` and `en` in `assets/js/i18n.js`.

## Design system

Generated with the `ui-ux-pro-max` skill and applied as follows:

- **Pattern** — Portfolio Grid: Hero → Project Grid → About → Contact, neutral background, filter by category
- **Style** — Brutalism: sharp corners, hard 2px borders, offset shadows, bold display type
- **Type** — Space Grotesk (display) + Archivo (body)
- **Colour** — monochrome with a blue accent; all tokens live at the top of `styles.css` and flip on `.dark`

Two deliberate departures from the generated system:

1. Brutalism specifies *no* transitions. The site keeps 150–300 ms hover/focus transitions, because
   instant state changes are listed as an anti-pattern in the same rule set and hurt perceived quality.
2. `--accent` (`#2563eb`) only reaches 4.35:1 against the muted panel, so accent-coloured text there
   uses `--accent-strong` (`#1d4ed8`, 5.64:1) instead.

## Accessibility

Verified in-browser, both themes:

- All text pairs ≥ 4.5:1; focus rings ≥ 3:1 (14/14 pass)
- Every control ≥ 44×44 px
- No horizontal scroll at 375 px
- Visible focus ring on every control; skip link to main content
- Filtering announced via `role="status"`, filtered cards `hidden` so they leave the tab order
- `<html lang>` updates with the language toggle
- `prefers-reduced-motion` disables reveals, smooth scrolling, and hover movement
- `scroll-padding-top` keeps anchor targets clear of the sticky header (WCAG 2.2 Focus Not Obscured)

## Deploying

Any static host — upload the `website/` folder as-is. Netlify, GitHub Pages, Cloudflare Pages,
or plain shared hosting all work with no configuration.

## One production note

Tailwind loads from a CDN and compiles in the browser. That is ideal for editing without a
toolchain, but it ships ~100 KB of JS and briefly delays styling on first paint. If the site gets
real traffic, swap it for a compiled stylesheet:

```bash
npx @tailwindcss/cli -i assets/css/tailwind-src.css -o assets/css/tailwind.css --minify
```

…then replace the CDN `<script>` with a `<link>` to the built file. Nothing else changes — the
custom classes in `styles.css` are plain CSS and do not depend on Tailwind.
