// Save a status-page preference in the database (so every browser and login matches).
// Fire-and-forget unless a callback is given: if it fails, the page still works.
// A view setting saved at once (review #7.2): `then` runs only once it's saved; a refusal or a lost connection
// says so in a pop-up, and the page stays as it is.
function savePref(path, fields, then) {
  var body = new URLSearchParams(Object.assign({ csrf: CSRF }, fields));
  fetch(path, { method: 'POST', body: body, credentials: 'same-origin' })
    .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); if (then) then(); })
    .catch(function () { tell(T.prefFailed); });
}
var CSRF = PAGE.csrf;

// (0.2.8-beta.21, F4) An (i) or (?) pop-up opens with its upper left at the icon. Past the window's right edge, its
// upper right sits at that edge instead; past the bottom, its lower corners sit at the bottom. In a pop-up, the
// pop-up's edges count as the window's.
function placeTip(dot) {
  var tip = dot && dot.querySelector('.helptip');
  if (!tip) return;
  tip.style.left = '0px'; tip.style.right = 'auto'; tip.style.bottom = 'auto'; tip.style.transform = 'none';
  tip.style.top = 'calc(100% + 6px)';
  var r = tip.getBoundingClientRect();
  if (!r.width) return;
  var w = document.documentElement.clientWidth, h = document.documentElement.clientHeight;
  // inside a pop-up, its edges are the window's: what's past them is hidden in the pop-up's scrolling
  var box = dot.closest('dialog[open]');
  if (box) {
    var b = box.getBoundingClientRect(), cs = getComputedStyle(box);
    w = Math.min(w, b.right - parseFloat(cs.borderRightWidth)); h = Math.min(h, b.bottom - parseFloat(cs.borderBottomWidth));
  }
  if (r.right > w) tip.style.left = Math.round(w - r.right) + 'px';
  if (r.bottom > h) tip.style.top = 'calc(100% + 6px + ' + Math.round(h - r.bottom) + 'px)';
}
['mouseover', 'focusin'].forEach(function (type) {
  document.addEventListener(type, function (e) {
    var dot = e.target.closest && e.target.closest('.helpdot');
    if (dot && !(e.relatedTarget && dot.contains(e.relatedTarget))) placeTip(dot);
  });
});

// (?): hovering or focusing shows the explanation; a click (or tap) keeps it open until a click
// elsewhere or Escape. Delegated, so it also works in sections swapped in after a save.
document.addEventListener('click', function (e) {
  var dot = e.target.closest('.helpdot');
  document.querySelectorAll('.helpdot.open').forEach(function (d) { if (d !== dot) { d.classList.remove('open'); d.setAttribute('aria-expanded', 'false'); } });
  if (!dot || e.target.closest('.helptip')) return;
  e.preventDefault(); e.stopPropagation();
  var on = !dot.classList.contains('open');
  dot.classList.toggle('open', on); dot.setAttribute('aria-expanded', String(on));
  if (on) placeTip(dot);
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
          if (step[0] === 'go') { btn.dataset.state = 'done'; setTimeout(function () { location.href = j.url || '/?menu=settings#googlesync'; }, 400); return; }
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

