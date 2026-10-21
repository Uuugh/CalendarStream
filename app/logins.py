"""The two logins, both kept in the database and set on the status page:

- the CCS+ Calendar Sync login (UID + Calendar Sync password, the password encrypted), used to
  download the schedule;
- the status-page login (user name + password, the password hashed), created on the first visit.

Until 0.1.2 both came from Docker secret files; if those values are still passed in, they are
imported once.
"""
from __future__ import annotations

import hashlib
import hmac
import re
import secrets

from .secretbox import SecretBox, check_password, hash_password

UID_RE = re.compile(r"^[A-Za-z0-9._@-]{2,64}$")
MIN_PASSWORD = 8


class LoginError(ValueError):
    """A value entered on the status page isn't acceptable; the message says why."""


class Logins:
    def __init__(self, store, box: SecretBox):
        self.store = store
        self.box = box
        self._ccs: tuple[str, str] | None = None
        self._ok: set[bytes] = set()     # recently accepted page logins, so each request skips scrypt
        # Shown in the container log until the status-page login is created; the first-visit form
        # asks for it, so only someone who can read the log can claim a new install.
        self.setup_code: str | None = None

    # --- CCS+ Calendar Sync login ---------------------------------------------------

    def ccs(self) -> tuple[str, str]:
        """(UID, Calendar Sync password), or ("", "") parts not set yet."""
        if self._ccs is None:
            saved = self.store.get("ccs_login") or {}
            password = ""
            if saved.get("password"):
                try:
                    password = self.box.unseal(saved["password"])
                except ValueError:
                    password = ""     # DB_PASSWORD changed: it has to be entered again
            self._ccs = (saved.get("uid", ""), password)
        return self._ccs

    @property
    def ccs_configured(self) -> bool:
        return all(self.ccs())

    def save_ccs(self, uid: str, password: str):
        """Save the CCS+ login. A blank password keeps the saved one (it's never shown again)."""
        uid = uid.strip()
        if not UID_RE.match(uid):
            raise LoginError("Enter your UID (letters and digits, e.g. U123456).")
        password = password.rstrip("\r\n")
        if not password:
            password = self.ccs()[1]
            if not password:
                raise LoginError("Enter the Calendar Sync password too.")
        if len(password) > 200:
            raise LoginError("That password is too long.")
        self.store.set("ccs_login", {"uid": uid, "password": self.box.seal(password)})
        self._ccs = None

    def clear_ccs(self):
        """Forget the CCS+ login (when CCS+ is removed as a calendar source)."""
        self.store.delete("ccs_login")
        self._ccs = None

    # --- Status-page login -----------------------------------------------------------

    def page_login(self) -> dict | None:
        return self.store.get("page_login")

    @property
    def has_page_login(self) -> bool:
        return bool(self.page_login())

    @property
    def page_user(self) -> str:
        return (self.page_login() or {}).get("user", "")

    def set_page_login(self, user: str, password: str, confirm: str | None = None):
        user = user.strip()
        if not user or len(user) > 64 or any(c.isspace() or c == ":" for c in user):
            raise LoginError("Choose a user name without spaces or colons.")
        if len(password) < MIN_PASSWORD:
            raise LoginError(f"Choose a password of at least {MIN_PASSWORD} characters.")
        if confirm is not None and password != confirm:
            raise LoginError("The two passwords don't match.")
        self.store.set("page_login", {"user": user, "password": hash_password(password)})
        self._ok.clear()
        self.setup_code = None

    def check_page_login(self, user: str, password: str) -> bool:
        saved = self.page_login()
        if not saved:
            return False
        # A keyed digest of what was accepted, so a correct login doesn't cost an scrypt every request.
        key = hmac.new(saved["password"]["hash"].encode(), f"{user}\0{password}".encode(), hashlib.sha256).digest()
        if key in self._ok:
            return True
        good = hmac.compare_digest(user.encode(), saved["user"].encode()) & check_password(password, saved["password"])
        if good:
            if len(self._ok) > 50:
                self._ok.clear()
            self._ok.add(key)
        return good

    def new_setup_code(self) -> str:
        code = secrets.token_hex(4).upper()
        self.setup_code = f"{code[:4]}-{code[4:]}"
        return self.setup_code

    def check_setup_code(self, code: str) -> bool:
        given = code.strip().upper().replace(" ", "")
        if len(given) == 8:
            given = f"{given[:4]}-{given[4:]}"
        return bool(self.setup_code) and hmac.compare_digest(given.encode(), self.setup_code.encode())

    # --- Moving from the old secret files ---------------------------------------------

    def import_old(self, ccs_user: str, ccs_password: str, gui_user: str, gui_password: str) -> list[str]:
        """Copy logins still passed in from the pre-0.1.3 secret files, once, when none is saved."""
        done = []
        if ccs_user and ccs_password and not self.store.get("ccs_login"):
            try:
                self.save_ccs(ccs_user, ccs_password)
                done.append("the CCS+ UID and Calendar Sync password")
            except LoginError:
                pass
        if gui_password and not self.has_page_login:
            self.store.set("page_login", {"user": gui_user or "admin", "password": hash_password(gui_password)})
            done.append("the status-page login")
        return done
