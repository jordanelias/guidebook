# room-acoustic-performance — Reasoning Document

**BPC slug:** `room-acoustic-performance`
**Topic directory:** `sensory-environment`
**Status:** PILOT (Phase E.1 Track 3) — first BPC under DR-2026-05-13 formal-pilot mandate; inline review at each rule-#9 walk completion
**Synthesis validity:** WORK IN PROGRESS (not yet shipped)
**Pilot session:** `session_2026-05-15a-governance-reconciliation` (pivot to pilot, continuation chat)
**Pilot scope this session:** rule-#9 walk for parameter **RT60 (reverberation time)** — steps 1, 2, 3 only (Pass 1). Steps 4-9 + reasoning-doc-citations pass come in subsequent sessions.

---

## Pilot scoping note

This reasoning doc is being authored as the **first BPC reasoning doc** under the Phase E.1 workflow per `audits/bpc-rewrite-workplan-2026-05-11.md` and the rule-#10 sub-rules 2/3 verification gate per DR-2026-05-13.

**Pilot unit:** one rule-#9 walk per parameter, all populations covered by the parent BPC. Multiple parameters in scope (RT60, NC, dB(A), STI, NRC) → multiple walks within this single reasoning doc.

**Pilot order:** RT60 first because:
1. Strongest Tier-1 evidence base (Iglehart 2020, AJA — peer-reviewed; ASA-coded as ANSI/ASA S12.60-2010/Part 1 Footnote e).
2. Cleanest multi-population structure (DEAF, NDV/AUT, DEM, NEU/PCS, OFS/PAIN, general — five disability populations + general).
3. Documented numerical contestation for NDV/AUT (Bettarello 2021 + Caniato 2024: existing standards insufficient, no quantified target — exercises adversarial-research properly).
4. Multi-population convergence point at RT60 ≤ 0.4s already documented in restored CON-0264.

**Skill chain (per skills/reasoning-doc-citations_SKILL.md "Integration with sibling skills" §):**
1. `adversarial-research` (rule #7) clears each claim across the literature → `gaps` rows with `confidence_interval`, `shift_conditions`, `named_dissenter`, `falsification_condition` populated
2. `progressive-measurement` (rule #8) probes numerical-spec boundaries → `spec_value_probes` walks completed, `items.pmp_*` populated
3. `reasoning-doc-citations` (rule #10 sub-rules 2/3) confirms each citation in this doc actually contains what the doc says it contains → `reasoning_doc_citations` rows per citation

Pilot will execute the chain in order. Skipping the upstream skills (rule #7, rule #8) is not "minimum viable pilot" — DR-2026-05-13 §1 and PI rule #10 explicitly chain them.

**Pre-flight anomaly — RESOLVED 2026-05-16:**
`REF-00561` (Bettarello 2021, *Applied Sciences*, MDPI) was previously stored with DOI `10.3403/30081120u` and publisher `BSI British Standards` — a CrossRef Jaccard=0.50 backfill that mis-matched the paper to a BSI standard. Corrected via data migration `data_20260516172800_correct_ref_00561_bettarello_2021_metadata.sql` (applied 2026-05-16 17:28 in session_2026-05-15a) to DOI `10.3390/app11093942`, publisher `MDPI`, journal `Applied Sciences` 11(9):3942. Independently re-verified 2026-05-17 against MDPI catalog, ResearchGate record, and downstream citing-paper bibliographic entries. Source is eligible for Pass 3 `reasoning_doc_citations` rows without further action. **First concrete instance of rule #10 sub-rule 2 catching a wrong-content VERIFIED record before reasoning_doc_citations row creation** — pilot evidentiary purpose served.

---

## Owner sign-offs (Phase E.1 pilot inline review per DR-2026-05-13)

This section records owner directives that govern the synthesis logic. Each item carries its directive verbatim and is referenced by step number where it applies.

### Item 1 — Worst-case point convention (RULES STEP 1 + STEP 3)

**Owner directive (2026-05-17):** "you explicitly note the discrepancies when the comparator itself differs. some by metric volume, some by room type"

**Interpretation:** No single global worst-case-point convention is imposed. Each jurisdiction's step 3 table cell is read against the worst-case point as that jurisdiction's code itself structures it (volume-based for ANSI/ASA; room-type-based for DIN 18041, BB93, UNI 11532-2). The comparator type is named explicitly in the step 3 table cell so cross-jurisdictional reads are not silently elided.

**Consequence for step 1:** the "worst-case point of code structure" row above is reframed from "smallest occupied volume" (ANSI-centric) to **"native to each jurisdiction's code structure; named per cell in step 3 table."**

**Consequence for step 3:** the existing table is extended with a "comparator type" column or annotation on each value cell so the structural difference is visible to a reader, not buried.

### Item 2 — NDV/AUT chosen-value approach (RULES STEP 6)

**Owner directive (2026-05-17):** "we explicitly note that this is conjecture rationally informed by literature"

**Interpretation:** The NDV/AUT chosen-value (aspiration ≤ 0.4 s per the Pass 2 plan) is **not** presented as a Tier-1-grounded specification. It is labeled **"conjecture rationally informed by literature"** inline at the point of the claim, not as a softening caveat appended afterward. The phrase carries the epistemic status. The reasoning doc's step 7 (rationale) explicitly names which findings inform the conjecture and which gaps prevent it from being more than conjecture.

**Consequence for step 6:** for NDV/AUT specifically, the chosen-value line reads as a labeled conjecture, e.g.:

> NDV/AUT (autism spectrum, sensory hypersensitivity): RT60 ≤ 0.4 s aspiration — **conjecture rationally informed by literature**. No Tier-1 quantified target exists for this population. Informed by Bettarello et al. 2021 (insufficient existing standards), Caniato et al. 2024 (sensory hypersensitivity to background noise increments), Black 2022 (autism + built environment review); contraindication of sound masking (A-13) and background noise ≤ 30 dB(A) aspiration are companion specifications that carry independent evidentiary support.

**Consequence for the spec layer:** any item that propagates the RT60 ≤ 0.4 s value for NDV/AUT inherits the "conjecture rationally informed by literature" label until or unless the Tier-1 evidence base develops to support a quantified target. Rule #8 PMP for this population specifically uses the conjecture as `spec_value_origin` and probes against literature support, with strict-termination expected to **fail** (no Tier-1 corroboration) — the recorded PMP outcome is the structured form of the conjecture label.

### Item 3 — Pre-pass order (CHAIN ORDER)

**Owner directive (2026-05-17, via delegation "do whatever makes most sense long-term integrity"):** Option A — rule #7 (adversarial-research) → rule #8 (PMP) → rule #10 (reasoning-doc-citations).

**Interpretation:** No integrity-relevant alternative. `progressive-measurement_SKILL.md` line 25: "PMP probes within a validated claim, so the underlying claim must clear adversarial first." `reasoning-doc-citations_SKILL.md` "Integration with sibling skills" § states the same dependency. Reversing the order would force PMP onto an unvalidated claim — a documented failure mode.

**Consequence:** Pass 2 opens with `adversarial-research` on the strongest contested claim (NDV/AUT quantified RT60 targets without Tier-1 base, per line 170), then `progressive-measurement` for DEAF RT60 ≤ 0.3 s, then rule #9 steps 4–9, then Pass 3 rule #10.

### Item 4 — Items↔BPCs schema model

**Owner directive (2026-05-17, via delegation):** Option B — add `item_bpc_links` join table; `items.bpc_source_slug` retained read-only for backward compatibility until all 91 items migrated, then deprecated.

**Rationale:** A-10b ("RT60 for Hydrotherapy and Pool Environments") already demonstrates a multi-BPC item in practice — it draws on `room-acoustic-performance` (parameter) and a hydrotherapy/pool BPC (context). The forthcoming `cross-population-conflict-resolutions` BPC will produce more such items. Denormalized 1:1 (Option A) would force an arbitrary "primary BPC" choice per multi-source item, captured only in `notes` — this replicates at the schema level the same topic-vs-claim conflation rule #10 sub-rule 2 exists to prevent at the citation level. One-time migration cost (new table, new validator) is preferable to permanent per-item schema-reality drift.

**Consequence:** `scripts/migrations/NNN_add_item_bpc_links.sql` authors the join table — columns `(item_code, slug, link_type, created_at, created_by_session)` with `link_type ∈ {primary, parameter, context, secondary}` and FK to both `items(item_code)` and `slugs(slug)`. CI structure check extended to verify every ACTIVE item has ≥1 link with `link_type='primary'`. Migration is the first sub-task of the next session, before Pass 2.

### Item 5 — Item creation policy for population-specific specs

**Owner directive (2026-05-17, via delegation):** Option A — single item per parameter-context, with population-specific values captured in `item_population_elaborations`. `item_population_links` records which populations a given item applies to; `item_population_elaborations` (schema fields `spec_variant_a`, `spec_variant_b`) records the population-specific spec variants.

**Rationale:** The schema already answers this question. `item_population_elaborations` was designed for "one item, multiple population-keyed spec values" (e.g., RT60 ≤ 0.3 s for DEAF / ≤ 0.5 s for DEM / ≤ 0.6 s for general). Forking items per population (Option B) breaks normalization and explodes item count at the 95 BPCs × ~5 parameters × ~4 populations rewrite scale. Option C (context-keyed items, e.g., RT60-classroom vs RT60-hydrotherapy) remains operative for context differentiation but does not solve population differentiation; the two compose — context-keyed items carrying population variants via elaborations.

**Consequence for the spec layer:** An acoustic parent item (existing A-NN family) holds the canonical parameter. Population-specific values are rows in `item_population_elaborations` keyed to that item — `spec_variant_a` carries the chosen value, `spec_variant_b` an alternate if a population's evidence supports a range. The NDV/AUT "conjecture rationally informed by literature" label (Item 2) propagates via the elaboration row's `notes` field, with the PMP outcome attached per Item 2's strict-termination-expected-to-FAIL contract.

### REF-00561 (Bettarello 2021) metadata correction — RESOLVED (no routing needed)

**Status (2026-05-17, post-bottom-up verification):** Already corrected. Data migration `data_20260516172800_correct_ref_00561_bettarello_2021_metadata.sql` was applied 2026-05-16 17:28 in session_2026-05-15a, ahead of this resumption session — the pre-flight note above was stale relative to repo state. Independent web verification 2026-05-17 confirms DOI `10.3390/app11093942` resolves to MDPI *Applied Sciences* 11(9):3942 with the correct authors. Source eligible for Pass 3 `reasoning_doc_citations` rows without further action.

---

**Pilot gate status (post-2026-05-18 PMP walk):** All five sign-off items closed. REF-00561 confirmed corrected. Schema migration 013 applied. A-18 authored under standing rule #3 Change Order with 4 population elaborations (closes GAP-282). GAP-291 closed-resolved on NDV/AUT RT60 target-absence claim (rule #7 pass). PMP-A18-001 walk passed strict termination at 0.30 s with REF-00325 (Iglehart 2020) Tier-1 anchor (rule #8 pass). Pass 2 sub-tasks 1 and 2 complete; sub-task 3 (rule #9 steps 4-9 authoring) is next. Pass 3 (rule #10 reasoning-doc-citations) follows once Pass 2 completes.

---



### Step 1 — Parameter declaration

| Field | Value |
|---|---|
| Parameter | RT60 (reverberation time at -60 dB decay) |
| Units | seconds (s) |
| Accessibility direction | LOWER is more inclusive (less reverberation = better speech intelligibility for hearing-impaired, lower sensory load for NDV/AUT, less agitation trigger for DEM) |
| Measurement point convention | Mid-frequency average over 500/1000/2000 Hz octave bands per ISO 3382-2; values reported at occupied room state where specified, otherwise unoccupied |
| Worst-case point of code structure | **Native to each jurisdiction's code structure; named per cell in step 3 table.** Comparator type varies — volume-based (ANSI/ASA: ≤ 283 m³ classroom); room-type-based (BB93, DIN 18041:2016, UNI 11532-2:2020 room-class A1-A4); formula-based (DIN 18041 uses a volume-dependent target curve); hybrid (some jurisdictions specify both). The rule #9 step 3 table makes the comparator explicit per cell rather than imposing a single global frame. Per owner sign-off Item 1 (2026-05-17). |

### Step 2 — Per-population worst-case user

Per rule #9: "Per-population worst-case user (no inline cross-population arbitration)." Cross-population arbitration is step 9 (conflict flag); steps 2-8 stay per-population.

| Population | Worst-case user statement | Source basis (Phase B-eligible) |
|---|---|---|
| **DEAF (hearing aid / cochlear implant users, children)** | Pediatric hearing-aid or CI user, school-age, in classroom listening at distance > 1.5 m from speaker, background noise present, competing-talker conditions. Speech-perception threshold materially degrades above RT60 ≈ 0.3 s; effect is non-linear, sharpest in the 0.3-0.6 s band where typical-hearing peers remain functional. | Iglehart 2020 (REF-00325, T1); Iglehart 2016 (REF-00578, T1); Neuman 2010 (REF-00577, T1); Wroblewski 2012 (REF-00576, T1) |
| **NDV/AUT (autism spectrum, sensory hypersensitivity)** | Autistic individual in occupied space with sudden noise events + reverberant acoustic environment. Threshold of distress varies across the population. **No Tier-1 quantified RT60 threshold exists** — independently corroborated by Marzi 2025 (REF-00727, Sci Rep): *"In the absence of specific quantitative data on sound levels tailored to autistic users, a study on neurotypical students was referenced."* Bettarello 2021 (REF-00561, Tier 3) DOES propose an aspirational range of **0.4–0.7 s** from a single Italian daily-care facility (n=7 rooms) — a quantified design recommendation, not a Tier-1 threshold. Adversarial-research pass closed under GAP-291 (2026-05-17); confidence 85–95%. | Bettarello 2021 (REF-00561, T3); Marzi 2024 (REF-00726, T1 review); Marzi 2025 (REF-00727, T1 primary); Black 2022 (REF-00589, T3) |
| **DEM (dementia)** | Person living with dementia in long-term care common areas during peak occupancy. Acoustic environment is a confirmed contributor to agitation-event frequency; therapeutic target is acoustic calm. RT60 reduction documented as part of intervention bundles; no isolated RT60 dose-response curve in the literature reviewed. | Devos 2019 (REF-00571, T3); BrainXchange Canada (Tier 2 Co-1, ref not yet linked); Lyngby-Taarbæk POE (Tier 2 case study, ref not yet linked) |
| **NEU/PCS (post-concussion syndrome, photo/phonosensitivity)** | Person in post-concussion recovery with phonosensitivity. RT60-specific evidence not located in the populations covered by Phase B; PCS population is absent from acoustic standards in any jurisdiction reviewed. | NO direct evidence in eligible-source pool; claim downgraded to "no quantified target available" at step 6 |
| **OFS/PAIN (orthostatic / pain populations)** | No room-acoustic mechanism identified that this population requires differently from general. | THIN-BASE per BPC; no claim made |
| **general (typical-hearing adult or child)** | Occupant in general-use indoor space. Speech intelligibility intact up to RT60 ≈ 0.6 s in volumes ≤ 283 m³ per established acoustic engineering literature. | ANSI/ASA S12.60-2010 (Tier 6, statutory); BB93 (UK); DIN 18041:2016; UNI 11532-2:2020; AS/NZS 2107; multiple jurisdictions concur. |

**Cross-population arbitration deferred to step 9.** No inline statement that any one population's target supersedes another at this step.

### Step 3 — Jurisdiction comparison table

Per rule #9 step 3: "every surveyed jurisdiction's value at worst-case point; `scope` column."

Per owner sign-off Item 1: comparator type named per row so structural differences across codes are explicit, not elided.

| Jurisdiction | Standard / Code | Comparator type | Worst-case-point (general) | Worst-case-point (DEAF / HI) | Worst-case-point (NDV/AUT) | Scope |
|---|---|---|---|---|---|---|
| **US** | ANSI/ASA S12.60-2010/Part 1 | volume-based (≤ 283 m³ / 283-566 m³) | RT60 ≤ 0.6 s (≤ 283 m³); ≤ 0.7 s (> 283 m³ to 566 m³) | RT60 ≤ 0.3 s (≤ 283 m³) per Footnote e (HA/CI users) | not addressed | classrooms / learning spaces; statutory in many states |
| **UK** | BB93 (Building Bulletin 93, 2015) | room-type-based (by space function) | RT60 ≤ 0.4-0.8 s by room type | RT60 ≤ 0.4 s in "specially resourced provision" for hearing-impaired | not addressed | new build schools; statutory under Education (School Premises) Regulations |
| **UK (transversal)** | PAS 6463:2022 | qualitative; no numeric comparator | qualitative ("acoustic calm in sensory-sensitive spaces") | references BB93 | qualitative guidance, no quantified RT60 | publicly accessible buildings; not statutory |
| **DE** | DIN 18041:2016 | formula-based (volume-dependent target curve) by room type | target curve typically 0.4-0.8 s | annex addresses "Hörsamkeit bei Behinderung" qualitatively | not quantified | acoustic quality in small-to-medium rooms; widely referenced in DE design |
| **IT** | UNI 11532-2:2020 | room-class-based (categories A1-A4) | RT60 by room class A1-A4; A4 (high-criticality educational) ≈ 0.5 s | category A3.1 / A4 explicitly addresses students with hearing deficit; lower RT targets | not quantified specifically; category A4 considers cognitive accessibility qualitatively | classrooms; mandatory citation in IT acoustic design |
| **FR** | NF S 31-080 (2006) | room-category-based | RT60 ≤ 0.4-0.8 s by room category | not differentiated | not addressed | classrooms / offices |
| **AU/NZ** | AS/NZS 2107:2016 | space-type-based table | RT60 by space type (table); typical classroom 0.4-0.6 s | references but does not quantify HI-specific | not addressed | recommended levels for indoor spaces |
| **JP** | JIS Z 8731 framework + Barrier-Free Law | measurement-method; no quantified-target comparator in acoustic standard | general RT guidance; no disability-specific differentiation in the acoustic standard itself | Barrier-Free Law addresses physical access; acoustic provisions not quantified per population | not addressed | acoustic measurement; barrier-free is separate regulation |
| **CN** | GB 50118-2010 | volume-based (classroom) | RT60 ≤ 0.7-0.9 s (classroom, by volume) | not differentiated | not addressed | civil-building acoustic design |
| **DK / NO / SE / FI** | National building codes referencing ISO 3382 / NS-EN 16798 | room-type-based (classroom focus) | typical 0.4-0.6 s (classrooms) | thin coverage; some references to assistive-listening infrastructure | not addressed | school acoustics |
| **NL** | NEN 3088 | room-type-based | RT60 ≤ 0.5-0.8 s | not differentiated | not addressed | school acoustics |
| **BE** | NBN S 01-400-2 | room-type-based | RT60 ≤ 0.8 s typical classroom | not differentiated | not addressed | acoustic performance |
| **ES** | DB-HR (CTE) | room-type-based | RT60 ≤ 0.7 s typical classroom | not differentiated | not addressed | sound protection (technical building code) |
| **PT** | Portuguese national requirements (RGR / school acoustic guidance) | coverage thin in BPC | not separately codified per the BPC's coverage | not differentiated | not addressed | partial coverage in BPC |
| **KR** | KS F 2814 + barrier-free law framework | coverage thin in BPC | not separately codified per the BPC's coverage | not differentiated | not addressed | partial coverage in BPC |
| **NL/KO/SV-FI thin** | per BPC header | acknowledged thin coverage | acknowledged thin coverage | acknowledged thin coverage | acknowledged thin coverage | gap documented |

**Structural observation surfaced by the comparator-type column:** the surveyed jurisdictions divide into four families — volume-based (US, CN), room-type-based (UK BB93, FR, AU/NZ, NL, BE, ES, Nordic), formula-based with room-type input (DE DIN 18041), room-class-based (IT UNI 11532-2). Cross-jurisdictional reads at the same nominal point ("classroom RT60 target") are not directly comparable without first noting which family the source jurisdiction belongs to. This is the heart of why rule #9 step 3 cannot collapse into a single ranked column — different jurisdictions answer different questions.

**Citation-grade verification of this table is PENDING.** Every cell that asserts a specific value for a specific jurisdiction at the worst-case point becomes a `reasoning_doc_citations` row in the rule-#10 pass. None of those rows exist yet; this Pass-1 table is the structure that the Pass-3 pass will verify against the cited sources.

**Note on `[UNVERIFIED-TERMS]` per rule #9.** The 5 flagged languages (AR, HI, ID, SW, BN) do not appear in this parameter's surveyed jurisdiction set — RT60 codes in those languages were not part of the original multilingual coverage. This is a gap in coverage rather than an unverified-keyword issue; logged here for Phase A.11 cross-reference but not blocking this walk.

---

## Pass 2 — Rule #9 steps 4 through 9

### Step 4 — Lowest-barrier code per population

Per the project's `<terminology>` definition: the jurisdiction-level regulatory standard imposing the lowest barrier to access for the most-constrained user, evaluated at the worst-case point in the code's structure. Per Item 1 sign-off, "worst-case point" is read against each jurisdiction's native comparator type (volume-based, room-type-based, formula-based, room-class-based), not a single global frame.

- **DEAF.** ANSI/ASA S12.60-2010/Part 1 Footnote e + Commentary 5.3.1 (US) — RT60 ≤ 0.3 s in core learning spaces ≤ 283 m³ for children with hearing impairment. Lowest barrier in the surveyed set evaluated at the US volume-based worst-case point. BB93 (UK) "specially resourced provision" at ≤ 0.4 s is the next-lowest in the room-type-based family.
- **NDV/AUT.** No jurisdiction codifies a quantified RT60 for autistic occupants. PAS 6463:2022 (UK) is the only standards-body publication explicitly addressing neurodivergent occupant acoustic needs and stays qualitative. Marzi 2025 (REF-00727) documents the absence on the literature side as well. Functionally, the lowest barrier reached by any code for this population is the room's general-occupant target.
- **DEM.** No jurisdiction codifies an RT60 specific to dementia care environments. WELL Building Standard addresses reverberation generally (≤ 0.6 s for ≤ 280 m³) but not population-specifically. The lowest barrier in practice comes from healthcare design guidance (FGI in US, HBN in UK) referencing general acoustic standards without dementia-specific quantification.
- **general.** ANSI/ASA S12.60-2010/Part 1 main rule (RT60 ≤ 0.6 s, ≤ 283 m³) is the lowest barrier at the smallest-volume worst-case point in the volume-based family. In room-type-based jurisdictions (BB93, DIN 18041, UNI 11532-2, AS/NZS 2107), the lowest-barrier room class at the same epistemic register is the comparator. Cross-family comparison requires the comparator-type translation per step 3.

### Step 5 — Tier evidence per population

Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 enumeration per rule #9. Tier 4 (international advisory) and Tier 5 (national-recommended) excluded at this step.

- **DEAF.**
  - Tier 1: Iglehart 2020 (REF-00325, primary validation of 0.3 s with hearing-aid users, N=10); Iglehart 2016 (REF-00578); Neuman 2010 (REF-00577); Wroblewski 2012 (REF-00576).
  - Co-1: Iglehart's role on the ASA S12 working group anchors the ANSI/ASA S12.60 footnote — primary research and standards-setting overlap.
  - Tier 2: none additional surfaced in BPC inventory.
  - Co-2: none.
  - Tier 3: clinical-audiology guidance from professional bodies (ASHA classroom-acoustics portal; AAA pediatric guidance) — corroborative, not primary.
- **NDV/AUT.**
  - Tier 1: Marzi 2024 (REF-00726, B&E comprehensive review of neurodivergent indoor comfort); Marzi 2025 (REF-00727, Sci Rep primary documenting threshold-absence and attentional decrement at 55 dB(A) background).
  - Co-1: Bozen-Bolzano + Stuttgart research group carries multi-paper continuity from 2021 Bettarello onward — same investigators appearing in both Tier-1 and Tier-3 sources.
  - Tier 2: none in BPC inventory.
  - Co-2: none.
  - Tier 3: Bettarello 2021 (REF-00561, n=7 rooms, proposes 0.4-0.7 s aspirational range); Black 2022 (REF-00589, autism + built environment review); Caniato 2022 (Energy Reports Parts 1+2).
- **DEM.**
  - Tier 1: none — no peer-reviewed primary with isolated RT60 dose-response for this population.
  - Co-1: none.
  - Tier 2: Lyngby-Taarbæk POE (DK case study, RT60 reduction within multi-component intervention).
  - Co-2: BrainXchange Canada (Tier 2 Co-1, knowledge-translation network).
  - Tier 3: Devos 2019 (REF-00571, review).
- **general.**
  - Tier 1: speech-perception primary literature (Bradley & Sato 1990s-2000s; underlying STI development).
  - Co-1: standards-setting working groups (ASA S12 in US, BB93 in UK, DIN 18041 in DE) include primary researchers.
  - Tier 2: jurisdiction-level technical reports.
  - Co-2: none distinct from Co-1.
  - Tier 3: practitioner literature (ASHA, ASA educational materials).

### Step 6 — Guidebook chosen value per population

Per Item 2 sign-off: NDV/AUT line carries the "conjecture rationally informed by literature" label inline.

- **DEAF: RT60 ≤ 0.3 s** in occupied learning and listening spaces ≤ 283 m³. Empirically validated by PMP walk PMP-A18-001 (2026-05-18); strict termination PASSED at V₀ = 0.3 s with Iglehart 2020 (REF-00325) anchor; gap_signed = 0.00. Co-supported by ANSI/ASA S12.60-2010/Part 1 (REF-00335, pending citation-miner pass for rule-#10 eligibility).
- **NDV/AUT: RT60 ≤ 0.4 s aspiration** — **conjecture rationally informed by literature**. No Tier-1 quantified threshold exists (GAP-291 closed-resolved 2026-05-17 at 85-95% confidence; Marzi 2025 corroborates absence). Bettarello 2021 (Tier 3) proposes 0.4-0.7 s from one Italian facility (n=7 rooms); the pilot's chosen value sits at the lower bound of that recommendation. Companion specifications (no sound masking per A-13; background noise ≤ 30 dB(A) aspiration) carry independent evidentiary support. Future PMP walk for this population will exercise the conjecture against strict termination; failure is the expected and structurally correct outcome — the recorded PMP outcome is the structured form of the conjecture label.
- **DEM: RT60 ≤ 0.5 s** in occupied common areas. Matches the BPC's existing language. Evidence base Tier 2-3.
- **general: RT60 ≤ 0.6 s** in occupied general-use indoor space ≤ 283 m³. Matches cross-jurisdictional convergence.

### Step 7 — Rationale per population

Historical context + clinical basis per rule #9.

**DEAF.** The US ANSI/ASA S12.60 standard originated in a 1998 US Access Board + Acoustical Society of America working group convened to address chronic underperformance of school acoustic environments for children at risk — including children with hearing loss, temporary hearing impairment from otitis media, learning disabilities, and non-native speakers of English. The 2002 first edition set 35 dB(A) background and 0.6 s reverberation for typical classrooms ≤ 283 m³ but did not differentiate by occupant hearing status. The 2010 revision retained 0.6 s general and added §5.3 Footnote e + Annex Commentary 5.3.1 specifying RT60 ≤ 0.3 s for children with hearing impairment in the same volume — based at the time on preliminary conference proceedings (Iglehart 2007, 2008a, 2008b) rather than peer-reviewed publication. Iglehart 2020 (REF-00325) is the first peer-reviewed validation: children with hearing loss using hearing aids tested across four RT conditions showed speech perception in 0.3-s RT measurably below sound-booth baseline but acceptable, with significant degradation at longer RTs. The clinical basis is mechanistic: hearing aids and cochlear implants amplify reverberant energy along with direct speech signal, so any given RT60 has greater perceptual impact for HA/CI users than for typical-hearing peers; reduced auditory cortical adaptation in HA/CI users compounds this; and the binaural cues typical-hearing listeners use to separate direct speech from reflections are degraded in HA/CI processing. 0.3 s is therefore not a comfort threshold but a speech-access threshold — below the RT at which hearing-aid amplification stops being a net benefit. Adoption into the 2016 IBC reference brought the value into US building code where state and local jurisdictions ratify.

**NDV/AUT.** No regulatory tradition addresses autism-specific acoustic requirements. PAS 6463:2022 (UK) is the first major standards-body publication to acknowledge neurodivergent occupant acoustic needs and remains qualitative. The empirical lineage is recent: Caldas/Masiero/Wang surveyed teachers of children with ASD and identified air conditioning noise and reverberant echoes as the dominant in-classroom acoustic stressors; Zaniboni et al. 2021 surveyed parents/caregivers and found 48% of autistic individuals report reverberation as actively problematic. Bettarello et al. 2021 (REF-00561) produced the first quantified design recommendation — 0.4-0.7 s — from acoustic optimization of one Italian daily-care facility (n=7 rooms). Caniato et al. 2022 (Energy Reports Parts 1+2) and Marzi/Caniato/Gasparella 2024 (REF-00726, B&E review) extended the line. Marzi 2025 (REF-00727, Sci Rep) tested autistic and typically-developed individuals across six environmental scenarios and documented attentional decrement for autistic participants at 55 dB(A) background where TD participants showed none; the paper opens its acoustic methods by stating that no specific quantitative thresholds tailored to autistic users exist. The clinical basis is sensory hypersensitivity: reverberation increases ambiguity in source identification (Bettarello's framing — autistic listeners report greater confusion between sound and noise than typical), and sudden noise events are disproportionately distressing. The pilot's ≤ 0.4 s aspiration sits at the lower bound of Bettarello's range — choosing the most conservative end of the only quantified Tier-3 recommendation available, while explicitly carrying the conjecture label until a future Tier-1 publication tests the value directly.

**DEM.** Acoustic environment in long-term dementia care surfaced as an agitation modifier in nursing-home research in the 1990s-2000s without producing isolated RT60 dose-response data. Intervention studies that include acoustic modification typically bundle RT60 reduction with other environmental changes (lighting, color, wayfinding cues), so the contribution of RT60 alone is not separable in current literature. Devos 2019 (REF-00571) characterizes the position. BrainXchange Canada and the Lyngby-Taarbæk POE document RT60 reduction within real-world intervention bundles. The clinical basis is reduced cognitive bandwidth for noise filtering: dementia is associated with disproportionate distress from acoustic complexity, and the therapeutic target is acoustic calm rather than speech intelligibility per se. The BPC's ≤ 0.5 s is therefore not anchored in an isolated dose-response study but in the convergent pattern of intervention bundles that include RT60 reduction at roughly this magnitude alongside other modifications. **Honest characterization: this is the thinnest evidence base of the four populations addressed by this BPC; the ≤ 0.5 s value should be read as defensible-but-not-empirically-validated, pending Tier-1 publication of an isolated dose-response.**

**general.** The 0.6 s typical-classroom value descends from a long lineage of speech-intelligibility research — Sabine's foundational absorption work (early 1900s), the Speech Transmission Index framework developed by Houtgast & Steeneken (1970s onward), Bradley & Sato's classroom-acoustics studies (1990s-2000s) — converging on the band 0.4-0.8 s as the range within which typical-hearing listeners maintain effective speech understanding at conversational distance under controlled background noise. ANSI/ASA S12.60-2002 codified 0.6 s for ≤ 283 m³ as the central value, retained in the 2010 revision. The cross-jurisdictional convergence visible in step 3 (UK BB93, DE DIN 18041, IT UNI 11532-2, AU/NZ AS/NZS 2107, NL/BE/ES national codes, FR NF S 31-080) is independent rather than copy-derived — different working groups landed in the same band from different epistemic frames. The clinical basis is the same speech-perception physics that underlies the DEAF rationale, with wider tolerance because typical-hearing listeners can use binaural cues, contextual prediction, and active gain control that HA/CI users cannot.

### Step 8 — Trade-offs

- **NRC vs STI.** Broadband absorption ≥ 0.85 NRC (item A-02) can degrade Speech Transmission Index by reducing not only reverberant noise but also useful early reflections that aid speech intelligibility — documented in Amlani & Russo 2016 (REF-00580). GAP-RAP-01's evidence-auditor adjudication treats this as a co-design constraint: absorption placement (rear and side walls, ceiling tiles preferentially over upper third) matters as much as bulk absorption magnitude. The pilot does not resolve to a single rule; the trade-off is named so downstream design guidance can address it.
- **DEAF target vs general target in shared-occupancy buildings.** The DEAF ≤ 0.3 s requires roughly twice the absorption of the general ≤ 0.6 s target in the same volume. In buildings serving both populations (mainstream schools with HA/CI students, mixed-occupancy classrooms), the design implication is universal application of the DEAF target rather than per-room differentiation — simpler in practice and avoids stigmatizing designated "hearing-impaired classrooms." Cost trade-off lives elsewhere in the BPC.
- **NDV/AUT aspiration vs current jurisdictional codes.** The ≤ 0.4 s aspiration sits below every surveyed jurisdiction's general target (≤ 0.5 s in IT UNI A4 category is the closest). In jurisdictions where building codes set ≤ 0.6 s or higher as the regulatory floor, designing to ≤ 0.4 s for NDV/AUT-occupied spaces is supererogatory — exceeds code — with no enforcement against under-compliance to the aspiration. The trade-off is between aspiration and what a designer can defend to a client at code-compliance budget.
- **Absorption strategy vs visual / wayfinding / contamination considerations.** Carpet and soft furnishings are dominant RT60-reduction strategies but trade against VIS-navigability (carpet pattern can disorient vision-impaired users) and air-quality / infection control (carpets retain particulates and allergens). Item A-05 names this trade-off; resolution is context-dependent.

### Step 9 — Cross-population conflict flag

**No conflict for RT60 across the four populations addressed.** All population-specific values (DEAF ≤ 0.3 s, NDV/AUT ≤ 0.4 s aspiration, DEM ≤ 0.5 s, general ≤ 0.6 s) point in the same direction — lower RT60 is more accessible — and the most-constrained value (DEAF ≤ 0.3 s) is implementable in any space that meets the general code. The relationship is structurally **convergent**, not in tension: a building designed to the DEAF target automatically satisfies all three others. This is the matched-direction case noted in the restored CON-0264 connection record. Cross-population arbitration is therefore moot for this parameter; no arbitration-BPC routing required. The pilot's first cross-jurisdictional synthesis under rule #9 produces a clean convergent result — useful as a baseline before subsequent BPCs surface the conflicted cases (e.g., MS thermal needs vs DEM thermal needs, where direction itself diverges).

---

## Session log

### Pass 3 plan (subsequent session)

Run `reasoning-doc-citations` on every cell of step 3's jurisdiction table that asserts a value + every claim in steps 6-7 attributed to a specific source. Estimate: ~40-60 rows. Each row requires opening the cited source at the cited section and confirming `value_match` or `claim_match`.

Pre-flight: REF-00561 metadata correction status — RESOLVED 2026-05-16. REF-00335 (ANSI/ASA S12.60-2010) requires `citation-miner` pass before any reasoning-doc-citations row referencing US standard claims can land; surfaced by this session's PMP walk.

### Rule #7 adversarial-research pass — COMPLETED 2026-05-17

Adversarial-research on the contested claim **"NDV/AUT require quantified RT60 targets but no Tier-1 evidence base exists for what those targets should be"** closed under **GAP-291** (CLOSED-RESOLVED) with all four protocol fields populated:
- `confidence_interval`: 85-95%
- `named_dissenter`: NONE FOUND for the Tier-1-threshold-absence claim. Partial sharpening from Bettarello 2021 (Tier-3 design recommendation 0.4-0.7 s exists, just not at Tier 1).
- `shift_conditions`: drops to 50-65% on non-English Tier-1 threshold publication; rises to 95%+ on 2026 affirmation; etc.
- `falsification_condition`: peer-reviewed primary study N>20 autistic occupants with RT60 dose-response, OR new ISO/ANSI/PAS standard with quantified NDV/AUT RT60 target, OR systematic review identifying ≥3 such missed studies.

Four `evidence_population_match` rows logged (EPM-RAP-001..004). Per migration `data_20260517235900_adversarial_research_ndv_aut_rt60_target_absence.sql`.

### Rule #8 PMP pass — COMPLETED 2026-05-18

PMP walk **PMP-A18-001** for A-18 DEAF RT60 maximum 0.3 s. Setup: V₀ = 0.3 s, U = s, D = down, claim_type = maximum, δ_min = 0.05 s. Three probe rows:

| step | phase | V_test | passes_strict | anchor |
|---|---|---|---|---|
| 1 | outer-stop | 0.24 s | 0 | (no source; 0.24 s appears only as Iglehart 2020 calibration signal, topic-not-claim) |
| 2 | refinement-stop | 0.27 s | 0 | (no source; nearest published values 0.3 s / 0.45 s DGUV) |
| 3 | **final** | **0.30 s** | **1** | **REF-00325 Iglehart 2020 (Tier 1, COMPLETE/VERIFIED)** |

**V_empirical_ceiling = 0.30 s** (matches V₀). **gap_signed = 0.00**. Strict termination PASSED. Co-supporting source REF-00335 (ANSI/ASA S12.60-2010) is AUTHOR-TITLE-ONLY and rule-#10-ineligible; logged for citation-miner pickup. Per migration `data_20260518010000_pmp_walk_a18_deaf_rt60.sql`.

### Rule #9 steps 4-9 authoring — COMPLETED 2026-05-18

Steps 4-9 authored from primitives this session (Pass 2 sub-task 3). Step 7 historical/clinical rationale paragraphs grounded in source reads — ANSI S12.60 lineage (1998 Access Board working group, 2002 first edition, 2010 revision adding 0.3 s for HI), Bettarello/Marzi/Caniato research line for NDV/AUT, Devos 2019 + intervention-bundle pattern for DEM, Sabine/STI/Bradley-Sato lineage for general. DEM rationale explicitly characterizes thin-evidence base honestly. Step 8 expanded to four trade-offs (NRC↔STI, DEAF-vs-general in shared-occupancy, NDV/AUT aspiration vs code floor, absorption-vs-visual/contamination). Step 9 verdict: convergent no-conflict case.

Pass 2 complete. Pass 3 (rule #10 reasoning-doc-citations) is the next session.

---

## Outstanding flags from this pilot session

1. **REF-00335 (ANSI/ASA S12.60-2010) is AUTHOR-TITLE-ONLY** — surfaced by PMP walk PMP-A18-001 as the binding gap. Co-supports DEAF 0.3 s independently of Iglehart 2020; rule-#10-ineligible until `citation-miner` brings it to COMPLETE/VERIFIED. Blocks step-3 jurisdiction-comparison rows for US/ANSI in Pass 3.
2. PCS population has no acoustic evidence in the eligible-source pool; chosen-value will be "no quantified target available" at step 6 rather than a fabricated number. Confirms rule #10 sub-rule 2 working as intended.
3. KO, NL, SV, FI thin-jurisdiction coverage per BPC header is real and acknowledged; rule #9 step 3 table marks them. Multilingual extension is a Phase A.11 sequel, not in scope.
4. DEM rationale evidence base is the thinnest of four populations — no isolated RT60 dose-response published. Step 7 names this explicitly; ≤ 0.5 s value is defensible-but-not-empirically-validated.

---

## Metadata

```yaml
reasoning_doc_slug: room-acoustic-performance
parent_bpc: references/bpc/sensory-environment/room-acoustic-performance.md
pilot_designation: TRACK-3-PILOT-1
pilot_pass_completed: PASS-2
pilot_pass_pending: PASS-3 (rule #10 reasoning-doc-citations)
parameters_in_scope:
  - RT60  # this walk
  - NC    # subsequent walks
  - dB(A)
  - STI
  - NRC
review_required_at:
  - end_of_PASS-1   # ← now
  - end_of_adversarial-research  # rule #7
  - end_of_PMP-DEAF-RT60         # rule #8
  - end_of_PASS-2                # rule #9 steps 4-9
  - end_of_PASS-3                # rule #10 citation verification
synthesis_validity: WORK-IN-PROGRESS  # not yet shippable
created: 2026-05-16
created_by_session: session_2026-05-15a-governance-reconciliation-and-pilot
```
