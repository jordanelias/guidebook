"""Build observations / coverage / reverse-harvest TSVs for the PT/PT terminology pass, verifying every
quote (after whitespace collapse) in the saved extracted text, and every phrase inside its quote.
Adapted from FR-FR/build.py. Run from the repository root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/PT-PT/build.py
Exits 1 if any quote or phrase fails to verify. Read-only apart from the TSVs in this folder."""
import re, sys, csv
D = 'scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/PT-PT'
INST = {
 # principal: consolidated current text (5th version, DL 10/2024; art. 12 and 21 also Lei 44/2026), PGDL host
 'L': ("Decreto-Lei n.º 163/2006, de 8 de Agosto (versão actualizada), com o Anexo 'Normas técnicas para melhoria da acessibilidade das pessoas com mobilidade condicionada'", D + '/text/b54a68f15078.txt'),
 # original Diário da República publication, used ONLY for table and figure labels the consolidated page omits ('(ver documento original)')
 'O': ("Decreto-Lei n.º 163/2006, Diário da República, 1.a série, N.o 152, 8 de Agosto de 2006 (original publication; tables and figure labels)", D + '/text/5b800bfbee2e.txt'),
 # secondary transcription (official DR text not obtained); flagged in every row
 'P': ("Portaria n.º 301/2019, de 12 de setembro (método de projeto, edifícios de habitação existentes) [transcription by informador.pt, NOT the Diário da República original]", D + '/text/cdc065b2bfd5.txt'),
}
def norm(s): return re.sub(r'\s+', ' ', s).strip()
TXT = {k: norm(open(v[1], encoding='utf-8').read()) for k, v in INST.items()}

ILL = "Well-illuminated (if site expected to be lit)|Well illuminated (if required for expected usage)"
SURF = "Surface is firm, stable and slip resistant|Floor surface is stable, firm, and non-slip|Surface is stable, firm, and slip resistant"
LAND = "Level landings with clear space|Level landings with clear space and at regular intervals"
HEAD = "Height clearance (if sheltered or parkade)|clearance|Headroom clearance (parameter 11)|Headroom and protruding objects (B651 4.5)|Headroom (B651 4.5.1)|height"

# (concepts '|'-separated, phrase verbatim, instrument, locator, quote verbatim, note)
OBS = [
 (ILL, "iluminação nocturna", "L", "Anexo 4.14.4", "pela colocação de barreiras devidamente sinalizadas por avisos, cores contrastantes e iluminação nocturna", "only lighting of barriers around works on accessible routes; no route lighting, no illuminance"),
 (SURF, "pisos e os seus revestimentos", "L", "Anexo 4.7.1", "Os pisos e os seus revestimentos devem ter uma superfície:", "the regulated object is floor + finish together"),
 (SURF, "Estável", "L", "Anexo 4.7.1 1)", "1) Estável - não se desloca quando sujeita às acções mecânicas decorrentes do uso normal;", "each property is defined in the text"),
 (SURF, "Firme", "L", "Anexo 4.7.1 3)", "3) Firme - não é deformável quando sujeito às acções mecânicas decorrentes do uso normal;", ""),
 (SURF, "boa aderência", "L", "Anexo 4.7.7 1)", "1) Garantir boa aderência mesmo na presença de humidade ou água;", "slip resistance stated as grip in wet conditions, for unenclosed and wet spaces only"),
 (SURF, "revestimento antiderrapante", "L", "Anexo 3.4.4", "As zonas pavimentadas adjacentes ao tanque da piscina, bem como as escadas e rampas de acesso, devem ter revestimento antiderrapante.", "pool surrounds"),
 (SURF, "superfície firme, segura e confortável", "P", "Anexo, Quadro 3, ação 13", "13. Alteração da estabilidade, conforto, segurança e/ou durabilidade dos revestimentos de pavimentos do percurso acessível.\nAdoção de materiais que apresentem uma superfície firme, segura e confortável.", "secondary transcription"),
 ("Seating", "banco", "L", "Anexo 2.10.4", "No interior dos vestiários e cabinas de prova deve existir um banco que satisfaça as seguintes condições:", "changing-room bench only"),
 ("Seating", "assento da base de duche", "L", "Anexo 2.9.11", "O assento da base de duche acessível deve satisfazer as seguintes condições:", "shower seat"),
 ("Handrails", "corrimãos", "L", "Anexo 2.4.8", "As escadas que vencerem desníveis superiores a 0,4 m devem possuir corrimãos de ambos os lados.", ""),
 ("Handrails", "duplo corrimão central", "L", "Anexo 1.5.1 1)", "Ter corrimãos de ambos os lados ou um duplo corrimão central, se a largura da rampa for superior a 3 m;", "a central double rail on wide public-way ramps and stairs"),
 ("Handrails", "elemento preênsil", "L", "Anexo 2.5.9", "o corrimão deve ter pelo menos um elemento preênsil a uma altura compreendida entre 0,85 m e 0,95 m", "the graspable member is named apart from the rail"),
 ("Handrails", "elemento preensível", "L", "Anexo 2.4.9 1)", "medida verticalmente entre o focinho dos degraus e o bordo superior do elemento preensível", "second spelling of the same member in the same text (2.4.9 vs 2.5.9)"),
 ("Clear width|width", "largura livre", "L", "Anexo 1.2.1", "Os passeios adjacentes a vias principais e vias distribuidoras devem ter uma largura livre não inferior a 1,5 m.", ""),
 ("Clear width|clearance", "canal de circulação", "L", "Anexo 4.3.1", "um canal de circulação contínuo e desimpedido de obstruções com uma largura não inferior a 1,2 m, medida ao nível do pavimento", "clear width is defined as a continuous unobstructed channel measured at pavement level"),
 ("Accessible path of travel", "Percurso acessível", "L", "Anexo, Capítulo 4", "Capítulo 4 - Percurso acessível:", "a whole chapter; also the heading of 1.1 and 2.1"),
 ("Accessible path of travel", "rede de percursos pedonais acessíveis", "L", "Anexo 1.1.2", "A rede de percursos pedonais acessíveis deve ser contínua e coerente", "in the public way the object is a network, not a route"),
 ("Drainage", "drenagem das águas pluviais", "L", "Anexo 1.8.2 1)", "Deve assegurar-se a drenagem das águas pluviais, através de disposições técnicas e construtivas que garantam o rápido escoamento e a secagem dos pavimentos", ""),
 ("Drainage", "drenagem superficial", "L", "Anexo 4.7.7 2)", "2) Ter boas qualidades de drenagem superficial e de secagem;", ""),
 ("Drainage", "sumidouros", "L", "Anexo 1.6.5 3)", "3) Ter os sumidouros implantados a montante das passagens de peões, de modo a evitar o fluxo de águas pluviais nesta zona.", "gully placement upstream of crossings"),
 ("Clear signage", "Sinalização e orientação", "L", "Anexo, Secção 4.14", "Secção 4.14 - Sinalização e orientação:", ""),
 ("Clear signage", "legibilidade", "L", "Anexo 4.14.5", "Para assegurar a legibilidade a sinalização deve possuir as seguintes características:", ""),
 ("Clear signage", "superfície anti-reflexo", "L", "Anexo 4.14.5 2)", "2) Ter uma superfície anti-reflexo;", ""),
 ("Audio accessibility and communication enhancement technologies", "sinal sonoro", "L", "Anexo 1.6.4 3)", "devem ser equipados com mecanismos complementares que emitam um sinal sonoro quando o sinal estiver verde para os peões", "audible crossing signal only"),
 ("Audio accessibility and communication enhancement technologies", "alerta luminoso e sonoro", "L", "Anexo 2.9.15 2)", "2) Deve disparar um alerta luminoso e sonoro;", "toilet alarm; no listening system, loop or amplification anywhere"),
 (LAND, "plataformas horizontais de descanso", "L", "Anexo 2.5.5", "As rampas devem possuir plataformas horizontais de descanso: na base e no topo de cada lanço", "the ramp landing is a 'rest platform'"),
 (LAND, "Patins intermédios", "L", "Anexo 2.4.2 2)", "2) Patins intermédios com uma profundidade, medida no sentido do movimento, não inferior a 0,7 m", "intermediate landing = patim; end landing = patamar"),
 ("Level landings with clear space", "Patamares superiores e inferiores", "L", "Anexo 2.4.2 1)", "1) Patamares superiores e inferiores com uma profundidade, medida no sentido do movimento, não inferior a 1,2 m", ""),
 ("Level landings with clear space and at regular intervals", "patins", "L", "Anexo 1.4.1 2)", "2) A projecção horizontal dos troços em rampa entre patins ou entre troços de nível não deve ser superior a 20 m.", "interval stated as a maximum horizontal projection between landings"),
 ("Clear space for approach", "zona livre", "L", "Anexo 4.1.1", "A zona livre para o acesso e a permanência de uma pessoa em cadeira de rodas deve ter dimensões que satisfaçam o definido em seguida:", "defined for access AND for remaining (permanência)"),
 ("Clear space for approach", "aproximação frontal ou lateral", "L", "Anexo 2.11.1 2)", "2) Deve existir uma zona livre que permita a aproximação frontal ou lateral de acordo com o especificado na secção 4.1;", ""),
 ("Clear space for approach", "Zonas de permanência", "L", "Anexo, Secção 4.1", "Secção 4.1 - Zonas de permanência:", "section heading"),
 ("Shelter", "cobertas", "L", "Anexo 3.5.1", "3.5.1 - As passagens exteriores entre edifícios devem ser cobertas.", "school and training buildings only"),
 ("Riser height and tread depth|tread|depth", "profundidade (cobertor)", "L", "Anexo 2.4.3 1)", "1) Uma profundidade (cobertor) não inferior a 0,28 m;", "tread is a depth, the element is the cobertor"),
 ("Riser height and tread depth|riser|height", "altura (espelho)", "L", "Anexo 2.4.3 2)", "2) Uma altura (espelho) não superior a 0,18 m;", "riser element = espelho"),
 ("Riser height and tread depth|tread", "Comprimento (cobertor)", "O", "Anexo 1.3.1 2), table", "Altura (espelho) Comprimento (cobertor)", "in the public-way stair table the tread is a LENGTH, not a depth"),
 ("Nosing design", "aresta do focinho boleada", "L", "Anexo 2.4.3 4)", "4) A aresta do focinho boleada com um raio de curvatura compreendido entre 0,005 m e 0,01 m;", "nosing = focinho"),
 ("Level threshold", "soleiras", "L", "Anexo 4.9.8", "Se nas portas existirem ressaltos de piso, calhas elevadas, batentes ou soleiras, não devem ter uma altura, medida relativamente ao piso adjacente, superior a 0,02 m.", "a capped upstand, not a 'level' threshold"),
 ("Level threshold", "ressaltos de soleira", "L", "Anexo 4.8.1", "As mudanças de nível abruptas devem ser evitadas (exemplos: ressaltos de soleira,", ""),
 (HEAD, "altura livre", "L", "Anexo 4.5.1", "A altura livre de obstruções em toda a largura dos percursos não deve ser inferior a 2 m nos espaços encerrados e 2,4 m nos espaços não encerrados.", "pedestrian headroom, two values by enclosed/unenclosed space; no vehicle or parkade clearance"),
 ("Headroom clearance (parameter 11)", "altura útil de passagem", "L", "Anexo 4.9.2", "Os vãos de porta devem ter uma altura útil de passagem não inferior a 2 m.", "door headroom is a separate quantity"),
 ("Edge protection", "elementos de protecção", "L", "Anexo 2.5.11", "devem ser ladeadas, em toda a sua extensão, de pelo menos um dos seguintes tipos de elementos de protecção: rebordos laterais com uma altura não inferior a 0,05 m", "a menu of five alternatives (rebordos, paredes/muretes, guardas, extensão lateral do pavimento, outras barreiras)"),
 ("Edge protection", "anteparos", "L", "Anexo 2.7.5", "devem possuir anteparos com uma altura não inferior a 0,1 m", "platform-lift edges"),
 ("Colour-contrasted and slip-resistant strip on nosing|Colour-contrasted and slip-resistant strip", "Faixas antiderrapantes e de sinalização visual", "L", "Anexo 2.4.3 5)", "5) Faixas antiderrapantes e de sinalização visual com uma largura não inferior a 0,04 m e encastradas junto ao focinho dos degraus.", "contrast is expressed as 'visual signalling', not colour"),
 ("Colour-contrasted and slip-resistant strip", "faixas com diferenciação de textura e cor contrastante", "L", "Anexo 2.5.10", "O revestimento de piso das rampas, no seu início e fim, deve ter faixas com diferenciação de textura e cor contrastante relativamente ao pavimento adjacente.", "texture + colour, not slip resistance"),
 ("Tactile attention indicators (truncated domes)", "sinalização táctil", "L", "Anexo 1.6.5 2)", "2) Ter o início e o fim assinalados no piso dos passeios por sinalização táctil;", "no profile (domes, bars) specified"),
 ("Tactile attention indicators (truncated domes)", "faixa de aproximação", "L", "Anexo 1.3.1 1)", "com uma faixa de aproximação constituída por um material de revestimento de textura diferente e cor contrastante com o restante piso", "warning band at stair heads defined by 'different texture'"),
 ("Slope|slope|gradient|Ramp gradient (parameter 3)", "inclinação", "L", "Anexo 2.5.1", "As rampas devem ter a menor inclinação possível", "one word for slope and gradient; a least-slope aim precedes the limits"),
 ("Slope|slope|gradient|Ramp gradient (parameter 3)", "inclinação nominal", "L", "Anexo 1.4.1 1)", "1) Os troços em rampa devem ter uma inclinação nominal não superior a 6/prct.", "'/prct.' is the PGDL page's rendering of %"),
 ("Slope|slope|gradient", "na direcção transversal ao percurso", "L", "Anexo 4.7.5 2)", "2) Não superior a 2/prct. na direcção transversal ao percurso.", "cross slope by direction phrase, no noun"),
 ("Slope|Ramp gradient (parameter 3)", "devem ser considerados rampas", "L", "Anexo 4.7.6", "Os troços de percursos pedonais com inclinação igual ou superior a 5/prct. devem ser considerados rampas", "a ramp is DEFINED by a slope threshold"),
 ("Sink faucet is easy to use or automatic", "monocomando", "L", "Anexo 2.9.17 5)", "5) As torneiras devem ser do tipo monocomando e accionadas por alavanca;", "lever single-control; no automatic tap"),
 ("Outlets and switches are at accessible heights", "comutadores de luz", "L", "Anexo 4.12.2", "Os botões de campainha, os comutadores de luz e os botões do sistema de comando dos ascensores e plataformas elevatórias devem ser indicados por dispositivo luminoso de presença", "switches yes; socket outlets ('tomada') 0 occurrences"),
 ("Accessible lockers", "cacifos", "L", "Anexo 3.4.2 1)", "Deve existir pelo menos um conjunto de cabides fixos e cacifos localizados de modo a permitir o alcance por uma pessoa em cadeira de rodas", "sports changing rooms"),
 ("Accessible door hardware", "dispositivos de operação das portas", "L", "Anexo 4.9.9", "Os puxadores, as fechaduras, os trincos e outros dispositivos de operação das portas devem oferecer uma resistência mínima", ""),
 ("Accessible door hardware", "puxadores em forma de maçaneta", "L", "Anexo 4.9.9", "os puxadores em forma de maçaneta não devem ser utilizados", "PT 'maçaneta' is the prohibited knob form; contrast the held BR seed 'maçaneta tipo alavanca'"),
 ("Accessible controls", "Comandos e controlos", "L", "Anexo, Secção 4.12", "Secção 4.12 - Comandos e controlos:", ""),
 ("Accessible controls", "dispositivos de comando", "L", "Anexo 2.6.5", "Os dispositivos de comando dos ascensores devem:", "lift controls"),
 ("height", "altura do piso", "L", "Anexo 2.9.4 1)", "A altura do piso ao bordo superior do assento da sanita deve ser de 0,45 m", "heights are 'floor to edge' with a stated tolerance"),
 ("level", "mudanças de nível", "L", "Anexo 4.8.2", "Se existirem mudanças de nível, devem ter um tratamento adequado à sua altura:", ""),
 ("level", "desnível", "L", "Anexo 2.5.1 1)", "Ter uma inclinação não superior a 6/prct., vencer um desnível não superior a 0,6 m e ter uma projecção horizontal não superior a 10 m;", "the rise a ramp 'overcomes' (vencer)"),
 ("level", "diferença de cotas", "L", "Anexo 3.2.1", "com uma diferença de cotas entre pisos utilizáveis não superior a 11,5 m", "level difference as a difference of elevations"),
 ("width|Door width (parameter 9)", "largura útil", "L", "Anexo 2.2.3", "As portas de entrada/saída dos edifícios e estabelecimentos devem ter um largura útil não inferior a 0,87 m", "entrance doors have their own width"),
 ("Door width (parameter 9)", "vãos de porta", "L", "Anexo 4.9.1", "Os vãos de porta devem possuir uma largura útil não inferior a 0,77 m, medida entre a face da folha da porta quando aberta e o batente ou guarnição do lado oposto", "the measured object is the opening (vão), not the door"),
 ("Door width (parameter 9)", "largura útil", "P", "Anexo, Quadro 3, ação 1", "Garantir os valores mínimos dimensionais de 0,77 m de largura útil e 2 m de altura útil.", "secondary transcription"),
 ("number", "número de lugares reservados", "L", "Anexo 2.8.1", "O número de lugares reservados para veículos em que um dos ocupantes seja uma pessoa com mobilidade condicionada", ""),
 ("force|Operating force (parameter 6)", "força necessária para operar", "L", "Anexo 4.9.13", "A força necessária para operar as portas interiores, puxando ou empurrando, não deve ser superior a 22 N", "interior doors; fire doors excepted"),
 ("force|Operating force (parameter 6)", "força", "L", "Anexo 4.12.1 4)", "4) Poder ser operados sem ser requerida uma força superior a 22 N;", "controls"),
 ("time", "tempo suficiente", "L", "Anexo 1.6.4 2)", "O sinal verde de travessia de peões deve estar aberto o tempo suficiente para permitir a travessia, a uma velocidade de 0,4 m/s", "time derived from a design walking speed"),
 ("size", "dimensões interiores", "L", "Anexo 2.6.2 1)", "Possuir cabinas com dimensões interiores, medidas entre os painéis da estrutura da cabina", ""),
 ("capacity", "lotação", "L", "Anexo 2.8.1 1)", "Um lugar em espaços de estacionamento com uma lotação não superior a 10 lugares;", "car-park capacity"),
 ("capacity", "capacidade", "L", "Anexo 3.6.1 1)", "Um lugar, no caso de salas ou recintos com uma capacidade até 25 lugares;", "seating capacity of halls"),
 ("distance", "distâncias de percurso", "L", "Anexo 1.1.5", "distâncias de percurso, medidas segundo o trajecto real no terreno", "route length relative to the most direct route"),
 ("ratio", "relação", "L", "Anexo 2.4.4", "se a relação de duas vezes a altura do espelho mais uma vez a profundidade do cobertor se mantiver constante", "the stair 2R+G relation"),
 ("ratio", "número total de cada aparelho instalado", "L", "Anexo 2.9.3", "devem representar pelo menos 10/prct. do número total de cada aparelho instalado e nunca inferior a um", "proportion of accessible fixtures"),
 ("Corridor width (parameter 4)", "corredores", "L", "Anexo 2.3.1", "Os patamares, galerias e corredores devem possuir uma largura não inferior a 1,2 m.", "corridors grouped with landings and galleries"),
 ("Corridor width (parameter 4)", "espaços de circulação horizontal", "L", "Anexo 3.3.2", "Os corredores e outros espaços de circulação horizontal das habitações devem ter uma largura não inferior a 1,1 m", "dwellings"),
 ("Turning circle (parameter 5)", "zona de manobra para rotação de 360º", "L", "Anexo 2.2.2", "Nos átrios interiores deve ser possível inscrever uma zona de manobra para rotação de 360º.", "a zone one must be able to 'inscribe', graded by rotation angle"),
 ("Turning circle (parameter 5)", "mudança de direcção de 180º em T", "L", "Anexo 2.3.3", "a rotação de 360º ou a mudança de direcção de 180º em T", ""),
 ("Turning circle (parameter 5)", "Rotação de 360°", "O", "Anexo 4.4.1, figure label", "Rotação de 360°", "figure label; also 'Rotação de 90°' and 'Rotação de 180°'"),
 ("Turning circle (parameter 5)", "diâmetro das zonas de manobra", "P", "Anexo n.º 8 b)", "O diâmetro das zonas de manobra não deve ser inferior a 1,20 m;", "secondary transcription; here the zone is a diameter"),
 ("LRV contrast (parameter 8)", "reflectância média", "L", "Anexo 4.7.2", "é recomendável que a reflectância média das superfícies dos revestimentos de piso nos espaços encerrados esteja compreendida entre 15/prct. e 40/prct.", "floor reflectance band, recommended; not a contrast quantity"),
 ("LRV contrast (parameter 8)", "cores que contrastem com o fundo", "L", "Anexo 4.14.5 3)", "3) Possuir caracteres e símbolos com cores que contrastem com o fundo;", "contrast unquantified"),
 ("Ramp run length (parameter 12)", "projecção horizontal", "L", "Anexo 2.5.1 1)", "Ter uma inclinação não superior a 6/prct., vencer um desnível não superior a 0,6 m e ter uma projecção horizontal não superior a 10 m;", "run = horizontal projection, tied to slope and rise in one triple"),
 ("Gratings (B651 4.4.4)", "grelhas, buracos ou frestas", "L", "Anexo 4.7.4", "Se existirem grelhas, buracos ou frestas no piso (exemplos: juntas de dilatação, aberturas de escoamento de água), os espaços não devem permitir a passagem de uma esfera rígida", "opening limit tested by a rigid sphere"),
 ("Protruding objects (B651 4.5.2)|Headroom and protruding objects (B651 4.5)", "Objectos salientes", "L", "Anexo, Secção 4.6", "Secção 4.6 - Objectos salientes:", ""),
 ("Lavatories (B651 6.2.3)", "lavatórios acessíveis", "L", "Anexo 2.9.13", "Os lavatórios acessíveis devem satisfazer as seguintes condições:", "lavatório = washbasin, same sense as B651"),
 ("Enclosures (B651 6.5.3)", "protecções de banheira", "L", "Anexo 2.9.18", "Caso existam, as protecções de banheira ou bases de duche acessíveis devem satisfazer as seguintes condições:", "bath/shower screens"),
 ("Landscaping elements (B651 8.7)", "Elementos vegetais", "L", "Anexo, Secção 4.13", "Secção 4.13 - Elementos vegetais:", "landscaping is plants only"),
 ("Vegetation (B651 8.7.3)", "elementos da vegetação", "L", "Anexo 4.13.4", "Os elementos da vegetação (exemplos: ramos pendentes de árvores, galhos projectados de arbustos)", ""),
 ("Scaffolding (B651 8.8.2)", "obras nos percursos acessíveis", "L", "Anexo 4.14.4", "Se existirem obras nos percursos acessíveis que prejudiquem as condições de acessibilidade definidas", "works on routes in general; scaffolding not named"),
]

REGISTER = [  # catalogue 2.1 (32), 2.2 (18), base parameters (10), B651 headings RHFAC does not name (15)
 "Well-illuminated (if site expected to be lit)", "Surface is firm, stable and slip resistant", "Seating", "Handrails", "Clear width",
 "Accessible path of travel", "Drainage", "Clear signage", "Audio accessibility and communication enhancement technologies",
 "Level landings with clear space", "Floor surface is stable, firm, and non-slip", "Clear space for approach",
 "Well illuminated (if required for expected usage)", "Surface is stable, firm, and slip resistant", "Shelter",
 "Riser height and tread depth", "Nosing design", "No open riser", "Level threshold", "Height clearance (if sheltered or parkade)",
 "Edge protection", "Colour-contrasted and slip-resistant strip on nosing", "Tactile attention indicators (truncated domes)", "Slope",
 "Sink faucet is easy to use or automatic", "Outlets and switches are at accessible heights", "Microwave mounting height accessible and safe",
 "Level landings with clear space and at regular intervals", "Colour-contrasted and slip-resistant strip", "Accessible lockers",
 "Accessible door hardware", "Accessible controls",
 "height", "level", "width", "clearance", "number", "slope", "depth", "riser", "tread", "force", "time", "gradient", "size", "volume",
 "capacity", "distance", "lighting levels", "ratio",
 "Ramp gradient (parameter 3)", "Corridor width (parameter 4)", "Turning circle (parameter 5)", "Operating force (parameter 6)",
 "Reverberation time (parameter 7)", "LRV contrast (parameter 8)", "Door width (parameter 9)", "Colour temperature (parameter 10)",
 "Headroom clearance (parameter 11)", "Ramp run length (parameter 12)",
 "Gratings (B651 4.4.4)", "Headroom and protruding objects (B651 4.5)", "Headroom (B651 4.5.1)", "Protruding objects (B651 4.5.2)",
 "Spouts (B651 6.1.2)", "Lavatories (B651 6.2.3)", "Enclosures (B651 6.5.3)", "Speed bumps (B651 8.3.8)", "Bollards (B651 8.3.9)",
 "Landscaping elements (B651 8.7)", "Flower or shrub planters (B651 8.7.1)", "Vegetation (B651 8.7.3)", "Guy wires (B651 8.7.4)",
 "Scaffolding (B651 8.8.2)", "Gradation limits (B651 D.6.1)",
]
PARTIAL = {  # concept -> why the PT match is not the English concept (ours)
 "Well-illuminated (if site expected to be lit)": "NARROWER: night lighting of works barriers only",
 "Well illuminated (if required for expected usage)": "NARROWER: night lighting of works barriers only",
 "Seating": "NARROWER: changing-room bench and shower seat; no rest seating on routes",
 "Audio accessibility and communication enhancement technologies": "NARROWER: audible crossing signal and toilet alarm only",
 "Shelter": "NARROWER: covered passages between school buildings only",
 "Height clearance (if sheltered or parkade)": "DIFFERENT OBJECT: pedestrian headroom; no vehicle/parkade clearance",
 "Tactile attention indicators (truncated domes)": "BROADER: 'sinalização táctil' and texture bands; no dome profile",
 "Outlets and switches are at accessible heights": "NARROWER: switches only; outlets 0",
 "capacity": "DIFFERENT SENSE: car-park and hall capacity, no lift capacity",
 "distance": "DIFFERENT SENSE: route length vs direct route; no distance markers",
 "ratio": "DIFFERENT SENSE: stair relation and fixture proportion; no room-type mix",
 "LRV contrast (parameter 8)": "PARTIAL: floor reflectance band (recommended) and unquantified contrast; no contrast quantity",
 "Scaffolding (B651 8.8.2)": "BROADER: works on routes, scaffolding not named",
}
ABSENT = {
 "No open riser": "no open-riser rule; 'espelho aberto' 0; 2.4.6 forbids projecting elements between riser and tread, a different rule",
 "Microwave mounting height accessible and safe": "'micro' 0 in all three texts; kitchens are treated only by turning zone and counter spacing (3.3.3)",
 "volume": "only 'grande volume de tráfego' (1.6.4 3)), traffic volume, a different sense; no speaker volume",
 "lighting levels": "'lux' occurs only inside 'fluxo'; no illuminance anywhere",
 "Reverberation time (parameter 7)": "'reverbera' 0; 'acústica' once, as 'acústica pelo menos equivalentes' for wheelchair seating (3.6.2 3))",
 "Colour temperature (parameter 10)": "'temperatura de cor' 0",
 "Spouts (B651 6.1.2)": "'bebedouro' 0; no drinking fountains",
 "Speed bumps (B651 8.3.8)": "'lomba' 0",
 "Bollards (B651 8.3.9)": "'pilarete' 0, 'baliza' 0",
 "Flower or shrub planters (B651 8.7.1)": "'floreira' 0; nearest is 'caldeiras das árvores' (tree pits, 4.13.1), a different object (see reverse harvest)",
 "Guy wires (B651 8.7.4)": "'espia'/'estai'/'tirante' not found ('estai' 0)",
 "Gradation limits (B651 D.6.1)": "no aggregate or surface gradation clause",
}

# Reverse harvest: (phrase verbatim, kind (ours), instrument, locator, quote verbatim, gloss — OURS, not the instrument's)
REV = [
 ("pessoas com mobilidade condicionada", "defined beneficiary category", "L", "preâmbulo", "Do conjunto das pessoas com necessidades especiais fazem parte pessoas com mobilidade condicionada, isto é, pessoas em cadeiras de rodas, pessoas incapazes de andar ou que não conseguem percorrer grandes distâncias, pessoas com dificuldades sensoriais", "the beneficiary class of the whole annex title; includes sensory, pregnancy, children, older people"),
 ("pessoas com necessidades especiais", "defined beneficiary category", "L", "preâmbulo", "pessoas com necessidades especiais, ou seja, pessoas que se confrontam com barreiras ambientais", "wider class containing the above"),
 ("produtos de apoio para a marcha", "defined beneficiary category", "P", "art. 1.º, 2", "utilizam cadeiras de rodas ou produtos de apoio para a marcha, como canadianas, andarilhos ou bengalas, as pessoas com dificuldades de coordenação motora", "the 2019 definition adds walking aids, coordination and 'baixa estatura'"),
 ("pessoas com baixa estatura", "defined beneficiary category", "P", "art. 1.º, 2", "as pessoas com baixa estatura", "short stature named"),
 ("barreiras urbanísticas e arquitectónicas", "doctrine term", "L", "preâmbulo", "visando a eliminação de barreiras urbanísticas e arquitectónicas nos edifícios públicos", ""),
 ("plano de acessibilidades", "compliance document", "L", "art. 3.º, 1", "devem ser instruídos com um plano de acessibilidades que apresente a rede de espaços e equipamentos acessíveis", "accessibility plan submitted with permit"),
 ("termo de responsabilidade", "compliance route", "L", "art. 3.º, 2", "Quando o plano de acessibilidades referido no número anterior seja acompanhado por termo de responsabilidade", "designer's declaration dispensing prior review"),
 ("símbolo internacional de acessibilidade", "defined element", "L", "art. 1.º, 3", "Mantém-se o símbolo internacional de acessibilidade, que consiste numa placa com uma figura em branco sobre um fundo azul, em tinta reflectora", ""),
 ("edifícios habitacionais e predominantemente habitacionais", "legal building category", "L", "art. 2.º, 3", "aplicam-se ainda aos edifícios habitacionais e predominantemente habitacionais", "50 % of area threshold"),
 ("desproporcionadamente difíceis", "exception ground", "L", "art. 10.º, 1", "quando as obras necessárias à sua execução sejam desproporcionadamente difíceis", ""),
 ("especial interesse histórico e arquitetónico", "exception route", "L", "art. 10.º, 8", "a edifícios e respetivos espaços circundantes que revistam especial interesse histórico e arquitetónico", "case-by-case with heritage authority opinion"),
 ("áreas privativas dos fogos", "housing carve", "L", "art. 23.º, 1", "no que respeita às áreas privativas dos fogos destinados a habitação de cada edifício", "phased share of dwellings (transitional)"),
 ("método de projeto", "compliance route (existing housing)", "L", "art. 9.º-A, 2", "As medidas definidas no método de projeto para a melhoria da acessibilidade das pessoas com mobilidade condicionada em edifícios de habitação existentes", ""),
 ("Escadarias em rampa", "element", "L", "Anexo, Secção 1.4", "Secção 1.4 - Escadarias em rampa na via pública:", "stepped ramp: ramped treads with steps; no register row"),
 ("desenvolvimento, medido entre o focinho de um degrau e a base do degrau seguinte", "quantity", "L", "Anexo 1.4.1 1)", "um desenvolvimento, medido entre o focinho de um degrau e a base do degrau seguinte, não inferior a 0,75 m", "going of a stepped-ramp tread"),
 ("Passagens de peões de superfície", "element", "L", "Anexo, Secção 1.6", "Secção 1.6 - Passagens de peões de superfície:", "at-grade crossings"),
 ("Passagens de peões desniveladas", "element", "L", "Anexo, Secção 1.7", "Secção 1.7 - Passagens de peões desniveladas:", "grade-separated crossings"),
 ("altura do lancil", "quantity", "L", "Anexo 1.6.1", "A altura do lancil em toda a largura das passagens de peões não deve ser superior a 0,02 m.", "kerb height at crossings"),
 ("rampeado", "technique", "L", "Anexo 1.6.2", "O pavimento do passeio na zona imediatamente adjacente à passagem de peões deve ser rampeado", "kerb ramping, stated by participle not by element name"),
 ("separadores centrais", "element", "L", "Anexo 1.6.3", "A zona de intercepção das passagens de peões com os separadores centrais das rodovias", "median refuge"),
 ("dispositivos semafóricos", "element", "L", "Anexo 1.6.4", "Caso as passagens de peões estejam dotadas de dispositivos semafóricos de controlo da circulação", ""),
 ("velocidade", "quantity", "L", "Anexo 1.6.4 2)", "a uma velocidade de 0,4 m/s", "design crossing speed"),
 ("dispositivos mecânicos de elevação", "element class", "L", "Anexo 1.7.2", "os desníveis devem ser vencidos por dispositivos mecânicos de elevação (exemplos: ascensores, plataformas elevatórias)", ""),
 ("Plataformas elevatórias", "element", "L", "Anexo, Secção 2.7", "Secção 2.7 - Plataformas elevatórias:", ""),
 ("precisão de paragem", "quantity", "L", "Anexo 2.6.2 2)", "Ter uma precisão de paragem relativamente ao nível do piso dos patamares", "lift levelling accuracy"),
 ("cortina de luz", "element", "L", "Anexo 2.6.4 3)", "Ter uma cortina de luz standard (com feixe plano) que imobilize as portas e o andamento da cabina.", "light curtain"),
 ("faixa de acesso lateral", "element", "L", "Anexo 2.8.2 2)", "Possuir uma faixa de acesso lateral com uma largura útil não inferior a 1 m;", "parking access aisle"),
 ("instalação sanitária específica para pessoas com mobilidade condicionada", "category", "L", "Anexo 2.9.2", "Se existir uma instalação sanitária específica para pessoas com mobilidade condicionada, esta pode servir para o sexo masculino e para o sexo feminino", "vs 'instalação sanitária conjunta' (2.9.1)"),
 ("for previsível um uso frequente", "usage-intensity category", "L", "Anexo 2.9.6", "Quando a sanita acessível estiver instalada numa cabina e for previsível um uso frequente por pessoas com mobilidade condicionada", "a second, larger tier triggered by foreseeable frequent use"),
 ("área de transferência", "space", "L", "Anexo 2.9.5 2)", "É recomendável a instalação de um lavatório acessível que não interfira com a área de transferência para a sanita;", ""),
 ("rebatíveis na vertical", "technique", "L", "Anexo 2.9.4 6)", "Se existirem barras de apoio lateral que sejam adjacentes à zona livre, devem ser rebatíveis na vertical;", "fold-up grab bars"),
 ("tanque de mochila", "element", "L", "Anexo 2.9.4 7)", "Quando se optar por acoplar um tanque de mochila à sanita", "close-coupled cistern"),
 ("bases de duche acessíveis", "element", "L", "Anexo 2.9.8", "As bases de duche acessíveis devem permitir pelo menos uma das seguintes formas de utilização por uma pessoa em cadeira de rodas:", "two modes: roll-in or transfer"),
 ("chuveiro deve ser do tipo telefone", "element", "L", "Anexo 2.9.17 4)", "O chuveiro deve ser do tipo telefone", "hand shower"),
 ("posição deitada no chão após uma queda", "design user state", "L", "Anexo 2.9.15 5)", "de modo a que possam ser alcançados por uma pessoa na posição deitada no chão após uma queda ou por uma pessoa em cadeira de rodas", "alarm reach from the floor after a fall"),
 ("Vestiários e cabinas de prova", "room type", "L", "Anexo, Secção 2.10", "Secção 2.10 - Vestiários e cabinas de prova:", ""),
 ("Equipamentos de auto-atendimento", "element", "L", "Anexo, Secção 2.11", "Secção 2.11 - Equipamentos de auto-atendimento:", "self-service machines"),
 ("referência táctil", "technique", "L", "Anexo 2.11.1 7)", "As teclas devem ser identificadas com referência táctil (exemplos: em alto-relevo ou braille).", ""),
 ("Balcões e guichés de atendimento", "element", "L", "Anexo, Secção 2.12", "Secção 2.12 - Balcões e guichés de atendimento:", ""),
 ("Telefones de uso público", "element", "L", "Anexo, Secção 2.13", "Secção 2.13 - Telefones de uso público:", ""),
 ("Bateria de receptáculos postais", "element", "L", "Anexo, Secção 2.14", "Secção 2.14 - Bateria de receptáculos postais:", "mailbox bank"),
 ("meios mecânicos de comunicação vertical", "element class", "L", "Anexo 3.2.1", "podem não ser instalados meios mecânicos de comunicação vertical alternativos às escadas", ""),
 ("instalados a posteriori", "provision-for-future technique", "L", "Anexo 3.2.2", "deve ser prevista no projecto a possibilidade de todos os pisos serem servidos por meios mecânicos de comunicação vertical instalados a posteriori", "designed-in future lift"),
 ("lugar supletivo", "housing carve", "L", "Anexo 3.2.6 3)", "devem constituir um lugar supletivo a localizar no espaço comum do edifício", ""),
 ("acesso à água por rampa ou por meios mecânicos", "element", "L", "Anexo 3.4.3", "Nas piscinas deve existir pelo menos um acesso à água por rampa ou por meios mecânicos", "pool entry"),
 ("lugares especialmente destinados a pessoas em cadeiras de rodas", "category", "L", "Anexo 3.6.1", "O número de lugares especialmente destinados a pessoas em cadeiras de rodas não deve ser inferior ao definido em seguida:", "wheelchair spectator spaces"),
 ("lugar para acompanhante", "category", "L", "Anexo 3.6.3", "deve estar junto de pelo menos um lugar para acompanhante sem limitações de mobilidade", "companion seat"),
 ("bomba acessível", "element", "L", "Anexo 3.7.1", "Em cada posto de abastecimento de combustível deve existir pelo menos uma bomba acessível", "fuel pump; with a service alternative"),
 ("Alcance", "space/quantity", "L", "Anexo, Secção 4.2", "Secção 4.2 - Alcance:", "reach ranges"),
 ("Alcance frontal", "figure label", "O", "Anexo 4.2.1, figure label", "Alcance frontal", "also 'sobre obstáculo' variants"),
 ("Recanto frontal", "figure label", "O", "Anexo 4.1.3, figure label", "Recanto frontal (quando D > 0,60 m)", "alcove condition; and 'Recanto lateral'"),
 ("espaço de manobra adicional", "space", "L", "Anexo 4.1.3", "deve existir um espaço de manobra adicional conforme definido em seguida:", "extra space when a clear space is in an alcove"),
 ("sem deslocamento", "manoeuvre category", "L", "Anexo 4.4.1", "mudanças de direcção de uma pessoa em cadeira de rodas sem deslocamento", "turning on the spot (rotação)"),
 ("com deslocamento", "manoeuvre category", "L", "Anexo 4.4.2", "mudanças de direcção de uma pessoa em cadeira de rodas com deslocamento", "turning while moving (mudança de direcção)"),
 ("Mudança de direcção de 90°", "figure label", "O", "Anexo 4.4.2, figure label", "Mudança de direcção de 90°", ""),
 ("espaços encerrados", "defined spatial category", "L", "Anexo 4.5.1", "não deve ser inferior a 2 m nos espaços encerrados e 2,4 m nos espaços não encerrados", "enclosed vs unenclosed; recurs in 4.7.2 and 4.7.7"),
 ("esfera rígida", "test object", "L", "Anexo 4.7.4", "os espaços não devem permitir a passagem de uma esfera rígida com um diâmetro superior a 0,02 m", ""),
 ("tapetes, passadeiras ou alcatifas", "element", "L", "Anexo 4.7.3", "Se forem utilizados tapetes, passadeiras ou alcatifas no revestimento do piso, devem ser fixos", "rugs, runners, carpet"),
 ("Contínua", "surface property", "L", "Anexo 4.7.1 4)", "4) Contínua - não possui juntas com uma profundidade superior a 0,005 m.", "continuity as a fourth surface property"),
 ("Durável", "surface property", "L", "Anexo 4.7.1 2)", "2) Durável - não é desgastável pela acção da chuva ou de lavagens frequentes;", "durability as a surface property"),
 ("bordo boleado ou chanfrado", "technique", "L", "Anexo 4.8.2 2)", "podem ser verticais com o bordo boleado ou chanfrado com uma inclinação não superior a 50/prct.;", "graded treatment of level changes by height"),
 ("portas giratórias, molinetes ou torniquetes", "element", "L", "Anexo 4.9.4", "Podem existir portas giratórias, molinetes ou torniquetes se existir uma porta ou passagem acessível, alternativa, contígua e em uso.", ""),
 ("barra horizontal", "element", "L", "Anexo 4.9.11", "Em portas de batente deve ser prevista a possibilidade de montar uma barra horizontal fixa", "pull bar on hinged doors"),
 ("marcas de segurança", "element", "L", "Anexo 4.9.14", "As portas e as paredes com grandes superfícies envidraçadas devem ter marcas de segurança que as tornem bem visíveis", "glazing manifestation"),
 ("Portas de movimento automático", "element", "L", "Anexo, Secção 4.10", "Secção 4.10 - Portas de movimento automático:", ""),
 ("dispositivo luminoso de presença", "technique", "L", "Anexo 4.12.2", "devem ser indicados por dispositivo luminoso de presença e possuir identificação táctil", "locator light on buttons"),
 ("caldeiras das árvores", "element", "L", "Anexo 4.13.1", "As caldeiras das árvores existentes nos percursos acessíveis e situadas ao nível do piso devem ser revestidas por grelhas de protecção", "tree pits"),
 ("com espinhos", "plant property", "L", "Anexo 4.13.3", "com espinhos ou que apresentem elementos contundentes; produtoras de substâncias tóxicas", "plant species exclusion"),
 ("identificação do número do piso", "element", "L", "Anexo 4.14.6", "Nos edifícios, a identificação do número do piso deve possuir as seguintes características:", "tactile floor numbers"),
 ("Caso um percurso não seja acessível, a sinalização deve indicá-lo", "signage rule", "L", "Anexo 4.14.2", "Caso um percurso não seja acessível, a sinalização deve indicá-lo.", "signing the inaccessible route"),
 ("É recomendável", "drafting register (recommendation)", "L", "Anexo 2.4.10", "É recomendável que não existam degraus isolados nem escadas constituídas por menos de três degraus", "the annex mixes obligations ('deve') and recommendations"),
 ("degrau de arranque", "element", "L", "Anexo 2.4.4", "O degrau de arranque pode ter dimensões do cobertor e do espelho diferentes", "first step"),
 ("rampas em curva", "element", "L", "Anexo 2.5.3", "Se existirem rampas em curva, o raio de curvatura não deve ser inferior a 3 m", ""),
 ("obras de alteração ou conservação", "compliance route (existing)", "L", "Anexo 2.5.2", "No caso de edifícios sujeitos a obras de alteração ou conservação, se as limitações de espaço impedirem a utilização de rampas com uma inclinação não superior a 8/prct.", "relaxed values by works type"),
 ("coincidir com o percurso dos restantes utilizadores", "doctrine rule", "L", "Anexo 2.1.3", "o percurso acessível deve coincidir com o percurso dos restantes utilizadores", "same route for everyone in new work"),
 ("legibilidade do espaço", "wayfinding technique", "L", "Anexo 1.8.2 2)", "Deve proporcionar-se a legibilidade do espaço, através da adopção de elementos e texturas de pavimento", "legibility of open spaces for people with visual impairment"),
 ("mobiliário urbano", "element", "L", "Anexo 4.3.2", "Devem incluir-se nas obstruções referidas no n.º 4.3.1 o mobiliário urbano, as árvores, as placas de sinalização, as bocas-de-incêndio", "obstruction list counted against clear width"),
 ("não afectada pelo movimento de abertura da porta", "space rule", "L", "Anexo 2.9.19 1)", "Deve ser possível inscrever uma zona de manobra, não afectada pelo movimento de abertura da porta de acesso, que permita rotação de 360º;", ""),
 ("Intervenção simples (N1)", "intervention level", "P", "Anexo n.º 2 a)", "a) Intervenção simples (N1): aquela que cumpre todos os critérios de classificação apresentados na coluna correspondente;", "secondary transcription; also N2 média, N3 profunda"),
 ("parcela acessível", "defined spatial category", "P", "Anexo n.º 4", "Entende-se por parcela acessível a parte do edifício ou da habitação constituída pelos percursos de acesso e pelos compartimentos essenciais à acessibilidade.", "secondary transcription"),
 ("compartimentos essenciais à acessibilidade", "defined category", "P", "Anexo n.º 5", "Entendem-se por compartimentos essenciais à acessibilidade:", "secondary transcription; kitchen, sanitary room, living room, bedroom by T-type"),
 ("Medidas de mitigação", "compliance route", "P", "Anexo n.º 6 a)", "a) Medidas de mitigação: medidas que, não atingindo o mesmo nível de desempenho em termos de acessibilidade", "secondary transcription"),
 ("Medidas de compensação", "compliance route (equivalent performance)", "P", "Anexo n.º 6 b)", "b) Medidas de compensação: medidas alternativas que proporcionam um desempenho equivalente ao disposto nas NTA", "secondary transcription"),
 ("comunicações verticais", "element class", "P", "Anexo, Quadro 1", "– Não altera a localização, forma ou dimensão das comunicações verticais da habitação ou do edifício.", "secondary transcription; and 'comunicações horizontais'"),
 ("Motivos de exclusão", "compliance route", "P", "Anexo, Quadro 3", "Motivos de exclusão", "secondary transcription"),
]

def main():
    bad = 0; rows = []
    for c, ph, ins, loc, q, note in OBS:
        ok = norm(q) in TXT[ins] and norm(ph).lower() in norm(q).lower()
        if not ok: bad += 1; print('FAIL', ins, loc, ph, norm(q) in TXT[ins], file=sys.stderr)
        for x in c.split('|'):
            if x not in REGISTER: bad += 1; print('UNKNOWN CONCEPT', x, file=sys.stderr)
        rows.append([c, ph, 'pt (PT)', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok else 'NO', note])
    with open(D + '/observations.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept (English register label; | = counts for each)', 'phrase_verbatim', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'note (ours)'])
        w.writerows(rows)
    with open(D + '/reverse-harvest.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['phrase_verbatim (instrument own phrase)', 'kind (ours)', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'gloss_OURS_not_an_equivalence'])
        for ph, kind, ins, loc, q, g in REV:
            ok = norm(q) in TXT[ins] and norm(ph).lower() in norm(q).lower()
            if not ok: bad += 1; print('REV FAIL', ins, loc, ph, norm(q) in TXT[ins], file=sys.stderr)
            w.writerow([ph, kind, 'pt (PT)', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok else 'NO', g])
    with open(D + '/coverage.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['register_concept', 'register_source', 'status', 'n_observations', 'phrases_found (distinct)', 'note'])
        for i, c in enumerate(REGISTER):
            src = 'catalogue 2.1' if i < 32 else 'catalogue 2.2' if i < 50 else 'base_parameters' if i < 60 else 'b651-headings (RHFAC-does-not-name)'
            hit = [r for r in rows if c in r[0].split('|')]
            if hit:
                st = 'FOUND-PARTIAL' if c in PARTIAL else 'FOUND'
                notes = '; '.join(sorted({r[8] for r in hit if r[8]}))
                w.writerow([c, src, st, len(hit), ' / '.join(sorted({r[1] for r in hit})), (PARTIAL[c] + '; ' if c in PARTIAL else '') + notes])
            else:
                if c not in ABSENT: bad += 1; print('NO ABSENT NOTE', c, file=sys.stderr)
                w.writerow([c, src, 'SEARCHED-ABSENT', 0, '', ABSENT.get(c, 'NO NOTE')])
    print('observations', len(rows), 'reverse-harvest', len(REV), 'failures', bad)
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
