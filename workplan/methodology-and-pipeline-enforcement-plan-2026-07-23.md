# Workplan: Methodology & Pipeline Enforcement Plan

**Date:** 2026-07-23
**Status:** PROPOSED — owner-gated. Nothing here is executed until ratified.
**Author:** Claude (Opus). Prepared at owner direction after a Fable-5 read-only
session audit and a stage-by-stage interrogation of `governance/pipeline-contract.yaml`.
**Decision surface:** the new *rules* are **D-METH / DG-NON** (owner decides — §6);
the *script wiring* touches `scripts/audit/` and `.github/workflows/`, both
**CODEOWNERS-protected** (owner sign-off required).

> **Premise (owner directive):** compliance must not rely on Claude instructions
> that degrade or are ignored as context fills. It must be mechanical — Python
> audit scripts and a **visible GitHub CI chain** that confirms process — promoted
> up the repo's own enforcement spectrum, extending the existing apparatus rather
> than re-spinning it.

---

## §1. Diagnosis — the facts (checkable; re-run the commands and verify)

This section is a **facts ledger**: every row is reproducible read-only. It is
kept separate from the judgment in §2–§8 so that trust in the facts never depends
on trusting the recommendations. (This separation is itself rule R4 below.)

**F1 — The pipeline declares 19 contracts; most are unenforced by CI.**
`scripts/audit/pipeline_contract_audit.py` reports **14 VERIFIABLE / 5 INCOMPLETE
/ 0 BROKEN**. But "VERIFIABLE" means only that the enforcer script exists on disk.
Cross-referencing each named enforcer against `.github/workflows/` (grep) shows
**only 4 of the 11 unique enforcers run in CI** (`validate_evidence_state`,
`adherence_log_audit`, `migrate_db`, `doctrine_recheck`). Re-scored by *actual CI
enforcement*:

| Enforcement reality | Count | Contracts |
|---|---|---|
| **No verification** (`check: null`) | 5 | discovery-provenance, derivation-handshake, convergence-independence, opus-routing, render-freshness |
| **Enforcer exists but never runs in CI** (Level 2) | 7 | adversarial-fields, pmp-strict-termination, evidence-verification-gate (rule #10), **nine-step-synthesis**, register-invariants, matrix-consistency, **definition-of-done** |
| **CI-verified** | 7 | governing-refs / no-rso-stated / tier3-threshold (path-gated), adherence-log, attestation-doctrine-binding, reproducibility-invariant, doctrine-recheck |

**F2 — Synthesis/reasoning-doc PRs are not verified by any *synthesis* contract.**
ci.yml's `schema`, `db_integrity`, and `governance` jobs are gated on `push` OR a
PR touching `data/`/`schemas/`/`governance/`; `commit-msg` (with the doctrine-token
step) is `push`-only. A PR that touches only `references/bpc-reasoning/**` fires:
`syntax` + `structure` (no path filter); the whole `audit.yml` `audit` job —
`source_slug_links_duplicates`, `citation_mining_completeness`, and
migration-reproducibility, **all blocking, no path filter**; and the three
`attestation_*` jobs (presence/schema blocking). *(Precision fix, v2: the earlier
draft listed only "reproducibility" here — corrected per the independent review,
which verified the two additional always-on audit checks.)* None of those checks
the **synthesis** stage: `validate_reasoning.py` (the **nine-step synthesis**
contract) is **not invoked by any workflow** (independently confirmed). This is the mechanism by which PR #56 (the
Category-E synthesis) passed CI green while failing the 9-step's spirit and
flip-flopping through its adversarial pass: **CI never checked the synthesis
contract.**

**F3 — `pipeline_contract_audit.py` itself is not in CI.** The meta-check that
surfaces null/phantom contracts is Level 2. Drift in the contract is invisible to CI.

**F4 — The tool-chain sequence is unreceipted in git.** `pipeline_runs` has 16
rows, **all `run_by_session='resolve-dois-action'`** (the DOI/URL job's phase_0–4
receipts). The content pipeline (research→…→render) emits its per-stage
`[ADHERENCE-LOG — stage N]` blocks only into the deployed claude.ai user-prefs
`<audit_trail>`, **which is not in git** (`pipeline-contract.yaml` header, lines
14–17). No `.claude/settings.json` exists, so **no harness hook** pre-empts or
records the sequence. Today only Claude's in-context attention orders the chain.

**F5 — The render→website tail is ungated.** `render-freshness` is `null`;
`parts/` + `site/` (116 HTML files) have no fingerprint/regeneration gate (unlike
the DB, which has a blocking reproducibility gate). No workflow builds or link-
or accessibility-checks the site. `grep` finds **no** HTML/WCAG/link validator in
`scripts/` or `requirements.txt`, and **no deploy/publish workflow**. For an
*accessibility* advocacy product, its own rendered site is neither
freshness-gated nor accessibility-tested.

**F6 — Two lifecycle stages are missing from the contract.** The contract runs
research → collection → judgment → synthesis → render. It omits **(a)** a
pre-research *scope / derivation-frame* stage (the frame is assumed correct — the
exact locus of the session's scaffold-not-graph failure) and **(b)** a post-render
*publish/deploy* stage (git artifacts ≠ what's served live).

**F8 — The committed `parts/` are ALREADY stale vs the DB (a live instance of the F5 gap).**
Regenerating `parts/v10/` from the committed DB (via `scripts/generate_parts.py`)
yields **16 changed files**; `part04.md` regenerates to **93 items vs the
committed 92** (adds `F-07 Thermal Zoning`) and **13 cell-state rows vs the
committed 0**. The generator is deterministic (a second regen is byte-identical),
so this is genuine staleness, not nondeterminism: **the published `parts/` product
currently misrepresents the canonical data.** (Independently verified; reproducible
by regenerate-and-diff.) This both motivates R6 and constrains it — see the WS2-d
correction in §3.

**F7 — What already exists and must NOT be rebuilt** (from the enforcement map):
`claims_docket.py` (working-diff claim register + commitment gate),
`register_integrity_check.py` + `validate_evidence_state.py` (T4–T6-only never
`stated`, no best-practice language on regulatory cells — the band rule),
`research_protocol_audit.py` CHECK 1 + `gap_mining_audit.py` CHECK 2
(falsification_condition required on gap closures), and `DR-2026-07-20-intra-category-cross-test`
(ACCEPTED — the sibling/cross-category test, "specify systems not atoms"). The
plan **extends** these.

---

## §2. The rules of application to codify

Each is stated crisply, mapped to its audit-origin, its decision category, and
what it needs (DR / RULE ledger entry / script). Rules already codified are
**cited, not re-proposed**.

| ID | Rule | Origin | Category / tier | Needs |
|---|---|---|---|---|
| **R1** | **Work from the evidence graph, not the item scaffold.** Synthesis derivation begins by enumerating the domain's slugs / `connections` / `convergence_assessment` for the declared populations+axes; the item scaffold is a rendering target, never the derivation frame. Any slug carrying anchoring-band sources in-domain must be **used or excluded-with-reason.** | Audit A3; F6(a) | D-METH / **DG-NON** | DR + RULE + script (WS2-a) |
| **R2** | **Red-team calibration.** A reversal is itself a claim: it must meet the evidence bar of the claim it overturns, carry a `falsification_condition`, and **name the specific new fact** that forced it. A red-team may downgrade-and-re-anchor, not retract, when other verified anchors survive. One adversarial pass per artifact *version*, run against the rewritten version — never appended to the old, never in the same context that produced it. | Audit A13; the session's flip-flops | D-METH / **DG-NON** | DR + RULE + partial script (WS2-b) |
| **R3** | **Definition-of-done is mechanical.** No "ready for review" / ratification while the 9-step synthesis check, the render-integrity battery, or an independent adversarial pass is unrun/unapplied. | Contract `definition-of-done` (exists, Level 2); F2 | D-OP / DG-REVIEW | CI wiring (WS1) |
| **R4** | **Facts ledger ≠ judgment.** A synthesis/reasoning artifact separates a re-verifiable facts ledger (DB-checkable rows) from the judgment layer; judgment claims cite ledger rows. | Audit fix #2 | D-METH / DG-NON | DR + template + script (WS2-c) |
| **R5** | **Grade atoms, specify systems.** Evidence bands attach per determination; specifications may be system-level with the weakest-component band disclosed. | Category-E §H.0 lesson | D-DOCT / DG-NON | DR (text rule; largely un-mechanizable) |
| **R6** | **Render-freshness + publish integrity** (new stages). `parts/`+`site/` must reproduce from DB state (regenerate-and-compare, mirroring the migration gate); a publish/deploy stage asserts the served product matches the validated artifacts. | F5, F6(b) | D-OP / DG-REVIEW | script + stage (WS2-d) |
| — | *Test every spec against category-siblings and cross-category ("systems, not silos").* | — | **ALREADY CODIFIED** | cite `DR-2026-07-20-intra-category-cross-test` — do nothing |
| — | *Non-English / high-tier-non-English coverage.* | — | **ALREADY CODIFIED** | `project-standards` RULE 2026-03-19 19:28; log the primary/lived recovery gap as a GAP, not a rule |

---

## §3. Enforcement design — mapped to the spectrum (extend, don't re-spin)

Three workstreams, ordered by leverage-per-cost. The repo's enforcement spectrum
(architecture v2.3 §`<enforcement_spectrum>`) governs: *promote only when
mechanically checkable AND drift is costly; new CI checks start non-blocking
(Level 3) and flip to blocking (Level 4) after a shakedown.* Every script follows
the house style (numbered checks in docstring, single `audit()`, `=`-report,
exit 0/1, `GUIDEBOOK_DB_PATH`-overridable, `--selftest`).

### WS1 — Promote existing Level-2 enforcers into CI (zero new scripts; highest leverage)

This alone closes **7** of the enforcement gaps and directly prevents the PR-#56
failure mode. Add a new CI job group (see §4) that runs, path-triggered on
synthesis/render/data paths, **non-blocking first**:

| Contract closed | Enforcer (exists) | Trigger paths |
|---|---|---|
| nine-step-synthesis | `validate_reasoning.py --mode all` | `references/bpc-reasoning/**`, `references/connection-reasoning/**` |
| definition-of-done | `claims_docket.py check` | any curated-dir change |
| register-invariants | `register_integrity_check.py` | render artifacts / pilot HTML |
| mode-stratum-matrix | `matrix_consistency.py` | `schemas/directness.py`, `governance/evidence-architecture.md` |
| adversarial-fields | `research_protocol_audit.py` | `data/**` |
| pmp-strict-termination | `pmp_audit.py` | `data/**` |
| evidence-verification-gate | `metadata_integrity_audit.py` | `data/**` |
| contract self-integrity | `pipeline_contract_audit.py` | `governance/pipeline-contract.yaml`, `scripts/audit/**` |

**Also fix the trigger-gating (F2):** add `references/bpc-reasoning/**` and
`references/connection-reasoning/**` to the path filters of the `schema` job (so
`validate_evidence_state` runs when a synthesis PR asserts a determination) — a
synthesis PR must trigger the judgment+synthesis+render checks, not skip them.

**ENGINE-LAG caveat:** `register_integrity_check.py` still enforces I3's *repealed*
absolute form (DR-2026-07-21 §5). Promoting it to CI **requires first** patching
it to the amended Option-A weak-band rule, else it will false-fail correct
weak-band rendering. This patch is a prerequisite, tracked here, owner-gated.

### WS2 — New scripts for the mechanizable gaps + new rules

Each is a new `scripts/audit/*.py` (DG-NON methodology decision **and**
CODEOWNERS-gated). Built with a `--selftest` mutation harness (the repo's "passes
count only after demonstrated firing" norm).

- **WS2-a `evidence_graph_coverage_audit.py` (R1).** Input: a synthesis reasoning
  doc's declared domain (populations/axes in its header) + a required
  `## Evidence inventory — slugs considered` section. Query the DB for slugs
  carrying anchoring-band (T1/Co-1/T2/Co-2/T3-clinical) sources linked to those
  populations; **fail if any such slug is neither cited nor listed
  excluded-with-reason.** This would have failed loudly on the missed
  `manoeuvring-footprint-vs-turning-radius-methodology` slug. Extends
  `graph_audit.py`'s `orphan.uncited_source` from corpus-global to per-doc-in-domain.
- **WS2-b `claim_flip_audit.py` (R2, anti-flip-flop).** Compares determination
  tuples / claim-register bands across the PR diff (git). A changed
  determination or band **without** a companion delta entry naming the new fact
  (`forced_by:` a REF-ID or a ledger row) **fails.** This is the mechanical form
  of "a reversal must name the new fact," and is the check the session most
  needed. Complements `claims_docket.py` (which is within-diff only) by adding the
  cross-commit axis.
- **WS2-c facts-ledger verifier (R4).** A sidecar `*.facts.yaml` per synthesis
  doc: rows of `{query, expected}`. `verify_facts_ledger.py` **re-executes** each
  query against the DB and fails on mismatch (the ledger is *run*, not merely
  annotated — the gap `claims_docket.py` leaves). Trust becomes re-checkable, not
  narrative.
- **WS2-d `render_freshness_audit.py` (R6, the render gate) — scoped down per the
  review.** *Corrected v2:* the earlier draft ("regenerate `parts/` and `site/` …
  mirrors the migration gate exactly") was two claims too strong.
  - **`parts/` half — feasible now, but with a precondition.** `scripts/generate_parts.py`
    deterministically rebuilds `parts/` from the DB, so a regenerate-and-compare
    gate is buildable. **But** F8 shows the committed `parts/` are *already* stale,
    so the gate is RED on the current tree. Precondition: **first regenerate and
    commit `parts/` (a one-time sync), then** the gate holds it fresh. Unlike the
    migration gate (which currently passes), this gate first *surfaces an existing
    bug* before it can protect against new drift — sequence accordingly.
  - **`site/` half — deferred; no build entry point exists.** `scripts/generate/*`
    are **per-page CLIs** (`spec_page.py` takes one `item_code`); no orchestrator
    loops them over the corpus, and `site/assets/*` are not DB-derived. A
    site-freshness gate therefore needs a **site-build orchestrator built first**
    (excluding `site/assets/`). Deferred until that orchestrator exists.
  - So WS2-d ships as a **`parts/`-only** gate after the one-time sync; `site/` is a
    later, larger piece. This still closes the render-freshness contract for the
    machine-generated `parts/` corpus.
- **WS2-e `cite_or_declare_audit.py` (R2/R5 support).** Connection/conflict
  reasoning-doc cross-link assertions must cite a CON-ID/conflict row or state
  "no existing row." Extends `reasoning_doc_citations_audit.py` (BPC-only today)
  to `references/connection-reasoning/`.
- **WS2-f `ship_clean_audit.py` (R5).** An operative doc (`Status: COMPLETE`)
  must contain **zero** retracted-position / "where §X corrects §Y governs" /
  controlling-note braid. Extends the `pre_rehab_banner_audit.py` cohort-linter
  pattern. (Superseded reasoning lives in git history, not interleaved prose.)
- **WS2-g (proportionality-flagged, DEFERRED) website accessibility + link check.**
  *Corrected v2:* "vendored axe-core/pa11y-equivalent, self-contained" was
  hand-waving — axe-core needs a live DOM engine and pa11y needs headless
  Chrome + node; vendoring minified JS does not make either runnable in CI, and
  "no external CDN" is the Artifact-runtime CSP rule, not a CI-dependency norm.
  What is genuinely feasible and proportionate to a 116-file static site is a
  **pure-Python static-subset linter** (lxml checks: `alt` text, `lang`, heading
  order, form-label association, landmark presence) + an internal-link checker —
  *not* an axe-core equivalent, and honestly weaker. *Mission-fidelity:* an
  accessibility project testing its own product is right in principle.
  *Proportionality:* deferred until the site is real (it is currently thin, with
  "not yet computed" banners) — stays **informational** when it lands.

### WS3 — Tool-chain sequence: receipts + verification (the sequence-consistency layer)

The most ambitious, highest-cost workstream — staged last and flagged for the
sharpest proportionality scrutiny (§7).

- **A committed run-manifest** — promote the off-git `[ADHERENCE-LOG — stage N]`
  spine into git as a machine-readable per-artifact receipt
  (`<artifact>.run.json`): which contracts ran, in declared order, with
  per-check result + warrant. This is the git-side reconstruction the contract
  header (line 16) already says is owed.
- **`sequence_audit.py`** — CI verifies the manifest against the declared chain
  for the task type (from `pipeline-contract.yaml`): all required stage-checks
  present, in order, passing. A skipped stage is a **failure**, not a silent
  omission — so context-degradation cannot drop a step unseen.
- **Harness pre-emption (`.claude/settings.json` hooks)** — a `SessionStart` hook
  installs deps + prints the contract checklist; a `Stop`/PreToolUse hook runs the
  relevant battery before a "done"/PR action. Hooks run at the *harness* level,
  so they do not degrade with context — the direct answer to the premise. **But
  hooks are local (≈Level 5) and per-session; they complement, never replace, the
  CI chain**, which is the durable, visible, shared enforcement. (Authored via the
  `update-config` skill; `.claude/settings.json` is not CODEOWNERS-listed, so this
  is the lowest-gate workstream — but also the least durable, hence secondary to CI.)

---

## §4. The visible CI chain (answering "do we require a visible chain?")

**Yes.** The repo already realizes it as named jobs running audit scripts as
required checks. This plan adds one job group and follows the in-repo
shakedown→blocking pattern (`audit.yml`'s `attestation_evidence` is the precedent:
`continue-on-error: true  # Level 2 during shakedown; flip to false after Day-7 gate met`).

Illustrative shape (a new `synthesis_contract` job in `ci.yml`, or a new
`pipeline-contract.yml` workflow):

```yaml
  synthesis_contract:
    name: Synthesis & render contract (shakedown — non-blocking)
    if: >-
      github.event_name == 'push' ||
      (github.event_name == 'pull_request' &&
       (contains(github.event.pull_request.changed_files, 'references/bpc-reasoning/') ||
        contains(github.event.pull_request.changed_files, 'references/connection-reasoning/') ||
        contains(github.event.pull_request.changed_files, 'data/')))
    runs-on: ubuntu-latest
    continue-on-error: true          # Level 3 during shakedown; flip to false after gate met
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5   { with: { python-version: "3.12" } }
      - run: pip install -r requirements.txt --quiet
      - run: python3 scripts/validate_reasoning.py --mode all --strict
      - run: python3 scripts/audit/claims_docket.py check
      - run: python3 scripts/audit/pipeline_contract_audit.py
      - run: python3 scripts/audit/evidence_graph_coverage_audit.py --changed
      - run: python3 scripts/audit/claim_flip_audit.py --base origin/main --head HEAD
      - run: python3 scripts/audit/ship_clean_audit.py --changed
      # render tail (path-gated to parts//site/ changes in a sibling job):
      - run: python3 scripts/audit/render_freshness_audit.py
```

Each check surfaces as a visible line in the PR's Checks tab — the "confirm
process" chain. Promotion to blocking (`continue-on-error: false`) is a separate,
owner-gated commit taken per check after its shakedown false-positive rate is
acceptable.

---

## §5. Rollout (phased; each phase owner-gated)

1. **Phase 0 — Ratify the rules.** Owner rules on **R1, R2, R4, R5 (DG-NON —
   new methodology/doctrine)** via short DRs (this plan supplies drafts on
   request). **R3 and R6 are D-OP/DG-REVIEW** (operational CI gates — agent
   decides, owner reviews; *not* owner-non-delegable). *Corrected v2: the earlier
   draft wrongly swept R6 into the DG-NON list, contradicting its own §2 table;
   per decision-protocol §2.2 a render-freshness CI gate is D-OP, never DG-NON.*
   No code ships before the doctrinal rules (R1/R2/R4/R5) are decided.
2. **Phase 1 — WS1 promotion + trigger-gating fix + the ENGINE-LAG patch.** Cheap,
   high-leverage, no new scripts. Ships non-blocking. Closes 7 gaps.
3. **Phase 2 — WS2 scripts** (a–f), each with `--selftest`, ships non-blocking.
   WS2-g stays informational.
4. **Phase 3 — WS3** receipts + `sequence_audit.py` + optional hooks. Highest
   scrutiny; may be deferred or scoped down per §7.
5. **Phase 4 — Flip to blocking**, per check, after each meets its shakedown gate.
   Update `pipeline-contract.yaml` `check:` paths + `enforcement_level`, and wire
   `pipeline_contract_audit.py` so contract drift is itself gated.

### §5.1 Demonstrated vs speculative — apply the spectrum's own bar honestly (v2)

The enforcement spectrum promotes a rule *only when drift is **observably**
costly*. The independent review's central correction: I met that bar for WS1 but
merely **asserted** it for the rest. Re-scored honestly:

| Tier | Workstreams | Justification | Disposition |
|---|---|---|---|
| **Demonstrated** | WS1 (promote existing enforcers + fix trigger-gating), WS2-a (evidence-graph coverage), WS2-b (claim-flip) | PR #56 is the observed, concrete failure these three directly prevent | **Ship** (Phase 1–2) |
| **Motivated but single-instance** | WS2-d/R6 (`parts/`-only render gate) | F8 shows a real current staleness bug | **Ship the one-time `parts/` sync now; the gate after** |
| **Speculative** | WS2-c (facts-ledger), WS2-e (cite-or-declare), WS2-f (ship-clean), WS2-g (site a11y), WS3 (receipts/sequence) | aspiration or single incidents, not observed *recurring* cost | **Defer** until a recurrence or a second contributor earns it |

**Backfill / exemption (the missing piece).** WS2-a's required
`## Evidence inventory — slugs considered` section, WS2-c's `*.facts.yaml`, and
WS3's `*.run.json` are **new structural contracts on the primary deliverable —
which is "barely started"** (most BPCs retracted-pre-rehab or partial, CLAUDE.md
§1). Imposing per-doc compliance on docs that mostly don't exist is the
scaffolding-for-scaffolding the spectrum warns against. Therefore: **any new
author-side structural requirement applies only to synthesis docs authored/edited
*after* its rule ratifies AND at `Status: COMPLETE`; the stub / `DRAFT` /
retracted-pre-rehab corpus is exempt** (mirroring the backfill-on-touch pattern
already used for attestations). No retroactive sweep.

---

## §6. Governance & gating (respected, not bypassed)

- **DG-NON (owner decides; I propose):** **R1, R2, R4, R5** are *new methodology/
  doctrine* → decision-protocol §2.2 default DG-NON. I draft the DRs; the owner
  ratifies. **R3 and R6 are D-OP/DG-REVIEW** (CI-gate operations — the §2.2 named
  example is "CI matrix updates"; not on the §2.3 DG-NON always-list).
- **CODEOWNERS:** every `scripts/audit/*.py` and every `.github/workflows/` edit
  is `@jordanelias`-gated. Each new RULE in `project-standards.md` is append-only
  via `session-consolidator`, and `decision_capture.py` C7 expects a paired DR.
- **Nothing blocking on day one.** The spectrum's promotion discipline is
  followed literally; blocking is a later, separate, owner-gated step per check.

---

## §7. Adversarial pass — commensurability & proportionality (vs mission/doctrine/standards/ethos)

*Held to the evidence bar (R2): each objection either survives or is answered
with a fact; the pass does not overswing into "scrap it all."* **This section was
refined by an independent adversarial review (v2); its verified findings are
integrated in §1 (F2 precision, F8), §3 (WS2-d, WS2-g corrections), §5/§6 (R6
gating), and §5.1 (demonstrated-vs-speculative split + backfill exemption). The
review's verdict — "slightly over-reaching: WS1 + WS2-a/b commensurate, the rest
speculative" — is adopted.**

- **Proportionality (the strongest objection).** The repo is single-author,
  pre-launch; the enforcement spectrum says promote *only* when drift is
  *observably costly*. **Answer:** WS1 promotes checks that already exist for
  contracts the project already declared it wants — near-zero new surface, and the
  drift cost is *demonstrated* (PR #56 shipped unsound because the synthesis
  contract didn't run). WS1 is unambiguously commensurate. WS2 adds ~6 scripts to
  an existing 22-script apparatus — proportionate. **WS3 is where the objection
  bites:** a git-committed run-manifest + sequence audit is heavy for one author,
  and risks becoming the very scaffolding-for-its-own-sake the repo already
  over-indexes on. **Concession:** WS3 is demoted to optional/deferred; start with
  the *cheap* half (harness hooks) and only build the manifest system if a second
  contributor or a demonstrated sequence-skip justifies it.
- **Ethos — "thinking tool, not authority."** Does hardening CI make the project
  feel rigid/authoritative? **Answer:** the enforcement is on *process integrity*
  (did the evidence graph get consulted; did the reversal name its fact; is the
  band honest), never on *content conclusions*. It protects the "ask the right
  questions" ethos by stopping unsound *best-practice* claims — the thing that
  most damages a disability-advocacy tool's credibility — from shipping.
- **False positives.** `claim_flip_audit` / `ship_clean_audit` could fire on
  legitimate revision or on quoted retractions. **Mitigations:** the delta-naming
  escape hatch (a flip *with* a named fact passes), the shakedown period (non-
  blocking until the FP rate is known), and `--selftest` harnesses proving each
  fires only on real mutations.
- **Duplication (guardrail 3).** Verified against the enforcement map: the plan
  *extends* `claims_docket` (adds cross-commit), `graph_audit` (adds per-doc-in-
  domain), `research_protocol_audit` (adds reversal-scope beyond gaps),
  `reasoning_doc_citations_audit` (adds connection docs), `pre_rehab_banner_audit`
  (adds general braid) — and **re-proposes nothing** ICCT/claims_docket/
  register_integrity already cover.
- **Commensurate *extent*.** Existing enforcement is deep on the data/judgment
  spine and absent on synthesis/render/sequence. The plan's weight lands exactly
  on the absent tail — it *balances* the existing scope rather than piling onto
  the already-covered core. That is the correct commensurability test: enforce the
  under-enforced, not the over-enforced.

---

## §8. What this plan deliberately does NOT do

- Does **not** auto-ratify any rule — DG-NON items are the owner's to decide.
- Does **not** make anything blocking on day one — shakedown first, per the spectrum.
- Does **not** add pre-commit hooks (Level 5) — deferred while contributor count = 1.
- Does **not** touch content, cells, or items — this is process enforcement only.
- Does **not** re-implement ICCT, `claims_docket`, `register_integrity_check`, or
  the gap-closure falsification checks — it cites and extends them.
- Does **not** commit WS3's manifest system without a demonstrated need (§7).

---

## §9. Revision history

- v1 (2026-07-23): initial draft on owner directive, grounded in the Fable-5
  audit + the contract-completion interrogation (§1 facts F1–F7).
- v2 (2026-07-23): independent adversarial-review corrections applied. Per R2,
  each names the fact that forced it:
  - **F2 precision** — a bpc-reasoning PR also triggers `source_slug_links_duplicates`
    + `citation_mining_completeness` (both blocking), not only reproducibility
    (verified in `audit.yml`). Fixed.
  - **F8 added** — regenerating `parts/v10` yields 16 changed files (part04: 93 vs
    92 items, adds F-07, 13 cell-rows vs 0); the committed product is stale.
  - **WS2-d rescoped** — the render gate is RED on the current tree and "mirrors
    the migration gate exactly" was false; there is no site-build orchestrator
    (`scripts/generate/*` are per-page CLIs). Now `parts/`-only, after a one-time
    sync; `site/` deferred.
  - **WS2-g corrected** — axe-core/pa11y "vendored self-contained" is infeasible
    in CI (DOM engine / headless Chrome); replaced with a pure-Python static-subset
    linter and deferred.
  - **R6 re-gated** — was wrongly listed DG-NON in §5/§6, contradicting the §2
    table; D-OP → DG-REVIEW per decision-protocol §2.2.
  - **§5.1 added** — demonstrated (WS1 + WS2-a/b) vs speculative (the rest,
    deferred) split, plus a backfill exemption so new per-doc contracts never
    sweep the "barely started" stub/retracted corpus. This is the review's most
    important finding: the plan applied the demonstrated-cost bar to WS3 but not to
    the speculative half of WS2. Corrected.
