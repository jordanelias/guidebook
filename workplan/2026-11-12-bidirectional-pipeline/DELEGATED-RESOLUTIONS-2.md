# Delegated resolutions, second pass: the open register decisions OD-40 to OD-55

_Written 2026-11-13 23:31 (UTC) by an Opus-class model, read-only except for this file and `OWNER-SHEET-PLAIN.md` beside it. **Nothing here is the owner's words, and nothing here is in the ledger yet.** No ledger entry, plan, task file, `DECISION-CLOSURE.md`, Edmonton scratchpad file or database row was changed. Every figure is given with the command that produces it: re-run it, do not trust a number written here. Canadian English._

`sha256sum data/guidebook.db` during this pass: `3c575c89c1a6af4b9d2192e9eb43ed78bfeb366d7b31fe5fe41715c731634cdb` (HEAD `8b4c4e8b`). It did not move.

**One side effect, undone.** The generator the brief names (`python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_batches.py`) rewrites `REMEDIATION-PLAN.md` on every run (its docstring: "Reads only; writes REMEDIATION-PLAN.md"). Run once as given, it changed only the plan's "Generated … at commit …" line; that file was restored with `git checkout -- workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-PLAN.md`, and every later run used a copy whose `OUT` points into the session scratchpad (`sed -e 's#^OUT = W / "REMEDIATION-PLAN.md"#OUT = Path("<scratchpad>/od2/REMEDIATION-PLAN.generated.md")#'`). Its output is the source of every "holds" line below.

## The owner's words that started this pass

Quoted verbatim, as relayed to this pass in the session's brief (2026-11-13):

> "are you sure you can't resolve these owner decisions using Opus based upon prior rulings, mission/doctrine and project goal?"

> "I don't know the machinery or code"

[ASSUMPTION: read as asking that the standing delegation of 2026-11-12 ("I guess opus can do it", `grep -n -F "I guess opus can do it" references/project-standards.md`) be applied to the open decisions OD-40 to OD-55, which are questions about machinery the owner cannot judge. The first sentence is a question, not a ruling, so the delegation's limits stand: nothing in a DG-NON category is resolved here (`governance/decision-protocol.md` §2.4), condition (e) holds (a resolution never overrides a standing owner ruling), and condition (d) is applied to every resolution: each is checked by a second, independent Opus-class instance before anything relies on it. Unratified.]

**How each decision was judged.** First, its category under `governance/decision-protocol.md` §1.1 and its delegation under §2.2 to §2.4. A decision in an always-DG-NON type (§2.4) is referred back. Second, whether any standing owner ruling decides it or forbids an option (condition (e)); an option that overrides one is not available. Third, the owner's three criteria in the order the owner ratified on 2026-11-13 (OI-14, `grep -n -F "OI-14 STATUS" references/project-standards.md`): C1 integrity (accuracy, academic rigour, provenance), then C2 legibility, then C3 coverage across lenses, ethical approaches and design modes. Below, "PS:n" is a line of `references/project-standards.md` at HEAD `8b4c4e8b`; re-find each by its quoted phrase.

**The gate today** (`for n in $(seq 40 55); do grep -c -F "OD-$n STATUS:" references/project-standards.md; done` printed sixteen zeros): no decision of this range has a status line, so every one reads CLOSED. The generator's state line (`python3 -I <copy of build_batches.py> | sed -n 2p`) printed: `blocking ['OD-40', 'OD-41', 'OD-42', 'OD-43', 'OD-44', 'OD-45', 'OD-46', 'OD-48', 'OD-49'] standing ['OD-17', 'OD-47', 'OD-50', 'OD-51', 'OD-52', 'OD-53', 'OD-54', 'OD-55']`.

---

## 0. Verdict

Resolved under delegation (each `CHECK: pending` until the independent check of condition (d) is recorded):

- **OD-40** RESOLVED: a derived figure has no quote or locator of its own; both are its inputs', reached through its two `derived_from` edges.
- **OD-41** RESOLVED: `ratio` to `rise:run ratio` is a reformat. The owner already named this very case as a reformat in the prompt OR-3 answered.
- **OD-42** RESOLVED: a figure moved between metric units is shown exactly; the 5 mm rounding of OR-10 and OD-22 is for conversions between inch-foot and metric units.
- **OD-43** RESOLVED: `convergent` only when the Tier 1 to 3 clinical axis and the Co-1 axis both govern, state the same bound, can all hold, and rest on two or more independent roots; otherwise `pending_assessment`.
- **OD-45** RESOLVED: a request that never returned a result list is a search not run, recorded with `deferred_reason` and owed a re-run.
- **OD-49** RESOLVED: (a1) building type, new or existing work and interior or exterior are typed circumstances on the figure, shown as branches, the building type pointing at the first of the three ruled levels; (b2) the 2026-08-27 "three tables" ruling stands, and an element row points at its term and holds no name of its own.
- **OD-50** RESOLVED: any admitted source may add a parameter in its data pull request, under the existing minting conditions.
- **OD-53** RESOLVED: any research batch may decline a held term that its own adjudications name, one stated reason per term, element or method only; T-072 item 6 reviews these declinations and may revoke them.
- **OD-55** RESOLVED: not reached while OD-41 stands as a reformat; if OD-41 is ever reversed, the stored row is retired in place, naming its successor.

Referred back to the owner (plain-language sheet: `OWNER-SHEET-PLAIN.md`):

- **OD-44** REFERRED BACK: the owner's own answer (OR-15) rests on a false premise. Every option either departs from what the owner chose or drops the reason the prompt gave for choosing it, and the prompt marked the choice as the owner's.
- **OD-46** REFERRED BACK: whether jurisdictions are included or excluded is DG-NON (§2.4 item 4). A recorded ruling also says that admitting a map-only code "is a scope decision". Unsure; see §1.
- **OD-47** REFERRED BACK: population taxonomy, including proxy decisions, is DG-NON (§2.4 item 2). Taking the lens from the parameter's function is a proxy decision.
- **OD-48** REFERRED BACK: Design Modes are mission doctrine, and two owner records conflict: DR-2026-07-12 item G1(a), ratified 2026-07-13, and the OD-31 option of 2026-11-12, whose prompt carried a false premise. Unsure; see §1.
- **OD-51** REFERRED BACK: evidence-tier definitions and the Co-1 corpus are DG-NON (§2.4 items 3 and 6).
- **OD-52** REFERRED BACK: every option either applies the owner's approved definition of a catalogue term or widens it, and catalogue terms are approved by the owner.
- **OD-54** REFERRED BACK: option (b) sets aside `CLAUDE.md` rules 3 and 10, which only the owner can do.

**Where this pass departs from the register as written.** OD-41's register entry says the question is open; the owner's OR-3 prompt already lists it. OD-42's entry says an inch conversion is inexact, which is false. OD-43's options (a) and (b) would allow `convergent` on a clinical and Co-2 cell that the ratified definition excludes. OD-48 is not the plain doctrine question its entry presents: the owner's OD-31 option was chosen on a premise the engine contradicts. OD-50's entry reads OR-13 as a restriction, which it is not. Section 4 lists each.

**Decisions where the DG-NON line was close.** OD-46 (referred; reasons in §1). OD-48 (referred; reasons in §1). OD-49 (resolved; the "jurisdiction and scope vocabulary" the register names is not the jurisdiction-inclusion type of §2.4, and the only option no ruling forbids is (a1)). OD-53 (resolved; not a §2.4 type, and the gate it concerns was designed for the batch to dispose).

---

## 1. Per decision

### OD-40 — What a derived figure carries as its quote and its locator

**Category.** D-SCHEMA (primary effect: what one kind of row stores), with a D-METH flow-through (the verbatim floor). Default DG-REVIEW: "Schema choices that satisfy already-canonical methodology are delegable" (§2.2). Not a §2.4 type.

**Resolution.** (a) `OD-40: a derived figure has no quote or locator of its own; both are its inputs'`. A derived row stores no `claim_text` and no locator; its words and its place are its two inputs', reached through its two `derived_from` edges, each of which already carries its input's verified quote. The writer refuses a derived row whose inputs lack a quote or a locator, and still checks the arithmetic (`_refuse_derived_mismatch`). A derived row that a source does state in words may carry that quote, checked like any other.

**What decided it.**
- *Standing rulings.* The owner's 2026-08-24 rule-5 ruling, "It is better to have a table cell point to another table cell than to rewrite" (`grep -n -F 'point to another table cell' CLAUDE.md`), names (a). The owner's ruling of 2026-09-13, "Derived figures are a weighted average of their figures" (PS:3178), presupposes derived rows and takes a derived figure's standing from its inputs. Option (c), which deletes derived rows, would contradict it, so (c) is unavailable (condition (e)). OR-14 (PS:4679) expects the specifications pass to be "adjudicating, deriving and synthesizing across rows". The register's "no ruling settles it" is true of the quote only.
- *C1.* Under (a) every stored quote is a source's own bytes, so the verbatim floor (`CLAUDE.md` §5 (c)) has no exemption. Under (b), `claim_text`, a column that everywhere else means "the source's words", would hold an analyst's sentence that no source wrote, exempt from the saved-bytes check. That is the shape of the fabricated-citation failure §5 (c) records, and OR-17 (PS:4713) forbids presenting a model's wording as a source's. Provenance under (a) is a pointer, which is stronger than a copy.
- *C2.* A reader sees the two source sentences the figure was computed from, not a sentence of ours. *C3.* Neutral.

**Facts checked.**
- `grep -n -F 'never read off the source' scripts/migrations/075_extraction_relations.sql` printed `66:--   derived    -- computed from other rows this project holds, never read off the source`.
- `grep -n -F 'KNOWN DEFECT, recorded by T' scripts/db.py` printed `10511:` (the three blockers: no locator, no comparator, the analyst's sentence refused by the verbatim check).
- `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select count(*) from source_value_extractions where figure_role='derived'\").fetchone())"` printed `(0,)`.
- `PRAGMA table_info(source_value_extractions)` shows `claim_text`, `source_section` with `notnull` 0. Under (a) no schema change is needed.
- `grep -n -i "derived" scripts/assess/assess_cell.py`: the engine reads `figure_role IN ('claim','derived')` as governing (lines 319 to 345). A derived row is therefore read, so (c) would remove something the engine uses.
- `git grep -n -i -E "derived (figure|row).{0,60}(quote|claim_text|verbatim)" -- references/project-standards.md decisions` printed nothing (the register's search, repeated).

**Reversal condition.** A derived figure must be shown to a reader with a sentence of its own that no input supplies, or the owner wants computed figures kept only in prose.

**Tasks.** Holds: T-063 (generator: `OD-40 | CLOSED (no status line) | T-063 | — | 1`). It opens T-063 only when (1) the check line reads `confirmed` or `confirmed with corrections applied`, and (2) T-063's section 2 names OD-40 in a "Delegated resolutions this task rests on" bullet with the gate loop (`for n in OD-40; do gate $n; done`) instead of in its "Owner decisions" bullet. The generator counts a decision in the "Owner decisions" bullet as needing the owner's words (`build_batches.py` lines 90 to 101 and `closed()`).

**Plan changes (described, not made).** T-063 §2: move OD-40 to a "Delegated resolutions" bullet citing this entry; §4 item 3: build the "(a)" branch only and delete the "(b)" sub-bullet and the "(c)" paragraph. `REMEDIATION-WORKPLAN.md` §8 OD-40: status line "RESOLVED UNDER DELEGATION (2026-11-13), check pending". `DECISION-CLOSURE.md` §4 prompt 2: remove it, or mark it resolved under delegation with the ledger pointer.

### OD-41 — `ratio` to `rise:run ratio`: a reformat or a new reading?

**Category.** D-METH, the application of an owner ruling (OR-3) that narrows D-0168. DG-REVIEW. Under condition (c) this is a reading of the owner's words, but here the owner's own prompt settles it.

**Resolution.** (a) `OD-41: ratio to rise:run ratio is a reformat`. The rows are amended in place under OR-3: same digits, same quote, the old unit kept in `notes`. T-061 gains the one branch it names: a new unit that is a member of `dbcore.NOTATION_FAMILIES` is accepted when the old unit stands, on word boundaries, in the new one and the stored figure reads under it. T-093 builds that branch, and T-086 applies it.

**What decided it.**
- *The owner's answered prompt.* OR-3 asked "May a figure's value, unit and empty setting be reformatted in place, keeping the same digits and quote and recording the old text in notes?", and its context listed, among the awkward forms to be reformatted, "**a unit written 'ratio' where it is 'rise:run ratio'**" (`grep -n 'id: OR-3$' -A8 governance/owner-browser.yaml`, line 219). The owner answered "Yes, reformat in place" (PS:4618). Calling it a new reading would set aside the owner's answer to the case the owner was shown (condition (e)).
- *C1.* Options (a) and (b) assert the same reading (a horizontal run). They differ only in whether a second row repeats the first, and a second row is a dual home (rule 5) that the engine must then avoid counting twice. OR-3 keeps the old text in `notes`, so provenance is kept.
- *C2.* One figure, one row. *C3.* Neutral.

**Facts checked.**
- `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select group_concat(extraction_id) from source_value_extractions where claimed_unit='ratio'\").fetchone())"` printed `('52,53,54,57,58,60,61,62,64,65,66',)`. Their quotes write the figure as a slope or gradient `1:n` ("a 1:20 slope", "gradient of or less than 1:12", "Table 20 Ramp Gradient Recommendations").
- `grep -n -F 'Reformatting a figure' references/project-standards.md` printed PS:4632: "with the same digits and quote and the old text kept in notes, narrows D-0168's … for reformatting only".
- `grep -n -E 'Not built here' workplan/2026-11-12-bidirectional-pipeline/tasks/T-061-amend-extraction-reformat.md` printed line 154, the held branch, which says the question "is the owner's reading of OR-3". The OR-3 prompt above answers it.

**Reversal condition.** The owner says the OR-3 example did not mean the bare-`ratio` rows, or a row's source defines its ratio otherwise (rise over sloped length). Such a row is then a new reading.

**Tasks.** Holds: T-086 and T-093 (generator: `OD-41 | … | T-086, T-093 | — | 2, 3`). It opens both on a confirmed check and on moving OD-41 to their "Delegated resolutions" bullets. Under this answer OD-55 holds nothing.

**Plan changes.** T-093 §2 and T-086 §2: move OD-41 to the delegated bullet. T-086 §4 item 2 (second rows): delete it; the rows are amended in place. Remove T-086's bullet on OD-55. T-061 §4 "Not built here": point at T-093 as built. `REMEDIATION-WORKPLAN.md` §5 batch 1 line ("T-093 … built only under its answer (a)"): built. `DECISION-CLOSURE.md` §4 prompts 3 and 17: remove or mark them.

### OD-42 — A figure moved between metric units: rounded, or shown exactly?

**Category.** D-PRES (how a figure reaches the reader), with D-METH flow-through. DG-REVIEW. It applies the owner's OR-10 and the delegated OD-22.

**Resolution.** (b) `OD-42: a metric-to-metric conversion is shown exactly`. A change of metric prefix (cm to mm, m to mm) keeps the source's digits and moves only the decimal point, so the shown figure is exact: 122.2 cm is shown beside 1222 mm. The quarter-inch or 5 mm rounding (OR-10), on the safe side (OD-22), applies to a conversion between inch-foot units and metric units.

**What decided it.**
- *Standing rulings.* OR-10 answered a question about "exact length units (inches and feet to millimetres and metres)" (`grep -n 'id: OR-10' -A6 governance/owner-browser.yaml`). Its rounding, "Round to nearest 1/4" or 5mm" (PS:4667), answers that question. Not rounding a metric prefix change does not override it. The 2026-10-29 entry keeps OR-10's ACTION (3): never round a derived figure into the position of a stated figure (PS:4693).
- *C1.* Rounding 1222 mm to 1225 mm prints digits no source stated, for a quantity whose exact digits are in hand. Across inch and metric units a shown figure is a translation between systems, which the owner chose to round. Within metric it is the source's own number.
- *C2.* 1222 mm is already a whole millimetre, so rounding gains nothing in legibility. *C3.* An exact minimum is never below the source's minimum, so no protected user is harmed.

**Facts checked.**
- `grep -n -F 'nearest quarter inch or 5 mm' workplan/2026-11-12-bidirectional-pipeline/tasks/T-030-units-as-data.md` printed lines 24 and 63 (OD-22's display rule).
- `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select claimed_unit, count(*) from source_value_extractions where figure_role in ('claim','derived') and claimed_unit in ('cm','m','mm','in','ft','inches','feet') group by 1\").fetchall())"` printed `[('cm', 3), ('m', 33), ('mm', 32)]`. No inch or foot figure is held today.
- Parameter 12's claims are stated in cm, m and mm (`select claimed_unit, group_concat(claimed_value,' | ') from source_value_extractions where parameter_id=12 and figure_role='claim' group by 1`).

**Reversal condition.** The owner says OR-10's rounding covers every shown converted length, metric prefix changes included.

**Tasks.** Holds: T-030, and through it T-033 and T-110 (generator: `OD-42 | … | T-030 | T-033, T-110 | 3`). It opens T-030 on a confirmed check and on moving OD-42 to T-030's existing "Delegated resolutions" bullet (line 24 already names OD-22 and OD-24).

**Plan changes.** T-030 §2 line 23: move OD-42 into the line-24 bullet. §4 item 1: the converter distinguishes a metric prefix change (shown exactly) from an inch-foot and metric conversion (rounded to the safe side). `DECISION-CLOSURE.md` §4 prompt 4: remove it, and correct its premise (§4 below).

### OD-43 — When may the engine call a cell `convergent`?

**Category.** D-METH. "Convergence assessment rules" is the category's named example (§1.1). New methodology is DG-NON; the application of existing methodology is DG-REVIEW (§2.2). A ratified definition exists, so this is an application.

**Resolution.** (b), made exact against the ratified definition: `OD-43: convergent only when the clinical (Tier 1 to 3) and Co-1 axes both govern, state the same bound on the parameter's scale, can all hold, and rest on two or more independent roots`. Otherwise the cell is `pending_assessment` with two or more axes, or `single_axis` with one. A cell whose axes are clinical and Co-2 only is never `convergent`. The engine computes the status; the validator checks the same root condition.

**What decided it.**
- *Standing records.* `governance/evidence-methodology.md` defines `convergent` as "Tier 1–3 clinical evidence and Co-1 evidence agree on the parameter value or range" (line 245), and the page renders it as "Tier 1 OT evidence ([sources]) and Co-1 sources ([sources]) converge on [claim]" (line 284). H1 counts roots, not documents (`governance/evidence-architecture.md` §4.5). The owner's OR-6b ("No, the spread is printed in the note", PS:4661) makes differing floors that can all be met *not divergent*. It does not make them *agree on the value*, so they stay `pending_assessment`, with the spread in the note. The owner ruled the determination computed (2026-09-09 evening, PS:2684), which (c) would partly undo for this status.
- *C1.* The book tells a reader the evidence agrees only when it does. Option (a) would print "converge" over 900 and 1500 because both can be met. Options (a) and (b) as registered count "two or more axes", which the engine reads as any two of clinical, Co-1 and Co-2 (`assess_cell.py` lines 1296 to 1299). That would print a Co-1-C sentence naming Co-1 sources for a cell that has none.
- *C2.* The sentence a reader sees is true word for word. *C3.* Holding Co-1 as a named half of convergence keeps lived-experience evidence co-primary (mission, commitment 3).

**Facts checked.**
- `grep -n -F 'exists for grading agreement between extracted values' scripts/assess/assess_cell.py` printed `1337:`; the engine writes `pending_assessment` for two or more axes.
- `grep -n -F 'agree on the parameter value or range' governance/evidence-methodology.md` printed `245:`; `grep -n -F '| \`convergent\` | Co-1-C |' governance/evidence-methodology.md` printed `284:`.
- `grep -n -F "status 'convergent' requires" scripts/validate_evidence_state.py` printed `371:` (axes only).
- `grep -n -i -E 'axes_clinical|axes_co1|axes_co2|n_axes =' scripts/assess/assess_cell.py` shows the three axes and their count.

**Reversal condition.** The owner wants agreement within a stated tolerance to count, or a cell with two clinical roots and no Co-1 evidence to count as convergent. The latter would need the definition rewritten, which is the owner's.

**Tasks.** Holds: T-068 (generator: `OD-43 | … | T-068 | — | 2`). It opens on a confirmed check and on moving OD-43 to a delegated bullet. T-068 §2 says "until a ledger line in the owner's words answers it, do not start", so that sentence must change too.

**Plan changes.** T-068 §4 item 3: build "(b)", and add the condition that the governing figures include the engine's clinical axis and its Co-1 axis. Item 2 (validator): the same two-axis condition beside the root count. §2: the delegated bullet. `DECISION-CLOSURE.md` §4 prompt 5: remove it, or mark it.

### OD-44 — Which second source for the blind double extraction?

**Category.** D-METH (the design of a reliability test). It turns on what the owner meant by an earlier answer.

**Referred back.** The owner answered OR-15 "Yes, use batch 23's material" (PS:4675) to a prompt that described that material as "one code with a step table and one T1 paper with findings" and said "You choose the test material" (`grep -n 'id: OR-15' -A6 governance/owner-browser.yaml`). Batch 23 holds no Tier 1 or Tier 2 source. Option (a) keeps the T1 test and departs from the owner's "batch 23's material". Option (b) keeps the owner's words and loses the T1 test the prompt described. Option (c) is the owner naming it. The criteria favour (a) (C1: two readers agreeing on a code's table is not informative), but that conflicts with the letter of a standing owner answer, so condition (e) refers it back. The reason a code is not informative ("A code converges trivially") is the 2026-10-22 resolution report's own reasoning, not the owner's words (`scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md:1007`). Nothing is lost by asking: T-070 also needs the owner to launch the rater sessions.

**Facts checked.** The evidence command of T-070 §3 printed `batch 23 sources by tier: [(3, 'grey', 3), (5, 'national_fw', 3), (6, 'code', 8)]`. The T1 or T2 source with the most `finding` rows corpus-wide is `('REF-01033', 1, 'clinical', 'session_2026-10-30-ramp-spec-pages-rebuild', 3)`, tied with REF-01034 at 3. The batch-23 non-code source with the most rows is `('REF-01030', 5, 'national_fw', 7)`. **The assistant's recommendation, not a ruling:** (a), REF-01033 retrieved first (R10), beside batch 23's code with the most condition rows.

**Tasks.** Still holds T-070 (generator: `OD-44 | … | T-070 | — | 1`).

### OD-45 — A logged search whose request never returned results

**Category.** D-METH, the application of R14 and of the operative instrument (`decisions/DR-2026-08-19-research-restart-operative-instrument.md`). DG-REVIEW.

**Resolution.** (c) `OD-45: a search not run, deferred`. A logged search whose request returned no result list (a publisher 403 or bot challenge, a 429, a connection reset, a stub page) was not run. It is recorded with `deferred_reason` naming the failure, carries no `absence_class`, and is owed a re-run, including the Internet Archive route of `CLAUDE.md` §7. T-079's `v_deferred_acts` lists it. T-080's refusal tells such a request to log with `--deferred-reason`. T-081 records the stored rows as deferrals owed a re-run.

**What decided it.**
- *Standing rules.* R14: "A zero-yield search is evidence of ABSENCE only if the query was well-formed" (`grep -n -A8 'id: R14' governance/research-contract.yaml`). The operative instrument: "`deferred_reason` is for searches *not run*, never a findings channel" (DR line 1039). The owner: "deferred is okay so long as it runs eventually" (2026-09-18, PS:3737). `CLAUDE.md` §7: "A publisher block … is not terminal". Options (a) and (b) record a request that never reached the index as a finding about the index, against all three.
- *C1.* The mission distinguishes absence of evidence from evidence of absence (mission, "Silence on evidence-thin populations is not the default"). A failed request is neither, and no absence class may be written for it, not even a fourth one: `absence_class` is CHECKed to `results_found = 0`, and a request with no result list has no count. *C2.* A reader is never told "nothing found" where nothing was searched. *C3.* A blocked national source stays owed instead of closed, which matters most for the non-English jurisdictions the blocks fall on.

**Facts checked.**
- `python3 -I -c "import sqlite3;s=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute(\"select sql from sqlite_master where name='search_executions'\").fetchone()[0];i=s.find('absence_class');print(s[i:i+200])"` printed the three-value CHECK and `CHECK (absence_class IS NULL OR results_found = 0)`.
- T-080 §3's query printed `(13, 0, 1, 12)`. Rows 81, 87, 133, 138 and 191 describe a request that did not return a list, for example 87: "NOT A ZERO-YIELD — AN UNFIRED QUERY … All three requests returned HTTP 429", and 138: "RETRIEVAL FAILURE, NOT ABSENCE: HTTP 403".
- `grep -n -i -E 'search|deferred_reason' workplan/2026-11-12-bidirectional-pipeline/tasks/T-079-deferred-acts-with-age.md`: the view lists searches with `deferred_reason IS NOT NULL`.

**Reversal condition.** The owner wants a blocked request kept as a finding about the source's reachability, a fourth cause in a findings channel.

**Tasks.** Holds: T-080 and T-081 (generator: `OD-45 | … | T-080, T-081 | — | 1, 2`). It opens T-080 on a confirmed check and the bullet move. T-081 also waits on OI-55 (1), which this does not answer.

**Plan changes.** T-080 §4: the refusal is option (c)'s. T-081 §4: classify the five rows as deferrals with their reasons, and give the column comment's word "deliberate" (`deferred_reason TEXT -- non-NULL => deliberate no-search`) a sentence in the pull request: a blocked request is a search not run, not a choice. `DECISION-CLOSURE.md` §4 prompt 7.

### OD-46 — The `lang_jur_map` codes missing from the jurisdiction registry

**Category.** D-DOCT: "Inclusion/exclusion of jurisdictions" is always DG-NON (§2.4 item 4).

**Referred back.** Unsure; I went to referral. For resolving: the owner's OD-04 answer set the scope as a closed list (PS:5946), and none of the seventeen codes is on it, so option (a), declaring them out of scope, records an exclusion the owner already made. That is the "merely operationalises a prior decision" downgrade of §2.3, and (b) is unavailable to delegation because a removal is an exception to "retire in place then" that only the owner grants. Against resolving: the owner ruling of 2026-09-18 says of these very codes that "admitting a code silently converts a candidate jurisdiction into a declared one, and that is a scope decision about the project's coverage", with ACTION "(3) Do not admit a `lang_jur_map`-only code without a scope ruling" (PS:3714 and PS:3727). That entry calls the map "places the project **may expand into**". Whether OD-04 is that scope ruling for codes it does not name is a reading of the owner's words about a DG-NON type. A committed `INSERT` into the registry cannot be withdrawn without another owner exception. The decision blocks only an FK task. **The assistant's recommendation, not a ruling:** (a), with every pair marked `scoped-out` and the OD-04 entry as the approval.

**Facts checked.** `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('select count(distinct l.jurisdiction), count(*) from lang_jur_map l left join base_jurisdictions b on b.jurisdiction_code=l.jurisdiction where b.jurisdiction_code is null').fetchone())"` printed `(17, 19)`. The codes are AR, AT, CL, CO, CR, CY, EC, ET, GH, GT, MA (AR, FR), MX, PE, PH, TH, TZ (EN, SW) and UY. All are countries, none is in the OD-04 set, none is sub-national, and none respells a held code. `select scope_status, count(*) from lang_jur_map group by 1` printed `[(None, 70)]`. The registry already holds countries outside the OD-04 set, admitted because evidence uses them (`select jurisdiction_code from base_jurisdictions` includes BD, BR, EG, IN, KE, NG, UG, ZA), so membership is not scope.

**Tasks.** Still holds T-084, and through it T-085 (generator: `OD-46 | … | T-084 | T-085 | 2`).

### OD-47 — The lens of a figure whose clause names no person, function or need

**Category.** D-DOCT: "Population taxonomy structure (codes, sub-codes, proxy decisions)" is always DG-NON (§2.4 item 2).

**Referred back.** Option (a) assigns the lens from the function the parameter serves, which is a proxy decision in the plain sense of item 2. Option (b) takes the document's audience as a proxy. Options (c) and (d) decide which groups a code clause is said to serve. The adjudicator's R6 also names three rules that collide here: D-0182 (at least one lens), OD-31 (no `ALL`; general heading: ICF and need only) and the lens writer's warrant rule (the words must be found). Any option relaxes one of them. **The assistant's recommendation, not a ruling:** (a), with the crossing held once on the parameter (rule 5), the figure's basis recorded as "from the parameter's function", and never shown as the source's own words.

**Facts checked.** `grep -n 'def _require_lens_warrant' -A30 scripts/db.py` (line 9602): the bases `named_in_text`, `heading`, `study_participants`, each found in the source's words. `select basis, count(*) from v_live_lens_links where identity_code='ALL' group by 1` printed `[('carried', 34)]`. `select (icf_code is not null),(needs_code is not null),(identity_code is not null),count(*) from v_live_lens_links group by 1,2,3` printed `[(0, 0, 1, 212), (0, 1, 0, 3), (1, 0, 0, 1)]`: almost every live link is an identity link.

**Tasks.** No gate (generator: standing). It holds T-087's parked figures, and bears on T-115 step 3 and T-106.

### OD-48 — What `design_scale = 'universal'` states

**Category.** D-DOCT (Design Modes, mission commitment 4), with a D-SCHEMA effect.

**Referred back.** Unsure; I went to referral. The doctrine leans to (a), "whom it is for". The ledger's first rule calls Universal Mode "population-agnostic" (PS:14). The mission keeps tier and scale orthogonal: "Neither axis determines the other" (`governance/mission-and-epistemics.md` line 103), and "Universal Mode is a code-floor raised by population-level evidence" (line 107). Under (b), a universal value raised by evidence would stop being universal. `regulatory_stratum_only` already holds "rests on codes only" (rule 5). Two owner records nonetheless conflict:
1. DR-2026-07-12 item G1(a), ratified by owner directive 2026-07-13: "T4–6-only determinations are Universal-Mode regulatory determinations" (`decisions/DR-2026-07-12-evidence-architecture-unification.md` line 24). The engine's G1 line implements it (`grep -n 'G1  T4' scripts/assess/assess_cell.py`, line 86; `design_scale = SCALE_UNIVERSAL`, line 1405).
2. OD-31 of 2026-11-12, whose selected option says "'Universal' is stated once, by design_scale (one home)". The prompt the owner answered said "ALL only repeats what design_scale = 'universal' already says" (preserved transcript `transcripts/harness_4a95df3b/main.jsonl`, the `AskUserQuestion` for OD-31). That premise is false: the engine writes `universal` for code-only, not for "everyone".

Rule 0 would let the later statement win on contact, but OD-31 does not name G1. Treating a ratified record as superseded by a ruling that does not name it, on a premise that was false, is the act the delegation reserved (the OD-14 correction, PS:5751; condition (e)). The case has the same shape as OD-10, which was referred for the same reason. **The assistant's recommendation, not a ruling:** (a).

**Facts checked.** `PRAGMA table_info(specifications)`: `design_scale` with CHECK `('universal','population','person')`, and `regulatory_stratum_only` NOT NULL. `select count(*), sum(retired_at is null) from specifications` printed `(8, 0)`: no live determination exists today, so nothing on `main` displays the collision yet. The adjudicator's example is from its scratch copy.

**Tasks.** Still holds T-056, and through it T-115 (generator: `OD-48 | … | T-056 | T-115 | 2`). T-056 §2 also requires "the owner's words".

### OD-49 — Building type, a figure's other circumstances, and where an element lives

**Category.** D-SCHEMA (a carrier for a figure's circumstance), with a D-METH flow-through (the determination key). DG-REVIEW. Not a §2.4 type: a building-type vocabulary is not the inclusion or exclusion of a jurisdiction.

**Resolution.** `OD-49: (a1); (b2)`.
- **(a1)** Building type (use), new or existing work, and interior or exterior are each a typed circumstance on the figure, one value per cell, and the engine shows them as branches within one determination per parameter and lens. Building type points at the first of the three building levels the owner ruled on 2026-08-27 ("Building types (eg residential, commercial)"). That level is seeded from the owner's two examples and extended by data, each new type taken from an instrument's own scope phrase in a data pull request the owner reads (OR-17). "Public" is adjudicated per instrument, because the held instruments use it as a legal scope phrase. The vocabulary of the other two circumstances is set by T-091's design, as a column CHECK or a small row set, never a list in code (rule 8).
- **(b2)** The owner's "5 is three" ruling (2026-08-27) stands. `base_elements`, built when a reader needs it (T-060 or render), holds for each element a pointer to its term and its parent within the level. It holds no name of its own, so the term stays the element's one home (rule 5), and the element is never a container that figures are filed into (OR-14, OR-14b).

**What decided it.**
- *Standing rulings forbid the other options.* (a2) changes the key the owner ruled on 2026-08-26 and 2026-08-28, which condition (e) forbids. (a3) leaves three facts joined in `setting`, against the owner's schema-shape ruling of 2026-11-06 ("one value per cell", `CLAUDE.md` §4) and against the owner's first building level. (b1) withdraws the "three tables" ruling, which no later owner statement names. OR-14 (PS:4699) concerns element *pages*, and treating an owner ruling as lapsed by implication is reserved (PS:5751). So (a1) and (b2) are the only options left within the delegation.
- *C1.* A dwelling figure and a public-building figure no longer compose into one headline the engine cannot tell apart. The key is unchanged. *C2.* A designer reads the branch for their building use. *C3.* The circumstances the owner's Q7 asked about become visible to every group's cells.
- The pattern follows OD-01 (confirmed with corrections): a circumstance is a typed condition and a branch, never a key.

**Facts checked.**
- `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('select setting from source_value_extractions where parameter_id=9').fetchall()[:8])"` printed values such as `'new buildings; straight-on approach'` and `'existing buildings; right angles to an access route at least 1500 mm wide'`: three facts in one cell.
- `select count(*), count(distinct setting), sum(setting is not null) from source_value_extractions` printed `(214, 76, 125)`.
- `grep -n 'setting' scripts/assess/assess_cell.py` printed one docstring line (327) and nothing that reads the column.
- `select name, type from sqlite_master where name like '%room%' or name like '%building%' or name like '%element%'` printed only `rooms`. No building-type or element table exists, and the `room_items` the 2026-08-27 ACTION names is gone.
- The rulings: PS:2053 ("THREE levels"), PS:2082 (ACTION), PS:2196 (D3, reopened), and the owner's "5 is three" later the same day (PS:2419, `grep -n -F '"5 is three."' references/project-standards.md`).

**Reversal condition.** The owner wants building type in the key, or elements held as terms only. Or a parameter's branches by building use cannot be shown without hiding a group's difference.

**Tasks.** Holds: T-091 and T-092 (generator: `OD-49 | … | T-091, T-092 | — | 1, 2`). It opens T-091 (its design file is written after the answer) on a confirmed check and the bullet move. Part (b) bears on T-060's design only.

**Plan changes.** T-091 §2: delegated bullet. Its design file states (a1) as above, with building type pointing at the building-type level, whose creation T-091's design names. T-092: delegated bullet, and delete the "(a3) declined" sentence. T-060 design: element rows as in (b2). `DECISION-CLOSURE.md` §4 prompt 11.

### OD-50 — May a source that is not a code add a parameter?

**Category.** D-METH, the application of the existing minting and promotion rules. DG-REVIEW.

**Resolution.** (a) `OD-50: any admitted source`. Any admitted source may promote a quantity it states to a parameter, in its data pull request, under the conditions already standing: the name is the source's own phrase in its jurisdiction and language (OR-17), minted from an observation (`add-term --from-observation`). The term is a quantity with a kind (T-020), passes the writer's domain refusals, and becomes a parameter by `add-parameter`. The owner reads the pull request (OR-17). Until a named judge picks a name, the first recorded name is shown (OD-38).

**What decided it.**
- *Standing rulings.* OR-13 ("From the codes held") answered a choice between two seeding routes for D-8, "From the codes held" or "Slug by slug" (`grep -n 'id: OR-13' -A18 governance/owner-browser.yaml`). It is not a rule on which sources may add a parameter later. The owner's own words on the parameter list are "pull from the major codes, literature and advocacy from major countries" (PS:4395). The 2026-10-09 scan contract reads every admitted source against the whole list and takes "names from observed phrases" (PS:4422). The skill states that `add-parameter` takes no approval flag and that "Owner approval is the data PR the owner reads" (`skills/run-pipeline_SKILL.md` lines 69 to 74).
- *C1.* A parameter is a question, not an answer: promoting one asserts no value, and every figure still carries its own tier. Requiring a code to state a quantity first would make the weak band (mission, commitment 2) the gatekeeper of what the book may ask. *C2.* Neutral. *C3.* Quantities that codes rarely state (sensory, cognitive, rest and seating) can then be asked about. The adjudication's coverage finding is that the catalogue cannot speak for blind, Deaf, cognitive or invisible needs (ADJUDICATION §3).

**Facts checked.** The quotes above. `python3 scripts/db.py decline-parameter --help` and the skill lines show the verbs take no approval flag. REF-01037 is not in the canonical database (`select ref_id from evidence_sources where ref_id='REF-01037'` printed `[]`); its batch is T-087's.

**Reversal condition.** The owner wants parameters only from codes or standards, or from two independent sources. Or the catalogue grows faster than readings can be owed against it (`v_scan_ledger` debt that no batch discharges).

**Tasks.** No gate (generator: standing). It bears on T-072 (its subject is unchanged; the coordinator may widen it or author a sibling, as T-072 line 24 already provides) and on T-087 (its quantity concepts need not wait).

**Plan changes.** T-087 §4: a quantity concept the checklist states may be minted and promoted in the batch, not deferred on OD-50, and its rationale names this entry. T-072 line 24: name this resolution. `DECISION-CLOSURE.md` §4 prompt 12.

### OD-51 — A municipal advisory committee's document and Co-1 standing

**Category.** D-DOCT: "Evidence-tier definitions" and "Co-1 source corpus inclusion/exclusion" are always DG-NON (§2.4 items 3 and 6).

**Referred back.** **The assistant's recommendation, not a ruling:** (b). The document is Co-1 only on a retrieved source showing that disabled members authored it, recorded by name as co-producers (`CLAUDE.md` §6: "Co-1's warrant is co-production"). Facts: the Co-1 row reads "Disability-led lived-experience publications — DPOs, … CRPD Art. 4.3 consultation outputs" (`grep -n -F '| **Co-1** |' governance/tier-system.md`, line 16). The second edge of OR-5b is open (`OR-5b STATUS: ANSWERED BY THE OWNER, PARTLY`, PS:6174).

**Tasks.** No gate. REF-01037 stays T3 grey in T-087.

### OD-52 — "Barrier-free path of travel" as the Edmonton checklist uses it

**Category.** D-METH (vocabulary). Catalogue terms are approved by the owner before they are added (2026-10-09, as the OT-2 prompt records: `grep -n 'id: OT-2' -A6 governance/owner-browser.yaml`).

**Referred back.** Options (a) and (b) widen the scope note the owner approved, which reads "A circulation route through a building … the whole route", to an outdoor route. Option (c) applies the definition as written and leaves the observations waiting on another owner prompt (observation 71). Either way the answer is the owner's words on the owner's term. One fact bears on it: the source the scope note cites for the phrase, the Ontario code (REF-01013), uses it for "floor s or walks in a barrier-free path of travel" (its saved page, `retrieval-log/session_2026-09-28-research-batch-22-selection/40becb4f9c8fbb81.html`, three hits). **The assistant's recommendation, not a ruling:** (b). The route is the term, with the scope note widened to outdoor walks, which the code itself covers. The contrast provision is a separate figure for blind and low-vision people, consistent with the owner's separation of this term from a route "navigated by someone who is blind" (PS:4802).

**Tasks.** No gate. It holds two observations of T-087.

### OD-53 — May a single-source batch decline held terms as parameters?

**Category.** D-OP / D-METH application (who records a declination already provided for). DG-REVIEW. Not a §2.4 type.

**Resolution.** (a), bounded: `OD-53: any batch, for a term its own adjudications name, one stated reason per term, element or method only`. A research batch may decline, with `decline-parameter --reason`, a held term that an adjudication of its own observations names, when the term is an element, a lens term or a method (the verb's own reason vocabulary). It may not decline a quantity: a quantity is promoted (OD-50) or left for T-072. Each declination is listed in the data pull request the owner reads. T-072 item 6 reviews the declinations in its catalogue-wide pass and revokes any it disagrees with (`revoke-declination`).

**What decided it.**
- *Standing records.* The gate requires it and was built expecting it. R16's own comment reads: "every named term must be disposed of, figure or none. A disposition is per term and corpus-wide, so that costs one call per term once, not one per batch", and "the rule does not hold red a batch that did its judging" (`scripts/audit/research_batch_dod.py` lines 988 to 1013). The skill: `decline-parameter` "take[s] no approval flag", with approval in the data pull request (OR-17). E12 records declining terms as parameters, "each with a reason, and kept as terms" (PS:5060). No owner ruling reserves declination to one task.
- *C1.* A declination carries its reason and its judge, is revocable, and is reviewed twice, by the owner reading the pull request and by T-072 item 6. A research gate held red with a waiver on every batch until T-072 runs is a check red by construction, which `CLAUDE.md` rule 6 says "teaches its reader to ignore it". *C2.* The batch's R16 means what it says. *C3.* The adjudicator's coverage concern, that declined elements leave the Deaf and blind vocabulary with no parameter under them, is answered by limiting declination to elements and methods and by T-090's coverage read, not by withholding the act.

**Facts checked.** `python3 -I -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('select count(*), sum(not exists(select 1 from base_parameters p where p.term_id=t.term_id) and not exists(select 1 from parameter_declinations d where d.term_id=t.term_id and d.revoked_at is null)) from terms t').fetchone())"` printed `(94, 83)`. `python3 scripts/db.py decline-parameter --help`: `--reason` "WHY this term is not a quantity under determination (an element, a lens term, a method)". T-072 item 6: line 78.

**Reversal condition.** Batch declinations prove inconsistent, with T-072 item 6 revoking a material share of them, or a declined element hides a group that no coverage read reports.

**Tasks.** No gate (generator: standing). It changes T-087: R16 can turn green by declining in the batch. Its waiver is needed only for any term left undisposed.

**Plan changes.** T-087 §4 item 6 and §11: decline the named elements and methods with a reason each, and keep the waiver only for what is left. T-072 line 24: name this resolution, and item 6 reviews batch declinations. `REMEDIATION-WORKPLAN.md` §8 OD-53's "Holds". `DECISION-CLOSURE.md` §4 prompt 15.

### OD-54 — May an agent write the canonical row by hand when a writer cannot hold content?

**Category.** D-OP with doctrine-level effect. Option (b) would set aside `CLAUDE.md` rules 3 and 10, which only a live owner statement can do (rule 0).

**Referred back.** **The assistant's recommendation, not a ruling:** (a), into the register and replayed through the writer, which T-088 and T-089 already build. It keeps every canonical row behind the refusals that stop an invented or mistyped value (`CLAUDE.md` §5 (c)), and still loses no content. Facts: `CLAUDE.md` rule 3 ("Never write `data/guidebook.db` directly. Migrations only") and rule 10 ("never patched with hand SQL disguised inside the batch's data migration"); the ADJUDICATION Q10 reading.

**Tasks.** None held.

### OD-55 — After a second reading of a bare-`ratio` gradient, is the stored row retired?

**Category.** D-METH application (the owner's retire-in-place ruling of 2026-09-16). DG-REVIEW.

**Resolution.** `OD-55: not reached while OD-41 stands as a reformat; if OD-41 is reversed to a new reading, retire the stored row in place once its second reading is written, naming its successor`. Under the resolution of OD-41 above there is no second row. If OD-41 is reversed, the stored row is retired in place (T-078's verb) with its successor named, and the engine and the value note count one claim per pair.

**What decided it.** The owner's "retire in place then" (2026-09-16) keeps the stored row as history. Rule 5 forbids two live homes for one statement. *C1:* one claim per statement. *C2:* the note does not double-count. *C3:* neutral.

**Facts checked.** As OD-41. `grep -n -F 'retire in place then' references/project-standards.md` finds the ruling.

**Reversal condition.** The owner says D-0168's second row must leave the first live.

**Tasks.** No gate. It bears on T-086 §4 item 2 only under a reversed OD-41.

---

## 2. Ledger-ready text

To be appended to `references/project-standards.md` by the session that records it, in this order, only after the owner has seen it or the coordinating session decides to record it. **No line below is in the ledger yet.**

```
## Owner question 2026-11-13 — may the open decisions OD-40 to OD-55 be resolved by an Opus-class model on prior rulings, doctrine and the project's goal

Given in the coordinating session of the Edmonton case study (`session_2026-11-13-edmonton-checklist-pass`), dated by the server clock, UTC, and recorded on contact per `CLAUDE.md` rule 0. Quoted verbatim, in the order given:

> "are you sure you can't resolve these owner decisions using Opus based upon prior rulings, mission/doctrine and project goal?"

> "I don't know the machinery or code"

**What this records.** The owner asks whether the open register decisions OD-40 to OD-55 can be resolved by an Opus-class model on the owner's prior rulings, the mission and doctrine, and the project's goal, and says the owner cannot judge the machinery or the code. [ASSUMPTION: read as asking that the delegation of 2026-11-12 ("I guess opus can do it") be applied to OD-40 to OD-55 with its limits: nothing in an always-DG-NON type of `governance/decision-protocol.md` §2.4 is resolved; a resolution never overrides a standing owner ruling (condition (e)); and every resolution is checked by a second, independent Opus-class instance before it is relied on (condition (d)). The first sentence is a question, not a ruling. Unratified.] The pass is `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2.md`; the decisions referred back are put in plain words in `workplan/2026-11-12-bidirectional-pipeline/OWNER-SHEET-PLAIN.md`.

CONDITION: any session asking whether OD-40 to OD-55 are answered, or relying on a resolution of one.
ACTION: (1) Read each decision's state by the gate of the 2026-11-12 convention, never by its `OD-NN:` line. (2) Treat every resolution of this pass as delegated, not the owner's words, and not to be relied on until its check line reads confirmed. (3) Treat the [ASSUMPTION] above as unratified.
DATE: 2026-11-13 — owner question, quoted above.


## Delegated resolution 2026-11-13 — OD-40 what a derived figure carries as its quote and its locator

This is a resolution by an Opus-class model under the owner's delegation of 2026-11-12 ("I guess opus can do it"), applied to this decision at the owner's question of 2026-11-13 (entry above), judged against the owner's three criteria in the order ratified by OI-14. **It is not the owner's words**, it stands until the owner reverses it, and under condition (d) it is **not to be relied on until a second, independent Opus-class instance has checked it**. Reasoning, facts and commands: `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2.md` (section OD-40).

OD-40: a derived figure has no quote or locator of its own; both are its inputs'

**The resolution.** A derived row stores no quote and no locator; its words and its place are its two inputs', reached through its two `derived_from` edges, each carrying its input's verified quote. The writer refuses a derived row whose inputs lack a quote or a locator and still checks the arithmetic. A derived figure a source does state in words may carry that quote, checked like any other.

**What decided it.** The owner's 2026-08-24 ruling ("It is better to have a table cell point to another table cell than to rewrite") names it; the owner's 2026-09-13 ruling ("Derived figures are a weighted average of their figures") presupposes derived rows, so deleting the verb is not available. Criterion 1: every stored quote stays a source's own bytes, so the verbatim floor has no exemption; an analyst's sentence in a column that means "the source's words" is the shape of the fabricated-citation failure.

**Reversal condition.** A derived figure must be shown with a sentence of its own that no input supplies, or the owner wants computed figures kept only in prose.

CONDITION: any session writing, repairing or reading a derived figure.
ACTION: (1) Store no quote or locator on a derived row; reach both through its edges. (2) Refuse a derived row whose inputs lack either. (3) Keep the arithmetic check. (4) Do not rely on this entry until the independent check of condition (d) is recorded.
DATE: 2026-11-13 — delegated resolution, not an owner statement.

OD-40 STATUS: RESOLVED UNDER DELEGATION
OD-40 CHECK: pending


## Delegated resolution 2026-11-13 — OD-41 the unit `ratio` changed to `rise:run ratio`

This is a resolution by an Opus-class model under the owner's delegation of 2026-11-12 ("I guess opus can do it"), applied at the owner's question of 2026-11-13, judged against the owner's three criteria in the order ratified by OI-14. **It is not the owner's words**, it stands until the owner reverses it, and it is **not to be relied on until the independent check of condition (d) is recorded**. It is a reading of the owner's OR-3 under condition (c), resting on the prompt the owner answered. Reasoning: `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2.md` (section OD-41).

OD-41: ratio to rise:run ratio is a reformat

**The resolution.** The stored rows whose unit is the bare word `ratio` are amended in place under OR-3 (same digits and quote, the old unit kept in notes). `amend-extraction` gains one branch: a new unit in the notation families is accepted when the old unit stands, on word boundaries, in the new one and the stored figure reads under it.

**What decided it.** The OR-3 prompt the owner answered "Yes, reformat in place" listed, among the forms to reformat, "a unit written 'ratio' where it is 'rise:run ratio'" (`grep -n 'id: OR-3$' -A8 governance/owner-browser.yaml`). Criterion 1: both options assert the same reading; a second row would be a second live home for one statement (rule 5).

**Reversal condition.** The owner says the OR-3 example did not mean these rows, or a row's source defines its ratio otherwise (rise over sloped length), which is then a new reading.

CONDITION: any session amending a bare-`ratio` row or building the reformat branch.
ACTION: (1) Amend in place under OR-3, keeping the old unit in notes. (2) Write no second row for these. (3) Do not rely on this entry until the independent check of condition (d) is recorded.
DATE: 2026-11-13 — delegated resolution, not an owner statement.

OD-41 STATUS: RESOLVED UNDER DELEGATION
OD-41 CHECK: pending


## Delegated resolution 2026-11-13 — OD-42 a figure moved between metric units

This is a resolution by an Opus-class model under the owner's delegation of 2026-11-12 ("I guess opus can do it"), applied at the owner's question of 2026-11-13, judged against the owner's three criteria in the order ratified by OI-14. **It is not the owner's words**, it stands until the owner reverses it, and it is **not to be relied on until the independent check of condition (d) is recorded**. It reads OR-10 under condition (c). Reasoning: `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2.md` (section OD-42).

OD-42: a metric-to-metric conversion is shown exactly

**The resolution.** A change of metric prefix (cm to mm, m to mm) keeps the source's digits and is shown exactly. The nearest quarter inch or 5 mm, on the safe side (OR-10, OD-22), applies to a conversion between inch-foot and metric units.

**What decided it.** OR-10 answered a question about "inches and feet to millimetres and metres". Criterion 1: rounding a prefix change prints digits no source stated for a figure whose exact digits are in hand; it gains nothing in legibility, and an exact minimum is never below the source's.

**Reversal condition.** The owner says OR-10's rounding covers every shown converted length.

CONDITION: any session converting or displaying a length.
ACTION: (1) Show a metric prefix change exactly. (2) Round only an inch-foot and metric conversion, on the safe side. (3) Do not rely on this entry until the independent check of condition (d) is recorded.
DATE: 2026-11-13 — delegated resolution, not an owner statement.

OD-42 STATUS: RESOLVED UNDER DELEGATION
OD-42 CHECK: pending


## Delegated resolution 2026-11-13 — OD-43 when the engine may call a cell `convergent`

This is a resolution by an Opus-class model under the owner's delegation of 2026-11-12 ("I guess opus can do it"), applied at the owner's question of 2026-11-13, judged against the owner's three criteria in the order ratified by OI-14. **It is not the owner's words**, it stands until the owner reverses it, and it is **not to be relied on until the independent check of condition (d) is recorded**. It applies a ratified definition; it makes none. Reasoning: `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2.md` (section OD-43).

OD-43: convergent only when the clinical (Tier 1 to 3) and Co-1 axes both govern, state the same bound, can all hold, and rest on two or more independent roots

**The resolution.** The engine writes `convergent` only when the governing figures include its clinical axis and its Co-1 axis, the axes state the same bound on the parameter's scale, the anchoring claims can all hold, and the governing figures rest on two or more independent roots; otherwise `pending_assessment` (two or more axes) or `single_axis`. A clinical and Co-2 cell is never `convergent`. The validator checks the same conditions.

**What decided it.** The ratified definition ("Tier 1–3 clinical evidence and Co-1 evidence agree on the parameter value or range", `governance/evidence-methodology.md`) and its rendered sentence, which names Co-1 sources; H1 (roots, not documents); OR-6b (differing satisfiable floors are not divergent, which is not agreement). Criterion 1: the book says the evidence agrees only when it does.

**Reversal condition.** The owner wants agreement within a stated tolerance to count, or convergence without Co-1 evidence (which would rewrite the definition).

CONDITION: any session building or reading the convergence status.
ACTION: (1) Write `convergent` only on all four conditions. (2) Keep differing floors that can all be met `pending_assessment`, with the spread in the note. (3) Do not rely on this entry until the independent check of condition (d) is recorded.
DATE: 2026-11-13 — delegated resolution, not an owner statement.

OD-43 STATUS: RESOLVED UNDER DELEGATION
OD-43 CHECK: pending


## Delegated resolution 2026-11-13 — OD-45 a logged search whose request never returned results

This is a resolution by an Opus-class model under the owner's delegation of 2026-11-12 ("I guess opus can do it"), applied at the owner's question of 2026-11-13, judged against the owner's three criteria in the order ratified by OI-14. **It is not the owner's words**, it stands until the owner reverses it, and it is **not to be relied on until the independent check of condition (d) is recorded**. Reasoning: `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2.md` (section OD-45).

OD-45: a search not run, deferred

**The resolution.** A logged search whose request returned no result list (a 403 or bot challenge, a 429, a connection reset, a stub page) is a search not run: recorded with `deferred_reason` naming the failure, with no absence class, and owed a re-run, including the Internet Archive route.

**What decided it.** R14 (absence is evidence only for a well-formed query), the operative instrument ("`deferred_reason` is for searches *not run*, never a findings channel"), the owner's "deferred is okay so long as it runs eventually" (2026-09-18). Criterion 1: the book never reports absence where nothing was searched.

**Reversal condition.** The owner wants a blocked request kept as a finding about a source's reachability.

CONDITION: any session logging, classifying or re-running a search.
ACTION: (1) Log a request with no result list as deferred, with its reason. (2) Give it no absence class. (3) Re-run it. (4) Do not rely on this entry until the independent check of condition (d) is recorded.
DATE: 2026-11-13 — delegated resolution, not an owner statement.

OD-45 STATUS: RESOLVED UNDER DELEGATION
OD-45 CHECK: pending


## Delegated resolution 2026-11-13 — OD-49 building type, a figure's other circumstances, and where an element lives

This is a resolution by an Opus-class model under the owner's delegation of 2026-11-12 ("I guess opus can do it"), applied at the owner's question of 2026-11-13, judged against the owner's three criteria in the order ratified by OI-14. **It is not the owner's words**, it stands until the owner reverses it, and it is **not to be relied on until the independent check of condition (d) is recorded**. Reasoning: `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2.md` (section OD-49).

OD-49: (a1); (b2)

**The resolution.** (a1) Building type, new or existing work, and interior or exterior are each a typed circumstance on the figure, one value per cell, shown as branches within one determination per parameter and lens; building type points at the first of the owner's three building levels, seeded from the owner's examples ("residential, commercial") and extended by data, each new type from an instrument's own scope phrase in a data pull request; "public" is adjudicated per instrument. (b2) The owner's 2026-08-27 "three tables" ruling stands; an element row, when a reader needs it, holds a pointer to its term and its parent within the level, and no name of its own.

**What decided it.** The other options override standing owner rulings: (a2) the determination key (2026-08-26, 2026-08-28); (a3) one value per cell (2026-11-06) and the building levels (2026-08-27); (b1) "5 is three" (2026-08-27), which OR-14 on element pages does not name. Criterion 1: figures for different building uses no longer compose into one headline; the key is unchanged.

**Reversal condition.** The owner wants building type in the key, or elements as terms only.

CONDITION: any session designing a figure's circumstance, a building-type vocabulary, or the element level.
ACTION: (1) Type each circumstance in its own cell and branch on it. (2) Point building type at the ruled first level. (3) Build element rows as pointers to terms when a reader needs them. (4) Do not rely on this entry until the independent check of condition (d) is recorded.
DATE: 2026-11-13 — delegated resolution, not an owner statement.

OD-49 STATUS: RESOLVED UNDER DELEGATION
OD-49 CHECK: pending


## Delegated resolution 2026-11-13 — OD-50 a source that is not a code adding a parameter

This is a resolution by an Opus-class model under the owner's delegation of 2026-11-12 ("I guess opus can do it"), applied at the owner's question of 2026-11-13, judged against the owner's three criteria in the order ratified by OI-14. **It is not the owner's words**, it stands until the owner reverses it, and it is **not to be relied on until the independent check of condition (d) is recorded**. Reasoning: `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2.md` (section OD-50).

OD-50: any admitted source

**The resolution.** Any admitted source may promote a quantity it states to a parameter in its data pull request, under the standing conditions: the source's own phrase (OR-17), minted from an observation, a quantity with a kind (T-020), the owner reading the pull request.

**What decided it.** OR-13 chose between seeding from the codes held and seeding slug by slug; it does not limit later growth. The owner's words of 2026-10-09: "pull from the major codes, literature and advocacy from major countries". Criterion 1: a parameter is a question, not a value. Criterion 3: quantities codes rarely state can be asked about.

**Reversal condition.** The owner wants parameters only from codes or standards, or from two independent sources.

CONDITION: any session promoting a parameter from a source that is not a code or standard.
ACTION: (1) Promote under the standing conditions, in a data pull request. (2) Do not rely on this entry until the independent check of condition (d) is recorded.
DATE: 2026-11-13 — delegated resolution, not an owner statement.

OD-50 STATUS: RESOLVED UNDER DELEGATION
OD-50 CHECK: pending


## Delegated resolution 2026-11-13 — OD-53 declining held terms in a single-source batch

This is a resolution by an Opus-class model under the owner's delegation of 2026-11-12 ("I guess opus can do it"), applied at the owner's question of 2026-11-13, judged against the owner's three criteria in the order ratified by OI-14. **It is not the owner's words**, it stands until the owner reverses it, and it is **not to be relied on until the independent check of condition (d) is recorded**. Reasoning: `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2.md` (section OD-53).

OD-53: any batch, for a term its own adjudications name, one stated reason per term, element or method only

**The resolution.** A research batch may decline a held term that an adjudication of its own observations names, when the term is an element, a lens term or a method, with one stated reason per term, listed in its data pull request. It may not decline a quantity. T-072's catalogue pass reviews these declinations and may revoke any.

**What decided it.** The research gate's own design ("A disposition is per term and corpus-wide, so that costs one call per term once"; "the rule does not hold red a batch that did its judging"); the verb takes no approval flag and approval is the data pull request (OR-17); E12. Criterion 1: each declination is reasoned, attributed, revocable and reviewed twice, and a gate red by construction is avoided.

**Reversal condition.** Batch declinations prove inconsistent under the catalogue review, or a declined element hides a group no coverage read reports.

CONDITION: any research batch whose adjudications name held terms that are neither parameters nor declined.
ACTION: (1) Decline only elements, lens terms and methods, one reason each. (2) List them in the pull request. (3) Do not rely on this entry until the independent check of condition (d) is recorded.
DATE: 2026-11-13 — delegated resolution, not an owner statement.

OD-53 STATUS: RESOLVED UNDER DELEGATION
OD-53 CHECK: pending


## Delegated resolution 2026-11-13 — OD-55 the stored row after a second reading of a bare-`ratio` gradient

This is a resolution by an Opus-class model under the owner's delegation of 2026-11-12 ("I guess opus can do it"), applied at the owner's question of 2026-11-13, judged against the owner's three criteria in the order ratified by OI-14. **It is not the owner's words**, it stands until the owner reverses it, and it is **not to be relied on until the independent check of condition (d) is recorded**. Reasoning: `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2.md` (section OD-55).

OD-55: not reached while OD-41 stands as a reformat; if OD-41 is reversed, retire the stored row in place once its second reading is written, naming its successor

**The resolution.** Under the resolution of OD-41 no second row is written. If OD-41 is reversed to a new reading, the stored row is retired in place with its successor named, and the note and the engine count one claim per pair.

**What decided it.** The owner's "retire in place then" (2026-09-16) and rule 5 (one live home per statement).

**Reversal condition.** The owner says a second reading must leave the first live.

CONDITION: any session writing a second reading of a bare-`ratio` row.
ACTION: (1) Retire the stored row in place, naming its successor. (2) Do not rely on this entry until the independent check of condition (d) is recorded.
DATE: 2026-11-13 — delegated resolution, not an owner statement.

OD-55 STATUS: RESOLVED UNDER DELEGATION
OD-55 CHECK: pending


## Referrals 2026-11-13 — OD-44, OD-46, OD-47, OD-48, OD-51, OD-52 and OD-54 referred back to the owner

Recorded in the same pass, under the owner's question of 2026-11-13 (entry above). **Not the owner's words.** Each decision below was examined for resolution under the delegation of 2026-11-12 and is referred back; the reasons, the facts checked and the assistant's recommendation (marked as such) are in `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-2.md`, and the plain-language questions are in `workplan/2026-11-12-bidirectional-pipeline/OWNER-SHEET-PLAIN.md`.

- **OD-44.** The owner's OR-15 answer rests on a premise the repository does not bear out (batch 23 holds no Tier 1 or Tier 2 source); every option either departs from the answer or drops the reason the prompt gave; the prompt marked the choice as the owner's (condition (e)).
- **OD-46.** Inclusion or exclusion of jurisdictions is always DG-NON (`governance/decision-protocol.md` §2.4 item 4), and the owner ruling of 2026-09-18 calls admitting a map-only code a scope decision.
- **OD-47.** Population taxonomy, including proxy decisions, is always DG-NON (§2.4 item 2).
- **OD-48.** Design Modes are mission doctrine, and two owner records conflict (DR-2026-07-12 item G1(a), ratified 2026-07-13; the OD-31 option of 2026-11-12, chosen on a premise the engine contradicts); concluding that one supersedes the other without naming it is reserved.
- **OD-51.** Evidence-tier definitions and the Co-1 corpus are always DG-NON (§2.4 items 3 and 6).
- **OD-52.** The term, its definition and its scope note are the owner's approved words; catalogue terms are approved by the owner.
- **OD-54.** Option (b) sets aside `CLAUDE.md` rules 3 and 10, which only the owner can do.

OD-44 STATUS: REFERRED BACK TO THE OWNER
OD-46 STATUS: REFERRED BACK TO THE OWNER
OD-47 STATUS: REFERRED BACK TO THE OWNER
OD-48 STATUS: REFERRED BACK TO THE OWNER
OD-51 STATUS: REFERRED BACK TO THE OWNER
OD-52 STATUS: REFERRED BACK TO THE OWNER
OD-54 STATUS: REFERRED BACK TO THE OWNER

CONDITION: any session asking whether one of these seven decisions is answered.
ACTION: (1) Treat each as the owner's, CLOSED by the gate. (2) Put the plain-language question to the owner. (3) Record the owner's answer with `ANSWERED BY THE OWNER` in the same entry.
DATE: 2026-11-13 — referrals recorded in the delegated pass, not owner statements.
```

**What the gate will read once these are appended.** Every resolved decision reads `CLOSED (check: pending)` until a later line `OD-NN CHECK: confirmed` (or `confirmed with corrections applied`) is appended by the independent check. Each referred decision reads `CLOSED (REFERRED BACK TO THE OWNER)`. No task opens on this pass alone.

---

## 3. Plain-language sheet

`workplan/2026-11-12-bidirectional-pipeline/OWNER-SHEET-PLAIN.md`, for OD-44, OD-46, OD-47, OD-48, OD-51, OD-52 and OD-54.

---

## 4. Facts in the register, the adjudication or the plan that the repository contradicts

1. **OD-41 is not open on the record.** The register entry (`REMEDIATION-WORKPLAN.md` §8, "Why it is the owner's. It is a reading of the owner's own ruling OR-3") and T-061 line 154 ("Whether that change is a reformat is the owner's reading of OR-3") treat it as unasked. The OR-3 prompt the owner answered lists "a unit written 'ratio' where it is 'rise:run ratio'" as a case of reformatting (`governance/owner-browser.yaml` line 219).
2. **"A conversion from inches is inexact" is false** (OD-42 register entry and `DECISION-CLOSURE.md` §4 prompt 4). One inch is 25.4 mm exactly, and OR-10's own prompt says "Inches and feet convert to millimetres and metres exactly" (`grep -n 'id: OR-10' -A10 governance/owner-browser.yaml`). The real difference is between a metric prefix change, which keeps the digits, and a change of measurement system. No inch or foot figure is held today (`select claimed_unit, count(*) … group by 1`, §1 OD-42).
3. **OD-40's "No ruling settles it" leaves out a bearing ruling.** The owner's 2026-09-13 ruling ("Derived figures are a weighted average of their figures", PS:3178) presupposes derived rows, so option (c) contradicts a standing owner ruling. The register lists (c) as open.
4. **OD-43's options (a) and (b) are looser than the ratified definition.** "Two or more axes" is satisfied by clinical plus Co-2 (`assess_cell.py` lines 1296 to 1299). The definition requires clinical and Co-1 (`evidence-methodology.md` line 245), and the rendered sentence names Co-1 sources (line 284).
5. **OD-48 omits the owner-ratified record behind the engine's G1.** DR-2026-07-12 item G1(a) was ratified by owner directive on 2026-07-13 (the DR's status line). The OD-31 prompt the owner answered stated "ALL only repeats what design_scale = 'universal' already says" (transcript `harness_4a95df3b`), which the engine contradicts: it writes `universal` for code-only determinations (`assess_cell.py` line 1405). ADJUDICATION AQ-2 and R3 carry the same omission.
6. **OD-50's entry reads OR-13 as a restriction on sources.** OR-13 chose "From the codes held" over "Slug by slug" as the seeding route for D-8 (`governance/owner-browser.yaml` lines 543 to 560). The owner's 2026-10-09 words name "codes, literature and advocacy" (PS:4395). ADJUDICATION R9 and Q2 item 3 share the reading.
7. **OD-49's "a later answer (OR-14) may have overtaken" the three-tables ACTION.** OR-14 concerns element pages (`governance/owner-browser.yaml` line 562). The owner's own "5 is three" (PS:2419), given after the D3 reopening, is the ruling on tables. The same ACTION's "`room_items` is the existing one and is re-pointed" names a table that no longer exists (`select name from sqlite_master where name like '%room%'` prints only `rooms`); ADJUDICATION Q7 also notes this.
8. **OD-44's "The second source exists because a code converges trivially"** is the 2026-10-22 resolution report's reasoning (`scratchpad/session_2026-10-22-pipeline-stress-test/resolution-report-2026-10-22.md:1007`). The register's wording reads as though the owner said it; the owner's words are only "Yes, use batch 23's material".
9. **OD-53's plan route works against the gate's stated design.** T-087's red-with-waiver route for R16 contradicts the gate's own comment: "the rule does not hold red a batch that did its judging" and "A disposition is per term and corpus-wide, so that costs one call per term once, not one per batch" (`scripts/audit/research_batch_dod.py` lines 988 to 1013).
10. **OD-45: the column comment and the instrument differ.** `search_executions.deferred_reason`'s DDL comment says "non-NULL => deliberate no-search for this cell", while the operative instrument says "for searches *not run*" (DR line 1039). A blocked request is not run but not deliberate either. T-080 should align the comment.
11. **OD-52: the cited source widens the approved definition.** The scope note the owner approved cites REF-01013 as the source phrase, and that saved code page applies the phrase to "floor s or walks" (`retrieval-log/session_2026-09-28-research-batch-22-selection/40becb4f9c8fbb81.html`), while the approved definition says "through a building". This was not before the owner when OT-2 was approved.
12. **The generator is not read-only.** `DECISION-CLOSURE.md` §4 and `REMEDIATION-WORKPLAN.md` §8 tell a reader to run `build_batches.py` to read the state of the decisions. Each run rewrites the tracked `REMEDIATION-PLAN.md` (`OUT.write_text`, line 333), so reading the state dirties the tree.
13. **OD-48's example is not on `main`.** `select count(*), sum(retired_at is null) from specifications` prints `(8, 0)`: no live determination exists in the canonical database. The "wheelchair-keyed cell reads `universal`" of the register and of ADJUDICATION Q6 is from the adjudicator's scratch copy.
