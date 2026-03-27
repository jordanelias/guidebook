<!-- GOVERNED BY PROJECT INSTRUCTIONS — execution copy only. PI definition governs on conflict. -->

---
name: item-specification-writer
description: >
  Draft, revise, and audit item-level design specifications for any volume of the guidebook
  containing itemised provisions. Applies the three-tier design hierarchy, specification
  range doctrine, social model framing, and population code cross-referencing to every item.
  ALWAYS use this skill when asked to: write a new specification item, revise an existing
  item, draft evidence tables for items, write room or typology matrices, produce synthesis
  sections for a specification category, or produce any structured item-level content.
  Trigger on: "write the item", "draft the spec", "revise this item", "new specification",
  "item spec", "add a provision", "draft the category", "write the evidence table",
  "item-level content", "specification for [population] [building element]", or any task
  where the output is a structured design specification with a code, title, specification
  text, evidence basis, and population tags. Also trigger when revising existing items
  for evidence upgrades, framing corrections, or consolidation outputs.
---

**Model:** Sonnet 4.6 — judgment required for all evidence and framing decisions  
**Input:** item brief (code · title · population codes · evidence · typology scope) + section map  
**Output:** complete item block in guidebook format + evidence table + population tag table  
**Chunk ceiling:** ≤30 items per run. Full category → haiku-chunker first.

---

## Governing Principles

### Social Model (non-negotiable)
The built environment creates barriers. People are not the problem.  
- CRPD Articles 9, 19, and 30 govern all specification decisions.
- State the ideal built environment first. Note constraints only where genuinely necessary.
- Never: "to help users with X", "to accommodate disability". Always: "to remove the barrier", "to provide equivalent access".

### Three-Tier Design Hierarchy
Every item must identify which tier it serves and apply the tier's specification standard:

| Tier | Context | Specification standard |
|---|---|---|
| Tier 0: Universal Design, improvable floor | No particular disability population is a predominant user (e.g. public institutional spaces) | Above code minimum — executed in a way that allows tailoring and improvement for specific people as required |
| Tier 1: Population-Informed Inclusive Design | Identified disability population(s) most likely to use the building | Ranges; median is the population-informed default. Core question: what works best for this population? |
| Tier 2: Person-Specific Co-Design | Named client/person; specific building | Co-design: OT establishes functional capacity; client expresses own preferences. Specifications uniquely tailored to the person |

The Tier 1 range is the population evidence envelope. At Tier 2, co-design between OT and client resolves the specific value within that range.

### Specification Range Doctrine
Ranges appearing in specifications are not expressions of uncertainty. They are the mechanism that allows a single item to serve both Tier 1 and Tier 2 practice simultaneously.

- At Tier 1 (identified population): use the median value as the population-informed default.
- At Tier 2 (named person/client): the position within the range is determined through co-design — OT establishes functional capacity; client expresses own preferences. Both are required inputs.
- Never: "between X and Y" without specifying which end applies at which tier.
- Priority populations for range framing: MOB/AMB, MOB/UPL, OFS, and any population where functional variation is high.

---

## Item Format

Every item block follows this structure, in this order:

```markdown
### [CODE] [Title — Descriptive Only; No Values or Thresholds in Heading]

**Population codes:** [code list]  
**Typology:** Residential · Non-Residential · Both  
**Design stage:** [SD / DD / TA / Construction / Post-occupancy]

#### Specification

● or ○ [Ideal provision — state the best achievable outcome first]

● or ○ [Best practice — what this guidebook targets for new build]

● or ○ [Acceptable — where spatial or structural constraint exists; always specify what constraint justifies it]

● or ○ [Minimum — only where a hard floor is needed; note that this is a floor, not a target]

**Evidence markers (mandatory):** Every prescriptive sentence carries exactly one marker.
- **●** (filled circle) = evidence-based — at least one Tier 1–6 source directly supports this value
- **○** (empty circle) = inferred — derived from clinical reasoning, expert consensus, or extrapolation; gap disclosed
- Non-prescriptive sentences (rationale, context, cross-references) carry no marker.
- See `evidence-marker` skill for classification criteria and upgrade protocol.

#### Evidence basis

| Tier | Source | Claim supported |
|---|---|---|
| [1–6] | [Author, Year] | [Specific claim] |

#### Conflict notes
[Only where this item conflicts with a provision for another population code — name the conflict, state the resolution rule from §IV.2, and cross-reference the other item]

#### Cross-references
[Internal refs to related items, evidence annex entries, DAR register entries]

#### Retrofit note
**Retrofit:** [HIGH / MODERATE / LOW penalty] — see §8.4.[X]

#### Illustration
**[Illustration: to be provided]**
Remove this note only when an actual illustration is supplied. Every Part 7 item (including Appendix B and C items) is designed to be accompanied by a technical diagram, drawing, or illustration.
```

---

## K-Category Template (v10.1 addition — Sensory Environment)

Category K items address sensory environment specifications (lighting, acoustics, thermal, olfactory). K-items follow the standard item format above with these additions:

```markdown
### K-[NN] [Title — Descriptive Only]

**Population codes:** [code list — K-items typically affect NDV/SENS, NDV/AUT, DEM, VIS, DEAF, NEU]
**Typology:** Residential · Non-Residential · Both
**Design stage:** [SD / DD / TA / Construction / Post-occupancy]
**Sensory domain:** Acoustic · Visual · Thermal · Olfactory · Tactile · Multi-sensory

#### Specification
[Standard ●/○ marked specification sentences]

#### Sensory interaction notes
[Where this item's provision interacts with other sensory domains — e.g., acoustic treatment affecting thermal mass, lighting affecting NDV/SENS overstimulation. Cross-reference Part 8 §8.4 conflict resolutions where applicable.]

#### Evidence basis
[Standard evidence table]

#### Cross-population conflicts
[K-items frequently produce cross-population conflicts. Identify all known conflicts and cross-reference Part 8 §8.4 resolution entries. Flag unresolved conflicts for Part 8 development.]
```

K-category codes: K-01 through K-[NN]. Numbering is sequential within the category.

---

## Population Code Rules

- Apply all 11 population codes. Never collapse sub-codes.
- `●` = primary population (item primarily addresses this population's barriers)
- `○` = secondary population (item has secondary benefit)
- `—` = not applicable (no meaningful interaction)
- Where a population code produces a conflicting requirement: flag with `⚠ CONFLICT` and apply §IV.2 conflict priority rules.

**Canonical codes:** MOB (MOB/AMB, MOB/UPL) · VIS/vis · VIS/DEAF · NEU (NEU/PCS) · DEM · NDV (NDV/AUT, NDV/ADHD, NDV/SENS) · NDV/MH · PAIN · DBL · OFS (OFS/ME, OFS/POTS, OFS/MCAS)

BAR is not a main-taxonomy code. Large body size provisions belong in the supplementary volume. Do not add BAR items to the main specification library.

---

## Evidence Rules

- Every prescriptive claim carries a citation or evidence tier marker.
- Unsupported claims: flag `[UNSUPPORTED — citation required]`.
- Tier 1 (OT clinical systematic reviews): cite author-year + journal.
- Tier 2 (community/lived experience research): cite source + note it provides outcome criteria, not override.
- Tiers 3–6: cite source; note tier explicitly in evidence table.
- Single-source specifications: flag `[SINGLE SOURCE — Tier X protocol applies]`.
- Do not embed extended evidence rationale in the item body. Two sentences maximum: OT framework name + one-sentence claim. Extended rationale belongs in the evidence annex.

---

## Heading Rule

No values, ranges, or thresholds in item headings. The heading is a navigational label only.

✓ `### G-03 Grab Bar Provision in Accessible Bathrooms`  
✗ `### G-03 Grab Bars (32–45 mm Diameter, 200 kg Rated)`

---

## Sequencing Rule

Ideal → Best Practice → Acceptable → Minimum — at item level, in this order.  
Where only one tier is applicable, state that tier and omit the others.  
Never start with Minimum and work upward.

---

**Typology scope** (required on every item): Residential (dwellings, supported living, care homes) · Non-Residential (workplaces, healthcare, education, civic, retail, transport) · Both. Where specification differs by typology, use tiered sub-specifications rather than two separate items.

---

## Passes Required

**New items:** 3 passes — (1) draft, (2) framing-checker review, (3) evidence-auditor review.  
**Revised items:** 2 passes — (1) revision, (2) framing-checker spot-check.  
**Evidence upgrade only:** 1 pass — swap citation, re-run evidence-auditor.

---

## Escalation Triggers

Stop and confirm with user:

- Item requires original research that is not available in the evidence corpus — do not draft a specification without evidence; flag as `[EVIDENCE GAP — item cannot be specified without further research]`
- Item conflicts with a locked decision in `project-standards.md` — do not draft; flag the conflict
- Typology scope is unclear (item may apply differently in R vs NR but current scope is "Both") — confirm before drafting
- Population code produces an irresolvable conflict where no §IV.2 rule applies — escalate to workplan-orchestrator

---

**Preceded by:** `item-consolidation-analyzer` · `citation-verifier` (parallel)
**Feeds into:** `framing-checker` + `evidence-auditor` (after each pass) · `prose-style-checker` (before packaging) · `volii-validator` (after category complete)

---

## Source Citation Protocol (endnote system)

**Pre-step:** `research-log-manager RETRIEVE` for each relevant slug before writing. BPC `Key sources` list provides the REF-ID index.

**REF-ID markers:** Every prescriptive claim citing evidence carries `[REF:{slug}:{NN}]` inline. `{slug}` = BPC slug; `{NN}` = 01-indexed position in BPC Key sources. Multiple markers at one point for multi-source claims.

**Placement:**
- After claim, before punctuation.
- Every bullet with dimensional value, material requirement, or performance threshold needs ≥1 REF-ID. No source → `[UNSUPPORTED — citation required]`.

**Sources-cited table:** `#### Sources cited` after each item block:

```markdown
#### Sources cited

| REF-ID | Authors | Year | Title | Journal/Publisher | DOI/URL | Tier | Lang | Jurisdiction |
|---|---|---|---|---|---|---|---|---|
```

Min 2, max 12 sources per item. Every REF-ID ↔ sources-cited row bidirectional. Real sources only. Source not in BPC Key sources → flag `[NOT IN BPC — verify via citation-verifier]`. <2 verified → `[CITATION GAP — evidence-auditor referral required]`.

**Replaces Key citations** for new/revised items. Do not emit both. Legacy items retain `Key citations` until revised.

**Downstream:** `vol2-item-formatter` validates REF-ID ↔ sources-cited. `bibliography-compiler` compiles volume-end endnotes. `cross-reference-resolver` validates superscripts.

**Preceded by:** `item-consolidation-analyzer` · `research-log-manager RETRIEVE`
**Feeds into:** `vol2-item-formatter` → `framing-checker` + `evidence-auditor` → `prose-style-checker` → `volii-validator`
