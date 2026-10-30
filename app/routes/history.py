"""History: Undo / Redo, how many changes are kept, and the container's log.

Part of app/main.py until 0.2.8-beta.20 (F12): the code is unchanged, only moved. The app, shared state
and helpers are in main.py (imported here); names the tests replace on main are read as core.<name>."""
from __future__ import annotations

from fastapi import Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse, Response

from ..main import (_is_async, after_restore, app, check_csrf, gui_auth, log, LOG_TAIL, mark_deleted, pop_undo,
    state, store, UNDO_KEEP, unmark_deleted)


@app.post("/history/undo", dependencies=[Depends(gui_auth)])
async def history_undo(request: Request, csrf: str = Form(""), entry: int = Form(0), redo: str = Form("")):
    """Undo (or redo) a change from History (0.2.8-beta.15): a stack, so it's always the newest change
    that's undone first, and the oldest undone one that's redone first."""
    check_csrf(csrf)
    top, nxt = store.undo_stack()
    if entry != (nxt if redo else top):
        raise HTTPException(400, "Newer changes come first: undo (or redo) the one with the arrow.")
    found = store.undo_entry(entry)
    if not found:
        raise HTTPException(404, "That change can't be undone any more.")
    undo = found["undo"]
    if undo.get("type") == "deleted":
        for uid in undo["uids"]:
            if redo:
                e = store.get_event(uid)
                if e:
                    mark_deleted(e, undo["where"])
            else:
                unmark_deleted(uid)
        after_restore()
    else:
        store.restore(undo["after" if redo else "before"])
        after_restore()
    store.set_undo_state(entry, "done" if redo else "undone")
    log.info("%s: %s", "Redone" if redo else "Undone", found["msg"])
    return {"ok": True} if _is_async(request) else RedirectResponse("/#activity", status_code=303)


@app.get("/history/container", dependencies=[Depends(gui_auth)])
def container_log():
    """History › Container log (0.2.8-beta.15): what `docker logs` shows for CalendarStream since it started
    (its last LOG_TAIL_LINES lines), newest last. (An admin's page once there are several users.)"""
    return Response("\n".join(LOG_TAIL.lines) + "\n", media_type="text/plain; charset=utf-8")


@app.post("/history/keep", dependencies=[Depends(gui_auth)])
async def history_keep(request: Request, csrf: str = Form(""), keep: int = Form(UNDO_KEEP)):
    """How many changes History remembers for Undo (1–200)."""
    check_csrf(csrf)
    if not 1 <= keep <= 200:
        raise HTTPException(400, "Between 1 and 200 changes.")
    store.set("undo_keep", keep)
    pop_undo()
    state.record("info", f"History remembers the last {keep} changes for Undo", kind="Settings")
    return {"ok": True} if _is_async(request) else RedirectResponse("/#activity", status_code=303)
