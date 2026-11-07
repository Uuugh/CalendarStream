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
// --- 0.2.8-beta.29: the calendar's top line, key, full page, stretch and hourly grid (F15, F26, F27, F28) --------------------
// F15.1: the tools sit right of the date with a space between them; when they don't fit, they go under the top line,
// right-aligned, and the + stays in the top right corner.
function fitCalHead() {
  var head = document.querySelector('#cal .calhead');
  if (!head) return;
  head.classList.remove('two');
  var l = head.querySelector('.calleft'), r = head.querySelector('.calright'), p = head.querySelector('.calplus');
  head.classList.toggle('two', l.scrollWidth + r.scrollWidth + p.offsetWidth + 36 > head.clientWidth);
}
// F15.3: From and To are hints inside the search line's date fields, written in the date's format (the browser's).
function dateFormatHint() {
  try {
    return new Intl.DateTimeFormat(navigator.language).formatToParts(new Date(2000, 10, 22)).map(function (p) {
      return p.type === 'day' ? 'dd' : p.type === 'month' ? 'mm' : p.type === 'year' ? 'yyyy' : p.value;
    }).join('').replace(/\s+/g, '');
  } catch (e) { return 'yyyy-mm-dd'; }
}
function initHints() {
  var fmt = dateFormatHint();
  document.querySelectorAll('#calsearch .hinted .fld').forEach(function (lab) {
    var span = lab.querySelector('span'), inp = lab.querySelector('input');
    if (!span || !inp) return;
    lab.dataset.hint = span.textContent.trim() + ' ' + fmt;
    var mark = function () { inp.dataset.empty = inp.value ? '' : '1'; };
    mark(); inp.addEventListener('input', mark); inp.addEventListener('change', mark);
  });
}
// F15.9: Week and Day open at the first events (or 7 am).
function scrollHours() {
  var hs = document.querySelector('#cal .hscroll');
  if (!hs) return;
  var hh = (hs.querySelector('.hlab') || {}).offsetHeight || 44, top = 7 * hh;
  hs.querySelectorAll('.ev.timed').forEach(function (e) { top = Math.min(top, e.offsetTop - hh / 2); });
  hs.scrollTop = Math.max(0, top);
}
// F15.8: the key's columns run three tall; when they don't fit across, every column grows a row taller (--rows).
function fitKey() {
  document.querySelectorAll('#cal .legcols').forEach(function (list) {
    var n = list.children.length, rows = 3;
    if (!n) return;
    list.style.setProperty('--rows', String(rows));
    while (rows < n && list.scrollWidth > list.clientWidth + 10) list.style.setProperty('--rows', String(++rows));
  });
}
// F27: full page fills the browser. The month keeps each day at most 2:3 (2 wide for 3 tall); past that, weeks are
// added: first a week of the next month, then of the previous month, alternately, until the page is full.
function fitFull() {
  var cal = document.getElementById('cal'), body = document.getElementById('calbody');
  if (!cal || !body || !cal.classList.contains('full')) return;
  var legend = cal.querySelector('.legend');
  var avail = Math.max(260, window.innerHeight - body.getBoundingClientRect().top - (legend ? legend.offsetHeight : 0) - 36);   // (beta.31, I14: 28 left the page 4 px too tall)
  var view = body.dataset.view, month = body.querySelector('.month');
  if (view === 'month' && month) {
    var extras = {}, base = 0;
    month.querySelectorAll('.day').forEach(function (d) {
      var x = d.dataset.x;
      if (x) (extras[x] = extras[x] || []).push(d); else base++;
    });
    base = base / 7;
    var w = month.clientWidth / 7, dow = month.querySelector('.dow'), head = dow ? dow.offsetHeight : 0;
    var rows = Math.max(base, Math.ceil((avail - head) / (1.5 * w)));
    var order = [];
    for (var k = 1; k <= 6; k++) order.push('n' + k, 'p' + k);
    var want = rows - base;
    order.forEach(function (x, i) { (extras[x] || []).forEach(function (d) { d.hidden = i >= want; }); });
    var shown = base + Math.min(want, order.length);
    month.style.gridTemplateRows = 'auto repeat(' + shown + ', minmax(0, 1fr))';
    month.style.height = avail + 'px';
  } else if (body.querySelector('.hscroll')) {
    var hs = body.querySelector('.hscroll'), above = hs.getBoundingClientRect().top - body.getBoundingClientRect().top;
    hs.style.maxHeight = Math.max(200, avail - above) + 'px';
  } else {
    body.style.maxHeight = avail + 'px'; body.style.overflow = 'auto';
  }
}
(function () {
  var t = null;
  window.addEventListener('resize', function () { clearTimeout(t); t = setTimeout(function () { fitCalHead(); fitKey(); fitFull(); }, 80); });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { fitCalHead(); fitKey(); fitFull(); });
  // F15.4: Full page hides every other section (and becomes Back); the calendar is drawn again with the weeks it needs.
  document.addEventListener('click', function (e) {
    var fb = e.target.closest('#fullbtn');
    if (fb) {
      var to = fb.getAttribute('aria-pressed') !== 'true';
      savePref('/ui/calview', { full: to ? '1' : '0' }, function () {
        document.body.classList.toggle('calfull', to);
        // (0.2.8-beta.31, F34, F35) the button is in the title bar now, outside the calendar: change it here
        fb.setAttribute('aria-pressed', String(to));
        var tt = to ? fb.dataset.backTitle : fb.dataset.fullTitle;
        fb.title = tt; fb.setAttribute('aria-label', tt);
        var use = fb.querySelector('use'); if (use) use.setAttribute('href', '#mi-' + (to ? 'filter_none' : 'fullscreen'));
        loadCal(location.href);
      });
      return;
    }
    // F15.9, F28: a click on a key item dims it and hides its events here only, in every mode (0.2.8-beta.33, F48);
    // leaving full page (if that's where it was clicked) shows them again just the same
    var it = e.target.closest('#cal .legitem[data-hide]');
    if (it) {
      var off = it.getAttribute('aria-pressed') === 'true';
      it.setAttribute('aria-pressed', String(!off)); it.classList.toggle('dim', off);
      var keys = Array.prototype.map.call(document.querySelectorAll('#cal .legitem.dim[data-hide]'), function (x) { return x.dataset.hide; });
      savePref('/ui/calview', { hide: keys.join(',') || '-' }, function () { loadCal(location.href); });   // (beta.31, I15: '-' = none; an empty value is not sent)
      return;
    }
    // F50: View All clears every dimmed Calendars/Key item at once
    if (e.target.closest('#legviewall')) {
      savePref('/ui/calview', { hide: '-' }, function () { loadCal(location.href); });
    }
  });
  // F15.7: the stretch handle in the calendar's lower left corner: drag (or ↑ ↓) to make the calendar taller or shorter
  var drag = null, saver = null;
  function stretch(cal, px) { px = Math.max(0, Math.min(1200, Math.round(px))); cal.style.setProperty('--st', px + 'px'); return px; }
  function remember(px) { clearTimeout(saver); saver = setTimeout(function () { savePref('/ui/calview', { stretch: String(px) }); }, 400); }
  document.addEventListener('pointerdown', function (e) {
    var h = e.target.closest('#calstretch');
    if (!h) return;
    var cal = h.closest('#cal');
    drag = { y: e.clientY, st: parseFloat(getComputedStyle(cal).getPropertyValue('--st')) || 0, cal: cal, now: null };
    if (h.setPointerCapture) h.setPointerCapture(e.pointerId);
    e.preventDefault();
  });
  document.addEventListener('pointermove', function (e) { if (drag) drag.now = stretch(drag.cal, drag.st + (e.clientY - drag.y)); });
  document.addEventListener('pointerup', function () { if (drag && drag.now !== null) remember(drag.now); drag = null; });
  // (0.2.8-beta.31, I20) the hour-height handle left of the times: drag (or ↑ ↓) to make each hour shorter or taller
  var hdrag = null, hsaver = null;
  function hourSet(view, px) { px = Math.max(20, Math.min(120, Math.round(px))); view.style.setProperty('--hhu', px + 'px');
    var g = view.querySelector('#hourgrip'); if (g) g.setAttribute('aria-valuenow', String(px)); return px; }
  function hourKeep(px) { clearTimeout(hsaver); hsaver = setTimeout(function () { savePref('/ui/calview', { hour: String(px) }); }, 400); }
  document.addEventListener('pointerdown', function (e) {
    var g = e.target.closest('#hourgrip'); if (!g) return;
    var v = g.closest('.hourview');
    hdrag = { y: e.clientY, h: parseFloat(g.getAttribute('aria-valuenow')) || 44, v: v, now: null };
    if (g.setPointerCapture) g.setPointerCapture(e.pointerId);
    e.preventDefault();
  });
  document.addEventListener('pointermove', function (e) { if (hdrag) hdrag.now = hourSet(hdrag.v, hdrag.h + (e.clientY - hdrag.y) / 6); });
  document.addEventListener('pointerup', function () { if (hdrag && hdrag.now !== null) hourKeep(hdrag.now); hdrag = null; });
  document.addEventListener('keydown', function (e) {
    var g = e.target.closest && e.target.closest('#hourgrip');
    if (!g || (e.key !== 'ArrowDown' && e.key !== 'ArrowUp')) return;
    var v = g.closest('.hourview'), now = parseFloat(g.getAttribute('aria-valuenow')) || 44;
    e.preventDefault(); hourKeep(hourSet(v, now + (e.key === 'ArrowDown' ? 4 : -4)));
  });
  document.addEventListener('keydown', function (e) {
    var h = e.target.closest && e.target.closest('#calstretch');
    if (!h || (e.key !== 'ArrowDown' && e.key !== 'ArrowUp')) return;
    var cal = h.closest('#cal'), now = parseFloat(getComputedStyle(cal).getPropertyValue('--st')) || 0;
    e.preventDefault(); remember(stretch(cal, now + (e.key === 'ArrowDown' ? 24 : -24)));
  });
})();

function initCal() {
  // The 12h / 24h switch: the only place the time format is set (times elsewhere change too, so the
  // page is drawn again).
  var sw = document.getElementById('clockswitch');
  if (sw) sw.addEventListener('click', function () {
    var to24 = sw.getAttribute('aria-checked') !== 'true';
    sw.setAttribute('aria-checked', String(to24));
    savePref('/ui/clock', { clock: to24 ? '24' : '12' }, function () { location.reload(); });
  });
  // The view (0.2.8-beta.29, F15.6; 0.2.8-beta.33, F52: icons, not words - a button + menu, like ☰ Settings).
  // #cal (with #viewbtn/#viewmenu inside it) is swapped in fresh on every view or month change, so the
  // outside-click/Escape listeners are bound to document ONCE (by id, re-read each time they fire) instead of
  // piling up a pair per swap; the button and its options still get plain per-swap listeners, which die with
  // the old nodes they're on.
  var vbtn = document.getElementById('viewbtn'), vmenu = document.getElementById('viewmenu');
  if (vbtn && vmenu) {
    function closeView() { var m = document.getElementById('viewmenu'), b = document.getElementById('viewbtn'); if (m) m.hidden = true; if (b) b.setAttribute('aria-expanded', 'false'); }
    vbtn.addEventListener('click', function (e) { e.stopPropagation(); var open = vmenu.hidden; closeView(); if (open) { vmenu.hidden = false; vbtn.setAttribute('aria-expanded', 'true'); } });
    vmenu.querySelectorAll('[data-view]').forEach(function (b) {
      b.addEventListener('click', function () { closeView(); chooseView(b.dataset.view); });
    });
    if (!initCal._viewDocBound) {
      initCal._viewDocBound = true;
      document.addEventListener('click', function (e) {
        var m = document.getElementById('viewmenu'), b = document.getElementById('viewbtn');
        if (m && !m.hidden && !m.contains(e.target) && e.target !== b) closeView();
      });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeView(); });
    }
  }
  // The time zone (this page only).
  var sel = document.getElementById('tzpick');
  if (sel) sel.addEventListener('change', function () { savePref('/ui/tz', { tz: sel.value }, function () { loadCal(location.href); }); });
  fitCalHead(); initHints(); scrollHours(); fitKey(); fitFull();
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
// F40: a horizontal swipe on the calendar grid moves to the next or previous period (left = next, right =
// previous), the same as ‹ ›; vertical scrolling is left untouched (no preventDefault, measured on release).
(function () {
  var sx = 0, sy = 0, tracking = false;
  document.addEventListener('touchstart', function (e) {
    tracking = !!e.target.closest('#calbody') && e.touches.length === 1;
    if (tracking) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }
  }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (!tracking) return;
    tracking = false;
    var t = e.changedTouches[0], dx = t.clientX - sx, dy = t.clientY - sy;
    if (Math.abs(dx) < 50 || Math.abs(dx) < Math.abs(dy) * 1.5) return;   // too short, or more vertical than horizontal
    var links = Array.prototype.filter.call(document.querySelectorAll('#cal .calhead a.navbtn'), function (a) { return !a.classList.contains('wide'); });
    var a = dx > 0 ? links[0] : links[1];   // swipe right -> previous (links[0]); swipe left -> next (links[1])
    if (a) loadCal(a.href);
  }, { passive: true });
})();

