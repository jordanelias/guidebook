# A2 — Adversarial audit: logic and sequence

Subject: `NOMENCLATURE.md` (Parts A–L), the two 2026-08-27 RULE entries in
`references/project-standards.md` (from :1445), and the CLAUDE.md pipeline edits in commit
`c94a715`. Every figure below re-measured against `data/guidebook.db` (user_version 64, read-only)
on 2026-08-27. Findings ranked: **BREAKS** (the proposal cannot ship as argued), **WEAKENS**
(argument survives only after repair), **DEFECT** (wording/consistency).

The base measurements largely reproduce: 66 tables, 18 views, 80 FKs, 875/10/4/6 REF overlap,
0/109 non-null in `jurisdictional_values`, `term_aliases` PK `(term_id, alias, language)`,
`bpc_metadata` PK `slug`, `site_pages_fresh` advisory (`governance/check-registry.yaml:1359`),
`regenerate_derived.sh` covering `tools/` only. **One measurement is wrong (B1 below), and most of
the damage is in the inferences, not the arithmetic.**

---

## BREAKS

### B0. The cardinality table contradicts the owner quote it stands on — in both directions — and the contradiction is resolved by weighing a DR against a live ruling (rule 0)

The owner's quoted statement (`project-standards.md:1523`):

> "research produces many rows of evidence from one slug. **each row of evidence provides one row
> for judgment.** one-to-many rows of judgment provide one row for syntheses. one-to-many rows of
> syntheses provide one row for specifications."

Three problems, escalating:

1. **evidence → judgment.** The owner says 1:1. The doc and the RULE record **1:N**
   ("deliberately not UNIQUE"), justified by `DR-2026-08-19 §7`'s dissent mechanism. That is a
   prior ratified record weighed against a live owner statement — the move rule 0 exists to
   forbid, and rule 0's own text says the job is to *record the supersession*, "never to weigh the
   ruling against the paperwork it changes." The conflict is not even flagged: "1:N — normally
   1:1; see dissent" presents the deviation as harmonious. Rule-0-compliant handling was: record
   1:1, surface the collision with the dissent design, put it to the owner. The dissent case may
   well win — but that is the owner's call, and the doc made it silently. Note also the analogy is
   weaker than claimed: `evidence_population_match` (the "verified" precedent) keys `ref_id` →
   sources, not extractions; its dissent pattern is a different edge entirely.

2. **judgment → synthesis.** The owner says N:1. The proposed junction `syn_judgment_links` with
   no UNIQUE on `judgment_item_id` implements **M:N** — and the doc *argues for* that surplus:
   the back-pointer is rejected partly because it would "forbid one judgment feeding two
   syntheses," a capability the quoted ruling does not grant. So the same sentence's clauses are
   read as law where they support the design (junctions at the pivot) and as loose description
   where they don't (1:1, N:1). Selective literalism.

3. **The third option the doc never considers**: a junction **with `UNIQUE(judgment_item_id)`**.
   It expresses the owner's N:1 exactly, is written by the downstream stage (no write into a
   completed stage), and keeps every guarantee the doc wants from the junction. The
   back-pointer-vs-junction dilemma is false; the doc compares its preferred shape only against a
   strawman. (Symmetrically: the doc is emphatic that UNIQUE must be *absent* on
   `jud_items.evidence_item_id` but never asks whether UNIQUE should be *present* on the junction
   side to honour the ruling.)

And the enforcement claim over-sells: "**the hand-off is a NOT NULL foreign key**" (RULE headline)
is true only for the two fan-out columns. "≥1 per synthesis" is **not expressible as DDL in
SQLite** — no declared constraint makes a junction row exist. The fan-in half of "the rename
creates the spine" is a trigger or a gate that the doc never specifies, i.e. currently aspiration.
"A NOT NULL key added now is DDL" (Part B, I.7) is only half the spine.

### B1. The RULE's headline attributes to the owner a ruling the quotes do not contain

`project-standards.md:1486`: "Every stage's hand-off object is named `<stage>_items`, **and the
hand-off is a NOT NULL foreign key**. Owner ruling 2026-08-27, two parts, **both quoted**." The two
quotes that follow are entirely about *naming* ("just append '-item'"). Neither mentions keys,
foreign or otherwise. The key half rests on an unquoted paraphrase — "Owner ruling, same day,
selecting *'the rename creates the spine'* over deferring it" — where the quoted phrase is the
agent's own option text, not owner wording. Further out on the same limb:
**specification → render N:1** appears in the cardinality table as if ruled; the owner's quote
stops at specifications and says nothing about render. And it is almost certainly wrong on the
merits: one specification appears on many surfaces (its own page, a room page, an index) and one
surface draws on many specifications — K.5's own "junctions naming what it draws on" concedes M:N.
Rule 0's history note names this exact failure class ("an agent invented an owner directive that
was never given and built a 531-row table on it"). The naming ruling is genuinely recorded; the
keyed-spine and the render cardinality are design promoted to ruling. One more thread for the
owner: the quote itself says "an 'item' in evidence is just under **column** called… evidence-item"
— the owner said column; the doc built tables. Probably fine, but it is an interpretation and
should be marked as one.

### B2. Part J refutes Part E, and the document ships both

Part J.4's rule — *new table only for a new ROW-KIND; provenance is a COLUMN; activity is a `kind`
value on an existing runs table* — invalidates Part E's own plan, and no reconciliation pass was
made:

- **J.3 declares the four lead tables one row-kind** ("every one is 'a document we might admit,
  and why we think so'") and J.1 supplies the exact `origin` vocabulary to unify them
  (`searched · mined-* · gap-driven · code-register · hand-entered`). Part E keeps **three**
  of them as separate tables (`res_items`, `res_candidates`, `res_code_leads`).
- **J.1 declares a mining pass "a search with a different origin."** Part E keeps
  `res_mining_runs` and `res_gap_mining_runs` as separate activity tables — precisely the
  one-table-per-activity growth J.3 diagnoses as the disease.
- **J.3 orders `search_coverage` / `search_languages` deleted** as rule-5 dual homes; Part E
  proposes renames for both (`res_coverage_links`, `res_language_links`).
- **J.3 makes `search_admissions` "a join, not a table"; Part E renames it**
  (`evi_admission_links`).

Part E is the operative 66-row plan; Part J is the ruling-shaped principle. A migration author
following E executes what J forbids. This is not a nuance — it is two incompatible table plans in
one document, written hours apart and never merged.

### B3. The seven-view list now committed into CLAUDE.md is wrong by CLAUDE.md's own definitions

"Substrate is not a stage" (CLAUDE.md, same section). Then, by the doc's own Part E / the 08-25
map (both put `items`, `slugs`, `lang_jur_map` in substrate):

- `v_coverage_priority` reads `search_executions` + `slugs` + `lang_jur_map` — **one stage plus
  substrate. Crosses nothing.** The repo's own 2026-08-25 correction record measured exactly this:
  "Only v_coverage_priority is a real candidate… **research-stage only, no cross-stage role**."
- `v_item_extractions` reads `source_value_extractions` + `evidence_sources` + `items` — **one
  stage plus substrate. Crosses nothing.**

The commit attributes the four→seven delta to "resolving nested views and quoted table names,
which the earlier pass missed." That explanation is real for `v_code_floor_only` (its SQL quotes
`"specifications"`) and plausibly `v_pending` — but for the two above the delta comes from
**silently counting substrate joins as boundary crossings**, a definition change nowhere declared.
Applied consistently, that definition makes almost every view in the schema "the most protected
object in the schema" (41 of 80 FKs point into substrate) and vacates the protection rule. So
either the substrate rule or the seven-list is false as written, and the falsehood is now in
CLAUDE.md, tagged as a *measurement*. Five of the seven survive scrutiny; two do not.

### B4. Sequence: Part L's step 1 arms a blocking gate against a table Part I retires — and Part G's caller census omits the entire generator family

- `build_site.py --check` walks `items` (`scripts/generate/build_site.py:110,125`); it is the
  command behind `site_pages_fresh`. L.6 step 1 promotes that check to **blocking**. Part I's
  baseline **retires `items`**. Nothing in the document orders `build_site.py` (or `spec_page.py`,
  `population_page.py`, `room_page.py`) rewritten in the same change: **Part G's caller list —
  views, db.py, dbcore, schemas, pipeline-contract, pipeline_completeness, check-registry, skills,
  data migrations — does not contain `scripts/generate/` at all**, even though K.2 measured those
  very files. Executed in the doc's own order, the baseline lands with a blocking gate whose
  subject table no longer exists: a hard red, or worse a §2(a) vacuous pass, on the repo's only
  reader-facing gate. Promotion is fine *today*; the doc never reconciles it with its own
  retirement plan.
- **L.6 step 3 precedes its own dependencies.** "The two columns" are specified as
  `spe_items.rationale` and `syn_items.synthesis` (L.5) — host tables that only exist after step
  4's baseline creates them. As ordered, step 3 either targets the old tables (then is redone in
  the baseline) or cannot run.
- **Circular gating on F.2.** I.6: do not run the baseline before Part F is answered; F.2 says
  whether `ren_items` is a table is "not decided." K.5 then flatly decides it ("A manifest") and
  L.6 step 4 schedules it into the baseline. The doc's gate on itself is both open and satisfied.
- **`ren_items` re-creates a table the owner had dropped.** `build_site.py`'s own docstring:
  an earlier `render_manifest` "was dropped by migration 046: **the owner has stated the target
  architecture is dynamic rendering** … under dynamic rendering there is no per-page build event
  to record." K.5's manifest-row-per-published-surface is that table again. A live prior owner
  statement is contradicted with no recorded contact — the mirror image of the rule-0 failure in
  B0, and a §1 burden-of-proof question ("what wrong thing reaches the guidebook") that is asked
  of neither new table against the dynamic-rendering target.

---

## WEAKENS

### W1. L.3's "nine of 93" is a hand-written count, and it is wrong by ~3×

Measured: **28 of 93 `items.name` values contain digits; 23 match a value-plus-unit pattern.**
Beyond the nine listed, the same class includes `A-02` NRC ≥0.85 · `A-03` STC ≥35 · `A-08` NC-25 ·
`B-01` ≥150 EML · `B-06` ≥300 lux · `B-08` ≤30 gloss units · `B-11` ≤2700 K · `C-04` LRV ≥30 ·
`E-03` ≤1:20 · `E-07` PTV ≥36 · `I-01` ≤22 N · `A-16` ≥8 m² — quantified determinations
indistinguishable from `E-08`'s ≥1200 mm. Consequences: (a) L.6 step 2's remediation ("those nine
are then owed real determinations") is under-scoped threefold; (b) the proposed check as worded —
"no label, name or description may contain a quantity" — also fires on `ISO 23599:2019`,
`IEEE 1789-2015`, `MERV 13`, which are standard designations, not determinations: false positives
in a repo whose own quoted doctrine (L.4) says noise "teaches the reader to ignore the check";
(c) this is §2(b) — a hand-written count in a derived document — committed inside the very section
proposing a gate against exactly that defect.

### W2. The causal core — "no FK lands on a hand-off object, which is why it does not walk" — is overclaimed

- **A keyed cross-stage walk exists today.** `search_admissions(exec_id → search_executions,
  ref_id → evidence_sources)` is a research→evidence edge at the level of the *act*, with
  timestamps. The walk from query to admitted source works; what is missing is the lead-level
  edge and everything downstream of extraction. "The walk itself has no keys" is false for the
  first hand-off.
- **Downstream emptiness fully explains downstream non-walking.** Judgment/synthesis/specification
  hold 0 rows because no synthesis has been done (CLAUDE.md §3: "the content is barely started"),
  keys or no keys. The doc's better sentence — "The row counts say it is empty downstream; this
  says it was never connected" — distinguishes the two; the causal "which is why" collapses them.
- **The schema already holds a synthesis→specification pointer** under the doc's own six-stage
  assignment: `specifications.convergence_id → convergence_assessment` (nullable). It is not the
  designated hand-off *object*, but it is a specification-stage row keyed to a synthesis-stage
  product — the closest thing to a hand-off key in the schema. The doc mentions the column only
  to complain it is a rowid (C.4) and never states its fate under `spe_synthesis_links`. "None of
  the 41 is a hand-off" survives only on the five-stage attribution the doc itself supersedes.
- Same-family leaps: "`judgment_items`' absence is why the extraction table could sit… unwritten
  without anything noticing" (a 0-row consumer notices nothing; a *gate* notices, and none is
  proposed); "the stranded-yield bug is a consequence of modelling mining as a table" (the bug is
  a missing writer; an `origin` column writes no rows either); "`bpc_metadata`'s PK is slug — the
  fan-in… already encoded" (a PK on the *target* encodes nothing about inbound cardinality —
  especially when the doc's own headline is that **nothing points at `bpc_metadata` at all**);
  "no UNIQUE on `(ref_id, parameter)` — the fan-out, likewise already encoded" (absence of a
  constraint is absence, not encoding).

### W3. J.3's "33 zero-row tables = §1's burden unpaid thirty-three times" contradicts the repo's rule 4 and the doc's own Part I

CLAUDE.md rule 4: "treat a 0-row object as unproven, not clean" — and the 2026-08-25 correction
commit spelled out that it cuts both ways: "EMPTY IS NOT DEAD… render surfaces awaiting data."
Most of the 33 are downstream-of-content tables whose emptiness is the *ordained pre-synthesis
state* — the same emptiness Parts G and I celebrate as "the window" and "the opportunity." The doc
uses 0 rows as indictment in J.3 and as opportunity in I.7. Some of the 33 are genuinely unread
apparatus; the count proves nothing about which, and "never been used once" is an inference the
current row count cannot carry.

### W4. Stage-move problems within attack surface 1

- **`evidence_population_match` → judgment**: defensible in principle (a grade is a judgment), but
  the moved table cannot participate in the stage it moves to. It keys `ref_id` → sources — a
  *satellite*, in the doc's own terms — not any evidence-item; its 25 rows were written while
  extractions number 0, i.e. the grading act happens **during collection**, before any
  evidence-item exists to judge. A judgment-stage table with no possible `evidence_item_id`
  breaks the spine's own grammar. Worse, F.1 says the grade *folds into* `jud_items`' column set
  while Part E keeps `jud_population_grades` as a separate table — the doc holds both.
- **`spec_value_probes` → specification**: Part B condemns its keying ("reaches past the
  extraction to the paper"); Part E moves it **without a re-key note**, while giving
  `item_bpc_links` an explicit one two rows up. The mis-key the doc itself flagged survives the
  move. A probe in the specification stage should consume synthesis/judgment items; as keyed it
  consumes papers.
- **`convergence_assessment` → synthesis**: the justification is circular — "counting independent
  roots is weighing, which is what synthesis now names" — but the ruled judgment row *also* names
  weighing ("how it weighs"). Aggregate-vs-per-item weighing makes the move defensible; the
  doc's stated reason does not, because the word it leans on appears in both stage definitions.
- **`conflicts` → synthesis**: fine as a cross-population finding; the doc flags it arguable,
  correctly. But its `pop_a`/`pop_b` free-text keys (C.3) are disposed of nowhere — not in E, not
  in I.5's baseline list, not in L.
- **Not moved but owed the same scrutiny**: (i) **`gaps`** — the 08-25 map's own gloss is "a gap
  is a first-class **finding**… a **publishable result**"; findings are synthesis output that
  *re-enters* research, and the doc assigns it to research without a word; (ii)
  **`jurisdictional_values`** — kept in research as `res_code_leads`, yet L.5 renders the
  "jurisdictional comparison" from "code-leads × `spe_items`". Under the REFERENCE-ONLY ruling
  the doc itself cites, code-leads carry **0 values in 109 rows by ruling** — the comparison view
  has literally nothing to display, and any jurisdictional value that reaches a reader must have
  passed through evidence→judgment, not be rendered off a research lead table. L.5's row is
  incoherent with Part E's row for the same table; (iii)
  **`source_value_extractions.promoted_to_rdc_id → reasoning_doc_citations`** — an
  evidence-stage column pointing *downstream* into synthesis, filled after the extraction is
  complete: the exact "write into a completed stage" anti-pattern Part B invokes to reject
  back-pointers, sitting **on the proposed `evi_items` itself**, unflagged anywhere in 877 lines.

### W5. C.3's soft-reference census misses live cases on the very tables under study

- `evidence_population_match.source_ref` **duplicates `ref_id` byte-for-byte on all 25 rows** — a
  live rule-5 dual home on the table the doc moves between stages, missed by C.2's
  seven-names-for-one-referent list (it would be the eighth).
- `evidence_population_match.target_population` / `study_population` — population references with
  **no FK to `populations`** (its only FKs are ref_id and gap_id). C.3 lists `conflicts.pop_a/b`
  and misses these.
- `search_executions.admitted_ref_ids` — a **packed JSON list of ref_ids on a research row**,
  crossing into evidence. Missed by C.3's packed-reference list — and if J.3 deletes
  `search_admissions`, this packed column becomes the *only* home of the admission edge, the
  worse home winning by deletion.
- J.3's premise for deleting `search_admissions` — "the lead names its search" — is **false
  today and never specified as an addition**: `source_locators` has no exec/search column (its 20
  columns end at `notes`), and Part B/J.1's column list for `res_items` (`origin`,
  `parent_item_id`) does not include one. Executed as written, J.3 severs the only keyed
  research→evidence edge in the schema (see W2) and loses `search_admissions`' own payload
  (`created_at`, `created_by_session` — the admission *act*).

### W6. `stage_id[:3]` is collision-safe today and drift-unsafe forever

Six distinct codes today, verified. But: (a) no collision guard exists or is proposed — any future
stage id starting `res`/`syn`/`spe`… collides silently (`resolution`, `review` of specs,
`specialization`), and `stage_prefix()` will happily mint the duplicate; (b) the deeper problem is
that the derivation runs **once, at christening** — the prefix is then *stored* in 66 table names.
The stage list has changed **twice in the 72 hours before this proposal** (08-24 → 08-25 five-stage
→ 08-27 six-stage). On the next rename, `stage_prefix(new_id)` diverges from every stored table
name and **no check is proposed comparing `sqlite_master` prefixes against
`pipeline-contract.yaml` stage ids**. "Derived, not a second vocabulary" is true of the function
and false of the schema: the table names are a second home with no drift detector — rule 5
satisfied in the argument, not in the mechanism. (c) Also unremarked: stage ids *already* have two
homes — `pipeline-contract.yaml` (CLAUDE.md: "the single home") and the hardcoded `STAGES` list in
`tools/pipeline_completeness.py:37` — and Part G lists both as callers without noticing the
duplication it walks past.

---

## DEFECTS (wording / internal consistency)

- **D1. Part E violates Part D's own run test.** `search_executions` carries `executed_at`
  (timestamp) and `results_found/screened/admitted` (outcome) — D's run test verbatim — yet E
  assigns `res_searches` on a taste note ("the row is a search, not an 'execution'") while
  `citation_mining`, an equally act-shaped table, gets `_runs`. D's stated purpose was "decided by
  a test against the schema rather than by taste."
- **D2. `syn_convergence` violates D's "head noun always plural."** Convergence is a mass noun.
- **D3. Junction naming is inconsistent in E.** `evi_slug_links` and `syn_item_links` name the far
  side; `ren_case_study_links` and `ren_economics_links` name the *near* side and drop the linked
  side entirely — for the two tables E itself flags as "named for the specification, foreign-keyed
  to `items`", the proposed fix names *neither*.
- **D4. `figures`/`figure_links` (Part K) carry no stage prefix** though they are render-stage
  content, against Part A's "no prefix means not a stage." And `figure_links(figure_id,
  target_kind, target_id)` is the **polymorphic junction J.4 explicitly forbids** ("SQLite cannot
  key a polymorphic column"), offered as the primary shape with the J-compliant per-stage junction
  demoted to a parenthesis.
- **D5. The word "item" survives everywhere with its retired meaning.** `items` is "retired
  outright — the word was the ambiguity," and "-item" is simultaneously consecrated as the
  hand-off word. Yet E leaves `item_population_links`, `item_demand_links`, `term_item_links` and
  coins `syn_item_links` — four names carrying the retired sense. The doc notices this hazard
  once, for `room_items`, and nowhere else. "Re-pointed once `items` retires" never names the
  re-point target; if it is `ren_items`, substrate junctions point *into render*, the inversion
  the doc flags on `item_population_elaborations`.
- **D6. L.6 step 1's payoff sentence contradicts L.3.** "After this, an `e-08`-class page edit
  cannot be committed" — L.3's whole point is that e-08 is **not an edit** (it renders the DB
  faithfully). The gate that catches the e-08 class is step 2's vocabulary check; step 1 catches
  hand-edits, a class with zero known instances on `site/specs`.
- **D7. Small stale/hand counts**: "`skills/` holds 49 skills" — 50 entries on disk; Part A cites
  "`stage_label` … existing, :42" without naming its file (`tools/pipeline_completeness.py`); the
  RULE's Condition/Action orders the contract/STAGES updates but not the re-derivation of the
  seven view spans it renders stale in the same commit.

---

## What was NOT found

For balance of record, claims attacked and confirmed sound: the 875/10/4/6 REF-overlap figures;
`REF-VERIFIED` breaking `MAX()`; the 41/39 FK split arithmetic (under its five-stage attribution,
as hedged); `bpc_metadata` PK = `slug`; jv 0/109 non-null; `site_pages_fresh` advisory and
uninvoked by `regenerate_derived.sh`; the rule-0 handling of the six-stage supersession itself
(recorded on contact, superseded wording correctly barred as counter-argument); the Part H
walk-back on `v_divergence` (honest and correct in both directions); the baseline-over-renames
argument in I.1–I.2 (057 precedent and the SQLite constraint-ALTER limitation are real and
sufficient); I.6's refusal to hand-build the DB.

## Verdict

**The six-stage assignment and the `-item` naming hold as recorded for stages one through five;
the proposal as argued does not.** The keyed-spine half rests on (i) a cardinality table that
contradicts its owner quote in one cell (evidence→judgment) and exceeds it in another
(specification→render), with the contradiction resolved by the exact paperwork-versus-ruling move
rule 0 forbids; (ii) a junction shape that enforces neither the owner's N:1 nor its own "≥1"
promise, chosen over an unexamined third option (junction + UNIQUE) that satisfies the ruling
exactly; and (iii) a causal story ("no keys is why it does not walk") that the existing
`search_admissions` edge and the downstream 0-row state jointly refute as stated. Part E and Part
J are two incompatible table plans in one document; Part L's implementation order arms a blocking
gate against a table Part I retires and adds columns to tables that do not yet exist; and the
seven-view list committed into CLAUDE.md misclassifies two views by CLAUDE.md's own
substrate-is-not-a-stage definition. Before any migration is drafted: put the evidence→judgment
cardinality and the render-manifest-vs-dynamic-rendering conflict back to the owner, reconcile E
against J (one plan), fix the seven-view list, and re-order L.6 around the `items` retirement.
