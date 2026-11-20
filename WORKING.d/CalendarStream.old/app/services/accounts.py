"""Holds: accounts.
Depends on: app/gsync.py. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
from ..gsync import Google


def google_for(
    account: str, *, Google, _accounts, box, google_traffic, settings, store
) -> Google:
    """A Google account's connection (0.2.8-beta.15: each Google module can use its own Gmail; they share
    the OAuth client). "" is the first one."""
    if account not in _accounts:
        _accounts[account] = Google(
            store, box, settings.timezone, account, traffic=google_traffic
        )
    return _accounts[account]


def dest_google(d: dict, *, Google, google_for) -> Google:
    return google_for(d.get("account", ""))


def google_accounts(*, destinations) -> list[str]:
    """The accounts in use: the first, and any a Google module uses."""
    return list(
        dict.fromkeys([""] + [d.get("account", "") for d in destinations("google")])
    )


def _shared_grant(g: Google, *, Google, google_accounts, google_for) -> bool:
    """Another account here is signed in with the same Gmail (0.2.8-beta.17, I5). Google keeps one grant per
    Gmail, so revoking this sign-in would sign the other out too: it's only forgotten here.
    """
    email = (g.info().get("email") or "").lower()
    return bool(email) and any(
        x is not g and x.connected and (x.info().get("email") or "").lower() == email
        for x in [google_for(a) for a in google_accounts()]
    )
