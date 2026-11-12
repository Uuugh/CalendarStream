// History's filter (0.2.8-beta.15): a Type, some words, a time; rows that don't fit are hidden
document.addEventListener('input', histFilter);
document.addEventListener('change', histFilter);
function histFilter(e) {
  if (!e.target.closest || !e.target.closest('.histfilter')) return;
  var box = e.target.closest('#activity'), kind = box.querySelector('.hfkind').value, words = box.querySelector('.hfwords').value.trim().toLowerCase(),
      hours = +box.querySelector('.hftime').value, since = hours ? Date.now() / 1000 - hours * 3600 : 0;
  box.querySelectorAll('.logwin tbody tr').forEach(function (tr) {
    tr.hidden = (kind && tr.dataset.kind !== kind) || (words && tr.textContent.toLowerCase().indexOf(words) < 0) || (since && +tr.dataset.at < since);
  });
}
// Copy the container log (0.2.8-beta.42, troubleshooting): fetches the same text the Container log link
// opens, and puts it straight on the clipboard, so copying it all for a bug report needs no new tab and no
// manual select-all.
document.addEventListener('click', function (e) {
  var btn = e.target.closest && e.target.closest('#copycontainerlog');
  if (!btn) return;
  fetch('/history/container', { credentials: 'same-origin' }).then(function (r) { return r.text(); })
    .then(function (text) { copyText(text, btn); })
    .catch(function () { tell(T.prefFailed); });
});
// A file field shows the chosen file's name in its box
document.addEventListener('change', function (e) {
  if (!e.target.matches || !e.target.matches('.filefield input[type=file]')) return;
  var span = e.target.parentNode.querySelector('.filename');
  span.textContent = e.target.files.length ? e.target.files[0].name : span.dataset.none;
  span.classList.toggle('chosen', e.target.files.length > 0);
});
// A date range's All (0.2.8-beta.15): ticked, the dates are cleared and off (every date); unticked, they're open
document.addEventListener('change', function (e) {
  if (!e.target.matches || !e.target.matches('.daterange .rangeall')) return;
  e.target.closest('.daterange').querySelectorAll('input[type=date]').forEach(function (i) { if (e.target.checked) i.value = ''; i.readOnly = e.target.checked; i.classList.toggle('off', e.target.checked); });
  if (e.target.form) e.target.form.dispatchEvent(new Event('input', { bubbles: true }));     // (a watched form: Save shows)
});
document.addEventListener('input', function (e) {     // a date typed in: All goes off
  if (!e.target.matches || !e.target.matches('.daterange input[type=date]')) return;
  var all = e.target.closest('.daterange').querySelector('.rangeall'); if (all && e.target.value) all.checked = false;
});
// The pop-up's title is the page's own heading (Add event, Edit event…), which the page hides when embedded
eventFrame.addEventListener('load', function () {
  var h = null;
  try { h = eventFrame.contentDocument && eventFrame.contentDocument.querySelector('h1'); } catch (err) { /* not this site's page */ }
  eventDialog.querySelector('.dlghead .title').textContent = h ? h.textContent : eventFrame.dataset.title;
});

// Pop-ups: ← (and Escape) closes them; on a phone they fill the screen.
document.querySelectorAll('dialog.popup .dlgback').forEach(function (b) {
  b.addEventListener('click', function () { b.closest('dialog').close(); });
});

// History's headers slide (drag) to reorder, or focus one and press ← → (0.2.8-beta.32, F44).
// #activity is swapped in whole on undo/redo, so every listener here is delegated at document level.
function histColOrder(table) { return Array.from(table.querySelectorAll('thead .histcol')).map(function (th) { return th.dataset.col; }); }
function moveHistCol(table, fromCol, toCol) {
  if (fromCol === toCol) return;
  var headRow = table.querySelector('thead tr'), ths = Array.from(headRow.children);
  var fromTh = ths.filter(function (th) { return th.dataset.col === fromCol; })[0], toTh = ths.filter(function (th) { return th.dataset.col === toCol; })[0];
  if (!fromTh || !toTh) return;
  var forward = ths.indexOf(fromTh) < ths.indexOf(toTh);
  if (forward) toTh.after(fromTh); else toTh.before(fromTh);
  table.querySelectorAll('tbody tr').forEach(function (tr) {
    var tds = Array.from(tr.children);
    var fromTd = tds.filter(function (td) { return td.dataset.col === fromCol; })[0], toTd = tds.filter(function (td) { return td.dataset.col === toCol; })[0];
    if (!fromTd || !toTd) return;
    if (forward) toTd.after(fromTd); else toTd.before(fromTd);
  });
  savePref('/ui/history', { order: histColOrder(table).join(',') });
}
var histDragCol = null;
document.addEventListener('dragstart', function (e) {
  var th = e.target.closest && e.target.closest('.histcol'); if (!th) return;
  histDragCol = th.dataset.col;
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', histDragCol);
});
document.addEventListener('dragover', function (e) {
  var th = e.target.closest && e.target.closest('.histcol'); if (!th || !histDragCol) return;
  e.preventDefault();
  th.classList.add('dragover');
});
document.addEventListener('dragleave', function (e) {
  var th = e.target.closest && e.target.closest('.histcol'); if (th) th.classList.remove('dragover');
});
document.addEventListener('drop', function (e) {
  var th = e.target.closest && e.target.closest('.histcol'); if (!th || !histDragCol) return;
  e.preventDefault();
  th.classList.remove('dragover');
  moveHistCol(th.closest('table'), histDragCol, th.dataset.col);
  histDragCol = null;
});
document.addEventListener('dragend', function () {
  document.querySelectorAll('.histcol.dragover').forEach(function (th) { th.classList.remove('dragover'); });
  histDragCol = null;
});
document.addEventListener('keydown', function (e) {
  var th = e.target.closest && e.target.closest('.histcol'); if (!th) return;
  if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
  var table = th.closest('table'), ths = Array.from(table.querySelectorAll('thead .histcol'));
  var i = ths.indexOf(th), j = e.key === 'ArrowLeft' ? i - 1 : i + 1;
  if (j < 0 || j >= ths.length) return;
  e.preventDefault();
  moveHistCol(table, th.dataset.col, ths[j].dataset.col);
  th.focus();
});

