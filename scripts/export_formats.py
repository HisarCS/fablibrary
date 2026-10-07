#!/usr/bin/env python3
"""Exports every design file in the formats other programs want. Standard library only.

  python scripts/export_formats.py

Writes to projects/<project>/exports/:
  inkscape/     SVG with named layers and millimetre display units (opens ready to edit in Inkscape)
  illustrator/  plain SVG, layers named by group id (Illustrator turns each group into a layer)
  dxf/          one DXF per laser / Roland file: layers CUT (red) and ENGRAVE (black), millimetres, text kept as text
  onshape/      DXF sketches for Onshape: the flat profiles (cut line only) and the half-profiles of the revolved parts
Run it after the generators (build.py, model_b.py) and after 'svg_tool.py prepare'.
Remember: an STL is only a mesh. Onshape cannot edit it as CAD. Use the onshape/ sketches (see docs: 'Files for Inkscape, Illustrator and Onshape')."""
import os, re, sys, glob, math
import xml.etree.ElementTree as ET

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
NS = '{http://www.w3.org/2000/svg}'
INK = 'xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"'
SODI = 'xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"'
ACI = {'CUT': 1, 'ENGRAVE': 7, 'PROFILE': 7, 'AXIS': 5}

# ---------------- SVG variants ----------------
def inkscape_variant(s):
    if INK not in s: s = re.sub(r'<svg ', '<svg ' + INK + ' ', s, count=1)
    if SODI not in s: s = re.sub(r'<svg ', '<svg ' + SODI + ' ', s, count=1)
    if 'sodipodi:namedview' not in s:
        s = re.sub(r'(<svg[^>]*>)', r'\1\n<sodipodi:namedview id="base" inkscape:document-units="mm" units="mm" showgrid="false"/>', s, count=1)
    return s

def illustrator_variant(s):
    s = re.sub(r'\sxmlns:(inkscape|sodipodi)="[^"]*"', '', s)
    s = re.sub(r'<sodipodi:namedview[^>]*/>\n?', '', s)
    s = re.sub(r'\sinkscape:(groupmode|label)="[^"]*"', '', s)
    return s

# ---------------- tiny 2D affine helpers ----------------
def mat_mul(a, b):  # 2x3 affine matrices (a b c d e f)
    return (a[0]*b[0]+a[2]*b[1], a[1]*b[0]+a[3]*b[1], a[0]*b[2]+a[2]*b[3], a[1]*b[2]+a[3]*b[3], a[0]*b[4]+a[2]*b[5]+a[4], a[1]*b[4]+a[3]*b[5]+a[5])
def parse_transform(t):
    M = (1, 0, 0, 1, 0, 0)
    for name, args in re.findall(r'(\w+)\(([^)]*)\)', t or ''):
        v = [float(x) for x in re.split(r'[ ,]+', args.strip()) if x]
        if name == 'translate': T = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif name == 'rotate':
            c, s_ = math.cos(math.radians(v[0])), math.sin(math.radians(v[0])); T = (c, s_, -s_, c, 0, 0)
        elif name == 'scale': T = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        else: T = (1, 0, 0, 1, 0, 0)
        M = mat_mul(M, T)
    return M
def apply(M, p): return (M[0]*p[0] + M[2]*p[1] + M[4], M[1]*p[0] + M[3]*p[1] + M[5])

# ---------------- SVG -> shapes ----------------
def layer_of(gid):
    if gid.startswith('CUT') or gid == 'CutContour': return 'CUT'
    if gid.startswith('ENGRAVE'): return 'ENGRAVE'
    if gid == 'PRINT': return None
    return None

def rounded_rect(x, y, w, h, r):
    if r <= 0: return [(x, y), (x+w, y), (x+w, y+h), (x, y+h)]
    pts = []
    for cx, cy, a0 in ((x+w-r, y+r, -90), (x+w-r, y+h-r, 0), (x+r, y+h-r, 90), (x+r, y+r, 180)):
        for i in range(7):
            a = math.radians(a0 + 90*i/6); pts.append((cx + r*math.cos(a), cy + r*math.sin(a)))
    return pts

def shapes(root_el, default_layer=None):
    out = []
    def walk(el, M, layer):
        for ch in el:
            tag = ch.tag.replace(NS, '')
            m = mat_mul(M, parse_transform(ch.get('transform')))
            if tag == 'g':
                L = layer_of(ch.get('id', '')) or layer
                walk(ch, m, L)
                continue
            if layer is None: continue
            if tag == 'circle':
                out.append(('circle', layer, apply(m, (float(ch.get('cx')), float(ch.get('cy')))), float(ch.get('r'))))
            elif tag == 'rect':
                pts = rounded_rect(float(ch.get('x', 0)), float(ch.get('y', 0)), float(ch.get('width')), float(ch.get('height')), float(ch.get('rx', 0)))
                out.append(('poly', layer, [apply(m, p) for p in pts], True))
            elif tag in ('polygon', 'polyline'):
                nums = [float(v) for v in re.findall(r'-?[\d.]+(?:e-?\d+)?', ch.get('points', ''))]
                pts = list(zip(nums[0::2], nums[1::2]))
                out.append(('poly', layer, [apply(m, p) for p in pts], tag == 'polygon'))
            elif tag == 'text':
                out.append(('text', layer, apply(m, (float(ch.get('x', 0)), float(ch.get('y', 0)))), float(ch.get('font-size', 4)), ''.join(ch.itertext()), ch.get('text-anchor', 'start')))
    walk(root_el, (1, 0, 0, 1, 0, 0), default_layer)
    return out

# ---------------- DXF R12 writer ----------------
class Dxf:
    def __init__(self): self.e = []; self.layers = set()
    def _g(self, *pairs): self.e += [f'{c}\n{v}' for c, v in pairs]
    def circle(self, layer, c, r):
        self.layers.add(layer); self._g((0, 'CIRCLE'), (8, layer), (10, f'{c[0]:.4f}'), (20, f'{c[1]:.4f}'), (30, 0), (40, f'{r:.4f}'))
    def poly(self, layer, pts, closed=True):
        self.layers.add(layer); self._g((0, 'POLYLINE'), (8, layer), (66, 1), (70, 1 if closed else 0))
        for x, y in pts: self._g((0, 'VERTEX'), (8, layer), (10, f'{x:.4f}'), (20, f'{y:.4f}'), (30, 0))
        self._g((0, 'SEQEND'), (8, layer))
    def line(self, layer, a, b):
        self.layers.add(layer); self._g((0, 'LINE'), (8, layer), (10, f'{a[0]:.4f}'), (20, f'{a[1]:.4f}'), (30, 0), (11, f'{b[0]:.4f}'), (21, f'{b[1]:.4f}'), (31, 0))
    def text(self, layer, p, h, s, anchor='start'):
        self.layers.add(layer)
        g = [(0, 'TEXT'), (8, layer), (10, f'{p[0]:.4f}'), (20, f'{p[1]:.4f}'), (30, 0), (40, f'{h:.3f}'), (1, s)]
        if anchor == 'middle': g += [(72, 1), (11, f'{p[0]:.4f}'), (21, f'{p[1]:.4f}'), (31, 0)]
        self._g(*g)
    def dumps(self):
        L = ['0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1009\n9\n$INSUNITS\n70\n4\n0\nENDSEC',
             '0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLTYPE\n70\n1\n0\nLTYPE\n2\nCONTINUOUS\n70\n0\n3\nSolid line\n72\n65\n73\n0\n40\n0.0\n0\nENDTAB',
             '0\nTABLE\n2\nLAYER\n70\n%d' % (len(self.layers) or 1)]
        for n in sorted(self.layers): L.append('0\nLAYER\n2\n%s\n70\n0\n62\n%d\n6\nCONTINUOUS' % (n, ACI.get(n, 7)))
        L.append('0\nENDTAB\n0\nENDSEC')
        L.append('0\nSECTION\n2\nENTITIES\n' + '\n'.join(self.e) + '\n0\nENDSEC\n0\nEOF\n')
        return '\n'.join(L)

def svg_to_dxf(path, cut_only=False, profile_name=None):
    tree = ET.parse(path); r = tree.getroot()
    vb = [float(v) for v in r.get('viewBox').split()]; H = vb[3]
    flip = lambda p: (p[0], H - p[1])
    d = Dxf()
    for s in shapes(r):
        kind, layer = s[0], s[1]
        if cut_only and layer != 'CUT': continue
        L = profile_name or layer
        if kind == 'circle': d.circle(L, flip(s[2]), s[3])
        elif kind == 'poly': d.poly(L, [flip(p) for p in s[2]], s[3])
        elif kind == 'text' and not cut_only: d.text(L, flip(s[2]), s[3], s[4], s[5])
    return d

# ---------------- revolve profiles for Onshape (keep in sync with 3d/*.scad) ----------------
def ellipse_arc(a, b, z0, n=90):
    return [(a * math.sqrt(max(0.0, 1 - (z / b) ** 2)), z) for z in [z0 + (b - z0) * i / n for i in range(n + 1)]]
def nose_profiles(R, H, wall, hubH, hubRin):
    outer = ellipse_arc(R, H, 0)
    inner = ellipse_arc(R - wall, H - wall, 0)
    shell = outer + inner[::-1]
    r12 = (R - wall) * math.sqrt(1 - (hubH / (H - wall)) ** 2)
    hub = [(hubRin, 0), (R - wall, 0), (r12, hubH), (hubRin, hubH)]
    return shell, hub
def diffuser_profile(H=24.0, Rtop=58.0, Rbot=62.0, wall=1.2, pocketD=110.4, pocketH=3.0, ledgeR=50.0, ledgeT=2.0, chamferDz=10.0):
    rp = pocketD / 2; zl = H - pocketH; zb = zl - ledgeT; rout = lambda z: Rbot + (Rtop - Rbot) * z / H; zc = zb - chamferDz
    return [(rp, H), (Rtop, H), (Rbot, 0), (Rbot - wall, 0), (rout(zc) - wall, zc), (ledgeR, zb), (ledgeR, zl), (rp, zl)]

def revolve_dxf(loops, height):
    d = Dxf()
    for lp in loops: d.poly('PROFILE', lp, True)
    d.line('AXIS', (0, -2), (0, height + 4))
    return d

# ---------------- run ----------------
def main():
    n = {'inkscape': 0, 'illustrator': 0, 'dxf': 0, 'onshape': 0}
    for proj in sorted(glob.glob(os.path.join(ROOT, 'projects', '*'))):
        ex = os.path.join(proj, 'exports')
        for sub in n: os.makedirs(os.path.join(ex, sub), exist_ok=True)
        svgs = []
        for d in ('laser', 'stickers', 'teaching', 'drawings', 'custom'): svgs += sorted(glob.glob(os.path.join(proj, d, '*.svg')))
        for f in svgs:
            base = os.path.basename(f); s = open(f, encoding='utf-8').read()
            open(os.path.join(ex, 'inkscape', base), 'w', encoding='utf-8').write(inkscape_variant(s)); n['inkscape'] += 1
            open(os.path.join(ex, 'illustrator', base), 'w', encoding='utf-8').write(illustrator_variant(s)); n['illustrator'] += 1
            parent = os.path.basename(os.path.dirname(f))
            if parent in ('laser', 'stickers', 'custom'):
                d = svg_to_dxf(f)
                if d.e: open(os.path.join(ex, 'dxf', base.replace('.svg', '.dxf')), 'w').write(d.dumps()); n['dxf'] += 1
                if parent == 'laser' and 'copper' not in base and 'comb' not in base:
                    p = svg_to_dxf(f, cut_only=True, profile_name='PROFILE')
                    if p.e: open(os.path.join(ex, 'onshape', base.replace('_laser.svg', '_profile.dxf')), 'w').write(p.dumps()); n['onshape'] += 1
        # revolved parts
        for name, loops, h in (
            ('v1_nose_cone_profile.dxf', nose_profiles(23.0, 45.0, 1.2, 12.0, 8.0), 45.0),
            ('v1b_nose_cone_profile.dxf', nose_profiles(33.0, 50.0, 1.2, 12.0, 8.0), 50.0),
            ('v1_diffuser_profile.dxf', (diffuser_profile(),), 24.0)):
            open(os.path.join(ex, 'onshape', name), 'w').write(revolve_dxf(loops, h).dumps()); n['onshape'] += 1
        open(os.path.join(ex, 'README.md'), 'w').write(
            '# Exports\n\nGenerated by `scripts/export_formats.py`. Do not edit these files by hand: edit the sources and run the script again.\n\n'
            '| Folder | For | Notes |\n|---|---|---|\n'
            '| `inkscape/` | Inkscape | Named layers, millimetre display units |\n'
            '| `illustrator/` | Adobe Illustrator | Plain SVG, each group becomes a layer |\n'
            '| `dxf/` | Laser software, LightBurn, xTool, Epilog, any CAD | Layers CUT (red) and ENGRAVE (black), millimetres |\n'
            '| `onshape/` | Onshape (and any CAD) | Flat profiles and the half-profiles of the revolved parts, for sketches. STL cannot be edited as CAD. |\n')
    print('exported:', ', '.join(f'{v} {k}' for k, v in n.items()))

if __name__ == '__main__':
    main()
