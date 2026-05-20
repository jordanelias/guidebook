# DR-2026-05-20: Evidence metadata rehabilitation — type-routed protocol with mandatory cross-check

**Status:** PROPOSED (pending owner ratification)
**Adopted by:** session_2026-05-20-ato-rehab (pilot evidence from 3 cohorts)
**Supersedes:** ad-hoc author-title-only resolution in workplan §5 B.2

## Problem

Workplan §5 B.2 sized AUTHOR-TITLE-ONLY rehabilitation at ~15 min per row, treating it as mechanical web-search-by-author-year-title followed by metadata population. Pilot work across three cohorts (DOI/Crossref, PMID/PubMed, statutory/web-research) reveals two systematic issues that invalidate the "mechanical" framing:

1. **Pre-existing data-quality drift.** Of 75 rows probed across the three cohorts, **30 (40%) had recorded metadata that disagrees with the canonical record at the cited identifier**. Three sub-patterns isolated:
   - *Note-as-title* (academic-DOI cohort, ~12% of probed rows): `pub_title` was used at ingest as a citation shorthand or annotation rather than the canonical source title. Example: `"HIPI study. Lancet 385:231–238. 61006-0"` (with a DOI suffix fragment trailing) instead of `"Home modifications to reduce injuries from falls"`.
   - *Journal-name-as-title* (PMID cohort, ~7%): `pub_title` stores the journal name or `journal — topic` string. Example: `"J Psychiatric Research"` instead of the actual paper title.
   - *Programme-as-standard / Note-style standard_number* (statutory cohort): `standard_number` stores a programme name (Singapore EASE 2.0) or a topic description (KR 편의증진법 — 점자블록 statutory provisions) rather than a stable provision identifier.
2. **Truncated identifiers.** ~10% of stored DOIs are publisher-prefix-only fragments (`10.1080/10400435`, `10.3389/fbuil`). They were probably truncated at ingest from longer canonical DOIs. PubMed `articleids` can recover canonical DOIs for the subset that also has a PMID.

Treating these rows as "missing metadata, fill from search results" silently overwrites the original BPC author's intent (note-as-title was a deliberate annotation, even if a poor one), can attach metadata of a different paper (when the identifier was wrong), and erases owner-reviewable signal that the row needs human disposition.

## Decision

Evidence metadata rehabilitation is a type-routed protocol with mandatory cross-check before any field write. Specifically:

### 1. Type routing

For each AUTHOR-TITLE-ONLY row, classify into a metadata-completion path:

| Path | source_type / evidence_type signal | Target metadata_quality | Resolution mechanism |
|---|---|---|---|
| Academic-DOI | `doi` populated; `evidence_type ∈ {clinical, co1, co2, sr_meta}` | `COMPLETE` | Crossref `/works/{doi}` |
| Academic-PMID | `pmid` populated; same evidence_types | `COMPLETE` | NCBI EUtils esummary |
| Academic-no-ID | no `doi`, no `pmid`; same evidence_types | `COMPLETE` (after ID recovery) | Crossref title search; held if no match |
| Statutory | `source_type='standard'` OR `evidence_type ∈ {code, national_fw}` OR (`evidence_type='standard_eb'` AND `tier ∈ {2,4}`) | `COMPLETE-STATUTORY` | Per-row issuing-body + edition-year research per V2-manual routing |
| Advocacy/grey-org | residual | Decision-per-row | Same as statutory protocol with type determination as first step |

### 2. Cross-check is mandatory

For every row where an external identifier resolves to canonical metadata, run a normalized cross-check before any write:

- **Title check**: NFKD-normalized (strip combining marks), lowercased, de-punctuated. At least 3 shared tokens between stored `pub_title` and canonical title, OR stored title is fewer than 3 tokens.
- **Author check**: NFKD-normalized comparison of stored `first_author_last` against canonical first author surname.
- **Year check**: stored `pub_year` within ±1 of canonical (allows online-ahead-of-print drift).

Cross-check failures route to integrity-hold states (see schema 014). The row is NOT auto-upgraded; the discrepancy is logged for owner review.

### 3. Schema enforcement

Schema migration 014 adds two columns to `evidence_sources`:

- `metadata_integrity_status` (TEXT enum): `OK` / `MISMATCH-TITLE` / `MISMATCH-AUTHOR` / `MISMATCH-YEAR` / `MISMATCH-MULTI` / `DOI-TRUNCATED` / `DOI-404` / `RESOLVED`
- `metadata_integrity_detail` (TEXT): `cr=<canonical> vs db=<stored>` or, for RESOLVED rows, `[RESOLVED: ...]` prefix.

The integrity column is queryable as the owner-review queue: `WHERE metadata_integrity_status NOT IN ('OK', 'RESOLVED', NULL)`.

### 4. Reconciliation of multi-API mismatch

A row may be probed via multiple identifiers (e.g., a row with both DOI and PMID). If both APIs flag mismatch but on different fields, the reconciled status escalates to `MISMATCH-MULTI`. If both agree on the field, the status stays the same and the detail is appended. The reconciliation logic lives in the probe script; the DB always carries the most-conservative status.

### 5. Truncated-DOI rescue

When a row carries both a truncated DOI (flagged `DOI-TRUNCATED`) and a PMID, the PMID-resolution path attempts canonical-DOI recovery via PubMed's `articleids` list. Successful rescue overwrites the truncated DOI with the canonical full DOI AND clears the integrity status to `OK`. Rescue is contingent on cross-check passing — a wrong PMID does not rescue a truncated DOI; both flags compound.

### 6. Statutory cohort: V2-manual routing

For statutory rows, edition-year and issuing-body completion follows the V2-manual routing matrix from DR-2026-05-19:

- Static portal, EN, no paywall, primary text retrievable → `VERIFIED`
- Static portal, non-EN, primary text retrievable + secondary EN corroboration (WHO, official translations) → `UNVERIFIED-1`
- Commercial publication (SBi, NEN, ANSI, IEC, etc.) → `IS-PAYWALL`, hold `metadata_quality=AUTHOR-TITLE-ONLY` until owner purchases or recovers edition year via secondary
- SPA catalog non-EN, no paywall → `DEFERRED-V2-AUTOMATED` until per-portal scrapers exist
- 403/DNS/bot block → `NEEDS-HUMAN` (owner different-IP fetch)

## Anti-patterns

- **Treating identifier-resolution as gospel.** APIs return what the identifier points to; that's existence, not correctness-of-attribution. A wrong PMID returns a real paper that just isn't the one the BPC author meant to cite.
- **Auto-overwriting `pub_title` from canonical.** The stored value may be a deliberate annotation. Move it to `bpc_note` only after owner confirms the canonical is the intended source.
- **Counting MISMATCH rows as "verified-not-eligible."** They're verified-existence-but-misattributed. They do NOT clear rule #10 — and shouldn't be cited in synthesis until resolved.
- **Skipping cross-check on PARTIAL matches.** Crossref's `type` field distinguishes book chapters / preprints / etc. from journal articles; the cross-check threshold is the same regardless.

## Pilot evidence (cohort-spanning yield)

Three batches across this session:

| Batch | Cohort | n | Upgrades | Holds | Yield |
|---|---|---|---|---|---|
| 1 | Academic-DOI (Crossref) | 59 | 35 | 24 | 59% |
| 2 | Academic-PMID (PubMed) | 9 | 2 (incl. 1 DOI-rescue) | 7 | 22% |
| 3 | Statutory (web-research) | 7 | 3 | 4 | 43% |
| **Total** | — | **75** | **40** | **35** | **53%** |

Hold-rate above ~30% is consistent across cohorts — this is structural data-quality drift, not classifier strictness. The DR codifies the protocol that surfaces it for owner review rather than papering it over.

## Acceptance criteria for this protocol

A row is considered fully rehabilitated when:

1. `metadata_quality ∈ {COMPLETE, COMPLETE-STATUTORY}` AND
2. `verification_status ∈ {VERIFIED, UNVERIFIED-1}` AND
3. `metadata_integrity_status ∈ {OK, RESOLVED}` AND
4. The cross-check that produced (3) is recorded in `verification_note` with the probe timestamp and tool name.

The third predicate is new — added by this DR. Rule #10 sub-rule 1 (numerical-spec claim verification via PMP) and sub-rules 2/3 (reasoning-doc citation re-read) remain unchanged.

## Enforcement

- **Skill:** `skills/evidence-metadata-rehabilitation_SKILL.md` (this DR's protocol, type-routed).
- **Audit:** `scripts/audit/metadata_integrity_audit.py` (Level 2: surfaces inconsistencies between `metadata_quality=COMPLETE/COMPLETE-STATUTORY` and `metadata_integrity_status NOT IN ('OK','RESOLVED')`, plus the no-cross-check-recorded case).
- **CI:** no new blocking job this DR. The existing rule #10 audit at `scripts/audit_evidence_metadata.py` is unchanged.
