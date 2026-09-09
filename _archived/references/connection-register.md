# Connection Register — REDIRECTED

**The connection register is the `connections` table in `data/guidebook.db`.**

```
python3 scripts/db.py connections --status PENDING
python3 scripts/db.py connections --status PENDING --confidence HIGH
python3 scripts/db.py connections --summary
```

Reasoning for a given connection lives at `references/connection-reasoning/<con-id>.md`;
the per-topic narrative files are under `references/connections/`.

## Do not read the split files

This stub used to say "split into `connection-register-active.md` (PENDING entries — use
this) and `connection-register-archive.md`". That instruction was correct for nine days.
Both files were themselves archived on 2026-04-08 (CO-0006 Phase 0B-1) and carry banners
saying so, while this stub — the file a session lands on first, because it has the obvious
name — kept sending readers to them for four months.

The numbers, measured 2026-08-06: the two split files hold **113** distinct CON ids
between them. `references/connections/**` holds **246**. The `connections` table holds
**273**. Every id in the split files appears in both of the others; they contain nothing
unique, and they are missing 160 connections that exist in the database. A session that
followed this stub got a stale subset and no way to tell.

Retiring the three files to `_archived/references/` was recorded here as owner-gated
(a file move — the former CLAUDE.md §9 guardrail 4). **That guardrail no longer exists.**
The 2026-08-19 rewrite replaced it with §1: removal needs *evidence*, not permission, and
the owner's 2026-08-19 ruling makes `_archived/` the right home for retired reader-facing
content. Owner sign-off is still required for the DG-NON class — mission, audience, CRPD
posture, population taxonomy, evidence-tier definitions, jurisdiction and work-product
inclusion, licensing, trajectory — and a stale duplicate register is none of those. The
evidence §1 asks for is the paragraph above. [Pointer corrected 2026-08-22.] It is item W4.4 of
`workplan/2026-08-02-architecture-decision-and-execution-plan.md`. The reconciliation that
must precede it is done and is the paragraph above: the registers are a strict subset, so
the retirement loses nothing.
