"""MkDocs hook, runs before each build.
Copies from projects/<project>/ into docs/projects/<project>/ (all copies are git-ignored):
  drawings/*.svg            -> img/
  laser/*.svg, 3d/*.scad, stickers/*.svg, teaching/*.svg, tests/*.csv -> files/ (direct downloads)
  kit-list.md               -> kit-list.md
"""
import os, shutil

def _copy(src_dir, dst_dir, exts):
    if not os.path.isdir(src_dir):
        return
    os.makedirs(dst_dir, exist_ok=True)
    for f in os.listdir(src_dir):
        if f.endswith(exts):
            shutil.copy(os.path.join(src_dir, f), os.path.join(dst_dir, f))

def on_pre_build(config, **kwargs):
    root = os.path.dirname(config["config_file_path"])
    pdir = os.path.join(root, "projects")
    if not os.path.isdir(pdir):
        return
    for proj in os.listdir(pdir):
        src = os.path.join(pdir, proj)
        dst = os.path.join(root, "docs", "projects", proj)
        _copy(os.path.join(src, "drawings"), os.path.join(dst, "img"), (".svg",))
        _copy(os.path.join(src, "laser"), os.path.join(dst, "files"), (".svg",))
        _copy(os.path.join(src, "3d"), os.path.join(dst, "files"), (".scad",))
        _copy(os.path.join(src, "stickers"), os.path.join(dst, "files"), (".svg",))
        _copy(os.path.join(src, "teaching"), os.path.join(dst, "files"), (".svg",))
        _copy(os.path.join(src, "tests"), os.path.join(dst, "files"), (".csv",))
        kit = os.path.join(src, "kit-list.md")
        if os.path.isfile(kit):
            os.makedirs(dst, exist_ok=True)
            shutil.copy(kit, os.path.join(dst, "kit-list.md"))
