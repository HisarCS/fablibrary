"""MkDocs hook: builds the "Source files" page and one downloadable archive of every editable file.
Runs before each build. Everything it writes is git-ignored, so the page can never go stale:
  docs/projects/<project>/sources.md
  docs/projects/<project>/files/src/...                  (a copy of each file, for single downloads)
  docs/projects/<project>/files/<project>-sources.zip    (all editable files, small: generated bulk is left out)
"""
import os, shutil, zipfile, datetime

SKIP_DIRS = {'__pycache__', 'preview', 'test-prints', 't1', 'out', '.venv', 'site'}
ROOT_FILES = ['README.md', 'CLAUDE.md', 'CHANGELOG.md', 'CONTRIBUTING.md', 'mkdocs.yml', 'requirements.txt', 'LICENSE', 'LICENSE-DESIGNS.md', '.gitignore']

OPEN_WITH = {'.scad': 'OpenSCAD', '.svg': 'Inkscape, Illustrator or your laser/Roland software', '.stl': 'Bambu Studio or any slicer',
             '.py': 'any text editor + Python 3', '.md': 'any text editor', '.csv': 'Excel, Numbers or Sheets', '.html': 'any text editor, then a browser',
             '.sh': 'any text editor + a terminal', '.yml': 'any text editor', '.txt': 'any text editor'}
ABOUT = {
    'v1_nose_cone.scad': 'Model A nose cone (parametric)', 'v1_diffuser.scad': 'Base diffuser, shared by both models (parametric)', 'v1b_nose_cone.scad': 'Model B nose cone (parametric)',
    'v1_base_plate_laser.svg': 'Model A base plate (cut + engrave)', 'v1_panel_laser.svg': 'Model A body panels', 'v1_wing_laser.svg': 'Model A wings', 'v1_comb_test_laser.svg': 'Press-fit comb test',
    'v1_copper_rails_gs24_cut.svg': 'Model A copper rails and patches, Roland GS-24', 'v1b_base_plate_laser.svg': 'Model B base plate', 'v1b_panels_set_laser.svg': 'Model B panels: 1 power panel + 2 plain',
    'v1b_wing_laser.svg': 'Model B wings', 'v1b_copper_rails_gs24_cut.svg': 'Model B copper rails and patches, Roland GS-24',
    'v1_sticker_sheet_print_cut.svg': 'Sticker sheet for the Roland BN-20 (print + cut)', 'v1_troubleshooting_card.svg': 'Bug Hunter troubleshooting card (A6)', 'v1_student_card.svg': 'Picture-first student step card (A4)',
    'build.py': 'Rebuilds every generated file', 'base_diffuser_comb.py': 'Generates the Model A plate, comb test and base + diffuser drawing', 'panel_nosecone.py': 'Generates the Model A panel and nose cone files',
    'wing.py': 'Generates the Model A wing files', 'assembly.py': 'Generates the assembly drawing', 'hero.py': 'Generates the day / night and personalization illustrations',
    'printables.py': 'Generates the GS-24 band, sticker sheet and troubleshooting card', 'student_card.py': 'Generates the student step card', 'model3d.py': 'Builds the Model A 3D preview and viewer data',
    'model_b.py': 'Builds every Model B file (laser, drawing, nose cone, 3D)', 'meshlib.py': 'Shared mesh helpers for the 3D generators',
    'bench-test-template.csv': 'Electronics bench test log', 'pilot-log-template.csv': 'Pilot lesson log', 'ab-test-template.csv': 'Model A / B build and test log', 'ab-decision-template.csv': 'Model A / B weighted decision table',
    'kit-list.md': 'Parts per kit and the parameter map', 'index.html': 'Single-file web page', 'check_stl.py': 'Checks an STL: size, watertight, overhang', 'export_stl.sh': 'Exports the print STLs from the SCAD files',
    'export_test_prints.sh': 'Exports the tolerance test prints', 'check_site.sh': 'Checks the published site', 'create_first_week_issues.sh': 'Opens the first-week GitHub issues', 'create_ab_issues.sh': 'Opens the Model A / B issues',
}

def _walk(base, rel_base):
    for dp, dns, fns in os.walk(base):
        dns[:] = sorted(d for d in dns if d not in SKIP_DIRS)
        for fn in sorted(fns):
            if fn.endswith('.pyc') or fn == '.DS_Store': continue
            yield os.path.relpath(os.path.join(dp, fn), rel_base).replace(os.sep, '/')

def _category(rel, proj):
    p = f'projects/{proj}/'
    if rel.startswith(p + '3d/stl/'): return '3. Print-ready STL (generated from the SCAD files)'
    if rel.startswith(p + '3d/'): return '2. 3D printed parts (OpenSCAD, parametric)'
    if rel.startswith(p + 'laser/'): return '1. Laser and Roland files (SVG)'
    if rel.startswith(p + 'drawings/'): return '4. Technical drawings and illustrations (SVG)'
    if rel.startswith(p + 'stickers/') or rel.startswith(p + 'teaching/'): return '5. Stickers and printable cards'
    if rel.startswith(p + 'tests/'): return '6. Test templates'
    if rel.startswith(p + 'generators/'): return '7. Generators (Python): change a parameter, rebuild'
    if rel.startswith('docs/projects/') and ('/game/' in rel or '/viewer/' in rel): return '8. Game and 3D explorer (HTML)'
    if rel.startswith('docs/'): return '9. Site pages (Markdown)'
    if rel.startswith(p): return '10. Project notes'
    if rel.startswith('scripts/'): return '11. Repo scripts'
    return '12. Site and repo setup'

def _hidden(rel): return any(part.startswith('.') for part in rel.split('/'))

def _human(n): return f'{n/1024:.0f} KB' if n < 1024*1024 else f'{n/1024/1024:.1f} MB'

def on_pre_build(config, **kwargs):
    root = os.path.dirname(config['config_file_path'])
    pdir = os.path.join(root, 'projects')
    if not os.path.isdir(pdir): return
    for proj in sorted(os.listdir(pdir)):
        if not os.path.isdir(os.path.join(pdir, proj)): continue
        files = list(_walk(os.path.join(pdir, proj), root))
        docp = os.path.join(root, 'docs', 'projects', proj)
        for sub in ('', 'game', 'viewer'):
            d = os.path.join(docp, sub)
            if not os.path.isdir(d): continue
            for fn in sorted(os.listdir(d)):
                full = os.path.join(d, fn)
                if not os.path.isfile(full): continue
                ok = (sub == '' and fn.endswith('.md') and fn not in ('sources.md', 'kit-list.md')) or (sub in ('game', 'viewer') and fn == 'index.html')
                if ok: files.append('docs/projects/%s/%s%s' % (proj, sub + '/' if sub else '', fn))
        for sd in ('scripts', 'hooks', os.path.join('.github', 'ISSUE_TEMPLATE')):
            if os.path.isdir(os.path.join(root, sd)):
                files += [(sd + '/' + f).replace(os.sep, '/') for f in sorted(os.listdir(os.path.join(root, sd))) if os.path.isfile(os.path.join(root, sd, f)) and not f.endswith('.pyc')]
        files += [f for f in ROOT_FILES if os.path.isfile(os.path.join(root, f))]
        files = list(dict.fromkeys(files))

        out = os.path.join(docp, 'files'); src = os.path.join(out, 'src')
        shutil.rmtree(src, ignore_errors=True); os.makedirs(src, exist_ok=True)
        for f in files:
            if f.endswith('.md') or _hidden(f): continue   # MkDocs would treat copied .md files as pages, and drops dotfiles; both link to GitHub instead
            dst = os.path.join(src, f); os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy(os.path.join(root, f), dst)
        zpath = os.path.join(out, f'{proj}-sources.zip')
        with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
            z.writestr('README_SOURCES.txt',
                       f'FabLibrary - {proj} - editable source files\nBuilt {datetime.date.today()}.\n\n'
                       'Folder layout is the same as the GitHub repository, so you can unzip it over a clone.\n'
                       'Left out on purpose (rebuild with the generators): the 3D explorer data (model.js, model_b.js) and the preview STL meshes.\n')
            for f in files: z.write(os.path.join(root, f), f)
        zsize = os.path.getsize(zpath)

        groups = {}
        for f in files:
            groups.setdefault(_category(f, proj), []).append(f)
        L = ['# Source files', '',
             'Every editable file of this project in one place. Edit it, test it, and send the changes back.', '',
             f'[Download all {len(files)} files as one ZIP ({_human(zsize)})](files/{proj}-sources.zip){{ .md-button .md-button--primary download }}', '',
             'The ZIP keeps the repository folder layout, so it unzips straight over a clone. It leaves out the generated bulk (3D explorer data and preview STL meshes), which the generators rebuild.', '',
             '## How to edit', '',
             '1. **Change a number, not a drawing.** The SVG files and the 3D explorer are generated. Change the parameter in `generators/` (or at the top of the `.scad` file), then run `python projects/%s/generators/build.py`.' % proj,
             '2. **Print STLs come from the SCAD files.** After every `.scad` change run `bash scripts/export_stl.sh`.',
             '3. **Record what you measured** in a *Test result* issue and in the [assumptions log](assumptions.md).', '',
             '## Send it back for the final optimization', '',
             'Attach to your message: the ZIP, your filled test CSVs (`tests/*.csv`), the issue numbers of the test results and the decision (Model A or B). Say which parameters you changed.', '']
        for cat in sorted(groups, key=lambda c: int(c.split('.')[0])):
            L += [f'## {cat.split(". ", 1)[1]}', '', '| File | What it is | Open with | Size |', '|---|---|---|---|']
            for f in groups[cat]:
                name = os.path.basename(f); ext = os.path.splitext(f)[1]
                size = _human(os.path.getsize(os.path.join(root, f)))
                link = (config.get('repo_url', '').replace('github.com', 'raw.githubusercontent.com').rstrip('/') + '/main/' + f) if ext == '.md' or _hidden(f) else f'files/src/{f}'
                L.append(f'| [`{f}`]({link}){{ download }} | {ABOUT.get(name, "")} | {OPEN_WITH.get(ext, "a text editor")} | {size} |')
            L.append('')
        L += ['!!! note "Generated files are not listed here"', '    `viewer/model.js`, `viewer/model_b.js` and `3d/preview/*.stl` are rebuilt by `generators/model3d.py` and `generators/model_b.py`.']
        with open(os.path.join(docp, 'sources.md'), 'w') as fh: fh.write('\n'.join(L) + '\n')
