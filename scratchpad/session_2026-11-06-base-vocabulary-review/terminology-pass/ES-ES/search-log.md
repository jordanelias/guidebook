# Search log — terminology pass ES/ES, session_2026-11-06-base-vocabulary-review

Each entry: query verbatim, prior expectation (written before the result), result, note on query shape (R14). Empties kept.

## B — derivation from the base (before any web search)
- B1. `select ref_id, pub_title, standard_number from evidence_sources where jurisdiction='ES'`. Prior: one or two rows, CTE DB-SUA likely. Result: 3 rows — REF-01027 (DB-SUA con comentarios), REF-01028 (Orden TMA/851/2021), REF-01029 (CERMI Madrid methodology, T3, municipal, not a national instrument). Note: evidence_sources gives the instruments a prior ramp batch needed, not the accessibility corpus.
- B2. `research_code_leads` rows with jurisdiction ES. Prior: one ramp lead. Result: leads 91 (CTE DB-SUA, clause SUA 1 4.3.1) and 93 (CERMI Madrid). No lead for the real decree on basic conditions, nor for housing-specific or existing-building rules.
- B3. `references/standards-registry.md` ES entries. Prior: CTE and UNE. Result: CTE DB SUA (source_url DBSUA.pdf) and UNE 41500:2020 (paywalled UNE store link only).
- B4. `retrieval-log/*/manifest.jsonl` grep for SUA / boe.es. Prior: the batch-23 artefacts. Result: held — `1bc0a3fe0bdf78f2.pdf` (DccSUA.pdf, DB-SUA "con comentarios", articulado 14 junio 2022, comentarios 15 julio 2024), `9f561626b2028bed.html` (BOE consolidated Orden TMA/851/2021), `ce7c5fdc63f3bb2c.html` (BOE Orden VIV/561/2010, derogated). The held DB-SUA reading in batch 23 covered pages 1-2 and 27-28 only (manifest purpose line), so it was not a full reading.

## W — web searches
