// Events (F2.2): an open event stays open (also when the calendar is redrawn) until its Close; the
// bell sets its reminders. Clicking an empty part of a day adds an event on that day.
(function () {
  document.addEventListener('click', function (e) {
    var close = e.target.closest('.evclose');
    if (close) { close.closest('details.ev').open = false; return; }
    var day = e.target.closest('.day');
    if (day && !e.target.closest('details.ev, a, button') && day.dataset.add) openEvent(day.dataset.add);
  });
})();
var openEvents = {};
document.addEventListener('toggle', function (e) {
  var d = e.target;
  if (d.matches && d.matches('details.ev') && d.dataset.uid) {
    if (d.open) { openEvents[d.dataset.uid] = 1; fillTools(d); } else delete openEvents[d.dataset.uid];
  }
}, true);
// An opened event gets its tools from #evtoolstpl (0.2.8-beta.4): its reminders, edit and delete
// fitted to it (a rule's event can't be edited or deleted; a hidden one can't be deleted again).
function fillTools(d) {
  var box = d.querySelector('.evtools'), tpl = document.getElementById('evtoolstpl');
  if (!box || !tpl || box.dataset.filled) return;
  var uid = d.dataset.uid, q = encodeURIComponent(uid), month = tpl.dataset.month, origin = box.dataset.origin;
  box.appendChild(tpl.content.cloneNode(true));
  var bell = box.querySelector('.evalarm');
  bell.dataset.uid = uid; bell.dataset.alarms = box.dataset.alarms || '';
  if (box.dataset.alarms) { bell.classList.add('on'); var use = bell.querySelector('use'); if (use) use.setAttribute('href', '#mi-alarm_on'); }
  var edit = box.querySelector('.evedit');
  if (origin === 'rule') edit.remove(); else edit.href = '/event?uid=' + q + '&month=' + month;
  // Link (0.2.8-beta.10): the event's pop-up, opened at "Linked to" (a rule's events can't be linked)
  var lk = box.querySelector('.evlinkto');
  if (origin === 'rule') lk.remove(); else { lk.href = '/event?uid=' + q + '&month=' + month + '&link=1'; if (box.dataset.linked) lk.classList.add('on'); }
  box.querySelector('.evcopy').href = '/event?copy=' + q + '&month=' + month;
  var del = box.querySelector('.evdel');
  if (box.dataset.deleted) { [edit, lk, bell].forEach(function (x) { if (x && x.parentNode) x.remove(); }); }   // deleted: only Restore and Duplicate
  if (origin === 'rule' || box.dataset.hidden) del.remove();
  else { del.elements.uid.value = uid; del.dataset.confirm = origin === 'custom' ? tpl.dataset.delCustom : tpl.dataset.delSource; }
  box.dataset.filled = '1';
  bindConfirm();
}
function reopenEvents() {
  document.querySelectorAll('#cal details.ev').forEach(function (d) { if (openEvents[d.dataset.uid]) d.open = true; });
}

// The event page: in a pop-up on a computer (adding, editing or duplicating an event), the page itself
// on a phone (F1.3). The pop-up tells this page when it's saved; then the calendar is redrawn.
var eventDialog = document.getElementById('eventdialog'), eventFrame = eventDialog.querySelector('iframe');
function narrow() { return window.matchMedia('(max-width: 700px)').matches; }
function openEvent(url) {
  if (narrow()) { location.href = url; return; }
  eventFrame.style.height = '';      // (F11) until the page says how tall it is
  eventFrame.src = url + (url.indexOf('?') < 0 ? '?' : '&') + 'embed=1';
  eventDialog.showModal();
}
document.addEventListener('click', function (e) {
  var a = e.target.closest('a[href^="/event?"]');
  if (!a || e.ctrlKey || e.metaKey || e.shiftKey || e.button || narrow()) return;
  e.preventDefault(); openEvent(a.getAttribute('href'));
});
window.addEventListener('message', function (e) {
  if (e.origin !== location.origin) return;
  if (e.data === 'calendarstream:event-close') { eventDialog.close(); return; }
  // (0.2.8-beta.22, F11) the event page's height: the pop-up fits it, up to the window; Print: Print Preview on its day
  if (e.data && e.data.kind === 'calendarstream:event-size' && e.source === eventFrame.contentWindow) { eventFrame.style.height = (+e.data.height || 0) + 'px'; return; }
  if (e.data && e.data.kind === 'calendarstream:print') { if (window.openPrintDay) window.openPrintDay(e.data.date); return; }
  // Link › Rule in the event pop-up (0.2.8-beta.15): its rule, or a new one for it, opens in the rule dialog
  if (e.data && e.data.kind === 'calendarstream:open-rule') { eventDialog.close(); if (RD.rules[e.data.id]) openRule(RD.rules[e.data.id]); return; }
  if (e.data && e.data.kind === 'calendarstream:new-rule') { eventDialog.close(); openRuleFor(e.data.title, e.data.date, e.data.sid); return; }
  if (e.data !== 'calendarstream:event-saved') return;
  eventDialog.close(); eventFrame.src = 'about:blank';
  swapIn(location.href, ['#cal', '#activity', '.box.src .srcright']).then(function () { initCal(); bindAll(); reopenEvents(); });
});
eventDialog.addEventListener('close', function () { eventFrame.src = 'about:blank'; });
