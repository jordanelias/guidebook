# Equivalents search log: ZH-CN (Simplified, mainland China), session_2026-11-06-base-vocabulary-review

Every query and fetch verbatim. "Prior" is written before the call, appended to this file by the shell before the search or fetch runs; "Result" is appended after. Times UTC, 2026-11-06. WebSearch summaries are model text and are used only to find URLs; no form is taken from a summary.

## Tier 1: second reading of texts already in hand (local, from the first pass)
- L1 grep of `text/ee78b16e1dec13b8.txt` (GB 55019 TRANSCRIPTION, OCR-corrected; not artefact bytes) for 停车|车位|电梯|升降|梯|通用|残疾人|方便|便利. Prior: 无障碍机动车停车位 (2.9), 无障碍电梯 and 升降平台 (2.6), no 通用设计. Result: as expected; also 停车位 bare (2.9.1), 自动扶梯 (2.2.5), 楼梯 vs 梯段. Shape: substring grep; each hit read in its clause.
- L2 grep of `text/575638778aada9c1.txt` (law, extracted from HTML) for 无障碍|停车|电梯|通用设计|残疾人. Prior: 无障碍停车位 in a parking article, 加装电梯, 通用设计理念. Result: art. 24 has 无障碍停车位, 残疾人车辆专用标志, 残疾人证, 行动不便; art. 22 加装电梯. Shape: substring grep; hits read in their article.

## Tiers 2 to 5 (web)
- S1 prior: a national standard listing for GB/T 24805 (vertical lifting platforms for people with impaired mobility) on openstd or std.samr; the title will use 升降平台 and 行动不便者. Query `GB/T 24805 行动不便人员使用的垂直升降平台`.
- S2 prior: GB 5768.2 or GB/T 10001.9 titles; a sign named 无障碍设施 or 残疾人专用. Query `GB/T 10001.9 公共信息图形符号 无障碍设施符号`.
- S3 prior: a city government page on 残疾人专用停车位 or 无障碍停车位 (Beijing/Shanghai/Shenzhen gov.cn). Query `残疾人专用停车位 申请 北京市 gov.cn`.
- S4 prior: CDPF (cdpf.org.cn) pages on 无障碍; perhaps the 残障 vs 残疾 debate in an organisation's guide. Query `中国残联 无障碍 停车位 残疾人车辆专用标志 cdpf.org.cn`.
- S1 result: codeofchina, chinesestandard (sales), two ndls.org.cn (国家标准馆) detail pages, EN 81-41 shops. Title form 行动不便人员使用的垂直升降平台 appears in the search summary only; not attested until a page is fetched. Shape: number plus title is the right shape for a title lookup.
- S2 result: a gov.cn PDF (2019-12, unknown content), a cspress PDF, chinesestandard related lists, an ndls detail page. Summary says Part 9 is for 无障碍设施 symbols; not attested until fetched. Shape: fine.
- S3 result: no Beijing page. xuancheng.gov.cn download 2412487 (a 市残联 reply), sf.sz.gov.cn .doc (Shenzhen notice draft on 残疾人专用停车位使用标识), Munich zh-CN pages (foreign jurisdiction: excluded). Shape: "gov.cn" in the query is not a filter.
- S4 result: no cdpf.org.cn page; sina news 2012 (news: excluded by brief), the same xuancheng and Shenzhen items, a New Jersey zh-Hans guide (foreign: excluded). Shape: a domain inside the query does not restrict.

## Fetches (retrieval_log.fetch from the repo root)
- F1 prior: xuancheng 2412487 is a 市残联 reply quoting the 2012 条例 with 无障碍停车位 and perhaps 残疾人专用泊位. URL https://www.xuancheng.gov.cn/OpennessContent/download/2412487.html
- F2 prior: Shenzhen .doc (Word binary) is a draft notice using 残疾人专用停车位 and 使用标识. URL https://sf.sz.gov.cn/attachment/0/802/802552/8943784.doc
- F3 prior: gov.cn 2019-12 PDF is a list of national standards approved, possibly including GB/T 10001.9 or lift standards. URL https://www.gov.cn/xinwen/2019-12/24/5463665/files/4bb69f1b9c8743c7aedd9f1b44858f1a.pdf
- F4 prior: ndls.org.cn detail page for GB/T 24805 gives the Chinese title with 垂直升降平台; may be a JavaScript shell. URL https://ndls.org.cn/standard/detail/7a3ebd5943f7104cea42dbb7f605fc0c
- F1 result: exit 35 (TLS failure), 0 bytes. F2 result: exit 35, 0 bytes. F4 result: exit 35, 0 bytes. All three are TLS handshake failures from this egress; Wayback tried below.
- F3 result: 200, 1,079,577 bytes, artefact 600c6137712d20e2.pdf, text layer present (pdftotext -layout → text/600c6137712d20e2.txt, not committed). It is NOT a GB/T 10001.9 text: it is MZ/T 131—2019 《养老服务常用图形符号及标志》 (民政部, a signage standard for elderly-care services). It reproduces symbols from GB/T 10001.9-2008 with their Chinese names, so it attests the signage names second-hand. Prior partly wrong (expected a standards list).
- S5 prior: gov.cn full text of the 2012 State Council 《无障碍环境建设条例》 (国务院令第622号), superseded by the 2023 law; expect 无障碍停车位 and maybe 残疾人专用. Query `无障碍环境建设条例 国务院令 第622号 全文 gov.cn`.
- S6 prior: SAMR 《特种设备目录》 page defining 电梯 with subclasses incl. 自动扶梯 and 杂物电梯. Query `特种设备目录 电梯 曳引与强制驱动电梯 自动扶梯 质检总局 2014年第114号`.
- S7 prior: a DPO or CDPF text on preferring 残障 over 残疾, or on 残废 as a rejected word. Query `残障 残疾 称谓 残废 歧视性用语 残疾人联合会`.
- S8 prior: municipal (Beijing or Shanghai) guidance using 通用无障碍 or 无障碍电梯 / 加装电梯 in public-service pages. Query `通用无障碍 北京市 无障碍环境建设 专项行动 gov.cn`.
- S5 result: gov.cn content_2179947 (法律法规>>行政法规) and content_2179864 (国务院令), cecc.gov English, fadada copies. Shape: fine.
- S6 result: university copies, a Shaanxi SAMR PDF (snamr.shaanxi.gov.cn) whose attachment 3 is the 2014 catalogue, a Fujian PDF; no samr.gov.cn page. Shape: the announcement number found the catalogue only second-hand.
- S7 result: UN Geneva Chinese inclusive-language guide (an international body, not a CN source; not used as CN attestation), no CDPF or CN DPO page. Empty for tier 5. Shape: a vocabulary-debate query returns international guides.
- S8 result: beijing.gov.cn PDF of 《北京市无障碍环境建设条例》 (2021), a 住建委 docx of the same, ghzrzyw.beijing.gov.cn PDF (a 规划和自然资源委员会 standard or guide, 2021-06), people.com.cn and chinadaily news (excluded). Shape: fine.
- F5 prior: 2012 条例 full text; 无障碍停车位 and 残疾人专用 forms likely. URL https://www.gov.cn/flfg/2012-07/10/content_2179947.htm
- F6 prior: Beijing 条例 PDF with 无障碍停车位, 无障碍电梯, maybe 通用设计. URL https://www.beijing.gov.cn/zhengce/dfxfg/202110/W020230904572688598051.pdf
- F7 prior: ghzrzyw PDF is the 北京无障碍城市设计导则 with colloquial or design forms (无障碍电梯, 无障碍停车位, perhaps 通用设计). URL https://ghzrzyw.beijing.gov.cn/biaozhunguanli/bz/qt/202106/P020210624562130214835.pdf
- F8 prior: Shaanxi PDF reproduces 特种设备目录 with 电梯 classes (曳引与强制驱动电梯, 液压驱动电梯, 自动扶梯与自动人行道, 其他类型电梯). URL https://snamr.shaanxi.gov.cn/__local/6/F3/27/D68050D229CBF36BC34E28B7BD8_0469C35B_6F6F7.pdf
- F5 result: 200, 21,536 bytes, artefact 74b8d2c5429630c9.html (text 74b8d2c5429630c9.txt, tags stripped). Arts. 6, 14, 32 carry 无障碍通用设计, 残疾人专用的无障碍技术和产品, 无障碍停车位. Prior right.
- F6 result: 200, 188,738 bytes, artefact 23135cb9ffb84656.pdf, text layer (pdftotext). Art. 3 通用设计; art. 16 无障碍电梯, 加装无障碍电梯; art. 17 无障碍停车位, 肢体残疾人证; art. 39 泊位. Prior right.
- F7 result: 200, 104,204,697 bytes, artefact a3650e08fd144a75.pdf (76 PDF pages, two printed pages per sheet); pdftotext gives text with column interleaving and missing-font warnings. 《北京无障碍城市设计导则》 (hosted by 北京市规划和自然资源委员会, ghzrzyw.beijing.gov.cn, 2021-06 path). Forms: 无障碍停车位, 无障碍机动车停车位, 无障碍车位, 无障碍电梯, 无障碍垂直电梯, 垂直电梯, 直梯, 天桥升降梯, 轮椅升降机, 通用包容, 全龄友好, 残障人士. PDF p.11 read from a page image (pdftoppm -r 50) because the extraction interleaves speech bubbles. Prior right, with more colloquial forms than expected.
- F8 result: 404, 146 bytes (artefact 55f7d9e99b8e2d4e.html). Empty.
- Local check of MZ/T 131 table A.3 (road-traffic signs from GB 5768.2-2009), PDF pp.33-34: no parking or disability sign among the eight reproduced. Prior (a sign for 残疾人专用) wrong for this table.
- S9 prior: GB 5768.2 text or a gov page naming the road sign 残疾人专用设施 or 无障碍停车位 sign. Query `GB 5768.2 道路交通标志 残疾人专用设施 标志 停车位`.
- S10 prior: a cdpf.org.cn page (CDPF is the statutory body named in the law art. 8) using 无障碍 forms; possibly 残疾人专用停车位. Query `site:cdpf.org.cn 无障碍停车位`.
- S11 prior: an official text where 电梯 covers 自动扶梯 (special-equipment law). Query `特种设备安全法 电梯 是指 动力驱动 自动扶梯 自动人行道 npc`.
- W1 prior: Wayback availability for the xuancheng and Shenzhen URLs probably empty. Calls `http://archive.org/wayback/available?url=www.xuancheng.gov.cn/OpennessContent/download/2412487.html` and `...url=sf.sz.gov.cn/attachment/0/802/802552/8943784.doc`.
- W1 result: `archived_snapshots: {}` for both. F1 and F2 stay NOT-OBTAINABLE from this environment.
- S9 result: xxgk.mot.gov.cn PDF (交通运输部, 2020-06; content unknown), Wikimedia copies of GB 5768.2-2022 (not an official host), sales sites. Shape: fine; no official full text of GB 5768.2 found.
- S10 result: no cdpf.org.cn result; xuancheng, napstic, sina, chinanews, a Taiwan county PDF (land.chcg.gov.tw: Taiwan, a different jurisdiction, excluded), wenxuecity (forum/news, excluded). Empty for tier 5. Shape: site filter honoured but the site is not indexed for this phrase.
- S11 result: university copies of 《特种设备安全法》, zgm.cn popular article (excluded), a Fujian provincial PDF (wlt.fujian.gov.cn, 2026-04). Shape: fine.
- F9 prior: the MOT PDF is a GB 5768.2 draft (征求意见稿) or a related road-sign standard and may name a sign for 残疾人 or 无障碍. URL https://xxgk.mot.gov.cn/2020/jigou/kjs/202006/P020200623760741738973.pdf
- F10 prior: the Fujian PDF is a special-equipment notice and may reproduce 电梯 categories. URL https://wlt.fujian.gov.cn/zwgk/zcfg/zxwj/202604/P020260424407151294400.pdf
- F9 result: exit 35 (TLS failure), 0 bytes. F10 result: exit 35, 0 bytes. Pattern: gov.cn and beijing.gov.cn hosts complete; several provincial and ministry hosts fail the TLS handshake from this egress.
- S12 prior: a gov.cn text of 《特种设备安全监察条例》 whose 附则 defines 电梯 to include 自动扶梯 and 自动人行道. Query `特种设备安全监察条例 附则 电梯 是指 gov.cn 国务院令 第549号`.
- S13 prior: a cdpf.org.cn page on accessibility or on how disabled people are named. Query `中国残疾人联合会 cdpf.org.cn 无障碍 环境 建设 残疾人 称谓`.
- S12 result: gov.cn content_2602533 (the 2009 amending decision, not a consolidated text), university copies, a second Fujian PDF, a Pingdingshan draft. The summary reports no definition of 电梯 in the regulation. Not fetched: a definition of 电梯 covering 自动扶梯 would need TSG or a GB elevator standard, neither on a reachable official host. Shape: the definitional query assumed a 附则 definition that may not exist.
- S13 result: huanqiu, chinadigitaltimes, jiemian, chinadaily (all news; excluded), cecc, faolex. No cdpf.org.cn page. Empty for tier 5.
- F11 prior: www.cdpf.org.cn home page reachable, HTML with a navigation link to 无障碍 pages; it may be a JS shell or fail TLS like the provincial hosts. URL https://www.cdpf.org.cn/
- F11 result: exit 35 (TLS failure), 0 bytes.
- W2 prior: Wayback holds a snapshot of www.cdpf.org.cn; its home page links a 无障碍 section. Call `http://archive.org/wayback/available?url=www.cdpf.org.cn/`.
- W2 result: snapshot listed (20261017135457). Fetch via `https://web.archive.org/web/20261017135457if_/https://www.cdpf.org.cn/` and via the plain `/web/20261017135457/` form: both exit 35, 0 bytes; proxy status `recentRelayFailures` shows web.archive.org:443 ws_closed_mid_exchange ×4 while a gov.cn control returned 200. Tier 5 (CDPF, any DPO) NOT-OBTAINABLE in this session.
