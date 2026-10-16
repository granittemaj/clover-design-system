# Clover · coffee · wine · flowers

Brand system for **Clover**, a small place for coffee in the morning, wine in the evening and flowers all day: a hand-drawn four-leaf clover, a signature-script wordmark, and a golden-hour palette of cream, kraft and espresso.

**Site:** https://granittemaj.github.io/clover-design-system/ (the clover drawing itself, the four leaves, the board of applications, logo downloads, colours, type and the menu).

## What's here

| Path | What |
| --- | --- |
| `BRAND.md` | The brand book: voice, logo rules, colour, type, materials, the room. |
| `assets/Logos/` | 27 SVG logos: stacked and horizontal lockups (English and Albanian descriptor), round sign, mark, wordmark, avatars. |
| `tokens.json`, `tokens.css` | Colour (day cream / evening espresso), type, spacing, radius and shadow tokens. |
| `fonts/` | Allison (the wordmark script) and Mali (woff2). |
| `site/index.template.html` | The hand-written home page. |
| `index.html`, `assets/site/dapple.svg` | The generated site and its sunlight-through-leaves overlay. |
| `scripts/` | `build_clover.py` (logos), `tokens.py` (tokens.json with contrast checks), `tokens_css.py` (tokens.css), `build_pages.py` (the site). |

## Regenerating

Run from the repo root (needs `fonttools` and `brotli` for the logos):

```bash
python3 scripts/build_clover.py
```

```bash
python3 scripts/tokens.py tokens.json
```

```bash
python3 scripts/tokens_css.py
```

```bash
python3 scripts/build_pages.py
```
