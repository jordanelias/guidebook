#!/usr/bin/env python3
"""
scripts/audit/session_pointer_audit.py — keep the continuity surface honest.

Three files tell a fresh session where to start: `sessions/LATEST`,
`sessions/LATEST-RESEARCH`, and `sessions/handoff-next-session.md`. All three are
hand-maintained, none of them was checked, and each has been wrong for weeks at a
time. This audits all three.

`sessions/LATEST` and `sessions/LATEST-RESEARCH` are one-line files naming a
session record. Session-scoped checks in `governance/check-registry.yaml` resolve
their `@SESSION@` substitution through them, so the pointers decide what those
checks look at — and a check that looks at the wrong thing, or at nothing, is
worse than no check, because it reports a pass either way.

Two failure modes, and they need different treatment.

P1 — DANGLING (blocking). A pointer that is missing, empty, or names a file that
does not exist. `run_checks.py` treats an unreadable pointer as "no session" and
SKIPs every check that requires one. The BLOCKING `citation_mining_session` gate
therefore switches itself off silently: deleting one 60-byte file disarms a gate
and nothing in the output says so. That is the hazard this script exists for.

P2 — DRIFT (reported, not failed). `LATEST-RESEARCH` naming a session older than
the most recent session that actually logged evidence_sources rows. This is the
condition W4 found on 2026-08-06 and fixed by hand: LATEST named a June
continuity session while research had run through 26 July, so the mining gate
scoped itself to a session that had touched no sources. A hand-fix that nothing
watches is a hand-fix that rots, so drift is detected here. It is REPORTED rather
than failed because advancing the pointer is a judgment call — the newest session
with rows is not always the newest session whose research is finished — and
because a stale pointer breaks no invariant on its own.

The split itself is the point. Before W4 one name answered both "where did work
leave off" and "whose research should be audited"; those diverge, and every hour
they stay diverged the gate reads the wrong session. This script measures the
divergence that made the split necessary.

Exit codes: 0 = pointers resolve (drift may be reported), 1 = P1 failure,
2 = DB unreadable.

Usage:
    python3 scripts/audit/session_pointer_audit.py
    python3 scripts/audit/session_pointer_audit.py --selftest
"""
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SESSIONS = REPO / "sessions"
DB_PATH = Path(os.environ.get("GUIDEBOOK_DB_PATH", REPO / "data" / "guidebook.db"))

# Mirrors run_checks.SESSION_POINTERS. Kept as a literal rather than imported:
# this audit must be able to report that run_checks' own table is wrong, which it
# cannot do if it borrows that table as its definition of correct.
POINTERS = {
    "LATEST": "continuity — where work left off; the default for session-scoped checks",
    "LATEST-RESEARCH": "subject of the blocking citation_mining_session gate",
}

DATE_RE = re.compile(r"session_(\d{4}-\d{2}-\d{2})")

HANDOFF = SESSIONS / "handoff-next-session.md"

# The handoff's header is a set of `**Label:** value` lines. These three name
# things on disk or in history; a dangling one sends the next session nowhere.
HANDOFF_FIELDS = {
    "HEAD at handoff": re.compile(r"\*\*HEAD at handoff:\*\*\s*`([0-9a-f]{7,40})`"),
    "Last session record": re.compile(r"\*\*Last session record:\*\*\s*`([^`]+)`"),
    "The plan to work from": re.compile(r"\*\*The plan to work from:\*\*\s*`([^`]+)`"),
}


def git(*args):
    """(ok, stdout). Never raises — git absence is a condition to report, not crash on."""
    try:
        p = subprocess.run(["git", *args], cwd=REPO, capture_output=True, text=True)
    except FileNotFoundError:                                  # pragma: no cover
        return False, ""
    return p.returncode == 0, p.stdout.strip()


def audit_handoff():
    """(problems, drift, lines) for sessions/handoff-next-session.md.

    A dangling PATH is a problem: the handoff is where a fresh session is told
    what to read, so a named file that does not exist costs the next session its
    first twenty minutes. A stale HEAD or session name is DRIFT: it is wrong but
    it is prose, and failing CI over unrewritten prose would make the check
    something to route around. The distinction is the same one drawn for the
    pointers above — enforce what silently breaks machinery, report what merely
    misleads a reader, and never let the second masquerade as the first.

    This file went eleven weeks naming a HEAD from May and a branch that had been
    merged. Nothing was wrong with the repo; the map was wrong, and the map is
    what a session reads first.
    """
    problems, drift, lines = [], [], []
    if not HANDOFF.exists():
        drift.append("sessions/handoff-next-session.md is missing — a fresh session "
                     "has no entry point but §9's 'sort workplan/ by date'.")
        return problems, drift, lines

    text = HANDOFF.read_text(encoding="utf-8")
    for label, pattern in HANDOFF_FIELDS.items():
        m = pattern.search(text)
        if not m:
            drift.append(f"handoff has no `{label}:` line — the header format changed "
                         f"or the field was dropped; nothing can check it.")
            continue
        value = m.group(1).strip()

        if label == "HEAD at handoff":
            ok, _ = git("cat-file", "-e", f"{value}^{{commit}}")
            if not ok:
                drift.append(f"handoff names HEAD {value}, which is not a commit in this "
                             f"clone — the handoff describes history this branch does not "
                             f"have.")
                continue
            anc, _ = git("merge-base", "--is-ancestor", value, "HEAD")
            if not anc:
                drift.append(f"handoff names HEAD {value}, which is NOT an ancestor of the "
                             f"current HEAD — it was written on a different line of history.")
                continue
            ok, behind = git("rev-list", "--count", f"{value}..HEAD")
            lines.append(f"  ok      handoff HEAD {value} is an ancestor"
                         + (f", {behind} commit(s) back" if ok else ""))
        else:
            target = REPO / value
            if not target.exists():
                problems.append(f"handoff's `{label}` names {value!r}, which does not exist")
                lines.append(f"  FAIL    handoff {label} -> {value} (no such file)")
            else:
                lines.append(f"  ok      handoff {label} -> {value}")

    return problems, drift, lines


def session_date(name):
    """The date a session name carries, or None. Names are `session_YYYY-MM-DD-…`."""
    m = DATE_RE.match(name or "")
    return m.group(1) if m else None


def read_pointer(name):
    """(value, error). `value` is the first non-blank line, or None."""
    path = SESSIONS / name
    if not path.exists():
        return None, f"sessions/{name} does not exist"
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8").splitlines()]
    lines = [ln for ln in lines if ln]
    if not lines:
        return None, f"sessions/{name} is empty"
    return lines[0], None


def newest_session(conn, gate_scope=False):
    """The latest-dated session that logged evidence_sources rows.

    `gate_scope=True` narrows to the predicate the citation_mining_session gate
    actually scopes by: slug-linked sources at Tier 1-2. The two answers differ,
    and the difference is the point — see drift_report().

    Ordered by the date in the name, not by rowid or insertion order: sessions are
    imported and backfilled out of order, so "last written" is not "most recent".
    """
    sql = ("SELECT DISTINCT es.created_by_session FROM evidence_sources es "
           "JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id "
           "WHERE es.tier BETWEEN 1 AND 2" if gate_scope else
           "SELECT DISTINCT created_by_session FROM evidence_sources es "
           "WHERE 1=1")
    names = [r[0] for r in conn.execute(
        sql + " AND es.created_by_session IS NOT NULL AND es.created_by_session != ''"
    )]
    dated = [(session_date(n), n) for n in names if session_date(n)]
    return max(dated)[1] if dated else None


def audit():
    problems, drift, lines = [], [], []

    known = {p.name for p in SESSIONS.rglob("*.md")}

    resolved = {}
    for name, purpose in POINTERS.items():
        value, err = read_pointer(name)
        if err:
            problems.append(err)
            lines.append(f"  FAIL    sessions/{name} — {err}")
            continue
        resolved[name] = value
        if value not in known:
            problems.append(
                f"sessions/{name} names {value!r}, which is not a file under sessions/")
            lines.append(f"  FAIL    sessions/{name} -> {value} (no such record)")
        else:
            lines.append(f"  ok      sessions/{name} -> {value}")
        lines.append(f"          ({purpose})")

    # P2 — drift, DB-dependent and non-fatal.
    db_note = None
    if not DB_PATH.exists():
        db_note = f"DB not found at {DB_PATH}; drift not checked"
    else:
        try:
            conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
        except sqlite3.Error as exc:                            # pragma: no cover
            return 2, [f"cannot open {DB_PATH}: {exc}"], [], []
        newest = newest_session(conn)
        newest_in_gate_scope = newest_session(conn, gate_scope=True)
        conn.close()
        pointed = resolved.get("LATEST-RESEARCH")
        if newest and pointed:
            pd, nd = session_date(pointed), session_date(newest)
            if pd and nd and pd < nd:
                drift.append(
                    f"sessions/LATEST-RESEARCH names {pointed!r} ({pd}), but "
                    f"{newest!r} ({nd}) logged evidence_sources rows later. The "
                    f"mining gate is auditing a session that research has moved "
                    f"past. Advance the pointer, or record why this one is still "
                    f"the subject.")
        elif not newest:
            db_note = "no session in evidence_sources carries a parseable date"

        # The pointer's contract and the gate's predicate are not the same
        # predicate, and when they diverge the blocking gate has no subject.
        #
        # LATEST-RESEARCH means "newest session with evidence_sources rows".
        # citation_mining_session scopes to SLUG-LINKED sources at TIER 1-2,
        # because that is what RULE 124 makes mining mandatory for. A session that
        # admitted only Tier 3 satisfies the first and offers the second nothing,
        # so the gate reports NOTHING-IN-SCOPE and passes — correctly, and without
        # having checked anything.
        #
        # That is the state on 2026-08-06 and it is not obviously wrong: the
        # newest research session genuinely has nothing to mine. What is wrong is
        # that it was INVISIBLE. Reported rather than failed, because advancing
        # the pointer to the newest session with subjects would point a BLOCKING
        # gate at a real 8-source backlog and redden main for content work that is
        # deliberately deferred — a permanently-red gate is one people learn to
        # ignore, which is how this whole class of defect survives.
        if newest_in_gate_scope and pointed:
            pd, gd = session_date(pointed), session_date(newest_in_gate_scope)
            if pd and gd and pd != gd:
                drift.append(
                    f"sessions/LATEST-RESEARCH names {pointed!r}, which holds no "
                    f"slug-linked Tier 1-2 sources — so citation_mining_session, "
                    f"which is BLOCKING, examines nothing and passes. The newest "
                    f"session inside that gate's scope is "
                    f"{newest_in_gate_scope!r} ({gd}). Repointing there is a "
                    f"judgment call with a consequence: run the gate against it "
                    f"first and see what it reports.")

    hp, hd, hl = audit_handoff()
    problems += hp
    drift += hd
    lines += hl

    return (1 if problems else 0), problems, drift, lines + ([f"  note    {db_note}"]
                                                             if db_note else [])


def selftest():
    """Assertions over the pure helpers. The pointer/DB reads are not mocked —
    what would need mocking is the filesystem, and a selftest that rebuilds
    sessions/ to test a reader of sessions/ tests the rebuild."""
    cases = [
        ("session_2026-07-26-energy-conservation-b3.md", "2026-07-26"),
        ("session_2026-05-11g-citation-mining", "2026-05-11"),
        ("LATEST", None),
        ("", None),
        (None, None),
        ("notes_2026-07-26-thing.md", None),          # not a session_ name
        ("session_2026-7-26-short.md", None),         # not zero-padded
    ]
    failed = 0
    for name, expected in cases:
        got = session_date(name)
        if got != expected:
            print(f"  FAIL session_date({name!r}) = {got!r}, expected {expected!r}")
            failed += 1

    # Ordering is by date, and must not be by string length or lexical rank of
    # the whole name — `session_2026-07-26-a` vs `session_2026-07-26-zzzz`.
    if max([("2026-05-11", "a"), ("2026-07-26", "b")])[1] != "b":
        print("  FAIL date ordering")
        failed += 1

    print(f"RESULTS: {len(cases) + 1 - failed}/{len(cases) + 1} selftest assertions pass")
    return 1 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()

    code, problems, drift, lines = audit()
    print("=" * 70)
    print("session_pointer_audit.py — the continuity surface points at real things")
    print("=" * 70)
    for ln in lines:
        print(ln)

    if drift:
        print()
        for d in drift:
            print(f"  DRIFT   {d}")

    if problems:
        print()
        print(f"{len(problems)} unresolvable reference(s) on the continuity surface.")
        print("  A POINTER that does not resolve does not fail the checks that read "
              "it — run_checks.py SKIPs them, so the blocking citation_mining_session "
              "gate turns itself off in silence.")
        print("  A HANDOFF path that does not resolve sends the next session to a file "
              "that is not there, which is the first thing it reads.")
        print("  Point them at something that exists.")
        return 1

    print()
    print(f"RESULTS: {len(POINTERS)}/{len(POINTERS)} pointers resolve, handoff paths resolve"
          + (f", {len(drift)} drift warning(s)" if drift else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
