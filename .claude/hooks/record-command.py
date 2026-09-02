#!/usr/bin/env python3
"""PostToolUse(Bash) — persist the scratchpad mechanically, not by memory.

Owner directive 2026-08-20: "the scratchpad needs to be getting saved always for
provenance." Prose cannot deliver that: an agent must choose to load it, and
attention degrades as context fills. This runs at the HARNESS level, so the
record exists whether or not the session remembers to make one.

Appends one JSON line per Bash call to scratchpad/<session>/commands.jsonl.
The session stem is DERIVED (see `open_session` below), never read from a
pointer that answers a different question.

Fails silently and always exits 0 by design: provenance capture must never block
or fail the work it is recording. A missing line is a gap in the record; a
raised exception would be a gap in the research.

Bearing on tier grading: a tier is a JUDGEMENT, and a judgement without a
recorded derivation is an assertion. co1_provenance being NULL on all three
Co-1-tiered rows is the same defect class as a citation written from memory —
see workplan/2026-08-20-adversarial-adjudication-a18-aut.md §4.
"""

import sys,json,os,hashlib,datetime,pathlib


def open_session(root, sid=None):
    """Stem of the session running NOW, derived. '' when it cannot be told.

    THE 2026-08-23 FIX WAS WRONG AND THIS RECORDS WHY, because the wrong version
    is the plausible one and will be reached for again.

    Until 2026-08-23 this hook read `.claude/session`. That pointer went stale and
    filed one session's commands under the previous session's scratchpad. The fix
    swapped it for `sessions/LATEST` on the ground that LATEST is "the single home
    for this fact". IT IS NOT. LATEST answers *which session record is most recent*
    and is moved BY THE CLOSE-OUT RITUAL — so for the entire life of a session it
    names the PREVIOUS one. Both pointers were stale in exactly the same way and
    for exactly the same reason; swapping which stale pointer you read changed
    nothing. MEASURED 2026-08-25, in the file the fix was supposed to protect:

        scratchpad/session_2026-08-23-research-batch-03-forward-mining/commands.jsonl
            5 lines dated 2026-08-23   <- its own session
          405 lines dated 2026-08-24   <- session_2026-08-24-pointer-discipline
          274 lines dated 2026-08-25   <- session_2026-08-25-rulings-...-sweep

    Three sessions, one file, named after the earliest. The two later sessions have
    scratchpad directories of their own and NO commands.jsonl in them. That defeats
    the owner directive the whole hook exists to serve (2026-08-20, "the scratchpad
    needs to be getting saved always for provenance"; 2026-08-25, "so that we
    actually have a surface to review") -- a surface filed under another session's
    name is not a review surface, and it corrupts that session's frozen record too.

    So DERIVE it instead, from a fact already stated once, with no new pointer:

        A SESSION IS CLOSED EXACTLY WHEN ITS RECORD sessions/<stem>.md EXISTS.

    A scratchpad/session_* directory with no record behind it is therefore OPEN,
    and the newest open one is the session running now (stems are date-prefixed by
    convention, so lexical order is chronological). Verified against the same three
    sessions: 08-23 has a record and is closed; 08-24 and 08-25 have none, which is
    exactly why their lines had nowhere correct to go.

    LIMIT, stated rather than discovered later: stems are date-prefixed, so lexical
    order is chronological ACROSS days but arbitrary WITHIN one. Two sessions opened
    on the same UTC day and both left un-closed tie on alphabet. That case resolves
    by closing sessions out, not by making this cleverer -- 08-21-reasoning-doc-
    digestion has been OPEN since 2026-08-21 for exactly that want of a close-out.

    Returning '' rather than guessing is deliberate. The caller then files under the
    harness session id -- a visibly foreign directory name. A WRONG ANSWER MUST BE
    LOUD. Silently appending to a closed session's log is the failure this function
    exists to end, and it stayed invisible for three sessions precisely because it
    produced a plausible-looking file.

    `sid` IS THE ANCHOR, AND THE DERIVATION ABOVE IS ONLY THE OPENING GUESS. The
    harness session id is the one fact that actually says which session is running;
    everything else here is inference from filenames. So it is written onto EVERY
    line, and once a line exists this function stops inferring and follows it: the
    session's own lines are always appended, so a directory whose log ENDS with our
    sid is our directory. Exact from line 2 onward.

    That is not tidiness, it closes a real hole. Tested before shipping: the moment a
    session writes its own close-out record `sessions/<stem>.md` -- the documented
    ritual, and sessions routinely keep working afterwards -- the newest-open rule
    stops matching it and falls back to the newest STALE open session. Measured:
    with 08-25's record present, the guess returned `session_2026-08-24-pointer-
    discipline`, a session that ended a day earlier. Same defect as the one this
    function was written to fix, reached by a different door. The anchor holds
    through close-out because it does not care about records at all.

    Recording the sid also makes the log SELF-DESCRIBING: a reader partitions it by
    a stated fact instead of inferring boundaries from timestamps. That is what made
    the three misfiled sessions unsplittable -- the 08-24 session ran through
    midnight UTC, so the only available boundary was a guess. Future logs carry the
    answer.
    """
    # scratchpad/CURRENT IS A STATED FACT AND OUTRANKS EVERY INFERENCE BELOW.
    #
    # Added 2026-09-02, after measuring that ALL 969 lines of three project sessions
    # had landed in ONE directory -- batch 04's -- while batch 05's scratchpad held no
    # commands.jsonl at all. The docstring above calls `sid` the anchor. It is not:
    # `sid` identifies the HARNESS session, and one harness session spans as many
    # project sessions as the container survives. Here a single sid covered batch 04,
    # a repairs session and batch 05. So the anchor matched the first directory it
    # ever wrote to and returned it forever -- the hook locking onto its own first
    # mistake, which is why the misfiling was total rather than partial.
    #
    # The two existing pointers cannot help: CLAUDE.md 7 records that `sessions/LATEST`
    # and `LATEST-RESEARCH` both move at CLOSE, so both name the PREVIOUS session for
    # the whole life of the current one. CURRENT moves at OPEN, which is the only time
    # a pointer to the running session can be correct.
    cur = root/"scratchpad"/"CURRENT"
    try:
        stated = cur.read_text(encoding="utf-8").strip()
    except OSError:
        stated = ""
    if stated and (root/"scratchpad"/stated).is_dir():
        return stated

    try:
        # Accepts pr-<n>-<slug> as well as session_<stem>: owner directive 2026-09-02,
        # scratchpad folders are named for the PR they belong to. Both prefixes are
        # matched because the historical directories keep their names.
        pads = sorted(q.name for q in (root/"scratchpad").iterdir()
                      if q.is_dir() and (q.name.startswith("session_")
                                         or q.name.startswith("pr-")))
    except OSError:
        return ""
    if sid:
        for n in reversed(pads):
            f = root/"scratchpad"/n/"commands.jsonl"
            try:
                # Last line only: our lines are appended, so if this log is ours it
                # ends with us. Reading whole logs on every Bash call would grow
                # without bound for an answer the tail already gives.
                last = f.read_bytes().rsplit(b"\n", 2)[-2 if f.stat().st_size else 0]
                if json.loads(last).get("session_id") == sid:
                    return n
            except (OSError, ValueError, IndexError):
                continue
    openp = [n for n in pads if not (root/"sessions"/f"{n}.md").exists()]
    return openp[-1] if openp else ""


try:
    d=json.load(sys.stdin)
    ti=d.get("tool_input") or {}
    c=ti.get("command")
    if not c: sys.exit(0)
    # Do not record commands that COMMIT or PUSH. Two reasons, and the second is
    # the one that matters.
    #
    # (1) Convergence. This file is tracked, so appending to it dirties the
    #     worktree. The stop hook demands a clean tree. Recording the very
    #     command that commits the record leaves a new uncommitted line every
    #     time — a livelock with no fixed point, observed 2026-08-21 across four
    #     consecutive turns. The record of an action is always written after the
    #     action, so no ordering fixes this; only not recording it does.
    #
    # (2) It loses nothing. A commit's provenance is ALREADY in git — message,
    #     author, timestamp, tree sha, full diff — which is a stronger and more
    #     durable record than a sha256 of stdout. The scratchpad exists for the
    #     commands git does NOT record: queries, probes, retrievals, gate runs.
    #     Skipping the one class git already covers is narrowing the apparatus
    #     to what it is for.
    #
    # Deliberately loose: a compound command containing a commit is skipped
    # whole. Whatever else it did is visible in that commit's own diff.
    #
    # EXTENDED 2026-08-23. The 2026-08-21 fix named the livelock correctly and
    # then closed only half of it. The other half is `git status`: the stop hook
    # demands a clean tree, checking the tree means running git status, and
    # recording that run dirties the tree again. Observed across three turns
    # today — commit, check, dirty, commit, check, dirty. Identical fixed-point
    # problem, identical remedy.
    #
    # The class is READ-ONLY QUERIES OF GIT'S OWN STATE. Argument (2) above
    # applies to them with full force: git already holds everything these
    # commands read, so recording a query OF git INTO a git-tracked file is the
    # purest form of the recursion this repository exists to resist. Commands
    # that MUTATE the tree (add, mv, rm, checkout) are still recorded — they
    # change something, and what they changed is worth a line.
    GIT_READONLY = ("git status", "git diff", "git log", "git rev-parse",
                    "git rev-list", "git ls-files", "git show", "git branch",
                    "git stash list")
    if "git commit" in c or "git push" in c: sys.exit(0)
    if any(q in c for q in GIT_READONLY): sys.exit(0)
    tr=d.get("tool_response")
    out=""
    if isinstance(tr,dict):
        out=tr.get("stdout") or ""
        # MEASURED CORRECTION 2026-08-22. This comment used to read: "exit_code is
        # absent from this harness's PostToolUse payload; is_error is what it
        # actually carries." That is FALSE, and its own log falsifies it: of 356
        # committed lines, exactly one carries a non-null `exit` and one a non-null
        # `is_error`, and both are hand-fed probes (`echo test`; `cwd: /x`). Across
        # 354 real harness events BOTH keys are absent, so both `.get()`s return
        # None every time. The belief came from the synthetic probe, not a payload.
        #
        # The fields are KEPT rather than deleted, deliberately: this log is
        # append-only and 356 lines already carry the schema, so dropping keys
        # mid-stream would make the old and new records differ for a reason that
        # has nothing to do with what happened. But READ THEM AS ALWAYS-NULL. A
        # line in this file proves a command was ISSUED. It does not prove it
        # SUCCEEDED, and no gate, session record or attestation may cite it as if
        # it did. `response_keys` below records what the payload actually carried,
        # so the next auditor measures instead of inferring.
        ec=tr.get("exit_code")
        err=tr.get("is_error")
        # MEASURED 2026-08-22 by recording response_keys for one turn. This
        # harness's Bash tool_response carries exactly:
        #   interrupted, isImage, noOutputExpected, stderr, stdout
        # No exit_code and no is_error — hence the correction above.
        #
        # SECOND MEASUREMENT, SAME DAY, CORRECTING THE FIRST. When these fields
        # were added the comment here claimed `stderr` "IS carried and was being
        # thrown away, which is why the log could not distinguish a gate that
        # passed from a gate that raised." That inferred a capability from the
        # PRESENCE OF A KEY. Measured over 88 real events in
        # scratchpad/session_2026-08-22-research-batch-02-.../commands.jsonl:
        # stderr_bytes is 0 on EVERY line, including two commands that raised
        # Python tracebacks (an IntegrityError on a column type and another on a
        # CHECK constraint). The key exists and is empty; the error text reaches
        # the caller by some other route.
        #
        # So the honest statement is the uncomfortable one: THIS LOG STILL CANNOT
        # TELL YOU WHETHER A COMMAND SUCCEEDED. exit and is_error are absent,
        # stderr is present-but-empty, and the only real signals are `interrupted`
        # and the size of stdout. The fields are kept because recording a measured
        # empty is worth more than recording nothing — a future harness may
        # populate stderr, and then these lines become comparable — but no gate,
        # session record or attestation may cite a line in this file as evidence
        # that a command WORKED. It proves a command was ISSUED.
        errout=tr.get("stderr") or ""
        interrupted=tr.get("interrupted")
    else:
        out=str(tr or ""); ec=None; err=None; errout=""; interrupted=None
    root=pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".")
    sid=d.get("session_id")
    sess=open_session(root,sid) or (sid or "unassigned")
    p=root/"scratchpad"/sess
    p.mkdir(parents=True,exist_ok=True)
    b=out.encode("utf-8","replace")
    eb=errout.encode("utf-8","replace")
    rec={"ts":datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
         "cwd":d.get("cwd"),"command":c,"exit":ec,"is_error":err,
         # Ground truth for WHICH SESSION issued this. Every other signal in this
         # hook is inferred from filenames; this one is stated. See open_session().
         "session_id":sid,
         "interrupted":interrupted,
         "response_keys":sorted(tr.keys()) if isinstance(tr,dict) else None,
         "stdout_sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),
         "stderr_sha256":hashlib.sha256(eb).hexdigest() if eb else None,
         "stderr_bytes":len(eb)}
    with open(p/"commands.jsonl","a",encoding="utf-8") as fh:
        fh.write(json.dumps(rec,ensure_ascii=False)+"\n")
except Exception:
    pass
