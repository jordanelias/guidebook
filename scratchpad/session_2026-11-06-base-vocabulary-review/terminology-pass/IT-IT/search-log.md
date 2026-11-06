# Search log — terminology pass IT/IT (session_2026-11-06-base-vocabulary-review)

Every query or retrieval in order. "Prior" was written before the result. Shape note per R14. Empties kept. Artefacts are under `retrieval-log/session_2026-11-06-base-vocabulary-review/`; the manifest lines carry the purpose prefix "terminology pass IT-IT:".

## Instrument derivation (database and repository, read-only)
- D1 `select * from research_code_leads where jurisdiction like '%IT%'`. Prior: 0 rows (the caller said Italy has no leads). Result: 0 rows. The table's distinct jurisdictions are AU CA CH DE ES EU FR INT ISO JP NL NO SG UG UK US. A second query on `standard_name`/`notes` for "ital", "236" and "503" also gave 0 rows. Shape: well-formed.
- D2 `select ref_id, pub_title, standard_number from evidence_sources where jurisdiction='IT'`. Prior: 0 rows. Result: 0 rows.
- D3 `grep -n -i "ital\|\bIT\b" references/standards-registry.md`. Prior: one DM 236 entry. Result: two IT entries: "DM 236/89" (source_url GU PDF `gazzettaufficiale.it/eli/gu/1989/06/23/145/so/47/sg/pdf`, "under review") and "UNI 11532-2:2020" (acoustics, paid). DPR 503/1996 and L. 13/1989 are not in the registry.
- D4 `select alias, alias_type, jurisdiction, notes from term_aliases where lower(language)='it'`. Result: the held aliases, all TRANSLATION/SYNONYM/BROADER/DOMAIN, most noted "model-generated 2026-07-25". They are treated as seeds.
- **How the list was built:** D3 supplied DM 236. The caller named the three candidates (the DM, the presidential decree on public buildings, and the law). The DM's own preamble ("Visto l'art. 1 della legge 9 gennaio 1989, n. 13") and DPR 503 art. 1 comma 6 confirmed the pairing and the split between private and public scope. DPR 380/2001 arts 77-82 came from DPR 503 being cited in DPR 380 art. 78 and from my own knowledge that L. 13/1989 was carried into the Testo unico. That is model knowledge, verified only by the retrieved text of arts 77 and 82, which cite L. 13 art. 1 and DPR 503 by name. Nothing was derivable from the base apart from DM 236.

## Retrievals (all via `retrieval_log.fetch`, run from the repository root)
- R1 `https://www.normattiva.it/uri-res/N2Ls?urn:nir:ministero.lavori.pubblici:decreto:1989-06-14;236`. Prior: 200 with the whole act or its first article. Result: 200, 89000 bytes, `8389d1d659da538e.html`. It holds art. 1 only, plus the act index; the index shows arts 1-12 and Allegato A. Shape: a correct ELI/URN form.
- R2 GU PDF from the registry (`.../so/47/sg/pdf`). Prior: a scanned PDF without text. Result: 200, 3883923 bytes, `cb49c9007b74465f.pdf`, 79 pages; `pdftotext` returns no text. Not OCR'd.
- R3 `https://www.normattiva.it/esporta/attoCompleto?atto.dataPubblicazioneGazzetta=1989-06-23&atto.codiceRedazionale=089G0298`, a link taken from R1. Prior: the whole act. Result: 200 but the page says "Errore nel caricamento delle informazioni" (`1e60f6405a5d0de0.html`). The link needs a session cookie, which `fetch()` does not keep.
- R4 `https://www.normattiva.it/do/atto/caricaAKN?dataGU=19890623&codiceRedaz=089G0298&dataVigenza=20261106`, the Akoma Ntoso export taken from R1. Prior: XML. Result: the same error page (`c9d6ff593606445b.html`). Same cause as R3.
- R5 `.../atto/caricaArticolo?...idArticolo=8...`, a link taken from R1. Prior: art. 8. Result: HTTP 500, "Errore! Sessione scaduta" (`cf203db6ba6ae17a.html`).
- R6 URN with `~art8`. Prior: art. 8 without a session. Result: 200, `c5174db912c656ef.html`. Art. 8 is text apart from 6 "Parte di provvedimento in formato grafico" links (`/cgi-bin/db2www/arti/arti.mac/report4?cdimg=089G0298000801` and following), which were not fetched. **Shape lesson:** the per-article URN `~artN` works where every session-bound link fails.
- R7 URN `~art1` … `~art12` (excluding 8). Result: all 200. The first `~art1` response was empty (0 bytes, no status) and a retry returned R1's bytes. Artefacts: 1eb7803e30a719e5 (2), f998067e0b9502d2 (3), d4c287be39e505af (4), 559bbda34dd994c4 (5), f746723b9ab1ef8f (6), 62d133bb180ba6d0 (7), 10903672f4ef0b70 (9), 841a7df49ce08a21 (10), 34e74cadad837463 (11), 4a3e28f19eb45ac1 (12).
- R8 `...urn:nir:presidente.repubblica:decreto:1996-07-24;503`. Prior: 200, art. 1 page. Result: 200, `5d768f53eed9adaa.html`; the index shows arts 1-32 and Allegati A, B, C.
- R9 `...urn:nir:stato:legge:1989-01-09;13`. Prior: 200, art. 1. Result: 200, `47cc14cd99f79e38.html`, art. 1 only. Other articles were not fetched.
- R10 DPR 503 `~art2` … `~art32`. Result: 24 returned 200 at the first attempt and 7 (arts 4, 5, 9, 11, 13, 14, 32) came back empty. Retried once and all 200. The art. 32 page (`6ce5a1b63a1225c1.html`, 160 KB) carries an "Appendice" that reprints DM 236.
- R11 DPR 380/2001 `~art77` … `~art82`. Result: all 200 (art. 79 after one empty first response).
- W1 WebSearch (standard) `nuovo decreto barriere architettoniche sostituisce DM 236/1989 2025 2026`. Prior: no adopted replacement, possibly a pending bill. Result: 18 links. They include a Senate dossier on a bill proposing a new regulation that would repeal DPR 503 and DM 236, and 2026 tax-bonus pages still citing DM 236. No adopted replacement appears. The search summaries are not sources, and nothing is taken from them beyond "currency UNVERIFIED". Shape: an Italian query on a US-only engine, so thin.

## Text extraction
`tools/nt2txt.py` (html.parser) extracts each article page. A first regex tag-strip silently ate everything after each `---->  Parte … <----` marker, because the `<----` opens a pseudo-tag. That is why art. 8 first appeared to end at 8.0.2. Fixed before any reading. A second fix stops the extraction at "articolo successivo" when there is no "articolo precedente" (the first article of an act).

## Absence and sense checks (case-insensitive, whitespace-collapsed; counts are DM 236 arts 1-12 / DPR 503 arts 1-31)
Prior for each: absent or only in another sense.
- `drenag` 0/1 and `acque` 0/1. Both hits are in the Codice della strada "Cunetta" definition quoted in a note to DPR 503 art. 11. Not in the accessibility sense.
- `riverber` 0/0; `acustic` 3/2 ("percezioni acustiche", the "acustica" kerb percussion, the telephone "isolato sotto il profilo acustico"); `lux` 0/0; `illuminamento` 0/0; `temperatura` 0/0.
- `armadiet` 0/0; `microonde` 0/0; `forno` 0/0; `casse` 3/0 (all "cassette per la posta").
- `forza` 0/1 (DPR 503 note, "forza di legge"). Force is "pressione … kg".
- `tattil` 0/0, `podotattil` 0/0, `loges` 0/0; `rugosit` 0/1 (DPR 503 art. 6: road-surface texture to slow drivers, not a pedestrian indicator).
- `pensilin` 0/0; `copertura` 1/1 (DM 8.2.3 parking roof; DPR 503 art. 25 "criteri di copertura dei maggiori oneri", a financial sense).
- `contrasto` 1/0 (in the notes to DM art. 1, "in contrasto con le norme", a legal sense); `luminanz` 0/0; `cromatic` 2/0; `colore` 2/0.
- `spazio di manovra` 0/0 (the text has "spazi di manovra"); `raggio` 0/0; `rotazione` 2/0; `circonferenza` 1/0.
- `volume` 0/2 (traffic volume; building volume).
- **Second-witness comparison (APP vs DM, punto 4.1.9).** The Normattiva DM page reads "I corridoi devono presentare variazioni di livello"; the DPR 503 Appendice reads "I corridoi non devono presentare variazioni di livello". The DM page's reading contradicts its own next clause ("in caso contrario queste devono essere superate mediante rampe"), so the Appendice's "non" is very probably the correct text. Not checked against the GU scan (no OCR).

## Held aliases against the texts
121 distinct held `it` aliases were each tested as a lower-cased substring of the whitespace-collapsed text of all saved files. 7 occur: adattabilità, affaticamento, corridoio, larghezza del corridoio, luce netta, maniglione, visitabilità. The parameter-level TRANSLATION aliases "pendenza della rampa", "larghezza della porta", "spazio di manovra", "raggio di rotazione", "forza di azionamento", "tempo di riverbero", "contrasto di luminanza", "temperatura colore" and "soglia a filo" occur 0 times. "affaticamento" occurs in DM 4.1.11, in the ramp-fatigue sense.
