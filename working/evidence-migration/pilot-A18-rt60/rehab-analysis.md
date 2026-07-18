# Pilot — A-18 (RT60 in Occupied Learning and Listening Spaces)

*Slug: `room-acoustic-performance` · population tag: NDV · `evidence_state`: RETRACTED-PRE-REHAB ·
citation-mining ✓ · supersession ✓ · co1 ✗ · pico ✗ · jurisdictions-searched ✗.*

Chosen as first pilot because it is the **furthest-along** slug (citation-mining + supersession already
done), has a **strong Tier-1 base** (16 clinical studies), a **physics-based parameter** (RT60 — the clean
case for the Kawa universal-transfer rule), and a **richly multi-jurisdictional code-floor**
(ANSI/BB93/DIN/NS/UNI/AS-NZS/GB/AIJES/SBi) — the ideal stress-test for *convergence ≠ evidence*.

All figures below are read from `data/guidebook.db` (grounded) or retrieved with a cited URL. A **separate
guilty-until-proven verifier agent** independently re-checked the load-bearing claims; its verdict is in
`verifier-verdict.md` (§ Verifier).

---

## The headline: grading ≠ rehabilitation

A-18's **value derivation is already excellent** — four `evidence_cell_state` rows, evidence-graded,
`code_floor_only=0` (i.e., ● evidence-derived, not ◐ code-derived):

| # | design_scale | state | value (s) | tier_basis | governing_refs | condition (population) |
|---|---|---|---|---|---|---|
| 1 | population | **stated** | **0.3** | T1 | REF-00325, 00577, 00576, 00578 | pediatric hearing-aid/CI (HI children), ≤283 m³ |
| 2 | universal | **stated** | **0.55–0.57** | T1 | REF-00581, 00577 | typical-hearing classroom |
| 3 | population | provisional | 0.5 | T2 | REF-00569 | dementia care |
| 4 | population | provisional | 0.4 | T3 | REF-00561 | autism |

Yet the slug is still `RETRACTED-PRE-REHAB`. **The migration debt is not the value — it is the layers
around it:**

| rehabilitation layer | A-18 today | gap |
|---|---|---|
| Person / OT mode | absent from `evidence_cell_state` (0 person rows anywhere in the DB) | but `items.pmp_delta_min=0.05, direction=down` **is** a real Person-mode signal — un-migrated into a cell |
| Co-1 lived experience | `co1_pass_count=0`; no lived-experience row | HI people's lived experience of reverberant space absent |
| Walled-off code-floor (◐) | none | 10 linked standards, no cell recording "codes = floor, distinct from evidence" |
| DAR (Design for Adaptable Readiness) | none | acoustic treatment is highly retrofittable — a real DAR story is missing |
| `population_code` on the population rows | **NULL** on all | the 0.3s value is *for HI children* but the structured field is empty |
| `item_population_links` | **0 for A-18** | no bottom-up capacity linkage, despite population-specific values |
| jurisdiction/language coverage record | `jurisdictions_searched=0` | 13 jurisdictions of standards linked but never recorded as a searched matrix |

This is the whole thesis in one cell: the corpus migrated the **number** and even graded it well, but the
**rehabilitation** (person mode, lived experience, the floor/evidence separation, adaptability, the
coverage record) never happened.

---

## Value derivation — three modes, two directions, DAR (S8)

**TARGET layer (performance value):**

- **Universal (top-down floor)** — RT60 ≤ **0.55–0.57 s** for typical-hearing occupants (● T1, DB row 2).
  This is the design-for-all floor: population-agnostic, fixed.
- **Population (evidence range)** — RT60 ≤ **0.3 s** for hearing-impaired children (● T1, DB row 1);
  ≤ 0.5 s dementia (◑ T2, provisional); ≤ 0.4 s autism (◑ T3, provisional). Median-of-range logic applies
  *within* a population, not across them — these are distinct populations, not a single range (do **not**
  average 0.3/0.4/0.5).
- **Person (bottom-up, OT within range)** — the DB does not hold a person row, but `items.pmp_delta_min =
  0.05 (down)` encodes it: an OT resolves the person's point by tightening the population value by up to
  **0.05 s** for greater individual need. Provenance-strength: **`direct` (from `items` PMP field)** but
  **un-migrated into a cell** — a determination is owed.

**TECHNIQUE layer (how to hit it):** porous absorption (ceiling NRC ≥0.85 per A-02; fabric wall panels NRC
≥0.70 per A-06), avoiding parallel hard surfaces (flutter echo, A-07). *Graded separately* — the technique
items exist but their own cell-states are a separate rehabilitation.

**DAR layer:** acoustic absorption is largely **retrofittable without structural change** (demountable
ceiling tiles, applied wall panels) — a strong DAR story (low deferral penalty). Provision it: ceiling grid
+ wall blocking that *accepts* future higher-NRC treatment. Absent from the current record; venture as an
approach.

### Convergence ≠ evidence (the S4/S8 demonstration — grounded)

- **Evidence-based best practice (●, T1):** RT60 ≤ **0.3 s** for HI children, ≤283 m³ (DB row 1, governing
  refs present).
- **Code-floor (◐, T4):** ANSI/ASA S12.60-2010 Part 1 requires RT60 ≤ **0.6 s** (unoccupied) for core
  learning spaces ≤283 m³ — *retrieved*, not asserted
  ([ANSI Blog](https://blog.ansi.org/ansi/ansi-asa-s12-60-part-1-2010-r2020-school-acoustics/),
  [Armstrong](https://www.armstrongceilings.com/commercial/en/articles/classroom-acoustics-ansi-standard.html)).

The code-floor is **~2× laxer** than the T1 evidence-based target for the same space size. **Building only
to the ANSI floor would leave hearing-impaired children in roughly double the reverberation the Tier-1
evidence indicates they need.** That is *convergence ≠ evidence* made concrete: the ANSI value is a
compliance **floor** (◐), never the best-practice **anchor** (●).

> **Caveat, flagged honestly (S3) — pending verifier:** the 0.3 s figure's condition and the ANSI 0.6 s
> figure may differ on **occupied vs unoccupied** RT (ANSI 0.6 s is *unoccupied*; occupied RT is lower as
> bodies add absorption). If so, the raw "2×" understates or overstates the true gap and needs an
> occupied-basis restatement. The direction of the finding (evidence target is materially tighter than the
> code floor) is robust; the exact multiple is caveated until the bases are reconciled. **The separate
> verifier was specifically tasked to test this** — see § Verifier.

### Un-migrated code-floor VALUES (a real gap, admitted)

The DB catalogues the 10 acoustic standards as source rows but records **none of their numeric RT60
thresholds** in any structured field (`bpc_note`/`notes`/`derivation_chain` hold only provenance text). So
a statement like "the codes converge on 0.4–0.6 s" is **not grounded in the DB** and is not asserted here —
only the single ANSI value, which was retrieved. Extracting each standard's threshold (in its home
language) is a named work item, and where a threshold is not yet retrieved the code-floor cell reads
`absent`, not a guessed number.
