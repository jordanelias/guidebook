# Search log: terminology pass PT/PT, session_2026-11-06-base-vocabulary-review

Method note: the prior expectations below were written in working notes before each result came back, and copied into this file afterwards. They were not committed before the results arrived, so treat them as declared, not proven, priors.

## S1. Base: held PT sources
- Query: `select ref_id, pub_title, standard_number, url from evidence_sources where jurisdiction in ('PT','pt','Portugal')`
- Prior: one or two rows for DL 163/2006, because PT is a bucket-2 jurisdiction since 2026-10-01.
- Result: REF-01026, an Ordem dos Arquitectos transcription marked UNVERIFIED, whose notes list DL 136/2014, 125/2017, 95/2019 and 10/2024 as amending decrees with "CURRENCY NOT ESTABLISHED". REF-01032 is the Diário da República original of 8 Aug 2006, VERIFIED.
- Query shape: jurisdiction match only. The held source is the 2006 original, not the edition in force.

## S2. Base: research_code_leads
- Query: every row of `research_code_leads` whose fields contain 'PT' or 'ortug'.
- Prior: there may be a lead for the ramp clause.
- Result: 0 rows printed. The instrument list cannot be derived from leads.

## S3. Registry
- Query: `grep -n -i "portug\|PT " references/standards-registry.md`
- Result: one entry. `standard_cited: "Decreto-Lei 163/2006"`, `status: CURRENT`, last_checked 2026-04-19, source_url dre.pt. The entry gives no amendment history. It also quotes values in key_changes, which this pass does not use.

## S4. Held artefacts for DL 163/2006
- Query: manifest lines in retrieval-log/*/manifest.jsonl matching 163, pgdl or dre.
- Result, all from batch 23: the OA PDF; the DR consolidated page (a 2346-byte JS shell); the DR 2006 PDF; and three PGDL single-article pages. The PGDL page lists versions 1 to 5, the latest being DL 10/2024, and offers "Imprimir todo o diploma".

## S5. Fetch: PGDL whole-diploma page
- URL: https://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?nid=3110&tabela=leis&nversao=&so_miolo=
- Prior: the full consolidated text, current version, with tables possibly missing.
- Result: 200, 198910 bytes, ISO-8859-1, artefact b54a68f15078410a.html. The full text has every article and the whole annex. Thirteen tables or figures are replaced by "(ver documento original)". Per-article amendment notes are shown, including a "Lei n.º 44/2026, de 10/08" on arts 12 and 21, which no held record mentions. The page writes "%" as "/prct.".

## S6. Fetch: DR consolidated
- URL: https://diariodarepublica.pt/dr/legislacao-consolidada/decreto-lei/2006-108253479
- Prior: a JS shell again.
- Result: a JS shell, identical sha to batch 23 (0794abe5…). The Wayback route was NOT attempted (budget). The PGDL text was not cross-checked against a DR consolidated version, which is a gap.

## S7. WebSearch: the implementing portaria of art. 9.º-A
- Query: `portaria método de projeto melhoria da acessibilidade edifícios de habitação existentes artigo 9.º-A Decreto-Lei 163/2006`
- Prior: a 2019 or 2020 portaria exists.
- Result: Portaria n.º 301/2019, de 12 de setembro. The hits were aggregators (informador.pt), practitioner blogs and LNEC papers, plus one diariodarepublica.pt link to DL 163/2006 itself.
- Query shape: descriptive Portuguese. It found the instrument's name but no official URL.

## S8. WebSearch: official URL for Portaria 301/2019
- Query: `"Portaria n.º 301/2019" pgdlisboa OR files.dre.pt método de projeto acessibilidade`
- Prior: a files.dre.pt PDF link.
- Result: aggregators only, with no files.dre.pt or pgdlisboa hit. The tool reports that it does not support OR.

## S9. WebSearch: second attempt
- Query: `"301/2019" portaria acessibilidade "files.dre.pt" OR "dre.pt/application" 2019-09-12 175`
- Prior: low.
- Result: no official URL. Mostly Brazilian noise. EMPTY for the official text.

## S10. Fetch: informador.pt transcription
- URL: https://informador.pt/legislacao/diploma/portaria-n-o-301-2019/
- Purpose: link discovery. No DR link was found in the page, and the page holds the full transcription.
- Result: 200, artefact cdc065b2bfd585b3.html. Read as a SECONDARY copy and flagged on every row. Quadro 2 is missing from it.

## S11. In-text absence checks (all three saved texts)
- Command: `grep -oi <w> text/<file> | wc -l`, giving counts for L / O / P:
  micro 0/0/0; tomada 0/0/0; bebedouro 0/0/0; lomba 0/0/0; pilarete 0/0/0; baliza 0/0/0; andaime 0/0/0; lux 1/1/0 (only inside "fluxo"); ilumina 2/1/0; acústic 1/1/0; reverbera 0/0/0; "temperatura de cor" 0/0/0; volume 1/1/0 (traffic volume); capacidade 9/8/0; lotação 10/10/0; contrast 10/9/0; reflect 6/6/0; abrigo 0/0/2; cobert 10/11/0 (mostly "cobertor"); toldo 1/1/0 (an obstruction); "espelho aberto" 0; táctil 4/4/0; tátil 0; podot 0; indução 0; floreira 0; estai 0; envidra 1/1/0; campainha 1/1/0.
- Prior: no acoustics, lighting or colour-temperature quantities, since the French instrument already lacked colour temperature and this is an older text.

## S12. Held pt aliases in the saved texts
- Query: `select distinct alias, jurisdiction from term_aliases where lower(language)='pt'`. Each alias was lower-cased and tested as a substring of the whitespace-collapsed, lower-cased text/*.txt.
- Result: 114 distinct aliases, none tagged PT (21 tagged BR, the rest untagged), and 10 substring hits: altura livre, andarilho, banco, barra de apoio (BR), cadeira de rodas, circulação, corredor, lavandaria, normas de acessibilidade, percurso acessível. "banco" also matches "bancos" (banks, art. 2.º h)) and "bancadas", so a substring hit alone does not establish the sense. None of the parameter-level TRANSLATION aliases occurs: largura da porta, soleira nivelada, tempo de reverberação, contraste de luminância, or the BR-tagged inclinação de rampa, largura do corredor, área de manobra, força de operação, maçaneta tipo alavanca.
