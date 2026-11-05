{# (0.2.8-beta.28, F7/F8) Notes under a field while typing, in the standard colors: green when it's good, amber saying why when it isn't.
   Advice only (the server still decides on Save). Now: a feed's stream name (any 1–128 letters, digits, - or _; a whole old link is fine)
   with a strength meter; E-mail addresses (data-note="email"). #}
(function () {
  var N = {
    stream: {{ _('Stream name')|string|tojson }},
    strong: {{ _('Good: hard to guess')|string|tojson }}, fair: {{ _('Fair: longer or more mixed is harder to guess')|string|tojson }},
    weak: {{ _('Weak: easy to guess, make it longer')|string|tojson }},
    bad: {{ _('Only letters, digits, - or _ (up to 128)')|string|tojson }},
    old: {{ _('An old feed link: its stream name is used')|string|tojson }},
    mail: {{ _('Not an e-mail address yet')|string|tojson }}, mailok: {{ _('Looks like an e-mail address')|string|tojson }}
  };
  function noteFor(input, after) {
    var n = input._note;
    if (!n) {
      n = document.createElement('span'); n.className = 'fnote'; n.hidden = true; n.setAttribute('aria-live', 'polite');
      after.parentNode.insertBefore(n, after.nextSibling); input._note = n;
    }
    return n;
  }
  function show(n, ok, text) { n.hidden = !text; n.classList.toggle('good', !!ok); n.textContent = text || ''; }
  function streamNote(input) {
    var v = input.value.trim(), n = noteFor(input, input.closest('.feedlink'));
    if (!v) return show(n, false, '');
    if (/^https?:\/\//i.test(v)) return show(n, true, N.old);
    if (!/^[A-Za-z0-9_-]{1,128}$/.test(v)) return show(n, false, N.bad);
    var kinds = (/[a-z]/.test(v) ? 1 : 0) + (/[A-Z]/.test(v) ? 1 : 0) + (/[0-9]/.test(v) ? 1 : 0) + (/[_-]/.test(v) ? 1 : 0);
    var score = v.length * 1.0 + kinds * 4 - (/(.)\1\1/.test(v) ? 8 : 0);
    if (score >= 26) show(n, true, N.strong);
    else if (score >= 18) show(n, false, N.fair);
    else show(n, false, N.weak);
  }
  function mailNote(input) {
    var v = input.value.trim(), n = noteFor(input, input.closest('.inbox') || input);
    if (!v) return show(n, false, '');
    var ok = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v);
    show(n, ok, ok ? N.mailok : N.mail);
  }
  document.addEventListener('input', function (e) {
    var t = e.target;
    if (!t || !t.matches) return;
    if (t.matches('input.fstream')) streamNote(t);
    else if (t.matches('input[data-note="email"]')) mailNote(t);
  });
})();
