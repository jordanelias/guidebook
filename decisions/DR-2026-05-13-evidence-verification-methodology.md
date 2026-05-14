# Decision Record: Evidence Verification Methodology — Existence vs. Claim
**Date:** 2026-05-13
**Status:** ADOPTED 2026-05-13 — owner directive: "whatever is in best interest of project long-term, do" (session 2026-05-13b, after research and DR review). Adoption matches the delegation pattern of DR-2026-05-09.
**Supersedes:** None directly. Refines DR-2026-05-09 (adversarial research) and DR-2026-05-10 (PMP) by clarifying the boundary between existence verification (Phase B) and claim verification (handled jointly by PMP, the 9-step rule, and new per-cell records).
**Author:** Claude (session 2026-05-13b, continuation)
**Self-review caveat:** This DR reviews diagnoses I authored in the immediately prior session. `[SELF-AUTHORED — bias risk]` applies. Independent-reviewer limitations flagged in §Limitations.

---

## 1. Context

Handoff `handoff-2026-05-13b-schema-and-verification-methodology.md` identified that `evidence_sources.verification_status = VERIFIED` in the current pipeline means **existence-verified only** — the source is real, reachable, and the catalog page bears the cited designation. It does **not** mean that the specific numerical or claim-level content the Guidebook attributes to that source has been verified to appear in the source itself.

Concrete findings (cross-checked against `data/guidebook.db` schema this session):

- 410/675 records VERIFIED. Of these:
  - 133 are `co1-manual-pre-pipeline` backfill (unknown verification depth)
  - 137 have `verified_by_tool = NULL` (unknown provenance)
  - 58 are `crossref-doi-backfill` (DOI resolution only)
  - 41 are `publisher-catalog-fetch` (existence only)
  - 41 are other pipeline existence checks
- 0/675 records have claim-level content verification
- 0/675 records have populated `superseded_by_ref_id` (versioning untracked)
- 1/675 has populated `edition` (REF-00178)
- `source_slug_links` columns: `(ref_id, slug, local_ref_id, …)` — explicitly topic-level. No claim-, value-, section-, or population-level fields.
- `evidence_population_match` has both `source_ref` (NOT NULL) and `ref_id` (nullable). The duplicate-column situation is real (separate migration concern).

Standing rule #7 was written to fight the topic-evidence-vs-claim-evidence conflation at the *research* stage. The handoff demonstrates that the same anti-pattern is embedded in the *infrastructure*: VERIFIED + topic-linkage do not equal claim-evidence. Standing rule #10's evidence verification gate currently reads as if `verification_status = VERIFIED` is content-grade. It is not. The gate is weaker than it reads.

---

## 2. Research findings from parallel situations

Surveyed mature evidence-curation methodologies and the empirical literature on citation accuracy.

### 2.1 Mature methodologies treat existence and content as separate phases

- **Cochrane Handbook (current), Chapter 5 §5.5.2.** "Use (at least) two people working independently to extract outcome data from reports of each study, and define in advance the process for resolving disagreements." **Mandatory** under MECIR Box 5.4.a. Screening/inclusion (existence + relevance) is treated as a phase distinct from data extraction (claim-level), with separate forms, training, and quality controls.
- **GRADE Evidence-to-Decision framework** (Murray et al. 2023, *HRB Open Research* 6:50). "Standardized, piloted, dual independent extraction forms" with **10% pilot calibration** before full extraction begins; disagreement resolution protocol defined in advance.
- **JBI scoping review methodology.** Same pattern: dual independent extraction with pre-piloted forms.

The Guidebook's Phase B is the analog of the screening/inclusion phase. **No analog of the data-extraction phase currently exists in the pipeline.** PMP (rule #8) is the partial exception — it performs claim-level work for numerical specs.

### 2.2 Empirical quotation-error base rate in peer-reviewed literature

Three meta-analyses converge on a 15–25% quotation error rate even in peer-reviewed medical literature with formal review processes:

| Study | N (studies / quotations) | Total error rate | Major error rate |
|---|---|---|---|
| Jergas & Baethge 2015 | 28 / ~7,000 | 25.4% (95% CI: 19.5–32.4) | 11.9% |
| Mogull 2017 | 15 / 5,535 | 14.5% | 64.8% of errors were major |
| Cobey et al. 2025 (RIPR) | 46 / 32,000 | 16.9% (95% CI: 14.1–20.0) | 8.0% |
| Smith & Cumberledge 2020 (*Proc. Roy. Soc. A*) | — | 25% | "Completely unsubstantiated" = 33.9% of error subtype |

Cobey et al. 2025 meta-regression shows **no improvement over time** (slope: −0.002 [95% CI: −0.03 to 0.02], p = 0.85). "Major error" is defined as a claim that contradicts the cited article, fails to substantiate, or is unrelated to the cited source's content — exactly the failure mode the handoff identified.

**Implication for the Guidebook.** Peer-reviewed medical literature, with formal peer review, runs at ~15–25% quotation errors. The Guidebook has had no equivalent peer-review pass on its specific value claims. A reasonable prior is that the Guidebook's claim-level error rate is **at or above** the medical-literature rate. The 25–33% "completely unsubstantiated" subtype (Smith & Cumberledge) is the directly analogous failure mode for what would happen if a Phase E synthesis ran on existence-only verification.

### 2.3 Dual-reviewer gap is structural

Cochrane's gold standard requires two human reviewers. The Guidebook is a single-reviewer project. This is a structural gap that **no methodology choice in this DR closes**. Mitigation rather than closure: pre-piloted templates, per-cell verification records, occasional cross-session re-check passes, audit scripts at level 2 enforcement. Honest acknowledgment: the project's evidence quality ceiling sits below the Cochrane bar.

### 2.4 Technical-debt framing

The technical-debt literature counsels: high-impact / low-cost fixes (e.g., versioning backfill from already-fetched catalog pages) executed quickly; high-impact / high-cost fixes (e.g., parallel claim-registry infrastructure with paywall purchases) executed only when the cost is justified against the failure-mode evidence and reversibility properties.

---

## 3. Options considered

**Option A** (handoff §6). Defer content verification entirely to Phase E. Cheap upfront; risks cascading rework if Phase E encounters VERIFIED-but-content-wrong sources mid-rewrite.

**Option B** (handoff §6). Build a parallel `source_claims` registry table now as a new Phase B.8. Front-loads infrastructure. Requires paywalled-document access decisions before Phase E can begin. Risk of duplicating PMP's existing claim-recording role.

**Option C** (this DR). Three-track hybrid that extends existing infrastructure rather than building parallel. Recommended.

---

## 4. Decision

Adopt **Option C**: three parallel tracks, sequenced as below.

### Track 1 — Versioning backfill (quick win)

Scope: populate `evidence_sources.superseded_by_ref_id` and `evidence_sources.edition` from already-fetched publisher catalog pages.

- ≥41 records have publisher-catalog-fetch verification_note content already in the DB; many of these note supersession chains in free text.
- Other Phase B sessions have similar catalog data in `verification_note`.
- Source data → structured columns. No new schema needed; `superseded_by_ref_id` and `edition` already exist.
- Flag edition gaps where the Guidebook cites an older edition than current. Do not auto-invalidate — older editions are sometimes the deliberate regulatory reference (e.g., AS 1428.1:2009 still mandatory in NCC BCA).

Estimated effort: 2–4 sessions for the publisher-catalog-fetch subset; opportunistic backfill thereafter as Phase B continues.

### Track 2 — Promote PMP to the gate it should be

Scope: tighten standing rule #10 so that for numerical-spec citations, synthesis requires evidence of an active PMP walk.

- `spec_value_probes` is functionally a claim registry for numerical claims (it records per-step ref_id, value, population, passes_strict).
- Rule #10 currently admits any VERIFIED+COMPLETE source into synthesis. This admits existence-verified-but-content-unknown sources for numerical-spec claims, which is incoherent with rule #8's PMP requirement.
- Sharpening: for numerical-spec claims specifically, synthesis must additionally reference a `spec_value_probes` row in which the cited value passed strict termination for the target population, OR an explicit logged `pmp_waiver` (e.g., for qualitative claims that nonetheless touch a numerical context).

No new schema. Existing 88-item PMP backlog now legible as content-verification work rather than as a separate workstream.

### Track 3 — Per-cell verification in reasoning docs (during Phase E, not before)

Scope: each row of the 9-step rule's step-3 jurisdiction-comparison table records which source section was actually read to produce the cited value.

New table (extended from initial draft to cover qualitative and definitional claims via `claim_type` enum — per §12.1 adoption answer below):

```sql
CREATE TABLE reasoning_doc_citations (
    citation_id          TEXT PRIMARY KEY,
    reasoning_doc_slug   TEXT NOT NULL,
    parameter            TEXT NOT NULL,
    jurisdiction         TEXT,                 -- NULL for non-jurisdictional qualitative claims
    population           TEXT,
    claim_type           TEXT NOT NULL CHECK(claim_type IN (
        'numerical_spec','jurisdiction_value','qualitative','definitional'
    )),
    claimed_value        TEXT,                 -- required for numerical_spec, jurisdiction_value
    claimed_unit         TEXT,
    claim_text           TEXT,                 -- paraphrase, required for qualitative, definitional
    source_ref_id        TEXT NOT NULL REFERENCES evidence_sources(ref_id),
    source_section       TEXT,
    value_match          TEXT CHECK(value_match IN (
        'EXACT','WITHIN-TOLERANCE','DIFFERENT','NOT-FOUND','PAYWALL','SUPERSEDED'
    )),                                         -- required for numerical_spec, jurisdiction_value
    claim_match          TEXT CHECK(claim_match IN (
        'SUPPORTED','PARTIAL','NOT-FOUND','PAYWALL','CONTRADICTED'
    )),                                         -- required for qualitative, definitional
    verified_at          TEXT NOT NULL,
    verified_by_session  TEXT NOT NULL,
    paywall_purchase_candidate INTEGER DEFAULT 0,   -- 1 = flagged for owner purchase review
    notes                TEXT,
    CHECK (
      (claim_type IN ('numerical_spec','jurisdiction_value') AND claimed_value IS NOT NULL AND value_match IS NOT NULL) OR
      (claim_type IN ('qualitative','definitional') AND claim_text IS NOT NULL AND claim_match IS NOT NULL)
    )
);
CREATE INDEX idx_rdc_slug_param ON reasoning_doc_citations(reasoning_doc_slug, parameter);
CREATE INDEX idx_rdc_ref ON reasoning_doc_citations(source_ref_id);
CREATE INDEX idx_rdc_claim_type ON reasoning_doc_citations(claim_type);
CREATE INDEX idx_rdc_paywall ON reasoning_doc_citations(paywall_purchase_candidate) WHERE paywall_purchase_candidate = 1;
```

Runs during Phase E.1 (per-BPC reasoning draft) as a mandatory recording requirement. **Not** a pre-condition for Phase E start. The per-cell records are produced as a byproduct of the 9-step rule work that Phase E.1 already requires.

`value_match = PAYWALL` / `claim_match = PAYWALL` is a real outcome: where the cited source is paywalled and the value cannot be confirmed via abstracts, government plain-language guides, or compliance commentary, the row records PAYWALL and the synthesis must either downgrade certainty grade or find a non-paywalled corroborating source. `paywall_purchase_candidate = 1` flags the row for periodic owner review of whether the source is high-impact enough to justify purchase.

**Single-BPC pilot mandate (per §12.4 adoption answer).** Before Track 3 scales beyond one BPC, the first BPC under Track 3 runs as a formal pilot: all rows produced under the pilot must be reviewed inline before scaling. This is the structural mitigation for the missing dual-reviewer (see §2.3).

### What this leaves explicitly uncovered

- **Dual independent extraction.** Structurally unavailable; see §2.3. Pilot mandate is the partial mitigation.
- **Retrospective claim verification of 30 retracted Opus syntheses.** Workplan Phase E.2g handles this; not in this DR's scope.
- **Non-Track-3-recordable claims** — claims that don't map to a specific source section (e.g., "consensus across the field is..."). Reasoning docs may still make such statements but they require a `notes` row recording the multiplicity of cited sources, and a synthesis-grade downgrade.

---

## 5. Why not Option B

1. **PMP already implements claim-level verification for numerical specs.** `spec_value_probes` is functionally the claim registry that Option B's `source_claims` would duplicate. Building a parallel table creates reconciliation drift between the two — exactly the pattern the skill-registry deprecation note already flags for `toc-editor`.
2. **The 9-step rule's step-3 jurisdiction comparison is naturally per-cell, not per-source.** Recording verification inside the reasoning doc (Track 3) keeps data with the synthesis it supports. Option B's per-source registration loses the per-(parameter, jurisdiction) granularity that the synthesis actually needs.
3. **Front-loading 675 sources is the wrong unit of work.** Most sources are corroborating, not primary citations for a specific value. The work that matters is per-claim, bounded by BPC count × parameters × jurisdictions, not by source count. Track 3 scopes the work correctly.
4. **Paywall reality.** Track 3's `PAYWALL` outcome is an honest recording mechanism. Option B implicitly requires solving the paywall problem before Phase E can begin, which is not solvable without a budget.
5. **Reversibility.** Track 3 data is monotonically additive. If the project later upgrades to a full `source_claims` table, the per-cell records become input to migration, not waste.

---

## 6. Why not Option A

1. **Versioning backfill is too cheap to defer.** Catalog pages already fetched; not capturing supersession info is wasteful.
2. **Rule #10 incoherence is gate-blocking.** Rule #10 reads as if VERIFIED is content-grade. Under Option A, Phase E synthesis runs through that broken gate. The rule must be sharpened (Track 2) before Phase E begins regardless.
3. **PMP backlog (88 items) is partially the deferred work already.** Treating PMP as the gate (Track 2) reframes existing backlog as content-verification, rather than treating it as a separate Phase.

---

## 7. Workplan impact

Operative workplan (`audits/bpc-rewrite-workplan-2026-05-11.md`) Phase B scope is **unchanged**: existence verification remains Phase B's primary objective. Tracks 1, 2, 3 are amendments:

- **Track 1** runs alongside Phase B (no sequencing change). May be assigned to Phase B as a subtask "B.x — versioning backfill."
- **Track 2** is a rule sharpening + audit hook; no Phase change beyond enforcement.
- **Track 3** binds into Phase E.1's reasoning-document workflow; modifies Phase E.1 specification but does **not** gate Phase E start beyond what existing rule #6 (strict sequential B before E for formally-linked sources) already requires.

Aggregate ~2300-hour estimate unchanged. The work that would have been Phase B.8 in Option B is reframed as already-in-scope (PMP backlog) or moved into Phase E.1 (per-cell records). Some Phase E.1 sessions become slightly heavier; some workplan-level effort moves from "Phase B.8" to "Phase E.1 recording overhead."

---

## 8. Standing rule #10 amendment

Adopt the following replacement language for standing rule #10 (changes in PI v10.9 to follow this DR's adoption, queued via `decisions/PI-update-needed.md` pattern):

> **10. Evidence verification gate for synthesis.** No BPC synthesis claim may cite a source with `metadata_quality = AUTHOR-TITLE-ONLY` or `verification_status = NULL`. Required minimum: `metadata_quality = COMPLETE` AND `verification_status ∈ {VERIFIED, UNVERIFIED-1}`.
>
> **Note on the existence-vs-content distinction.** `verification_status = VERIFIED` confirms source existence and identification, not content. Additional content-verification requirements apply by claim type:
>
> 1. **For numerical-spec claims**: the synthesis must additionally cite a `spec_value_probes` walk in which the cited value passed strict termination for the target population (rule #8), or an explicit `pmp_waiver` is logged with rationale.
> 2. **For jurisdiction-comparison cells in 9-step reasoning docs** (rule #9 step 3): each (parameter, jurisdiction) cell must have a corresponding `reasoning_doc_citations` row with `value_match ∈ {EXACT, WITHIN-TOLERANCE}` from a documented re-read of the specific code section. `value_match = PAYWALL` requires either a downgraded synthesis grade or a non-paywalled corroborating source.
> 3. **For qualitative claims**: no automated gate exists yet. Synthesis must cite source section and a paraphrased claim summary in the reasoning doc body. Tracked gap pending future DR.
>
> Sources with `verification_status ∈ {UNVERIFIED-CLOSED, CLOSED-DELETED}` remain excluded from all synthesis.

---

## 9. Implementation plan (next session)

Sequenced for the next session under operative workplan §Phase A/B parallel-track:

1. **Migration 010** (handoff §3). Independent of this DR. FK fixes on 4 tables / 782 rows, single transaction, `PRAGMA foreign_keys=OFF` at start. user_version 9 → 10. Includes the PMP-A02-001-S2 ref_id fix and the 5 epm ref_id NULL backfills.
2. **Migration 011** (this DR). `CREATE TABLE reasoning_doc_citations` + indexes. Standalone migration; can ship immediately after 010. user_version 10 → 11.
3. **PI v10.9** drafted in repo (`governance/project-instructions-v10_9.md`). Sharpens rule #10 per §8 above. Adds `decisions/PI-update-needed.md` update entry (per existing pattern).
4. **Track 1 first pass**: backfill `superseded_by_ref_id` and `edition` on the ≥41 publisher-catalog-fetch records from session 2026-05-13a. Pull supersession info from existing verification_note text where present; flag records that need a fresh fetch.
5. **Audit script stubs** (level 2 enforcement, not yet promoted to hooks):
   - `scripts/audit/reasoning_doc_citations_audit.py` — checks rule #10's new sub-requirements.
   - Update `scripts/audit/pmp_audit.py` (rule #8) to additionally flag synthesis claims that fail rule #10's new numerical-spec sub-requirement.
6. **Research log entry** for the parallel-situation research conducted in this session (Cochrane, GRADE, quotation-error meta-analyses). Per standing rule #4.
7. **Session record** for 2026-05-13b (the handoff session) — formal commit with `session-consolidator` skill.

---

## 10. Reversibility analysis

| Track | If we later realize Option B was right | If we later realize Option A was right |
|---|---|---|
| 1 (versioning backfill) | Data is reusable in any registry design. No rework. | No-op; data is correct regardless. |
| 2 (PMP as gate) | Rule #10 amendment is reversible by future PI revision. PMP walks already done remain valuable. | Slight overhead in Phase E for PMP-gated checks. Walks remain valuable. |
| 3 (per-cell records) | `reasoning_doc_citations` rows become input to a future `source_claims` migration. No data lost. | Continue using as-is; per-cell records are the content-verification record. |

Option C is **strictly more reversible** than Option B and **strictly more cautious** than Option A.

---

## 11. Limitations (independent reviewer flag)

`[SELF-AUTHORED — bias risk]` applies. An independent reviewer would likely add:

1. **The 15–25% quotation error rate is from medical literature, not building codes.** Base rates in standards-citation contexts are unknown and could be higher (technical numerical precision, less professional citation training) or lower (more prescriptive citation styles). The "reasonable prior" claim in §2.2 carries this uncertainty. `[CONFIDENCE: medium — base rate not domain-matched]`
2. **The handoff's diagnosis is my own prior output.** I'm validating it against schema this session (confirmed) but the framing remains author-aligned. A fresh reviewer would likely push harder on whether "PMP already covers numerical claims" is true in practice or just in theory — most existing BPCs don't have PMP walks yet (88 backlog).
3. **Track 3 scope is potentially too narrow.** Recording only the lowest-barrier-code cells (rule #9 step 4) rather than all (parameter × jurisdiction) cells (step 3) would shrink the work but lose the audit trail for the jurisdiction comparison. A reviewer may prefer the broader scope; this DR is silent on which.
4. **Qualitative claims are deferred as a "tracked gap."** A reviewer concerned about long-term integrity may push back: qualitative claims are roughly half the Guidebook content. Deferring them indefinitely is a substantial concession.
5. **No empirical pilot.** Cochrane and GRADE mandate a 10% pilot before extraction begins. This DR does not require a pilot for Track 3's per-cell recording. A reviewer would likely add: "first 1 BPC under Track 3 = formal pilot with explicit review of the reasoning_doc_citations rows produced."

---

## 12. Open question adoption answers (owner delegation: "do whatever is in best interest of project long-term")

1. **Non-numerical qualitative claims** → **Track 3 schema extended** (see §4 / Track 3 above). Single table with `claim_type` enum covers numerical, jurisdictional, qualitative, and definitional. No separate Track 4. Forward-compatible with future split if needed. Rationale: qualitative claims are ~half of BPC content; deferring them indefinitely is not in long-term integrity interest. Extension cost is one extra enum value at table-creation time, not a new infrastructure layer.

2. **Paywall handling** → **PAYWALL accepted as real outcome**, plus `paywall_purchase_candidate INTEGER DEFAULT 0` flag for owner review. Owner can periodically query `SELECT source_ref_id, COUNT(*) FROM reasoning_doc_citations WHERE paywall_purchase_candidate=1 GROUP BY source_ref_id ORDER BY 2 DESC` to surface the highest-leverage purchase candidates. No upfront budget decision required from this DR.

3. **Track 3 scope** → **All (parameter × jurisdiction) cells**, not just lowest-barrier-code. Rationale: the 9-step rule step 3 explicitly requires every surveyed jurisdiction in the comparison table. Recording only the chosen-lowest cell leaves the comparison rows unverified, defeating the audit-trail purpose. The narrower scope was cost-saving, not integrity-driven.

4. **Pilot requirement** → **Yes, mandated** (see §4 / Track 3 above). First BPC under Track 3 runs as a formal pilot with full inline review before scaling. This is the structural mitigation for the unavailable dual-reviewer (§2.3). The cost is one BPC's worth of slow careful work — cheap insurance.

These answers are locked into the schema and the standing-rule sharpening (§8) as adopted.

---

## 13. Adoption criteria

- [x] Owner reviews and accepts §4 (Decision) and §8 (rule #10 amendment language). *Adopted via owner directive "do whatever is in best interest of project long-term" — same delegation pattern as DR-2026-05-09.*
- [x] Owner answers §12 open questions or explicitly defers them. *Per same delegation, answers in §12 adopted as part of this DR.*
- [x] DR moved to ADOPTED status with date and session reference. *See header.*
- [ ] PI v10.9 drafted in `governance/`. *Action item this session.*
- [ ] `decisions/PI-update-needed.md` updated with v10.9 deployment instructions. *Action item this session.*

---

**End of DR draft.**
