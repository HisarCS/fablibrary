"""Builds the 3D PREVIEW model of the v1 ship from the same parameters as the drawings.
Outputs:
  projects/welcome-space/3d/preview/*.stl      one STL per part + the assembled ship (preview meshes, NOT for printing)
  docs/projects/welcome-space/viewer/model.js  mesh data for the web viewer
Run from the repo root:  python projects/welcome-space/generators/model3d.py
Simplified on purpose: nose-cone slots and the diffuser window are not modeled. Print from the OpenSCAD files."""
import os, math, base64, json, struct
import numpy as np
from scipy.spatial import Delaunay, cKDTree
from matplotlib.path import Path

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
STL_DIR = os.path.join(ROOT, 'projects', 'welcome-space', '3d', 'preview')
VIEW_DIR = os.path.join(ROOT, 'docs', 'projects', 'welcome-space', 'viewer')

# ---- parameters (keep in sync with the generators) ----
PLATE_R, PLATE_T = 55.0, 3.0
Z_TOP = 24.0                     # top of plate = top of diffuser
Z_PL0 = Z_TOP - PLATE_T          # 21
SLOT_W, SLOT_L, SLOT_RC = 3.1, 28.0, 38.0
WSLOT_L, WSLOT_RC = 20.0, 40.0
PANEL_ANG, WING_ANG = [90, 210, 330], [30, 150, 270]
PANEL = [(8,0),(24.1,0),(24.1,-2.5),(51.9,-2.5),(51.9,0),(54,0),(54,30),(21,130),(19,130),(19,140),(11,140),(11,130),(8,130)]
WING = [(26,0),(30.1,0),(30.1,-2.5),(49.9,-2.5),(49.9,0),(63,0),(63,-18),(78,-18),(78,-8),(40,70),(26,70)]
NOSE_R, NOSE_H, NOSE_WALL, HUB_H, HUB_RIN = 23.0, 45.0, 1.2, 12.0, 8.0
NOSE_Z0 = Z_TOP + 130.0
DIFF = dict(H=24.0, Rtop=58.0, Rbot=62.0, wall=1.2, pocketD=110.4, pocketH=3.0, ledgeR=50.0, ledgeT=2.0)

# ---------- geometry helpers ----------
def sample_loop(pts, step):
    out = []
    n = len(pts)
    for i in range(n):
        a = np.array(pts[i], float); b = np.array(pts[(i + 1) % n], float)
        k = max(1, int(math.ceil(np.linalg.norm(b - a) / step)))
        for j in range(k): out.append(a + (b - a) * j / k)
    return np.array(out)

def region(outer, holes=(), step=1.0, hole_step=1.0, grid=3.0):
    lo = sample_loop(outer, step); hls = [sample_loop(h, hole_step) for h in holes]
    allb = np.vstack([lo] + hls)
    tree = cKDTree(allb)
    po = Path(np.array(outer + [outer[0]])); phs = [Path(np.array(h + [h[0]])) for h in holes]
    mn, mx = np.min(lo, 0), np.max(lo, 0)
    gx, gy = np.meshgrid(np.arange(mn[0] + grid / 2, mx[0], grid), np.arange(mn[1] + grid / 2, mx[1], grid))
    g = np.c_[gx.ravel(), gy.ravel()]
    ok = po.contains_points(g)
    for ph in phs: ok &= ~ph.contains_points(g)
    ok &= tree.query(g)[0] > grid * 0.6
    pts = np.vstack([allb, g[ok]])
    tri = Delaunay(pts).simplices
    c = pts[tri].mean(axis=1)
    keep = po.contains_points(c)
    for ph in phs: keep &= ~ph.contains_points(c)
    tri = tri[keep]
    return pts, tri, [lo] + hls

def poly_area(p):
    x, y = p[:, 0], p[:, 1]; return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

def extrude(outer, holes, d0, d1, plane, step=1.0, hole_step=1.0, grid=3.0):
    """Extrude a 2D region between depths d0..d1. plane 'xy': (p,q,d)  'xz': (p,d,q)"""
    pts, tri, loops = region(outer, holes, step, hole_step, grid)
    area = sum(0.5 * abs(np.cross(pts[t[1]] - pts[t[0]], pts[t[2]] - pts[t[0]])) for t in tri)
    ref = poly_area(np.array(outer)) - sum(poly_area(np.array(h)) for h in holes)
    assert abs(area - ref) / ref < 0.01, ('triangulation area mismatch', area, ref)
    def m(p, q, d): return (p, q, d) if plane == 'xy' else (p, d, q)
    def nrm(a, b, c): return (0, 0, 1) if plane == 'xy' else (0, 1, 0)  # sign is irrelevant (two-sided shading)
    V, N = [], []
    for t in tri:
        a, b, c = pts[t]
        for d, flip in ((d1, 1), (d0, -1)):
            tri3 = [m(*a, d), m(*b, d), m(*c, d)]
            V += tri3; N += [nrm(0, 0, 0)] * 3
    for lp in loops:
        n = len(lp)
        for i in range(n):
            p0, p1 = lp[i], lp[(i + 1) % n]
            dx, dy = p1 - p0; L = math.hypot(dx, dy) or 1
            e = (dy / L, -dx / L)
            nn = (e[0], e[1], 0) if plane == 'xy' else (e[0], 0, e[1])
            A, B, C, D = m(*p0, d0), m(*p1, d0), m(*p1, d1), m(*p0, d1)
            V += [A, B, C, A, C, D]; N += [nn] * 6
    return np.array(V, np.float32), np.array(N, np.float32)

def box(x0, x1, y0, y1, z0, z1):
    V, N = [], []
    def quad(a, b, c, d, n): V.extend([a, b, c, a, c, d]); N.extend([n] * 6)
    quad((x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1),(0,0,1)); quad((x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(0,0,-1))
    quad((x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1),(0,-1,0)); quad((x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1),(0,1,0))
    quad((x0,y0,z0),(x0,y1,z0),(x0,y1,z1),(x0,y0,z1),(-1,0,0)); quad((x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1),(1,0,0))
    return np.array(V, np.float32), np.array(N, np.float32)

def revolve(loops, cx=0.0, cy=0.0, seg=64, step=1.0):
    """loops: list of closed (r,z) polylines. Smooth normals along gentle curves, crisp at corners."""
    V, N = [], []
    for loop in loops:
        P = sample_loop(loop, step); n = len(P)
        segn = []
        for i in range(n):
            d = P[(i + 1) % n] - P[i]; L = np.hypot(*d) or 1
            segn.append(np.array([d[1] / L, -d[0] / L]))
        def vn(i, s):  # normal at point i for segment s (i is an endpoint of s)
            other = segn[(i - 1) % n] if s == i else segn[i % n]
            return (segn[s] + other) / np.linalg.norm(segn[s] + other) if np.dot(segn[s], other) > math.cos(math.radians(40)) else segn[s]
        for i in range(n):
            j = (i + 1) % n; s = i
            n0, n1 = vn(i, s), vn(j, s)
            for k in range(seg):
                a0, a1 = 2 * math.pi * k / seg, 2 * math.pi * (k + 1) / seg
                def pt(r, z, a): return (cx + r * math.cos(a), cy + r * math.sin(a), z)
                def nm(nv, a): return (nv[0] * math.cos(a), nv[0] * math.sin(a), nv[1])
                A, B = pt(P[i][0], P[i][1], a0), pt(P[i][0], P[i][1], a1)
                C, D = pt(P[j][0], P[j][1], a1), pt(P[j][0], P[j][1], a0)
                nA, nB, nC, nD = nm(n0, a0), nm(n0, a1), nm(n1, a1), nm(n1, a0)
                V += [A, B, C, A, C, D]; N += [nA, nB, nC, nA, nC, nD]
    return np.array(V, np.float32), np.array(N, np.float32)

def merge(*ms): return np.concatenate([m[0] for m in ms]), np.concatenate([m[1] for m in ms])

def rot_poly_rect(center_r, ang, L, W):
    """rectangle (radial length L, width W) centred at radius center_r, rotated to ang (deg, standard math angle)"""
    a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    cx, cy = center_r * c, center_r * s
    pts = [(-L/2,-W/2),(L/2,-W/2),(L/2,W/2),(-L/2,W/2)]
    return [(cx + p*c - q*s, cy + p*s + q*c) for p, q in pts]

# ---------- parts ----------
parts = []
def add(id, name, group, info, color, alpha, mesh, inst=(0,), explode=(0,0,0), led=None):
    parts.append(dict(id=id, name=name, group=group, info=info, color=color, alpha=alpha, mesh=mesh, inst=list(inst), explode=list(explode), led=led))

# base plate: disc with 3 panel slots + 3 wing slots (viewed from the top, standard math angles)
slots = [rot_poly_rect(SLOT_RC, a, SLOT_L, SLOT_W) for a in PANEL_ANG] + [rot_poly_rect(WSLOT_RC, a, WSLOT_L, SLOT_W) for a in WING_ANG]
circle = [(PLATE_R*math.cos(2*math.pi*i/180), PLATE_R*math.sin(2*math.pi*i/180)) for i in range(180)]
add('plate', 'Base plate', 'plate', 'Laser-cut 3 mm birch plywood, diameter 110 mm. Panels and wings clip into its slots.', [0.91,0.81,0.64], 1.0,
    extrude(circle, slots, Z_PL0, Z_TOP, 'xy', step=2.0, hole_step=1.0, grid=4.0))

def thin(profile):  # panel/wing profile (u, v) -> z = Z_TOP + v ; thickness 3 along y
    pts = [(u, Z_TOP + v) for u, v in profile]
    return extrude(pts, [], -1.5, 1.5, 'xz', step=1.0, grid=3.0)
add('panel', 'Body panel', 'panels', 'Three identical laser-cut panels. Press-fit tabs, no glue. The window is a sticker area.', [0.91,0.81,0.64], 1.0, thin(PANEL), inst=PANEL_ANG, explode=(0,0,40))
add('wing', 'Wing', 'wings', 'Three identical laser-cut wings (shown with a blue sticker). Short slots, so they cannot go in the wrong place.', [0.22,0.54,0.87], 1.0, thin(WING), inst=WING_ANG, explode=(35,0,-12))

# nose cone: translucent shell + hub (slots not modeled)
def ell(r, h, w, n=40):
    return [(r*math.sqrt(max(0, 1-(h*i/n/h)**2)), h*i/n) for i in range(n+1)]
R, H, w = NOSE_R, NOSE_H, NOSE_WALL
outer = [(R*math.sqrt(max(0, 1-(z/H)**2)), z) for z in np.linspace(0, H, 41)]
inner = [((R-w)*math.sqrt(max(0, 1-(z/(H-w))**2)), z) for z in np.linspace(0, H-w, 41)]
shell = outer + inner[::-1]
r12 = (R-w)*math.sqrt(1-(HUB_H/(H-w))**2)
hub = [(HUB_RIN, 0), (R-w, 0), (r12, HUB_H), (HUB_RIN, HUB_H)]
nm = revolve([[(r, z + NOSE_Z0) for r, z in shell], [(r, z + NOSE_Z0) for r, z in hub]], step=2.5)
add('nose', 'Nose cone', 'nose', '3D printed in translucent PLA or PETG. It locks the tops of the three panels together. (Slots not shown in this preview.)', [0.71,0.83,0.96], 0.45, nm, explode=(0,0,80))

# diffuser
D = DIFF; rp = D['pocketD']/2; zl = D['H'] - D['pocketH']; zb = zl - D['ledgeT']
rout = lambda z: D['Rbot'] + (D['Rtop']-D['Rbot'])*z/D['H']
prof = [(rp, D['H']), (D['Rtop'], D['H']), (D['Rbot'], 0), (D['Rbot']-D['wall'], 0), (rout(zb)-D['wall'], zb), (D['ledgeR'], zb), (D['ledgeR'], zl), (rp, zl)]
add('diffuser', 'Exhaust diffuser', 'diffuser', '3D printed, translucent. Holds the plate, hides the electronics and glows when the LEDs are on. (Switch window not shown in this preview.)', [0.71,0.83,0.96], 0.40, revolve([prof], step=3.0), explode=(0,0,-60))

# electronics under the plate. Plan (drawing) x maps to world -x because the bottom view is mirrored.
zt = Z_PL0
rails = merge(box(-44, 10, 4, 9, zt-0.5, zt), box(-44, 10, -9, -4, zt-0.5, zt))
add('rails', 'Copper rails', 'electronics', 'Two copper tape rails, cut on the Roland GS-24. + rail on one side, - rail on the other, 8 mm apart.', [0.85,0.38,0.2], 1.0, rails, explode=(0,0,-30))
add('holder', 'Battery holder', 'electronics', 'Ready-made CR2032 holder with cover and ON/OFF switch (about 24 x 34 x 6 mm). Bought, not made in the lab.', [0.82,0.82,0.8], 0.5, box(12, 46, -12, 12, zt-6.2, zt-0.5), explode=(0,0,-30))
cell = revolve([[(0,0),(10,0),(10,3.2),(0,3.2)]], cx=29, cy=0, seg=48, step=1.0)
cell = (cell[0] + np.array([0,0,zt-5.4], np.float32), cell[1])
add('cell', 'CR2032 cell', 'electronics', 'The 3 V coin cell. It sits in the holder; students never open the cover.', [0.75,0.77,0.8], 1.0, cell, explode=(0,0,-30))
add('switch', 'ON/OFF switch', 'electronics', 'Part of the holder. Reachable from below.', [0.94,0.62,0.15], 1.0, box(40, 46, 6, 11.5, zt-5.5, zt-1.5), explode=(0,0,-30))
# LEDs: body + dome hanging down, legs lying on the rails
led_loop = [(0, 14.0), (2.5, 14.0), (2.5, 20.0), (3.2, 20.0), (3.2, 20.6), (0, 20.6)]
dome = [(2.5*math.sin(t), 14.0 - 2.5*math.cos(t) + 2.5) for t in np.linspace(0, math.pi/2, 10)]
led_body = revolve([[(0, 16.5)] + [(2.5*math.cos(t), 16.5 - 2.5*math.sin(t)) for t in np.linspace(0, math.pi/2, 9)][::-1] + [(2.5, 16.5), (2.5, 20.0), (3.2, 20.0), (3.2, 20.6), (0, 20.6)]], seg=24, step=1.0)
leds = []
for x, col in ((-2, [1,1,1]), (-19, [1,1,1]), (-36, [0.47,0.72,1.0])):
    b = (led_body[0] + np.array([x, 0, 0], np.float32), led_body[1])
    legs = merge(box(x-0.3, x+0.3, 2.0, 6.5, zt-1.1, zt-0.5), box(x-0.3, x+0.3, -6.5, -2.0, zt-1.1, zt-0.5))
    add('led%d' % len(leds), 'LED', 'electronics', 'A 5 mm LED. The long leg lies on the + rail, the short leg on the - rail. Its light goes down into the diffuser.', col, 0.95, merge(b, legs), explode=(0,0,-30), led=[x, 0, 16.0])
    leds.append(x)

# ---------- outputs ----------
def inst_rot(V, N, ang):
    a = math.radians(ang); c, s = math.cos(a), math.sin(a)
    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], np.float32)
    return V @ R.T, N @ R.T

def write_stl(path, V):
    tris = V.reshape(-1, 3, 3)
    with open(path, 'wb') as f:
        f.write(b'FabLibrary v1 PREVIEW mesh - not for printing'.ljust(80, b' '))
        f.write(struct.pack('<I', len(tris)))
        for t in tris:
            n = np.cross(t[1]-t[0], t[2]-t[0]); L = np.linalg.norm(n); n = n/L if L > 0 else n
            f.write(struct.pack('<12fH', *n, *t.ravel(), 0))

os.makedirs(STL_DIR, exist_ok=True); os.makedirs(VIEW_DIR, exist_ok=True)
allV = []
names = {'plate': 'v1_base_plate', 'panel': 'v1_panel', 'wing': 'v1_wing', 'nose': 'v1_nose_cone', 'diffuser': 'v1_diffuser'}
for p in parts:
    V, N = p['mesh']
    world = [inst_rot(V, N, a)[0] for a in p['inst']] if p['id'] in ('panel', 'wing') else [V]
    allV += world
    if p['id'] in names:
        write_stl(os.path.join(STL_DIR, names[p['id']] + '_preview.stl'), V if p['id'] in ('panel', 'wing') else world[0])
write_stl(os.path.join(STL_DIR, 'v1_assembly_preview.stl'), np.concatenate(allV))

def b64(a): return base64.b64encode(a.tobytes()).decode()
out = []
for p in parts:
    V, N = p['mesh']
    q = np.clip(np.round(N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9) * 127), -127, 127).astype(np.int8)
    out.append(dict(id=p['id'], name=p['name'], group=p['group'], info=p['info'], color=p['color'], alpha=p['alpha'],
                    inst=p['inst'], explode=p['explode'], led=p['led'], n=len(V), pos=b64(V.astype(np.float32)), nrm=b64(q)))
with open(os.path.join(VIEW_DIR, 'model.js'), 'w') as f:
    f.write('window.MODEL=' + json.dumps(dict(parts=out, zmin=0, zmax=NOSE_Z0 + NOSE_H), separators=(',', ':')) + ';\n')
tot = sum(len(p['mesh'][0]) // 3 * (len(p['inst']) if p['id'] in ('panel', 'wing') else 1) for p in parts)
print('parts', len(parts), 'triangles (assembled)', tot, 'model.js KB', os.path.getsize(os.path.join(VIEW_DIR, 'model.js')) // 1024)
