# BouquetCard

A bouquet a guest can order: an art panel, the name, three sizes, the price of the chosen size and one button.

- The card uses the leaf corner (`radius-leaf` top-left and bottom-right). Keep it; it is the brand's shape.
- Photography replaces the drawn art panel when it exists: shoot on `peony-soft` or `matcha-soft` paper, flowers centred, no props.
- The consumer provides `name`, `note`, `sizes` (`{id, price}`), and `onOrder`. The size state lives inside the card; listen with `onSizeChange`.
- Names are short and seasonal: “Bozhure”, “Tulipanë të bardhë”, “Buqeta e javës”.
