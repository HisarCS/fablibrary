# Notes for Claude Code

## Language
All repository content (docs, READMEs, code comments, drawing labels, commit messages) is in **English**.

## Structure
- `projects/<project>/` : source files for each project (laser, 3d, drawings, electronics, teaching, tests, generators)
- `docs/` : MkDocs Material site. Project pages live in `docs/projects/<project>/`.
- `hooks/copy_assets.py` : before each build, copies drawings to `docs/projects/<project>/img/`, laser SVGs and SCAD files to `files/` (downloads) and `kit-list.md` into the docs. All of these copies are git-ignored; edit the sources under `projects/`.
- `.github/workflows/pages.yml` : publishes the site to GitHub Pages on every push to `main`.

## Rules
- Never edit generated SVGs by hand. Change the parameter in `projects/welcome-space/generators/*.py`, then run:
  `python projects/welcome-space/generators/build.py`
- Laser SVGs: red (#FF0000) hairline = cut, black = engrave. Units are mm.
- OpenSCAD files are parametric; parameters are at the top of each file.
- Key parameters: `SLOT_W` (slot width), `SLOT_L` (panel slot), `WSLOT_L` (wing slot), `slotW` (nose cone), `pocketD` (diffuser pocket).
- For every parameter change, update `CHANGELOG.md` and link the related test issue.
- Never add student names, photos or any personal data to the repository.
- After changes, verify the site with `mkdocs build --strict`.
