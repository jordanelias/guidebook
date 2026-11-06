# Equivalents record — DA/DK, second pass (session_2026-11-06-base-vocabulary-review)

**Verdict.** Danish has no single umbrella qualifier. The code's domain word is "Adgangsforhold". "tilgængelig(hed)" carries access only in some places and means "open to the public" in others. Compounds take the prefix "handicap-", and the older "invalide" survives in road-sign names that are in force today. Parking is named three ways in law: by the vehicle (BR18 § 401), by the permit (BEK 99 § 14), and by the people (BEK 426 § 202). The compound "handicapparkeringsplads" is the guidance and municipal form. "Løfteplatform" is the Danish platform lift, and the elevator guidance says outright that it is not an elevator. Breadth was limited: 16 of 560 concepts were attempted, and forms were recorded for 14. No tier-5 source on naming (a DPO glossary or style guide) was obtained. Nothing was written to the database and nothing was committed.

## Concepts attempted (16)
With forms (14): R2-050 parking, R2-333 qualifier, R2-163 elevator, R2-164 elevating devices, R2-168 platform lift, R2-169 stair lift, R2-208 pictogram, R2-179 toilet room, R2-198 assistive listening, R2-059 curb ramp, R2-083 ramp, R2-089 handrails, R2-093 tactile walking surface, R2-161 level threshold. Attempted with no second form found: R2-005 clear opening width ("fri passagebredde" only), R2-022 turning areas ("frit manøvreareal" only; "vendeplads" occurs for vehicles only). Not attempted: the other 544 rows (budget).

## Counts (re-run from this folder; do not trust these figures)
- Rows: `tail -n +2 equivalents.tsv | wc -l` gave 59. Concepts: `awk -F'\t' 'NR>1{print $1}' equivalents.tsv | sort -u | wc -l` gave 14.
- By usage type: `awk -F'\t' 'NR>1{print $6}' equivalents.tsv | sort | uniq -c` gave code term 40, colloquial 7, outdated or disfavoured 5, qualifier 4, regional variant 2, unattested seed 1.
- By tier: `awk -F'\t' 'NR>1{print $8}' equivalents.tsv | sort | uniq -c` gave 1: 23, 2: 3, 3: 20, 4: 9, 5: 3, seed: 1.
- Rows with a conflation note: `awk -F'\t' 'NR>1 && $12!=""' equivalents.tsv | wc -l` gave 14.

## The owner classes in Danish
- **Parking.** handicapegnede køretøjer (BR18); parkeringsbåse mv. forbeholdt personer med parkeringskort (BEK 99); parkeringsbås og parkeringsbane for handicappede (BEK 426); Handicapparkeringspladser (vejregler); handicapparkering; handicapplads; besøgshandicappladser (KK, narrower); handikapparkeringsplads (orthographic variant); invalideparkeringsplads (marked "tidligere" by Brøndby); Handicap-parkering (God Adgang). The narrower classes are a bay reserved for one vehicle (BEK 99 § 13) and Handicappladser til kassevogne (the analogue of "van accessible").
- **Qualifier.** Adgangsforhold, tilgængelighed, tilgængelige for handicappede, Tilgængelighed for alle (the DS/ISO 21542 title), universelt design (wider), fysisk tilgængelighed (narrower, DH), niveaufri (narrower), handicapegnede, the handicap- prefix, invalide (outdated and still in force), handicapvenlig (colloquial, a policy sense). barrierefri: an unattested seed.
- **Lift.** elevator; type 2 elevator (narrower, DS/EN 81-70); minielevator; løftemateriel (the class); løfteplatforme, including the standard-title form "vertikale løfteplatforme til personer med hæmmede bevægelsesmuligheder"; trappelift (colloquial). "lift" appears in BR18 only in "elevator, lift eller lignende" (§§ 215, 216, 224), undefined.

## Conflations (recorded, not resolved)
1. Two decrees dated 13/04/2023 name one sign two ways: "invalidesymbol" (BEK 425, pdf p. 29; V 23 Invalidesymbol) and "handicapsymbol" (BEK 426 § 413). God Adgang writes "handicapsymbol (V23)".
2. BEK 426 § 433, stk. 3 treats compliance with "Tilgængelighed for alle" as making a building "tilgængelige for handicappede": two scopes used as one.
3. "lift" is an undefined alternative to "elevator" in BR18, a vehicle tail lift in the parking vejregel, and part of "trappelift" in KK. The elevator guidance's "Løfteplatforme forstås ikke som elevatorer" is an explicit non-equivalence.
4. "tilgængelig" means "open to the public" in BR18 § 214 (carried over from the first pass).
5. One sign, E 23 "Vejledning for invalide", serves access points, wheelchair routes and reserved parking.

## Not obtained
borger.dk: two fetches, 0 bytes each. A Svendborg God Adgang report: 404. vejregler.dk itself was not reached; both vejregler came from a municipal mirror. The DH report and both vejregler were read by stem grep, not in full. No DPO naming guide, so no community rejection of a form is attested. DS Håndbog 186 is paid.

## Self-attack
1. Sense is my judgment, row by row: "handicapvenlig kommune" is a policy sense, and I may have stretched it to fill the "wheelchair friendly" slot.
2. Tier 3 sources are mirrors. The vejregler PDFs on albertslund.dk are taken to equal Vejdirektoratet's text, which I did not check.
3. Breadth: 14 of 560 concepts. The quantity and element rows the first pass FOUND were barely touched.
4. Locators: the BEK 426 § 201, stk. 4 attribution comes from reading order in a two-column PDF, and the BR18 § numbers come from fragment headings.
5. The missing tier 5 matters most. Without a DPO source on naming, no form is known to be rejected by the community, and "invalide" is marked outdated only on a municipal page's word.
