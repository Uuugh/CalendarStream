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
    if (mod && pal.dataset.c) mod.style.setProperty('--mc', pal.dataset.c);   // (0.2.8-beta.24, F7) its border and tints follow
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
  // (0.2.8-beta.19, F7) a Google module's first Sync Now: its tab opens now, at the click, so no pop-up blocker
  // stops it; it shows "Making the calendar…" and then Google Calendar
  var btn = f.querySelector('.syncnow[data-gopen]');
  if (btn) {
    var w = window.open(btn.dataset.gopen, '_blank');
    if (w) w.opener = null;
    btn.removeAttribute('data-gopen');
  }
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
    box.style.setProperty('--mc', val.dataset.default);
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

