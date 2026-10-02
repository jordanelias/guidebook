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
```
python3 scripts/db.py log-search ... --prior-expectation "<what you expect, written BEFORE you run it>"
```
State what you expected to find before searching, and why. If the search result matches the prior exactly, that's a flag, not confirmation.

**Corrected 2026-09-03.** This block read `UPDATE evidence_sources SET prior_expectation = ?
WHERE ref_id = ?` — hand-written SQL against a column that no longer exists on that table, and
against the wrong stage besides. `prior_expectation` moved to `search_executions` in migration
069, because DR-2026-05-09 §24 defines it as *what was expected BEFORE searching* and
`add-source` runs after the source is searched, screened, retrieved and read; a field written
there can only ever be a reconstruction, which is the exact artefact this output exists to
prevent. A skill is a caller (CLAUDE.md rule 4) and this one was missed by the sweep that moved
the field.

### 2. Search queries used
```sql
-- RETIRED 2026-08-25. Do NOT write evidence_sources.search_queries_used.
-- The query that surfaced a source is a RESEARCH-stage fact; writing it onto an
-- EVIDENCE row copies a fact across a stage boundary, which the owner's ruling of
-- 2026-08-25 forbids. It is already recorded once, verbatim, in
-- search_executions.query_text (rule R8 logs every query before screening), and is
-- reached from a ref_id through v_source_admission.query_text.
-- Log the search, not the copy:  python3 scripts/db.py log-search ...
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

## Standing subjects of every adversarial pass

**These four properties are NOT machine-decidable and no gate asserts them.** Each was raised as
a defect whose gate could only ever report, never check (D05-021, D05-022, D05-023; subject 4,
GAP-061), and the remedy chosen was to give the property a durable home in the pass that *can*
decide it. **This section is that home** — added 2026-09-03 after an audit found
`research_batch_dod.py`'s R7 and R13 comments naming "a standing subject of the adversarial pass"
while no such subject existed anywhere a brief would read. Cite all four by name in your
findings, including when you find nothing.

1. **Harm findings against the rows that claim them.** R7 prints the count of
   `search_executions.harm_finding = 1` and the candidate count, and asserts nothing about
   either. Since 2026-10-02 the only thing that can fail R7 is a search log whose counts
   contradict each other (screened more than found, or admitted more than screened); its
   candidate floor was removed because the batch being judged typed both terms of it. That
   leaves this subject, and RC1's `provenance_artefact_audit`, as R7's substantive
   enforcers. Read the flagged rows' `findings_note` against
   what the batch actually recorded: a harm flag with no finding behind it, and a finding in the
   brief that never reached a flagged row, are both invisible to the gate. The batch-05 exec-32
   filing gap was invisible by construction. The same reading covers R7's other half: an
   off-slug or unverified document the session record or transcript names that no
   `search_candidates` row records stayed in prose, and no count can show it.

2. **Each `mismatch_note` against the retained payload.** R13 tests that a population-match ROW
   exists; nothing reads `match_grade` or `mismatch_note`. A row whose stated rationale the
   stored payload contradicts passes. Open the payload under `retrieval-log/<session>/` and read
   the note against it — that is the only place the two can meet. Dissent is writable: a second
   row for the same (ref_id, population) is a contest, not a collision (DR-2026-08-19 §7).

3. **Independence and containment.** Nothing anywhere tests whether two "converging" sources are
   independent. In batch 05, REF-00977 (a systematic review) contains REF-00971 and REF-00784
   among its 48 included studies, and the DOIs were in the batch's own `citation_mining` row
   hours before the gate ran green over them. A synthesis counted as convergent with its own
   included primaries is one line of evidence counted three times. The standing query, until a
   writer exists:

   ```sql
   SELECT sr.ref_id AS container, cm.cited_doi, e.ref_id AS contained
   FROM citation_mining cm
   JOIN evidence_sources sr ON sr.ref_id = cm.ref_id
   JOIN evidence_sources e  ON LOWER(e.doi) = LOWER(cm.cited_doi)
   WHERE sr.ref_id <> e.ref_id;
   ```

   `v_source_containment` was proposed and **not** built: `connections_produced` carries no
   per-connection direction, so a view over it would assert containment the data cannot support.
   Run the query; do not trust its absence.

   **`connections_produced` RETIRED 2026-09-28** (DR-2026-09-26 phase 2b): the reasoning above
   still holds for every row written before that date (the column's live history), but no session
   writes it going forward, so the standing query's population stops growing. A source mined after
   this date has no `connections_produced` entry to find here at all — check the mining search's
   own `search_executions` row (`mined_ref_id`) joined to `search_candidates.exec_id` instead.

4. **Figures the payload states that no extraction carries, and concepts it names that no
   observation records.** Added 2026-10-02 for GAP-061. R11-harvest tests that each admission
   carries at least one observation; R16-adjudicate that every observation is adjudicated; R16
   that every term an adjudication names is a parameter or declined. All three read rows that
   exist. None can see a figure the source states for a concept nobody observed, or a figure for
   an observed, parameterised concept that no extraction carries — the row that would be checked
   was never written. That is how every figure batches stated for any concept but the one
   parameter that existed was lost while the gate read green. Take one sample per admitted
   source, not one per figure: open the persisted payload under `retrieval-log/<session>/` (the
   `-text.txt` where one exists), list the figures it states and the concept each is stated
   for, then read the record side for that `ref_id`:

   ```sql
   SELECT o.observation_id, o.surface_form, a.outcome, a.term_id, p.parameter_id
   FROM observed_terms o
   LEFT JOIN term_adjudications a ON a.observation_id = o.observation_id
   LEFT JOIN base_parameters p ON p.term_id = a.term_id
   WHERE o.ref_id = :ref;
   SELECT extraction_id, parameter_id, figure_role, claimed_value, claimed_unit, claim_text
   FROM source_value_extractions WHERE ref_id = :ref;
   ```

   A stated figure with no extraction, and a concept the payload states a figure for with no
   observation, are each a finding. Record it under `L2-fidelity` (the record does not say what
   the artefact says; there is no lens of its own, and the lens vocabulary is the column's CHECK),
   with `subject_table` `source_value_extractions` or `observed_terms` and the payload as
   `artefact`.

   **Read the answers that discharge the gates, not only that they exist** (added after the
   T2 review). R16 is satisfied by any adjudication and any declination, so a `DEFERRED` with
   a throwaway rationale, or a `decline-parameter --reason` of one word, clears it; R5 is
   cleared by an `R5-GREY-WARRANTED: <reason>` in a source's `grey_reason`. Read every
   `DEFERRED` rationale and every declination reason on the batch's admissions — the R16 PASS
   line's REPORTED `DEFERRED` count is the trigger — and every R5-waived row, whose reason the
   R5 line prints by `ref_id`: read it against the payload (a thesis or report, or a refereed
   article filed grey?). A one-word reason is a finding. Declining a population-lens term
   (`TERM-016` wheelchair user, for example) is a legitimate disposition, since a lens term is
   not a quantity under determination, but it is an owner-level framing question: if it reads
   as ritual rather than judgement, record it `WITHHELD-FOR-OWNER`.

   ```sql
   SELECT a.adjudication_id, o.ref_id, o.surface_form, a.rationale, a.created_by_session
   FROM term_adjudications a
   JOIN observed_terms o ON o.observation_id = a.observation_id
   JOIN evidence_sources e ON e.ref_id = o.ref_id
   WHERE a.outcome = 'DEFERRED' AND e.created_by_session = :batch;
   SELECT DISTINCT d.term_id, d.reason, d.created_by_session
   FROM parameter_declinations d
   JOIN term_adjudications a ON a.term_id = d.term_id
   JOIN observed_terms o ON o.observation_id = a.observation_id
   JOIN evidence_sources e ON e.ref_id = o.ref_id
   WHERE e.created_by_session = :batch;
   SELECT ref_id, grey_reason FROM evidence_sources
   WHERE grey_reason LIKE '%R5-GREY-WARRANTED:%' AND created_by_session = :batch;
   ```

## Population match record (per cited study)

```bash
# CORRECTED 2026-08-25. This block was hand-written SQL because db.py had no writer
# for this table -- the gap CLAUDE.md §4 names as where the 2026-08-19 fabrication
# entered. It has one now, and the CLI refuses what raw SQL could not see:
# a ref_id that is not an admitted source, a population code not in `populations`,
# a match_grade outside the schema's own CHECK, and MISMATCH with no reason given.
python3 scripts/db.py add-population-match \
  --ref-id REF-NNNNN --target-population AUT \
  --study-population "12 autistic adults, UK, semi-structured interviews" \
  --sample-size 12 --match-grade EXACT \
  --session {session}          # add --mismatch-note when the grade is MISMATCH
```

> **A SECOND ROW FOR THE SAME (ref_id, population) IS NOT AN ERROR AND IS NOT REFUSED.**
> `DR-2026-08-19` §7: an adversarial pass that re-grades blind lands its DISSENTING
> grade as a second row distinguished by `created_by_session`, and divergent grades
> **read as a contest**. That is the mechanic this skill exists to run. `source_ref` is
> written from `--ref-id` automatically -- it is a dual home the CLI cannot remove
> (committed migrations INSERT it) but can keep from ever disagreeing.

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
4. If unverifiable: do NOT claim citation supports the recommendation. Set
   `verification_status='UNVERIFIED'` with `verification_disposition='CLOSED'` and a
   `verification_closure_reason` (`not-found-after-search` or `disputed-existence`), and
   treat as no evidence. (`UNVERIFIABLE` was never in the vocabulary — before D-0157 or
   after it. The binary is VERIFIED / UNVERIFIED; why the pursuit stopped goes in the
   reason column.)

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
search_queries_used: RETIRED — read v_source_admission.query_text instead (2026-08-25)
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
