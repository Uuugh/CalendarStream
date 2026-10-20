"""Settings loaded from environment variables (populated from .env by docker compose)."""
import os
import secrets
from urllib.parse import quote
from dataclasses import dataclass, field
from pathlib import Path


def _env(name: str, default: str = "") -> str:
    return os.environ.get(name, default).strip()


def _secret(env_name: str, secret_name: str, strip_all: bool = True) -> str:
    """Read a credential from (in order): <ENV>_FILE, /run/secrets/<secret_name>, or <ENV>."""
    candidates = [_env(f"{env_name}_FILE"), f"/run/secrets/{secret_name}"]
    for path in candidates:
        if path and os.path.isfile(path):
            try:
                raw = Path(path).read_text()
            except PermissionError:
                if not os.environ.get(env_name):  # the entrypoint normally passes it on as env
                    print(f"WARNING: secret file {path} isn't readable and {env_name} is not set")
                continue
            # Usernames: trim all whitespace. Passwords: only drop the trailing newline an editor adds.
            return raw.strip() if strip_all else raw.rstrip("\r\n")
    return os.environ.get(env_name, "").strip() if strip_all else os.environ.get(env_name, "").rstrip("\r\n")


def _public_url() -> str:
    url = (_env("PUBLIC_URL") or _env("PUBLIC_BASE_URL")).rstrip("/")
    if url and "://" not in url:
        url = "https://" + url   # allow "ccs.example.com"
    return url


DEFAULT_CALENDAR_URL = "https://ccsplus.ual.com/calendarsyncapi/api/Calendar/GetCalendar"


@dataclass
class Settings:
    # CCS+ Calendar Sync sign-in (HTTP Basic). Docker secrets CCS_USER / CCS_PASSWORD win over .env.
    #   username = your UID;  password = the Calendar Sync password created in CCS+ (not your CCS login)
    username: str = field(default_factory=lambda: _secret("CCS_USERNAME", "CCS_USER"))
    password: str = field(default_factory=lambda: _secret("CCS_PASSWORD", "CCS_PASSWORD", strip_all=False))
    # The link from CCS+ "Copy link". Can also be set on the status page (saved in the database,
    # where it takes priority over this value).
    calendar_url: str = field(default_factory=lambda: _env("CCS_CALENDAR_URL", DEFAULT_CALENDAR_URL))

    # Behaviour
    interval_minutes: int = field(default_factory=lambda: max(15, int(_env("SYNC_INTERVAL_MINUTES",
                                                                       _env("SCRAPE_INTERVAL_MINUTES", "60")))))
    timezone: str = field(default_factory=lambda: _env("TZ", "America/Chicago"))
    calendar_name: str = field(default_factory=lambda: _env("CALENDAR_NAME", "United CCS Schedule"))
    # Items with a start time but no end time: a number of hours, or "allday"
    default_event_raw: str = field(default_factory=lambda: _env("DEFAULT_EVENT_HOURS", "1").lower())
    default_event_type: str = "hours"
    default_event_hours: float = 1.0
    # Timed events lasting exactly 24 h (or 48 h, 72 h…) are shown as all-day events
    allday_24h: bool = field(default_factory=lambda: _env("ALLDAY_24H", "true").lower() not in ("0", "false", "no", "off"))

    # Feed / GUI security
    feed_token: str = field(default_factory=lambda: _env("FEED_TOKEN"))
    # Status-page login: Docker secrets GUI_USER / GUI_PASSWORD (USER.txt / PASSWORD.txt) take priority.
    gui_user: str = field(default_factory=lambda: _secret("GUI_USERNAME", "GUI_USER"))
    gui_password: str = field(default_factory=lambda: _secret("GUI_PASSWORD", "GUI_PASSWORD", strip_all=False))
    public_base_url: str = field(default_factory=_public_url)

    # Postgres (all project data lives here). Password: Docker secret DB_PASSWORD (DB_PASSWORD.txt).
    db_host: str = field(default_factory=lambda: _env("DB_HOST", "calendar_stream_db"))
    db_port: str = field(default_factory=lambda: _env("DB_PORT", "5432"))
    db_name: str = field(default_factory=lambda: _env("DB_NAME", "calendar_stream"))
    db_user: str = field(default_factory=lambda: _env("DB_USER", "ccs"))
    db_password: str = field(default_factory=lambda: _secret("DB_PASSWORD", "DB_PASSWORD", strip_all=False))

    # Google Calendar sync (optional): the OAuth client from Google Cloud, as Docker secrets
    # GOOGLE_CLIENT_ID / GOOGLE_CLIENT_SECRET (GOOGLE_CLIENT_ID.txt / GOOGLE_CLIENT_SECRET.txt).
    google_client_id: str = field(default_factory=lambda: _secret("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_ID"))
    google_client_secret: str = field(default_factory=lambda: _secret("GOOGLE_CLIENT_SECRET", "GOOGLE_CLIENT_SECRET"))

    def __post_init__(self):
        self.gui_user = self.gui_user or "admin"
        if not self.gui_password:
            print("WARNING: no status-page password (GUI_PASSWORD secret / .env) - the status page is open to anyone who can reach it")
        raw = self.default_event_raw.replace(" ", "")
        if raw in ("allday", "all-day", "all_day", "fullday", "full-day", "day"):
            self.default_event_type = "allday"
        else:
            try:
                self.default_event_hours = float(raw.rstrip("h") or 1)
                if self.default_event_hours <= 0:
                    raise ValueError
            except ValueError:
                print(f"WARNING: DEFAULT_EVENT_HOURS={self.default_event_raw!r} not recognised; using 1 hour")
                self.default_event_hours = 1.0
        if not self.db_password:
            print("WARNING: no database password (DB_PASSWORD secret / .env)")

    @property
    def dsn(self) -> str:
        return (f"postgresql://{quote(self.db_user, safe='')}:{quote(self.db_password, safe='')}"
                f"@{self.db_host}:{self.db_port}/{quote(self.db_name, safe='')}")

    def resolve_feed_token(self, store):
        """FEED_TOKEN in .env wins; otherwise use the one saved in the database, creating it once."""
        if self.feed_token:
            return
        self.feed_token = store.get("feed_token")
        if not self.feed_token:
            self.feed_token = secrets.token_urlsafe(24)
            store.set("feed_token", self.feed_token)

    @property
    def configured(self) -> bool:
        return bool(self.username and self.password)


settings = Settings()
