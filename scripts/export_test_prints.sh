#!/usr/bin/env bash
# Exports the first-week test prints as STL files, one per tolerance value, and checks each one.
# Needs OpenSCAD (sudo apt install openscad) and numpy.
# Usage (from the repo root): bash scripts/export_test_prints.sh
# Output: projects/welcome-space/3d/test-prints/*.stl
set -euo pipefail
SCAD_DIR="projects/welcome-space/3d"
OUT="$SCAD_DIR/test-prints"
mkdir -p "$OUT"
command -v openscad >/dev/null || { echo "openscad not found: sudo apt install openscad"; exit 1; }

for v in 3.2 3.3 3.4; do
  openscad -o "$OUT/v1_nose_cone_slotW${v}.stl" -D "slotW=${v}" "$SCAD_DIR/v1_nose_cone.scad"
done
for v in 110.25 110.40 110.55; do
  openscad -o "$OUT/v1_diffuser_pocketD${v}.stl" -D "pocketD=${v}" "$SCAD_DIR/v1_diffuser.scad"
done

python3 scripts/check_stl.py "$OUT"/*.stl
echo
echo "Done. Print one of each value, mark the parts (slotW / pocketD) and record which one fits."
