# FabLibrary – Hisar FabLab

An open design library for the K12 Fab STEAM projects of Hisar IdeaLab FabLab.
Every project is documented here with its laser-cut, 3D-printed, electronics and teaching materials.

**Website:** https://hisarcs.github.io/fablibrary/

## Projects

| Project | Level | Status |
|---|---|---|
| [Welcome Space](projects/welcome-space/) – LED-lit spaceship (Mission 01) | Grade 4, 60 min | v1 prototype |

## Quick start

```bash
pip install -r requirements.txt
python projects/welcome-space/generators/build.py   # regenerate design files
mkdocs serve                                        # preview the site at http://127.0.0.1:8000
```

## License

- Design files and documentation: CC BY-SA 4.0 ([LICENSE-DESIGNS.md](LICENSE-DESIGNS.md))
- Code (generators, scripts): MIT ([LICENSE](LICENSE))

How to contribute: [CONTRIBUTING.md](CONTRIBUTING.md)
