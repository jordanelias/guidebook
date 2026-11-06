# Equivalents record, JA-JP (2026-11-06)

**Verdict.** The three owner classes are covered in Japanese, from the code (tier 1), road law and building law (tier 2), one road-sign ordinance (tier 3) and ministry and prefectural pages (tier 4). There are no Co-1 forms (tier 5): two DPO searches found no DPO page, and the one DPI Japan PDF retrieved had no extractable Japanese text. 19 register-v2 concepts were attempted out of 560, chosen as the owner classes plus the element classes where the first pass had already seen a variant pair. Nothing was written to the DB, committed or pushed.

## Counts (re-run, do not trust; from this folder)
- Rows: `tail -n +2 equivalents.tsv | wc -l`. By usage type: `tail -n +2 equivalents.tsv | cut -f6 | sort | uniq -c`. By tier: `... | cut -f8 | sort | uniq -c`. Concepts: `... | cut -f1 | sort -u`. Rows with a conflation note: `awk -F'\t' 'NR>1 && $12!=""' equivalents.tsv | wc -l`. On 2026-11-06 these gave 93 rows; 40 code term, 15 product name, 15 qualifier, 9 regional variant, 8 colloquial, 5 outdated or disfavoured, 1 unattested seed; tiers 1:43, 2:7, 3:1, 4:41, seed:1; 19 concepts; 25 conflation notes.
- Attempted: R2-050 R2-051 R2-281 (parking); R2-333 R2-424 (qualifier); R2-163 R2-164 R2-165 R2-166 R2-168 R2-169 (vertical transport); R2-178 (toilet names); R2-013 R2-014 R2-211 R2-093 R2-094 R2-095 R2-083 (variant pairs). Not attempted: every other row.

## The owner classes in Japanese
- **Parking.** The code term is 車椅子使用者用駐車施設 (政令379 Art.18(1)). The Act's phrase is 車椅子を使用している者が円滑に利用することができる駐車施設, and 路外駐車場車椅子使用者用駐車施設 is the off-street form. Guidance prose has the variants 車椅子使用者用駐車区画 and 車椅子利用者用駐車施設. The local permit schemes add 障害者等用駐車区画 (also spelled 障がい者等用), 身体障害者等用駐車場, 身障者用駐車場 (disfavoured), 車いす使用者等用駐車場 and 障害者等専用駐車場. There are also about 15 scheme brands: おもいやり／思いやり駐車場, ゆずりあい駐車場, ハートフル, ちゅらパーキング and others. The second bay is 優先駐車区画. Road law has a separate on-street object, 高齢運転者等専用（時間制限）駐車区間, with the sign 高齢運転者等標章自動車駐車可.
- **Umbrella qualifier.** The code's terms are 移動等円滑化 (the defined aim, R2-424), its qualifier 移動等円滑化の措置がとられた, and the long form 高齢者、障害者等が円滑に利用できる. バリアフリー is the colloquial word and is the defined short title of the Act in the design standard. ユニバーサルデザイン (UD) is wider and is framed as covering everyone. The text also uses アクセシビリティ／アクセシブル, the current JIS wording 障害のある人が使える, the outdated 身障者用, and the narrower 車椅子使用者用 / 車いす使用者用. 人にやさしい and 福祉のまちづくり are the prefectural welfare framing. There is no インクルーシブ in any text read.
- **Vertical transport.** エレベーター is the code term, and the building-law definition sits under the class 昇降機 (建築基準法施行令 Art.129-3). The car is written 籠 in 政令379 and かご in 規則110, an orthographic pair with identical definitions. 段差解消機 is the platform lift, and the design standard defines it as a kind of エレベーター. It splits into 鉛直型 (vertical) and 斜行型 (inclined, along stairs). In prefectural guidance it is called リフト or リフト状のエレベーター. In law, リフト alone names the goods hoist 簡易リフト. いす式階段昇降機 is a seed only.

## Conflations (each has its own locator in the TSV)
1. Platform lift and elevator: 段差解消機 is legally an エレベーター (pdf p.215), and Gunma writes リフト状のエレベーター. One word covers both the vertical and the stair-inclined device.
2. 昇降機 is used for a person lift (政令379 Art.19) and, one article earlier, for a car-stacking machine (Art.18).
3. Who may use the parking: the permit schemes' 障害者等用駐車区画 admits older people needing care, pregnant women and injured people (casebook p.3). Those are the users the design standard sends to the separate 優先駐車区画 (p.52). Brand names such as おもいやり駐車場 do not say which of the two bays they mean.
4. 傾斜路 (a built ramp) is said to include 据え置き型スロープ (a placed portable device) (p.164).
5. 多機能／多目的 were names for one all-in-one toilet. The design standard rules them out (p.144), and Mie renamed 多機能便房 to 車椅子使用者用便房 "in name only".

## Could not obtain
The Osaka scheme guide (408 directly; the Wayback snapshot returned no bytes on either form), the Aichi PDF (302 with no body), the Iwate PDF (404), and the 告示1413 text (MLIT PDF, no font mapping). The DPI Japan PDF also had no font mapping. JIS Z 8210 and JIS T 9251 remain NOT-OBTAINABLE (first pass).

## Self-attack
1. Tier 4 is dominated by one page, the MLIT prefecture list: 24 of the 41 tier-4 rows on 2026-11-06 (`grep -c sosei_barrierfree_tk_000362 equivalents.tsv`). Those rows are scheme names quoted by a ministry, not the prefectures' own pages, and the bay a brand names was inferred from the scheme title.
2. Usage types are my judgment. The brief's closed list has no orthographic slot, so I filed spelling pairs under "code term" or "regional variant", and lexical variants inside one issuer's prose under "colloquial". A reader could reasonably regroup them.
3. There is no Co-1 voice. The community's own forms, and the forms it rejects (for example any objection to 身障者 or 障害者 versus 障がい者), are unrecorded. 身障者 is marked disfavoured only by analogy with the 2010 JIS pictogram rename.
4. Second-bay users and the permit-scheme bay are compared only through two MLIT documents. Prefectural scheme rules (e.g. Osaka's two permit colours) were seen only in a search summary and are not recorded.
5. The quote checks ran against my own extraction, with whitespace removed and restricted to the page. Two-column PDF pages (casebook p.3, design standard p.57) could join text from neighbouring columns: the p.57 quote carries the PDF's own line-break space (車椅子利 用者).
