"""Illustrations of the finished v1 ship: day / night view and personalization examples.
Artistic illustration (not a technical drawing). LEDs sit under the plate, inside the diffuser."""
import os
OUT = os.environ.get('OUT', './out/')
W, WS = '#E8CFA3', '#8A6A3C'
P, PS = '#B5D4F4', '#185FA5'

def rocket(cx, yb, s, night=False, deco=0, wing='#378ADD', led=('#ffffff', '#ffffff', '#378ADD')):
    k = lambda v: v * s
    wd = '#3a2e22' if night else W
    ws = '#8a7457' if night else WS
    g = ''
    # light pool on the table (night)
    if night:
        g += f'<ellipse cx="{cx}" cy="{yb+k(23)}" rx="{k(78)}" ry="{k(8)}" fill="#FFE9A0" fill-opacity=".28"/>'
    # wings
    for sg in (-1, 1):
        g += (f'<path d="M{cx+sg*k(22)} {yb-k(6)}L{cx+sg*k(56)} {yb+k(8)}L{cx+sg*k(20)} {yb-k(66)}Z" '
              f'fill="{wing}" fill-opacity="{.55 if night else .95}" stroke="{ws}" stroke-width=".8"/>')
    # diffuser (skirt) behind the body bottom
    g += (f'<path d="M{cx-k(30)} {yb}H{cx+k(30)}L{cx+k(34)} {yb+k(22)}H{cx-k(34)}Z" '
          f'fill="{"#FFD27A" if night else P}" fill-opacity="{.75 if night else .6}" stroke="{PS}" stroke-width=".8"/>')
    # LEDs + holder under the plate, inside the diffuser
    g += f'<rect x="{cx-k(26)}" y="{yb+k(5)}" width="{k(14)}" height="{k(6)}" rx="1" fill="#D3D1C7" stroke="#5F5E5A" stroke-width=".5"/>'
    for i, dx in enumerate((-4, 8, 20)):
        if night:
            g += f'<circle cx="{cx+k(dx)}" cy="{yb+k(14)}" r="{k(11)}" fill="{led[i]}" fill-opacity=".35"/>'
        g += f'<circle cx="{cx+k(dx)}" cy="{yb+k(10)}" r="{k(2.6)}" fill="{led[i]}" stroke="#5F5E5A" stroke-width=".5"/>'
    # body
    g += (f'<path d="M{cx-k(24)} {yb}L{cx-k(16)} {yb-k(110)}H{cx+k(16)}L{cx+k(24)} {yb}Z" '
          f'fill="{wd}" stroke="{ws}" stroke-width=".8"/>')
    if deco == 0:
        g += f'<rect x="{cx-k(21)}" y="{yb-k(40)}" width="{k(42)}" height="{k(9)}" fill="#E24B4A" fill-opacity="{.6 if night else 1}"/>'
    if deco == 1:
        for x, y in ((-8, -30), (9, -46), (-5, -96), (10, -88)):
            g += f'<circle cx="{cx+k(x)}" cy="{yb+k(y)}" r="{k(3)}" fill="#EF9F27"/>'
        g += f'<circle cx="{cx+k(8)}" cy="{yb-k(24)}" r="{k(5)}" fill="#7F77DD"/>'
    if deco == 2:
        for i, y in enumerate((-48, -36, -24)):
            g += f'<rect x="{cx-k(22)}" y="{yb+k(y)}" width="{k(44)}" height="{k(6)}" fill="{"#1D9E75" if i==1 else "#5DCAA5"}" fill-opacity="{.65 if night else 1}"/>'
    g += f'<circle cx="{cx}" cy="{yb-k(76)}" r="{k(10)}" fill="{"#FFE9A0" if night else P}" stroke="{ws}" stroke-width=".8"/>'
    # nose cone (translucent; brightness to be verified in the dark-room test)
    g += (f'<path d="M{cx-k(17)} {yb-k(110)}Q{cx-k(13)} {yb-k(150)} {cx} {yb-k(166)}Q{cx+k(13)} {yb-k(150)} {cx+k(17)} {yb-k(110)}Z" '
          f'fill="{"#FFF1B8" if night else P}" fill-opacity="{.5 if night else .8}" stroke="{PS}" stroke-width=".8"/>')
    # plate edge
    g += f'<ellipse cx="{cx}" cy="{yb}" rx="{k(30)}" ry="{k(6)}" fill="{wd}" stroke="{ws}" stroke-width=".8"/>'
    return g

def stars(pts):
    return ''.join(f'<circle cx="{x}" cy="{y}" r="1.4" fill="#fff"/>' for x, y in pts)

def label(x, y, t, col):
    return f'<text x="{x}" y="{y}" font-size="13" text-anchor="middle" font-family="Arial" fill="{col}">{t}</text>'

# day + night
svg = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 320" role="img">'
       '<title>v1 spaceship: day and night view</title>'
       '<rect x="0" y="0" width="380" height="320" rx="12" fill="#EAF3FB"/>'
       '<rect x="400" y="0" width="380" height="320" rx="12" fill="#0a0f24"/>'
       '<line x1="30" y1="287" x2="350" y2="287" stroke="#888780" stroke-width=".8"/>'
       '<line x1="430" y1="287" x2="750" y2="287" stroke="#4a5170" stroke-width=".8"/>')
svg += rocket(190, 258, 1.3, night=False)
svg += stars([(430, 30), (470, 80), (720, 40), (700, 120), (440, 150), (740, 200), (560, 24), (620, 60)])
svg += rocket(590, 258, 1.3, night=True)
svg += label(190, 308, 'Day', '#444441') + label(590, 308, 'Dark room', '#D3D1C7')
svg += '</svg>\n'
open(OUT + 'v1_day_night_illustration.svg', 'w').write(svg)

# personalization
svg = ('<?xml version="1.0" encoding="UTF-8"?>\n'
       '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 260" role="img">'
       '<title>Three personalized v1 ships</title>'
       '<rect x="0" y="0" width="780" height="260" rx="12" fill="#EAF3FB"/>')
svg += rocket(130, 205, .8, deco=0, wing='#E24B4A', led=('#ffffff', '#ffffff', '#E24B4A'))
svg += rocket(390, 205, .8, deco=1, wing='#7F77DD')
svg += rocket(650, 205, .8, deco=2, wing='#1D9E75', led=('#ffffff', '#ffffff', '#5DCAA5'))
svg += label(130, 248, 'Red wings', '#444441') + label(390, 248, 'Stars and planet', '#444441') + label(650, 248, 'Green stripes', '#444441')
svg += '</svg>\n'
open(OUT + 'v1_personalization_illustration.svg', 'w').write(svg)
print('ok')
