# Search log: equivalents pass PT-PT, session_2026-11-06-base-vocabulary-review

Method: each fetch's prior is appended to this file by `tools/get.py` in the same process, before `retrieval_log.fetch()` is called (SYNTHESIS defect 9 convention). Web-search queries and local greps are logged by hand; for those the prior was written in working notes first, so treat those priors as declared, not proven. Jurisdiction of every source is stated; BR sources are excluded from PT attestation.

## E1. Tier 1: second reading of DL 163/2006 (consolidated, text/b54a68f15078.txt)
- Query: `grep -n -i -E 'estacionamento|ascensor|plataforma|monta|tapete|cartão|design|desenho|universal|barreira|símbolo'` and stem counts for 'elevador', 'inclusiv', 'universal', 'acessív', 'mobilidade condicionada', 'deficiência', 'dístico'.
- Prior: 'ascensor' (not 'elevador') for the car lift; 'plataforma elevatória' for the platform device; parking as 'lugares reservados'; umbrella word 'acessível', no 'universal' or 'inclusivo'.
- Result: 'elevador' 0, 'universal' 0, 'inclusiv' 0, 'dístico' 0. 'ascensor' 16, 'plataforma' 21, 'estacionamento' 25. New: 'mobilidade reduzida' (art. 14.º) beside 'mobilidade condicionada'; 'pessoas com necessidades especiais' (preamble); 'meios mecânicos de comunicação vertical' (3.2.1-3.2.3) as the class word; 'Ascensores de cabina' and 'Plataformas elevatórias de escada' (3.2.2); 'dispositivos mecânicos de elevação' (1.7.2).
- Query shape: stems, so inflection is caught; sense read per line.

## E2
- Fetch: `https://imt.madeira.gov.pt/images/Documentos%20Condutor/Decreto_Lei%20n307_2003%2010%20dezembro.pdf`
- Prior (written before the call): PDF of the 2003 original (national decree hosted by a Madeira regional body, so jurisdiction PT national; text may be a scan). Expect 'cartão de estacionamento', 'pessoas com deficiência condicionadas na sua mobilidade', 'lugares reservados'.
- Retrieval: status 200, 454784 bytes, artefact 46145b1adc316236.pdf, sha256 46145b1adc316236131871d7713efffd3574db20ab8bbd636c740cf27e44f74e, text 11708 chars -> text/46145b1adc31.txt

## E3
- Fetch: `https://imt.madeira.gov.pt/images/Documentos%20Veiculos/Distico/Decreto%20Lei%20128_2017_9out.pdf`
- Prior (written before the call): DR PDF of DL 128/2017; expect 'cartão de estacionamento de modelo comunitário', 'mobilidade condicionada' and perhaps 'dístico' in the folder name only.
- Retrieval: status 200, 162754 bytes, artefact 346a9653b5975d28.pdf, sha256 346a9653b5975d282fd5fff2de2bc16db64a1bd42b9cfecfea29ee3056d7e66c, text 13115 chars -> text/346a9653b597.txt

## E4
- Fetch: `https://informacoeseservicos.lisboa.pt/servicos/detalhe/estacionamento-para-pessoa-com-mobilidade-condicionada`
- Prior (written before the call): Municipal service page; expect 'lugar de estacionamento reservado', 'dístico' or 'cartão', perhaps 'pessoa com mobilidade condicionada'. Could be a JS shell.
- Retrieval: status 403, 5687 bytes, artefact 55a86a76c807ec00.html, sha256 55a86a76c807ec004abc44bc6abf1c042e1af695ac86be89477cc8bebf2105fb, text 59 chars -> text/55a86a76c807.txt

## E5
- Fetch: `https://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?nid=349&tabela=leis&so_miolo=`
- Prior (written before the call): nid=349 is a guess from memory for the Código da Estrada; it may return a different diploma. If right, expect art. 50.º/70.º 'lugares reservados a veículos ... pessoas com deficiência' and 'cartão de estacionamento'.
- Retrieval: status 200, 461853 bytes, artefact 77a1b6761d1b14b4.html, sha256 77a1b6761d1b14b493a92762b908edc7fe8b5b30c176403b862b26eaccd651f5, text 143858 chars -> text/77a1b6761d1b.txt

## E6
- Fetch: `https://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?nid=349&tabela=leis&pagina=2&ficha=101&so_miolo=`
- Prior (written before the call): Pagination parameter guessed (pagina=2, ficha=101); may return page 1 again. If right, expect art. 145.º 'estacionamento ... em lugar reservado ... pessoas com deficiência' as a grave offence.
- Retrieval: status 200, 489358 bytes, artefact 86e1e7861124b891.html, sha256 86e1e7861124b891285a329c27efdcc90235e7cef6e2050d17b4ee7ffd99ffe1, text 166141 chars -> text/86e1e7861124.txt

## E7
- Fetch: `https://www.madeira.gov.pt//Portals/27/Documentos/Legislacao/1998_10_01_DecReg_22A_98_AprovaoRegulamentodeSinalizacaodoTransito_RST.pdf`
- Prior (written before the call): 1998 original DR PDF hosted by Madeira regional government; possibly a scan with no text layer. If text, expect a painel adicional 'modelo n.º 11d' for vehicles bearing the 'dístico de deficiente' (outdated form, since DL 307/2003 replaced the dístico with the cartão).
- Retrieval: status 200, 29322274 bytes, artefact a2177a5496fe5308.pdf, sha256 a2177a5496fe530816447d27f7a91ee5abb6d813d999d776dedca8dbfff0f59a, text 268404 chars -> text/a2177a5496fe.txt

## E8
- Fetch: `https://www.cm-mgrande.pt/cmmgrande/uploads/document/file/3882/regulamento_municipal_de_manuten__o_e_inspe__o_de_ascensores__monta__cargas__escadas_mec_nicas_e_tapetes_rolantes.pdf`
- Prior (written before the call): Municipal regulation under DL 320/2002; expect the statutory class 'ascensores, monta-cargas, escadas mecânicas e tapetes rolantes' and 'instalações'; no 'elevador'; no platform lift.
- Retrieval: status 200, 224841 bytes, artefact 4001b27cc7717c2a.pdf, sha256 4001b27cc7717c2abd5245ccf13345122a67b61b7f3d7de74e581fd406d74eed, text 29624 chars -> text/4001b27cc771.txt

## E9
- Fetch: `https://associacaosalvador.com/wp-content/uploads/2024/11/CARTAO-DE-ESTACIONAMENTO-PCDM-1.pdf`
- Prior (written before the call): Advocacy guide for people with motor disability; expect 'cartão de estacionamento para pessoas com deficiência condicionadas na sua mobilidade' (PCDM acronym from the filename) and 'lugares reservados'; perhaps the colloquial 'lugar para deficientes' named as wrong.
- Retrieval: status 200, 79654 bytes, artefact d3e2eee5fb4c2c11.pdf, sha256 d3e2eee5fb4c2c118a4d5a6062f7cb7330e02a31b6de3b588575f4f650499263, text 2511 chars -> text/d3e2eee5fb4c.txt

## E10
- Fetch: `https://www.provedor-jus.pt/documentos/Rec_1B2015.pdf`
- Prior (written before the call): Ombudsman recommendation; expect statutory forms plus 'dístico' as an older or everyday name, and 'lugares de estacionamento reservados'.
- Retrieval: status 200, 135737 bytes, artefact d70346d6040ceb56.pdf, sha256 d70346d6040ceb566d8ae4f8cc7287afdb535c20abaf4e34266f9f49a2e280bd, text 20198 chars -> text/d70346d6040c.txt

## E11
- Fetch: `https://arquivo.pt/wayback/20131107121800mp_/http://www.umic.pt/images/stories/publicacoes/rcm9_2007.pdf`
- Prior (written before the call): DR text of RCM 9/2007 archived by arquivo.pt (the Portuguese web archive, a Wayback analogue). Expect 'desenho para todos', 'design inclusivo' or 'desenho universal', 'acessibilidade', 'mobilidade condicionada'; possibly 'barreiras'.
- Retrieval: status 403, 239 bytes, artefact ab768623070128cc.html, sha256 ab768623070128ccef048c88def86155dbe776c3d8db423cc8fa89432673d8a8, text 76 chars -> text/ab7686230701.txt

## E12
- Fetch: `https://www.metrolisboa.pt/institucional/?p=28217`
- Prior (written before the call): Operator press release; expect 'elevadores' (not 'ascensores') and 'acessibilidade plena', 'mobilidade reduzida'.
- Retrieval: status 403, 318 bytes, artefact b0c7e6712ecbf97a.html, sha256 b0c7e6712ecbf97a1e3a14f19e3aed5dbd6553f21a2852565bfc5518925713db, text 188 chars -> text/b0c7e6712ecb.txt

## E13
- Fetch: `https://www.cm-vfxira.pt/uploads/writer_file/document/10482/projeto_revisao_DL163-2006.pdf`
- Prior (written before the call): A government draft circulated for public consultation; not law. Expect the same 'ascensores' / 'plataformas elevatórias' and maybe new defined terms ('desenho universal', 'acessibilidade universal').
- Retrieval: status 200, 198011 bytes, artefact db850d2b44b4dcda.pdf, sha256 db850d2b44b4dcda9b0cd9e78c0d474e14c77871f473be6fdb09bc25151c13e8, text 77184 chars -> text/db850d2b44b4.txt

## W1. Wayback availability lookups (archive.org/wayback/available)
- Queries: umic.pt rcm9_2007.pdf; metrolisboa.pt ?p=28217; metrolisboa.pt/viajar/acessibilidade/; informacoeseservicos.lisboa.pt (parking page); inr.pt/acessibilidades.
- Prior: Lisbon and INR snapshots likely; Metro less likely.
- Result: snapshots for RCM 9/2007 (20260118134422), the Lisbon page (20260118103826) and INR (20260217145450); none for either Metro URL.

## E14
- Fetch: `https://web.archive.org/web/20260118134422if_/https://umic.pt/images/stories/publicacoes/rcm9_2007.pdf`
- Prior (written before the call): DR text of RCM 9/2007; per the search summary the annex says 'desenho para todos'; expect also 'design inclusivo' or 'desenho universal' and 'acessibilidade'.
- Retrieval: status None, 0 bytes, artefact e3b0c44298fc1c14.txt, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, text 0 chars -> text/e3b0c44298fc.txt

## E15
- Fetch: `https://web.archive.org/web/20260118103826if_/https://informacoeseservicos.lisboa.pt/servicos/detalhe/estacionamento-para-pessoa-com-mobilidade-condicionada`
- Prior (written before the call): Municipal page; expect 'lugar de estacionamento reservado' or 'lugar privativo', 'pessoa com mobilidade condicionada', 'cartão de estacionamento'; might be a JS app with no text.
- Retrieval: status None, 0 bytes, artefact e3b0c44298fc1c14.txt, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, text 0 chars -> text/e3b0c44298fc.txt

## E16
- Fetch: `https://web.archive.org/web/20260217145450if_/https://www.inr.pt/acessibilidades`
- Prior (written before the call): INR page; expect 'acessibilidade', 'desenho universal' or 'design inclusivo', and 'mobilidade condicionada'.
- Retrieval: status None, 0 bytes, artefact e3b0c44298fc1c14.txt, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, text 0 chars -> text/e3b0c44298fc.txt

## E16b
- Fetch: `https://web.archive.org/web/20260217145450/https://www.inr.pt/acessibilidades`
- Prior (written before the call): After the empty if_ result, the plain form; expect either the page or the same empty result (proxy reset).
- Retrieval: status None, 0 bytes, artefact e3b0c44298fc1c14.txt, sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855, text 0 chars -> text/e3b0c44298fc.txt

## E17
- Fetch: `https://www.inr.pt/acessibilidades`
- Prior (written before the call): Direct fetch after Wayback reset; INR (Instituto Nacional para a Reabilitação, I.P.) site may be a Liferay page with text. Expect 'acessibilidade', 'mobilidade condicionada', perhaps 'desenho universal'.
- Retrieval: status 200, 105703 bytes, artefact 7f49a872085ec781.html, sha256 7f49a872085ec781641b71b941e43b728b4512236a308f306f20465457794ab9, text 43842 chars -> text/7f49a872085e.txt

## E18
- Fetch: `https://umic.pt/images/stories/publicacoes/rcm9_2007.pdf`
- Prior (written before the call): Live host; may be gone (the snapshot is recent so possibly still live). Expect the DR text.
- Retrieval: status 404, 3716 bytes, artefact 65e702c0ca5f670d.html, sha256 65e702c0ca5f670de37031de3a3b49b924a6cc23eb29b7077c75c99a05079a8a, text 1000 chars -> text/65e702c0ca5f.txt

## E19
- Fetch: `https://portugal2030.pt/wp-content/uploads/sites/3/2023/03/rcm119_2021-1.pdf`
- Prior (written before the call): DR text; expect 'desenho universal', 'acessibilidade', perhaps 'design inclusivo' and 'barreiras arquitetónicas'; qualifier usage.
- Retrieval: status 200, 6393970 bytes, artefact b07b94fb8b61dd45.pdf, sha256 b07b94fb8b61dd45644db997692820360b4a92f28b84cea42eea920fdbc54f32, text 281791 chars -> text/b07b94fb8b61.txt

## E20
- Fetch: `https://www.emel.pt/fotos/editor2/regulamento-parque-azinhaga-cidade-11042025.pdf`
- Prior (written before the call): Operator regulation; expect 'lugares reservados a pessoas com mobilidade condicionada' or 'com deficiência' and 'cartão de estacionamento'.
- Retrieval: status 200, 740 bytes, artefact acf77c3737b1b1ff.html, sha256 acf77c3737b1b1ff935f30bd1e4f29456f23d9000052cccf010110e43e84a6be, text 22 chars -> text/acf77c3737b1.txt

## E21
- Fetch: `https://www.cm-odivelas.pt/cmodivelas/uploads/document/file/9729/regulamento_municipal_de_estacionamento_na_via_publica.pdf`
- Prior (written before the call): Municipal regulation; expect 'lugares de estacionamento privativos' or 'reservados' for 'pessoas com deficiência', perhaps 'dístico'.
- Retrieval: status 200, 2203843 bytes, artefact a4e1bceb125bb96d.pdf, sha256 a4e1bceb125bb96d5e6e2e31a10ca272c3f17b511c0d2d97aadf77ee6f713dc7, text 49295 chars -> text/a4e1bceb125b.txt

## E22
- Fetch: `https://www.escs.ipl.pt/sites/default/files/2023-10/como-e-quando-falar-da-deficiencia.pdf`
- Prior (written before the call): PT guide on language; expect it to reject 'deficiente' as a noun, 'portador de deficiência', 'pessoas com necessidades especiais' and possibly comment on 'lugar para deficientes' or 'acessível' vs 'adaptado'.
- Retrieval: status 200, 281719 bytes, artefact f9cffc92dcc51dc4.pdf, sha256 f9cffc92dcc51dc43789ef96b8deab6313473b4b8fe6b5eb363fedb48412bbcc, text 45913 chars -> text/f9cffc92dcc5.txt

## E23
- Fetch: `https://www.metrolisboa.pt/institucional/wp-content/uploads/sites/2/2018/11/96_PRRampas-Amoviveis.pdf`
- Prior (written before the call): Same host returned 403 for E12; a PDF under wp-content may also be blocked. If retrieved, expect 'rampas amovíveis', 'elevadores', 'mobilidade reduzida'.
- Retrieval: status 403, 318 bytes, artefact b0c7e6712ecbf97a.html, sha256 b0c7e6712ecbf97a1e3a14f19e3aed5dbd6553f21a2852565bfc5518925713db, text 188 chars -> text/b0c7e6712ecb.txt

## E24
- Fetch: `https://www.carris.pt/viaje/elevadores/`
- Prior (written before the call): URL path guessed; may 404. If retrieved, expect proper names 'Elevador de Santa Justa' (vertical lift) beside 'Elevador da Glória', 'da Bica', 'do Lavra' (funiculars): one word for two devices.
- Retrieval: status 404, 943 bytes, artefact 1bc05cd0d71db058.html, sha256 1bc05cd0d71db058f8e49824e75b5236884cd410b4aa74d28753afc0b7fd895a, text 43 chars -> text/1bc05cd0d71d.txt

## E25
- Fetch: `https://carris.pt/en/discover/fleet/funicular`
- Prior (written before the call): English page; useful only for its link to the Portuguese page and any Portuguese proper names ('Ascensor da Glória', 'Elevador de Santa Justa').
- Retrieval: status 200, 87311 bytes, artefact c632961bd309c200.html, sha256 c632961bd309c20006c17fd013e737895aaefb2ecab5270fc145577bff2204b0, text 1507 chars -> text/c632961bd309.txt

## E26
- Fetch: `https://carris.pt/descubra/frota/ascensores/`
- Prior (written before the call): Link found on the English page. Expect the section named 'Ascensores' covering the funiculars (Glória, Bica, Lavra), with Santa Justa called 'Elevador'; a JS app may leave little text.
- Retrieval: status 200, 100634 bytes, artefact a53002e801807374.html, sha256 a53002e801807374b045d5aae4dcd06fd6c895e40a5e54e9eadfc856d0c4d88c, text 1746 chars -> text/a53002e80180.txt

## Web searches (discovery only; nothing below is attestation)
Priors for these were written in working notes before each result; declared, not proven.
- Q1 `Decreto-Lei 307/2003 cartão de estacionamento pessoas com deficiência condicionadas na sua mobilidade pgdlisboa`. Prior: DR or PGDL copy. Result: imt.madeira.gov.pt PDFs of DL 307/2003 and DL 128/2017, Lisbon service page, Associação Salvador PDF, Provedor PDFs. Shape: statutory title words worked.
- Q2 `Regulamento de Sinalização do Trânsito Decreto Regulamentar 22-A/98 painel adicional deficientes estacionamento pgdlisboa`. Prior: annex with the panel. Result: madeira.gov.pt PDF of the 1998 original; BR results mixed in (CONTRAN), discarded as another jurisdiction.
- Q3 `pgdlisboa Código da Estrada "estacionamento" "pessoas com deficiência" artigo 50.º lei_mostra_articulado`. Prior: PGDL nid. Result: no PGDL URL; news and aggregator pages, not used. The nid=349 used in E5 is from memory and was confirmed by the page title.
- Q4 `Regulamento de Sinalização do Trânsito "Modelo 11d" OR "deficientes" ...`. Result: driving-school pages (not used) naming panel 11d; BR results discarded.
- Q5 `Decreto-Lei 320/2002 manutenção inspecção ascensores ...`. Result: vlex (aggregator, not used), municipal regulations; Marinha Grande chosen.
- Q6 `Metro de Lisboa acessibilidade estações elevadores ...`. Result: metrolisboa.pt press releases (403 on fetch), news (not used).
- Q7 `Plano Nacional de Promoção da Acessibilidade ... "desenho universal"`. Result: arquivo.pt and DR links; mostly BR pages, discarded. The search summary's "desenho para todos" is NOT recorded: the RCM 9/2007 bytes were never obtained.
- Q8 `Estratégia Nacional para a Inclusão ... 119/2021 ...`. Result: portugal2030.pt PDF.
- Q9 `Regulamento Geral de Estacionamento e Paragem na Via Pública Lisboa ...`. Result: EMEL PDFs, Odivelas regulation; the Lisbon RGEPVP text (Aviso 3856/2021) was not located.
- Q10 `"pessoa com deficiência" e não "deficiente" guia linguagem ...`. Prior: an APD or ACAPO guide. Result: mostly BR (discarded); one PT guide by Acesso Cultura (escs.ipl.pt host). No APD, ACAPO or CNOD guide found.
- Q11 `carris.pt Elevador de Santa Justa ...`. Result: carris.pt English fleet page; the Santa Justa = "Elevador" identification rests on search snippets only and is NOT recorded as attested.

## Result notes per fetch (the lines above each were written by tools/get.py)
- E2 DL 307/2003: text layer present; two-column layout breaks words at line ends, so quotes were cut short to avoid hyphen breaks. Forms: cartão de estacionamento de modelo comunitário; locais reservados para o efeito (art. 10.º); dístico de identificação de deficiente motor (preamble, revoked Portaria 878/81).
- E3 DL 128/2017: forms as expected; no 'dístico' in the text.
- E4 Lisbon page: 403 Cloudflare challenge ("Just a moment..."). Wayback snapshot exists (W1) but every Wayback fetch reset (E15, E16, E16b; control example.com 200): session-level block, as in CLAUDE.md section 7's CSA case. NOT OBTAINED.
- E5/E6 Código da Estrada: PGDL page is ISO-8859-1; re-extracted with tools/h2t.py. Page 1 ends at art. 97.º, page 2 runs to art. 189.º. Forms at arts 1.º q), 70.º n.º 4, 145.º q), 164.º n.º 2 g).
- E7 RST 1998 original: 29 MB PDF with a text layer; panel 11d "dístico de deficiente" at art. 46.º. Later amendments (DR 41/2002 ... DR 6/2019) not read, so the wording in force is UNVERIFIED.
- E8 Marinha Grande: scope list excludes 'funiculares' and 'elevadores de maquinaria de teatro'; 'plataforma' 0.
- E9 Salvador: one page; no rejected forms named.
- E10 Provedor: uses 'dístico de estacionamento' (2015) for the card.
- E11 arquivo.pt 403; E14 Wayback reset; E18 umic.pt 404. RCM 9/2007 NOT OBTAINED.
- E12, E23 metrolisboa.pt 403. NOT OBTAINED.
- E13 draft revision of DL 163/2006 (cm-vfxira host, not in force): 'elevador' 0, 'universal' 0, adds 'Ascensores incluídos em percursos acessíveis' and 'zonas de rotação'. Not used as attestation (a draft).
- E17 the inr.pt URL served the home page of the Instituto para os Direitos das Pessoas com Deficiência, I.P. (IDiPD); news items only; 'acesso universal à literatura' is not a built-environment use. Not used.
- E19 ENIPD: 'design universal' 2, 'desenho universal' 0, 'sem barreiras' 1; 'vagas' 6, all care-home or course places, none parking.
- E20 EMEL park regulation: 740-byte HTML stub, no PDF. NOT OBTAINED.
- E21 Odivelas: definitions at art. 4.º; request form in the annex.
- E22 Acesso Cultura: the Usar / Não usar table (pdf p. 39) is two columns; pdftotext -raw flattens it and misplaces "Casa de banho adaptada" into the wrong column; column membership was read from the -layout text.
- E24 carris.pt guessed path 404; E25 English page gave the link; E26 Portuguese page: menu 'Funiculares / Ascensores / Elevador', items 'Ascensor da Glória', 'Ascensor do Lavra'.

## L1. Local grep for held BR-tagged aliases in the PT texts read
- Query: counts of 'vaga', 'banheiro', 'elevador', 'desenho universal', 'design universal' over the 13 saved texts (read-only DB query for pt aliases on parking, lift, qualifier and sanitary stems gave 'banheiro acessível' BR, 'sanitário adaptado' BR, 'elevador acessível' BR, 'desenho universal' BR, 'vaga acessível' untagged).
- Prior: none of 'vaga', 'banheiro', 'desenho universal' in PT texts.
- Result: 'banheiro' 0 and 'desenho universal' 0 everywhere; 'vaga' 6, all in ENIPD and none in the parking sense; 'elevador' 3 (MG stage machinery 1, Carris 2), 0 in DL 163/2006. Shape: substring counts, used only to say "not attested by these texts".
