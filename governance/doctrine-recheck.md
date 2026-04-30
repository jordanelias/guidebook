# Doctrine Recheck Cadence
**Status:** CANONICAL — A13 Session 1
**Phase:** Stage A Phase 13 — Doctrine-recheck cadence
**Created:** 2026-04-30 03:00 UTC
**Doctrinal basis:** `workplan/workplan-co0007-v3.md` §A13 (resolves B-06 long-context drift; partial D-04 epistemic defense) · `workplan/workplan-co0007-v3-amendments.md` Amendment 6 (cadence: every 25 working sessions / at stage transition / on doctrinal-rule revision; sampling methodology from Stage 0.4 N=15 BPC contamination sample as recheck procedure) · `workplan/co0007-contamination-sample.md` (Stage 0.4 N=15 stratified sample; four-state classification CLEAN / AMBIGUOUS / STUB / MERGED per Amendment 3) · A12 decision-protocol.md §6 (CS8 decision capture activated)

---

## 0. What this document covers and what it does not

The project's doctrine — mission, audience, evidence methodology, population taxonomy, jurisdiction philosophy, time model, adversarial-use framework, legal posture, decision protocol — is established across A1–A12. Doctrine drift is the failure mode where, over many sessions, the project's working state quietly diverges from its canonical commitments without anyone noticing. The drift may be in synthesised content (BPCs that no longer match the methodology that produced them), in operational practice (sessions that proceed without the discipline the protocol requires), or in interpretive convention (terms used inconsistently relative to their canonical definitions). This document specifies the cadence and procedure by which the project rechecks itself against its doctrine, and the two code tools that operationalise the recheck.

The document does not produce the recheck. It specifies *when* rechecks run, *what* they examine, *how* the examination is conducted, and *how* findings are recorded. The recheck itself runs in dedicated sessions on the cadence's schedule.

The document does not duplicate adversarial-use review (A10 / CS9), which examines specific misuse vectors. Doctrine recheck examines the project's own internal consistency — whether the work-product matches the doctrine, not whether the work-product is being misused externally.

---

## 1. Recheck triggers (cadence)

Per Amendment 6, three triggers schedule a recheck:

### 1.1 Periodic — every 25 working sessions

A working session is one that produces or substantively modifies project content. Sessions that only adjust skills, fix typos, or rebase commits do not count toward the 25-session interval. The session-consolidator (CS8 wiring, A12 Session 2) maintains a working-session count; the recheck triggers automatically when the count reaches a multiple of 25.

### 1.2 Stage transition (A→B, B→C)

When the project transitions between stages, a pre-transition recheck establishes the doctrinal baseline. The transitioning stage's final session and the recheck session may be the same session (recheck-then-transition); a separate recheck session is preferred when the transitioning stage's final session is dense.

### 1.3 Doctrinal-rule revision

When a CANONICAL governance document or a project-standards RULE is revised — added, materially edited, superseded, or retired — a targeted recheck runs against the revised rule. The recheck examines: are downstream work-products still consistent with the revised rule? are there governance documents that depended on the prior version? The targeted recheck is narrower in scope than periodic and stage-transition rechecks; it is sized to the revision.

### 1.4 What is not a trigger

A new RULE that doesn't supersede or revise an existing one is not a trigger. A new governance document for a new phase (e.g., this A13 document) is not a trigger. A skill update or an operational change (commit-message convention, branch-protection state) is not a trigger. The criterion is doctrinal change — change to what the project commits to be — not operational change.

---

## 2. Recheck procedure

### 2.1 Scope and sequence

A periodic recheck (§1.1) runs five passes:

| Pass | Examines | Reference |
|---|---|---|
| 2.2 Doctrine inventory | All 13 CANONICAL governance docs; project-standards CANONICAL rules | A1–A13 governance corpus |
| 2.3 Cross-reference consistency | Each governance doc against the doctrine it depends on | doctrinal_basis fields per governance doc |
| 2.4 Drift detection | Current doctrine vs. prior recheck baseline | Prior recheck record |
| 2.5 Decision-register cross-check | Every CANONICAL RULE has a Decision record; every Decision record's `decision_artifacts` resolves | A12 register (post A12 S2) |
| 2.6 Contamination resampling | N≥15 BPC stratified sample; classify each per the four-state rubric | §3 below |

A stage-transition recheck (§1.2) runs all five passes plus a baseline-classification pass establishing pre-transition state.

A doctrinal-rule-revision recheck (§1.3) runs only passes 2.3, 2.4, and 2.5, scoped to the revised rule.

### 2.2 Doctrine inventory

The validator (`scripts/doctrine_recheck.py` §6) loads:

- All `governance/*.md` files where `Status: CANONICAL` appears in the front matter
- All RULE blocks in `references/project-standards.md` where the rule text contains `CANONICAL`
- All entries in `data/decisions/decision_register.yaml` with `status: ACTIVE`

The output is a doctrine snapshot — a single YAML structure recording governance-doc paths, RULE summaries, and Decision IDs. Snapshots are stored at `data/doctrine_recheck/snapshot_{YYYY-MM-DD}.yaml`.

### 2.3 Cross-reference consistency

Every CANONICAL governance doc has a `doctrinal_basis` field naming the prior phase work it depends on. The cross-reference check confirms: every doctrinal_basis reference resolves to a CANONICAL document or RULE that exists in the inventory. Missing or stale references surface as findings.

The check is one-directional (does X depend on Y, and does Y exist?) — it does not check semantic consistency (whether X's interpretation of Y matches Y's actual content). Semantic consistency is the human-judgment portion of the recheck.

### 2.4 Drift detection

The current snapshot is compared to the prior recheck's snapshot. Three categories of difference are reported:

- **Additions:** governance docs, rules, or decisions present now but not in the prior snapshot. Expected; not findings unless they conflict with prior items.
- **Removals:** items present in the prior snapshot but absent now. Examined: was the removal explicit (superseded, retired) or silent (deleted without record)? Silent removals are findings.
- **Mutations:** items present in both snapshots but with substantively different content. Examined: was the mutation explicit (versioned change with date and rationale) or silent? Silent mutations are findings.

Drift detection requires a prior snapshot; the first recheck records the baseline only.

### 2.5 Decision-register cross-check

After A12 Session 2 lands the seeded register, every CANONICAL RULE in project-standards must map to at least one Decision record (the Decision record's `decision_artifacts` lists the RULE's section reference). Pre-A12-S2, this check is suppressed (the register is empty by design).

Conversely, every Decision record's `decision_artifacts` should resolve to existing files. Stale artifact paths are findings.

### 2.6 Contamination resampling

Per §3 below.

### 2.7 Recheck record

Each recheck produces a record at `data/doctrine_recheck/recheck_{YYYY-MM-DD}.yaml` containing:

- `recheck_id`: `RC-NNN` zero-padded sequential
- `trigger`: one of PERIODIC, STAGE_TRANSITION, RULE_REVISION
- `trigger_detail`: session count or stage tag or rule reference
- `recheck_date`: YYYY-MM-DD HH:MM
- `recheck_by`: agent identifier
- `model_routing`: per A12 §4 notation (typically `opus/150/arbitrate`)
- `passes_run`: list of pass IDs (2.2–2.6)
- `findings`: list of RecheckFinding records (§5.2)
- `drift_summary`: aggregate drift statistics
- `contamination_summary`: aggregate sampling statistics
- `next_recheck_due`: trigger condition for the next recheck

---

## 3. Contamination resampling protocol

### 3.1 Methodology

The protocol adapts the Stage 0.4 contamination sampling (per `workplan/co0007-contamination-sample.md`) as a recheck procedure. It runs at every periodic and stage-transition recheck.

Sample size: N≥15 BPC files. Larger samples are preferred for stage-transition rechecks (N=20–25 recommended).

Stratification: by topic group, proportional to topic-group population, rounded such that each topic group with ≥1 BPC has at least 1 sample.

Selection: deterministic — first-alphabetical filename within each topic group's stratum. Determinism enables reproducibility (the same sample is selected if the recheck is rerun against the same HEAD).

The `contamination_sampler.py` tool (§7) implements selection mechanically.

### 3.2 Classification rubric

Each sampled BPC's `best_practice_synthesis` field is classified into one of four states (per Amendment 3):

| State | Definition |
|---|---|
| CLEAN | Doctrinally aligned with project-standards Core Doctrine; matches A6 evidence-state machine; matches A7 population taxonomy; cites Tier 1–6 sources per A6 hierarchy with appropriate convergence assessment |
| AMBIGUOUS | Tier-5-only derivation, or self-flagged PROVISIONAL, or unclear convergence assessment; not frankly contaminated but requires confidence-flag review |
| STUB | Synthesis pending Opus pass; placeholder content; not yet a synthesis |
| MERGED | CO-0006 redirect file pointing to another BPC; the redirect target is the substantive BPC |

The classification is a per-BPC human judgment by the recheck reviewer, supported by the tool's evidence display (the tool surfaces each BPC's tier citations, convergence flag, and source list).

### 3.3 Drift report

The drift report compares the current sample's classification distribution against:

- The Stage 0.4 baseline: 78% CLEAN / 7% AMBIGUOUS / 7% STUB / 7% MERGED
- The prior recheck's distribution

Material divergence (>15 percentage-point shift in any category) is a finding. The report distinguishes drift from sampling variance (small shifts in N=15 samples are within sampling variance) — a Z-test against the prior distribution surfaces statistically meaningful divergence.

### 3.4 What this does not do

Contamination resampling does not validate every BPC. It samples. The sample's classification distribution is an estimator of the corpus state; it is not a per-file audit. A BPC that the sample missed but that has drifted does not surface in this recheck — it surfaces in a per-file review elsewhere (B6 pilot validation, future per-Topic audits).

The protocol does not produce per-population coverage statistics. That is connection-register / coverage-matrix territory, not doctrine recheck.

---

## 4. Fresh-context decision-checking (B-06 mitigation)

### 4.1 The B-06 finding

Audit finding B-06 (long-context drift): over a long working session, an agent's interpretation of doctrine can drift from the canonical text without the drift surfacing within the session. The session's outputs are internally consistent but inconsistent with documents the session never re-read.

### 4.2 Mitigation

A periodic recheck (§1.1) runs in fresh context. The recheck session loads only the doctrine inventory (§2.2) — no prior session conversation, no prior turn-by-turn reasoning. The recheck examines work products from the prior 25 sessions and asks: is this consistent with the doctrine as a fresh reader interprets it?

Fresh-context decision-checking is built into the recheck procedure; it is not a separate practice. The cadence (§1.1) ensures it runs.

### 4.3 Targeted fresh-context checks

Major decisions per A12 protocol carry a `fresh_context_recheck_due` annotation in their Decision record. Decisions tagged `D-DOCT` with delegation `DG-NON` are checked at the next periodic recheck after they land. Decisions tagged `D-DOCT` with `DG-REVIEW` are checked at the recheck that follows their review confirmation.

The mechanism — a flag on the Decision record that surfaces in the recheck queue — operationalises B-06's mitigation without requiring the recheck to examine every decision every time.

### 4.4 D-04 partial resolution

Audit finding D-04 (epistemic defense doc-only) names a separate concern: the project's claims should be testable against simulated external critique. The `epistemic-defense` skill (referenced in workplan-v3 §A6.213) is the operational form. A13 partially resolves D-04 by establishing the recheck cadence; the skill itself is built in C2 per workplan-v3. The recheck procedure runs the skill when the skill is built (post-Stage-A); pre-skill, the recheck performs structural consistency checks (§2.3) and contamination sampling (§3) only.

---

## 5. Recheck record format

### 5.1 RecheckSession

The container record per recheck session.

| Field | Description |
|---|---|
| recheck_id | RC-NNN |
| trigger | PERIODIC / STAGE_TRANSITION / RULE_REVISION |
| trigger_detail | session_count for PERIODIC; stage tag for STAGE_TRANSITION; rule_id for RULE_REVISION |
| recheck_date | YYYY-MM-DD HH:MM |
| recheck_by | agent identifier |
| model_routing | per A12 §4 |
| passes_run | list of pass IDs |
| findings | list of RecheckFinding |
| drift_summary | dict with additions/removals/mutations counts |
| contamination_summary | dict with classification counts and Z-test results |
| next_recheck_due | when the next recheck is expected |
| notes | freeform |

### 5.2 RecheckFinding

A single finding within a recheck.

| Field | Description |
|---|---|
| finding_id | RC-NNN-FF (recheck_id + finding-NN) |
| severity | INFO / WARNING / ERROR |
| pass | which pass surfaced it (2.2–2.6) |
| description | the finding text |
| affected_artifacts | list of file paths or rule IDs |
| recommended_action | what should be done |
| status | OPEN / RESOLVED / DEFERRED |
| resolution_commit | OID if RESOLVED |
| notes | freeform |

### 5.3 ContaminationSample

One record per sampled BPC.

| Field | Description |
|---|---|
| recheck_id | parent RC-NNN |
| bpc_path | file path |
| topic_group | stratification group |
| disposition | CLEAN / AMBIGUOUS / STUB / MERGED |
| disposition_rationale | 1–2 sentences explaining the call |
| reviewer | agent identifier |
| review_date | YYYY-MM-DD HH:MM |

---

## 6. Validator: `scripts/doctrine_recheck.py`

### 6.1 Scope

The validator runs passes 2.2–2.5 mechanically and produces a structured input for the §3 contamination resampling pass (which has a human-judgment component).

### 6.2 Inputs

| Path | Purpose |
|---|---|
| `governance/*.md` | CANONICAL governance docs (parsed for `Status: CANONICAL` and `doctrinal_basis`) |
| `references/project-standards.md` | RULE blocks (parsed for `RULE:`, `DATE:`, CANONICAL marker) |
| `data/decisions/decision_register.yaml` | Decision register (post A12 S2) |
| `data/doctrine_recheck/snapshot_*.yaml` | Prior snapshots for drift detection |
| `data/doctrine_recheck/recheck_*.yaml` | Prior recheck records |

### 6.3 Outputs

A snapshot YAML (`data/doctrine_recheck/snapshot_{YYYY-MM-DD}.yaml`) and a draft recheck record (`data/doctrine_recheck/recheck_{YYYY-MM-DD}.draft.yaml`) with mechanically-detected findings populated. The recheck reviewer adds contamination-sampling findings (per §3) and finalises the record.

### 6.4 CLI

| Flag | Behaviour |
|---|---|
| `--snapshot-only` | Run pass 2.2 only; produce snapshot |
| `--cross-ref` | Run passes 2.2–2.3 |
| `--full` | Run passes 2.2–2.5 (default) |
| `--baseline-against PATH` | Use the named snapshot as the prior baseline (default: most recent) |
| `--report` | Print summary; exit 0 always |

Exit codes: 0 = pass with no ERROR findings; 1 = ERROR findings present; 2 = config error.

### 6.5 What this does NOT do

The validator does not perform contamination sampling (that is `contamination_sampler.py`'s job). It does not perform semantic consistency checks (that is human review). It does not enforce the cadence triggers — those are tracked by session-consolidator. The validator is invoked when a recheck is scheduled; it does not initiate rechecks.

---

## 7. Sampler: `scripts/contamination_sampler.py`

### 7.1 Scope

The sampler implements §3.1 selection methodology mechanically. It walks the BPC corpus, stratifies by topic group, and selects a deterministic sample.

### 7.2 Inputs

| Path | Purpose |
|---|---|
| `references/bpc/*/` | BPC corpus organised by topic group |

### 7.3 Outputs

A sampling manifest at `data/doctrine_recheck/sample_{YYYY-MM-DD}.yaml` containing the sampled file paths, the topic-group stratification, and a per-BPC `disposition: PENDING` placeholder. The recheck reviewer fills in the `disposition` field via human classification.

### 7.4 CLI

| Flag | Behaviour |
|---|---|
| `--n N` | Sample size (default: 15; minimum: 15) |
| `--seed N` | Random seed for tie-breaking when stratification underdetermines (default: 0) |
| `--corpus-root PATH` | Override default `references/bpc/` |
| `--output PATH` | Override default output path |

Exit codes: 0 = sample written; 2 = corpus not found.

### 7.5 What this does NOT do

The sampler does not classify the sampled BPCs (that is human judgment). It does not enforce disposition-distribution targets (the sample reflects the corpus; the corpus state is what is being measured). It does not run statistical tests against prior samples — that is done in `doctrine_recheck.py` aggregation.

---

## 8. CS1 cross-stage activation

### 8.1 What CS1 activates

CS1 (cross-stage 1) per `workplan/workplan-co0007-v3.md`: doctrine-recheck cadence. With this document landing, CS1 is LIVE. From this point forward:

- Every 25th working session triggers a periodic recheck (cadence enforced by session-consolidator)
- Every stage transition triggers a stage-transition recheck (the transitioning phase's close commit references the recheck record)
- Every doctrinal-rule revision triggers a targeted recheck (tracked at session close)

### 8.2 Operational integration

Session-consolidator (per CS8 / A12 Session 2 wiring) maintains the working-session counter. When the counter reaches a multiple of 25, session-consolidator surfaces a "recheck due" advisory at session close. The advisory is non-blocking — the session that triggered the threshold completes normally — but the recheck is the next session's first action.

### 8.3 Recheck-of-A13

A13 itself is doctrine. Subsequent rechecks examine A13 too — the recheck procedure does not exempt itself. A finding that the recheck procedure is missing a check, or that a trigger is wrongly calibrated, is recorded and surfaces for revision at the next governance update.

---

## 9. Status

| Field | Value |
|---|---|
| Created | 2026-04-30 03:00 UTC |
| Phase | Stage A Phase 13 — Doctrine-recheck cadence — Session 1 |
| Status | CANONICAL |
| Forward dependencies | A12 Session 2 (decision register seeding required for §2.5 to operate fully); session-consolidator update (Amendment 6 cadence wiring); first periodic recheck at session count 25 |
| Schema dependencies | `schemas/doctrine_recheck.py` (new); `schemas/enums.py` (extended) |
| Resolves | B-06 long-context drift (mitigation in place via §1.1 + §4); D-04 partial (epistemic-defense skill is post-Stage-A; structural consistency is in place) |
| Closes | Stage A done criterion: "Doctrine-recheck cadence operational (A13); CS1 LIVE" |

### 9.1 Change log

| Date | Change |
|---|---|
| 2026-04-30 03:00 | Initial canonical version. Cadence triggers (periodic 25-session / stage-transition / rule-revision); 5-pass procedure; contamination resampling per Stage 0.4 methodology; recheck record format; validator + sampler scope; CS1 LIVE. |

---

**End of A13 governance document.**
