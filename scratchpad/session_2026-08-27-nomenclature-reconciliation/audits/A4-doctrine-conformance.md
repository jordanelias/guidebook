# A4 — Doctrine conformance audit (adversarial)

Audited 2026-08-27 against `data/guidebook.db` at `user_version` 64, HEAD = `8dc74bd`.
Range audited: `fced925..8dc74bd` — **nine commits, not eight**: `8dc74bd` (02:55) landed while
this audit was running, adding a THIRD 2026-08-27 ledger entry and rewriting NOMENCLATURE L.3
(877 → 912 lines). Everything below is stated against the state at `8dc74bd`.

Verdict summary: the session's measurements against the DATABASE are almost uniformly accurate
(38/38 row counts, the 41/39 FK split, the seven-target distribution, and the zero-inbound-key
finding all reproduce exactly). The breaches are concentrated where the project's rules say its
failures always are: hand-written counts outside the DB pin, claims about the record rather than
the database, attribution of agent design to owner rulings, and the same fact written into
multiple homes.

---

## BREACHES, in decreasing order of seriousness

### B1 — Rule 4b / owner-ruling contact failure, inside the session (acknowledged, owner-forced)
The session reported *"nine of 93 item names carry a quantified determination"* as a finding
(commits `563ff8e`, `9bb8ce6`; NOMENCLATURE L.3 as committed at 01:55) and used **E-08** as its
worked example — twice. The ratified instrument (`decisions/DR-2026-08-19-...md:127`), which
CLAUDE.md instructs every session to read FIRST, had already measured the property a week earlier
(28 numeric · 23 prescriptive · overlap **9** · 42 distinct, "and 42 is a floor"): the session's
"nine" is the instrument's OVERLAP figure, re-derived by an invented regex and misdescribed. E-08
is separately ruled against on the record (`RATIFICATION-PACKAGE-2026-07-12.md:47`,
`DR-2026-08-12-...md:69`) and the owner had said in this same session it *"has been ruled against
for like a month now."* The correction (`8dc74bd`, ledger entry 3) was **owner-forced** (*"yet
again e-08.html appears despite me having ruled it doesn't exist a million times"*), not
self-caught. Commit messages `563ff8e`/`9bb8ce6` carry the wrong figure and the E-08 example
permanently. This is the exact failure class rule 4b records — searching the database and not the
record — committed by the session whose subject was rule conformance.

### B2 — The session's own new standing ACTION is violated by its own document at HEAD
Ledger entry 3, ACTION (4): *"Do not use E-08 as an example of anything."* At `8dc74bd`,
NOMENCLATURE still uses E-08 as the worked example at **lines 659** ("And the failure is already
shipped: `site/specs/e-08.html` headlines..."), **685** ("the gate that would have caught
`e-08.html`"), and **903** ("an `e-08`-class page edit"). `8dc74bd`'s message claims "Part K's
cross-reference fixed"; its diff touches only L.3. Lines 806–862 legitimately name E-08 (they ARE
the correction record); 659/685/903 are example-usage and stand uncorrected.

### B3 — Rule 0 lens: attribution expansion — agent design folded under the owner-ruling banner
`CLAUDE.md` (edit in `c94a715`): **"Every stage's hand-off object is `<stage>_items`, and the
hand-off is a NOT NULL foreign key. Owner ruling 2026-08-27."** The ledger entry's header makes
the same move: *"Owner ruling 2026-08-27, two parts, both quoted"* — but both quoted owner
statements cover NAMING only ("just call them whatever their stage is and add -item"; "we just
append '-item'"), and the separately quoted cardinality statement covers CARDINALITY only. The
NOT NULL / foreign-key / junction mechanics are agent design (the entry itself proves this: "I
first recorded all five hand-offs as NOT NULL columns. That is wrong for two of them" — an owner
ruling would not need the agent's own correction). The owner's recorded selection is *"the rename
creates the spine"* — timing, not key shape. CLAUDE.md's compressed sentence attributes the
mechanism to the owner. This is the mild form of the invented-directive failure mode Rule 0's
history records; the fix is one clause distinguishing "owner ruled the spine lands at rename"
from "the key shapes are the session's derivation from the quoted cardinality."
Minor same-lens fault: the `-item` quote is rendered with different punctuation in the two
records — ledger: *"for item — we just append '-item'"*; NOMENCLATURE: *"for item. we just
append '-item'."* Two variant renderings of one verbatim owner quote.

### B4 — Rule 5 lens: a live same-fact-in-two-columns instance, missed on the very table the
### session "Verified" the same day
`evidence_population_match` carries BOTH `source_ref` and `ref_id`; measured: **identical in all
25 rows** (`SUM(source_ref=ref_id)=25`). The session wrote "Verified 2026-08-27:
`evidence_population_match` carries no UNIQUE beyond `match_id`; 25 rows across 10 sources" —
true, and the verification pass looked straight past the dual home on the same table. Consequence
for the document: C.2's **"Seven column names for one referent"** is an undercount — `source_ref`
is an eighth (single-value, 25 live rows), and the packed-list columns (`admitted_ref_ids`,
`superseding_ref_ids`, `governing_refs`) are also uninventoried beyond `used_in_bpcs`.

### B5 — §2(b): hand-written counts that are wrong, in the document that condemns them
NOMENCLATURE carries a date stamp and a DB pin ("measured against `data/guidebook.db` at
`user_version` 64") — but no drift warning, and the pin cannot cover its many non-DB counts.
Wrong today, at the pinned version where DB-derived:
1. **"`jurisdiction`, on 9 tables"** (C.3) — measured: **11 tables** carry a `jurisdiction`
   column (evidence_sources, search_coverage, term_aliases, lang_jur_map, jurisdictional_values,
   search_executions, economics_entries, source_value_extractions, reasoning_doc_citations,
   reference_stubs, source_locators).
2. **"nine of 93"** — see B1; wrong at commit time, corrected only on owner contact.
3. **"30 carry a name fault"** (commits `d354550`, `de6bdea`: "the 30 name faults marked"; and
   the withdrawal narrative "a hand-written count of 35 name faults where the table holds 30") —
   the Part E register held **29** dagger-marked rows at `d354550` and holds **31** at HEAD. The
   corrected count was wrong when written and has drifted since — §2(b) reproduced inside the
   correction of a §2(b) fault.
4. **"`site_pages_fresh` ... advisory, and nothing calls it"** (L.2 table; repeated in
   `9bb8ce6`) — FALSE. `.github/workflows/ci.yml:251` runs `--battery render` on every gated
   run, and `site_pages_fresh` is registered in that battery. The true claim is narrower: no
   REGENERATION script invokes `build_site.py` (`regenerate_derived.sh` omits it). As written it
   erases the fact that the check has been running and its advisory results visible.
5. Notation: "`REF-VERIFIED-001` … `-012`" implies twelve; the count stated (11) is correct —
   `-008` is absent. The range notation invites the wrong count.
Unverifiable as stated (no method, no date, outside the pin): "23 literal-string lines in
spec_page.py, 14 ..., 11 ..." (no definition of a literal-string line); "272 mobility DOIs of
which 256 in neither store" (prior-session OpenAlex pass, carried); "retired population codes
live only in 12 skill files". Verified correct (sample of ~30): 66 tables / 33 zero-row / 18
views / 80 FKs = 41 cross + 39 within with exactly the claimed seven-target distribution /
5,318 rows splitting 4,122·1,087·92·17·0·0·0 / 875·10·4·6 REF namespace / 1,044 · 39 · 372
Part-J.3 sums / 49 skills (50 entries minus `deprecated/`) / 359 archived migrations / 33 data
migrations / 2 bpc-reasoning files / 138·4 mining DOIs / 0 non-null jurisdictional values / 16
`bpc_metadata` columns as listed / 23 `search_executions` columns incl. `mining_direction` /
`regenerate_derived.sh` 7×/0× / e-08.html h1 line 53 vs "not yet computed" line 92 /
build_site.py:14 stale comment (93/93 pages exist) / DR:127 carries 28·23·9·42 as quoted.

### B6 — §2(b) in CLAUDE.md itself: the edit leaves the file contradicting the machine
The `c94a715` edit makes the pipeline section state SIX stages while leaving intact the
paragraph **"The machine enforces this spine, and as of 2026-08-25 it enforces it under these
names: `governance/pipeline-contract.yaml` (the single home of the stage ids)..."** — measured:
the contract's `stages:` lists FIVE (research, evidence-collection, judgment, synthesis, render;
no `specification`), and `tools/pipeline_completeness.py:37` `STAGES` likewise. The machine
enforces the superseded spine; CLAUDE.md now asserts it enforces "this" (six-stage) one. The
ledger ACTION records the pending contract change — correctly — but CLAUDE.md was edited around
that sentence without touching it, so prose contradicts the database's enforcing machinery
today. Additionally the edit hardcodes fresh volatile counts ("**SEVEN** views", "All **41**
cross-stage keys", "zero inbound keys ... one each") into a file that says of itself "This file
hardcodes none." The view list carries a date and an owed-re-derivation warning (the §2(b)
escape hatch); the 41 carries a date only; the "hardcodes none" sentence is now false as
written.

### B7 — The "SEVEN cross-stage views" figure rests on an unstated definitional switch
Reproduced: under the bucket definition the FK analysis uses (substrate counts as a bucket, and
any two-bucket join "crosses a boundary"), exactly seven views span two buckets — the number is
internally consistent with the 41-FK derivation, and the v_divergence correction is right
(specifications + convergence_assessment are both judgment under the five-stage map). BUT
CLAUDE.md's own protection rationale defines the protected object as "a view that joins TWO
STAGES," and the same section says "Substrate is not a stage." Under that stated definition the
count is **FIVE**: `v_item_extractions` reads source_value_extractions + evidence_sources (both
evidence-collection) + `items` (substrate), and `v_coverage_priority` reads search_executions
(research) + slugs + lang_jur_map (both substrate) — neither joins two stages. Counting
`items`-joins as cross-stage requires resolving the very question the session's own d354550
commit lists as OPEN ("the 2026-08-26 ruling ... re-classifies all 10 foreign keys that target
it"), or requires the substrate-bucket definition, which is nowhere stated. A number that
changes with an unstated definition is now hardcoded in CLAUDE.md.

### B8 — Rule 5 lens: the ruling and its measurements are now in four homes
The six-stage list: CLAUDE.md (quote + table) · project-standards RULE (quote + table) ·
NOMENCLATURE Part A (table) · the published artifact — plus `pipeline-contract.yaml`, the
declared "single home of the stage ids," which still says five and therefore DISAGREES with all
of them today. The hand-off/cardinality table appears near-verbatim in the ledger AND
NOMENCLATURE Part B; the zero-inbound-FK measurement table in the ledger, NOMENCLATURE, and
(prose form) CLAUDE.md; the seven-view list in CLAUDE.md and NOMENCLATURE Part H. NOMENCLATURE
says "Both are in `references/project-standards.md` ... with their quoted wording" and then
restates both in full. The ledger is the record home and CLAUDE.md is by design a map — but
duplicating the volatile MEASUREMENTS (41, seven, zero/one inbound) rather than pointing at the
ledger entry recreates the drift surface rule 5 exists to remove, and B5.3 shows the drift is
not hypothetical. `stage_id[:3]` is genuinely one derivation (a function, not a lookup table),
but its six outputs are written out literally in at least three places; checkable, so marginal.

### B9 — §1 burden of proof: two of the five additions never state what reaches the book
Judged in §1's own terms ("state what wrong thing reaches the *guidebook* if it does not
exist"):
- **vocabulary check** — PAYS: 42 determinations asserted in labels with no determination
  behind them, shipped to the reader (post-correction framing; pre-correction it said nine).
- **`site_pages_fresh` promotion** — PAYS (a hand-edited reader-facing page becomes
  uncommittable) — but the proposal never engages the registry's RECORDED reason for advisory
  status ("Advisory until the committed-vs-generated policy is settled"), and its premise
  "nothing calls it" is false (B5.4). Promotion without addressing the recorded condition is
  the inverse of arguing paperwork against a ruling: ignoring recorded reasoning unexamined.
- **`figures`** — PAYS, in book terms: a value-encoding figure drawn by hand is a second home
  that drifts against the determination the reader sees, and `text_equivalent NOT NULL` is
  justified by the book's own subject.
- **`ren_items`** — MARGINAL: justified primarily as "makes K.3's gate possible" (apparatus),
  though the book harm (a page claim that traces to nothing) is stated in K.3's testable form.
- **`jud_items`** — FAILS as written. Justification is entirely structural ("the spine",
  "its absence is why the extraction table could sit ... unwritten without anything noticing").
  Nowhere does it state what wrong thing reaches the guidebook — the obvious candidate (a
  determination built on ungraded, unweighed extractions) is never written down.
- **`syn_judgment_links` / `spe_synthesis_links` (and J.2's `syn_synthesis_links`)** — FAIL as
  written. Justified by "the walk itself has no keys, which is why it does not walk" —
  apparatus language throughout; the book harm (a rendered determination that cannot name the
  judgments behind it, hence cannot be contested or re-derived) is inferable and never stated.

### B10 — §0.4 lens: the caller enumeration for retiring `items` is materially incomplete
The proposal is explicit that no sweep has run ("Nothing is renamed ... no caller is swept"),
so §0.4 is not yet violated — but Part G's caller list, which prices the change, misses most of
the callers of the one table retired OUTRIGHT. Independently derived caller set for `items`
(93 rows):
- **3 views**: v_item_provenance, v_source_reach_all, v_item_extractions (Part G says "18
  views, 7 cross-stage" generically; never names which read `items`).
- **16 Python files**: scripts/generate/build_site.py (walks `items` to build every page),
  spec_page.py, population_page.py, generate_parts.py, pilot_renderings.py,
  scripts/validate_items.py (a registered check NAMED for the table), scripts/db.py,
  scripts/audit_consolidator.py, scripts/audit/{graph/extract_db,migration_reproducibility,
  pmp_audit,graph_audit}.py, scripts/tests/{test_db_integrity,test_evidence_cell_state_2_3,
  test_validate_evidence_state_2_4}.py, tools/{pipeline_completeness,evidentiary_audit,
  regenerate_vetting_surface}.py. Part G names db.py/dbcore/schemas and
  pipeline_completeness.py; it never mentions the generators, the validator, the audit
  scripts, or the tests.
- **22 skills** name `items` (Part G says "the skills" — adequate as a category).
- **4 governance YAMLs**: check-registry.yaml, context-map.yaml, pipeline-map.yaml,
  retired-vocabulary.yaml — Part G names only check-registry and pipeline-contract.
- **Registry checks whose subject is `items`**: validate_items (advisory), site_pages_fresh
  (EXAMINED = pages built from `items`), evidentiary_audit_fresh.
- **Data migrations**: no committed `data_*` INSERTs into `items` (rows come from baseline
  057), so the rule-5 drop constraint routes through the baseline path Part I correctly
  proposes.
Sharpest internal contradiction: **L.6 step 1 promotes to blocking a gate whose EXAMINED corpus
is built by walking `items`, while Part E retires `items` outright** — the proposal never
reconciles the two, and executing them in the written order (promote first, rename later) makes
the rename a blocking-gate change nowhere flagged as one.

### B11 — §2(a) lens: the proposed vocabulary check specifies no EXAMINED and no floor
§2(a): every check must print `EXAMINED: <n>`; the registry carries `min_items`/`no_floor` per
check. The vocabulary-check proposal (L.3/L.6, re-scoped by `8dc74bd`) specifies neither, and
its subject (`items.name`) is the table the same document retires — subject continuity across
the rename is unaddressed. `site_pages_fresh` itself is already instrumented (EXAMINED = page
rows, `min_items: 1`, mutation-tested — registry note), so its promotion is NOT vacuous-prone;
the proposal never checks or states this, but the outcome is compliant.

---

## Per-lens verdicts

| # | Lens | Verdict |
|---|---|---|
| 1 | Rule 0 — supersession on contact | **BREACH** (B1 in-session rule-4b/ruled-against-example failure, owner-forced correction; B3 attribution expansion; quote-rendering variance). Recording itself: done — three ledger entries, quotes present, supersessions named, no paperwork argued against a live ruling; conceptual-model.md cited as corroboration only. |
| 2 | Rule 5 — point, do not copy | **BREACH** (B4 live dual column missed on the "verified" table; B8 four-home duplication of the ruling and its volatile measurements; contract-vs-CLAUDE.md stage-list disagreement live today). |
| 3 | §2(b) — hand-written counts | **BREACH** (B5: two false DB-derived counts, one false process claim, a count wrong-then-drifted in its own correction; partial stamp only — DB pin covers a fraction of the figures; no drift warning). |
| 4 | §1 — burden of proof | **BREACH in part** (B9: jud_items and the three junctions never pay in §1's terms; figures and the vocabulary check pay; site_pages_fresh pays but ignores the recorded advisory condition; ren_items marginal). |
| 5 | §0.4 — caller sweep | **BREACH as enumeration** (B10; no sweep yet owed since nothing executed, but the priced caller set omits the generators, validator, tests, audit scripts and two YAMLs, and the promote-then-retire contradiction is unflagged). |
| 6 | §2(a) — vacuous gates | **BREACH in part** (B11: new check unspecified; promotion target verified instrumented and safe). |
| 7 | The session itself | **OPEN, obligations pending** — see verdict below. Rule 1: all nine commits comply with `{skill}: {action} [ts]`. Rule 6: complied (nine scratchpad commits across the session; the Bash-log misfiling into the 2026-08-25 scratchpad is the hook's stale-stem trap, recorded twice by the author, and the append-only log was correctly left where it landed). `references/project-standards.md` change is append-only (0 deletions). |
| 8 | Claimed verifications | **BREACH in part** (B1 "nine" claimed measured and wrong; B5.4 "nothing calls it" false; B7 "re-measured ... SEVEN" true only under an unstated definition; B4 the same-day "Verified" pass missed the dual column it was touching). The core DB measurements — 41/39, seven targets, zero inbound hand-off keys, three forward pointers incl. one substrate→evidence, every row count — reproduce exactly. |

## Session record and attestation verdict
- **A session record is owed.** `scratchpad/session_2026-08-27-nomenclature-reconciliation/`
  exists and `sessions/session_2026-08-27-nomenclature-reconciliation.md` does not — by
  CLAUDE.md §7's own derivation the session is OPEN and must close with a record.
  `sessions/LATEST` (currently the 2026-08-25 session, correctly) must move at that close;
  `sessions/LATEST-RESEARCH` must NOT (no research was done).
- **An attestation is owed at close, not yet.** Nothing committed so far touches a rule-2 path
  (`CLAUDE.md`, `references/project-standards.md`, `scratchpad/` are not
  `references/bpc-reasoning/`, `references/connection-reasoning/`, `decisions/` or
  `sessions/`). Writing the session record into `sessions/` triggers rule 2, so the close-out
  commit owes `attestations/<slug>.json` against `schemas/attestation.schema.json`.
- Note for whoever closes: the session was still committing while under audit (`8dc74bd` at
  02:55; NOMENCLATURE 877 → 912 lines); this report is stated against `8dc74bd`.
