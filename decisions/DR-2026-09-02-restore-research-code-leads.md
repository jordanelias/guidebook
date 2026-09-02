# DR-2026-09-02-restore-research-code-leads — Restore the 83 archived code/standard leads as research_code_leads, executing D-0181 rather than superseding it.

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0185` · category `D-OP` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-09-02 19:10 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner ruling 2026-09-02, choosing option A of three put to the owner.

## Rationale

The 2026-09-01 base-and-research-only ruling emptied jurisdictional_values as a side effect of deleting the item layer, because its item_code column is NOT NULL REFERENCES items. Neither quoted ruling named the table, and DR-2026-08-19 §1.5 had demanded the opposite sequencing: decide it separately, 'it must not be collateral damage'. It was collateral damage. D-0181 of 2026-08-31 had already called these rows research and already named the successor table, so restoring them EXECUTES that decision. Measured: the 109 archived records carry three non-null columns and collapse to 83 distinct (jurisdiction, standard_name) leads across 12 jurisdictions; the other 26 are the same standard restated per design parameter. 100% of surviving information is item-independent, so the only thing dropped is the item link -- the thing the ruling says must not exist -- and it survives in the archived filenames for provenance.

## Alternatives considered

- Confirm the deletion and record it as superseding D-0181 -- rejected by the owner: ~72 of the 83 leads exist nowhere else and would die with the archive.
- Merge them into source_locators -- rejected: that store already carries 24 rows holding both a standard_number and a DOI, and a standard has no DOI. That misalignment is what made REF-00037 carry a PLoS ONE DOI against a RIBA housing-guide title and falsely block an admission on 2026-09-01.

## Notes, and what remains owed

OWED, AND DELIBERATELY NOT DONE HERE. jurisdictional_values is left in place and empty rather than dropped, because v_code_floor_only reads it and CLAUDE.md holds a cross-stage view to be the most protected object in the schema -- the pointer rule 5's point-don't-copy actually means in SQL. That view joins on item_code, a column the owner ruled out of existence, so what it becomes is its own question. ALSO OWED: 11 of the 83 standards also appear in source_locators.standard_number and are reconciliation debt, not a licence to duplicate; and research_code_leads.jurisdiction carries NO CHECK because the vocabulary's nearest home, lang_jur_map, lacks two of the twelve values restored (GB and ISO, the latter a standards body rather than a country) -- registering a real jurisdiction vocabulary and pointing both at it is owed, not faked. D-0181's own note is now stale: it says the rename lands in 'the parked migration 065', but slot 065 was consumed by the four-lens link table on 2026-09-01.

## Delegation

Owner ruling. Work-product inclusion and the disposition of a retired corpus are judgements about the book, which governance/decision-protocol.md places in the DG-NON class and CLAUDE.md rule 0 makes non-delegable. DR-2026-08-19 §1.5 named this consequence specifically and demanded it be decided 'as its own decision, before items is touched'.

## Artifacts

- `decisions/DR-2026-09-02-restore-research-code-leads.md`
- `scripts/migrations/066_research_code_leads.sql`
- `scripts/migrations/data_20260902191029_2026-09-02-restore-research-code-leads.sql`
