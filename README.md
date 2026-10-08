# research-tools

A Claude Code plugin marketplace (`miguel-tools`) containing one plugin, `paper-tools`: shared skills for empirical research papers in labour economics and international trade. Empirical work runs in Stata locally; Python is used in Codespaces.

## Skills in `paper-tools`

| Skill | What it does |
|---|---|
| `/newproject` | Scaffolds a research project (`code/stata`, `code/python`, `data/`, `output/`, `decks/`, …) with a CLAUDE.md template. |
| `/beautiful_deck` | End-to-end Beamer deck: audience triage, house-style or original theme, narrative outline, reuses Stata figures from `output/figures`, new figures in Python, zero-warning compile, rhetoric and graphics audits. |
| `/compiledeck` | Beamer preamble (Warm Professional house style), slide rules, compile loop, palettes, TikZ rules. |
| `/compiletex` | Compiles a `.tex` file and reports errors and warnings. |
| `/referee2` | Fresh-session audit. Deck mode reviews slides; code mode audits the Stata pipeline, replicates it in Python, and compares against the paper's LaTeX tables (copied into e.g. `stata_output/`). Markdown report only. |
| `/blindspot` | Audits your perception of a figure or table before you interpret it: overlooked problems and overlooked opportunities. |
| `/bibcheck` | One agent per `.bib` entry verifies each citation against canonical sources; writes a report and `corrected.bib`. |
| `/split-pdf` | Reads academic PDFs in 4-page chunks and writes structured reading notes. |
| `/tikz` | Quick collision check for TikZ code or rendered figures (labels on curves, cramped labels, clipping). |

## Credits

Many skills in `plugins/paper-tools/` are adapted from Scott Cunningham's
[MixtapeTools](https://github.com/scunning1975/MixtapeTools).

## Routine

### Edit a skill

```bash
git pull
# edit files under plugins/paper-tools/
git add -A
git commit -m "Describe the change"
git push
```

### Update a paper's codespace to the latest version

```bash
claude plugin marketplace update miguel-tools
claude plugin update paper-tools@miguel-tools
# if it says the plugin is not installed:
claude plugin install paper-tools@miguel-tools
```

Then restart Claude Code so the updated skills load.
