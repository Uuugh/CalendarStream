"""F59: one exchange with Google (a request and its response), kept for the Beta traffic view.

Holds: the time, which account made the call, the request (method, URL, headers, body) and the response
(status, headers, body) or the error that stood in for one, and how long it took.

Depends on: nothing (plain data).
Used by: app/google/traffic_log.py (keeps a bounded list of these), app/google/api.py (makes one per call),
app/routes/google.py (reads them for the Beta traffic view).
Reads/writes: nothing; held only in memory, never in the database (F59: "I want to see everything", so
nothing here is redacted, and it must not outlive the process by landing in a report or a log file).

Dart note: an immutable data class (`TrafficEntry`), in the `domain` layer alongside the other Google types.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TrafficEntry:
    at: float                       # time.time() when the call finished
    account: str                    # "" for the first Google account, else its a123456 id
    method: str
    url: str
    request_headers: dict = field(default_factory=dict)
    request_body: str = ""
    status: int | str = ""          # an HTTP status, or a short word ("error") when none came back
    response_headers: dict = field(default_factory=dict)
    response_body: str = ""
    ms: float = 0.0                 # how long the call took

    def to_dict(self) -> dict:
        return {"at": self.at, "account": self.account, "method": self.method, "url": self.url,
                "request_headers": self.request_headers, "request_body": self.request_body,
                "status": self.status, "response_headers": self.response_headers,
                "response_body": self.response_body, "ms": round(self.ms, 1)}
