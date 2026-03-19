# Format Rules
<!-- Managed by guidebook-auditor Mode A. GET before audit; PUT back after update. -->
<!-- Last backfilled: 2026-03-18 23:30 from Project Instructions + project-standards.md -->

---

## 1. Document Structure

### 1.1 Volume and Part Numbering
- Volumes: Roman numerals (I, II, III)
- Parts: Arabic numerals, sequential across all volumes (1–13)
- Sections: §[part].[section].[subsection] (e.g., §3.2.1)
- Item codes: category letter + two-digit number (e.g., A-01, B-03) — exempt from part renumbering
- Item code prefix: V2-P8-xx (canonical; V2-P4-xx deprecated)
- Supplementary Volume: Supp. Part 1–4 with §1.x–§4.x section coding, independent of main numbering

### 1.2 Heading Rules
- Headings: descriptive only — no values, ranges, or thresholds in heading text
- Heading hierarchy must be strictly nested (H1 → H2 → H3; no skips)
- No duplicate headings at the same level within a section

### 1.3 Prohibited Structural Elements
- BAR / Category J: not permitted in Volumes 1–3 (Supplementary Volume Supp. Part 4 only)
- BIO items: Appendix B only — not in Part 8 or inline specs
- TC items: Appendix C only — not in Part 8 or inline specs
- Supplementary Resources A and B: struck from Volume 2 body
- V2-PV-XX item codes: deprecated — replace on sight with V2-P8-XX

---

## 2. Prose Register

### 2.1 Voice
- Soft imperative subjunctive throughout: "to be", "not to exceed", "to provide"
- No direct commands ("must", "shall") except where citing statutory code language
- No passive constructions that obscure the design obligation

### 2.2 Sentence Rules
- ≤25 words per specification sentence
- One claim per sentence
- Every prescriptive claim carries citation, evidence tier marker, or `[UNSUPPORTED — citation required]`

### 2.3 Sequencing
- Specifications follow: Ideal → Best Practice → Acceptable → Minimum
- Tier identification required per item: Tier 0 / Tier 1 / Tier 2

### 2.4 Prohibited Language
- Medical model framing (deficits, impairments as primary lens)
- Universal design described as aspirational (it is the code floor)
- Inclusive design described as obligatory minimum (it is the positive aspiration)
- VIS/DEAF as a compound code (error — use VIS, DEAF, or DBL independently)

---

## 3. Population Codes

### 3.1 Canonical Main-Taxonomy Codes
| Code | Label |
|---|---|
| MOB | Mobility & Strength (MOB/AMB, MOB/UPL) |
| VIS | Visual impairment |
| DEAF | Deaf / hard of hearing / hearing device users |
| NEU | Neurological / ABI (NEU/PCS) |
| DEM | Dementia |
| NDV | Neurodivergence (NDV/AUT, NDV/ADHD, NDV/SENS) |
| NDV/MH | Mental health / PTSD / trauma |
| PAIN | Chronic pain / fibromyalgia |
| DBL | DeafBlind |
| OFS | Orthostatic & fatigue spectrum (OFS/ME, OFS/POTS, OFS/MCAS) |
| IntD | Intellectual disability |
| ALL | All disability categories |

### 3.2 Supplementary Codes (not main taxonomy)
CHD · LPA · EXH — Supp. Parts 1–3 only

### 3.3 Prohibited Codes
- BAR: not a main-taxonomy code; Supplementary Volume only
- VIS/DEAF: invalid compound — flag and split on sight
- V2-P8-J / Category J: invalid in Volumes 1–3

---

## 4. Evidence and Citation Formatting

### 4.1 Evidence Tier Markers
Every prescriptive claim must carry one of:
- `[Tier 1]` — OT clinical research, intervention-tested
- `[Co-1]` — Lived experience / participatory design (CRPD Art. 4.3)
- `[Tier 2]` — Disability-led NGO/DPO/advocacy guidelines
- `[Tier 3]` — Systematic review or meta-analysis
- `[Tier 4]` — International standard with evidence basis
- `[Tier 5]` — National beyond-code framework
- `[Tier 6]` — Statutory code (reference baseline only)
- `[UNSUPPORTED — citation required]` — no source available
- `[UNVERIFIED — DOI/URL required before publication]` — source not confirmed
- `[EXPERT CONSENSUS — March 2026]` — PAIN/OFS/DBL/IntD provisions without built-environment evidence base
- `[THIN BASE — <3 studies]` — insufficient evidence
- `[SYSTEMIC GAP — {description}]` — gap across all jurisdictions searched

### 4.2 Population-Specific Disclosure Requirements
- PAIN and OFS items: mandatory expert consensus disclosure note (full text per project-standards.md)
- DBL room matrix additions: `[EXPERT CONSENSUS — no standard; March 2026]`
- IntD room matrix additions: `[TIER 4-5; no quantified architectural standard in any jurisdiction; March 2026]`

### 4.3 Citation Format
- Inline: Author Year (doi:xx.xxxx/xxxxx)
- Unverified: append `[UNVERIFIED — DOI/URL required before publication]`
- After two failed independent search attempts: delete value; log CLOSED-DELETED in gap_register.md

---

## 5. Specification Range Formatting

### 5.1 Range Expression
- Ranges expressed as: `{lower}–{upper} {unit}` (en-dash, no spaces around dash)
- Median stated explicitly: `(median {value} {unit})`
- Tier context stated: Tier 1 → use median; Tier 2 → resolve through co-design

### 5.2 Three-Tier Identification
Each item must state which tier(s) it addresses:
- Tier 0: fixed value, no range
- Tier 1: range with stated median
- Tier 2: co-designed; resolves within Tier 1 range; DAR note mandatory

---

## 6. Table and Figure Rules

### 6.1 Table Format
- Pipe tables preferred for markdown
- Column headers: bold, sentence case
- No merged cells in markdown tables; use notes for spanning content
- Population matrix tables: population codes in row headers; spaces not permitted in code cells

### 6.2 Numbering
- Tables: Table [Part].[sequential] (e.g., Table 3.1)
- Figures: Figure [Part].[sequential] (e.g., Figure 3.1)
- Numbered sequentially within each Part; reset at each new Part

---

## 7. Cross-Reference Formatting

- Internal cross-references: `§[part].[section]` or `[Item code]` as appropriate
- Appendix references: `Appendix [letter]` (e.g., Appendix B, Appendix C)
- Supplementary volume: `Supp. Part [n] §[n.x]`
- Broken or unresolved cross-references: flag `[XREF-BROKEN — {target}]`
- "Chapter C" → "Part 8 §8.4" (82 instances deferred; find-and-replace pending)
- "Part VIII (case studies)" → "Part 9" (12 instances deferred; find-and-replace pending)

---

## 8. Timestamp and Version Formatting

- All timestamps: `YYYY-MM-DD HH:MM` (never date-only)
- Version identifiers: `V[major].[minor] YYYY-MM-DD HH:MM`
- Design stage: "DD" = Design Development (never "Developed Design")
- Design stage: "RFO" = Ready for Occupancy (never "Commissioning" or "Practical Completion")

---

## 9. Output Format Rules

| Output type | Format |
|---|---|
| Inter-agent state, session handoffs | YAML |
| Human-readable final outputs | Markdown (.md) |
| Word documents | .docx — only if explicitly requested |
| Intermediate working documents | Lightweight, minimal formatting |

---

## 10. Structural Change Control

- Any structural change (rename, recode, move, add, remove) → `toc-editor` first
- `toc-editor` updates `references/toc.md` and generates Change Order at `references/change-orders/CO-{NNNN}-{YYYY-MM-DD-HHMM}.md`
- find-and-replace and cross-reference-resolver execute against guidebook source using the Change Order
- Never make structural changes without corresponding `toc.md` update and Change Order on GitHub
