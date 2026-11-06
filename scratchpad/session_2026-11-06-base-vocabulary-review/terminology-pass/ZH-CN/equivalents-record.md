# Equivalents record: ZH-CN (Simplified, mainland China), session_2026-11-06-base-vocabulary-review

**Verdict.** Partial, breadth-limited pass. All three owner classes are covered from six mainland texts: the 2021 code, the 2023 law, the 2012 State Council regulation, the 2021 Beijing regulation, a 民政部 signage standard and Beijing municipal design guidance. Tier 5 (disabled people's organisations) is NOT-OBTAINABLE: cdpf.org.cn and its Wayback snapshot both failed at the egress. **Every GB 55019 form is taken from the first pass's OCR TRANSCRIPTION of an image-only PDF, not from artefact bytes.** `quote_check` says so on each row. Taiwan, Hong Kong and Singapore Chinese were excluded as other jurisdictions, and a Taiwan hit (land.chcg.gov.tw) was dropped. Nothing was written to the database, committed or pushed.

**Concepts attempted: 20 of 560.** R2-050, R2-051 (conflation note only, no form row), R2-281, R2-333, R2-163, R2-164, R2-166, R2-168, R2-169 (seed only), R2-174, R2-083, R2-059, R2-072, R2-176, R2-177, R2-178, R2-201, R2-111, R2-093. The other 540 were not attempted. That includes the quantity rows, the ZH-origin trigger and drafting rows (R2-456 to R2-458 and R2-503 to R2-506), handrails and grab bars.

**Counts (re-run; D = this folder):** rows and concepts come from `python3 -I $D/tools/equiv_build.py`. Usage type: `tail -n +2 $D/equivalents.tsv | cut -f6 | sort | uniq -c`. Tier: `... | cut -f8 | sort | uniq -c`. Conflation notes: `awk -F'\t' 'NR>1 && $12!=""' $D/equivalents.tsv | wc -l`. On 2026-11-06 these gave 64 rows over 18 concepts. By usage type: 31 code term, 12 qualifier, 12 colloquial, 4 regional variant, 2 outdated or disfavoured, 3 unattested seed. By tier: 28 / 9 / 4 / 20 / 0 / seed 3. There were 16 conflation notes. Tier 1 is the first-pass instruments re-read, tier 2 the 2012 and Beijing regulations, tier 3 MZ/T 131, tier 4 the Beijing guidance. Do not trust these figures; re-run the commands.

## The owner classes in Chinese (CN)
- **Parking.** The code term is 无障碍机动车停车位 (GB 2.9). The statutes use 无障碍停车位 (law art. 24, 2012 regulation art. 14, Beijing art. 17), and so does the signage name (MZ/T 131, table A.1 no. 40). The guidance short form is 无障碍车位, and 泊位 is the generic bay word. 残疾人专用停车位 is a seed only. Unlike most pairs, the umbrella word 无障碍 prefixes the parking form, with no user-group noun. The scope moved from "exclusive" (专用, 2012) to "priority" (优先, 2023).
- **Umbrella qualifier.** 无障碍 is the code and statute word. Its stated scope is wider than disabled people: 残疾人、老年人等有需求的人 (GB 1.0.3(1); law art. 2). Beside it stand 通用设计(理念) (law art. 51; Beijing art. 3), the compound 无障碍通用设计 (2012 art. 6; Beijing art. 7), the narrower 残疾人专用 (2012 art. 6), 通用包容 / 包容性 / 通用性 (Beijing guidance), 全龄友好 (the nearest "…friendly" form; age-based) and 适老化 (older people, coupled by law art. 4). No "wheelchair friendly" analogue was attested.
- **Vertical transport.** The code has 电梯, with 无障碍电梯 as its accessible subset. The platform lift is 升降平台, and the code heads one section with both objects (2.6) instead of an umbrella noun. The escalator is 自动扶梯, and 候梯厅 is the lift lobby. Colloquial and guidance forms are 直梯, 垂直电梯, 扶梯, 天桥升降梯 / 人行天桥电梯 and 轮椅升降机. The stair-lift and vertical-platform standard titles (GB/T 24806, 24805) are seeds only.

## Conflations (recorded, not resolved; locators in equivalents.tsv)
1. **通用 has two senses inside one code.** The title 无障碍通用规范 uses 通用 for a "general technical code" (前言: 通用技术类规范（简称通用规范）). Elsewhere 通用设计 means universal design (law art. 51). The Beijing guide also uses 国际通用 for "internationally common". This is the most surprising one: the code's title reads as "universal" to anyone who takes the qualifier sense.
2. **无障碍卫生间.** The code uses it only for the bathroom of an accessible guest room or dwelling (3.4.4) and calls the public stand-alone room 无障碍厕所 (3.2.3). The Beijing guide uses 无障碍卫生间 for the public room (PDF p.63).
3. **垂直电梯 / 直梯 written against 扶梯** suggests that 电梯 can cover escalators. The special-equipment definition was not retrieved.
4. **One bay, ordered users (law art. 24) versus B651's second bay class (R2-051).** Also: 无障碍通用设计 fuses two umbrella words, 天桥升降梯 versus 人行天桥电梯 is not judged, 轮椅坡道 versus 无障碍坡道 is not judged, and 标识 / 标志 sit in adjacent clauses.

## Not obtained
- TLS failure (exit 35) at: xuancheng.gov.cn (a 残联 reply), sf.sz.gov.cn (Shenzhen permit notice), ndls.org.cn (standard titles), xxgk.mot.gov.cn (road signs), wlt.fujian.gov.cn (special equipment) and cdpf.org.cn.
- Wayback: no snapshot for the first two. The CDPF snapshot exists, but web.archive.org reset under both URL forms while a gov.cn control returned 200.
- The Shaanxi catalogue PDF returned 404. No official GB 5768.2 (road signs), GB/T 10001.9 or TSG text was found.

## Self-attack
1. Tier-1 GB forms rest on my predecessor's transcription. A misread glyph would verify against itself (pass-record M1, M2).
2. Tier 4 is one Beijing document (CN-BJ), so "colloquial" here means Beijing guidance usage, not national speech.
3. Usage types are my judgment. 下降式路缘石 is filed as outdated but is really a historical calque, and 泊位 is filed as a code term although it is generic.
4. MZ/T 131 attests GB/T 10001.9-2008 names second-hand, and that edition has been replaced (2021 per a search summary, UNVERIFIED).
5. The 2012 regulation's status after the 2023 law is UNVERIFIED. Its rows may be labelled wrongly as outdated or as code terms.
