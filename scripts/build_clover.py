"""Clover logo system generator: the hand-drawn line clover and the handwritten wordmark.

Run from the repo root: python3 scripts/build_clover.py
Writes every logo SVG into assets/Logos/. Needs fonttools and brotli.

The clover is four clover leaves (wide round lobes, a notch, a short pointed base)
drawn as single pen strokes with a little seeded wobble, plus a stem. The pen never
quite closes each leaf at its base, so the centre stays open. The wordmark and the
descriptor are outlined: the name in Allison (a light signature script), the
descriptor in Mali Light, lowercase and widely spaced.
"""
import math
import os
import random

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

OUT = "assets/Logos"
os.makedirs(OUT, exist_ok=True)

INK = "#4B2E20"      # espresso
CREAM = "#F5EDE0"
KRAFT = "#C9A57E"
WINE = "#5C2230"

SCRIPT = TTFont("fonts/Allison-400.woff2")
BODY = TTFont("fonts/Mali-300.woff2")


def f(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# ------------------------------------------------------------------ the clover
def catmull(p):
    d = f"M{f(p[0][0])} {f(p[0][1])}"
    n = len(p)
    for i in range(n - 1):
        p0 = p[i - 1] if i > 0 else p[i]
        p1, p2 = p[i], p[i + 1]
        p3 = p[i + 2] if i + 2 < n else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d


# left half of one leaf, base at (0,0), lobes toward -y; mirrored for the right half
LEFT = [(-1.1, -1.7), (-2.8, -4.4), (-6.4, -9.0), (-11.0, -13.6), (-14.0, -18.6), (-14.6, -23.2),
        (-12.6, -27.2), (-8.6, -29.2), (-4.4, -28.4), (-1.4, -25.8), (0.0, -23.6)]

# (rotation from "up", length, width factor, seed): the lower pair spreads to make room for the stem
LEAVES = [(-44, 30.5, 1.00, 3), (42, 32.0, 1.04, 7), (120, 28.5, 0.98, 11), (238, 27.5, 1.02, 19)]
TILT = -6
CX, CY, GAP = 50, 40, 1.6


def leaf(length, width_k, seed, wobble=0.35):
    rnd = random.Random(seed)
    right = [(-x, y) for x, y in reversed(LEFT[:-1])]
    right[-1] = (1.3, -1.5)
    pts = LEFT + right
    s = length / 29.2
    out = []
    for i, (x, y) in enumerate(pts):
        jx, jy = (0, 0) if i in (0, len(pts) - 1) else (rnd.uniform(-wobble, wobble), rnd.uniform(-wobble, wobble))
        out.append(((x * width_k + jx) * s, (y + jy) * s))
    return out


def place(pts, rot, dx, dy):
    a = math.radians(rot)
    ca, sa = math.cos(a), math.sin(a)
    return [(x * ca - y * sa + dx, x * sa + y * ca + dy) for x, y in pts]


def clover_paths():
    paths = []
    for rot, ln, wk, seed in LEAVES:
        a = math.radians(rot)
        paths.append(catmull(place(leaf(ln, wk, seed), rot + TILT, CX + GAP * math.sin(a), CY - GAP * math.cos(a))))
    rnd = random.Random(42)
    stem = []
    for i in range(14):
        u = i / 13
        stem.append((CX + .6 + 2.2 * math.sin(u * 2.8) + 5.5 * u ** 2.2 + rnd.uniform(-.1, .1), CY + 3 + 45 * u))
    paths.append(catmull(stem))
    return paths


PATHS = clover_paths()
BOX = (17.6, 4.5, 82.4, 89.3)  # drawn extent of the clover in its 100 grid, stroke included


def clover(x, y, h, color, sw=2.5):
    """The clover with its drawn box scaled to height h, top-left at (x, y)."""
    x0, y0, x1, y1 = BOX
    s = h / (y1 - y0)
    body = "".join(f'<path d="{d}"/>' for d in PATHS)
    g = (f'<g transform="translate({f(x - x0 * s)} {f(y - y0 * s)}) scale({f(s)})" fill="none" stroke="{color}" '
         f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{body}</g>')
    return g, (x1 - x0) * s


# ------------------------------------------------------------------ type
def text(t, size, x, baseline, color, tracking=0.0, font=None):
    font = font or SCRIPT
    gs = font.getGlyphSet()
    cmap = font.getBestCmap()
    s = size / font["head"].unitsPerEm
    pen = SVGPathPen(gs)
    cur = x
    for ch in t:
        g = gs[cmap[ord(ch)]]
        g.draw(TransformPen(pen, (s, 0, 0, -s, cur, baseline)))
        cur += g.width * s + tracking * size
    return f'<path fill="{color}" d="{pen.getCommands()}"/>', cur - x - tracking * size


def centred(t, size, cx, baseline, color, tracking=0.0, font=None):
    _, w = text(t, size, 0, 0, color, tracking, font)
    return text(t, size, cx - w / 2, baseline, color, tracking, font)


def desc_text(t, size, x, baseline, color):
    return text(t, size, x, baseline, color, tracking=0.24, font=BODY)


def desc_centred(t, size, cx, baseline, color):
    return centred(t, size, cx, baseline, color, tracking=0.24, font=BODY)


def svg(w, h, body, bg=None, title="Clover"):
    rect = f'<rect width="{f(w)}" height="{f(h)}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {f(w)} {f(h)}" width="{f(w)}" height="{f(h)}" '
            f'role="img"><title>{title}</title>{rect}{body}</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), "w") as fh:
        fh.write(content)


if __name__ == "__main__":
    for old in os.listdir(OUT):
        if old.endswith(".svg"):
            os.remove(os.path.join(OUT, old))

    DESCRIPTORS = {"en": "coffee · wine · flowers", "sq": "kafe · verë · lule"}
    INKS = {"ink": INK, "cream": CREAM, "wine": WINE}
    mark_w = lambda h: (BOX[2] - BOX[0]) * h / (BOX[3] - BOX[1])

    SW = 2.2  # clover line, matched to Allison's light pen
    for slug, c in INKS.items():
        g, w = clover(10, 8, 104, c, sw=2.4)
        write(f"clover-mark-{slug}.svg", svg(math.ceil(w + 20), 120, g, title="Clover mark"))

    for slug, c in INKS.items():
        body, w = text("Clover", 260, 10, 190, c)
        write(f"clover-wordmark-{slug}.svg", svg(math.ceil(w + 30), 225, body, title="Clover"))

    for lang, desc in DESCRIPTORS.items():
        for slug, c in INKS.items():
            _, ww = text("Clover", 270, 0, 0, c)
            _, dw = desc_text(desc, 26, 0, 0, c)
            W = math.ceil(max(ww, dw) + 110)
            mh = 210
            g, _ = clover(W / 2 - mark_w(mh) / 2 - 6, 24, mh, c, sw=SW)
            base = 24 + mh + 170
            word, _ = centred("Clover", 270, W / 2 + 8, base, c)
            d, _ = desc_centred(desc, 26, W / 2, base + 92, c)
            write(f"clover-lockup-stacked-{lang}-{slug}.svg", svg(W, base + 122, g + word + d, title="Clover"))

    for lang, desc in DESCRIPTORS.items():
        for slug, c in INKS.items():
            mh = 200
            g, mw = clover(16, 14, mh, c, sw=SW)
            x = 16 + mw + 22
            word, ww = text("Clover", 240, x, 168, c)
            d, dw = desc_text(desc, 24, x + 30, 222, c)
            write(f"clover-lockup-horizontal-{lang}-{slug}.svg",
                  svg(math.ceil(x + max(ww, dw + 30) + 24), 250, g + word + d, title="Clover"))

    for lang, desc in DESCRIPTORS.items():
        for slug, (fg, bg) in {"cream": (INK, CREAM), "espresso": (CREAM, INK), "kraft": (INK, KRAFT)}.items():
            C = 300
            body = f'<circle cx="{C}" cy="{C}" r="{C - 4}" fill="{bg}"/>'
            body += f'<circle cx="{C}" cy="{C}" r="{C - 26}" fill="none" stroke="{fg}" stroke-width="3"/>'
            mh = 190
            g, _ = clover(C - mark_w(mh) / 2 - 4, 78, mh, fg, sw=SW + .2)
            word, _ = centred("Clover", 200, C + 6, 408, fg)
            d, _ = desc_centred(desc, 21, C, 470, fg)
            write(f"clover-badge-{lang}-{slug}.svg", svg(2 * C, 2 * C, body + g + word + d, title="Clover"))

    for slug, (fg, bg) in {"cream": (INK, CREAM), "espresso": (CREAM, INK), "kraft": (INK, KRAFT)}.items():
        mh = 300
        g, _ = clover(200 - mark_w(mh) / 2 - 6, 50, mh, fg, sw=2.6)
        write(f"clover-avatar-{slug}.svg", svg(400, 400, g, bg=bg, title="Clover"))

    print(len([n for n in os.listdir(OUT) if n.endswith(".svg")]), "logo files")
