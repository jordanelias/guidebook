# PI Deployment Queue

**Live in claude.ai project settings:** v10.13 (deployed by owner; the most recent session prompt loaded v10.13, confirming deployment).
**Repo-side snapshot:** `governance/project-instructions-v10_13.md` (commit `29ea3bf`, 2026-05-19).
**Pending deployment:** **v10.14** — `governance/project-instructions-v10_14.md` (rewritten 2026-05-20).

---

## State as of 2026-05-20

One pending entry: v10.14. Owner action: paste contents of `governance/project-instructions-v10_14.md` into claude.ai → Project Settings.

| Version | Live in claude.ai | Repo snapshot | Notes |
|---|---|---|---|
| v10.11 | Yes (since ≤2026-05-15) | `governance/project-instructions-v10_11.md` | `reasoning-doc-citations` skill promotion. |
| v10.12 | Yes (deployed before 2026-05-17 amend) | `governance/project-instructions-v10_12.md` | Bootstrap `_GH_SKILLS()` fix + standing rule #11 amend (adherence logging). |
| v10.13 | Yes (loads this session) | `governance/project-instructions-v10_13.md` (commit `29ea3bf`) | DR-2026-05-18: `COMPLETE-STATUTORY` peer value in rule #10. |
| **v10.14** | **No — paste needed** | `governance/project-instructions-v10_14.md` (commit on 2026-05-20) | (1) Rule #11(a) explicit token placement clarification. (2) Bootstrap extracted to `scripts/bootstrap.sh` — future bootstrap drift no longer requires PI bumps. |

---

## v10.14 specific changes

**The point of v10.14 is to be the last bootstrap-related PI bump.** After this paste, future bootstrap drift (status-block formatting, numerator updates, new state queries, grep-pattern tweaks) ships as ordinary commits to `scripts/bootstrap.sh` on main — no PI bump, no owner paste.

1. **Standing rule #11 sub-(a) explicit token placement.** Adds the canonical form `{skill}: {action} [DOCTRINE: <sha>] [YYYY-MM-DD HH:MM]` to the rule text. Rationale: `scripts/ci_helpers/check_commit_msg.py` regex requires the timestamp as the LAST bracket. Token-after-timestamp ordering fails the format check silently. Six session-2026-05-19 governance commits hit this (`9e2b986`, `d641e42`, `1290f2d`, `662af85`, `478683f`, `2a9fad3`). Commit `a262dcd` (first v10.14 author) and `b6d2c58` (session record) demonstrate the corrected ordering and pass CI.

2. **Bootstrap extracted to `scripts/bootstrap.sh`.** The inline bash block in the PI's `<bootstrap>` section is replaced with a 6-line thin caller:

    ```bash
    PAT=$(sed -E 's/^`//; s/`$//' /mnt/project/GitHub_pat | tr -d '\n')
    export PAT REPO="jordanelias/guidebook"
    curl -fsSL -H "Authorization: Bearer $PAT" \
      "https://raw.githubusercontent.com/${REPO}/main/scripts/bootstrap.sh" | bash
    ```

    The script itself:
    - Reads `PAT` from env (set by the thin caller from `/mnt/project/GitHub_pat`, which is provided by claude.ai project knowledge — no PAT in repo).
    - Derives the `evidence_sources` numerator from a DB query at runtime (no hardcoded `/661` or `/670` to drift).
    - Uses a stable section-grep pattern (`^## (Headline|Known broken|Next-action|Next action)`) matching the post-architecture-split session-record format.
    - Lives in the repo and updates via normal commits.

    Architecturally aligned with architecture v2.3 `<bootstrap_pattern>` which explicitly contemplated this extraction: "When bootstrap grows past these budgets, extract the heaviest portion (typically SQLite state queries) to a `bootstrap-status` skill and leave a thin caller in PI."

**Effect on PI size:** v10.13 was 280 lines; v10.14 is 217 lines (–63 lines, ~–23%). The deleted lines moved to `scripts/bootstrap.sh` (verbatim plus the inline patches the session would have otherwise needed).

**Bootstrap-exempt clause stays in PI** (it's a rule about when bootstrap runs, not bootstrap mechanics).

---

## What this changes about future workflow

Before v10.14:

| Change type | Required action |
|---|---|
| Standing rule edit | PI bump + owner paste |
| New skill assignment | PI bump + owner paste |
| Bootstrap status-block content update | PI bump + owner paste |
| Bootstrap grep pattern fix | PI bump + owner paste |
| Numerator update | PI bump + owner paste |
| New state-query addition | PI bump + owner paste |

After v10.14 paste:

| Change type | Required action |
|---|---|
| Standing rule edit | PI bump + owner paste |
| New skill assignment | PI bump + owner paste |
| Bootstrap status-block content update | **commit to main only** |
| Bootstrap grep pattern fix | **commit to main only** |
| Numerator update | **commit to main only** (or dynamic via DB query) |
| New state-query addition | **commit to main only** |

The PI becomes the rule layer it was supposed to be; mechanics live in the repo where they belong.

---

## v10.15 queued (added 2026-05-23)

| Version | Live in claude.ai | Repo snapshot | Notes |
|---|---|---|---|
| **v10.15** | **No — paste needed when authored** | not yet authored — will be `governance/project-instructions-v10_15.md` | Rule #10 final paragraph cohort wording: drop the "from the 2026-03-30 round" restrictor. Sharpened by DR-2026-05-23. |

**v10.15 specific change.** Standing rule #10 final paragraph currently reads:

> BPCs bearing `opus_synthesis: YES [OPUS-SYNTHESIS]` from the 2026-03-30 round carry a `synthesis_validity: PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION` banner until Phase E.2g overwrites.

Operational application (B.0 closure on 2026-05-23) found that the 2026-03-30 round is the largest single cohort but not the only pre-rehab synthesis batch — four rounds collectively touched 70 files across 68 unique slugs, all of which used pre-rehab evidence. DR-2026-05-23 redefined the cohort as any positive `[OPUS-SYNTHESIS*]` tag pre-dating the 2026-05-23 rehab closure. The v10.15 patch ratifies the DR's cohort definition in PI rule #10 text. The replacement text is:

> BPCs bearing any positive `[OPUS-SYNTHESIS*]` tag (any variant — bare, dated, provisional, or annotated) where the synthesis date predates the 2026-05-23 evidence-metadata-rehabilitation closure (commit `b0a4a25`) carry a `**SYNTHESIS VALIDITY:** PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION` banner until Phase E.2g overwrites. Cohort enumeration and selection criterion: DR-2026-05-23. Live state of which BPCs carry the banner: `bpc_metadata.evidence_state = 'RETRACTED-PRE-REHAB'`.

No other rule changes; no skill-assignment changes; no bootstrap changes.

---

## Conventions reminder

Per architecture v2.3 `<migration_and_growth>`: PI bumps go live only when the owner manually pastes the new content into claude.ai → Project Settings. Repo-side snapshot files in `governance/` are the audit-trail counterpart and are committed directly. The repo-side commit does not change the live PI.

Per standing rule #11 (per v10.13 still live; v10.14 adds the explicit ordering): commits modifying this file (`decisions/PI-update-needed.md`) require a `[DOCTRINE: <sha>]` token AND a corresponding `attestations/decisions_PI-update-needed.json` entry. Going forward (per v10.14): token placement is BEFORE the timestamp.
