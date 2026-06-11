# PI Deployment Queue

**Live in claude.ai project settings:** v10.14 (deployed by owner; the operative session prompt loads v10.14 — header reads "V10.14 · Revised 2026-05-20" — confirming deployment).
**Repo-side snapshot:** `governance/project-instructions-v10_14.md` (rewritten 2026-05-20).
**Pending deployment:** none on the bootstrap/rule track. Queued for the next legitimate PI bump (documentation-only, per "no PI bump unless critical armature"): the v10.16 `gap-driven-mining` skill-assignment line, and the DR-2026-05-28-c `<hooks_status>` addition (`scripts/audit/population_integrity_audit.py`).

---

## State as of 2026-06-09

v10.14 is **DEPLOYED** — it is the operative PI loaded this session, closing the prior pending-paste entry. No rule/bootstrap-track paste is pending. Documentation-only additions are queued for the next legitimate PI bump (see header): the v10.16 skill-assignment line and the DR-2026-05-28-c `<hooks_status>` audit entry.

| Version | Live in claude.ai | Repo snapshot | Notes |
|---|---|---|---|
| v10.11 | Yes (since ≤2026-05-15) | `governance/project-instructions-v10_11.md` | `reasoning-doc-citations` skill promotion. |
| v10.12 | Yes (deployed before 2026-05-17 amend) | `governance/project-instructions-v10_12.md` | Bootstrap `_GH_SKILLS()` fix + standing rule #11 amend (adherence logging). |
| v10.13 | Yes (loads this session) | `governance/project-instructions-v10_13.md` (commit `29ea3bf`) | DR-2026-05-18: `COMPLETE-STATUTORY` peer value in rule #10. |
| **v10.14** | **Yes — deployed (loads this session)** | `governance/project-instructions-v10_14.md` (commit on 2026-05-20) | (1) Rule #11(a) explicit token placement clarification. (2) Bootstrap extracted to `scripts/bootstrap.sh` — future bootstrap drift no longer requires PI bumps. |

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

## v10.16 — queued (2026-05-26)

**Status:** queued — repo-side snapshot pending.
**Source:** DR-2026-05-26 gap-driven mining protocol; Pass 2b session 2026-05-26.

Single-line change to `<skills_assigned>`: add `gap-driven-mining` to the skills PI itself invokes by name. Skill file ships in this session at `skills/gap-driven-mining_SKILL.md`; the skill registry is updated by the same commit; PI text changes are deferred to the next bump per architecture v2.3 `<scope_assumptions>` (skill-assignment-only changes do not require an out-of-band PI bump).

Proposed line addition (under `<skills_assigned>` near the existing per-skill entries):

```markdown
- `gap-driven-mining` — per DR-2026-05-26 for mining-addressable gaps (companion to citation-miner; gap-keyed rather than anchor-source-keyed)
```

The skill name belongs alongside `citation-miner`, `adversarial-research`, and `progressive-measurement` in the existing PI list — each is invoked per a specific standing rule or DR. No new standing rule is added; the protocol is governed by the DR, and the skill file declares its rule interlocks (#7, #8, #10, DR-2026-05-24).

**Hold reason.** Bundling with the next legitimate PI bump per the v10.15-rejected rationale ("no PI bump unless critical armature"). Skill assignments are not critical armature; the skill is invocable via its trigger keywords whether or not PI text names it. The PI line addition is documentation, not gate. When the next PI version ships for an unrelated reason, this line gets folded in.

**Bootstrap impact.** None. The skill counts in `_GH_SKILLS()` (per v10.12 fix) which counts `skills/*_SKILL.md` files via the GitHub contents API — the new file is auto-counted.

---

## DR-2026-05-28-c `<hooks_status>` addition — queued (2026-06-09)

**Status:** queued — bundle with the next legitimate PI bump.
**Source:** DR-2026-05-28-c (population-junctions governance close); migration 021.

Single addition to PI `<hooks_status>` Level-2 list:

```markdown
- `scripts/audit/population_integrity_audit.py` — scalar↔junction population consistency (DR-2026-05-28-c)
```

**Hold reason.** Same as v10.16 — adding an audit-script line to `<hooks_status>` is documentation, not gate. The audit runs whether or not the PI names it; CI `db_integrity` already enforces the junction FKs via `PRAGMA foreign_key_check` at the blocking level. Folds into the next PI bump shipped for an unrelated reason.

**Bootstrap impact.** None.

---

## v10.15 — considered and rejected (2026-05-23)

A v10.15 entry was briefly queued in this file on 2026-05-23 (commit `be146a2`) to amend standing rule #10 final-paragraph cohort wording (broaden "from the 2026-03-30 round" to "any positive `[OPUS-SYNTHESIS*]` tag pre-dating the 2026-05-23 rehab closure"). Withdrawn the same session per owner directive: no PI bump unless critical armature.

Rationale for withdrawal — the proposed amendment was not critical armature:

- **The DR governs cohort scope.** `decisions/DR-2026-05-23-pre-rehab-banner-cohort-definition.md` defines the cohort criterion and freezes enumeration in `decisions/DR-2026-05-23-cohort-manifest.json`. PI rule #10 already cites DRs as the authoritative locus for cohort decisions (the rule's own banner-removal predicate references sub-rules 1/2/3 by content, not by enumerated slug list).
- **State, not rule.** Per architecture v2.3 `<migration_and_growth>` ("PI standing rules describe rules, not state. State content — current AUTHOR-TITLE-ONLY counts, retraction banners, session-specific commentary — belongs in DRs, audit scripts, or the DB"), which BPCs hold the banner is state. The rule predicate ("any positive `[OPUS-SYNTHESIS*]` tag pre-rehab") is also operational classification, not a standing-rule mechanism change.
- **Audit + DB carry the load.** `scripts/audit/pre_rehab_banner_audit.py` (Level 2) enforces the four invariants against the DR. `bpc_metadata.evidence_state = 'RETRACTED-PRE-REHAB'` is the queryable source of truth. The literal PI text "from the 2026-03-30 round" remains defensible reading as descriptive shorthand for the dominant round; the DR sharpens scope without contradicting the rule.

The cohort decision is captured durably without touching PI. Future Phase E.2g overwrites transition specific slugs out of `RETRACTED-PRE-REHAB` per the DR's overwrite predicate; no PI bump required for that workflow either.

---

## Conventions reminder

Per architecture v2.3 `<migration_and_growth>`: PI bumps go live only when the owner manually pastes the new content into claude.ai → Project Settings. Repo-side snapshot files in `governance/` are the audit-trail counterpart and are committed directly. The repo-side commit does not change the live PI.

Per standing rule #11 (per v10.13 still live; v10.14 adds the explicit ordering): commits modifying this file (`decisions/PI-update-needed.md`) require a `[DOCTRINE: <sha>]` token AND a corresponding `attestations/decisions_PI-update-needed.json` entry. Going forward (per v10.14): token placement is BEFORE the timestamp.

---

## v10.15 — QUEUED (2026-06-10): rule #2 capability-floor clarification

Per `decisions/DR-2026-06-10-synthesis-model-floor.md` (RATIFIED 2026-06-10). Amend standing rule #2's first sentence to express the synthesis restriction as a **capability floor**, not a brand pin:

> Current: "Sonnet does NOT write `best_practice_synthesis` — only Opus."
> Proposed: "`best_practice_synthesis` is written only by an Opus-class-or-above model (the project's top capability tier); lower-tier models produce evidence inventories, reasoning-document drafts, and per-population logging, and queue for synthesis per Phase E.2f."

Rationale: the rule protects judgment quality at the top tier; the literal string "Opus" was the capability ceiling at authoring time and now under-specifies it (Stage 4.3 runs under Fable 5, a Mythos-class model above Opus). State/skill model-pins are swept separately (Stage 4.3 plan G4c). Goes live only on owner paste into claude.ai → Project Settings; this file and the DR are the repo-side audit-trail counterpart.
