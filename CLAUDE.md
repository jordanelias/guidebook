# CLAUDE.md — Guidebook (code-only fork)

The **Accessible Built Environments Guidebook**: a reference on architecture, accessibility and
built-environment standards centred on **disabled people**. It is a thinking tool and advocacy
project, not an authority — "the purpose of this guidebook is to get people to ask the right
questions." *Inclusive / accessible / universal* here always means inclusion of persons with
disabilities; no design-for-everyone framing.

This fork carries code, data, contracts and the research corpus. It deliberately leaves behind
~1,200 files of session records, workplans, audits, attestations, decision records and governance
prose. That history had accumulated superseded and mutually contradicting rulings, and reading it
was costing more than it informed. `jordanelias/guidebook` retains all of it.

---

## Non-negotiables

1. **Commit format** — `{skill-name}: {action} [YYYY-MM-DD HH:MM]`, timestamp last.
   `date -u '+%Y-%m-%d %H:%M'`. Use `governance` when no skill applies.
2. **Never write `data/guidebook.db` directly.** Every change is a migration:
   `python3 scripts/emit_data_migration.py --session <id> --summary "<what>" --input changes.sql`
   then `python3 scripts/migrate_db.py`. The DB rebuilds from `scripts/migrations/` and CI compares.
3. **Never author `best_practice_synthesis` below the Opus floor.**
4. **A status column ships with its check.** A state nothing can contradict is an assertion, not data.
5. **A column holds one domain.** Value columns hold values; qualifying prose goes in the paired
   `<column>_note` overflow. A state written as prose defeats the gates that read it.

## The pipeline

topic → research across languages/jurisdictions → adjudicate → log source + associate to topic →
extract values + assess population relevance → flag findings for other topics → adversarial QC →
doctrine review → decompose into specifications → synthesise best practices → template + category →
catalogue (specifications, rooms, buildings, case studies).

Operation definitions — and why "mining" unqualified is banned — are in
`governance/pipeline-operations.md`. Discovery produces **sources**; extraction produces **values**;
synthesis produces **statements**.

## The one number

```
python3 scripts/audit/table_connectivity.py
```

The **fully-evidenced walk**: topics traceable from source through captured value and population
match to a published best practice, every hop required. It is currently **0 of 80**. Moving it is
the job. Report it at the top of every status.

## Running things

```
pip install -r requirements.txt && pip install jsonschema
scripts/preflight.sh                       # gate your diff
python3 scripts/run_checks.py --list       # the registry; every check lives there
python3 scripts/tests/test_db_integrity.py # expect ~31/41 — see below
python3 scripts/migrate_db.py --rebuild /tmp/rebuilt.db
```

`governance/check-registry.yaml` is the only inventory of checks; `scripts/run_checks.py` is their
only invoker. Adding a check means editing the registry. **Mutation-test before registering** —
plant the violation it exists to catch and watch it fail. A check that has only ever passed is
unverified.

**Expected red:** nine content rows in `test_db_integrity` (B01/B02/B05/B06 vocabulary,
C01–C04/G02 metadata backfill) and C10, which flags one published cell resting on DISPUTED sources.

## Layout

| Path | |
|---|---|
| `scripts/migrations/` | the chain — schema and data, forward-only, immutable once committed |
| `scripts/` | 93 python: audits, validators, generators, CI helpers |
| `schemas/` | Pydantic models + `attestation.schema.json` |
| `data/` | `guidebook.db` (canonical) + entity YAML |
| `governance/` | 3 machine-readable contracts + doctrine, tier system, taxonomy, operations |
| `references/bpc,search-log,fdr,conflict-matrices` | the research corpus — **input awaiting extraction**, not reference material |
| `skills/` | 20 authoring and research protocols |

**The DB is authoritative.** Generated output derives from it and never outranks it. When two
stores disagree, reconcile toward the DB.

## Two habits worth keeping

**Verify by execution, not by reading.** Five of six data-sourcing queries in one skill had been
broken for months because nobody ran them.

**Test the logic before blaming the data, and the data before blaming the logic.** The structure
here is consistently sounder than its population: the walk executes, 75 declared foreign keys have
zero orphans, and almost everything that looks like a broken pipe is an empty one.
