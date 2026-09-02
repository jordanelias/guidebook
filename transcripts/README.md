# Agent transcripts — primary provenance

**This directory is the single home for what the agents actually did.** Not what they
concluded — the conclusions live in session records, commit messages and the DB. This is
the workings: every tool call, every query, every intermediate result, verbatim.

## Why it exists

On 2026-09-02 the owner asked whether the adversarial pass's direct workings had been
lost. They had been about to be. The antagonist ran read-only and wrote nothing itself;
its findings reached the repository only through commit messages and a defect register,
and the `antagonist/` scratchpad directory stood empty. Its transcript existed **only in
ephemeral container storage** and would have gone when the container was reclaimed.

That had already happened once in the same session: the first antagonist run was killed
mid-flight by a container restart, and everything it had done survived only because the
orchestrator happened to have read its partial output before it died.

**The project's infrastructure is incomplete, so the transcripts are how we audit the
workflow itself.** A conclusion you cannot trace is a conclusion you cannot correct.

## What is here

`harness_<id>/main.jsonl` — the orchestrator's own transcript for that harness session.
`harness_<id>/subagents/<started>_<role>_<agentid>.jsonl` — one per subagent.
`harness_<id>/index.json` — machine-readable: start time, role, size, agent id, filename.

Roles are **derived from each agent's own brief**, not from filenames. Note that
`ANTAGONIST` contains the substring `AGONIST`; a naive match mislabels every antagonist
as an agonist, which it did once here before being caught.

One harness session can span several *project* sessions — `harness_6a6f63cd` covers both
research batch 04 (2026-09-01) and batch 05 (2026-09-02).

## Reading them

JSONL, one record per line. Roughly:

```python
import json
for line in open("transcripts/harness_6a6f63cd/subagents/....jsonl", errors="replace"):
    rec = json.loads(line)
    if rec.get("type") == "assistant":
        for c in (rec.get("message") or {}).get("content") or []:
            if c.get("type") == "text":   print(c["text"])
            if c.get("type") == "tool_use": print(c["name"], c["input"])
```

## Two things to know before relying on this

**It is captured by hand, and that is a defect, not a design.** Nothing in the repository
copies these files. They were copied because someone asked the right question at the right
moment. **A session that does not think of it will lose its own transcripts**, exactly as
this one nearly did. Registered as D05-029.

**Search scope is unresolved and owner-gated.** These files are large and full of
intermediate text. Left visible to ripgrep they will flood ordinary searches — the precise
problem `.ignore` exists to solve. But adding an entry to `.ignore` is owner-gated by
`decisions/DR-2026-08-06-cold-storage-search-scope.md`, so no entry was added. Until the
owner rules: `git grep`, `grep -r`, Glob and all Python tooling see these files; if
ripgrep results become unusable, that is the reason. Registered as D05-030.
