"""Printable / cuttable consumables: GS-24 copper rail band, BN-20 sticker sheet, troubleshooting card.
ASSUMPTIONS (see docs assumptions page): GS-24 can feed a 50 mm wide conductive copper roll; thin rails can be weeded."""
import os, math
OUT = os.environ.get('OUT', './out/')
CUT = '#FF0000'
MAG = '#FF00FF'
HDR = '<?xml version="1.0" encoding="UTF-8"?>\n'

# ---------- 1) GS-24 copper band: 50 mm roll, 3 kit sets (6 rails 54x5, 24+4 patches 6x6) per band
W, H = 50, 88
s = HDR + f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n<g id="CUT-red-hairline">\n'
for i in range(6):
    x = 2.5 + i * 8
    s += f'<rect x="{x}" y="2" width="5" height="54" fill="none" stroke="{CUT}" stroke-width="0.1"/>\n'
for r in range(4):
    for c in range(7):
        s += f'<rect x="{1 + c*7}" y="{60 + r*7}" width="6" height="6" fill="none" stroke="{CUT}" stroke-width="0.1"/>\n'
s += '</g>\n</svg>\n'
open(OUT + 'v1_copper_rails_gs24_cut.svg', 'w').write(s)

# ---------- 2) BN-20 sticker sheet (print + cut), one student sheet 130 x 100 mm
def star(cx, cy, r):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f'{cx + rr*math.cos(a):.2f},{cy + rr*math.sin(a):.2f}')
    return ' '.join(pts)
W, H = 130, 100
pr, cu = '', ''
def both(print_svg, cut_svg):
    global pr, cu
    pr += print_svg; cu += cut_svg
# windows (3) diameter 20
for cx, ring in ((16, '#185FA5'), (40, '#EF9F27'), (64, '#7F77DD')):
    both(f'<circle cx="{cx}" cy="16" r="10" fill="#B5D4F4" stroke="{ring}" stroke-width="1.6"/><ellipse cx="{cx-3}" cy="12" rx="3" ry="2" fill="#ffffff" fill-opacity=".7"/>',
         f'<circle cx="{cx}" cy="16" r="10" fill="none" stroke="{MAG}" stroke-width="0.2"/>')
# planets (3)
for cx, r, col in ((94, 7, '#1D9E75'), (112, 5, '#EF9F27'), (124, 3.5, '#7F77DD')):
    both(f'<circle cx="{cx}" cy="16" r="{r}" fill="{col}"/><rect x="{cx-r}" y="{16-r*0.2}" width="{2*r}" height="{r*0.4}" fill="#ffffff" fill-opacity=".35"/>',
         f'<circle cx="{cx}" cy="16" r="{r}" fill="none" stroke="{MAG}" stroke-width="0.2"/>')
# stars (5)
for cx in (12, 28, 44, 60, 76):
    both(f'<polygon points="{star(cx,36,5)}" fill="#EF9F27"/>', f'<polygon points="{star(cx,36,5)}" fill="none" stroke="{MAG}" stroke-width="0.2"/>')
# wing patterns (3): 28 x 40
for i, x in enumerate((8, 42, 76)):
    base = f'<rect x="{x}" y="46" width="28" height="40" rx="3" fill="{["#378ADD","#E24B4A","#1D9E75"][i]}"/>'
    if i == 0: base += ''.join(f'<rect x="{x}" y="{50+j*9}" width="28" height="3" fill="#ffffff" fill-opacity=".7"/>' for j in range(4))
    if i == 1: base += ''.join(f'<circle cx="{x+7+(j%2)*14}" cy="{54+(j//2)*12}" r="3" fill="#ffffff" fill-opacity=".8"/>' for j in range(6))
    if i == 2: base += ''.join(f'<polyline points="{x+3},{54+j*10} {x+14},{49+j*10} {x+25},{54+j*10}" fill="none" stroke="#ffffff" stroke-width="2"/>' for j in range(3))
    both(base, f'<rect x="{x}" y="46" width="28" height="40" rx="3" fill="none" stroke="{MAG}" stroke-width="0.2"/>')
# stripes (2)
for y, col in ((48, '#E24B4A'), (59, '#EF9F27')):
    both(f'<rect x="108" y="{y}" width="18" height="7" rx="1" fill="{col}"/>', f'<rect x="108" y="{y}" width="18" height="7" rx="1" fill="none" stroke="{MAG}" stroke-width="0.2"/>')
# blank name label (optional)
both('<rect x="8" y="90" width="60" height="8" rx="1.5" fill="#ffffff" stroke="#B4B2A9" stroke-width=".3" stroke-dasharray="1.5 1"/>',
     f'<rect x="8" y="90" width="60" height="8" rx="1.5" fill="none" stroke="{MAG}" stroke-width="0.2"/>')
# bug hunter badge
both('<circle cx="117" cy="82" r="10" fill="#EF9F27"/><text x="117" y="80.5" font-size="3.4" text-anchor="middle" font-family="Arial" font-weight="bold" fill="#412402">BUG</text><text x="117" y="85" font-size="3.4" text-anchor="middle" font-family="Arial" font-weight="bold" fill="#412402">HUNTER</text>',
     f'<circle cx="117" cy="82" r="10" fill="none" stroke="{MAG}" stroke-width="0.2"/>')
s = HDR + f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n<g id="PRINT">{pr}</g>\n<g id="CutContour">{cu}</g>\n</svg>\n'
open(OUT + 'v1_sticker_sheet_print_cut.svg', 'w').write(s)

# ---------- 3) troubleshooting card A6 landscape 148 x 105
W, H = 148, 105
rows = [('Battery', 'Is the cell in, with the + side up? Is it fresh?'),
        ('Switch', 'Is the switch ON?'),
        ('LED direction', 'Long leg to the + rail, short leg to the - rail.'),
        ('Copper tape', 'Is the tape flat and touching at both ends?'),
        ('LED legs', 'Does each leg touch the tape under its patch?')]
s = HDR + f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" rx="4" fill="#ffffff" stroke="#888780" stroke-width=".4"/>\n'
s += f'<text x="8" y="14" font-size="7" font-family="Arial" font-weight="bold" fill="#185FA5">Light not on? Be a Bug Hunter!</text>\n'
for i, (a, b) in enumerate(rows):
    y = 28 + i * 14
    s += f'<circle cx="14" cy="{y}" r="4.6" fill="#185FA5"/><text x="14" y="{y+1.6}" font-size="5" text-anchor="middle" font-family="Arial" font-weight="bold" fill="#ffffff">{i+1}</text>'
    s += f'<text x="24" y="{y-1}" font-size="4.4" font-family="Arial" font-weight="bold" fill="#222">{a}</text><text x="24" y="{y+4.4}" font-size="3.6" font-family="Arial" fill="#444">{b}</text>\n'
s += f'<rect x="8" y="94" width="132" height="8" rx="2" fill="#EAF3FB"/><text x="74" y="99.4" font-size="4" text-anchor="middle" font-family="Arial" fill="#185FA5">Observe &#8594; Guess &#8594; Check &#8594; Fix &#8594; Test again</text>\n</svg>\n'
open(OUT + 'v1_troubleshooting_card.svg', 'w').write(s)
print('ok')
