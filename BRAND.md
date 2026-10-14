**Clover** is a florist that is also a café by day (kafe, matcha, ëmbëlsira) and a wine bar by evening (verë, meze). A four-leaf clover is luck, and the house does four things, so each leaf is one of them: **lule, kafe, ëmbëlsira, verë**. Every rule below serves that idea, and the line that goes with it: **lule ditën, verë mbrëmjen**, flowers by day and wine by evening, in the same room.

Always pair the name with the descriptor (“Clover · lule, kafe, verë”) on signage, maps and social profiles, so it reads as this house and not as another brand called Clover.

## Voice

Write the way a neighbour talks across the counter: warm, short, a little playful, never salesy.

- **Albanian first.** Write every line in Albanian; add an English line under it only on the menu and the website, never on signage. Use ë and ç correctly, always.
- **Sentence case** everywhere. The wordmark is lowercase *clover*; in running text write *Clover*. The name stays in English; everything around it is Albanian.
- **Concrete over adjectives.** “Bozhure nga Drenica, sot në mëngjes”, not “lule të mrekullueshme”. Name the place a thing comes from (Rahovec, Rugova, Sharr).
- **Humour is allowed, lightly.** “Naj meze me verë?” on a chalkboard is right; jokes on the menu are not.
- No exclamation marks, no emoji, no ALL-CAPS sentences (caps are for `label` eyebrows only).
- Numbers: 24-hour clock with an en dash for ranges (`07:30–17:00`); prices with the euro sign first (`€3.50`); a glass and a bottle as `€4 / €22`.

Real lines to reuse:

> Lule ditën, verë mbrëmjen.
> Katër gjethe, një shtëpi.
> Kafe në mëngjes. Matcha pasdite. Verë kur bie nata.
> Lule me porosi. Na tregoni për kë është.
> Buqeta e javës, nga €24. Porosit deri në 17:00.

## Day and evening

The system has two themes and they follow the clock, not a preference.

- **Ditë** (`light`, 07:30–17:00): `ground` pale sage paper, `ink` stem green-black, `primary` = `matcha`.
- **Mbrëmje** (`dark`, 17:00–00:00): `ground` aubergine, `ink` petal white, `primary` = `peony`.
- Screens that know the time switch at 17:00 with a 400ms crossfade. Print picks one: the coffee menu, cups and bouquet tags are Ditë; the wine list and event posters are Mbrëmje. To pin an object to one palette in code, wrap it in `data-theme="light"` or `data-theme="dark"`.
- `OpenNow` is the component that tells guests which half of the day it is. Put it first on every screen.

## Logo

The mark is a four-leaf clover. Each leaf is one part of the house and carries its colour token: **lule** top right (`leaf-lule`, peony), **kafe and matcha** bottom right (`leaf-kafe`, matcha), **verë** bottom left (`leaf-vere`, wine), **ëmbëlsira** top left (`leaf-embelsira`, honey). The stem (`ink`) drops through the cut between the lower leaves. The wordmark is Gloock, lowercase. See the **Logo** page for anatomy, clear space and misuse, and the **Logos** asset group for files.

- Use `clover-lockup-horizontal` first; `clover-lockup-stacked` on cups, bags and square formats; `clover-mark` alone only where the name is already present.
- `-day` files go on light grounds, `-evening` files on dark grounds and on wine; `-ink` and `-paper` are one-colour versions for print, stamps and embossing.
- Clear space is 1x on every side (x = the height of one leaf). Minimums: lockup 96px / 25mm, wordmark 72px / 18mm, mark 16px / 5mm.
- The leaves never swap places or colours, and never get a fifth leaf or a different shape.
- Use the files rather than retyping the name, so the spacing stays exact.

## Colour

Name tokens, never hex values. Every text token states the grounds it is legible on; all pairs meet WCAG AA in both themes.

- `ground`, `ground-raised`, `ground-sunk` for surfaces; `ink` and `ink-muted` for text on them.
- `matcha` is the day: coffee, matcha, the day menu, the primary action by day.
- `peony` is the flowers: the lule leaf, bouquets, the order flow, the primary action by evening.
- `wine` is the evening and the façade: the fascia, the wine list, evening event covers. In the evening theme it is a fill only, with `on-wine` text.
- `candle` is for small highlights: “E RE”, “SOT”, today's sweet. Never a large area.
- `leaf-lule`, `leaf-kafe`, `leaf-vere`, `leaf-embelsira` are fills only: the clover's leaves, and colour-coding in illustrations, menu section markers and signage for each part of the house.
- Each brand colour has a `-soft` tint for backgrounds behind its own text, and an `on-` token for text on its fill.
- `alert` is for form errors, always with a written message, and it is never used as decoration.
- Keyboard focus is the `focus-ring` shadow: a 2px ground gap, then 2px of solid primary.

## Type

- **Gloock** (`display-xl`, `display-lg`, `display-md`) for headlines and section titles, the same face as the wordmark. Never below 24px, never for body.
- **Familjen Grotesk** (`lead`, `body`, `item`, `small`, `label`) for everything people read.
- **DM Mono** (`price`, `hours`) for anything you count: prices, hours, sizes, dates.

## Shape

The leaf corner: two opposite corners round at `radius-leaf` (top-left and bottom-right), the other two stay at `radius-sm`. It is a clover leaf reduced to a rectangle. Use it on cards, photos, bouquet tags, menus and packaging labels. Buttons, chips and the day-part switch are pills (`radius-full`). Inputs are `radius-sm`. Shadows are rare: `shadow-sm` on cards, `shadow-lg` only for things that float.

## Space

4px base. Menu rows sit `space-4` apart with a `line` hairline between them; sections are `space-12` apart; page margins on large screens are `space-16`. Let menus breathe.

## Iconography

A custom set of 24px line icons in the **Icons** group: 1.6px stroke, round caps and joins, drawn in `ink`. Each names a part of the house: kafe, matcha, verë, buqetë, ëmbëlsira, meze, lule me porosi, ditë, mbrëmje, hapësira. Use them at 24px or 20px beside a label, never alone as decoration, and never with emoji. On evening grounds, inline the SVG and set `stroke` to `currentColor`.

## Imagery

- **Day**: flowers shot in daylight on `matcha-soft` or `peony-soft` paper, centred, no props; coffee and matcha from above on the marble counter.
- **Evening**: low candle light, warm, glasses and meze boards close up; let the edges fall into `ground`.
- Real people from the house, never stock. No filters that shift the greens.

## Motion

Quiet. The only orchestrated moment is the 17:00 crossfade between themes (400ms ease). Buttons press down 1px. Respect `prefers-reduced-motion`.

## The room

The same system briefs the architect, so the space and the screens match.

- Walls and ceiling in a pale sage lime plaster close to `ground`; the bar front in matcha-green glazed tile close to `matcha`.
- Four zones that follow the four leaves: the flower window (peony), the coffee bar (matcha), the sweets counter (honey), the wine wall (wine). Mark each with its leaf.
- Banquettes in wine velvet close to `wine`; brass candle sconces for the evening (`candle`).
- The flower display is the shop window and the first thing seen from the street; a wine fascia with the paper lockup above it.
- Tables and shelves with rounded corners on the leaf diagonal, echoing `radius-leaf`.
- Two lighting scenes on one switch: bright daylight until 17:00, low and warm after.

## Components

`window.Clover` (React 18): `Button`, `Tag`, `OpenNow`, `MenuItem`, `BouquetCard`, `Field`. Each has guidelines and a live preview. The **Logo** and **Applications** pages show the identity on real objects: fascia, cup, bouquet tag, business card, both menus and two Instagram posts.
