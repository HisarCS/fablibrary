"""Illustrations of the finished v1 ship WITH the BN-20 stickers applied: day / night view and personalization examples.
Artistic illustration (not a technical drawing). LEDs sit under the plate, inside the diffuser."""
import os, math
OUT = os.environ.get('OUT', './out/')
W, WS = '#E8CFA3', '#8A6A3C'
P, PS = '#B5D4F4', '#185FA5'
_clip = [0]

def star(cx, cy, r, fill='#EF9F27', op=1):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f'{cx + rr*math.cos(a):.2f},{cy + rr*math.sin(a):.2f}')
    return f'<polygon points="{" ".join(pts)}" fill="{fill}" fill-opacity="{op}"/>'

def wing_pattern(sg, cx, yb, s, kind, night):
    """Sticker pattern clipped to the wing triangle."""
    k = lambda v: v * s
    tri = f'{cx+sg*k(22):.2f},{yb-k(6):.2f} {cx+sg*k(56):.2f},{yb+k(8):.2f} {cx+sg*k(20):.2f},{yb-k(66):.2f}'
    _clip[0] += 1
    cid = f'wc{_clip[0]}'
    op = .55 if night else .9
    g = f'<clipPath id="{cid}"><polygon points="{tri}"/></clipPath><g clip-path="url(#{cid})" fill-opacity="{op}" stroke-opacity="{op}">'
    x0 = cx + sg * k(20)
    if kind == 'stripes':
        for j in range(5):
            y = yb - k(58) + j * k(13)
            g += f'<rect x="{min(x0, x0+sg*k(40)):.2f}" y="{y:.2f}" width="{k(40)}" height="{k(4)}" fill="#ffffff"/>'
    elif kind == 'dots':
        for j in range(6):
            g += f'<circle cx="{x0+sg*k(8+(j%2)*12):.2f}" cy="{yb-k(52)+(j//2)*k(20):.2f}" r="{k(3.4)}" fill="#ffffff"/>'
    elif kind == 'chevron':
        for j in range(4):
            y = yb - k(48) + j * k(15)
            g += (f'<polyline points="{x0:.2f},{y+k(7):.2f} {x0+sg*k(14):.2f},{y:.2f} {x0+sg*k(30):.2f},{y+k(7):.2f}" '
                  f'fill="none" stroke="#ffffff" stroke-width="{k(2.6)}"/>')
    return g + '</g>'

def rocket(cx, yb, s, night=False, kit='full', wing='#378ADD', wingpat=None, ring='#185FA5',
           led=('#ffffff', '#ffffff', '#378ADD')):
    k = lambda v: v * s
    wd = '#3a2e22' if night else W
    ws = '#8a7457' if night else WS
    g = ''
    if night:
        g += f'<ellipse cx="{cx}" cy="{yb+k(23)}" rx="{k(78)}" ry="{k(8)}" fill="#FFE9A0" fill-opacity=".28"/>'
    for sg in (-1, 1):
        g += (f'<path d="M{cx+sg*k(22)} {yb-k(6)}L{cx+sg*k(56)} {yb+k(8)}L{cx+sg*k(20)} {yb-k(66)}Z" '
              f'fill="{wing}" fill-opacity="{.55 if night else .95}" stroke="{ws}" stroke-width=".8"/>')
        if wingpat:
            g += wing_pattern(sg, cx, yb, s, wingpat, night)
    g += (f'<path d="M{cx-k(30)} {yb}H{cx+k(30)}L{cx+k(34)} {yb+k(22)}H{cx-k(34)}Z" '
          f'fill="{"#FFD27A" if night else P}" fill-opacity="{.75 if night else .6}" stroke="{PS}" stroke-width=".8"/>')
    g += f'<rect x="{cx-k(26)}" y="{yb+k(5)}" width="{k(14)}" height="{k(6)}" rx="1" fill="#D3D1C7" stroke="#5F5E5A" stroke-width=".5"/>'
    for i, dx in enumerate((-4, 8, 20)):
        if night:
            g += f'<circle cx="{cx+k(dx)}" cy="{yb+k(14)}" r="{k(11)}" fill="{led[i]}" fill-opacity=".35"/>'
        g += f'<circle cx="{cx+k(dx)}" cy="{yb+k(10)}" r="{k(2.6)}" fill="{led[i]}" stroke="#5F5E5A" stroke-width=".5"/>'
    g += (f'<path d="M{cx-k(24)} {yb}L{cx-k(16)} {yb-k(110)}H{cx+k(16)}L{cx+k(24)} {yb}Z" '
          f'fill="{wd}" stroke="{ws}" stroke-width=".8"/>')
    dim = .6 if night else 1
    # --- stickers on the panel ---
    if kit in ('full', 'stripes'):
        g += f'<rect x="{cx-k(21)}" y="{yb-k(40)}" width="{k(42)}" height="{k(8)}" rx="{k(1)}" fill="#E24B4A" fill-opacity="{dim}"/>'
        g += f'<rect x="{cx-k(21.5)}" y="{yb-k(30)}" width="{k(43)}" height="{k(8)}" rx="{k(1)}" fill="#EF9F27" fill-opacity="{dim}"/>'
    if kit in ('full', 'space'):
        for x, y in ((-9, -52), (9, -62), (-6, -98), (10, -92)):
            g += star(cx + k(x), yb + k(y), k(4.2), '#EF9F27', dim)
        g += (f'<circle cx="{cx-k(9)}" cy="{yb-k(20)}" r="{k(6)}" fill="#1D9E75" fill-opacity="{dim}"/>'
              f'<rect x="{cx-k(15)}" y="{yb-k(21.2)}" width="{k(12)}" height="{k(2.4)}" fill="#ffffff" fill-opacity="{.35*dim}"/>')
        g += f'<circle cx="{cx+k(10)}" cy="{yb-k(18)}" r="{k(3.4)}" fill="#7F77DD" fill-opacity="{dim}"/>'
    if kit == 'bands':
        for i, y in enumerate((-48, -36, -24)):
            g += f'<rect x="{cx-k(22)}" y="{yb+k(y)}" width="{k(44)}" height="{k(6)}" fill="{"#1D9E75" if i==1 else "#5DCAA5"}" fill-opacity="{dim}"/>'
    # window sticker (ring color choice)
    g += (f'<circle cx="{cx}" cy="{yb-k(76)}" r="{k(10)}" fill="{"#FFE9A0" if night else P}" stroke="{ring}" stroke-width="{k(1.6)}"/>'
          f'<ellipse cx="{cx-k(3)}" cy="{yb-k(80)}" rx="{k(3)}" ry="{k(2)}" fill="#ffffff" fill-opacity="{.35 if night else .7}"/>')
    # bug hunter badge (only on the fully decorated ship), lower corner of the panel
    if kit == 'full':
        g += f'<circle cx="{cx+k(11)}" cy="{yb-k(8)}" r="{k(6.5)}" fill="#EF9F27" stroke="#854F0B" stroke-width=".6" fill-opacity="{dim}"/>' + star(cx + k(11), yb - k(8), k(3.8), '#412402', dim)
    g += (f'<path d="M{cx-k(17)} {yb-k(110)}Q{cx-k(13)} {yb-k(150)} {cx} {yb-k(166)}Q{cx+k(13)} {yb-k(150)} {cx+k(17)} {yb-k(110)}Z" '
          f'fill="{"#FFF1B8" if night else P}" fill-opacity="{.5 if night else .8}" stroke="{PS}" stroke-width=".8"/>')
    g += f'<ellipse cx="{cx}" cy="{yb}" rx="{k(30)}" ry="{k(6)}" fill="{wd}" stroke="{ws}" stroke-width=".8"/>'
    return g

def label(x, y, t, col):
    return f'<text x="{x}" y="{y}" font-size="13" text-anchor="middle" font-family="Arial" fill="{col}">{t}</text>'

# ---- day + night, fully decorated (home page hero)
svg = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 320" role="img">'
       '<title>Finished v1 spaceship with stickers: day and dark room</title>'
       '<rect x="0" y="0" width="380" height="320" rx="12" fill="#EAF3FB"/>'
       '<rect x="400" y="0" width="380" height="320" rx="12" fill="#0a0f24"/>'
       '<line x1="30" y1="287" x2="350" y2="287" stroke="#888780" stroke-width=".8"/>'
       '<line x1="430" y1="287" x2="750" y2="287" stroke="#4a5170" stroke-width=".8"/>')
kw = dict(kit='full', wing='#1D9E75', wingpat='chevron', ring='#EF9F27', led=('#ffffff', '#ffffff', '#5DCAA5'))
svg += rocket(190, 258, 1.3, night=False, **kw)
for x, y in ((430, 30), (470, 80), (720, 40), (700, 120), (440, 150), (740, 200), (560, 24), (620, 60)):
    svg += f'<circle cx="{x}" cy="{y}" r="1.4" fill="#fff"/>'
svg += rocket(590, 258, 1.3, night=True, **kw)
svg += label(190, 308, 'Day', '#444441') + label(590, 308, 'Dark room', '#D3D1C7')
svg += '</svg>\n'
open(OUT + 'v1_day_night_illustration.svg', 'w').write(svg)

# ---- personalization (three different sticker choices from the same sheet)
svg = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 260" role="img">'
       '<title>Three personalized v1 ships made from the same sticker sheet</title>'
       '<rect x="0" y="0" width="780" height="260" rx="12" fill="#EAF3FB"/>')
svg += rocket(130, 205, .8, kit='stripes', wing='#378ADD', wingpat='stripes', ring='#185FA5', led=('#ffffff', '#ffffff', '#378ADD'))
svg += rocket(390, 205, .8, kit='space', wing='#E24B4A', wingpat='dots', ring='#7F77DD', led=('#ffffff', '#ffffff', '#E24B4A'))
svg += rocket(650, 205, .8, kit='bands', wing='#1D9E75', wingpat='chevron', ring='#EF9F27', led=('#ffffff', '#ffffff', '#5DCAA5'))
svg += label(130, 248, 'Blue stripes', '#444441') + label(390, 248, 'Stars and planets', '#444441') + label(650, 248, 'Green chevrons', '#444441')
svg += '</svg>\n'
open(OUT + 'v1_personalization_illustration.svg', 'w').write(svg)
print('ok')
