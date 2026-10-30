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

