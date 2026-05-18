# Decision Record: Statutory Metadata Completeness — `COMPLETE-STATUTORY`
**Date:** 2026-05-18
**Status:** ADOPTED 2026-05-18 — owner directive 2026-05-18 in pilot session resumption: "A" (path A — new metadata_quality value preserving statutory-vs-academic distinction).
**Supersedes:** None. Refines DR-2026-05-13 §3 evidence verification gate by recognizing that statutory documents and academic publications carry structurally different metadata fields, and that the gate's `metadata_quality='COMPLETE'` predicate was implicitly academic-only.
**Author:** Claude (session 2026-05-17-pilot-pass-3-blocker-resolution)
**Self-review caveat:** This DR resolves a blocker surfaced during Pass 3 of the Phase E.1 pilot — the same session that authored the steps being verified. `[SELF-AUTHORED — bias risk]` applies. The bias direction is toward criteria broad enough to unblock the pilot. Independent-reviewer counterclaim in §Limitations.

---

## 1. Context

Phase E.1 pilot Pass 3 (rule #10 reasoning-doc-citations) requires opening cited sources at cited sections and confirming `value_match` / `claim_match`. Pre-check filter per rule #10: `metadata_quality='COMPLETE' AND verification_status IN ('VERIFIED','UNVERIFIED-1')`.

Of 33 sources linked to slug `room-acoustic-performance`, 13 fail the pre-check — every one a statutory or guideline document (ANSI/ASA S12.60-2010, BB93:2015, DIN 18041:2016, UNI 11532-2:2020, PAS 6463:2022, AS/NZS 2107:2016, GB 50118-2010, NS 8175:2019, etc.). All 13 are tagged `metadata_quality='AUTHOR-TITLE-ONLY'` despite carrying issuing body, year, jurisdiction, title, and (for most) standard number or publisher catalog URL.

Inspection of representative rows (REF-00329 DIN 18041:2016, REF-00568 PAS 6463:2022) shows publisher, edition, DOI, standard_number, verification_note, and verified_by_tool already populated — yet the rows remain AUTHOR-TITLE-ONLY. The label is reading these as incomplete *academic* metadata. They are complete *statutory* metadata.

The conflation is systemic, not local: ~290 rows across `source_type IN ('standard','guideline')` are similarly mislabeled.

## 2. Diagnosis

Statutory codes and academic publications evaluate differently:

| Field | Academic | Statutory |
|---|---|---|
| Authors | Named individuals (required) | Issuing body (e.g., ANSI/ASA, DIN, BSI) — `author_display` carries this |
| Title | Article/book title | Standard title (often bilingual) |
| Publisher | Journal/publisher | Standards body, often same as author |
| Year | Publication year | Edition year |
| Identifier | DOI / PMID | Standard number (DIN 18041:2016, PAS 6463:2022) |
| Pagination | Page range | Clause / section / annex reference |

Academic-COMPLETE requires DOI or PMID, named authors, journal, page range. Statutory documents legitimately lack all four — they are complete without them. The current `metadata_quality` taxonomy has no value to represent this; AUTHOR-TITLE-ONLY is the closest existing label and has been applied as a fallback, with the side-effect of making every statutory code rule-#10-ineligible.

The pilot surfaced the conflation; the DR fixes it.

## 3. Decision

Introduce `metadata_quality='COMPLETE-STATUTORY'` as a peer value to `COMPLETE`. Both values clear the rule #10 existence gate. They remain queryably distinct so academic and statutory citations can be analyzed separately in audits.

### 3.1 Criteria for `COMPLETE-STATUTORY`

A row qualifies if **all** of:

1. `source_type IN ('standard','guideline')`
2. `author_display IS NOT NULL AND author_display <> ''` (issuing body)
3. `pub_title IS NOT NULL AND pub_title <> ''`
4. `pub_year IS NOT NULL`
5. `jurisdiction IS NOT NULL AND jurisdiction <> ''`
6. At least one of: `standard_number IS NOT NULL AND standard_number <> ''` OR `publisher IS NOT NULL AND publisher <> ''`

Criterion 6 admits both international standards (which carry standard numbers; publisher field is redundant with issuer) and national informal guidelines (which carry an authoritative publisher but may lack a formal standard number).

`source_type='report'` is **excluded**: inspection of the 181 `report` rows tagged AUTHOR-TITLE-ONLY shows many are journal articles or grey literature misclassified at ingest. Those rows route to a separate misclassification audit, not to statutory promotion.

### 3.2 Eligibility gate update

Rule #10's existence gate becomes:

> `metadata_quality IN ('COMPLETE','COMPLETE-STATUTORY') AND verification_status IN ('VERIFIED','UNVERIFIED-1')`

`UNVERIFIED-CLOSED` and `CLOSED-DELETED` remain excluded; the verification_status axis is orthogonal to the metadata_quality axis.

### 3.3 Verification semantics for statutory sources

Same content-verification requirements apply at Pass 3 (rule #10 sub-rules 1/2/3). A `reasoning_doc_citations` row citing a statutory source must still record `value_match` or `claim_match` against the actual cited clause. COMPLETE-STATUTORY clears the *existence* gate; it does not certify that the cited clause contains the claimed value. Pass 3 still requires the clause text.

For paywalled statutory codes (DIN, UNI, AS/NZS, BSI, ANSI), the existing PAYWALL handling (rule #10 sub-rule 2; `paywall_purchase_candidate=1`) applies unchanged. The DR does not waive paywall verification; it only stops mislabeling complete statutory metadata as incomplete.

### 3.4 Migration

Bulk-promote qualifying rows from `AUTHOR-TITLE-ONLY` to `COMPLETE-STATUTORY` via forward-only data migration tracked in `data_migrations`. Preserve original `metadata_quality` history in `verification_note` (append, not overwrite) so the change is reversible-by-audit.

Estimated population: ~140 standards + ~91 guidelines = ~231 rows promote. RAP slug specifically: 11 of 13 ineligible sources clear; REF-00569 (misclassified report — leave for audit) and REF-00575 (missing pub_year — backfill separately) remain.

### 3.5 Audit-script update

`scripts/audit_evidence_metadata.py` updated to:
- Recognize `COMPLETE-STATUTORY` as gate-passing.
- Report academic-COMPLETE and statutory-COMPLETE counts separately.
- Continue to flag AUTHOR-TITLE-ONLY rows post-promotion (residue indicates non-statutory rows still needing genuine completion).

`scripts/audit/reasoning_doc_citations_audit.py` and `scripts/audit/pmp_audit.py` updated identically for their pre-check predicates.

### 3.6 PI clause

PI v10.11 rule #10 text reads "Required minimum: `metadata_quality = COMPLETE` ...". Bump to v10.12 (or amend in place):

> Required minimum: `metadata_quality IN ('COMPLETE','COMPLETE-STATUTORY')` AND `verification_status ∈ {VERIFIED, UNVERIFIED-1}`.

Queue via `decisions/PI-update-needed.md` per architecture v2.3 `<migration_and_growth>`. PI is not API-writable; owner pastes the new clause into claude.ai project settings to ratify.

## 4. Limitations

- **`[SELF-AUTHORED — bias risk]`** — This DR was authored mid-pilot to unblock the pilot. A reviewer not invested in pilot completion might prefer Path B (treat statutory rows as `COMPLETE`, no new value), arguing that one additional taxonomy value adds query complexity for marginal analytic gain. Counterclaim: the distinction is real evidence about source type; preserving it queryably is long-term hygiene over short-term economy.
- **The taxonomy still has a `report` problem.** 181 rows mislabeled at ingest as `report` when many are journal articles or grey lit. Out of scope for this DR; routes to a separate `source_type` audit. Until done, ~30 sources that should be journal_article-eligible remain ineligible.
- **Single-reviewer methodology ceiling** per DR-2026-05-13 §2.1 unchanged.
- **The Bettarello (REF-00561) precedent** showed that even VERIFIED + COMPLETE academic metadata can be wrong (DOI mismatch caught by rule #10 sub-rule 2). Statutory rows promoted to COMPLETE-STATUTORY carry the same residual risk; promotion does not pre-empt content review.

## 5. Implementation order

1. This DR ships.
2. Migration `data_20260518_promote_statutory_metadata.sql` applied; reproducibility-verified.
3. Audit scripts updated; spot-checked against promoted population.
4. `decisions/PI-update-needed.md` updated with the rule #10 text amendment.
5. Pass 3 of pilot resumes against the larger eligible-source pool.

## 6. References

- DR-2026-05-13 evidence verification methodology (parent gate definition)
- PI v10.11 standing rule #10
- Architecture guidebook v2.3 `<data_layer_pattern>` (forward-only migration discipline)
- Architecture guidebook v2.3 `<migration_and_growth>` (PI-update queue mechanism)
- Phase E.1 pilot session 2026-05-17 (blocker discovery)
- `references/bpc-reasoning/room-acoustic-performance.md` (pilot doc; Pass 3 target)
