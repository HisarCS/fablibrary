"""Regenerates all v1 files.
Usage (from repo root):  python projects/welcome-space/generators/build.py
Parameters live at the top of each script (e.g. SLOT_W, SLOT_L, WSLOT_L)."""
import os, subprocess, shutil, sys, tempfile
here = os.path.dirname(os.path.abspath(__file__))
proj = os.path.dirname(here)
dest = {'print_cut.svg': 'stickers', 'card.svg': 'teaching', 'gs24_cut.svg': 'laser', 'laser.svg': 'laser', '.scad': '3d', 'drawing.svg': 'drawings', 'illustration.svg': 'drawings'}
with tempfile.TemporaryDirectory() as tmp:
    env = dict(os.environ, OUT=tmp + os.sep)
    for s in ['base_diffuser_comb.py', 'panel_nosecone.py', 'wing.py', 'assembly.py', 'hero.py', 'printables.py', 'student_card.py']:
        subprocess.run([sys.executable, os.path.join(here, s)], env=env, check=True)
    for f in sorted(os.listdir(tmp)):
        sub = next((d for k, d in dest.items() if f.endswith(k)), 'drawings')
        shutil.copy(os.path.join(tmp, f), os.path.join(proj, sub, f))
        print(f'{sub}/{f}')
