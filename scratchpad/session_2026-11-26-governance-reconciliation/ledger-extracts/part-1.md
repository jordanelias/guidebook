# project-standards.md — current-state extract, part 1 (source lines 1–1145)

Conventions: "Owner words" are verbatim quotations the ledger marks as the owner's. Everything else is the recorder's text reduced to what binds. Dates are ranking keys. Tags: [unratified reading], [OPEN], [CHECK], [STATUS UNCERTAIN: ...].

---

## Core Doctrine (locked)

### 2026-04-24 — Purpose: get people to ask the right questions [L8-L9]
Owner words: none quoted — recorder entry, not owner words.
In force:
- THE PURPOSE OF THIS GUIDEBOOK IS TO GET PEOPLE TO ASK THE RIGHT QUESTIONS; foundational principle governing all other rules.
- Not a prescription manual, not an authority on measurements; does not dictate values designers, policymakers or practitioners must apply. A thinking tool for asking the right questions depending on circumstance.
- Measurements, ranges and reference data serve the questions, not the reverse.
- Every item specification, BPC synthesis and piece of prose is evaluated against: does it help the reader ask better questions about this design element; surface considerations they would not otherwise meet; make them think more critically about their situation.
- Aim: raise the floor of understanding for everyone who touches the built environment.
Open: none.

### 2026-04-24 — Disability populations are not uniform [L11-L12]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Every person within a population code has a unique experience and unique functional limitations; there is no generic ideal for any population.
- Specifications provide ranges and starting points, not definitive answers.
- Co-occurring conditions are the norm; every item specification acknowledges functional variability within the population and discusses how co-occurrence affects the design parameter.
- Population codes are a high-level organising principle: Universal Mode — comprehensive; Population Mode — insight for a known population; Person Mode — they step aside (OT works bottom-up from functional impairments; everything tailored to the individual).
Open: none.
[CHECK] Later rulings outside this slice (lens columns replacing `population_code`, per CLAUDE.md §6) may bear on "population code" wording; the principle itself is not marked superseded.

### pre-session — Design Modes govern all specifications [L14-L15]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Universal Mode = Universal Design / Code Compliance (population-agnostic, fixed values).
- Population Mode = Population-Informed Inclusive Design (ranges; median as default).
- Person Mode = Person-Specific Co-Design (OT assessment resolves position within the Population-Mode range).
- DAR mandatory at all modes.
Open: none.

### 2026-05-25 (owner directive); 2026-07-13 (ratification) — Evidence hierarchy: seven tiers [L17-L18]
Owner words: "t2>t3 this is enshrined"
In force:
- Seven tiers per `governance/tier-system.md` (operative).
- Tier 1 = primary research with intervention-level or biomechanical control (OT-prioritised, not OT-exclusive).
- Co-1 = lived experience / participatory design (CRPD Art. 4.3), co-primary with Tier 1.
- Tier 2 = synthesis: (a) systematic reviews / meta-analyses AND (b) named-organisation evidence-based standards.
- Co-2 = OT professional body CPGs, co-primary with Tier 2.
- Tier 3 = lower-control primary clinical research + grey-literature primary research; supporting, rarely sole basis; T3-alone never reaches `stated`.
- Tiers 4–6 = regulatory stratum (international standards, national frameworks, statutory codes): walled off from best-practice anchoring; convergence-not-evidence.
- The evidence hierarchy determines best practice; where higher-tier evidence exists, it governs.
Open: none.

### 2026-04-24 (amended 2026-07-21, owner directive, Option A) — Best practice defined by evidence, not code consensus [L20-L21]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Best practice = the most accommodating, thoughtful, respectful, dignified and usable condition achievable for the disabled person.
- Determined by the evidence hierarchy (T1, Co-1, T2 SR/MA + named-organisation evidence-based standards, Co-2 OT CPGs) — not by code consensus. Codes are Tier 6: the compliance floor, not the aspiration.
- A best_practice_synthesis deriving its value solely from code consensus is a weak-band (○) claim — "best practice as currently known" — valid only when flagged code-derived with the convergence-not-evidence caveat; never rendered unflagged or above the weak band. An unflagged or full-strength code-consensus best-practice claim is in error (`decisions/DR-2026-07-21-evidence-architecture-option-a-execution.md`).
- Test: does the specification provide the most accommodating, dignified, usable condition the evidence supports, or merely reflect what codes agree on?
Open: none.

### pre-session — Universal design = code compliance floor [L23-L24]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Universal design is co-extensive with code compliance — the floor, not an aspiration. Inclusive design is the positive aspiration.
Open: none.

### 2026-07-13 — Evidence specification markers ●/◐/○ [L26-L27]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Per `governance/tier-system.md` §5: ● = confirmed evidence base (T1, T2 both streams, T3-clinical, Co-1, Co-2); ◐ = policy/standards basis only (T4, T5); ○ = grey, expert consensus, thin base, unconfirmed (T3-grey, [EXPERT CONSENSUS], [THIN BASE], T6).
- A T4–6-only basis never renders best-practice language in any register (G1b, invariant I3).
- Every specification sentence carries a marker; for quantitative specifications ● also requires value-level support, not only direction. Unmarked = error.
Open: none.

### pre-session — BAR not a main taxonomy code [L29-L30]: nothing in force (superseded within this slice by the 2026-07-24 population-scheme reconciliation, L573-L579: LPA/TALL/BAR are retained codes). [CHECK] The 2026-07-24 entry names the "BAR is not a main taxonomy code / Large body size is not a disability / Delete on sight" clauses as superseded; it does not separately mention "Category J (J-01–J-05) is struck from Volume II Part 4" or the "Supp. Part 4 only" containment.

### pre-session — Specification ranges are not uncertainty [L32-L33]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Ranges are the designed-in bridge between Population Mode and Person Mode. Population Mode: median. Person Mode: resolve through co-design.
- Never write a range without specifying which end applies at which mode.
Open: none.

### pre-session (reconciled 2026-07-13) — Co-1 co-primary with Tier 1 [L35-L36]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Lived experience evidence (Co-1) is co-primary with Tier 1 on the claim types it anchors (preference, dignity, autonomy, self-determined accommodation) — unconditionally, not merely where no clinical trial is feasible.
Open: none.

### pre-session — VIS, DEAF, DBL distinct codes [L38-L40]
Owner words: none quoted — recorder entry, not owner words.
In force:
- VIS, DEAF, DBL are three distinct independent population codes. VIS/DEAF as a compound code is an error. DBL ≠ VIS + DEAF.
- The full canonical code list is the `base_taxonomy_identity` table.
Open: none.
[STATUS UNCERTAIN: entry carries "AMENDED 2026-11-06: the full canonical list is the `base_taxonomy_identity` table; the skill section this rule pointed to is retired" — amendment originates outside this slice ("Owner instruction 2026-11-06 — retire workplan-orchestrator; /run-pipeline replaces it").]
[CHECK] The 2026-07-24 flat 23-code set (L573) names these communities BLIND, DEAF, DEAFBLIND, not VIS/DBL; the distinctness principle is not stated as superseded.

### 2026-03-25 — IntD not a standalone code [L42-L43]: nothing in force (superseded within this slice by the 2026-07-24 population-scheme reconciliation, L573-L579: ID is first-class; do not proxy). [CHECK] The THIN-BASE disclosure clause for IntD specifications is not separately addressed by the superseding entry.

### 2026-03-18 — Biophilic Design and Thermal Comfort in Appendices B and C [L45-L46]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Biophilic Design (BIO-01–BIO-05) in Appendix B; Thermal Comfort (TC-01–TC-05) in Appendix C. Supplementary Resources A and B struck from Volume II body.
- No inline BIO- or TC- cross-references in Part 4 specs or room matrices. Single opening notice permitted in volume front matter.
Open: none.
[CHECK] Refers to prior-version document structure and codes (CLAUDE.md §7 treats `[A-Z]-NN`-style codes as prior-version content).

### 2026-03-26 — Starting framework for professional judgment [L48-L49]
Owner words: none quoted — recorder entry, not owner words.
In force:
- The guidebook is a starting framework for professional judgment, not a substitute for it. Population-level specifications (Universal and Population Mode) are necessary but insufficient. Part 1 must state this explicitly as a foundational principle.
Open: none.

### 2026-03-26 — Conflict resolution operates at Population Mode only [L51-L52]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Conflict resolution protocol (Part 5 and cross-synthesis escalation) operates at Population Mode only. At Person Mode, conflict resolution is the domain of the OT and the individual through co-design.
- The guidebook's Person Mode role: equip non-OT professionals with decision frameworks and structured approaches, not prescriptive answers.
Open: none.

### 2026-04-26 — Advocacy project, not an authority [L54-L55]
Owner words: none quoted — recorder entry, not owner words.
In force:
- The guidebook is an advocacy project, not an authority. It does not teach professional judgment, confer competence, and is not a registered body, standard-setting organisation, or regulatory instrument.
- Derived from comprehensive research, presented multimodally to equip people who touch the built environment with better questions, evidence and starting points. Readers apply their own professional judgment.
- Value lies in quality/comprehensiveness of the research synthesised and accessibility of presentation — not in any claim to authority over practice. Supersedes any language elsewhere implying institutional authority or mandating power.
Open: none.

---

## Item Code System

### pre-session — Item codes: bare category prefix [L61-L62]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Item codes use bare category prefix only (A-01, B-06, etc.); no volume-part prefix. Part-independent; do not change with renumbering.
Open: none.
[CHECK] CLAUDE.md §7 states the item layer has been dropped from the database and item codes are prior-version content; this ledger entry is not marked superseded.

---

## Citation and Evidence Standards

### pre-session — All sources confirmed real [L68-L69]
Owner words: none quoted — recorder entry, not owner words.
In force:
- All sources must be confirmed real. Unverified claims → [UNVERIFIED — DOI/URL required before publication]. citation-verifier defaults to PROVISIONAL mode.
Open: none.

### 2026-03-17 — G-03 cites both Levine papers [L71-L72]
Owner words: none quoted — recorder entry, not owner words.
In force:
- G-03 cites Levine 2023 (Human Factors, doi:10.1177/00187208211059860) AND Levine 2025 (JMIR, doi:10.2196/69442). Both required. Replace any "Levine 2024" with both.
Open: none.
[CHECK] Keyed on a prior-version item code.

### 2026-03-18 — Two failed searches → delete unverifiable value [L74-L75]
Owner words: none quoted — recorder entry, not owner words.
In force:
- 2 failed independent searches → delete the unverifiable value (CLOSED-DELETED). Do not accumulate unresolvable UNVERIFIED flags.
Open: none.

### 2026-03-28 — AOTA Home Modification guidelines edition [L77-L78]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Confirmed edition: Siebert, Smallfield & Stark (2014). Verify whether a 2023 revision exists before citing as 2023.
Open:
- [OPEN] Whether a 2023 revision exists.

---

## Structural Decisions

### 2026-03-18 — toc.md is canonical structural record [L86-L87]
Owner words: none quoted — recorder entry, not owner words.
In force:
- references/toc.md is the canonical structural record. Structural changes → toc-editor → Change Order → find-and-replace + cross-reference-resolver.
Open: none.

---

## CO-0003 + CO-0004 Structural Rules (section marked "TRANSITIONAL — remove after CO-0004 propagation pass is complete")

### 2026-03-29 (signed off 2026-03-30) — CO-0004 Volume merge and Part renumbering [L94-L96]
Owner words: none quoted — recorder entry, not owner words.
In force:
- 2 Volumes: Volume I (Parts 1–9), Volume II (Parts 10–12). Appendices, Bibliography and Glossary follow Volume II but are not part of it. Supplementary unchanged.
- CO-0004 supersedes CO-0003 structural provisions; CO-0003 terminology changes remain in full effect.
- Part Map: `workplan/P1-D2-D3-co0004-remapping.md`.
Open: none.
[STATUS UNCERTAIN: entry carries "AMENDED 2026-11-06: the Part Map this rule pointed to survives at workplan/P1-D2-D3-co0004-remapping.md; the skill section is retired" — amendment originates outside this slice.]
[CHECK] Section header marks these rules TRANSITIONAL pending the CO-0004 propagation pass; completion status not stated.

### 2026-03-28 — "Cross-population" retired [L98-L99]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Use "co-occurring disability" (intra-individual) or "multi-population" (inter-group).
- Notation: `+` = co-occurring in one person; `/` = different people, same space.
Open: none.

### 2026-03-29 — Part 5 owns building-wide conflicts [L101-L102]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Part 5 (Building-Level Co-Occurrence Resolution) owns building-wide system conflicts. Room-level conflicts → Parts 6/7 inline annotations. Methodology → Part 3 §3.8–§3.9. Items → Part 4. Engineering → Part 8. Consultants → Part 9.
Open: none.

### 2026-03-29 — Parts 6/7 inline conflict notes format [L104-L105]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Format: "Conflict note — [code]: Items [X-NN] and [Y-NN] conflict for [POP+POP]: [description]. Resolution: Part 3 §3.9.N. See Part 5 if building-wide."
Open: none.

### 2026-03-29 — Part 9 §9.9/§9.10 co-occurrence protocol [L107-L108]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Part 9 §9.9 and §9.10 contain the co-occurrence collaboration protocol and OT appointment threshold. Route there, not Part 5.
Open: none.

### 2026-03-28 — Slug names are frozen path identifiers [L110-L111]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Slug names are frozen path identifiers, never renamed by CO-0003. Content adopts new terminology; paths unchanged.
Open: none.

### 2026-03-28 — Part 7 conflict entry tags [L113-L114]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Part 7 conflict entries tagged [INTRA-INDIVIDUAL], [INTER-GROUP] or [BOTH]. Intra → Person Mode OT resolution. Inter → Universal/Population Mode architectural. Both → state both pathways.
Open: none.

---

## Research and Evidence Pipeline

### 2026-03-18 — One slug, one population [L120-L121]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Each slug covers exactly one population. Combined slugs not permitted.
Open: none.
[CHECK] Bears on the 2026-08-24 full-cross-product ruling (L941), which requires every slug to be searched against every population/access need/ICF code; the two are not stated to conflict.

### 2026-03-19 — 24 jurisdictions canonical; coverage record [L123-L124]
Owner words: none quoted — recorder entry, not owner words.
In force:
- 24 jurisdictions canonical (per jurisdiction-tracker §4.7.3). Language and jurisdiction coverage are distinct axes, both satisfied independently.
- Per-jurisdiction tier coverage record required: status (SEARCHED|THIN|NO-DATA|NOT-RUN), co1_attempted, tier5_attempted, tier6_attempted.
- Pre-LOG completeness check mandatory (24 jurisdictions, co1_pass_summary, best_practice_synthesis, citation_mining, native_aliases for 14 languages) — fail = BLOCKER.
- BPC entry PROVISIONAL until all 24 recorded + co1_pass ≥9 languages.
Open: none.

### 2026-03-18 — Forward + backward citation mining mandatory [L126-L127]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Forward + backward citation mining mandatory for every confirmed Tier 1–2 source. Use citation-miner skill (inline = fallback only).
Open: none.

### 2026-03-18 — Early-close gate removed [L129-L130]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Early-close gate permanently removed. All 14 languages searched to completion on every run.
- Exception: IntD only — early-close active (literature confirmed absent in non-English).
Open: none.
[CHECK] The IntD exception uses the retired IntD label (ID is first-class per L573).

### 2026-03-19 — PICO framing starts with population need [L132-L133]
Owner words: none quoted — recorder entry, not owner words.
In force:
- PICO framing begins with population need and functional outcome evidence, not standard values. Standards at Step 2.
Open: none.

### 2026-03-26 — Standards registry current editions [L135-L136]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Current editions: BCA Accessibility Code 2025 (SG), NEN 9120:2025 (NL), BFS 2024:12 / ALM 2 (SE). Prior editions superseded.
Open: none.

---

## Endnote and Source Pipeline

### 2026-03-27 — Evidence priority: BPC synthesis governs [L142-L143]
Owner words: none quoted — recorder entry, not owner words.
In force:
- BPC best_practice_synthesis governs as primary evidence basis. Raw search results supplement but never override. Contradictions → evidence-auditor.
Open: none.

### 2026-03-27 — Source propagation to endnotes [L145-L146]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Every cited source → in-text [REF:{slug}:{NN}] marker → bibliography-compiler → superscript endnote + volume-end endnote list. No source without endnote; no endnote without citation.
Open: none.

### 2026-03-28 — PROVISIONAL-REF pattern [L148-L149]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Assign REF-ID positions only after BPC Key sources updated. Never emit final text with provisional positions.
Open: none.

---

## Session and Process Management

### 2026-03-27 — Flat BPC/SL files frozen [L155-L156]
Owner words: none quoted — recorder entry, not owner words.
In force:
- The 15 population-level flat BPC/SL files are frozen archives. New research creates per-slug directory entries.
Open: none.

---

## Functional Deficit Research

### 2026-03-27 — FDR CONTRADICTS resolution [L162-L163]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Do not delete the original BPC claim. Append [CONTRADICTED BY FDR]. Route to evidence-auditor for adjudication.
Open: none.

### 2026-03-28 — PubMed MeSH "dressing" conflict [L165-L166]
Owner words: none quoted — recorder entry, not owner words.
In force:
- PubMed MeSH "dressing" → "bandages" conflict. Skip PubMed Step 1 for d540/ADL/bedroom scenarios; go direct to Step 2 (OT practice guidelines).
Open: none.

---

## Specification Process Rules

### 2026-04-26 — Specification language tier-appropriate; "shall be" retired [L172-L173]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Specification language is tier-appropriate and claims no authority the project lacks.
- Universal Mode: "Code requires [value] per [standard]" (authority is the code).
- Population Mode: "[Evidence tier] evidence supports [value]" or "Best practice based on [N] jurisdictions and [tier] evidence is [value]" (authority is the evidence).
- Person Mode: "OT assessment determines position within [range] based on [functional parameter]" (authority is the OT).
- Blanket "shall be" constructions are retired. Always run prose-style-checker before vol2-item-formatter. Existing Part 4 text using "shall be" requires a voice pass.
Open: none.

### 2026-03-28 — "Adjustable" not a universal resolution [L175-L176]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Document operability per population. Flag populations who cannot self-adjust. Route to Person Mode if an ambient parameter is irreconcilable.
Open: none.

### 2026-03-28 — Conflicts searched by conflict domain [L178-L179]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Cross-population conflicts searched by CONFLICT DOMAIN (12 environmental parameter conflicts), not by population pair. Aged care POEs are the richest evidence source.
Open: none.

### 2026-03-28 — Check conflict mapper before finalising single-population specs [L181-L182]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Population-specific guideline sets do not cross-reference conflict points. Check cross-population-conflict-mapper §1 before finalising any single-population spec in shared spaces.
Open: none.

### 2026-03-28 — Universal Mode rejection test (DEAF) [L184-L185]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Provisions creating emergency communication isolation are incompatible with Universal Mode for DEAF. Check DEAF population before assigning Universal Mode to acoustic isolation specs.
Open: none.

### 2026-03-27 — STI, not NRC, is the acoustic criterion [L187-L188]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Acoustic panel NRC is not a standalone performance criterion; STI is. STI ≥ 0.60 (general) / STI ≥ 0.75 (DEAF/CI). NRC is means, not end.
Open: none.

---

## Case Studies

### 2026-03-27 — Case study deduplication [L194-L195]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Deduplication checks name variants, date variants, building vs programme level. Programme-level entries (CAPABLE, DFG, BATH-OUT) use programme-level format.
Open: none.

### 2026-03-30 — Part 4 sole specification authority [L198-L199]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Part 4 holds sole specification authority for all performance targets. Anything distinctly spatial is architectural; engineers support execution.
- Part 8 is a coordination register mapping architect-specified targets to engineering briefs — not a parallel specification. Where Part 8 restates Part 4 values, replace with cross-reference; where they contradict, Part 4 governs.
- Performance targets (RT60, STI, NC, STC, melanopic EDI, MERV, etc.) are architect specifications derived from population evidence.
Open: none.

### 2026-03-30 — Population operability note for "adjustable" specs [L201-L202]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Every Part 4 specification using "adjustable", "individual control" or "user-operated" includes a population operability note: (1) populations who can self-adjust; (2) populations requiring carer/staff operation; (3) default setting when no individual present, with harm-asymmetry rationale.
Open: none.

### 2026-03-30 — Person Mode handoff flag on ranges [L204-L205]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Every Part 4 specification with a range reflecting individual variation (not jurisdictional difference) carries: "Population Mode default: [median]. Tier 2: OT assessment resolves position within range based on [functional parameter]."
Open: none.

### 2026-03-30 — Check for variable conflation before asserting conflict [L207-L208]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Step 0 in §3.8 decision tree: verify that opposing needs operate on the same physical variable (e.g. width ≠ sensory load; LRV contrast ≠ chroma; adequate space ≠ reconfiguration).
Open: none.

### 2026-03-30 — Harm asymmetry governs divergent defaults [L210-L211]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Where no single specification serves all populations: (1) identify which population suffers greater harm from the wrong default; (2) set default to protect the higher-harm population; (3) provide individual supplemental provision for the lower-harm population.
- Examples: dim lighting default (NDV pain > DEM reduced benefit); cool temperature default (NEU/MS neurological deterioration > PAIN discomfort).
Open: none.

### 2026-03-30 — DEM olfactory wayfinding not a built-environment spec [L213-L214]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Aromatherapy is a clinical care intervention, not an architectural specification. Fragrance-free is the universal built-environment specification.
Open: none.

---

## Writing Style

### 2026-03-31 — voice-style_SKILL.md mandatory [L220-L221]
Owner words: none quoted — recorder entry, not owner words.
In force:
- skills/voice-style_SKILL.md is mandatory for all prose writing and all framing/language review; it replaces the former voice-style and framing-checker skills.
- Load before drafting, revising, reviewing or auditing guidebook prose. Apply the 11-point calibration test before finalising. For framing audits invoke §12 Framing Audit Protocol.
- Scope: all body text in Parts 0–12, supplementary volumes, appendices, front matter. Not tables, reference lists, abbreviation registers, amendment registers.
Open: none.

### 2026-03-31 — Two Part 1 structural gaps [L223-L224]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Track as open items (below).
Open:
- [OPEN] §1.2 endorsements sentence references a list that does not follow — append the 17-jurisdiction endorsement list or remove the sentence.
- [OPEN] §1.5 Co-primary Person Mode header — verify drafted content on next Part 1 review pass.

### 2026-03-31 — Never use jq [L226-L229]
Owner words: none quoted — recorder entry, not owner words.
In force:
- CONDITION: every bash_tool call that parses JSON. ACTION: use `python3 -c "import sys,json; d=json.load(sys.stdin); ..."`; never call, install or pip/apt install jq.
Open: none.

### 2026-03-31 — Session start protocol before any GitHub write [L231-L235]
Owner words: none quoted — recorder entry, not owner words.
In force:
- A session opens with /session-open then /orient (per the 2026-11-06 annotation).
Open: none.
[STATUS UNCERTAIN: entry carries "SUPERSEDED 2026-11-06: the skill this protocol runs through is retired; a session opens with /session-open then /orient" — supersession originates outside this slice. Original protocol: GraphQL batch read of LATEST + project-standards + workplan-orchestrator, then session file, then gap-register P1 filter, before any GitHub write.]

### 2026-03-31 — "Start a new conversation" reserved for context boundaries [L237-L240]
Owner words: none quoted — recorder entry, not owner words.
In force:
- CONDITION: writing next_action during session close. ACTION: omit "start a new conversation" unless (a) context is ≥85% consumed, or (b) the next task requires a materially different workflow type. Simple continuations do not qualify.
Open: none.

### 2026-03-31 — No background processes for GitHub API calls [L241-L244]
Owner words: none quoted — recorder entry, not owner words.
In force:
- CONDITION: any bash_tool call involving curl to api.github.com (REST or GraphQL). ACTION: all GitHub reads and writes sequential; no `&`.
Open: none.

### 2026-03-31 — No stale blockers in session YAML [L246-L249]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Before writing next_action blockers, verify each blocker's gap ID is still OPEN in gap_register.md; if CLOSED remove it; if no gap ID exists, create one or drop the blocker.
Open: none.

### 2026-03-31 — Do not use conversation_search for current state [L251-L254]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Never use conversation_search or project_knowledge_search for current project state. Get state from the repository (session file). conversation_search is for past conversation context only.
Open: none.
[CHECK] ACTION names the "session start protocol" whose status is uncertain (see L231-L235).

### 2026-03-31 — GraphQL batch reads for >3 BPC/SL files [L256-L259]
Owner words: none quoted — recorder entry, not owner words.
In force:
- For >3 BPC/SL file reads, batch up to 20 files per GraphQL call using aliased object() queries (github-io batch_read()).
Open: none.

### 2026-05-04 — Connection state is in SQLite [L261-L264]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Connection state is in SQLite (`connections` + `connection_targets`); query via `python3 scripts/db.py connections`. Do not load archived markdown connection files (`_index.md`, per-topic `connections.md`); they are read-only historical records.
Open: none.
[STATUS UNCERTAIN: entry is headed "[RETIRED — CO-0009]" while its body states a live SQLite rule; whether "RETIRED" applies to the rule or to the markdown files cannot be told from the text.]

### 2026-03-31 — Do not re-read workplan-orchestrator mid-session [L266-L270]
Owner words: none quoted — recorder entry, not owner words.
In force: none stated beyond the annotation (the skill no longer exists).
Open: none.
[STATUS UNCERTAIN: entry carries "SUPERSEDED 2026-11-06: the skill no longer exists" — supersession originates outside this slice.]

### 2026-03-31 — Record commit OID in session YAML [L271-L274]
Owner words: none quoted — recorder entry, not owner words.
In force:
- After any batch_commit(), session-consolidator records `commit_oid: {first 12 chars of OID}` alongside github_writes in the session YAML.
Open: none.

### 2026-04-02 — Verify an item does not exist before raising "create item" [L276-L279]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Before any gap entry with action "create item"/"write item specification", GET the relevant part05-* file and look for the item heading; if found, change action to "verify/update" and note pre-existence.
Open: none.
[CHECK] Item layer status (see L61-L62 note).

### 2026-04-02 — XREF-PENDING tags live in the consolidated file [L281-L284]
Owner words: none quoted — recorder entry, not owner words.
In force:
- XREF-PENDING tags and Part stub content live in versions/current/Guidebook_for_Accessible_Design_v9-0_2026-03-20.md, not in part05-* files. Check the consolidated file first.
Open: none.

### 2026-04-02 — Connection register ID format CON-0NNN [L286-L289]
Owner words: none quoted — recorder entry, not owner words.
In force:
- IDs use 4-digit zero-padded format (CON-0093, not CON-093). Verification scripts: f"CON-0{i:03d}".
Open: none.

### 2026-04-02 — Part file names do not map 1:1 to Part numbers [L291-L294]
Owner words: none quoted — recorder entry, not owner words.
In force:
- After CO-0004: part08 = Part 9 Engineering; part03 = Part 3 Multiple Categories; part04 = Part 4 Synthesis Matrices; part05-a through k = Item Specifications. Read the first heading (## Part N:) before editing.
Open: none.

### 2026-04-02 — Part 5 content kept in two stores [L296-L299]
Owner words: none quoted — recorder entry, not owner words.
In force:
- A write to parts/v10/ (e.g. part05_v10-0_draft.md) requires the corresponding stub in versions/current/ to be updated in the same session.
Open: none.
[CHECK] Two stores of the same content is the shape later pointer-discipline rulings (L866) forbid in the database; this file-level rule is not marked superseded.

---

## Session 2026-04-06 — Evidence Expansion Phase 1

### 2026-04-06 — Do not use PubMed for architecture topics [L306-L308]
Owner words: none quoted — recorder entry, not owner words.
In force:
- CONDITION: research on architecture, wayfinding, bathroom design, sensory space design or built-environment typology. ACTION: do not use PubMed; use web search, J-STAGE (JA), MDPI, ResearchGate, PMC (disability studies), AJOL (Africa), LILACS (LAC).
Open: none.

### 2026-04-06 — Accessible bathroom outside Europe/NA/AU [L310-L312]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Indonesia Sejong Toilet (Plan International / Nusa Cendana University / DPO, 2022) is the only documented accessible squat-toilet adaptation; cite as Co-1/Tier 1. Japan 多目的トイレ (Barrier-Free New Law 2006) is the most comprehensive non-Western accessible toilet standard.
Open: none.

### 2026-04-06 — Wayfinding outside Europe/NA/AU [L314-L316]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Singapore BCA Code on Accessibility 2025 Ch. 8 is the most comprehensive Asian wayfinding code (Tier 6). ISO 23599:2019 is technically sound globally — gap is implementation, not specification. India 75% policy gap (PMC12082883). Nigeria: no tactile in hospital wayfinding (Ahmed 2022).
Open: none.

### 2026-04-06 — Sensory space design outside UK/AU/US/IE/CA [L318-L320]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Confirmed non-Western sources: Japan (Tsukuba Tier 1 J-STAGE 2025), Egypt (Mostafa ASPECTSS — 5/21 Bertone 2021 studies), Chile (Ley Autismo N°21.545, Tier 6).
- Collectivist-culture transfer problem: private individual retreat model (PAS 6463) does not fit collectivist contexts; no alternative model exists in the literature.
Open: none.

### 2026-04-06 — Global South disability housing [L322-L324]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Formal/informal city divide is the meta-barrier; legislation exists but implementation fails across ET/TZ/ZA/IN.
- Best Co-1 route: peer-reviewed papers embedding DPO narratives (not direct DPO websites).
- Kenya National Cooperative Housing Union (WHO HHGL) is the only Global South positive accessible housing production model identified.
Open: none.

---

## Session 2026-04-06 — Phase 1-E Sessions 2-3 + Phase 2

### 2026-04-06 — Full 40-char OIDs before REST PUT [L330-L333]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Retrieve full 40-char OIDs via GraphQL `oid` before any REST PUT; never use a truncated sha.
Open: none.

### 2026-04-06 — ZH housing evidence ceiling [L335-L338]
Owner words: none quoted — recorder entry, not owner words.
In force:
- ZH disability housing evidence is policy/statistical dominant; peer-reviewed Co-1 housing narratives unavailable. Accept CDPF statistical bulletins and Wuzhang'ai Lanpishu as the ceiling; flag as statistical-only in co1_pass_summary; do not extend search.
Open: none.

### 2026-04-06 — IDA compilations for CRPD concluding observations [L340-L343]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Search internationaldisabilityalliance.org article-specific compilations first for Art. 9 / Art. 19 evidence; individual OHCHR country pages only for jurisdictions not covered.
Open: none.

### 2026-04-06 — UN-Habitat Housing Accessibility Handbook (2016) [L345-L348]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Only identified design-level guidance for accessible housing in slum upgrading, affordable housing and reconstruction contexts. Cite as Tier 4 when addressing accessible design outside formal new construction; do not treat formal new-construction standards as applicable to informal contexts without it.
Open: none.

---

## Session 2026-04-07 — thermoregulation-built-environment

### 2026-04-07 — Thermoregulation-impaired: 18–22 °C [L355-L358]
Owner words: none quoted — recorder entry, not owner words.
In force:
- CONDITION: indoor thermal environment for NEU (MS, SCI), OFS (POTS, MCAS) or PAIN (FMS). ACTION: working target 18–22 °C. Floor 18 °C (WHO minimum; FMS cold threshold). Ceiling 22 °C (MS Uhthoff onset; SCI heat risk). Above 24 °C exceeds WHO vulnerable-individual threshold — not acceptable at rest.
- Flag as derived from clinical evidence synthesis, not any single accessible building standard or OT CPG.
Open: none.
[CHECK] Uses pre-2026-07-23 population codes (NEU, OFS).

### 2026-04-07 — FMS thermal profile opposite to MS/SCI [L360-L363]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Confirmed co-occurrence conflict. Apply harm asymmetry: neurological deterioration (MS/SCI) is higher harm. Ambient default 18–20 °C; individual local warmth provision for FMS (heated seating, radiant panel, additional clothing insulation) as supplementary provision.
Open: none.

### 2026-04-07 — No OT CPG addresses thermal environment [L365-L368]
Owner words: none quoted — recorder entry, not owner words.
In force:
- When citing OT evidence for thermal specifications, disclose: "No OT CPG addresses thermal environment as a home modification domain [confirmed GAP-LRP-01 Phase 1-A search 2026-04-07]. Specifications derived from clinical evidence and WHO housing standards."
Open: none.

### 2026-04-07 — Mechanical cooling in hot-humid tropics [L370-L373]
Owner words: none quoted — recorder entry, not owner words.
In force:
- In hot-humid contexts (ambient >32 °C, RH >70%), passive cooling cannot hold ≤22 °C; mechanical cooling or dehumidification + fan is medically necessary for SCI tetraplegia (≥C8) and heat-sensitive MS — a designed-in feature, not optional retrofit.
- Applies to tropical/subtropical jurisdictions (IN, ZA, NG, KE, ID, PH, TH, BD, SG, BR coastal, CO/EC coastal, EG). Cross-reference CON-0101, CON-0107 and F-07.
Open: none.

### 2026-04-07 — Formal/informal divide; informal housing out of scope [L375-L376]
Owner words: none quoted — recorder entry, not owner words.
In force:
- The guidebook specifies for formal new construction and planned retrofit only; informal settlement housing is out of specification scope. Part 1 states this and identifies it as the highest-priority research and policy gap.
Open: none.

### 2026-04-07 — ISO wayfinding transfers universally [L378-L379]
Owner words: none quoted — recorder entry, not owner words.
In force:
- ISO 23599 and 21542 wayfinding specifications are physically determined and transfer universally; the Global South gap is implementation and maintenance.
Open: none.

### 2026-04-07 — PAS 6463 two layers [L381-L382]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Physics-based layer (acoustic, lighting, visual complexity) transfers universally; spatial-model layer (private individual retreat) does not transfer to collectivist cultures. Specify the physics; flag the spatial model for Person Mode co-design.
Open: none.

### 2026-04-07 — FMS vs MS/SCI thermal conflict resolution [L384-L385]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Resolves to cool ambient default (18–20 °C) + local warmth for FMS. Severity asymmetry: neurological deterioration (MS/SCI) > pain exacerbation (FMS, reversible). No single thermal standard is universally applicable across disability populations.
Open: none.

### 2026-04-07 — CRPD treaty bodies mandate obligations, not specifications [L387-L388]
Owner words: none quoted — recorder entry, not owner words.
In force:
- The guidebook fills the specification gap treaty bodies leave. Part 1 states this relationship explicitly.
Open: none.

---

## Session 2026-04-09 — Framework Review + Compound Functioning

### 2026-04-09 — Four-framework theoretical layering [L394-L397]
Owner words: none quoted — recorder entry, not owner words.
In force:
- ICF = taxonomy; PEO/PEOP = practice model; Capability Approach = justice framework; Kawa = cultural lens. All four required (Part 3 §3.2.4). Do not position the guidebook as "ICF-based" alone.
Open: none.

### 2026-04-09 — Compound functioning principle [L399-L402]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Co-occurring conditions produce supra-additive disability (MWI: ~16% per additional condition; Clarke: 4.52x environment-impairment interaction). Pairwise conflict resolution (Part 3 §3.8, Part 5) is necessary but insufficient for intra-individual compound profiles.
- Apply §3.8 Step 0 compound functioning check; if non-additive interaction identified, route to Person Mode with documented mechanism. The guidebook equips professionals; it does not prescribe compound resolutions.
Open: none.

### 2026-04-09 — FDR four scenario types [L404-L407]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Scenario types: granular (ICF), compound [COMPOUND], occupation [OCCUPATION], environment [ENVIRONMENT]. Token weights: compound 2x, occupation 3x, environment 2x. Compound and occupation synthesis requires Opus[-class].
- Registry: references/fdr/fdr-slug-registry-v2.md (supersedes §9 priority targets). Apply §11 protocols.
Open: none.

### 2026-04-09 — Kawa informs non-Western sensory space [L409-L411]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Kawa-informed specification designs for shared calm (collective flow) rather than individual withdrawal. Specify physics-based parameters universally; flag the spatial model for Person Mode co-design with cultural context input. Reference Kawa (Iwama 2006).
- Applies to sensory rooms (A-16), retreat spaces, NDV/MH provisions for non-Western or collectivist contexts.
Open: none.

### 2026-04-09 — connection_type field [L413-L416]
Owner words: none quoted — recorder entry, not owner words.
In force:
- connection_type: CROSS-POPULATION, CROSS-ITEM, COMPOUND-INTERACTION or METHODOLOGY. COMPOUND-INTERACTION connections come from FDR compound scenarios (registry §C), flag non-additive effects, route to ISW with compound-synthesis brief (Opus[-class] required).
- Run Step 2b (compound interaction scan) after Step 2.
Open: none.
[CHECK] Names connection-scout, which a skill listing describes as absorbed into connection-discovery (D-0146) — outside this slice.

### 2026-04-09 — MH de-escalation room distinct from sensory quiet room [L418-L419]
Owner words: none quoted — recorder entry, not owner words.
In force:
- MH de-escalation room requires exit sightline (PTSD anti-entrapment) and staff access; A-16 requires acoustic isolation without staff presence. Both required in healthcare, psychiatric and supported housing settings. Wilson 2023 (Co-1) documents failure of combined rooms.
- CON-0002 multi-population expansion of A-16 (NDV, OFS, PAIN) is correct; CON-0002 retirement of separate MH room is incorrect per CON-0131. Faerden 2022 d=2.0 for user control is contingent on MH-specific parameters.
Open: none.

### 2026-04-09 — Quantified claims need DOI + page/table [L421-L424]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Quantified outcome claims (percentages, n= counts, reduction/increase figures) require DOI + page/table reference, or a direct URL. Otherwise [UNVERIFIED-QUANT]; not used in Part 4 specifications or Part 11 economic arguments without verification.
- Verify the specific number appears in the cited source before committing; after 2 failed attempts apply [UNVERIFIED-QUANT]; do not delete the directional claim — flag the number only.
- "X% across N facilities (Author Year)" is the highest-risk hallucination template.
Open: none.

---

## Enforcement Gates

### 2026-04-19 — Validators and CI [L429-L475]
Owner words: none quoted — recorder entry, not owner words.
In force:
- `scripts/validate_bpc.py`: all 8 mandatory BPC sections (PICO, Search strategy, Key sources, Best practice synthesis, Evidence gaps, Jurisdiction coverage, Co-1 pass, Metadata); Key sources as CO-0006 REF-ID table (REF-ID, Authors, Year, Title) or legacy flat format (transition); Metadata keys slug, population, last_updated. Failure codes MISSING_SECTION · KEY_SOURCES_FORMAT · KEY_SOURCES_MISSING_COLUMN · METADATA_MISSING_KEY. Relax only via PR modifying the validator; do not remove validation.
- `scripts/validate_cross_refs.py`: CON-IDs resolve to `references/connections/_index.md`; every BPC has a matching search-log and vice versa. Failure codes BROKEN_CON_ID · MISSING_SEARCH_LOG · ORPHAN_SEARCH_LOG.
- `scripts/check_thresholds.py` retired; registers are in SQLite (`data/guidebook.db`).
- `ci.yml`: jobs `syntax`, `structure`, `commit-msg` (HEAD message matches `{skill-name}: {action} [YYYY-MM-DD HH:MM]`). Do not bypass.
- Branch-protection clause: see the 2026-04-19 02:20 entry below (later same day; ruleset disabled during Phase A).
Open: none.
[CHECK] `validate_cross_refs.py` points at the markdown `_index.md` that L261 calls archived. CLAUDE.md (outside slice) describes a different current check apparatus (`check-registry.yaml`, `run_checks.py`); this section is not marked superseded.

### 2026-04-19 — Branch protection ruleset disabled during Phase A [L478-L481]
Owner words: none quoted — recorder entry, not owner words.
In force:
- GitHub branch protection ruleset stays DISABLED during Phase A; CI still runs on every push. Re-enable only on transition to PR-based workflow in Phase B. Do not re-enable or instruct the user to re-enable during Phase A.
Open:
- [CHECK] Whether Phase A has ended / the project is now on a PR-based workflow (CLAUDE.md rule 9 describes PRs).

---

## Session 2026-04-26 — CO-0007 Stage 0 close

### 2026-04-26 — Pre-launch reality: solo authorship [L488-L489]
Owner words: none quoted — recorder entry, not owner words.
In force:
- The project is a single-author synthesis; no DPO partnerships, Co-1 collaborator panels, recruitment thread or compensation structure exist.
- Co-1 evidence is engaged through the published corpus (peer-reviewed lived-experience research, DPO position papers, named advocacy organisational positions, Co-1-authored academic narratives), not through collaborators.
- Post-launch collaboration is contingent and may never occur; solo-only-permanent is a possible end-state. Governance language declares this reality and does not project a fictional operational structure with pending triggers.
- The Co-1 evidence commitment (co-primary with T1) is unaffected. CRPD Art. 4.3 honoured in partial form pre-launch; full participatory honouring is contingent on launch.
- Supersedes the original D-03 resolution in `governance/pre-stage-a-decisions.md`.
Open: none.

### 2026-04-26 — Governance + code co-production [L492-L495]
Owner words: none quoted — recorder entry, not owner words.
In force:
- CONDITION: any Stage A phase (A3–A13) defining or refining an entity, taxonomy or state machine. ACTION: deliverables include the governance document AND (1) a Pydantic schema in `schemas/`, (2) a CI validator in `scripts/`, (3) a sample conversion script in `scripts/convert/`. Prose SKILL.md files give judgment guidance only; output validation is mechanical. CI must pass before session close.
Open: none.
[CHECK] Bears on later minimise-code doctrine (CLAUDE.md §8, outside slice); not marked superseded.

---

## Session 2026-04-29 — A4 / A5 / A6

### 2026-04-29 — Specification voice tier- and authority-located [L502-L505]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Per voice-style §8.1: Universal Mode cites the code; Population Mode cites the evidence; Person Mode locates authority in OT assessment plus the individual.
- §8.2: Pattern A (inline location) for prose and short cells; Pattern B (umbrella convention) for dense matrix tables.
- §8.3: Co-1 voice patterns Co-1-A (single-source), Co-1-B (multi-source synthesis), Co-1-C (T1/Co-1 convergence), Co-1-D (T1/Co-1 divergence).
- Categorical authority claims ("shall be" as blanket spec, "operates above the code floor", "this document governs" over external instruments, "non-negotiable" as self-claim, unlocated "X is mandatory") are voice failures routed to remediation.
Open: none.

### 2026-04-29 — Co-1 citations carry six schema fields [L508-L511]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Per `governance/co1-operational.md` §6.1: `tier`, `evidence_type`, `co1_provenance`, `co1_source_type`, `verification_status`, `synthesis_attribution_required`. Reject any Co-1 citation lacking them.
- Pre-launch all `co1_provenance` = `published_corpus`; `participatory_synthesis` is post-launch contingent.
- CS2 (Co-1 recruitment) requires three triggers (launch + resources + co-designed recruitment specification); pre-launch INOPERATIVE.
- CS5 pre-launch = corpus-representation monitoring (per-population, per-domain, per-jurisdiction Co-1 inventories, gap-flagging via `gap_register.md`).
Open: none.

### 2026-04-29 — Values-based conflicts: broadest-benefit [L519-L522]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Per `governance/evidence-methodology.md` §4: classify conflict as function-based (→ harm asymmetry) or values-based (→ broadest-benefit). Assess population breadth, irreversibility, supplementary-provision feasibility; document both positions with Person Mode handoff.
- Values-criteria does not override harm asymmetry, does not apply at Universal Mode, does not eliminate Person Mode resolution.
- ACTION: apply §4.2 three-step assessment; default per broadest-benefit; supplementary provision for the alternative; record convergence assessment as divergent with synthesis_approach.
Open: none.

### 2026-04-29 — Meta-methodological citations outside the tiers [L524-L527]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Pedagogy/theory/methodology citations (e.g. Schön 1983, Hmelo-Silver 2004, Royeen 1995, ICF, PEO/PEOP, Capability Approach, Kawa) sit outside the seven tiers: cited in Part 1/mission/front matter only; no evidence marker; not processed by validate_evidence_state.py; not stored as EvidenceSource records; not in specification cells.
Open: none.

### 2026-04-29 — A6 evidence-methodology.md canonical [L529-L530]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Canonical; governs evidence-state machine (T-04), convergence assessment, values-criteria mechanism, design-pedagogy classification, epistemic-defence patterns. Schema: evidence_state.py, enums.py, evidence_source.py. Validator: validate_evidence_state.py.
Open: none.

### 2026-04-29 — A7 population-taxonomy.md canonical [L533-L534]
Owner words: none quoted — recorder entry, not owner words.
In force (resulting state per 2026-07-24, L576):
- population-taxonomy.md carries a SUPERSEDED banner for its code scheme; its IntD-proxy and BAR-containment sub-rules are void. Its non-code content (sub-code hierarchy/inheritance, VIS/DEAF/DBL distinctness, co-occurrence notation, one-slug-one-population, conflict-domain resolution) stands until its rewrite.
- Validator: validate_population.py.
Open:
- [OPEN] Rewrite of population-taxonomy.md (deferred per the 2026-07-24 entry).

### 2026-04-29 — A8 jurisdiction-philosophy.md canonical [L536-L537]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Canonical; governs 24-jurisdiction approach, jurisdiction–tier relationship (codes = Tier 6, standards = Tier 4–5), standards currency tracking, GB→UK enforcement. Validators: validate_jurisdiction.py, convert_jurisdictions.py.
Open: none.

### 2026-04-30 — A9 time-model.md canonical [L539-L540]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Canonical; five temporal axes (document version, standards edition, project-rule effective date, source publication/verification, launch phase); SupersedenceLink primitive (types rule/standard/version/decision/source); date format `YYYY-MM-DD HH:MM` canonical, pre-session anchor `2026-03-15 00:00`; freshness windows per evidence tier.
- Schema: temporal.py, enums.py. Validators: validate_temporal.py (T-01–T-12), version_retrofit.py (to `data/temporal/`).
Open: none.

### 2026-04-30 — A10 adversarial-use-framework.md canonical [L543-L544]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Canonical; nine misuse vectors: V-01 minimum-compliance weaponisation, V-02 exclusionary ROI, V-03 surveillance via inferred functional needs, V-04 selective citation, V-05 Co-1 instrumentalisation, V-06 evidence-tier laundering, V-07 anti-DAR deferral, V-08 adversarial litigation citation, V-09 population-proxy denial.
- Pre-public-release review gate (C1 catalogue well-formed, C2 review coverage complete, C3 review entries well-formed); CS9 review cadence (per release, Stage C periodic, retroactive coverage on catalogue extensions); release-override path for ESCALATE reviews.
- Schema adversarial_use.py; validator audit_adversarial_use.py (checklist runner, not auto-detection); catalogue data/adversarial_use/catalog.yaml.
Open: none.

### 2026-04-30 — A11 legal-regulatory.md canonical [L546-L547]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Canonical, with §3.3 provisional pending counsel review. Teaches-not-prescribes posture (§1); liability framing across four risk vectors (§2: misuse-of-recommendation, V-08 adversarial citation, currency, mis-jurisdiction).
- Five-element front-matter disclaimer (§3.2: not-legal-authority, not-professional-advice, synthesis-state-transparency, currency-notice, jurisdictional-scope); provisional wording §3.3.
- CC BY-SA 4.0 licensing (§4.3) with carve-outs for Co-1 sources and standards/codes.
- Decline-pursuit / accept-invitation trajectory (§5.3): no active jurisdictional adoption pursuit; no certification system.
- §7 review cadence: major release / jurisdictional law change / material methodology change.
- V-08 release-gate reviews status = cleared_with_notes pending counsel completion.
Open:
- [OPEN] §3.3 disclaimer wording pending counsel review.
- [OPEN] 10-question counsel review queue (§6).

### 2026-04-30 — A12 decision-protocol.md canonical [L549-L550]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Decision categories: D-DOCT, D-METH, D-SCHEMA, D-OP, D-PRES. Delegation categories: DG-NON, DG-REVIEW, DG-AUTO, with default table.
- Always-DG-NON: mission/CRPD; population taxonomy; evidence-tier definitions; jurisdiction inclusion; major work-products; Co-1 corpus; licensing (A11 §4); trajectory (A11 §5); misuse-vector retirement (A10 §5.4); counsel-queue resolution (A11 §6).
- 16-field capture protocol; §3.3 rationale-length norms; §3.4 anti-patterns (tautology, authority-without-content, outcome-as-rationale).
- Model-routing notation `{tier}/{effort}/{modifier}` (see 2026-07-25 entry: class, never version).
- Decision register at data/decisions/decision_register.yaml.
- CS8: every new RULE in project-standards pairs with a Decision record.
- Schema decision.py; validator decision_capture.py (C1–C8).
Open:
- [CHECK] "Sessions remaining in A12" (seeding extraction, session-consolidator wiring, C7 tightening; presentation-layer expansion) — completion status not stated.

### 2026-04-30 (amended within slice 2026-08-19) — A13 doctrine-recheck.md canonical [L552-L553]
Owner words: none quoted — recorder entry, not owner words.
In force (resulting state per 2026-08-19, L649-L661):
- Two cadence triggers: PERIODIC every 25 working sessions; STAGE_TRANSITION at A→B and B→C. RULE_REVISION is struck. Non-triggers: new RULE without supersession, new governance doc for a new phase, skill or operational change.
- Procedure passes: 2.2 doctrine inventory; 2.3 cross-reference consistency; 2.4 drift detection; 2.5 decision-register cross-check; 2.6 contamination resampling (4-state rubric CLEAN / AMBIGUOUS / STUB / MERGED); fresh-context decision-checking.
- Record format: RecheckSession + RecheckFinding + ContaminationSample + DoctrineSnapshot. Schema doctrine_recheck.py; validators doctrine_recheck.py, contamination_sampler.py (--n floor 15).
- CS1 LIVE.
Open: none.

### 2026-05-04 — Citation mining state is in SQLite [L555-L558]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Citation mining state in `citation_mining` table; query `python3 scripts/db.py mining`. CHECK before mining (skip if backward=1 and forward=1); LOG via `db.py log-mining`. Skipping CHECK or LOG is a protocol error.
Open: none.
[STATUS UNCERTAIN: entry is headed "[SUPERSEDED — CO-0009]" while its body states a live SQLite rule; what superseded it, and whether the label refers to the markdown register, cannot be told from the text.]

---

## 2026-07 rulings

### 2026-07-22 (terminology superseded within slice 2026-08-24 / 2026-08-25) — Work from ICF-anchored demands, no armchair umbrellas [L561-L564]
Owner words: "work from axes"; "record and remember what you just wrote ... extremely important to your process"
In force:
- All population/profile curation, demand-mapping and specification proceeds FROM the functional demand layer (Layer 1 of `governance/functional-taxonomy.md`: architect-actionable, diagnosis-neutral, co-occurrence-native), never FROM broad population/profile umbrellas.
- The profile layer (Layer 2) holds only specific self-identified communities named on their own terms (co-produced; "nothing about us without us"); never armchair coalition codes.
- Broad umbrellas (e.g. "physically disabled"; clinical-cluster relabels like "energy-limiting chronic illness") are forbidden as profile codes. A population is a mapping-confidence-weighted vector over demand dimensions, not a bucket. Umbrellas only as additive cross-cutting tags, never replacement codes.
- ACTION: (1) work from the demand layer, not umbrellas; (2) if coining an umbrella, STOP and decompose; (3) add profiles only as specific self-identified communities, co-produced; (4) umbrellas only as additive tags.
- Terminology: the word "axis" is not to be used as the layer's identifier (2026-08-24); the layer is named `icf_demands` (2026-08-25). Substance survives the rename.
- Amended in part by the 2026-07-23 design-equivalence exception (next entry).
Open: none.

### 2026-07-23 — Design-equivalence exception to the anti-umbrella rule [L567-L570]
Owner words: "make ... exceptions ... brain and complex are literally TOO complex to avoid umbrellas ... high comorbidity ... 5 tags with 100% overlap"; "umbrellas are bad when they erase differences, and in this context, they aren't really different"
In force:
- An umbrella population code is permitted when members do not meaningfully differ for design (shared/overlapping demand signature), even with differing etiology. Forbidden only when it erases design differences (collapsing opposed or orthogonal demands, or dropping distinct signatures; OFS→"ELCI" remains the paradigm forbidden case).
- Ratified exceptions: COM (complex conditions — dysautonomia / long-COVID / MCAS / ME/CFS / POTS) and BRAIN (acquired brain injury — stroke / TBI / post-concussion).
- Test, all three required: (a) high within-umbrella comorbidity OR near-identical design profile; (b) the UNION of member demand signatures preserved on the umbrella code, never deduped (COM: AX-CHM+AX-STA+AX-BAL+AX-THR+AX-COG-O; BRAIN: AX-COG-O+AX-BAL+AX-AMB+AX-ARO+AX-COM-E+AX-SPR+AX-STA); (c) no opposed demand between members.
- Does not license further umbrellas failing (a)–(c); any new umbrella is forbidden until it passes the test and is owner-ratified. The base rule stands for all other cases.
Open: none.

### 2026-07-24 — Population-scheme reconciliation [L573-L579]
Owner words: "body size as a code"
In force:
- Population code scheme: flat, community-organised set of 23 codes: BLIND, DEAF, DEAFBLIND, MOB, LMB, SCI, MOVE, NDV, AUT, ADHD, ID, DEM, BRAIN, COM, PAIN, MS, EPI, VES, MH, LPA, TALL, BAR, ALL — no parent codes, no slash sub-codes. Operative source: `schemas/enums.py` PopulationCode + DR-2026-07-23-population-schema-replace (not population-taxonomy.md's superseded body).
- ID (intellectual disability) is first-class; do not proxy (People First person-first naming). The IntD-proxy rule (2026-03-25) is void.
- LPA (little people / dwarfism), TALL and BAR (larger bodies) are retained codes forming the body-size-and-stature group, served by the A-SIZE access need, framed as the environment being wrongly normed to an average body — never as bodies deviating. "Is it a disability" is not the inclusion test; inclusion is by self-identified community + shared design demand. TALL is included for fit, not as a disability-identity claim. The BAR-exclusion rule is void.
- population-taxonomy.md: SUPERSEDED banner for its code scheme; IntD-proxy and BAR-containment sub-rules void; non-code content stands until rewrite.
Open:
- [OPEN] population-taxonomy.md rewrite (DR "Deferred").
[CHECK] CLAUDE.md §6 (outside slice) records `population_code` retired in favour of three lens columns (owner 2026-08-28; medical lens deleted 2026-11-16) and `base_taxonomy_identity` as the identity lens; the adjudicator should rank this entry against those.

### 2026-07-24 — Merge implies ratification [L582-L585]
Owner words: "always assume I Ratify if I merge it unless I explicitly note otherwise"; "I want to ratify and progress, not find out something was never implemented because it was just merged without ratifying formally"
In force:
- Merging a branch/PR to `main` ratifies every decision, DR, governance proposal and rule change it contains, with the force of an explicit "ratify", unless the owner explicitly notes otherwise on that merge.
- Limits: (1) merge ratifies the decision but does not complete gated execution — those items become authorised-and-owed, tracked in the ratification-execution register; (2) does not waive genuine external preconditions a DR names; (3) does not promote an evidence-maturity `provisional`/`pending` state to `stated`; (4) DG-NON items still require the owner's substantive direction to have occurred.
- ACTION: flip stale PROPOSED/PENDING status text to ratified-by-merge (dated); move gated execution from "blocked pending ratification" to "authorised/owed" and surface it; do not use the rule to auto-complete DG-NON substance, skip named preconditions, or promote evidence states.
Open: none.

### 2026-07-25 — Rendered document is a derived surface; gate it [L588-L591]
Owner words: "How do you ensure that everything gets called up every time?"
In force:
- A hand-authored rendered document (`specs/*.html` and any successor surface) may summarise the canonical record; it may not contradict it or present it as stronger than it is.
- Enforcement at preflight via two gates: `scripts/audit/check_rendered_docs.py` (document vs DB: C1 citation fidelity; C2 epistemic persistence; C3 doc↔DB drift against `item_population_links`; C4 grade preconditions — no ● over a pending convergence, wholesale down-weighting, or T4–T6 governing ref without disclosure) and `scripts/audit/render_audit.js` (real browser: R1 print, R2 no-JS, R3 reflow at 320/768/1280 and under WCAG 1.4.12 text spacing, R4 target size 2.5.8, R5 focus-not-obscured 2.4.11).
- A checker that cannot see the whole system must not render a verdict on the whole system; the browser is the authority on visibility; `preflight.sh` prints a loud `[SKIP] … this check did NOT run` rather than passing silently.
- ACTION: (1) run `scripts/preflight.sh` before pushing; (2) never let a page assert more than the record holds — if thin, say so; (3) a checker whose evidence cannot decide its question is demoted to WARN and points at the one that can; (4) any page under `specs/` is in scope automatically.
- Applies also to any session changing `assets/guidebook.css`.
Open: none.
[CHECK] CLAUDE.md §3 (outside slice) records render surfaces are read from the database when rendered and "no committed file is one" (owner 2026-08-27); C3 reads `item_population_links` (item layer reportedly dropped).

### 2026-07-25 — Symmetric disclosure [L594-L597]
Owner words: none quoted — recorder entry, not owner words.
In force:
- When a document characterises the weakness, provenance or down-weighting of sources it discounts, it discloses the equivalent facts about its own governing sources with the same specificity and in the same place.
- ACTION: (1) for every weakness stated about a discounted source, state the equivalent about your own; (2) put it where the claim is, not only in an appendix; (3) if your own anchor is pending, down-weighted or regulatory-stratum, say so beside the grade.
- Partially mechanised by C4 of `check_rendered_docs.py`; the general obligation is level 1.
Open: none.

### 2026-07-25 — No scope narrowing in restatement [L600-L603]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Restate the scope the source claims. Any narrower scope is the guidebook's claim and is marked as the guidebook's, never attributed to the source.
- ACTION: (1) check restated scope against the source's own scope statement; (2) if you narrow, attribute the narrowing to the guidebook; (3) if the source's scope is unclear, say so — do not resolve it silently either way.
- Not mechanisable with current tooling; level 1.
Open: none.

### 2026-07-25 — Model routing names a class, never a version [L606-L609]
Owner words: "best_practice_synthesis can be fable as well. opus 5 is clearly opus class. if it's specifying model number then strip that going forward"
In force:
- All model-routing text names a class (`opus`, `fable`, `sonnet`, `haiku`, `human`), never a version number; strip version numbers on touch.
- `fable` is a synthesis-capable tier (`governance/decision-protocol.md` §4.2/§4.4; `schemas/decision.py` pattern `^(opus|fable|sonnet|haiku|human|legacy)/…`).
- `best_practice_synthesis` floor: Opus-class or above, which includes Fable-class; `sonnet` and `haiku` do not satisfy it.
- Do not re-pin the floor to whatever model is current.
Open: none.

### 2026-07-25 — Parameter vs element; relations are pointers, not shared aliases [L612-L615]
Owner words: "build a list of synonyms across each language ... ensure that equivalent words for a term get grouped"
In force:
- A parameter and its element are distinct terms; each `scope_note` names its counterpart (e.g. TERM-002 corridor width ↔ TERM-048 circulation route; TERM-012 sensory room ↔ TERM-074 withdrawal space; TERM-016 wheelchair user ↔ TERM-079 mobility aid).
- Two concepts sharing an alias is a collision, not a link. Express relations with NARROWER/BROADER and name the counterpart in `scope_note`.
- Deliberate exception: population/project codes (OFS, TALL, LMB, MOVE) may map to two sibling concepts; such rows are annotated as intentional.
- ACTION: (1) when adding a dimensional parameter, check whether its element exists, and vice versa; (2) never relate terms by shared alias; (3) run `python3 scripts/audit/alias_provenance_audit.py` and the collision query AFTER the change; (4) annotate any deliberate shared code alias.
Open: none.

### 2026-07-25 — Match slug tokens, never substrings [L618-L621]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Slug→term resolution uses token matching over canonical names AND English aliases, a corpus-derived stoplist, and a specificity rule discarding common-token-only matches when a rare token also matched.
- A stemmer must not strip the final `s` of *access*/*cross*/*analysis*.
- When a synonym causes a bad match, the synonym is the defect: fix the alias, not the stoplist.
- ACTION: (1) never resolve an identifier by substring against a name; tokenise both sides; (2) print the TERMS a slug resolved to, not only the query; (3) after changing vocabulary, re-run the false-positive sweep across ALL slugs; (4) fix the offending alias.
Open: none.

### 2026-07-25 — Alias provenance [L624-L627]
Owner words: "did we fix everything identified?"; "resolve usefully"
In force:
- Every alias created on or after 2026-07-24 carries a provenance marker in `notes`; earlier cohorts grandfathered and reported (backfill-on-touch).
- Markers per `references/native-alias-verification.md`: MODEL-GENERATED → VERIFIED-GLOSSARY (standards-body glossary) / VERIFIED-NATIVE (qualified native-speaker review) / VERIFIED-CROSS (corroborated across published sources).
- Enforcement: `scripts/audit/alias_provenance_audit.py`, blocking in `audit.yml`.
- Do not model-generate vocabulary in a language nobody on the project reads; source it from a published glossary or register the gap (GAP-302). Unverified backlog tracked as GAP-303.
- Remedy model: named national instrument, verbatim retrieval, no back-translation.
- "A convention introduced mid-flight meets correct work that predates it, and the convention is what yields." [CHECK: principle or one-off observation]
- ACTION: (1) record a marker on every alias you add; (2) flag model-generated terms in any artefact that ships them; (3) never invent vocabulary in a language you cannot read — register a gap naming the glossary; (4) treat non-English retrieval as unverified until a VERIFIED-* marker exists; do not report its coverage as confirmed.
Open:
- [CHECK] Whether the gate defect (provenance asserted in prose failing a marker-string check) has been fixed.

### 2026-07-25 — Environment contract enforced; exemptions declare dependencies [L630-L633]
Owner words: "We MUST resolve this"
In force:
- Every DB-aware script honours `GUIDEBOOK_DB_PATH`; enforced by `scripts/audit/db_path_env_audit.py` (blocking in `audit.yml`). Scope by AST (calls `sqlite3.connect` AND names the DB outside a docstring) over `scripts/`+`tools/` minus one-time/legacy dirs (same `EXCLUDE_PARTS` as the code-layer audit).
- `scripts/db/**` targets `data/db/guidebook.db`, a different legacy file, not the canonical DB.
- Exemptions are documented in the audit; a delegating exemption declares `delegates_to` so it self-invalidates (e.g. `graph_audit.py` → `graph/build.py`).
- ACTION: (1) resolve DB path as `Path(os.environ.get("GUIDEBOOK_DB_PATH", <default>))`; (2) before trusting a redirected test, confirm the script honours the variable; (3) an exemption states its reason and names any component it rests on; (4) when a documented contract is false, fix the code AND the document, and gate it.
Open: none.

### 2026-08-19 — Search for existing work before writing anything [L636-L639]
Owner words: "add a standing rule to always check for existing work/tools before writing any code"
In force:
- CONDITION: before writing or proposing any script, check, registry entry, workplan document, DR, standing rule, register, sweep or protocol; and whenever a finding feels novel.
- ACTION: (1) search first and say what you searched: `governance/check-registry.yaml` and `references/tooling-register.md`; `scripts/` and `tools/` by function; `references/project-standards.md`; `decisions/` and the `decisions` table; `workplan/` by date. The root `.ignore` hides `_archived/`, `audits/`, `sessions/`, `workplan/_superseded/`, `versions/` from ripgrep — search those by explicit path. (2) If prior work exists, extend or cite it; if you supersede it, say what changed and why the earlier version failed. (3) If a prior rule, freeze or tripwire covers the situation, check whether it was executed before proposing a replacement — an unenforced rule needs teeth, not a successor. (4) Record the search in the session record or artefact; a search that found nothing is completed work.
Open: none.
[CHECK] The 2026-08-22 entry (L663) forbids text search to establish facts about the repository; this entry prescribes searching for prior work. Not stated to conflict.

### 2026-08-19 — Adversarial review bound to evidence, never plans [L642-L647]
Owner words: "the plan will require adversarial reviews to ensure accuracy and factuality, and it may need to be agonist-antagonist in manner"
In force:
- An adversarial pass may be commissioned ONLY against a diff that (a) wrote rows to research tables (`search_executions`, `search_candidates`, `evidence_sources`, `source_slug_links`, `evidence_population_match`, `source_value_extractions`, `specifications`, `convergence_assessment`, `jurisdictional_values`, `case_studies`, `economics_entries`) or (b) authored/amended a synthesis artefact (`references/bpc-reasoning/*`, `best_practice_synthesis`, a rendered determination page). Plans, critiques, censuses, handoffs, registers, session records, DRs and this ledger are not subjects.
- The antagonist attacks the recorded affirmative case through named lenses — existence, fidelity, independence, tier, population, contrary-finding, recognition by the population served, query-shape; blind-then-compare (re-grade tier and population-match before seeing the author's grades, then diff).
- ACTION: (1) test target against (a)/(b); if it fails, decline in one line of the session log; no critique document. (2) Record each finding as claim-attacked / method / verdict / severity, including SURVIVED claims. (3) Close each sustained finding by row correction in the same pass via migration; if disputed, cap the cell at `provisional` and record the dispute; never schedule remediation; a pass emits data plus one session record and may not create or modify a workplan. (4) To contest a plan, append a single objection ≤1 page to the plan file, naming the clause and evidence, and flag the owner; no standalone contest document, no counter-critique. (5) At most one adversarial pass per research batch; a pass on a pass is forbidden.
Open: none.
[STATUS UNCERTAIN: entry carries "AMENDED 2026-10-09 for one plan only: the owner commissioned a read-only critique of the catalogue plan, so the clause that plans and critiques are not adversarial-pass subjects did not bar it" — amendment originates outside this slice. See also the 2026-08-25 smoke-test record (L1058), a single-session scoped exception that leaves the rule unamended.]

### 2026-08-19 — Doctrine token abolished [L649-L661]
Owner words: none quoted (OD-10 item 4, signed 2026-08-19) — recorder entry, not owner words.
In force:
- CONDITION: any commit touching a synthesis path (`references/bpc-reasoning/`, `references/connection-reasoning/`, `decisions/`, `sessions/`). ACTION: do NOT add a `[DOCTRINE: <sha>]` token. The token apparatus is abolished (token, CI step, `check_doctrine_token.py`, `check_2_doctrine_sha`, `RE_ATTESTATION_WINDOW`, working-session counter); `governance/doctrine-recheck.md` §1.3 RULE_REVISION trigger struck.
- The attestation requirement is unchanged and still binds.
- Supersedes standing rule #11(a) of `governance/project-instructions-v10_14.md`; read this ledger, not the PI.
- Doctrine recheck has two cadences (PERIODIC, STAGE_TRANSITION). `RecheckTrigger.RULE_REVISION` enum value retained for the historical record; new records must not use it.
Open: none.

### 2026-08-22 — Establish facts from structure, never text search [L663-L694]
Owner words: none quoted — recorder entry, not owner words.
In force:
- CONDITION: any claim about what the repository contains, counts, reads, writes, calls, enforces or leaves unenforced (check inventory, reader/caller count, table consumers, battery selection, enforcing code, source already held).
- ACTION: derive from authoritative structure and say which: SQL and `PRAGMA` against `data/guidebook.db`; `governance/check-registry.yaml`; `run_checks.classify()` imported and run; Python AST or import graph; `git ls-files`; `governance/pipeline-map.yaml` for wiring. Do NOT use grep, ripgrep, `git grep` or a regex over the tree to establish it; do not report a hit count as a finding.
- Only exception: precise editing — locating a known literal in a known file to change it; exact-match replacement with an asserted match count is preferred. "finding a place to edit is fine; deciding what is true is not."
- A text match cannot distinguish use from mention, reader from writer, live code from docstring, or absent string from absent file; a tool that could not have seen the thing is not evidence of its absence.
Open: none.
[CHECK] Names `governance/pipeline-map.yaml` as a structural authority; CLAUDE.md §3 (outside slice) calls it retired. CLAUDE.md (outside slice) also prescribes grep for caller sweeps (rule 4) — adjudicator to rank.

### 2026-08-23 — The database is the only system of record for anything a gate must see [L698-L796]
Owner words: "The only data I would truly expect to see from evidence phase onwards is the REF# for cross-referencing specific rows, and population codes / access needs / ICF codes for grouping items."
In force:
- A fact a gate must enforce against may not have a tracked file as its sole home; every check queries `data/guidebook.db`. A file may mirror the DB and may hold what no gate reads (prose, reasoning, session records, retrieval payloads).
- Before deleting any file that holds data, diff it against the table that replaced it and migrate the remainder first. A referent scan proves only that no code reads it, never that nothing is in it.
- `data/decisions/decision_register.yaml` is a consistent mirror of the `decisions` table with live readers (`scripts/decision_capture.py`, `scripts/doctrine_recheck.py`) — not a cull target; cull item D2 is struck. [CHECK: mirror status was a dated measurement]
- Downstream of evidence, a row carries a reference and a grouping key, nothing else about the source. Titles, DOIs, years, journals, tiers and locators are attributes of the source.
- A DOI belongs once, in `source_locators` keyed by `ref_id`; other tables carry `ref_id`, not the string. This structural fix is a schema decision, owner-gated (D-SCHEMA). Until it lands, no new table may add a DOI column, and any join on a DOI must fold case.
- `source_locators` is the identifier home: `doi`, `url`, `pmid`, `isbn`, `issn`, `standard_number` and resolution outcomes belong there. `search_executions.target_tier` describes a search, not a source — exempt.
- Repair targets named: `citation_mining.doi` (redundant with `global_ref_id`); `search_candidates` lacks `ref_id`; re-shape `specifications` (`governing_refs` JSON blob, not FK/join table), `case_studies` (no `ref_id`), `economics_entries` (duplicated source attributes beside `ref_id`) before they take rows. All are D-SCHEMA, owner-gated.
- Within slice, modified by: 2026-08-24 correction (L824) — "drop `citation_mining.doi`" is not executable; use writer-retire, reader-retire, NULL forward; and 2026-08-24 clue-store ruling (L919) — the same DOI in `source_locators` and `evidence_sources` is not a defect; `source_locators` is exempt permanently and its case-drift need not be normalised.
- R9a/R9b reconcile copies; once the single-home fix lands they become unnecessary and can be deleted.
Open:
- [OPEN] The D-SCHEMA single-home DOI fix and the re-shaping of the named tables.
- [CHECK] Live state of `specifications`, `case_studies`, `economics_entries`, `search_candidates` columns has likely moved since 2026-08-23 (CLAUDE.md cites later migrations re-keying `specifications`); counts in the entry are dated measurements and are not reproduced.

### 2026-08-24 — "Axis" is descriptive vocabulary, not a domain identifier [L800-L820]
Owner words: "I don't want axis to be used"; "Axis is a term that we should be able to use freely to describe how things are set up."
In force:
- "Axis" may not name a specific vocabulary layer; it stays free for plain description.
- Pull a frame as ICF codes with names, never bare codes.
- `item_axis_links → population_axis_map` is not a route to item–population applicability; `item_population_links` is. Ratified documents using the old term (incl. the 2026-07-22/23 RULEs and the 2026-08-23 corollary's "two routes" framing) are superseded by this ruling, not authorities against it.
- The layer's name: superseded within slice by 2026-08-25 (L1103) — `icf_demands`, not "ICF-anchored access needs".
- The rename (4 tables, 6 columns, a blocking check, tracked files) is D-SCHEMA and owner-gated (`decisions/DR-2026-08-24-scaffolding-is-phase-specific.md` §1 R8).
Open:
- [OPEN] Execution of the rename migration.

### 2026-08-24 — Correction: `citation_mining` count and repair order [L824-L845]
Owner words: none quoted — recorder entry, not owner words.
In force:
- Derive the `citation_mining.doi` count, never quote it: `SELECT COUNT(*) FROM citation_mining WHERE COALESCE(doi,'') <> ''`.
- A column committed data migrations INSERT cannot be dropped by a DROP that replays before those INSERTs (breaks `migration_reproducibility`). Applies to every column named for dropping in the 2026-08-23 passage where a committed migration writes it.
- Available shape: writer-retire, reader-retire, NULL forward — the column survives as a tombstone; no program writes it; every reader goes to the pointed-to home.
- Before proposing any drop, grep `scripts/migrations/data_*` for the column name — that grep is the gate.
- Tracked as PD-2 in `workplan/2026-08-24-pointer-discipline-queue.md`.
Open: none.
[CHECK] CLAUDE.md rule 5 (outside slice) gives a later form: such a column can be dropped only by a schema migration the replay plan orders after every data migration that INSERTs it (`migrate_db.build_plan()`, `-- AFTER_DATA:` line).

### 2026-08-25 — The four 2026-08-24 owner rulings entered as operative rules (preamble) [L849-L862]
Owner words: none quoted — recorder entry, not owner words.
In force:
- The four rulings that follow (point-don't-copy; pointer discipline; clue store; applicability as output) are operative, not proposals, and were never awaiting ratification (CLAUDE.md rule 0).
- "A ruling that governs the work belongs where the work looks." [CHECK: principle stated by recorder]
Open: none.

### 2026-08-24 — Never write the same fact into a second table; point, do not copy [L866-L892]
Owner words: "If you have reference identification in tables that allow them to be cross-referenced, then you don't need to duplicate anything from one table to the other aside from that reference identifier because you can point to it. I could literally have a thousand tables. So long as each table has a row with a column that shares the same reference identifier, then you can call up information from any one so long as you point to the correct table and column." / "If a crossing row 'carries' its own reason, that introduces the possibility of error and drift because it implies the reason is being written across two or more tables. It is better to have a table cell point to another table cell than to rewrite." / "A crossing row only takes its reference ID. If it is providing a reason, then that reason is specific to the new table."
In force:
- A parity check is not a fix: do not add parity checks, triggers or CHECK apparatus to police a copy — remove the copy.
- A column a committed data migration INSERTs is not physically dropped by a DROP that replays before it; use writer-retire, reader-retire, NULL forward; grep `scripts/migrations/data_*` for the column name before proposing any drop — that grep is the gate.
Open: none.
[CHECK] Same later-form note as the correction entry above (CLAUDE.md rule 5, AFTER_DATA ordering).

### 2026-08-24 — "Highly procedural" means pointer discipline [L896-L915]
Owner words: "Reference IDs carry from table to table across stages. Data relevant in one stage does not cross to another stage. We do not need an author name in a synthesis table when synthesizing information. We do not need an author name when writing a specification in a specification table. We do not need an author name when rendering in a render table. If we have the same reference ID, then we know that we can just point towards the relevant table in the relevant stage for that information. For rendering a citation, then, we point towards the evidence table for that reference ID."
In force:
- Each stage holds only its own stage's data; anything from an earlier stage is reached by pointer on the shared reference ID. A renderer looks up a citation; it does not receive one.
- No checklist of what may cross is written or owed; the rule is structural, enforced by schema shape, not by a gate.
- A view is a caller: when retiring a copy, grep `sqlite_master` as well as the tree, and treat a 0-row object as unproven, not clean.
- Stage list in this entry ("research → evidence → synthesis → specification → render") superseded within slice by 2026-08-25 (L1006).
Open: none.

### 2026-08-24 — The clue store exists to be copied out of [L919-L936]
Owner words: "The clues table is a historical artifact. The DOIs it contains are expected to be used by the researcher and, if the researcher deems that DOI to be relevant, then it will write that DOI into the new correct evidence sources table. This means that whenever the new correct evidence sources table duplicates the DOI from the clues table, it simply means that the clues table was useful. We do not care about information in the clues table being duplicated. We just want to shortcut research time because we've already found so many sources."
In force:
- Same DOI in `source_locators` and `evidence_sources`: fine, not a defect.
- Same fact written into two tables within the live pipeline: defect — point, do not copy.
- Same DOI under different reference IDs: defect (two identities for one source); R9a/R9b detect it.
- `source_locators` is exempt permanently; do not spend effort normalising its case-drifted DOIs.
Open: none.

### 2026-08-24 — Applicability is an output, never an input; research the full cross-product [L941-L974]
Owner words: "Every research slug gets cross-referenced against a population code, access need or ICF code because there is always the chance that there is an unexpected connection between them. If we only link our taxonomy to research slugs by what seems obvious, we may miss evidence." / "Until we have secured an astounding body of evidence and synthesized that work while cross-referencing against our populations/access needs/ICFs, we are not able to define these connections — we are waiting until we have finished our syntheses to ensure we define them with evidenced justification, not presuppositions."
In force:
- `item_population_links` edges are findings produced downstream and justified by evidence; writing them first is forbidden presupposition.
- Zero `item_population_links` before synthesis is the correct state; nothing is owed.
- D-0165 (population-taxonomy pass) does not block research; every "blocked by D-0165" note is void.
- Every slug is searched against every population / access need / ICF code; the frame is the full cross-product, pulled as ICF and access-need codes WITH names, never bare codes.
- Pointer-correct shape for recording cross-product coverage: a junction on `exec_id` (mirroring `search_admissions`), never a copied code on the row.
Open:
- [OPEN] `search_executions` carries no population/access-need/ICF column, so cross-product coverage is unrecordable and ungateable as the schema stood (GAP-B01-003). [CHECK: may since be resolved]
[CHECK] CLAUDE.md §6 (outside slice) records an owner ruling of 2026-08-27 "overruling DR-2026-08-24 §2.4": the crossing is judgment's output (harvest at evidence, adjudicate at judgment). That bears directly on "output of synthesis" here.

### 2026-08-25 — Scratchpads are committed, not accumulated [L978-L1002]
Owner words: "ensure that we are always committing our scratchpads to the repository so that we actually have a surface to review… committed regularly enough that they do not [get] impacted [by compaction]."
In force:
- Commit the scratchpad at every natural break (finished investigation, batch step, migration emitted, answer given to the owner), not once at session end; the interval that matters is elapsed work.
- Never wait for a session record to exist; if no session directory exists, create it and commit into it.
- `governance: session command log [YYYY-MM-DD HH:MM]` is a complete commit message.
- `scratchpad/**/commands.jsonl` is exempt from `retired_vocabulary` (`retired-vocabulary.yaml`).
Open: none.

### 2026-08-25 — Pipeline stages: research → evidence collection → judgment → synthesis → render [L1006-L1054]
Owner words: "research → evidence collection → judgment → synthesis → render" / "that works for me"
In force:
- Five stages: research → evidence collection → judgment → synthesis → render. Supersedes the 2026-08-24 stage list.
- `judgment` is its own stage; determination is not folded into synthesis. `specifications` is a table `judgment` writes, not a stage.
- Ratifies the spine of `DR-2026-07-13-pipeline-contract` as declared in `governance/pipeline-contract.yaml`, with stage 2 named "evidence collection", not bare "collection".
- Substrate (vocabularies and registries: `items`, `populations`, `slugs`, `terms`, `access_needs`, crossing maps) is not a stage; it is the layer all stages point into. Table-to-stage assignments must be re-derived against the stages before being relied on.
- Re-entrancy holds: a walk may re-enter any stage; each stage's tables still carry only their own facts.
Open:
- [OPEN] Stage-2 identifier rename (`collection` → evidence collection) in `pipeline-contract.yaml`, `tools/pipeline_completeness.py` and the dashboard — a caller sweep under rule 4, tracked, not done.
[CHECK] CLAUDE.md §3 (outside slice) renders a later spine from `pipeline-contract.yaml`: base -> research -> evidence -> judgment -> synthesis -> specification -> render (owner formulation 2026-08-27), with `specification` as a stage. Adjudicator to rank by date.

### 2026-08-25 — Supersession record: pipeline smoke test (single-session scope) [L1058-L1099]
Owner words: "run a smoke test on the pipeline from start to finish… ensure that you attempt to run all skills/tools, including those that may not be explicitly built yet… ensure that you run every skill/tool/hook/script/etc by stage" / "use Fable 5 read-only to investigate the consequences of each step… you are auditing Sonnet 5's output by contextualizing it against the repository's doctrine/mission/pipeline."
In force:
- The supersession of the 2026-08-19 adversarial-review RULE applied to `session_2026-08-25-pipeline-smoke-test-mobility` only and its purpose only; it is spent.
- The 2026-08-19 RULE is not amended. A future session may not cite this record to authorise a critique of a plan, census, register or another pass. It is not a licence to audit prose.
- The next adversarial pass owed remains the one on batch 1's admitted rows, under the 2026-08-19 RULE unchanged. [CHECK: likely stale]
Open: none.

### 2026-08-25 — Person-side demand layer named `icf_demands`; not folded into `access_needs` [L1103-L1142]
Owner words: none quoted (owner ruling recorded without quotation) — recorder entry, not owner words.
In force:
- The layer formerly called `axes` is named `icf_demands` (`icf_demands.demand_code`; correspondingly `item_demand_links`, `population_demand_map`, `access_need_demand_map`, `slugs.serves_demands`, `situations.attaches_demands`). Supersedes §R8's replacement wording "ICF-anchored access needs" (name already taken).
- "Axis" is descriptive vocabulary, never a domain identifier (§R8 item 1 stands).
- Do not fold `icf_demands` into `access_needs`: `icf_demands` anchors ICF b + d (person's functional demand, carries `mechanism`); `access_needs` anchors ICF e (what the environment must do, carries `design_obligation`); the map is many-to-many. The split is the social model in the schema.
- Ambulant and wheeled movement are alternatives, not orthogonal, and on ramp gradient their demands are opposed — relevant to the permitted-umbrella test's "opposed or orthogonal" distinction.
- ACTION: (1) use `icf_demands` and its codes WITH names, never bare codes (the 2026-08-18 rule stands); (2) do not fold the two layers; cite this record if asked; (3) the rename is a D-SCHEMA migration with a full caller sweep across four tables, six columns, a blocking check (`validate_axes.py`) and tracked files — scoped, owner-gated, not to be attempted piecemeal (§R8 item 3 stands).
Open:
- [OPEN] Execution of the rename migration.

---

Slice stats: entries read 141; entries reduced to nothing in force 2; entries tagged [STATUS UNCERTAIN] 7; lines read 1-1145.
