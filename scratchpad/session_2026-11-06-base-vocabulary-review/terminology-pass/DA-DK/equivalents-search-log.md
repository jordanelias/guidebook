# Equivalents search log — DA/DK (second pass), session_2026-11-06-base-vocabulary-review

Each prior is written to this file by the same command before the fetch runs (helper script in the session scratchpad, not kept). WebSearch queries are logged with their prior before the call is made, by hand in the same shell step. Query-shape notes follow results.

## Tier 1 — second reading of first-pass texts (local, no fetch)
- Q0 `grep -oiE "(parker|elevator|lift|løft|platform|handicap|tilgængelig|universel|kørestol|invalid|ligeværd|barriere|inklusi)" text/*.txt`. Prior: BR18 uses "parkeringspladser" and "elevator" only; no "lift". Result: "elevator, lift eller lignende" occurs in §§ 214-type wc clauses (kap. 9, 3 fragments); "handicaptoiletter" in § 62 stk. 2; "handicapegnede køretøjer" § 401; "universelt design" only in brugerbegreb guidance; "tilgængelig" mostly = open to the public. Shape: stem regex over the first-pass extracts; a hit is a string, sense read per occurrence below.

## Discovery queries (WebSearch, for locating sources only; results are never attestation)
- W1 query `parkeringskort til personer med handicap borger.dk`. Prior: borger.dk has a page "Parkeringskort til personer med handicap"; form "handicapparkering" likely on the page.
- W2 query `bekendtgørelse om vejafmærkning handicapparkering tavle E 33 undertavle`. Prior: the road-sign decree names an undertavle with the wheelchair symbol; wording maybe "forbeholdt" or "bevægelseshæmmede".
- W3 query `Dansk Handicap Forbund handicapparkering parkeringskort`. Prior: DHF administers the card; page uses "handicapparkeringskort" and "handicap-p-plads".
- W4 query `vejledning om elevatorer bygningsreglementet løfteplatform trappelift`. Prior: the BR18 elevator guidance names "løfteplatform", "trappelift" and maybe "plateaulift".
- W1-W4 results: borger.dk transport page, kk.dk 'Handicapparkering i København', brondby.dk handicapparkering, Retsinformation PDFs (eli/lta/2024/99/pdf; 2023/425 and 2023/426 vejafmærkning), bygningsreglementet.dk generel_vejledning PDFs (two media paths), gi.dk minielevator book. Search-engine summaries are not attestation and nothing is quoted from them. Shape: Danish administrative nouns worked; W3 named the wrong DPO (the card is issued by Danske Handicaporganisationer).

### F1 FETCH `https://www.retsinformation.dk/eli/lta/2024/99/pdf`
- Prior (written before the call): Retsinformation /eli/.../pdf serves a PDF (not the JS shell); parking-card decree titled 'parkeringskort for personer med handicap'; form 'handicapparkeringskort' may not occur
- Result: status 200, 180242 bytes, artefact 6e29bc47fa18a33d.pdf, sha256 6e29bc47fa18a33d, extracted 19853 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/6e29bc47fa18a33d.txt

### F2 FETCH `https://www.retsinformation.dk/eli/lta/2023/425/pdf`
- Prior (written before the call): Vejafmærkning decree PDF; E 33 Parkering and undertavle E 23 named 'Vejledning for invalide' or a newer name
- Result: status 200, 3018207 bytes, artefact 3d184d29f6ad6ad8.pdf, sha256 3d184d29f6ad6ad8, extracted 162133 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/3d184d29f6ad6ad8.txt

### F3 FETCH `https://www.retsinformation.dk/eli/lta/2023/426/pdf`
- Prior (written before the call): anvendelse af vejafmærkning; 'handicapparkering' or 'parkeringspladser for personer med handicap'
- Result: status 200, 13651581 bytes, artefact 88ed43f4be1606dc.pdf, sha256 88ed43f4be1606dc, extracted 307993 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/88ed43f4be1606dc.txt

### F4 FETCH `https://www.kk.dk/borger/parkering-trafik-og-veje/parkering/handicapparkering`
- Prior (written before the call): municipal page uses 'handicapparkering', 'handicap-p-plads', 'handicapparkeringskort'
- Result: status 200, 73196 bytes, artefact 1c0817588995bc03.html, sha256 1c0817588995bc03, extracted 2266 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/1c0817588995bc03.txt

### F5 FETCH `https://brondby.dk/borger/veje-og-trafik/parkering/handicapparkering`
- Prior (written before the call): Brøndby page uses 'handicapparkeringsplads' and 'parkeringskort'
- Result: status 200, 197137 bytes, artefact 9a28af88e95b4114.html, sha256 9a28af88e95b4114, extracted 11812 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/9a28af88e95b4114.txt

### F6 FETCH `https://www.borger.dk/handicap/hjaelpemidler/transport-for-personer-med-handicap`
- Prior (written before the call): borger.dk may be a JS shell; if text, 'parkeringskort til personer med handicap'
- Result: status None, 0 bytes, artefact e3b0c44298fc1c14.txt, sha256 e3b0c44298fc1c14, extracted 0 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/e3b0c44298fc1c14.txt

### F7 FETCH `https://www.bygningsreglementet.dk/media/bc2lu4q2/generel_vejledning.pdf`
- Prior (written before the call): one of these is the BR18 elevator guidance: 'løfteplatform', 'trappelift', 'type 2 elevator'
- Result: status 200, 261757 bytes, artefact 339ec718c3425b73.pdf, sha256 339ec718c3425b73, extracted 12131 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/339ec718c3425b73.txt

### F8 FETCH `https://bygningsreglementet.dk/media/xchn2hyy/generel_vejledning.pdf`
- Prior (written before the call): the other generel_vejledning PDF; unknown chapter
- Result: status 200, 261725 bytes, artefact fd5eebd4b262e531.pdf, sha256 fd5eebd4b262e531, extracted 12131 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/fd5eebd4b262e531.txt
- F1-F8 notes: F1 is BEK nr. 99 af 30/01/2024 (tier 2, in force per its own date). F2 BEK nr. 425 af 13/04/2023 vejafmærkning, F3 BEK nr. 426 af 13/04/2023 anvendelse af vejafmærkning (tier 3 signage decrees). F4 kk.dk and F5 brondby.dk read (tier 4). F6 borger.dk returned 0 bytes (empty, recorded). F7 and F8 are byte-different copies of one 5-page "Bygningsreglementets vejledning om elevatorer" with identical extracted text (F7 used). Retsinformation's /eli/lta/<year>/<nr>/pdf route serves the PDF, unlike the HTML route the first pass hit (first-pass D2 is route-specific).
- W5 query `trappelift kommune hjælpemiddel boligændring`. Prior: municipal hjælpemiddel pages use "trappelift" and maybe "trappeelevator", "stolelift", "plateaulift".
- W6 query `Danske Handicaporganisationer tilgængelighed "handicapvenlig"`. Prior: DH uses "tilgængelighed" and "tilgængelig for alle"; "handicapvenlig" colloquial, possibly criticised.
- W7 query `God Adgang tilgængelighedsmærkning kriterier`. Prior: God Adgang uses "tilgængelighed" with user-group symbols (bevægelse, syn, hørelse...).
- W5-W7 results: kk.dk hjælpemidler pages, sundhed.dk, Ankestyrelsen on Retsinformation; DH (handicap.dk) PDFs incl. the 2024 civil-society report to the UN committee; God Adgang reports (Svendborg library), borger.dk 'Fysisk tilgængelighed'. Shape: W6's quoted 'handicapvenlig' gave no DH page using it; W7 gave inspection reports, not the criteria list.

### F9 FETCH `https://www.borger.dk/handicap/tilgaengelighed-og-handicap/fysisk-tilgaengelighed`
- Prior (written before the call): borger.dk may return empty again (as F6); if text: 'fysisk tilgængelighed', 'handicapvenlig' unlikely
- Result: status None, 0 bytes, artefact e3b0c44298fc1c14.txt, sha256 e3b0c44298fc1c14, extracted 0 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/e3b0c44298fc1c14.txt

### F10 FETCH `https://svendborgbibliotek.dk/sites/svendborgbibliotek.dk/files/god_adgang_maerkning_af_thuroe_bibliotek_-_tilbagemelding.pdf`
- Prior (written before the call): God Adgang inspection report: 'kørestolsbrugere', 'handicapparkering' or 'handicap-p-plads', 'elevator', 'lift'
- Result: status 404, 123019 bytes, artefact c66dff981ac6423f.html, sha256 c66dff981ac6423f, extracted 2183 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/c66dff981ac6423f.txt

### F11 FETCH `https://handicap.dk/files/media/document/Civilsamfundsrapport%20til%20FN%27s%20Handicapkomit%C3%A9%20fra%20Danmark%20og%20F%C3%A6r%C3%B8erne%202024-654121_%281%29.pdf`
- Prior (written before the call): DH civil-society report (Co-1): 'tilgængelighed', 'universelt design', 'handicapparkering' maybe; 'elevatorer' at stations
- Result: status 200, 1089858 bytes, artefact 5c395d7f220e0fe2.pdf, sha256 5c395d7f220e0fe2, extracted 116328 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/5c395d7f220e0fe2.txt

### F12 FETCH `https://www.kk.dk/borger/sundhed-og-forebyggelse/sygdom/hjerneskade/hjaelpemidler-og-boligaendringer`
- Prior (written before the call): kk.dk hjælpemidler/boligændringer page lists 'trappelift' and perhaps 'loftlift'
- Result: status 200, 69181 bytes, artefact ddb59c5967a6b9d6.html, sha256 ddb59c5967a6b9d6, extracted 4307 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/ddb59c5967a6b9d6.txt

### F13 FETCH `https://www.viborg.dk/media/blhflbc4/god-adgang-statusrapport.pdf`
- Prior (written before the call): Viborg God Adgang status report: 'tilgængelighed', 'God Adgang', parking and lift forms
- Result: status 200, 582306 bytes, artefact d5065665c76684ef.pdf, sha256 d5065665c76684ef, extracted 11661 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/d5065665c76684ef.txt
- F9-F13 notes: F9 borger.dk empty again (0 bytes; two of two borger.dk fetches empty, so the host is unreachable by this route). F10 Svendborg library URL 404 (page body recorded, not used). F11 DH civil-society report 2024 read by grep for the qualifier, parking and lift stems (not in full). F12 kk.dk hjælpemidler page read in full (short). F13 Viborg God Adgang status report read in full (11 pp. text).
- W8 query `"Færdselsarealer for alle" håndbog i tilgængelighed vejregler pdf`. Prior: Vejdirektoratet hosts it on vejregler.lovportaler.dk, possibly a JS portal; a PDF copy may exist on a municipal site.
- W9 query `"handicapvenlig" site:dk kommune`. Prior: municipal pages use "handicapvenlig" for toilets, beaches or playgrounds as a colloquial qualifier.
- W8-W9 results: 2023 vejregel 'Færdselsarealer for alle – Universelt design og tilgængelighed' mirrored on albertslund.dk; 2017 edition (aarhus.dk, filename '_dh'); vejregel 'Anlæg for parkering og standsning i byer' 2023 (albertslund.dk); Mariagerfjord handicappolitik PDF using 'handicapvenlig'. Shape: the quoted title found mirrors; no vejregler.dk link surfaced. Mirrors are named as such in the source column.

### F14 FETCH `https://albertslund.dk/media/4n5lhfp5/vejdirektoratet_2023c_faerdselsarealer-for-alle-universelt-design-og-tilgaengelighed_haandbog.pdf`
- Prior (written before the call): 2023 vejregel: 'universelt design' as umbrella, 'handicapparkering' or 'handicapparkeringsplads', 'kørestolsbrugere', 'ledelinjer'
- Result: status 200, 18608082 bytes, artefact e1ebf8c5bfa8b8fc.pdf, sha256 e1ebf8c5bfa8b8fc, extracted 218955 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/e1ebf8c5bfa8b8fc.txt

### F15 FETCH `https://albertslund.dk/media/ddadxbsj/vejdirektoratet_2023_anlaeg-for-parkering-og-stadsning-i-byer.pdf`
- Prior (written before the call): parking vejregel: 'handicapparkeringspladser', 'p-pladser for handicappede', 'handicapbås' and maybe 'kørestolsbrugere'
- Result: status 200, 13919868 bytes, artefact 5b92c3f2f3898cc0.pdf, sha256 5b92c3f2f3898cc0, extracted 169781 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/5b92c3f2f3898cc0.txt

### F16 FETCH `https://www.mariagerfjord.dk/media/ugdd0fao/handicappolitik.pdf`
- Prior (written before the call): handicappolitik: 'handicapvenlig kommune', 'tilgængelig for alle'
- Result: status 200, 76019 bytes, artefact b60cd88ae258df66.pdf, sha256 b60cd88ae258df66, extracted 13167 chars -> scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK/text/b60cd88ae258df66.txt
- F14-F16 notes: F14 (2023 Færdselsarealer for alle, 18.6 MB) and F15 (2023 Anlæg for parkering og standsning i byer, 13.9 MB) are Vejdirektoratet vejregler fetched from Albertslund Kommune's mirror (vejregler.dk not reached); read by stem grep and located passages, not in full. F16 Mariagerfjord policy read in full (undated). Prior for F15 partly wrong: no "p-pladser for handicappede"; instead "Handicapparkeringspladser" (heading 4.4), "handicapparkeringsbåse", "Handicappladser til kassevogne", and "lift" meaning a vehicle tail lift.
- F2/F3/F1 re-extracted with `pdftotext` (no -layout) as `<sha16>.flow.txt`: the -layout extraction interleaves the two columns, so quotes are verified against the reading-order extraction; page numbers are PDF pages, not printed page numbers.

## Tier 1 second reading, further greps (local)
- Q1 `grep -n "^§"` over the kap. 9 fragments to assign § numbers to the "elevator, lift eller lignende" lines. Prior: §§ 215, 216, 224. Result: § 215 (5d525b6233ea1586 l. 25), § 216 (l. 29, 31), § 224 (a62e0887da12d2c1 l. 39, 41).
- Q2 stems rampe, håndl, støttegreb, manøvre/vendeplads, dørtrin/niveaufri, teleslyng, ledelinje/taktil, symbol, wc-rum/handicaptoilet, fri passage/dørbredde over all texts. Prior: second forms for ramp, toilet, loop, symbol; none for door width or turning. Result as prior: no second form for fri passagebredde or frit manøvreareal in any text read; "vendeplads(er)" occurs only for vehicles in the road decrees (not the WC turning space; not recorded).

## Verification
- Every quote in `equivalents.tsv` was checked verbatim (whitespace-collapsed) against the saved extraction, and every PDF locator's page against the page holding the quote, by a throwaway script in the session scratchpad (not kept; minimise code). 59 rows, 0 quote failures, 0 page mismatches at writing. The script first mis-tiered Brøndby rows as tier 1 (a prefix test caught "BRO" as BR18); fixed before writing.
