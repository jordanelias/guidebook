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
    register [--session S] [--db D]
                           every refusal of every committed `scratchpad/*/refusals.jsonl` (plus S's file, committed or
                           not), one line each, with its disposition and the gap's live category and status (T-089)
    classes [--session S]  the refusals grouped by signature, verb, stage and cited rule id, ranked by count, and for
                           each stage they touch the CUE: the registered checks to re-run and the skill section to
                           re-read. With S, only S's refusals, and the exit and the NOT RUN are `list`'s (T-089)

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
import subprocess
import sqlite3
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dbcore  # noqa: E402  -- stdlib only

DISPOSITIONS = ("retried", "parked", "waived")
CODE_ROOT = Path(__file__).resolve().parents[2]     # the checkout this script runs from: the state graph, the registry, the skill
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


def _db_with_gaps(refusal, db=None):
    """`db` when the caller gave one (`register --db`), else the database the refusal names (`db`: a repository-relative
    path), else the one this process opens (GUIDEBOOK_DB_PATH, else the canonical file): an `<outside-repo>/...` name
    cannot be opened from here."""
    named = refusal.get("db")
    for p in ([Path(db)] if db else [dbcore.REPO_ROOT / named] if named else []) + [dbcore.db_path()]:
        if p.is_file():
            return p
    raise Refused(f"neither the database the refusal names ({named!r}) nor {dbcore.db_path()} exists")


def _defect(how, gap_id, reason, refusal, db=None):
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
    db = _db_with_gaps(refusal, db)
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


def _audit(stem, db=None):
    """([(refusal, disposition as written or None, disposition that holds or None, state)], problems) of one session's
    file: the ONE reading `list`, `register` and `classes` share, so a disposition that no longer holds (a parked gap
    closed since) makes the refusal UNDISPOSED in all three, and an unreadable, foreign, duplicated or orphan line is a
    problem in all three."""
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
    out = []
    for _, r in refusals:
        d, state, held = by_key.get(_key(r)), "UNDISPOSED", None
        if d is not None:
            try:
                why = _defect(d["as"], d.get("gap_id"), d.get("reason"), r, db)
            except Refused as exc:
                why = str(exc)
            state = (f"{d['as']}" + (f" {d['gap_id']}" if d.get("gap_id") else "")
                     + (f" ({_one_line(d['reason'], 80)})" if d.get("reason") else "")) if why is None else \
                f"UNDISPOSED (the {d['as']} disposition no longer holds: {_one_line(why, 160)})"
            held = d if why is None else None
        out.append((r, d, held, state))
    return out, problems


def cmd_list(args):
    try:
        stem = _session(args.session)
    except NotRun as exc:
        print(f"NOT RUN: {exc}")
        print("NOT EXAMINED: nothing was looked at, which is not a clean result")
        return 2
    entries, problems = _audit(stem)
    undisposed = 0
    if not entries:
        print(f"no refusal captured for {stem}")
    for r, _, _, state in entries:
        undisposed += state.startswith("UNDISPOSED")
        print(f"{_key(r)}  {r.get('verb')}  {_one_line(r.get('sentence'), 160)}  -> {state}")
    for p in problems:
        print(f"PROBLEM {p}")
    print(f"UNDISPOSED: {undisposed}")
    print(f"EXAMINED: {len(entries)} refusal(s)")
    return 1 if undisposed or problems else 0


# ---- the register and the classes (T-089): read at run time from the files, the state graph, the registry and the skill

SIG_QUOTED = re.compile(r"""(?<!\w)'[^']*'(?!\w)|"[^"]*"|`[^`]*`""")
SIG_ID = re.compile(r"\bREF-\d+|\bGAP-[\w-]+|\bTERM-\d+|\bsession_\S+")
SIG_NUM = re.compile(r"\d+(?:\.\d+)?")
CITED = re.compile(r"\b(?:R\d+[a-z]?|OR-\d+[a-z]?|OD-\d+|OT-\d+|D-\d{4}|T-\d{3}|E\d+)\b")
SKILL = "skills/run-pipeline_SKILL.md"
ENGINE_VERB = "assess_cell"       # the engine writes `specifications`, by a path the state graph's verb derivation does not read


def signature(sentence):
    """The sentence with quoted values, identifiers and numbers replaced by placeholders and whitespace collapsed: ONE
    function, so every class is computed the same way."""
    s = SIG_QUOTED.sub("<Q>", str(sentence))
    s = SIG_NUM.sub("<N>", SIG_ID.sub("<ID>", s))
    return re.sub(r"\s+", " ", s).strip()


def _tree():
    """The state graph's `Tree` of this checkout: the one derivation of verb to tables and of table to stage."""
    sys.path.insert(0, str(CODE_ROOT / "workplan" / "pipeline-state-graph"))
    try:
        import build_graph
        return build_graph.Tree(CODE_ROOT)
    except Exception as exc:   # noqa: BLE001 -- the builder moved or could not read the checkout: say so, never guess a stage
        raise Refused(f"cannot derive stages: workplan/pipeline-state-graph/build_graph.py `Tree` failed ({type(exc).__name__}: {exc}); "
                      f"this script imports it, so a move of the builder is a caller to sweep")
    finally:
        sys.path.pop(0)


def _sessions(args, whole):
    """The session stems to read: `--session S` alone for `classes`; every committed `refusals.jsonl` (plus S's file, which
    may be uncommitted) for `register`. NotRun when git cannot say what is committed or S is not a folder."""
    given = _session(args.session) if args.session else None
    if given and not whole:
        return [given]
    got = subprocess.run(["git", "-C", str(dbcore.REPO_ROOT), "ls-files", "-z", "--", "scratchpad/*/refusals.jsonl"],
                         capture_output=True, text=True, encoding="utf-8")
    if got.returncode != 0:
        raise NotRun(f"`git ls-files` failed in {dbcore.REPO_ROOT}, so the committed refusal files are unknown: {_one_line(got.stderr, 160)}")
    stems = [m.group(1) for p in got.stdout.split("\0") if (m := re.fullmatch(r"scratchpad/([^/]+)/refusals\.jsonl", p))]
    return sorted(set(stems) | ({given} if given else set()))


def _gap(refusal, gap_id, db, cache):
    """(category, status) of the gap in the database that answers for this refusal, or None: the same choice `_defect` makes."""
    try:
        path = _db_with_gaps(refusal, db)
    except Refused:
        return None
    if path not in cache:
        try:
            con = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
            try:
                cache[path] = {g: (c, st) for g, c, st in con.execute("SELECT gap_id, category, status FROM gaps")}
            finally:
                con.close()
        except sqlite3.Error:
            cache[path] = {}
    return cache[path].get(gap_id)


def _instances(args, whole):
    """Every refusal in scope as a dict, and the problems and sessions read. Disposition, gap category and status are read here."""
    out, problems, stems, cache = [], [], _sessions(args, whole), {}
    db = getattr(args, "db", None)
    for stem in stems:
        entries, probs = _audit(stem, db)
        problems += [f"{stem} {p}" for p in probs]
        for r, d, held, state in entries:
            gap = _gap(r, d.get("gap_id"), db, cache) if d and d.get("gap_id") else None
            out.append({"session": stem, "ts": r.get("ts") or "", "id": _key(r), "verb": r.get("verb"), "script": r.get("script"),
                        "argv": r.get("argv") or [], "sentence": r.get("sentence") or "", "state": state, "disp": d,
                        "held": held, "gap": gap, "undisposed": state.startswith("UNDISPOSED")})
    return out, problems, stems


def cmd_register(args):
    try:
        items, problems, stems = _instances(args, whole=True)
    except NotRun as exc:
        print(f"NOT RUN: {exc}")
        print("NOT EXAMINED: nothing was looked at, which is not a clean result")
        return 2
    for i in sorted(items, key=lambda i: (i["ts"], i["session"], i["id"])):
        tail = ""
        if i["disp"] and i["disp"].get("gap_id"):
            g = i["gap"]
            tail = f"  [gap {i['disp']['gap_id']}: " + (f"category {g[0]}, status {g[1]}]" if g else "not in the gaps table]")
        print(f"{i['session']}  {i['ts']}  {i['verb']}  {_one_line(' '.join(map(str, i['argv'])), 10**6)}  "
              f":: {_one_line(i['sentence'], 10**6)}  -> {i['state']}{tail}")
    for p in problems:
        print(f"PROBLEM {p}")
    print(f"EXAMINED: {len(items)} refusal(s) in {len(stems)} session(s)")
    return 1 if problems else 0


def _writes(tree, i):
    """The tables a refusal's verb writes, from the state graph (a `db.py` verb it knows) or the engine's one; else none."""
    if i["script"] == "scripts/db.py" and i["verb"] in tree.verbs:
        return list(tree.verbs[i["verb"]]["writes"])
    return ["specifications"] if i["verb"] == ENGINE_VERB else []


def _names_a_table(check, tables, texts):
    """Does the script a registered check runs name one of `tables`? (The script's text is read, never a list.)"""
    for part in check.get("cmd") or []:
        path = CODE_ROOT / str(part)
        if str(part).endswith(".py") and path.is_file():
            text = texts.setdefault(path, path.read_text(encoding="utf-8", errors="replace"))
            return any(re.search(rf"\b{re.escape(t)}\b", text) for t in tables)
    return False


def _cue(tree, stage, tables, texts):
    """`CUE <stage>: re-run <check ids>; re-read "<heading>"`: the checks whose basis begins `<stage>/` or whose script
    names a table the refused verbs write in that stage, and the skill's `## N. <stage> -` heading."""
    ids = sorted({c["id"] for c in tree.registry["checks"]
                  if str(c.get("basis", "")).startswith(stage + "/") or _names_a_table(c, tables, texts)})
    heads = [m.group(1) for m in re.finditer(rf"^## (\d+\. {re.escape(stage)} \u2014 .*)$",
                                             (CODE_ROOT / SKILL).read_text(encoding="utf-8"), re.M)]
    return (f"CUE {stage}: re-run {', '.join(ids) if ids else '(no registered check)'}; "
            + (f're-read "{heads[0]}"' if heads else f"{SKILL} has no section for it"))


def _triage(items):
    """What the instances were disposed as and filed under: retried; parked with the gap's category; waived with its reason."""
    n = Counter()
    for i in items:
        d = i["held"]
        if d is None:
            continue
        if d["as"] == "parked":
            n[f"parked({i['gap'][0] if i['gap'] else 'gap not found'})"] += 1
        elif d["as"] == "waived":
            n[f"waived ({_one_line(d.get('reason'), 60)})"] += 1
        else:
            n[d["as"]] += 1
    return ", ".join(f"{k} {v}" for k, v in sorted(n.items())) or "none disposed"


def _print_group(title, groups):
    print(f"CLASSES by {title}")
    for key, items in sorted(groups.items(), key=lambda kv: (-len(kv[1]), str(kv[0]))):
        ts = sorted(i["ts"] for i in items)
        print(f"  {len(items)}x  {_one_line(key, 240)}")
        print(f"      sessions {len({i['session'] for i in items})}, first {ts[0]}, last {ts[-1]}, "
              f"undisposed {sum(i['undisposed'] for i in items)}/{len(items)}; triage: {_triage(items)}")


def cmd_classes(args):
    try:
        items, problems, stems = _instances(args, whole=False)
    except NotRun as exc:
        print(f"NOT RUN: {exc}")
        print("NOT EXAMINED: nothing was looked at, which is not a clean result")
        return 2
    tree = _tree() if items else None
    by_sig, by_verb, by_stage, by_cited = defaultdict(list), defaultdict(list), defaultdict(list), defaultdict(list)
    stage_tables = defaultdict(set)
    for i in items:
        tables = _writes(tree, i)
        stages = sorted({tree.stage(t) for t in tables}) or ["?"]
        for t in tables:
            stage_tables[tree.stage(t)].add(t)
        by_sig[signature(i["sentence"])].append(i)
        by_verb[i["verb"]].append(i)
        for st in stages:
            by_stage[st].append(i)
        for c in sorted(set(CITED.findall(i["sentence"]))) or ["(none)"]:
            by_cited[c].append(i)
    for title, groups in (("signature", by_sig), ("verb", by_verb), ("stage", by_stage), ("cited id", by_cited)):
        _print_group(title, groups)
    texts = {}
    for st in sorted(by_stage, key=lambda s: (tree.stages.index(s) if s in tree.stages else len(tree.stages), s)):
        if st in tree.stages:
            print(_cue(tree, st, stage_tables[st], texts))
    for p in problems:
        print(f"PROBLEM {p}")
    undisposed = sum(i["undisposed"] for i in items)
    print(f"UNDISPOSED: {undisposed}")
    print(f"EXAMINED: {len(items)} refusal(s) in {len(stems)} session(s)")
    return 1 if problems or (args.session and undisposed) else 0


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
    p = sub.add_parser("register", help="every refusal of every committed session, one line each, with its disposition and gap")
    p.add_argument("--session", help="also read this session's file when it is not committed")
    p.add_argument("--db", help="the database whose gaps table answers (default: the one `list` uses)")
    p.set_defaults(fn=cmd_register)
    p = sub.add_parser("classes", help="the refusals grouped by signature, verb, stage and cited id, with the CUE per stage")
    p.add_argument("--session", help="only this session's refusals; exit 1 if any is undisposed, 2 if not run")
    p.set_defaults(fn=cmd_classes)
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
