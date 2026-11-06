# Pass record: terminology pass NL/NL, session_2026-11-06-base-vocabulary-review

**Verdict.** The principal instrument, the Besluit bouwwerken leefomgeving (Bbl), was retrieved in its expression in force on 2026-11-06 (2026-09-24_0) from the official BWB XML repository. wetten.overheid.nl reset every connection. Every accessibility-bearing part was read in full in Dutch. The rest of the decree (fire, structure, energy, health apart from galm) was skipped and only grep-located. Bouwbesluit 2012 is repealed (last expression ends 2023-12-31) and was read only for carve comparison. NEN 9120:2025 is NOT-OBTAINABLE: it is free of charge but geo-restricted to the Netherlands and DRM-locked. Of 75 register concepts: 27 FOUND, 26 FOUND-PARTIAL, 22 SEARCHED-ABSENT. The reverse harvest holds 48 phrases. Every quote verifies in the saved text. No database row was written and nothing was committed.

## Retrieved and read
- Bbl, artefact `52ef1dbbf8d109ba.xml`, converted to `text/52ef1dbbf8d109ba.txt` by `tools/x2t.py`. Read in full: afd. 4.1; §§ 4.2.3–4.2.5; § 4.3.3; afd. 4.5; afd. 4.6; § 4.7.1; arts 4.213–4.218a; § 4.7.10; their Hoofdstuk 3 counterparts (§§ 3.2.3–3.2.4, afd. 3.5–3.6, § 3.7.1); afd. 5.1–5.2; arts 2.4–2.5, 6.15a and 6.22; Bijlage I divisies A and B. [SKIPPED: the remaining safety, health, energy, chapter 6 and chapter 7 rules, and most of afd. 5.3–5.4, because they are not accessibility-bearing (grep-checked for the concept words, search-log G1–G10). The converter flattens table cells into rows, so the multi-row table headers were read as flattened rows. Two images in Bouwbesluit 2012 are unread.]
- Bouwbesluit 2012, artefact `56c4f96582c47206.xml`. Read: arts 2.33a and 2.42–2.46, afd. 4.4–4.7. The rest was skipped.
- Ministry page "Toegankelijk bouwen" (BZK), artefact `8be21dedbca82962.html`. This is guidance, not an instrument. It is used for one observation and two reverse-harvest rows, and these never set a coverage status (build.py decides status on Bbl rows only).
- Not read: the Regeling bouwwerken leefomgeving, the Omgevingswet, the nota van toelichting of Stb. 2024, 368, and the NEN standards the Bbl points to (NEN 2580, 2575, 3011, EN 1125). These are NOT-READ because of the budget. The NEN texts were not attempted, so they are not marked NOT-OBTAINABLE. Public realm (CROW, municipal rules) is outside the Bbl and was not searched.

## Counts (re-run, do not trust; from the repo root, `D=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/NL-NL`)
- Rebuild and verify: `python3 -I $D/build.py` (exits 1 on any unverified quote, unknown concept or missing ABSENT note). At writing: 51 observations, 48 reverse-harvest rows, 0 failures.
- Status: `cut -f3 $D/coverage.tsv | sort | uniq -c` gives 27 FOUND / 26 FOUND-PARTIAL / 22 SEARCHED-ABSENT. Status by register source: `awk -F'\t' 'NR>1{print $2"\t"$3}' $D/coverage.tsv | sort | uniq -c`. 12 of the 22 absences are B651 public-realm headings.
- Distinct phrases: `awk -F'\t' 'NR>1{print $2}' $D/observations.tsv | sort -u | wc -l` gives 51. There are no duplicate phrases. Near-duplicate register rows share observations through `|`.
- Rows per text file: `awk -F'\t' 'NR>1{print $7}' $D/observations.tsv | sort | uniq -c` gives Bbl 48, BB2012 2, BZK 1.
- Raw-byte check: the `locate_quote` one-liner from FR-FR/pass-record.md, with `$D`, reports 16 of 99 quotes "missing" from the raw XML. These quotes cross an `<intref>` tag, a list number or a heading in the XML. They verify in the text layer, and their locators were cross-checked against the article spans of the text (0 outside their article).
- Held NL aliases occurring in the Bbl text: 13 of 140 by substring (search-log G10). Of those, 7 are hits in the register sense. None of the eight parameter-level TRANSLATION aliases occurs.

## Where the Dutch instrument carves the field differently (instrument-derived; glosses ours)
1. **Accessibility is a sector, not a feature.** The "toegankelijkheidssector" is a defined part of a building that is "zelfstandig bruikbaar" for "personen met een functiebeperking". Floor area, height and use class trigger it, and inside it the room sizes, corridor widths and wholly accessible WC and bath apply. The English register has no zoning concept.
2. **Doors are not regulated, openings are.** The width rule falls on the "doorgang" (vrije breedte, defined between construction parts), not on the "deur". Door hardware and force appear only for escape routes ("lichte druk tegen de deur", "panieksluiting").
3. **The threshold is a level difference.** "drempel" never occurs in the Bbl. Each threshold rule is a "hoogteverschil groter dan 0,02 m, gemeten vanaf de vloer met aankleding, overbrugd door een hellingbaan". The ministry's own page translates it back to "drempel". Bouwbesluit 2012 measured from the "afgewerkte vloer".
4. **A ramp is capped by its rise, not its run.** Art. 4.30 sets "een hoogte van niet meer dan 1 m" and grades the slope by rise. No intermediate landing ("tussenbordes" 0) and no run length are named. There is only a top "hellingbaanbordes", waived below 0,03 m. Ramps carry a "geleiderand", not a handrail.
5. **Stairs and ramps sit under safety.** § 4.2.4 is "Veilig overbruggen van hoogteverschillen" in afdeling Veiligheid. Accessibility (afd. 4.6) points back to it. Edge protection is framed as preventing falls, with a climb test ("voorkomen overklauteren") and a sphere test for openings.
6. **One population umbrella.** "personen met een functiebeperking" is the only population term, and "rolstoelgebruiker" appears once. There is no sensory, cognitive or neurodivergent carve. Contrast appears once ("hoog contrast", unquantified). The decree names the CRPD in its considerans.
7. **Every rule passes through a use-class table.** Each paragraph opens with an "aansturingsartikel" (a functional aim) and a table of "gebruiksfuncties" that switches lids and values on or off. Compliance routes are a "gelijkwaardige maatregel", a "maatwerkvoorschrift" (which may only relax) and, for alterations, the "rechtens verkregen niveau". Owner-built dwellings ("woonfunctie voor particulier eigendom") are exempt from all of afd. 4.6.
8. **Acoustics is absorption area,** per unit of room volume, in shared circulation of residential buildings only, against "geluidhinder door galm". It is not reverberation time, the same as in the French pass.
9. **Corridor is "gemeenschappelijke verkeersruimte".** The held aliases "gang" and "gangbreedte" occur in no rule.

## Overlap with TERM-090 and TERM-092 (Belgian-sourced; noted, not edited)
- TERM-090 "level difference" was minted from Flemish "niveauverschil". The Bbl's phrase for the same concept is "hoogteverschil" (48 hits). "niveauverschil" occurs only inside "lucht-geluidniveauverschil", in the acoustics sense. The NL and BE phrases differ, so a single Dutch alias would mislead.
- TERM-092 "intermediate landing" has no NL counterpart in the Bbl ("tussenbordes" 0, "rustbordes" 0). The Bbl caps the rise per ramp instead.

## Defects found in the METHOD
- D1. **The official HTML portal is unreachable here.** wetten.overheid.nl fails at the protocol level (exit 92/52). The BWB XML repository is the working route and should be the default for NL. `retrieval_log` has no BWB helper. `tools/x2t.py` is ad hoc and outside the repository.
- D2. **The registry is wrong about NEN 9120.** Its URL is a 404, and "free to download" hides a geo-block and DRM. Lead 98 ("paywalled") is also inexact: the standard is free but not obtainable from here. Neither defect was corrected.
- D3. **The register is criterion-shaped** (as in FR D1 and DE D1). Three slip-resistant-surface rows and two lighting rows share observations.
- D4. **The 2.2 quantity words are senses** (volume, capacity, distance, time). Each NL hit is in another sense, and FOUND-PARTIAL was set by hand in `PARTIAL`, which is a judgment.
- D5. **The register has no slot for zoning by trigger** (toegankelijkheidssector), use-class switching, or exemptions by tenure. These are the axes the Dutch rule is built on.
- D6. **Substring alias testing over-attests:** "gang" hits only in toegang and gangpad.
- D7. **The instrument list is not derivable.** No lead or registry entry names the Bbl itself. The list came from knowledge of the Omgevingswet structure, confirmed by the BWB manifest.

## Self-attack: the five likeliest ways this record is wrong
1. **Skipped parts.** Fire-safety and vluchtroute rules were read only where grep pointed. An accessibility-relevant clause there (for example evacuation of wheelchair users) could be missed.
2. **Table flattening.** `x2t.py` writes table cells row by row, so a column heading paired with the wrong lid could mislead. No observation depends on a table column mapping, but the reading of which use classes a rule applies to is unverified.
3. **Concept matching is my judgment.** Treating "hoogteverschil > 0,02 m" as the level threshold, "verhard pad" as a firm surface or "spreekinstallatie" as communication technology is my reading, not the instrument's equation.
4. **NEN 9120 carries the real technical vocabulary.** Many SEARCHED-ABSENT rows (tactile indicators, controls, contrast quantities) are absent from the Bbl, not from Dutch practice. NL coverage is not exhausted.
5. **Currency.** The expression is current per the manifest of 2026-11-05. An amendment published but not yet consolidated would not show. The Regeling (ministerial rules) was not checked.
