// Rule and template rows: only saved rows are listed. + (on the last row, or in the box's corner
// when there are none) adds an empty row; the bin removes one. Save shows once there's something to save.
function bindTags() { each('form.tagsform', 'tags', function (form) {
  var rows = form.querySelector('.tagrows'), tpl = form.querySelector('template.rowtpl'),
      first = form.closest('.box, .subbox, .card').querySelector('.addfirst'), foot = form.querySelector('.tagfoot');
  function refresh(changed) {
    if (first && !first.classList.contains('plus')) first.hidden = rows.children.length > 0;   // a section's + always shows
    var empty = form.closest('.card').querySelector(':scope > .empty');
    if (empty && rows.children.length) empty.hidden = true;
    if (foot && (changed || rows.children.length)) foot.hidden = false;
  }
  function addRow() {
    var row = tpl.content.firstElementChild.cloneNode(true);
    rows.appendChild(row); refresh(true);
    row.querySelector('input[type=text]').focus();
  }
  if (first) first.addEventListener('click', addRow);
  rows.addEventListener('click', function (e) {
    var row = e.target.closest('.tagrow');
    if (!row) return;
    if (e.target.closest('.addtag')) {
      addRow();
    } else if (e.target.closest('.casebtn')) {
      var on = row.querySelector('input[name=tag_case]').value !== '1';
      row.querySelector('input[name=tag_case]').value = on ? '1' : '';
      e.target.closest('.casebtn').setAttribute('aria-pressed', String(on));
    } else if (e.target.closest('.deltag')) {
      row.remove(); refresh(true);
    }
  });
  // A rule's action shows its own fields; an all-day template has no length.
  rows.addEventListener('change', function (e) {
    var row = e.target.closest('.tagrow');
    if (e.target.matches('.ruleaction')) row.dataset.action = e.target.value;
    if (e.target.matches('.tplkind')) row.dataset.kind = e.target.value;
  });
}); }
bindTags();

// + in the corner of Calendar Sources / Calendar Destinations opens its menu.
function bindAdd() { each('.addwrap', 'add', function (w) {
  var btn = w.querySelector('.plus, .addrule'), pop = w.querySelector('dialog.addpop');
  if (pop) {      // (0.2.8-beta.15) a centred pop-up, the page dimmed behind it
    btn.addEventListener('click', function () {
      pop.showModal(); btn.setAttribute('aria-expanded', 'true');
      var f = pop.querySelector('input:not([type=hidden]):not([hidden])'); if (f) f.focus();
    });
    pop.addEventListener('close', function () { btn.setAttribute('aria-expanded', 'false'); });
    pop.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', function () { pop.close(); }); });
    return;
  }
  var menu = w.querySelector('.addmenu');
  function set(open) { menu.hidden = !open; btn.setAttribute('aria-expanded', String(open)); }
  btn.addEventListener('click', function (e) {
    e.stopPropagation(); set(menu.hidden);
    if (!menu.hidden) { var f = menu.querySelector('input:not([type=hidden])'); if (f) f.focus(); }
  });
  document.addEventListener('click', function (e) { if (!menu.hidden && !w.contains(e.target)) set(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
}); }
bindAdd();

// Removing a source, destination or event asks first.
// A + that opens a pop-up of its own (0.2.8-beta.15: Event Templates); [data-close] inside closes it
document.addEventListener('click', function (e) {
  var b = e.target.closest && e.target.closest('.opendlg');
  if (b) { var d = document.getElementById(b.dataset.dialog); d.showModal(); var i = d.querySelector('input[type=text]'); if (i) i.focus(); return; }
  var c = e.target.closest && e.target.closest('dialog.addpop [data-close]');
  if (c) c.closest('dialog').close();
});
// A Google module's Remove (0.2.8-beta.15): three answers, one under the other
function bindGRemove() { each('form.gremovemod', 'gremove', function (f) {
  f.addEventListener('submit', function (e) {
    if (f.dataset.confirmed) { delete f.dataset.confirmed; return; }
    e.preventDefault(); e.stopImmediatePropagation();
    ask(f.dataset.ask, [{ label: f.dataset.yesdel, value: '1', cls: 'danger solid' }, { label: f.dataset.yeskeep, value: '0', cls: 'ghost danger' },
                        { label: f.dataset.no, value: null, cls: 'ghost' }], true).then(function (v) {
      if (v === null) return;
      f.elements.delete.value = v === '1' ? '1' : ''; f.dataset.confirmed = '1'; f.requestSubmit();
    });
  });
}); }
bindGRemove();
function bindConfirm() { bindGRemove(); each('form[data-confirm]', 'confirm', function (f) {
  guard(f, function () { return f.dataset.confirm; });     // (read when sent: an event's text changes with the event)
}); }
bindConfirm();

// "This page" buttons fill their box with the address this page is open at.
each('[data-fill]', 'fill', function (b) {
  b.addEventListener('click', function () { document.getElementById(b.dataset.fill).value = location.origin; });
});

// Saving without reloading the page (F1.5): a form with data-swap is sent in the background, and only
// the parts of the page it names ("#src-ccs|#cal|#activity") are swapped in from the page that comes
// back; everything else (what's being typed elsewhere, open boxes, the scroll) stays as it is.
function bindAll() {
  RD = JSON.parse(document.getElementById('ruledata').textContent);     // the rules, as now saved
  bindWatch(); bindFiles(); bindCfg(); bindSrc(); bindPresets(); bindTags(); bindAdd(); bindConfirm(); bindGuide();
  each('[data-fill]', 'fill', function (b) { b.addEventListener('click', function () { document.getElementById(b.dataset.fill).value = location.origin; }); });
  each('.disconnectform', 'disconnect', function (f) { guard(f, T.disconnect); });
  initSections();
  if (window.fitHeads) fitHeads();
  followRunning();
}
function swapFrom(html, selectors) {
  var doc = new DOMParser().parseFromString(html, 'text/html');
  selectors.forEach(function (sel) {
    var fresh = doc.querySelectorAll(sel);
    document.querySelectorAll(sel).forEach(function (el, i) { if (fresh[i]) el.replaceWith(fresh[i]); });
  });
  if (selectors.indexOf('#cal') >= 0) initCal();
  bindAll();
}
function sendSwap(f, body) {
  var sels = (f.dataset.swap || '').split('|').filter(Boolean);
  return fetch(f.getAttribute('action'), { method: 'POST', body: body, credentials: 'same-origin', headers: { 'X-CS-Async': '1' } })
    .then(function (r) {
      if (!r.ok) return r.json().catch(function () { return {}; }).then(function (j) { var er = new Error(j.detail || ('HTTP ' + r.status)); er.status = r.status; er.fields = r.headers.get('X-CS-Fields') || ''; throw er; });
      var json = (r.headers.get('content-type') || '').indexOf('json') >= 0;
      // a JSON answer (the rule dialog's): the page is fetched for the swap
      return (json ? fetch(location.pathname + location.search, { cache: 'no-store', credentials: 'same-origin' }) : Promise.resolve(r))
        .then(function (page) { var url = page.url; return page.text().then(function (html) { return { html: html, url: url }; }); });
    })
    .then(function (res) { swapFrom(res.html, sels); return res; });
}
// Settings → Check now (0.2.8-beta.8) works like Sync Now: Checking… (at least 0.7 s, so it's seen), then
// Up to date (a green pulse), Update found (yellow) or Couldn't check (yellow) for 2.4 s; then it shrinks
// back and Updates (and the version at the top) are redrawn with what the check found.
function checkNow(f, btn, body) {
  if (btn.dataset.state !== 'idle') return;
  var started = Date.now(), sb = btn.closest('.statusbox');
  btn.dataset.state = 'syncing'; btn.disabled = true;
  function finish(state, html) {
    setTimeout(function () {
      btn.dataset.state = state;
      setTimeout(function () {
        btn.dataset.state = 'idle';
        setTimeout(function () { if (html) swapFrom(html, ['#updates', '.topbar .ver']); else btn.disabled = false; }, 300);
      }, 2400);
    }, Math.max(0, 700 - (Date.now() - started)));
  }
  fetch(f.getAttribute('action'), { method: 'POST', body: body, credentials: 'same-origin', headers: { 'X-CS-Async': '1' } })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
    .then(function (html) {
      var fresh = new DOMParser().parseFromString(html, 'text/html').getElementById('updates');
      if (!fresh) throw new Error('no answer');
      finish(fresh.querySelector('.check.bad') ? 'fail' : fresh.querySelector('.upgradebtn') ? 'found' : 'done', html);
    }, function () { finish('fail', null); });
  if (sb) sb.title = '';
}
// The Cancel | Save pair: the pressed side fills it and says what happened, for 3 seconds.
function pairState(p, st) {
  if (!p) return;
  var sv = p.querySelector('.psave'), c = p.querySelector('.pcancel');
  p.dataset.state = st;
  sv.textContent = { saving: sv.dataset.busy, saved: sv.dataset.done, failed: T.failed }[st] || sv.dataset.text;
  if (st === 'failed') sv.insertAdjacentHTML('afterbegin', p.dataset.cause === 'inside' ? ICON.fail : ICON.warn);
  c.textContent = st === 'cancelled' ? c.dataset.done : c.dataset.text;
}
function flashPair(p, st, then) {
  pairState(p, st);
  setTimeout(function () { if (p.dataset.state === st) pairState(p, 'idle'); if (then) then(); }, 3000);
}
// (A form's own id is read with getAttribute: the rule form has a field named "id", which hides f.id.)
function formId(f) { return f.getAttribute('id') || ''; }
function pairFor(f) { return formId(f) ? document.querySelector('.pairbtns[data-pair="' + formId(f) + '"]') : null; }
document.addEventListener('submit', function (e) {
  var f = e.target;
  if (e.defaultPrevented || !f.matches || !f.matches('form[data-swap]')) return;
  var btn = e.submitter;
  if (btn && btn.name === 'then' && btn.value === 'connect') return;     // Connect me goes on to Google's sign-in
  e.preventDefault();
  var body = new FormData(f), pair = pairFor(f);
  clearFix(f);
  if (btn && btn.name) body.append(btn.name, btn.value);
  if (btn && btn.classList.contains('checknow')) { checkNow(f, btn, body); return; }
  if (pair) pairState(pair, 'saving');
  var old = f.parentNode && f.parentNode.querySelector('.pairfail:not(.rdmsg)'); if (old) old.remove();   // (the rule dialog keeps its own)
  sendSwap(f, body).then(function (res) {
    var p2 = pairFor(f) || pair;                      // the pair may have been swapped for a new one
    if (p2) flashPair(p2, 'saved');
    if (formId(f) === 'ruleform') setTimeout(function () { ruleDialog.close(); }, 900);
    var dl = f.closest('dialog.addpop'); if (dl) setTimeout(function () { dl.close(); f.reset(); }, 900);    // a + pop-up closes once saved
    var copy = new URL(res.url, location.href).searchParams.get('rule');     // after Copy in All Rules
    if (copy && RD.rules[copy]) openRule(RD.rules[copy]);
  }, function (err) {
    // amber when what was typed was refused (4xx: waiting on you); red when CalendarStream itself failed
    var inside = !err.status || err.status >= 500;
    if (err.fields) markFix(f, err.fields);
    if (pair) {
      if (inside) pair.dataset.cause = 'inside'; else delete pair.dataset.cause;
      pairState(pair, 'failed');
      var note = document.createElement('p'); note.className = 'pairfail' + (inside ? ' inside' : ''); note.innerHTML = (inside ? ICON.fail : ICON.warn) + esc(err.message);
      pair.parentNode.appendChild(note);
      setTimeout(function () { if (pair.dataset.state === 'failed') pairState(pair, 'idle'); }, 4000);
    } else tell(err.message);
  });
});
document.addEventListener('click', function (e) {
  var c = e.target.closest('.pairbtns .pcancel');
  if (!c) return;
  var p = c.closest('.pairbtns'), f = document.getElementById(p.dataset.pair);
  if (f) { f.reset(); f.dispatchEvent(new CustomEvent('paircancel')); }
  var old = p.parentNode.querySelector('.pairfail:not(.rdmsg)'); if (old) old.remove();
  if (f && formId(f) === 'ruleform') { pairState(p, 'cancelled'); setTimeout(function () { ruleDialog.close(); }, 700); return; }
  var dl = c.closest('dialog.addpop'); if (dl && !dl.querySelector('.addbody, .addmenu')) { pairState(p, 'cancelled'); setTimeout(function () { dl.close(); }, 700); return; }
  flashPair(p, 'cancelled');
  // In + Add a calendar (0.2.8-beta.9), Cancel closes the menu once it has shown "Cancelled"
  var pop = c.closest('dialog.addpop');
  if (pop) setTimeout(function () { pop.close(); }, 700);
  // Cancel also folds the module (F1.1), once it has shown "Cancelled"
  var box = c.closest('.box.cfgbox');
  if (box) setTimeout(function () { setModule(box, false); }, 700);
});

