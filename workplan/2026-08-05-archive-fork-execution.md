# Archive fork: execution state and the caller sweep that narrowed it

**Date:** 2026-08-05 · **Status:** BLOCKED on one owner action, then ready
**Owner ruling:** ⚑1 fork trajectory = **archive fork** (2026-08-05). This closes the
DG-NON gate that `workplan/2026-08-03-fork-cut-walkable-graph-execution-plan.md` line 662
left open ("Whether to fork at all — owner only"). ⚑2 and ⚑3 remain open and are **not**
required for the archive reading.
**Owner parameters:** archive is **private**; prune scope is **safe set only**.

---

## 1. The blocker

`mcp__github__create_repository` returns `403 Resource not accessible by integration`.
Repository creation is outside the GitHub App's grant. **This session cannot create the
archive repo.** One owner action unblocks everything below:

1. Create `jordanelias/guidebook-archive` — **private**, **do not** initialise with a
   README/licence/gitignore (an empty repo makes the mirror push clean).
2. Tell a session it exists; it will `add_repo` and push the mirror.

Nothing is at risk while this is pending: git history in `jordanelias/guidebook` already
retains everything, so the archive is for browsability and separation, not data safety.

## 2. The caller sweep NARROWED the approved safe set, 4 directories to 2

Per `architecture/project-architecture-guidebook-v2.3.md` `<migration_and_growth>` and
CLAUDE.md §0 rule 5: a structural removal is not done until the caller sweep is done. The
sweep was run before any move, and it disqualified half the approved set. Recording the
evidence rather than quietly shrinking the plan.

### CLEARED — move to the archive

| Path | Size | Files | Why it is safe |
|---|---|---|---|
| `_archived/` | 4.6M | 170 | Every CODE reference is *exclusion* logic — `scripts/audit/graph/extract_content.py:28`, `scripts/audit/db_path_env_audit.py:37`, `scripts/audit/retired_vocabulary_audit.py` exempt_paths. Each becomes a harmless no-op when the directory is gone. `scripts/ci_helpers/check_yaml.py:6` names it only in a comment. The other 52 inbound references are prose. |
| `workplan/_superseded/` | 428K | 20 | 7 inbound references, all prose. No code path. |

**Total: 5.0 MB, 190 files.**

### HELD — do NOT move without further work

| Path | Blocker | What it would take |
|---|---|---|
| `references/search-log/` | `scripts/validate_cross_refs.py:115` globs `references/search-log/**/*.md`, and `validate_cross_refs` is **`level: blocking`, `kinds: [always]`** — it runs on every diff. Deleting its subject would very likely make it pass **vacuously**, which is the precise failure class four gates were repaired for this week. | Give the check a `min_items` floor so it FAILS on an empty subject, then decide whether the log is still its subject at all. |
| `versions/` | `scripts/item_audit_pipeline.py:30,71-73` reads `versions/current/Guidebook_for_Accessible_Design_v9-0_2026-03-20.md`. It guards with `.exists()`, so removal degrades it **silently** rather than crashing — worse, not better. Also `scripts/validate_temporal.py:210` (quarantined) and `scripts/convert/version_retrofit.py`. | Rehome the spec source, or make the pipeline fail loudly when it is absent. |

`sessions/` and `audits/` were already excluded before the sweep: `sessions/LATEST` feeds the
blocking `citation_mining_session` check (the pointer split is W4.1), and `audits/` holds
`bpc-rewrite-workplan-2026-05-11.md`, which CLAUDE.md §6 names as the ACTIVE content workplan.

## 3. Execution order, once the repo exists

1. `add_repo` the archive; push a **full-history mirror** (`git push --mirror`). Verify the
   archive's `main` resolves to the same tree SHA as the source before anything is removed.
2. Remove the two cleared directories from `jordanelias/guidebook` in one commit.
3. **Redirect stubs, per CLAUDE.md §9 guardrail 2** — do not simply delete anything still
   referenced. Leave `_archived/README.md` and `workplan/_superseded/README.md` in place,
   each naming the archive repo and the commit SHA at which the content moved, so a reader
   following a stale path lands on a pointer rather than a 404.
4. Re-run `scripts/preflight.sh --all`. Expect `validate_cross_refs` and the tripwire to stay
   green: the tripwire's `_archived/**` and `workplan/_superseded/**` exemptions become
   no-ops, not errors.
5. Correct `CLAUDE.md` §3's repository map, which currently describes `_archived/` as
   "Retire *here*, don't delete." After the cut, the retire-here target is the archive repo.

## 4. What this does and does not buy

Removes ~5.0 MB and 190 files — about **9% of tracked files** — from the surface a session
scans. It does not touch the research corpus, which is the larger mass and is content work.

The honest measure: this is a modest win on its own. The larger legibility gains this week
came from making registers stop lying, not from moving bytes. The archive's real value is
that it gives `_archived/` a destination outside the working tree, so the next retirement
has somewhere to go that is not "still in the repo, but with a different prefix".
