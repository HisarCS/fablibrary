"""Shared mesh helpers (copied from model3d.py so Model B can be generated without re-running Model A)."""
import math, struct
import numpy as np
from scipy.spatial import Delaunay, cKDTree
from matplotlib.path import Path

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


def b64(a):
    import base64
    return base64.b64encode(a.tobytes()).decode()

def xform(mesh, M, t=(0, 0, 0)):
    """Apply a 3x3 matrix M and translation t to (vertices, normals)."""
    V, N = mesh
    M = np.array(M, np.float32)
    return (V @ M.T + np.array(t, np.float32)), (N @ M.T)

def seg(p0, p1, r=0.6):
    """Square-section tube between two 3D points."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0; L = np.linalg.norm(d); d /= L
    a = np.array([0, 0, 1.0]) if abs(d[2]) < 0.9 else np.array([1.0, 0, 0])
    u = np.cross(d, a); u /= np.linalg.norm(u); v = np.cross(d, u)
    C = [p0 + (su*u + sv*v) * r for su, sv in ((1,1),(-1,1),(-1,-1),(1,-1))]
    D = [c + d * L for c in C]
    V, N = [], []
    for i in range(4):
        j = (i + 1) % 4
        n = (C[i] + C[j]) / 2 - p0; n /= np.linalg.norm(n)
        V += [C[i], C[j], D[j], C[i], D[j], D[i]]; N += [n] * 6
    V += [C[0], C[1], C[2], C[0], C[2], C[3], D[0], D[1], D[2], D[0], D[2], D[3]]; N += [-d] * 6 + [d] * 6
    return np.array(V, np.float32), np.array(N, np.float32)
