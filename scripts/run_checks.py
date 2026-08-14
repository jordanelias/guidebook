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
# Two pointers, because one name was being asked to mean two different objects.
#
# `LATEST` answered "where did work leave off" (continuity) AND "which session's
# research should the mining gate check". Those diverge: on 2026-08-06 LATEST named
# a June continuity session while the most recent session that actually mined
# citations was 2026-07-26. The blocking `citation_mining_session` gate therefore
# scoped itself to a session that touched no sources and reported
# `Outstanding: 0` at 4.7% coverage — passing by having nothing in scope.
# CLAUDE.md §10 called both states meaningless, and it was right: left stale the
# gate validates a closed set, advanced to the newest session it reports zero by
# having nothing to check.
#
# A check declares which pointer it means via `session_pointer:` in the registry;
# the default is LATEST.
SESSION_POINTERS = {
    "LATEST":          os.path.join(REPO_ROOT, "sessions", "LATEST"),
    "LATEST-RESEARCH": os.path.join(REPO_ROOT, "sessions", "LATEST-RESEARCH"),
}
DEFAULT_SESSION_POINTER = "LATEST"
SESSION_POINTER = SESSION_POINTERS[DEFAULT_SESSION_POINTER]   # back-compat alias

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


def read_pointer(name=DEFAULT_SESSION_POINTER):
    """Session named by one of the pointers, or '' when it is absent."""
    try:
        with open(SESSION_POINTERS[name], encoding="utf-8") as fh:
            return fh.read().strip()
    except (OSError, KeyError):
        return ""


def current_session():
    """The continuity pointer. Kept for callers that mean 'where did work stop'."""
    return read_pointer(DEFAULT_SESSION_POINTER)


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
    PASS / FAIL / SKIP / ERROR.

    `session` is the continuity pointer. A check that means a different one
    declares `session_pointer:` in the registry and gets that instead — see the
    SESSION_POINTERS comment for why one name could not serve both.
    """
    pointer = check.get("session_pointer", DEFAULT_SESSION_POINTER)
    subject = session if pointer == DEFAULT_SESSION_POINTER else read_pointer(pointer)
    cmd = expand(check["cmd"], subject)
    if check.get("requires_session") and not subject:
        # A BLOCKING check with no subject FAILS. It used to SKIP, and SKIP is
        # excluded from the verdict even at blocking level — so deleting one
        # 60-byte pointer file silently switched off a blocking gate, and the run
        # still reported green. That is the disarming-by-omission this repo has
        # now produced five times, and it was living inside the dispatcher that
        # every other check depends on.
        #
        # Advisory checks still SKIP: an advisory result changes no verdict, so
        # failing one only adds noise. The severity of a missing subject is the
        # severity of the check that wanted it.
        if check.get("level", "blocking") == "blocking":
            return "FAIL", 0.0, (
                f"no sessions/{pointer} pointer, and this check is BLOCKING. "
                f"Its subject is missing, so it cannot report on anything — "
                f"which is a failure, not a pass. Restore the pointer or point "
                f"it at a session that exists.")
        return "SKIP", 0.0, (f"no sessions/{pointer} pointer — session-scoped check "
                             f"skipped")
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
        vacuity = vacuity_failure(check, output)
        if vacuity:
            return "FAIL", elapsed, f"{output}\n\nVACUITY GUARD: {vacuity}"
        if nothing_in_scope(output):
            return "NONE", elapsed, output
        return "PASS", elapsed, output
    if proc.returncode == 2 and check.get("optional_exit2"):
        return "SKIP", elapsed, output
    return "FAIL", elapsed, output


# Leading whitespace allowed. The anchor was column 0, which silently excluded
# every check that prints an indented summary block — `source_slug_links_
# duplicates` declared min_items, printed `  EXAMINED: 1011`, and was failed for
# "printing no EXAMINED line". A formatting convention is not what this contract
# is about; still anchored to line start so a mid-sentence "examined" cannot match.
# `EXAMINED: <n>` is a WHOLE-CHECK contract, not a per-subject one. It says how
# many items THIS CHECK looked at; a check whose EXAMINED lines are all zero is
# rendered NOTHING-IN-SCOPE. So a multi-subject check must never spend the token
# on one of its subjects: test_db_integrity runs 72 checks over the live DB and
# briefly printed `EXAMINED: 0` for the one subject that is empty
# (evidence_sources.tier), which relabelled the whole blocking gate as vacuous.
# A sub-check reports its subject in its own words.
EXAMINED_RE = re.compile(r"^\s*EXAMINED:\s*(\d+)\b", re.MULTILINE)

# Anchored to line start for the reason in `nothing_in_scope`: the phrase is
# discussed in prose all over this repo, and a check that merely *mentions* it
# must not be relabelled by it. Allows a `VERDICT: ` prefix, which is the form
# `citation_mining_completeness.py` and `verify_urls.py` print.
NOTHING_IN_SCOPE_RE = re.compile(r"^\s*(?:VERDICT:\s*)?NOTHING-IN-SCOPE\b", re.MULTILINE)


def vacuity_failure(check, output):
    """A check that examined nothing has not passed — it has abstained.

    `validate_schema` was BLOCKING and named six data/ subdirectories that have
    never existed. It found zero files, printed "No entity files found to
    validate." and exited 0, so the entity-schema gate reported green for its
    whole life while examining nothing. That is worse than no gate, because it is
    counted as coverage.

    Opt-in per check via `min_items:` in the registry, because some corpora are
    legitimately empty. A declared check must print `EXAMINED: <n>`; if it does
    not, that is itself the failure — an unverifiable count cannot be trusted to
    be non-zero. Deliberately a FAIL and not a SKIP: SKIP is excluded from the
    verdict even at blocking level, which would hide exactly what this catches.
    """
    minimum = check.get("min_items")
    if not minimum:
        return None
    match = EXAMINED_RE.search(output or "")
    if not match:
        return (f"declares min_items={minimum} but printed no 'EXAMINED: <n>' line, "
                "so the number of items it looked at cannot be established")
    seen = int(match.group(1))
    if seen < minimum:
        return (f"examined {seen} item(s), below the declared minimum of {minimum} — "
                "the check passed by having nothing to look at")
    return None


def nothing_in_scope(output):
    """True when a check exited 0 having examined nothing.

    Such a check has not passed — it abstained. `vacuity_failure` already turns
    that into a FAIL for the checks that declared a floor; this is the other half,
    for checks whose corpus is *legitimately* empty. They are correct, and they are
    still not evidence. Rendering them `[PASS]` is how a green run overstates its
    own coverage: 13 of 65 checks examine zero records today, five of them BLOCKING,
    and the runner reported all thirteen as earned green.

    The signal is the `EXAMINED:` line the checks already print — this adds no new
    convention and requires no script to change. `NOTHING-IN-SCOPE` is accepted as
    an equivalent verdict because `citation_mining_completeness.py` already speaks
    it, and it must be anchored to line start: the phrase appears in prose (this
    docstring included) and a mid-sentence mention must never relabel a result.

    Deliberately requires EVERY `EXAMINED:` line to be zero, not just the first.
    A check that examined 0 of one thing and 500 of another examined something,
    and calling that vacuous would be the same overstatement in the other
    direction. Narrower than `vacuity_failure`'s first-match rule on purpose: this
    predicate can only ever move a result out of PASS, so it must not guess.
    """
    counts = [int(m) for m in EXAMINED_RE.findall(output or "")]
    if counts:
        return max(counts) == 0
    return bool(NOTHING_IN_SCOPE_RE.search(output or ""))


def report_line(check, status, elapsed):
    level = check.get("level", "blocking")
    mark = {"PASS": "[PASS]", "FAIL": "[FAIL]", "SKIP": "[SKIP]",
            "ERROR": "[ERR ]", "NONE": "[NONE]"}[status]
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
    # Explicit kinds and a diff to classify are contradictory: one of them would be
    # silently discarded. It used to be --changed-from, which produced the worst
    # possible output — `--kinds "" --changed-from origin/main` reported "0 changed
    # file(s)" against a 12-file diff and ran 6 checks instead of 39. Fixing the
    # empty-kinds crash created that path, so this is a regression introduced while
    # removing one of the same family. preflight.sh forwards extra flags onto a
    # --changed-from invocation, so `preflight.sh --kinds ""` reaches it. Use
    # `--kinds auto` to mean "classify the diff for me".
    if args.kinds is not None and args.kinds != "auto" and args.changed_from:
        print("run_checks: --kinds and --changed-from are mutually exclusive "
              "(one would be silently ignored).", file=sys.stderr)
        print("  Use --kinds auto --changed-from REF to classify the diff, or pass "
              "--kinds alone.", file=sys.stderr)
        return 2

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
    failures, errors, skips, vacuous = [], [], [], []
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
            elif status in ("SKIP", "NONE"):
                print(f"         {output.splitlines()[-1] if output else 'skipped'}")

        if status == "SKIP":
            skips.append(check["id"])
        elif status == "NONE":
            vacuous.append((check["id"], level))
            if args.github:
                print(f"::notice::{check['id']} examined nothing ({level}) — "
                      f"clean, but not coverage")
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
    if vacuous:
        blocking_vacuous = [i for i, lv in vacuous if lv == "blocking"]
        print(f"NOTHING-IN-SCOPE ({len(vacuous)}): {', '.join(i for i, _ in vacuous)}")
        print("  These ran clean and examined nothing. They are not evidence of anything.")
        if blocking_vacuous:
            # The distinction the summary exists to make: a BLOCKING gate that
            # abstained let everything through. Whether that is fine (an empty
            # corpus) or a disarmed gate (a scoping predicate that matches
            # nothing) is a judgement, and it cannot be made if the line reads
            # [PASS]. Declaring `min_items` is how a check says which it is.
            print(f"  BLOCKING and vacuous ({len(blocking_vacuous)}): "
                  f"{', '.join(blocking_vacuous)} — a gate that examined nothing "
                  f"gated nothing.")
    if other_bad:
        print(f"NON-BLOCKING failures ({len(other_bad)}): {', '.join(other_bad)}")
    if blocking_bad:
        print(f"BLOCKING failures ({len(blocking_bad)}): {', '.join(blocking_bad)}")
        print("RESULT: FAIL")
        return 1
    print(f"RESULT: PASS — "
          f"{len(active) - len(skips) - len(other_bad) - len(vacuous)} check(s) green"
          f"{', ' + str(len(vacuous)) + ' nothing-in-scope' if vacuous else ''}"
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
    """C1-C8. Proves the registry is coherent and the classifier does what the
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

    # Regression: fixing the empty-kinds crash opened a path where --kinds "" beat
    # --changed-from, so a real diff reported "0 changed file(s)" and ran 6 checks
    # instead of 39 — loud-wrong traded for silent-wrong. Found by adversarial
    # review after the three cases above passed.
    # HEAD, not HEAD~1. A selftest must not depend on how deeply the repo was
    # cloned: with --depth 1 there is no HEAD~1 and this case failed with a git
    # error, so the registry selftest — a BLOCKING CI step — would have reported
    # the checkout depth as a registry defect. It passes today only because the
    # classify job happens to use fetch-depth: 0, an undeclared coupling. HEAD
    # exists in any repo with a commit; the diff is empty, which is all these two
    # cases need. Asserting on "changed file(s) vs" proves the classify path was
    # taken rather than the explicit-kinds one, so `auto` cannot silently become
    # a literal kind name.
    r = cli("--kinds", "", "--changed-from", "HEAD", "--dry-run")
    check("C6 --kinds with --changed-from is refused, not silently resolved",
          r.returncode == 2, f"exit {r.returncode}")

    r = cli("--kinds", "auto", "--changed-from", "HEAD", "--dry-run")
    check("C6 --kinds auto still takes the classify path",
          r.returncode == 0 and "changed file(s) vs" in r.stdout,
          f"exit {r.returncode}: {(r.stderr or r.stdout).strip()[:160]}")

    # --- C7: every check declares the authority it enforces ------------------
    # 51 of 57 checks could not say what they were for. A check with no stated
    # basis cannot be audited for relevance, cannot be retired with confidence,
    # and cannot answer the only question that matters of a governance
    # apparatus: is every contract actually enforced?
    #
    # `basis` is a pipeline-contract criterion id ("stage/criterion"), the literal
    # `hygiene` (encoding, parsing, structural sanity — no doctrinal authority is
    # needed to justify checking that JSON parses), or `unattributed`.
    # `unattributed` is ALLOWED and COUNTED, deliberately: forbidding it would
    # have meant inventing authorities for 29 checks in one sitting, which is how
    # a register fills up with plausible fiction. The count is printed so it can
    # be ratcheted down and so its direction is visible.
    missing = [c["id"] for c in reg["checks"] if not c.get("basis")]
    check("C7 every check declares a basis", not missing, str(missing[:5]))

    contract_ids = set()
    try:
        import yaml as _yaml
        _pc = _yaml.safe_load(open(os.path.join(REPO_ROOT, "governance",
                                                "pipeline-contract.yaml"), encoding="utf-8"))
        for _st in _pc.get("stages", []) or []:
            for _cr in _st.get("criteria", []) or []:
                contract_ids.add(f"{_st['id']}/{_cr['id']}")
        for _cs in _pc.get("cross_stage", []) or []:
            contract_ids.add(f"cross_stage/{_cs['id']}")
    except Exception as exc:  # noqa: BLE001
        contract_ids = None
        check("C7 pipeline contract is readable for basis resolution", False, str(exc))

    if contract_ids is not None:
        # `basis` may be a list: one check often enforces several criteria
        # (validate_evidence_state covers three judgment-stage rules), and
        # claiming only the first is how a criterion silently reads as unenforced.
        def _bases(entry):
            b = entry.get("basis")
            return b if isinstance(b, list) else [b]

        dangling = [(c["id"], b) for c in reg["checks"] for b in _bases(c)
                    if "/" in str(b) and b not in contract_ids]
        check("C7 every contract basis resolves to a real criterion",
              not dangling, str(dangling[:5]))

        # The reverse direction: a criterion whose enforcer is registered must be
        # claimed by that check's basis, or the two maps have drifted apart.
        claimed = {b for c in reg["checks"] for b in _bases(c) if "/" in str(b)}
        unclaimed = sorted(contract_ids - claimed)
        print(f"  [INFO] contract criteria with no check claiming them: "
              f"{len(unclaimed)} of {len(contract_ids)}")
        for cid in unclaimed:
            print(f"           {cid}")

    # --- C8: every check declares its vacuity regime -------------------------
    # A6's sweep declares `min_items` or `no_floor` on all 65 checks. Without this
    # assertion that sweep is a snapshot: check 66 is added with neither, reports
    # [PASS] on an empty corpus, and the repo runs its named recurring failure mode
    # a fifth time. C8 is the structural half — it makes the declaration a
    # condition of registration rather than a thing someone remembered.
    #
    # `no_floor` carries a REASON, not `true`. "This corpus is legitimately empty"
    # is a claim about the world that someone should have to write down and a
    # reviewer should be able to disagree with; a bare boolean is unfalsifiable.
    undeclared = [c["id"] for c in reg["checks"]
                  if "min_items" not in c and "no_floor" not in c]
    check("C8 every check declares min_items or no_floor", not undeclared,
          f"{len(undeclared)} undeclared: {undeclared[:5]}")

    both = [c["id"] for c in reg["checks"] if "min_items" in c and "no_floor" in c]
    check("C8 no check declares both a floor and no_floor", not both, str(both[:5]))

    # Must be a STRING with something in it. `no_floor: true` is the failure this
    # assertion exists for, and the first version of it passed `true` — YAML parses
    # it to a bool, `str(True)` is a non-empty string, and the guard waved it
    # through while its own comment said it would not. Caught by mutation-testing
    # the assertion rather than by reading it.
    bare = [c["id"] for c in reg["checks"]
            if "no_floor" in c
            and (not isinstance(c["no_floor"], str) or len(c["no_floor"].strip()) < 12)]
    check("C8 every no_floor states a reason, not a bare true", not bare, str(bare[:5]))

    floored = [c for c in reg["checks"] if "min_items" in c]
    print(f"  [INFO] checks with a real floor: {len(floored)} of "
          f"{len(reg['checks'])} — every no_floor is a corpus that cannot yet "
          f"falsify its check; ratchet this up as the corpus fills")

    unattributed = [c["id"] for c in reg["checks"] if c.get("basis") == "unattributed"]
    print(f"  [INFO] checks with no stated authority: {len(unattributed)} of "
          f"{len(reg['checks'])} — ratchet this down, do not invent authorities")

    print("=" * 78)
    if failures:
        print(f"SELFTEST: FAIL — {len(failures)} check(s): {', '.join(failures)}")
        return 1
    print("SELFTEST: PASS — registry coherent, classifier and selector behave as documented.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
