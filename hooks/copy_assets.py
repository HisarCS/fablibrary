"""MkDocs hook: copies projects/*/drawings/*.svg -> docs/projects/<project>/img/ before each build."""
import os, shutil

def on_pre_build(config, **kwargs):
    root = os.path.dirname(config["config_file_path"])
    pdir = os.path.join(root, "projects")
    if not os.path.isdir(pdir):
        return
    for proj in os.listdir(pdir):
        src = os.path.join(pdir, proj, "drawings")
        if not os.path.isdir(src):
            continue
        dst = os.path.join(root, "docs", "projects", proj, "img")
        os.makedirs(dst, exist_ok=True)
        for f in os.listdir(src):
            if f.endswith(".svg"):
                shutil.copy(os.path.join(src, f), os.path.join(dst, f))
