"""Holds: invites.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
import secrets


def _invites(*, now, store) -> dict:
    now_ = now().timestamp()
    found = {
        t: v
        for t, v in (store.get("google_invites") or {}).items()
        if v.get("expires", 0) > now_
    }
    return found


def make_invite(
    d: dict, account: str | None, *, INVITE_DAYS, _invites, now, state, store
) -> str:
    """(0.2.8-beta.34, review #9 finding 1) `account` is the Google account the invited person will sign in as;
    the module keeps its own (`from`) until they have, so an invite nobody finishes costs the module nothing.
    """
    found = _invites()
    found = {
        t: v for t, v in found.items() if v["did"] != d["id"]
    }  # one live invite per module
    token = secrets.token_urlsafe(24)
    found[token] = {
        "did": d["id"],
        "account": account or d["account"],
        "from": d["account"],
        "expires": now().timestamp() + INVITE_DAYS * 86400,
    }
    store.set("google_invites", found)
    state.record(
        "info",
        f"Google, {d['name']}: invite made (works once, for {INVITE_DAYS} days)",
        kind="Google",
    )
    return token


def forget_invites(did: str, *, _invites, store):
    store.set(
        "google_invites", {t: v for t, v in _invites().items() if v["did"] != did}
    )
