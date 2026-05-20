---
name: evidence-metadata-rehabilitation
title: Evidence Metadata Rehabilitation Protocol
purpose: Move AUTHOR-TITLE-ONLY and GREY rows past rule #10's existence gate via type-routed identifier resolution with mandatory cross-check
status: active
adopted: 2026-05-20
decision_record: decisions/DR-2026-05-20-evidence-metadata-rehabilitation.md
governs: AUTHOR-TITLE-ONLY × any-status and GREY × any-status rows in evidence_sources
enforcement: Level 2 (audit at scripts/audit/metadata_integrity_audit.py); existence-gate audit at scripts/audit_evidence_metadata.py
---

# Skill: Evidence Metadata Rehabilitation

## When to invoke

Trigger this skill for ANY of:
- A row where `metadata_quality='AUTHOR-TITLE-ONLY'` (regardless of `verification_status`)
- A row where `metadata_quality='GREY'`
- A row where `metadata_quality IS NULL` AND `verification_status='VERIFIED'` (classification-gap rows)
- A row where `metadata_integrity_status='DOI-TRUNCATED'` AND `pmid` is populated (rescue path)
- Any commit closing an open metadata-integrity hold (status update to `RESOLVED`)

Do NOT invoke for:
- Rows where `verification_status ∈ {CLOSED-DELETED, UNVERIFIED-CLOSED}` — already terminal
- Rows where `metadata_quality ∈ {COMPLETE, COMPLETE-STATUTORY}` AND `metadata_integrity_status='OK'` — fully rehabilitated
- Synthesis writes — those flow through `best-practice-synthesis-routing` (Opus only), not this skill

## What this skill does NOT solve

Read this first.
- Cannot recover the BPC author's original intent when `pub_title` is note-style and disagrees with the canonical title at the cited identifier. That decision is owner-only.
- Cannot detect wrong-identifier misattribution when both stored identifier AND stored author/year agree (only stored title disagrees with canonical content).
- Cannot upgrade rows whose canonical metadata sits behind a paywall the owner has not purchased.
- Cannot replace per-row human review when the integrity check flags a discrepancy. The protocol routes to `MISMATCH-*`; it does not resolve.

## Type routing (apply before any external call)

Read the row, then decide path:

| Signal | Path | Resolver | Target metadata_quality |
|---|---|---|---|
| `doi IS NOT NULL` AND `evidence_type ∈ {clinical, co1, co2, sr_meta}` | Academic-DOI | Crossref `/works/{doi}` | `COMPLETE` |
| `pmid IS NOT NULL` AND `evidence_type ∈ {clinical, co1, co2, sr_meta}` | Academic-PMID | NCBI EUtils `esummary.fcgi` | `COMPLETE` |
| `doi IS NOT NULL` AND `metadata_integrity_status='DOI-TRUNCATED'` AND `pmid IS NOT NULL` | DOI-rescue | NCBI EUtils → extract canonical DOI from `articleids` | `COMPLETE` |
| `source_type='standard'` OR `evidence_type ∈ {code, national_fw}` OR (`evidence_type='standard_eb'` AND `tier ∈ {2,4}`) | Statutory | Per-row issuing-body + edition-year web research; V2-manual routing per DR-2026-05-19 routing matrix | `COMPLETE-STATUTORY` |
| Residual (advocacy/grey-org/general report without identifier) | Type-determination-first | Determine canonical type via issuer; route to Academic-no-ID or Statutory | depends on determined type |

If multiple paths apply to one row (e.g., academic with both DOI and PMID): run them in priority order DOI > PMID > rescue > statutory > residual; the FIRST clean MATCH terminates further calls.

## Mandatory cross-check (run before any field write)

Before populating any field on a row, run normalized comparison against the canonical record:

### Normalizer (apply to all string comparisons)
```python
def normalize(s):
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()
```
NFKD-strip is required: failure to strip combining marks produces false-positive HOLD on rows where the only difference is a diacritic (e.g., `Larivière` vs `Lariviere`).

### Three checks per row
- **Title**: shared-token-count between `normalize(canonical_title)` and `normalize(db_pub_title)` ≥ 3, OR db value has fewer than 3 tokens.
- **Author**: `normalize(canonical_first_author_surname) == normalize(db_first_author_last)`.
- **Year**: `abs(canonical_year - db_pub_year) ≤ 1` (allows online-ahead-of-print drift).

### Verdict from cross-check
- All three pass → MATCH path: upgrade `metadata_quality`, populate missing fields, set `metadata_integrity_status='OK'`.
- Any check fails → HOLD path: populate `metadata_integrity_status` per the failing-check type, store discrepancy in `metadata_integrity_detail`, do NOT write canonical metadata to the row. Bump `verification_attempt_count`.

HOLD-state enum and meanings:

| Status | Meaning |
|---|---|
| `MISMATCH-TITLE` | Only title disagrees. Likely note-as-title or journal-as-title pattern. |
| `MISMATCH-AUTHOR` | Only author disagrees. Possible misattribution; possible name-form variation the normalizer didn't catch. |
| `MISMATCH-YEAR` | Only year disagrees by >1. Likely wrong identifier OR ingest typo. |
| `MISMATCH-MULTI` | Multiple fields disagree. Strongly suggests wrong identifier — escalate to owner. |
| `DOI-TRUNCATED` | DOI is a publisher-prefix fragment lacking article suffix. Rescue path applies if PMID available. |
| `DOI-404` | Well-formed DOI but not found at registrar. Re-search by author+year+title needed. |

## Mandatory field-write discipline

When upgrading a row (MATCH path):

1. Write canonical metadata to fields where DB value is NULL or empty. **Do NOT overwrite a populated field** even if the canonical disagrees with the current value — that disagreement is the cross-check's job and would route to HOLD instead.
2. Exception: DOI rescue path. When `metadata_integrity_status='DOI-TRUNCATED'` AND PubMed returns a canonical DOI, overwrite the truncated stored DOI with the canonical version. Document the swap in `verification_note`.
3. Set `metadata_quality` to the path target (`COMPLETE` or `COMPLETE-STATUTORY`).
4. Set `metadata_integrity_status='OK'`.
5. Set `metadata_integrity_detail` to a short record: `{resolver}-resolved {timestamp}; {type-info-if-meaningful}`.
6. Append a single line to `verification_note` recording the probe: `[PROBE {date} {batch-name}] upgrade ATO->{target}`.
7. Bump `verification_attempt_count` by 1.

When holding a row (HOLD path):

1. Do NOT touch any metadata field.
2. Set `metadata_integrity_status` to the specific MISMATCH-* or DOI-* value.
3. Set `metadata_integrity_detail` to the discrepancy: `{resolver}-mismatch {timestamp}: {reasons}`.
4. If the row already had a `metadata_integrity_status` from a prior probe, reconcile:
   - Same field flagged by both → keep status, append to detail.
   - Different field flagged → escalate to `MISMATCH-MULTI`.
   - Prior was `DOI-TRUNCATED` and new probe finds wrong-content → escalate to new MISMATCH status.
5. Append a single line to `verification_note` recording the probe: `[PROBE {date} {batch-name}] {new-status}`.
6. Bump `verification_attempt_count` by 1.

## Multi-API reconciliation

A row may be probed via DOI AND PMID in sequence (DOI first per priority order). If DOI HOLD and PMID MATCH (e.g., DOI-TRUNCATED rescue): apply PMID path, clear status to OK. If DOI MATCH and PMID HOLD: the DOI's MATCH stands; the PMID disagreement is logged as a separate note but does not reverse the upgrade. If both HOLD on different fields: `MISMATCH-MULTI`.

## Statutory path additional requirements

Statutory rows do not have a single-call resolver. Per-row research is mandatory:

1. Standard number + jurisdiction usually identifies the issuing body unambiguously (e.g., `HTM 08-01` + `UK` → NHS England / Dept of Health). Establish via web search.
2. Edition year is established via the issuing body's own portal where retrievable. Where commercial paywall prevents retrieval, route `verification_status='IS-PAYWALL'` and KEEP `metadata_quality='AUTHOR-TITLE-ONLY'` (the row is not COMPLETE-STATUTORY without year).
3. Title coherence: confirm stored `pub_title` matches the standard number's documented content. Statutory equivalents of the note-as-title pattern (programme name in `standard_number`, topic in `pub_title`) route to `MISMATCH-MULTI`.
4. Non-EN primary text with EN secondary corroboration (WHO MiNDbank, official translations) → `verification_status='UNVERIFIED-1'`, not VERIFIED.

## Worked example: clean MATCH

Stored row: `REF-00012`, DOI `10.1177/19375867231178313`, `first_author_last=NULL`, `pub_title="Housing accessibility and rehabilitation outcomes after stroke"`, `pub_year=2023`, `journal_name=NULL`.

Crossref `/works/10.1177/19375867231178313` returns:
- title: "Housing accessibility and rehabilitation outcomes after stroke"
- author[0]: Elf M.
- container-title: "HERD: Health Environments Research & Design Journal"
- volume: "16", issue: "4", page: "172-186"
- ISSN: 1937-5867
- issued.date-parts: [[2023, 6]]

Cross-check:
- title: 7 shared tokens — PASS
- author: db NULL, canonical "Elf" — PASS (no contradiction)
- year: 2023 = 2023 — PASS

Verdict: MATCH. Upgrade path. Write `journal_name`, `volume`, `issue`, `pages_start`, `pages_end`, `publisher`, `issn`, `first_author_last`, `first_author_first`, `author_count`, `author_display`. Set `metadata_quality='COMPLETE'`, `metadata_integrity_status='OK'`.

## Worked example: HOLD (note-as-title)

Stored row: `REF-00028`, DOI `10.1177/00187208211059860`, `first_author_last="Levine"`, `pub_title="Grab bar placement varies with body height (r=0.67). Human Factors"`, `pub_year=2023`.

Crossref returns:
- title: "Grab Bar Use Influences Fall Hazard During Bathtub Exit"
- author[0]: Levine S.
- issued.date-parts: [[2021]]

Cross-check:
- title: 1 shared token ("grab", "bar") — FAIL
- author: Levine = Levine — PASS
- year: |2023 - 2021| = 2 — FAIL (>1)

Verdict: HOLD with MISMATCH-MULTI (title + year). The DOI may still be correct — `pub_title` looks like a citation note ("varies with body height (r=0.67). Human Factors" reads as a paraphrase + journal-fragment) and `pub_year=2023` may be an entry error. No metadata is written. Owner reviews via the queue.

## Worked example: DOI rescue

Stored row: `REF-00027`, `doi="10.1080/10400435"` (truncated — only Taylor & Francis publisher prefix), `pmid="26132352"`, `metadata_integrity_status="DOI-TRUNCATED"` from prior Crossref probe.

PubMed esummary on PMID 26132352 returns:
- title: "Toilet Grab-Bar Preference and Center of Pressure Deviation During Toilet Transfer"
- author[0]: Kennedy MJ
- articleids: [..., {idtype: "doi", value: "10.1080/10400435.2014.976799"}]

Cross-check: title matches stored, author matches, year matches. MATCH path.

Rescue actions:
- Overwrite `doi` from truncated `10.1080/10400435` to canonical `10.1080/10400435.2014.976799`.
- Set `metadata_quality='COMPLETE'`.
- Set `metadata_integrity_status='OK'` (clears the prior DOI-TRUNCATED).
- Note in `verification_note`: `[PROBE {date} ATO-PMID-rehab] upgrade ATO->COMPLETE (DOI rescue)`.

## Verification step (mandatory)

Before claiming a citation supports a rule #10 synthesis claim, confirm:

1. `metadata_quality ∈ {COMPLETE, COMPLETE-STATUTORY}` AND
2. `verification_status ∈ {VERIFIED, UNVERIFIED-1}` AND
3. `metadata_integrity_status ∈ {OK, RESOLVED}` AND
4. `verification_note` contains the probe timestamp from this protocol.

Failing any predicate: the row is NOT eligible to support a synthesis claim. The fourth predicate catches rows that may have legacy COMPLETE+VERIFIED states from before this protocol existed; those rows need a fresh cross-check before synthesis use.

## Patterns that catch fabrication

- **The note-as-title pattern.** If `pub_title` reads like a fragment of a bibliography draft (journal name embedded, page range embedded, DOI suffix embedded), it is a citation-note. The canonical title is at the identifier; the row needs owner disposition on whether to move the note to `bpc_note` and adopt the canonical title.
- **The journal-name-as-title pattern.** If `pub_title` is itself a journal name or `<journal> — <topic>` string, the row's title was never populated. Same disposition as note-as-title.
- **The truncated-DOI pattern.** Stored DOI has only one slash and a short right-hand side (publisher prefix or journal-stem only). Crossref returns 404. Rescue via PMID if available; otherwise re-search by author+year+title.
- **The programme-as-standard pattern.** `standard_number` stores a programme/scheme name (e.g., a government subsidy programme) rather than a stable standards identifier. Owner reclassification needed.

## Integration with related skills

- `adversarial-research`: applies AFTER this skill clears a row's metadata. This skill provides existence + content-attribution; `adversarial-research` provides the dissenter/falsification framing for any synthesis built on the row.
- `progressive-measurement`: applies to numerical-spec claims that cite rows this skill rehabilitated. Spec verification is content-level; this skill is attribution-level.
- `citation-miner`: feeds candidates INTO this skill. When mining surfaces a new reference, this skill processes it through type-routing on first ingest.
- `manual-statutory-verification`: deprecated by this skill's statutory path. Use this skill going forward; preserve `manual-statutory-verification` references for historical sessions.
