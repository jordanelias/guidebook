# Owner rulings captured at contact, 2026-09-01 (post-065)

**Captured, not yet formalised.** These are recorded here first because `CLAUDE.md` rule 6 says a
scratchpad that lives only in context is not a review surface, and rule 0 says a live owner
statement supersedes on contact — the record of it must not wait on a migration cycle. Register
rows and DRs follow once the one open item below is ruled.

## Ruled, and settled

**R1 — the crossing maps are ICF maps, and `axis` is a coined layer sitting between.**
Owner: *"axis better not be referring to 'icf' here, but i think it is. gotta rename
population_icf_map, access_need_icf_map"*.

Measured before acting, and it corrects half the premise:

| table | rows | holds | coverage |
|---|---|---|---|
| `access_need_icf` | **43** | **real ICF codes** (`e150`, `e250`, `b765`, `d510`) with `icf_type` b/d/e/s and confidence | **17 of 17** needs |
| `access_need_axis_map` | 21 | coined `AX-*` codes | 15 of 17 needs |
| `population_axis_map` | 53 | coined `AX-*` codes | 20 of 23 populations |

`axis` is NOT ICF: axis codes are coined (`AX-AUD`), and they *anchor* to ICF through CSV strings
in `axes.icf_b_anchors` / `icf_d_anchors`. So the owner's instinct was right about the ambiguity
and the consequence runs the other way: `access_need_icf` is the DIRECT map and the better one;
renaming `access_need_axis_map` to `access_need_icf_map` would MANUFACTURE the duplicate.

**Ruled 2026-09-01: retire the axis maps.** `access_need_icf` is the needs→ICF map.
`population_axis_map` becomes `population_icf_map` only once its populations carry real ICF codes —
until then it is the only population→ICF route there is, so retiring it first loses the route.

**R2 — build a real ICF code table.** `item_taxonomy_links.icf_code`, landed in migration 065,
references `axes(axis_code)` — coined codes, not ICF. Ruled wrong. A `base_taxonomy_icf` holding
real ICF codes becomes the foreign-key target for both `item_taxonomy_links.icf_code` and
`access_need_icf.icf_code`.

**R3 — the medical vocabulary is ICD-11.** Owner: *"use ICD-11"*.

**R4 — top-down, not hyper-specific.** Owner: *"we don't include EVERYTHING. we have to work from a
top-down approach for ICF and medical, not hyper-specific conditions, that roughly correlate to what
we have from identity and needs"* · *"like if i have Hyperadrenergic POTS, i don't want to select
that in medical. I just want to select 'complex' or something"*.

## Measured while checking

- **The two ICF vocabularies in this repo are DISJOINT.** 46 codes in `axes` anchors, 15 in
  `access_need_icf`, **zero overlap** — 61 distinct codes, 26 `b` + 25 `d` + 10 `e`, and **zero
  `s`**. Two unrelated sets, neither aware of the other.
- **Nothing constrains an ICF code today.** `access_need_icf.icf_code` is bare `TEXT`; the
  `REFERENCES` in that table is on `need_code`. A typo is accepted silently.
- The repo already carries coarse groupings at the granularity R4 describes:
  `populations.category` (8 over 23) and `access_needs.family` (5 over 17).

## What the owner's three sources establish

`https://www.who.int/standards/classifications` ·
`https://icd.who.int/browse/2026-01/mms/en` ·
`https://pmc.ncbi.nlm.nih.gov/articles/PMC10374130/`

**THE LENS ARCHITECTURE IS WHO'S OWN, AND IT IS NOT A COINAGE HERE.** ICD-11, ICF and ICHI are the
three WHO *reference classifications*, and they are views over ONE **Foundation Component** — in
WHO's words *"a multidimensional collection of interconnected entities and synonyms"* holding
diseases, disorders, injuries, external causes, signs and symptoms, functional descriptions,
interventions and extension codes. The ICD-11 statistical core derives from that foundation, *"with
ICF and ICHI to follow"*. A linearisation IS a top-down view over the foundation, which is R4 stated
in WHO's vocabulary.

Della Mea et al., *PLoS One* 2023 — **"Harmonization of ICF Body Structures and ICD-11 Anatomic
Detail: One Foundation for Multiple Classifications"** — demonstrates the crossing in practice: 218
ICF entities, three independent raters, 93.5% interobserver agreement over 631 mappings,
consolidated to 434 relations typed `identical_to` / `synonym_of` / `broader_than` / `narrower_than`,
published as SSSOM on GitHub.

**THE CAVEAT THAT MATTERS AND IS EASY TO MISS.** That paper maps ICF **Body Structures** — the `s`
chapter — to ICD-11 Anatomic Detail. This repo holds **26 b, 25 d, 10 e and ZERO s codes**. So the
published mapping covers **none** of the ICF codes here. It is the right precedent and the wrong
chapter, and it must not be cited as though it crossed our set.

**Reachability, measured through this session's proxy** (all HTTP 200):
`icd.who.int/browse/2026-01/mms/en` · `id.who.int/swagger/index.html` ·
`icd.who.int/docs/icd-api/APIDoc-Version2/`. The ICD-API needs **registered client credentials**
(the owner's to create). Two routes avoid a per-request network dependency: a **local Docker
deployment** of the ICD-API, and the published **`SimpleTabulation-ICD-11-MMS-en.zip`** spreadsheet.

## Open, and genuinely the owner's

**R3 and R4 do not yet compose, and the sources do not resolve it.** ICD-11 top-down means its
chapter/block level — "Diseases of the nervous system", "Mental, behavioural or neurodevelopmental
disorders". *"Complex"* is not in ICD-11 at any level, and it is not in the Foundation either.
Hyperadrenergic POTS lands under *Diseases of the circulatory system*, which is a body-system answer
to a question the owner asked about **shape** — multisystem, fluctuating, progressive, stable.

So the medical lens is one of two vocabularies and they are orthogonal:
- **body system** — ICD-11 chapters, imported and citable; or
- **course / shape** — authored here at the granularity of `populations.category`, defensible as
  project doctrine but not ICD-11.

Building the wrong one wastes the lens. It is DG-NON content and it is not a session's to pick.
