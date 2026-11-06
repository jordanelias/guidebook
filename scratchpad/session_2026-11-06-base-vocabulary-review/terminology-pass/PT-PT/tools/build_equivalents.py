"""Equivalents pass PT-PT: write equivalents.tsv and exit 1 if any quote or form is not found in its saved text.
Run from the PT-PT folder: python3 -I tools/build_equivalents.py
Matching: whitespace collapsed on both sides; nothing else is folded. Page numbers for PDFs are the
form-feed page of the first match in the saved pdftotext output."""
import csv, re, sys, pathlib
H = pathlib.Path(__file__).resolve().parent.parent
REG = H.parent.parent / 'register-v2' / 'concepts.tsv'
labels = {r['concept_id']: (r['label_en'] or r['origin_phrase']) for r in csv.DictReader(open(REG, encoding='utf-8'), delimiter='\t')}

# key: (title as written, issuer, jurisdiction, tier, URL, text file, is_pdf)
S = {
 'DL': ("Decreto-Lei n.º 163/2006, de 8 de Agosto (versão actualizada), with Anexo 'Normas técnicas para melhoria da acessibilidade das pessoas com mobilidade condicionada'", "Governo; host Procuradoria-Geral Regional de Lisboa (PGDL)", 'PT', '1',
        'https://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?nid=3110&tabela=leis&nversao=&so_miolo=', 'b54a68f15078.txt', 0),
 'PORT': ("Portaria n.º 301/2019, de 12 de setembro (secondary transcription)", "SE Inclusão das Pessoas com Deficiência and SE Habitação; host informador.pt", 'PT', '1',
        'https://informador.pt/legislacao/diploma/portaria-n-o-301-2019/', 'cdc065b2bfd5.txt', 0),
 'CE1': ("CÓDIGO DA ESTRADA (versão actualizada), 28ª versão (Lei n.º 24/2025, de 12/03), page 1", "Assembleia/Governo; host PGDL", 'PT', '2',
        'https://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?nid=349&tabela=leis&so_miolo=', '77a1b6761d1b.txt', 0),
 'CE2': ("CÓDIGO DA ESTRADA (versão actualizada), 28ª versão, page 2", "Assembleia/Governo; host PGDL", 'PT', '2',
        'https://www.pgdlisboa.pt/leis/lei_mostra_articulado.php?nid=349&tabela=leis&pagina=2&ficha=101&so_miolo=', '86e1e7861124.txt', 0),
 'D307': ("Decreto-Lei n.º 307/2003, de 10 de Dezembro, DR I Série-A N.º 284 (original 2003 text; amended by DL 17/2011, Lei 48/2017, DL 128/2017)", "Ministério da Administração Interna; host imt.madeira.gov.pt", 'PT', '2',
        'https://imt.madeira.gov.pt/images/Documentos%20Condutor/Decreto_Lei%20n307_2003%2010%20dezembro.pdf', '46145b1adc31.raw.txt', 1),
 'D128': ("Decreto-Lei n.º 128/2017, de 9 de outubro, DR 1.ª série N.º 194", "Trabalho, Solidariedade e Segurança Social; host imt.madeira.gov.pt", 'PT', '2',
        'https://imt.madeira.gov.pt/images/Documentos%20Veiculos/Distico/Decreto%20Lei%20128_2017_9out.pdf', '346a9653b597.raw.txt', 1),
 'ENIPD': ("Resolução do Conselho de Ministros n.º 119/2021 (ENIPD 2021-2025), DR 1.ª série", "Presidência do Conselho de Ministros; host portugal2030.pt", 'PT', '2',
        'https://portugal2030.pt/wp-content/uploads/sites/3/2023/03/rcm119_2021-1.pdf', 'b07b94fb8b61.raw.txt', 1),
 'RST': ("Decreto Regulamentar n.º 22-A/98 (Regulamento de Sinalização do Trânsito), DR I Série-B N.º 227, 1-10-1998 (original text; later amended, wording in force unverified)", "Governo; host madeira.gov.pt", 'PT', '3',
        'https://www.madeira.gov.pt//Portals/27/Documentos/Legislacao/1998_10_01_DecReg_22A_98_AprovaoRegulamentodeSinalizacaodoTransito_RST.pdf', 'a2177a5496fe.txt', 1),
 'MG': ("Regulamento municipal de manutenção e inspecção de ascensores, monta-cargas, escadas mecânicas e tapetes rolantes, DR 2.ª série N.º 63, 31-03-2008", "Câmara Municipal da Marinha Grande", 'PT (municipal)', '4',
        'https://www.cm-mgrande.pt/cmmgrande/uploads/document/file/3882/regulamento_municipal_de_manuten__o_e_inspe__o_de_ascensores__monta__cargas__escadas_mec_nicas_e_tapetes_rolantes.pdf', '4001b27cc771.raw.txt', 1),
 'ODV': ("Regulamento n.º 553/2023, Regulamento Municipal de Estacionamento na Via Pública, DR 2.ª série N.º 97", "Município de Odivelas", 'PT (municipal)', '4',
        'https://www.cm-odivelas.pt/cmodivelas/uploads/document/file/9729/regulamento_municipal_de_estacionamento_na_via_publica.pdf', 'a4e1bceb125b.raw.txt', 1),
 'PJ': ("Recomendação n.º 1/B/2015 (Proc. Q-6601/12)", "Provedor de Justiça", 'PT', '4',
        'https://www.provedor-jus.pt/documentos/Rec_1B2015.pdf', 'd70346d6040c.raw.txt', 1),
 'CAR': ("CARRIS, Descubra > Frota > Ascensores", "Companhia Carris de Ferro de Lisboa (Lisbon municipal transport operator)", 'PT (Lisboa)', '4',
        'https://carris.pt/descubra/frota/ascensores/', 'a53002e80180.txt', 0),
 'SALV': ("CARTÃO DE ESTACIONAMENTO PARA PESSOAS COM DEFICIÊNCIA", "Associação Salvador", 'PT', '5',
        'https://associacaosalvador.com/wp-content/uploads/2024/11/CARTAO-DE-ESTACIONAMENTO-PCDM-1.pdf', 'd3e2eee5fb4c.txt', 1),
 'AC': ("Como (e quando) falar da deficiência? Um guia para profissionais de comunicação cultural e jornalistas (2023)", "Acesso Cultura, Associação Cultural; text Dora Alexandre and Maria Vlachou, review Diana Niepce, Diana Santos, Joana Reais, Mia Meneses, Mickaella Dantas, Patrícia Carmo", 'PT', '5',
        'https://www.escs.ipl.pt/sites/default/files/2023-10/como-e-quando-falar-da-deficiencia.pdf', 'f9cffc92dcc5.txt', 1),
}
DLL = 'art. 26.º Anexo '
# (concept_id, form, usage_type, scope_note, source, locator, quote, conflation_note)
R = [
# ---- parking: R2-050 designated accessible spaces ----
('R2-050', 'lugares reservados para veículos em que um dos ocupantes seja uma pessoa com mobilidade condicionada', 'code term', 'keyed to a vehicle occupant with reduced mobility, not to an umbrella adjective', 'DL', DLL+'2.8.1', 'O número de lugares reservados para veículos em que um dos ocupantes seja uma pessoa com mobilidade condicionada', ''),
('R2-050', 'lugares de estacionamento reservados', 'code term', 'the short form the annex uses after 2.8.1', 'DL', DLL+'2.8.2', 'Os lugares de estacionamento reservados devem:', ''),
('R2-050', 'lugares de estacionamento reservado', 'regional variant', 'orthographic: adjective agrees with estacionamento, singular, same text', 'DL', DLL+'2.8.3', 'partilhada por dois lugares de estacionamento reservado contíguos', ''),
('R2-050', 'lugares de estacionamento reservados para pessoas com mobilidade condicionada', 'code term', 'the signage-clause form', 'DL', DLL+'4.14.1', 'lugares de estacionamento reservados para pessoas com mobilidade condicionada', ''),
('R2-050', 'lugares reservados para veículos de pessoa com mobilidade condicionada', 'code term', 'housing variant (3.2.6 relaxes the count)', 'DL', DLL+'3.2.6 1)', 'O número de lugares reservados para veículos de pessoa com mobilidade condicionada', ''),
('R2-050', 'lugar supletivo', 'code term', 'NARROWER: the reserved bay in residential common space', 'DL', DLL+'3.2.6 3)', 'devem constituir um lugar supletivo a localizar no espaço comum do edifício', ''),
('R2-050', 'lugar reservado a pessoa com deficiência condicionada na sua mobilidade', 'code term', 'road-law form; keyed to the DL 307/2003 permit; uses pessoa com deficiência, not mobilidade condicionada alone', 'CE2', 'art. 145.º, alínea q)', 'A paragem e o estacionamento em lugar reservado a pessoa com deficiência condicionada na sua mobilidade', ''),
('R2-050', 'reservados lugares ao estacionamento de veículos ... utilizados no transporte de pessoas com deficiência', 'code term', 'road-law form keyed to the vehicle that carries the person', 'CE1', 'art. 70.º, n.º 4', 'ser reservados lugares ao estacionamento de veículos afetos ao serviço de determinadas entidades ou utilizados no transporte de pessoas com deficiência', 'CONFLATION: one clause reserves bays for official vehicles and for vehicles carrying disabled people (art. 70.º n.º 4); the register keeps them apart'),
('R2-050', 'local destinado ao estacionamento de veículos ... utilizados no transporte de pessoas com deficiência', 'code term', 'removal clause; same carve as art. 70.º', 'CE2', 'art. 164.º, n.º 2, alínea g)', 'Em local destinado ao estacionamento de veículos de certas categorias, ao serviço de determinadas entidades ou utilizados no transporte de pessoas com deficiência', ''),
('R2-050', 'locais reservados para o efeito', 'code term', 'permit statute: the places where the card may be used', 'D307', 'art. 10.º', 'nos locais reservados para o efeito', ''),
('R2-050', 'lugar de estacionamento para pessoa com deficiência', 'code term', 'municipal application form; the person is defined as the card holder (art. 4.º)', 'ODV', 'Anexos, request form', 'O condicionamento de lugar de estacionamento para pessoa com deficiência:', 'CONFLATION: art. 4.º n.º 1 defines "Pessoa com deficiência" as the holder of the parking card, so the regulation equates the person with the permit'),
('R2-050', 'lugares ... Pessoas com deficiência, junto à sua residência ou local de trabalho', 'code term', 'NARROWER: a bay assigned to one person near home or work, usable by any card holder', 'ODV', 'art. 6.º, n.º 1, alínea c)', 'Pessoas com deficiência, junto à sua residência ou local de trabalho, podendo os lugares', ''),
('R2-050', 'estacionamento condicionado', 'code term', 'WIDER: any class of vehicle restricted by signage', 'ODV', 'art. 4.º, n.º 3', 'Estacionamento condicionado: zona afeta, por sinalização, ao estacionamento na via', 'CONFLATION (word): "condicionado" means restricted here, while "mobilidade condicionada" means reduced mobility; a search on "condicionado" mixes the two'),
('R2-050', 'lugares reservados', 'code term', 'ombudsman usage of the statutory short form', 'PJ', 'p. 3 (pdf)', 'lugares reservados', ''),
('R2-050', 'locais que lhe estão destinados', 'colloquial', 'DPO guide paraphrase of DL 307/2003 art. 1.º n.º 2', 'SALV', 'p. 1', 'sempre que este se encontre estacionado nos locais que lhe estão destinados', ''),
# parking permit forms (related; not the bay)
('R2-050', 'cartão de estacionamento de modelo comunitário para pessoas com deficiência', 'code term', 'DIFFERENT OBJECT: the permit, not the bay; PT bays are keyed to it (Código da Estrada art. 145.º q))', 'D128', 'art. 1.º', 'cartão de estacionamento de modelo comunitário para pessoas com deficiência', ''),
('R2-050', 'cartão de estacionamento para pessoas com deficiência', 'colloquial', 'DIFFERENT OBJECT: permit; the DPO uses the short title', 'SALV', 'p. 1 (title)', 'CARTÃO DE ESTACIONAMENTO PARA PESSOAS COM DEFICIÊNCIA', ''),
('R2-050', 'dístico de identificação de deficiente motor', 'outdated or disfavoured', 'DIFFERENT OBJECT: the pre-2003 permit (Portaria 878/81, revoked by DL 307/2003 art. 12.º); "deficiente motor" is a form the Acesso Cultura guide says not to use', 'D307', 'preamble, p. 1', 'foi aprovado o dístico de identificação de defi-', ''),
('R2-050', 'dístico de deficiente', 'outdated or disfavoured', 'DIFFERENT OBJECT: permit named on road sign panel model 11d; 1998 text, still in force as amended UNVERIFIED', 'RST', 'art. 46.º, p. 14 (pdf)', 'para veículos portadores do dístico de deficiente', ''),
('R2-050', 'dístico de estacionamento', 'outdated or disfavoured', 'the ombudsman uses the old word for the card in 2015', 'PJ', 'p. 5 (pdf)', 'a atribuição do dístico de estacionamento', 'CONFLATION: "dístico" (pre-2003 decal) and "cartão" (EU-model card) used for one permit'),
# ---- R2-281 Parking (setting) ----
('R2-281', 'Espaços para estacionamento de viaturas', 'code term', 'section heading', 'DL', DLL+'Secção 2.8', 'Secção 2.8 - Espaços para estacionamento de viaturas', ''),
('R2-281', 'Parques de estacionamento de veículos automóveis', 'code term', 'building type in scope', 'DL', 'art. 2.º, n.º 2, alínea i)', 'Parques de estacionamento de veículos automóveis', ''),
('R2-281', 'Espaços de estacionamento marginal à via pública', 'code term', 'NARROWER: on-street parking', 'DL', 'art. 2.º, n.º 2, alínea b)', 'Espaços de estacionamento marginal à via pública ou em parques de estacionamento público', ''),
# ---- qualifier: R2-333 Accessible ----
('R2-333', 'acessível / acessíveis', 'qualifier', 'the code umbrella word; PT applies it by designation: elements meeting the annex are "designados de acessíveis"', 'DL', DLL+'1.1.1; 2.1.1; 2.9.1', 'uma rede de percursos pedonais, designados de acessíveis', ''),
('R2-333', 'designados de acessíveis', 'code term', 'a defined-by-compliance construction: accessible means meeting the annex', 'DL', DLL+'2.9.1', 'designados de acessíveis', ''),
('R2-333', 'acessibilidades', 'qualifier', 'plural noun used as the domain name ("normas técnicas sobre acessibilidades", "plano de acessibilidades")', 'DL', 'art. 2.º, n.º 1', 'As normas técnicas sobre acessibilidades aplicam-se', ''),
('R2-333', 'mobilidade condicionada', 'qualifier', 'USER-GROUP qualifier, not an adjective of the object; the annex title and most parking forms carry it; the preamble defines it to include wheelchair users, people who cannot walk far, blind or deaf people, and temporarily the pregnant, children and older people', 'DL', 'preamble', 'fazem parte pessoas com mobilidade condicionada, isto é, pessoas em cadeiras de rodas', 'CONFLATION: one class word covers mobility, sensory and transient conditions (preamble)'),
('R2-333', 'mobilidade reduzida', 'qualifier', 'USER-GROUP qualifier; variant of mobilidade condicionada in the same decree', 'DL', 'art. 14.º, n.º 1', 'organizações não governamentais das pessoas com deficiência e de mobilidade reduzida', 'CONFLATION: art. 14.º uses "mobilidade reduzida" where arts 7.º and the annex use "mobilidade condicionada"; the Acesso Cultura guide lists them together (p. 39)'),
('R2-333', 'pessoas com mobilidade reduzida', 'qualifier', 'road law definition of vulnerable users', 'CE1', 'art. 1.º, alínea q)', 'pessoas com mobilidade reduzida ou pessoas com deficiência', ''),
('R2-333', 'pessoas com necessidades especiais', 'outdated or disfavoured', 'umbrella in the DL preamble; listed under "Não usar" by Acesso Cultura (p. 39)', 'DL', 'preamble', 'os direitos das pessoas com necessidades especiais', ''),
('R2-333', 'Pessoa com necessidades especiais', 'outdated or disfavoured', 'rejected form ("Não usar" column)', 'AC', 'p. 39', 'Pessoa com necessidades especiais', ''),
('R2-333', 'Pessoa com mobilidade condicionada/reduzida', 'qualifier', 'endorsed form ("Usar" column): the guide treats the two words as one', 'AC', 'p. 39', 'Pessoa com mobilidade', 'CONFLATION: condicionada and reduzida printed as one entry with a slash (p. 39)'),
('R2-333', 'design universal', 'qualifier', 'WIDER: a design principle, policy tier; absent from DL 163/2006 (grep "universal" 0)', 'ENIPD', 'objetivos; medida 2.1.2', 'a inclusão dos temas «acessibilidade» e «design universal» nos currículos académicos', ''),
('R2-333', 'sem barreiras', 'qualifier', 'WIDER: policy slogan ("Portugal sem barreiras à inclusão"), not a design qualifier', 'ENIPD', 'objetivos', 'um Portugal sem barreiras à inclusão', ''),
('R2-333', 'eliminação de barreiras urbanísticas e arquitectónicas', 'qualifier', 'the aim of the 1997 predecessor decree as the preamble names it', 'DL', 'preamble', 'visando a eliminação de barreiras urbanísticas e arquitectónicas', ''),
('R2-333', 'barreiras arquitetónicas', 'qualifier', 'post-1990 spelling (arquitetónicas) beside the DL\'s arquitectónicas', 'ENIPD', 'medida 2.2.1', 'eliminação de barreiras arquitetónicas', ''),
('R2-333', 'mobilidade sem condicionamentos', 'qualifier', 'preamble phrase for the aim', 'DL', 'preamble', 'garantindo-se assim a mobilidade sem condicionamentos', ''),
('R2-333', 'sociedade para todos', 'qualifier', 'WIDER: quoted from Lei 38/2004 art. 3.º d)', 'DL', 'preamble', 'a promoção de uma sociedade para todos através da eliminação de barreiras', ''),
('R2-333', 'inclusiva', 'qualifier', 'WIDER: general inclusion; used of society, not of an object', 'AC', 'p. 3', 'sociedade curiosa e inclusiva', ''),
('R2-333', 'adaptada', 'qualifier', 'endorsed beside acessível for a toilet ("Usar" column)', 'AC', 'p. 39', 'Casa de banho adaptada', 'CONFLATION: the guide lists "acessível" and "adaptada" as one usable pair (p. 39); the DL never uses "adaptada" for a toilet'),
('R2-333', 'dos deficientes', 'outdated or disfavoured', 'rejected ("Não usar") in "Casa de banho dos deficientes"; same rejection list carries "Deficiente" and "Deficiente motor"', 'AC', 'p. 39', 'Casa de banho dos deficientes', ''),
# ---- R2-208 pictogram ----
('R2-208', 'símbolo internacional de acessibilidade', 'code term', 'kept by art. 1.º n.º 3, specified in 4.14.3', 'DL', 'art. 1.º, n.º 3', 'Mantém-se o símbolo internacional de acessibilidade', ''),
('R2-208', 'símbolo de acessibilidade', 'code term', 'short form in the same clause as the long form', 'DL', DLL+'2.8.2 7)', 'por um sinal vertical com o símbolo de acessibilidade', ''),
('R2-208', 'figura estilizada de uma pessoa em cadeira de rodas', 'code term', 'the definition of the symbol', 'DL', DLL+'4.14.3', 'consiste numa figura estilizada de uma pessoa em cadeira de rodas', ''),
# ---- vertical transport ----
('R2-163', 'ascensores', 'code term', 'the car lift; section heading; "elevador" occurs 0 times in DL 163/2006', 'DL', DLL+'Secção 2.6', 'Secção 2.6 - Ascensores:', 'CONFLATION: Carris (Lisbon) names its funiculars "Ascensor" and its one vertical lift "Elevador" (row below); DL 163/2006 uses "ascensor" for the car lift'),
('R2-163', 'Ascensores de cabina', 'code term', 'explicitly the car type, against a stair platform (3.2.2 1))', 'DL', DLL+'3.2.2 2)', 'Ascensores de cabina que satisfaçam o especificado na secção 2.6', ''),
('R2-163', 'ascensor', 'code term', 'municipal lift-inspection usage, with "cabine" spelling', 'MG', 'art. 9.º? (n.º 4; pdf p. 2)', 'na cabine do ascensor', 'spelling: "cabine" here, "cabina" in DL 163/2006 2.6.2'),
('R2-163', 'elevadores de maquinaria de teatro', 'code term', 'DIFFERENT OBJECT: stage machinery, excluded from the lift rules; the one "elevador" in the regulation', 'MG', 'art. 1.º, n.º 2, alínea d)', 'Os elevadores de maquinaria de teatro', 'CONFLATION (word): "elevador" names stage machinery here and a passenger lift at Carris'),
('R2-163', 'Elevador', 'product name', 'Carris menu item for its single vertical lift (Santa Justa per search snippets, not read); proper-name usage', 'CAR', 'site menu (Frota)', 'Funiculares Ascensores Elevador', ''),
('R2-163', 'Ascensor da Glória', 'product name', 'DIFFERENT OBJECT: a funicular named "ascensor"', 'CAR', 'Frota > Ascensores', 'Ascensor da Glória (Encerrado temporariamente)', 'CONFLATION: "ascensor" = funicular in Lisbon proper names; the Marinha Grande regulation excludes "funiculares" from "ascensores" (art. 1.º n.º 2 a))'),
('R2-164', 'meios mecânicos de comunicação vertical', 'code term', 'the class over ascensores and plataformas elevatórias', 'DL', DLL+'3.2.1; 3.2.2', 'podem não ser instalados meios mecânicos de comunicação vertical alternativos às escadas', ''),
('R2-164', 'dispositivos mecânicos de elevação', 'code term', 'class word in the street chapter, with examples', 'DL', DLL+'1.7.2', 'dispositivos mecânicos de elevação (exemplos: ascensores, plataformas elevatórias)', ''),
('R2-164', 'instalações', 'code term', 'municipal collective term for lifts, goods lifts, escalators and moving walkways', 'MG', 'art. 1.º, n.º 1', 'designados abreviadamente por ins-', ''),
('R2-168', 'plataformas elevatórias', 'code term', 'section heading; sized for an adult in a wheelchair (2.7.1)', 'DL', DLL+'Secção 2.7', 'Secção 2.7 - Plataformas elevatórias:', ''),
('R2-168', 'plataforma elevatória', 'code term', 'singular form in the same section', 'DL', DLL+'2.7.4', 'Se o desnível entre a plataforma elevatória e o piso', ''),
('R2-169', 'Plataformas elevatórias de escada', 'code term', 'NARROWER: platform on a stair; the register "stair lift" may be a seat, not judged', 'DL', DLL+'3.2.2 1)', 'Plataformas elevatórias de escada ou outros meios mecânicos de comunicação vertical', ''),
('R2-169', 'plataformas elevatórias ... instaladas sobre escadas', 'code term', 'descriptive form, folding requirement', 'DL', DLL+'2.7.6', 'Caso as plataformas elevatórias sejam instaladas sobre escadas, devem ser rebatíveis', ''),
('R2-174', 'escadas mecânicas', 'code term', 'escalator; lift-inspection regime (DL 320/2002 as cited)', 'MG', 'art. 1.º, n.º 1', 'ascensores, monta-cargas, escadas mecânicas', ''),
('R2-175', 'tapetes rolantes', 'code term', 'moving walkway; same regime', 'MG', 'title', 'escadas mecânicas e tapetes rolantes', ''),
# ---- route, washroom, others (tier 1 second reading) ----
('R2-074', 'percurso acessível', 'code term', 'chapter heading; defined in buildings as one route designated accessible', 'DL', DLL+'Capítulo 4; 2.1.1', 'Capítulo 4 - Percurso acessível:', 'CONFLATION: the register splits Accessible route (R2-072) from Accessible path of travel (R2-074); PT has one phrase for both'),
('R2-074', 'rede de percursos pedonais', 'code term', 'BROADER: the street chapter regulates a network', 'DL', DLL+'1.1.1', 'servidas por uma rede de percursos pedonais', ''),
('R2-176', 'instalação sanitária', 'code term', 'room; the accessible items are the "aparelhos sanitários" inside it', 'DL', DLL+'2.9.1', 'numa instalação sanitária conjunta para pessoas com e sem limitações de mobilidade', ''),
('R2-176', 'instalação sanitária específica para pessoas com mobilidade condicionada', 'code term', 'NARROWER: the separate accessible room, may serve both sexes (2.9.2)', 'DL', DLL+'2.9.2', 'Se existir uma instalação sanitária específica para pessoas com mobilidade condicionada', ''),
('R2-176', 'instalações sanitárias de utilização geral acessíveis', 'code term', 'signage-clause form', 'DL', DLL+'4.14.1', 'instalações sanitárias de utilização geral acessíveis', ''),
('R2-176', 'Casa de banho acessível', 'colloquial', 'endorsed everyday form ("Usar"); "casa de banho" occurs 0 times in DL 163/2006', 'AC', 'p. 39', 'Casa de banho acessível', ''),
('R2-176', 'casa de banho adaptada', 'colloquial', 'used in the guide\'s own advice', 'AC', 'p. 31', 'com casa de banho adaptada', ''),
('R2-176', 'Casa de banho dos deficientes', 'outdated or disfavoured', 'rejected form ("Não usar"); kept because people search with it', 'AC', 'p. 39', 'Casa de banho dos deficientes', ''),
('R2-085', 'escadas', 'code term', 'in buildings (Secção 2.4)', 'DL', DLL+'Secção 2.4', 'Secção 2.4 - Escadas:', ''),
('R2-085', 'escadarias', 'code term', 'in the public way; a separate word from "escadas"', 'DL', DLL+'1.3.1', 'As escadarias na via pública devem satisfazer o especificado na secção 2.4', 'CARVE: "escadarias" (street) vs "escadas" (buildings), one object in two chapters'),
('R2-083', 'rampas', 'code term', 'defined by slope threshold (4.7.6, pass 1)', 'DL', DLL+'2.4.11', 'complementadas por rampas, ascensores ou plataformas elevatórias', ''),
('R2-358', 'escadarias em rampa', 'code term', 'lower-case listing form of the register origin phrase', 'DL', DLL+'1.1.3 2)', 'As escadarias, escadarias em rampa e rampas', ''),
('R2-057', 'passagens de peões', 'code term', 'pedestrian crossing; section 1.6 (not "passadeira", which the annex uses for a floor runner, 4.7.3)', 'DL', DLL+'1.6.1', 'A altura do lancil em toda a largura das passagens de peões', 'CONFLATION (word): in PT usage "passadeira" can name a zebra crossing; this text uses it only for a carpet runner (4.7.3)'),
('R2-092', 'lancil', 'code term', 'the kerb edge at crossings', 'DL', DLL+'1.6.1', 'A altura do lancil', ''),
('R2-005', 'vãos de porta', 'code term', 'the measured object is the opening', 'DL', DLL+'4.9.1', 'Os vãos de porta devem possuir uma largura útil', ''),
('R2-004', 'largura livre', 'code term', 'route and pavement width', 'DL', DLL+'1.2.1', 'devem ter uma largura livre não inferior a 1,5 m', ''),
('R2-021', 'zonas de manobra', 'code term', 'manoeuvring zones graded by rotation', 'DL', DLL+'4.4.1', 'as zonas de manobra devem ter dimensões', ''),
('R2-021', 'diâmetro das zonas de manobra', 'code term', 'existing-housing form: a diameter (secondary transcription)', 'PORT', 'Anexo, n.º 11', 'o diâmetro das zonas de manobra não deve ser inferior a 1,20 m', ''),
('R2-020', 'zona livre', 'code term', 'clear space for access and for remaining (permanência)', 'DL', DLL+'4.1.1', 'A zona livre para o acesso e a permanência de uma pessoa em cadeira de rodas', ''),
('R2-114', 'assento ... no interior da base de duche', 'code term', 'shower seat by description', 'DL', DLL+'2.9.8 2)', 'para um assento existente no interior da base de duche', ''),
('R2-089', 'barras de apoio', 'code term', 'DIFFERENT OBJECT from corrimãos: grab bars (also in lift cars, 2.6.2 4))', 'DL', DLL+'2.6.2 4)', 'Ter pelo menos uma barra de apoio colocada numa parede livre', 'register R2-089 is Handrails; "barra de apoio" is the grab bar, recorded here only to mark the carve'),
]
txt = {}
def norm(s): return re.sub(r'\s+', ' ', s).strip()
fails = 0; out = []
for cid, form, ut, scope, sk, loc, quote, conf in R:
    title, issuer, jur, tier, url, tf, pdf = S[sk]
    if tf not in txt:
        raw = (H / 'text' / tf).read_text(encoding='utf-8')
        txt[tf] = (raw, norm(raw))
    raw, n = txt[tf]
    ok = norm(quote) in n
    if not ok:
        fails += 1; print('QUOTE NOT FOUND', cid, sk, repr(quote)); continue
    if len(quote.split()) > 25: fails += 1; print('QUOTE > 25 WORDS', cid, quote)
    if pdf and 'p.' not in loc:
        pages = raw.split('\f')
        pg = next((i for i, p in enumerate(pages, 1) if norm(quote) in norm(p)), None)
        loc = f"{loc}; pdf p. {pg}" if pg else loc
    out.append([cid, labels.get(cid, ''), form, 'pt', jur, ut, scope, tier, f"{title} | {issuer} | {url}", loc, quote, conf])
with open(H / 'equivalents.tsv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t', lineterminator='\n')
    w.writerow(['concept_id', 'concept_label', 'form', 'language', 'jurisdiction', 'usage_type', 'scope_note', 'attestation_tier', 'source', 'locator', 'quote', 'conflation_note'])
    w.writerows(out)
print(f'{len(out)} rows written, {fails} failures')
sys.exit(1 if fails else 0)
