# Project Standards
<!-- Managed by session-consolidator. Do not edit manually. -->
<!-- Append new RULE blocks at the bottom. Never overwrite existing entries. -->

---

## Core Doctrine (locked)

RULE: Three-Tier Design Hierarchy governs all specifications. Tier 0 = Universal Design / Code Compliance (population-agnostic, fixed values). Tier 1 = Population-Informed Inclusive Design (ranges; median as default). Tier 2 = Person-Specific Co-Design (OT assessment resolves position within Tier 1 range). DAR mandatory at all tiers.
CONDITION: All specification items.
ACTION: Every item must identify which tier it serves and apply that tier's specification standard.
DATE: Established — pre-session

RULE: Universal design is co-extensive with code compliance — the floor, not an aspiration. Inclusive design is the positive aspiration.
CONDITION: All editorial and framing decisions.
ACTION: Never frame UD as aspirational. Never frame ID as obligatory minimum.
DATE: Established — pre-session

RULE: BAR is not a main taxonomy code. Large body size is not a disability. BAR provisions belong in Supplementary Volume §IV only. Category J (J-01 through J-05) is to be struck entirely from Volume 2 Part IV. No BAR reference, cross-reference, or heading is permitted anywhere in Volumes 1–3. Delete on sight; do not relocate — items already exist in Supplementary Volume §IV.
CONDITION: Any item, cross-reference, or heading in Volumes 1–3.
ACTION: Flag and delete any BAR or J-code instance in Volumes 1–3. Do not replace with Supplementary Volume pointers.
DATE: Established — pre-session; updated 2026-03-18 20:10

RULE: Specification ranges are not expressions of uncertainty. They are the designed-in bridge between Tier 1 and Tier 2. At Tier 1 use median. At Tier 2 resolve through co-design.
CONDITION: All range specifications.
ACTION: Never write a range without specifying which end applies at which tier.
DATE: Established — pre-session

RULE: Lived experience evidence is co-primary at Tier 3–4 where no clinical trial is feasible.
CONDITION: Evidence stratification decisions.
ACTION: Do not subordinate lived experience evidence to clinical research when no RCT is feasible for the population.
DATE: Established — pre-session

RULE: VIS and DEAF are separate independent population codes — never grouped or combined. VIS = visual impairment. DEAF = Deaf/hard of hearing/hearing device users. DBL = DeafBlind — a third distinct population, not a combination of VIS + DEAF. VIS/DEAF as a compound code is an error requiring correction on sight.
CONDITION: All population code usage throughout Volumes 1–3, matrices, item specs, glossary, abbreviations.
ACTION: Replace all VIS/DEAF compound instances with standalone VIS or DEAF as appropriate. Update all matrices, glossary, and quick reference tables.
DATE: Established — pre-session; updated 2026-03-18 20:20

RULE: IntD (Intellectual Disability) is a main-body population category. It appears in Volume 1 Part II and receives full item coverage in Volume 2 matrices, residential and non-residential. All IntD specifications carry THIN-BASE disclosure: [TIER 4-5; no quantified architectural standard in any jurisdiction; March 2026].
CONDITION: Any task touching IntD population coverage.
ACTION: Treat IntD as a full main-taxonomy category. Author items in main body. Apply THIN-BASE disclosure to all IntD specifications.
DATE: 2026-03-18 20:20

RULE: Biophilic Design (BIO-01–BIO-05) and Thermal Comfort (TC-01–TC-05) are canonical in Volume 3 Appendix B and Appendix C respectively. Supplementary Resources A and B in the Volume 2 body are to be struck. No inline BIO- or TC- cross-references are permitted in Part IV item specs or room matrices. A single opening notice is permitted in volume front matter: "This guidebook includes supplementary appendices covering biophilic design (Appendix B) and thermal comfort (Appendix C)."
CONDITION: Any edit touching Volume 2 body or Part IV item specs.
ACTION: Delete Supplementary Resources A and B from Volume 2. Remove all inline BIO- and TC- cross-references. Retain opening notice only.
DATE: 2026-03-18 20:10; consolidated 2026-03-18 20:20

---

## Item Code System

RULE: V2-P4-XX is the canonical item code system. V2-PV-XX is deprecated and must not be used.
CONDITION: All item codes in all volumes.
ACTION: Replace any V2-PV-XX instance on sight.
DATE: Established — pre-session

---

## Citation and Evidence Standards

RULE: All sources must be confirmed real before inclusion. Unverified claims → [UNVERIFIED — DOI/URL required before publication].
CONDITION: All citations.
ACTION: Never silently remove unverified claims — flag them. citation-verifier defaults to PROVISIONAL mode.
DATE: Established — pre-session

RULE: G-03 cites two Levine papers — Levine 2023 (Human Factors) AND Levine 2025 (JMIR). Both required.
CONDITION: Item G-03 and room matrix R-BA-02.
ACTION: Levine 2023: doi:10.1177/00187208211059860. Levine 2025: doi:10.2196/69442. Replace any "Levine 2024" reference with both.
DATE: 2026-03-17 21:30

RULE: NIH NIOSH storage height claim (40% strain reduction at shoulder-hip zone) — primary source not confirmed.
CONDITION: Any citation of this claim in PAIN items.
ACTION: Flag [UNVERIFIED — DOI/URL required before publication] until primary source retrieved.
DATE: 2026-03-18 10:00

RULE: If a publication blocker requires citation verification and two or more independent searches across sessions have returned no confirmed source, the item or specification value is to be deleted rather than indefinitely flagged. Deletion is the resolution. Do not accumulate unresolvable UNVERIFIED flags. Log deletion in gap_register.md as CLOSED-DELETED.
CONDITION: Any specification value carrying [UNVERIFIED] after two or more failed independent search attempts.
ACTION: Delete the specific value or claim. Retain the item structure if the remainder is evidence-supported.
DATE: 2026-03-18 19:10

---

## Specification Upgrades (rules confirmed by evidence)

RULE: E-08 corridor primary route specification is ≥1500 mm (not 1200 mm).
CONDITION: Any primary route corridor specification in public buildings.
ACTION: Upgrade to ≥1500 mm citing DIN 18040-1 + TEK17 §8-6. Note: 1200 mm acceptable for secondary residential corridors only.
DATE: 2026-03-17 21:30

RULE: C-04 LRV contrast is a split tiered table within the single item C-04. No new item code is created. Row 1: general accessible environments ≥30 LRV. Row 2: critical navigation junctions ≥40 LRV. A note is added for severe VIS users: environments serving severe VIS may require ≥65% Michelson contrast at critical junctions and signage (Dain 2022; DIN 32975 K≥0.7). Conflict resolution note cross-referencing C-04 vs C-05 to be added in Part E.
CONDITION: C-04 item specification and any item citing LRV thresholds.
ACTION: Replace single-value spec with two-row tiered table. Add severe-VIS note. Add Part E conflict note.
DATE: 2026-03-17 21:30; updated 2026-03-18 20:20

RULE: Ramp gradient for independent propulsion — evidence maximum is 6% (1:16.7), not 8.3% (1:12).
CONDITION: E-03 and all ramp gradient specifications.
ACTION: Maintain ADA 1:12 as Tier 0 code floor. State 6% (DIN 18040; TEK17) as Tier 1 evidence-supported maximum for independent propulsion. 8.3% acceptable only for short assisted rises ≤0.30 m.
DATE: 2026-03-18 10:00

RULE: Turning circle standard values serve ≤50th percentile of wheelchair users. 95th percentile power chairs require 2100 mm; scooters require 2489 mm.
CONDITION: All turning circle specifications.
ACTION: Tier 1 range: 1300 mm (indoor manual, minimum) → 2100 mm (power chair, preferred). Specify 2489 mm for scooter-inclusive environments. Cite D'Souza 2011 + CSA B651:23.
DATE: 2026-03-18 10:00

RULE: E-10 rest seating interval is 25–30 m (Tier 1 range; median 27.5 m), replacing the previous 20 m value. OFS populations additionally require reclining/tilt seating option at each station.
CONDITION: E-10 item specification and all room-matrix references to rest seating interval.
ACTION: Update E-10 to 25–30 m range with 27.5 m median. Add OFS seating-type note. Update all room matrices referencing the 20 m value.
DATE: 2026-03-18 20:20

RULE: H-04 does not include temperature specification. Temperature for OFS/PAIN populations is addressed exclusively in Thermal Comfort Appendix C. Any temperature content in H-04 is to be removed and replaced with: "For thermal environment requirements for OFS and PAIN populations, see Appendix C."
CONDITION: H-04 item specification.
ACTION: Remove temperature content from H-04. Add single cross-reference note to Appendix C.
DATE: 2026-03-18 20:20

---

## Structural Decisions

RULE: B-10 strobe VAD seizure risk is a gap across all European standards.
CONDITION: B-10 specification.
ACTION: Retain item. Flag as [SYSTEMIC GAP — no European standard specifies strobe frequency limit for VAD; UK interim guidance only].
DATE: 2026-03-17 21:30

RULE: All PAIN and OFS item specifications must carry: "Specifications for this item serving PAIN and/or OFS populations are derived from expert consensus and clinical evidence; no built-environment design research base exists for these populations in any of 14 languages searched (March 2026). [EXPERT CONSENSUS — March 2026]"
CONDITION: Any item specification serving PAIN or OFS populations.
ACTION: Apply disclosure note to all PAIN/OFS provisions including E-10, G-06, A-09, and all room matrix provisions.
DATE: 2026-03-18 18:30

RULE: DBL room matrix additions carry: [EXPERT CONSENSUS — no standard; March 2026]. IntD room matrix additions carry: [TIER 4-5; March 2026]. Both disclosures are mandatory.
CONDITION: Any DBL or IntD provision added to room matrices.
ACTION: Apply respective disclosure per item-spec-revisions-2026-03-18-18-00.md §6.
DATE: 2026-03-18 18:30

RULE: DBL is included in the Part III co-occurrence matrix (§III.3) and co-occurrence design guidance (§III.4) as a standalone population. A note at the end of §III.4 explains that DBL requirements arise from the primacy of tactility and combined sensory loss — not from the sum of VIS and DEAF provisions.
CONDITION: Part III co-occurrence matrix and guidance.
ACTION: Add DBL row/column to §III.3. Add DBL guidance to §III.4. Add explanatory note at end of §III.4.
DATE: 2026-03-18 20:20

RULE: Part I section §1.11 Scope is renumbered to §1.9. No content authored for the gap. All cross-references to §1.11 updated to §1.9.
CONDITION: Part I section numbering.
ACTION: Renumber §1.11 → §1.9. Update all cross-references throughout the document.
DATE: 2026-03-18 20:20

RULE: Part V (Engineering and Coordination) contains placeholder headings only. Each of V.1–V.5 carries: "Brief template to be provided. Engage relevant specialist consultant at [design stage]." No templates to be authored in this edition.
CONDITION: Part V content.
ACTION: Add placeholder note under each V.1–V.5 heading.
DATE: 2026-03-18 20:20

RULE: De-escalation rooms are out of scope. No item to be authored. May be noted in gap register only.
CONDITION: Any request to author a de-escalation room item.
ACTION: Decline item creation. Log as scope-exclusion if raised.
DATE: 2026-03-18 20:20

RULE: IntD-specific emergency egress is covered by the existing deferral to jurisdiction-specific building codes (Appendix D). No separate IntD egress item to be authored.
CONDITION: Any request to author IntD egress provisions.
ACTION: Refer to Appendix D deferral. No new item.
DATE: 2026-03-18 20:20

RULE: When Category J cross-references are struck from room matrices, entry paths, and reading guides, they are deleted without replacement. No pointer to Supplementary Volume §IV is added.
CONDITION: find-and-replace pass striking Category J.
ACTION: Delete all J-code cross-references. Do not replace.
DATE: 2026-03-18 20:20

---

## Research Log Standards

RULE: research-log-manager CHECK must be called before any multilingual-research run. research-log-manager LOG must be called after every run. Skipping either is an error.
CONDITION: Every multilingual-research invocation.
ACTION: No exceptions. If LOG was missed in a prior session, flag as BLOCKER in the next session-close YAML.
DATE: Established — pre-session

RULE: Staleness threshold for BPC entries is 90 days. Entries older than 90 days → STALE on CHECK. Re-run multilingual-research for any STALE entry in an active section.
CONDITION: All BPC retrieval operations.
ACTION: Compare last_searched date to current date. If >90 days: status = STALE, proceed to full re-run.
DATE: Established — pre-session

RULE: SCOPE-GATE-CANDIDATE: 3+ independent searches returning NO-DATA for the same language across different topics → append P3 item to gap_register.md.
CONDITION: research-log-manager LOG operations.
ACTION: DA, FI, ZH, JA confirmed SCOPE-GATE-CANDIDATEs for PAIN/OFS population searches. Never permanently exclude a language.
DATE: 2026-03-18 10:00

RULE: Early-close gate is SUSPENDED for all multilingual-research runs on population categories and item-level searches. All 9 core languages must be fully searched before a run closes. EXCEPTION: IntD only — early-close gate remains active; literature is confirmed absent in non-English sources.
CONDITION: Any multilingual-research run except IntD.
ACTION: Run all 9 core languages to completion. Do not close at early-close gate. Record all NO-DATA and THIN results explicitly.
DATE: 2026-03-18 15:00

---

## Session Management

RULE: Never re-run a completed stage. Consume existing outputs.
CONDITION: Session start and task intake.
ACTION: Confirm completed stages from session close YAML before beginning work.
DATE: Established — pre-session

RULE: All timestamps must include hour and minute: YYYY-MM-DD HH:MM. No date-only timestamps.
CONDITION: All outputs, file names, YAML entries.
ACTION: Enforce without exception.
DATE: Established — pre-session

RULE: Context limit approaching → complete current stage, invoke session-consolidator, instruct user to start new chat.
CONDITION: Context approaching limit.
ACTION: Prioritise clean session close over partial additional work.
DATE: Established — pre-session

RULE: Session logs are stored at sessions/session_YYYY-MM-DD-HHMM.md — one new file per session. Legacy session_log.md is deprecated as of 2026-03-18.
CONDITION: All session start and session end operations.
ACTION: workplan-orchestrator: LIST sessions/ directory, sort descending, GET most recent file. session-consolidator: CREATE new sessions/session_{YYYY-MM-DD-HHMM}.md — never append to existing. Do not read or write session_log.md.
DATE: 2026-03-18 18:30

RULE: Updated skill files are written to skills/ directory on GitHub. When a skill has both a project file and a skills/ GitHub file, the GitHub version takes precedence.
CONDITION: Any skill updated through the 2026-03-18 audit.
ACTION: Check skills/{skill-name}_SKILL.md on GitHub first. Fall back to /mnt/project/{skill-name}_SKILL.md only if not found on GitHub.
DATE: 2026-03-18 18:30


RULE: Part V (Engineering and Coordination) is a fully authored section containing the Engineering Coordination Register (V.1) and discipline brief templates (V.2–V.5) for AC, EE, ME, and SE. The 2026-03-18 20:20 placeholder rule is superseded. Part V is no longer a stub.
CONDITION: Any edit or reference to Part V content.
ACTION: Use Part-V-MEP-Coordination-2026-03-18-rev4 as the canonical Part V content. Do not add placeholder notes. Do not treat Part V as incomplete.
DATE: 2026-03-18 18:30

RULE: Part VI (Working with Specialist Consultants) is a fully authored Volume 2 section covering OT appointment, dementia design specialists, DeafSpace consultants, sensory design specialists, and accessibility auditors. It is placed in Volume 2 after Part V (Engineering and Coordination), not in Volume 3.
CONDITION: Any structural edit, assembly pass, or cross-reference to specialist consultant guidance.
ACTION: Place Part VI immediately after Part V in Volume 2. Do not place in Volume 3. Use Part-VI-Specialist-Consultants-2026-03-18 as canonical content.
DATE: 2026-03-18 18:30

RULE: §I.8 "From Approach to Application" is the closing section of Volume 2 Part I (Synthesis and Sequencing). It follows §I.7 (Worked Examples). Cross-reference "Vol 1 §1.4a" in §I.8 is to be verified against actual §1.4 sub-section numbering before integration and corrected if needed.
CONDITION: Any assembly or integration pass touching Volume 2 Part I.
ACTION: Insert §I.8 after §I.7. Verify and correct the §1.4a cross-reference. Update Part and Section Map in front matter.
DATE: 2026-03-18 18:30

RULE: VIS/DEAF is not a valid population code. CONDITION: All documents, skills, tables, and code lists in this project. ACTION: Use VIS for vision impairment only; use DEAF for Deaf/hard of hearing; use DBL for DeafBlind. VIS/DEAF must never appear. DATE: 2026-03-18 19:00

RULE: references/toc.md on GitHub is the canonical structural record of the Guidebook (volumes, parts, sections, items, codes, labels).
CONDITION: Any structural or nomenclature change to the Guidebook — removing, renaming, recoding, moving, or adding any volume, part, section, or item.
ACTION: Use toc-editor skill. toc-editor updates toc.md and generates a Change Order (references/change-orders/CO-NNNN-*.md). find-and-replace and cross-reference-resolver execute against the guidebook source using the Change Order. Never make structural changes to the guidebook without a corresponding toc.md update and Change Order.
DATE: 2026-03-18 19:00

RULE: Change Orders are stored at references/change-orders/CO-{NNNN}-{YYYY-MM-DD-HHMM}.md and are the authoritative record of structural changes to the Guidebook.
CONDITION: All structural edits executed by find-and-replace or cross-reference-resolver.
ACTION: Locate and read the relevant Change Order before executing. Mark Sign-off checkboxes as tasks complete.
DATE: 2026-03-18 19:00

RULE: Guidebook volumes use Roman numerals (I, II, III). Parts are numbered sequentially 1–13 across all volumes. Sections use §[part].[section].[subsection] format. Item Specification Library (Part 8) category codes (A–I) and item codes (A-01 etc.) are exempt — they do not change with part renumbering. Cross-volume item code prefix is V2-P8-xx (formerly V2-P4-xx).
CONDITION: Any document, skill, table, or specification in this project referencing volume, part, section, or item codes.
ACTION: Use Roman numeral volumes, Arabic part numbers 1–13, §x.x.x section codes. Never use Roman numeral part labels (Part I, Part II etc.) or lettered parts (Part E). Part 8 item codes use category letter prefix only (A-01, not §8.A-01).
DATE: 2026-03-18 19:00

RULE: Category J (Bariatric Provisions) does not exist in Volume II Part 8. All bariatric provisions are in Supplementary Volume Supp. Part 4. The V2-P8-J prefix is invalid.
CONDITION: Any skill, specification, cross-reference, or item code lookup in Volume II.
ACTION: Route all bariatric/BAR item references to Supplementary Volume §4.x. Flag any V2-P8-J or Category J reference in Volume II as an error.
DATE: 2026-03-18 19:00

RULE: BIO and TC items are in Appendices B and C respectively, not in Part 8.
CONDITION: Any cross-reference to BIO-01–BIO-05 or TC-01–TC-05.
ACTION: Cite as Appendix B (BIO items) or Appendix C (TC items). Do not reference Part 8 or Part IV for these items.
DATE: 2026-03-18 19:00

RULE: Supplementary Volume uses Supp. Part 1–4 with §1.x–§4.x section coding, independent of main guidebook numbering.
CONDITION: Any cross-reference to the Supplementary Volume from the main guidebook or skills.
ACTION: Use "Supp. Part [n] §[n.x]" form. Do not use "Section I", "Section II" etc. for the Supplementary Volume.
DATE: 2026-03-18 19:00


RULE: GitHub skills/ directory is inventory only. Skills in skills/ on GitHub are never read or executed — they exist solely as a human-readable record of what skills are registered in the project. Canonical execution source is always /mnt/project/{skill}_SKILL.md. Reading skills from GitHub adds unnecessary token overhead and is forbidden.
CONDITION: Any skill invocation or skill file access.
ACTION: Always read and execute skills from /mnt/project/. Write updated skill content to both /mnt/project/ (canonical) and skills/ on GitHub (inventory copy). Never fetch from GitHub skills/ at runtime.
DATE: 2026-03-18 22:15


RULE: SUPERSEDED — the rule dated 2026-03-18 18:30 stating "Updated skill files are written to skills/ directory on GitHub. When a skill has both a project file and a skills/ GitHub file, the GitHub version takes precedence." is superseded by the inventory rule dated 2026-03-18 22:15. GitHub skills/ is inventory only and is never read at runtime. /mnt/project/ is always canonical.
CONDITION: Any skill invocation.
ACTION: Ignore the superseded precedence rule. Always execute from /mnt/project/.
DATE: 2026-03-18 22:25


RULE: §1.5 of Volume 1 is the canonical evidence hierarchy for this project. The tier ordering is: Tier 1 = OT clinical research; Co-primary Tier 1 = lived experience and participatory design research (CRPD Art. 4.3); Tier 2 = NGO/advocacy organisation guidelines; Tier 3 = systematic reviews and meta-analyses; Tier 4 = international standards with evidence basis; Tier 5 = jurisdiction-specific regulatory documents and grey literature. This ordering supersedes any generic clinical research pyramid (RCT > cohort > consensus) used in prior skill versions.
CONDITION: Any skill, document, or instruction that references an evidence tier or ranks source types.
ACTION: Apply §1.5 hierarchy. Lived experience is co-primary at Tier 1, not subordinate. NGO guidelines outrank systematic reviews. OT clinical evidence is highest authority.
DATE: 2026-03-18 22:35


RULE: Native-language concept vocabulary must be loaded before any multilingual-research run.
CONDITION: Any multilingual-research run, Step 0.
ACTION: Call keyword-lookup with slug + population codes + all 14 language codes. Use returned native terms as primary search strings. Do not substitute English translations. Where a native concept has no English equivalent (e.g., DE Barrierefreiheit, NO universell utforming, FI esteettomyys/saavutettavuus distinction), preserve the native concept in synthesis output; never flatten to English.
DATE: 2026-03-18 23:00

RULE: Co-1 / Tier 2 disability-led organisation pass must precede all academic database searches.
CONDITION: Any multilingual-research run, Pass A.
ACTION: For each language, search the relevant disability-led organisation publications (national Deaf associations, DPOs, patient-led research collectives, community design guides) before PubMed, Consensus, Scholar Gateway, or any other academic database. The clinical pyramid is not the default search order for this project.
DATE: 2026-03-18 23:00

RULE: Forward and backward citation mining is mandatory for every confirmed Tier 1-2 source.
CONDITION: Any confirmed Tier 1 or Co-1 or Tier 2 source retrieved during a multilingual-research run.
ACTION: Run backward pass (mine source reference list) and forward pass (Google Scholar cited-by, assess top 10). Log counts in BPC entry citation_mining fields. This is PRISMA standard methodology and is never optional.
DATE: 2026-03-18 23:00

RULE: Ireland (IE) and Singapore (SG) are standing jurisdictions in all multilingual-research runs.
CONDITION: Any multilingual-research run, Passes A-D.
ACTION: Always include IE (CEUD Building for Everyone series, NDA, Building Regulations Part M:2010, DeafHear IE, NCBI) and SG (BCA Accessibility Code 2019, SgEnable, SADeaf, SAVH, UD Mark) in every research run. Do not treat these as optional extended-language jurisdictions. They are required in Pass A (Co-1/Tier 2) and Pass B (native standards) on every run.
DATE: 2026-03-18 23:00

RULE: The early-close gate is permanently removed from multilingual-research.
CONDITION: Any multilingual-research run.
ACTION: All 14 languages must be searched to completion on every run. Extended languages (NL, ES, PT, KO, IT) are standard, not optional. The early-close gate produced Anglophone-heavy closures. Remove any reference to it from skill descriptions or execution plans.
DATE: 2026-03-18 23:00

RULE: keyword-lookup is a registered skill. Its canonical execution source is /mnt/project/keyword-lookup_SKILL.md.
CONDITION: Any multilingual-research run Step 0, or any task requiring native-language search term generation.
ACTION: Read and execute from /mnt/project/keyword-lookup_SKILL.md. GitHub skills/ copy is inventory only.
DATE: 2026-03-18 23:00

RULE: Slugs are infrastructure keys, not conceptual claims. Each slug entry carries native_aliases (14 languages with CLEAN/PARTIAL map quality ratings) and concept_boundary_warnings specifying where the English frame distorts and how the search should deviate.
CONDITION: Every multilingual-research run and every research-log-manager LOG call.
ACTION: Load native_aliases from slug-registry.md before generating search queries. Where a PARTIAL rating exists, apply the concept_boundary_warning deviation. BPC synthesis for that language opens with the concept boundary table — before findings.
DATE: 2026-03-19 04:08

RULE: The slug registry (references/slug-registry.md) is the canonical list of all research domains. It covers all main taxonomy population codes (MOB, VIS, DEAF, NEU, DEM, NDV, NDV/MH, PAIN, DBL, OFS, IntD, ALL) and all supplementary volume codes (CHD, LPA, EXH, BAR). All slugs carry pre-populated native_aliases and concept_boundary_warnings for all 14 languages.
CONDITION: Any new multilingual-research run.
ACTION: Check slug-registry.md first. Use the broadest domain slug that covers the research need. Do not create sub-slugs for sub-findings — surface them within the run. Add new slugs to slug-registry.md via research-log-manager only.
DATE: 2026-03-19 04:08

RULE: Best-practice synthesis is mandatory on every multilingual-research run. Synthesis is not a catalogue of findings.
CONDITION: Every multilingual-research run at synthesis stage, before research-log-manager LOG.
ACTION: For every slug, identify the most amenable, inclusive, forgiving, caring, accommodating, dignified, specific, and targeted provision the evidence supports. Record in BPC best_practice_synthesis field. If this field is empty at LOG time, session-consolidator flags BLOCKER.
DATE: 2026-03-19 04:08

RULE: PICO framing in literature-review-planner must begin with population need and functional outcome evidence — not standard values. Standard values appear at Step 2 (minimum baseline), not Step 1 (optimal evidence).
CONDITION: Any literature-review-planner run.
ACTION: Step 1 = what does best-practice evidence show is optimal? Step 2 = what do standards require as minimum? Step 3 = what is the gap? Step 4 = design synthesis. Never anchor on a standard value and seek confirming evidence.
DATE: 2026-03-19 04:08

RULE: research-log-manager schema carries five new Option 2 fields: native_aliases, concept_boundary_warnings, co1_pass_summary, native_standards_pass_summary, companion_networks, citation_mining, at_database_pass. All must be populated on every LOG call.
CONDITION: Every research-log-manager LOG call.
ACTION: Populate all Option 2 fields. Empty native_aliases or missing concept_boundary_warnings at LOG time = BLOCKER. DATE: 2026-03-19 04:08

RULE: Slugs in search-log.md, best-practices-compendium.md, and slug-registry.md must not include population code abbreviations as pipe-delimited suffixes (e.g. |MOB, |VIS, |ALL). Slugs are topic-only, human-readable strings. Population scope is recorded in the query field and BPC content — not the slug key.
CONDITION: Any new or updated search-log or BPC entry.
ACTION: Normalise slug to topic-only format before LOG. Strip any pipe-delimited suffix on CHECK.
DATE: 2026-03-18 23:30

RULE: Each slug covers exactly one population. Combined slugs (e.g. a slug covering both VIS and DEAF) are not permitted. Where research was conducted in a single pass covering multiple populations, the primary slug holds the full content; secondary population slugs hold a see-also pointer referencing the primary slug.
CONDITION: Any new slug creation or split of an existing combined slug.
ACTION: Create one slug per population. If primary/secondary distinction applies, secondary slug entry contains 'SEE-ALSO: {primary-slug}' only.
DATE: 2026-03-18 23:30

RULE: OT professional body guidelines are Tier 3
CONDITION: Any source is an OT professional body publication — including but not limited to CAOT, AOTA, RCOT, COTEC, WFOT, DVE, AITO, Ergoterapeutene, FSA, OT Australia, and national equivalents — whether a practice document, position statement, practice guideline, or professional framework.
ACTION: Assign Tier 3 in evidence hierarchy. Update §1.5 primary sources list. Add [Tier 3 — D-18] notation in bibliography Section D. Do not list OT body guidelines in Tier 1 primary sources (Tier 1 is reserved for intervention-tested peer-reviewed OT clinical research). Do not list OT body guidelines in Tier 5 (Tier 5 is for national beyond-code regulatory frameworks).
DATE: 2026-03-19 DECISION: D-18

RULE: Evidence hierarchy is seven tiers (Option A, D-18 extension). Tier 1 = OT intervention-tested clinical research; Co-1 = lived experience / participatory design (CRPD Art. 4.3, co-primary with Tier 1); Tier 2 = NGO/DPO/advocacy guidelines; Co-2 = OT professional body clinical practice guidelines (CAOT, AOTA, RCOT, COTEC, WFOT, and national equivalents); Tier 3 = systematic reviews and meta-analyses; Tier 4 = international standards with evidence basis; Tier 5 = national beyond-code frameworks; Tier 6 = statutory codes (reference baseline only).
CONDITION: Any source classification, evidence tier marker, or skill that embeds a tier table.
ACTION: Apply seven-tier hierarchy. Use [Tier 3 — CPG] marker for OT CPGs. Renumber all existing [Tier 3]→[Tier 4], [Tier 4]→[Tier 5], [Tier 5]→[Tier 6], [Tier 6]→[Tier 7] in guidebook body (deferred — see gap_register.md GAP for tier-marker renumber pass). Supersedes prior D-18 rule and §1.5 hierarchy rule dated 2026-03-18 22:35.
DATE: 2026-03-19 19:00

RULE: The canonical jurisdiction list for all multilingual-research runs is 24 jurisdictions, as defined in the jurisdiction-tracker skill (§4.7.3). Jurisdictions: Germany · Belgium · Norway · France · Brazil · Japan · Canada · Switzerland · Australia · UK · USA · EU · ISO · Singapore · Sweden · Denmark · Finland · China · Ireland · New Zealand · South Korea · Spain · Netherlands · Italy. This supersedes the prior 17-jurisdiction list. Ireland (IE), New Zealand (NZ), Switzerland (CH), Finland (FI), and Italy (IT) are additions.
CONDITION: Any multilingual-research run, any research-log-manager LOG call, any gap_register entry citing jurisdiction coverage.
ACTION: All 24 jurisdictions must appear in the search-log entry for a slug with a recorded status: SEARCHED · THIN · NO-DATA · NOT-RUN. A LOG entry missing any of the 24 jurisdictions is incomplete and must not be marked COMPLETE. research-log-manager LOG must refuse to write a COMPLETE status if any jurisdiction has no recorded status.
DATE: 2026-03-19 19:28

RULE: Language coverage and jurisdiction coverage are distinct axes. Both must be satisfied independently. A language pass does not substitute for a jurisdiction pass.
CONDITION: Any multilingual-research run planning or LOG evaluation.
ACTION: EN covers: USA, UK, Canada, Australia, Ireland, New Zealand, Singapore (primary); EU and ISO (as standards bodies). Each of these must be tracked as a separate jurisdiction entry in the search-log, not collapsed into a single EN pass. ZH covers: China. JA covers: Japan. KO covers: South Korea. FR covers: France, Belgium (FR-region), Switzerland (FR-region). DE covers: Germany, Switzerland (DE-region), Austria (if in scope). NL covers: Netherlands, Belgium (NL-region). PT covers: Brazil (primary), Portugal. IT covers: Italy. SV covers: Sweden. NO covers: Norway. DA covers: Denmark. FI covers: Finland. Where a single-language pass covers multiple jurisdictions, each jurisdiction must be recorded separately with its own tier coverage status.
DATE: 2026-03-19 19:28

RULE: Each jurisdiction requires a tier coverage record. The LOG gate enforces this.
CONDITION: Every research-log-manager LOG call.
ACTION: The search-log entry must include a jurisdiction_coverage block (see schema below). For each of the 24 jurisdictions, record: status (SEARCHED · THIN · NO-DATA · NOT-RUN), co1_attempted (true/false), tier5_attempted (true/false), tier6_attempted (true/false). A LOG call is a BLOCKER if: (a) any jurisdiction is absent from the block; (b) co1_attempted is false for more than 12 of 24 jurisdictions; (c) tier5_attempted is false for more than 16 of 24 jurisdictions. These thresholds are minimums — full coverage is the target.
DATE: 2026-03-19 19:28

RULE: The pre-LOG completeness check is mandatory and non-skippable. research-log-manager LOG executes this check before writing any entry.
CONDITION: Every research-log-manager LOG call, without exception.
ACTION: Before writing to GitHub, research-log-manager LOG must verify: (1) all 24 jurisdictions present in jurisdiction_coverage block; (2) co1_pass_summary lists at least one language as complete; (3) best_practice_synthesis field is populated (non-empty); (4) citation_mining backward and forward counts are recorded (may be 0 if no Tier 1/2 sources found, but the field must be present and explained); (5) native_aliases populated for all 14 languages. If any check fails: do not write; surface as named BLOCKER with the specific field missing. The user must resolve or explicitly accept the gap before LOG proceeds.
DATE: 2026-03-19 19:28

RULE: A slug BPC entry is PROVISIONAL until all 24 jurisdictions have a recorded status and co1_pass is complete for at least 9 of 14 languages. PROVISIONAL entries must carry a warning header and must not be used as the sole basis for specification writing.
CONDITION: Any BPC entry written before full coverage is achieved; any item-specification-writer run that draws on a BPC entry.
ACTION: Write the PROVISIONAL warning header on the BPC entry at LOG time if coverage thresholds are not met. item-specification-writer must check for PROVISIONAL status before using a BPC entry. If PROVISIONAL: note the gaps in the specification draft and flag [BPC PROVISIONAL — jurisdiction/tier gaps; see gap_register].
DATE: 2026-03-19 19:28

RULE: Search-log entries must include a jurisdiction_coverage block with the following schema. This supersedes the prior language-only schema.
CONDITION: Every new or updated search-log entry.
ACTION: Add jurisdiction_coverage block after the languages block:

jurisdiction_coverage:
  DE: {status: SEARCHED|THIN|NO-DATA|NOT-RUN, co1_attempted: true|false, tier5_attempted: true|false, tier6_attempted: true|false}
  BE: {status: ..., co1_attempted: ..., tier5_attempted: ..., tier6_attempted: ...}
  NO: {status: ..., ...}
  FR: {status: ..., ...}
  BR: {status: ..., ...}
  JA: {status: ..., ...}
  CA: {status: ..., ...}
  CH: {status: ..., ...}
  AU: {status: ..., ...}
  UK: {status: ..., ...}
  US: {status: ..., ...}
  EU: {status: ..., ...}
  ISO: {status: ..., ...}
  SG: {status: ..., ...}
  SE: {status: ..., ...}
  DK: {status: ..., ...}
  FI: {status: ..., ...}
  CN: {status: ..., ...}
  IE: {status: ..., ...}
  NZ: {status: ..., ...}
  KR: {status: ..., ...}
  ES: {status: ..., ...}
  NL: {status: ..., ...}
  IT: {status: ..., ...}

jurisdiction_coverage_summary:
  searched: []
  thin: []
  no_data: []
  not_run: []
  co1_complete: []
  co1_not_attempted: []
  tier5_complete: []
  tier5_not_attempted: []

DATE: 2026-03-19 19:28
RULE: 1524mm ADA turning circle is not a permitted specification floor in this guidebook. It is based on 1970s anthropometric data and is rejected as a design baseline.
CONDITION: Any MOB turning space specification, any item referencing ADA 1524mm.
ACTION: The minimum permitted floor is 1700mm (RHFAC/BS8300 best practice). ADA 1524mm may be cited as a historical data point or evidence of regulatory lag only. It must never appear as a design value or minimum threshold in any item specification, BPC synthesis, or guidance text.
DATE: 2026-03-19 22:45

RULE: At session end, log each completed workplan reference code to the session YAML as a completed_items list entry with -DONE suffix.
CONDITION: Any session where a named workplan item (e.g. WS-1 Pre-session, BPC-1, P11 item N) is fully executed.
ACTION: List item as "{code}-DONE" in session YAML completed_items block. This is the canonical completion record — workplan files on GitHub are updated where they exist; /mnt/project/ workplan files are read-only and cannot be edited.
DATE: 2026-03-19 20:00


RULE: v10.0 Part Renumbering. Old Part 8 (Conflict Resolutions) absorbed into Part 4. Old Part 9 → Part 8. Old Part 10 → Part 9. Old Part 11 → Part 10. Old Part 12 → Part 11. Old Part 13 → Part 12. Section numbering follows Part number: Part N uses §N.x.
CONDITION: All documents, cross-references, skill triggers, and workplan references from v10.0 onward.
ACTION: Apply new Part numbering. Update all §-references. See workplan/v10-0-comprehensive.md §0.1 for full map.
DATE: 2026-03-20 21:00

RULE: No BAR in Volume I. Large body size provisions belong exclusively in the Supplementary Volume. BAR is not mentioned, referenced, or cross-referenced anywhere in Volume I (Parts 1–3).
CONDITION: All Volume I content in v10.0 and subsequent.
ACTION: Delete any BAR mention, redirect, or footnote in Parts 1–3. BAR row/column removed from co-occurrence matrix.
DATE: 2026-03-20 21:00

RULE: Evidence specification markers. ● (filled circle) = evidence-based specification (Tier 1–6 evidence exists). ○ (empty circle) = inferred from clinical reasoning or expert consensus (evidence gap disclosed). The distinction is noted at the beginning of each volume.
CONDITION: All prescriptive specifications in Parts 2, 5, 6, 7, and Appendices B/C.
ACTION: Every specification sentence carries either ● or ○. Unmarked specifications are errors.
DATE: 2026-03-20 21:00

RULE: Tier defaults for building types. Public building with unknown population = Tier 0. Public building with identified disabled populations = Tier 1. Residential home = Tier 2 (every person lives somewhere; every residence should tailor itself to the people who live there).
CONDITION: §1.4.3, §4.8, and any tier-assignment guidance.
ACTION: Apply residential = Tier 2 default throughout. Residential matrices operate at Tier 2 assumption unless stated otherwise.
DATE: 2026-03-20 21:00

RULE: Part 2 disability categories sorted alphabetically by code.
CONDITION: Part 2 in v10.0 and subsequent.
ACTION: Order: DBL, DEAF, DEM, IntD, MOB, NDV, NDV/MH, NEU, OFS, PAIN, UPL, VIS. Renumber §2.1–§2.12 accordingly.
DATE: 2026-03-20 21:00

RULE: CRPD Articles 3, 4.3, and 9 quoted in full in §1.7.
CONDITION: Part 1 §1.7 CRPD Framework Alignment in v10.0 and subsequent.
ACTION: Insert quoted blocks of CRPD Article 3 (General Principles), Article 4.3 (participation clause), and Article 9 (Accessibility).
DATE: 2026-03-20 21:00

RULE: All Part 7 items are designed to be accompanied by a technical diagram, drawing, or illustration. Where illustrations are not yet provided, add "[Illustration: to be provided]" note.
CONDITION: All Part 7 item specifications including Appendix B and C items.
ACTION: Add illustration note to each item. Remove note only when illustration is provided.
DATE: 2026-03-20 21:00

RULE: Each Part produces its own .md file. Each Item Specification Library Category produces its own .md file. Master document is assembled from parts.
CONDITION: v10.0 file architecture.
ACTION: Files stored at parts/v10/{filename}.md on GitHub. Assembly via chunk-assembler.
DATE: 2026-03-20 21:00

RULE: IntD (Intellectual Disability) is not a standalone population code or category. IntD provisions are proxied through DEM (wayfinding, cognitive simplicity) and NDV (sensory environment, Easy Read signage). No §2.12, no IntD matrix column, no IntD population code table entry.
CONDITION: All volumes, all matrices, population code tables, ToC.
ACTION: Delete any standalone IntD reference. Preserve substance as proxy notes within DEM and NDV sections. See CO-0002-2026-03-25-1935.md.
DATE: 2026-03-25 19:35
RULE: The guidebook is a starting framework for professional judgment, not a substitute for it. Population-level specifications (Tier 0 and Tier 1) are necessary but insufficient. Individual function is unique — even within the same disability population, two individuals' functional capacities and required accommodations may differ radically. The guidebook cannot solve accessible design through catch-all procedures for single or multiple disability populations. Part 1 must state this explicitly as a foundational principle.
CONDITION: Part 1 foundational principles (§1.2 or equivalent); any section that could be read as implying population-level specs are complete solutions.
ACTION: Include explicit framing statement in Part 1. Audit prescriptive language throughout to ensure it does not imply sufficiency without Tier 2 co-design.
DATE: 2026-03-26 16:00

RULE: The guidebook's conflict resolution protocol (§IV.2 and cross-synthesis escalation) operates at Tier 1 only. At Tier 2, conflict resolution is the domain of the OT and the individual through co-design — the guidebook has no authority to prescribe person-specific outcomes. The guidebook's Tier 2 role is to equip non-OT professionals (architects, builders, project managers) with decision frameworks, the right questions, and structured approaches for co-design — not to prescribe answers.
CONDITION: §IV.2 conflict priority rules; any Tier 2 guidance; any cross-synthesis or conflict resolution text.
ACTION: State explicitly that §IV.2 governs Tier 1 only. Tier 2 conflict resolution sections provide frameworks and questions for co-design, not prescriptive outcomes.
DATE: 2026-03-26 16:00
RULE: Bottom-up functional deficit research is a standing complementary methodology. The skill `functional-deficit-researcher` searches OT intervention literature by ICF activity code + functional constraint + environment context, then categorizes findings into the guidebook's population framework. It runs after `multilingual-research` top-down pass is COMPLETE for target slugs. Findings classified as NOVEL or REFINES feed to `item-specification-writer`. Findings serving ≥3 population codes are flagged as TIER-0-CANDIDATE for potential universal design migration. Search-log entries carry a `functional_deficit_pass` block; BPC entries carry a `### Bottom-up findings` subsection.
CONDITION: Any slug with ≥2 THIN flags, any item-specification-writer evidence gap, any connection-scout cross-population gap unresolved by top-down search, or explicit user request.
ACTION: Run `functional-deficit-researcher` on the relevant environment context batch. ≤12 scenarios per session. Results merge into existing BPC.
DATE: 2026-03-26 16:15

RULE: Session Start Protocol runs once per conversation. If it has already completed in the current conversation, "resume," "continue," or equivalent directives do not re-trigger it.
CONDITION: Any message containing "resume," "continue," "carry on," "pick up where we left off," or equivalent in a conversation where Session Start Protocol has already run.
ACTION: Skip Session Start Protocol; proceed directly to the referenced task.
DATE: 2026-03-26 18:30

RULE: All working documents must be committed to GitHub before session close. No work product may exist only in /mnt/user-data/outputs/ at session end — that directory does not persist across sessions.
CONDITION: Any session that produces working documents, research outputs, backfill logs, draft specifications, or intermediate analysis files.
ACTION: Before session-consolidator runs, commit all working documents to `research/` or `misc/` on GitHub. Filename convention: `{task-descriptor}_{YYYY-MM-DD-HHMM}.md`. session-consolidator must verify no uncommitted working documents remain.
DATE: 2026-03-26 21:00

RULE: research-log-manager uses per-slug topic-directory architecture. Flat files `references/search-log.md` and `references/best-practices-compendium.md` are retired frozen archives — do not read or write.
CONDITION: Every research-log-manager CHECK, LOG, or RETRIEVE operation.
ACTION: Resolve slug to file path via `references/slug-registry.md`. Search log file at `references/search-log/{topic}/{slug}.md`. BPC file at `references/bpc/{topic}/{slug}.md`. For new slugs: assign topic dir, create both files, update slug-registry.md. Topic directories: entrances-and-circulation, health-and-symptom-management, bathrooms-and-wet-areas, kitchens-and-workspaces, wayfinding-and-signage, seating-and-rest, sensory-environment, communication-and-alerts.
DATE: 2026-03-26 16:30

RULE: Standards registry entries for SG (BCA 2025), NL (NEN 9120:2025), SE (BFS 2024:12) are SUPERSEDED relative to previously cited versions.
CONDITION: Any multilingual-research, jurisdiction-tracker, or item-specification-writer run referencing SG, NL, or SE statutory standards.
ACTION: Cite BCA Accessibility Code 2025 (SG), NEN 9120:2025 (NL), BFS 2024:12 / ALM 2 (SE) as current. Flag any guidebook text citing prior editions as requiring update.
DATE: 2026-03-26 16:30

RULE: Skills not in /mnt/project/ must be read from GitHub skills/{name}_SKILL.md via GET before execution. Currently affected: bulk-renumber, citation-miner, sensory-coherence-checker, connection-scout.
CONDITION: Any session requiring execution of a skill whose _SKILL.md file is absent from /mnt/project/.
ACTION: GET the skill file from GitHub before execution. PI definition governs for PI-governed skills.
DATE: 2026-03-26 19:15

RULE: keyword-lookup is DEPRECATED. Functionality subsumed by multilingual-research Rule 16 (view Keyword Compendium Part 3 directly).
CONDITION: Any reference to keyword-lookup or native-language keyword lookup.
ACTION: Use multilingual-research Rule 16 protocol instead. Do not invoke keyword-lookup.
DATE: 2026-03-26 19:15

RULE: Evidence Priority and Source Propagation. (a) When any writing or specification skill receives both curated BPC content and raw search/session outputs, the BPC best_practice_synthesis field governs as the primary evidence basis. Raw search results may supplement but never override BPC synthesis. If raw results contradict BPC synthesis, flag as CONTRADICTION and route to evidence-auditor — do not silently prefer the raw result. (b) Every source cited in a specification, practice note, or guidebook section must propagate to: (i) an in-text superscript endnote marker, and (ii) a corresponding entry in the volume-end endnote list. item-specification-writer outputs a sources-cited block per item using REF-ID markers. bibliography-compiler collects, deduplicates, assigns sequential endnote numbers per volume, replaces REF-ID markers with superscripts, and generates the endnote list. No source may appear in text without an endnote entry; no endnote entry may exist without an in-text citation.
CONDITION: All writing, specification, and assembly workflows. All item-specification-writer, chunk-assembler, and bibliography-compiler runs.
ACTION: (a) Prefer BPC synthesis; flag contradictions. (b) item-specification-writer emits REF-ID markers and sources-cited blocks. bibliography-compiler runs at assembly to compile volume-end endnotes. Endnote numbering resets at each volume boundary. Endnote list ordered by first appearance in text.
DATE: 2026-03-27 14:00
