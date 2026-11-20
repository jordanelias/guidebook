# Open decisions, third adjudication: every question still open after the third tooling stack, adjudicated for provenance and walkability

_Written 2026-11-19 (UTC) by an Opus-class adjudicator, on the owner's instruction of 2026-11-19, relayed by the coordinator of `session_2026-11-18-remediation-batch-1-tooling-stack-2`: "have Opus adjudicate all open decisions based upon long-term integrity re provenance and walkability as well as context from my prior rulings". Planning only: no script, schema, check, migration, database row, ledger line or task file was changed. Canadian English. Every figure is given as the command that produces it; re-run it. Checked against branch `ccr-cc893571-i4lug4` at `41b67411` (pull request #240, open, untouched), schema version `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('pragma user_version').fetchone())"`. Form and discipline follow `PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md`. The ledger outranks this file._

## 0. Rule 0 on contact, and what the delegation does not reach

**The owner's instruction of today supersedes, for the items below and on contact (CLAUDE.md rule 0), every ledger sentence that said an item was not to be resolved under delegation.** Named, so the supersession is recorded and not implied: the ACTION (3) of "Owner statements 2026-11-18 — OD-71 … and OD-72 …" ("Ask the owner the open parts in their plain form; do not resolve them under delegation"); ACTION (3) of "Owner statement 2026-11-18 (third) — OD-69"; ACTION (4) of "Owner answers 2026-11-17 — OD-68 … OD-69 … OD-70"; ACTION (4) of "Correction and registration 2026-11-15" (OD-67); the "Registration 2026-11-14" sentence "None is to be resolved under delegation" (OD-62); and the referrals of 2026-11-13 (OD-46 to OD-54), which were a delegate's own referrals and never an owner's prohibition. The ledger is not edited here; the draft entry of section 4 records it.

**What the delegation does not reach.** It does not move CLAUDE.md §8: content and doctrine (mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction, licensing, trajectory) stay the owner's to ratify. For each such item the resolution below is a **recommended default the owner must ratify**, with what is safe meanwhile. A ratification act that is the owner's by its nature (OD-17, "ratify the contract") is not adjudicable at all.

**The test applied to every item.** PROVENANCE: one home per fact; a typed value warranted by the source's own words, never by memory or a substring; nothing fabricated; history retired in place ("retire in place then", owner ruling 2026-09-16). WALKABILITY: the pipeline "can be run in all directions at any stage in such a manner where we can dynamically research, adjudicate, synthesize, specify and render across a multitude of languages and jurisdictions" (owner, 2026-11-12), with "no hard coded behaviours" and no "dead ends or whatever" (owner statements 2026-11-12 (seventh)); a rule that blocks a legitimate walk, or lets a walk reach a cell through an unwarranted step, fails.

## 1. How the list was derived

1. **The three sweep lists**, read in full: every item under "Not repaired", "Open", "Stopped", or marked OWNER'S, owner question or design question (`scratchpad/session_2026-11-15-remediation-stack/sweep-list.md`, `scratchpad/session_2026-11-16-remediation-batch-1-tooling-stack/sweep-list.md`, `scratchpad/session_2026-11-18-remediation-batch-1-tooling-stack-2/sweep-list.md`; abbreviated S15, S16, S18 below with line numbers).
2. **The register**: every OD whose last status line is neither ANSWERED BY THE OWNER nor RESOLVED UNDER DELEGATION with a satisfied check: `for n in $(seq -w 1 72); do grep -F "OD-$n STATUS:" references/project-standards.md | tail -1; done` and the same for `CHECK:`. Every delegated resolution's check reads `not required` or `confirmed with corrections applied`. Open: OD-17 (DEFERRED BY THE OWNER), OD-46, OD-47, OD-48, OD-51, OD-52, OD-54, OD-62, OD-67, OD-69, OD-72 (REFERRED BACK), and OD-71's "not decided" residue.
3. **Every ledger `REFERRED BACK TO THE OWNER`**: `grep -n "REFERRED BACK" references/project-standards.md`; each id whose latest status still reads so is in (2).
4. **Pull request #240's eleven "Open owner questions"** (read through `gh api repos/jordanelias/guidebook/pulls/240`); each maps onto an S18 item.

Items that are a limit, a datum or a process note rather than a decision are numbered in the table and marked LIMIT, with their disposition in one line; only decisions get the six-part adjudication. Items that later commits already closed are marked CLOSED with the evidence.

**Could not place, or outside the four sources.** `OPEN-ITEMS-PLAN.md` OI-55 holds twelve owner questions "none yet asked" (`sed -n 124p workplan/2026-11-12-bidirectional-pipeline/OPEN-ITEMS-PLAN.md`); parts (4), (5), (6), (7) and (10) are adjudicated here because the four sources carry them (as OD-46, OD-68, item 14, item 21, item 72); parts (1), (2), (3), (8), (9), (11) and (12) are outside the instructed derivation and are not adjudicated. The OR-5b edges enter only as item 67.

## 2. The numbered list

| # | Id | The question in one line | Source |
|---|---|---|---|
| 1 | OD-17 | Ratify the corrected pipeline contract | WORKPLAN §8 L601 |
| 2 | OD-46 | Map codes missing from the jurisdiction registry: admit as declared out-of-scope, or remove their pairs | WORKPLAN L983 |
| 3 | OD-47 | Lens of a figure whose clause names no person, function or need | WORKPLAN L999 |
| 4 | OD-48 | What `design_scale = 'universal'` states | WORKPLAN L1016 |
| 5 | OD-51 | Co-1 standing of a municipal advisory committee's document | WORKPLAN L1064 |
| 6 | OD-52 | Does REF-01037's "barrier-free path of travel" name the owner's term | WORKPLAN L1079 |
| 7 | OD-54 | "By hand": into the refusal register, or into the database | WORKPLAN L1109 |
| 8 | OD-62 | Rename "best practice" to "ideal" (optional) | WORKPLAN L1226 |
| 9 | OD-67 (+S18 T-126 item 4) | Confirm T-128's full list of population-to-ICF rows in one answer | WORKPLAN L1287; S18 L124 |
| 10 | OD-69 | The form of the topic-area list: free text or rows extended by data | WORKPLAN L1309; ledger L7851 |
| 11 | OD-72 (+S18 T-028 item 5; PR q3) | Displayed name: what an appearance is, tolerance, tie, no form, first met outside English, CSA/ISO combination, where the cell lives | WORKPLAN L1336; S18 L17-20, L40 |
| 12 | OD-71 (a); PR q1; S18 T-083 item 1 | Does the base repeat a source's quoted words, or only the locator | WORKPLAN L1334; S18 L90 |
| 13 | OD-71 (b); PR q2 | Does OD-71 supersede the 2026-10-30 basis of `base_parameters.direction_ref_id` | S18 L60 |
| 14 | OD-71 (c); PR q2; OI-55 (6) | `term_aliases.observation_id`, and an absorbed phrase: attested form or search aid | S18 L59-60 |
| 15 | T-031; PR q4 | May retained clause text enter git history | S18 L73 |
| 16 | T-031; PR q4 | The clause inventory's matching rule | S18 L79 |
| 17 | T-126; PR q5 | The tier floor (4 and above) for the `context` lens | S18 L121 |
| 18 | T-126; PR q5 | The strength of the `context` warrant | S18 L122 |
| 19 | T-126; PR q5 | A `context` link on a figure whose clause names the group, or on a superseded source | S18 L123 |
| 20 | T-056 / OD-31; PR q6 | `ALL` still accepted as an identity under `named_in_text` and `heading` | S18 L130 |
| 21 | OI-55 (7); PR q7 | Do `add-lens-link` and `retire-lens-link` refuse while a live determination uses the figure | S18 L151 |
| 22 | T-078; PR q7 | A pair whose only figure is withdrawn reads READ-NOTHING-FOUND and owes nothing | S18 L150 |
| 23 | T-083; PR q8 | An open determination gate refuses a parameter its kind | S18 L91 |
| 24 | T-083; PR q8; OI-78 | `merge-parameter` changes the kind under stored figures | S18 L92 |
| 25 | T-119; PR q9 | Three pairs for the weighted-strength anchor model, not named by the plan | S18 L110 |
| 26 | T-119; PR q9 | A borderline passage left unpaired in DR-2026-07-21 tier-doctrine | S18 L112 |
| 27 | T-119; PR q9 | The attestation names a session record not yet written | S18 L106 |
| 28 | T-134; PR q10 | A unique ledger quote fails the day a later entry re-quotes it | S18 L168 |
| 29 | T-134; PR q10 | A deleted passage re-embedded elsewhere passes as MOVED, exit 0 | S18 L169 |
| 30 | T-027; PR q11 | What warrants `edition` or `original_title` on a source with no DOI | S18 L138; S15 L60, L67 |
| 31 | T-030 | No route to add a unit by data, and no warrant | S18 L49 |
| 32 | T-030 | `degrees`, a non-linear unit | S18 L50 |
| 33 | T-030 | The stale-determination check is blind to a rule change | S18 L51 |
| 34 | T-030 | Value rows whose unit has no `base_units` row | S18 L53 |
| 35 | T-030 | `specifications.value_min`/`value_max` stored as REAL | S18 L63 |
| 36 | T-030 | Showing an exact, marked conversion where the increment would cross both bounds | S18 L64 |
| 37 | T-029 | The relation table accepts contradictions | S18 L29 |
| 38 | T-029 | Must a warrant concern its two terms | S18 L28 |
| 39 | T-029 | The `reason` cell, and relations of a merged term | S18 L32, L35 |
| 40 | T-028 | The judge is any non-blank string | S18 L11 |
| 41 | T-020 | The warrant's digit test admits a year or clause number | S16 L10 |
| 42 | T-020 | `insert_parameter` under a blank session | S16 L11 |
| 43 | T-022 | `gaps.status` has no CHECK (B10) | S16 L21 |
| 44 | T-022 | B13 one carrier; B11 and the skim edges share a carrier | S16 L22-23 |
| 45 | T-049 | Must a review's session differ from the translator's | S16 L35 |
| 46 | T-049 | A translation equal to its original | S16 L36 |
| 47 | T-049 | The number rule (grouping, reorder, unit, comparator) | S16 L37 |
| 48 | T-049 | A stale `requested` translation has no closing verb | S16 L38 |
| 49 | T-050 | Retirement columns accept empty strings | S16 L48 |
| 50 | T-050 | Two readers disagree on a retired connection id | S16 L50 |
| 51 | T-089 | The refusal signature rule groups poorly | S16 L59 |
| 52 | T-089 | A parked refusal whose gap is closed reads undisposed | S16 L60 |
| 53 | T-089 | Cross-stage verbs get no cue; the cue is broad; `ENGINE_VERB` | S16 L61-63 |
| 54 | T-093 | A future notation-family member widens the reformat silently | S16 L74 |
| 55 | T-093; OI-78 | "What the row said before" lives in a note | S16 L75 |
| 56 | T-041 | Duplicate `_tables` helpers; differing helpers | S15 L6-7 |
| 57 | T-007 | A non-member value through the Python entry raises a raw CHECK error | S15 L9 |
| 58 | T-009 | Unspaced scripts as one token; numerals as words in names | S15 L11, L13 |
| 59 | T-010 | May bodies of law and cost terms be declined as parameters | S15 L15 |
| 60 | T-010 | `amend-term` cannot mint a domain; a sole carrier's move is one-way | S15 L16-17 |
| 61 | T-011 | The engine links the newest retired row, one retired for error included | S15 L23 |
| 62 | T-015 | A source in a language `lang_jur_map` does not hold; NULL read as English | S15 L28, L30; S15 L74 |
| 63 | T-015 | Language spelling split (upper and lower case) | S15 L29 |
| 64 | T-001 | A stale research batch reverts a correction `main` made | S15 L32 |
| 65 | T-001 | `ratified` and `status` in the contract header are untied | S15 L35 |
| 66 | T-052 | Out-of-scope instruments: a new flag, or `add-code-lead` | S15 L43-44 |
| 67 | T-003 | OR-5b: close, or split | S15 L39, L56 |
| 68 | T-002/T-042 | Where the determination machine sits; the specification entry's order | S15 L46-48 |
| 69 | T-002/T-042 | The scope of the existence gate | S15 L49 |
| 70 | OD-11 (S15 T-051) | "Count it as a member of each stage it carries" is unmet | S15 L54; S16 L61 |
| 71 | T-021 | QUESTION gates: owner-page wording, timestamp formats, two homes of a refusal | S15 L64 |
| 72 | OR-1c; OI-55 (10) | Does the link table cover determinations | S15 L56 |
| 73 | T-054/T-048 | `register-root`'s type unread; `root_ref_id` and `root_id` both set; holes of 135 | S15 L68 |
| 74 | T-055 | A parent cell's function path reads the parent's code only | S15 L71; BATCH-1 L30 |
| 75 | T-034 (/code-review) | The approval of a pair, scope or identity is checked and stored nowhere | S15 L74 |
| 76 | T-027 | `code_currency_status` vocabulary lives in a governance sentence | S15 L61, L68 (f) |
| 77 | T-027 | `v_evidence_authors` full given name | S18 L141; S15 L60 |
| 78 | T-076; T-126 | A free-text reason passes any non-blank text (`--deferred-reason x`) | S15 L71 (b) |
| 79 | T-028 | LIMIT: junction remap unproven at rest; no attested alias exists | S18 L12-13 |
| 80 | T-029 | LIMIT: probe record lost; census examined no column | S18 L30-31 |
| 81 | T-030 | LIMIT: kind not read against unit; process `rm` | S18 L52, L54 |
| 82 | T-031 | LIMIT: census; key by `scan_id` (plan edit); `--deep`; new view; `reread_flagged` subset | S18 L74-81 |
| 83 | T-083 | LIMIT: locator CHECK copied in three tables; graph; `--deep` | S18 L93-95 |
| 84 | T-119 | LIMIT: shared paragraph; one BY sentence; prose callers to T-120 | S18 L107-109 |
| 85 | T-126 | LIMIT: ICF-only warning; CJK matcher; graph; unexamined | S18 L125-127, L131 |
| 86 | T-078 | LIMIT: M04; REPLACE un-retires; unproven views; `repoint-extraction-relation`; T078-24 | S18 L152-159 |
| 87 | T-134 | LIMIT: no quote floor; `verify_atoms`; PIP-01; process; TSVs publish cited source | S18 L170-174 |
| 88 | T-027 | LIMIT: premise partly stale; notes true | S18 L139-140 |
| 89 | T-020/T-022 | LIMIT: typed count in 143; carriers empty; graph; B9/B14 | S16 L12-13, L20, L24-25 |
| 90 | T-049/T-050/T-089/T-093 | LIMIT: census; tests on fixtures; no real record; derived-family test; engine premise | S16 L34, L39-40, L49, L51-52, L64-65, L72-73, L76 |
| 91 | S15 remainder | LIMIT or CLOSED: T-006 x3, T-011 replay counts, T-001 steps 5 and zero-selection, T-003 page, OR-17b, gloss, DR line 452, "RED on main", empty lists, squash declined, simplify skips, `.ignore` glob | S15 L19-24, L33-41, L50-51, L57, L74, L76-77 |

Count the rows: `grep -c -E '^\| [0-9]+ \|' workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md`.

## 3. The adjudications, in the table's order

Format: **Q** question; **O** options, each with what wrong thing reaches the guidebook; **R** resolution and warrant; **C** confidence; **Res** reserved by §8; **F** follow-on. Items adjudicated together say so.

### 1. OD-17: ratify the corrected contract
**Q** Does the owner ratify `governance/pipeline-contract.yaml` as corrected by T-002 and T-022? **O** (a) ratify: the header says so; (b) not yet: `ratified: false` stays (`grep -n '^ratified' governance/pipeline-contract.yaml`). Neither puts a wrong thing in the book. **R** NOT ADJUDICABLE: ratification is the owner's act (the owner selected "Ratify after T-022 merges, once I have read the corrected contract", `grep -n -F "OD-17: the owner will ratify" references/project-standards.md`). Its condition is now met: T-022 merged in #238 (`git log --oneline origin/main --grep=T-022`). **C** high. **Res** yes, by its nature. **F** the coordinator puts it to the owner with `git diff <pre-T-002 commit> origin/main -- governance/pipeline-contract.yaml`; no task.

### 2. OD-46: map codes missing from the registry
**Q** Pairs in `lang_jur_map` name jurisdiction codes the registry never declared (count: the register's command, `select count(distinct l.jurisdiction), count(*) from lang_jur_map l left join base_jurisdictions b on b.jurisdiction_code=l.jurisdiction where b.jurisdiction_code is null`). Admit or remove? **O** (a) admit as declared, scoped-out codes: nothing lost; scope stays OD-04's; (b) remove the pairs: needs a hard-delete exception to "retire in place then", erasing the record of what was searched. **R** (a). Provenance: a logged search keeps a resolvable jurisdiction; removal erases history the 2026-09-16 ruling forbids. OD-04's owner answer ("UN out; sub-national counts toward its country") is about scope, which a declared-but-out code respects. **C** high. **Res** yes (jurisdiction). Default (a); safe meanwhile: T-084 and T-085 wait; nothing is written. **F** T-084 executes (a) on ratification; then T-085.

### 3. OD-47: the lens of a clause that names no one
**Q** A clause such as "Corridors should be 1100mm" names no person, function or need; what lens does it carry? **O** (a) the parameter's function, warranted by our definition: a lens from our words, not the source's, and a schema change; (b) the document's stated audience for every item: groups attached to items that do not concern them; (c) not written: content lost, a dead end; (d) `ALL` until re-tagged: contradicts OD-31. **R** For code values this is decided by the owner: "3 all code values will have a lens even if it's not explicitly stated. use contextual judgment" (Owner answers 2026-11-14 (fifteenth set)) and "at the moment of recording the row is when you will have best idea of context" (sixteenth set, later); T-126 built it. For other figures: **(b) narrowed to a per-item judgment**: the recording session assigns, by the `context` basis, only the groups the document's own stated audience names and the item plausibly serves, quoting the document's audience words in `basis_reason`. Provenance: the warrant is the source's own words, per item, never our definition. Walkability: no dead end. This extends item 17's floor for this case only. **C** medium (it widens a mechanism the owner named for code values). **Res** yes (population taxonomy). Default as above; safe meanwhile: T-087's parked figures stay parked; code values take T-126's default. **F** on ratification, T-126's `context` tier floor gains an exception for a clause naming no one with a quoted audience (tooling, small); T-087 replays its parked argv.

### 4. OD-48: what `design_scale = 'universal'` states
**Q** Is `universal` "whom it is for" (no identity) or "what it rests on" (codes only)? **O** (a) whom: "rests on codes" is read from `regulatory_stratum_only`; (b) what it rests on: two columns state one fact, and "universal" for a figure for everyone has no home; (c) two columns: one already exists. **R** (a). Warrant: the owner selected "Heading's group; ALL leaves the identity lens" (`grep -n -F "Heading's group" references/project-standards.md`), and the answer line recorded from that choice reads "universal being stated once, by design_scale" (the recorder's words for the option's meaning, not the owner's own, which is why this stays the owner's; `DECISION-CLOSURE.md` §10 puts it on that premise); the conflicting record cited by the referral, DR-2026-07-12 G1(a), now carries a SUPERSEDES pair from the T-119 unification (`grep -n -F "T4–6-only determinations are Universal-Mode" references/project-standards.md`). Rule 5: under (b) `design_scale='universal'` and `regulatory_stratum_only=1` are one fact in two cells. **C** medium-high. **Res** yes (Design Modes, mission doctrine; the first ledger RULE). Default (a); safe meanwhile: T-056 item 3 and 3a wait. **F** T-056 split (item 20); its engine part opens on ratification.

### 5. OD-51: a municipal committee's Co-1 standing
**Q** If a retrieved source shows disabled people authored a committee's checklist, is it Co-1? **O** (a) never: a co-produced work is graded as grey and its makers erased; (b) yes, on retrieved proof of authorship, co-producers recorded as authors; (c) per source by the owner: a queue with no rule. **R** (b). Warrant: CLAUDE.md §6, "Co-1's warrant is co-production. The disabled people who produced the work are part of the evidence"; proof must be a logged retrieval (§5(c)), never inference from a committee's name. **C** medium. **Res** yes (evidence-tier definitions). Default (b); safe meanwhile: REF-01037 stays T3 grey. **F** none until ratified; then a research re-grade.

### 6. OD-52: "barrier-free path of travel" in REF-01037
**Q** Do the two observations name the owner's approved term? **O** (a) yes with a scope note; (b) yes, and the contrast provision is a separate figure for its own lens; (c) no, something wider. Wrong things: (a) files a blind-and-low-vision provision under a mobility term; (c) leaves a held term unlinked from its use. **R** (b). Warrant: "Equivalence is judged per occurrence, by the sense the source gives the form" and "Conflation is recorded, not resolved" (Owner statements 2026-11-06 (sixth), readings of "there is a lot of conflation in literature"); the owner separated the term from a route "navigated by someone who is blind" (`grep -n -F 'navigated by someone who is blind' references/project-standards.md`). **C** medium. **Res** yes (the owner's term and definition). Default (b); safe meanwhile: the two observations stay DEFERRED. **F** T-087 (research) after ratification.

### 7. OD-54: what "by hand" means
**Q** Does an agent write the intended row into the register for replay, or into the database? **O** (a) register, replayed through the writer; (b) database, flagged: a row that passed no refusal, against rules 3 and 10. **R** (a). It is what T-088 and T-089 built and the only reading that keeps every canonical row behind a writer's refusals (CLAUDE.md §4, "`db.py` refuses, and that is its whole value"). **C** high. **Res** no: (a) relaxes nothing; (b) would need the owner. **F** none.

### 8. OD-62: rename "best practice" to "ideal"
**Q** Write "ideal" in place of "best practice"? **O** (a) no rename; (b) rename: a migration and a caller sweep for no change of meaning. **R** (a), the registered default. Warrant: "my definition of best practice IS the same as ideal IS the same as most accommodating" (U1 of the unification entry). Meaning is fixed; a rename moves only words. **C** high. **Res** the book's vocabulary is content, but the registration made (a) the default if unanswered; recorded as standing. **F** none.

### 9. OD-67 (with S18 T-126 item 4): T-128's list in one answer
**Q** May the full batch list of new population-to-ICF rows be confirmed in one answer? **O** (a) one answer; (b) row by row: same rows, slower; (c) no rows: the owner's own reach and seated-posture defaults propose nothing (`d415`/`A-REACH` today, S18 L124). **R** (a), with VES withheld (OD-37: "MOVE and VES are access needs"). **C** high. **Res** yes (population taxonomy). Safe meanwhile: no map row; T-126 still writes judged identities. **F** T-128 prepares the list on a scratch copy.

### 10. OD-69: the form of the topic-area list (adjudicated with item 60)
**Q** Free text, or rows extended by data with a warrant? **O** (a) free text: "circulation", "Circulation", "circulation route" drift into near-duplicate classes, the owner's Q2 harm; `NON_QUANTITY_DOMAINS` stays a typed list in code (rule 8); (b) rows extended by data with a warrant, no closed list. **R** (b). Owner's words: "the overall class of a parameter eg circulation … the project is supposed to be like that" (Owner answers 2026-11-17) and "list of topic areas is not fixed" (Owner statement 2026-11-18 (third)). (b) honours "not fixed" (any session adds a class with a warrant, no owner gate) while giving one home that `terms.domain` points into and from which the non-quantity rule is derived (a typed column on the class row, moved from the constant by the migration, not curated). It also closes item 60: a class row persists when its last carrier moves. Seed rows from the values in use (`select domain, count(*) from terms group by 1`) as recorded usage, each warranted "in use at migration"; renaming or merging a seeded class is a judged act through T-130's candidates. **C** high on the form; which in-use values are classes and which are kinds a parameter may not be is moved, not decided. **Res** no: the owner answered the substance; the form is schema (Layer 1). **F** T-135 rewritten (tooling): a `term_domains` table with a warrant and an admits-parameter cell, `terms.domain` a foreign key into it, `add-domain` with a warrant, `dbcore.NON_QUANTITY_DOMAINS` derived from it.

### 11. OD-72: the displayed name (with S18 T-028 item 5)
**Q** How is the displayed name computed from counted appearances with CSA and ISO first, and what of ties, no form, and a concept first met outside English? **O** per part: an appearance = any `term_aliases` row (seeds would vote, against E4); = an attested row (seeds and unrecorded never vote); = a source (one per URL). CSA/ISO = wins / tie-break only / weight. Tie = a tolerance band / a named judge. No form = our label / nothing. First met outside English = by first form's date (no column records it) / by the absence of an attested English form. **R** Owner's words decide most of it: "we're basically just counting the number of times it appears written in a given way. I would prefer to prioritize CSA/ISO for terminology"; "record it in whatever form and then have a preferred display term column maybe"; "likely have to do a convergence test … or I rule" (Owner statements 2026-11-18 and (second)). Resolved: (1) an appearance is one ATTESTED occurrence row (`v_attested_term_forms`): E4 (Owner statement 2026-11-06 (second), "never vocabulary") excludes `model_seed`, `unrecorded` and `owner_supplied` until a source attests them; an occurrence is a place (`ux_term_aliases_occurrence` keys on URL, clause, page, line), so "times it appears" is counted literally. "Written in a given way" groups by language and the form after the one quote normaliser (`retrieval_log.normalise_quote`), case-folded. (2) CSA/ISO **wins**: "prioritize" read in its ordinary sense; among several CSA/ISO forms the count decides. (3) No tolerance: a count needs none; an exact tie at the top shows the label and flags "judge owed", never `MIN(form_id)` (the ledger's ACTION (2) forbids it). (4) A named judge's pick (`term_label_picks`) overrides; that IS the owner's "preferred display term column", held once on the concept (a parameter reads its term), so no stored display cell is added (rule 8: the default is computed). (5) No attested form: the label `terms.canonical_en`, marked `label_ours`. (6) "First met outside English" dissolves into a derivable test, E1's own: a concept has no attested English instrument form of an in-scope jurisdiction; then the count runs over its attested forms in every language. No date of attestation is needed. **Datum that bounds it:** no attested form exists (`select count(*) from term_aliases where attestation in ('instrument','other_source')` prints 0), so the rule has no live subject; build it with T-107. **Identifying CSA/ISO** needs a typed issuing-body cell on the occurrence (a URL substring is not a warrant); ISO exists as a meta jurisdiction (`select * from base_jurisdictions where jurisdiction_code='ISO'`), CSA does not. **C** medium on (2) and the grouping; high on (1), (4), (6). **Res** no by §8's list; the owner keeps "or I rule" through the pick. **F** new tooling task, after T-107 attests forms: an issuing-body cell on `term_aliases` (a foreign key into a bodies vocabulary held as rows), and `v_term_names` rebuilt by a compensating migration to the rule above; T-028-design §8 amended.

### 12, 15 and 30 together: holding a source's words (the quote in the base, clause text in git, typed bibliographic values)
All three ask how much of a source's own text the project holds, where, and why.

**12. Q** Does an absorbed base grounding repeat the quoted words or only the locator? **O** (a) locator only: the base cannot check itself (retrieved files are not committed, Owner statement 2026-11-06 (fifth)), and the T-083 critic's case returns, corridor width made a colour temperature on `https://example.org` page `n/a` (S18 L87); (b) locator plus the words the base cell asserts were found, as short as the base's own refusal needs; (c) locator plus the whole passage: a second home of the evidence stage's text. **R** (b). The owner's words: the base cell carries "the source's URL and, if need be, page and line" (2026-11-06 (seventh)); OD-71: the justification is "absorbed by base and grounded as if it were always there to prevent loops/recursion/sequencing conflicts". A locator alone absorbs nothing: the content stays outside the base, in a file the repository does not keep. The words are the base's own fact (what was found), as a form's own text already is (`term_aliases.alias`); rule 5 is kept where it can be, because the evidence stage's quote verification, tier and standing stay there. Bound: the words that hold the cell's claim and that a base refusal reads (a value with a digit and unit for a kind, item 41; the words stating a direction, item 13; the words naming both terms for a relation, item 38). **C** medium-high. **Res** no (code architecture; holding is settled, item 15). **F** nothing to repair: T-083's repair `3caac402` kept `quantity_kind_quote`; `term_relations` (repaired `1c5e4ce9`) gains a quote under item 38.

**15. Q** May `clause_text` enter git history through `data_*.sql`? **O** (a) yes; (b) no: then OD-23's retained text cannot exist, since `data/guidebook.db` itself is a committed blob and any `source_clauses` row enters history with it; (c) hold the text outside git: a second store of a fact the database owns. **R** (a). The owner settled holding twice: "oh fuck off with the "no electronic copy". we are doing a not for profit volunteer advocacy project. this is fine" (2026-11-06 (fourth)) and "We do not need licenses as this is a not-for-profit advocacy project." (OD-15); and chose "Clause inventory backed by retained text; clause NOT shown" (OD-23, Owner answers 2026-11-12). Showing stays forbidden (`dbcore.NOT_SHOWN` holds it). The fifth statement's concern was size and tokens; a clause is held once per place per full reading, not the whole file. **C** medium (licensing is the owner's, though the owner's words are on point). **Res** yes (licensing). Default (a); safe meanwhile: no clause row exists (`select count(*) from source_clauses` prints 0), so nothing has entered history. **F** none; T-031's file records the ruling once ratified.

**30. Q** What warrants `edition` or `original_title` on a source with no DOI (`select sum(doi is null), count(*) from evidence_sources`)? **O** (a) any occurrence in a saved file: the reverted `c9c84466` wrote another standard's edition; (b) Crossref only: a DOI-less standard can never carry an edition or its own-language title; (c) a judged value tied to the source's OWN statement: the words stored in a typed warrant cell, the locator in the document's front matter or imprint, the retrieval-log sha256 of the file, the judge and reason; the typed value must be a whole-token run of the stored words, and a value that normalises to empty is refused. **R** (c). CLAUDE.md §5(c), "Never write a bibliographic field from memory when a payload is in hand"; rule 8: where judgment is required "the script asks for it … demanding the evidence for it, and recording the answer and its warrant in named columns". Whether the words are the source's own statement is a judgment no substring can make; the critic's counterexamples are what a machine-only rule produces. No length threshold is invented: the whole-token and non-empty tests do the work. **C** medium. **Res** no. **F** T-027 rewritten (tooling): warrant columns per field, a CHECK on `code_currency_status` folded into the same `evidence_sources` rebuild (item 76).

### 13. OD-71 and `direction_ref_id`
**Q** Does OD-71 supersede the basis of `base_parameters.direction_ref_id` and `set-parameter-direction`'s refusal that an admitted source hold an extraction for the parameter? **O** (a) keep: a base write waits on evidence admission and a judgment-stage row, the sequencing OD-71 forbids; (b) absorb: the direction's warrant (the words stating which way is better, URL, page or clause, line) in base cells, `direction_ref_id` provenance only with no foreign key. **R** (b), on contact. The refusal cites "ledger 2026-10-30, ACTION 6" (`grep -n "FROM AN ADMITTED SOURCE" scripts/db.py`), but "with its direction recorded from an admitted source and not hand-set" is the recorder's ACTION, not among that entry's quoted owner words (`sed -n 4814,4866p references/project-standards.md`). The owner's later words govern: "ref_id as provenance? sure. but it's ONLY for provenance". "Not hand-set" survives as the quote-and-locator refusal, so no refusal weakens in substance; it moves into the base. Datum: no row uses the column (`select count(*), sum(direction_ref_id is not null), sum(accessibility_direction is not null) from base_parameters`), so nothing migrates. **C** medium-high. **Res** no. **F** new tooling task "absorb the direction warrant": columns, writer refusal, the foreign key dropped by a schema migration (no data migration inserts it: checked).

### 14. `term_aliases.observation_id`; attested form or search aid (OI-55 (6))
**Q** When `add-term --from-observation` absorbs a phrase before its quote is checked in a saved file, is the form attested or a search aid? **O** (a) attested (`instrument` or `other_source`) when it carries a URL and a page or clause; `unrecorded` otherwise; (b) always `unrecorded` until quote-verified: re-imposes the saved-file wait the seventh statement removed, and no form could ever become vocabulary from the base route; (c) always attested: a form with no locator would count as vocabulary. **R** (a). E4: a form "becomes vocabulary only when an instrument in its language is read and the phrase is found there"; an observation is that reading, recorded verbatim with a locator; "none of the work in base needs to be verified and stored in evidence" (2026-11-06 (seventh)). The table's own CHECK already requires a URL and a page or clause for an attested row. The kind (`instrument` against `other_source`) is the operator's judgment, constrained by the CHECK. Then `observation_id` goes: no live row sets it (`select count(*) from term_aliases where observation_id is not null`) and no data migration inserts it. **C** high. **Res** no. **F** new tooling task with item 13 (one schema migration): drop the column and its CHECK branch, rebuild `ux_term_aliases_occurrence` without it, remove the `unrecorded` hold.

### 16. The clause inventory's matching rule
**Q** Is "a clause holds a form of the concept, word by word" the test that a clause is about a parameter? **O** (a) label plus attested forms (as built): with no attested form, matching runs on our English label alone, so non-English clauses are never flagged, a walk that fails across languages; (b) every recorded form, seeds included, as an owed flag: re-reads raised on a model's guess; (c) (a) for owed flags, and seeds and unrecorded forms listed separately as candidates. **R** (c). E4 calls seeds "flagged search aids": matching a clause is a search act, so seeds may PROPOSE; they never make a pair owed. OD-23: "we just want to minimize duplicate reads for efficiency"; only warranted forms raise the owed flag. **C** medium. **Res** no. **F** `scripts/audit/scan_debt.py` gains a candidates line; T-031 §4 records the rule. CJK whole-word matching stays item 85's limit.

### 17. The tier floor of the `context` lens
**Q** Is "tier 4 and above" the right floor for a code value? **O** (a) keep: T5 national frameworks are included; (b) T6 only: T4 and T5 regulatory values get no lens; (c) all tiers: the owner's "code values" widened without warrant. **R** (a): the floor is the regulatory stratum as ratified ("T4–T6 the regulatory stratum", CLAUDE.md §6; `governance/tier-system.md` rows T4 to T6), which is what "code values" (fifteenth set) means in the project's terms; the engine reads the same stratum (`b["t45"] + b["t6"]`, `grep -n 'regulatory = b\["t45"\]' scripts/assess/assess_cell.py`). Not a threshold invented here. **C** high. **Res** no: it applies a tier definition, it does not set one. **F** one home for "regulatory stratum" (`grep -n ">= 4" scripts/db.py` finds several), a small tooling repair.

### 18. The strength of the `context` warrant
**Q** Should the writer refuse weak reasons (`x`, `idk`)? **O** (a) a mechanical rule: a judgment cannot be graded by code, and any rule is a curated list; (b) as built (non-blank, a letter), with the audit's queue and the adversarial pass reading the reasons. **R** (b). "use contextual judgment" (fifteenth set) entrusts judgment; rule 8's remedy is to record "the answer and its warrant in named columns", which `basis_reason` and the session stamp do. **C** high. **Res** no. **F** none; same answer for item 78.

### 19. A `context` link where the clause names the group
**Q** May a session record `context` when the clause itself names the group? **O** (a) allow: a checkable warrant is recorded as an uncheckable one; (b) refuse when the same code would pass the `named_in_text` test, naming `--basis named_in_text` as the next action. **R** (b): provenance demands the strongest warrant the words support. A superseded source's figure is a recording question, not a lens one: the lens follows the figure. **C** high. **Res** no. **F** small tooling repair in `db.py`'s lens writer.

### 20. `ALL` under `named_in_text` and `heading` (T-056, OD-31)
**Q** Should those bases refuse `ALL` now? **O** (a) wait for T-056 whole: new `ALL` links keep arriving while OD-48 is open; (b) split T-056: the writer refusal now, the engine part after OD-48. **R** (b). The owner selected "Heading's group; ALL leaves the identity lens" (OD-31). A refusal on new writes changes no live row (`select basis, count(*) from extraction_lens_links where identity_code='ALL' group by 1`); the stored links are T-115's. **C** high. **Res** no. **F** T-056 split; part 1 tooling now.

### 21. OI-55 (7): lens changes under a live determination
**Q** Do `add-lens-link` and `retire-lens-link` refuse while a live determination uses the figure? **O** (a) refuse, naming the determination and the next act (retire it, change the link, re-determine); (b) allow and let the recompute flag staleness, which binds only once T-132 lands. **R** (a). The project's pattern is "writers that refuse until dependents are handled" (`PROPAGATION-AND-CONSOLIDATION-ADJUDICATION.md` §4), as `retire-extraction` already refuses a figure a live determination names (T-078). The backward walk stays open (retire, change, recompute). **C** high. **Res** no. **F** tooling; no live determination exists (`select count(*), sum(retired_at is null) from specifications`), so it is cheap now.

### 22. A pair whose only figure is withdrawn
**Q** Should such a pair read READ-NOTHING-FOUND and owe nothing? **O** (a) as built: a misread is recorded as "the source says nothing", a false fact, and nothing re-reads it; (b) owed when the pair has no live figure, at least one retired figure, and no reading recorded after the retirement. **R** (b), derived from timestamps, never from parsing `retirement_reason`. OD-23: "We can flag a source to be read again". **C** high. **Res** no. **F** tooling: `v_scan_ledger` (compensating migration) and `scan_debt.py`; T-078 file amended.

### 23. An open gate refuses a kind
**Q** Should `set-parameter-kind` refuse while an open gate stands (parameter 3, gate 1, `UNLINKED`: `select gate_id, parameter_id, verdict from determination_gates where resolved_at is null`)? **O** (a) refuse: a later stage's open question blocks a base fact, a walk ordered backwards; (b) allow; keep refusing a live determination. **R** (b). `_refuse_live_work` blocks merge and retire because they change "what the parameter IS" and the question could not be answered; declaring a NULL kind once names the quantity the parameter already measures and leaves the gate's question (read the full text) intact. OD-71's sequencing ("the base is never ordered after evidence") applies all the more to specification. **C** medium-high. **Res** no. **F** tooling: `set-parameter-kind` passes a gate flag to `_refuse_live_work`; T-083 §4 and T-109 amended.

### 24. `merge-parameter` and the kind (with OI-78)
**Q** May a merge leave figures under a survivor of another kind, or none? **O** (a) allow: figures stated in one quantity sit under another; (b) refuse unless both kinds are equal, naming `set-parameter-kind` on the survivor first. **R** (b). OD-24 (delegated): two cases are two parameters when "they cannot be placed on one scale". **C** high. **Res** no. **F** tooling, with OI-78's reshaping of the merge to T-129's form (a row and a derived survivor); none has been run (`select count(*) from base_parameters where status='merged'`).

### 25, 26 and 27: T-119
**25. Q** Keep the three pairs for `DR-2026-07-20-weighted-strength-anchor-model.md`? **O** (a) keep; (b) remove: an OPERATIVE record a live reader reaches keeps its old band table unmarked, a walk through a superseded step. **R** (a). CLAUDE.md rule 0: "Record the supersession"; the bands are the owner's own later words ("empty for 5/6", "T4 only half circle", U7). Recording is not deciding. **C** high. **Res** no.
**26. Q** Pair the gloss "(weak-band convergence floor)" in DR-2026-07-21 tier-doctrine (`grep -n -F "weak-band convergence floor" decisions/DR-2026-07-21-tier-doctrine-source-class-consistency.md`)? **O** (a) leave: one record glosses code agreement as a floor while the anchor model's equal gloss is marked; (b) an AMENDED pair as to the gloss only (the tier ruling stands). **R** (b), one treatment for one gloss: "convergence just means values coming together" (U2) and "minimum is code stratum unless there is no code data" (U3). **C** medium. **Res** no.
**27. Q** An attestation names a session record not yet written. **O** (a) leave it to the close: a pointer to nothing on a merged tree if the close slips; (b) the coordinator writes the session record before #240 merges. **R** (b). Provenance: a pointer resolves or is not written. **C** high. **Res** no. **F** for 25 to 27: a ledger line and one marker (26); a process step for 27; no tooling.

### 28 and 29 together: T-134's quote binding
**Q** A ledger quote found once today fails when a later entry re-quotes it; a deleted passage re-embedded elsewhere passes as MOVED with exit 0. **O** (a) as built: red by construction in an append-only file (rule 6's argument) and a location lost; (b) a distance limit: a typed number; (c) bind an atom to its enclosing heading (an entry or a section key) and its quote: found once inside that section passes, moved within it reports MOVED, found only outside it FAILS. **R** (c). Headings of an append-only ledger do not move; uniqueness within a section also gives a quote floor with no typed length (item 87's `''`, `a`, `the` stop being unique). **C** medium-high. **Res** no. **F** tooling (T-134 follow-on): `build_graph.py`, the atom files, `verify_atoms.py` on the same rule.

### 31 to 36: T-030
**31. Q** How is a unit added? **O** (a) hand-written migration only: "hard coded behaviours" in another form; (b) `add-unit` by data with a warrant: the factor as the exact fraction its defining standard states, that standard's locator and words in the row (OD-71's shape), `base_units` in the capture set. **R** (b). "pipeline must not have hard coded behaviours" (2026-11-12 (seventh)); OD-24 (delegated): kinds are "extended by data with a warrant", and a unit is the same shape. **C** high. **Res** no. **F** tooling; T-047 is its add-by-data test.
**32. Q** `degrees` on the gradient kind? **O** (a) stand alone (today): degree and percent figures of one cell cannot be compared; (b) a non-linear rule as data: percent = 100·tan(θ), monotonic, so accommodation order is exact; display rounds on the safe side (OD-22) and is marked converted. **R** (b) adopted as the rule, DEFERRED in build to T-059's comparison step. Live subject: `select extraction_id, parameter_id from source_value_extractions where claimed_unit='degrees' and retired_at is null`. Today's refusal composes nothing wrongly, so the interim is safe. **C** medium. **Res** no. **F** a cell on `base_units` naming the conversion, inside the T-059 prerequisites.
**33. Q** A determination written under an older `RULE_VERSION` is invisible to `stale_determinations`. **O** (a) as built: a superseded computation reads current; (b) a different rule version is stale by definition. **R** (b). "you have to compute it" (2026-09-09, evening): a cache of a rule no longer in force is not the computation. **C** high. **Res** no. **F** T-132's scope.
**34. Q** Value rows whose unit has no `base_units` row (T-030's definition; a broader count: `select count(*), count(distinct claimed_unit) from source_value_extractions x where retired_at is null and claimed_value is not null and not exists(select 1 from base_units u where u.unit=x.claimed_unit)`). **R** DEFER: each unit is placed by `add-unit` (item 31) or left standing alone, by judgment per unit, in a research batch. Datum: the exact predicate is `load_units`'s. **C** high. **F** research, after item 31.
**35. Q** Bounds stored as REAL. **O** (a) keep: a stored figure differs from the source's; (b) exact text with its unit. **R** (b), before the first live determination (T-110), while no determination is live. **C** high. **Res** no. **F** tooling migration.
**36. Q** Where the increment would cross both bounds, show each exact conversion marked "unrounded"? **R** yes: it satisfies both halves of OD-22 (never below a source's minimum, never above its maximum) and states no figure the source did not. **C** high. **Res** no. **F** none.

### 37, 38 and 39: T-029
**37. Q** The table accepts `element has parameter` beside `element has provision` for one pair, `broader` beside `part of`, and a three-cycle of `broader`. **O** (a) accept all; (b) refuse a cycle of any length in `broader` and `part of` (a hierarchy that loops is not one), and refuse `has parameter` with `has provision` for one pair (OD-56: "a provision is not a parameter"); allow `broader` with `part of` (a term can be both a kind of and a part of another, as sources conflate). **R** (b). Owner: "b" (OD-56); 2026-11-06 (sixth): "Conflation is recorded, not resolved". **C** medium-high. **Res** no. **F** tooling.
**38. Q** Must a warrant concern its terms? **O** (a) no: one observation warranted sixteen unrelated relations; (b) the warrant's quote (item 12) must hold a recorded form of each term (label or any recorded form, seeds included, since this is a check and not vocabulary); a form the source uses but the base lacks is recorded first, with its locator. **R** (b). **C** medium. **Res** no. **F** tooling, with item 12's quote cell on `term_relations` (0 rows today: `select count(*) from term_relations`).
**39. Q** The `reason` cell; relations of a merged term. **R** keep `reason` as the base's own cell: OD-71 forbids a base row pointing into an adjudication, so a `distinct` row absorbs its reason ("absorbed by base and grounded as if it were always there"); T-129-design A6 amended accordingly. Relations are read through `v_term_survivor`; the raw-id unique index stays as the record written. **C** high. **F** plan edits to T-029 §4 and T-129-design A6.

### 40. T-028: the judge is any non-blank string
**R** Keep non-blank (a CHECK at the next rebuild of `term_label_picks`); build no judge vocabulary, which would be a curated list of people and models the database cannot verify. The session stamp is the verifiable part. **C** medium. **Res** no.

### 41 and 42: T-020
**41. Q** The digit test admits "Class 1" or a year. **O** (a) as built; (b) the quote must hold a number followed by a unit of the declared kind, read from `base_units`. **R** (b): derived from data, no list. **C** high. **F** tooling after item 31; applies to `quantity_kind_quote`.
**42. R** Refuse a blank session in `insert_parameter`, as `insert_quantity_kind` does. **C** high. **F** tooling.

### 43 and 44: T-022
**43. R** A real CHECK on `gaps.status` at its next rebuild (rule 8: `dbcore.check_values` reads a vocabulary from a CHECK). **C** high. **F** tooling.
**44. R** Keep: B13's carrier is the URL, as the owner said page and line are "if need be" (2026-11-06 (fifth)); B11 and the skim edges stay two edges because two stages re-enter; add no column until a reader needs one (§8). **C** high.

### 45 to 48: T-049
**45. R** Refuse a review in the translator's session. OD-30 (delegated) requires review before a reader sees a translation; a self-review in one session is no review. **C** medium-high. **F** tooling.
**46. R** Refuse a translation identical to its original, naming the act: no translation is needed. **C** medium.
**47. R** Compare the sequence of comparator, number and unit after normalising digit grouping, in T-008's reader, so "1 200 mm" to "1,200 mm" passes and a reorder, unit or comparator change fails. **C** medium-high. **F** tooling (T-049 item 5 and T-008).
**48. R** A `withdraw-translation` that retires a `requested` row in place ("retire in place then"). **C** high.

### 49 and 50: T-050
**49. R** Close the empty-string holes by a compensating migration at the next rebuild. **C** high.
**50. R** Both readers are right for their purpose; the cross-reference validator resolves a retired id AND flags it as citing a withdrawn claim; the graph of live state drops it. **C** medium. **F** small tooling.

### 51 to 53: T-089
**51. R** Key a refusal's signature on its template (an id the `Refusal` carries at raise time), not on its operands. **C** medium. **F** tooling.
**52. R** A disposition that parks a refusal on a gap reads that gap's state: a closed gap reads disposed. One home (the gap). **C** high.
**53. R** Cue a cross-stage verb once, under `cross-stage`; derive `ENGINE_VERB`'s tables from the engine's emitted SQL; narrow each cue to checks whose subject tables the verb writes (from the registry), so suites run rarely (§1). **C** medium.

### 54 and 55: T-093 (55 with OI-78)
**54. R** Accept: once notation families are data (T-030), a new member is a warranted data act, so the widening is warranted, not silent. **C** medium-high.
**55. Q** The old unit survives only as a dated line in `notes`. **O** (a) as built: the shape the 2026-11-06 statement forbids, "data stored in the wrong cell"; (b) one typed amendment record for every `amend-*` verb (row, column, old value, new value, judge, reason, time); the merge's `MERGED` note (OI-78) moves to T-129's merge-row shape. **R** (b). "we do NOT want to have data joined in cells … or have data stored in the wrong cell"; "more columns = more specificity" (2026-11-06). **C** high. **Res** no. **F** tooling.

### 56 to 61: the first stack, part one
**56. R** One stdlib-only helper for `_tables`, when either file is next touched; the differing helpers are left unless a later task names one home. **C** medium.
**57. R** `insert_evidence_source` refuses a non-member by name through `dbcore.check_values`. **C** high. **F** tooling.
**58. R** Decline both in writing: a word-segmentation dictionary and a number-word list are curated lists (rule 8); cross-script near names reach a judge through T-130's proposals (the previous adjudication, G4); OD-68 confines screens to one language. **C** high.
**59. Q** May bodies of law (TERM-067, TERM-075) and cost terms (TERM-066) be declined as parameters? **R** Yes, each with its reason, kept as terms: the same shape the owner applied in E12 for functional-axis and method terms, and `dbcore.NON_QUANTITY_DOMAINS` already refuses `legal` and `economics`. A declination is reversible. **C** high. **Res** no (OD-53, delegated, covers who declines). **F** research.
**60.** Closed by item 10.
**61. Q** The engine links "the newest retired row", including one retired for error. **R** Follow only an explicit successor pointer; a row retired with no successor contributes nothing; never parse `retirement_reason`. **C** medium (the engine path was not re-read here). **F** tooling, T-011 follow-on.

### 62 and 63: T-015
**62. Q** A source written in a language `lang_jur_map` does not hold cannot state it; NULL is read as English. **O** (a) add the pair to the map: scope (OD-04) widened to describe a held source; (b) a flagged "other": a joined meaning; (c) a language vocabulary held as rows, independent of the scope map; NULL read as unknown, never English. **R** (c). Reading NULL as English fabricates a fact and is the bias the owner named: English labels allowed, "the aim is to avoid English bias" (2026-11-06 (eighth) heading). Scope says what research is owed, not what a source may be. **C** medium-high. **Res** no: no scope changes. **F** tooling (a `base_languages` table; `lang_jur_map` points into it).
**63. R** Writers fold to upper case (they already do); one compensating data migration folds existing rows, in its own pull request (rule 10); readers then drop their folds. **C** medium.

### 64 and 65: T-001
**64. Q** A batch captured from an older base emits an UPDATE that reverts a correction `main` made. **R** Refuse a capture whose scratch copy's base sha256 is not the current canonical database's; serial landing is the owner's answer ("Serial is fine", OD-27). Silent reversion erases history. **C** high. **F** tooling in `emit_batch_sql.py` (no such guard: `grep -n -i "base hash\|stale base" scripts/research/emit_batch_sql.py` prints nothing).
**65. R** One fact, one home: derive `ratified` from `status`, or refuse disagreement in the model. **C** medium.

### 66. T-052: out-of-scope instruments
**R** (b): stage them through the existing `add-code-lead` (a validated jurisdiction), naming it in the two mining skills; no new flag. OD-05 (delegated): "stage as a lead"; OD-34 (owner): the bucket order covers instruments only. Reuse before adding (§8). **C** high. **F** T-052 rewritten as a skill-and-file edit.

### 67. OR-5b: close or split
**R** Split: the answered part keeps "ANSWERED BY THE OWNER, PARTLY", and each of its three edges is registered as its own open item, so an answer is never read as wider than it was (`grep -n -F "OR-5b STATUS" references/project-standards.md`). The edges' content (soundness of lived-experience work) stays the owner's. **C** high on the bookkeeping. **Res** the edges yes (tier definitions).

### 68 and 69: T-002/T-042
**68. Q** The judgment stage's `anchor:` names "the 4-state determination machine + convergence + directness"; `pipeline-operations.md` has synthesis producing `specifications`; the specification entry's order differs from the engine. **R** The owner's spine decides: "you research slugs, evidence research, judge evidence, synthesize judgments, specify syntheses, and render specifications" (2026-08-27). Directness belongs to judgment, convergence to synthesis, the determination machine to specification; OD-07 (delegated) keeps convergence computed inside the engine, so the specification entry says the engine writes its synthesis output in the same run. **C** high. **Res** no (the owner ruled the spine). **F** a governance text edit (tooling kind), then OD-17.
**69. Q** Does the existence gate cover "a BPC synthesis claim" or "any source the work rests on"? **R** Any source a figure or a determination rests on: the BPC is frozen and quarantined (OD-61), and §5(c)'s failure was a fabricated citation that passed because gates asked the wrong question. PI versions lag doctrine by design (CLAUDE.md §7). **C** medium. **Res** no.

### 70. OD-11's unmet sentence
**Q** The delegated OD-11 resolution says the instrument "must count it as a member of each stage it carries"; T-051 reverted that and the previous adjudication declined it (G11). **R** Record a correction to the delegated OD-11 resolution: a `cross-stage` table is walkable as an intermediate and counted in no stage; its ACTION (3), "lose no path", is met. The sentence otherwise stands unmet forever. **C** high. **F** a ledger correction line in section 4's entry.

### 71. T-021 leftovers
**R** (b) owner-page options worded by verdict (a QUESTION is not a wrong-evidence prompt); (c) writers stamp through `dbcore.stamp_for` in the column's existing format; (d) one home for the delegated-prefix refusal (`_owner_approval`). Item (a), a QUESTION blocking merge and retire, stands: it is the refusal item 23 relies on. **C** medium-high. **F** small tooling.

### 72. OR-1c / OI-55 (10): link table and determinations
**R** The link table covers figures only; a determination keeps its lens columns. The owner's 2026-08-28 ruling set "three lens columns, one CHECK, real FKs" on a table attaching a determination (CLAUDE.md §6), and OD-39 superseded only the "Never a `population_*` link table" clause for a figure's lens codes. **C** high. **F** OR-1c's mark stands; OI-55 (10) closed by this line.

### 73. T-054/T-048: roots and holes of migration 135
**R** One home for a root's type: the figure reads it through the registry, and a CHECK refuses `root_ref_id` and `root_id` both set; the 135 holes (NULL status, self-successor, `''` dates) close by a compensating migration at the next rebuild; a crossing retired by mistake is corrected by a new row, not an un-retire (retire in place). **C** medium-high. **F** tooling.

### 74. T-055: a parent cell's function path
**Q** The parent gathers its descendants' figures but reads only its own `identity_icf_map` rows. **R** Read the descendants' map rows too: one rule for what a parent cell is, symmetric with its figures. **C** medium. **Res** yes (population taxonomy, and it adjoins OI-55 (2)). Default as stated; safe meanwhile: no determination is live. **F** tooling after ratification.

### 75. The approval stored nowhere
**R** Store the approving ledger heading in a typed column on each row written by `add-lang-jur-pair`, `set-pair-scope` and `add-identity`: rule 8's "recording the answer and its warrant in named columns". **C** high. **F** tooling.

### 76 and 77: T-027
**76. R** A CHECK on `code_currency_status` in item 30's `evidence_sources` rebuild; `dbcore.code_currency_vocabulary` then reads the CHECK, not a governance sentence. **C** high.
**77. R** No "initials convention" flag: show the given name as stored, which `--verify-authors` holds to the logged payload; the flag would be a judgment no source states. **C** medium-low (the original requirement's intent was not traced). **F** a view edit only.

### 78. Free-text reasons
**R** As item 18: a reason is a recorded judgment that the audit and the adversarial pass read; no mechanical grading. **C** high.

### 79 to 91: limits
Each is a datum, a process note or a limit, carried by the task or batch named in its row: re-run the joined-cells census after the first row of a new table; probe under `session_task-probe` and never delete `refusals.jsonl`; critics keep scratch files in their own folders; `migration_reproducibility --deep` once on the final tree; T-120 carries the prose callers and PIP-01; `repoint-extraction-relation` gains the retired-figure refusal (a defect, not a decision, repaired with item 21's tooling); M04 gains its retire transition with T-134's follow-on; `OPEN-QUESTIONS.tsv` and `AMBIGUITIES.tsv` publish the line found, with items 28 and 29. CLOSED by later commits: S15's zero-selection PASS (T-075), the owner page's delegated group and OR-17b (S15 L53), `original_title` (S15 L66), `retirement_reason` readers (owned by T-050's amendment in the previous adjudication, G13).

## 4. What to do next

**Dependency order. Rule 10: every task below is tooling unless marked RESEARCH, and no tooling task ships with research rows.**

1. Coordinator, before #240 merges (process, no task): write the T-119 session record (item 27); put OD-17 to the owner with the contract diff (item 1); put the reserved defaults (items 2, 3, 4, 5, 6, 9, 15, 67, 74) to the owner in plain form.
2. TOOLING "base grounding absorbed" (items 13, 14, 12, 38, 37, 39): one schema migration drops `term_aliases.observation_id` and `base_parameters.direction_ref_id`'s foreign key, adds the direction warrant cells and a relation quote; writers refuse a warrant without words and locator, a relation quote lacking a form of either term, and relation cycles. Amend T-129-design A6.
3. TOOLING "units and kinds as data" (items 31, 41, 35, 33): `add-unit` with a warrant; the kind quote's number-and-unit test; exact bounds on `specifications`; a rule-version change reads stale (into T-132).
4. TOOLING "lens and figure refusals" (items 19, 20, 21, 22, 23, 24, 17): T-056 part 1; refusal of `context` where `named_in_text` holds; lens changes refused under a live determination; withdrawn-figure pairs owed; gate no longer blocks a kind; merge refuses differing kinds; one home for the regulatory stratum.
5. TOOLING T-135 rewritten (item 10): `term_domains` extended by data.
6. TOOLING "amendment record" (item 55, OI-78), before T-059 rewrites the gather.
7. TOOLING T-027 rewritten (items 30, 76).
8. TOOLING "state-graph binding" (items 28, 29, 87).
9. TOOLING small repairs, any order: 16, 40, 42, 43, 45 to 53, 57, 61, 62 to 65, 71, 73, 75, 77.
10. TOOLING after T-107: displayed-name rule and issuing-body cell (item 11).
11. TOOLING with T-059: the degrees rule (item 32).
12. RESEARCH, each in its own pull request after its tooling: T-084 (item 2, on ratification), T-087's parked figures (items 3, 6), declinations (item 59), units placed (item 34), the language fold (item 63).
13. Plan edits (no task): T-031 §4 (items 15, 16), T-078 (22), T-083 and T-109 (23, 24), T-052 (66), T-029 §4 (38, 39), T-028-design §8 (11), `governance/pipeline-contract.yaml` and `pipeline-operations.md` (68).

**Nothing already merged on the branch must be reverted.** Items 13, 14 and 38 extend `29c8b236`, `1c5e4ce9` and `3caac402`; item 20 extends `336685a2`; item 22 extends `cd778176`; item 28 extends `ee64bf80`. Each is additive.

**DRAFT for the coordinator, NOT appended.**

```
## Delegated resolutions 2026-11-19 — the open decisions after the third tooling stack (OD-17, OD-46 to OD-54, OD-62, OD-67, OD-69, OD-71's residue, OD-72, and the stack's design questions)

Given in the session `session_2026-11-18-remediation-batch-1-tooling-stack-2`; the owner's instruction was typed to the coordinator and relayed; derive its time from the preserved transcript (`git grep -n -F "have Opus adjudicate all open decisions" -- transcripts`).

**Owner's words, quoted (typed):**

> "have Opus adjudicate all open decisions based upon long-term integrity re provenance and walkability as well as context from my prior rulings"

**Readings.**

- [ASSUMPTION: "all open decisions" covers every register entry not answered or resolved with its check satisfied, every item the three sweep lists left open, and the eleven questions of pull request #240 — basis: the words; the list is `workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md` section 2].
- [ASSUMPTION: the instruction supersedes, for those items, on contact (CLAUDE.md rule 0), the sentences that said they were not to be resolved under delegation: ACTION (3) of "Owner statements 2026-11-18 — OD-71 …", ACTION (3) of "Owner statement 2026-11-18 (third) — OD-69", ACTION (4) of "Owner answers 2026-11-17 — OD-68 …", ACTION (4) of "Correction and registration 2026-11-15", and the "Registration 2026-11-14" sentence on OD-62 — basis: a live owner instruction naming "all open decisions"].
- [ASSUMPTION: it does not move CLAUDE.md §8: an item of content or doctrine is resolved as a recommended default the owner ratifies, and stays REFERRED BACK — basis: §8; the instruction names criteria, not ratification].
- [ASSUMPTION: "provenance" and "walkability" are read as defined in the adjudication's section 0 — basis: the owner's rulings it quotes].

OD-17: not adjudicable; the owner's act; its condition (T-022 merged) is met; asked again with the contract diff
OD-17 STATUS: DEFERRED BY THE OWNER

OD-46: recommended default, admit as declared, scoped-out codes
OD-46 STATUS: REFERRED BACK TO THE OWNER

OD-47: recommended default, the document's stated audience judged per item by context, the audience words quoted
OD-47 STATUS: REFERRED BACK TO THE OWNER

OD-48: recommended default, whom it is for
OD-48 STATUS: REFERRED BACK TO THE OWNER

OD-51: recommended default, yes, on retrieved proof of authorship
OD-51 STATUS: REFERRED BACK TO THE OWNER

OD-52: recommended default, names the term; the contrast provision is separate
OD-52 STATUS: REFERRED BACK TO THE OWNER

OD-54: into the register, replayed through the writer
OD-54 STATUS: RESOLVED UNDER DELEGATION
OD-54 CHECK: pending

OD-62: no rename (the registered default)
OD-62 STATUS: RESOLVED UNDER DELEGATION
OD-62 CHECK: pending

OD-67: recommended default, yes, one answer on the full list, VES withheld
OD-67 STATUS: REFERRED BACK TO THE OWNER

OD-69: (a) a concept's topic area; not fixed; held as rows extended by data with a warrant
OD-69 STATUS: RESOLVED UNDER DELEGATION
OD-69 CHECK: pending

OD-71: the absorbed grounding holds the locator and the words the base cell asserts were found, as far as a base refusal reads them; direction_ref_id and term_aliases.observation_id become provenance only or are dropped; an absorbed phrase with a URL and a page or clause is attested
OD-71 STATUS: ANSWERED BY THE OWNER

OD-72: an appearance is one attested occurrence; CSA or ISO wins, then the count; an exact tie shows the label and a judge is owed; a named judge's pick overrides; no form shows the label; a concept with no attested English instrument form of an in-scope jurisdiction is counted across its attested forms in every language
OD-72 STATUS: RESOLVED UNDER DELEGATION
OD-72 CHECK: pending

Correction to the delegated resolution of OD-11: a cross-stage table is walkable as an intermediate and counted in no stage; "count it as a member of each stage it carries" is withdrawn; ACTION (3), "lose no path", is met.

SUPERSEDES: decisions/DR-2026-07-21-tier-doctrine-source-class-consistency.md :: "weak-band convergence floor"
  BY: references/project-standards.md :: "best, most common and minimum are read as the owner defined them on 2026-11-14"
[the passage's marker reads AMENDED, as to the gloss only; the coordinator verifies the pair passes supersession_backpointer_audit before appending it]

CONDITION: any session executing a task the adjudication names, writing a base warrant, a lens link, a unit, a direction, a domain or a displayed name, or meeting an item of its section 2.
ACTION: (1) Treat each RESOLVED UNDER DELEGATION line as opening a task's gate only once its CHECK reads confirmed (or not required, if the coordinator so records). (2) Treat each REFERRED BACK line's recommended default as unratified; do what the adjudication names as safe meanwhile. (3) Author the tooling tasks of the adjudication's section 4 in its order; ship research separately (rule 10). (4) Treat every [ASSUMPTION] above as unratified.
DATE: 2026-11-19 — delegated resolutions under the owner's instruction (typed words, quoted above); not the owner's own answers.
```

(The OD-71 status line restates that the owner's answer stands; the coordinator may omit it, since the latest line already reads ANSWERED BY THE OWNER and this entry decides only its residue. The design questions numbered 12 to 78 that carry no OD number are recorded by the entry's reference to this file and are not given status lines.)
