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
import os
import re
import sqlite3
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


def dead_exemptions(root=REPO, register=None):
    """Exemptions naming a concrete path that does not exist.

    WHY THIS IS PART OF THIS CHECK AND NOT A NEW ONE. An exempt_paths entry is the
    only thing that can licence a retired token to sit on a live surface, so a dead
    one is this register's own integrity, not a separate subject. §8: "Nothing is
    added without naming what reads it" -- an exemption naming a deleted file is that
    defect pointed the other way, and this register carried five for
    scripts/generate/population_page.py within hours of the branch that deleted it.

    THE PROCESS, NOT THE FACT. Sweeping the five by hand fixes today and nothing
    else: rule 4 says a removal is not done until the callers are swept, AN
    EXEMPTION IS A CALLER, and no gate covered that class. This is the gate. The
    next deletion that leaves an exemption behind is named here rather than found by
    someone reading 77 glob patterns.

    GLOBS ARE NOT CHECKED, deliberately. `decisions/**` and `workplan/*20??-??-??*`
    are properties of a shape, not claims that a file exists, and an empty directory
    is a legitimate state. Only entries with no glob metacharacter are asserted to
    exist -- those are unambiguous claims about a path.
    """
    data = register if register is not None else load_register()
    seen, dead = {}, []
    def note(where, paths):
        for raw in paths or []:
            g = str(raw)
            if any(c in g for c in "*?["):
                continue
            seen.setdefault(g, []).append(where)
    note("exempt_paths (global)", data.get("exempt_paths"))
    for e in data.get("entries") or []:
        note(f"{e['id']} ({e['token']})", e.get("exempt_paths"))
    for g, wheres in sorted(seen.items()):
        if not (Path(root) / g).exists():
            dead.append((g, wheres))
    return dead


# --- replacement staleness ---------------------------------------------------
# HONOURS GUIDEBOOK_DB_PATH. The blocking db_path_env_audit requires it and its reason
# applies here: a script that ignores the variable reads the committed database while a
# test believes it is reading a scratch copy.
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))

#: Tokens that look like an identifier but are not one. `PRAGMA user_version` is a SQLite
#: pragma, not a column, and is the only one of its kind in the register today.
_PRAGMA_PRECEDED = re.compile(r"PRAGMA\s+$", re.I)
#: A file path is not a schema reference.
_FILEY = re.compile(r"\.(yml|yaml|py|md|json|sql|html|sh|txt|db|jsonl)\b")
#: snake_case, optionally table-qualified. Requires an underscore, which is what separates
#: a schema identifier from an English word or a CI job name (`classify`, `research`).
_SNAKE = re.compile(r"\b([a-z][a-z0-9_]*\.)?([a-z][a-z0-9]*(?:_[a-z0-9]+)+)\b")
#: An ALL-CAPS hyphenated code value: DM-AMB, MD-AUTISM, GAP-001, CLOSED-DECIDED.
_CODEISH = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b")


def _live_vocabulary(db=None):
    """What the database can be asked to confirm: object names, column names, code values.

    The code universe is every distinct value held in a `*_code` or `*_id` column. That is
    derived from the schema, never listed here (rule 8) -- a hand-maintained list of code
    columns would go blind exactly the way `WRITABLE_TABLES` did eight times.
    """
    path = Path(db or DB_PATH)
    if not path.exists():
        return None
    con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        objects = {n for (n,) in con.execute(
            "SELECT name FROM sqlite_master WHERE type IN ('table','view')")}
        cols, every_col, codes = {}, set(), set()
        for t in objects:
            try:
                cols[t] = {c[1] for c in con.execute('PRAGMA table_info("%s")' % t)}
            except sqlite3.Error:
                cols[t] = set()
            every_col |= cols[t]
        for t, cs in cols.items():
            for c in cs:
                if not (c.endswith("_code") or c.endswith("_id")):
                    continue
                try:
                    for (v,) in con.execute('SELECT DISTINCT "%s" FROM "%s"' % (c, t)):
                        if isinstance(v, str):
                            codes.add(v)
                except sqlite3.Error:
                    continue
        return {"objects": objects, "cols": cols, "every_col": every_col, "codes": codes}
    finally:
        con.close()


def stale_replacements(register=None, db=None):
    """Every entry's `replacement` must name things that still exist.

    THE HOLE THIS CLOSES, and it was found the hard way. On 2026-09-15 seventeen entries
    were added for the retired `AX-*` codes, each naming its `DM-*` successor as the
    replacement. On 2026-09-16 migration 084 deleted every one of those successors. The
    register then told anyone who met `AX-AMB` to use `DM-AMB`, which no longer existed --
    a retired-vocabulary entry that had itself become readable and wrong, which is the
    precise defect this whole file exists to catch. **Nothing noticed, because the scan
    counts occurrences of the TOKEN and never reads the REPLACEMENT it prints beside
    them.** A register that is checked only on its left-hand column is half a register.

    WHAT IS RESOLVABLE IS CHECKED; WHAT IS NOT IS LEFT ALONE. A replacement is prose, and
    most of it cannot be verified by machine. Two classes can: snake_case identifiers,
    against the live schema's objects and columns, and ALL-CAPS hyphenated code values,
    against every value held in a `*_code` or `*_id` column. Calibrated against the live
    register before it was wired: 46 of 51 references resolved, and of the five that did
    not, four were extractor faults now fixed here (a SQL alias, a PRAGMA name, a
    deliberately-named historical identifier) and ONE was a real stale pointer.

    A TABLE-QUALIFIED REFERENCE FALLS BACK TO THE COLUMN. `es.author_display` is a SQL
    alias for `evidence_sources`, not a table; refusing it would flag correct prose. If
    the qualifier is not a live object, the column half is checked on its own.

    THE ESCAPE IS THE SAME ONE THE SCAN USES. A replacement that must name a dead
    identifier -- RV-001 records the junction's interim name between two migrations --
    carries `[RETIRED-VOCAB-OK]` and is skipped whole, so the licence is visible in the
    register rather than hidden in this file.
    """
    data = register if register is not None else load_register()
    vocab = _live_vocabulary(db)
    if vocab is None:
        return None, 0                      # no database: report, never pretend
    stale, examined = [], 0
    for e in data.get("entries") or []:
        text = str(e.get("replacement") or "")
        if ESCAPE in text:
            continue
        clean = _FILEY.sub("", text)
        for m in _SNAKE.finditer(clean):
            if _PRAGMA_PRECEDED.search(clean[:m.start()]):
                continue
            qual, ident = m.group(1), m.group(2)
            if qual:
                table = qual.rstrip(".")
                ok = (ident in vocab["cols"].get(table, set())
                      if table in vocab["objects"] else ident in vocab["every_col"])
            else:
                ok = ident in vocab["objects"] or ident in vocab["every_col"]
            examined += 1
            if not ok:
                stale.append((e["id"], e["token"], m.group(0), "no such table or column"))
        for m in set(_CODEISH.findall(clean)):
            examined += 1
            if m not in vocab["codes"] and m != e["token"]:
                stale.append((e["id"], e["token"], m, "no such code value"))
    return sorted(set(stale)), examined


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

    stale, stale_examined = stale_replacements()
    if stale:
        print()
        print("-" * 70)
        print(f"STALE REPLACEMENTS: {len(stale)} reference(s) in a `replacement` field name")
        print("  something that no longer exists. The entry tells the next reader to use a")
        print("  table, column or code that is gone — a retired-vocabulary entry that has")
        print("  itself become readable and wrong, which is what this register exists to")
        print("  catch. Fix the replacement, or mark a deliberate historical mention with")
        print(f"  {ESCAPE}.")
        for eid, token, ref, why in stale:
            print(f"    {eid} ({token}): {ref}  — {why}")
    elif stale is None:
        print()
        print("  NOTE: replacement staleness NOT CHECKED — no database at "
              f"{DB_PATH}. Reported rather than passed over: a sub-check that silently")
        print("  examines nothing is the vacuity failure this repository names first.")

    dead = dead_exemptions()
    if dead:
        print()
        print("-" * 70)
        print(f"DEAD EXEMPTIONS: {len(dead)} exempt_paths entr(ies) name a path that does "
              f"not exist.")
        print("  An exemption for a deleted file exempts nothing and misleads the next")
        print("  reader of this register. Rule 4: an exemption IS a caller. Remove it, or")
        print("  restore the path.")
        for g, wheres in dead:
            print(f"    {g}")
            for w in wheres:
                print(f"        cited by: {w}")

    print()
    if total or dead or stale:
        if total:
            print(f"RESULTS: {total} occurrence(s) of retired vocabulary on the live surface.")
            print("Each is a wrong answer waiting for whoever greps next. Fix the text, or —")
            print("if the occurrence is a licensed mention rather than a use — add the path to")
            print(f"that entry's exempt_paths, or append {ESCAPE} to the line.")
        print(f"EXAMINED: {len(ordered)} register entr(ies) + "
              f"{len(dead)} dead exemption(s) + {stale_examined} replacement reference(s)")
        return 1
    print(f"RESULTS: {len(ordered)}/{len(ordered)} register entries clean on the live surface, "
          f"every concrete exemption resolves, and every resolvable reference in a "
          f"replacement still exists.")
    print(f"EXAMINED: {len(ordered)} entr(ies) + {stale_examined} replacement reference(s)")
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

        # DEAD-EXEMPTION DETECTION, mutation-tested both ways. Added 2026-09-11 with
        # the finding class itself: a new branch with no selftest is what this file's
        # own header calls a checker whose next refactor silently stops checking.
        reg = {
            "exempt_paths": ["live/a.md", "live/gone.md", "live/**"],
            "entries": [{"id": "X", "token": "t", "match": "identifier",
                         "exempt_paths": ["live/also-gone.py"]}],
        }
        dead = {g for g, _ in dead_exemptions(root=root, register=reg)}
        if "live/gone.md" not in dead:
            failures.append("dead_exemptions: missed a global exemption naming a "
                            "nonexistent path")
        if "live/also-gone.py" not in dead:
            failures.append("dead_exemptions: missed a per-entry exemption naming a "
                            "nonexistent path")
        if "live/a.md" in dead:
            failures.append("dead_exemptions: flagged an exemption whose path EXISTS")
        if "live/**" in dead:
            failures.append("dead_exemptions: flagged a GLOB, which asserts a shape "
                            "rather than a path")

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

    # REPLACEMENT STALENESS, pinned here because the hole it closes was invisible for a
    # day and the three true-positive shapes are exactly the ones that occurred: a code
    # value deleted out from under an entry (the `DM-AMB` case), a deleted table, and a
    # deleted table.column. The seven controls are the extractor faults found while
    # calibrating against the live register — each one was a false positive before it was
    # fixed, so each is a regression that would otherwise return unnoticed.
    REPL_CASES = [
        ("deleted code value",        "DM-AMB — Ambulant movement",                 True),
        ("deleted table",             "use base_icf_groupings instead",             True),
        ("deleted table.column",      "read base_icf_groupings.grouping_code",      True),
        ("live table",                "use population_icf_links instead",           False),
        ("live table.column",         "read specifications.icf_code",               False),
        ("live code value",           "use BLIND for that",                         False),
        ("SQL alias, column resolves", "es.author_display, or es.first_author_last", False),
        ("PRAGMA is not a column",    "PRAGMA user_version",                        False),
        ("CI job name is not schema", "ci.yml — the `classify` job",                False),
        ("escape suppresses",         "base_icf_groupings " + ESCAPE + " deliberate", False),
    ]
    if _live_vocabulary() is None:
        failures.append("replacement staleness: no database — the sub-check cannot be "
                        "exercised, and a selftest that skips a case silently is the "
                        "vacuity this file reports on")
    else:
        for label, text, should_flag in REPL_CASES:
            reg = {"entries": [{"id": "RV-TEST", "token": "SOME-TOKEN",
                                "match": "identifier", "severity": "broken",
                                "retired_by": "selftest", "replacement": text}]}
            flagged, _ = stale_replacements(register=reg)
            if bool(flagged) != should_flag:
                failures.append(
                    f"replacement staleness [{label}]: flagged={bool(flagged)}, "
                    f"expected {should_flag}")

    # 15 content cases + binary skip + register parses + entries non-empty +
    # deferred present + rejected present + unknown-mode raises + 10 replacement cases.
    n = len(CASES) + 6 + len(REPL_CASES)
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
