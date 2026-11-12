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
  var btn = w.querySelector('.addreuse') || w.querySelector('.plus, .addrule'), pop = w.querySelector('dialog.addpop');
  if (pop) {      // (0.2.8-beta.15) a centred pop-up, the page dimmed behind it
    btn.addEventListener('click', function () {
      pop.showModal(); btn.setAttribute('aria-expanded', 'true');
      var f = pop.querySelector('input:not([type=hidden]):not([hidden])'); if (f) f.focus();
    });
    pop.addEventListener('close', function () { btn.setAttribute('aria-expanded', 'false'); });
    pop.querySelectorAll('[data-close]').forEach(function (b) { b.addEventListener('click', function () { pop.close(); }); });
    return;
  }
  var menu = w.querySelector('.addmenu'); if (!menu || btn.classList.contains('newrule')) return;
  function set(open) { menu.hidden = !open; btn.setAttribute('aria-expanded', String(open)); }
  btn.addEventListener('click', function (e) {
    e.stopPropagation(); set(menu.hidden);
    if (!menu.hidden) { var f = menu.querySelector('input:not([type=hidden])'); if (f) f.focus(); }
  });
  document.addEventListener('click', function (e) { if (!menu.hidden && !w.contains(e.target)) set(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
}); }
bindAdd();
// (0.2.8-beta.33, I32) A + pop-up's own submit button, disabled while its fetch is in flight (below), is freed
// again once the pop-up closes - saved, cancelled, or stepped back from - so reopening it to add another
// doesn't find it stuck disabled from a previous add.
function bindAddPopReset() { each('dialog.addpop', 'addpopreset', function (d) {
  d.addEventListener('close', function () { d.querySelectorAll('button[type=submit]:disabled, button:not([type]):disabled').forEach(function (b) { b.disabled = false; }); });
}); }
bindAddPopReset();

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
  bindWatch(); bindFiles(); bindCfg(); bindSrc(); bindPresets(); bindTags(); bindAdd(); bindAddPopReset(); bindConfirm(); bindGuide();
  each('[data-fill]', 'fill', function (b) { b.addEventListener('click', function () { document.getElementById(b.dataset.fill).value = location.origin; }); });
  each('.disconnectform', 'disconnect', function (f) { guard(f, T.disconnect); });
  initSections();
  bindSettingsMenu(); bindSettingsForms();
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
  if (selectors.indexOf('#cal') >= 0 && typeof reopenEvents === 'function') reopenEvents();     // (0.2.8-beta.28, I9) events opened in the calendar stay open after a module's Save
}
function sendSwap(f, body) {
  var sels = (f.dataset.swap || '').split('|').filter(Boolean);
  return fetch(f.getAttribute('action'), { method: 'POST', body: body, credentials: 'same-origin', headers: { 'X-CS-Async': '1' } })
    .then(function (r) {
      if (!r.ok) return r.json().catch(function () { return {}; }).then(function (j) { var er = new Error(j.detail || ('HTTP ' + r.status)); er.status = r.status; er.fields = r.headers.get('X-CS-Fields') || ''; throw er; });
      var json = (r.headers.get('content-type') || '').indexOf('json') >= 0;
      if (json) {     // (0.2.8-beta.29, F32) a changed login ends every session: go to the sign-in page
        return r.clone().json().catch(function () { return {}; }).then(function (j) {
          if (j && j.redirect) { location.href = j.redirect; return new Promise(function () {}); }
          return fetch(location.pathname + location.search, { cache: 'no-store', credentials: 'same-origin' })
            .then(function (page) { var url = page.url; return page.text().then(function (html) { return { html: html, url: url }; }); });
        });
      }
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
        setTimeout(function () { if (html) swapFrom(html, ['#updates .module.bare', '#updates .update-error', '.topbar .ver']); else btn.disabled = false; }, 300);
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
  if (p.dataset.state === 'cancelled' && st === 'idle') p.dataset.prev = 'cancelled'; else delete p.dataset.prev;   // (F12.5: Cancel shrinks back as slowly as it grew)
  p.dataset.state = st;
  sv.textContent = { saving: sv.dataset.busy, saved: sv.dataset.done, failed: T.failed }[st] || sv.dataset.text;
  if (st === 'failed') sv.insertAdjacentHTML('afterbegin', p.dataset.cause === 'inside' ? ICON.fail : ICON.warn);
  c.textContent = st === 'cancelled' ? c.dataset.done : c.dataset.text;
  if (st === 'idle') setTimeout(pairRefresh, 0);
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
  if (btn && btn.disabled) return;          // (0.2.8-beta.33, I32) already sending: a second click/Enter is ignored,
                                             // not a second destination (and a second invite) made from it
  e.preventDefault();
  var body = new FormData(f), pair = pairFor(f);
  clearFix(f);
  if (btn && btn.name) body.append(btn.name, btn.value);
  if (btn && btn.classList.contains('checknow')) { checkNow(f, btn, body); return; }
  if (pair) pairState(pair, 'saving');
  else if (btn) btn.disabled = true;         // a pair shows "Saving…" and disables itself; a plain form (+ Add) has no
                                              // pair, so its own submit button is disabled here instead, until it answers
  var old = f.parentNode && f.parentNode.querySelector('.pairfail:not(.rdmsg)'); if (old) old.remove();   // (the rule dialog keeps its own)
  sendSwap(f, body).then(function (res) {
    var p2 = pairFor(f) || pair;                      // the pair may have been swapped for a new one
    if (p2) flashPair(p2, 'saved');
    if (formId(f) === 'ruleform') setTimeout(function () { ruleDialog.close(); }, 900);
    if (f.dataset.reload) setTimeout(function () { location.href = '/?menu=settings'; }, 900);
    var dl = f.closest('dialog.addpop, dialog.settings-popup'); if (dl) setTimeout(function () { dl.close(); f.reset(); }, 900);    // a + pop-up closes once saved
    var copy = new URL(res.url, location.href).searchParams.get('rule');     // after Copy in All Rules
    if (copy && RD.rules[copy]) openRule(RD.rules[copy]);
    // (0.2.8-beta.33, F56) ☰ Settings › Administrator: a changed public address breaks Google Calendar API
    // Sync's redirect URI match; settings.py's redirect carries &fixapi=1 when that just happened. The swap
    // never navigates, so there's no query string to clean up here (unlike PAGE.fixApi's full-page path).
    if (new URL(res.url, location.href).searchParams.get('fixapi') === '1') tell(T.fixApi);
  }, function (err) {
    // amber when what was typed was refused (4xx: waiting on you); red when CalendarStream itself failed
    var inside = !err.status || err.status >= 500;
    if (err.fields) markFix(f, err.fields);
    if (!pair && btn) btn.disabled = false;   // (0.2.8-beta.33, I32) failed: let a plain form's button be tried again
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
  if (f && formId(f) === 'ruleform') {
    pairState(p, 'cancelled');
    // (0.2.8-beta.32, I18) opened from the event pop-up: reopen it as it was, unsaved edits included, instead of
    // just closing (its iframe wasn't wiped: eventSuspend, 08-events.js).
    var backToEvent = ruleFromEvent;
    setTimeout(function () { ruleDialog.close(); if (backToEvent) eventDialog.showModal(); }, 700);
    return;
  }
  var dl = c.closest('dialog.addpop, dialog.settings-popup'); if (dl && !dl.querySelector('.addbody, .addmenu')) { pairState(p, 'cancelled'); setTimeout(function () { dl.close(); }, 700); return; }
  flashPair(p, 'cancelled');
  // In + Add a calendar (0.2.8-beta.9), Cancel closes the menu once it has shown "Cancelled"
  var pop = c.closest('dialog.addpop');
  if (pop) setTimeout(function () { pop.close(); }, 700);
  // Cancel also folds the module (F1.1), once it has shown "Cancelled"
  var box = c.closest('.box.cfgbox');
  if (box) setTimeout(function () { setModule(box, false); }, 700);
});


// (0.2.8-beta.26, F9, F12.4) Cancel | Save while there is nothing to save: truly disabled (greyed, not focusable). The first change
// enables the pair and Save pulses for about 5 seconds, then stays in full color; Save or Cancel brings it back. What the
// form held when it appeared (or was opened, or last saved) is compared with what it holds now. + Add pop-ups keep their
// buttons enabled: a new calendar or feed can be added with the defaults.
var pairBase = new WeakMap();
function pairSig(p) {
  var f = document.getElementById(p.dataset.pair);
  if (!f) return null;
  if (formId(f) === 'ruleform') return typeof ruleSig === 'function' && ruleDialog.open ? ruleSig() : null;
  var s = [];
  new FormData(f).forEach(function (v, k) { if (k !== 'csrf') s.push(k + '=' + (typeof v === 'string' ? v : v.name + ':' + v.size)); });
  return s.join('&');
}
function pairReset(p) { if (p && pairBase) pairBase.delete(p); setTimeout(pairRefresh, 0); }
function pairRefresh() {
  document.querySelectorAll('.pairbtns').forEach(function (p) {
    if (p.dataset.state !== 'idle') return;
    var sv = p.querySelector('.psave'), c = p.querySelector('.pcancel');
    if (!sv || !c || p.closest('dialog.addpop')) return;
    if (p.closest('#ruledialog') && !editing) return;                      // (a new rule: Apply stays available)
    var sig = pairSig(p);
    if (sig === null) return;
    if (!pairBase.has(p)) pairBase.set(p, sig);
    var dirty = sig !== pairBase.get(p), rx = !!(p.closest('#ruledialog') && condBox.querySelector('.cond.rxbad'));
    sv.disabled = !dirty || rx; c.disabled = !dirty && !p.closest('dialog');   // (a pop-up's Cancel closes it: always available)
    if (dirty && p.dataset.dirty !== '1') p.dataset.dirty = '1'; else if (!dirty) delete p.dataset.dirty;
  });
}
['input', 'change', 'keyup'].forEach(function (t) { document.addEventListener(t, function () { setTimeout(pairRefresh, 0); }, true); });
document.addEventListener('click', function () { setTimeout(pairRefresh, 30); }, true);
document.addEventListener('paircancel', function () { setTimeout(pairRefresh, 0); }, true);
new MutationObserver(function () { clearTimeout(pairRefresh.t); pairRefresh.t = setTimeout(pairRefresh, 60); }).observe(document.body, { childList: true, subtree: true });
pairRefresh();


// (0.2.8-beta.29, F32) Settings > Administrator: the current password and the repeat are asked for only while the
// user name or the password is changed; Cancel puts them away again.
function bindSettingsForms() { each('#adminform', 'admin', function (f) {
  function more() {
    var u = f.elements.user, pw = f.elements.password;
    var on = !!pw.value || u.value.trim() !== u.defaultValue;
    f.querySelectorAll('.more').forEach(function (el) { el.hidden = !on; });
    f.elements.current.required = on;
  }
  f.addEventListener('input', more);
  f.addEventListener('paircancel', function () { setTimeout(more, 0); });
});

// (0.2.8-beta.29, F14) Settings > Look: the animation sliders act at once (the page shows them); Reset puts both back to 100 %.
// A saved Look redraws the whole page (the logo and favicon are in its head).
each('form.lookform', 'look', function (f) {
  var I = document.getElementById('animI'), D = document.getElementById('animD');
  function apply() {
    var r = document.documentElement.style;
    r.setProperty('--anim-i', (I.value / 100).toString()); r.setProperty('--anim-d', (D.value / 100).toString());
    document.getElementById('animIo').textContent = I.value + '%'; document.getElementById('animDo').textContent = D.value + '%';
  }
  I.addEventListener('input', apply); D.addEventListener('input', apply);
  f.addEventListener('paircancel', function () { setTimeout(apply, 0); });
  document.getElementById('animReset').addEventListener('click', function () {
    I.value = 100; D.value = 100; apply();
    I.dispatchEvent(new Event('input', { bubbles: true }));
  });
}); }
bindSettingsForms();
