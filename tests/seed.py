"""The made-up demo setup used by the screenshot scripts and some tests (0.2.8 rules)."""
import asyncio, json, os
HERE = os.path.dirname(os.path.abspath(__file__))


def rule(c, csrf, title="", conds=(), actions=(), apply="all"):
    r = c.post("/rules/save", data={"csrf": csrf, "rule": json.dumps({"title": title, "conds": list(conds), "actions": list(actions), "apply": apply})},
               headers={"X-CS-Async": "1"})
    assert r.status_code == 200, r.text
    return r.json()["id"]


def text(value, op="word"):
    return {"type": "text", "op": op, "value": value}


def demo(c, csrf, main, feed_url="https://example.org/work.ics"):
    c.post("/sources/add", data={"csrf": csrf, "type": "ccs"})
    main.logins.save_ccs("U123456", "pw12345"); main.state.last_auth_ok = True
    c.post("/setup/upload", data={"csrf": csrf}, files={"file": ("Calendar.ics", open(os.path.join(HERE, "data", "Demo.ics"), "rb").read())})
    main.state.status = "ok"
    c.post("/sources/add", data={"csrf": csrf, "type": "ics", "url": feed_url, "name": "Work"})
    sid = [x for x in main.source_ids() if x.startswith("f")][0]
    main.store.set(f"calendar_color:{sid}", "#8e24aa")
    asyncio.run(main.run_feed(sid))
    c.post("/templates", data={"csrf": csrf, "tpl_id": ["", ""], "tpl_title": ["Drive to the airport", "Day off"], "tpl_kind": ["timed", "allday"],
                               "tpl_duration": ["1:30", ""], "tpl_location": ["EWR", ""], "tpl_color": ["#616161", ""]})
    tid = main.event_templates()[0]["id"]
    rule(c, csrf, "", [text("RDO")], [{"type": "color", "color": "#d50000"}], ["ccs"])
    rule(c, csrf, "Drive to the airport", [text("EWR", "contains")], [{"type": "event", "template": tid, "when": "before_start", "offset": 120}], ["ccs"])
    rule(c, csrf, "", [text("VAC")], [{"type": "color", "color": "#0b8043"}, {"type": "emoji", "emoji": "🏝️"}])
    rule(c, csrf, "", [text("SIM")], [{"type": "color", "color": "#8e24aa"}], [])
    # Google Calendar sync set up first, so + Google Calendar makes a Google calendar (0.2.8-beta.4)
    main.store.set("google_client", {"id": "123-abc.apps.googleusercontent.com", "secret": main.google._seal("s"),
                                     "check": {"ok": True, "message": "", "at": "2026-10-20T20:00:00+00:00", "redirect_ok": True}})
    main.google._client = None
    c.post("/destinations/add", data={"csrf": csrf, "type": "google", "name": "Flying", "public": "https://cal.example.com"})
    c.post("/destinations/update", data={"csrf": csrf, "did": main.destinations("google")[0]["id"], "name": "Flying", "sources": ["ccs"]})
    c.post("/destinations/add", data={"csrf": csrf, "type": "feed", "name": "Everything"})
    return sid
