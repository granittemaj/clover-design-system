"""Build the GitHub Pages site: index.html, logo.html, applications.html.

Run from the repo root: python3 scripts/build_pages.py
Reads tokens.json, assets/ and components/*/preview.html; writes static HTML.
"""
import html
import math
import json
import os
import re

t = json.load(open("tokens.json"))

HEAD_LIBS = """<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components/bundle.css">
<script src="https://cdn.jsdelivr.net/npm/react@18.3.1/umd/react.production.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/react-dom@18.3.1/umd/react-dom.production.min.js"></script>
<script src="components/bundle.js"></script>"""

# Day before 17:00, evening after; a saved toggle choice wins.
THEME_BOOT = """<script>
(function () {
  var pick = null;
  try { pick = localStorage.getItem('clover-theme'); } catch (e) {}
  var q = /[?&]theme=(light|dark)/.exec(location.search);
  if (q) pick = q[1];
  var h = new Date().getHours();
  var auto = (h >= 17 || h < 6) ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', pick || auto);
})();
</script>"""

NAV_CSS = """
.site-nav { flex-wrap: wrap; position: sticky; top: env(safe-area-inset-top, 0px); z-index: 10; display: flex; align-items: center; justify-content: space-between; gap: var(--space-4); padding: var(--space-3) var(--space-6); background: var(--ground); border-bottom: 1px solid var(--line); font-family: var(--font-sans); }
.site-nav a.home img { height: 26px; width: auto; }
.site-nav .links { min-width: 0; display: flex; flex-wrap: wrap; gap: var(--space-4); align-items: center; font-size: 14px; }
.site-nav .links a { color: var(--ink); text-decoration: none; font-weight: 600; }
.site-nav .links a:hover { color: var(--primary); }
.theme-btn { font: inherit; font-size: 13px; font-weight: 600; padding: 6px 14px; border-radius: var(--radius-full); border: 1.5px solid var(--line-strong); background: transparent; color: var(--ink); cursor: pointer; }
.theme-btn:focus-visible { outline: none; box-shadow: var(--focus-ring); }
.on-day { display: block; } .on-eve { display: none; }
[data-theme="dark"] .on-day { display: none; } [data-theme="dark"] .on-eve { display: block; }
"""


def nav(prefix=""):
    return f"""<nav class="site-nav" aria-label="Clover">
  <a class="home" href="{prefix}index.html"><img class="on-day" src="{prefix}assets/Logos/clover-lockup-horizontal-day.svg" alt="Clover"><img class="on-eve" src="{prefix}assets/Logos/clover-lockup-horizontal-evening.svg" alt="Clover"></a>
  <div class="links">
    <a href="{prefix}index.html#logot">Logot</a>
    <a href="{prefix}logo.html">Udhëzimet</a>
    <a href="{prefix}applications.html">Aplikime</a>
    <a href="https://github.com/granittemaj/clover-design-system/blob/main/BRAND.md">Brand book</a>
    <button class="theme-btn" id="theme-btn" type="button">Mbrëmje</button>
  </div>
</nav>"""


THEME_JS = """<script>
(function () {
  var b = document.getElementById('theme-btn');
  function label() { b.textContent = document.documentElement.getAttribute('data-theme') === 'dark' ? 'Ditë' : 'Mbrëmje'; }
  label();
  b.addEventListener('click', function () {
    var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('clover-theme', next); } catch (e) {}
    label();
  });
})();
</script>"""


def standalone(src_path, out_path, title, description):
    """Wrap a showcase preview (designed at 960px) as a page of its own."""
    src = open(src_path).read()
    src = re.sub(r"^<!-- @dsCard[^\n]*-->\n", "", src)
    src = src.replace("../../assets/", "assets/")
    src = re.sub(r"<!doctype html>\s*<html[^>]*>\s*<head>", "", src, count=1, flags=re.I)
    head_end = src.index("</head>")
    head_inner, body = src[:head_end], src[head_end + len("</head>"):]
    head_inner = re.sub(r"<meta charset=\"utf-8\">", "", head_inner)
    head_inner = re.sub(r"<title>.*?</title>", "", head_inner)
    body = body.replace("<body>", "", 1).replace("</body>", "").replace("</html>", "")
    page = f"""<!doctype html>
<html lang="sq">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=1000">
<title>{title}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="assets/Logos/clover-mark-day.svg" type="image/svg+xml">
{THEME_BOOT}
{HEAD_LIBS}
<style>{NAV_CSS}
.frame {{ max-width: 960px; margin: 0 auto; }}
</style>
{head_inner}
</head>
<body>
{nav()}
<main class="frame">
{body}
</main>
{THEME_JS}
</body>
</html>
"""
    open(out_path, "w").write(page)


standalone("components/Logo/preview.html", "logo.html", "Clover · Logo",
           "Clover logo guidelines: the four-leaf mark, lockups, clear space, minimum sizes, colour and misuse.")
standalone("components/Applications/preview.html", "applications.html", "Clover · Aplikime",
           "Clover on real objects: fascia, cup, bouquet tag, business card, menus and Instagram posts.")

# ------------------------------------------------------------------ index
# The home page is hand-written in site/index.template.html; this fills in the
# clover (same geometry as scripts/build_clover.py), the marquee and the shopfront.
src = open("scripts/build_clover.py").read()
LEAF = re.search(r'^LEAF = \("([^"]+)"\)', src, re.M).group(1)
STEM = re.search(r'^STEM = "([^"]+)"', src, re.M).group(1)
GAP = float(re.search(r"^GAP = ([\d.]+)", src, re.M).group(1))
ORDER = [("lule", 45), ("kafe", 135), ("vere", 225), ("emb", 315)]


def leaf_d(rot):
    return f'transform="rotate({rot} 50 46) translate(50 {46 - GAP:g})" d="{LEAF}"'


def clover_svg(cls="clover", extra="", label="Clover"):
    leaves = "".join(f'<g class="lf lf-{k}" data-leaf="{k}"><path fill-rule="evenodd" {leaf_d(r)}/></g>' for k, r in ORDER)
    return (f'<svg class="{cls}" viewBox="12 8 76 80.2" role="img" aria-label="{label}">'
            f'{extra}{leaves}<path class="stem" d="{STEM}"/></svg>')


def blueprint():
    g = ['<g aria-hidden="true">',
         '<circle class="guide" cx="50" cy="46" r="38.6"/>',
         f'<circle class="guide" cx="50" cy="46" r="{GAP:g}"/>',
         '<path class="guide" d="M50 4V92M8 46H92"/>',
         '<path class="guide" d="M18 14L82 78M82 14L18 78" stroke-dasharray="1 1"/>']
    for _, r in ORDER:  # lobe circles and the crescent axis of each leaf
        g.append(f'<g transform="rotate({r} 50 46) translate(50 {46 - GAP:g})">'
                 '<circle class="guide" cx="-8.4" cy="-22.6" r="8.6"/><circle class="guide" cx="8.4" cy="-22.6" r="8.6"/></g>')
    g += ['<text class="guide-txt" x="73" y="20">45°</text>',
          '<text class="guide-txt" x="52" y="44.6">x</text>',
          '<text class="guide-txt" x="86" y="70">r 38.6</text>',
          '<text class="guide-txt" x="13" y="90">clover · ndërtimi</text>',
          '</g>']
    return clover_svg("clover", extra="".join(g), label="Clover mark with construction lines")


def mini():
    leaves = "".join(f'<g class="lf lf-{k}"><path fill-rule="evenodd" {leaf_d(r)}/></g>' for k, r in ORDER)
    return f'<svg class="clover" viewBox="12 8 76 80.2" aria-hidden="true">{leaves}<path class="stem" d="{STEM}"/></svg>'


words = [("Lule", "--leaf-lule"), ("Kafe", "--leaf-kafe"), ("Matcha", "--leaf-kafe"), ("Ëmbëlsira", "--leaf-embelsira"),
         ("Verë", "--leaf-vere"), ("Meze", "--leaf-vere"), ("Buqeta me porosi", "--leaf-lule")]
run = "".join(f'<span>{w}</span><i style="background:var({c})"></i>' for w, c in words)
marquee = run + run


def lockup_size(path):
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', open(path).read())
    return float(m.group(1)), float(m.group(2))


def shopfront():
    lw, lh = lockup_size("assets/Logos/clover-lockup-horizontal-evening.svg")
    lock_h = 50
    lock_w = lock_h * lw / lh
    EVE = {"lule": "#F28DB0", "kafe": "#A9C56B", "vere": "#C25A7C", "emb": "#EDB54E"}
    def bloom(x, y, rot, s, col):
        return f'<path fill="{col}" fill-rule="evenodd" transform="translate({x} {y}) rotate({rot}) scale({s})" d="{LEAF}"/>'
    bouquets = []
    deep = {"lule": "#B02A5A", "pink": "#D2557F", "vere": "#5E1A33", "emb": "#C08A1E", "kafe": "#4A671B"}
    vases = [(248, 50, "#3A1626", ["pink", "lule", "emb", "lule", "pink"]),
             (352, 64, "#1E2A1F", ["vere", "lule", "pink", "lule", "emb", "lule"]),
             (520, 46, "#5E1A33", ["emb", "pink", "lule", "pink", "emb"]),
             (628, 60, "#3A1626", ["lule", "vere", "pink", "lule", "pink", "vere"])]
    for vx, vh, vc, cols in vases:
        top = 500 - vh
        cx, cy = vx, top - 46
        n = len(cols)
        for j, c in enumerate(cols):
            ang = -72 + 144 * j / (n - 1)
            rad = 30 if j % 2 else 38
            bx = cx + rad * math.sin(math.radians(ang))
            by = cy - rad * math.cos(math.radians(ang)) * .8 + 10
            bouquets.append(f'<path d="M{vx} {top + 2}Q{vx + (bx - vx) * .25:.0f} {top - 22} {bx:.0f} {by + 6:.0f}" stroke="#2F4A1A" stroke-width="2.2" fill="none"/>')
        for j, c in enumerate(cols):
            ang = -72 + 144 * j / (n - 1)
            rad = 30 if j % 2 else 38
            bx = cx + rad * math.sin(math.radians(ang))
            by = cy - rad * math.cos(math.radians(ang)) * .8 + 10
            bouquets.append(bloom(round(bx), round(by), round(ang), 0.92, deep[c]))
        bouquets.append(f'<path d="M{vx - 17} {top}H{vx + 17}L{vx + 20} {top + vh - 8}Q{vx + 20} {top + vh} {vx + 12} {top + vh}H{vx - 12}Q{vx - 20} {top + vh} {vx - 20} {top + vh - 8}Z" fill="{vc}"/>')
    windows = []
    for k, wx in enumerate((200, 430, 660, 890)):
        lit = k == 2
        windows.append(f'<rect x="{wx}" y="104" width="110" height="112" rx="3" fill="{"url(#warm)" if lit else "#1A0F14"}" opacity="{".7" if lit else "1"}" stroke="#3A2530" stroke-width="6"/>')
        windows.append(f'<path d="M{wx + 55} 104V216" stroke="#3A2530" stroke-width="4"/>')
    stars = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#F4E9EC" opacity=".55"/>' for x, y, r in
                    ((40, 40, 1.4), (88, 110, 1), (60, 220, 1.2), (1140, 54, 1.4), (1170, 160, 1), (1110, 250, 1.2), (30, 330, 1)))
    door_mark = "".join(f'<path fill="#F4E9EC" fill-rule="evenodd" {leaf_d(r)}/>' for _, r in ORDER) + f'<path fill="#F4E9EC" d="{STEM}"/>'
    return f"""<svg class="front" viewBox="0 0 1200 640" role="img" aria-label="The Clover shopfront at night: a wine-red fascia with the logo, a warm-lit window full of flowers, a glass door and a wine board on the pavement.">
<defs>
<radialGradient id="warm" cx=".5" cy=".42" r=".75"><stop offset="0" stop-color="#FFE3A6"/><stop offset=".35" stop-color="#F2BE63"/><stop offset=".78" stop-color="#B8642F"/><stop offset="1" stop-color="#5A2128"/></radialGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#FFD58A" stop-opacity=".75"/><stop offset="1" stop-color="#FFD58A" stop-opacity="0"/></radialGradient>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0D060A"/><stop offset="1" stop-color="#22111A"/></linearGradient>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="22"/></filter>
</defs>
<rect width="1200" height="640" fill="url(#sky)"/>
{stars}
<rect x="120" y="60" width="960" height="530" fill="#2A1820"/>
<rect x="104" y="52" width="992" height="16" fill="#3A2530"/>
{''.join(windows)}
<rect x="160" y="246" width="880" height="80" rx="3" fill="#5E1A33"/>
<image href="assets/Logos/clover-lockup-horizontal-evening.svg" x="{600 - lock_w / 2:.1f}" y="{286 - lock_h / 2:.1f}" width="{lock_w:.1f}" height="{lock_h}"/>
<rect class="glow" x="150" y="330" width="620" height="260" fill="#F2BE63" opacity=".35" filter="url(#soft)"/>
<rect x="180" y="352" width="560" height="214" fill="url(#warm)"/>
<g class="glow"><circle cx="300" cy="384" r="34" fill="url(#halo)"/><circle cx="460" cy="384" r="34" fill="url(#halo)"/><circle cx="620" cy="384" r="34" fill="url(#halo)"/></g>
<path d="M300 352V378M460 352V378M620 352V378" stroke="#3A1626" stroke-width="2"/>
<circle cx="300" cy="382" r="6" fill="#FFF1CF"/><circle cx="460" cy="382" r="6" fill="#FFF1CF"/><circle cx="620" cy="382" r="6" fill="#FFF1CF"/>
{''.join(bouquets)}
<rect x="180" y="500" width="560" height="66" fill="#3A1626" opacity=".94"/>
<text x="460" y="542" text-anchor="middle" fill="#F4E9EC" style="font-family:Gloock,Georgia,serif;font-size:26px;letter-spacing:-.4px">Lule me porosi · Kafe · Verë</text>
<rect x="180" y="352" width="560" height="214" fill="none" stroke="#140B10" stroke-width="10"/>
<path d="M460 352V500" stroke="#140B10" stroke-width="7"/>
<rect x="170" y="566" width="580" height="22" fill="#3A1626"/>
<rect x="798" y="352" width="160" height="238" fill="#140B10"/>
<rect x="816" y="370" width="124" height="150" fill="url(#warm)" opacity=".9"/>
<g transform="translate(846 404) scale(.82)" opacity=".9">{door_mark}</g>
<rect x="922" y="470" width="6" height="44" rx="3" fill="#EDB54E"/>
<g class="glow"><circle cx="780" cy="372" r="46" fill="url(#halo)"/><circle cx="976" cy="372" r="46" fill="url(#halo)"/></g>
<rect x="776" y="364" width="8" height="16" rx="3" fill="#FFF1CF"/><rect x="972" y="364" width="8" height="16" rx="3" fill="#FFF1CF"/>
<path d="M1000 588L1022 498H1078L1100 588" fill="#1C1016" stroke="#4A2E3C" stroke-width="3"/>
<text x="1050" y="534" text-anchor="middle" fill="#F28DB0" style="font-family:Gloock,Georgia,serif;font-size:19px">Verë</text>
<text x="1050" y="556" text-anchor="middle" fill="#F4E9EC" style="font-family:'DM Mono',monospace;font-size:11px">17–00</text>
<rect x="0" y="588" width="1200" height="52" fill="#0D060A"/>
<path d="M0 588H1200" stroke="#3A2530" stroke-width="2"/>
<ellipse class="glow" cx="460" cy="606" rx="300" ry="12" fill="#F2BE63" opacity=".22" filter="url(#soft)"/>
</svg>"""


tpl = open("site/index.template.html").read()
out = (tpl.replace("__MINI__", mini())
          .replace("__CLOVER_HERO__", clover_svg())
          .replace("__CLOVER_STAGE__", clover_svg(label="Clover, one leaf for each part of the day"))
          .replace("__CLOVER_BLUEPRINT__", blueprint())
          .replace("__MARQUEE__", marquee)
          .replace("__SHOPFRONT__", shopfront()))
assert "__" not in re.sub(r"__proto__", "", out), "unfilled placeholder"
open("index.html", "w").write(out)
print("index.html, logo.html, applications.html written")
