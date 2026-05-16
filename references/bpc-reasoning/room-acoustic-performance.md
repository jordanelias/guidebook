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

**Pre-flight anomaly flagged for triage (does not block pilot):**
`REF-00561` (Bettarello 2021, *Applied Sciences*, MDPI) has `metadata_quality=COMPLETE verification_status=VERIFIED` but the DOI `10.3403/30081120u` and publisher `BSI British Standards` are clearly wrong for this paper — that DOI prefix belongs to British Standards Institution. The `VERIFIED` tag confirmed a target resolved, but rule #10 sub-rule 2 (claim-content matching) catches the inconsistency. The actual Bettarello et al. 2021 paper is in MDPI *Applied Sciences*. Logged here; route to `citation-miner` next-session to correct metadata before this source is used to ground any reasoning-doc-citations row.

---

## Rule-#9 walk: RT60 (reverberation time)

### Step 1 — Parameter declaration

| Field | Value |
|---|---|
| Parameter | RT60 (reverberation time at -60 dB decay) |
| Units | seconds (s) |
| Accessibility direction | LOWER is more inclusive (less reverberation = better speech intelligibility for hearing-impaired, lower sensory load for NDV/AUT, less agitation trigger for DEM) |
| Measurement point convention | Mid-frequency average over 500/1000/2000 Hz octave bands per ISO 3382-2; values reported at occupied room state where specified, otherwise unoccupied |
| Worst-case point of code structure | Smallest occupied volume where the parameter is regulated (typically classroom ≤ 283 m³; some codes structure by room type rather than volume — recorded per-jurisdiction in step 3) |

### Step 2 — Per-population worst-case user

Per rule #9: "Per-population worst-case user (no inline cross-population arbitration)." Cross-population arbitration is step 9 (conflict flag); steps 2-8 stay per-population.

| Population | Worst-case user statement | Source basis (Phase B-eligible) |
|---|---|---|
| **DEAF (hearing aid / cochlear implant users, children)** | Pediatric hearing-aid or CI user, school-age, in classroom listening at distance > 1.5 m from speaker, background noise present, competing-talker conditions. Speech-perception threshold materially degrades above RT60 ≈ 0.3 s; effect is non-linear, sharpest in the 0.3-0.6 s band where typical-hearing peers remain functional. | Iglehart 2020 (REF-00325, T1); Iglehart 2016 (REF-00578, T1); Neuman 2010 (REF-00577, T1); Wroblewski 2012 (REF-00576, T1) |
| **NDV/AUT (autism spectrum, sensory hypersensitivity)** | Autistic individual in occupied space with sudden noise events + reverberant acoustic environment. Threshold of distress varies across the population; no quantified RT60 ceiling has been established that the literature treats as evidence-based for this population. Existing standards explicitly inadequate per the BPC's Opus synthesis. | Bettarello 2021 (REF-00561, T3 — metadata flagged); Caniato 2024 (cited in BPC, ref not yet linked); Black 2022 (REF-00589, T3) |
| **DEM (dementia)** | Person living with dementia in long-term care common areas during peak occupancy. Acoustic environment is a confirmed contributor to agitation-event frequency; therapeutic target is acoustic calm. RT60 reduction documented as part of intervention bundles; no isolated RT60 dose-response curve in the literature reviewed. | Devos 2019 (REF-00571, T3); BrainXchange Canada (Tier 2 Co-1, ref not yet linked); Lyngby-Taarbæk POE (Tier 2 case study, ref not yet linked) |
| **NEU/PCS (post-concussion syndrome, photo/phonosensitivity)** | Person in post-concussion recovery with phonosensitivity. RT60-specific evidence not located in the populations covered by Phase B; PCS population is absent from acoustic standards in any jurisdiction reviewed. | NO direct evidence in eligible-source pool; claim downgraded to "no quantified target available" at step 6 |
| **OFS/PAIN (orthostatic / pain populations)** | No room-acoustic mechanism identified that this population requires differently from general. | THIN-BASE per BPC; no claim made |
| **general (typical-hearing adult or child)** | Occupant in general-use indoor space. Speech intelligibility intact up to RT60 ≈ 0.6 s in volumes ≤ 283 m³ per established acoustic engineering literature. | ANSI/ASA S12.60-2010 (Tier 6, statutory); BB93 (UK); DIN 18041:2016; UNI 11532-2:2020; AS/NZS 2107; multiple jurisdictions concur. |

**Cross-population arbitration deferred to step 9.** No inline statement that any one population's target supersedes another at this step.

### Step 3 — Jurisdiction comparison table

Per rule #9 step 3: "every surveyed jurisdiction's value at worst-case point; `scope` column."

| Jurisdiction | Standard / Code | Worst-case-point value (general) | Worst-case-point value (DEAF / HI) | Worst-case-point value (NDV/AUT) | Scope |
|---|---|---|---|---|---|
| **US** | ANSI/ASA S12.60-2010/Part 1 | RT60 ≤ 0.6 s (≤ 283 m³); ≤ 0.7 s (> 283 m³ to 566 m³) | RT60 ≤ 0.3 s (≤ 283 m³) per Footnote e (HA/CI users) | not addressed | classrooms / learning spaces; statutory in many states |
| **UK** | BB93 (Building Bulletin 93, 2015) | RT60 ≤ 0.4-0.8 s by room type | RT60 ≤ 0.4 s in "specially resourced provision" for hearing-impaired | not addressed | new build schools; statutory under Education (School Premises) Regulations |
| **UK (transversal)** | PAS 6463:2022 | qualitative ("acoustic calm in sensory-sensitive spaces") | references BB93 | qualitative guidance, no quantified RT60 | publicly accessible buildings; not statutory |
| **DE** | DIN 18041:2016 | RT60 by room type and volume (formula-based: typically 0.4-0.8 s) | annex addresses "Hörsamkeit bei Behinderung" qualitatively | not quantified | acoustic quality in small-to-medium rooms; widely referenced in DE design |
| **IT** | UNI 11532-2:2020 | RT60 by room class A1-A4; A4 (high-criticality educational) ≈ 0.5 s | category A3.1 / A4 explicitly addresses students with hearing deficit; lower RT targets | not quantified specifically; category A4 considers cognitive accessibility qualitatively | classrooms; mandatory citation in IT acoustic design |
| **FR** | NF S 31-080 (2006) | RT60 ≤ 0.4-0.8 s by room category | not differentiated | not addressed | classrooms / offices |
| **AU/NZ** | AS/NZS 2107:2016 | RT60 by space type (table); typical classroom 0.4-0.6 s | references but does not quantify HI-specific | not addressed | recommended levels for indoor spaces |
| **JP** | JIS Z 8731 framework + Barrier-Free Law | general RT guidance; no disability-specific differentiation in the acoustic standard itself | Barrier-Free Law addresses physical access; acoustic provisions not quantified per population | not addressed | acoustic measurement; barrier-free is separate regulation |
| **CN** | GB 50118-2010 | RT60 ≤ 0.7-0.9 s (classroom, by volume) | not differentiated | not addressed | civil-building acoustic design |
| **DK / NO / SE / FI** | National building codes referencing ISO 3382 / NS-EN 16798 | typical 0.4-0.6 s (classrooms) | thin coverage; some references to assistive-listening infrastructure | not addressed | school acoustics |
| **NL** | NEN 3088 | RT60 ≤ 0.5-0.8 s | not differentiated | not addressed | school acoustics |
| **BE** | NBN S 01-400-2 | RT60 ≤ 0.8 s typical classroom | not differentiated | not addressed | acoustic performance |
| **ES** | DB-HR (CTE) | RT60 ≤ 0.7 s typical classroom | not differentiated | not addressed | sound protection (technical building code) |
| **PT** | Portuguese national requirements (RGR / school acoustic guidance) | not separately codified per the BPC's coverage | not differentiated | not addressed | partial coverage in BPC |
| **KR** | KS F 2814 + barrier-free law framework | not separately codified per the BPC's coverage | not differentiated | not addressed | partial coverage in BPC |
| **NL/KO/SV-FI thin** | per BPC header "NL, KO, SV/FI thin; 18/24 jurisdictions" | acknowledged thin coverage | acknowledged thin coverage | acknowledged thin coverage | gap documented |

**Citation-grade verification of this table is PENDING.** Every cell that asserts a specific value for a specific jurisdiction at the worst-case point becomes a `reasoning_doc_citations` row in the rule-#10 pass. None of those rows exist yet; this Pass-1 table is the structure that the Pass-3 pass will verify against the cited sources.

**Note on `[UNVERIFIED-TERMS]` per rule #9.** The 5 flagged languages (AR, HI, ID, SW, BN) do not appear in this parameter's surveyed jurisdiction set — RT60 codes in those languages were not part of the original multilingual coverage. This is a gap in coverage rather than an unverified-keyword issue; logged here for Phase A.11 cross-reference but not blocking this walk.

---

## Pass 1 deliverable boundary

Per `<long_deliverable_protocol>`, this turn ends at the natural review boundary. Steps 4-9 of the rule-#9 walk + the reasoning-doc-citations pass come in subsequent sessions with inline review at each.

### Pass 2 plan (next session)

Step 4 — Lowest-barrier code(s) per population (per terminology entry: "the jurisdiction-level regulatory standard that imposes the lowest barrier to access for the most-constrained user in the parameter's target population, evaluated at the worst-case point in the code's structure"):
- DEAF: ANSI/ASA S12.60 Footnote e (US) — RT60 ≤ 0.3 s — explicitly the lowest barrier in the surveyed set
- NDV/AUT: no quantified jurisdictional standard; PAS 6463 (UK) qualitative is the only codified mention
- DEM: no quantified jurisdictional standard
- general: ANSI/ASA S12.60 main rule (RT60 ≤ 0.6 s) is the lowest barrier at the smallest-volume worst-case point

Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence per population:
- DEAF: Tier 1 dominant (Iglehart 2020/2016, Wroblewski 2012, Neuman 2010, Reinhart 2019, McGarrigle 2019, Saravanan 2019). Co-1: Iglehart's ASA committee role anchors the ANSI footnote.
- NDV/AUT: Tier 3 only (Bettarello 2021, Black 2022) + Tier 4 international (PAS 6463 qualitative). Tier 1 evidence base does not yet exist for quantified RT60-NDV targets.
- DEM: Tier 2-3 (Devos 2019; BrainXchange; Lyngby-Taarbæk POE).

Step 6 — Guidebook chosen value per population (these are the synthesis claims that rule #10 will verify):
- DEAF: RT60 ≤ 0.3 s (proposed, anchored in Iglehart 2020). PMP walk required (rule #8) before this can be a numerical-spec claim.
- NDV/AUT: aspiration ≤ 0.4 s with explicit note "no Tier-1 quantified target available" + reliance on background-noise and sound-masking-contraindication specs from the BPC.
- DEM: ≤ 0.5 s in occupied common areas (matching the BPC's existing language).
- general: ≤ 0.6 s (matches consensus).

Step 7 — Rationale (historical context + clinical basis): drafted from BPC Opus synthesis notes.

Step 8 — Trade-offs: NRC ≥ 0.85 broadband absorption can degrade STI per Amlani & Russo 2016 (REF-00580); the GAP-RAP-01 evidence-auditor adjudication is the trade-off statement.

Step 9 — Cross-population conflict flag: DEAF target (0.3 s) and DEM target (0.5 s) are not in conflict (both lower than general). NDV target (≤ 0.4 s aspiration) is also compatible. **No conflict flag for this parameter** — convergent multi-population case (matches restored CON-0264).

### Pass 3 plan (subsequent session)

Run `reasoning-doc-citations` on every cell of step 3's jurisdiction table that asserts a value + every claim in steps 6-7 attributed to a specific source. Estimate: ~40-60 rows. Each row requires opening the cited source at the cited section and confirming `value_match` or `claim_match`.

Pre-flight: REF-00561 metadata correction must happen before any citation against Bettarello 2021 can land.

### Out-of-band: rule #7 adversarial-research pass

Adversarial-research on the strongest contested claim — **"NDV/AUT require quantified RT60 targets but no Tier-1 evidence base exists for what those targets should be"** — is the next-session priority alongside or before Pass 2. The session should produce a `gaps` row with all four required fields (`confidence_interval`, `shift_conditions`, `named_dissenter`, `falsification_condition`) per rule #7.

Pre-PMP for DEAF RT60 ≤ 0.3 s: queued for the same next-session run; the empirical ceiling probe must clear strict termination before this becomes a numerical-spec claim per rule #8.

---

## Outstanding flags from this pilot session

1. `REF-00561` (Bettarello 2021) metadata is wrong (DOI + publisher) — flagged for `citation-miner` correction before any rule-#10 row is created against it.
2. Items↔BPCs linkage question (`items.bpc_source_slug = NULL` across all acoustic items) is deferred per the chat's strategic discussion — pilot evidence will inform whether a join table is needed before scaling Phase E.
3. PCS population has no acoustic evidence in the eligible-source pool; chosen-value will be "no quantified target available" at step 6 rather than a fabricated number. Confirms rule #10 sub-rule 2 working as intended.
4. KO, NL, SV, FI thin-jurisdiction coverage per BPC header is real and acknowledged; rule #9 step 3 table marks them. Multilingual extension is a Phase A.11 sequel, not in scope.

---

## Metadata

```yaml
reasoning_doc_slug: room-acoustic-performance
parent_bpc: references/bpc/sensory-environment/room-acoustic-performance.md
pilot_designation: TRACK-3-PILOT-1
pilot_pass_completed: PASS-1
pilot_pass_pending: PASS-2 (rule #9 steps 4-9), PASS-3 (rule #10 reasoning-doc-citations), PRE-PASS (rule #7 adversarial-research + rule #8 PMP for DEAF RT60 ≤ 0.3s)
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
