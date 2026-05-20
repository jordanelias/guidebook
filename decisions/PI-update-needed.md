# PI Deployment Queue

**Live in claude.ai project settings:** v10.13 (deployed by owner; the most recent session prompt loaded v10.13, confirming deployment).
**Repo-side snapshot:** `governance/project-instructions-v10_13.md` (commit `29ea3bf`, 2026-05-19).
**Pending deployment:** **v10.14** — `governance/project-instructions-v10_14.md` (this session, 2026-05-20).

---

## State as of 2026-05-20

One pending entry: v10.14. Owner action needed to paste contents of `governance/project-instructions-v10_14.md` into claude.ai → Project Settings to make it live.

| Version | Live in claude.ai | Repo snapshot | Notes |
|---|---|---|---|
| v10.11 | Yes (since ≤2026-05-15) | `governance/project-instructions-v10_11.md` | `reasoning-doc-citations` skill promotion. |
| v10.12 | Yes (deployed before 2026-05-17 amend) | `governance/project-instructions-v10_12.md` | Bootstrap `_GH_SKILLS()` fix + standing rule #11 amend (adherence logging). |
| v10.13 | Yes (loads this session) | `governance/project-instructions-v10_13.md` (commit `29ea3bf`) | DR-2026-05-18: `COMPLETE-STATUTORY` peer value in rule #10. |
| **v10.14** | **No — paste needed** | `governance/project-instructions-v10_14.md` (this session) | Three minor-patch drifts from session 2026-05-19: rule #11(a) token placement, bootstrap `/661`→`/670`, bootstrap grep update. Preferences pointer bump to `userPreferences-v6.3.md`. |

---

## v10.14 specific changes

1. **Standing rule #11 sub-(a) explicit token placement.** Adds the canonical form `{skill}: {action} [DOCTRINE: <sha>] [YYYY-MM-DD HH:MM]` to the rule text. Rationale: `scripts/ci_helpers/check_commit_msg.py` regex requires the timestamp as the LAST bracket. Token-after-timestamp ordering fails the format check silently. Six session-2026-05-19 governance commits hit this (`9e2b986`, `d641e42`, `1290f2d`, `662af85`, `478683f`, `2a9fad3`). v10.14 commit `b6d2c58` (this session record) demonstrates the corrected ordering and passes CI.

2. **Bootstrap `evidence_sources` numerator.** `/661` → `/670`. Post-dedup count after `data_20260519060000_dedup_bettarello_2021_app11093942.sql` removed REF-00047. Both occurrences (AUTHOR-TITLE-ONLY ratio + NULL verification_status ratio) updated.

3. **Bootstrap state-query grep.** `grep -E "session_close|next_action|blockers"` → `grep -E "^## (Headline|Known broken|Next-action|Next action)"`. The prior pattern matched no headers in the current session-record format (architecture v2.3 era), quietly returning empty lines on every session start. Updated to match both `## Headline outcomes` (v2026-05-19 format) and `## Known broken / pending work` (v2026-05-17 format) and `## Next-action handoff` (variant).

No standing-rule semantic changes. No `<skills_assigned>` changes. No structural rename or removal. Preferences pointer updated `userPreferences-v6.2.md` → `userPreferences-v6.3.md`.

---

## Conventions reminder

Per architecture v2.3 `<migration_and_growth>`: PI bumps go live only when the owner manually pastes the new content into claude.ai → Project Settings. Repo-side snapshot files in `governance/` are the audit-trail counterpart and are committed directly. The repo-side commit does not change the live PI.

Per standing rule #11: commits modifying this file (`decisions/PI-update-needed.md`) require a `[DOCTRINE: <sha>]` token AND a corresponding `attestations/decisions_PI-update-needed.json` entry. Going forward (per v10.14): token placement is BEFORE the timestamp.
