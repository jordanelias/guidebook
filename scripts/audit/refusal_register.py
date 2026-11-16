#!/usr/bin/env python3
"""scripts/audit/refusal_register.py — every writer refusal a batch met, and what became of each (T-088).

WHY THIS EXISTS. A writer's refusal is the only record of what the batch tried to hold and could not write
(a figure, an inadequacy statement), and it was printed once and lost: the session's command log keeps the
command and a hash of the output. `dbcore.record_refusal` now keeps each one in
`scratchpad/<session>/refusals.jsonl` (the file is committed with the session, CLAUDE.md rule 6). This script
reads that one file and records what became of each refusal, so a batch cannot be called done with a refusal
nobody answered (`/batch-done`).

    list [--session S]     each refusal with its disposition or UNDISPOSED; exit 1 if any is undisposed
    dispose --session S --ts T --as retried|parked|waived [--gap-id G] [--reason R]

A refusal line is `{ts, session, script, verb, argv, sentence, db}`; a disposition line is
`{kind: "disposition", refusal_ts, as, gap_id, reason, ts}` appended to the same file. A line without `kind`
is a refusal. `ts` has microseconds because `dispose` names a refusal by it and a retry loop refuses twice in
one minute. This script never writes the database, and it never writes a canonical row by hand (OD-54).

The dispositions are declared once, below, and read from there by both subcommands: a rule declared once in
a stated place (owner, 2026-11-12). What a disposition means:
  retried  the writer was right and the corrected call succeeded (not checkable here: say so in --reason if useful)
  parked   the content waits: a gap (`db.py add-gap`, typed by its subject) names what is held back and the
           refused argv in this file is the replay command; --gap-id is checked against the database the
           refusal names
  waived   nothing is held back, and --reason says why
"""
import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dbcore  # noqa: E402  -- stdlib only

DISPOSITIONS = ("retried", "parked", "waived")


class Refused(Exception):
    """This script's own refusal: printed as `REFUSING: ...`, exit 1."""


def _session(given):
    """The bare stem of `given`, else of `scratchpad/CURRENT`; refused when neither names a folder."""
    stem = dbcore.session_stem(given) if given else None
    if not stem:
        cur = dbcore.REPO_ROOT / "scratchpad" / "CURRENT"
        stem = dbcore.session_stem(cur.read_text(encoding="utf-8").strip()) if cur.is_file() else None
    if not stem or "/" in stem:
        raise Refused("no session: give --session, or set scratchpad/CURRENT")
    return stem


def _read(stem):
    """(refusals, dispositions, unreadable) of the session's file: three lists of (line number, record). A file that
    does not exist is three empty lists, not an error. A line that is not a JSON object, or has an unknown `kind`,
    is unreadable and is reported, never skipped."""
    path = dbcore.REPO_ROOT / "scratchpad" / stem / "refusals.jsonl"
    refusals, dispositions, bad = [], [], []
    if not path.is_file():
        return refusals, dispositions, bad
    for n, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
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


def cmd_list(args):
    stem = _session(args.session)
    refusals, dispositions, bad = _read(stem)
    by_ts, problems = {}, [f"line {n}: unreadable ({why})" for n, why in bad]
    ts_held = [r.get("ts") for _, r in refusals]
    for n, d in dispositions:
        if d.get("refusal_ts") not in ts_held:
            problems.append(f"line {n}: a disposition for {d.get('refusal_ts')!r}, which no refusal of this file carries")
        elif d["refusal_ts"] in by_ts:
            problems.append(f"line {n}: {d['refusal_ts']!r} is disposed a second time")
        else:
            by_ts[d["refusal_ts"]] = d
    undisposed = 0
    if not refusals:
        print(f"no refusal captured for {stem}")
    for _, r in refusals:
        d = by_ts.get(r.get("ts"))
        if d is None:
            undisposed += 1
            state = "UNDISPOSED"
        else:
            state = f"{d['as']}" + (f" {d['gap_id']}" if d.get("gap_id") else "") + (f" ({_one_line(d['reason'], 80)})" if d.get("reason") else "")
        print(f"{r.get('ts')}  {r.get('verb')}  {_one_line(r.get('sentence'), 160)}  -> {state}")
    for p in problems:
        print(f"PROBLEM {p}")
    print(f"UNDISPOSED: {undisposed}")
    print(f"EXAMINED: {len(refusals)} refusal(s)")
    return 1 if undisposed or problems else 0


def _db_with_gaps(refusal):
    """The database the refusal names (`db`: a repository-relative or absolute path, `~` forms are not
    resolvable), else the one this process opens (GUIDEBOOK_DB_PATH, else the canonical file)."""
    named = refusal.get("db")
    cand = [dbcore.REPO_ROOT / named] if named and not str(named).startswith("~") else []
    for p in cand + [dbcore.db_path()]:
        if p.is_file():
            return p
    raise Refused(f"neither the database the refusal names ({named!r}) nor {dbcore.db_path()} exists")


def cmd_dispose(args):
    stem = _session(args.session)
    refusals, dispositions, bad = _read(stem)
    held = [r for _, r in refusals if r.get("ts") == args.ts]
    if not held:
        raise Refused(f"no refusal of {stem} carries ts {args.ts!r}: `list` prints each refusal's ts")
    if len(held) > 1:
        raise Refused(f"ts {args.ts!r} is carried by {len(held)} refusal lines, so it cannot name one: edit the file by hand")
    if any(d.get("refusal_ts") == args.ts for _, d in dispositions):
        raise Refused(f"the refusal at {args.ts!r} is already disposed; a disposition is not rewritten here")
    reason = (args.reason or "").strip()
    if args.disposition == "parked":
        if not args.gap_id:
            raise Refused("parked needs --gap-id: file the gap first (`db.py add-gap`, typed by its subject), "
                          "the refused argv in this file is the replay command")
        db = _db_with_gaps(held[0])
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            row = con.execute("SELECT status FROM gaps WHERE gap_id = ?", (args.gap_id,)).fetchone()
        except sqlite3.Error as exc:
            raise Refused(f"{db} cannot answer for gap {args.gap_id!r}: {exc}")
        finally:
            con.close()
        if row is None:
            raise Refused(f"gap {args.gap_id!r} is not in the gaps table of {db}: parking needs a gap that holds the content")
        if not str(row[0]).startswith("OPEN"):
            raise Refused(f"gap {args.gap_id!r} is {row[0]!r}, not open: a closed gap holds nothing back")
    elif args.gap_id:
        raise Refused(f"--gap-id belongs to parked, not {args.disposition}")
    if args.disposition == "waived" and not reason:
        raise Refused("waived needs --reason: a refusal set aside without a reason is a refusal lost")
    line = {"kind": "disposition", "refusal_ts": args.ts, "as": args.disposition, "gap_id": args.gap_id or None,
            "reason": reason or None, "ts": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f")}
    with open(dbcore.REPO_ROOT / "scratchpad" / stem / "refusals.jsonl", "a", encoding="utf-8") as fh:
        fh.write(json.dumps(line, ensure_ascii=False) + "\n")
    print(f"disposed {args.ts} as {args.disposition}" + (f" {args.gap_id}" if args.gap_id else ""))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list", help="each refusal of a session and its disposition; exit 1 if any is undisposed")
    p.add_argument("--session", help="default: scratchpad/CURRENT")
    p.set_defaults(fn=cmd_list)
    p = sub.add_parser("dispose", help="record what became of one refusal")
    p.add_argument("--session", required=True)
    p.add_argument("--ts", required=True, help="the refusal's ts, as `list` prints it")
    p.add_argument("--as", dest="disposition", required=True, choices=DISPOSITIONS)
    p.add_argument("--gap-id", help="parked: the open gap that holds the content")
    p.add_argument("--reason", help="waived: why; any other: optional")
    p.set_defaults(fn=cmd_dispose)
    args = ap.parse_args(argv)
    try:
        return args.fn(args)
    except Refused as exc:
        print(f"REFUSING: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
