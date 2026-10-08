---
name: bibcheck
description: Many-agent bibliography audit. Verify each citation in a .bib file by spawning one narrow-focus agent per entry that confirms the DOI/URL and cross-checks that all fields belong to the same paper. Catches mixed-up entries (one paper's title with another's authors), wrong years, journal misattributions, and unverifiable references. Use when reviewing a manuscript's bibliography for accuracy before submission, after literature review, or when inheriting a .bib from a coauthor.
allowed-tools: Bash(ls*), Bash(cat*), Bash(wc*), Bash(grep*), Bash(mkdir*), Bash(cp*), Read, Write, Edit, WebSearch, WebFetch, Agent
argument-hint: '<path-to-bib-or-tex> [--max-parallel N]'
---

# Bibcheck: Many-Agent Bibliography Audit

You are running `/bibcheck` — a verification routine that audits a bibliography by spawning many narrow-focus agents, one per citation, so each agent operates on a small task with low risk of attention decay over a long context.

## Why narrow agents

A single agent asked to audit 80 citations in one pass tends to drift: early entries get careful treatment; later entries get pattern-matched. Splitting the work — one agent per entry — keeps each agent focused on something small and verifiable. The bottleneck shifts from agent attention to orchestration, which is what cheap parallel agents are for.

See `methodology.md` for the full rationale.

## Step 0: Read your full methodology

Read `methodology.md` in this skill directory — it explains the attention-decay rationale and the audit standard.

## Step 1: Parse arguments

| Argument | What it does |
|----------|--------------|
| `<file>` | The `.bib` or `.tex` file to audit. One Agent subagent per bib entry; each fully audits its one entry. |
| `--max-parallel N` | Optional. Cap concurrent subagents. Default 8. |

Input file:
- `.bib` — use directly
- `.tex` — extract `\bibitem{}` blocks or read the linked `.bib` from `\bibliography{}`. If both a `.tex` and a `.bib` are in the same folder, prefer the `.bib`.

If the user invoked `/bibcheck` with no arguments, ask for the path to the .bib or .tex. Do not guess.

## Step 2: Set up the run directory

Create a working folder next to the input file:

```
<bib_dir>/bibcheck_<timestamp>/
  ├── input.bib              # copy of source
  ├── entries/               # split entries (one .bib per entry)
  ├── reports/               # per-agent JSON/markdown outputs
  ├── bibcheck_report.md     # final consolidated report
  └── corrected.bib          # drop-in replacement
```

The timestamped folder means re-runs do not clobber prior audits.

## Step 3: Audit each citation

1. **Split the .bib into per-entry files.** A robust splitter: read the .bib, walk for `@type{key,` openers, balance braces to find each entry's close, write to `entries/<key>.bib`.

2. **Launch agents in waves of `--max-parallel`.** For each entry, dispatch one Agent subagent (subagent_type: general-purpose) with this brief:

   ```
   You are auditing one bibliography entry. The entry is:

   <paste the .bib block>

   Your job:
   1. Identify the cited paper. Use WebSearch (and WebFetch if needed) to find it.
   2. Locate a canonical anchor: DOI, journal landing page URL, or author working-paper URL.
   3. Cross-check every field in the .bib block against the canonical source:
      - title, authors, year, journal/booktitle, volume, number, pages, publisher, DOI
   4. Specifically test for "field mixing" — e.g., the title belongs to one paper but the authors or year belong to another. This is the most common silent error in inherited .bib files.
   5. Output JSON to <reports/<key>.json> with:
      - status: "clean" | "corrected" | "unverifiable"
      - one_sentence: plain-language description of the paper (one sentence)
      - canonical_url: DOI or URL
      - issues: list of {field, original, corrected, reason}
      - corrected_bib: the corrected entry (or the original if status=clean)

   You do NOT modify the input file. You only write the report and the corrected entry.
   ```

3. **Final reviewer pass.** When all entries are done, dispatch a single reviewer agent that:
   - Reads every `reports/*.json`.
   - Spot-checks any entry marked "unverifiable" (does a quick second WebSearch).
   - Adjudicates conflicts where a corrected field looks suspicious.
   - Looks across the corrected entries for systematic patterns (e.g., a journal name consistently abbreviated differently, working-paper years leaking into published entries) and notes them in the report.
   - Writes `bibcheck_report.md` with a summary table (Clean / Corrected / Unverifiable counts) and per-entry detail.
   - Concatenates the corrected_bib fields into `corrected.bib`.

## Step 4: Present the result to the user

Show the user:

```
bibcheck complete.

  Clean:        N entries
  Corrected:    M entries (see bibcheck_report.md)
  Unverifiable: K entries (need human eyes)

Drop-in replacement: corrected.bib
Full audit:          bibcheck_report.md
```

Do not auto-overwrite the user's source `.bib`. They review, then move `corrected.bib` into place themselves.

## Defaults and tone

- Default `--max-parallel` is **8**. Bump on request.
- This is a verification skill — never *write* citations from scratch. Only audit and correct.
- If a citation is genuinely unverifiable (paywalled, dead URL, ambiguous match), say so. Do not invent a DOI.
