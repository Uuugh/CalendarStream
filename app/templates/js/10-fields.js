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

