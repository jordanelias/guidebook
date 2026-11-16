# Batch 1: what was executed, what stopped, and what later tasks must read

_Written at the end of the batch (owner instruction 2026-11-15, "sweep … forward and backward"). Derive every count from `git log`; none is typed here. The line-by-line account of what the critics found and what is still the owner's is `scratchpad/session_2026-11-15-remediation-stack/sweep-list.md`._

## Executed (one commit per task, then one repair commit per critic pass; stacked on one branch)

T-001, T-002, T-003, T-004, T-006, T-007, T-009, T-010, T-011, T-015, T-021, T-023, T-025, T-027 (in part), T-034, T-041, T-042, T-043, T-048, T-051, T-054, T-055, T-073, T-076, T-080, T-090, T-121. `git log --oneline --grep='T-0\|T-1'` lists the commits.

## Stopped, and why (not repaired: a design or owner question)

- **T-052**: its paragraph names `db.py add-locator --jurisdiction`; the verb has no such flag and `source_locators.jurisdiction` is legacy free text exempted from the jurisdiction audit (GAP-008). Nothing was changed.
- **T-027, two parts**: `original_title` is now a payload field of `correct-source` (done after the critic), but a standard's `edition` still has no writer (Crossref has none for a document with no DOI), and the `v_evidence_authors` full given name needs a column saying which names have no initials convention.
- **Not reached in this batch** (executed in a later session): T-061, T-063, T-067, T-074, T-075, T-077, T-079, T-088. Their task files are unchanged except where a line below says to read something first.
- **Research-kind READY tasks (own pull request, after the tooling merges, CLAUDE.md rule 10)**: T-104, T-111, T-113. **Not for Sonnet** (design or owner): T-028, T-031, T-070, T-078, T-082, T-091 (design file missing), T-103, T-106, T-119, T-123, T-126.

## Later tasks: read these before executing

- **T-056** adds a third successor column "and widens this CHECK": the check on `base_taxonomy_identity` is a column-level CHECK carried by `superseded_by_identity` (migration 135, added in place). Widening it needs a table rebuild (as 133/136 did), not an ALTER.
- **T-102, T-114, T-115, T-116** call `retire-identity`. It refuses unless the approving entry's heading begins "Owner", is dated, found once and **names the code**; a logged search and a graded population match are records and do not block (they are listed in the result); a resolved gate and a closed gap are not live; a code that is another deprecated code's successor cannot be retired. A crossing row moves with `add-population-icf-link` (a new row) then `retire-population-icf-link`.
- **T-018, T-117, T-118**: `determination_gates` now has the four lens columns and the verdict `QUESTION` (no tier, no source, never caps a cell; the engine prints it as QUESTIONED). Migration 134 states the true lens-matching rule in its stored DDL.
- **T-061, T-071, T-102, T-113**: the amendable set of `source_value_extractions` is derived (T-061, GAP-013): the live columns minus `db._NOT_AMENDABLE_SVE`, each exclusion with its reason (`db._amendable_sve_fields(conn)`); it holds `root_id` (T-048), `device_class` (T-055) and the three reformat fields. A task that wants a column amendable removes it from the exclusion dict, with its gate.
- **T-049**: `gaps` is `cross-stage` in the stage map (T-051); `walkability.py` is unchanged, so a cross-stage table stays outside the spine and OD-11's "count it as a member of each stage it carries" is not met (sweep list: the design question).
- **T-047, T-085, T-101**: `add-lang-jur-pair`, `set-pair-scope` take an `--approval-ref` that must be an "Owner…" ledger entry; a sub-national code is refused for a pair.
- **T-031, T-053**: `db.py cell-status` exists (T-034); research is read through the slug a parameter's figures carry, and a lens narrows evidence held, gates and gaps.
- **T-080 / T-081**: `log-search` now refuses a zero-result search with no `--absence-class` and no `--deferred-reason`; the 12 live zero-result rows are T-081's (research).
- **T-075**: `migration_reproducibility --deep` compares rows, not the stored DDL text; a comment edited in an applied migration passed it (the critic found it by diffing `sqlite_master` against a rebuild).
- **T-067 / T-079** (after migration 137): `v_coverage_priority` now anti-joins only searches that ran (`deferred_reason IS NULL`); T-067's redefinition starts from the 137 text, not from 135's. `db.py coverage --slug` reads `searched` the same way; a pair whose only logged search is a deferral is owed and shows in `v_coverage_lens.deferred`.
- **T-067, T-055 follow-on**: the function path (`identity_icf_map`) of a parent cell reads the parent's own code only; a ruling is needed before any task assumes a parent's cell reads its descendants' mappings (sweep list, T-055 critic (a)).
- **T-088 / T-089**: a writer's refusal under the running `--session` is kept in `scratchpad/<session>/refusals.jsonl` (`dbcore.record_refusal`); `T088-09` walks the syntax of every writer script (one that adds `--session`) and fails any place that says no (an exit with a message or code, a REFUSING/ERROR print, a JSON error print, a plain ArgumentParser) that no recorder call precedes, so a new writer's refusal must be routed there. `refusal_register.py` already has `list` and `dispose` (a refusal is named by its `refusal_id`); T-089's precondition records the exact line shape.
