"""Build observations / coverage / reverse-harvest TSVs for the ES/ES terminology pass, verifying every
quote (after whitespace collapse) in the saved extracted text. Adapted from FR-FR/build.py. Run from the
repository root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/ES-ES/build.py
Exits non-zero if any quote or phrase fails to verify. Read-only apart from the TSVs in this folder."""
import re, sys, csv
D = 'scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/ES-ES'
INST = {
 'SUA': ("Documento Básico SUA Seguridad de utilización y accesibilidad (CTE), articulado 14 junio 2022", D + '/text/3cfb5bbb135e8f02.txt'),
 'RD505': ("Real Decreto 505/2007, de 20 de abril, por el que se aprueban las condiciones básicas de accesibilidad y no discriminación de las personas con discapacidad para el acceso y utilización de los espacios públicos urbanizados y edificaciones", D + '/text/28c05a6de0c17ba7.txt'),
 'TMA': ("Orden TMA/851/2021, de 23 de julio, por la que se desarrolla el documento técnico de condiciones básicas de accesibilidad y no discriminación para el acceso y la utilización de los espacios públicos urbanizados", D + '/text/6c3b1865d0b18bd1.txt'),
 'RD707': ("Real Decreto 707/2026, de 2 de septiembre (Reglamento de las condiciones básicas de accesibilidad cognitiva)", D + '/text/320a3d263fa4b99d.txt'),
}
def norm(s): return re.sub(r'\s+', ' ', s).strip()
LOW = 'a-záéíóúüñ'
def dehyph(s):  # DB-SUA breaks words at line end with '-'; join only lower-case letter runs (DB-SUA texts only)
    return re.sub(r'(?<=[' + LOW + r'])-[ \t]*\n\s*(?=[' + LOW + r'])', '', s)
TXT = {k: norm((dehyph if k == 'SUA' else str)(open(v[1], encoding='utf-8').read())) for k, v in INST.items()}
DCC = norm(dehyph(open(D + '/text/1bc0a3fe0bdf78f2.txt', encoding='utf-8').read()))  # held DB-SUA con comentarios

L = 'Well-illuminated (if site expected to be lit)|Well illuminated (if required for expected usage)|lighting levels'
S = 'Surface is firm, stable and slip resistant|Floor surface is stable, firm, and non-slip|Surface is stable, firm, and slip resistant'
# (concepts '|'-separated, phrase verbatim, instrument, locator, quote verbatim, note)
OBS = [
 (L, "niveles de iluminación del recorrido", "TMA", "anexo art. 5.2 h)", "En todo su desarrollo se ajustarán los niveles de iluminación del recorrido a los especificados en el Real Decreto 1890/2008", "outdoor route lighting is delegated to the outdoor-lighting energy regulation, not stated here"),
 (L, "iluminación adecuada", "RD505", "anexo, Itinerario accesible", "El itinerario cuenta con iluminación adecuada y con la señalización que permita la localización de los accesos", ""),
 (L, "Alumbrado normal en zonas de circulación", "SUA", "SUA 4, 1", "Alumbrado normal en zonas de circulación", "lighting sits under a fall/impact SAFETY exigencia (SUA 4), not under SUA 9 accesibilidad"),
 (L, "iluminancia mínima", "SUA", "SUA 4, 1.1", "una iluminancia mínima de 20 lux en zonas exteriores y de 100 lux en zonas interiores", "quantity named 'iluminancia', defined in anejo A"),
 (L, "factor de uniformidad media", "SUA", "SUA 4, 1.1", "El factor de uniformidad media será del 40% como mínimo.", "a uniformity quantity the register lacks"),
 (S, "duro, estable", "TMA", "anexo art. 11.1", "El pavimento del itinerario peatonal accesible será duro, estable y cumplirá con la exigencia de resbaladicidad", "'duro' (hard), not 'firm'; slip resistance by cross-reference to DB-SUA"),
 (S, "resbaladicidad", "SUA", "SUA 1, 1", "Resbaladicidad de los suelos", "slip is a classed property ('clase' 0-3) by location, not a yes/no"),
 (S, "resistencia al deslizamiento Rd", "SUA", "SUA 1, 1.2", "Los suelos se clasifican, en función de su valor de resistencia al deslizamiento Rd", ""),
 (S, "resistentes a la deformación", "SUA", "anejo A, Itinerario accesible, Pavimento", "los suelos son resistentes a la deformación", "the firmness criterion is worded as resistance to deformation"),
 (S, "No contiene piezas ni elementos sueltos", "SUA", "anejo A, Itinerario accesible, Pavimento", "No contiene piezas ni elementos sueltos, tales como gravas o arenas.", "stability worded as absence of loose elements"),
 (S, "resistencia al deslizamiento", "RD505", "art. 12.1", "El pavimento tendrá una resistencia al deslizamiento que reduzca el riesgo de los resbalamientos.", ""),
 ("Seating", "Bancos y mesas de estancia", "TMA", "anexo art. 26", "Artículo 26. Bancos y mesas de estancia.", "outdoor benches, with seat depth, height, armrests and backrest"),
 ("Seating", "asientos convertibles", "RD505", "art. 6.3", "se dispondrán asientos convertibles, próximos a las vías de salida", "seating in assembly spaces"),
 ("Seating", "asientos de apoyo", "SUA", "anejo A, Servicios higiénicos accesibles, Duchas accesibles", "Dispone de barras de apoyo, mecanismos, accesorios y asientos de apoyo diferenciados cromáticamente del entorno", "shower and changing-room support seats (the table heading 'Asientos de apoyo en duchas y vestuarios' is split by the layout)"),
 ("Handrails", "pasamanos", "SUA", "SUA 1, 4.2.4.1", "Las escaleras que salven una altura mayor que 55 cm dispondrán de pasamanos al menos en un lado.", ""),
 ("Handrails", "pasamanos dobles", "TMA", "anexo art. 30.3 c)", "Se instalarán pasamanos dobles cuya altura de colocación estará comprendida", "double rail is the default outdoors"),
 ("Handrails", "barandilla", "SUA", "SUA 1, 4.1.4", "Dispondrán de barandilla en sus lados abiertos.", "'barandilla' is the guarding rail; 'pasamanos' the hand rail; the register's 'Handrails' maps to the second"),
 ("Clear width", "anchura libre de paso", "SUA", "anejo A, Itinerario accesible, Pasillos y pasos", "Anchura libre de paso ≥ 1,20 m.", ""),
 ("Clear width", "anchura útil", "SUA", "SUA 1, 4.2.2.4", "La anchura útil del tramo se determinará de acuerdo con las exigencias de evacuación", "stair/ramp width is 'anchura útil', set by evacuation, not by access"),
 ("Clear width", "ancho libre de paso", "TMA", "anexo art. 14.3", "respetando como mínimo un ancho libre de paso, a lo largo del mismo, de 1,80 m", "TMA alternates 'ancho' and 'anchura'"),
 ("Accessible path of travel", "itinerario accesible", "SUA", "anejo A, Itinerario accesible", "Itinerario accesible Itinerario que, considerando su utilización en ambos sentidos, cumple las condiciones que se establecen", "a DEFINED term carrying a bundle of conditions (levels, turning, widths, doors, floor, slope)"),
 ("Accessible path of travel", "itinerarios peatonales accesibles", "TMA", "anexo art. 5.1", "Se consideran itinerarios peatonales accesibles aquellos que garantizan el uso y la circulación de forma segura, cómoda, autónoma y continua de todas las personas.", "outdoor counterpart; a separate defined term"),
 ("Accessible path of travel", "Itinerario accesible a nivel", "RD505", "anexo", "Itinerario accesible a nivel: Itinerario predominantemente horizontal, que puede incluir desniveles, de altura no mayor que un peldaño", "RD505 splits the route into 'a nivel' and 'entre diferentes niveles'"),
 ("Drainage", "estancamientos de aguas", "TMA", "anexo art. 11.2", "sin ocasionar hundimientos ni estancamientos de aguas", "drainage worded as absence of ponding"),
 ("Drainage", "Impedirá la acumulación de agua", "TMA", "anexo art. 27 c)", "Impedirá la acumulación de agua.", "at drinking fountains"),
 ("Drainage|Gratings", "rejillas", "TMA", "anexo art. 12.1 a)", "Las rejillas y tapas de instalación se colocarán enrasadas con el pavimento circundante", ""),
 ("Drainage", "pendiente de evacuación", "SUA", "anejo A, aparatos sanitarios, Ducha", "Suelo enrasado con pendiente de evacuación ≤ 2%", "shower floor fall"),
 ("Drainage", "evitará el encharcamiento", "SUA", "SUA 6, 1.3", "su construcción evitará el encharcamiento", "pool surround"),
 ("Clear signage", "información y señalización para la accesibilidad", "SUA", "SUA 9, 2", "Condiciones y características de la información y señalización para la accesibilidad", ""),
 ("Clear signage", "señalización accesible", "RD707", "Reglamento art. 3 n)", "Señalización accesible: conjunto de elementos de texto, pictogramas, flechas y encaminamientos", "a defined term in the cognitive-accessibility regulation"),
 ("Clear signage", "Señalización visual y acústica", "TMA", "anexo art. 41", "Artículo 41. Señalización visual y acústica.", ""),
 ("Clear signage", "señalización direccional", "RD505", "art. 19.1", "mediante señalización direccional que garantice su lectura por peatones", "a held alias also found here, in this sense"),
 ("Audio accessibility and communication enhancement technologies", "bucle magnético", "SUA", "SUA 9, tabla 2.1", "Zonas dotadas con bucle magnético u otros sistemas", ""),
 ("Audio accessibility and communication enhancement technologies", "bucle de inducción", "SUA", "anejo A, Plaza reservada para personas con discapacidad auditiva", "Plaza que dispone de un sistema de mejora acústica proporcionado mediante bucle de inducción", ""),
 ("Audio accessibility and communication enhancement technologies", "sistema de mejora acústica", "SUA", "anejo A, Plaza reservada para personas con discapacidad auditiva", "Plaza que dispone de un sistema de mejora acústica", "the generic category; the loop is one instance"),
 ("Audio accessibility and communication enhancement technologies", "bucle de inducción magnética", "TMA", "anexo art. 16.6", "contará con un bucle de inducción magnética convenientemente señalizado", "in lift cars"),
 ("Level landings with clear space|Level landings with clear space and at regular intervals", "Mesetas", "SUA", "SUA 1, 4.3.3.1", "Las mesetas dispuestas entre los tramos de una rampa con la misma dirección tendrán al menos la anchura de la rampa", "the building code's word for a landing is 'meseta'"),
 ("Level landings with clear space|Level landings with clear space and at regular intervals", "rellanos", "TMA", "anexo art. 14.3", "Los rellanos situados entre tramos de una rampa sin cambio de dirección tendrán el mismo ancho que ésta", "the public-space order's word is 'rellano'; same object, two words"),
 ("Level landings with clear space", "superficie horizontal al principio y al final del tramo", "SUA", "SUA 1, 4.3.2.3", "dispondrán de una superficie horizontal al principio y al final del tramo", "top/bottom landing is a 'superficie horizontal', not a 'meseta'"),
 ("Level landings with clear space and at regular intervals", "longitud de 15 m como máximo", "SUA", "SUA 1, 4.3.2.1", "Los tramos tendrán una longitud de 15 m como máximo", "regular interval arises from a maximum 'tramo' length, not stated as an interval"),
 ("Clear space for approach", "espacio anejo de aproximación y transferencia", "SUA", "anejo A, Plaza de aparcamiento accesible", "Dispone de un espacio anejo de aproximación y transferencia", "approach and transfer are paired"),
 ("Clear space for approach", "espacio libre inferior", "SUA", "anejo A, Punto de atención accesible", "tiene un espacio libre inferior de 70 x 80 x 50 cm", "knee space under counters"),
 ("Clear space for approach", "zona de aproximación", "TMA", "anexo art. 26.2 c)", "un espacio libre de obstáculos o zona de aproximación donde pueda inscribirse un círculo", ""),
 ("Clear space for approach", "aproximación frontal", "SUA", "anejo A, Plaza reservada para usuarios de silla de ruedas", "en caso de aproximación frontal, y de 0,80 por 1,50 m como mínimo, en caso de aproximación lateral", "frontal vs lateral approach are distinct"),
 ("Shelter", "marquesinas de espera y refugio", "RD505", "art. 15.5", "Las marquesinas de espera y refugio en la vía pública deberán ser accesibles", "NARROWER: transit and street waiting shelters only"),
 ("Shelter", "marquesinas de espera del transporte público", "TMA", "anexo art. 36", "Los accesos, paradas y marquesinas de espera del transporte público se situarán próximas al itinerario peatonal accesible", "NARROWER"),
 ("Shelter", "preferiblemente en sombra", "TMA", "anexo art. 9.4", "deberá existir una superficie horizontal, preferiblemente en sombra", "beach access point; shade, not weather shelter"),
 ("Riser height and tread depth|riser|tread", "contrahuella", "SUA", "SUA 1, 4.2.1.1", "En tramos rectos o curvos la contrahuella medirá 13 cm como mínimo", "riser HEIGHT is the 'contrahuella'"),
 ("Riser height and tread depth|tread", "huella", "SUA", "SUA 1, 4.2.1.1", "En tramos rectos, la huella medirá 28 cm como mínimo.", ""),
 ("Riser height and tread depth", "2C + H", "SUA", "SUA 1, 4.2.1.1", "54 cm ≤ 2C + H ≤ 70 cm", "riser and tread are bound by a stride relation, not set separately"),
 ("Nosing design", "No se admite bocel", "SUA", "SUA 1, 4.2.1.2", "No se admite bocel.", "the nosing projection is prohibited outright"),
 ("Nosing design", "No se admitirá bocel", "TMA", "anexo art. 15.3 e)", "No se admitirá bocel.", ""),
 ("No open riser|riser", "tabicas", "SUA", "SUA 1, 4.2.1.2", "deben disponerse tabicas y éstas serán verticales o inclina", "the riser ELEMENT is 'tabica'; required only for ascending evacuation or where no accessible alternative exists"),
 ("No open riser", "escalones sin tabica", "SUA", "SUA 1, 4.1.3", "Podrán disponerse mesetas partidas con peldaños a 45º y escalones sin tabica.", "open risers are PERMITTED on restricted-use stairs"),
 ("No open riser", "sin pieza de tabica", "TMA", "anexo art. 15.3 b)", "No se admitirán escalones con discontinuidades en la huella o sin pieza de tabica", "prohibited outdoors"),
 ("Level threshold", "carecerán de desnivel en el umbral", "RD505", "art. 2.3", "carecerán de desnivel en el umbral", ""),
 ("Level threshold", "Carpintería enrasada con pavimento", "SUA", "anejo A, Vivienda accesible, Terraza", "Carpintería enrasada con pavimento o con resalto cercos ≤ 5 cm", "terrace door sill"),
 ("Height clearance (if sheltered or parkade)|clearance|Headroom clearance (parameter 11)|Headroom and protruding objects|Headroom", "altura libre de paso", "SUA", "SUA 2, 1.1.1", "La altura libre de paso en zonas de circulación será, como mínimo, 2,10 m en zonas de uso restrin", "headroom sits under impact SAFETY (SUA 2)"),
 ("Height clearance (if sheltered or parkade)", "gálibos y las alturas limitadas", "SUA", "SUA 7, 4.1", "tendrán señalizado además los gálibos y las alturas limitadas", "parking: signed vehicle clearances (vehicle sense)"),
 ("Headroom clearance (parameter 11)|Headroom", "altura libre de paso", "TMA", "anexo art. 5.2 c)", "En todo su desarrollo poseerá una altura libre de paso no inferior a 2,20 m.", ""),
 ("Edge protection", "barreras de protección", "SUA", "SUA 1, 3.1.1", "existirán barreras de protección en los desniveles, huecos y", "guarding against falls"),
 ("Edge protection", "zócalo o elemento de protección lateral", "SUA", "SUA 1, 4.3.4.2", "los bordes libres contarán con un zócalo o elemento de protección lateral de 10 cm de altura", "ramp kerb"),
 ("Edge protection", "Elementos de protección peatonal", "TMA", "anexo art. 30.1", "Se consideran elementos de protección peatonal las barandillas, los pasamanos, las vallas y los zócalos.", "a category that groups rails, guards, fences and kerbs"),
 ("Edge protection", "diferenciación visual y táctil", "SUA", "SUA 1, 3.1.2", "mediante diferenciación visual y táctil", "below the guarding threshold, edges are marked rather than guarded"),
 ("Colour-contrasted and slip-resistant strip on nosing", "banda de 5 cm de anchura enrasada en la huella", "TMA", "anexo art. 15.3 f)", "Cada escalón se señalizará en toda su longitud con una banda de 5 cm de anchura enrasada en la huella y situada a 3 cm del borde, que contrastará en textura y color con el pavimento del escalón.", "PARTIAL: contrast in texture and colour; slip resistance not stated for the band; set back 3 cm from the edge, not on the nosing"),
 ("Colour-contrasted and slip-resistant strip", "bandas señalizadoras visuales y táctiles", "SUA", "SUA 9, 2.2.4", "Las bandas señalizadoras visuales y táctiles serán de color contrastado con el pavimento", "PARTIAL: contrast and relief stated; slip resistance not stated for the strip"),
 ("Tactile attention indicators (truncated domes)", "Pavimento táctil indicador de advertencia", "TMA", "anexo art. 45.2 b)", "Pavimento táctil indicador de advertencia, para señalar proximidad a puntos de peligro o puntos de decisión.", "warning surface; paired with a 'direccional' (guidance) surface"),
 ("Tactile attention indicators (truncated domes)", "cúpula truncada", "TMA", "anexo art. 45.2 b)", "botones sin aristas vivas, de forma troncocónica, cúpula truncada o funcionalmente equivalente", ""),
 ("Tactile attention indicators (truncated domes)", "franja de pavimento visual y táctil", "SUA", "SUA 1, 4.2.3.4", "se dispondrá una franja de pavimento visual y táctil en el arranque de los tramos", "inside buildings the stair-start strip is GROOVED ('acanaladuras'), not domed"),
 ("Slope|slope|gradient|Ramp gradient (parameter 3)", "pendiente", "SUA", "SUA 1, 4.3.1.1", "Las rampas tendrán una pendiente del 12%, como máximo", ""),
 ("Slope|slope|gradient", "pendiente transversal", "SUA", "SUA 1, 4.3.1.2", "La pendiente transversal de las rampas que pertenezcan a itinerarios accesibles será del 2%", "cross slope is a named quantity"),
 ("Slope|slope|gradient|Ramp gradient (parameter 3)", "pendiente longitudinal máxima", "TMA", "anexo art. 14.2 c)", "La pendiente longitudinal máxima será del 10% para tramos de hasta 3,00 m de", ""),
 ("Ramp gradient (parameter 3)", "se consideran rampa", "SUA", "SUA 1, 4.3.1", "Los itinerarios cuya pendiente exceda del 4% se consideran rampa a efectos de este DB-SUA", "a ramp is DEFINED by a slope threshold; the outdoor order uses a different threshold"),
 ("Ramp gradient (parameter 3)", "planos inclinados con pendiente superior al 6%", "TMA", "anexo art. 14.1", "Se entiende por rampas vinculadas a un itinerario peatonal accesible los planos inclinados con pendiente superior al 6%", "outdoor ramp threshold differs from the building code"),
 ("Sink faucet is easy to use or automatic", "Grifería automática", "SUA", "anejo A, Mecanismos y accesorios", "Grifería automática dotada de un sistema de detección de presencia o manual de tipo monomando con palanca alargada de tipo gerontológico.", "'tipo gerontológico' lever"),
 ("Outlets and switches are at accessible heights", "tomas de corriente", "SUA", "anejo A, Mecanismos accesibles", "y entre 40 y 120 cm cuando sean tomas de corriente o de señal.", "outlets ('tomas de corriente') and controls ('elementos de mando y control') have separate height bands"),
 ("Outlets and switches are at accessible heights|Accessible controls", "elementos de mando y control", "SUA", "anejo A, Mecanismos accesibles", "cuando se trate de elementos de mando y control, y entre 40 y 120 cm cuando sean tomas de corriente o de señal.", ""),
 ("Accessible controls", "puño cerrado, codo y con una mano", "SUA", "anejo A, Mecanismos accesibles", "Los interruptores y los pulsadores de alarma son de fácil accionamiento mediante puño cerrado, codo y con una mano", "operability by closed fist or elbow"),
 ("Accessible controls", "No se admiten interruptores de giro y palanca", "SUA", "anejo A, Mecanismos accesibles", "No se admiten interruptores de giro y palanca.", ""),
 ("Accessible lockers", "taquillas", "SUA", "anejo A, Vestuario con elementos accesibles, Espacio de circulación", "taquillas, etc., anchura libre de paso ≥ 1,20 m", "PARTIAL: circulation width in locker areas ('espacios de taquillas', split by the layout) only; no locker reach or height rule"),
 ("Accessible door hardware", "Mecanismos de apertura y cierre", "SUA", "anejo A, Itinerario accesible, Puertas", "Mecanismos de apertura y cierre situados a una altura entre 0,80 - 1,20 m, de funciona", "pressure or lever, one-handed, or automatic"),
 ("Accessible door hardware", "maniobrables con una sola mano", "SUA", "anejo A, Vivienda accesible, Puertas", "presión o palanca y maniobrables con una sola mano, o son automáticos", ""),
 ("height", "altura", "SUA", "SUA 1, 4.2.4.4", "El pasamanos estará a una altura comprendida entre 90 y 110 cm.", ""),
 ("level", "desniveles", "SUA", "SUA 1, 2.1 b)", "Los desniveles que no excedan de 5 cm se resolverán con una pendiente", "'level' splits into 'nivel', 'desnivel', 'diferencia de cota', 'cota', 'rasante'"),
 ("level", "diferencia de cota", "SUA", "SUA 1, 3.1.1", "con una diferencia de cota mayor que 55 cm", ""),
 ("level", "diferencia de rasantes", "RD505", "art. 14.2", "la diferencia de rasantes entre la vía pública y la parcela", "level between plot and public way"),
 ("width", "anchura", "SUA", "SUA 1, 4.1.1", "La anchura de cada tramo será de 0,80 m, como mínimo.", ""),
 ("clearance", "espacio horizontal libre del barrido de las hojas", "SUA", "anejo A, Itinerario accesible, Puertas", "En ambas caras de las puertas existe un espacio horizontal libre del barrido de las hojas", "clear floor space is 'libre del barrido' (free of the door sweep)"),
 ("clearance", "Holgura para evitar atrapamientos", "SUA", "SUA 2, figura 2.1", "Holgura para evitar atrapamientos", "figure caption; 'holgura' is mechanical clearance"),
 ("number", "número", "SUA", "SUA 9, 1.2.2", "Número de alojamientos accesibles", "provision counts; table title"),
 ("depth", "profundidad", "SUA", "SUA 1, 4.2.3.3", "la profundidad de las mesetas en las que el", ""),
 ("depth", "fondo", "TMA", "anexo art. 46.2 a)", "su fondo será de entre 80 y 120 cm", "'fondo' is depth in the walking direction"),
 ("force|Operating force (parameter 6)", "fuerza de apertura", "SUA", "SUA 3, 1.3", "La fuerza de apertura de las puertas de salida será de 140 N, como máximo", ""),
 ("force|Operating force (parameter 6)", "fuerza de maniobra", "SUA", "SUA 3, 1.4", "Para determinar la fuerza de maniobra de apertura y cierre de las puertas de maniobra manual", "test method cited to a UNE-EN standard"),
 ("force", "fuerza horizontal", "SUA", "SUA 1, 3.2.2", "para resistir la fuerza horizontal establecida en el apartado 3.2.1 del Documento Básico SE-AE", "structural load on guarding: a different sense of 'force'"),
 ("time", "tiempo de paso", "RD505", "art. 13.4", "El tiempo de paso será el suficiente para garantizar el cruce completo de personas con movilidad reducida.", "pedestrian signal crossing time"),
 ("time", "tiempo de luz verde intermitente", "TMA", "anexo art. 23.5", "El tiempo de luz verde intermitente de los semáforos tendrá una duración que", ""),
 ("time", "iluminación con temporización", "SUA", "anejo A, Mecanismos accesibles", "No se admite iluminación con temporización en cabinas de aseos accesibles y vestuarios accesibles.", "timed lighting prohibited in accessible WCs"),
 ("size", "Tamaño de textos según la distancia", "TMA", "anexo art. 41.2 b)", "Tamaño de textos según la distancia", "letter height scaled to reading distance"),
 ("volume", "volumen", "TMA", "anexo art. 23.4", "su volumen estará permanentemente regulado según la intensidad del ruido ambiental", "signal volume tracking ambient noise; close to the RHFAC sense (speaker volume)"),
 ("capacity", "capacidad", "SUA", "SUA 7, 3.1", "En plantas de Aparcamiento con capacidad mayor que 200 vehículos", "DIFFERENT SENSE: car-park capacity, not lift capacity"),
 ("capacity", "capacidad suficiente", "RD505", "anexo, Zona de refugio", "con capacidad suficiente para que puedan acceder y situarse en ella sin dificultad personas en silla de ruedas", "refuge capacity"),
 ("distance", "ubicación y distancias", "TMA", "anexo art. 7.4", "incluirá, como mínimo, la información relativa a ubicación y distancias", "PARTIAL: distance information on park signage, nearest to trail-marker sense"),
 ("distance", "distancia", "SUA", "SUA 1, 4.2.3.4", "puertas situados a menos de 40 cm de distancia del primer peldaño", "spacing from a stair start"),
 ("ratio", "una plaza accesible por cada 33 plazas", "SUA", "SUA 9, 1.2.3.2 b)", "una plaza accesible por cada 33 plazas de aparcamiento o fracción", "PARTIAL: proportional provision ('por cada … o fracción'), no room-type mix"),
 ("ratio|LRV contrast (parameter 8)", "relación entre la luminancia", "SUA", "SUA 4, 2.4.1 c)", "La relación entre la luminancia Lblanca, y la luminancia Lcolor", "a luminance contrast ratio exists, but only for emergency safety signs"),
 ("LRV contrast (parameter 8)", "contraste cromático", "SUA", "anejo A, Mecanismos accesibles", "Tienen contraste cromático respecto del entorno.", "BROADER: contrast is required but never quantified for accessibility elements"),
 ("LRV contrast (parameter 8)", "contrastados cromáticamente", "SUA", "anejo A, Ascensor accesible", "La botonera incluye caracteres en Braille y en alto relieve, contrastados cromáticamente.", ""),
 ("Corridor width (parameter 4)", "Pasillos y pasos", "SUA", "anejo A, Itinerario accesible", "- Pasillos y pasos - Anchura libre de paso ≥ 1,20 m.", "corridor width is a row of the 'itinerario accesible' definition; 'pasillo' does occur"),
 ("Corridor width (parameter 4)", "Estrechamientos puntuales", "SUA", "anejo A, Itinerario accesible, Pasillos y pasos", "Estrechamientos puntuales de anchura ≥ 1,00 m, de longitud ≤ 0,50 m", "permitted local pinch points: a sub-quantity the register lacks"),
 ("Turning circle (parameter 5)", "Espacio para giro", "SUA", "anejo A, Itinerario accesible", "- Espacio para giro - Diámetro Ø 1,50 m libre de obstáculos en el vestíbulo de entrada", "located at specified places (entrance, corridor ends, lifts), not everywhere"),
 ("Turning circle (parameter 5)", "pueda inscribirse un círculo", "TMA", "anexo art. 8.4", "se preverán espacios libres de obstáculos donde pueda inscribirse un círculo de 1,50 m de diámetro mínimo", "outdoor wording: a circle that can be inscribed"),
 ("Door width (parameter 9)", "Anchura libre de paso", "SUA", "anejo A, Itinerario accesible, Puertas", "Anchura libre de paso ≥ 0,80 m medida en el marco y aportada por no más de una hoja.", "door width measured AT THE FRAME and also at maximum opening reduced by leaf thickness: two quantities"),
 ("Door width (parameter 9)", "reducida por el grosor de la hoja", "SUA", "anejo A, Itinerario accesible, Puertas", "la anchura libre de paso reducida por el grosor de la hoja de la puerta debe ser ≥ 0,78 m", ""),
 ("Ramp run length (parameter 12)", "longitud del tramo", "SUA", "SUA 1, 4.3.2.1", "en cuyo caso la longitud del tramo será de 9 m, como máximo", "run length belongs to the 'tramo'"),
 ("Ramp run length (parameter 12)", "longitud máxima en proyección horizontal", "TMA", "anexo art. 14.2 b)", "La longitud máxima en proyección horizontal será de 9,00 m.", "measured in horizontal projection"),
 ("Gratings", "Rejillas, tapas de instalación y alcorques", "TMA", "anexo art. 12", "Artículo 12. Rejillas, tapas de instalación y alcorques.", "gratings grouped with access covers and tree pits"),
 ("Protruding objects|Headroom and protruding objects", "elementos salientes", "SUA", "SUA 2, 1.1.3", "las paredes carecerán de elementos salientes que no arranquen del suelo", ""),
 ("Protruding objects|Headroom and protruding objects", "elementos volados", "SUA", "SUA 2, 1.1.4", "Se limitará el riesgo de impacto con elementos volados cuya altura sea menor que 2 m", "under-stair/ramp soffits; detection by cane named"),
 ("Spouts", "Fuentes de agua potable", "TMA", "anexo art. 27", "Artículo 27. Fuentes de agua potable.", "PARTIAL: drinking fountain treated as a whole; the outlet is 'grifo', no spout rule"),
 ("Lavatories", "Lavabo", "SUA", "anejo A, aparatos sanitarios", "- Lavabo - Espacio libre inferior mínimo de 70 (altura) x 50 (profundidad)", "lavatory is 'lavabo'"),
 ("Enclosures", "cerramientos de duchas y bañeras", "SUA", "SUA 2, 1.3.3", "Las partes vidriadas de puertas y de cerramientos de duchas y bañeras", "DIFFERENT PURPOSE: glazing impact safety, not accessibility of the enclosure"),
 ("Bollards", "Bolardos", "TMA", "anexo art. 29", "Artículo 29. Bolardos.", ""),
 ("Landscaping elements|Vegetation", "Vegetación", "TMA", "anexo art. 18", "Artículo 18. Vegetación.", ""),
 ("Vegetation", "La vegetación en la vía pública", "RD505", "art. 12.5", "La vegetación en la vía pública se dispondrá de manera que no se invada el espacio libre de paso.", ""),
 ("Scaffolding", "andamio", "TMA", "anexo art. 39.2", "Cuando el itinerario peatonal accesible discurra por debajo de un andamio o estructura provisional", ""),
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
 "Gratings", "Headroom and protruding objects", "Headroom", "Protruding objects", "Spouts", "Lavatories", "Enclosures",
 "Speed bumps", "Bollards", "Landscaping elements", "Flower or shrub planters", "Vegetation", "Guy wires", "Scaffolding", "Gradation limits",
]
PARTIAL = {  # concept -> why the Spanish match is not the English concept (ours)
 "Shelter": "NARROWER: transit/street waiting shelters ('marquesinas') and beach shade only; no building-entrance shelter",
 "Height clearance (if sheltered or parkade)": "PARTIAL: pedestrian headroom general; parking clearance only as signed vehicle 'gálibos'",
 "Colour-contrasted and slip-resistant strip on nosing": "PARTIAL: contrast in texture and colour; no slip rule for the band; set back from the edge",
 "Colour-contrasted and slip-resistant strip": "PARTIAL: colour contrast and relief; no slip rule for the strip",
 "Accessible lockers": "PARTIAL: only circulation width in locker areas",
 "capacity": "DIFFERENT SENSE: car-park and refuge capacity; no lift capacity",
 "distance": "PARTIAL: distance information on park signage; no trail distance markers as such",
 "ratio": "PARTIAL: proportional provision and luminance ratios; no room-type mix",
 "LRV contrast (parameter 8)": "BROADER: contrast required, never quantified for accessibility; a luminance ratio exists only for safety signs",
 "Spouts": "PARTIAL: drinking fountain as a whole; outlet is 'grifo'",
 "Enclosures": "DIFFERENT PURPOSE: glazing impact safety of shower/bath enclosures",
 "Landscaping elements": "PARTIAL: vegetation and tree pits only",
}
ABSENT = {
 "Microwave mounting height accessible and safe": "'microondas' 0 in all four texts; the kitchen of a 'vivienda accesible' carries worktop height and under-sink space only",
 "Reverberation time (parameter 7)": "'reverbera' 0/0/0/0; 'acústic' occurs only as signalling or 'sistema de mejora acústica'; acoustic design is not treated in these texts (any other CTE document NOT-READ)",
 "Colour temperature (parameter 10)": "'temperatura de color' 0, 'kelvin' 0; DB-SUA has colour RENDERING ('índice de rendimiento cromático Ra') for emergency lighting only",
 "Speed bumps": "'reductor' 0; SUA 7 regulates vehicle speed by signage only",
 "Flower or shrub planters": "'jardiner' 0, 'macet' 0; nearest is 'alcorques' (tree pits)",
 "Guy wires": "'viento' 0, 'tirante' 0",
 "Gradation limits": "no trail gradient gradation; beach routes are 'pasarelas' over sand (TMA art. 9.2 b)",
}

# Reverse harvest: (phrase verbatim, kind (ours), instrument, locator, quote verbatim, gloss -- OURS, not the instrument's)
REV = [
 ("Deambulación", "DALCO criterion", "RD707", "Reglamento art. 7.2 a)", "Deambulación: se refiere a la accesibilidad física y a la necesidad de comprender cuál es el camino", "first of the four DALCO criteria named in the regulation itself"),
 ("Aprehensión", "DALCO criterion", "RD707", "Reglamento art. 7.2 b)", "Aprehensión: hace referencia a la posibilidad de aprehender, agarrar y alcanzar los elementos manuales, visuales y auditivos", "reach and grasp extended to visual and auditory elements"),
 ("Localización", "DALCO criterion", "RD707", "Reglamento art. 7.2 c)", "Localización: posibilidad de las personas de poder determinar dónde se encuentran", "wayfinding as knowing where one is and how to get there"),
 ("Comunicación", "DALCO criterion", "RD707", "Reglamento art. 7.2 d)", "Comunicación: hace referencia a todos los procesos de emisión, intercambio y recepción de información", ""),
 ("Control de los estímulos sensoriales", "design principle", "RD707", "Reglamento art. 4.2 a) 7.º", "Control de los estímulos sensoriales: permite la personalización de la incidencia de los estímulos sensoriales", "sensory-load control as a design principle"),
 ("sobresaturación estimular", "design hazard", "TMA", "anexo art. 40.1", "evitando la sobresaturación estimular", "signage that overloads the senses"),
 ("Diseño de sistemas de orientación espacial", "defined technique", "RD707", "Reglamento art. 3 g)", "Diseño de sistemas de orientación espacial: se refiere al diseño de recursos y sistemas que permiten y facilitan los procesos de navegación y orientación en el entorno", ""),
 ("Dificultades cognitivas", "defined category (people)", "RD707", "Reglamento art. 3 e)", "Dificultades cognitivas: barreras que encuentra una persona en la comprensión, comunicación e interacción", "defined as barriers met, not as an impairment"),
 ("Lectura fácil", "defined technique", "RD707", "Reglamento art. 3 i)", "Lectura fácil: método que recoge un conjunto de pautas y recomendaciones relativas a la redacción de textos", "held alias 'lectura fácil' occurs here in this sense"),
 ("Lenguaje claro", "defined technique", "RD707", "Reglamento art. 3 j)", "Lenguaje claro: comunicación que prioriza a las personas lectoras", ""),
 ("Lenguaje sencillo", "defined technique", "RD707", "Reglamento art. 3 k)", "Lenguaje sencillo: es la comunicación que, transmitida en forma oral, escrita o ambas", "a third, lower register than lectura fácil and lenguaje claro"),
 ("Apoyos visuales", "defined technique", "RD707", "Reglamento art. 3 b)", "Apoyos visuales: cualquier elemento visual, como una imagen, objeto o gesto", ""),
 ("Tolerancia al error", "design principle", "RD707", "Reglamento art. 4.2 a) 5.º", "Tolerancia al error: deben reducirse las consecuencias de los errores en el uso", ""),
 ("Reducción del esfuerzo", "design principle", "RD707", "Reglamento art. 4.2 a) 6.º", "Reducción del esfuerzo: se emplea con un mínimo de fatiga psíquica y física", "names psychic as well as physical fatigue"),
 ("Acompañamiento", "planning criterion", "RD707", "Reglamento art. 7.2 j)", "Acompañamiento: se garantizará el acceso de los asistentes personales y otras personas de apoyo", "access for personal assistants"),
 ("Validación", "process principle", "RD707", "Reglamento art. 4.2 g)", "Validación: las medidas aquí contenidas estarán sometidas, cuando sea posible, a procesos de participación, verificación y seguimiento de su implementación y funcionamiento por parte de equipos especializados en los que participen personas con dificultades cognitivas.", "validation with participation of people with cognitive difficulties (a Co-1-shaped requirement)"),
 ("Pavimento táctil indicador direccional", "element", "TMA", "anexo art. 45.2 a)", "Pavimento táctil indicador direccional, para señalar encaminamiento o guía, así como proximidad a elementos para el cambio de nivel.", "the guidance surface is also the stair/ramp warning, not the warning surface"),
 ("franja-guía", "element", "TMA", "anexo art. 46.1", "su desarrollo deberá señalizarse mediante una franja-guía longitudinal de pavimento táctil indicador direccional", "a guidance strip where no building line exists"),
 ("línea de fachada o referencia edificada", "orientation reference", "TMA", "anexo art. 5.2 a)", "Discurrirá de manera colindante a la línea de fachada o referencia edificada a nivel del suelo.", "the building face as the default shoreline"),
 ("puntos de decisión", "element", "TMA", "anexo art. 46.7", "Para señalar cruces o puntos de decisión", ""),
 ("Vados peatonales", "element", "TMA", "anexo art. 20", "Artículo 20. Vados peatonales.", "kerb ramp: not a 'rampa' at all; separately defined"),
 ("vados vehiculares", "element", "TMA", "anexo art. 13", "Los vados vehiculares no alterarán las condiciones generales de los itinerarios", ""),
 ("Isletas de refugio", "element", "TMA", "anexo art. 22", "Artículo 22. Isletas de refugio.", "pedestrian refuge island"),
 ("plataforma única", "defined route type", "TMA", "anexo art. 5.3", "En las zonas de plataforma única, donde el itinerario peatonal accesible y la calzada estén a un mismo nivel", "shared surface street"),
 ("contrapendiente", "quantity", "TMA", "anexo art. 20.7", "La calzada en la zona de encuentro con el vado tendrá una contrapendiente máxima del 2%.", "counter-slope of the carriageway at a kerb ramp"),
 ("velocidad máxima de paso peatonal", "quantity", "TMA", "anexo art. 23.6", "desde el supuesto de una velocidad máxima de paso peatonal de 0,50 m/s", "walking speed as a design assumption"),
 ("avisador acústico", "element", "TMA", "anexo art. 23.2", "dispondrán de avisador acústico que emita una señal de cruce", "accessible pedestrian signal"),
 ("sistema de vibración integrado", "element", "TMA", "anexo art. 23.2 a)", "dispondrán de un sistema de vibración integrado", "vibrating push button"),
 ("Áreas de descanso", "space type", "TMA", "anexo art. 6", "Artículo 6. Áreas de descanso y áreas con presencia de espectadores.", ""),
 ("áreas con presencia de espectadores", "space type", "TMA", "anexo art. 6", "áreas con presencia de espectadores", ""),
 ("Área de estancia", "defined space type", "TMA", "anexo art. 4 c)", "Área de estancia: la parte de la zona de uso peatonal", "where people stay for a time, distinct from passage"),
 ("Zona de uso peatonal", "defined space type", "TMA", "anexo art. 4 a)", "Zona de uso peatonal: todo espacio público urbanizado destinado de forma permanente al tránsito o estancia peatonal.", ""),
 ("Sectores de juegos infantiles y de ejercicios", "space type", "TMA", "anexo art. 8", "Artículo 8. Sectores de juegos infantiles y de ejercicios.", "play and exercise equipment, one in five accessible"),
 ("tipo dinámico o que genere movimiento", "provision rule", "TMA", "anexo art. 8.1", "de tipo dinámico o que genere movimiento al introducirse en su interior", "the accessible play element must give motion"),
 ("Tramos urbanos de las playas", "space type", "TMA", "anexo art. 9", "Artículo 9. Tramos urbanos de las playas.", "urban beaches as regulated public space"),
 ("puntos accesibles", "element", "TMA", "anexo art. 9.1", "deberán disponer de puntos accesibles", "beach access points"),
 ("coeficiente de transmisión térmica", "quantity", "TMA", "anexo art. 9.2 b)", "materiales que posean un coeficiente de transmisión térmica y condiciones de continuidad adecuados para caminar descalzo", "boardwalk surface temperature for bare feet"),
 ("Urbanización de frentes de parcela", "element", "TMA", "anexo cap. VII", "Urbanización de frentes de parcela", "plot frontage: level differences resolved inside the plot"),
 ("Papeleras y contenedores", "element", "TMA", "anexo art. 28", "Artículo 28. Papeleras y contenedores para depósito y recogida de residuos.", "bins and waste containers with mouth heights"),
 ("sistema de cierre será retardado", "element property", "TMA", "anexo art. 28 b)", "el sistema de cierre será retardado", "delayed-closing lid"),
 ("Mesas de estancia", "element", "TMA", "anexo art. 26.2", "El diseño de las mesas de estancia ubicadas en las zonas de uso peatonal", ""),
 ("Espacios reservados al tránsito de bicicletas y vehículos de movilidad personal", "space type", "TMA", "anexo art. 38", "Artículo 38. Espacios reservados al tránsito de bicicletas y vehículos de movilidad personal.", "segregation of cycles and e-scooters"),
 ("zona ergonómica de interacción del brazo", "defined zone", "TMA", "anexo art. 44.1", "zona ergonómica de interacción del brazo", "reach zone for tactile signs"),
 ("mapas, planos o maquetas táctiles", "element", "TMA", "anexo art. 44.2", "Los mapas, planos o maquetas táctiles", ""),
 ("Símbolo de accesibilidad para la movilidad", "element", "TMA", "anexo art. 43", "Artículo 43. Aplicaciones del Símbolo de accesibilidad para la movilidad.", "the ISA under its UNE name, 'para la movilidad'"),
 ("fuentes tipo palo seco", "technique", "TMA", "anexo art. 41.2 a)", "Se utilizarán fuentes tipo palo seco", "sans-serif type"),
 ("Plazas de aparcamiento reservadas para personas con movilidad reducida", "element", "TMA", "anexo art. 35", "Artículo 35. Plazas de aparcamiento reservadas para personas con movilidad reducida.", ""),
 ("tarjeta de estacionamiento para personas con discapacidad", "legal category", "TMA", "anexo art. 35.1", "titulares de la tarjeta de estacionamiento para personas con discapacidad", ""),
 ("zona de aproximación y transferencia lateral", "element", "TMA", "anexo art. 35.3", "dispondrán de una zona de aproximación y transferencia lateral", ""),
 ("Andenes móviles y escaleras mecánicas", "element", "TMA", "anexo art. 17", "Artículo 17. Andenes móviles y escaleras mecánicas.", "moving walks: complementary, never part of the accessible route"),
 ("elementos complementarios", "classification", "TMA", "anexo art. 15.1", "Las escaleras no forman parte de los itinerarios peatonales accesibles, pero se consideran elementos complementarios a los mismos.", "stairs are outside the accessible route by definition"),
 ("ajustes razonables", "legal category", "RD505", "disp. final quinta", "existentes que sean susceptibles de ajustes razonables", "the duty for existing buildings is framed as reasonable adjustment"),
 ("soluciones alternativas", "compliance route", "SUA", "Introducción III", "se podrán aplicar aquellas soluciones alternativas que permitan la mayor adecuación", "existing buildings: alternative solutions with 'mayor adecuación posible'"),
 ("otras soluciones de adecuación efectiva", "compliance route", "TMA", "anexo art. 2.3", "proponiéndose en todo caso otras soluciones de adecuación efectiva", ""),
 ("uso restringido", "defined category (use)", "SUA", "anejo A, Uso restringido", "Uso restringido Utilización de las zonas o elementos de circulación limitados a un máximo de 10 personas", "a use class that relaxes many rules"),
 ("uso público", "defined category (use)", "SUA", "anejo A, Uso público", "Uso público Zonas o elementos de circulación susceptibles de ser utilizados por el público en general", ""),
 ("zonas de ocupación nula", "defined category (use)", "SUA", "SUA 9, 1.2.8", "Excepto en el interior de las viviendas y en las zonas de ocupación nula", "defined in DB SI, used to exempt spaces"),
 ("Uso Residencial Vivienda", "building typology", "SUA", "anejo A", "Uso Residencial Vivienda Edificio o zona destinada a alojamiento permanente", "one of nine named uses that structure every rule"),
 ("Vivienda accesible para usuarios de silla de ruedas", "defined dwelling type", "SUA", "anejo A", "Vivienda accesible para usuarios de silla de ruedas", "accessible dwellings split by user"),
 ("Vivienda accesible para personas con discapacidad auditiva", "defined dwelling type", "SUA", "anejo A", "Vivienda accesible para personas con discapacidad auditiva Vivienda que dispone de avisador luminoso y sonoro de timbre", "a dwelling type defined for deaf people"),
 ("Alojamiento accesible", "defined room type", "SUA", "anejo A", "Alojamiento accesible Habitación de hotel, de albergue, de residencia de estudiantes", ""),
 ("sistema de alarma que transmita señales visuales", "element", "SUA", "anejo A, Alojamiento accesible", "contará con un sistema de alarma que transmita señales visuales visibles desde todo punto interior, incluido el aseo", ""),
 ("Plaza reservada para personas con discapacidad auditiva", "defined element", "SUA", "anejo A", "Plaza reservada para personas con discapacidad auditiva", "reserved seat defined by hearing-assistance, not by space"),
 ("Punto de atención accesible", "defined element", "SUA", "anejo A", "Punto de atención accesible Punto de atención al público, como ventanillas, taquillas de venta al público, mostradores de información", ""),
 ("Punto de llamada accesible", "defined element", "SUA", "anejo A", "Punto de llamada accesible Punto de llamada para recibir asistencia que cumple las siguientes condiciones", "an alternative to an accessible counter"),
 ("comunicación bidireccional", "element property", "SUA", "anejo A, Punto de llamada accesible", "permite la comunicación bidireccional con personas con discapacidad auditiva", ""),
 ("llamada de asistencia", "element", "SUA", "SUA 3, 1.2", "mediante el cual se transmita una llamada de asistencia perceptible desde un punto de control", "assistance call in accessible WCs"),
 ("Espacio de transferencia lateral", "quantity", "SUA", "anejo A, aparatos sanitarios, Inodoro", "Espacio de transferencia lateral de anchura ≥ 80 cm", ""),
 ("Espacio de aproximación y transferencia en un lado de la cama", "quantity", "SUA", "anejo A, Vivienda accesible, Dormitorios", "Espacio de aproximación y transferencia en un lado de la cama", "bedside transfer space"),
 ("Espacio de paso a los pies de la cama", "quantity", "SUA", "anejo A, Vivienda accesible, Dormitorios", "Espacio de paso a los pies de la cama", ""),
 ("considerando el amueblamiento", "measurement rule", "SUA", "anejo A, Vivienda accesible, Estancia principal", "Espacio para giro de diámetro Ø 1,50 m libre de obstáculos considerando el amueblamiento de", "turning space measured with furniture in place"),
 ("encuentros en rincón", "quantity", "SUA", "anejo A, Mecanismos accesibles", "La distancia a encuentros en rincón es de 35 cm, como mínimo.", "distance of a control from an internal corner"),
 ("tipo gerontológico", "element type", "SUA", "anejo A, Mecanismos y accesorios", "palanca alargada de tipo gerontológico", ""),
 ("orientable hasta al menos 10º sobre la vertical", "element property", "SUA", "anejo A, Mecanismos y accesorios", "o es orientable hasta al menos 10º sobre la vertical", "tilting mirror"),
 ("Alcance horizontal desde asiento", "quantity", "SUA", "anejo A, Mecanismos y accesorios", "Alcance horizontal desde asiento ≤ 60 cm", "reach measured from the WC seat"),
 ("grúa para piscina", "element", "SUA", "SUA 9, 1.2.5", "alguna entrada al vaso mediante grúa para piscina", "pool hoist"),
 ("marcapasos u otros dispositivos médicos", "exclusion", "SUA", "anejo A, Itinerario accesible", "aquellos elementos que no sean adecuados para personas con marcapasos u otros dispositivos médicos", "security gates excluded from the route for people with pacemakers"),
 ("barreras tipo torno", "exclusion", "SUA", "anejo A, Itinerario accesible", "a las barreras tipo torno", "turnstiles excluded from the accessible route"),
 ("estación de recarga de vehículo eléctrico", "element", "SUA", "anejo A, Plaza de aparcamiento accesible", "cuente con una estación de recarga de vehículo eléctrico", "EV charger reach and route"),
 ("Braille y arábigo en alto relieve", "technique", "SUA", "SUA 9, 2.2.2", "contarán con indicación en Braille y arábigo en alto relieve", "floor number in Braille and raised Arabic numerals"),
 ("pictogramas normalizados de sexo", "technique", "SUA", "SUA 9, 2.2.3", "se señalizarán con pictogramas normalizados de sexo en", ""),
 ("acanaladuras", "element property", "SUA", "SUA 9, 2.2.4", "acanaladuras perpendiculares al eje de la escalera", "grooved strip at stair starts"),
 ("perros guía, perros de asistencia", "user aid", "RD505", "art. 2.5", "que sean usuarias de perros guía, perros de asistencia o cualquier otro tipo de ayuda", ""),
 ("comunicación visual de determinados espacios", "requirement", "RD505", "art. 4.2 c)", "La comunicación visual de determinados espacios, según su uso, atendiendo a las necesidades de las personas con discapacidad auditiva.", "visual connection between spaces for deaf people"),
 ("Zona de refugio", "defined space", "RD505", "anexo, Zona de refugio", "Zona de refugio: Zona delimitada por elementos resistentes al fuego, con capacidad suficiente", ""),
 ("ascensor de emergencia", "element", "RD505", "art. 8.1", "Los edificios dispondrán de ascensor de emergencia con accesos desde cada planta", ""),
 ("señalización óptica, acústica y táctil", "technique", "RD505", "art. 8.3", "señalización óptica, acústica y táctil adecuadas para facilitar la orientación", "evacuation routes"),
 ("plataformas salvaescaleras", "element", "RD505", "anexo, Itinerario accesible entre diferentes niveles", "tales como rampas, ascensores o plataformas salvaescaleras", "stair platform lifts as an alternative means"),
 ("alcorque", "element", "RD505", "art. 12.5", "En el caso de que el alcorque quede dentro de dicho espacio, deberá estar", "tree pit"),
 ("diseño para todos", "principle", "RD505", "preámbulo", "la visión de la accesibilidad fundamentada en el diseño para todos y la autonomía personal", ""),
]

def write_rev():
    bad = 0
    with open(D + '/reverse-harvest.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['phrase_verbatim (instrument own phrase)', 'kind (ours)', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'gloss_OURS_not_an_equivalence'])
        for ph, kind, ins, loc, q, g in REV:
            ok = norm(q) in TXT[ins] and norm(ph).lower() in norm(q).lower()
            if not ok: bad += 1; print('REV FAIL', ins, loc, ph, norm(q) in TXT[ins], file=sys.stderr)
            w.writerow([ph, kind, 'ES', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok else 'NO', g])
    print('reverse-harvest', len(REV), 'verified', len(REV) - bad)
    return bad

def main():
    bad = write_rev(); rows = []; sua_in_dcc = 0; sua_n = 0
    for c, ph, ins, loc, q, note in OBS:
        ok_q = norm(q) in TXT[ins]
        ok_p = norm(ph).lower() in norm(q).lower()
        if ins == 'SUA':
            sua_n += 1; sua_in_dcc += norm(q) in DCC
        if not (ok_q and ok_p): bad += 1; print('FAIL', ins, loc, ph, ok_q, ok_p, file=sys.stderr)
        rows.append([c, ph, 'ES', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok_q and ok_p else 'NO', note])
    with open(D + '/observations.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept (English register label; | = counts for each)', 'phrase_verbatim', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'note (ours)'])
        w.writerows(rows)
    with open(D + '/coverage.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['register_concept', 'register_source', 'status', 'n_observations', 'phrases_found (distinct)', 'note'])
        for i, c in enumerate(REGISTER):
            src = 'catalogue 2.1' if i < 32 else ('catalogue 2.2' if i < 50 else ('base_parameters' if i < 60 else 'b651 heading RHFAC-does-not-name'))
            hit = [r for r in rows if c in r[0].split('|')]
            if hit:
                ph = sorted({r[1] for r in hit})
                notes = '; '.join(sorted({r[8] for r in hit if r[8]}))
                st = 'FOUND-PARTIAL' if c in PARTIAL else 'FOUND'
                w.writerow([c, src, st, len(hit), ' / '.join(ph), (PARTIAL.get(c, '') + '; ' if c in PARTIAL else '') + notes])
            else:
                w.writerow([c, src, 'SEARCHED-ABSENT', 0, '', ABSENT.get(c, 'NO NOTE: check')])
    print('observations', len(rows), 'failures (obs+rev)', bad, '| SUA quotes also in held DB-SUA con comentarios:', sua_in_dcc, 'of', sua_n)
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
