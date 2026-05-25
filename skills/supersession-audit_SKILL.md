---
name: supersession-audit
description: >
  Best-practice supersession check for the guidebook evidence corpus. For each anchor
  source cited by a slug, asks "is this source still the best current evidence for the
  parameter × population × outcome it supports?" — a temporal-and-tier search across
  PubMed, Scholar Gateway, Cochrane, and standards bodies. Runs in two modes: PER-SLUG
  (at slug closure under v2 closure-definition) and SEMIANNUAL (sweep across full
  corpus every 6 months). Produces per-source supersession_check records that gate
  bpc_metadata.supersession_check_complete and the v2 slug closure bar. ALWAYS use when
  asked to: check supersession, audit anchor sources, verify best evidence, run
  semiannual sweep, close slug under v2 definition. Trigger on: "supersession check",
  "audit anchor sources", "is this still best evidence", "semiannual sweep", "v2 closure",
  "best-practice audit".
---

**Model:** Sonnet 4.6 (mining + candidate harvesting) → Opus 4.7 for outcome judgment when ≥3 candidates returned
**Connectors:** PubMed (required), Scholar Gateway (required for design/OT/Co-1), Cochrane (web_fetch acceptable), CrossRef (web_fetch acceptable). Activate for the audit.
**SQLite:** `data/guidebook.db` via `scripts/db.py`
**Authoritative DR:** `decisions/DR-2026-05-24-best-practice-supersession-protocol.md`
**Schema:** `supersession_check` table; `bpc_metadata.supersession_check_complete` flag (migration 015)

---

## 0. Connector availability (read BEFORE auditing)

Before any supersession-audit pass, probe connector availability:

- **PubMed** — required for clinical (Tier 1) and SR/meta (Tier 3) supersession searches. If unavailable, ABORT the pass and log `[GAP — PubMed connector unavailable]`.
- **Scholar Gateway** — required for design literature, OT evidence, and Co-1. If unavailable, mark each affected source's outcome as `pending` with explicit `deferred_reason` and skip the slug closure flag. Do NOT substitute PubMed for Scholar Gateway on Co-1 — they index different corpora.
- **CrossRef** (via web_fetch) — used to fetch publication metadata on candidates returned by PubMed/Scholar Gateway when the source DOI is needed for the candidate record.
- **Standards bodies** (ISO, IEC, EN, ANSI, BSI) — Tier 4-5 supersession checks fetch directly from the publication catalog. Web_fetch acceptable.

**Partial-availability rule:** If a connector required for a source's evidence type is unavailable, that source's supersession check is marked `pending` (not deferred — `pending` is the explicit terminal state for incomplete checks). The slug cannot reach `supersession_check_complete = 1` while any source is `pending`.

---

## 1. Two Modes

### PER-SLUG mode (at slug closure)

Triggered when citation-miner has set `citation_mining_complete = 1` and the slug is ready for v2 closure. Walks every evidence_sources row cited by the slug (via source_slug_links), runs the supersession search per source per the §2 strategy matrix, records the outcome, and sets `supersession_check_complete = 1` when all are terminal. Then stamps `closure_definition_version = 'v2'`.

### SEMIANNUAL mode (sweep across full corpus)

Triggered on a calendar cadence (2026-12-01, 2027-06-01, etc.). For every (slug, ref_id) with last `supersession_check.checked_at` older than the sweep horizon (typically `checked_at < {sweep_date} - 6 months`), re-run the supersession search filtered to publication date > last checked_at. Outcomes update the most recent check record; older records retained for audit history.

The semiannual sweep can be partially automated (PubMed/Scholar Gateway query batches return candidates); the outcome-judgment step (does the candidate actually supersede?) remains human or Opus.

---

## 2. Search strategy matrix

For each anchor source, the search strategy depends on `evidence_type`:

### Tier 1 clinical (RCT, OT intervention; evidence_type IN ('clinical'))

**Primary:** PubMed search. Query construction:
- Parameter terms (from BPC parameter taxonomy) AND population terms AND outcome terms
- Filter: `pdat:{anchor_year+1}:3000` (publication date strictly after anchor)
- Publication types: prefer `Randomized Controlled Trial[Publication Type]` then `Clinical Trial[Publication Type]`
- Sort: relevance, max_results 20

**Secondary:** Cochrane Library direct (via web_fetch to cochranelibrary.com search). Look for any Cochrane review covering the same population × intervention.

**Tertiary:** Scholar Gateway, scoped to clinical literature for the parameter.

### Co-1 (lived experience, DPO position; evidence_type = 'co1')

**Primary:** Scholar Gateway. Query construction:
- Lived-experience / participatory-design / DPO terms AND parameter terms AND population terms
- Year filter: `start_year={anchor_year+1}`

**Secondary:** Direct DPO/NGO publication catalog (named-organization website fetch where applicable: e.g., IDA, HLAA, LPA, Habinteg, RNID, ENIL).

**Co-1 outcome rule:** unless the candidate explicitly invalidates the anchor (e.g., DPO retraction notice, position-paper update by the same organization), the default outcome is `co1_addition_logged` — the candidate is added to the slug's Co-1 corpus and the original anchor remains current. Co-1 evidence accumulates rather than supersedes.

### Tier 2 (NGO/DPO guideline; evidence_type = 'national_fw' or 'grey')

**Primary:** Direct organizational publication catalog (organization-specific URL).

**Secondary:** Web search for updated edition (e.g., "LPA Medical Resource Center [year]" for newer edition).

### Co-2 (OT CPG; evidence_type = 'co2')

**Primary:** Direct OT body publication catalog: CAOT (Canada), AOTA (USA), RCOT (UK), COTEC (Europe), WFOT (international).

**Secondary:** PubMed filtered to `Practice Guideline[Publication Type]`.

### Tier 3 (SR/meta-analysis; evidence_type = 'sr_meta')

**Primary:** PubMed search. Query:
- Parameter+population+outcome AND `(Systematic Review[Publication Type] OR Meta-Analysis[Publication Type])`
- Filter: `pdat:{anchor_year+1}:3000`
- Sort: relevance

**Secondary:** Cochrane Library direct.

**Tertiary:** Scholar Gateway, scoped to SR/meta corpus.

### Tier 4 (international standard; evidence_type = 'standard_eb')

**Primary:** Standards body catalog (ISO, IEC, EN, ANSI/ASA). Web_fetch to the catalog page for the standard's revision history; look for a more recent edition.

**Secondary:** Direct web search for "ISO {number} revision history" or "{standard} latest edition."

### Tier 5 (national beyond-code framework; evidence_type = 'national_fw')

**Primary:** Direct national framework publication catalog (BSI for BS 8300, NEN for Dutch standards, etc.).

**Secondary:** multilingual-research skill if the framework is non-English.

### Tier 6 (statutory code)

Not in scope for this skill. Tier 6 supersession is tracked under jurisdiction-tracker skill.

---

## 3. Outcome judgment

For each anchor source, after running the search:

| candidates returned | judgment workflow |
|---|---|
| 0 | Outcome = `current_best`. Record search_strategy_record and close. |
| 1-2 | Sonnet reads abstract(s); applies the four-outcome decision (current_best, superseded_by, refined_by, divergent). For ambiguous cases, escalate to Opus. |
| 3+ | Opus reads abstracts; multi-candidate synthesis. Most likely outcome: `divergent_no_supersession` or `refined_by` with the dimension named. |
| any Co-1 search | Default outcome: `co1_addition_logged` unless explicit invalidation found. |

### Decision rules for the four outcomes (Tier 1-5)

**current_best**: no candidate exists, OR every candidate is lower-tier than the anchor, OR every candidate is on a different parameter × population × outcome.

**superseded_by**: a candidate exists that is (a) higher-tier than the anchor, or (b) same-tier and more recent, AND addresses the same parameter × population × outcome AND its findings either confirm-with-larger-N or replace the anchor's findings.

**refined_by**: a candidate addresses the same parameter × population × outcome but refines on a specific dimension (e.g., a sub-population, a parameter value range, a specific outcome measure). The anchor still governs the unaffected dimensions. The refinement_dimension column must name the affected dimension.

**divergent_no_supersession**: multiple recent works exist with diverging findings on the same parameter × population × outcome. No single candidate supersedes; the synthesis cell needs joint assessment rather than single-source replacement. divergence_notes must summarize the divergence.

### Composite cluster searches (formalized 2026-05-25 per Pass-2 audit-pattern observations)

When a slug has multiple anchors covering overlapping parameter × population × outcome cells, per-anchor individual searches return mostly the same candidates at significant tool-call cost. The cluster pattern: identify topic clusters across the slug's anchors (typically 3-6 clusters per slug), run one composite PubMed/Scholar Gateway/standards-body query per cluster, and judge each anchor in the cluster against the cluster's candidate set. Each anchor still gets its own supersession_check row; the row's `search_strategy_record` records the composite query plus a note identifying which cluster the anchor belongs to. This pattern is replayable (the audit trail captures the cluster query verbatim) and tractable (~5x fewer tool calls than per-anchor searches with no loss of findings on densely-overlapping literatures). Per-anchor searches remain appropriate when an anchor has a unique parameter × population × outcome not shared with other slug anchors.

### Tier-6 supersession verification (lesson learned 2026-05-25)

When a Tier-6 statutory code is logged with outcome `current_best` because it is "out-of-scope per DR §Out-of-scope and handed off to jurisdiction-tracker", **do not speculate on supersession status from age alone**. Old codes are often still operative under building-code referencing mechanisms (e.g., NZS 4121:2001 remains the New Zealand Building Code D1/AS1 Acceptable Solution per Building Act 2004 §119 as of 2024-2025). The handoff note should say "queued for jurisdiction-tracker verification" without prejudging the outcome. Lessons surfaced in MOB-23 audit (Pass-2, room-acoustic-performance + mobility-built-environment).

---

## 4. Recording the outcome

For each anchor source, write one `supersession_check` row via `scripts/db.py`:

```bash
python3 scripts/db.py add-supersession-check \
    --slug {slug} \
    --local-ref {LOCAL_REF} \
    --ref {REF_ID} \
    --tier {anchor_tier} \
    --evidence-type {anchor_evidence_type} \
    --outcome {current_best|superseded_by|refined_by|divergent_no_supersession|co1_addition_logged} \
    --superseding-refs '[]'  # JSON list of ref_ids for not-yet-INSERTed; empty for current_best
    --superseding-dois '[]'  # JSON list of DOIs for candidates not yet in evidence_sources
    --refinement-dimension "..."  # only for refined_by
    --divergence-notes "..."  # only for divergent_no_supersession
    --search-strategy '{"tool":"pubmed","query":"...","date_filter":"...","candidates_returned":N,"candidates_reviewed":M}' \
    --check-method {pubmed_search|scholar_gateway|cochrane_direct|standards_body_direct|multilingual_research|composite} \
    --session {SESSION}
```

The `superseding_dois` field is the key gate: rule #10 forbids INSERTing candidates as evidence_sources rows without verification. Supersession candidates that are not yet verified live in `superseding_dois` (DOI list) rather than `superseding_ref_ids` (FK list). When a candidate is subsequently verified and INSERTed to evidence_sources, the supersession_check row should be UPDATED to move the DOI from `superseding_dois` to `superseding_ref_ids`.

---

## 5. Closing the slug under v2 definition

After every cited anchor source has a terminal supersession_check outcome (i.e., none `pending`):

```bash
python3 scripts/db.py update-bpc \
    --slug {slug} \
    --supersession-check-complete 1 \
    --closure-definition-version v2 \
    --session {SESSION}
```

This is in addition to `citation_mining_complete = 1`. The v2 closure bar requires both.

---

## 6. Anti-patterns

**Confusing supersession with citation-graph mining.** Forward mining via OpenAlex `cites:` finds papers that cite the anchor. Supersession searches via PubMed/Scholar Gateway find papers on the same parameter × population × outcome regardless of whether they cite the anchor. These are different operations; do not substitute one for the other.

**Treating Tier as the only dimension.** A higher-tier candidate does not automatically supersede a lower-tier anchor if it's on a different population or outcome. Match the cell (parameter × population × outcome) first; only then compare tier and recency.

**INSERTing candidates as evidence_sources during the audit.** The supersession_check record names candidates by DOI. Verification + INSERT is a separate downstream operation governed by PI rule #10's existence-and-content gate. Do not bypass.

**Closing under v2 with `pending` outcomes.** A `pending` outcome means the check is incomplete (connector unavailable, paywall, time-out, etc.). The slug cannot reach v2 closure while any source is pending. Either complete the check or downgrade to v1 closure and log the deferral.

**Treating Co-1 as supersedable by default.** Per DR-2026-05-24 §Co-1 supersession treatment, Co-1 evidence accumulates rather than supersedes. The default Co-1 outcome is `co1_addition_logged`, not `superseded_by`. Override only with explicit invalidation evidence (DPO retraction, position-paper update by the same organization).

---

## 7. Spot-check requirement (per PI rule #11 attestation)

When this skill is invoked, the audit_trail must include a `[READ: DR-2026-05-24]` tag and at least one `[STAGE: supersession-audit-{slug}]` boundary per slug audited. Failure to log the audit trail blocks attestation.

For semiannual sweeps, the attestation must include the sweep_date and the number of (slug, ref_id) pairs re-checked. Records older than the sweep horizon that did NOT get re-checked must be enumerated as `[GAP: skipped — {reason}]`.

---

## 8. Edge cases

**Anchor source no longer relevant to the slug.** If the supersession search reveals that the anchor was misclassified (e.g., GAP-292 RAP-13 rat-kindling paper under room-acoustic-performance), the outcome is recorded as `current_best` with a note flagging the misclassification, and the source_slug_links row is queued for owner review rather than retired by the audit.

**Anchor source retracted between original verification and audit.** Outcome = `superseded_by`, superseding_ref_ids = [the retraction notice or the corrected article if one exists], notes = "retraction surfaced during supersession audit." The original verification_status remains VERIFIED (the source did exist) but the synthesis cell needs to drop the anchor.

**Multilingual anchor where the audit can't read the language.** If a non-English-language anchor's parameter × population × outcome can't be expressed in English search terms, mark `pending` and queue for multilingual-research follow-up. Do not guess.
