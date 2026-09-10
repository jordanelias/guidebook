# Archived prior-version reference material

**Owner ruling 2026-09-09:** *"archive prior corpus so it can't be found by tools we use
commonly."* Frozen and archived here rather than deleted, **mirroring origin paths** — a file that
was `references/X` is now `_archived/references/X`, so a dangling reference in a frozen record, a
Decision Record or a skill resolves by prefixing `_archived/`.

## What "can't be found by the tools we use commonly" means, precisely

`_archived/` is in `.ignore`, so **ripgrep and the Grep tool no longer return these files.**
`grep -r`, `git grep`, Glob and Read still reach them — that is the deliberate escape hatch for
history work, and `CLAUDE.md` §7 tells sessions to use `grep -r` when they need it.

So archiving does not make this content unreachable. **It changes what a hit says about itself.**
`_archived/references/part04-item-index.md` is labelled prior-version by its own path;
`references/part04-item-index.md` read as live. That asymmetry is the entire benefit and it should
not be oversold.

## Why it could not stay

Every file here publishes the **item layer**, which the owner deleted from the database on
2026-09-01 (`befaa29`), in their own words: *"if E-08 already exists then the work is predisposed
to filing into a container that already exists, and that biases every finding."*

`DR-2026-08-19` §1.1 measured the problem: **42 of the 93 item names embedded a determination** —
`E-08 Corridor Clear Width (≥1200 mm Minimum on All Primary Routes)` states its answer in its own
name, so a search framed on it is a search for confirmation. The database was cleaned; these
indexes, registers and matrices kept handing the same containers to any session that grepped for a
topic. `db.py add-item` refuses for the same reason.

## What is here

Part-4 indexes, registers and matrices keyed on item codes; the per-item audit briefs; the
item×item connection register and conflict matrices. Derive the list rather than trusting this
paragraph: `git log --diff-filter=R --name-status -1 -- _archived/references`.

## What deliberately did NOT move

`project-standards.md` (the live append-only ruling ledger), `bpc-reasoning/`,
`connection-reasoning/`, `owner-notes/`, `search-log/`, `audits/`, `skill-registry.md` and
`tooling-register.md`.

**`bpc/` also stayed, and the reason is mechanical rather than editorial.**
`scripts/validate_cross_refs.py` check 4 asserts **BPC ↔ search-log co-existence** — every BPC has
a matching search-log and every search-log a matching BPC. Moving `bpc/` while `search-log/` stays
makes every search-log an `ORPHAN_SEARCH_LOG` and turns that **blocking** check red; moving both
would also strand `validate_bpc` (blocking, `min_items: 1`) with no subject at all, which
`run_checks.py` escalates as blocking-and-vacuous. That pair is one coupled decision with two
blocking gates attached, and it is the owner's.
