import os, json
from playwright.sync_api import sync_playwright

PAGES = ["index.html", "about.html", "properties.html", "property-details.html", "services.html", "contact.html"]
WIDTHS = [1920, 1440, 1024, 768, 390]
report = []

with sync_playwright() as p:
    b = p.chromium.launch()
    for name in PAGES:
        for wdt in WIDTHS:
            pg = b.new_page(viewport={"width": wdt, "height": 900})
            errs = []
            pg.on("pageerror", lambda e: errs.append(str(e)))
            pg.on("console", lambda m: errs.append(m.text) if m.type == "error" and "ERR_TUNNEL" not in m.text else None)
            pg.goto("file://" + os.path.abspath(name))
            pg.wait_for_timeout(700)
            sw = pg.evaluate("document.documentElement.scrollWidth")
            cw = pg.evaluate("document.documentElement.clientWidth")
            overflow = pg.evaluate("""() => [...document.querySelectorAll('body *')]
                .filter(el => el.getBoundingClientRect().right > document.documentElement.clientWidth + 2
                           || el.getBoundingClientRect().left < -2)
                .slice(0,6).map(el => el.tagName + '.' + String(el.className.baseVal !== undefined ? el.className.baseVal : el.className).split(' ')[0])""")
            report.append(dict(page=name, w=wdt, hscroll=sw > cw + 1, sw=sw, cw=cw, overflow=overflow, errors=errs[:3]))
            pg.close()

    # интерактив на главной
    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("file://" + os.path.abspath("index.html"))
    pg.wait_for_timeout(600)
    before = pg.evaluate("document.querySelector('[data-slider-track]').style.translate")
    pg.click("[data-slider-next]")
    pg.wait_for_timeout(700)
    after = pg.evaluate("document.querySelector('[data-slider-track]').style.translate")
    counter = pg.inner_text("[data-slider-current]")
    report.append(dict(check="slider", before=before, after=after, counter=counter))
    pg.close()

    pg = b.new_page(viewport={"width": 390, "height": 800})
    pg.goto("file://" + os.path.abspath("index.html"))
    pg.wait_for_timeout(500)
    pg.click("[data-menu-open]")
    pg.wait_for_timeout(600)
    opened = pg.evaluate("document.querySelector('[data-menu]').classList.contains('is-open')")
    pg.click("[data-menu-close]")
    pg.wait_for_timeout(500)
    closed = not pg.evaluate("document.querySelector('[data-menu]').classList.contains('is-open')")
    report.append(dict(check="menu", opened=opened, closed=closed))
    pg.close()

    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("file://" + os.path.abspath("contact.html"))
    pg.wait_for_timeout(500)
    pg.click('[data-tab="international"]')
    pg.wait_for_timeout(400)
    visible = pg.evaluate("[...document.querySelectorAll('[data-tab-item]')].map(e=>[e.dataset.tabItem, !e.hidden])")
    report.append(dict(check="tabs", visible=visible))
    # форма
    pg.click("form[data-form] button[type=submit]")
    pg.wait_for_timeout(300)
    status = pg.inner_text("[data-form-status]")
    errfields = pg.evaluate("document.querySelectorAll('.field.has-error').length")
    report.append(dict(check="form-empty", status=status, err_fields=errfields))
    pg.close()

    pg = b.new_page(viewport={"width": 1440, "height": 900})
    pg.goto("file://" + os.path.abspath("property-details.html"))
    pg.wait_for_timeout(500)
    first = pg.get_attribute("[data-viewer-stage] img", "src")
    pg.click("[data-viewer-next]")
    pg.wait_for_timeout(400)
    second = pg.get_attribute("[data-viewer-stage] img", "src")
    report.append(dict(check="viewer", changed=first != second))
    pg.close()
    b.close()

print(json.dumps(report, ensure_ascii=False, indent=1))
