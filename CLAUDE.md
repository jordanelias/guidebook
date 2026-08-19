# CLAUDE.md — working guide for the Accessible Built Environments Guidebook

**Rewritten 2026-08-19** to comply with the mission of the preceding fortnight, after an audit
found this file was itself a recursion engine: it made apparatus **cheap to add and expensive to
remove**, taxed the project's real deliverable more heavily than its cheapest busywork, and
enforced by machine only the rule that blocked deletion. The three guardrails that would have
caught this repository's actual failures had **zero** enforcing code.

> **Read `decisions/DR-2026-08-19-research-restart-operative-instrument.md` first.** It is
> RATIFIED and operative: it carries the execution order, the runbook, and the acceptance
> criterion. It is meant to be **run**, not consulted. This file is the mechanical map — write
> path, gates, traps. Where they disagree, the instrument wins and this file is what to correct.

---

## 0. What will actually stop you

Five rules. Everything else in this file is orientation.

1. **Commit format.** `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last.
   `date -u '+%Y-%m-%d %H:%M'`. Use `governance` when no project skill fits.
2. **Doctrine token on synthesis paths.** Touching `references/bpc-reasoning/`,
   `references/connection-reasoning/`, `decisions/` or `sessions/` needs
   `[DOCTRINE: <7-hex>] ` before the timestamp:
   `git rev-parse HEAD:governance/mission-and-epistemics.md | cut -c1-7`.
3. **Attestation on the same paths.** `attestations/<slug>.json` against
   `schemas/attestation.schema.json`.
4. **Never write `data/guidebook.db` directly.** Migrations only, via
   `scripts/emit_data_migration.py` → `scripts/migrate_db.py`. Append-only and immutable once
   committed: fix forward with a compensating migration. CI rebuilds and compares.
5. **A rename or removal is not done until the callers are swept.** Search every non-archived
   caller and fix each one. A sweep that stops at the filename is not a sweep — that exact
   shortcut left two dangling paths inside an attestation on 2026-08-19.

Rules 2 and 3 are a **tax on the deliverable**, inverted against rule-free `workplan/` files
which cost nothing at all. They are described here because they are still enforced — not because
they are defensible. Two facts a reader should have:

- The commit-message and doctrine-token check is `if: github.event_name == 'push'`, so it is
  **skipped on every PR**, and merge commits are exempt. On the PR path §0.2 is pure convention.
- **The doctrine-token apparatus is already queued for abolition** by the ratified instrument's
  §10 item 4, pending owner signature on **OD-10**. Nothing needs re-arguing; it needs signing.

Neither rule has ever caught any of the three failures in §2. Attestations have caught real
deviations — in their free text, which no gate reads for meaning.

---

## 1. Symmetry: deleting is as cheap as adding

**This replaces the old "owner-gate file moves and retirements" guardrail, which was the
pathology.** Adding a check cost a commit; removing one cost an owner decision. A system with
that gradient can only accrete, and it did: 65 checks, ~35k executable LOC, most of it policing
itself.

- **Code, checks, scripts, dead tables and views: delete them.** No owner gate. You need
  *evidence* — that it is unreferenced, or vacuous after a real batch, or superseded — not
  permission. Record the evidence in the commit.
- **Git history is the archive.** Do not copy files to `_archived/` to "preserve" them; git
  already did. `_archived/` exists for content retired before this rule and is not to grow.
- **Owner sign-off is still required for content and doctrine**: mission, audience, CRPD
  posture, population taxonomy, evidence-tier definitions, jurisdiction and work-product
  inclusion, licensing, trajectory (the DG-NON class in `governance/decision-protocol.md`).
  Those are judgements about the book. Code is not.
- **Adding apparatus carries the burden of proof**, not removing it. Before adding a check,
  script or table, state what wrong thing reaches the *guidebook* if it does not exist. If the
  answer is about the apparatus rather than the book, do not add it.
- **Nothing is added without naming what reads it.** This is the mirror of rule §0.5, which taxes
  removal only. An unread field, an uncalled script and an unregistered check are the same defect.
- **A specific, ratified authorisation beats a blanket caution.** On 2026-08-19 a session left 521
  lines of dead code in place, citing a six-word guardrail, when the code's own docstring and
  registry note already authorised its retirement. Blanket removal-friction winning ties against
  specific removal-permission is exactly how this file became a ratchet.

---

## 2. The three failure modes that are real

Derived from what has actually gone wrong here, not from what might.

**(a) A gate that passes having examined nothing.** Produced four separate times. Every check
must print `EXAMINED: <n>`; `scripts/run_checks.py` reports zero-subject passes as
NOTHING-IN-SCOPE and escalates blocking-and-vacuous ones. **When a check passes, confirm it had a
subject.** A blocking check whose session pointer is missing FAILs rather than SKIPs, deliberately.

**(b) Prose that contradicts the database.** *Rule: no hand-written counts in derived documents.
Generate them from the DB, or stamp the document with its generation date and a drift warning.* Counts in this file, in `index.html`, in manifests
and in audits have all drifted. **Derive every volatile fact — row counts, schema version, CI
status, the doctrine SHA, the active plan — from the live repo.** This file hardcodes none.
On 2026-08-19 a rendered search log claimed "three cells are EXACT" while the DB said two, made
stale within the hour by the same session's own correction.

**(c) A fabricated citation passing green gates.** On 2026-08-19 all five sources in the first
research batch were stored with **invented co-authors** — including the deletion of autistic
community co-authors from a Co-1 paper whose Co-1 warrant *is* their co-authorship. Six gates
passed it, because each asked whether the author fields were *populated*, never whether they were
*true*, while `verified_by_tool='crossref'` asserted the very property that had failed.

The fix, and the general principle: **verification must leave an artefact.**
`scripts/research/retrieval_log.py` persists every retrieved payload under `retrieval-log/`, and
`--verify-authors` diffs stored data against the bytes actually received — offline, no network,
no drift. Storage is cheap; the log is read only when auditing fidelity, which is exactly when it
is irreplaceable. **Never write a bibliographic field from memory when a payload is in hand.**

---

## 3. What this project is

A reference on architecture, accessibility and built-environment standards centred on **disabled
people**. Fixed doctrine: a **thinking tool and advocacy project, not an authority** — "the
purpose of this guidebook is to get people to ask the right questions." Not a prescription
manual, not a legal authority, not a substitute for professional judgment. "Inclusive /
accessible / universal" here always means *inclusion of persons with disabilities*.

Pre-launch, single author (`@jordanelias`). The governance and tooling are elaborate; **the
content is barely started**. Query the DB for the real state.

---

## 4. The data layer

`data/guidebook.db`, SQLite, committed as a binary blob. `PRAGMA user_version` is the schema
version. **There is no `sqlite3` CLI** — use Python, read-only:

```python
import sqlite3
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
```

**Backbone.** `items` (design parameters) × `populations` meet in `specifications`, the
per-(item × population) synthesis record. Evidence lives in `evidence_sources` and attaches via
`source_slug_links`, `evidence_population_match`, `search_admissions`. `source_locators` is a
**lead index of ~835 identifiers, not evidence** — the R9 duplicate gate currently cannot see it,
which is a known live defect (OD-5).

**Changing it.** Schema → new `scripts/migrations/NNN_slug.sql`, bump `user_version`, mirror the
Pydantic model. Data → `emit_data_migration.py --input` then `migrate_db.py`. Verify with
`migrate_db.py --rebuild /tmp/rebuilt.db`. `057_baseline_2026-08-12.sql` is the baseline.

**Research writes go to a scratch copy first.** `cp data/guidebook.db $SCRATCH`, point
`GUIDEBOOK_DB_PATH` at it inline on every call (the harness resets env between shells), then
capture the delta with `scripts/research/emit_batch_sql.py` and ship it as a migration. Every
write-time refusal stays live and the canonical DB's sha256 must not move until the migration is
applied.

`scripts/db.py` reads freely and has write subcommands for some tables — but **not** for
`search_candidates`, `evidence_population_match`, `economics_entries`, `case_studies` or
`jurisdictional_values` values, and `add-source` cannot write `doi_resolution_outcome`, `url`,
`pages`, `first_author_last` or author rows. Those need hand-written SQL against the scratch, and
that gap is where the fabrication of 2026-08-19 entered. There is no `next_ref_id` allocator;
mint above the `source_locators` high-water mark or you will collide with a held identifier.

---

## 5. Running checks

```
scripts/preflight.sh                                    # gate your diff vs origin/main
python3 scripts/run_checks.py --changed-from origin/main --explain
python3 scripts/run_checks.py --list                    # registry + quarantine
```

`governance/check-registry.yaml` is the single inventory; `run_checks.py` is the only thing that
invokes a check; CI and preflight both call it. Adding a check means editing the registry —
never a workflow — and now carries the burden of proof in §1.

CI is four workflows (`ci.yml` gates `main`; three scheduled). **Before assuming a red check is
yours, read the run and reproduce it locally** — this file deliberately does not record which
gates are currently red, because that claim went stale twice and was still being cited after the
backlog it described had cleared.

---

## 6. Evidence model, briefly

`governance/tier-system.md` is operative. **T1** primary controlled research · **Co-1** lived
experience / participatory design, **co-primary with T1** under CRPD Art 4.3 · **T2** synthesis ·
**Co-2** OT professional-body CPGs · **T3** grey primary · **T4–T6** the regulatory stratum,
walled off from full-strength anchoring.

Markers: **●** confirmed · **◐** policy/standards only · **○** grey/thin. Unmarked is an error.
Cell states: `stated` / `provisional` / `pending` / `not_applicable`.

**Co-1's warrant is co-production.** When you cite lived-experience work, the disabled people who
produced it are part of the evidence, not metadata. Erasing them while claiming the tier is the
worst failure available here.

**Synthesis routing:** only Opus-class models write `best_practice_synthesis`. **Citation
discipline:** confirmed real sources only — "I don't know" beats invention; quantified claims need
a locator or `[UNVERIFIED-QUANT]`.

Work from the **ICF/access-need frame with codes AND names**, never from bare axis codes and never
from population umbrellas. On 2026-08-19 a frame pulled as bare `axis_code` hid that a slug spanned
two demand mechanisms, and four of five searches were framed on one of them.

---

## 7. Traps

- **`.ignore` hides frozen records from ripgrep** — `_archived/`, `audits/`, `sessions/`,
  `references/search-log/`, `versions/`, `workplan/_superseded/`. "No matches" ≠ absent: confirm
  with `ls` or Glob. `grep -r` and `git grep` ignore it; Python tools see everything. Search those
  paths explicitly when doing history work. **Note the cost:** rendered search logs live under an
  ignored path, so the project's own research output is invisible to search.
- **Two session pointers.** `sessions/LATEST` is continuity; `sessions/LATEST-RESEARCH` is the
  subject of the blocking citation-mining gate. Update `LATEST` on any session close; update
  `LATEST-RESEARCH` only when the session actually did research.
- **Session ids: bare stem in the DB, `.md` in pointers and `emit_data_migration --session`.**
  Getting it wrong scopes a gate to nothing and it passes green.
- **Don't hand-edit generated output** (`parts/`, `site/`, `audits/`, `tools/*.html`) — regenerate
  with `scripts/regenerate_derived.sh`. A DB change makes them stale and two blocking checks red.
- **`schemas/*.py` ↔ SQLite drift is a bug**, not a convention.
- **PI versioning is intentional** — highest-numbered `governance/project-instructions-v*.md` is
  live, and it legitimately lags doctrine. Prefer `references/project-standards.md` and recent DRs.
- **Don't run `scripts/bootstrap.sh`** — PAT-gated, for the claude.ai surface.

---

## 8. Where to read for depth

| Question | Read |
|---|---|
| What to do now | `decisions/DR-2026-08-19-research-restart-operative-instrument.md` |
| Doctrine | `governance/mission-and-epistemics.md` |
| Current operative rules | `references/project-standards.md` |
| Tiers, markers, weighting | `governance/tier-system.md`, `governance/evidence-architecture.md` |
| Entity model, ICF frame | `governance/conceptual-model.md`, `governance/functional-taxonomy.md` |
| Decision process | `governance/decision-protocol.md` + recent `decisions/DR-*` |
| Architecture | `architecture/project-architecture-guidebook-v2.3.md` |

*Volatile facts are deliberately absent above. Derive them from the repo.*
