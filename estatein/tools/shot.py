import sys, os
from playwright.sync_api import sync_playwright
page_name = sys.argv[1]
width = int(sys.argv[2]) if len(sys.argv) > 2 else 1920
out = sys.argv[3] if len(sys.argv) > 3 else '/tmp/page.png'
full = sys.argv[4] != '0' if len(sys.argv) > 4 else True
path = os.path.abspath(page_name)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': width, 'height': 1000}, device_scale_factor=1)
    errs = []
    pg.on('console', lambda m: errs.append(m.text) if m.type == 'error' else None)
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + path)
    pg.wait_for_timeout(1500)
    pg.screenshot(path=out, full_page=full)
    b.close()
print('errors:', errs[:10])
