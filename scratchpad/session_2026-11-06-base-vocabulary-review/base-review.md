# Base-table review: vocabulary coverage, multilingual reach, and routes to populate

Session `session_2026-11-06-base-vocabulary-review`. Research session; no rows written. Every figure below was
derived from `data/guidebook.db` and the repository on 2026-11-06; re-derive, do not trust (rule 7a).
Scope for languages and jurisdictions: P1+P2+P3 of the ramp-spec handoff (`workplan/2026-10-30-ramp-spec-pages/HANDOFF.md`
section 3; owner: "Yes it is P1+P2+P3", `references/project-standards.md`, 2026-10-30): US UK AU CA DE NO SE ISO EU; FR CH NL DK FI BE IE ES IT PT; JP SG NZ KR CN.

## 1. Verdict

The base does not yet do the job of catching omissions. Three defects, worst first.

1. **The parameter list is ten rows.** `base_parameters` holds 10 active rows; 94 `terms` exist, of which 84 are not parameters
   and only one is declined. Two-thirds of the quantities any accessibility code states (stairs, handrails, grab bars,
   slip resistance, sound insulation, illuminance, seat heights, control heights, counter heights …) have no term at all.
2. **Non-English vocabulary is nominal.** 14 languages serve P1+P2+P3 (DA DE EN ES FI FR IT JA KO NL NO PT SV ZH). All have aliases for most terms,
   but of 2382 aliases only 15 are verified (all Indonesian, outside P1-3). 1163 are model-generated, 880 carry no provenance,
   and the 304 English ones are "curated". Not one P1-3 non-English alias has been checked against a glossary or native source.
   A translation is also not a native term: `jurisdiction` is NULL on 2133 of 2382 aliases, so DE/AT/CH or FR/BE/CH/CA usage, or US "curb ramp"
   against UK "dropped kerb", cannot be told apart.
3. **The non-term base tables are English-only and thin.** `base_icf`: 72 codes, 29 with titles, none in another language.
   `base_taxonomy_medical`, `icf_medical_map`, `identity_medical_map`: 0 rows. `rooms`: 17, no category. Identity display names exist in English only.

## 2. Table-by-table

| Table | Live state (derive: `select count(*)`) | Finding |
|---|---|---|
| `slugs` | 106 in 13 topic directories (80 ACTIVE, 23 STUB, 3 MERGED) | Searches' unit, not a vocabulary. Topic gaps against the held terms: stairs and handrails, doors beyond hardware, lifts, parking, egress and evacuation, outdoor routes, toilets beyond bathrooms, controls beyond reach. The 2026-08-27 ruling treats slugs as a revisable seed corrected by the harvest. |
| `terms` | 94; 17 `functional_axis`, 16 `circulation`, 14 `methodology` | Mixed kinds under one table: quantities, elements, methods, lenses, settings. Only the quantities can be parameters. |
| `base_parameters` | 10 | See 1.1. Only two carry `accessibility_direction`. |
| `term_aliases` | 2382 in 15 languages | See 1.2. 6 terms (89–94) have no non-English alias; 13 `functional_axis`/method terms lack 7–10 of the 13 non-English languages. |
| `base_icf` | 72; b 26, d 36, e 10 | 43 untitled (title needs a verified `title_source`). Only 10 `e` codes, so products, support and attitudes chapters are almost absent: the codes the built environment mostly sits in. |
| `base_taxonomy_identity` | 23 | Population taxonomy: owner-only (DG-NON). Not touched. |
| `base_taxonomy_medical` + both maps | 0 | The medical lens is offered, not adopted (D-0170), and is empty. |
| `access_needs` | 17 (family × stakes) | Only 1 carries `typical_stakes`. |
| `rooms` | 17 | No category; no link to terms or parameters. |
| `lang_jur_map` | 14 P1-3 languages cover every P1-3 jurisdiction except ISO, which is a meta-code | Structurally complete for P1-3. AR BN HI SW are scoped out (OR-12a). |

## 3. Prior editions: what exists and what the rules allow

| Prior work | Where | Status for this purpose |
|---|---|---|
| 88 pre-reset terms | `_archived/data/corpus-pre-reset-2026-08-06.db` `terms` | **Permitted catalogue, exhausted.** Every one is already held by name or alias (checked), so `mint-term-from-catalogue` has nothing new to take. |
| Code and standards registries | `references/standards-registry.md`, `tier456/co1/co2-verified-sources.json` | Permitted catalogues, but bibliographic: they name instruments, not quantities. |
| 93 listed specification items | pre-reset `items`; `_archived/references/part04-item-index.md` | **Not a permitted name source** (owner, 2026-10-09: offered, not selected; item layer deleted 2026-09-01 because the names carry answers). Used below only as a read-only leak check. |
| 109 jurisdictional values | pre-reset `jurisdictional_values` | Values by item and jurisdiction (DE, GB, US, AU 18–20 each; ISO 13). Not a vocabulary. Also, no row for CN, KR, DK, NL, IT, PT. |
| Synonym chart and alias verification protocol | `_archived/references/synonym-chart.md`, `references/native-alias-verification.md` | Already the source of the 2382 aliases; the chart says outright that none is native-verified (GAP-302/303). |

**Conflict to rule on (rule 0):** "we should have some work already done based upon … those listed specification items" reads as wanting
the 93 items used. The standing 2026-10-09 ruling excludes their names as a source for parameters. I have not minted from them.

## 4. Leak check: quantities the 93 item subjects imply that no term holds

Value-stripped, quantity-shaped subjects only, derived by dropping the parenthetical and bracketed text from `items.name`.
**These are leads for the open pass, not names to mint** — a name is minted only from a phrase an admitted source uses
(`add-term --from-observation`), or from a permitted catalogue after your approval.

- **Acoustic:** sound absorption (have `acoustic absorption`), sound insulation between spaces, background noise level from building services, vibration isolation, hearing-loop field strength.
- **Lighting and colour:** illuminance, glare, flicker, daylight provision, luminance contrast of floor transitions (floor LRV differential), floor-surface reflectance, lighting transition between zones.
- **Surfaces and routes:** slip resistance, door opening force (have `operating force`), automatic-door timing, landing size at entrances, rest-point spacing (ruled a second headline parameter on 2026-10-30), tactile-indicator dimensions, kerb or step height.
- **Reach and fittings:** control height, work-surface height, counter height, grab-bar position and diameter, seat height, wardrobe and storage reach.
- **Environment:** thermal setpoint and response, ventilation and air quality, scent and fragrance load.
- **Stairs, handrails, cross-slope and lift car size are not in the 93 at all** and are absent from the terms: the leak check shows the old list is not a ceiling either.

## 5. Routes that can populate the base, by what each needs

| Route | Needs | Yield |
|---|---|---|
| Open pass over held codes (OR-13, D-3) | Reading held full texts: UK AD M (REF-00992), ADA 2010 (REF-00987), SG Code (REF-00139) and others, with `observe-term` rows carrying verified quotes | Real parameter names, in the source's words. No scan has done the open pass: all 9 `source_scans` read `open_pass_done = 0`. Slowest, best warranted. |
| Native-language open pass over P1-3 codes (DIN 18040, NF/arrêtés, CTE DB-SUA, CAN/CSA B651, KR/JP/CN instruments, …) | Retrieval of each, then `observe-term` with `--language` | The only route that yields native terms with in-language provenance (R11). Fetches are limited to P1-3 (2026-09-28, OR-16: read held first). |
| `mint-term-from-catalogue` | Your approval entry in `references/project-standards.md`, and a catalogue with names in it | Nothing today (section 3). Becomes live only if you admit another catalogue. |
| Alias verification against published glossaries | DIN 18040 terminology, AFNOR, SIS, etc. through `retrieval_log.fetch()` | Moves aliases from model-generated to `VERIFIED-GLOSSARY`. Per-language, per-term. |

## 6. Decision wanted

One question, because it changes what I do next: **do you want the 93 item subjects (values stripped, screened, listed with their old codes removed) admitted as a catalogue for prepopulating parameter names, overriding the 2026-10-09 exclusion?**
If yes, I record it as a dated ruling and screen the list for your approval, the existing guard. If no, the next step is the open pass, starting with the three codes already held, plus native-language retrievals for the P1-3 languages.
