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
