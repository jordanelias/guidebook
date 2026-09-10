# What is inert — strand 1 of 3: the check registry

Not "what might break if I change something" but "what is already dead, and how would
anyone know". Every line below was produced by running the check, not by reading it.

## The finding

**The 2026-08-06 corpus reset and the 2026-09-01 item-layer deletion were swept through
the check registry only PARTLY.** Six checks were correctly retired to `no_floor` on
2026-09-01 with a reason recorded in the registry itself. Four more were missed, and are
now permanently red or permanently vacuous against a corpus that no longer exists. That
permanent red is the thing CLAUDE.md rule 6 warns about — *a check that is red by
construction teaches its reader to ignore it* — and it is currently training its reader
across the whole battery, not just those four.

## Vacuous by design — NOT a problem, and the registry already says so

The `NOTHING-IN-SCOPE (10)` headline oversells the trouble. Nine of the ten carry a
recorded reason and are behaving correctly:

| Class | Checks | Why 0 is right |
|---|---|---|
| `empty-by-decision` | `validate_schema`, `validate_evidence_state`, `validate_verification_consistency`, `population_integrity_audit`, `pmp_audit`, `reasoning_doc_citations_audit` | corpus emptied deliberately; they fire again when the book has content |
| `changeset-scoped` | `attestation_presence`, `attestation_schema`, `attestation_verdict` | they examine HEAD~1..HEAD, not the 79 attestations on disk. 0 means *this commit owed none*. A floor would fail every non-synthesis commit |

The three attestation checks should arguably not appear in that headline at all: they
are working exactly as designed, and listing them beside genuinely dead gates is what
makes the list easy to skim past.

## Genuinely inert or miscalibrated — four

| Check | Level | State | Why |
|---|---|---|---|
| `validate_items` | advisory | **RED, floor 1, EXAMINED 0** | Floor never retired when `items` was emptied, unlike its six siblings. Worse: its declared `basis` is `base/base-parameter-vocabulary`, and after migration 071 that vocabulary is `base_parameters` — a table that exists and *can* be checked. The check is pointed at the deleted layer while its stated authority points at the live one. |
| `site_pages_fresh` | advisory | **RED, floor 1, EXAMINED 0** | Same class: `site/` holds no pages, floor never retired. |
| `test_verification_pipeline` | advisory | **RED, 3 of 18** | G01 wants language on ≥50 sources (live: 0). G02 wants ORCID on ≥30 authors (0). G03 wants COMPLETE ≥100 (8). All three are **pre-reset thresholds asserted against a post-reset corpus** — they were calibrated when the old corpus existed and were never recalibrated. |
| `check_rendered_docs` | **blocking** | NOTHING-IN-SCOPE | `examines-none-by-policy`: `specs/` holds one brief, `--all` deliberately declines to check it because it cites REF-ids the reset removed. And it would RAISE if it ran — its SQL selects `specifications.item_code`, dropped by 071 — and it derives its DB key from a *filename*, `specs/e-08-brief.html` → `E-08`. A blocking gate keyed on the contamination example CLAUDE.md §7 names. |

## Red with REAL findings — three, and these are work, not calibration

| Check | Finding |
|---|---|
| `retired_vocabulary` | Retired terms still taught by the reading surface: `applicable_groups` (1), `UNVERIFIED-1` (12), `VERIFIED-WITH-CORRECTION` (36) — overwhelmingly in `references/bpc/`. Couples directly to the unresolved archive question: moving `references/bpc/` would clear most of these and strand two other blocking gates. |
| `metadata_integrity_audit` | 8 COMPLETE/COMPLETE-STATUTORY rows carrying an open integrity flag. EXAMINED 9, so this one has a real subject and a real verdict. |
| `validate_reasoning` | `references/bpc-reasoning/room-acoustic-performance.md` is missing three required header fields (**BPC file**, **BPC population**, **Generated**). Small and fixable. |

## Red by construction — one

`validate_pydantic_schemas` reports 243 drift findings and is explicitly *"a REPORTING
tool, not a gate ... Exit code is always 0 unless run with --strict"*. It is red every
run and always will be until a per-model accept/reject policy exists, which its own
docstring defers as separate work. It is the single loudest contributor to the battery's
background noise.
