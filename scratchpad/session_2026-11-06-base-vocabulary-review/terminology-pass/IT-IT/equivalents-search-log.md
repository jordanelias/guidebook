# Equivalents search log — IT-IT, session_2026-11-06-base-vocabulary-review

Every fetch goes through `tools/efetch.py`, which appends the prior line to this file BEFORE `retrieval_log.fetch()` runs; the result line is appended after. Queries against local texts (tier 1, second reading) are logged with the grep pattern verbatim.

## Tier 1: second reading of the first-pass texts (local `text/`, Normattiva article pages)
- Query (grep -o -i -E, all `text/*.txt`): `\b(parcheggi[a-z]*|posti auto|posto auto|stall[oi]|posteggi[a-z]*|autorimess[ae]|contrassegn[a-z]*|ascensor[ei]|elevator[ei]|piattaform[ae][a-z ]*|servoscal[ae]|montascal[ae]|impiant[oi] di sollevamento|apparecchiature elevatrici|sollevamento|accessibil[a-zà]*|visitabil[a-zà]*|adattabil[a-zà]*|barrier[ae] architettonic[ah]e|senza barriere|disabil[a-zà]*|handicap[a-z]*|invalid[ia]|portatori di handicap|ridotta o impedita capacit[aà']+ motoria)`
  - Prior: parking as "posti auto" / "parcheggi" with "riservati"; lift as "ascensore"; "servoscala" and "piattaforma elevatrice" as platform devices; qualifier "accessibile"; "montascale" absent (a trade word); "handicap" in older notes.
  - Result: ascensore 31 + ascensori 16; servoscala 48; piattaforma elevatrice 6 + piattaforme elevatrici 5; elevatore 1 (DPR 503 art. 28); montascale 0; posti auto 12, posto auto 3, parcheggi 10, parcheggio 5, stalli 1 (Codice della strada note in DPR 503 art. 11), autorimesse 8; contrassegno 7; disabili 13, invalidi 13, handicappate 5, portatori di handicap 1; senza barriere 2. Counts are hits across overlapping witnesses (DM pages plus the DPR 503 Appendice), not distinct occurrences.
  - Shape: one wide alternation, case-folded; a count of strings, not senses. Senses were judged by reading each context (below, in equivalents.tsv).
- Query: `\b(fruib[a-zà]*|utilizzab[a-zà]*|agevolmente [a-z]+|privi di barriere|priva di barriere|eliminazione delle barriere|superamento delle barriere|rampe mobili|collegament[oi] vertical[ei]|mezzi di sollevamento|apparecchi di risalita|tappeti mobili|scale mobili)`
  - Prior: "fruibile/fruibilità" as a second umbrella; generic vertical-transport class words.
  - Result: eliminazione delle barriere 23; fruibilità 7; mezzi di sollevamento 6; agevolmente fruibile 4; utilizzabilità 4; collegamenti verticali 2; apparecchi di risalita 2; rampe mobili 1; privi di barriere 1; scale mobili 0; tappeti mobili 0.
  - Shape: as above.

### FETCH https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:1992-04-30;285~art188
- what: tier 2: Nuovo codice della strada art. 188 (sosta persone invalide)
- prior (written before fetch): Codice della strada art. 188 on Normattiva: 'veicoli al servizio delle persone invalide', 'contrassegno', 'strutture'/'spazi riservati'; old 'invalidi' wording kept.

### FETCH https://www.normattiva.it/uri-res/N2Ls?urn:nir:presidente.repubblica:decreto:1992-12-16;495~art381
- what: tier 2/3: Regolamento CdS art. 381 (contrassegno, segnaletica)
- prior (written before fetch): DPR 495/1992 art. 381 (regolamento CdS): 'contrassegno speciale', 'strutture e segnaletica per la mobilità delle persone invalide', figura V.4, spazi di sosta riservati; post-2012 'contrassegno di parcheggio per disabili'.

### FETCH https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2024-05-03;62~art4
- what: tier 2: D.Lgs. 62/2024 art. 4 terminology
- prior (written before fetch): D.Lgs. 62/2024 art. 4: mandates replacing 'handicap', 'persona handicappata', 'portatore di handicap', 'disabile' with 'persona con disabilità' (disfavoured-form attestation).

### FETCH https://www.normattiva.it/uri-res/N2Ls?urn:nir:presidente.repubblica:decreto:1992-12-16;495~art120
- what: tier 3: Regolamento CdS art. 120 (fig. II 79/a)
- prior (written before fetch): DPR 495/1992 art. 120 (segnali di indicazione / pannelli integrativi): fig. II.79/a as a panel showing the disabled-access symbol on parking signs; wording 'invalidi'.

### FETCH https://www.normattiva.it/uri-res/N2Ls?urn:nir:presidente.repubblica:decreto:1992-12-16;495~art149
- what: tier 3: Regolamento CdS art. 149 (stalli di sosta)
- prior (written before fetch): DPR 495/1992 art. 149 (segnaletica orizzontale, stalli di sosta): yellow lines for 'stalli riservati' to 'veicoli al servizio di persone invalide'.

### FETCH https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2024-05-03;62~art2
- what: tier 2: D.Lgs. 62/2024 art. 2 definitions
- prior (written before fetch): D.Lgs. 62/2024 art. 2 definitions: 'accomodamento ragionevole', perhaps 'progettazione universale'; 'persona con disabilità'.

### FETCH https://www.normattiva.it/uri-res/N2Ls?urn:nir:presidente.repubblica:decreto:1999-04-30;162~art2
- what: tier 2: DPR 162/1999 art. 2 (ascensore definition)
- prior (written before fetch): DPR 162/1999 art. 2 (ascensori regulation) defines 'ascensore' as an apparatus serving defined levels with a cabin on guides; may mention 'montacarichi'.
- Results so far: CdS art. 188 200, 1.55 MB, vigente 14-12-2024 (text 0c0c87f3c395fb56.txt); DPR 495 art. 381 200 (d7a12939ad74bc2c.txt); D.Lgs. 62/2024 art. 4 200 (2f3ef11b600382ec.txt); DPR 495 art. 120 200 (4230c0efcf3b45fc.txt); DPR 495 art. 149 exit 35 (TLS, no response; retried below); D.Lgs. 62/2024 art. 2 exit 35 (retried below); DPR 162/1999 art. 2 200 (98462a6237c09a30.txt).

### FETCH https://www.normattiva.it/uri-res/N2Ls?urn:nir:presidente.repubblica:decreto:1992-12-16;495~art149
- what: tier 3: Regolamento CdS art. 149 retry
- prior (written before fetch): retry after exit 35; same prior: yellow lines for stalli riservati.

### FETCH https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:2024-05-03;62~art2
- what: tier 2: D.Lgs. 62/2024 art. 2 retry
- prior (written before fetch): retry after exit 35; same prior: definitions incl. accomodamento ragionevole, progettazione universale.
- Retry results: DPR 495 art. 149 200 (dd4fa8309d171cfc.txt); D.Lgs. 62/2024 art. 2 200 (e4359fb9079ce4be.txt). Art. 2 defines «condizione di disabilità» and the art. 3 replacement of L. 104/1992; it does not carry "accomodamento ragionevole" or "progettazione universale" in its own text (grep 0). Art. 120 carries "SOSTA CONSENTITA A PARTICOLARE CATEGORIA (figg. II.79/a, II.79/b)" "esclusivamente per i veicoli degli invalidi". Art. 149 c. 5 carries "stalli di sosta riservati alle persone invalide". DPR 162/1999 art. 2 a) defines "ascensore" as "un apparecchio di sollevamento che collega piani definiti".

## Tier 4 and 5 discovery (WebSearch, US-only engine; result lists are leads, not attestation)

### FETCH https://www.normattiva.it/uri-res/N2Ls?urn:nir:presidente.repubblica:decreto:1999-04-30;162~art1
- what: tier 2: DPR 162/1999 art. 1 scope
- prior (written before fetch): DPR 162/1999 art. 1 scope: excludes lifting appliances with speed not over 0.15 m/s (the platform lifts), naming them.
- DPR 162/1999 art. 1: 200 (5df038af6226fc46.txt); c. 3 a) excludes "gli apparecchi di sollevamento la cui velocità di spostamento non supera 0,15 m/s" (prior met).
- WebSearch `comune contrassegno di parcheggio per disabili CUDE stalli riservati richiesta` (standard). Prior: municipal pages using "CUDE", "stalli riservati", "posto personalizzato". Result: 16 links; municipal leads comune.alghero.ss.it (regolamento stalli), comune.modena.it; rest are commercial portals (disabili.com, dequo.it, lentepubblica.it) and are not used as attestation (news/portal tier excluded). Shape: Italian keyword bag; US-only engine.
- WebSearch `FISH FIABA guida linguaggio "persona con disabilità" "diversamente abile" barriere architettoniche` (standard). Prior: a FISH or FIABA terminology guide. Result: EMPTY for the target; only disabili.com reports. Shape: too many quoted phrases.
- WebSearch `servoscala montascale piattaforma elevatrice differenza contributo barriere architettoniche comune` (standard). Prior: "montascale" as the colloquial/product word for servoscala. Result: commercial portals only (disabili.com, edilizia.com, idealista) and a court ruling PDF (osservatoriodisabilitahumanhall.unimi.it); no municipal or DPO page. Commercial pages not used as attestation.

### FETCH https://comune.alghero.ss.it/.galleries/doc-documenti/Regolamento-stalli-sosta-riservati-persone-disabilita.pdf
- what: tier 4: Comune di Alghero regolamento stalli sosta riservati
- prior (written before fetch): Municipal regulation: 'stalli di sosta riservati', 'stallo personalizzato', 'contrassegno', 'persone con disabilità'; may still say 'invalidi'.
- Comune di Alghero regolamento: 200, PDF 8 pages (b881363b31d5afc4.txt). Prior met: "stalli di sosta riservati", "stalli generici" vs "stalli personalizzati", CUDE; prior "invalidi" only in quoted law ("particolari condizioni di invalidità", art. 5 c. 2 c).
- WebSearch `superando.it "progettazione universale" "accessibilità" barriere architettoniche parole` (standard). Prior: superando.it (disability-movement news site) pages. Result: no superando.it page; public-body leads: Regione FVG linee guida (cbc-fe-collaudo.regione.fvg.it), Archivio di Stato di Asti PEBA "Universal Design", Comune di Piacenza PEBA; DPO lead: ENS "L'accessibilità migliora la vita" (vecchiosito.ens.it). University lecture PDFs not used (not in the tier list).
- WebSearch `CRIBA Emilia-Romagna scheda servoscala piattaforma elevatrice ascensore accessibile` (standard). Prior: a CRIBA (regional information centre) sheet. Result: EMPTY for CRIBA; product catalogues (infobuild, siva portal product sheets) and a Garda Trentino "marchio Open" disciplinare. Not fetched.

### FETCH https://cbc-fe-collaudo.regione.fvg.it/wp-content/uploads/2023/01/1311244354128_plugin-LINEE_GUIDA_PER_IL_SUPERAMENTO_DELLE_BARRIERE_ARCHITETTONICHE.pdf
- what: tier 4: Regione FVG linee guida superamento barriere architettoniche
- prior (written before fetch): Regional guidance: 'ascensore', 'servoscala', 'piattaforma elevatrice', maybe 'montascale'; qualifier 'accessibile', 'fruibile', 'inclusivo', 'Design for All'; parking 'posti auto riservati'.

### FETCH https://vecchiosito.ens.it/attachments/article/2833/L'accessibilità migliora la vita.pdf
- what: tier 5: ENS L'accessibilità migliora la vita
- prior (written before fetch): DPO (Ente Nazionale Sordi) guide: 'accessibilità' extended to communication; 'persone sorde'; rejects 'sordomuto'; maybe 'barriere della comunicazione'.

### FETCH https://archiviodistatoasti.cultura.gov.it/fileadmin/risorse/ASAT_DOWNLOADS/exa026_PEBA_AS_Asti_PDF/exa026_A03_Universal_Design.pdf
- what: tier 4: Archivio di Stato di Asti PEBA Universal Design
- prior (written before fetch): Public-body PEBA document on 'Universal Design' / 'progettazione universale' / 'Design for All' / 'progettazione inclusiva'.

### FETCH https://vecchiosito.ens.it/attachments/article/2833/L%27accessibilit%C3%A0%20migliora%20la%20vita.pdf
- what: tier 5: ENS L'accessibilità migliora la vita (encoded)
- prior (written before fetch): retry with percent-encoded URL (exit 3 = malformed URL from the space and accent); same prior.

### FETCH https://archiviodistatoasti.cultura.gov.it/fileadmin/risorse/ASAT_DOWNLOADS/exa026_PEBA_AS_Asti_PDF/exa026_A03_Universal_Design.pdf
- what: tier 4: Archivio di Stato di Asti PEBA Universal Design retry
- prior (written before fetch): retry after exit 35; same prior.
- FVG-hosted PDF: 200, 460 KB (76212f3b5aa29622.txt). It is the culture-sector commission's "LINEE GUIDA PER IL SUPERAMENTO DELLE BARRIERE ARCHITETTONICHE NEI LUOGHI DI INTERESSE CULTURALE" (title page, p1), hosted by Regione FVG. Prior partly met: ascensore, servoscala, piattaforma elevatrice, "Design for all", "Universal Design", "inclusivi". Not predicted: "montascale" used for a tracked stair-climber applied under the wheelchair (p35), distinct from "servoscala" (CONFLATION against the commercial usage seen in search results); "progetto senza barriere" (Barrier-free Design) presented as stigmatising (p17).
- ENS PDF: exit 3 (unencoded URL), then exit 56 (connection reset) with encoded URL. Wayback `available?url=vecchiosito.ens.it/...` returns no snapshot. NOT OBTAINED.
- Asti PEBA PDF: exit 35 twice (TLS handshake). NOT OBTAINED.
- WebSearch `UILDM OR FISH OR ANMIC "posti auto riservati" OR "parcheggi riservati" persone con disabilità guida associazione` (standard). Prior: a DPO page naming reserved parking. Result: mainly disabili.com news (excluded); DPO lead archivio.uildm.org "dm207_mondo_uildm.pdf" (UILDM magazine DM); camera.it hearing memo (issuer unknown until read).

### FETCH https://archivio.uildm.org/sites/default/files/DM/207/dm207_mondo_uildm.pdf
- what: tier 5: UILDM DM 207 Mondo UILDM
- prior (written before fetch): UILDM (DPO) magazine pages: 'posti riservati', 'parcheggi per disabili', 'contrassegno', 'persone con disabilità'; maybe 'barriere architettoniche', 'accessibile'.

### FETCH https://documenti.camera.it/leg19/documentiAcquisiti/COM09/Audizioni/leg19.com09.Audizioni.Memoria.PUBBLICO.ideGes.24413.21-11-2023-18-27-00.013.pdf
- what: tier 5 candidate: Camera COM09 audizione memoria (CdS)
- prior (written before fetch): Hearing memo to Camera Commission IX (transport) on Codice della strada; probably FISH or a DPO; 'CUDE', 'stalli riservati', 'persone con disabilità'.
- UILDM DM 207 PDF: exit 60 (TLS certificate problem; verification not disabled). Wayback `available?url=archivio.uildm.org/...dm207_mondo_uildm.pdf` returns no snapshot. NOT OBTAINED.
- Camera memo: 200 (4b99b0c608b289dc.txt). It is the "Memoria della FISH – Federazione Italiana per il Superamento dell'Handicap – ETS", audizione informale 21 novembre 2023. Prior (CUDE, stalli riservati) NOT met: `stall` 0 in the parking sense, `CUDE` 0, `contrassegno` 0, `parchegg` 0. Qualifier found: "pienamente accessibile e fruibile" (p4). The DPO's own name keeps "Handicap" although D.Lgs. 62/2024 art. 4 replaces the word in statute.
- Wayback `available?url=fishonlus.it` returns a 2026-10-25 snapshot; not fetched (budget; the memo already gives a FISH text).

## Tier 1 re-check of quotes during the build
- `percorso accessibile` is not in DM art. 8 text (my first locator was wrong); found in DPR 503 art. 4 c. 1 (019bb2eeffedadc2.txt) and used there.
- `senza barriere architettoniche` is in DM 7.4 (62d133bb180ba6d0.txt); DPR 503 art. 19 c. 1 reads "senza dar luogo a barriere architettoniche" (3e4efb4b6dcd2063.txt). My first locator (DPR 19) was wrong; corrected.

## Not attempted (budget)
Regional laws; RFI / Trenitalia and transport-operator accessibility pages; city permit pages of Rome, Milan, Turin; UNI 11532 and EN 81-70 / EN 81-41 Italian editions (paid); Gazzetta Ufficiale figure tables II.79/a, V.4, V.5 (images); the CRPD Italian text annexed to L. 18/2009 ("progettazione universale").
