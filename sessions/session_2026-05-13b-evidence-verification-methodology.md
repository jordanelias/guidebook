---
session: session_2026-05-13b-evidence-verification-methodology
date: 2026-05-13
duration_hours: ~3 (continuation of compacted session)
operator: Claude (Opus 4.7)
session_close: 2026-05-13 — work artifacts committed; v10.9 PI staged for owner deployment
next_action: owner deploys PI v10.9 to live project settings (see decisions/PI-update-needed.md); next-session work: Track 1 second pass on remaining non-catalog-fetch records; Phase E.1 single-BPC pilot under new reasoning_doc_citations workflow (per DR-2026-05-13 §4 Track 3 pilot mandate)
blockers: PI v10.9 deployment requires manual owner paste into claude.ai project settings (Anthropic's project-knowledge layer is not API-writable); first Phase E.1 pilot BPC has not been selected yet — owner directive needed on which BPC enters the pilot
---

# Session 2026-05-13b — Evidence Verification Methodology

## Mandate

Owner directive (three times): "do whatever is in long-term best interest for project, but research best practices for parallel situations first" → "whatever is in best interest of project long-term, do" → "whatever is in best interest of project long-term, do". Same delegation pattern as DR-2026-05-09 ("whatever makes sense for long-term integrity and health"). Treated as authoritative delegation to research, decide, and execute.

## Diagnosis (continued from compacted prior session)

Prior session (also 13b, pre-compact) identified that `evidence_sources.verification_status = VERIFIED` is existence-verified only — not content-verified. `source_slug_links` is topic-level (ref_id ↔ slug), with no claim-level field. Per the handoff: 0/675 records have content-verified claim-level linkage; 0/675 have versioning tracked.

Owner question (via handoff): Option A (defer all to Phase E) vs Option B (build `source_claims` registry now as new Phase B.8).

## Research (5 web searches; web_search only, no PubMed/Consensus connector activation)

1. **Cochrane Handbook §5.5.2**: dual independent data extraction with pre-piloted forms is **mandatory** (MECIR Box 5.4.a). Screening (existence/relevance) is structurally separate from data extraction (claim-level).
2. **GRADE Evidence-to-Decision framework**: standardized dual independent extraction; 10% pilot calibration before full extraction.
3. **Empirical quotation-error base rate** (peer-reviewed medical literature):
   - Mogull 2017 (15 studies, 5,535 quotations): 14.5%; 64.8% of errors major
   - Jergas & Baethge 2015 (28 studies): 25.4% total; 11.9% major
   - Cobey et al. 2025 RIPR (46 studies, 32,000 quotations): 16.9% (CI: 14.1–20.0); 8.0% major
   - Smith & Cumberledge 2020 Proc. Roy. Soc.: 25%; "completely unsubstantiated" subtype = 33.9% of errors
   - Meta-regression: no improvement over time (slope −0.002, p=0.85)
4. **Technical-debt management**: front-load high-impact / low-cost (versioning backfill from existing data); defer high-impact / high-cost (full registry rebuild) unless cost-justified.
5. **Building code citation auditing**: less directly relevant; standards-development organization (SDO) practice is mostly about how *external* consumers cite SDO outputs, not how SDOs internally verify cited sources.

## Decision (DR-2026-05-13)

**Option C** (three-track hybrid). Not A or B. Rationale:
- `spec_value_probes` (PMP, rule #8) is functionally already a claim registry for numerical specs. Building a parallel `source_claims` table duplicates this.
- The 9-step rule step 3 is naturally per-(parameter × jurisdiction); recording verification inside the reasoning doc keeps data with synthesis.
- Front-loading 675 sources is the wrong unit; work-that-matters is per-claim, bounded by BPC count × parameters × jurisdictions.
- Paywall reality argues for a `value_match=PAYWALL` outcome rather than a blocking purchase-decision step.

**Tracks:**
1. **Versioning backfill** (`superseded_by_ref_id`, `edition` columns; no new schema)
2. **PMP as actual gate** for numerical-spec claims (rule #10 sharpening)
3. **`reasoning_doc_citations` table** for per-cell verification of jurisdiction values, qualitative claims, and definitional claims (used during Phase E.1)

§12 open questions answered by Claude under delegation:
- §12.1: Track 3 extended via `claim_type` enum (4 values) — no separate Track 4
- §12.2: `value_match=PAYWALL` accepted; `paywall_purchase_candidate` flag for periodic owner review
- §12.3: All (parameter × jurisdiction) cells (full scope)
- §12.4: Single-BPC pilot mandated before Track 3 scales

## Artifacts produced

| Artifact | Path | Status |
|---|---|---|
| Decision record | `decisions/DR-2026-05-13-evidence-verification-methodology.md` | ADOPTED |
| PI v10.9 draft | `governance/project-instructions-v10_9.md` | drafted; awaiting owner deployment per `decisions/PI-update-needed.md` |
| PI deployment queue update | `decisions/PI-update-needed.md` | updated for v10.9 |
| Migration 010 (FK integrity) | `scripts/migrations/010_fk_integrity_legacy_to_evidence_sources.py` | executed; user_version 9→10 |
| Migration 011 (reasoning_doc_citations table) | `scripts/migrations/011_reasoning_doc_citations.py` | executed; user_version 10→11 |
| Track 1 data migration | `scripts/migrations/data_20260513_track1_versioning_backfill_pass1.py` | executed; 41 records' editions populated |
| PMP audit script | `scripts/audit/pmp_audit.py` | created (was placeholder in PI rule #8); finds 3 real issues against current DB |
| Reasoning-doc-citations audit | `scripts/audit/reasoning_doc_citations_audit.py` | created (stub, empty-table case verified) |
| Updated DB | `data/guidebook.db` | schema_version 6→11; user_version 9→11 |

## DB state changes (verified)

- FK violations: 1 → 0
- `evidence_population_match.ref_id` NULLs: 5 → 0 (backfilled per handoff)
- PMP-A02-001-S2 ref_id: 'ANSI-S12.60-S5.3' (invalid) → 'REF-00335' (valid)
- `evidence_population_match.gap_id` column: added (NULL on all 22 existing rows; populates going forward)
- `reasoning_doc_citations` table: created (0 rows; first rows produced during Phase E.1 pilot)
- `evidence_sources.edition` populated: 1 → 42 records
- `evidence_sources.superseded_by_ref_id` populated: 0 → 0 (this pass; manual review needed before linking)

## Audit findings (pmp_audit.py against current DB)

3 real issues surfaced by the new audit:
- **CHECK 3**: walk PMP-A08-001 (school-environment-autism, A-08) has 3 steps but zero passing strict steps. ANSI S12.60 explicitly excludes special-education rooms; no autism-specific NC standard exists at the asserted value.
- **CHECK 4**: PMP-A02-001-S2 passes_strict=1 cites REF-00335 (ANSI S12.60:2010), but REF-00335 has `metadata_quality=AUTHOR-TITLE-ONLY` and `verification_status=NULL` — making it ineligible for synthesis under rule #10's existing gate. This is exactly the kind of cross-rule issue the sharpened rule #10 (combining existence + content gates) was meant to surface.

Both findings are pre-existing data conditions exposed by the new audit; not regressions caused by this session's work.

## Research log

Five web_search queries conducted; no PubMed / Consensus / Scholar Gateway connector activation (per standing rule #5 — connectors only when task explicitly requires research and web sources are insufficient; web sources were sufficient here). No per-slug research-log-manager LOG action required (this was project-meta research, not slug-keyed multilingual research).

Sources captured in DR §2:
- Cochrane Handbook ch. 5 (training.cochrane.org)
- Murray et al. 2023 HRBOR (GRADE EtD scoping review protocol)
- Cobey et al. 2025, RIPR meta-analysis (46 studies / 32,000 quotations)
- Mogull 2017, PLOS One (15 studies / 5,535 quotations)
- Jergas & Baethge 2015, PeerJ (28 studies, 25.4% pooled rate)
- Smith & Cumberledge 2020, Proc. Roy. Soc. A (33.9% unsubstantiated subtype)

## Workplan impact

`audits/bpc-rewrite-workplan-2026-05-11.md` Phase B scope unchanged. Tracks 1/2/3 added as amendments:
- **Track 1** runs alongside Phase B (no sequencing change)
- **Track 2** is a rule sharpening + audit hook; no Phase change
- **Track 3** binds into Phase E.1's reasoning-document workflow; modifies Phase E.1 specification but does NOT additionally gate Phase E start

Aggregate ~2300-hour estimate unchanged.

## Self-review caveat

`[SELF-AUTHORED — bias risk]` applies. This session reviewed and built on a handoff document Claude authored in the immediately prior (pre-compact) session. Cross-checked handoff diagnostic claims against actual DB schema this session — all verified. Five independent-reviewer limitations flagged in DR §11. `[CONFIDENCE: medium — quotation-error base rate is from medical literature, not building codes; domain extrapolation is reasonable but not domain-matched]`.

## Logging tags applied this session

- `[SELF-AUTHORED — bias risk]` on the DR (reviewing my own prior diagnosis)
- `[CONFIDENCE: medium — base rate not domain-matched]` on the 17–25% prior
- `[CTX: <25% | this turn: <25%]` at start of execution turn

## Token usage

Approximate: 300k of 1M context window (~30%). Substantial headroom remaining.

Breakdown (estimated, ±25%):
- Bootstrap + project file: ~15k
- Compacted-context summary: ~9k
- Prior chat reasoning + handoff fetch + research turn-1: ~80k
- Web search results (5 queries): ~30k
- DR drafting + editing: ~15k
- PI v10.9 drafting: ~10k
- Migration script writing + verification output: ~60k
- Audit script writing + testing: ~25k
- This session record + commits: ~50k
- Tool call overhead + reasoning: ~30k
