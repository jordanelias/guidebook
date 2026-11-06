# Equivalents search log, JA-JP (session_2026-11-06-base-vocabulary-review, 2026-11-06)

Every query and fetch in order. The prior line is written by the same command before the call runs (SYNTHESIS defect 9). Results include empties. Fetches go through `retrieval_log.fetch` from the repository root; text extracted to `text/<sha16>.txt` (not committed).

## Tier 1: second reading of first-pass texts (local, no fetch)
- Query shape: page-aware regex over `text/*.txt` (helper in the session scratchpad, not kept), terms: 駐車場 駐車施設 駐車区画 車椅子使用者用駐車 優先駐車 障害者用駐車 身障者 駐車スペース 駐車ます 駐車マス パーキング 思いやり駐車 パーキング・パーミット エレベーター エレベータ 昇降機 段差解消機 いす式 階段昇降 リフト エスカレーター ホームエレベーター 昇降路 籠 かご バリアフリー ユニバーサルデザイン 移動等円滑化 インクルーシブ アクセシブル アクセシビリティ だれでも 誰でも 多機能 多目的 車椅子 車いす 車イス.
- Prior: the law texts use only 車椅子使用者用駐車施設, エレベーターその他の昇降機, 移動等円滑化; the design standard adds バリアフリー and perhaps 段差解消機; no colloquial parking form.
- Result: as expected for the law texts. The design standard adds 優先駐車区画 (pdf p.52), 車椅子利用者用駐車施設 (p.57, one-off variant), 障害者等用駐車区画 (p.57, in a cited title), パーキング・パーミット制度 (p.57), 段差解消機 defined as a kind of エレベーター (p.215), 斜行型/鉛直型 (p.216-217), バリアフリー法 as the defined short title of 法91 (p.6), 「多機能」「多目的」 as toilet names to avoid (p.144), 身障者用設備 as the pre-2010 JIS Z 8210 name (p.103). 0 hits: 障害者用駐車, 思いやり駐車, 駐車ます/マス, いす式, 階段昇降, ホームエレベーター, インクルーシブ, 車イス.
- Note: counts by `grep -o <term> text/<file> | wc -l`; a count is presence, not sense.

### FETCH https://laws.e-gov.go.jp/api/2/law_data/335AC0000000105
- purpose: tier 2 道路交通法 (parking for disabled drivers, 高齢運転者等専用駐車区間)
- prior (written before fetch): expect 高齢運転者等専用駐車区間 and 高齢運転者等標章; 身体障害者 as a driver class; no 車椅子 parking term
- result: status 200, 1488250 bytes, sha256 601f4f75a3757b3b21ba88dd09278a365e6632ca1aaa6c4f73571cbe4c14a719, artefact 601f4f75a3757b3b.json, text 601f4f75a3757b3b.txt (872738 bytes)

### FETCH https://laws.e-gov.go.jp/api/2/law_data/335M50004002003
- purpose: tier 3 道路標識、区画線及び道路標示に関する命令 (sign names for disabled-driver parking)
- prior (written before fetch): expect a sign named 高齢運転者等専用 with the 標章 symbol; perhaps 身体障害者 in the sign table
- result: status 200, 629404 bytes, sha256 a5803f6946e2dcb45e9bba1e159544cf26a0db72e7cc432ebb8fbdf82b0bc496, artefact a5803f6946e2dcb4.json, text a5803f6946e2dcb4.txt (261267 bytes)

### FETCH https://laws.e-gov.go.jp/api/2/law_data/325CO0000000338
- purpose: tier 2 建築基準法施行令 (昇降機 class, エレベーター, 段差解消機 reference)
- prior (written before fetch): expect 昇降機 as class over エレベーター, エスカレーター, 小荷物専用昇降機; no 段差解消機 word (that lives in a 告示)
- result: status 200, 1677051 bytes, sha256 a4509c729cfa9c5e00745f026b60b88b3cb3379c18d5777f062775967f716664, artefact a4509c729cfa9c5e.json, text a4509c729cfa9c5e.txt (813751 bytes)

### FETCH https://laws.e-gov.go.jp/api/2/laws?law_title=%E8%B7%AF%E5%A4%96%E9%A7%90%E8%BB%8A%E5%A0%B4
- purpose: tier 2 locate 路外駐車場移動等円滑化基準 ordinance by title search
- prior (written before fetch): expect a list including 移動等円滑化のために必要な特定路外駐車場の構造及び設備に関する基準を定める省令
- result: status 200, 2871 bytes, sha256 66a218172f6fe5d84a20dd4a7644571d6e28ebafad1ed3374b4587422ed43b19, artefact 66a218172f6fe5d8.json, text - (0 bytes)

### FETCH https://laws.e-gov.go.jp/api/2/law_data/418M60000800112
- purpose: tier 2 路外駐車場移動等円滑化基準 (省令112)
- prior (written before fetch): expect 車椅子使用者用駐車施設 defined again, width 350cm; same code term as 政令379
- result: status 200, 15360 bytes, sha256 42279a446b2d8d278a2a73514823338618a57c1f2666b95623e1525f79dc594e, artefact 42279a446b2d8d27.json, text 42279a446b2d8d27.txt (6437 bytes)

### FETCH https://www.mlit.go.jp/sogoseisaku/barrierfree/sosei_barrierfree_tk_000362.html
- purpose: tier 4 MLIT page: parking permit schemes by local government
- prior (written before fetch): expect パーキング・パーミット制度, 障害者等用駐車区画, perhaps prefecture scheme names (思いやり駐車場, ゆずりあい駐車場)
- result: status 200, 21951 bytes, sha256 276b094a63182c98c6f280c5db33291003529246c0780bc615da04d4fb21b775, artefact 276b094a63182c98.xml, text 276b094a63182c98.txt (6568 bytes)

### FETCH https://www.mlit.go.jp/sogoseisaku/barrierfree/sosei_barrierfree_tk_000322.html
- purpose: tier 4 MLIT page: 車椅子使用者用駐車施設等の適正利用 guideline
- prior (written before fetch): expect 車椅子使用者用駐車施設等, 優先駐車区画, ダブルスペース; link to guideline PDF
- result: status 200, 10931 bytes, sha256 6b35786a20a88e4f5b3eb924dd0cb428fa74e92ddc15bec40e0e8520c3a65ccd, artefact 6b35786a20a88e4f.xml, text 6b35786a20a88e4f.txt (2547 bytes)

### FETCH https://www.mlit.go.jp/common/001285172.pdf
- purpose: tier 4 MLIT パーキング・パーミット制度事例集 (2019)
- prior (written before fetch): expect many local scheme names: 思いやり駐車場, ゆずりあい駐車場, 身障者用駐車場 as a colloquial/signage form
- result: status 200, 3779042 bytes, sha256 a9d9ff0ac21ef780be4447a681742d2c9f216d5d29d833a1828346431457bd6f, artefact a9d9ff0ac21ef780.pdf, text a9d9ff0ac21ef780.txt (89360 bytes)

## Discovery queries (WebSearch; results are URL leads only, never attestation)
- Q1 `DPI日本会議 車椅子使用者用駐車施設 適正利用 意見` — prior: a DPI page or statement naming the bay. Result: MLIT committee PDFs only (DPI is a committee member); no DPI-hosted page. Shape: organisation name + code term was too narrow.
- Q2 `大阪府 障がい者等用駐車区画利用証制度 対象者` — prior: Osaka page naming two bay types. Result: Osaka PDFs (tebiki_1.pdf, chirashi), Sakai city page. Fetched below.

### FETCH https://www.pref.osaka.lg.jp/documents/5328/tebiki_1.pdf
- purpose: tier 4 Osaka Prefecture permit scheme guide (tebiki)
- prior (written before fetch): expect 車いす使用者用駐車区画 and ゆずりあい駐車区画 as two bay forms, 障がい者 spelling
- result: status 408, 795 bytes, sha256 89b37885cb556977fc8d374e09a05c660bd09ba00cab953bd7e9c015679ee33b, artefact 89b37885cb556977.html, text - (0 bytes)

### FETCH https://www.city.sakai.lg.jp/kenko/fukushikaigo/shogaifukushi/syakai_sanka/seikatsu/kukaku123.html
- purpose: tier 4 Sakai City page on the Osaka permit scheme
- prior (written before fetch): expect the same two bay names; possibly 身障者用駐車場 colloquially
- result: status 408, 795 bytes, sha256 e6209cc22704ac98de4d3382bd3bec432b3d93fc78559c42adbb732a415a748a, artefact e6209cc22704ac98.html, text - (0 bytes)
- note: both direct fetches above returned 408 (Request Timeout) of 795 bytes; Wayback availability API: tebiki_1.pdf snapshot 20260715005729, Sakai page none.

### FETCH https://web.archive.org/web/20260715005729if_/https://www.pref.osaka.lg.jp/documents/5328/tebiki_1.pdf
- purpose: tier 4 Osaka permit scheme guide via Wayback if_
- prior (written before fetch): expect 車いす使用者用駐車区画 and ゆずりあい駐車区画 as two bay forms
- result: status None, 0 bytes, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, artefact e3b0c44298fc1c14.txt, text - (0 bytes)

### FETCH https://web.archive.org/web/20260715005729/https://www.pref.osaka.lg.jp/documents/5328/tebiki_1.pdf
- purpose: tier 4 Osaka permit scheme guide via Wayback plain form (retry, other form)
- prior (written before fetch): expect same as above; may reset
- result: status None, 0 bytes, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, artefact e3b0c44298fc1c14.txt, text - (0 bytes)

### FETCH https://www.pref.osaka.lg.jp/o090050/keikakusuishin/riyousyouseido/kyouryokushisetsu.html
- purpose: tier 4 Osaka scheme cooperating-facility page (direct)
- prior (written before fetch): expect 障がい者等用駐車区画, 車いす使用者用駐車区画, ゆずりあい駐車区画; may 408 again
- result: status 408, 795 bytes, sha256 a2d2bfd67011161d8fba32b17c833ccdff72d1fa3393ca06e946294efa190ce2, artefact a2d2bfd67011161d.html, text - (0 bytes)
- Q3 `佐賀県パーキングパーミット 身障者用駐車場利用証 制度 対象者` — prior: the Saga prefecture page. Result: no Saga page in results; Aichi, Okinawa, Iwate PDFs and MLIT PDFs. Shape: the scheme title as quoted by MLIT did not surface the issuer's own page.

### FETCH https://www.pref.aichi.jp/uploaded/attachment/577638.pdf
- purpose: tier 4 Aichi Prefecture parking-permit document
- prior (written before fetch): expect 愛知県パーキング・パーミット制度 with bay names (車いす使用者用駐車区画? 障害者等用駐車区画) and target groups
- result: status 302, 0 bytes, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, artefact e3b0c44298fc1c14.txt, text - (0 bytes)

### FETCH https://www.pref.iwate.jp/_res/projects/default_project/_page_/001/026/773/08_5pp.pdf
- purpose: tier 4 Iwate Prefecture document on ひとにやさしい駐車場
- prior (written before fetch): expect ひとにやさしい駐車場, 車いす使用者用駐車施設, target groups
- result: status 404, 2878 bytes, sha256 7c81a170a8ac500cd7cf9b523e6013ddf7ad25de6b40ba4fedf51df5d0dcc2d9, artefact 7c81a170a8ac500c.html, text - (0 bytes)

### FETCH https://www.pref.okinawa.lg.jp/_res/projects/default_project/_page_/001/014/549/6sannkousiryou1.pdf
- purpose: tier 4 Okinawa Prefecture reference document on ちゅらパーキング
- prior (written before fetch): expect ちゅらパーキング, 障害者等用駐車区画, maybe 車いす使用者用 and a second bay type
- result: status 200, 2527262 bytes, sha256 a40d1bcb48d589dcfce9f59c87ecfa84f6ca42261dc701eaef5fe6329be73442, artefact a40d1bcb48d589dc.pdf, text a40d1bcb48d589dc.txt (46050 bytes)
- note: Aichi 577638.pdf returned 302 with 0 bytes; Iwate 08_5pp.pdf returned 404. Okinawa 6sannkousiryou1.pdf retrieved; its p.1 reads word for word as the MLIT casebook p.3 (an included reference copy, judged by reading both), so it is not a second independent witness for p.1.
- Q4 `平成12年建設省告示第1413号 段差解消機 いす式階段昇降機 特殊な構造又は使用形態のエレベーター` — prior: the notice text on MLIT and a prefectural checklist. Result: Osaka, Gunma, Kanagawa checklists; MLIT PDFs; an elevator association (n-elekyo) yearbook. Shape: notice number + device names worked.

### FETCH https://www.pref.gunma.jp/site/fukushinomachi/2896.html
- purpose: tier 4 Gunma Prefecture welfare-town-planning guidance page (段差解消機)
- prior (written before fetch): expect 段差解消機 described as an elevator or a lift-shaped device along stairs; maybe いす式階段昇降機 excluded
- result: status 200, 25579 bytes, sha256 37545e8a68524cc8e412677d7a6ded8c74da57d1476224842528ff778473ab6d, artefact 37545e8a68524cc8.html, text 37545e8a68524cc8.txt (4796 bytes)

### FETCH https://www.mlit.go.jp/common/000027744.pdf
- purpose: tier 2 MLIT PDF possibly the text of 告示1413
- prior (written before fetch): expect the notice text naming 段差解消機 by structure only (車いすに座ったまま使用するエレベーター), いす式階段昇降機 as its own item
- result: status 200, 11351 bytes, sha256 559726bb5149989ac758339e2cfd2439b7d97bd569aff8ddc517df533c7825d8, artefact 559726bb5149989a.pdf, text 559726bb5149989a.txt (2 bytes)
- note: 000027744.pdf extracted to 2 bytes (fonts without a usable mapping); unreadable here, recorded as an empty extraction.
- Q5 `dpi-japan.org バリアフリー法 エレベーター 車いす使用者用駐車施設` — prior: a DPI Japan (Co-1 DPO) statement using the community's own forms. Result: one DPI PDF (2017-12 demands on the Act); others municipal/MLIT. Shape: domain token in the query did not restrict results; one DPO hit.

### FETCH https://www.dpi-japan.org/wp-content/uploads/2017/12/92adbba5d0fbc581240d403fd692b52d.pdf
- purpose: tier 5 DPI日本会議 2017-12 demands on the barrier-free Act
- prior (written before fetch): expect 車いす (hiragana) spelling, バリアフリー, エレベーター, perhaps 障害者用駐車場; may reject 多目的トイレ
- result: status 200, 46885 bytes, sha256 696353fb5d931b815a5a32b50f8612155e11783e2936ab93a31d28bb0ef1fc89, artefact 696353fb5d931b81.pdf, text 696353fb5d931b81.txt (2004 bytes)
- note: DPI PDF retrieved (200) but pdftotext extracted only digits and Latin (CJK fonts lack a usable mapping): unreadable here, no form taken from it.
- Q6 `DPI日本会議 ブログ 多機能トイレ 名称 車椅子使用者用便房 バリアフリー` — prior: a DPI page rejecting 多機能トイレ. Result: no DPI page; MLIT committee PDFs, a Mie prefecture PDF, a Tokyo welfare bureau document. Shape: the DPO name did not pull DPO-hosted pages in two tries; Co-1 tier left thin.

### FETCH https://www.pref.mie.lg.jp/common/content/001197868.pdf
- purpose: tier 4 Mie Prefecture ordinance-amendment document (多機能便房 renamed)
- prior (written before fetch): expect 多機能便房 as the old ordinance term mapped to 車椅子使用者用便房
- result: status 200, 143185 bytes, sha256 01d1e7758bdc65a97162522db95fcf17a96f2b3a30ddc3899b78e083a7835993, artefact 01d1e7758bdc65a9.pdf, text 01d1e7758bdc65a9.txt (9305 bytes)
