---
name: reasoning-doc-citations
title: Reasoning Document Citations — Claim-Level Verification Protocol
purpose: Verify that a specific cited source actually contains the value or claim a BPC reasoning document attributes to it, distinct from existence-verifying that the source is real
status: active
adopted: 2026-05-13
decision_record: decisions/DR-2026-05-13-evidence-verification-methodology.md
governs: All citations in `references/bpc-reasoning/<slug>.md` that support jurisdiction-comparison cells (rule #9 step 3), qualitative claims, or definitional claims
enforcement: Level 2 (audit query at scripts/audit/reasoning_doc_citations_audit.py)
companion: adversarial-research (claim validation across the literature); progressive-measurement (numerical-value boundary probing)
---

# Skill: Reasoning Document Citations

## When to invoke

Trigger this skill during Phase E.1 BPC reasoning-document authoring whenever a citation is being made to support one of:

- A **jurisdiction-comparison cell** (rule #9 step 3) — a specific value attributed to a specific jurisdiction at the parameter's worst-case point
- A **qualitative claim** — a non-numerical assertion about user need, design intent, regulatory posture, clinical rationale, etc., where the reasoning doc attributes the claim to a specific source
- A **definitional claim** — a term or concept whose meaning the reasoning doc attributes to a specific source

Also trigger during:
- Phase E.2g rehabilitation of BPCs carrying `synthesis_validity: PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION`
- Audit-phase re-evaluation of an existing reasoning doc when a cited source has been superseded by a new edition

Do NOT invoke for:
- **Numerical specification values** asserted in a BPC item (mm, s, NC, lux, °C, %, N, LRV, dB(A), NRC, ratio, count) — these route to `progressive-measurement` per rule #8 sub-rule 1. A `reasoning_doc_citations` row of `claim_type='numerical_spec'` is permitted by schema and may corroborate a PMP walk, but the PMP `spec_value_probes` walk is the primary evidence path; this skill does not substitute for it.
- Existence-level source verification (catalog reachable, DOI resolves, designation exists) — that's the Phase B `verification_status` gate, populated by the `citation-miner` and ingestion pipelines.
- Claims where the underlying validity-for-population question has not yet cleared `adversarial-research`. This skill verifies that the source contains the claim; it does NOT verify that the claim is correct.

## What this skill does NOT solve

Read this first. Do not skip:

- **Cannot detect fabricated citations.** A row with `value_match='EXACT'` and `source_section='p. 47'` is trustworthy only to the extent the reviewer actually opened p. 47. Audit C5 (passes without `source_section`) flags one tier of carelessness; reviewer spot-check is the truth-source.
- **Cannot verify content behind a paywall the project has not purchased.** PAYWALL is a status, not a verification. PAYWALL requires either (a) downgrade of the citation, (b) corroboration from a non-paywalled source, or (c) queueing the source for purchase via the `paywall_purchase_candidate` flag.
- **Single-reviewer methodology has a documented ceiling.** Cochrane gold-standard dual-reviewer extraction (DR-2026-05-13 §2.1) is structurally unavailable here. The Track 3 pilot mandate (PI rule #10) — first BPC in Phase E.1 runs as a formal pilot with inline review before scaling — is the partial mitigation, not a fix.
- **Cannot rescue an ineligible source.** If the source has `metadata_quality='AUTHOR-TITLE-ONLY'` or `verification_status` is NULL/UNVERIFIED-CLOSED/CLOSED-DELETED, the row cannot be created. Pre-check fails. Source must be upgraded first (route to `citation-miner` / Phase B).
- **CONTRADICTED is not a row to file and move on.** A `claim_match='CONTRADICTED'` row invalidates the BPC claim. The reasoning doc must be rewritten or the claim removed before the BPC ships.

## Required inputs (per citation)

| Input | Source | Notes |
|---|---|---|
| `reasoning_doc_slug` | reasoning doc filename | matches `references/bpc-reasoning/<slug>.md`; the BPC's slug |
| `parameter` | reasoning doc | the parameter name as declared in step 1 of the 9-step rule |
| `jurisdiction` | reasoning doc, step 3 row | required if `claim_type='jurisdiction_value'`; else NULL |
| `population` | reasoning doc, step 2 | per-population worst-case user statement; nullable for definitional claims that are population-agnostic |
| `claim_type` | author decision | one of `jurisdiction_value`, `qualitative`, `definitional` (also `numerical_spec` if corroborating PMP — uncommon) |
| `claimed_value` + `claimed_unit` | reasoning doc | required for `jurisdiction_value` and `numerical_spec`; the value as the doc states it, in native units |
| `claim_text` | reasoning doc | required for `qualitative` and `definitional`; the doc's assertion verbatim or near-verbatim |
| `source_ref_id` | `evidence_sources.ref_id` | must already exist and clear the existence gate (see pre-check below) |
| `source_section` | reviewer | page number, section number, paragraph anchor — wherever the value/claim lives in the source |

## Pre-check (run before any per-citation work)

The cited source must clear PI rule #10's existence gate before claim-level work begins:

```sql
SELECT metadata_quality, verification_status
FROM evidence_sources
WHERE ref_id = :source_ref_id;
```

Required: `metadata_quality = 'COMPLETE'` AND `verification_status IN ('VERIFIED', 'UNVERIFIED-1')`.

If the source fails the gate:
- Do NOT create a `reasoning_doc_citations` row.
- Route to `citation-miner` / Phase B to upgrade the source.
- Log `[GAP: <ref_id> ineligible for synthesis — <metadata_quality>/<verification_status>]` in the session record.
- The reasoning doc cannot cite this source until upgraded. Substitute another source or remove the claim.

## Algorithm

```
for each citation in reasoning_doc:
  # 0. PRE-CHECK
  if not pre_check(citation.source_ref_id):
    log_ineligible(citation)
    skip

  # 1. OPEN SOURCE AT CITED SECTION
  content ← fetch_section(citation.source_ref_id, citation.source_section)
  if content.is_paywalled:
    handle_paywall(citation)
    continue

  # 2. CLASSIFY BY CLAIM TYPE
  if citation.claim_type in ('jurisdiction_value', 'numerical_spec'):
    value_match ← compare_value(content, citation.claimed_value, citation.claimed_unit)
    claim_match ← NULL
  else:  # qualitative, definitional
    claim_match ← compare_claim(content, citation.claim_text)
    value_match ← NULL

  # 3. INSERT ROW
  insert_rdc_row(citation, value_match, claim_match, verified_at=now(), verified_by_session=session_id)

  # 4. ACT ON OUTCOME
  if value_match == 'DIFFERENT' or claim_match == 'CONTRADICTED':
    flag_for_doc_revision(citation)        # BPC claim must be removed or rewritten
  if value_match == 'PAYWALL' or claim_match == 'PAYWALL':
    record_purchase_candidate(citation)    # set paywall_purchase_candidate=1
    require_non_paywalled_corroboration_or_downgrade(citation)
  if value_match == 'NOT-FOUND' or claim_match == 'NOT-FOUND':
    flag_for_section_review(citation)      # cited section may be wrong; reviewer rechecks
```

## value_match definition (jurisdiction_value, numerical_spec)

The reasoning doc states a value (e.g., "Germany: 1500 mm clear width at corridor pinch point"). The reviewer opens the cited German code at the cited section and reads what's actually there.

| value_match | When to assign |
|---|---|
| `EXACT` | Cited section contains the same value in the same units (or a trivially-convertible unit) at the same worst-case point |
| `WITHIN-TOLERANCE` | Cited section contains a value within ±tolerance(U) of the claimed value at the same worst-case point. Tolerance is unit-dependent: ±1 mm for mm, ±0.01 s for s, ±1 NC, ±5 lux, ±0.5 °C, ±1 %, ±1 N, ±2 LRV points, ±1 dB(A), ±0.05 NRC. Tighter tolerance overrides this default when the parameter's regulatory context demands it. |
| `DIFFERENT` | Cited section contains a different value at the same worst-case point. **The BPC claim is invalid.** |
| `NOT-FOUND` | Cited section does not address the parameter at the worst-case point. Either the section reference is wrong (reviewer rechecks) or the source does not actually cover this parameter (claim re-sourced or removed). |
| `PAYWALL` | Cited section is behind a paywall the project has not purchased. Row recorded; `paywall_purchase_candidate=1`; see PAYWALL handling below. |
| `SUPERSEDED` | Cited edition has been superseded by a newer edition (`evidence_sources.superseded_by_ref_id` populated). Re-cite the newer edition and re-verify. |

The worst-case point must match the parameter as declared. A code that specifies "1200 mm normally; 1500 mm at corridor pinch points" cited as "Germany: 1500 mm" is `EXACT` if the cited section is the pinch-point clause, but `DIFFERENT` if the cited section is the general clause.

## claim_match definition (qualitative, definitional)

The reasoning doc states a non-numerical assertion (e.g., "user control is the primary design variable for sensory environments"). The reviewer opens the cited source at the cited section and reads what's actually there.

| claim_match | When to assign |
|---|---|
| `SUPPORTED` | Cited section asserts the claim in substantively the same form. Wording may differ; the proposition is the same. |
| `PARTIAL` | Cited section asserts a weaker, narrower, or context-bounded version of the claim. The BPC claim should be downgraded to match the source's actual scope, OR additional corroborating sources are needed for the full claim. |
| `NOT-FOUND` | Cited section does not address the claim. Reviewer rechecks the section reference; if still not found, the claim must be re-sourced. |
| `CONTRADICTED` | Cited section asserts the opposite or a substantively-incompatible position. **The BPC claim is invalid.** Reasoning doc must be revised; if no other source supports the claim, the claim is removed. |
| `PAYWALL` | Cited section is behind a paywall. Row recorded; `paywall_purchase_candidate=1`; see PAYWALL handling below. |

## PAYWALL handling

Per PI rule #10 sub-rule 2: "PAYWALL requires downgrade or non-paywalled corroboration."

Operationally, this means one of three paths after a PAYWALL row is recorded:

1. **Downgrade.** The reasoning doc citation is rewritten to remove the specific value/claim attribution. The source can still be cited as topical evidence but cannot be used to ground a jurisdiction-comparison cell or a synthesized assertion. The cell or assertion in the reasoning doc is either softened to match what the project can verify, or removed.
2. **Non-paywalled corroboration.** A separate, accessible source is located that contains the same value/claim. A new `reasoning_doc_citations` row is created against the accessible source; the PAYWALL row remains as supporting context but is not load-bearing.
3. **Queue for purchase.** Set `paywall_purchase_candidate=1`. The audit script aggregates these for owner review. Until purchased and re-verified, the citation cannot bear synthesis weight; treat as path 1 in the interim.

Path 1 and path 3 are not exclusive — record the candidate and downgrade until the candidate is acted on.

## Required DB writes

Per citation:

```sql
INSERT INTO reasoning_doc_citations (
  citation_id, reasoning_doc_slug, parameter, jurisdiction, population,
  claim_type, claimed_value, claimed_unit, claim_text,
  source_ref_id, source_section,
  value_match, claim_match,
  verified_at, verified_by_session,
  paywall_purchase_candidate, notes
) VALUES (
  :citation_id, :slug, :parameter, :jurisdiction, :population,
  :claim_type, :claimed_value, :claimed_unit, :claim_text,
  :source_ref_id, :source_section,
  :value_match, :claim_match,
  :verified_at, :session_id,
  :paywall_flag, :notes
);
```

`citation_id` convention: `RDC-<slug>-<parameter-fragment>-<NNN>` where NNN is a per-doc sequence. Uniqueness is enforced by PRIMARY KEY; collision means re-verification of an existing row — UPDATE instead of INSERT, preserving the original `verified_at` in `notes` if material.

Schema check constraints enforce:
- `claim_type IN ('numerical_spec','jurisdiction_value')` requires `claimed_value IS NOT NULL` AND `value_match IS NOT NULL`
- `claim_type IN ('qualitative','definitional')` requires `claim_text IS NOT NULL` AND `claim_match IS NOT NULL`
- `source_ref_id` FK to `evidence_sources(ref_id)`

No write to `items` is required by this skill. Reasoning docs are markdown in `references/bpc-reasoning/` and are not row-keyed in `items`.

## Integration with sibling skills

| Question | Skill | Output |
|---|---|---|
| Is the claim itself correct for this population? | `adversarial-research` | `named_dissenter`, `confidence_interval`, `falsification_condition` |
| At what value does the empirical evidence stop validating a numerical claim? | `progressive-measurement` | `pmp_empirical_ceiling`, `pmp_gap_signed` |
| Does the specific cited source contain the value or claim attributed to it? | **this skill** | `value_match`, `claim_match` |

Order within Phase E.1 reasoning-doc authoring:
1. `adversarial-research` clears the underlying claim across the literature.
2. For numerical specs, `progressive-measurement` probes the value boundary.
3. For each citation in the reasoning doc, this skill confirms the specific source contains what the doc says it contains.

Skipping step 3 means the BPC ships with citations that may or may not say what the doc claims they say. Rule #10 makes this a synthesis-blocking gate.

## Multilingual scope

For non-English sources, claim and value extraction runs in the source's native language. Translation to English is for the reasoning doc's reader, not for verification.

When the BPC reasoning doc is in English but cites a non-English source:
- The reviewer reads the cited section in the source language.
- `claim_text` in the row may be a literal translation; `notes` records the original-language phrasing if material differences exist.
- For `value_match`, units may need conversion (e.g., a Japanese code citing "75 cm" cited in the BPC as "750 mm" is `EXACT` — record the conversion in `notes`).
- For the 5 languages flagged `[UNVERIFIED-TERMS]` in PI rule #9 (AR, HI, ID, SW, BN), citations against sources in these languages should additionally cite the relevant keyword compendium row from `references/keyword-compendiums/<lang>.md` in `notes`; if compendium not yet validated, flag the row `notes='compendium-pending'` and queue for re-verification once Phase A.11 completes.

## Audit query

`scripts/audit/reasoning_doc_citations_audit.py` (level 2). Flags rows that violate the rule #10 sub-rules 2 and 3 contract.

Documented checks (canonical list lives in the audit script docstring; reproduced here for skill self-containment):
- **C1.** Rows with `value_match='NOT-FOUND'` or `claim_match='NOT-FOUND'` — claim was sought but not located.
- **C2.** Rows with `value_match='CONTRADICTED'` (schema-disallowed but defensive) or `claim_match='CONTRADICTED'` — synthesis invalid; must be addressed pre-ship.
- **C3.** PAYWALL rows without downgrade note in `notes`.
- **C4.** Rows whose `source_ref_id` points to an `evidence_sources` row failing rule #10's existence gate.
- **C5.** VERIFIED-content rows with empty `source_section`.
- **C6.** `paywall_purchase_candidate=1` aggregated by `source_ref_id` for owner review.
- **C7.** `claim_type` distribution sanity check.
- **C8.** Slug-side coverage gap (rows-vs-docs cross-check; limited from DB alone).

Run before session close:

```bash
python3 scripts/audit/reasoning_doc_citations_audit.py
```

Exit 0 = clean. Exit 1 = deficient rows present.

## Detection question (mandatory before declaring a citation verified)

> **"At this cited section, does the source state this value or claim, or does it speak to the topic?"**

If the answer is "speaks to the topic," `value_match` or `claim_match` MUST be `NOT-FOUND`, regardless of how relevant the section is. This is the topic-vs-claim conflation guard from PI rule #7, applied at the citation level. DR-2026-05-13 §1 demonstrates that the same anti-pattern was previously embedded in infrastructure (VERIFIED + topic-linkage being mistaken for content-grade evidence); this skill exists to keep it out of the reasoning layer.

## Worked example — generic structure

Reasoning doc `references/bpc-reasoning/<slug>.md` declares parameter P with worst-case point W. Step 3 of the 9-step rule produces a jurisdiction-comparison table including:

| Jurisdiction | Value at W | Source | Section |
|---|---|---|---|
| Jurisdiction A | 1500 mm | REF-NNNNN | §X.Y.Z |
| Jurisdiction B | 1200 mm | REF-MMMMM | §A.B.C |

For row 1:
- Pre-check: `evidence_sources` shows REF-NNNNN with `metadata_quality='COMPLETE'`, `verification_status='VERIFIED'`. Gate passes.
- Reviewer opens REF-NNNNN at §X.Y.Z. Section text states "where corridor narrows between fixed obstructions, minimum 1500 mm". Worst-case point W is corridor-pinch-point. Match: `EXACT`.
- INSERT row with `claim_type='jurisdiction_value'`, `claimed_value='1500'`, `claimed_unit='mm'`, `value_match='EXACT'`, `source_section='§X.Y.Z'`.

For row 2:
- Pre-check: REF-MMMMM passes gate.
- Reviewer opens REF-MMMMM at §A.B.C. Section text states "corridors shall be a minimum of 1200 mm" with no pinch-point qualifier. Worst-case point W (pinch point) is not addressed at the cited section. Match: `NOT-FOUND`.
- INSERT row with `value_match='NOT-FOUND'`. Reviewer rechecks the source for a pinch-point clause; if none exists in REF-MMMMM, the jurisdiction-comparison cell is downgraded ("not addressed by code at worst-case point") or re-sourced.

The pattern generalizes to qualitative and definitional claims: locate the section, read what's there, compare to what the doc says it says.

## Spot-check schedule (human responsibility)

The Track 3 pilot mandate in PI rule #10 establishes that the first BPC entering Phase E.1 runs as a formal pilot with inline review before the skill scales to other BPCs. The pilot is not optional and not retroactively reconstructable — pilot review must happen before pilot conclusions can be drawn.

Beyond the pilot:
- **Per session:** 1 random citation closed this session. Open the cited source at the cited section. Ask: does the section actually contain what the row says it contains?
- **Per 10 sessions:** sample 3 rows by `value_match='EXACT'` or `claim_match='SUPPORTED'`. Re-verify against the cited section. If discrepancies emerge, the spot-check rate increases until calibrated.
- **Per 50 sessions:** external domain expert review of 5 closed citations. Compare expert verification to recorded `value_match`/`claim_match`. Discrepancies drive a methodology recheck — either tolerance ranges are wrong, the detection question is being applied loosely, or single-reviewer capacity has been exceeded for the domain.

## See also

- `decisions/DR-2026-05-13-evidence-verification-methodology.md` — adoption record; existence-vs-claim separation rationale
- `scripts/audit/reasoning_doc_citations_audit.py` — audit script (level 2)
- `skills/adversarial-research_SKILL.md` — companion: validates claim across literature
- `skills/progressive-measurement_SKILL.md` — companion: numerical-value boundary probing
- `skills/citation-miner_SKILL.md` — upstream: source existence verification (Phase B)
- `references/keyword-compendiums/<lang>.md` — multilingual term references (Phase A.11)
- `audits/bpc-rewrite-workplan-2026-05-11.md` — Phase E.1 execution context
