"""Student step card: picture-first, A4 landscape, 8 tiles. Few words, so a grade 4 student can follow it alone."""
import os, math
OUT = os.environ.get('OUT', './out/')
W, H = 297, 210
HDR = '<?xml version="1.0" encoding="UTF-8"?>\n'
WOOD, WS, P, PS = '#E8CFA3', '#8A6A3C', '#B5D4F4', '#185FA5'

def star(cx, cy, r, fill='#EF9F27'):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        rr = r if i % 2 == 0 else r * 0.45
        pts.append(f'{cx + rr*math.cos(a):.2f},{cy + rr*math.sin(a):.2f}')
    return f'<polygon points="{" ".join(pts)}" fill="{fill}"/>'

def txt(x, y, t, sz=5, w='normal', col='#222', a='middle'):
    return f'<text x="{x}" y="{y}" font-size="{sz}" text-anchor="{a}" font-family="Arial" font-weight="{w}" fill="{col}">{t}</text>'

def led(x, y, col='#ffffff', lit=False):
    g = f'<circle cx="{x}" cy="{y}" r="6.5" fill="#FFE9A0" fill-opacity=".6"/>' if lit else ''
    return g + f'<circle cx="{x}" cy="{y}" r="3.2" fill="{col}" stroke="#5F5E5A" stroke-width=".4"/>'

# drawings: local coords, tile 66 wide, drawing area y 14..58, centre x=33
def d1():  # stickers
    return (f'<path d="M20 58L22 16H44L46 58Z" fill="{WOOD}" stroke="{WS}" stroke-width=".5"/>'
            f'<circle cx="33" cy="26" r="6" fill="{P}" stroke="#EF9F27" stroke-width="1.2"/>' + star(27, 40, 3) + star(39, 44, 3) +
            '<circle cx="33" cy="52" r="3" fill="#7F77DD"/>')
def d2():  # rails
    return (f'<circle cx="33" cy="36" r="22" fill="{WOOD}" stroke="{WS}" stroke-width=".5"/>'
            '<rect x="16" y="29" width="34" height="4" fill="#D85A30"/><rect x="16" y="40" width="34" height="4" fill="#D85A30"/>' +
            txt(11, 33, '+', 6, 'bold', '#D85A30') + txt(11, 44, '-', 6, 'bold', '#D85A30'))
def d3():  # LEDs
    g = (f'<circle cx="33" cy="36" r="22" fill="{WOOD}" stroke="{WS}" stroke-width=".5"/>'
         '<rect x="16" y="29" width="34" height="4" fill="#D85A30"/><rect x="16" y="40" width="34" height="4" fill="#D85A30"/>')
    for x, c in ((22, '#ffffff'), (33, '#ffffff'), (44, '#378ADD')):
        g += f'<line x1="{x}" y1="30" x2="{x}" y2="35" stroke="#5F5E5A" stroke-width=".8"/><line x1="{x}" y1="37" x2="{x}" y2="42" stroke="#5F5E5A" stroke-width=".8"/>'
        g += f'<circle cx="{x}" cy="36" r="3" fill="{c}" stroke="#5F5E5A" stroke-width=".4"/>'
    return g + txt(33, 62, 'long leg = +', 4, 'bold', '#D85A30')
def d4():  # battery + ON
    return ('<rect x="10" y="22" width="46" height="26" rx="4" fill="#D3D1C7" stroke="#5F5E5A" stroke-width=".5"/>'
            '<circle cx="28" cy="35" r="9" fill="#F1EFE8" stroke="#5F5E5A" stroke-width=".5"/>' + txt(28, 37, '+', 6, 'bold', '#5F5E5A') +
            '<rect x="40" y="29" width="12" height="12" rx="2" fill="#EF9F27" stroke="#854F0B" stroke-width=".5"/>' + txt(46, 38, 'ON', 4, 'bold', '#412402') +
            led(20, 56, '#ffffff', True) + led(33, 56, '#ffffff', True) + led(46, 56, '#378ADD', True))
def d5():  # panels
    g = f'<ellipse cx="33" cy="52" rx="26" ry="6" fill="{WOOD}" stroke="{WS}" stroke-width=".5"/>'
    for x in (18, 28, 38):
        g += f'<rect x="{x}" y="14" width="9" height="38" fill="{WOOD}" stroke="{WS}" stroke-width=".5" fill-opacity=".95"/>'
    return g
def d6():  # nose + diffuser
    return (f'<path d="M22 28Q23 16 33 10Q43 16 44 28Z" fill="{P}" stroke="{PS}" stroke-width=".5"/>'
            f'<rect x="22" y="28" width="22" height="16" fill="{WOOD}" stroke="{WS}" stroke-width=".5"/>'
            f'<ellipse cx="33" cy="44" rx="14" ry="3.5" fill="{WOOD}" stroke="{WS}" stroke-width=".5"/>'
            f'<path d="M19 44H47L50 56H16Z" fill="{P}" fill-opacity=".7" stroke="{PS}" stroke-width=".5"/>')
def d7():  # wings
    return (f'<path d="M24 20L24 50L8 56L14 36Z" fill="#378ADD" stroke="{WS}" stroke-width=".5"/>'
            f'<path d="M42 20L42 50L58 56L52 36Z" fill="#378ADD" stroke="{WS}" stroke-width=".5"/>'
            f'<rect x="24" y="14" width="18" height="38" fill="{WOOD}" stroke="{WS}" stroke-width=".5"/>'
            f'<path d="M24 14Q26 6 33 4Q40 6 42 14Z" fill="{P}" stroke="{PS}" stroke-width=".5"/>')
def d8():  # lights off
    g = '<rect x="6" y="8" width="54" height="52" rx="6" fill="#0a0f24"/>'
    g += star(14, 16, 2, '#ffffff') + star(52, 22, 2, '#ffffff') + star(48, 12, 1.6, '#ffffff')
    g += f'<path d="M28 36L28 54H38L38 36Q38 24 33 18Q28 24 28 36Z" fill="#FFF1B8" fill-opacity=".85"/>'
    return g + led(27, 56, '#ffffff', True) + led(33, 56, '#ffffff', True) + led(39, 56, '#5DCAA5', True)

tiles = [('Stick', d1), ('Rails', d2), ('LEDs', d3), ('Power ON', d4), ('Panels', d5), ('Nose + plate', d6), ('Wings', d7), ('Lights off!', d8)]
s = HDR + f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}mm" height="{H}mm" viewBox="0 0 {W} {H}">\n<rect width="{W}" height="{H}" fill="#ffffff"/>\n'
s += txt(10, 16, 'Build your spaceship', 11, 'bold', '#185FA5', 'start')
s += txt(10, 25, 'Follow the pictures. Stuck? Use the Bug Hunter card.', 5, 'normal', '#444441', 'start')
for i, (name, fn) in enumerate(tiles):
    col, row = i % 4, i // 4
    x, y = 8 + col * 70, 34 + row * 86
    s += f'<g transform="translate({x},{y})"><rect width="66" height="78" rx="5" fill="#F7F9FC" stroke="#B5D4F4" stroke-width=".6"/>'
    s += f'<g transform="translate(0,2)">{fn()}</g>'
    s += f'<circle cx="9" cy="9" r="5.2" fill="#185FA5"/>' + txt(9, 11, str(i + 1), 6, 'bold', '#ffffff')
    s += txt(33, 72, name, 6, 'bold', '#222')
    s += '</g>\n'
s += txt(10, 205, 'Step 4: do all 3 lights shine?  YES: go on.   NO: Bug Hunter card.', 5, 'bold', '#D85A30', 'start')
s += '</svg>\n'
open(OUT + 'v1_student_card.svg', 'w').write(s)
print('ok')
