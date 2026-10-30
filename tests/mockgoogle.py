"""A small stand-in for Google's OAuth and Calendar API, for testing CalendarStream offline."""
import base64, hashlib, json, secrets
from urllib.parse import urlencode
from fastapi import FastAPI, Form, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response

CLIENT_ID, CLIENT_SECRET = "test-client.apps.googleusercontent.com", "test-secret"
CAL_SCOPE = "https://www.googleapis.com/auth/calendar.app.created"
S = {"codes": {}, "refresh": {}, "access": {}, "calendars": {}, "events": {}, "revoked": set(),
     "grant_calendar": True, "email": "pilot@example.com", "calls": [], "fail_next": [],
     # (0.2.8-beta.14) several OAuth clients; each one's Authorized redirect URIs (None: any); which
     # client signed each token in (an app sees only the calendars its own client made)
     "clients": {CLIENT_ID: CLIENT_SECRET}, "redirects": None, "refresh_client": {},
     # (0.2.8-beta.19, I1) refuse every calendar color with a 401, as Google did for the Developer
     "refuse_color": False}
# What Google sends with a 401 (its usual body)
REFUSED_401 = {"error": {"code": 401, "message": "Request had invalid authentication credentials. Expected OAuth 2 access "
               "token, login cookie or other valid authentication credential.",
               "errors": [{"message": "Invalid Credentials", "domain": "global", "reason": "authError",
                           "location": "Authorization", "locationType": "header"}], "status": "UNAUTHENTICATED"}}
app = FastAPI()


def b64(d): return base64.urlsafe_b64encode(d).rstrip(b"=").decode()


@app.get("/auth")
def auth(client_id: str, redirect_uri: str, response_type: str, scope: str, state: str,
         code_challenge: str, code_challenge_method: str, access_type: str = "", prompt: str = ""):
    if client_id not in S["clients"]:
        return HTMLResponse("<h1>Access blocked: Authorization Error</h1><p>Error 401: invalid_client</p>", 401)
    allowed = (S["redirects"] or {}).get(client_id) if S["redirects"] is not None else None
    if S["redirects"] is not None and redirect_uri not in (allowed or []):
        return HTMLResponse("<h1>Access blocked: This app's request is invalid</h1><p>Error 400: redirect_uri_mismatch</p>", 400)
    assert response_type == "code" and code_challenge_method == "S256"
    assert access_type == "offline" and set(scope.split()) == {"openid", "email", CAL_SCOPE}, scope
    code = secrets.token_urlsafe(8)
    granted = "openid " + "https://www.googleapis.com/auth/userinfo.email" + (" " + CAL_SCOPE if S["grant_calendar"] else "")
    S["codes"][code] = (code_challenge, redirect_uri, granted, client_id)
    return RedirectResponse(redirect_uri + "?" + urlencode({"state": state, "code": code}), 302)


def _access(refresh):
    tok = secrets.token_urlsafe(8); S["access"][tok] = refresh; return tok


@app.post("/token")
def token(grant_type: str = Form(), client_id: str = Form(), client_secret: str = Form(), code: str = Form(""),
          redirect_uri: str = Form(""), code_verifier: str = Form(""), refresh_token: str = Form("")):
    if client_id not in S["clients"]:
        return JSONResponse({"error": "invalid_client", "error_description": "The OAuth client was not found."}, 401)
    if client_secret != S["clients"][client_id]:
        return JSONResponse({"error": "invalid_client", "error_description": "Unauthorized"}, 401)
    if grant_type == "authorization_code":
        found = S["codes"].pop(code, None)
        if not found or found[1] != redirect_uri or b64(hashlib.sha256(code_verifier.encode()).digest()) != found[0]:
            return JSONResponse({"error": "invalid_grant"}, 400)
        refresh = "1//" + secrets.token_urlsafe(12); S["refresh"][refresh] = S["email"]; S["refresh_client"][refresh] = found[3]
        claims = b64(json.dumps({"iss": "https://accounts.google.com", "aud": CLIENT_ID, "email": S["email"],
                                 "email_verified": True}).encode())
        return {"access_token": _access(refresh), "expires_in": 3599, "refresh_token": refresh, "scope": found[2],
                "token_type": "Bearer", "id_token": f"e30.{claims}.sig"}
    if grant_type == "refresh_token":
        if refresh_token not in S["refresh"] or refresh_token in S["revoked"]:
            return JSONResponse({"error": "invalid_grant"}, 400)
        return {"access_token": _access(refresh_token), "expires_in": 3599, "scope": CAL_SCOPE, "token_type": "Bearer"}
    return JSONResponse({"error": "unsupported_grant_type"}, 400)


@app.post("/revoke")
def revoke(token: str = Form()):
    if token not in S["refresh"]:
        return JSONResponse({"error": "invalid_token"}, 400)
    S["revoked"].add(token); return {}


def who(authorization):
    tok = (authorization or "").removeprefix("Bearer ")
    refresh = S["access"].get(tok)
    if not refresh or refresh in S["revoked"]:
        raise HTTPException(401)
    return S["refresh"][refresh]


def client_of(authorization):
    tok = (authorization or "").removeprefix("Bearer ")
    return S["refresh_client"].get(S["access"].get(tok), CLIENT_ID)


def gerr(code, reason):
    return JSONResponse({"error": {"code": code, "errors": [{"reason": reason}]}}, code)


@app.middleware("http")
async def log_calls(request: Request, call_next):
    if request.url.path.startswith("/calendar/"):
        S["calls"].append(f"{request.method} {request.url.path.removeprefix('/calendar/v3')}")
        if S["fail_next"]:
            code, reason = S["fail_next"].pop(0)
            return gerr(code, reason)
    return await call_next(request)


@app.post("/calendar/v3/calendars")
async def cal_insert(request: Request, authorization: str = Header("")):
    owner = who(authorization); body = await request.json()
    cid = secrets.token_hex(8) + "@group.calendar.google.com"
    S["calendars"][cid] = {"id": cid, "summary": body["summary"], "timeZone": body.get("timeZone"), "owner": owner,
                           "description": body.get("description", ""), "client": client_of(authorization)}
    S["events"][cid] = {}
    return S["calendars"][cid]


@app.get("/calendar/v3/calendars/{cid}")
def cal_get(cid: str, authorization: str = Header("")):
    owner = who(authorization)
    c = S["calendars"].get(cid)
    if not c or c["owner"] != owner:
        return gerr(404, "notFound")
    if c.get("client", CLIENT_ID) != client_of(authorization):     # calendar.app.created: another client's calendar
        return gerr(403, "forbidden")
    return c


@app.delete("/calendar/v3/calendars/{cid}")
def cal_delete(cid: str, authorization: str = Header("")):
    owner = who(authorization)
    c = S["calendars"].get(cid)
    if not c or c["owner"] != owner:
        return gerr(404, "notFound")
    del S["calendars"][cid]; S["events"].pop(cid, None)
    return Response(status_code=204)


# --- Events ----------------------------------------------------------------
import re as _re
from datetime import datetime as _dt, timezone as _tz
ID_RE = _re.compile(r"^[a-v0-9]{5,1024}$")


def _now():
    return _dt.now(_tz.utc).isoformat().replace("+00:00", "Z")


def _cal(cid, authorization):
    owner = who(authorization)
    c = S["calendars"].get(cid)
    if not c or c["owner"] != owner:
        raise HTTPException(404)
    if c.get("client", CLIENT_ID) != client_of(authorization):
        raise HTTPException(403)
    return S["events"][cid]


def _check(body):
    assert ID_RE.match(body["id"]), body["id"]
    for k in ("start", "end"):
        v = body[k]
        assert ("date" in v) != ("dateTime" in v), v
        if "dateTime" in v:
            _dt.fromisoformat(v["dateTime"]); assert v.get("timeZone")
    if "colorId" in body:
        assert body["colorId"] in {str(i) for i in range(1, 12)}
    assert body["transparency"] in ("opaque", "transparent")


@app.patch("/calendar/v3/calendars/{cid}")
async def cal_patch(cid: str, request: Request, authorization: str = Header("")):
    owner = who(authorization); c = S["calendars"].get(cid)
    if not c or c["owner"] != owner:
        return gerr(404, "notFound")
    c.update(await request.json()); return c


@app.patch("/calendar/v3/users/me/calendarList/{cid}")
async def calendarlist_patch(cid: str, request: Request, authorization: str = Header("")):
    """A calendar's color in the person's list (0.2.8-beta.15)."""
    if S["refuse_color"]:
        return JSONResponse(REFUSED_401, 401)
    owner = who(authorization); c = S["calendars"].get(cid)
    if not c or c["owner"] != owner:
        return gerr(404, "notFound")
    body = await request.json()
    c["backgroundColor"] = body.get("backgroundColor"); return c


@app.post("/calendar/v3/calendars/{cid}/events")
async def ev_insert(cid: str, request: Request, authorization: str = Header("")):
    try:
        evs = _cal(cid, authorization)
    except HTTPException as e:
        return gerr(e.status_code, "forbidden" if e.status_code == 403 else "notFound")
    body = await request.json(); _check(body)
    if body["id"] in evs:
        return gerr(409, "duplicate")
    evs[body["id"]] = {**body, "updated": _now()}; return evs[body["id"]]


@app.put("/calendar/v3/calendars/{cid}/events/{eid}")
async def ev_update(cid: str, eid: str, request: Request, authorization: str = Header("")):
    try:
        evs = _cal(cid, authorization)
    except HTTPException as e:
        return gerr(e.status_code, "forbidden" if e.status_code == 403 else "notFound")
    if eid not in evs:
        return gerr(404, "notFound")
    body = await request.json(); _check(body); assert body["id"] == eid
    evs[eid] = {**body, "updated": _now()}; return evs[eid]


@app.delete("/calendar/v3/calendars/{cid}/events/{eid}")
def ev_delete(cid: str, eid: str, authorization: str = Header("")):
    try:
        evs = _cal(cid, authorization)
    except HTTPException as e:
        return gerr(e.status_code, "forbidden" if e.status_code == 403 else "notFound")
    if eid not in evs:
        return gerr(404, "notFound")
    if evs[eid]["status"] == "cancelled":
        return gerr(410, "deleted")
    evs[eid]["status"] = "cancelled"; evs[eid]["updated"] = _now()
    return Response(status_code=204)


@app.get("/calendar/v3/calendars/{cid}/events")
def ev_list(cid: str, timeMin: str = "", showDeleted: str = "false", maxResults: int = 250, pageToken: str = "",
            privateExtendedProperty: str = "", authorization: str = Header("")):
    try:
        evs = _cal(cid, authorization)
    except HTTPException as e:
        return gerr(e.status_code, "forbidden" if e.status_code == 403 else "notFound")
    tmin = _dt.fromisoformat(timeMin) if timeMin else None
    def ends(e):
        v = e["end"]
        return _dt.fromisoformat(v["dateTime"]) if "dateTime" in v else _dt.fromisoformat(v["date"] + "T00:00:00+00:00")
    items = [e for e in evs.values()
             if (showDeleted == "true" or e["status"] != "cancelled")
             and (not tmin or ends(e) > tmin)
             and (not privateExtendedProperty or e.get("extendedProperties", {}).get("private", {}).get(
                 privateExtendedProperty.split("=")[0]) == privateExtendedProperty.split("=")[1])]
    start = int(pageToken or 0); page = items[start:start + 40]       # small pages to test paging
    out = {"items": page}
    if start + 40 < len(items):
        out["nextPageToken"] = str(start + 40)
    return out


# Push notifications: channels are recorded; tests call notify() to play Google's part.
S.setdefault("channels", {})
S.setdefault("refuse_watch", False)


@app.post("/calendar/v3/calendars/{cid}/events/watch")
async def ev_watch(cid: str, request: Request, authorization: str = Header("")):
    _cal(cid, authorization)
    if S["refuse_watch"]:
        return gerr(403, "pushNotSupportedForRequestedResource")
    body = await request.json()
    assert body["type"] == "web_hook" and body["address"].startswith("https://"), body
    rid = "res-" + secrets.token_hex(4)
    S["channels"][body["id"]] = {"cid": cid, "address": body["address"], "token": body.get("token"), "resource": rid,
                                 "ttl": body.get("params", {}).get("ttl")}
    import time
    return {"kind": "api#channel", "id": body["id"], "resourceId": rid, "resourceUri": f"/calendars/{cid}/events",
            "expiration": str(int((time.time() + 7 * 86400) * 1000))}


@app.post("/calendar/v3/channels/stop")
async def ch_stop(request: Request, authorization: str = Header("")):
    who(authorization)
    body = await request.json()
    ch = S["channels"].get(body["id"])
    if not ch or ch["resource"] != body["resourceId"]:
        raise HTTPException(404)
    del S["channels"][body["id"]]
    return Response(status_code=204)
