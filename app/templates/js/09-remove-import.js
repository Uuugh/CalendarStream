// Remove a calendar (0.2.8-beta.15): Merge its events into another calendar (not itself; a new CalendarStream
// one is always offered) or Delete them; "Download a copy (.ics) first"; with a Merge and rules of its
// own, whether they move with them. The last CalendarStream calendar says Empty: it stays.
document.addEventListener('click', function (e) {
  var b = e.target.closest('.removecal');
  if (!b) return;
  var dlg = document.getElementById('removedialog'), f = dlg.querySelector('form'), into = f.querySelector('.rminto'), empty = !!b.dataset.empty;
  f.elements.sid.value = b.dataset.sid; f.dataset.name = b.dataset.name; f.dataset.rules = b.dataset.rules || '0';
  ['#rmtitle', '.rmnote'].forEach(function (sel) { var el = dlg.querySelector(sel); el.textContent = (empty ? el.dataset.empty : el.dataset.text).replace('{name}', b.dataset.name); });
  var go = dlg.querySelector('.rmgo span'); go.textContent = empty ? go.parentNode.dataset.empty : go.parentNode.dataset.text;
  Array.prototype.forEach.call(into.options, function (o) { o.hidden = o.disabled = o.value === b.dataset.sid; });
  into.value = Array.prototype.find.call(into.options, function (o) { return !o.disabled; }).value;
  f.querySelector('input[name=keep][value=merge]').checked = true;
  f.querySelector('input[name=rules][value=move]').checked = true;
  rmRules(f);
  dlg.showModal();
});
function rmRules(f) {      // "Its N rules: Move to <calendar> | Delete them", only with a Merge and rules of its own
  var n = +f.dataset.rules, merge = f.querySelector('input[name=keep][value=merge]').checked, box = f.querySelector('.rmrules'), into = f.querySelector('.rminto');
  box.hidden = !(merge && n > 0);
  var lbl = box.querySelector('.rmrulesn'); lbl.textContent = n === 1 ? lbl.dataset.one : lbl.dataset.many.replace('{n}', n);
  box.querySelector('.rmtarget').textContent = into.options[into.selectedIndex].text;
}
document.querySelectorAll('dialog [data-close]').forEach(function (b) { b.addEventListener('click', function () { b.closest('dialog').close(); }); });
document.getElementById('removeform').addEventListener('change', function (e) {
  if (e.target.matches('.rminto')) e.target.closest('.rmopt').querySelector('input[type=radio]').checked = true;
  rmRules(e.target.form);
});
document.getElementById('removeform').addEventListener('submit', function (e) {
  var f = e.target;
  if (f.querySelector('.rmdownload').checked) {      // the copy is downloaded before anything changes
    var a = document.createElement('a'); a.href = '/sources/export?sid=' + encodeURIComponent(f.elements.sid.value); a.download = '';
    document.body.appendChild(a); a.click(); a.remove();
  }
  setTimeout(function () { document.getElementById('removedialog').close(); }, 50);
});
// Import .ics (0.2.8-beta.15): the file is read, then each of its events already in the calendar is asked
// about one at a time (Merge | Delete, "Do this for all remaining"), then the rest is added.
document.addEventListener('submit', function (e) {
  var f = e.target;
  if (!f.matches || !f.matches('form.importrow:not(.uploadform)')) return;
  e.preventDefault();
  var btn = f.querySelector('button:not([type=button])'), data = new FormData(f);
  btn.disabled = true;
  fetch('/sources/import', { method: 'POST', body: data, credentials: 'same-origin', headers: { 'X-CS-Async': '1' } })
    .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw new Error(j.detail || ('HTTP ' + r.status)); return j; }); })
    .then(function (j) {
      var choices = {}, all = null;
      return j.conflicts.reduce(function (p, c, i) {
        return p.then(function () {
          if (all) { choices[c.key] = all; return; }
          return askConflict(c, i + 1, j.conflicts.length).then(function (res) { choices[c.key] = res.choice; if (res.all) all = res.choice; });
        });
      }, Promise.resolve()).then(function () {
        var body = new URLSearchParams({ csrf: CSRF, token: j.token, choices: JSON.stringify(choices) });
        return fetch('/sources/import/finish', { method: 'POST', body: body, credentials: 'same-origin', headers: { 'X-CS-Async': '1' } });
      });
    })
    .then(function (r) { if (!r.ok) return r.json().then(function (j) { throw new Error(j.detail); }); f.reset(); return swapIn(location.href, ['#sources', '#cal', '#activity']); })
    .then(function () { initCal(); bindAll(); reopenEvents(); })
    .catch(function (err) { tell(err.message); })
    .then(function () { btn.disabled = false; });
});
function askConflict(c, n, total) {
  var d = document.getElementById('conflictdialog');
  d.querySelector('.cfcount').textContent = T.alreadyHere.replace('{n}', n).replace('{total}', total);
  d.querySelector('.cfthere').textContent = c.there.title + ' · ' + c.there.when;
  d.querySelector('.cffile').textContent = c.file.title + ' · ' + c.file.when;
  var rest = d.querySelector('.cfall'); rest.checked = false;
  rest.closest('label').hidden = n === total;
  rest.closest('label').querySelector('.cfleft').textContent = total - n;
  return new Promise(function (ok) {
    d.querySelector('.cfmerge').onclick = function () { ok({ choice: 'merge', all: rest.checked }); d.close(); };
    d.querySelector('.cfdelete').onclick = function () { ok({ choice: 'delete', all: rest.checked }); d.close(); };
    d.onclose = function () { ok({ choice: 'delete', all: true }); };   // closed: the rest of the file's copies are dropped
    d.showModal();
  });
}
