# Inline Critique: Guidebook for Accessible Design v9.0

*Method: working through the document sequentially, recording critical observations inline as encountered. This is a practitioner-facing critique, not an editorial checklist.*

---

## Front Matter and About Section

**Production amendment register is a significant improvement over v8.8.** The explicit table at the top tracking what changed in this version (WS-1A through WS-3E) gives reviewers an immediate orientation to what's new. This should become a permanent feature of all future versions.

**Missing: version supersession statement.** The header says "Version: 9.0" but there's no clear statement that this supersedes v8.8. The old v8.8 included "Version 8.0 Draft supersedes: v6.2 (Final Edition, Rev 6.1)" — this is absent from v9.0. A practitioner picking up this document doesn't know the lineage.

**The Part and Section Map is substantially improved** — Arabic numerals throughout, consistent with the CO-0001 execution. However:

- Part 7 lists "Category K: DeafBlind Environment Provisions (K-01–K-04)" but this is a new addition in v9.0 and sits alongside legacy categories without explanation of why K was chosen (I and J were taken, but this should be noted somewhere)
- "Part 8 — Cross-Population Conflict Resolutions *(Deferred to v10.0)*" is listed in the ToC but has no real content. A reader following the ToC will hit a dead end. The stub should be more explicit: "See §3.4 for interim co-occurrence guidance pending full Part 8 in v10.0."

---

## Volume I

### Part 1: Foundations

**§1.1 — Excellent.** The three-component definition (independence, safety, dignity) remains one of the strongest sections in the guidebook. No critique here.

**§1.2 — Code-as-Floor.** The eleven-jurisdiction quote list is strong but the formatting inconsistency from v8.8 has carried forward: some entries use single quotation marks, some use double, some are run-on paragraphs and some are bullet-formatted. This should be standardised.

**More critically**: the multilingual endorsements stop in 2025 at the latest. Given the guidebook's claim to be calibrated to "best available multilingual evidence," the jurisdictions cited are almost entirely Anglophone (with German/Nordic additions). No Japanese, Korean, Brazilian, or Spanish-language endorsements of the code-as-floor principle are cited here, even though those jurisdictions' standards are cited extensively elsewhere. This is a framing gap.

**§1.3 — A subtle framing issue persists.** The section opens: "A critical failing of code-based accessibility is the implicit assumption that all disabled people within a category have identical functional characteristics." This is correct. But the section then describes variation in terms of "functional capacity" throughout, with the social model framing (disability as mismatch) appearing only by reference. The section would benefit from a brief acknowledgment that this variation is partly about functional capacity *and* partly about environmental design assumptions — the mismatch is bidirectional.

**§1.4.3 — Tier 0 specification change is unexplained.** In v8.8, Tier 0 read: "Single fixed values, calibrated to statistical average." In v9.0 it reads: "Range of values calibrated to an abstractly disabled non-existent person." This is a substantive change in meaning and no rationale is given. The new wording is philosophically sharper but "abstractly disabled non-existent person" is awkward as technical specification language. The amendment register does not flag this change — it should.

**§1.5 — Evidence Hierarchy.** The 7-tier D-18 structure (WS-2A amendment) has been applied, and "Co-primary Tier 2 — Occupational Therapy Clinical Practice Guidelines" has been added. However:

- The new tier is described as "Co-primary Tier 2" but it appears *after* the Tier 2 NGO/advocacy guidelines section, not alongside Tier 1 where co-primary positioning would logically sit. The reader must parse this structural oddity.
- "Co-primary Tier 2 — Occupational Therapy Clinical Practice Guidelines" is a stub — it has a heading but no content, no primary sources listed. Every other tier has an example source list. This looks unfinished.
- The old Tier 1 description included CAOT, JOTA, COTEC/WFOT, AOTA, and RCOT as Tier 1 sources. In v9.0 these have been reclassified to "Co-2" per the WS-2A plan, but the new tier heading only says "Co-primary Tier 2" — it doesn't name any of those organisations. The practitioner who cites CAOT guidelines now has no guidance on what tier that citation sits in.

**§1.6 — DAR Principle.** The cost multiplier table from §1.6 in v8.8 is gone. The reader is told "See Part 11" but the table was functionally useful in Part 1 as a front-matter hook. This is an acceptable trade for structural cleanliness, but the cross-reference should be more prominent.

**§1.7 — CRPD.** The WS-2A plan noted FR-01 (add CRPD Article 19 independent living). This has not been done. §1.7 still only references Article 9 and Article 3. Article 19 is arguably more directly relevant to the guidebook's residential provisions than Article 3. This is an unexecuted amendment.

**§1.8 — Evidence Frameworks.** Intact from v8.8. No issues here, but notably §1.8.10 (Prospect-Refuge Theory) and §1.8.11 (Behaviour Settings) from v8.8 are missing — the section jumps from §1.8.9 to... nothing. The section numbering ends at §1.8.9 (ART and SRT) with no §1.8.10 or §1.8.11 present in v9.0. This appears to be a truncation error. Two complete theoretical frameworks have been dropped without explanation.

**§1.9 — Scope.** The renumbering from §1.11 to §1.9 (WS-2A: S-36) has been executed. The cross-reference at the end now correctly reads "Part 3 (Multiple Categories); Part 8 (Conflict Resolutions)." Good.

---

### Part 2: Disability Categories

**The new Category Code Reference table is cleaner** — Arabic Part numbers, new IntD entry. But it has an obvious schema problem: the table has headers "Code | Category" with a dividing line after the header row, but the rest of the table collapses to a single-column format for the actual entries. This is a Markdown rendering issue — the vertical bar after "Code" is misread as a row separator. The table is technically broken.

**§2.1 MOB — Largely intact.** The "Distinct from BAR" note reads "Large body size design provisions (BAR) address structural load-bearing requirements and dignity provisions and have been relocated to the Supplementary Volume, Section IV." The Section IV reference is stale — per CO-0001 this should now be "Supp. Part 4." Several of these stale "Section IV" references appear to have survived the batch find-and-replace.

**§2.2 UPL — Opening sentence issue.** "UPL is consolidated as sub-code MOB/UPL in an earlier edition." This is vague historical note language that doesn't belong in the current specification. In v8.8 this read "UPL is consolidated as sub-code MOB/UPL in v7.0" — the version reference was removed but the ghost of the sentence remains. Either explain the current status fully or remove the sentence.

**§2.3 VIS — No issues.**

**§2.4 DEAF — Structural improvement.** The two-paragraph structure (audiological; Deaf cultural) has been maintained. The NAD (2023) citation is present. The DeafSpace design principles reference in the core needs list is good. However: "Spatial layouts that support Deaf communication practices" is listed as a core environmental need but there's no specification. What spatial layouts? This is a known gap (Category K addresses some DBL provisions but DEAF-specific spatial provisions remain under-specified in Part 2).

**§2.5 NEU — Critical correction confirmed.** §2.5 and the Uhthoff's reference correctly state "Design environments for MS should target ambient temperatures of 18°C." This aligns with the BPC-1 correction (≤22°C → ≤18°C) flagged as patient safety. Cross-reference to "Part 8, §8.4.4" is correct under the new numbering.

**§2.6 DEM — No issues. The LBD caution is intact and bidirectionally cross-referenced.**

**§2.7 NDV — No issues.**

**§2.8 NDV/MH — Opening sentence persists from earlier editions:** "MH is consolidated as sub-code NDV/MH in an earlier edition." Same vague historical language problem as §2.2. Needs either full context or removal.

**§2.9 PAIN — Short but adequate. The distinct-from-NEU note correctly cross-references §8.4.4.**

**§2.10 DBL — Key framing issue.** The section opens with "Combined vision and hearing loss, making both visual alerts and audio announcements inaccessible or insufficient." This is a functional description, not an environmental barriers description. Given the guidebook's social model framing, the definition should lead with what the environment fails to provide, not what the person lacks. Compare to §2.3 VIS which defines the impairment and then describes environmental needs — here the opening conflates the two.

The Protactile reference is absent from the core environmental needs list. K-03 (Haptic Communication Clear Floor Zone) is one of the four new K items, and Protactile is its primary evidence source (Co-1: Clark 2024), but this isn't surfaced in Part 2 §2.10 at all. A practitioner reading Part 2 before going to Part 7 gets no signal that Protactile-informed spatial design exists.

**§2.11 OFS — Strong.** The three-condition table is well-constructed. The MCAS prevalence caveat (Molderings et al. specialist cohort warning) has been preserved. Good.

**§2.12 IntD — Unchanged from v8.8.** The category is marked "under development" and the note says "full Part II category with OT evidence basis...is under development for v9.0." This is now in v9.0 and it's still not done — the same placeholder text is present. The note should be updated to say "under development for v10.0" and the WS-3C IntD matrix insertions should be reflected in how this section is framed. Currently the section promises interim provisions (listed) and points to DEM and NDV as proxies — this is reasonable but the user of v9.0 deserves an accurate version target, not a stale promise.

---

### Part 3: Designing for Multiple Disability Categories

**§3.1 — BAR column in the co-occurrence matrix.** The matrix still contains BAR as a column and row. Per CO-0001 and the workplan, BAR should have been removed from main-taxonomy matrices. The note at the bottom says "*BAR provisions relocated: see Supplementary Volume 'Designing for Different Body Sizes,' Section IV. BAR column retained for cross-reference continuity (Option B interim).*" Option B was an interim measure described in the workplan, but with a full v9.0 production cycle complete, maintaining a column for a non-taxonomy code is inconsistent with the stated direction. This should be flagged for v10.0 removal.

**§3.4 Key Co-occurrence Design Guidance — Strong content, weak structure.** The fourteen co-occurrence pairs are well-specified with cross-references. However: four new conflict resolutions were added in WS-3E (§8.4.10 DEM/PD floor pattern; §8.4.11 NDV/AUT + NDV/MH colour; §8.4.12 ramp gradient walker vs wheelchair). None of these appear as named pairs in §3.4. The floor pattern conflict (DEM + PD) is particularly important and clinically significant — Parkinson's Disease gait cueing requires high-contrast floor patterns while DEM requires plain floors. This appears in §8.4 (deferred) but not in §3.4 (the current interim guidance section). Practitioners reading §3.4 will not find this conflict.

**The NEU + OFS section specifies rest seating "at ≤15 m on primary routes (more frequent than the ≤20 m standard)"** — this is a tighter specification than E-10 but it's inconsistent with the WS-2B decision to update E-10 to "25–30 m range (median 27.5 m)." Either E-10 was updated (which I'll check when I reach Part 7) or these two sections are now in conflict. This is precisely the kind of intra-document inconsistency the `cross-reference-resolver` was supposed to catch.

---

## Volume II

### Part 4: Synthesis and Sequencing

**§4.3 Principle 3** references "conflict register in Parts E and F" — this is stale v8.8 language (Parts E and F were pre-renaming). Should read "Part 8" in v9.0. The `cross-reference-resolver` should have caught this.

**§4.4 Stage 0 Brief** contains: "Conflict register: pre-populate with standard conflicts from Parts E/F relevant to building type." Same stale reference.

**§4.5 Strategy A** references "Universal Non-Residential Provisions (Part F §F.0)" — stale. Should be "Part 6 §6.0" in v9.0.

**§4.5 Strategy A** also references "conflict resolutions from Part F §NR.3" — stale.

These are systematic cross-reference failures. Several appear to have been missed by find-and-replace because they use "Parts E and F" rather than the item codes the search targeted. This is a known limitation of the deferred "Chapter C" batch.

**§4.6 Decision Framework Q3** says "apply the resolution documented in Parts E/F" — same issue.

**§4.7 Worked Examples — Generally strong.** The five worked examples are detailed and well-structured. Notable improvement: Worked Example 4 now correctly uses "→ Supp Vol IV" for BAR references in some places.

However, WS-2C note U-003 specified: "Worked example 5: remove BAR as primary population; replace with Supp. Vol. cross-reference." Worked Example 5 does NOT list BAR — it lists "MOB primary (all 12 residents); DEM secondary; NDV/AUT tertiary; PAIN + OFS." The BAR references in the worked examples were correctly cleaned. Good.

**§4.8 — This section has a numbering error.** It reads "§I.8 From Approach to Application" in the heading, with the text below correctly positioned as §4.8. The Roman numeral heading is a surviving artifact from the v8.8 structure that was not caught.

The cross-references within §4.8 are also stale: "Entry Paths I–III, preceding Part I" should reference the Part 4 Entry Paths. "§I.7 (Worked Examples)" should be "§4.7." "§I.1–§I.7" should be "§4.1–§4.7." The entire internal cross-reference structure of §4.8 is unreformed. This section appears to have been copied from v8.8 with minimal updating.

---

### Part 5: Residential Application Matrices

**The section numbering is wrong from the start.** The section heading reads "6.0 How to Read the Residential Matrices" — this should be "5.0." The sub-sections are numbered 6.1 through 6.10, all of which should be 5.1 through 5.10. This is a systematic numbering error throughout the entire residential matrices section — every room code (R-ENT, R-GAR, etc.) is prefixed with 6.x when it should be 5.x. This will create index confusion for any practitioner trying to follow the Part/Section Map from the front matter.

**Universal Residential Provisions table** — uses "K-01" for "Lever hardware on all doors." But K-01 in the new Category K is "Intervenor Adjacency at Service Counters" (a DBL item). The lever hardware item has been I-01 throughout the guidebook. This is a cross-contamination error — the old K-01 (upper limb) has been reassigned to a new K-category item (DBL), but the Universal Residential Provisions table hasn't been updated.

**IntD column added to matrices (WS-3C).** The IntD additions appear in the R-ENT, R-BED, R-GAR, R-LAU, R-LIV, R-KIT, R-HAL, R-STA tables. The standing disclosure `[TIER 4-5; interim; March 2026]` appears in the introductory note but is not repeated per-cell. Given the guidebook's evidence standards, some readers will not connect the introductory note to individual cell entries. This is acceptable practice — but should be flagged.

**R-ENT table — DBL additions:** K-02 and K-04 appear as new rows. This is correct per WS-3B. However K-04 (Vibrotactile alert) has "DEAF ●" as well as "DBL ●" in the entry — but looking at the DBL column specifically, the table has 11 columns with IntD added. This is now a very wide table and the Markdown rendering will likely be problematic on narrow displays.

**R-BED table.** The DEAF column now has B-10 (Visual fire alarm / vibrating alert) with a primary bullet — this is the WS-3D DEAF residential coverage addition. K-04 (Vibrotactile bedside alert) is added for DBL. However, looking carefully at the table: it now has 12 population columns. This is approaching the practical limit of what Markdown tables can render usably. No guidance is given on how to handle this for practitioners using the document on screen.

**R-BA (Bathroom) table.** DEAF and DBL columns have been added (B-10 for visual alarm, K-04 for vibrotactile). The R-BA table previously identified "BAR" as a primary population — that column is retained with "→ Supp Vol IV" references. The split R-BA-04a / R-BA-04b from v8.8 has been maintained. Good.

**R-LIV table.** The DEAF column now includes A-11 (hearing loop in living room) ● and K-03 (haptic communication clear floor zone) for DBL. However K-03 is listed under the DBL column but doesn't appear in the non-residential matrices I've reviewed yet — need to check consistency.

**DAR Priority Register (§6.10 / should be §5.10).** Unchanged from v8.8 except for reference corrections. The "large body size structural (BAR → Supp Vol IV) floor provision" entry in the table maintains the messy embedded cross-reference syntax. This should have been cleaned to simply "See Supplementary Volume, Supp. Part 4" in a clean cell.

---

### Part 6: Non-Residential Application Matrices

**§7.0 Universal Non-Residential Provisions** — again, section numbered 7.0 when it should be 6.0. Same systematic numbering error as Part 5.

**The Universal NR table has been updated.** "E-08: Corridor clear width ≥1500 mm (≥1800 mm HLT/TRP)" now correctly references "Supp. Part 4" instead of the old Category J for BAR. Good.

**NR-EDU (§7.1 / should be §6.1).** The DBL additions are present — K-02, K-03 referenced in classroom and assembly hall space criticality table. The IntD provisions note is appended after the education schematic checklist with the appropriate disclosure. However: the IntD provisions note for NR-EDU says "Apply to all educational settings serving students with intellectual disability" — but the preceding space criticality table doesn't include IntD as a named population anywhere. A practitioner scanning the table for their population code will miss the IntD note entirely.

**NR-HLT (§7.2 / should be §6.2).** The DBL additions are present in the space criticality table. The IntD provisions note is appended. Same issue as NR-EDU — IntD isn't named in the primary space criticality table.

The TC-01 specification in the patient ward row reads "≤24°C general; ≤18°C MS ward" — this is correct and reflects the BPC-1 patient safety correction.

**NR-WRK (§7.3 / should be §6.3).** The DBL workplace provisions are described as "reasonable adjustment provisions; implement on identified need" — this is an important qualification that distinguishes DBL workplace provisions from universal provisions. The framing is appropriate.

**NR-CUL (§7.5 / should be §6.5).** "Tactile building map station (K-02) mandatory at all cultural venue principal entrances" — this is strong. The 90-day currency requirement for map updates is specified. Good.

**NR-TRP (§7.7 / should be §6.7).** The transport DBL provisions are the most comprehensive of any building type — vibrotactile floor panels, personal pager BMS infrastructure, staff assistance points with tactile communication materials. The IntD transport note is useful and practical.

---

### Part 7: Item Specification Library

**Category A: Acoustics — generally well-preserved from v8.8 with corrections applied.**

**A-10 and A-11 — Applicable Groups correction.** Both now read "DEAF, DBL" rather than the incorrect "VIS (hearing device users)." The WS-2A correction has been applied. Good. However: the "VIS (Deaf/HoH users)" language has been removed from the preamble but in the Evidence Basis section of A-10 we still find "The counter loop is an environmental compensation enabling the occupation of independent service interaction for users dependent on hearing devices." This is functionally fine but "VIS (Deaf/HoH)" was a code error, not a content error — the evidence basis language is acceptable as written.

**A-10, A-11, A-12 DBL evidence notes.** The thin-base disclosure has been added: `[THIN BASE — Tier 2+4 only; no Tier 1 OT clinical research on DeafBlind built environments in any jurisdiction; March 2026]`. This is the WS-3A implementation. However: the disclosures appear *after* the Applicable Groups line rather than in a consistent position. In some items the disclosure is in the middle of the specification; in others it's between sections. This should be standardised — ideally as a named sub-field in the item template.

**A-13 — Non-English evidence block.** The De Hogeweyk reference in A-13 includes the original metrics (94% vs 34% wayfinding success). This is correct but the source note at the end of this item says "BuroKade/Vivium, Dutch-language reports, 2012-2019" — these have been flagged as UNVERIFIABLE in the BPC. The item carries the data without the UNVERIFIABLE flag. This is an inconsistency between BPC standards and the item library.

**B-10 — Visual Fire Alarm.** The specification reads "75 candela minimum" but §2.4 DEAF specifies "strobes ≥110 cd." In v8.8 this was noted as a conflict (GAP-STEP5-01) requiring reconciliation. WS-2A planned to "reconcile 75 cd (item) vs ≥110 cd (§2.4 DEAF) — adopt EN 54-23 spatial coverage method; add footnote." This reconciliation has NOT been executed. The conflict remains. A reader comparing §2.4 (110 cd) to B-10 (75 cd) will find two different specifications for the same provision. This is a patient safety adjacent issue for Deaf occupants.

**Category C: C-04 LRV Contrast.** In v8.8 this read "Minimum 35 LRV in DEM/elderly public settings. Minimum 40 LRV in aged care/DeafBlind settings." In v9.0 this is unchanged. WS-2B planned to "replace flat ≥30 with tiered table." The tiered table has NOT been implemented. The specification still uses flat ≥30 as the primary value with unformatted supplementary text. This is an unexecuted WS-2B amendment.

**Category D — generally well-maintained.** The cross-references from v8.8's "Part V" have been updated to "Part 7" in most places. However D-06 (Memory Boxes) has an evidence basis note that reads "Allen's CDM. Dead-end elimination removes a wayfinding failure mode..." — this is the evidence basis for D-01 (Loop Floor Plan), not D-06. This is a copy-paste error from v8.8 that has persisted.

**E-10 Rest Seating.** Maximum interval remains at "20m" in the specification. WS-2B planned to update this to "25–30 m range (median 27.5 m); reclining seating option required on primary OFS-designated routes." This has NOT been executed. But §6.0 (Universal NR Provisions) now reads "E-10: Rest seating at ≤25 m on all primary routes" — different from E-10's own specification of ≤20 m. There are now THREE different rest seating intervals in the document: 20m (E-10 item), 25m (Universal NR), and 15m (§3.4 NEU+OFS). This is a significant intra-document inconsistency.

**Category F: Sensory Zoning — F-04 and F-05 are new and well-drafted.** The air quality and seated-task specifications are clinically grounded. Both correctly carry Tier X flags noting absence of RCT evidence.

**Category G — generally clean.** G-03 (Grab Bars) carries the corrected Levine et al. (2024) citation replacing the unverified 2023 version. The "Evidence note (v9.0)" callout correctly explains the substitution. This is good editorial practice.

The BAR references throughout Category G now consistently redirect to "Supplementary Volume, Supp. Part 4" rather than the old J-category items. However: G-02 still lists "BAR seating: minimum 1 reinforced chair ≥250 kg per area (see Supplementary Volume, Supp. Part 4)" — but the Supplementary Volume uses "J-02" for this specification. The cross-reference to "Supp. Part 4" is correct in direction but doesn't give the item code, which matters for a practitioner trying to navigate.

**Category K: DeafBlind Environment Provisions (K-01 through K-04).** This is new in v9.0 and represents the WS-3A/3B implementation. Critical assessment:

**K-01 (Intervenor Adjacency).** Well-structured. The 1200mm counter width specification (wider than standard G-06 1000mm) is evidence-based from DbI guidelines. The staff awareness note ("speak to the DeafBlind user directly, not to the intervenor") is an important dignity provision that goes beyond most standards. Strong item.

**K-02 (Tactile Building Map Station).** The 90-day currency requirement is specific and actionable. The approach route specification (TWSI directional bar from entrance) ensures the map is findable. The companion audio option is well-framed as optional. One issue: the specification says "minimum 400 × 300 mm tactile field; maximum 600 × 450 mm (beyond this, single-session orientation is not achievable)" — the maximum is stated as if this is evidence-based, but no source is cited for the cognitive limit claim. This should be flagged as `[UNSUPPORTED — citation required]`.

**K-03 (Haptic Communication Clear Floor Zone).** The Protactile Co-1 evidence basis is appropriately cited. The 1500 mm zone at service points and 900 mm alongside seating are derived from two-person communication positioning. The note that "no architectural standard in any jurisdiction mandates haptic communication clear floor zone dimensions" is honest and important. The [EXPERT CONSENSUS] disclosure is used correctly.

**K-04 (Vibrotactile Alert).** This item is the weakest of the four. The vibration frequency specification (20–200 Hz) cites Verrillo (1993) for tactile sensitivity thresholds, but Verrillo's work is on intact sensory sensitivity — its applicability to the diverse sensory profiles of DeafBlind persons is not discussed. The spec also lists both floor panel and personal pager systems without clearly distinguishing when each applies. The "charging station at accessible height" requirement is practical but the position (home base within building) is vague for non-residential contexts.

**E-11 Coverage Gap Note** still reads "deferred to v9.0" — this is a self-referential error. The note was written for v8.8 and says provisions are deferred to v9.0, but we're now in v9.0 and they're still not done. Should read "deferred to v10.0."

**H-04 Coverage Gap Note** has the same problem: "Deferred to v9.0." Now it's v9.0 and NDV/NEU control interface specifications are still absent.

---

### Part 9: Engineering and Coordination

**The section is well-structured** and the discipline-based organisation (AC, EE, ME, SE) is cleaner than the previous categorisation. The VE Protection Register is an important addition.

**Systematic cross-reference issue:** Throughout Part 9, references to "Part 12 §12.4.x" appear. These are correct for v9.0. However several entries still read "See Part VIII, C.1.x" or "See Part VIII §8.4" — these are v8.8 references that survived. Specifically: A-08 Retrofit cost note reads "See Part 12 §12.4.2" in the item library but some Part 9 tables still reference the old Part VIII format.

**The Stage-Gated Coordination Protocol (§9.3)** is one of the most practically valuable additions to v9.0. The "If Missed" multiplier column is clear and actionable.

**The SE brief standard clause** contains "Rick Hansen Foundation 2023; TERRAGON/DStGB 2017" as citations for the cost multiplier figures. These are the correct sources, properly cited. Good.

---

### Part 10: Working with Specialist Consultants

**Major structural issue: the internal section numbering.** Part 10 is titled "Working with Specialist Consultants" but its sections are numbered §9.1, §9.2 through §9.8. This is clearly a carry-forward from when this content was originally drafted as "Part VI" or similar. The section numbering §9.x within a document Part numbered 10 is deeply confusing. A practitioner cross-referencing "§10.3" would be looking for a section numbered 10.3, not one labelled §9.3 within Part 10.

**§9.2.6 (within Part 10) says** "This guidebook is a distillation of OT evidence into architectural specification form. Its design library items (Part 7)..." — this is good internal consistency.

**The Specialist Consultant Coordination Protocol (§9.7)** gives a sensible five-step sequencing. However: step 2 says "DeafBlind design consultant" — there is no such specialist type named anywhere in the standard professional landscape. The guidebook acknowledges this implicitly (K-01 through K-04 are all expert consensus with no standards base) but names the consultant type as if they exist in the market. The section would benefit from a note that DBL specialist consultancy may need to be sourced from organisations like DbI Nordic or Sense UK rather than from specialist architectural practice.

**§9.8 — Disability Organisations and Lived Experience Input.** Good section, well-framed. References the 17-Jurisdiction Research Compendium §A1–A17, which is not actually included in the v9.0 document. This is a hanging reference to a companion document that may or may not exist separately.

---

## Volume III

### Part 11: DAR

**The DAR cost multiplier table (§11.1)** has a broken cell: "Large body size floor loading (BAR → Supp. Part 4) floor loading (4.0 kN/m²)" — the description is duplicated mid-cell. This is a formatting artifact from the renaming pass.

**§11.7 Case Study Evidence** — now correctly references Part 13 case study section numbers (§13.03, §13.07, §13.14) rather than "Part IX-03" etc. Good.

---

### Part 12: Economics

**This is the most complete and well-argued section of the guidebook.** The core ratio, cost intelligence tables, and client argument frameworks are strong.

**§12.3.3 Market and Institutional Value.** The Hangzhou elevator study (5.53% price increase) is flagged with "Single-city study; treat as jurisdiction-specific, not generalisable without corroborating evidence." This is exactly the right epistemic qualification and it was flagged in the workplan (PR-019) for citation improvement. The citation itself ("Buildings, 2024") is vague — the full citation has apparently not been added. Buildings is a journal (MDPI) and the 2024 volume, issue, and article number are not given.

**§12.4 Cost Intelligence Tables.** All Part references have been updated to Part 7 codes (A-04, B-03 etc.) rather than old Part V codes. The tables are cross-navigable.

**§12.10.4 Editorial Note: Part 7 Items Requiring Evidence Updates.** This persists as a living editorial note — appropriate in a draft, but should be converted to gap register entries and removed from the body before external publication.

---

### Part 13: Case Studies

**Case study numbering has been changed** from "Part IX-01" to "§12.01" through "§12.14" — but they should be "§13.01" through "§13.14" per the Part 13 designation. The cross-references in Part 11 §11.7 use "§13.03" etc., but the actual case study headers read "§12.01." Internal inconsistency.

**§12.09 De Hogeweyk.** The POE reports are cited as "BuroKade/Vivium, Dutch-language reports, 2012–2019" — flagged as UNVERIFIABLE in the BPC. No UNVERIFIABLE flag appears in the case study body. Readers relying on this case study for the 94% wayfinding figure will not know the underlying verification status of the primary source.

**§12.12 Village Landais Alzheimer.** The 31% psychotropic medication reduction figure is cited as "NORD Architects / Département des Landes, unpublished in English." The BPC flags this as grey literature. The case study correctly notes "unpublished in English" but doesn't note that this means independent peer review has not occurred.

---

## Appendices

### Appendix B: Biophilic Design

**BIO-01 Retrofit cost note** reads "See Part 11I §8.4" — this is corrupted notation. "Part 11I" is not a real part number. This appears to be an artifact of a failed substitution (Part VIII → Part 11I?). Several BIO and TC items contain similar corrupted cross-references ("Part 11I §8.4.x" appears at least six times across the appendices). This is a systematic substitution error.

### Appendix C: Thermal Comfort

**TC-01 — correct.** Ambient ≤18°C is correctly specified. The cross-reference to "Part 8 §8.4.4" is correct.

**TC-05 — the evidence update note.** "See Part 11I §8.10.4" — same corrupted reference. Should read "See Part 12 §12.10.4."

---

## Supplementary Volume

**The Supplementary Volume is largely unchanged from v8.8 in terms of content.** The BAR relocation and CHD/LPA/EXH sections appear to be carried forward. The preamble has been updated from "v7" to "v9.0" (per WS-2C S-03 amendment) and "DEAF" has been added to the population code list (WS-2A F-13).

**Section I (CHD).** The age-band framework and building typology matrices are valuable content not found elsewhere in mainstream accessibility literature. The evidence notes are appropriately cautious (⚠ EVIDENCE NOTE throughout).

**Section II (LPA).** The LPA-07 (Seating and Workstations) item recommends footrests for LPA/ACH users with a note: "⚠ EVIDENCE NOTE: No specific study confirming optimal seating parameters for LPA users was identified for the footrest recommendation; derived from clinical principles." This is good epistemic hygiene.

**Section IV (BAR) — the most significant gap.** The section explicitly states: "Large body size is not a disability." This is the correct framing per the workplan. However: the Category J items in Part 7 (J-01 through J-05) were supposed to be deleted per CO-0001 Pass 6. Looking at Part 7, I see **no J-category items** — Category J heading and all J items are absent. But the Not-Retrofittable table in the Volume II header still reads "J-04 (BAR → Supp Vol IV) | large body size wet room structural floor (BAR → Supp Vol IV) | SD | Permanent structural inadequacy | Structural drawings (SE confirmation)." 

So: J-items deleted from Part 7 ✓, but J-04 reference persists in the not-retrofittable table ✗. This is an incomplete deletion.

**Section V (Guidebook Revision Notes)** — per CO-0001 Pass 11, this section was supposed to be deleted ("No redirect — content is on GitHub"). It is **still present** in the v9.0 document. This is an unexecuted CO-0001 pass.

---

## Overall Assessment

### What v9.0 Gets Right

1. **Arabic numeralisation (CO-0001)** — the structural renumbering from Roman to Arabic parts/volumes is executed throughout most of the document. This is a major improvement.
2. **Category K (DBL provisions)** — the four K-items are genuinely new content, grounded in Co-1 Protactile evidence, with appropriate [EXPERT CONSENSUS] disclosures. This is the most intellectually honest new content in the edition.
3. **IntD matrix insertions** — the interim coverage approach (DEM/NDV as proxy with disclosure) is epistemically sound.
4. **B-10/temperature patient safety corrections** — the ≤18°C correction is confirmed applied throughout.
5. **Evidence hierarchy reform** — the 7-tier structure with Co-primary tiers is cleaner than the old 6-tier.
6. **Part 9 engineering coordination** — the stage-gated tables and VE protection register are significant practical improvements.
7. **DEAF code correction** — VIS/DEAF replaced with DEAF throughout relevant items.

### What v9.0 Does Not Complete

1. **Systematic section numbering errors** in Parts 5 and 6 (numbered 6.x and 7.x respectively)
2. **Multiple stale Part E/F cross-references** throughout Volume II
3. **Rest seating interval inconsistency** — three different values coexist (15m, 20m, 25m)
4. **B-10 visual alarm intensity conflict** — 75 cd vs 110 cd unresolved
5. **K-01 misassignment** in Universal Residential Provisions table
6. **§1.8.10/§1.8.11 truncation** — two theoretical frameworks dropped without explanation
7. **Corrupted cross-references** — "Part 11I" appearing in appendices
8. **Case study numbering** — §12.01 vs §13.01
9. **Section V of Supplementary Volume** still present (CO-0001 Pass 11 unexecuted)
10. **J-04 in Not-Retrofittable table** — J-category deletion incomplete
11. **Version-stale gap notes** — "deferred to v9.0" appearing in a v9.0 document
12. **§4.8 Roman numeral heading** and stale internal cross-references
13. **CRPD Article 19** still absent from §1.7 (FR-01 unexecuted)
14. **Co-primary Tier 2 evidence tier** stub — heading without content
15. **C-04 tiered LRV table** — WS-2B amendment unexecuted

### Priority Corrections Before External Distribution

**P1 (publication blocking):**
- Section numbering correction in Parts 5 and 6
- K-01 misassignment in Universal Residential Provisions
- B-10 intensity conflict (75 cd vs 110 cd)
- "Deferred to v9.0" notes updated to v10.0
- "Part 11I" corrupted references corrected

**P2 (significant but non-blocking):**
- Rest seating interval standardised across three locations
- §4.8 Roman numeral heading and stale cross-references
- Case study section numbering (§12.xx vs §13.xx)
- Section V Supplementary Volume deletion
- Co-primary Tier 2 content populated or removed

**P3 (editorial):**
- §1.8.10/§1.8.11 restoration or documented removal
- "consolidated as sub-code...in an earlier edition" ghost sentences cleaned
- D-06 evidence basis copy-paste error corrected
- IntD named in space criticality tables, not only in appended notes
