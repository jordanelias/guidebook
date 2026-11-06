# Equivalents record: SV-SE (Swedish, Sweden), session_2026-11-06-base-vocabulary-review

**Verdict.** This pass is partial by design. It covers 13 register-v2 concepts, centred on the three owner classes; it does not cover all 560. Every non-seed quote and form verifies in the retrieved bytes: `python3 -I $D/tools/verify_equivalents.py` prints EXAMINED and failures and exits 1 on any failure. Swedish has no single umbrella word that prefixes "parking". The code pair "tillgänglig och användbar" qualifies the bay in one instrument. Traffic law, signs and municipal pages name the bay by its user group or permit ("rörelsehindrade", "parkeringstillstånd"). The disfavoured "handikapp-" forms survive in older official text and in lay usage. Nothing was written to the database, committed or pushed.

Here `D=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/SV-SE` and `E=$D/equivalents.tsv`. Re-run every count below rather than trusting a figure.

## Concepts attempted (13; list with `cut -f1 $E | tail -n +2 | sort -u`)
- Attempted: R2-050 designated accessible spaces, R2-052 Passenger pick-up areas, R2-281 Parking, R2-208 Pictogram of accessibility, R2-333 Accessible (the qualifier class), R2-402 tillgänglig och användbar, R2-179 toilet room, R2-163 Elevators, R2-165 cab, R2-164 Elevating devices, R2-168 Platform lifts, R2-169 stair lift, R2-173 lift (ceiling hoist).
- Not attempted: the other register-v2 rows, including the quantity, element and setting rows the first pass marked FOUND. For those the first-pass `observations.tsv` still holds one form per concept.

## Forms by usage type and tier
- By usage type: `awk -F'\t' 'NR>1{print $6}' $E | sort | uniq -c`. By tier: `awk -F'\t' 'NR>1{print $8}' $E | sort | uniq -c`.
- Tier 1 is the four first-pass Boverket texts. Tier 2 is Trafikförordningen, PBL, TSFS 2009:73, BFS 2011:12 and the repealed MFD ordinance. Tier 3 is Vägmärkesförordningen, the sign catalogue in law. Tier 4 is the Transportstyrelsen decision page, a Riksdag motion, Sundsvalls kommun and the VGR guideline (co-produced with DPOs). Tier 5 is Funktionsrätt Sverige and DHR. Seeds: `grep -c 'unattested seed' $E`. All seeds are flagged MODEL-GENERATED and are not findings.

## The owner classes in Swedish
- **Parking.** Code terms: "parkeringsplatser för rörelsehindrade med särskilt tillstånd" (HIN 17 §, binding), "tillgänglig och användbar parkeringsplats" (BFS 2024:13 2 kap. 6 §) and "parkeringsplatser som … reserverats för rörelsehindrade med parkeringstillstånd" (TF 13 kap. 8 §). Signs: "T7 Rörelsehindrade" under "E19 Parkering"; marking "M33 Rörelsehindrad". Guidance: "parkeringsplatser för personer med svårt att röra sig". Disfavoured: "handikapplats" (a citizen, quoted by Transportstyrelsen) and "handikapplatser" (motion 2008/09:T445).
- **Umbrella qualifier.** The code's own term is "tillgänglig och användbar" (PBL 8 kap. 1 § 3). Other forms: "tillgänglig" (sign H14, "tillgänglig även för rörelsehindrade"), "universell utformning" (repealed MFD ordinance 2 §, defined apart from "tillgänglighet"), "universellt utformad" (DHR, FRS) and "tillgänglighetsanpassade" (VGR, said of websites). The "handikapp" prefix is rejected by the DPO as "ålderdomligt eller stigmatiserande". No attested "wheelchair friendly" analogue: "rullstolsvänlig" is a seed only.
- **Vertical transport.** "hiss" and "personhiss" (BFS 2024:12 2 kap. 5 §, one object); "plattformshiss" and "trapphissar" (BFS 2011:12); "lyftanordning" is the class. Swedish keeps the hoist apart as "lyft" ("taklyft", "personlyft", "patientlyftar", product "Liko taklyft"), where English "lift" spans elevator, platform lift and hoist. "lyftplattform" is a seed only: it was not found in any fetched text.

## Conflations (recorded, not settled; see `conflation_note` in $E)
1. BFS 2011:12 defines "hiss" twice. 3 § includes a "plattform" as the load-carrier. Bilaga 5 excludes devices at no more than 0,15 m/s, which takes in most platform lifts. BFS 2024:12 does not say whether a "plattformshiss" is its "hiss".
2. "uppställningsplats" names a parking bay in HIN 17 § and a fire-vehicle hardstanding in BFS 2024:13 3 kap.
3. TSFS 2009:73 calls the pictogram both "den internationella handikappsymbolen" and "Rullstolssymbolen".
4. The owner's class treats accessible and universal as one usage. FRS and DHR separate them by scope.
5. VGR puts the set-down place and the reserved bay under one heading; BFS 2024:13 keeps them in two sections.
6. One phrase holds two register rows (R2-333 and R2-402).
- Correction to SYNTHESIS 3(e): the HIN parking form is not only advice-tier. The binding sentence of 17 § carries it.

## Could not obtain
The MFD PM on universal design (403 Cloudflare challenge; both Wayback forms gave no response). The Stockholm parking pages (404; no snapshot). The Linköping info sheet (404). Two guessed Boverket URLs (404). The Socialstyrelsen term bank itself was not reached. Currency of BFS 2011:12 and TSFS 2009:73 is [UNVERIFIED]: both were read as first issued.

## Self-attack
1. Two key texts may be superseded expressions: BFS 2011:12 and TSFS 2009:73 were read as first issued. Their terms may have changed in later amendments or in the 2025 rule set.
2. Sense judgments are mine, notably filing "Vertikalgående plattformshissar" under R2-168 rather than R2-170, and "personlyft" under R2-173.
3. Tier 4 mixes a co-produced guideline, a 2008 motion and a quoted citizen. "handikapplats" attests lay usage only.
4. Usage types are coerced to the brief's set. Guideline terms are marked "code term" with a scope note.
5. Colloquial coverage is thin: no news or forum sources (by rule), one municipality, and no DPO guide naming objects.
