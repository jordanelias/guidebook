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
        # exit_code is absent from this harness's PostToolUse payload; is_error is
        # what it actually carries. Record both and let the reader see which was
        # available rather than storing a field that is always null.
        ec=tr.get("exit_code")
        err=tr.get("is_error")
    else:
        out=str(tr or ""); ec=None; err=None
    root=pathlib.Path(os.environ.get("CLAUDE_PROJECT_DIR") or ".")
    sf=root/".claude"/"session"
    sess=sf.read_text().strip() if sf.exists() else (d.get("session_id") or "unassigned")
    p=root/"scratchpad"/sess
    p.mkdir(parents=True,exist_ok=True)
    b=out.encode("utf-8","replace")
    rec={"ts":datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
         "cwd":d.get("cwd"),"command":c,"exit":ec,"is_error":err,
         "stdout_sha256":hashlib.sha256(b).hexdigest(),"bytes":len(b)}
    with open(p/"commands.jsonl","a",encoding="utf-8") as fh:
        fh.write(json.dumps(rec,ensure_ascii=False)+"\n")
except Exception:
    pass
