# v1 Spaceship – Kit List and Parameter Map

Target: 140 students + spares and prototypes = **160 kits**. All values are v1 drafts and will be updated after testing.

## 1. Parts per kit

| # | Part | Qty/kit | Process | File | Total (160) |
|---|---|---|---|---|---|
| 1 | Base plate Ø110 | 1 | Laser, 3 mm birch | `laser/v1_base_plate_laser.svg` | 160 |
| 2 | Body panel | 3 | Laser, 3 mm birch | `laser/v1_panel_laser.svg` | 480 |
| 3 | Wing | 3 | Laser, 3 mm birch | `laser/v1_wing_laser.svg` | 480 |
| 4 | Nose cone | 1 | 3D, translucent PLA/PETG | `3d/v1_nose_cone.scad` | 160 |
| 5 | Exhaust diffuser | 1 | 3D, translucent PLA/PETG | `3d/v1_diffuser.scad` | 160 |
| 6 | CR2032 holder with cover and switch | 1 | Off the shelf (Motorobit, sample pending) | – | 160 |
| 7 | CR2032 cell | 1 | Off the shelf | – | 160 |
| 8 | 5 mm LED, white | 2 | Off the shelf | – | 320 |
| 9 | 5 mm LED, color | 1 | Off the shelf | – | 160 |
| 10 | Copper rail set (2 rails 54×5 + 6 patches) | 1 | GS-24 cut or by hand | – | 160 |
| 11 | Resistor | 0–3 | Off the shelf, pre-soldered by assistants | Set by testing | TBD |
| 12 | Sticker sheet | 1 | BN-20 print + cut | To be designed | 160 |
| 13 | Double-sided tape (for holder) | 1 piece | Off the shelf | – | 160 |

## 2. Approximate materials (estimates, not measured)

| Material | Per kit | 160 kits |
|---|---|---|
| 3 mm birch plywood | ~0.06 m² (incl. 35% waste) | ~10 m² |
| Translucent filament | ~45 g (nose cone ~22 g + diffuser ~24 g, assuming 100% infill) | ~7.5 kg + test waste → **~9 kg** |
| 5 mm copper tape | ~0.3 m | ~50–60 m |

Print and laser times: **to be measured on the first part**, then split across 17 printers and 3 lasers.

## 3. Per class (outside the kit)

- Multimeter ×3, battery/LED tester ×2–3, tweezers ×5–6
- Spare finished rockets ×5–6
- Spare LEDs, cells, copper tape and stickers (15%)
- Troubleshooting card (5 steps: battery → switch → LED direction → tape contact → leg contact)

## 4. Parameters to change after testing

| Test | Value to measure | File and parameter to change |
|---|---|---|
| Comb test | Best slot width (3.00–3.30) | `generators/base_diffuser_comb.py`: `SLOT_W` (now 3.1) |
| Comb test | Same value | Panel bottom tab 27.8 and wing tab 19.8 (shorten if needed) |
| Nose cone print | Which of 3.2 / 3.3 / 3.4 fits | `3d/v1_nose_cone.scad`: `slotW` |
| Diffuser print | Which of 110.25 / 110.40 / 110.55 fits | `3d/v1_diffuser.scad`: `pocketD` |
| Holder sample | Switch side, height, wire exit | `3d/v1_diffuser.scad`: `winAng`, `winW`, `winZ0`, `winZ1` |
| Electronics bench test | LED type, resistor value, current | This list: #8, #9, #11 |
| Dark room | Does the nose cone glow? | LED direction or `wall` if needed |
| Wing wobble | Does it lean? | Split the wing tab in two |
| Child assembly | Order of steps 4-5-6 | `generators/assembly.py` |
