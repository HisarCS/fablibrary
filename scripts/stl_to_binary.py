#!/usr/bin/env python3
"""Converts ASCII STL files to binary STL in place (same file name). Binary files are left as they are.
Usage: python scripts/stl_to_binary.py file.stl [more.stl ...]
Standard library only."""
import sys, struct

def is_binary(data):
    return len(data) >= 84 and 84 + struct.unpack('<I', data[80:84])[0] * 50 == len(data)

def parse_ascii(text):
    tris, verts = [], []
    toks = text.split()
    i = 0
    while i < len(toks):
        if toks[i] == 'vertex':
            verts.append((float(toks[i + 1]), float(toks[i + 2]), float(toks[i + 3])))
            if len(verts) == 3:
                tris.append(tuple(verts)); verts = []
            i += 4
        else:
            i += 1
    return tris

def normal(a, b, c):
    u = [b[k] - a[k] for k in range(3)]; v = [c[k] - a[k] for k in range(3)]
    n = [u[1]*v[2] - u[2]*v[1], u[2]*v[0] - u[0]*v[2], u[0]*v[1] - u[1]*v[0]]
    l = sum(x * x for x in n) ** 0.5
    return [x / l for x in n] if l > 0 else [0.0, 0.0, 0.0]

def convert(path):
    data = open(path, 'rb').read()
    if is_binary(data):
        print(f'{path}: already binary'); return
    tris = parse_ascii(data.decode('utf-8', 'ignore'))
    if not tris: sys.exit(f'{path}: no triangles found, file left unchanged')
    out = bytearray(b'Binary STL'.ljust(80, b'\0')) + struct.pack('<I', len(tris))
    for t in tris:
        out += struct.pack('<12fH', *normal(*t), *t[0], *t[1], *t[2], 0)
    open(path, 'wb').write(bytes(out))
    print(f'{path}: {len(tris)} triangles, {len(data)//1024} KB -> {len(out)//1024} KB')

if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    for p in sys.argv[1:]: convert(p)
