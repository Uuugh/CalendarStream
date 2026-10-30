// Feeds (0.2.8-beta.17)
(function () {
  // + › step 1 picks the module (F7); step 2 is that module in a pop-up. The account line is the same for both
  // Google modules; Information & Instructions is each one's own.
  function showKind(type) {
    var d2 = document.getElementById('adddest2'), f = document.getElementById('adddest');
    if (!d2 || !f) return;
    var group = type === 'feed' ? 'feed' : 'google', info = type === 'google' ? 'google2' : type;
    f.elements.type.value = type;
    var k = d2.querySelector('.addkind'); k.textContent = k.dataset[type] || k.textContent;
    d2.querySelectorAll('.addfor').forEach(function (b) {
      var on = b.dataset.for === group || b.dataset.for === info;
      b.hidden = !on;
      b.querySelectorAll('input, select, button').forEach(function (x) { x.disabled = !on; });
    });
  }
  document.addEventListener('click', function (e) {
    var t = e.target.closest ? e.target : null; if (!t) return;
    var pick = t.closest('.pickdest');
    if (pick && !pick.disabled) {
      document.getElementById('adddestpop').close();
      showKind(pick.dataset.type);
      var d2 = document.getElementById('adddest2'); addDefaults(); d2.showModal();
      var n = d2.querySelector('.nameinput'); if (n) n.focus();
      return;
    }
    if (t.closest('.adddestback')) {
      document.getElementById('adddest2').close();
      document.getElementById('adddestpop').showModal();
      return;
    }
    // The feed link's copy (F10): address + /calendar/ + stream name + .ics, as now typed
    var cp = t.closest('.feedcopy');
    if (cp) {
      var fl = cp.closest('.feedlink'), st = fl.querySelector('.fstream');
      if (!st.value.trim()) { st.focus(); return; }
      copyText(fl.querySelector('.fbase').value + '/calendar/' + st.value.trim() + '.ics', cp);
      return;
    }
    // Send to… (F6): e-mail, a text message, the device's share menu, or copy
    var sb = t.closest('.sendbtn');
    if (sb) {
      var menu = sb.parentNode.querySelector('.sendmenu'), open = menu.hidden;
      closeSend();
      if (open) {
        menu.hidden = false; sb.setAttribute('aria-expanded', 'true');
        menu.querySelector('.sendshare').hidden = !navigator.share;
      }
      return;
    }
    var sh = t.closest('.sendshare');
    if (sh) {
      var b = sh.closest('.sendto').querySelector('.sendbtn');
      navigator.share({ title: b.dataset.title, text: b.dataset.text, url: b.dataset.url }).catch(function () {});
      closeSend(); return;
    }
    var sc = t.closest('.sendcopy');
    if (sc) { copyText(sc.closest('.sendto').querySelector('.sendbtn').dataset.url, sc); setTimeout(closeSend, 1200); return; }
    if (!t.closest('.sendmenu')) closeSend();
    // ☰ Settings › More addresses (F11): + adds a row; the trash takes one out (Save keeps it)
    var add = t.closest('.extraadd');
    if (add) {
      var form = add.closest('form'), rows = form.querySelector('.extrarows');
      rows.appendChild(form.querySelector('.extratpl').content.cloneNode(true));
      rows.lastElementChild.querySelector('input').focus();
      return;
    }
    var del = t.closest('.extradel');
    if (del) del.closest('.extrarow').remove();
  });
  function closeSend() {
    document.querySelectorAll('.sendmenu:not([hidden])').forEach(function (m) {
      m.hidden = true; m.parentNode.querySelector('.sendbtn').setAttribute('aria-expanded', 'false');
    });
  }
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeSend(); });
  // The address drop-down's last choice, + Add a domain, opens ☰ Settings › Public address
  document.addEventListener('focusin', function (e) { if (e.target.matches && e.target.matches('.fbase')) e.target.dataset.was = e.target.value; });
  document.addEventListener('change', function (e) {
    var s = e.target;
    if (!s.matches || !s.matches('.fbase') || s.value !== '+add') return;
    s.value = s.dataset.was || (s.options[0] && s.options[0].value) || '';
    location.href = '/?menu=settings#public';
  });
  // (0.2.8-beta.23, F13.2) Label and Notes show, in grey, what they take when left empty: the top calendar the
  // feed includes (one that comes from somewhere, not Local, when there is one) and that calendar's note
  function addDefaults() {
    var f = document.getElementById('adddest'); if (!f) return;
    var on = Array.prototype.filter.call(f.querySelectorAll('input[name=sources]'), function (x) { return x.checked; });
    var top = on.filter(function (x) { return !x.dataset.local; })[0] || on[0];
    var n = f.querySelector('.nameinput'), o = f.querySelector('.noteinput');
    if (n) n.placeholder = top && top.dataset.name ? top.dataset.name : n.dataset.default;
    if (o) o.placeholder = top && top.dataset.note ? top.dataset.note : o.dataset.default;
  }
  document.addEventListener('change', function (e) {
    if (e.target.name === 'sources' && e.target.form && e.target.form.id === 'adddest') addDefaults();
  });
  // Enter in the add pop-up is Save (not Connect me, the form's first button)
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Enter' || !e.target.form || e.target.form.id !== 'adddest' || e.target.tagName !== 'INPUT') return;
    e.preventDefault(); e.target.form.requestSubmit(e.target.form.querySelector('.psave'));
  });
  // Cancel in the add pop-up starts it over: Calendar Feed, nothing typed
  document.addEventListener('close', function (e) {
    if (e.target.id === 'adddest2') { var f = document.getElementById('adddest'); f.reset(); clearFix(f); addDefaults(); }
  }, true);
})();

// (0.2.8-beta.21, F5.3) An Include box's calendars: three a column, then another column; when no other column
// fits, every column grows taller instead (--rows). Kept up to date as the box changes width or is redrawn.
(function () {
  function rows(list) {
    var items = list.querySelectorAll('.srcpick'), n = items.length;
    if (!n) return;
    var gap = parseFloat(getComputedStyle(list).columnGap) || 0, widest = 0;
    items.forEach(function (x) { widest = Math.max(widest, x.getBoundingClientRect().width); });
    var fit = Math.max(1, Math.floor((list.clientWidth + gap) / (widest + gap)));
    var want = String(Math.max(3, Math.ceil(n / fit)));
    if (list.style.getPropertyValue('--rows') !== want) list.style.setProperty('--rows', want);
  }
  var seen = typeof ResizeObserver === 'function' ? new ResizeObserver(function (all) { all.forEach(function (e) { rows(e.target); }); }) : null;
  function watch() {
    document.querySelectorAll('.feedinclude .srcpicks').forEach(function (list) {
      if (list.dataset.rows) return;
      list.dataset.rows = '1';
      if (seen) seen.observe(list); else rows(list);
    });
  }
  watch();
  new MutationObserver(watch).observe(document.body, { childList: true, subtree: true });
})();

