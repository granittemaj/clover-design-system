"""Build the GitHub Pages site (index.html) from site/index.template.html.

Run from the repo root: python3 scripts/build_pages.py
Fills in the hand-drawn clover (from scripts/build_clover.py), the single-leaf
drawings, the board of illustrated mockups, and writes assets/site/dapple.svg,
the sunlight-through-leaves overlay.
"""
import importlib.util
import math
import os
import random

spec = importlib.util.spec_from_file_location("bc", "scripts/build_clover.py")
bc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bc)

LOGO = "assets/Logos"
INK, CREAM, KRAFT = "#4B2E20", "#F5EDE0", "#C9A57E"
VB = "17.6 4.5 64.8 84.8"


def f(v):
    return bc.f(v)


def lockup_ratio(name):
    import re
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', open(f"{LOGO}/{name}").read())
    return float(m.group(2)) / float(m.group(1))


STACK = "clover-lockup-stacked-en-ink.svg"
STACK_R = lockup_ratio(STACK)
MARK = "clover-mark-ink.svg"
MARK_R = lockup_ratio(MARK)
BADGE = "clover-badge-en-cream.svg"


def img(name, x, y, w, ratio, extra=""):
    return f'<image href="{LOGO}/{name}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(w * ratio)}" {extra}/>'


# ------------------------------------------------------------------ the clover
def clover_draw():
    paths = "".join(f'<path pathLength="1" d="{d}"/>' for d in bc.PATHS)
    return f'<svg viewBox="{VB}" role="img" aria-label="Clover">{paths}</svg>'


def mini():
    paths = "".join(f'<path d="{d}"/>' for d in bc.PATHS)
    return (f'<svg viewBox="{VB}" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="3.6" '
            f'stroke-linecap="round" stroke-linejoin="round">{paths}</g></svg>')


def single_leaf():
    pts = bc.leaf(68, 1.0, 7)
    return bc.catmull([(x + 50, y + 86) for x, y in pts])


# ------------------------------------------------------------------ sunlight overlay
def dapple():
    rnd = random.Random(5)
    shapes = []
    leaf = bc.catmull(bc.leaf(29.2, 1.0, 3) + [bc.leaf(29.2, 1.0, 3)[0]])
    for _ in range(70):
        x, y = rnd.uniform(-100, 1700), rnd.uniform(-100, 1100)
        s = rnd.uniform(1.6, 4.2)
        r = rnd.uniform(0, 360)
        shapes.append(f'<path d="{leaf}" transform="translate({x:.0f} {y:.0f}) rotate({r:.0f}) scale({s:.2f})"/>')
    for _ in range(40):
        x, y = rnd.uniform(-100, 1700), rnd.uniform(-100, 1100)
        shapes.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(30, 90):.0f}" ry="{rnd.uniform(12, 40):.0f}" '
                      f'transform="rotate({rnd.uniform(0, 180):.0f} {x:.0f} {y:.0f})"/>')
    branches = "".join(
        f'<path d="M{rnd.uniform(-100, 1700):.0f} -60 Q{rnd.uniform(0, 1600):.0f} {rnd.uniform(300, 700):.0f} {rnd.uniform(-100, 1700):.0f} 1100" '
        f'fill="none" stroke="#3a2614" stroke-width="{rnd.uniform(6, 14):.0f}"/>' for _ in range(5))
    os.makedirs("assets/site", exist_ok=True)
    open("assets/site/dapple.svg", "w").write(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 1000" preserveAspectRatio="xMidYMid slice">'
        '<filter id="b" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="16"/></filter>'
        f'<g filter="url(#b)" fill="#3a2614">{branches}{"".join(shapes)}</g></svg>\n')


# ------------------------------------------------------------------ board illustrations
def flowers(cx, cy, spread, n, seed, kinds=("daisy", "blush", "pink", "daisy"), scale=1.0):
    rnd = random.Random(seed)
    out_leaves, out_heads = [], []
    for _ in range(n + 4):
        x, y = cx + rnd.uniform(-spread, spread), cy + rnd.uniform(-spread * .5, spread * .45)
        out_leaves.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{rnd.uniform(5, 9) * scale:.1f}" ry="{rnd.uniform(2.4, 3.6) * scale:.1f}" '
                          f'fill="{rnd.choice(["#6F7F57", "#8E9C77", "#5E6E4C"])}" transform="rotate({rnd.uniform(0, 180):.0f} {x:.1f} {y:.1f})"/>')
    for i in range(n):
        x, y = cx + rnd.uniform(-spread, spread), cy + rnd.uniform(-spread * .55, spread * .35)
        k = kinds[i % len(kinds)]
        r = rnd.uniform(6.5, 9.5) * scale
        if k == "daisy":
            petals = "".join(f'<ellipse cx="{x + r * .55 * math.cos(math.radians(a)):.1f}" cy="{y + r * .55 * math.sin(math.radians(a)):.1f}" '
                             f'rx="{r * .55:.1f}" ry="{r * .22:.1f}" fill="#FFFDF7" transform="rotate({a} {x + r * .55 * math.cos(math.radians(a)):.1f} {y + r * .55 * math.sin(math.radians(a)):.1f})"/>'
                             for a in range(0, 360, 30))
            out_heads.append(petals + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * .28:.1f}" fill="#E2B23F"/>')
        else:
            col = {"blush": "#EBCBC6", "pink": "#D99AA5", "rose": "#C77C88"}[k]
            out_heads.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{col}"/>'
                             f'<path d="M{x - r * .4:.1f} {y:.1f}a{r * .4:.1f} {r * .4:.1f} 0 1 1 {r * .5:.1f} {r * .25:.1f}" fill="none" stroke="#00000022" stroke-width="1.2"/>')
    return "".join(out_leaves) + "".join(out_heads)


def foliage(rnd, cx, cy, spread, n):
    """A loose cluster of olive-like leaves, each rotated about its own centre."""
    out = []
    for _ in range(n):
        x, y = cx + rnd.gauss(0, spread * .45), cy + rnd.gauss(0, spread * .4)
        out.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(6, 12):.0f}" ry="{rnd.uniform(2.6, 4.6):.1f}" '
                   f'fill="{rnd.choice(["#7d8c63", "#8E9C77", "#66754f", "#94a37c"])}" transform="rotate({rnd.uniform(-80, 80):.0f} {x:.0f} {y:.0f})"/>')
    return "".join(out)


def tile(cls, cap, vb, body, defs=""):
    return (f'    <div class="tile {cls} rv" tabindex="0" aria-label="{cap}"><svg viewBox="{vb}" preserveAspectRatio="xMidYMid slice" aria-hidden="true">'
            f'<defs>{defs}</defs>{body}</svg><span class="cap">{cap}</span></div>')


def t_logo():
    defs = '<radialGradient id="lg-bg" cx=".35" cy=".25" r=".9"><stop offset="0" stop-color="#FBF3E4"/><stop offset=".6" stop-color="#F3E7D4"/><stop offset="1" stop-color="#E4D1B5"/></radialGradient>'
    w = 300
    return tile("t-logo", "logo", "0 0 500 504",
                f'<rect width="500" height="504" fill="url(#lg-bg)"/>' + img(STACK, 250 - w / 2, 252 - w * STACK_R / 2, w, STACK_R), defs)


def t_front():
    defs = ('<linearGradient id="fr-in" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FCE6B8"/><stop offset=".55" stop-color="#E0A866"/><stop offset="1" stop-color="#8C5630"/></linearGradient>'
            '<linearGradient id="fr-zinc" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9AA0A4"/><stop offset=".5" stop-color="#D6DADC"/><stop offset="1" stop-color="#8A9094"/></linearGradient>'
            '<radialGradient id="fr-glow"><stop offset="0" stop-color="#FFE9B5" stop-opacity=".9"/><stop offset="1" stop-color="#FFE9B5" stop-opacity="0"/></radialGradient>'
            '<linearGradient id="fr-shade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a2614" stop-opacity=".28"/><stop offset="1" stop-color="#3a2614" stop-opacity="0"/></linearGradient>')
    joints = "".join(f'<path d="M0 {y}H400" stroke="#DCCAB0" stroke-width="1.2"/>' for y in range(42, 200, 42))
    lamps = "".join(f'<path d="M{x} 206V236" stroke="#2a1e16" stroke-width="1.4"/><circle cx="{x}" cy="240" r="26" fill="url(#fr-glow)"/><circle cx="{x}" cy="240" r="6" fill="#FFF4D6"/>' for x in (100, 200, 300))
    rnd = random.Random(2)
    shelf = "".join(f'<rect x="{x}" y="{y - h}" width="7" height="{h}" rx="2" fill="{rnd.choice(["#4a2a1c", "#6b3a2a", "#2f2a22", "#7a5a3a"])}"/>'
                    for y in (300, 352) for x, h in ((rnd.randint(60, 340), rnd.randint(16, 26)) for _ in range(16)))
    tree = '<path d="M28 520C30 440 22 380 34 300" fill="none" stroke="#6b5440" stroke-width="5" stroke-linecap="round"/>' + foliage(rnd, 34, 250, 52, 85)
    w = 150
    body = (f'<rect width="400" height="504" fill="#ECDDC6"/>{joints}'
            + img(STACK, 200 - w / 2, 22, w, STACK_R)
            + '<rect x="30" y="192" width="340" height="320" fill="#1F1A16"/>'
            '<rect x="42" y="204" width="316" height="310" fill="url(#fr-in)"/>'
            + lamps + '<path d="M50 300H350M50 352H350" stroke="#5a3a24" stroke-width="3"/>' + shelf
            + '<rect x="146" y="204" width="9" height="310" fill="#1F1A16"/><rect x="246" y="204" width="9" height="310" fill="#1F1A16"/>'
            '<rect x="42" y="204" width="316" height="34" fill="url(#fr-shade)"/>'
            '<path d="M136 360V430M164 360V430" stroke="#c9a57e" stroke-width="3" stroke-linecap="round"/>'
            '<path d="M170 470h70l-6 34h-58z" fill="#3a2a1e" opacity=".55"/>'
            + tree
            + '<path d="M14 440h82l-8 70H22z" fill="url(#fr-zinc)"/><path d="M300 446h80l-8 64h-64z" fill="url(#fr-zinc)"/>'
            + flowers(55, 420, 40, 14, 4) + flowers(340, 428, 40, 13, 9, ("blush", "daisy", "pink", "daisy")))
    return tile("t-front", "fasada", "0 0 400 504", body, defs)


def t_sign():
    defs = '<linearGradient id="sg-wall" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F0E3CD"/><stop offset="1" stop-color="#DCC6A6"/></linearGradient>'
    rnd = random.Random(8)
    green = foliage(rnd, 40, 30, 70, 60)
    body = ('<rect width="300" height="344" fill="url(#sg-wall)"/>' + green
            + '<rect x="262" y="20" width="38" height="44" rx="3" fill="#1F1A16"/><path d="M262 40H150" stroke="#1F1A16" stroke-width="7" stroke-linecap="round"/>'
            '<path d="M150 40l-30 8" stroke="#1F1A16" stroke-width="3"/><path d="M160 40V78M240 40V78" stroke="#1F1A16" stroke-width="2"/>'
            '<ellipse cx="208" cy="214" rx="104" ry="104" fill="#3a2614" opacity=".18"/>'
            '<circle cx="200" cy="200" r="104" fill="#1F1A16"/>'
            + img(BADGE, 200 - 96, 200 - 96, 192, 1))
    return tile("t-sign", "tabela", "0 0 300 344", body, defs)


def t_box():
    a, b, d = (40, 70), (190, 40), (120, 112)
    m = f'matrix({(b[0] - a[0]) / 100} {(b[1] - a[1]) / 100} {(d[0] - a[0]) / 100} {(d[1] - a[1]) / 100} {a[0]} {a[1]})'
    body = ('<rect width="300" height="168" fill="#E5D3B8"/>'
            '<ellipse cx="160" cy="154" rx="130" ry="12" fill="#3a2614" opacity=".14"/>'
            '<path d="M40 70L190 40L270 80L120 112Z" fill="#D2B18A"/><path d="M40 70L120 112L120 150L40 108Z" fill="#B99268"/>'
            '<path d="M120 112L270 80L270 118L120 150Z" fill="#A98258"/>'
            f'<g transform="{m}"><image href="{LOGO}/{MARK}" x="30" y="10" width="40" height="80" preserveAspectRatio="xMidYMid meet"/></g>'
            + flowers(262, 120, 22, 6, 13, ("daisy",)))
    return tile("t-box", "kutia", "0 0 300 168", body)


def t_cup():
    defs = ('<linearGradient id="cp-g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#E3D8C6"/><stop offset=".45" stop-color="#FBF8F1"/><stop offset="1" stop-color="#DCCFBB"/></linearGradient>'
            '<linearGradient id="cp-wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EAD9BE"/><stop offset="1" stop-color="#D9C3A3"/></linearGradient>')
    w = 92
    body = ('<rect width="300" height="344" fill="url(#cp-wall)"/>'
            '<path d="M0 270Q150 250 300 270V344H0Z" fill="#EEE9E1"/><path d="M20 300q60-14 120 6M170 318q50-10 110 0" stroke="#d8d1c6" stroke-width="2" fill="none"/>'
            '<ellipse cx="156" cy="290" rx="80" ry="12" fill="#3a2614" opacity=".22"/>'
            '<path d="M78 96H222L204 286Q150 296 96 286Z" fill="url(#cp-g)"/>'
            '<rect x="68" y="76" width="164" height="26" rx="8" fill="#3B2418"/><path d="M84 76Q150 52 216 76Z" fill="#4A2E20"/><path d="M80 90H220" stroke="#5c3a28" stroke-width="2"/>'
            + img(STACK, 150 - w / 2, 150, w, STACK_R))
    return tile("t-cup", "gota", "0 0 300 344", body, defs)


def t_wine():
    defs = ('<linearGradient id="wn-b" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#14110e"/><stop offset=".3" stop-color="#3b352e"/><stop offset=".42" stop-color="#1a1714"/><stop offset="1" stop-color="#0e0c0a"/></linearGradient>'
            '<linearGradient id="wn-bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E7D2B2"/><stop offset="1" stop-color="#C9AE88"/></linearGradient>')
    w = 50
    body = ('<rect width="200" height="344" fill="url(#wn-bg)"/>'
            '<path d="M18 150c0 40 16 60 34 62v70" fill="none" stroke="#ffffffaa" stroke-width="2"/><path d="M86 150c0 40-16 60-34 62" fill="none" stroke="#ffffffaa" stroke-width="2"/>'
            '<path d="M22 186c6 18 16 26 30 26s24-8 30-26z" fill="#E7B877" opacity=".75"/><path d="M34 282h36" stroke="#ffffffaa" stroke-width="2"/>'
            '<ellipse cx="128" cy="334" rx="40" ry="6" fill="#3a2614" opacity=".25"/>'
            '<path d="M116 26H140V100Q140 128 160 150V326Q128 336 96 326V150Q116 128 116 100Z" fill="url(#wn-b)"/>'
            '<rect x="114" y="26" width="28" height="18" fill="#2a1418"/>'
            '<rect x="100" y="186" width="56" height="96" rx="2" fill="#F6EFE2"/>'
            + img(STACK, 128 - w / 2, 200, w, STACK_R))
    return tile("t-wine", "vera", "0 0 200 344", body, defs)


def t_bouquet():
    defs = '<linearGradient id="bq-k" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#B99268"/><stop offset=".5" stop-color="#D5B48C"/><stop offset="1" stop-color="#AE875E"/></linearGradient>'
    rnd = random.Random(21)
    euc = "".join(f'<path d="M{150 + dx} 170q{dx * .3:.0f} -50 {dx * .9:.0f} -90" fill="none" stroke="#8E9C77" stroke-width="2"/>'
                  + "".join(f'<circle cx="{150 + dx + dx * .9 * t:.0f}" cy="{170 - 90 * t:.0f}" r="5" fill="#A7B497"/>' for t in (.3, .5, .7, .9))
                  for dx in (-70, -40, 50, 80))
    w = 62
    body = ('<rect width="300" height="344" fill="#E6D3B6"/>' + euc
            + '<path d="M58 160L242 160L176 344L124 344Z" fill="url(#bq-k)"/><path d="M58 160L150 250M242 160L150 250M110 160L150 344M190 160L150 344" stroke="#9b7650" stroke-width="1.4" opacity=".6"/>'
            + flowers(150, 132, 72, 30, 31, ("daisy", "blush", "daisy", "pink", "daisy", "rose"), scale=1.45)
            + '<path d="M118 268q32 12 64 0" fill="none" stroke="#7a5a3a" stroke-width="3"/><path d="M168 272q6 10 10 22" fill="none" stroke="#7a5a3a" stroke-width="1.6"/>'
            '<g transform="translate(0 -46) rotate(-8 200 290)"><path d="M168 272v18" stroke="#7a5a3a" stroke-width="1.4"/><rect x="162" y="288" width="82" height="100" rx="4" fill="#F6EFE2"/><circle cx="203" cy="298" r="3.6" fill="#E6D3B6"/>'
            + img(STACK, 203 - w / 2, 310, w, STACK_R) + '</g>')
    return tile("t-bouquet", "buqeta", "0 0 300 344", body, defs)


PRICES = {"Espresso": "1.20", "Latte": "2.50", "Matcha latte": "3.50", "Glass of wine": "4.00", "Selection": "18.00",
          "Fresh bouquets": "20.00", "Flower box": "30.00"}


def t_menu():
    lines = []
    y = 104
    for title, items in (("Coffee", ["Espresso", "Latte", "Matcha latte"]), ("Wine", ["Glass of wine", "Selection"]), ("Flowers", ["Fresh bouquets", "Flower box"])):
        lines.append(f'<text x="44" y="{y + 2}" style="font-family:Allison,cursive;font-size:22px" fill="{INK}">{title}</text>')
        y += 13
        for it in items:
            lines.append(f'<text x="44" y="{y}" style="font-family:Mali,sans-serif;font-weight:300;font-size:6.6px" fill="{INK}">{it}</text>'
                         f'<text x="156" y="{y}" text-anchor="end" style="font-family:Mali,sans-serif;font-weight:300;font-size:6.6px" fill="{INK}">{PRICES[it]}</text>')
            y += 11
        y += 9
    w = 22
    body = ('<rect width="200" height="344" fill="#D9C3A3"/><ellipse cx="104" cy="334" rx="80" ry="8" fill="#3a2614" opacity=".2"/>'
            '<rect x="20" y="24" width="160" height="306" rx="8" fill="#B48A5E"/><rect x="30" y="44" width="140" height="278" rx="2" fill="#FBF7F0"/>'
            '<rect x="70" y="16" width="60" height="30" rx="6" fill="#8F857C"/><rect x="82" y="22" width="36" height="8" rx="4" fill="#B48A5E"/>'
            + img(MARK, 100 - w / 2, 52, w, MARK_R)
            + f'<text x="100" y="94" text-anchor="middle" style="font-family:Allison,cursive;font-size:30px" fill="{INK}">Clover</text>'
            + "".join(lines))
    return tile("t-menu", "menuja", "0 0 200 344", body)


def t_cake():
    w = 64
    body = ('<rect width="200" height="344" fill="#E8D6BB"/><ellipse cx="102" cy="316" rx="84" ry="10" fill="#3a2614" opacity=".2"/>'
            '<path d="M38 150L162 150L150 64L50 64Z" fill="#D5B48C"/>'
            + img(STACK, 100 - w / 2, 76, w, STACK_R)
            + '<path d="M30 150H170V306H30Z" fill="#C9A57E"/><path d="M30 150H170L162 166H38Z" fill="#B99268"/>'
            '<path d="M54 176H146V260H54Z" fill="#F3E9DA"/><path d="M62 190H138V246H62Z" fill="#4A2C1E"/>'
            + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#C79A5B"/>' for x, y in ((76, 204), (100, 212), (122, 200), (88, 232), (116, 230), (132, 222))))
    return tile("t-cake", "ëmbëlsira", "0 0 200 344", body)


def board():
    return "\n".join([t_logo(), t_front(), t_sign(), t_box(), t_cup(), t_wine(), t_bouquet(), t_menu(), t_cake()])


if __name__ == "__main__":
    dapple()
    tpl = open("site/index.template.html").read()
    out = (tpl.replace("__MINI__", mini()).replace("__CLOVER_DRAW__", clover_draw())
              .replace("__LEAF__", single_leaf())
              .replace("__CLOVER_CARD__", clover_draw().replace('role="img" aria-label="Clover"', 'aria-hidden="true"')).replace("__BOARD__", board()))
    assert "__" not in out.replace("__proto__", ""), "unfilled placeholder"
    open("index.html", "w").write(out)
    print("index.html and assets/site/dapple.svg written")
