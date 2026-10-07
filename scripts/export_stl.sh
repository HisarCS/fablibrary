#!/usr/bin/env bash
# Exports the print-ready STL files from the OpenSCAD sources, checks them, and puts them where the website picks them up.
# Needs OpenSCAD (sudo apt install openscad) and numpy. The STLs are converted to binary to keep them small.
# Usage (from the repo root): bash scripts/export_stl.sh
# Output: projects/welcome-space/3d/stl/*.stl  (the site hook copies them to the download folder)
set -euo pipefail
SRC="projects/welcome-space/3d"
OUT="$SRC/stl"
mkdir -p "$OUT"
command -v openscad >/dev/null || { echo "openscad not found: sudo apt install openscad"; exit 1; }

# Model A and Model B print parts. Add a line here for every new .scad part.
for name in v1_nose_cone v1_diffuser v1b_nose_cone; do
  echo "Exporting $name ..."
  openscad -o "$OUT/$name.stl" "$SRC/$name.scad"
  python3 scripts/stl_to_binary.py "$OUT/$name.stl"
done

python3 scripts/check_stl.py "$OUT"/*.stl
echo
echo "Done. Commit projects/welcome-space/3d/stl/ and push: the site then offers these STL files for download."
