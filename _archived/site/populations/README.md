# Archived population pages — retired taxonomy codes

Five rendered population pages, retired 2026-08-12 by owner instruction. They mirror their origin
path (`site/populations/`), per the retire-here-don't-delete rule.

## Why they could not stay

Each names a population code that **no longer exists in the database**. The 2026-07-23 population
schema replacement (`DR-2026-07-23-population-schema-replace`, DG-NON — population taxonomy is
owner-only) replaced them:

| Archived page | Code it renders | Superseded by |
|---|---|---|
| `vis.html` | `VIS` — vision impairment | `BLIND` |
| `ofs.html` | `OFS` — orthostatic/fatigue spectrum | `COM` (with `CFS`, `MCAS`, `POTS`, `LCOV`) |
| `dbl.html` | `DBL` — deafblindness | `DEAFBLIND` |
| `neu.html` | `NEU` — neurological (general) | `BRAIN` (with `PCS`) |
| `upl.html` | `UPL` — upper-limb impairment | `LMB` |

`scripts/generate/population_page.py` refuses these codes (`ERROR: Population 'VIS' not found.`), so
they could not be regenerated to match the current database and had been drifting since July.
`scripts/generate/build_site.py` states in its own header that it drives `site/specs/` only, so
nothing was regenerating `site/populations/` at all.

## The substantive reason, not just the mechanical one

**Two of these pages are the umbrella framing the project bans.** `ofs.html` describes itself as an
"Umbrella for orthostatic intolerance, dysautonomia, and chronic fatigue conditions"; `neu.html` as
a "General neurological category; includes MS, epilepsy, Parkinson, stroke sequelae." Collapsing
opposed demands into a broad umbrella is a named, repeatedly-caught failure mode — see
`governance/functional-taxonomy.md` §3.3, `references/project-standards.md` (RULE 2026-07-22) and
`DR-2026-07-22-work-from-axes`. The July replacement exists to curate from functional axes instead.
Leaving these rendered and reachable kept teaching the erased framing.

## What was on them, and what was lost

Nothing live. Every Best Practice Compendium entry listed on these pages is already
`RETRACTED — pending reverification`, and every best-practice determination section is empty
(`specifications` has held 0 rows since the 2026-08-06 clean-room reset). What the pages carried was
a description, an applicable-item list (VIS 43, OFS 30, DBL 17, NEU 9, UPL 8) and retracted-entry
tables — all of which are derivable from the database under the successor codes.

## Callers

No live page linked to any of the five. Two historical records mention `upl.html`
(`working/claims-docket.md`, `workplan/ratification-execution-register-2026-07-13.md`); both are
records of their date and are left as written.

Four of the five carried an explicit `STALE PAGE` banner added earlier on 2026-08-12, naming the
retirement and the successor code. `neu.html` did not — it never mentioned the renamed
`specifications` table, so the retired-vocabulary check never surfaced it. It is retired here on the
same grounds as the other four.
