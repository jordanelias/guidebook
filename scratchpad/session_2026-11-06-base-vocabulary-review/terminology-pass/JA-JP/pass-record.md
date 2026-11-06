# Terminology pass JA/JP — pass record (session_2026-11-06-base-vocabulary-review, 2026-11-06)

**Verdict.** The binding instruments are read in full and recorded: the Cabinet Order (政令379, Arts 1–32) and the guidance-standard Ordinance (省令114, Arts 1–19). The Act (法91) is read for its definitions and building chapter, and the enforcement rules (規則110) for Arts 1–3. The MLIT 建築設計標準（令和７年度改正版）, 260 pp., is only **partly** read: about 40 pages in full, plus about 25 pages where one clause was found by grep and read. So every SEARCHED-ABSENT result rests on the law texts plus a grep of the design standard, not on reading the whole standard. JIS T 9251 and JIS Z 8210 are NOT-OBTAINABLE (JISC down, and both are sold by JSA). The 2024 MLIT notices (告示1072–1074), the 付録 and the 当事者参画 guideline were found but not fetched (budget). Nothing was written to the DB, committed or pushed.

## Retrieved (all 200; bytes under retrieval-log/session_2026-11-06-base-vocabulary-review/, text under text/)
e-Gov API v2 JSON: 法91, 政令379, 規則110, 省令113, 省令114, all CurrentEnforced (per e-Gov revision_info: 2025-04-01 for the Act, 2025-06-01 for the others). MLIT index page (moved; the registry URL is stale). The design-standard PDF (59.9 MB). The JISC probe returned a 502 maintenance page. Per-instrument read/skipped detail: instruments.tsv.

## Counts (re-run, do not trust; run from the repo root, P=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/JA-JP)
- Observations 104, distinct phrases 98: `tail -n +2 $P/observations.tsv | wc -l`, `… | cut -f4 | sort -u | wc -l`
- Reverse-harvest rows 53: `tail -n +2 $P/reverse-harvest.tsv | wc -l`
- Register concepts 60 (32 statements from 2.1, 18 words from 2.2, 10 active parameters, all derived by `tools/build.py` from the catalogue and the DB). Coverage: 50 FOUND, 8 FOUND but grep-located only, 2 SEARCHED-ABSENT (microwave height; colour temperature), 0 NOT-OBTAINABLE at concept level. `tail -n +2 $P/coverage.tsv | cut -f4 | sed 's/ (shared.*//; s/ (grep.*/-GREP/' | sort | uniq -c`. Seven FOUND rows are "shared": the register lists the same concept twice.
- Quote checks: 146 exact, 7 match after whitespace normalisation, 4 match after joining wrapped PDF lines, 0 missing (`python3 -I $P/tools/verify.py $P/tools $P/text`). The check is my script against my saved text files, not `retrieval_log.quote_in_artefacts` (see defect 3).
- Held JA aliases found verbatim somewhere in the persisted texts: 33 of 150 (inline script in the transcript: substring match of `term_aliases` where language='ja'). That is substring presence only: 有効幅 counts because it sits inside 有効幅員. It is not attestation.

## Where English and Japanese carve the field differently
1. **Applicability is by building class and user population, not by element.** Every clause opens 「不特定かつ多数の者が利用し、又は主として高齢者、障害者等が利用する…」. Duties attach to 特別特定建築物 above a floor area (Order Art. 9), with a best-effort tier (特定建築物) and a guidance tier (誘導基準) tied to certification and a floor-area-ratio bonus. The register has no tier or class axis.
2. **The ostomy toilet is hidden in the statute.** The Order says only 「高齢者、障害者等が円滑に利用することができる構造の水洗器具を設けた便房」 (Art. 14(3)). The design standard files the same clause under 「オストメイト用設備を有する便房」 (pdf p.128). The register has no ostomy concept. A seed made from English "faucet" or "fixture" would point at 水栓, the wrong object.
3. **Ramp landings are set by rise, not run.** The landing rule is 「高さ七十五センチメートル以内ごとに…踊場」, so the register's *ramp run length* (P12) has no counterpart. Likewise *turning circle* is carved by function: 車椅子の転回に支障がない場所 (corridors, every 50 m), 140㎝角, and 「直径150㎝以上の円が内接できるスペース」 (rooms). 回転 (360°) and 転回（方向転換） are distinguished.
4. **Contrast is hue, value and saturation, not LRV.** The law writes 「色の明度、色相又は彩度の差」. The design standard adds 輝度比 and 輝度コントラスト. LRV does not occur.
5. **Reverberation has no time quantity.** It appears only as 「響きの抑制」 together with 騒音の低減. 残響 occurs nowhere in the texts.
6. **Tactile indicators come as a defined pair** (点状ブロック等 for warning, 線状ブロック等 for guidance). The register names only truncated domes.
7. **Toilets have two levels and a typology.** 便所 (the room) contains 便房 (cubicles). The cubicle types are 車椅子使用者用便房, オストメイト, 乳幼児, and 男女共用の広めの便房, and the technique 機能分散 spreads functions across them. English "accessible washroom" collapses all of this.
8. **The population carve differs.** One statutory class, 高齢者、障害者等, is read by the standard to include intellectual, psychiatric and developmental disability. The standard also lists 色覚多様性のある人, 内部障害者 and 重複障害 as user groups.
9. **Staffing substitutes for provision.** A 案内所 exempts a building from the sign-board and braille-map duties (Order Art. 21(3)).

## Defects in the METHOD
1. **The register's concepts are not atomic.** C02, C11 and C14 are one concept worded three ways, and so are C01/C13, C10/C28 and C22/C29. RHFAC phrasing variants become separate concepts, which inflates coverage. The 2.1 list needs deduplication before any pair is run.
2. **The English register names objects; Japanese law names performance and structure.** "Accessible door hardware" maps to a door *structure* (自動的に開閉する構造…). "Level threshold" has no noun; the law says 戸の前後に高低差がない. "Seating" becomes 休憩の用に供する設備. A concept-by-concept FOUND therefore overstates equivalence. The coverage column needs a carve-relation field (same / narrower / wider / different axis), not FOUND alone.
3. **Tooling gap: quote verification.** `retrieval_log.quote_in_artefacts` cannot search PDF artefacts ("bytes undecodable"; all 5 session PDFs skipped), so the principal guidance text cannot be verified by the sanctioned tool. It also misses e-Gov JSON quotes that cross ruby markup (Order Art. 13(1)(1), 勾配; measured False). Separately, my own first converter inlined the ruby reading as 「勾こう配」. I caught and corrected this (search-log, CORRECTION entry). Any JA/ZH/KO pass meets ruby, and nothing in the pipeline normalises it.
4. **Orthographic variants inside one instrument.** The standard writes 蹴上げ and けあげ, 踏面 and 踏み面, 浮彫 (heading) and 浮き彫り (body). 省令113 still says 日本工業規格 where 省令114 says 日本産業規格. Exact-string attestation splits these into separate aliases unless variant folding is defined.
5. **SEARCHED-ABSENT needs "read in full"**, and a 260-page guidance document is not read in full in one pass. The method should name the principal binding text as the unit for absence, and treat guidance as located-only, or budget it explicitly.
6. **e-Gov definition items are two-column cells** (term | definition). A converter must choose a separator; I used a space, so those quotes contain a space the instrument does not print.
7. **The retrieval logger saved the MLIT XHTML index with an .xml extension, and stores a 60 MB PDF under retrieval-log/.** Check the size against the repository's policy before committing.
8. **Stale prose callers.** references/standards-registry.md gives the old MLIT URL (now a Shift_JIS redirect stub) and dates JIS T 9251 to 2001 where lead 50 says 2014. Not edited (out of scope).

## Self-attack: the five likeliest ways this record is wrong
1. **Partial read presented as coverage.** 8 FOUND rows rest on a single grep-located clause, and both SEARCHED-ABSENT rows rest on a grep of a text only about 15% read. Microwave height or colour temperature could sit in a figure, a table image, or a page I skipped.
2. **Wrong concept mapping.** Mapping 優先席 to Seating, クリアランス (hinge gap) to "clearance", or 天井高さ in a parking photo caption to height clearance may be loose. Each is a sighting of the string, not proof of the same concept. Notes flag them, but the FOUND status still counts them.
3. **Locator drift.** Design-standard locators combine the pdf page index and the printed page number, mapped by footer. Two-column layout can misattribute a line to a neighbouring clause. The line-joined matches (4) are the most exposed.
4. **Edition currency.** "In force" comes from e-Gov's revision_info and the PDF cover, not from an amendment history read end to end. A later 告示 could change delegated structures that I did not retrieve.
5. **Gloss leakage.** The reverse-harvest glosses are mine and marked as such. Read as equivalents, they would reintroduce exactly the English framing E1 forbids. The 2.2 quantity words are also English lemmas, so "Q-level" mixing 高低差 and 水平 is my grouping.

Files: search-log.md, instruments.tsv, observations.tsv, coverage.tsv, reverse-harvest.tsv, seeds.tsv (9 MODEL-GENERATED), text/*.txt, tools/ (converter, verifier, data, builder — reproducible).
