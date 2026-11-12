// (F59) Beta: Google Traffic — while the section is open, poll the calls CalendarStream made to Google and
// show them, newest first; each row expands to its full request and response (nothing redacted). Clear empties
// the log (it's never saved, so Clear just starts it fresh).
(function () {
  var sec = document.getElementById('beta');
  if (!sec) return;
  var list = document.getElementById('betalist'), empty = document.getElementById('betaempty'),
      clearBtn = document.getElementById('betaclear'), copyBtn = document.getElementById('betacopy');
  var openIds = {};   // which rows are expanded, kept across a refresh (by their position: see renderRow)
  var lastEntries = [];   // the entries currently shown, for Copy all (0.2.8-beta.42, troubleshooting)

  function row(e, i) {
    var id = 'betadetail-' + i;
    var li = document.createElement('li'); li.className = 'betaentry';
    var open = !!openIds[i];
    var when = new Date(e.at * 1000);
    var statusCls = (typeof e.status === 'number' && e.status < 400) ? 'good' : (e.status === 'error' || e.status >= 400 ? 'bad' : '');
    li.innerHTML = '<button type="button" aria-expanded="' + open + '" aria-controls="' + id + '">' +
      '<span class="betatime">' + when.toLocaleTimeString() + '</span>' +
      '<span class="betamethod">' + e.method + '</span>' +
      '<span class="betaurl">' + e.url + '</span>' +
      '<span class="betastatus ' + statusCls + '">' + e.status + '</span></button>' +
      '<div class="betadetail" id="' + id + '"' + (open ? '' : ' hidden') + '>' +
      '<pre>' + reqText(e) + '</pre><pre>' + respText(e) + '</pre></div>';
    li.querySelector('button').addEventListener('click', function () {
      var now = !open; openIds[i] = now;
      var d = li.querySelector('.betadetail'); d.hidden = !now;
      li.querySelector('button').setAttribute('aria-expanded', String(now));
    });
    return li;
  }
  function headers(h) { return Object.keys(h || {}).map(function (k) { return k + ': ' + h[k]; }).join('\n'); }
  function reqText(e) { return '→ ' + e.method + ' ' + e.url + (e.ms ? ' (' + e.ms + ' ms)' : '') +
    (headers(e.request_headers) ? '\n' + headers(e.request_headers) : '') + (e.request_body ? '\n\n' + e.request_body : ''); }
  function respText(e) { return '← ' + e.status + (headers(e.response_headers) ? '\n' + headers(e.response_headers) : '') +
    (e.response_body ? '\n\n' + e.response_body : ''); }

  function render(entries) {
    lastEntries = entries;
    list.innerHTML = '';
    entries.forEach(function (e, i) { list.appendChild(row(e, i)); });
    empty.hidden = entries.length > 0;
  }
  // Copy all: every entry currently shown (not just the expanded ones), full request and response, newest
  // first (the order shown), one click to the clipboard for pasting into a bug report.
  copyBtn.addEventListener('click', function () {
    var text = lastEntries.map(function (e) { return reqText(e) + '\n' + respText(e); }).join('\n\n----------\n\n');
    copyText(text || empty.textContent, copyBtn);
  });
  function refresh() {
    if (!sec.classList.contains('open')) return;
    fetch('/google/traffic', { cache: 'no-store', credentials: 'same-origin' })
      .then(function (r) { return r.ok ? r.json() : { entries: [] }; })
      .then(function (j) { render(j.entries || []); })
      .catch(function () {});
  }
  clearBtn.addEventListener('click', function () {
    openIds = {};
    fetch('/google/traffic/clear', { method: 'POST', body: new URLSearchParams({ csrf: CSRF }), credentials: 'same-origin' })
      .then(refresh).catch(function () { tell(T.prefFailed); });
  });
  refresh();
  setInterval(refresh, 2000);
})();
