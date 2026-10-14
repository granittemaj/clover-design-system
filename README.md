# Clover design system

Brand and UI system for **Clover**: a florist that is a café by day (kafe, matcha, ëmbëlsira) and a wine bar by evening (verë, meze). Four leaves, one for each part of the house.

**Site:** https://granittemaj.github.io/clover-design-system/ — the clover unfolding over the wordmark, a scroll story through one day at Clover (07:30 kafe → 11:00 lule → 15:00 ëmbëlsira → 19:00 verë), the mark's construction, colour, type and the shopfront at night. Also [logo guidelines](https://granittemaj.github.io/clover-design-system/logo.html) and [applications](https://granittemaj.github.io/clover-design-system/applications.html). It opens in the day palette before 17:00 and the evening palette after; add `?theme=light` or `?theme=dark` to a link to fix one.

## What's here

| Path | What |
| --- | --- |
| `BRAND.md` | The brand book: voice, day/evening rule, logo, colour, type, shape, icons, imagery, the room. Start here. |
| `tokens.json` | Source of truth for colours (Ditë/day and Mbrëmje/evening themes), type, spacing, radius and shadows. |
| `tokens.css` | CSS custom properties compiled from `tokens.json`. Day is the default; add `data-theme="dark"` for evening. |
| `assets/Logos/` | 18 outlined SVG logos (each leaf carries the crescent watermark of white clover): horizontal and stacked lockups, mark, wordmark, stamp, avatars. Day, evening, ink and paper versions. |
| `assets/Icons/` | 10 custom 24px line icons. |
| `fonts/` | Gloock, Familjen Grotesk and DM Mono (woff2, latin). |
| `components/` | React 18 components on `window.Clover` (`bundle.js`, `bundle.css`, `index.d.ts`), with a guideline `README.md` and a `preview.html` for each. `Logo/` and `Applications/` are showcase pages. |
| `site/index.template.html` | The hand-written home page. `scripts/build_pages.py` fills in the clover, marquee and shopfront and writes `index.html`. |
| `index.html`, `logo.html`, `applications.html` | The GitHub Pages site (generated). |
| `scripts/` | Generators: `build_clover.py` (logos), `tokens.py` (tokens.json with contrast checks), `tokens_css.py` (tokens.css), `build_pages.py` (the site). |

## Using it

```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components/bundle.css">
<script src="https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
<script src="components/bundle.js"></script>
```

The `preview.html` files are fragments meant to run with those four files already loaded, as the artifact does.

## Regenerating

```bash
python3 scripts/tokens_css.py
```

```bash
python3 scripts/build_pages.py
```

```bash
python3 scripts/build_clover.py fonts assets/Logos
```

`build_clover.py` needs `fonttools` and `brotli`. `tokens.py` takes the output path as its argument and fails if any text colour pair drops below WCAG AA.
