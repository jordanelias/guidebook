# BPC Rewrite Workplan — Integrity Restoration with Reasoning Transparency

**Generated:** 2026-05-11 (Opus 4.7, session_2026-05-11e)
**Predicate:** 8-phase audit (Phases 1–7 executed; this is the Phase 8 deliverable)
**Scope:** 95 BPC files + 245 connections + 661 evidence sources + 1408 source-slug links + 91 items
**User decisions locked (this session):**
- Coverage scope: **19 languages × 46 jurisdictions** (full protocol per `multilingual-research_SKILL.md`)
- Reasoning doc location: **new directory** `references/bpc-reasoning/<slug>.md` (do not extend `search-log/`)
- Phase sequencing: **strict sequential B before E** (verify all 661 sources first, then rewrite)
- Citation mining: explicitly noted as separate Phase B7 deliverable
- Terminology: **disability-centric framing throughout**; "most inclusive code" retained unambiguously meaning "lowest barrier for persons with disabilities"

---

## 0. Executive summary

The guidebook's evidence and synthesis infrastructure is well-designed at the schema level but ~95% unpopulated in practice. Of the protocol-required infrastructure:

| Required by protocol | Actual state | Gap |
|---|---|---|
| Every source confirmed real | 86% AUTHOR-TITLE-ONLY, 2% VERIFIED | Verification not done |
| Two-field encoding (tier + evidence_type) | tier 99%, evidence_type 3% | Encoding half-implemented |
| Co-1 six required fields populated | All ~0–5% | Co-1 protocol unimplemented |
| 19 languages × 46 jurisdictions | 14 langs × 24 juris in DB | Coverage axes incomplete |
| Sonnet never writes synthesis | Existing syntheses compliant; my drafts violated | Protocol holds; this session's drafts retracted |
| `synthesis_attribution_required` populated | 0/661 | Field exists, never used |
| `derivation_chain` populated | 0/661 | Field exists, never used |
| Citation mining run per BPC | 0 rows in `citation_mining` table | Mining never executed |
| Connections describe what they connect | 244/245 empty `description` | Bulk-created stubs |

This workplan rehabilitates the evidence base first (Phase B), then rewrites every BPC and connection with a public reasoning document showing every source, every inference, every gap. The reasoning documents are the primary deliverable; the rewritten BPCs are derived from them.

The workplan does NOT try to make synthesis judgments faster. It is explicit about which work is mechanical (source verification, mapping table construction) versus which requires Opus synthesis sessions. The mechanical work is sized in source-units; the synthesis work is sized in slug-units with explicit gates.

---

## 1. Locked operational rule for synthesis

Every BPC reasoning document must apply the 9-step rule for each parameter where ≥3 jurisdictions specify different values:

1. **Parameter declaration**: name, units, accessibility direction (LOWER / HIGHER / POPULATION-DEPENDENT — declare explicitly).
2. **Per-population worst-case user**: list every affected population; for each, name the most-constrained user. If populations conflict, log per-population separately. **Do not arbitrate cross-population conflicts inline.**
3. **Jurisdiction comparison table**: every surveyed jurisdiction's value evaluated at its code's worst-case point in the code's structure (single-value codes: the single value; length-tiered: most permissive run length; height-tiered: most permissive height; element-tiered: most permissive element). For cross-jurisdiction comparison only.
4. **Lowest-barrier code(s) per population**: the jurisdiction-evaluated worst-case value closest to the access direction. If populations conflict, one entry per population.
5. **Evidence cited**: Tier 1 (clinical) / Co-1 (lived experience per CRPD Art 4.3) / Tier 2 (NGO/DPO guidelines) / Co-2 (OT professional CPGs) / Tier 3 (systematic reviews, meta-analyses) that supports or exceeds the lowest-barrier code. **Tier 4 / Tier 5 excluded at this step** — they belong to the jurisdiction comparison in step 3.
6. **Guidebook chosen value per population**: may match or exceed the lowest-barrier code.
7. **Rationale**: historical context of permissive codes; clinical basis for the chosen value.
8. **Trade-offs**: cost, retrofit feasibility, named cross-population conflicts.
9. **Cross-population conflict flag**: if multiple populations have different chosen values, queue for `cross-population-conflict-resolutions` BPC arbitration.

The 9-step rule is the contract for every parameter in every BPC. Reasoning documents that do not apply all 9 steps to a parameter are incomplete.

---

## 2. Per-BPC reasoning-document template

**Location:** `references/bpc-reasoning/<slug>.md`
**One file per slug.** ACTIVE slugs only initially; MERGED/STUB slugs require redirect-only stubs.

```markdown
# Reasoning: <slug>

**BPC file:** references/bpc/<topic>/<slug>.md
**BPC population:** <POP1, POP2, ...>
**Generated:** YYYY-MM-DD by session_<id>
**Status:** DRAFT | OPUS-PENDING | COMPLETE
**Opus session ref:** <session_id or N/A>

---

## A. Evidence inventory

### A.1 Sources formally linked to this slug (from source_slug_links)
| REF-ID | Local-ID | Authors | Year | Title | Tier | Evidence type | DOI/PMID | metadata_quality | verification_status | Read directly? | Date read | Method |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| REF-NNNNN | XYZ-NN | ... | ... | ... | N | clinical | 10.XXXX/... | COMPLETE | VERIFIED | YES | YYYY-MM-DD | web_fetch / PDF / DOI resolver |

### A.2 Sources cited in this BPC but NOT formally linked
List every author/title cited in the BPC markdown that lacks a corresponding source_slug_links row. Each must be either added to source_slug_links + evidence_sources, or struck from the BPC.

### A.3 Practitioner / secondary sources used during Tier 2 multilingual search
| Language | URL | Date accessed | Type (gov-summary / industry-blog / news / association / academic-press / etc.) | Used for claim | Verified against primary text? |
|---|---|---|---|---|---|

### A.4 Primary regulatory documents retrieved
| Jurisdiction | Instrument | Citation | URL/DOI | Date retrieved | Section(s) read |
|---|---|---|---|---|---|

### A.5 Gaps in the evidence inventory
For each gap: subject, why it matters, attempted resolutions, current status (OPEN / CLOSED-DELETED / CLOSED-RESOLVED), adversarial-protocol fields (confidence_interval, shift_conditions, named_dissenter, falsification_condition).

---

## B. Per-parameter reasoning (apply 9-step rule)

### B.1 Parameter: <name> (<units>)

**Step 1 — Direction**: LOWER-is-better | HIGHER-is-better | POPULATION-DEPENDENT (explain)

**Step 2 — Per-population worst-case user**:
- Population <POP1>: most-constrained user = <description>
- Population <POP2>: most-constrained user = <description>
- Cross-population conflict: <YES/NO>; if YES, log per-population entries below, do not reconcile inline

**Step 3 — Jurisdiction comparison (worst-case-point evaluation)**:
| Jurisdiction | Instrument | Scope | Structure type | Worst-case value | Direct-text verified? | Source REF-ID |
|---|---|---|---|---|---|---|

`Scope` column values (per Decision 2): `statutory-code` | `national-framework` (Tier 5) | `international-standard` (Tier 4) | `national-recommended` | `provincial-local`. Tier 4 international standards (e.g., ISO 21542) and Tier 5 national frameworks (e.g., BS 8300-2 Annex G) are grouped with statutory codes for jurisdiction-comparison purposes only; they are NOT cited as independent evidence in Step 5.

**Step 4 — Lowest-barrier code per population**:
- For <POP1>: <jurisdiction> at <value>
- For <POP2>: <jurisdiction> at <value>

**Step 5 — Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence supporting or exceeding**:
| REF-ID | Tier | Evidence type | Citation | Key finding | Supports / Exceeds the lowest-barrier code? | Direct-text verified? |
|---|---|---|---|---|---|---|

**Step 6 — Guidebook chosen value per population**:
- <POP1>: <value> (rationale tag)
- <POP2>: <value> (rationale tag)

**Step 7 — Rationale**:
Historical context of permissive codes; clinical basis for chosen value. Where Sonnet inference is used, mark [SONNET-INFERENCE]; where Opus arbitration was applied, mark [OPUS-DECISION session_<id>].

**Step 8 — Trade-offs**:
Cost; retrofit feasibility; named cross-population conflicts.

**Step 9 — Cross-population conflict flag**:
If <POP1> and <POP2> chosen values differ → QUEUE for `cross-population-conflict-resolutions` BPC. Otherwise → N/A.

### B.2 Parameter: <next parameter>...

---

## C. Synthesis claims that did NOT survive evidence review

For each retracted claim from the prior 2026-03-30 synthesis or this session's drafts:
- Original claim
- Source previously cited
- Why retracted (e.g., secondary source only, primary text retrieval failed, contradicted by Tier 1 evidence)
- Replacement claim or NO REPLACEMENT (gap)

---

## D. Cross-references

- BPC dependencies (other BPCs cited): <list with rationale>
- Items derived from this BPC: <list of item_codes>
- Connections involving this slug: <list of CON-NNNN>
- Gaps registered: <list of gap IDs>

---

## E. Adversarial protocol pass (per standing rule #7)

For every closed gap and every synthesis claim:
- Confidence interval
- Shift conditions (what evidence would shift CI up/down)
- Named dissenter (specific contrary view OR "NONE FOUND" with logged search queries)
- Falsification condition (specific finding that would invalidate)

---

## F. Provenance trail

- Every source's `derivation_chain` field populated
- Every Co-1 source's six required fields populated (A5 governance/co1-operational.md)
- Every synthesis decision tagged with Opus session ID
- `synthesis_attribution_required` populated for Co-1 sources where substantial synthesis occurred
```

---

## 3. Per-connection reasoning-document template

**Location:** `references/connection-reasoning/<con-id>.md` (new directory)
**One file per CON-NNNN.** 245 connections to be processed.

```markdown
# Reasoning: CON-NNNN

**Status:** CONSUMED | CONSUMED-DEFERRED | PENDING | CLOSED
**Confidence:** HIGH | MODERATE | SPECULATIVE
**Connection type:** CROSS-POPULATION | CROSS-ITEM | COMPOUND-INTERACTION | METHODOLOGY
**Filed in:** <topic_directory>
**Opus reviewed:** YES | NO + reason

---

## A. What this connection asserts
Free-text description (≥1 sentence, ≤500 chars). Must answer: "When doing X, also consider Y, because Z."

## B. Targets verified
| Target string (from connection_targets) | Resolves to (item_code / slug / TBD) | Verified to exist? |

## C. Evidence supporting the connection
Tier 1–3 sources only (per step 5 rule).

## D. Confidence rationale
Why HIGH / MODERATE / SPECULATIVE. Must reference evidence in §C.

## E. Opus review decision
If status was PENDING and now resolved, log the Opus session ID and the decision rationale.

## F. Application
If status is CONSUMED, log which item/spec/BPC consumed it (session ref).
```

---

## 4. Phase A — Foundation work (prerequisite for all later phases)

| Sub-phase | Action | Effort estimate | Gate to next |
|---|---|---|---|
| A.1 | Reconcile `slugs` table (currently 81 rows) against `bpc_metadata` (97 rows) and filesystem (95 files). Populate missing 14 slug rows. | 2–3 hours | All 95 filesystem BPCs have a row in `slugs` |
| A.2 | Populate `slugs.merged_into` for every MERGED filesystem BPC. Identify all merges by reading BPC files for "Status: MERGED" header. | 1–2 hours | All MERGED files reflected in `slugs.merged_into` |
| A.3 | Build language↔jurisdiction mapping table. Schema: `lang_jur_map(language, jurisdiction, role)` where role ∈ {PRIMARY, SECONDARY, COLONIAL}. E.g., (EN, US, PRIMARY), (EN, UK, PRIMARY), (EN, IE, PRIMARY), (EN, CA, PRIMARY), (EN, AU, PRIMARY), (EN, NZ, PRIMARY), (EN, IN, SECONDARY), (EN, ZA, SECONDARY). | 4–6 hours | Mapping table covers all 19 langs × all 46 juris with role assigned |
| A.4 | Expand `search_languages` schema/data to 19 languages: add AR, HI, ID, SW, BN as NOT-RUN for all 81 slugs (5 × 81 = 405 new rows). Mark with `[UNVERIFIED-TERMS]` per skill's CO-0005 caveat. | 2 hours | search_languages has 19 × 81 = 1539 rows |
| A.5 | Expand `search_coverage` schema/data to 46 jurisdictions: add AT, BE, BG, CH (already there?), CL, CO, CR, EC, EG, ET, GH, GT, ID (already?), IN (already?), KE, MA, MX, NG, PE, PH, TH, TZ, UY (22 new jurisdictions). Mark missing as NOT-RUN. | 3 hours | search_coverage has 46 × 81 = 3726 rows |
| A.6 | Populate `items.bpc_source_slug` for all 91 items. Cross-reference items table category/name against BPC content. | 4–5 hours | All 91 items have a non-empty bpc_source_slug |
| A.7 | Create `references/bpc-reasoning/` directory + commit `_template.md` (the template in §2 above). | 1 hour | Directory exists, validate_reasoning.py written |
| A.8 | Create `references/connection-reasoning/` directory + commit `_template.md` (the template in §3 above). | 30 min | Directory exists |
| A.9 | Write `scripts/validate_reasoning.py` — validates that each reasoning document has all required sections, all 9 steps populated for each declared parameter, no inline cross-population reconciliation. | 4–6 hours | Script passes on the template; integrated into pre-commit |
| A.10 | Write `scripts/audit_evidence_metadata.py` — reports `metadata_quality` and `verification_status` distributions per slug. Will be used as a Phase B progress monitor. | 2–3 hours | Script runs against current DB and produces baseline report |
| A.11 | **Native-language keyword compendium verification** (Decision 1 LOCKED) — for AR, HI, ID, SW, BN added in A.4: per language retrieve concept-vocabulary compendium for accessibility/disability terminology (native synonyms, regulatory terms, advocacy organization names, native equivalents of MOB/VIS/DEAF/DEM/AUT/NDV etc.). Each compendium validated against ≥1 native-speaker source (academic glossary, advocacy organization publication, government regulatory text in that language). Until validation recorded, all retrievals from that language flag `[UNVERIFIED-TERMS]`. Per-language deliverable: `references/keyword-compendiums/<lang>.md`. | 5 langs × 8–12 hours = 40–60 hours | All 5 languages have a committed compendium + validation source(s) |
| A.12 | **Phase G output generator built early** (Decision 3 LOCKED) — write the bespoke guidebook-generator script in `scripts/generate_parts.py` with stub mode (renders whatever BPCs are currently rehabilitated) and full mode (requires all 95 ACTIVE BPCs at COMPLETE). Generator runs idempotent; output → `parts/v10/`. Generator must read from SQLite + BPC markdown + reasoning docs and emit a single consistent guidebook structure per `architecture/page-templates.md`. | 30–50 hours | Generator runs in stub mode and produces non-empty parts/v10/ from any subset of rehabilitated BPCs |

**Phase A total effort:** ~95–145 hours (was 25–35; A.11 adds 40–60, A.12 adds 30–50). **Phase A gate to B:** all foundation tables consistent; reasoning template committed; keyword compendiums for AR/HI/ID/SW/BN drafted; output generator in stub mode operational.

---

## 5. Phase B — Evidence base rehabilitation (must complete before Phase E begins)

| Sub-phase | Action | Source count | Effort estimate | Gate |
|---|---|---|---|---|
| B.0 | **Retract pre-rehabilitation syntheses** (Decision 5 LOCKED) — for every BPC currently bearing `opus_synthesis: YES [OPUS-SYNTHESIS]` from the 2026-03-30 round (~30 BPCs estimated): insert a banner at the top of the BPC file reading `**SYNTHESIS VALIDITY:** PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION (banner added YYYY-MM-DD by session_<id>; will be removed when Phase E.2g re-runs Opus synthesis with rehabilitated evidence)`. Also update `bpc_metadata.evidence_state` to `RETRACTED-PRE-REHAB`. The original synthesis text remains in the file (historical record) but no downstream consumer should cite it during the rehabilitation window. | ~30 BPCs | 2 hours total | Banner present on every PRE-REHAB BPC; bpc_metadata flag set |
| B.1 | Triage 661 sources by current `metadata_quality`. Output: priority queue. | 661 | 4 hours | Triage report committed |
| B.2 | Resolve 567 AUTHOR-TITLE-ONLY sources. For each: web search by author+year+title; identify DOI/PMID; populate `doi`/`pmid`; upgrade `metadata_quality` to COMPLETE; populate `evidence_type` (clinical / co1 / co2 / sr_meta / standard_eb / national_fw / code / grey). Sources not findable after 2 search attempts → mark CLOSED-DELETED per standing rule #1. | 567 | ~15 min each = ~140 hours | All 567 either upgraded or CLOSED-DELETED |
| B.3 | Resolve 68 GREY sources (incomplete metadata). For each: attempt primary-text retrieval (DOI resolver, publisher site, archive); if successful upgrade to COMPLETE, else mark CLOSED-DELETED. | 68 | ~30 min each = ~34 hours | All 68 either upgraded or CLOSED-DELETED |
| B.4 | Resolve 7 NULL `metadata_quality` sources. | 7 | ~30 min each = ~3.5 hours | All 7 classified |
| B.5 | Resolve 1 PMID-ONLY source. | 1 | ~15 min | Source upgraded |
| B.6 | Populate `evidence_type` field for all surviving sources (currently 3% populated). Use the 9-value enum from `governance/evidence-methodology.md`. | ~660 | ~5 min each = ~55 hours | `evidence_type` 100% populated |
| B.7 | Populate `verification_status` for all surviving sources. VERIFIED requires direct-text retrieval and field-by-field check; UNVERIFIED-1 / UNVERIFIED-CLOSED per A5 protocol. | ~660 | ~10 min each = ~110 hours (a substantial portion fall to UNVERIFIED-1) | `verification_status` 100% populated |
| B.8 | Populate Co-1 six required fields for all `evidence_type = co1` sources (per `governance/co1-operational.md` §A5): `tier`, `evidence_type`, `co1_provenance`, `co1_source_type`, `verification_status`, `synthesis_attribution_required`. | Co-1 subset (~50 sources estimated) | ~20 min each = ~16 hours | All Co-1 fields populated |
| B.9 | Populate `derivation_chain` for every source that synthesized a guidebook claim. Currently 0/661. | ~200 sources | ~10 min each = ~33 hours | `derivation_chain` populated for cited sources |
| B.10 | Populate `synthesis_attribution_required` for Co-1 sources where substantial synthesis occurred. Currently 0/661. | Co-1 subset | ~15 min each = ~12 hours | Field populated |
| B.11 | **Citation mining** — run `citation-miner` skill per slug for every BPC with ≥1 source. Currently 0 rows in `citation_mining` table; target ~95 rows minimum (one per active slug). Each mining run produces: backward references (cited by this source), forward references (citing this source), connections produced. | 95 slugs | ~1 hour each = ~95 hours | `citation_mining` table populated; new source candidates added to `evidence_sources` |
| B.12 | Add new Tier 2 jurisdictional regulatory instruments to `evidence_sources`. The 14-language Tier 2 work this session identified ~50 instruments (DPCM, BR18, TEK17, GB 50763, etc.); each must be entered with `metadata_quality: TIER2-PRACTITIONER-SUMMARY` and `verification_status: UNVERIFIED-1` until primary-text retrieval upgrades them. | ~50 | ~15 min each = ~12 hours | Tier 2 regulatory instruments are evidence_sources rows |

**Phase B total effort:** ~510 hours = ~13 weeks of sustained 40-hour work (one person), or ~6 weeks at 80-hour weeks (e.g. multiple sessions per day with verification gates).

**Phase B critical gate to Phase E:** No BPC can be rewritten until its formally-linked sources are at metadata_quality ≥ COMPLETE and verification_status = VERIFIED or UNVERIFIED-1 (not NULL). Reasoning documents written against unverified sources fail validate_reasoning.py.

**Optimization option:** Phase B can be parallelized by source-type. Tier 6 codes (89 sources) require regulator-website retrieval; Tier 1 clinical (101 sources) require DOI lookup; Tier 5 frameworks (121 sources) require institutional repository retrieval. These three tracks can run concurrently.

---

## 6. Phase C — Coverage axis expansion to 19 × 46

| Sub-phase | Action | Effort | Gate |
|---|---|---|---|
| C.1 | Mark all current `search_languages` and `search_coverage` rows as `protocol_state: PRE-EXPANSION` (add column or use notes). This preserves the existing 14×24 work as historical evidence. | 1 hour | New column added |
| C.2 | Per Phase A.4: AR, HI, ID, SW, BN added to `search_languages` schema and existing slugs as NOT-RUN. | (Done in A.4) | |
| C.3 | Per Phase A.5: 22 new jurisdictions added to `search_coverage` as NOT-RUN. | (Done in A.5) | |
| C.4 | Decision per slug: re-survey at 19×46 immediately, or queue for batched re-survey? Recommendation: **batched re-survey** triggered by per-slug Phase E rewrite. Each slug that goes through Phase E has its multilingual research run at 19×46 as part of E.2b. | 0 hours (decision documented) | Decision logged |
| C.5 | Build `lang_jur_map` table (per A.3) and use it during multilingual research to cross-check coverage. E.g., if EN is SEARCHED but the US-specific source for a US jurisdiction claim isn't logged, flag the lang-jurisdiction mismatch. | (Built in A.3) | Mapping table used by Phase E |

**Phase C effort:** Roughly 2 hours discrete + folded into Phase A and Phase E.

---

## 7. Phase D — Connection rehabilitation

| Sub-phase | Action | Connection count | Effort | Gate |
|---|---|---|---|---|
| D.1 | Triage 245 connections by status + populated fields. Output: priority queue. | 245 | 3 hours | Triage report |
| D.2 | For each of 244 connections with empty `description`: read `connection_targets` rows; reconstruct what the connection asserts; write reasoning document per §3 template. | 244 | ~30 min each = ~122 hours | Each connection has a reasoning doc |
| D.3 | Verify every `connection_targets.target` string resolves to an actual `item_code` (in `items` table) or an actual `slug` (in `slugs` table) or is a free-text description. Currently targets are raw strings like `item:I-01`, `A-16`, etc. | 507 targets | ~5 min each = ~42 hours | Every target verified |
| D.4 | Apply Opus review to every PENDING connection (`opus_reviewed = 0`). Set `opus_reviewed = 1` if applicable; set `confidence` accordingly. | ~PENDING subset | ~15 min each | All PENDING reviewed or moved to CONSUMED |
| D.5 | Archive CONSUMED connections (move to a historical view; preserve in DB but stop showing in primary queries). | ~CONSUMED subset | 2 hours | Archive view created |
| D.6 | Populate `connection_type` for all 244 currently-NULL connections. Enum: CROSS-POPULATION / CROSS-ITEM / COMPOUND-INTERACTION / METHODOLOGY. | 244 | ~10 min each = ~41 hours | `connection_type` 100% populated |

**Phase D total effort:** ~210 hours = ~5 weeks at 40-hour work.

**Phase D depends on Phase B** (cannot fully describe a connection if the underlying sources are unverified). However, D.1, D.3, D.5 are mechanical and can run in parallel with Phase B.

---

## 8. Phase E — Per-BPC rewrite pipeline (only after Phase B complete)

For each of 95 BPCs, the rewrite pipeline is:

| Step | Action | Effort per slug | Notes |
|---|---|---|---|
| E.1 | **Pre-conditions check**: all formally-linked sources have `verification_status = VERIFIED` or `UNVERIFIED-1`; `metadata_quality ≥ COMPLETE`; `evidence_type` populated. | 15 min | If pre-conditions fail, slug is blocked until Phase B resolves |
| E.2a | **Reasoning doc generation** — create `references/bpc-reasoning/<slug>.md` from template. Populate Section A (Evidence inventory) by joining `source_slug_links`, `evidence_sources`, `search_languages`, `search_coverage`. | 1 hour | Mostly mechanical |
| E.2b | **Multilingual research at 19 × 46** — run `multilingual-research` skill to fill the expanded coverage axes. For each language/jurisdiction not yet SEARCHED, conduct a native-language search; log new sources to `evidence_sources` with `verification_status: UNVERIFIED-1` initially. | 8–24 hours depending on slug complexity | Largest variable in Phase E |
| E.2c | **Cross-jurisdictional comparison** — apply 9-step rule per parameter. Build the Step 3 comparison table. Identify the lowest-barrier code per population. | 2–4 hours per parameter | Multi-parameter slugs scale linearly |
| E.2d | **Cross-population conflict logging** — for each parameter that has population conflicts, log per-population entries separately. Do NOT reconcile inline. Queue conflict for `cross-population-conflict-resolutions` BPC. | 30 min per conflict | Per-population logging only |
| E.2e | **Adversarial protocol pass** — for every closed gap and every synthesis claim, populate `confidence_interval`, `shift_conditions`, `named_dissenter`, `falsification_condition`. | 1 hour per slug typical | Standing rule #7 |
| E.2f | **Queue for Opus session** — once Sonnet work in E.2a–E.2e is complete, the reasoning doc is queued for Opus synthesis. Sonnet does NOT write best-practice synthesis (per skill protocol). | 0 hours Sonnet; ~2–4 hours Opus per slug | Opus-only step |
| E.2g | **BPC update after Opus session** — Opus writes the synthesis sections of the BPC (Best-practice synthesis, Consensus findings, Divergent findings, Opus synthesis note). Cross-reference to reasoning doc. | 2 hours Opus | Opus session output |
| E.2h | **Validation** — run `validate_bpc.py` and `validate_reasoning.py` against the updated files. | 15 min | Must pass |

**Per-slug effort estimate (Sonnet + Opus combined):**
- High-coverage slug (60+ sources, multiple parameters): 18–28 hours
- Mid-coverage slug (20–40 sources, 2–3 parameters): 8–14 hours
- Low-coverage slug (≤20 sources, 1 parameter): 4–8 hours
- Zero-source slug (currently): 6–10 hours (multilingual research adds sources from scratch)

**Phase E total effort estimate** (95 slugs, weighted distribution):
- ~25 high-coverage × 22 hours = 550 hours
- ~40 mid-coverage × 11 hours = 440 hours
- ~30 low-coverage × 6 hours = 180 hours
- **Total: ~1170 hours = ~29 weeks at 40h/week**

**Phase E sequencing**:
- Process by priority queue (see Appendix A): ACTIVE slugs with P1 gaps first; population-general slugs (DEAF, MOB, DEM, VIS, NDV) before specific-feature slugs; cross-population conflict BPCs LAST (need other BPCs done first to arbitrate).

---

## 9. Phase F — Items pipeline

| Sub-phase | Action | Count | Effort | Notes |
|---|---|---|---|---|
| F.1 | Populate `items.bpc_source_slug` for all 91 items. (Done in A.6) | 91 | (Done in A.6) | |
| F.2 | Run `spec_value_probes` for items currently without a probe (73 of 91 lack any probe row). | 73 | ~30 min each = 36 hours | Increases spec_value_probes coverage to 100% |
| F.3 | Run `item-specification-writer` skill on each item after its source BPC is updated in Phase E. | 91 | ~1–2 hours per item = ~135 hours | Items synced with updated BPCs |
| F.4 | Run `validate_items.py` and `validate_jurisdiction.py`. | 1 hour | | Must pass |

**Phase F total effort:** ~172 hours = ~4 weeks at 40h/week.

**Phase F depends on Phase E** (items derive from BPCs).

---

## 10. Phase G — Output regeneration and audit

| Sub-phase | Action | Effort | Notes |
|---|---|---|---|
| G.1 | Generate `parts/v10/` guidebook content from rehabilitated BPCs + items + connections. Currently parts/v10/ is empty (0 bytes). | 40–60 hours | Requires assembly skill not currently inventoried; may need bespoke tooling |
| G.2 | Run consolidated audit: `validate_bpc.py --all`, `validate_db.py`, `validate_audit_runs.py`, `validate_cross_refs.py`, `validate_evidence_state.py`, `validate_temporal.py`. All must return 0 issues. | 8 hours | Final integrity gate |
| G.3 | Adversarial spot-check per standing rule #7: minimum 1 closed gap per slug verified against primary text. For 95 slugs that's 95 verifications. | ~30 min each = ~48 hours | Standing rule compliance |
| G.4 | Cross-population synthesis pass — now that per-population entries are logged in each BPC, run a dedicated Opus session over the `cross-population-conflict-resolutions` BPC to arbitrate every flagged conflict. | ~20–40 hours Opus | The deferred reconciliation from §1 step 9 |

**Phase G total effort:** ~120–160 hours = ~3–4 weeks at 40h/week.

---

## 11. Aggregate effort and timeline

| Phase | Effort (hours) | Critical path |
|---|---|---|
| A. Foundation | 25–35 | Yes (blocks all) |
| B. Evidence rehabilitation | 510 | Yes (blocks E) |
| C. Coverage axis expansion | 2 (folded into A) | Embedded |
| D. Connection rehabilitation | 210 | Partial (parallel with B) |
| E. Per-BPC rewrite | 1170 | Yes (blocks F, G) |
| F. Items pipeline | 172 | After E |
| G. Output regeneration | 120–160 | Last |
| **Total** | **~2200–2300 hours** | |

**Calendar estimate at sustained 40 h/week single-person:** ~55 weeks = ~13 months.

**Realistic estimate with session-based work pattern (≤4 effective hours/session, ~5 sessions/week):** ~110–120 weeks = ~2.3 years.

**Compression options:**
- Parallel B+D tracks save ~5 weeks
- Skip MERGED/STUB slugs in Phase E (drops 95 → ~70 ACTIVE) saves ~25 weeks
- Defer 5 newly-added languages (AR/HI/ID/SW/BN) save ~15 weeks
- Defer 22 newly-added jurisdictions save ~30 weeks
- Combined compression: ~75 weeks down from 110

---

## 12. Risk register

| Risk | Severity | Likelihood | Mitigation |
|---|---|---|---|
| Sources unfindable after 2 search attempts (per standing rule #1) → many CLOSED-DELETED | MEDIUM | HIGH (especially for older AUTHOR-TITLE-ONLY) | Track CLOSED-DELETED rate; if >30%, escalate to library / database access strategy |
| Opus session capacity insufficient for ~95 slug synthesis sessions | HIGH | MEDIUM | Pre-schedule Opus sessions; batch by topic-directory |
| Persistence-failure on long sessions (per preferences `<persistence_safeguards>`) | MEDIUM | HIGH | Inline checkpoints every ~10 sources processed; per-slug commits to GitHub |
| Cross-population conflict arbitration becomes self-referential (BPC A conflicts with BPC B, both flag for cross-pop, neither can complete) | MEDIUM | MEDIUM | Sequence cross-pop BPC LAST; require all single-pop BPCs done first |
| Multilingual research at 19 langs × 46 jurisdictions overwhelms a single slug pass (874 cells per slug × 95 slugs = 83,030 cells) | HIGH | HIGH | Mark "PROVISIONAL-NOT-SEARCHED" for non-priority jur-langs; iterate over time; do not block Phase E on full coverage |
| Reasoning documents become too long to be useful (>5000 lines per slug for high-coverage) | LOW | MEDIUM | Split per-parameter sections into linked sub-documents if any one exceeds 2000 lines |
| Adversarial protocol fields become rote-filled rather than rigorous | HIGH | MEDIUM | Independent spot-check sample of 5% per session; named_dissenter must cite specific contrary author/source |

---

## 13. Acceptance criteria

A rewritten BPC is COMPLETE only when:

1. Every formally-linked source has `metadata_quality = COMPLETE` and `verification_status ∈ {VERIFIED, UNVERIFIED-1}` (no NULL, no UNVERIFIED-CLOSED, no CLOSED-DELETED).
2. The reasoning document exists, passes `validate_reasoning.py`, and applies all 9 steps to every parameter where ≥3 jurisdictions specify different values.
3. Every Co-1 source has all six required fields populated.
4. Every gap registered has all four adversarial-protocol fields populated.
5. Every jurisdictional claim cites a primary-text REF-ID, not a practitioner summary.
6. Every cross-population conflict is logged per-population without inline reconciliation.
7. The BPC file itself has the Opus synthesis sections populated (Best-practice synthesis, Consensus findings, Divergent findings, Opus synthesis note) with `opus_synthesis: YES [OPUS-SYNTHESIS]` and a valid `opus_session` ref.
8. `validate_bpc.py` passes.
9. The reasoning document and the BPC cross-reference each other.

A rewritten connection is COMPLETE only when:

1. `description` is non-empty and follows "When doing X, also consider Y, because Z" pattern.
2. `connection_type` is one of CROSS-POPULATION / CROSS-ITEM / COMPOUND-INTERACTION / METHODOLOGY.
3. Every `connection_targets.target` resolves to a real item_code, slug, or labelled free-text.
4. `confidence` is justified by Tier 1–3 evidence cited in the reasoning doc.
5. `opus_reviewed = 1` (or status moved to CONSUMED with session_applied ref).
6. The reasoning document exists and passes `validate_reasoning.py`.

Project-level acceptance:

1. All 95 ACTIVE BPCs meet the BPC criteria above.
2. All 245 connections meet the connection criteria above.
3. All 91 items have `bpc_source_slug` populated and ≥1 `spec_value_probe`.
4. All 661 sources have `metadata_quality ≥ COMPLETE`, `evidence_type` populated, `verification_status` ∈ {VERIFIED, UNVERIFIED-1, CLOSED-DELETED}.
5. `citation_mining` table has ≥1 row per ACTIVE slug.
6. `lang_jur_map` table exists and is referenced by all multilingual queries.
7. `parts/v10/` directory is non-empty (guidebook output generated).
8. All `validate_*.py` scripts pass.
9. Adversarial spot-check: 5% random sample of closed gaps verified against primary text.

---

## Appendix A — Per-slug priority order for Phase E

**Tier 1 (rewrite first):** ACTIVE slugs with P1 OPEN gaps and item dependencies.

| Slug | Reason | Source count |
|---|---|---|
| (To be derived from Phase A audit of `gaps` and `source_slug_links`; current P1 count = 8) | | |

**Tier 2 (population-general):** Foundation BPCs that other BPCs depend on.
- DEAF.md, MOB.md, DEM.md, VIS.md, NDV.md, NDV-MH.md, IntD.md, DBL.md (all have 0 linked sources currently — Phase E will populate)
- ALL-ENV.md, ALL-FW.md, ALL-ROOMS.md (cross-cutting)
- NEU.md, OFS.md, PAIN.md, NEU.md

**Tier 3 (high-coverage feature BPCs):**
- accessibility-feature-market-value-uplift-framing (68 sources)
- threshold-door-hardware (64 sources)
- room-acoustic-performance (62 sources)
- mental-health-built-environment (50 sources)
- mobility-built-environment (48 sources)
- accessible-bathroom-and-grab-bar (46 sources)
- cognitive-wayfinding-design (44 sources)
- residential-entry-and-threshold (42 sources)

**Tier 4 (mid-coverage):** 32 slugs with 20–40 sources.

**Tier 5 (low-coverage):** ~30 slugs with ≤20 sources.

**Tier 6 (cross-population conflict resolution):** LAST. Cannot complete until per-population entries from all relevant BPCs are logged.

---

## Appendix B — Concurrent-work guidance

Phase B and Phase D have independent parts that can run concurrently:
- Phase B.2 (AUTHOR-TITLE-ONLY upgrade) and Phase D.3 (target verification) touch different tables and can run in parallel sessions.
- Phase A.6 (items↔BPC linking) and Phase B.6 (evidence_type population) are independent.

Phase E slugs in different topic_directories can be rewritten in parallel sessions if:
- Their formally-linked sources have completed Phase B verification
- They have no PENDING connection dependencies on each other

---

## Appendix C — Session-handoff protocol

Each session that touches this workplan must:
1. Open by reading the current state of the affected tables (`bpc_metadata`, `evidence_sources`, `connections`, etc.)
2. Update the Phase tracker (suggested location: `audits/bpc-rewrite-phase-tracker.md`)
3. Commit any reasoning-document changes to `references/bpc-reasoning/` or `references/connection-reasoning/`
4. Log session completion in `sessions/<session_id>.md` with: phases touched, sources processed, slugs completed, gaps registered, gates passed
5. Run `validate_*.py` scripts before closing

---

## Appendix D — Decisions log (LOCKED 2026-05-11)

| # | Decision | Locked outcome | Workplan section affected |
|---|---|---|---|
| 1 | AR/HI/ID/SW/BN native-language keyword verification | **In-scope** for this workplan, not a separate workstream. New Phase A.11 sub-task. Each language requires keyword compendium retrieval + native-speaker validation; `[UNVERIFIED-TERMS]` flag per CO-0005 until validation recorded. | §4 Phase A; §11 effort table |
| 2 | Tier 4 (international standards) and Tier 5 (national frameworks) treatment | **Grouped with statutory codes** in Step 3 jurisdiction comparison. NOT used as Step 5 evidence citation. Each Tier 4/5 entry gets its own row in the jurisdiction comparison table with `scope` column ∈ {international / national-framework / statutory-code / national-recommended / provincial-local}. | §1 operational rule clarification; §2 template Step 3 |
| 3 | Phase G output generator | **Built early** as new Phase A.12. Rationale: incremental testing during Phase E catches generator bugs against real rehabilitated BPCs; deferring to Phase G concentrates discovery risk at the end. Generator runs in stub mode initially, gains capability as BPCs are completed. | §4 Phase A; §10 Phase G updated |
| 4 | MERGED / STUB slug handling | **MERGED slugs:** minimal redirect-only reasoning docs (~30 lines: redirect target, merge reason, date, session ref). **STUB slugs:** gap-naming reasoning docs explaining why stub + what would need to exist for it to be ACTIVE. Neither runs the full 9-step rule. | §8 Phase E sub-pipeline; §13 acceptance criteria |
| 5 | Pre-Phase-E synthesis retraction | **Immediate retraction** upon entering Phase B (not when Phase E reaches each slug). Add `synthesis_validity: PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION` banner to every BPC with `opus_synthesis: YES [OPUS-SYNTHESIS]` from the 2026-03-30 round. Banner remains until Phase E.2g overwrites. Rationale: preserves historical record while preventing downstream consumers from citing unverified claims during the ~13-month rehabilitation. | §5 Phase B new sub-task B.0; §13 acceptance criteria |

---

## Appendix E — Supersession map: workplan reconciliation 2026-05-11

This workplan is the **sole authoritative content workplan** for the project as of 2026-05-11. Every other file in `workplan/` has one of four dispositions: SUPERSEDED-BY-THIS-WORKPLAN, SUBORDINATE-TO-PI-STANDING-RULE, ABSORBED, or HISTORICAL-COMPLETED. This appendix is the canonical list.

### E.1 SUPERSEDED — fully replaced by this workplan (no further reference needed for forward work)

| File | Was | Now superseded by |
|---|---|---|
| `workplan/workplan-co0007-v4.md` | OPERATIVE (Stage C1–C11 ACTIVE) | This workplan §Phase E. Stage A/B foundation work in v4 remains validly completed (~43 sessions consumed); only Stage C content scoping is replaced. |
| `workplan/workplan-reconciliation-2026-05-08.md` | Prior reconciliation map | This appendix E (E.1–E.5) replaces it. |
| `workplan/workplan-item-audit-pipeline-co0009.md` | PROPOSED (CO-0009) | This workplan §Phase F. Item audit pipeline runs after Phase E rehabilitates the source BPCs. |
| `workplan/co0008-scope-infrastructure-overhaul.md` | DRAFT (CO-0008) | This workplan §Phase A (foundation infrastructure work is folded into A.1–A.12). |
| `workplan/co0008-throughline-analysis.md` | DRAFT | Subsumed by Phase A foundation work. |
| `workplan/pi-update-co0008.md` | READY TO APPLY | PI v10.8 supersedes (v10.8 is the new live PI per `decisions/PI-update-needed.md`). |
| `workplan/pi-revision-co-paste-ready.md` | Paste-ready PI patches | PI v10.8 supersedes. |
| `workplan/multilingual-search-remediation.md` | Multilingual remediation plan | This workplan §Phase B + §Phase C (B7 citation mining + C coverage axis expansion to 19×46). |
| `workplan/workplan-jurisdiction-sweep.md` | Jurisdiction sweep workplan | This workplan §Phase C (coverage axis expansion to 46 jurisdictions). |
| `workplan/evidence-expansion-2026-04-03.md` | Evidence base expansion programme | This workplan §Phase B (evidence rehabilitation, 510-hour estimate). |
| `workplan/website-preparation.md` | Tactical reference subordinate to v4 | This workplan §Phase G (output regeneration). |
| `workplan/co0007-synthesis-workplan-2.md` | Stage 0.7 synthesis workplan | Foundation complete; superseded by this workplan for forward work. |

### E.2 SUBORDINATE — still active under PI v10.8 standing rules (sub-protocols supporting this workplan)

| File | Subordinate to | Role |
|---|---|---|
| `workplan/progressive-measurement-protocol.md` | PI v10.8 standing rule #8 | PMP walks for numerical-spec items. Required during Phase F (items pipeline). |
| `workplan/research-protocol-adversarial.md` | PI v10.8 standing rule #7 | Anti-consensus-bias research protocol. Required at every gap closure throughout all Phases. |
| `workplan/hook-workplan-guidebook.md` | PI v10.8 `<hooks_status>` | Engineering workplan for hook enforcement (level 0 → level 2 → level 3 promotion). Runs orthogonal to content phases. |

These three files are NOT superseded. They continue to govern their specific protocols.

### E.3 HISTORICAL-COMPLETED — Stage A / B foundation deliverables (preserve as record; no forward use)

| File | Status |
|---|---|
| `workplan/a1-a2-iteration-plan.md` | A1–A2 complete |
| `workplan/a4-part01-audit-2026-04-27.md` | A4 complete |
| `workplan/a5-handoff.md` | A5 handoff (Co-1 operational spec) — work absorbed into `governance/co1-operational.md` |
| `workplan/a6-handoff.md` | A6 handoff (Evidence methodology) — work absorbed into `governance/evidence-methodology.md` |
| `workplan/b1-derivation-framework.md` | B1 framework — superseded by adopted candidate |
| `workplan/b1-candidate-a-markdown-yaml.md` | B1 candidate eval — not adopted |
| `workplan/b1-candidate-b-relational.md` | B1 candidate eval — **adopted (relational schema chosen)** |
| `workplan/b1-candidate-c-graph.md` | B1 candidate eval — not adopted |
| `workplan/b1-candidate-d-hybrid.md` | B1 candidate eval — not adopted |
| `workplan/b1-comparative-scoring.md` | B1 scoring — work record |
| `workplan/b1-criteria-weighting.md` | B1 requirements lock — work record |
| `workplan/co0007-contamination-sample.md` | CO-0007 Stage 0 deliverable |
| `workplan/co0007-quantitative-verification.md` | CO-0007 Stage 0 deliverable |
| `workplan/co0007-session-grounding-report.md` | CO-0007 Stage 0 deliverable |
| `workplan/co0007-skill-inventory.md` | CO-0007 Stage 0 deliverable — superseded by `references/skill-registry.md` |
| `workplan/co0007-stage-0_5-decision-package.md` | CO-0007 Stage 0.5 decision materials |
| `workplan/co0007-stage-0_9-adoption-package.md` | CO-0007 Stage 0.9 adoption package |
| `workplan/co0009-phase0-handoff.md` | CO-0009 Phase 0 handoff |
| `workplan/phase1b-part01-s15-expansion.md` | Phase 1B draft (Part 1 §1.5 expansion) |
| `workplan/co0003-amendment-2026-03-28.md` | CO-0003 amendment record |
| `workplan/co0004-body-propagation.md` | CO-0004 body propagation work |
| `workplan/P1-D2-D3-co0004-remapping.md` | CO-0004 decision remapping |
| `workplan/slug-triage-2026-03-28.md` | Slug triage record (Phase 2A Session 4) |
| `workplan/v10-5_2026-03-29.md` | Already marked DEPRECATED (v10-5 of co0007) |
| `workplan/roadmap-2026-04-27.md` | Already marked DEPRECATED |
| `workplan/workplan-co0007-audit.md` | Already marked DEPRECATED (Stage 0 audit) |
| `workplan/workplan-co0007-synthesis.md` | Already marked DEPRECATED |
| `workplan/workplan-co0007-v3-amendments.md` | Already marked DEPRECATED |
| `workplan/workplan-co0007-v3.md` | Already marked DEPRECATED |

### E.4 DECISION-SUPPORT — not workplans; standalone analysis documents (preserve as-is)

These are not workplans and are not subject to supersession. They are decision records / analyses.

| File | Type |
|---|---|
| `workplan/placeholder-review-triage.md` | Decision-support |
| `workplan/gap-p1-reclassification-recommendation.md` | Decision-support (GAP-079 / GAP-CITE-01) |
| `workplan/external-review-queue.md` | Decision-support (external review prioritisation) |
| `workplan/external-review-outreach-drafts.md` | Application-ready artifact |
| `workplan/opa-adjudication.md` | OP-A adjudication (Part 5 §5.2 conflict resolution) — RESOLVED |
| `workplan/opb-adjudication.md` | OP-B adjudication (CON connection synthesis) |
| `workplan/opg-methodology-review.md` | OP-G methodology review (Part 3 §3.8/3.9) |
| `workplan/opus-missing-passes.md` | Opus synthesis queue tracker — referenced by Phase E.2f |
| `workplan/opus-synthesis-queue.md` | Opus synthesis queue tracker — referenced by Phase E.2f |
| `workplan/struck-claim-research-attempt_2026-05-01.md` | Research findings (struck claims) |
| `workplan/economics-audit-research-2026-05-03.md` | Interim research findings |

### E.5 Forward-work rule

For any session opening under PI v10.8, the operative workplan is **this document** (`audits/bpc-rewrite-workplan-2026-05-11.md`). Do not consult the files in E.1 except for historical context. The files in E.2 remain operative for their specific protocols and must be honoured. The files in E.3 and E.4 are records; consult only when investigating prior decisions.

If a session discovers a workplan-like file not classified above (created after 2026-05-11 11:00 UTC), default to: NOT-AUTHORITATIVE pending explicit adoption in a future PI revision.

---

**End of workplan.**

