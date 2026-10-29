{# The status page's script (0.2.8-beta.4): one file per version and language, cached by the browser.
   What changes from page to page (the form token, the view…) comes from #pagedata. #}
var PAGE = JSON.parse(document.getElementById('pagedata').textContent);
// Texts used by the scripts below, in the page's language.
var T = {
  copied: {{ _('Copied')|string|tojson }}, gSaving: {{ _('Saving…')|string|tojson }}, gChecking: {{ _('Checking…')|string|tojson }}, gAddress: {{ _('Checking address…')|string|tojson }}, gOpening: {{ _('Opening Google…')|string|tojson }}, stepAuto: {{ _('Ticks itself when CalendarStream can confirm it')|string|tojson }}, stepDone: {{ _('Step done')|string|tojson }}, pressCtrlC: {{ _('Press Ctrl+C')|string|tojson }},
  saved: {{ _('Saved')|string|tojson }}, verifying: {{ _('Verifying…')|string|tojson }},
  validated: {{ _('Validated')|string|tojson }}, verifyFailed: {{ _('Failed')|string|tojson }},
  disconnect: {{ _('Disconnect Google Calendar?')|string|tojson }},
  downloading: {{ _('Downloading…')|string|tojson }}, restarting: {{ _('Restarting…')|string|tojson }},
  updateFailed: {{ _('Update failed')|string|tojson }}, updated: {{ _('Updated')|string|tojson }}, updateSlow: {{ _('It’s taking longer than expected; check the updater container’s log.')|string|tojson }},
  syncing: {{ _('Syncing…')|string|tojson }}, saving: {{ _('Saving…')|string|tojson }},
  copiedReport: {{ _('Report copied')|string|tojson }}, longReport: {{ _('The report is long, so GitHub gets the start of it; the whole report is copied: paste it into the issue.')|string|tojson }},
  alreadyHere: {{ _('Already in this calendar ({n} of {total})')|string|tojson }},
  failed: {{ _('Failed')|string|tojson }}, ok: {{ _('OK')|string|tojson }}, cancel: {{ _('Cancel')|string|tojson }}, yes: {{ _('Yes')|string|tojson }}
};

// Icons the scripts put next to a message (Material Symbols).
var ICON = { ok: {{ icon("check_circle", 15)|string|tojson }}, fail: {{ icon("cancel", 15)|string|tojson }},
             run: {{ icon("sync", 15)|string|tojson }}, warn: {{ icon("warning", 15)|string|tojson }} };

// Questions and notices in a web pop-up (0.2.8-beta.15), never the browser's own alert / confirm boxes:
// ask(text, [{label, value, cls}], vertical) resolves to the chosen value (null when closed).
function ask(text, choices, vertical) {
  var d = document.getElementById('askdialog'), box = d.querySelector('.askchoices');
  d.querySelector('.asktext').textContent = text;
  box.classList.toggle('vert', !!vertical); box.innerHTML = '';
  return new Promise(function (ok) {
    choices.forEach(function (c) {
      var b = document.createElement('button'); b.type = 'button'; b.className = c.cls || ''; b.textContent = c.label;
      b.addEventListener('click', function () { ok(c.value); d.close(); });
      box.appendChild(b);
    });
    d.addEventListener('close', function once() { d.removeEventListener('close', once); ok(null); });
    d.showModal();
    var last = box.lastElementChild; if (last) last.focus();
  });
}
function tell(text) { return ask(text, [{ label: T.ok, value: true }]); }
function confirmed(text, yes) { return ask(text, [{ label: T.cancel, value: false, cls: 'ghost' }, { label: yes || T.yes, value: true, cls: 'danger solid' }]); }
// A form that asks first: sent only after Yes in the pop-up
function guard(f, text) {
  f.addEventListener('submit', function (e) {
    if (f.dataset.confirmed) { delete f.dataset.confirmed; return; }
    e.preventDefault(); e.stopImmediatePropagation();
    var sub = e.submitter && e.submitter.form === f ? e.submitter : undefined;
    confirmed(typeof text === 'function' ? text() : text).then(function (y) { if (y) { f.dataset.confirmed = '1'; f.requestSubmit(sub); } });
  });
}

// Bind behaviour to elements once each: run again after a section is swapped in, it only binds the
// new elements (an element's mark doesn't survive being replaced).
function each(sel, key, fn) {
  document.querySelectorAll(sel).forEach(function (el) { if (el['_b_' + key]) return; el['_b_' + key] = true; fn(el); });
}

// Copy a field's text. Uses the Clipboard API on HTTPS/localhost, and falls back to
// select + execCommand on plain-HTTP pages (e.g. http://192.168.x.x:8080) where it's blocked.
function copyField(id, btn) {
  var el = document.getElementById(id), text = el.value, icon = btn.innerHTML;
  function done(msg) {   // show the result briefly, then the copy icon again
    btn.textContent = msg || T.copied; btn.classList.add('done');
    setTimeout(function () { btn.innerHTML = icon; btn.classList.remove('done'); }, 1800);
  }
  function fallback() {
    el.focus(); el.select(); el.setSelectionRange(0, text.length);
    var ok = false;
    try { ok = document.execCommand('copy'); } catch (e) {}
    done(ok ? T.copied : T.pressCtrlC);   // text stays selected if the browser refused
  }
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(function () { done(); }, fallback);
  } else { fallback(); }
}

// Login forms ("watch"): typing swaps "✓ Validated" / "✓ Signed in" for Save and Cancel (and shows any
// extra fields the change needs: the page login asks for the current password). Cancel grows to fill
// the slot, undoes the typing and fades back to ✓. Save grows and is sent in the background: "Saved",
// then "Verifying…" (the server checks the login: /verify), then "✓ Validated" or "✗ Verification
// failed" with the reason under the boxes. The page login has nothing to verify: it's simply sent.
function bindWatch() { each('form.watch', 'watch', function (f) {
  var slot = f.querySelector('.okslot');
  if (!slot) return;
  var save = slot.querySelector('.slotsave'), cancel = slot.querySelector('.slotcancel'), word = save.querySelector('.slotword'),
      msg = slot.querySelector('.slotmsg'), label = word.textContent, initial = slot.dataset.state, note = null;
  function set(state) { slot.dataset.state = state; }
  function busy() { return slot.dataset.state === 'saving' || slot.dataset.state === 'verifying' || slot.dataset.state === 'valid'; }
  function extras(show) {
    f.querySelectorAll('.more').forEach(function (el) { el.hidden = !show; });
    f.querySelectorAll('[data-required]').forEach(function (el) { el.required = show; });
  }
  function fail(text) {
    set('failed'); msg.innerHTML = ICON.fail + esc(T.verifyFailed); word.textContent = label;
    if (text) { note = document.createElement('p'); note.className = 'check bad slotnote'; note.textContent = text; f.appendChild(note); }
  }
  f.addEventListener('input', function () {
    if (busy()) return;
    if (note) { note.remove(); note = null; }
    set('edit'); extras(true);
  });
  cancel.addEventListener('click', function () {
    f.reset(); extras(false);
    if (note) { note.remove(); note = null; }
    set('cancel');
    setTimeout(function () { set(initial); }, 380);
  });
  f.addEventListener('submit', function (e) {
    if (e.submitter && !e.submitter.matches('.slotsave')) return;     // Check again, Remove…: a normal post
    if (busy()) { e.preventDefault(); return; }
    e.preventDefault();
    var data;
    try { data = new FormData(f, e.submitter || undefined); } catch (err) { data = new FormData(f); if (save.name) data.append(save.name, save.value); }
    set('saving');
    var kind = f.dataset.verify;
    if (!kind && f.dataset.swap) {     // saved in place (Settings, beta.3): only the parts it names are redrawn
      sendSwap(f, data).catch(function (err) { fail(err.message); });
      return;
    }
    if (!kind) {     // nothing to check here: show Saved, then send it
      setTimeout(function () { word.textContent = T.saved; setTimeout(function () { HTMLFormElement.prototype.submit.call(f); }, 450); }, 300);
      return;
    }
    var pause = function (ms) { return new Promise(function (ok) { setTimeout(ok, ms); }); };
    fetch(f.getAttribute('action'), { method: 'POST', body: data, credentials: 'same-origin', headers: { 'X-CS-Async': '1' } })
      .then(function (r) { return r.json().catch(function () { return {}; }).then(function (j) { if (!r.ok) throw (j.detail || ''); }); })
      .then(function () { word.textContent = T.saved; return pause(600); })
      .then(function () {
        set('verifying'); msg.textContent = T.verifying;
        var body = new URLSearchParams({ csrf: CSRF, kind: kind, sid: f.dataset.sid || '' });
        return fetch('/verify', { method: 'POST', body: body, credentials: 'same-origin', headers: { 'X-CS-Async': '1' } })
          .then(function (r) { return r.json(); });
      })
      .then(function (j) {
        if (!j.ok) return fail(j.message);
        set('valid'); msg.innerHTML = ICON.ok + esc(T.validated); initial = 'ok';
        setTimeout(function () { location.reload(); }, 1600);      // show the rest of the page up to date
      })
      .catch(function (text) { fail(typeof text === 'string' ? text : ''); });
  });
}); }
bindWatch();

// #9: the styled "Choose Calendar.ics…" button shows the chosen file's name.
function bindFiles() { each('.filebtn input[type=file]', 'file', function (input) {
  input.addEventListener('change', function () {
    var label = input.parentNode.querySelector('span');
    label.textContent = input.files && input.files[0] ? input.files[0].name : label.dataset.none;
  });
}); }
bindFiles();

// The calendar changes in place: a view (month, week, day, list), a time zone or another month is
// fetched and swapped in without reloading the page (and the address keeps the month, not the view).
function swapIn(url, selectors) {
  return fetch(url, { cache: 'no-store', credentials: 'same-origin' })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
    .then(function (html) {
      var doc = new DOMParser().parseFromString(html, 'text/html');
      selectors.forEach(function (sel) {
        var fresh = doc.querySelectorAll(sel);
        document.querySelectorAll(sel).forEach(function (el, i) { if (fresh[i]) el.replaceWith(fresh[i]); });
      });
      return doc;
    });
}
function loadCal(url) {
  var cal = document.getElementById('cal');
  if (cal) cal.classList.add('loading');
  return swapIn(url, ['#cal']).then(function () {
    var u = new URL(url, location.href); u.searchParams.delete('view');
    history.replaceState(null, '', u.pathname + u.search + location.hash);
    initCal();
  }, function () { location.href = url; });
}
function chooseView(view) {
  savePref('/ui/view', { view: view });
  var u = new URL(location.href); u.searchParams.set('view', view); u.hash = '';
  loadCal(u.toString());
}
function initCal() {
  // The 12h / 24h switch: the only place the time format is set (times elsewhere change too, so the
  // page is drawn again).
  var sw = document.getElementById('clockswitch');
  if (sw) sw.addEventListener('click', function () {
    var to24 = sw.getAttribute('aria-checked') !== 'true';
    sw.setAttribute('aria-checked', String(to24));
    savePref('/ui/clock', { clock: to24 ? '24' : '12' }, function () { location.reload(); });
  });
  document.querySelectorAll('.viewseg [data-view]').forEach(function (b) {
    b.addEventListener('click', function () { chooseView(b.dataset.view); });
  });
  // Narrow screens: one button steps through the views.
  var order = ['month', 'week', 'day', 'list'], cyc = document.querySelector('.viewcycle');
  if (cyc) cyc.addEventListener('click', function () { chooseView(order[(order.indexOf(cyc.dataset.view) + 1) % order.length]); });
  // The time zone (this page only).
  var sel = document.getElementById('tzpick');
  if (sel) sel.addEventListener('change', function () { savePref('/ui/tz', { tz: sel.value }, function () { loadCal(location.href); }); });
  // Month picker: ‹ › change the year; a month jumps there.
  var btn = document.getElementById('monthbtn'), box = document.getElementById('monthpick');
  if (!btn) return;
  var cur = box.dataset.month, year = +cur.slice(0, 4), yearEl = document.getElementById('pickyear');
  function draw() {
    yearEl.textContent = year;
    box.querySelectorAll('[data-m]').forEach(function (b) { b.classList.toggle('on', year + '-' + b.dataset.m === cur); });
  }
  btn.addEventListener('click', function () {
    var open = box.hidden; box.hidden = !open; btn.setAttribute('aria-expanded', String(open));
    if (open) { year = +cur.slice(0, 4); draw(); }
  });
  box.addEventListener('click', function (e) {
    var y = e.target.closest('[data-year]'), m = e.target.closest('[data-m]');
    if (y) { year += +y.dataset.year; draw(); }
    if (m) loadCal('/?date=' + year + '-' + m.dataset.m + '-01');
  });
}
initCal();
// The calendar's search (0.2.8-beta.11): the search icon opens the line under the header; typing (or a
// filter) shows what matches, listed by day, in place of the calendar; ✕ closes it and brings the
// calendar back. Only the results and the title are redrawn, so the words being typed stay put.
(function () {
  var timer = null, last = '';
  function form() { return document.getElementById('calsearch'); }
  function show(url) {
    return swapIn(url, ['#calbody', '#monthbtn']).then(function () { initCal(); bindAll(); reopenEvents(); });
  }
  function run() {
    var f = form(), q = f.elements.q.value.trim();
    var u = new URL('/', location.href);
    if (q) {
      u.searchParams.set('q', q);
      ['qsrc', 'qfrom', 'qto'].forEach(function (k) { if (f.elements[k].value) u.searchParams.set(k, f.elements[k].value); });
    } else {
      var here = new URL(location.href); ['date', 'month'].forEach(function (k) { if (here.searchParams.get(k)) u.searchParams.set(k, here.searchParams.get(k)); });
    }
    if (u.toString() === last) return;
    last = u.toString(); show(last);
  }
  function close() {
    var f = form(); f.hidden = true; f.reset(); f.elements.q.value = '';
    document.getElementById('searchbtn').setAttribute('aria-expanded', 'false');
    last = ''; run();
  }
  document.addEventListener('click', function (e) {
    if (e.target.closest('#searchbtn')) {
      var f = form(), open = f.hidden;
      if (!open) { close(); return; }
      f.hidden = false; e.target.closest('#searchbtn').setAttribute('aria-expanded', 'true'); f.elements.q.focus();
    }
    if (e.target.closest('#calqclose')) close();
    var plus = e.target.closest('.calplus');
    if (plus) openEvent(plus.dataset.add);
  });
  document.addEventListener('input', function (e) {
    if (!e.target.closest || !e.target.closest('#calsearch')) return;
    clearTimeout(timer); timer = setTimeout(run, 300);
  });
  document.addEventListener('change', function (e) { if (e.target.closest && e.target.closest('#calsearch')) run(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && e.target.closest && e.target.closest('#calsearch')) close(); });
})();
// ‹ › and Today swap the calendar in too (a click with Ctrl or ⌘ still opens a new tab).
document.addEventListener('click', function (e) {
  var a = e.target.closest('#cal .calhead a.navbtn');
  if (!a || e.ctrlKey || e.metaKey || e.shiftKey || e.button) return;
  e.preventDefault(); loadCal(a.href);
});
// The month picker closes on an outside click or Escape.
function closeMonthPick() {
  var box = document.getElementById('monthpick'), btn = document.getElementById('monthbtn');
  if (box && !box.hidden) { box.hidden = true; btn.setAttribute('aria-expanded', 'false'); }
}
document.addEventListener('click', function (e) { if (!e.target.closest('.monthwrap')) closeMonthPick(); });
document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeMonthPick(); });
// Until a view has been chosen, phones open on the list (an itinerary); wider screens on the month.
(function () {
  if (!PAGE.viewExplicit && window.matchMedia('(max-width: 700px)').matches && PAGE.view === 'month'
      && !/[?&]view=/.test(location.search)) {
    var u = new URL(location.href); u.searchParams.set('view', 'list');
    loadCal(u.toString());
  }
})();

// Save a status-page preference in the database (so every browser and login matches).
// Fire-and-forget unless a callback is given: if it fails, the page still works.
function savePref(path, fields, then) {
  var body = new URLSearchParams(Object.assign({ csrf: CSRF }, fields));
  fetch(path, { method: 'POST', body: body, credentials: 'same-origin' }).then(then || function () {}, then || function () {});
}
var CSRF = PAGE.csrf;

// (?): hovering or focusing shows the explanation; a click (or tap) keeps it open until a click
// elsewhere or Escape. Delegated, so it also works in sections swapped in after a save.
document.addEventListener('click', function (e) {
  var dot = e.target.closest('.helpdot');
  document.querySelectorAll('.helpdot.open').forEach(function (d) { if (d !== dot) { d.classList.remove('open'); d.setAttribute('aria-expanded', 'false'); } });
  if (!dot || e.target.closest('.helptip')) return;
  e.preventDefault(); e.stopPropagation();
  var on = !dot.classList.contains('open');
  dot.classList.toggle('open', on); dot.setAttribute('aria-expanded', String(on));
}, true);
document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.helpdot.open').forEach(function (d) { d.classList.remove('open'); d.setAttribute('aria-expanded', 'false'); });
    if (document.activeElement && document.activeElement.classList.contains('helpdot')) document.activeElement.blur();
  }
  if ((e.key === 'Enter' || e.key === ' ') && e.target.classList && e.target.classList.contains('helpdot')) { e.preventDefault(); e.target.click(); }
});

// Update now (top bar) and Settings → Update: ask the updater (POST /update/now), then follow along
// with /api/status. It answers with the old version while the new image downloads, not at all while
// the container restarts, then with the new version: the version at the top (and in the footer)
// changes and the page reloads with the new version. One listener for the whole
// page, so the buttons keep working after Settings is redrawn in place (a Check now, a save).
var updating = false;
function updateNow() {
  var slot = document.querySelector('.updslot');
  if (!slot || updating) return;
  var btn = slot.querySelector('.updbtn'), text = slot.querySelector('.updtext'), from = slot.dataset.from;
  // One action, one state (0.2.8-beta.13): the top bar's Update now and Settings → Update now always show
  // the same words at the same moment (Downloading…, Restarting…, then Updated or Update failed), and
  // end together.
  function settingsBtns(state, label) { document.querySelectorAll('button.upgradebtn').forEach(function (b) {
    b.dataset.state = state; b.disabled = state === 'syncing';
    if (state === 'fail') b.dataset.cause = 'inside'; else delete b.dataset.cause;   // CalendarStream's updater failed: red (beta.14)
    var words = b.querySelector('.sn.' + (state === 'syncing' ? 'syncing' : state) + ' .snword');
    if (words && label) words.textContent = label;
  }); }
  function show(state, label) {
    slot.dataset.state = state; text.textContent = label || '';
    settingsBtns({ downloading: 'syncing', restarting: 'syncing', failed: 'fail', done: 'done' }[state] || 'idle', label);
  }
  function fail(why) { updating = false;
                       show('failed', T.updateFailed); text.insertAdjacentHTML('afterbegin', ICON.fail); slot.title = why || ''; btn.disabled = false;
                       setTimeout(function () { if (slot.dataset.state === 'failed') show('ready'); }, 2400); }
  function done(version) {
    document.querySelectorAll('.topbar .curver').forEach(function (a) {
      a.textContent = 'v' + version; a.href = a.href.replace(/\/v[^\/]*$/, '/v' + version);
    });
    var foot = document.querySelector('.foot');
    if (foot) foot.innerHTML = foot.innerHTML.replace('v' + from, 'v' + version);
    document.querySelectorAll('.topbar .newver').forEach(function (el) { el.remove(); });
    show('done', T.updated);
    // The page is reloaded (0.2.8-beta.9) so the new version's script and stylesheet are the ones
    // running: drawn in place, its parts would be run by the old ones. Settings stays open if it was.
    var menu = document.getElementById('menu'), inSettings = menu && !menu.hidden;
    setTimeout(function () {
      if (inSettings && !/[?&]menu=settings/.test(location.search)) location.href = '/?menu=settings#updates';
      else location.reload();
    }, 800);
  }
  function follow() {
    var started = Date.now(), down = false;
    (function poll() {
      fetch('/api/status', { cache: 'no-store', credentials: 'same-origin' })
        .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
        .then(function (j) {
          if (j.version && j.version !== from) { done(j.version); return; }
          next();
        }, function () { if (!down) { down = true; show('restarting', T.restarting); } next(); });
      function next() {
        if (Date.now() - started > 15 * 60 * 1000) { fail(T.updateSlow); return; }
        setTimeout(poll, 2000);
      }
    })();
  }
  updating = true;
  btn.disabled = true; slot.title = ''; show('downloading', T.downloading);
  fetch('/update/now', { method: 'POST', body: new URLSearchParams({ csrf: CSRF }), credentials: 'same-origin',
                         headers: { 'X-CS-Async': '1' } })
    .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw new Error(j.detail || ('HTTP ' + r.status)); return j; }); })
    .then(follow, function (e) { fail(e.message); });
}
document.addEventListener('click', function (e) {
  var b = e.target.closest && e.target.closest('.updslot .updbtn, button.upgradebtn');
  if (!b || b.disabled) return;
  updateNow();
});

// Settings → Google Calendar API Sync → Guided setup (0.2.8-beta.10): a tick on each step (the client
// steps, 6 and 7, tick themselves once Google accepted the client, step 8 once connected; the others are
// ticked by hand and remembered in this browser), the first unticked step marked as the current one,
// and Google's pages opened in a window beside this one.
// Google Calendar API Sync → Connect, one straight line (0.2.8-beta.14): Saving…, Checking…, Checking
// address…, then Google's sign-in. Each step is asked of the server in turn and shown in the status box
// (the theme's multi-button); the first that fails stops it: the box pulses Stopped and the line under
// the row says what to fix, with Copy and Open buttons. Pressing Connect again starts over.
document.addEventListener('click', function (e) {
  var btn = e.target.closest('.gconnectbtn');
  if (!btn || btn.dataset.state !== 'idle') return;
  var f = btn.closest('form'), box = f.querySelector('.gstepmsg'), words = btn.querySelector('.sn.syncing .snword');
  var steps = [['save', T.gSaving], ['client', T.gChecking], ['address', T.gAddress], ['go', T.gOpening]];
  box.hidden = true; btn.dataset.state = 'syncing'; btn.disabled = true;
  function stopped(j) {
    btn.dataset.state = 'fail';
    f.querySelector('.gsteptext').textContent = j.message || T.failed;
    f.querySelector('.gcopyaddr').hidden = !(j.fix && j.fix.copy);
    f.querySelector('.gopenclient').hidden = !(j.fix && j.fix.open);
    box.hidden = false;
    setTimeout(function () { btn.dataset.state = 'idle'; btn.disabled = false; }, 2400);
  }
  (function next(i) {
    var step = steps[i], started = Date.now();
    words.textContent = step[1];
    var body = new URLSearchParams({ csrf: CSRF, step: step[0], client_id: f.elements.client_id.value, client_secret: f.elements.client_secret.value });
    fetch('/google/step', { method: 'POST', body: body, credentials: 'same-origin', headers: { 'X-CS-Async': '1' } })
      .then(function (r) { return r.json(); })
      .then(function (j) {
        setTimeout(function () {
          if (!j.ok) { stopped(j); return; }
          if (step[0] === 'go') { btn.dataset.state = 'done'; setTimeout(function () { location.href = j.url; }, 400); return; }
          next(i + 1);
        }, Math.max(0, 500 - (Date.now() - started)));      // each step stays long enough to read
      }, function () { stopped({}); });
  })(0);
});

function bindGuide() { each('details.gsteps', 'gsteps', function (g) {
  var key = 'cs-gsteps', done = {};
  try { done = JSON.parse(localStorage.getItem(key) || '{}') || {}; } catch (err) { done = {}; }
  var auto = { 6: g.dataset.address === '1', 7: g.dataset.valid === '1', 8: g.dataset.connected === '1' };   // 6: Google accepts the address (beta.14)
  var steps = g.querySelectorAll('li[data-step]');
  function mark() {
    var current = null;
    steps.forEach(function (li) {
      var n = li.dataset.step, on = !!(auto[n] || done[n]), box = li.querySelector('.steptick');
      box.checked = on; li.classList.toggle('done', on);
      li.classList.remove('current');
      if (!on && !current) current = li;
    });
    if (current) current.classList.add('current');
  }
  steps.forEach(function (li) {
    var n = li.dataset.step, box = document.createElement('input');
    box.type = 'checkbox'; box.className = 'steptick';
    if (auto[n] !== undefined) { box.disabled = true; box.title = T.stepAuto; }
    box.setAttribute('aria-label', T.stepDone + ' ' + n);
    box.addEventListener('change', function () {
      done[n] = box.checked;
      try { localStorage.setItem(key, JSON.stringify(done)); } catch (err) { /* private window: kept for this visit */ }
      mark();
    });
    li.insertBefore(box, li.firstChild);
  });
  mark();
  // Google's pages: in a window beside this one (the right half of the screen)
  g.querySelectorAll('a[href^="https://console.cloud.google.com"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var w = Math.round((screen.availWidth || 1400) / 2), h = screen.availHeight || 900;
      var win = window.open(a.href, 'csgoogle', 'popup,width=' + w + ',height=' + h + ',left=' + w + ',top=0');
      if (win) { e.preventDefault(); win.focus(); }
    });
  });
}); }
bindGuide();

// Small drop-down menus (settings, language): close on an outside click or Escape.
function dropdown(btnId, menuId) {
  var btn = document.getElementById(btnId), menu = document.getElementById(menuId);
  function set(open) { menu.hidden = !open; btn.setAttribute('aria-expanded', String(open)); }
  btn.addEventListener('click', function (e) { e.stopPropagation(); set(menu.hidden); });
  document.addEventListener('click', function (e) { if (!menu.hidden && !menu.contains(e.target)) set(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
  return set;
}

// Language: saved in the database, then the page is drawn again in the new language.
(function () {
  dropdown('langbtn', 'langmenu');
  document.querySelectorAll('#langmenu [data-lang]').forEach(function (b) {
    b.addEventListener('click', function () {
      savePref('/ui/lang', { lang: b.dataset.lang }, function () { location.reload(); });
    });
  });
})();

// Light / dark / system theme. "system" removes the override so the device setting applies.
(function () {
  var buttons = document.querySelectorAll('[data-theme-choice]');
  function show(choice) {
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.themeChoice === choice)); });
  }
  buttons.forEach(function (b) {
    b.addEventListener('click', function () {
      var choice = b.dataset.themeChoice;
      if (choice === 'system') document.documentElement.removeAttribute('data-theme');
      else document.documentElement.setAttribute('data-theme', choice);
      show(choice);
      savePref('/ui/theme', { theme: choice });
    });
  });
  show(PAGE.theme);
  // Narrow screens: one button steps through light → dark → system.
  var cyc = document.querySelector('.themecycle'), themes = ['light', 'dark', 'system'];
  var current = PAGE.theme;
  function label() {      // the same icon as the theme switch's button for it
    cyc.innerHTML = document.querySelector('[data-theme-choice="' + current + '"]').innerHTML;
    cyc.title = document.querySelector('[data-theme-choice="' + current + '"]').title;
  }
  label();
  cyc.addEventListener('click', function () {
    current = themes[(themes.indexOf(current) + 1) % themes.length];
    if (current === 'system') document.documentElement.removeAttribute('data-theme');
    else document.documentElement.setAttribute('data-theme', current);
    show(current); label();
    savePref('/ui/theme', { theme: current });
  });
})();

// "This page" fills the public address with the address this page is open at.
document.getElementById('usethis').addEventListener('click', function () {
  var input = document.getElementById('publicurl');
  input.value = location.origin;
  input.dispatchEvent(new Event('input', { bubbles: true }));      // shows ✕ | ✓
});

// Settings menu: opens by itself after Check for updates (?menu=settings). The Disconnect
// confirmation belongs to the Google Calendar Autosync box.
(function () {
  var set = dropdown('menubtn', 'menu');
  if (PAGE.openMenu) {
    set(true);
    history.replaceState(null, '', location.pathname);   // a reload shouldn't open it again
  }
  each('.disconnectform', 'disconnect', function (f) { guard(f, T.disconnect); });
})();

// Collapsible sections: clicking the header (outside its form) or the arrow opens or closes the
// section, and the state is saved in the database. + in a folded section's corner opens it too.
function initSections() {
  document.querySelectorAll('.section[data-section]').forEach(function (sec) {
    if (sec.dataset.bound) return;
    sec.dataset.bound = '1';
    var head = sec.querySelector(':scope > .shead'), toggle = sec.querySelector(':scope > .shead .toggle, :scope > .cfgline .toggle'),
        body = sec.querySelector(':scope > .sbody');
    function set(open) {
      sec.classList.toggle('open', open);
      body.hidden = !open;
      toggle.setAttribute('aria-expanded', String(open));
      savePref('/ui/section', { section: sec.dataset.section, open: open ? '1' : '0' });
    }
    head.addEventListener('click', function (e) {
      if (e.target.closest('form, #editbtn, .helpdot')) return;   // the editor and (?) don't toggle the section
      // A section that looks like a module (All Rules, Event Templates, History) opens only
      // from its Expand line (or +), like a module: a click on its header leaves it as it is (beta.3)
      if (sec.classList.contains('modsection') && !e.target.closest('.headplus')) return;
      if (e.target.closest('.headplus')) { if (!sec.classList.contains('open')) set(true); return; }
      set(!sec.classList.contains('open'));
    });
    if (!head.contains(toggle)) toggle.addEventListener('click', function () { set(!sec.classList.contains('open')); });
  });
}
initSections();

// Modules (calendars, feeds, the Google account): "▸ Expand … ◂" opens the rest; "Close" (or Cancel)
// folds it. While open, a calendar's title and note (a feed's name) are fields. Open or folded is
// remembered (in the database).
function setModule(box, open) {
  var cfg = box.querySelector('.cfgtoggle'), body = box.querySelector('.cfgbody');
  if (!cfg || !body || body.hidden === !open) return;
  body.hidden = !open;
  box.classList.toggle('cfgopen', open);
  cfg.setAttribute('aria-expanded', String(open));
  var pick = box.querySelector('.colorpick');
  if (pick) pick.tabIndex = open ? 0 : -1;
  if (!open) colorOpen(box, false);
  savePref('/ui/section', { section: box.dataset.section, open: open ? '1' : '0' });
}
function bindCfg() { each('.box.cfgbox, .module.bare.cfgbox', 'cfg', function (box) {
  box.querySelector('.cfgtoggle').addEventListener('click', function () { setModule(box, !box.classList.contains('cfgopen')); });
  // The color box changes the calendar's color while the module is expanded (0.2.8-beta.3), like its
  // title and note; folded, it only shows it.
  var pick = box.querySelector('.colorpick');
  if (pick) pick.tabIndex = box.classList.contains('cfgopen') ? 0 : -1;
}); }
// The color box (0.2.8-beta.15): a click opens Google's 11 colors (only while its module is expanded, or
// anywhere it's free to change); a chosen color is sent with the module's Save. (Listened for on the page:
// the header, color box included, is swapped for a new one after each save.)
function colorOpen(scope, on) {
  scope.querySelectorAll('.palpop').forEach(function (p) { p.hidden = !on; var b = p.parentNode.querySelector('.colorpick'); if (b) b.setAttribute('aria-expanded', String(on)); });
}
document.addEventListener('click', function (e) {
  var cb = e.target.closest && e.target.closest('.colorbox');
  document.querySelectorAll('.palpop:not([hidden])').forEach(function (p) { if (!cb || !cb.contains(p)) colorOpen(p.parentNode, false); });
  if (!cb) return;
  var mod = cb.closest('.module');
  if (mod && !mod.classList.contains('cfgopen') && !cb.classList.contains('free')) return;
  var pal = e.target.closest('.pal');
  if (pal) {
    var val = cb.querySelector('.colorval');
    val.value = pal.dataset.c; if (!val.name) val.name = 'color';
    cb.querySelector('.colorpick').style.setProperty('--c', pal.dataset.c || 'transparent');
    cb.querySelector('.colorpick').classList.toggle('nocolor', !pal.dataset.c);
    cb.querySelectorAll('.pal').forEach(function (b) { b.setAttribute('aria-checked', String(b === pal)); });
    colorOpen(cb, false); cb.querySelector('.colorpick').focus();
    if (cb.classList.contains('free')) cb.dispatchEvent(new Event('change', { bubbles: true }));
    return;
  }
  if (e.target.closest('.colorpick')) colorOpen(cb, cb.querySelector('.palpop').hidden);
});
document.addEventListener('keydown', function (e) { if (e.key === 'Escape') colorOpen(document, false); });
bindCfg();

// A module's header: when the long wording ("Downloaded 98 events from feed @ 14:53.", "Next scheduled
// check @ 15:08") doesn't fit its two status lines, the short wording is used ("98 events @ 14:53",
// "Next check @ 15:08"). Measured in the page, so it also fits other languages. (In a narrow module the
// lines go under the title with the short words anyway: see the CSS.)
(function () {
  var watched = typeof WeakSet === 'function' ? new WeakSet() : null, ro = window.ResizeObserver ? new ResizeObserver(function () { fit(); }) : null;
  function fit() {
    document.querySelectorAll('.srchead').forEach(function (h) {
      if (ro && watched && !watched.has(h)) { watched.add(h); ro.observe(h); }
      var lines = h.querySelectorAll('.srcright p');
      h.classList.remove('tight');
      if (Array.prototype.some.call(lines, function (p) { return p.scrollWidth > p.clientWidth + 1; })) h.classList.add('tight');
    });
  }
  fit();
  window.fitHeads = fit;
  if (!ro) window.addEventListener('resize', fit);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);   // after IBM Plex has loaded
})();

// Sync Now (F1.1): the download runs in the background; the button says Syncing… and only that module's
// header, the calendar and the log are brought up to date when it's done (no page reload). The button
// then pulses green (Synced) or yellow (Failed) for a moment and says Sync Now again. A download that's
// already running when the page opens is followed the same way. "google" is the Google account's.
// "google" is every Google calendar in Feeds (0.2.8-beta.4): one sync for all of them, so each one's
// Sync Now shows it.
function syncButtons(sid) {
  return Array.prototype.map.call(document.querySelectorAll('.syncform input[name=sid][value="' + sid + '"]'),
                                  function (input) { return input.form.querySelector('.syncnow'); });
}
function syncButton(sid) { return syncButtons(sid)[0] || null; }
function moduleOf(sid) { return sid === 'google' ? document.getElementById('destinations') : document.getElementById('src-' + sid); }
function showSyncing(sid) {
  if (!moduleOf(sid)) return;
  syncButtons(sid).forEach(function (btn) {
    var sb = btn.closest('.statusbox'), chip = sb && sb.querySelector('.chip');
    if (chip) { sb.className = 'statusbox run'; chip.className = 'chip run'; chip.innerHTML = ICON.run + '<span class="chiptext">' + esc(T.syncing) + '</span>'; }
    btn.dataset.state = 'syncing'; btn.disabled = true;
  });
}
function syncDone(sid, ok) {
  syncButtons(sid).forEach(function (btn) {
    // The status box was just swapped for a fresh one (at rest): it takes the full-box state at once,
    // without growing again, so the button stays where it was; it shrinks back smoothly later.
    var sb = btn.closest('.statusbox');
    if (sb) sb.classList.add('instant');
    btn.dataset.state = ok ? 'done' : 'fail'; btn.disabled = true;
    // red when CalendarStream itself failed (its fresh box says so), amber when the trouble is outside it (beta.14)
    if (!ok && sb && sb.classList.contains('bad')) btn.dataset.cause = 'inside'; else delete btn.dataset.cause;
    if (sb) { void sb.offsetHeight; requestAnimationFrame(function () { sb.classList.remove('instant'); }); }
    setTimeout(function () { btn.dataset.state = 'idle'; btn.disabled = false; }, 2400);
  });
}
function followSync(sid) {
  var box = moduleOf(sid);
  if (!box || box._following) return;
  box._following = true;
  showSyncing(sid);
  var started = Date.now();
  (function poll() {
    fetch('/api/status', { cache: 'no-store', credentials: 'same-origin' }).then(function (r) { return r.json(); }).then(function (j) {
      var me = sid === 'google' ? j.google : (j.sources || []).filter(function (x) { return x.id === sid; })[0];
      if (me && (me.running || me.pending) && Date.now() - started < 5 * 60 * 1000) { setTimeout(poll, 1500); return; }
      // only the status parts of the headers: a title being typed is kept
      var head = sid === 'google' ? ['.box.dest .srcright', '.box.dest .statusbox', '#googlesync']
                                  : ['#src-' + sid + ' .srcright', '#src-' + sid + ' .statusbox'];
      swapIn(location.href, ['#cal', '#activity'].concat(head)).then(function () {
        initCal(); bindAll();
        syncDone(sid, !!me && (sid === 'google' ? !me.error : me.status === 'ok'));
        var b = moduleOf(sid); if (b) b._following = false;
      });
    }, function () { setTimeout(poll, 3000); });
  })();
}
document.addEventListener('submit', function (e) {
  var f = e.target.closest('form.syncform');
  if (!f) return;
  e.preventDefault();
  var sid = f.elements.sid.value;
  showSyncing(sid);
  fetch(f.getAttribute('action'), { method: 'POST', body: new URLSearchParams({ csrf: CSRF, sid: sid }), credentials: 'same-origin',
                    headers: { 'X-CS-Async': '1' } }).then(function () { followSync(sid); }, function () { f.submit(); });
});
function followRunning() {
  document.querySelectorAll('.box.module .statusbox.run').forEach(function (sb) {
    var box = sb.closest('.box.module');
    var sid = box.classList.contains('gdest') ? 'google' : box.dataset.sid;
    if (sid) followSync(sid);
  });
}
followRunning();

// A calendar module: Cancel puts back its title, note and color; its rules: ✎ opens the rule dialog,
// the bin takes a rule off this calendar, + Add a rule offers a new rule or one of the others.
function bindSrc() { each('.box.src', 'src', function (box) {
  var val = box.querySelector('.colorval'), form = document.getElementById('srcform-' + box.dataset.sid);
  if (form) form.addEventListener('paircancel', function () {
    if (!val) return;
    val.removeAttribute('name'); val.value = val.dataset.default;
    box.querySelector('.colorpick').style.setProperty('--c', val.dataset.default);
    box.querySelectorAll('.pal').forEach(function (b) { b.setAttribute('aria-checked', String(b.dataset.c === val.dataset.default)); });
  });
}); }
bindSrc();
var RD = JSON.parse(document.getElementById('ruledata').textContent);
function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
function opts(list, cur) { return list.map(function (o) { return '<option value="' + esc(o[0]) + '"' + (String(o[0]) === String(cur) ? ' selected' : '') + '>' + esc(o[1]) + '</option>'; }).join(''); }
function hm(min) { return Math.floor(min / 60) + ':' + ('0' + min % 60).slice(-2); }
function minutesOf(text) { var m = /^\s*(\d{1,3})(?::(\d{1,2}))?\s*$/.exec(text || ''); return m ? +m[1] * 60 + +(m[2] || 0) : NaN; }
document.addEventListener('click', function (e) {
  var line = e.target.closest('.ruleline');
  if (line && e.target.closest('.editrule')) { openRule(RD.rules[line.dataset.ruleId] || null); return; }
  if (line && e.target.closest('.unapply')) {
    var body = new URLSearchParams({ csrf: CSRF, id: line.dataset.ruleId, sid: line.dataset.sid, on: '0' });
    line.classList.add('going');
    fetch('/rules/apply', { method: 'POST', body: body, credentials: 'same-origin', headers: { 'X-CS-Async': '1' } })
      .then(function () { return swapIn(location.href, ['#src-' + line.dataset.sid + ' .rules', '#rules .rulelist', '#ruleconflicts', '#rulecount', '#cal', '#activity', '#ruledata']); })
      .then(function () { RD = JSON.parse(document.getElementById('ruledata').textContent); initCal(); bindAll(); reopenEvents(); });
    return;
  }
  var nr = e.target.closest('.newrule');
  if (nr) { var w = nr.closest('.addwrap'); if (w && w.querySelector('.rulemenu')) w.querySelector('.rulemenu').hidden = true; openRule(null, nr.dataset.sid || ''); }
});

// Report a problem / Suggest a feature: the form gathers what's ticked (private details are taken out
// by the server: /report/data), shows a preview, and opens GitHub's new-issue page filled in. Without a
// GitHub account, the report can be copied or downloaded instead.
(function () {
  var dlg = document.getElementById('reportdialog');
  if (!dlg) return;
  var form = dlg.querySelector('form'), pre = dlg.querySelector('pre.preview'), title = document.getElementById('rptitle'),
      whatLbl = dlg.querySelector('label[for=rpwhat]'), kind = 'bug', data = null;
  function parts() {
    var f = form.elements, p = { what: f.what.value.trim(), log: '', setup: '', device: '', contact: '' };
    if (data && f.inc_activity.checked) p.log = data.activity;
    if (data) dlg.querySelectorAll('input[name=inc_src]:checked').forEach(function (c) {
      var x = data.sources.filter(function (y) { return y.id === c.value; })[0];
      if (x) p.log += '\n\n--- ' + x.name + ' (' + x.type + '): ' + x.status + '\n' + (x.debug || '(no download details)');
    });
    if (data && f.inc_device.checked) {
      p.setup = 'CalendarStream ' + data.version + ' (' + data.image_tag + ', ' + data.channel + '), ' + data.server + ', TZ ' + data.time_zone
              + '\nSources: ' + data.sources.map(function (x) { return x.type + ' (' + x.status.split(':')[0] + ')'; }).join(', ')
              + '\nDestinations: ' + (data.destinations.join(', ') || 'none') + (data.google_connected ? ', Google connected' : '')
              + (data.updater ? ', updater on' : '');
      p.device = 'Browser: ' + navigator.userAgent + '\nScreen: ' + screen.width + '×' + screen.height + ', window ' + innerWidth + '×' + innerHeight
               + '\nLanguage: ' + navigator.language + ', theme: ' + (document.documentElement.dataset.theme || 'system');
    }
    if (f.inc_contact.checked && f.contact.value.trim()) p.contact = f.contact.value.trim();
    if (f.notify.checked) p.contact = (p.contact ? p.contact + ' · ' : '') + 'would like to be notified of replies';
    return p;
  }
  function text() {
    var p = parts(), out = '# ' + (form.elements.subject.value.trim() || title.textContent) + '\n\n' + (p.what || '(no description)');
    if (p.setup) out += '\n\n## Setup\n' + p.setup;
    if (p.device) out += '\n\n## Device\n' + p.device;
    if (p.contact) out += '\n\n## Contact\n' + p.contact;
    if (p.log) out += '\n\n## Logs\n' + p.log;
    return out;
  }
  function refresh() { pre.textContent = text(); }
  document.querySelectorAll('.reportbtn').forEach(function (b) {
    b.addEventListener('click', function () {
      kind = b.dataset.kind; title.textContent = title.dataset[kind]; whatLbl.textContent = whatLbl.dataset[kind];
      dlg.showModal(); refresh();
      if (!data) fetch('/report/data', { cache: 'no-store', credentials: 'same-origin' }).then(function (r) { return r.json(); })
        .then(function (j) { data = j; refresh(); });
    });
  });
  form.addEventListener('input', refresh); form.addEventListener('change', refresh);
  dlg.querySelector('.rpcancel').addEventListener('click', function () { dlg.close(); });
  function copy(then) {
    var t = text();
    (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(then, function () {
      var ta = document.createElement('textarea'); ta.value = t; document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); } catch (e) {} ta.remove(); if (then) then();
    });
  }
  dlg.querySelector('.rpcopy').addEventListener('click', function (e) { var b = e.currentTarget; copy(function () { b.textContent = T.copiedReport; }); });
  dlg.querySelector('.rpdownload').addEventListener('click', function () {
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([text()], { type: 'text/plain' }));
    a.download = 'calendarstream-report.txt'; document.body.appendChild(a); a.click(); a.remove();
  });
  dlg.querySelector('.rpgithub').addEventListener('click', function () {
    var p = parts(), q = new URLSearchParams({ template: kind === 'bug' ? 'bug_report.yml' : 'feature_request.yml',
                                              title: form.elements.subject.value.trim() });
    if (kind === 'bug') { q.set('version', data ? data.version : ''); q.set('what', p.what); q.set('setup', p.setup); q.set('device', p.device); q.set('log', p.log); }
    else { q.set('idea', p.what); q.set('setup', p.setup); }
    q.set('contact', p.contact);
    var url = 'https://github.com/Uuugh/CalendarStream/issues/new?' + q.toString();
    if (url.length > 7000) {          // too long for a link: GitHub gets the start, the whole report is copied
      q.set('log', p.log.slice(0, 1500) + '\n… ' + T.longReport);
      url = 'https://github.com/Uuugh/CalendarStream/issues/new?' + q.toString();
      copy(); tell(T.longReport);
    }
    window.open(url, '_blank', 'noopener');
  });
})();

// + Add a calendar: the presets (United CCS+, Google, Apple, Other) choose the form and its words.
function bindPresets() { each('#addsrc', 'presets', function (menu) {
  menu.querySelectorAll('.preset').forEach(function (b) {
    b.addEventListener('click', function () {
      var p = b.dataset.preset;
      menu.querySelectorAll('.preset').forEach(function (x) { x.setAttribute('aria-checked', String(x === b)); });
      menu.querySelectorAll('.presetform').forEach(function (f) { f.hidden = f.dataset.for.split(' ').indexOf(p) < 0; });
      var feed = menu.querySelector('.presetform[data-for~="other"]');
      if (p !== 'ccs') {
        feed.elements.preset.value = p;
        feed.querySelectorAll('[data-text-' + p + ']').forEach(function (el) { el.textContent = el.getAttribute('data-text-' + p); });
      }
    });
  });
}); }
bindPresets();

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
  // Emoji (0.2.8-beta.15): the field, the common ones, and ☺+ for every emoji (10 a line, a search on top)
  if (t === 'emoji') return '<input type="text" class="aval emoji" maxlength="16" value="' + esc(a.emoji || '') + '" aria-label="' + esc(RD.t.emoji) + '" placeholder="✈️">'
      + '<span class="emojis">' + RD.emoji.map(function (x) { return '<button type="button" class="ghost emo">' + x + '</button>'; }).join('')
      + '<button type="button" class="ghost emomore" aria-expanded="false" title="' + esc(RD.t.moreEmoji) + '" aria-label="' + esc(RD.t.moreEmoji) + '">' + {{ icon("add_reaction", 18)|string|tojson }} + '</button></span>'
      + '<div class="emopick" hidden><input type="search" class="emosearch" placeholder="' + esc(RD.t.searchEmoji) + '" aria-label="' + esc(RD.t.searchEmoji) + '">'
      + '<div class="emogrid" role="listbox" aria-label="' + esc(RD.t.emoji) + '"></div></div>';
  if (t === 'event') {
    var isNew = !a.template, h = '<select class="atpl">' + opts(RD.templates, a.template) + '<option value=""' + (isNew ? ' selected' : '') + '>' + esc(RD.t.newEvent) + '</option></select>';
    if (isNew) h += '<input type="text" class="anew title" maxlength="200" value="' + esc(a.title || '') + '" placeholder="' + esc(RD.t.title) + '">'
      + '<label class="mnote"><input type="checkbox" class="anew allday"' + (a.all_day ? ' checked' : '') + '> ' + esc(RD.t.allDay) + '</label>'
      + '<input type="text" class="anew minutes dur" value="' + hm(a.minutes || 60) + '" title="' + esc(RD.t.length) + '">'
      + '<input type="text" class="anew location" maxlength="200" value="' + esc(a.location || '') + '" placeholder="' + esc(RD.t.location) + '">';
    return h + '<input type="text" class="aoff dur" value="' + hm(a.offset || 0) + '" title="' + esc(RD.t.time) + '"><select class="awhen">' + opts(RD.when, a.when || 'before_start') + '</select>';
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
  rows.forEach(function (row, i) { row.querySelector('.aadd').hidden = i < rows.length - 1; row.querySelector('.adel').hidden = rows.length < 2; });
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
  if (emo) { row.querySelector('.aval.emoji').value = emo.textContent; var pk = row.querySelector('.emopick'); if (pk && !pk.hidden) emoOpen(row, false); }
  if (e.target.closest('.emomore')) { emoOpen(row, row.querySelector('.emopick').hidden); return; }
  var pal = e.target.closest('.pal');
  if (pal) { row.querySelector('.aval').value = pal.dataset.c;
             row.querySelectorAll('.pal').forEach(function (b) { b.setAttribute('aria-checked', String(b === pal)); }); }
});
// Every emoji (0.2.8-beta.15): loaded once, the first time the picker opens
var emojiData = null;
function emoOpen(row, on) {
  var pk = row.querySelector('.emopick'), btn = row.querySelector('.emomore');
  pk.hidden = !on; btn.setAttribute('aria-expanded', String(on));
  if (!on) return;
  (emojiData || (emojiData = fetch('/static/emoji.json?v=' + encodeURIComponent(RD.version), { credentials: 'same-origin' }).then(function (r) { return r.json(); })))
    .then(function (d) { emoDraw(row, d, ''); pk.querySelector('.emosearch').focus(); });
}
function emoDraw(row, d, q) {
  q = q.trim().toLowerCase();
  var grid = row.querySelector('.emogrid'), html = '', last = -1;
  d.emoji.forEach(function (x) {
    if (q && x[1].indexOf(q) < 0) return;
    if (!q && x[2] !== last) { html += '<div class="emogroup">' + esc(d.groups[x[2]]) + '</div>'; last = x[2]; }
    html += '<button type="button" class="ghost emo" title="' + esc(x[1]) + '" role="option">' + esc(x[0]) + '</button>';
  });
  grid.innerHTML = html || '<p class="mnote">' + esc(RD.t.noEmoji) + '</p>';
}
actBox.addEventListener('input', function (e) {
  if (!e.target.matches('.emosearch')) return;
  var row = e.target.closest('.act');
  emojiData.then(function (d) { emoDraw(row, d, e.target.value); });
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
      if (!r.ok) return r.json().catch(function () { return {}; }).then(function (j) { var er = new Error(j.detail || ('HTTP ' + r.status)); er.status = r.status; throw er; });
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
  e.preventDefault();
  var body = new FormData(f), btn = e.submitter, pair = pairFor(f);
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

// Events (F2.2): an open event stays open (also when the calendar is redrawn) until its Close; the
// bell sets its reminders. Clicking an empty part of a day adds an event on that day.
(function () {
  document.addEventListener('click', function (e) {
    var close = e.target.closest('.evclose');
    if (close) { close.closest('details.ev').open = false; return; }
    var day = e.target.closest('.day');
    if (day && !e.target.closest('details.ev, a, button') && day.dataset.add) openEvent(day.dataset.add);
  });
})();
var openEvents = {};
document.addEventListener('toggle', function (e) {
  var d = e.target;
  if (d.matches && d.matches('details.ev') && d.dataset.uid) {
    if (d.open) { openEvents[d.dataset.uid] = 1; fillTools(d); } else delete openEvents[d.dataset.uid];
  }
}, true);
// An opened event gets its tools from #evtoolstpl (0.2.8-beta.4): its reminders, edit and delete
// fitted to it (a rule's event can't be edited or deleted; a hidden one can't be deleted again).
function fillTools(d) {
  var box = d.querySelector('.evtools'), tpl = document.getElementById('evtoolstpl');
  if (!box || !tpl || box.dataset.filled) return;
  var uid = d.dataset.uid, q = encodeURIComponent(uid), month = tpl.dataset.month, origin = box.dataset.origin;
  box.appendChild(tpl.content.cloneNode(true));
  var bell = box.querySelector('.evalarm');
  bell.dataset.uid = uid; bell.dataset.alarms = box.dataset.alarms || '';
  if (box.dataset.alarms) { bell.classList.add('on'); var use = bell.querySelector('use'); if (use) use.setAttribute('href', '#mi-alarm_on'); }
  var edit = box.querySelector('.evedit');
  if (origin === 'rule') edit.remove(); else edit.href = '/event?uid=' + q + '&month=' + month;
  // Link (0.2.8-beta.10): the event's pop-up, opened at "Linked to" (a rule's events can't be linked)
  var lk = box.querySelector('.evlinkto');
  if (origin === 'rule') lk.remove(); else { lk.href = '/event?uid=' + q + '&month=' + month + '&link=1'; if (box.dataset.linked) lk.classList.add('on'); }
  box.querySelector('.evcopy').href = '/event?copy=' + q + '&month=' + month;
  var del = box.querySelector('.evdel');
  if (box.dataset.deleted) { [edit, lk, bell].forEach(function (x) { if (x && x.parentNode) x.remove(); }); }   // deleted: only Restore and Duplicate
  if (origin === 'rule' || box.dataset.hidden) del.remove();
  else { del.elements.uid.value = uid; del.dataset.confirm = origin === 'custom' ? tpl.dataset.delCustom : tpl.dataset.delSource; }
  box.dataset.filled = '1';
  bindConfirm();
}
function reopenEvents() {
  document.querySelectorAll('#cal details.ev').forEach(function (d) { if (openEvents[d.dataset.uid]) d.open = true; });
}

// The event page: in a pop-up on a computer (adding, editing or duplicating an event), the page itself
// on a phone (F1.3). The pop-up tells this page when it's saved; then the calendar is redrawn.
var eventDialog = document.getElementById('eventdialog'), eventFrame = eventDialog.querySelector('iframe');
function narrow() { return window.matchMedia('(max-width: 700px)').matches; }
function openEvent(url) {
  if (narrow()) { location.href = url; return; }
  eventFrame.src = url + (url.indexOf('?') < 0 ? '?' : '&') + 'embed=1';
  eventDialog.showModal();
}
document.addEventListener('click', function (e) {
  var a = e.target.closest('a[href^="/event?"]');
  if (!a || e.ctrlKey || e.metaKey || e.shiftKey || e.button || narrow()) return;
  e.preventDefault(); openEvent(a.getAttribute('href'));
});
window.addEventListener('message', function (e) {
  if (e.origin !== location.origin) return;
  if (e.data === 'calendarstream:event-close') { eventDialog.close(); return; }
  // Link › Rule in the event pop-up (0.2.8-beta.15): its rule, or a new one for it, opens in the rule dialog
  if (e.data && e.data.kind === 'calendarstream:open-rule') { eventDialog.close(); if (RD.rules[e.data.id]) openRule(RD.rules[e.data.id]); return; }
  if (e.data && e.data.kind === 'calendarstream:new-rule') { eventDialog.close(); openRuleFor(e.data.title, e.data.date, e.data.sid); return; }
  if (e.data !== 'calendarstream:event-saved') return;
  eventDialog.close(); eventFrame.src = 'about:blank';
  swapIn(location.href, ['#cal', '#activity', '.box.src .srcright']).then(function () { initCal(); bindAll(); reopenEvents(); });
});
eventDialog.addEventListener('close', function () { eventFrame.src = 'about:blank'; });
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

// Reminders: the bell opens a small list next to it; Save sends it in the background.
(function () {
  var pop = document.getElementById('alarmpop'), form = pop.querySelector('form');
  function close() { pop.hidden = true; }
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.evalarm');
    if (b) {
      var on = (b.dataset.alarms || '').split(','), r = b.getBoundingClientRect();
      form.elements.uid.value = b.dataset.uid;
      form.querySelectorAll('input[name=minutes]').forEach(function (c) { c.checked = on.indexOf(c.value) >= 0; });
      pop.hidden = false;
      pop.style.top = (window.scrollY + r.bottom + 6) + 'px';
      pop.style.left = Math.max(8, Math.min(window.scrollX + r.left - 120, window.scrollX + document.documentElement.clientWidth - pop.offsetWidth - 8)) + 'px';
      return;
    }
    if (!pop.hidden && (e.target.closest('.apcancel') || !pop.contains(e.target))) close();
  });
  form.addEventListener('submit', function () { setTimeout(close, 50); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
  form.addEventListener('change', function () {
    var boxes = form.querySelectorAll('input[name=minutes]:checked');
    form.querySelectorAll('input[name=minutes]:not(:checked)').forEach(function (c) { c.disabled = boxes.length >= 5; });
  });
})();

// Print Preview (F2.1): the choices redraw the preview; Print prints it and remembers the choices.
(function () {
  var dlg = document.getElementById('printdialog'), f = dlg.querySelector('form'), frame = dlg.querySelector('iframe'),
      prefs = PAGE.printPrefs, calView = PAGE.printView, timer = null;
  function pick(group, attr, value) {
    dlg.querySelectorAll(group + ' [data-' + attr + ']').forEach(function (b) { b.setAttribute('aria-checked', String(b.dataset[attr] === value)); });
  }
  function picked(group, attr) { var b = dlg.querySelector(group + ' [aria-checked=true]'); return b ? b.dataset[attr] : ''; }
  function url() {
    var q = new URLSearchParams({ view: picked('.viewpick', 'v'), theme: picked('.themepick', 't'),
                                  weekends: f.elements.weekends.checked ? '1' : '0', start: f.elements.start.value, end: f.elements.end.value,
                                  all: f.querySelector('.rangeall').checked ? '1' : '' });
    return '/print?' + q.toString();
  }
  function refresh() { clearTimeout(timer); timer = setTimeout(function () { frame.src = url(); }, 250); }
  document.addEventListener('click', function (e) {
    if (!e.target.closest('#printbtn')) return;
    var month = document.getElementById('monthpick').dataset.month, y = +month.slice(0, 4), m = +month.slice(5, 7);
    var last = new Date(y, m, 0).getDate();
    f.elements.start.value = month + '-01'; f.elements.end.value = month + '-' + ('0' + last).slice(-2);
    var all = f.querySelector('.rangeall'); all.checked = false; f.querySelectorAll('.daterange input[type=date]').forEach(function (i) { i.readOnly = false; i.classList.remove('off'); });
    pick('.viewpick', 'v', prefs.view || calView); pick('.themepick', 't', prefs.theme || 'light');
    f.elements.weekends.checked = prefs.weekends !== false;
    frame.src = url(); dlg.showModal();
  });
  dlg.querySelectorAll('.viewpick [data-v]').forEach(function (b) { b.addEventListener('click', function () { pick('.viewpick', 'v', b.dataset.v); refresh(); }); });
  dlg.querySelectorAll('.themepick [data-t]').forEach(function (b) { b.addEventListener('click', function () { pick('.themepick', 't', b.dataset.t); refresh(); }); });
  f.addEventListener('change', refresh);
  dlg.querySelector('.ppcancel').addEventListener('click', function () { dlg.close(); });
  dlg.querySelector('.ppprint').addEventListener('click', function () {
    prefs = { view: picked('.viewpick', 'v'), theme: picked('.themepick', 't'), weekends: f.elements.weekends.checked };
    savePref('/ui/print', { view: prefs.view, theme: prefs.theme, weekends: prefs.weekends ? '1' : '0' });
    frame.contentWindow.focus(); frame.contentWindow.print();
  });
})();

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

