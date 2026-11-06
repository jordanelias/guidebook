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
  Result R1: exit 35 (TLS connect error), 0 bytes, artefact e3b0c44298fc1c14.txt (empty). Retried below.
  Result R2: 200, 1336 bytes, artefact aebf02fb480950a1.html: an iframe shell pointing at `/LSW//lsInfoP.do?lsiSeq=281167&chrClsCd=010202&urlMode=lsInfoP&efYd=20260102&ancYnChk=0`. So the decree in force has lsiSeq 281167, effective 2026-01-02 (from the shell's own parameters; not yet confirmed from text). Shape: the expected JS/frame shell.
- R3 fetch the iframe target `https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=281167&chrClsCd=010202&urlMode=lsInfoP&efYd=20260102&ancYnChk=0`. Prior: 200 with a page skeleton; article text loaded later by AJAX (lsInfoR.do), so probably no article text.
- R4 retry R1 once. Prior: 200 PDF this time (exit 35 looks transient).
  Result R3: 200, 145677 bytes, artefact 58316fcadb1a87bb.html. Stripped text holds the header only: "장애인ㆍ노인ㆍ임산부 등의 편의증진 보장에 관한 법률 시행령 [시행 2026. 1. 2.] [대통령령 제35947호, 2025. 12. 30., 타법개정]" and menu labels; the body loads through `lsInfoR.do` (AJAX). As expected.
  Result R4: 200, 489120 bytes, sha256 b71c64f1a9b3125fbedc6fce85831ef3964819988ce76d5aac4ba26eb0902c63: byte-identical to the 2026-10-01 artefact. The served file for flSeq=162983711 has not changed. (Whether it is still the CURRENT annex is a separate question: see R6.)
- R5 fetch `https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=281167&chrClsCd=010202&urlMode=lsInfoP&efYd=20260102&ancYnChk=0` (the AJAX body endpoint, by GET). Prior: either the full article body as an HTML fragment, or an error because it expects POST.
  Result R5: 200, 210371 bytes, artefact 436707211a092d9d.html: the full decree body (articles, 부칙, and an annex list with flDownload links). GET works for the AJAX endpoint. The annex list gives PDF files: 별표 1 "편의시설 설치 대상시설(제3조 관련)" flSeq=159615049; 별표 2 "대상시설별 편의시설의 종류 및 설치기준(제4조관련)" flSeq=159615061; 별표 2의2, 2의3 (BF certification facilities), 2의4 (parking permit) and others.
- R6 fetch `https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=159615061&bylClsCd=110201` (decree 별표 2 PDF). Prior: 200 PDF, a long table by facility class (several pages).
- R7 fetch `https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=159615049&bylClsCd=110201` (decree 별표 1 PDF, target facilities). Prior: 200 PDF.
- R8 fetch `https://www.law.go.kr/법령/장애인ㆍ노인ㆍ임산부등의편의증진보장에관한법률시행규칙` (Rule shell). Prior: iframe shell giving the Rule's lsiSeq and efYd; if the Rule's 별표 1 was amended after 2023-12-11, a new flSeq will appear in its body.
- R9 fetch `https://www.law.go.kr/법령/장애인ㆍ노인ㆍ임산부등의편의증진보장에관한법률` (Act shell). Prior: iframe shell giving the Act's lsiSeq.
  Result R6: 200, 158317 bytes, artefact 7f0d40fff30743f5.pdf.
  Result R7: 200, 87832 bytes, artefact 418c8dbed012ef70.pdf.
  Result R8: 200, 1339 bytes, artefact 7b08e91550f1e9f5.html; iframe to lsiSeq=285263, efYd=20260702. The Rule in force is therefore effective 2026-07-02, LATER than the held annex stamp <개정 2023. 12. 11.>. Prior not met in the interesting direction: the held REF-01031 file may not be the current annex.
  Result R9: 200, 1327 bytes, artefact 5d25743e1d727244.html; iframe to lsiSeq=267429, efYd=20251221.
- R10 fetch `https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=285263&chrClsCd=010202&urlMode=lsInfoP&efYd=20260702&ancYnChk=0` (Rule body). Prior: 200 body with an annex list; 별표 1 "편의시설의 구조ㆍ재질등에 관한 세부기준" carrying a flSeq different from 162983711 and an amendment stamp later than 2023-12-11.
- R11 fetch `https://www.law.go.kr/LSW/lsInfoR.do?lsiSeq=267429&chrClsCd=010202&urlMode=lsInfoP&efYd=20251221&ancYnChk=0` (Act body). Prior: 200 body, definitions in art. 2.
  Result R10: first attempt exit 35 (TLS, transient, empty artefact e3b0c442…); retry 200, 114668 bytes, artefact 5c7c9db943614f9f.html. Header: "[시행 2026. 7. 2.] [보건복지부령 제1166호, 2026. 4. 1., 일부개정]". Annex list: 별표 1 "편의시설의 구조·재질등에 관한 세부기준(제2조제1항관련)" HWP flSeq=162950007, PDF flSeq=162950009; 별표 2 "편의시설의 안내표시기준(제3조관련)" PDF 162950097; 별표 3 (wheelchairs to be kept) PDF 162950103; forms.
  Result R11: 200, 155972 bytes, artefact 8883966f2cba408a.html.
- R12 fetch `https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162950009&bylClsCd=110201` (Rule 별표 1 PDF as linked from the in-force body). Prior: 200 PDF; possibly byte-identical to 162983711 if the 2026-04-01 amendment did not touch 별표 1, otherwise a later stamp.
- R13 fetch `https://www.law.go.kr/LSW/flDownload.do?gubun=&flSeq=162950097&bylClsCd=110201` (Rule 별표 2, signage standard PDF). Prior: 200 PDF, pictogram table (image-heavy).
  Result R12: 200, 489120 bytes, sha256 b71c64f1a9b3125fbedc6fce85831ef3964819988ce76d5aac4ba26eb0902c63: byte-identical to the held file. The in-force Rule (2026-07-02) links the SAME 별표 1 bytes, stamped <개정 2023. 12. 11.>, so the held annex is current as of today's portal state.
  Result R13: first attempt exit 35 (empty artefact e3b0c442…); retry 200, 68977 bytes, artefact 788c3fe703cb3d54.pdf, one page, stamp <개정 2023. 12. 11.>; text plus a drawing ("작도법") that is an image.
- Text extraction: `pdftotext` (poppler, no -layout) for the four PDFs; `tools/h2t.py` (tag strip) for the three lsInfoR HTML bodies. Reading copies were made with `pdftotext -layout` outside the repo; quotes are verified against the saved non-layout text.

## Absence and sense checks inside the read texts (whitespace-stripped substring counts over all seven saved texts; prior written before running)
