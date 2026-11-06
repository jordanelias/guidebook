# Equivalents record — DE/DE (Germany), session_2026-11-06-base-vocabulary-review

**Verdict.** I attempted 14 register-v2 concepts, chosen for the three owner classes and their neighbours. Every quote verifies in text extracted from retrieved bytes: `python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DE-DE/tools/equiv_build.py`, run from the repo root, exits 0. German parking is not one noun. Building law says **Stellplatz** and marks the accessible bay with the umbrella predicate. Road law says **Parkplatz** and keys the bay to a permit class. The colloquial **Behindertenparkplatz** appears only in municipal and publisher texts. Sources are DE only: federal, plus the Länder BY, BE, BW, NI, BB and RP, with each row's jurisdiction recorded. No Austrian or Swiss source was used.

**Attempted (14):** `awk -F'\t' 'NR>1{print $1}' equivalents.tsv | sort -u`. These are R2-005, -050, -083, -163, -164, -165, -168, -169, -208, -333, -399, -471, -534 and -540. **Not attempted:** the other 546 rows (`tail -n +2 ../../register-v2/concepts.tsv | wc -l` minus 14). That includes R2-051, R2-170 (named in notes only, not judged), R2-281 and every DE-origin performance-criterion row except R2-399.

**Counts (re-run; do not trust).** I recorded 64 rows and 61 distinct forms (`awk -F'\t' 'NR>1{print $3}' equivalents.tsv | sort -u | wc -l`).
- By usage type (`cut -f6 | sort | uniq -c`): code term 41, colloquial 12, qualifier 6, product name 2, outdated or disfavoured 1, unattested seed 2.
- By tier (`cut -f8 | sort | uniq -c`): tier 1 (second reading) 14, tier 2 (other statutes and regulations) 15, tier 4 (public bodies) 29, tier 5 (DPO) 4, seed 2. Tier 3: 0 rows. StVO § 39 and Anlage 3 are counted as tier 2 because the sign rules live in the statute. I found no separate signage manual (the VzKat was not fetched).
- Rows with a conflation note: 12 (`awk -F'\t' 'NR>1 && $12!=""' equivalents.tsv | wc -l`).

**The owner classes in German (DE):**
- *Parking:* the building-law forms are Stellplätze, PKW-Stellplätze, barrierefreie(r) Stellplatz/Stellplätze and Stellplätze für Menschen mit Behinderungen. The road-law forms are Parkmöglichkeiten für schwerbehinderte Menschen mit außergewöhnlicher Gehbehinderung … sowie für blinde Menschen, Parkplätze für schwerbehinderte Menschen and, for the personal bay, Parkplätze für bestimmte schwerbehinderte Menschen. The colloquial forms are Behindertenparkplätze, Behinderten-Parkplätze and, in Leichte Sprache, Behinderten-Park-Plätze. The road-law class includes blind people, so it is not a wheelchair class.
- *Umbrella qualifier:* barrierefrei is the statutory term (BGG § 4). Wider terms appear in federal guidance: inklusiv, Design für alle (with "Konzeption für alle Nutzer" as the EU-law rendering), universelles Design and Zugänglichkeit. Narrower terms: rollstuhlgerecht, glossed as "barrierefrei und uneingeschränkt mit dem Rollstuhl nutzbar" (DIN 18040-2 level R, RLP circular), and stufenlos erreichbar, which Berlin ranks below barrierefrei. Older term: behindertengerecht, still in force in VwV-StVO zu § 26. I could not verify that it is disfavoured.
- *Vertical transport:* Aufzug, Aufzüge and Aufzugsanlagen are the code terms. Fahrstuhl and Fahrstuhlanlage are colloquial and appear beside Aufzug in one municipal text. The platform lift is Plattformaufzug or Vertikaler Plattformaufzug, and Hublift is a weak match. The stair lift is Treppenlift, Treppenschrägaufzug or Plattformaufzug mit geneigter Fahrbahn. The cab is Fahrkorb, Aufzugskabine or Förderplattform, and I found no German word for the elevator cab apart from these.

**Conflations, recorded and not settled:**
1. **Stellplatz and Parkplatz.** Building law and road law use different nouns, and the Bundesfachstelle checklist uses both for one object in one sentence (PDF p. 7).
2. **Zugänglich.** "Öffentlich zugänglich" means open to the public (BayBO Art. 48 Abs. 2), while "Zugänglichkeit" in the federal guide means accessibility (UN-BRK), and EU law renders Barrierefreiheit as "Zugänglichkeitskriterien" (BBSR PDF p. 32). This is the same pattern as Danish tilgængelig.
3. **Lift.** It is the stair lift in BayTB Anlage A 4.2/1 Nr. 2 and an Aufzug in "brokenlifts.org" (BVG FAQ).
4. **Rollstuhlfahrersinnbild/-symbol.** The sign marks bays for aG, Amelie/Phokomelie and blind people (StVO Anlage 3 lfd. Nr. 7).
5. **Rampe.** The BVG FAQ uses it for both the station ramp and the deployable vehicle device.
6. **2-Kanal-Prinzip.** BSK uses it for two routes (stair plus lift) and Zwei-Sinne-Prinzip for two senses.

**What I could not obtain:**
- Wheelmap categories: 403, then the Wayback `if_` and plain forms both returned no response (E12–E14).
- LAGeSo Berlin flyer (404) and BayGaStellV (404, guessed URL).
- A road-sign catalogue (VzKat): not attempted.
- DIN 18040-1/-2/-3 and DIN EN 81-40/-41/-70 bodies: paid.
- The Leidmedien.de list has no built-environment terms, so I found no DPO source that rejects any form.
- I read the large PDFs (BBSR, Bundesfachstelle) only at grep-located passages.

**Self-attack:**
1. Tier 4 is 29 of 62 attested rows, and three municipalities (Stuttgart, Hameln, München) carry the whole colloquial parking class. Three cities are not "DE usage", so read those rows as sub-national.
2. The Hameln text is an OCR layer, so a quote can verify against OCR error. I chose clean spans, but the `text_kind` column, not my eye, is the guard.
3. Several equivalences rest on my reading of the sense: Hublift as a platform lift, Förderplattform under cab, and Vertikale Erschließung as broader. A German reader could file them differently.
4. Nine web-search priors in the log were reconstructed after the results (flagged there). The fetch priors were written before `fetch()`.
5. Labelling behindertengerecht "outdated or disfavoured" rests on no source read here. The note says [UNVERIFIED], but the usage-type cell asserts it anyway.
