#!/usr/bin/env python3
"""scripts/audit/research_tooling_separation.py — research and tooling ship apart (RC6).

WHY THIS EXISTS. DR-2026-09-26-recurring-defect-shapes-remediation.md section 6: batch
20's own PR shipped `data/guidebook.db` (research rows) together with new `db.py`
subcommands, a schema migration and a new test file (tooling) in the same changeset. By
the batch's own record: "Every correctness defect was found by running the code, not by
any gate" -- `link-admission` was a tautology, `unlink-admission` was unshippable (its
capture path refused the DELETE and its own test never went through capture), and
pre-write quote checks "were vacuous". A writer gap discovered mid-batch, under deadline,
is the moment a session is likeliest to patch it with hand SQL disguised as a schema fix
-- exactly what CLAUDE.md section 4 forbids, because it bypasses every refusal db.py has.

WHAT COUNTS AS EACH, and why the registry's `kinds:` globs alone cannot say. `schema:`'s
glob (`scripts/migrations/**`) is checked before `data:`'s and `tooling:`'s (first match
wins, CLAUDE.md-adjacent `run_checks.classify`), so EVERY file under `scripts/migrations/`
-- a numbered schema migration and a `data_*.sql` migration alike -- classifies `schema`,
never `data` or `tooling`. `migrate_db.py`'s `DATA_PATTERN`/`SCHEMA_PATTERN` are the one
home of the distinction the kind glob cannot make:

  * RESEARCH DATA: a path classified `data` (today, only `data/**`), OR a path under
    `scripts/migrations/` whose basename matches `migrate_db.DATA_PATTERN`.
  * TOOLING: a path classified `tooling` (scripts, tools, .github, .claude), OR a path
    classified `schema` that is NOT a data migration -- a numbered migration
    (`migrate_db.SCHEMA_PATTERN`) or anything under `schemas/**`.

FAILS when one changeset contains both. A scratchpad driver script belongs to no
registered kind and stays allowed either way.

`data/guidebook.db` ITSELF IS A NAMED EXCEPTION, not a bare `data:`-kind path. Every
schema migration ships committed together with the blob it produced -- migrations
094-097 all did, and that convention long predates RC6, which never proposes splitting a
schema bump (a `user_version` stamp plus empty tables, zero new or changed rows) into its
own PR. So `data/guidebook.db` counts as research data only when the SAME changeset also
carries a `data_*.sql` migration (unambiguous: a data migration by definition captures
rows), or carries NO migration file at all (a blob change with no migration behind it is
already CLAUDE.md rule 3's violation, and this check errs toward flagging it, not hiding
it). A changeset with `data/guidebook.db` plus ONLY numbered schema migrations is not
research data for this check's purposes -- it is a schema-only PR, tooling through and
through, and phase 1a of this DR's own build is the first specimen of exactly that shape.

NAMED RESIDUAL. `governance/check-registry.yaml` itself classifies `governance`, so a
registry entry that registers new tooling alongside research rows passes this check —
PR #159 did exactly that. Adding that one path to the tooling set here would be a
curated list (CLAUDE.md rule 8); it is named as a residual rather than patched.

Advisory until OQ-3 is answered and one clean batch has passed it (DR-2026-09-26 section
7). CHANGESET-SCOPED: the subject is a diff against `--base` (default `origin/main`), so
its size varies per commit and zero of either kind is a routine, correct result.
"""
import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import run_checks                                                   # noqa: E402
import migrate_db                                                    # noqa: E402


def classify_path(path: str, reg: dict, has_data_migration: bool):
    """(is_research_data, is_tooling) for one changed path.

    `has_data_migration` is a fact about the WHOLE changeset (whether ANY path in it is a
    `data_*.sql` migration), needed only to resolve `data/guidebook.db`'s named exception.
    """
    kinds, _ = run_checks.classify([path], reg)
    name = Path(path).name
    is_data_migration = bool(migrate_db.DATA_PATTERN.match(name))
    is_schema_kind = "schema" in kinds
    if path == "data/guidebook.db":
        # A schema-only changeset (no data migration alongside) is the DB's normal,
        # expected companion change, not research data — see module docstring.
        return has_data_migration, not has_data_migration
    research = ("data" in kinds) or (is_schema_kind and is_data_migration)
    tooling = ("tooling" in kinds) or (is_schema_kind and not is_data_migration)
    return research, tooling


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="origin/main")
    args = ap.parse_args()

    # run_checks.changed_paths resolves the merge-base and includes untracked files, so
    # this also sees a session's in-progress, uncommitted work -- the diff-scoped gate's
    # own semantics, not a re-derivation of them (CLAUDE.md section 1).
    try:
        paths = run_checks.changed_paths(args.base)
    except RuntimeError as exc:
        print(f"[ERROR] cannot read base ref {args.base!r}: {exc}")
        print("EXAMINED: 0")
        return 2

    reg = run_checks.load_registry()
    has_data_migration = any(
        migrate_db.DATA_PATTERN.match(Path(p).name) for p in paths
        if p.startswith("scripts/migrations/"))
    research_paths, tooling_paths = [], []
    for p in paths:
        is_research, is_tooling = classify_path(p, reg, has_data_migration)
        if is_research:
            research_paths.append(p)
        if is_tooling:
            tooling_paths.append(p)

    print(f"Changeset vs {args.base}: {len(paths)} path(s)")
    if research_paths:
        print(f"Research data path(s) ({len(research_paths)}):")
        for p in research_paths:
            print(f"  {p}")
    if tooling_paths:
        print(f"Tooling path(s) ({len(tooling_paths)}):")
        for p in tooling_paths:
            print(f"  {p}")
    print(f"EXAMINED: {len(paths)}")

    if research_paths and tooling_paths:
        print("VERDICT: FAIL — this changeset carries both research data and tooling. "
              "RC6 (DR-2026-09-26-recurring-defect-shapes-remediation.md section 6): "
              "they ship apart, so a writer gap found mid-batch cannot be patched with "
              "hand SQL disguised as a schema fix.")
        return 1
    print("VERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
