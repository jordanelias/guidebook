# Equivalents record: PT-PT, session_2026-11-06-base-vocabulary-review

**Verdict.** The three owner classes are covered in Portuguese (Portugal) from 13 retrieved texts across all five tiers, but the coverage is narrow: 23 of 560 register-v2 concepts were attempted, most in a single pass over DL 163/2006. No Brazilian source is used as attestation. The held pt aliases for these classes are BR-tagged or untagged ('vaga acessível', 'banheiro acessível', 'elevador acessível', 'desenho universal'), and none is attested by the PT texts read. Every quote verifies in its saved text (`python3 -I tools/build_equivalents.py` exits 0). Nothing was written to the database, and nothing was committed.

**Concepts attempted (23):** R2-004, 005, 020, 021, 050, 057, 074, 083, 085, 089, 092, 114, 163, 164, 168, 169, 174, 175, 176, 208, 281, 333, 358. List them with `cut -f1,2 equivalents.tsv | tail -n +2 | sort -u`. The other 537 rows, including every performance criterion, outcome level and trigger-rule row PT originated, were not attempted, because the budget went to the owner classes.

**Counts (re-run, do not trust):** `tail -n +2 equivalents.tsv | wc -l` gave 80 rows. By usage type, `cut -f6 equivalents.tsv | tail -n +2 | sort | uniq -c` gave code term 52, qualifier 14, outdated or disfavoured 7, colloquial 4, product name 2, regional variant 1. By tier, `cut -f8 equivalents.tsv | tail -n +2 | sort | uniq -c` gave tier 1: 47, tier 2: 10, tier 3: 1, tier 4: 12, tier 5: 10. Rows with a conflation note: `awk -F'\t' 'NR>1 && $12!=""' equivalents.tsv | wc -l` gave 16. There are no unattested seeds.

## The owner classes in Portuguese (Portugal)
- **Parking.** No PT form uses an umbrella adjective. The code forms are "lugares (de estacionamento) reservados" plus a user group: "para veículos em que um dos ocupantes seja uma pessoa com mobilidade condicionada" in DL 163/2006 2.8.1, and "a pessoa com deficiência condicionada na sua mobilidade" in Código da Estrada art. 145.º q). The bay is keyed to the permit, "cartão de estacionamento de modelo comunitário" (DL 307/2003 and DL 128/2017). The older permit word "dístico" survives on road-sign panel 11d (RST art. 46.º, 1998 text) and in the Provedor's 2015 usage. "Vaga", the BR word for a parking bay, means a care-home or course place in the PT texts.
- **Umbrella qualifier.** The code word is "acessível", applied by designation ("designados de acessíveis"), and its domain noun is the plural "acessibilidades". The user-group words "mobilidade condicionada" and "mobilidade reduzida" do most of the work. "Design universal" (not "desenho universal") and "sem barreiras" appear only in policy (ENIPD). "Inclusiva" qualifies society, not objects. Disfavoured forms are "necessidades especiais" (DL preamble, rejected by Acesso Cultura), "dos deficientes" and "deficiente motor".
- **Vertical transport.** The car lift is "ascensor" ("Ascensores de cabina"). The platform lift is "plataforma elevatória", and the stair platform is "plataforma elevatória de escada". The class word is "meios mecânicos de comunicação vertical". Escalators and moving walkways are "escadas mecânicas" and "tapetes rolantes". "Elevador" occurs 0 times in DL 163/2006.

## Conflations (recorded, not resolved; locators in equivalents.tsv)
1. **"Ascensor" vs "elevador" in Lisbon.** Carris names its funiculars "Ascensor (da Glória, do Lavra)" and lists "Elevador" as a separate fleet class. The Marinha Grande lift regulation excludes "funiculares" from "ascensores" and uses "elevadores" only for theatre machinery. So the code's car-lift word is the operator's funicular word.
2. **"Condicionado".** In "mobilidade condicionada" it means reduced mobility. In Odivelas "estacionamento condicionado" (art. 4.º n.º 3) it means restricted parking.
3. **The person is defined as the permit.** Odivelas art. 4.º n.º 1 defines "Pessoa com deficiência" as the holder of the parking card.
4. **Synonym pairs used as one.** "Mobilidade condicionada" and "mobilidade reduzida" sit in one decree (art. 14.º against the annex) and in one table entry (Acesso Cultura p. 39). The guide also treats "acessível" and "adaptada" as one usable pair, and both "dístico" and "cartão" name one permit.
5. **Carve differences.** One PT phrase, "percurso acessível", covers register rows R2-072 and R2-074. Stairs take two words, "escadas" (buildings) and "escadarias" (street).

## Not obtained
- The Lisbon city parking page (Cloudflare 403).
- RCM 9/2007 (arquivo.pt 403, umic.pt 404).
- Metro de Lisboa (403).
- An EMEL regulation (HTML stub).
- Every Wayback fetch, reset at session level while a control URL returned 200.
- DL 320/2002 itself, and the RST amendments.
- No APD, ACAPO or CNOD guide was found. Acesso Cultura is a cultural-access association with named reviewers; its Co-1 status is not established.

## Self-attack
1. Tier 1 dominates (47 of 80), so the "other forms" are mostly the same decree read twice. Colloquial attestation rests on two tier-5 documents.
2. Several PDFs were fetched from regional or aggregator hosts (madeira.gov.pt, portugal2030.pt, escs.ipl.pt), not the DR. The DL 307/2003 and RST texts are originals, not consolidated.
3. Sense calls are mine: "lancil" set against R2-092, "barras de apoio" set against handrails, and "Plataformas elevatórias de escada" set against stair lift.
4. Short quotes ("lugares reservados", the "ins-" fragment) verify, but they carry little context. Two-column PDFs forced cut quotes.
5. The Carris claim that "Elevador" is Santa Justa rests on search snippets. The bytes show only the menu word.
