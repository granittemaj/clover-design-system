"""Build the GitHub Pages site: index.html, logo.html, applications.html.

Run from the repo root: python3 scripts/build_pages.py
Reads tokens.json, assets/ and components/*/preview.html; writes static HTML.
"""
import html
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
first = t["color"]["themes"][0]["id"]
colors = t["color"]["tokens"]
brand = ["leaf-lule", "leaf-kafe", "leaf-embelsira", "leaf-vere", "matcha", "peony", "wine", "candle"]
neutral = ["ground", "ground-raised", "ground-sunk", "line", "line-strong", "ink", "ink-muted", "alert"]
by_name = {c["name"]: c for c in colors}


def raw(name, theme):
    v = by_name[name]["value"]
    x = v.get(theme, v.get(first)) if isinstance(v, dict) else v
    m = re.fullmatch(r"\{(.+)\}", x)
    return raw(m.group(1), theme) if m else x


def swatches(names):
    out = []
    for n in names:
        usage = html.escape(by_name[n]["usage"].split(". ")[0].rstrip(".") + ".")
        out.append(f"""<div class="sw"><div class="chip" style="background:var(--{n})"></div>
<div class="sw-meta"><b>{n}</b><span class="hex"><span class="on-day">{raw(n, 'light')}</span><span class="on-eve">{raw(n, 'dark')}</span></span><span class="use">{usage}</span></div></div>""")
    return "\n".join(out)


type_rows = []
for g in t["type"]["groups"]:
    for st in g["styles"]:
        meta = f"{st['fontSize']} / {st['lineHeight']} · {st['fontWeight']}"
        type_rows.append(f"""<div class="ty"><div class="ty-meta"><b>{st['name']}</b><span>{meta}</span></div><div class="{st['name']} ty-sample">{html.escape(st['sample'])}</div></div>""")

logos = sorted(f for f in os.listdir("assets/Logos") if f.endswith(".svg"))
logo_tiles = []
for f in logos:
    dark = any(k in f for k in ("-evening", "-paper"))
    logo_tiles.append(f"""<a class="lt{' lt-dark' if dark else ''}" href="assets/Logos/{f}" download><span class="lt-art"><img src="assets/Logos/{f}" alt=""></span><span class="lt-name">{f}</span></a>""")

icons = sorted(f for f in os.listdir("assets/Icons") if f.endswith(".svg"))
icon_tiles = "\n".join(f"""<a class="ic" href="assets/Icons/{f}" download><img src="assets/Icons/{f}" alt=""><span>{f[5:-4]}</span></a>""" for f in icons)

index = f"""<!doctype html>
<html lang="sq">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Clover · Sistemi i dizajnit</title>
<meta name="description" content="Clover: lule, kafe, ëmbëlsira, verë. Logo, colours, type, icons and components.">
<link rel="icon" href="assets/Logos/clover-mark-day.svg" type="image/svg+xml">
{THEME_BOOT}
{HEAD_LIBS}
<style>{NAV_CSS}
body {{ margin: 0; background: var(--ground); color: var(--ink); }}
.wrap {{ max-width: 1080px; margin: 0 auto; padding-inline: var(--space-6); }}
section {{ padding-block: var(--space-12); border-bottom: 1px solid var(--line); }}
.eyebrow {{ font-size: 12px; line-height: 16px; font-weight: 650; letter-spacing: .14em; text-transform: uppercase; color: var(--ink-muted); margin: 0 0 var(--space-3); }}
h2 {{ font-family: var(--font-display); font-weight: 400; font-size: clamp(30px, 5vw, 44px); line-height: 1.1; letter-spacing: -.015em; margin: 0 0 var(--space-4); text-wrap: balance; }}
p.lede {{ margin: 0; font-size: 17px; line-height: 26px; color: var(--ink-muted); max-width: 62ch; }}
.hero {{ display: grid; grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr); gap: var(--space-8); align-items: center; padding-block: var(--space-16); }}
.hero h1 {{ font-family: var(--font-display); font-weight: 400; font-size: clamp(72px, 14vw, 156px); line-height: .9; letter-spacing: -.02em; margin: 0; }}
.hero .tag {{ margin: var(--space-4) 0 var(--space-6); font-size: 18px; line-height: 28px; color: var(--ink-muted); max-width: 34ch; }}
.quad {{ display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-4); max-width: 360px; width: 100%; justify-self: end; }}
.quad div {{ aspect-ratio: 1; }}
.q1 {{ background: var(--leaf-embelsira); border-radius: 50% 50% 4px 50%; }}
.q2 {{ background: var(--leaf-lule); border-radius: 50% 50% 50% 4px; }}
.q3 {{ background: var(--leaf-vere); border-radius: 50% 4px 50% 50%; }}
.q4 {{ background: var(--leaf-kafe); border-radius: 4px 50% 50% 50%; }}
.leaves {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: var(--space-4); margin-top: var(--space-8); }}
.leafcard {{ background: var(--ground-raised); border-radius: var(--radius-leaf) var(--radius-sm) var(--radius-leaf) var(--radius-sm); padding: var(--space-6); display: grid; gap: var(--space-2); }}
.leafcard i {{ width: 28px; height: 28px; border-radius: 50% 50% 50% 4px; display: block; }}
.leafcard b {{ font-family: var(--font-display); font-weight: 400; font-size: 24px; line-height: 30px; }}
.leafcard span {{ font-size: 14px; line-height: 20px; color: var(--ink-muted); }}
.cta-row {{ display: flex; flex-wrap: wrap; gap: var(--space-3); }}
.cta-row a {{ text-decoration: none; }}
.lts {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: var(--space-3); margin-top: var(--space-6); }}
.lt {{ display: grid; grid-template-rows: 140px auto; background: var(--ground-raised); border-radius: var(--radius-md); overflow: hidden; color: var(--ink); text-decoration: none; border: 1px solid var(--line); }}
.lt-dark .lt-art {{ background: #1C1016; }}
.lt-art {{ display: grid; place-items: center; padding: var(--space-4); background: #F3F4EC; }}
.lt-art img {{ max-width: 100%; max-height: 104px; height: auto; }}
.lt-name {{ font-family: var(--font-mono); font-size: 12px; line-height: 16px; padding: var(--space-3) var(--space-4); overflow-wrap: anywhere; }}
.lt:hover {{ border-color: var(--line-strong); }}
.lt:focus-visible, .ic:focus-visible {{ outline: none; box-shadow: var(--focus-ring); }}
.sws {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: var(--space-4); margin-top: var(--space-6); }}
.sw {{ display: grid; grid-template-columns: 56px minmax(0, 1fr); gap: var(--space-3); align-items: start; }}
.chip {{ width: 56px; height: 56px; border-radius: 50% 50% 50% 4px; border: 1px solid var(--line); }}
.sw-meta {{ display: grid; gap: 2px; font-size: 13px; line-height: 18px; min-width: 0; }}
.sw-meta b {{ font-weight: 650; font-size: 14px; }}
.sw-meta .hex {{ font-family: var(--font-mono); font-size: 12px; color: var(--ink-muted); }}
.sw-meta .hex .on-day, .sw-meta .hex .on-eve {{ display: none; }}
:root:not([data-theme="dark"]) .sw-meta .hex .on-day, [data-theme="dark"] .sw-meta .hex .on-eve {{ display: inline; }}
.sw-meta .use {{ color: var(--ink-muted); }}
h3.sub {{ font-family: var(--font-sans); font-size: 14px; letter-spacing: .14em; text-transform: uppercase; font-weight: 650; color: var(--ink-muted); margin: var(--space-8) 0 0; }}
.ty {{ display: grid; grid-template-columns: 180px minmax(0, 1fr); gap: var(--space-6); padding-block: var(--space-4); border-top: 1px solid var(--line); align-items: baseline; }}
.ty-meta {{ display: grid; gap: 2px; font-size: 13px; }}
.ty-meta span {{ font-family: var(--font-mono); font-size: 12px; color: var(--ink-muted); }}
.ty-sample {{ min-width: 0; overflow-wrap: anywhere; }}
.label.ty-sample {{ text-transform: uppercase; }}
.ics {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(110px, 1fr)); gap: var(--space-3); margin-top: var(--space-6); }}
.ic {{ display: grid; justify-items: center; gap: var(--space-2); padding: var(--space-4); background: #F3F4EC; border-radius: var(--radius-md); color: #1E2A1F; text-decoration: none; font-size: 13px; border: 1px solid var(--line); }}
.ic img {{ width: 36px; height: 36px; }}
.demo {{ display: grid; gap: var(--space-6); margin-top: var(--space-6); }}
.demo-row {{ display: flex; flex-wrap: wrap; gap: var(--space-3); align-items: center; }}
.demo-cols {{ display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: var(--space-8); align-items: start; }}
.menu-box {{ background: var(--ground-raised); border-radius: var(--radius-leaf) var(--radius-sm) var(--radius-leaf) var(--radius-sm); padding: var(--space-6); }}
.menu-box h4 {{ font-family: var(--font-display); font-weight: 400; font-size: 28px; line-height: 34px; margin: 0 0 var(--space-2); }}
footer {{ padding-block: var(--space-12); color: var(--ink-muted); font-size: 14px; line-height: 22px; }}
footer a {{ color: var(--ink); }}
p.lede a {{ color: var(--primary); text-underline-offset: 3px; }}
body {{ overflow-x: hidden; }}
@media (max-width: 760px) {{
  .hero {{ grid-template-columns: 1fr; padding-block: var(--space-12); }}
  .quad {{ justify-self: start; max-width: 240px; }}
  .leaves {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
  .demo-cols {{ grid-template-columns: 1fr; }}
  .ty {{ grid-template-columns: 1fr; gap: var(--space-2); }}
  .site-nav {{ padding-inline: var(--space-4); }}
  .site-nav .links {{ gap: var(--space-3); font-size: 13px; }}
}}
</style>
</head>
<body>
{nav()}
<main class="wrap">

<section class="hero">
  <div>
    <p class="eyebrow">Sistemi i dizajnit</p>
    <h1>Clover</h1>
    <p class="tag">Lule, kafe, ëmbëlsira, verë. Katër gjethe, një shtëpi. Lule ditën, verë mbrëmjen.</p>
    <div class="cta-row">
      <a class="cv-btn cv-btn-primary" href="logo.html">Udhëzimet e logos</a>
      <a class="cv-btn cv-btn-quiet" href="applications.html">Shiko aplikimet</a>
    </div>
  </div>
  <div class="quad" aria-hidden="true"><div class="q1"></div><div class="q2"></div><div class="q3"></div><div class="q4"></div></div>
</section>

<section>
  <p class="eyebrow">Ideja</p>
  <h2>Katër gjethe, një për secilën pjesë të shtëpisë</h2>
  <p class="lede">A four-leaf clover is luck, and a gift from Clover should feel lucky. Each leaf is one thing the house does, and each takes that part's colour. By day the house serves coffee and matcha; after 17:00 it turns into a wine bar, and the whole palette turns with it. Try the Ditë / Mbrëmje switch at the top.</p>
  <div class="leaves">
    <div class="leafcard"><i style="background:var(--leaf-lule)"></i><b>Lule</b><span>Flowers and bouquets. Peony.</span></div>
    <div class="leafcard"><i style="background:var(--leaf-kafe)"></i><b>Kafe</b><span>Coffee and matcha. Matcha green.</span></div>
    <div class="leafcard"><i style="background:var(--leaf-embelsira)"></i><b>Ëmbëlsira</b><span>Sweets and small treats. Honey.</span></div>
    <div class="leafcard"><i style="background:var(--leaf-vere)"></i><b>Verë</b><span>Wine and meze, the evening. Wine.</span></div>
  </div>
</section>

<section id="logot">
  <p class="eyebrow">Logot</p>
  <h2>Download the logo files</h2>
  <p class="lede">Outlined SVGs, no fonts needed. Use <b>-day</b> on light grounds, <b>-evening</b> on dark grounds and wine, <b>-ink</b> and <b>-paper</b> for one-colour print. Start with the horizontal lockup. Rules for clear space, sizes and misuse are on the <a href="logo.html">logo guidelines</a> page.</p>
  <div class="lts">
{chr(10).join(logo_tiles)}
  </div>
</section>

<section>
  <p class="eyebrow">Ngjyra</p>
  <h2>Colour</h2>
  <p class="lede">Values switch with the theme. Every text colour meets WCAG AA on the grounds it is used on, in both themes.</p>
  <h3 class="sub">Leaves and brand</h3>
  <div class="sws">{swatches(brand)}</div>
  <h3 class="sub">Grounds and text</h3>
  <div class="sws">{swatches(neutral)}</div>
</section>

<section>
  <p class="eyebrow">Tipografia</p>
  <h2>Gloock, Familjen Grotesk, DM Mono</h2>
  <p class="lede">Gloock for headlines, the same face as the wordmark. Familjen Grotesk for everything people read. DM Mono for anything you count: prices, hours, sizes.</p>
  <div style="margin-top:var(--space-6)">
{chr(10).join(type_rows)}
  </div>
</section>

<section>
  <p class="eyebrow">Ikonat</p>
  <h2>Ten icons for the house</h2>
  <p class="lede">24px line icons, 1.6px stroke, round caps. Click one to download it.</p>
  <div class="ics">
{icon_tiles}
  </div>
</section>

<section>
  <p class="eyebrow">Komponentët</p>
  <h2>Components</h2>
  <p class="lede">React 18 components on <code>window.Clover</code>. These are live: switch the theme and they follow.</p>
  <div class="demo">
    <div class="demo-row" id="d-buttons"></div>
    <div class="demo-row" id="d-status"></div>
    <div class="demo-cols">
      <div class="menu-box"><h4>Kafe &amp; matcha</h4><div id="d-menu"></div></div>
      <div id="d-bouquet"></div>
    </div>
    <div id="d-form" style="max-width:520px;display:grid;gap:var(--space-6)"></div>
  </div>
</section>

<footer>
  Clover design system. Logos, tokens, components and the brand book live in the <a href="https://github.com/granittemaj/clover-design-system">GitHub repo</a>. Names and contact details on the sample business card are placeholders.
</footer>
</main>
{THEME_JS}
<script>
  var C = window.Clover, h = React.createElement;
  function mount(id, el) {{ ReactDOM.createRoot(document.getElementById(id)).render(el); }}
  mount('d-buttons', h(React.Fragment, null, h(C.Button, null, 'Porosit buqetën'), h(C.Button, {{ variant: 'quiet' }}, 'Rezervo tavolinë'), h(C.Button, {{ variant: 'ghost' }}, 'Shiko menunë')));
  mount('d-status', h(React.Fragment, null, h(C.OpenNow, {{ part: 'day' }}), h(C.OpenNow, {{ part: 'evening' }}), h(C.Tag, {{ tone: 'matcha' }}, 'Matcha'), h(C.Tag, {{ tone: 'peony' }}, 'Sezonale'), h(C.Tag, {{ tone: 'candle' }}, 'Sot')));
  mount('d-menu', h(React.Fragment, null,
    h(C.MenuItem, {{ name: 'Makiato e madhe', note: 'Espreso me shkumë qumështi', price: '€1.50' }}),
    h(C.MenuItem, {{ name: 'Matcha latte', note: 'Ceremoniale, qumësht tërshëre', price: '€3.50', tag: 'E re', tagTone: 'candle' }}),
    h(C.MenuItem, {{ name: 'Trileçe', note: 'Ëmbëlsira e ditës', price: '€2.50' }})));
  mount('d-bouquet', h(C.BouquetCard, {{ name: 'Bozhure', note: 'Bozhure rozë me eukalipt, të mbështjella në letër.', tag: 'Sezonale' }}));
  mount('d-form', h(React.Fragment, null,
    h(C.Field, {{ id: 'per-ke', label: 'Për kë është?', placeholder: 'p.sh. për nënën, për ditëlindje', hint: 'Na ndihmon të zgjedhim ngjyrat.' }}),
    h(C.Field, {{ id: 'mesazhi', label: 'Mesazhi në kartolinë', multiline: true, placeholder: 'Shkruani deri në 200 shkronja' }})));
</script>
</body>
</html>
"""
open("index.html", "w").write(index)
print("index.html, logo.html, applications.html written")
