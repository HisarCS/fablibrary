# Your own edited SVG files

Put hand-edited SVGs here. **Nothing in this folder is overwritten** by the generators or by `build.py`.

Name them after the original plus what you changed:

```
v1_base_plate_laser__custom-wider-slots.svg
v1_panel_laser__custom-name-engraving.svg
```

Before cutting, check the file:

```bash
python scripts/svg_tool.py check projects/welcome-space/custom/your_file.svg
```

If your edit is a **better design** (not just a one-off), say so in an issue and change the parameter in the generator instead, so everyone gets it.
