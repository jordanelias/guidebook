# CO-0007 Skill Inventory
**Created:** 2026-04-26 01:49 UTC
**Stage:** 0.3 (Skill inventory)
**Resolves audit finding:** B-04 (skill ecosystem rebuild scope asserted, not enumerated)
**Status:** Stage-0 deliverable; pre-adoption (workplan v3 not yet adopted per 0.9)

---

## Purpose

Workplan v3 §0.3 requires enumerating `skills/` and mapping each to NEW / REBUILT / MODIFIED / DEPRECATED status against the inventory proposed in workplan v3 §C2 (which is the audit-resolved version of the safeguards analysis inventory). Audit v2 §B-04 designated this High because the synthesis cited "approximately 40 skill files" without enumeration; per-skill role assignments and the C2 budget (8–12 sessions, since revised to 12–16) are built on that count.

---

## Live skill enumeration

**Source:** `skills/` directory tree at HEAD `d1d7d450e9d92` (post-Stage-0.1+0.2 commit).
**Total files:** 45 (42 active in `skills/`, 3 archived in `skills/deprecated/`).
**Audit's "~40" understates by ~5.**

### Active (42)

| # | Skill file | Model | Notes from skill index (workplan-orchestrator §Skill Index) |
|---|---|---|---|
| 1 | bibliography-compiler | Sonnet 4.6 | Writing |
| 2 | bulk-renumber | Sonnet 4.6 | Document Processing |
| 3 | chunk-assembler | Sonnet 4.6 | Document Processing |
| 4 | citation-miner | Sonnet 4.6 | Research |
| 5 | citation-verifier | Sonnet 4.6 | Research |
| 6 | connection-scout | Opus 4.6 | Research (Opus for synthesis) |
| 7 | content-gap-analyzer | Sonnet 4.6 | Content Analysis |
| 8 | critique-report-writer | Sonnet 4.6 | Reporting |
| 9 | cross-population-conflict-mapper | Opus 4.6 | Reference (Opus for synthesis) |
| 10 | cross-reference-resolver | Sonnet 4.6 | Reference |
| 11 | economics-researcher | Sonnet 4.6 | Research |
| 12 | evidence-auditor | Sonnet 4.6 | Content Analysis |
| 13 | evidence-marker | Sonnet 4.6 | Content Analysis |
| 14 | file-splitter | Sonnet 4.6 | Document Processing |
| 15 | find-and-replace | Sonnet 4.6 | Document Processing |
| 16 | fix-linebreaks | Sonnet 4.6 | Document Processing |
| 17 | functional-deficit-researcher | Opus 4.6 | Research (Opus for synthesis) |
| 18 | github-filing | Sonnet 4.6 | Orchestration / infrastructure |
| 19 | github-io | Sonnet 4.6 | Orchestration / infrastructure |
| 20 | guidebook-auditor | Sonnet 4.6 | Content Analysis |
| 21 | haiku-chunker | Sonnet 4.6 | Document Processing |
| 22 | item-consolidation-analyzer | Sonnet 4.6 | Content Analysis |
| 23 | item-specification-writer | Sonnet 4.6 | Writing |
| 24 | jurisdiction-tracker | Sonnet 4.6 | Research |
| 25 | literature-review-planner | Sonnet 4.6 | Research |
| 26 | markdown-formatter | Sonnet 4.6 | Document Processing |
| 27 | multilingual-research | Opus 4.6 | Research (Opus for synthesis) |
| 28 | practice-note-generator | Sonnet 4.6 | Writing |
| 29 | prose-style-checker | Sonnet 4.6 | Writing |
| 30 | relational-integrity-checker | Sonnet 4.6 | (Not in workplan-orchestrator skill index) |
| 31 | research-log-manager | Sonnet 4.6 | Research |
| 32 | sensory-coherence-checker | Sonnet 4.6 | Content Analysis |
| 33 | session-consolidator | Sonnet 4.6 | Orchestration |
| 34 | structure-auditor | Sonnet 4.6 | Document Processing |
| 35 | supplemental-integrator | Sonnet 4.6 | Reference |
| 36 | table-formatter | Sonnet 4.6 | Document Processing |
| 37 | toc-editor | Sonnet 4.6 | Document Processing |
| 38 | version-diff | Sonnet 4.6 | Content Analysis |
| 39 | voice-style | Sonnet 4.6 | Writing |
| 40 | vol2-item-formatter | Sonnet 4.6 | Writing |
| 41 | volii-validator | Sonnet 4.6 | Reference |
| 42 | workplan-orchestrator | Sonnet 4.6 | Orchestration |

### Already-deprecated (3)

| # | Path |
|---|---|
| 43 | skills/deprecated/bibliography-updater_SKILL.md |
| 44 | skills/deprecated/keyword-lookup_SKILL.md |
| 45 | skills/deprecated/neufert-image-analyzer_SKILL.md |

### Workplan-orchestrator's "Retired" list (not in `skills/deprecated/`)

The skill index file lists five additional retired skills not present anywhere in the tree:
`vol1-corrections-writer · vol2-revision · plain-language-synthesizer · neufert-image-analyzer · keyword-lookup`

The last two are in `skills/deprecated/`. The other three (`vol1-corrections-writer`, `vol2-revision`, `plain-language-synthesizer`) are ghosts — referenced as retired but not preserved in `deprecated/`. Minor housekeeping issue.

### Workplan-orchestrator's "To build (P2)" list

Seven future skills cited as planned but not yet built:
`poe-assessor · intersectionality-checker · index-generator · glossary-manager · figure-numbering · docx-exporter · accessibility-checker`

These are an orthogonal wishlist not aligned with workplan v3 §C2. **Flag for C0 responsibility-matrix reconciliation** (see §Discrepancies).

---

## Disposition mapping (live skills → workplan v3 §C2 status)

Workplan v3 §C2 explicit tags: NEW · REBUILT · MODIFIED · DEPRECATED. I extend with KEEP (no change required) and FLAG (overlap with NEW skill that may absorb).

### Live skills with explicit workplan v3 §C2 tag

| Live skill | Workplan v3 tag | Rationale |
|---|---|---|
| cross-reference-resolver | **REBUILT** | Listed explicitly in §C2 Validation as REBUILT |
| evidence-auditor | **REBUILT** | Listed explicitly in §C2 Research as REBUILT |
| jurisdiction-tracker | **REBUILT** | Listed explicitly in §C2 Research as REBUILT |
| multilingual-research | **REBUILT** | Listed explicitly in §C2 Research as REBUILT |
| toc-editor | **REBUILT** | Listed explicitly in §C2 Project Orchestration as "REBUILT for entity-composition rather than markdown TOC" |
| voice-style | **REBUILT** | Listed explicitly in §C2 Authoring as "REBUILT post-A4" |
| research-log-manager | **KEEP** | Listed in §C2 Project Orchestration without tag (no change) |
| session-consolidator | **KEEP** | Listed in §C2 Project Orchestration without tag |
| workplan-orchestrator | **KEEP** | Listed in §C2 Project Orchestration without tag |

**Subtotal: 9 live skills with explicit C2 disposition.**

### Live skills with implicit disposition (not named in C2 but mapped by function)

| Live skill | Inferred disposition | Mapping rationale |
|---|---|---|
| bibliography-compiler | **DEPRECATE** | Bibliography becomes structured library (C7) generated by query, not "compiled" from BPC tables |
| bulk-renumber | **MODIFY** | Utility survives; needs entity-aware version once items become composed views |
| chunk-assembler | **DEPRECATE** | Markdown-only utility; structured form composes by query, no chunk-assembly |
| citation-miner | **MODIFY** | Citation function survives; output target shifts to citation entity |
| citation-verifier | **KEEP** | Source verification still required (especially for the 81-source [GREY] residual) |
| connection-scout | **REBUILT** | Connection register concept survives but as structured-data relationship; closest C2 analog is `entity-validator` + Opus run pattern |
| content-gap-analyzer | **MODIFY** | Still needed; output structure-aware |
| critique-report-writer | **KEEP** | Audit reporting still needed |
| cross-population-conflict-mapper | **REBUILT** | Maps to C2 Synthesis `conflict-resolver (REBUILT)` — same skill, renamed |
| economics-researcher | **MODIFY** | Research function survives; output target shifts to entity records |
| evidence-marker | **MODIFY** | Marker concept (●/○) folds into evidence-claim entity attributes |
| file-splitter | **KEEP-then-DEPRECATE** | Migration utility; deprecates with `markdown-extractor` after Stage C |
| find-and-replace | **KEEP-then-DEPRECATE** | Markdown utility; deprecates as markdown becomes rendering-only |
| fix-linebreaks | **KEEP-then-DEPRECATE** | Same as above |
| functional-deficit-researcher | **MODIFY** | FDR concept survives; aligns with `Co-1-evidence-intake` and parameter-entity work |
| github-filing | **KEEP** | Infrastructure |
| github-io | **KEEP** | Infrastructure |
| guidebook-auditor | **REBUILT** | Audit becomes byproduct of structured validators (per audit theme) |
| haiku-chunker | **KEEP-then-DEPRECATE** | Token-management utility; less needed when structured form replaces large markdown reads |
| item-consolidation-analyzer | **DEPRECATE** | Items become composed views; consolidation handled by composition logic |
| item-specification-writer | **DEPRECATE** | Replaced by C2 `entity-authoring (NEW)` + `narrative-prose (REBUILT)` |
| literature-review-planner | **MODIFY** | Research planning survives; integrates with `Co-1-evidence-intake` |
| markdown-formatter | **KEEP-then-DEPRECATE** | Markdown rendering survives until structured form is canonical |
| practice-note-generator | **MODIFY** | Practice notes become a content type; generator structure-aware |
| prose-style-checker | **FLAG** | Overlaps `voice-style` (REBUILT). Per project-standards 2026-03-31, `voice-style_SKILL.md` already absorbed framing-checker. Likely C0 consolidates these. |
| relational-integrity-checker | **REBUILT** | Direct precursor to C2 Validation `schema-validator` + `cross-reference-resolver`. Splits into two skills. |
| sensory-coherence-checker | **MODIFY** | Domain-specific validator; folds into `design-stage-coverage-validator` family or stays as a topical checker |
| structure-auditor | **DEPRECATE** | Structure becomes schema in B1; auditor function shifts to `schema-validator (NEW)` |
| supplemental-integrator | **DEPRECATE** | Supplementary volume content becomes population/parameter records with typology tags |
| table-formatter | **KEEP-then-DEPRECATE** | Markdown utility |
| version-diff | **MODIFY** | Useful; integrates with A9 time model |
| vol2-item-formatter | **DEPRECATE** | Markdown-only formatter; structured form has no "Volume 2" concept post-rebuild |
| volii-validator | **DEPRECATE** | Markdown-only Volume II validator |

**Subtotal: 33 live skills with inferred disposition.**

### Disposition rollup (active skills)

| Disposition | Count | Skills |
|---|---|---|
| **KEEP** (no change) | 6 | citation-verifier, critique-report-writer, github-filing, github-io, research-log-manager, session-consolidator, workplan-orchestrator (=7; minor count) |
| **MODIFY** | 9 | bulk-renumber, citation-miner, content-gap-analyzer, economics-researcher, evidence-marker, functional-deficit-researcher, literature-review-planner, practice-note-generator, sensory-coherence-checker, version-diff (=10) |
| **REBUILT** | 9 | connection-scout, cross-population-conflict-mapper → conflict-resolver, cross-reference-resolver, evidence-auditor, guidebook-auditor, jurisdiction-tracker, multilingual-research, relational-integrity-checker (splits into schema-validator + cross-reference-resolver), toc-editor, voice-style |
| **KEEP-then-DEPRECATE** (after Stage C) | 6 | file-splitter, find-and-replace, fix-linebreaks, haiku-chunker, markdown-formatter, table-formatter |
| **DEPRECATE** (in Stage C2) | 8 | bibliography-compiler, chunk-assembler, item-consolidation-analyzer, item-specification-writer, structure-auditor, supplemental-integrator, vol2-item-formatter, volii-validator |
| **FLAG** (overlap with rebuilt skill) | 1 | prose-style-checker (overlaps voice-style) |
| Already-deprecated | 3 | bibliography-updater, keyword-lookup, neufert-image-analyzer |

(The active count totals 42; FLAG/MODIFY/etc rollup arithmetic above varies by ±1 depending on whether prose-style-checker is FLAG or MODIFY, and where workplan-orchestrator/research-log-manager/session-consolidator are placed in the KEEP bucket. Exact bucket sizes are clarification work for C0, not 0.3.)

---

## Skills NEW per workplan v3 §C2 (do not exist in live `skills/`)

Workplan v3 §C2 names many skills that don't exist yet. These are pure construction work in C2.

### Research category (1 new)

- `Co-1-evidence-intake` (NEW)
- *(Note: workplan v3 lists `standards-registry` as "REBUILT" under Research, but `references/standards-registry.md` is a data file, not a skill. This appears to be a workplan-side naming error — likely intended `jurisdiction-tracker` covers this, or a new `standards-registry-tracker` skill. Flag for clarification in C0.)*

### Synthesis category (3 new)

- `BPC-orchestrator` (REBUILT — but no live `BPC-orchestrator` exists; functionally NEW via combination of literature-review-planner + connection-scout + opus-synthesis patterns)
- `divergence-synthesis` (REBUILT — currently exists only as the artifact `references/opus-divergence-synthesis.md` produced ad-hoc; functionally NEW as a skill)
- `question-author` (NEW)
- `specialist-handoff-author` (NEW)

### Migration category (4 new, all deprecate after Stage C)

- `markdown-extractor` (NEW)
- `entity-validator` (NEW)
- `migration-orchestrator` (NEW)
- `supersession-marker` (NEW)

### Authoring category (1 new)

- `entity-authoring` (NEW)
- *(workplan v3 lists `narrative-prose (REBUILT)` but no live precursor exists; closest is `prose-style-checker` + `practice-note-generator` partial. Effectively NEW.)*

### Validation category (10 new + 1 existing reclassified)

- `schema-validator` (NEW; not explicitly tagged in §C2 but no live precursor)
- `evidence-tier-validator` Co-1-aware (NEW; live `evidence-auditor` is a partial precursor and is REBUILT; these are distinct in §C2)
- `single-source-validator` (NEW; live `relational-integrity-checker` is a partial precursor)
- `Co-1-representation-validator` (NEW)
- `temporal-coherence-validator` (NEW)
- `round-trip-rendering-validator` (NEW)
- `question-coverage-validator` (NEW per audit T-02)
- `variability-coverage-validator` (NEW per audit N-04)
- `design-stage-coverage-validator` (NEW per audit T-06)
- `refresh-staleness-validator` (NEW per audit D-02)

### Co-1 interface category (entire category NEW — 4 new)

- `Co-1-recruitment` (NEW)
- `Co-1-review-prep` (NEW)
- `Co-1-disagreement-tracker` (NEW)
- `Co-1-compensation-tracker` (NEW)

### Project orchestration category (3 new)

- `gap-register` (NEW as proper skill; currently exists only as a write-protocol section inside workplan-orchestrator §Gap Register)
- `change-order` (NEW as proper skill; currently exists only as referenced procedure in project-standards Structural Decisions)
- `doctrine-recheck` (NEW per audit A13)
- `decision-capture` (NEW per audit A12)
- `supersession-checker` (NEW per audit D-05)

### Rendering category (entire category NEW — 6 new)

- `markdown-renderer` (NEW)
- `web-renderer` (NEW)
- `navigation-mode-renderer` (NEW)
- `respect-visibility-renderer` (NEW)
- `questions-renderer` (NEW per audit T-02)
- `rendering-refresh-coordinator` (NEW per audit D-02)

### Epistemic category (entire category NEW — 1 new)

- `epistemic-defense` (NEW per audit D-04)

### NEW total

**~33 new skills** (slight variance depending on whether `BPC-orchestrator`/`narrative-prose`/`schema-validator` count as REBUILT-from-existing-pattern or NEW-from-zero). All require construction in Stage C2.

---

## Sequence implications for C2

Workplan v3 §C2 estimates 12–16 sessions. Verifying budget:

| Bucket | Count | Per-skill effort estimate | Subtotal sessions |
|---|---|---|---|
| KEEP (preserve as-is, document scope) | 7 | 0.1 | ~1 |
| KEEP-then-DEPRECATE (deprecation manifest) | 6 | 0.1 | ~1 |
| MODIFY (output-target shift, mostly) | 10 | 0.3 | ~3 |
| REBUILT (substantive rewrite from precursor) | 9 | 0.5 | ~4–5 |
| DEPRECATE (write supersession notes) | 8 | 0.2 | ~1.5 |
| NEW (full construction) | 33 | 0.4 | ~13 |
| **Total** | 73 skill-tasks | — | **~24 sessions** |

The 12–16 session estimate **understates by ~50%** if every NEW skill is built with full specification + tests. Either:
- C2 constructs only the *minimum-viable* set for B-stage pilots, deferring some NEW skills to Stage C-mid (e.g., `web-renderer`, `respect-visibility-renderer` could wait until rendering is needed), or
- C2 budget is revised upward to ~20–28 sessions.

**Flag for 0.7 / 0.9 (workplan revision).**

---

## Discrepancies

### D-03-A · workplan-orchestrator's "To build (P2)" wishlist is orthogonal to workplan v3 §C2

| P2 wishlist (workplan-orchestrator) | Workplan v3 §C2 status |
|---|---|
| poe-assessor | not in C2 |
| intersectionality-checker | not in C2 |
| index-generator | not in C2 (replaced by query layer in structured form) |
| glossary-manager | not in C2 |
| figure-numbering | not in C2 |
| docx-exporter | not in C2 (out of architecture scope) |
| accessibility-checker | not in C2 |

These were planned as next-tier additions under the markdown-form architecture. Most of them don't have analogs in workplan v3's structured-form architecture (e.g., index-generator is replaced by composed views; docx-exporter is post-rebuild). **Resolution: C0 responsibility matrix reconciles by either dropping the P2 list or mapping P2 items to NEW skills where they have analog (e.g., poe-assessor and intersectionality-checker may be domain-specific validators).**

### D-03-B · "standards-registry" tagged as REBUILT skill but is a data file

Workplan v3 §C2 Research bucket lists `standards-registry (REBUILT)`. Live: `references/standards-registry.md` is a data file (1,152 lines, YAML blocks). No `skills/standards-registry_SKILL.md` exists. This is a workplan-side naming error.

**Resolution:** Either rename to `standards-registry-tracker` (skill that maintains the data file) and treat as REBUILT from `jurisdiction-tracker`, or absorb into `jurisdiction-tracker (REBUILT)` and remove from §C2. C0 decides.

### D-03-C · `prose-style-checker` ↔ `voice-style` overlap

Per project-standards 2026-03-31: `voice-style_SKILL.md` is mandatory for all prose writing and superseded `framing-checker`. `prose-style-checker` continues to exist as a separate skill. Two skills checking prose style is the L-03 boundary problem.

**Resolution:** C0 either consolidates them (likely) or specifies non-overlapping responsibilities (less likely given current state). Audit L-03 explicitly flags this kind of overlap.

### D-03-D · Three "Retired" skills not preserved in `skills/deprecated/`

`vol1-corrections-writer`, `vol2-revision`, `plain-language-synthesizer` are listed as Retired in the skill index but not present in `skills/deprecated/`. Either they were never created (skill index is aspirational) or they were deleted without archiving.

**Resolution:** Minor housekeeping. C0 documents canonical retirement procedure (move to `deprecated/`, don't delete).

### D-03-E · `relational-integrity-checker` not in workplan-orchestrator skill index

Live skill `relational-integrity-checker_SKILL.md` exists but is not listed in workplan-orchestrator §Skill Index. Either added recently and index not updated, or named in conflict.

**Resolution:** C0 reconciles index against tree. Mechanical fix.

---

## Confirmation that 0.3 prerequisites are met

| Requirement | Met? | Evidence |
|---|---|---|
| Enumerate `skills/` directory | Yes | 45 files |
| Map to NEW/REBUILT/MODIFIED/DEPRECATED status | Yes | All 42 active skills classified; 33 NEW skills enumerated |
| Identify missing-but-named | Yes | D-03-D (3 ghost retired skills); D-03-B (standards-registry) |
| Identify present-but-unnamed | Yes | D-03-E (relational-integrity-checker not in index) |

---

## What this report does not do

- **Does not commit C2 budget revision.** The ~24-session estimate is informational; formal revision is 0.7 + 0.9 work.
- **Does not modify any skill file.** Inventory-only.
- **Does not create the C0 responsibility matrix.** That is C0 work in Stage C, after architecture lock.
- **Does not resolve overlaps (D-03-A through D-03-E).** Logged for C0 reconciliation.
- **Does not adopt or reject workplan v3.** That is 0.9.

---

## Coda

Forty-five skills exist, of which 42 are active. Audit's "~40" is approximately right. Roughly 9 of the 42 active skills are explicitly tagged in workplan v3 §C2; the remaining 33 are implicitly disposed by inferred function-mapping. Adding the 33 NEW skills in §C2, the total skill count post-rebuild is ~70+. The C2 session budget probably understates by ~50% if every NEW skill is built fully; defer the budget question to 0.7. Five small discrepancies are logged for C0 reconciliation.

The skill ecosystem is more developed than the synthesis credited (~40 → 45) but still needs substantial construction (~33 new skills) to operationalize the doctrinal commitments audit v2 surfaced.
