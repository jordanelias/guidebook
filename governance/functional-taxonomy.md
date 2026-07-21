# Functional Taxonomy — Two-Layer Model (Axes × Profiles)

**Status: PROPOSED — pending owner ratification.** See
`decisions/DR-2026-07-21-two-layer-functional-taxonomy.md` for the decision wrapper,
alternatives considered, and ratification checklist.
**This document states doctrine; it executes nothing.** No `populations` row, item link,
or skill file changes until ratification. Staged schema:
`working/taxonomy/staged_schema_functional_axes.sql` (deliberately outside
`scripts/migrations/` so `db.py migrate` cannot pick it up).

---

## §0 Why taxonomy is the curation gate

Every research entity downstream of this document — slugs, search-log entries, BPC
files, evidence rows, item links — inherits its selection and attachment rules from the
population taxonomy. A source is only findable if some entity names the thing it is
evidence *about*; it is only curatable if some entity exists for it to attach *to*. The
session audit of 2026-07-21 showed both failure modes live:

- **Findability failure:** vestibular/balance function has no entity → zero slugs, zero
  searches, zero ICF `b`-code anchors corpus-wide → an entire evidence base is
  structurally invisible, regardless of search effort.
- **Attachment failure:** evidence about MS thermal intolerance attaches to a *diagnosis*
  parented under "neurological" — an etiological shelf — rather than to the
  thermoregulation function it is actually about, so sibling populations with the same
  functional demand (SCI poikilothermia, POTS, older adults) cannot reach it.

The fix is not more entities of the same kind. It is separating the two kinds that are
currently fused: **what a body cannot do in an environment** (functional axes) and
**who the evidence is about** (profiles).

## §1 The defect being fixed

The current `populations` table (22 rows) plus the unmodeled supplementary-volume
archetypes (CHD/LPA/EXH/BAR) mix three ontologies under one key:

| Kind | Current members | Problem |
|---|---|---|
| Functional axes | MOB, UPL, VIS, DEAF, PAIN, OFS, SENS | Correct kind, wrong grain (MOB fuses ambulant+wheeled; VIS fuses low-vision+blind) |
| Diagnoses | MS, POTS, MCAS, CFS, EPI, SCI, ADHD, AUT, PCS, DEM, MH, NEU | Category-thinking §1.3 forbids; several mis-parented (MS←NEU, MCAS←OFS); PCS defined two incompatible ways (DB: post-concussion/cognitive; FDA skill: post-COVID/autonomic) |
| Archetypes | CHD, LPA, EXH, BAR | Body-envelope classes, absent from the table entirely |

Verified consequences (session 2026-07-21, live DB): the corpus contains **zero** ICF
`b`-codes (body functions) — impairment information therefore smuggles in as diagnoses;
`d415` (maintaining body position) maps to no population; SENS carries 1 item link
despite sensory processing being the theoretical core of the NDV corpus; the FDA skill
audits against codes (`ABI`, `ASD`, `LOW-VISION`) that do not exist in the canonical
table; `evidence_population_match.target_population` is uncontrolled free text.

## §2 Layer 1 — Functional axes

An **axis** is an architect-actionable functional-demand primitive: a capacity of the
person that a design parameter can meet, compensate, or fail. Axes are anchored on ICF
**body functions (`b`)** mapped to the **activities (`d`)** they limit. Axes are the
canonical attachment point for mechanism and threshold evidence, and for
`item_axis_links`. An axis with zero linked slugs or items is a *visible, queryable
coverage hole* — that visibility is a design goal of this model, not an error state.

### §2.1 The axis register (17)

| Axis | Name | ICF `b` anchors | ICF `d` anchors | Mechanism (one line) | Status |
|---|---|---|---|---|---|
| `AX-AMB` | Ambulation & gait | b770, b730 | d450, d455, d460 | Walking, stairs, distance, gradients for ambulant users | ESTABLISHED |
| `AX-WHM` | Wheeled mobility & transfer | b730, b710 | d465, d420, d410 | Wheelchair/scooter geometry, turning, transfer | ESTABLISHED |
| `AX-REA` | Reach & manipulation | b730, b710 | d440, d445 | Reach ranges, grip, operating force, bilateral/one-hand use | ESTABLISHED |
| `AX-BAL` | Balance & postural stability | **b235, b240** | **d415**, d410 | (i) biomechanical fall risk; (ii) vestibular-sensory precipitants — environments that *induce* dizziness (pattern, glare, glazed edges, escalators, large open visual fields) | **STUB — new** |
| `AX-STA` | Stamina & orthostatic tolerance | b455, b130 | d230, d450, d455 | Exertion limits, standing intolerance, PEM; rest/distance/seating economy | ESTABLISHED |
| `AX-PAI` | Pain-limited function | b280 | d410, d450, d640 | Nociceptive load: impact, vibration, pressure, cold-triggered pain | ESTABLISHED |
| `AX-THR` | Thermoregulation & autonomic tolerance | b550 | d230 | Impaired heat/cold regulation (Uhthoff, poikilothermia); ambient stability, zoned control | PARTIAL |
| `AX-CHM` | Chemical & air-quality tolerance | b435, b440 | d230 | Immune/respiratory reaction to VOCs, fragrance, particulates | PARTIAL |
| `AX-VIS-L` | Low vision | b210 (partial) | d460, d166 | Residual-vision use: contrast, lighting, glare, size | ESTABLISHED |
| `AX-VIS-N` | Non-visual function | b210 (profound) | d460 | Tactile/auditory substitution: TWSI, acoustic differentiation, braille | ESTABLISHED |
| `AX-AUD` | Auditory access & alerting | b230 | d310–d329, d115 | Speech access, alert receipt, assistive listening | ESTABLISHED |
| `AX-SPR` | Sensory processing & modulation | b156, b140 † | d230, d160 | Hyper/hypo-reactivity, sensory load, trigger avoidance (incl. photic) | ESTABLISHED (mislabeled as pop. SENS) |
| `AX-COG-O` | Orientation & wayfinding cognition | b114, b144 | d460, d175 | Memory, spatial cognition, sequencing, legibility | ESTABLISHED |
| `AX-COG-L` | Learning & information access | b117, b167 | d166, d310, d315 | Comprehension of environmental information: Easy Read, pictograms, symbol systems | **STUB — new** |
| `AX-COM-E` | Expressive communication | b320, b330 | d330–d349, d350 | Producing speech/sign/AAC in the environment: counter dwell, sightlines for sign (d340), acoustic conditions for device output | **STUB — new** |
| `AX-ARO` | Arousal, stress & emotional regulation | b152 | d240 | Threat appraisal, retreat, predictability, defensible space | **STUB — new (currently FDA-scoped-out)** |
| `AX-CNT` | Continence & elimination urgency | b620, b525 | d530 | Urgency/frequency as plan-driver: proximity, provision count, management space (ostomy/catheter) | **STUB — new** |

† ICF represents sensory *modulation* poorly (a known limitation); `b156/b140` are the
closest anchors. This is recorded honestly rather than forced — consistent with
thinking-tool posture.

Axes deliberately **not** created, with reasons: respiratory (decomposes to `AX-STA` +
`AX-CHM`; residual O₂-equipment egress note belongs to the egress thread); anthropometric
fit (archetypes are profiles interacting with `AX-REA`/`AX-WHM` envelopes, not a
capacity); interoception (research-immature; parked); fluctuation/episodic capacity
(cross-cutting temporal property of several axes; handled as a profile attribute
`fluctuating: yes/no`, candidate future axis).

### §2.2 Specifications for the six new axes

**`AX-BAL` — Balance & postural stability.** Two distinct mechanisms, both currently
homeless: *(a) biomechanical* — fall risk under gait/transfer load (handrails, stair
geometry, slip resistance already exist as items but link only via MOB); *(b)
vestibular-sensory* — the environment as symptom *precipitant*: high-contrast repeating
patterns, specular floors, glass balustrades at height, escalators/travelators, large
uniform visual fields. Mechanism (b) has zero corpus presence (verified). Feeding slug
(proposed, queued): `vestibular-balance-built-environment`. Falsification: axis merges
back into `AX-AMB` if research shows precipitant guidance fully reduces to existing
fall-prevention parameters. Prevalence and mechanism claims **require Tier-anchored
sourcing before any threshold enters an item** — nothing in this document is citable
evidence.

**`AX-COG-L` — Learning & information access.** Un-proxies intellectual disability
(currently "proxied through DEM and NDV" per ToC note; GAP-277 asks the existence
question this axis answers). Curates: symbol/pictogram comprehension, Easy Read
signage, plain-language wayfinding, dwell-time tolerance. Distinct from `AX-COG-O`
(orientation) because the design responses differ: legible *information* vs legible
*space*.

**`AX-COM-E` — Expressive communication.** Receiving-side communication lives in
`AX-AUD`/`AX-VIS-*`; the producing side has no home. Curates: reception-counter design
for AAC users (shelf, sightline, time), acoustic conditions for speech-generating
devices, sign-production sightlines and lighting (d340 — shared custody with the
Deaf-cultural profile's DeafSpace corpus), intercom/entry systems with non-speech paths
(H-04). Bulk of communication *support* remains human/service scope — out of remit; the
built-environment residual is this axis.

**`AX-ARO` — Arousal, stress & emotional regulation.** `b152/d240` are currently
scoped **out** by the FDA — which leaves MH represented only by proxy codes (routine,
retreat, interpersonal). Ratifying this axis rescinds that scope-out for the
architecturally actionable subset: defensible seating (G-01), retreat provision (A-16,
D-05), stimulus gradient (F-01), sightline control, exit legibility. Trauma-informed
design evidence curates here.

**`AX-CNT` — Continence & elimination urgency.** d530 is Tier-A spatially dependent,
yet all bathroom entities are *spatial-geometry* framed (grab bars, turning). This axis
curates the physiological drivers: urgency→proximity and provision-count parameters,
frequency→distribution, management space (ostomy/catheter/Changing Places-class
provision as need-driven, not checkbox). Serves MS, SCI, OFS, IBD/ostomy (future
profile), older-adult, PAIN.

**`AX-CHM` — Chemical & air-quality tolerance.** Names the axis the
`air-quality-voc-chemical-sensitivity` slug already feeds; re-homes MCAS correctly
(immune mechanism, not orthostatic association) and gives asthma/MCS evidence an
attachment point. Items F-02, F-04.

## §3 Layer 2 — Profiles

A **profile** is who evidence is about: a diagnostic, identity-cultural, demographic,
anthropometric, compound, or umbrella grouping, expressed as **weighted mappings onto
axes** *plus* **authored emergent content** that is never derived from, and never
reduced to, the axis layer.

**The emergence guarantee (anti-reductionism clause).** Mature design corpora —
DeafSpace, dementia-friendly design, ASPECTSS, age-friendly design, DBL tactile-first
practice — are *authored at profile level* and are not reconstructable as sums of axis
guidance. Profile-level evidence, and all Co-1 lived-experience evidence, curates
against profiles and is **never subordinated** to axis-level clinical evidence
(re-affirming `co1-operational.md`; consistent with DR-2026-07-20 weighted-strength
bands). Where profile guidance and axis-derived guidance conflict, the conflict is
**displayed at parity** per the existing convention — this taxonomy adds no precedence
rule and repudiates the one floated (and retracted) in-session.

**Profile kinds:** `diagnostic` (ICD-11-anchored where verifiable), `identity-cultural`
(deliberately **no** ICD anchor — Deaf culture and identity-model neurodivergence are
not disorders-of-record here), `demographic`, `anthropometric`, `compound`, `umbrella`.

## §4 Disposition of every existing population code

No rows change until ratification. `ALL` is re-classed as a link-scope **qualifier**
(it is not a population). Codes are retained for continuity; layer membership is what
changes.

| Code | Disposition | Maps to | Rationale / fixes |
|---|---|---|---|
| MOB | AXIS-ALIAS | `AX-AMB` + `AX-WHM` | Fuses ambulant and wheeled users whose parameters differ (stairs vs turning circles); 31 item links to be re-derived per mechanism at harvest |
| UPL | AXIS-ALIAS | `AX-REA` | Direct |
| VIS | AXIS-ALIAS | `AX-VIS-L` + `AX-VIS-N` | Low-vision and blindness have partially *inverse* responses (contrast maximisation vs tactile substitution); FDA already splits them informally |
| DEAF | **Dual** | axis-alias `AX-AUD` **+ Deaf-cultural profile** (identity-cultural, no ICD) | Hearing function is an axis; DeafSpace spatial practice (incl. d340 sign production) is emergent profile content. The one deliberately non-mechanical disposition — flagged for owner attention |
| SENS | AXIS-ALIAS | `AX-SPR` | Was an axis mislabeled as a population; explains its 1-item-link starvation |
| PAIN | AXIS-ALIAS | `AX-PAI` | Slug layer already merged pain+fatigue; axes stay distinct (nociception ≠ endurance), both feed `pain-ofs-built-environment-design` |
| OFS | AXIS-ALIAS | `AX-STA` (+`AX-THR` secondary) | Named umbrella retained as alias for slug continuity |
| DEM | PROFILE (diagnostic) | `AX-COG-O` primary; `AX-ARO`, `AX-VIS-L`, `AX-AMB` secondary | Carries mature emergent corpus (dementia-friendly design); ICD-11 6D8x TO-VERIFY |
| NDV | PROFILE (umbrella, identity-cultural framing) | `AX-SPR`, `AX-ARO`, `AX-COG-O` | Umbrella retained; no ICD anchor by design |
| AUT | PROFILE (diagnostic/identity dual; parent NDV) | `AX-SPR` primary; `AX-ARO`, `AX-COM-E` secondary | **Retained as distinct profile** — ASPECTSS is autism-specific emergent content; the in-session claim that AUT≡NDV was retracted (FDA mapping coarseness, not world-fact). ICD-11 6A02 |
| ADHD | PROFILE (diagnostic; parent NDV) | `AX-SPR`, `AX-COG-O` | ICD-11 6A05 |
| MH | PROFILE (umbrella) | **`AX-ARO` primary** (its real axis, currently scoped out); `AX-SPR` secondary | Fixes proxy-only representation |
| NEU | PROFILE (umbrella: ABI, stroke, TBI…) | `AX-COG-O`, `AX-AMB`, `AX-ARO`, `AX-COM-E` | FDA's `ABI` reconciles here |
| EPI | PROFILE (diagnostic; parent NEU) | `AX-SPR` (situational: photic/flicker trigger avoidance) | Judgment call documented: seizure is not sensory-*processing*, but the design lever (stimulus control, B-04) lives on that axis; safety adjacency noted |
| MS | PROFILE (diagnostic) — **re-parented off NEU** | `AX-THR` primary (Uhthoff); `AX-STA`, `AX-AMB`, `AX-VIS-L`, `AX-CNT` | Etiological shelf → functional vector; existing `ms-thermal` slug becomes legible as THR evidence |
| SCI | PROFILE (diagnostic) — **re-parented off MOB** | `AX-WHM`, `AX-REA`, `AX-THR` (poikilothermia), `AX-CNT`, `AX-PAI` | FDA already noted "biomechanical **+ autonomic**"; the table didn't |
| POTS | PROFILE (diagnostic; was OFS sub-code) | `AX-STA`, `AX-THR`, `AX-BAL` (situational) | |
| CFS | PROFILE (diagnostic; was OFS sub-code) | `AX-STA` (PEM note: rest ≠ recovery; `fluctuating: yes`) | |
| MCAS | PROFILE (diagnostic) — **re-parented off OFS** | `AX-CHM` primary | Was parented by comorbidity, not mechanism |
| PCS | **SPLIT.** `PCS-TBI` profile (post-concussion) | `AX-BAL`, `AX-SPR` (photo/phonophobia), `AX-COG-O`, `AX-STA` | DB and FDA skill currently define PCS as two different conditions. Split resolves it: post-concussion here (ICD-10 legacy F07.2; ICD-11 mapping TO-VERIFY)… |
| — | …and `LCOV` profile (post-COVID condition), **new** | `AX-STA` (PEM), `AX-THR`, `AX-COG-O` ("fog") | …post-COVID here (ICD-11 RA02). FDA skill's PCS row reconciles to LCOV |
| DBL | PROFILE (compound) | `AX-VIS-N` × `AX-AUD` at compound weight | De-privileged as a special population, retained as first-class *profile* with emergent tactile-first corpus (K-04 vibrotactile). Any compound may become a profile when it carries authored content — DBL qualifies; this resolves "why is DBL special" |
| ALL | QUALIFIER | — | Link-scope marker, not a population; excluded from both layers |

**New profiles admitted (4):** `CHD`, `LPA`, `EXH`, `BAR` (anthropometric; weights on
`AX-REA`/`AX-WHM`/`AX-AMB` envelope parameters; emergent corpora = Supplementary Volume
Parts 1–4) · `OLD` older adults (demographic; `AX-VIS-L`+`AX-AUD`+`AX-AMB`+`AX-BAL`+
`AX-COG-O`+`AX-THR`+`AX-CNT`; age-friendly emergent corpus — readmitted per the
decomposition-test consistency correction: same emergent-corpus criterion that keeps
DEM) · `VES` vestibular disorders (diagnostic; `AX-BAL` primary, `AX-SPR` secondary;
STUB pending slug) · `LCOV` (above).
**Deferred candidates** (named, not created; queue-behind rule §8 applies): migraine
(`AX-SPR`+`AX-BAL` — vestibular migraine), aphasia/dysarthria (`AX-COM-E`), IBD/ostomy
(`AX-CNT`).

## §5 Curation rules — what gets curated, and how

1. **Selection principle (the gate).** A source is in-scope iff it bears on (a) an
   axis mechanism or threshold, (b) a profile's axis-weights or emergent guidance, or
   (c) an item parameter. Otherwise it is logged out-of-scope with reason. This is the
   selection principle the slug system currently lacks.
2. **Attachment.** Mechanism/threshold evidence (clinical, biomechanical,
   psychophysical) → **axes**. Population-specific outcomes, lived experience (Co-1),
   cultural design corpora → **profiles**. Spec values and jurisdictional floors →
   **items** (unchanged). One source may attach at multiple layers.
3. **Slug discipline.** Every slug declares `serves_axes` (≥1) at creation; existing 79
   slugs get a backfill pass (post-ratification step). Search-log entries record axis
   codes henceforth, ending the free-text population drift found in
   `evidence_population_match.target_population` (to be normalised to codes +
   elaboration text).
4. **Strength semantics unchanged.** Tier and `●◐○` banding per
   DR-2026-07-20 apply at every layer; Co-1 non-subordination per `co1-operational.md`
   applies at profile layer. This taxonomy adds attachment rules, not strength rules.
5. **Items.** `item_axis_links` (staged) carries item→axis with a mechanism note and
   strength band; initial seeding by harvest from the 87 FDA audit briefs
   (`references/audit-briefs/*_brief.md`), which already contain per-item ICF
   reasoning in prose. `item_population_links` is retained during transition and
   re-derived as item→profile (via axes ∪ direct emergent links) after harvest QA.
6. **Coverage semantics.** `axis with zero slugs` and `axis with zero item links` are
   standing queryable gap conditions (extend `db.py validate`). The six new axes start
   as exactly such visible holes — by design.

## §6 Vocabulary reconciliation (FDA skill ↔ DB ↔ this document)

| FDA skill term | Canonical resolution |
|---|---|
| `ABI` | `NEU` umbrella profile |
| `ASD` | `AUT` profile |
| `LOW-VISION` | `AX-VIS-L` axis |
| `PCS` (= post-COVID, autonomic) | `LCOV` profile |
| `PCS` (DB: post-concussion, cognitive) | `PCS-TBI` profile |
| MOB "balance" (mechanism text) | `AX-BAL` (previously unmapped: b235/b240/d415 had zero corpus presence) |

Post-ratification, `functional-deficit-auditor_SKILL.md` §1–2 is regenerated from the
axis register so the audit instrument and the canonical store can no longer drift.

## §7 Compatibility — what this document does NOT change

Item codes A–K (per DR-2026-07-21 namespace rename, entities are `ENT-##`; items keep
`E-##` etc.) · conflict handling (parity display; §3.9 strategies menu; no precedence
rule) · tier system and DR-2026-07-20 weighted-strength bands · product posture
(adjudicates, declines authority) · the `populations` table rows themselves, the FDA
skill text, and all item links — until ratification · Part 2's prose structure (a
rendering concern for Phase E, downstream of this doctrine).

## §8 Coverage holes made visible, and the queue rule

Ratification creates five STUB axes (`AX-BAL`, `AX-COG-L`, `AX-COM-E`, `AX-ARO`,
`AX-CNT`), one newly *named* PARTIAL axis (`AX-CHM`, already fed by the air-quality
slug), and two STUB profiles (`VES`, `LCOV`) — with **zero evidence obligations
attached**. Research execution against them **queues behind the
existing language/jurisdiction debt** (AR/HI/BN/SW at zero; 3,140 NOT-RUN cells) unless
the owner explicitly reorders — new taxonomy must not displace declared-debt execution
(anti-displacement discipline, `workplan/next-steps-synthesis-2026-07-14.md` §4).
Proposed slug stubs, held until then: `vestibular-balance-built-environment`,
`egress-under-failure-disability`, `toileting-proximity-urgency-design`.

## §9 Migration plan (all steps post-ratification)

1. Apply staged DDL + seeds (`working/taxonomy/staged_schema_functional_axes.sql` →
   promoted into `scripts/migrations/` with a proper timestamp at apply time).
2. Backfill `slugs.serves_axes` (79 slugs; mechanical for ~60, judgment for the rest).
3. Harvest `item_axis_links` from FDA briefs; QA pass; then re-derive
   `item_population_links`.
4. Regenerate FDA skill §1–2 from the axis register.
5. Normalise `evidence_population_match.target_population` to codes + elaboration.
6. Extend `db.py validate` with the two zero-coverage gap conditions.
7. Record gaps: close GAP-277 (IntD existence — answered by `AX-COG-L`); open gap rows
   for the six STUB axes' evidence debts.
