# B1 Session 6 — Candidate D Evaluation + Eliminator Test
**Phase:** B1 (Schema design with architectural derivation)
**Session:** 6 of 6–9
**Candidate:** D — Hybrid (multi-substrate)
**Status:** Per-criterion evaluation complete; D-0112 eliminator test applied; **Candidate D dismissed**
**Predecessor session:** `sessions/session_2026-05-02-b1-s5.md` (Candidate C evaluation, 155/171)
**Operative governance:** D-0108, D-0110, D-0111, D-0112 (applies to this session), D-0113
**Model routing:** opus/150/synth

---

## 1. Session purpose and scope

Apply the 4-question evaluation template to Candidate D (Hybrid) across all 30 criteria. Apply the D-0112 eliminator test: D survives elimination iff ∃ i such that D_i > max(A_i, B_i, C_i). If D is strictly dominated, D is dismissed without proceeding to Session 7 comparative scoring; if D survives, it joins A, B, C in Session 7.

This session also includes the within-Candidate-D sub-substrate sketch (which two stores does the hybrid combine?) per framework §5.2.

### 1.1 Inputs read

- Sessions 1, 2, 3, 4, 5 deliverables (per-criterion score tables from D-0119, D-0121, D-0132 mechanically extracted)
- A6, A9 already in context

### 1.2 Per-criterion max(A_i, B_i, C_i) — input to the eliminator test

The per-criterion scores from D-0119 (A), D-0121 (B), D-0132 (C) yield M_i = max(A_i, B_i, C_i):

| Criterion | Weight | A | B | C | **M** |
|---|---|---|---|---|---|
| C-1.1 | 2 | 2 | 3 | 3 | **3** |
| C-1.2 | 2 | 2 | 3 | 3 | **3** |
| C-1.3 | 3 | 2 | 3 | 3 | **3** |
| C-1.4 | 2 | 3 | 2 | 3 | **3** |
| C-2.1 | 2 | 2 | 3 | 3 | **3** |
| C-2.2 | 2 | 3 | 3 | 3 | **3** |
| C-2.3 | 2 | 3 | 3 | 3 | **3** |
| C-3.1 | 3 | 2 | 3 | 3 | **3** |
| C-4.1 | 2 | 3 | 3 | 3 | **3** |
| C-4.2 | 2 | 2 | 3 | 3 | **3** |
| C-4.3 | 2 | 2 | 3 | 3 | **3** |
| C-5.1 | 2 | 3 | 3 | 3 | **3** |
| **C-5.2** | 2 | 1 | 2 | 2 | **2** |
| C-6.1 | 2 | 3 | 3 | 3 | **3** |
| C-7.1 | 2 | 1 | 3 | 3 | **3** |
| C-7.2 | 2 | 1 | 3 | 3 | **3** |
| C-7.3 | 2 | 1 | 3 | 3 | **3** |
| C-7.4 | 3 | 2 | 3 | 3 | **3** |
| C-8.1 | 2 | 2 | 2 | 3 | **3** |
| C-8.2 | 2 | 3 | 3 | 3 | **3** |
| C-8.3 | 2 | 2 | 3 | 3 | **3** |
| C-8.4 | 1 | 3 | 3 | 3 | **3** |
| C-9.1 | 1 | 3 | 2 | 1 | **3** |
| C-9.2 | 2 | 3 | 2 | 1 | **3** |
| C-9.3 | 1 | 3 | 1 | 1 | **3** |
| C-9.4 | 1 | 3 | 1 | 1 | **3** |
| C-9.5 | 2 | 3 | 1 | 1 | **3** |
| C-10.1 | 1 | 3 | 2 | 3 | **3** |
| C-10.2 | 1 | 3 | 2 | 3 | **3** |
| C-10.3 | 2 | 3 | 3 | 3 | **3** |

**Critical observation: M_i = 3 on 29 of 30 criteria; M_i = 2 only on C-5.2.**

Because the rubric caps at 3, D cannot exceed M_i = 3 on any criterion. D's only path to survival is **D_C-5.2 = 3** (exceeding M=2 on the lone non-saturated criterion). If D scores ≤ 2 on C-5.2, D is strictly dominated.

This single-criterion bottleneck is itself an outcome of the framework: at least one of A, B, or C natively satisfies every criterion except C-5.2 (sentence-level evidence-marker enforcement). The hybrid's only structural opportunity is to satisfy C-5.2 in a way no singleton does.

### 1.3 Within-Candidate-D sub-substrate selection

Per framework §5.4, two hybrid configurations are conceivable (with a third sub-variant for the pivotal criterion):

**H1 — SQLite (cells, sources, governance) + Markdown (specifications) + YAML (configuration).** Cells, sources, connections, decisions, governance live in SQLite. Specifications remain markdown for human readability. Governance configuration in YAML. Cross-store boundary: spec_id on the relational side references markdown filename; markdown frontmatter references spec_id. Cross-store integrity is application-enforced.

**H2 — RDF/Jena (relationships, cells, semantic structure) + SQLite (tabular records — decisions, gaps, slugs).** Semantic graph for cell-level data, supersedence, relationships. Tabular records in SQLite for SQL convenience. Cross-store boundary: RDF graph references SQLite tabular records by stable IDs.

**H1' — H1 with structured-marker convention.** As H1 but with mandate that evidence markers appear in unambiguous syntactic form (e.g., `[●]` / `[○]` end-of-sentence tokens) for regex-clean enforcement. The "structured" variant is an enforcement convention that could in principle be applied to any candidate, including A alone — it does not require a hybrid form.

**Operative configuration: H1.** H1 preserves markdown's editing affordance for the highest-volume content type (specifications), is the most solo-author-tractable hybrid, and represents D's strongest argument for survival because it could plausibly score 3 on C-5.2 if the structured-marker convention provides regex-clean enforcement. H2 doubles up on database-substrate operational burden without the prose-handling benefit; if H1 is dismissed, H2 is dismissed by transitivity (operational scores can only worsen).

This sub-decision is captured as **D-0133 D-METH/DG-REVIEW** below.

---

## 2. Per-criterion evaluation of Candidate D (H1)

For each criterion, four-question template applied. Where H1's evaluation is identical to one of the constituent substrates' evaluations, scoring is noted briefly; where the hybrid burden materially affects the score, the analysis is detailed.

### 2.1 Cluster I — Entity & relationship

#### C-1.1 — Entity-type expressiveness
H1: Entities split across SQLite tables (cells, sources, decisions, etc.) and markdown files (specifications). Adding a new entity type requires deciding which substrate it lands in plus updating the cross-store boundary mapping. This is an extra step that single-substrate candidates do not impose. **Score: 2** (adapted, moderate cost — substrate-routing decision is the hybrid burden).

#### C-1.2 — Relationship-type expressiveness
H1: Cross-store relationships (spec markdown ↔ cell SQLite row) are application-enforced; intra-store relationships (cell ↔ source) are FK-enforced. The cross-store boundary is the failure surface no single-substrate candidate has. **Score: 2** (write-time integrity holds within each substrate but not across the boundary).

#### C-1.3 — Within-population variability **[Weight 3]**
H1: Cell rows in SQLite. Same as Candidate B. **Score: 3** (native within the relational substrate).

#### C-1.4 — Sub-population inheritance
H1: Population/sub-population in SQLite (per Candidate B's score 2 — inheritance not native to relational). **Score: 2**.

**Cluster I subtotal D: 2+2+3+2 = 9 (weighted: 4+4+9+4 = 21 of max 27 = 78%)**

### 2.2 Cluster II — Cell-level state

C-2.1, C-2.2, C-2.3 all live in SQLite per H1; all three score **3** (native within the relational substrate, same as Candidate B).

**Cluster II subtotal D: 18 of max 18 = 100%**

### 2.3 Cluster III — Co-1 schema discipline

C-3.1: Co-1 fields on `evidence_source` SQLite table. Same as B. **Score: 3**.

**Cluster III subtotal D: 9 of max 9 = 100%**

### 2.4 Cluster IV — Synthesis metadata

C-4.1, C-4.2, C-4.3 all in SQLite. All score **3**.

**Cluster IV subtotal D: 18 of max 18 = 100%**

### 2.5 Cluster V — Verification

#### C-5.1 — Verification-status state machine
SQLite enum + transition table. **Score: 3**.

#### C-5.2 — Evidence markers ●/○ enforced **[The pivotal criterion for elimination]**

The pivotal evaluation. The 4-question template applied with care:

1. **Native, adapted, or absent?** H1's specifications live in markdown; cell-level metadata lives in SQLite. Sentence-level evidence markers are inherently a property of spec prose. Three options for H1 enforcement:

   **(a) Tokenizer on markdown body.** Same as Candidate A's score 1 — sentence boundary detection is non-trivial; tokenizer accuracy bounds enforcement. *Score 1.*

   **(b) Sentence-level normalization to SQLite.** Specifications normalized to `specification_sentence` table with evidence_marker column. Same as Candidate B's option (a) — substantial extraction work; defeats the H1 premise of preserving markdown for prose. *Score 2.*

   **(c) Structured-marker convention in markdown + regex enforcement (H1' variant).** Mandate that markers appear in a structured form (e.g., end-of-sentence `[●]` or `[○]` token) such that regex enforcement is unambiguous. Validator becomes a regex sweep. **The hybrid form does not structurally improve over plain markdown for this — option (c) is available to Candidate A as well.** A literate-markdown candidate with structured markers achieves the same score whether it stores cells in SQLite, in YAML, or in RDF.

   The H1 hybrid provides no structural advantage on C-5.2 over Candidate B alone or Candidate A with structured markers. Sentence-level enforcement is determined by how prose is processed and what marker convention is mandated, not by which substrate non-prose lives in.

2. **Adaptation cost?** Same as Candidate B's option (a) — 2–3 sessions for sentence normalization.
3. **Operational risk?** Medium — same as B.
4. **Downstream binding?** Same as B.

**Score: D_C-5.2 = 2** (the hybrid does not exceed B/C on this criterion because the structural advantage isn't from hybridization).

This is the dispositive score. **D_C-5.2 = 2 = max(A, B, C) on C-5.2. D does not strictly exceed M on this criterion — and C-5.2 was D's only path to survival.**

**Cluster V subtotal D: 3+2 = 5 (weighted: 6+4 = 10 of max 12 = 83%)**

### 2.6 Cluster VI — Cross-cutting axes

C-6.1: SQLite WHERE on join tables. **Score: 3**.

**Cluster VI subtotal D: 6 of max 6 = 100%**

### 2.7 Cluster VII — Navigation / audience

All four navigation-mode criteria are SQL queries against SQLite (where cells live). The hybrid does not impair the query-mode strengths of the relational substrate.

C-7.1, C-7.2, C-7.3 all score **3**.
C-7.4 (questions-led, weight 3): Question entity in SQLite when B3 ships; SQL filter. **Score: 3**.

**Cluster VII subtotal D: 27 of max 27 = 100%**

### 2.8 Cluster VIII — Time model

#### C-8.1 — Entity-level versioning per A9
H1 places A9 entities in SQLite. Same as B's score 2 (retrofit converter cost remains). **Score: 2**.

C-8.2: SQLite supersedence_link table. **Score: 3**.
C-8.3: SQLite. **Score: 3**.
C-8.4 (weight 1): SQL date arithmetic. **Score: 3**.

**Cluster VIII subtotal D: 2+3+3+3 = 11 (weighted: 4+6+6+3 = 19 of max 21 = 90%)**

### 2.9 Cluster IX — Operational

The hybrid burden falls hardest in this cluster. Operational cost is approximately the SUM of B's relational cost AND A's markdown cost AND a new cross-store boundary cost — not the minimum.

#### C-9.1 — CI validation tractability **[Weight 1]**
H1 CI must validate both substrates plus the cross-store boundary (spec_id consistency between markdown frontmatter and SQLite rows). More CI surface than either B (just SQLite) or A (just markdown). **Score: 1** (worse than B's 2 and A's 3).

#### C-9.2 — Solo-author operability **[Weight 2]**
The author edits markdown for prose and SQL/CLI for cells. Mental model spans both. Cross-store boundary discipline is on the author. **Score: 1** (worse than B's 2 and A's 3 — the hybrid burden on a solo author is acute; D-03 binding force applies).

#### C-9.3 — Audit-trail preservation across migration **[Weight 1]**
Migration is from current state to H1 (markdown stays as markdown for specs; SQLite is new). Migration cost is between A's 0 and B's 4–6 sessions — call it 3–5 sessions for the partial migration plus cross-store boundary tooling. **Score: 1**.

#### C-9.4 — Migration cost from current 1,098 records **[Weight 1]**
Same as C-9.3. **Score: 1**.

#### C-9.5 — A10/A12/A13 integration cost **[Weight 2]**
A10/A12/A13 migrate to SQLite per H1. Validator rewrites required. **Score: 1**.

**Cluster IX subtotal D: 5 (weighted: 7 of max 21 = 33%)**

D's Cluster IX is materially worse than A (100%) and B (48%), tied with C (33%). The hybrid burden is the cost driver.

### 2.10 Cluster X — Sustainability

C-10.1 (weight 1): Mix of markdown (max longevity) and SQLite (durable but tool-dependent); bounded by SQLite. **Score: 2** (same as B).
C-10.2 (weight 1): Same as B. **Score: 2**.

#### C-10.3 — Migration-out cost (S-05) **[Weight 2]**

Per D-0111, evaluate against the 5 deliverables for H1:

1. **Full data export.** Two operations (markdown copy + SQLite dump). Both straightforward.
2. **Relationship preservation.** Within-substrate native; cross-store boundary requires explicit mapping export.
3. **State preservation.** Cell-level state in SQLite preserves natively; markdown content preserves trivially.
4. **Schema mapping document.** ~1.5 sessions (more complex than B alone — must specify how SQLite + markdown re-import into target).
5. **Export tooling cost.** ~2 sessions. **Within budget but tighter than B's headroom.**

All 5 deliverables satisfied. **PASS**.

**Score: 2** (adapted, moderate cost — two-substrate export is more work than single-substrate; within S-05 standard but not the trivial export of A).

**Cluster X subtotal D: 6 (weighted: 8 of max 12 = 67%)**

---

## 3. D's score summary

### 3.1 Per-criterion score table

| Criterion | Weight | D | Weighted |
|---|---|---|---|
| C-1.1 | 2 | 2 | 4 |
| C-1.2 | 2 | 2 | 4 |
| C-1.3 | 3 | 3 | 9 |
| C-1.4 | 2 | 2 | 4 |
| C-2.1 | 2 | 3 | 6 |
| C-2.2 | 2 | 3 | 6 |
| C-2.3 | 2 | 3 | 6 |
| C-3.1 | 3 | 3 | 9 |
| C-4.1 | 2 | 3 | 6 |
| C-4.2 | 2 | 3 | 6 |
| C-4.3 | 2 | 3 | 6 |
| C-5.1 | 2 | 3 | 6 |
| C-5.2 | 2 | 2 | 4 |
| C-6.1 | 2 | 3 | 6 |
| C-7.1 | 2 | 3 | 6 |
| C-7.2 | 2 | 3 | 6 |
| C-7.3 | 2 | 3 | 6 |
| C-7.4 | 3 | 3 | 9 |
| C-8.1 | 2 | 2 | 4 |
| C-8.2 | 2 | 3 | 6 |
| C-8.3 | 2 | 3 | 6 |
| C-8.4 | 1 | 3 | 3 |
| C-9.1 | 1 | 1 | 1 |
| C-9.2 | 2 | 1 | 2 |
| C-9.3 | 1 | 1 | 1 |
| C-9.4 | 1 | 1 | 1 |
| C-9.5 | 2 | 1 | 2 |
| C-10.1 | 1 | 2 | 2 |
| C-10.2 | 1 | 2 | 2 |
| C-10.3 | 2 | 2 | 4 |

### 3.2 D's cluster totals

| Cluster | Weighted | Max | Ratio |
|---|---|---|---|
| I | 21 | 27 | 78% |
| II | 18 | 18 | 100% |
| III | 9 | 9 | 100% |
| IV | 18 | 18 | 100% |
| V | 10 | 12 | 83% |
| VI | 6 | 6 | 100% |
| VII | 27 | 27 | 100% |
| VIII | 19 | 21 | 90% |
| IX | 7 | 21 | 33% |
| X | 8 | 12 | 67% |
| **Total** | **143** | **171** | **84%** |

**Candidate D (H1) weighted score: 143 / 171 = 84%.**

This is informational only — the eliminator test (§4) determines whether D proceeds to comparative scoring at Session 7, regardless of weighted total. (Note: 84% is between A's 77% and B's 89%, but the test is per-criterion strict-dominance, not weighted total.)

---

## 4. D-0112 Eliminator Test

### 4.1 Per-criterion comparison D vs M

| Criterion | M | D | D > M? |
|---|---|---|---|
| C-1.1 | 3 | 2 | No (loss) |
| C-1.2 | 3 | 2 | No (loss) |
| C-1.3 | 3 | 3 | No (tie) |
| C-1.4 | 3 | 2 | No (loss) |
| C-2.1 | 3 | 3 | No (tie) |
| C-2.2 | 3 | 3 | No (tie) |
| C-2.3 | 3 | 3 | No (tie) |
| C-3.1 | 3 | 3 | No (tie) |
| C-4.1 | 3 | 3 | No (tie) |
| C-4.2 | 3 | 3 | No (tie) |
| C-4.3 | 3 | 3 | No (tie) |
| C-5.1 | 3 | 3 | No (tie) |
| **C-5.2** | **2** | **2** | **No (tie)** |
| C-6.1 | 3 | 3 | No (tie) |
| C-7.1 | 3 | 3 | No (tie) |
| C-7.2 | 3 | 3 | No (tie) |
| C-7.3 | 3 | 3 | No (tie) |
| C-7.4 | 3 | 3 | No (tie) |
| C-8.1 | 3 | 2 | No (loss) |
| C-8.2 | 3 | 3 | No (tie) |
| C-8.3 | 3 | 3 | No (tie) |
| C-8.4 | 3 | 3 | No (tie) |
| C-9.1 | 3 | 1 | No (loss) |
| C-9.2 | 3 | 1 | No (loss) |
| C-9.3 | 3 | 1 | No (loss) |
| C-9.4 | 3 | 1 | No (loss) |
| C-9.5 | 3 | 1 | No (loss) |
| C-10.1 | 3 | 2 | No (loss) |
| C-10.2 | 3 | 2 | No (loss) |
| C-10.3 | 3 | 2 | No (loss) |

**D > M on 0 of 30 criteria.**

Tally: **0 wins · 18 ties · 12 losses · 30 total.**

### 4.2 Test outcome

Per D-0112: "Candidate D survives elimination iff there exists at least one criterion `i` such that `D_i > M_i` (strict inequality). If for all 30 criteria `D_i ≤ M_i`, Candidate D is strictly dominated and dismissed without further evaluation."

**D_i ≤ M_i for all 30 criteria. Candidate D is strictly dominated.**

The pivotal criterion was C-5.2 — the only criterion where M < 3 and thus the only criterion where D could exceed by scoring 3. D scored 2 on C-5.2, tying B and C, not exceeding them. The hybrid form does not provide a structural advantage on sentence-level marker enforcement because spec text is markdown either way; sentence-level enforcement is determined by how prose is processed and what marker convention is mandated, not by which substrate non-prose data lives in.

**Candidate D is dismissed.** Session 7 comparative scoring proceeds with Candidates A, B, C only.

### 4.3 Why D was dismissed without surprise

The framework's §7.1 conjectured that Candidate D would likely be strictly dominated. The conjecture rested on three structural observations now confirmed mechanically:

1. **A hybrid is bounded above by the best of its constituent substrates on most criteria.** A hybrid combining substrate X and substrate Y can score at most max(X_i, Y_i) on criterion i for most criteria — and often less due to cross-store boundary cost. In the concrete H1 evaluation: D matched B's score on most criteria where B scored 3; D underperformed both A and B in Cluster IX where the hybrid burden compounds.
2. **Operational criteria (Cluster IX) compound the hybrid burden.** Operating two substrates is approximately the SUM of their individual operational costs, not the minimum. D's Cluster IX scored 33% — at the C-substrate floor.
3. **Solo-author posture (D-03) is hostile to hybrids.** Cognitive overhead of two stores — when to use which, how to maintain cross-store integrity — is itself a binding constraint. The framework anticipated this and built the eliminator test to dismiss D when no doctrinal-binding criterion uniquely favors it.

The eliminator test is functioning as designed. **D is not dismissed because its weighted total is low** (it's 84%, sitting between A's 77% and B's 89%); D is dismissed because **no single criterion uniquely favors the hybrid form** over the best singleton.

**Transitivity to H2:** Configuration H2 (RDF + SQLite, no markdown) replaces markdown with RDF for prose handling, doubling up on database-substrate operational burden without preserving the markdown editing workflow. H2's Cluster IX would be worse than H1's (two databases instead of one + markdown); H2's C-5.2 would not improve (RDF does not natively express sentence-level prose markers any more than SQLite does). H2 is dismissed by transitivity — it cannot satisfy any criterion that H1 cannot.

---

## 5. Decision-capture

### 5.1 D-0133 — Within-Candidate-D substrate: H1 (SQLite + Markdown + YAML)

| Field | Value |
|---|---|
| category | D-METH |
| delegation | DG-REVIEW |
| review_status | PENDING |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108 |

DG-REVIEW for the methodological commitment. This decision becomes operationally moot once D-0134 dismisses Candidate D, but is captured for evaluation-trail completeness — the test outcome depends on which hybrid configuration was tested.

### 5.2 D-0134 — Candidate D dismissed under D-0112 strict-dominance test

| Field | Value |
|---|---|
| category | D-METH |
| delegation | DG-REVIEW |
| review_status | PENDING |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108, D-0110, D-0112, D-0113, D-0119, D-0121, D-0132, D-0133 |

DG-REVIEW because dismissal of a framework-named candidate is a methodological commitment, not a routine evaluation outcome. Project-owner review confirms the eliminator test applied correctly and the dismissal is well-founded. Session 7 input set is reduced from {A, B, C, D} to {A, B, C}.

### 5.3 D-0135 — Candidate D scored 143 / 171 (84%) — informational

| Field | Value |
|---|---|
| category | D-OP |
| delegation | DG-AUTO |
| review_status | NA |
| model_routing | opus/150/synth |
| effort_level | 150 |
| predecessors | D-0108, D-0110, D-0113, D-0133, D-0134 |

DG-AUTO. Score recorded for completeness; D is dismissed regardless of weighted total because the dismissal is per-criterion strict-dominance.

---

## 6. Status

| Field | Value |
|---|---|
| B1 Session 6 | COMPLETE |
| Candidate D (H1) score | 143 / 171 (84%) — informational |
| D-0112 eliminator test | **D dismissed** (strictly dominated; D_i ≤ M_i on all 30 criteria; 0 wins, 18 ties, 12 losses) |
| Transitivity to H2 | H2 dismissed (cannot satisfy any criterion H1 cannot) |
| Survivors entering Session 7 | Candidates A, B, C |
| Decisions captured | D-0133, D-0134, D-0135 |
| Working session counter | 8 → 9 |
| Session log | `sessions/session_2026-05-02-b1-s6.md` |
| Predecessor | `sessions/session_2026-05-02-b1-s5.md` |
| Next session | B1 Session 7 — Comparative scoring (A vs B vs C) + dismissed-alternatives drafting |

---

## 7. Session 7 next-action

**Session 7 = Comparative scoring across A, B, C + dismissed-alternatives drafting.**

Inputs: Sessions 3, 4, 5 deliverables (per-candidate scores and cluster-level analysis); this session's dismissal of D.

Session 7 produces:
- Cross-candidate comparison matrix (per-criterion, per-cluster, weighted totals)
- Selection-question framing: B vs C is the close call (152 vs 155, 89% vs 91%); A's distinct profile (operational at 100%, navigation at 44%) makes the A-vs-(B|C) tradeoff a different question
- Weighted-difference threshold or selection rule (e.g., is +3 weighted points C-over-B decisive given C's worse Cluster IX?)
- Dismissed-alternatives draft for the architecture/storage-derivation.md final document (D dismissed per this session; PostgreSQL/DuckDB dismissed within Candidate B per D-0120; Blazegraph/Neo4j/Memgraph dismissed within Candidate C per D-0131)

Output: `workplan/b1-comparative-scoring.md` (~400 lines).

Out of scope for Session 7: final selection (Session 8) and architecture writeup (Session 8) and schema spec (Session 9).
