"""Compile tokens.json into tokens.css.

Run from the repo root: python3 scripts/tokens_css.py
Day (light) is the default; [data-theme="dark"] is the evening palette.
"""
import json
import re

t = json.load(open("tokens.json"))
first, second = [th["id"] for th in t["color"]["themes"]]


def val(v, theme):
    x = v.get(theme, v.get(first)) if isinstance(v, dict) else v
    m = re.fullmatch(r"\{(.+)\}", x)
    return f"var(--{m.group(1)})" if m else x


out = [f"/* {t['name']} — generated from tokens.json */"]
for theme, sel in ((first, f':root, [data-theme="{first}"]'), (second, f'[data-theme="{second}"]')):
    decls = [f"  --{x['name']}: {val(x['value'], theme)};" for x in t["color"]["tokens"]]
    decls += [f"  --{x['name']}: {val(x['value'], theme)};" for x in t["shadow"]["tokens"]]
    out.append(sel + " {\n" + "\n".join(decls) + "\n}")
root = [f"  --{x['name']}: {x['value']};" for fam in ("spacing", "radius") for x in t[fam]["tokens"]]
root += [f"  --font-{k}: {v};" for k, v in t["type"]["families"].items()]
out.append(":root {\n" + "\n".join(root) + "\n}")
for f in t["type"]["fonts"]:
    out.append(
        f"@font-face {{ font-family: \"{f['family']}\"; src: url(\"{f['file']}\") format(\"woff2\"); "
        f"font-weight: {f['weight']}; font-style: {f.get('style', 'normal')}; font-display: swap; }}"
    )
for g in t["type"]["groups"]:
    for st in g["styles"]:
        fam = st.get("family", g["family"])
        props = [f"font-family: var(--font-{fam})", f"font-size: {st['fontSize']}", f"line-height: {st['lineHeight']}",
                 f"font-weight: {st['fontWeight']}"]
        if "letterSpacing" in st:
            props.append(f"letter-spacing: {st['letterSpacing']}")
        out.append(f".{st['name']} {{ " + "; ".join(props) + "; }")
open("tokens.css", "w").write("\n".join(out) + "\n")
print("tokens.css written")
