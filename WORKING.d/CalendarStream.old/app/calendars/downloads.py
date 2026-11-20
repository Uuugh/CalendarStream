"""Holds: Calendar download transports and retry plan.
Depends on: app/calendars/download.py, app/calendars/errors.py, app/calendars/validation.py.
Used by: app/calsync.py.
Reads/writes: HTTP downloads, curl subprocesses, temporary files and monotonic clock.
Dart note: calendar data adapters; inject transports and limits; preserve the compatibility facade.
"""

from __future__ import annotations
import asyncio
import json as _json
import os
import re
import tempfile
import time
from urllib.parse import urljoin, urlparse
from .errors import AuthError, BlockedError, SourceError, NoReplyError
from .download import Download
from .validation import _snippet

# Optional transport availability is captured once, retaining the existing error message on use.
try:
    from curl_cffi import __version__ as cffi_version
    from curl_cffi.requests import AsyncSession
    from curl_cffi.requests import exceptions as cx
except ImportError:
    cffi_version = AsyncSession = cx = None


def ccs_client(client: str | None, *, CCS_CLIENTS) -> str:
    """The CCS+ client in use: the argument, else CCS_CLIENT in .env, else auto (an unknown name is auto too)."""
    name = (client or os.environ.get("CCS_CLIENT", "") or "auto").strip().lower()
    return name if name in CCS_CLIENTS else "auto"


def _q(value: str) -> str:
    """Quote a value for a curl config file."""
    return (
        '"'
        + value.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\n", "")
        .replace("\r", "")
        + '"'
    )


def _parse_headers(raw: str) -> dict:
    """Headers of the final response (curl writes one block per redirect)."""
    blocks = [b for b in re.split(r"\r?\n\r?\n", raw.strip()) if b.strip()]
    headers: dict[str, str] = {}
    for line in (blocks[-1].splitlines()[1:] if blocks else []):
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.strip().lower()] = v.strip()
    return headers


async def curl_version(*, CURL, _curl_version) -> str:
    if not _curl_version:
        try:
            proc = await asyncio.create_subprocess_exec(
                CURL, "--version", stdout=asyncio.subprocess.PIPE
            )
            out, _ = await proc.communicate()
            _curl_version = out.decode().split(" (")[0].strip() or "curl"
        except FileNotFoundError:
            _curl_version = "curl not installed"
    return _curl_version


def _no_reply(host: str, timeout: float, who: str) -> NoReplyError:
    return NoReplyError(
        f"Connected to {host}, but it sent no reply within {int(timeout)} seconds. "
        + (
            "United's bot protection may be holding the request; "
            "use Upload & publish in the CCS+ Calendar Sync box in the meantime."
            if who == "CCS+"
            else "Try again later."
        )
    )


def _not_https(who: str) -> SourceError:
    return SourceError(
        ("The Calendar Sync link" if who == "CCS+" else "The feed link")
        + " must start with https://, and may only redirect to https:// addresses (CalendarStream only downloads over https)."
    )


def _too_many_redirects(host: str, who: str) -> SourceError:
    return SourceError(
        f"{host} redirected too many times; check the "
        + ("Calendar Sync link." if who == "CCS+" else "feed link.")
    )


def _too_large(host: str) -> SourceError:
    return SourceError(
        f"{host} sent more than 5 MB, which is too large for a schedule."
    )


def _finish(
    status: int,
    body: bytes,
    headers: dict,
    debug: dict,
    host: str,
    who: str,
    etag: str,
    last_modified: str,
) -> Download:
    """What a response means, the same for every client: a Download, or the error for it."""
    if status == 304:
        return Download(
            304, not_modified=True, etag=etag, last_modified=last_modified, debug=debug
        )
    if status == 401 and who != "CCS+":
        raise AuthError(
            f"{host} wants a login (HTTP 401). Use the calendar's public or secret .ics "
            "link, which works without one."
        )
    if status == 401:
        raise AuthError(
            "CCS+ rejected the UID or Calendar Sync password (HTTP 401). Check both in "
            "the CCS+ Calendar Sync box (the Calendar Sync password, not your CCS login)."
        )
    if status == 403:
        server = headers.get("server", "")
        ref = re.search(r"Reference\s*#?\s*([\w.]+)", _snippet(body, 1000))
        by = (
            "Akamai (United's bot protection)"
            if "akamai" in server.lower()
            else (server or "the server")
        )
        raise BlockedError(
            f"Access denied by {by}, HTTP 403"
            + (f", reference {ref[1]}" if ref else "")
            + "."
        )
    if status >= 400:
        raise SourceError(
            f"{who} answered HTTP {status}: {_snippet(body, 160) or 'no details'}"
        )
    if b"BEGIN:VCALENDAR" not in body[:2000]:
        raise SourceError(
            f"{who} answered, but not with a calendar file "
            f"({headers.get('content-type', 'unknown type')}): {_snippet(body, 160)}"
        )
    return Download(
        status,
        body=body,
        etag=headers.get("etag", ""),
        last_modified=headers.get("last-modified", ""),
        debug=debug,
    )


async def _download_curl(
    *,
    url: str,
    username: str,
    password: str,
    etag: str,
    last_modified: str,
    timeout: float,
    connect_timeout: float,
    who: str,
    CURL,
    MAX_BYTES,
    MAX_REDIRECTS,
    _KEEP,
    _finish,
    _no_reply,
    _not_https,
    _parse_headers,
    _q,
    _too_large,
    _too_many_redirects,
    curl_version,
) -> Download:
    """The curl program. It identifies itself as curl."""
    host = urlparse(url).hostname or url
    with tempfile.TemporaryDirectory(prefix="calsync-") as tmp:
        body_path, head_path = os.path.join(tmp, "body"), os.path.join(tmp, "headers")
        # Credentials go to curl on stdin (a config file), never on the command line.
        config = [
            f"url = {_q(url)}",
            f'header = {_q("Accept: text/calendar, */*;q=0.5")}',
        ]
        if username:
            config.append(f"user = {_q(f'{username}:{password}')}")
        if etag:
            config.append(f"header = {_q('If-None-Match: ' + etag)}")
        if last_modified:
            config.append(f"header = {_q('If-Modified-Since: ' + last_modified)}")
        # https only (also after redirects), at most 5 redirects and 5 MB, like a hand upload
        args = [
            CURL,
            "--silent",
            "--show-error",
            "--location",
            "--config",
            "-",
            "--proto",
            "=https",
            "--proto-redir",
            "=https",
            "--max-redirs",
            str(MAX_REDIRECTS),
            "--max-filesize",
            str(MAX_BYTES),
            "--connect-timeout",
            str(int(connect_timeout)),
            "--max-time",
            str(int(timeout)),
            "--output",
            body_path,
            "--dump-header",
            head_path,
            "--write-out",
            "%{json}",
        ]
        try:
            proc = await asyncio.create_subprocess_exec(
                *args,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
        except FileNotFoundError:
            raise SourceError(
                "curl isn't installed in this container (it's needed to download calendars)."
            )
        out, err = await proc.communicate(("\n".join(config) + "\n").encode())
        try:
            info = _json.loads(out.decode() or "{}")
        except ValueError:
            info = {}
        body = open(body_path, "rb").read() if os.path.exists(body_path) else b""
        headers = (
            _parse_headers(open(head_path, encoding="latin-1").read())
            if os.path.exists(head_path)
            else {}
        )

    code = proc.returncode
    status = int(info.get("http_code") or info.get("response_code") or 0)
    connected = float(info.get("time_connect") or 0) > 0
    if code == 28:
        if not connected:
            raise SourceError(
                f"Couldn't connect to {host} within {int(connect_timeout)} seconds "
                "(network, DNS or firewall problem on this server)."
            )
        raise _no_reply(host, timeout, who)
    if code == 1:
        raise _not_https(who)
    if code == 47:
        raise _too_many_redirects(host, who)
    if code == 63:
        raise _too_large(host)
    if code in (6, 7):
        raise SourceError(
            f"Couldn't reach {host}: {err.decode().strip() or f'curl error {code}'}"
        )
    if code != 0 and not status:
        raise SourceError(
            f"Download from {host} failed: {err.decode().strip() or f'curl error {code}'}"
        )

    debug = {
        "url": info.get("url_effective", url),
        "status": status,
        "elapsed_s": round(float(info.get("time_total") or 0), 2),
        "bytes": len(body),
        "client": await curl_version(),
        "headers": {k: v for k, v in headers.items() if k in _KEEP},
    }
    return _finish(status, body, headers, debug, host, who, etag, last_modified)


async def _download_browser(
    *,
    url: str,
    username: str,
    password: str,
    etag: str,
    last_modified: str,
    timeout: float,
    connect_timeout: float,
    who: str,
    BROWSER_PROFILE,
    MAX_BYTES,
    MAX_REDIRECTS,
    _KEEP,
    _SESSION_EXTRA,
    _finish,
    _no_reply,
    _not_https,
    _too_large,
    _too_many_redirects,
) -> Download:
    """curl_cffi: a client that presents a current Chrome's connection (TLS and HTTP/2) fingerprint, so
    United's bot protection treats it as a browser. Redirects are followed here, by hand, so that https only,
    five at most and no sign-in sent to another host hold exactly as they do for curl.
    """
    if AsyncSession is None:
        raise SourceError(
            "The browser-like client (curl_cffi) isn't installed in this container."
        )
    host = urlparse(url).hostname or url
    headers = {"Accept": "text/calendar, */*;q=0.5"}
    if etag:
        headers["If-None-Match"] = etag
    if last_modified:
        headers["If-Modified-Since"] = last_modified
    started = time.monotonic()

    async def fetch():
        cur = url
        async with AsyncSession(
            impersonate=BROWSER_PROFILE, **_SESSION_EXTRA
        ) as session:
            for hop in range(MAX_REDIRECTS + 1):
                if urlparse(cur).scheme != "https":
                    raise _not_https(who)
                auth = (
                    (username, password)
                    if username and urlparse(cur).hostname == host
                    else None
                )
                async with session.stream(
                    "GET",
                    cur,
                    headers=headers,
                    auth=auth,
                    allow_redirects=False,
                    timeout=(connect_timeout, timeout),
                ) as resp:
                    status = resp.status_code
                    got = {k.lower(): v for k, v in resp.headers.items()}
                    if status in (301, 302, 303, 307, 308) and got.get("location"):
                        cur = urljoin(cur, got["location"])
                        continue
                    chunks, size = [], 0
                    async for chunk in resp.aiter_content():
                        size += len(chunk)
                        if size > MAX_BYTES:
                            raise _too_large(host)
                        chunks.append(chunk)
                    return cur, status, b"".join(chunks), got
            raise _too_many_redirects(host, who)

    try:
        final, status, body, got = await asyncio.wait_for(fetch(), timeout)
    except (asyncio.TimeoutError, cx.ReadTimeout):
        raise _no_reply(host, timeout, who)
    except cx.ConnectTimeout:
        raise SourceError(
            f"Couldn't connect to {host} within {int(connect_timeout)} seconds "
            "(network, DNS or firewall problem on this server)."
        )
    except cx.Timeout:
        raise _no_reply(host, timeout, who)
    except cx.RequestException as e:
        raise SourceError(
            f"Couldn't reach {host}: {str(e).strip() or type(e).__name__}"
        )
    debug = {
        "url": final,
        "status": status,
        "elapsed_s": round(time.monotonic() - started, 2),
        "bytes": len(body),
        "client": f"curl_cffi {cffi_version}, as {BROWSER_PROFILE}",
        "headers": {k: v for k, v in got.items() if k in _KEEP},
    }
    return _finish(status, body, got, debug, host, who, etag, last_modified)


async def download(
    url: str,
    username: str,
    password: str,
    etag: str,
    last_modified: str,
    timeout: float,
    connect_timeout: float,
    who: str,
    client: str | None,
    *,
    PAUSE_SCALE,
    _PLANS,
    _download_browser,
    _download_curl,
    ccs_client,
    log,
) -> Download:
    """Download a calendar. `username`/`password` are sent with HTTP Basic (CCS+); feeds send none.
    `who` names the server in messages ("CCS+", or the feed's host). `client` picks the CCS+ client (see above;
    default CCS_CLIENT); feeds always use curl, which identifies itself."""
    common = dict(
        url=url,
        username=username,
        password=password,
        etag=etag,
        last_modified=last_modified,
        connect_timeout=connect_timeout,
        who=who,
    )
    if who != "CCS+":
        return await _download_curl(timeout=timeout, **common)
    plan, tried, last = _PLANS[ccs_client(client)], [], None
    for i, (engine, factor, pause) in enumerate(plan):
        if pause and PAUSE_SCALE:
            await asyncio.sleep(pause * PAUSE_SCALE)
        try:
            dl = await (_download_browser if engine == "browser" else _download_curl)(
                timeout=timeout * factor, **common
            )
        except (
            NoReplyError,
            BlockedError,
        ) as e:  # worth trying again, or the next client
            tried.append(
                f"{engine}: {'no reply in %d s' % int(timeout * factor) if isinstance(e, NoReplyError) else 'refused (HTTP 403)'}"
            )
            log.warning("CCS+ download, %s: %s", tried[-1], e)
            last = e
            continue
        tried.append(f"{engine}: HTTP {dl.status}")
        if dl.debug is not None:
            dl.debug["tried"] = tried
        if len(tried) > 1:
            log.info("CCS+ download answered after %s", "; ".join(tried))
        return dl
    raise last
