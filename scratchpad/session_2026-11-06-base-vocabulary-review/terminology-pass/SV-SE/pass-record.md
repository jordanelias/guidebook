# Pass record: terminology pass SV-SE (Swedish, Sweden), session_2026-11-06-base-vocabulary-review

**Verdict.** This record restarts an attempt that was cut off. The caller's candidate, "BBR accessibility provisions", is no longer the instrument. Boverket's own page (a9327303d7fa8feb.html) says BBR was repealed on 1 October 2026 by BFS 2026:9. It says the new rules "i huvudsak inte längre" carry allmänna råd, and that older BBR rules may still be applied for a limited time. The binding building accessibility text is now **BFS 2024:12**, which sits beside **BFS 2024:9** (safety in use, which also carries accessibility requirements under PBF 3 kap. 18 §) and **BFS 2024:13** (plots). All three have been in force since 1 July 2025. The simple-obstacles rules are **HIN, BFS 2011:13** in the BFS 2013:9 reprint. I retrieved all four from rinfo.boverket.se and read them in full. Of 75 register concepts, 40 are FOUND, 20 FOUND-PARTIAL and 15 SEARCHED-ABSENT. The reverse harvest has 100 rows. Every quote verifies. Nothing was written to the database.

## Audit of the cut-off attempt's files
- The four text files are byte-identical to `pdftotext -layout` of the persisted PDFs. `build.py` `chain()` checks this, and the PDF sha256 prefixes match the manifest. All 104 observation quotes and all 100 reverse-harvest quotes verify. I read all four texts in full and checked each observation's locator and sense against that reading. I re-tested each zero-count claim in the ABSENT notes by substring.
- Kept: all observations, all reverse-harvest rows, seeds.tsv and coverage.tsv. Discarded: nothing failed verification.
- Corrected: (1) instruments.tsv said 5 kap. of BFS 2024:13 was skipped from the harvest, but two rows come from it (5 kap. 2 § and 6 §). The row now says so. (2) instruments.tsv now records the HIN currency evidence and the JavaScript-shell result (search-log W5).
- Not repairable: the search-log for W0, W1 and W2 records expectations that were written after the results. That deviation is declared there and stands.

## Retrieved and read
- **P12** BFS 2024:12, all of 1–4 kap. plus transitional provisions (b8d1102ac9bece6f). **P9** BFS 2024:9, 1–3 kap. (dea239e870469ba8). Roof safety, poisoning and plant rooms were read but not harvested. **P13** BFS 2024:13, 1–5 kap. (24b5e81b0f4a0928). 3 kap. (fire-service access) was not harvested. **HIN** BFS 2013:9 omtryck, 1–18 § with all advice text (c40b915d36d9d797). [SKIPPED: bild 1–2, image-only.]
- Retrieved, not read as instruments: BBR avsnitt 3 (26fe99c7c3402a1e, repealed), the BBR guidance PDF (b87cd122ace6e7b4, archived), and HIN 2 (e41ecfa32b0c440f, superseded by the reprint).
- Not attempted (budget): ALM 2 (BFS 2011:5, public places), BFS 2024:10 (noise; reverberation likely sits there), BFS 2024:11 (dwelling suitability), SS-EN 81-70, Arbetsmiljöverket rules. None of these is marked NOT-OBTAINABLE.

## Counts (re-run, do not trust; from the repository root, `D=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/SV-SE`)
- Rebuild and verify with `python3 -I $D/build.py`, which exits 1 on any failure. At writing: 104 observations, 100 reverse-harvest rows, 0 failures.
- Coverage: `cut -f3 $D/coverage.tsv | sort | uniq -c` gave 40 / 20 / 15. Source groups: `cut -f2 $D/coverage.tsv | sort | uniq -c` gave 32 + 18 + 10 + 15.
- Distinct phrases: `awk -F'\t' 'NR>1{print $2}' $D/observations.tsv | sort -u | wc -l` gave 102.
- Per instrument: `awk -F'\t' 'NR>1{print $4}' $D/observations.tsv | sort | uniq -c` gave HIN 48, P9 24, P12 23, P13 9.
- Advice-tier rows: `grep -c 'allmänt råd' $D/observations.tsv` gave 39. These are non-binding text.
- Held sv aliases: `select count(*), count(distinct alias) from term_aliases where lower(language)='sv'`. Of these, 17 distinct aliases are substrings of the four texts (snippet in search-log W4). The eight parameter-level TRANSLATION aliases (ramplutning, korridorbredd, dörrbredd, vändyta, manöverkraft, efterklangstid, luminanskontrast, färgtemperatur) occur 0 times. They are word-for-word renderings that no instrument uses (lesson 5).

## Where Swedish carves the field differently (instrument-derived; glosses ours)
1. **The numbers left the rule.** BFS 2024:12 has no corridor width, door-leaf width, control height or contrast value. It fixes three "dimensionerande" measures: "planmåttet för rullstol", "vändmåttet av en cirkel" and "öppningsmåttet för fri passage". It also sets a 1:12 ramp, a lift with a 1 100 mm short side, and a lift at more than 1 m of level difference. Everything else is "tillgänglig och användbar". Width "ska ... bestämmas utifrån utformningen och längden av utrymmet". Where English names a quantity, Swedish law names the reference wheelchair and the function.
2. **One measure, three figures.** "öppningsmåttet för fri passage" is 0,80 in buildings, 0,76 in dwellings and 0,90 on plots. The plot instrument restates the whole measure set. Door width (parameter 9) is a clear-passage opening, not a door property.
3. **Population carve.** The law has two groups: "nedsatt rörelse- eller orienteringsförmåga". In HIN's advice, orientation covers sight, hearing and cognition, so hearing loops and acoustics are orientation provisions. The helper ("hjälpare") is part of the design body: landings and lifts are sized for a wheelchair "som manövreras av hjälpare".
4. **Corridor is not the object.** The regulated space is the defined "kommunikationsutrymme". "korridorer" appears only as an example of it (HIN 4 §).
5. **HIN is obstacle-shaped.** Each binding clause reads "Hinder i form av bristande ... ska avhjälpas". Removal is tempered by "praktiska och ekonomiska förutsättningarna", and the measures appear only as "bör" advice. Contrast is quantified as NCS "ljushetskontrast på minst 0,40", not as LRV.
6. **Accessibility is spread across instruments.** Lighting, slip, handrails ("balansstöd" is the class, "ledstång" one form), stair marking, headroom and glass marking all sit in the *safety* rule BFS 2024:9. Headroom is split into "fri höjd" (2,00) and "utskjutande byggnadsdelar" below 2,20 over a "gångyta".
7. **Drafting.** BFS 2024:12 separates "utformningskrav" (2 kap.) from "tekniska egenskapskrav" (3 kap.). Alterations go through an "anpassning" ground list (4 kap. 1 §). Deterioration is barred, with exceptions (4 kap. 2 §). "Mindre avvikelse" is permitted.

## Defects found in the METHOD
- D1. Substring tests over-count across Swedish compounds and inflection: "korridor" ⊂ "korridorer", "trycke" ⊂ "trycket", "lättläst" ⊂ "lättlästa". The 17-alias figure is therefore not a findings count.
- D2. `retrieval_log.locate_quote` cannot read the compressed PDF bytes. Verification rests on pdftotext output, chained to the PDF by `chain()`.
- D3. The rinfo.boverket.se listing pages are JavaScript shells (W5), so I could not test amendments to BFS 2024:12 or BFS 2011:13 against the register.
- D4. `references/standards-registry.md` has two SE entries that contradict each other and mislabel BFS 2024:12 as "ALM 2 / allmänna råd". REF-01024's URL is a municipal copy. 132 of the 134 held sv aliases have jurisdiction NULL. None of these was corrected (outside my folder).
- D5. The instrument list was not derivable from the base: `research_code_leads` returned 0 rows. I found P9 and P13 by following P12's citations and Boverket's list of the new rules.
- D6. The search-log expectations for W0, W1 and W2 were written after the results.

## Self-attack: the five likeliest ways this record is wrong
1. **Advice counted as FOUND.** HIN advice ("bör") supplies 39 rows. Signage, door hardware, controls and tactile marking reach FOUND largely through it. A binding-only view needs a filter on `allmänt råd`.
2. **Sense judgments are mine.** Bollards ("Stolpar i gångbanor"), Gratings (scraper and drainage gratings, and child-safety well lids), "Seating" (audience places) and "distance" (walking and reading distance) are FOUND-PARTIAL by my reading. `PARTIAL` in build.py is hand-assigned.
3. **Scope.** SEARCHED-ABSENT means absent from four texts. Reverberation time and colour temperature may sit in BFS 2024:10 or in Arbetsmiljöverket rules, which I did not read. Speed bumps and planters belong to ALM 2 and street design.
4. **Currency.** The amendment status of BFS 2024:12 and HIN after retrieval is [UNVERIFIED] (D3). Lag 2026:746 changes PBL 8 kap. from 2027-01-01, and HIN may be reissued under it.
5. **Repeal reading.** The BBR repeal and its transition rest on one Boverket web page, not on the text of BFS 2026:9, which I did not retrieve. While older BBR rules may still be applied in some cases, its avsnitt 3 terms remain live practice vocabulary that this record omits.
