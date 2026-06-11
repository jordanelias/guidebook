# DR-2026-06-10 — E.2g Reverification Scope (full re-synthesis; prior text is a claim inventory, not salvageable prose)

**Status:** RATIFIED 2026-06-10 (owner directive: "proceed with recommendations with care", ratifying Stage 4.3 plan §9 D-4.3-B).
**Authored:** `session_2026-06-10-stage4-3-ratification`
**Doctrine SHA at authorship:** `3da73bd` (`governance/mission-and-epistemics.md`)
**Relates to:** PI v10.14 standing rules #6, #7, #8, #10; BPC-rewrite workplan Phase E.2g; the 68 BPCs at `bpc_metadata.evidence_state='RETRACTED-PRE-REHAB'`; the deferred decision the master workplan surfaces at Stage 4.3.

---

## Context

68 BPCs carry the `PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION` banner and `evidence_state='RETRACTED-PRE-REHAB'` (Phase B.0, Decision 5). Their original synthesis text remains in the files as historical record but is barred from downstream citation. Phase E.2g overwrites that text with rehabilitated synthesis. The open question (deferred by the master workplan to Stage 4.3): when E.2g runs, may the prior synthesis prose be *salvaged* — edited forward — or must each BPC be re-synthesized from the rehabilitated evidence base?

## Decision

1. **Full re-synthesis.** Every RETRACTED-PRE-REHAB BPC is re-synthesized from its rehabilitated evidence inventory through the Phase E pipeline (rules #7/#8/#9/#10). The synthesis sections are authored fresh, not edited forward from the retracted prose.
2. **Prior text is admissible only as a claim inventory.** The retracted synthesis may be read to enumerate the *assertions* it made — a checklist of claims to verify or discard under the verification gates — and for nothing else. It is never carried forward as prose, partial paragraphs, or phrasing.
3. **Consultation is bias-tagged.** Any consultation of prior retracted text during re-synthesis is logged `[SELF-AUTHORED — bias risk]` per `userPreferences <layering>` self-review, and the re-synthesis must surface at least one assertion the prior text made that the rehabilitated evidence does *not* support (the prior round's failure mode made visible).

## Rationale

Under rule #10, the cost of a rehabilitated BPC is **verification, not drafting** — every jurisdiction cell needs a `reasoning_doc_citations` re-read, every numerical value a PMP walk, every claim an adversarial pass. Salvaging prior prose saves only the drafting minutes, which are a small fraction of per-BPC cost, while importing a large, well-documented risk: anchoring on assertions that were retracted precisely because they were unreliable. In a single-reviewer methodology (the documented ceiling), anchor bias is the dominant threat to verification integrity. Discarding the prose and keeping only the claim inventory captures the genuine value of prior work (knowing what was claimed) at the lowest bias cost.

## Consequences

- Phase E.2g per-BPC effort is sized as fresh synthesis, not as edit-forward (Stage 4.3 plan §10 sizing already assumes this).
- The retracted prose remains in the file's history for provenance but is not a source for the rehabilitated sections.
- The "at least one unsupported prior assertion" requirement is a per-BPC E.2g checklist item, spot-checked in the §7 battery.

## Verification

This DR records an owner ratification; it makes no DB or evidence claim. Compliance with rule #11 is the attestation `attestations/decisions_DR-2026-06-10-e2g-reverification-scope.json`.
