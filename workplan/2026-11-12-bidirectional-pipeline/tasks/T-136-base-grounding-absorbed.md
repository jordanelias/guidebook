# T-136  The base grounds itself: a direction and a relation carry their own words and locator, and no base row points into evidence

_One task of a stacked pull request (owner instruction of 2026-11-15: `grep -n -F "Owner instruction 2026-11-15 — tasks of the remediation plan are stacked" references/project-standards.md`). The ratification entry of 2026-11-19 says "each its own pull request" in its ACTION (2); those are the recorder's words, the owner's instruction of 2026-11-15 is stacked, and the stack stands. Read `CLAUDE.md` first; beyond it this file is self-contained. Why, and the options weighed: `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md`, items 12, 13, 14, 37, 38 and 39 (section 3) and section 4 item 2, ratified by the owner (`grep -n -F "## Owner ratification 2026-11-19" references/project-standards.md`). Every number was read on 2026-11-19 with the command that produces it: re-run it._

**Pilot status.** Not piloted. Authored 2026-11-19 from the ratified adjudication; evidence run read-only at `a6c478e0` (schema 159). Expect a defect in this file; report it rather than work around it.

## 1. Identity

| | |
|---|---|
| Task | T-136 |
| Title | The base grounds itself: a direction and a relation carry their own words and locator, and no base row points into evidence |
| Wave | 0 (now) |
| Layer (CLAUDE.md §3) | 1 |
| Kind | **TOOLING** (CLAUDE.md rule 10: tooling and research never share a pull request); one schema migration (`base_parameters`, `term_aliases`, `term_relations`), the writers `set-parameter-direction`, `add-term`, `add-alias`, `add-term-relation`, one audit branch, prose callers, a dated amendment of `tasks/T-129-design.md` A6 |
| Executor | NOT FOR SONNET: Opus-class. The task writes the shape of three warrants and the meaning of five refusals (a direction's words, a relation's words naming both terms, a hierarchy cycle, a parameter beside a provision, an absorbed phrase's attestation) |
| Traces to | OD-71 (`grep -n -F "## Owner statements 2026-11-18 — OD-71" references/project-standards.md`) and its ratified residue (2026-11-19); OD-56 (`grep -n -F "## Owner answer 2026-11-14 — OD-56" references/project-standards.md`); E4 (owner statement 2026-11-06 (second)); the T-028, T-029 and T-083 sweep items (`scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/sweep-list.md` lines 28 to 35, 59 to 60, 90) |

## 2. Preconditions

- **The integration base.** A task named below is merged if its commit is on `HEAD` (the batch's branch) or on `origin/main`. `$BASE` serves preconditions only; `BASE_PRE` (your starting commit) serves every diff, gate and count.
- **Tasks that must be merged to the integration base first:** T-028, T-029 and T-083, with their OD-71 repairs. Check by subject: `git log --oneline HEAD | grep -F -e "ground label picks in the base per OD-71" -e "ground term relations in the base per OD-71" -e "repair T-083 after the adversarial pass"` prints three lines.
- **Owner decisions:** OD-71 and OD-56, both answered by the owner. Run the gate of the convention of 2026-11-12 before you start and before you commit; anything but OPEN is a stop:
```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in OD-71 OD-56; do gate $n; done
grep -c -F "## Owner ratification 2026-11-19 — the third adjudication" references/project-standards.md
```
  Printed on 2026-11-19: `OD-71 OPEN (owner)`, `OD-56 OPEN (owner)`, `1`. The design items 12, 13, 14, 37, 38 and 39 carry no OD number; they are ratified by reference to the adjudication (the last line must print `1`). If a later entry narrows "Ratify all" (its ACTION (3)), stop.
- **Tests that must be red before you start:** `T136-01`, `T136-02`, `T136-05`, `T136-08`, `T136-10` (section 6).
- **Set-up** (stacked-branch convention, `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 1):

```
cd /home/user/guidebook                                    # repository root; every command below runs from here
bash .claude/hooks/ensure-deps.sh && python3 -c "import pydantic, jsonschema, yaml"   # a red check without pydantic proves nothing
git fetch origin
W=$(git log --remotes --format=%H -1 -- workplan/2026-11-12-bidirectional-pipeline); BASE=$(git branch -r --contains "$W" --format='%(refname:short)' | grep -x origin/main || git branch -r --contains "$W" --format='%(refname:short)' | head -1); echo "BASE=$BASE"
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-136" && mkdir -p "$SCRATCH" && cp data/guidebook.db "$SCRATCH/t.db"   # all experiments run on this copy
git rev-parse HEAD > "$SCRATCH/base_pre"; sha256sum data/guidebook.db | tee "$SCRATCH/db.sha"   # no git switch -c: stay on the batch's branch
```
- **Shell variables do not survive between calls:** begin each block with the `export SCRATCH=…` line and `BASE_PRE=$(cat "$SCRATCH/base_pre")`; probe with `GUIDEBOOK_DB_PATH="$SCRATCH/t.db"` inline and `--session session_task-probe`; never delete `refusals.jsonl`. `/session-open` and `scratchpad/CURRENT` are the coordinator's.

## 3. The problem, in the guidebook's terms

OD-71: "the base grounds itself"; a base row holds its justification in its own cells and waits on no evidence. Three base facts break this. A parameter's accessibility direction (which way is better for a disabled person, the rule every determination is read by) is recorded only by naming an admitted source holding an extraction for the parameter, through a foreign key into `evidence_sources`: the base is ordered after judgment, and the words saying which way is better are nowhere in it. A form absorbed from an observation keeps a foreign key into `observed_terms` and is written `unrecorded` (a search aid, never vocabulary) until its quote is found in a saved file. A relation between two terms rests on a locator alone: one observation warranted sixteen unrelated relations on a scratch copy, and the table accepts a three-cycle of `broader` and `element has parameter` beside `element has provision` for one pair, so a hierarchy can loop and a provision be read as a parameter (OD-56).

**Evidence commands** (read-only):

```
python3 -I -c "
import sqlite3,yaml;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
st={k:v for k,v in yaml.safe_load(open('governance/stage-map.yaml'))['tables'].items() if isinstance(v,str)}
print([(t,f[3],f[2],st.get(f[2])) for t,s in st.items() if s=='base' for f in c.execute(f'pragma foreign_key_list(\"{t}\")') if st.get(f[2]) not in ('base',None)])
print([r[1] for r in c.execute('pragma table_info(term_relations)') if 'quote' in r[1]], [r[1] for r in c.execute('pragma table_info(base_parameters)') if r[1].startswith('direction')])
print(c.execute('select count(*),sum(direction_ref_id is not null),sum(accessibility_direction is not null) from base_parameters').fetchone(), c.execute('select count(*) from term_aliases where observation_id is not null').fetchone(), c.execute('select attestation,count(*) from term_aliases group by 1').fetchall(), c.execute('select count(*) from term_relations').fetchone())"
grep -c -F 'attestation="unrecorded" if problem' scripts/db.py; grep -n -F "FROM AN ADMITTED SOURCE" scripts/db.py | cut -c1-40
grep -l -E 'INSERT INTO "?term_aliases"?' scripts/migrations/data_*; grep -l direction_ref_id scripts/migrations/data_*; echo end
```

**Printed on 2026-11-19:** `[('base_parameters', 'direction_ref_id', 'evidence_sources', 'evidence'), ('term_aliases', 'observation_id', 'observed_terms', 'evidence')]`; `[] ['direction_rationale', 'direction_ref_id']`; `(10, 0, 2) (0,) [('model_seed', 1163), ('unrecorded', 1219)] (0,)`; `1`; one line at `8206:` of `scripts/db.py`; then only `end` (no committed data migration INSERTs `term_aliases` or names `direction_ref_id`, so rule 5 lets both changes be made). This agrees with the adjudication. The two directions held predate the source rule and carry no warrant (`select parameter_id from base_parameters where accessibility_direction is not null`).

If the output differs, the ground has moved: stop (section 9).

## 4. The change

Order of preference, from CLAUDE.md §8: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. Every refusal names the next act.

**One schema migration** (number derived at execution: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1`, plus one; `scripts/migrations/NNN_base_grounding_absorbed.sql`, ending with `PRAGMA user_version = NNN`). Model it on migrations 155 and 156 (`DROP COLUMN` where SQLite allows; create, copy, drop, rename where a column sits in an index or another column's CHECK). Spell every new non-blank CHECK with 156's whitespace and zero-width set (`dbcore.ZERO_WIDTH` is its Python twin), not the older `char(32,9,10,13)`.

1. **The direction's warrant, absorbed (item 13).** `base_parameters` gains `direction_quote` (the source's words stating which way is better, verbatim), `direction_source_url`, `direction_source_page`, `direction_source_clause`, `direction_source_line`, spelled and checked as the `quantity_kind_*` cells are. `direction_ref_id` stays, **provenance only**: its foreign key into `evidence_sources` is dropped (every row holds NULL today, so the column may be dropped and re-added without one, or the table rebuilt). The row CHECK: the five warrant cells are all present (a quote, a URL, and a page or a clause; the line optional) or all absent, and a warrant with no `accessibility_direction` is refused. The CHECK does **not** require a warrant on every direction: the two pre-rule directions were written by committed data migrations, which must replay, and their backfill is open owner question 7 (`grep -n -F "open owner question 7" skills/run-pipeline_SKILL.md`).
   **`set-parameter-direction`**: the refusals "--ref-id is required", "not an admitted source" and "holds no extraction for parameter N" are **removed** (OD-71: a base writer "neither requires it nor refuses a row for lacking it"; the 2026-10-30 basis is superseded on contact, adjudication item 13). In their place, and before any write: refuse a direction (any value of the CHECK, `contested` included, as `--ref-id` was required of every value) without `--direction-quote`, `--direction-source-url` and `--direction-source-page` or `--direction-source-clause`; refuse a blank or zero-width part and a malformed URL through `_check_base_locator(…, prefix="direction-")`; refuse a quote with no letter (words that state nothing). `--ref-id` stays, optional, shape-checked, never looked up. The "re-stating a direction is refused" refusal stays unchanged. **What this weakens, stated (open point O-1):** the replacement asks only for words with a letter and a well-formed locator, and the direction is write-once, so `x`, `https://example.org`, page `n/a` would fix the rule every determination of the parameter is selected by, with no correcting verb. Invent no stronger test (a length, a word list; a lookup into evidence OD-71 forbids). `contested` today needs one `--ref-id` like any value, and the engine then anchors no value (`grep -n 'if direction == "contested"' scripts/assess/assess_cell.py`); this task asks one warrant of it, though a contest is two sources' words: report it, add no second warrant. Reuse the `_KIND_WARRANT` shape (one tuple per flag, one helper for flags and dispatch) by parameterising it on the prefix rather than copying it.
2. **An absorbed phrase is attested by its locator (item 14).** `term_aliases.observation_id` is dropped, with its CHECK branch (`OR observation_id IS NOT NULL`: an attested occurrence then says where, always) and its place in `ux_term_aliases_occurrence` (rebuilt on the same key without it). `add-term --from-observation` and `add-alias --observation-id` accept `--source-url`, `--source-page` or `--source-clause`, and `--source-line` (refused as "stray" today): the operator's, because mapping the observation's free-text `locator` would be a guess (sweep list line 59); print that `locator` beside any refusal as a hint. Then:
   - `add-term --from-observation` with a locator writes the first form attested (`--attestation`, default `other_source`; `_observed_source` still refuses `instrument` outside the regulatory stratum); **without** a locator it writes the form `unrecorded`, says so, and names `add-alias` with the locator flags as the promotion. The saved-file wait (`_observed_quote`'s second branch, "is not in a file saved for …") no longer decides anything on either route: that is the `unrecorded` hold the adjudication removes (E4; the seventh statement: "none of the work in base needs to be verified and stored in evidence").
   - `add-alias --observation-id` **requires** the locator (an alias route exists to attest; a seed has its own route): refuse without it, naming the flags. The refusal "the latest adjudication of observation N does not name TERM" stays: it is the judgment at write time.
   - The phrase-in-quote test (`_observed_quote`'s first branch) stays a refusal on `add-alias`, where it is today. On `add-term --from-observation` it keeps today's effect (the form is written `unrecorded`, not refused): item 14 names only "`unrecorded` otherwise", and making it a refusal there would be this author's addition. Delete the saved-file branch and every caller of it the sweep finds.
   - Neither route writes the observation's id into `notes` (data in the wrong cell, owner 2026-11-06): the observation-to-term link is the judgment stage's `term_adjudications` row, which points into the base, as OD-71 allows.
   - `scripts/audit/alias_provenance_audit.py` (BLOCKING) reads the dropped column twice: `classify()`'s `observation_id` fallback and the "re-judged since" branch (T-074). Both go with the column, because the base row no longer rests on an observation (OD-71, "grounded as if it were always there"); the branch examined 0 rows today (`select count(*) from term_aliases where observation_id is not null`). **This also closes, without an adjudication item, the T-074 question "whether the latest governs" (`grep -n -F "Whether the latest governs is an owner question" workplan/2026-11-12-bidirectional-pipeline/BATCH-1-EXECUTION-NOTES.md`): open point O-2, for the owner's confirmation.** Nothing replaces the branch: the write-time refusal (the latest adjudication must name the term) stays; a later re-judgment no longer reaches a stored form. Name it in the commit body as a subject withdrawn by a ruling, pending O-2.
3. **A relation's words name both terms (items 12 and 38).** `term_relations` gains `source_quote` (the source's words, verbatim). CHECK: a row with a URL carries a quote and a row with a quote carries a URL; every kind but `distinct` carries both (`distinct` rests on `reason`, which stays the base's own cell, item 39). `add-term-relation --source-quote` refuses, in this order after the existing refusals: a located row with no quote; a quote that does not hold **a recorded form of each term**: its label (`terms.canonical_en`) or any `term_aliases.alias` of the term, any language, seeds included, (a check that the words concern the terms, not a vocabulary act: item 38). The refusal names the missing term and the next act: record the form the source uses first (`add-alias` with its locator), then relate. **Containment, one helper in `scripts/dbcore.py`, derived from the script, never a language list:** both texts are NFKC-normalised and case-folded; a form holding any character whose Unicode East Asian Width is `W` or `F` (`unicodedata.east_asian_width`: Han, kana, Hangul, fullwidth forms, scripts written without spaces between words) is matched as a substring (Korean particles attach: `경사로` inside `경사로의`); any other form on word boundaries, as `_as_whole_words` does. Residual, stated in the docstring: a script without word spaces whose characters are not wide (Thai, Lao, Khmer, Myanmar) is matched on word boundaries and may miss; report it, do not type a script list. On live rows (`select surface_form, context_quote from observed_terms` where the form holds a wide character) `_as_whole_words` found 1 of 9 phrases in their own quotes on 2026-11-19 and this rule finds 8; the ninth (observation 10) is not in its quote at all.
4. **No contradiction a hierarchy cannot hold (item 37).** `add-term-relation` refuses: (a) a `broader` or `part of` row whose `to` term already reaches its `from` term through live rows **of the same kind** (a recursive CTE over `retired_at IS NULL` rows; the two-cycle is already refused as "the same pair"), naming the path found; (b) an `element has parameter` row where a live `element has provision` row joins the same two terms, and the reverse (OD-56), naming the held row and `retire-term-relation`. `broader` beside `part of` for one pair stays **allowed** ("Conflation is recorded, not resolved", owner 2026-11-06 (sixth)). Cycles are read on raw term ids; reading them through survivors is T-129's (amendment below).
5. **Amend `workplan/2026-11-12-bidirectional-pipeline/tasks/T-129-design.md` A6 (item 39)** by appending, under A6's paragraph, this dated line and nothing else (never a silent rewrite):

   > **Amended 2026-11-19 (third adjudication item 39, ratified 2026-11-19; OD-71):** a `distinct` row that `add-term --distinct-from` writes carries no pointer to the NAMES-NEW adjudication: `term_relations` has held no warrant key into the judgment stage since `1c5e4ce9`, and OD-71 forbids a base row pointing into an adjudication. Its warrant is its own `reason` cell, the `--rationale` text, absorbed into the base ("grounded as if it were always there"). Relations of a merged term are read through `v_term_survivor`; the raw-id unique index `ux_term_relations_live_pair` stays as the record written. T-136's cycle and parameter-or-provision refusals read raw term ids.

**What reads it:** the direction cells: `set-parameter-direction`, the contract criterion (rewritten), the owner browser; `assess_cell.py` reads `direction_ref_id` as before. `source_quote`: `add-term-relation`, and `element-parameters` (add it to its SELECT). **Without it**, a direction cannot be recorded without a judgment-stage row, and carries no words; a relation can rest on words about something else; a looping hierarchy or a provision read as a parameter reaches the element pages.

**Not in this task:** a warrant for the two pre-rule directions; the kind quote's unit test (T-137); T-029 §4's text (the coordinator's plan edit).

**Schema migration discipline.** Run `python3 scripts/audit/joined_cells_census.py` before and after and keep both outputs (it counts only columns holding data, so an empty new column proves nothing: say so). List and recreate every view, index and trigger naming a rebuilt table (`select type, name from sqlite_master where sql like '%<table>%'`). Show that the replay plan orders the migration after every data migration (`python3 -c "import sys;sys.path.insert(0,'scripts');import migrate_db as m;p=m.build_plan();print(p[-1][:2], [s[:2] for s in p if s[0]=='data'][-1])"`: the last step is your schema migration). Apply only with `python3 scripts/migrate_db.py`; prove with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` (exit 0) and `python3 scripts/audit/migration_reproducibility.py --deep` (PASS). No `scripts/migrations/data_*` file. Then `python3 scripts/generate/context_map.py` and include `governance/context-map.yaml`.

**Code size.** Report `git diff --shortstat "$BASE_PRE" -- scripts schemas .github skills ':!scripts/migrations'` (after `git add`), and for anything added name what reads it and what it replaces or makes deletable (the removed `--ref-id` lookups, `_observed_quote`'s saved-file branch and the audit's re-judged branch are deletions).

## 5. Caller sweep

Names to sweep: `direction_ref_id`, `set-parameter-direction`, `set_parameter_direction`, `FROM AN ADMITTED SOURCE`, `observation_id` (in `term_aliases` contexts), `form_unrecorded`, `_observed_quote`, `add-alias --observation-id`, `--from-observation`, `ux_term_aliases_occurrence`, `add-term-relation`, `add_term_relation`, `term_relations`, `base-direction-from-source`.

A caller is a hit whose behaviour or truth changes (code, a test exercising it, a view, index or trigger, a registry entry, a skill or governance sentence stating it); a hit that stays true is a mention. **Fixing a caller is in scope** (rule 4). Left out: `workplan/` except `machines.yaml`, the ledger, `scripts/migrations/`, and the frozen records.

```
N='<name>'
git grep -n -F -e "$N" -- scripts schemas .github .claude skills ':(exclude)scripts/migrations'
python3 -I -c "import sqlite3,sys;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print([(r[0],r[1]) for r in c.execute('select type,name from sqlite_master where sql like ?',('%'+sys.argv[1]+'%',))])" "$N"
python3 -c "import yaml,sys;print([c['id'] for c in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if sys.argv[1] in str(c)])" "$N"
git grep -n -F -e "$N" -- governance architecture CLAUDE.md references workplan/pipeline-state-graph/machines.yaml ':(exclude)references/project-standards.md' ':(exclude)references/search-log'
```
This task changes verbs and refusal texts: run `python3 workplan/pipeline-state-graph/build_graph.py --check` before and after and report the difference (red on the base; only a failure line your change adds is yours).

**Callers found on 2026-11-19** (re-run; a new hit is yours to judge): `scripts/db.py` (`set_parameter_direction`, `p_spd`, `insert_term`, `add_alias`, `_observed_quote`, `_observed_source`, `rename_term`'s next-action text, `add_term_relation`, `p_atr`, `element_parameters`); `scripts/assess/assess_cell.py` (a comment); `scripts/audit/alias_provenance_audit.py`; tests `test_run_pipeline_refusals.py` (section A6), `test_db_amend_writers.py`, `test_scan_contract.py` (`form_unrecorded`, the T-028 and T-029 cases), `test_evidence_cell_state_2_3.py`; skills `run-pipeline_SKILL.md` (the direction, `unrecorded` and `term_relations` sentences), `cross-population-conflict-mapper_SKILL.md` ("requires `--ref-id`"); `governance/pipeline-contract.yaml` (criterion `base-direction-from-source`), `governance/evidence-architecture.md` (read its direction bullet), `governance/context-map.yaml` (regenerated). `machines.yaml` names none of these verbs.

## 6. Verification

**Step 1, before any edit: the before-run.** Checks that read what this task touches: `test_scan_contract test_db_amend_writers test_run_pipeline_refusals test_db_integrity alias_provenance_audit schema_reference_audit column_vocabulary_audit derived_not_curated_audit pipeline_contract_audit migration_reproducibility context_map_fresh`.

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-136"
CHECKS="test_scan_contract test_db_amend_writers test_run_pipeline_refusals test_db_integrity alias_provenance_audit schema_reference_audit column_vocabulary_audit derived_not_curated_audit pipeline_contract_audit migration_reproducibility context_map_fresh"
for c in $CHECKS; do cmd=$(python3 -c "import yaml,sys,shlex;print(shlex.join(next(x['cmd'] for x in yaml.safe_load(open('governance/check-registry.yaml'))['checks'] if x['id']==sys.argv[1])))" $c); $cmd > "$SCRATCH/before-$c.txt" 2>&1; echo "$c rc=$? | $(grep -E 'EXAMINED|RESULTS|FAILED|VERDICT' "$SCRATCH/before-$c.txt" | tr '\n' ' ' | cut -c1-200)"; done
```
Record any check red here; one with no `EXAMINED:` line, or `EXAMINED: 0`, examined nothing: say so.

**Step 2: red before, green after.** Case ids `T136-NN`; confirm the prefix is free (`git grep -c '"T136-' -- scripts/tests` printed nothing on 2026-11-19). Direction cases go in `scripts/tests/test_run_pipeline_refusals.py` (beside section A6), term and relation cases in `scripts/tests/test_scan_contract.py` (beside the T-028 and T-029 cases). Probes by query or on the test's own scratch copy labelled `TASK-FIXTURE`; type nothing the database can derive. Show each case red on a seeded defect you then remove (`cmp`).

| Case | Red before (or the seeded defect) | Green after |
|---|---|---|
| T136-01 | the derived join of section 3 lists two base foreign keys into evidence | it lists none (read the stage map and `pragma foreign_key_list`, never a typed table list); seeded defect: re-add the key in a scratch migration |
| T136-02 | `set-parameter-direction` with words and a locator and no `--ref-id` is refused | it writes the direction and the five warrant cells; `direction_ref_id` NULL; a `--ref-id` naming no source is kept as given (provenance, not looked up) |
| T136-03 | seeded: drop the quote check | a direction with no `--direction-quote`, with a quote holding no letter, with no URL, with a URL and neither page nor clause, with a zero-width page: each refused, nothing written (compare the row before and after) |
| T136-04 | seeded: drop the CHECK on a rebuilt scratch copy | the table refuses a raw INSERT of a warrant with no direction, and of a partial warrant |
| T136-05 | `add-term --from-observation` with a locator, on an observation whose quote is in no saved file, writes the form `unrecorded` | it writes it `other_source` with the locator; without a locator it writes `unrecorded` and names the promotion |
| T136-06 | seeded: let `add-alias --observation-id` pass with no locator | it is refused, naming the flags; with a locator it writes an attested row with no `observation_id` column and no observation id in `notes` |
| T136-07 | seeded: drop the phrase-in-quote test | an observation whose quote does not hold its phrase is refused by `add-alias` and written `unrecorded` by `add-term --from-observation`, with a locator or without |
| T136-08 | `add-term-relation` writes a located row with no `--source-quote` | refused; a quote naming only one term is refused naming the other; a quote holding a seed form of each term passes |
| T136-09 | seeded: use `_as_whole_words` for every form; then seeded: substring for every form | one case per script family, each a live observed phrase and its own quote chosen by query (a Japanese and a Korean phrase found by substring; a Latin form found only inside a longer word, `ramp` in `ramparts`, refused); no language code is typed |
| T136-10 | a three-cycle of `broader` is written on a fixture | the closing row is refused naming the path; the same for `part of`; a four-cycle too (the CTE is not length-bound) |
| T136-11 | seeded: drop the parameter-or-provision refusal | `element has provision` beside a live `element has parameter` for the same two terms is refused, and the reverse; `broader` beside `part of` for one pair passes |
| T136-12 | seeded: re-add the re-judged branch reading a column that no longer exists | `alias_provenance_audit.py` runs on the rebuilt schema with exit 0 and an `EXAMINED`-bearing summary; it reads no `observation_id` of `term_aliases` (AST or text scan of the file) |

**Step 3, after the change: the after-run.** The same loop with `after-`; compare check by check: `diff <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/before-$c.txt") <(grep -E '\[✗\]|^ *FAIL|^FAILED|VERDICT: FAIL' "$SCRATCH/after-$c.txt")`. No failing case may appear that was not failing before; a case of the before-run that asserted the old refusals (`--ref-id` required, `form_unrecorded`) is a caller updated to the ruled behaviour, named in the commit body with the ruling.

**Step 4: the gate, once**, when every edit is made, in the background with a long timeout, waiting with an until-loop on its output file:

```
export SCRATCH="${TMPDIR:-/tmp}/guidebook-t-136"; BASE_PRE=$(cat "$SCRATCH/base_pre")
scripts/preflight.sh --base "$BASE_PRE" --explain > "$SCRATCH/gate.txt" 2>&1; echo "rc=$?"; grep -E '^(RESULT|PREFLIGHT|SELFTEST)|FAIL|NOTHING-IN-SCOPE' "$SCRATCH/gate.txt"
```
Read the `RESULT` line, any `NOTHING-IN-SCOPE` (not a pass), any blocking `FAIL` (one red on `$BASE_PRE` too is not yours: give both lines).

## 7. Commit

Commit after the gate is clean, staged with `git add -A . ':!transcripts' ':!*commands.jsonl' ':!.claude/worktrees'` (check `git status` lists only your files):
```
git commit -m "governance: the base grounds a direction and a relation in its own words and locator, and points into no evidence row [$(date -u '+%Y-%m-%d %H:%M')]" -m "<body: what changed, the evidence before and after, each caller and what was done, the removed refusals and the ruling that removed each>" -m "<the attribution trailers your session instructions give>"
```

## 8. What you must NOT do

- Do not write `data/guidebook.db` except through `scripts/migrate_db.py`.
- Do not run `scripts/run_checks.py --all`, `scripts/bootstrap.sh`, or `pip install -r requirements.txt`; do not push, open a pull request, subscribe, run `/adversarial` or `/batch-done` (the coordinator's).
- Do not write a warrant onto the two pre-rule directions, or any research row (rule 10).
- Do not add a foreign key from a base table into evidence or judgment, or a pointer a base row's validity waits on (OD-71); do not keep `observation_id` under another name, in `notes` or anywhere in `term_aliases`.
- Do not map an observation's free-text `locator` into a page or a clause.
- Do not build a word segmenter, a script or language list, a stop-word list or a judge vocabulary (rule 8).
- Do not add a table, column, flag, check or verb that section 4 does not name; list in your report any helper you add. Fixing a caller the sweep finds is in scope.
- Do not weaken a refusal, relax a CHECK, quarantine a check or change a registry level. The three refusals section 4 removes are removed by the owner's ruling, named there; nothing else is removed.
- Do not edit `tasks/T-129-design.md` beyond the one dated line, nor T-029's file. Hand-type no count.

## 9. Stop conditions

Stop, change nothing further, and report (what you ran, saw and expected) when:
- a precondition of section 2 is not met, or the gate prints anything but OPEN, or a later ledger entry narrows the ratification;
- an evidence command of section 3 prints otherwise (in particular: any row with `direction_ref_id` or `term_aliases.observation_id` set, any committed data migration naming either, a live `term_relations` row);
- a red test is not red before or not green after one honest attempt;
- the sweep finds a caller you cannot repair without adding something section 4 does not name;
- a check green in the before-run is red after, other than a case asserting a refusal section 4 removes by ruling;
- `migrate_db.py --rebuild` does not reproduce the database, or the replay plan does not order your migration after every data migration;
- you would have to guess a value, a form, a locator or an owner's intent (for instance whether `contested` needs a warrant: this file keeps the refusal on every value, as `--ref-id` was; if the owner has since ruled otherwise, stop);
- a probe shows a warrant you judge to be junk accepted (O-1): record the probe and its output in the report as an open point; do not add a test of your own to refuse it.

**Open points for the owner (carried in the report, not decided here).** O-1: the direction's replacement warrant is checked for form only, and the direction is write-once; is a stronger test, or a correcting verb, wanted? O-2: dropping `term_aliases.observation_id` ends the T-074 re-judgment check; confirm that a later adjudication no longer reaches a stored form.

## 10. Rollback

Before merge the coordinator drops the commit; after merge, `git revert` in a new pull request. A committed migration is never edited: fix forward (rule 3).

## 11. Adversarial pass and pull request

The coordinator runs `/adversarial`, `/batch-done`, the push and the pull request. Report per `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/executor-brief.md` section 3, with a heading "Task-file defects".
