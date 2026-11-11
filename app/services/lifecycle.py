"""Holds: lifecycle.
Depends on: no other app files. Other collaborators are explicit arguments/providers.
Used by: app/main.py.
Reads/writes: supplied services may access storage, network, files and the clock.
Dart note: feature application services; inject collaborators through typed interfaces.
"""

from __future__ import annotations
import asyncio
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(
    _app,
    *,
    ensure_local,
    google_loop,
    import_public_url,
    log,
    logins,
    migrate_destinations,
    migrate_links,
    migrate_rules,
    migrate_sources,
    rebuild,
    settings,
    share_converted_rules,
    source_ids,
    source_tasks,
    start_source,
    state,
    store,
    tail_logs,
    update_loop,
    updater_loop,
):
    await asyncio.to_thread(store.open)  # waits for the database container if needed
    settings.resolve_feed_token(store)
    if store.get("feed_token_manual") and store.get("feed_token"):
        settings.feed_token = store.get(
            "feed_token"
        )  # a stream name entered by hand wins over FEED_TOKEN
    state.load()
    import_public_url()
    migrate_sources()
    migrate_destinations()
    migrate_rules()
    migrate_links()
    tail_logs()
    ensure_local()
    share_converted_rules()
    imported = logins.import_old(
        settings.username, settings.password, settings.gui_user, settings.gui_password
    )
    if imported:
        state.record(
            "info",
            "Imported "
            + " and ".join(imported)
            + " from the old secret files. They're "
            "now kept in the database and changed on the status page; the files can be deleted.",
        )
    if not logins.has_page_login:
        # First start: the status page asks for this code before the login can be created.
        log.warning(
            "First-time setup: open the status page and enter the setup code %s",
            logins.new_setup_code(),
        )
    # Re-apply current settings (calendar name, DEFAULT_EVENT_HOURS, edits) to the last download
    try:
        rebuild()
    except Exception as e:
        log.error("Couldn't rebuild the feed from the stored download: %s", e)
    for sid in source_ids():
        start_source(sid)
    tasks = [
        asyncio.create_task(google_loop()),
        asyncio.create_task(update_loop()),
        asyncio.create_task(updater_loop()),
    ]
    yield
    tasks += list(source_tasks.values())
    source_tasks.clear()
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    store.close()
