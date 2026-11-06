"""Build observations / coverage / reverse-harvest TSVs for the FR/FR terminology pass, verifying every
quote byte-for-byte (after whitespace collapse) in the saved extracted text. Run from the repository root:
    python3 -I scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/FR-FR/build.py
Exits non-zero if any quote or phrase fails to verify. Read-only apart from the TSVs in this folder."""
import re, sys, csv, os, hashlib
D = 'scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/FR-FR'
INST = {
 'A17': ("Arrêté du 20 avril 2017 relatif à l'accessibilité aux personnes handicapées des établissements recevant du public lors de leur construction et des installations ouvertes au public lors de leur aménagement", D + '/text/43802a8ee631.txt'),
 'A15': ("Arrêté du 24 décembre 2015 relatif à l'accessibilité aux personnes handicapées des bâtiments d'habitation collectifs et des maisons individuelles lors de leur construction", D + '/text/014af9f59daf.txt'),
}
def norm(s): return re.sub(r'\s+', ' ', s).strip()
TXT = {k: norm(open(v[1], encoding='utf-8').read()) for k, v in INST.items()}

# (concepts '|'-separated, phrase verbatim, instrument, locator, quote verbatim, note)
OBS = [
 ("Well-illuminated (if site expected to be lit)|Well illuminated (if required for expected usage)|lighting levels", "dispositif d'éclairage", "A17", "art. 2, II, 3°", "Le cheminement accessible comporte un dispositif d'éclairage répondant aux exigences définies à l'article 14.", ""),
 ("Well-illuminated (if site expected to be lit)|Well illuminated (if required for expected usage)|lighting levels", "valeurs d'éclairement moyen horizontal", "A17", "art. 14, II", "Il permet d'assurer des valeurs d'éclairement moyen horizontal mesurées au sol le long du parcours usuel de circulation", "the quantity is horizontal illuminance measured at floor level along the route"),
 ("Well-illuminated (if site expected to be lit)|Well illuminated (if required for expected usage)", "qualité d'éclairage renforcée", "A17", "art. 14, I", "les dispositifs d'accès et les informations fournies par la signalétique font l'objet d'une qualité d'éclairage renforcée", ""),
 ("Well-illuminated (if site expected to be lit)|Well illuminated (if required for expected usage)|lighting levels", "dispositif d'éclairage", "A15", "art. 2, II, 3°", "Le cheminement doit comporter un dispositif d'éclairage répondant aux exigences définies à l'article 10.", ""),
 ("Well illuminated (if required for expected usage)", "éclairage suffisant", "A15", "art. 10, I", "Les locaux collectifs font l'objet d'un éclairage suffisant.", ""),
 ("Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant", "non meuble, non glissant, non réfléchissant et sans obstacle à la roue", "A17", "art. 2, II, 3°", "Le sol ou le revêtement de sol du cheminement accessible est non meuble, non glissant, non réfléchissant et sans obstacle à la roue.", "adds 'non réfléchissant' (non-reflective), which the English criterion lacks"),
 ("Surface is firm, stable and slip resistant|Surface is stable, firm, and slip resistant", "non meuble, non glissant, non réfléchissant et sans obstacle à la roue", "A15", "art. 2, II, 3°", "Le sol ou le revêtement de sol du cheminement accessible doit être non meuble, non glissant, non réfléchissant et sans obstacle à la roue.", ""),
 ("Floor surface is stable, firm, and non-slip", "revêtements de sol", "A17", "art. 9, I", "Les revêtements de sol et les équipements situés sur le sol des cheminements sont sûrs et permettent une circulation aisée des personnes handicapées.", ""),
 ("Floor surface is stable, firm, and non-slip", "tapis fixes", "A17", "art. 9, II", "les tapis fixes présentent la dureté nécessaire pour ne pas gêner la progression d'un fauteuil roulant", ""),
 ("Seating", "équipement permettant de s'asseoir", "A17", "art. 18, II, 2°", "un équipement permettant de s'asseoir et de disposer d'un appui en position", "NARROWER: a seat in an adapted cabin or shower only; rest seating along routes is not treated"),
 ("Handrails", "main courante", "A17", "art. 7-1, II, 3°", "L'escalier, quelle que soit sa conception, comporte une main courante de chaque côté.", ""),
 ("Handrails", "main courante", "A15", "art. 6, 6.1, II, 3°", "L'escalier, quelle que soit sa conception, doit comporter une main courante de chaque côté.", ""),
 ("Handrails", "mains courantes", "A17", "art. 8, II, 2°", "Les mains courantes situées de part et d'autre de l'équipement accompagnent le déplacement", "on moving walkways and escalators"),
 ("Clear width|width", "largeur de passage utile", "A17", "art. 10, II, 1°", "Les portes principales desservant des locaux ou zones pouvant recevoir 100 personnes ou plus ont une largeur de passage utile minimale de 1,40 m.", ""),
 ("Clear width|width", "libre de tout obstacle", "A17", "art. 2, II, 2° b)", "La largeur minimale du cheminement accessible est de 1,40 m libre de tout obstacle afin de faciliter les croisements.", ""),
 ("Clear width", "Largeur de passage", "A17", "art. 2, II, 2° b) (sub-heading)", "Profil en travers : Largeur de passage :", ""),
 ("Accessible path of travel", "cheminement accessible", "A17", "art. 2, I", "Un cheminement accessible permet d'accéder à l'entrée principale, ou à une des entrées principales, des bâtiments depuis l'accès au terrain.", ""),
 ("Accessible path of travel", "cheminement accessible", "A15", "art. 2, I", "Un cheminement accessible doit permettre d'atteindre, depuis un accès par la voie de desserte :", ""),
 ("Drainage", "éviter la stagnation d'eau", "A17", "art. 2, II, 2° b)", "Le cheminement est conçu et mis en œuvre de manière à éviter la stagnation d'eau.", "framed as a design aim tied to cross-fall, not as drainage hardware"),
 ("Drainage", "siphon de sol", "A17", "art. 18, II, 2°", "un siphon de sol ;", "floor drain in an adapted shower"),
 ("Clear signage", "signalisation adaptée", "A17", "art. 2, II, 1°", "Une signalisation adaptée est mise en place à l'entrée du terrain de l'opération", ""),
 ("Clear signage", "INFORMATION ET SIGNALISATION", "A17", "annexe 3 (heading)", "INFORMATION ET SIGNALISATION", ""),
 ("Clear signage", "signalétique", "A17", "annexe 3, Compréhension", "Lorsque la signalétique repose sur un code, utilisant notamment différentes couleurs, celui-ci est homogène et continu dans tout l'établissement", ""),
 ("Audio accessibility and communication enhancement technologies", "boucle d'induction magnétique", "A17", "art. 5, II", "sont équipés obligatoirement d'une telle boucle d'induction magnétique", ""),
 ("Audio accessibility and communication enhancement technologies", "système de transmission du signal acoustique par induction magnétique", "A17", "art. 5, II", "Lorsque l'accueil est sonorisé, il est équipé d'un système de transmission du signal acoustique par induction magnétique", ""),
 ("Audio accessibility and communication enhancement technologies", "boucle à induction magnétique", "A17", "art. 11, II, 2°", "au moins une de ces salles est équipée d'une boucle à induction magnétique", "same text uses three phrasings for the loop"),
 ("Audio accessibility and communication enhancement technologies", "boucle magnétique", "A15", "art. 4, II, 2°", "Les combinés sont équipés d'une boucle magnétique respectant les dispositions décrites en annexe 7 permettant l'amplification par une prothèse auditive.", ""),
 ("Audio accessibility and communication enhancement technologies", "sous-titrage", "A17", "art. 20", "Dans les lieux publics collectifs, le sous-titrage en français est activé sur les téléviseurs", ""),
 ("Audio accessibility and communication enhancement technologies", "audiodescription", "A17", "art. 20", "des notices simplifiées indiquent comment activer le sous-titrage et l'audiodescription.", ""),
 ("Audio accessibility and communication enhancement technologies", "retour visuel des informations principales fournies oralement", "A17", "art. 4, II, 3°", "un retour visuel des informations principales fournies oralement.", ""),
 ("Level landings with clear space", "palier de repos", "A17", "annexe 2, 1.", "Le palier de repos s'insère en intégralité dans le cheminement.", ""),
 ("Level landings with clear space", "palier de repos", "A15", "annexe 2, 1.", "Le palier de repos permet à une personne debout mais à mobilité réduite ou à une personne en fauteuil roulant de se reprendre, de souffler.", ""),
 ("Level landings with clear space and at regular intervals", "palier de repos est nécessaire tous les", "A17", "art. 2, II, 2° a)", "En cas de plan incliné de pente supérieure ou égale à 4 %, un palier de repos est nécessaire tous les 10 m.", ""),
 ("Clear space for approach", "espace d'usage", "A17", "annexe 2, 4.", "L'espace d'usage permet le positionnement du fauteuil roulant ou d'une personne avec une ou deux cannes pour utiliser un équipement ou un dispositif de commande ou de service.", "defined for wheelchair users AND people using one or two canes"),
 ("Clear space for approach", "obstacle à l'approche d'un fauteuil roulant", "A17", "art. 4, II, 3°", "ils sont situés à plus de 0,40 m d'un angle rentrant de parois ou de tout autre obstacle à l'approche d'un fauteuil roulant", ""),
 ("Riser height and tread depth|tread", "largeur du giron", "A17", "art. 7-1, II, 1°", "la largeur du giron est supérieure ou égale à 28 cm", "French carves tread as a WIDTH (largeur du giron); English says depth"),
 ("Riser height and tread depth|tread", "largeur du giron", "A15", "art. 12, II, 1°", "largeur du giron supérieure ou égale à 24 cm", ""),
 ("Riser height and tread depth|riser|No open riser", "contremarche", "A17", "art. 7-1, II, 2°", "La première et la dernière marche sont pourvues d'une contremarche d'une hauteur minimale de 0,10 m", "for 'No open riser': NARROWER, only the first and last step require a riser"),
 ("Riser height and tread depth|riser", "Les marches répondent aux exigences suivantes", "A17", "art. 7-1, II, 1°", "Les marches répondent aux exigences suivantes : - leur hauteur est inférieure ou égale à 16 cm", "riser height is 'leur hauteur' (the steps' height); 'contremarche' is the riser element"),
 ("Nosing design", "nez de marches", "A17", "art. 7-1, II, 2°", "Les nez de marches répondent aux exigences suivantes :", ""),
 ("Nosing design", "nez de marches", "A15", "art. 6, 6.1, II, 2°", "Les nez de marches doivent répondre aux exigences suivantes :", ""),
 ("Colour-contrasted and slip-resistant strip on nosing|Colour-contrasted and slip-resistant strip", "contrastés visuellement", "A17", "art. 7-1, II, 2°", "être contrastés visuellement par rapport au reste de l'escalier sur au moins 3 cm en horizontal", "no 'strip': the nosing itself is contrasted"),
 ("Colour-contrasted and slip-resistant strip on nosing|Colour-contrasted and slip-resistant strip", "non glissants", "A17", "art. 7-1, II, 2°", "être non glissants ;", ""),
 ("Level threshold", "sans ressaut", "A17", "art. 4, II, 1°", "L'accès est horizontal et sans ressaut", ""),
 ("Level threshold", "seuils de porte", "A17", "art. 2, II, 2° a)", "Cette dernière disposition ne s'applique pas aux seuils de porte ni aux pas de porte.", ""),
 ("Level threshold", "ressaut dû au seuil", "A15", "art. 8, II, 1°", "S'il ne peut être évité, la hauteur maximale du ressaut dû au seuil est de 2 cm.", ""),
 ("Level threshold", "de plain-pied", "A15", "art. 14, II, 2°", "Le cheminement de la pièce intérieure vers l'espace extérieur est aménagé de plain-pied ou présente une différence de niveau limitée.", ""),
 ("Height clearance (if sheltered or parkade)|clearance", "passage libre", "A17", "art. 2, II, 3°", "un passage libre d'au moins 2,20 m de hauteur au-dessus du sol est prévu", ""),
 ("Height clearance (if sheltered or parkade)|clearance", "passage libre sous les obstacles en hauteur", "A17", "art. 6, II", "le passage libre sous les obstacles en hauteur, qui est réduit à 2 m dans les parcs de stationnement.", "the parkade case the English criterion names"),
 ("Height clearance (if sheltered or parkade)|clearance", "HAUTEUR LIBRE SOUS L'OBSTACLE", "A17", "annexe 4 (table heading)", "HAUTEUR LIBRE SOUS L'OBSTACLE", ""),
 ("Edge protection", "dispositif de protection", "A17", "art. 2, II, 3°", "une rupture de niveau vers le bas d'une hauteur de plus de 0,25 m, un dispositif de protection est implanté afin d'alerter les personnes du risque de chute", "purpose: to WARN of the fall risk"),
 ("Edge protection", "dispositif de protection", "A15", "art. 2, II, 3°", "un dispositif de protection doit être implanté afin d'éviter les chutes", "purpose: to PREVENT falls (differs from A17)"),
 ("Tactile attention indicators (truncated domes)", "bande d'éveil à la vigilance", "A17", "annexe 7", "Une bande d'éveil à la vigilance a pour objectif d'éveiller la vigilance des personnes présentant une déficience visuelle par détection tactile et visuelle.", ""),
 ("Tactile attention indicators (truncated domes)", "plots régulièrement espacés", "A17", "annexe 7", "elle est constituée de plots régulièrement espacés", "studs; 'truncated domes' is not the French term"),
 ("Tactile attention indicators (truncated domes)", "dispositif d'éveil à la vigilance", "A15", "annexe 6, I", "Un dispositif d'éveil à la vigilance a pour objectif d'éveiller la vigilance des personnes présentant une déficience visuelle par détection tactile et visuelle mais ne présente pas de risque de chute.", ""),
 ("Tactile attention indicators (truncated domes)", "changement de revêtement de sol", "A15", "annexe 6, II", "il est constitué par un changement de revêtement de sol", "housing: a change of floor finish, no studs specified"),
 ("Slope|gradient", "pente", "A17", "art. 2, II, 2° a)", "un plan incliné de pente inférieure ou égale à 5 % est aménagé afin de la franchir", "one French word for slope and gradient"),
 ("Slope|gradient", "dévers", "A17", "art. 2, II, 2° b)", "Lorsqu'un dévers est nécessaire, il est inférieur ou égal à 2 %.", "cross-slope has its own word"),
 ("Slope", "Profil en long", "A17", "art. 2, II, 2° a) (sub-heading)", "a) Profil en long :", ""),
 ("Sink faucet is easy to use or automatic", "robinetterie", "A17", "art. 12, II, 2°", "le choix et le positionnement de la robinetterie permettent un usage complet du lavabo en position assis", ""),
 ("Sink faucet is easy to use or automatic", "cellule de déclenchement", "A17", "art. 12, II, 2°", "équipé d'une robinetterie dont la commande ou la cellule de déclenchement est située à plus de 0,40 m", "sensor tap named by its trigger cell"),
 ("Outlets and switches are at accessible heights", "interrupteur de commande d'éclairage", "A15", "art. 11, II, 2°", "Un interrupteur de commande d'éclairage doit être situé en entrée de chaque pièce.", ""),
 ("Outlets and switches are at accessible heights", "prise de courant", "A15", "art. 11, II, 2°", "une prise de courant est disposée à proximité immédiate de l'interrupteur de commande d'éclairage situé en entrée de la pièce", ""),
 ("Outlets and switches are at accessible heights", "prises d'alimentation électrique", "A15", "art. 11, II, 2°", "Les autres prises d'alimentation électrique, à l'exception des prises alimentant des équipements fixes par nature", ""),
 ("Outlets and switches are at accessible heights", "prise de courant", "A17", "art. 17, II, 1°", "une prise de courant au moins est située à proximité d'un lit", ""),
 ("Accessible door hardware", "poignées de porte", "A17", "art. 10, II, 2°", "Les poignées de porte sont facilement préhensibles et manœuvrables en position", ""),
 ("Accessible door hardware", "geste de rotation du poignet", "A17", "art. 10, II, 2°", "par une personne ayant des difficultés à saisir et à faire un geste de rotation du poignet", ""),
 ("Accessible door hardware", "serrures", "A15", "art. 8, II, 2°", "Les serrures doivent être situées à plus de 0,30 m d'un angle rentrant de parois", ""),
 ("Accessible controls", "dispositifs de commande", "A17", "art. 11, II, 1°", "Les dispositifs de commande sont repérables par un contraste visuel et tactile.", ""),
 ("Accessible controls", "commande manuelle", "A17", "art. 11, II, 2° a)", "pour une commande manuelle ;", ""),
 ("Accessible controls", "à effleurement", "A17", "art. 11, II, 2°", "Les interrupteurs et les boutons de commande mis à disposition du public ne sont pas à effleurement.", "touch-sensitive controls excluded"),
 # quantity-bearing words (catalogue 2.2)
 ("height", "hauteur", "A17", "art. 4, II, 3°", "ils sont situés à une hauteur comprise entre 0,90 m et 1,30 m", ""),
 ("level", "horizontal et sans ressaut", "A17", "art. 2, II, 2° a)", "Le cheminement accessible est horizontal et sans ressaut.", "'level' as flat"),
 ("level", "écart de niveau", "A17", "art. 2, II, 2° a)", "un faible écart de niveau peut être traité par un ressaut à bord arrondi ou muni d'un chanfrein", "'level' as difference in height"),
 ("level", "niveau décalé", "A17", "art. 7", "Toute dénivellation des circulations horizontales supérieure ou égale à 1,20 m détermine un niveau décalé considéré comme un étage.", "'level' as storey"),
 ("level", "dénivellation", "A17", "art. 2, II, 2° a)", "Lorsqu'une dénivellation ne peut être évitée", ""),
 ("width|Clear width", "largeur nominale", "A17", "art. 10, II, 1°", "Les portes principales desservant des locaux pouvant recevoir moins de 100 personnes ont une largeur nominale minimale de 0,90 m, correspondant à une largeur de passage utile de 0,83 m.", "two widths per door: nominal and clear"),
 ("clearance", "vide en partie inférieure", "A17", "art. 5, II", "l'équipement présente un vide en partie inférieure d'au moins 0,30 m de profondeur", "knee and foot clearance"),
 ("clearance", "espace libre", "A15", "art. 13, II, 1°", "Un cabinet d'aisances au moins doit offrir un espace libre accessible à une personne en fauteuil roulant", ""),
 ("number", "nombre total de places", "A17", "art. 3, II, 3°", "Les places adaptées destinées à l'usage du public représentent au minimum 2 % du nombre total de places prévues pour le public.", ""),
 ("number|ratio", "par tranche ou fraction", "A17", "art. 17, II, 2° a)", "1 chambre supplémentaire par tranche ou fraction de 50 chambres supplémentaire au-delà de 50", "for 'ratio': proportional provision; the English 'mix' of shower and bath rooms is not treated"),
 ("depth", "profondeur", "A15", "art. 14, I", "tout balcon, loggia ou terrasse présentant une profondeur de plus de 60 cm", ""),
 ("force|Operating force (parameter 6)", "effort nécessaire pour ouvrir la porte", "A17", "art. 10, II, 2°", "L'effort nécessaire pour ouvrir la porte est inférieur ou égal à 50 N", ""),
 ("force|Operating force (parameter 6)", "effort nécessaire pour ouvrir la porte", "A15", "art. 8, II, 2°", "L'effort nécessaire pour ouvrir la porte doit être inférieur ou égal à 50 N", ""),
 ("force|Operating force (parameter 6)", "force de pression", "A17", "art. 7-2, II, 3° c)", "la force de pression nécessaire pour activer les commandes est comprise entre 2 N et 5 N", "lift controls"),
 ("time", "durée d'ouverture", "A17", "art. 10, II, 2°", "Lorsqu'une porte est à ouverture automatique, la durée d'ouverture permet le passage de personnes à mobilité réduite.", ""),
 ("time", "durée de fonctionnement", "A17", "art. 14, II", "Lorsque la durée de fonctionnement d'un système d'éclairage est temporisée, l'extinction est progressive.", ""),
 ("size", "dimension utile", "A17", "art. 7-2, II, 3° c)", "la plate-forme élévatrice a une dimension utile de 0,90 m × 1,40 m", ""),
 ("size", "dimensions d'encombrement", "A17", "annexe 1", "un fauteuil roulant occupé dont les dimensions d'encombrement sont de 0,75 m × 1,25 m", ""),
 ("capacity", "soulever une charge", "A17", "art. 7-2, II, 3° c)", "la plate-forme élévatrice peut soulever une charge de 250 kg/m2", "the English 'capacity' is a platform lift's"),
 ("volume", "niveau de pression acoustique", "A17", "annexe 8", "le niveau de pression acoustique du message sonore est adapté aux conditions du site", "PARTIAL: sound level of an accessible pedestrian signal; adjustable paging volume is not treated"),
 ("distance", "distance minimale", "A17", "art. 2, II, 2° a)", "La distance minimale entre deux ressauts successifs est de 2,50 m.", "different sense from the English 'distance markers along route'"),
 ("distance", "distance de lecture de référence", "A17", "annexe 3, Lisibilité", "la distance de lecture de référence fixée par le maître d'ouvrage", ""),
 # base parameters
 ("Ramp gradient (parameter 3)|Slope", "plan incliné", "A17", "art. 2, I", "Lorsque le cheminement courant se fait par un plan incliné, celui-ci offre des caractéristiques minimales définies au II ci-après.", "the fixed ramp is 'plan incliné'; 'rampe' appears only in A15 as a removable ramp"),
 ("Ramp gradient (parameter 3)", "rampe amovible", "A15", "art. 14, II, 3° b)", "pour permettre l'installation ultérieure d'une rampe amovible ou d'un appareil élévateur vertical", ""),
 ("Corridor width (parameter 4)", "circulations intérieures horizontales", "A17", "art. 6, II", "Les circulations intérieures horizontales répondent aux exigences applicables au cheminement extérieur accessible visées à l'article 2", "no 'couloir' anywhere; the corridor is a 'circulation'"),
 ("Corridor width (parameter 4)", "largeur minimale des circulations intérieures", "A15", "art. 11, II, 1°", "La largeur minimale des circulations intérieures doit être de 0,90 m.", "inside the dwelling"),
 ("Turning circle (parameter 5)", "Espace de manœuvre avec possibilité de demi-tour", "A17", "annexe 2, 2.", "2. Espace de manœuvre avec possibilité de demi-tour", "defined for wheelchairs AND people with one or two canes"),
 ("Turning circle (parameter 5)", "faire demi-tour", "A17", "annexe 2, 2.", "Il permet de s'orienter différemment ou de faire demi-tour.", ""),
 ("Reverberation time (parameter 7)", "temps de réverbération", "A17", "art. 9, II", "les valeurs réglementaires de temps de réverbération et de surface équivalente de matériaux absorbants définies par les exigences acoustiques en vigueur sont respectées", "pointer to other acoustic rules; fallback quantity is absorption area"),
 ("Reverberation time (parameter 7)", "aire d'absorption équivalente", "A15", "art. 7, II", "l'aire d'absorption équivalente des revêtements et éléments absorbants disposés dans les halls et les circulations intérieures desservant des logements", "housing uses absorption area only, no reverberation time"),
 ("LRV contrast (parameter 8)", "contraste visuel", "A17", "art. 10, II, 3°", "Les portes ou leur encadrement ainsi que leur dispositif de manœuvre présentent un contraste visuel par rapport à leur environnement.", "BROADER: contrast is never quantified; no luminance or LRV term"),
 ("LRV contrast (parameter 8)", "fortement contrastées", "A17", "annexe 3, Lisibilité", "être fortement contrastées par rapport au fond du support", ""),
 ("LRV contrast (parameter 8)", "contraste de couleur ou de lumière", "A17", "art. 8, II, 2°", "Le départ et l'arrivée des parties en mouvement sont mis en évidence par un contraste de couleur ou de lumière.", ""),
 ("Door width (parameter 9)", "largeur nominale", "A15", "art. 11, II, 1°", "La porte d'entrée doit avoir une largeur nominale minimale de 0,90 m correspondant à une largeur de passage utile minimale de 0,83 m.", ""),
 ("Door width (parameter 9)", "largeur de passage utile", "A17", "art. 10, II, 1°", "Les portes principales desservant des locaux ou zones pouvant recevoir 100 personnes ou plus ont une largeur de passage utile minimale de 1,40 m.", ""),
 ("Headroom clearance (parameter 11)", "passage libre", "A15", "art. 2, II, 3°", "laisser un passage libre d'au moins 2,20 m de hauteur au-dessus du sol", ""),
 ("Headroom clearance (parameter 11)", "HAUTEUR LIBRE SOUS L'OBSTACLE", "A17", "annexe 4 (table heading)", "HAUTEUR LIBRE SOUS L'OBSTACLE", ""),
 ("Ramp run length (parameter 12)", "longueur", "A17", "art. 2, II, 2° a)", "jusqu'à 8 % sur une longueur inférieure ou égale à 2 m", "length is attached to each tolerated slope, not stated as a run limit"),
 ("Ramp run length (parameter 12)", "quelle qu'en soit la longueur", "A17", "art. 2, II, 2° a)", "Un palier de repos est nécessaire en haut et en bas de chaque plan incliné quelle qu'en soit la longueur.", ""),
]

REGISTER = [  # catalogue 2.1 (32), 2.2 (18), base parameters (10), in that order
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
]
ALIAS = {"slope": "Slope"}
PARTIAL = {  # concept -> why the French match is not the English concept (ours)
 "Seating": "NARROWER: shower/cabin seat only",
 "No open riser": "NARROWER: riser required on first and last step only",
 "volume": "PARTIAL: signal sound level, not paging volume",
 "ratio": "PARTIAL: proportional count, no shower/bath mix",
 "distance": "DIFFERENT SENSE: no distance markers",
 "LRV contrast (parameter 8)": "BROADER: contrast never quantified",
}  # the 2.2 word 'slope' counts the 2.1 concept's observations
ABSENT = {
 "Shelter": "no canopy or shelter requirement; grep 'abri' 0/0; 'couvert' in A15 only as 'locaux collectifs couverts' for lighting",
 "Microwave mounting height accessible and safe": "no kitchen-appliance mounting rule; 'micro-ondes' 0/0; A15 treats the kitchen only as a passage between appliances",
 "Accessible lockers": "'casier' 0/0, 'consigne' 0/0; nearest are 'patères' (coat hooks) and A15 'boîtes aux lettres'",
 "Colour temperature (parameter 10)": "'température de couleur' 0/0, 'kelvin' 0/0; lighting is regulated only by illuminance, glare and timing",
}

# Reverse harvest: (phrase verbatim, kind, instrument, locator, quote verbatim, gloss — OURS, not the instrument's)
REV = [
 ("établissements recevant du public", "legal category (building class)", "A17", "title / art. 1", "relatif à l'accessibilité aux personnes handicapées des établissements recevant du public lors de leur construction", "the regulated building class; the regime differs from housing"),
 ("installations ouvertes au public", "legal category", "A17", "title", "et des installations ouvertes au public lors de leur aménagement", "open-air or non-building installations open to the public"),
 ("de 1re à 4e catégorie", "legal category (ERP size class)", "A17", "art. 5, II", "établissements recevant du public de 1re à 4e catégorie sont équipés obligatoirement", "a fire-safety size class reused as an accessibility trigger"),
 ("bâtiments d'habitation collectifs", "legal category", "A15", "title", "des bâtiments d'habitation collectifs et des maisons individuelles lors de leur construction", ""),
 ("maisons individuelles", "legal category", "A15", "title", "des bâtiments d'habitation collectifs et des maisons individuelles lors de leur construction", ""),
 ("logements destinés à une occupation temporaire ou saisonnière", "legal category", "A15", "art. 1", "ne s'appliquent pas aux logements destinés à une occupation temporaire ou saisonnière", ""),
 ("Usages attendus", "drafting structure", "A17", "art. 2, I (and every article)", "I.-Usages attendus :", "each article states expected uses (performance aim) then 'Caractéristiques minimales'; an aim/prescription split the register does not carry"),
 ("Caractéristiques minimales", "drafting structure", "A17", "art. 2, II", "II.-Caractéristiques minimales :", ""),
 ("solutions d'effet équivalent", "compliance route", "A17", "art. 1", "Des solutions d'effet équivalent peuvent être mises en œuvre dès lors que celles-ci satisfont aux mêmes objectifs", "equivalent-performance route with prefect approval"),
 ("repéré, détecté, atteint et utilisé", "functional chain", "A17", "art. 5, I", "doit pouvoir être repéré, détecté, atteint et utilisé par une personne handicapée", "the four verbs organise the sub-headings Repérage / Atteinte et usage / Sécurité d'usage"),
 ("Repérage et guidage", "sub-heading category", "A17", "art. 2, II, 1°", "1° Repérage et guidage :", ""),
 ("Sécurité d'usage", "sub-heading category", "A17", "art. 2, II, 3°", "3° Sécurité d'usage :", ""),
 ("Atteinte et usage", "sub-heading category", "A17", "art. 3, II, 5°", "5° Atteinte et usage :", ""),
 ("chaîne du déplacement", "concept", "A17", "art. 2, I", "ils facilitent la continuité de la chaîne du déplacement avec l'extérieur du terrain", "continuity of the travel chain beyond the site"),
 ("cheminement usuel", "concept", "A17", "art. 2, I", "Le cheminement accessible est le cheminement usuel, ou l'un des cheminements usuels.", "the accessible route must be the ordinary one"),
 ("Profil en travers", "dimensional category", "A17", "art. 2, II, 2° b)", "b) Profil en travers :", "cross-section (paired with 'Profil en long')"),
 ("ressaut", "element", "A17", "art. 2, II, 2° a)", "un ressaut à bord arrondi ou muni d'un chanfrein", "a small permitted upstand; English register has only 'level threshold'"),
 ("pas d'âne", "element (prohibited)", "A17", "art. 2, II, 2° a)", "Les pentes comportant plusieurs ressauts successifs, dits \" pas d'âne \", sont interdites.", "stepped ramp"),
 ("Espace de manœuvre de porte", "space type", "A17", "annexe 2, 3.", "3. Espace de manœuvre de porte", "door manoeuvring space, length differs push vs pull"),
 ("GABARIT D'ENCOMBREMENT DU FAUTEUIL ROULANT", "reference body", "A17", "annexe 1", "GABARIT D'ENCOMBREMENT DU FAUTEUIL ROULANT", "the reference occupied-wheelchair envelope"),
 ("BESOINS D'ESPACES LIBRES DE TOUT OBSTACLE", "space typology", "A17", "annexe 2", "BESOINS D'ESPACES LIBRES DE TOUT OBSTACLE", "three reasons: se reposer, effectuer une manœuvre, utiliser un équipement"),
 ("chevauchement", "technique (permitted overlap)", "A17", "annexe 2, 2.", "Un seul chevauchement peut être effectué sur un espace de manoeuvre avec possibilité de demi-tour.", ""),
 ("angle rentrant de parois", "geometric reference", "A17", "art. 4, II, 3°", "à plus de 0,40 m d'un angle rentrant de parois", "distance of a control from an inside corner"),
 ("en position \" debout \" comme en position \" assis \"", "use condition", "A17", "art. 4, II, 3°", "Le système d'ouverture des portes est utilisable en position \" debout \" comme en position \" assis \".", "standing-and-seated usability as a stated test"),
 ("rupture de niveau", "hazard", "A17", "art. 2, II, 3°", "par une rupture de niveau vers le bas", "drop-off beside a route"),
 ("dispositif de détection", "element", "A17", "art. 2, II, 3°", "un dispositif de détection permettant de prévenir du danger de choc est prévu", "cane-detectable warning under a protruding object"),
 ("zone de balayage d'une canne blanche", "reference zone", "A17", "art. 2, II, 3°", "Ce dispositif de détection est situé dans la zone de balayage d'une canne blanche", "the white-cane sweep zone"),
 ("en saillie latérale ou en porte-à-faux", "hazard type", "A17", "annexe 4 (heading)", "DÉTECTION DES OBSTACLES EN SAILLIE LATÉRALE OU EN PORTE-À-FAUX", ""),
 ("DÉTECTION DES MOBILIERS, BORNES ET POTEAUX", "element", "A17", "annexe 5", "DÉTECTION DES MOBILIERS, BORNES ET POTEAUX", "bollard and post detectability geometry"),
 ("parois vitrées", "element", "A17", "art. 2, II, 3°", "Les parois vitrées situées sur les cheminements ou en bordure immédiate de ceux-ci sont repérables par des personnes de toutes tailles", ""),
 ("covisibilité", "concept", "A17", "art. 2, II, 3°", "la covisibilité entre les conducteurs des véhicules et les piétons est garantie", "mutual visibility at a vehicle crossing"),
 ("BANDES DE GUIDAGE TACTILE AU SOL", "element", "A17", "annexe 6", "BANDES DE GUIDAGE TACTILE AU SOL", "tactile guidance strip; the register has attention indicators only"),
 ("repère continu", "element", "A17", "art. 2, II, 1°", "un repère continu, tactile pour le guidage à l'aide d'une canne blanche", ""),
 ("DISPOSITIFS RÉPÉTITEURS DE FEUX DE CIRCULATION", "element", "A17", "annexe 8", "DISPOSITIFS RÉPÉTITEURS DE FEUX DE CIRCULATION À L'USAGE DES PERSONNES AVEUGLES OU MALVOYANTES", "accessible pedestrian signals; 'boîtier vibrant' or 'cône tournant'"),
 ("niveau décalé considéré comme un étage", "rule of classification", "A17", "art. 7", "détermine un niveau décalé considéré comme un étage", ""),
 ("Appareils élévateurs verticaux", "element", "A17", "art. 7-2, II, 3°", "3° Appareils élévateurs verticaux :", "platform lift; three types by 'hauteur de course'"),
 ("hauteur de course", "quantity", "A17", "art. 7-2, II, 3° b)", "Le choix du type de matériel se fait en fonction de la hauteur de course", "lift travel height"),
 ("commandes à pression maintenue", "element", "A17", "art. 7-2, II, 3° c)", "les commandes à pression maintenue respectent les conditions suivantes", "hold-to-run controls"),
 ("Tapis roulants, escaliers et plans inclinés mécaniques", "element", "A17", "art. 8 (heading)", "Dispositions relatives aux tapis roulants, escaliers et plans inclinés mécaniques.", ""),
 ("aire d'absorption équivalente", "quantity", "A17", "art. 9, II", "L'aire d'absorption équivalente A d'un revêtement absorbant est donnée par la formule", "absorption area as % of floor area; register has reverberation time only"),
 ("sas d'isolement", "element", "A17", "annexe 2, 3.", "Cas particulier des sas d'isolement", "fire lobby; its A15 dimensions were annulled by the Conseil d'État (A15 annexe 2)"),
 ("portes à tambour, tourniquets ou sas cylindriques", "element", "A17", "art. 10, I", "notamment dans le cas de portes à tambour, tourniquets ou sas cylindriques, une porte adaptée est installée à proximité", ""),
 ("portiques de sécurité", "element", "A17", "art. 10, II, 1°", "Les portiques de sécurité ont une largeur de passage utile minimale", ""),
 ("animaux d'assistance", "user", "A17", "art. 10, II, 2°", "Le système est conçu pour pouvoir détecter des personnes de toutes tailles ainsi que les animaux d'assistance.", ""),
 ("cabinet d'aisances adapté", "room", "A17", "art. 12, I", "comporte au moins un cabinet d'aisances adapté pour les personnes handicapées circulant en fauteuil roulant", ""),
 ("sens de transfert", "concept", "A17", "art. 12, II, 1°", "Le sens de transfert est indiqué sur la porte de chaque cabinet d'aisances adapté par un pictogramme adapté.", "left/right transfer, equitably distributed"),
 ("aide au relevage", "function", "A17", "art. 12, II, 2°", "permettant le transfert d'une personne en fauteuil roulant et apportant une aide au relevage", "grab bar's sit-to-stand role"),
 ("barre d'appui latérale", "element", "A17", "art. 12, II, 2°", "une barre d'appui latérale est prévue à côté de la cuvette", ""),
 ("lave-mains", "element", "A17", "art. 12, II, 2°", "il comporte un lave-mains dont le plan supérieur est situé à une hauteur maximale", ""),
 ("disposés en batterie", "arrangement", "A17", "art. 12, II, 2°", "Lorsque des urinoirs ou des sèche-mains sont disposés en batterie, ils sont positionnés à des hauteurs différentes.", ""),
 ("Sorties", "element", "A17", "art. 13 (heading)", "Dispositions relatives aux sorties.", "ordinary exits, kept distinct from 'issues de secours'"),
 ("issues de secours", "element (distinguished)", "A17", "art. 13, II", "la signalisation indiquant la sortie ne présente aucun risque de confusion avec le repérage des issues de secours", ""),
 ("extinction est progressive", "technique", "A17", "art. 14, II", "l'extinction est progressive", "timed lighting fades out"),
 ("deux zones de détection successives se chevauchent", "technique", "A17", "art. 14, II", "deux zones de détection successives se chevauchent obligatoirement", "presence-detector overlap"),
 ("effet d'éblouissement", "hazard", "A17", "art. 14, II", "La mise en œuvre des points lumineux évite tout effet d'éblouissement direct", "glare; the register has no glare row"),
 ("établissements recevant du public assis", "building typology", "A17", "art. 16 (heading)", "Dispositions spécifiques relatives aux établissements recevant du public assis.", ""),
 ("emplacements accessibles", "space", "A17", "art. 16, II, 1°", "Le nombre d'emplacements accessibles est d'au moins 2 jusqu'à 50 places", "wheelchair spaces in seated venues"),
 ("Répartition", "provision rule", "A17", "art. 16, II, 2°", "2° Répartition :", "distribution across seat categories"),
 ("emmarchements des gradins", "element", "A17", "art. 16, II, 3°", "Les emmarchements des gradins et les gradins ne sont pas considérés comme des circulations intérieures", ""),
 ("chambres ou locaux à sommeil", "room", "A17", "art. 17, I", "comporte des chambres ou locaux à sommeil accessibles", ""),
 ("plan de couchage", "element", "A17", "art. 17, II, 2° b)", "le plan de couchage est situé à une hauteur comprise entre", "bed height"),
 ("cabines et aux espaces à usage individuel", "room", "A17", "art. 18 (heading)", "Dispositions spécifiques relatives aux cabines et aux espaces à usage individuel.", "changing, care and shower cubicles"),
 ("caisses de paiement", "element", "A17", "art. 19 (heading)", "Dispositions spécifiques relatives aux caisses de paiement", ""),
 ("prioritairement ouvert", "operational rule", "A17", "art. 19, I", "l'un d'entre eux est prioritairement ouvert", "the adapted unit is the one opened first"),
 ("carte \" mobilité inclusion \"", "legal instrument (person)", "A17", "art. 3, I", "titulaires de la carte \" mobilité inclusion \"", ""),
 ("surlongueur", "quantity", "A17", "art. 3, II, 4°", "une surlongueur de 1,20 m est matérialisée sur la voie de circulation", "rear-transfer extension of a parking bay"),
 ("appareils d'interphonie", "element", "A17", "art. 3, II, 5°", "les appareils d'interphonie sont munis d'un système permettant au personnel de l'établissement de visualiser le conducteur", ""),
 ("points d'affichage instantané", "element", "A17", "art. 11, II, 2°", "Lorsqu'il existe un ou plusieurs points d'affichage instantané, toute information sonore est doublée par une information visuelle", ""),
 ("ambiance visuelle et sonore adaptée", "concept", "A17", "art. 5, I", "le dispositif d'accueil bénéficie d'une ambiance visuelle et sonore adaptée", ""),
 ("contre-jour", "hazard", "A17", "art. 5, II", "en évitant l'effet d'éblouissement ou de contre-jour dû à l'éclairage naturel ou artificiel", "backlighting at reception, for lip-reading"),
 ("lettres bâton", "technique", "A17", "annexe 3, Compréhension", "Les informations écrites recourent autant que possible aux lettres bâton.", "sans-serif lettering"),
 ("hauteur des caractères d'écriture", "quantity", "A17", "annexe 3, Lisibilité", "la hauteur des caractères d'écriture est proportionnée aux circonstances", ""),
 ("pictogrammes normalisés", "technique", "A17", "annexe 3, Compréhension", "Lorsqu'ils existent, le recours aux pictogrammes normalisés s'impose.", ""),
 ("faciles à lire et à comprendre", "technique", "A17", "annexe 3, Compréhension", "Ces informations sont concises, faciles à lire et à comprendre.", ""),
 ("signalétique en relief", "technique", "A17", "art. 7", "par une signalétique en relief visuellement contrastée", "raised floor numbering at lift landings"),
 ("bobine d'induction captrice", "element", "A17", "annexe 9", "fonctionnant avec une bobine d'induction captrice", "hearing-aid telecoil"),
 ("niveau de bruit de fond magnétique", "quantity", "A17", "annexe 9", "le niveau de bruit de fond magnétique est tel qu'il n'altère pas la qualité d'écoute", ""),
 ("unité de vie", "defined term (dwelling)", "A15", "art. 13, I", "L'unité de vie des logements est définie de la façon suivante", "kitchen, living room, one bedroom, WC and shower room on the entry level"),
 ("caractéristiques de base des logements", "defined category", "A15", "art. 11 (heading)", "Dispositions relatives aux caractéristiques de base des logements.", ""),
 ("caractéristiques d'accessibilité et d'adaptabilité", "defined category", "A15", "art. 13", "doivent présenter les caractéristiques d'accessibilité et d'adaptabilité suivantes", "accessible now vs adaptable later"),
 ("logements évolutifs", "defined term", "A15", "art. 16 (heading)", "Dispositions relatives aux logements évolutifs.", ""),
 ("travaux simples", "defined term", "A15", "art. 16, I", "permettre la redistribution des volumes par des travaux simples", "five conditions (no structure, no shared risers, etc.)"),
 ("travaux modificatifs de l'acquéreur", "legal mechanism", "A15", "art. 17 (heading)", "Dispositions relatives aux travaux modificatifs de l'acquéreur.", ""),
 ("réversibilité", "concept", "A15", "art. 17", "la nature des interventions nécessaires pour permettre la réversibilité du logement", ""),
 ("zone de douche accessible", "space", "A15", "art. 15, I", "est équipée d'une zone de douche accessible dont l'accès se fait sans ressaut ou d'une baignoire", "a volume, may be deferred if a bath is fitted"),
 ("réservation dans le gros œuvre", "technique", "A15", "art. 13, I", "une réservation dans le gros œuvre permettant l'installation ultérieure d'un appareil élévateur vertical", ""),
 ("Balcons, terrasses et loggias", "element", "A15", "art. 14 (heading)", "Dispositions relatives aux balcons, terrasses et loggias.", ""),
 ("rejingot", "element", "A15", "art. 14, II, 2°", "la hauteur du rejingot doit être égale à la hauteur minimale admise par les règles de l'art", "upstand of the window-door sill"),
 ("dispositif de mise à niveau du plancher", "technique", "A15", "art. 14, II, 4°", "un dispositif de mise à niveau du plancher, tel qu'un caillebotis, des dalles sur plots", ""),
 ("chape flottante associée à une isolation", "construction condition", "A15", "art. 14, II, 3° a)", "lorsque le logement est muni d'une chape flottante associée à une isolation", ""),
 ("systèmes d'occultation extérieurs", "element", "A15", "art. 11, II, 2°", "des systèmes d'occultation extérieurs commandés de l'intérieur", "shutters and blinds controls"),
 ("dispositifs de manœuvre des fenêtres", "element", "A15", "art. 11, II, 2°", "les dispositifs de manœuvre des fenêtres et portes-fenêtres", ""),
 ("boîtes aux lettres", "element", "A15", "art. 9, II, 2°", "s'agissant des ensembles de boîtes aux lettres normalisées, cette obligation ne concerne que 30 % d'entre elles", ""),
 ("portier d'immeuble", "element", "A15", "art. 4, II, 1°", "notamment le portier d'immeuble et le bouton de déverrouillage de la porte", ""),
 ("appel direct par un code", "technique", "A15", "art. 4, II, 2°", "Les appareils à menu déroulant doivent permettre l'appel direct par un code.", ""),
 ("acheminement de l'image jusqu'au logement", "technique", "A15", "art. 4, II, 2°", "un système d'acheminement de l'image jusqu'au logement de nature à permettre à un occupant de visualiser ses visiteurs", "video entry"),
 ("détecteur crépusculaire", "element", "A15", "art. 10, II", "tel qu'un détecteur crépusculaire", ""),
 ("caves et celliers", "room", "A15", "art. 5, I", "Les occupants handicapés doivent pouvoir accéder à l'ensemble des locaux collectifs, caves et celliers", ""),
 ("physiques, sensorielles, cognitives, mentales ou psychiques", "population carve", "A15", "art. 1", "notamment physiques, sensorielles, cognitives, mentales ou psychiques", "five-way impairment list in housing; A17 names déficience visuelle/auditive/motrice/mentale case by case"),
 ("difficultés de repérage dans l'espace", "population carve", "A17", "annexe 6", "Elle peut également être une aide pour les personnes ayant des difficultés de repérage dans l'espace et pour les personnes présentant une déficience mentale ou cognitive.", ""),
]

def write_rev():
    bad = 0
    with open(D + '/reverse-harvest.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['phrase_verbatim (instrument own phrase)', 'kind (ours)', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'gloss_OURS_not_an_equivalence'])
        for ph, kind, ins, loc, q, g in REV:
            ok = norm(q) in TXT[ins] and norm(ph).lower() in norm(q).lower()
            if not ok: bad += 1; print('REV FAIL', ins, loc, ph, file=sys.stderr)
            w.writerow([ph, kind, 'FR', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok else 'NO', g])
    print('reverse-harvest', len(REV), 'verified', len(REV) - bad)
    return bad

def main():
    bad = write_rev(); rows = []
    for c, ph, ins, loc, q, note in OBS:
        ok_q = norm(q) in TXT[ins]
        ok_p = norm(ph).lower() in norm(q).lower()
        if not (ok_q and ok_p): bad += 1; print('FAIL', ins, loc, ph, ok_q, ok_p, file=sys.stderr)
        rows.append([c, ph, 'FR', INST[ins][0], loc, q, INST[ins][1].split('/')[-1], 'yes' if ok_q and ok_p else 'NO', note])
    with open(D + '/observations.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['concept (English register label; | = counts for each)', 'phrase_verbatim', 'language', 'instrument', 'locator', 'context_quote_verbatim', 'text_file', 'quote_verified_in_text', 'note (ours)'])
        w.writerows(rows)
    with open(D + '/coverage.tsv', 'w', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['register_concept', 'register_source', 'status', 'n_observations', 'phrases_found (distinct)', 'note'])
        for i, c in enumerate(REGISTER):
            src = 'catalogue 2.1' if i < 32 else ('catalogue 2.2' if i < 50 else 'base_parameters')
            hit = [r for r in rows if c in r[0].split('|') or (c in ALIAS and ALIAS[c] in r[0].split('|'))]
            if hit:
                ph = sorted({r[1] for r in hit})
                notes = '; '.join(sorted({r[8] for r in hit if r[8]}))
                st = 'FOUND-PARTIAL' if c in PARTIAL else 'FOUND'
                w.writerow([c, src, st, len(hit), ' / '.join(ph), (PARTIAL.get(c, '') + '; ' if c in PARTIAL else '') + notes])
            else:
                w.writerow([c, src, 'SEARCHED-ABSENT', 0, '', ABSENT.get(c, 'NO NOTE: check')])
    print('observations', len(rows), 'failures (obs+rev)', bad)
    sys.exit(1 if bad else 0)

if __name__ == '__main__':
    main()
