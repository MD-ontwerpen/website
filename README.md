# MD-ontwerpen — portfolio site

Static, bilingual (NL/EN) portfolio site. No build step, no dependencies to install.

```
website/
├── index.html              # the whole page
├── assets/
│   ├── css/styles.css      # design tokens + custom styles
│   ├── img/logo.svg        # traced wordmark, painted via CSS mask
│   └── js/
│       ├── i18n.js         # NL/EN switching
│       └── main.js         # filtering, reveal, mobile nav
└── README.md
```

## Running it

Open `index.html` directly in a browser, or serve it locally:

```bash
python -m http.server 5510 --directory website
```

Then visit <http://localhost:5510>.

## What this site is

MD-ontwerpen is a practice for **architecture, building engineering and construction
management**. The site has a homepage plus one page per service in `diensten/`.

> Earlier versions of this site described a graphic-design studio. That was wrong -
> the copy, the projects and the metadata have all been rewritten.

## Regenerating the generated parts

Three scripts build the repetitive parts. Run them from `website/`:

```bash
python build-service-images.py
```
```bash
python build-service-pages.py
```

- `build-service-images.py` - one shared building-section drawing plus a highlight
  variant per service, into `assets/img/diensten/`. The base geometry is identical in
  every file; only the highlight layer differs, so the set reads as one system.
- `build-service-pages.py` - the 13 pages in `diensten/`. All article copy lives in
  this file's `SERVICES` list; edit it there and re-run rather than editing the HTML.
- `build_service_data.py` - the short card text shared by the homepage grid and sitemap.

`build-home.py` and `build-copy.py` were one-time migration scripts for the rewrite.
They are kept for reference but are not idempotent - do not re-run them.

## The layered 3D model

`assets/models/gebouw-lagen.glb` (86 KB, 2,632 triangles) holds one building whose
meshes are named `layer_<slug>__<part>`. The viewer groups meshes by that prefix, so
selecting a service highlights its layer and ghosts the rest - the 3D counterpart of
the per-service drawings.

```bash
python build-model.py
```

Two things that are easy to get wrong here:

- **The model is authored Z-up** (building convention) and rotated to **Y-up** before
  export, because glTF requires Y-up. Without that rotation the building loads lying
  on its side in every viewer.
- **Materials, not face colours.** Face colours are baked to per-vertex data on export,
  which needs scipy and inflates the file. One PBR material per mesh is also what the
  viewer swaps when highlighting.

The viewer (`assets/js/viewer.js`) is vanilla Three.js loaded from a CDN via the
**import map in `index.html`** - the three.js addons import from a bare `"three"`
specifier, which a browser cannot resolve without it. The map points at the minified
build (692 KB, not 1.3 MB).

Guards, per the `3d-web-experience` skill's anti-patterns:

- Nothing is downloaded until the visitor presses the button, so the page keeps its
  sub-second load; the static drawing shows until then
- 3D is not offered at all without WebGL, or under reduced-motion, save-data, or on
  a machine reporting two cores or fewer - and it says why rather than failing silently
- Explicit load progress, because a blank canvas reads as broken
- Device pixel ratio capped at 2, and frames render on demand rather than in a loop

**The model is placeholder massing, not a real project.** Replace it with an ArchiCAD
export when one is available; keep the `layer_<slug>__<part>` naming and the viewer
works unchanged.

## Still placeholder

| What | Where | Currently |
|------|-------|-----------|
| Email address | `index.html`, two `mailto:` links in Contact | `hallo@md-ontwerpen.nl` |
| Statistics | `index.html`, the `<dl>` in the About section | 12 / 140+ / 68% |
| Testimonials | `assets/js/i18n.js`, keys `r1.*` … `r3.*` | Bracketed placeholders |

**The three statistics are invented and are visible on a live, indexed site.** They
read as claims the practice is making about itself. Replace them with real figures or
remove the block.

The service articles describe what each discipline involves. They make no claim about
experience, project count or clients - that is deliberate, and anything of that kind
must be true before it goes in.

## Design system

Generated with the `ui-ux-pro-max` skill and applied as follows:

- **Pattern** — Portfolio Grid: Hero → Project Grid → About → Contact, neutral background, filter by category
- **Style** — Minimalist Monochrome Editorial on a structural grid: sharp corners, hard 2px borders,
  restrained offset shadows
- **Type** — Roboto (display and body) + Roboto Mono (labels, uppercase,
  wide tracking).
- **Colour** — monochrome with a blue accent, **light mode only**; all tokens live at the top of `styles.css`

Three deliberate departures from the generated system:

1. The first pass used Brutalism with Space Grotesk/Archivo, then an editorial serif pairing
   (Playfair Display / Source Serif 4) chosen to match the logo. Roboto was requested instead,
   so the type is now a neutral grotesque and does not track the logo's serif character.
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

The logo therefore takes its colour from the surrounding text rather than having it
baked in, and stays crisp at any size. An `<img>` could not do this: `currentColor`
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

Verified in-browser:

- All text pairs ≥ 4.5:1; focus rings ≥ 3:1 (8/8 pass)
- Every control ≥ 44×44 px
- No horizontal scroll at 375 px
- Visible focus ring on every control; skip link to main content
- Filtering announced via `role="status"`, filtered cards `hidden` so they leave the tab order
- `<html lang>` updates with the language toggle
- `prefers-reduced-motion` disables reveals, smooth scrolling, and hover movement
- The menu button is hidden at ≥768px by an explicit media query, because `.control`
  sets `display` in this stylesheet and would otherwise override Tailwind's `md:hidden`
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
