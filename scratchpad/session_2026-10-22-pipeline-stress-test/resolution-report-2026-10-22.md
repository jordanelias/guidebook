# Resolution report: the 2026-10-22 stress-test questions (Q0 to Q14, E0 to E13), with exact instructions

Written 2026-10-22 for the owner of `/home/user/guidebook`, from the question register (`question-register-2026-10-22.md`) and the reasoning pass (`fable-resolution-reasoning-2026-10-22.md`), both in the scratchpad. Every claim the plan rests on was re-checked against the code or the database before it became an instruction. Where the reasoning pass was wrong, the instruction follows the evidence, and Appendix A records the difference.

**State this report was written against.** Repository HEAD `f80bb3e4`, which is PR #201's head. GitHub reports PR #201 merged at 03:10 UTC on 2026-10-22. The local `origin/main` ref still names `bb43e5b0` until it is fetched. `data/guidebook.db` is at `PRAGMA user_version` 116 with sha256 `4b3cfb03d41d8a98…`; the same sha was measured before and after every experiment (C01). Nothing in the repository was edited, committed or migrated. Every experiment ran on copies under `/tmp/claude-0/-home-user-guidebook/f366a537-569c-50d0-a2d1-f74dc994928a/scratchpad/report-probes/`.

---

## 1. Reading guide and verdict

**How to read this.**
- Section 2 holds the owner decisions. Read it first, because the work plan branches on the answers.
- Section 3 is the ordered list of pull requests: the common protocol first, then each tooling PR in full.
- Section 4 gives the research-data procedures.
- Sections 5 and 6 are cross-references: one short entry per question, then a matrix showing how to prove each question resolved.
- Appendix C holds every command, with ids `C01`…; the text cites those ids.

**Marks used.**
- `[EXECUTED]` means I ran it and give the observed result. `[NOT EXECUTED]` means I did not.
- "measured 2026-10-22; re-run Cnn" marks a figure that will drift (CLAUDE.md rule 7a).
- `OR-n` is an owner decision (section 2), `T-n` a tooling PR, `D-n` or `S-n` a data PR, and `RC-A` to `RC-H` the shared root causes (Appendix B).
- "the engine" is `scripts/assess/assess_cell.py`; "the writer" is `scripts/db.py`.

### Verdict

**What is wrong, ranked by what would reach a disabled reader if it were rendered today.**

1. **Every population is given the wheelchair answer.** On a scratch copy, parameter 3 (ramp gradient) was determined under AUT, BLIND, ADHD, ICF d450 and need A-EFFORT. Each came out `provisional ○ max 5 %` from the same 26 governing sources as MOB. The cells (MOB) and (MOB, d450) share one `derivation_sha` `[EXECUTED, C30]`.
   - The cause is RC-C. The engine gathers by `parameter_id` alone, and `sha()` hashes the first non-null lens only.
   - The reasoning pass proposed routing rows one hop through the crossing maps. The project has already rejected that traversal twice: D-0184 measured that it "manufactures inference", and RULINGS R33 says the crossing is written on the row at judgment. The fix here is a lens predicate on the row's own columns (T-3).

2. **Stepped code rules print as one number, and the reader accepts nonsense silently.**
   - 24 of parameter 3's 34 governing claims contribute nothing to its value, because their notation or their conditions sit in free text. 45 of the 68 numerical or range rows cannot be read at all (measured 2026-10-22; re-run C21).
   - The reader takes `1/12` as 0.083 %, which would win a lower-is-better selection, and `12:1` as 1200 %. The writer accepts both, along with `8.33%`, `1 in 12` and `viisi prosenttia` `[EXECUTED, C24]`.
   - Conditional relaxations, such as 1:8 for short rises or 12 % in alterations, are never shown beside the value (RC-A, RC-B; T-1, T-2, D-1).

3. **Disagreement is hidden or misexplained.**
   - A T1 figure of 900 mm below three code floors of 1200 mm prints `stated ● ≥900`. The floors are labelled "disqualified on tier, verification or supersession", which is false: they were outranked.
   - Two anchoring claims that cannot both hold (≥1200 against ≤1000) print `stated ●` with no value, and a note that blames a missing comparator.
   - A Co-1 dimensional figure out-votes T1 and T2 (G4). The project's methodology document says it should not, and claims a mechanism that does not exist `[EXECUTED, C25]` (RC-D; T-4, OR-5, OR-6).

4. **Every pending cell claims a "function_only" derivation.** Its rationale says "the determination rests on the functional mapping alone", but a pending cell rests on nothing. This defect is new: neither the register nor the pass found it `[EXECUTED, C31]` (T-3, step 9).

5. **The writer accepts a derived figure that contradicts its own inputs.** `add-extraction --figure-role derived` stored 99 against base plus delta of 14.51. The blocking `extraction_relations_integrity` check catches it afterwards, in CI `[EXECUTED, C26]` (T-1, step 7).

**What is only undecided, and what is already fine.**

The owner decisions in section 2 are open. Six of them gate building:
- OR-1, the lens rule, which confirms D-0184 for the engine;
- OR-2, whether conditional branches sit beside a headline value;
- OR-3, whether a value's representation may be corrected in place (it touches D-0168);
- OR-5, Co-1 and dimensional values;
- OR-6, how divergence is recorded (it touches evidence-methodology §3.3);
- OR-8, the coverage unit.

Several things the questions probed are already sound:
- The write path replays and rebuilds exactly. Engine output was captured, emitted, migrated and rebuilt in a scratch clone with every table count equal `[EXECUTED, C34]`.
- Two engine runs on fresh copies emit byte-identical SQL `[EXECUTED, C35]`.
- Non-English bytes are kept verbatim, and the verbatim and CJK-numeral gates hold.
- Citation-mining completeness is already scoped to T1 and T2, and reports CLEAN over 13 sources `[EXECUTED, C27]`. The reasoning pass's proposed change there is unnecessary.
- The rule that both notations are presented is correct within the gradient family.
- Internal staleness detection works, and the refusal to supersede a source a live determination rests on works.
- There is no render surface. That is the planned step 3.R, unbuilt. While it is unbuilt nothing reaches the book, so nothing misleads yet. The danger is in building it before T-2 to T-4, which is why render comes after them.

---

## 2. Owner decision sheet (answer before the plan)

Ids are this report's own (`OR-n`), so they cannot collide with `RULINGS.md` R1 to R49. The "pass" column gives the reasoning pass's number. Each question can be answered in one word. "Default" is the recommendation, and the work plan follows the default unless the owner answers otherwise. **Every answer is recorded in the ledger** (`references/project-standards.md`, an appended `## Owner ruling YYYY-MM-DD — …` entry) **before any branch that depends on it opens** (CLAUDE.md rule 0).

| id | pass | question (one word) | default | if the default / if not | blocks until answered |
|---|---|---|---|---|---|
| OR-1 | R3 (corrected) | Confirm D-0184 for the engine: does a row reach a cell **only** through the cell's own lens codes written on the row, never through a crossing map? (D-0184 is "ADOPTED, REVIEW PENDING"; R33 says the crossing is judgment's output.) | **yes** | yes: T-3 as written; AUT, BLIND, ADHD, d450 and A-EFFORT cells for parameter 3 become `pending` with a gap naming the lens. no: the owner must state the traversal rule, D-0184 is recorded as superseded, and T-3 builds the gather over `identity_icf_map`, `access_need_icf` and the medical maps (the pass's design) | T-3, D-2 |
| OR-1b | new | Does a row tagged identity `ALL` (the "scope marker") reach every identity cell? | **no** | no: `ALL` rows reach only an `ALL` cell. yes: T-3's predicate adds `OR x.identity_code = 'ALL'` for identity cells, and the gap text says the value is a scope statement, not population evidence | T-3 |
| OR-2 | R2 + E1 | Does a determination carry conditional branches, shown beside a headline taken only from unconditioned claims, with an **empty** headline when every claim is conditioned? | **yes, empty** | yes: T-2 as written. "strictest branch" instead: T-2 step 1 composes the headline from all governing rows when none is unconditioned, and the note says so. no branches at all: T-2 is not built, and the book prints one number for a code's table (today's behaviour) | T-2, D-1 |
| OR-3 | R5 (extended) | May `claimed_value`, `claimed_unit` and a NULL `setting` be **reformatted in place**, with the same digits and the same quote and the old text kept in `notes` (`6%`→`6` with unit `%`; `30,0`→`30.0`; unit `ratio`→`rise:run ratio`; a conditional unit sentence → bare unit, the condition re-extracted as its own row)? This narrows D-0168 (`decisions/DR-2026-08-27-evidence-is-the-source-judgment-is-the-extraction.md`), which makes a wrong value "a SECOND ROW". | **yes** | yes: T-1 step 8 widens `amend-extraction`, and D-1 amends the repair set (the union of C21's and C22's rows). no: D-1 writes one new row per affected figure (batch 21's precedent: row 73 restating row 72 as `30.0`). The old rows stay as recorded contests and are still counted as unparsed in every `value_note` | D-1 (T-1 step 8) |
| OR-4 | R1(a) | Within the anchoring set (T1, Co-1, T2, Co-2), does the most accommodating value win whatever anchoring tier stated it (G3, G12, G13)? | **yes** | yes: no change (the 2026-07-21 rule as the engine extends it). no: the owner must state a composition rule; none exists ("the operands do not exist", ledger 2026-09-13), and T-4 waits | T-4 step 4 |
| OR-5 | E8 (premise restored) | Does `references/methodology-evidence-hierarchy-mapping.md` §6.4 hold, so that **Co-1 sets direction and barrier identification but not a dimensional value**, and the value comes from T1/T2/T3 (or the code minimum)? | **yes** | yes: T-4 step 3 leaves Co-1 rows out of the numeric bound (they still govern the state and are rendered beside the value), and §6.4's false sentence "this boundary is now mechanically expressed … by value-directness" is corrected. no: no engine change; §6.4's first sentence and its mechanism claim are deleted, and ARCH §2's claim-type split is restated as rendering guidance only | T-4 |
| OR-6 | R4 (corrected) | When anchoring claims **cannot all hold** (G8: ≥1200 against ≤1000), does the cell stay `stated` with convergence `divergent`, and refuse to be written until an Opus-class session supplies the synthesis approach, as evidence-methodology §3.3 already says? (That document's status is CANONICAL, and ratified ARCH lists it as doctrinal basis.) | **yes (§3.3)** | yes: T-4 step 2 as written. "cap at provisional" instead: T-4 step 2 writes `provisional` with a confidence flag naming the divergence and an optional synthesis approach. That amends §3.3 ("No fifth state. The cell is `stated`"), so the ledger records the supersession | T-4 |
| OR-6b | new | Do anchoring floors that differ but can all be met (G3: ≥900 and ≥1500) count as divergent? | **no** | no: not divergent; the spread is printed in `value_note`. yes: T-4 step 2 also marks any two distinct anchoring bounds on one side as divergent, so most multi-source cells need a synthesis approach | T-4 |
| OR-7 | R15 | Confirm what Option A already ratifies (tier-system §8 line 98; ARCH line 121): a T6-only cell (`code_floor_only = 1`) appears in `v_best_practice` as a flagged weak-band row? | **yes** | yes: T-5 step 2 drops `code_floor_only = 0` from the view. no: the view stays, and ARCH line 121 and tier-system line 98 are amended to say "T4/T5-only", which changes a ratified text | T-5 step 2 only |
| OR-8 | R7 / D4 | Is exhaustion judged per **parameter × bucket-1/2 jurisdiction × language**, with the bucket list entered once as a base table? | **yes** | yes: T-6 steps 4 and 5. no: coverage stays per slug × jurisdiction × language, and T-6 builds steps 1 to 3 only | T-6 steps 4 and 5 |
| OR-9 | R8 | Which indices must be searched for each evidence type? (Name them, or answer "none yet".) | **none yet** | none yet: T-6 step 6 is not built. named: T-6 step 6 adds `search_indices`, seeded with the named set | T-6 step 6 |
| OR-10 | R6 / E3 | May the engine compose across **exact linear units** (in, ft ↔ mm, m), presenting both, as it already does for ratio and percent? (This extends the 2026-09-17 ruling, whose ACTION (4) keeps units apart.) | **yes** | yes: T-1 step 9. no: every length parameter with US and metric sources declines with "different units" | T-1 step 9 |
| OR-11a | R12 | Does `extraction_status = 'verified'` require a recorded **full-scope** `source_scans` reading that covers the row's parameter? | **yes** | yes: T-1 step 10, and T-5 prints the status for each row. no: `verified` stays an unread, self-declared word. Nothing reads it today (Appendix A, A-12) | T-1 step 10 |
| OR-11b | D1c (open since 2026-10-09) | May a figure read in full but still `preliminary` (not reviewed) set a published value? | **yes, flagged** | yes: no engine change, and T-5 flags `preliminary` rows. no: add `preliminary` to the rule beside `dbcore.NOT_PUBLISHABLE_METHODS` (its comment forbids doing that without this answer) | nothing in T-1 to T-4 |
| OR-12 | R9 / R10 | (a) Are AR, BN, HI and SW, which `lang_jur_map` requires and which have no aliases, scoped out by the bucket table until buckets 1 and 2 are exhausted? (b) May a model-generated alias be used for a search if the search is flagged? | **yes; yes** | (a) no: alias building for four languages becomes research debt. (b) no: 1,163 aliases (C14) become unusable for searching at once | T-6 step 3 (flagging) |
| OR-13 | R11 + the unanswered 06:07 choice of 2026-10-09 | Seed the quantity list by an **open-pass scan of the bucket-1/2 codes already held**, rather than slug by slug? | **codes** | codes: D-8 as written. slugs: D-8 runs per slug from the slug's admitted sources | D-8 |
| OR-14 | R16 / D6 | Is a book page for an element (a ramp) **derived** from a typed term pointer (`quantity_of`) to its parameters' live determinations, with "one parameter" as the degenerate case, and never a container rows are filed into? | **yes** | yes: T-7 and D-6. no: pages are per parameter only, and Q6/E0 stay open | T-7 |
| OR-15 | D13 | Use held batch-23 material for the inter-rater test (one code with a step table plus one T1 paper with findings)? | **yes** | yes: D-5 as written. no: the owner names the material | D-5 |
| OR-16 | D10 / D11 | Read sources already held, in and out of buckets 1 and 2, before fetching more? | **yes** | yes: D-3 covers every unsuperseded source. no: D-3 is limited to bucket-1/2 jurisdictions | D-3 scope |
| OR-17 | D5 (pass "R19") | Bulk vocabulary approvals by the assistant under LED-154, with the owner reading the PR? | **yes** | no: each D-4 and D-8 approval table goes to the owner before minting | D-4, D-8 pace |
| OR-18 | R13 | Is the preserved transcript record (model and `effort` on every assistant message, `transcripts/harness_*/main.jsonl`) sufficient telemetry, or must the session record state them? | **transcripts suffice** | suffice: D-5 derives model and effort from transcripts. state them: every session record gains `Model:` and `Effort:` header lines (a convention last used 2026-07-25, C28) | D-5 reporting |
| OR-19 | R17 | Confirm the rebuttable-presumption shape for grey sources echoing a code value? | **yes** | no: T-8 does not apply it | T-8 step 3 |
| OR-20 | R14 | Mine T4 to T6 anchors backward, for root tracing only? | **no** | yes: an R2 amendment of the research contract, and D-7 gains a mining pass | D-7 |
| OR-21 | R18 | When a direction is `contested`, record a direction per lens? | **yes, when it first arises** | the trigger query is `C29`, which returns 0 today, so nothing is built now | nothing now |
| OR-22 | standing | Ledger "Correction 2026-10-22" item 2: what determination is a floor claim that a study (all rows `absent`) confirms? | owner | — | the REF-00980 cell |
| OR-23 | standing | tier-system §8: an unretrievable source keeps its tier and may anchor, earning no band above ○. Confirm? | **confirm** | — | none |
| OR-24 | standing | 2026-10-09 item 4 [ASSUMPTION]: "skimmed" means `extraction_method = 'skim'`. Confirm? | **confirm** | — | none |
| OR-25 | standing | Does batch 23's pilot extraction cap carry over to the scan contract (2026-10-09 ACTION 5)? | **no cap; one source is the review unit** (the 2026-10-09 recommendation, unratified) | yes, the cap carries over: D-3 stops each batch at the cap, which is derived from batch 23's own row count, never typed | D-3 batch size |
| — | D7, D9 | The category list; publishing Release 0 | not needed by this plan | — | — |

**The six that gate building**: OR-1, OR-2, OR-3, OR-5, OR-6 and OR-8. T-1 steps 1 to 7 need no ruling and can start now.

---
## 3. Work plan: pull requests in order (CLAUDE.md rule 10)

**Order.** Tooling first, each merged to `main` before any branch that depends on it opens:
T-1 reading → T-2 conditions → T-3 lens → T-4 agreement → T-5 render (plan step 3.R) → T-6 coverage → T-7 element pointer → T-8 roots.

T-6 and T-7 depend on nothing in T-1 to T-4 and may be opened in parallel with them. Research-data PRs follow their tooling (section 4):
- D-1 units and conditions (after T-1 and T-2)
- D-2 lens tagging (after T-3)
- D-3 scans (after T-1)
- D-4 aliases (any time; its `terms_used` half after T-6)
- D-5 inter-rater (after T-1)
- D-6 element pointers (after T-7)
- D-7 roots (after T-8)
- D-8 quantity seeding (after OR-13)
- S-1 determinations and the first render (after T-5, D-1, D-3)

### 3.0 Common protocol (every PR; each step is a command)

**P-1 Branch from the merged `main`.** PR #201 has merged and the current `scratchpad/CURRENT` (`session_2026-10-21-step-3-specification-marker`) names a merged PR's session, so it is stale (CLAUDE.md §7).
```bash
cd /home/user/guidebook
python3 scripts/preserve_transcripts.py            # copy out the previous session's transcripts
git fetch origin
git switch -c claude/<pr-slug> origin/main         # never `git checkout -B` or `git rebase` (blocked)
STEM="session_$(date -u +%Y-%m-%d)-<pr-slug>"
mkdir -p "scratchpad/$STEM" && echo "$STEM" > scratchpad/CURRENT && cat scratchpad/CURRENT   # folder name == CURRENT, same action
bash .claude/hooks/ensure-deps.sh; python3 -c "import pydantic, jsonschema"   # must print nothing
git status --short    # carried-over logs/transcripts: commit them with the work (rule 6), never alone without [skip ci]
```
State in the first status line whether this is a **tooling** or a **research** session (RC6; `/session-open`).

**P-2 Before writing.**
- Measure the baseline of the net-negative rule (C03).
- Derive the next schema migration number (C02). It is 117 today (measured 2026-10-22). Re-derive it at branch time, because two open PRs can claim the same number; the later one renumbers at merge.

**P-3 Schema migrations.**
- Use `scripts/migrations/NNN_<slug>.sql`. The last statement is `PRAGMA user_version = NNN;`.
- A header comment names every new column's or view's **reader** (rule 8).
- Map any new table in `governance/stage-map.yaml` `tables:` in the same PR.
- Verify with `python3 scripts/migrate_db.py --rebuild "$SCRATCH/rebuilt.db"` and a per-table count comparison (C34's last step), then regenerate `python3 scripts/generate/context_map.py`.
- `data/guidebook.db` changes **only** through `python3 scripts/migrate_db.py` (rule 3).

**P-4 Caller sweep for every rename or removal (rule 4).**
- The tree, through the Grep tool and also through `grep -r`, because `.ignore` hides `_archived/ audits/ sessions/ references/search-log/ versions/ workplan/_superseded/ transcripts/`. History paths need no edit but must be looked at.
- Views: C05.
- Skills: `grep -rln '<name>' skills .claude`.
- The registry: `grep -n '<name>' governance/check-registry.yaml`.
- The instrument: `grep -rn '<name>' workplan/pipeline-state-graph/` (atoms, `machines.yaml` needles).
- Prose: `grep -rn '<name>' governance references architecture workplan CLAUDE.md`.

**P-5 Tests and mutations.**
- Add the named tests.
- Write a harness `scratchpad/$STEM/<pr>-mutations.py` in the format of `scratchpad/session_2026-10-21-step-3-specification-marker/review-followup-mutations.py`: a list of `(name, path, old, new, test)` tuples; each edit is applied once, the test run, and the file restored.
- Every mutation listed must print `KILLED`. A `SURVIVED` mutation means the test is missing; it does not mean the mutation is wrong.

**P-6 Gate once, when the diff is ready.**
```bash
scripts/preflight.sh
python3 scripts/run_checks.py --changed-from origin/main --explain
python3 scripts/run_checks.py --selftest                      # after any registry, basis or name change
python3 workplan/pipeline-state-graph/build_graph.py --check  # plan W4: 0 failures; commit ATOMS.tsv and edited atoms if it re-anchors
```
- For every check the PR's acceptance criteria name, read its `EXAMINED:` line. A pass over 0 subjects is not a pass (CLAUDE.md §5(a)).
- A red that is also red on untouched `main` is not this PR's doing. Prove it with `git stash; <check>; git stash pop`.

**P-7 Net-negative statement (CLAUDE.md §8).** Run C03 and C03b and paste the two `--shortstat` lines into the PR body. When the total rises, the PR body carries this PR's exception text, given below, verbatim and with the measured figures filled in.

**P-8 Commit (rule 1).**
```bash
TS=$(date -u '+%Y-%m-%d %H:%M')
git add <paths> && git commit -F - <<EOF
governance: <action> [$TS]

<what changed and why; errors found, if any, described here and not in CLAUDE.md>

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_019DBbAfKYEE5x5qvYnBRp3W
EOF
python3 scripts/preserve_transcripts.py && git add transcripts scratchpad/$STEM && git commit -m "governance: session command log [$(date -u '+%Y-%m-%d %H:%M')]"
```
Use a project skill's name in place of `governance` only where one fits; `multilingual-research` fits a research batch.

**P-9 Open the PR last, once (rule 9).**
- `git push -u origin claude/<pr-slug>`. The final push is **not** `[skip ci]`.
- Create the PR (`create_pull_request`, base `main`). Its body holds: What, Evidence (commands and results), the net-negative paragraph, owner items, and then the two attribution lines:
  `🤖 Generated with [Claude Code](https://claude.com/claude-code)` / `https://claude.ai/code/session_019DBbAfKYEE5x5qvYnBRp3W`.
- Immediately afterwards call `unsubscribe_pr_activity` (owner `jordanelias`, repo `guidebook`, the new number).
- Never call `subscribe_pr_activity`, `send_later` or `create_trigger`. Push nothing more unless the change is deliberate.

**P-10 A dependent branch** takes a merged predecessor with `git fetch origin && git merge origin/main`. Never rebase.

---

### T-1 reading: every written figure is readable, or the writer refuses with the fix

**Purpose.** One home for notation arithmetic. The writer refuses figures the engine cannot read: a symbol in the value, `1/12`, `12:1`, `1 in 12`, a decimal comma, a spelled numeral without a gloss, a sentence in the unit, or a missing comparator on a value-supplying row. A derived figure that contradicts its own inputs is refused at write time.

**Resolves.** Q3, Q8 (half), Q13-trust (half), E2, E3 (if OR-10), Q2-assembly (derived arithmetic), Q4 (no new conditional units). It also closes GAP-056; the gap row itself is closed in D-1 with `db.py close-gap`, per rule 10.

**Prerequisites.** None for steps 1 to 7. OR-3 for step 8, OR-10 for step 9, OR-11a for step 10.

**Files.** `scripts/dbcore.py`, `scripts/assess/assess_cell.py`, `scripts/db.py`, `scripts/tests/test_db_amend_writers.py`, `scripts/tests/test_assess_cell_pilot.py`, and (step 8) the ledger entry recording OR-3.

**Steps.**

1. **Move the notation code to `dbcore` (stdlib only).**
   - Cut, in `assess_cell.py`, from the comment block that opens `#: NOTATIONS OF ONE QUANTITY` through the end of `def bound_on_scale` (locate both with `grep -n "NOTATIONS OF ONE QUANTITY\|^def bound_on_scale\|^def parse_bound" scripts/assess/assess_cell.py`).
   - Paste the block into `scripts/dbcore.py` after `ENGINE_EXTRACTION_COLUMNS`, and add `from fractions import Fraction` to dbcore's imports (`re` is already imported).
   - In `assess_cell.py`, import the names back, so the engine's public names stay valid for the test at `test_assess_cell_pilot.py` (its block that patches `_ac.NOTATION_FAMILIES["gradient"]`):
   ```python
   from dbcore import (NOTATION_FAMILIES, _CONVERTIBLE, notation_family,  # noqa: E402 -- one home (T-1)
                       to_canonical, from_canonical, bound_on_scale)
   ```
   - Also change that test to import `dbcore` and patch `dbcore.NOTATION_FAMILIES`. The dict object is shared, so both forms pass today, but the test should name the home.
2. **Delete `parse_bound`.**
   - `grep -rn "parse_bound(" scripts schemas workplan` returns only its own `def` (measured 2026-10-22; it is dead code, about 50 lines).
   - In `compose_value`'s comment "`parse_bound`'s own docstring says the comparator IS the bound", change the name to `bound_on_scale`.
   - Leave the ledger lines that name it (3644 and 3673; the ledger is append-only history).
3. **Add `dbcore.figure_refusal(value, unit, comparator, claim_type) -> str | None`.**
   - It returns `None` when `claim_type not in ("numerical", "range")`.
   - Otherwise it returns the refusal sentence. It returns `None` only when `bound_on_scale(...)` reads the figure **and** the figure is neither a slash ratio in a gradient unit nor an inverted gradient ratio. Sketch, not applied:
   ```python
   def figure_refusal(value, unit, comparator, claim_type):
       if claim_type not in ("numerical", "range"):
           return None
       v, u = (value or "").strip(), (unit or "").strip()
       if "/" in v and notation_family(u):      # bound_on_scale READS '1/12' (as 0.083 %), so test before it
           return "write a gradient ratio as rise:run (1:12), not 1/12, which reads as 0.083 %"
       b = bound_on_scale(v, u, comparator, claim_type)
       if b is None:
           if re.search(r"\d\s*%", v):          return f"write the number ({v.replace('%','').strip()}) and put % in --claimed-unit"
           if re.search(r"\d\s+in\s+\d", v):    return "write '1 in 12' as 1:12 with --claimed-unit 'rise:run ratio'"
           if re.search(r"\d,\d", v):           return "write a decimal comma as a point (30,0 -> 30.0); the digits stay the same"
           if ":" in v and not notation_family(u):
               return ("a ratio needs the unit 'rise:run ratio' -- if, and only if, the source measures "
                       "rise over HORIZONTAL run; rise over slope length is a different unit (E2)")
           if claim_type == "range":            return "write a range as 'a to b' (e.g. '0 to 4.8')"
           if not re.search(r"\d", v):          return "a number written in words needs --numeral-gloss WORD=DIGITS"
           return f"{v!r} with unit {u!r} cannot be placed on any scale"
       if notation_family(u) and ":" in v:
           rise, run = (Fraction(x) for x in v.split(":", 1))
           if rise > run:
               return "an inverted ratio (rise larger than run): write 1:12, and record the source's order in --notes"
       return None
   ```
   `[EXECUTED as a probe, not applied]`: this sketch and step 4's screen were run on the N1 to N8 inputs and on the controls (`0 to 4.8`, `20 ft`, a qualitative claim, `dB(A)`, `lx`). Each refused or passed as the test table below expects.
4. **Add `dbcore.unit_refusal(unit) -> str | None`, and move the value screen to dbcore.**
   - Move `_VALUE_BEARING` from `db.py` to `dbcore.VALUE_BEARING`, leaving `_VALUE_BEARING = dbcore.VALUE_BEARING` in `db.py` (one definition; `grep -n "_VALUE_BEARING" scripts/db.py` lists its five uses).
   - The screen refuses a unit when any of these holds:
     - `VALUE_BEARING.search(unit)`;
     - `re.search(r"[;,]|\b(where|if|unless|except|only|when)\b", unit, re.I)`;
     - `"(" in unit and not re.fullmatch(r"[A-Za-z]+\([A-Z]\)", unit)`. The exception lets a weighting unit such as `dB(A)` through.
   - The sentence returned: *"a unit names the scale only. Put a condition in its own row (`add-extraction --figure-role condition` on the parameter it measures) joined by `--relation condition_on`; put applicability (new build, alteration, building type) in `--setting`; put commentary in `--notes`."*
   - `[EXECUTED, C22]`: on the live corpus this screen refuses 27 of the 33 distinct `claimed_unit` values (33 of 101 rows). It passes `NULL`, `%`, `degrees`, `ft`, `ratio` and `rise:run ratio`.
5. **Wire the refusals into `db.insert_extraction`**, after the `_SVE_VOCAB_COLUMNS` loop (`grep -n "for col in _SVE_VOCAB_COLUMNS" scripts/db.py`):
   ```python
   for _why in (dbcore.unit_refusal(row.get("claimed_unit")),
                dbcore.figure_refusal(value, row.get("claimed_unit"), row.get("comparator"), claim_type)):
       if _why: raise Refusal(f"add-extraction: {_why}. Nothing was written.")
   if figure_role in ("claim", "derived") and claim_type == "numerical" and not row.get("comparator"):
       raise Refusal("add-extraction: a value-supplying numerical row needs --comparator "
                     "('=' for a point); a bare number is read as a point and adds a floor as well as a ceiling.")
   ```
   Every live numerical claim already carries a comparator (C23), so no existing writer route breaks.
6. **Add the numeral gloss.**
   - Add `p_ax.add_argument("--numeral-gloss", action="append", default=[], metavar="WORD=DIGITS")` to the add-extraction parser (`grep -n 'p_ax = sub.add_parser("add-extraction"' scripts/db.py`).
   - Pass `numeral_gloss=args.numeral_gloss` through the dispatch (`elif args.command == "add-extraction":`) into `insert_extraction(..., numeral_gloss=None)`, and on into `_require_verbatim(..., numeral_gloss=None)`.
   - In `_require_verbatim`, before raising on `missing` digits: for each `word=digits`, refuse when `_verbatim_norm(word)` is not in `body`; otherwise drop `digits` from `missing`.
   - Append `NUMERAL-GLOSS: <word>=<digits>` to `notes`. This is ledgered on the row, the way `VERBATIM-EXEMPT` is.
   - Refuse a gloss whose digits do not occur in `claimed_value`.
   - No per-language numeral table in code: the gloss records who judged the number.
7. **One home for derived arithmetic.**
   - In `insert_extraction`, after the edge loop, when `figure_role == "derived"`, run the check below inside the same connection. A refusal rolls back the row and its edges.
   - Do the same in `relate_extraction` when the from-row is `derived` and `relation == "derived_from"`.
   - Then delete the duplicate comparison in `derive_extraction`: the `if claimed_value is not None: … abs(cn - (bn + dn)) > 1e-9 … raise Refusal` block. Keep its computation branch, and keep the string "extract the base figure first with add-extraction", which `workplan/pipeline-state-graph/machines.yaml:230` uses as a needle.
   - The tolerance is the one `extraction_relations_integrity` uses (its `EPSILON`).
   ```python
   bad = conn.execute("SELECT stored, recomputed FROM v_derived_figure_check WHERE derived_id = ?",
                      (extraction_id,)).fetchone()
   if bad and abs(bad["recomputed"] - bad["stored"]) > 1e-9:
       raise Refusal(f"add-extraction: derived figure {bad['stored']} disagrees with its own "
                     f"base + delta ({bad['recomputed']}). Nothing was written.")
   ```
   - `[EXECUTED, C26]`: today `insert_extraction` accepts a derived row stored 99 against base 5.50 plus delta 9.01, on REF-01001 rows 42 and 43, on a scratch copy. `extraction_relations_integrity` then reports `VERDICT: FAIL`.
8. **(OR-3 = yes) Reformatting in place.**
   - Add `"claimed_value", "claimed_unit", "setting"` to `_AMENDABLE_SVE_FIELDS`.
   - Guard the new fields with `_normalisation_refusal(row, field, value)`, which refuses:
     - `claimed_unit` when `unit_refusal(new)` refuses;
     - `claimed_value` when `re.findall(r"\d+", new) != re.findall(r"\d+", old)`, because the digits must not change (`viisi prosenttia`→`5` is therefore refused and becomes a second row with `--numeral-gloss`);
     - `claimed_value` when `figure_refusal(new, <row's current unit>, …)` refuses. This is why D-1 always amends the **unit first, then the value**; the other order deadlocks on a prose unit;
     - `setting` unless the old value is NULL.
   - `ENGINE_EXTRACTION_COLUMNS` already lists `claimed_value` and `claimed_unit`, so the live-determination refusal applies (0 live determinations today, C10).
   - Rewrite the first refusal in `amend_extraction` to say: *"a different number or quote is a SECOND ROW and a contest (D-0168); reformatting the same digits is an amendment (owner ruling <date>)"*.
9. **(OR-10 = yes) Exact linear units.**
   - `NOTATION_FAMILIES["length"] = ("mm", "m", "in", "ft")`, with millimetres canonical. Factors, in `Fraction`: m ×1000, in ×254/10, ft ×3048/10.
   - Extend `to_canonical`, `from_canonical` and `_CONVERTIBLE`.
   - This changes engine behaviour, so bump `RULE_VERSION` (C36 shows the current label). The payload format is unchanged, so K01 needs no edit.
   - Otherwise the move in steps 1 and 2 changes no behaviour and no bump is made.
10. **(OR-11a = yes) The `verified` gate.**
    - In `insert_extraction`, and in `amend_extraction` for field `extraction_status`, refuse `verified` unless a full-scope reading covers the row:
    ```sql
    SELECT 1 FROM source_scans WHERE ref_id = ? AND text_scope = 'full'
       AND ((mode = 'catalogue' AND catalogue_version >= ?) OR (mode = 'targeted' AND target_parameter_id = ?))
    ```
    - Its reader is T-5, which prints each row's status. Do not add a parity check between status and scans (rule 5).

**Caller sweep (rule 4).**
```bash
grep -rn "parse_bound\|assess_cell\.\(NOTATION_FAMILIES\|to_canonical\|from_canonical\|bound_on_scale\|notation_family\|_CONVERTIBLE\|_RATIO_RE\)" scripts schemas workplan skills .claude governance
grep -rn "_VALUE_BEARING" scripts                        # db.py's five uses keep the alias
grep -rn "parse_bound\|_VALUE_BEARING\|derive_extraction" workplan/pipeline-state-graph   # machines.yaml:230 needle must still match
grep -rn "parse_bound" governance references architecture --include=*.md    # history in the ledger only; no edit
```
Views: C05 with `parse_bound`, which returns nothing. Registry: no entry names these functions.

**Tests to add.**

`scripts/tests/test_db_amend_writers.py`, a new "Section N (notation, T-1)". Each case runs through `refusal(db.insert_extraction, …)` or `run_cli("add-extraction", …)`. Ids are read from the copy, never typed: the probe source is `q("SELECT ref_id, claim_text FROM source_value_extractions WHERE extraction_id = (SELECT MIN(extraction_id) FROM source_value_extractions WHERE claimed_unit='rise:run ratio' AND figure_role='claim')")`.

| id | input | expect |
|---|---|---|
| N1 | value `8.33%`, unit `%` | refused, the message contains "put % in --claimed-unit" |
| N2 | value `1/12`, unit `rise:run ratio` | refused, "not 1/12" |
| N3 | value `12:1`, unit `rise:run ratio` | refused, "inverted" |
| N4 | unit `rise:run ratio (maximum) where the height difference is <= 0.05 m` | refused, "condition_on" |
| N5 | value `1:12`, unit `ratio` | refused, "rise:run ratio" |
| N6 | numerical claim, no `--comparator` | refused |
| N7 | `1:12` / `rise:run ratio` / `<=` (control) | accepted; a qualitative claim with unit NULL is also accepted (control) |
| N8 | row 80's quote (`claimed_value='viisi prosenttia'`), value `5`, unit `%`, no gloss | refused (digit 5 not in the quote); with `--numeral-gloss viisi=5`, accepted, and `notes` contains `NUMERAL-GLOSS: viisi=5` |
| N8b | the gloss `kuusi=6` on the same quote | refused, the word is not in the quote |
| N9 | derived row via `insert_extraction` on REF-01001, base and delta its two `%` findings (looked up: `SELECT extraction_id FROM source_value_extractions WHERE ref_id='REF-01001' AND claimed_unit='%' ORDER BY 1`, 42 and 43 today), value `99` | refused, and the row count is unchanged |
| N10 | the same with value `14.51` (control) | accepted |
| N11 | `derive_extraction` with a mismatched `--claimed-value` | still refused (now by the shared check) |
| N12 | (OR-3) amend `6%`→`6` / unit `%` (accepted); `6%`→`7` (refused); unit → a prose string (refused); `setting` on a row whose setting is set (refused) | as stated |

`scripts/tests/test_assess_cell_pilot.py`: assert `dbcore.bound_on_scale` on the C24 table. `('1:12','rise:run ratio','<=','numerical')` gives `(None, Fraction(25,3))`; `('8.33','%','<=','numerical')` gives `(None, Fraction('8.33'))`; with OR-10, `('36','in','>=','numerical')` gives `(Fraction(4572,5), None)`.

**Mutations** (each must be KILLED):

| id | file | one-line edit | turns red |
|---|---|---|---|
| M1 | `scripts/dbcore.py` | in `unit_refusal`: `if VALUE_BEARING.search(u)` → `if False` | N4 |
| M2 | `scripts/db.py` | the comparator refusal's condition → `if False:` | N6 |
| M3 | `scripts/dbcore.py` | first line of `figure_refusal` body → `return None` | N1, N2, N5 |
| M4 | `scripts/db.py` | `> 1e-9` in the new derived check → `> 1e9` | N9 |
| M5 | `scripts/db.py` | the gloss word-in-quote refusal → `if False:` | N8b |
| M6 | `scripts/db.py` | (OR-3) the digit-identity comparison → `if False:` | N12 (`6%`→`7`) |

**Acceptance.**
- `python3 scripts/tests/test_db_amend_writers.py` shows every case `[✓]`, including N1 to N12.
- `python3 scripts/tests/test_assess_cell_pilot.py` passes.
- `python3 scripts/audit/extraction_relations_integrity.py` reports `VERDICT: CLEAN` with `EXAMINED:` > 0.
- `grep -rn "def parse_bound" scripts` prints nothing.
- `python3 -I <scratch>/fixtures_g1_g13.py "$PWD"` (Appendix C, C32) is byte-identical to its pre-change output, because the move changes nothing.
- The mutation harness prints KILLED six times.
- `build_graph.py --check` reports 0 failures.

**Registry.** No change. The two test files are already registered (`test_db_amend_writers`, `test_assess_cell_pilot`, advisory).

**Guard against the likely error.** An executing agent will be tempted to "fix" the 45 unreadable live rows inside this PR. That is research data (rule 10) and goes in D-1. A second risk is applying the parse refusal to qualitative or absent rows, which is why N7's qualitative control exists.

**Net-negative exception text.** *"This PR adds writer refusals (unit screen, figure readability, comparator, numeral gloss, derived arithmetic) and moves the notation arithmetic to one home in dbcore. It replaces: `parse_bound` (dead, ~50 lines), the duplicate arithmetic check in `derive_extraction`, and the engine-local copy of the notation code. Measured: <C03>; non-test: <C03b>. The rise is regression cover for refusals that close GAP-056 and the stress-test findings of 2026-10-22."*

**Commit.** `governance: writer refuses unreadable figures and conditional units; notation arithmetic has one home in dbcore; derived arithmetic refused at write [TS]`

---

### T-2 conditions: a conditioned claim never sets the headline

**Purpose.** Governing rows that carry an outgoing `condition_on` edge (075's own meaning: "this figure only holds given a second figure") leave the headline composition and become branches. The `value_note` says how many. A new `condition_on` edge cannot silently move a live answer.

**Resolves.** Q4, Q5 (mechanism), Q8 (conditionals), E1 (with D-1's condition rows), and Q2-cross (the edge is how one parameter checks another).

**Prerequisites.** T-1 merged; OR-2 answered.

**Files.** `scripts/assess/assess_cell.py` (`compose_value`, `RULE_VERSION`), `scripts/db.py` (`_write_relation_edge`), `scripts/tests/test_assess_cell_pilot.py`, `scripts/tests/test_db_amend_writers.py`.

**What the live edges are.** Measured 2026-10-22 (re-run C20):
- 10 `condition_on` edges exist.
- 7 run **from** `condition` rows, five of them gradient relaxations pointing at the general claim they relax (rows 23, 83, 108, 97, 111). The engine already links those rows `conditioning` and never composes them.
- 1 runs from a finding (18→17).
- 2 run from skimmed claims (45→44 and 51→50), which never govern.
- So **no governing row has an outgoing `condition_on` edge today**, and T-2 changes no live value. C20's second query must print `0` before and after the change.

**Steps.**
1. In `compose_value(conn, links, direction)`, immediately after `ids = [l["extraction_id"] for l in gov]`:
   ```python
   conditioned = set()
   if _table_exists(conn, "extraction_relations"):
       conditioned = {r[0] for r in conn.execute(
           "SELECT DISTINCT from_extraction_id FROM extraction_relations WHERE relation = 'condition_on' "
           "AND from_extraction_id IN (%s)" % ",".join("?" * len(ids)), ids)}
   headline = [i for i in ids if i not in conditioned]
   if not headline:                                   # OR-2 default: empty headline
       return None, None, None, (f"piecewise only: all {len(ids)} governing claim(s) are conditioned "
                                 f"(condition_on); the branches are the answer"), None
   ```
   - Compose from `headline`, not `ids`. Use `rows = conn.execute(... WHERE extraction_id IN (headline))`.
   - Append to the returned note: `f"; {len(conditioned)} conditioned claim(s) are branches, not the headline"` when `conditioned` is non-empty.
   - OR-2 "strictest branch" branch: replace the early return with `headline = ids`, and the note says *"headline is the strictest of N conditioned branches"*.
   - Link roles are **unchanged**: conditioned rows stay `governing`, so K02 is satisfied and `derivation_sha` does not move.
2. Bump `RULE_VERSION` from the label C36 prints to the next pilot label, with a comment block: *"T-2: conditioned governing claims are branches, not the headline. Payload format unchanged; K01/K02 read this label as a link-set version."*
   - `stale_determinations` compares only rows of the current version. Rows of an earlier version are history and are re-determined by retire-and-run.
3. In `db._write_relation_edge`, after the `if relation == "confirms": _refuse_live_confirmation(...)` line:
   ```python
   if relation == "condition_on" and dbcore.live_determinations_linked(conn, from_id, governing_only=True):
       raise Refusal(f"{context}: extraction {from_id} governs a live determination; a condition_on edge from it "
                     f"would move it out of that headline without re-deciding it. Retire the specification first "
                     f"(db.py retire-specification), add the edge, re-determine. Nothing was written.")
   ```
   - Edges **to** a governing row from a condition row (the relaxation shape) are not refused: they change what T-5 renders, never the stored answer.

**Caller sweep.**
- `grep -rn "RULE_VERSION\|pilot-4" scripts governance references --include=*.py --include=*.md --include=*.yaml` must show only the engine, the tests, and history.
- K01/K02's `LEGACY_SHA_VERSIONS` stays `("pilot-2",)`.

**Tests.**

`test_assess_cell_pilot.py`, section "T-2 branches". Extend `synth_db` to `CREATE TABLE extraction_relations (relation_id INTEGER PRIMARY KEY AUTOINCREMENT, from_extraction_id INT, relation TEXT, to_extraction_id INT, to_label TEXT, input_role TEXT)`, empty by default, with an `edges=()` argument.

| id | fixture (lower_is_better, unit `rise:run ratio`, comparator `<=`) | expect |
|---|---|---|
| B1 | T1 `1:12` unconditioned; T1 `1:20` with `condition_on` → a condition row on parameter 2 (`0.5`, `m`, `>`) | `value_max == 100/12`; note contains "1 conditioned claim(s)". Today: `5.0`. |
| B2 | the NL five-step table: five T6 rows `1:6, 1:10, 1:12, 1:16, 1:20`, each conditioned on a level-difference row | value `None`, note starts "piecewise only". Today: `5.0`. |
| B3 | no edges (control) | identical to today's `compose_value` result |
| B4 | NO: T1 `1:15` unconditioned plus T1 `1:12` conditioned on run `<3 m` | `value_max == 100/15`, note names 1 branch |

`test_db_amend_writers.py`, Section "B (T-2)". `unretire(con, spec)` a retired determination whose links include a governing row (`q("SELECT l.specification_id, l.extraction_id FROM specification_extraction_links l WHERE l.role='governing' LIMIT 1")`). Then:
- B5: `relate-extraction --from <that row> --relation condition_on --to-extraction <a condition row of the same source>` is refused.
- B6: the same edge from a condition row is accepted.
- Finish with `reretire(...)`.

**Mutations.**
- M7: `headline = [i for i in ids if i not in conditioned]` → `headline = list(ids)`. Kills B1, B2.
- M8: the new `condition_on` refusal's condition → `if False and`. Kills B5.

**Acceptance.**
- The tests pass; KILLED ×2.
- C20's governing-edge query prints 0.
- C32's fixture output is unchanged.
- On a scratch copy, C30's parameter-3 MOB cell still prints `max 5.0` (no governing edge in the corpus).

**Registry.** None.

**Guard.** Do not read the five relaxation edges as "the claim is conditioned". They point **from** the relaxation **to** the general claim. Reading them the other way would push the general Japanese, Korean and Portuguese claims out of the headline.

**Net-negative exception.** *"Adds the branch partition (~25 lines) and one refusal. Replaces no code; the rise is test cover. Measured: <C03>/<C03b>."*

**Commit.** `governance: a conditioned claim is a branch, not the headline; condition_on edges refused under a live determination [TS]`

---
### T-3 lens: a lens is a column, not a traversal

**Purpose.**
- A row reaches a cell only through the lens codes written on the row (D-0184; RULINGS R33). Rows of other lenses are linked `excluded`, with the reason.
- A multi-lens cell hashes its whole lens.
- A pending cell stops claiming a derivation path.
- A lens code can be filled on an existing row, with warrant: the crossing is written at judgment.

**Resolves.** Q7, Q9, E6 (half), and the pending function-only defect (verdict item 4).

**Prerequisites.** OR-1 and OR-1b answered; T-2 merged (one `RULE_VERSION` sequence).

**Files.**
- `scripts/assess/assess_cell.py`: `_gather`, `gather_sources`, `gather_findings`, `gather_confirmers`, `gather_extraction_links`, `count_extractions`, `determine`, `sha`, `gap_account`, `stale_determinations`.
- `scripts/dbcore.py`: `ENGINE_EXTRACTION_COLUMNS`.
- `scripts/db.py`: `_AMENDABLE_SVE_FIELDS`, `amend_extraction`.
- `scripts/tests/test_db_integrity.py`: K01.
- `scripts/audit/derivation_handshake_integrity.py`: the NULL-paths note.
- `scripts/tests/test_assess_cell_pilot.py`: `synth_db`.

**Steps.**
1. Add `_lens_clause(lens, alias)` to the engine. With OR-1b = yes, add `OR {alias}.identity_code = 'ALL'` to the second group, for cells that state an identity.
   ```python
   def _lens_clause(lens, alias):
       """A row reaches a cell only through the lens codes written on it (D-0184; RULINGS R33):
       for every lens the cell states, the row states the same code or none, and it states at
       least one of them. Crossing maps are not traversed."""
       stated = [c for c in LENS_ORDER if lens.get(c)]
       agree = " AND ".join(f"({alias}.{c} IS NULL OR {alias}.{c} = ?)" for c in stated)
       some = " OR ".join(f"{alias}.{c} = ?" for c in stated)
       vals = [lens[c] for c in stated]
       return f"AND ({agree}) AND ({some})", (*vals, *vals)
   ```
2. Give `gather_sources(conn, parameter_id, lens)`, `gather_findings(…, lens)` and `gather_confirmers(…, lens)` the lens, and append `_lens_clause(lens, "x")` to the `where` that `_gather` receives. In `determine`, pass `lens` to all three.
3. Give `gather_extraction_links(conn, parameter_id, governing_refs, lens, cause=None)` the lens.
   - Select the four lens columns as well.
   - **Before** every other branch: if the row fails the predicate, set `role, why = "excluded", f"stated in lens {row_lens}; this cell is {cell_lens}; a row reaches a cell only through its own lens codes (D-0184, RULINGS R33)"`.
   - Keep linking **every** extraction of the parameter. K02 (`test_db_integrity.py`) requires the junction to account for all of them.
4. Add `n_extractions_in_lens` to the determination dict (the count of rows passing the predicate). In `gap_account`, add a first branch: when `det_x > 0` and `n_extractions_in_lens == 0`, the cause is *"{det_x} extraction(s) exist for parameter P, none stated in this cell's lens ({cell_lens}); they are stated in {lenses with counts}. A lens is a column, not a traversal (D-0184)"*. The remedy is *"read admitted sources for this population or function, and tag a row's lens at judgment only with warrant (`db.py amend-extraction --field <lens column>`)"*.
5. Make `sha()` hash the four-tuple: `payload = f"{parameter_id}|{'|'.join(lens.get(c) or '' for c in LENS_ORDER)}|" + link_payload(links) + "::" + RULE_VERSION`. Change its caller in `determine` to `sha(parameter_id, lens, links)`. Keep `lens_key` for display only.
6. Bump `RULE_VERSION`. In `test_db_integrity.py` K01:
   - Select the four lens columns.
   - Add the closed set `COALESCE_LENS_SHA_VERSIONS = (<every link-set label before this bump>)`, derived from `git log -p -S'RULE_VERSION = ' -- scripts/assess/assess_cell.py`. It is `("pilot-3", "pilot-4", <T-2's label>)` if T-2 landed first.
   - Build `lens` as the COALESCE for those versions and as the four-tuple string otherwise.
   - This mirrors the existing closed-set rule (`LEGACY_SHA_VERSIONS`), so the next bump needs no edit.
7. Add the four lens columns to `dbcore.ENGINE_EXTRACTION_COLUMNS`, because the engine now reads them. In `db.py`:
   - Add them to `_AMENDABLE_SVE_FIELDS`.
   - In `amend_extraction`, refuse a lens column unless the old value is NULL: changing a stated lens is a contest, a second row.
   - `--reason` is the warrant (the quote stating the population or function). `fk_declared` already checks the code is live.
8. In `stale_determinations`, the recompute already passes `lens`; confirm it still matches the four columns.
9. Remove the derivation-path claim from pending cells. In `determine`, after the H4 cap:
   ```python
   if state == "pending":          # nothing is derived for a cell with no answer
       functional_basis = derivation_paths = derivation_rationale = None
   ```
   The `specifications` CHECK permits `derivation_paths IS NULL`. In `derivation_handshake_integrity.py`, change the `if paths is None:` note so that a `pending` row with NULL paths is expected rather than reported as "written before migration 080".
10. Change the rationale wording in `derivation_handshake` for ICF and need cells. "no identity_icf_map row characterises this lens" is replaced by *"this cell is stated in an ICF or need lens; the function path is read only for an identity lens (identity_icf_map)"*. The text only; the path semantics are an owner question (section 8).

**Caller sweep.**
```bash
grep -rn "gather_sources(\|gather_findings(\|gather_confirmers(\|gather_extraction_links(\|lens_key(\|\bsha(" scripts workplan --include=*.py
grep -rn "ENGINE_EXTRACTION_COLUMNS\|_AMENDABLE_SVE_FIELDS" scripts
grep -rn "COALESCE(identity_code, icf_code, needs_code, medical_code)" scripts governance   # K01 and the views: the views keep COALESCE as display
grep -rn "identity_icf_map row characterises" scripts workplan references governance
```
Views that COALESCE the lens (`v_item_provenance`, `v_determination_provenance`) are display only and are not changed. Confirm with C05 on `COALESCE(s.identity_code`.

**Tests.**

`test_assess_cell_pilot.py`:
- Give `synth_db` a `row_lens=None` argument (default `{"identity_code": "MOB"}`) that sets the four lens columns on every extraction. Per-source dicts may override it with their own `identity_code`, `icf_code` or `needs_code`.
- Update the four existing calls whose cell lens is not MOB (`grep -n '"identity_code": "DEM"\|"identity_code": "NEU"\|"icf_code": "AX-AMB"' scripts/tests/test_assess_cell_pilot.py`) to pass `row_lens` equal to the cell lens, so they keep testing what they were written for.
- New cases:

| id | fixture | expect |
|---|---|---|
| L1 | 3 T1 claims tagged MOB; cell `{identity_code: AUT}` | `state == 'pending'`; every link `excluded` with "D-0184"; `len(links) == 3`; the gap cause contains "AUT" |
| L2 | the same rows; cells (MOB) and (MOB, icf d450) | both `stated`; different `derivation_sha` |
| L3 | a row tagged (MOB, d450) and a row tagged MOB only; cell `{icf_code: d450}` | only the first governs |
| L4 | a row tagged identity ALL; cell AUT | excluded (OR-1b = no) or governs (OR-1b = yes) |
| L5 | no rows for the cell; identity has `identity_icf_map` rows | `derivation_paths is None` |

`test_db_amend_writers.py`: amend `icf_code` from NULL succeeds; amend a non-NULL `identity_code` is refused; amend under an `unretire`d live determination is refused (lens columns now engine-read).

**Mutations.**
- M9: `_lens_clause` returns `("", ())`. Kills L1, L3.
- M10: the `sha()` payload back to `lens_key(lens)`. Kills L2.
- M11: delete step 9's `if state == "pending":` block. Kills L5.
- M12: remove the lens columns from `ENGINE_EXTRACTION_COLUMNS`. Kills the amend-under-live test.

**Acceptance.**
- `[NOT EXECUTED]` C30 on a fresh copy after the change should show AUT, BLIND, ADHD and d450 `pending`. A-EFFORT should also be `pending`, with a "finding only" gap: its one row, 33, is a qualitative finding.
- MOB and (MOB, d450) should differ in sha. MOB's value should stay `max 5.0`.
- `GUIDEBOOK_DB_PATH=<populated scratch> python3 scripts/tests/test_db_integrity.py` should give K01 PASS and K02 PASS with a non-zero subject count.
- `python3 scripts/audit/derivation_handshake_integrity.py --db <populated scratch>` should print no "written before migration 080" note for a pending cell.

**Guard.** The pass's design (gather through `identity_icf_map` and `access_need_icf`) is exactly what D-0184 measured and rejected: "DEAF returns 20 items while AX-AUD returns 38". It would also route every MOB ramp row into the d530 (toileting) cell, because `identity_icf_map` holds MOB's whole functional profile (C15). Do not build it unless OR-1 = no.

**Net-negative exception.** *"Adds the lens predicate, the four-tuple attestation and the lens amendment path, and removes a false derivation claim from pending cells. Replaces the COALESCE lens key in the attestation. Measured: <C03>/<C03b>."*

**Commit.** `governance: a lens is a column, not a traversal; the attestation hashes the whole lens; a pending cell claims no derivation path [TS]`

---

### T-4 agreement: true exclusion reasons, recorded divergence, the Co-1 dimensional boundary, a fragility note

**Purpose.**
- An excluded value row names its true cause.
- Anchoring claims that cannot all hold are recorded as `divergent`, and cannot be written without a synthesis approach (evidence-methodology §3.3).
- Co-1 figures leave the numeric bound under OR-5.
- `value_note` reports how many rows set the selected bound and the spread of the bounds passed over.

**Resolves.** Q1, Q2-assembly (critical checks), E8, E13 and Q10-stepping (fragility), and E6 (spread text).

**Prerequisites.** T-1 (bounds parse); OR-4, OR-5, OR-6 and OR-6b answered. Land after T-3 to keep one `RULE_VERSION` sequence.

**Files.** `scripts/assess/assess_cell.py` (`determine`, `gather_extraction_links`, `compose_value`, `stale_determinations`, `main`), `references/methodology-evidence-hierarchy-mapping.md` §6.4 (prose), `scripts/tests/test_assess_cell_pilot.py`.

**Steps.**
1. **Exclusion causes.** In `determine`, after `classify`, build `cause: dict[ref_id, str]` from `recs`, first match wins:
   - `_is_disqualified(r)` gives "disqualified: verification closed with nothing found".
   - `not r["tier_consistent"]` gives "non-anchoring: tier not derivable from (evidence_type, scope)".
   - `r["conditioning"] in (COND_NON_ANCHORING, COND_DISCOUNTED)` gives `f"non-anchoring on directness ({r['conditioning']})"`.
   - Co-1 and not `_verified(r)` gives "Co-1 counts toward a value only when VERIFIED (evidence-methodology §2.2)".
   - Otherwise: `f"outranked: the cell rests on {tier_basis}; this {stratum} row is shown as the code floor and spread (evidence-architecture §5, invariant I2), not discarded"`.

   Pass `cause` to `gather_extraction_links`. In its "value-supplying, but not governing" branch, use `cause.get(ref, <the old sentence>)`. The reason text is not hashed, so the sha is unaffected.
2. **Divergence (OR-6 default).**
   - Add `determine(..., synthesis_approach=None)`.
   - In the anchored branch, place the anchoring governing rows' bounds with `dbcore.bound_on_scale`. When all are on one scale, a point counts as `[v, v]`; let `lo = max(all lower bounds)` and `hi = min(all upper bounds)`. If `lo > hi`, the claims cannot all hold, and they are divergent. No tolerance: rule 7a.
   - If divergent and `synthesis_approach` is None, `main()` raises `Refusal`: *"anchoring claims cannot all hold (…list…); evidence-methodology §3.3 records this as `divergent` with a synthesis approach, which is judgment (contract synthesis/opus-routing). Re-run with --synthesis-approach-file <path> written by an Opus-class session."*
   - Otherwise set `conv_status = "divergent"`, `synth = synthesis_approach`, and keep `state = "stated"`. `compose_value` returns value NULL with the note *"anchoring claims diverge; the synthesis approach (convergence {id}) governs"*. The old "INCOHERENT INTERVAL … comparator" sentence stays only for a single-source point conflict.
   - Add `--synthesis-approach-file` to `main()`'s parser.
   - `stale_determinations` reads the stored approach through `specifications.convergence_id → convergence_assessment.synthesis_approach` and passes it to `determine`.
   - OR-6 "cap" branch: when divergent, set `state = "provisional"` and `conf = dict(present=[tier_basis], absent=["anchoring claims diverge: <bounds>"], basis="divergence recorded; synthesis approach owed")`; the approach is optional.
   - OR-6b = no: when the bounds intersect but differ, append to the note `f"governing {side} bounds range {min}–{max}; the most accommodating is selected (owner 2026-07-21)"`.
3. **Co-1 dimensional boundary (OR-5 = yes).**
   - In `compose_value`, join `evidence_sources` for `evidence_type`. Exclude Co-1 rows from `bounds`, recording them as `co1_figures`.
   - If no bound remains, return value NULL with the note *"the only numeric figures are Co-1 ({…}); Co-1 is co-primary for direction and barrier identification, not for dimensional values (methodology-evidence-hierarchy-mapping §6.4)"*. Otherwise append *"Co-1 figure(s) {…} are shown beside the value, not composed into it (§6.4)"*. State and marker are unchanged.
   - **Either answer to OR-5:** delete §6.4's sentence "This boundary is now mechanically expressed twice: by value-directness (…) and by grain (…)". Value directness is `NOT_ASSESSED` for every source (`assess_source`; stop condition 4). Under OR-5 = yes, replace it with *"applied at composition by assess_cell.compose_value (T-4)"*. Under OR-5 = no, delete the boundary clause as well. Re-run `python3 workplan/pipeline-state-graph/verify_atoms.py workplan/pipeline-state-graph/atoms/<file>` for any atom quoting §6.4 (`grep -rln "dimensional values" workplan/pipeline-state-graph/atoms`).
4. **Fragility (E13).**
   - Inside `compose_value` after selection: `n_set = sum(1 for b, _u in bounds if (vmin is not None and b[0] == vmin) or (vmax is not None and b[1] == vmax))`.
   - Note `f"the selected bound is stated by {n_set} of {len(bounds)} composed claim(s)"`.
   - Removing a row changes a min/max selection exactly when that row alone states the selected bound, so `n_set == 1` **is** the leave-one-out answer. No perturbation step and no threshold.
   - A ±N % harness stays in tests only: section 6, F-tests.
5. Bump `RULE_VERSION` (C36). K01/K02 need no edit.

**Tests.** Port the fixtures (C32) into `test_assess_cell_pilot.py` as assertions, through `synth_db` with `direction=`:

| id | expect after T-4 | today `[EXECUTED, C32]` |
|---|---|---|
| G2 (T1 ≥900 against three T6 ≥1200) | value 900; each T6 link's reason starts "outranked" | reason "disqualified on tier, verification or supersession" |
| G8 (T1 ≥1200, T2 ≤1000) | `Refusal` without an approach; with one: `conv=divergent`, state `stated`, synthesis stored | `stated ●`, note "INCOHERENT INTERVAL" |
| G3 (T1 ≥900, T1 ≥1500) | value 1500, conv unchanged, note "range 900–1500" | value 1500, no spread |
| G4 (T1 1000, Co-1 1500, T2 1200) | OR-5 = yes: value 1200, note names Co-1 1500. OR-5 = no: 1500 | 1500 |
| G12 / G13 | 1200 / 1800 (Co-1 excluded; T1 or T2 sets the value) | 1200 / 1800 |
| G1 | note "stated by 1 of 2" | no note |

**Mutations.**
- M13: `cause.get(ref, …)` → the old constant sentence. Kills G2.
- M14: the divergence test `if lo > hi` → `if False`. Kills G8.
- M15: the Co-1 exclusion filter removed. Kills G4 (OR-5 = yes).
- M16: `n_set` → `len(bounds)`. Kills G1.

**Acceptance.**
- Tests pass; KILLED ×4.
- `python3 scripts/tests/test_evidence_cell_state_2_3.py` and `python3 scripts/validate_evidence_state.py` pass: the pydantic model already requires `synthesis_approach` for `divergent`.

**Guard.**
- Never let the engine write a synthesis approach of its own: that is the Opus-floor judgment.
- Never add a divergence tolerance.
- Never implement a "value-directness grade" for OR-5. The §6.4 rule is a role rule (Co-1 does not set dimensional values), not a directness grading, so stop condition 4 is respected.

**Net-negative exception.** *"Adds exclusion causes, divergence detection with the canonical §3.3 recording, the §6.4 composition rule and a fragility note; replaces the single exclusion sentence. Measured: <C03>/<C03b>."*

**Commit.** `governance: excluded rows name their cause; unsatisfiable anchoring claims are recorded divergent per evidence-methodology 3.3; Co-1 figures shown beside, not composed into, dimensional values [TS]`

---

### T-5 render (plan step 3.R): one renderer over live determinations of every state

**Purpose.** One renderer prints every live cell, including pending and T6-only cells:
- its state and marker, and `provisional ●` told apart from `stated ●`;
- the value with both notations and its note;
- the flags: weak or code-derived with the convergence-not-evidence caveat, proxy, unverified;
- the code floors beside an anchored value (I2);
- the branches, including relaxations;
- governing qualitative claims verbatim;
- findings that the code is inadequate;
- code edition currency;
- the reading status of each row (OR-11);
- for a pending cell, its gap.

**Resolves.** Q0, Q8 (render), E4, E6, E7 (the handoff text), E10, and Q2-cross (it names the absence of a cross-parameter check).

**Prerequisites.** T-2, T-3 and T-4 merged; OR-7.

**Files.**
- New `scripts/generate/render_cells.py`. The plan's target is at most 300 lines, an estimate.
- New `scripts/tests/test_render_cells.py`.
- New migration `scripts/migrations/<C02+1>_render_views.sql`.
- `workplan/pipeline-state-graph/build_graph.py` (the probe P-K tuple).
- `governance/check-registry.yaml`.

**Steps.**
1. Write the migration. Its header names the reader of each view: `render_cells.py`.
   ```sql
   -- v_best_practice: OR-7 / Option A (tier-system §8 line 98): a T4-6-only cell, T6-only included, is a flagged weak-band row
   DROP VIEW v_best_practice;
   CREATE VIEW v_best_practice AS
       SELECT * FROM "specifications"
       WHERE state IN ('stated', 'provisional') AND retired_at IS NULL;
   -- v_determination_branches: the governing claims a condition qualifies (075's sense) and the condition rows that point at a claim (the relaxation shape)
   CREATE VIEW v_determination_branches AS
   SELECT l.specification_id, 'conditioned_claim' AS shape, g.extraction_id AS value_row, g.ref_id,
          g.claimed_value, g.claimed_unit, g.comparator, c.extraction_id AS other_row,
          c.parameter_id AS other_parameter_id, c.claimed_value AS other_value, c.claimed_unit AS other_unit,
          c.comparator AS other_comparator, r.quote
     FROM specification_extraction_links l
     JOIN specifications s          ON s.specification_id = l.specification_id AND s.retired_at IS NULL
     JOIN source_value_extractions g ON g.extraction_id = l.extraction_id
     JOIN extraction_relations r     ON r.from_extraction_id = g.extraction_id AND r.relation = 'condition_on'
     JOIN source_value_extractions c ON c.extraction_id = r.to_extraction_id
    WHERE l.role = 'governing'
   UNION ALL
   SELECT l.specification_id, 'qualifying_row', c.extraction_id, c.ref_id, c.claimed_value, c.claimed_unit,
          c.comparator, g.extraction_id, g.parameter_id, g.claimed_value, g.claimed_unit, g.comparator, r.quote
     FROM specification_extraction_links l
     JOIN specifications s          ON s.specification_id = l.specification_id AND s.retired_at IS NULL
     JOIN source_value_extractions c ON c.extraction_id = l.extraction_id
     JOIN extraction_relations r     ON r.from_extraction_id = c.extraction_id AND r.relation = 'condition_on'
     JOIN source_value_extractions g ON g.extraction_id = r.to_extraction_id
    WHERE l.role = 'conditioning';
   -- v_code_inadequacy: findings that a referent (a code value) is not enough, or more than needed (ruling 2026-09-13: rendered)
   CREATE VIEW v_code_inadequacy AS
   SELECT x.parameter_id, x.extraction_id, x.ref_id, e.tier, e.evidence_type, e.verification_status,
          r.relation, r.to_extraction_id, r.to_label, r.to_kind, r.quote, x.claim_text
     FROM extraction_relations r
     JOIN source_value_extractions x ON x.extraction_id = r.from_extraction_id
     JOIN evidence_sources e         ON e.ref_id = x.ref_id AND e.superseded_by_ref_id IS NULL
    WHERE r.relation IN ('insufficient', 'exceeds');
   PRAGMA user_version = <NNN>;
   ```
   `[EXECUTED as a sketch on the populated scratch copy, not applied]`: the three statements compile. `v_determination_branches` returned 7 `qualifying_row` rows and 0 `conditioned_claim` rows (no governing row has an outgoing edge until D-1). `v_code_inadequacy` returned 5. The redefined `v_best_practice` returned 1.
   - Two of the 7 qualifying rows are skimmed conditions pointing at findings (11→15, 12→16). The renderer prints a qualifying row as a **branch** only when its `other_row` is linked `governing` in the same specification, and otherwise as context.
   `v_code_floor_only` stays as the T6-only subset. No further views are needed:
   - the spread is `v_determination_provenance` filtered by role;
   - edition currency is `evidence_sources.code_currency_status` through the same view's `ref_id`;
   - the pending gap is `v_pending`.
2. **The renderer.** `python3 scripts/generate/render_cells.py [--db PATH] [--parameter-id N] [--out PATH]` writes Markdown to stdout or to `--out` (a scratch path; **no rendered file is committed**). For each live cell:
   - Query `SELECT … FROM specifications s WHERE s.retired_at IS NULL AND s.parameter_id = ?`, keeping that literal, because probe P-K finds a renderer by a string constant naming `specifications` and `parameter_id`.
   - Parameter name: `base_parameters → terms`. Lens labels: the four registries.
   - Value and `value_notations`; the selected bound's sources, recomputed with `dbcore.bound_on_scale` (no stored column).
   - Flags, with I3's wording.
   - Governing rows from `v_determination_provenance` (`claim_text` for qualitative claims).
   - "Code floor" lines: the excluded tier ≥ 4 rows whose reason starts "outranked", with the delta to the anchored value (I2).
   - Branches from `v_determination_branches`; inadequacy from `v_code_inadequacy` for the parameter.
   - "Edition currency unverified" for each tier ≥ 4 governing source whose `code_currency_status` is NULL (all 29 such sources today, C19).
   - The status of each row (OR-11).
   - For a pending cell, `v_pending.gap_description`.
   - The Person-Mode handoff: `functional_basis` codes, for the reader to take to an OT, with no value derived from it.
3. Add `"scripts/generate/render_cells.py"` to the tuple in probe P-K (`grep -n '"scripts/generate/build_site.py"' workplan/pipeline-state-graph/build_graph.py`).
4. Add a registry entry:
   ```yaml
   - id: test_render_cells
     cmd: [python3, scripts/tests/test_render_cells.py]
     battery: tests
     kinds: [tooling, data]
     level: advisory
     basis: hygiene
     cost: fast
     no_floor: selftest -- subject is its own fixtures, not a corpus; a floor would count the wrong thing
   ```

**Caller sweep for `v_best_practice` (redefined, not renamed).**
- C05 with `v_best_practice` returns no other view.
- Code: `scripts/audit/graph/extract_db.py`, `scripts/audit/migration_reproducibility.py` and the engine's comments; confirm none assumes T6-only rows are absent.
- Prose: `governance/evidence-architecture.md:121` and `governance/evidence-methodology.md:144` already say the view includes the regulatory-stratum cell, and become true for T6-only. Check `references/tooling-register.md`.

**Tests.** `scripts/tests/test_render_cells.py`:
- Copy the canonical DB to a temp directory.
- Write determinations with the engine (`subprocess` of `assess_cell.py --db <copy>` for parameters 3 to 12 under MOB, as C30 does), and create one T6-only cell with a `synth_db`-built database.
- Assert:
  - R1: the count of rendered cells equals `SELECT COUNT(*) FROM specifications WHERE retired_at IS NULL`, and the script prints `EXAMINED: <n>`.
  - R2: each `pending` cell prints its gap.
  - R3: a `regulatory_stratum_only` or `code_floor_only` cell prints the weak or code-derived flag.
  - R4: a cell with excluded tier ≥ 4 rows prints "Code floor".
  - R5: branches print when `v_determination_branches` has rows.
  - R6: the T6-only cell appears in `v_best_practice`.

**Mutations.**
- M17: delete the code-floor section. Kills R4.
- M18: filter `state IN ('stated','provisional')`. Kills R2.
- M19: drop the weak flag line. Kills R3.

**Acceptance.**
- `build_graph.py --check` reports 0 failures, and P-K reads PASS in `build_graph.py`'s output.
- `python3 scripts/generate/render_cells.py --db <populated scratch>` renders parameter 3 with "Code floor" lines and "piecewise" or branch lines once D-1 has landed.
- Walkability into render still prints NO PATH. That is by construction: a view's stage is the stage of the tables it reads (WALKABILITY finding 1). Record it in the PR. Do not invent a render table.

**Guard.**
- The renderer must not read `v_best_practice` as its source; it would lose pending cells.
- It must not commit output.
- It must not paraphrase claim text. Verbatim only; the source's language is kept.

**Net-negative exception.** *"A named exception (plan W3, step 3.R): replaces the five renderers step 1.1 deleted. Adds one renderer and two views. Measured: <C03>/<C03b>."*

**Commit.** `governance: step 3.R, one renderer over live determinations of every state, with branches, code floors, inadequacy and edition currency [TS]`

---

### T-6 coverage (independent of T-1 to T-5)

**Purpose.**
- Fold language labels to one case.
- Derive `terms_used` from the alias table.
- Report coverage reached through admissions, in the determination's unit (parameter).
- Under OR-8, scope coverage to buckets 1 and 2.

**Resolves.** Q10-coverage, Q11-search, E9, and Q12 (slug↔parameter is derived, never a column).

**Prerequisites.** OR-8, OR-9 and OR-12 for steps 4 to 6.

**Steps.**
1. `db.log_search`: `language = (language or "").strip().upper()`; refuse unless `re.fullmatch(r"[A-Z]{2}", language)`. This is a shape check, not a list. 21 rows are lower case today (13 `en`, 2 `fr`, 3 `ja`, 3 `nl`; measured 2026-10-22, re-run C13).
2. Migration `<NNN>_coverage_case_fold.sql`: drop and recreate `v_coverage_language`, `v_coverage_lens` and `v_coverage_priority`, with `UPPER(language)` wherever `search_executions.language` is grouped or compared. `v_coverage_priority` compares `se.language = ljm.language`, so today lower-case searches never satisfy an `EN` requirement. Do not UPDATE the 21 rows: `search_executions` is append-only history, and a fold in the view suffices.
3. Add `log-search --term TERM-NNN` (repeatable).
   - Derive `terms_used` as JSON `[{"term_id","alias","language","provenance"}]` from `term_aliases` where `term_id = ? AND upper(language) = <search language>`.
   - `provenance` comes from `alias_provenance_audit.classify(notes)`; import it, never restate it.
   - Refuse `--terms-used` together with `--term`.
   - Refuse a term with no alias in the search language unless `--alias-free "<reason>"` is given.
   - Under OR-12(b) = yes, a model-generated alias is accepted and its provenance is carried, so the coverage view can say "searched with unverified vocabulary".
4. (OR-8 = yes) In the same migration, create `jurisdiction_buckets(jurisdiction TEXT PRIMARY KEY, bucket INTEGER NOT NULL CHECK (bucket IN (1,2,3)), approval_ref TEXT NOT NULL)`.
   - Insert the members the owner approves. Map them to codes `dbcore.check_jurisdiction` accepts (`UK`, not `GB`). UN and ISO are not jurisdictions in the enum (batch 22 used `INT`), so the owner rules their codes.
   - `approval_ref` is the ledger heading of the ruling.
   - Map it as `base` in `stage-map.yaml`.
   - Make `workplan/2026-08-18-research-frame-proposal.md:420-424` point to the table (rule 5).
   - Redefine `v_coverage_priority` to `JOIN jurisdiction_buckets b ON b.jurisdiction = ljm.jurisdiction AND b.bucket IN (1,2)`.
5. (OR-8 = yes) `v_coverage_parameter_via_admission`, the only new reach. The direct route is already `v_coverage_lens`, which groups by `parameter_id`.
   ```sql
   CREATE VIEW v_coverage_parameter_via_admission AS
   SELECT x.parameter_id, UPPER(se.language) AS language, se.jurisdiction,
          COUNT(DISTINCT se.exec_id) AS searches, COUNT(DISTINCT sa.ref_id) AS sources_admitted
     FROM search_executions se
     JOIN search_admissions sa ON sa.exec_id = se.exec_id
     JOIN source_value_extractions x ON x.ref_id = sa.ref_id
    WHERE se.deferred_reason IS NULL
    GROUP BY 1, 2, 3;
   ```
   `[EXECUTED as a sketch on the populated scratch copy]`: it compiles and returns 21 rows over 18 jurisdictions. Readers: the `multilingual-research` skill's CHECK step (edit its text to query this view and `v_coverage_lens`), and `research_batch_dod.py` R1/R2 if the owner wants them to read it (no change otherwise).
6. (OR-9 named) `search_indices(index_code TEXT PRIMARY KEY, kind TEXT NOT NULL CHECK (kind IN ('academic','standards_body','dpo','web','repository')), approval_ref TEXT NOT NULL)`, seeded from the owner's list. `log-search` refuses an `--engine` not in it. Otherwise, do not build it.

**Tests.** In `test_db_amend_writers.py`, section "C6":
- `log-search --language fr` stores `FR`; `--language xx1` is refused;
- `--term TERM-001 --language JA` stores the JA aliases of TERM-001 in `terms_used`, read back as JSON;
- `--term` with no alias in that language and no `--alias-free` is refused.
- On the migrated scratch DB, `SELECT COUNT(DISTINCT language) FROM v_coverage_language` equals `SELECT COUNT(DISTINCT UPPER(language)) FROM search_executions` (13 today; C13).

**Mutations.**
- M20: remove `.upper()`. Kills the `FR` case.
- M21: drop the no-alias refusal. Kills that case.

**Guard.**
- Do not backfill `evidence_sources.language` from `lang_detected`. It would make a second home for one fact (rule 5): `lang_detected` is the home, and `db.py`'s unmined listing already reads `COALESCE(lang_detected, language)`.
- Do not UPDATE `search_executions` by hand.

**Net-negative exception.** *"Adds a language fold, `--term` derivation of `terms_used`, and (under OR-8) the bucket table and one coverage view. It replaces hand-typed `--terms-used` JSON. Measured: <C03>/<C03b>."*

**Commit.** `governance: search languages fold to one case; terms_used derived from the alias table; coverage reached through admissions [TS]`

---

### T-7 element pointer (OR-14 = yes)

**Purpose.** A typed pointer from a parameter's term to an element's term (`ramp`), so that an element page is **derived** from live determinations. Nothing is filed into a container.

**Resolves.** E0, Q6, and Q5 (assembly).

**Prerequisites.** OR-14 answered; T-5 merged (step 3 extends its renderer).

**Steps.**
1. Migration `<NNN>_term_relations.sql`. Map the table as `base` in `stage-map.yaml`.
   - `term_relations(relation_id INTEGER PRIMARY KEY AUTOINCREMENT, from_term_id TEXT NOT NULL REFERENCES terms(term_id), relation TEXT NOT NULL CHECK (relation IN ('quantity_of')), to_term_id TEXT NOT NULL REFERENCES terms(term_id), warrant_observation_id INTEGER REFERENCES observed_terms(observation_id), warrant_ref_id TEXT REFERENCES evidence_sources(ref_id), rationale TEXT NOT NULL, created_at TEXT NOT NULL, created_by_session TEXT NOT NULL, CHECK (warrant_observation_id IS NOT NULL OR warrant_ref_id IS NOT NULL), CHECK (from_term_id <> to_term_id), UNIQUE (from_term_id, relation, to_term_id))`.
   - One relation value: the vocabulary is judged, and it grows by migration with the owner's sign-off.
   - View `v_element_page`: `term_relations` (to an element) → `base_parameters` (`term_id = from_term_id`, `status='active'`) → live `specifications`.
2. Add the verb `relate-term --from-term --relation --to-term (--observation-id N | --ref-id R) --rationale --session`. It refuses:
   - a relation outside the CHECK;
   - a `from_term` that is not an active parameter's term;
   - a `to_term` that **is** an active parameter's term (an element is not a quantity: TERM-089 `ramp` is declined, C17);
   - a warrant observation whose `context_quote` contains neither term's `canonical_en` nor one of its aliases;
   - a `to_term` whose `canonical_en` matches `dbcore.VALUE_BEARING` or `db._ITEM_CODE`.
3. Add `--element TERM-NNN` to `render_cells.py`, which renders the page from `v_element_page`.
4. The BROADER and NARROWER **aliases** stay. They name phrases (subtypes such as "curb ramp"), not relations between terms; the reasoning pass's proposal to retire them is withdrawn (Appendix A).

**Tests.** The verb's refusals, each of the four with a control; `v_element_page` lists parameters 3 and 12 for TERM-089 after two `relate-term` calls on a copy.

**Mutation.** M22: remove the `to_term is a parameter` refusal. Kills its test.

**Guard.**
- Element terms come from observed phrases or approved catalogues only, never from the old Part 4 item index. Every `[A-Z]-NN` code is prior-version content.
- An element row holds no value.

**Net-negative exception.** *"Adds one table, one verb and one render flag for the element page OR-14 approved. Replaces nothing; the BROADER and NARROWER aliases stay. Measured: <C03>/<C03b>."*

**Commit.** `governance: a typed term pointer derives an element page from its parameters' determinations [TS]`

### T-8 roots (E5; after T-4)

**Prerequisites.** T-4 merged; OR-19 for step 3. **Files.** `scripts/db.py` (new verb), `scripts/assess/assess_cell.py` (`determine`), migration `<NNN>_value_independence_rows.sql`, tests in `test_db_amend_writers.py` and `test_assess_cell_pilot.py`.

**Steps.**
1. Add the verb `add-root --description --root-type --provenance-ref --session` writing `external_root_registry`. Its refusals:
   - a description that normalises to an existing one (`v_registry_duplicate_descriptions`);
   - a `root_type` outside its CHECK;
   - a root whose source is in the corpus, which is `--root-ref-id` on the extraction instead.

   This is RULINGS R24's filed GAP.
2. In `determine`, for anchored cells, write `convergent` only when two or more axes are present, the anchoring bounds intersect (T-4 step 2), and the governing rows have two or more distinct roots.
   - Count the roots through a new row-level view `v_value_independence_rows`: the `WHERE` of today's `v_value_independence`, without its `GROUP BY`.
   - In the same migration, redefine `v_value_independence` as an aggregate over it, so the engine and the view share one predicate.
   - The engine reads `SELECT COUNT(DISTINCT root) FROM v_value_independence_rows WHERE extraction_id IN (<governing rows>)`.
3. (OR-19 = yes) A grey row whose value equals a same-jurisdiction code row is reported in the engine report as a presumed echo. It is not re-tiered.

**Tests.** Two sources sharing a `root_ref_id` give `pending_assessment`; distinct roots that agree give `convergent`.

**Guard.** Do not claim `convergent` on axis co-presence alone. That is the G2 spirit the engine already honours.

**Mutation.** M23: the root-count condition → `True`. Kills the shared-root test.

**Net-negative exception.** *"Adds the registry writer RULINGS R24 filed as a GAP, and the root condition on `convergent`. Replaces nothing. Measured: <C03>/<C03b>."*

**Commit.** `governance: external roots have a writer; convergent requires two independent roots [TS]`

---

### 3.9 Research-data PRs

D-1, D-2, D-3, D-4, D-5, D-6, D-7, D-8 and S-1 follow in the order given at the top of this section. Each is a separate PR, opened under 3.0, and contains no tooling (rule 10). A writer gap found mid-batch is filed as a GAP and either left unwritten or written through verbs the CLI already has. Their procedures are in section 4.

---

## 4. Research-data work plan (after the tooling)

### 4.0 The ritual every data PR follows

1. **Open the session.** Follow P-1, with a research slug, e.g. `research-batch-25-units-and-conditions`. Say "research session" in the first status line.
2. **Make a scratch copy and record the canonical sha.** Its sha must not move until `migrate_db.py` runs.
   ```bash
   SCRATCH="$TMPDIR/$STEM.db"; cp data/guidebook.db "$SCRATCH"; sha256sum data/guidebook.db | tee "scratchpad/$STEM/canonical.sha"
   ```
3. **Write only through `db.py` verbs**, with `GUIDEBOOK_DB_PATH="$SCRATCH"` inline on **every** call, because the harness resets the environment between shells:
   ```bash
   GUIDEBOOK_DB_PATH="$SCRATCH" python3 scripts/db.py <verb> … --session "$STEM"
   ```
4. **Capture, emit, apply, verify:**
   ```bash
   sha256sum -c "scratchpad/$STEM/canonical.sha"                       # must print OK
   GUIDEBOOK_DB_PATH="$SCRATCH" python3 scripts/research/emit_batch_sql.py --scratch "$SCRATCH" \
       --canonical data/guidebook.db --out "scratchpad/$STEM/batch.sql"
   python3 scripts/emit_data_migration.py --session "$STEM.md" --summary "<one line>" --input "scratchpad/$STEM/batch.sql"
   python3 scripts/migrate_db.py --session "$STEM"
   python3 scripts/migrate_db.py --rebuild "$TMPDIR/$STEM.rebuilt.db"       # then C34's comparison: differing tables = []
   ```
   The session id is the **bare stem** in the database and `.md` in `--session` for `emit_data_migration` (CLAUDE.md §7).
5. **Definition of done.** Every line must pass:
   ```bash
   python3 scripts/audit/research_batch_dod.py --session "$(cat scratchpad/CURRENT)"
   python3 scripts/audit/adversarial_pass_audit.py --session "$(cat scratchpad/CURRENT)"
   python3 scripts/audit/search_log_completeness.py --session "$(cat scratchpad/CURRENT)"
   python3 scripts/audit/research_batch_dod.py --all          # posture not regressed
   ```
   Run `/adversarial` (the `antagonist` agent). Record the pass with `db.py record-adversarial-pass --subject-session "$STEM" --subject-commit <sha> --reviewer-transcript <path> --author-transcript <path> --session "$STEM"`; it derives the models from the transcripts.
6. **Session record and attestation (rule 2).** Write `sessions/$STEM.md` and `attestations/sessions_$STEM.json`, validated against `schemas/attestation.schema.json` (required keys: `schema_version`, `session`, `artifact`, `doctrine_sha`, `rules_in_scope`, `per_rule_status`, `deviations`, `bias_direction`, `independent_reviewer_counterclaim`, `verdict`).
7. Then P-6 to P-9. The commit uses `multilingual-research:` or `governance:`.

### D-1 units and conditions, parameter 3 (after T-1 and T-2; OR-2, OR-3)

**Repair set.** List the repair set and save it as `scratchpad/$STEM/repair-set.tsv`:
```bash
GUIDEBOOK_DB_PATH="$SCRATCH" python3 - <<'PY'
import os, sqlite3, sys; sys.path.insert(0, "scripts"); import dbcore
c = sqlite3.connect(f"file:{os.environ['GUIDEBOOK_DB_PATH']}?mode=ro", uri=True)
for eid, ref, role, ct, v, u, cmp_ in c.execute(
        "SELECT extraction_id, ref_id, figure_role, claim_type, claimed_value, claimed_unit, comparator "
        "FROM source_value_extractions ORDER BY extraction_id"):
    why = dbcore.unit_refusal(u) or dbcore.figure_refusal(v, u, cmp_, ct)
    if why: print(eid, ref, role, v, (u or "")[:60], why[:60], sep="\t")
PY
```
The output has 45 or more rows (measured 2026-10-22 with the engine's reader, re-run C21).

**Classify each row, then act.** A row may fall in several classes; apply them in table order, the unit first. With OR-3 = yes the action is an amendment. With OR-3 = no it is a second row, written with `add-extraction` and the same quote, and the old row stays.

| class | example rows | action |
|---|---|---|
| a. symbol in the value / decimal comma | 95, 96, 98–101, 103, 105 (`6%`…), 72 (`30,0`) | `amend-extraction --extraction-id N --field claimed_unit --value '%' --reason "OR-3: bare unit; the old text is kept in notes"`, **then** `--field claimed_value --value 6 --reason "OR-3: % moved to the unit"` |
| b. bare `ratio` | 52–54, 57, 58, 60–62, 64–66 | first open the persisted artefact at the row's locator and confirm the source measures rise over **horizontal run** (E2). If it does, `--field claimed_unit --value 'rise:run ratio'`. If it measures along the slope, record the finding in the session record and leave the row alone: a different unit should refuse to compose |
| c. a condition in the unit | 84–88 (height difference), 74 (relaxed to 1:12 for runs under 3.0 m), 78 and 81 (relaxed to 1:12 for flights ≤ 2000 mm going), 113 (rise between landings), 95, 96, 109, 110 (rise and projection), 103's two tolerances | A relaxed value stated inside the unit becomes its own `claim` row, conditioned as below. (i) Amend the unit to the bare unit. (ii) Mint the conditioning parameter once: `db.py add-parameter --term-id TERM-090 --notes "level difference: conditions ramp gradient (D-1)" --session "$STEM"` (run length is parameter 12 already). (iii) Write the condition: `add-extraction --ref-id <same> --parameter-id <12 or the new id> --identity MOB --claim-type numerical --claimed-value 0.05 --claimed-unit m --comparator '<=' --figure-role condition --claim-text "<verbatim clause>" --relation none --extraction-method full-read --session "$STEM"`. For a tier ≥ 4 source, add the structured locator R3 requires (`--locator-scheme … --loc-section …`; `add-extraction` refuses a regulatory-stratum value without one). (iv) Join them: `relate-extraction --from <gradient row> --relation condition_on --to-extraction <condition row> --stated named --quote "<verbatim>" --session "$STEM"` |
| d. applicability in the unit | 90 (new building), 103 (existing ERP/IOP) | amend the unit; `amend-extraction --field setting --value "<the source's own scope words>"` (allowed only from NULL) |
| e. a relaxation already encoded as a condition row | 23, 83, 108, 97, 111 | amend the unit only; their `condition_on` edge to the general claim stays (T-5 renders it as a qualifying row) |
| f. a spelled numeral | 80 (`viisi prosenttia`) | a second row: `add-extraction … --claimed-value 5 --claimed-unit % --comparator '<=' --numeral-gloss viisi=5 --claim-text "<row 80's claim_text>" --figure-role claim --relation none`; the 8 % relaxation as its own row with `--numeral-gloss kahdeksan=8`, conditioned (class c) on level difference ≤ 1000 mm |
| g. a denominator description (findings) | 72, 73 | amend the unit to `%`; the old text survives in `notes` |
| h. commentary or normative force (recommended, preferred, requested) | 76, 79, 94, 105 | amend the unit to the bare unit. The qualifier survives in `notes` through the amendment marker, and the session record lists these rows. Whether normative force earns a column is open (section 8, U-9) |
| d+c. both applicability and tolerances | 103 (existing ERP/IOP; 10 % over ≤ 2 m, 12 % over ≤ 0.50 m) | class d for the scope; class c for each tolerance |

**Close the gap.** `GUIDEBOOK_DB_PATH="$SCRATCH" python3 scripts/db.py close-gap --gap-id GAP-056 --status CLOSED-FIXED --session "$STEM"` (fixed by T-1). Check GAP-007 the same way: the code says it was closed 2026-09-18 and the row still reads OPEN (C38).

**Done when.**
- The repair-set query prints only rows deliberately left alone (class b on a slope-length source), each named in the session record.
- C20's first query lists the new edges.
- The rebuild matches.
- No determination is written in D-1. That is S-1, after T-5.

**Guard.** Every new row's `claim_text` is the source's verbatim clause, which the verbatim gate checks. A condition row is written only where the source states the condition; never infer one from the step pattern of another code.

### D-2 lens tagging (after T-3; OR-1)

1. For each extraction of a parameter, decide at judgment whether the source states its figure for a population or function beyond the tag it carries. The warrant is a quote naming the users, e.g. "wheelchair users" or "people who walk with aids".
2. Only with warrant: `GUIDEBOOK_DB_PATH="$SCRATCH" python3 scripts/db.py amend-extraction --extraction-id N --field icf_code --value d465 --reason "<verbatim warrant, locator>" --session "$STEM"`. This fills a NULL lens column only (T-3 step 7).
3. A code clause that applies to every user of a ramp is a scope statement. With OR-1b = no it is **not** a reason to tag AUT, BLIND or any other population. Those cells stay `pending` until a source is read for them, which is the honest state.
4. Done when the session record lists every tag with its warrant. C30 rerun then shows which lens cells moved from `pending`.

### D-3 scans: the scan contract, exercised (after T-1; OR-16, OR-25, OR-11a)

For each unsuperseded source (`SELECT ref_id FROM evidence_sources WHERE superseded_by_ref_id IS NULL`; 52 today, C18):
1. `python3 scripts/research/full_text.py --ref-id R --session "$STEM"`. A pre-1990 scan with no text layer cannot be read in full (GAP-028); record it as `--text-scope partial` and say so.
2. Read the derived text against **every** active parameter (`SELECT p.parameter_id, t.canonical_en FROM base_parameters p JOIN terms t USING(term_id) WHERE p.status='active'`). Write `add-extraction` rows for what the source states, and `observe-term` for every quantity phrase the list lacks (the open pass, R16).
3. Record the reading: `GUIDEBOOK_DB_PATH="$SCRATCH" python3 scripts/db.py record-scan --ref-id R --mode catalogue --text-scope full --file-sha256 <sha256 of the derived text> --method full-read --open-pass-done --session "$STEM"`.
4. Under OR-11a = yes, re-grade with `amend-extraction --field extraction_status --value verified` only rows whose source now has the full scan. List the 31 rows `verified` today: all 31 lack a scan, because `source_scans` is empty (C11).
5. Done when `python3 scripts/audit/scan_debt.py` shows the batch's pairs out of NOT-READ, and `SELECT status, COUNT(*) FROM v_scan_ledger GROUP BY 1` (C12) shows `READ-NOTHING-FOUND` > 0.

### D-4 aliases from observed phrases (any time; `terms_used` after T-6)

1. List the candidates (22 measured 2026-10-22, re-run C16):
   ```sql
   SELECT o.observation_id, o.surface_form, o.language, a.term_id FROM observed_terms o
     JOIN term_adjudications a ON a.observation_id = o.observation_id
    WHERE o.language <> 'EN' AND a.outcome = 'NAMES-EXISTING';
   ```
2. For each: `GUIDEBOOK_DB_PATH="$SCRATCH" python3 scripts/db.py add-alias --term-id <term_id> --observation-id <id> --alias-type TRANSLATION --session "$STEM"`. A refusal ("quote is not in a file saved for …") is recorded in the session record, never worked around.
3. Adjudicate the 11 unadjudicated observations (C16, second query) with `adjudicate-term --observation-id N --outcome <NAMES-EXISTING|NAMES-NEW|NOT-OURS|DEFERRED> --term-id … --rationale …`.
4. Done when `python3 scripts/audit/alias_provenance_audit.py` shows the attested column above 0.

### D-5 inter-rater and model or effort calibration (after T-1; OR-15, OR-18)

**What is measured.** Whether two readers, blind to each other, record the same rows from one source. Whether a model or effort difference changes what is recorded.

**Material.** Choose by query, not by hand:
- (a) The T6 source with the most conditioned rows: `SELECT x.ref_id, COUNT(*) FROM source_value_extractions x JOIN evidence_sources e USING(ref_id) WHERE e.tier = 6 AND (x.claimed_unit LIKE '%where%' OR x.claimed_unit LIKE '%relaxed%') GROUP BY 1 ORDER BY 2 DESC LIMIT 1`. Run this before D-1 or on a pre-D-1 copy.
- (b) The T1 or T2 source with the most `finding` rows: `SELECT x.ref_id, COUNT(*) FROM source_value_extractions x JOIN evidence_sources e USING(ref_id) WHERE e.tier IN (1,2) AND x.figure_role='finding' GROUP BY 1 ORDER BY 2 DESC LIMIT 1`.
- A code converges trivially, which is why (b) is included.

**Raters.**
- Rater A is an Opus-class session and rater B a Sonnet-class session. The owner sets the same effort for both, e.g. `high`. A third rater, C, is A's model at a different effort.
- Each rater is a separate harness session, launched by the owner with the model named.
- Each works on its **own** copy of the same canonical sha, and on the two sources only.
- The brief says: do not query `source_value_extractions` or `extraction_relations` for those `ref_id`s, and read the derived full text.
- Blindness is checked afterwards from the transcript: `grep -c "source_value_extractions" transcripts/harness_<id>/main.jsonl` must show no SELECT naming those ref_ids before the rater's first `add-extraction`.

**Scoring.** A script in `scratchpad/$STEM/inter_rater.py` reads the two scratch databases by `created_by_session`:
- **Match key**: (`ref_id`, `parameter_id`, `figure_role`, `normalise_quote(claim_text)`); a second pass keys on `source_section` / `loc_*` in place of the quote.
- **Coverage**: |A∩B| / |A∪B| on keys.
- **Field agreement** on matched keys: `claim_type`, `comparator`, the canonical bound (`dbcore.bound_on_scale`), `claimed_unit`, the set of `condition_on` targets.
- **Cohen's kappa** for `figure_role`, over rows matched on (`ref_id`, `parameter_id`, `normalise_quote(claim_text)`) alone. Matching on a key that includes `figure_role` would force agreement.
- Print `EXAMINED: <rows compared>`. Every figure is computed by the script and is never typed into a document.

**Telemetry.** Per rater, from `transcripts/harness_<id>/main.jsonl`:
- model (the `"model"` field);
- effort (`"effort"`);
- the sum of `"output_tokens"`;
- tool calls (count of `"type":"tool_use"`);
- wall time (first to last `"timestamp"`).

Map a database session to its harness id with `scratchpad/<stem>/commands.jsonl` (`session_id`). Store the report as `scratchpad/$STEM/inter-rater-report.md`, generated by the script with its commands printed beside each figure.

**Retrospective.** The same script can tabulate existing rows by model, but it cannot answer the causal question:
- Batches 16 to 23 map to harnesses; 08 to 15 and 20 have no command log (C28).
- Each batch read different sources, so model and source are confounded.

**Data.** The raters' rows are measurement, not corpus. Nothing from D-5 is emitted, unless the owner then adopts one rater's reconciled rows as a normal batch, through the ritual in 4.0.

### D-6 element pointers (after T-7)

Write `relate-term --from-term TERM-001 --relation quantity_of --to-term TERM-089 --observation-id <an observation of "ramp" whose quote names its slope> --rationale … --session "$STEM"`, and the same for TERM-091. Write one for TERM-090 only if the source warrant says the level difference is the ramp's.

### D-7 roots (after T-8)

Re-grade the 23 NULL and 6 `untraced` `root_type` rows (C09) with `amend-extraction --field root_type|root_ref_id`, and register external roots with `add-root`. Each move is warranted by the source's own citation.

### D-8 quantity seeding from the codes already held (OR-13)

For each bucket-1/2 code document admitted (tier ≥ 4, jurisdiction in `jurisdiction_buckets` once T-6 exists):
1. In the open pass of D-3, `observe-term` every quantity the code treats as a design quantity: handrail height, landing length, slip resistance and so on, in the code's own words.
2. `adjudicate-term`, then `add-term --from-observation`, then `add-parameter`.
3. A name taken from a registry (`references/standards-registry.md`, `references/tier456-verified-sources.json` and so on) goes through `mint-term-from-catalogue … --approval-ref "<dated ledger heading>"`, after an approval table is shown to the owner, or to the assistant under OR-17.

**Never** take a name from the old Part 4 item index.

### S-1 determinations and the first render (after T-5, D-1 and D-3)

On a scratch copy, run the engine for each parameter that has extractions × each lens that rows carry. Use C30's loop with `--slug <topic> --session "$STEM" --stamp "<fixed>"`. Then capture and apply per 4.0, and run `python3 scripts/generate/render_cells.py --db data/guidebook.db --out "$TMPDIR/render.md"`. The rendered file is never committed. C10 then counts live determinations.

---
## 5. Per-question resolution (cross-references; the steps are in sections 3 and 4)

**Q0. Stress test in all directions; attempt to render.**
- **Class.** GAP: no render surface (RC-H), plus one view that contradicts its doctrine.
- **Measured.**
  - Render is NO PATH in all ten render pairs, on canonical and on the populated scratch.
  - The write path replays and rebuilds with no table differing.
  - Two engine runs are byte-identical.
  - `v_best_practice` drops T6-only cells, which tier-system §8 (line 98) and ARCH (line 121) say render as flagged weak-band `[EXECUTED, C33/C34/C35; C06]`.
- **Resolved by.** T-5 (and OR-7); S-1 for the first real render.
- **Proof.** R1 to R6 in `test_render_cells.py`; P-K PASS.
- **Open.** Walkability will still say NO PATH by construction. Not a defect: the render stage holds no table, by the owner's own description of the stage.

**Q1. Competing rows; a gradient of conflicting values across tiers.**
- **Class.**
  - DEFECT: the exclusion reason is wrong.
  - GAP: divergence is never recorded.
  - DESIGN: tier-blind selection within anchors (RC-D).
- **Measured.** G1 to G13 reproduce `[EXECUTED, C32]`. G12 and G13 were re-specified by me; the 2026-10-22 script did not keep them.
- **Resolved by.** T-4 steps 1, 2 and 4.
- **Proof.** G2, G8 and G3 assertions; M13, M14.
- **Open.** OR-4, OR-6, OR-6b.

**Q2 (assembly). How are specifications critically assembled?**
- **Class.** DOCUMENTATION; the sequence in the register matches `determine`.
- **Absent checks.** Divergence (T-4), the Co-1 role (T-4, OR-5), and derived arithmetic. The last is refused at write in T-1 step 7: the engine itself does **not** read `v_derived_figure_check`, and the blocking `extraction_relations_integrity` reads it after the fact.
- **Proof.** N9 and N10; M4.

**Q2 (cross-referencing). Testing a parameter by related parameters.**
- **Class.** GAP with a ruled deferral (RULINGS R17: build nothing until a second parameter holds an extraction; trigger C08). RC-E.
- **Resolved by.** The mechanism for checking one parameter against another is the cross-parameter `condition_on` edge that D-1 writes (gradient → level difference or run length). D-1 also fires R17's trigger, so R17's revisit follows D-1.
- **Proof.** C08 > 1 after D-1; `v_determination_branches` lists `other_parameter_id ≠ parameter_id`.

**Q3. Ratios, percentages, degrees: a common base?**
- **Class.** DEFECT in the reader and writer. The family conversion is correct and ruled (RC-A).
- **Resolved by.** T-1 steps 1 to 6; D-1 classes a, b, f.
- **Proof.** N1 to N8 and C24. After D-1, C21 prints only rows left deliberately.

**Q4. A steeper slope allowed below one metre.**
- **Class.** DEFECT: a stepped rule prints as one number. GAP: no branch structure (RC-A, RC-B).
- **Resolved by.** T-2 (headline from unconditioned claims), T-5 (`v_determination_branches`), D-1 class c.
- **Proof.** B1 to B4; R5.
- **Open.** OR-2.

**Q5. Rest landings.**
- **Class.** GAP: parameters not minted; the relation is unread (RC-B, RC-E).
- **Resolved by.** D-1 (row 113's landing clause becomes a run-length or rise condition); D-8 (landing length observed and minted through the term route); T-7 and D-6 (the ramp page).
- **Proof.** `SELECT COUNT(*) FROM source_value_extractions WHERE parameter_id = 12` > 0 after D-1.

**Q6. Rails, surfaces, locations.**
- **Class.** GAP: no vocabulary, no element pointer (RC-E).
- **Resolved by.** D-8 (observe and mint handrail height, slip resistance and so on from the codes); T-7 and D-6 (the element pointer). A categorical quantity such as location has no direction; `compose_value` declines with its note, and state and marker still compute.
- **Proof.** `v_element_page` for TERM-089 lists the new parameters.

**Q7. Different access needs.**
- **Class.** GAP: routing (RC-C).
- **Resolved by.** T-3, D-2.
- **Proof.** C30 after T-3: the A-EFFORT cell is `pending` with a "finding only" gap. Its single row, 33, is a qualitative finding.
- **Open.** OR-1.

**Q8. Qualitative information, clauses, exceptions, conditionals.**
- **Class.** Qualitative claims are handled at the data layer: the text is reached by pointer through `v_determination_provenance`, which is rule 5 working. Clauses, exceptions and conditionals are Q4.
- **Resolved by.** T-5 prints governing qualitative `claim_text` verbatim; T-2 and D-1 handle the conditionals.
- **Proof.** R-tests.

**Q9. Are access needs, identities and ICF codes directed appropriately?**
- **Class.**
  - DEFECT: the attestation collides for multi-lens cells.
  - GAP: routing.
  - NOT A ROUTING DEFECT: the medical lens is empty, and RULINGS R16 orders it filled from persisted WHO payloads through `add-medical` (Phase 5 research). Its emptiness is owed research. It also explains 2 of the 3 UNWRITABLE columns (C04), the medical maps; the third is `connection_targets.con_id`.
- **Resolved by.** T-3.
- **Proof.** L1 to L3; C30.
- **Open.** OR-1, OR-1b.

**Q10 (coverage). Are jurisdictions, languages and academic bodies searched?**
- **Class.**
  - GAP: no stopping rule in the determination's unit; no index registry.
  - DEFECT: language labels in two cases; `v_coverage_priority` misses lower-case searches.
  - DESIGN: OR-8, OR-9 (RC-F).
- **Resolved by.** T-6.
- **Proof.** C13; T-6's tests.

**Q10 (stepping) and E13. Stepping values up and down.**
- **Class.** GAP.
- **Resolved by.** T-4 step 4 (the leave-one-out count, exact for a min/max selection); the ±N % perturbation lives only in tests, F-tests in section 6.
- **Proof.** M16.

**Q11 (aliases, search, retrieval).**
- **Class.** Retrieval is already handled, in bytes, language-agnostic. Aliases:
  - DEFECT in provenance (0 attested; C14);
  - GAP: no consumer;
  - DESIGN: OR-12.
- **Resolved by.** D-4 (22 candidates, C16, not the register's 33: only 22 non-English observations are adjudicated NAMES-EXISTING); T-6 step 3 (`terms_used` derived).
- **Do not.** Backfill `evidence_sources.language` (Appendix A, A-9).

**Q12. All slugs and parameters; a value-free generic list.**
- **Class.** DESIGN: OR-13. The value screen's two definition hits (`360°`, `RT60`) are **not** a defect to fix:
  - the screen on definitions exists only in `mint-term-from-catalogue`;
  - both terms already exist;
  - "screen, then you approve" is the owner's guard.
- **Resolved by.** D-8. Slug↔parameter is derived (T-6 step 5), never a column.
- **Proof.** New parameters carry `catalogue_approval_ref` or an observation.

**Q13 (trust).**
- **Class.**
  - PARTLY HANDLED: bytes persisted, verbatim, digits in the quote, author diff.
  - GAP: the readability of the value (T-1), comparators (T-1 step 5), what `verified` means (T-1 step 10, OR-11a), and scans unexercised (D-3) (RC-G).
- **Proof.** N1 to N8; C11 and C12 after D-3.

**Q13 (what to record).**
- **Class.** Handled by contract (the scan contract, R11, R7, R12); its exercise is a GAP (D-3).
- **Proof.** C12 shows READ-NOTHING-FOUND > 0.

**Q13 (models, effort).**
- **Class.** DESIGN (OR-18) plus measurement (D-5). The database stores no model or effort. The **preserved transcripts do**, on every assistant message (`"model"`, `"effort"`, `"output_tokens"`; C28), so a retrospective tabulation is possible but confounded.
- **Resolved by.** D-5.

**Q13 (citation mining).**
- **Class.** Already handled. `citation_mining_completeness.py` scopes to T1 and T2 by default and reports `VERDICT: CLEAN`, EXAMINED 13 (C27). The 30 `pending` T3 to T6 sources are not owed under R2.
- **Open.** OR-20.

**Q14. Throughlines.**
- **Class.** DOCUMENTATION. The six throughlines map onto RC-A to RC-H (Appendix B). The PR order follows the register's priority by consequence, with one change: reading (T-1) precedes conditions (T-2), because a condition cannot be composed from an unparsed bound.

**E0. The element-level assembly tension.**
- **Class.** DESIGN: OR-14.
- **Resolved by.** T-7 and D-6: a derived page, never a container.
- **Guard.** Section 7, K-3.

**E1. Applicability.**
- **Class.** GAP. `setting` is free text on 16 rows and read by nothing (C09).
- **Resolved by.** D-1 classes d and e (applicability to `setting`; alteration-only relaxations stay as qualifying rows that T-5 renders). A typed column waits until a vocabulary emerges from use. `schemas/enums.py` already holds unread `DesignStage` and `ProjectType` enums, a candidate vocabulary the owner may adopt.

**E2. Is a quantity defined the same way everywhere?**
- **Resolved by.** D-1 class b: the definition is checked before `ratio` → `rise:run ratio`. A slope-length ratio is a different unit and refuses to compose.

**E3. US customary lengths.**
- **Resolved by.** T-1 step 9 (OR-10).
- **Proof.** `('36','in','>=')` gives `(Fraction(4572,5), None)`.

**E4. When evidence says the code is inadequate.**
- **Resolved by.** T-5 (`v_code_inadequacy`). Five edges today (C07); all point at labels, so `repoint-extraction-relation` must aim them at code rows once those are extracted (D-1 or D-3).

**E5. Independent confirmation versus echo.**
- **Resolved by.** T-8 and D-7.
- **Open.** OR-19.

**E6. Where a contested direction's spread is stored.**
- **Class.** NOT-A-PROBLEM for storage: it is derived (`v_determination_provenance` by role; T-4's spread note).
- **Open.** Per-lens direction is OR-21, deferred to its trigger, C29.

**E7. Person Mode.**
- **Class.** NOT-A-PROBLEM by doctrine (ARCH §3: Person Mode resolves the individual's needs by OT co-design; the population range informs and does not bound).
- **Resolved by.** T-5 prints the `functional_basis` handoff.
- **Note.** `schemas.directness.SCALE_FROM_RECOMMENDATION` is read only by its own test (C37), which makes it a deletion candidate (CLAUDE.md §8).

**E8. Does Co-1's non-primacy for dimensional values hold mechanically?**
- **Class.** DEFECT against standing text. The premise is **true**: `references/methodology-evidence-hierarchy-mapping.md:151` (§6.4) states it, and ratified ARCH cites that document as its correspondence home (line 32). G4 shows the engine does not apply it, and §6.4's claim that value-directness expresses it is false.
- **Resolved by.** T-4 step 3.
- **Open.** OR-5.

**E9. A stopping rule.**
- **Resolved by.** T-6 steps 4 and 5 (OR-8). "Robust" for a parameter means:
  - every bucket-1/2 jurisdiction × its `lang_jur_map` language has a non-deferred search reaching the parameter (directly, or through an admission), or a deferred row saying why;
  - **and** `scan_debt.py` is 0 over that parameter's admitted sources.

**E10. A code re-issued after a determination.**
- **Class.** PARTLY HANDLED (`supersede-source` refuses under a live determination).
- **Resolved by.** T-5 prints "edition currency unverified" for each governing source at tier ≥ 4 whose `code_currency_status` is NULL. That is all 29 such sources today (C19).
- **Repair path.** Admit the new edition, then `supersede-source --by`, `retire-specification`, re-run, all existing verbs.

**E11. Would two blind agents extract the same rows?**
- **Resolved by.** D-5.
- **Open.** OR-15, OR-18.

**E12. What the owner reviews each day.**
- **Class.** DESIGN: OR-17.
- **The queue is derived.** Add this command to `/orient`'s text (no new apparatus):
```sql
SELECT 'open gates', COUNT(*) FROM v_open_determination_gates
UNION ALL SELECT 'open follow-ups', COUNT(*) FROM extraction_follow_ups
UNION ALL SELECT 'catalogue names awaiting approval', COUNT(*) FROM terms WHERE catalogue IS NOT NULL AND catalogue_approval_ref IS NULL
UNION ALL SELECT 'unadjudicated observations', COUNT(*) FROM observed_terms o WHERE NOT EXISTS (SELECT 1 FROM term_adjudications a WHERE a.observation_id = o.observation_id);
```

---
## 6. Verification matrix and the regression suite

### 6.1 Matrix

"Red today" was observed on 2026-10-22 unless marked `[NOT EXECUTED]`. Every count carries its command.

| question | proof | red today (observed) | green expected |
|---|---|---|---|
| Q0 | C34 replay and rebuild; C35 determinism; R1–R6; P-K | replay matches, determinism identical (already green); T6-only cell absent from `v_best_practice` (view SQL, C06); no renderer | R1–R6 pass; P-K PASS; `v_best_practice` holds the T6-only fixture |
| Q1 | G2, G8, G3 assertions (C32) | G2 reason "disqualified on tier…"; G8 `stated ●` with an "INCOHERENT INTERVAL" note; `convergence_assessment` all `pending_assessment` (C10) | G2 "outranked"; G8 refused without an approach, `divergent` with one; G3 spread in the note |
| Q2-assembly | N9, N10 | derived 99 against 14.51 accepted; XRI FAIL on the scratch copy (C26) | N9 refused, the row count unchanged |
| Q2-cross | C08; `v_determination_branches` | C08 = 1; no cross-parameter edge (C20) | C08 ≥ 2 after D-1; branch rows with `other_parameter_id ≠ parameter_id` |
| Q3 | N1–N8; C24; C21 | `1/12` → 0.0833, `12:1` → 1200, `8.33%` → None; 45 of 68 numerical rows unreadable (C21) | the writer refuses each; C21 lists only rows left deliberately |
| Q4 | B1–B4; R5 | B2 fixture gives `max 5.0` (the strictest step) `[NOT EXECUTED as B2; same arithmetic as C32's G9]` | B2 `None` with "piecewise only"; branches rendered |
| Q5 | `SELECT COUNT(*) FROM source_value_extractions WHERE parameter_id=12` | 0 | > 0 after D-1 |
| Q6 | `v_element_page` for TERM-089 | the view does not exist | lists parameters 3 and 12 (and D-8's) |
| Q7, Q9 | C30; L1–L5 | five lenses each `provisional ○ max 5.0` from 26 sources; MOB and MOB+d450 sha `62d6fa8e88c2` both (C30) | non-MOB cells `pending` with a lens-naming gap; the two shas differ |
| Q8 | R-tests (qualitative claim text printed) | no renderer | a stated cell with NULL value prints its governing claim sentences |
| Q10-coverage | C13; the C6 tests | 17 raw labels, 13 folded; 0 searches carry `parameter_id` (C13) | the view fold gives 13 = 13; a new `fr` is stored `FR` |
| Q10-stepping, E13 | M16; the F-tests below | no fragility note | the note "stated by n of m" |
| Q11 | `alias_provenance_audit.py` (C14); C16 | attested 0; 22 candidates | attested ≥ 1 after D-4; refusals listed |
| Q12 | D-8 rows carry `catalogue_approval_ref` or an observation | — | every new term traceable |
| Q13-trust | N6; T-1 step 10 test; C11 | `source_scans` 0; 31 `verified` rows rest on no scan | `verified` refused without a full scan |
| Q13-record | C12 | EXTRACTED 47 / STATED-ABSENT 5 / NOT-READ 468 (C12) | READ-NOTHING-FOUND > 0 after D-3 |
| Q13-models | D-5 report | no measure | an agreement table per model pair, each figure from the script |
| Q13-mining | C27 | already CLEAN, EXAMINED 13 | unchanged |
| E1 | `SELECT COUNT(*) FROM source_value_extractions WHERE setting IS NOT NULL` (C09) | 16 | rises by D-1 class d |
| E4 | `SELECT COUNT(*) FROM v_code_inadequacy` | the view does not exist; 5 edges (C07) | 5 or more, printed beside the floor |
| E5 | T-8 tests | `external_root_registry` 0 rows (C04 lists it empty) | `convergent` only with ≥ 2 roots |
| E8 | G4 | 1500 (Co-1 wins) | 1200 under OR-5 = yes |
| E10 | the renderer's currency line | `code_currency_status` NULL on 29 of 29 T4–T6 sources (C19) | "edition currency unverified" printed |
| E11 | D-5 | no measure | kappa and coverage computed |
| new: pending path claim | L5; C31 | `function_only` with "rests on the functional mapping alone" on 9 pending cells | `derivation_paths` NULL on pending cells |

**F-tests, perturbation in tests only (Q10-stepping).** Add `test_assess_cell_pilot.py` section F:
- For each G fixture, multiply every governing value by `Fraction(11,10)` and by `Fraction(9,10)` in turn, and flip each comparator between `>=` and `<=` one row at a time.
- Assert which cells change `state` and which change `value_min` or `value_max`, against expectations written beside each case.
- The ±10 % factor lives **only** in this test (rule 7a forbids it in a check or a column).

### 6.2 The regression suite: re-run the 2026-10-22 stress test end to end

**Where it ran.** I executed it on 2026-10-22 from `/tmp/claude-0/-home-user-guidebook/f366a537-569c-50d0-a2d1-f74dc994928a/scratchpad/report-probes/` (`regress_2026-10-22.sh`, `fixtures_g1_g13.py`, `notation_probe.py`, `render_attempt.py`). Its output is in that directory's `regress.out` and the results are quoted throughout this report. To re-run it elsewhere:
1. Save the three files below into a fresh directory outside the repository.
2. Copy `render_attempt.py` from the scratchpad path above, or omit stage 6.
3. Run `bash regress_2026-10-22.sh /home/user/guidebook "$TMPDIR/regress"`.

It never writes the repository: the canonical sha is printed before and after, and must match.

`[EXECUTED as printed]`: the three blocks below were extracted from this report into `report-probes/asprinted/` and run unchanged. The results matched the first run on every stage: the same seven lens shas, the same fixture lines (`diff` empty), 182 INSERTs, `differing: []`, and the canonical sha unchanged.

**Order it covers.**
1. The lens runs.
2. Every parameter on a populated copy.
3. The fixtures G1 to G13.
4. The notation probes.
5. Walkability on canonical and on the populated copy.
6. The render attempt.
7. The write-path replay, applied and rebuilt in a scratch clone made by `git archive` (a read-only git operation).

Each tooling PR re-runs it, before and after, and the PR body states the differences. The expected differences per PR are in section 3's acceptance criteria.

```bash
#!/bin/bash
# regress_2026-10-22.sh -- re-run the 2026-10-22 stress test on scratch copies. Never writes the repository.
# usage: regress_2026-10-22.sh <repo> <outdir>
set -u
REPO=${1:-/home/user/guidebook}; R=${2:?outdir}; HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$R"/cells "$R"/lens
SESSION=session_2026-10-22-regression; STAMP='2026-10-22 05:00:00'
echo "canonical sha256 before: $(sha256sum "$REPO/data/guidebook.db" | cut -c1-64)"
cp "$REPO/data/guidebook.db" "$R/lens.db"; cp "$REPO/data/guidebook.db" "$R/cells.db"
eng() { local db=$1 od=$2 label=$3 p=$4; shift 4
  (cd "$REPO" && GUIDEBOOK_DB_PATH=$db python3 scripts/assess/assess_cell.py --db "$db" --emit-sql "$od/$label.sql" \
     --parameter-id "$p" --slug stress-test "$@" --session $SESSION --stamp "$STAMP" --report-json "$od/$label.json" \
     > "$od/$label.log" 2>&1); echo "$label rc=$?"; }
echo "== 1. lens runs, parameter 3"
eng "$R/lens.db" "$R/lens" MOB 3 --identity MOB
eng "$R/lens.db" "$R/lens" MOB_d450 3 --identity MOB --icf d450
for L in AUT BLIND ADHD; do eng "$R/lens.db" "$R/lens" $L 3 --identity $L; done
eng "$R/lens.db" "$R/lens" d450 3 --icf d450
eng "$R/lens.db" "$R/lens" A-EFFORT 3 --needs A-EFFORT
python3 -I - "$R/lens" <<'PY'
import json, glob, sys, os
for f in sorted(glob.glob(sys.argv[1] + "/*.json")):
    r = json.load(open(f))[0]
    print(f"{os.path.basename(f)[:-5]:<10} state={r['state']:<11} marker={r['marker']} gov={len(r['governing_refs'])} "
          f"min={r['value_min']} max={r['value_max']} sha={r['derivation_sha'][:12]}")
PY
echo "== 2. every parameter under MOB (the populated scratch)"
for p in $(python3 -c "import sqlite3;print(' '.join(str(r[0]) for r in sqlite3.connect('file:$REPO/data/guidebook.db?mode=ro',uri=True).execute(\"select parameter_id from base_parameters where status='active' order by 1\")))"); do
  eng "$R/cells.db" "$R/cells" p${p}_MOB $p --identity MOB; done
python3 -I - "$R/cells.db" <<'PY'
import sqlite3, sys
c = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
for r in c.execute("select parameter_id, state, marker, derivation_paths, value_max, substr(value_note,1,90) "
                   "from specifications where retired_at is null order by 1"): print(r)
PY
echo "== 3. fixtures G1-G13";  python3 -I "$HERE/fixtures_g1_g13.py" "$REPO"
echo "== 4. notation probes";  python3 -I "$HERE/notation_probe.py" "$REPO"
echo "== 5. walkability"
(cd "$REPO" && python3 workplan/pipeline-state-graph/walkability.py data/guidebook.db > "$R/walk_canonical.txt" 2>&1
 python3 workplan/pipeline-state-graph/walkability.py "$R/cells.db" > "$R/walk_populated.txt" 2>&1)
grep -c "render *NO PATH" "$R/walk_canonical.txt" "$R/walk_populated.txt"
echo "== 6. render attempt"; [ -f "$HERE/render_attempt.py" ] && python3 -I "$HERE/render_attempt.py" "$R/cells.db" | head -30
echo "== 7. write path: capture, emit, apply, rebuild in a scratch clone"
rm -rf "$R/clone"; mkdir -p "$R/clone"
git -C "$REPO" archive HEAD CLAUDE.md requirements.txt data governance references schemas scripts | tar -x -C "$R/clone"
(cd "$R/clone" && GUIDEBOOK_DB_PATH="$R/cells.db" python3 scripts/research/emit_batch_sql.py --scratch "$R/cells.db" \
   --canonical data/guidebook.db --out "$R/batch.sql" 2>&1 | tail -2)
grep -oE '^INSERT INTO "?[a-z_]+' "$R/batch.sql" | sort | uniq -c
(cd "$R/clone" && python3 scripts/emit_data_migration.py --session $SESSION.md --summary "regression replay" \
   --input "$R/batch.sql" 2>&1 | tail -1 && python3 scripts/migrate_db.py --session $SESSION 2>&1 | tail -2)
(cd "$R/clone" && timeout 900 python3 scripts/migrate_db.py --rebuild "$R/rebuilt.db" 2>&1 | tail -1)
python3 -I - "$R/clone/data/guidebook.db" "$R/rebuilt.db" <<'PY'
import sqlite3, sys
a, b = (sqlite3.connect(f"file:{p}?mode=ro", uri=True) for p in sys.argv[1:3])
ts = [t for (t,) in a.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
d = [(t, a.execute(f'select count(*) from "{t}"').fetchone()[0], b.execute(f'select count(*) from "{t}"').fetchone()[0]) for t in ts]
print("EXAMINED tables:", len(d), "| differing:", [x for x in d if x[1] != x[2]])
PY
echo "canonical sha256 after:  $(sha256sum "$REPO/data/guidebook.db" | cut -c1-64)"
```

```python
# fixtures_g1_g13.py -- G1-G13 over the engine via the pilot test's synth_db (in memory). usage: python3 -I fixtures_g1_g13.py <repo>
import sys, json
REPO = sys.argv[1] if len(sys.argv) > 1 else "/home/user/guidebook"
for p in ("scripts/tests", "scripts/assess", "scripts", ""):
    sys.path.insert(0, f"{REPO}/{p}".rstrip("/"))
import test_assess_cell_pilot as t
from assess_cell import determine
def S(tier, et, val, cmp_=">=", unit="mm", ref=None, jur=None, **k):
    d = {"tier": tier, "evidence_type": et, "claimed_value": str(val), "claimed_unit": unit, "comparator": cmp_}
    if ref: d["ref_id"] = ref
    if jur: d["jurisdiction"] = jur
    d.update(k); return d
T1 = lambda v, **k: S(1, "clinical", v, **k);  T2 = lambda v, **k: S(2, "sr_meta", v, **k)
CO1 = lambda v, **k: S(1, "co1", v, co1_source_type="dpo_annual_survey", **k)
T3C = lambda v, **k: S(3, "clinical", v, scope="lower_control", **k)
T4 = lambda v, **k: S(4, "standard_eb", v, scope="international", **k);  T5 = lambda v, **k: S(5, "national_fw", v, **k)
T6 = lambda v, j, **k: S(6, "code", v, jur=j, **k)
def run(gid, srcs, direction="higher_is_better", extra=None):
    conn = t.synth_db(srcs, direction=direction)
    if extra: extra(conn)
    d = determine(conn, 1, {"identity_code": "MOB"}, "s", "n")
    ex = sorted({(l["ref_id"], (l["exclusion_reason"] or "")[:60]) for l in d["links"] if l["role"] == "excluded"})
    print(json.dumps({"id": gid, "state": d["state"], "marker": d["marker"], "basis": d["tier_basis"],
        "min": d["value_min"], "max": d["value_max"], "unit": d["value_unit"], "note": (d["value_note"] or "")[:70],
        "conv": (d["convergence"] or {}).get("status"), "governing": d["governing_refs"],
        "excluded": [e[0] for e in ex], "excl_reason_sample": ex[0][1] if ex else None}, ensure_ascii=False))
run("G1", [T1(1500, ref="R-T1"), T2(1200, ref="R-T2"), T3C(1000, ref="R-T3C"), T4(1100, ref="R-T4"), T5(1300, ref="R-T5"),
           T6(900, "US", ref="R-T6a"), T6(1000, "GB", ref="R-T6b"), T6(1100, "AU", ref="R-T6c")])
run("G2", [T1(900, ref="R-T1"), T6(1200, "US", ref="R-T6a"), T6(1200, "GB", ref="R-T6b"), T6(1200, "AU", ref="R-T6c")])
run("G3", [T1(900, ref="R-T1a"), T1(1500, ref="R-T1b")])
run("G4", [T1(1000, ref="R-T1"), CO1(1500, ref="R-CO1"), T2(1200, ref="R-T2")])
run("G5", [T3C(1500, ref="R-T3C"), T6(900, "US", ref="R-T6a"), T6(1000, "GB", ref="R-T6b"), T6(1100, "AU", ref="R-T6c")])
run("G6", [T4(1800, ref="R-T4"), T5(1300, ref="R-T5"), T6(900, "US", ref="R-T6a"), T6(1000, "GB", ref="R-T6b")])
run("G7", [T1(1000, ref="R-T1"), T2(40, unit="in", ref="R-T2")])
run("G8", [T1(1200, ref="R-T1"), T2(1000, cmp_="<=", ref="R-T2")])
run("G9", [T1(8, unit="%", cmp_="<=", ref="R-T1"), T2(5, unit="%", cmp_="<=", ref="R-T2"), T6(8.33, "US", unit="%", cmp_="<=", ref="R-T6a"),
           T6(8.33, "GB", unit="%", cmp_="<=", ref="R-T6b"), T6(6, "AU", unit="%", cmp_="<=", ref="R-T6c")], direction="lower_is_better")
run("G10", [T1(900, ref="R-T1a"), T1(1500, ref="R-T1b")], direction="contested")
run("G11", [T1(900, ref="R-T1")], extra=lambda c: c.execute(
    "insert into source_value_extractions (ref_id,slug,parameter_id,identity_code,claim_type,claimed_value,claimed_unit,"
    "figure_role,comparator) values ('R-T1','s',1,'MOB','numerical','1500','mm','claim','>=')"))
run("G12", [T1(1000, ref="R-T1"), CO1(1100, ref="R-CO1"), T2(1200, ref="R-T2"), T3C(1300, ref="R-T3C"), T4(1400, ref="R-T4"),
            T5(1500, ref="R-T5"), T6(1600, "US", ref="R-T6a"), T6(1700, "GB", ref="R-T6b"), T6(1800, "AU", ref="R-T6c")])
run("G13", [T1(1800, ref="R-T1"), CO1(1700, ref="R-CO1"), T2(1600, ref="R-T2"), T3C(1500, ref="R-T3C"), T4(1400, ref="R-T4"),
            T5(1300, ref="R-T5"), T6(1200, "US", ref="R-T6a"), T6(1100, "GB", ref="R-T6b"), T6(1000, "AU", ref="R-T6c")])
```

```python
# notation_probe.py -- the engine's reader on hand-picked inputs. usage: python3 -I notation_probe.py <repo>
import sys
REPO = sys.argv[1] if len(sys.argv) > 1 else "/home/user/guidebook"
for p in ("scripts/assess", "scripts", ""):
    sys.path.insert(0, f"{REPO}/{p}".rstrip("/"))
from assess_cell import bound_on_scale          # after T-1: from dbcore import bound_on_scale
for v, u, c, ct in [("1:12","rise:run ratio","<=","numerical"), ("8.33","%","<=","numerical"), ("8.33%","%","<=","numerical"),
        ("1 in 12","rise:run ratio","<=","numerical"), ("12:1","rise:run ratio","<=","numerical"),
        ("1/12","rise:run ratio","<=","numerical"), ("1:12","ratio","<=","numerical"), ("5","gradient","<=","numerical"),
        ("viisi prosenttia","%","<=","numerical"), ("0-4.8","%","between","range"),
        ("1:6 to 1:14","rise:run ratio","between","range"), ("5","degrees","<=","numerical"),
        ("36","in",">=","numerical"), ("900","mm",">=","numerical"), ("1200","mm",None,"numerical")]:
    b = bound_on_scale(v, u, c, ct)
    print(f"{v!r:>20} unit={u!r:<18} cmp={c!r:<10} -> {None if b is None else tuple(None if x is None else float(x) for x in b)}")
```

**Observed 2026-10-22, before any change `[EXECUTED]`.**

1. **Lens runs.** All seven parameter-3 cells were `provisional ○ gov=26 max=5.0`. MOB and MOB_d450 shared sha `62d6fa8e88c2`. AUT and BLIND were labelled `dual`; ADHD, d450 and A-EFFORT were `population_only`.
2. **Every parameter.** Parameter 3 gave `provisional ○` with the note "composed from 10 of 34 governing claims …". Parameters 4 to 12 were `pending` with `function_only`.
3. **Fixtures.** As in the matrix above.
4. **Notation probes.**
   - `1/12` gave 0.0833.
   - `12:1` gave 1200.
   - `8.33%`, `1 in 12`, `1:12`+`ratio`, `viisi prosenttia` and `0-4.8` gave None.
   - `5`+`gradient` gave `(None, 5.0)` on a scale of its own (not "unread", as the register said).
5. **Walkability.** 10 lines `render NO PATH` in each file.
6. **Render attempt.** `v_best_practice` 1, `v_pending` 9, `v_code_floor_only` 0.
7. **Write path.** 182 INSERTs in 6 tables, one data migration applied, and the rebuild had `EXAMINED tables: 56 | differing: []`. The canonical sha was the same before and after.

**Determinism (C35) `[EXECUTED]`.** Two fresh copies, the same cell and stamp: the emitted SQL was byte-identical (`26247c75ba1fc42a…` both).

**Fault injection along stage boundaries.** The register lists this as not completed. Beyond C26 (derived arithmetic) and C31 (the pending path claim) it remains `[NOT EXECUTED]`. The per-writer refusal matrix is what T-1 to T-3's tests build.

---
## 7. Risks, and what not to do

### 7.1 Tempting fixes that break a rule or bring the item layer back

| id | the tempting fix | why not | instead |
|---|---|---|---|
| K-1 | Route lenses through `identity_icf_map` or `access_need_icf` (the pass's Q9 design) | D-0184 measured that traversal "manufactures inference" (DEAF gives 20 items, AX-AUD gives 38); RULINGS R33 puts the crossing on the row at judgment; MOB's map would send ramp rows to the d530 (toileting) cell | T-3's lens predicate; D-2 tags with warrant |
| K-2 | Add `condition_text`, `branches_json`, `spread_json` or `selected_bound` columns | a second home for derivable facts (rule 5); `governing_refs` was writer-retired for exactly this | views (`v_determination_branches`) and the renderer's own recomputation through `dbcore.bound_on_scale` |
| K-3 | Seed parameters or element pages from the old Part 4 index, or name an element after an `[A-Z]-NN` item | the owner deleted the item layer because "if E-08 already exists then the work is predisposed to filing into a container that already exists, and that biases every finding" (CLAUDE.md §7; earliest record commit `befaa29e`); 2026-10-09: Part 4 names "NOT selected" | observed phrases or approved catalogues only (D-8); `relate-term` refuses value-bearing names and item codes |
| K-4 | A divergence tolerance, or a ±N % sensitivity, in a check or a column | rule 7a: a hard-coded number goes stale silently | set logic (T-4 step 2); perturbation in tests only (section 6, F-tests) |
| K-5 | Let the engine write a synthesis approach | judgment, at the Opus floor (contract `synthesis/opus-routing`) | refuse; take `--synthesis-approach-file` |
| K-6 | A value-directness grade for Co-1 | stop condition 4: "no value-directness grading rule exists … do not invent one" | §6.4's role rule (Co-1 is not composed into a dimensional bound), under OR-5 |
| K-7 | Fix the 45 unreadable rows with hand SQL inside a batch's migration | rules 3 and 10, and CLAUDE.md §4 "do not hand-write SQL against a table the CLI can reach" | `amend-extraction` (OR-3) or second rows, in D-1 after T-1 |
| K-8 | A parity check between `extraction_status='verified'` and `source_scans` | rule 5: "a parity check is not a fix" | the writer refuses (T-1 step 10) |
| K-9 | Backfill `evidence_sources.language` from `lang_detected` | a second home; `language` has no writer and is read only as a `COALESCE` fallback | leave it NULL-forward |
| K-10 | UPDATE the 21 lower-case `search_executions.language` rows | append-only history; no verb amends that column | fold in the views (T-6 step 2) |
| K-11 | Read the five relaxation `condition_on` edges as "this claim is conditioned" | they point from the relaxation to the general claim; reading them the other way removes the Japanese, Korean and Portuguese general claims from the headline | T-2 reads only edges **from** governing rows |
| K-12 | Narrow `_VALUE_BEARING` to names only (the pass's Q12 fix) | it weakens a guard for two terms that already exist | no change |
| K-13 | Commit a rendered page, or regenerate the instrument in two open PRs | CLAUDE.md §3 (render is read from the database when rendered); plan W4 (instrument regeneration conflicts) | render to `$TMPDIR`; regenerate `build_graph.py` output last, in one PR at a time |
| K-14 | `run_checks.py --all` to re-confirm | the expensive default (CLAUDE.md §7) | the gate named in P-6, once |

### 7.2 Order dependencies that break if sequenced wrongly

- **T-2 before T-1.** Conditions would be partitioned over bounds that do not parse; B-tests would pass on fixtures while the corpus composes nothing new.
- **T-3 and T-2 or T-4 bumping `RULE_VERSION` in parallel branches.** Two PRs would mint the same next label with different payload semantics. Land them in order. Derive the label from `main` at branch time (C36) and K01's closed set from the git history of that constant.
- **T-5 before T-2 to T-4.** The renderer would print today's defects with authority: `max 5 %` for a step table, the wheelchair answer under every lens, "disqualified" code floors.
- **D-1 before T-1.** Nothing stops a new prose unit while old ones are being cleaned.
- **D-2 before T-3.** Lens amendments would be refused (`_AMENDABLE_SVE_FIELDS`), and nothing reads the tags yet.
- **S-1 before D-1.** The first published determinations would be built on 10 of 34 claims.
- **Any data PR opened while a tooling PR touching `data/guidebook.db` is open.** The second to merge takes `main`'s blob and re-runs `python3 scripts/migrate_db.py` (the ledger's 2026-10-09 item 5).

### 7.3 Where a fix changes a ratified ruling (rule 0: record the supersession in the ledger first)

| fix | ruling it touches | where it lives |
|---|---|---|
| OR-3, reformatting in place | D-0168, "a wrong claimed_value … is a SECOND ROW" | `decisions/DR-2026-08-27-evidence-is-the-source-judgment-is-the-extraction.md`; `db.amend_extraction`'s first refusal |
| OR-6 "cap" branch only | evidence-methodology §3.3, "No fifth state. The cell is `stated`" | `governance/evidence-methodology.md:250-274` |
| OR-5 | `references/methodology-evidence-hierarchy-mapping.md` §6.4 (cited by ratified ARCH line 32); ARCH §2 line 41 (claim-type split) | both, in either branch |
| OR-2 | owner directive 2026-07-21 (most-accommodating selection), now applied to unconditioned claims only | `decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md` §5.2; ARCH line 122 |
| OR-10 | ledger "Owner ruling 2026-09-17 — PRESENT BOTH notations; never choose between ratio and percentage", ACTION (4) | `references/project-standards.md:3638` |
| OR-7 = no only | tier-system §8 line 98; ARCH line 121 (Option A, DR-2026-07-21) | both |
| OR-1 = no only | D-0184 (review pending) and RULINGS R33 | `decisions/DR-2026-09-01-the-lens-is-a-column-not-a-traversal.md` |
| OR-11b = no | the 2026-10-09 entry item 4 ("not settled (D1c)") | `references/project-standards.md:4401` |

### 7.4 The likeliest executor error in each PR, and its guard

| PR | likely error | guard (already written into the steps) |
|---|---|---|
| T-1 | breaking the machines.yaml needle in `derive_extraction`; refusing qualitative rows | keep the string; the N7 controls |
| T-2 | changing link roles, which turns K02 red | roles unchanged; C20 must print 0 |
| T-3 | crossing-map traversal; dropping other-lens rows from the junction; forgetting `synth_db` and `ENGINE_EXTRACTION_COLUMNS` | K-1; step 3; L-tests; M12 |
| T-4 | an engine-authored synthesis approach; a tolerance | K-4, K-5 |
| T-5 | reading `v_best_practice` as the source | R2 |
| D-1 | inferring a condition from another code's steps | verbatim gate; the session record lists each condition's quote |

---

## 8. What remains unknown, and the command that would settle it

| id | unknown | settle with |
|---|---|---|
| U-1 | Whether model or effort changes what is recorded | D-5's script; until then I don't know |
| U-2 | Whether the 31 `verified` rows would survive a full scan | after D-3: `SELECT x.extraction_id FROM source_value_extractions x WHERE x.extraction_status='verified' AND NOT EXISTS (SELECT 1 FROM v_scan_ledger l WHERE l.ref_id=x.ref_id AND l.parameter_id=x.parameter_id AND l.text_scope='full')` |
| U-3 | How many D-1 class-b rows measure rise over slope length (E2) | read each source at its locator: `python3 scripts/research/full_text.py --ref-id <REF-01005 / REF-01006 / REF-01008> --session "$STEM"`, then search for the definition of "ratio" |
| U-4 | Whether the function path should be parameter-specific. Today `identity_icf_map` is a population's whole profile, so AUT's ramp cell read `dual` from d230, d710–d729 and d910–d920 (C15) | owner or doctrine question (DR-2026-07-13 H2); no command settles it |
| U-5 | Whether T-5 fits the plan's 300-line target | `wc -l scripts/generate/render_cells.py` after T-5 |
| U-6 | The owner's verbatim words behind CLAUDE.md §7's item-layer quote | the earliest record found is commit `befaa29e`'s message, which paraphrases them; `git log --all --oneline -S'predisposed' -- scratchpad sessions references decisions` lists the later commits that quote it; the 2026-09-01 R-01 to R-05 scratchpad was not found by `grep -rl "R-01" scratchpad/` |
| U-7 | Whether walkability should count a view-only render as reached | owner or plan (WALKABILITY finding 1); `python3 workplan/pipeline-state-graph/walkability.py <db>` after any probe change |
| U-8 | Whether the per-writer fault-injection matrix finds more than C26 and C31 | build it as section 3's writer tests; the remainder is `[NOT EXECUTED]` |
| U-9 | Whether normative force (required, recommended, preferred) needs a typed column (D-1 class h) | count after D-1: `SELECT COUNT(*) FROM source_value_extractions WHERE notes LIKE '%recommended%' OR notes LIKE '%preferred%'`; then OR-2's follow-up |
| U-10 | Whether `connection_targets.con_id` (UNWRITABLE: its parent `connections` is empty) should be dropped under plan step 1.9 | C04; RULINGS R17's deferral governs `connections` |

---
## 9. Appendices

### Appendix A. Divergences from the reasoning pass, each with its evidence

**A. Where the pass was wrong, and the instruction changed.**

| # | the pass said | what is true | evidence |
|---|---|---|---|
| A-1 | Part C on E8: "no governance text says Co-1 is not co-primary for dimensional values"; E8 is a premise to put to the owner | The sentence exists in `references/methodology-evidence-hierarchy-mapping.md:151` (§6.4). **Standing:** the file is v2 (2026-07-12) and executes the owner directive of 2026-05-25 and DR-2026-05-29. Its header says it "Governs … the Co-1 co-primacy justification". Ratified ARCH (CANONICAL, 2026-07-13) names it at line 32 as the home of the GRADE/JBI/SIGN correspondence and at line 214 as where co-primacy is argued. It was swept as a prose caller in PR #201 (§7.1). §6.4 itself carries no separate ratification, and no live owner statement contradicts it. Its claim that the boundary "is now mechanically expressed … by value-directness" is false: value directness is `NOT_ASSESSED` on every source. So E8 is a defect against standing text, decided by OR-5 | the file; `grep -n "methodology-evidence-hierarchy-mapping" governance/evidence-architecture.md`; `assess_cell.assess_source` (`val = NOT_ASSESSED`); G4 in C32 |
| A-2 | Part C: `extraction_relations_integrity` reads `v_derived_figure_check`; the engine should exclude mismatched derived rows | The first half is true: check 3 reads the view, and the check is BLOCKING in the `db_integrity` battery. **The engine does not read the view at all.** It admits a `figure_role='derived'` row on its stored value: `gather_sources` filters `figure_role IN ('claim','derived')` and `compose_value` reads `claimed_value`. The real hole is that `add-extraction` accepts a mismatched derived row; only `derive-extraction` checks the arithmetic. So the fix is at the writer (T-1 step 7), not in the engine | `extraction_relations_integrity.py` lines 140–164; `check-registry.yaml` entry `level: blocking`; C26 `[EXECUTED]` |
| A-3 | Q2: "amend-extraction of the base row was ALLOWED … after changing the base value, `stale_determinations` returns []"; widen `live_determinations_linked` one hop | The experiment inserted all three rows, and later changed the base value, **by direct SQL on the scratch copy**. `claimed_value` is not amendable (`_AMENDABLE_SVE_FIELDS`). The only CLI amendment it tried was `comparator` on the base row, which does not move the derived value. The one-hop widening guards a route the CLI cannot take, so it is dropped | the command log `scratchpad/session_2026-10-21-step-3-specification-marker/commands.jsonl` (entries naming `xparam2`); `db.py` `_AMENDABLE_SVE_FIELDS` |
| A-4 | Q9, R3: an extraction reaches a cell through its own tag **or one hop through a crossing map** | That contradicts D-0184 ("traversal manufactures inference and changes the answer … render is `WHERE <lens>_code = ?`") and RULINGS R33 ("the crossing is judgment's output, written on the extraction's lens columns"). `identity_icf_map` holds a population's whole profile (MOB → d410 … d530), so one hop would put ramp rows into a toileting cell. Corrected to the lens predicate (T-3); OR-1 asks only for confirmation | `decisions/DR-2026-09-01-the-lens-is-a-column-not-a-traversal.md`; `RULINGS.md` R33; C15 |
| A-5 | Q1, R4: on divergence, cap at `provisional` (default) | Evidence-methodology §3.3 (status CANONICAL; doctrinal basis of ratified ARCH): "No fifth state. The cell is `stated` … convergence assessment records `divergent`". The pydantic model already requires `synthesis_approach` for `divergent`. Default changed to §3.3; the cap is the alternative, and it amends canonical text | `governance/evidence-methodology.md:250-274`; `schemas/evidence_state.py` `check_rationale_requirements` |
| A-6 | Q1: add `selected_bound` to `specification_extraction_links`; "`_written` is computed and dropped" | After T-1, the renderer can recompute which rows set the bound with `dbcore.bound_on_scale`, so a column would be a second home. `_written` is not dropped: it is the set of notation **units** used for the `stated` flag in `value_notations`, and it never held row ids | `compose_value` (`_written`, `notations`) |
| A-7 | Q12: apply `_VALUE_BEARING` to names only | The definition screen exists only in `mint-term-from-catalogue`. `turning circle` and `reverberation time` already exist and will not be re-minted. Narrowing a guard for no live case is rejected | `grep -n "_VALUE_BEARING" scripts/db.py` (5915 names; 7073 names and definitions) |
| A-8 | Q13 (mining): a small tooling PR so that "owed" is derived by tier | `citation_mining_completeness.py` already defaults to `--tier-max 2` and reports CLEAN, EXAMINED 13. No tooling is needed | C27 |
| A-9 | Q11: backfill `evidence_sources.language` from `lang_detected` | It would be a second home (rule 5). `language` has no writer (not in `amend-source`'s `_AMENDABLE`, no `add-source` flag) and is read only as `COALESCE(lang_detected, language)` | `db.py` unmined listing (`grep -n "COALESCE(es.lang_detected" scripts/db.py`); `_AMENDABLE` |
| A-10 | Q11: "promote the 33 non-English observations" | 33 is right, but only 22 are adjudicated `NAMES-EXISTING`: 4 are unadjudicated, 4 DEFERRED, 2 NAMES-NEW and 2 NOT-OURS. `add-alias` refuses any without such an adjudication | C16 |
| A-11 | Q4: "the gradient row carries a `condition_on` edge to that row"; the engine partitions on outgoing edges | That is right for 075's meaning, but **7 of the 10 live edges run the other way**, from condition rows (five gradient relaxations) to the general claim. No governing row has an outgoing edge today. T-2 reads only edges from governing rows; T-5's view renders both shapes | C20 |
| A-12 | Q13 (trust): make `verified` a refusal | It is defensible, but **nothing reads `extraction_status`** anywhere in `scripts/`, and the pass missed the owner's open D1c (may a `preliminary` figure set a value?). OR-11a and OR-11b are added; T-5 is named as the reader | `grep -rn "extraction_status" scripts --include=*.py`; ledger line 4401; `dbcore.py` comment above `NOT_PUBLISHABLE_METHODS` |
| A-13 | Q13 (models): "Effort is nowhere" | Every preserved assistant message carries `"model"` and `"effort"` (for example `"effort":"xhigh"`, `"model":"claude-sonnet-5-5"`), and `record-adversarial-pass` derives the models from transcripts. Before 2026-07-25 the session files also carried a `Model:` header | C28 |
| A-14 | Q0, E4, E6, E10: build `v_render_cell`, `v_determination_spread`, `v_code_currency_owed` and `v_code_inadequacy` | Only `v_code_inadequacy` and `v_determination_branches` are new. The spread is `v_determination_provenance` by role, the pending gap is `v_pending`, and currency is a column of `evidence_sources` | view list (C05 with no name) |
| A-15 | Q10: build `v_coverage_parameter` (direct and transitive) | The direct route exists as `v_coverage_lens`, grouped by `parameter_id`. Only the route through admissions is new | `SELECT sql FROM sqlite_master WHERE name='v_coverage_lens'` |
| A-16 | Q10: `log-search` refuses a language not in `lang_jur_map` | HR is searched but is not in `lang_jur_map`, so that rule would refuse a real search. Replaced with a two-letter shape check and an upper-case fold | C13; `SELECT DISTINCT language FROM lang_jur_map` |
| A-17 | E0: `term_relations` with five relation values, replacing the BROADER/NARROWER alias rows (216) | Those aliases name **phrases** (subtypes such as "curb ramp"), not relations between terms; they stay. The vocabulary is reduced to `quantity_of`, the one relation with a named reader | `SELECT alias, language FROM term_aliases WHERE alias_type IN ('BROADER','NARROWER') LIMIT 8` |
| A-18 | B.1 item 8: a CHECK on `claimed_unit` after the data cleanup | SQLite cannot add a column CHECK without rebuilding `source_value_extractions`, which has 51 columns and inbound foreign keys. Without it, a new spelling of a unit makes the engine decline with a visible "different units" note, not a wrong value. The burden of proof for new apparatus fails (CLAUDE.md §8); it is dropped | C09 (units); `compose_value`'s "different units" branch |
| A-19 | Q9: a functional basis for ICF and need cells "reads the ICF code itself; `dual` by construction" | That is a doctrinal change to H2 (DR-2026-07-13) and is not adopted; only the false wording changes (T-3 step 10). Left as U-4 | `derivation_handshake` |

**B. New findings the pass did not have.**

| # | finding | evidence |
|---|---|---|
| A-20 | Every pending cell under an identity with `identity_icf_map` rows is written `derivation_paths='function_only'`, with the rationale "the determination rests on the functional mapping alone". A pending cell has no determination. Fixed in T-3 step 9 | C31: parameters 4 to 12 under MOB on the populated scratch |
| A-21 | `parse_bound` is dead: no caller. Deleting it pays for part of T-1 | `grep -rn "parse_bound(" scripts` |
| A-22 | `schemas.directness.SCALE_FROM_RECOMMENDATION` is read only by its own test | C37 |
| A-23 | The `DesignStage` and `ProjectType` enums survive in `schemas/enums.py` with no reader in `scripts/`. They are a ready candidate vocabulary for E1, and otherwise a deletion candidate | `grep -rn "DesignStage\|ProjectType" scripts schemas` |
| A-24 | GAP-007's row reads OPEN although `_write_relation_edge`'s comment records it closed on 2026-09-18 | C38 |

**C. Items the pass marked unverified (B.5 and Part C), now settled.**

| item | result | command |
|---|---|---|
| distinct jurisdictions in `lang_jur_map` | 48 | C13 |
| UNWRITABLE columns | 3. Two are the medical maps (`identity_medical_map`, `icf_medical_map`); the third is `connection_targets.con_id → connections`. The register's "(medical lens chain)" is two-thirds right | C04 |
| governing claims entering the parameter-3 interval | 10 of 34, reproduced | C30 (stage 2 note) |
| fixtures G1 to G11 | reproduced exactly; G12 and G13 re-specified (the 2026-10-22 script did not keep them) and consistent: tier gates the stratum, and the value is tier-blind within the anchors | C32 |
| non-English observations | 33 of 88; 11 of 88 unadjudicated | C16 |
| `functional_axis` terms | 17 in the domain; 14 are named "…demand" (`Ambulant movement`, `Reach & manipulation` and `Wheeled movement & transfer` are not) | `SELECT canonical_en FROM terms WHERE domain='functional_axis'` |
| `code_currency_status` on T4–T6 sources | NULL on all 29 | C19 |
| model in `sessions/*.md` headers | 84 of 182 files mention a model; the dated `Model:` convention appears only up to 2026-07-25; no extraction-era session records one | C28 |
| the item-layer quote | earliest record found: commit `befaa29e` (2026-09-01 21:12), which paraphrases "in the owner's words" | U-6 |
| abstract-only `verified` rows | all 31 `verified` rows lack any scan (`source_scans` is empty); whether their artefacts are abstracts is U-2 | C11 |
| `DesignStage` and `ProjectType` | survive, unread | A-23 |
| "bare unit `gradient` → unread" (register) | `5` with unit `gradient` is read on a scale of its own; it only refuses to compose with `%` | C24 |
| PR #201 | merged 2026-10-22 03:10 UTC (GitHub API) | `gh pr view 201 --repo jordanelias/guidebook --json mergedAt` |

**D. Confirmed as the pass stated.**
- RC-A to RC-H, apart from the refinements in Appendix B.
- The exclusion-reason text.
- The sha over `lens_key`.
- `convergence_assessment` written only as `pending_assessment` or `single_axis`.
- Every live numerical claim carries a comparator (C23).
- `search_executions.parameter_id` exists and is NULL on all rows (C13).
- The `record-scan` full-PDF refusal (`db.record_scan`).
- `v_best_practice`'s predicate.

### Appendix B. The shared root causes, as verified

- **RC-A.** The unit and value columns carry notation, conditions and applicability.
  - `claimed_unit` has no CHECK and is not among `_SVE_VOCAB_COLUMNS`.
  - 27 of 33 distinct units fail a scale-only screen (C22).
  - 45 of 68 numerical or range rows are unreadable by the engine (C21).
  - Verified, with one refinement: a plain number with a non-family unit **is** read, on a scale named by the unit string, so a prose unit with a plain number would make the engine decline with "different units", not silently drop the row. Today no such row exists, which is why 10 of 34 compose.
- **RC-B.** Conditions are rows and edges, but nothing composes them and no branch is stored. Verified, with one refinement: most live edges encode relaxations in the reverse direction (A-11).
- **RC-C.** The lens is a label, not a route. Verified. The resolution is the lens column (A-4). Includes the pending-path defect (A-20).
- **RC-D.** Tier gates the stratum; value selection is tier-blind; agreement is never assessed. Verified. Two additions: the Co-1 role boundary (A-1), and canonical §3.3 for divergence (A-5).
- **RC-E.** No typed relation between parameters, or between an element and its parameters. Verified, with one refinement: BROADER/NARROWER are phrase aliases, not the missing relation (A-17).
- **RC-F.** Coverage is measured in slug units, its vocabulary is unverified, and nothing consumes it. Verified, with one refinement: `v_coverage_lens` already carries `parameter_id` (A-15), and `v_coverage_priority` misses lower-case searches.
- **RC-G.** Reading is self-declared and unexercised.
  - `source_scans` has 0 rows.
  - `extraction_status` is read by nothing.
  - Telemetry exists in transcripts but not in the database (A-12, A-13).
- **RC-H.** Render has no surface. Verified: the render stage maps only `weighting_profile` (5 rows), which no script reads (its one code mention is a string in `emit_data_migration.py`'s selftest). Step 1.1 has landed (`tools/` and the five renderers are gone).

### Appendix C. Command index (each once, in order of first use)

Run from `/home/user/guidebook`. The helper used below:
```bash
q() { python3 -c "import sqlite3,sys;c=sqlite3.connect('file:'+sys.argv[2]+'?mode=ro',uri=True);[print(r) for r in c.execute(sys.argv[1])]" "$1" "${2:-data/guidebook.db}"; }
```

| id | command | 2026-10-22 result (re-run; do not quote) |
|---|---|---|
| C01 | `sha256sum data/guidebook.db; q "PRAGMA user_version"` | `4b3cfb03…`, 116 |
| C02 | `ls scripts/migrations \| grep -E '^[0-9]{3}_' \| sort \| tail -1` | `116_specification_marker.sql`, so next is 117 |
| C03 | `git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations'` | (per PR) |
| C03b | `git diff --shortstat origin/main -- scripts schemas .github skills ':!scripts/migrations' ':!scripts/tests'` | (per PR) |
| C04 | CLAUDE.md §4's UNWRITABLE block, plus `print(sorted(empty))` | 13 empty tables; 3 UNWRITABLE |
| C05 | `q "SELECT type, name FROM sqlite_master WHERE sql LIKE '%<name>%'"` | (per name) |
| C06 | `q "SELECT sql FROM sqlite_master WHERE name='v_best_practice'"` | `… AND code_floor_only = 0 …` |
| C07 | `q "SELECT relation, to_extraction_id IS NOT NULL, COUNT(*) FROM extraction_relations GROUP BY 1,2"` | condition_on 10 (rows); insufficient 4, exceeds 1 (labels) |
| C08 | `q "SELECT COUNT(DISTINCT parameter_id) FROM source_value_extractions"` | 1 |
| C09 | `q "SELECT claimed_unit, COUNT(*) FROM source_value_extractions GROUP BY 1 ORDER BY 2 DESC"`; `q "SELECT root_type, COUNT(*) FROM source_value_extractions GROUP BY 1"`; `q "SELECT COUNT(*) FROM source_value_extractions WHERE setting IS NOT NULL AND trim(setting)<>''"` | 33 distinct units; root NULL 23, untraced 6; setting 16 |
| C10 | `q "SELECT COUNT(*), SUM(retired_at IS NULL) FROM specifications"`; `q "SELECT status, COUNT(*) FROM convergence_assessment GROUP BY 1"` | 8, 0; pending_assessment 5 |
| C11 | `q "SELECT COUNT(*) FROM source_scans"`; `q "SELECT COUNT(*) FROM source_value_extractions WHERE extraction_status='verified'"` | 0; 31 |
| C12 | `q "SELECT status, COUNT(*) FROM v_scan_ledger GROUP BY 1"` | EXTRACTED 47, NOT-READ 468, STATED-ABSENT 5 |
| C13 | `q "SELECT language, COUNT(*) FROM search_executions GROUP BY 1"`; `q "SELECT COUNT(DISTINCT UPPER(language)), SUM(parameter_id IS NOT NULL), COUNT(DISTINCT jurisdiction) FROM search_executions"`; `q "SELECT COUNT(DISTINCT jurisdiction) FROM lang_jur_map"` | 17 labels; 13 folded; 0; 24; 48 |
| C14 | `python3 scripts/audit/alias_provenance_audit.py \| tail -14` | 2,382 aliases; 15 verified; 0 attested; 1,163 model-generated; 880 grandfathered |
| C15 | `q "SELECT identity_code, icf_code FROM identity_icf_map WHERE identity_code IN ('MOB','AUT','BLIND','ADHD') ORDER BY 1"` | MOB: d410 … d530; AUT: d230, d710–d729, d910–d920; ADHD: none |
| C16 | `q "SELECT a.outcome, COUNT(*) FROM observed_terms o LEFT JOIN term_adjudications a ON a.observation_id=o.observation_id WHERE o.language<>'EN' GROUP BY 1"`; `q "SELECT COUNT(*) FROM observed_terms o WHERE NOT EXISTS (SELECT 1 FROM term_adjudications a WHERE a.observation_id=o.observation_id)"` | NAMES-EXISTING 22, unadjudicated 4 (of 33); 11 overall |
| C17 | `q "SELECT term_id, substr(reason,1,60) FROM parameter_declinations"` | TERM-089 "An element, not a quantity…" |
| C18 | `q "SELECT COUNT(*) FROM evidence_sources WHERE superseded_by_ref_id IS NULL"` | 52 |
| C19 | `q "SELECT tier, code_currency_status, COUNT(*) FROM evidence_sources WHERE tier>=4 GROUP BY 1,2"` | NULL on 2 + 7 + 20 |
| C20 | `q "SELECT r.from_extraction_id, a.figure_role, a.extraction_method, r.to_extraction_id, b.figure_role FROM extraction_relations r JOIN source_value_extractions a ON a.extraction_id=r.from_extraction_id JOIN source_value_extractions b ON b.extraction_id=r.to_extraction_id WHERE r.relation='condition_on'"`; `q "SELECT COUNT(*) FROM extraction_relations r JOIN source_value_extractions x ON x.extraction_id=r.from_extraction_id WHERE r.relation='condition_on' AND x.figure_role IN ('claim','derived') AND x.extraction_method <> 'skim'"` | 10 edges (7 from condition rows); 0 |
| C21 | `python3 -c "import sqlite3,sys;sys.path[:0]=['scripts/assess','scripts','.'];from assess_cell import bound_on_scale as b;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);r=c.execute(\"select claimed_value,claimed_unit,comparator,claim_type from source_value_extractions where claim_type in ('numerical','range')\").fetchall();print(len(r),sum(b(*x) is None for x in r))"` (after T-1: `from dbcore import bound_on_scale`) | 68, 45 |
| C22 | the unit-screen probe: T-1 step 4's three conditions applied to `SELECT claimed_unit, COUNT(*) … GROUP BY 1` | 27 of 33 distinct (33 of 101 rows) refused |
| C23 | `q "SELECT COUNT(*) FROM source_value_extractions WHERE figure_role='claim' AND claim_type='numerical' AND comparator IS NULL"` | 0 |
| C24 | `python3 -I notation_probe.py /home/user/guidebook` (section 6.2) | see 6.2 |
| C25 | G4 in C32 | 1500, Co-1 wins |
| C26 | the script below the table, on a scratch copy | ACCEPTED; `VERDICT: FAIL` (stored 99, recomputed 14.51) |
| C27 | `python3 scripts/audit/citation_mining_completeness.py \| tail -8` | EXAMINED 13, CLEAN |
| C28 | `for d in transcripts/*/; do echo $d $(grep -oh '"model":"[^"]*"' $d/main.jsonl \| sort \| uniq -c \| sort -rn \| head -1) $(grep -oh '"effort":"[a-z]*"' $d/main.jsonl \| sort \| uniq -c \| head -2); done`; `grep -h -i -E '^\s*[-*]?\s*\**model\**\s*[:\|]' sessions/*.md \| sort \| uniq -c` | model and effort on every assistant message |
| C29 | `q "SELECT COUNT(*) FROM base_parameters WHERE accessibility_direction='contested'"` | 0 |
| C30 | section 6.2, stage 1 | as reported in 6.2 |
| C31 | section 6.2, stage 2 (the `specifications` printout) | 9 pending cells with `function_only` |
| C32 | `python3 -I fixtures_g1_g13.py /home/user/guidebook` | as in 6.1 |
| C33 | section 6.2, stage 5 | 10 `render NO PATH` lines in each file |
| C34 | section 6.2, stage 7 | 182 INSERTs; `differing: []` |
| C35 | `T=$TMPDIR; for i in 1 2; do cp data/guidebook.db $T/d$i.db; GUIDEBOOK_DB_PATH=$T/d$i.db python3 scripts/assess/assess_cell.py --db $T/d$i.db --emit-sql $T/d$i.sql --parameter-id 3 --slug stress-test --identity MOB --session session_2026-10-22-regression --stamp '2026-10-22 05:00:00' >/dev/null; done; cmp $T/d1.sql $T/d2.sql && echo IDENTICAL` | IDENTICAL |
| C36 | `grep -n '^RULE_VERSION' scripts/assess/assess_cell.py` | `pilot-4` |
| C37 | `grep -rn "SCALE_FROM_RECOMMENDATION" --include=*.py scripts schemas` | `schemas/directness.py` and `scripts/tests/test_directness_2_2.py` only |
| C38 | `q "SELECT gap_id, status FROM gaps WHERE gap_id IN ('GAP-007','GAP-056')"` | both OPEN |

**C26, the derived-arithmetic probe.** It runs on a copy, never on the canonical file:
```bash
T="$TMPDIR/derived_probe.db"; cp data/guidebook.db "$T"
GUIDEBOOK_DB_PATH="$T" python3 - <<'EOF'
import os, sqlite3, sys; sys.path.insert(0, "scripts"); import db
from dbcore import Refusal
c = sqlite3.connect(f"file:{os.environ['GUIDEBOOK_DB_PATH']}?mode=ro", uri=True)
(b_id, b_q), (d_id, d_q) = c.execute("SELECT extraction_id, claim_text FROM source_value_extractions "
                                     "WHERE ref_id='REF-01001' AND claimed_unit='%' ORDER BY 1").fetchall()[:2]
data = dict(ref_id="REF-01001", parameter_id=3, identity_code="MOB", claim_type="numerical", claimed_value="99",
            claimed_unit="%", claim_text="derived probe", figure_role="derived", comparator=">",
            extraction_method="full-read", extraction_status="preliminary")
rels = [{"relation": "derived_from", "to_extraction": b_id, "stated": "named", "quote": b_q, "input_role": "base"},
        {"relation": "derived_from", "to_extraction": d_id, "stated": "named", "quote": d_q, "input_role": "delta"}]
try:
    print("ACCEPTED", db.insert_extraction(data, session="session_2026-10-22-probe", relations=rels,
                                           verbatim_exempt="probe: computation statement")["extraction_id"])
except Refusal as e:
    print("REFUSED", str(e)[:200])
EOF
GUIDEBOOK_DB_PATH="$T" python3 scripts/audit/extraction_relations_integrity.py | tail -3
```

### Appendix D. Estimated size of each PR, in physical lines

**These are estimates.** They come from the measured size of the code each PR moves or deletes (`awk` or `grep -n` line spans), and from the shape of recent comparable PRs. PR #201's non-test code was +458/−216, per its own description. Measure the real figure with C03 and C03b.

| PR | moved or deleted (measured) | added non-test (estimate) | tests (estimate) | net non-test (estimate) | migration lines (excluded from the rule) |
|---|---|---|---|---|---|
| T-1 | notation block 126 lines moved (from the `NOTATIONS OF ONE QUANTITY` comment to `def parse_bound`; `grep -n "NOTATIONS OF ONE QUANTITY\|^def parse_bound" scripts/assess/assess_cell.py`); `parse_bound` −52; `derive_extraction` duplicate check about −11 | +110 to +160 (two screens, wiring, gloss, derived check, step 8 at ~+30, step 9 at ~+25, step 10 at ~+15) | +150 to +220 | +45 to +95 | 0 |
| T-2 | — | +35 to +50 | +80 to +110 | +35 to +50 | 0 |
| T-3 | COALESCE lens payload (a few lines) | +60 to +90 | +90 to +130 | +55 to +85 | 0 |
| T-4 | the single exclusion sentence (~4) | +90 to +130 | +100 to +150 | +85 to +125 | 0 |
| T-5 | — | renderer ≤ 300 (plan target, unverified) + 1 P-K line + 9 registry lines | +100 to +150 | +250 to +310 | ~50 |
| T-6 | — | +50 to +80 | +50 to +80 | +50 to +80 | ~60 to 90 |
| T-7 | — | +70 to +100 (verb, render flag) | +60 to +90 | +70 to +100 | ~30 |
| T-8 | — | +60 to +90 | +50 to +80 | +60 to +90 | ~25 (`v_value_independence_rows` and the redefined aggregate) |

Every tooling PR here except a pure deletion raises the total, so each carries the exception text given in its section. The deletions named in Appendix A (`parse_bound`, possibly `SCALE_FROM_RECOMMENDATION` and the unread enums) are the offsets on offer. Data PRs add migration lines, session records and attestations, and no code.

---

## If you only do three things

(1) Answer OR-1 now, one word confirming D-0184 for the engine, and land T-3 as soon as T-1 and T-2 are in. It stops the guidebook giving autistic, blind and ADHD readers the wheelchair answer under their own name. (2) Land T-1 and T-2, and answer OR-2 and OR-3 so that D-1 can run. Until then, 24 of 34 ramp claims say nothing (re-run C30, stage 2) and a code's step table prints as one number. (3) Do not build the renderer (T-5) before T-2 to T-4 are in. A page would publish these defects with authority, which is worse than having no page.
