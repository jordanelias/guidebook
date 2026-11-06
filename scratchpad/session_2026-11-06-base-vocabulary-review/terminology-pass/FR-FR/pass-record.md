# Pass record — terminology pass FR/FR (pilot), session_2026-11-06-base-vocabulary-review

**Verdict.** Both principal French building-accessibility arrêtés were retrieved (Légifrance returned 403; the Wayback `if_` route worked) and read in full in French, apart from four annex diagrams. Of 60 register concepts: 50 FOUND, 6 FOUND-PARTIAL, 4 SEARCHED-ABSENT. The reverse harvest has 100 phrases the English register does not name. Every quote verifies in the saved text and in the raw persisted bytes. The pass is not complete for FR: existing buildings, voirie, the CCH and the AFNOR standards were not read. Nothing was written to the database.

## Retrieved and read
- Arrêté du 20 avril 2017 (new ERP and IOP), consolidated "Version en vigueur au 09 novembre 2024": articles 1–24 and annexes 1–9 read. [SKIPPED: the diagrams of annexes 4 and 5, which are images.] Artefact `43802a8ee6314644.html`.
- Arrêté du 24 décembre 2015 (new collective housing and individual houses), consolidated "Version en vigueur au 08 février 2025": articles 1–21 and annexes 1–7 read. [SKIPPED: the diagrams of annexes 4 and 5.] Artefact `014af9f59dafdd0b.html`.
- Not read: the arrêté du 8 décembre 2014 (existing ERP), the voirie texts (arrêté du 15 janvier 2007, décret 2006-1658), the CCH articles and the arrêté du 14 mars 2014. All are NOT-READ because of the budget. The five AFNOR/NF standards the arrêtés cite were not attempted, so they are not marked NOT-OBTAINABLE. Currency after the snapshot dates is UNVERIFIED (R4).

## Counts (re-run, do not trust; run from the repository root, with `D=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/FR-FR`)
- Rebuild and verify everything: `python3 -I $D/build.py` (exits 1 on any unverified quote). At writing it reported 110 observations, 100 reverse-harvest rows and 0 failures.
- Coverage by status: `cut -f3 $D/coverage.tsv | sort | uniq -c` gives 50 FOUND, 6 FOUND-PARTIAL, 4 SEARCHED-ABSENT.
- Distinct French phrases observed: `awk -F'\t' 'NR>1{print $2}' $D/observations.tsv | sort -u | wc -l` gives 96.
- Rows per instrument: `awk -F'\t' 'NR>1{print $4}' $D/observations.tsv | sort | uniq -c` gives 84 for A17 and 26 for A15. For the reverse harvest it gives 75 and 25.
- Raw-byte check (0 missing for both TSVs at writing): `python3 -c "import sys,csv;sys.path.insert(0,'scripts/research');import retrieval_log as r;f='$D/observations.tsv';print(sum(r.locate_quote(x[5],session='session_2026-11-06-base-vocabulary-review')[0]=='missing' for x in list(csv.reader(open(f),delimiter='\t'))[1:]))"` (and the same for reverse-harvest.tsv).
- Held French aliases occurring as substrings of the two texts (169 distinct, 17 hit at writing): `select distinct alias from term_aliases where lower(language)='fr'`, each lower-cased and tested with `in` against the whitespace-collapsed, lower-cased `$D/text/*.txt`.

## Where English and French carve the field differently (instrument-derived; glosses ours)
1. **Ramp.** The fixed ramp is a "plan incliné". "rampe" appears only in A15, as a "rampe amovible", and never in A17. The base's seed "pente de rampe" does not occur in either text.
2. **One rule, every route.** Corridors are "circulations intérieures horizontales" and inherit the "cheminement extérieur accessible" rules (A17 art. 6). "couloir" does not occur (0/0). The register splits corridor, path and ramp into separate concepts; French has one route object with a "profil en long" and a "profil en travers".
3. **Door width is two quantities**: a "largeur nominale" paired with the "largeur de passage utile" it corresponds to. A single "door width" parameter loses that pairing.
4. **Tread is a width** ("largeur du giron"), not a depth. Riser height is the steps' "hauteur", and the "contremarche" is the riser element.
5. **Contrast is never quantified.** There is no luminance, LRV or réflexion term (0/0). "contraste visuel" and "fortement contrastées" are BROADER than parameter 8.
6. **Acoustics are pointed elsewhere.** A17 defers reverberation time to the "exigences acoustiques en vigueur" and falls back on "aire d'absorption équivalente". A15 uses absorption area only.
7. **"level" is four French notions:** horizontal, "écart de niveau", "dénivellation", and "niveau décalé considéré comme un étage". The register's quantity word "level" is ambiguous across them.
8. **Spaces are defined by need, not by device:** "espace d'usage", "espace de manœuvre (de porte | avec possibilité de demi-tour)" and "palier de repos". Each is defined for wheelchair users *and* people with one or two canes (annexe 2).
9. **Each article is drafted as aim, then prescription** ("Usages attendus" / "Caractéristiques minimales"), with an equivalent-effect route ("solutions d'effet équivalent"). The register carries prescriptions only.
10. **Housing has its own carve** with no register row: "unité de vie", "caractéristiques de base", "adaptabilité", "logements évolutifs", "travaux simples", "réversibilité".
11. **Edge protection's purpose differs between the two texts.** A17 says "alerter les personnes du risque de chute"; A15 says "éviter les chutes".

## Defects found in the METHOD
- **D1. The register is criterion-shaped, not concept-shaped.** Several are near-duplicates, such as "Surface is firm, stable and slip resistant" and "Surface is stable, firm, and slip resistant". They inflate FOUND counts because they share observations. The 32 recurring statements need collapsing to concepts before 14 languages are counted against them.
- **D2. The quantity words of catalogue 2.2 are senses, not concepts.** "volume" (speaker volume), "capacity" (lift capacity), "ratio" (room-type mix) and "distance" (trail markers) each mean one RHFAC criterion. A French hit on the bare word is in another sense: volume as a spatial volume, distance between "ressauts". The FOUND-PARTIAL label had to be added by hand (`PARTIAL` in build.py), which is a judgment, not a derivation.
- **D3. Substring matching of held aliases over-attests.** "inclinaison" and "orientation" occur only in unrelated senses. A string hit must not promote an alias (E4) without the sense being judged. `add-alias` via T3 should require the quote, not a text match.
- **D4. Some held aliases are word-for-word translations,** such as "seuil de niveau" and "largeur de couloir", in neither text. This is the OR-12b failure the method exists to prevent.
- **D5. Tooling gaps.** No helper turns a Légifrance HTML page into article-located text, so `h2t.py` was written ad hoc and is outside the repo. `retrieval_log.fetch` records no "via Wayback" field beyond the URL. The register has no "aim vs prescription" or "compliance route" axis.
- **D6. Registry defect (not corrected).** `references/standards-registry.md` titles its FR entry "Arrêté du 20 avril 2017" but links JORFTEXT000029925726, the 2014 text. Research lead 86's "every route 403" was true for direct fetches only; the Wayback `if_` route succeeds.
- **D7. The instrument list is not derivable.** `research_code_leads` holds no FR housing, voirie or existing-building leads, so the list came from search (W1–W2), not the base.

## Self-attack: the five likeliest ways this record is wrong
1. **Currency.** Both texts are snapshots from November 2024 and February 2025. An amendment between then and 2026-11-06 would make some locators or phrases stale, and nothing here would show it.
2. **HTML extraction.** `h2t.py` strips tags and could drop text held in attributes or tables. The two annex tables (annexe 4) read coherently, but the diagrams were never seen. A phrase living only in a figure is missed.
3. **Concept matching is my judgment.** Mapping "palier de repos" to "Level landings with clear space", "espace d'usage" to "Clear space for approach", or "à effleurement" to "Accessible controls" is my reading, not the instrument's equation. Some FOUND rows may be wider or narrower than marked.
4. **Locators were assigned by hand** from the reading, not parsed. A sub-paragraph number (2° b) and similar) may be off by one level even where the quote verifies.
5. **Coverage is scoped to two texts.** SEARCHED-ABSENT means absent from these two arrêtés, not from French law. Shelter, seating and lockers may sit in the voirie texts or in guides not read. Coverage for the FR pair is therefore not exhausted (plan C.3 stopping rule unmet).
