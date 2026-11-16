#!/usr/bin/env python3
"""scripts/audit/refusal_register.py — every writer refusal a batch met, and what became of each (T-088).

WHY THIS EXISTS. A writer's refusal is the only record of what the batch tried to hold and could not write
(a figure, an inadequacy statement), and it was printed once and lost: the session's command log keeps the
command and a hash of the output. `dbcore.record_refusal` now keeps each one in
`scratchpad/<session>/refusals.jsonl` (the file is committed with the session, CLAUDE.md rule 6). This script
reads that one file and records what became of each refusal, so a batch cannot be called done with a refusal
nobody answered (`/batch-done`).

    list [--session S]     each refusal with its disposition or UNDISPOSED; exit 1 if any is undisposed or any line
                           is unreadable, foreign, duplicated or disposed by a disposition that no longer holds;
                           exit 2 (NOT RUN) when S is not a `session_YYYY-MM-DD-...` stem whose folder exists under
                           `scratchpad/`: nothing could have been captured, so nothing was examined
    dispose --session S --id K --as retried|parked|waived [--gap-id G] [--reason R]

A refusal line is `{refusal_id, ts, session, script, verb, argv, sentence, db}`; a disposition line is
`{kind: "disposition", refusal_id, as, gap_id, reason, ts}` appended to the same file. A line without `kind` is a
refusal. `K` is the refusal's `refusal_id` (a line written before that field existed is named by its `ts`). This
script never writes the database, and it never writes a canonical row by hand (OD-54).

The dispositions are declared once, below, and read from there by both subcommands: a rule declared once in
a stated place (owner, 2026-11-12). `list` re-checks every disposition when it lists, with the same function
`dispose` uses, so a gap closed after it was parked, or a line written by hand, makes the refusal UNDISPOSED again.
  retried  the writer was right and the corrected call succeeded (not checkable here: say so in --reason if useful)
  parked   the content waits: a gap (`db.py add-gap`, typed by its subject) names what is held back and the
           refused argv in this file is the replay command; --gap-id must be an OPEN gap of the database the
           refusal names (a repository-relative `db`), else of the database this process opens
  waived   nothing is held back, and --reason says why
"""
import argparse
import json
import re
import sqlite3
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dbcore  # noqa: E402  -- stdlib only

DISPOSITIONS = ("retried", "parked", "waived")
MIN_REASON = 10     # a waiver's reason: at least this many characters, with a letter or digit (`--reason "."` waives nothing)


class Refused(Exception):
    """This script's own refusal: printed as `REFUSING: ...`, exit 1."""


class NotRun(Refused):
    """The session is not one a refusal could have been kept for: `list` says NOT RUN, exit 2, and examined nothing."""


def _session(given):
    """The bare stem of `given`, else of `scratchpad/CURRENT`; NotRun unless it is a `session_YYYY-MM-DD-...` stem
    (never a path, never `..`) whose folder exists: the capture never creates the folder, so a misspelt CURRENT, a
    branch slug or a folder that was never made would otherwise list as a clean `EXAMINED: 0`."""
    stem = dbcore.session_stem(given) if given else None
    if not stem:
        cur = dbcore.REPO_ROOT / "scratchpad" / "CURRENT"
        stem = dbcore.session_stem(cur.read_text(encoding="utf-8-sig").strip()) if cur.is_file() else None
    if not stem:
        raise NotRun("no session: give --session, or set scratchpad/CURRENT")
    if not dbcore.SESSION_STEM.fullmatch(stem):
        raise NotRun(f"{stem!r} is not a session stem (session_YYYY-MM-DD-...): fix scratchpad/CURRENT as /session-open sets it")
    if not (dbcore.REPO_ROOT / "scratchpad" / stem).is_dir():
        raise NotRun(f"scratchpad/{stem} is not a folder, so no refusal could have been kept for it: "
                     f"fix scratchpad/CURRENT or create the folder as /session-open does")
    return stem


def _key(rec):
    """What names a refusal: its `refusal_id`; a line written before that field existed is named by its `ts`."""
    return rec.get("refusal_id") or rec.get("ts")


def _read(stem):
    """(refusals, dispositions, unreadable) of the session's file: three lists of (line number, record). A file that
    does not exist is three empty lists, not an error. A line that is not a JSON object, or has an unknown `kind`,
    is unreadable and is reported, never skipped. A byte-order mark and CRLF line ends are read."""
    path = dbcore.REPO_ROOT / "scratchpad" / stem / "refusals.jsonl"
    refusals, dispositions, bad = [], [], []
    if not path.is_file():
        return refusals, dispositions, bad
    for n, raw in enumerate(path.read_bytes().decode("utf-8-sig", "replace").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            rec = json.loads(raw)
        except ValueError:
            rec = None
        if not isinstance(rec, dict):
            bad.append((n, "not a JSON object"))
        elif "kind" not in rec:
            refusals.append((n, rec))
        elif rec["kind"] == "disposition":
            if rec.get("as") in DISPOSITIONS:
                dispositions.append((n, rec))
            else:
                bad.append((n, f"unknown disposition {rec.get('as')!r}"))
        else:
            bad.append((n, f"unknown kind {rec['kind']!r}"))
    return refusals, dispositions, bad


def _one_line(text, width):
    return re.sub(r"\s+", " ", str(text)).strip()[:width]


def _db_with_gaps(refusal):
    """The database the refusal names (`db`: a repository-relative path), else the one this process opens
    (GUIDEBOOK_DB_PATH, else the canonical file): an `<outside-repo>/...` name cannot be opened from here."""
    named = refusal.get("db")
    for p in ([dbcore.REPO_ROOT / named] if named else []) + [dbcore.db_path()]:
        if p.is_file():
            return p
    raise Refused(f"neither the database the refusal names ({named!r}) nor {dbcore.db_path()} exists")


def _defect(how, gap_id, reason, refusal):
    """Why this disposition does not hold, or None. ONE function: `dispose` refuses on it and `list` re-checks every
    disposition with it, so what was true when it was written is checked again when it is read."""
    if how != "parked":
        if gap_id:
            return f"--gap-id belongs to parked, not {how}"
        reason = (reason or "").strip()
        if how == "waived" and (len(reason) < MIN_REASON or not any(c.isalnum() for c in reason)):
            return (f"waived needs --reason of at least {MIN_REASON} characters with a letter or digit: "
                    f"a refusal set aside without a reason is a refusal lost")
        return None
    if not gap_id:
        return ("parked needs --gap-id: file the gap first (`db.py add-gap`, typed by its subject), "
                "the refused argv in this file is the replay command")
    db = _db_with_gaps(refusal)
    con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    try:
        row = con.execute("SELECT status FROM gaps WHERE gap_id = ?", (gap_id,)).fetchone()
    except sqlite3.Error as exc:
        return f"{db} cannot answer for gap {gap_id!r}: {exc}"
    finally:
        con.close()
    if row is None:
        return f"gap {gap_id!r} is not in the gaps table of {db}: parking needs a gap that holds the content"
    if not str(row[0]).startswith("OPEN"):
        return f"gap {gap_id!r} is {row[0]!r}, not open: a closed gap holds nothing back"
    return None


def cmd_list(args):
    try:
        stem = _session(args.session)
    except NotRun as exc:
        print(f"NOT RUN: {exc}")
        print("NOT EXAMINED: nothing was looked at, which is not a clean result")
        return 2
    refusals, dispositions, bad = _read(stem)
    problems = [f"line {n}: unreadable ({why})" for n, why in bad]
    keys = Counter(_key(r) for _, r in refusals)
    problems += [f"{k!r} is carried by {c} refusal lines, so no disposition can name one: edit the file by hand"
                 for k, c in keys.items() if c > 1]
    problems += [f"line {n}: foreign line (session {r.get('session')!r}, not {stem})" for n, r in refusals if r.get("session") != stem]
    by_key = {}
    for n, d in dispositions:
        k = d.get("refusal_id") or d.get("refusal_ts")
        if k not in keys:
            problems.append(f"line {n}: a disposition for {k!r}, which no refusal of this file carries")
        elif k in by_key:
            problems.append(f"line {n}: {k!r} is disposed a second time")
        elif keys[k] == 1:
            by_key[k] = d
    undisposed = 0
    if not refusals:
        print(f"no refusal captured for {stem}")
    for _, r in refusals:
        d, state = by_key.get(_key(r)), "UNDISPOSED"
        if d is not None:
            try:
                why = _defect(d["as"], d.get("gap_id"), d.get("reason"), r)
            except Refused as exc:
                why = str(exc)
            state = (f"{d['as']}" + (f" {d['gap_id']}" if d.get("gap_id") else "")
                     + (f" ({_one_line(d['reason'], 80)})" if d.get("reason") else "")) if why is None else \
                f"UNDISPOSED (the {d['as']} disposition no longer holds: {_one_line(why, 160)})"
        undisposed += state.startswith("UNDISPOSED")
        print(f"{_key(r)}  {r.get('verb')}  {_one_line(r.get('sentence'), 160)}  -> {state}")
    for p in problems:
        print(f"PROBLEM {p}")
    print(f"UNDISPOSED: {undisposed}")
    print(f"EXAMINED: {len(refusals)} refusal(s)")
    return 1 if undisposed or problems else 0


def cmd_dispose(args):
    stem = _session(args.session)
    refusals, dispositions, bad = _read(stem)
    held = [r for _, r in refusals if _key(r) == args.id]
    if not held:
        raise Refused(f"no refusal of {stem} carries id {args.id!r}: `list` prints each refusal's id")
    if len(held) > 1:
        raise Refused(f"id {args.id!r} is carried by {len(held)} refusal lines, so it cannot name one: edit the file by hand")
    if any((d.get("refusal_id") or d.get("refusal_ts")) == args.id for _, d in dispositions):
        raise Refused(f"the refusal {args.id!r} is already disposed; a disposition is not rewritten here")
    why = _defect(args.disposition, args.gap_id, args.reason, held[0])
    if why:
        raise Refused(why)
    line = {"kind": "disposition", "refusal_id": args.id, "as": args.disposition, "gap_id": args.gap_id or None,
            "reason": (args.reason or "").strip() or None, "ts": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")}
    dbcore.append_line(dbcore.REPO_ROOT / "scratchpad" / stem / "refusals.jsonl", json.dumps(line, ensure_ascii=False))
    print(f"disposed {args.id} as {args.disposition}" + (f" {args.gap_id}" if args.gap_id else ""))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list", help="each refusal of a session and its disposition; exit 1 if any is undisposed, 2 if not run")
    p.add_argument("--session", help="default: scratchpad/CURRENT")
    p.set_defaults(fn=cmd_list)
    p = sub.add_parser("dispose", help="record what became of one refusal")
    p.add_argument("--session", required=True)
    p.add_argument("--id", required=True, help="the refusal's id, as `list` prints it")
    p.add_argument("--as", dest="disposition", required=True, choices=DISPOSITIONS)
    p.add_argument("--gap-id", help="parked: the open gap that holds the content")
    p.add_argument("--reason", help=f"waived: why, at least {MIN_REASON} characters; any other: optional")
    p.set_defaults(fn=cmd_dispose)
    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except Refused as exc:
        print(f"REFUSING: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
