"""Shared paths. All scripts import from here; nothing is hard-coded elsewhere."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "clean"
TABLES = ROOT / "output" / "tables"
FIGURES = ROOT / "output" / "figures"

for p in (CLEAN, TABLES, FIGURES):
    p.mkdir(parents=True, exist_ok=True)

# Overleaf project, synced via Dropbox. OVERLEAF is the path inside Dropbox (used by the API);
# OVERLEAF_LOCAL is the same folder on a machine running the Dropbox client.
OVERLEAF = "/Apps/Overleaf/[OVERLEAF PROJECT]"
OVERLEAF_LOCAL = Path.home() / "Dropbox" / OVERLEAF.lstrip("/")
# Subfolders of the Overleaf project that the paper's \input / \includegraphics point to ("" = project root)
OVERLEAF_DIRS = {"tables": "[TABLES SUBFOLDER]", "figures": "[FIGURES SUBFOLDER]"}
