# Can we perform research? — derived 2026-09-12, branch `claude/research-capability-status-fxoybg`

Every figure below was derived from the live repo on the date in the heading. Re-derive before
relying on any of it (`CLAUDE.md` rule 7). Commands are given so you can.

## VERDICT

**Yes. Research is not blocked, and it has already run.** Batch 06 walked
base → research → evidence → judgment → specification, landed in canonical
`data/guidebook.db` (`PRAGMA user_version` 74), and its definition-of-done gate returns
**COMPLIANT on all nineteen rules**:

```
python3 scripts/audit/research_batch_dod.py --session session_2026-09-10-research-batch-06-circulation-geometry
```

The premise that "all the blockers must be resolved first" was true on 2026-09-10 and is false
today. `workplan/2026-09-10-road-to-batch-06.md` listed B1–B7. Six and a half are closed:

| Blocker | State, derived |
|---|---|
| B1 — contract says the cell key is an open owner decision | **closed** — `grep -n "open owner decision" governance/research-contract.yaml` returns nothing; R4's hook now reads "THE KEY IS RULED" |
| B2 — no runbook for the walk | **closed** — `workplan/2026-09-10-batch-06-runbook.md`, every command executed for real; `db.py next-id ref` exists |
| B3 — the cron's wake condition reachable by a batch | **closed** — DoD rule **R10b** fires on a URL-bearing admission left `verification_status NULL` |
| B4 — no extraction writer; engine gathered by slug | **closed** — `db.py add-extraction` exists; `gather_sources(conn, parameter_id)` (`scripts/assess/assess_cell.py:212`) joins on the extraction, not the slug |
| B5a — engine anchored `stated` on underivable tiers | **closed** — the tier gate conditions `COND_NON_ANCHORING` inside `anchoring()` (`:332-353`) |
| B5b — `scope` NULL on every source | **CLOSED 2026-09-12** by the owner's three rulings, executed the same day. All 11 rows carry `scope`; 0 NULL; `adjudication_integrity` VERDICT PASS |
| B6 — two specification skills teach the retired key | **closed** — both deleted, `ffe6d76` |
| B7 — regenerate before the gate | **closed** — runbook `:430`, `:485` |

## ~~THE ONE LIVE BLOCKER~~ — CLOSED 2026-09-12

`schemas/tier_derivation.py:115` keys the ratified tier on `(evidence_type, scope)`. A NULL `scope`
makes the stored tier underivable, `check_tier_consistency` returns False, and **B5a's tier gate then
makes the row non-anchoring**. Four rows are in that state:

```
python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);\
print(list(c.execute('select ref_id,tier,evidence_type,scope from evidence_sources where scope is null')))"
```

→ **returns nothing today.** The four rows were REF-00784, REF-00971, REF-00972, REF-00976, and the
owner ruled on all three questions that were put on 2026-09-12: REF-00971/972 to `lower_control` on
the design-control reading, REF-00784 and REF-00976 from payloads retrieved under the same ruling.
REF-00784 moved tier 1 → 3 on its own abstract's word ("Case series", "sample of convenience").
Full record: `references/project-standards.md`, entry dated 2026-09-12. Ruling 4 — retrospective
ratification of the five scope values applied on 2026-09-10 — was not put and is still open.

**Why this gated the NEXT batch and did not gate the last one.** Batch 06's cell was
`ramp gradient (TERM-001) × MOB`, whose two anchors (REF-00973, REF-00974) already carry
`high_control`. Batch 07's planned cell is `corridor width (TERM-002)`, and REF-00784/971/972 are
precisely the sources that measured corridor and passage geometry. Until their scope was settled they
were non-anchoring, so the cell would have come out on a Co-1 survey option phrase while the three
studies that actually measured it sat excluded. They now reach the engine — **at T3, not T1**, so
this does not by itself make the cell `stated`. Run the engine rather than predicting the state.

**Nothing else in the escalation set blocks a batch.** `adjudication_integrity` was quarantined on
these same four rows and is now GREEN (11/11 tier-consistent). It stays quarantined: its promotion
clause waits on OD-E, ruled 2026-08-31 (D-0179), whose subject holds 0 rows — so promotion has no
mechanical blocker left and is an owner call.

## SECOND — a determination has no NUMBER, and this is upstream of a gate

`specifications.value_min`, `value_max`, `value_unit` are written `NULL` by the engine
(`scripts/assess/assess_cell.py:1079`, hardcoded `None, None, None`) and read by nothing
(`grep -rn value_min scripts/ tools/ --include='*.py'`). The spine defines specification as
*"the determination: therefore 1200 mm, marked ●"*, and the stage resolves no figure. The one
determination in the database is `stated` with all three columns NULL.

This is a decision, not a defect to fix quietly: either value resolution gets built — and then a
`stated` cell with no value should be refused — or the three columns get dropped. Do not add a gate
before it is settled (`CLAUDE.md` §8: nothing is added without naming what reads it).

## THIRD — batch 06 is not formally CLOSED

`sessions/LATEST` and `sessions/LATEST-RESEARCH` both still name batch 05; no
`sessions/session_2026-09-10-research-batch-06-circulation-geometry.md` exists and no attestation
under that id. The D-0188 attestation already names that session id, so the record must be written
under exactly that stem. This is owed work, not a blocker.

## NOT blocking, contrary to earlier plans

- **Supersede design (W2).** `idx_spec_row_identity` is UNIQUE on
  `(parameter_id, identity_code, icf_code, needs_code, medical_code)`, so it refuses a *re*-run of
  the same cell only. A new parameter or a new lens tuple is a different row and needs nothing.
  `scratchpad/pr-134-repository-orientation/ORDER-OF-WORK.md` records that no owner ruling on
  supersession exists — the "owner decision" wording was session-authored.
- **The medical lens.** Ruled 2026-08-27 (D-0170), delegated 2026-09-11 (D-0188), and the ledger's
  correction sets its shape: populate by correspondence from `populations` and `axes`, ~15–20 rows,
  then on demand. `base_taxonomy_medical` at 0 rows is unexecuted work, not an open question.
- **The item layer.** Gone by ruling; `add-item` refuses. Any `[A-Z]-NN` code met in `references/`
  or `working/` is prior-version content.
