{# The status page's script (0.2.8-beta.4): one file per version and language, cached by the browser.
   What changes from page to page (the form token, the view…) comes from #pagedata. #}
var PAGE = JSON.parse(document.getElementById('pagedata').textContent);
// Texts used by the scripts below, in the page's language.
var T = {
  copied: {{ _('Copied')|string|tojson }}, gSaving: {{ _('Saving…')|string|tojson }}, gChecking: {{ _('Checking…')|string|tojson }}, gAddress: {{ _('Checking address…')|string|tojson }}, gOpening: {{ _('Connecting…')|string|tojson }}, stepAuto: {{ _('Ticks itself when CalendarStream can confirm it')|string|tojson }}, stepDone: {{ _('Step done')|string|tojson }}, pressCtrlC: {{ _('Press Ctrl+C')|string|tojson }},
  saved: {{ _('Saved')|string|tojson }}, verifying: {{ _('Verifying…')|string|tojson }},
  validated: {{ _('Validated')|string|tojson }}, verifyFailed: {{ _('Failed')|string|tojson }},
  disconnect: {{ _('Disconnect Google Calendar?')|string|tojson }},
  downloading: {{ _('Downloading…')|string|tojson }}, restarting: {{ _('Restarting…')|string|tojson }},
  updateFailed: {{ _('Update failed')|string|tojson }}, updated: {{ _('Updated')|string|tojson }}, updateSlow: {{ _('It’s taking longer than expected; check the updater container’s log.')|string|tojson }},
  syncing: {{ _('Syncing…')|string|tojson }}, saving: {{ _('Saving…')|string|tojson }},
  copiedReport: {{ _('Report copied')|string|tojson }}, longReport: {{ _('The report is long, so GitHub gets the start of it; the whole report is copied: paste it into the issue.')|string|tojson }},
  alreadyHere: {{ _('Already in this calendar ({n} of {total})')|string|tojson }},
  failed: {{ _('Failed')|string|tojson }}, prefFailed: {{ _('That setting wasn’t saved: CalendarStream couldn’t be reached, or refused it. Try again.')|string|tojson }}, ok: {{ _('OK')|string|tojson }}, cancel: {{ _('Cancel')|string|tojson }}, yes: {{ _('Yes')|string|tojson }}
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

