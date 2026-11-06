# Search log — terminology pass KO/KR (session_2026-11-06-base-vocabulary-review)

Every query or retrieval verbatim. "Prior" is written before the result is seen (results appended after). Shape note per R14. Empties kept.

## Instrument derivation (database, read-only)

- D1 `select ref_id, pub_title, standard_number, jurisdiction from evidence_sources where jurisdiction like '%KR%' or jurisdiction like '%Korea%'` — Prior: one or two rows for the Enforcement Rule annex read in an earlier batch. Result: 3 rows. REF-01004 (a journal article on wheelchair ramp slope, not an instrument); REF-01019 (NEPLA legal-wiki mirror of 시행규칙 [별표 1] <개정 2023. 12. 11.>, superseded by REF-01031); REF-01031 (the same annex, official law.go.kr flDownload.do?flSeq=162983711, PDF of 22 pages, retrieved 2026-10-01 in session_2026-10-01-research-batch-23, artefact b71c64f1a9b3125f.pdf). Shape: well-formed.
- D2 `select jurisdiction, count(*) from research_code_leads group by 1` — Prior: no KR row. Result: no KR row (16 jurisdictions, none KR). Shape: well-formed. The instrument list therefore cannot be derived from leads.
- D3 `grep -n -i "korea\|KR" references/standards-registry.md` — Prior: one entry naming the Act. Result: one entry (line 473), "Korean Welfare Facilities Promotion Act — 2024 revision shifts from route access to daily life access", source_url `https://www.law.go.kr/` (portal root, not the text). Not verified here; recorded as a registry prose claim only.
- D4 Prior held text: session_2026-11-06-pipeline-batch-2 filed extractions on REF-01031 (scan notes, gaps.py), reading the same Annex 1. Its pre-screen read is the "held KR source" this pass must read in full.

## Retrievals
- R1 fetch `https://www.law.go.kr/LSW/flDownload.do?flSeq=162983711` (the held REF-01031 file, re-fetched to check it is still served and byte-identical). Prior: 200, PDF, sha256 b71c64f1… identical to the 2026-10-01 artefact.
- R2 fetch `https://www.law.go.kr/법령/장애인ㆍ노인ㆍ임산부등의편의증진보장에관한법률시행령` (decree, current-version path). Prior: 200 but a frame/JavaScript shell with no article text.
