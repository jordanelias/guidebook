#!/usr/bin/env python3
"""scripts/audit/search_log_completeness.py — a search the session RAN but never LOGGED fails.

WHY THIS EXISTS, as CLAUDE.md section 8 requires. Without the audit, a WebSearch whose results
fed a coverage claim but which never reached `search_executions` is visible only to a reviewer
diffing the transcript by hand, and the claim reaches `v_coverage_jurisdiction` and R14's
absence reasoning unscreened (I5). Without THIS test, the audit can go vacuous the way the
repo's gates have before: the hook and the audit must agree on field names (`tool`, `query`,
`url`), and nothing else checks that they do.

Fixtures: a COPY of the canonical database in a temp directory, with search rows written by
`db.py log-search` itself (the sanctioned writer, so a writer that changed what it stores would
show here), a temp retrieval-log root via GUIDEBOOK_RETRIEVAL_LOG, and hand-written
commands.jsonl ledgers. E01 instead drives `.claude/hooks/record-command.py` with a WebSearch
payload and audits the line it actually wrote. Nothing depends on a live id: the slug is read
from the copy.

WHAT FAILS ON THE UNBUILT CODE. With no audit script every case is red. With the audit but the
old hook, E01 is red: the old hook writes no line for a WebSearch payload, so the audit reports
NOTHING-IN-SCOPE where E01 requires a FAIL.
"""
import json
import os
import pathlib
import shutil
import sqlite3
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parents[2]
AUDIT = REPO / "scripts" / "audit" / "search_log_completeness.py"
HOOK = REPO / ".claude" / "hooks" / "record-command.py"
S = "session_test-search-log-completeness"
OTHER = "session_test-search-log-completeness-other"

results = []


def record(tid, name, passed, details=""):
    results.append(bool(passed))
    print(f"  [{'✓' if passed else '✗'}] {tid}: {name}")
    if details and not passed:
        print(f"      {details}")


TMP = pathlib.Path(tempfile.mkdtemp(prefix="search-log-completeness-"))
DB = TMP / "guidebook.db"
LOGROOT = TMP / "retrieval-log"
ENV = dict(os.environ, GUIDEBOOK_DB_PATH=str(DB), GUIDEBOOK_RETRIEVAL_LOG=str(LOGROOT))


def ledger(name, lines):
    p = TMP / f"{name}.jsonl"
    p.write_text("".join(json.dumps(x) + "\n" for x in lines), encoding="utf-8")
    return p


def audit(ledger_path, session=S):
    r = subprocess.run([sys.executable, str(AUDIT), "--session", session,
                        "--ledger", str(ledger_path)],
                       cwd=REPO, env=ENV, capture_output=True, text=True, timeout=120)
    return r.returncode, r.stdout + r.stderr


SLUG = None


def log_search(query, session=S):
    r = subprocess.run([sys.executable, str(REPO / "scripts" / "db.py"), "log-search",
                        "--slug", SLUG, "--language", "EN", "--query-text", query,
                        "--engine", "web", "--depth-method", "scoping",
                        "--session", session,
                        "--prior-expectation", "test fixture: no expectation"],
                       cwd=REPO, env=ENV, capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"log-search refused the fixture: {(r.stderr or r.stdout)[:300]}")


def ws(query, ts="2026-10-01T00:00:00Z"):
    return {"ts": ts, "tool": "WebSearch", "query": query, "session_id": "SID"}


def wf(url, ts="2026-10-01T00:00:01Z"):
    return {"ts": ts, "tool": "WebFetch", "url": url, "session_id": "SID"}


def bash(command, tool=True):
    rec = {"ts": "2026-10-01T00:00:02Z", "command": command, "session_id": "SID"}
    if tool:
        rec["tool"] = "Bash"
    return rec


if not AUDIT.exists():
    print(f"  [✗] AUDIT MISSING: {AUDIT}")
    print("EXAMINED: 0 assertion(s)")
    sys.exit(1)

try:
    shutil.copy(REPO / "data" / "guidebook.db", DB)
    con = sqlite3.connect(DB)
    SLUG = con.execute("SELECT slug FROM slugs WHERE status = 'ACTIVE' ORDER BY slug "
                       "LIMIT 1").fetchone()[0]
    con.close()
    sys.path.insert(0, str(REPO / "scripts"))
    import run_checks                                                    # noqa: E402

    # ── N: nothing in scope ──────────────────────────────────────────────────
    rc, out = audit(ledger("bash-only", [bash("ls", tool=False), bash("echo hi")]))
    record("N01", "a ledger with no WebSearch/WebFetch line is NOTHING-IN-SCOPE, exit 0",
           rc == 0 and "EXAMINED: 0" in out and "VERDICT: NOTHING-IN-SCOPE" in out, out)
    record("N02", "and run_checks classifies that output as NOTHING-IN-SCOPE, not PASS",
           run_checks.nothing_in_scope(out), out)
    rc, out = audit(TMP / "does-not-exist.jsonl")
    record("N03", "an absent ledger is NOTHING-IN-SCOPE and says where it looked",
           rc == 0 and "absent" in out and "VERDICT: NOTHING-IN-SCOPE" in out, out)

    # ── F: the FAIL rule ─────────────────────────────────────────────────────
    one = ledger("one-unlogged", [ws("ramp gradient TEK17 Norway")])
    rc, out = audit(one)
    record("F01", "one unlogged WebSearch query FAILs (exit 1) and is named",
           rc == 1 and "FAIL" in out and "ramp gradient tek17 norway" in out
           and "EXAMINED: 1" in out, out)

    log_search("ramp gradient TEK17 Norway", session=OTHER)
    rc, out = audit(one)
    record("F02", "the same query logged by ANOTHER session does not clear it",
           rc == 1 and "unlogged" in out, out)

    rc, out = audit(ledger("queryless", [{"ts": "t", "tool": "WebSearch", "query": None,
                                          "input_keys": ["q"]}]))
    record("F03", "a WebSearch line with no query FAILs rather than passing unexamined",
           rc == 1 and "no query" in out, out)

    # ── P: the passing shape ─────────────────────────────────────────────────
    log_search("Ramp  Gradient TEK17   Norway")                    # equal after the fold
    log_search("site:dibk.no kerb ramp 1:15 max gradient regulation")  # contains the next
    two = ledger("all-logged", [ws("ramp gradient TEK17 Norway"),
                                ws("kerb ramp 1:15 max gradient")])
    rc, out = audit(two)
    record("P01", "every query logged (equal after casefold/whitespace, or contained) PASSes",
           rc == 0 and "VERDICT: PASS" in out and "EXAMINED: 2" in out, out)
    record("P02", "and run_checks counts that as examined, not NOTHING-IN-SCOPE",
           not run_checks.nothing_in_scope(out), out)
    rc, out = audit(two, session=S + ".md")
    record("P03", "the .md pointer form scopes to the same rows",
           rc == 0 and "VERDICT: PASS" in out, out)
    rc, out = audit(ledger("not-contained", [ws("kerb ramp 1:15 max gradient Norway")]))
    record("P04", "containment runs one way: a ledger query LONGER than any logged one FAILs",
           rc == 1, out)

    # ── R: the REPORTED rules never fail ─────────────────────────────────────
    (LOGROOT / S).mkdir(parents=True)
    (LOGROOT / S / "manifest.jsonl").write_text(
        json.dumps({"url": "https://www.dibk.no/regelverk/tek17/12-16",
                    "artefact": "a.html"}) + "\n", encoding="utf-8")
    rc, out = audit(ledger("fetches", [ws("ramp gradient TEK17 Norway"),
                                       wf("https://www.dibk.no/regelverk/tek17/12-16/"),
                                       wf("https://unpersisted.example.org/page")]))
    record("R01", "a WebFetch URL absent from manifest and query_text is REPORTED, exit 0",
           rc == 0 and "unpersisted.example.org/page" in out and "REPORTED" in out, out)
    record("R02", "a WebFetch URL the manifest holds is not reported (trailing slash folded)",
           "tek17/12-16/" not in out, out)

    rc, out = audit(ledger("curls", [
        bash('curl -sS "https://stray.example.net/x.pdf" -o /tmp/x.pdf'),
        bash('wget https://www.dibk.no/other'),
        bash('python3 -c "print(\'https://not-fetched.example.com/\')"\ncurl -sS \\\n'
             '  "https://continued.example.net/y"', tool=False)]))
    record("R03", "a bare curl host absent from the manifest is REPORTED, never failed",
           rc == 0 and "stray.example.net" in out, out)
    record("R04", "a host the manifest names is not reported",
           "www.dibk.no" not in out, out)
    record("R05", "a URL on a non-curl line of the same command is not read as fetched",
           "not-fetched.example.com" not in out, out)
    record("R06", "a backslash-continued curl line is read whole; a tool-less line is Bash",
           "continued.example.net" in out, out)

    # ── E: end to end, through the hook that writes the ledger ───────────────
    # The audit and the hook must agree on `tool` and `query`. Each is tested alone
    # elsewhere; only this case fails if they drift apart.
    proj = TMP / "proj"
    stem = "session_test-search-log-e2e"
    (proj / "scratchpad" / stem).mkdir(parents=True)
    (proj / "sessions").mkdir()
    (proj / "scratchpad" / "CURRENT").write_text(stem + "\n")
    payload = {"session_id": "SID-E2E", "tool_name": "WebSearch",
               "tool_input": {"query": "tactile paving spacing Japan JIS T 9251"},
               "tool_response": {"query": "tactile paving spacing Japan JIS T 9251",
                                 "results": []}}
    subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload), text=True,
                   env=dict(os.environ, CLAUDE_PROJECT_DIR=str(proj)), timeout=60)
    written = proj / "scratchpad" / stem / "commands.jsonl"
    rc, out = audit(written, session=stem)
    record("E01", "a WebSearch the hook recorded and nobody logged FAILs",
           rc == 1 and "tactile paving spacing japan jis t 9251" in out, out)
    log_search("tactile paving spacing Japan JIS T 9251", session=stem)
    rc, out = audit(written, session=stem)
    record("E02", "and PASSes once db.py log-search records it",
           rc == 0 and "VERDICT: PASS" in out, out)
finally:
    shutil.rmtree(TMP, ignore_errors=True)

print("\n" + "=" * 70)
print(f"EXAMINED: {len(results)} assertion(s)")
print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
if sum(results) < len(results):
    print(f"FAILED: {len(results) - sum(results)}")
print("=" * 70)
sys.exit(0 if results and sum(results) == len(results) else 1)
