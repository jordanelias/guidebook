# Pass record: terminology pass ZH/CN (Simplified), session_2026-11-06-base-vocabulary-review

**Verdict.** The current national accessibility code, GB 55019-2021 《建筑与市政工程无障碍通用规范》, a fully mandatory code in force since 2022-04-01, was retrieved from gov.cn and read in full. So was the 2023 《中华人民共和国无障碍环境建设法》 (12371.cn, a 新华社 republication). Of 75 register concepts: 47 FOUND, 17 FOUND-PARTIAL, 11 SEARCHED-ABSENT, with 95 reverse-harvest phrases. **Caveat:** the official GB 55019 PDF is image-only. Its "saved text" is my corrected OCR transcription, not the artefact's bytes, so the build verifies its quotes against my transcription. The older and much longer design code, GB 50763-2012 《无障碍设计规范》, is NOT-OBTAINABLE: MOHURD's site is refused at the egress proxy and Wayback holds no snapshot. Every ABSENT result rests on two short texts, and GB 50763 is the likeliest home of most of the missing detail. Nothing was written to the database, committed or pushed.

## How the instrument list was built
The base gave nothing for China: `research_code_leads` has 0 rows matching CN, and `evidence_sources` has 0 CN rows. `references/standards-registry.md` names only GB 50763-2012 and does not know GB 55019. The list therefore came from web search (search-log W1 to W7). The gov.cn notice (公告2021年第174号) supplied both attachments, and its attachment 2 shows that GB 55019 repealed only five mandatory clauses of GB 50763, so the rest of GB 50763 still stands. Building-specific regulation sits in these engineering codes. The statute sets duties and refers design to 无障碍设施工程建设标准 (arts. 12, 15).

## Retrieved and read
- GB 55019-2021: 前言, 目次, chapters 1 to 5 (printed pp. 1–17), read in full from the page images. The code has no figures. The PDF has no cover, title or notice page. Transcript `text/ee78b16e1dec13b8.txt`.
- The 2023 law, arts. 1–72, read in full (`text/575638778aada9c1.txt`). Attachment 2 (repealed clauses) and the notice were also read (`text/9cffed8f3e412af0.txt`, `text/96574756986c5488.txt`).
- Not read: GB 50763-2012 (NOT-OBTAINABLE, above). Also not read, because of the budget: GB 50096 (residential), GB 50624 (handover and maintenance), the road and transit codes, and local standards (Beijing PDFs were seen in search results). Currency after 2021 for GB 55019, and after 2023 for the law, is UNVERIFIED.

## Counts (re-run, do not trust; from the repo root, D=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/ZH-CN)
- Rebuild and verify: `python3 -I $D/build.py`. It reports register 75, observations 79, reverse-harvest 95 and failures 0, and exits 1 on any failure.
- Status: `cut -f4 $D/coverage.tsv | tail -n +2 | sort | uniq -c` gives 47 / 17 / 11. By source: `cut -f3,4 $D/coverage.tsv | tail -n +2 | sort | uniq -c` (catalogue 2.1: 22/8/2; 2.2: 13/4/1; parameters: 6/2/2; B651-only headings: 6/3/6).
- Distinct phrases: `awk -F'\t' 'NR>1{print $2}' $D/observations.tsv | sort -u | wc -l` gives 77. By instrument: `awk -F'\t' 'NR>1{print $4}' $D/observations.tsv | sort | uniq -c` gives 76 GB 55019 and 3 law. For the reverse harvest it gives 82 and 13.
- Raw-byte check: the 16 law quotes all occur in the raw HTML (`retrieval_log.locate_quote`, kind 'unscoped', no ref_id). The GB 55019 quotes cannot be checked against bytes, because no text exists in the PDF.
- Held zh aliases found as substrings of the two texts: 17 of 155 (`select distinct alias from term_aliases where lower(language) like 'zh%'`, each tested with `in` against the whitespace-free texts). A hit is presence only: 通道 and 轮椅 hit only inside longer phrases. 走廊宽度, 坡道坡度, 门宽 and 无障碍门槛 (word-for-word translations) occur in neither text.

## Where the Chinese code carves the field differently (instrument-derived; glosses ours)
1. **Three facility classes, not elements.** Everything is a 无障碍通行设施, a 无障碍服务设施 or a 无障碍信息交流设施 (1.0.3(4)). Information and communication has a whole chapter (ch. 4), which covers phones, kiosks, screen readers, replaceable keyboards and crossing signals. The register has no such axis.
2. **One width word, no corridor.** 通行净宽 serves routes, ramps, doors (measured "after opening"), gates and lift doors. 走廊 occurs 0 times. The route object is 无障碍通道 within a continuous 无障碍通行流线 that spans open space, site and building. A crowded-place variant (人员密集的公共场所) raises the width.
3. **Two ramps.** The 轮椅坡道 (wheelchair ramp) and the 缘石坡道 (kerb ramp, with its own types: 全宽式单面坡, 三面坡; and parts: 坡口, 过渡空间) are separate objects. A run is bounded by 提升高度 (rise), not by run length, so P12 has no direct counterpart. This matches the Japanese carve.
4. **扶手 is both handrail and door handle** (2.5.4(2): 门扇外侧和里侧均应设置扶手，扶手应保证单手握拳操作). The window handle is 执手, and grab bars are 安全抓杆. An English-led seed (把手 for a door handle) would miss the instrument's word. I made exactly that error in transcription before correcting it.
5. **Toilet hierarchy.** A 无障碍厕位 (a cubicle inside a public toilet) differs from a 无障碍厕所 (a stand-alone room). Each must allow use by someone 跌倒在地面 (fallen to the floor). The register has one "accessible washroom".
6. **Tactile paving is a pair under one parent:** 盲道 = 提示盲道 (warning) + 行进盲道 (guidance), and 2.11.4 requires colour or material difference.
7. **Contrast is "colour or brightness" (颜色或亮度对比), never quantified;** for steps it is "colour or material" (颜色或材质). There is no LRV, and no luminance term beyond 亮度.
8. **No lighting or acoustics** (照度, 混响, 色温 all 0). Noise appears only as a nuisance of crossing signals (4.0.8(4)).
9. **Scoping by user, and the "mainly used by" device.** Stair and handrail rules apply where 视觉障碍者 or 行动障碍者 主要使用. The statutory population is 残疾人、老年人 (law art. 2), with ageing joined by statute (适老化改造, art. 4).
10. **Drafting and compliance structure.** The code is "full-text mandatory" (前言), with a performance route for innovation (1.0.4: 论证 against performance), separate lower values for 既有建筑改造或改建, and a relaxation trigger (条件受限). The law adds 替代性措施 where retrofit is infeasible (art. 18), the "five synchronies" (art. 12), and 体验试用 by disabled and older people's representatives (art. 17). **Maintenance is part of the code** (ch. 5: 维护责任人, 应急维护措施).

## Defects in the METHOD
- **M1. Image-only official texts break the verification chain.** `build.py` proves a quote is in my transcript, not in the artefact. `retrieval_log` has no OCR step and no field marking a text as a transcription, so a reader of observations.tsv cannot tell a transcribed quote from an extracted one except through the text-file header. The method needs a `text_kind` column (extracted / OCR / OCR-corrected) and, ideally, page-image hashes.
- **M2. Transcription drift towards the expected word** (把手 for 扶手). This is caught here only because a character diff against raw OCR was run. Any CJK pass that hand-corrects OCR needs that diff as a required step.
- **M3. Quantity words of 2.2 are English lemmas.** "level", "distance" and "capacity" map to senses (高差, 距离 as setback, 容纳担架), and FOUND-PARTIAL is assigned by my judgment (the PARTIAL dict), as in the FR pass.
- **M4. The register remains criterion-shaped** (C02/C11/C14, C01/C13, C22/C29, C10/C28 are near-duplicates). Here one phrase, 坚固、平整、防滑、不积水, fills three concepts.
- **M5. Egress, not the publisher, blocked MOHURD.** That makes GB 50763 NOT-OBTAINABLE from this environment only. A session on another network, or the owner, might reach it. The Wayback route does not help for MOHURD at the paths tried.
- **M6. Registry staleness.** `references/standards-registry.md` lists GB 50763 as CURRENT and omits GB 55019 (prevailing since 2022). Not edited (out of scope).

## Self-attack: the five likeliest ways this record is wrong
1. **Transcription error.** A glyph I misread, or "normalised" as with 把手, would put a wrong phrase into the record and still verify, because the check runs against my own text. 箅子 (grating) is read visually and is the most exposed. Every clause was compared with its page image, but only twice at 300 dpi.
2. **ABSENT is narrow.** SEARCHED-ABSENT means absent from GB 55019 and the 2023 law. GB 50763-2012, which is not read, almost certainly treats stair dimensions, outlets, lighting or landscaping somewhere. The 11 ABSENT rows and several PARTIAL rows should be re-run once GB 50763 is in hand.
3. **Concept mapping is mine.** Mapping 净高 (low-space barring) to "Height clearance (parkade)", 容纳担架 to "capacity", 临时占用 to "Scaffolding" or 电器 to "Microwave" stretches the senses. The notes flag each one, but the FOUND/PARTIAL status still counts them.
4. **Currency and edition.** "In force" rests on the 2021 notice and the statute's commencement article. A later MOHURD amendment notice, or a GB 50763 revision, would not show here. The law's text is a republication (12371/新华社), not the NPC gazette.
5. **Locators.** Clause numbers are printed in the code and are reliable. Printed page numbers come from the page footers. Law locators are article numbers counted from the text, and 12371's article breaks were assumed to match the gazette.

Files: search-log.md, instruments.tsv, observations.tsv, coverage.tsv, reverse-harvest.tsv, seeds.tsv (10 MODEL-GENERATED), build.py, text/ (four texts), tools/fetch.py.
