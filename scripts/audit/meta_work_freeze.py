#!/usr/bin/env python3
"""
scripts/audit/meta_work_freeze.py — the meta-work freeze, made mechanical.

DR-2026-08-19 §2.2, ratified 2026-08-19. Until `evidence_sources` holds at least
one admitted source, this changeset may not:

  1. add a file under `workplan/`
  2. add a new entry to `governance/check-registry.yaml`

Corrections to existing instances are explicitly excepted, so this compares
ADDED files and ADDED check ids, never modifications.

WHY A CHECK AND NOT A RULE
--------------------------
A governance freeze already existed. `workplan/next-steps-synthesis-2026-07-14.md`
§2.6 declared one with a prose tripwire, it was ratified into
`DR-2026-07-21`, its firing condition was met every week for five weeks, and no
session ever checked it. Prose tripwires do not fire. This one is build-rejected.

SELF-EXPIRING
-------------
The freeze has no lift ceremony to be planned, breached or adjudicated. It ends
the moment `evidence_sources` is non-empty — this check then passes
unconditionally and can be retired at leisure rather than repealed.
"""

import argparse
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", "data/guidebook.db"))
REGISTRY = "governance/check-registry.yaml"

# This check's own registry entry. DR-2026-08-19 §2.5(c) requires the check to
# land in the SAME commit as the ratification it enforces, so counting itself
# would make the ratifying PR unmergeable — the deadlock CLAUDE.md §7 warns
# about, built in on day one. Nothing else may be added here without a DR.
SELF_EXEMPT = {"meta_work_freeze"}


def git(*args):
    r = subprocess.run(["git"] + list(args), capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def resolve_base(base):
    """Resolve the comparison base, or return None.

    Default order is origin/main, then main, then HEAD~1 — NOT HEAD~1 first.
    The subject is "what does this branch propose to add to main", which is what
    a PR diff means and what run_checks.py itself classifies against
    (--changed-from origin/main). Defaulting to HEAD~1 made the check judge
    whatever a merge commit happened to bring in, so on a pre-ratification merge
    it flagged a plan file added days before the freeze existed. A freeze that
    convicts history it could not have governed is the deadlock trap CLAUDE.md §7
    warns about, and it would have made this very PR unmergeable.

    A blocking gate that cannot see its subject must FAIL, not pass — SKIP on a
    missing subject is how this repository has repeatedly shipped a green check
    that examined nothing (CLAUDE.md §10).
    """
    candidates = [base] if base else ["origin/main", "main", "HEAD~1"]
    for candidate in candidates + ["origin/main", "main"]:
        if not candidate:
            continue
        rc, out, _ = git("rev-parse", "--verify", "--quiet", candidate + "^{commit}")
        if rc == 0 and out.strip():
            return candidate
    return None


def worktree_added_workplan():
    """Files under workplan/ added but not yet committed (staged or untracked).

    Without this the local gate passes on an uncommitted plan and only refuses it
    after the commit exists — which is exactly when it is most annoying to undo.
    """
    rc, out, _ = git("status", "--porcelain", "--", "workplan/")
    if rc != 0:
        return []
    found = []
    for line in out.splitlines():
        if not line.strip():
            continue
        code, _, path = line[:2], line[2:3], line[3:].strip()
        if code in ("??", "A ", "AM", " A"):
            found.append(path + "  (uncommitted)")
    return found


def registry_ids(ref):
    """The set of check ids in the registry at `ref`, or None if unreadable."""
    import yaml
    if ref is None:
        text = Path(REGISTRY).read_text(encoding="utf-8")
    else:
        rc, out, _ = git("show", f"{ref}:{REGISTRY}")
        if rc != 0:
            return None
        text = out
    try:
        doc = yaml.safe_load(text) or {}
    except yaml.YAMLError:
        return None
    return {c.get("id") for c in (doc.get("checks") or []) if c.get("id")}


def audit(base, head):
    evidence = 0
    if DB_PATH.exists():
        cx = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        try:
            evidence = cx.execute("SELECT COUNT(*) FROM evidence_sources").fetchone()[0]
        except sqlite3.Error:
            evidence = 0
        cx.close()

    print("=" * 78)
    print("META-WORK FREEZE — DR-2026-08-19 §2.2")
    print("=" * 78)

    if evidence >= 1:
        print(f"  evidence_sources = {evidence}")
        print("  EXAMINED: 1")
        print("\n  LIFTED — the freeze expired by its own terms. One admitted source "
              "exists,\n  so new apparatus is no longer being built instead of research.")
        return 0

    resolved = resolve_base(base)
    if resolved is None:
        print(f"  ERROR: cannot resolve a comparison base (tried {base!r}, "
              "'origin/main', 'main').")
        print("  EXAMINED: 0")
        print("\n  A blocking gate that cannot see its subject FAILS rather than passing.")
        print("  In CI this usually means the clone is too shallow: fetch more depth.")
        return 1

    rc, out, err = git("diff", "--diff-filter=A", "--name-only", resolved, head, "--", "workplan/")
    if rc != 0:
        print(f"  ERROR: git diff failed: {err.strip()}")
        print("  EXAMINED: 0")
        return 1
    added_workplan = [p for p in out.splitlines() if p.strip()] + worktree_added_workplan()

    base_ids = registry_ids(resolved)
    head_ids = registry_ids(None)
    if head_ids is None:
        print(f"  ERROR: {REGISTRY} is unreadable at the working tree.")
        print("  EXAMINED: 0")
        return 1
    if base_ids is None:
        # The registry did not exist at base, or did not parse. Treat every id as
        # new rather than waving it through.
        base_ids = set()
    added_checks = sorted((head_ids - base_ids) - SELF_EXEMPT)

    examined = len(added_workplan) + len(head_ids)
    print(f"  base: {resolved}    head: {head}")
    print(f"  evidence_sources = {evidence}  → freeze ACTIVE")
    print(f"  added files under workplan/ : {len(added_workplan)}")
    print(f"  check ids in registry       : {len(head_ids)} "
          f"({len(head_ids - base_ids)} added, {len(SELF_EXEMPT & (head_ids - base_ids))} self-exempt)")
    print(f"  EXAMINED: {examined}")

    if not added_workplan and not added_checks:
        print("\n  CLEAN — this changeset adds no plan and no check.")
        return 0

    print("\n" + "-" * 78)
    for path in added_workplan:
        print(f"  ✗ new workplan file: {path}")
    for cid in added_checks:
        print(f"  ✗ new registry check: {cid}")
    print("-" * 78)
    print("\n  FROZEN. Until one source is admitted, the apparatus does not grow.")
    print("  DR-2026-08-19 §2.2. Correct an existing document or check instead —")
    print("  modifications are explicitly excepted; only additions are refused.")
    print("  The freeze lifts automatically at evidence_sources >= 1. The next")
    print("  artifact this project owes is a search log, not a plan.")
    return 1


def selftest():
    """Prove the three behaviours, in a throwaway git repo."""
    import tempfile, shutil, textwrap
    global DB_PATH
    results, failures = [], 0

    def check(name, cond, detail=""):
        nonlocal failures
        results.append((name, bool(cond), detail))
        if not cond:
            failures += 1

    real_db, cwd = DB_PATH, os.getcwd()
    tmp = tempfile.mkdtemp()
    try:
        os.chdir(tmp)
        git("init", "-q", "-b", "main")
        git("config", "user.email", "t@t"); git("config", "user.name", "t")
        Path("governance").mkdir(); Path("workplan").mkdir()
        reg = "checks:\n  - id: alpha\n    battery: syntax\n"
        Path(REGISTRY).write_text(reg)
        Path("workplan/old.md").write_text("existing\n")
        git("add", "-A"); git("commit", "-qm", "base")

        # OUTSIDE the repo: `git add -A` would otherwise track the fixture DB and
        # `git reset --hard` would then delete it mid-test.
        dbdir = tempfile.mkdtemp()
        db = Path(dbdir) / "t.db"
        con = sqlite3.connect(str(db)); con.execute("CREATE TABLE evidence_sources (ref_id TEXT)")
        con.commit(); con.close()
        DB_PATH = db

        check("clean changeset passes", audit("HEAD", "HEAD") == 0)

        Path("workplan/new-plan.md").write_text("a new plan\n")
        git("add", "-A"); git("commit", "-qm", "adds plan")
        check("new workplan file refused", audit("HEAD~1", "HEAD") == 1)

        git("reset", "-q", "--hard", "HEAD~1")
        Path(REGISTRY).write_text(reg + "  - id: beta\n    battery: syntax\n")
        git("add", "-A"); git("commit", "-qm", "adds check")
        check("new registry check refused", audit("HEAD~1", "HEAD") == 1)

        Path(REGISTRY).write_text(reg.replace("battery: syntax", "battery: structure"))
        git("add", "-A"); git("commit", "-qm", "corrects existing")
        check("correction to an existing check allowed", audit("HEAD~1", "HEAD") == 0)

        git("reset", "-q", "--hard", "HEAD~1")
        Path(REGISTRY).write_text(reg + "  - id: meta_work_freeze\n    battery: governance\n")
        git("add", "-A"); git("commit", "-qm", "adds the freeze check itself")
        check("the freeze check does not block its own introduction",
              audit("HEAD~1", "HEAD") == 0)

        Path("workplan/uncommitted.md").write_text("not yet committed\n")
        check("uncommitted workplan file refused", audit("HEAD", "HEAD") == 1)
        os.unlink("workplan/uncommitted.md")
        check("clean again once removed", audit("HEAD", "HEAD") == 0)


        con = sqlite3.connect(str(db)); con.execute("INSERT INTO evidence_sources VALUES ('REF-1')")
        con.commit(); con.close()
        Path("workplan/another.md").write_text("x\n")
        git("add", "-A"); git("commit", "-qm", "plan after a source exists")
        check("freeze lifts once one source is admitted", audit("HEAD~1", "HEAD") == 0)

        # Base resolution: an unknown ref falls back to main rather than silently
        # comparing against nothing...
        check("unknown base falls back to a real ref",
              resolve_base("no-such-ref-xyz") == "main",
              repr(resolve_base("no-such-ref-xyz")))
        # ...and when nothing resolves at all, the gate FAILS instead of passing.
        outside = tempfile.mkdtemp()
        os.chdir(outside)
        check("no resolvable base at all → None", resolve_base("no-such-ref-xyz") is None)
        DB_PATH = Path(outside) / "absent.db"
        check("unresolvable base fails the gate", audit("no-such-ref-xyz", "HEAD") == 1)
        os.chdir(tmp)
        shutil.rmtree(outside, ignore_errors=True)
    finally:
        DB_PATH = real_db
        os.chdir(cwd)
        shutil.rmtree(tmp, ignore_errors=True)
        try:
            shutil.rmtree(dbdir, ignore_errors=True)
        except NameError:
            pass

    print("\n--- meta_work_freeze selftest ---")
    for name, ok, detail in results:
        print("  %s: %s%s" % ("PASS" if ok else "**FAIL**", name,
                              ("  [%s]" % detail) if not ok else ""))
    print("\nRESULTS: %d/%d selftest cases pass" % (len(results) - failures, len(results)))
    print("SELFTEST: %s" % ("FAIL" if failures else "PASS"))
    return 1 if failures else 0


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--base", default=None,
                   help="Comparison base (default: origin/main, then main, then HEAD~1)")
    p.add_argument("--head", default="HEAD", help="Comparison head (default HEAD)")
    p.add_argument("--selftest", action="store_true", help="Run the behaviour tests and exit")
    args = p.parse_args()
    if args.selftest:
        sys.exit(selftest())
    sys.exit(audit(args.base, args.head))


if __name__ == "__main__":
    main()
