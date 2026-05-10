---
name: adversarial-research
title: Adversarial Research Protocol
purpose: Force every research-generating gap closure to produce specific, falsifiable artifacts that resist consensus-confirmation bias
status: active
adopted: 2026-05-09
decision_record: decisions/DR-2026-05-09-adversarial-research-protocol.md
governs: All gap closures with category=RP or descriptions containing "research"/"FDR"/"THIN-BASE"
enforcement: Level 2 (audit query at scripts/audit/research_protocol_audit.py)
---

# Skill: Adversarial Research Protocol

## When to invoke

Trigger this skill for ANY of:
- Gap closure where category=RP
- Gap closure where description contains "research", "FDR", "THIN-BASE"
- Adding evidence_sources entry with verification_status=VERIFIED
- Closing a gap that asserts a numerical specification value
- Multilingual remediation searches (multilingual-search-remediation.md)

Do NOT invoke for:
- Gap closures with category=AUDT/MX/CD/EC (different work types)
- Sync-only closures (CLOSED-SYNC) — no new evidence claim
- False-positive closures (CLOSED-FALSE-POSITIVE) — refutation, not research

## What this skill does NOT solve

Read this first. Do not skip:
- Cannot prevent fabrication of citations
- Cannot calibrate confidence intervals
- Cannot make match grades non-biased
- Cannot replace human spot-check
- Creates audit trails, not truth

The reviewer is the truth-source. This skill makes shallow research VISIBLE so the reviewer can act.

## Required outputs (DB-enforced)

Before any gap closure under this skill, populate ALL FIVE:

### 1. Prior expectation
```sql
UPDATE evidence_sources SET prior_expectation = ? WHERE ref_id = ?;
```
State what you expected to find before searching, and why. If the search result matches the prior exactly, that's a flag, not confirmation.

### 2. Search queries used
```sql
UPDATE evidence_sources SET search_queries_used = ? WHERE ref_id = ?;
```
List the queries you actually ran. This lets the reviewer audit whether queries were genuinely adversarial.

### 3. Confidence interval + shift conditions
```sql
UPDATE gaps SET 
    confidence_interval = '60-80%',
    shift_conditions = 'Drops to X if Y. Rises to Z if W.'
WHERE gap_id = ?;
```
Numerical range, not narrative ("moderate," "strong"). Specify both directions.

### 4. Named dissenter
```sql
UPDATE gaps SET named_dissenter = ? WHERE gap_id = ?;
```
Specific researcher/paper/institution with contrary or qualifying view. If absent, "NONE FOUND — searched [list queries]". The "NONE FOUND" is honest signal — either consensus is genuine or the search failed.

### 5. Falsification condition
```sql
UPDATE gaps SET falsification_condition = ? WHERE gap_id = ?;
```
Specific finding that would invalidate the recommendation. Multiple disjunctive conditions OK. Vague conditions ("better evidence") are not acceptable.

## Population match record (per cited study)

```sql
INSERT INTO evidence_population_match (
    match_id, source_ref, target_population, study_population, 
    sample_size, match_grade, mismatch_note, created_at, created_by_session
) VALUES (...);
```

Match grade rubric:
- **EXACT**: Same condition, same age range, same setting, sample size adequate. Or: standards-track document directly addressing target population.
- **PARTIAL**: Same condition, different age/setting OR adequate evidence with one significant qualifier
- **PROXY**: Related condition or methodology; small sample; generalization requires assumption
- **MISMATCH**: Different condition or population; do NOT use as primary support

If population_match grade distribution shows >70% EXACT across recent records, the audit will flag — this is the protocol working.

## Verification step (mandatory for evidence claims)

Before claiming a citation supports a recommendation:

1. Search for the citation directly (web_search with author + year + title keywords)
2. Confirm via INDEPENDENT sources (PubMed, publisher, indexing service, citing reviews)
3. Note in evidence_sources.notes: "Verified [date] via [list sources]"
4. If unverifiable: do NOT claim citation supports the recommendation. Mark verification_status as 'UNVERIFIABLE' and treat as no evidence.

Pattern that catches fabrication: I generate a plausible-sounding citation (right author style, right year range, right journal) that does not exist. The verification step is the ONLY way to catch this.

## Worked example

Bad (consensus-confirming):
```
Gap closure: "Door force ≤22N supported by ADA, ISO 21542, BS 8300 consensus"
prior_expectation: NULL
named_dissenter: NULL
confidence_interval: NULL
```

Good (protocol-compliant):
```
Gap closure: "Door force ≤22N supported by ISO 21542; PARTIAL match for RA flare via Björk 1997"
prior_expectation: "Expected 22N to be well-supported because ADA/ISO/BS converge"
search_queries_used: "Chaffin grip force rheumatoid arthritis door handle 22N; Björk grip force RA"
named_dissenter: "Björk et al. 1997 (PMID 9021280) — N=20 women with RA, grip force during pain. Small sample, women only, does not directly test 22N threshold."
confidence_interval: "40-55%"
shift_conditions: "Drops to 25-35% if specific Chaffin et al. 2006 citation cannot be verified. Rises to 65-80% if Björk 1997 successor studies confirm 22N within RA flare capacity."
falsification_condition: "Recommendation would change if (a) Björk or successor RA grip force study with N>30 shows 22N exceeds capacity for >10% of RA flare population; (b) ISO 21542 working group documentation cannot defend 22N derivation; (c) post-occupancy data shows hardware-related access failures correlate with 22N threshold."
evidence_population_match: PARTIAL (Björk N=20, women only, RA-specific)
```

The bad version produces no audit trail. The good version exposes that the recommendation rests on a small Swedish RA study and that the original Chaffin 2006 citation in the protocol example was unverifiable.

## What this skill caught (2026-05-09)

The protocol caught FOUR fabrications during its first deployment:
1. "Yang et al." standalone with 2.09× force figure (Yang IS co-author on Koontz 2005, but no standalone study with that figure)
2. "Japanese cervical SCI normalized power 0.23-0.26 W/kg" study
3. "Chaffin et al. 2006" RA grip force citation (used as example IN protocol v1 — protocol caught its own fabrication)
4. "30 second" DBL alarm detection threshold (no such NFPA 72 threshold)

The protocol also caught a SILENT BUG:
- INSERT OR IGNORE hid evidence_sources schema mismatch (tier INTEGER vs TEXT)
- Audit query showed "0 verified citations" after I claimed 4 in commit messages
- Schema strictness + audit separation = each layer catches different failure modes


## Pattern: topic-evidence vs claim-evidence (added 2026-05-10)

Caught during DR-2026-05-09 strict re-examination. The most common bias mode for Claude:

> **Conflating "evidence on the topic" with "evidence supporting the specific claim"**

Examples this skill caught when applied rigorously:

### Case 1: Hearing loops (GAP-069 A-10)
- Cited: IEC 60118-4 (real, verified)
- Claim: "Install hearing loops at reception/service counters"
- Bias: The standard specifies hearing loop PERFORMANCE (field strength), not WHERE to install loops. The "at counter" placement decision is design-derived, not evidence-derived.
- Result: Reopened, CI dropped from 70-85% to 40-55%.

### Case 2: Lip-reading lighting (GAP-097 B-02)
- Cited: Erber 1974 (real, shadow effect on lipreading documented)
- Claim: Specific lux thresholds for shadow-free face illumination
- Bias: Erber demonstrates SHADOWS reduce lipreading 3-12% but does NOT provide quantitative lux thresholds. BS 8300, CIBSE, AJA Bernstein 2021 — none provide lux thresholds for lipreading-specific illumination.
- Result: Reopened, CI dropped from 60-75% to 25-40%.

### Case 3: Thermal comfort (GAP-260 K-05)
- Cited: Griggs 2019 (PMID 31414956, real)
- Claim: Built-environment temperature specification for SCI users
- Bias: Griggs is exercise physiology — heat balance during EXERCISE/REST. Translation to building design specifications is an assumption.
- Result: Reopened, CI dropped from 75-85% to 45-60%.

### Case 4: Auracast (GAP-076 A-12)
- Cited: Bluetooth SIG specification + 2.5M global deployment forecast
- Claim: Specify Auracast readiness in new buildings
- Bias: The technology is real and deploying. But "specify readiness now in 2026 vs retrofit when needed in 2030" is a forward-looking design choice. Industry forecast ≠ empirical study showing building-side readiness adds value.
- Result: Reopened, CI dropped from 70-85% to 50-65%.

## Detection question

Before closing any research gap, answer in writing:

> **"Does the cited evidence specifically validate THE SPECIFIC CLAIM, or does it just speak to the topic?"**

If the answer is "speaks to the topic," the gap stays open OR closes with low confidence and explicit acknowledgment of the gap between cited evidence and specific claim.

## Audit checks for this pattern

The audit query (scripts/audit/research_protocol_audit.py) flags:
- CHECK 5: Closed gaps with NONE FOUND dissenter that lack review markers
- CHECK 2: Verified citations without population_match record (forces "what specifically does this support" question)
- CHECK 3: Population match grade distribution >70% EXACT (real evidence rarely perfectly matches)

## What this means for application

When invoking this skill:
1. State the prior
2. Search adversarially (find evidence AGAINST, not just FOR)
3. **Verify citations exist** (independent sources)
4. **Distinguish topic from claim**: trace what the citation actually supports
5. Population match: grade with rubric, log ref_id FK
6. Log all 5 protocol fields to gap

If you cannot honestly populate all 5 fields with specific content, the gap should remain OPEN. "NOT-RESEARCHED" is acceptable; vague closure is not.

## Audit query

Run before session close:
```bash
python3 scripts/audit/research_protocol_audit.py
```

Exit code 0 = clean. Exit code 1 = deficient closures present.

## Spot-check schedule (human responsibility)

Per session: 1 random gap, ask Claude "trace this to primary data" and "what would change your mind"

Per 10 sessions: Audit population_match grade distribution; pick 3 NONE FOUND entries and re-run searches with different phrasing.

Per 50 sessions: External domain expert review of 5 closed gaps; compare expert's confidence interval to Claude's.

## See also

- `decisions/DR-2026-05-09-adversarial-research-protocol.md`
- `workplan/research-protocol-adversarial.md` (full protocol document)
- `workplan/multilingual-search-remediation.md` (research execution plan that adopts this skill)
