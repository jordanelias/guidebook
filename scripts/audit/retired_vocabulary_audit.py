#!/usr/bin/env python3
"""
scripts/audit/retired_vocabulary_audit.py — flag text that is READABLE AND WRONG.

WHY THIS EXISTS
---------------
The expensive failure in this repo is not that old files exist. It is that a
session greps for a fact, gets several answers, and cannot tell which is
current. Three worked examples, all real:

  * `audit.yml` was folded into `ci.yml` on 2026-08-01. Dozens of live documents
    still name it. CLAUDE.md §0 named it too, and in doing so contradicted its
    own §7 two hundred lines below, for a day.
  * `applicable_groups` is a column that no longer exists. `migrate_items.py`
    took no required arguments, opened the canonical database immediately, and
    was saved from writing it ONLY because it crashed on that column name.
  * A skill instructed sessions to open `/tmp/guidebook.db`. That path does not
    exist, so the failure reads as a broken environment rather than a wrong
    instruction.

Each is a rule that lives only as prose, and prose does not check itself. This
promotes the rule to level 2 on the enforcement spectrum (CLAUDE.md §2: text
rule -> audit script), and registration in governance/check-registry.yaml takes
it to level 3.

WHAT IT DOES NOT DO
-------------------
It does not sweep history. `_archived/`, `sessions/`, `decisions/`,
`scripts/migrations/` and the dated audit reports are exempt by default,
because rewriting them would contradict the forward-only, immutable-record
convention that DR-2026-07-21 §4 invoked when it refused to rewrite `E-##` in
past records, and that CLAUDE.md §4 states for migrations.

It also does not decide what is retired. That lives in
governance/retired-vocabulary.yaml, which carries the admission test, the
authority for each entry, and — importantly — the `deferred:` and `rejected:`
sections recording what was considered and NOT added. Read those before
extending the register; three of the obvious candidates are traps.

EXIT CODE
---------
1 if any occurrence survives the exemptions, 0 otherwise. Registered `advisory`,
so today that reports without failing the build; the level is a one-word change
in the registry once the false-positive rate is known (house norm).
"""
import argparse
import re
import sys
import tempfile
from pathlib import Path

try:
    import yaml
except ImportError:                                          # pragma: no cover
    sys.exit("retired_vocabulary_audit.py: needs PyYAML (pip install -r requirements.txt)")

REPO = Path(__file__).resolve().parent.parent.parent
REGISTER = REPO / "governance" / "retired-vocabulary.yaml"

# Same-line escape. Deliberately ugly to type: reaching for it often is a signal
# that the register entry is wrong, not that the file is special.
ESCAPE = "[RETIRED-VOCAB-OK]"

# File-level skip, honouring a convention the repo already keeps: twelve documents
# open with `<!-- SUPERSEDED 2026-05-11 -->` and a banner reading "Preserved here
# as historical record. Do not use for forward work." That is precisely the
# semantic this scanner needs, already maintained by hand for other reasons, so
# reading it beats keeping a parallel path list that would drift out of step with
# it. Header-scoped on purpose — a file that merely discusses supersession
# somewhere in its body is still live.
SUPERSEDED_MARK = "<!-- SUPERSEDED"
SUPERSEDED_WINDOW = 400          # bytes; the marker is always the first line

# Extensions that are never text. The null-byte sniff below catches the rest;
# this list just avoids reading a 4 MB database to discover it is binary.
BINARY_EXT = {
    ".db", ".sqlite", ".sqlite3", ".pyc", ".png", ".jpg", ".jpeg", ".gif",
    ".pdf", ".zip", ".gz", ".tar", ".woff", ".woff2", ".ttf", ".ico", ".xlsx",
}

MATCH_MODES = ("identifier", "literal", "phrase")


# --- pattern construction ---------------------------------------------------
# The substring trap is the whole game here. A naive literal search for
# `audit.yml` also matches `regenerate-evidentiary-audit.yml`; a naive search
# for `VERIFIED-1` also matches `UNVERIFIED-1`. Both would report the retirement
# of a token that is not present. Every mode therefore carries an explicit
# boundary, and the selftest pins each one.

def build_pattern(token, mode):
    """Compile the matcher for one register entry."""
    if mode == "identifier":
        # Word-boundary on both sides, hyphen-aware so `VERIFIED-1` does not
        # match inside `UNVERIFIED-1` and `applicable_groups` does not match
        # inside `applicable_groups_v2`.
        return re.compile(rf"(?<![\w-]){re.escape(token)}(?![\w-])")
    if mode == "literal":
        # Filenames and paths. `/` must be allowed to PRECEDE the token
        # (`workflows/audit.yml` is a true hit) while `-` and word characters
        # must not (`evidentiary-audit.yml` is not).
        return re.compile(rf"(?<![\w-]){re.escape(token)}(?![\w])")
    if mode == "phrase":
        # Prose. Case-insensitive, tolerant of runs of whitespace, still
        # boundaried so a longer word does not trip it.
        parts = [re.escape(w) for w in token.split()]
        body = r"\s+".join(parts)
        return re.compile(rf"(?<![\w-]){body}(?![\w-])", re.IGNORECASE)
    raise ValueError(f"unknown match mode {mode!r} (expected one of {MATCH_MODES})")


def glob_to_re(pattern):
    """Translate a register path glob to a regex over posix-relative paths.

    fnmatch is not usable here: its `*` matches `/`, so `scripts/*` would match
    `scripts/a/b/c.py` and every exemption would be far wider than it reads.
    """
    out, i = [], 0
    while i < len(pattern):
        c = pattern[i]
        if pattern.startswith("**/", i):
            out.append(r"(?:.*/)?")          # zero or more leading directories
            i += 3
        elif pattern.startswith("**", i):
            out.append(r".*")
            i += 2
        elif c == "*":
            out.append(r"[^/]*")
            i += 1
        elif c == "?":
            out.append(r"[^/]")
            i += 1
        else:
            out.append(re.escape(c))
            i += 1
    return re.compile("^" + "".join(out) + "$")


def path_exempt(rel, globs):
    return any(g.match(rel) for g in globs)


# --- register ---------------------------------------------------------------

def load_register(path=REGISTER):
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors = []
    seen = set()
    entries = data.get("entries") or []
    for e in entries:
        eid = e.get("id", "<no id>")
        if eid in seen:
            errors.append(f"{eid}: duplicate id")
        seen.add(eid)
        for field in ("id", "token", "match", "severity", "retired_by", "replacement"):
            if not e.get(field):
                errors.append(f"{eid}: missing required field {field!r}")
        if e.get("match") not in MATCH_MODES:
            errors.append(f"{eid}: match {e.get('match')!r} not in {MATCH_MODES}")
    if errors:
        raise ValueError("register is incoherent:\n  " + "\n  ".join(errors))
    return data


# --- scan -------------------------------------------------------------------

def iter_text_files(root, global_globs):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        rel = path.relative_to(root).as_posix()
        if path.suffix.lower() in BINARY_EXT or path_exempt(rel, global_globs):
            continue
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        if b"\0" in raw[:4096]:                 # binary without a telling suffix
            continue
        if SUPERSEDED_MARK in raw[:SUPERSEDED_WINDOW].decode("utf-8", "replace"):
            continue
        try:
            yield rel, raw.decode("utf-8")
        except UnicodeDecodeError:
            continue


def scan(root=REPO, register=None):
    """Return {entry_id: [(rel, lineno, line), ...]} plus the entry index."""
    data = register if register is not None else load_register()
    global_globs = [glob_to_re(g) for g in (data.get("exempt_paths") or [])]
    entries = data.get("entries") or []

    compiled = []
    for e in entries:
        compiled.append((
            e,
            build_pattern(e["token"], e["match"]),
            [glob_to_re(g) for g in (e.get("exempt_paths") or [])],
        ))

    findings = {e["id"]: [] for e in entries}
    for rel, text in iter_text_files(root, global_globs):
        for e, pat, own_globs in compiled:
            if path_exempt(rel, own_globs):
                continue
            for n, line in enumerate(text.splitlines(), 1):
                if ESCAPE in line:
                    continue
                if pat.search(line):
                    findings[e["id"]].append((rel, n, line.strip()[:120]))
    return findings, {e["id"]: e for e in entries}


# --- reporting --------------------------------------------------------------

SEVERITY_ORDER = {"broken": 0, "doctrine": 1, "stale-pointer": 2}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true",
                    help="run the mutation tests for the matcher and exemptions")
    ap.add_argument("--max-per-entry", type=int, default=12,
                    help="occurrences printed per entry before eliding (default 12)")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    try:
        findings, index = scan()
    except ValueError as exc:
        print(f"FAIL: {exc}")
        return 1

    print("=" * 74)
    print("retired_vocabulary_audit.py — tokens that are readable and wrong")
    print("=" * 74)

    total = 0
    ordered = sorted(index.values(),
                     key=lambda e: (SEVERITY_ORDER.get(e["severity"], 9), e["id"]))
    for e in ordered:
        hits = findings[e["id"]]
        total += len(hits)
        mark = "FAIL" if hits else "ok"
        print(f"\n  {mark:<5} {e['id']}  [{e['severity']}]  {e['token']!r} "
              f"({len(hits)} occurrence(s))")
        if not hits:
            continue
        print(f"        replace with: {str(e['replacement']).strip()}")
        print(f"        retired by:   {str(e['retired_by']).strip()}")
        for rel, n, line in hits[:args.max_per_entry]:
            print(f"          {rel}:{n}: {line}")
        if len(hits) > args.max_per_entry:
            print(f"          ... and {len(hits) - args.max_per_entry} more")

    print()
    if total:
        print(f"RESULTS: {total} occurrence(s) of retired vocabulary on the live surface.")
        print("Each is a wrong answer waiting for whoever greps next. Fix the text, or —")
        print("if the occurrence is a licensed mention rather than a use — add the path to")
        print(f"that entry's exempt_paths, or append {ESCAPE} to the line.")
        print(f"EXAMINED: {len(ordered)}")
        return 1
    print(f"RESULTS: {len(ordered)}/{len(ordered)} register entries clean on the live surface.")
    print(f"EXAMINED: {len(ordered)}")
    return 0


# --- selftest ---------------------------------------------------------------
# Mutation-tested in the style of graph_audit / register_integrity_check: build a
# synthetic tree whose expected verdict is known for each case, and assert the
# scanner returns exactly that. A checker with no selftest is a checker whose
# next refactor silently stops checking — which is the failure this whole file
# exists to prevent, so it would be a poor place to skip it.

CASES = [
    # (path, content, entry_id it must hit or None)
    ("live/a.md", "the items.applicable_groups column\n", "T-ident"),
    ("live/b.md", "applicable_groups_v2 is fine\n", None),
    ("live/c.md", "xapplicable_groups is fine\n", None),
    ("live/d.md", "see .github/workflows/audit.yml today\n", "T-lit"),
    ("live/e.md", "see regenerate-evidentiary-audit.yml today\n", None),
    ("live/f.md", "myaudit.yml is a different file\n", None),
    ("live/g.md", "provision for physically disabled users\n", "T-phrase"),
    ("live/h.md", "PHYSICALLY   DISABLED people\n", "T-phrase"),
    ("live/i.md", "nonphysically disabled-ish\n", None),
    ("_archived/j.md", "applicable_groups everywhere\n", None),      # global exempt
    ("licensed/k.md", "applicable_groups named on purpose\n", None),  # entry exempt
    ("live/l.md", f"applicable_groups {ESCAPE}\n", None),             # inline escape
    ("live/m.md", f"{ESCAPE}\napplicable_groups\n", "T-ident"),       # escape is line-scoped
    # The substring trap, pinned in both directions. Note the fixture must not
    # itself contain the shorter token — the first draft of this case did, and
    # the selftest caught its own prose.
    ("live/n.md", "UNVERIFIED-1 alone must not trip the shorter token\n", None),
    ("live/o.md", "the bare token VERIFIED-1 does\n", "T-suffix"),
    # The repo's own historical-record convention, honoured at file level.
    ("live/p.md", "<!-- SUPERSEDED 2026-05-11 -->\napplicable_groups\n", None),
    # ...but only in the header. A live file that discusses supersession later on
    # must stay in scope, or one sentence anywhere disarms the whole file.
    ("live/q.md", ("filler\n" * 90) + "<!-- SUPERSEDED -->\napplicable_groups\n", "T-ident"),
]

SELFTEST_REGISTER = {
    "exempt_paths": ["_archived/**"],
    "entries": [
        {"id": "T-ident", "token": "applicable_groups", "match": "identifier",
         "severity": "broken", "retired_by": "test", "replacement": "test",
         "exempt_paths": ["licensed/**"]},
        {"id": "T-lit", "token": "audit.yml", "match": "literal",
         "severity": "stale-pointer", "retired_by": "test", "replacement": "test"},
        {"id": "T-phrase", "token": "physically disabled", "match": "phrase",
         "severity": "doctrine", "retired_by": "test", "replacement": "test"},
        {"id": "T-suffix", "token": "VERIFIED-1", "match": "identifier",
         "severity": "broken", "retired_by": "test", "replacement": "test"},
    ],
}


def selftest():
    failures = []

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for rel, content, _ in CASES:
            p = root / rel
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(content, encoding="utf-8")
        # A binary file with no telling suffix must be skipped, not decoded.
        (root / "live" / "blob.dat").write_bytes(b"applicable_groups\x00\xff\xfe")

        findings, _ = scan(root=root, register=SELFTEST_REGISTER)
        hit_paths = {eid: {rel for rel, _, _ in hits} for eid, hits in findings.items()}

        for rel, _, expected in CASES:
            got = {eid for eid, paths in hit_paths.items() if rel in paths}
            if expected is None and got:
                failures.append(f"{rel}: expected no hit, got {sorted(got)}")
            elif expected is not None and expected not in got:
                failures.append(f"{rel}: expected {expected}, got {sorted(got) or 'none'}")

        if any("blob.dat" in paths for paths in hit_paths.values()):
            failures.append("blob.dat: binary file was scanned")

    # The register itself must be coherent, and must not silently degrade into
    # an empty scan — a register that parses but selects nothing passes every
    # content test above while checking the repo for nothing at all.
    try:
        data = load_register()
        if not (data.get("entries") or []):
            failures.append("live register: parses but declares zero entries")
        for section in ("deferred", "rejected"):
            if section not in data:
                failures.append(f"live register: {section!r} section removed — "
                                "the reasoning it holds is the point")
    except Exception as exc:                                  # noqa: BLE001
        failures.append(f"live register: {exc}")

    # An unknown match mode must raise rather than silently match nothing.
    try:
        build_pattern("x", "regex")
        failures.append("build_pattern accepted an unknown match mode")
    except ValueError:
        pass

    # 15 content cases + binary skip + register parses + entries non-empty +
    # deferred present + rejected present + unknown-mode raises.
    n = len(CASES) + 6
    if failures:
        print("retired_vocabulary_audit selftest FAILURES:")
        for f in failures:
            print(f"  - {f}")
        print(f"\nRESULTS: {n - len(failures)}/{n}")
        return 1
    print(f"RESULTS: {n}/{n} selftest cases pass "
          "(boundaries, exemptions, escape scoping, binary skip, register coherence)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
