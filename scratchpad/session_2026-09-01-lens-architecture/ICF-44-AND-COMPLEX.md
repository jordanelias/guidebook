# The 44 WHO domains, and where the complex conditions actually live

All codes and titles read from the WHO 2026-01 MMS release file
(sha256 `f1356588f40953a83e3af2b662deab47c5e269f944d1ea4ed0cfeb2007c7cd39`, 37,118 entities).

**A search caveat that governs every "not found" below (R14).** The release file carries
**titles only** — its columns are Foundation URI, Linearization URI, Code, BlockId, Title,
ClassKind, DepthInKind, IsResidual, ChapterNo, BrowserLink, isLeaf, Primary tabulation,
Grouping1–5, CodingNote, Parent. **No index terms, no synonyms.** So "fibromyalgia: 0 hits"
means *not a title*, NOT *not in ICD-11* — it is an index term under a title. Resolving index
terms needs the ICD-API, which returns 401 without registered credentials.

---

# Part 1 — item 4: the complex conditions

## Where the five actually land

| condition | ICD-11 | chapter |
|---|---|---|
| POTS | `8D89.2` Postural orthostatic tachycardia syndrome, under `8D89` **Disorders of orthostatic tolerance** | 08 nervous system |
| ME/CFS | `8E49` **Postviral fatigue syndrome** | 08 nervous system |
| long COVID | `RA02` **Post COVID-19 condition** | 25 codes for special purposes |
| fibromyalgia | not a title. WHO files it under `MG30.01` **Chronic widespread pain** — *needs index confirmation* | 21 symptoms, signs or clinical findings |
| MCAS | not a title, and **no near miss**. The mast-cell titles are `2A21` Mastocytosis (ch 02, neoplasms) and `4A84.6` Anaphylaxis secondary to mast cell disorder (ch 04, immune). Neither is MCAS | — |

**Five conditions, four or five different chapters, and one with no evident home.** That is not a
defect in ICD-11 — it is ICD-11 working as designed. It files by *mechanism*, and these conditions
have contested, plural, or unknown mechanisms. There is no "complex" in ICD-11 and there will not
be one, because "complex" is not a mechanism.

⚠ `MG30.04` is titled **Complex regional pain syndrome**. The word appears; the meaning is
unrelated and narrow. Nothing should key a "complex" category off it.

## WHO already conceded the point once

`MG30.0` **Chronic primary pain** — with `MG30.01` Chronic widespread pain,
`MG30.02` Chronic primary musculoskeletal pain, `MG30.03` Chronic primary headache or orofacial
pain, `MG30.00` Chronic primary visceral pain — is a **functional** grouping. *Primary* means the
pain is not explained by another condition. WHO created it in ICD-11 precisely because the
aetiological model failed for these patients, and it is where fibromyalgia sits.

That is the precedent for what follows, made by WHO, inside ICD-11.

## The answer: you don't do it in the medical lens

**The 44 functioning domains the owner just adopted already carry it**, because they describe
function rather than cause. The shared profile of fibromyalgia, POTS, MCAS, ME/CFS and long COVID
is not a diagnosis — it is this:

```
VV00  Energy and drive functions          VV01  Sleep functions
VV12  Sensation of pain                   VV02  Attention functions
VV30  Exercise tolerance functions        VV03  Memory functions
VV91  Handling stress and other psychological demands
```

Every one of those is a WHO-authored code in chapter V. Together they describe all five conditions
as **one profile** — which is exactly what a design guidebook needs, because *the built environment
meets the profile, never the diagnosis*. A rest seat, a shaded route, a quiet room and a step-free
path respond to `VV30` and `VV00`. They do not respond to `8E49` versus `RA02`.

And the identity lens already has the constituency: **`COM` — "people with complex conditions"**.

So the wide row does the work migration 065 built it to do:

```
identity_code = 'COM'      icf_code = 'VV30'      medical_code = '8E49'
identity_code = 'COM'      icf_code = 'VV00'      medical_code = '8D89.2'
identity_code = 'PAIN'     icf_code = 'VV12'      medical_code = 'MG30.01'
```

One fact, three lenses. A reader who filters on **exercise tolerance** finds the guidance whether
or not they have a diagnosis, whether or not their diagnosis is contested, and whether or not it
existed when the page was written. A reader who arrives with `8E49` in hand finds the same page.
**That is the argument for the lens architecture, restated by the hardest case.**

**"Complex" therefore does NOT need a new axis.** It is `COM` in the identity lens plus a
functioning profile in the ICF lens. Inventing a fifth vocabulary for it would be a second home
for a fact those two already state — rule 5.

---

# Part 2 — item 3: adopting the 44, and the one thing it costs

**Ruled 2026-09-01: use the 44 WHO Generic functioning domains as the ICF lens.**

## What it replaces

The 17 coined `AX-*` axes. They were always hand-made restatements of ICF — each carries its own
`icf_b_anchors` / `icf_d_anchors` — so the replacement is principled rather than arbitrary, and
most map cleanly through those anchors:

| coined axis | anchors | WHO domain |
|---|---|---|
| `AX-AUD` Auditory access & alerting | b230 | `VV11` Hearing and vestibular functions |
| `AX-VIS-N` / `AX-VIS-L` | b210 | `VV10` Seeing and related functions |
| `AX-PAI` Pain-load demand | b280 | `VV12` Sensation of pain |
| `AX-STA` Sustained-exertion demand | b455 | `VV30` Exercise tolerance functions |
| `AX-ARO` Arousal-safety demand | b152 | `VV04` Emotional functions |
| `AX-COG-O` Orientation demand | b114, b144 | `VV02` Attention · `VV03` Memory |
| `AX-REA` Reach & manipulation | b730, b710 | `VV61` Muscle power · `VV60` Mobility of joint |
| `AX-WHM` Wheeled movement & transfer | d465 | `VW15` Moving around using equipment · `VW11` Transferring oneself |
| `AX-AMB` Ambulant movement | d450, d455 | `VW13` Walking |
| `AX-BAL` Balance & postural demand | d415, d410 | `VW10` Maintaining a standing position |
| `AX-CNT` Toileting-proximity demand | d530 | `VW22` Toileting |
| `AX-COM-E` Expressive-communication | d330–d350 | `VW00` Communicating — receiving — spoken messages · `VW01` Conversation |

Reach: `item_taxonomy_links.icf_code` **158 rows** · `population_axis_map` **53** ·
`access_need_axis_map` **21** · `axes` **17** · `slugs.serves_axes` **1**. Live callers: 15 files,
of which only `scripts/validate_axes.py` and `scripts/audit/graph/extract_db.py` are executable
readers.

## THE COST, AND IT IS THE ONE THAT MATTERS

**The 44 domains are ICF `b` and `d` only. There is not one `e` code among them.**

`e` is **Environmental factors** — and measured against the live database, *this project's ICF
usage is overwhelmingly environmental*:

| `access_need_icf` | rows | distinct codes |
|---|---|---|
| type `e` — environmental factors | **38** | **10** |
| type `d` — activities and participation | 3 | 3 |
| type `b` — body functions | 2 | 2 |

**16 of the 17 access needs carry an `e` code.** They are:

```
e150  building design (public)     — 11 needs
e155  building design (private)    —  5
e125  products & technology for communication
e1251 assistive products & technology for communication
e120  mobility products & technology
e115  products for daily living
e240  Light            e250  Sound            e260  Air quality
e340  personal-care providers / SSPs
```

**`e150 building design (public)` is this guidebook.** `e250 Sound` is what item `A-18 RT60 in
Occupied Learning and Listening Spaces` IS. Adopting the 44 as the *whole* ICF lens would delete
the environmental dimension from a book about the built environment.

**They are not rivals; they describe different objects.** The 44 describe the **person** — energy,
pain, walking, hearing. The `e` codes describe the **building** — light, sound, air, design. Four
lenses that all describe the person, and a project whose entire subject is the building.

Three ways to keep both, in ascending order of change:
1. **A fifth column** on `item_taxonomy_links` — `environment_code`, referencing an ICF `e`
   vocabulary. The at-least-one CHECK grows by one term. Smallest change; keeps `e` in the same
   row as the function it serves.
2. **`e` codes move to `items`.** If `e250 Sound` is what A-18 *is* rather than something A-18
   *links to*, it belongs on the item, not on the junction. Structurally cleanest, and it makes
   every item say which environmental factor it modifies.
3. **One ICF vocabulary holding all four types** — the 44 `b`/`d` domains plus the 10 `e` codes,
   with `icf_type` carried as a column. Simplest schema, but it puts person-facts and
   building-facts in one column, and a filter would have to know which is which.

**Recommendation: (2), with (1) as the fallback.** The guidebook's items ARE environmental factors
at a finer grain than ICF has codes for — `A-18` is `e250 Sound` made specific. Putting `e` on
`items` makes that relationship explicit and leaves the four lenses purely about people, which is
what they are for.

This is not a decision a session should take. It is recorded as owed.

## Also owed before the 44 land

- **`access_need_icf`'s 5 non-`e` rows** (2 `b`, 3 `d`) overlap the 44's territory and should be
  re-pointed at WHO domains rather than kept as loose codes.
- **The 46 ICF codes anchored in `axes`** disappear with the axes. They are anchors, not data —
  but they are the only record of *why* each coined axis existed, so they belong in the migration's
  prose before the table goes.
- **`AX-CHM` Airborne-exposure, `AX-THR` Thermal, `AX-SPR` Sensory-load** have no clean home among
  the 44. `AX-CHM` and `AX-THR` are environmental in substance (`e260` Air quality; there is no ICF
  code for thermal environment), which is the same finding from the other side.
