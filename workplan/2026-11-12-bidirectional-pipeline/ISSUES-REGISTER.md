# Issues to file as gaps: what is still unresolved after the three 2026-11 tooling stacks

_Compiled 2026-11-20 (UTC) by an Opus-class compiler on the owner's typed instruction "Create a register with all issues logged that have yet to be resolved if it doesn't exist already", as changed the same day by "shouldn't we just write all of this to gaps table because we already have tools pointed there" and a request for resolution provenance. Checked at `db1fadc5`. Canadian spelling. No count is typed: each is a command or a listing stamped "generated; re-run rather than trust"._

**Status 2026-11-20: filed.** This file is the planning input of the data batch `session_2026-11-20-file-open-issues-as-gaps`, and the `gaps` table now holds its rows. The rows filed are `scratchpad/session_2026-11-20-file-open-issues-as-gaps/gap-batch-final.tsv` (the ISS rows of section 2 re-verified, plus the unresolved critic findings that section 3 had planned for `adversarial_findings`, a route closed because `record-adversarial-pass` takes one pass per batch). Read the table, not this file: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);[print(*r,sep=' | ') for r in c.execute(\"select gap_id, category, priority, status, substr(description,1,120) from gaps where created_by_session = 'session_2026-11-20-file-open-issues-as-gaps' order by gap_id\")]"`. The body below is kept as written on 2026-11-20 and is not maintained, except section 5.

**Corrected refile, same day, twice.** The first filing (`1a0793ba`) and the first correction (`de60aa94`) were both withdrawn: the database blob is restored to the pre-batch parent `9e434dca` and both batch migration files removed, then the corrected list is refiled through the same write path as one fresh migration. A row that stems from a critic finding takes that finding's own severity (CRITICAL and HIGH P1, MEDIUM P2, LOW P3), matched to the SAME finding and quoted verbatim (its `claim_attacked`, verdict, severity and index) in `scratchpad/session_2026-11-20-file-open-issues-as-gaps/gap-batch-final-severity.tsv`, which also gives the reasoning for every row priced by the rule and every cell left blank. Descriptions are one fact each; GAP-076 is closed against OD-47's ratified line and carries a note pointing at GAP-087. Count the rows and their split, never trust a typed figure: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);[print(*r) for r in c.execute(\"select category, priority, count(*) from gaps where created_by_session = 'session_2026-11-20-file-open-issues-as-gaps' group by 1,2\")]"`; rows still prefixed `[UNVERIFIED-OPEN`: the same query with `and description like '%UNVERIFIED-OPEN%'`.

**What the gates did not see.** No gate reads a `gaps` row for truth (GAP-069 states the class). The registered `research_dod_session` expands `@SESSION@` from `sessions/LATEST-RESEARCH`, which names another session, so the preflight PASS examined no row of this batch. The four `/batch-done` gates, run on this session with their true exit codes, examine nothing but the refusal record; `research_batch_dod` exits 1 by design here, because a gap-only batch logs no search and admits nothing (R1, R9a, R9b).

**Disclosures, not gaps.** The T-029 executor's deletion of its batch's `refusals.jsonl` (S18 T-029 item 4) and the critics' `rm` in a shared scratchpad (S18 T-030 item 6, T-134 item 5) are past events that cannot be resolved: they belong in the session record and the pull request body, not in gap rows (section 4, history). This batch's own command log is incomplete: the executor commands run while `scratchpad/session_2026-11-20-file-open-issues-as-gaps/commands.jsonl` was copied out and restored around the first revert (the backup and the revert among them) are absent from it; their record is the transcript `transcripts/harness_82388ac1/subagents/2026-11-20T03-56-40_other_a08e89ad.jsonl`.

**What this file is.** It is a **planning input for a later data pull request**, not a standing register. The standing register is the database: the `gaps` table (written by `db.py add-gap`, read by the refusal gate, `research_protocol_audit`, `gap_mining_audit` and `assess_cell`) for issues that no critic raised, and the `adversarial_findings` table (written by `db.py record-adversarial-pass` and `dispose-adversarial-finding`) for findings a critic raised. Rows are data, so they go in a data pull request, never in the tooling pull request #240 (CLAUDE.md rule 10). Once those rows are filed, this file is **regenerated from the tables and never kept by hand**. The rows ready for `db.py add-gap` are in `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/gap-batch.tsv`, one line per ISS row of section 2.

## 1. Does a register already exist?

Yes, in five places. None of them is the single list of what is still open:

- **The `gaps` table** of `data/guidebook.db`: `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('select status, count(*) from gaps group by 1').fetchall())"`. It has no row for any finding of the 2026-11 tooling stacks; section 7 lists its open rows.
- **The owner decision register**, `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md` section 8 (OD-nn), read through each decision's last `STATUS:` line in `references/project-standards.md`. Every OD now reads answered, or delegated with a satisfied CHECK (OD-16 withdrawn); derive it with the ledger's gate, `grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`. The only ledger status still open is OR-5b's (`grep -n -F "OR-5b STATUS" references/project-standards.md`).
- **`workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md`** (OI-nn), classed A to E and R. Its own command lists the open rows.
- **`workplan/2026-08-11-reconciled-findings-register.md`** (historical, August 2026) and **`_archived/gap_register*.md`** (archived).

**How this file differs.** It is the one index of what is unresolved across them, plus the design questions, open points and limits the 2026-11 tooling stacks recorded only in sweep lists, task files and repair commits. It points to each record and replaces none. Section 2 lists the issues that no critic raised, which go to `gaps`. Section 3 lists the critics' passes, which go to `adversarial_findings`.

**Read in full:** CLAUDE.md; the three sweep lists (abbreviated below: **S15** `scratchpad/session_2026-11-15-remediation-stack/sweep-list.md`, **S16** `scratchpad/session_2026-11-16-remediation-batch-1-tooling-stack/sweep-list.md`, **S18** `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/sweep-list.md`); **ADJ3** `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md`; **B1N** `workplan/2026-11-12-bidirectional-pipeline/BATCH-1-EXECUTION-NOTES.md`; the task file T-027; the ledger's status lines and its tail from the ratification of 2026-11-19 on; the repair commits on the branch (`git log --format='%h %s%n%b' origin/main..HEAD --grep='repair'`). **Other abbreviations:** **OIP** is `OPEN-ITEMS-PLAN.md` (rows with class A to D and O read in full; the list of class-E rows read, their bodies skimmed); **LEDGER** is `references/project-standards.md`; **TASKS** is `workplan/2026-11-12-bidirectional-pipeline/tasks`.

[SKIPPED: T-135 to T-143 sections 1 to 8: headings, sections 9 and 12, open points and the change items carrying a reading were read, not every line, for size (`wc -w workplan/2026-11-12-bidirectional-pipeline/tasks/T-13[5-9]*.md workplan/2026-11-12-bidirectional-pipeline/tasks/T-14[0-3]*.md`).] [SKIPPED: `references/project-standards.md` before line 7967: searched by `STATUS:`, `CHECK:` and id, not read end to end (the file is too large to read at once).] [SKIPPED: the critics' transcripts: read for their prompts and their closing JSON blocks only, by the command of section 3.]

## 2. The issues no critic raised (to file as gaps)

**What counts.** An unanswered owner question; a design question or author's reading awaiting confirmation; an executor-reported defect no commit repaired; a hole (a ratified fix no task carries, or an author's open point); a data gap with no task; a standing limit. Nothing repaired is listed; a row whose repair could not be checked starts `[UNVERIFIED-OPEN: …]`. An authored, unexecuted task is work, not an issue: T-136 to T-143 appear only through their open points.

**Columns.** Props: W walkability in every direction, L a dynamic base across all languages, S one source serving many parameters, P provenance. Severity is blank where no recorder gave one. **Closes with**: the resolving task, owner act or commit, for the `resolution_ref` the table is to gain (with `resolved_at`, `resolved_by_session`, in a tooling change that merges first). Grouped by kind, owner questions first; within a kind, rows holding a task or a live act first.

Count the rows by kind: `grep -o -E '^\| ISS-[0-9]+ \| [^|]+ \| [A-Z-]+ \|' workplan/2026-11-12-bidirectional-pipeline/ISSUES-REGISTER.md | awk -F'|' '{print $4}' | sort | uniq -c`.

### Owner questions

| ISS | Issue | Kind | Stage | Props | Severity | Recorded | Closes with | First logged |
|---|---|---|---|---|---|---|---|---|
| ISS-001 | Whether 'Ratify all' covers every resolution of the third adjudication, design questions included, is an unconfirmed assumption; OD-17 was ratified without the owner being shown the contract diff | OWNER-QUESTION | tooling | P |  | LEDGER :: Owner ratification 2026-11-19 (ACTION (3), the breadth of "all" is the first to confirm) | the owner | 2026-11-19 |
| ISS-002 | The judgment stage's anchor in the pipeline contract still places the determination machine in judgment; the ratified text edit (adjudication item 68) has no task, and the contract was ratified before it was made | OWNER-QUESTION | tooling | W |  | governance/pipeline-contract.yaml :: Correction 2026-11-19 to the note above | the owner, then no task | 2026-11-15 (S15 T-002/T-042) |
| ISS-003 | How a Co-1 source is shown academically sound is answered only in part: what 'academic rigour re PubMed' means, how a disabled people's organisation's statement or lived-experience publication is shown sound, and whether the test reaches every tier; the Co-1 boundary step has no task until then, and the ratified split of the three edges into registered items was not made | OWNER-QUESTION | judgment | P |  | LEDGER :: OR-5b STATUS; OIP :: OI-51, OI-52, OI-55 (8); ADJ3 :: 67. OR-5b: close or split | the owner, then a task for the Co-1 boundary (no task) | 2026-11-13 (tenth set) |
| ISS-004 | With the medical lens deleted, where a spinal cord injury and its level are held, and whether SCI is still retired into WHEEL | OWNER-QUESTION | base |  |  | LEDGER :: Correction 2026-11-16 — to the entry that deletes the medical lens; OIP :: OI-77 | the owner; T-102 waits | 2026-11-16 |
| ISS-005 | How a carry-only research batch (searches nothing, admits nothing) is gated, since the session definition-of-done check is red by construction on it | OWNER-QUESTION | research | W |  | OIP :: OI-55 (1) | the owner; T-081, T-082, T-084 and T-102 wait | 2026-11-13 |
| ISS-006 | The population taxonomy says a sub-code inherits its parent's evidence, which the 2026-08-25 ruling contradicts | OWNER-QUESTION | base |  |  | OIP :: OI-55 (2); TASKS/T-102-design.md :: E6 | the owner | 2026-11-13 |
| ISS-007 | The mechanisms of the mobility family's ICF crossings in the T-102 design are not confirmed | OWNER-QUESTION | base |  |  | OIP :: OI-55 (3); TASKS/T-102-design.md :: §7.3 (E7) | the owner | 2026-11-13 |
| ISS-008 | Whether a gentler value that holds only under a condition may leave the headline in favour of a steeper unconditioned one (OR-2 says yes; the 2026-10-30 rulings say the gentlest value is the gentlest) | OWNER-QUESTION | specification |  |  | OIP :: OI-55 (9) | the owner | 2026-11-13 |
| ISS-009 | What a typed name or alias table for lens codes would hold, so a lens link's warrant can be checked as naming the group (many ICF titles are empty; access needs have no name column) | OWNER-QUESTION | judgment | L P |  | OIP :: OI-55 (11) | the owner | 2026-11-13 |
| ISS-010 | Whether the engine should link figures outside a cell's lens as excluded at all: those rows restate what the live lens view says and couple every cell to every figure of the parameter | OWNER-QUESTION | specification | W |  | OIP :: OI-55 (12) | the owner | 2026-11-13 |
| ISS-011 | The engine's 'presumed echo' report line (prior workplan T-8 step 3) has no task: confirm the decline or ask for the task | OWNER-QUESTION | synthesis |  |  | OIP :: OI-58 (19) | the owner | 2026-11-13 |
| ISS-012 | Five live condition edges run from a parameter-12 claim to a parameter-3 claim, making the parameter-12 row a branch and leaving its parameter-3 partner in the headline; the data repair needs an owner | OWNER-QUESTION | judgment | S |  | OIP :: OI-56 (What remains), OI-58 (20) | the owner, then a research pull request (no task) | 2026-11-13 |
| ISS-013 | The scope status of a language-jurisdiction pair as the bucket table OR-8 asked for came through a blanket reading marked as an assumption: confirm | OWNER-QUESTION | research | L |  | OIP :: OI-58 (21) | the owner | 2026-11-13 |
| ISS-014 | The age at which a standing deferral becomes a defect is not set (T-079 builds the measure, no gate reads it) | OWNER-QUESTION | research | W |  | OIP :: OI-58 (22) | the owner | 2026-11-13 |
| ISS-015 | The owner kept unverified sources with a warning mark, but the figure writer refuses any source not verified, so no new value from such a source can be recorded | OWNER-QUESTION | judgment | P |  | OIP :: OI-71 | the coordinator; the owner if the reading is questioned | 2026-11-14 |
| ISS-016 | Whether the latest adjudication of an observation governs the alias resting on it, and whether dropping the alias's observation pointer (ending the re-judgment check) is accepted | OWNER-QUESTION | base | P |  | B1N :: T-069 / T-074; TASKS/T-136-base-grounding-absorbed.md :: §9 O-2 | the owner | 2026-11-16 |
| ISS-017 | A parameter's absorbed direction warrant is checked for form only and the direction is write-once: is a stronger test or a correcting verb wanted | OWNER-QUESTION | base | P W |  | TASKS/T-136-base-grounding-absorbed.md :: §9 O-1 | the owner | 2026-11-19 |
| ISS-018 | A quantity-kind quote whose value is written in words or as a fraction in words has no deterministic reading and no judged route, so the number-and-unit test is not built where such figures exist | OWNER-QUESTION | base | L |  | TASKS/T-137-units-and-kinds-as-data.md :: §9 O-1 | the owner | 2026-11-19 |
| ISS-019 | A unit whose defining statement gives its factor only in words, or with an ambiguous numeral, has no route into the unit table: is a judged factor wanted | OWNER-QUESTION | base | L |  | TASKS/T-137-units-and-kinds-as-data.md :: §9 O-2 | the owner | 2026-11-19 |
| ISS-020 | Refusing a context lens where the clause names the group is built on the task author's reading (a recorded name of that identity in the clause), not the literal reading | OWNER-QUESTION | judgment | P |  | TASKS/T-138-lens-and-figure-refusals.md :: §9 O-1 | the owner or the coordinator | 2026-11-19 |
| ISS-021 | Once ALL is refused, a clause below tier 4 that names no one has no identity route: the ratified floor exception of OD-47 has no tooling task | OWNER-QUESTION | judgment | W |  | TASKS/T-138-lens-and-figure-refusals.md :: §9 O-2; ADJ3 :: 3. OD-47 (F) | the owner, then no task | 2026-11-19 |
| ISS-022 | Refusing lens changes under a live determination freezes every figure the determination links, so adding a new group's link to any figure of the parameter first needs every live cell retired | OWNER-QUESTION | judgment | W |  | TASKS/T-138-lens-and-figure-refusals.md :: §9 O-3 | the owner | 2026-11-19 |
| ISS-023 | The displayed-name task is written to run before the research batch that attests forms, which departs from the ratified order | OWNER-QUESTION | base | L |  | TASKS/T-142-displayed-name-rule.md :: §2 The order against T-107 | the owner; T-142 stops until answered | 2026-11-19 |
| ISS-024 | Whether a rotation angle (a door's opening angle) is a quantity kind of its own or out of scope | OWNER-QUESTION | base |  |  | TASKS/T-143-degrees-rule.md :: §4 item 2a, open point | the owner | 2026-11-19 |
| ISS-025 | A source's edition shorter than a punctuation-delimited segment in a script written without spaces cannot be recorded by the boundary rule | OWNER-QUESTION | evidence | L P |  | TASKS/T-027-source-identity-edition.md :: §12.7 Correction 1, OPEN POINT | the owner or the coordinator | 2026-11-19 |

### Design questions

| ISS | Issue | Kind | Stage | Props | Severity | Recorded | Closes with | First logged |
|---|---|---|---|---|---|---|---|---|
| ISS-026 | The parameter merge keeps re-pointing rows until T-059 instead of taking the merge-row shape now; the task author's reading awaits confirmation | DESIGN-QUESTION | base | S P |  | TASKS/T-139-amendment-record.md :: §4 item 5, OPEN POINT | the coordinator or the owner, before T-139 item 5 | 2026-11-19 |
| ISS-027 | How a determination stores a bound governed by an angle with no exact gradient value, and what warrants a tangent unit: two readings for the coordinator to confirm | DESIGN-QUESTION | specification | L |  | TASKS/T-143-degrees-rule.md :: §4 item 3 (Storage, per bound) and item 4 | the coordinator, before T-143 item 3 | 2026-11-19 |
| ISS-028 | A topic-area code is accepted in any script with only a trim test: the task author's reading awaits confirmation | DESIGN-QUESTION | base | L |  | TASKS/T-135-domain-vocabulary.md :: §12.7 Correction to 12.3 item 1 | the coordinator | 2026-11-19 |
| ISS-029 | A source-identity value may not be the whole of the words that state it: the task author's reading awaits confirmation | DESIGN-QUESTION | evidence | P |  | TASKS/T-027-source-identity-edition.md :: §12.7 Correction 1 (the author's reading, for confirmation) | the coordinator | 2026-11-19 |
| ISS-030 | Two readings of the displayed-name rule are the task file's own, among them which spelling shows when two spellings tie inside the winning group | DESIGN-QUESTION | base | L |  | TASKS/T-142-displayed-name-rule.md :: §4 item 3e (This file's reading) | the coordinator | 2026-11-19 |
| ISS-031 | Whether the harm test also supplies the synthesis approach for a divergence within one rank (T1 against T1, Co-1 against T1) | DESIGN-QUESTION | synthesis |  |  | OIP :: OI-66 | T-059's executor, then the owner | 2026-11-14 |
| ISS-032 | No ICF hierarchy exists, so a figure keyed on a child code does not reach a cell keyed on its parent; whether parent cells gather children is not decided | DESIGN-QUESTION | judgment | W |  | OIP :: OI-76 | the coordinator (a tooling task after T-128 if wanted) | 2026-11-15 |
| ISS-033 | Whether a figure's jurisdiction column repeats its source's jurisdiction (a second home) | DESIGN-QUESTION | judgment | P |  | OIP :: OI-29 | T-024's executor | 2026-11-12 |
| ISS-034 | Whether the derived-figure writer should take the as-written wording | DESIGN-QUESTION | judgment |  |  | OIP :: OI-26 | T-008 | 2026-11-12 |
| ISS-035 | Whether ALL's successor is a second column or a generalised successor | DESIGN-QUESTION | base |  |  | OIP :: OI-32 | T-056's executor | 2026-11-13 |

### Defects

| ISS | Issue | Kind | Stage | Props | Severity | Recorded | Closes with | First logged |
|---|---|---|---|---|---|---|---|---|
| ISS-036 | Grey has two homes on a source (its evidence type and a grey flag with a reason) | DEFECT | evidence | P |  | OIP :: OI-67 | a tooling task after T-117 (not authored) | 2026-11-14 |
| ISS-037 | An access need's 'absorbs' cell holds a delimited list of populations and situations | DEFECT | base | L |  | OIP :: OI-75 | a tooling task (not authored) | 2026-11-15 |
| ISS-038 | The ratified scope of the existence gate (any source a figure or determination rests on) is tested by no check; the integrity audit tests neither predicate | DEFECT | tooling | P |  | S15 :: T-002 / T-042 (scope of the existence gate); ADJ3 :: 69 | no task | 2026-11-15 |
| ISS-039 | The cell-status read narrows open gaps by a gap's parameter column, which no live gap sets | DEFECT | tooling | W |  | S15 :: T-027 / T-034 / T-048 / T-054 NOT repaired (e) | no task | 2026-11-15 |
| ISS-040 | [UNVERIFIED-OPEN: the read verb was not re-run] The cell-status read does not model a BLOCKED scan status or a lens given twice, and an empty identity flag is unfiltered | DEFECT | tooling | W |  | S15 :: T-027 / T-034 / T-048 / T-054 NOT repaired (e) | no task | 2026-11-15 |
| ISS-041 | [UNVERIFIED-OPEN: the read verb was not re-run] The cell-status read matches two lens codes on figures whose codes sit on separate link rows, where the specification requires one row | DEFECT | tooling | W |  | S15 :: T-027 / T-034 / T-048 / T-054 NOT repaired (e) | no task | 2026-11-15 |
| ISS-042 | [UNVERIFIED-OPEN: the refusal texts were not re-read] Refusals for a deprecated code name a --needs flag on writers that have none, and the identity amending verb still edits a deprecated code | DEFECT | base |  |  | S15 :: T-027 / T-034 / T-048 / T-054 NOT repaired (d) | no task | 2026-11-15 |
| ISS-043 | The owner's page build reports a table with no gloss (base_jurisdictions) on every build | DEFECT | render |  |  | S15 :: T-003 (owner_browser_build.py prints) | no task | 2026-11-15 |
| ISS-044 | Prose still restates the old two-way mobility split and the old name of MOB | DEFECT | base |  |  | OIP :: OI-34 | T-102's executor; the owner for governance changes | 2026-11-12 |

### Holes

| ISS | Issue | Kind | Stage | Props | Severity | Recorded | Closes with | First logged |
|---|---|---|---|---|---|---|---|---|
| ISS-045 | A parent identity cell reads only its own ICF map rows while it gathers its descendants' figures; the ratified fix (read the descendants' rows) has no task | HOLE | judgment | W |  | ADJ3 :: 74. T-055; S15 :: T-076 / T-080 / T-090 NOT repaired (a); B1N :: T-067, T-055 follow-on | no task | 2026-11-15 |
| ISS-046 | No verb folds the letter case of a stored language column, so the ratified case fold cannot be written through the write path and its follow-on is blocked | HOLE | tooling | L |  | TASKS/T-141-small-repairs.md :: 63. Readers drop their case folds | a tooling task (not authored) | 2026-11-19 |
| ISS-047 | Nothing writes a decision's status, so baseline decisions the term plan superseded in prose stay ACTIVE | HOLE | tooling | P |  | OIP :: OI-61 | no task (to be filed by a research batch) | 2026-11-14 |
| ISS-048 | No writer reaches the subject table of an adversarial finding, so rows naming a renamed table cannot be moved | HOLE | tooling | P |  | OIP :: OI-70 | after T-118 (no task) | 2026-11-14 |
| ISS-049 | The element determination has no design file, so nothing of it can be built | HOLE | specification |  |  | OIP :: OI-53 | an Opus-class design session (no task) | 2026-11-13 |
| ISS-050 | The typed circumstance carrier has no design file, so 'the same lens and context' has only its lens half built | HOLE | judgment |  |  | B1N :: Stopped, and why (T-091); OIP :: OI-69 | T-091 (design file missing) | 2026-11-14 |

### Data gaps

| ISS | Issue | Kind | Stage | Props | Severity | Recorded | Closes with | First logged |
|---|---|---|---|---|---|---|---|---|
| ISS-051 | The owner-approved term 'barrier-free path of travel' has not been minted | DATA-GAP | base | L |  | OIP :: OI-12 | a research pull request (no task) | 2026-11-13 |
| ISS-052 | The declination of bodies of law and cost terms as parameters, ratified, is not written | DATA-GAP | base |  |  | S15 :: T-010; ADJ3 :: 59 | a research pull request (no task) | 2026-11-15 |
| ISS-053 | MOB's high-predictive ICF crossings are flagged as overstated and no task re-judges them | DATA-GAP | base |  |  | OIP :: OI-22 | a research task after T-102 (no task) | 2026-11-12 |

### Limits

| ISS | Issue | Kind | Stage | Props | Severity | Recorded | Closes with | First logged |
|---|---|---|---|---|---|---|---|---|
| ISS-054 | No live determination exists, so acceptance tests that need one cannot run | LIMIT | specification |  |  | OIP :: OI-19 | after T-110 | 2026-11-12 |
| ISS-055 | Paths no stress round exercised: candidate staging to admission, a citation-mining row, merging or declining a parameter with figures, a non-English source end to end | LIMIT | tooling | W |  | OIP :: OI-28 | no task | 2026-11-12 |
| ISS-056 | The general reason check was not tightened against zero-width text; only the figure retirement verb refuses it | LIMIT | tooling | P |  | cd778176; 9d2985a8 | no task | 2026-11-19 |
| ISS-057 | A directory-naming glob overrides the .ignore negation (a harness property) | LIMIT | tooling |  |  | S15 :: T-076 / T-080 / T-090 NOT repaired (c) | none (harness) | 2026-11-15 |
| ISS-058 | A thinness grade cannot be derived for a cell keyed only on ICF or access-need codes | LIMIT | synthesis |  |  | OIP :: OI-68 | a research batch files it; then a design if wanted | 2026-11-14 |
| ISS-059 | The owner's page cannot be built or tested in this environment (it needs the sql.js wasm download) | LIMIT | render |  |  | S15 :: T-003; TASKS/T-141-small-repairs.md :: §9 item 71 (b) | none here | 2026-11-15 |
| ISS-060 | /simplify deferrals: the searched-pairs rule held by three readers, a shared insert helper, the amendable per-field spec and others | LIMIT | tooling |  |  | S15 :: /simplify of the PR (2026-11-16) SKIPPED | no task | 2026-11-16 |
| ISS-061 | Two identical table-listing helpers have no shared home (to merge when either file is next touched) | LIMIT | tooling |  |  | S15 :: T-041; ADJ3 :: 56 | no task | 2026-11-15 |
| ISS-062 | [UNVERIFIED-OPEN: T-007 executed; the refusal was not probed] Whether adding a source refuses a NULL standing when a URL is given | LIMIT | evidence | P |  | OIP :: OI-25 | T-007 (executed) | 2026-11-12 |
| ISS-063 | [UNVERIFIED-OPEN: T-051 executed; the build was not run] How the owner's page build handles the cross-stage stage value | LIMIT | render |  |  | OIP :: OI-30 | T-051 (executed) | 2026-11-12 |
| ISS-064 | [UNVERIFIED-OPEN: the git grep was not re-run] 'provisional' aligned to OD-10 in live prose and its coverage meaning retired | LIMIT | tooling |  |  | OIP :: OI-35 | T-001 (executed) | 2026-11-12 |
| ISS-065 | [UNVERIFIED-OPEN: not checked] The doctrine-deltas file's reader and the term plan's incomplete checks | LIMIT | tooling |  |  | OIP :: OI-62, OI-64 | T-120, T-035 | 2026-11-14 |
| ISS-066 | [UNVERIFIED-OPEN: the section 3.1 map was not re-run] Acceptance tests covered by a task but not named by it | LIMIT | tooling |  |  | OIP :: OI-18 | the coordinator (plan edits) | 2026-11-12 |

## 3. To record as adversarial passes (not gaps)

**Why not gaps.** A critic's finding has a home with its resolution: `adversarial_findings` (disposition REPAIRED, REJECTED, PROVISIONAL-DISPUTED or OWNER-RULED; `disposition_ref`, `disposed_by_session`, `disposed_at`), written by `db.py record-adversarial-pass` and `dispose-adversarial-finding`. A gap row for the same finding would be a second home (CLAUDE.md rule 5). The data pull request records each pass below from the critic's closing JSON block. Repaired findings are disposed REPAIRED with the repair commit as `disposition_ref`; unrepaired ones stay undisposed, or OWNER-RULED where the 2026-11-19 ratification ruled them (ADJ3 section 2 maps them).

**Scope (a judgment, for the coordinator).** "This session" is read as a pass whose transcript is under `transcripts/harness_82388ac1/subagents/`. S15's critics ran in the earlier session, so S15's unrepaired items stay in section 2. Without the session bound, the rows whose "Recorded" cell starts `S15 ::` move here.

**Findings by verdict and severity, per critic transcript (generated 2026-11-20 02:37 UTC; generated; re-run rather than trust).** The command:

```
python3 -I - <<'PY'
import json,glob,re,collections
for f in sorted(glob.glob('transcripts/harness_82388ac1/subagents/*.jsonl')):
    L=[json.loads(l) for l in open(f) if l.strip()]
    T=lambda m:(lambda c:c if isinstance(c,str) else '\n'.join(x.get('text','') if x.get('type')=='text' else x.get('input',{}).get('message','') for x in c or [] if isinstance(x,dict)))((m.get('message') or {}).get('content'))
    p=next((T(m) for m in L if m.get('type')=='user' and T(m)),'')
    if not re.match(r'(Read-only\. )?(Attack|Adversarially review)',p): continue
    r=([T(m) for m in L if m.get('type')=='assistant' and T(m)] or [''])[-1]
    F=[x for b in re.findall(r'```(?:json)?[^\n]*\n(.*?)```',r,re.S) for x in (lambda j:j if isinstance(j,list) else j.get('findings',[]) if isinstance(j,dict) else [])((lambda s:json.loads(s) if s.strip().startswith(('[','{')) else [])(b)) if isinstance(x,dict)]
    c=collections.Counter(f"{x.get('verdict','?')}/{x.get('severity','-')}" for x in F)
    print(f.split('/')[-1][:19], f[-14:-6], ' '.join(f'{k}={v}' for k,v in sorted(c.items())) or 'NO-BLOCK')
PY
```

```
2026-11-16T18-08-10 a6ce1af7 NOT-ATTACKED/-=1 SURVIVED/-=4 SUSTAINED/HIGH=3 SUSTAINED/LOW=3 SUSTAINED/MEDIUM=3 WITHHELD-FOR-OWNER/-=2
2026-11-16T18-34-24 accc4fed NOT-ATTACKED/-=3 SURVIVED/-=4 SUSTAINED/HIGH=3 SUSTAINED/LOW=2 SUSTAINED/MEDIUM=3 WITHHELD-FOR-OWNER/-=1
2026-11-16T19-04-25 ae5ceb5b NOT-ATTACKED/-=4 SURVIVED/-=2 SUSTAINED/CRITICAL=1 SUSTAINED/HIGH=2 SUSTAINED/LOW=1 SUSTAINED/MEDIUM=2
2026-11-16T19-34-14 a854d244 NOT-ATTACKED/-=1 SURVIVED/-=2 SUSTAINED/HIGH=3 SUSTAINED/LOW=2 SUSTAINED/MEDIUM=4
2026-11-16T19-47-49 a2314e08 NOT-ATTACKED/-=2 SURVIVED/-=3 SUSTAINED/HIGH=2 SUSTAINED/LOW=2 SUSTAINED/MEDIUM=2 WITHHELD-FOR-OWNER/-=1
2026-11-16T20-12-10 aca829af SURVIVED/-=2 SUSTAINED/HIGH=2 SUSTAINED/LOW=4 SUSTAINED/MEDIUM=4
2026-11-16T21-02-05 aa49cdec NOT-ATTACKED/-=5 SURVIVED/-=4 SUSTAINED/HIGH=3 SUSTAINED/LOW=3 SUSTAINED/MEDIUM=4 WITHHELD-FOR-OWNER/-=1
2026-11-16T21-22-25 a3ca6ddf NOT-ATTACKED/-=2 SURVIVED/-=3 SUSTAINED/HIGH=3 SUSTAINED/MEDIUM=5
2026-11-16T23-29-23 aadcde62 NOT-ATTACKED/-=3 SURVIVED/-=4 SUSTAINED/LOW=2 SUSTAINED/MEDIUM=3
2026-11-17T00-00-03 a05f3777 NOT-ATTACKED/-=4 SURVIVED/-=3 SUSTAINED/HIGH=3 SUSTAINED/LOW=2 SUSTAINED/MEDIUM=3
2026-11-17T00-25-58 ab6fcba9 NOT-ATTACKED/-=3 SURVIVED/-=3 SUSTAINED/HIGH=3 SUSTAINED/LOW=1 SUSTAINED/MEDIUM=2
2026-11-17T00-56-01 affbe318 NOT-ATTACKED/-=2 SURVIVED/-=4 SUSTAINED/HIGH=2 SUSTAINED/LOW=1 SUSTAINED/MEDIUM=3
2026-11-17T01-55-05 aaa0c04b NOT-ATTACKED/-=2 SURVIVED/-=2 SUSTAINED/HIGH=3 SUSTAINED/LOW=1 SUSTAINED/MEDIUM=4
2026-11-17T02-43-02 a2ed7d9a NOT-ATTACKED/-=4 SURVIVED/-=3 SUSTAINED/CRITICAL=1 SUSTAINED/HIGH=1 SUSTAINED/MEDIUM=3
2026-11-18T19-38-09 af5360a9 NOT-ATTACKED/-=1 SURVIVED/-=3 SUSTAINED/HIGH=2 SUSTAINED/LOW=2 SUSTAINED/MEDIUM=3 WITHHELD-FOR-OWNER/-=1
2026-11-18T20-45-45 a5e322b7 NOT-ATTACKED/-=3 SURVIVED/-=3 SUSTAINED/HIGH=3 SUSTAINED/MEDIUM=4 WITHHELD-FOR-OWNER/-=1
2026-11-18T21-49-01 a9ccd809 NOT-ATTACKED/-=2 SURVIVED/-=3 SUSTAINED/HIGH=2 SUSTAINED/MEDIUM=5
2026-11-18T23-03-16 ad377f82 NOT-ATTACKED/-=1 SURVIVED/-=3 SUSTAINED/HIGH=4 SUSTAINED/MEDIUM=4
2026-11-18T23-59-06 ac174efc NO-BLOCK
2026-11-19T00-16-44 ac4adac3 NOT-ATTACKED/-=3 SURVIVED/-=1 SUSTAINED/CRITICAL=1 SUSTAINED/HIGH=2 SUSTAINED/LOW=2 SUSTAINED/MEDIUM=3
2026-11-19T02-04-35 a95a470c NOT-ATTACKED/-=1 SURVIVED/-=3 SUSTAINED/HIGH=3 SUSTAINED/LOW=3 SUSTAINED/MEDIUM=4
2026-11-19T02-56-13 a36e0be0 NOT-ATTACKED/-=2 SURVIVED/-=5 SUSTAINED/HIGH=3 SUSTAINED/LOW=2 SUSTAINED/MEDIUM=4 WITHHELD-FOR-OWNER/-=1
2026-11-19T04-46-26 a2b4d735 NOT-ATTACKED/-=1 SURVIVED/-=2 SUSTAINED/CRITICAL=2 SUSTAINED/HIGH=3 SUSTAINED/LOW=2 SUSTAINED/MEDIUM=3
2026-11-19T05-35-42 aa78dfbf NOT-ATTACKED/-=4 SURVIVED/-=3 SUSTAINED/HIGH=2 SUSTAINED/LOW=1 SUSTAINED/MEDIUM=6
2026-11-19T06-39-37 a2016a8d NOT-ATTACKED/-=1 SURVIVED/-=3 SUSTAINED/HIGH=3 SUSTAINED/LOW=3 SUSTAINED/MEDIUM=4
2026-11-19T23-31-46 a2853abe NOT-ATTACKED/-=2 SURVIVED/-=2 SUSTAINED/HIGH=3 SUSTAINED/LOW=2 SUSTAINED/MEDIUM=3
2026-11-19T23-31-46 a42ab055 NOT-ATTACKED/-=1 SURVIVED/-=2 SUSTAINED/HIGH=2 SUSTAINED/LOW=1 SUSTAINED/MEDIUM=8
2026-11-19T23-31-46 a43875ff SURVIVED/-=3 SUSTAINED/HIGH=2 SUSTAINED/LOW=2 SUSTAINED/MEDIUM=6
2026-11-19T23-31-46 a4e235a3 NOT-ATTACKED/-=2 SURVIVED/-=4 SUSTAINED/HIGH=4 SUSTAINED/LOW=3 SUSTAINED/MEDIUM=3
2026-11-19T23-32-25 a5c5b6ef NOT-ATTACKED/-=4 SURVIVED/-=6 SUSTAINED/HIGH=2 SUSTAINED/LOW=1 SUSTAINED/MEDIUM=9
2026-11-19T23-32-25 a8df4496 NOT-ATTACKED/-=3 SURVIVED/-=5 SUSTAINED/HIGH=3 SUSTAINED/LOW=5 SUSTAINED/MEDIUM=11 WITHHELD-FOR-OWNER/-=1
2026-11-19T23-32-25 ae372438 NOT-ATTACKED/-=2 SURVIVED/-=6 SUSTAINED/HIGH=4 SUSTAINED/LOW=4 SUSTAINED/MEDIUM=6 WITHHELD-FOR-OWNER/-=2
```

**The passes** (transcripts under `transcripts/harness_82388ac1/subagents/`):

| Task | Subject commit the critic read | Critic transcript | Repair commit | Not repaired (the record) |
|---|---|---|---|---|
| medical lens deletion | `5e1f8780` | `2026-11-16T18-08-10_other_a6ce1af7.jsonl` | `3e42a6e1` | the repair commit's message; OIP :: OI-77 (the SCI premise, ISS row in section 2) |
| T-061 | `bdf68c98` | `2026-11-16T18-34-24_other_accc4fed.jsonl` | `0708137b` | the repair commit's message |
| T-063 | `25feb853` | `2026-11-16T19-04-25_other_ae5ceb5b.jsonl` | `8ff98019` | the repair commit's message |
| T-067 | `5afd741b` | `2026-11-16T19-34-14_other_a854d244.jsonl` | `adb98816` | the repair commit's message |
| T-074 | `da86854a` | `2026-11-16T19-47-49_other_a2314e08.jsonl` | `2335149f` | the repair commit's message; B1N :: T-069 / T-074 (owner question, section 2) |
| T-075 | `0ccb7a38` | `2026-11-16T20-12-10_other_aca829af.jsonl` | `18601db2` | the repair commit's message |
| T-079 | `25a07958` | `2026-11-16T21-02-05_other_aa49cdec.jsonl` | `e045739c` | the repair commit's message |
| T-088 | `d4f0ef2a` | `2026-11-16T21-22-25_other_a3ca6ddf.jsonl` | `d47d2deb` | the repair commit's message |
| T-020 | `d1bfc280` | `2026-11-16T23-29-23_other_aadcde62.jsonl` | `087390b6` | S16 :: T-020 Not repaired (items 1 and 2 ruled as ADJ3 items 41 and 42, carried by T-137 and T-141) |
| T-022 | `1ca23587` | `2026-11-17T00-00-03_other_a05f3777.jsonl` | `b0c16a6a` | S16 :: T-022 Not repaired (items 1 and 6 stand as limits: carriers empty; B9 and B14 not ruled) |
| T-049 | `3818ed33` | `2026-11-17T00-25-58_other_ab6fcba9.jsonl` | `81768a93` | S16 :: T-049 Not repaired (items 2 to 5 carried by T-141; item 1 by T-037; item 6, the census, stands) |
| T-050 | `77f86902` | `2026-11-17T00-56-01_other_affbe318.jsonl` | `257c9d8e` | S16 :: T-050 Not repaired. **Items 1 and 3 are NOT repaired, though ADJ3 section 3 (79 to 91) records them closed.** `TASKS/T-050-retire-admission-edges-and-connections.md` "Amended 2026-11-17 (G13)" assigns a live view per table and `db.py connections --retired` to the sweep. Neither exists: `select name from sqlite_master where type='view' and (name like '%live_conn%' or name like '%live_admis%')` prints nothing, and `grep -c -- '--retired' scripts/db.py` prints 0. |
| T-089 | `d1d08b90` | `2026-11-17T01-55-05_other_aaa0c04b.jsonl` | `17e6e062` | S16 :: T-089 Not repaired (items 1 to 5 carried by T-141 items 51 to 53; item 7 stands: no real record, and "recurring signatures first" is not built) |
| T-093 | `84615350` | `2026-11-17T02-43-02_other_a2ed7d9a.jsonl` | `fd98a842` | S16 :: T-093 Not repaired. Items 1 and 2 stand. The premise note for T-093 section 3 and T-086 was not added: `grep -c -i "unproven" workplan/2026-11-12-bidirectional-pipeline/tasks/T-086*.md` prints 0. |
| T-028 | `4dc99ce3` | `2026-11-18T19-38-09_other_af5360a9.jsonl` | `ea4e7b18`, then `29c8b236` (OD-71) | S18 :: T-028 Not repaired (items 3 and 4 stand as limits: no committed proof of the junction remap; no attested alias, `select count(*) from term_aliases where attestation in ('instrument','other_source')`) |
| T-029 | `23cfaf16` | `2026-11-18T20-45-45_other_a5e322b7.jsonl` | `bf7a3575`, then `1c5e4ce9` (OD-71) | S18 :: T-029 Not repaired (items 2 and 3 carried by T-136; item 4, the lost probe record, and item 5, the census, stand) |
| T-030 | `bdecc47c` | `2026-11-18T21-49-01_other_a9ccd809.jsonl` | `4ee40b64` | S18 :: T-030 Not repaired (items 1, 3 and 7 carried by T-137; item 2 by T-143; item 5, units with no unit row, is research after T-137; item 6, the critic's `rm` in a shared folder, stands) |
| T-031 | `d9a0e3ed` | `2026-11-18T23-03-16_other_ad377f82.jsonl` | `ce0be07c` | S18 :: T-031 Not repaired. Item 3 stands: section 4 of the task file still keys a clause by `ref_id`, `awk '/^## 4\./{f=1} /^## 5\./{f=0} f' workplan/2026-11-12-bidirectional-pipeline/tasks/T-031-clause-unit-and-open-pass.md \| grep -n ref_id`. Item 2, the census, stands. |
| T-083 | `217d7af8` | `2026-11-19T00-16-44_other_ac4adac3.jsonl` (an earlier run, `2026-11-18T23-59-06_other_ac174efc.jsonl`, closed with no report) | `3caac402` | S18 :: T-083 Not repaired (items 2 and 3 carried by T-138; item 4, the locator CHECK hand-copied in three tables, has no task) |
| T-119 | `5829c4f6` | `2026-11-19T02-04-35_adversarial_a95a470c.jsonl` | `2228252c` | S18 :: T-119 Not repaired (item 1 closed by the session record of `6c12dd07`; items 2 and 3 stand; item 4 is T-120's; item 5 ruled) |
| T-126 | `017d1778` | `2026-11-19T02-56-13_adversarial_a36e0be0.jsonl` | `336685a2` | S18 :: T-126 Not repaired (items 1 to 3 ruled; item 5, the warnings and the CJK matcher, partly carried by T-138's amendment; item 7, unexamined paths, stands) |
| T-027 | `c9c84466` | `2026-11-19T04-46-26_adversarial_a2b4d735.jsonl` | `d6c19cbd` (revert) | S18 :: T-027 (commit c9c84466, REVERTED); carried by T-027 section 12 |
| T-078 | `1187ac12` | `2026-11-19T05-35-42_adversarial_aa78dfbf.jsonl` | `cd778176` | S18 :: T-078 Not repaired (item 7 repaired by `9d2985a8`; items 1 and 2 carried by T-138; item 3 by T-140; items 4 to 6 stand: INSERT OR REPLACE un-retires, unproven views, unexamined paths) |
| T-134 | `d33f091c` | `2026-11-19T06-39-37_adversarial_a2016a8d.jsonl` | `ee64bf80` | S18 :: T-134 Not repaired (items 1 to 3 carried by T-140; item 4 by T-120; item 5, the `rm` in a shared folder, stands) |
| T-083, second pass | `3caac402` | `2026-11-19T23-31-46_adversarial_a2853abe.jsonl` | `860718e6` | the message of `860718e6`, item 2. **U+034F (category Mn) is outside `dbcore.blank_chars()` and still passes**; closing it changes T-078's definition, and no task carries it. Items 4 to 6 are recorded only (T-136, T-137, T-138). |
| T-126, second pass | `336685a2` | `2026-11-19T23-31-46_adversarial_a42ab055.jsonl` | `3806b054` | the message of `3806b054` (T-138 item 2 amended) |
| T-134, second pass | `ee64bf80` | `2026-11-19T23-31-46_adversarial_a43875ff.jsonl` | `931bcc0f` | the message of `931bcc0f` |
| T-078, second pass | `cd778176` | `2026-11-19T23-31-46_adversarial_a4e235a3.jsonl` | `9d2985a8` | the message of `9d2985a8` (`require_reason` not tightened, a deviation the executor recorded; section 2 carries it) |
| task files T-142, T-143 and dated amendments | `a6c478e0` and the uncommitted task files | `2026-11-19T23-32-25_adversarial_a5c5b6ef.jsonl` | `558c5cad` | the corrections in each task file (`grep -n "Corrections 2026-11-19\|corrected 2026-11-19" workplan/2026-11-12-bidirectional-pipeline/tasks/T-14[23]*.md`) |
| task files T-027, T-135, T-139, T-140, T-141 | as above | `2026-11-19T23-32-25_adversarial_a8df4496.jsonl` | `558c5cad` | the "12.7 Corrections" sections and dated lines in those files |
| task files T-136, T-137, T-138 | as above | `2026-11-19T23-32-25_adversarial_ae372438.jsonl` | `558c5cad` | the corrections in those files; the critic's withheld readings are carried as the files' open points (section 2) |

**Not checked per finding.** Status comes from the repair commit and the sweep list named in each row. Only the T-050, T-031 and T-093 items were re-checked, by the commands shown.

## 4. Excluded from the gap batch, with their homes

- **Every registered OD decision.** The home is its ledger `STATUS:` line. The open OD questions were adjudicated in ADJ3 and ratified on 2026-11-19 (`grep -n -F "## Owner ratification 2026-11-19" references/project-standards.md`). **Corrected 2026-11-20 (what the batch did):** an issue that an authored task will repair but has not is NOT excluded; it is filed as a gap, with the task named in its description, because the owner asked for "all issues logged that have yet to be resolved" (the gap is the tracked issue, the task the plan's work item, and the gap's closing will point at the task). What stays excluded is the decision itself, once ratified, and an item a ratified decision settled with no work left. ADJ3 items 25 to 27, 70 and 72 were completed by the ratification entry and by `6c12dd07`.
- **Owner decisions already in the `gaps` table**: GAP-074, GAP-075 and GAP-077 (category DEC), and GAP-100 (none of them is on the owner's page). They are pointers, not new rows. **GAP-076** (the lens of a clause that names no one) asks the question OD-47 answered on 2026-11-19 (ratified). The data pull request may close it against that ledger entry.
- **Repaired since recorded, checked**: S15's zero-selection PASS (T-075); `repoint-extraction-relation` refusing a retired figure (`9d2985a8`); OI-06 (`awk '/^def rename_term/,/^def [a-z]/' scripts/db.py | grep -c AMENDED` prints 0); OI-27 (`ce0be07c` item 6); the state graph (`4f282c18`); the T-119 session record (`6c12dd07`); the DR-2026-07-21 marker; OD-71's quote question (B1N, correction of 2026-11-20).
- **Class-E rows of OIP accepted as standing limits or declined** (OI-05, 15, 16, 21, 37 to 47). They were accepted by their recorder with a reason, so they are not repeated here: `grep -E '^\| OI-[0-9]+ \|' workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md | grep -E ' \| E \| [^|]*\|$' | cut -d'|' -f2`. OI-61 and OI-68 are kept in section 2, because their recorder asked for a gap row that was never filed.
- **History that cannot change**: typed counts in committed migrations and commits (S16 T-020 item 3); frozen records (S15).

## 5. Mapping the register to the table: the judgments made

Vocabulary: the column's CHECK (`python3 scripts/db.py add-gap --help`). Meanings: how existing rows use each category (`python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);[print(*r) for r in c.execute('select category, gap_id, substr(description,1,90) from gaps order by 1')]"`) and from D-0144 in `scripts/migrations/057_baseline_2026-08-12.sql` (CONF for the conflict mapper, AUDT for the evidence auditor's findings). **GAP-290, the precedent the coordinator named, does not exist** (`select gap_id from gaps where gap_id like '%290%'` prints nothing). GAP-069 and GAP-095 (AUDT) serve as the tooling precedent.

- **OWNER-QUESTION, DESIGN-QUESTION and DECISION-PENDING map to DEC.** The existing DEC rows are open questions waiting on a decision (GAP-015, GAP-063, GAP-074 to GAP-077). An OD-registered question is excluded (section 4).
- **A DEFECT or HOLE in a writer, a view, the schema or the engine maps to SW.** The existing SW rows are writer and view defects (GAP-007, GAP-062, GAP-087).
- **A DEFECT or LIMIT in a check, an audit, a test, the state-graph instrument, plan text or process maps to AUDT.** The existing AUDT rows are gates that pass having examined nothing and process findings (GAP-020, GAP-069, GAP-095, GAP-101).
- **A LIMIT that is a property of a writer or a trigger maps to SW**, by the same reading as a defect.
- **A DATA-GAP in the base vocabulary or taxonomy maps to ST.** The existing ST rows are vocabulary and taxonomy rows (GAP-ICF-TITLES, GAP-H3-PCS-COLLISION, GAP-072). A prose defect about the population taxonomy (OI-34) is ST for the same reason.
- **No row maps to EG or RP** (no issue here is a parameter's evidence gap or a research-process finding).
- **Priority (corrected 2026-11-20, ledger correction of that date on critic findings that stand).** A row that stems from a critic finding takes the critic's own severity: CRITICAL and HIGH map to P1, MEDIUM to P2, LOW to P3, read from the critic's closing JSON block under `transcripts/harness_82388ac1/subagents/` and matched by subject; each match is quoted in `scratchpad/session_2026-11-20-file-open-issues-as-gaps/gap-batch-final-severity.tsv`. Where several critics raised one issue, the highest severity governs. A row with no recorder severity (the S15 critics, whose transcripts are not in this harness, the executors' own notes, owner questions with no finding) keeps the rule: a question, defect or hole P2, a limit or data gap P3. Count by priority with the query in the header.
- **One fact per cell (corrected 2026-11-20, twice).** `description` holds one plain statement; a description that joined several facts or hid a list behind "and others" is split, one row per fact, every item named. `section` holds the pointer, as `path :: heading`, or a commit sha. `parameter`, `identity`, `icf`, `needs`, `jurisdiction` and `language` are set where the issue is specific to one held value. `add-gap` refuses an open gap whose six subject cells are identical to an open gap's (a second gap differing in any one cell is accepted), so each open row carries a distinct combination: the bare-ratio figures carry parameter 3 alone; the open gate that refuses a kind carries parameter 3 with MOB, its own lens; the condition edges carry parameter 12; each of MOB's flagged ICF crossings carries MOB with its ICF code; the prose about MOB carries MOB; the matcher rows carry zh, ja and ko. Where a second issue has no other truthful cell (the ratio premise, the second SCI question, two ALL questions, the spaceless-script edition row), its cell is left blank and the severity file says why; the refusal itself is a gap row. `skill` is blank on every row, because no issue has a skill as its subject.
- **An `[UNVERIFIED-OPEN: …]` prefix** stays in the description until whoever files the row checks it.

## 6. What the table cannot hold

These columns stay in section 2 only, for the planning step:
- **Kind**: `category` is coarser (DEFECT and HOLE both become SW).
- **Stage** and **the owner's properties**: no column.
- **Closes with**: goes into `resolution_ref` at closing, once the resolution columns exist; rows are filed OPEN.
- **First logged**: `created_at` will be the filing time; the date stays here and in the record `section` points to.

## 7. Logged in the database

The command (open gaps by category and priority, then the open rows):

```
python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
for r in c.execute(\"select category, priority, count(*) from gaps where status like 'OPEN%' group by 1,2 order by 2,1\"): print(*r, sep=' | ')
print('--')
for r in c.execute(\"select gap_id, category, priority, replace(substr(description,1,120),char(10),' ') from gaps where status like 'OPEN%' order by priority, category, gap_id\"): print(*r, sep=' | ')
"
```

Generated 2026-11-20 02:37 UTC by that command; generated; re-run rather than trust:

```
AUDT | P1 | 4
DEC | P1 | 3
EG | P1 | 7
RP | P1 | 7
SW | P1 | 10
AUDT | P2 | 5
CI | P2 | 1
DEC | P2 | 4
EG | P2 | 4
RP | P2 | 8
ST | P2 | 2
SW | P2 | 20
AUDT | P3 | 2
EG | P3 | 3
RP | P3 | 1
ST | P3 | 2
SW | P3 | 5
--
GAP-020 | AUDT | P1 | THE CORPUS NOW HAS ZERO LIVE DETERMINATIONS, AND K01/K02 PASS BY HAVING NOTHING TO EXAMINE. Batch 16 retired specificati
GAP-024 | AUDT | P1 | GAP-020 IS NOT CLOSED BY THE GAP-019 FIX, AND THE REASON IS NOW MECHANICAL RATHER THAN A JUDGEMENT CALL. With the engine
GAP-B01-001 | AUDT | P1 | All five batch-1 admissions had FABRICATED author lists on first write (12 of 19 author rows named non-authors), correct
GAP-B02-001 | AUDT | P1 | Batch 2 admitted five sources on metadata alone. No full text was read: every field is payload-verified and no CONTENT c
GAP-074 | DEC | P1 | WHAT TERM NAMES THE WIDTH A PASSAGE NEEDS AT A TURN, AND WHICH PARAMETER HOLDS IT? OWNER DECISION. Found in sessions ses
GAP-075 | DEC | P1 | CAN A CONTROLLED PRIMARY MEASUREMENT REPORT FILED AS grey REACH T1? OWNER DECISION. Found in sessions session_2026-11-06
GAP-076 | DEC | P1 | WHICH LENS DOES A CLAUSE CARRY WHEN ITS OWN TEXT NAMES NO ONE BUT SITS UNDER A DISABILITY HEADING (MOB OR ALL), AND WHO 
GAP-002 | EG | P1 | RAMP GRADIENT HAS DOSE-RESPONSE EVIDENCE AND NO THRESHOLD. Batch 08 admitted two studies measuring the EFFECT of gradien
GAP-016 | EG | P1 | READ VREDENBURGH ET AL. 2009 (REF-01002) IN FULL. IT IS THE FIRST ANCHORING-TIER STATED MAXIMUM THIS PARAMETER HAS HAD, 
GAP-028 | EG | P1 | THE PRE-1990 RAMP-GRADIENT LITERATURE HAS NO DOIs, AND IT IS WHERE THE 1:12 THRESHOLD PROBABLY COMES FROM. REF-00980 bac
GAP-037 | EG | P1 | GAP-028 IS ANSWERED, AND THE ANSWER IS THAT 1:12 WAS MEASURED AND FOUND WANTING BEFORE IT WAS ADOPTED. GAP-028 asked whe
GAP-078 | EG | P1 | PARAMETERS 7 AND 10 HOLD NO EXTRACTION AFTER FOUR SOURCES WERE READ AGAINST THE WHOLE CATALOGUE, AND PARAMETERS 5 AND 8 
GAP-079 | EG | P1 | NO CO-1 SOURCE HAS BEEN RETRIEVED FOR DOOR, CORRIDOR OR TURNING-SPACE DIMENSIONS. R1 PASSES ONLY BECAUSE A SEARCH WAS TA
GAP-097 | EG | P1 | PARAMETERS 4 TO 11 HAVE NO accessibility_direction, SO NO DETERMINATION CAN BE COMPOSED ON ANY OF THEM. Found by the res
GAP-025 | RP | P1 | BATCH 17 MINING ASSIGNMENT — owner instruction 2026-09-18, answering GAP-022: "then assign the mining for the next batch
GAP-029 | RP | P1 | THE GAP-018 PREDICTOR IS FALSIFIED, AND THE RESULT REPORTED AS ITS FIRST SUCCESS WAS A SCREEN ARTEFACT. THIS RETRACTS A 
GAP-061 | RP | P1 | NOTHING PROMOTES A HARVESTED TERM TO A PARAMETER, SO EVERY BATCH IS CONFINED TO THE ONE PARAMETER THAT EXISTS. source_va
GAP-067 | RP | P1 | THE NOTE ON ALL NINE PROMOTED PARAMETERS IS FALSE FOR PARAMETER 12 AND COPIES FACTS THE SCHEMA DERIVES. 'no source adjud
GAP-070 | RP | P1 | REST-LANDING LIMITS STATED AS RISE HAVE NO PARAMETER. Parameter 12 is the horizontal run between landings (TERM-091), an
GAP-098 | RP | P1 | EVERY ROW OF BOTH BATCHES CARRIES AN IDENTITY LENS ONLY; THE ICF AND ACCESS-NEED LENSES ARE EMPTY, AGAINST OR-1 ACTION (
GAP-B01-002 | RP | P1 | DEM carries 8 of 13 items on this slug -- the heaviest-weighted population -- and batch 1 admitted NO source grading abo
GAP-008 | SW | P1 | source_locators.doi IS SHUFFLED RELATIVE TO title/authors/pub_year ACROSS THE PRE-RESET MIGRATION, AND IT BREAKS R9 IN B
GAP-009 | SW | P1 | EVERY SOURCE ADMITTED BEFORE 2026-09-18 WAS FILED TO EXACTLY ONE SLUG, AND THE CAUSE WAS A MISSING WRITER RATHER THAN A 
GAP-011 | SW | P1 | MULTI-SLUG FILING BREAKS citation_mining_completeness's PER-SLUG SEMANTICS, AND GAP-009's FIX IS WHAT OPENED IT. citatio
GAP-012 | SW | P1 | EVERY retrieval_log.fetch() CALL IN BATCHES 10-15 OMITS ref_id=, SO THE VERBATIM CHECK RESOLVES TO ITS WEAK BRANCH. quot
GAP-021 | SW | P1 | citation_mining.backward AND .forward ARE SET TO 1 ON A PASS THAT WAS DEFERRED, SO THE DIRECTION FLAGS DO NOT MEAN THE P
GAP-030 | SW | P1 | GAP-008 HAS NOW BLOCKED THE SAME ADMISSION TWICE, AND THIS BATCH HAS THE CONCRETE PROOF OF THE CORRUPTION RATHER THAN TH
GAP-033 | SW | P1 | TERM ADJUDICATION HAS NEVER RUN, AND NOTHING SAYS SO. Harvest at evidence, adjudicate at judgment (owner 2026-08-27, ove
GAP-086 | SW | P1 | THE DEFINITION-OF-DONE GATE READS NEITHER source_scans NOR source_value_extractions, SO COMPLIANT SAYS NOTHING ABOUT THE
GAP-087 | SW | P1 | NO SANCTIONED WRITER CORRECTS A LENS, A LOCATOR, A SETTING, THE contested FLAG, A CANDIDATE'S harm_finding OR TITLE, OR 
GAP-099 | SW | P1 | v_scan_ledger COUNTS A pre-screen AS A FULL READING, SO scan_debt FELL ON READINGS WHOSE ABSENCE CLAIMS WERE LATER DISPR
GAP-048 | AUDT | P2 | v_value_independence COUNTS ABSENCES AS INDEPENDENT ROOTS. The view counts DISTINCT COALESCE(root_ref_id, root_id) over 
GAP-069 | AUDT | P2 | No gate scoped to a session examines a term-adjudication-only batch. adversarial_pass_audit.py (RC4) derives its subject
GAP-085 | AUDT | P2 | EVERY READING RECORDED IN THESE TWO BATCHES IS pre-screen; NO SOURCE WAS READ END TO END AND NO OPEN PASS WAS DONE. Foun
GAP-095 | AUDT | P2 | PREFLIGHT PRINTS ADVISORY FAILURES THAT NO SESSION HAS DIAGNOSED, AND TWO TESTS ARE RED ON UNTOUCHED main. Found in sess
GAP-101 | AUDT | P2 | ADVERSARIAL PASS 5 HAS SUSTAINED FINDINGS WITH NO DISPOSITION, NO SESSION RECORD AND NO GAP. Found by the resolution ana
GAP-B01-004 | CI | P2 | Tier-1 room-side controlled evidence that batch 1 wrongly reported absent is held in this project as source_locators lea
GAP-015 | DEC | P2 | IS THE R2 MINING OBLIGATION PER SOURCE OR PER (SOURCE, SLUG)? THE REPOSITORY HOLDS BOTH ANSWERS AND THEY ONLY AGREED WHI
GAP-063 | DEC | P2 | THE LIVE CO-1 SOURCE TYPES ARE NOT THE ENUM THE WRITER CHECKS, AND THE ENGINE GRADES THEM BY FALLBACK. Derive: select re
GAP-077 | DEC | P2 | SHOULD AN INSTRUMENT FOR ENGLAND ONLY BE REPRESENTABLE BELOW UK? OWNER VOCABULARY DECISION. Found in sessions session_20
GAP-100 | DEC | P2 | NONE OF THE OWNER DECISIONS (GAP-074 TO GAP-077) IS ON THE OWNER'S PAGE. Found by the resolution analysis (scratchpad/se
GAP-001 | EG | P2 | Evidence gap (parameter-scoped): 4 extraction(s) exist for parameter 3, but EVERY source holding one has been SUPERSEDED
GAP-003 | EG | P2 | Evidence gap (parameter-scoped): 8 extraction(s) from 1 source(s) exist for parameter 3, but none of those sources quali
GAP-004 | EG | P2 | Evidence gap (parameter-scoped): 11 extraction(s) from 2 source(s) exist for parameter 3, but none of those sources qual
GAP-083 | EG | P2 | THE PORTUGUESE DECREE IS HELD AS 5 OF 20 PAGES, AND ITS TURNING DIMENSION IS NOT AMONG THEM. Found in sessions session_2
GAP-041 | RP | P2 | THE DISCOVERY-CATALOGUE STRATUM IS CLOSED IN THIS ENVIRONMENT, AND THREE BATCHES HAVE NOW EACH DISCOVERED IT SEPARATELY.
GAP-049 | RP | P2 | BATCH 20's R1 (Co-1 / T2) LEG WAS A THIN DISCHARGE OF R1, NOT A FULL ONE. It ran three queries (exec 92-94): English onl
GAP-068 | RP | P2 | PARAMETER 5 (TERM-003, turning circle) MAY NAME A SPACE, NOT A QUANTITY. With 'Minimum' removed its definition reads 'Sp
GAP-071 | RP | P2 | REST-LANDING SPACING IS READ FOR A FEW CODES; THE COMPLEMENT QUERY OVER-INCLUDES. Derive what parameter 12 holds: select
GAP-080 | RP | P2 | SIX PRIMARY-STUDY CANDIDATES ARE STAGED ON ABSTRACTS AND NONE HAS A REACHABLE FULL TEXT; THE CROSS-FILING ID OF ONE IS U
GAP-081 | RP | P2 | CITATION MINING OF THE ANTHROPOMETRY REPORT IS DEFERRED IN BOTH DIRECTIONS. Found in sessions session_2026-11-06-pipelin
GAP-082 | RP | P2 | FIGURES STATED IN THE SOURCES READ AND LEFT UNFILED, AND CONCEPTS THE REPORT NAMES THAT NO OBSERVATION RECORDS. Found in
GAP-B01-003 | RP | P2 | MH (5 items) was never searched, never deferred and never mentioned by batch 1 -- a larger unrecorded hole than the SCI 
GAP-094 | ST | P2 | ROWS IN METRES, CENTIMETRES, MILLIMETRES AND NEWTONS ARE FILED BESIDE ONE ANOTHER ON PARAMETERS 4, 6, 9 AND 11, AND THE 
GAP-ICF-TITLES | ST | P2 | base_icf holds 72 ICF codes of which 29 carry a title stated by a document in this repository (the functional-deficit-au
GAP-007 | SW | P2 | relate-extraction HAS NO --verbatim-exempt AND add-extraction DOES, SO A CONDITION READ FROM A NON-UTF-8 PAYLOAD CANNOT 
GAP-013 | SW | P2 | FOUR DEEPER FIXES A /simplify PASS NAMED AND THIS SESSION DID NOT TAKE, each wider than the diff it reviewed. (1) _AMEND
GAP-017 | SW | P2 | log-mining COULD NOT EXPRESS A MINING PASS THAT RAN AND FOUND NOTHING, AND NEVER CLEARED A DEFERRAL IT DISCHARGED -- BOT
GAP-031 | SW | P2 | THREE FIELDS WITH NO REPAIR PATH, FOUND BY A CODE REVIEW OF BATCH 17 ADMISSIONS. (1) evidence_sources.journal_name is NU
GAP-034 | SW | P2 | AN EVIDENCE RETRIEVAL MADE THROUGH WebFetch LEAVES NO ARTEFACT, AND THE RECORD CANNOT TELL. CLAUDE.md section 5(c): veri
GAP-038 | SW | P2 | THE SEVENTH CAPTURE-PATH BLINDNESS, AND IT WAS FOUND BY THE ROW IT BROKE. add-source could not write source_type, instit
GAP-039 | SW | P2 | GAP-007 IS CLOSED, AND THE DEFECT WAS WORSE THAN GAP-007 DESCRIBED IT. GAP-007 recorded that relate-extraction lacks --v
GAP-040 | SW | P2 | A FAILED RETRIEVAL WAS RECORDED AS A NULL RESULT, ONE BATCH AFTER THE SAME ERROR WAS RECORDED AS A LESSON. Batch 18 fire
GAP-042 | SW | P2 | FOUR MORE evidence_sources VOCABULARIES LIVE ONLY IN A TEST FILE, AND THE WRITER CANNOT SEE ANY OF THEM. Migration 089 f
GAP-043 | SW | P2 | TWO WRITER-REACH DEFECTS FOUND BY A CODE REVIEW OF BATCH 19, both narrower than they look and both leaving a column no s
GAP-044 | SW | P2 | A KNOWN-WRONG AUTHOR ROW THAT NO SANCTIONED WRITER CAN CORRECT. REF-01002's fourth author is stored as 'Weiner, Jerome M
GAP-062 | SW | P2 | SIX VIEWS DO NOT FILTER A SUPERSEDED SOURCE, SO A TOMBSTONE STILL READS AS LIVE THROUGH THEM. supersede-source (T1, PR #
GAP-064 | SW | P2 | WRITER GAP: add-parameter SCREENS ONLY THE TERM'S canonical_en FOR A DIRECTION OR A VALUE; THE DEFINITION AND scope_note
GAP-065 | SW | P2 | A CAPTURED UPDATE CARRIES NO OLD-VALUE GUARD. emit_batch_sql.py writes UPDATE statements that set absolute captured valu
GAP-066 | SW | P2 | THE BOOK-SURFACE PARTS ARE STALE AGAINST THE DATABASE AND NO CHECK COVERS THEM. parts/v10/ is generated by scripts/gener
GAP-088 | SW | P2 | A RESULT PAYLOAD CAN BE LINKED TO A SEARCH ONLY IF THE SEARCH'S query_text NAMES THE PAYLOAD'S HOST, AND A WebSearch LEA
GAP-089 | SW | P2 | pages_read ON A SCAN ROW COUNTS THE PAGES HELD, NOT THE PAGES READ, SO A POINTER SCAN READS AS A FULL READ. TOOLING PR (
GAP-090 | SW | P2 | THE VERBATIM CHECK CANNOT QUOTE A KOREAN SENTENCE THAT CROSSES A LINE BREAK, SO claim_text IS CUT MID-WORD. TOOLING PR (
GAP-091 | SW | P2 | A SEARCH RUN BECAUSE A CRITIC FOUND A QUERY-SHAPE FAILURE CANNOT BE LABELLED adversarial-pass AT WRITE TIME. TOOLING PR 
GAP-092 | SW | P2 | A CATALOGUE READING DEPENDS ON THE READER'S KEYWORDS, AND THEY MISSED STATED FIGURES IN BOTH BATCHES. PROCESS AND TOOLIN
GAP-096 | AUDT | P3 | ADVERSARIAL PASS 7 IS STILL OPEN, AND ITS CLOSING NEEDS THE OWNER OR A TOOLING CHANGE. Carried from the previous session
GAP-102 | AUDT | P3 | TYPED COLUMNS CONTRADICT THEIR OWN NOTES, AND resolve-candidate WAS USED AS A NOTE CHANNEL. Found by the resolution anal
GAP-014 | EG | P3 | GAP-010 RESOLVED 2026-09-18: REF-01001 IS NOT Co-1, AND PARAMETER 3 REMAINS A PROXY DETERMINATION. Full text retrieved v
GAP-073 | EG | P3 | WRITER GAP (rule 10: filed, not patched). add-source has no flag for journal_name or publisher and correct-source cannot
GAP-084 | EG | P3 | WHETHER THE UK 1500 BY 1500 mm LANDING AND MANOEUVRING SPACES ARE TURNING SPACES IS NOT SETTLED BY ANY HELD SOURCE. Foun
GAP-052 | RP | P3 | LEGACY REHOME CANDIDATES THAT NAME NO DESTINATION. From 2026-09-26 both writers that can set REHOME -- add-candidate and
GAP-072 | ST | P3 | COMPOSITION OF PARAMETER 12 REFUSES MIXED LENGTH UNITS. assess_cell.NOTATION_FAMILIES holds only the gradient family, so
GAP-H3-PCS-COLLISION | ST | P3 | 'PCS' denotes two different conditions in two live documents: populations.BRAIN.description reads 'Merges former NEU + P
GAP-023 | SW | P3 | GAP-019 RESOLVED 2026-09-18, AND HALF OF WHAT IT CLAIMED WAS AN INSTRUMENTATION ERROR OF MINE THAT MUST BE RETRACTED. TH
GAP-035 | SW | P3 | THREE FIELDS THAT CAN ONLY BE RIGHT OR WRONG, NEVER INFORMATIVE (rule 8). (1) doctrine_sha in every attestation: the sch
GAP-036 | SW | P3 | tools/pipeline_walk.py ATTRIBUTES ONLY CREATED ROWS, SO A BATCH THAT MINES LOOKS IDLE. It derives session columns throug
GAP-056 | SW | P3 | scripts/db.py's _require_verbatim digit-check (add-extraction's claimed_value verification, ~line 6579) was widened 2026
GAP-093 | SW | P3 | update-locator REWRITES created_by_session AND created_at ON A STASH ROW ALTHOUGH ITS DOCSTRING SAYS ONLY THE STATUS MOV
```

## 8. How this file is kept

- **Not kept by hand once filed.** The data pull request files section 2 through `db.py add-gap` (from `gap-batch.tsv`) and section 3 through `db.py record-adversarial-pass`; this file is then regenerated from the tables. Until then a status change is made in place, dated, with the resolving commit, and the row moves to a "Resolved" section at the end. Nothing is deleted.
- **A new issue** gets the next ISS number and a line in the TSV, in the same edit.
- **Read by** the coordinator at session open (`/orient`) and the owner.
- **What would be wrong to add:** a copy of the detailed record (the sweep list item, the critic's finding, the task file's open point). A row states the issue in one line and points to the record. So would a typed count (rule 7a).
- **Filing a row in the database is a data change.** It goes in a research or data pull request, never in a tooling one (CLAUDE.md rule 10). The tooling change that adds resolution columns to `gaps` merges first, and the rows are filed after it.
