#!/usr/bin/env python3
"""Makes the laser / Roland SVGs friendly to edit by hand, and checks them before they go to a machine.

  python scripts/svg_tool.py prepare            add Inkscape layer names (CUT / ENGRAVE / PRINT / CUT CONTOUR) to every SVG
  python scripts/svg_tool.py check [files...]   check scale, colors, text and line width before cutting

'prepare' is safe to run again and again. Run it after the generators (build.py, model_b.py), because they rewrite the files.
Only the standard library is needed."""
import os, re, sys, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DIRS = ['laser', 'stickers', 'teaching', 'custom']
LAYERS = {
    'CUT-red-hairline': 'CUT: red hairline, cuts through',
    'ENGRAVE-black': 'ENGRAVE: black, engraves',
    'PRINT': 'PRINT: colors for the BN-20',
    'CutContour': 'CUT CONTOUR: magenta, the BN-20 cut line',
}
INK = 'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"'

def svg_files(args=None):
    if args: return args
    out = []
    for proj in glob.glob(os.path.join(ROOT, 'projects', '*')):
        for d in DIRS: out += sorted(glob.glob(os.path.join(proj, d, '*.svg')))
    return out

def prepare():
    n = 0
    for f in svg_files():
        s = open(f, encoding='utf-8').read(); o = s
        if 'inkscape:groupmode' not in s and any(('id="%s"' % k) in s for k in LAYERS):
            if INK not in s: s = re.sub(r'<svg ', '<svg ' + INK + ' ', s, count=1)
            for k, label in LAYERS.items():
                s = s.replace('<g id="%s">' % k, '<g id="%s" inkscape:groupmode="layer" inkscape:label="%s">' % (k, label))
        if s != o:
            open(f, 'w', encoding='utf-8').write(s); n += 1
    print(f'prepared {n} file(s); {len(svg_files())} SVG file(s) in laser/, stickers/, teaching/, custom/')

def mm(v):
    m = re.match(r'^\s*([\d.]+)\s*(mm|cm|in|px)?\s*$', v or '')
    if not m: return None
    x = float(m.group(1)); u = m.group(2) or 'px'
    return {'mm': 1, 'cm': 10, 'in': 25.4, 'px': 25.4 / 96}[u] * x

def check(files):
    bad = 0
    for f in files:
        s = open(f, encoding='utf-8').read(); name = os.path.relpath(f, ROOT); msgs = []
        w = re.search(r'<svg[^>]*\swidth="([^"]+)"', s); h = re.search(r'<svg[^>]*\sheight="([^"]+)"', s)
        vb = re.search(r'viewBox="([\d.\s-]+)"', s)
        if not (w and h and vb): msgs.append('ERROR no width / height / viewBox: scale cannot be trusted')
        else:
            W, H = mm(w.group(1)), mm(h.group(1)); v = [float(x) for x in vb.group(1).split()]
            if W is None or H is None or 'mm' not in w.group(1): msgs.append(f'WARN size is "{w.group(1)} x {h.group(1)}", expected millimetres (e.g. 110mm)')
            elif abs(W - v[2]) > 0.01 or abs(H - v[3]) > 0.01: msgs.append(f'ERROR scale: {W:.2f} x {H:.2f} mm but viewBox is {v[2]:g} x {v[3]:g} (1 unit must be 1 mm)')
        cols = set(c.upper() for c in re.findall(r'stroke="(#[0-9A-Fa-f]{6})"', s))
        if 'laser' in name.replace('\\', '/').split('/'):
            other = sorted(c for c in cols if c not in ('#FF0000', '#000000'))
            if other: msgs.append('WARN strokes other than red (cut) and black (engrave): ' + ', '.join(other))
            fat = [float(x) for x in re.findall(r'stroke="#FF0000"[^>]*stroke-width="([\d.]+)"', s) if float(x) > 0.2]
            if fat: msgs.append('WARN red cut lines thicker than 0.2 mm: the machine may read them as an engraving, not a cut')
        t = len(re.findall(r'<text[ >]', s))
        if t: msgs.append(f'NOTE {t} text element(s): convert text to outlines before sending to the laser (Inkscape: Path > Object to Path)')
        status = 'ERROR' if any(m.startswith('ERROR') for m in msgs) else 'WARN' if any(m.startswith('WARN') for m in msgs) else 'OK'
        bad += status == 'ERROR'
        print(f'[{status}] {name}')
        for m in msgs: print('    ' + m)
    print('\nNo errors.' if not bad else f'\n{bad} file(s) with errors: fix them before cutting.')
    return bad == 0

if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if cmd == 'prepare': prepare()
    elif cmd == 'check': sys.exit(0 if check(svg_files(sys.argv[2:])) else 1)
    else: sys.exit(__doc__)
