"""Calendar grid lane placement and optional date parsing.

Holds: _lanes and _opt_day.
Depends on: no other app files.
Used by: app/main.py.
Reads/writes: _lanes mutates caller-supplied layout dictionaries; _opt_day reads input only.
Dart note: Presentation layout helpers in calendars/ui; no app globals.
"""
from datetime import date

def _lanes(items: list[dict]) -> None:
    """Side-by-side places for the timed events of one day in the hourly grid (0.2.8-beta.29, F15.9): every
    cluster of events that overlap shares the width, each in its own lane."""
    timed = sorted((i for i in items if i["m0"] is not None), key=lambda i: (i["m0"], -i["m1"]))
    cluster: list[dict] = []
    ends: list[int] = []
    def close():
        for i in cluster:
            i["lanes"] = max(1, len(ends))
    for it in timed:
        if cluster and it["m0"] >= max(i["m1"] for i in cluster):
            close(); cluster, ends = [], []
        lane = next((n for n, end in enumerate(ends) if end <= it["m0"]), len(ends))
        if lane == len(ends):
            ends.append(it["m1"])
        else:
            ends[lane] = it["m1"]
        it["lane"] = lane
        cluster.append(it)
    close()


def _opt_day(value: str) -> date | None:
    try:
        d = date.fromisoformat(value)
        return d if 2000 <= d.year <= 2100 else None
    except ValueError:
        return None


