"""Log in to CCS with a headless Chromium and capture the schedule page.

The page sits behind United's login (often an SSO redirect), so a real browser is
used. Cookies are saved in the database (kv "session") so most runs skip the login entirely.
What the browser saw on the last run is saved to the debug_files table for tuning.
"""
from __future__ import annotations

import json
import logging
import re
import time
from dataclasses import dataclass, field
from urllib.parse import urlparse

from playwright.async_api import async_playwright, Page, TimeoutError as PWTimeout

from .config import Settings

log = logging.getLogger("ccs.scraper")

USER_SELECTORS = [
    "input[type=email]",
    "input[name*=user i]", "input[id*=user i]",
    "input[name*=login i]", "input[id*=login i]",
    "input[name*=employee i]", "input[id*=employee i]",
    "input[name=identifier]", "input[name=loginfmt]",
    "input[type=text]",
]
PASS_SELECTORS = ["input[type=password]"]
SUBMIT_SELECTORS = [
    "button[type=submit]", "input[type=submit]",
    "button:has-text('Sign in')", "button:has-text('Log in')", "button:has-text('Login')",
    "button:has-text('Next')", "button:has-text('Continue')",
]
MFA_HINTS = ["verification code", "one-time", "authenticator", "approve sign in",
             "approve the request", "enter code", "multi-factor", "two-factor", "push notification"]
FAIL_HINTS = ["incorrect", "invalid", "not recognized", "failed", "locked", "try again", "wrong password"]


class SiteUnreachable(Exception):
    pass


async def _settle(page: Page, idle_ms: int = 2500):
    """Wait for the page to finish loading. Pages that keep polling the server never go fully
    quiet ("networkidle"), so that wait is best-effort and never fails the run."""
    for state, ms in (("load", 15000), ("networkidle", idle_ms)):
        try:
            await page.wait_for_load_state(state, timeout=ms)
        except PWTimeout:
            pass


async def _goto(page: Page, url: str):
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
    except PWTimeout:
        raise SiteUnreachable(
            f"{urlparse(url).hostname} didn't respond within 60 seconds. Check the container can reach "
            "the internet (DNS, firewall, VPN), then look at the debug screenshot: a blank page means no "
            "connection; an 'access denied' page means the site is refusing automated access.")
    await _settle(page)


class LoginError(Exception):
    def __init__(self, message: str, kind: str = "failed"):
        super().__init__(message)
        self.kind = kind  # "failed" | "mfa" | "unknown"


@dataclass
class ScrapeResult:
    used_saved_session: bool = False
    logged_in: bool = False
    html: str = ""
    json_payloads: list = field(default_factory=list)
    final_url: str = ""
    refreshed: bool = False
    refresh_note: str = ""      # e.g. "46 minutes ago -> a few seconds ago"
    timings: dict = field(default_factory=dict)


async def _first_visible(page: Page, selectors: list[str]):
    for sel in selectors:
        try:
            loc = page.locator(sel)
            for i in range(await loc.count()):
                el = loc.nth(i)
                if await el.is_visible():
                    return el
        except Exception:
            continue
    return None


async def _on_login_page(page: Page) -> bool:
    return await _first_visible(page, PASS_SELECTORS) is not None or \
        (await _first_visible(page, USER_SELECTORS[:-1])) is not None


async def _page_text(page: Page) -> str:
    try:
        return (await page.inner_text("body", timeout=3000)).lower()
    except Exception:
        return ""


async def _submit(page: Page, cfg: Settings, field_el):
    btn = await _first_visible(page, [cfg.submit_selector] if cfg.submit_selector else SUBMIT_SELECTORS)
    if btn:
        await btn.click()
    else:
        await field_el.press("Enter")
    await page.wait_for_timeout(1500)  # give the click time to start a navigation
    await _settle(page)


async def _login(page: Page, cfg: Settings):
    """Handles one-page forms and two-step (username → next → password) flows."""
    user_sel = [cfg.user_selector] if cfg.user_selector else USER_SELECTORS
    pass_sel = [cfg.pass_selector] if cfg.pass_selector else PASS_SELECTORS
    password_sent = False

    for _step in range(4):
        pw = await _first_visible(page, pass_sel)
        user = await _first_visible(page, user_sel)
        if pw:
            if user and not await user.input_value():
                await user.fill(cfg.username)
            await pw.fill(cfg.password)
            await _submit(page, cfg, pw)
            password_sent = True
        elif user:
            await user.fill(cfg.username)
            await _submit(page, cfg, user)
        else:
            break
        if password_sent and not await _first_visible(page, pass_sel):
            break

    text = await _page_text(page)
    if any(h in text for h in MFA_HINTS):
        raise LoginError("Login needs a multi-factor step (code / push approval). See README.", "mfa")
    if await _first_visible(page, pass_sel):
        hint = next((h for h in FAIL_HINTS if h in text), None)
        raise LoginError(f"Still on the login form after submitting ({hint or 'no error text found'}).", "failed")
    if not password_sent:
        raise LoginError("Could not find a password field on the login page. "
                         "Set CCS_USER_SELECTOR / CCS_PASS_SELECTOR in .env.", "unknown")


async def _wait_for_login_or_page(page: Page, schedule_host: str, max_s: int = 20) -> bool:
    """SSO often redirects a few seconds after the first page loads. Returns True once a login
    form shows up, or False once we've sat on the schedule site for a few seconds without one."""
    calm = 0
    for _ in range(max_s):
        if await _on_login_page(page):
            return True
        calm = calm + 1 if urlparse(page.url).hostname == schedule_host else 0
        if calm >= 3:
            return False
        await page.wait_for_timeout(1000)
    return await _on_login_page(page)


FRESH_HINTS = re.compile(r"just now|few seconds|seconds? ago|\b0 minutes?\b|\b1 minute ago|\bnow\b", re.I)


async def _status_text(page: Page, selector: str) -> str:
    try:
        loc = page.locator(selector).first
        return (await loc.inner_text(timeout=1000)).strip() if await loc.count() else ""
    except Exception:
        return ""


async def _refresh_schedule(page: Page, cfg: Settings, result: ScrapeResult) -> list:
    """Click CCS's own Refresh link so the schedule is current, then wait for
    "Last refreshed" to update. Returns the JSON captured before the click, as a fallback."""
    link = page.locator(cfg.refresh_selector).first
    try:
        await link.wait_for(state="visible", timeout=20000)   # the Angular app renders it late
    except PWTimeout:
        result.refresh_note = "Refresh button not found; the schedule may be out of date"
        return []

    before = await _status_text(page, cfg.refresh_status_selector)
    pre_click = result.json_payloads[:]
    result.json_payloads.clear()          # from here on, keep only data loaded by the refresh
    await link.click()

    after = before
    for _ in range(90):                   # up to ~45 s for CCS to finish refreshing
        await page.wait_for_timeout(500)
        after = await _status_text(page, cfg.refresh_status_selector)
        if after and after != before and FRESH_HINTS.search(after):
            break
    await _settle(page)
    await page.wait_for_timeout(1000)     # late XHRs after the refresh

    short = lambda t: re.sub(r"^\s*Last refreshed:\s*", "", t or "?", flags=re.I)
    if after != before:
        result.refreshed = True
        result.refresh_note = f"{short(before)} -> {short(after)}"
    else:
        result.refresh_note = f"clicked Refresh but 'Last refreshed' didn't change ({short(before)})"
    return pre_click


async def scrape(cfg: Settings, store) -> ScrapeResult:
    result = ScrapeResult()
    schedule_host = urlparse(cfg.schedule_url).hostname

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        ctx_kwargs = {"timezone_id": cfg.timezone, "locale": "en-US",
                      "viewport": {"width": 1400, "height": 1000}}
        saved_session = store.get("session")
        if saved_session:
            ctx_kwargs["storage_state"] = saved_session
        context = await browser.new_context(**ctx_kwargs)
        page = await context.new_page()

        # Many schedule pages load their data from a JSON API — capture it.
        async def on_response(resp):
            try:
                if urlparse(resp.url).hostname == schedule_host and "json" in (resp.headers.get("content-type") or ""):
                    result.json_payloads.append({"url": resp.url, "data": await resp.json()})
            except Exception:
                pass
        page.on("response", on_response)

        t0 = t = time.monotonic()

        def lap(name):
            nonlocal t
            now = time.monotonic(); result.timings[name] = round(now - t, 1); t = now

        try:
            await _goto(page, cfg.schedule_url)
            lap("load")

            if await _wait_for_login_or_page(page, schedule_host):
                log.info("Login form detected; signing in")
                await _login(page, cfg)
                result.logged_in = True
                if not page.url.startswith(cfg.schedule_url):
                    await _goto(page, cfg.schedule_url)
                if await _wait_for_login_or_page(page, schedule_host, max_s=8):
                    raise LoginError("Redirected back to the login page after signing in.", "failed")
            else:
                result.used_saved_session = True
            lap("login")

            await page.wait_for_timeout(1500)  # let late XHRs settle
            if cfg.refresh_enabled:
                pre_click = await _refresh_schedule(page, cfg, result)
                if not result.json_payloads:   # refresh didn't load new data; use what we had
                    result.json_payloads.extend(pre_click)
                lap("refresh")
            result.html = await page.content()
            result.final_url = page.url
            store.set("session", await context.storage_state())
            result.timings["total"] = round(time.monotonic() - t0, 1)
        finally:
            try:
                store.save_debug("html", (await page.content()).encode(), "text/plain; charset=utf-8")
                store.save_debug("json", json.dumps(result.json_payloads, indent=2, default=str).encode(),
                                 "application/json")
                store.save_debug("screenshot", await page.screenshot(full_page=True, timeout=10000), "image/png")
            except Exception:
                pass
            await browser.close()

    return result
