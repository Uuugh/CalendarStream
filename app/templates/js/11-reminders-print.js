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
  var oneDay = false;     // opened from an event (F11.1): its day, in the Day view; Print doesn't keep that view
  function open(start, end, view) {
    f.elements.start.value = start; f.elements.end.value = end;
    var all = f.querySelector('.rangeall'); all.checked = false; f.querySelectorAll('.daterange input[type=date]').forEach(function (i) { i.readOnly = false; i.classList.remove('off'); });
    pick('.viewpick', 'v', view); pick('.themepick', 't', prefs.theme || 'light');
    f.elements.weekends.checked = prefs.weekends !== false;
    frame.src = url(); dlg.showModal();
  }
  document.addEventListener('click', function (e) {
    if (!e.target.closest('#printbtn')) return;
    var month = document.getElementById('monthpick').dataset.month, y = +month.slice(0, 4), m = +month.slice(5, 7);
    var last = new Date(y, m, 0).getDate();
    oneDay = false; open(month + '-01', month + '-' + ('0' + last).slice(-2), prefs.view || calView);
  });
  window.openPrintDay = function (day) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(day || '')) return;
    oneDay = true; open(day, day, 'day');
  };
  // The event page on its own (a phone): its Print comes back here with ?print=<day>
  var askedDay = new URLSearchParams(location.search).get('print');
  if (askedDay) window.openPrintDay(askedDay);
  dlg.querySelectorAll('.viewpick [data-v]').forEach(function (b) { b.addEventListener('click', function () { pick('.viewpick', 'v', b.dataset.v); refresh(); }); });
  dlg.querySelectorAll('.themepick [data-t]').forEach(function (b) { b.addEventListener('click', function () { pick('.themepick', 't', b.dataset.t); refresh(); }); });
  f.addEventListener('change', refresh);
  dlg.querySelector('.ppcancel').addEventListener('click', function () { dlg.close(); });
  dlg.querySelector('.ppprint').addEventListener('click', function () {
    prefs = { view: oneDay && picked('.viewpick', 'v') === 'day' ? (prefs.view || calView) : picked('.viewpick', 'v'), theme: picked('.themepick', 't'), weekends: f.elements.weekends.checked };
    savePref('/ui/print', { view: prefs.view, theme: prefs.theme, weekends: prefs.weekends ? '1' : '0' });
    frame.contentWindow.focus(); frame.contentWindow.print();
  });
})();

