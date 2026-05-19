# PI Deployment Queue

**Live in claude.ai project settings:** v10.13 (deployed by owner; the present-session prompt loads v10.13, confirming deployment).
**Repo-side snapshot:** `governance/project-instructions-v10_13.md` (commit `29ea3bf`, 2026-05-19).
**Pending deployment:** none. Queue is empty.

---

## State as of 2026-05-19

All three pending entries (v10.11, v10.12, v10.13) deployed and snapshotted. No outstanding PI bumps.

| Version    | Live in claude.ai | Repo snapshot                                 | Notes                                                                                 |
|------------|-------------------|-----------------------------------------------|---------------------------------------------------------------------------------------|
| v10.11     | Yes (since ≤2026-05-15) | `governance/project-instructions-v10_11.md` | `reasoning-doc-citations` skill promotion.                                            |
| v10.12     | Yes (deployed before 2026-05-17 amend) | `governance/project-instructions-v10_12.md` | Bootstrap `_GH_SKILLS()` fix + standing rule #11 amend (adherence logging).            |
| v10.13     | Yes (loads this session) | `governance/project-instructions-v10_13.md` (commit `29ea3bf`) | DR-2026-05-18: `COMPLETE-STATUTORY` peer value in rule #10. |

Historical detail of v10.6 → v10.11 cumulative changes is preserved in the corresponding `governance/project-instructions-v10_*.md` snapshots and in `sessions/session_2026-05-13b-evidence-verification-methodology.md` plus `sessions/session_2026-05-15a-governance-reconciliation.md`.

---

## Drift observations carried forward

These are not PI-bump candidates — they are downstream content/code drift surfaced during the 2026-05-19 robustness review of `evidence_sources`:

1. **PI rule #10 numerator drift.** Rule #10 prose and the bootstrap status block reference `/661` evidence_sources rows; actual count is 671 (+10). Cosmetic but visible at every session start. Candidate for inclusion in the next substantive PI bump rather than a standalone v10.14 patch.
2. **`evidence_sources` row count drift.** Same root cause; tracked in the DB itself, no separate remediation needed.
3. **Bootstrap status grep no-op.** The line `grep -E "session_close|next_action|blockers" /tmp/session.md` does not match the current session-record header format. Status block still prints the session ID. Candidate for the same future PI patch.

None of these block synthesis work. Defer.

---

## Conventions reminder

Per architecture v2.3 `<migration_and_growth>`: PI bumps go live only when the owner manually pastes the new content into claude.ai → Project Settings. Repo-side snapshot files in `governance/` are the audit-trail counterpart and are committed directly. The repo-side commit does not change the live PI.

Per standing rule #11: commits modifying this file (`decisions/PI-update-needed.md`) require a `[DOCTRINE: <sha>]` token and a corresponding `attestations/PI-update-needed.json` entry.
