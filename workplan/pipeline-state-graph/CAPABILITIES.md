# Capability interrogation

_Rendered from `capabilities.yaml` by `build_graph.py`. Each predicate is evaluated against the live tree (a probe, a verb, a needle in code, a column's CHECK, a row count) or marked HAND-ASSESSED. `CAN` = every predicate passes; `BLOCKED` = at least one fails or its construct does not exist; `UNKNOWN` = no failure but a predicate could not be decided._

The four capabilities are stated by the owner as what the pipeline must be able to do, not as a checklist of verbs.
A capability is judged here as CAN only if every predicate holds on the tree being examined; a single FAIL or a
construct that does not exist makes it BLOCKED, and the blocking predicates are named. The verdicts describe the
checkout the generator was run in; `--compare` adds a second tree (the unreleased tooling branch) as a column.
Predicates answer "can the machinery do this at all", not "has it been done": the live row counts are in
STATE-GRAPH.md. A predicate that tests a ruling the mechanism does not carry fails even where a workaround exists
(a hand-written migration is not the pipeline).

## Summary

| capability | this tree |
|---|---|
| C1 Mine one source across many parameters | **BLOCKED** |
| C2 Grow its own parameter base | **BLOCKED** |
| C3 Synthesize across parameters | **BLOCKED** |
| C4 Specify, then render | **BLOCKED** |

## C1 Mine one source across many parameters

Can a single admitted source be read once and yield values for several parameters, in every lens, with a
record of what was and was not looked for -- without the slug it happened to be filed under limiting what
is taken from it (owner, 2026-10-09: "every admitted source is scanned for any and all applicable parameters,
whatever slug it was filed under")?

| pred | says | verdict | why | atoms |
|---|---|---|---|---|
| C1.1 | no UNIQUE(ref_id) on the capture table: one source may yield many rows | **PASS** | P-D = PASS | LED-100, LED-101 |
| C1.2 | a phrase can be harvested from a source without presupposing a category | **PASS** | matched | LED-115, CLM-040 |
| C1.3 | one source can be harvested for more than one sense of the same phrase | **PASS** | P-W = PASS | LED-197 |
| C1.4 | an extraction can be filed under a slug other than the one the source was admitted to | **FAIL** | P-V2 = FAIL | LED-196, LED-201 |
| C1.5 | a record exists of which parameters a source has been read for | **PASS** | P-V = PASS | LED-195, LED-199 |
| C1.6 | a value can be stated in every lens, including the medical lens | **FAIL** | P-MEDICAL = FAIL | LED-110, LED-154 |
| C1.7 | arguments and qualitative findings can be captured as well as numbers | **PASS** | source_value_extractions.claim_type admits qualitative | SES-022, SES-023 |
| C1.8 | a search records which slug x lens cells it covered | **FAIL** | P-M = FAIL | LED-084, RES-04 |

## C2 Grow its own parameter base

Can a concept met in a source become a parameter, and can the parameter list be extended, corrected, retired
and merged, through sanctioned writers and with the warrant recorded -- without a container that states its own
answer and without hand SQL?

| pred | says | verdict | why | atoms |
|---|---|---|---|---|
| C2.1 | a new concept enters only as a term minted from an observation | **PASS** | verb add-term declared on this tree | LED-150, LED-203 |
| C2.2 | a name may not state its own answer | **PASS** | matched | LED-148, PIP-16 |
| C2.3 | an adjudicated term can be promoted to a parameter | **PASS** | verb add-parameter declared on this tree | LED-092 |
| C2.4 | a term can be judged not-a-parameter, with the reason on record | **PASS** | verb decline-parameter declared on this tree | RES-16 |
| C2.5 | a parameter can be retired or merged on record (retire in place) | **PASS** | P-PARAM-LIFECYCLE = PASS | LED-169, LED-170 |
| C2.6 | the list can be prepopulated from earlier catalogues under screening and owner approval | **PASS** | verb mint-term-from-catalogue declared on this tree | LED-204, LED-205 |
| C2.7 | which direction is better for a disabled person can be recorded per parameter | **PASS** | verb set-parameter-direction declared on this tree | LED-091 |
| C2.8 | the base vocabularies a parameter and a lens point into have a sanctioned writer | **FAIL** | P-O = FAIL | LED-182, CLM-031 |

## C3 Synthesize across parameters

Can the machinery combine what independent sources say about one parameter into a determination, show where
they diverge, and relate more than one parameter to another (interaction, compounding, conflict) -- so that a
finding that depends on two parameters has a place to be recorded and a source to be traced to?

| pred | says | verdict | why | atoms |
|---|---|---|---|---|
| C3.1 | independent sources for one (parameter x lens) cell are combined into one state | **PASS** | matched | LED-151, PIP-08 |
| C3.2 | divergence between sources is a recorded state | **PASS** | convergence_assessment.status admits divergent | MIS-06 |
| C3.3 | a spread across lenses is carried with each lens's direction | **PASS** | matched | LED-176 |
| C3.4 | findings plus a threshold can reach a determination | **PASS** | P-R = PASS | LED-174, LED-172 |
| C3.5 | a synthesis-stage structure can relate two or more parameters | **FAIL** | P-X = FAIL | LED-097, LED-098 |

## C4 Specify, then render

Can a determination be computed from the evidence, keyed on parameter x lens, written through a migration,
retired and redetermined; and can what is written be rendered to a reader at its stated strength, from the
database, with the rendering gated?

| pred | says | verdict | why | atoms |
|---|---|---|---|---|
| C4.1 | a determination is keyed on parameter_id x at least one lens | **PASS** | P-Y = PASS | LED-091, LED-130 |
| C4.2 | the state is computed by the engine from tier arithmetic | **PASS** | P-ENG-T3 = PASS | LED-151, LED-152, LED-010 |
| C4.3 | a determination can be written today: no NOT NULL foreign key of specifications points into an emptied table | **PASS** | specifications has no NOT NULL FK into an emptied table | CLM-034 |
| C4.4 | the engine can assign every value of the state vocabulary | **FAIL** | P-ENG-STATE = FAIL | EVI-361 |
| C4.5 | a determination can be retired in place and redetermined | **PASS** | verb retire-specification declared on this tree | LED-169 |
| C4.6 | a live renderer reads parameter x lens determinations | **NOT-BUILT** | P-K = NOT-BUILT | LED-103, PIP-06 |
| C4.8 | the rendering invariants and tier-derivation consistency are gated | **FAIL** | P-QUARANTINE = FAIL | PIP-06, POS-03 |

## Components against the four capabilities

| component | stage | C1 | C2 | C3 | C4 | what it does for the capability / what stops it |
|---|---|---|---|---|---|---|
| Search log (log-search, search_executions) | research | PARTIAL | -- | -- | -- | logs the query and the prior; has no lens column, so R4's slug x lens coverage cannot be shown (C1.8). |
| Candidate staging (add-candidate, resolve-candidate) | research | -- | -- | -- | -- | holds what a search surfaced; any disposition can follow any other (M01.t3). |
| Source admission (add-source, supersede-source, correct-source) | evidence | PARTIAL | -- | -- | -- | admits a source to slugs; the slug link is what add-extraction later reads as its permission. |
| Citation mining (log-mining) | evidence | PARTIAL | -- | -- | -- | discovery of further SOURCES, not values; a separate axis from extraction (pipeline-operations section 2). |
| Term harvest (observe-term) | evidence | True | True | -- | -- | records any phrase a source uses, any number per source, unjudged; the entry point for new vocabulary. |
| Adjudication and minting (adjudicate-term, add-term) | judgment | -- | True | -- | -- | the only route from a phrase to a term; divergent judgments are allowed to stand as a contest. |
| Parameter registry (add-parameter, decline-parameter, set-parameter-direction) | base | -- | PARTIAL | -- | PARTIAL | creates and declines; on the main tree nothing retires or merges a parameter (C2.5). Direction is the judgment the engine cannot make. |
| Lens registries (populations, base_icf, access_needs, base_taxonomy_medical) | base | PARTIAL | PARTIAL | -- | PARTIAL | add-extraction refuses a lens code whose registry is empty; the medical registry is empty (C1.6) and several base tables have no verb (C2.8). |
| Extraction (add-extraction, derive-extraction, amend-extraction) | judgment | PARTIAL | -- | PARTIAL | True | one parameter per call; refuses a slug the source was not admitted to (C1.4); requires a lens; is what the engine gathers by parameter. |
| Scan ledger (source_scans, v_scan_ledger) | judgment | NO (main) / YES (unreleased branch) | -- | -- | -- | the (source x parameter) read-state record the scan contract needs; absent from the main tree (C1.5). |
| Determination engine (assess_cell) | specification | -- | -- | PARTIAL | True | computes state per (parameter x one lens) cell per run and emits SQL; combines sources within a cell, not across parameters (C3.5); cannot reach a determination from findings plus a threshold (C3.4). |
| Determination gates (raise/resolve) | specification | -- | -- | PARTIAL | PARTIAL | records that a determination disagrees with a link; carries one lens column only (P-GT). |
| Convergence assessment | synthesis | -- | -- | PARTIAL | -- | per-parameter convergence of independent roots; no cross-parameter form. |
| Connections and conflicts (add-connection, add-conflict) | synthesis | -- | -- | False | -- | free-text targets and item-layer keys; no column can name a parameter (C3.5). |
| Gaps (add-gap, assess_cell) | synthesis | -- | -- | PARTIAL | -- | records that a cell is pending and why; sub-vocabulary after OPEN/CLOSED is free text. |
| Renderers | render | -- | -- | -- | False | none exist: the render apparatus was deleted (plan step 1.1; RULINGS R1) and the one view and one renderer of step 3.R are not built (C4.6). |
| Checks and gates (Layer 0) | Layer 0 | -- | -- | -- | PARTIAL | the checks that would hold rendering invariants and tier derivation are quarantined (C4.8). |

