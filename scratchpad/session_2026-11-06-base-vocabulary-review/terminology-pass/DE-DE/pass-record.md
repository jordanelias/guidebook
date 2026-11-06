# Pass record — terminology pass DE/DE (pilot), session_2026-11-06-base-vocabulary-review

**Verdict.** One principal instrument read in full (ASR V3a.2, federal workplace rule, 2025 amendment), plus the Bavarian building-code layer (BayBO Art. 48, BayTB Feb 2025 chapter A 4) and BGG § 4. The DIN 18040 bodies are NOT-OBTAINABLE (paid); only their free tables of contents were read. The pass is therefore a reading of the *workplace* carve and the *legal adoption* layer of German accessibility, not of DIN 18040's technical content, and coverage figures must be read with that limit. No database row, no commit. Every quote verifies in the saved text (`tools/build.py` exits 0).

## Retrieved and read
- ASR V3a.2 — BAuA blocked by Bunny Shield (403); retrieved via Wayback `if_` (snapshot 20251223). Read in full (text layer); figure images not read [SKIPPED].
- BayBO Art. 48 (Land Bayern; "Text gilt ab: 01.05.2026") — read in full. Other BayBO articles it cross-references NOT-READ.
- BayTB Ausgabe Februar 2025 (Land Bayern, 351 pp.) — chapter A 4 and Anlagen A 4.2/1, /2Bay, /3Bay read in full; rest [SKIPPED], grep-located only. Currency on 2026-11-06 [UNVERIFIED].
- BGG § 4 (federal) — read in full.
- DIN 18040-1:2010-10 and DIN 18040-2:2011-09 — body NOT-OBTAINABLE (DIN Media "ab 105,20 EUR"); free one-page TOCs and the 18040-1 product abstract read in full. Nothing about clause content is inferred from headings.
- Not attempted: DIN 18040-3, DIN 18041, DIN 32975/32984, DIN 18065, ASR A3.4 / A4.1, other Länder, MBO (model, not law). See `search-log.md`.

## Counts (computed; re-run, do not trust these)
- Observations: 90 — `awk -F'\t' 'NR>1' observations.tsv | wc -l` (by instrument: `awk -F'\t' 'NR>1{print $4}' observations.tsv | sort | uniq -c`).
- Reverse harvest: 90 — `awk -F'\t' 'NR>1' reverse-harvest.tsv | wc -l`.
- Coverage over 60 register concepts (32 from catalogue 2.1, 18 from 2.2, 10 active parameters): FOUND 53, SEARCHED-ABSENT 7, NOT-OBTAINABLE 0, NOT-READ 0 — `awk -F'\t' 'NR>1{print $2}' coverage.tsv | sort | uniq -c`.
- Quote verification: 179 exact byte substrings, 1 whitespace-normalised (a line break inside the quote), 0 failures — `python3 -I tools/build.py` (from repo root).
- Base DE aliases (all model-generated or unrecorded) seen in the saved texts: 28 of 190 by substring — see search-log, last entry; the parameter-level TRANSLATION aliases (Rampenneigung, Wendekreis, Bedienkraft, Flurbreite, Türbreite, Nachhallzeit, Farbtemperatur, Leuchtdichtekontrast) occur 0 times: `grep -c <alias> text/efd0b35345a96a8b.txt text/a301*.txt text/f695*.txt text/61c9*.txt`.

## Where English and German carve the field differently
1. **Performance criteria, not elements.** ASR organises every element by Wahrnehmbarkeit, Erkennbarkeit, Erreichbarkeit, Nutzbarkeit (plus Auffindbarkeit, Bedienbarkeit, Passierbarkeit), and by the Zwei-Sinne-Prinzip; BGG § 4 defines barrierefrei by "auffindbar, zugänglich und nutzbar". The English register has element statements and no criterion axis.
2. **Ramp is two things.** ASR "Schrägrampen (geneigte Verkehrswege …)" are in its scope; "Eine Rampe gemäß DIN 18040-1 Nr. 4.3.8 ist eine spezielle bauliche Anlage", outside it. One English parameter (ramp gradient) maps to two German objects with different rules; slope also splits into Längsneigung and Querneigung.
3. **Space is area × approach × under-run.** Bewegungsfläche (stated as a length × width area, never a "Wendekreis"), seitliche/frontale Anfahrbarkeit, Unterfahrbarkeit/Nichtunterfahrbarkeit change each other. "Turning circle" and "clear space for approach" are one German system.
4. **Force and torque.** Kraftaufwand (N) and Drehmoment/Moment (Nm) are stated separately for fittings; the register has force only.
5. **"Clearance" and "level" are three words each.** lichte Höhe here protects blind people from walking under stairs (unterlaufen), not vehicle headroom; Unterfahrbarkeit and lichte Weite are other clearances. "Level" sighted only as niveaugleich.
6. **Bedienelement** is one German class for every operable element (switch, handle, alarm call point, tap); RHFAC splits outlets, switches, controls, door hardware.
7. **Determination route.** ASR fixes measures through the Gefährdungsbeurteilung for the individual employee, with organisational measures (Patenschaften) as fallback; BayTB adopts DIN 18040 clause-by-clause and excludes all "R"-marked requirements of DIN 18040-2 in Bavaria. A German requirement is jurisdiction × building class × instrument layer, not one value.
8. **Absent from the workplace rule entirely:** sanitary rooms, lighting levels, acoustics quantities (only "raumakustische Maßnahmen"), parking — ASR V3a.2 supplements only the ASRs it has annexes for.

## Defects found in the METHOD
- **D1 Register rows are normalised statements, not concepts.** Catalogue 2.1 holds three near-duplicates of the slip-resistant-surface statement, two of "well-illuminated", two of "level landings", two of the contrast strip; coverage counts them as separate concepts and inflates FOUND. Collapse to concepts before rendering seeds.
- **D2 Ambiguous English heads.** "level", "clearance", "slope/gradient", "height clearance (if sheltered or parkade)" cannot be rendered to one seed; the register needs the sense, not the word.
- **D3 Element-only register.** No row for performance criteria, the two-senses principle, the determination route, or the people a rule names (Kleinwüchsige, Fußhebeschwäche, Echte Migräne, Tinnitus) — the axis on which the German text is built. The reverse harvest is larger than the forward hits.
- **D4 Instrument layer is not in the model.** German law reaches DIN through a Land's VV TB with exclusions; the register/coverage cell (concept × language-jurisdiction) has no slot for "Land" or "adopting instrument", and jurisdiction DE hides 16 Länder.
- **D5 Paywalled principal standard.** The instrument that carries most German building quantities (DIN 18040) is unreadable; a free TOC gives headings only. SEARCHED-ABSENT against ASR is not absence in German practice. Coverage needs a "read layer" column.
- **D6 Alias check by substring is wrong both ways** (inflection: "lichte Höhe" vs "lichten Höhe"; noise: "Gang" in "Zugang"). Promotion of a seed needs lemma-aware matching plus a human read, not `in`.
- **D7 Soft hyphens (U+00AD) in pdftotext output** split words at line ends ("Radabwei­/ser"), so a verbatim phrase may not exist as a byte string; the record must either quote the split form or normalise and say so. This pass quoted only unsplit spans.
- **D8 retrieval_log has no Wayback helper and CDX is blocked by egress policy**; snapshot choice used the availability API with a timestamp, which returns only the closest capture.

## Self-attack — five likeliest ways this record is wrong
1. **FOUND is generous.** Several FOUND rows rest on a weak sense (Zapfstelle for sink faucet; Mikrowelle in a reach area for "microwave mounting height"; DIN headings only for audio communication). A stricter reader would mark 5-10 of them SEARCHED-ABSENT or PARTIAL.
2. **Wrong principal instrument.** The ASR is a workplace rule; building accessibility in Germany is DIN 18040 via the Länder. Choosing the free text over the governing one may skew the German carve toward employer duties (Gefährdungsbeurteilung) that a building-code reading would not show.
3. **Currency.** BayTB Feb 2025 being in force on 2026-11-06 is unverified; a 2026 BayTB or a published DIN 18040 revision (drafts 2023) would change which clauses are adopted.
4. **Figures unread.** ASR dimensions inside Abb. images (e.g. door approach areas) were not read; terms printed only inside figures are missing from the harvest.
5. **Reverse-harvest glosses leak English framing.** Each gloss is marked as ours, but choosing which German phrases count as "concepts the register lacks" was done with the English register in mind; an equally valid German reader might split or merge them differently.
