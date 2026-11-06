# Search log — terminology pass DA/DK, session_2026-11-06-base-vocabulary-review

Every retrieval below is persisted in `retrieval-log/session_2026-11-06-base-vocabulary-review/` (manifest line by URL).
**Method defect, stated first:** the prior expectations were formed before each call but written into this file
after the retrievals, from the session transcript. They are recorded as held, not as timestamped predictions.
Ordering is chronological.

## S0. Base-derived candidates (no network)
- Query: `select * from research_code_leads` filtered for DK/Denmark/Dan. Expectation: none (the caller said so). Result: 0 rows. Shape: string filter on every column, so a lead spelled "Danmark" would also have been missed only if no column held "Dan" — it would have matched.
- Query: `select ref_id, pub_title, standard_number from evidence_sources where jurisdiction='DK'`. Expectation: 0. Result: 0.
- Query: grep `references/standards-registry.md` for DK/Denmark/danish/bygnings. Expectation: a BR18 entry. Result: two DK entries, both "BR18", `source_url: https://bygningsreglementet.dk`; one asserts a "Three-quality-level framework (A/B/C) in SBi-anvisning 230". That assertion was not checked here (SBi anvisninger are not free) and is not relied on.
- Query: held aliases `term_aliases where lower(language)='da'`. Result: 156 distinct; all TRANSLATION/SYNONYM/BROADER/NARROWER/DOMAIN with no jurisdiction; many noted "model-generated 2026-07-25". Treated as seeds.
- **Instrument list therefore came from the registry's one URL plus the portal's own navigation (S1–S4), not from the base.**

## S1. Portal home — `https://bygningsreglementet.dk/`
- Expectation: a BR18 portal with a chapter called "Tilgængelighed". Result: 200. The chapter list has **no "Tilgængelighed" chapter**: the access chapter is "2 Adgangsforhold (§ 48 - § 62)". Other access-relevant chapters located by title: 6 Brugerbetjente anlæg, 9 Bygningens indretning, 10 Elevatorer, 17 Lydforhold, 18 Lys og udsyn, 20 Ubebyggede arealer. Version selector: "BR18 (Aktuelt)", last closed period "BR18 (1/7-31/12 2025)".
- Shape: navigation, not search; the expectation was wrong in the instructive direction (the register's own word is not the instrument's).

## S2. Retsinformation (legal text) — `https://www.retsinformation.dk/eli/lta/2019/1399`, then `/api/document/eli/lta/2019/1399`
- Expectation: consolidated BEK. The ELI number was my guess, not derived. Result: both 200 but a JavaScript app shell. Wayback availability API for the ELI URL: no snapshot. Abandoned; the portal text was used. Whether portal and legal text are identical is UNVERIFIED.

## S3. Chapter pages `tekniske-bestemmelser/{02,09,10,17,18,20}/krav/`
- Expectation: full text. Result: 200 each, but only accordion headings; the section text is served from `data-href="...?ajax=1"` fragments. Shape lesson: an HTML 200 can hold no requirement text; check the extracted length.

## S4. Section fragments (26, then 8 more for kap. 6, 7, 16)
- Expectation: full § text. Result: all 200; text extracted with `tools/h2t.py`. Kap. 6, 7 and 16 were added after reading kap. 2 suggested that user-operated installations might hold the "controls" concept (it did: § 159-160) and that scaffolding might sit in kap. 7 (it does not).

## S5. Guidance index `vejledninger/.../oversigt_br_vejledninger/` and its `kap_2`, `kap_9`, `kap_10` fragments
- Expectation: a substantive "vejledning om tilgængelighed". Result: kap. 2 lists "Spørgsmål og svar om adgangsforhold", "Bygningsreglementets vejledning om adgangsforhold" (linked via a `historisk/br18_version6` path), "Vejledning til brugerbegreb", "Vejledning til kommunerne om krav til parkering", "Vejledning om tilgængelighed til transportable konstruktioner".

## S6. Guidance documents
- `.../historisk/br18_version6/.../generel_vejledning/adgangsforhold/` → page; its PDF `media/pydnkz1j/generel_vejledning.pdf`. Expectation: several pages of guidance. Result: **one page**, a pointer to "DS Håndbog 186: Tilgængelighedskrav i BR18 holdt op mod DS/ISO 21542." sold in DS's webshop.
- A guessed current path `.../tekniske-bestemmelser/02/vejledninger/generel_vejledning/adgangsforhold/` → 404 (kept as a failed retrieval).
- `Vejledning-til-brugerbegreb` page and PDF `media/ujzcpny1/vejledning-til-brugerbegreb.pdf` → 5 pages, read in full.
- `media/lnvhj0zl/vejledning-om-tilgaengelighed-til-transportable-konstruktioner-a.pdf` → 4 pages, read in full.

## S7. DS Håndbog 186 — `https://webshop.ds.dk/search?q=Håndbog 186`
- Expectation: a priced product page (paid). Result: 200 but a script-rendered shell; no product text. Recorded NOT-OBTAINABLE on the guidance's own statement that it is sold there. No purchase or other route attempted. DS/ISO 21542, DS/EN 81-70 and DS 490 not attempted.

## S8. In-text greps for absent concepts
- Regexes per concept are held in `build.py` (`ABSENT`) and their counts are recomputed into `coverage.tsv` on every run. Note a shape trap met here: the stem `rist` (gratings) matched "frist" (deadline) until anchored as `\brist`; `greb` matches "brugerbegreb"; the held-alias substring report in `build.py` has the same weakness and over-reports.

## Not searched (logged so absence is not read as evidence)
Vejregler (road-design rules) for bollards, speed bumps and kerbs; Arbejdstilsynet workplace rules; SBi/BUILD anvisninger; Bolig- og Planstyrelsen / sbst.dk news on 2026 amendments; DS standards.
