#!/usr/bin/env python3
"""Quick sanity check for STL files before slicing.
Usage: python scripts/check_stl.py path/to/file.stl [more.stl ...]
Checks: triangle count, size (bounding box), volume, watertightness, and, when the file name contains
'nose' or 'diffuser', the expected v1 size. Needs only numpy."""
import sys, struct, re, os
import numpy as np

EXPECT = {  # name keyword: (x, y, z) size in mm, tolerance
    'nose': (46.0, 46.0, 45.0),
    'diffuser': (124.0, 124.0, 24.0),
}

def load(path):
    data = open(path, 'rb').read()
    if len(data) >= 84 and 84 + struct.unpack('<I', data[80:84])[0] * 50 == len(data):
        n = struct.unpack('<I', data[80:84])[0]
        a = np.frombuffer(data[84:], dtype=np.dtype([('n', '<f4', 3), ('v', '<f4', (3, 3)), ('a', '<u2')]), count=n)
        return a['v'].astype(np.float64)
    txt = data.decode('utf-8', 'ignore')
    v = np.array([[float(x) for x in m.groups()] for m in re.finditer(r'vertex\s+(\S+)\s+(\S+)\s+(\S+)', txt)])
    return v.reshape(-1, 3, 3)

def check(path):
    T = load(path)
    print(f'\n{os.path.basename(path)}')
    print(f'  triangles: {len(T)}')
    lo, hi = T.reshape(-1, 3).min(0), T.reshape(-1, 3).max(0)
    size = hi - lo
    print(f'  size (mm): {size[0]:.2f} x {size[1]:.2f} x {size[2]:.2f}')
    vol = np.einsum('ij,ij->i', T[:, 0], np.cross(T[:, 1], T[:, 2])).sum() / 6.0
    print(f'  volume: {abs(vol)/1000:.2f} cm3  (about {abs(vol)/1000*1.24:.0f} g of PLA at 100% infill)')
    # watertight: every edge shared by exactly two triangles
    V = np.round(T.reshape(-1, 3), 4)
    _, idx = np.unique(V, axis=0, return_inverse=True)
    idx = idx.reshape(-1, 3)
    edges = np.sort(np.concatenate([idx[:, [0, 1]], idx[:, [1, 2]], idx[:, [2, 0]]]), axis=1)
    _, cnt = np.unique(edges, axis=0, return_counts=True)
    bad = int((cnt != 2).sum())
    print('  watertight: ' + ('yes' if bad == 0 else f'NO ({bad} open or non-manifold edges)'))
    if lo[2] < -0.01 or abs(lo[2]) > 0.01:
        print(f'  note: lowest point is at z={lo[2]:.2f} (slicers usually place it on the bed anyway)')
    # overhang: faces leaning more than 45 degrees past vertical, not on the bed (may need supports)
    nrm = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])
    area = np.linalg.norm(nrm, axis=1) / 2
    nrm = nrm / np.maximum(np.linalg.norm(nrm, axis=1, keepdims=True), 1e-12)
    zc = T[:, :, 2].mean(1)
    zbed = lo[2]
    oh = (nrm[:, 2] < -0.7071) & (zc > zbed + 0.05)
    a = area[oh].sum()
    print(f'  overhang beyond 45 degrees: {a:.0f} mm2' + ('  (looks printable without supports)' if a < 150 else '  (check the slicer preview: supports may be needed)'))
    name = os.path.basename(path).lower()
    for k, exp in EXPECT.items():
        if k in name:
            ok = all(abs(s - e) <= 0.6 for s, e in zip(size, exp))
            print(f'  expected ~{exp[0]:.0f} x {exp[1]:.0f} x {exp[2]:.0f}: ' + ('OK' if ok else 'DIFFERENT, check the model or the export'))
    return bad == 0

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(0 if all([check(p) for p in sys.argv[1:]]) else 1)
