# Concurrent-write architecture — proposal

**Filed:** 2026-05-11 (session_2026-05-11g-citation-mining.md)
**Gap:** GAP-290 (P1, AUDT)
**Status:** Proposal — awaiting owner decision

## Context

`data/guidebook.db` is a SQLite binary file committed directly to git. The project's session model assumes a single agent writes the file per session, but session boundaries are not enforced architecturally. When two agents work concurrently, git's last-write-wins semantics on the binary file cause complete data loss for whichever session pushed earlier.

This is not theoretical. **Session 2026-05-11g-citation-mining (this session) was clobbered three times in a single 8-minute window** by session_2026-05-11e-wayfinding-dementia (a workplan-orchestrator session running in parallel). Timeline:

| Time (UTC) | Event | Outcome for this session |
|---|---|---|
| 03:24 | 1st-tranche DB push (commit `89543326e7`) | Lands |
| 03:32 | 2nd-tranche + 3rd-tranche DB pushes (commits `3d36bc682b`, `0b27fe5966`) | Lands |
| 04:13 | wayfinding-dementia push #1 (`d803dbda39`) | **My 14 sources / 21 mining rows / 7 gaps / 700 cleanups / 2 renumbers — all lost** |
| 04:16 | My 1st recovery (`b254fb71a1`) | Restored |
| 04:17 | wayfinding-dementia push #2 (`ab30ef3d81`, 31s after my recovery) | **All restored work lost again** |
| 04:19 | My 2nd recovery (`1dc4ca4d25`) | Restored |
| 04:21 | wayfinding-dementia push #3 (`c2bc96be28`, 68s after my recovery) | **Lost a third time** |
| 04:22 | Session ends with DB writes unrecoverable while wayfinding-dementia continues pushing | Captured in `scripts/migrations/session_2026_05_11g_data.json` for future replay |

The wayfinding-dementia session is not at fault. Both sessions performed legitimate, valuable work on disjoint slices of the DB (search_languages for wayfinding-dementia; evidence_sources / citation_mining / source_slug_links / gaps for this session). Neither agent could have known the other was writing concurrently. The architecture cannot support concurrent writers.

## What survived this session

- All code commits (skills, audit scripts, CI workflow, governance memos, session file) — different files, no conflict
- A captured snapshot of the lost DB work in `scripts/migrations/session_2026_05_11g_data.json`
- A replay script `scripts/migrations/session_2026_05_11g_replay.py` (idempotent)

The replay can be run when the wayfinding-dementia session finishes — but that strategy only works because the two sessions touched disjoint slices. Two sessions modifying the *same row* would lose data with no recovery path.

## Failure modes by likelihood

Ranked by what we've observed in practice:

1. **Two sessions writing to different tables, same DB** — common (this session vs wayfinding-dementia). Recoverable via replay if both sessions captured their work; data-loss otherwise. **Currently the dominant failure mode.**
2. **Two sessions writing to the same row** — would cause silent data conflict. The "winner" is whoever pushed last; the loser's edits vanish without notice unless they validate post-push. **Latent risk** — hasn't been observed because most sessions slice by slug/topic.
3. **Schema drift across sessions** — if two sessions run migrations independently, the later one will fail when its CREATE conflicts. Would surface loudly. **Low frequency, high signal.**

## Option A — Session-level lock file (lightweight)

Add `sessions/CURRENT_WRITER.txt` with format:

```
session: session_2026-05-11g-citation-mining.md
acquired_at: 2026-05-11T03:24:00Z
expires_at: 2026-05-11T04:24:00Z
heartbeat_at: 2026-05-11T04:15:00Z
```

Sessions must:
- Acquire the lock before any DB write (CAS-style: pull, check expiry, write+commit lock file as first commit)
- Heartbeat (rewrite lock file with refreshed `expires_at`) every 5 min
- Release the lock on session close (delete the file)
- If lock is owned by another session and not expired: ABORT or wait

### Pros
- Minimal infrastructure change — just a new file convention
- Works within existing git workflow
- Can be enforced via `.github/workflows/audit.yml` (block DB-file pushes if the lock is held by another session)

### Cons
- **Has its own race condition** — two sessions can both pull, both see "no current writer," both write the lock file. The lock commit is itself a race.
- Requires every skill that writes to honor the convention. Strong coordination dependency.
- No protection against a misbehaving session that ignores the lock.
- Stale-lock recovery (session died mid-work) is manual.

### Verdict
Easy to ship; weak guarantees. Mitigates the *frequency* of clobbers but not the *possibility*. Recommend ONLY as Phase 0 (interim) while a stronger fix lands.

## Option B — Migration-based schema (text-merge friendly)

Treat `data/guidebook.db` as a derived artifact. Sessions write `migrations/{timestamp}-{session}.sql` (or `.py`) files containing SQL/script operations. A CI step applies migrations sequentially to produce the binary DB.

### Pros
- Migration files are text — **git can actually merge them**. Two sessions can land independent migrations on the same branch with no conflict.
- Reproducible. Anyone can rebuild the DB from migrations.
- Auditable. Every DB change is a reviewable commit with a clear message.
- Compatible with this session's existing replay script (`session_2026_05_11g_replay.py`) — that IS a migration in this style.

### Cons
- **Significant migration effort** — convert all existing sessions' workflows to write migrations instead of (or in addition to) raw DB.
- Performance: replaying many migrations to rebuild the DB grows linearly with history. Mitigation: periodic "snapshot" migrations that consolidate prior history.
- Schema changes (ALTER TABLE) interact with migration ordering — needs care.
- Some skills (e.g., `db.py upsert-coverage`) issue many small updates; converting each to a migration creates churn.

### Verdict
Right answer for long-term integrity. Aligns with how mature systems handle DB-as-code (Alembic, Flyway, sqitch). Requires meaningful engineering work.

## Option C — Live DB outside git (infrastructure shift)

Move the live DB to a hosted service (Turso, Supabase, Postgres, etc.). Git holds a periodic snapshot for reference only; live writes go to the hosted DB via API.

### Pros
- Proper concurrency control at the DB level (transactions, locks, isolation).
- No git-merge issues at all — the binary file is no longer authoritative.
- Scales to many concurrent agents.

### Cons
- **Infrastructure dependency** — credentials, hosting, billing, uptime, backup.
- Session-replay testability decreases (can't `git checkout` and recreate state offline as easily).
- Migration cost includes both the architecture shift and ops work.

### Verdict
Strongest guarantees. Highest setup cost. Worth it if the project plans for >2 concurrent agents routinely.

## Recommendation

**Phase 0 (immediate, 1–2 days):** Adopt Option A. Add `sessions/CURRENT_WRITER.txt` convention. Add a CI check that blocks DB pushes if the lock is held. Accept the residual race risk. This stops 90% of clobbers.

**Phase 1 (1–2 weeks):** Adopt Option B. Begin writing migration files alongside DB pushes. Build the migration-runner that produces the binary DB from migrations. Make migration files the source of truth; binary DB becomes a build artifact in `.gitignore`. The replay script written this session (`scripts/migrations/session_2026_05_11g_replay.py`) is the template.

**Phase 2 (decision later):** Evaluate Option C against actual contention rate. If Phase 1's migration approach keeps up with the project's growth, skip Option C. If the migration history grows unwieldy or contention persists, migrate to a hosted DB.

## Acceptance criteria for closing GAP-290

- `sessions/CURRENT_WRITER.txt` convention documented in `governance/` and adopted by at least one writing skill (Phase 0 milestone)
- A migration-runner script (`scripts/migrations/run.py`) that takes the DB state from previous migration to a target migration (Phase 1 milestone)
- A demonstration: two simulated concurrent sessions, each writing a migration, both land on `main` cleanly, both replays produce the merged DB (Phase 1 acceptance test)

## Open questions for the owner

1. Is Phase 1 (migration-based) the intended trajectory, or do you want Option C (hosted DB) sooner?
2. Should the `CURRENT_WRITER` lock be opt-in (skills opt-in by calling a `acquire-writer-lock` helper) or mandatory (CI blocks any DB push without a lock)?
3. The wayfinding-dementia session today demonstrated the failure mode. Is there an owner-controlled way to halt or coordinate concurrent agents in the interim?
