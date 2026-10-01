#!/usr/bin/env bash
# Creates the first-week task issues for Welcome Space. Requires the GitHub CLI (gh) logged in.
# Usage: bash scripts/create_first_week_issues.sh
set -euo pipefail
REPO="HisarCS/fablibrary"
for l in "lead:0E8A16" "production:1D76DB" "electronics:D93F0B" "week-1:5319E7"; do
  gh label create "${l%%:*}" --color "${l##*:}" --repo "$REPO" 2>/dev/null || true
done
mk() { gh issue create --repo "$REPO" --title "$1" --label "$2" --body "$3"; }

mk "[W1-D1] Order samples and tools" "lead,week-1" "5 × CR2032 holders with cover and switch (both single models), 2 × 2×AAA holders with switch, LED assortment (white, blue, red, green, yellow), resistor set (22/47/100/150/220 ohm), 3 multimeters, conductive copper tape. Note delivery dates here."
mk "[W1-D1] Comb test on Epilog and xTool" "production,week-1" "Cut projects/welcome-space/laser/v1_comb_test_laser.svg from the real plywood on each machine. Find the slot width that slides in by hand without force or wobble. Record the best width per machine (3.00–3.30 mm) with a photo."
mk "[W1-D1] Copper tape conductivity check" "electronics,week-1" "Multimeter from adhesive side to foil side on 5 spots of each roll. Record conductive / not conductive per roll."
mk "[W1-D2] 3D test prints: nose cone and diffuser" "production,week-1" "Nose cone slotW 3.2 / 3.3 / 3.4. Diffuser pocketD 110.25 / 110.40 / 110.55. Translucent PLA and PETG if possible. Record print time, filament and which values fit."
mk "[W1-D2] Set SLOT_W after the comb test (pull request)" "lead,week-1" "Change SLOT_W (base plate), panel tab and wing tab in the generator scripts, run build.py, open a PR, update CHANGELOG.md."
mk "[W1-D3] Cut the first full laser set" "production,week-1" "Base, 3 panels, 3 wings with the new values. Sand edges lightly. Photo of the complete set."
mk "[W1-D3] Electronics bench test" "electronics,week-1" "CR2032 holder + 2 rails + 3 LEDs on a plywood scrap. Measure open-circuit and loaded voltage, current per LED type, brightness. Table: LED type vs current and brightness. Gate: 10 of 10 circuits work."
mk "[W1-D4] Integrated prototype, timed" "production,electronics,week-1" "An adult builds one ship using only the assembly drawing. Stopwatch. Test the order of steps 4-5-6. Target 15–20 min. List every problem."
mk "[W1-D4] Dark-room test" "electronics,week-1" "Are all three LEDs visible from 3 m? How bright is the nose cone? Photos and verdict."
mk "[W1-D5] GS-24 copper cut and BN-20 sticker tests" "production,week-1" "10 cuts of the two rails on the GS-24 (clean peel?). BN-20 stickers on bare plywood: adhesion, clean peel, ink bleed."
mk "[W1-D5] Week review and decisions" "lead,week-1" "Review all issues. Decide: first pilot date, parameters to freeze, tests to repeat."
echo done
