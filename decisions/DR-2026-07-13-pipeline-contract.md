# DR-2026-07-13: Pipeline contract — one machine-checkable stage-gate spec for evidence work

- Status: **PROPOSED — pending owner ratification. Not owner-ratified.** (Authored by Claude in the vectorized-audit-tool build; it introduces no new doctrine and is advisory / Level-2 until the owner ratifies it.)
- Date: 2026-07-13
- Prepared by: Claude. Grounded in a full read of the enforcement stack (`governance/`, `decisions/`, `schemas/`, `scripts/audit/`) performed this session, not from memory.
- Category: **D-METH** (methodological — how evidence work is gated as it flows through stages). Default delegation **DG-NON** (new methodology is the owner's to adopt); other agents propose, the owner decides.
- Creates: `governance/pipeline-contract.yaml` (the declarative spec), `schemas/pipeline_contract.py` (its Pydantic model), `scripts/audit/pipeline_contract_audit.py` (validator + referential-integrity check, ships its own `--selftest`), and graph ingestion (`scripts/audit/graph/extract_contract.py`) so the contract's stages/checks become edges the structural audit traverses.
- Related: `governance/conceptual-model.md` §2.1 (the E-02→E-03→E-01→E-08 spine), `governance/evidence-architecture.md` §5/§6/§10, `governance/doctrine-recheck.md`, `DR-2026-07-13-integrity-protocol-three-modes` (P2/P3), `DR-2026-07-13-value-genealogy-and-derivation-handshake` (H2/H4), PI v10.14 rules #7–#11, `schemas/attestation.schema.json`, `architecture/project-architecture-guidebook-v2.3.md` `<enforcement_spectrum>`.

## Context — the gates exist; the contract that names them in one place does not

The project already enforces evidence integrity at many points: the rule-#10 verification gate, `governing_refs` non-emptiness, the Tier-3-alone threshold, the derivation handshake, invariants I1–I5, the `[ADHERENCE-LOG — stage N]` block, attestations + the doctrine-SHA token, the integrity-protocol Mode-3 battery, and the 7-invariant reproducibility gate. But these gates are **scattered across a dozen documents and scripts**, and three specific weaknesses follow from that scatter:

1. **No repo-side stage model.** The numbered `[ADHERENCE-LOG — stage N: <name>]` list lives only in the *deployed* claude.ai user-preferences `<audit_trail>` section — it is **not in git**. A session cannot mechanically answer "which gates must a judgment-stage output clear before synthesis?" from the repository alone.
2. **Phantom enforcement is undetectable.** Governance prose and skills cite enforcer scripts by name; some cited checks do not exist or were renamed (the shape audit and skills read found several). Nothing verifies that every named gate resolves to a real, present enforcer.
3. **Coverage gaps are implicit.** Some stage criteria (discovery provenance, value-level convergence, render freshness) have *no* committed enforcer, but that is nowhere stated as such — it reads as "covered" when it is not.

This DR proposes a single machine-checkable file that **declares** each stage's criteria and **names** the ratified enforcer for each, and an audit that keeps that file honest.

## Proposed decision

Adopt `governance/pipeline-contract.yaml` as the canonical, machine-checkable declaration of the evidence pipeline's stage gates, with `scripts/audit/pipeline_contract_audit.py` as its Level-2 enforcer. Specifically:

- **P-1 — Stage spine.** Five stages (`research → collection → judgment → synthesis → render`) mapped onto the ratified entity spine (`conceptual-model.md` §2.1) and PI rules #7–#11, plus a `cross_stage` block (adherence-log, attestation/doctrine-binding, definition-of-done, reproducibility, doctrine-recheck). The stage ids are the **repo-side reconstruction** of the deployed `<audit_trail>` spine and are advisory **until reconciled against that deployed list (owner action) — a ratification precondition, not a silent claim of correctness.**
- **P-2 — Each criterion names its enforcer.** Every criterion carries `check:` = a repo-relative path to an already-ratified enforcer, or `null` where the criterion is **declared-but-unenforced** (an honest coverage gap). The audit classifies each as VERIFIABLE / INCOMPLETE / BROKEN and **fails only on BROKEN** (a named enforcer that does not exist). VERIFIED-BY `pipeline_contract_audit.py` on this branch: 15 VERIFIABLE, 4 INCOMPLETE, 0 BROKEN across 5 stages + 5 cross-stage gates.
- **P-3 — The contract introduces no new doctrine.** "handshake" / "contract" / "definition of done" are **not** doctrinal vocabulary here (they appear zero times in `governance/`); each maps onto an existing primitive — a *gate* + an `[ADHERENCE-LOG — stage N]` block + an *attestation* + integrity-protocol *Mode 3*. The contract is an index and a referential-integrity checker over the existing stack, not a seventh restatement of it. Where the contract and a cited source diverge, the cited source governs.

## Self-application (per the integrity-protocol Mode-1 clause)

The rule this DR proposes — *"every declared gate must resolve to a real enforcer, and unenforced criteria must be marked as such"* — is applied to the contract itself: `pipeline_contract_audit.py` runs over `pipeline-contract.yaml` and reports 0 BROKEN and 4 explicitly-labelled INCOMPLETE criteria; and the audit **ships its own `--selftest`** (a malformed contract is rejected; a phantom check path is classed BROKEN) — the same "a verifier that has only ever passed is unverified" rule the contract's own `definition-of-done` criterion cites. The flagship example (the corridor determination) is not re-adjudicated here; the contract only routes it through the existing judgment/render gates.

## Adversarial review (author's Mode-3 pass; an independent pass is owed before ratification)

Strongest objections considered, with responses:

- **"It re-fragments governance by adding new vocabulary."** — It adds one YAML + one script, not a doctrine document; P-3 binds every term to an existing primitive and cedes authority to cited sources. If anything it *de*-fragments, by indexing the scattered gates in one queryable place.
- **"It gives false assurance that stages are gated."** — The opposite: the audit's check 3 reports that **10 of 15 named enforcers ship no `--selftest`** (VERIFIED-BY the audit run), so the *assurance gap* is surfaced, not hidden; and 4 criteria are printed as INCOMPLETE every run.
- **"The stage ids are invented and may contradict the deployed `<audit_trail>`."** — Conceded and made a ratification precondition (P-1); the ids are labelled a reconstruction, not the canonical list.
- **"`pipeline_contract_audit.py` imports pydantic — inconsistent with the stdlib-only audit spine."** — The graph *spine* stays stdlib+PyYAML (`extract_contract.py` parses YAML directly, never pydantic); only the contract *validator* uses pydantic, consistent with the repo's existing `schema` CI job.

**Correction this pass produced:** check 3's selftest-presence heuristic greps for the literal `--selftest` and therefore *undercounts* — an enforcer whose mutation harness lives in a separate `scripts/tests/test_*.py` is reported as "no selftest" though it is in fact verified. The INFO is therefore a **lower bound on self-verified enforcers**, not a claim that the other 10 are unverified; the audit's wording and this DR say so rather than overstating. (No BROKEN or schema findings were produced by the pass.)

## Consequences if ratified

`governance/pipeline-contract.yaml` becomes the canonical stage-gate index; `pipeline_contract_audit.py` joins the Level-2 self-run battery (and can be promoted to a blocking CI job if/when owner action C3 restores Actions). The reconciliation of stage ids against the deployed `<audit_trail>` becomes the first execution item. No existing gate, schema, or migration changes; the reproducibility invariant is untouched (the contract is read-only and adds no DB write).

## What would make this ACCEPTED

Owner review of P-1–P-3, and specifically: (a) confirmation (or correction) of the five stage names against the deployed `<audit_trail>` list; (b) a decision on whether the four INCOMPLETE criteria should get enforcers now or stay declared gaps; and (c) an independent adversarial pass per P3 (this section is the author's own pass, which P3 treats as necessary but not sufficient).

## Revision history

- v1 (2026-07-13): initial proposal. Author's adversarial pass applied inline (one correction: the selftest-presence INFO is a lower bound, not a coverage claim). Figures (15/4/0; 10-of-15) are RECOUNTED from `pipeline_contract_audit.py` output on this branch, not recalled.
