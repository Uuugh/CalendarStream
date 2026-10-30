// The rule dialog (F4): a title, If lines (conditions, joined by and / or, grouped with brackets) and
// Then lines (what to do), Apply to, and Remove / Cancel | Apply. It's sent as JSON (see app/rules.py).
var ruleDialog = document.getElementById('ruledialog'), ruleForm = ruleDialog.querySelector('form'),
    condBox = ruleForm.querySelector('.conds'), actBox = ruleForm.querySelector('.acts'), editing = null;
function brackets(n, ch, cls, title) {
  var h = '', ghost = '<button type="button" class="brk spare ' + cls + '" title="' + esc(title) + '" aria-label="' + esc(title) + '">' + ch + '</button>';
  for (var i = 0; i < n; i++) h += '<button type="button" class="brk on ' + cls + '" title="' + esc(title) + '">' + ch + '</button>';
  return cls === 'open' ? ghost + h : h + ghost;
}
// Insert helpers (0.2.8-beta.15): a regex or a pattern is built by clicking what it should do; each puts its
// piece at the cursor (or around the selected text)
var RX_HELP = {
  regex: [['^', 'starts'], ['$', 'ends'], ['\\b…\\b', 'word'], ['(A|B)', 'either'], ['.*', 'any'], ['\\d+', 'digits'], ['\\s', 'space'], ['?', 'optional'], ['a\\.b', 'literal']],
  pattern: [['*', 'anyText'], ['#', 'digit'], ['?', 'oneChar']]
};
function condFields(c) {
  var t = c.type, h = '';
  if (t === 'text' || t === 'any') {
    h = '<input type="text" class="cval" maxlength="200" value="' + esc(c.value || '') + '" aria-label="' + esc(RD.types[t]) + '"'
      + (c.op === 'pattern' ? ' placeholder="*E####"' : c.op === 'regex' ? ' placeholder="E\\d{4}"' : '') + ' spellcheck="false">'
      + '<button type="button" class="ghost casebtn" aria-pressed="' + !!c.case + '" title="' + esc(RD.t.caps) + '">Aa</button>';
    if (c.op === 'regex' || c.op === 'pattern') h += rxTools(c.op);
  }
  else if (t === 'date' || t === 'time') {
    var kind = t === 'date' ? 'date' : 'time';
    h = '<input type="' + kind + '" class="cval" value="' + esc(c.value || '') + '">';
    if (c.op === 'between') h += '<span class="arrow">–</span><input type="' + kind + '" class="cval2" value="' + esc(c.value2 || '') + '">';
  } else if (t === 'days') {
    h = '<span class="dayset" data-op="' + esc(c.op) + '">' + RD.days.map(function (d, i) {
      return '<button type="button" class="wd" data-d="' + i + '" aria-pressed="' + ((c.days || []).indexOf(i) >= 0) + '">' + esc(d) + '</button>'; }).join('') + '</span>';
  } else if (t === 'length' && c.op !== 'days') {
    var m = c.minutes || 0, w = Math.floor(m / 10080), d = Math.floor(m % 10080 / 1440), hh = Math.floor(m % 1440 / 60), mi = m % 60;
    h = '<span class="lenset">' + [['w', w, RD.t.weeks], ['d', d, RD.t.days], ['h', hh, RD.t.hours], ['m', mi, RD.t.minutes]].map(function (x, i) {
      return (i ? '<b class="colon">:</b>' : '') + '<input type="number" min="0" class="len" data-u="' + x[0] + '" value="' + (x[1] || '') + '" placeholder="' + esc(x[2]) + '" aria-label="' + esc(x[2]) + '">'; }).join('')
      + '</span><span class="mnote">' + esc(RD.t.noEnd) + '</span>';
  }
  return h;
}
// The regex test box (0.2.8-beta.15): helpers, then your event titles (one per line, editable) each with
// ✓ or ✕ and the part that matched; checked by the server, with the rule's own matching, as you type.
function rxTools(op) {
  return '<div class="rxtools"><div class="rxhelp">' + RX_HELP[op].map(function (x) {
      return '<button type="button" class="ghost rxins" data-ins="' + esc(x[1]) + '" title="' + esc(RD.rx[x[1]]) + '">' + esc(x[0]) + '</button>'; }).join('')
    + '</div><p class="rxerr" hidden></p>'
    + '<div class="rxbox"><div class="rxhead"><span class="rxcount"></span><button type="button" class="ghost rxedit" title="' + esc(RD.t.editSamples) + '" aria-label="' + esc(RD.t.editSamples) + '">'
    + {{ icon("edit", 15)|string|tojson }} + '</button></div>'
    + '<ol class="rxlist"></ol><textarea class="rxsamples" rows="6" hidden spellcheck="false" aria-label="' + esc(RD.t.editSamples) + '">' + esc((RD.samples || []).join('\n')) + '</textarea></div></div>';
}
function rxInsert(row, kind) {
  var f = row.querySelector('.cval'), a = f.selectionStart, b = f.selectionEnd, v = f.value, sel = v.slice(a, b), put;
  var esc1 = function (x) { return x.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); };
  put = { starts: '^', ends: '$', word: '\\b' + (sel || '') + '\\b', either: '(' + (sel ? sel.trim().split(/\s+/).join('|') : 'A|B') + ')', any: '.*', digits: '\\d+',
          space: '\\s', optional: '?', literal: esc1(sel), anyText: '*', digit: '#', oneChar: '?' }[kind];
  if (kind === 'starts') { f.value = '^' + v.replace(/^\^/, ''); }
  else if (kind === 'ends') { f.value = v.replace(/\$$/, '') + '$'; }
  else { f.value = v.slice(0, a) + put + v.slice(b); var at = a + put.length; f.setSelectionRange(at, at); }
  f.focus(); rxTest(row);
}
var rxTimer = null;
function rxTest(row) {
  var box = row.querySelector('.rxtools');
  if (!box) return;
  clearTimeout(rxTimer);
  rxTimer = setTimeout(function () {
    var body = new URLSearchParams({ csrf: CSRF, value: row.querySelector('.cval').value, op: row.querySelector('.cop').value,
                                     case: row.querySelector('.casebtn').getAttribute('aria-pressed') === 'true' ? '1' : '', samples: box.querySelector('.rxsamples').value });
    fetch('/rules/test', { method: 'POST', body: body, credentials: 'same-origin', headers: { 'X-CS-Async': '1' } })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        var err = box.querySelector('.rxerr'), list = box.querySelector('.rxlist');
        err.hidden = !j.error; err.innerHTML = j.error ? ICON.warn + esc(j.error) : '';
        row.classList.toggle('rxbad', !!j.error); rxBlock();
        var n = 0;
        list.innerHTML = (j.results || []).map(function (x) {
          if (x.match) n++;
          // the span counts characters (Python), so slice by characters, not UTF-16 units (an emoji is one)
          var t = Array.from(x.text), sp = x.span || [], part = function (a, b) { return esc(t.slice(a, b).join('')); };
          var shown = x.match && sp.length ? part(0, sp[0]) + '<mark>' + part(sp[0], sp[1]) + '</mark>' + part(sp[1]) : part(0);
          return '<li class="' + (x.match ? 'yes' : 'no') + '"><span class="rxmark">' + (x.match ? '✓' : '✕') + '</span>' + shown + '</li>'; }).join('');
        box.querySelector('.rxcount').textContent = j.error ? '' : RD.t.matchCount.replace('{n}', n).replace('{total}', (j.results || []).length);
      });
  }, 300);
}
// A rule with a broken pattern can't be applied: its Apply waits until the pattern works
function rxBlock() {
  var bad = !!condBox.querySelector('.cond.rxbad'), sv = ruleForm.querySelector('.psave');
  if (sv) sv.disabled = bad;
}
function condRow(c) {
  c = c || { type: 'text', op: 'contains', value: '', case: false, open: 0, close: 0, join: 'and' };
  var row = document.createElement('div');
  row.className = 'cond'; row.dataset.open = c.open || 0; row.dataset.close = c.close || 0; row.dataset.join = c.join || 'and';
  row.innerHTML = '<span class="brks open">' + brackets(c.open || 0, '(', 'open', RD.t.open) + '</span>'
    + '<select class="ctype" aria-label="If">' + opts(Object.keys(RD.types).map(function (k) { return [k, RD.types[k]]; }), c.type) + '</select>'
    + '<select class="cop">' + opts(RD.ops[c.type], c.op) + '</select><span class="cfields">' + condFields(c) + '</span>'
    + '<span class="brks close">' + brackets(c.close || 0, ')', 'close', RD.t.close) + '</span>'
    // & (and) · | (or) · ✕ (take the line out), grey until chosen (0.2.8-beta.15)
    + '<span class="cjoins" role="group" aria-label="' + esc(RD.t.and) + ' / ' + esc(RD.t.or) + '">'
    + '<button type="button" class="ghost cj" data-j="and" title="' + esc(RD.t.andAdd) + '" aria-label="' + esc(RD.t.and) + '" aria-pressed="false">&amp;</button>'
    + '<button type="button" class="ghost cj" data-j="or" title="' + esc(RD.t.orAdd) + '" aria-label="' + esc(RD.t.or) + '" aria-pressed="false">|</button>'
    + '<button type="button" class="ghost cdel" title="' + esc(RD.t.remove) + '" aria-label="' + esc(RD.t.remove) + '">' + {{ icon("close", 16)|string|tojson }} + '</button></span>';
  if (c.op === 'regex' || c.op === 'pattern') setTimeout(function () { rxTest(row); }, 0);
  return row;
}
function actFields(a) {
  var t = a.type;
  if (t === 'color') {      // one of Google's 11 colors (0.2.8-beta.5); an older rule's own color shows as the nearest
    var cur = nearestPalette(a.color || RD.palette[0][0]);
    return '<input type="hidden" class="aval" value="' + esc(cur) + '"><span class="palette" role="radiogroup" aria-label="' + esc(RD.t.color) + '">'
      + RD.palette.map(function (p) { return '<button type="button" class="pal" role="radio" data-c="' + esc(p[0]) + '" title="' + esc(p[1]) + '" aria-label="' + esc(p[1])
        + '" aria-checked="' + (p[0] === cur) + '" style="--c:' + esc(p[0]) + '"></button>'; }).join('') + '</span>';
  }
  // Emoji: the field, the common ones, then a search field for every emoji (0.2.8-beta.17, was a face+ button):
  // typing in it (or clicking it) opens the full list under the line, ten a line, filtered as you type
  if (t === 'emoji') return '<input type="text" class="aval emoji" maxlength="16" value="' + esc(a.emoji || '') + '" aria-label="' + esc(RD.t.emoji) + '" placeholder="✈️">'
      + '<span class="helpdot notedot emowarn" tabindex="0" role="button" aria-label="' + esc(RD.t.olderWindows) + '" aria-expanded="false"'
      + (emoNewer(a.emoji) ? '' : ' hidden') + '>' + RD.info_icon + '<span class="helptip" role="tooltip">' + esc(RD.t.olderWindows) + '</span></span>'
      + '<span class="emojis">' + RD.emoji.map(function (x) { return '<button type="button" class="ghost emo">' + x + '</button>'; }).join('') + '</span>'
      + '<input type="search" class="emofind" placeholder="' + esc(RD.t.searchEmoji) + '" aria-label="' + esc(RD.t.searchEmoji) + '" aria-expanded="false" autocomplete="off">'
      + '<div class="emopick" hidden><div class="emogrid" role="listbox" aria-label="' + esc(RD.t.emoji) + '"></div></div>';
  // Create event (0.2.8-beta.17, I6): read as a sentence, in groups that wrap whole, never field by field:
  // [template or New event…] [Title] [All day] lasting [1:00] · at [Location] · [0:00] [before the start]
  if (t === 'event') {
    var isNew = !a.template, h = '<span class="evpart"><select class="atpl" aria-label="' + esc(RD.t.newEvent) + '">' + opts(RD.templates, a.template)
      + '<option value=""' + (isNew ? ' selected' : '') + '>' + esc(RD.t.newEvent) + '</option></select>';
    if (isNew) h += '<input type="text" class="anew title" maxlength="200" value="' + esc(a.title || '') + '" placeholder="' + esc(RD.t.title) + '" aria-label="' + esc(RD.t.title) + '"></span>'
      + '<span class="evpart"><label class="mnote"><input type="checkbox" class="anew allday"' + (a.all_day ? ' checked' : '') + '> ' + esc(RD.t.allDay) + '</label>'
      + '<span class="mnote">' + esc(RD.t.lasting) + '</span><input type="text" class="anew minutes dur" value="' + hm(a.minutes || 60) + '" title="' + esc(RD.t.length) + '" aria-label="' + esc(RD.t.length) + '"></span>'
      + '<span class="evpart"><span class="mnote">' + esc(RD.t.at) + '</span><input type="text" class="anew location" maxlength="200" value="' + esc(a.location || '') + '" placeholder="' + esc(RD.t.location) + '" aria-label="' + esc(RD.t.location) + '"></span>';
    else h += '</span>';
    return h + '<span class="evpart"><input type="text" class="aoff dur" value="' + hm(a.offset || 0) + '" title="' + esc(RD.t.time) + '" aria-label="' + esc(RD.t.time) + '">'
      + '<select class="awhen">' + opts(RD.when, a.when || 'before_start') + '</select></span>';
  }
  if (t === 'change') return '<span class="mnote">' + esc(RD.t.changeTo) + '</span><select class="ato"><option value="allday"' + (a.to === 'allday' ? ' selected' : '') + '>' + esc(RD.t.toAllDay)
      + '</option><option value="length"' + (a.to === 'length' ? ' selected' : '') + '>' + esc(RD.t.toLength) + '</option></select>'
      + (a.to === 'length' ? '<input type="text" class="amin dur" value="' + hm(a.minutes || 60) + '" title="' + esc(RD.t.length) + '">' : '');
  return '';
}
function nearestPalette(hex) {
  function rgb(h) { return [1, 3, 5].map(function (i) { return parseInt(h.substr(i, 2), 16); }); }
  if (!/^#[0-9a-f]{6}$/i.test(hex || '')) return RD.palette[0][0];
  var c = rgb(hex), best = RD.palette[0][0], dist = Infinity;
  RD.palette.forEach(function (p) { var q = rgb(p[0]), d = (c[0] - q[0]) * (c[0] - q[0]) + (c[1] - q[1]) * (c[1] - q[1]) + (c[2] - q[2]) * (c[2] - q[2]);
    if (d < dist) { dist = d; best = p[0]; } });
  return best;
}
function actRow(a) {
  a = a || { type: 'color', color: '#d50000' };
  var row = document.createElement('div');
  row.className = 'act';
  row.innerHTML = '<select class="atype" aria-label="Then">' + opts(RD.actions, a.type) + '</select><span class="afields">' + actFields(a) + '</span>'
    + '<button type="button" class="ghost adel" title="' + esc(RD.t.remove) + '" aria-label="' + esc(RD.t.remove) + '">' + {{ icon("close", 16)|string|tojson }} + '</button>'
    + '<button type="button" class="ghost aadd" title="+" aria-label="+">' + {{ icon("add", 16)|string|tojson }} + '</button>';
  return row;
}
// Reading a line back
function readCond(row) {
  var c = { type: row.querySelector('.ctype').value, op: row.querySelector('.cop').value, open: +row.dataset.open, close: +row.dataset.close,
            join: row.dataset.join || 'and' };
  if (c.type === 'text' || c.type === 'any') { c.value = row.querySelector('.cval').value; c.case = row.querySelector('.casebtn').getAttribute('aria-pressed') === 'true'; }
  if (c.type === 'date' || c.type === 'time') { c.value = row.querySelector('.cval').value; var v2 = row.querySelector('.cval2'); c.value2 = v2 ? v2.value : ''; }
  if (c.type === 'days') c.days = row.querySelector('.dayset').dataset.sel ? JSON.parse(row.querySelector('.dayset').dataset.sel)
                                 : Array.prototype.map.call(row.querySelectorAll('.wd[aria-pressed=true]'), function (b) { return +b.dataset.d; });
  if (c.type === 'length') {
    var u = { w: 10080, d: 1440, h: 60, m: 1 }, total = 0;
    row.querySelectorAll('.len').forEach(function (i) { total += (+i.value || 0) * u[i.dataset.u]; });
    c.minutes = c.op === 'days' ? 1440 : total;
  }
  return c;
}
function readAct(row) {
  var a = { type: row.querySelector('.atype').value }, f = function (s) { return row.querySelector(s); };
  if (a.type === 'color') a.color = f('.aval').value;
  if (a.type === 'emoji') a.emoji = f('.aval').value;
  if (a.type === 'event') {
    a.template = f('.atpl').value; a.offset = minutesOf(f('.aoff').value) || 0; a.when = f('.awhen').value;
    // (just after "New event" is picked its fields aren't there yet: the row is redrawn with them)
    if (!a.template && f('.anew.title')) { a.title = f('.anew.title').value; a.all_day = f('.anew.allday').checked; a.minutes = minutesOf(f('.anew.minutes').value) || 60; a.location = f('.anew.location').value; }
  }
  // (.amin isn't there yet just after "to a length" is picked: the row is redrawn with it)
  if (a.type === 'change') { a.to = f('.ato').value; if (a.to === 'length') a.minutes = (f('.amin') && minutesOf(f('.amin').value)) || 60; }
  return a;
}
// Brackets: each level of nesting in its own color; the last line's and / or adds a line
function drawConds() {
  var rows = condBox.querySelectorAll('.cond'), depth = 0;
  rows.forEach(function (row, i) {
    row.querySelectorAll('.brk.on.open').forEach(function (b) { depth++; b.dataset.level = Math.min(depth, 3); });
    row.querySelectorAll('.brk.on.close').forEach(function (b) { b.dataset.level = Math.max(1, Math.min(depth, 3)); depth--; });
    var join = i < rows.length - 1 ? (rows[i + 1].dataset.join || 'and') : '';
    row.querySelectorAll('.cj').forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.j === join)); });
    row.querySelector('.cdel').hidden = rows.length < 2;
  });
  ruleForm.classList.toggle('unbalanced', depth !== 0);
}
// A ")" with no "(" before it to pair with: a "(" is added (and flashes) on the first line of the
// group it closes, i.e. the first line at the same level of brackets (the rule's first line at the top)
function pairOpen(row) {
  var rows = Array.prototype.slice.call(condBox.querySelectorAll('.cond')), i = rows.indexOf(row), d = 0, before = [];
  rows.forEach(function (r) { before.push(d); d += +r.dataset.open - +r.dataset.close; });
  var end = before[i] + +row.dataset.open - +row.dataset.close;
  if (end >= 0) return;                         // it pairs with an earlier "("
  var j = i;
  while (j > 0 && before[j - 1] + +rows[j - 1].dataset.open - +rows[j - 1].dataset.close >= before[i] && before[j - 1] >= before[i]) j--;
  var target = rows[j], n = Math.min(3, +target.dataset.open + 1);
  target.dataset.open = n;
  target.querySelector('.brks.open').innerHTML = brackets(n, '(', 'open', RD.t.open);
  var added = target.querySelectorAll('.brk.on.open'); added = added[added.length - 1];
  if (added) { added.classList.add('flash'); setTimeout(function () { added.classList.remove('flash'); }, 1500); }
}
function drawActs() {
  var rows = actBox.querySelectorAll('.act');
  rows.forEach(function (row, i) { row.querySelector('.aadd').hidden = i < rows.length - 1; row.querySelector('.adel').hidden = rows.length < 2;
                                   emoWarn(row); });
}
condBox.addEventListener('click', function (e) {
  var row = e.target.closest('.cond');
  if (!row) return;
  var b = e.target.closest('.brk');
  if (b) {
    var side = b.classList.contains('open') ? 'open' : 'close', n = +row.dataset[side];
    n = b.classList.contains('spare') ? Math.min(3, n + 1) : n - 1;
    row.dataset[side] = n;
    row.querySelector('.brks.' + side).innerHTML = brackets(n, side === 'open' ? '(' : ')', side, RD.t[side]);
    if (side === 'close' && b.classList.contains('spare')) pairOpen(row);
    drawConds(); return;
  }
  if (e.target.closest('.casebtn')) { var cb = e.target.closest('.casebtn'); cb.setAttribute('aria-pressed', String(cb.getAttribute('aria-pressed') !== 'true')); rxTest(row); return; }
  var ins = e.target.closest('.rxins');
  if (ins) { rxInsert(row, ins.dataset.ins); return; }
  // the test box: its titles are edited in place (✎, or a click on the list), and tested again after
  if (e.target.closest('.rxedit, .rxlist')) {
    var ta = row.querySelector('.rxsamples'), list = row.querySelector('.rxlist');
    ta.hidden = false; list.hidden = true; ta.focus(); return;
  }
  var cj = e.target.closest('.cj');
  if (cj) {     // the last line's & or | adds a line joined that way; another line's switches its join
    var nx = row.nextElementSibling;
    if (!nx) { var nr = condRow(); nr.dataset.join = cj.dataset.j; condBox.appendChild(nr); nr.querySelector('.cval, select').focus(); }
    else nx.dataset.join = cj.dataset.j;
    drawConds(); return;
  }
  if (e.target.closest('.cdel')) {
    var next = row.nextElementSibling;
    if (next && !row.previousElementSibling) next.dataset.join = 'and';
    if (condBox.querySelectorAll('.cond').length > 1) row.remove(); else row.replaceWith(condRow());
    drawConds(); return;
  }
  var day = e.target.closest('.dayset .wd');
  if (day) {      // standard selection: a click picks one day, Ctrl (⌘) adds or removes one, Shift a run
    var set = day.parentNode, all = Array.prototype.slice.call(set.querySelectorAll('.wd')), d = +day.dataset.d, op = set.dataset.op;
    var last = set.dataset.last ? +set.dataset.last : d, sel;
    if (op === 'between') sel = e.shiftKey && set.dataset.last ? [last, d] : [d];
    else if (op !== 'is') sel = [d];
    else if (e.shiftKey && set.dataset.last) { sel = []; for (var x = Math.min(last, d); x <= Math.max(last, d); x++) sel.push(x); }
    else if (e.ctrlKey || e.metaKey) { sel = all.filter(function (b) { return b.getAttribute('aria-pressed') === 'true'; }).map(function (b) { return +b.dataset.d; });
      sel = sel.indexOf(d) >= 0 ? sel.filter(function (x) { return x !== d; }) : sel.concat([d]); }
    else sel = [d];
    if (!e.shiftKey) set.dataset.last = d;
    set.dataset.sel = JSON.stringify(sel);
    var lit = op === 'between' && sel.length === 2 ? (function () { var r = [], x = sel[0]; while (true) { r.push(x); if (x === sel[1]) break; x = (x + 1) % 7; } return r; })() : sel;
    all.forEach(function (b) { b.setAttribute('aria-pressed', String(lit.indexOf(+b.dataset.d) >= 0)); });
  }
});
condBox.addEventListener('change', function (e) {
  var row = e.target.closest('.cond');
  if (!row) return;
  if (e.target.matches('.ctype')) { row.replaceWith(condRow({ type: e.target.value, op: RD.ops[e.target.value][0][0], open: +row.dataset.open, close: +row.dataset.close, join: row.dataset.join })); drawConds(); }
  else if (e.target.matches('.cop')) { var c = readCond(row); c.op = e.target.value; if (c.type === 'days' && c.op !== 'is') c.days = c.days.slice(0, c.op === 'between' ? 2 : 1); row.replaceWith(condRow(c)); drawConds(); }
});
condBox.addEventListener('input', function (e) {
  var row = e.target.closest('.cond');
  if (row && e.target.matches('.cval, .rxsamples')) rxTest(row);
});
condBox.addEventListener('focusout', function (e) {     // the edited titles are shown with their ✓ / ✕ again
  if (!e.target.matches('.rxsamples')) return;
  var row = e.target.closest('.cond');
  e.target.hidden = true; row.querySelector('.rxlist').hidden = false; rxTest(row);
});
actBox.addEventListener('click', function (e) {
  var row = e.target.closest('.act');
  if (!row) return;
  if (e.target.closest('.aadd')) { var a = actRow({ type: 'emoji', emoji: '' }); actBox.appendChild(a); drawActs(); return; }
  if (e.target.closest('.adel')) { row.remove(); drawActs(); return; }
  var emo = e.target.closest('.emo');
  if (emo) { row.querySelector('.aval.emoji').value = emo.textContent; emoWarn(row); var pk = row.querySelector('.emopick');
             if (pk && !pk.hidden) { row.querySelector('.emofind').value = ''; emoOpen(row, false); } }
  if (e.target.closest('.emofind')) { emoOpen(row, true); return; }
  var pal = e.target.closest('.pal');
  if (pal) { row.querySelector('.aval').value = pal.dataset.c;
             row.querySelectorAll('.pal').forEach(function (b) { b.setAttribute('aria-checked', String(b === pal)); }); }
});
// Every emoji (0.2.8-beta.15): loaded once, the first time the picker opens
var emojiData = null;
// (0.2.8-beta.19, F8) Emoji older Windows may not draw: flags (regional letters or tag letters) and those newer than
// Emoji 12.0 (marked in emoji.json); the chosen one gets an (i) beside the field
var emojiNewer = null;
function loadEmoji() {
  return emojiData || (emojiData = fetch('/static/emoji.json?v=' + encodeURIComponent(RD.version), { credentials: 'same-origin' }).then(function (r) { return r.json(); }));
}
function emoNewer(v) {
  v = (v || '').replace(/\uFE0F/g, '');
  if (!v) return false;
  if (/[\u{1F1E6}-\u{1F1FF}\u{E0020}-\u{E007F}]/u.test(v)) return true;
  if (!emojiNewer) return false;
  for (var i = 0; i < emojiNewer.length; i++) if (v.indexOf(emojiNewer[i]) >= 0) return true;
  return false;
}
function emoWarn(row) {
  var f = row.querySelector('.aval.emoji'), w = row.querySelector('.emowarn');
  if (!f || !w) return;
  w.hidden = !emoNewer(f.value);
  if (f.value && !emojiNewer && /[^\x00-\u2FFF]/.test(f.value)) loadEmoji().then(function (d) {
    emojiNewer = d.emoji.filter(function (x) { return x[3]; }).map(function (x) { return x[0].replace(/\uFE0F/g, ''); });
    w.hidden = !emoNewer(f.value);
  });
}
function emoOpen(row, on) {
  var pk = row.querySelector('.emopick'), find = row.querySelector('.emofind');
  pk.hidden = !on; find.setAttribute('aria-expanded', String(on));
  if (!on) return;
  loadEmoji().then(function (d) { emoDraw(row, d, find.value); });
}
function emoDraw(row, d, q) {
  q = q.trim().toLowerCase();
  var grid = row.querySelector('.emogrid'), html = '', last = -1;
  d.emoji.forEach(function (x) {
    if (q && x[1].indexOf(q) < 0) return;
    if (!q && x[2] !== last) { html += '<div class="emogroup">' + esc(d.groups[x[2]]) + '</div>'; last = x[2]; }
    html += x[3] ? '<button type="button" class="ghost emo newemo" title="' + esc(x[1] + ' · ' + RD.t.olderWindows) + '" role="option">' + esc(x[0]) + '</button>'
                 : '<button type="button" class="ghost emo" title="' + esc(x[1]) + '" role="option">' + esc(x[0]) + '</button>';
  });
  grid.innerHTML = html || '<p class="mnote">' + esc(RD.t.noEmoji) + '</p>';
}
actBox.addEventListener('input', function (e) {
  if (e.target.matches('.aval.emoji')) { emoWarn(e.target.closest('.act')); return; }
  if (!e.target.matches('.emofind')) return;
  var row = e.target.closest('.act');
  if (row.querySelector('.emopick').hidden) emoOpen(row, true);
  else emojiData.then(function (d) { emoDraw(row, d, e.target.value); });
});
actBox.addEventListener('keydown', function (e) {
  if (e.key === 'Escape' && e.target.matches('.emofind') && !e.target.closest('.act').querySelector('.emopick').hidden) {
    e.preventDefault(); e.stopPropagation(); e.target.value = ''; emoOpen(e.target.closest('.act'), false);
  }
});
actBox.addEventListener('change', function (e) {
  var row = e.target.closest('.act');
  if (!row) return;
  if (e.target.matches('.atype')) { row.replaceWith(actRow({ type: e.target.value })); drawActs(); }
  else if (e.target.matches('.atpl, .ato')) { var a = readAct(row); if (e.target.matches('.atpl') && !e.target.value) a.title = ''; row.replaceWith(actRow(a)); drawActs(); }
});
// Apply to: ticks in a drop-down. "All calendars" and single calendars exclude each other.
// (The menu is drawn again when calendars are added, renamed or removed, so it's always looked up.)
var applyBox = ruleForm.querySelector('.rdapply'), applyBtn = applyBox.querySelector('.ddbtn');
function applyMenuEl() { return applyBox.querySelector('.ddmenu'); }
function applyChosen() {
  return Array.prototype.filter.call(applyMenuEl().querySelectorAll('input'), function (i) { return i.checked; }).map(function (i) { return i.value; });
}
function drawApply() {
  var chosen = applyMenuEl().querySelectorAll('input:checked'), sum = applyBtn.querySelector('.ddsum');
  sum.innerHTML = chosen.length ? Array.prototype.map.call(chosen, function (i) {
    var o = i.closest('.ddopt'); return o.querySelector('.ddsw').outerHTML + '<span>' + esc(o.querySelector('.ddname').textContent) + '</span>'; }).join('<span class="mnote">,</span>')
    : '<span class="mnote">' + esc(RD.t.noCalendar) + '</span>';
}
function setApply(apply) {
  applyMenuEl().querySelectorAll('input').forEach(function (i) { i.checked = apply === 'all' ? i.value === 'all' : apply.indexOf(i.value) >= 0; });
  drawApply(); openApply(false);
}
function openApply(on) { applyMenuEl().hidden = !on; applyBtn.setAttribute('aria-expanded', String(on)); }
applyBtn.addEventListener('click', function () { openApply(applyMenuEl().hidden); });
applyBox.addEventListener('change', function (e) {
  var menu = applyMenuEl();
  if (e.target.value === 'all' && e.target.checked) menu.querySelectorAll('input:not([value="all"])').forEach(function (i) { i.checked = false; });
  else if (e.target.checked) menu.querySelector('input[value="all"]').checked = false;
  drawApply();
});
ruleDialog.addEventListener('click', function (e) { if (!applyMenuEl().hidden && !applyBox.contains(e.target)) openApply(false); });
ruleDialog.addEventListener('keydown', function (e) {   // Escape closes the menu first, then the dialog
  if (e.key === 'Escape' && !applyMenuEl().hidden) { e.preventDefault(); openApply(false); applyBtn.focus(); }
});
function openRule(rule, sid) {
  editing = rule;
  var title = document.getElementById('rdtitle');
  title.textContent = rule ? title.dataset.edit : title.dataset.new;
  ruleForm.querySelector('.rdname').value = rule ? rule.title : '';
  condBox.innerHTML = ''; actBox.innerHTML = ''; rxBlock();
  (rule && rule.conds.length ? rule.conds : [null]).forEach(function (c) { condBox.appendChild(condRow(c)); });
  (rule ? rule.actions : [null]).forEach(function (a) { actBox.appendChild(actRow(a)); });
  // A new rule made in a calendar applies to that calendar; one made in All Rules to every calendar (F4.1)
  setApply(rule ? rule.apply : (sid ? [sid] : 'all'));
  ruleForm.querySelector('.rdremove').hidden = !rule;
  ruleForm.querySelector('.rdmsg').hidden = true;
  pairState(ruleForm.querySelector('.pairbtns'), 'idle');
  drawConds(); drawActs();
  ruleDialog.showModal();
}
// Apply: the rule as JSON in the form's "rule" field (the page's saving script sends it)
ruleForm.addEventListener('submit', function (e) {
  var msg = ruleForm.querySelector('.rdmsg');
  var conds = Array.prototype.map.call(condBox.querySelectorAll('.cond'), readCond).filter(function (c, i, all) {
    return all.length > 1 || (c.type === 'text' || c.type === 'any' ? c.value.trim() : true); });
  if (ruleForm.classList.contains('unbalanced')) { e.preventDefault(); msg.hidden = false; msg.textContent = {{ _('The brackets don’t pair up: every ( needs a ) after it.')|string|tojson }}; return; }
  var sel = applyChosen();
  var rule = { id: editing ? editing.id : '', title: ruleForm.querySelector('.rdname').value, conds: conds,
               actions: Array.prototype.map.call(actBox.querySelectorAll('.act'), readAct),
               apply: sel.indexOf('all') >= 0 ? 'all' : sel };
  ruleForm.elements.rule.value = JSON.stringify(rule);
  msg.hidden = true;
});
ruleForm.querySelector('.rdremove').addEventListener('click', function () {
  if (!editing) return;
  confirmed({{ _('Delete this rule? It’s removed from every calendar that uses it.')|string|tojson }}).then(function (y) {
    if (!y) return;
    var body = new URLSearchParams({ csrf: CSRF, id: editing.id });
    fetch('/rules/delete', { method: 'POST', body: body, credentials: 'same-origin', headers: { 'X-CS-Async': '1' } })
      .then(function () { ruleDialog.close(); return swapIn(location.href, ['#sources', '#rules', '#cal', '#activity', '#ruledata']); })
      .then(function () { RD = JSON.parse(document.getElementById('ruledata').textContent); initCal(); bindAll(); reopenEvents(); });
  });
});
// A new rule made for an event (Link › Rule › Create new, 0.2.8-beta.15): Title is <its title> and Date is <its day>
function openRuleFor(title, day, sid) {
  openRule(null, sid);
  condBox.innerHTML = '';
  condBox.appendChild(condRow({ type: 'text', op: 'is', value: title, case: false, open: 0, close: 0, join: 'and' }));
  condBox.appendChild(condRow({ type: 'date', op: 'is', value: day, value2: '', open: 0, close: 0, join: 'and' }));
  drawConds();
}
// After "Copy" in All Rules (?rule=<the copy>): the copy opens in the rule dialog to be changed; from an
// event's own page (Link › Rule), its rule (?rule=) or a new one for it (?newrule=1&title=&date=&sid=).
(function () {
  var q = new URLSearchParams(location.search), id = q.get('rule');
  if (id && RD.rules[id]) openRule(RD.rules[id]);
  else if (q.get('newrule')) openRuleFor(q.get('title') || '', q.get('date') || '', q.get('sid') || '');
})();

