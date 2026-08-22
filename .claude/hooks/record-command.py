#!/usr/bin/env python3
"""PostToolUse(Bash) — persist the scratchpad mechanically, not by memory.

Owner directive 2026-08-20: "the scratchpad needs to be getting saved always for
provenance." Prose cannot deliver that: an agent must choose to load it, and
attention degrades as context fills. This runs at the HARNESS level, so the
record exists whether or not the session remembers to make one.

Appends one JSON line per Bash call to scratchpad/<session>/commands.jsonl.
The session stem comes from .claude/session (bare stem, as the DB stores it),
falling back to the harness session_id.

Fails silently and always exits 0 by design: provenance capture must never block
or fail the work it is recording. A missing line is a gap in the record; a
raised exception would be a gap in the research.

Bearing on tier grading: a tier is a JUDGEMENT, and a judgement without a
recorded derivation is an assertion. co1_provenance being NULL on all three
Co-1-tiered rows is the same defect class as a citation written from memory —
see workplan/2026-08-20-adversarial-adjudication-a18-aut.md §4.
"""

import sys,json,os,hashlib,datetime,pathlib
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
    if "git commit" in c or "git push" in c: sys.exit(0)
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
    sf=root/".claude"/"session"
    sess=sf.read_text().strip() if sf.exists() else (d.get("session_id") or "unassigned")
    p=root/"scratchpad"/sess
    p.mkdir(parents=True,exist_ok=True)
    b=out.encode("utf-8","replace")
    eb=errout.encode("utf-8","replace")
    rec={"ts":datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
         "cwd":d.get("cwd"),"command":c,"exit":ec,"is_error":err,
         "interrupted":interrupted,
         "response_keys":sorted(tr.keys()) if isinstance(tr,dict) else None,
         "stdout_sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b),
         "stderr_sha256":hashlib.sha256(eb).hexdigest() if eb else None,
         "stderr_bytes":len(eb)}
    with open(p/"commands.jsonl","a",encoding="utf-8") as fh:
        fh.write(json.dumps(rec,ensure_ascii=False)+"\n")
except Exception:
    pass
