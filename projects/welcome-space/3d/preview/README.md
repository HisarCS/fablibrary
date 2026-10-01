# Preview meshes (not for printing)

These STL files are generated from the same numbers as the drawings by `generators/model3d.py`. They exist so that anyone can look at the design in a 3D viewer, a slicer preview or the website explorer.

- `v1_assembly_preview.stl`: the whole ship, assembled.
- One STL per part type: base plate, panel (1 of 3), wing (1 of 3), nose cone, diffuser.

They are **simplified**: the nose-cone slots and the diffuser switch window are not modeled. **Print from the OpenSCAD files** (`../v1_nose_cone.scad`, `../v1_diffuser.scad`). To export real print STLs:

```bash
sudo apt install openscad
openscad -o v1_nose_cone.stl ../v1_nose_cone.scad
openscad -o v1_diffuser.stl ../v1_diffuser.scad
```

Regenerate the previews (needs `numpy`, `scipy` and `matplotlib`):

```bash
pip install numpy scipy matplotlib
python projects/welcome-space/generators/model3d.py
```
