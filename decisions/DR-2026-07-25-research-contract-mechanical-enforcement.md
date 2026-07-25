# DR-2026-07-25 — The research contract: mechanical enforcement of research validity

- Status: **ADOPTED — owner directive 2026-07-24/25**, verbatim: *"OUR RESEARCH IS INVALID IF IT
  IS NOT COMPLIANT WITH OUR GOVERNANCE AND VERIFICATION TOOLS AND RULES AND ETHOS"*, and
  *"synthesize all your lessons here and apply them going forward in such a manner that they are
  never ignored."* The validity principle is owner-stated doctrine; this DR records the mechanism
  built to enforce it and the schema it required.
- Date: 2026-07-25
- Category: **D-METH** (how research work is judged complete) with **D-SCHEMA** components
  (migrations 036, 037) and **D-OP** components (harness hooks, CI wiring, baseline file).
- Delegation: **DG-REVIEW.** The *validity principle* is owner-stated (DG-NON, already decided).
  What this DR decides is the mechanism — promoting already-canonical rules from prose (level 1)
  to scripts and CI (level 2/3) per architecture v2.3 `<enforcement_spectrum>`. It originates no
  doctrine: every one of R1–R15 restates a rule already written in `skills/`, `governance/`,
  `CLAUDE.md` or a prior DR. §6 lists what is raised for the owner rather than decided.
- Prepared by: Claude (Opus), session `session_2026-07-24-research-matrix-completion`.
- Affects: `scripts/audit/research_batch_dod.py` (new), `.claude/settings.json` (new),
  `.github/workflows/research-contract.yml` (new), `governance/research-contract-baseline.json`
  (new), `scripts/migrations/036_search_findings_and_candidates.sql` (new),
  `scripts/migrations/037_case_studies_and_economics.sql` (new),
  `scripts/audit/research_protocol_audit.py` (bug fix).
- Related: `workplan/methodology-and-pipeline-enforcement-plan-2026-07-23.md` (finding F1, whose
  predicted failure this session empirically confirmed), `DR-2026-05-09-adversarial-research-protocol`,
  `DR-2026-06-10-synthesis-model-floor`, `governance/tier-system.md` (Co-1 co-primacy),
  `governance/pipeline-contract.yaml`.

## Context — the failure this closes

A nine-batch research run logged 52 searches and admitted 18 sources while skipping most of this
project's own research doctrine: **zero Co-1 sources** (co-primary with T1 under CRPD Art. 4.3, and
"first; no exceptions" in `multilingual-research_SKILL`), **zero citation mining**
(`mining_direction='none'` on every row), **zero clause citations** on five regulatory sources with
quantified values and no `[UNVERIFIED-QUANT]` flags, and **zero combinatorial pairing** despite 23
populations, 17 access needs and 43 ICF codes sitting unused.

**The rules did not fail. Prose failed.** Every one was documented; an agent must choose to load it,
and attention degrades as context fills. This is exactly what
`methodology-and-pipeline-enforcement-plan-2026-07-23` F1 predicted: **28 enforcer scripts existed
on disk referenced by no workflow**, so a run could skip all of the above and still show green CI.

## Decision

**1. Research validity is mechanically gated.** `scripts/audit/research_batch_dod.py` implements
R1–R15, each restating an existing rule and each traceable to an observed violation. Non-compliance
means the research is invalid until remediated or waived with reasons in the PR.

**2. Enforcement runs where attention cannot degrade.** A `SessionStart` hook re-injects the
contract before context fills; a `Stop` hook runs the gate so a session cannot quietly end
non-compliant; CI runs the gate plus **six previously-unwired enforcers**
(`research_protocol_audit`, `metadata_integrity_audit`, `gap_mining_audit`,
`population_integrity_audit`, `graph_audit`, `pipeline_contract_audit`).

**3. Shakedown discipline is honoured with one exception.** All checks ship non-blocking (level 3)
except the **selftest, which blocks from day one**: it has no false-positive surface, and a gate
that has silently stopped detecting anything is worse than no gate. That is not hypothetical — the
first selftest *did* rot, crashing instead of testing when the checks were hardened, and was caught
only by manual re-run. It now clones the live schema and fails loudly.

**4. Inherited debt is disclosed, not hidden, and ratchets down only.**
`governance/research-contract-baseline.json` records pre-existing debt so the gate fails on
**regressions**, not on legacy. A permanently-red gate teaches people to ignore it. Baseline numbers
may **fall** as debt is remediated and may **never rise** to make a batch pass; the writer merges,
never deletes, and prints a REGRESSION warning instead of raising a threshold.

**5. Two schema additions were required** (D-SCHEMA):
- **036** — `search_executions.findings_note` + `.harm_finding`, and the `search_candidates`
  register. Substantive findings had been written into `deferred_reason`, which means *deliberately
  not searched* and which the coverage views filter on, so six genuinely-searched cells were being
  counted as deferred. Failure/harm evidence and off-slug material had no structured home at all.
- **037** — `case_studies` / `case_study_*` and `economics_entries` / junction tables.
  `schemas/case_study.py` and `schemas/economics.py` had existed as fully-specified Pydantic models
  with **no SQLite tables** — the schema↔DB drift `CLAUDE.md` §10 calls a bug — across eight ACTIVE
  slugs.

## Adversarial pass (this version)

The mechanism was attacked before being trusted. **Eight of eight attacks succeeded**, and each fix
is now a design rule recorded in the script:

- **R1 false-passed on a substring** — a run with 0 Co-1 searches and 0 Co-1 sources passed because
  one unrelated query contained "lived experience". The project's most important doctrinal
  commitment had its weakest check. → structural evidence required.
- **R2 was satisfied by one stub row** and never consulted `citation_mining`. → consults the register.
- **R4 matched population codes inside ordinary words** (SQLite `LIKE` is case-insensitive: `COM`
  in "accommodate", `AUT` in "autistic"). → text can never prove a crossing; structural linkage required.
- **R8 could never fail** — every zero-yield row could be deleted and it still passed. → append-only
  integrity check.
- **R7/R12 were one-row-forever thresholds.** → proportionate.
- **R10 ignored whether the locator resolved.** → requires the recorded outcome.
- **`--all` was permanently red on inherited debt.** → baseline.
- **The selftest had silently rotted.** → clones live schema, fails loudly, blocking in CI.

Design rules extracted: prefer **structural over textual** evidence; `> 0` thresholds are gameable;
a check that cannot fail is decorative; baselines ratchet down only; a rotted guard manufactures
false confidence.

## What this DR does NOT do

- Does **not** originate doctrine — R1–R15 restate existing rules; the validity principle is the
  owner's.
- Does **not** make content checks blocking (only the selftest blocks); promotion per check is a
  separate owner-gated step.
- Does **not** ratify migration **037's shape**. It was designed from the Pydantic models alone;
  consulting prior work afterwards found a real mismatch — `references/case-study-compendium.md`
  carries its own `## Schema` and uses `CS-01`, while the model's validator demands `CS-NNNN`, and
  case studies are §13.x in v9, not §12. **037 is flagged NEEDS-RECONCILIATION** and its tables ship
  empty. See §6.
- Does **not** claim the corpus is compliant. 494 tier-1..3 sources still lack population grading —
  disclosed in the baseline, not resolved.

## §6 — Raised for the owner, not decided here

1. **Reconcile 037 against `case-study-compendium.md`** (ID format `CS-01` vs `CS-NNNN`, the
   compendium's own schema block, §13.x vs §12) before any case study is ingested.
2. **Promotion of content checks to blocking**, per check, after shakedown.
3. **The 494-source population-grading backlog** — the largest single quality gap now visible.
4. **Independent review of the gate's thresholds.** They were authored by the agent whose work they
   judge; R1's original false-pass is direct evidence of that bias.
