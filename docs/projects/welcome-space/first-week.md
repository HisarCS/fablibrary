# First week plan

Goal of the week: **know the real numbers.** Every task ends with a GitHub issue (*Issues → Test result*) containing the measured value, a photo (no student faces) and a decision. Parameters are changed only through a pull request.

Roles: **Lead** (decisions, ordering), **Production** (laser, 3D printers, Roland), **Electronics** (bench tests, class support).

| Day | Role | Task | Done when |
|---|---|---|---|
| 1 | Lead | Order samples: 5 × CR2032 holders with cover and switch (both "single" models), 2 × 2×AAA holders with switch, LED assortment (white, blue, red, green, yellow), resistor set (22, 47, 100, 150, 220 Ω), 3 multimeters, conductive copper tape | Order placed, delivery dates noted in the issue |
| 1 | Production | **Comb test**: cut `v1_comb_test_laser.svg` on the Epilog and on an xTool, from the real plywood. Try each slot with a plywood tab, find the width that slides in by hand without force and does not wobble | Best width for each machine recorded (3.00–3.30 mm) |
| 1 | Electronics | **Copper tape check**: multimeter from the adhesive side to the foil side on 5 spots of each roll | Conductive or not, per roll |
| 2 | Production | **3D test prints**: nose cone with `slotW` 3.2 / 3.3 / 3.4, diffuser with `pocketD` 110.25 / 110.40 / 110.55 (translucent PLA and PETG if possible). Note print time and filament per part | Best values and print times recorded |
| 2 | Lead | Review comb test result, open the pull request that sets `SLOT_W` (base plate, panel tab, wing tab) | PR merged, generators rebuilt |
| 3 | Production | Cut the first full laser set with the new values (base, 3 panels, 3 wings). Sand edges lightly | One complete set, photo |
| 3 | Electronics | **Bench test** when the samples arrive: CR2032 holder + 2 rails + 3 LEDs on a plywood scrap. Measure open-circuit and loaded voltage, current per LED type, brightness | Table of LED type vs. current and brightness |
| 4 | All | **Integrated prototype**: an adult builds one ship following only the assembly drawing, timed with a stopwatch. Test the order of assembly steps 4-5-6 | Time recorded (target 15–20 min), problems listed |
| 4 | Electronics | **Dark-room test**: all three LEDs visible from 3 m? How bright is the nose cone? | Photos and verdict |
| 5 | Production | **GS-24** copper cut test (10 cuts of the two rails) and **BN-20** sticker test on bare plywood: adhesion, clean peel, no ink bleed | 10/10 clean cuts, sticker verdict |
| 5 | Lead | Review all issues, decide: first pilot date, which parameters to freeze, what to re-test | Written decision in the issue tracker |

## Rules

- Do not change a design file by hand. Change the parameter in `projects/welcome-space/generators/`, run `build.py`, open a pull request.
- If a gate fails, that is a useful result. Record it, do not hide it.
- The holder samples may arrive late: do the tasks that do not depend on them first (comb test, copper tape check, 3D test prints).
- Keep one tray for all small parts and count coin cells in and out.

## Gate criteria

| Test | Pass |
|---|---|
| Comb test | Slides in by hand, no force, no wobble |
| 3D prints | Nose cone and diffuser both fit |
| Electronics | 10 circuits out of 10 light all three LEDs |
| Integrated prototype | Adult builds it in 15–20 minutes |
| Dark room | Three LEDs seen from 3 m |
