# Pass record — terminology pass DA/DK, session_2026-11-06-base-vocabulary-review

**Verdict.** The principal Danish instrument, BR18 as published on bygningsreglementet.dk ("BR18 (Aktuelt)"), was retrieved directly and its nine access-relevant chapters (kap. 2, 6, 7, 9, 10, 16, 17, 18, 20) were read in full in Danish, with three official guidance documents. Of 75 register concepts (60 as in the FR pilot plus the 15 B651 headings RHFAC does not name): 38 FOUND, 14 FOUND-PARTIAL, 23 SEARCHED-ABSENT. The reverse harvest has 69 rows. Every quote verifies in the saved text, and every saved text re-derives byte-for-byte from its raw artefact (`build.py` exits 0). The Danish technical layer the authority points to (DS Håndbog 186, DS/ISO 21542) is paid and NOT-OBTAINABLE, so this record covers the regulation and its free guidance only. Nothing was written to the database and nothing was committed.

## Retrieved and read
- BR18 kap. 2 Adgangsforhold (§§ 48–62), kap. 6 (§§ 159–160), kap. 7 (§§ 161–165), kap. 9 (§§ 196–241), kap. 10 (§§ 242–249), kap. 16 (§§ 358–367), kap. 17 (§§ 368–376), kap. 18 (§§ 377–384), kap. 20 (§§ 393–402): every `?ajax=1` section fragment, read in full. The chapter pages are accordion shells; the text comes from the fragments.
- Vejledning til brugerbegreb (5 pp.), Vejledning om tilgængelighed ved transportable konstruktioner (1. udg. 2020, 4 pp.), Bygningsreglementets vejledning om adgangsforhold (1 p.): read in full. No figures in any of them.

## Not read, and why
- BR18 kap. 1, 3–5, 8, 11–15, 19, 21–37 and bilag 1–6: budget. Kap. 4 Afløb and kap. 14 Fugt og vådrum are the likeliest places for drainage and floor-surface rules, so those two SEARCHED-ABSENT rows are weak.
- Retsinformation's consolidated bekendtgørelse: JavaScript shell, no Wayback snapshot. The ELI number tried was my guess. Whether the portal text equals the legal text is UNVERIFIED, and so is currency after the "1/7-31/12 2025" period.
- DS Håndbog 186 and DS/ISO 21542: NOT-OBTAINABLE (paid; the guidance says so itself). DS/EN 81-70 and DS 490: paid, not attempted. The vejledninger on lydforhold, lys og udsyn, elevatorer and boligindretning, and the Q&A pages: NOT-READ (budget).

## Counts (re-run, do not trust; from the repo root, `D=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/DA-DK`)
- Rebuild and verify: `python3 -I $D/build.py`. At writing it reported 80 observations, 69 reverse-harvest rows, 39 text files re-derived from raw bytes, and 0 failures.
- Coverage: `cut -f3 $D/coverage.tsv | sort | uniq -c` gave 38 / 14 / 23.
- Distinct Danish phrases observed: `awk -F'\t' 'NR>1{print $2}' $D/observations.tsv | sort -u | wc -l` gave 75.
- Rows per instrument: `awk -F'\t' 'NR>1{print $4}' $D/observations.tsv | sort | uniq -c` gave 74 for BR18 and 6 for the transportable-structures guidance. For the reverse harvest it gave 52 BR18, 11 brugerbegreb, 5 transportable and 1 adgangsforhold.
- Held DA aliases that occur as substrings of the saved texts: printed by `build.py` (19 of 156 at writing). Several of these are string hits only: "greb" hits inside "brugerbegreb", "tilgængelighed" occurs only in the guidance, and "stigning" occurs as riser height, not as ramp gradient. Parameter-level TRANSLATION aliases that occur nowhere: rampehældning, gangbredde, vendeplads, betjeningskraft, dørbredde, luminanskontrast, farvetemperatur, støttegreb, taktile ledelinjer.
- Raw-byte check with `retrieval_log.locate_quote`: it reports most quotes as "missing". The cause is that the HTML carries entities (`&aelig;`) and `<a name>` anchors in the middle of sentences, and the PDFs are compressed. `build.py`'s re-derivation check stands in for it. This is a tool limit, recorded under D4.

## Where Danish carves the field differently (instrument-derived; glosses ours)
1. **The domain is "Adgangsforhold" (access conditions), not "tilgængelighed".** In the BR18 text read, "tilgængelig" means *open to the public* ("offentligt tilgængelige bygninger"). "tilgængelighed" occurs only in § 246 (the EN 81-70 title and "der sikrer tilgængelighed for personer med handicap") and in the guidance. A search seeded with the register's "accessibility" → "tilgængelighed" misses the regulation's own chapter.
2. **One standard of performance, "ved egen hjælp", organised as a chain:** "komme frem til dem, ind i dem samt frem til deres funktioner". Kap. 2 is split *frem til bygningen / ved bygningen / fælles adgangsveje i bygningen*. Only COMMON routes are regulated in kap. 2. Routes inside dwellings are in kap. 9.
3. **Landing interval has two different bases.** Outdoors, "reposer for hver 12 m" (by length). In common routes, "en vandret repos for hver 0,60 m stigning" (by rise). The register's "regular intervals" and parameter 12 hold only one of these.
4. **"stigning" is both riser height (§ 57) and the rise of a ramp (§ 56).** "grund" is the tread, defined as a depth. The held alias "stigning" as a SYNONYM for ramp gradient is therefore a sense error.
5. **Door width is one quantity, "fri passagebredde"**, which is the same everywhere (doors, WC doors, temporary structures). It comes with a latch-side space "ved siden af døren modsat hængselsiden". There is no nominal-leaf pairing (contrast the French carve).
6. **The turning space exists only in the WC:** "frit manøvreareal med en diameter på 1,5 m … fri af dørens opslagsareal". There is no general turning circle.
7. **Parking is defined by the vehicle**: "handicapegnede køretøjer".
8. **Contrast, edges and slip are unquantified or absent.** "kontrastfarve" is never given a value. "værn" is a fall guard, not a kerb. Slip resistance appears only in guidance ("skrid hæmmende").
9. **Acoustics and lighting sit outside the access chapter** and are pointed to DS 490 and the sound and light vejledninger. Assistive listening is "teleslyngeanlæg eller lignende installationer på minimum samme niveau".
10. **Drafting structure:** a functional rule followed by "Bestemmelsen anses som opfyldt når" (deemed-to-satisfy values). The equivalent route is a municipal "dispensation" if "hensynene bag kravene opfyldes igennem andre løsninger". Disabled people's organisations have standing to appeal.
11. **Who the rules serve is stated by the authority itself.** The detail rules are "overvejende udformet med henblik på kørestolsbrugere, gangbesværede og synshandicappede". The "brugerbegreb" widens the users to "alle mennesker, med ingen, mindre eller større funktionsnedsættelser".
12. **A named conflict:** step-free access may give way to flood protection ("uforenlig med hensynet til klimasikring", § 51, stk. 4).

## Defects found in the METHOD
- **D1. The base cannot derive the DK instrument list.** It has 0 research_code_leads and 0 evidence_sources, and the registry entry is one URL plus an unverified claim about SBi 230. The list came from the portal's own navigation (search-log S0–S6).
- **D2. A 200 is not a text.** The chapter pages and the Retsinformation and DS pages are shells. Extracted-length checks caught this. Nothing in `retrieval_log.fetch` flags it.
- **D3. The register's own label misdirects** (carve 1). Seeding on "accessibility" alone would have found only guidance.
- **D4. `locate_quote` cannot verify quotes in entity-encoded HTML or compressed PDF.** The FR pass's raw-byte check does not carry over. A re-derivation check was used instead.
- **D5. The official guidance is partly stale.** Brugerbegreb cites "kapitel 6 om adgangsforhold" and "kapitel 13 om indretning", which is an older chapter numbering, and the adgangsforhold guidance is linked through a `br18_version6` path.
- **D6. Substring alias matching over-attests** ("greb", "stigning"), as the FR pilot found. FOUND and the alias report are string results, and the sense judgment is mine.
- **D7. Prior expectations were logged after the fact** (see the search-log header).

## Self-attack: the five likeliest ways this record is wrong
1. **Currency and legal identity.** The text is the portal's "Aktuelt". The bekendtgørelse was never read, so an amendment or a portal-versus-law difference would not show here.
2. **Scope.** SEARCHED-ABSENT means absent from nine chapters and three guidance documents, not from Danish law or practice. Kap. 4 and 14, the vejregler and DS Håndbog 186 could hold shelter, drainage, floor slip, bollards and controls.
3. **Sense judgments.** Mapping "værn" to edge protection, "Brugerbetjente anlæg" to accessible controls, "fri afstand" to clear space for approach, or "opklappelige armstøtter" to grab bars is my reading. Some FOUND rows may be wider or narrower than marked.
4. **Locators were assigned by hand.** The single-§ fragments (§§ 48, 57, 61, 62, 159, 160, 358, 359, 366, 367, 368, 377, 378) carry no "§" in their text. Their § number comes from the fragment URL, and an "nr." could be off by one.
5. **Extraction.** `h2t.py` and `pdftotext` could split or join words ("skrid hæmmende" is likely one word in the source). A quote that verifies against the extraction is not proof of the source's exact spelling.
