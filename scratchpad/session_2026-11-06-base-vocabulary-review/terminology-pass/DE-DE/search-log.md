# Search log — terminology pass DE/DE (session_2026-11-06-base-vocabulary-review)

Each entry: query verbatim, PRIOR (written before the result), RESULT, SHAPE (R14). Empties kept.

## Q1 — local derivation (DB, read-only)
- Query: `select ref_id, pub_title, standard_number from evidence_sources where jurisdiction='DE'`; `select * from research_code_leads where jurisdiction like '%DE%'`; grep of `references/standards-registry.md` for DE.
- PRIOR: a handful of DIN 18040 leads; perhaps one held German source; no ASR or Bauordnung.
- RESULT: 1 held source (REF-00988, a DGUV Information 215-112 excerpt on ramps); 15 leads, all DIN (18040-1/-2, 18041, 32975, 32984, 32986, 51130, EN 81-41, EN 81-70, DVGW W 551), all REFERENCE-ONLY; registry lists DIN 18040-1/-2/-3 with revision drafts. No ASR V3a.2, no MBO/MVV TB, no BGG in any home.
- SHAPE: well-formed exact-match queries. Absence of ASR/MBO in the leads is a defect of the lead set (DIN-only), not evidence the instruments are minor.

## Q2 — web search
- Query: `ASR V3a.2 Barrierefreie Gestaltung von Arbeitsstätten BAuA PDF`
- PRIOR: baua.de hosts the ASR V3a.2 as a free PDF; the edition is 2012 with later amendments (I expect a 2021/2022 amendment, unconfirmed).
- RESULT: no baua.de link in results. Results report a current amendment of May 2025 (GMBl 2025 S. 365, in force 23 May 2025, concerning Anhang A1.5 floors) — a search-engine summary, not verified until a text in hand states it. Copies at forum-verlag (consolidated "Stand Mai 2025"), ruhr-uni-bochum (unofficial, marked), dguv.de (2014), bgn, umwelt-online.
- SHAPE: well-formed; the official host was absent from results, so I try the BAuA URL pattern directly (Q3).

## Q3 — direct fetch of BAuA PDF
- Query: `https://www.baua.de/DE/Angebote/Regelwerk/ASR/pdf/ASR-V3a-2.pdf?__blob=publicationFile`
- PRIOR: 50/50 — BAuA PDF paths carry this pattern, but the exact filename is my guess (a seed URL, not a citation).
- RESULT: HTTP 403, a Bunny Shield JS challenge page (artefact a7830b7eefbc91c1.html, 2182 bytes). Publisher block, not absence.
- SHAPE: URL was guessed; the block page proves the host answered for that path family, not that the file exists at it.

## Q4 — Wayback availability
- Query: `http://archive.org/wayback/available?url=www.baua.de/DE/Angebote/Regelwerk/ASR/pdf/ASR-V3a-2.pdf%3F__blob%3DpublicationFile&timestamp=20261101` (and the same without the query string). A CDX listing attempt was "Blocked by egress policy".
- PRIOR: a snapshot exists; whether it post-dates the May 2025 amendment is uncertain.
- RESULT: closest snapshot 20251223025649 (with `?__blob=publicationFile`); without the query string, 20231111044552 only. The 2025-12 snapshot should post-date May 2025, to be confirmed from the text's own "Ausgabe/Stand" line.

## Q5 — Wayback if_ fetch of ASR V3a.2
- Query: `https://web.archive.org/web/20251223025649if_/https://www.baua.de/DE/Angebote/Regelwerk/ASR/pdf/ASR-V3a-2.pdf?__blob=publicationFile`
- PRIOR: succeeds (Wayback if_ cleared a Bunny Shield block in batch 21).
- RESULT: HTTP 200, application/pdf, 1,113,546 bytes, sha256 efd0b353…; PDF metadata title "ASR V3a.2 Barrierefreie Gestaltung von Arbeitsstätten", created 2025-05-13. Text header: "Ausgabe: August 2012 / zuletzt geändert GMBL 2025, S. 365 (v. 23.05.2025)" — consistent with Q2's summary, now verified from the text.
- SHAPE: the BAuA filename guessed in Q3 turned out to be the real one (the Wayback index holds it); the guess is recorded as a guess.

## Q6 — web search
- Query: `Musterbauordnung MBO § 50 Barrierefreies Bauen PDF bauministerkonferenz`
- PRIOR: MBO (latest amendment 2023 or 2024) free on is-argebau.de / bauministerkonferenz.de; § 50 is the accessibility section; § 2 has no definition of "barrierefrei" (it defers to the wording in § 50 itself).
- RESULT: no official MBO host in results; secondary copies (DGUV excerpt kapitel2-3-1.pdf; Land codes on a shopify CDN — not used); a Saxon VV TB 2024 copy on nullbarriere.de; a summary that Berlin's equivalent is § 51.
- SHAPE: well-formed; the official host is not indexed by this engine for this query. Decision: the MBO is a model, not law in force; go to a Land code in force (Bavaria chosen: official HTML host gesetze-bayern.de) and to the federal BGG (gesetze-im-internet.de).

## Q7 — direct fetches (Land code, federal statute)
- Query: `https://www.gesetze-bayern.de/Content/Document/BayBO-48`; `https://www.gesetze-im-internet.de/bgg/__4.html`
- PRIOR: BayBO Art. 48 "Barrierefreies Bauen" is retrievable as HTML; BGG § 4 "Barrierefreiheit" is a short definition. Both likely 200.
- RESULT: both 200. BayBO page states "Text gilt ab: 01.05.2026", "Fassung: 14.08.2007" (artefact 61c9cb0a70b48be3.html). BGG § 4 (artefact dcd3deee983e5503.html, iso-8859-1). Read both in full: Art. 48 is a scoping article (which buildings, which rooms) and names no design quantity; BGG § 4 is the definition the ASR 3.2 cites.
- SHAPE: well-formed.

## Q8 — web search (Bavarian technical building rules, DIN 18040 adoption)
- Query: `Bayerische Technische Baubestimmungen BayTB DIN 18040 Anlage A 4.2 PDF`
- PRIOR: the BayTB (an Bekanntmachung of the StMB) lists DIN 18040-1 and -2 under A 4.2 with an Anlage that excludes or modifies clauses (I expect the wheelchair "R" requirements of 18040-2 to be partly excluded). Free PDF on stmb.bayern.de or verkuendung-bayern.de.
- RESULT: official gazette PDF located: verkuendung-bayern.de/files/baymbl/2025/87/anhang/Anlage.pdf ("BayTB Ausgabe Februar 2025", per the search summary — unverified until read). A mirror (nullbarriere.de) and an StMB explanatory PDF on applying DIN 18040-1/-2 also surfaced. Whether a later BayTB edition superseded Feb 2025 before 2026-11-06 is NOT established by this query.
- SHAPE: well-formed; currency check deferred to the text itself plus Q10.

## Q9 — direct fetch of BayTB Feb 2025 (official gazette)
- Query: `https://www.verkuendung-bayern.de/files/baymbl/2025/87/anhang/Anlage.pdf`
- PRIOR: 200, a long PDF (hundreds of pages); A 4.2 with Anlagen A 4.2/2Bay and A 4.2/3Bay containing modifications to DIN 18040 clauses, which will quote DIN clause headings — so this is the only free route to some DIN 18040 phrasing.
- RESULT: 200, application/pdf, 8,677,899 bytes, 351 pages, sha256 9b838dcd…; title "Anlage: Bayerische Technische Baubestimmungen (BayTB) – Ausgabe Februar 2025". A 4.2 (text lines 3466–3612 of the extraction) holds DIN 18065, DIN 18040-1:2010-10 (Anlage A 4.2/2Bay) and DIN 18040-2:2011-09 (Anlage A 4.2/3Bay). PRIOR on "R" exclusion confirmed in the text ("alle Anforderungen mit der Kennzeichnung „R“ sind von der Einführung ausgenommen"). The Anlagen name DIN clause numbers and a few DIN terms (Greifhöhe, Achsmaß, Bewegungsflächen, Duschplatz) but do NOT reproduce DIN clause headings — the prior that they would was wrong.
- SHAPE: well-formed.

## Q10 — currency of BayTB
- Query: `BayTB Ausgabe 2026 Bayerische Technische Baubestimmungen Bekanntmachung`
- PRIOR: unsure; BayTB editions appeared 2022-06, 2024-12 (per Q8 summary of the dinmedia listing) and 2025-02; a 2026 edition is possible.
- RESULT: no 2026 BayTB edition found; results list only the June 2022 edition and unrelated 2026 gazette items. The engine's summary did not even surface the Feb 2025 edition already in hand, so the query is weak evidence either way.
- SHAPE: weak — a search engine is the wrong tool for gazette currency; the right check is the BayMBl index on verkuendung-bayern.de, not done here. Status: Feb 2025 is the newest edition OBSERVED; that it is in force on 2026-11-06 is [UNVERIFIED].

## Q11 — DIN 18040-1 full text (paywall check)
- Query: web search `DIN 18040-1:2010-10 dinmedia Barrierefreies Bauen Öffentlich zugängliche Gebäude` then fetch the product page found.
- PRIOR: DIN Media sells it; no free full text; a product page with a short abstract only.
- RESULT: dinmedia.de product page 200 (artefact 5a933d138d378242.html): "[AKTUELL]", 30 pages, "ab 105,20 EUR inkl. MwSt.", "Dieses Dokument wurde teilweise ersetzt durch DIN EN 17210:2021-08". The body is NOT-OBTAINABLE (paid). The search also surfaced a free din.de table-of-contents download, fetched: 200, 1-page PDF (artefact a301a6bf293f64ad.pdf) carrying DIN 18040-1's clause headings. Headings are the standard's own phrases and are recorded as observations of HEADINGS only; nothing about the clause content is inferred.
- SHAPE: well-formed. Not substituted from memory. The search summary's claim that the 2023 draft "aligns Sections 4 and 5 with DIN EN 17210" is a summary, not read.

## Q12 — DIN 18040-2 TOC
- Query: web search `DIN 18040-2:2011-09 Wohnungen Inhaltsverzeichnis din.de toc download`
- PRIOR: din.de offers the same TOC download for part 2 under its own document id.
