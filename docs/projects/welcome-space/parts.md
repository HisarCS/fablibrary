# Parts and files

**Everything for this project is on this page:** every part, every file format, the 3D models, the sources and the tools. Click a picture to see it large.

[Download everything as one ZIP](files/welcome-space-sources.zip){ .md-button .md-button--primary download }
[Open the full file list](sources.md){ .md-button }

The ZIP holds every editable file and keeps the repository folder layout. It leaves out the generated bulk (3D explorer data and preview meshes), which the generators rebuild.

## Pick your program

| I use | Take | Where on this page |
|---|---|---|
| **Inkscape** | the Inkscape SVG | "Open it in" column of every laser, Roland and sticker file |
| **Adobe Illustrator** | the Illustrator SVG | same column |
| **Laser or Roland software** (Epilog, xTool, LightBurn, CutStudio) | the DXF or the Illustrator SVG | same column |
| **Onshape or other CAD** | the Onshape sketch (DXF) | same column, and the 3D printed parts table |
| **A slicer** (Bambu Studio) | the STL | 3D printed parts |
| **OpenSCAD** | the `.scad` source | 3D printed parts |
| **Just looking** | the picture, or the 3D explorer | pictures below, [3D explorer](explore-3d.md) |

How the formats differ, and how to build an editable Onshape model: [Files for Inkscape, Illustrator and Onshape](formats.md). How to edit SVG files safely: [Editing the SVG files](edit-svg.md).

!!! warning "Tolerances are estimates"
    All dimensions are estimates until the first tests. Open one file in your own program, measure it (a plate must be **110 mm**), then cut a test piece on scrap plywood. Convert text to outlines before it goes to the laser.

## Model A: electronics under the plate

### Laser and Roland files

| Part | Picture (click to enlarge) | As made | Open it in |
|---|---|---|---|
| **Base plate**<br>Ø110, 3 mm plywood, ×1 | [![v1_base_plate_laser](files/src/projects/welcome-space/exports/web/v1_base_plate_laser.svg){ width="130" }](files/src/projects/welcome-space/exports/web/v1_base_plate_laser.svg) | [SVG](files/v1_base_plate_laser.svg){ download } | [Inkscape](files/src/projects/welcome-space/exports/inkscape/v1_base_plate_laser.svg){ download } · [Illustrator](files/src/projects/welcome-space/exports/illustrator/v1_base_plate_laser.svg){ download } · [DXF](files/src/projects/welcome-space/exports/dxf/v1_base_plate_laser.dxf){ download } · [Onshape sketch](files/src/projects/welcome-space/exports/onshape/v1_base_plate_profile.dxf){ download } |
| **Body panels**<br>3 mm plywood, ×3 | [![v1_panel_laser](files/src/projects/welcome-space/exports/web/v1_panel_laser.svg){ width="130" }](files/src/projects/welcome-space/exports/web/v1_panel_laser.svg) | [SVG](files/v1_panel_laser.svg){ download } | [Inkscape](files/src/projects/welcome-space/exports/inkscape/v1_panel_laser.svg){ download } · [Illustrator](files/src/projects/welcome-space/exports/illustrator/v1_panel_laser.svg){ download } · [DXF](files/src/projects/welcome-space/exports/dxf/v1_panel_laser.dxf){ download } · [Onshape sketch](files/src/projects/welcome-space/exports/onshape/v1_panel_profile.dxf){ download } |
| **Wings**<br>3 mm plywood, ×3 | [![v1_wing_laser](files/src/projects/welcome-space/exports/web/v1_wing_laser.svg){ width="130" }](files/src/projects/welcome-space/exports/web/v1_wing_laser.svg) | [SVG](files/v1_wing_laser.svg){ download } | [Inkscape](files/src/projects/welcome-space/exports/inkscape/v1_wing_laser.svg){ download } · [Illustrator](files/src/projects/welcome-space/exports/illustrator/v1_wing_laser.svg){ download } · [DXF](files/src/projects/welcome-space/exports/dxf/v1_wing_laser.dxf){ download } · [Onshape sketch](files/src/projects/welcome-space/exports/onshape/v1_wing_profile.dxf){ download } |
| **Comb test**<br>slot widths 3.00 to 3.30 mm | [![v1_comb_test_laser](files/src/projects/welcome-space/exports/web/v1_comb_test_laser.svg){ width="130" }](files/src/projects/welcome-space/exports/web/v1_comb_test_laser.svg) | [SVG](files/v1_comb_test_laser.svg){ download } | [Inkscape](files/src/projects/welcome-space/exports/inkscape/v1_comb_test_laser.svg){ download } · [Illustrator](files/src/projects/welcome-space/exports/illustrator/v1_comb_test_laser.svg){ download } · [DXF](files/src/projects/welcome-space/exports/dxf/v1_comb_test_laser.dxf){ download } |
| **Copper rails and patches**<br>Roland GS-24, 50 mm roll, 3 kits per band | [![v1_copper_rails_gs24_cut](files/src/projects/welcome-space/exports/web/v1_copper_rails_gs24_cut.svg){ width="130" }](files/src/projects/welcome-space/exports/web/v1_copper_rails_gs24_cut.svg) | [SVG](files/v1_copper_rails_gs24_cut.svg){ download } | [Inkscape](files/src/projects/welcome-space/exports/inkscape/v1_copper_rails_gs24_cut.svg){ download } · [Illustrator](files/src/projects/welcome-space/exports/illustrator/v1_copper_rails_gs24_cut.svg){ download } · [DXF](files/src/projects/welcome-space/exports/dxf/v1_copper_rails_gs24_cut.dxf){ download } |

### 3D printed parts

| Part | As made | Open it in |
|---|---|---|
| **Nose cone**<br>translucent PLA or PETG, ×1 | [STL](files/v1_nose_cone.stl){ download } · [OpenSCAD](files/v1_nose_cone.scad){ download } | [Onshape sketch](files/src/projects/welcome-space/exports/onshape/v1_nose_cone_profile.dxf){ download } · [View in 3D](viewer/index.html) |
| **Base diffuser**<br>translucent, ×1, shared by Model A and B | [STL](files/v1_diffuser.stl){ download } · [OpenSCAD](files/v1_diffuser.scad){ download } | [Onshape sketch](files/src/projects/welcome-space/exports/onshape/v1_diffuser_profile.dxf){ download } · [View in 3D](viewer/index.html) |

## Model B: LEDs outside

See [Model A or Model B?](models.md) for the differences and the tests.

### Laser and Roland files

| Part | Picture (click to enlarge) | As made | Open it in |
|---|---|---|---|
| **Base plate B**<br>Ø110, 3 panel slots, 3 wing slots, 2 wire holes | [![v1b_base_plate_laser](files/src/projects/welcome-space/exports/web/v1b_base_plate_laser.svg){ width="130" }](files/src/projects/welcome-space/exports/web/v1b_base_plate_laser.svg) | [SVG](files/v1b_base_plate_laser.svg){ download } | [Inkscape](files/src/projects/welcome-space/exports/inkscape/v1b_base_plate_laser.svg){ download } · [Illustrator](files/src/projects/welcome-space/exports/illustrator/v1b_base_plate_laser.svg){ download } · [DXF](files/src/projects/welcome-space/exports/dxf/v1b_base_plate_laser.dxf){ download } · [Onshape sketch](files/src/projects/welcome-space/exports/onshape/v1b_base_plate_profile.dxf){ download } |
| **Panel set B**<br>1 power panel + 2 plain panels | [![v1b_panels_set_laser](files/src/projects/welcome-space/exports/web/v1b_panels_set_laser.svg){ width="130" }](files/src/projects/welcome-space/exports/web/v1b_panels_set_laser.svg) | [SVG](files/v1b_panels_set_laser.svg){ download } | [Inkscape](files/src/projects/welcome-space/exports/inkscape/v1b_panels_set_laser.svg){ download } · [Illustrator](files/src/projects/welcome-space/exports/illustrator/v1b_panels_set_laser.svg){ download } · [DXF](files/src/projects/welcome-space/exports/dxf/v1b_panels_set_laser.dxf){ download } · [Onshape sketch](files/src/projects/welcome-space/exports/onshape/v1b_panels_set_profile.dxf){ download } |
| **Wings B**<br>3 mm plywood, ×3 | [![v1b_wing_laser](files/src/projects/welcome-space/exports/web/v1b_wing_laser.svg){ width="130" }](files/src/projects/welcome-space/exports/web/v1b_wing_laser.svg) | [SVG](files/v1b_wing_laser.svg){ download } | [Inkscape](files/src/projects/welcome-space/exports/inkscape/v1b_wing_laser.svg){ download } · [Illustrator](files/src/projects/welcome-space/exports/illustrator/v1b_wing_laser.svg){ download } · [DXF](files/src/projects/welcome-space/exports/dxf/v1b_wing_laser.dxf){ download } · [Onshape sketch](files/src/projects/welcome-space/exports/onshape/v1b_wing_profile.dxf){ download } |
| **Copper rails B**<br>2 rails 106 mm + patches, Roland GS-24 | [![v1b_copper_rails_gs24_cut](files/src/projects/welcome-space/exports/web/v1b_copper_rails_gs24_cut.svg){ width="130" }](files/src/projects/welcome-space/exports/web/v1b_copper_rails_gs24_cut.svg) | [SVG](files/v1b_copper_rails_gs24_cut.svg){ download } | [Inkscape](files/src/projects/welcome-space/exports/inkscape/v1b_copper_rails_gs24_cut.svg){ download } · [Illustrator](files/src/projects/welcome-space/exports/illustrator/v1b_copper_rails_gs24_cut.svg){ download } · [DXF](files/src/projects/welcome-space/exports/dxf/v1b_copper_rails_gs24_cut.dxf){ download } |

### 3D printed parts

| Part | As made | Open it in |
|---|---|---|
| **Nose cone B**<br>translucent, Ø66 base, ×1 | [STL](files/v1b_nose_cone.stl){ download } · [OpenSCAD](files/v1b_nose_cone.scad){ download } | [Onshape sketch](files/src/projects/welcome-space/exports/onshape/v1b_nose_cone_profile.dxf){ download } · [View in 3D](viewer/index.html?m=b) |
The diffuser is the same part as in Model A.

## Stickers and printable cards

| Part | Picture (click to enlarge) | As made | Open it in |
|---|---|---|---|
| **Sticker sheet**<br>Roland BN-20, print + cut, one per student | [![v1_sticker_sheet_print_cut](files/src/projects/welcome-space/exports/web/v1_sticker_sheet_print_cut.svg){ width="130" }](files/src/projects/welcome-space/exports/web/v1_sticker_sheet_print_cut.svg) | [SVG](files/v1_sticker_sheet_print_cut.svg){ download } | [Inkscape](files/src/projects/welcome-space/exports/inkscape/v1_sticker_sheet_print_cut.svg){ download } · [Illustrator](files/src/projects/welcome-space/exports/illustrator/v1_sticker_sheet_print_cut.svg){ download } · [DXF](files/src/projects/welcome-space/exports/dxf/v1_sticker_sheet_print_cut.dxf){ download } |
| **Troubleshooting card**<br>A6, Bug Hunter | [![v1_troubleshooting_card](files/src/projects/welcome-space/exports/web/v1_troubleshooting_card.svg){ width="130" }](files/src/projects/welcome-space/exports/web/v1_troubleshooting_card.svg) | [SVG](files/v1_troubleshooting_card.svg){ download } | [Inkscape](files/src/projects/welcome-space/exports/inkscape/v1_troubleshooting_card.svg){ download } · [Illustrator](files/src/projects/welcome-space/exports/illustrator/v1_troubleshooting_card.svg){ download } |
| **Student step card**<br>A4, picture-first | [![v1_student_card](files/src/projects/welcome-space/exports/web/v1_student_card.svg){ width="130" }](files/src/projects/welcome-space/exports/web/v1_student_card.svg) | [SVG](files/v1_student_card.svg){ download } | [Inkscape](files/src/projects/welcome-space/exports/inkscape/v1_student_card.svg){ download } · [Illustrator](files/src/projects/welcome-space/exports/illustrator/v1_student_card.svg){ download } |

## Test logs

| File | What it is |
|---|---|
| [bench-test-template.csv](files/bench-test-template.csv){ download } | Electronics bench test log |
| [pilot-log-template.csv](files/pilot-log-template.csv){ download } | Pilot lesson log |
| [ab-test-template.csv](files/ab-test-template.csv){ download } | Model A / B build and test log |
| [ab-decision-template.csv](files/ab-decision-template.csv){ download } | Model A / B weighted decision table |

!!! note "Laser colors"
    Red hairline = cut, black = engrave. In the sticker sheet, magenta is the BN-20 cut line.

## 3D models to look at

Open them in any 3D viewer or slicer preview. They are **simplified previews, not for printing**: slots in the nose cone and the diffuser window are missing. Print from the STL files above.

| Model | File | View online |
|---|---|---|
| Model A, whole ship | [v1_assembly_preview.stl](https://raw.githubusercontent.com/HisarCS/fablibrary/main/projects/welcome-space/3d/preview/v1_assembly_preview.stl){ download } | [3D explorer](viewer/index.html) |
| Model B, whole ship | [v1b_assembly_preview.stl](https://raw.githubusercontent.com/HisarCS/fablibrary/main/projects/welcome-space/3d/preview/v1b_assembly_preview.stl){ download } | [3D explorer](viewer/index.html?m=b) |

In the explorer you can turn the ship, pull it apart, cut it in half and switch between Model A and Model B.

## Game

[Play Mission Control](play.md){ .md-button } A game for iPad that teaches the machines, the circuit, the fit and the build order.

## Sources and tools

Everything above is generated from these files. To change a design, change a number here, then rebuild. Do not edit the generated files by hand.

| File | What it does |
|---|---|
| [generators/build.py](https://raw.githubusercontent.com/HisarCS/fablibrary/main/projects/welcome-space/generators/build.py) | Rebuilds every Model A file |
| [generators/model_b.py](https://raw.githubusercontent.com/HisarCS/fablibrary/main/projects/welcome-space/generators/model_b.py) | Builds every Model B file |
| [generators/model3d.py](https://raw.githubusercontent.com/HisarCS/fablibrary/main/projects/welcome-space/generators/model3d.py) | Builds the Model A 3D preview and explorer data |
| [generators/printables.py](https://raw.githubusercontent.com/HisarCS/fablibrary/main/projects/welcome-space/generators/printables.py) | Copper band, sticker sheet, troubleshooting card |
| [3d/v1_nose_cone.scad](files/v1_nose_cone.scad){ download }, [v1_diffuser.scad](files/v1_diffuser.scad){ download }, [v1b_nose_cone.scad](files/v1b_nose_cone.scad){ download } | The parametric 3D parts |
| [kit-list.md](kit-list.md) | Parts per kit and the parameter map |

Repository scripts: `svg_tool.py` (prepare and check SVG files), `export_formats.py` (Inkscape, Illustrator, DXF, Onshape), `export_stl.sh` (print STL files), `check_stl.py` (check an STL), `export_test_prints.sh` (tolerance test prints). They are in the `scripts` folder of the [repository](https://github.com/HisarCS/fablibrary/tree/main/scripts) and in the ZIP above.

## Drawings

### Base plate and diffuser
![Base plate and diffuser](img/v1_base_diffuser_drawing.svg)

### Panel and nose cone
![Panel and nose cone](img/v1_panel_nosecone_drawing.svg)

### Wing
![Wing](img/v1_wing_drawing.svg)

### Model B
![Model B drawing](img/v1b_drawing.svg)
