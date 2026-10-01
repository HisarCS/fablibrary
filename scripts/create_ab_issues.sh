#!/usr/bin/env bash
# Creates the Model A / Model B comparison issues. Requires the GitHub CLI (gh) logged in.
# Usage: bash scripts/create_ab_issues.sh
set -euo pipefail
REPO="HisarCS/fablibrary"
for l in "ab-test:FBCA04" "decision:B60205"; do gh label create "${l%%:*}" --color "${l##*:}" --repo "$REPO" 2>/dev/null || true; done
mk() { gh issue create --repo "$REPO" --title "$1" --label "$2" --body "$3"; }
mk "[A/B] Build 5 ships of Model A (timed)" "ab-test" "Follow the Model A assembly. Log each build in tests/ab-test-template.csv: minutes, first-try success, failures."
mk "[A/B] Build 5 ships of Model B (timed)" "ab-test" "Cut the B laser files (plate, panel set, wings), print the B nose cone, cut the GS-24 band. Follow the build order on the Model A or Model B page. Log each build."
mk "[A/B] Electronics gate: 10 builds each, 10 working" "ab-test" "A model that does not light all 3 LEDs in 10 of 10 builds is out, whatever its score."
mk "[A/B] Shake and tug test" "ab-test" "Gentle shake and a gentle tug on the wires. Do the LEDs stay lit? Which joint fails first?"
mk "[A/B] Stand, wobble and dark-room test" "ab-test" "Wobble 1 to 5 before and after the nose cone. 3 LEDs visible from 3 m? Is the nose cone lit (Model A)?"
mk "[A/B] Planted fault test" "ab-test" "One helper plants a fault, another finds it. Minutes for each model."
mk "[A/B] Decision meeting" "decision" "Fill in the weighted table (tests/ab-decision-template.csv) and record the result with the A/B decision form."
echo done
