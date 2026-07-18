# Evidence landscape — A-18 (RT60)

*The transparency artifact (S1, owner-reaffirmed): make available **all jurisdictions / international
standards / precedents**; **admit extrapolation** when venturing a suggestion; **admit a thin base**. Every
row carries a provenance-strength: `direct` · `inadequate` · `extrapolated-from(X)` · `absent`.*

> **Corrected** after the adversarial verifier: the first draft wrongly called the code-floor values
> `absent`. They are **present** in `source_value_extractions`. Fixed below.

## Made available — what the corpus holds

**Direct primary evidence (● Tier-1, 16 studies):** classroom reverberation / speech-perception research in
hearing-impaired and typical-hearing children — Iglehart (REF-00325, 00578, 00588), Neuman (00577),
Wroblewski (00576), Prodi (00581), Spratford (00582), Wu (00586), Marzi 2024/25 (00726/00727). Jurisdictions
US ×11, INT, UK, IN, IT. `direct`.

**International standards / codes (11, across 13 jurisdictions) — the code-floor (◐, T4–6), with their VALUES
migrated:** ANSI/ASA S12.60 (US: 0.6 s ALL / **0.3 s DEAF, Footnote e**), BB93 (UK: 0.6–0.8 s), DIN 18041
(DE: 0.4–0.8 s), UNI 11532-2 (IT: 0.5 s), AS/NZS 2107 (AU/NZ: 0.4–0.6 s), plus NS 8175 (NO), AIJES (JP),
SBi-anvisning (DA), GB 50118 (CN). Values live in `source_value_extractions` with `echo_of` provenance
marking each as a committee/evidence **echo**, never independent evidence. `direct` (present), correctly
walled off as ◐.

**Precedents (built exemplars demonstrating a value achieved):** **`absent`** — no linked case-study/POE
showing an RT60 target achieved in a real inclusive building. A named search target (Nordic/Japanese
school-acoustics exemplars are the likely home).

## Admitted — where we are extrapolating (labeled, as *suggestions* not determinations)

- **Person-mode value = `extrapolated-from(population range + items.pmp_delta_min=0.05)`** — no Tier-1
  person-level study; the "OT tightens by up to 0.05 s" suggestion is extrapolated, offered as an approach.
- **DEM 0.5 s / AUT 0.4 s = `extrapolated-from` literature, conjecture** — the DB's PMP walks record
  strict-termination **FAIL by design** for both; the autism value is explicitly "a conjecture rationally
  informed by literature, not a Tier-1 threshold." The admission is already done correctly in the DB.

## Admitted — where the base is thin or absent (`inadequate` / `absent`)

| item | provenance-strength | honest statement |
|---|---|---|
| Dementia RT60 (0.5 s) | `inadequate` | one T2 framework (REF-00569), no dose-response; provisional |
| Autism RT60 (0.4 s) | `inadequate` | one T3 single-site range (REF-00561); no Tier-1 autism-distinct target (GAP-291 closed-resolved) |
| Code-floor **values** | **`direct` (present)** | in `source_value_extractions` — *correction of the first draft, which wrongly said absent* |
| Non-English standards' **content** | `inadequate` | catalogued/extracted via English metadata; original-language content may be missed |
| Co-1 lived experience | `absent` | all cells `single_axis` clinical, `co1_sources=[]`, `co1_pass_count=0` — the modality most owed |
| Built precedents | `absent` | none linked |
| Devos 2019 dementia source | **mislinked** | elab cites REF-00571 (actually *Kotloski 2020, genetics*); real Devos = REF-00735, unlinked |

## Why this matters

Nothing is hidden to make A-18 look more finished than it is — and, corrected, nothing is claimed *missing*
that is actually present. The **value** is strong and `direct` where it counts (DEAF 0.3 s, ● T1); the
**code-floor values** are migrated and correctly walled off; the genuine **gaps** are Co-1, precedents,
person/DAR layers, and two DB-flagged data errors (the Devos mislink, the ANSI duplicate records).
