# Website Preparation — Tactical Reference
**Version:** 3.0 (excised 2026-05-08)
**Canonical plan:** workplan-co0007-v4.md (ADOPTED 2026-05-03)
**This file provides:** tactical procedures referenced by v4 C-stages. Not a standalone workplan.
**Stale content excised to:** workplan/deprecated/website-preparation-stale-2026-05-08.md
**Original:** website-preparation.md v2.0 (2026-04-17). Phase A Block sequencing, Phase B tech stack, session estimates, and gap register superseded by v4.

---

## 1. Glossary

| Term | Meaning |
|---|---|
| **BPC** | Best Practices Compendium — per-topic research files in `references/bpc/{topic}/{slug}.md` |
| **FDR** | Functional Deficit Researcher — skill that generates specifications from ICF functional needs |
| **ISW** | Item Specification Writer — skill that produces Part 4 item spec entries |
| **Opus synthesis** | Cross-evidence judgment produced by Opus sessions; Sonnet never determines best practice |
| **CO-0006** | Change Order that established BPC Key sources REF-ID schema |
| **REF-ID** | Sequential integer (01, 02, …) identifying a source within a single BPC entry's Key sources table |
| **CON-ID** | Global connection identifier (CON-0001 through CON-0248+) |
| **GRADE** | Grading of Recommendations Assessment, Development and Evaluation — evidence confidence framework |
| **Co-1** | First-tier lived experience evidence (CRPD Art. 4.3 aligned) |
| **DAR** | Design for Adaptable Readiness |
| **Universal Mode/1/2** | Universal / Population-informed / Person-specific design hierarchy |

---

## 2. BPC CO-0006 Migration Pipeline (per file)

Referenced by v4 C1 (migration tooling) and C7 (evidence base). This is the tactical per-file procedure for migrating BPC Key sources from flat lists to CO-0006 REF-ID table format.

```
1. READ current BPC file
2. EXTRACT existing Key sources section (flat list or partial table)
3. IDENTIFY each source: authors, year, title, publisher, DOI/URL, tier, language, jurisdictions
4. NORMALIZE into CO-0006 table rows with sequential REF-IDs (01, 02, 03...)
5. VALIDATE: every source has all required fields (or [GREY] for missing DOI)
6. WRITE new Key sources section replacing old
7. UPDATE corresponding search-log disposition field
8. ATOMIC COMMIT: BPC + search-log in same commit (co-file rule)
9. VALIDATE: run validate_bpc.py locally before commit
10. CI RUN: confirms structure gate passes
```

**Error handling:**
- Source has missing fields → [GREY] placeholder + gap register entry GAP-CITE-NNN
- Source cannot be parsed → session-local blocker, move to next file, flag in session close
- validate_bpc.py fails → fix inline, re-commit
- Tier classification ambiguous → default to lowest applicable tier, flag for Opus review

**Per-session checkpoint:**
- [ ] All files in session's batch migrated
- [ ] CI green on all session commits
- [ ] Search-log dispositions updated
- [ ] Session log records: files migrated, REF-IDs assigned, gaps raised

**CO-0006 / CO-0008 bridge note (2026-05-08):** This pipeline produces CO-0006-compliant BPC markdown tables. These tables feed the website parser (p11_sources) and `convert_bpc_metadata.py`. They do NOT automatically populate CO-0008's global-reference-registry.json → data/evidence_sources/ YAML pipeline. A bridge script (`convert_bpc_sources.py`) is needed to close this gap. See workplan-reconciliation-2026-05-08.md §7.

---

## 3. Transition Criteria (programmatic)

From original §6. `scripts/check_phase_a_complete.py` implements these checks. Some are superseded by v4's data-layer approach but the script is still in CI and the checks remain useful diagnostics.

```bash
# Run from guidebook repo
python3 scripts/validate_bpc.py --all                    # BPC files valid
python3 scripts/validate_cross_refs.py                   # no broken references
python3 scripts/check_phase_a_complete.py                # all criteria below
```

| # | Criterion | v4 status |
|---|---|---|
| A1 | ≥95% BPC files have CO-0006 Key sources table | Still valid — C1/C7 dependency |
| A2 | spec-db-part4-reconciliation.md exists | COMPLETE |
| A3 | gap_register.md + gap_register_archive.md both exist | COMPLETE (2026-05-08) |
| A4 | Part 4 items valid (no duplicate codes, 88-95 range) | Still valid — C3 dependency |
| A5 | Standards registry ≥80 entries | Still valid |
| A6 | Parser source readiness PASS | Pending v4 C1 parser reconciliation |
| A7 | Part 4 HTML annotations present (≥90 each) | Still valid — C3 dependency |
| B1 | Connections CONSUMED ≥182, PENDING=0 | Still valid — C3 dependency |
| B2 | Priority SRs referenced in BPC | Still valid |
| B3 | GRADE annotations ≥40 | Still valid — C3 dependency |
| B5 | Hallucination audit exists | Still valid |

---

## 4. Error Management

### Session-local errors
Fix within session. Log in session close YAML. No gap register entry needed unless recurring.

### Cross-session errors
Raise gap register entry (P1 if blocks next stage, P2 otherwise). Session-consolidator propagates blocker through sessions until closed.

### Architectural errors
If a stage checkpoint fails in ways the gap register cannot resolve: stop, revise workplan (new version), resume. Do not execute further stages.

### Rollback protocol
- **Session-level:** `git revert <commit_oid>`. Session-consolidator records the revert.
- **Stage-level:** Tag `stage-N-broken-YYYYMMDD` → branch from last good commit → cherry-pick surviving work → merge via PR (CI must pass). Document lessons learned.
- **Never:** delete commits, force-push, modify shared history.

### Hallucination prevention (citation migration)
- Every REF-ID entry must cite a source from the original BPC's flat Key sources list. No new sources invented during migration.
- DOIs/URLs must be verifiable — if not in original BPC, mark [GREY] rather than fabricate.
- validate_bpc.py can cross-check REF-ID count against original list length.
