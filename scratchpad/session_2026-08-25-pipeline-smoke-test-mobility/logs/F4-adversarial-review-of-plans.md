# F4 — READ-ONLY ADVERSARIAL REVIEW OF THE SESSION'S PLANS AND CONTENT

Commissioned by the owner, 2026-08-25. Subject: `WALK-REPAIR-PLAN.md`, `WAVE-H-SCOPE.md`,
`severed-walk.html`, the session record, and the two ledger entries appended to
`references/project-standards.md` today. Every claim below was re-derived read-only against the
committed repository (`data/guidebook.db` sha256 `30a10669…dceaf`, verified unchanged by this
review). This file is this review's only write.

Verdicts use: **CONFIRMED** / **REFUTED** / **OVERSTATED** / **UNDERSTATED** / **UNVERIFIABLE**.

---

## LENS 1 — LOGIC

**L1. P2.3 rests on a category error, and it is the plan's worst logical defect.**
The plan says: *"Stale-synthesis propagation is BUILT and has never run… `supersession_check` …
has a writer (`db.py:1671 add_supersession_check`), a CLI subcommand, and a schema — and 0 rows.
This one needs running and wiring, not building: when a judgment changes, dependent syntheses must
be marked stale."* The writer, subcommand and 0 rows are CONFIRMED. But read the table's own DDL
(`SELECT sql FROM sqlite_master WHERE name='supersession_check'`): it records **per-anchor-source
literature-supersession outcomes** — `anchor_tier`, `outcome IN ('current_best','superseded_by',
'refined_by',…)`, `search_strategy_record`, `check_method IN ('pubmed_search',…)`. It answers
"has a newer *source* superseded this cited anchor?" (DR-2026-05-24). It has no reference to
`specifications`, no judgment identity, no staleness flag on any synthesis row. It **cannot**
mark a synthesis stale when a judgment changes. The S4 trace had this right:
*"Judgment-staleness propagation into synthesis — ABSENT (item 4, Q3)."* The plan's "correction to
an earlier reading" overcorrected: what is built is source-currency checking; the re-entrant edge
P2.3 claims to close remains absent. Running `add-supersession-check` would close nothing and the
plan would record the edge as done. (The actual staleness primitive that exists is
`specifications.derivation_sha` — "staleness check" in its own DDL comment — which P2.2's
comparator could use; P2.3 as written should be struck or rewritten as a genuinely new mechanism.)

**L2. The closing paragraph contradicts P2.2.** *"This plan … adds no new check to the registry"*
— but P2.2 says *"Add one check: for each synthesis, every determination it cites must exist…"*.
Either P2.2 is a registered check (contradicting the closing claim) or an unregistered one
(CLAUDE.md §1: *"an unregistered check is the same defect"*). One of the two sentences must go.

**L3. P2.1's evidence is right, its letter is wrong.** *"`connections_produced` is written only by
data migrations and read by no script in `scripts/` or `tools/`."* REFUTED in letter:
`scripts/db.py:194` (is-mined) SELECTs it and `db.py:225-245` (log-mining) reads, merges and
REwrites it — the CLI is a writer and a reader. What is true, and what the finding needs: nothing
**consumes** the harvested DOIs — no code path moves them toward `source_locators`. The promotion
edge is genuinely absent; "write-only data" is not the accurate description. (`severed-walk.html`
repeats the same overstatement.)

**L4. P1.1's vocabulary prescription contradicts CLAUDE.md §4.** The plan prescribes enforcing
`--evidence-type` from *"the correct list [that] already sits at `db.py:1223`"*. CLAUDE.md §4:
*"Vocabularies come from the schema, not from a list in the code."* Measured:
`evidence_sources.evidence_type` is bare `TEXT`, **no CHECK constraint** — so `check_values()`
has nothing to read, and copying the `add-supersession-check` choices list creates a second
(third, counting the schema's absence) code home for the vocabulary — the rule-5 shape the same
plan condemns in P3.2. The clean fix is one CHECK-constraint migration + `check_values()`. Same
gap, same class: `evidence_sources.tier` also has no CHECK (S6 §8b found this; the plan drops it).

**L5. Everything else in the logic column holds.** P0.1, P0.2, P1.2, P1.6, P2.5, P3.2, P3.3,
P4.2–P4.5 all follow from evidence I reproduced (see LENS 3). P1.5's doctrinal parsing is
correct: `evidence-methodology.md` §2.2 puts "for the target population" in conditions 1 and 3
and not in 2 or 4 — verified against the text at :128-133. The refusal to generalise to T2/Co-2
is right, and the plan's restraint here is the best reasoning in the document.

---

## LENS 2 — SEQUENCE

**S1. The acceptance test depends on a renderer change that sits in NO phase.** The claimed
dependency chain P1.1→P1.5 ends at a rendered page "showing the value AND the sources". Phase 3
("render truthfulness") does not contain the needed fix either — P3.1–P3.4 are room_page,
index.html, register_integrity_check, and a freshness fingerprint. The fix the walk needs
(`spec_page.py` selecting and rendering `value_min/value_max/value_unit` — see LENS 4) is in no
phase at all. This is the hidden Phase-3-shaped dependency of Phase 1 the brief asked about, and
it is real.

**S2. "P1.1 gates P2.1" — right conclusion, wrong mechanism.** The plan's stated reason:
*"dedup via P1.1's two-table check"* and *"promoting 256 leads into a store the writer cannot
dedup against is how duplicates get made at scale."* But the promotion writes `source_locators`
rows, and the plan's own P1.1 text concedes `add-locator` **already checks both tables**
(verified: `db.py` add-locator R9 is two-table; `add-source` at :1992-2000 is one-table). The
promotion itself dedups fine today. The real dependency is admission-side: after promotion, an
un-fixed `add-source` can mint a second identity for a DOI the clue store already holds (OD-5's
unfixed half). Keep the order; fix the stated reason, or a reader will "correct" the order later
on the strength of the bad justification.

**S3. P0-first is prudence dramatised as necessity.** *"the only defect here that can silently
destroy the append-only ledger"* — OVERSTATED. Instrument F4 (done) removed the WAL pragma, so
reads no longer dirty the blob; a stray canonical write dirties `git status`, fails the runbook's
own sha256 discipline, and a committed mutation fails CI's rebuild-and-compare (CLAUDE.md rule 3).
Nothing here is silent end-to-end. P0 first is still right — it is two hours and protects
mid-session state — but it is a seatbelt, not a bomb-disposal.

**S4. P2.4's deferral is justified, not an excuse.** `bpc_metadata` = 0 rows (verified); a
contradiction check now would be a blocking-or-advisory gate with EXAMINED: 0, the §2(a) failure
this repo has produced four times. Correct call, correctly reasoned.

**S5. P1.3 before P1.4 hides that they overlap and that P1.3 is under-specified.** `assess_cell.py`
already writes `specifications` AND `convergence_assessment` AND `gaps` (INSERTs at :525-574).
P1.3's `add-specification` is a second writer for the same table, and its refusal list is missing
the two hardest `validate_evidence_state` rules (see LENS 4, W3). As ordered, a session could land
P1.3, write a cell through it, and fail the blocking battery — with P1.4 later making P1.3 mostly
redundant. State the relationship: assess_cell is the writer that satisfies the gates; the CLI
writer must enforce the same five rules or refuse `stated`/`provisional` outright.

---

## LENS 3 — FACTUALITY

Every load-bearing number and file:line, re-derived. Command shown where it settles the claim.

| # | Claim | Verdict | Evidence |
|---|---|---|---|
| F1 | `is_canonical()` callers = own selftest only; `connect()` never calls it; `db_path()` defaults canonical | **CONFIRMED** | `grep -rn is_canonical scripts/ tools/ schemas/` → dbcore.py:65 (def), :438-439 (selftest) only; `db_path()` at :60 defaults `data/guidebook.db` |
| F2 | Skill lines auditor:185,192,199 / discovery:219 instruct canonical path on write commands | **CONFIRMED** | grep: update-connection ×2, add-gap, add-connection — exactly those four lines |
| F3 | `source_value_extractions`: "no script, no CLI subcommand and no committed migration has ever inserted a row" | **OVERSTATED in letter** | The html's own reproducing command `grep -rlE "INSERT INTO source_value_extractions…" --include='*.py' --include='*.sql' .` returns **five files**, not "no output" — `_archived/scripts/migrations/data_2026071*…data_20260804*.sql` all INSERTed rows pre-reset (GNU grep ignores `.ignore`; only rg hides them). True statement: nothing in the **live tree or live migration chain** writes it, and it holds 0 rows. The substantive finding stands; the verbatim command claim in the html is false as written — §7 trap 1's exact shape, inside the report that cites the trap |
| F4 | Mining: 138 distinct DOIs harvested, 4 in clue store, 134 stranded | **CONFIRMED / off-by-one** | Re-derived from `citation_mining.connections_produced`: 138 distinct; 4 in `source_locators`; 2 in `evidence_sources` (1 overlapping) → **133** in neither, not 134. P2.1's own two-table dedup would promote 133 |
| F5 | Artefacts: 272 DOIs, 16 in store, 256 in neither; `title_short` truncated mid-word | **CONFIRMED exactly** | Re-parsed both `sessions/artifacts/2026-05-24-b11-mobility-*.json`: 272 / 16 / 0 in evidence / 256 neither; sample title ends "…powered wheelchair and sc" |
| F6 | Wave H: all 14 tables referencing `items` key on `item_code`, none on `name` | **CONFIRMED** | `PRAGMA foreign_key_list` over every table: exactly the 14 listed, all `item_code`. `items.name` is NOT UNIQUE (no collision hazard); 3 views (`v_source_reach_all`, `v_item_extractions`, `v_item_provenance`) SELECT `i.name` as display only, never as a join key |
| F7 | Wave H counts 21 / 20 / 41 vs instrument's 42 | **CONFIRMED but incomplete** | 21 matches provenance-walk plan D-5 (2026-08-21) verbatim. But the same 93 names measured **28** numeric / 23 clause / overlap 9 / union 42 in instrument §1.1, and Wave H never reconciles. Digit-test on live DB: 28 names contain a digit. Wave H's net demonstrably misses: **F-04** (`MERV 13+` — absent from the 41-row table entirely), **B-04** (`IEEE 1789-2015 Compliant`), **E-09** (`ISO 23599:2019`), and classes **A-08** (`NC-25 Maximum` — a numeric maximum) as JUDGEMENT with no LEAD flag, so its value is never queued for extraction. Under §1.4 rule 2 ("no value crosses") those values survive the strip |
| F8 | `db.py:1671 add_supersession_check` exists, 0 rows | **CONFIRMED** | call at :1671; `SELECT COUNT(*) FROM supersession_check` → 0. (But see L1: wrong mechanism for P2.3's goal) |
| F9 | `update-bpc` crashes on first INSERT for any slug | **CONFIRMED** | `bpc_metadata.population TEXT NOT NULL`; `_BPC_META_COLS` (db.py:60-66) whitelists `population`; parser (:1039-1052) has no `--population`; INSERT branch (:1775-1782) inserts without it; 0 rows live |
| F10 | `opus_reviewed` hardcoded 0 (db.py:1374), never read; `build_part05` filters on `status` only | **CONFIRMED** | :1374 `"opus_reviewed": 0`; generate_parts.py :250-266 renders PENDING descriptions verbatim; zero readers repo-wide in live code |
| F11 | Census 978 / 92 / 0 / 0 / 126 (+ per-table breakdowns) | **CONFIRMED exactly** | Re-derived every COUNT(*); `jurisdictional_values.value_text/value_numeric` all NULL across 109 rows as claimed |
| F12 | `index.html:7` "91 provisions, 661 evidence sources" vs live 93 / 10 | **CONFIRMED** | items=93, evidence_sources=10 |
| F13 | `register_integrity_check.py` prints "(DB cross-check on)" while the path never executes | **CONFIRMED** | db_rows from 0-row `specifications` (:137-153); `if db_rows:` gate (:182); print at :431; author's own comment :362-366 |
| F14 | add-source: no `--scope`; VERIFIED never sets disposition; I1 blocking | **CONFIRMED** | parser has no --scope and `scope` absent from `_ES_COLS`; VERIFIED branch sets method/attempts only, UNVERIFIED branch alone defaults a disposition; test_db_integrity I1 (:312-318) fails any VERIFIED row not CLOSED |
| F15 | P2.2 "Ten scripts touch both `specifications` and `bpc_metadata`" | **OVERSTATED** | Measured: **8** (assess_cell, validate_pydantic_schemas, population_page, spec_page, generate_parts, test_db_integrity, evidentiary_audit, pipeline_completeness). The substantive claim — none compares, all render/count/audit — holds |
| F16 | P3.1 room_page: "Two wrong names, one file" | **UNDERSTATED, badly** | room_page.py references **six** nonexistent objects: `room` (:26,:29), `room_item` (:35), `room_item_population` (:44,:84), `room_dar_provision` (:66), `room_conflict` (:75), `specification` singular (:51) — and keys on `room_id` where the live `rooms` PK is `room_code`. The two-rename fix leaves it just as crashed. S5's trace already said "two nonexistent tables (room, specification-singular)"; the plan halved even that. Honest option under §1 symmetry: delete or rewrite, not rename |
| F17 | `next_gap_id()` GAP-NNN vs live GAP-B0n-NNN | **CONFIRMED** | :135-144 GLOB `GAP-[0-9]*`; live gap_ids all `GAP-B0#-###` → allocator returns GAP-001 |
| F18 | JurisdictionCode lacks ES/PT/FI; enum inert; `insert_jurisdictional_value` has no jurisdiction vocab check | **CONFIRMED** | enums.py:140-178; only `scripts/validate_jurisdiction.py` imports it, never opens the DB; writer validates item FK + tier band only |
| F19 | Runbook: :794 deleted script; :830 "No CLI" stale; :856-864 abolished dual write citing deleted H03/H04 | **CONFIRMED** | `scripts/audit/table_connectivity.py` deleted in cull commit 80a34d1; `add-candidate` at db.py:823; db.py:394 "admitted_ref_ids intentionally NOT written"; test_db_integrity.py:1038 "REMOVED 2026-08-24 with H03/H04" |
| F20 | html: generators ≈2,630 lines (8.6%), audit+test 11,476 (38%), 63 checks / 4 quarantined, 30,494 LOC, 7,122 trace lines, sha unchanged | **CONFIRMED** | registry: 63/4; find|wc: 30,494; scripts/generate (2,167) + generate_parts.py (463) = 2,630 exactly; audit+tests 11,476; logs wc = 7,122; sha256 matches |
| F21 | html: "Contract covered 13 of 19" | **UNVERIFIABLE as stated** | pipeline-contract.yaml holds 19 criteria, **14** with a named check, 5 `check: null` by direct count. No reproducing command is given for "13" — the one figure in a report claiming "every figure derived at run time" that I could not reproduce |
| F22 | `needs_population_assessment` computed :209, aggregated :421-422, emitted :582, read by nothing | **CONFIRMED** | all four verified in scripts/assess/assess_cell.py; zero external readers |
| F23 | PILOT_CELLS :114-130; argparse --db/--emit-sql/--report-json only | **CONFIRMED** | :115-130; :489-491. ("Crashes twice on live data" accepted from S3's run, not re-derived here) |
| F24 | directness consolidation :225-234; anchoring() admits NOT_ASSESSED/PARTIAL/PROXY | **CONFIRMED** | directness.py: MISMATCH/CONTRADICTED→DISCOUNTED, everything else non-full→DOWN_WEIGHTED; anchoring() (:249-251) excludes only NON_ANCHORING/DISCOUNTED |
| F25 | validate_evidence_state.py:76-110 reads `data/sources/*.yaml`, a directory that does not exist, with a dormant NameError | **CONFIRMED** | the code's own comment at :96-101 admits both defects |
| F26 | Session record: "two of the four [DG-NON items] are now ruled" (plan, scope §1) | **UNVERIFIABLE** | The two ledger entries appended today are the supersession record and `icf_demands` — neither rules any of the four DG-NON items (populations, E-08 figure, jurisdictions, freeze). If two were ruled, the ledger does not show it; rule 0 says the record was owed on contact |

---

## LENS 4 — WALKABILITY (the one that matters)

The plan's test: after P0 + P1, on scratch — *one source admitted → one value extracted with a
locator → one (item × population) cell with governing_refs → one synthesis → one rendered page
showing value AND sources.*

**Verdict: Phase 0 + Phase 1 as specified is NOT sufficient. The walk fails at its final clause,
and wobbles at two middle ones.** Step by step against the live code and schema:

**W1 — Admission (P1.1): passes, with two residues.** log-search → add-candidate → add-source
(--scope added, VERIFIED→CLOSED, vocab, two-table R9) → source_slug_links (written by add-source
--slug, db.py:2033) → search_admissions (written by log-search --admitted-ref-id, :428) →
add-population-match. Residues the plan does not list: **(a)** add-source's
`--verification-method` choices include `corroborated-not-retrieved` and `citing-bibliography`,
both of which blocking **I4** (test_db_integrity:346-352) rejects for VERIFIED rows, and omit
`direct-render` which I4 accepts — a session following the CLI's own help fails a blocking gate
even after P1.1; **(b)** S2's finding that `add-source --dry-run` with `--slug` crashes is not in
the plan.

**W2 — Extraction (P1.2): the row lands, but the promise doesn't.** The schema
(`source_value_extractions`) is writable with the plan's refusals (FK ref_id/slug/item_code,
claim_type CHECK incl. the claimed_value pairing CHECK, mandatory locator). But P1.2's own
rationale — convergence counting values, `v_value_independence` becoming non-zero — requires what
the specified writer does not touch: the view (read its DDL) counts only rows with
`root_type IN ('measurement_primary','participatory_finding','derived_calculation')` AND
(`root_ref_id` set OR `root_id` registered in `external_root_registry`). The plan's add-extraction
names none of `root_type` / `root_ref_id` / `root_id`, and `external_root_registry` (0 rows) has
no writer anywhere. As specified, extractions land and **`v_value_independence` still returns 0**.

**W3 — Judgment cell: reachable only through P1.4, and P1.3 as specified writes gate-failing
rows.** `validate_evidence_state.py` (blocking battery) requires for `stated` AND `provisional` a
**convergence assessment** (:258, :264), and for `provisional` the **confidence flag** (:255).
P1.3's refusal list has neither — it names governing_refs, code-floor, and the T3 cap only, while
claiming to "implement what validate_evidence_state.py currently only detects". There is **no CLI
writer for `convergence_assessment`** and P1.3 does not add one. A cell written through
add-specification as specified fails the blocking battery on arrival. The walk survives only
because P1.4's `assess_cell.py` writes `convergence_assessment` + `specifications` + `gaps`
together (:525-574) — the plan never states that this is the only gate-clean path.

**W4 — The value never reaches the cell.** `assess_cell.py` INSERTs
`value_min, value_max, value_unit` as literal `None, None, None` (:561); nothing computes them
from `source_value_extractions`; P1.3's add-specification does not name them. The cell the walk
produces carries **no value**.

**W5 — The renderer cannot show a value at all.** `spec_page.py`'s cell query (:74-77) selects
state/tier_basis/flags — **not** `value_min/value_max/value_unit`; `grep -n value
scripts/generate/spec_page.py` returns nothing; the rendered table has no value column. Sources
DO render (the :98-105 join through `specification_source_links` exists — P1.3's link writer is
necessary and sufficient for that half). So after P0+P1 exactly as written the walk ends at: a
rendered page showing state, tier and sources, **no value anywhere on it** — failing the plan's
own acceptance sentence and §4's "one answered question" (a question answered without its value is
not answered). Also: nothing regenerates the page — `regenerate_derived.sh` covers only the three
`tools/` writers; `build_site.py` (advisory `site_pages_fresh`) or per-item `spec_page.py` must be
invoked by hand, which the plan nowhere says.

**What must be added to Phase 1 for the walk to complete:** (1) value fields on the judgment
writer — either add-specification takes `--value-min/--value-max/--value-unit` or assess_cell
derives them from extractions; (2) `spec_page.py` selects and renders the value tuple; (3) P1.3
refuses `stated`/`provisional` without a convergence row + confidence flag, or the plan states
that assess_cell is the sole sanctioned judgment writer; (4) add-extraction exposes
root_type/root_ref_id (and an `external_root_registry` path) or P1.2's convergence rationale is
withdrawn; (5) I4-consistent `--verification-method` choices. With those five, the walk closes;
without them it provably does not.

---

## LENS 5 — THE TWO LEDGER ENTRIES

**Supersession record.** Scope is honest and deliberately narrow: one session, one purpose, RULE
unamended, future citation forbidden, batch-1 pass still owed. Quotes of the 2026-08-19 RULE's
limbs and clause (5) are verbatim-accurate against project-standards.md:638-640. Two defects:
**(a)** THIS review falls outside it. The record covers "establishing whether the pipeline can
carry a mobility batch"; this pass — an adversarial review of plans, a census, a session record
and the ledger, commissioned hours later — is limb-(a)/(b)-outside AND a pass on a pass AND not
named by the record. It is lawful the same way the session was (live owner instruction, rule 0),
which means a supersession record for it is owed **now** and does not exist. The per-session
scoping strategy manufactures a fresh recording debt on every further owner instruction — worth
saying in the record itself. **(b)** WALK-REPAIR-PLAN sits outside the recorded scope in letter:
the RULE's ACTION (3) forbids a pass to "schedule remediation", and the record's stated purpose is
investigation, not repair planning. The plan's own defence ("a repair list, not a
plan-instrument", scratchpad not workplan/) is a location argument against a substance rule.
Either the record names remediation-scoping as within the owner's directive (it plausibly was —
"scope it, don't execute") or the plan is unauthorised paper. One sentence fixes it; unfixed, it
is the same omission the record itself confesses to.

**`icf_demands` RULE.** The measurements: 17/17 rows CONFIRMED; 21-row map, 15 distinct codes per
side, `A-REACH`→3 CONFIRMED; `axes` carries `icf_b_anchors`+`icf_d_anchors`+`mechanism`
CONFIRMED; `access_needs` carries `design_obligation` CONFIRMED. The fold-refusal is correct and
well-grounded: the two tables carry opposite sides of the social-model relation and the
many-to-many map is real structure, not duplication. Three defects: **(a) the citation is wrong —
there is no §R6 in DR-2026-08-24.** The axis ruling is **§R8** (the DR runs R1, R2, R8, R7); the
"two items left NOT DECIDED" and "item 1"/"item 3" all live in R8's decided/not-decided list. An
operative ledger entry pointing at a nonexistent section, three times, on the day rule 4b was
written about exactly this class of miss. **(b)** "the b/d ÷ e split is the social model expressed
in the schema" is 88% true: `access_need_icf` holds **5 non-e anchors** (A-PRECISION b765;
A-SELFCARE d510/d540/d550; A-TIME b164) against 38 e-anchors. The refusal survives the exception
rows easily — but a RULE recording a measurement should record them. **(c)** "'Axis' asserts an
orthogonal scalar dimension" — the non-orthogonality of AX-AMB/AX-WHM (alternatives, simultaneous
for part-time users, opposed on gradient) is factually right and the tie to the permitted-umbrella
test's "opposed **or** orthogonal" wording is sharp; but "asserts" states as semantic fact what is
an argument about connotation. Mild overreach, harmless because the operative content (rename +
no-fold) is the owner's ruling, not the metaphor critique. The rename-remains-gated clause
correctly preserves R8 item 3.

---

## WAVE-H-SCOPE — the specific checks asked

- **Referential integrity claim: CONFIRMED** (F6). No view, trigger or index keys on `items.name`;
  no UNIQUE on name; the three views carry it as a display column that re-resolves after a data
  migration.
- **But the caller sweep is incomplete.** Non-archived surfaces carrying determination-bearing
  item names that the sweep does not list: **`data/question-headings.yaml`** (hand-authored
  2026-05-03, titles like "Acoustic Ceiling Panels (NRC ≥0.85)", read by `tools/evidentiary_audit.py`),
  `references/toc.md`, `references/part04-item-index.md`, `skills/question-author_SKILL.md:70`
  ("Corridor Clear Width ≥1200mm"), `schemas/item.py:33` (docstring example), `working/pilot/*`.
  None breaks the migration; all go prose-stale against it (§2(b)).
- **Step 3 of "what executing it would be" is unwalkable as written.**
  `scripts/regenerate_derived.sh` regenerates only `tools/pipeline_completeness.py`,
  `tools/evidentiary_audit.py` and the vetting surface — it does **not** touch `site/specs/`
  (that is `scripts/generate/build_site.py`, whose freshness check `site_pages_fresh` is
  **advisory**), nor `parts/`, nor `index.html`. Run as written, the confirmation in step 3
  ("`site/specs/e-08.html` `<h1>` no longer carries a figure") **fails** — the file would be
  untouched. The recipe needs build_site.py + generate_parts.py + the index regeneration named
  explicitly.
- **The three tests leak values** (F7): F-04's `MERV 13+` is outside even the 41-row wide net;
  A-08's `NC-25` is inside the table but flagged JUDGEMENT-only, so no lead is queued for it.
  Both violate the quoted rule's "no value crosses" if Test A or C is executed as scoped. Also the
  block-quote of the provenance-walk rule silently drops "The 21" from "The 21 embedded values" —
  a small unmarked elision in a quoted ruling.

---

## DROPPED DEFECTS — plan vs the S1–S6 traces

Code-only findings in the traces that appear in neither the plan nor the session record's
"Deferred deliberately" list (which covers only reasoning_doc_citations, attestation window,
contract prose, doctrine_recheck, R8):

1. **`add-population-match` same-session divergent-grade crash** (S2 case 24). The dissent
   mechanism CLAUDE.md §4 celebrates as deliberately duplicate-friendly crashes in practice on the
   id mint. Directly relevant to the batch's adversarial pass.
2. **`adjudication_integrity.py` exit code does not reflect its own FAIL verdict** (S2 case 30) —
   a gate that cannot fail; §2(a)'s exact shape.
3. **`source_locators.jurisdiction`: 818 of 875 values are not jurisdictions, no check reads the
   column** (OPUS D-7, S1) — for a batch "driven from the clue store" by jurisdiction buckets,
   the bucket filter is unusable and nobody recorded deciding that's acceptable.
4. **`spec_value_probes` + `items.pmp_*` have no writer while the progressive-measurement skill
   teaches raw INSERT** (S1/S3) — every mobility item is a quantity; probes are the vetting path.
5. `add-source --dry-run` + `--slug` crash (S2 case 4).
6. `log-search --deferred-reason ""` silently miscounts as deferred (S1).
7. `validate_reasoning.py` exits 0 on a nonexistent slug and on real errors without `--strict` (S4).
8. `context_map.py --check` currently red/stale (S5) — a live red advisory the plan's P3 doesn't list.
9. `retired_vocabulary_audit` EXAMINED 26 of 66 live occurrences (S6).
10. `evidence_sources.tier` has no CHECK — same class as the evidence_type gap P1.1 fixes (S6 §8b).

Some of these legitimately fail §1's burden-of-proof bar for batch 1 — but the plan's own standard
(P2.4, and the session record's Deferred section) is that a deliberate deferral is *recorded*.
Items 1–4 have batch impact and no recorded disposition anywhere.

## CONTENT WEARING A CODE COSTUME

Checked every plan item against §1's owner-gate list. **P1.5** is an interpretation of ratified
text executed as code — the text genuinely supports it (verified), and the C-5 correction trail
shows the question was asked; legitimate. **P2.5's "make it real" arm** quietly sets policy (must
connections be Opus-reviewed before rendering Part 5?) that no ratified record states; the
**delete** arm is pure code. If P2.5 is executed as "make it real", that is a routing-doctrine
decision and should be flagged to the owner; as deletion it needs nobody. Everything else in the
plan is genuinely code. Wave H itself is correctly held as owner-gated content — the provenance
plan's own words ("owner-gated because item identity is content") survive Wave H's
integrity-measurement correction, and Wave H does not claim otherwise.

---

## TOP THREE CHANGES REQUIRED BEFORE EXECUTION

1. **Close the value path or stop claiming the walk.** Add to Phase 1: value fields on the
   judgment writer (or assess_cell deriving them from extractions), `spec_page.py` rendering the
   value tuple, and the regeneration step. Without these the plan's own acceptance test is
   unpassable by construction (W4/W5) — and no checklist in the plan would notice, which is this
   repository's signature failure transplanted into its repair plan.
2. **Rewrite P2.3.** `supersession_check` is source-currency tracking, not judgment→synthesis
   staleness (L1). As written, the plan runs the wrong mechanism and marks the re-entrant edge
   closed. Either build the propagation P2.3 describes (via `derivation_sha` + the P2.2
   comparator) or record the edge as ABSENT, as S4 correctly had it.
3. **Complete P1.3's refusal list** (convergence assessment + confidence flag, or declare
   assess_cell the sole writer) and fix the I4 verification-method mismatch — otherwise the first
   honestly-admitted, honestly-judged cell still fails the blocking battery, which is the exact
   condition (green-path unreachable → hand SQL) that produced the 2026-08-19 fabrication.

Also owed before anyone executes: correct §R6→§R8 in the `icf_demands` RULE; extend the
supersession record to name this pass and the repair-planning activity; fix P3.1's scope (six bad
references, not two — or delete room_page.py); reconcile or annotate Wave H's 21/41 against the
instrument's 28/42 and catch F-04/A-08's values; correct "read by no script" (L3), "134 stranded"
(F4), "ten scripts" (F15), and the html's false "→ no output" grep claim (F3).

## VERDICT BY LENS

1. **LOGIC:** Sound except P2.3 (category error, must be rewritten), the P2.2-vs-closing-line
   contradiction, and P1.1's rule-5-violating vocabulary prescription.
2. **SEQUENCE:** Order mostly right; P0-first is prudence not necessity; P1.1→P2.1's stated
   mechanism is wrong though the order is right; the fatal sequencing fact is a renderer
   dependency assigned to no phase.
3. **FACTUALITY:** Strong — 19 of 26 spot-checks CONFIRMED exactly, several to the digit. The
   misses are characteristic: counts inflated in the plan's favour (10-vs-8, 134-vs-133,
   "no output" that outputs, "read by nothing" that is read) and one systematic undercount
   (room_page). Nothing fabricated; several things rounded toward the thesis.
4. **WALKABILITY:** **Phase 0 + Phase 1 as specified does NOT produce the walk.** Sources render;
   the value never reaches the cell and could not render if it did. Five named additions close it.
5. **RULINGS:** Supersession record honest but already outgrown (doesn't cover this pass or the
   plan); `icf_demands` RULE correct in substance, wrong in its §R6 citation, slightly overstated
   on the b/d÷e purity and the orthogonality claim.

The plan is worth executing — after change 1–3. Its core diagnosis (the sever at
`source_value_extractions`, the flag-sized evidence gaps, the dead safeguards) survived every
check I threw at it. What did not survive is its acceptance test: the plan, like the pipeline it
repairs, currently ends one column earlier than it looks.
