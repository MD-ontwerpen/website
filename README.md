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
- **Style** — Minimalist Monochrome Editorial on a structural grid: sharp corners, hard 2px borders,
  restrained offset shadows
- **Type** — Playfair Display (display) + Source Serif 4 (body) + JetBrains Mono (labels, uppercase,
  wide tracking). Chosen to match the high-contrast serif of the MD-ontwerpen logo.
- **Colour** — monochrome with a blue accent; all tokens live at the top of `styles.css` and flip on `.dark`

Three deliberate departures from the generated system:

1. The first pass used Brutalism with Space Grotesk/Archivo. That clashed with the logo's refined
   serif, so the type was rebuilt around the logo and the brutalist shadows were softened.
2. The style specifies *no* transitions. The site keeps 150–300 ms hover/focus transitions, because
   instant state changes are listed as an anti-pattern in the same rule set and hurt perceived quality.
3. `--accent` (`#2563eb`) only reaches 4.35:1 against the muted panel, so accent-coloured text there
   uses `--accent-strong` (`#1d4ed8`, 5.64:1) instead.

## The logo

`assets/img/logo.svg` is what the site loads. It was traced from the supplied
print original, which was a 4500x4500 **CMYK JPEG** (2.6 MB) — a print export, not a
web asset. CMYK JPEGs render with wrong colours in some browsers, carry no transparency,
and 97% of that canvas was empty margin.

The traced SVG is 14 KB, crops to the artwork, and uses `fill="currentColor"`.

The header applies it as a **CSS mask** over a `currentColor` background:

```css
.site-logo {
  background-color: currentColor;
  mask: url("../img/logo.svg") no-repeat center / contain;
  aspect-ratio: 2200 / 1368;   /* matches the SVG viewBox */
}
```

That makes the logo follow the theme automatically — near-black in light mode,
near-white in dark — from a single file. An `<img>` could not do this: `currentColor`
inside an externally referenced SVG does not inherit the host page's colour. Browsers
without mask support fall back to the text wordmark via `@supports`.

The print original is **git-ignored** (`assets/img/logo*.jpg`) so it is never published.
Keep it — it is the source. To re-trace after a logo change:

```bash
python -m pip install Pillow potracer
```

then re-run the trace, thresholding the greyscale at 128 and passing the **inverted**
mask to `potrace.Bitmap` — it traces the `False` region, so passing `crop < 128`
produces the background instead of the letterforms.

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
