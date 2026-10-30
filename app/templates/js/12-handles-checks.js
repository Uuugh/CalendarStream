// Handles (F1.2): ▲ / ▼ move a calendar, feed or rule one place; the bars drag it. The new order is
// saved at once: the page sends the neighbour it now sits above (or below).
(function () {
  var MOVE = { source: ['/sources/move', 'sid'], dest: ['/destinations/move', 'did'], rule: ['/rules/move', 'id'] };
  function rowOf(el) { return el.closest('.modrow, .ruleline'); }
  function rows(list) { return Array.prototype.filter.call(list.children, function (c) { return c.matches('.modrow:not(.fixed), .ruleline'); }); }
  function save(row) {
    var list = row.parentNode, kind = list.dataset.kind, all = rows(list), i = all.indexOf(row),
        id = row.dataset.id || row.dataset.ruleId, nb = all[i + 1], pv = all[i - 1];
    var body = new URLSearchParams({ csrf: CSRF }), m = MOVE[kind];
    body.set(m[1], id);
    if (nb) body.set('before', nb.dataset.id || nb.dataset.ruleId); else if (pv) body.set('after', pv.dataset.id || pv.dataset.ruleId);
    fetch(m[0], { method: 'POST', body: body, credentials: 'same-origin', headers: { 'X-CS-Async': '1' } }).then(function (r) {
      if (!r.ok) return;
      // the other lists that show the same rules (All Rules, the calendars) and the calendar follow
      var sel = kind === 'rule' ? ['#rules .rulelist', '#ruleconflicts', '#rulecount', '.box.src .srcrules', '#cal'] : kind === 'source' ? ['#sources', '#cal'] : [];
      if (sel.length) swapIn(location.href, sel).then(function () { initCal(); bindAll(); reopenEvents(); });
    });
  }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.handle .hmove');
    if (!b) return;
    var row = rowOf(b), all = rows(row.parentNode), i = all.indexOf(row);
    if (b.dataset.dir === 'up' && i > 0) row.parentNode.insertBefore(row, all[i - 1]);
    else if (b.dataset.dir === 'down' && i < all.length - 1) row.parentNode.insertBefore(row, all[i + 1].nextSibling);
    else return;
    b.focus(); save(row);
  });
  var dragging = null;
  document.addEventListener('dragstart', function (e) {
    var grip = e.target.closest && e.target.closest('.hgrip');
    if (!grip) return;
    dragging = rowOf(grip); dragging.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    try { e.dataTransfer.setData('text/plain', ''); e.dataTransfer.setDragImage(dragging, 20, 20); } catch (err) {}
  });
  document.addEventListener('dragover', function (e) {
    if (!dragging) return;
    var over = e.target.closest && rowOf(e.target);
    if (!over || over === dragging || over.parentNode !== dragging.parentNode || over.matches('.fixed')) return;
    e.preventDefault();
    var r = over.getBoundingClientRect(), below = e.clientY > r.top + r.height / 2;
    over.parentNode.insertBefore(dragging, below ? over.nextSibling : over);
  });
  document.addEventListener('drop', function (e) { if (dragging) e.preventDefault(); });
  document.addEventListener('dragend', function () {
    if (!dragging) return;
    var row = dragging; dragging = null; row.classList.remove('dragging'); save(row);
  });
})();

// Save checks (0.2.8-beta.17, F8): a refused Save names its fields (X-CS-Fields); they're outlined in amber
// until changed. "url2" is the third field named url.
function fieldsOf(f, name) {
  var m = /^(.*?)(\d+)$/.exec(name), all = Array.prototype.filter.call(f.elements, function (x) { return x.name === (m ? m[1] : name); });
  return m ? (all[+m[2]] ? [all[+m[2]]] : []) : all;
}
function markFix(f, names) {
  var first = null;
  names.split(',').filter(Boolean).forEach(function (n) {
    fieldsOf(f, n).forEach(function (x) { x.classList.add('needsfix'); x.setAttribute('aria-invalid', 'true'); first = first || x; });
  });
  if (first) first.focus();
}
function clearFix(f) {
  Array.prototype.forEach.call(f.elements, function (x) { x.classList.remove('needsfix'); x.removeAttribute('aria-invalid'); });
}
document.addEventListener('input', function (e) {
  if (e.target.classList && e.target.classList.contains('needsfix')) { e.target.classList.remove('needsfix'); e.target.removeAttribute('aria-invalid'); }
});

// Copy a text (not a field's): the Clipboard API, or a hidden box and execCommand on plain-HTTP pages.
function copyText(text, btn) {
  var icon = btn.innerHTML;
  function done(msg) { btn.textContent = msg || T.copied; btn.classList.add('done'); setTimeout(function () { btn.innerHTML = icon; btn.classList.remove('done'); }, 1800); }
  function fallback() {
    var ta = document.createElement('textarea'); ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
    document.body.appendChild(ta); ta.select(); var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    ta.remove(); done(ok ? T.copied : T.pressCtrlC);
  }
  if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(function () { done(); }, fallback);
  else fallback();
}

