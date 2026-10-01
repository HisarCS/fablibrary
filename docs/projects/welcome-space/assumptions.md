# Assumptions log

For planning, we **assume all ordered parts have arrived** and all machines work as expected. Each row below is something the design currently depends on but nobody has verified yet. When a test confirms or breaks an assumption, change its status and link the issue.

Status: **Assumed** (not verified) · **Confirmed** · **Broken** (design must change)

| ID | Assumption | Used in | Verify with | Status |
|---|---|---|---|---|
| A1 | Parts orders (holders, LEDs, resistors, multimeters, copper tape) arrive on time | Whole plan | Week 1, Day 1 order issue | Assumed |
| A2 | The Motorobit "CR2032 holder, cover and switch, transparent" is 24 × 34 × 6.2 mm, has wire leads, and the switch and cover are reachable from below | Base plate footprint, diffuser window | Holder sample on arrival | Assumed |
| A3 | A child cannot easily open the holder cover; the cell stays inside | Safety | Hand test with 5 samples | Assumed |
| A4 | The switch survives 100 on/off cycles | Electronics | Bench test | Assumed |
| A5 | The 5 mm copper tape has conductive adhesive (adhesive side to foil side reads as conductive) | Rails, patches | Copper tape check, Day 1 | Assumed |
| A6 | A CR2032 lights white and blue 5 mm LEDs well enough without resistors; 15–25 h of running time | LED set, resistor decision | Bench test, Day 3 | Assumed |
| A7 | Real plywood thickness is 3.0 mm | All slots | Caliper measurement | Assumed |
| A8 | `SLOT_W` 3.1 mm works as a child-friendly fit | Base, panel, wing | Comb test, Day 1 | Assumed |
| A9 | Nose cone `slotW` 3.3 mm and diffuser `pocketD` 110.4 mm fit | 3D parts | 3D test prints, Day 2 | Assumed |
| A10 | Light from the LEDs under the plate reaches and visibly lights the nose cone | Dark-room look | Dark-room test, Day 4 | Assumed |
| A11 | A panel held by one 28 mm tab stands upright once the nose cone is on | Mechanics | Integrated prototype, Day 4 | Assumed |
| A12 | A wing held by one 20 mm tab does not lean or snap | Mechanics | Integrated prototype, Day 4 | Assumed |
| A13 | The GS-24 can feed a 50 mm wide conductive copper roll and thin rails can be weeded; otherwise rails are cut by hand with a jig | Copper band file | GS-24 test, Day 5 | Assumed |
| A14 | BN-20 stickers stick to bare birch plywood and peel cleanly | Sticker sheet | BN-20 test, Day 5 | Assumed |
| A15 | An adult builds a ship in 15–20 min; a child needs 35–45 min | Lesson plan | Integrated prototype, then pilot | Assumed |
| A16 | Filament use is about 45 g per kit (upper bound, 100% infill) | Kit list | First print | Assumed |

## How to update this page

1. Run the test and record it in a *Test result* issue.
2. Change the status in this table and link the issue number.
3. If an assumption is **Broken**, open a pull request that changes the design parameters, and add a line to `CHANGELOG.md`.
