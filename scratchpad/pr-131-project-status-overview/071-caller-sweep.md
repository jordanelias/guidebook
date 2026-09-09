# Migration 071 — the callers still unswept

Rule 4: *a rename or removal is not done until the callers are swept.* Migration 071
re-keyed `specifications` from `(item_code, population_code)` to
`(parameter_id, four lens columns)`. This is the record of what that broke, what has
been fixed, and the one cluster that cannot be fixed without an owner decision.

Every "BROKEN" line below was **executed** against the live schema, not inferred.

## Swept and fixed

| Caller | What was wrong |
|---|---|
| `scripts/validate_evidence_state.py` | cell-state column list; fixed earlier in session |
| `scripts/validate_verification_consistency.py` | live query + selftest fixture |
| `scripts/tests/test_db_integrity.py` block K | re-keyed |
| `tools/pipeline_completeness.py` | re-keyed |
| `scripts/tests/test_validate_evidence_state_2_4.py` | fixture derived from live schema |
| `scripts/audit/register_integrity_check.py` | re-keyed |
| `schemas/evidence_state.py` | **the Pydantic mirror** — still demanded the pre-071 key |
| `scripts/tests/test_evidence_cell_state_2_3.py` | Part 1 re-keyed; Part 2 was building the pre-071 table from the frozen baseline and asserting FKs on dropped columns |
| `schemas/source_value_extraction.py` | `parameter_id` unmirrored |
| `schemas/base_parameter.py` | new table shipped with no mirror at all |
| `scripts/tests/_baseline_ddl.py` | claimed the baseline "holds the CURRENT schema"; now warns when it does not |
| 18 live views | all execute (checked; 072 repaired the three 071 broke) |

## BROKEN, unswept — the prior-version render surface

```
BROKEN  build_site.governing_refs      : no such column: ecs.item_code
BROKEN  spec_page.cells                : no such column: population_code
BROKEN  check_rendered_docs.governing  : no such column: item_code
BROKEN  check_rendered_docs.identity   : no such column: item_code
BROKEN  pilot_renderings.cells         : no such column: item_code
```

**Why these cannot simply be re-pointed.** Migration 071 severed the edge they
traverse. Each asks *"which specification cells belong to this item?"*, and after 071
`specifications` holds no item reference at all. The replacement the owner ruled —
`items` as a Part-4 render rollup **derived from** specifications (2026-08-26) — does
not exist yet. So the query has no post-071 form; it has a missing derivation.

**Why they are green today.** All four are dormant, and each for a reason that hides
the breakage rather than excusing it:

- `check_rendered_docs` is **BLOCKING** and reports NOTHING-IN-SCOPE. Its only subject
  is `specs/e-08-brief.html`, "reference-only since the 2026-08-06 reset". It derives
  its DB key from the *filename* — `e-08-brief.html` → `E-08`. So a blocking gate is
  keyed on the single item code CLAUDE.md §7 names as THE contamination example, and
  it passes by never running the query that would crash.
- `build_site`, `spec_page`, `pilot_renderings` all drive off `items`, which holds 0
  rows, so their loops never reach the broken SQL.

This is failure mode (a) — a gate that passes having examined nothing — sitting on top
of failure mode "a writer that cannot produce a state its own schema accepts".

## The decision this needs

These four, plus `scripts/assess/assess_cell.py`, are one cluster: the **prior-version
render and determination surface**, keyed on the item layer the owner emptied on
2026-09-01. Repointing them means choosing what a rendered page IS after the re-key —
a page per parameter, or a page per derived item rollup. That is the reading surface,
which is content, which is owner-gated (CLAUDE.md §8). It is not a code sweep.

Deleting them is the other option and CLAUDE.md §8 makes it cheap: git history is the
archive for code, and the evidence (superseded by 071; subject list is prior-version;
gate blocking-and-vacuous) is on the record above. What would be lost is the
determination logic in `assess_cell.py` — tier anchoring, T3-alone thresholds,
regulatory-stratum G1, grain-mismatch conditioning — which may have no other
implementation in the repo.

**Not decided here.** Recorded so the next session does not meet five green checks and
conclude the re-key was finished.
