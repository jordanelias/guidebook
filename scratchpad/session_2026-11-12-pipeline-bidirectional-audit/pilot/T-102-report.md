# T-102 pilot report: PARTIAL dry pilot, stage P7 (mobility split)

Executor: Opus-class pilot, 2026-11-13. Task file `workplan/2026-11-12-bidirectional-pipeline/tasks/T-102-mobility-split.md`. Design `tasks/T-102-design.md` governs where the two differ. Scope as given by the coordinator (OPEN-ITEMS-PLAN §4 row P7): the carry decision table and after-tests (3) and (5) on a sample of MOB figures, taken through `emit_batch_sql.py` to a scratch migration that is never applied to the canonical copy. **Outcome: PILOTED (partial).** No row was written to the canonical database or its committed copy. The design's section 10 report was not appended.

## Base, stack and set-up

- **Base commit:** `10f9072` (`origin/claude/peaceful-noether-kvf3sf`). Per the brief I overrode the task file's own `BASE=` line. That line derives the base from the workplan's last commit, and on this clone it would have chosen a stale base.
- **Clone:** `$SCR/pilot/T-102`, branch `pilot-T-102`. `ensure-deps.sh` and `import pydantic, jsonschema, yaml` both passed.
- **Stack, and the route that worked for each patch:**

| Patch | Route | Migration |
|---|---|---|
| T-008-repilot | plain `git am` | 126_value_as_written |
| T-016 | plain `git am` | none |
| T-017 | plain `git am` | none |
| T-018 | plain `git am` | 127_extraction_lens_links |
| T-019 | plain `git am` | none |
| T-055 | plain `git am` (one whitespace warning) | 128_device_class_mobility_values |
| T-024 | plain `git am` failed; `git am --3way` failed. `git apply --index --exclude=data/guidebook.db` also failed (context in `governance/context-map.yaml` and `scripts/db.py`). **What worked:** `git apply --3way --exclude=data/guidebook.db`, then two conflicts resolved by hand and a local commit `da3ed58`. In `scripts/db.py`, `_AMENDABLE_SVE_FIELDS` now holds the union of T-055's `device_class` and `value_as_written` and T-024's `jurisdiction`. In `governance/context-map.yaml` I took ours and regenerated the file with `context_map.py`. | **renumbered 126 to 129**: file `129_jurisdiction_registry.sql`, its header line, `PRAGMA user_version = 129`, the seed rows' `created_by_session` `migration_126` changed to `migration_129`, and the context-map entry |
| T-025 | plain `git am` | **none (checked: no file under `scripts/migrations/`)** |

- After the stack, `python3 scripts/migrate_db.py` printed `Schema at version 129; 0 data migration(s) applied`. `base_jurisdictions` holds 36 rows. `context_map.py --check` prints `EXAMINED: 1 context map ... fresh`.
- **Scratch:** `/tmp/guidebook-t-102` (TMPDIR is unset, so the file's `${TMPDIR:-/tmp}` resolves to `/tmp`). It held `s.db` (the working copy) and `base.db` (the pre-change copy, for replay). I made no `t.db`: probes ran read-only or with `--dry-run`, which kept the number of database copies down as the coordinator asked. A temporary `replay.db` and `rebuilt.db` were made, then deleted. Every scratch file is deleted at the end.
- **Canonical database sha256:** `c9ecb846...7c4d` before, and the same after.

## Preconditions (section 2)

- OD-14, OD-37, OI-13, OD-31 and OI-03 each read `... STATUS: ANSWERED BY THE OWNER` as their last line.
- `grep -n -F "OD-14: codes confirmed as proposed in T-102-design.md"` finds 1 line (6063).
- The fifth-set full heading occurs once (`git grep -c` prints 1; `dbcore.ledger_quote_count` prints 1). The short form occurs 2 times, which matches what the design says.
- The seventh-set full heading occurs once.
- **T-054 is not in the stack**, although section 2 requires it merged. That was expected for this pilot. Item 4a therefore cannot finish (see 6a below).

## Evidence command (section 3)

Run on the clone after the stack, it printed what section 3 says:
- `[('LMB', None, 'active'), ('MOB', None, 'active'), ('SCI', None, 'active')]`
- Live lens links: `MOB 170, ALL 34, BLIND 3, SCI 3, MS 2`.
- MOB `device_class`: NULL 105, `manual_self_propelled` 18, `mixed` 7, `not_device_scoped` 40.
- MOB grades: 59.

The ground has not moved.

**Item 4a's "counts today" command is wrong.** It reads `source_value_extractions.identity_code='SCI'` and prints `('source_value_extractions', 0)`. The same database holds 3 live SCI figures (`select count(*) from v_live_lens_links where identity_code='SCI'` prints 3). T-018 NULLed that column. The task file itself warns about exactly this in section 3 and in test (3), and then repeats the mistake in 4a.

## What was done on `s.db` (all through `db.py`, every call with `GUIDEBOOK_DB_PATH` inline, session `session_2026-11-13-t102-pilot`)

**(b) The children.**
- `add-identity` `WHEEL`, `LLD` and `WALKAID`, each with `--parent MOB --category mobility`, taking the descriptions in design §2.
- `amend-identity --code MOB --display-name "disabled people with mobility needs"`. Its output printed the replaced value, as designed.
- **The patch's flag is `--ledger-pointer`.** The folded task file and design §9 say `--approval-ref`, checked by `dbcore.require_approval_heading`. That function does not exist in the stack (`grep -c require_approval_heading scripts/dbcore.py scripts/db.py` prints 0). The patch checks `dbcore.require_ledger_quote_once`, which accepts any quote that occurs once, not only a heading. I passed the full fifth-set heading.
- **Item 3, the children's crossings**, written with `add-population-icf-link --mapping-confidence moderate_contextual --provenance "T-102 design and report"`: WHEEL d465, d420, d410; LLD d450, d455; WALKAID d450, d465.
- **The design gives no `--mechanism`, which the verb requires.** I wrote a labelled placeholder. A real executor would have to guess the value, and section 9 makes that a stop.

**(c) The sample.** Chosen by query: the design's keyword groups, taking the first rows of each by `extraction_id`, plus the first rows under the most frequent regulatory heading. Each row's judgment:

| ext | Its words / participants | Judgment (row of design §6) | Writes |
|---|---|---|---|
| 13 | "wheelchair propulsion at different speeds and inclines" | wheelchair users → WHEEL, `named_in_text` | link 217; MOB link 3 retired |
| 12 | "propelled a MWC" (participants: able-bodied proxies) | names the device, not users. Carried to WHEEL by device, `named_in_text`. Ambiguous under the table (finding 9) | 218; retired 2 |
| 11 | names no one. Participants: "17 spinal cord injury participants propelling their own manual wheelchairs" | WHEEL, `study_participants` (text found in the grade's study_population) | 219; retired 1 |
| 20 | "車椅子ユーザー" (first person) | WHEEL; drive not stated | 220; retired 10 |
| 21 | "車椅子を自走で上る" | WHEEL; drive stated → `amend-extraction --field device_class --value manual_self_propelled` (NULL before) | 221; retired 11; device set |
| 52 | "Every member of the wheelchair user group, including quadriplegics" | WHEEL. The level stays in the quote (`base_taxonomy_medical` holds 0 rows) | 222; retired 42 |
| 55 | "walking aid users" and "ambulant users with stamina limitations" (and hemiplegics, quadriplegics) | WALKAID, plus MOB judged (a no-device mobility group). Walking-aid kind unstated → `device_class` left NULL (finding 10) | 223 WALKAID; 224 MOB replaced carried 45 |
| 194 | "a scooter user" only | MOB judged (E2); `device_class scooter` | 225 replaced 179; device set |
| 196 | "manual and power wheelchair users and ... scooter users" | WHEEL, plus MOB judged for the scooter users; `device_class mixed`. The table's "several → retire MOB" row contradicts its "scooter → keep MOB" row (finding 8) | 226 WHEEL; 227 MOB replaced 181; device set |
| 120 | Singapore Code 2025 Table 5 ramp gradient tiers. Heading names no group; nothing warrants an ICF or need link | general heading, no lens warrantable → **keep the carried MOB and list the row** | none (listed) |

**Grades.**
- One new child grade where the participants are the child: `REF-00985 → WHEEL EXACT` ("17 spinal cord injury participants propelling their own manual wheelchairs").
- No MOB grade was touched.

**(f) §6a, SCI to WHEEL.**
- **Figures:**
  - 158 → WHEEL `named_in_text` "five wheelchair users with cervical cord injury".
  - 159 and 160 → WHEEL `study_participants` (their words do not name wheelchair users).
  - SCI links 145, 146 and 147 retired.
  - Design §2 says "every figure filed under SCI today names 'wheelchair users with cervical cord injury'". **That is false for 159 and 160** (finding 12).
- **Grade:** a new `REF-01033 → WHEEL PARTIAL`, naming its participants. The SCI grade stays.
- **Crossings:**
  - Sample move: SCI link 24 (d450) → WHEEL, keeping "Biomechanical + autonomic" and `high_predictive`, with provenance naming link_id 24.
  - A dry-run probe of SCI link 22 (d410) → WHEEL was **accepted**, although WHEEL already holds d410 from item 3. `UNIQUE(identity_code, icf_code, mechanism)` includes the mechanism, so the "a row the table's UNIQUE refuses" branch of design §6a.3 never fires. Two live WHEEL d410 rows would differ only by mechanism and confidence (finding 13).
  - Judgment on the rest:
    - d410, d420 and d465 are already on WHEEL by item 3. They should be retired with reasons naming the WHEEL rows.
    - d455 holds for wheelchair users (move).
    - d510, d520, d530 and d630 (self-care, meals) come from the injury's upper-limb and autonomic involvement, not from wheelchair use, so they should be retired with no successor.
- **What T-102 cannot do in this stack (T-054 is absent):**
  - `retire-population-icf-link` does not exist (`db.py: error: argument command: invalid choice`).
  - `identity_icf_map` has **no `retired_at` column** (columns: `link_id, identity_code, icf_code, mechanism, mapping_confidence, provenance, notes, created_at, created_by_session`).
  - `retire-identity` does not exist.
  - `base_taxonomy_identity` has **no `superseded_by_identity` column**. Its `status` CHECK is `{active, deprecated}`.
  - Consequences:
    - The 9 SCI crossings stay live.
    - SCI stays `active`.
    - Test 9's second query fails with `no such column: retired_at`.
    - Test 1's SCI clause fails with `no such column: superseded_by_identity`.

## After-tests, scratch copy (before = `base.db`, after = `s.db`)

The test commands are hard-coded to `data/guidebook.db`. I ran each with the path replaced by the scratch path (finding 4).

| Test | Before | After | Note |
|---|---|---|---|
| (3) no MOB figure names a device | `EXAMINED: 170`, 28 | `EXAMINED: 164`, 24 | Of the 24, 22 are unsampled carried rows. **2 are deliberate judged MOB links**: 55 (a no-device group named beside walking-aid users) and 196 (scooter users named beside wheelchair users). By the design's own table, test (3) can never reach 0 while E2 keeps scooter users on MOB. The test's regex also missed ext 12 ("MWC") before the carry (finding 6) |
| (5) no division held twice | `EXAMINED: 1`, [] | `EXAMINED: 4`, [] | **Green before as well as after.** The defect item 5 fixes ("; wheelchair users" in MOB's name) is not one of the test's words. It cannot go red on the defect in front of it (finding 5) |
| (1) children with parent; MOB active | MOB only | MOB "disabled people with mobility needs", WHEEL/LLD/WALKAID parent MOB, active | SCI clause errors (no `superseded_by_identity`) |
| (4) no fan-out | MOB grades 59 | 59; two child grades, each naming participants | — |
| (6) every link judged | — | 161 carried on the family | expected for a sample |
| (7) G04 every figure has a live lens | — | `[✓] G04 ... (214 examined)`, 57/57 (`test_db_integrity` with `GUIDEBOOK_DB_PATH`) | — |
| (8) device and child agree | — | `EXAMINED: 11` child links, 0 disagreements | — |
| (9) SCI carried | 3 live SCI links | 0 live SCI links. Crossings query errors | blocked by T-054 |
| (10) counted once | — | EXISTS gather 173 figures; join 175 rows / 173 distinct | green; T-055's `T055-04` PASS |

**Design-equivalence reasoning for a determination at MOB.**
- After the carry, MOB's family is `MOB, LLD, WALKAID, WHEEL` (recursive CTE).
- **Parameter 3 (ramp gradient).** Every sampled figure for it now sits on WHEEL, apart from 55 (WALKAID plus MOB) and 120 (MOB, carried).
  - In this sample the children's demands are not opposed: every figure argues for gentler slopes.
  - But the 2026-08-25 ruling records the opposition (manual wheelchair users against ambulant people with fatigue). So a MOB cell for parameter 3 is not design-equivalent, and it is determined per child.
  - **Nothing in the stack refuses a MOB cell for parameter 3.** The design-equivalence test belongs to T-110, which is not in the stack. The parent gather of T-055 would gather it without complaint.
- **Parameter 4 (ext 196, a width accommodating the percentages of each device group).** WHEEL and scooter users on MOB want more width in the same direction, so MOB passes the test there. The largest footprint (scooters) governs.

## (e) Emit and replay

- `emit_batch_sql.py --scratch s.db --out batch.sql` (canonical defaulted to the clone's `data/guidebook.db`, byte-identical to `base.db`) printed `27 insert(s), 16 update(s), 0 delete(s)`, rc 0.
- Statements by table:
  - `base_taxonomy_identity`: 3 INSERT, 1 UPDATE.
  - `evidence_population_match`: 2 INSERT.
  - `identity_icf_map`: 8 INSERT.
  - `source_value_extractions`: 3 UPDATE.
  - `extraction_lens_links`: 14 INSERT, then 12 UPDATE.
- **Replay, in emitted order, on a fresh copy of `base.db`: FAILED** with `UNIQUE constraint failed: index 'ux_extraction_lens_live'`. **This stack's emitter has T-018's INSERT-before-UPDATE defect.**
  - The emitter last changed on 2026-10-16 (`d63fa40`). No patch in the stack touches it.
  - The cause: `add-lens-link` on a code with a live *carried* link retires the carried one and inserts the judged one in one call. The emitter writes each table's INSERTs before its UPDATEs. So the judged MOB links 224, 225 and 227 are inserted while carried links 45, 179 and 181 are still live in the replay, and the partial unique index refuses them.
  - Every row that stays on MOB with a judged warrant takes this path. Design §6 makes that the normal path ("keep MOB, judged").
- **The full write path fails the same way.** `emit_data_migration.py --session session_2026-11-13-t102-pilot.md ...` wrote `data_20261113051730_...sql` in the clone. `migrate_db.py --rebuild /tmp/guidebook-t-102/rebuilt.db` then printed `ERROR applying data_20261113051730_2026-11-13-t102-pilot: UNIQUE constraint failed: index 'ux_extraction_lens_live'`, rc 1. I deleted the file and the rebuilt database. Nothing was applied to the clone's DB or to the canonical one.
- **Replay with the lens-link UPDATEs moved ahead of that table's INSERTs:** OK. Compared table by table with `s.db`, all five are IDENTICAL:
  - `extraction_lens_links` 230 rows
  - `base_taxonomy_identity` 26
  - `identity_icf_map` 69
  - `evidence_population_match` 63
  - `source_value_extractions` 214
- `emit_batch_sql.py --selftest` prints 19/19 PASS. **None of its cases covers a partial unique index**, so it cannot go red on this defect.

## Gates and checks (EXAMINED lines)

- **`research_batch_dod.py --session session_2026-11-13-t102-pilot`** (on `s.db`): rc 1.
  - **R1 ✗** (no Co-1 pass). **R9a ✗ and R9b ✗**: NOTHING IN SCOPE, "this batch admitted no sources AND logged no searches".
  - Every other case passes with `EXAMINED: 0 ... asserts nothing`.
  - **This research gate is red by construction for a carry-only batch.** T-102 searches nothing and admits nothing, so section 6's "the research gate" cannot go green. The file does not say which cases are expected red, or how to record `CO1-NOT-APPLICABLE` (finding 15).
  - R12 is in the R2 baseline; here it passes against the scratch DB.
- **`test_db_integrity`** (G04, test 7): `214 examined`, 57/57.
- **`emit_batch_sql --selftest`:** 19/19.
- **`test_assess_cell_pilot` (T-055 gather):** T055-01 to T055-07 PASS.
- **`context_map.py --check`:** `EXAMINED: 1`.
- **Section 6's session-stamp proof,** run per table:
  - `extraction_lens_links`: (26,)
  - `source_value_extractions`: (3,)
  - **`base_taxonomy_identity`: `no such column: created_by_session`.** The children carry no session at all.
  - **`identity_icf_map` and `evidence_population_match`: `no such column: updated_by_session`.**
  - The command fails for three of the five tables this task writes (finding 14).
- **`preflight.sh` was not run.** This partial pilot changes no tracked file of its own: the rows live only on the scratch copy, and the scratch migration was deleted. A diff-scoped gate against `$BASE` would examine only the predecessors' commits, so it says nothing about T-102 (CLAUDE.md §1: ask what a run proves). I record this as a departure from brief item (4).

## Before/after table (the checks named)

| Check | Before (`base.db`) | After (`s.db`) |
|---|---|---|
| after-test (3) | EXAMINED 170 / 28 | EXAMINED 164 / 24 (22 unsampled + 2 judged) |
| after-test (5) | EXAMINED 1 / 0 (not red) | EXAMINED 4 / 0 |
| G04 lens per figure | 214 examined ✓ | 214 examined ✓ |
| A14 grades → identity | 61 examined ✓ | 63 examined ✓ |
| research_batch_dod | n/a | R1, R9a, R9b ✗ (by construction) |
| emitted-order replay | — | FAIL (UNIQUE ux_extraction_lens_live) |
| reordered replay vs scratch | — | IDENTICAL, 5 tables |

## Sweep (section 5)

- The command uses `git grep -n -F -e "$V"` with no `-w`. For `MOB` that matches 117 files (`MOBILITY` and the like); with `-w` it is still 117. For `SCI` it matches 41 files, 37 with `-w`. As written, the sweep cannot be read row by row for a two- or three-letter code.
- The old display string appears in 0 files. `WHEEL`, `WALKAID` and `LLD` appear in 0.
- **One caller contradicts the design, and it is doctrine, so I listed it rather than editing it.** `governance/population-taxonomy.md`:
  - Line 34 lists `MOB/AMB, MOB/UPL` as MOB's sub-codes. AMB is not minted, and UPL is outside mobility.
  - Line 75 says "**a sub-code inherits all evidence from its parent**". That is the opposite direction to design §5, where the parent gathers its children and a child gathers only itself.
  - Line 77 says a sub-code's range is always a subset of its parent's.
  - Line 81 says BPC research uses `MOB/AMB`.
  - Changing these is population taxonomy, which is the owner's call. The design's §11 allows only a one-line pointer.

## Code size

`git diff --shortstat origin/claude/peaceful-noether-kvf3sf -- scripts schemas .github skills ':!scripts/migrations'` counts only the predecessors' changes. T-102 changes no code, and `$OUT/T-102.patch` is an empty note.

## The five brief items

1. **Only CLAUDE.md, the task file and the design were followed:** held. I also read the predecessor patches and `db.py` source, which the coordinator required. I read the T-018 design only to check a flag name.
2. **The evidence command printed what the file says:** held. The 4a counts command did not (finding 1).
3. **Red before, green after:**
   - Test (1): red before, green after (on the scratch copy).
   - Test (3): red before. After is partial: a sample was carried, and 2 deliberate judged MOB links will always remain.
   - Test (5): **not red before** (finding 5).
   - Tests (9) and (1)'s SCI clause cannot run without T-054.
   - Emitted-order replay: red. That is an emitter defect, not a task defect, but it blocks the file's write path.
4. **The gate ran once:** not run, for the reason given above. Every named check's `EXAMINED:` is listed above.
5. **Patch and report saved:** held.

## Task-file defects

1. **4a's "counts today" command reads `source_value_extractions.identity_code`, which T-018 NULLs.** It prints `('source_value_extractions', 0)` while 3 live SCI figures exist. Corrected: `select count(*) from v_live_lens_links where identity_code='SCI'`.
2. **Write path blocked: the emitter writes INSERTs before UPDATEs within a table**, and `ux_extraction_lens_live` refuses the judged link while the carried one is still live. Evidence:
   - The emitted-order replay fails.
   - `migrate_db.py --rebuild` fails: `ERROR applying data_..._t102-pilot: UNIQUE constraint failed: index 'ux_extraction_lens_live'`.
   - Every "keep MOB, judged" row (design §6, three of the table's rows) takes this path.

   The fix is tooling: emit UPDATEs that retire rows before INSERTs into a table carrying a partial unique index, or a T-018 follow-up. Rule 10 puts that fix in a tooling PR before T-102, and section 2 should name that PR as a precondition. The emitter selftest (19/19) has no case for it.
3. **Section 2's flags do not match the stack, and section 9 would stop an executor at the first `add-identity` call.**
   - The folded file and design §9 name `add-identity ... --approval-ref` with `dbcore.require_approval_heading`. The T-025 patch has `--ledger-pointer` with `require_ledger_quote_once`, and `require_approval_heading` does not exist.
   - Design §9 names `add-lens-link --basis/--basis-text`. The T-018 patch has `--lens-basis/--lens-basis-text`, and the T-018 design is inconsistent with itself (line 136 `--lens-basis`, line 142 `--basis`).
4. **Every after-test command is hard-coded to `data/guidebook.db`.** Run as written on a scratch batch, it tests the unchanged canonical copy. A corrected file passes the DB path as an argument (as §6's heuristic does with `"$SCRATCH/s.db"`) and says which copy each test runs on: scratch before emit, migrated after.
5. **Test (5) cannot go red on the defect item 5 fixes.** Before: `EXAMINED: 1`, no hits, while MOB's name still reads "...; wheelchair users". The corrected test also asserts that MOB's `display_name` contains no `;`, and no child code's or device word (`wheelchair`).
6. **Test (3) can never reach 0 under the design's own table, and it misses abbreviations.**
   - E2 keeps scooter users on MOB, so a figure naming wheelchair and scooter users (196) keeps a judged MOB link whose text matches `wheel ?chair`. A row naming walking-aid users beside a no-device group (55) does the same.
   - The regex misses "MWC" (ext 12, "propelled a MWC", was not counted before the carry).
   - Corrected: the test counts only **carried** MOB links, or excludes judged MOB links whose `basis_text` names a scooter or no-device group. It adds `\bMWC\b` and `\bPWC\b`.
7. **Item 3 / design §7.3 give no `--mechanism` for the seven children's crossings**, and `add-population-icf-link` requires one. The executor must guess, which is a section 9 stop. The design should state each mechanism.
8. **The decision table contradicts itself for a figure naming wheelchair users and scooter users** (ext 196). "Several of these: one link per child; `mixed`; retire MOB" conflicts with "scooter users: keep MOB". The table needs a row for a figure naming a child group and a group that stays on the parent (keep both, judged).
9. **The table is keyed on "names wheelchair users", but the children are defined by device.** A figure naming only the device ("propelled a MWC"), with proxy participants (able-bodied, REF-00983), falls between the "wheelchair users" row and test 3's exception ("mentions a chair without naming its users"). The table should say whether naming the device is enough to warrant the child.
10. **No `device_class` value exists for an unspecified walking aid.** Ext 55 names "walking aid users" with no kind, and the table says "the matching `device_class`". There is none: `walker_rollator`, `crutches` and `cane` are each a kind. The file should say to leave it NULL.
11. **A figure naming people with a level (quadriplegics, hemiplegics) beside a device group** (55) has no row in the table. I placed it by device and left the level in the quote, because `base_taxonomy_medical` holds 0 rows. The table should say so.
12. **Design §2/§6a state that "every figure filed under SCI today names 'wheelchair users with cervical cord injury'".** That is false: only ext 158 does. Exts 159 and 160 say "subjects with cervical cord injury" or nothing. §6a.1's "where its words name wheelchair users → `named_in_text`" therefore does not fit 159 and 160. They need `study_participants` (which works: the grade's study_population holds the words).
13. **§6a.3's "a row the table's UNIQUE refuses already exists on WHEEL" never fires**, because the UNIQUE key is `(identity_code, icf_code, mechanism)` and the SCI rows' mechanism ("Biomechanical + autonomic") differs from item 3's. A dry-run of SCI link 22 (d410) → WHEEL was accepted beside item 3's WHEEL d410. Test 9's "no `(identity_code, icf_code, mechanism)` repeats" passes trivially while WHEEL holds d410 twice. The test should check `(identity_code, icf_code)`, and §6a.3 should say "if WHEEL already holds the ICF code (any mechanism), retire the SCI row naming it". Copying "Biomechanical + autonomic, high_predictive" onto a device-defined code is also doubtful: the autonomic mechanism is the injury's, not the wheelchair's.
14. **Section 6's session-stamp proof fails for three of the five tables written.** `base_taxonomy_identity` has no `created_by_session` (the new codes carry no session at all). `identity_icf_map` and `evidence_population_match` have no `updated_by_session`, so the command raises `no such column`. The command needs a per-table form.
15. **`research_batch_dod.py` is named as "the research gate", but it is red by construction for a carry batch:** R1 (no Co-1 pass), R9a and R9b ("admitted no sources AND logged no searches"). The file must say which cases are expected red for a no-search batch, and how to record `CO1-NOT-APPLICABLE` (in which table's `findings_note`, through which verb), or name a different gate.
16. **Test 1's SCI clause (`superseded_by_identity`) and test 9's `identity_icf_map ... retired_at` query error in this stack.** Neither column exists until T-054. The file lists T-054 as a precondition, but the stack the coordinator assembled for P7 lacks it, so 4a and tests 1 and 9 cannot run. The file has no partial path: it should say "if T-054 is absent, do items 3 and 4, carry the SCI figures and grade, and stop before the crossings and the code".
17. **No check refuses a MOB determination on a design-inequivalent parameter** (ramp gradient, parameter 3). The T-055 parent gather would gather WHEEL, WALKAID and MOB figures into one cell. The file defers this to T-110 without saying T-110 must precede any MOB determination.
18. **The section 5 sweep command has no `-w`,** so `MOB` matches 117 files and `SCI` 41. That is unreadable as a caller list. The expected caller `governance/population-taxonomy.md` contradicts the design:
    - Line 75 says "a sub-code inherits all evidence from its parent", the opposite of design §5.
    - Line 34 names `MOB/AMB, MOB/UPL`.

    Correcting it is doctrine. The file should name it as an owner item, not a sweep repair.
19. **The task file's set-up block copies `t.db` "for probes"** that no step uses: every probe in sections 6 and 8 reads `data/guidebook.db`. Its `BASE` derivation would pick a stale base on this clone (overridden per the brief).
20. **The design's LLD description is marked "PROPOSED, owner confirms".** The ninth set selected the name, and no ledger line confirms the description. A real executor must either stop or note it. I used the design text.
21. **(Stack, not this file.)** T-024's patch cannot be applied by `git am` or `git am --3way` onto a stack containing T-008-repilot and T-055. It conflicts in `_AMENDABLE_SVE_FIELDS` and `context-map.yaml`. The fold must take the union of the amendable fields (`value_as_written`, `device_class`, `jurisdiction`).
