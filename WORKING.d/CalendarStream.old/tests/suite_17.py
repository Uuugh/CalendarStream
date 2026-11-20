"""0.1.5 tests: languages."""
import json, os, re, sys, html
os.environ.update(DB_HOST=os.environ.get("TEST_DB_HOST", "127.0.0.1"), DB_PORT=os.environ.get("TEST_DB_PORT", "5432"), DB_NAME=sys.argv[1], DB_USER=os.environ.get("TEST_DB_USER", "ccs"), DB_PASSWORD=os.environ.get("TEST_DB_PASSWORD", "testpw"),
                  GUI_USERNAME="t", GUI_PASSWORD="password1", TZ="America/New_York", PUBLIC_URL="https://cal.example.com",
                  CCS_USERNAME="U123456", CCS_PASSWORD="pw")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch
from fastapi.testclient import TestClient
from app import main, i18n
A = ("t", "password1"); fails = 0
def ok(c, label):
    global fails; fails += not c; print(("PASS " if c else "FAIL ") + label)
async def noop(*a, **k): pass
REAL = os.path.join(HERE, "data", "Demo.ics")
with patch.object(main, "loop", noop), patch.object(main, "google_loop", noop), TestClient(main.app) as c:
    p = c.get("/", auth=A).text; csrf = re.search(r'name="csrf" value="([^"]+)"', p)[1]
    c.post("/setup/upload", auth=A, data={"csrf": csrf}, files={"file": ("Calendar.ics", open(REAL, "rb").read())})
    c.post("/feed/name", auth=A, data={"csrf": csrf, "name": "United CCS Schedule", "tag": ["RDO"], "tag_color": ["#d50000"], "tag_mode": ["word"], "tag_case": [""]})
    c.post("/setup/interval", auth=A, data={"csrf": csrf, "minutes": "30"})
    ok('<html lang="en"' in p and 'id="langbtn"' in p and p.index('id="langbtn"') < p.index('data-theme-choice="light"'), "globe left of the theme switch; English by default")
    ok(c.get("/", auth=A, headers={"Accept-Language": "fr-FR,fr;q=0.9"}).text.count('<html lang="fr"') == 1, "Automatic follows the browser (French)")
    ok('<html lang="nl-BE"' in c.get("/", auth=A, headers={"Accept-Language": "nl-BE"}).text, "Flemish from nl-BE")
    ok('<html lang="en"' in c.get("/", auth=A, headers={"Accept-Language": "ja"}).text, "unknown browser language → English")
    english_bits = ["Activity log", "Sync now", "Status &amp; setup", "Public address", "How to turn on Calendar Sync",
                    "Shareable subscribe page", "Previous month", "events in feed", "Schedule received"]
    for lang in ("es", "fr", "de", "pt", "nl"):
        r = c.post("/ui/lang", auth=A, data={"csrf": csrf, "lang": lang}); assert r.status_code == 204
        page = c.get("/?month=2026-10", auth=A, headers={"Accept-Language": "en"}).text
        visible = re.sub(r"<style>.*?</style>", "", page, flags=re.S)
        left = [b for b in english_bits if b in visible]
        cat = i18n.CATALOGS[lang]
        month = i18n.Dates(lang).title(__import__("datetime").date(2026, 10, 1))
        ok(f'<html lang="{i18n.HTML_LANG[lang]}"' in page and not left and month in page, f"{lang}: page translated ({month}); English left: {left}")
        logs = [h["msg"] for h in main.store.recent_log(20)]
        tr = [i18n.message(lang, m) for m in logs]
        same = [m for m, t in zip(logs, tr) if m == t]
        ok(not same, f"{lang}: activity log translated ({len(logs) - len(same)}/{len(logs)}) {same[:2]}")
        status = i18n.message(lang, main.state.message)
        ok(status != main.state.message, f"{lang}: status → {status[:70]}")
        e = c.get("/event?uid=" + main.store.load_events()[0].uid.replace("@", "%40"), auth=A).text
        ok(cat["Edit United event"] in html.unescape(e) or cat["Edit event"] in html.unescape(e), f"{lang}: event editor translated")
        err = c.post("/setup/interval", auth=A, data={"csrf": csrf, "minutes": "5"}, headers={"Accept": "text/html"})
        ok(err.status_code == 400 and html.unescape(cat["Choose between {n} and {n2} minutes."].format(n=15, n2=1440)) in html.unescape(err.text), f"{lang}: error page translated")
    c.post("/ui/lang", auth=A, data={"csrf": csrf, "lang": "auto"})
    ok(main.store.get("ui_lang") is None and '<html lang="de"' in c.get("/", auth=A, headers={"Accept-Language": "de"}).text, "Automatic again")
    ok(c.post("/ui/lang", auth=A, data={"csrf": csrf, "lang": "xx"}).status_code == 400, "unknown language refused")
    s = c.get(f"/subscribe/{main.settings.feed_token}", headers={"Accept-Language": "pt-BR"}).text
    ok('<html lang="pt-BR"' in s and "Passo a passo" in s, "subscribe page in the visitor's language")
    ok(c.post("/setup/interval", auth=A, data={"csrf": csrf, "minutes": "5"}).headers["content-type"].startswith("application/json"), "API-style requests still get JSON errors")
    # Messages with parts: nested translation
    m = "Google: 3 added, 1 updated, calendar renamed (more at the next sync)"
    ok(i18n.message("es", m) == "Google: 3 añadidos, 1 actualizados, calendario renombrado (más en la próxima sincronización)", "nested message: " + i18n.message("es", m))
    m = "Download failed: Couldn't connect to ccsplus.ual.com within 10 seconds (network, DNS or firewall problem on this server)."
    ok(i18n.message("de", m).startswith("Download fehlgeschlagen: Keine Verbindung zu ccsplus.ual.com innerhalb von 10 Sekunden"), "nested error: " + i18n.message("de", m)[:80])
    ok(i18n.message("fr", 'Edited "UA 122 EWR-LHR" (2026-10-07)') == "« UA 122 EWR-LHR » (2026-10-07) modifié", "titles kept as they are")
    ok(i18n.message("es", "some brand-new message") == "some brand-new message", "unknown message stays English")
    # Script and menu text: injection-safe
    ok("<script>" not in i18n.tr("es", "Signed in as <b>{user}</b> · change", user="<script>"), "values are escaped")
print("FAILED:", fails) if fails else print("ALL PASSED")
