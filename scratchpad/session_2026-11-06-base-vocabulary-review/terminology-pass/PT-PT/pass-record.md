# Pass record: terminology pass PT/PT, session_2026-11-06-base-vocabulary-review

**Verdict.** The principal Portuguese instrument was read in full in Portuguese: Decreto-Lei n.º 163/2006, consolidated to its 5th version (DL 10/2024, with Lei 44/2026 on arts 12 and 21), with its annex "Normas técnicas". Its 13 tables and figures, which the consolidated page omits, were read as text labels from the held 2006 Diário da República original. The drawings were not read. Portaria n.º 301/2019 (the existing-housing method) was read only as a secondary transcription; the official text was not obtained. Of 75 register concepts, 50 are FOUND, 13 FOUND-PARTIAL and 12 SEARCHED-ABSENT. The reverse harvest has 85 phrases. Every quote verifies in the saved text (`build.py` exits 0). Nothing was written to the database and nothing was committed.

## Retrieved and read
- **DL 163/2006, versão actualizada** (PGDL host, artefact `b54a68f15078410a.html`, fetched 2026-11-06). Read in full: preamble, arts 1–26 incl. 9.º-A, and annex chapters 1–4. [SKIPPED: 13 "(ver documento original)" tables and figures. Their labels were read from the 2006 original.]
- **DL 163/2006, DR 1.ª série N.º 152, 2006** (held REF-01032, artefact `5b800bfbee2efde7.pdf`, batch 23). Partly read: the table and figure labels only, extracted here with `pdftotext -raw`. [SKIPPED: the drawings, which are images. The 2006 body was not re-read, because the consolidated text supersedes it.]
- **Portaria n.º 301/2019** (informador.pt transcription, artefact `cdc065b2bfd585b3.html`). Read in full as transcribed. [SKIPPED: Quadro 2, which is absent from the copy.] Its fidelity to the DR original is UNVERIFIED, and every row from it says so.
- **Not read:** the DR consolidated text (a JS shell, Wayback not tried); Portaria 1110/2001 (plan contents); DL 95/2019 (reabilitação); acoustic, fire and workplace rules; the regional diplomas of Açores and Madeira; LNEC guides; and the NP/EN standards. All NOT-READ for budget, and none attempted, so none is marked NOT-OBTAINABLE.

## Counts (re-run, do not trust; from the repo root, `D=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/PT-PT`)
- Rebuild and verify: `python3 -I $D/build.py`. At writing it reported 91 observations, 85 reverse-harvest rows and 0 failures.
- Coverage: `cut -f3 $D/coverage.tsv | sort | uniq -c` gave 50 FOUND, 13 FOUND-PARTIAL, 12 SEARCHED-ABSENT. By source, `awk -F'\t' 'NR>1{print $2"\t"$3}' $D/coverage.tsv | sort | uniq -c` gave: catalogue 2.1 22/8/2; catalogue 2.2 13/3/2; base parameters 7/1/2; the 15 B651 headings RHFAC does not name 8/1/6.
- Distinct phrases observed: `awk -F'\t' 'NR>1{print $2}' $D/observations.tsv | sort -u | wc -l` gave 90.
- Rows per text file: `awk -F'\t' 'NR>1{print $7}' $D/observations.tsv | sort | uniq -c` gave 86 for the consolidated text, 2 for the 2006 original and 3 for the portaria. The same command on reverse-harvest.tsv gave 73, 3 and 9.
- Raw-byte check: the FR command with `locate_quote(..., session='session_2026-11-06-base-vocabulary-review')`. 4 rows are `missing`: the 2006 figure labels, which live in a compressed PDF from batch 23 and verify only in this pass's own pdftotext output.
- Held pt aliases in the texts: search-log S12 gave 10 of 114 by substring. 0 aliases are tagged PT, and no parameter-level TRANSLATION alias occurs.

## Where Portuguese carves the field differently from English (instrument-derived; glosses ours)
1. **Ramp is defined by slope, and run by projection.** "Os troços de percursos pedonais com inclinação igual ou superior a 5 % devem ser considerados rampas" (4.7.6). Run length is "projecção horizontal". Each limit is a triple of inclinação, desnível and projecção horizontal, with "valores interpolados" allowed between triples. A separate relaxed set applies to "obras de alteração ou conservação".
2. **"Escadarias em rampa"** (stepped ramp) is its own element with its own "desenvolvimento", and has no register row.
3. **Tread is a depth in buildings and a length in the street.** The tread is "profundidade (cobertor)" in 2.4.3, but "Comprimento (cobertor)" in the public-way stair table (1.3.1). Riser is "altura (espelho)". Landings split into "patamares" (ends) and "patins" (intermediate). Ramp landings are "plataformas horizontais de descanso".
4. **Turning is two categories.** Manoeuvres are "sem deslocamento" (rotação de 90º/180º/360º) or "com deslocamento" (mudança de direcção de 90º/180º/180º em T). The portaria instead speaks of a "diâmetro das zonas de manobra". There is no single "turning circle".
5. **Contrast is not quantified, but floor reflectance is.** It is a recommended band, "reflectância média … entre 15 % e 40 %" (4.7.2). That is a luminance-reflectance quantity without a contrast pair, which LRV contrast (parameter 8) does not capture.
6. **Door hardware turns on "maçaneta".** In PT-PT the "puxadores em forma de maçaneta" are forbidden (4.9.9). The held BR seed "maçaneta tipo alavanca" would point a PT search at a prohibited object.
7. **Surface properties are defined terms:** Estável, Durável, Firme, Contínua (4.7.1), each with its own definition. Slip resistance appears only as "boa aderência mesmo na presença de humidade ou água" for unenclosed and wet spaces, and as "antiderrapante" for nosing strips and pool surrounds.
8. **"espaços encerrados" / "não encerrados"** is a defined split that changes values (headroom 2 m / 2,4 m) and the surface rules.
9. **Tiers by use, not by building type.** A toilet tier is triggered by "for previsível um uso frequente" (2.9.4 4), 2.9.6).
10. **Existing housing has its own regime (portaria, secondary).** Intervenção simples, média and profunda (N1/N2/N3); "parcela acessível"; "compartimentos essenciais à acessibilidade" by dwelling type (T3); and "medidas de mitigação" vs "medidas de compensação" (equivalent performance) vs "Cumprimento das NTA".
11. **Drafting.** The annex mixes "deve" with "É recomendável". Exceptions are an argued route (art. 10: "desproporcionadamente difíceis", heritage case by case, with the justification published). Compliance runs through a "plano de acessibilidades" and a "termo de responsabilidade".

## Defects found in the METHOD
- D1. **The held source was not the edition in force.** REF-01032 is the 2006 original. Its currency note lists four amending decrees, and the PGDL page also shows Lei 44/2026 (on arts 12 and 21). A pass that read only the held source would have read a superseded annex: 3.3.4 1)–2) are revoked by DL 10/2024.
- D2. **The consolidated host omits every table and figure**, so a full read needs two texts of different dates. The labels were checked only where read, and the figure drawings were not seen.
- D3. **Substring alias hits over-attest** ("banco" hits banks and worktops). Same as FR D3.
- D4. **The language-tag carve is weak.** All 114 pt aliases are BR-tagged or untagged, none PT. BR and PT terms differ in sense here ("maçaneta").
- D5. **The 2.2 quantity words remain senses, not concepts** ("volume" = traffic volume; "capacity" = car-park and hall capacity). FOUND-PARTIAL and ABSENT were judged by hand in `PARTIAL`/`ABSENT`.
- D6. **The instrument list is not derivable:** `research_code_leads` has no PT row, and the registry entry has no amendment history. Portaria 301/2019 came from web search.
- D7. **No locate_quote route for derived PDF text.** The raw-byte check cannot see the 2006 figure labels.

## Self-attack: the five likeliest ways this record is wrong
1. **The PGDL host is not the official journal.** It may lag or mis-transcribe an amendment, and it was not cross-checked against a DR consolidated text. Lei 44/2026 is taken from its own note.
2. **Figure labels come from the 2006 original.** If DL 10/2024 or another amendment changed a table, those labels may be stale. The annex amendment note names only 3.3.4.
3. **The portaria rows rest on an aggregator copy.** Quadro 2 is missing, and the wording may differ from the DR original.
4. **Sense judgments are mine.** For example: "plataformas horizontais de descanso" read as level landings, "protecções de banheira" as B651 enclosures, "cobertas" as shelter, and "obras nos percursos acessíveis" as scaffolding. Some FOUND or FOUND-PARTIAL calls may be too generous.
5. **Absence is scoped to three texts.** Lighting, acoustics, bollards and speed bumps may sit in other PT rules (acoustic regulation, road code, municipal regulations) that were not read. SEARCHED-ABSENT here does not mean absent from Portuguese law.
