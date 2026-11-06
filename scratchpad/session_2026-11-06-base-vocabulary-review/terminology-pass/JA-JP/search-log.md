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
- RESULT: 200, 59,903,589 bytes, 260 pages, cover 「令和７（２０２５）年５月 国土交通省」. pdftotext -layout succeeded (Japanese text extractable; figures not). Read status recorded in instruments.tsv (partly).
- SHAPE: direct retrieval. Note the artefact is ~60 MB inside retrieval-log/ (tracked path?) — size is a tooling concern for the commit, flagged in pass-record.

## Q7. JIS T 9251 (tactile walking surface indicators) — JISC
- Query: `https://www.jisc.go.jp/app/jis/general/GnrJISNumberNameSearchList?toGnrJISStandardDetailList&jisStdNo=T9251`
- PRIOR: JISC is a JavaScript/login-gated viewer; free on-screen viewing only, no downloadable text. Expect a page shell or redirect, no standard text. NOT-OBTAINABLE is the expected outcome.
- RESULT: HTTP 502, 5208 bytes: JISC 「サービス停止のお知らせ … 只今メンテナンスのため、システムを停止しています」. No standard text. JIS T 9251 and JIS Z 8210 (the latter named in Ordinance 114 Art. 14(2)) are NOT-OBTAINABLE in this pass; purchase is through the Japanese Standards Association (named on the same page). Not substituted from memory.
- SHAPE: well-formed URL; the outage makes this a non-result, not evidence of absence. One attempt only (budget).

## Q8–Q10. In-text location greps over the persisted texts (not web searches)
- Q8 query: Python `str.count` / page scan over text/1bc5c919cb81e7bf.txt for: 照明 照度 排水 有効幅 有効高さ 天井高 残響 輝度 明度 色温度 操作力 ヒアリングループ 磁気ループ 集団補聴 補聴 ロッカー 電子レンジ コンセント スイッチ レバーハンドル 把手 取っ手 蹴込み 脱輪 立ち上がり 庇 ひさし 屋根 水栓 オストメイト 水洗器具 段差 転回 回転 直径 アプローチ グラブ 排水溝 グレーチング 休憩 ベンチ いす 椅子 カームダウン クールダウン 色覚 反射 まぶしさ グレア 開閉力 開閉 触知 点字 音声案内 ピクトグラム 高低差 有効 すりつけ 手すり 段鼻 ノンスリップ 滑り
- PRIOR (written before running): the design standard uses 有効幅員 rather than 有効幅; uses 手すり heavily; probably has 照度 and コンセント; I expected 残響時間 to be absent from a design standard of this kind and 色温度 absent; I expected 磁気ループ rather than ヒアリングループ (wrong — see result); 電子レンジ expected absent.
- RESULT: zero hits: 有効高さ, 残響, 色温度, 操作力, 磁気ループ, 電子レンジ, 把手, ひさし, グラブ, グレーチング, まぶしさ, 開閉力, すりつけ. 有効幅 70 (all inside 有効幅員), ヒアリングループ 7, 集団補聴 18, 照度 4, 輝度 9, 明度 27, 色覚 30, 響き (separate query) present as 「響きの抑制」. Page lists recorded in the transcript.
- SHAPE: exact-string search over pdftotext output. A zero is evidence that the string is absent from the extracted text only (figures, tables rendered as images and hyphenated line breaks are invisible to it). It is not evidence that the concept is absent: e.g. reverberation is treated as 「響きの抑制」, not as 残響.
- Q9 query: context-line scan for 軽い力 操作に要する力 響き 照度 ロッカー 自動水栓 レバー式 電子レンジ 色温度 シェルター 上屋 車寄せ 有効幅員 戸の有効幅 前面 アプローチ 直径150 150㎝以上の円 エスコートゾーン
- PRIOR: 軽い力 for door operation; 直径150㎝ for turning space; 上屋 for shelter.
- RESULT: as expected for those three; 操作に要する力, 自動水栓, シェルター, 色温度, 電子レンジ zero; 戸の有効幅 zero (the standard writes 出入口の有効幅員).
