"""Draws the CalendarStream Theme Rules pictures from the demo page itself (0.2.8-beta.24, R2), so they always show what
is built and are redrawn with one command:

    tests/tools/demo.sh                       # the demo server, filled with the made-up schedule
    tests/tools/theme_rules.py                # writes build_rules/CalendarStream_Theme_Rules_Light.png and _Dark.png

Part 1: the whole page, a module open in every section, each part named where it is. Part 2: one card per section
of build_rules/theme.md (card 2·N = section N): its title, the rule's first paragraph, and the real thing taken from
the page (or drawn with the page's own stylesheet). A card whose part can't be found on the demo says so on the card.
"""
import base64, html, os, re, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
PORT = os.environ.get("DEMO_PORT", "8177")
BASE = f"http://127.0.0.1:{PORT}"
AUTH = {"Authorization": "Basic " + base64.b64encode(b"t:password1").decode()}
STEADY = "*, *::before, *::after { animation:none !important; transition:none !important; caret-color:transparent !important }"
EXPAND = ("document.querySelectorAll('.cfgbody[hidden], .section > .sbody[hidden]').forEach(b => b.hidden = false);"
          "document.querySelectorAll('.cfgbox').forEach(b => b.classList.add('cfgopen'));"
          "document.querySelectorAll('.section').forEach(b => b.classList.add('open'))")
# Part 1's names: (label, selector) — the first element each selector finds is outlined and named
PARTS = [("Top bar", ".topbar"), ("Calendar", "#cal"), ("Calendars", "#sources"), ("Module (calendar)", "#sources .box.module"),
         ("Status/Action buttons", "#sources .statusbox"), ("Handles", "#sources .handle"), ("Feeds", "#destinations"),
         ("Module (feed)", "#destinations .box.module"), ("All Rules", "#rules"), ("Event Templates", "#templates"),
         ("History, Undo & Logs", "#activity"), ("(?) help", ".helpdot")]
# Part 2's pictures, by card: a list of steps, each ("shot", selector) after optional ("js", code)
CARDS = {
    1: [("html", """<div style="display:grid;gap:6px;font-size:14px"><div style="font:700 17px var(--font)">United Airlines CCS+ <span style="font-weight:400;font-size:14px">module kind, 17 px / 700</span></div>
        <div>Text 14 px · <b style="font-weight:600;color:var(--muted);font-size:12px">LABEL 12 PX / 600</b> · <span style="font-size:13px;color:var(--muted)">note 13 px, muted</span></div>
        <div style="font:14px var(--mono)">webcal://calendar.example.com/calendar/Kq2mPa9tR4x7Lw3n.ics</div></div>""")],
    2: [("js", "palette")],
    3: [("js", "icons")],
    4: [("html", """<div style="display:flex;gap:10px;align-items:center"><button class="ghost" style="height:34px">Control · 8 px</button>
        <div style="border:1px solid var(--line);border-radius:var(--rbox);padding:10px 14px;background:var(--card)">Section, module, pop-up · 12 px</div>
        <span style="display:inline-block;width:22px;height:22px;border-radius:5px;background:var(--accent)"></span><span class="muted">mark · 4–6 px</span></div>""")],
    5: [("shot", "#sources .cardhead"), ("shot", "#sources .box.module")],
    6: [("expand", ""), ("shot", "#sources .box.module.cfgopen .pairbtns")],
    7: [("shot", "#sources .box.module:nth-of-type(1) .statusbox"), ("js", "looks")],
    8: [("table", "8")],
    9: [("shot", "#sources .modrow:nth-child(2)"), ("shot", "#destinations .modrow")],
    10: [("shot", "#sources .sortable")],
    11: [("js", "ask"), ("shot", "#askdialog")],
    12: [("js", "help"), ("shot", "#sources .cardhead")],
    13: [("html", """<div style="font-size:14px">Google Cloud › Clients › CalendarStream › Authorized redirect URIs › + Add URI › Save</div>""")],
    14: [("expand", ""), ("js", "colorbox"), ("shot", "#sources .box.module.cfgopen .srchead")],
    15: [("expand", ""), ("shot", "#sources .box.module.cfgopen:last-of-type .cfgbody")],
    16: [("expand", ""), ("shot", "#activity")],
    17: [("shot", "#sources")],
    18: [("event", "")],
}
JS = {
    "palette": """() => { const s = getComputedStyle(document.documentElement); const t = ['--bg','--card','--soft','--line','--text','--muted','--accent','--ok','--okbg','--run','--runbg','--warn','--warnbg','--bad','--badbg'];
      const secs = [['Calendar','#cal'],['Calendars','#sources'],['Feeds','#destinations'],['All Rules','#rules'],['Event Templates','#templates'],['History','#activity']];
      const sw = (c, n) => `<div style="display:grid;gap:3px;justify-items:center;font-size:11px"><span style="width:46px;height:30px;border-radius:5px;border:1px solid var(--line);background:${c}"></span>${n}</div>`;
      const box = document.createElement('div'); box.id = 'tr-pic';
      box.innerHTML = '<div style="display:flex;flex-wrap:wrap;gap:8px">' + t.map(x => sw(s.getPropertyValue(x).trim(), x)).join('') + '</div>' +
        '<div style="display:flex;flex-wrap:wrap;gap:8px;margin-top:10px">' + secs.map(([n, q]) => { const e = document.querySelector(q); return sw(e ? getComputedStyle(e).borderTopColor : 'transparent', n); }).join('') + '</div>';
      return box; }""",
    "icons": """() => { const box = document.createElement('div'); box.id = 'tr-pic'; box.style.cssText = 'display:flex;flex-wrap:wrap;gap:14px;color:var(--text)';
      const seen = new Set(); document.querySelectorAll('svg').forEach(v => { const k = v.innerHTML; if (seen.has(k) || seen.size >= 24 || v.closest('#tr-root')) return; seen.add(k); const c = v.cloneNode(true); c.setAttribute('width', 22); c.setAttribute('height', 22); box.appendChild(c); });
      return box; }""",
    "looks": """() => { const box = document.createElement('div'); box.id = 'tr-pic'; box.style.cssText = 'display:flex;flex-wrap:wrap;gap:8px';
      [['good','Healthy','--ok','--okbg'],['run','Syncing…','--run','--runbg'],['warn','Sign-in rejected','--warn','--warnbg'],['bad','Internal error','--bad','--badbg']].forEach(([k, w, f, b]) => {
        box.insertAdjacentHTML('beforeend', `<span style="display:inline-flex;align-items:center;height:34px;padding:0 14px;border-radius:var(--r);font:600 13px var(--font);color:var(${f});background:var(${b});border:1px solid color-mix(in srgb, var(${f}) 35%, var(--line))">${w}</span>`); });
      box.insertAdjacentHTML('beforeend', '<span style="display:inline-flex;align-items:center;height:34px;padding:0 14px;border-radius:var(--r);font:600 13px var(--font);color:var(--onaccent);background:var(--accent)">Blue: buttons only</span>');
      return box; }""",
}


def section_texts():
    """theme.md's sections: {N: (title, first paragraph without markdown)} and its tables, by section."""
    md = (ROOT / "build_rules" / "theme.md").read_text()
    out, tables = {}, {}
    for m in re.finditer(r"^## (\d+)\. (.+?)\n(.*?)(?=^## |\Z)", md, re.S | re.M):
        n, title, body = int(m[1]), m[2].strip(), m[3]
        paras = [p.strip() for p in body.split("\n\n") if p.strip() and not p.strip().startswith("|")]
        text = re.sub(r"`([^`]*)`", r"\1", re.sub(r"\*\*([^*]+)\*\*", r"\1", " ".join(paras[0].split()))) if paras else ""
        out[n] = (title, re.sub(r"^Picture 2·\d+[^.]*\.\s*", "", text))
        rows = [r for r in body.splitlines() if r.startswith("|") and not r.startswith("| ---")]
        tables[n] = [[c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", r)[1:-1]] for r in rows]
    return out, tables


def png(el):
    return "data:image/png;base64," + base64.b64encode(el.screenshot(animations="disabled")).decode()


def draw(pw, dark: bool, out: Path):
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1400, "height": 900}, device_scale_factor=2, color_scheme="dark" if dark else "light",
                    extra_http_headers=AUTH)
    def fresh(url="/?month=2026-10"):
        pg.goto(BASE + url); pg.add_style_tag(content=STEADY); pg.wait_for_timeout(400)
    texts, tables = section_texts()
    # Part 1: the whole page, everything open, each part outlined and named
    fresh(); pg.evaluate(f"() => {{ {EXPAND} }}"); pg.wait_for_timeout(300)
    boxes = pg.evaluate("""(parts) => parts.map(([n, q]) => { const e = document.querySelector(q); if (!e) return null;
        const r = e.getBoundingClientRect(); return [n, r.left + scrollX, r.top + scrollY, r.width, r.height]; }).filter(Boolean)""", PARTS)
    whole = "data:image/png;base64," + base64.b64encode(pg.screenshot(full_page=True, animations="disabled")).decode()
    width = pg.evaluate("() => document.documentElement.scrollWidth")
    # Part 2: each card's pictures
    cards = []
    for n in sorted(texts):
        title, text = texts[n]
        pics = []
        fresh()
        try:
            for kind, arg in CARDS.get(n, []):
                if kind == "expand":
                    fresh(); pg.evaluate(f"() => {{ {EXPAND} }}"); pg.wait_for_timeout(200)
                elif kind == "html":
                    pics.append(("html", arg))
                elif kind == "table":
                    rows = tables.get(int(arg)) or []
                    pics.append(("html", "<table class='tr-t'>" + "".join("<tr>" + "".join(f"<{'th' if i == 0 else 'td'}>{html.escape(c)}</{'th' if i == 0 else 'td'}>" for c in r) + "</tr>" for i, r in enumerate(rows)) + "</table>"))
                elif kind == "event":
                    fresh("/event?date=2026-10-21&month=2026-10&embed=1")
                    pics.append(("img", png(pg.locator("body"))))
                    fresh()
                elif kind == "js" and arg in JS:
                    if not pg.locator(".topbar").count(): fresh()
                    pg.evaluate(f"() => {{ const e = ({JS[arg]})(); document.body.appendChild(e); }}")
                    pics.append(("img", png(pg.locator("#tr-pic"))))
                    pg.evaluate("() => document.getElementById('tr-pic').remove()")
                elif kind == "js" and arg == "ask":
                    fresh(); pg.evaluate("() => { ask('Remove the feed Everything?\\nIts links and subscribe page stop working.', [{label:'No',value:false},{label:'Yes',value:true}], false, true); }")
                    pg.wait_for_timeout(300)
                elif kind == "js" and arg == "help":
                    fresh(); pg.locator("#sources .cardhead .helpdot").first.click(timeout=3000); pg.wait_for_timeout(300)
                elif kind == "js" and arg == "colorbox":
                    pg.locator("#sources .box.module.cfgopen .colorpick").first.click(); pg.wait_for_timeout(200)
                elif kind == "shot":
                    loc = pg.locator(arg).first
                    pics.append(("img", png(loc)) if loc.count() else ("miss", arg))
            if n in (11, 12, 14): fresh()
        except Exception as e:   # one card's trouble is shown on that card, not a stopped drawing
            pics.append(("miss", f"{type(e).__name__}: {e}"[:160])); fresh()
        cards.append((n, title, text, pics))
    # Compose both parts as one page, drawn with the app's own stylesheet and fonts, and take it whole
    fresh()
    sc = 0.5    # Part 1's page at half size
    marks = "".join(f'<div class="tr-m" style="left:{x*sc}px;top:{y*sc}px;width:{w*sc}px;height:{h*sc}px"><span>{html.escape(n)}</span></div>' for n, x, y, w, h in boxes)
    def pic(k, v):
        if k == "img": return f'<img src="{v}" style="max-width:100%;width:auto;zoom:.5">'
        if k == "miss": return f'<p class="tr-miss">Not found on the demo: {html.escape(v)}</p>'
        return f'<div class="tr-h">{v}</div>'
    body = f"""<div id="tr-root"><h1>CalendarStream Theme Rules</h1>
      <p class="muted">Drawn from the demo page by tests/tools/theme_rules.py · {'Dark' if dark else 'Light'} · the rules: build_rules/theme.md</p>
      <h2>Part 1: the page</h2>
      <div class="tr-p1" style="width:{width*sc}px"><img src="{whole}" style="width:{width*sc}px">{marks}</div>
      <h2>Part 2: the rules (card 2·N = theme.md section N)</h2>
      <div class="tr-cards">""" + "".join(
        f'<section class="tr-c"><h3>{n} · {html.escape(t)}</h3><p>{html.escape(x)}</p>{"".join(pic(k, v) for k, v in p)}</section>'
        for n, t, x, p in cards) + "</div></div>"
    css = """#tr-root { padding:24px; background:var(--bg); color:var(--text); font:14px/1.45 var(--font); width:1352px }
      #tr-root h1 { font-size:28px; margin:0 0 4px } #tr-root h2 { font-size:20px; margin:24px 0 10px }
      .tr-p1 { position:relative; border:1px solid var(--line); border-radius:12px; overflow:hidden }
      .tr-m { position:absolute; border:2px solid #d6336c; border-radius:6px; pointer-events:none }
      .tr-m span { position:absolute; left:-2px; top:-2px; background:#d6336c; color:#fff; font:600 11px var(--font); padding:1px 6px; border-radius:6px 0 6px 0; white-space:nowrap }
      .tr-cards { display:grid; grid-template-columns:1fr 1fr; gap:12px; align-items:start }
      .tr-c { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:14px; display:grid; gap:8px; min-width:0 }
      .tr-c h3 { margin:0; font-size:16px } .tr-c p { margin:0; color:var(--muted); font-size:13px }
      .tr-c img { border:1px dashed var(--line); border-radius:6px; justify-self:start }
      .tr-h { min-width:0 } .tr-miss { color:var(--warn) !important }
      .tr-t { border-collapse:collapse; font-size:11.5px } .tr-t th, .tr-t td { text-align:left; vertical-align:top; padding:3px 6px; border-top:1px solid var(--line) }
      .tr-c:has(.tr-t) { grid-column:1 / -1 }"""
    pg.evaluate("""([b, c]) => { document.body.innerHTML = b; const s = document.createElement('style'); s.textContent = c; document.head.appendChild(s);
                     document.body.style.cssText = 'margin:0;background:var(--bg);width:1400px'; }""", [body, css])
    pg.wait_for_timeout(800)
    pg.locator("#tr-root").screenshot(path=str(out), animations="disabled")
    b.close()
    print(out, "·", [(c[0], v) for c in cards for k, v in c[3] if k == "miss"] or "every part found")


if __name__ == "__main__":
    with sync_playwright() as pw:
        for dark in (False, True):
            draw(pw, dark, ROOT / "build_rules" / f"CalendarStream_Theme_Rules_{'Dark' if dark else 'Light'}.png")
    sys.exit(0)
