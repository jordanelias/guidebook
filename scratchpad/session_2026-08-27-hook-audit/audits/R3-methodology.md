# R3 — Methodology coherence audit: does the reconciled pipeline work as a PROCESS?

**Adversarial auditor 3 of 4 · 2026-08-27 · READ-ONLY · DB `user_version` 64, opened `mode=ro`.**

**Scope attacked:** `base → research → evidence (cursory scan) → judgment (deep read) → synthesis →
specification → render`, as proposed in `references/owner-notes/2026-08-27-architecture-note.md` and
read as process in `scratchpad/session_2026-08-27-hook-audit/WALKABILITY-PLAN.md` Parts 15–16.

**Counting conventions used throughout.** "66 tables" = `sqlite_master WHERE type='table' AND name
NOT LIKE 'sqlite_%'`. All row counts measured this session against the live DB; all are dated
2026-08-27 and are re-derivation commands, not facts to quote onward. "Populated" =
`IS NOT NULL AND TRIM(x) <> ''`.

---

## 1. The aporia resolution — the ontology survives; its two material preconditions do not exist

### 1.1 What I attacked and could NOT break

WALKABILITY-PLAN 16.1's core move — *"observed, but not yet adjudicated"* — is genuinely coherent as
epistemology. Recording that a source uses the phrase "wayfinding" verbatim is a fact about the
document, the same epistemic act as recording its DOI. It presupposes no category membership. I
tried to collapse it into the presupposition it claims to escape and failed on the ontological
level: the presupposition is NOT in the harvested row. It is elsewhere — see 1.2 and 1.3, where it
actually lives.

The seed defence (16.2 — "the seed is allowed to be wrong, because it is revisable") is also sound
*in form*, and substrate growth from downstream stages has real precedent:
`governance/pipeline-map.yaml:157` records `2-acquisition → 1-substrate` ("an admitted source
introduces terms/aliases (R11)") as a NORMAL loop, not a defect. Re-entrancy is not being invented
for this argument.

### 1.2 BLOCKER — the observation substrate is not retained, so "observed but not yet adjudicated" is not a durable state

The harvest requires a term-hood criterion — *"listing out all concepts/topics/key words/phrases
that appear in the source"* (owner, architecture-note.md:96-98) is not mechanically definable.
Any extractor either matches against existing vocabulary (re-importing the presupposition) or is
unbounded (all n-grams). **That is survivable only because the criterion is a revisable seed — and
a seed revision requires re-scanning every already-scanned source.**

Measured: **the project retains nothing to re-scan.**

- `find . -name '*.pdf'` over the whole tree (excluding `.git`): **0 files**.
- `retrieval-log/`: **33 files, 1.4 MB, 3 session directories** — Crossref/PubMed JSON, XML,
  landing-page HTML. Metadata payloads. **No full text of any source, anywhere.**
- No `fulltext` store exists under any name (`find -name '*fulltext*'`: 0).

Failure scenario: the harvest runs over 200 sources with extractor v1; judgment discovers v1 missed
a concept class (say, non-noun-phrase process terms); v2 exists; the 200 sources are paywalled,
link-rotted, or simply gone. The "third state" collapses back into the aporia: the vocabulary is
once again bounded by what was presupposed — this time by the extractor — with no record of what was
lost. This is also §2(c)'s defect class at concept level: `CLAUDE.md` §2(c)'s fix was
*"verification must leave an artefact"* and *"never write a bibliographic field from memory when a
payload is in hand"* — a harvested term with no retained payload behind it is a concept-level field
that can never be diffed against bytes. Judgment's *deep read* likewise has no stored object to
read: the note's own judgment stage (*"the deep read on it"*) presumes text in hand that the
repository does not hold.

**Smallest fix:** extend `scripts/research/retrieval_log.py` — the mechanism already exists and is
already sha-addressed per session — to persist the retrieved text layer (PDF or extracted text) of
every admitted source at admission time. One flag on an existing script, no new table.
**Owner-gated part:** retaining copyrighted full texts is a licensing posture question, which
`CLAUDE.md` §1 puts in the owner-sign-off class. Flag it; do not decide it.

### 1.3 DEFECT — 16.2 overstates re-entrancy's standing and its scope

16.2: *"That is re-entrancy, and it is already ratified — governance/pipeline-map.yaml:78."* Two
problems, both file-bound:

1. **The file disclaims the authority being borrowed.** `pipeline-map.yaml:18-19`: *"STATUS:
   DESCRIPTIVE, not normative. It records the pipeline as it IS on 2026-08-21, defects included.
   It is not a design."* Re-entrancy's doctrinal standing comes from `CLAUDE.md`'s pipeline
   section, not from ratification of this file — and `CLAUDE.md` immediately scopes it: *"That
   answers write order."*
2. **Write-order re-entrancy is not seed revisability.** The aporia argument needs substrate rows
   to be *corrected* cheaply. Substrate is `entered_by: migration only` (`pipeline-map.yaml:85`),
   migrations are append-only and immutable (`CLAUDE.md` rule 3, fix-forward), and a seed
   correction that renames or retires a topic must sweep callers (rule 0.4) — `slugs.slug` carries
   **14 inbound FKs** (CLAUDE.md's own 2026-08-27 measurement), and the repository's last rename
   swept eight readers and six skills and still missed a view (migration 064). *"The seed is
   allowed to be wrong"* is doctrinally true and mechanically priced at migration-plus-sweep, not
   zero. The plan prices it at zero.

**Smallest fix:** one sentence in the plan replacing "already ratified" with "held descriptively at
`pipeline-map.yaml:78` and doctrinally in `CLAUDE.md`, scoped to write order", plus a stated cost
model for seed revision (compensating migration + rule-0.4 sweep).

---

## 2. Relevance vs applicability — the line holds, conditionally, and the condition recurses to 1.2

### 2.1 What I attacked and could NOT break

The two-adjudication split survives direct attack. Relevance ("is this document about this topic")
must be settled at collection or nothing is admissible; applicability ("does this bear on this
population's parameter") is downstream — that asymmetry is real and R1's `phase: before-admitting`
(`research-contract.yaml:61`) is consistent with collection being an adjudicating stage, exactly as
15.6 concluded. The late-visible-relevance case — a source whose relevance only appears on deep
read — has a recovery path that already exists: rejected/undecided candidates are retained
(`search_candidates` measured: 55 `PENDING-VERIFICATION`, 3 `REHOME`, 1 `MISCELLANEOUS`, 1
`ADMITTED`; `OUT-OF-SCOPE` in the CHECK vocabulary with 0 live rows), R8 keeps empties, and R2
citation mining re-raises sources from other sources' reference lists. Re-adjudication is possible.

### 2.2 MAJOR — but the line is only stable in one direction, and the schema records neither adjudication

Two measured failure points:

1. **Relevance to a concept that does not exist yet.** Relevance is adjudicated against topics —
   the seed. When judgment mints a NEW concept (the whole point of `term_adjudications`), every
   previously-scanned source was never adjudicated for relevance to it. The plan's own answer is
   "grep the harvest retroactively" (16.4's derivable relevance) — which is correct and is exactly
   why this finding recurses to 1.2: **retroactive relevance is bounded by harvest completeness,
   and harvest completeness is bounded by retention.** Without 1.2's fix, late-minted concepts
   silently lose their pre-existing evidence base.
2. **The adjudication being made now leaves no record.** Measured: `source_slug_links` 10 rows,
   `relevance_note` populated in **0**; `search_admissions` carries no grounds column (schema:
   `exec_id, ref_id, created_at, session`). And the granularity the owner names —
   *"topic/category/concept"* — is inexpressible: `slugs` is **flat** (measured columns: no
   parent/category/level; 106 rows). A category-level relevance judgment must be either copied
   across leaves (rule 5) or dropped. Confirms 15.6; the parent column is owner-confirmed already.

**Smallest fix:** the plan's own two-table harvest plus the parent column — already ordered
correctly in 16.7. Add one thing 16.7 omits: a re-adjudication obligation (contract rule or
trigger) when `term_adjudications` mints a NEW concept — "sweep the harvest for prior observations
of it" — otherwise recovery is possible but never obliged, which is a convention edge, the exact
kind `pipeline-map.yaml:31-33` says fails quietly.

---

## 3. Saturation vs the matrix — the split is right; the stopping rule is not computable when research needs it

### 3.1 What I could NOT break

Matrix = spread (structural defence against the 2026-08-19 four-of-five-on-one-mechanism failure),
saturation = stop. The division of labour in 16.5 is methodologically standard and sound, and the
matrix-as-denominator reading (15.3) is proven buildable: `v_coverage_priority` (a real view,
`slugs × lang_jur_map`, 7,208 rows) is one cross of it running today.

### 3.2 MAJOR — saturation-by-concept-novelty cannot be measured before judgment has run, and judgment is the named bottleneck with no writer

The claim (16.5): saturation = *"new sources stop yielding new concepts"*, and *"the harvest makes
the existing column mean something."* Measured against what exists:

- `search_executions.saturation_signal` is a per-search **self-report**, CHECK-limited to
  `('none','partial','saturated')`. Holds today: **NULL 18 · none 3 · partial 7 · saturated 0**
  over 28 executions. Nothing derives it; nothing reads it.
- "New **concept**" is a post-adjudication fact. A new *verbatim term* is not a new concept:
  measured surface-to-concept ratio is **2,382 `term_aliases` / 88 `terms` ≈ 27:1 across 15
  languages**. A verbatim-novelty proxy therefore inflates novelty ~27-fold and the multilingual
  axis (two of the five matrix modes) guarantees near-endless "new" surface forms — verbatim
  saturation would essentially never trigger. Concept-novelty saturation requires
  `term_adjudications`, which is a **judgment** output — and 15.8 itself names judgment as *"the
  throughput bottleneck, and it is the stage with no writer"* (verified: no `db.py` extraction
  subcommand; `source_value_extractions` 0 rows).

So the process's stopping rule for research is gated on its slowest, least-built stage staying
current with collection. That coupling is real, defensible under re-entrancy — but **nowhere
stated**, and a sweep that outruns adjudication has no stopping signal at all. Failure scenario:
the matrix drives 500 searches across a region; adjudication is 300 sources behind; every
saturation read says "still yielding" because yield is unmeasurable; the sweep continues on fiat.

**Smallest fix:** (a) state the coupling — a matrix region may not be declared saturated until its
observed terms are adjudicated; (b) build saturation as a **derived view** over
`term_adjudications` novelty per region, and retire or demote `saturation_signal` to the
self-report hint it is — deriving saturation *and* keeping the hand-written column is a rule-5 dual
home in the making.

---

## 4. value / process / figure / goal — "no schema home" is the wrong diagnosis; the missing thing is a LANE, and the mission owns it

15.7's table says process and goal have **no** schema home. Measured, that is overstated at the
column level and understated at the process level:

- `source_value_extractions.claim_type` CHECK is
  `('numerical','range','qualitative','framework','absent')` — a process or goal determination
  *can* be filed today as `qualitative`/`framework` text in `claim_text`. The column exists.
- **What does not exist is any consumer.** The entire downstream — synthesis →
  `specifications` (a per item × population cell), markers, render — consumes cell-shaped
  *values*. The evidence-state machine (`mission-and-epistemics.md`, T-04 table) is defined per
  *(parameter × population) cell*: `stated/provisional/pending/not_applicable`. A goal ("optimise
  for speech intelligibility, not silence") is typically population-general and parameter-spanning
  — **it is not a cell**, so the state machine does not apply to it, and no stage reads it.
  Markers partially transfer (● is "evidence-based"; a Co-1-anchored goal could carry ●), but tier
  attaches to the *source*, and nothing downstream renders a marked goal anywhere.
- **Figure** is the one genuinely homeless output: scanned all 66 tables for any
  figure/image/diagram/caption/alt-text/asset column — **zero** (convention: substring match on
  column names). It also carries reproduction-licensing questions that are owner-gated content
  doctrine (`CLAUDE.md` §1), and — in an accessibility guidebook — a figure store without an
  alt-text column would be a self-indictment. Figures are a design task, not a column.

**Ranked MAJOR, and here is the deep version:** `mission-and-epistemics.md:72`: *"Questions are
first-class data, not annotations."* Measured: among 66 tables there is **no questions table**
(nearest: `gaps` 5 rows, `gap_mining`). The mission's first-class object has no home while the
value lane has six stages, an acceptance test, and 48 columns. Process and goal are the
question-shaped outputs — the material of "get people to ask the right questions" — and they are
exactly the outputs the pipeline cannot carry end-to-end. Adding a `judgment_items.category` column
without a declared reader for the non-value categories violates `CLAUDE.md` §1 directly: *"Nothing
is added without naming what reads it."*

**Smallest fix:** before creating `judgment_items`, declare the consumer per category — value →
synthesis/specification (exists); process/goal → the questions-led render surface the mission
already commits to (doctrinal commitment 6, B3), which needs its first table; figure → deferred to
an owner licensing ruling. One design decision, made once, at the point 16.4's tables are created —
not a retrofit.

---

## 5. Writers and readers per stage; R1–R15 under the new boundaries

### 5.1 Stage-by-stage (convention: "exists" = live table with the stated role; proposal objects marked)

| stage | produces | consumed by | breaks |
|---|---|---|---|
| base | taxonomies, topics, targets, jurisdictions | research.matrix | **matrix consumes 3 members nothing produces**: `base.jurisdictions`, `base.sources` (targets), `base.models` — all **absent** (arch-note measurement table; `jurisdiction` an inert enum on 11 tables). Two of five matrix modes cannot be crossed. |
| research | `search_executions` (28), logs, failures | evidence admission (`search_admissions.exec_id`); coverage views | holds. R8/R14's empties have a reader (`v_coverage_priority`). But `terms_used` populated in only **9/28** — the multilingual axis's search-generation role (15.5) currently has no writer discipline. |
| evidence | APA metadata (30 columns, built) + **`observed_terms` (proposed)** | judgment; saturation; relevance grounds | the harvest table does not exist, so today judgment-as-adjudication consumes something nothing produces. Acknowledged gap (16.4) — consistent. |
| judgment | tier verdict; category; **value/process/figure/goal**; `term_adjudications` (proposed) | synthesis (value only) | **three of four outputs have no reader** (§4). Also: judgment re-enters `base` by minting terms — but `base.taxonomy_*` (population taxonomy) is owner-gated doctrine (`CLAUDE.md` §1 DG-NON class). 16.7's *"base is an output that accretes"* is true for `terms` and false for taxonomies; **the boundary is undeclared**. MAJOR: an agent stage cannot be the writer of owner-gated substrate, and nothing in the plan says which `base` members judgment may grow. |
| synthesis | best_practice_synthesis (Opus floor) | specification | the note stops at judgment; the owner's overrule names `evidence>judgment>synthesis`, so synthesis's input is `judgment_items` — which does not exist, and (CLAUDE.md, measured 2026-08-27) **not one FK in the schema lands on any stage's hand-off object**. |
| specification | `specifications` (0 rows) | render views (`v_divergence` etc.) | writer absent; REPAIR-PLAN §7's `walk_e2e.sh` *"fails by construction today"* — consistent, that is the acceptance criterion. |
| render | site/parts/tools | readers | holds. |

### 5.2 The contract under the new boundaries — one vacuity, three mis-phasings, one survivor strengthened

The pivotal schema fact: `evidence_sources.tier` is **nullable** (`tier INTEGER`, no NOT NULL —
measured from DDL), and under the owner's model the tier verdict moves to judgment
(architecture-note.md:60: judgment *"delivers a verdict on an evidence item for what tier"*), while
evidence records only *"type of source (academic, code, professional practices, etc)"* (:58).

- **R2 — MAJOR, goes §2(a)-vacuous.** `research_batch_dod.py` computes admitted anchors as
  `evidence_sources.tier BETWEEN 1 AND 3` scoped to the session (~line 317). If tier is unfilled
  until judgment, `admitted = 0`, and R2 **passes with zero citation-mining rows** — a gate
  passing having examined nothing, the repository's most-produced failure mode (`CLAUDE.md` §2(a),
  produced four times). Failure scenario: cursory-scan batch admits 20 sources, tier deferred, DoD
  green, no mining ever obliged. **Smallest fix:** re-key R2's anchor count to the judgment-stage
  verdict table when it exists, and until then have R2 FAIL (not pass) when admitted sources carry
  NULL tier — mirroring the deliberate missing-pointer-FAILs-not-SKIPs design.
- **R13 — mis-phased.** *"Grade population-of-study vs population-served on every admission"*
  (`research-contract.yaml:195-203`) requires reading a methods section — a deep-read act demanded
  at what is now a grep/regex stage. Either R13 moves to judgment or admission is not cursory.
  The note is silent on population matching entirely (15.9's warning). Same class: **R5**
  (peer-reviewed-vs-grey is a classification verdict, now judgment's job) and **R4** (already
  flagged at 16.6.3). **R3/R12/R15** ("when-filing") survive if "filing" is re-declared to mean
  judgment-stage writes — but their enforcer is the *research-batch* DoD keyed to
  `sessions/LATEST-RESEARCH`; a judgment session that is not a research session scopes the gate to
  nothing, and it passes green (the exact trap in `CLAUDE.md` §7, "session ids").
- **R1 — attacked and NOT broken; strengthened.** Its structural check already rests on
  `search_executions.target_evidence_type IN ('co1','co2')` — search *intent*, not verdict — which
  is research-stage data and survives the boundary shift untouched. Under the matrix, "Co-1/T2/Co-2
  FIRST" becomes a *sweep-ordering rule over matrix cells* — structural rather than remembered,
  the same upgrade 15.4 claims for the mechanism-split defence. `before-admitting` still means
  something because collection still adjudicates (relevance); what it stops gating is tier.
- **R10 — unaffected and load-bearing:** locator re-retrieval is mechanical and is precisely what a
  cursory-scan stage can do; it is also the hook on which the §1.2 retention fix hangs.

---

## 6. The mission test — the process is not a determination machine, but the buildable subset of it is

Attacked the strong form ("this optimises for a determination machine") and could not sustain it
against the design *as proposed*: the harvest grounds vocabulary in sources rather than authority;
saturation is a question-honesty rule; the matrix serves declared, transparent methodology (mission
test #7); R7 makes harm first-class and anchors to the mission line itself
(`research-contract.yaml:146`). Four output kinds, two of which (process, goal) are
question-material, is *more* mission-shaped than the current value-only extraction schema.

**What fails the test is the implemented and planned subset — MAJOR:**

1. Every output the mission ranks central is the unbuilt part: no questions table in 66 (§4), no
   process/goal reader, figures absent, and 42 of 93 element names carrying determinations in the
   label (15.7's symptom) because the mission-shaped outputs have nowhere else to go.
2. The acceptance test itself encodes the bias: REPAIR-PLAN §7 defines Phase-1-done as *"a
   specific value and its ref-id both appear on the rendered page."* Passing the project's only
   end-to-end test requires rendering a **number** and cannot be advanced one inch by rendering a
   question, a divergence, or a goal. Mission test #1 (*"does this decision help readers ask
   better questions?"*) is not represented in any gate, check, or acceptance criterion — grep of
   `governance/check-registry.yaml` concepts across the battery shows the entire enforcement
   surface checks provenance, counts, and format; nothing checks that a question exists.
3. 15.9's warning is load-bearing and under-ranked: the note is silent on dissent (the
   deliberately-absent uniqueness refusal, DR-2026-08-19 §7), divergence-visibility (a synthesis
   that suppresses divergence "is in error" — mission), and within-population variability
   (doctrinal commitment 1). These are mission commitments with existing mechanical carriers;
   a re-shape that ports only the note's stages drops them by omission, not decision.

**Smallest fix:** extend `walk_e2e.sh`'s assertion set by one clause — a non-value judgment output
(a goal or process row) must also reach a rendered surface — at the moment `judgment_items` is
designed. One assertion, and the acceptance test stops being structurally value-only.

---

## 7. Verdict table

| # | rank | finding | binding |
|---|---|---|---|
| 1 | **BLOCKER** | Aporia resolution depends on repeatable observation; nothing retains source text (0 PDFs in tree; retrieval-log = 33 metadata payloads / 1.4 MB / 3 sessions). Extractor revision → unrepeatable harvest → aporia returns via the extractor. | §1.2 |
| 2 | **MAJOR** | Saturation stopping rule needs concept-novelty = post-adjudication; judgment is the no-writer bottleneck; verbatim proxy inflates novelty 27:1 (2,382/88, 15 languages); `saturation_signal` is an unread self-report (18 NULL/3 none/7 partial/0 saturated) and deriving saturation beside it is a rule-5 dual home. | §3.2 |
| 3 | **MAJOR** | R2 goes §2(a)-vacuous under the new boundaries (`tier BETWEEN 1 AND 3` at admission; tier nullable and deferred to judgment → admitted=0 → green with zero mining). R13/R5/R4 mis-phased; "when-filing" enforcers scope to nothing in judgment-only sessions. | §5.2 |
| 4 | **MAJOR** | Process/goal have a column (`claim_type` CHECK includes `qualitative`,`framework`) but no reader; figure has neither (0 figure/caption/alt columns in 66 tables); mission's "questions are first-class data" has no table. Missing lane, not missing column; creating rows without a declared reader violates §1. | §4 |
| 5 | **MAJOR** | "base accretes as judgment output" collides with owner-gated taxonomy (§1 DG-NON) and migration-only substrate; the agent-mintable vs owner-gated boundary inside `base` is undeclared. Matrix also consumes 3 base members nothing produces (jurisdictions, targets, models — all absent). | §5.1 |
| 6 | **MAJOR** | Relevance line stable only given harvest completeness (recurses to #1); the adjudication now being made is never recorded (relevance_note 0/10; `search_admissions` has no grounds column); category-level relevance inexpressible (`slugs` flat, 106 leaves); no re-adjudication obligation when a new concept is minted. | §2.2 |
| 7 | DEFECT | 16.2 cites `pipeline-map.yaml:78` as "ratified"; the file self-declares DESCRIPTIVE/not-a-design (:18-19); re-entrancy is scoped to write order and does not price seed revision, which costs migration + 14-FK sweep. | §1.3 |
| 8 | DEFECT | Acceptance test `walk_e2e.sh` (REPAIR-PLAN §7) is value-lane only; Phase-1-done cannot be advanced by any mission-central output. | §6 |
| 9 | DEFECT | `terms_used` populated 9/28 — the multilingual search-generation role (15.5) has no writer discipline behind it yet. | §5.1 |

**Attacked and NOT broken (evidence, per house standard):** the observed-not-adjudicated ontology
itself (§1.1) · the relevance/applicability two-adjudication split and R1's `before-admitting`
consistency with it (§2.1) · matrix-as-denominator, proven buildable by `v_coverage_priority`
(7,208 rows) (§3.1) · the spread/stop division of labour (§3.1) · substrate growth from downstream
stages (precedented at `pipeline-map.yaml:157`) · R1 and R10 under the new boundaries, R1
strengthened (§5.2) · the mission-compatibility of the *design* as opposed to its buildable subset
(§6).

---

## Digest

1. **BLOCKER:** the aporia fix is coherent only with a retained observation substrate; the repo holds 0 source texts (33 metadata payloads only) — extend `retrieval_log.py` to persist full text, licensing question to owner.
2. **MAJOR:** saturation = concept-novelty is measurable only after judgment (the no-writer bottleneck); verbatim proxy inflates 27:1; `saturation_signal` is an unread self-report — derive it from adjudications or the sweep has no stop.
3. **MAJOR:** R2 goes vacuous (tier-at-admission keying) and R13/R5/R4 mis-phase under the new boundaries; R1 survives and is strengthened as a matrix-ordering rule.
4. **MAJOR:** process/goal/figure lack a *reader*, not a column — and the mission's first-class "questions" have no table in 66; fix is a declared non-value lane plus one added `walk_e2e` assertion, decided when `judgment_items` is designed.
5. **MAJOR:** "base accretes" is right for `terms`, wrong for owner-gated taxonomies, and undeclared in between; the matrix consumes three base members (jurisdictions, targets, models) that nothing produces.
