# Editing the SVG files

The laser, Roland and drawing files are plain SVG. You can open and edit them in any vector editor. This page shows how to do it safely.

## Which program?

| Program | Cost | Good for |
|---|---|---|
| **Inkscape** | free | Everything on this page. Recommended. Ubuntu: `sudo apt install inkscape` |
| Illustrator, CorelDRAW | paid | Fine, if your laser software is built on them |
| xTool Creative Space, LightBurn | | Open the SVG directly to cut it. Edit in Inkscape first for bigger changes |
| A text editor | free | Change a number or a word. SVG is just text |

## The rules every file follows

| Rule | Why |
|---|---|
| **1 unit = 1 mm.** Size is written in mm (for example `110mm`), and the `viewBox` has the same number. | The file cuts at real size. Keep the document scale at 100%. |
| **Red hairline = cut through.** Line width about 0.1 mm. | Laser software reads thin red as a cut. |
| **Black = engrave.** | Text, marks and guides on the surface. |
| **Magenta `CutContour` = the BN-20 cut line**, with the colors on a separate `PRINT` layer. | The Roland prints the colors and cuts along the magenta line. |
| Each file has named layers: **CUT**, **ENGRAVE** (and **PRINT**, **CUT CONTOUR** for stickers). | Open Inkscape's Layers panel (`Shift+Ctrl+L`) to hide or lock them. |

## Edit, step by step (Inkscape)

1. Open the file. If Inkscape asks about scale, choose the default and keep **mm** as the display unit (Document Properties, `Shift+Ctrl+D`).
2. In the Layers panel, **lock the CUT layer** while you edit the ENGRAVE layer (and the other way round), so you do not move the wrong thing.
3. Make your change. To move or resize something exactly, use the X, Y, W, H boxes in the toolbar, in mm.
4. **Convert text to outlines** before it goes to the machine: select the text, then *Path > Object to Path* (`Shift+Ctrl+C`). Otherwise the machine may use a different font.
5. Save as **Plain SVG** or **Inkscape SVG**, into `projects/welcome-space/custom/` (see below).
6. **Check it** before cutting:

   ```bash
   python scripts/svg_tool.py check projects/welcome-space/custom/your_file.svg
   ```

   It checks scale, colors, line width and text, and says what is wrong.

## Important: where to save your edit

Most SVGs here are **generated** from numbers (`generators/`). If you save your edit over the original, the next rebuild overwrites it.

- **A one-off edit** (a name engraved on one plate, a test piece): save it in **`projects/welcome-space/custom/`** with the name `<original>__custom-<what-you-changed>.svg`. That folder is never overwritten.
- **A real improvement** (a better slot width, a new hole): change the **parameter** in the generator, rebuild, and open an issue. Then every file and the 3D explorer update together.

## Quick fixes in a text editor

| I want to | Change |
|---|---|
| Change the plate diameter | The `r="55"` of the circle in the CUT layer (radius, in mm) |
| Make slots wider | The `height` or `width` of the slot rectangles. The generator parameter is `SLOT_W` |
| Move a label | The `x` and `y` of its `<text>` |
| Hide a layer in the machine software | Delete the layer's `<g> ... </g>` block |

## Check list before you cut

- [ ] `svg_tool.py check` says no errors
- [ ] Measure the finished file's size in the machine software: **110 mm** for a plate, with calipers on the first test piece
- [ ] Text is converted to outlines
- [ ] Red = cut, black = engrave, nothing else
- [ ] First cut on scrap plywood
