# Execution plan — reconciling the 2026-09-10 adversarial audits

Two read-only Fable audits ran against this session's diff: one on logic and
correctness, one on architecture, layer compliance and stage placement. This is the
reconciled register and the instructions to work it.

**Routing rule** (owner preference): Opus for judgment, reasoning and synthesis; Sonnet
for sweeps, batteries and mechanical enumeration; Haiku for nothing here. Every task
below names its tier and says why.

**Format.** Each task carries an AGONIST brief (build it) and an ANTAGONIST brief
(break it). The antagonist is read-only, runs AFTER the agonist commits, and its single
question is *"what did the agonist claim that is not true?"* A task is done when the
antagonist reports the claim survived AND names what it attacked the claim with.

**The standing failure this plan exists to stop.** Three times in one session, a caller
written in PROSE was invisible to a reachability test built on registry/CI/imports:
`emit_batch_sql.py` (the write path's capture step), `rename_insurance.py` (rule-4
rename insurance, unused during the re-key it exists for), and `audit_consolidator.py`
(deleted despite a bold BLOCKED marker in `workplan/2026-08-18-cull-execution-plan.md`
saying an active skill invokes it). **No task below may conclude "nothing calls this"
without a `grep -r` over `skills/`, `CLAUDE.md`, `workplan/` and `attestations/`.**

---

## ALREADY FIXED THIS SESSION — do not redo

| Defect | Fix | Verified by |
|---|---|---|
| Engine wrote `governing_refs` and not `specification_source_links`; H02 BLOCKING was red | engine emits junction rows | H01/H02 green, 5 examined each |
| `--scope` guard skipped when `--evidence-type` absent | type now REQUIRED | scratch: bare `--tier 1` refused |
| `--evidence-type CLINICAL` stored raw, invisible to `classify()` | normalised before store | scratch: stores `clinical` |
| `amend-source --field scope` wrote tier contradictions | re-derives, refuses | scratch: refused; consistent amend still accepted |
| `--identity ""` keyed and hashed different lenses, FK violation | blanks → None | scratch: `identity_code` None, FK clean |
| Engine ran with FKs OFF, laxer than its own replay | `PRAGMA foreign_keys=ON` | scratch FK check clean |
| `reject()` accepted any exception; two assertions vacuous | `expect=` names the reason | fault-injected `extra="allow"`: both red |
| `audit_consolidator.py` deleted while a skill invokes it | restored from `8730246^` | `--help` parses |

---

## TASK 1 — Layer 1 does not govern the stage that writes determinations  ·  **OPUS**

**The architecture audit's top verdict.** Ratified G2/G3/G6 grain rules, the four-state
thresholds and the attestation-hash rule have their only executable home inside
`scripts/assess/assess_cell.py` (`:25-27, 164-176, 313-323`), while `schemas/directness.py:80,82`
maps `co1 → specific` and `standard_eb → code` UNCONDITIONALLY — i.e. says the opposite.
Register item Q4. Opus tier: this is doctrine execution, and getting it wrong changes
what the book asserts.

**AGONIST.** Promote `source_grain()` into `schemas/directness.py` as
`grain_for(evidence_type, tier, co1_source_type)`. Keep `GRAIN_FROM_EVIDENCE_TYPE` as
the default map — `test_directness_2_2:80-84` asserts its contents and those stay true.
Add `NOT_ASSESSED` to the shared vocabulary so G2 is a first-class grade rather than an
engine-local string that caps by falling through. Re-point the engine to import it.
`test_directness_2_2` asserts the PRE-G2 semantics and **breaks by design** — the
workplan says so; update it and say in the commit that the ratified rule won.

**ANTAGONIST.** Does the promoted function produce the same grade as the engine did, for
every `(evidence_type, tier, co1_source_type)` triple? Enumerate all of them and diff
old against new. Any triple where they differ is either a promotion bug or a defect the
engine had — say which. Then: does any OTHER caller of `consolidate()` change behaviour?

**STOP.** If the promotion changes a grade for a live source, stop and report — that
changes a tier's weight and is owner-facing.

---

## TASK 2 — the engine anchors on tiers it itself reports as underivable  ·  **OPUS**

`check_tier_consistency` is computed per source (`assess_cell.py:238`) and surfaced only
in the report (`:473`). It never conditions `classify()` or the state. On the live
corpus the engine returns `stated / T1+CO1+T2` while `tier_inconsistent` lists **all 9
sources**. Synthetic confirmations: `co2` at tier 6 → `stated CO2`; `code` at tier 1 →
silently dropped to `other` → `pending`.

**AGONIST.** Make the flag load-bearing: a source whose stored tier is not derivable
from `(evidence_type, scope)` must not anchor. Decide and state whether it (a) refuses
the run, (b) drops that source from the anchor set with the reason recorded, or (c)
forces the cell to `pending`. **Recommend (b) with the reason in the report**, because
the corpus is entirely underivable today and (a) blocks all work until the backfill.

**ANTAGONIST.** After the change, run the engine on the live corpus. If it still returns
`stated`, the flag is still inert — prove which path bypasses it. Then check the
converse: does a fully-derivable corpus still reach `stated` where it should?

**DEPENDS ON** the scope backfill (Task 3) to be anything but `pending` everywhere.

---

## TASK 3 — backfill `scope` on the 9 admitted sources  ·  **OWNER DECISION, then SONNET**

Not a judgment call any more, and this is the finding that changes it: `amend-source
--field scope` now REFUSES any scope that contradicts the stored tier and ACCEPTS one
that agrees. So recording `high_control` on a tier-1 clinical source invents nothing —
it writes down the scope the adjudicated tier already encodes. `clinical` tier 1 →
`high_control`; tier 3 → `lower_control`; `sr_meta`/`co1` → `intrinsic`.

**OWNER GATE:** evidence-tier definitions are owner-gated (CLAUDE.md §8). The mechanism
is safe; the authorisation is not mine.

**AGONIST (Sonnet, after authorisation).** Nine `amend-source` calls through the
sanctioned path, scratch copy first, then `emit_data_migration` → `migrate_db`.

**ANTAGONIST.** Re-run `adjudication_integrity.py`: it must go from 9 of 9 underivable
to 0. Any residue is a real defect, not a backfill miss.

---

## TASK 4 — §2.3 jurisdiction distinctness counts nothing as something  ·  **SONNET**

`regulatory_richness()` (`assess_cell.py:299-309`) builds `{r.get("jurisdiction")}` and
tests `len(set) >= N`. Executed: `("US", None)` → provisional; `("US","us","US ")` →
provisional. Doctrine (§2.3) requires sources "from different jurisdictions"; a source
with no recorded jurisdiction is being counted as one.

**AGONIST.** Normalise: strip, casefold, drop None/empty before the distinctness count.
**ANTAGONIST.** Construct the cases that should now fail and confirm they do; confirm
three genuinely distinct jurisdictions still pass. Check no other site counts a raw set.

---

## TASK 5 — sweep the 071 re-key where it is still unswept  ·  **SONNET**

Rule 4. Enumerated by the architecture audit, verified as raising or mis-keyed:

- `scripts/generate/population_page.py:79`, `spec_page.py:77` — RAISE against the live DB
- `scripts/generate/pilot_renderings.py:234-239, 294-298` — raises; its private
  `derivation_sha` is item-keyed and now contradicts K01
- `scripts/audit/register_integrity_check.py:385-396` — still splits `data-cell` into
  `item_code, population_code` and inserts a synthetic `parameter_id=999999`
- `skills/specification-curator_SKILL.md:70-100`, `item-specification-writer_SKILL.md:91`
  — teach the pre-071 key. **A SKILL IS A CALLER.**
- `governance/evidence-architecture.md:114`, `pipeline-operations.md:28` — "(item × population)"
- `governance/research-contract.yaml:119` — "What a cell keys on is an open owner
  decision", now false. **Hash-pinned by `research_contract_sync` (blocking): the hook
  must be regenerated in the same commit.**

**ANTAGONIST.** Re-run the executed sweep: every query in the changed files, executed
against the live schema, must not raise. Then `grep -r` for the retired keys across
`skills/`, `governance/`, `CLAUDE.md`, `workplan/` and report anything left.

---

## TASK 6 — CLAUDE.md states things that are now false  ·  **OPUS**

Layer 0, auto-loaded, so a false statement propagates into every session. Both audits
found these independently:

- `:5-7` — "Where it disagrees with DR-2026-08-19, that instrument wins." No longer
  uniformly true: the owner overrode §12.5 on 2026-09-09.
- `:250-251, 256-257, 268` — `specifications.population_code` "a sweep owed",
  `item_code` "presently NOT NULL", both "stay unwritable until [the sweeps] are done".
  Migration 071 dropped both columns and did both sweeps.
- `:187-190` — `specifications` unwritable "because the owner emptied the item layer".
  Now unwritable because `parameter_id → base_parameters` holds 0 rows. Conclusion
  right, mechanism stale.
- `:292-305` — the archive bullet and its two derivation commands point at
  `references/part04-item-index.md` and `index.html`, which THIS SESSION moved under
  `_archived/`, which `.ignore:63` hides. The bullet asserts the opposite of the state.
- `:172-176` — names `add-source` for a refusal that lives in `insert_economics_entry`.
- `:169` — "blind to a live table three times"; it is now six.

**AGONIST.** Correct each. Do NOT restate counts — derive or date-stamp them (rule 7).
**ANTAGONIST.** For every factual claim in the changed sections, execute the check that
would falsify it. Report any claim that cannot be mechanically checked at all.

---

## TASK 7 — the parameter registry has no gate  ·  **SONNET**

`governance/pipeline-contract.yaml:53-56` and `check-registry.yaml:298` point
`base-parameter-vocabulary` at `scripts/validate_items.py`, which reads `items`. The
parameter layer was rebuilt at `base_parameters`; the check was not repointed — which is
also why `validate_items` is red with `EXAMINED: 0` against a `min_items: 1` floor.

**AGONIST.** Repoint the criterion to a check that reads `base_parameters`.
**ANTAGONIST.** Confirm it examines > 0 once a parameter exists, and that it can fail —
fault-inject a bad row.

---

## TASK 8 — smaller, verified, unfixed  ·  **SONNET**

Each was executed by the logic audit; each needs a fix and a fault-injected test.

1. `insert_term` mints multiple NAMES-NEW terms from ONE observation, and accepts
   whitespace-variant duplicates (`'manoeuvring  space'` beside `'manoeuvring space'`) —
   the clash check is `lower()` with no whitespace normalisation. Two rule-5 dual homes
   created through the sanctioned writer.
2. `_VALUE_BEARING` is ASCII-only: `١٢٠٠`, `１２００`, "at least twelve hundred
   millimetres", "not less than one point two metres", "≧ one metre", "minimal corridor
   width" all promoted to parameters.
3. `next_gap_id` mints `GAP-001` beside live `GAP-B01-001`, and the Pydantic validator
   (`evidence_state.py:181`) rejects the live id format outright.
4. 071 silently dropped `idx_specifications_state`.
5. NULL `verification_status` anchors `stated` unflagged.
6. An unknown `--slug` mints a gap saying "no evidence is linked via slug" rather than
   refusing the typo.
7. `v_value_independence` (`071:161-170`) groups by `parameter_id` AND the verbatim
   label, so two phrasings of one parameter fragment the independence count — the exact
   defect ACTION (4) was quoted to eliminate, moved from population to label.

---

## What is NOT in this plan, and why

- **The render surface** (`items` as a Part-4 rollup derived FROM specifications) — the
  edge 071 severed has no replacement, and choosing what a rendered page IS is content.
- **`room_page.py` and the question-author skill** — owner-gated, decision 8, open since
  2026-08-02. Owner ruled 2026-09-10 that owner-gated work stays.
- **Retiring `evidence_sources.tier`** — with `scope` recorded, tier IS
  `derive_tier(evidence_type, scope)`. Rule 5's remedy is writer-retire → reader-retire →
  NULL forward, a sweep across every reader including the engine. Named, not scheduled.
- **Retiring `specifications.governing_refs`** — same shape; the junction is the pointer
  and the JSON is the copy, but the copy is what `derivation_sha` hashes and K01
  recomputes, so dropping it re-keys the attestation.
