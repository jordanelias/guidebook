# Equivalents search log — DE/DE (Germany), session_2026-11-06-base-vocabulary-review

Second pass (EQUIV-BRIEF.md). Each entry: fetch or query verbatim, PRIOR (appended to this file by the same command, before `retrieval_log.fetch` ran), RESULT, SHAPE. Empties kept. Jurisdiction of every source is recorded; Austrian and Swiss sources are not used for DE.

## E0 — tier 1, second reading of the first-pass texts (local grep, no fetch)
- Query: `grep -noiE '[A-Za-zÄÖÜäöüß-]*(stellpl|parkpl|parkier|parkm|aufz|fahrstuhl|lift|hebeb|hubpl|plattform|rollstuhlgerecht|behindertengerecht|rollstuhlnutz|barrierearm|universell|inklusiv|design for all|zugänglich|uneingeschränkt)[A-Za-zÄÖÜäöüß-]*'` over the seven saved texts in `text/`.
- PRIOR (written before the grep): parking appears only as "Stellplätze" (BayBO, DIN TOC) with no disability-marked parking noun; lift words Aufzug, Plattformaufzug, Treppenlift; no "behindertengerecht" or "rollstuhlgerecht" in any official text.
- RESULT: as expected. Parking: "Stellplätze" (BayBO Art. 48 Abs. 2 Nr. 9 and Satz 4; BayTB Anlage A 4.2/2Bay Nr. 07), "PKW-Stellplätze" (DIN 18040-1 and -2 TOC 4.2.2); no Behindertenparkplatz form. Lifts: Aufzug/Aufzüge (ASR, BayBO), Aufzugsanlagen (DIN TOC 4.3.5), Plattformaufzüge / Vertikale Plattformaufzüge / Förderplattform (ASR A1.8 Abs. 12, 19; BayTB Nr. 010), Treppenlifte (ASR; BayTB Anlage A 4.2/1), Hublift (ASR A1.8 Abs. 11), and bare "Lift" for the stair lift (BayTB Anlage A 4.2/1 Nr. 2 Ziff. 3–4). No rollstuhlgerecht, behindertengerecht, barrierearm, universell or inklusiv. "öffentlich zugängige" (DIN 18024-2 title, quoted on the DIN Media page) is an older spelling of "zugängliche".
- SHAPE: stem regex; misses forms with no listed stem (none expected in these texts).

## E1 — StVO § 45 (federal road traffic regulation)
- Fetch: `https://www.gesetze-im-internet.de/stvo_2013/__45.html`
- PRIOR: § 45 Abs. 1b Nr. 2 names 'Parkmöglichkeiten für schwerbehinderte Menschen mit außergewöhnlicher Gehbehinderung' and blind people; no 'Behindertenparkplatz'.

## E2 — StVO § 46 (exceptions; parking relief)
- Fetch: `https://www.gesetze-im-internet.de/stvo_2013/__46.html`
- PRIOR: § 46 Abs. 1 Nr. 11 permits exceptions; may name 'Parkausweis' or not; probably refers to signs only.

## E3 — StVO Anlage 3 (Richtzeichen incl. Zeichen 314)
- Fetch: `https://www.gesetze-im-internet.de/stvo_2013/anlage_3.html`
- PRIOR: Anlage 3 lfd. Nr. 7 Zeichen 314 Parken; the explanatory text mentions the Zusatzzeichen with Rollstuhlfahrersinnbild and 'Schwerbehinderte mit außergewöhnlicher Gehbehinderung ... blinde Menschen' and 'Parkausweis Nr.'. Sign images not readable.

## E4 — VwV-StVO (federal administrative regulation to the StVO)
- Fetch: `https://www.verwaltungsvorschriften-im-internet.de/bsvwvbund_26012001_S3236420014.htm`
- PRIOR: The VwV to § 45 and § 46 uses a noun for the reserved bay, possibly 'Parkplätze für Schwerbehinderte' or 'Behindertenparkplätze', distinguishes general from personal (Parkausweis-Nr.) bays, and names the EU-model 'Parkausweis'.

## E5 — BayBO Art. 37 (Land Bayern)
- Fetch: `https://www.gesetze-bayern.de/Content/Document/BayBO-37`
- PRIOR: Art. 37 uses 'Aufzüge' (code term) and requires lifts that take 'Rollstühle' and 'Krankentragen'; no 'Fahrstuhl' or 'Lift'.

## E6 — BayGaStellV (Land Bayern, garage and parking regulation)
- Fetch: `https://www.gesetze-bayern.de/Content/Document/BayGaStellV`
- PRIOR: GaStellV may define Stellplatz and possibly 'Stellplätze für Menschen mit Behinderung' or none; 50/50.

## E7 — StVO § 39 (Sinnbilder list)
- Fetch: `https://www.gesetze-im-internet.de/stvo_2013/__39.html`
- PRIOR: § 39 Abs. 7 lists Sinnbilder as images with captions; a caption 'Rollstuhlfahrer' or 'Schwerbehinderte' appears; captions may be images only (then empty).

## E8 — Landeshauptstadt München service page (Land Bayern, municipal)
- Fetch: `https://stadt.muenchen.de/infos/park-ausweis-mensch-mit-behinderung-ls.html`
- PRIOR: Municipal page uses 'blauer Parkausweis', 'EU-Parkausweis', 'Behindertenparkplatz' and possibly 'orangefarbener Parkausweis'; written partly in Leichte Sprache ('-ls' in URL).

## E9 — LAGeSo Berlin flyer Parkerleichterung 2024 (Land Berlin, public body)
- Fetch: `https://berlin.de/lageso/_assets/behinderung/schwerbehinderung-versorgungsamt/publikationen/2024_flyer-parkerleichterung_web.pdf`
- PRIOR: Flyer names 'blauer Parkausweis', 'Merkzeichen aG', 'Behindertenparkplätze' or 'Schwerbehindertenparkplätze', and the Berlin-only orange card if any.

## E10 — Stadt Stuttgart service page (Land Baden-Württemberg, municipal)
- Fetch: `https://www.stuttgart.de/organigramm/leistungen/parkerleichterungen-fuer-menschen-mit-schweren-behinderungen-beantragen-blauer-parkausweis-`
- PRIOR: Uses 'blauer Parkausweis' and 'orangefarbener Parkausweis'; parking-bay noun 'Behindertenparkplätze' or 'Schwerbehindertenparkplätze'.

## E11 — Leidmedien.de term list (Sozialhelden e.V., Berlin; disabled-led media project, Co-1 candidate)
- Fetch: `https://leidmedien.de/begriffe/`
- PRIOR: A term list advising against 'behindertengerecht' and perhaps 'Behindertenparkplatz' wording; recommends 'barrierefrei'. Path guessed; may 404.

## E12 — Wheelmap.org (Sozialhelden e.V., Berlin; disabled-led product)
- Fetch: `https://wheelmap.org/`
- PRIOR: Homepage carries 'rollstuhlgerecht', 'teilweise rollstuhlgerecht', 'nicht rollstuhlgerecht' (Wheelmap traffic-light categories); may be a JS shell.

## E13 — Wheelmap FAQ via Wayback if_ (Sozialhelden e.V., Berlin)
- Fetch: `https://web.archive.org/web/20260510112724if_/https://news.wheelmap.org/faq/`
- PRIOR: German FAQ defines 'voll rollstuhlgerecht', 'teilweise rollstuhlgerecht', 'nicht rollstuhlgerecht'; may serve English by default.

## E14 — Wheelmap FAQ, plain Wayback form (retry per CLAUDE.md s.7)
- Fetch: `https://web.archive.org/web/20260510112724/https://news.wheelmap.org/faq/`
- PRIOR: Same as E13; plain form may also reset.

## E15 — BBSR Leitfaden Barrierefreies Bauen 2.0 (Bund, federal guidance; copy held by ULB Bonn Pflichtexemplar)
- Fetch: `https://epflicht.ulb.uni-bonn.de/download/pdf/806182`
- PRIOR: Federal guide uses 'barrierefreie PKW-Stellplätze' or 'Stellplätze für Menschen mit Behinderungen', 'Aufzug', and the qualifiers 'inklusiv' and possibly 'Design für Alle' / 'universelles Design'; 'behindertengerecht' absent.

## E16 — BVG FAQ Barrierefreiheit (Berliner Verkehrsbetriebe, Land Berlin public transport operator)
- Fetch: `https://www.bvg.de/de/service-und-kontakt/barrierefreiheit-bei-der-bvg/faq`
- PRIOR: FAQ uses 'Aufzug' / 'Aufzüge', 'stufenlos', 'barrierefrei', maybe 'Fahrstuhl' colloquially; may be a JS shell.

## E17 — Abgeordnetenhaus Berlin Schriftliche Anfrage S19-26488 (Land Berlin, parliament/Senate answer)
- Fetch: `https://pardok.parlament-berlin.de/starweb/adis/citat/VT/19/SchrAnfr/S19-26488.pdf`
- PRIOR: Answer distinguishes 'stufenlos erreichbar' from 'barrierefrei' (ramp stations at 10 % gradient), uses 'Aufzugsanlagen'.

## E18 — Stadt Hameln Hinweise Behindertenparkplätze (Land Niedersachsen, municipal)
- Fetch: `https://www.hameln.de/fileadmin/media/Dokumente/Abt._22__Ordnung_und_Strassenverkehr/Strassenverkehr_und_Luft/Hinweise_Behindertenparkplaetze.pdf`
- PRIOR: Municipal leaflet uses 'Behindertenparkplatz' in its title, distinguishes 'allgemeiner' from 'personengebundener' bay, and the blue/orange cards.

## E19 — Verkehrsblatt-Verlag Parkausweise Prospekt (federal official-notice publisher)
- Fetch: `https://verkehrsblatt.de/pdf/Parkausweise_Prospekt.pdf`
- PRIOR: Sales leaflet for the printed card forms: names 'Parkausweis für Menschen mit Behinderungen' (EU model) and maybe 'orangefarbener Parkausweis' as product names.

## E20 — BSK e.V. ABC barrierefreies Bauen (Bundesverband Selbsthilfe Körperbehinderter, Krautheim; DPO, Co-1 candidate)
- Fetch: `https://www.bsk-ev.org/informieren/barrierefreies-bauen/abc-barrierefreies-bauen/abc-barierefreies-bauen`
- PRIOR: A glossary distinguishing 'barrierefrei' from 'rollstuhlgerecht' (DIN 18040-2 R), naming 'Aufzug', 'Treppenlift', 'Hublift', perhaps rejecting 'behindertengerecht'.

## E21 — Bundesfachstelle Barrierefreiheit checklist § 8 BGG (federal public body)
- Fetch: `https://www.bundesfachstelle-barrierefreiheit.de/SharedDocs/Downloads/DE/Veroeffentlichungen/checkliste-paragraf-8-bgg.pdf?__blob=publicationFile&v=6`
- PRIOR: Federal checklist uses 'Behindertenparkplatz' or 'barrierefreier Stellplatz', 'Aufzug', 'rollstuhlgerecht'; may be a Bunny-Shield-type block.

## E22 — DIN EN 81-40:2020-12 free table of contents (DIN, NAM; German adoption of EN)
- Fetch: `https://www.din.de/de/mitwirken/normenausschuesse/nam/veroeffentlichungen/wdc-beuth:din21:309233271/toc-3070646/download`
- PRIOR: German title 'Treppenschrägaufzüge und Plattformaufzüge mit geneigter Fahrbahn für Personen mit eingeschränkter Mobilität'; TOC may carry Sitzlift / Stehplattform / Rollstuhlplattform terms.

## E23 — Stadt Eberswalde press release 89/2026 (Land Brandenburg, municipal)
- Fetch: `https://www.eberswalde.de/publications/Pressemitteilungen/ARCHIV/2026/89-11.05.2026-Fahrstuhl_Sanierung_Rathaus.pdf`
- PRIOR: Municipal release uses 'Fahrstuhl' / 'Fahrstuhlanlage' in title and body, maybe also 'Aufzug' in the same text (within-source equivalence).

## E24 — LBauO Rheinland-Pfalz § 51 Abs. 1 (Land Rheinland-Pfalz; copy on nullbarriere.de, a private mirror)
- Fetch: `https://nullbarriere.de/files/pdf/gesetze/paragraf-51-abs1-lbauo-rlp.pdf`
- PRIOR: § 51 Abs. 1 says Wohnungen must be 'barrierefrei' and one 'uneingeschränkt mit dem Rollstuhl nutzbar'; the word 'rollstuhlgerecht' is absent from the statute.

---
## Results for E1–E24 (written after the fetches; each PRIOR above was appended by the same command before `fetch()` ran)
Text extracts are in `text/<sha16>.txt` (not committed); manifest lines are in `retrieval-log/session_2026-11-06-base-vocabulary-review/manifest.jsonl`.

- **E1 StVO § 45** — 200. RESULT: as expected. Abs. 1b Satz 1 Nr. 2 "Parkmöglichkeiten für schwerbehinderte Menschen mit außergewöhnlicher Gehbehinderung … sowie für blinde Menschen". No noun for the bay. SHAPE: direct statute URL, known pattern.
- **E2 StVO § 46** — 200. RESULT: only "Bewohnerparkausweise" and "Parkausweise" in general; no disability-parking noun. Empty for the class.
- **E3 StVO Anlage 3** — 200. RESULT: lfd. Nr. 7 Zeichen 314 and lfd. Nr. 10 Zeichen 315: "Zusatzzeichen mit Rollstuhlfahrersinnbild"; the restricted group again includes blind people. Sign images not read.
- **E4 VwV-StVO** — 200, ISO-8859-1 (first extraction as UTF-8 was garbled; re-decoded from the same bytes). RESULT: richer than expected: "Parkplätzen für schwerbehinderte Menschen" (zu § 45, X., Rn. 20), the personal bay "Parkplätze für bestimmte schwerbehinderte Menschen" (Rn. 23), "Rollstuhlfahrersymbol" (Rn. 21, 22, 28), "EU-einheitliche(n) Parkausweis (für behinderte Menschen)" (zu § 46), and, unexpected, "behindertengerecht" (zu § 26, Rn. 14). No "Behindertenparkplatz".
- **E5 BayBO Art. 37** — 200. RESULT: as expected, plus Fahrkorb/Fahrschacht, "Aufzug für Rollstühle und Krankentragen", "stufenlos erreichbar", "Bewegungsfläche", "lichte Durchgangsbreite".
- **E6 BayGaStellV** — 404 (URL guessed). EMPTY; not retried (budget). The Land garage regulation remains NOT-READ.
- **E7 StVO § 39** — 200. RESULT: the Abs. 7 Sinnbild captions carry no wheelchair symbol. EMPTY for the class.
- **WebSearch W1** `service.berlin.de Parkausweis Menschen mit Behinderungen Behindertenparkplatz beantragen` — PRIOR (NOT written before the search; reconstructed afterwards, an R14 defect): Berlin service page plus other cities. RESULT: Berlin portal pages (navigation only), LAGeSo flyer, München, Stuttgart, Heidelberg URLs. Search summary not used as attestation.
- **WebSearch W2** `Leitfaden Barrierefreies Bauen Bundesministerium PDF barrierefreie Stellplätze Aufzug` — PRIOR (NOT written before the search; reconstructed afterwards, an R14 defect): BBSR/BMWSB guide. RESULT: Leitfaden 2.0 (ULB Bonn copy) and Land/municipal guides.
- **WebSearch W3** `leidmedien.de Begriffe behindertengerecht barrierefrei Behindertenparkplatz` — PRIOR (NOT written before the search; reconstructed afterwards, an R14 defect): Leidmedien term list. RESULT: no direct page; secondary sources only (not used).
- **E8 München (Leichte Sprache)** — 200. RESULT: "Behinderten-Park-Plätzen", "eigenen Park-Platz"; no "blauer Parkausweis" on this page. Soft hyphens (U+00AD) inside some words.
- **E9 LAGeSo Berlin flyer** — 404. EMPTY (the search result URL was dead). Not retried via Wayback (budget).
- **E10 Stuttgart** — 200. RESULT: "Parkplätzen (Behindertenparkplätze)", "blauer Parkausweis", "Schwerbehindertenparkausweise". No orange card on this page.
- **E11 Leidmedien.de /begriffe/** — 200. RESULT: a person-language list (Ableismus, beeinträchtigt, "Der Rollstuhl"); no built-environment qualifier, no parking or lift form. EMPTY for the three classes. SHAPE: guessed path; the page exists but treats people-words only.
- **E12 Wheelmap.org** — 403 (Cloudflare JS challenge). **E13** Wayback `if_` of news.wheelmap.org/faq/ (snapshot 20260510112724 from the availability API) — no HTTP response (status null, 0 bytes). **E14** plain Wayback form — same. Per CLAUDE.md s.7, both forms tried once each; Wheelmap categories stay unattested (seed row).
- **E15 BBSR Leitfaden Barrierefreies Bauen 2.0** — 200, 2.4 MB PDF. RESULT: "barrierefreie(r) Stellplatz/Stellplätze", "Stellplätzen für Menschen mit Behinderungen", "inklusiv", "Design für alle", "Konzeption für alle Nutzer", "universellen Designs", "Zugänglichkeit", "Aufzugskabine". No "behindertengerecht". Read: grep-located passages only [SKIPPED: the rest of the 69 pages].
- **WebSearch W4** `BVG barrierefrei Aufzug U-Bahnhof stufenlos Rampe Hublift Seite` — PRIOR (NOT written before the search; reconstructed afterwards, an R14 defect): BVG accessibility pages. RESULT: BVG FAQ and an Abgeordnetenhaus Schriftliche Anfrage.
- **E16 BVG FAQ** — 200. RESULT: "Aufzug/Aufzüge/Aufzugsstörungen", "voll barrierefrei" (app filter), "brokenlifts.org", "mobile Rampe" and bare "Rampe" for both station ramps and the vehicle device. No "Fahrstuhl".
- **E17 Berlin Drucksache 19/26 488** — 200. RESULT: "Aufzugsanlagen", "stufenlos erreichbar, jedoch nicht vollständig barrierefrei", "Rampen mit einer Steigung von 10 %". Exceeded the prior: the source ranks step-free below barrierefrei.
- **WebSearch W5** `BSK Bundesverband Selbsthilfe Körperbehinderter Behindertenparkplatz Parkausweis rollstuhlgerecht` — PRIOR (NOT written before the search; reconstructed afterwards, an R14 defect): a BSK page. RESULT: no BSK page; municipal leaflets (Hameln) and Verkehrsblatt. Commercial law and news sites ignored per brief.
- **E18 Hameln leaflet** — 200. RESULT: OCR text layer of a scan; "Behindertenparkplätze", "Behinderten-Parkplätzen", "Rollstuhlsymbol", "blauen Parkausweis". Undated.
- **E19 Verkehrsblatt Prospekt** — 200. RESULT: "Behinderten-/parkplätzen" (line-broken), "Piktogramm eines Roll-/stuhlfahrers", the orange "Ausweis zur Ausnahmegenehmigung" (a product) which "gilt nicht für Parkplätze mit Zusatzzeichen (Rollstuhlfahrersymbol)".
- **WebSearch W6** `rollstuhlgerecht barrierefrei Unterschied Aufzug Parkplatz`, allowed_domains bsk-ev.org, isl-ev.de, dbsv.org, vdk.de, abid-ev.de, sozialhelden.de, wheelmap.org, rollstuhlfahrer.de, behindertenbeauftragter.de, bundesfachstelle-barrierefreiheit.de — PRIOR (NOT written before the search; reconstructed afterwards, an R14 defect): a DPO glossary. RESULT: BSK ABC page and the Bundesfachstelle checklist.
- **E20 BSK ABC barrierefreies Bauen** — 200. RESULT: "PKW-Stellplätze", "Aufzug", "Vertikale Erschließung", "2-Kanal-Prinzip" (two routes) beside "Zwei-Sinne-Prinzip" (senses); no "rollstuhlgerecht", no "behindertengerecht". Prior partly wrong: the glossary rejects no form.
- **E21 Bundesfachstelle checklist (§ 8 BGG)** — 200, 4 MB. RESULT: "PKW-Stellplatz" module, "für Menschen mit Behinderung ausgewiesenen Parkplät-ze", "Aufzug/Aufzugsanlage"; no "Behindertenparkplatz", no "rollstuhlgerecht". Read: the parking module only [SKIPPED: rest].
- **WebSearch W7** `dinmedia.de DIN EN 81-40 Treppenschrägaufzüge Plattformaufzüge mit geneigter Fahrbahn …` — PRIOR (NOT written before the search; reconstructed afterwards, an R14 defect): the product page and a free TOC. RESULT: TOC URL on din.de.
- **E22 DIN EN 81-40:2020-12 TOC** — 200. RESULT: title "Treppenschrägaufzüge und Plattformaufzüge mit geneigter Fahrbahn für Personen mit Behinderungen", Anhang C "Treppenlifts", D.2 "Stuhl-Treppenschrägaufzugs". The title says "Personen mit Behinderungen"; the prior's "eingeschränkter Mobilität" came from the search summary's English rendering and was wrong.
- **WebSearch W8** `"Fahrstuhl" barrierefrei Leichte Sprache Rathaus Stadt Aufzug` — PRIOR (NOT written before the search; reconstructed afterwards, an R14 defect): a municipal use of Fahrstuhl. RESULT: Eberswalde press release; news sites ignored.
- **E23 Eberswalde press release 89/2026** — 200. RESULT: "Fahrstuhlanlage", "Aufzug", "Fahrstuhl" for one installation in one text.
- **WebSearch W9** `Landesbauordnung "uneingeschränkt mit dem Rollstuhl nutzbar" Wohnungen Paragraph Text` — PRIOR (NOT written before the search; reconstructed afterwards, an R14 defect): a Land code. RESULT: an RLP extract on nullbarriere.de (private mirror) and NRW parliament papers.
- **E24 RLP Rundschreiben extract (§ 51 Abs. 1 LBauO)** — 200. RESULT: not the statute but the ministry's implementing circular (29.10.2015); it glosses "barrierefrei und uneingeschränkt mit dem Rollstuhl nutzbar" as "rollstuhlgerechten Wohnungen" and contrasts it with "barrierefrei nutzbar". Mirror host noted; currency after the 2015 amendment not checked.

SHAPE notes overall: direct statute URLs worked; guessed URLs (E6, E9) failed; DPO sites were reachable only through a domain-restricted search; Wheelmap blocked at the proxy level and through Wayback. No Austrian or Swiss source was fetched; ÖNORM and SN results shown by search (W7) were ignored.
