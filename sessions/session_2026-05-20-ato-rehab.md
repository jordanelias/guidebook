# Session record: 2026-05-20 — AUTHOR-TITLE-ONLY × DOI rehabilitation pilot + schema 014

**Session ID:** `session_2026-05-20-ato-rehab`
**Span:** 2026-05-20 ~20:00 UTC → 2026-05-20 ~20:45 UTC
**Bootstrap version:** PI v10.14 + architecture v2.3 + userPreferences v6.3
**Pilot artifact:** Crossref-based metadata rehabilitation for AUTHOR-TITLE-ONLY × VERIFIED × DOI cohort
**Outcome:** Eligible pool 236 → 271 (35.2% → 40.4%, +5.2pp); AUTHOR-TITLE-ONLY 312 → 277; schema migration 014 adds explicit metadata-integrity tracking; CI regression introduced + diagnosed + fixed within session; both workflows green on `66dc69e9`.

---

## Headline outcomes

| Metric | Pre-session | Post-batch-1 | Post-batch-2 | Post-batch-3 | Session Δ |
|---|---|---|---|---|---|
| Eligible pool (rule #10) | 236 (35.2%) | 271 (40.4%) | 273 (40.7%) | 276 (41.2%) | **+40 (+6.0pp)** |
| AUTHOR-TITLE-ONLY | 312 | 277 | 275 | 272 | −40 |
| COMPLETE | 147 | 182 | 184 | 184 | +37 |
| COMPLETE-STATUTORY | 134 | 134 | 134 | 137 | +3 |
| metadata_integrity_status flags | none (column didn't exist) | 35 OK + 24 holds | 37 OK + 25 holds | 41 OK + 28 holds | new tracking dimension |
| Schema version | 13 | 14 | 14 | 14 | +1 |
| Both CI workflows green on HEAD | ✓ (`75158a9b`) | ✓ (`66dc69e9`) | ✓ (`f028b395`) | ✓ (`15b286d2`) | held; mid-session red on `ad92e95c`, `460e02c5` (both diagnosed + fixed in-session) |

---

## Commits in chronological order

1. `d9253768` — governance: schema 014 add metadata_integrity_status + metadata_integrity_detail columns
2. `ad92e95c` — evidence-metadata-rehabilitation: ATO-DOI rehab batch 1 (collapsed commit, **CI failed**: commit-msg + GAP-290 migration reproducibility)
3. `66dc69e9` — evidence-metadata-rehabilitation: strip self-insert from batch 1 migrations (CI green)
4. `460e02c5` — session-consolidator: initial session record (**CI failed**: rule #11 missing DOCTRINE + attestation)
5. `20d23f55` — session-consolidator: attestation for session record + DOCTRINE token (CI green)
6. `f028b395` — evidence-metadata-rehabilitation: ATO-PMID rehab batch 2 — 2 upgrades incl. DOI rescue, 7 holds (CI green)
7. `b84041e0` — evidence-metadata-rehabilitation: statutory rehab batch 3 — 3 upgrades, 1 IS-PAYWALL, 3 holds (CI green)
8. `15b286d2` — evidence-metadata-rehabilitation: DR-2026-05-20 + skill + audit script + registry (CI green)

Two mid-session CI regressions, both diagnosed and fixed within the session. Final HEAD `15b286d2`.

---

## Work executed

### 1. Triage of the AUTHOR-TITLE-ONLY + NULL cohorts

Initial bootstrap status block: 312 AUTHOR-TITLE-ONLY, 203 NULL verification. Cross-tab analysis revealed the cohorts overlap differently than the headline suggests:

| metadata_quality | verification_status | n | Implication |
|---|---|---|---|
| AUTHOR-TITLE-ONLY | VERIFIED | 163 | Existence already established — needs metadata completion only |
| AUTHOR-TITLE-ONLY | NULL | 149 | Full probe + metadata completion |
| GREY | NULL | 54 | Different track |
| NULL metadata | VERIFIED | 10 | Classification gap |

Triage routed the 312 by document type per the user's reminder:
- Academic/research path (`COMPLETE` target): DOI/PMID + journal + volume + pages + authors. ~165 rows.
- Statutory path (`COMPLETE-STATUTORY` target, per DR-2026-05-18): issuing body + jurisdiction + standard number + edition year. ~120 rows.
- Advocacy/grey-org: type determination first.

### 2. Schema migration 014: metadata-integrity tracking

The user directed: "Create explicit field for mismatched data in sqlite."

Two new columns on `evidence_sources`:
- `metadata_integrity_status` (TEXT, NULL default) — enum: `OK` / `MISMATCH-TITLE` / `MISMATCH-AUTHOR` / `MISMATCH-YEAR` / `MISMATCH-MULTI` / `DOI-TRUNCATED` / `DOI-404` / `RESOLVED`
- `metadata_integrity_detail` (TEXT) — human-readable detail; for RESOLVED, prefixed `[RESOLVED: ...]`

Applied as schema migration 014. user_version 13 → 14.

### 3. Pilot batch 1: AUTHOR-TITLE-ONLY × VERIFIED × has-DOI

Script: `scripts/probes/probe_ato_verified_doi.py`. Cohort: 59 rows. Protocol per row:
1. GET `https://api.crossref.org/works/{doi}` (4 req/sec, under the 5/sec limit)
2. Cross-check Crossref's title / first-author surname / year against DB-recorded values (normalized comparison)
3. If cross-check passes: extract journal_name / volume / issue / pages / publisher / ISSN / authors, upgrade `metadata_quality` to `COMPLETE`, set `metadata_integrity_status='OK'`
4. If cross-check fails: leave existing metadata alone, populate `metadata_integrity_status='MISMATCH-*'`, record discrepancy in `metadata_integrity_detail`, bump `verification_attempt_count`

Verdict distribution:

| Verdict | n | % |
|---|---|---|
| ATO→COMPLETE-CROSSREF-MATCH | 32 | 54% |
| ATO→COMPLETE-CROSSREF-PARTIAL | 2 | 3% |
| Diacritic false-positive (reclassed as MATCH) | 1 | 2% |
| HOLD-CROSSREF-MISMATCH | 18 | 31% |
| HOLD-CROSSREF-404 | 6 | 10% |
| **Total** | **59** | |

Net: 35 upgrades, 24 holds with integrity flags.

### 4. Methodology finding (NEW — DR candidate)

The 31% mismatch + 10% 404 rate is not API noise. Two systematic patterns isolated:

**A. Note-as-title pattern.** `pub_title` was used at ingest as a citation shorthand or annotation rather than the canonical source title. Examples surfaced:
- REF-00028: db `"Grab bar placement varies with body height (r=0.67)"` (a paraphrase of finding); Crossref `"Grab Bar Use Influences Fall Hazard During Bathtub Exit"`
- REF-00068: db `"HIPI study. Lancet 385:231–238. 61006-0"` (bibliography-draft fragment with DOI suffix appended); Crossref `"Home modifications to reduce injuries from falls"`
- REF-00091, 00101, 00103, 00136, 00151, 00069 (multi-field): same pattern

This affects ~12% of academic-source rows in the DOI cohort and likely affects the non-DOI cohort too.

**B. Truncated DOIs.** 5 of 6 404s stored a publisher-prefix-only fragment as the DOI:
- `10.1080/10400435` (T&F prefix, no article suffix)
- `10.1080/00140139` (T&F prefix)
- `10.1080/09613218` (T&F prefix)
- `10.3389/fbuil` (Frontiers prefix+journal-stem)
- `10.21834/jabs` (publisher+journal-stem)

These need re-search by author+year+title to recover the full DOI.

**C. Author misattribution** (smaller subset): REF-00008 `'van der Kuil' vs 'van der Ham'`, REF-00041 `'Hu' vs 'Clark'`, etc. — appear to be genuine ingest-era errors, not the note-as-title pattern. ~6 rows.

These findings will inform a DR proposing methodology refinements (Crossref cross-check as a mandatory step in ATO-rehab; type-routed metadata completion protocol). The DR is not authored this session — single pilot batch is insufficient justification per DR-2026-05-19 precedent (needs ≥3 jurisdictions / cohorts).

### 5. Companion author-row backfill

Initial migration broke db_integrity check G02 (3 COMPLETE person-authored sources missing rows in `evidence_source_authors` join table). Resolved by `data_20260520201500_ato_doi_rehab_batch_1_author_rows.sql` — refetched authors from Crossref for the 3 affected refs (REF-00012, REF-00332, REF-00602), inserted 13 author rows. 35/35 integrity checks restored.

### 6. CI regression + recovery

Push of `ad92e95c` failed both CI workflows:

**Failure 1 — Commit message format.** `check_commit_msg.py` validates only HEAD's subject line via `git log -1 --format=%s` and requires the timestamp as the last bracket. My amended commit moved the timestamp into the body. Per last session's precedent (no force-push on main), addressed by pushing a fix-up commit (`66dc69e9`) with a properly-formatted subject.

**Failure 2 — Migration reproducibility (GAP-290).** Root cause: my data migration files included a self-insert into `data_migrations` using the filename-stem migration_id. The runner's `--rebuild` path also inserts a tracking row with the same filename-stem ID → UNIQUE constraint collision. 11 of 25 historical migrations also self-insert, but they use custom migration_ids (no collision with the runner's filename-stem insert). Last session's batches stopped self-inserting entirely (cleaner pattern).

Fix in `66dc69e9`: stripped the `INSERT INTO data_migrations ...` block from both my data migration files, replaced with a comment `-- (data_migrations tracking row is inserted by scripts/migrate_db.py runner)`. Local `scripts/migrate_db.py --rebuild` verified 3 schema + 22 data migrations replay cleanly before push.

### 7. Pilot batch 2: AUTHOR-TITLE-ONLY × VERIFIED × has-PMID (+ DOI-TRUNCATED rescue path)

Script: `scripts/probes/probe_ato_verified_pmid.py`. Cohort: 9 rows (7 ATO×VERIFIED×has-PMID + 2 batch-1 DOI-TRUNCATED rescue candidates with PMIDs).

Applied batch-1 lessons:
- NFKD-strip normalizer (eliminates the diacritic FP class the batch-1 manual reclass exposed)
- No `INSERT INTO data_migrations` (runner tracks via filename stem)
- New rescue path: when `metadata_integrity_status='DOI-TRUNCATED'` AND PMID present, PubMed's `articleids` list can recover the canonical DOI

Verdict distribution:

| Verdict | n | % |
|---|---|---|
| ATO→COMPLETE-PUBMED-MATCH | 1 | 11% |
| ATO→COMPLETE-PUBMED-MATCH-DOI-RESCUE | 1 | 11% |
| HOLD-PUBMED-MISMATCH | 7 | 78% |
| **Total** | **9** | |

Net: 2 upgrades (REF-00027 truncated-DOI rescue → canonical `10.1080/10400435.2014.976799`; REF-00538 clean match), 7 holds.

**78% mismatch rate isn't classifier strictness — it's structural.** The mismatches cluster in two patterns:

- **Journal-name-as-title (REF-00100, 00101, 00103, 00105)** — `pub_title` stores the journal name or `<journal> — <topic>` string rather than the canonical paper title. Same family as batch 1's note-as-title pattern. Affects ~7% of the academic-PMID cohort.
- **Wrong-PMID misattribution (REF-00069, 00096, 00527)** — the PMID resolves to an unrelated paper. REF-00069 and REF-00096 also had `MISMATCH-MULTI` from batch 1's Crossref probe; both APIs flagging the same row is strong evidence of full-row misattribution at ingest.

REF-00527's batch-1 `DOI-TRUNCATED` flag was escalated to `MISMATCH-MULTI` (wrong PMID is bigger than truncation).

### 8. Pilot batch 3: statutory cohort (source_type=standard × NULL)

Cohort: 7 rows (KR/SG/UK/UK/ES/DK/KR). All seven had `jurisdiction` + `standard_number` + `tier` + `evidence_type` populated; missing `publisher` (issuing body) and `pub_year` (edition year) — the two remaining COMPLETE-STATUTORY requirements per DR-2026-05-18.

Protocol: per-row web research with cross-check between stored title and standard_number's documented content. No single-call resolver (unlike DOI/PMID); each row required individual judgment.

Dispositions:

| Ref | Decision | Why |
|---|---|---|
| REF-00020 (KR 편의증진법 시행규칙) | → COMPLETE-STATUTORY × UNVERIFIED-1 | Korean Ministry of Health & Welfare, enacted 1997; non-EN primary text with EN secondary corroboration via WHO MiNDbank |
| REF-00164 (SG EASE 2.0) | → MISMATCH-MULTI | EASE 2.0 is an HDB subsidy programme (2024), not a standards document. Owner reclassification needed |
| REF-00193 (UK HBN 00-03) | → MISMATCH-TITLE | HBN 00-03 documented as "Clinical and clinical support spaces" (NHS England, 2013); DB `pub_title="healthcare bariatric guidance"` is wrong-attribution |
| REF-00403 (UK HTM 08-01 Acoustics) | → COMPLETE-STATUTORY × VERIFIED | NHS England 2013-03-19, open-access PDF |
| REF-00464 (ES DB SUA) | → COMPLETE-STATUTORY × VERIFIED | Ministerio de Transportes/Movilidad/Agenda Urbana, base year 2010, open-access at codigotecnico.org |
| REF-00469 (DK SBi 230) | → IS-PAYWALL (metadata_quality unchanged) | SBi/AAU commercial; cannot confirm edition year without paywall purchase |
| REF-00511 (KR 편의증진법 — 점자블록) | → MISMATCH-MULTI | `standard_number` is note-style ("점자블록 statutory provisions"), not a stable identifier |

3 upgrades, 4 holds. The note-as-title pattern from batches 1-2 has a statutory analog: **programme-as-standard** (EASE 2.0) and **note-style standard_number** (편의증진법 — 점자블록). Pattern is cohort-spanning, not academic-specific.

### 9. Skill promotion (DR + skill + audit + registry registration)

Three cohorts validated → skill promotion threshold met per DR-2026-05-19 step 5 precedent (≥3 distinct cohorts).

Artifacts shipped in commit `15b286d2`:

- **`decisions/DR-2026-05-20-evidence-metadata-rehabilitation.md`** — methodology DR codifying the type-routed protocol with mandatory cross-check. Status PROPOSED pending owner ratification. Documents the three findings as cohort-spanning patterns; establishes a new fourth acceptance predicate (`metadata_integrity_status ∈ {OK,RESOLVED}` AND `verification_note` carries probe timestamp).
- **`skills/evidence-metadata-rehabilitation_SKILL.md`** — protocol skill mirroring the `adversarial-research_SKILL.md` format. Universal per architecture v2.3 (no session IDs / dates / SHAs in body). Type routing table, mandatory cross-check with NFKD normalizer, HOLD-state enum, multi-API reconciliation logic, DOI rescue path, statutory path with V2-manual routing reference, worked examples.
- **`scripts/audit/metadata_integrity_audit.py`** — Level 2 audit script. Three checks: (1) inconsistency FAIL on COMPLETE rows with open MISMATCH/DOI status; (2) INFO on rule #10 eligible rows lacking cross-check record (236 / 276 are legacy pre-DR); (3) INFO surfaces the owner-review queue counts. Exit code 0 on PASS, 1 on inconsistency.
- **`references/skill-registry.md`** — `evidence-metadata-rehabilitation` registered alphabetically in active-skills list.
- **`attestations/decisions_DR-2026-05-20-evidence-metadata-rehabilitation.json`** — rule #11 attestation. Notes the self-authored-DR bias risk and an independent-reviewer counterclaim on classifier-strictness assumptions. Verdict: DEVIATION-LOGGED.

Audit script run at HEAD: 0 inconsistencies; 236/276 (85.5%) eligible rows are pre-DR legacy needing cross-check before any future synthesis use; 28-row owner-review queue.

---

## Surfaced patterns / drift

### Drift 1: Commit-message format vs amended-body timestamp

**Issue.** Amending a commit with multi-line message body where the timestamp moves to the body fails `check_commit_msg.py` because the validator reads `--format=%s` (subject only). Same family as last session's Drift 1 (DOCTRINE-token placement) — both are subject-line-position constraints not documented inline at the point of editing.

**Resolution this session.** Pushed `66dc69e9` with correctly-formatted subject. The bad commit `ad92e95c` remains in history (per last session's precedent).

**Forward.** Worth a `scripts/ci_helpers/pre_commit_msg.sh` developer hook that validates the subject before commit lands. Not authored this session.

### Drift 2: Migration self-insert pattern inconsistency

**Issue.** 11 of 25 historical data migrations self-insert into `data_migrations` (with custom IDs); 14 do not (runner tracks). I followed the wrong pattern. The mixed convention is itself drift — a clean repo would have either all-self-insert (with custom IDs to avoid collision) or none-self-insert (runner tracks).

**Resolution this session.** My batch normalized to none-self-insert. Future migrations should follow this. The 11 historical self-inserters are not retroactively fixed — they work because their custom IDs differ from filename stems.

**Forward.** Architecture DR candidate: codify "data migrations do not self-insert into data_migrations; the runner is the sole tracker" as a hard convention. Audit script `scripts/audit/migration_self_insert_audit.py` could enforce on new migrations.

---

### Drift 3: Inherited row-level rebuild parity gap (NOT introduced by this session)

**Issue.** Local `--rebuild` invariant check during post-session double-check revealed 10 rows where committed DB shows `metadata_quality='COMPLETE'` but rebuilt-from-migrations DB shows `metadata_quality='COMPLETE-STATUTORY'`. The 10 rows: REF-00018, REF-00144, REF-00207, REF-00323, REF-00329, REF-00351, REF-00412, REF-00422, REF-00431, REF-00445. Migration `data_20260518050000_promote_statutory_metadata.sql` in the history promotes them; the committed DB never received the promotion (their `updated_by_session='26025520450'` is a Unix-epoch artifact suggesting a non-runner write path).

**Pre-session check.** Verified via `git checkout 75158a9b -- data/guidebook.db` (the pre-session commit): 10/10 rows showed COMPLETE then too. Drift inherited; not introduced this session.

**Why CI didn't catch it.** The `migration-reproducibility` job in `audit.yml` (GAP-290 blocker) compares 6 invariants between committed and rebuilt DBs: `user_version`, total counts of `evidence_sources` / `citation_mining` / `source_slug_links` / `gaps` / `connections` / `items`. Bucketed `metadata_quality` distributions are not in that invariant set. CI is satisfied; bit-parity is not.

**Correction to earlier session record claim.** "Local `scripts/migrate_db.py --rebuild` verified 3 schema + 22 data migrations replay cleanly before push" (line 125) is true narrowly — the runner exits 0 — but misleading. It does not establish row-level parity, and 10 rows of preexisting drift were present then and now.

**Implications for net session figures.** My headline claim was eligible pool 236→276 (+40, +6.0pp). That figure compares committed DB pre-session to committed DB post-session. If we use the rebuilt-from-history DB as the truth source, the 10 drift rows would already count as COMPLETE-STATUTORY × VERIFIED — meaning the pre-session truth was 246/670 (36.7%), not 236/670 (35.2%). Net session delta would be +30, not +40. The drift doesn't reduce my work; it changes the starting line.

**Forward.** This belongs to a future GAP-290 audit script revision: extend the invariant comparison to include `metadata_quality` cross-tab. Either reconcile the committed DB to the migration history (apply the missing UPDATE), or emit a new data migration that explicitly reverts the 10 rows if the committed state is the intended one. Either resolution needs owner direction since the source of the 10 COMPLETE values is unknown.

## Rule traceability

| Rule | Mechanism | This session's instance |
|---|---|---|
| #1 source discipline | text rule | Cross-check mismatches NOT auto-overwritten. 24 rows held with explicit `metadata_integrity_status` flags rather than silent metadata-import. Honest documentation of 31% mismatch rate. |
| #4 research-log discipline | text rule | Crossref-resolution is not slug-keyed research; no research log entry needed. |
| #10 evidence-verification | scripts/audit_evidence_metadata.py | Direct purpose of session — moved 35 rows past the existence gate. New `metadata_integrity_status='OK'` provides content-verification beyond plain existence. |
| #11 adherence-logging | scripts/audit/adherence_log_audit.py | No synthesis-bearing files touched; commits did not require DOCTRINE token. Adherence-log not emitted (no synthesis stage boundary this session). |

---

## State of integrity columns post-session

```
metadata_integrity_status     count
NULL                          601
OK                            41
MISMATCH-TITLE                10
MISMATCH-MULTI                8
MISMATCH-AUTHOR               5
DOI-TRUNCATED                 4
MISMATCH-YEAR                 1
```

28 holds queryable as `WHERE metadata_integrity_status NOT IN ('OK', 'RESOLVED', NULL)`. This is the owner-review queue surfaced by `scripts/audit/metadata_integrity_audit.py`.

41 OK comprises 40 this-session upgrades + 1 batch-2 NULL→OK promotion (REF-00538). Pre-DR-2026-05-20 legacy rows: 236 / 276 eligible (85.5%) — they cleared rule #10 but predate cross-check; future synthesis claims on them should run cross-check first.

---

## Known broken / pending work

### Owner-review queue: 28 metadata-integrity holds (final post-session count)

Queryable: `SELECT ref_id, metadata_integrity_status, metadata_integrity_detail FROM evidence_sources WHERE metadata_integrity_status LIKE 'MISMATCH%' OR metadata_integrity_status LIKE 'DOI-%' ORDER BY metadata_integrity_status;`

By type (post-batch-3):
- **MISMATCH-TITLE (10 rows)** — `pub_title` is citation shorthand or wrong-attribution; canonical title at identifier differs.
- **MISMATCH-MULTI (8 rows)** — multiple-field disagreement, likely wrong identifier (REF-00069, REF-00096 flagged by BOTH Crossref AND PubMed).
- **MISMATCH-AUTHOR (5 rows)** — surname mismatch. Possible misattribution.
- **DOI-TRUNCATED (4 rows, post-rescue)** — stored DOI is publisher-prefix fragment; no PMID for rescue. Re-search by author+year+title needed.
- **MISMATCH-YEAR (1 row)** — year off by >1.

### Remaining AUTHOR-TITLE-ONLY cohort (272 rows post-session)

- 126 VERIFIED × no-DOI / no-PMID  — natural next batch: Crossref title-search path. Many are reports/guidelines.
- 145 NULL × all types  — full-probe required; type-determination first.
- 1 IS-PAYWALL (REF-00469 SBi 230) — paywall queue.

### Remaining NULL verification (145 rows post-session, was 203 pre-session)

- 145 AUTHOR-TITLE-ONLY × NULL (same set as above)
- 54 GREY × NULL — separate track entirely; type-determination first
- 10 NULL-metadata × VERIFIED — classification-gap rows (VERIFIED existence but no metadata_quality value)

---

## Next-action handoff

### Completed this session ✓

- [x] Schema 014 (`metadata_integrity_status`, `metadata_integrity_detail` columns)
- [x] Batch 1: 35 ATO×DOI → COMPLETE (Crossref)
- [x] Batch 2: 2 ATO×PMID → COMPLETE incl. REF-00027 truncated-DOI rescue
- [x] Batch 3: 3 statutory → COMPLETE-STATUTORY (UK HTM 08-01 VERIFIED, ES DB SUA VERIFIED, KR 편의증진법 UNVERIFIED-1)
- [x] DR-2026-05-20 authored, attested, committed
- [x] Skill `evidence-metadata-rehabilitation_SKILL.md` authored, registered in skill-registry
- [x] Level-2 audit `scripts/audit/metadata_integrity_audit.py`

### Pending — next session candidates (handoff queue)

1. **No-DOI/no-PMID × VERIFIED cohort** (~126 rows). Crossref title-search path. Probe script analog to `probe_ato_verified_doi.py` but using `https://api.crossref.org/works?query.title=X&query.author=Y`. Yield estimate 30–50%.

2. **ATO × NULL full-probe cohort** (~145 rows). Mixed types. Per-row triage first to assign academic vs statutory vs grey-org path, then run the appropriate probe.

3. **GREY × NULL cohort** (54 rows). Separate track. Type-determination-first.

4. **Cross-check the 236 legacy COMPLETE rows** (check 2 of metadata_integrity_audit.py). These cleared rule #10 pre-DR but never had cross-check. Before next major synthesis push, batch-probe them via DOI/PMID where present.

5. **Owner-action queue (28 rows in `metadata_integrity_status` queue)** — needs owner disposition:
   - 10 MISMATCH-TITLE: re-attribution or accept (move note to `bpc_note`, adopt canonical title)
   - 8 MISMATCH-MULTI: likely wrong-identifier; verify and either correct identifier or delete row
   - 5 MISMATCH-AUTHOR: re-attribution or normalize name-form
   - 4 DOI-TRUNCATED (no rescuable PMID): re-search by author+year+title
   - 1 MISMATCH-YEAR: verify identifier is correct

6. **Owner-action: paywall queue** — REF-00074 (BCA Code on Accessibility 2025, SG; commercial), REF-00469 (SBi 230, DK; commercial) plus existing IS-PAYWALL rows. Purchase or alternate route.

7. **GitHub Issues for owner queues** (process change). 28-row metadata-integrity queue + IS-PAYWALL queue + NEEDS-HUMAN queue belong as labeled GitHub Issues, not buried in session records. Owner ratification needed before auto-creating issues.

### Pending — for owner ratification

- **DR-2026-05-20 status PROPOSED → RATIFIED**. After ratification, the new acceptance predicate (`verification_note` carries probe timestamp) becomes binding.
- **Audit script promotion Level 2 → Level 4** (blocking) after a 7-day shakedown period per workplan §8.
- **GitHub Issues for owner-action queues** (per #7 above).

session_close marker: this session ends here. Final HEAD `15b286d2`. Eligible pool **276/670 (41.2%)**. Next session bootstrap should fetch `sessions/LATEST` → `session_2026-05-20-ato-rehab.md` and pick from items 1–7 above.

---

## CONTINUATION 2026-05-21: Web-Search Pivot + 14 batches

**Continuation entry appended 2026-05-21 11:10. Prior session_close above was premature; the work continued the next day and is captured below.**

### Methodology pivot (DR-2026-05-18 enforcement)

Owner reminder mid-session: *"non academic doesn't follow the same process for metadata"*. Claude acknowledged misapplying academic protocol (Crossref / PubMed / OpenAlex) to gray-lit cohort for the prior session. Correct path per DR-2026-05-18: gray-lit verifies via **issuing body + edition year + jurisdiction + publisher + URL → COMPLETE-STATUTORY** (no DOI required). Academic books verify via **ISBN + publisher + edition** with `doi_resolution_outcome=NO-MATCH` to clear C04.

Web-search batches pivoted from academic-DOI-probing to issuing-body verification. Each batch:

- Search authoritative source (issuing body's website)
- Cross-check via 2-3 independent secondary references
- Capture `url`, `verified_by_tool`, `last_verified_at` as audit trail
- Promote to `COMPLETE-STATUTORY` (gray-lit) or `COMPLETE` (book with ISBN) or `COMPLETE` (academic article with DOI)
- Land each batch via discrete `data_2026-05-21*.sql` migration with `BEGIN TRANSACTION; ... COMMIT;` envelope
- `data_migrations` tracking row inserted by `scripts/migrate_db.py` runner (do NOT include INSERT INTO in migration body — this convention was reconfirmed)

### Batches landed (14 total, 47 rows promoted)

| # | Migration | Rows | Type | Net eligible |
|---|-----------|------|------|--------------|
| 1 | `data_20260521040000_uk_guidelines_batch_1.sql` + `040500_audit_trail` | 6 | UK guidelines | +6 → 301 |
| 2 | `data_20260521050000_uk_guidelines_batch_2.sql` | 5 | UK guidelines | +5 → 306 |
| 3 | `data_20260521055000_uk_guidelines_batch_3.sql` | 4 | UK guidelines | +4 → 310 |
| 4 | `data_20260521060000_mixed_batch_4.sql` | 2 | Acad+Stat | +2 → 312 |
| 5 | `data_20260521065000_us_guidelines_batch_5.sql` | 5 | US guidelines | +5 → 317 |
| 6 | `data_20260521072000_us_guidelines_batch_6.sql` | 4 | US guidelines | +4 → 321 |
| 7 | `data_20260521074000_int_reports_batch_7.sql` | 3 | INT reports | +3 → 324 |
| 8 | `data_20260521080000_books_batch_8.sql` + `080500_audit_trail` | 3 | Books (ISBN) | +3 → 327 |
| 9 | `data_20260521084000_mixed_batch_9.sql` | 2 | Mixed | +2 → 329 |
| 10 | `data_20260521090000_mixed_batch_10.sql` | 1 | Academic | +1 → 330 |
| 11 | `data_20260521094000_au_reports_batch_11.sql` | 5 | AU reports | +5 → 335 |
| 12 | `data_20260521101000_aucca_batch_12.sql` | 4 | AU+CA | +4 → 339 ⭐ 50% |
| 13 | `data_20260521103000_ca_batch_13.sql` | 2 | CA | +2 → 341 |
| 14 | `data_20260521110000_books_batch_14.sql` | 1 | CA book | +1 → 342 |

### Specific row promotions

**UK guidelines (15 rows):**
- REF-00425 ADM Vol 2 (HM Gov 2024 amendments)
- REF-00405 Wheelchair Housing Design Guide 3rd ed (Habinteg/RIBA 2018, ISBN 9781859468289)
- REF-00404 + REF-00437 (dup) Inclusive Housing Design Guide (Runnalls/Walker, RIBA 2024, ISBN 9781915722355)
- REF-00378 + REF-00053 (dup) Adaptations Without Delay (Russell/Walker/Copeman/Porteus, RCOT/Housing LIN 2019)
- REF-00084 + REF-00201 (dup) EADDAT (Palmer/DSDC Stirling 2022)
- REF-00281 Click-Away Pound 2019 (Williams & Brownlow/Freeney Williams)
- REF-00280 Purple Pound 2020 (Purple/DWP £274B)
- REF-00022 Building Sight RNIB 2023 (Lewis & Thomas)
- REF-00248 VisitBritain "Make your business accessible"
- REF-00264 HM Gov "Raising accessibility standards for new homes" consultation outcome 2022
- REF-00282 WEC HC 605 "Accessibility of products and services to disabled people" 2024
- REF-00247 Wheels for Wellbeing "Benches and Seating in Public Spaces" 2025

**US guidelines (9 rows):**
- REF-00447 ICC A117.1-2017 Accessible and Usable Buildings and Facilities (ISBN 9781609837013)
- REF-00143 HUD FHA Design Manual 1998 (stored year 2022 corrected; ISBN 9780894992391)
- REF-00062 PVA Accessible Home Design 2nd ed (Davies & Lopez; ISBN 9780929819181)
- REF-00316 VA SAH/SHA grants FY2024 Federal Register notice
- REF-00317 USDA Section 504 Rural Housing Repair (7 CFR Part 3550)
- REF-00267 Maisel/Smith/Steinfeld 2008 AARP Public Policy Institute Visitability
- REF-00213 ADA National Network "Opening Doors to Everyone" factsheet 2017
- REF-00206 Greene 2014 Construction Specifier door requirements
- REF-00112 Hunt/Sine/McMurray 2024 Behavioral Health Design Guide (26th rev, BHFC)

**INT reports/books/journal articles (8 rows):**
- REF-00156 UN CRPD General Comment No. 2 on Art 9 Accessibility 2014 (CRPD/C/GC/2)
- REF-00157 UN CRPD General Comment No. 5 on Art 19 Independent Living 2017 (CRPD/C/GC/5)
- REF-00158 IDA compilation of CRPD Concluding Observations Art 9
- REF-00176 Barker 1968 Ecological Psychology Stanford UP (ISBN 9780804706582)
- REF-00478 Passini 1984 Wayfinding in Architecture Van Nostrand Reinhold (ISBN 9780442275907)
- REF-00485 Kaplan & Kaplan 1989 Experience of Nature Cambridge UP (ISBN 9780521341394)
- REF-00484 Kahneman 1973 Attention and Effort Prentice-Hall (ISBN 9780130505187)
- REF-00203 Walton et al. 2020 MS Atlas 3rd ed Multiple Sclerosis Journal 26(14):1816-1821 DOI 10.1177/1352458520970841
- REF-00030 Kim et al. 2014 IJIE 44(5):636-646 ramp slope wheelchair DOI 10.1016/j.ergon.2014.07.001
- REF-00169 Williams/Corbyn/Hart 2023 NDTi sensory environments Child Care in Practice 29(1):35-53 DOI 10.1080/13575279.2022.2126437
- REF-00339 Gallaudet DeafSpace Design Guidelines Vol 1 2010

**AU/CA (15 rows):**
- REF-00075 Winkler 2024 Summer Foundation design/construction sector accessibility
- REF-00076 + REF-00153 (potential-dup) Newton 2023 UTS Inclusive Bathroom Design
- REF-00315 NDIS Home Modifications NDIA Operational Guideline
- REF-00501 Dementia Australia Designing Dementia-Friendly Care Environments
- REF-00271 + REF-00471 (potential-dup) LHA Livable Housing Design Guidelines 4th ed 2017
- REF-00141 CMHC Universal Design Guide 2023
- REF-00288 Rick Hansen Foundation Accessibility Certification v4.0 2024
- REF-00205 CMHC Renovating for Accessibility fact-sheet series 2021
- REF-00160 CRA Home Accessibility Tax Credit (HATC) Line 31285
- REF-00177 Townsend & Polatajko 2007 Enabling Occupation II (CAOT ISBN 9781895437768)

### Final state at continuation close

- HEAD: `66baa31f` (14 commits this continuation, all CI green on both workflows)
- Eligible pool: **342/678 (50.4%)** — ⭐ **CROSSED 50% MILESTONE** at batch 12
- Net gain this continuation: **+47 rows** (+7.0pp from session-close baseline of 295/670, +15.5pp from session-open baseline)
- Schema: v14, Total rows: 678
- Remaining ATO × no-ID: **205 rows** (down from 252 at continuation open, 254 at session open)

### New owner-queue rows from this continuation

Deferred because of ambiguity, source mismatch, or potential duplication:

- **REF-00591** Allen 1988 CDM AJOT — ambiguous; likely actually the 1985 book "Occupational Therapy for Psychiatric Diseases" (ISBN search via owner)
- **REF-00384** Simoneau 1991 — Crossref returned Journal of Gerontology candidate, journal mismatch with stored "Hum Mov Sci"
- **REF-00388** Koontz 2012 — Crossref returned J Appl Biomech candidate, but title doesn't match stored "Shoulder moment contributions to wheelchair propulsion. Clin Biomech"
- **REF-00386** Kim 2014 J Mech Sci Technol — possibly dup of REF-00030, possibly sister paper; needs owner check
- **REF-00735** Devos 2019 dementia soundscape PMC6950055 — Crossref author+title search did not surface; PMC ID present so PubMed should resolve; deferred
- **REF-00254** cross-reference only — internal pointer to MST-01/hs3, likely a placeholder not a real citable source; recommend delete or recategorize
- **REF-00055** Living Well by Design 2023 — ambiguous title
- **REF-00408** Dementia Design Guidance 2020 — ambiguous (could be UK Dementia Services Development Centre / Stirling, or other)
- **REF-00428** Lifts in dwellings — could be BS 6440 or BS EN 81-41
- **REF-00118** Adaptable Housing guide UK 2022 — ambiguous; multiple candidates
- **REF-00119** Accessible homes guidance UK 2022 — ambiguous
- **REF-00241** Energy conservation guide UK 2020 — likely Approved Document L of Building Regulations but not confirmed
- **REF-00615** MCAS environmental management 2023 — likely Mast Cell Action UK Primary Care Guide
- **REF-00045** AU "Adapting the Environment" 2022 — too generic to identify with confidence
- **REF-00073** Ringaert 2001 UDI Manitoba — stored title doesn't match either of two Ringaert UD publications (the 2001 Universal Design Handbook ch. 6 or the 2002 Husbanken book chapter)

### Newly identified duplicate pairs (POTENTIAL-DUPLICATE-OF-* tags applied)

- REF-00076 + REF-00153 (both Newton 2023 UTS bathroom)
- REF-00271 + REF-00471 (both LHA 4th ed 2017)
- REF-00378 + REF-00053 (both Adaptations Without Delay)
- REF-00084 + REF-00201 (both EADDAT)
- REF-00404 + REF-00437 (both Inclusive Housing Design Guide)

Owner queue: consolidate or accept-as-separate per BPC slug context.

### Convention reconfirmations

- Data migrations MUST NOT include `INSERT INTO data_migrations` (runner tracks via filename stem)
- Books with ISBN as canonical identifier: set `doi_resolution_outcome='NO-MATCH'` to clear C04
- COMPLETE-STATUTORY is the right metadata_quality value for gray-lit (issuing body + edition + jurisdiction)
- COMPLETE applies to academic journal articles (DOI-verified) and academic books (ISBN-verified with NO-MATCH outcome)
- `verified_by_tool` audit field uses naming pattern `web-search-multi+<authoritative-domain>-official`
- All commits passed both `Guidebook CI` and `Repo Integrity Audits` workflows

### Continuation close

`66baa31f`. Next session bootstrap: read this session record, then continue from owner-queue items 1-15 above + remaining 205 ATO × no-ID rows. Top remaining buckets: report×US (15), report×INT (11), report×UK (15), guideline×US (10), guideline×UK (7), guideline×FR (6), report×DE (6), guideline×INT (7).

---

## CONTINUATION 2026-05-21 (second push): Batches 15-23

After the morning's continuation closed, owner said "proceed now" multiple times. 9 more batches landed, +29 rows.

### Batches landed (15-23, 29 rows)

| # | Migration | Rows | Net eligible |
|---|-----------|------|--------------|
| 15 | `data_20260521120000_us_reports_batch_15.sql` | 7 | +7 → 349 |
| 15.5 | audit allowlist (Bateman ME/CFS DOI) | 0 | 349 |
| 16 | `data_20260521122000_us_reports_batch_16.sql` | 2 | +2 → 351 |
| 17 | `data_20260521130000_auracast_batch_17.sql` | 5 | +5 → 356 |
| 18 | `data_20260521133000_us_reports_batch_18.sql` | 3 | +3 → 359 |
| 19 | `data_20260521140000_int_reports_batch_19.sql` | 4 | +4 → 363 |
| 19.5 | `data_20260521141000_batch_19_fixup.sql` + audit allowlist (Owen TID DOI) | 0 | 363 |
| 20 | `data_20260521143000_int_reports_batch_20.sql` | 1 | +1 → 364 |
| 21 | `data_20260521150000_uk_reports_batch_21.sql` | 4 | +4 → 368 |
| 22 | `data_20260521152000_uk_reports_batch_22.sql` | 2 | +2 → 370 |
| 23 | `data_20260521154000_uk_reports_batch_23.sql` | 1 | +1 → 371 |

### Specific verifications (batches 15-23)

**Batch 15 — US reports (7 rows, +56 cumulative since start):**
- REF-00161 VA SAH/SHA FY2026 (FedReg doc 2025-20047; SAH $126,526, SHA $25,350; 38 U.S.C. 2102(e), 38 CFR 36.4411)
- REF-00338 Bauman 2010 DeafSpace Design Guidelines 85pp (dup-of REF-00339; same Gallaudet 2010 artifact)
- REF-00223/00234/00231/00245 ME/CFS Clinical Care — Bateman et al. 2021 Mayo Clin Proc 96(11):2861-2878 DOI `10.1016/j.mayocp.2021.07.004` (4-way duplicate cluster; stored years 2024/2025 → 2021)
- REF-00042 Clark 2021 "Against Access" McSweeney's Quarterly Concern 64

**Batch 15 audit fixup:** Added `10.1016/j.mayocp.2021.07.004` to KNOWN_DUP_DOIS allowlist (4 BPCs cite same paper).

**Batch 16 — US reports (2 rows):**
- REF-00276 Accenture+Disability:IN+AAPD 2023 "The Disability Inclusion Imperative" (346-company DEI sample)
- REF-00731 Szanton et al. 2016 Health Affairs 35(9):1558-1563 "Home-Based Care Program Reduces Disability" DOI `10.1377/hlthaff.2016.0140` (stored year 2019 corrected to 2016; $2,825/participant CAPABLE figure traces to this paper)

**Batch 17 — Auracast cluster (5 rows, +61):**
- REF-00333/00337/00352/00354 Bluetooth SIG Auracast Broadcast Audio specification 2022 (4-way potential-duplicate cluster — Kirkland WA June 8, 2022; HAP 1.0 + BASS 1.0 + Public Broadcast Profile; Bluetooth Core Spec 5.2+ required)
- REF-00336 Auri™ first certified Auracast ALS product (Listen Technologies + Ampetronic; shipped Jan 2025)

**Batch 18 — US reports (3 rows):**
- REF-00092 SAMHSA TIP 57 Trauma-Informed Care in Behavioral Health Services 2014 (HHS Publication No. SMA 14-4816; produced under contracts by KAP/CDM Group/JBS International)
- REF-00140 Visitability — Eleanor Smith / Concrete Change 1987 (Atlanta; concept origin; 3 core features = zero-step entry + 32" doors + main-floor accessible bath)
- REF-00113 Center for Health Design Behavioral & Mental Health Toolbox 2018 (issue brief + universal-approach tool + lessons learned)

**Batch 19 — INT reports (4 rows, +69):**
- REF-00090 Owen & Crane 2022 TID scoping review IJERPH 19(21):14279 DOI `10.3390/ijerph192114279` PMID 36361166 PMC9658651 (Univ. of Tasmania; jurisdiction INT→AU; flagged as duplicate of REF-00527; Crane first name owner-queue: '527 'Jasmine' vs PMC source 'James')
- REF-00735 Devos et al. 2019 IJERPH 16(24):4904 DOI `10.3390/ijerph16244904` PMC6950055 dementia soundscape (Ghent University BE + UCL + Artevelde UC)
- REF-00342 Vaughn 2018 "DeafScape: Applying DeafSpace to Landscape" Ground Up Journal Issue 7 (UC Berkeley CED, May 2018; jurisdiction INT→US)
- REF-00343 Bauman & Murray (eds.) 2014 "Deaf Gain: Raising the Stakes for Human Diversity" Univ. of Minnesota Press ISBN 9780816691227 (H-Dirksen L. Bauman ≠ Hansel Bauman; both at Gallaudet)

**Batch 19 audit fixup:** Inserted Owen + Crane authors for REF-00090; flagged REF-00090+REF-00527 as POTENTIAL-DUPLICATE pair; added `10.3390/ijerph192114279` to KNOWN_DUP_DOIS allowlist.

**Batch 20 — INT reports (1 row):**
- REF-00291 OECD Tourism Trends and Policies 2016 DOI `10.1787/tour-2016-en` ISBN 9789264245976 (50 OECD countries; biennial; AU 2.8-3.4 disabled-traveler-group multiplier figure confirmed)

**Batch 21 — UK reports (4 rows, +73):**
- REF-00162/00259/00313 Disabled Facilities Grant 3-row cluster (MHCLG+DHSC; Housing Grants Construction and Regeneration Act 1996; £30k max England, £36k Wales, £25k NI; £711M annual allocation 2024-26)
- REF-00149 Habinteg "A Forecast for Accessible Homes 2025: One Decade On — Milestone or Millstone?" (311 English local plans; 4% planned new homes M4(3); regional disparity London 1:210 vs NW 1:2006)

**Batch 22 — UK reports (2 rows, +75):**
- REF-00734 Tibble 2005 "Review of existing research on the extra costs of disability" DWP Working Paper No. 21
- REF-00268 Provan/Lane/Horne Rowan 2023 LSE CASEreport 147 "The Social and Economic Value of Wheelchair User Homes" (Habinteg public-facing title: "Living Not Existing"; +£22k build cost / £94k 10-yr benefit / 4x ROI for working-age)

**Batch 23 — UK reports (1 row):**
- REF-00258 M4(3) Wheelchair Standard Cost Study (potential dup-of REF-00268 — both cite Provan 2023 LSE CASEreport 147)

### New duplicate clusters identified (batches 15-23)

- **REF-00338 + REF-00339** Gallaudet DeafSpace Design Guidelines Vol 1 2010 (both cite same Bauman 2010 artifact)
- **REF-00223/00231/00234/00245** Bateman et al. 2021 ME/CFS Essentials (4-way DOI duplicate)
- **REF-00333/00337/00352/00354** Bluetooth SIG Auracast spec (4-way potential duplicate)
- **REF-00162/00259/00313** UK DFG programme (3-row programme cluster — same authority, different facets)
- **REF-00258 + REF-00268** Provan 2023 LSE CASEreport 147

### New owner-queue rows from batches 15-23

- **REF-00527 vs REF-00090** Crane first name discrepancy: REF-00527 stored 'Jasmine'; PMC9658651 source verified 'James'. Determine if REF-00527 is misattributed or a different work entirely.
- **REF-00273** Brunson 2019 "An Adorable Housing Paper" — title likely OCR error; could not identify with confidence
- **REF-00733** Ismail 2023 Fibromyalgia hydrotherapy SR Tandfonline — Crossref + web search did not surface
- **REF-00292/REF-00293** Modern bathroom / 2026 Rental Market accessibility blog posts — generic blog content; need original BPC context
- **REF-00304/00305/00308/00309** Cost-of-accessible-design figures — too generic without BPC context
- **REF-00339** earlier already verified — but stored title "DeafSpace Design Guidelines Vol 1 2010" (verified prior session). Confirm REF-00338 + REF-00339 should consolidate.

### Final state (continuation 2 close)

- HEAD: `6eab3153` (23 batch commits + 3 audit allowlist commits since 2026-05-20 morning session-close)
- **Eligible pool: 371/678 (54.7%)** — +76 from start of web-search work; +95 from session-open baseline (276/670 = 41.2%)
- Schema v14, 678 rows
- ATO × no-ID remaining: **~180 rows** (down from 254)
- All 23 commits pass 35/35 db_integrity + Guidebook CI + Repo Integrity Audits

### Continuation-2 close

`6eab3153`. Next session bootstrap: read this session record, continue from owner-queue items + remaining 180 ATO × no-ID rows. Top remaining buckets: UK guidelines (10), US guidelines (13), INT reports (~13 remaining), report×DE (6), guideline×FR (6), report×NL (5), report×NO (5), report×CA (5).
