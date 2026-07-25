#!/usr/bin/env python3
"""
scripts/audit/db_path_env_audit.py — enforce the GUIDEBOOK_DB_PATH contract.

CLAUDE.md §7 states: "Every DB-aware script honours GUIDEBOOK_DB_PATH (default
data/guidebook.db)." On 2026-07-25 that was false for 9 of the 12 live
DB-connecting scripts. The cost was not theoretical: a reach test for the
synonym-grouping work silently read the committed database instead of the
scratch copy it was pointed at, and reported "no change" for a change that had
in fact taken effect.

A text rule that nothing checks is a rule that drifts. This promotes it to
level 2 on the enforcement spectrum (CLAUDE.md §2: text rule -> audit script).

Scope. A script is IN SCOPE when all three hold:
  1. it is not under a one-time/legacy directory (see EXCLUDE_PARTS, mirroring
     scripts/audit/graph/extract_code.py so "legacy" means one thing repo-wide);
  2. it calls sqlite3.connect;
  3. it names guidebook.db somewhere other than a docstring — i.e. in code.

Condition 3 is what keeps false positives out: several modules discuss the
database in prose but never build a path to it. Condition 1 is what excludes
scripts/db/**, which points at data/db/guidebook.db — a different, legacy file
that is not the canonical database and must not be redirected by this variable.

Exit 0 when every in-scope script honours the variable; exit 1 with the
offending list otherwise.
"""
import ast
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

# Mirrors extract_code.py: one-time / legacy / different-schema code.
EXCLUDE_PARTS = {"migrations", "db", "migrate", "probes", "test", "tests",
                 "__pycache__", "_archived"}

ENV_VAR = "GUIDEBOOK_DB_PATH"
DB_NAME = "guidebook.db"

# Scripts that do not read the variable directly and are still correct.
# `delegates_to` makes the exemption self-invalidating: the named module must
# itself be compliant, so if it ever regresses this exemption fails with it
# rather than quietly covering for it. A `None` delegate is a standing
# exemption justified by `reason` alone.
EXEMPT = {
    "scripts/assess/assess_cell.py": {
        "delegates_to": None,
        "reason": "requires --db and actively refuses the canonical database; "
                  "honouring the variable would defeat that guard",
    },
    "scripts/audit/graph_audit.py": {
        "delegates_to": "scripts/audit/graph/build.py",
        "reason": "resolves the path through graph/build.py rather than itself",
    },
}


def _docstring_nodes(tree):
    """Constant-string nodes that are docstrings, so prose mentions don't count."""
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            body = getattr(node, "body", None)
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                out.add(id(body[0].value))
    return out


def _names_db_in_code(tree):
    docs = _docstring_nodes(tree)
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                and id(node) not in docs and DB_NAME in node.value):
            return True
    return False


def _calls_sqlite_connect(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr == "connect":
            return True
    return False


def _reads_env(tree):
    for node in ast.walk(tree):
        if (isinstance(node, ast.Constant) and isinstance(node.value, str)
                and node.value == ENV_VAR):
            return True
    return False


def audit():
    in_scope, offenders = [], []
    for path in sorted(REPO.glob("**/*.py")):
        rel = path.relative_to(REPO)
        if EXCLUDE_PARTS & set(rel.parts):
            continue
        if rel.parts[0] not in ("scripts", "tools"):
            continue
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        if not (_calls_sqlite_connect(tree) and _names_db_in_code(tree)):
            continue
        in_scope.append(rel)
        if not _reads_env(tree):
            offenders.append(rel)
    return in_scope, offenders


def main():
    in_scope, offenders = audit()
    compliant = {str(p) for p in in_scope if p not in offenders}

    real, exempted, stale = [], [], []
    for rel in offenders:
        key = str(rel)
        ex = EXEMPT.get(key)
        if ex is None:
            real.append(rel)
        elif ex["delegates_to"] and ex["delegates_to"] not in compliant:
            stale.append((rel, ex))          # the delegate regressed
        else:
            exempted.append((rel, ex))

    print("=" * 70)
    print(f"db_path_env_audit.py — {ENV_VAR} contract (CLAUDE.md §7)")
    print("=" * 70)
    print(f"in-scope scripts (connect to the canonical DB): {len(in_scope)}")
    for rel in in_scope:
        key = str(rel)
        if rel in real:
            mark = "FAIL"
        elif any(rel == r for r, _ in stale):
            mark = "STALE"
        elif key in EXEMPT:
            mark = "exempt"
        else:
            mark = "ok"
        print(f"  {mark:<6}  {rel}")

    for rel, ex in exempted:
        print(f"\nexempt: {rel}\n        {ex['reason']}")
    for rel, ex in stale:
        print(f"\nSTALE EXEMPTION: {rel}")
        print(f"        claims delegation to {ex['delegates_to']}, which no longer "
              f"honours {ENV_VAR}. Fix the delegate or drop the exemption.")

    if real or stale:
        n = len(real) + len(stale)
        print(f"\n{n} script(s) hardcode the database path and ignore {ENV_VAR}.")
        print('Fix: DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", <default>))')
        print("A script that ignores it will silently read the committed database "
              "while a test believes it is reading a scratch copy.")
        return 1

    print(f"\nRESULTS: {len(compliant)}/{len(in_scope)} honour {ENV_VAR} directly, "
          f"{len(exempted)} documented exemption(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
