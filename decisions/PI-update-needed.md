# PI Deployment Queue

**Live in claude.ai project settings:** v10.11 (deployed by owner sometime between session_2026-05-13b close and session_2026-05-15a; the present-session prompt loads v10.11, confirming deployment).
**Pending deployment:** v10.12 (drafted in session_2026-05-15a).

---

## v10.13 — Pending (NEW, blocks Pass 3)

**Status:** Not yet drafted as `governance/project-instructions-v10_13.md`. Awaits v10.12 deployment first; v10.13 supersedes v10.12 cumulatively when authored.
**Trigger:** DR-2026-05-18 statutory-metadata-completeness (adopted 2026-05-18 in session_2026-05-17-pilot-pass-3-blocker-resolution).
**Action:** Standing rule #10 eligibility predicate text must be amended.

### What changes

Standing rule #10 currently reads:

> Required minimum: `metadata_quality = COMPLETE` AND `verification_status ∈ {VERIFIED, UNVERIFIED-1}`.

Amend to:

> Required minimum: `metadata_quality ∈ {COMPLETE, COMPLETE-STATUTORY}` AND `verification_status ∈ {VERIFIED, UNVERIFIED-1}`. The `COMPLETE-STATUTORY` value (introduced 2026-05-18 per DR-2026-05-18) certifies that a statutory document (standard, guideline) carries the metadata fields appropriate to its source type — issuing body, edition year, jurisdiction, and standard number or publisher — rather than the academic-publication fields (DOI, journal, page range, named authors) the unqualified `COMPLETE` requires. Both values clear the existence gate; they remain queryably distinct for audit purposes.

### Why this is blocking

PI v10.11 / v10.12 rule #10 reads strictly `metadata_quality = COMPLETE`. Until v10.13 deploys, any Pass 3 work citing a `COMPLETE-STATUTORY` source is operating under a rule-bend that is documented in the DR but not yet ratified in the live PI text. The bend is defensible (DR adopted; data already promoted) but creates rule/code drift per architecture v2.3 `<conflict_resolution>` row 4 (text rule vs CI workflow) — though here the CI predicate has already been updated in `scripts/audit_evidence_metadata.py`, so the inverse: code is ahead of text.

### Owner action

- [ ] After v10.12 deploys, draft v10.13 as a minimal patch (single rule-#10 text amendment + changelog entry)
- [ ] Paste into claude.ai → Project Settings → Custom Instructions
- [ ] Verify version line reads `V10.13 · Revised 2026-05-18`

### Until ratified

Pass 3 work this pilot session may proceed citing COMPLETE-STATUTORY sources because (a) DR-2026-05-18 is adopted, (b) the eligibility predicate is updated in code, (c) the rule/text drift is acknowledged here. Each Pass 3 row referencing a COMPLETE-STATUTORY source carries an implicit `[DRIFT: rule-#10 text vs code — DR-2026-05-18 adopted, PI v10.13 not yet deployed]` tag that becomes explicit in the audit trail if surfaced for review.

---

## v10.12 — Pending

**Status:** v10.12 drafted at `governance/project-instructions-v10_12.md` @ session_2026-05-15a.
**Action:** Owner manually pastes v10.12 content into claude.ai → Project Settings → Custom Instructions when convenient.

### What changed vs live v10.11

Single-purpose patch.

- **Bootstrap pattern fix.** Replaced `echo "Skills: $(grep -c '^### ' /tmp/registry.md) registered"` (matched 0 against current registry shape) with a backend-aware `_GH_SKILLS()` helper that counts `skills/*_SKILL.md` files via the GitHub contents API and excludes `skills/deprecated/`. Helper added to both `gh` and `curl` backend blocks (lines 175 and 184 in v10.11 source). Status-block label `Skills: X registered` → `Skills: X active`.
- **Changelog entry** for v10.12 added at top.
- **No standing-rule changes.** No `<skills_assigned>` changes. No structural removals or renames — no caller-sweep required.

### Owner action

- [ ] Open claude.ai → Project Settings → Custom Instructions
- [ ] Replace live PI (currently v10.11) with content of `governance/project-instructions-v10_12.md`
- [ ] Verify version line reads `V10.12 · Revised 2026-05-15`
- [ ] Save; next chat will bootstrap under v10.12 and the `Skills: X active` line will show a non-zero count

---

## v10.11 — Confirmed deployed

The earlier entry for v10.10 deployment is retired; v10.10 → v10.11 was a small surgical patch (single-skill promotion) and the live PI in session_2026-05-15a's prompt is v10.11, so deployment of both v10.10 and v10.11 is treated as complete.

Historical detail of v10.6 → v10.10 → v10.11 cumulative changes is preserved in:
- `governance/project-instructions-v10_10.md` (v10.10 snapshot, with v10.6→v10.10 changelog entries)
- `governance/project-instructions-v10_11.md` (v10.11 snapshot)
- `sessions/session_2026-05-13b-evidence-verification-methodology.md` (architecture v2.3 + DR-2026-05-13 + PI v10.10 work)
- `sessions/session_2026-05-15a-governance-reconciliation.md` (v10.11 promotion + 2026-05-15 governance reconciliation)
