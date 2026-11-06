# Pass record: terminology pass NO/NO, session_2026-11-06-base-vocabulary-review

**Verdict.** TEK17 was retrieved twice. Lovdata returned 405, so the consolidated text came from a Wayback snapshot dated 2026-06-20. DiBK's "TEK17 med veiledning" was retrieved directly on 2026-11-06. The accessibility provisions were read in full in Norwegian: § 1-3, ch. 8, ch. 12, §§ 13-6, 13-7 and 15-9 to 15-12, with their guidance. The rest of TEK17 was searched by script and not read. Of 75 register concepts: 48 FOUND, 18 FOUND-PARTIAL, 9 SEARCHED-ABSENT. The reverse harvest has 87 phrases. Every quote verifies in the saved text and in the raw persisted bytes. **Currency is open:** the Lovdata page says TEK17 "Endres ved forskrift 12 juni 2026 nr. 1085 (i kraft 1 juli 2026)", and that amendment could not be obtained. DiBK's live regulation text matches the June snapshot line for line, which suggests ch. 8 and ch. 12 were not changed. It does not prove it. Nothing was written to the database.

## Written standard (E7)
Both texts are in **Bokmål**. This is our judgment from the forms; neither page labels its standard. The only Nynorsk seen is the cited title of lov 16. juni 1994 nr. 20 in the Hjemmel line. No Nynorsk edition of TEK17 or of the guidance was found, on one search (W2). So under E7 no Bokmål/Nynorsk split is warranted for this instrument. Every row carries `no (Bokmål)`.

## Retrieved and read
- Lovdata TEK17, artefact `ea23447c30729bf4.html`. Read: § 1-3 and the § 10-3 (3) and § 13-15 (2) passages that searches hit. Ch. 8 and ch. 12 were read through the DiBK pages instead: the 245 numbered regulation lines there match this text, and the 8 misses are 3 zero-width-space artefacts and 5 § 13-7 guidance items. [SKIPPED: chapters 2-7, 9-11, 14, 16-18 and the other § 13 sections; searched by script only.]
- DiBK pages (list and sha256 in `tools/dibk_artefacts.tsv`, plus the ch. 12 introduction `cc6cab12262007f3.html`). Read in full: the regulation text, veiledning, preaksepterte ytelser and spørsmål og svar on each page. [SKIPPED: every figure (images); the DiBK § 1-3 page; §§ 15-5 and 15-6, fetched by a wrong guess and never read.]
- The amendment FOR-2025-08-15-1662 was read in full and touches energy only. FOR-2026-06-12-1085 is NOT-OBTAINABLE: Lovdata blocked, regjeringen.no behind a Cloudflare 403, no Wayback snapshot.
- Not attempted: NS 11001-1/-2:2018, NS 8175:2012 and NS 3041:2007 (sold by Standard Norge), SINTEF Byggforskserien (subscription), and Statens vegvesen V129 (not tried). Not read: likestillings- og diskrimineringsloven and arbeidsplassforskriften.

## Counts (re-run, do not trust; run from the repository root, with `D=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/NO-NO`)
- Rebuild and verify: `python3 -I $D/build.py` exits 1 on any unverified quote. At writing: 105 observations, 87 reverse-harvest rows, 0 failures.
- Status counts: `cut -f3 $D/coverage.tsv | sort | uniq -c`. At writing: 48 / 18 / 9.
- Distinct phrases observed: `awk -F'\t' 'NR>1{print $2}' $D/observations.tsv | sort -u | wc -l`. At writing: 97.
- Regulation quotes from DiBK also present in the Lovdata snapshot: `awk -F'\t' 'NR>1 && $9!=""{print $9}' $D/observations.tsv | sort | uniq -c`. At writing: 64 yes, 0 NO.
- Raw-byte check: the FR command, with `x[5]`, on `observations.tsv` and on `reverse-harvest.tsv`. At writing: 0 missing in each.
- Held 'no' aliases occurring as substrings of the saved texts: `select distinct alias from term_aliases where lower(language)='no'`, tested as in FR. At writing: 26 of 132. Several of those hits are in another sense or in a cited standard's title. Examples: "tilgjengelig heis" occurs only inside "tilgjengelig heisstol", and "dørbredde" only in a paraphrase of EN 81-70.

## Where Norwegian carves the field differently (instrument-derived; glosses ours)
1. **Two tactile fields, not one indicator.** A "farefelt" (hazard) goes before the top step. An "oppmerksomhetsfelt" (attention) goes at the bottom step and before main entrance doors. They must not be confused by touch ("ikke forveksles med et farefelt"). The register's single "tactile attention indicators (truncated domes)" merges them, and domes are never named.
2. **Contrast is a luminance-contrast number, not LRV.** "luminanskontrast" is defined from luminance, after NS 11001-1, and set at two tiers (0,4 for objects and surfaces, 0,8 for text, nosings, handrails and hazard fields). "synlig kontrast" in a regulation is read through that number. Parameter 8 ("LRV contrast") names a different quantity.
3. **"trinnfri" is a defined term with a tolerance** (§ 1-3 m). Level threshold, step-free entrance, walkway and route are all instances of that one attribute, not separate concepts.
4. **Routes split by inside and outside.** "gangatkomst" (exterior, defined in § 1-3) and "kommunikasjonsvei" (interior: corridor, access balcony and stairwell, but not the approach and not inside a dwelling) are separate legal objects. "svalgang" shares the corridor rule. The register's single "accessible path of travel" covers both.
5. **Landing intervals are set by height gained** ("for hver 1,0 m høydeforskjell"), not by run length. Run length appears only as the condition for a steeper gradient ("strekninger under 3,0 m"). Ramp ("rampe"), walkway ("gangatkomst") and stair landings ("repos") are three words with different purposes; a repos is there "to stop falls".
6. **Three quality tiers, not one.** General requirements, then "tilgjengelig" (housing, with a design basis of a manual wheelchair user with "full førlighet i overkroppen"), then "universell utforming" (public and work buildings), keyed to "hovedløsning". Most provisions are written three times, once per tier.
7. **The drafting is functional requirement plus pre-accepted performance.** The regulation states a "funksjonskrav". The directorate's "preakseptert ytelse" gives deemed-to-satisfy values, and many values in this field (contrast numbers, illuminance, outlet placement) live only there. The register has no "regulation vs deemed-to-satisfy" axis.
8. **Function words replace device words.** Shower is a "dusjsone" that must work without an enclosure. Seating is regulated as "plass for rullestol der det anlegges sitteplasser". Planters and vegetation appear as fall barriers. A grating ("skraperist") appears as an attention field.
9. **Acoustics and colour temperature are delegated or absent.** There is no reverberation-time term: § 13-6 points to "lydklasse C" in NS 8175. There is no colour temperature: § 13-7 regulates the daylight factor only.
10. **Population carve** (§ 12-1 veiledning): reduced strength and movement, sight, hearing, "nedsatt kognitivitet (forståelsestap)" and allergies. People who cannot speak and people "ømfintlige for inneklimafaktorer" are in the design basis.

## Defects found in the METHOD
- **M1. Priors are transcribed, not time-stamped.** The search log was written after the run. The brief's "prior before result" is a discipline nothing records.
- **M2. Currency cannot be closed when the law portal blocks.** Lovdata blocks both the page and the open API (405). The Wayback snapshot is dated, and a later amendment is announced on the page itself. The DiBK cross-check is a proxy, not a verification.
- **M3. Register size differs from the pilots.** This pass adds the 15 "RHFAC-does-not-name" B651 headings, as the brief asks, giving 75 rows; FR/DE/JA used 60. Cross-pair totals are not comparable without filtering on `register_source`.
- **M4. The FOUND-PARTIAL labels are hand judgments** (`PARTIAL` in build.py), as in FR. The near-duplicate surface and illumination criteria (FR D1) again share observations and inflate FOUND.
- **M5. Substring alias testing over-attests** (FR D3 reproduced): it counted 26 hits, some of them only in a cited standard's title.
- **M6. Tooling:** `tools/h2t.py --trim` is ad hoc and keyed to DiBK page markers. `retrieval_log.fetch` cannot send a browser User-Agent, which may be what Lovdata's IPS blocks; this was not tested.

## Self-attack: the five likeliest ways this record is wrong
1. **Currency.** The 1 July 2026 amendment may have changed ch. 8 or ch. 12. DiBK's page could lag the law, so the line-for-line match does not exclude a change.
2. **Bokmål judgment.** No page states its written standard. Calling the texts Bokmål is our reading of their forms. One search does not prove there is no Nynorsk edition.
3. **Sense matching is mine.** Some mappings may be wider or narrower than marked. Examples: "skjerming mot vær og klima" to Shelter, "garderobene" to lockers, "horisontalt felt" to level landings, "tilstrekkelig kapasitet" to RHFAC's capacity.
4. **Guidance vs regulation.** DiBK pages interleave both. A locator marked "(forskrift)" was checked against Lovdata, but a guidance locator could be misattributed to a ledd.
5. **Scope.** SEARCHED-ABSENT means absent from TEK17 and the guidance pages read. Some concepts may sit in NS 11001, V129 or ch. 13 sections not read: speed bumps, spouts, door timing, colour temperature, rest seating.
