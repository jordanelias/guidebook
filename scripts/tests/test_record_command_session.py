#!/usr/bin/env python3
"""`.claude/hooks/record-command.py` — which session does a Bash call get filed under?

WHY THIS EXISTS, stated as CLAUDE.md §1 requires. This one function has been wrong
twice in three days, both times invisibly, and both times the wrong answer looked
like a correct file:

  2026-08-23  read `.claude/session`, a pointer moved at close-out -> every command
              of one session filed under the previous session's directory.
  2026-08-23  "fixed" by reading `sessions/LATEST` instead. LATEST is ALSO moved at
              close-out. Three sessions' logs ended up in one file named after the
              earliest (5 + 405 + 274 lines) before anyone noticed, and the two
              later sessions had no log at all.
  2026-08-25  derivation added; found by test, before shipping, to fall back to a
              STALE open session the moment a session writes its own close-out
              record and keeps working -- which is the documented ritual.

The wrong thing that reaches the guidebook without this test is a provenance record
that misattributes which session did which work, against a directive the owner has
now stated twice ("the scratchpad needs to be getting saved always for provenance",
2026-08-20; "so that we actually have a surface to review", 2026-08-25). It is not
apparatus about apparatus: it guards the review surface itself.

The hook cannot be imported -- it reads stdin and exits at module scope -- so this
execs the text above its `try:` block, which is exactly the helper under test.
"""
import sys, json, pathlib, tempfile, shutil

HOOK = pathlib.Path(__file__).resolve().parents[2] / ".claude" / "hooks" / "record-command.py"

results = []
def record(tid, name, passed, details=""):
    results.append(passed)
    print(f"  [{'✓' if passed else '✗'}] {tid}: {name}")
    if details and not passed:
        print(f"      {details}")

def load():
    src = HOOK.read_text()
    ns = {}
    exec(src.split("\ntry:\n", 1)[0], ns)
    return ns["open_session"]

def build(tmp, dirs):
    """Rebuild `tmp` to hold EXACTLY `dirs`. {name: (lines_or_None, closed_bool)}

    WIPES FIRST, deliberately. An additive version leaked fixtures between cases:
    a directory left behind by S01 changed which session A03 resolved to, so two
    assertions passed on the order they happened to run in rather than on the code.
    Caught by adding a case, not by the suite going red -- which is the point.
    """
    shutil.rmtree(tmp, ignore_errors=True)
    (tmp / "sessions").mkdir(parents=True, exist_ok=True)
    (tmp / "scratchpad").mkdir(parents=True, exist_ok=True)
    for name, (lines, closed) in dirs.items():
        d = tmp / "scratchpad" / name
        d.mkdir(exist_ok=True)
        if lines is not None:
            (d / "commands.jsonl").write_text(
                "".join(json.dumps(x) + "\n" for x in lines))
        if closed:
            (tmp / "sessions" / f"{name}.md").write_text("record\n")
    return tmp

OPEN, CLOSED = False, True

if not HOOK.exists():
    print(f"  [✗] HOOK MISSING: {HOOK}")
    sys.exit(1)

open_session = load()
tmp = pathlib.Path(tempfile.mkdtemp(prefix="record-command-test-"))
try:
    # ── S: the guess, used only until a line exists to anchor to ──────────────
    # The CLOSED session is deliberately the NEWEST here. If it were the older one,
    # "pick the newest" and "pick the newest OPEN" would agree and this assertion
    # would pass without testing anything -- which is how it was first written.
    build(tmp, {"session_2026-08-24-mine": (None, OPEN),
                "session_2026-08-25-closed": (None, CLOSED)})
    record("S01", "a closed session is never written into, even when it is newest",
           open_session(tmp, "SID-A") == "session_2026-08-24-mine",
           f"got {open_session(tmp, 'SID-A')!r}")

    build(tmp, {"session_2026-08-25-mine": ([{"session_id": "SID-A"}], OPEN)})
    record("S02", "once a line exists the sid anchors the choice",
           open_session(tmp, "SID-A") == "session_2026-08-25-mine")

    # ── A: the anchor, and the hole it closes ────────────────────────────────
    # THE REGRESSION. Writing sessions/<stem>.md is the close-out ritual, and a
    # session routinely keeps working afterwards. Newest-open alone stops matching
    # the live session at that instant and falls into an older one.
    build(tmp, {"session_2026-08-25-mine":            ([{"session_id": "SID-A"}], CLOSED),
                "session_2026-08-21-stale-neverclosed": (None, OPEN)})
    record("A01", "REGRESSION: a session survives writing its own close-out record",
           open_session(tmp, "SID-A") == "session_2026-08-25-mine",
           f"got {open_session(tmp, 'SID-A')!r} — fell back to a stale open session")
    record("A02", "and without the anchor it demonstrably would not have",
           open_session(tmp, None) == "session_2026-08-21-stale-neverclosed",
           "the guess no longer reproduces the failure this test pins")
    record("A03", "a NEW session does not inherit an anchored directory",
           open_session(tmp, "SID-B") == "session_2026-08-21-stale-neverclosed",
           f"got {open_session(tmp, 'SID-B')!r}")

    # ── R: never raise. This runs on every Bash call; an exception here would be
    #      a gap in the research, not just in the record.
    build(tmp, {"session_2026-08-25-mine":  ([{"session_id": "SID-A"}], OPEN),
                "session_2026-08-26-empty": ([], OPEN)})
    record("R01", "an empty log is tolerated",
           open_session(tmp, "SID-A") == "session_2026-08-25-mine")
    (tmp / "scratchpad" / "session_2026-08-26-empty" / "commands.jsonl").write_text("not json\n")
    record("R02", "a malformed log is tolerated",
           open_session(tmp, "SID-A") == "session_2026-08-25-mine")
    record("R03", "no scratchpad directory returns '' rather than raising",
           open_session(pathlib.Path(tempfile.mkdtemp()), "SID-A") == "")
    record("R04", "no open session and no anchor returns '' (caller then files loudly)",
           open_session(build(pathlib.Path(tempfile.mkdtemp()),
                              {"session_2026-08-25-x": (None, CLOSED)}), "SID-Z") == "")

    # ── W: the writer must actually record the anchor the reader depends on ──
    src = HOOK.read_text()
    record("W01", "the hook writes session_id onto every line",
           '"session_id":sid' in src.replace(" ", ""),
           "open_session anchors on a field nothing writes — the anchor is dead")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\n" + "=" * 70)
print(f"EXAMINED: {len(results)} assertion(s)")
print(f"RESULTS: {sum(results)}/{len(results)} tests passed")
if sum(results) < len(results):
    print(f"FAILED: {len(results) - sum(results)}")
print("=" * 70)
sys.exit(0 if sum(results) == len(results) else 1)
