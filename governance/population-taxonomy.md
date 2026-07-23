# Population Taxonomy
**Status:** SUPERSEDED (population code set) — see banner below. Structural detail retained pending full rewrite.
**Phase:** Stage A Phase 7 — Population taxonomy
**Created:** 2026-04-29 19:06 UTC
**Doctrinal basis:** workplan-orchestrator §Population Codes · project-standards (L11, L38, L41, L96, L118) · `schemas/enums.py` PopulationCode

---

> ## ⚠ Superseded by DR-2026-07-23 (Access-Taxonomy Axis-2 population set)
>
> The population **code set** below (11 top-level + slash sub-codes + parent nesting) is
> **retired**. Per `decisions/DR-2026-07-23-population-schema-replace.md`, the canonical set is
> now the flat, community-organized **23 codes** (no parent codes, no containment):
>
> `BLIND DEAF DEAFBLIND MOB LMB SCI MOVE NDV AUT ADHD ID DEM BRAIN COM PAIN MS EPI VES MH LPA TALL BAR ALL`
>
> **Crosswalk:** VIS→BLIND · UPL→LMB · DBL→DEAFBLIND · {NEU,PCS}→BRAIN ·
> {OFS,CFS,MCAS,POTS}→COM · SENS→NDV · EXH→TALL · IntD→ID · ABI→BRAIN. New: MOVE, ID, VES,
> LPA, TALL, BAR. `ID` (intellectual disability) is now **first-class** (ends the DEM+NDV proxy).
> `NDV` is a **peer view, not a parent** of AUT/ADHD. Life stage (SEN older adults, CHD children)
> is an **orthogonal modifier** (`life_stage_modifiers` table), not a population. `ALL` and `MH`
> are retained. Access needs (Axis 1) are the tagging axis — see the access-needs layer
> (migration 031) crosswalked to ICF. The single source of truth remains `schemas/enums.py`
> `PopulationCode`. Sections below describe the retired scheme and await a full rewrite.

## 1. Taxonomy structure

### 1.1 Main taxonomy — 11 top-level codes

The guidebook organizes disability populations into 11 primary codes. Each code represents a cluster of functional impairments that share design implications for the built environment. The codes are an organizing convenience, not a definition of people — per project-standards: "a person is not defined by their disabilities."

| Code | Label | Sub-codes | Part 2 section |
|---|---|---|---|
| MOB | Mobility & Strength | MOB/AMB (ambulatory mobility), MOB/UPL (upper-limb / dexterity) | §2.1 |
| VIS | Visual impairment | — | §2.2 |
| DEAF | Deaf / hard of hearing / hearing device users | — | §2.3 |
| NEU | Neurological / acquired brain injury | NEU/PCS (post-concussion syndrome) | §2.4 |
| DEM | Dementia | — | §2.5 |
| NDV | Neurodivergence | NDV/AUT (autism spectrum), NDV/ADHD, NDV/SENS (sensory processing) | §2.6 |
| NDV/MH | Mental health / PTSD / trauma | — | §2.7 |
| PAIN | Chronic pain / fibromyalgia | — | §2.8 |
| DBL | DeafBlind | — | §2.9 |
| OFS | Orthostatic & fatigue spectrum | OFS/ME, OFS/POTS, OFS/MCAS | §2.10 |
| ALL | All disability categories | — | Cross-cutting |

**IntD (Intellectual Disability)** is NOT a top-level code. It is proxied through DEM (wayfinding, cognitive simplicity) and NDV (sensory environment, Easy Read signage). No §2.12, no IntD matrix column, no IntD population code table entry. All IntD-relevant specifications carry THIN-BASE disclosure. The proxy decision is documented in project-standards (2026-03-25) and reflects the evidence landscape: IntD-specific built environment research is extremely sparse; the functional overlaps with DEM and NDV are substantial enough that proxy coverage is defensible, while a standalone code would produce mostly `pending` cells.

### 1.2 Supplementary codes

Four additional codes exist for supplementary content only. They do NOT appear in the main population matrix (Parts 4–8), volume I–II room matrices, or the specification grid.

| Code | Label | Location |
|---|---|---|
| CHD | Children / pediatric | Supp. Part 4 |
| LPA | Little People / restricted growth | Supp. Part 4 |
| EXH | Extreme height | Supp. Part 4 |
| BAR | Large body size / bariatric | Supp. Part 4 |

**BAR in Volumes I–II is an error.** The validator flags any BAR code outside Supplementary Part 4 files.

### 1.3 The ALL code

`ALL` is not a population — it is a scope marker meaning "this specification applies to all populations." Typical uses: Universal Mode code compliance values (e.g., minimum corridor width per code); universal design principles that do not vary by population. `ALL` specifications do not have population-specific columns in the matrix — they have a single value that applies universally.

`ALL` must not be combined with specific population codes on the same specification. A specification is either `ALL` or it is population-specific. The validator rejects `populations: [ALL, MOB]` — this is incoherent.

---

## 2. Sub-code hierarchy

### 2.1 Inheritance rules

Sub-codes are specializations of their parent. The relationship is:

- **Evidence inheritance:** a sub-code inherits all evidence from its parent. MOB/AMB inherits all MOB evidence. NDV/AUT inherits all NDV evidence.
- **Evidence addition:** a sub-code may have additional evidence specific to the specialization. MOB/AMB may have evidence about ambulatory gait that does not apply to MOB/UPL.
- **Specification narrowing:** a sub-code's specification range is always a subset of (or equal to) its parent's range. If MOB specifies grab bar diameter 32–38 mm, MOB/AMB cannot specify 28–42 mm. It may specify 34–38 mm (a narrowing).

### 2.2 When to use sub-codes vs. parent codes

- **BPC research:** always uses the most specific applicable code. If evidence addresses ambulatory mobility specifically, the BPC slug uses MOB/AMB, not MOB.
- **Specification records:** use the parent code unless the sub-code produces a meaningfully different range or recommendation. A specification that applies identically to MOB/AMB and MOB/UPL uses MOB.
- **Room matrices:** use parent codes. Sub-code distinctions surface in the specification detail, not in the matrix layout.
- **Search logs:** use the most specific applicable code.

### 2.3 Sub-code enumeration

The current sub-code taxonomy is:

**MOB sub-codes:**
- MOB/AMB — ambulatory mobility impairment (gait, balance, lower-limb function)
- MOB/UPL — upper-limb and dexterity impairment (grip, reach, fine motor)

**NDV sub-codes:**
- NDV/AUT — autism spectrum (sensory, social, environmental predictability)
- NDV/ADHD — attention-deficit (distraction management, environmental stimulation)
- NDV/SENS — sensory processing disorder (sensory filtering, environmental modulation)

**NEU sub-codes:**
- NEU/PCS — post-concussion syndrome (light sensitivity, cognitive fatigue, vestibular)

**OFS sub-codes:**
- OFS/ME — myalgic encephalomyelitis / chronic fatigue syndrome
- OFS/POTS — postural orthostatic tachycardia syndrome
- OFS/MCAS — mast cell activation syndrome

### 2.4 NDV/MH status

NDV/MH (Mental health / PTSD / trauma) is listed at the top level, not as a sub-code of NDV. This is deliberate: while co-occurring with neurodivergence frequently, mental health conditions have distinct functional profiles and distinct design implications (trauma-informed design, security perception, control over environment). NDV/MH has its own Part 2 section (§2.7).

---

## 3. Population code rules

### 3.1 Distinctness rules

**VIS, DEAF, DBL are three distinct independent codes.** VIS/DEAF as a compound code is an error. DBL ≠ VIS + DEAF. DeafBlindness has unique functional implications (tactile communication, combined orientation/mobility loss, reduced redundant sensory channels) that are not the sum of visual and hearing impairment.

The validator rejects:
- `VIS/DEAF` as a population code
- Any specification that lists both VIS and DEAF on the assumption that their union equals DBL
- Any prose that describes DBL as "combined VIS and DEAF"

### 3.2 Co-occurrence notation

Per project-standards CO-0003:

- **`+` (plus)** = co-occurring conditions in one person. Example: "MOB+VIS" means a person who has both mobility impairment and visual impairment. Used in Tier 2 co-design context and Part 5 co-occurrence resolution.
- **`/` (slash)** = different people sharing the same space. Example: "DEAF/VIS" means a space must serve both a deaf person and a visually impaired person (not the same person). Used in Part 5 building-level conflict resolution and room matrices.

The slash notation for sub-codes (MOB/AMB) is distinct from the slash notation for multi-population spaces. Context disambiguates: sub-codes are defined in the taxonomy; multi-population uses are preceded by a different population code. The validator distinguishes these by checking against the canonical sub-code list.

### 3.3 One slug, one population

Per project-standards: "Each slug covers exactly one population." A BPC slug addresses a single population code (top-level or sub-code). Combined slugs are not permitted. If a design parameter needs research for both MOB and VIS, two slugs are created.

### 3.4 Population variability acknowledgment

Per project-standards Core Doctrine: "Disability populations are not uniform." Every item specification must acknowledge functional variability within the population and discuss how co-occurrence affects the design parameter. Population codes are organizing principles, not definitions of people:

- At **Universal Mode**: comprehensive (mapping all considerations for a parameter)
- At **Tier 1**: insight-providing (what to think about for a known population)
- At **Tier 2**: they step aside — OT works bottom-up from functional impairments

### 3.5 Conflict domain resolution

Cross-population conflicts are searched by **conflict domain** (12 environmental parameter conflicts), not by population pair. This prevents combinatorial explosion (11 × 10 = 110 population pairs vs. 12 conflict domains). Aged care POE literature is the richest evidence source for multi-population conflicts.

---

## 4. Validator specification

### 4.1 validate_population.py scope

The validator checks population codes across the corpus:

| Check | Severity | Description |
|---|---|---|
| Valid code | ERROR | Every population code in BPC files, specifications, search logs, and connections resolves to `PopulationCode` enum |
| BAR containment | ERROR | BAR code appears only in files under `references/bpc/supplementary/` or paths containing `supp` |
| CHD/LPA/EXH containment | ERROR | Supplementary codes appear only in supplementary file paths |
| VIS/DEAF compound | ERROR | `VIS/DEAF` as a single code is rejected |
| ALL exclusivity | ERROR | `ALL` never appears alongside specific population codes in the same specification's `populations` list |
| One slug one population | WARNING | Each BPC slug's population field contains exactly one code |
| IntD rejection | ERROR | `IntD` does not appear as a population code in specifications, BPC entries, or matrix columns |
| Sub-code parent consistency | WARNING | Sub-code value ranges fall within parent code ranges (where both exist for the same parameter) |
| Co-occurrence notation | WARNING | `+` used for intra-individual co-occurrence; `/` used for multi-population spaces; sub-code `/` distinguishable from multi-population `/` by context |

### 4.2 Input sources

The validator scans:

1. `data/specifications/*.yaml` — `populations` field
2. `references/bpc/**/*.md` — YAML front matter `population` field
3. `references/search-logs/**/*.md` — `population` field
4. `references/connections/**/*.md` — population references in connection text
5. `schemas/enums.py` — canonical reference (not validated against; it IS the source of truth)

### 4.3 Exit codes

- 0 = all checks pass
- 1 = one or more errors found
- 2 = configuration error (missing files, unparseable YAML)

---

## 5. Enum alignment

The `PopulationCode` enum in `schemas/enums.py` is the single source of truth for valid population codes. This governance document does not add or remove codes — it documents the rules governing those codes.

If a new population code is needed (e.g., a new sub-code for an emerging evidence base), the process is:

1. Proposal with evidence basis (what functional profile does this code capture that is not covered by existing codes?)
2. Decision via project-standards RULE
3. Addition to `PopulationCode` enum
4. Update to this governance document
5. Update to workplan-orchestrator §Population Codes

Changes to the enum without governance documentation are validator errors at the next doctrine-recheck (A13).

---

## 6. Status

| Field | Value |
|---|---|
| Created | 2026-04-29 19:06 UTC |
| Phase | Stage A Phase 7 (Population taxonomy) — Session 1 |
| Status | CANONICAL |
| Consolidates | workplan-orchestrator §Population Codes, project-standards L11/L38/L41/L96/L118, PopulationCode enum |
| Forward dependencies | validate_population.py (this session), A13 doctrine-recheck |

---

**End of A7 governance document.**
