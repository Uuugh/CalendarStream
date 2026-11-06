// (0.2.8-beta.26, F23; 0.2.8-beta.27, I10; 0.2.8-beta.32, I21; 0.2.8-beta.33, I21/F45) A status word (icon and
// words) shows in full for a moment, then, outside a Status/Action button, shrinks (collapses) to just its icon,
// gently (not with reduced motion); the word stays as the icon's tooltip and accessible name. The Status/Action buttons
// (every .statusbox: Healthy, Up to date, Connected, Read by Google, the counts) always keep icon and words together:
// only the words shown elsewhere (a login block's word, a message) collapse. Then, unless it's an ongoing health
// check to keep (something that can become unhealthy, e.g. CCS+ or a feed's "Validated"; marked data-fold-vanish="0"
// or simply not marked), it vanishes entirely too, giving the freed space back to its line (a plain one-off
// confirmation such as History's "Saved" is marked data-fold-vanish="1" and goes all the way). How long each step
// holds follows the Animation duration setting (--anim-d; HOLD_BASE at its default of 1).
// (F20) A section or module left open folds again after 24 hours: the server does it at the next page load (main.section_state);
// a page left open that long does it here, counting from when it first saw it open.
(function () {
  var HOLD_BASE = 2400, seen = typeof WeakSet === 'function' ? new WeakSet() : null;
  function hold() {
    var d = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--anim-d'));
    return HOLD_BASE * (isNaN(d) || d <= 0 ? 1 : d);
  }
  function shrink(el) {
    var word = (el.querySelector('.chiptext') || el).textContent.replace(/\s+/g, ' ').trim();
    if (word && !el.getAttribute('aria-label')) el.setAttribute('aria-label', word);
    el.classList.add('shrunk');
  }
  function vanish(el) {
    el.classList.add('gone');
    setTimeout(function () { if (document.body.contains(el)) el.hidden = true; }, 450);
  }
  function scan() {
    document.querySelectorAll('.chip.good, .okmark').forEach(function (el) {
      if (el.closest('.statusbox, .countbox') || (seen && seen.has(el))) return;
      if (seen) seen.add(el);
      el.classList.remove('shrunk'); el.classList.remove('gone'); el.hidden = false;
      var slot = el.closest('.okslot'), doVanish = slot && slot.getAttribute('data-fold-vanish') === '1';
      setTimeout(function () {
        if (!document.body.contains(el)) return;
        shrink(el);
        if (doVanish) setTimeout(function () { if (document.body.contains(el)) vanish(el); }, hold());
      }, hold());
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
