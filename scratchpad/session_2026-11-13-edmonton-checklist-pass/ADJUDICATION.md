# Adjudication: the Edmonton checklist digest (REF-01037) and the owner's ten questions

Written 2026-11-13 by the adjudicator (Fable 5.2), read-only. Sources read: the hand-off, `CLAUDE.md`, the ledger by `git grep`, the scratch database (read-only), `scripts/db.py`, `scripts/dbcore.py`, `scripts/assess/assess_cell.py`, `skills/run-pipeline_SKILL.md`, the task files named below, the PDF text layer and renders p0000, p0001, p0004, p0005. Line numbers are as read on that date; each is given with a grep that finds it again. Counts are given as commands (rule 7a); where a figure is printed it is dated and the command is beside it.

`S` below is the scratch database: `/tmp/claude-0/-home-user-guidebook/5dbc61f3-e21d-5874-a6a8-3a991f0f402c/scratchpad/edm/guidebook.db`.

## 0. Verdict

1. **The digest should not be repaired in place. Replay it on a fresh scratch copy.** Nothing is committed, the drivers are on disk (`helpers/obs.py`, `obs2.py`, `ext.py`), and an in-place repair would carry into the emitted migration two retired parameters with burnt ids, retired cells, retired `ALL` links, amended comparators and an `absent` row that cannot be retired. `CLAUDE.md` rule 3's "fix forward" binds committed migrations only.
2. **Of the nine answers: A1, A3, A4 stand with corrections; A2, A5, A6, A7, A8, A9 are corrected; none is withdrawn whole.** The largest errors are in the digest itself, not the answers: it wrote the identity `ALL` against OD-31, wrote no ICF or access-need link at all, pre-empted two owner rulings on "barrier-free path of travel", and promoted two elements.
3. **Most of what the owner's questions ask for is already ruled or already tasked.** The gaps are four: `DEFERRED` has no reader; `design_scale` carries two meanings; a figure's circumstance (building type, new or existing, interior or exterior) sits in a joined free-text cell the engine never reads; and a figure whose clause names no one has no lawful lens. Three of those need the owner.
4. **Coverage.** The catalogue can hold almost none of what this document says for blind, Deaf, cognitive or invisible access needs. That is derivable today by one query (section 3) and is the finding the exercise is most useful for.
5. **Q10** (added by the coordinator): the rules support the register reading. A hand-written canonical row would override rules 3 and 10 and is left as an open owner question.

Eight owner questions are raised (section 5.3), all left OPEN.

---

## 1. Adjudication of each question and answer

### Q1 / A1. Code floor versus above the floor — STANDS, with one correction and one question withdrawn from the owner

**Premise check.** No best-practice column exists in the schema (`PRAGMA table_info(source_value_extractions)`). The "column" was a column of the report's table and a proposal in GAP-103. The owner's point holds against both.

**The owner's rule, in the owner's words** (`git grep -n -F 'best practice = the best way to do something' -- references/project-standards.md`, line 4820 and the lines after it): "best practice = the best way to do something according to how it benefits the intended group"; "best practice =/= most common or agreed upon"; "the gentlest value is the gentlest value. the evidence is that it exists in practice". Best practice is therefore an output of the determination, selected in the parameter's recorded direction. A1 is right to concede.

**Correction: A1 leaves open something that is already derivable or ruled.**
- Floor or above-floor is not a property to type on a figure. It is derived: a figure is a floor when its source is in the regulatory stratum (`db._regulatory_pairs()`), or when it echoes one; "above the floor" is a comparison on the parameter's scale (`dbcore.bound_on_scale`) against the regulatory figures of the same parameter and jurisdiction. Rule 8 forbids a curated column for it.
- What the source's blue marking adds is an **attribution**: the source says the figure is the Alberta code's. That is root genealogy, and its homes exist: `root_type`, `root_ref_id`, `root_classification_basis`. The owner has ruled on the case: OR-19, "Yes, presume an echo" (`git grep -n -F 'OR-19: "Yes, presume an echo"' -- references/project-standards.md`, line 4717; reading at 4754: "presumed to echo the code, without being re-tiered, and the presumption can be rebutted").
- So **the critic's withheld question "wrapper or root" is not the owner's: it is answered.** The wrapper keeps its tier (T3 grey); the blue figures are presumed echoes and supply no independent root. Because the Alberta code is not held, they are `untraced` with the basis sentence (precedent: extractions 57 and 64) and a lead; T-071 step 3 re-roots them when the code is admitted.
- The relation of a magenta figure to the blue figure beside it (1800 against 1100; 920 against 850) is the source's own pairing and has a typed home: an `extraction_relations` edge. None was written (`select count(*) from extraction_relations r join source_value_extractions e on e.extraction_id=r.from_extraction_id where e.ref_id='REF-01037'` on `S`).
- GAP-103 should be closed as answered by derivation, not left as a schema proposal.

**A pull-apart A1 did not see.** `governance/adversarial-use-framework.md` line 31 (`grep -n 'never \*best practice\*' governance/adversarial-use-framework.md`) says Universal Mode is "never *best practice*". The 2026-10-30 rulings name the gentlest code value as best practice at ○ with the code-derived flag (ACTION 1 of that entry; ratified by "Yes, keep the ○ band and flag", line 4873). The ruling wins (rule 0). The framework sentence is a prose caller. [NOT VERIFIED: whether it carries a supersession mark.]

### Q2 / A2. Subjects in the PDF with no base term — CORRECTED

What stands: T-072's subject is the regulatory stratum only (its section 4 item 1), REF-01037 is outside it, and no code, view, check, skill line or task reads a `DEFERRED` adjudication (`git grep -n -E "'DEFERRED'|\"DEFERRED\"" -- scripts governance/check-registry.yaml governance/pipeline-contract.yaml ':!scripts/migrations'` returns only the writer's message). The skill's resume list names unadjudicated observations and NAMES-NEW terms, not deferred ones (`grep -n 'Resume from live state' -A6 skills/run-pipeline_SKILL.md`).

What is wrong:
1. **"OR-17 leaves minting to the data pull request" is not a reason to defer; this digest is a data batch.** OR-17 in the owner's words (line 4713): "Yes, bulk, with me reading the PR — Ensure that these phrases/names/aliases are all present in their prescribed jurisdiction/language. It is not acceptable for the model to generate its own phrases/names/aliases." It sets conditions on minting; it does not postpone it. The skill says the same (`grep -n 'A new concept arises while a source is in hand' skills/run-pipeline_SKILL.md`). The critic's F16 is sustained.
2. **`DEFERRED` was used for two different states.** The schema defines it as "cannot be settled on this source alone" (`term_adjudications` DDL comment). "Handrail height" is settled on this source: it names a quantity the catalogue lacks. "Colour contrast" against LRV contrast is the genuinely unsettled kind. The first kind has a home that already has a reader: mint the **term** (not the parameter) with `add-term --from-observation`; a NAMES-NEW term that is neither a parameter nor declined is on the skill's resume list and is T-072 section 4 item 6's subject.
3. **The proposal to widen T-072 to every source pulls against OR-13** ("From the codes held", line 4677; reading at 4698: "seeded by an open-pass scan of the bucket 1 and 2 codes already held, not slug by slug"). Whether a non-code source may promote a *parameter* is not ruled. It is put to the owner as AQ-4. Minting the *term* is within the standing rule.
4. The count "57" is a result. The command: `with latest as (select a.* from term_adjudications a where a.adjudication_id=(select max(adjudication_id) from term_adjudications b where b.observation_id=a.observation_id)) select coalesce(l.outcome,'UNADJUDICATED'), count(*) from observed_terms o left join latest l using(observation_id) where o.ref_id='REF-01037' group by 1`.

### Q3 / A3. Growing the base dynamically — STANDS, with the proposal reduced

The five steps of today's mechanism are verified: the four outcomes are the column's CHECK; `v_scan_ledger` owes a reading for every source against every active parameter and a catalogue reading covers a parameter only when `catalogue_version >= parameter_id` (view header), so a new parameter creates re-read debt mechanically; `_near_terms` is the duplicate guard.

Reduced, by section 8's order:
- **Candidate queue.** Do not build a table or a ranking. The unadjudicated and deferred observations are already rows; what is missing is one read. T-079 is building `v_deferred_acts` for searches, mining and readings (`grep -n 'v_deferred_acts' workplan/2026-11-12-bidirectional-pipeline/tasks/T-079-deferred-acts-with-age.md`); a deferred adjudication is a fourth kind of the same thing and rests on the same owner sentence, "deferred is okay so long as it runs eventually". Extend that view. See P3.
- **Recurrence as a signal** is T-033's subject ("terms sharing a form", read-only candidates). No second mechanism.
- **Review sheet for the owner**: the data pull request is the review (OR-17). No generator.
- **Feedback hook from a pending cell**: not needed. A cell is keyed on a parameter, so a cell cannot be pending for a parameter that does not exist. Withdrawn.
- The three "decisions put to the owner" collapse into AQ-4.

### Q4 / A4. Not duplicating — STANDS, with two corrections

Verified in `scripts/db.py` (`grep -n 'def _near_terms' -A30 scripts/db.py`): token-set subset or superset against every canonical name and every English alias whose attestation is not `model_seed`; a one-token held name inside a compound is not a match. The alias types and attestation values are the CHECKs of `term_aliases`. `merge-parameter`, `rename-term` and `retire-parameter` exist as verbs.

Corrections:
1. **The proposed ranked candidate list is T-033**, which the plan already holds, with T-029 (term-to-term pointers) and T-028 (a concept that is not an English string) under it. Extend T-033's inputs to a proposed name; add nothing new.
2. **Three places will record "equivalent", and the plan does not say how they differ.** `term_aliases.alias_type` (a phrase to a term); T-029's kinds, which include `equivalent` and `broader` (term to term); T-032's relation kinds `equivalence`, `adjacency` (provision to provision, OD-25). Two terms that are equivalent are a dual home (rule 5): the act is a merge or an alias, never a standing pointer. Smallest reconciliation: a convention in T-029's design that its `equivalent` kind is either dropped or defined as "counterpart, not identical", and one sentence naming each table's subject. No owner question.

The digest's own equivalence judgments are weaker than A4 admits. The critic's F12 list is sustained, and observation 110 ("ACCESSIBLE WASHROOM STALL" to TERM-009 accessible bathroom) is a stall adjudicated to a room.

### Q5 / A5. Branch, clause or own parameter — CORRECTED in mechanism

The table's principle matches OD-24 (`git grep -n -F 'OD-24: flat and coarse' -- references/project-standards.md`, line 5643; "two cases are two parameters only when they cannot be placed on one scale or their accessibility directions differ"). OD-24 is a delegated resolution, "not the owner's words; standing until the owner reverses it"; A5 should say so.

Corrections:
1. **"A condition on a handrail rule, not a stair-width parameter" is wrong as mechanism.** A `condition_on` edge needs a row at both ends (`extraction_relations` DDL: "this figure only holds given a second figure this project also holds as a row"), and every extraction row has `parameter_id NOT NULL`. So the 1100 mm is a row of `figure_role='condition'` **on a stair-width parameter**, which never anchors. The stair-width parameter must exist for the condition to be typed.
2. **"Handrails on one side or both" is a count.** The kinds OD-24 lists are length, gradient, force, time, luminous reflectance and its contrast, colour temperature. A new kind is added by data with a warrant and, by T-072 item 5, the owner's approval. A5 lists "count" as if it were held.
3. **"A circumstance goes in `--setting`" is today's practice and is the defect, not the answer.** See Q7.
4. The element pointer is T-029's, not T-060's.
5. The admitted error (parameters 13 and 14) is confirmed and worse than stated: TERM-092 is named in E2 as one of the terms "that carry a name no source used", to be renamed in a research pull request (`git grep -n '^| E2 ' -- references/project-standards.md`, line 5050), and it is T-072 item 6's to judge. The promotion pre-empted both.

### Q6 / A6. Values per group, and design modes — CORRECTED

Verified: the determination's key and its "at least one lens" CHECK (`specifications` DDL); a figure reaches a cell only through its live lens links (`grep -n 'a figure reaches' scripts/assess/assess_cell.py`); a contested direction prints the spread (`grep -n 'direction == "contested"' scripts/assess/assess_cell.py`); the engine sets `design_scale` to `universal` only on a regulatory-only basis (`grep -n 'design_scale = SCALE_UNIVERSAL' scripts/assess/assess_cell.py`) and never writes `person`.

Corrections:
1. **A6 omits the ruling that governs the question.** OD-31 (`git grep -n -F 'OD-31: a provision that names no one' -- references/project-standards.md`, line 6044): "a provision that names no one carries the group its heading names (under a mobility heading, the parent MOB with no child; under a general disability heading, no identity, only its ICF and access-need lenses); ALL leaves the identity lens, universal being stated once, by design_scale". ACTION: "do not use `ALL` as an identity".
2. **`design_scale` holds two meanings.** The engine's G1 writes `universal` for "rests on codes only". OD-31 makes `universal` mean "names no group". The scratch database shows the collision: a `MOB` cell reads `universal` and an `ALL` cell reads `population` (`select parameter_id, identity_code, design_scale, regulatory_stratum_only from specifications where retired_at is null` on `S`). The code-only fact already has its own column, `regulatory_stratum_only`, so `design_scale` repeats it (rule 5) and has no room for OD-31's meaning. T-056 item 3 changes how a universal determination gathers and does not touch G1. This is AQ-2.
3. **"No rule derives a universal value from the per-group cells" is correct and is not a gap.** The ledger's first design-mode rule (line 14) defines Universal Mode as "Universal Design / Code Compliance (population-agnostic, fixed values)" and Population Mode as ranges. A universal value is not an aggregate of group values under either meaning.
4. **The lens is almost never ICF or access need.** `select (icf_code is not null), (needs_code is not null), (identity_code is not null), count(*) from v_live_lens_links group by 1,2,3` on `S` (2026-11-13: one ICF link, three access-need links, the rest identity). The answer describes four lenses; the data use one. `CLAUDE.md` section 6 requires the ICF and access-need frame.

### Q7 / A7. Commercial, residential, public — CORRECTED and completed

Verified: the 2026-08-27 ruling and its three levels (`git grep -n -F 'base_building' -- references/project-standards.md`, line 2053; the owner's words at 2056); ENT-16 is "Deferred" (`grep -n 'ENT-16' governance/conceptual-model.md`); `rooms` is the only level present.

The two items A7 could not verify:
- **`room_items` no longer exists**, and nothing references `rooms`: `select name, type from sqlite_master where sql like '%room%'` returns the `rooms` table alone. The ruling's ACTION ("`room_items` is the existing one and is re-pointed, not replaced") names an object that is gone.
- **No figure carries a typed building type.** The circumstance is in `setting`, and the project's own census flags that column as holding joined values: `GUIDEBOOK_DB_PATH=<db> python3 scripts/audit/joined_cells_census.py | grep setting`. Door width shows it plainly: `select setting from source_value_extractions where parameter_id=9` returns values such as "new buildings; external doors to buildings used by the general public" and "existing buildings; straight-on approach": construction status, approach geometry and building use in one cell, against the 2026-11-06 schema-shape ruling (one value per cell).
- The engine does not read `setting` (`grep -n 'setting' scripts/assess/assess_cell.py`: one docstring line). So A7's consequence is confirmed: a dwelling figure and a public-building figure for one parameter and lens compose into one headline.

Correction: "OD-24 says carry such variations as typed conditions; T-017 turns a conditioned claim into a branch" does not reach this case. T-017's branch is a `condition_on` edge between two rows on parameters. Building type is not a quantity, so it cannot be a condition row. **"Typed condition" has a carrier only for conditions that are themselves measured.** This is the real distance between OD-24 and the building ruling. AQ-3.

"Public" is not one of the owner's examples of a building type ("residential, commercial"); in the held sources it is a legal scope phrase that differs by instrument.

### Q8 / A8. Too granular or too encompassing — STANDS, one stale statement corrected

The split test, the reversal condition and the medical-lens history are quoted correctly (lines 5643 to 5649; 2956; 3016).

Correction: A8 lists as open "how the grain is represented, who judges a grouping, and whether a granularity policy is doctrine". Those were left open by the owner's statement (line 5247 and its "What it does not decide") and were then **resolved under delegation the same day** by OD-24: flat, families by typed term pointers, no element required (`git grep -n 'OD-24 STATUS' -- references/project-standards.md`: "RESOLVED UNDER DELEGATION"). Who judges a relation is OD-25 through T-032 (an Opus-class judge). What remains the owner's is the option to reverse.

Two signs A8 should add, both derivable: a parameter whose `setting` values partition its figures (too encompassing; see Q7), and a parameter with no figure from any lens but one (section 3).

### Q9 / A9. Parameters that belong together — STANDS, with corrections

OR-14b is quoted correctly (`git grep -n -F 'OR-14b — who writes an element page' -- references/project-standards.md`, line 6189), including "The element is still never a container that figures are filed into". T-060 stops on its design file. The skill line on `connections` and `conflicts` having no reader is verified (`grep -n 'No code reads' skills/run-pipeline_SKILL.md`).

Corrections:
1. `connections` is to be reshaped by T-032 into one relation home with kinds `equivalence`, `commonality`, `similarity`, `adjacency` (OD-25); A9 describes the table as it is, not as tasked. The element-to-parameter pointer is T-029's `element has parameter`.
2. **Two homes for "element" are in play.** The 2026-08-27 ruling orders a `base_elements` table. OR-14 (2026-10-29, line 4699) derives an element page "from a typed term pointer", OD-24 says "elements reach parameters by term pointers", and the catalogue already holds elements as terms declined as parameters (TERM-089 `ramp`). AQ-3 part (b).
3. **What an element determination may hold** follows from OR-14b and rule 5, and Edmonton supplies the test: items 4.7 and 7.1 state a rule that belongs to no single parameter (handrails on both sides when the stair is 1100 mm or wider). The element row may hold pointers to its parameters' determinations and pointers to the relation and condition rows that cross them, and nothing else. A value column on it would be a copy. This is a constraint for `T-060-design.md`, not an owner question.

### Q10. A register for what the pipeline cannot execute — the register reading is the one the rules support

The owner's words, as relayed by the coordinator (not yet in the ledger): "it may be worthwhile to have a mechanism whereby when our scripting/pipeline cannot execute something, we explicitly flag it as a gap/issue for future resolution in a register alongside having an agent fix it by hand with correct context so we aren't losing content alongside filling in its resolution and proposed amendments for that gap/issue in register"; "that way we aren't held up"; "it could be like a layer 2 protocol or something".

**Ruling on the two readings.**
- Rule 3: "Never write `data/guidebook.db` directly. Migrations only". Section 4: "Do not hand-write SQL against a table the CLI can reach. If you find one it cannot, that is a coverage bug to fix, not a licence to bypass." Rule 10: a writer gap "is filed as a GAP and either left unwritten or written through verbs the CLI already has; it is never patched with hand SQL disguised inside the batch's data migration", with batch 20 as its proof.
- These leave exactly two lawful acts when a writer refuses: write through an existing verb, or park. **The coordinator's reading (an agent with context writes the intended row, the refusal, its class and a proposed amendment into a register, and the content is replayed through the sanctioned writer after the tooling merges) is inside the rules.** It is also what "so we aren't losing content" and "that way we aren't held up" ask for.
- The other reading (an agent writes the canonical row by hand) contradicts rules 3 and 10. A live owner statement would supersede them on contact (rule 0), but the words do not say "into the database", and a rule is not read as overturned by an ambiguous phrase. It is AQ-8, OPEN.

**Facts checked.**
- The command log keeps the command and hashes, not output: keys of a line are `bytes, command, cwd, exit, interrupted, is_error, response_keys, session_id, stderr_bytes, stderr_sha256, stdout_sha256, tool, ts` (`python3 -c "import json;print(sorted(json.loads(open('scratchpad/session_2026-11-13-edmonton-checklist-pass/commands.jsonl').readline())))"`). A refusal's sentence is therefore lost. `exit` is not reliable (the hook's own comment, `grep -n 'MEASURED CORRECTION' .claude/hooks/record-command.py`), so refusals cannot be recovered from exit codes either.
- **"`dbcore.Refusal` is the single exception class" is not quite right**: `grep -n '^class Refusal' scripts/dbcore.py scripts/assess/assess_cell.py` finds two. `db.py` catches at one point (`grep -n 'except Refusal as exc' scripts/db.py`).
- `gaps` has no payload column (DDL); categories are the CHECK's.

**What the digest shows.** Two different losses, and only one of them is a refusal:
- (i) *A writer refused.* The command and the sentence are the content at risk.
- (ii) *No verb could hold it.* Nothing was attempted, so nothing is captured at a refusal point. For this kind the homes mostly exist and were not used: a figure for no parameter is already held verbatim with its locator and quote as an **observation**; a harm statement tied to no parameter has the R7 route (search flag plus GAP); the per-statement marking is root genealogy and relation edges (Q1). What is missing for (ii) is a reader for parked observations (P3), not a new store.

**Smallest mechanism, by section 8's order.**
1. *Do nothing*: fails for (i); the sentence is gone and the retry history with it.
2. *Convention*: a rule in `/batch-done` that every refusal met in the batch is listed with one disposition: **retried** (the writer was right and the corrected call succeeded), **parked** (a gap id), or **waived** (with a reason). This is the definition-of-done part and needs no code.
3. *Reuse*: the register is the `gaps` table (`add-gap`, category by the CHECK; T-013 is already typing gaps). The payload's home is the captured line itself, since the refused argv **is** the replay command. No payload column and no new table until a reader needs to query payloads across sessions; today the reader is the tooling task that closes the gap and the research batch that replays.
4. *Smallest code*: at `db.py`'s one catch point (and the engine's), append one JSON line to `scratchpad/<CURRENT>/refusals.jsonl`: time, verb, argv, the refusal sentence. It rides rule 6's commit of the scratchpad. A handful of lines; it replaces nothing and makes nothing deletable, so it must be justified by its reader: `/batch-done`'s disposition list and the replay.

**Classes.** They are a judgment recorded on the gap, not a vocabulary to add: a policy refusal that was right (disposition *retried*, no gap); a missing verb or field (gap, parked, replay after the tooling pull request); a tool defect (gap, parked); an environment block (the existing `processing_blocked_reason` and deferred-act records); a data conflict (a follow-up or a contest row, which the writers already accept). If T-013's typed gap gains a kind, these map onto it; do not add a second list.

**Layers** (`CLAUDE.md` section 3).
- The capture point and the line's shape: **Layer 1** (shared by every writer; one home).
- Each stage's triage, meaning which refusals are expected at that stage and what the lawful alternative verb is: **Layer 2**, as lines in that stage's section of the skill.
- The rule that every refusal is disposed, in `/batch-done`, and a registered check only if review proves insufficient: **Layer 0**.
- The parked content and its replayed rows: **Layer 3**.

**On "a layer 2 protocol".** Best taken as a per-stage protocol with three moves: acknowledge (the row is written), refuse-and-park (the sentence and argv are captured and a gap is filed), replay (through the sanctioned writer, in a research pull request after the tooling merges, rule 10). The data-link analogy fits that shape. It does not fit the existing stage-pair checks (`judgment_handoff_shape`, `derivation_handshake_integrity`), which test the shape of rows already written; a refusal happens at a writer, inside a stage. So: a Layer 2 protocol on a Layer 1 carrier under a Layer 0 gate, not a new stage-pair contract.

**What wrong thing reaches the guidebook without it.** A determination that omits a figure or an inadequacy statement its source held, with no record that it was met; or, under the other reading, a canonical row that bypassed the refusal that would have stopped a fabricated or mis-typed value (section 5(c) of `CLAUDE.md`).

---

## 2. Reconciliation: one account

**Floor and above the floor.** A figure is recorded as its source states it, with its root. A regulatory source's figure is a floor in its jurisdiction by derivation from the source's `(evidence_type, scope)`. A grey source that repeats or attributes a code value is an echo (OR-19): its tier is unchanged and it supplies no independent root. A source's own pairing of a higher value with a floor is a relation edge. Best practice is selected by the determination as the most accommodating value in the parameter's direction; a determination resting on the regulatory stratum alone is named at ○ with the code-derived flag (OR-7; 2026-10-30). No stored property says "best practice" on an input.

**Growth of the vocabulary.** Every reading harvests phrases; each is adjudicated; a new concept is minted as a term in the source's own words in a data pull request the owner reads (OR-17); a term becomes a parameter only when it is a quantity with a kind (T-020, T-072); an element or a method is declined and kept. A new parameter makes every held source owe a reading (`v_scan_ledger`). Parameters are seeded from the held codes (OR-13); whether another source may promote one is AQ-4.

**Equivalence.** A phrase for a held concept is an alias with its type and attestation. Two terms for one concept are merged. Related-but-distinct concepts are term pointers (T-029). Provisions that say the same thing are synthesis relations judged at the Opus floor (T-032), proposed read-only by T-033. The writer's token guard catches shared words only; everything else is a recorded judgment.

**Parameter, branch, or own parameter.** One measured quantity is one parameter (OD-24). A measured condition is a `condition` row on its own parameter joined by `condition_on`, and T-017 shows the conditioned claim as a branch. A thing is a term, declined. An unmeasured circumstance has no typed carrier today (AQ-3).

**Lens and design scale.** A figure carries the group its own words name, else the group its heading names, else no identity and its ICF and access-need lenses (OD-31). `ALL` is not an identity. A determination is keyed on a parameter and at least one lens. `design_scale` is where "universal" is stated once (OD-31) and is today written from the evidence's stratum (AQ-2).

**Building type and occupancy.** Ruled as the first of three base levels (2026-08-27); absent; held in a joined free-text cell the engine does not read.

**Grain.** Flat and coarse, with the split test (OD-24, delegated), because the owner needs to "unify then specify". Too coarse shows as figures partitioning by circumstance; too fine as parameters no two instruments can both fill.

**Composition.** Parameters stay separate; an element is a term reached by pointers; the specifications pass writes an element determination that points and never copies (OR-14b).

### Where things pull apart, and the smallest reconciliation

| # | The two sides | Smallest reconciliation | Kind |
|---|---|---|---|
| R1 | OD-24's "every clause variation a typed condition" and the 2026-08-27 building-level ruling. `condition_on` carries only measured conditions; building type is not measured and sits in `setting` | The owner decides the carrier and the vocabulary | AQ-3 |
| R2 | T-060's stored element determination and "never a container" | Design constraint: pointers to parameter determinations and to crossing relation rows only; a test that the table has no value column | convention in `T-060-design.md` |
| R3 | `design_scale` as "rests on codes only" (engine G1) and as "names no group" (OD-31). `regulatory_stratum_only` already holds the first | The owner says which fact `design_scale` states; then one line in the engine | AQ-2 |
| R4 | OR-17 as a minting condition and `DEFERRED` as a place content goes to stop | Mint the term when the source settles the concept; keep `DEFERRED` for the unsettled; give it a reader by extending T-079's view | convention plus derived view (P3) |
| R5 | The `ALL` precedent (all earlier `ALL` links are `carried`) and OD-31 | Nothing new: T-056 builds the refusal and T-115 re-tags. Until T-056 merges the rule is the ledger's ACTION and the session is the gate | none; do not add an interim check |
| R6 | D-0182 (a figure needs at least one lens), OD-31 (no `ALL`; under a general heading, ICF and need "from the clause") and the lens writer's warrant (the words must be found). A clause that names no person, function or need has no lawful lens and cannot be written | The owner decides | AQ-1 |
| R7 | The 2026-08-27 ruling's `base_elements` table and OR-14 and OD-24's "typed term pointer" with elements already held as terms | One home; the owner says which | AQ-3 (b) |
| R8 | The skill's "`=` for a point" and the engine: `bound_on_scale` reads `=` as floor and ceiling at once, and no value-supplying claim in the canonical database carries `=` (`select comparator, count(*) from source_value_extractions where figure_role='claim' group by 1` on `data/guidebook.db`) | One sentence in the skill: `=` only where the source states an exact value; a "should be", "preferred" or "recommended" figure is a bound in the sense the source's own framing gives, with the warrant in the row | convention; a prose change in a tooling pull request |
| R9 | OR-13 (parameters seeded from held codes) and the standing rule that a concept is minted from any source in hand | Terms from any source; parameters as the owner rules | AQ-4 |
| R10 | Three records of "equivalent" (alias type, T-029 kind, T-032 kind) | State each table's subject once; drop or redefine T-029's `equivalent` | convention in T-029's design |
| R11 | `adversarial-use-framework.md` ("never best practice") and the 2026-10-30 rulings | Rule 0: the ruling governs; correct the sentence when that file is next opened by a doctrine task | prose caller; owner sign-off applies to the file |
| R12 | OT-1 and OT-2 (a route "through a building", specific to wheelchair and mobility-device users) and REF-01037's use of the same phrase for an exterior route carrying a contrast-and-pattern provision | The owner's term; put the new usage to the owner | AQ-6 |
| R13 | The lens warrant `named_in_text` accepts any words in the source's saved file, so a preamble can warrant every figure in a document | Convention in the skill: the words are the figure's item's own, or the basis is `heading`; a preamble sentence warrants only the quantities it names. No code: the judge is the gate and the warrant is auditable | convention |

---

## 3. Disability coverage

**What the document reaches.** Read from the text layer, by the groups its own clauses name or plainly serve:
- Named in a clause: wheelchair and scooter users (2.7, 6.5, 9.6, 9.7, page 1); "person with limited mobility" (8.6); "persons who are blind" (8.2); "someone who uses a cane" (11.1); "users who are Deaf or hard of hearing" (9.2); "those with visual processing difficulties or who are unable to read" (3.2); "people with low vision" (page 1). Page 1 also names "Strollers for children", which is not a disability group.
- Served without being named: blind and low-vision people (tactile strips, braille, contrast, glare, cane detection, audible announcements: 1.2, 3.3, 3.5, 3.6, 4.1, 4.2, 4.5, 4.8, 5.1, 5.5, 5.6, 5.8, 6.4, 7.2, 9.8, 11.2); Deaf and hard-of-hearing people (3.1, 5.7, 9.9, 10.1); cognitive access (3.2, 3.4, 1.11); fatigue and pain (5.9 seating, 6.2 resting areas, 11.3 benches); sensory and invisible needs (11.4 "Have a quiet space available"); body size (8.6 "various toilet size and heights", 9.6 seat widths).
- The four access categories ("Physical Access", "Deaf or Hard of Hearing Access", "Blind or Low Vision Access", "Cognitive Limitations Access") are in the text layer of page 1 and not visible in render p0000. [NOT VERIFIED: whether they are white text or labels of the four logo figures.] No item carries them.

**What the catalogue can hold.** `select p.parameter_id, t.canonical_en from base_parameters p join terms t using(term_id) where p.status='active'` on the canonical database: widths, a gradient, a run length, a turning space, a headroom, an operating force, and three sensory quantities (reverberation time, LRV contrast, colour temperature). Of the sensory three, two hold no figure at all and the third holds none with a value from this source.

**Where the pipeline as it stands under-serves a group.**
1. **Every extraction the digest wrote is a mobility quantity.** Sixteen rows, ten parameters, and the document's blind, Deaf, cognitive and invisible content reached rows only as two `absent` findings. Everything else is a deferred observation with no reader (R4).
2. **The identity lens is nearly empty outside mobility, and the other lenses are nearly empty altogether.** Derive it; do not trust the list: `select identity_code from base_taxonomy_identity where status='active' and identity_code not in (select identity_code from v_live_lens_links where identity_code is not null)` and `select need_code from access_needs where need_code not in (select needs_code from v_live_lens_links where needs_code is not null)`. On `S`, 2026-11-13, the first returns every sensory, cognitive, neurological and mental-health code except `BLIND`, and the second returns every access need but one.
3. **`ALL` stands in for unnamed groups.** Item 4.1's tactile strips, item 6.2's resting areas and item 2.10's corridor are all "everyone" under the digest's tag, so the blind reading of a ramp and the fatigue reading of a landing interval are both lost. OD-31 already forbids this.
4. **A parameter only a mobility reading fills.** Ramp run length (parameter 12) is filled by `MOB` links from codes, while the source's own words for it are "resting areas": an effort and fatigue need (`A-EFFORT`), which reaches people with chronic pain, MS and energy-limiting conditions. Corridor and path width in item 1.2 is paired in the same clause with "colour contrast and distinctive patterns where there are changes in level": a low-vision provision on the route the owner placed with wheelchair users (R12).
5. **The medical lens is empty** (`select count(*) from base_taxonomy_medical`), so no figure can be found by condition; T-103 fills it and OD-15 is answered.
6. **A group named only in a clause.** Items 8.2 and 11.1 name blind people and cane users inside provisions that have no quantity. They can only be parameter-less statements today. Item 8.2 is also a harm statement ("so persons who are blind do not become disoriented") with no judgment row.
7. **Declining an element without minting its quantities removes a group from view.** The digest declined fourteen held terms as elements, among them hearing loop, visual fire alarm, pictogram signage, live captioning, grab bars and tactile surfaces (`select term_id, created_by_session from parameter_declinations` on `S`). Each decline is right by the TERM-089 precedent. Together they leave the Deaf and blind vocabulary as elements with no parameter under them, and nothing shows that. Bulk declination was also outside what a single-source digest needed; in the replay, decline only what a refused `add-parameter` would otherwise have promoted, and leave the rest to T-072 item 6.

**What surfaces this mechanically, from the pipeline's own rows.** Three derived reads, no curated list:
- *Lens by parameter*: for every active code of each lens registry and every active parameter, the count of live value-supplying figures linked to it, zeros included (a cross join of the registries with `base_parameters`, left-joined to `v_live_lens_links` and `source_value_extractions`). A row of zeros across a lens code is a group the catalogue cannot speak about.
- *Lens by figure*: figures whose only live link is an identity, and figures whose only identity is `ALL` or a parent code.
- *Group words without a parameter*: observations whose latest adjudication is `DEFERRED`, `NOT-OURS` or absent, per source, with their locator. Joined to P3's view.
- When T-029 lands: elements (declined terms) with no `element has parameter` pointer.

These are queries first (a convention in `/batch-done`'s report); a view only when T-034 or the renderer's Gaps section reads them. `v_coverage_lens` exists and is a different thing (it counts searches).

---

## 4. The critic's findings and the repair plan

**Order.** Replay on a fresh copy (verdict 1). Within the replay: admission and `pub_year` basis (F10); observations in one pass with every figure (F9, F14); adjudication (F1, F12, F16, the term minting of A2); lens rule (F4); extractions with comparators, roles and roots (F2, F6, F7); findings and edges (F3); no promotion (F5); no `absent` row on an unsettled concept (F8); scans recorded as readings (F13); typed columns (F15); engine once, after everything (F11); checks once; report generated from the final state.

| F | Disposition | Notes |
|---|---|---|
| F1 | **Repair; verified.** Observations 99 and 160 point at TERM-048; observation 68 is unadjudicated (`S`). OT-1 (line 4786) and OT-2 (line 6195) are as quoted | The repair plan's "DEFERRED pending the owner-approved term" is weaker than the ruling allows: OT-2 says "A data pull request mints the term from observation 68". This batch is a data pull request and may mint it, but OI-12 records it as "not yet a task" and the definition says "through a building" where REF-01037's route is exterior. Do not adjudicate 99 or 160 to it until AQ-6 is answered. Observation 99's surface form is cut from "Barrier-free unobstructed path of travel"; record the phrase as printed |
| F2 | **Repair; verified.** Parameter 4 already holds ramp-width figures, including a "between handrails" setting (`select extraction_id, ref_id, setting, claimed_value from source_value_extractions where parameter_id=4 and setting like '%ramp%'`) | Render p0005 confirms the 1500 is magenta and the 870 line blue. Item 6.2's first clause has no subject noun as printed ("With the ramp…"); extract with the text verbatim and a follow-up, not a silent reading as "width" |
| F3 | **Repair; verified** (no harm row, no edge, on `S`). The plan's two edges are right: a finding on door width `insufficient` to extraction 234; a finding on turning `insufficient` to a labelled standard | The same page-1 sentence is an admitted source's statement of which way is better for parameters 5 and 9, both of which have no direction (`select parameter_id from base_parameters where accessibility_direction is null`). `set-parameter-direction --ref-id` is available; whether a grey committee's assertion should set a direction is the judging session's call and must be named in the pull request |
| F4 | **Repair; verified.** Before the digest every `ALL` link was `carried`; the digest wrote the first judged ones (`select basis, count(*) from v_live_lens_links where identity_code='ALL' group by 1` on `S` and on canonical) | **The repair plan is wrong here.** Re-tagging the ramp figures and 231 to `MOB` on item 6.5's and page 1's words borrows a warrant again: item 6.5 names "larger chairs and scooters" for landings only, and page 1 names doors and turning only. By OD-31 and T-115 item 1: 243 takes the mobility identity on item 6.5's words; 234 to 237 keep `MOB` on the page-1 sentence, which names exactly their two quantities; 239 takes `A-EFFORT` on "resting areas"; the rest carry no identity and take ICF or need links only where their clause names a function or need. Figures whose clause names none wait on AQ-1 and are not written |
| F5 | **Repair.** Verified, with E2 and T-072 item 6 as further grounds (A5) | **"There is no retire path for a parameter" is false**: `retire-parameter` exists (`grep -n 'def retire_parameter' scripts/db.py`) and refuses only while a live determination or open gate stands. It is moot in a replay. There is no retire path for an extraction (T-078), which is the reason to replay |
| F6 | **Repair as planned** (`untraced` with the basis sentence), and write the relation edges of Q1 | The "wrapper or root" question is ruled by OR-19; see Q1. `code_floor_only` reading 0 on these cells is correct: the column is the cell's stratum, and a grey echo does not make a cell regulatory |
| F7 | **Repair, widened; one part rejected.** 228 is a `condition` with `condition_on` edges from 229 and 230. Every `=` should become a bound (R8), including the magenta "preferred" and "recommend" rows and 239 (an interval, so a ceiling), each with its warrant in the row | Rejected in part for 237: "turning radius of 1500x1500mm" can be parsed either way, and a square turning space stored as its side has precedent (extraction 211, `S`). Keep it on parameter 5 with `value_as_written` and a follow-up naming the ambiguity. I checked extractions 78 and 81 for the same threshold defect; they are sound (their text also states "The preferred maximum gradient is 1:20") |
| F8 | **Repair by not writing the row.** The plan's `preliminary` status still asserts that the source addresses LRV contrast | Whether "colour contrast" names TERM-011 is a vocabulary judgment under OR-17, not doctrine: the judging session decides and the pull request names it. The alias type `BROADER` exists for a phrase wider than its term. GAP-105 should not be an owner DEC |
| F9 | **Repair.** The three figures are in no observation quote (`select observation_id from observed_terms where ref_id='REF-01037' and context_quote like '%1700%'` and the like return nothing on `S`) | The chronology defect disappears in a replay. Run the checks once, after the last write |
| F10 | **Repair.** The cache-buster decodes to 2021-09-14; I could not find the string by a plain byte search of the PDF (it is presumably in a compressed stream) | Record `pub_year_note` with the basis; if the basis is the build date, say so |
| F11 | **Repair the report.** Spot-checked: the parameter 4 `ALL` lens holds figures from six sources, five of them tier 6 (`S`) | The engine's "from N source(s)" counts something other than sources in lens. That is a tool defect: file a gap; do not patch it in this batch (rule 10) |
| F12 | **Repair**, and add observation 110 | |
| F13 | **Repair.** Moot once nothing is promoted, since the targeted scans existed only for parameters 13 and 14 | |
| F14 | **Repair.** `observed_terms.surface_form` is "The phrase EXACTLY as the source writes it" | |
| F15 | **Repair** | `device_class` where item 6.5 and page 1 name scooters |
| F16 | **Sustained.** See A2 | |

**The critic's two withheld questions.** Co-1 standing of an advisory committee: correctly withheld; AQ-5. Wrapper or root: not the owner's; ruled by OR-19.

**What the critic got wrong or missed.** Withholding the root question; treating 237 as a misstatement; not noticing that the digest wrote no ICF or access-need link, which is the larger half of F4; not noticing the bulk declinations; not testing the repair route against `retire-parameter`.

**Colour classification.** I checked items 1.2, 1.5, 1.8, 1.9, 5.3, 6.1, 6.2, 6.5 and 7.1 to 7.4 against renders p0001, p0004 and p0005, two of which the critic did not open. They agree with the critic's list of Code-marked rows.

---

## 5. Proposals for incorporation, in dependency order

### 5.1 Research (this batch)

**P1. Replay the digest.** *Research.* Section 4's order. Reads: the batch's own migration. Without it: sixteen figures tagged "everyone", two elements as parameters and an invented reading of LRV absence enter the canonical database. Extends no task. Waits on AQ-1 for the figures whose clause names no one, on AQ-6 for observations 99 and 160; everything else proceeds.

### 5.2 Tooling (each its own pull request, before the research that uses it)

**P2. No new mechanism for floor and above-floor.** *Convention.* One paragraph in the skill's judgment section: a source's own "code" marking is root attribution (`untraced` or the code's `ref_id`, with the basis sentence); a source's own pairing of a higher figure with a floor is an edge. Reads: `v_value_independence`, T-068, the renderer's convergence sentence. Without it: a grey echo counts as independent corroboration of the code it copies. Extends T-071 (data) and T-035 (skills repair). No owner decision.

**P3. A reader for deferred adjudications.** *Tooling.* Add a fourth kind, `adjudication`, to T-079's `v_deferred_acts`: the observation, its source, its age, its rationale. Reads: `/batch-done`, the skill's resume list, T-072. Without it: a source's content for groups the catalogue lacks is recorded once and never met again. Extends T-079 (one more `UNION` arm). Count today: the command in A2, without the `where`. No owner decision.

**P4. The comparator convention (R8) and the lens-warrant convention (R13).** *Tooling, prose only.* Reads: every judging session. Without them: a "should be 1100" composes as a ceiling; a preamble warrants a whole document. Extends T-035.

**P5. Coverage reads.** *Convention first.* The three queries of section 3 in `/batch-done`'s report. Reads: the owner at the pull request; T-110 before first determinations. Without it: a book whose parameters are mobility quantities presents itself as covering disabled people. Extends T-034 if a verb is wanted; a view only when render reads it. No owner decision.

**P6. Refusal capture and disposition (Q10).** *Tooling.* The capture line at the writers' catch points; the `/batch-done` rule; the stage triage lines in the skill. Reads and consequence: Q10. New task; small. The register part waits on nothing; the "by hand into canonical" part waits on AQ-8.

**P7. `design_scale` states one fact.** *Tooling.* One change in the engine and T-056's item 3. Waits on AQ-2. Should be answered before T-056 executes.

**P8. A typed carrier for a figure's circumstance.** *Tooling, then research to re-tag.* Waits on AQ-3. Reads: the engine's branch partition (T-017) and the renderer. Without it: Q7's consequence. Measure the subject with `select parameter_id, count(distinct setting) from source_value_extractions group by 1`.

**P9. `T-060-design.md` constraint (R2) and T-029's `equivalent` (R10).** *Design text.* No code beyond those tasks.

### 5.3 Owner questions (OPEN; numbered AQ here, to be given register numbers by the integrator: `grep -n -E '^### OD-[0-9]+' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md | tail -1`)

### AQ-1  What lens does a figure carry when its clause names no person, function or need?
- **Status: OPEN (not yet asked).** Holds: part of P1; bears on T-115 and T-106.
- **Question.** OD-31 rules that a provision under a general disability heading carries "no identity, only its ICF and access-need lenses", and D-0182 requires at least one lens. The lens writer accepts a link only on words found in the clause, the heading or the study's participants. A clause such as "Corridors should be 1100mm" names no one and no function. What lens does it carry?
- **Why it is the owner's.** It decides who a figure is said to be for: the population taxonomy and the lens key.
- **Options and what follows.**
  - (a) The judge assigns ICF and need codes from the function the *parameter* serves, with the parameter's definition as the warrant. *Then:* every such figure can be written; the crossing is a property of the parameter, so by rule 5 it is held once on the parameter and derived for figures, which is a schema change.
  - (b) The document's own stated audience is the warrant (here: "people with low vision, people who use different mobility devices"). *Then:* every item of a document carries the same groups, including items that do not concern them.
  - (c) The figure is not written until a clause names someone; the phrase stays an observation and a gap is filed. *Then:* checklists and most code clauses contribute observations only.
  - (d) It keeps `ALL` until re-tagged (T-115's present fallback). *Then:* T-115 step 3 stays blocked, as it already says.
- **Recommendation.** None given.
- **Answer in one line.** `AQ-1: function of the parameter` · `AQ-1: the document's stated audience` · `AQ-1: not written` · `AQ-1: keeps ALL until you rule per row`
- **Where the evidence is.** Line 6044; `tasks/T-115-retag-all-rows.md` section 4 item 2; `grep -n 'def _require_lens_warrant' -A12 scripts/db.py`.

### AQ-2  What does `design_scale = 'universal'` state?
- **Status: OPEN (not yet asked).** Holds: P7; should precede T-056.
- **Question.** The engine writes `universal` when a determination rests on codes alone. OD-31 says `ALL` leaves the identity lens, "universal being stated once, by design_scale". Today a wheelchair-keyed cell built on codes reads `universal`. Which fact does the column state?
- **Why it is the owner's.** Design Modes are the ledger's first rule (line 14) and Universal Mode is defined there as both "Universal Design" and "Code Compliance".
- **Options and what follows.**
  - (a) Whom it is for: `universal` when the determination names no identity. *Then:* "rests on codes only" is read from `regulatory_stratum_only`; the engine's G1 line changes; a code-only wheelchair cell reads `population` with the ○ flag.
  - (b) What it rests on: `universal` means code-only, as now. *Then:* OD-31's "universal" needs another home, and a figure for everyone is told apart only by having no identity.
  - (c) Both, as two columns. *Then:* a schema change; one already exists.
- **Recommendation.** None given.
- **Answer in one line.** `AQ-2: whom it is for` · `AQ-2: what it rests on` · `AQ-2: two columns`
- **Where the evidence is.** `grep -n 'design_scale = SCALE_UNIVERSAL' scripts/assess/assess_cell.py`; lines 14 and 6044; `tasks/T-056-all-leaves-identity-lens.md` section 4.

### AQ-3  Building type, the other circumstances of a figure, and where an element lives
- **Status: OPEN (not yet asked).** Holds: P8.
- **Question.** (a) You ruled three building levels on 2026-08-27 ("Building types (eg residential, commercial), room types…, construction elements…"). None is linked to a figure; building use, new or existing, and interior or exterior sit together in a free-text cell the engine does not read. Is building type a branch within one determination, or part of what a determination is keyed on, and what is its vocabulary? (b) Is the construction-element level a table of its own, or the element terms the catalogue already holds?
- **Why it is the owner's.** Jurisdiction and scope vocabulary; the key of a determination, ruled twice; a prior ruling's ACTION ("Three tables") that a later answer (OR-14, "typed term pointer") may have overtaken.
- **Options and what follows.**
  - (a1) A typed circumstance on the figure, shown as a branch; a small project vocabulary seeded from your examples and extended by data with a warrant, each instrument's scope phrase adjudicated to it. *Then:* one determination per parameter and lens, with branches; "public" is adjudicated per instrument.
  - (a2) Part of the key. *Then:* one determination per building type; the key ruled on 2026-08-26 and 2026-08-28 changes.
  - (a3) Leave it in `setting`. *Then:* dwelling and public-building figures compose into one headline.
  - (b1) Elements are terms; `base_building`'s third level is derived from them. *Then:* one home; the 2026-08-27 ACTION is amended for that level.
  - (b2) A separate `base_elements` table. *Then:* each element exists as a term and as a row, and one must point at the other.
- **Recommendation.** None given.
- **Answer in one line.** `AQ-3: (a1|a2|a3); (b1|b2)`
- **Where the evidence is.** Lines 2053 to 2070, 2425 to 2450, 4699, 5643; `select setting from source_value_extractions where parameter_id=9`.

### AQ-4  May a source that is not a code add a parameter?
- **Status: OPEN (not yet asked).** Holds: nothing in P1 (terms may be minted); bears on T-072.
- **Question.** You ruled that the list of quantities is seeded "From the codes held" (OR-13). REF-01037, a grey checklist, states figures for quantities no held parameter takes (handrail height and diameter, stair rise and run, control heights, toilet height, knee space, door dwell time). May such a source promote a parameter, or only mint the term and wait for a code?
- **Why it is the owner's.** It decides what the guidebook's pages can ask about and on whose word.
- **Options and what follows.**
  - (a) Any admitted source may, in its data pull request, under OR-17's conditions and T-020's kind. *Then:* the catalogue grows with each reading; names come from whichever source was read first until a judge picks (OD-38).
  - (b) Term only; a parameter needs a held code or standard that states the quantity. *Then:* the terms wait on T-105 and T-072, and P3's view keeps them visible.
  - (c) Term only, promoted when two independent sources state it. *Then:* a recurrence rule to build and maintain.
- **Recommendation.** None given.
- **Answer in one line.** `AQ-4: any admitted source` · `AQ-4: a code or standard must state it` · `AQ-4: two independent sources`
- **Where the evidence is.** Lines 4677, 4698, 4713; `tasks/T-072-seed-quantities-from-codes.md` section 4.

### AQ-5  Does a municipal accessibility advisory committee's own document carry Co-1 standing?
- **Status: OPEN (not yet asked).** Holds: nothing; REF-01037 stays T3 grey meanwhile.
- **Question.** The payload does not state the committee's membership. If membership of disabled people can be shown from another retrieved source, is the committee's checklist Co-1, and what proof is required?
- **Why it is the owner's.** A tier, and the meaning of co-production (`CLAUDE.md` section 6). It adjoins the open second edge of OR-5b (how a lived-experience publication with no reporting guideline is shown to be sound).
- **Options and what follows.** (a) Never: an appointed advisory body is not a representative organisation. (b) Yes, when a retrieved source shows disabled members authored it, recorded as co-producers. (c) Decided per source by the owner.
- **Recommendation.** None given.
- **Answer in one line.** `AQ-5: never` · `AQ-5: yes, on retrieved proof of authorship` · `AQ-5: per source`

### AQ-6  "Barrier-free path of travel" as REF-01037 uses it
- **Status: OPEN (not yet asked).** Holds: observations 99 and 160 in P1.
- **Question.** You approved the definition "A circulation route through a building that a person using a wheelchair or other mobility device can travel without barriers" (OT-2). REF-01037 uses the phrase for the route from parking to the entrance, outdoors, and attaches to it a provision for "colour contrast and distinctive patterns where there are changes in level". Do these two observations name the term you approved?
- **Why it is the owner's.** The term, its definition and its placement are the owner's words (OT-1, OT-2), and on 2026-10-29 (fifth) the owner separated it from a route "navigated by someone who is blind".
- **Options and what follows.** (a) Yes; the scope note records the exterior use. (b) Yes for the route; the contrast provision is a separate figure for blind and low-vision people on the same route. (c) No; it names something wider, to be adjudicated like "accessible route".
- **Recommendation.** None given.
- **Answer in one line.** `AQ-6: names the term` · `AQ-6: names the term; the contrast provision is separate` · `AQ-6: names something wider`
- **Where the evidence is.** Lines 4786, 4802, 6195; `governance/owner-browser.yaml` (`grep -n 'id: OT-2' -A12`); PDF items 1.2 and 2.1.

### AQ-7  Bulk declination in a single-source batch
- **Status: OPEN (not yet asked).** Holds: nothing; the replay declines only what it must.
- **Question.** May a research batch decline held terms as parameters in bulk when a source merely mentions them, or is that T-072's (item 6) to do once, across the catalogue?
- **Why it is the owner's.** OR-17's bulk approval names phrases, names and aliases; E12 names functional-axis and method terms; neither names elements.
- **Options and what follows.** (a) Any batch may, with a reason per term. (b) Only the catalogue-wide task. 
- **Answer in one line.** `AQ-7: any batch` · `AQ-7: the catalogue task only`

### AQ-8  When a writer cannot hold content, may an agent write the canonical row by hand?
- **Status: OPEN (not yet asked).** Holds: nothing in P6's register part.
- **Question.** You proposed a register of what the pipeline could not execute, "alongside having an agent fix it by hand with correct context so we aren't losing content". Does "by hand" mean the agent writes the intended row and a proposed amendment into the register, to be replayed through the writer once it is fixed, or writes the row into the database directly?
- **Why it is the owner's.** The second reading sets aside `CLAUDE.md` rules 3 and 10, which only a live owner statement can do.
- **Options and what follows.**
  - (a) Into the register; replay later. *Then:* no content is lost, the batch is not held up, and every canonical row has still passed a writer's refusals.
  - (b) Into the database, flagged, with the register entry beside it. *Then:* the content is usable at once; a hand-written row bypasses the refusals that exist to stop a mis-typed or invented value, and rules 3 and 10 gain a stated exception with its limits to be written.
- **Recommendation.** None given.
- **Answer in one line.** `AQ-8: into the register, replayed through the writer` · `AQ-8: into the database, flagged, within these limits: <…>`
- **Where the evidence is.** `CLAUDE.md` rules 3 and 10 and section 4; Q10 above.

---

## 6. Not verified, assumed, and premises

**Not verified.**
- [NOT VERIFIED] Renders p0002, p0003, p0006, p0007, p0008 were not opened by me; colour there rests on the critic (p0002) or the text layer.
- [NOT VERIFIED] The critic's full JSON; I worked from the hand-off's condensed section 4.
- [NOT VERIFIED] `batch.sql`, `digest-log.jsonl`, `items.json` and the `checks-after-*` files were not read; `DIGEST-REPORT.md` was read by headings and search only.
- [NOT VERIFIED] No check suite was run. The only script run was `joined_cells_census.py`, read-only, against `S`.
- [NOT VERIFIED] How `echo_of` is written and whether it has a vocabulary; I did not prescribe it.
- [NOT VERIFIED] What the engine's "from N source(s)" counts (F11); I report the mismatch only.
- [NOT VERIFIED] `T-028-design.md`, `T-018-design.md`, `T-102-design.md` and `DELEGATED-RESOLUTIONS.md` beyond the lines quoted; T-020, T-030, T-034, T-057, T-067 beyond their header and problem statement.
- [NOT VERIFIED] The plan files were being edited while I read them; task numbers and dependencies are as read.
- [NOT VERIFIED] Whether the Alberta Building Code or the Barrier-Free Design Guide is in the research scope; the leads were filed by the coordinator and not opened.
- [NOT VERIFIED] The three lines of the session's command log that contain "REFUS" were counted (`grep -c REFUS …/commands.jsonl`) and not read.

**Assumed.**
- [ASSUMPTION] The two coordinator messages carrying Q10 quote the owner faithfully; the words are not in the ledger and should be appended there before anything rests on them.
- [ASSUMPTION] "PDT" is PDF, as the hand-off reads it.
- [ASSUMPTION] The page-1 sentence on wheelchairs and scooters warrants a mobility link for door width and turning figures because it names those two quantities; a stricter reading of D-2 ("the figure's own words") would move 234 to 237 under AQ-1 as well.
- [ASSUMPTION] A replay is practical because the drivers exist; I did not run them.

**Premises in the owner's questions that the repository does not bear out.**
- Q1 supposes a best-practice column existed. It existed in a report table and a gap's proposal, never in the schema.
- Q6 treats universal, population and person as three working design modes. The engine writes two; `person` is never written, and `universal` is written from the evidence's stratum, not from whom the value is for (AQ-2).
- Q6 also supposes values differ by ICF code or access need in the data. The links are almost all identity links (section 3).
- Q7's "public" is not a building type in the owner's 2026-08-27 examples; in the held instruments it is a legal scope phrase.
- Q9's example cannot be represented today for a reason beyond the missing parameters: "handrails on one or both sides" is a count, and no count kind is held.
- Q10's "a register" already exists as the `gaps` table; what does not exist is capture of the refusal and a rule that it be disposed.
