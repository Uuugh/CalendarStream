// (0.2.8-beta.26, F23; 0.2.8-beta.27, I10) A good login word ("Signed in", "Validated", a connection status inside a module) shows
// its word for a moment, then shrinks to just its ✓, gently (not with reduced motion). The word stays as the ✓'s tooltip and
// accessible name. The Status/Action buttons (every .statusbox: Healthy, Up to date, Connected, Read by Google, the counts) never
// lose a word: only the login blocks shrink.
// (F20) A section or module left open folds again after 24 hours: the server does it at the next page load (main.section_state);
// a page left open that long does it here, counting from when it first saw it open.
(function () {
  var HOLD = 2400, seen = typeof WeakSet === 'function' ? new WeakSet() : null;
  function shrink(el) {
    var word = (el.querySelector('.chiptext') || el).textContent.replace(/\s+/g, ' ').trim();
    if (word && !el.getAttribute('aria-label')) el.setAttribute('aria-label', word);
    el.classList.add('shrunk');
  }
  function scan() {
    document.querySelectorAll('.chip.good, .okmark').forEach(function (el) {
      if (el.closest('.statusbox, .countbox') || (seen && seen.has(el))) return;
      if (seen) seen.add(el);
      el.classList.remove('shrunk');
      setTimeout(function () { if (document.body.contains(el)) shrink(el); }, HOLD);
    });
  }
  var t = null;
  new MutationObserver(function () { clearTimeout(t); t = setTimeout(scan, 80); }).observe(document.body, { childList: true, subtree: true });
  scan();
  setInterval(function () {
    var now = Date.now();
    document.querySelectorAll('.modsection.open, .module.cfgopen').forEach(function (el) {
      if (!el.dataset.seenOpen) { el.dataset.seenOpen = String(now); return; }
      if (now - Number(el.dataset.seenOpen) > 24 * 3600 * 1000) { var b = el.querySelector(':scope > .cfgline .cfgtoggle'); if (b) b.click(); delete el.dataset.seenOpen; }
    });
    document.querySelectorAll('.modsection:not(.open), .module:not(.cfgopen)').forEach(function (el) { delete el.dataset.seenOpen; });
  }, 60000);
})();
