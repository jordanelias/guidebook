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

---

# `assess_cell.py` — the deletion case was wrong, and what replaces it

An antagonist pass was run against the proposal to delete `scripts/assess/assess_cell.py`
and its registered check. The proposal does not survive. Two of its three grounds hold;
the third is overstated; and it missed the fact that decides the question.

**Verified independently, not taken on the agent's word:**

- `schemas/directness.py` maps `GRAIN_FROM_EVIDENCE_TYPE['co1'] = specific` and
  `['standard_eb'] = code` **unconditionally**. `co1_source_type` appears nowhere in
  that module — only on the `EvidenceSource` model, where nothing computes grain from it.
- `workplan/2026-08-11-remediation-and-pipeline-anatomy.md:4661-4663` states rows 6, 7
  and 8 — G2 unassessed-dimension capping, G3 Co-1 grain by `co1_source_type`, G6
  `standard_eb` grain by (type × tier) — are **"UNENFORCED in the shared model"**,
  "`assess_cell.source_grain()` only".
- These are ratified: `decisions/RATIFICATION-PACKAGE-2026-07-12.md:2`, "ratified in
  full by owner directive 2026-07-13". Their promotion into the shared model is owed as
  register item Q4.

So `determine()` is the only implementation in the repository of three ratified doctrine
items plus the T3-alone and regulatory-stratum state rules. Deleting the file destroys
them. The item-keyed *driver* around it — `PILOT_CELLS`, `main()`, the INSERT block, a
`next_gap_id` that mints `GAP-1` and fails the schema's own `^GAP-\d{3,4}$` — is dead.
Those are separable.

## The fork, which is not mine to settle

`decisions/DR-2026-08-19-research-restart-operative-instrument.md` §12.5:

> **Permanently manual:** … anything touching `specifications` or the reasoning doc,
> which sits at the Opus synthesis floor behind the B-before-E gate. The contract's
> premise is that these are judgment acts machinery can only *check*.

That is the newest operative word on this table, and it admits two readings that lead to
opposite work:

**(i) The engine is retired as a WRITER.** "Judgment acts machinery can only check" is a
claim about the nature of the act, not about which file gets written. An engine that
computes `state='stated'` from tier arithmetic is *performing* the judgment, not checking
it. `scratchpad/session_2026-08-25-…/REPAIR-PLAN.md:193-203` says the same from the other
side: "a CLI that lets a session assert `--state stated` directly *is the fabrication
shape*." Under this reading: extract G2/G3/G6 into `schemas/directness.py` (discharging
Q4), keep `determine()` as a checker, delete the emit half.

**(ii) The engine is human-gated, not forbidden.** It already refuses the canonical DB
outright and emits SQL marked "replayable ONLY after owner ratification", which is
"manual" in the sense that matters. Under this reading: re-key it — roughly 50 lines,
no migration, and the design is already written at `REPAIR-PLAN.md` P1.3′/P1.4.

Two sessions (`sessions/session_2026-08-20…:212`, `…2026-08-22…:297`) read §12.5 as
reading (i) and called the engine dead. Those are session authors' readings. A search
that would have found an owner ruling either way —
`grep -rn -iE "owner[^.]{0,120}(engine|assess_cell)" sessions/ decisions/ references/project-standards.md`
— returns nothing, and `references/project-standards.md` has no hit for
`assess_cell|pilot engine|determination engine` at all. **No owner statement retires it
and none preserves it.** Rule 4b applies in both directions: do not report a ruling
absent from a search that could not have seen it, and do not declare open a question
already answered. This one is genuinely open.

## Done regardless of which reading wins

`test_assess_cell_pilot.py` assertion 6 passed for the wrong reason from migration 071
until 2026-09-09: the cell was keyed `(item_code="E-06", population="MOB")`, 071 re-keyed
the model, `extra="forbid"` rejected `item_code`, and a bare `except Exception` reported
that as "not_applicable without rationale rejected". Re-keyed, and the assertion now
names the rule it tests — a refusal is only evidence for the refusal you asked for.
Fault-injected: restoring the old key turns it red instead of green.

The other 12 assertions in that file exercise `determine()` and are the only automated
coverage of T3-alone, T6 richness, jurisdiction distinctness, all-disqualified and
has-unverified. They are not vacuous, and they are a further argument against deletion.

## Also broken, and run by nothing

`scripts/generate/pilot_renderings.py:233-243` selects `item_code, population_code` and
joins `items`. No registry entry invokes it; it is not in `regenerate_derived.sh` or
`preflight.sh`. Only `register_integrity_check.py:34` imports from it, and only
`REGISTER_MAP` / `ROLES` / `tuple_class`. Its private copy of `derivation_sha`
(`:294-298`) is still item-keyed and now contradicts `test_db_integrity.py` K01, which
was re-keyed to `parameter_id|lens` on this branch. Two implementations of one hash that
disagree.
