# session_2026-09-01-lens-architecture

**Opened and closed 2026-09-01.** A read-only investigation the owner asked for, which produced a
finding that reversed the session's own parked migration — and then the migration was rebuilt to
match, landed, and its callers swept.

**Schema change: yes** — migration `065_one_link_table_four_lenses.sql`, `user_version` 64 → 65.
**Data migration: yes** — `data_20260901183203_2026-09-01-lens-architecture.sql`.
**No research, no evidence admitted.** `sessions/LATEST-RESEARCH` does not move.

Working record: `scratchpad/session_2026-09-01-lens-architecture/` — `LENS-ARCHITECTURE.md` (the
investigation), `insurance/` (the six declaration files the structural comparison was run with),
`build_decisions.py` and `render_drs.py` (one source for each of two dual homes).

## What the owner asked, in order

Ensure this session's decisions support a methodology where the disability taxonomies are
**abstracted**, so downstream tables reference them dynamically — *"evidence rows that concern ICF
codes for assistive mobility devices could also concern identities regarding wheelchairs could also
paraplegia medical etc"* · then the goal itself: *"a dynamically rendering website with a multimodal
lens and filters so that we can have specifications that are presented according to which lens the
user chooses and what filters they have selected"* · *"what best supports that final goal?"* ·
*"Fable 5 to read-only investigate what supports the final goal the best way in terms of table
joins, pointers, unions, filters, taxonomies, etc"*.

## Owner rulings recorded on contact

Three short messages, given while the investigation was running, which together settle a cardinality
the schema could not:

- *"it is OKAY for a link to be absent in a related taxonomy column"*
- *"but a link MUST be tied to at least one"*
- *"and ideally it ties into many"*

Recorded as **D-0182**. They reverse this session's own parked design, which had `CHECK (...) = 1` —
exactly one lens per row — and which would have refused the owner's own wheelchair example.

A fourth ruling, put and answered during the same exchange: **`rationale_ref` points at the DECISION
that authorises the edge**, recorded as **D-0183**.

## The finding

**The lens is a COLUMN, not a traversal.** The alternative — store a fact in one lens and cross to
the others at render — fails twice, measured against the live database:

| | |
|---|---|
| identity → ICF | 20 of 23 (`ALL`, `ID`, `MOVE` missing) |
| ICF → identity | 16 of 17 (`AX-COG-L` missing) |
| needs → ICF | 15 of 17 (`A-AT`, `A-TIME` missing) |
| ICF → needs | 15 of 17 (`AX-PAI`, `AX-THR` missing) |
| identity ↔ needs | **no direct map at all** |
| medical ↔ anything | **no table** — D-0170 ruled it exists; it did not |

Every gap is a silently empty page. And traversal **changes the answer**: the identity lens asked for
`DEAF` returns 20 items; the ICF lens asked for `AX-AUD` — the axis `DEAF` crosses to — returns 38
rows, because `DEAFBLIND` crosses there too. Only the first is a recorded fact. `D-0174` reserves
applicability to synthesis, so a render layer that crosses is adjudicating where nothing reviews it.

## What landed

- **One link table, four lenses.** `item_population_links` (372) and `item_axis_links` (158) become
  `item_taxonomy_links` (530, then 540), carrying `identity_code`, `icf_code`, `needs_code`,
  `medical_code`, at least one non-NULL. The ICF lens had a **second home**; it no longer does.
- **`base_taxonomy_medical`**, created empty. D-0170 named it on 2026-08-27; it had never existed.
  It is created now because SQLite cannot add a table-level CHECK by `ALTER`, so a `medical_code`
  bolted on later would sit outside the at-least-one rule.
- **`rationale_ref` is a typed pointer** at `decisions(decision_id)`. It was an unconstrained
  INTEGER with no foreign key — every integer satisfied OD-A's obligation.
- **The first ten edges that carry a warrant.** A-18 × DEAF/AUT/NDV/DEM cite `D-0177`; A-03/A-06/A-07
  × DEAF/COM cite `D-0176`. A-18 had **zero** links before this (BRK-20). They are **identity-lens
  only**: deriving their ICF and needs codes from the crossing maps would manufacture the exact
  inference the day's finding argues against.
- **The callers swept**, including six skills — `CLAUDE.md` §0.4 says a skill is a caller.

## What was given up, stated rather than buried

- **Uniqueness is weaker.** The old primary keys were `(item_code, population_code, subtype)` and
  `(item_code, axis_code)`. The wide form must permit A-18×DEAF×AX-AUD beside A-18×DEAF×AX-SPR —
  two mechanisms, not a duplicate. `idx_itl_row_identity` keeps every full lens tuple unique, but an
  identity-only row is no longer structurally prevented from sitting beside a wide row that already
  carries that identity. An audit is **owed**.
- **`applicability` is nullable now.** The 158 folded axis rows never carried it, and defaulting them
  to `applies` would assert a judgement nobody made. NULL means *not adjudicated*.
- **The graph extractor still draws only the identity lens.** `axes` is absent from its `PRIMARY`
  node registry, so emitting the ICF edge would fire `ref.dangling_structural` on all 158 rows.
  Registering `axes` is the one-line fix; it changes audit output, so it was recorded as owed rather
  than smuggled into a rename sweep. Coverage is unchanged either way — `item_axis_links` was never
  extracted.

## Verification

`scripts/audit/rename_insurance.py` compared a snapshot of canonical against a full rebuild from
migration history, under a declared fold map. **PASS**, with three findings declared and reasoned
rather than suppressed: the `pipeline_runs` heartbeat row (pre-existing — a rebuild at
`user_version` 64 diverges the same way) and the two uniqueness relaxations above.

The full suite is **PASS**. Four advisory checks fail — `validate_pydantic_schemas`,
`retired_vocabulary`, `validate_reasoning`, `test_verification_pipeline` — and all four fail
identically on `origin/main`, with the same counts (245 drift findings, 70 retired-vocabulary
occurrences). This change adds none. `--selftest` passes.

## Owed, carried forward

1. An audit for the identity-only-beside-wide-row dual home the relaxed uniqueness permits.
2. Register `axes` in `extract_db.py`'s `PRIMARY` so the ICF lens is visible to the graph audit.
3. `item_taxonomy_links` still has **no `db.py` writer** — the only route in is a hand-written
   migration, which `CLAUDE.md` §4 names as the setting the 2026-08-19 fabrication entered through.
4. `evidence_sources.tier` has no CHECK constraint, so `dbcore.check_values` returns an empty set
   for it and a tier rule cannot lean on the column's own vocabulary.
5. REF-00966's `co1_provenance` needs correcting **upward** from the retrieved payload (D-0178).
6. `base_taxonomy_medical` is empty, and no row can reference it until it is populated. That is
   content, DG-NON, and the owner's alone.
7. `populations`, `axes` and `access_needs` are still named for the pre-D-0170 vocabulary while the
   fourth lens already carries its ruled name. The parked rename closes that; SQLite's
   `ALTER TABLE RENAME` rewrites REFERENCES clauses, so 065 does not block it.
