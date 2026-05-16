# PI Deployment Queue

**Live in claude.ai project settings:** v10.11 (deployed by owner sometime between session_2026-05-13b close and session_2026-05-15a; the present-session prompt loads v10.11, confirming deployment).
**Pending deployment:** v10.12 (drafted in session_2026-05-15a).

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
