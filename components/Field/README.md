# Field

A labelled input for the “Lule me porosi” form and table bookings.

- The label is a short noun (“Për kë është?”, “Data e dorëzimit”); the hint says what good input looks like; the error says what to fix, in one sentence.
- `multiline` for the card message. Borders are `line-strong` (3:1); focus is the `focus-ring` token.
- The consumer provides `label`, `value`/`onChange` and `error`. Errors show in `alert` with text, never by colour alone.
