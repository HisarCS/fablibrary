"""MODEL B ("LEDs outside"): closed three-panel body, LEDs and straight copper rails on one 'power panel'.
Model A (existing files) keeps the electronics under the base plate. Generates for Model B:
  laser/v1b_*.svg, drawings/v1b_drawing.svg, 3d/v1b_nose_cone.scad, 3d/preview/v1b_*.stl, viewer/model_b.js
Run from the repo root:  python projects/welcome-space/generators/model_b.py
ASSUMPTIONS (unverified): wires + sandwich joints survive child assembly; the LED sits on the panel face with legs folded onto the rails."""
import os, math, json
import numpy as np
import meshlib as ml
from meshlib import extrude, box, revolve, merge, xform, seg, write_stl, b64, sample_loop

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
PROJ = os.path.join(ROOT, 'projects', 'welcome-space')
LASER, DRAW, SCAD, STL = [os.path.join(PROJ, d) for d in ('laser', 'drawings', '3d', os.path.join('3d', 'preview'))]
VIEW = os.path.join(ROOT, 'docs', 'projects', 'welcome-space', 'viewer')
for d in (LASER, DRAW, SCAD, STL, VIEW): os.makedirs(d, exist_ok=True)

# ---------------- parameters ----------------
Z_TOP, PLATE_T, PLATE_R = 24.0, 3.0, 55.0
Z_PL0 = Z_TOP - PLATE_T
T = 3.0                                  # plywood thickness
RI = 15.0                                # distance of the panel mid-plane from the axis (inradius of the triangle)
PANEL_W, PANEL_H = 46.0, 125.0
TAB_B, TAB_BH = 30.0, 2.5                # bottom tab length / depth into the plate
TAB_T, TAB_TH = 12.0, 9.5                # top tab width / height (goes into the nose cone)
PANEL_ANG = [90, 210, 330]               # outward normal of each panel
POWER_ANG = 330                          # the power panel
CORNER_ANG = [30, 150, 270]              # wings sit at the triangle corners
SLOT_W = 3.1
PSLOT_L = 32.0                           # panel slot length (tangential)
WSLOT_L, WSLOT_RC = 16.0, 44.0           # wing slot
HOLE_D, HOLE_R, HOLE_Y = 4.0, 24.0, 6.5  # wire holes beside the power panel
RAIL_W, RAIL_GAP, RAIL_V0, RAIL_V1 = 5.0, 8.0, 6.0, 112.0
LED_V = [45.0, 75.0, 105.0]
NOSE_R, NOSE_H, NOSE_WALL, HUB_H, HUB_RIN = 33.0, 50.0, 1.2, 12.0, 8.0
POCKET_L, POCKET_W, POCKET_D = 12.4, 3.3, 10.0
NOSE_Z0 = Z_TOP + PANEL_H
WING = [(33,0),(36.1,0),(36.1,-2.5),(51.9,-2.5),(51.9,0),(63,0),(63,-18),(78,-18),(78,-8),(45,70),(33,70)]
WING_TAB = (36.1, 51.9)
DIFF = dict(H=24.0, Rtop=58.0, Rbot=62.0, wall=1.2, pocketD=110.4, pocketH=3.0, ledgeR=50.0, ledgeT=2.0, chamferDz=10.0)
CUT, ENG = '#FF0000', '#000000'
HDR = '<?xml version="1.0" encoding="UTF-8"?>\n'

def panel_outline():  # (p along the width, q = v above the plate top), v up
    return [(0,0),(8,0),(8,-TAB_BH),(8+TAB_B,-TAB_BH),(8+TAB_B,0),(PANEL_W,0),(PANEL_W,PANEL_H),
            (PANEL_W/2+TAB_T/2,PANEL_H),(PANEL_W/2+TAB_T/2,PANEL_H+TAB_TH),(PANEL_W/2-TAB_T/2,PANEL_H+TAB_TH),(PANEL_W/2-TAB_T/2,PANEL_H),(0,PANEL_H)]

def rect_at(cx, cy, L, W, rot):
    a = math.radians(rot); c, s = math.cos(a), math.sin(a)
    return [(cx + p*c - q*s, cy + p*s + q*c) for p, q in ((-L/2,-W/2),(L/2,-W/2),(L/2,W/2),(-L/2,W/2))]
def pol(r, a): return (r*math.cos(math.radians(a)), r*math.sin(math.radians(a)))
def panel_slot(a):
    cx, cy = pol(RI, a); return rect_at(cx, cy, PSLOT_L, SLOT_W, a + 90)
def wing_slot(a):
    cx, cy = pol(WSLOT_RC, a); return rect_at(cx, cy, WSLOT_L, SLOT_W, a)
def local_to_world(x, y, ang):
    a = math.radians(ang); return (x*math.cos(a) - y*math.sin(a), x*math.sin(a) + y*math.cos(a))
def wire_holes():
    return [local_to_world(HOLE_R, s*HOLE_Y, POWER_ANG) for s in (+1, -1)]
def circle_poly(cx, cy, r, n=16): return [(cx + r*math.cos(2*math.pi*i/n), cy + r*math.sin(2*math.pi*i/n)) for i in range(n)]

# ---------------- laser SVGs ----------------
def doc(w, h, body): return HDR + f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">\n{body}</svg>\n'
def poly(pts, stroke, sw=0.1): return '<polygon points="' + ' '.join(f'{x:.3f},{y:.3f}' for x, y in pts) + f'" fill="none" stroke="{stroke}" stroke-width="{sw}"/>\n'
def text(x, y, t, sz=4, a='middle'): return f'<text x="{x}" y="{y}" font-size="{sz}" text-anchor="{a}" font-family="Arial" fill="#000">{t}</text>\n'

# plate (TOP view, x right, y up)
C0 = 55.0
sv = lambda pts: [(C0 + x, C0 - y) for x, y in pts]
cut = f'<circle cx="{C0}" cy="{C0}" r="{PLATE_R}" fill="none" stroke="{CUT}" stroke-width="0.1"/>\n'
for a in PANEL_ANG: cut += poly(sv(panel_slot(a)), CUT)
for a in CORNER_ANG: cut += poly(sv(wing_slot(a)), CUT)
for hx, hy in wire_holes(): cut += f'<circle cx="{C0+hx:.3f}" cy="{C0-hy:.3f}" r="{HOLE_D/2}" fill="none" stroke="{CUT}" stroke-width="0.1"/>\n'
eng = ''
for i, a in enumerate(PANEL_ANG):
    x, y = pol(7.5, a); eng += text(C0 + x, C0 - y + 1.5, str(i + 1), 4.5)
px, py = pol(36, POWER_ANG); eng += text(C0 + px, C0 - py + 1.4, 'POWER PANEL', 3.2)
open(os.path.join(LASER, 'v1b_base_plate_laser.svg'), 'w').write(doc(110, 110, f'<g id="CUT-red-hairline">\n{cut}</g>\n<g id="ENGRAVE-black">\n{eng}</g>\n'))

# panels set: power panel + 2 plain panels (seen from the OUTSIDE)
PW, PH = 58.0, PANEL_H + TAB_TH + TAB_BH + 6
def pan_svg(ox, power):
    base_y = PH - 3 - TAB_BH
    sp = lambda p, q: (ox + 6 + p, base_y - q)
    c = poly([sp(p, q) for p, q in panel_outline()], CUT)
    e = ''
    if power:
        for cxp in (PANEL_W/2 - RAIL_GAP/2 - RAIL_W/2, PANEL_W/2 + RAIL_GAP/2 + RAIL_W/2):
            x0, y0 = sp(cxp - RAIL_W/2, RAIL_V1); e += f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{RAIL_W}" height="{RAIL_V1-RAIL_V0}" fill="none" stroke="{ENG}" stroke-width="0.1"/>\n'
            for v in LED_V + [10.0]:
                x1, y1 = sp(cxp - 3, v + 3); e += f'<rect x="{x1:.2f}" y="{y1:.2f}" width="6" height="6" fill="none" stroke="{ENG}" stroke-width="0.1" stroke-dasharray="1 0.7"/>\n'
        for v in LED_V:
            x1, y1 = sp(PANEL_W/2, v); e += f'<circle cx="{x1:.2f}" cy="{y1:.2f}" r="3" fill="none" stroke="{ENG}" stroke-width="0.1"/>\n'
        xr, yr = sp(PANEL_W/2 + RAIL_GAP/2 + RAIL_W/2, RAIL_V1 + 5); e += text(xr, yr, '+', 6)
        xl, yl = sp(PANEL_W/2 - RAIL_GAP/2 - RAIL_W/2, RAIL_V1 + 5); e += text(xl, yl, '-', 6)
        xb, yb = sp(PANEL_W/2, 2); e += text(xb, yb, 'wires', 3)
    return c, e
c1, e1 = pan_svg(0, True); c2, e2 = pan_svg(PW, False); c3, e3 = pan_svg(2*PW, False)
open(os.path.join(LASER, 'v1b_panels_set_laser.svg'), 'w').write(doc(3*PW, PH, f'<g id="CUT-red-hairline">\n{c1}{c2}{c3}</g>\n<g id="ENGRAVE-black">\n{e1}{e2}{e3}</g>\n'))

# wings
ws = HDR
WW, WH = 90, 100
body = ''
for i in range(3):
    ox = 5 + i * 0 ; oy = 0
for i in range(3):
    ox = i * 62 - 28
    body += poly([(ox + u, 85 - v) for u, v in WING], CUT)
open(os.path.join(LASER, 'v1b_wing_laser.svg'), 'w').write(doc(3*62, 105, f'<g id="CUT-red-hairline">\n{body}</g>\n'))

# GS-24 copper band for the 50 mm roll: 6 rails (106 long) = 3 kits, 28 patches
RL = RAIL_V1 - RAIL_V0
band = ''
for i in range(6): band += f'<rect x="{2.5+i*8}" y="2" width="5" height="{RL}" fill="none" stroke="{CUT}" stroke-width="0.1"/>\n'
for r in range(4):
    for c in range(7): band += f'<rect x="{1+c*7}" y="{RL+6+r*7}" width="6" height="6" fill="none" stroke="{CUT}" stroke-width="0.1"/>\n'
open(os.path.join(LASER, 'v1b_copper_rails_gs24_cut.svg'), 'w').write(doc(50, RL + 6 + 28 + 2, f'<g id="CUT-red-hairline">\n{band}</g>\n'))

# ---------------- OpenSCAD nose cone B ----------------
scad = f'''// v1b spaceship (Model B) - nose cone, translucent PLA/PETG
// Units: mm. Print base down, no supports needed (pocket ceilings are 3.3 mm bridges).
R      = {NOSE_R};    // base outer radius
H      = {NOSE_H};    // height
wall   = {NOSE_WALL};   // shell wall
hubH   = {HUB_H};    // hub height
hubRin = {HUB_RIN};     // hub inner radius
// pockets for the 3 panel top tabs (tab {TAB_T} x {T} x {TAB_TH})
pL = {POCKET_L};  // pocket length (tangential)
pW = {POCKET_W};   // pocket width (test 3.2 / 3.3 / 3.4)
pD = {POCKET_D};   // pocket depth
rP = {RI};    // pocket centre radius
N  = 48;
$fn = 120;

function prof(r, h) = concat([[0,0]], [for (i=[0:N]) let(z=h*i/N) [r*sqrt(max(0,1-pow(z/h,2))), z]]);
module solid(r, h) {{ rotate_extrude() polygon(prof(r, h)); }}
module shell() {{ difference() {{ solid(R, H); translate([0,0,-0.01]) solid(R-wall, H-wall); }} }}
module hub() {{
  difference() {{
    intersection() {{ solid(R-wall+0.01, H-wall); cylinder(r=R, h=hubH); }}
    translate([0,0,-1]) cylinder(r=hubRin, h=hubH+2);
    for (a=[{PANEL_ANG[0]},{PANEL_ANG[1]},{PANEL_ANG[2]}]) rotate([0,0,a])
      translate([rP-pW/2, -pL/2, -1]) cube([pW, pL, pD+1]);
  }}
}}
union() {{ shell(); hub(); }}
'''
open(os.path.join(SCAD, 'v1b_nose_cone.scad'), 'w').write(scad)

# ---------------- 3D model ----------------
parts = []
def add(id, name, group, info, color, alpha, mesh, inst=(0,), explode=(0,0,0), led=None):
    parts.append(dict(id=id, name=name, group=group, info=info, color=color, alpha=alpha, mesh=mesh, inst=list(inst), explode=list(explode), led=led))
WOODC = [0.91, 0.81, 0.64]; COPPER = [0.85, 0.38, 0.2]

holes = wire_holes()
slots = [panel_slot(a) for a in PANEL_ANG] + [wing_slot(a) for a in CORNER_ANG]
circle = [(PLATE_R*math.cos(2*math.pi*i/180), PLATE_R*math.sin(2*math.pi*i/180)) for i in range(180)]
add('plate', 'Base plate', 'plate', 'Laser-cut 3 mm plywood, 110 mm. Three straight slots form a triangle for the panels, three short slots hold the wings, two small holes let the battery wires reach the power panel.', WOODC, 1.0,
    extrude(circle, slots + [circle_poly(hx, hy, HOLE_D/2) for hx, hy in holes], Z_PL0, Z_TOP, 'xy', step=2.0, hole_step=1.0, grid=4.0))

pan = extrude([(p, Z_TOP + q) for p, q in panel_outline()], [], -T/2, T/2, 'xz', step=1.0, grid=3.0)
pan = xform(pan, [[0,1,0],[1,0,0],[0,0,1]], (RI, -PANEL_W/2, 0))
add('panel', 'Body panel', 'panels', 'Two plain panels with a big sticker area. Press-fit tabs at the bottom and top, no glue.', WOODC, 1.0, pan, inst=[a for a in PANEL_ANG if a != POWER_ANG], explode=(0,0,40))
add('panel_power', 'Power panel', 'panels', 'The panel that carries the two straight copper rails and the three LEDs, facing outward.', WOODC, 1.0, pan, inst=[POWER_ANG], explode=(0,0,40))

xo = RI + T/2                                    # outer face of a panel (local x)
rail_y = [-(RAIL_GAP/2 + RAIL_W), RAIL_GAP/2]    # y of the rail edges
rails = merge(*[box(xo, xo + 0.3, y0, y0 + RAIL_W, Z_TOP + RAIL_V0, Z_TOP + RAIL_V1) for y0 in rail_y])
add('rails', 'Copper rails', 'electronics', 'Two straight copper tape rails on the outer face of the power panel (cut on the Roland GS-24). The + rail on the right.', COPPER, 1.0, rails, inst=[POWER_ANG], explode=(0,0,40))

led_loop = [(0,0),(3.1,0),(3.1,0.7),(2.5,0.7),(2.5,6.0)] + [(2.5*math.cos(t), 6.0 + 2.5*math.sin(t)) for t in np.linspace(0, math.pi/2, 8)[1:]] + [(0, 8.5)]
led_body = revolve([led_loop], seg=24, step=1.0)
cols = [[1,1,1],[1,1,1],[0.47,0.72,1.0]]
for i, v in enumerate(LED_V):
    z0 = Z_TOP + v
    b = xform(led_body, [[0,0,1],[1,0,0],[0,1,0]], (xo + 0.3, 0, z0))
    legs = merge(box(xo+0.3, xo+0.7, 2.4, 9.0, z0-0.3, z0+0.3), box(xo+0.3, xo+0.7, -6.5, -2.4, z0-0.3, z0+0.3))
    lx, ly = local_to_world(xo + 0.3 + 4.5, 0, POWER_ANG)
    add('led%d' % i, 'LED', 'electronics', 'A 5 mm LED facing outward. Its long leg lies on the + rail, the short leg on the - rail, each under a copper patch.', cols[i], 0.95, merge(b, legs), inst=[POWER_ANG], explode=(0,0,40), led=[lx, ly, z0])
patches = []
for z0 in [Z_TOP + v for v in LED_V] + [Z_TOP + 10.0]:
    for yc in (rail_y[0] + RAIL_W/2, rail_y[1] + RAIL_W/2):
        patches.append(box(xo+0.7, xo+0.95, yc - 3, yc + 3, z0 - 3, z0 + 3))
add('patches', 'Copper patches', 'electronics', 'Small copper tape patches pressing each LED leg and each wire end onto its rail (sandwich joint).', [0.95,0.55,0.35], 1.0, merge(*patches), inst=[POWER_ANG], explode=(0,0,40))

# under the plate: holder, cell, switch, wires
zt = Z_PL0
add('holder', 'Battery holder', 'electronics', 'Ready-made CR2032 holder with cover and ON/OFF switch (about 24 x 34 x 6 mm), under the plate inside the diffuser.', [0.82,0.82,0.8], 0.5, box(-44, -10, -12, 12, zt-6.2, zt-0.5), explode=(0,0,-30))
cell = revolve([[(0,0),(10,0),(10,3.2),(0,3.2)]], cx=-27, cy=0, seg=48, step=1.0)
add('cell', 'CR2032 cell', 'electronics', 'The 3 V coin cell.', [0.75,0.77,0.8], 1.0, (cell[0] + np.array([0,0,zt-5.4], np.float32), cell[1]), explode=(0,0,-30))
add('switch', 'ON/OFF switch', 'electronics', 'Part of the holder, reachable from below.', [0.94,0.62,0.15], 1.0, box(-44, -38, 6, 11.5, zt-5.5, zt-1.5), explode=(0,0,-30))
for sign, name, col, term_y in ((+1, 'plus', [0.85,0.15,0.15], 4.0), (-1, 'minus', [0.12,0.12,0.12], -4.0)):
    hx, hy = local_to_world(HOLE_R, sign*HOLE_Y, POWER_ANG)
    lo = merge(seg((-10, term_y, zt-3), (hx, hy, zt-3)), seg((hx, hy, zt-3), (hx, hy, zt)))
    tx, ty = local_to_world(xo + 0.9, sign*HOLE_Y, POWER_ANG)
    up = merge(seg((hx, hy, zt), (hx, hy, Z_TOP + 10.0)), seg((hx, hy, Z_TOP + 10.0), (tx, ty, Z_TOP + 10.0)))
    add('wire_%s_low' % name, 'Battery wire', 'electronics', 'A short wire from the holder, up through a hole in the plate.', col, 1.0, lo, explode=(0,0,-30))
    add('wire_%s_up' % name, 'Battery wire', 'electronics', 'The wire end is pressed onto the bottom of its rail with a copper patch.', col, 1.0, up, explode=(0,0,40))

wing = extrude([(u, Z_TOP + v) for u, v in WING], [], -T/2, T/2, 'xz', step=1.0, grid=3.0)
add('wing', 'Wing', 'wings', 'Three identical laser-cut wings at the corners of the triangle (shown with a blue sticker). Short slots, so they cannot go in a panel slot.', [0.22,0.54,0.87], 1.0, wing, inst=CORNER_ANG, explode=(35,0,-12))

R, H, w = NOSE_R, NOSE_H, NOSE_WALL
outer = [(R*math.sqrt(max(0, 1-(z/H)**2)), z) for z in np.linspace(0, H, 41)]
inner = [((R-w)*math.sqrt(max(0, 1-(z/(H-w))**2)), z) for z in np.linspace(0, H-w, 41)]
r12 = (R-w)*math.sqrt(1-(HUB_H/(H-w))**2)
hub = [(HUB_RIN, 0), (R-w, 0), (r12, HUB_H), (HUB_RIN, HUB_H)]
nm = revolve([[(r, z + NOSE_Z0) for r, z in outer + inner[::-1]], [(r, z + NOSE_Z0) for r, z in hub]], step=2.5)
add('nose', 'Nose cone', 'nose', '3D printed in translucent plastic. Three pockets in its base take the top tabs of the panels. (Pockets not shown in this preview.)', [0.71,0.83,0.96], 0.45, nm, explode=(0,0,80))

D = DIFF; rp = D['pocketD']/2; zl = D['H'] - D['pocketH']; zb = zl - D['ledgeT']
rout = lambda z: D['Rbot'] + (D['Rtop']-D['Rbot'])*z/D['H']
zc = zb - D['chamferDz']
prof = [(rp, D['H']), (D['Rtop'], D['H']), (D['Rbot'], 0), (D['Rbot']-D['wall'], 0), (rout(zc)-D['wall'], zc), (D['ledgeR'], zb), (D['ledgeR'], zl), (rp, zl)]
add('diffuser', 'Base diffuser', 'diffuser', 'The same 3D printed part as in Model A. It holds the plate and hides the battery holder. Here it does not glow, because the LEDs are outside.', [0.71,0.83,0.96], 0.40, revolve([prof], step=3.0), explode=(0,0,-60))

# ---------------- outputs ----------------
allV = []
names = {'plate': 'v1b_base_plate', 'panel': 'v1b_panel', 'wing': 'v1b_wing', 'nose': 'v1b_nose_cone', 'diffuser': 'v1b_diffuser'}
ROT = ('panel', 'panel_power', 'wing', 'rails', 'patches') + tuple('led%d' % i for i in range(3))
for p in parts:
    V, N = p['mesh']
    world = [ml.inst_rot(V, N, a)[0] for a in p['inst']] if p['id'] in ROT else [V]
    allV += world
    if p['id'] in names: write_stl(os.path.join(STL, names[p['id']] + '_preview.stl'), V if p['id'] in ('panel', 'wing') else world[0])
write_stl(os.path.join(STL, 'v1b_assembly_preview.stl'), np.concatenate(allV))
out = []
for p in parts:
    V, N = p['mesh']
    q = np.clip(np.round(N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9) * 127), -127, 127).astype(np.int8)
    out.append(dict(id=p['id'], name=p['name'], group=p['group'], info=p['info'], color=p['color'], alpha=p['alpha'], inst=p['inst'], explode=p['explode'], led=p['led'], n=len(V), pos=b64(V.astype(np.float32)), nrm=b64(q)))
info = {'panels': 'Body panels (3): closed triangular body. Two plain panels and one power panel with the copper rails and LEDs. Press-fit tabs, no glue.',
        'electronics': 'Model B electronics: the battery holder sits under the plate; two short wires come up through the plate and are pressed onto the bottom of the two straight copper rails on the power panel; the three LEDs face outward on the rails.',
        'nose': 'Nose cone: 3D printed, translucent. Three pockets lock the top tabs of the panels. In Model B it is only decoration: the LEDs shine outward.',
        'diffuser': 'Base diffuser: the same 3D printed part as in Model A. It holds the plate and hides the battery holder.'}
with open(os.path.join(VIEW, 'model_b.js'), 'w') as f:
    f.write('window.MODEL_B=' + json.dumps(dict(name='Model B: LEDs outside', parts=out, info=info, glow=dict(diffuser=False, nose=False)), separators=(',', ':')) + ';\n')
tri = sum(len(p['mesh'][0]) // 3 * (len(p['inst']) if p['id'] in ROT else 1) for p in parts)
print('Model B parts', len(parts), 'triangles', tri, 'model_b.js KB', os.path.getsize(os.path.join(VIEW, 'model_b.js')) // 1024)

# ---------------- dimensioned drawing ----------------
def dimline(x1, y1, x2, y2, t, dx=0, dy=-1.5, a='middle'):
    r = f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="#185FA5" stroke-width="0.25"/>'
    for x, y in ((x1, y1), (x2, y2)): r += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.6" fill="#185FA5"/>'
    return r + f'<text x="{(x1+x2)/2+dx:.2f}" y="{(y1+y2)/2+dy:.2f}" font-size="3.2" text-anchor="{a}" font-family="Arial" fill="#185FA5">{t}</text>\n'
def note(x, y, t, col='#555'): return f'<text x="{x}" y="{y}" font-size="3" font-family="Arial" fill="{col}">{t}</text>\n'
W_, H_ = 300, 212
d = HDR + f'<svg xmlns="http://www.w3.org/2000/svg" width="{W_}mm" height="{H_}mm" viewBox="0 0 {W_} {H_}">\n<rect width="{W_}" height="{H_}" fill="#fff"/>\n'
d += '<text x="8" y="9" font-size="5" font-family="Arial" font-weight="bold" fill="#222">v1b spaceship (Model B, LEDs outside) - plate, power panel, wing, nose cone (dimensions in mm)</text>\n'
cx, cy = 65, 85
mp = lambda x, y: (cx + x, cy - y)
d += f'<circle cx="{cx}" cy="{cy}" r="{PLATE_R}" fill="#E8CFA3" stroke="#8A6A3C" stroke-width="0.4"/>\n'
def wpoly(pts, fill, stroke='#8A6A3C'): return '<polygon points="' + ' '.join('%.2f,%.2f' % mp(x, y) for x, y in pts) + f'" fill="{fill}" stroke="{stroke}" stroke-width="0.4"/>\n'
for a in PANEL_ANG: d += wpoly(panel_slot(a), '#fff')
for a in CORNER_ANG: d += wpoly(wing_slot(a), '#fff')
for hx, hy in holes:
    x, y = mp(hx, hy); d += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{HOLE_D/2}" fill="#fff" stroke="#8A6A3C" stroke-width="0.4"/>\n'
tx_, ty_ = mp(*pol(42, POWER_ANG)); d += f'<text x="{tx_:.1f}" y="{ty_+1:.1f}" font-size="3" text-anchor="middle" font-family="Arial">POWER PANEL</text>\n'
for i, a in enumerate(PANEL_ANG):
    x, y = mp(*pol(7.5, a)); d += f'<text x="{x:.1f}" y="{y+1.5:.1f}" font-size="4.5" text-anchor="middle" font-family="Arial">{i+1}</text>\n'
d += dimline(cx - PLATE_R, cy + 62, cx + PLATE_R, cy + 62, '&#216;110')
d += note(8, 160, 'TOP view of the base plate.')
d += note(8, 165, f'panel slots {PSLOT_L:.0f} x {SLOT_W} at r{RI:.0f}, tangential (a triangle);')
d += note(8, 170, f'wing slots {WSLOT_L:.0f} x {SLOT_W} at r{WSLOT_RC:.0f}, radial, at the corners;')
d += note(8, 175, f'two wire holes &#216;{HOLE_D:.0f} at r{HOLE_R:.0f}, +/-{HOLE_Y} beside the power panel.')
d += note(8, 180, 'width 3.1 = 3.0 + T (comb test).')
# power panel face (outer side)
px0, pbase = 150, 178
pp = lambda p, q: (px0 + p, pbase - q)
d += '<polygon points="' + ' '.join('%.2f,%.2f' % pp(p, q) for p, q in panel_outline()) + '" fill="#E8CFA3" stroke="#8A6A3C" stroke-width="0.4"/>\n'
for cxp in (PANEL_W/2 - RAIL_GAP/2 - RAIL_W/2, PANEL_W/2 + RAIL_GAP/2 + RAIL_W/2):
    x, y = pp(cxp - RAIL_W/2, RAIL_V1); d += f'<rect x="{x:.2f}" y="{y:.2f}" width="{RAIL_W}" height="{RAIL_V1-RAIL_V0}" fill="#D85A30"/>\n'
for v in LED_V:
    x, y = pp(PANEL_W/2, v); d += f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3" fill="#fff" stroke="#555" stroke-width="0.3"/>\n'
x, y = pp(PANEL_W/2 + RAIL_GAP/2 + RAIL_W/2, RAIL_V1 + 3); d += f'<text x="{x:.1f}" y="{y:.1f}" font-size="5" text-anchor="middle" font-family="Arial">+</text>\n'
x, y = pp(PANEL_W/2 - RAIL_GAP/2 - RAIL_W/2, RAIL_V1 + 3); d += f'<text x="{x:.1f}" y="{y:.1f}" font-size="5" text-anchor="middle" font-family="Arial">-</text>\n'
x0, y0 = pp(0, 0); x1, y1 = pp(PANEL_W, 0)
d += dimline(x0, y0 + 8, x1, y1 + 8, f'{PANEL_W:.0f}', dy=4)
d += dimline(px0 - 6, pbase, px0 - 6, pbase - PANEL_H, f'{PANEL_H:.0f}', dx=-2, dy=1, a='end')
xa, ya = pp(PANEL_W/2 - RAIL_GAP/2 - RAIL_W, 30); xb, yb = pp(PANEL_W/2 + RAIL_GAP/2 + RAIL_W, 30)
d += dimline(pp(PANEL_W/2 - RAIL_GAP/2 - RAIL_W, 3)[0], pp(0, 3)[1], pp(PANEL_W/2 + RAIL_GAP/2 + RAIL_W, 3)[0], pp(0, 3)[1], '5 + 8 + 5', dy=-2)
d += note(px0 - 6, 20, 'POWER PANEL, outer face.')
d += note(px0 - 6, 24, 'Rails 106 long (v 6..112),')
d += note(px0 - 6, 28, 'LEDs at v 45 / 75 / 105.')
# wing
wx0, wbase = 222, 100
wp = lambda u, v: (wx0 + (u - 33), wbase - v)
d += '<polygon points="' + ' '.join('%.2f,%.2f' % wp(u, v) for u, v in WING) + '" fill="#378ADD" stroke="#0C447C" stroke-width="0.4"/>\n'
d += dimline(wp(33, 74)[0], wp(33, 74)[1], wp(78, 74)[0], wp(78, 74)[1], '45 (r 33..78)')
d += dimline(wp(80, -18)[0], wp(80, -18)[1], wp(80, 70)[0], wp(80, 70)[1], '88', dx=2, dy=1, a='start')
d += note(wx0 - 14, 124, f'WING: tab {WING_TAB[1]-WING_TAB[0]-0.2:.1f} x 2.5 in a {WSLOT_L:.0f} mm slot.')
d += note(wx0 - 14, 128, 'It sits at a corner of the triangular body.')
# nose cone section
nx, nb = 255, 196
for sg in (1, -1):
    pts = [(nx + sg*r, nb - z) for r, z in outer] + [(nx + sg*r, nb - z) for r, z in inner[::-1]]
    d += '<polygon points="' + ' '.join('%.2f,%.2f' % p for p in pts) + '" fill="#B5D4F4" fill-opacity="0.8" stroke="#185FA5" stroke-width="0.4"/>\n'
d += f'<rect x="{nx-R+w}" y="{nb-HUB_H}" width="{R-w-HUB_RIN}" height="{HUB_H}" fill="#B5D4F4" stroke="#185FA5" stroke-width="0.3"/>\n'
d += f'<rect x="{nx+HUB_RIN}" y="{nb-HUB_H}" width="{R-w-HUB_RIN}" height="{HUB_H}" fill="#B5D4F4" stroke="#185FA5" stroke-width="0.3"/>\n'
d += dimline(nx - R, nb + 6, nx + R, nb + 6, f'&#216;{2*R:.0f} base', dy=4)
d += dimline(nx + R + 6, nb, nx + R + 6, nb - H, f'{H:.0f}', dx=2, dy=1, a='start')
d += note(nx - 36, nb - 58, 'NOSE CONE: 3 pockets 12.4 x 3.3, 10 deep, take the')
d += note(nx - 36, nb - 54, 'panel top tabs (12 x 9.5). Print tip up, no supports.')
d += '</svg>\n'
open(os.path.join(DRAW, 'v1b_drawing.svg'), 'w').write(d)
print('drawing ok')
