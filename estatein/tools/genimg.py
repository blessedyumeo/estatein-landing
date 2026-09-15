#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор SVG-иллюстраций-заглушек для вёрстки Estatein.
Внешние картинки недоступны, поэтому вся графика собирается процедурно
в фирменной палитре макета (тёмный фон + фиолетовый акцент).
"""
import os, random, math

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "img")

PURPLE = "#703BF7"
PURPLE_L = "#A685FA"


def w(path, body):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(body)
    return full


def head(w_, h_, uid):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w_} {h_}" '
        f'width="{w_}" height="{h_}" role="img" aria-hidden="true">'
    )


def sky(uid, w_, h_, top, mid, bot):
    return (
        f'<defs><linearGradient id="sky{uid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{top}"/><stop offset=".55" stop-color="{mid}"/>'
        f'<stop offset="1" stop-color="{bot}"/></linearGradient>'
        f'<linearGradient id="glass{uid}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0" stop-color="#6C7BE8"/><stop offset=".5" stop-color="#3D46A8"/>'
        f'<stop offset="1" stop-color="#232a6b"/></linearGradient>'
        f'<linearGradient id="fade{uid}" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="#000" stop-opacity="0"/>'
        f'<stop offset="1" stop-color="#000" stop-opacity=".55"/></linearGradient></defs>'
        f'<rect width="{w_}" height="{h_}" fill="url(#sky{uid})"/>'
    )


def stars(rnd, w_, h_, n=40):
    out = []
    for _ in range(n):
        x = rnd.uniform(0, w_)
        y = rnd.uniform(0, h_ * 0.55)
        r = rnd.uniform(0.6, 1.6)
        o = rnd.uniform(0.15, 0.55)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#fff" opacity="{o:.2f}"/>')
    return "".join(out)


def contour(uid, w_, h_):
    """Тонкие «горизонтали» как на фоне макета."""
    out = []
    for i in range(9):
        y = h_ * (0.12 + i * 0.1)
        amp = 18 + i * 4
        d = f"M -20 {y:.0f} C {w_*0.25:.0f} {y-amp:.0f}, {w_*0.6:.0f} {y+amp:.0f}, {w_+20:.0f} {y-amp*0.4:.0f}"
        out.append(f'<path d="{d}" fill="none" stroke="#ffffff" stroke-opacity=".05" stroke-width="1"/>')
    return "".join(out)


def tower(rnd, x, y, tw, th, uid, warm=0.12):
    """Стеклянная башня с сеткой окон."""
    p = [f'<g><rect x="{x:.0f}" y="{y:.0f}" width="{tw:.0f}" height="{th:.0f}" rx="3" fill="url(#glass{uid})"/>']
    p.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{tw*0.28:.0f}" height="{th:.0f}" rx="3" fill="#ffffff" opacity=".07"/>')
    cols = max(3, int(tw // 16))
    rows = max(4, int(th // 18))
    cw = tw / cols
    ch = th / rows
    for r in range(rows):
        for c in range(cols):
            wx = x + c * cw + cw * 0.18
            wy = y + r * ch + ch * 0.2
            ww = cw * 0.64
            wh = ch * 0.55
            if rnd.random() < warm:
                fill, op = "#FFD9A0", rnd.uniform(0.55, 0.95)
            else:
                fill, op = "#BFD0FF", rnd.uniform(0.06, 0.22)
            p.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{ww:.1f}" height="{wh:.1f}" fill="{fill}" opacity="{op:.2f}"/>')
    p.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{tw:.0f}" height="{th:.0f}" rx="3" fill="none" stroke="#8FA0FF" stroke-opacity=".28"/>')
    p.append("</g>")
    return "".join(p)


def skyline(seed, w_, h_, uid, dense=True):
    rnd = random.Random(seed)
    out = []
    # задний план
    bx = -10
    while bx < w_ + 10:
        bw = rnd.uniform(28, 70)
        bh = rnd.uniform(h_ * 0.2, h_ * 0.45)
        out.append(f'<rect x="{bx:.0f}" y="{h_-bh:.0f}" width="{bw:.0f}" height="{bh:.0f}" fill="#141a3a" opacity=".85"/>')
        bx += bw + rnd.uniform(4, 14)
    # передний план
    n = 5 if dense else 3
    x = w_ * 0.06
    for i in range(n):
        tw = rnd.uniform(w_ * 0.09, w_ * 0.17)
        th = rnd.uniform(h_ * 0.38, h_ * 0.78)
        out.append(tower(rnd, x, h_ - th, tw, th, uid))
        x += tw + rnd.uniform(w_ * 0.01, w_ * 0.05)
        if x > w_:
            break
    return "".join(out)


# ---------- 1. Герой: небоскрёбы ----------
def hero(name="hero-building.svg", w_=900, h_=900, seed=7):
    uid = "H"
    rnd = random.Random(seed)
    s = head(w_, h_, uid)
    s += sky(uid, w_, h_, "#0A0A18", "#171034", "#241653")
    s += stars(rnd, w_, h_, 60)
    s += contour(uid, w_, h_)
    s += f'<ellipse cx="{w_*0.72:.0f}" cy="{h_*0.42:.0f}" rx="{w_*0.38:.0f}" ry="{h_*0.3:.0f}" fill="{PURPLE}" opacity=".18"/>'
    s += skyline(seed, w_, h_, uid)
    s += f'<rect y="{h_*0.72:.0f}" width="{w_}" height="{h_*0.28:.0f}" fill="url(#fade{uid})"/>'
    s += "</svg>"
    return w(name, s)


# ---------- 2. Карточки объектов ----------
def villa(name, seed, w_=800, h_=600, palette=("#0C1026", "#1A1442", "#2A1C5E")):
    uid = "V" + str(seed)
    rnd = random.Random(seed)
    s = head(w_, h_, uid)
    s += sky(uid, w_, h_, *palette)
    s += stars(rnd, w_, h_, 34)
    s += contour(uid, w_, h_)
    s += f'<ellipse cx="{w_*0.2:.0f}" cy="{h_*0.3:.0f}" rx="200" ry="150" fill="{PURPLE_L}" opacity=".12"/>'
    gy = h_ * 0.72
    s += f'<rect y="{gy:.0f}" width="{w_}" height="{h_-gy:.0f}" fill="#0b1226"/>'
    # вилла: два объёма
    s += f'<rect x="{w_*0.12:.0f}" y="{gy-170:.0f}" width="{w_*0.44:.0f}" height="170" rx="6" fill="#F2F0EC"/>'
    s += f'<rect x="{w_*0.12:.0f}" y="{gy-170:.0f}" width="{w_*0.44:.0f}" height="26" rx="4" fill="#DFDBD3"/>'
    s += f'<rect x="{w_*0.46:.0f}" y="{gy-250:.0f}" width="{w_*0.34:.0f}" height="250" rx="6" fill="#E8E5DF"/>'
    s += f'<rect x="{w_*0.46:.0f}" y="{gy-250:.0f}" width="{w_*0.34:.0f}" height="22" rx="4" fill="#CFCAC0"/>'
    # панорамное остекление
    for i in range(4):
        s += f'<rect x="{w_*0.15+i*w_*0.1:.0f}" y="{gy-140:.0f}" width="{w_*0.075:.0f}" height="96" rx="2" fill="url(#glass{uid})" opacity=".9"/>'
    for i in range(3):
        s += f'<rect x="{w_*0.49+i*w_*0.1:.0f}" y="{gy-215:.0f}" width="{w_*0.075:.0f}" height="80" rx="2" fill="#FFD9A0" opacity="{0.35+0.2*i:.2f}"/>'
    # бассейн
    s += f'<rect x="{w_*0.08:.0f}" y="{gy+24:.0f}" width="{w_*0.6:.0f}" height="{h_*0.16:.0f}" rx="10" fill="#1FB6C9" opacity=".65"/>'
    s += f'<rect x="{w_*0.08:.0f}" y="{gy+24:.0f}" width="{w_*0.6:.0f}" height="{h_*0.16:.0f}" rx="10" fill="none" stroke="#7FE6F2" stroke-opacity=".4"/>'
    for i in range(5):
        s += f'<rect x="{w_*0.12+i*w_*0.1:.0f}" y="{gy+34+i%2*10:.0f}" width="{w_*0.05:.0f}" height="4" rx="2" fill="#CFF7FC" opacity=".5"/>'
    # терраса и кустарник
    s += f'<rect x="{w_*0.7:.0f}" y="{gy:.0f}" width="{w_*0.26:.0f}" height="10" rx="3" fill="#6f5a45"/>'
    for i in range(3):
        cx = w_ * (0.74 + i * 0.08)
        s += f'<ellipse cx="{cx:.0f}" cy="{gy-16:.0f}" rx="26" ry="20" fill="#2f5a3d"/>'
        s += f'<ellipse cx="{cx-8:.0f}" cy="{gy-24:.0f}" rx="18" ry="14" fill="#3a6b48"/>'
    s += f'<rect y="{h_*0.78:.0f}" width="{w_}" height="{h_*0.22:.0f}" fill="url(#fade{uid})"/>'
    s += "</svg>"
    return w(name, s)


def cityscape(name, seed, w_=800, h_=600, palette=("#080B1C", "#141038", "#241A56")):
    uid = "C" + str(seed)
    rnd = random.Random(seed)
    s = head(w_, h_, uid)
    s += sky(uid, w_, h_, *palette)
    s += stars(rnd, w_, h_, 40)
    s += contour(uid, w_, h_)
    s += f'<ellipse cx="{w_*0.7:.0f}" cy="{h_*0.35:.0f}" rx="230" ry="160" fill="{PURPLE}" opacity=".16"/>'
    s += skyline(seed + 3, w_, h_, uid)
    s += f'<rect y="{h_*0.74:.0f}" width="{w_}" height="{h_*0.26:.0f}" fill="url(#fade{uid})"/>'
    s += "</svg>"
    return w(name, s)


def cottage(name, seed, w_=800, h_=600, palette=("#0A1220", "#122033", "#1D2E44")):
    uid = "K" + str(seed)
    rnd = random.Random(seed)
    s = head(w_, h_, uid)
    s += sky(uid, w_, h_, *palette)
    s += stars(rnd, w_, h_, 30)
    s += contour(uid, w_, h_)
    s += f'<ellipse cx="{w_*0.78:.0f}" cy="{h_*0.22:.0f}" rx="70" ry="70" fill="#F6E7C3" opacity=".22"/>'
    gy = h_ * 0.74
    # холмы
    s += f'<path d="M0 {gy:.0f} q {w_*0.25:.0f} -70 {w_*0.5:.0f} -10 q {w_*0.25:.0f} 60 {w_*0.5:.0f} 6 L{w_} {h_} L0 {h_} Z" fill="#14261f"/>'
    s += f'<path d="M0 {gy+40:.0f} q {w_*0.3:.0f} -50 {w_*0.6:.0f} 4 q {w_*0.2:.0f} 40 {w_*0.4:.0f} 10 L{w_} {h_} L0 {h_} Z" fill="#0e1b17"/>'
    # дом
    bx, by, bw_, bh_ = w_ * 0.3, gy - 130, w_ * 0.4, 130
    s += f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw_:.0f}" height="{bh_:.0f}" rx="4" fill="#E7DCCB"/>'
    s += f'<path d="M {bx-24:.0f} {by:.0f} L {bx+bw_/2:.0f} {by-86:.0f} L {bx+bw_+24:.0f} {by:.0f} Z" fill="#8B5A3C"/>'
    s += f'<rect x="{bx+bw_*0.62:.0f}" y="{by-64:.0f}" width="22" height="46" fill="#7a4d33"/>'
    for i in range(3):
        s += f'<rect x="{bx+24+i*(bw_*0.3):.0f}" y="{by+30:.0f}" width="46" height="42" rx="3" fill="#FFD9A0" opacity=".8"/>'
    s += f'<rect x="{bx+bw_*0.44:.0f}" y="{by+bh_-62:.0f}" width="44" height="62" rx="3" fill="#6b4630"/>'
    # ёлки
    for tx, sc in ((w_ * 0.12, 1.0), (w_ * 0.2, 0.7), (w_ * 0.82, 1.15), (w_ * 0.9, 0.8)):
        base = gy + 10
        s += f'<rect x="{tx:.0f}" y="{base-16*sc:.0f}" width="{7*sc:.0f}" height="{18*sc:.0f}" fill="#2d2118"/>'
        for k in range(3):
            yy = base - (16 + k * 30) * sc
            ww_ = (54 - k * 12) * sc
            s += f'<path d="M {tx+3.5*sc-ww_/2:.0f} {yy:.0f} L {tx+3.5*sc:.0f} {yy-46*sc:.0f} L {tx+3.5*sc+ww_/2:.0f} {yy:.0f} Z" fill="#20452f"/>'
    s += f'<rect y="{h_*0.8:.0f}" width="{w_}" height="{h_*0.2:.0f}" fill="url(#fade{uid})"/>'
    s += "</svg>"
    return w(name, s)


# ---------- 3. Интерьеры ----------
def interior(name, seed, w_=800, h_=600):
    uid = "I" + str(seed)
    rnd = random.Random(seed * 977)
    walls = ["#2B2622", "#232B33", "#2C2733", "#22262B", "#33302A", "#1F242C", "#2E2A26", "#262230"]
    floors = ["#3A2E25", "#2A2A2E", "#38302B", "#262B30", "#443528", "#23272E", "#3F342C", "#2B2833"]
    wall = walls[seed % len(walls)]
    floor = floors[(seed * 3 + 1) % len(floors)]
    mirror = seed % 2 == 1
    s = head(w_, h_, uid)
    s += (f'<defs><linearGradient id="wl{uid}" x1="0" y1="0" x2="0" y2="1">'
          f'<stop offset="0" stop-color="{wall}"/><stop offset="1" stop-color="#15161a"/></linearGradient>'
          f'<linearGradient id="win{uid}" x1="0" y1="0" x2="0" y2="1">'
          f'<stop offset="0" stop-color="#8FB6F5"/><stop offset="1" stop-color="#2C3E6B"/></linearGradient>'
          f'<linearGradient id="fd{uid}" x1="0" y1="0" x2="0" y2="1">'
          f'<stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/>'
          f'</linearGradient></defs>')
    s += f'<rect width="{w_}" height="{h_}" fill="url(#wl{uid})"/>'
    inner = []
    fy = h_ * rnd.uniform(0.62, 0.7)
    inner.append(f'<rect y="{fy:.0f}" width="{w_}" height="{h_-fy:.0f}" fill="{floor}"/>')
    # панорамное окно
    ww_ = w_ * rnd.uniform(0.34, 0.44)
    wh_ = h_ * rnd.uniform(0.42, 0.52)
    wx, wy = w_ * 0.53, h_ * rnd.uniform(0.09, 0.15)
    panes = rnd.choice([2, 3, 4])
    inner.append(f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{ww_:.0f}" height="{wh_:.0f}" rx="4" fill="url(#win{uid})" opacity=".9"/>')
    for i in range(1, panes):
        inner.append(f'<rect x="{wx+ww_*i/panes:.0f}" y="{wy:.0f}" width="5" height="{wh_:.0f}" fill="{wall}"/>')
    inner.append(f'<rect x="{wx:.0f}" y="{wy:.0f}" width="{ww_:.0f}" height="{wh_:.0f}" rx="4" fill="none" stroke="#0e0f12" stroke-width="6"/>')
    # светильники
    for i in range(rnd.choice([2, 3])):
        lx = w_ * rnd.uniform(0.12, 0.2) + i * w_ * 0.09
        ly = h_ * rnd.uniform(0.18, 0.28)
        inner.append(f'<line x1="{lx:.0f}" y1="0" x2="{lx:.0f}" y2="{ly:.0f}" stroke="#4a4a4a" stroke-width="2"/>')
        inner.append(f'<circle cx="{lx:.0f}" cy="{ly+10:.0f}" r="12" fill="#FFCE8A"/>')
        inner.append(f'<circle cx="{lx:.0f}" cy="{ly+10:.0f}" r="34" fill="#FFCE8A" opacity=".12"/>')
    # мягкая мебель: диван или кровать
    sofa_cols = ["#5C6470", "#6B5A72", "#4F5F55", "#6E6152", "#55607A"]
    col = sofa_cols[seed % len(sofa_cols)]
    sx = w_ * rnd.uniform(0.05, 0.1)
    sw = w_ * rnd.uniform(0.32, 0.4)
    if seed % 3 == 0:  # кровать
        inner.append(f'<rect x="{sx:.0f}" y="{fy-56:.0f}" width="{sw:.0f}" height="56" rx="8" fill="{col}"/>')
        inner.append(f'<rect x="{sx:.0f}" y="{fy-104:.0f}" width="{sw*0.18:.0f}" height="104" rx="8" fill="#3f4650"/>')
        for i in range(2):
            inner.append(f'<rect x="{sx+sw*0.22+i*sw*0.3:.0f}" y="{fy-70:.0f}" width="{sw*0.26:.0f}" height="26" rx="8" fill="#e6e6ea" opacity=".85"/>')
    else:  # диван
        sy = fy - 70
        inner.append(f'<rect x="{sx:.0f}" y="{sy:.0f}" width="{sw:.0f}" height="70" rx="12" fill="{col}"/>')
        inner.append(f'<rect x="{sx:.0f}" y="{sy-42:.0f}" width="{sw:.0f}" height="46" rx="10" fill="{col}" opacity=".78"/>')
        for i in range(3):
            inner.append(f'<rect x="{sx+16+i*sw*0.3:.0f}" y="{sy-30:.0f}" width="{sw*0.22:.0f}" height="34" rx="6" fill="#b9c0cb" opacity=".55"/>')
    # ковёр + столик
    if rnd.random() < 0.8:
        inner.append(f'<ellipse cx="{sx+sw*0.55:.0f}" cy="{fy+58:.0f}" rx="{w_*0.25:.0f}" ry="32" fill="#3d3a44" opacity=".75"/>')
        tx = sx + sw * 0.3
        inner.append(f'<rect x="{tx:.0f}" y="{fy+26:.0f}" width="{w_*0.17:.0f}" height="11" rx="4" fill="#C9A227" opacity=".85"/>')
        inner.append(f'<rect x="{tx+8:.0f}" y="{fy+37:.0f}" width="6" height="24" fill="#8a6f1c"/>')
        inner.append(f'<rect x="{tx+w_*0.17-14:.0f}" y="{fy+37:.0f}" width="6" height="24" fill="#8a6f1c"/>')
    # растение
    px = w_ * rnd.uniform(0.86, 0.92)
    inner.append(f'<rect x="{px:.0f}" y="{fy-6:.0f}" width="34" height="42" rx="6" fill="#7a5c43"/>')
    for a in range(-2, 3):
        inner.append(f'<path d="M {px+17:.0f} {fy-4:.0f} q {a*22} -46 {a*34} -84" fill="none" stroke="#3f7d4f" '
                     f'stroke-width="7" stroke-linecap="round"/>')
    # картина на стене
    if rnd.random() < 0.6:
        ax = w_ * rnd.uniform(0.1, 0.28)
        ay = h_ * rnd.uniform(0.18, 0.3)
        inner.append(f'<rect x="{ax:.0f}" y="{ay:.0f}" width="{w_*0.14:.0f}" height="{h_*0.16:.0f}" rx="3" fill="#0f1116" stroke="#6b5f4a" stroke-width="3"/>')
        inner.append(f'<rect x="{ax+6:.0f}" y="{ay+6:.0f}" width="{w_*0.14-12:.0f}" height="{h_*0.16-12:.0f}" fill="{PURPLE_L}" opacity=".35"/>')

    body = "".join(inner)
    if mirror:
        body = f'<g transform="translate({w_},0) scale(-1,1)">{body}</g>'
    s += body
    s += f'<rect y="{h_*0.78:.0f}" width="{w_}" height="{h_*0.22:.0f}" fill="url(#fd{uid})"/>'
    s += "</svg>"
    return w(name, s)


# ---------- 4. Офисные сцены (Contact) ----------
def office(name, seed, w_=800, h_=520):
    uid = "O" + str(seed)
    rnd = random.Random(seed)
    s = head(w_, h_, uid)
    s += (f'<defs><linearGradient id="ow{uid}" x1="0" y1="0" x2="0" y2="1">'
          f'<stop offset="0" stop-color="#262A33"/><stop offset="1" stop-color="#14161b"/></linearGradient></defs>')
    s += f'<rect width="{w_}" height="{h_}" fill="url(#ow{uid})"/>'
    fy = h_ * 0.7
    s += f'<rect y="{fy:.0f}" width="{w_}" height="{h_-fy:.0f}" fill="#20242b"/>'
    # окна-жалюзи
    s += f'<rect x="{w_*0.05:.0f}" y="{h_*0.1:.0f}" width="{w_*0.4:.0f}" height="{h_*0.42:.0f}" rx="4" fill="#5E7EA8" opacity=".55"/>'
    for i in range(9):
        s += f'<rect x="{w_*0.05:.0f}" y="{h_*0.1+i*h_*0.047:.0f}" width="{w_*0.4:.0f}" height="3" fill="#1b1f26" opacity=".7"/>'
    # стол + люди
    s += f'<rect x="{w_*0.1:.0f}" y="{fy-24:.0f}" width="{w_*0.8:.0f}" height="18" rx="6" fill="#6f5a45"/>'
    n = 3 + seed % 3
    for i in range(n):
        px = w_ * (0.18 + i * (0.64 / max(1, n - 1)))
        col = ["#8C93A1", "#A8724F", "#6E7B8C", "#B08968", "#7C6F9B"][(seed + i) % 5]
        s += f'<circle cx="{px:.0f}" cy="{fy-96:.0f}" r="26" fill="{col}"/>'
        s += f'<path d="M {px-42:.0f} {fy-24:.0f} q 42 -58 84 0 Z" fill="{col}" opacity=".85"/>'
        s += f'<rect x="{px-8:.0f}" y="{fy-66:.0f}" width="16" height="42" fill="#e9e9ee" opacity=".85"/>'
    # ноутбуки
    for i in range(2):
        lx = w_ * (0.3 + i * 0.3)
        s += f'<rect x="{lx:.0f}" y="{fy-52:.0f}" width="52" height="30" rx="3" fill="#2e3440"/>'
        s += f'<rect x="{lx+3:.0f}" y="{fy-49:.0f}" width="46" height="24" rx="2" fill="#8FB6F5" opacity=".7"/>'
    s += "</svg>"
    return w(name, s)


# ---------- 5. Аватары команды ----------
AVA = [("#703BF7", "#3D1E8A"), ("#3B82F7", "#153C87"), ("#F77C3B", "#8A3D13"), ("#2FB8A0", "#12594D")]


def avatar(name, seed, initials, w_=420, h_=520):
    uid = "A" + str(seed)
    c1, c2 = AVA[seed % len(AVA)]
    s = head(w_, h_, uid)
    s += (f'<defs><linearGradient id="ag{uid}" x1="0" y1="0" x2="1" y2="1">'
          f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>')
    s += f'<rect width="{w_}" height="{h_}" fill="#101014"/>'
    s += f'<rect width="{w_}" height="{h_}" fill="url(#ag{uid})" opacity=".85"/>'
    s += (f'<path d="M {w_*0.2:.0f} {h_:.0f} q {w_*0.3:.0f} {-h_*0.3:.0f} {w_*0.6:.0f} 0 Z" '
          f'fill="#0f1015" opacity=".3"/>')
    s += (f'<path d="M {w_*0.22:.0f} {h_:.0f} q {w_*0.28:.0f} {-h_*0.27:.0f} {w_*0.56:.0f} 0 Z" '
          f'fill="#E8E3F5" opacity=".92"/>')
    s += f'<circle cx="{w_*0.5:.0f}" cy="{h_*0.42:.0f}" r="{w_*0.175:.0f}" fill="#0f1015" opacity=".3"/>'
    s += f'<circle cx="{w_*0.5:.0f}" cy="{h_*0.42:.0f}" r="{w_*0.16:.0f}" fill="#E8E3F5" opacity=".95"/>'
    s += (f'<text x="{w_*0.5:.0f}" y="{h_*0.46:.0f}" text-anchor="middle" font-family="Urbanist, Arial, sans-serif" '
          f'font-size="{w_*0.14:.0f}" font-weight="700" fill="{c2}">{initials}</text>')
    s += "</svg>"
    return w(name, s)


# ---------- 6. О компании: дом на ладони ----------
def about_hero(name="about-house.svg", w_=900, h_=620):
    uid = "AB"
    s = head(w_, h_, uid)
    s += (f'<defs><linearGradient id="abg" x1="0" y1="0" x2="0" y2="1">'
          f'<stop offset="0" stop-color="#101021"/><stop offset="1" stop-color="#070711"/></linearGradient></defs>')
    s += f'<rect width="{w_}" height="{h_}" fill="url(#abg)"/>'
    s += contour(uid, w_, h_)
    s += f'<ellipse cx="{w_*0.5:.0f}" cy="{h_*0.42:.0f}" rx="300" ry="200" fill="{PURPLE}" opacity=".14"/>'
    # ладонь
    s += (f'<path d="M {w_*0.14:.0f} {h_*0.95:.0f} q {w_*0.1:.0f} {-h_*0.2:.0f} {w_*0.3:.0f} {-h_*0.22:.0f} '
          f'L {w_*0.78:.0f} {h_*0.7:.0f} q {w_*0.09:.0f} 0 {w_*0.09:.0f} {h_*0.05:.0f} '
          f'q 0 {h_*0.06:.0f} {-w_*0.1:.0f} {h_*0.06:.0f} L {w_*0.3:.0f} {h_*0.95:.0f} Z" fill="#C7A28A"/>')
    s += (f'<path d="M {w_*0.3:.0f} {h_*0.73:.0f} L {w_*0.78:.0f} {h_*0.7:.0f} q {w_*0.09:.0f} 0 {w_*0.09:.0f} {h_*0.05:.0f} '
          f'L {w_*0.3:.0f} {h_*0.79:.0f} Z" fill="#DDB79C"/>')
    # дом
    bx, by, bw_, bh_ = w_ * 0.34, h_ * 0.38, w_ * 0.34, h_ * 0.3
    s += f'<rect x="{bx:.0f}" y="{by:.0f}" width="{bw_:.0f}" height="{bh_:.0f}" rx="5" fill="#F0ECE4"/>'
    s += f'<path d="M {bx-26:.0f} {by:.0f} L {bx+bw_/2:.0f} {by-90:.0f} L {bx+bw_+26:.0f} {by:.0f} Z" fill="#2E3440"/>'
    s += f'<rect x="{bx+bw_*0.6:.0f}" y="{by-66:.0f}" width="24" height="46" fill="#39414f"/>'
    for i in range(2):
        for j in range(2):
            s += (f'<rect x="{bx+bw_*0.12+i*bw_*0.42:.0f}" y="{by+bh_*0.16+j*bh_*0.4:.0f}" '
                  f'width="{bw_*0.28:.0f}" height="{bh_*0.26:.0f}" rx="3" fill="#7EA8E8" opacity=".85"/>')
    s += f'<rect x="{bx+bw_*0.42:.0f}" y="{by+bh_-52:.0f}" width="{bw_*0.16:.0f}" height="52" rx="3" fill="#5C4633"/>'
    # пристройка
    s += f'<rect x="{bx+bw_:.0f}" y="{by+bh_*0.35:.0f}" width="{bw_*0.3:.0f}" height="{bh_*0.65:.0f}" rx="4" fill="#E2DCD2"/>'
    s += (f'<path d="M {bx+bw_-10:.0f} {by+bh_*0.35:.0f} L {bx+bw_*1.15:.0f} {by+bh_*0.1:.0f} '
          f'L {bx+bw_*1.4:.0f} {by+bh_*0.35:.0f} Z" fill="#2E3440"/>')
    s += "</svg>"
    return w(name, s)


# ---------- 7. Фоновые паттерны ----------
def pattern_cta(name="pattern-cta.svg", w_=1440, h_=380):
    s = head(w_, h_, "P")
    s += f'<rect width="{w_}" height="{h_}" fill="none"/>'
    rnd = random.Random(21)
    for i in range(120):
        x = rnd.uniform(0, w_)
        y = rnd.uniform(0, h_)
        sz = rnd.uniform(10, 34)
        rot = rnd.uniform(-25, 25)
        op = rnd.uniform(0.02, 0.08)
        s += (f'<rect x="{x:.0f}" y="{y:.0f}" width="{sz:.0f}" height="{sz:.0f}" rx="3" '
              f'transform="rotate({rot:.0f} {x:.0f} {y:.0f})" fill="none" stroke="#fff" stroke-opacity="{op:.2f}"/>')
    s += "</svg>"
    return w(name, s)


def pattern_lines(name="pattern-lines.svg", w_=1440, h_=700):
    s = head(w_, h_, "L")
    for i in range(14):
        y = h_ * (0.02 + i * 0.075)
        amp = 26 + i * 6
        d = (f"M -40 {y:.0f} C {w_*0.22:.0f} {y-amp:.0f}, {w_*0.55:.0f} {y+amp:.0f}, "
             f"{w_+40:.0f} {y-amp*0.5:.0f}")
        s += f'<path d="{d}" fill="none" stroke="#ffffff" stroke-opacity=".045" stroke-width="1"/>'
    s += "</svg>"
    return w(name, s)


if __name__ == "__main__":
    made = []
    made.append(hero())
    made.append(about_hero())
    made.append(pattern_cta())
    made.append(pattern_lines())

    props = [
        ("properties/seaside-serenity-villa.svg", villa, 11),
        ("properties/metropolitan-haven.svg", cityscape, 12),
        ("properties/rustic-retreat-cottage.svg", cottage, 13),
        ("properties/urban-oasis-loft.svg", cityscape, 14),
        ("properties/coastal-escape-villa.svg", villa, 15),
        ("properties/countryside-charm.svg", cottage, 16),
        ("properties/skyline-penthouse.svg", cityscape, 17),
        ("properties/lakeside-cabin.svg", cottage, 18),
        ("properties/modern-townhouse.svg", villa, 19),
    ]
    for path, fn, sd in props:
        made.append(fn(path, sd))

    for i in range(1, 9):
        made.append(interior(f"interior/interior-{i}.svg", 30 + i))

    for i in range(1, 7):
        made.append(office(f"gallery/office-{i}.svg", 40 + i))

    team = [("team/max-mitchell.svg", "MM"), ("team/sarah-johnson.svg", "SJ"),
            ("team/david-brown.svg", "DB"), ("team/michael-turner.svg", "MT")]
    for i, (p, ini) in enumerate(team):
        made.append(avatar(p, i, ini))

    for i, ini in enumerate(["WW", "ET", "JM"]):
        made.append(avatar(f"team/review-{i+1}.svg", i + 1, ini, 160, 160))

    print(f"OK: {len(made)} files")
