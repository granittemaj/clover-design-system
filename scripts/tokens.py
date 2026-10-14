import json, sys
out = sys.argv[1]
def lum(h):
    h=h.lstrip('#'); r,g,b=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    f=lambda c: c/12.92 if c<=0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b)
def cr(a,b):
    la,lb=sorted([lum(a),lum(b)],reverse=True); return (la+0.05)/(lb+0.05)

C = [
 # name, day, evening, usage
 ("ground", "#F3F4EC", "#1C1016", "Page background. Day is the pale sage of a florist's wrapping paper; evening is the aubergine of a wine bar after the lamps go on."),
 ("ground-raised", "#FBFBF6", "#28171F", "Cards, menus, the order form, anything that sits on the ground."),
 ("ground-sunk", "#E8EADF", "#140B10", "Recessed panels: the menu's price column band, footers, image placeholders."),
 ("line", "#D5D9C8", "#4A2E3C", "Decorative hairlines and dividers between menu rows. Not for control borders."),
 ("line-strong", "#7F8873", "#9A7686", "Input and control borders; meets 3:1 on ground and ground-raised in both themes."),
 ("ink", "#1E2A1F", "#F4E9EC", "Primary text on ground, ground-raised and ground-sunk. The mark's stem colour."),
 ("ink-muted", "#535E50", "#C4ABB5", "Secondary text, menu descriptions, hints; on ground, ground-raised and ground-sunk."),
 ("matcha", "#4A671B", "#A9C56B", "Daytime brand colour: coffee, matcha, the primary action by day. As text on any ground or matcha-soft."),
 ("matcha-soft", "#E2EBCB", "#27311B", "Tinted backgrounds behind matcha text: day-part chips, the coffee menu header."),
 ("on-matcha", "#FFFFFF", "#1C1016", "Text and icons on a matcha fill."),
 ("peony", "#B02A5A", "#F28DB0", "The flower colour (bozhure, the peony): the bloom in the logo, bouquets, the primary action by evening. As text on any ground or peony-soft."),
 ("peony-soft", "#F7DCE5", "#43192C", "Tinted backgrounds behind peony text: bouquet tags, the 'Lule me porosi' band."),
 ("on-peony", "#FFFFFF", "#1C1016", "Text and icons on a peony fill."),
 ("wine", "#5E1A33", "#8E2A4E", "Evening identity: wine list headers, the evening menu cover, signage after 17:00. As text by day only (on ground). In the evening theme it is a fill, never text."),
 ("wine-soft", "#F1DFE5", "#3A1626", "Tinted backgrounds for wine and meze content."),
 ("on-wine", "#FBFBF6", "#F4E9EC", "Text and icons on a wine fill."),
 ("candle", "#855508", "#EDB54E", "Small highlights only: 'new', today's sweet, the candle-lit hours. As text on any ground or candle-soft."),
 ("candle-soft", "#F6E7C4", "#3A2A10", "Tinted backgrounds behind candle text."),
 ("alert", "#A33A12", "#FF9F7A", "Form errors, always with a written message. Orange-red, kept apart from peony by hue and by the message text."),
]
D = {n:(d,e) for n,d,e,_ in C}
checks = [("ink",["ground","ground-raised","ground-sunk"],4.5),("ink-muted",["ground","ground-raised","ground-sunk"],4.5),
          ("matcha",["ground","ground-raised","matcha-soft"],4.5),("peony",["ground","ground-raised","peony-soft"],4.5),
          ("candle",["ground","ground-raised","candle-soft"],4.5),("alert",["ground","ground-raised"],4.5),
          ("on-matcha",["matcha"],4.5),("on-peony",["peony"],4.5),("on-wine",["wine"],4.5),
          ("line-strong",["ground","ground-raised"],3.0)]
bad=[]
for i,th in enumerate(("day","evening")):
    for fg,bgs,mn in checks:
        for bg in bgs:
            r=cr(D[fg][i],D[bg][i])
            if r<mn: bad.append((th,fg,bg,round(r,2)))
r=cr(D["wine"][0],D["ground"][0]); assert r>=4.5
print("contrast failures:", bad)
assert not bad

tokens = {
 "name": "Clover", "version": 1,
 "color": {
   "note": "Two themes that follow the house: Ditë (day: flowers, coffee, matcha) and Mbrëmje (evening: wine, meze, candles). Switch at 17:00 on screens that know the time.",
   "themes": [{"id":"light","name":"Ditë · day"},{"id":"dark","name":"Mbrëmje · evening"}],
   "tokens": [{"name":n,"value":{"light":d,"dark":e},"usage":u} for n,d,e,u in C] + [
     {"name":"leaf-lule","value":{"light":"{peony}","dark":"{peony}"},"usage":"Fill only. The flowers leaf of the clover (top right); flower content in illustrations."},
     {"name":"leaf-kafe","value":{"light":"{matcha}","dark":"{matcha}"},"usage":"Fill only. The coffee and matcha leaf (bottom right)."},
     {"name":"leaf-vere","value":{"light":"#5E1A33","dark":"#C25A7C"},"usage":"Fill only. The wine leaf (bottom left). Lighter in the evening so it holds on the aubergine ground."},
     {"name":"leaf-embelsira","value":{"light":"#C08A1E","dark":"#EDB54E"},"usage":"Fill only. The sweets leaf (top left), honey."},
     {"name":"primary","value":{"light":"{matcha}","dark":"{peony}"},"usage":"The one main action. Matcha by day, peony by evening. Alias, so the theme carries the switch."},
     {"name":"on-primary","value":{"light":"{on-matcha}","dark":"{on-peony}"},"usage":"Text on a primary fill."},
     {"name":"primary-soft","value":{"light":"{matcha-soft}","dark":"{peony-soft}"},"usage":"Tinted ground behind primary text."},
   ]},
 "type": {
   "fonts": [
     {"family":"Gloock","file":"fonts/Gloock-Regular.woff2","weight":"400","style":"normal"},
     {"family":"Familjen Grotesk","file":"fonts/FamiljenGrotesk-Variable.woff2","weight":"400 700","style":"normal"},
     {"family":"DM Mono","file":"fonts/DMMono-Regular.woff2","weight":"400","style":"normal"},
     {"family":"DM Mono","file":"fonts/DMMono-Medium.woff2","weight":"500","style":"normal"}
   ],
   "families": {
     "display": "\"Gloock\", \"Iowan Old Style\", Georgia, serif",
     "sans": "\"Familjen Grotesk\", ui-sans-serif, system-ui, sans-serif",
     "mono": "\"DM Mono\", ui-monospace, Menlo, monospace"
   },
   "groups": [
     {"name":"Display","family":"display","note":"Gloock, the wordmark's face. Headlines only, sentence case, never below 24px.","styles":[
       {"name":"display-xl","fontSize":"72px","lineHeight":"72px","fontWeight":400,"letterSpacing":"-0.02em","sample":"Lule ditën, verë mbrëmjen.","usage":"Signage, posters, the website hero. One per surface."},
       {"name":"display-lg","fontSize":"44px","lineHeight":"48px","fontWeight":400,"letterSpacing":"-0.015em","sample":"Buqeta e javës","usage":"Page titles, menu cover titles."},
       {"name":"display-md","fontSize":"28px","lineHeight":"34px","fontWeight":400,"letterSpacing":"-0.01em","sample":"Mbrëmje vere","usage":"Section titles: menu sections, card titles at large size."}]},
     {"name":"Text","family":"sans","note":"Familjen Grotesk: warm, a little hand-made at the joins, fully Albanian (ë, ç).","styles":[
       {"name":"lead","fontSize":"20px","lineHeight":"30px","fontWeight":400,"sample":"Lule të freskëta çdo mëngjes, kafe e matcha gjatë ditës, verë dhe meze në mbrëmje.","usage":"Intro paragraphs, one per page."},
       {"name":"body","fontSize":"16px","lineHeight":"24px","fontWeight":400,"sample":"Na tregoni për kë është buqeta dhe ne e përgatisim deri në orën 17:00.","usage":"Everything else."},
       {"name":"item","fontSize":"17px","lineHeight":"24px","fontWeight":600,"sample":"Matcha latte me qumësht tërshëre","usage":"Menu item and product names."},
       {"name":"small","fontSize":"14px","lineHeight":"20px","fontWeight":400,"sample":"Me mjaltë nga Rugova, sipas dëshirës.","usage":"Menu descriptions, hints, captions."},
       {"name":"label","fontSize":"12px","lineHeight":"16px","fontWeight":600,"letterSpacing":"0.14em","sample":"LULE · KAFE · VERË","usage":"Uppercase eyebrows and chip labels. Set in caps in the copy, keep it short."}]},
     {"name":"Figures","family":"mono","note":"DM Mono for anything you count: prices, hours, sizes.","styles":[
       {"name":"price","fontSize":"16px","lineHeight":"24px","fontWeight":500,"sample":"€3.50","usage":"Prices. Euro sign first, two decimals, no space."},
       {"name":"hours","fontSize":"13px","lineHeight":"20px","fontWeight":400,"letterSpacing":"0.02em","sample":"07:30–17:00 · 17:00–00:00","usage":"Opening hours, order cut-offs, dates. 24-hour clock, en dash for ranges."}]}
   ]},
 "spacing": {"note":"4px base. Menus breathe: rows sit space-4 apart, sections space-12.","tokens":[
   {"name":"space-1","value":"4px","usage":"Icon-to-label gap."},
   {"name":"space-2","value":"8px","usage":"Inside chips; between a name and its description."},
   {"name":"space-3","value":"12px","usage":"Between related controls."},
   {"name":"space-4","value":"16px","usage":"Card padding on phones; between menu rows."},
   {"name":"space-6","value":"24px","usage":"Card padding on desktop; between form fields."},
   {"name":"space-8","value":"32px","usage":"Between groups inside a section."},
   {"name":"space-12","value":"48px","usage":"Between sections."},
   {"name":"space-16","value":"64px","usage":"Page margins on large screens, poster margins."}]},
 "radius": {"note":"The leaf corner: two opposite corners round (radius-leaf), two stay nearly square (radius-sm). It comes from the leaf in the mark. Buttons and chips are pills.","tokens":[
   {"name":"radius-sm","value":"4px","usage":"Inputs; the two quiet corners of a leaf shape."},
   {"name":"radius-md","value":"12px","usage":"Small panels and image thumbnails."},
   {"name":"radius-leaf","value":"32px","usage":"Top-left and bottom-right corners of cards, photos and packaging labels."},
   {"name":"radius-full","value":"9999px","usage":"Buttons, chips, the day-part switch."}]},
 "shadow": {"note":"Shadows are rare. Paper and glass, not plastic.","tokens":[
   {"name":"shadow-sm","value":{"light":"0 1px 2px #1e2a1f14, 0 2px 6px #1e2a1f0f","dark":"0 1px 3px #000000a6"},"usage":"Cards at rest."},
   {"name":"shadow-lg","value":{"light":"0 6px 14px #1e2a1f14, 0 18px 40px -8px #1e2a1f29","dark":"0 18px 40px -8px #000000cc"},"usage":"Menus, popovers, the bouquet builder sheet."},
   {"name":"focus-ring","value":{"light":"0 0 0 2px #f3f4ec, 0 0 0 4px #4a671b","dark":"0 0 0 2px #1c1016, 0 0 0 4px #f28db0"},"usage":"Keyboard focus: a 2px ground gap, then 2px of solid primary (matcha by day, peony by evening). Meets 3:1 on every ground."}]}
}
json.dump(tokens, open(out,"w"), ensure_ascii=False, indent=1)
print("written")
