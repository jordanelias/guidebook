# Session record: 2026-05-20 — AUTHOR-TITLE-ONLY × DOI rehabilitation pilot + schema 014

**Session ID:** `session_2026-05-20-ato-rehab`
**Span:** 2026-05-20 ~20:00 UTC → 2026-05-20 ~20:45 UTC
**Bootstrap version:** PI v10.14 + architecture v2.3 + userPreferences v6.3
**Pilot artifact:** Crossref-based metadata rehabilitation for AUTHOR-TITLE-ONLY × VERIFIED × DOI cohort
**Outcome:** Eligible pool 236 → 271 (35.2% → 40.4%, +5.2pp); AUTHOR-TITLE-ONLY 312 → 277; schema migration 014 adds explicit metadata-integrity tracking; CI regression introduced + diagnosed + fixed within session; both workflows green on `66dc69e9`.

---

## Headline outcomes

| Metric | Pre-session | Post-session | Δ |
|---|---|---|---|
| Eligible pool (rule #10) | 236 (35.2%) | 271 (40.4%) | +35 (+5.2pp) |
| AUTHOR-TITLE-ONLY | 312 | 277 | −35 |
| COMPLETE | 147 | 182 | +35 |
| metadata_integrity_status flags | none (column didn't exist) | 35 OK + 18 MISMATCH-* + 6 DOI-TRUNCATED | new tracking dimension |
| Schema version | 13 | 14 | +1 |
| Both CI workflows green on HEAD | ✓ (`75158a9b`) | ✓ (`66dc69e9`) | held; mid-session red on `ad92e95c` |

---

## Commits in chronological order

1. `d9253768` — governance: schema 014 add metadata_integrity_status + metadata_integrity_detail columns
2. `ad92e95c` — evidence-metadata-rehabilitation: ATO-DOI rehab batch 1 (collapsed commit, amended message describes contents honestly) — **broke CI on push** (commit-msg format + migration reproducibility)
3. `66dc69e9` — evidence-metadata-rehabilitation: strip self-insert from batch 1 migrations — runner handles data_migrations tracking; restores --rebuild parity (GAP-290 CI fix) — **CI back to green**

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
NULL                          611
OK                            35
MISMATCH-TITLE                7
DOI-TRUNCATED                 6
MISMATCH-MULTI                5
MISMATCH-AUTHOR               5
MISMATCH-YEAR                 1
```

24 holds queryable as `WHERE metadata_integrity_status NOT IN ('OK', 'RESOLVED', NULL)`. This is the owner-review queue.

---

## Known broken / pending work

### Owner-review queue: 24 metadata-integrity holds

Queryable: `SELECT ref_id, metadata_integrity_status, metadata_integrity_detail FROM evidence_sources WHERE metadata_integrity_status LIKE 'MISMATCH%' OR metadata_integrity_status LIKE 'DOI-%' ORDER BY metadata_integrity_status;`

By type:
- **MISMATCH-TITLE (7 rows)** — `pub_title` is a citation shorthand; canonical title at DOI differs. Resolution: confirm DOI is correct, move existing text to `bpc_note`, replace `pub_title` with canonical.
- **DOI-TRUNCATED (6 rows)** — stored DOI is publisher-prefix fragment. Resolution: re-search by author+year+title for full DOI.
- **MISMATCH-MULTI (5 rows)** — multiple-field disagreement, likely wrong DOI entirely.
- **MISMATCH-AUTHOR (5 rows)** — surname mismatch. Possible misattribution.
- **MISMATCH-YEAR (1 row)** — year off by >1; possible misattribution.

### Remaining AUTHOR-TITLE-ONLY cohort (277 rows)

- 128 VERIFIED × no-DOI (16 have PMID — PubMed-resolution pilot is the natural next batch)
- 149 NULL × all types (full V2-manual-equivalent probe needed)

### Remaining NULL verification (149 rows after this session — went from 203 to 149)

- 149 AUTHOR-TITLE-ONLY × NULL (overlap with above)
- 54 GREY × NULL (different track entirely)

### 10 NULL-metadata × VERIFIED

Classification gap — VERIFIED but no `metadata_quality` value. Out of scope this session.

---

## Next-action handoff

1. **Pilot batch 2 — PMID→PubMed resolution.** 16 AUTHOR-TITLE-ONLY × VERIFIED × has-PMID rows. Mirror the probe_ato_verified_doi.py pattern against NCBI EUtils. Expected yield ~50–60% upgrade based on academic-source distribution. If mismatch rate is similar to DOI cohort (~31%), this confirms the note-as-title pattern is systemic.

2. **Pilot batch 3 — statutory cohort.** 7 `source_type=standard` × NULL rows + ~40 statutory-looking guidelines. V2-manual probe protocol with COMPLETE-STATUTORY target.

3. **Skill promotion candidate.** After batches 2 + 3 validate the type-routed protocol across ≥3 cohorts (academic-DOI, academic-PMID, statutory), promote to `skills/evidence-metadata-rehabilitation_SKILL.md`. Companion audit script `scripts/audit/metadata_integrity_audit.py` (level 2 → 4 after shakedown) checks for note-as-title and truncated-DOI patterns on new sources at ingest.

4. **DR candidate** — methodology refinement based on the note-as-title finding + truncated-DOI finding. Author after batch 2 confirms the pattern is academic-cohort-wide. Establish that ATO→COMPLETE upgrades MUST run cross-check, not silent metadata-import.

5. **GitHub Issues for owner-review queues** (process change, owner-ratification needed). Move IS-PAYWALL (18), NEEDS-HUMAN (2), metadata-mismatch (18), truncated-DOI (6) from session records to labeled GitHub Issues. Persists across sessions; doesn't bury in handoff text.

6. **NULL queue not in AUTHOR-TITLE-ONLY** — 54 GREY × NULL + 10 NULL-metadata × VERIFIED. These belong to different verification tracks; not on this session's protocol.

session_close marker: this session ends here. Next session bootstrap should fetch `sessions/LATEST` → `session_2026-05-20-ato-rehab.md` and pick from items 1–6 above.
