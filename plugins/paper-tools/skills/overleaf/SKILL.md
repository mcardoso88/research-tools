---
name: overleaf
description: Re-run the Python scripts whose code changed since their last run (plus everything downstream), so the refreshed tables and figures reach the paper's Overleaf project through the project's to_overleaf(). Also pushes existing outputs without re-running. Python only; Stata do-files are flagged for Miguel to run locally. Use when Miguel says /overleaf, "update the paper's tables/figures", or "send this to Overleaf".
allowed-tools: Bash, Read, Edit, Write
argument-hint: '[NN | --all | --push FILE... | --dry-run]'
---

# /overleaf: refresh the paper's tables and figures

The paper lives in Overleaf, synced through Dropbox (`Dropbox/Apps/Overleaf/<project>`). Projects scaffolded by `/newproject` set the path in `code/python/config.py` (`OVERLEAF`, `OVERLEAF_DIRS`) and send outputs with `to_overleaf()` from `code/python/overleaf.py`. Pipeline scripts are numbered (`01_build_panel.py`, `02_...`) and run in that order; each later script may read what earlier ones wrote.

This skill acts only when invoked. It never runs on save.

## Hard rules

- **Only outputs go to Overleaf:** `.tex`, `.pdf` and `.png` files under `output/`. Never anything from `data/`, never `.csv`, `.parquet`, `.dta`, `.pkl`, never logs. The project's CLAUDE.md data rules override this skill. If a script would upload something else, stop and tell Miguel.
- **Always upload through the project's `to_overleaf()`**, which handles the local-copy vs Dropbox API choice and the file-type check. Never call the Dropbox API directly or write your own uploader.
- **Never put credentials in code or print them.** Uploads from Codespaces need `DROPBOX_APP_KEY`, `DROPBOX_APP_SECRET`, `DROPBOX_REFRESH_TOKEN` as env vars (Codespaces secrets).
- **Stata does not run here.** Do-files write to Overleaf themselves via `code/stata/paths.do` (`$ov_tables`, `$ov_figures`) when Miguel runs them locally.
- **Don't comment on the results.** Report what ran and what was sent, not whether estimates look good (see the project's estimation philosophy).
- Do not stage, commit or push anything.

## Step 1: Check the setup

1. Read `code/python/config.py` and `code/python/overleaf.py`.
   - If either is missing, stop: suggest running `/newproject` (it adds them without overwriting existing files).
   - If `OVERLEAF` or `OVERLEAF_DIRS` still contain `[...]` placeholders, stop and ask Miguel for the Overleaf folder name and the subfolders the paper reads from.
2. Check `to_overleaf`'s signature (`inspect.signature`). The template uses `kind="tables"|"figures"`; older projects may use another keyword (e.g. `folder=`). Use whatever the project has.
3. Say which route uploads will take: local copy if the Dropbox folder exists on this machine, API if the three `DROPBOX_*` env vars are set (check with `[ -n "$VAR" ]`, never echo values), otherwise **neither** — in that case tell Miguel uploads will be skipped and ask whether to continue (outputs still refresh locally).

## Step 2: Work out what to run

Run stamps live in `output/.runstamps/<script>.stamp` (one per script, touched after each successful run). Make sure `output/.runstamps/` is in `.gitignore`; append it if not.

Pick the start script:

| Argument | Start |
|---|---|
| none | The earliest numbered script that is newer than its stamp or has no stamp. If `config.py`, or any non-numbered helper module the scripts import (other than `overleaf.py`), is newer than the oldest stamp, start at the first script. |
| `NN` (e.g. `04`) | That script. |
| `--all` | The first script. |
| `--push FILE...` | Run nothing; go to Step 4 with those files. |
| `--dry-run` | Do Steps 1–2, print the plan, stop. |

Then run **from the start script through the last one**, in order: downstream scripts may use what it writes. Nothing changed → say so and stop.

**Confirm first** (one short message) when there are no stamps yet, or when the plan includes the panel build (`01_*`), since a full run can be slow. Otherwise just state the plan and go.

Also list any do-file in `code/stata/` newer than the newest stamp: "these changed and must be run locally in Stata".

## Step 3: Run

From the repo root, for each script in order:

```bash
start=$(date +%s); python code/python/NN_name.py 2>&1 | tail -40; echo "exit=${PIPESTATUS[0]} secs=$(( $(date +%s) - start ))"
```

- Use a long Bash timeout; run in the background if a script is likely to take more than a few minutes, and wait for it to finish before starting the next.
- Show only the tail of the output. Don't print data.
- On success, `mkdir -p output/.runstamps && touch output/.runstamps/NN_name.stamp`.
- On failure, **stop**: don't run later scripts and don't touch their stamps. Show the error. Note that a script calls `to_overleaf` as it goes, so anything it sent before crashing is already in Overleaf; say which files those were.
- Collect the "copied to Overleaf" / "uploaded to Overleaf" lines from each script's output.

## Step 4: Outputs the scripts didn't send

Find `.tex`, `.pdf`, `.png` files in `output/tables` and `output/figures` written during this run that no script sent (often `.png` previews). **List them; don't send them.** The paper may not use them, and stray files clutter the Overleaf project. Send one only if Miguel says so.

For `--push FILE...`: check each file is under `output/` with an allowed extension, map `output/tables` → tables and `output/figures` → figures, and send it through `to_overleaf`:

```bash
cd code/python && python -c "from overleaf import to_overleaf; to_overleaf('../../output/tables/tab1.tex', kind='tables')"
```

(Use the keyword found in Step 1.)

## Step 5: Report

Keep it short:
- Scripts run, each with exit status and duration; any script skipped and why.
- Files sent, with their Overleaf destination and route (local copy or API). If uploads were skipped, say so plainly.
- Outputs written but not sent (Step 4).
- Stata do-files that changed and need a local run.
- If a table or figure the paper uses changed, remind Miguel that the numbers quoted in the text may need re-checking.
