# Every taxonomical code in the repository, sorted for categorization

Measured 2026-09-01 against `data/guidebook.db` at `user_version` 65. Every count is derived,
none typed from memory. WHO figures come from the 2026-01 ICD-11 MMS release file
(sha256 `f1356588f40953a83e3af2b662deab47c5e269f944d1ea4ed0cfeb2007c7cd39`).

---

# Part 1 — What exists

## 1a. Closed vocabularies declared in the schema

**89 `CHECK ... IN (...)` constraints.** They are not 89 vocabularies:

| | count |
|---|---|
| `IN ('0','1')` — booleans wearing a vocabulary costume | **22** |
| genuine value sets | **67** |
| …of those, **declared but with zero rows in use** | **35** |
| …with at least one value exercised | **32** |

**More than half the genuine value sets have never been used.** Nine-value
`source_value_extractions.measurement_paradigm`, nine-value `device_class`, seven-value
`spec_value_probes.phase`, six-value `gap_mining.outcome` — all zero. That is the same defect as
`J` in `items.category`: vocabulary posited ahead of the content it was meant to sort.

## 1b. Registry tables — tables whose ROWS are a vocabulary

| registry | rows | inbound FKs |
|---|---|---|
| `decisions.decision_id` | 184 | 1 |
| **`slugs.slug`** | **106** | **16 — the most-referenced object in the schema** |
| `items.item_code` | 93 | 13 |
| `terms.term_id` | 88 | 2 |
| `search_executions.exec_id` | 28 | 2 |
| `populations.population_code` | 23 | 11 |
| `access_needs.need_code` | 17 | 3 |
| `axes.axis_code` | 17 | 3 |
| `rooms.room_code` | 17 | 1 |
| `evidence_sources.ref_id` | 10 | 13 |
| `gaps.gap_id` | 5 | 3 |
| `access_duration.code` | 3 | 0 |
| `access_stakes.code` | 3 | 0 |
| `life_stage_modifiers.code` | 2 | 0 |

## 1c. Open vocabularies — a small distinct set with NO constraint

| column | distinct | note |
|---|---|---|
| `lang_jur_map.jurisdiction` | 48 | ISO country codes, unconstrained |
| `terms.domain` | 18 | includes `functional_axis` ×17 — **exactly the 17 axes**, a shadow copy |
| `lang_jur_map.language` | 19 | ISO language codes, unconstrained |
| `access_need_icf.icf_code` | 15 | real ICF codes, **no FK, no CHECK** — a typo is accepted |
| `jurisdictional_values.jurisdiction` | 12 | unconstrained |
| `evidence_sources.tier` | 3 | **the evidence tier has no CHECK at all** |

## 1d. External (WHO) vocabularies now in play

| set | size | status |
|---|---|---|
| ICD-11 chapters | 28 | reference |
| ICD-11 **Generic functioning domains**, ch V | **44** non-residual | **adopted as the ICF lens**, 2026-09-01 |
| ICD-11 WHODAS 2.0 (`VD*`) | 38 | available, not adopted |
| ICD-11 Brief Model Disability Survey (`VE*`) | 8 | available, not adopted |
| ICD-11 manifestation tier | ~19 proposed pairings | pending owner review |
| ICF `e` codes in use here | 10 | **ruled not a lens** — world-side |
| loose ICF `b`/`d` codes in the repo | 51 | superseded for lens purposes by the 44 |

---

# Part 2 — The sort: five kinds, and only one of them categorizes content

Nothing here is a matter of taste. A set's **kind** decides what it can sort.

| kind | what it sorts | count | can it categorize the guidebook's content? |
|---|---|---|---|
| **0. Flags** | nothing — `IN ('0','1')` | 22 | No. They are booleans. |
| **1. Identifiers** | individuals | 7 registries | No. They name things, they do not group them. |
| **2. Process / state** | **the record**, not the subject | ~40 | No. `status`, `disposition`, `phase`, `check_method`. |
| **3. Quality / grade** | **a claim**, not a subject | ~10 | No. `match_grade`, `strength_band`, `tier`, `applicability`, `access_stakes`. |
| **4. Subject** | **what a thing is about** | see Part 3 | **Yes — these are the only candidates.** |

---

# Part 3 — The subject sets, evaluated

Four tests, all of them drawn from rulings already on the books:

- **(a) real** — does it name a genuinely distinguishable thing?
- **(b) independent** — is it derived from, or a duplicate of, another set? (rule 5)
- **(c) not presupposed** — was it posited ahead of the synthesis meant to produce it?
  (`DR-2026-08-24` §2.4: categories are an **output**, *"not presuppositions"*)
- **(d) sourced** — external standard, or coined here?

| set | size | a | b | c | d | verdict |
|---|---|:-:|:-:|:-:|:-:|---|
| `populations` — identity | 23 | ✓ | ✓ | ✓ | coined | **USE**, minus `ALL` (see Part 5) |
| `access_needs` — demand | 17 | ✓ | ✓ | ✓ | coined | **USE** |
| WHO Generic functioning domains | 44 | ✓ | ✓ | ✓ | **WHO** | **USE** — adopted |
| ICD-11 manifestation tier | ~19 | ✓ | ✓ | ✓ | **WHO** | **USE**, pairings pending review |
| `rooms` — place | 17 | ✓ | ✓ | ✓ | coined | **USE** — and it is the only one of D-0171's three building levels that exists |
| jurisdiction | 12 / 48 | ✓ | ✓ | ✓ | **ISO** | **USE** |
| language | 19 | ✓ | ✓ | ✓ | **ISO** | **USE** |
| `access_duration` | 3 | ✓ | ✓ | ✓ | coined | **USE** — permanent / temporary / situational, orthogonal to everything |
| `access_needs.family` | 5 | ✓ | **✗** | ✓ | coined | **rollup** of `access_needs`. Fine as a display grouping; not an independent set |
| `populations.category` | 8 | ✓ | **✗** | ~ | coined | **rollup** of `populations`, and it bundles the `ALL` scope marker with three real identities |
| `life_stage_modifiers` | 2 | ✓ | ✓ | ✓ | coined | **thin** — two values, and its own notes concede weak evidence for `CHD` |
| `terms.domain` | 18 | ~ | **✗** | ✗ | coined | **shadow** — unconstrained, and `functional_axis` holds exactly the 17 retiring axes |
| `axes` — coined ICF | 17 | ✓ | **✗** | ✗ | coined | **RETIRE** — superseded by the 44 (owner ruling, 2026-09-01) |
| `items.category` A–K | 11 | ~ | **✗** | **✗** | coined | **RETIRE** — *"should not exist yet"* (owner ruling); and it duplicates the `item_code` prefix on 93 of 93 |
| ICF `e` codes | 10 | ✓ | ✓ | ✓ | WHO | **not a subject set for people** — world-side; nobody is an `e150` |
| `gaps.category` | 12 (3 used) | ✓ | ✓ | ✗ | coined | **process**, not subject |

---

# Part 4 — What survives, arranged

The usable sets are not one taxonomy. They are **five orthogonal axes**, and every rollup above
belongs *inside* one of them rather than beside it.

### AXIS 1 — WHO (four lenses, all person-side)
```
identity     populations              23   coined, community-facing
function     WHO generic domains      44   ICD-11 chapter V
diagnosis    ICD-11 manifestation    ~19   pending pairing review
demand       access_needs             17   coined
```
Rollups available for display: `populations.category` (8), `access_needs.family` (5).

### AXIS 2 — WHERE (place)
```
room type    rooms                    17
building type   — does not exist       0   D-0171 named it; never built
construction element — does not exist  0   D-0171 named it; never built
```

### AXIS 3 — WHEN (relationship to the barrier over time)
```
access_duration                        3   permanent / temporary / situational
life_stage_modifiers                   2   SEN / CHD — thin, and it says so itself
```

### AXIS 4 — WHERE IN THE WORLD
```
jurisdiction                       12/48   ISO
language                              19   ISO
```

### AXIS 5 — SUBJECT MATTER, and this is the one nobody named
```
slugs                                106   research topics · 16 inbound FKs
```

**`slugs` is already the subject categorization, and it is the only one that satisfies every
test.** It is the most-referenced object in the entire schema — 16 inbound foreign keys, more than
`items` (13) or `evidence_sources` (13) — and, unlike A–K, unlike the coined axes, unlike `ALL`,
**it grew out of research rather than being posited ahead of it.** Slugs like
`acoustics-speech-intelligibility-disability` and `chronic-pain-built-environment` are what the
project actually investigated.

That is exactly the shape `DR-2026-08-24` §2.4 demands — a categorization that is an *output*. If
A–K is retired and nothing replaces it, **nothing is lost**, because the subject categorization the
guidebook needs is already there, already used, and already evidenced.

---

# Part 5 — Findings

### F1. The repository already ruled that `ALL` should not exist, and it exists anyway

`access_duration.situational`, written 2026-07-23, carries this definition **in the database**:

> *"Context-induced for anyone (loud room, bright sun, carrying a child). **A non-empty situational
> relevance is why there is no ALL code.**"*

`populations.ALL` exists, with 9 link rows and 0 warrants. Two registries in one database directly
contradict each other, and the one that is wrong is the one being used. This is `CLAUDE.md` rule 4b
in its purest form — a ruling that is in the repository, in a file, and still fails to bind.

**It also settles the `ALL` question without needing a new ruling.** The reasoning is already
written: situational relevance is *why there is no ALL code*. `ALL` is not a population; it is the
absence of a population claim, and the correct representation of that is no row.

### F2. More than half the genuine value sets have never been used

35 of 67. Nine-value `measurement_paradigm`, nine-value `device_class`, seven-value
`spec_value_probes.phase` — declared, zero rows. Each is the same defect as `J`: vocabulary posited
ahead of content. **A cull is available and needs no ruling beyond the burden of proof `CLAUDE.md`
§1 already sets** — before keeping a check, name what wrong thing reaches the guidebook without it.

### F3. `terms` carries a shadow copy of the axes

`terms.domain = 'functional_axis'` holds exactly **17** terms — the same 17 as `axes`. When the
axes retire into the 44 WHO domains, these 17 terms retire or re-point with them, or the shadow
outlives the thing it shadowed.

### F4. The evidence tier has no CHECK constraint

`evidence_sources.tier` is unconstrained, so `dbcore.check_values()` returns an empty set for it
and no tier rule can lean on the column's own vocabulary. Meanwhile
`governance/tier-system.md` defines T1, Co-1, T2, Co-2, T3, T4–T6 — a **seven-value doctrine with
no schema behind it**, on the single most load-bearing judgement the project makes.

### F5. `access_need_icf.icf_code` has no FK and no CHECK

15 distinct real ICF codes, unconstrained. A typo is silently accepted in the one place the project
records its ICF mappings.

### F6. Two vocabularies encode the same fact twice

- `items.category` = `substr(item_code, 1, 1)` on **93 of 93** rows.
- `terms.domain='functional_axis'` = the `axes` table, 17 = 17.

Both are rule 5, both in plain sight.
