# Search log — terminology pass JA/JP (session_2026-11-06-base-vocabulary-review)

Each entry: query verbatim; PRIOR (written before the query ran); RESULT; SHAPE note (R14). Empty and failed results kept.

## Q1. Local derivation of candidate instruments (DB, read-only)
- Query: `select * from research_code_leads where jurisdiction like '%JP%'`; `select ref_id, pub_title, standard_number from evidence_sources where jurisdiction='JP'`; `grep -n -i 'japan\|JP\b\|JIS\|バリアフリー' references/standards-registry.md`
- PRIOR: one or two leads (JIS T 9251, the Barrier-Free Act); held e-Gov texts possibly from the ramp-gradient batches.
- RESULT: leads 50 (JIS T 9251:2014, REFERENCE-ONLY) and 85 (Barrier-Free Act / Cabinet Order 379/2006 Art. 19 / MLIT Ordinance 114/2006). Held: REF-00990 (Cabinet Order 379/2006, laws.e-gov.go.jp/law/418CO0000000379), REF-00991 (MLIT Ordinance 114/2006, 418M60000800114), plus two secondary items (REF-00989 blog, REF-00993 DPI Japan). Registry lists "建築物移動等円滑化誘導基準 (2024 revision)" with MLIT barrier-free page, and JIS T 9251:2001 (registry says 2001; lead says 2014 — edition conflict, unresolved by this pass).
- SHAPE: structured lookups, well-formed. The Act itself (法律) is not held; the enforcement ordinance (施行規則) is not held; MLIT 建築設計標準 not held.

## Q2. e-Gov law search API (v2) by title
- Query: `https://laws.e-gov.go.jp/api/2/laws?law_title=高齢者、障害者等の移動等の円滑化` (URL-encoded)
- PRIOR: returns the Act (法律第九十一号, 2006), its Cabinet Order (政令379), its enforcement rules (省令), the guidance-standard ordinance (省令114), and possibly transport/route ordinances; current revision dates.
- RESULT: 8 hits, all CurrentEnforced. Building-relevant: 418AC0000000091 Act (rev. in force 2025-04-01); 418CO0000000379 Cabinet Order (2025-06-01); 418M60000800110 enforcement rules (2025-06-01); 418M60000800113 ordinance on signs under Order Art. 20 (2025-06-01). Others are land readjustment, public transport projects, passenger counting, traffic signals (out of building scope). MLIT Ordinance 114/2006 did NOT appear: its title does not contain the searched string (it begins 高齢者、障害者等が円滑に利用できるようにするために誘導すべき…). 
- SHAPE: title-substring search; the miss of 114 is a query-shape artefact, not absence (R14). Building-sector ordinances whose titles do not begin with the Act's name are unreachable this way.

## Q3. e-Gov law_data retrieval of five texts (current revision)
- Query: `https://laws.e-gov.go.jp/api/2/law_data/<id>` for 418AC0000000091, 418CO0000000379, 418M60000800110, 418M60000800113, 418M60000800114
- PRIOR: JSON with full article tree. Order 379 Arts 10–24 hold the 建築物移動等円滑化基準 (mandatory); 114 holds the 誘導基準 (voluntary higher standard); 110 holds supplementary details (signs, information for visually impaired); 113 is short (the sign); the Act Art. 2 holds the defined terms.
- RESULT: all five 200 OK, JSON persisted (sha256 in instruments.tsv). Order 379 and Ordinance 114 bytes are byte-identical to the 2026-09-17 retrievals (same sha256 6ac7f09b…, edd9f6fc…), i.e. the 2025-06-01 revision was already current then. Converted to locator-tagged text (scratchpad tool egov2txt.py, outside the repo).
- SHAPE: direct ID retrieval, no search ambiguity. Observed text artefact: e-Gov renders ruby (furigana) inline, so Order 379 Art. 13(1)(1) and Ordinance 114 Art. 6(1)(2) read 「勾こう配」, while neighbouring clauses read 「勾配」. A grep for 勾配 misses those two clauses; quote verification must use the inline-ruby form.

## Q4. MLIT barrier-free building page (registry source_url) — locate the 建築設計標準
- Query: `https://www.mlit.go.jp/jutakukentiku/build/barrier-free.html`
- PRIOR: an index page linking the 高齢者、障害者等の円滑な移動等に配慮した建築設計標準 (latest revision, probably 令和6/7年) as a set of chapter PDFs; possibly 404 if MLIT reorganised URLs.
- RESULT: 200, 1172 bytes, Shift_JIS meta-refresh stub: page moved to https://www.mlit.go.jp/jutakukentiku/jutakukentiku_house_fr_000049.html. Registry source_url is stale (prose caller drift; not edited here).
- SHAPE: well-formed; the stub is evidence of a URL move, not of absence.

## Q5. MLIT moved page
- Query: `https://www.mlit.go.jp/jutakukentiku/jutakukentiku_house_fr_000049.html`
- PRIOR: index with links to 建築設計標準 PDFs and the 2025 revision notice.
- RESULT: 200, 26194 bytes (artefact 141828ea…, saved with .xml extension by the logger — an extension-sniffing quirk; it is XHTML). Lists: Act/Order/Rules/Ordinance PDFs; 2024 MLIT notices 1072–1074 (令和６年国土交通省告示); the current guidance 「高齢者、障害者等の円滑な移動等に配慮した建築設計標準（令和７年度改正版）」 本編 = /jutakukentiku/content/001892119.pdf, 付録 = 001892120.pdf; separate volumes 「建築プロジェクトの当事者参画ガイドライン」, 「バリアフリー改修・改善のポイント」, 設計事例集; and a notice on automatic unlocking of 車椅子使用者用便房（バリアフリートイレ）.
- SHAPE: index page; the guidance edition is read from the page's own label, not assumed.

## Q6. 建築設計標準（令和７年度改正版）本編 PDF
- Query: `https://www.mlit.go.jp/jutakukentiku/content/001892119.pdf`
- PRIOR: very large PDF (several hundred pages, tens of MB), text-extractable; chapter 2 「単位空間等の設計」 by element (敷地内通路, 駐車場, 出入口, 屋内通路, 階段, 昇降機, 便所, …). May time out on size.
