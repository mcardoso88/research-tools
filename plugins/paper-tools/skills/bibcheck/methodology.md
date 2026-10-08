# Bibcheck Methodology

## Why many narrow agents instead of one comprehensive agent

Long single-agent runs over many citations show a pattern: the first 10–15 entries get careful treatment, and the next 60 get pattern-matched. The agent is not lying — it is allocating attention the way any limited reasoner does. Whether you call it gradient decay, attention dilution, or just fatigue, the practical effect is the same: late-batch citations are checked less rigorously than early-batch citations, and the user has no way to see which is which.

The fix is structural. Give each agent one small, well-bounded task and let many agents run in parallel. Each agent now has full attention budget on its single task. The orchestration layer aggregates.

This is the same idea behind `/referee2` (one fresh agent reads the whole artifact cold, instead of asking the producing agent to grade itself) and behind `/split-pdf` (parallel agents on small chunks, instead of one agent on a giant PDF).

## What one agent per citation catches

Per-citation auditing is designed for *catching mixed-up entries*. The most common silent error in an inherited `.bib` file is a field paired with the wrong paper — the title of paper A with the authors and journal of paper B, where someone copy-pasted carelessly years ago. A per-citation agent looks for this directly: identify the paper from the canonical source, then ask "do all my fields belong to the same paper?"

Systematic transcription errors — a journal name consistently rendered with the wrong abbreviation, a year systematically off by one because a working-paper year leaked into the published-paper entry — are harder to see one entry at a time. The final reviewer pass looks across all corrected entries for these patterns.

## What the audit standard is

For each entry, the audit checks:

1. **Existence**: does this paper actually exist? Find a DOI, a published landing page, or an authoritative working-paper URL.
2. **Field consistency**: do title, authors, year, journal/venue, volume, issue, pages, and publisher all belong to the same paper? Mixed-up fields are the most common silent error.
3. **Field correctness**: is each field's content right? (Wrong year by one, abbreviated vs. spelled-out journal, missing volume number, wrong page range.)
4. **Format integrity**: is the BibTeX entry parseable? (This is a side check — usually pdflatex catches it, but unicode in author names sometimes silently fails.)

The audit does *not* check:

- Whether the citation is appropriate to the claim it supports — that is a `/referee2` literature audit, a separate job.
- Whether the cited paper's findings are correctly characterized in the manuscript — same: `/referee2` lit audit.
- Whether there are citations the manuscript should have but does not.

`/bibcheck` is bounded to: are the entries in this `.bib` file accurate descriptions of papers that exist?

## Why this is a verification skill, not a production skill

`/bibcheck` never writes a citation from scratch. It audits and corrects. The user supplies a `.bib`; the skill produces a `bibcheck_report.md` and a `corrected.bib`. The user decides what to merge in. This is by design: production agents that invent citations are exactly the failure mode the skill is meant to catch downstream of someone else's work.
