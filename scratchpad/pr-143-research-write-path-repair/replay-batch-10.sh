#!/usr/bin/env bash
# Batch 10 — the threshold pass. Every write, in order, against a SCRATCH copy.
#
# WHY THIS EXISTS. The batch was first run command-by-command and a probe of a
# refusal (REF-09999) survived into the scratch, because the guard being probed
# fired AFTER insert_evidence_source. Rebuilding from the canonical blob and
# replaying is the only way to be sure the emitted migration carries the batch
# and nothing else. Re-runnable from scratch; `emit_batch_sql.py` then diffs
# this scratch against canonical.
set -euo pipefail
S="${SCRATCH:?set SCRATCH to the scratch dir}"
SID=session_2026-09-17-research-batch-10-ramp-gradient-threshold
export GUIDEBOOK_DB_PATH="$S/batch10.db"
rm -f "$GUIDEBOOK_DB_PATH"; cp data/guidebook.db "$GUIDEBOOK_DB_PATH"
db(){ python3 scripts/db.py "$@" --session "$SID" >/dev/null; }

# ---- Leg A row 1: JP, Cabinet Order 379/2006 + MLIT Ordinance 114/2006 -------
db add-source --ref-id REF-00990 --year 2006 \
  --author 'corp|内閣（Cabinet of Japan）' \
  --title '高齢者、障害者等の移動等の円滑化の促進に関する法律施行令（平成十八年政令第三百七十九号）' \
  --tier 6 --jurisdiction JP --evidence-type code --scope intrinsic \
  --pages '第十九条第二項第四号ロ／第七号ニ（２）' \
  --url 'https://laws.e-gov.go.jp/law/418CO0000000379' --url-accessed 2026-09-17 \
  --lang-detected ja --metadata-quality COMPLETE-STATUTORY \
  --verification-status VERIFIED --verification-method tool --verified-by-tool e-gov-api \
  --slug accessible-circulation-geometry --local-ref-id 9

db add-source --ref-id REF-00991 --year 2006 \
  --author 'corp|国土交通省（Ministry of Land, Infrastructure, Transport and Tourism）' \
  --title '高齢者、障害者等が円滑に利用できるようにするために誘導すべき建築物特定施設の構造及び配置に関する基準を定める省令（平成十八年国土交通省令第百十四号）' \
  --tier 6 --jurisdiction JP --evidence-type code --scope intrinsic \
  --pages '第十一条第一項第六号ロ' \
  --url 'https://laws.e-gov.go.jp/law/418M60000800114' --url-accessed 2026-09-17 \
  --lang-detected ja --metadata-quality COMPLETE-STATUTORY \
  --verification-status VERIFIED --verification-method tool --verified-by-tool e-gov-api \
  --slug accessible-circulation-geometry --local-ref-id 10

# ---- Leg A row 3: GB, Approved Document M Vol 2 ------------------------------
db add-source --ref-id REF-00992 --year 2015 \
  --author 'corp|HM Government (Crown copyright)' \
  --title 'The Building Regulations 2010 — Approved Document M: Access to and use of buildings, Volume 2: Buildings other than dwellings (2015 edition incorporating 2020 and 2024 amendments)' \
  --tier 6 --jurisdiction GB --evidence-type code --scope intrinsic \
  --pages 'Section 1, para 1.26(b)–(c) and Table 1 (Limits for ramp gradients), p.19–20' \
  --url 'https://assets.publishing.service.gov.uk/media/66f6c5eec71e42688b65ee11/ADM__V2_with_2024_amendments.pdf' \
  --url-accessed 2026-09-17 --lang-detected en --metadata-quality COMPLETE-STATUTORY \
  --verification-status VERIFIED --verification-method tool --verified-by-tool gov-uk-assets \
  --slug accessible-circulation-geometry --local-ref-id 11

# ---- Leg D row 11: JP, DPI Japan (Co-1) -------------------------------------
db add-source --ref-id REF-00993 --year 2023 \
  --author 'corp|DPI日本会議（DPI-Japan, Japan National Assembly of Disabled Peoples International）' \
  --title '【バリアフリー】DPI日本会議 総括所見の分析と行動計画②' \
  --tier 1 --jurisdiction JP --evidence-type co1 --scope intrinsic \
  --co1-source-type dpo_position_statement \
  --co1-provenance 'DPI日本会議 (DPI-Japan) is the Japan national assembly of Disabled Peoples International — a cross-disability organisation OF disabled people, not a service provider for them, and DPI'"'"'s defining constitutional requirement is majority control by disabled people. The document is its own analysis of the CRPD Committee'"'"'s 2022 Concluding Observations on Japan and its resulting action plan, i.e. a DPO speaking in its own voice about the barrier-free standards its members live under. Evidenced in the retrieved bytes rather than inferred from venue (D-0178): the page is published under dpi-japan.org as the organisation'"'"'s own 要望・声明 (demands and statements) workstream output.' \
  --pages '2．法律・制度・施策の改善ポイント（2）バリアフリー法の課題／義務基準が不十分' \
  --url 'https://dpi-japan.org/blog/workinggroup/traffic/barrier-free-crpd/' \
  --url-accessed 2026-09-17 --lang-detected ja --metadata-quality COMPLETE \
  --verification-status VERIFIED --verification-method tool --verified-by-tool retrieval-log \
  --doi-resolution-outcome NO-MATCH \
  --slug accessible-circulation-geometry --local-ref-id 12

# ---- Extractions -------------------------------------------------------------
db add-extraction --ref-id REF-00990 --slug accessible-circulation-geometry \
  --parameter-id 3 --identity MOB --jurisdiction JP \
  --claim-type numerical --claimed-value '1:12' --claimed-unit 'rise:run ratio' --comparator '<=' \
  --claim-text '勾配は、十二分の一を超えないこと。' \
  --source-section '第十九条第二項第四号ロ（移動等円滑化経路を構成する傾斜路）' \
  --root-type committee_assertion --root-ref-id REF-00990 \
  --measurement-paradigm stated_unmeasured --device-class not_device_scoped \
  --extraction-method full-read --extraction-status verified \
  --figure-role claim --relation none \
  --notes 'THE MANDATORY JAPANESE CEILING, and the instrument that actually carries it. Cabinet Order 379/2006 is the 建築物移動等円滑化基準, the binding minimum. The identical sentence appears twice in Art.19(2) — item (iv)ro for ramps on an accessible route replacing or beside stairs, and item (vii)ni(2) for ramps on 敷地内の通路 — so ONE extraction is filed, because it is one figure stated twice and not two figures. Numerically identical to REF-00987 (ADA 1:12) from a wholly separate legal lineage, so this is convergence, not the convergence-by-descent the plan flagged for CA/US. relation=none is literal: the Order names no reference and states no warrant for 1/12. Stored as the source states it, a fraction; 1:12 = 8.33 percent = 4.76 degrees for reconciliation against the degree-denominated research rows, and that conversion is NOT stored.'

db add-extraction --ref-id REF-00990 --slug accessible-circulation-geometry \
  --parameter-id 3 --identity MOB --jurisdiction JP \
  --claim-type numerical --claimed-value '1:8' --claimed-unit 'rise:run ratio' --comparator '<=' \
  --claim-text 'ただし、高さが十六センチメートル以下のものにあっては、八分の一を超えないこと。' \
  --source-section '第十九条第二項第四号ロただし書（移動等円滑化経路を構成する傾斜路）' \
  --root-type committee_assertion --root-ref-id REF-00990 \
  --measurement-paradigm stated_unmeasured --device-class not_device_scoped \
  --extraction-method full-read --extraction-status verified \
  --figure-role condition --relation none \
  --notes 'A RELAXATION, NOT A SECOND CEILING — filed as `condition` so the determination engine does not gather it as a governing claim. 1:8 (12.5 percent) applies ONLY where the rise is 16 cm or less, and it is materially steeper than every other figure in this corpus including the German 6 percent. It is the shape the owner statement of 2026-09-16 warns about: a short rise buys a steeper gradient, which is a trade the code permits and the dose-response evidence does not endorse. Recording it as a condition keeps both facts — the permission is real, and it is not what the jurisdiction requires of ramps generally.'

db add-extraction --ref-id REF-00991 --slug accessible-circulation-geometry \
  --parameter-id 3 --identity MOB --jurisdiction JP \
  --claim-type numerical --claimed-value '1:15' --claimed-unit 'rise:run ratio' --comparator '<=' \
  --claim-text '勾配は、十五分の一を超えないこと。' \
  --source-section '第十一条第一項第六号ロ（敷地内の通路の傾斜路）' \
  --root-type committee_assertion --root-ref-id REF-00991 \
  --measurement-paradigm stated_unmeasured --device-class not_device_scoped \
  --extraction-method full-read --extraction-status verified \
  --figure-role claim --relation none \
  --notes 'THE FIGURE THE CORPUS HELD SECOND-HAND AND MISATTRIBUTED. REF-00989 (Co-1) attributes 1/15 to the Barrier-Free Law as the OUTDOOR figure. It is not in that law: 十五分の一 occurs ZERO times in Cabinet Order 379/2006. It is here, in MLIT Ordinance 114/2006 — the 誘導基準, the ENHANCED standard a building meets voluntarily to be certified, not the mandatory minimum. The domain is roughly what REF-00989 says (敷地内の通路, paths within the site, typically outdoors) but the legal force is not: nothing requires 1/15 of anyone. So the three figures REF-00989 presents as one law are two instruments at two different strengths. This matters beyond bookkeeping — a reader taking the Co-1 source at face value believes Japan requires 1/15 outdoors, and a determination built on that would overstate the regulatory floor. relation=none: the Ordinance states 1/15 absolutely and names no warrant for it.'

db add-extraction --ref-id REF-00992 --slug accessible-circulation-geometry \
  --parameter-id 3 --identity MOB --jurisdiction GB \
  --claim-type numerical --claimed-value '1:20' --claimed-unit 'rise:run ratio' --comparator '<=' \
  --claim-text 'Table 1 Limits for ramp gradients Going of a flight Maximum gradient Maximum rise 10m 1:20 500mm 5m 1:15 333mm 2m 1:12 166mm' \
  --verbatim-exempt 'The persisted artefact is a FlateDecode-compressed PDF (1,471,989 bytes, sha256 0e5d4dee25b341f4e80a99a40a6b36bb1a0251926867aa17e9f71e5b12a1046c), so no substring of its rendered text occurs in its bytes. Read off p.19-20 of that exact artefact via pypdf and reproduced character for character, including the tables column order. gov.uk publishes no HTML carrier of Table 1.' \
  --source-section 'Section 1, para 1.26(b)-(c), Table 1' \
  --root-type committee_assertion --root-ref-id REF-00992 \
  --measurement-paradigm stated_unmeasured --device-class not_device_scoped \
  --extraction-method full-read --extraction-status verified \
  --figure-role claim --relation none \
  --notes 'THE GOVERNING UK FIGURE IS 1:20, NOT 1:12, AND THE DIFFERENCE IS STRUCTURAL. AD M does not state a single ceiling: it conditions gradient on the GOING of the flight. 1:12 is permitted only for a 2 m going, which buys 166 mm of rise; a full 10 m flight is capped at 1:20. Filed at 1:20 because that is the limit for the longest flight the table admits and therefore the governing value for a ramp of any length; the 1:12 and 1:15 rows are filed as conditions. THIS BREAKS NUMERIC COMPARISON ACROSS THE CORPUS: REF-00987 (ADA) and REF-00990 (JP) both state a flat 1:12 with no length term in the same clause, so a table reading 1:12 = 1:12 = 1:12 across US/JP/GB would be false three ways. relation=none: AD M states Table 1 on its own authority. It cites BS 8300 in its standards list but attributes no figure in Table 1 to it, so nothing is inferred about BS 8300 from here — which is what Leg B row 6 exists to test.'

db add-extraction --ref-id REF-00992 --slug accessible-circulation-geometry \
  --parameter-id 3 --identity MOB --jurisdiction GB \
  --claim-type numerical --claimed-value '1:12' --claimed-unit 'rise:run ratio' --comparator '<=' \
  --claim-text 'Table 1 Limits for ramp gradients Going of a flight Maximum gradient Maximum rise 10m 1:20 500mm 5m 1:15 333mm 2m 1:12 166mm' \
  --verbatim-exempt 'Same persisted artefact and method as the sibling 1:20 extraction: FlateDecode-compressed PDF, sha256 0e5d4dee25b341f4e80a99a40a6b36bb1a0251926867aa17e9f71e5b12a1046c, read via pypdf from p.19-20. One table row, filed separately because it states a different figure under a different condition.' \
  --source-section 'Section 1, Table 1, row: going 2m' \
  --root-type committee_assertion --root-ref-id REF-00992 \
  --measurement-paradigm stated_unmeasured --device-class not_device_scoped \
  --extraction-method full-read --extraction-status verified \
  --figure-role finding --relation none \
  --notes 'FILED AS finding, NOT condition, AND THE REASON IS MECHANICAL. extraction_relations_integrity holds that a condition qualifying nothing is not a condition: it must be the target of an edge or the source of a condition_on edge. No edge from or to any AD M row can exist, because _write_relation_edge requires --quote with NO exemption (unlike --claim-text) and REF-00992 is a FlateDecode-compressed PDF whose rendered text is not a substring of its bytes under any normalisation. The batch-10 plan predicted this casualty for AD M by name. finding is accurate rather than a demotion of convenience — like extraction 18, the ADA advisory, it records something the source states that is NOT its governing ceiling — and it preserves the protection condition was chosen for, since gather_sources takes claim and derived only. THE UK 1:12 IS NOT THE US OR JAPANESE 1:12. It is admissible only for a going of 2 m, capped at 166 mm of rise — roughly one step. Filed as `condition`, not `claim`, so the determination engine does not gather it as a governing ceiling and so a cross-jurisdiction table cannot read three identical 1:12s as agreement. AD M adds that goings between 2 m and 10 m may be interpolated (1:14 at 4 m, 1:19 at 9 m), which is a continuous rule, not three discrete options.'

db add-extraction --ref-id REF-00993 --slug accessible-circulation-geometry \
  --parameter-id 3 --identity MOB --jurisdiction JP \
  --claim-type qualitative --claimed-value 'mandatory standard insufficient for smooth use' \
  --claim-text '国際パラリンピック委員会が策定したバリアフリー整備基準「IPCアクセシビリティガイド」に比べて、特に建物関係はバリアフリー法の義務基準が低く、移動等円滑化基準（義務基準）だけでは円滑な利用ができない。' \
  --source-section '2．法律・制度・施策の改善ポイント（2）／義務基準が不十分' \
  --root-type participatory_finding --root-ref-id REF-00993 \
  --measurement-paradigm stated_unmeasured --device-class not_device_scoped \
  --extraction-method full-read --extraction-status verified \
  --figure-role finding --relation none \
  --notes 'THE DPO SAYS THE INSTRUMENT ADMITTED AS REF-00990 IS NOT ENOUGH. DPI Japan, assessing Japan against the CRPD Committee 2022 Concluding Observations, states that the Barrier-Free Act mandatory standards are LOW compared with the IPC Accessibility Guide, particularly for buildings, and that the 移動等円滑化基準 ALONE does not permit 円滑な利用 (smooth use). Owner ruling 2026-09-13 governs: a finding that a CODE is insufficient supplies no value and is still first-class evidence. figure_role=finding, claimed value deliberately non-numeric. SCOPE DISCIPLINE, STATED SO IT IS NOT OVER-READ LATER: this document does NOT discuss ramp gradient. 勾配, スロープ and 傾斜 occur ZERO times in the retrieved bytes; its worked examples are toilets and parking bays. It is evidence that the mandatory standard as a WHOLE is judged inadequate by the people it governs — which bears directly on whether 1:12 can be read as a threshold of acceptability — and it is NOT evidence about the gradient figure specifically. Anyone later citing this row for a gradient claim is over-reading it.'

# ---- The JP proviso edge. Ids are DERIVED, never hard-coded (rule 8): they are
# ---- assigned at insert time and a literal here would rot on any replay.
JP12=$(python3 -c "import sqlite3,os;c=sqlite3.connect('file:'+os.environ['GUIDEBOOK_DB_PATH']+'?mode=ro',uri=True);print(c.execute(\"select extraction_id from source_value_extractions where ref_id='REF-00990' and claimed_value='1:12'\").fetchone()[0])")
JP8=$(python3 -c "import sqlite3,os;c=sqlite3.connect('file:'+os.environ['GUIDEBOOK_DB_PATH']+'?mode=ro',uri=True);print(c.execute(\"select extraction_id from source_value_extractions where ref_id='REF-00990' and claimed_value='1:8'\").fetchone()[0])")
db relate-extraction --from "$JP8" --relation condition_on --to-extraction "$JP12" --stated named \
  --quote 'ただし、高さが十六センチメートル以下のものにあっては、八分の一を超えないこと。' \
  --notes 'The 1:8 relaxation QUALIFIES the 1:12 ceiling in the same clause: it is the ただし書 (proviso) to Art.19(2)(iv)ro, admissible only where the rise is 16 cm or less. condition_on so the engine reads 1:8 as a qualification of 1:12 rather than as a competing Japanese ceiling. stated=named because the proviso is attached to the ceiling by the statute itself, in one sentence pair — nothing here is inferred.'

# ---- K02: the live determination cannot account for this batch's evidence -----
db retire-specification --specification-id 3 \
  --reason 'Batch 10 admitted four sources and six extractions for parameter 3 that this determination predates: REF-00990/REF-00991 (the Japanese mandatory ceiling and the voluntary guideline standard), REF-00992 (AD M length-conditioned table) and REF-00993 (DPI Japan Co-1 inadequacy finding). K02 fires correctly — derivation_sha hashes the junction, so leaving the row would attest a subset of the evidence while reading as the whole of it. Retired in place per the 2026-09-16 ruling so the cell can be recomputed against the full corpus; the row is kept because it correctly accounted for the evidence that existed when it was computed. NOT recomputed here: regulatory richness now clears on 3 T6 codes from 3 jurisdictions, but the batch-10 plan states in advance that this is a mechanical consequence of section 2.3 and not an answer to the owner question, and the engine change that would let Co-1 findings reach a cell is ACTION (2) of 2026-09-16, which is not this batch.'

# ---- R13 population grading (tier 1-3 admissions) ----------------------------
db add-population-match --ref-id REF-00993 --target-population MOB \
  --study-population 'Cross-disability membership of a national DPO; no study sample — this is an organisational position, not a study' \
  --match-grade PARTIAL \
  --mismatch-note 'PARTIAL, not EXACT, and the reason is the reverse of the usual one. DPI Japan is cross-disability: its assembly speaks for wheelchair users AND for blind, Deaf, intellectually disabled and psychosocially disabled members, so MOB is a PROPER SUBSET of who is speaking, not a proxy standing in for them. The inadequacy claim is made about the mandatory standard as a whole, and the worked examples in the document are toilets and parking bays rather than ramps. So the finding genuinely covers MOB but is not specific to MOB, and grading it EXACT would let a later reader treat a cross-disability judgement as a wheelchair-user-specific one. No sample size: R13 grades population-of-study against population-served, and there is no study here — the warrant is representative standing, not sampling.'

# ---- R11 term harvesting (D-0173: verbatim, unjudged) ------------------------
db observe-term --ref-id REF-00990 --surface-form '傾斜路' --language ja --locator '第十三条・第十九条第二項' --context-quote '不特定かつ多数の者が利用し、又は主として高齢者、障害者等が利用する傾斜路' --notes 'The statutory Japanese term for ramp. Verbatim and unjudged (D-0173): whether it corresponds to our ramp parameter is judgment stage work, not this.'
db observe-term --ref-id REF-00990 --surface-form '移動等円滑化経路' --language ja --locator '第十九条' --context-quote '高齢者、障害者等が円滑に利用できる経路' --notes 'The accessible-route concept the gradient clause attaches to. The 1:12 ceiling applies to ramps CONSTITUTING this route, not to every ramp in a building — a scoping fact that a bare 1:12 loses.'
db observe-term --ref-id REF-00990 --surface-form '敷地内の通路' --language ja --locator '第十七条・第十九条第二項第七号' --context-quote '不特定かつ多数の者が利用し、又は主として高齢者、障害者等が利用する敷地内の通路' --notes 'Path within the site. Carries its own ramp provisions, and is the domain REF-00989 loosely called outdoors.'
db observe-term --ref-id REF-00991 --surface-form '誘導すべき建築物特定施設' --language ja --locator '題名' --context-quote '高齢者、障害者等が円滑に利用できるようにするために誘導すべき建築物特定施設の構造及び配置に関する基準' --notes 'The 誘導 (guide toward / induce) framing is what distinguishes this instrument from the mandatory 円滑化基準, and it is the distinction REF-00989 collapsed. The source names its own standard as one buildings are GUIDED toward, not held to.'
db observe-term --ref-id REF-00992 --surface-form 'going of a flight' --language en --locator 'Table 1' --context-quote 'Table 1 Limits for ramp gradients Going of a flight Maximum gradient Maximum rise' --notes 'The UK conditions gradient on the GOING — the horizontal run of one flight. No Japanese or US instrument in this corpus carries this term, and it is why the three 1:12s are not one figure.'
db observe-term --ref-id REF-00993 --surface-form '義務基準' --language ja --locator '2．（2）義務基準が不十分' --context-quote '特に建物関係はバリアフリー法の義務基準が低く、移動等円滑化基準（義務基準）だけでは円滑な利用ができない。' --notes 'The DPO uses 義務基準 (mandatory standard) as a category explicitly contrasted with what adequate access would require. Harvested verbatim; adjudication of whether it maps to our regulatory-floor concept belongs to judgment.'

# ---- R2 citation mining on the one tier-1..3 anchor --------------------------
# REF-00993 is a DPO position statement, not a paper: it carries no reference
# list. Backward and forward are logged SEPARATELY and honestly rather than
# waived, because "no bibliography" is a real property of the document class and
# the register is the only evidence a pass happened at all.
db log-mining --slug accessible-circulation-geometry --ref REF-00993 --direction backward \
  --deferred-reason 'NO REFERENCE LIST EXISTS TO MINE. REF-00993 is a DPO analysis-and-action-plan page, not an academic work: it carries no bibliography, no DOI and no numbered citations. It names exactly two external instruments in running prose — the CRPD Committee 2022 Concluding Observations on Japan, and the IPC Accessibility Guide — and both are registered as search_candidates by this batch rather than invented as connections here. Backward mining of a document with no reference list is not deferred work; it is complete, and this row says so rather than leaving R2 silent.'
db log-mining --slug accessible-circulation-geometry --ref REF-00993 --direction forward \
  --deferred-reason 'FORWARD MINING NOT ATTEMPTED THIS PASS, and the reason is structural rather than a choice of effort: forward mining traces who CITES an anchor, which for this corpus runs through Crossref/Scopus citation graphs. A Japanese DPO web page carries no DOI and is not indexed by any citation database, so the forward graph does not reach it. The tractable forward route is a Japanese-language site search for organisations quoting the 義務基準が不十分 framing, which is a real unit of work and is NOT done here. Recorded as owed rather than passed.'

# ---- R7 candidates: seen, not admitted --------------------------------------
db add-candidate --found-under-slug accessible-circulation-geometry --disposition PENDING-VERIFICATION \
  --title 'IPC Accessibility Guide (International Paralympic Committee)' \
  --tier-guess 4 --locator-status UNVERIFIED \
  --why-not-admitted 'Named by REF-00993 as the benchmark against which Japan mandatory standards are judged LOW, but not retrieved in this pass and therefore not admitted. It is the comparator the Co-1 finding rests on, so admitting the finding without it leaves the standard of comparison unread.' \
  --notes 'HIGH VALUE FOR THE OWNER QUESTION. If the IPC guide states a ramp gradient, it is a T4-class international standard that would clear section 2.3 richness on its own AND would carry the threshold-of-acceptability framing the statutory codes do not. Retrieve before the next determination pass.'
db add-candidate --found-under-slug accessible-circulation-geometry --disposition PENDING-VERIFICATION \
  --title '高齢者、障害者等の円滑な移動等に配慮した建築設計標準（国土交通省）' \
  --tier-guess 6 --locator 'https://www.mlit.go.jp/jutakukentiku/content/001402840.pdf' --locator-status UNVERIFIED \
  --why-not-admitted 'Surfaced by the row 1 query as an MLIT design standard distinct from both instruments admitted. Not retrieved or screened in this pass; admitting a third Japanese document without reading it would repeat exactly the second-hand-attribution error this batch just corrected.' \
  --notes 'Japan therefore has at least THREE layers on this parameter: mandatory 円滑化基準 (REF-00990), voluntary 誘導基準 (REF-00991), and this design standard. REF-00989 collapsed the first two; this candidate is how the third stops being collapsed as well.'
db add-candidate --found-under-slug accessible-circulation-geometry --disposition PENDING-VERIFICATION \
  --title 'DPI日本会議 — 建築設計標準の見直し＆当事者参画ガイドライン パブリックコメント (2025)' \
  --tier-guess 1 --locator 'https://www.dpi-japan.org/blog/workinggroup/traffic/public-comment-20250430/' --locator-status RESOLVED \
  --why-not-admitted 'Retrieved and persisted (HTTP 200) but not screened in depth this pass. Registered rather than dropped because it is a Co-1 consultation response on the very design standard the candidate above names, and it is the most likely home of a gradient-specific DPO position — the thing Leg D looked for and did not find.' \
  --notes 'The gradient-specific Co-1 claim remains OWED after this batch. This candidate is the strongest known route to it.'

# ---- Leads and gaps ----------------------------------------------------------
db add-code-lead --jurisdiction FR \
  --standard-name 'Arrêté du 20 avril 2017 (accessibilité ERP neufs) — art. 2, profil en long' \
  --clause 'Article 2, II, 2° a) — plan incliné, pente' --status REFERENCE-ONLY \
  --recovered-from 'https://www.legifrance.gouv.fr/loda/id/JORFTEXT000034485459' \
  --notes 'RETRIEVAL FAILURE, NOT ABSENCE, and deliberately holding no values (2026-08-12 REFERENCE-ONLY ruling). Légifrance answers HTTP 403 to automated retrieval on every route tried — /loda/id/, /jorf/article_jo/, /jorf/id/ and /download/pdf — with a browser User-Agent set; persisted 403 artefacts ecc3d03788c5d0ad and 4ddca3bcc61e5d52 are the evidence. The ministry carrier accessibilite-batiment.fr returns 200 but serves a byte-identical JS shell for every section (sha e6fbf3f3c030e5c1), so it carries no clause text either. The document is freely published and correctly identified; only the machine route is blocked, so a session with a browser or with PISTE API credentials closes this in one step. Values were SEEN through a reader tool and are NOT recorded here, because a figure the corpus cannot check against persisted bytes is the 2026-08-19 shape.'

db add-gap --category SW --priority P2 \
  --description 'R15 CANNOT BE DISCHARGED AGAINST research_code_leads: there is no update-code-lead verb. R15 requires a staged description to be re-described from the source on resolution and corrected if over-claimed. Batch 10 resolved lead 85 and PROVED part of its note false — lead 85 records that REF-00989 attributes 12分の1, 1/15 outdoors and 8分の1 to the Barrier-Free Law, and the retrieved law (REF-00990) contains 十五分の一 ZERO times; 1/15 is in a different instrument, MLIT Ordinance 114/2006, the voluntary 誘導基準 (REF-00991). db.py offers add-code-lead only; status stays REFERENCE-ONLY though the document is now RETRIEVED, and the note keeps asserting the false attribution to the next reader. update-locator moves a LOCATOR status, not a lead. The correction is currently recorded only in REF-00991 extraction notes, which a reader of the lead never sees. Coverage bug per CLAUDE.md section 4 — fix the writer, do not hand-write SQL.'

# ---- Search log. LAST, deliberately: log-search refuses --results-admitted
# ---- without --admitted-ref-id (H05), so every admission must already exist.
db log-search --slug accessible-circulation-geometry --jurisdiction JP --language ja \
  --target-tier 6 --target-evidence-type code --target-scope intrinsic \
  --query-text '高齢者、障害者等の移動等の円滑化の促進に関する法律 建築物移動等円滑化基準 傾斜路 勾配 e-Gov' \
  --engine web --depth-method scoping --results-found 9 --results-screened 9 \
  --admitted-ref-id REF-00990 --admitted-ref-id REF-00991 \
  --prior-expectation 'research_code_leads 85, and it is a falsifiable row. The lead records that REF-00989 attributes three figures to this law — 12分の1, 1/15 outdoors, and 8分の１ for rises of 16cm or less — and that the law itself was never retrieved, so none was copied in (rule 5). Japanese law is published in full on e-Gov, so I expect the clause text itself. Prediction: all three figures are confirmed and no basis is stated for any of them. If they are not confirmed, the corpus has been holding a lived-experience assessment of a legal figure that is not what the law says, which is a larger finding than the value.' \
  --findings-note 'PRIOR PARTLY FALSIFIED, and the falsification is the result. Two of the three figures are confirmed IN THIS INSTRUMENT: Cabinet Order 379/2006 Art.19(2)(iv)ro and (vii)ni(2) both read 勾配は、十二分の一を超えないこと。ただし、高さが十六センチメートル以下のものにあっては、八分の一を超えないこと。 The third is NOT: 十五分の一 occurs ZERO times in the whole Cabinet Order. It was located instead in a DIFFERENT instrument retrieved in the same pass — MLIT Ordinance 114/2006 (the 誘導基準 / guideline standard), Art.11(1)(vi)ro, 勾配は、十五分の一を超えないこと, applying to 敷地内の通路 (paths within the site). So REF-00989 attributes to one law three figures that come from two instruments of DIFFERENT LEGAL FORCE: 1/12 and 1/8 are the mandatory 建築物移動等円滑化基準; 1/15 is the enhanced standard buildings meet voluntarily for certification. REF-00989 characterises 1/15 as the outdoor figure; the domain is roughly right (site paths) but the legal strength is not — nothing requires 1/15. Prior also CORRECT that no basis is stated: neither instrument gives any warrant, derivation or citation for any figure. Both admitted REF-00990 (Cabinet Order) and REF-00991 (Ordinance). Payloads persisted: retrieval-log manifest sha256 6ac7f09b… and edd9f6fc…, both HTTP 200 from the e-Gov API.'

db log-search --slug accessible-circulation-geometry --jurisdiction FR --language fr \
  --target-tier 6 --target-evidence-type code --target-scope intrinsic \
  --query-text 'arrêté accessibilité ERP pente rampe pourcentage Légifrance texte consolidé' \
  --engine web --depth-method scoping --results-found 9 --results-screened 9 --results-admitted 0 \
  --prior-expectation 'Légifrance publishes consolidated text free. I expect 5% as the general maximum with tolerances at 8% and 10% conditioned on length — i.e. a rise-conditioned structure like the Flemish one, which would make Flanders less of an outlier than it currently looks. No stated basis.' \
  --findings-note 'R14 DIAGNOSIS: RETRIEVAL FAILURE — not absence, not wrong index, not query shape. The document was located on the first query and is the right one (Arrêté du 20 avril 2017, ERP neufs). Légifrance returns HTTP 403 to automated retrieval on every route tried: /loda/id/, /jorf/article_jo/, /jorf/id/ and the /download/pdf endpoint, with a browser User-Agent set. Persisted as evidence of the attempt: artefacts ecc3d03788c5d0ad.html and 4ddca3bcc61e5d52.html, both 403. The ministry carrier accessibilite-batiment.fr returns 200 but is JS-driven — /dispositions-generales/ and /cheminements-exterieurs/ serve BYTE-IDENTICAL shells (sha e6fbf3f3c030e5c1, 13103 bytes both times) and the word incliné occurs only in the nav. PISTE sandbox 405, bulletin-officiel PDF 404. NOTHING ADMITTED, DELIBERATELY. A rendering of the Légifrance page was obtained through a reader tool and shows Art.2 II 2 a) Profil en long at 5% with tolerances of 8% over <=2 m and 10% over <=0.50 m — which would CONFIRM the prior exactly — but those bytes were never captured, so the figures are NOT filed as values and NOT admitted. Filing them would be a number attached to a quote the corpus cannot check, which is the 2026-08-19 shape. Recorded instead as a code lead naming the document to fetch, per the 2026-08-12 REFERENCE-ONLY ruling.'

db log-search --slug accessible-circulation-geometry --jurisdiction GB --language en \
  --target-tier 6 --target-evidence-type code --target-scope intrinsic \
  --query-text 'Approved Document M access to and use of buildings ramp gradient table gov.uk' \
  --engine web --depth-method scoping --results-found 9 --results-screened 9 \
  --admitted-ref-id REF-00992 \
  --prior-expectation 'AD M is Crown copyright and published free, unlike BS 8300 which it references. I expect a gradient/length table (1:20 to 1:12 by flight length) and an explicit pointer to BS 8300 for anything further — which makes AD M the reachable proxy for row 6 paywall, and I must record it as AD M own figure, not as BS 8300.' \
  --findings-note 'PRIOR CONFIRMED ON BOTH CLAUSES, and the second clause is the one that matters. Table 1 Limits for ramp gradients is exactly the gradient/length table predicted: going 10m -> 1:20 (rise 500mm), 5m -> 1:15 (333mm), 2m -> 1:12 (166mm), with interpolation between 2m and 10m (1:14 at 4m, 1:19 at 9m). BS 8300 appears in the standards list (BS 8300:2001, BS 8300:2009+A1:2010, BS 8300-2:2018) but NO figure in Table 1 is attributed to it, so AD M is recorded as stating its own figure and nothing is inferred about BS 8300 — which is precisely what Leg B row 6 was to test, and it is now testable against a read document rather than a catalogue page. THE SUBSTANTIVE FINDING: the UK does not state a single ceiling, it conditions gradient on the GOING of a flight. 1:12 is UK-legal only for a 2 m going (166 mm of rise, about one step); a 10 m flight is capped at 1:20. So the apparent US/JP/GB agreement at 1:12 is an artefact of reading three differently-shaped rules as one number. Filed as a claim at 1:20 and a condition at 1:12 so the engine cannot gather the false convergence. Payload persisted: 1,471,989-byte PDF, sha256 0e5d4dee25b341f4…, HTTP 200 from gov.uk assets.'

db log-search --slug accessible-circulation-geometry --jurisdiction JP --language ja \
  --target-tier 1 --target-evidence-type co1 --target-scope intrinsic \
  --query-text 'DPI日本会議 障害者団体 スロープ 勾配 建築物移動等円滑化基準 意見' \
  --engine web --depth-method scoping --results-found 9 --results-screened 9 \
  --admitted-ref-id REF-00993 \
  --prior-expectation 'The natural pairing for row 1: a Japanese DPO commenting on the Japanese statutory figure. I expect a position or consultation response arguing the legal gradient is insufficient — an inadequacy finding under R7 and the 2026-09-13 ruling, not a value. If it states a preferred maximum with its own warrant, that is the batch most valuable admission.' \
  --findings-note 'PRIOR HALF RIGHT, AND THE HALF IT GOT WRONG MATTERS. Right: DPI Japan does argue the mandatory standard is insufficient — 特に建物関係はバリアフリー法の義務基準が低く、移動等円滑化基準（義務基準）だけでは円滑な利用ができない, benchmarked against the IPC Accessibility Guide. That is the R7 inadequacy finding the prior expected, admitted as REF-00993 and filed figure_role=finding per the 2026-09-13 ruling. Wrong: the prior assumed a DPO commenting on the GRADIENT. It does not. 勾配, スロープ and 傾斜 occur ZERO times in the retrieved bytes; the worked examples are accessible toilets and parking bays. So the Co-1 leg reached a judgement about the instrument, not about the figure, and the extraction says so in its own notes to stop a later reader over-reading it. The gradient-specific Co-1 claim the prior hoped for was NOT found in this pass and remains owed. R14 on that narrower question: not absence — the query was well formed and returned the DPO, so this is a GENUINE GAP IN WHAT THE DPO HAS PUBLISHED on this parameter, which is itself worth knowing.'

echo "REPLAY COMPLETE"
