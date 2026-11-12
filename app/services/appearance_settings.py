"""Holds: validate appearance edits before any user preferences are saved.
Depends on: no app modules; upload, error and image validators are explicit arguments.
Used by: app/routes/settings.py.
Reads/writes: reads supplied uploads; returns values without changing storage.
Dart note: appearance application service with an injected image decoder.
"""
from __future__ import annotations
import base64


async def appearance_values(form, *, brand, image_kind, field_error, max_bytes):
    """Prepare a complete appearance update, rejecting all bad fields before persistence."""
    saved = dict(brand or {})
    for kind in ("logo", "favicon"):
        if form.get(f"remove_{kind}"):
            saved.pop(kind, None)
        upload = form.get(kind)
        if hasattr(upload, "read"):
            data = await upload.read(max_bytes + 1)
            if not data:
                continue
            if len(data) > max_bytes:
                raise field_error("That picture is over 256 KB.", kind)
            mime = image_kind(data)
            if not mime:
                raise field_error("Use a PNG, SVG, WebP, JPEG or ICO picture.", kind)
            saved[kind] = {"mime": mime, "b64": base64.b64encode(data).decode()}
    if form.get("reset"):
        return saved, "left", {"i": 100, "d": 100}
    try:
        intensity, duration = int(form.get("intensity", 100)), int(form.get("duration", 100))
    except (TypeError, ValueError):
        raise field_error("Intensity and duration are whole percentages.", "intensity", "duration")
    if not (0 <= intensity <= 200 and 25 <= duration <= 300):
        raise field_error("Intensity is 0–200 % and duration 25–300 %.", "intensity", "duration")
    grips = form.get("grips", "left")
    if grips not in ("left", "right"):
        raise field_error("Choose Left or Right.", "grips")
    return saved, grips, {"i": intensity, "d": duration}
