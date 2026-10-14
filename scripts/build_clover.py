"""Clover logo system generator.

Four heart-shaped leaves, one per thing the house does (lule, kafe, ëmbëlsira,
verë), a stem through the diagonal gap, and the wordmark outlined from Gloock.
Run: python3 build_clover.py <fontdir> <outdir>
"""
import math
import os
import sys

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONTDIR, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

DAY = dict(ink="#1E2A1F", peony="#B02A5A", matcha="#4A671B", candle="#C08A1E", wine="#5E1A33", ground="#F3F4EC")
EVE = dict(ink="#F4E9EC", peony="#F28DB0", matcha="#A9C56B", candle="#EDB54E", wine="#C25A7C", ground="#1C1016")
PAPER = "#F3F4EC"

gloock = TTFont(os.path.join(FONTDIR, "Gloock-Regular.woff2"))
grotesk = TTFont(os.path.join(FONTDIR, "FamiljenGrotesk-Variable.woff2"))


def fmt(n):
    s = f"{n:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ------------------------------------------------------------------ the mark
# One leaf: a heart, tip at (0,0), lobes pointing up (negative y). 30 wide, 31 tall.
LEAF = ("M0 0C-3.6-3.4-15-9.6-15-20.4C-15-27.4-9.6-31.4-4.6-30.6"
        "C-2.2-30.2-.6-28.6 0-26.4C.6-28.6 2.2-30.2 4.6-30.6"
        "C9.6-31.4 15-27.4 15-20.4C15-9.6 3.6-3.4 0 0Z")
GAP = 5.6  # tip distance from the centre: the cut between leaves
CX, CY = 50, 46
# leaf order: top = lule (peony), right = kafe/matcha, bottom = verë (wine), left = ëmbëlsira (candle)
LEAVES = [("peony", 45), ("matcha", 135), ("wine", 225), ("candle", 315)]
STEM_D = "M50 60C50 70 51 78.5 56.5 86.5"  # drops through the cut between the two lower leaves
STEM_W = 4.2
BOX = (13.7, 9.7, 86.3, 88.6)  # drawn extent incl. the stem cap


def leaf_path(rot):
    return f'transform="rotate({rot} {CX} {CY}) translate({CX} {CY - GAP})" d="{LEAF}"'


def mark_body(colors, mono=None):
    parts = []
    for key, rot in LEAVES:
        fill = mono or colors[key]
        parts.append(f'<path fill="{fill}" {leaf_path(rot)}/>')
    stem = mono or colors["ink"]
    parts.append(f'<path fill="none" stroke="{stem}" stroke-width="{STEM_W}" stroke-linecap="round" d="{STEM_D}"/>')
    return "".join(parts)


def mark_group(x, y, h, colors, mono=None):
    x0, y0, x1, y1 = BOX
    s = h / (y1 - y0)
    return (f'<g transform="translate({fmt(x - x0 * s)} {fmt(y - y0 * s)}) scale({fmt(s)})">{mark_body(colors, mono)}</g>',
            (x1 - x0) * s)


# ------------------------------------------------------------------ type
def text_path(font, text, size, x, baseline, tracking=0.0, wght=None):
    gs = font.getGlyphSet(location={"wght": wght} if wght else None)
    cmap = font.getBestCmap()
    s = size / font["head"].unitsPerEm
    pen = SVGPathPen(gs)
    cursor = x
    for ch in text:
        g = gs[cmap[ord(ch)]]
        g.draw(TransformPen(pen, (s, 0, 0, -s, cursor, baseline)))
        cursor += g.width * s + tracking * size
    return pen.getCommands(), cursor - x - tracking * size


def wordmark(size, x, baseline, fill):
    d, w = text_path(gloock, "clover", size, x, baseline, tracking=-0.01)
    return f'<path fill="{fill}" d="{d}"/>', w


def descriptor(text, size, cx, baseline, fill, tracking=0.22):
    d, w = text_path(grotesk, text, size, 0, baseline, tracking=tracking, wght=560)
    return f'<path fill="{fill}" transform="translate({fmt(cx - w / 2)} 0)" d="{d}"/>', w


def svg(w, h, body, bg=None, title="Clover"):
    rect = f'<rect width="{fmt(w)}" height="{fmt(h)}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(w)} {fmt(h)}" width="{fmt(w)}" '
            f'height="{fmt(h)}" role="img"><title>{title}</title>{rect}{body}</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)


# variants: (slug, leaf colours, mono ink, word ink)
VARIANTS = [
    ("day", DAY, None, DAY["ink"]),
    ("evening", EVE, None, EVE["ink"]),
    ("ink", DAY, DAY["ink"], DAY["ink"]),
    ("paper", DAY, PAPER, PAPER),
]

# 1. mark
for slug, cols, mono, _ in VARIANTS:
    g, mw = mark_group(8, 8, 84, cols, mono)
    write(f"clover-mark-{slug}.svg", svg(math.ceil(mw + 16), 100, g, title="Clover mark"))

# 2. wordmark
for slug, cols, mono, ink in [("ink", DAY, None, DAY["ink"]), ("paper", DAY, None, PAPER)]:
    body, w = wordmark(120, 0, 100, ink)
    write(f"clover-wordmark-{slug}.svg", svg(math.ceil(w) + 2, 116, body, title="Clover"))

# 3. horizontal lockup: mark spans the ascender, the stem ends near the baseline
asc = 788 / 1000 * 120
for slug, cols, mono, ink in VARIANTS:
    base = 120
    mh = asc * 1.08
    mg, mw = mark_group(0, base - asc * 1.03, mh, cols, mono)
    wm, ww = wordmark(120, mw + 30, base, ink)
    write(f"clover-lockup-horizontal-{slug}.svg", svg(math.ceil(mw + 30 + ww + 2), 140, mg + wm, title="Clover"))

# 4. stacked lockup
for slug, cols, mono, ink in VARIANTS:
    _, ww = wordmark(120, 0, 0, ink)
    W = math.ceil(ww) + 40
    mh = 170
    mw = (BOX[2] - BOX[0]) * mh / (BOX[3] - BOX[1])
    mg, _ = mark_group(W / 2 - mw / 2, 10, mh, cols, mono)
    wm, _ = wordmark(120, 20, 10 + mh + 120, ink)
    ds, _ = descriptor("LULE · KAFE · VERË", 22, W / 2, 10 + mh + 120 + 58, ink)
    write(f"clover-lockup-stacked-{slug}.svg", svg(W, 10 + mh + 120 + 74, mg + wm + ds, title="Clover"))


# 5. stamp
def ring_text(text, size, cx, cy, r, fill, start_deg=-90, tracking=0.12, wght=600):
    gs = grotesk.getGlyphSet(location={"wght": wght})
    cmap = grotesk.getBestCmap()
    s = size / grotesk["head"].unitsPerEm
    widths = [gs[cmap[ord(c)]].width * s + tracking * size for c in text]
    circ = 2 * math.pi * r
    k = circ / sum(widths)
    out, run = [], 0.0
    for c, wd in zip(text, widths):
        wd *= k
        ang = start_deg + (run + wd / 2) / circ * 360
        rad = math.radians(ang)
        g = gs[cmap[ord(c)]]
        pen = SVGPathPen(gs)
        g.draw(TransformPen(pen, (s, 0, 0, -s, -g.width * s / 2, 0)))
        d = pen.getCommands()
        if d:
            out.append(f'<path fill="{fill}" transform="translate({fmt(cx + r * math.cos(rad))} {fmt(cy + r * math.sin(rad))}) rotate({fmt(ang + 90)})" d="{d}"/>')
        run += wd
    return "".join(out)


for slug, cols, ink, bg in [("day", DAY, DAY["ink"], None), ("evening", EVE, EVE["ink"], EVE["ground"])]:
    C = 160
    body = f'<circle cx="{C}" cy="{C}" r="{C}" fill="{bg}"/>' if bg else ""
    body += f'<circle cx="{C}" cy="{C}" r="150" fill="none" stroke="{ink}" stroke-width="3"/>'
    body += f'<circle cx="{C}" cy="{C}" r="98" fill="none" stroke="{ink}" stroke-width="1.5"/>'
    body += ring_text("CLOVER · LULE · KAFE · ËMBËLSIRA · VERË · ", 26, C, C, 114, ink)
    mh = 112
    mw = (BOX[2] - BOX[0]) * mh / (BOX[3] - BOX[1])
    g, _ = mark_group(C - mw / 2, C - mh / 2, mh, cols)
    write(f"clover-stamp-{slug}.svg", svg(320, 320, body + g, title="Clover stamp"))

# 6. avatars
for slug, cols, bg in [("day", DAY, DAY["ground"]), ("evening", EVE, EVE["ground"])]:
    mh = 120
    mw = (BOX[2] - BOX[0]) * mh / (BOX[3] - BOX[1])
    g, _ = mark_group(100 - mw / 2, 100 - mh / 2, mh, cols)
    write(f"clover-avatar-{slug}.svg", svg(200, 200, g, bg=bg, title="Clover avatar"))

print("ok", sorted(os.listdir(OUT)))
