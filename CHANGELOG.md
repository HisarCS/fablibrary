# Changelog

## Welcome Space

### Model B (draft)
- Added Model B ("LEDs outside"): closed three-panel body, LEDs and straight copper rails on one power panel, 66 mm nose cone. Model A is unchanged. Files: `laser/v1b_*.svg`, `drawings/v1b_drawing.svg`, `3d/v1b_nose_cone.scad`, preview meshes and a Model A / Model B switch in the 3D explorer.
- Added the "Model A or Model B?" page with the comparison tests, a weighted decision table and an A/B decision issue form. Tests are tracked in the `[A/B]` issues.

### Diffuser: supportless ledge (draft)
- `v1_diffuser.scad`: the ledge underside is now a 45-degree chamfer instead of a flat shelf, so the diffuser prints without supports. New parameter `chamferDz` = 10 mm. The switch window cut now spans the wall from `ledgeR-6` to `Rbot+6`. `pocketD` is unchanged (110.4, still to be confirmed). Related test: [#4](https://github.com/HisarCS/fablibrary/issues/4).
- `v1_base_diffuser_drawing.svg` and the preview meshes regenerated from the same numbers.

### Site update
- Hero and personalization illustrations now show the stickers applied; the sticker sheet is shown on the project page.
- Added GS-24 copper band, BN-20 sticker sheet, troubleshooting card, bench test log template and an assumptions log (all parts assumed delivered for planning).
- Added a first-week task plan and a script that creates its GitHub issues.
- Added finished-ship illustrations (day, dark room, personalization), safety page, kit list page, real file downloads and a mission roadmap.

### v1-proto1 (draft)
- First design set: base plate (Ø110, 3 panel slots + 3 wing slots), panel ×3, wing ×3, nose cone, diffuser, comb test.
- Electronics: CR2032 holder with cover and switch, 2 copper rails, 3 LEDs, all under the base plate.
- All tolerances are estimates: `SLOT_W=3.1`, `slotW=3.3`, `pocketD=110.4`. To be updated after testing.
