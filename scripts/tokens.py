"""Write tokens.json for the Clover system, failing if any text pair drops below WCAG AA.

Run from the repo root: python3 scripts/tokens.py tokens.json
"""
import json
import sys

out = sys.argv[1] if len(sys.argv) > 1 else "tokens.json"


def lum(h):
    h = h.lstrip("#")
    r, g, b = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def cr(a, b):
    la, lb = sorted([lum(a), lum(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


C = [
    # name, day (cream), evening (espresso), usage
    ("cream", "#F5EDE0", "#2B1C15", "Page background: warm unbleached paper by day, espresso in the evening."),
    ("paper", "#FBF7F0", "#382419", "Cards, menus, labels: the brighter paper that sits on cream."),
    ("sand", "#EADBC5", "#22160F", "Recessed panels, footers, quiet bands."),
    ("kraft", "#C9A57E", "#6B4E33", "Kraft paper: boxes, bags, bouquet wrap, tags. A surface, never text."),
    ("line", "#DCCBB3", "#4E3426", "Hairlines and dividers."),
    ("line-strong", "#9C8069", "#A48A76", "Input and control borders; 3:1 on cream and paper."),
    ("ink", "#4B2E20", "#F3E8D8", "Espresso ink: the logo, headings and body text on cream, paper, sand, kraft and blush."),
    ("ink-muted", "#77584A", "#CDB8A3", "Secondary text and descriptions on cream and paper."),
    ("blush", "#EBCBC6", "#4A2C2E", "Flower pink: soft backgrounds behind flower content."),
    ("rose", "#9A4753", "#E7A9B1", "Flower accent as text: on cream and paper."),
    ("sage", "#566545", "#B4C29E", "Leaf green: foliage accents and the order flow by day."),
    ("sage-soft", "#DCE2CF", "#2F3626", "Soft green ground behind sage text."),
    ("wine", "#5C2230", "#C9788A", "Wine: the wine list, the evening, bottle labels. Text on cream and paper."),
    ("sun", "#F2DDB0", "#5A4022", "Golden-hour light: highlights and the warm glow behind photos."),
    ("on-ink", "#F5EDE0", "#2B1C15", "Text on an ink (espresso) fill."),
]
D = {n: (d, e) for n, d, e, _ in C}
checks = [("ink", ["cream", "paper", "sand", "kraft", "blush", "sage-soft"], 4.5),
          ("ink-muted", ["cream", "paper"], 4.5),
          ("rose", ["cream", "paper"], 4.5), ("sage", ["cream", "paper", "sage-soft"], 4.5),
          ("wine", ["cream", "paper"], 4.5), ("line-strong", ["cream", "paper"], 3.0), ("on-ink", ["ink"], 4.5)]
bad = [(i, fg, bg, round(cr(D[fg][i], D[bg][i]), 2)) for i in (0, 1) for fg, bgs, mn in checks for bg in bgs
       if cr(D[fg][i], D[bg][i]) < mn]
print("contrast failures:", bad)
assert not bad

tokens = {
    "name": "Clover", "version": 2,
    "color": {
        "note": "Golden-hour palette from the room itself: unbleached paper, kraft wrap, espresso ink, the flowers' blush and leaves, a glass of wine. Day is cream; evening flips to espresso.",
        "themes": [{"id": "light", "name": "Ditë · day"}, {"id": "dark", "name": "Mbrëmje · evening"}],
        "tokens": [{"name": n, "value": {"light": d, "dark": e}, "usage": u} for n, d, e, u in C] + [
            {"name": "primary", "value": {"light": "{ink}", "dark": "{ink}"}, "usage": "The main action: an espresso pill by day, a cream pill by evening."},
            {"name": "on-primary", "value": {"light": "{on-ink}", "dark": "{on-ink}"}, "usage": "Text on a primary fill."},
        ]},
    "type": {
        "fonts": [
            {"family": "Allison", "file": "fonts/Allison-400.woff2", "weight": "400", "style": "normal"},
            {"family": "Mali", "file": "fonts/Mali-300.woff2", "weight": "300", "style": "normal"},
            {"family": "Mali", "file": "fonts/Mali-400.woff2", "weight": "400", "style": "normal"},
            {"family": "Mali", "file": "fonts/Mali-600.woff2", "weight": "600", "style": "normal"},
        ],
        "families": {
            "script": "Allison, \"Segoe Script\", \"Brush Script MT\", cursive",
            "body": "Mali, \"Nunito\", ui-rounded, system-ui, sans-serif",
        },
        "groups": [
            {"name": "Script", "family": "script", "note": "Allison: the wordmark's signature hand. Short words only: the name, labels, titles of two or three words. Never sentences, never below 32px.", "styles": [
                {"name": "script-xl", "fontSize": "160px", "lineHeight": "150px", "fontWeight": 400, "sample": "Clover", "usage": "The name on signage and the website hero."},
                {"name": "script-lg", "fontSize": "84px", "lineHeight": "84px", "fontWeight": 400, "sample": "Kafe", "usage": "Menu section titles, card titles."},
                {"name": "script-md", "fontSize": "48px", "lineHeight": "52px", "fontWeight": 400, "sample": "katër gjethe", "usage": "Section labels above a headline."}]},
            {"name": "Body", "family": "body", "note": "Mali: soft and rounded, readable at menu sizes, full Albanian. Light weight for headlines.", "styles": [
                {"name": "headline", "fontSize": "48px", "lineHeight": "58px", "fontWeight": 300, "sample": "Tre gjëra që i bëjmë mirë.", "usage": "Section headlines."},
                {"name": "descriptor", "fontSize": "15px", "lineHeight": "20px", "fontWeight": 300, "letterSpacing": "0.24em", "sample": "coffee · wine · flowers", "usage": "The descriptor and small labels: lowercase, widely spaced."},
                {"name": "lead", "fontSize": "20px", "lineHeight": "32px", "fontWeight": 300, "sample": "Kafe në mëngjes, verë në mbrëmje, lule gjithë ditën.", "usage": "Intro paragraphs."},
                {"name": "body", "fontSize": "16px", "lineHeight": "26px", "fontWeight": 400, "sample": "Na tregoni për kë është buqeta dhe e përgatisim me dorë.", "usage": "Everything else."},
                {"name": "item", "fontSize": "16px", "lineHeight": "24px", "fontWeight": 600, "sample": "Matcha latte", "usage": "Menu item names."},
                {"name": "small", "fontSize": "13px", "lineHeight": "20px", "fontWeight": 400, "sample": "me qumësht tërshëre", "usage": "Notes, captions."}]},
        ]},
    "spacing": {"note": "4px base.", "tokens": [
        {"name": "space-1", "value": "4px", "usage": "Icon to label."}, {"name": "space-2", "value": "8px", "usage": "Inside chips."},
        {"name": "space-3", "value": "12px", "usage": "Related items."}, {"name": "space-4", "value": "16px", "usage": "Card padding on phones."},
        {"name": "space-6", "value": "24px", "usage": "Card padding."}, {"name": "space-8", "value": "32px", "usage": "Groups."},
        {"name": "space-12", "value": "48px", "usage": "Sections."}, {"name": "space-16", "value": "64px", "usage": "Page margins."}]},
    "radius": {"note": "Soft paper corners; the round sign is a full circle.", "tokens": [
        {"name": "radius-sm", "value": "6px", "usage": "Inputs, tags."}, {"name": "radius-md", "value": "14px", "usage": "Cards, menus, photos."},
        {"name": "radius-lg", "value": "28px", "usage": "Large panels."}, {"name": "radius-full", "value": "9999px", "usage": "Buttons, the round sign."}]},
    "shadow": {"note": "Soft, warm, low sun.", "tokens": [
        {"name": "shadow-sm", "value": {"light": "0 1px 2px #4b2e2014, 0 4px 12px #4b2e200f", "dark": "0 2px 6px #00000080"}, "usage": "Cards at rest."},
        {"name": "shadow-lg", "value": {"light": "0 12px 30px -8px #4b2e2033, 0 30px 60px -20px #4b2e2026", "dark": "0 24px 50px -12px #000000b3"}, "usage": "Mockups, things that float."},
        {"name": "focus-ring", "value": {"light": "0 0 0 2px #f5ede0, 0 0 0 4px #4b2e20", "dark": "0 0 0 2px #2b1c15, 0 0 0 4px #f3e8d8"}, "usage": "Keyboard focus."}]},
}
json.dump(tokens, open(out, "w"), ensure_ascii=False, indent=1)
print("written", out)
