#!/usr/bin/env python3
"""scripts/audit/search_log_completeness.py — every search the session RAN is a search it LOGGED.

WHY THIS EXISTS (I5, process-gap plan WP14). `search_executions` is the one event home of a
discovery step (pipeline contract evidence/discovery-provenance). Every coverage claim built on
it -- `v_coverage_jurisdiction`, R14's absence reasoning -- assumes a search that ran is a search
that was logged. Nothing checked that assumption: the only witness to a search the agent ran and
never logged was the transcript, and only a reviewer diffing it by hand could find the gap. A
coverage claim resting on an unscreened search reaches the book through those views.

THE WITNESS IS THE HARNESS, NOT THE AGENT. `.claude/hooks/record-command.py` is wired as a
PostToolUse hook on `WebSearch|WebFetch` (beside its `Bash` wiring) and appends one line per call
to scratchpad/<session>/commands.jsonl, routed by the same `open_session()` as the Bash log. The
agent being audited writes neither the hook nor its lines. This script compares that ledger
(the artefact) against `search_executions` (the record).

RULES
  FAIL      A WebSearch ledger line whose query, casefolded and whitespace-collapsed, equals or
            is contained in no `search_executions.query_text` (same fold) written by this
            session. A WebSearch line with NO query also FAILs: the hook could not read the
            field, so the line cannot be shown to be logged, and passing it would be a check
            that examined nothing and said green (CLAUDE.md 5(a)). Containment is the
            generous direction, deliberately: a logged query_text may carry a `site:`
            prefix or context the tool call did not. The cost is stated, not hidden -- a
            very short ledger query is matched by any logged query that contains it.
  REPORTED  A WebFetch URL found in neither this session's `query_text` nor its retrieval-log
            manifest. WebFetch hands back a model-written summary, not bytes, so R10
            persistence cannot apply to it; it is surfaced for a reviewer, never failed.
  REPORTED  A host reached by a bare `curl`/`wget` in a Bash ledger line that no URL in this
            session's manifest names -- a probe or retrieval outside `retrieval_log.fetch`.
            URLs are read only from the lines of a command that invoke curl or wget, after
            joining backslash continuations; a URL elsewhere in the same command is not one
            the tool fetched.

EXAMINED is the number of WebSearch + WebFetch ledger lines -- the subject the FAIL rule and the
first REPORTED rule are about. Bash lines are scanned for the third rule and counted in their own
words, never under the EXAMINED token: a session with no web-tool lines is NOTHING-IN-SCOPE
whatever its Bash history, because nothing in it could FAIL. Every session before this hook was
wired is in that state.

THE SESSION. `--session` takes the stem, bare or with `.md`. The ledger is
scratchpad/<stem>/commands.jsonl, which is where the hook files lines while scratchpad/CURRENT
holds the stem AND the folder is named identically to it (CLAUDE.md section 7). A ledger the hook
misfiled elsewhere is not found here; `--ledger PATH` reads one explicitly.

THE MANIFEST is read through `retrieval_log._manifest_records`, the one reader of it, so this
script inherits its `GUIDEBOOK_RETRIEVAL_LOG` override and its cwd-relative default: run it from
the repository root, as run_checks.py and /batch-done do. The path read and its line count are
printed, so an empty manifest is visible rather than inferred.

Exit: 0 PASS or NOTHING-IN-SCOPE; 1 FAIL; 2 cannot run (no database when one is needed).
"""
import argparse
import json
import re
import sqlite3
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import dbcore                                                        # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research"))
import retrieval_log                                                 # noqa: E402

REPO_ROOT = dbcore.REPO_ROOT

_FETCHER = re.compile(r"\b(curl|wget)\b")
_URL = re.compile(r"https?://[^\s\"'<>()\[\]{}|\\]+")


def fold(s):
    """Casefolded and whitespace-collapsed: the comparison form of a query."""
    return " ".join(str(s or "").casefold().split())


def fold_url(u):
    """A URL in comparison form: casefolded, fragment dropped, no trailing slash."""
    u = fold(u).split("#", 1)[0]
    return u.rstrip("/")


def fetched_urls(command):
    """URLs on the lines of `command` that invoke curl or wget."""
    out = []
    for line in str(command or "").replace("\\\n", " ").splitlines():
        if _FETCHER.search(line):
            out.extend(m.rstrip(".,;:") for m in _URL.findall(line))
    return out


def host(u):
    try:
        return (urllib.parse.urlsplit(u).hostname or "").casefold()
    except ValueError:
        return ""


def read_ledger(path):
    """(lines, unparseable). A missing file is an empty ledger."""
    lines, bad = [], 0
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None, 0
    for raw in text.splitlines():
        if not raw.strip():
            continue
        try:
            rec = json.loads(raw)
        except ValueError:
            bad += 1
            continue
        if isinstance(rec, dict):
            lines.append(rec)
        else:
            bad += 1
    return lines, bad


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("--session", required=True, help="session stem, bare or with .md")
    ap.add_argument("--ledger", help="commands.jsonl to read (default: scratchpad/<stem>/)")
    args = ap.parse_args(argv)

    stem = args.session[:-3] if args.session.endswith(".md") else args.session
    ledger = Path(args.ledger) if args.ledger else REPO_ROOT / "scratchpad" / stem / "commands.jsonl"
    lines, bad = read_ledger(ledger)
    try:
        ledger = ledger.resolve().relative_to(REPO_ROOT)
    except ValueError:
        pass  # a --ledger outside the repository prints as given

    print(f"Session: {stem}")
    if lines is None:
        print(f"Ledger: {ledger} -- absent. Either this session made no tool call the hook "
              f"records, or its lines were filed under another folder (CLAUDE.md section 7: "
              f"the folder must be named identically to scratchpad/CURRENT's content).")
        lines = []
    searches = [r for r in lines if r.get("tool") == "WebSearch"]
    fetches = [r for r in lines if r.get("tool") == "WebFetch"]
    # A line with no `tool` predates the WebSearch|WebFetch branch and is a Bash line.
    bash = [r for r in lines if r.get("tool", "Bash") == "Bash"]
    if lines or bad:
        print(f"Ledger: {ledger} -- {len(lines)} line(s): WebSearch {len(searches)}, "
              f"WebFetch {len(fetches)}, Bash {len(bash)}, other "
              f"{len(lines) - len(searches) - len(fetches) - len(bash)}"
              + (f"; {bad} unparseable line(s) skipped" if bad else ""))

    try:
        manifest = retrieval_log._manifest_records(stem)
        mnote = ""
    except (OSError, ValueError, KeyError) as exc:
        manifest, mnote = [], f" (unreadable: {exc.__class__.__name__}; treated as empty)"
    man_path = retrieval_log.LOG_ROOT / stem / "manifest.jsonl"
    man_urls = [fold_url(m.get("url")) for m in manifest if m.get("url")]
    man_hosts = {host(m.get("url") or "") for m in manifest} - {""}
    print(f"Manifest: {man_path} -- {len(manifest)} line(s){mnote}")

    examined = len(searches) + len(fetches)
    reports = []

    # Third rule first: it needs no database, and it runs whatever EXAMINED is.
    stray = {}
    for r in bash:
        for u in fetched_urls(r.get("command")):
            h = host(u)
            if h and h not in man_hosts:
                stray.setdefault(h, []).append(r.get("ts"))
    print(f"Bash lines scanned for bare curl/wget: {len(bash)}")
    for h, ts in sorted(stray.items()):
        reports.append(f"  curl/wget host absent from the manifest: {h} "
                       f"({len(ts)} line(s), first {ts[0]})")

    if examined == 0:
        print("EXAMINED: 0")
        if reports:
            print("REPORTED (not failing):")
            print("\n".join(reports))
        print("VERDICT: NOTHING-IN-SCOPE — no WebSearch or WebFetch line in this session's "
              "ledger, so no search can be shown unlogged.")
        return 0

    db = dbcore.db_path()
    if not db.exists():
        print(f"[ERROR] no database at {db}; {examined} ledger line(s) cannot be compared.")
        print("EXAMINED: 0")
        return 2
    conn = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
    logged = [fold(q) for (q,) in conn.execute(
        "SELECT query_text FROM search_executions WHERE created_by_session IN (?, ?)",
        (stem, stem + ".md"))]
    conn.close()
    print(f"search_executions rows for this session: {len(logged)}")
    print(f"EXAMINED: {examined}")

    unlogged, queryless = {}, []
    for r in searches:
        q = fold(r.get("query"))
        if not q:
            queryless.append(r.get("ts"))
        elif not any(q in t for t in logged):
            unlogged.setdefault(q, []).append(r.get("ts"))

    for r in fetches:
        u = fold_url(r.get("url"))
        if not u:
            reports.append(f"  WebFetch line with no url ({r.get('ts')}); input_keys "
                           f"{r.get('input_keys')}")
        elif not (any(u in t for t in logged) or any(u in m for m in man_urls)):
            reports.append(f"  WebFetch url in neither query_text nor the manifest: "
                           f"{r.get('url')} ({r.get('ts')})")

    if reports:
        print("REPORTED (not failing):")
        print("\n".join(reports))

    if unlogged or queryless:
        n = sum(len(v) for v in unlogged.values()) + len(queryless)
        print(f"FAIL: {n} WebSearch ledger line(s) match no search_executions.query_text "
              f"written by this session:")
        for q, ts in sorted(unlogged.items()):
            print(f"  unlogged: {q!r} ({len(ts)} call(s), first {ts[0]})")
        for ts in queryless:
            print(f"  no query on the ledger line ({ts}) -- the hook could not read "
                  f"tool_input.query; its input_keys say what the payload carried")
        print("  Log each with `db.py log-search` (R8: every query verbatim, empties kept). "
              "The ledger is not rewritten to clear this; the record is.")
        return 1

    print(f"VERDICT: PASS — {len(searches)} WebSearch call(s), each matched to a logged "
          f"query; {len(fetches)} WebFetch call(s) reported above where unmatched.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
