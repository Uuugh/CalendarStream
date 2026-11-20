"""Holds: administrator.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations


def admin_email(*, EMAIL_RE, store) -> str:
    """The administrator's e-mail address (☰ Settings), or "". Shown in the Google setup guide as
    the support / contact e-mail and the test user. Checked again on the way out (it goes into the page).
    """
    email = str(store.get("admin_email") or "")
    return email if EMAIL_RE.match(email) and len(email) <= 254 else ""
