# Equivalents record — IT-IT, session_2026-11-06-base-vocabulary-review

**Verdict.** The pass covered the three owner classes and 12 register-v2 concepts, but most register concepts were not attempted. Italian names the reserved bay by the vehicle, the permit or the user, never by an umbrella adjective. Building law says "posti auto riservati" and road law says "stalli di sosta riservati". "Accessibile" qualifies the car park as a whole. The vertical-transport class has one car word (ascensore), two platform words (servoscala, piattaforma elevatrice), and several wider class words. Every quote verifies in the saved text: `python3 -I $D/tools/equiv_build.py` exits 0 (D = this folder, run from the repo root). Nothing was written to the DB and nothing was committed.

## Attempted vs not (re-run, do not trust)
- Attempted: `awk -F'\t' 'NR>1{print $1}' $D/equivalents.tsv | sort -u | wc -l` gives 12 concepts. They are R2-050 parking bay, R2-281 Parking, R2-053 access aisle, R2-333 qualifier, R2-359/360/361/363 (the IT outcome levels), R2-208 pictogram, and R2-163/168/169 (lift, platform lift, stair lift).
- Not attempted: the other 548 register-v2 rows, including the FOUND quantity and element rows of the first pass (ramp, handrail, corridor, door, toilet and so on). Candidate forms for some of these were seen but are not recorded, because no sense judgment was made: rampa inclinata, piano inclinato, scivolo, w.c., servizi igienici, maniglione.

## Forms by usage type and tier (commands; at writing, 64 rows)
- `awk -F'\t' 'NR>1{print $6}' $D/equivalents.tsv | sort | uniq -c` gives 44 code term, 10 qualifier, 5 outdated or disfavoured, 3 regional variant (used here for printed misspellings and a gender variant, not geography), 1 product name, 1 colloquial.
- `awk -F'\t' 'NR>1{print $8}' $D/equivalents.tsv | sort | uniq -c` gives tier 1: 37, tier 2: 9, tier 3: 3, tier 4: 14, tier 5: 1. There are no seeds.

## The owner classes in Italian
- **Parking.** Building codes: posti auto (riservati), posto auto riservato, posti riservati, and "lo spazio riservato alla sosta delle autovetture al servizio delle persone disabili". Road code and regulation: stalli di sosta riservati alle persone invalide, stalli ad essi riservati, and the sign name SOSTA CONSENTITA A PARTICOLARE CATEGORIA. A municipal regulation splits the class into stalli generici and stalli personalizzati, the second assigned to one permit holder. The permit is the contrassegno di parcheggio per disabili, also called contrassegno invalidi, speciale contrassegno, or CUDE.
- **Umbrella qualifier.** The forms found are accessibile (also accessibilità), fruibile, "accessibile e fruibile" (FISH), and senza barriere architettoniche. Public guidance adds Design for all, Universal Design, utenza ampliata and inclusivo/inclusivi, all wider in scope. The same guidance names "progetto senza barriere (Barrier-free Design)" and "per handicappati" as stigmatising. Accessibilità, visitabilità and adattabilità are defined grades (DM art. 2 G-I) and are recorded as outcome-level rows, not as synonyms. The DPR 503 symbol "accessibilità condizionata" names the state the DM calls visitabilità condizionata.
- **Lift.** Ascensore is the car lift, defined in DPR 162/1999 art. 2 a. Piattaforma elevatrice is the vertical platform. Servoscala is the stair lift, with five categories in DM 8.1.13 including seat-only and wheelchair-platform types. The wider class words are mezzi / apparecchi di sollevamento, apparecchi di risalita, apparecchi elevatori, mezzi di elevazione, and L. 13's "meccanismi per l'accesso ai piani superiori, ivi compresi i servoscala". Italian has no "lift" word that, like the English one, can mean either the car or the platform.

## Conflations (in `conflation_note`; count with `awk -F'\t' 'NR>1 && $12!=""' $D/equivalents.tsv | wc -l`, 20 at writing)
- **montascale.** The culture-sector guidelines (p35) use it for a mobile tracked stair-climber placed under the wheelchair, distinct from servoscala. Commercial pages treat the two words as one, but those pages are excluded as attestation, so the commercial sense is unattested here.
- **Servoscala and piattaforma elevatrice.** DM 4.1.13 gives the two devices one definition, and 8.1.13 then separates them.
- **Speed thresholds.** DPR 162 excludes devices at or below 0.15 m/s from "ascensore", while the DM caps platforms at 0.1 m/s.
- **Accessibilità.** It is both the umbrella word and the top grade.
- **Permit and bay.** They are named through each other ("posti ... degli invalidi muniti di contrassegno").
- **One sign for two groups.** The sign SOSTA CONSENTITA A PARTICOLARE CATEGORIA serves disabled people and ambulances.
- **Old and new population words.** D.Lgs. 62/2024 art. 4 replaces "disabile", "persona handicappata" and "portatore di handicap" with "persona con disabilità" wherever they occur. The consolidated DM 236, DPR 503 and DPR 495 texts still print "disabili" and "invalidi", and CdS art. 188 holds both forms.

## Could not obtain
- ENS "L'accessibilità migliora la vita": connection reset, no Wayback snapshot.
- UILDM DM 207: TLS certificate error, no snapshot.
- Archivio di Stato di Asti PEBA "Universal Design": TLS handshake failure, twice.
- No FISH or FIABA terminology guide was found by search.
- The road-sign figures (II.79/a, V.4, V.5, II.445) are images and were not read.
- No city permit page of a large city and no transport-operator page was attempted.

## Self-attack
1. Tier 5 rests on one FISH memo, which carries no parking form. The community's own names for the bay ("posto disabili" and similar) are not attested, so Co-1 usage is the largest gap.
2. Tier 1 quotes come from Normattiva transcriptions (first-pass defect M1). Each misspelling recorded (accessibità, pittaforma) may belong to the transcription, not the Gazzetta Ufficiale text.
3. "Regional variant" is stretched to cover orthographic forms. A reader filtering by region will get false hits; the scope notes say which rows are orthographic.
4. The tiers are my reading. DPR 495 arts. 120 and 149 count as tier 3 (signage) and art. 381 as tier 2, although all three come from one regulation. The culture-sector guidelines count as tier 4, although the issuing commission belongs to a ministry and the file is hosted by a region.
5. The sense judgments are mine, notably elevatore a cabina chiusa = R2-163, piattaforma elevatrice under R2-168 rather than R2-170, and spazio libero... = access aisle. Read each quote before promoting any form.
