# Files for Inkscape, Illustrator and Onshape

The same designs, in the format your program wants. All of them are generated from the sources by `scripts/export_formats.py`, so they always match. They live in the repository folder [`projects/welcome-space/exports`](https://github.com/HisarCS/fablibrary/tree/main/projects/welcome-space/exports) and in the [Source files](sources.md) ZIP.

## Which folder for which program

| I use | Take the files from | What you get |
|---|---|---|
| **Inkscape** | `exports/inkscape/*.svg` | Named layers (CUT, ENGRAVE, PRINT), millimetre display units |
| **Adobe Illustrator** | `exports/illustrator/*.svg` | Plain SVG. Each group becomes a layer named CUT-..., ENGRAVE-... |
| **Laser software** (Epilog, xTool Creative Space, LightBurn) | `exports/dxf/*.dxf` or the Illustrator SVG | DXF with layers CUT (red) and ENGRAVE (black), in millimetres, text kept as text |
| **Onshape** (or any CAD) | `exports/onshape/*.dxf` | Flat profiles and half-profiles for sketches (see below) |
| **A slicer** (Bambu Studio) | `3d/stl/*.stl` | The print-ready meshes |
| **OpenSCAD** | `3d/*.scad` | The parametric source of the 3D printed parts |

!!! warning "Test one file first"
    Every program reads SVG and DXF a little differently. Open one file, measure it against the drawing (a plate must be **110 mm**), then cut a test piece on scrap plywood. Convert text to outlines before it goes to the laser.

## Onshape: what you can and cannot do

- **An STL is only a mesh.** Onshape can show it and measure it, but you cannot change a hole or a width in it. Keep STL for printing and fit checks.
- **To get an editable Onshape model, import the DXF sketches and build the part from them.** Then every dimension is yours to change.

Import a DXF into a Part Studio so that its lines become a sketch, and set the units to **millimetres**. (The names of Onshape's menus change from time to time, so look for "import a DXF into the Part Studio as a sketch".)

### Flat parts (laser cut): extrude 3 mm

| File | Extrude | Notes |
|---|---|---|
| `v1_base_plate_profile.dxf` | the disc, **3 mm** | The circle is the outline, the six rectangles are the slots (3 panel + 3 wing), keep them as holes |
| `v1_panel_profile.dxf` | **3 mm** | Contains the 3 panels: use one |
| `v1_wing_profile.dxf` | **3 mm** | Contains the 3 wings: use one |
| `v1b_base_plate_profile.dxf` | the disc, **3 mm** | Plate for Model B: 3 panel slots, 3 wing slots, 2 wire holes |
| `v1b_panels_set_profile.dxf` | **3 mm** | 3 panel outlines (1 power + 2 plain): use one |
| `v1b_wing_profile.dxf` | **3 mm** | 3 wings: use one |

### Round parts (3D printed): revolve 360 degrees

Each DXF holds the half-profile and a straight line called AXIS. Revolve the profile around the AXIS line.

| File | Revolve | Then add |
|---|---|---|
| `v1_diffuser_profile.dxf` | one closed profile | A window 14 mm wide through the wall at 180 degrees, from 8 to 18 mm above the table (parameters in `3d/v1_diffuser.scad`) |
| `v1_nose_cone_profile.dxf` | two closed profiles: the shell and the hub | 3 pockets 9 x 3.3 mm, radial, 11 mm deep, at 90 / 210 / 330 degrees |
| `v1b_nose_cone_profile.dxf` | the shell and the hub | 3 pockets 12.4 x 3.3 mm, **tangential**, 10 mm deep, at radius 15 mm, at 90 / 210 / 330 degrees |

The curved line of a nose cone is part of an ellipse. The DXF stores it as many short lines. To make it cleaner in Onshape, replace it with an ellipse: Model A has semi-axes **23 and 45 mm**, Model B **33 and 50 mm**, wall 1.2 mm.

### Where the parts sit (Model A, millimetres above the table)

| Part | Position |
|---|---|
| Diffuser | z 0 to 24 |
| Base plate | z 21 to 24 (flush with the top of the diffuser) |
| Panels | stand on the plate (z 24), 130 tall, tab 2.5 mm into the plate, 10 mm tab up into the nose cone |
| Nose cone | base at z 154, 45 tall |
| Wings | tab 2.5 mm into the plate, outer part hangs 18 mm below the plate top |

Model B: panels are 125 tall, the nose cone base is at z 149 and it is 50 tall.

## How these files were checked

The DXF files were read back with a separate reader and drawn: the plate slot is 28 x 3.1 mm, the plate is 110 x 110 mm, the nose cone profile is 23 wide and 45 tall. They were **not opened in Onshape, Illustrator, LightBurn or the laser programs**. Please test one file in your program and report problems in an issue.

## How to regenerate

After you change a parameter:

```bash
python projects/welcome-space/generators/build.py
python projects/welcome-space/generators/model_b.py
python scripts/svg_tool.py prepare
python scripts/export_formats.py
```
