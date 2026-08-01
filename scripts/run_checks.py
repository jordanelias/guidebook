#!/usr/bin/env python3
"""
scripts/run_checks.py — the single entry point for every ecosystem check.

Reads governance/check-registry.yaml, works out which checks the current change
actually warrants, runs them, and reports. CI and scripts/preflight.sh both call
this, so there is one list of checks in the repo rather than four hand-kept ones
that drift apart.

WHAT "GATING" MEANS HERE
------------------------
Each check declares the WORK KINDS it is relevant to (data / schema / synthesis /
governance / render / tooling, or `always`). This script classifies a diff into
kinds and runs the intersection. A docs-only change runs the always-on checks; a
data change runs the DB, schema and freshness batteries; a synthesis change runs
the judgment and attestation batteries.

Checks:
  C1  registry parses and every check id is unique
  C2  every referenced battery is declared
  C3  every check's executable exists on disk (catches a rename that skipped its
      caller sweep — architecture v2.3 <migration_and_growth>)
  C4  path classification maps representative paths to the expected kinds
  C5  selection honours kinds, batteries and `always`
  (C1-C5 are the --selftest. A gate nobody has watched fire is not a gate.)

Usage:
    python3 scripts/run_checks.py --changed-from origin/main   # gate a branch
    python3 scripts/run_checks.py --all                        # everything
    python3 scripts/run_checks.py --kinds data,schema          # explicit kinds
    python3 scripts/run_checks.py --battery schema --kinds data
    python3 scripts/run_checks.py --list                       # registry table
    python3 scripts/run_checks.py --explain --changed-from HEAD~1
    python3 scripts/run_checks.py --selftest

Exit codes:
    0  no blocking check failed
    1  at least one blocking check failed
    2  the runner itself could not run (bad registry, bad arguments)

Honours GUIDEBOOK_DB_PATH (default data/guidebook.db), per the repo-wide contract
enforced by scripts/audit/db_path_env_audit.py.
"""

import argparse
import os
import re
import subprocess
import sys
import time

try:
    import yaml
except ImportError:
    print("run_checks: PyYAML is required (pip install -r requirements.txt)", file=sys.stderr)
    sys.exit(2)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGISTRY = os.path.join(REPO_ROOT, "governance", "check-registry.yaml")
SESSION_POINTER = os.path.join(REPO_ROOT, "sessions", "LATEST")

LEVELS = ("blocking", "advisory", "informational")


# ---------------------------------------------------------------- registry ---

def load_registry(path=REGISTRY):
    with open(path, encoding="utf-8") as fh:
        reg = yaml.safe_load(fh)
    for key in ("kinds", "batteries", "checks"):
        if key not in reg:
            raise ValueError(f"check-registry.yaml missing top-level key: {key}")
    return reg


def glob_to_re(pattern):
    """Translate a registry path glob to a regex.

    `**` crosses directory separators; `*` and `?` do not. fnmatch is not usable
    here because its `*` also crosses separators, which would make `tools/*.html`
    match `tools/nested/x.html`.
    """
    out, i = [], 0
    while i < len(pattern):
        ch = pattern[i]
        if pattern.startswith("**", i):
            out.append(".*")
            i += 2
        elif ch == "*":
            out.append("[^/]*")
            i += 1
        elif ch == "?":
            out.append("[^/]")
            i += 1
        else:
            out.append(re.escape(ch))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def classify(paths, reg):
    """Map changed paths to work kinds. First matching kind wins per path."""
    compiled = [
        (name, [glob_to_re(p) for p in spec.get("paths", [])])
        for name, spec in reg["kinds"].items()
    ]
    kinds, attribution = set(), {}
    for path in paths:
        path = path.strip()
        # Strip a leading "./" PREFIX only. `lstrip("./")` strips those two
        # characters in any order, which silently turns ".github/workflows/ci.yml"
        # into "github/workflows/ci.yml" and misclassifies every workflow edit.
        if path.startswith("./"):
            path = path[2:]
        if not path:
            continue
        for name, regexes in compiled:
            if any(rx.match(path) for rx in regexes):
                kinds.add(name)
                attribution.setdefault(name, []).append(path)
                break
        else:
            attribution.setdefault("(unclassified)", []).append(path)
    return kinds, attribution


def changed_paths(base):
    """Files changed between `base` and the working tree."""
    merge_base = base
    probe = subprocess.run(
        ["git", "merge-base", base, "HEAD"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    if probe.returncode == 0 and probe.stdout.strip():
        merge_base = probe.stdout.strip()
    result = subprocess.run(
        ["git", "diff", "--name-only", merge_base],
        cwd=REPO_ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git diff against {base!r} failed: {result.stderr.strip()}")
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard"],
        cwd=REPO_ROOT, capture_output=True, text=True,
    ).stdout
    return [p for p in (result.stdout + untracked).splitlines() if p.strip()]


def current_session():
    try:
        with open(SESSION_POINTER, encoding="utf-8") as fh:
            return fh.read().strip()
    except OSError:
        return ""


def select(reg, kinds, batteries=None, levels=None, run_all=False):
    """Choose checks. Returns [(check, selected: bool, why: str)]."""
    chosen = []
    for check in reg["checks"]:
        ck = set(check.get("kinds", []))
        if run_all:
            ok, why = True, "--all"
        elif "always" in ck:
            ok, why = True, "always"
        elif ck & kinds:
            ok, why = True, "kind:" + ",".join(sorted(ck & kinds))
        else:
            ok, why = False, "no matching kind (declares " + ",".join(sorted(ck)) + ")"
        if ok and batteries and check.get("battery") not in batteries:
            ok, why = False, f"battery {check.get('battery')!r} not requested"
        if ok and levels and check.get("level", "blocking") not in levels:
            ok, why = False, f"level {check.get('level')!r} not requested"
        chosen.append((check, ok, why))
    return chosen


# ------------------------------------------------------------------- runner ---

def expand(cmd, session):
    return [part.replace("@SESSION@", session) for part in cmd]


def run_check(check, session, env, github=False):
    """Run one check. Returns (status, seconds, output) with status in
    PASS / FAIL / SKIP / ERROR."""
    cmd = expand(check["cmd"], session)
    if check.get("requires_session") and not session:
        return "SKIP", 0.0, "no sessions/LATEST pointer — session-scoped check skipped"
    exe = cmd[1] if cmd[0] in ("python3", "python", "node") else cmd[0]
    if not os.path.exists(os.path.join(REPO_ROOT, exe)):
        return "ERROR", 0.0, f"executable not found: {exe}"

    started = time.time()
    try:
        proc = subprocess.run(
            cmd, cwd=REPO_ROOT, capture_output=True, text=True, env=env, timeout=900
        )
    except subprocess.TimeoutExpired:
        return "ERROR", time.time() - started, "timed out after 900s"
    except FileNotFoundError as exc:
        if check.get("optional_exit2"):
            return "SKIP", time.time() - started, f"interpreter unavailable: {exc}"
        return "ERROR", time.time() - started, f"could not launch: {exc}"

    elapsed = time.time() - started
    output = (proc.stdout + proc.stderr).strip()
    if proc.returncode == 0:
        return "PASS", elapsed, output
    if proc.returncode == 2 and check.get("optional_exit2"):
        return "SKIP", elapsed, output
    return "FAIL", elapsed, output


def report_line(check, status, elapsed):
    level = check.get("level", "blocking")
    mark = {"PASS": "[PASS]", "FAIL": "[FAIL]", "SKIP": "[SKIP]", "ERROR": "[ERR ]"}[status]
    suffix = "" if level == "blocking" else f"  ({level})"
    return f"{mark} {check['id']:38} {elapsed:6.1f}s{suffix}"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--changed-from", metavar="REF",
                    help="classify the diff against REF (e.g. origin/main)")
    ap.add_argument("--kinds", help="comma-separated work kinds, or 'auto' with --changed-from")
    ap.add_argument("--all", action="store_true", help="run every active check")
    ap.add_argument("--battery", help="comma-separated batteries to run")
    ap.add_argument("--level", help="comma-separated levels to run (blocking/advisory/informational)")
    ap.add_argument("--list", action="store_true", help="print the registry and exit")
    ap.add_argument("--explain", action="store_true", help="show why each check was or was not selected")
    ap.add_argument("--github", action="store_true", help="emit GitHub Actions annotations and a step summary")
    ap.add_argument("--selftest", action="store_true", help="verify the registry and the classifier")
    ap.add_argument("--print-plan", action="store_true",
                    help="emit ONLY `kinds=`/`batteries=` lines for $GITHUB_OUTPUT, run nothing")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the plan and the selection, run nothing (pairs with --explain)")
    ap.add_argument("--registry", default=REGISTRY)
    args = ap.parse_args()

    try:
        reg = load_registry(args.registry)
    except Exception as exc:                                   # noqa: BLE001
        print(f"run_checks: cannot load registry: {exc}", file=sys.stderr)
        return 2

    if args.selftest:
        return selftest(reg)

    if args.list:
        return do_list(reg)

    # --- work out kinds -----------------------------------------------------
    kinds, attribution, paths = set(), {}, []
    # `is not None`, not truthiness: `--kinds ""` is the docs-only case (a diff that
    # matched no kind) and must mean "select the always-on checks", which is exactly
    # what select() already does with an empty set. Testing truthiness made an empty
    # --kinds indistinguishable from an absent one, so it fell through to ap.error()
    # and exited 2 — CI passes `--kinds "$KINDS"` unquoted-empty on any docs-only
    # diff, so three battery jobs died on an argparse usage error while the six
    # always-on checks they were supposed to run did not run at all.
    if args.kinds is not None and args.kinds != "auto":
        kinds = {k.strip() for k in args.kinds.split(",") if k.strip()}
        unknown = kinds - set(reg["kinds"]) - {"always"}
        if unknown:
            print(f"run_checks: unknown kind(s): {', '.join(sorted(unknown))}", file=sys.stderr)
            print(f"  known: {', '.join(reg['kinds'])}", file=sys.stderr)
            return 2
    elif args.changed_from:
        try:
            paths = changed_paths(args.changed_from)
        except RuntimeError as exc:
            print(f"run_checks: {exc}", file=sys.stderr)
            return 2
        kinds, attribution = classify(paths, reg)
    elif not args.all:
        ap.error("give one of --all, --kinds, or --changed-from")

    batteries = {b.strip() for b in args.battery.split(",")} if args.battery else None
    levels = {l.strip() for l in args.level.split(",")} if args.level else None

    session = current_session()
    env = dict(os.environ)
    env.setdefault("GUIDEBOOK_DB_PATH", "data/guidebook.db")

    selection = select(reg, kinds, batteries, levels, run_all=args.all)
    active = [c for c, ok, _ in selection if ok]

    if args.print_plan:
        # Consumed by ci.yml's `classify` job. Battery jobs gate on `batteries` so
        # a job with nothing to do is never spun up at all.
        wanted = sorted({c.get("battery") for c in active if c.get("battery")})
        print(f"kinds={','.join(sorted(kinds))}")
        print(f"batteries={','.join(wanted)}")
        print(f"checks={len(active)}")
        print(f"paths={len(paths)}")
        return 0

    # --- header -------------------------------------------------------------
    print("=" * 78)
    if args.all:
        print("run_checks: --all — every active check in the registry")
    elif args.changed_from:
        print(f"run_checks: {len(paths)} changed file(s) vs {args.changed_from}")
        print(f"  work kinds: {', '.join(sorted(kinds)) or '(none — docs-only change)'}")
        for kind, files in sorted(attribution.items()):
            sample = ", ".join(files[:3]) + (f", +{len(files) - 3} more" if len(files) > 3 else "")
            print(f"    {kind:16} {sample}")
    else:
        print(f"run_checks: kinds = {', '.join(sorted(kinds))}")
    if batteries:
        print(f"  batteries: {', '.join(sorted(batteries))}")
    print(f"  selected {len(active)} of {len(reg['checks'])} registered checks"
          f"  ({len(reg.get('quarantine', []))} quarantined, never selected)")
    print("=" * 78)

    if args.explain:
        for check, ok, why in selection:
            print(f"  {'RUN ' if ok else 'skip'} {check['id']:38} {why}")
        print("-" * 78)

    if args.dry_run:
        print("--dry-run: nothing was executed.")
        return 0

    # --- run ----------------------------------------------------------------
    failures, errors, skips = [], [], []
    for check in active:
        if args.github:
            print(f"::group::{check['id']}")
        status, elapsed, output = run_check(check, session, env, args.github)
        line = report_line(check, status, elapsed)
        level = check.get("level", "blocking")

        if args.github:
            print(output)
            print("::endgroup::")
            print(line)
        else:
            print(line)
            if status in ("FAIL", "ERROR"):
                for tail in output.splitlines()[-8:]:
                    print(f"         {tail}")
            elif status == "SKIP":
                print(f"         {output.splitlines()[-1] if output else 'skipped'}")

        if status == "SKIP":
            skips.append(check["id"])
        elif status == "ERROR":
            errors.append((check["id"], level))
        elif status == "FAIL":
            failures.append((check["id"], level))
            if args.github:
                sev = "error" if level == "blocking" else "warning"
                print(f"::{sev}::{check['id']} failed ({level})")

    # --- verdict ------------------------------------------------------------
    blocking_bad = [i for i, lv in failures + errors if lv == "blocking"]
    other_bad = [i for i, lv in failures + errors if lv != "blocking"]

    print("=" * 78)
    if skips:
        print(f"SKIPPED ({len(skips)}): {', '.join(skips)}")
        print("  A skipped check did NOT run. It is not a pass.")
    if other_bad:
        print(f"NON-BLOCKING failures ({len(other_bad)}): {', '.join(other_bad)}")
    if blocking_bad:
        print(f"BLOCKING failures ({len(blocking_bad)}): {', '.join(blocking_bad)}")
        print("RESULT: FAIL")
        return 1
    print(f"RESULT: PASS — {len(active) - len(skips) - len(other_bad)} check(s) green"
          f"{', ' + str(len(other_bad)) + ' advisory failure(s)' if other_bad else ''}")
    return 0


def do_list(reg):
    print(f"{'id':40} {'battery':12} {'level':14} kinds")
    print("-" * 100)
    for check in reg["checks"]:
        print(f"{check['id']:40} {check.get('battery',''):12} "
              f"{check.get('level','blocking'):14} {','.join(check.get('kinds', []))}")
    print()
    print("QUARANTINED (registered, never selected):")
    for entry in reg.get("quarantine", []):
        reason = " ".join(entry.get("reason", "").split())
        print(f"  {entry['id']:40} {entry.get('status','quarantined'):12} {reason[:120]}")
    return 0


# ----------------------------------------------------------------- selftest ---

def selftest(reg):
    """C1-C5. Proves the registry is coherent and the classifier does what the
    comments claim — the repo's "passes count only after demonstrated firing" norm."""
    failures = []

    def check(label, condition, detail=""):
        if condition:
            print(f"  [PASS] {label}")
        else:
            print(f"  [FAIL] {label}{': ' + detail if detail else ''}")
            failures.append(label)

    print("=" * 78)
    print("run_checks --selftest")
    print("=" * 78)

    # C1 — unique ids
    ids = [c["id"] for c in reg["checks"]]
    dupes = {i for i in ids if ids.count(i) > 1}
    check("C1 check ids are unique", not dupes, ", ".join(sorted(dupes)))

    q_ids = [e["id"] for e in reg.get("quarantine", [])]
    overlap = set(ids) & set(q_ids)
    check("C1b no id is both active and quarantined", not overlap, ", ".join(sorted(overlap)))

    # C2 — batteries declared
    declared = set(reg["batteries"])
    used = {c.get("battery") for c in reg["checks"]}
    check("C2 every referenced battery is declared", used <= declared,
          f"undeclared: {', '.join(sorted(used - declared))}")

    # C3 — executables exist (the caller-sweep guard)
    missing = []
    for entry in reg["checks"] + reg.get("quarantine", []):
        cmd = entry["cmd"]
        exe = cmd[1] if cmd[0] in ("python3", "python", "node") else cmd[0]
        if not os.path.exists(os.path.join(REPO_ROOT, exe)):
            missing.append(f"{entry['id']} -> {exe}")
    check("C3 every registered executable exists on disk", not missing, "; ".join(missing))

    # C4 — classification
    cases = [
        ("data/guidebook.db", "data"),
        ("data/decisions/decision_register.yaml", "data"),
        ("schemas/item.py", "schema"),
        ("scripts/migrations/013_x.sql", "schema"),
        ("governance/mission-and-epistemics.md", "governance"),
        ("decisions/DR-2026-08-01-x.md", "governance"),
        ("references/project-standards.md", "governance"),
        ("references/bpc-reasoning/x.md", "synthesis"),
        ("references/connection-reasoning/CON-1.md", "synthesis"),
        ("sessions/LATEST", "synthesis"),
        ("parts/v10/part04.md", "render"),
        ("tools/evidentiary-audit-dashboard.html", "render"),
        ("scripts/validate_bpc.py", "tooling"),
        (".github/workflows/ci.yml", "tooling"),
        ("requirements.txt", "tooling"),
    ]
    for path, expected in cases:
        kinds, _ = classify([path], reg)
        check(f"C4 {path} -> {expected}", kinds == {expected}, f"got {kinds or '{}'}")

    # A README at the root is nobody's work kind; it must classify to nothing.
    kinds, _ = classify(["README.md"], reg)
    check("C4 README.md -> no kind (docs-only)", kinds == set(), f"got {kinds}")

    # `**` crosses separators, plain `*` must not.
    kinds, _ = classify(["tools/nested/deep.html"], reg)
    check("C4 tools/nested/deep.html is NOT render (single-* must not cross '/')",
          "render" not in kinds, f"got {kinds}")

    # C5 — selection
    sel = {c["id"] for c, ok, _ in select(reg, set()) if ok}
    always = {c["id"] for c in reg["checks"] if "always" in c.get("kinds", [])}
    check("C5 empty kind set selects exactly the always-on checks", sel == always,
          f"got {sorted(sel ^ always)}")

    sel_data = {c["id"] for c, ok, _ in select(reg, {"data"}) if ok}
    check("C5 kind 'data' selects the reproducibility gate",
          "migration_reproducibility" in sel_data)
    check("C5 kind 'data' does not select render-only browser audit",
          "render_audit_browser" not in sel_data)

    sel_syn = {c["id"] for c, ok, _ in select(reg, {"synthesis"}) if ok}
    check("C5 kind 'synthesis' selects validate_evidence_state (2026-07-23 plan F2)",
          "validate_evidence_state" in sel_syn)
    check("C5 kind 'synthesis' selects the attestation checks",
          {"attestation_presence", "attestation_schema"} <= sel_syn)

    sel_bat = {c["id"] for c, ok, _ in select(reg, {"data"}, batteries={"schema"}) if ok}
    check("C5 battery filter narrows to one battery",
          all(next(c for c in reg["checks"] if c["id"] == i)["battery"] == "schema"
              for i in sel_bat) and sel_bat)

    sel_all = {c["id"] for c, ok, _ in select(reg, set(), run_all=True) if ok}
    check("C5 --all selects every active check", sel_all == set(ids))

    # No quarantined entry is reachable by any selection.
    check("C5 quarantined checks are unreachable by --all", not (sel_all & set(q_ids)))

    # Levels are spelled correctly, or the runner's verdict logic silently mis-sorts.
    bad_levels = {c["id"]: c.get("level") for c in reg["checks"]
                  if c.get("level", "blocking") not in LEVELS}
    check("C5 every level is one of blocking/advisory/informational", not bad_levels,
          str(bad_levels))

    # --- C6: the CLI layer, not just the selector ---------------------------
    # C5 asserted that an empty kind set selects the always-on checks, and it was
    # true — while `--kinds ""` still exited 2 on an argparse usage error, because
    # empty-string kinds were tested for truthiness and so read as "not supplied".
    # Every docs-only diff hit that path in CI. The selector was right and the
    # entry point was wrong, so testing select() in isolation could not see it.
    # These cases drive the real command line.
    def cli(*argv):
        return subprocess.run([sys.executable, os.path.abspath(__file__), *argv],
                              capture_output=True, text=True, timeout=120)

    r = cli("--kinds", "", "--dry-run")
    check("C6 --kinds '' is the docs-only case, not a usage error", r.returncode == 0,
          f"exit {r.returncode}: {r.stderr.strip()[:200]}")

    r = cli("--kinds", "", "--dry-run", "--explain")
    planned = sum(1 for ln in r.stdout.splitlines() if ln.strip().startswith("RUN "))
    always_n = len([c for c in reg["checks"] if "always" in c.get("kinds", [])])
    check("C6 --kinds '' still plans the always-on checks", planned == always_n,
          f"planned {planned}, expected {always_n}")

    r = cli("--dry-run")
    check("C6 omitting all selectors is still a usage error", r.returncode == 2,
          f"exit {r.returncode}")

    print("=" * 78)
    if failures:
        print(f"SELFTEST: FAIL — {len(failures)} check(s): {', '.join(failures)}")
        return 1
    print("SELFTEST: PASS — registry coherent, classifier and selector behave as documented.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
