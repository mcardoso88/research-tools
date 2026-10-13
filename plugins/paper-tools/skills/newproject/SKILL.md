---
name: newproject
description: Scaffold a new research project from a project summary document, with standard directory structure, a pre-filled CLAUDE.md, and a documented README. Use this at the start of every new project to ensure consistent organization.
allowed-tools: Bash(mkdir*), Bash(cp*), Bash(mv*), Bash(touch*), Bash(ls*), Bash(find*), Bash(git*), Bash(pandoc*), Bash(python*), Write, Read, Edit
argument-hint: [project-name]
---

# New Project Scaffold

Create Miguel's standard research project structure, starting from a project summary document. This skill is invoked at the start of every project, usually inside an existing git repo.

## What Gets Created

```
[project-root]/
├── CLAUDE.md              # Permanent research rules, pre-filled from the summary
├── README.md              # Project-specific overview (existing one is kept)
├── .gitignore             # Existing one is kept; data/ and stata_output/ appended
├── code/
│   ├── stata/
│   └── python/
├── data/
│   ├── raw/               # Original source data (never modify)
│   └── clean/             # Cleaned/merged datasets
├── output/
│   ├── tables/
│   └── figures/
├── documents/             # Outside PDFs, papers (use /split-pdf on these)
├── decks/                 # Beamer presentations (rhetoric of decks)
├── notes/                 # Project summary, scratch notes, random ideas
└── progress_logs/         # Session continuity across Claude conversations
```

Every empty folder gets a `.gitkeep` so git keeps the structure.

## Execution

0. **Find and read the project summary (before scaffolding anything).**
   - Search the repo for a summary: `notes/summary.*` first, then any file with "summary" in its name (case-insensitive) with extension `.md`, `.txt`, `.pdf` or `.docx`. Skip `.git/`.
     ```bash
     find . -path ./.git -prune -o -type f -iname '*summary*' \( -iname '*.md' -o -iname '*.txt' -o -iname '*.pdf' -o -iname '*.docx' \) -print
     ```
   - If several match, pick the best candidate (prefer `notes/summary.*`) and say which one you are using; ask only if it is genuinely ambiguous.
   - If none is found, **stop and ask Miguel to add one to the repo or paste it in**. Proceed without a summary only if he explicitly says so; in that case skip the pre-fill in step 7 and ask for the details instead.
   - Read it: `.md`/`.txt` with Read; `.pdf` with Read (use `pages` for long files); `.docx` converted to text first, with `pandoc file.docx -t plain` or, if pandoc is missing, python-docx (`python -I -c` reading paragraphs and tables). Convert into the scratchpad, not the repo.

1. **Get the project name** from the argument. If none, use the repo folder name or the summary's title and confirm.
   - Convert spaces to hyphens, lowercase

2. **Determine location.**
   - Check `git rev-parse --show-toplevel`. If the working directory is inside a git repo, **scaffold in the repo root**, not a subfolder named after the project.
   - Only if not in a repo, default to `[project-name]/` under the current directory (confirm if unclear).
   - Below, `ROOT` means the chosen location.

3. **Create all directories and `.gitkeep` files:**
   ```bash
   mkdir -p ROOT/{code/{stata,python},data/{raw,clean},output/{figures,tables},documents,decks,notes,progress_logs}
   ```
   Then add `.gitkeep` to each folder that is empty (leaf folders; do not add to a folder that already has files or subfolders). Never overwrite or delete existing files.
   ```bash
   find ROOT/{code,data,output,documents,decks,notes,progress_logs} -type d -empty -exec touch {}/.gitkeep \;
   ```
   Run this after step 5 so `notes/` is judged correctly.

4. **Update `.gitignore`.**
   - If `ROOT/.gitignore` exists, keep it and append only the missing lines (check first, no duplicates). If not, create it.
   - Lines to ensure: `data/` and `stata_output/`.
   - Because `data/` is ignored, the `.gitkeep` files under `data/` will not be tracked; that is fine and expected. Mention it in the report.

5. **Put the summary in `notes/`.**
   - If the summary is already in `ROOT/notes/`, leave it.
   - Otherwise **ask Miguel before moving it** (`git mv` if tracked, else `mv`). If he declines, leave it where it is and say so. If he pasted the summary rather than adding a file, offer to save it as `notes/summary.md`.

6. **Copy CLAUDE.md** from `CLAUDE_template.md` (relative to this skill's folder) to `ROOT/CLAUDE.md`. If `ROOT/CLAUDE.md` already exists, do not overwrite; ask what to do.
   - Replace `[Your Name]` with `Miguel`
   - Update project name in the overview section

7. **Pre-fill CLAUDE.md from the summary, then ask once.**
   - Fill every placeholder the summary supports: collaborators, overview, research question, data, identification strategy, key variables, sample, current phase/status, and so on. Use the summary's own facts; do not invent.
   - List what the summary does **not** cover and ask Miguel about all of it **in one batch** (a single message or one AskUserQuestion call), not one question at a time.
   - Apply his answers. Anything still unknown stays as a short placeholder (e.g. `[TBD]`, `[TBD: sample restrictions]`), not the template's long prompt text.

8. **Generate README.md.**
   - If `ROOT/README.md` exists, **keep it as is**. Only append a short "Project structure" section with the tree below if it has no directory tree; do not rewrite its content.
   - Otherwise create it with:
     - Project title
     - Visual directory tree in a fenced code block (monospace)
     - Explanation of each folder's purpose
     - Note that CLAUDE.md is copied from a permanent template and edited per-project
     - Note that README.md is for project-specific documentation
     - Note that progress_logs/ maintains continuity across Claude sessions
     - Placeholder sections: Overview, Collaborators, Status, Key Files

   The tree block:

   ````markdown
   ```
   [project-name]/
   ├── CLAUDE.md              # Research rules & estimation philosophy (permanent)
   ├── README.md              # This file — project-specific notes
   ├── code/
   │   ├── stata/             # Stata do-files (run locally)
   │   └── python/            # Python scripts
   ├── data/
   │   ├── raw/               # Original source data (never modify these)
   │   └── clean/             # Cleaned and merged datasets
   ├── output/
   │   ├── tables/            # Generated tables (LaTeX, CSV)
   │   └── figures/           # Generated figures (PDF, PNG)
   ├── documents/             # Outside papers and PDFs (split with /split-pdf)
   ├── decks/                 # Beamer presentations (rhetoric of decks philosophy)
   ├── notes/                 # Project summary, scratch notes, ideas, miscellaneous
   └── progress_logs/         # Session logs for continuity across Claude conversations
   ```
   ````

9. **Create initial progress log** at `progress_logs/YYYY-MM-DD_setup.md`:
   - Record the creation date and the summary file used
   - List next steps as a checklist

10. **Report, do not commit.**
    - Show the structure with `ls`.
    - Run `git status --short` and `git diff` (plus the contents of new untracked files such as CLAUDE.md) so Miguel can review.
    - **Do not stage or commit anything.** Leave that to Miguel.
    - Remind him which CLAUDE.md placeholders remain.
