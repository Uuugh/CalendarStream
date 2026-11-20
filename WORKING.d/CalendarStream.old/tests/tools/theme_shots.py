"""Render the CSS/theme review matrix using the synthetic demo server.

Run: DEMO_PORT=8180 python3 tests/tools/theme_shots.py OUTPUT_DIR
The output includes real app screenshots and computed component values; no real account data.
"""
import argparse
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

STABLE = '''.srcstatus b,.srcnext,.ver,.ptime,#activity time,.lastrun,.nextrun,.fstream{visibility:hidden!important}
*,*::before,*::after{animation:none!important;transition:none!important;caret-color:transparent!important}'''
EXPAND = '''document.querySelectorAll('.cfgbody[hidden]').forEach(x=>x.hidden=false);
document.querySelectorAll('.cfgbox').forEach(x=>x.classList.add('cfgopen'));'''

def main():
    parser=argparse.ArgumentParser();parser.add_argument('output');args=parser.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    base='http://127.0.0.1:'+os.environ.get('DEMO_PORT','8180')
    measurements=[]
    with sync_playwright() as pw:
        browser=pw.chromium.launch()
        for width in (1230,390):
            for theme in ('light','dark'):
                pg=browser.new_page(viewport={'width':width,'height':900},color_scheme=theme,
                                    extra_http_headers={'Authorization':'Basic dDpwYXNzd29yZDE='})
                errors=[];pg.on('pageerror',lambda err: errors.append(str(err)))
                def load(query=''):
                    pg.goto(base+'/?month=2026-10&date=2026-10-14'+query);pg.wait_for_load_state('networkidle')
                    pg.evaluate('(t)=>document.documentElement.dataset.theme=t',theme)
                    pg.add_style_tag(content=STABLE)
                def shot(name):
                    pg.evaluate('document.fonts.ready');pg.wait_for_timeout(120)
                    path=out/f'{name}-{width}-{theme}.png';pg.screenshot(path=str(path),full_page=True)
                    print(path,flush=True)
                load();csrf=pg.locator('input[name=csrf]').first.input_value()
                def post(path,**fields):
                    response=pg.request.post(base+path,form={'csrf':csrf,**fields});assert response.ok, response.status
                post('/ui/view',view='month');post('/ui/calview',full='0');load();shot('page')
                metrics=pg.evaluate('''()=>{const read=s=>{const e=document.querySelector(s),c=getComputedStyle(e),r=e.getBoundingClientRect();return {font:c.fontSize,padding:c.padding,margin:c.margin,radius:c.borderTopLeftRadius,width:r.width,height:r.height};};return {note:read('.mnote'),icon:read('.topbar .iconbtn'),legend:read('.legend'),month:read('.monthpick'),view:read('.viewmenu'),language:read('.langmenu')};}''')
                measurements.append({'width':width,'theme':theme,'values':metrics})
                pg.evaluate(EXPAND);shot('expanded');load('&menu=settings');shot('settings')
                for control,name in [('#monthbtn','month-picker'),('#viewbtn','view-menu'),('#langbtn','language-menu')]:
                    load();pg.click(control);shot(name)
                for dialog in ('addsrc','adddestpop','ruledialog','printdialog'):
                    load();pg.evaluate('(id)=>document.getElementById(id).showModal()',dialog);shot(dialog)
                for view in ('week','day','list'):
                    post('/ui/view',view=view);load();shot(view)
                post('/ui/view',view='month');post('/ui/calview',full='1');load();shot('full-page')
                post('/ui/calview',full='0');load();pg.emulate_media(media='print');shot('browser-print');pg.emulate_media(media='screen')
                pg.goto(base+'/print?view=month&start=2026-10-01&end=2026-10-31&theme='+theme)
                pg.wait_for_load_state('networkidle');pg.add_style_tag(content=STABLE);shot('print-preview')
                if errors:raise RuntimeError(str(errors))
                pg.close()
        browser.close()
    (out/'measurements.json').write_text(json.dumps(measurements,indent=2))

if __name__=='__main__':main()
