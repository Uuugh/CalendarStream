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

