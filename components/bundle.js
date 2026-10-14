/* @ds-bundle: {"format":4,"namespace":"Clover","components":[{"name":"Button"},{"name":"Tag"},{"name":"OpenNow"},{"name":"MenuItem"},{"name":"BouquetCard"},{"name":"Field"}]} */
(function () {
  var React = window.React;
  var h = React.createElement;

  function cx() {
    var out = [];
    for (var i = 0; i < arguments.length; i++) if (arguments[i]) out.push(arguments[i]);
    return out.join(' ');
  }
  function omit(obj, keys) {
    var o = {};
    for (var k in obj) if (Object.prototype.hasOwnProperty.call(obj, k) && keys.indexOf(k) < 0) o[k] = obj[k];
    return o;
  }

  var BLOOM = 'M32 18C36.5 19 40.5 22.5 43 28C44.6 21.6 47 16.8 50 12.5C53 16.8 55.4 21.6 57 28C59.5 22.5 63.5 19 68 18C70 41 62.5 55.5 50 57.5C37.5 55.5 30 41 32 18Z';
  var STEM = 'M46.8 56H53.2V85H46.8ZM47 80.5C38 79.8 32.4 73 31.6 62.4C40.6 63.6 46 70 47 75.2ZM37.7 83.6H62.3A2.7 2.7 0 0 1 62.3 89H37.7A2.7 2.7 0 0 1 37.7 83.6Z';

  function Icon(props) {
    var paths = {
      sun: ['M3 17h18', 'M7 17a5 5 0 0 1 10 0', 'M12 5v2.5M5.2 9.2l1.7 1.7M18.8 9.2l-1.7 1.7M3 13.5h1.8M19.2 13.5H21'],
      moon: ['M17.5 14.5A7.5 7.5 0 0 1 9.5 3.5a7.5 7.5 0 1 0 8 11z', 'M18 3.5v3M16.5 5h3']
    }[props.name] || [];
    return h('svg', { className: 'cv-icon', viewBox: '0 0 24 24', width: 16, height: 16, fill: 'none', stroke: 'currentColor', strokeWidth: 1.8, strokeLinecap: 'round', strokeLinejoin: 'round', 'aria-hidden': true },
      paths.map(function (d, i) { return h('path', { key: i, d: d }); }));
  }

  /** The one button. Primary at most once per view. */
  function Button(props) {
    var variant = props.variant || 'primary';
    var size = props.size || 'md';
    var rest = omit(props, ['variant', 'size', 'className', 'children']);
    return h('button', Object.assign({ type: 'button' }, rest, {
      className: cx('cv-btn', 'cv-btn-' + variant, size === 'sm' && 'cv-btn-sm', props.className)
    }), props.children);
  }

  /** One or two words of status beside a name. */
  function Tag(props) {
    return h('span', { className: cx('cv-tag', 'cv-tag-' + (props.tone || 'neutral')) }, props.children);
  }

  /** Which half of the day the house is in right now. */
  function OpenNow(props) {
    var evening = props.part === 'evening';
    var until = props.until || (evening ? '00:00' : '17:00');
    var what = props.serving || (evening ? 'verë e meze' : 'kafe e matcha');
    return h('span', { className: cx('cv-open', evening ? 'cv-open-evening' : 'cv-open-day'), role: 'status' },
      h(Icon, { name: evening ? 'moon' : 'sun' }),
      h('span', { className: 'cv-open-part' }, evening ? 'Mbrëmje' : 'Ditë'),
      h('span', { className: 'cv-open-sep', 'aria-hidden': true }, '·'),
      h('span', null, what + ' deri në '),
      h('span', { className: 'cv-open-time' }, until));
  }

  /** A row on the menu: name, a short note, a price. */
  function MenuItem(props) {
    return h('div', { className: 'cv-item' },
      h('div', { className: 'cv-item-main' },
        h('div', { className: 'cv-item-name' }, props.name, props.tag ? h(Tag, { tone: props.tagTone || 'candle' }, props.tag) : null),
        props.note ? h('div', { className: 'cv-item-note' }, props.note) : null),
      h('div', { className: 'cv-item-price' }, props.price));
  }

  /** A bouquet you can order: size picker, starting price, one action. */
  function BouquetCard(props) {
    var sizes = props.sizes || [{ id: 'S', price: '€18' }, { id: 'M', price: '€28' }, { id: 'L', price: '€42' }];
    var initial = props.defaultSize || sizes[1 % sizes.length].id;
    var st = React.useState(initial);
    var size = st[0], setSize = st[1];
    var current = sizes.filter(function (s) { return s.id === size; })[0] || sizes[0];
    var tone = props.tone || 'peony';
    return h('article', { className: 'cv-bouquet' },
      h('div', { className: cx('cv-bouquet-art', 'cv-art-' + tone), 'aria-hidden': true },
        h('svg', { viewBox: '0 0 100 100', className: 'cv-bouquet-svg' },
          h('g', { transform: 'translate(-22 6) rotate(-14 50 89)' }, h('path', { className: 'b', d: BLOOM }), h('path', { className: 's', d: STEM })),
          h('g', { transform: 'translate(0 -4)' }, h('path', { className: 'b', d: BLOOM }), h('path', { className: 's', d: STEM })),
          h('g', { transform: 'translate(22 6) rotate(14 50 89)' }, h('path', { className: 'b', d: BLOOM }), h('path', { className: 's', d: STEM })))),
      h('div', { className: 'cv-bouquet-body' },
        h('div', { className: 'cv-bouquet-head' },
          h('h3', { className: 'cv-bouquet-name' }, props.name),
          props.tag ? h(Tag, { tone: 'peony' }, props.tag) : null),
        props.note ? h('p', { className: 'cv-bouquet-note' }, props.note) : null,
        h('div', { className: 'cv-sizes', role: 'radiogroup', 'aria-label': 'Madhësia' },
          sizes.map(function (s) {
            return h('button', {
              key: s.id, type: 'button', role: 'radio', 'aria-checked': s.id === size,
              className: cx('cv-size', s.id === size && 'is-on'),
              onClick: function () { setSize(s.id); if (props.onSizeChange) props.onSizeChange(s.id); }
            }, s.id);
          })),
        h('div', { className: 'cv-bouquet-foot' },
          h('span', { className: 'cv-bouquet-price' }, current.price),
          h(Button, { size: 'sm', onClick: props.onOrder }, props.cta || 'Porosit'))));
  }

  /** A labelled input or textarea with a hint and an error message. */
  function Field(props) {
    var id = props.id || ('cv-f-' + String(props.label || '').toLowerCase().replace(/[^a-z0-9]+/g, '-'));
    var hintId = id + '-hint';
    var rest = omit(props, ['id', 'label', 'hint', 'error', 'multiline', 'className']);
    var control = h(props.multiline ? 'textarea' : 'input', Object.assign({ rows: props.multiline ? 3 : undefined }, rest, {
      id: id, className: 'cv-input', 'aria-invalid': props.error ? true : undefined,
      'aria-describedby': (props.hint || props.error) ? hintId : undefined
    }));
    return h('div', { className: cx('cv-field', props.error && 'has-error', props.className) },
      h('label', { className: 'cv-label', htmlFor: id }, props.label),
      control,
      props.error ? h('div', { id: hintId, className: 'cv-error' }, props.error)
        : props.hint ? h('div', { id: hintId, className: 'cv-hint' }, props.hint) : null);
  }

  var g = window;
  g.Clover = Object.assign(g.Clover || {}, { Button: Button, Tag: Tag, OpenNow: OpenNow, MenuItem: MenuItem, BouquetCard: BouquetCard, Field: Field });
})();
