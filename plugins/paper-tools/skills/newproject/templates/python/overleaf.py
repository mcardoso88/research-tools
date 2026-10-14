"""Send figures/tables to the Overleaf project in Dropbox.

Copies into the local Dropbox folder when it exists (Miguel's machine); otherwise uploads through the
Dropbox API with DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_REFRESH_TOKEN (e.g. in Codespaces).
Outputs only: data files are never sent to Overleaf.
"""
import os
import shutil
from pathlib import Path

from config import OVERLEAF, OVERLEAF_DIRS, OVERLEAF_LOCAL

ALLOWED = {'.pdf', '.png', '.tex'}


def to_overleaf(*paths, kind):
    """Send paths to the Overleaf subfolder for kind ('tables' or 'figures')."""
    paths = [Path(p) for p in paths]
    for p in paths:
        if p.suffix not in ALLOWED:
            raise ValueError(f"refusing to send {p.name}: only {sorted(ALLOWED)} outputs go to Overleaf")
    sub = OVERLEAF_DIRS[kind]

    if OVERLEAF_LOCAL.is_dir():
        dest = OVERLEAF_LOCAL / sub
        dest.mkdir(parents=True, exist_ok=True)
        for p in paths:
            shutil.copy2(p, dest / p.name)
            print(f"copied to Overleaf: {(Path(sub) / p.name).as_posix()}")
        return

    keys = [os.getenv(k) for k in ('DROPBOX_APP_KEY', 'DROPBOX_APP_SECRET', 'DROPBOX_REFRESH_TOKEN')]
    if not all(keys):
        print("No local Dropbox folder and no Dropbox credentials; skipping Overleaf upload")
        return
    import dropbox
    dbx = dropbox.Dropbox(app_key=keys[0], app_secret=keys[1], oauth2_refresh_token=keys[2])
    for p in paths:
        target = "/".join(s for s in (OVERLEAF, sub, p.name) if s)
        with open(p, 'rb') as f:
            dbx.files_upload(f.read(), target, mode=dropbox.files.WriteMode.overwrite)
        print(f"uploaded to Overleaf: {target}")
