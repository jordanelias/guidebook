---
name: citation-verifier
description: >
  Verify citations, evidence claims, and source credibility for accessibility and built environment
  documents. ALWAYS use this skill when asked to audit citations, check references, verify evidence,
  flag hallucinated sources, confirm source credibility, or perform any evidence quality review.
  Trigger on: "check citations", "verify sources", "audit references", "is this claim supported",
  "evidence review", "citation audit". Essential for any accessibility guidebook review workflow.
---

<!-- Updated: CO-0006 2026-04-08 — ENRICH action added -->

**Intake:** ≤500 lines only. Full document → haiku-chunker first.
**Model:** Sonnet 4.6
**Never assume a source exists. Confirm via tool lookup or mark UNVERIFIED.**
**Sources/journals:** → `references/project-standards.md`
**Output schema:** → `references/project-standards.md` (fields: claim_id, section, claim_text, source, claim_type, confidence, citation_status)
**SelfCheck:** HIGH-confidence citations → assess twice with different framing; divergence = UNCERTAIN_REVIEW

## Steps
1. Extract all citations, implicit claims, standards refs, statistical claims → `[claim_id | text | citation | type]`
2. Classify each: type (empirical/standard/guideline/expert-opinion/anecdotal) · priority (HIGH/MED/LOW) · verifiability (tool-searchable/standards-lookup/unknown)
3. Verify:
   - Peer-reviewed → PubMed → Consensus → Scholar Gateway (max 3 tools/citation)
   - Standards → ISO, IEC, AODA, ADA, NBC, AS 1428, BS 8300, EN 17210, WCAG, UN CRPD
   - Statistical claims → trace to primary source; flag secondary-only
   - Implicit claims → flag for manual review + suggested search terms
4. Output:

**A. Verified Citations Table**
| ID | Claim | Source | Status | Notes |

Status codes: CONFIRMED · MISMATCH · UNNUMBERED · UNRESOLVABLE · UNVERIFIED · NOT_FOUND

**B. Information Gaps:** claim text · suggested replacement · search terms · severity (foundational/supporting/contextual)

**C. Claim objects (YAML)** — one per flagged item per schema

## Connectors
PubMed, Consensus, Scholar Gateway — activate for verification only.

---

## HARVEST Mode (v10.1 addition)

When triggered with "HARVEST" or "bibliography assembly": extract every unique citation from the document scope and produce a structured bibliography.

**Procedure:**
1. Scan all inline citations, evidence tables, and Key Citations fields across scope.
2. Deduplicate by author-year-title (fuzzy match on title to catch minor variations).
3. For each unique citation:
   - Verify existence via PubMed/Scholar Gateway/Consensus
   - Standardise format: `Author(s). (Year). Title. *Journal/Publisher*, Volume(Issue), Pages. DOI/URL`
   - Classify by evidence tier (1–6, Co-1, Co-2)
   - Record all item codes that cite this source
4. Produce bibliography in two formats:
   - **Alphabetical** (for Appendix: Bibliography)
   - **By evidence tier** (for internal reference)

**Output:**
```markdown
## Bibliography — HARVEST
**Date:** YYYY-MM-DD HH:MM
**Scope:** [document/volume/part]
**Total unique citations:** [N]
**Verified:** [N] · **Unverified:** [N] · **Not found:** [N]

### Alphabetical
[Standard bibliography entries]

### By tier
#### Tier 1 / Co-1
[entries]
#### Tier 2 / Co-2
[entries]
...

### Citation-to-item map
| Citation | Items citing | Tier |
|---|---|---|

### Unverified citations
| Citation | Items citing | Issue |
|---|---|---|
```

HARVEST mode resolves GAP-CR-01 (empty bibliography). Run on assembled document during Phase 5.

---

## ENRICH Mode (CO-0006 2026-04-08)

When triggered with "ENRICH" or called by research-log-manager migration pass: take one or more BPC short-keys and return fully populated rows for the BPC Key sources metadata table.

**Trigger:** `citation-verifier ENRICH {short-key}` or `citation-verifier ENRICH BATCH [{key1}, {key2}, ...]`

**Process (per short-key):**
1. Parse short-key to extract identifiers:
   - PMID pattern: `PMID{digits}` or `-PMID{digits}` → extract PMID integer
   - DOI pattern: `DOI{string}` or embedded DOI after year → extract DOI
   - If neither: mark `[NO-ID — manual entry required]` and skip API lookup
2. For PMID: query PubMed API → retrieve authors, year, title, journal, DOI
3. For DOI only (no PMID): query CrossRef API → retrieve same fields
4. For standards short-keys (e.g., `ADA-2010-S404`, `BS8300-2018`): reconstruct metadata from short-key pattern deterministically — no API call needed
5. Assemble row in BPC Key sources table format:

```
| {REF-ID} | {short-key} | {Authors} | {Year} | {Title ≤120 chars} | {Journal/Publisher} | {DOI or URL or [GREY]} | {Tier} | {Lang} | {Jurisdictions} |
```

**Batch mode:** Accept a list of short-keys; return all rows in sequence. Continue on individual failures — do not abort batch.

**Failure output (per key):**
```
| {next REF-ID} | {short-key} | [UNRESOLVED] | — | — | — | [UNRESOLVED — manual entry required] | — | — | — |
```

**Coverage estimate:** Before running a batch ENRICH pass on an existing BPC, count short-keys matching PMID/DOI patterns and report: `{N}/{total} short-keys have extractable identifiers ({pct}%). Estimated automated coverage: {pct}%.` If <20%: recommend manual metadata entry as primary strategy; proceed with ENRICH only for keys that have identifiers.

**Connectors required:** PubMed (for PMID lookups). CrossRef via web_search (for DOI-only lookups). Activate for ENRICH runs only.

**Output format:** Ready-to-paste markdown table rows. One row per short-key. Caller pastes into BPC `### Key sources` table.

