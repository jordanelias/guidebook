**VERDICT: 29 of 32 spot-checks reproduce. 3 of those needed a correction, and 1 (P4) reproduces only in part. 2 were not re-run and 1 is already fixed (ledger §1). They reduce to four defects in the repo: (1) writers outside the §4 write path; (2) identifiers that can be reissued; (3) gates that check a thing exists rather than that it happened correctly; and (4) a harness loop that burns tokens. Each has a fix that needs no owner decision. Five items are owner-gated. Two are on the §8 doctrine list (ICF-mandatory lens, R1 exceptions). The other three are formally §8 code, but a note, a DR or repo-admin authority reserves them (deep-reproducibility route, D-0184 re-key, the GitHub ruleset). Of the 76 registered checks, delete 7, demote 3, promote 2, repair 9 and fold 1 into an existing check.**

Perspective: GRANULAR (finding by finding). Read-only.
- **No suites run.** Each finding was spot-verified with one read-only command against `file:data/guidebook.db?mode=ro`, the git tree, or the audits' cached `gh/prs.json`.
- **HEAD** = `250bd5a` (`git log -1 --format=%h`).
- **Live `user_version`** = 95 (`PRAGMA user_version`).
- **Status keys:** **V** = VERIFIED, **NR** = NOT REPRODUCED, **U** = UNVERIFIED, **V\*** = verified with a correction.

---

## 1. Verification ledger

| ID | Claim (source) | Command (one each) | Status |
|---|---|---|---|
| A1 | The bot commit `c4c8463` rewrote REF-01006 and deleted and re-inserted its authors (arch F1) | Per-column diff of `git show c4c8463^:data/guidebook.db` vs `c4c8463`. Result: 9 fields changed, incl. `author_count_is_complete` 0→1, `issn`, `pub_month`. Author rowids moved from 182–187 to 188–193. | **V\*** — the author **content is byte-identical** (same 6 names, same order). The substantive change is the completeness *assertion* plus 7 Crossref fills. The writer is `scripts/resolve_dois.py:552-573` (DELETE, then INSERT, then `author_count_is_complete = 1`). `grep -c retrieval_log scripts/resolve_dois.py` returns 0, so no payload artefact is kept. |
| A2 | `icf_code REFERENCES axes` in 065/071/073/074/076, reversed by 081 (arch F2) | `grep -n 'REFERENCES axes' scripts/migrations/0{65..99}_*.sql` | **V** (historical). Live: no `icf_code` FK into `axes`. The residual is that `axes` (17 rows), `population_axis_map` (53) and `access_need_axis_map` (21) are still live, and the blocking gate `validate_axes` guards them. |
| A3 | `specifications.functional_basis` copies `population_icf_links`; `determination_gates.trigger_tier`/`trigger_evidence_type` copy evidence (arch F3) | `select functional_basis from specifications …` vs `pragma table_info(population_icf_links)` | **V**. The JSON keys match the `population_icf_links` columns (icf_code, mechanism, mapping_confidence, provenance) word for word. |
| A4 | `item_taxonomy_links` is keyed on `item_code` and UNWRITABLE (arch F4) | CLAUDE.md §4 snippet | **V** |
| A5a | `schemas/bpc_metadata.py` fails to import (arch F5) | `python3 -c "import schemas.bpc_metadata"` → PydanticUserError, `decorator-missing-field` | **V**. Line 78 is `@field_validator("last_updated")`. The live `bpc_metadata` table has `updated_at`, not `last_updated`. |
| A5b | `scripts/db.py:90` `_BPC_META_COLS` still whitelists `last_updated` | `sed -n 88,92p scripts/db.py` | **V** |
| A5c | Registry `:802` claims "(232 today)" and counts the dropped `item_axis_links` | `sed -n 798,806p governance/check-registry.yaml` (this is `validate_axes`) | **V** |
| A5d | `rename_insurance.py` executes every view and is unregistered | `git grep -n rename_insurance -- governance scripts .github` finds only the script and migration comments | **V**. Today all 21 views execute (a read-only probe found 0 broken), so there is **no live breakage**, only no guard. |
| A6 | The 09-13 clear hand-DELETEd from 17 tables (arch F6) | `grep -oiE '^\s*DELETE FROM\s+"?[a-z_]+' data_20260913040739*.sql \| sort -u \| wc -l` | **V** (17) |
| A7 | Every determination and extraction is MOB-only; 0 adjudications; 0 live determinations (arch F7) | `select identity_code,count(*),sum(icf_code is not null),sum(retired_at is not null) from specifications group by 1` → `('MOB',8,0,8)`. Extractions: `('MOB',48,0)`. `term_adjudications` 0, `observed_terms` 57. | **V** |
| A8 | Hand `INSERT INTO gaps` although `add-gap` existed; `decisions` has no CLI verb (arch F8) | `grep -c 'INSERT INTO gaps'` on both files returns 1 each. `git show ce33ef6^1:scripts/db.py \| grep -c '"add-gap"'` returns 2. `grep -nE '"(add-decision\|record-decision\|decision)"' scripts/db.py` returns nothing. | **V** |
| A9 | `base_parameters` model drift; `MODEL_TABLE_MAP` is curated (arch F9) | `git grep -ln accessibility_direction -- schemas/` returns nothing | **V** |
| A10 | 19 UNWRITABLE FK columns across 18 tables (arch F10) | CLAUDE.md §4 snippet, counted | **V** (19 columns, 18 tables). 10 of the 19 are `item_code` into the emptied `items`. |
| A11 | `specifications.value_notations` and S01 parity (arch F11) | Not re-run | **U** (the audit already judges it minor/keep) |
| P1 | `exec_id` was reissued after the clear; R8 is blind; `_INT_KEYS` covers 2 tables (protocol F1) | `select max(exec_id),count(*) from search_executions` → (91,91). `sqlite_sequence` has no `search_executions` entry. `identifier_floor_audit.py:62-69` covers 2 keys. `research_batch_dod.py:455-463` tests only `mx > cnt`. | **V** |
| P1b | `search_candidates.candidate_id` may also have been reissued (protocol F1, marked [UNVERIFIED] there) | `git grep -hoiE 'INSERT INTO "?search_candidates"?…VALUES\s*\(\s*[0-9]+' -- 'scripts/migrations/data_*' \| grep -oE '[0-9]+$' \| sort -n \| uniq -d` | **V: now confirmed.** Ids 61, 62, … were issued twice across committed migrations. Of the 17 tables the clear touched, four hold an INTEGER PRIMARY KEY with no AUTOINCREMENT (derived from `pragma table_info` plus `sqlite_sequence`): `search_executions`, `search_candidates`, `observed_terms`, `term_adjudications`. `search_admissions` inherits `exec_id`. |
| P2 | 7 of 12 T1–T2 anchors have `forward=0`, no deferral, and are marked `mined` (protocol F2) | `select count(*) from citation_mining cm join evidence_sources es on es.ref_id=cm.global_ref_id where es.tier<=2 and cm.forward=0 and cm.deferred_reason is null` → 7. `… where tier<=2` → 12. | **V**. Also found: `evidence_sources.citation_mining_status` is a **second home** for a `citation_mining` fact. A parity test (test_db_integrity C08, cited at `scripts/db.py:328`) holds the two together. Status 'mined' ignores direction. This is rule 5. |
| P3 | The adversarial pass was absent on 5 data PRs and no gate checks it (protocol F3) | `independent_reviewer_counterclaim` in `attestations/sessions_…batch-09….json` reads "A reviewer should press hardest on…" | **V**. The field is required by `schemas/attestation.schema.json`, but it is **self-authored**. The gate accepts the author's own steelman as an "independent reviewer". |
| P4 | 0 GitHub reviews; #149/#151 merged with `Classify change` failing; ruleset disabled (protocol F4) | `gh/prs.json`: the sum of `reviews` is 0; failing checks on #149/#151 = `Classify change … failure` | **V** for reviews and red merges. **U** for "0 review threads": the cached `threads` field is a GraphQL-unavailable error string, not data. **U** for the ruleset: not re-fetched. |
| P5 | Queries were logged after screening in batches 15/16 (protocol F5) | Not re-run | **U** (the audit gives commit/time evidence; the gate fix below does not depend on it) |
| P6 | R1 order was inverted in batches 10/18/19 (protocol F6) | `select target_evidence_type … where created_by_session=? order by exec_id` → b10 `code,code,code,co1`; b18 co1 at position 9 of 10; b19 co1 last | **V**. `governance/research-contract.yaml:62-64` says "FIRST — no exceptions". |
| P8 | The stop-hook loop; the fix is per-container (protocol F8, tokens class 2) | `grep -c stophook.ignorePath ~/.claude/stop-hook-git-check.sh` → 0. `git config --get stophook.ignorePath` exits 1. | **V**: **the fix is not applied in this very container.** The project `Stop` hook (`.claude/settings.json:63-71`) also runs `research_batch_dod.py --all` on every turn. |
| P10 | Skills target the deleted item layer | `grep -c item_code skills/<s>_SKILL.md`: item-audit-pipeline 28, audit-consolidator 14, functional-deficit-auditor 9, economics-auditor 6, question-author 3 | **V\*** (28 lines, not 30 occurrences). `items` = 0 and `item_audit_runs` = 0. |
| P11 | The commit-msg job is push-only, depth 2 | `sed -n 253-266p .github/workflows/ci.yml` | **V** |
| T1 | CLAUDE.md is 34.6KB and carries 10 correction histories (claudemd 5) | `wc -c CLAUDE.md` → 34607. `grep -o 'until 20' CLAUDE.md \| wc -l` → **9** | **V\*** (9, not 10) |
| C1 | §6 says `base_parameters` is "still-empty" | `select count(*) from base_parameters` → 1. Offending line: `grep -n still-empty CLAUDE.md` → 364. | **V** |
| C2 | §4 and rule 8 name `dbcore.WRITABLE_TABLES` in the present tense | `grep -n WRITABLE_TABLES scripts/dbcore.py` → 783 ("GONE, deliberately"). `CLAUDE.md:240` still says "keeps going blind". | **V** |
| C3 | The §4 locator `db.py:3978-3999` is stale | The refusal is at `scripts/db.py:7063-7076` (`grep -n 'year.*journal' scripts/db.py`) | **V** |
| C4 | "four dashboards ~579KB" | `ls tools/*.html \| wc -l` → 7. `du -ch tools/*.html \| tail -1` → 4.1M. | **V** |
| C6 | CLAUDE.md never names `.claude/agents` or the workflow commands | `ls .claude/agents .claude/commands` → antagonist, db-census, repo-sweep; adversarial, batch-done, orient, session-open | **V** |
| X1 | `test_db_integrity` L04 fires by calendar (protocol §3) | `git show e17f829 -- scripts/tests/test_db_integrity.py` | **NR as live**: already fixed in `e17f829` (2026-09-18). Not carried forward. |
| X2 | `site_pages_fresh` is red by construction | Registry note: "page count built from `items` (93 today)". `items` = 0. | **V**. Its subject was deleted on 2026-09-01. |

---

## 2. Fixes, finding by finding

**Key.**
- **Size:** S < ½ day, M ≤ 2 days, L > 2 days.
- **Owner:** "no" means §8 code or process. "YES" means content or doctrine per §8, or reserved by a specific ratified record.
- **Dep:** the fix that must land first.

All DB changes follow the §4 write path. A schema change is a new `scripts/migrations/NNN_*.sql` plus a `user_version` bump plus the Pydantic mirror, then `migrate_db.py --rebuild` verification. A data change goes scratch copy → `db.py` → `emit_batch_sql.py` → `emit_data_migration.py` → `migrate_db.py`.

### G1: scheduled bots write the DB outside the write path (A1; arch F1) [MAJOR]

**Fix:**
1. `.github/workflows/resolve-dois.yml:59-115` and `verify-urls.yml:63-110`:
   - Stop running against `data/guidebook.db` and stop `git add data/guidebook.db`.
   - Instead: `cp` to a runner scratch, set `GUIDEBOOK_DB_PATH=<scratch>` on the script call, then `emit_batch_sql.py --scratch` → `emit_data_migration.py` → `migrate_db.py`, and commit the migration file together with the blob.
   - This removes the binary-conflict trap in CLAUDE.md rule 3, because every change becomes a text migration.
2. `scripts/resolve_dois.py:557` (DELETE then re-INSERT authors):
   - `emit_batch_sql` refuses deletions by design (its header, lines 17-20), so the author refresh must become an UPDATE-by-position plus an INSERT of the tail.
   - Better: only write when the Crossref list *differs* from the stored one. In `c4c8463` the lists were identical and the rewrite was pure churn.
3. `resolve_dois.py:570-573`:
   - Stop writing `author_count_is_complete = 1` from Crossref. It is a curation assertion that §5(c) protects, and Crossref lists truncate.
   - Alternatively, persist the Crossref payload through `scripts/research/retrieval_log.py` before writing, so `--verify-authors` has an artefact.
4. Delete `evidence_source_authors` from `EXEMPT_TABLES` (`scripts/audit/migration_reproducibility.py:72`) once step 1 lands. `pipeline_runs` stays exempt only if the job still writes it outside a migration; better to capture it too and empty the tuple.
5. Correct CLAUDE.md rule 3's bot paragraph (see §4).

**Size / owner / dep:**
- **Size:** M.
- **Owner:** the `migration_reproducibility_deep` note (`governance/check-registry.yaml:353-365`) reserves "widen the exemption vs require migrations" as an owner call. §8 classes this as code, but a ratified record reserves it, so **ask once, recommending "require migrations"**. Steps 2–3 need no owner call.
- **Dep:** none.

### G2: `icf_code → axes` legacy; the `axes` vocabulary is still live (A2; arch F2)

The FK reversal is done (081). What remains:
1. Retire `axes`, `population_axis_map` and `access_need_axis_map` under the 2026-08-18 ruling. Rule 0 applies: the ruling binds on contact.
2. Callers: `git grep -lw axes -- scripts skills .claude schemas | grep -v migrations/ | wc -l` → 18 files; each map table has 1 caller.
3. Sequence: writer-retire, reader-retire, then drop (views: none reference `axis`).
4. Delete the `validate_axes` check with it.
5. Add `AFTER_DATA` markers? No. The 158-FK-violation warning on rebuild is historical order, not a live defect. Record it in 081's successor header, not in a new check.

- **Size:** M. **Owner:** no for code. Confirm that `population_axis_map`'s 53 rows have their content re-homed in `population_icf_links` before the drop; that is a population-taxonomy content question, so **YES, content check only**.
- **Dep:** G14.

### G3: rule-5 copies in 080 (A3; arch F3) [MAJOR]

1. `specifications.functional_basis`:
   - Committed data migrations INSERT it (`git grep -l functional_basis -- 'scripts/migrations/data_*' | wc -l` → 8), so **it cannot be dropped**.
   - New migration: create `specification_icf_basis(specification_id REFERENCES specifications, link_id REFERENCES population_icf_links, PRIMARY KEY(both))`.
   - Writer-retire in `scripts/assess/assess_cell.py`. Reader-retire in `scripts/audit/derivation_handshake_integrity.py` and `scripts/tests/test_assess_cell_pilot.py`. NULL the column forward.
2. `determination_gates.trigger_tier` / `trigger_evidence_type` (NOT NULL):
   - 1 committed data migration INSERTs `trigger_tier`, so it cannot be dropped.
   - Rebuild the table to relax NOT NULL (1 row), and derive the tier through a view: `evidence_sources` joined on `trigger_ref_id`, tier from `derive_tier`.
   - Writer-retire in `db.py`/`assess_cell.py`, reader-retire in `derivation_handshake_integrity.py`, NULL forward.
   - DR-2026-07-13's "gate rows carry the tier" is satisfied by the pointer; record that in the migration header.
3. **Add no parity check** (rule 5).

- **Size:** M. **Owner:** no. **Dep:** none.

### G4: dead item-keyed and unwritable tables (A4, A10; arch F4, F10) [MAJOR]

- **Delete** (§8 needs evidence, not permission). The evidence: 0 rows, unwritable, no view reads them. Tables and non-migration callers (`git grep -lw <t> -- scripts .claude skills schemas governance/check-registry.yaml`):

  | Table | Callers |
  |---|---|
  | `room_items` | 0 |
  | `economics_entry_specs` | 0 |
  | `case_study_populations` | 0 |
  | `case_study_strategies` | 0 |
  | `case_study_specs` | 1 |
  | `case_study_outcomes` | 1 |
  | `item_population_elaborations` | 1 |
  | `term_item_links` | 2 |
  | `item_bpc_links` | 4 |
  | `item_audit_runs` | 6 |
  | `jurisdictional_values` | 7 |
  | `item_taxonomy_links` | 12 |
  | `spec_value_probes` | 14, plus 1 view |

  - Sweep the callers, `sqlite_master` and the skills (rule 4), then DROP in one migration.
  - `spec_value_probes` also takes down the `pmp_audit` check (below) and `probe_population_links`.
- **`icf_medical_map` / `identity_medical_map`:** keep. The owner has explicitly left them blocked on medical-lens content (074 header). They are unwritable *by design* until `base_taxonomy_medical` is populated. **Owner:** YES (content already pending).
- **`citation_population_links`, `connection_targets`:** investigate their parents (`citation_id`, `con_id`, both emptied). Delete if they share the item-era fate.
- **D-0184's object** (`item_taxonomy_links`): delete the table. Re-keying D-0184's crossing onto `parameter_id` is new content design, so **YES**, but it does not block the delete; the 2026-08-26 ruling already binds.
- **Size:** M (the sweep is the cost). **Dep:** G7 (the view probe) first, so the drop is proven safe.

### G5: rename sweep misses from 085 (A5a–c; arch F5) [MAJOR, and the cheapest]

1. `schemas/bpc_metadata.py:78`: `"last_updated"` → `"updated_at"`. Confirm the field name matches line 32's edit.
2. `scripts/db.py:90`: drop `"last_updated"` from `_BPC_META_COLS`. Check whether `updated_at` belongs in the whitelist or is stamped automatically.
3. `governance/check-registry.yaml:802`:
   - Replace "(232 today)" with the command. Rule 7a: `python3 -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(sum(c.execute(f'select count(*) from {t}').fetchone()[0] for t in ('population_axis_map','access_need_axis_map')))"`.
   - Or delete the entry with G2.

- **Size:** S. **Owner:** no. **Dep:** none. **Do first.**

### G6: bulk hand-DELETE retractions (A6; arch F6)

1. Both owner-ruled clears were hand SQL. Add a `db.py retract-slug --slug --ruling <ref>` verb that retire-in-places rows. The 083 pattern (`retired_at`, `retired_by_session`, `retirement_reason`) already exists on `specifications`.
   - For the research-stage tables (`search_executions`, `search_candidates`, `citation_mining`) add the same three columns. **Never DELETE**: R8 says the log is append-only.
2. Readers must filter `retired_at IS NULL`. This touches every reader of those tables, so rule 4 applies.

- **Size:** L. **Owner:** no. The *content* of any future clear is owner-ruled, but the mechanism is not.
- **Dep:** G8 (identifiers must be unreissuable before any further retraction).

### G7: no execution probe over views (A5d; arch F5)

1. Fold `rename_insurance.py`'s view loop (lines 74-78: `SELECT COUNT(*)` per view, catching `sqlite3.Error`) into the **existing blocking** `schema_reference_audit`, as "every view executes". `EXAMINED` = the view count.
   - **Book defect it prevents:** the 063→064 and 071→072 breaks, where `v_item_provenance` failed and a provenance surface rendered empty. Two real incidents (072's header records `run_checks --all` "PASS … over three broken objects").
2. Do not register `rename_insurance.py` itself. It is a one-shot rename proof, invoked per migration.

- **Size:** S. **Owner:** no. **Dep:** none.

### G8: identifiers are reissuable (P1, P1b; protocol F1) [CRITICAL]

1. **New schema migration** that rebuilds `search_executions`, `search_candidates`, `observed_terms` and `term_adjudications` with `INTEGER PRIMARY KEY AUTOINCREMENT`.
   - Seed `sqlite_sequence` to the **historical** high-water, derived as the max id ever INSERTed across `scripts/migrations/data_*` (the regex `identifier_floor_audit.py` already uses), **not** as `max()` of the live rows.
   - `search_admissions` is keyed on `exec_id`, so it follows.
   - The 076 pattern applies directly.
2. **Rule 8:** replace the curated `_INT_KEYS` (`scripts/audit/identifier_floor_audit.py:62-69`) with a derivation. Every table whose single PK is `INTEGER` gets a regex built from its name and PK column. The burden moves to exclusions.
3. **R8 gate** (`scripts/audit/research_batch_dod.py:455-463`):
   - Replace `mx > cnt` with `count < sqlite_sequence.seq` for `search_executions`, which step 1 makes meaningful.
   - Or call `identifier_floor_audit`'s high-water function directly.
4. **Permanent records now point at wrong rows:**
   - `sessions/…batch-05….md:85` (exec 34) and `sessions/…batch-07….md:39,91` (exec 47, 44). `sessions/` is frozen.
   - Append an erratum to `references/project-standards.md`, or a new session record, mapping "batch-05/07 exec N = deleted row, now reissued to batch 08–10". Needs an attestation (rule 2).
   - The deleted rows' content is recoverable from `data_*batch-0[5-7]*.sql`.
   - Also correct migration `data_20260913040739`'s "compensating, append-only" claim in the erratum. Migrations are immutable, so fix forward.

- **Size:** M. **Owner:** no. **Dep:** none. **Blocks** G6 and every future batch.

### G9: forward mining absent; `citation_mining_status` is a dual home (P2; protocol F2) [HIGH]

1. **Content:** run forward mining for the 7 anchors (REF-00979, 00980, 00983–00986, 01006) through the `citation-miner` skill in its forward mode, or record `--deferred-reason` per the GAP-022 ruling ("deferred is okay so long as it runs eventually").
2. **Gate R2** (`research_batch_dod.py:320-340`): require, per tier ≤ 2 anchor, a row with `backward=1 AND forward=1`, or a non-NULL `deferred_reason`. Count per anchor, not rows per batch. One SQL change.
3. **Rule 5:** `evidence_sources.citation_mining_status` restates `citation_mining`.
   - Grep `scripts/migrations/data_*` for it first. If it is inserted there, it cannot be dropped: writer-retire in `db.py:~400` and `log_mining`, reader-retire (5 files: `git grep -l citation_mining_status -- scripts | wc -l`), NULL forward.
   - Add a view `v_source_mining_status` that derives `mined` only when both directions are present.
   - Then delete test_db_integrity C08, the parity check, per rule 5.

- **Size:** step 1 M (research work), step 2 S, step 3 M. **Owner:** no. **Dep:** step 2 before step 1, so the re-run is gated.

### G10: the adversarial pass is unenforced (P3; protocol F3) [HIGH]

1. **Schema:** make `independent_reviewer_counterclaim` an object `{reviewer_transcript, verdict_excerpt}` in `schemas/attestation.schema.json` (bump `schema_version`).
   - `reviewer_transcript` must resolve to `transcripts/harness_*/subagents/*.jsonl`, and the first prompt must come from an `antagonist` or `adversarial` role.
   - Keep the self-authored steelman as a separate `author_steelman` field. It has value; it just is not independent.
2. **Trigger:** extend the attestation path regex (`scripts/audit/adherence_log_audit.py:82`) to include `scripts/migrations/data_*.sql`. DR-2026-08-19 §7 binds the pass to data diffs, and today only `sessions/` catches batch PRs.
3. **Gate:** `attestation_evidence` (advisory) checks the transcript pointer. **Promote to blocking** after one batch proves it.
4. Direct antagonist runs to the `antagonist` project agent (`.claude/agents/antagonist.md`), not general-purpose (tokens §3: 7 of 23 runs used it).

- **Size:** M. **Owner:** no (enforces a ratified DR). **Dep:** none.

### G11: GitHub merge gating (P4; protocol F4) [HIGH]

1. Enable ruleset 19136391 with `required_status_checks` covering the blocking batteries. **Owner: YES.** This is repo admin, not a code change the agent can make.
2. `Classify change` failed in 1–2 s on runner allocation (#149, #151). Add `retry` or `continue-on-error: false` with a single re-run step in `ci.yml`'s classify job, so a red means the diff. **S, no.**
3. No agent merges a PR whose head suite is still in progress. Put this in CLAUDE.md §7 (text in §4 below). **S, no.**

### G12: R1 order and R8 timing gates (P5, P6; protocol F5, F6) [MEDIUM]

1. **R1** (`research_batch_dod.py:290-317`): add `min(exec_id) where target_evidence_type in ('co1','t2','co2') < min(exec_id) where target_evidence_type not in (…)` per session.
   - **Owner: YES**, whether chain-following batches (18: archive route; 19: pre-1990 chain) are an exception. `research-contract.yaml:64` says "no exceptions" and cites CRPD 4.3, which is doctrine.
2. **R8 timing:**
   - `search_executions.created_at` must precede the `created_at` of every `search_candidates` row from that exec.
   - For batches whose priors are pre-committed in a file, accept a `prior_commit_sha` column whose commit time precedes the exec. That is a new column plus a `log-search` flag.
   - **S–M, no.**

### G13: stop-hook / notification token burn (P8; tokens classes 1–2, 1.03B tokens combined per audit_rank) [HIGH by cost]

1. **Repo-side, so it survives new containers:** make the growing files untracked while a session is live.
   - `.claude/hooks/record-command.py` writes to `scratchpad/<s>/commands.live.jsonl` (gitignored).
   - The transcript sync writes nowhere tracked until `scripts/preserve_transcripts.py` runs at a break (rule 6), and that copies both into tracked paths.
   - The tree is then clean between breaks, and the harness hook is satisfiable without `scripts/fix_stop_hook_loop.sh`. The script is blocked for the agent and unapplied here (P8).
   - **M, no.**
2. `.claude/settings.json:63-71`: the project Stop hook runs `research_batch_dod.py --all` on every turn (1,407 runs per audit_tokens). Gate it on `scratchpad/CURRENT` naming a `research-batch-*` session **and** the scratch DB having changed since the last run (compare mtime against a stamp file). **S, no.**
3. **Process:** open the PR once, at the end. Do not `subscribe_pr_activity` until the head is final. Never `send_later` to poll CI. The measured best batch (0e701d1b) did exactly this. CLAUDE.md text in §4. **S, no.**
4. **Context hygiene:** one harness session per batch or per PR. Hand off rather than riding to auto-compaction (all 10 compactions were automatic at 784–786k preTokens). CLAUDE.md text in §4. **S, no.**

### G14: stale skills (P10; tokens §3)

- **Delete** `item-audit-pipeline`, `audit-consolidator` and `item-consolidation-analyzer`. They operate on `items` and `item_audit_runs`, both 0 rows and to be dropped in G4.
- **Rewrite or delete** `functional-deficit-auditor`, `economics-auditor` and `question-author` (item-keyed by definition).
- **Sweep** `connection-discovery`, `cross-population-conflict-mapper`, `evidence-auditor` and `content-gap-analyzer` for item-code examples.
- Git history is the archive; do not move them to `_archived/` (§8).
- Remove the `.claude/skills/<name>` symlinks in the same commit.
- `multilingual-research` stays. `research-contract.yaml:65,191,242` anchors R1, R8 and R11 on it.
- **Size:** M. **Owner:** no (§8: code and apparatus). **Dep:** G4.

### G15: `decisions` has no CLI verb; hand `gaps` inserts (A8; arch F8)

- Add `db.py add-decision` (vocabularies via `dbcore.check_values`). 5 hand-SQL files in the period needed it.
- The `gaps` bypass: no action beyond the rule. The CLI existed and a compensating migration is not warranted. `add-gap`'s refusals simply were not exercised.
- **S, no.**

### G16: Pydantic drift (A9; arch F9)

- Replace the curated `MODEL_TABLE_MAP` in `scripts/audit/validate_pydantic_schemas.py:20` with a derived map: a model declares `__tablename__`, and the validator walks `schemas/*.py`.
- Fix `BaseParameter` (add `accessibility_direction`, `direction_rationale`) and `EvidenceStateRecord` (the columns from 079/080/083/086/087).
- Then the check can discriminate. See the merit table.
- **M, no.** **Dep:** G5.

### G17: determinations built on an umbrella; judgment never crosses terms (A7; arch F7) [MAJOR, content]

1. **Content:** adjudicate the 57 `observed_terms` (Opus-class, at judgment; §6).
   - No new determination may be stated until a spec row carries an `icf_code` or `needs_code`.
   - All 8 current specs are retired, so nothing live is wrong; the defect is the pipeline shape.
2. **Gate:** add a clause to the blocking `validate_evidence_state`: refuse `state IN ('stated','provisional')` where `icf_code IS NULL AND needs_code IS NULL AND medical_code IS NULL`.
   - This **tightens the D-0182 CHECK** ("at least one lens"), so **Owner: YES**.
   - Short of that, make it advisory without owner sign-off.
3. **Judgment DoD:** a batch that writes `observed_terms` must, before a spec is stated, have `term_adjudications` for them.

- **Size:** L (content). **Dep:** G8 (`term_adjudications` becomes AUTOINCREMENT).

### G18: rule 1 commit-format gate is vacuous (P11)

- Delete the `commit-msg` CI job (`ci.yml:253-266`). It guards apparatus, not the book (§8 test); it skipped 42 of 42 PRs; 7 malformed commits reached main.
- Keep rule 1 as text, marked "NOT ENFORCED".
- **S, no.**

---

## 3. Check merit table (every check the audits mention)

**Test:** what wrong thing reaches the *book* without it (§8), whether it has caught a real defect, and whether it is vacuous or red by construction. No check was run to produce this.

**Blocking checks**

| Check | Level now | Verdict | Reason |
|---|---|---|---|
| research_dod_session | blocking | **keep + repair** | Caught 5 unmet rules on batch 06 (7e9b9c8). Blind on R1 order, R2 direction and R8 identity/timing. Fix in G8, G9, G12. |
| research_dod_selftest | blocking | keep | It protects the DoD's own fault injection. |
| migration_reproducibility | blocking | **keep, then merge into deep** | Count-only: an UPDATE is invisible (arch F1). After G1, the deep variant subsumes it. |
| identifier_floor_audit | blocking | **keep + repair** | Caught reissue (6cd99a1). Curated to 2 keys, which is a rule-8 violation (G8). |
| test_db_integrity | blocking | keep; **delete C08 and the H-series parity checks** | Mixed. L04's calendar bug is already fixed (X1). Parity checks make dual homes permanent (rule 5; G9). |
| attestation_presence | blocking | **keep + widen** | Vacuous on non-synthesis diffs (4 PASS / 94 NONE per audit_suites). Widen its scope to `data_*` migrations (G10), which gives it a subject on every batch. |
| attestation_schema | blocking | keep | Cheap. Enforces the counterclaim object after G10. |
| column_vocabulary_audit | blocking | keep | Real vocabulary catches. Note that it does not exercise writers (65de740). |
| derived_not_curated_audit | blocking | keep | Guards rule 8, which is book-relevant through the vocabularies. |
| extraction_relations_integrity | blocking | keep | Judgment-stage shape on live rows. |
| schema_reference_audit | blocking | **keep + extend** | Name-only; it missed 071. Add the view-execution probe (G7). |
| judgment_handoff_shape | blocking | keep | Never red (89 observations), but mutation-tested (registry note) and it pins a 0-row table that rule 4 says to treat as unproven. |
| validate_evidence_state | blocking | keep; fix basis | Its `basis:` still cites `specification/governing-refs-nonempty`. `governing_refs` was retired in #157 and the script now reads the junction (`scripts/validate_evidence_state.py:289-294`). Re-state the basis. |
| claude_md_spine | blocking | **demote to advisory** | Guards CLAUDE.md prose, not the book. Never red. Keep only because it is nearly free. |
| research_contract_sync | blocking | keep | Hook/contract drift feeds every session. Its fragility is the index-0 trap; fix the hook to find its entry by marker, not index. |
| research_contract_baseline_ratchet | blocking | keep | Cheap. Guards the contract text the hook injects. |
| audit_adversarial_use | blocking | **demote to advisory** | Validates a misuse catalogue (`EXAMINED` = vector count), not any diff. Nothing to examine pre-release. |
| validate_axes | blocking | **delete (with G2)** | Guards the vocabulary the owner ruled a bad coined term. Its registry count is stale (A5c). |
| decision_capture | blocking | keep | Non-vacuous (C9 orphan DRs). Pair it with `add-decision` (G15). |
| doctrine_recheck | blocking | keep | Non-vacuous per registry. Low cost. |
| validate_cross_refs | blocking | keep | Structural. Rendered cross-refs reach readers. |
| validate_bpc | blocking | keep | BPC files are synthesis inputs. |
| alias_provenance_audit | blocking | keep | Its subject is term_aliases, whose size the registry records as 2382 (unverified this pass). R11 back-translation guard. |
| check_utf8_md / check_json / check_yaml | blocking | keep | Hygiene, near-zero cost, and they catch the YAML duplicate-key class. |
| jurisdiction_db_vocabulary / validate_jurisdiction | blocking | **merge into one** | The same basis `base/base-jurisdiction-vocabulary`, twice. |
| db_path_env_audit | blocking | keep | Protects the canonical sha during scratch work (§4). |
| source_slug_links_duplicates | blocking | **fold into test_db_integrity** | Vacuous 22 of 30 observations. A single uniqueness constraint in DDL would do it better. |
| pipeline_completeness_fresh / evidentiary_audit_fresh | blocking | **demote to advisory** | Render freshness is red by construction on any data change, and a bot regenerates it. It blocks nothing that is wrong in content. |
| `validate_verification_consistency` | blocking | not assessed | Not mentioned by the audits. |

**Advisory and informational checks**

| Check | Level now | Verdict | Reason |
|---|---|---|---|
| research_dod | advisory | keep (the corpus-wide view) | It is also what the Stop hook runs 1,407×. Scope the hook (G13). |
| author_fidelity | advisory | **promote to blocking** | §5(c) is "the worst failure available here". Caught real retractions (f6e9d4b). Its reds (115 of 122 per audit_suites) need triage first: promote once main is green on it, and fix the Crossref-403/429 handling so a publisher block is not a fail. |
| migration_reproducibility_deep | advisory | **promote to blocking after G1** | The only check that sees the bot rewrite. Red today only because the bots bypass migrations. |
| source_locators_integrity | advisory | keep advisory; **build the writer** | Caught the offset-DOI corruption (5cdbe6f). Red for 10+ days because no repair verb exists. Add `db.py amend-locator`, repair, then promote. |
| attestation_evidence | advisory | **promote after G10** | It becomes the adversarial-pass gate. |
| citation_mining_session | advisory | keep advisory | Demoted in e17f829. Superseded by R2 per anchor (G9). Delete once G9 lands. |
| validate_pydantic_schemas | advisory | **repair (G16), then keep advisory** | Red 288/288 per audit_suites, and 213 findings "informational". Vacuous as a gate while the map is curated. |
| site_pages_fresh | advisory | **delete** | Builds pages from `items` (0 rows). Red 328/328 per audit_suites, by construction since 2026-09-01. |
| context_map_fresh | advisory | keep | The map is the one searchable derived file. Red because nothing regenerates it on data PRs. Add it to `regenerate_derived.sh`'s bot. |
| retired_vocabulary | advisory | **repair or delete** | Red 314/314 per audit_suites. Either fix the 21 flagged surfaces (a registry count; re-derive) or accept that it is the item-layer corpus in `references/`/`working/` and scope it to live surfaces. A red that never clears is rule 6's anti-pattern. |
| test_verification_pipeline | advisory | **repair** | Asserts corpus floors (≥50/≥30/≥100) that an owner ruling cleared (CLAUDE.md rule 7a). Red 302/302 per audit_suites. Remove the floors. |
| metadata_integrity_audit | advisory | **repair the note, then judge** | The note says "0 today (clean-room reset)"; evidence_sources is not empty. Always red (206). Re-baseline on live rows. |
| validate_reasoning | advisory | keep, **fix the red** | The nine-step synthesis contract is book-relevant (PR #56). 3 reasoning docs per its note (re-derive). Red 191/191 per audit_suites means the docs fail it: fix the docs or the rule. |
| research_protocol_audit | advisory | keep | Occasionally green, so it discriminates. Its CHECK 1-9 include the empty `search_languages` (0 rows); drop that clause. |
| validate_schema_cross_check | advisory | **delete** | 5 passes and 101 fails per audit_suites. The registry note records a retirement rationale already. |
| medical_lens_integrity | advisory | keep | Book-relevant (medical lens as frame). Vacuous until medical content exists; the owner has that pending. |
| pmp_audit | advisory | **delete (with G4)** | Its subject `spec_value_probes` is an item-keyed dead table. |
| population_integrity_audit | advisory | **delete (with G4)** | Its subject is 3 junctions, all 0 rows and unwritable. |
| reasoning_doc_citations_audit | advisory | keep advisory | Empty-by-decision. Revisit when synthesis starts. |
| graph_audit / test_graph_audit | advisory | keep | Never red, but cheap. The graph extractor also executes views. |
| gap_mining_audit, claims_docket, matrix_consistency, readonly_db_open_audit, validate_population, audit_evidence_metadata, render_audit_browser, pipeline_contract_audit, validate_parameters, derivation_handshake_integrity | advisory | keep | Never red locally is not proof of no merit. They are cheap and advisory. `derivation_handshake_integrity` must be edited in G3 (it reads the copy columns). |
| schema_walkability_fresh / pipeline_walk_fresh | advisory | keep | Render freshness; advisory is correct. |
| test_record_command_session, test_url_verifier, test_assess_cell_pilot, test_evidence_cell_state_2_3, test_validate_evidence_state_2_4, test_directness_2_2, test_pipeline_contract | advisory | keep | Regression cover for scripts. `test_assess_cell_pilot` must follow G3. |
| claude_skills_loadable | advisory | keep | Its absence cost 17 days of unloadable skills (fixed by ce39a07). Never observed run; verify it is wired. |
| citation_mining_backlog_t2 / attestation_verdict | informational | keep | Informational by design. |

**Not in the registry**

| Check | Level now | Verdict | Reason |
|---|---|---|---|
| rename_insurance.py | unregistered | **do not register; fold its view loop into schema_reference_audit** | See G7. |
| CI `commit-msg` job | CI only | **delete** | See G18. |
| CI `Classify change` | CI only | **repair** | Runner-allocation reds (G11). |

**Net:**
- **Delete (7):** validate_axes, site_pages_fresh, validate_schema_cross_check, pmp_audit, population_integrity_audit, the `commit-msg` job, and citation_mining_session after G9.
- **Demote (3):** claude_md_spine and audit_adversarial_use; the two blocking `*_fresh` checks count as one render pair.
- **Promote (2):** author_fidelity and migration_reproducibility_deep, plus attestation_evidence after G10.
- **Merge or fold (3):** the jurisdiction pair; source_slug_links_duplicates; rename_insurance's view loop.
- **Repair (9):** research_dod_session, identifier_floor_audit, schema_reference_audit, attestation_presence, validate_evidence_state's basis, validate_pydantic_schemas, test_verification_pipeline, metadata_integrity_audit, retired_vocabulary.

The registry notes carry more "N today" figures that are now false: `site_pages_fresh` "93", `validate_axes` "232", `metadata_integrity_audit` "0", and the three "(clean-room reset)" notes. `grep -c ' today' governance/check-registry.yaml` gives the scale. Rule 7a: replace each with its command in the same pass as the verdicts above.

---

## 4. CLAUDE.md edits

| Where | Edit |
|---|---|
| §2 rule 3, bot paragraph | Name **both** out-of-path writers. `resolve-dois.yml` rewrites `evidence_sources` and `evidence_source_authors` (bot commit `c4c8463`: REF-01006 `author_count_is_complete` 0→1 with no payload); it is not only `pipeline_runs`. After G1, replace the whole paragraph with "bots write through migrations". |
| §4 "`dbcore.WRITABLE_TABLES` keeps going blind" (line 240) | Past tense: "was a curated list, now `dbcore.writable_tables(conn)`". Rule 8's proof already says so. |
| §4 locator `scripts/db.py:3978-3999` | Replace with `grep -n "year.*journal" scripts/db.py` (a command, not a line number; rule 7a). |
| §4 unwritable paragraph and §6 "still-empty `base_parameters`" (line 364) | Delete the claim. `base_parameters` holds rows and every `specifications` row is retired. Keep only "run the derivation". |
| §7 "four rendered dashboards ~579KB" | Replace with `ls tools/*.html \| wc -l; du -ch tools/*.html \| tail -1`. |
| §2 "this session's nine defects", §5(a) "four separate times" | Unanchored counts. Delete the numbers, or anchor them to a record. |
| §7 stop-hook trap | Replace the pointer to `scripts/fix_stop_hook_loop.sh` (the agent cannot run it; it is unapplied in this container) with the G13-1 mechanism once built. Until then: "a human runs it once per container". |
| New §7 bullet: **PR lifecycle** | "Open the PR when the work is done, not at the start. Do not subscribe or poll until the head is final. Never merge while the head suite is in progress. One harness session per batch or PR: hand off, don't ride to auto-compaction." Cost evidence: `audit_tokens.md` classes 1–3. |
| New §9 row: **project agents and commands** | Name `.claude/agents/{antagonist,db-census,repo-sweep}.md` and `.claude/commands/{orient,session-open,batch-done,adversarial}.md`, and state that the adversarial pass uses `antagonist`. |
| Correction histories (`grep -o 'until 20' CLAUDE.md \| wc -l` → 9) | Move them out. The brief says "process, workflow and rules only", and the histories are in git. Keep at most one worked example per rule. This also cuts part of the 34,607-byte (`wc -c CLAUDE.md`) per-call floor. |
| §2 rule 8 "24 of them derived" | Already stale: arch F9 measured 25. Remove the figure; the command is beside it. |

---

## 5. Dependency order

| Phase | Items | Owner |
|---|---|---|
| **1 (days, S)** | G5 (bpc_metadata import) · G7 (view probe) · G13-2/3/4 (Stop hook scoping, PR lifecycle, context) · G18 · G11-2/3 · G15 · CLAUDE.md §4 table | none |
| **2 (M)** | G8 (AUTOINCREMENT plus derived `_INT_KEYS` plus R8) → G9-2 (R2 per anchor) → G12-2 (R8 timing) · G10 (counterclaim pointer plus data-path trigger) · G3 (rule-5 copies) · G13-1 (untracked live logs) | none |
| **3 (M)** | G1 (bots through migrations) → promote `migration_reproducibility_deep`, retire the count-only gate · author_fidelity triage → promote | G1: ask once (the registry reserves it) |
| **4 (M–L)** | G4 (drop dead tables) → G14 (delete item-layer skills) · G2 (retire `axes`) → delete validate_axes · G16 (derived model map) · G9-3 (derive mining status, delete C08) · G6 (retract verb) | G2 content check; D-0184 re-key |
| **5 (content)** | G9-1 (forward-mine 7 anchors) · G17-1 (adjudicate 57 terms) | none |
| **Owner decisions** | G11-1 (enable ruleset) · G12-1 (R1 exceptions for chain batches?) · G17-2 (make an ICF/needs lens mandatory for stated cells: tightens D-0182) · G1 exemption route · G2/G4 content re-homing | YES |

**Not carried forward:**
- X1: L04 calendar trigger, already fixed in e17f829.
- "0 review threads": the cached data is an error string.
- The GitHub ruleset state: not re-fetched.
- P5 exact log/screen timing: not re-run. The G12-2 gate fix stands on its own.
- The arch "22 fix-keyword data migrations": the audit itself marks it a proxy.

---

## Handshake (granular → holistic)

**Round verdict:** I AMEND all seven R-items and DISAGREE with none. Each amendment is a mechanism detail that the granular spot-checks contradict or add to.

### R-items

| R | Call | One line |
|---|---|---|
| R1 | **AMEND** | Agree on the mechanism. Two corrections. First, the "227M in every fresh clone" benefit is false: gitignoring the files needs `git rm --cached`, and history still carries them (`git count-objects -vH` → size-pack 176.76 MiB), so only the working-tree checkout shrinks. Second, `preserve_transcripts.py --check` must read the provenance branch, or rule 6's check goes blind. |
| R2 | **AMEND** | Agree on lifecycle and ruleset. But **`paths-ignore` conflicts with R2's required status checks.** A workflow skipped by path filter leaves its required checks pending, which blocks the merge. Short-circuit inside `classify` instead (see the CI answer below). |
| R3 | **AMEND** | The trim is largely **done in e3846fa**: 34,607 → 32,230 bytes (`git show e3846fa:CLAUDE.md \| wc -c`), and 0 `until 20` (`… \| grep -o 'until 20' \| wc -l`). Three things are still missing: the one-deliverable/handoff norm, the PR lifecycle, and the rule-3 bot paragraph (see e3846fa below). |
| R4 | **AMEND** | Three changes. (a) **Do not register `rename_insurance.py`.** It is `--snapshot` / `--compare BEFORE AFTER --map` (lines 10–11), a per-rename comparator with no standalone subject; fold its view loop (lines 74–78) into the blocking `schema_reference_audit` instead (G7). (b) `_INT_KEYS` must be **derived**, not grown by two (rule 8). It must also cover `observed_terms` and `term_adjudications`: 4 reusable keys among the cleared tables, per `pragma table_info` and `sqlite_sequence`. (c) I accept deleting `claude_md_spine` instead of my demotion. |
| R5 | **AMEND** | Four additions. (a) AUTOINCREMENT on **all four** keys, not only `search_executions`. `candidate_id` reuse is VERIFIED: ids 61 and up were INSERTed twice across `data_*`. (b) Seed `sqlite_sequence` from the historical high-water across migrations, not from `max()` of the live rows. (c) `resolve_dois.py:557` DELETE-then-INSERT will be refused by `emit_batch_sql`, which is additive, so it must update in place. (d) Stop the bot writing `author_count_is_complete=1` (`:570-573`). |
| R6 | **AMEND** | Three changes. (a) The dead-table list is too narrow. The §4 snippet gives 19 UNWRITABLE columns across 18 tables; 13 item-era tables are 0-row and unwritable (G4 list), and `spec_value_probes` carries 14 callers plus 1 view. (b) **Add the retirement of `axes`, `population_axis_map` and `access_need_axis_map`,** and delete `validate_axes` with it (G2). (c) Keep the medical maps pending owner content (074 header); I agree the removal needs an owner YES. |
| R7 | **AMEND** | Two changes. (a) `research-contract.yaml:65,191,242` anchor R1, R8 and R11 on `multilingual-research_SKILL.md`, so retiring its CHECK/LOG must **re-anchor** those three rules. (b) The attestation's `independent_reviewer_counterclaim` is self-authored today (batch-09 attestation: "A reviewer should press…"). Make it a transcript pointer to an `antagonist` subagent, and extend the attestation path regex (`adherence_log_audit.py:82`) to `scripts/migrations/data_*.sql`. |

### G-items mapped to R-items

| G | Serves | Status |
|---|---|---|
| G1 bots through migrations | R5 | open |
| G2 retire `axes` | R6 (added by amendment) | open |
| G3 rule-5 copies | R6 | open |
| G4 dead tables | R6 (widened) | open |
| G5 `bpc_metadata`, `db.py:90`, registry `:802` | R6 | open (not touched by e3846fa, which changed CLAUDE.md only) |
| G6 retract verb | R5 | open |
| G7 view probe | R4 (amended) | open |
| G8 identifiers | R5 + R4 | open |
| G9 steps 2–3 (R2 gate per anchor; derived mining status, delete C08) | R4 and R6 | open |
| G9 step 1 (forward-mine 7 anchors) | **none** | **still needed.** It is content, owed under GAP-022. |
| G10 adversarial pointer | R7 | open |
| G11-1 ruleset, G11-3 no merge mid-suite | R2 | open (owner) |
| G11-2 `Classify` retry | R2 | still needed. R1 removes log-only PRs, but a runner-allocation red can still hit a real head. |
| G12 R1 order / R8 timing | R4 | open (R1 exceptions: owner) |
| G13-1 untracked live logs | R1 | **superseded by R1** (R1 is stronger) |
| G13-2 Stop-hook DoD | R1 | open |
| G13-3/4 PR lifecycle, session scope | R2, R3 | open. **Not in e3846fa.** |
| G14 stale skills | R7 | open |
| G15 `add-decision` | R5 | open |
| G16 derived model map | R4 / R6 | open |
| G17 ICF-lens adjudication | **none** | **still needed** as a content and owner item. I accept holistic point 5 that it is not yet a §6 defect, but the pipeline has run 0 of 57 adjudications. |
| G18 delete `commit-msg` job | R4 | open |

**§4 CLAUDE.md table, marked against e3846fa:**
- **DONE:** `WRITABLE_TABLES` tense (now past tense, line 170), the `3978` locator, "still-empty", "~579KB", "nine defects", "four separate times", the "24 of them" count, correction histories, agents and commands named (lines 42–44), and the suite-frequency rule (lines 26–28).
- **MISSED by e3846fa:**
  1. **Rule 3's bot paragraph (lines 89–91) still says the bot writes only `pipeline_runs`.** VERIFIED false: `c4c8463` rewrote `evidence_sources` REF-01006 (9 fields) and its 6 author rows.
  2. **No PR-lifecycle rule.** `grep -ci 'open the PR\|PR last\|in progress'` on the new file → 0. The only subscription mention is inside the stop-hook bullet (line 408).
  3. **No one-deliverable/handoff norm.**
  4. The stop-hook bullet (lines 402–417) still offers `fix_stop_hook_loop.sh` as the remedy, and it is unapplied in this container (`grep -c stophook.ignorePath ~/.claude/stop-hook-git-check.sh` → 0). Replace it once R1 lands.

### Holistic "overstated" claims, against my spot-checks

| # | Holistic claim | My check | Call |
|---|---|---|---|
| 1 | Token counts are not a cost | Not spot-checked | agree |
| 2 | "None of the 44 checks changes a decision" is overstated | My merit table keeps `author_fidelity` and `source_locators_integrity` for the same reason | agree |
| 3 | P-F4 is MEDIUM, not HIGH | Reviews = 0 VERIFIED. Threads UNVERIFIED (cached field is an error string). #149/#151 red on `Classify` only. | agree: MEDIUM |
| 4 | P-F1 is HIGH, not CRITICAL | VERIFIED, and wider than reported (`candidate_id` also reissued). No book content changed. | agree HIGH, but **keep it first in order**: every future retraction repeats it |
| 5 | A-F7 is partly overstated | VERIFIED: 8 of 8 specs retired (`sum(retired_at is not null)` = 8), so "after judgment" is not triggered | agree |
| 6 | P-F11 stamps are noise | Not checked | agree |
| 7 | A-F1 data probably improved; verify the authors | **VERIFIED: author rows are byte-identical before and after** (same 6 names and order; only the rowids moved from 182–187 to 188–193). No §5(c) fabrication. The residual defects are the unevidenced completeness flag and the path. | agree |
| 8 | C7 is the design working | VERIFIED unpatched here | agree |
| 9 | "Net DB rows" undercounts schema work | Not checked | agree |

### Owner question: how to stop CI wake-ups for good

**VERIFIED:** `ci.yml` has **no `paths-ignore` and no `concurrency`** (`grep -n 'paths-ignore\|concurrency' .github/workflows/ci.yml` → nothing). Triggers: `push:[main]`, `pull_request:[main]`, `workflow_dispatch`.

**AMEND the four-part proposal:**
1. **`permissions.deny` in `.claude/settings.json`:** agree, but it must name **both** subscription tools, `mcp__Claude_Code_Remote__subscribe_pr_activity` and `mcp__github__subscribe_pr_activity`. For `send_later`, deny it only if the owner accepts losing it for non-CI reminders too; the deny rule cannot tell a CI poll from any other use. Caveat: deny stops the agent subscribing. It does not stop a subscription made by the harness at PR creation or by a PR Steward. [UNVERIFIED whether `create_pull_request` auto-subscribes; check once, and call `unsubscribe_pr_activity` if it does.]
2. **CLAUDE.md rule:** agree. It is not in e3846fa.
3. **Open the PR last:** agree. This is the one mechanism that removes the wake source, since CI runs only for `pull_request` into main (plus pushes to main). Measured exemplar: 0e701d1b, 0 wakes.
4. **`paths-ignore`: DISAGREE as specified.** Once R2's ruleset requires status checks, a workflow skipped by `paths-ignore` leaves those checks **pending forever and blocks the merge**. Use instead:
   - (a) R1, so log-only pushes stop existing;
   - (b) a short-circuit in the existing `classify` job: when the diff is only `transcripts/` or `scratchpad/`, emit empty kinds so the batteries skip and pass.

   **`concurrency`: agree with a scope.** Use `group: ci-${{ github.workflow }}-${{ github.event.pull_request.number || github.sha }}` with `cancel-in-progress: ${{ github.event_name == 'pull_request' }}`, so pushes to main are never cancelled. Note it cuts runner load but **not wakes**: a cancelled suite still emits `check_suite.completed`.

**Net:** the wake-ups end through items 1 + 2 + 3 + R1. `concurrency` is hygiene. `paths-ignore` should be replaced by the classify short-circuit.
