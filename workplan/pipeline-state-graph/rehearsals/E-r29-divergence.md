# E-divergence: rehearsal of R29 (compensating migration for the `migration_reproducibility_deep` divergence)

Clone: `$S/rehearsals/E-divergence`, branch `r29-rehearsal`, base `31142552` (its DB blob is `d874ba9e`'s, git blob `2d37c876`). Nothing in `/home/user/guidebook` was written; its `git status` shows only the harness's own appends (`commands.jsonl`, `transcripts/`).

## Verdict

**EXECUTABLE WITH CHANGES.** The divergence clears with no invented data: every restored value is read from a `--rebuild` (the migration chain), and the deep check goes from FAIL to PASS. Three things in R29 and the plan do not hold as worded:

1. **R29's OVERTURN condition is met.** It reads "a divergent value shown to be payload-backed and not reproducible by any verb". All 27 divergent `evidence_sources` values, and the one ORCID the bot added, match CrossRef payloads that research sessions persisted before the bot ran. No verb can write any of the seven columns. The revert still stands on other grounds: nothing that reaches the book reads these columns, and two of them hold the wrong kind of value. The overturn clause needs rewording (see the last section).
2. **The re-entry branch is empty, because it cannot be executed.** `--verify-authors` only verifies and writes nothing. `amend-source` refuses all seven columns. `correct-source` writes only `retrieval_log.PAYLOAD_FIELDS`, which contains none of them. Re-entering any value needs a tooling PR first (rule 10).
3. **The sanctioned capture path alone gives a migration that breaks `--rebuild`.** `emit_batch_sql.py` captures a delta against the blob. A compensating migration also replays against the chain, which still holds the original author rows, so the replay fails with `UNIQUE constraint failed: evidence_source_authors.id`. The fix is 24 hand-added keyed `DELETE`s, marked in the file.

There is also an ordering constraint the plan does not state. The migration must land **after** step 1.5's deletion of `resolve-dois.yml` has merged. An offline replay of `resolve_dois.enrich_from_crossref`, using the persisted payloads, recreates the same divergence on the next scheduled run: 4 rows, 27 values and 24 author rows.

## (1) The divergence, reproduced

`python3 scripts/audit/migration_reproducibility.py --deep` at base reports `evidence_sources CONTENT 4 rows` and FAIL (deep). The checker's five-column summary hides two columns, so I also ran a full row diff (`E-tools/rowdiff.py`, keyed on the primary key). Its output is in `E-divergence_divergence.tsv` (attributed) and `E-divergence_rowdiff_rebuild_vs_committed.full.txt` (raw).

| table | rows | what differs (blob vs chain) |
|---|---|---|
| `evidence_sources` | REF-01006, REF-01007, REF-01009, REF-01011 | `author_count_is_complete` 0→1 (4); `journal_abbrev`, `issn`, `pub_month`, `subtype`, `citation_count` NULL→value (4 each); `language` NULL→'en' (3; REF-01011 has none upstream). That is **27 substantive values in 7 columns**, plus `updated_at` and `updated_by_session` (volatile) |
| `evidence_source_authors` (exempt at base) | 24 rows | the chain's ids 182–187, 194–197, 203–210 and 212–217 were deleted and re-inserted as 188–193, 199–202 and 245–258. Names are identical; `created_at` and `created_by_session` are new; REF-01007 position 2 (Köptcke) gained ORCID `0000-0001-7079-6575` |
| `pipeline_runs` (exempt) | 6 | bot run records; the chain builds none. R2's "5 rows" is now 6 |
| all others | — | identical. `data_migrations` differs only in its ledger provenance, which the check excludes by design |

Every non-NULL value of `journal_abbrev`, `issn`, `pub_month`, `language`, `subtype` and `citation_count` in the whole corpus, and every `author_count_is_complete = 1`, is bot-written. To re-derive: `select count(*) from evidence_sources where journal_abbrev is not null`.

## (2) Attribution to bot commits

I extracted the parent blob and the bot blob for each commit with `git show <sha>:data/guidebook.db` and diffed them by primary key (`E-divergence_bot_commit_diffs.txt`).

| commit | when (UTC) | GITHUB_RUN_ID | wrote |
|---|---|---|---|
| `c4c84634` | 2026-09-21 11:20 | 35593474934 | REF-01006: 7 values, 6 authors rewritten, 1 run row |
| `842bb74d` | 2026-09-28 06:06 | 36384796860 | REF-01007: 7 values, 4 authors rewritten (+ORCID), 1 run row |
| `1876a7f8` | 2026-10-05 06:10 | 37271064510 | REF-01009 (7 values) and REF-01011 (6 values), 8 + 6 authors rewritten, 1 run row |
| `d874ba9e` | 2026-10-12 06:09 | 38211139899 | **only** a `pipeline_runs` row. Its "p4=1" is REF-01011 queried again (language is still NULL and CrossRef has none), so nothing changed. `p4_enriched` counts CrossRef answers, not writes, so this repeats every week |

The `pipeline_runs` rows for 2026-08-24 and 2026-09-07 predate this shallow clone's history, which starts on 2026-09-18 (`git rev-parse --is-shallow-repository` = true). Their commits cannot be attributed here. Both rows show zero work.

## (3) Payload backing, and what the writer does

- **`resolve_dois.py` phase 4.** It selects rows that have a DOI, a `source_type` in its list, and any of these columns NULL: `journal_abbrev`, `volume`, `language`, `pages`, `citation_count`. It fetches `api.crossref.org/works/<doi>` and **does not persist the response**. `enrich_from_crossref` then fills only the empty columns:
  - `journal_abbrev` ← `container-title[0]`, the full title rather than an abbreviation, which copies `journal_name` (a rule 5 dual home);
  - `issn` ← `ISSN[0]`;
  - `pub_month` ← date-parts[1], taken from published-print, then published-online, then issued;
  - `language` ← `language`;
  - `subtype` ← `subtype`, or else `type`, which is how `'journal-article'` got there;
  - `citation_count` ← `is-referenced-by-count`, a figure that changes over time.
- **Authors.** When `author_count_is_complete` is 0 or NULL, the row is not corporate-primary, and CrossRef lists person authors, it DELETEs every author row and INSERTs CrossRef's list (family, given and ORCID, with the `orcid.org/` prefix removed). It stamps the run id and sets `author_count_is_complete = 1`, a completeness assertion that no payload field states.
- **Phases 0–3.** These write `verification_*`, `doi` and `pmcid` through `write_verification`. They examined nothing in any recorded run.
- **Payload check.** The research sessions persisted the payloads `9a51a98c7235d28f.json` (batch 19), `265e92157feb3c35.json` (batch 20), `1995c39d5571f3ec.json` and `dfca4e706e2da8b0.json` (batch 21). I derived each column with the bot's own code path. Every one of the 27 values and the ORCID matches its payload, the author names match exactly, and even `citation_count` matched on the day.
- **CLAUDE.md:93** says the bot wrote "with no saved payload". That is true of the bot's own fetch, but not of the values: the same values are on disk from the research sessions.
- **The verifier does not cover these columns.** `retrieval_log --verify-authors` compares only `_BIBLIO_FIELDS` (`volume`, `issue`, `article_number`, `pages`, `pub_year`, `journal_name`, `publisher`) plus the title and authors, so none of the seven columns is verifiable by it. Its verdict for the three sessions is identical before and after the revert. Batch 21's REF-01009 `pages` mis-file was already there and is unrelated.

## (4) The compensating migration

**What I did.**
- Prepared a scratch copy of the blob with `E-tools/prep_scratch.py`. It derives the divergent set by diffing against the rebuild, copies the rebuild's values, stamps rows with `dbcore.upd(session)`, and restores the chain's author rows verbatim (ids and stamps included).
- Captured the delta with `emit_batch_sql.py --allow-delete evidence_source_authors`, which produced 24 DELETE, 4 UPDATE and 24 INSERT statements.
- **Probe of the capture as-is:** emitted it into a copy of the migrations directory and ran `--rebuild`, which failed with `UNIQUE constraint failed: evidence_source_authors.id`.
- Added 24 keyed `DELETE`s of the chain ids before the INSERT block. These do nothing on the blob; on replay they remove rows that the INSERTs then restore identically.
- Emitted the result with `emit_data_migration.py` as `scripts/migrations/data_20261013212204_2026-10-13-r29-compensating-revert.sql` (copy at `$S/rehearsals/E-divergence_compensating_migration.sql`). Applied it with `migrate_db.py --session session_2026-10-13-r29-compensating-revert`.

**Why the verbs could not be used.** All 14 verb probes refused (`correct-source` and `amend-source` × 7 columns). `correct-source --field authors` rewrote REF-01007's authors as ids 259–262, dropped the ORCID, and reported `"corrected": []`. It cannot restore the chain's state.

**Counts.**

| item | count |
|---|---|
| rows and values reverted | 4 rows, 27 values in 7 columns, plus 8 volatile stamps rewritten to the compensating session |
| author rows | 24 bot rows deleted, 24 chain rows restored (this removes 1 payload-backed ORCID) |
| re-entered | 0 |
| could not decide | 0 |

Judgement note: `author_count_is_complete` (4 values) is not a bibliographic fact. Reverting it restores the column default of 0, which is the chain's state and asserts nothing.

**Commits.**

| commit | what | files | lines |
|---|---|---|---|
| `09e26db` | migration plus DB blob | 1 text file | +128 / −0, all migration: 46 comment lines and 76 statements |
| `257f679` | `scripts/regenerate_derived.sh` output (blocking freshness gates) | 7 generated files | +12 / −12 |
| `e9588bc` | tooling: `EXEMPT_TABLES = ("pipeline_runs",)` | 5 | +28 / −27 |

`e9588bc` breaks down as: script 7/6; registry note 11/14; contract criterion 2/2 (**owner merge**); CLAUDE.md 3/2 (**owner merge**); `architecture/meta-scripts-spec.md` item 6, 5/3. There are no code lines beyond the script's one constant and its docstring.

Net over all three commits: +168 / −39 across 13 files. The step **adds more lines than it removes**, and that is almost all the migration.

**Gates** (full `--all` at baseline and after `e9588bc`; `09e26db` measured before regeneration):

| check | baseline | after 09e26db | after 257f679 | after e9588bc |
|---|---|---|---|---|
| migration_reproducibility_deep (adv.) | FAIL | PASS | PASS | PASS (authors no longer exempt) |
| migration_reproducibility (blocking) | PASS | PASS | PASS | PASS |
| pipeline_completeness_fresh (blocking) | PASS | **FAIL** (stale render) | PASS | PASS |
| evidentiary_audit_fresh (blocking) | PASS | **FAIL** | PASS | PASS |
| pipeline_walk_fresh (adv.) | PASS | FAIL | PASS | PASS |
| schema_walkability_fresh (adv.) | FAIL | FAIL | PASS | PASS |
| research_tooling_separation (adv.) | PASS | — | PASS for `31142552..257f679` | FAIL on the combined changeset; **PASS** for `257f679..e9588bc` alone |
| totals | 67 green / 7 none / 11 adv. red | RESULT FAIL (2 blocking) | render battery 5 green / 2 baseline red | 68 green / 7 none / 10 adv. red |
| `--selftest` / `schema_reference_audit` / `build_graph --check` | PASS / PASS / 0 fail, 5 warn | same | same | same |

**`--rebuild` after `e9588bc`.** Identical sets of tables (82), views (21), triggers (1) and indexes (95), and the same `user_version` (101). Every row count is equal except `pipeline_runs` (6 vs 0, exempt; dropped by 1.5). The row diff of `evidence_sources` and `evidence_source_authors` is empty.

## (5) After 1.5, does the divergence stop growing?

**Yes.** Outside migrations, only two scripts write `evidence_sources` or `evidence_source_authors` to the blob:
- `resolve_dois.py`, run by `resolve-dois.yml` (cron Mondays 06:00 UTC, next run 2026-10-19);
- `verify_urls.py`, run by `verify-urls.yml` (1st and 15th at 06:00, next run 2026-10-15). It only touches rows with `verification_status IS NULL` and a URL. There are none today, so it is dormant, but a future admission without a status would wake it.

1.5 deletes both. Nothing else writes to the blob:
- `db.py` refuses the canonical path in `dbcore.connect` (`is_canonical`, resolved, dry-run included);
- `regenerate-derived.yml` (push and cron) commits only generated files;
- hooks do not open the DB read-write (`research_batch_dod.py` opens with `mode=ro`);
- the remaining hits are selftest fixtures on temporary databases.

The one residual route is an ad hoc read-write open of `data/guidebook.db`, which only the deep check sees, and that check stays advisory until OD-9.

**Until 1.5 lands:**
- REF-01011 gets a new `pipeline_runs` row every week;
- any new `journal_article` with a DOI is enriched within a week. Phase 4 only selects rows whose `source_type` is set: the four DOI rows admitted since 2026-09-20 carry one, while the twelve earlier DOI rows are NULL and never selected;
- landing this migration first undoes itself on the next run (simulated).

## Defects found

**In the plan and rulings:**
- Plan 1.5 attributes the red to `c4c8463` alone. It is three bot commits and four rows, and 24 author rewrites are hidden behind the exemption.
- R2's "5 rows" is now 6.
- R29's re-entry clause names `--verify-authors` as if it were a writer, which it is not.
- Neither the plan nor R29 states the ordering (1.5 → data PR → exemption PR → OD-9), or that RC6 forces the data and tooling into separate PRs.
- workplan 2026-09-23 calls the REF-01006 author rows "byte-identical before and after". The names are identical; the ids and stamps are not.

**Incidental:**
- `correct-source --field authors` deletes and re-inserts rows even when nothing changed, drops `orcid`, and reports nothing.
- `correct-source --help` lists 7 fields while `_CORRECTABLE` has 9 (`journal_name` and `publisher` are missing): a hand-typed list (rule 8).
- `emit_data_migration.RISKY_PATTERNS` does not match quoted identifiers, which is the form `emit_batch_sql` emits, so `DELETE FROM "t";` passes with no warning.
- `migration_reproducibility.py --selftest` fails at base ("missing tables are skipped, not fatal"). It asserts behaviour removed on 2026-08-28 and is in no registry entry, so nothing reports it.
- The registry note "7 today: schema_version + six table COUNT(*)s" is stale: the script now prints EXAMINED: 82.
- REF-01011's `journal_name` carries the HTML entity `&amp;` copied verbatim from the CrossRef deposit (outside R29).
- `sqlite_sequence` for the authors table reads 258 on the blob and 244 on the chain. That is harmless, because data migrations carry explicit ids.

## Residual risk

- The migration's stamps (`2026-10-13 21:21`, the session id) are rehearsal values. **Re-derive at execution; do not copy the file.**
- `verify-urls.yml` fires on 2026-10-15 before 1.5 can land. It is dormant today [UNVERIFIED that no admission with a NULL status lands before then].
- OD-9 (deep as the sole blocking gate) was **not executed**. Callers to sweep:
  - the two registry entries;
  - CLAUDE.md:88–96;
  - `governance/migration-based-writes-adopted-2026-05-11.md:29,75–90`;
  - the contract criterion;
  - `run_checks.py:749`;
  - `readonly_db_open_audit.py:15`;
  - `architecture/meta-scripts-spec.md:346,563,583` (line numbers at base);
  - `dbcore.py:976`.

## What the v4 plan must say

**1.5b — R29 compensating migration (data-only PR; only after 1.5 has merged).** Rebuild and row-diff the blob against the chain. On a scratch copy, set every divergent row to the chain's values, read from the rebuild and never typed, and stamp the `evidence_sources` rows with the session. Capture with `emit_batch_sql.py --allow-delete evidence_source_authors`, then put one keyed `DELETE` per restored author id ahead of the INSERT block, because without it `--rebuild` fails on `evidence_source_authors.id`. Emit, apply, and run `scripts/regenerate_derived.sh` unless 1.1 has landed. Nothing is re-entered: no verb writes the seven columns and nothing that reaches the book reads them. A wanted value is a Phase 5 tooling change to `retrieval_log._BIBLIO_FIELDS` first. Proof: the deep check passes, and `--rebuild` matches on every table, view and row count except `pipeline_runs`. Counts: derive them with `python3 scripts/audit/migration_reproducibility.py --deep` and a row diff; do not quote them.

**1.5c — tooling PR after 1.5b.** Remove `evidence_source_authors` from `EXEMPT_TABLES`. Same-PR edits:
- the script docstring;
- the `migration_reproducibility_deep` note;
- the `reproducibility-invariant` criterion (owner merge);
- CLAUDE.md rule-3 sentence "both author and run tables sit in its EXEMPT_TABLES" (owner merge);
- `architecture/meta-scripts-spec.md` item 6.

Then OD-9.

**R29 text.**
- Replace "re-enters through `amend-source`/`--verify-authors`" with "re-enters through `correct-source` from a persisted payload once the column is in `retrieval_log.PAYLOAD_FIELDS` (tooling first, rule 10)".
- Replace the OVERTURN clause with: "a divergent value shown to be payload-backed, read by something that reaches the book, and writable by no verb".
- Correct the premise "the divergence set is the plan's statement" to: three bot commits, four rows, 27 values, and 24 author rows behind the exemption.
