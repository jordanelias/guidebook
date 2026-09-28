-- 099_citation_mining_connections_produced_retires.sql
-- SCHEMA migration — DR-2026-09-26 phase 2b. `citation_mining.connections_produced`
-- retires as a written fact (rule 5): the event home RC5 settled in migration 098 --
-- `search_executions` (via `mined_ref_id`) together with `search_candidates.exec_id` --
-- is now where a mining pass's yield is recorded, and this column was the copy.
--
-- WHY THE REBUILD HAS TO COME BEFORE THE WRITER RETIRES (not after, rule 5's usual
-- order). The column is `TEXT NOT NULL DEFAULT '[]'`. A retired writer omitting the
-- column from its INSERT would still take the DEFAULT and write '[]', which every
-- reader has always taken to mean "this pass produced nothing" -- indistinguishable
-- from a real empty result. Only after NOT NULL is relaxed can a retired writer leave
-- the column NULL, which is what "NULL forward" (rule 5) actually requires here.
--
-- Rule 3 still forbids dropping the column outright: committed data migrations
-- INSERT it (`grep -lE 'INSERT INTO "?citation_mining"?' scripts/migrations/data_*.sql | wc -l`
-- printed 18 at authoring time; re-run, do not trust this number, rule 7a -- a plain
-- `grep -l connections_produced` over the same glob answers a different question and,
-- caught by an adversarial pass, already includes this PR's own data migration, which
-- mentions the column in prose without inserting it). The column stays; only its
-- constraint changes. Historical values are copied verbatim and untouched -- including
-- whatever shape they hold: a 2026-09-21-vintage comment in
-- scripts/tests/test_db_integrity.py claims 13 of 25 non-empty rows hold a bare integer
-- rather than a JSON array. That claim is FALSE OF LIVE DATA TODAY, discovered while
-- writing this migration (rule 7a's own failure mode, caught before it compounded):
-- `python3 -c "import sqlite3,json; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); print([type(json.loads(v)).__name__ for (v,) in c.execute('select connections_produced from citation_mining')])"`
-- prints `list` for all 29 live rows today. An adversarial pass went further and found
-- it false even at its own introducing commit (`git log -S"13 of its 25" -- scripts/tests/test_db_integrity.py`
-- finds it first at fae3fb0, 2026-09-18, not 2026-09-21; that commit's own DB blob holds
-- 16 rows, 7 non-empty, zero bare scalars) -- so "STALE" overclaimed a history nothing
-- here verifies. Recorded plainly at the source as false, not as having drifted.
--
-- No view, trigger, or inbound FK touches this table or this column
-- (`select name from sqlite_master where sql like '%connections_produced%'` names
-- only citation_mining itself; `PRAGMA foreign_key_list` on every live table finds no
-- inbound reference to citation_mining). The rebuild follows migration 067's own
-- precedent for this exact table: every column, CHECK and the primary key are
-- reproduced verbatim; only connections_produced changes shape.

CREATE TABLE citation_mining_new (
    slug                TEXT NOT NULL REFERENCES slugs(slug),
    local_ref_id        TEXT NOT NULL,
    global_ref_id       TEXT,
    doi                 TEXT,
    backward            INTEGER NOT NULL DEFAULT 0 CHECK(backward IN (0,1)),
    forward             INTEGER NOT NULL DEFAULT 0 CHECK(forward IN (0,1)),
    -- WAS: TEXT NOT NULL DEFAULT '[]'. Relaxed so a retired writer can leave it NULL
    -- instead of taking the old default and being misread as "found nothing". See
    -- header. The writer that stops setting it is scripts/db.py:log_mining.
    connections_produced TEXT,
    notes               TEXT,
    created_at          TEXT NOT NULL,
    created_by_session  TEXT NOT NULL,
    updated_at          TEXT NOT NULL,
    updated_by_session  TEXT NOT NULL,
    deferred_reason     TEXT,
    PRIMARY KEY (slug, local_ref_id)
);

INSERT INTO citation_mining_new
SELECT slug, local_ref_id, global_ref_id, doi, backward, forward,
       connections_produced, notes, created_at, created_by_session,
       updated_at, updated_by_session, deferred_reason
FROM citation_mining;

DROP TABLE citation_mining;
ALTER TABLE citation_mining_new RENAME TO citation_mining;

CREATE INDEX idx_cm_unmined ON citation_mining(slug, backward, forward);

PRAGMA user_version = 99;
