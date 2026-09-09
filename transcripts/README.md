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

**The JSONL here is hidden from ripgrep, and that was measured, not assumed.** With it
searchable, `REF-00977` returned 174 hits of which 136 were transcripts, and `next_ref_id`
305 of which 194 — a session grepping for a fact got more noise than signal, from
conversation that includes superseded and simply wrong statements. Owner ruling 2026-09-03
under `DR-2026-08-06-cold-storage-search-scope.md`. After: 39 hits, identical whether or
not transcripts are excluded.

**This README and every `index.json` stay searchable on purpose.** A grep still finds THAT
a transcript exists and which agent, role and time it belongs to; the file itself is one
`git grep` or one open away. Nothing is deleted, untracked, or hidden from code — git,
`grep -r`, `git grep`, Glob and all Python tooling read the whole tree.

The `.ignore` entry matches `transcripts/**/*.jsonl`, not the directory. `transcripts/**`
with negations was tried first and **failed a planted-token test**: README.md came back and
`index.json` did not, because `**` excludes the session directory and gitignore cannot
re-include a file whose parent is excluded. Matching the payload by extension needs no
negation, so there is nothing left to get subtly wrong. D05-030 closed.
