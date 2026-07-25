# Cross-Language Synonym Chart

**Generated:** 2026-07-25 · derived from `data/guidebook.db` (`terms` / `term_aliases` / `term_item_links`)

> **Generated file — do not hand-edit.** The database is canonical. Regenerate with
> `python3 scripts/generate_alias_chart.py`. To change vocabulary, emit a data migration
> (`scripts/emit_data_migration.py`) — never write the DB directly.

## What this is

Equivalent terms grouped under one concept, so that a search for *corridor* also finds
*hallway*, *circulation route* and *Flurbreite* — and so that two documents using
different words for the same thing are recognisably about the same thing.

`scripts/generate_search_queries.py` reads these groups to build per-language search
queries. Every slug in the corpus resolves to at least one concept.

### Relation types

| Type | Meaning |
|---|---|
| `SYNONYM` | Equivalent wording for the same concept |
| `TRANSLATION` | Primary equivalent in that language |
| `NARROWER` | A specific instance or sub-case |
| `BROADER` | The containing concept |
| `DOMAIN` | Project/population shorthand (e.g. `NDV`, `OT`) |
| `DEPRECATED` | Retained so old wording still resolves; do not use in new text |

### Provenance and limits

Non-English equivalents are **model-generated and pending native-speaker review** — they
are a *retrieval aid, not authoritative terminology*. Each row carries that status in
`term_aliases.notes`. Verification protocol: `references/native-alias-verification.md`.
Five languages required by `lang_jur_map` (AR, BN, HI, ID, SW) still carry **no aliases**
and cannot be searched until vocabulary is built from published glossaries.

**Coverage:** 88 concepts · 2381 aliases · 14 languages (of 19 required)

| EN | DE | FR | ES | IT | PT | NL | SV | NO | DA | FI | JA | ZH | KO |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 416 | 192 | 171 | 172 | 122 | 115 | 141 | 135 | 133 | 158 | 161 | 151 | 156 | 158 |

---

## Acoustic

### TERM-006 · hearing loop

Audio frequency induction loop system for hearing aid users

**English group:** `AFILS`, `T-loop`, `induction loop`, `telecoil loop`

| Lang | Equivalents |
|---|---|
| DE | Hörschleife, induktive Höranlage, Induktionsschleife |
| FR | boucle auditive, boucle à induction magnétique |
| ES | aro magnético, bucle de inducción, bucle magnético |
| IT | loop uditivo, anello a induzione magnetica |
| PT | anel de indução |
| NL | slechthorendenvoorziening, ringleiding |
| SV | teleslinga, hörslinga |
| NO | høresløyfe, teleslynge |
| DA | høresløjfe, induktionsanlæg, teleslynge |
| FI | T-silmukka, kuulosilmukka, induktiosilmukka |
| JA | 磁気ループ, ヒアリングループ |
| ZH | 助听回路, 感应线圈 |
| KO | 자기유도루프, 보청 루프 |

**Linked items:** A-10, A-10b, A-11

### TERM-007 · reverberation time

Time for sound to decay 60 dB (RT60)

**English group:** `RT60`, `decay time`

| Lang | Equivalents |
|---|---|
| DE | RT60, Nachhallzeit |
| FR | durée de réverbération, temps de réverbération |
| ES | acústica de sala, tiempo de reverberación |
| IT | acustica ambientale, tempo di riverbero |
| PT | acústica de sala, tempo de reverberação |
| NL | akoestiek, nagalmtijd |
| SV | rumsakustik, efterklangstid |
| NO | romakustikk, etterklangstid |
| DA | rumakustik, efterklangstid |
| FI | kaiunta-aika, jälkikaiunta-aika |
| JA | 残響時間 |
| ZH | 混响时间 |
| KO | 반향 시간, 잔향 시간 |

**Linked items:** A-10b, A-15

### TERM-029 · sound masking

Artificial broadband noise to mask distracting sounds

**English group:** `pink noise` *(narrower)*, `sound conditioning`, `white noise system`

| Lang | Equivalents |
|---|---|
| DE | Hintergrundbeschallung, Maskierungsgeräusch |
| FR | bruit de fond artificiel, masquage sonore |
| ES | ruido de fondo, enmascaramiento sonoro |
| IT | mascheramento acustico |
| PT | mascaramento sonoro |
| NL | geluidsmaskering |
| SV | ljudmaskering |
| NO | bakgrunnsstøy, lydmaskering |
| DA | baggrundsstøj, lydmaskering |
| FI | äänipeitto, äänimaski |
| JA | 音響マスキング, サウンドマスキング |
| ZH | 背景噪声, 声音遮蔽, 声掩蔽 |
| KO | 배경 소음, 소리 마스킹, 사운드 마스킹 |

### TERM-049 · acoustic absorption

Conversion of incident sound energy within a material rather than reflection back into the room

> **Scope:** Distinct from TERM-029 (sound masking, which ADDS sound) and TERM-007 (reverberation time, the room-level outcome absorption controls).

**English group:** `NRC` *(narrower)*, `absorption coefficient` *(narrower)*, `acoustic panel` *(narrower)*, `noise reduction coefficient` *(narrower)*, `acoustic baffling`, `acoustic damping`, `acoustic treatment`, `sound absorber`, `sound absorption`, `sound-absorbing material`

| Lang | Equivalents |
|---|---|
| DE | Absorptionsgrad, Akustikpaneel, Schallschluckung, Schallabsorption |
| FR | baffle acoustique, coefficient d'absorption, panneau acoustique, absorption acoustique |
| ES | coeficiente de absorción, panel acústico, absorción acústica |
| IT | coefficiente di assorbimento, pannello fonoassorbente, assorbimento acustico |
| PT | coeficiente de absorção, painel acústico, absorção acústica |
| NL | absorptiecoëfficiënt, akoestisch paneel, geluidsabsorptie |
| SV | absorptionsfaktor, akustikpanel, ljudabsorption |
| NO | absorpsjonsfaktor, akustikkplate, lydabsorpsjon |
| DA | absorptionskoefficient, akustikplade, lydabsorption |
| FI | absorptiosuhde, akustiikkalevy, äänenabsorptio |
| JA | 吸音パネル, 吸音率, 吸音 |
| ZH | 吸声板, 吸声系数, 吸声 |
| KO | 흡음 패널, 흡음률, 흡음 |

**Linked items:** A-02, A-06, A-10b, A-18

### TERM-050 · speech intelligibility

Proportion of speech content correctly understood by a listener in a given acoustic environment

> **Scope:** Outcome measure that RT60 (TERM-007) and absorption (TERM-049) act upon.

**English group:** `signal-to-noise ratio` *(broader)*, `%ALcons` *(narrower)*, `STI`, `intelligibility`, `speech clarity`, `speech perception`, `speech transmission index`

| Lang | Equivalents |
|---|---|
| DE | Sprachverständlichkeitsindex, Sprachverständlichkeit |
| FR | indice de transmission de la parole, intelligibilité de la parole |
| ES | índice de transmisión del habla, inteligibilidad del habla |
| IT | intelligibilità del parlato |
| PT | inteligibilidade da fala |
| NL | spraakverstaanbaarheid |
| SV | talförståelighet, taluppfattbarhet |
| NO | taleforståelighet |
| DA | taleforståelighed |
| FI | puheen ymmärrettävyys, puheen erotettavuus |
| JA | 明瞭度, 音声明瞭度 |
| ZH | 言语可懂度, 语音清晰度 |
| KO | 말소리 명료도, 음성 명료도 |

**Linked items:** A-08, A-18, B-02

## Bathroom

### TERM-008 · grab bar

Support rail for transfer and balance in bathrooms

**English group:** `assist bar`, `grab rail`, `support rail`

| Lang | Equivalents |
|---|---|
| DE | Stützklappgriff, Haltegriff, Stützgriff |
| FR | barre de maintien, barre d'appui |
| ES | asidero, barra de sujeción, barra de apoyo |
| IT | barra di appoggio, maniglione di sostegno |
| PT | barra de apoio |
| NL | steunbeugel, handgreep |
| SV | ledstång, stödhandtag |
| NO | gripestang, støttehåndtak |
| DA | håndgreb, gribebøjle, støttegreb |
| FI | käsituki, tukikahva, tukikaide |
| JA | 握りバー, 手すり |
| ZH | 安全扶手, 扶手 |
| KO | 손잡이, 지지대, 안전손잡이 |

**Linked items:** G-03, G-04, I-03

### TERM-009 · accessible bathroom

Bathroom designed for wheelchair users and people with disabilities

**English group:** `accessible toilet` *(narrower)*, `wet room` *(narrower)*, `wheelchair-accessible bathroom` *(narrower)*, `adapted bathroom`

| Lang | Equivalents |
|---|---|
| DE | rollstuhlgerechtes Bad, behindertengerechtes WC, barrierefreies Bad |
| FR | sanitaire PMR, salle de bain accessible |
| ES | aseo adaptado, baño adaptado, baño accesible |
| IT | servizio igienico per disabili, bagno accessibile |
| PT | sanitário adaptado, banheiro acessível |
| NL | miva-toilet, rolstoeltoilet, aangepast toilet |
| SV | RWC, handikapptoalett, tillgänglig toalett |
| NO | tilgjengelig toalett, universelt utformet toalett, HC-toalett |
| DA | handicap-wc, tilgængeligt toilet, handicaptoilet |
| FI | inva-wc, liikkumisesteetön wc, esteetön wc |
| JA | 車いす対応トイレ, 多機能トイレ, バリアフリートイレ |
| ZH | 残疾人卫生间, 无障碍卫生间 |
| KO | 무장애 화장실, 장애인 화장실 |

**Linked items:** G-01, G-03, G-04, I-03

### TERM-023 · anti-scald valve

Thermostatic mixing valve limiting water temperature

**English group:** `scald protection` *(broader)*, `TMV`, `thermostatic mixing valve`

| Lang | Equivalents |
|---|---|
| DE | thermostatisches Mischventil, Verbrühschutz |
| FR | protection anti-brûlure, mitigeur thermostatique |
| ES | válvula antiquemaduras, protección antiquemaduras, grifo termostático |
| IT | valvola termostatica |
| PT | válvula termostática |
| NL | thermostaatmengkraan |
| NO | termostatblander |
| DA | skoldningssikring, termostatblander |
| FI | palovammasuoja, termostaattihana |
| JA | やけど防止, サーモスタット混合水栓 |
| ZH | 恒温混合阀, 防烫阀 |
| KO | 온도 조절 수전, 화상방지밸브 |

### TERM-058 · Changing Places toilet

Larger accessible toilet with height-adjustable adult bench, hoist and space for two assistants

> **Scope:** Links item E-15. Distinct from TERM-009 (accessible bathroom), which is the standard-provision term.

**English group:** `accessible changing room`, `adult change table`, `adult changing facility`, `assisted-changing facility`, `fully accessible toilet`, `hoist-equipped toilet`

| Lang | Equivalents |
|---|---|
| DE | Pflegetoilette, Toilette für Alle |
| FR | sanitaire avec lève-personne, toilettes avec table de change adulte |
| ES | aseo asistido, aseo con cambiador de adultos |
| IT | bagno assistito, servizio igienico con lettino per adulti |
| PT | sanitário assistido, sanitário com marquesa para adultos |
| NL | verschoningsruimte voor volwassenen, Changing Places-toilet |
| SV | hygienrum, toalett med skötbord för vuxna |
| NO | stellerom, toalett med stellebenk for voksne |
| DA | pleje-toilet, toilet med voksenbriks |
| FI | esteetön hoitohuone, aikuisten hoitohuone |
| JA | ユニバーサルトイレ, 多機能トイレ（大人用ベッド付き） |
| ZH | 第三卫生间, 成人护理型无障碍卫生间 |
| KO | 다목적 화장실, 성인용 교환대 화장실 |

**Linked items:** E-15, I-04

### TERM-072 · toileting provision planning

Determining number, type and distribution of sanitary facilities across a building

> **Scope:** Quantity/distribution question. TERM-009 is the fixture-level accessible-WC term. Demand axis is TERM-036 (Toileting-proximity demand).

**English group:** `continence support` *(broader)*, `WC provision`, `restroom count`, `sanitary appliance ratio`, `sanitary provision`, `toilet accessibility ratio`, `toilet ratio`

| Lang | Equivalents |
|---|---|
| DE | WC-Bedarfsplanung, Sanitärausstattungsplanung |
| FR | nombre de toilettes, dimensionnement des sanitaires |
| ES | número de inodoros, dotación de aseos |
| IT | dotazione di servizi igienici |
| PT | dotação de sanitários |
| NL | toiletaantal, sanitaire voorzieningenplanning |
| SV | toalettantal, dimensionering av toaletter |
| NO | toalettantall, dimensjonering av toaletter |
| DA | toiletantal, dimensionering af toiletter |
| FI | käymälämäärä, wc-tilojen mitoitus |
| JA | 衛生設備計画, 便所数計画 |
| ZH | 厕位配比, 卫生间配置规划 |
| KO | 변기 수 산정, 화장실 설치 계획 |

**Linked items:** D-03, E-15, G-04

## Circulation

### TERM-001 · ramp gradient

Slope of an accessible ramp expressed as ratio or percentage

**English group:** `gradient` *(broader)*, `incline`, `ramp slope`

| Lang | Equivalents |
|---|---|
| DE | Gefälle, Steigung, Rampenneigung |
| FR | inclinaison, rampe d'accessibilité, pente de rampe |
| ES | rampa accesible, pendiente de rampa |
| IT | rampa accessibile, pendenza della rampa |
| PT | rampa de acessibilidade, inclinação de rampa |
| NL | hellingbaan, hellingspercentage |
| SV | tillgänglighetsramp, ramplutning |
| NO | tilgjengelighetsrampe, rampestigning |
| DA | stigning, tilgængelig rampe, rampehældning |
| FI | luiska, esteetön luiska, luiskan kaltevuus |
| JA | バリアフリースロープ, 傾斜路, スロープ勾配 |
| ZH | 无障碍坡道, 坡道坡度 |
| KO | 램프 경사, 경사로 기울기 |

**Linked items:** E-03

### TERM-002 · corridor width

Clear width of accessible circulation route

> **Scope:** Dimensional parameter. The element-level concept is TERM-048 (circulation route). es alias 'paso libre' is generic clear-passage wording also used for TERM-021.

**English group:** `clear width` *(narrower)*, `hallway width`, `passage width`

| Lang | Equivalents |
|---|---|
| DE | Durchgangsbreite, lichte Breite, Flurbreite |
| FR | largeur de passage, largeur de couloir |
| ES | paso libre, ancho de pasillo |
| IT | luce netta, larghezza del corridoio |
| PT | largura do corredor |
| NL | vrije doorloopbreedte, gangbreedte |
| SV | fri passagebredd, korridorbredd |
| NO | fri passasje, gangbredde |
| DA | gangareal, fri bredde, gangbredde |
| FI | kulkuväylän leveys, vapaa leveys, käytävän leveys |
| JA | 有効幅, 通路幅, 廊下幅 |
| ZH | 通道净宽, 走廊宽度 |
| KO | 통로 폭, 복도 폭 |

**Linked items:** E-08

### TERM-003 · turning circle

Minimum space for wheelchair 360° rotation

**English group:** `maneuvering clearance`, `turning space`, `wheelchair turning area`

| Lang | Equivalents |
|---|---|
| DE | Bewegungsfläche, Rollstuhlwendekreis, Wendekreis |
| FR | cercle de giration, aire de rotation |
| ES | espacio de maniobra, área de giro |
| IT | raggio di rotazione, spazio di manovra |
| PT | giro da cadeira de rodas, área de manobra |
| NL | manoeuvreerruimte, draaicirkel |
| SV | manöverutrymme, vändyta |
| NO | manøvreringsareal, snusirkel |
| DA | kørestols vendediameter, vendeareal, vendeplads |
| FI | pyörähdysympyrä, pyörätuolin kääntösäde, kääntymistila |
| JA | 車いす回転径, 回転スペース |
| ZH | 回转空间, 轮椅回转空间 |
| KO | 활동 공간, 회전 반경, 회전 공간 |

**Linked items:** E-08, E-12, G-01, G-03, G-04

### TERM-014 · accessible lift

Elevator meeting accessibility standards

**English group:** `passenger lift` *(broader)*, `wheelchair-accessible elevator` *(narrower)*, `accessible elevator`

| Lang | Equivalents |
|---|---|
| DE | Aufzug, behindertengerechter Fahrstuhl, barrierefreier Aufzug |
| FR | ascenseur PMR, ascenseur accessible |
| ES | elevador accesible, ascensor accesible |
| IT | elevatore per disabili, ascensore accessibile |
| PT | elevador acessível |
| NL | rolstoellift, toegankelijke lift |
| SV | rullstolshiss, tillgänglig hiss |
| NO | rullestolheis, tilgjengelig heis |
| DA | kørestolselevator, handicapelevator, tilgængelig elevator |
| FI | invahissi, pyörätuolihissi, esteetön hissi |
| JA | 車いす対応エレベーター, バリアフリーエレベーター |
| ZH | 残疾人电梯, 无障碍电梯 |
| KO | 무장애 엘리베이터, 장애인용 엘리베이터 |

**Linked items:** E-01, E-02

### TERM-021 · door width

Clear opening width of accessible door

> **Scope:** Dimensional parameter for door openings. es alias 'paso libre' is generic clear-passage wording also used for TERM-002.

| Lang | Equivalents |
|---|---|
| DE | lichte Durchgangsbreite, Türbreite |
| FR | passage libre, largeur de porte |
| ES | paso libre, ancho de puerta |
| IT | larghezza della porta |
| PT | largura da porta |
| NL | vrije doorgang, deurbreedte |
| SV | dörrbredd |
| NO | dørbredde |
| DA | fri døråbning, dørbredde |
| FI | oviaukon leveys, oven vapaa leveys |
| JA | 有効開口幅, ドア幅 |
| ZH | 净开口宽度, 门宽 |
| KO | 출입구 유효 폭, 문 폭 |

### TERM-022 · level threshold

Zero-step entry at doorway

**English group:** `level access` *(broader)*, `flush threshold`, `zero-step entry`

| Lang | Equivalents |
|---|---|
| DE | barrierefreie Schwelle, schwellenloser Zugang |
| FR | accès de plain-pied, seuil de niveau |
| ES | umbral enrasado |
| IT | soglia a filo |
| PT | soleira nivelada |
| NL | drempelloos |
| SV | tröskelfri |
| NO | trinnfri inngang |
| DA | trinfri adgang, niveaufri adgang |
| FI | kynnyksetön |
| JA | フラットエントリー, 段差なし |
| ZH | 无高差入口, 无障碍门槛 |
| KO | 무턱 출입구, 단차 없는 출입구 |

### TERM-027 · accessible parking

Designated parking for disabled drivers/passengers

**English group:** `handicapped parking` *(deprecated)*, `accessible bay`, `disabled parking`

| Lang | Equivalents |
|---|---|
| DE | barrierefreier Stellplatz, Behindertenparkplatz |
| FR | place handicapé, place de stationnement PMR |
| ES | plaza de aparcamiento accesible |
| IT | posto auto disabili |
| PT | vaga acessível |
| NL | gehandicaptenparkeerplaats |
| SV | handikapparkering |
| NO | HC-parkering |
| DA | tilgængelig parkeringsplads, handicapparkering |
| FI | invapysäköinti, liikkumisesteisen pysäköintipaikka |
| JA | 車いす使用者用駐車施設, 障害者用駐車場 |
| ZH | 残疾人专用停车位, 无障碍停车位 |
| KO | 장애인전용 주차구역, 장애인 주차 |

### TERM-048 · circulation route

Continuous route through a building used for horizontal movement between spaces

> **Scope:** Element-level concept. The dimensional parameter is TERM-002 (corridor width); this term groups the route itself so retrieval catches corridor/hallway/circulation wording.

**English group:** `accessible route` *(narrower)*, `aisle` *(narrower)*, `corridor width` *(narrower)*, `circulation path`, `corridor`, `hallway`, `passageway`, `path of travel`, `thoroughfare`, `walkway`

| Lang | Equivalents |
|---|---|
| DE | Erschließungsfläche, Flur, Gang, Verkehrsweg |
| FR | cheminement, couloir, dégagement, circulation |
| ES | corredor, itinerario accesible, pasillo, circulación |
| IT | corridoio, disimpegno, percorso di circolazione |
| PT | corredor, percurso acessível, circulação |
| NL | corridor, gang, looproute, verkeersroute |
| SV | gångstråk, korridor, kommunikationsyta |
| NO | gangvei, korridor, kommunikasjonsvei |
| DA | gangvej, korridor, gangareal |
| FI | kulkureitti, käytävä, kulkuväylä |
| JA | 廊下, 通路, 動線 |
| ZH | 走廊, 通道, 交通流线 |
| KO | 복도, 통로, 동선 |

**Linked items:** A-05, D-01, D-02, E-07, E-08

### TERM-052 · rest point seating

Seating provided at intervals along a route to permit recovery without leaving the route

> **Scope:** Links item E-10. Demand side is the sustained-exertion axis (TERM-043).

**English group:** `bench` *(narrower)*, `perch seat`, `respite seating`, `rest area`, `rest stop`, `resting point`, `seating provision`, `wayside seating`

| Lang | Equivalents |
|---|---|
| DE | Anlehnhilfe, Rastplatz, Sitzgelegenheit, Ruhesitzgelegenheit |
| FR | aire de repos, appui ischiatique, banc, assise de repos |
| ES | banco, área de descanso, asiento de descanso |
| IT | area di sosta, panchina, seduta di riposo |
| PT | banco, área de descanso, assento de descanso |
| NL | bank, steunleuning, zitgelegenheid, rustplek |
| SV | bänk, sittplats, viloplats |
| NO | benk, sitteplass, hvileplass |
| DA | bænk, siddeplads, hvileplads |
| FI | istuin, penkki, levähdyspaikka |
| JA | 休憩スペース, 休憩用ベンチ |
| ZH | 休息区, 长椅, 休息座椅 |
| KO | 벤치, 휴게 공간, 휴식 좌석 |

**Linked items:** D-11, E-10, G-02, G-07

### TERM-061 · headroom clearance

Unobstructed vertical dimension above a route or usable floor area

> **Scope:** Vertical counterpart to TERM-002 (corridor width). Governs tall-stature envelope and hoist runs.

**English group:** `ceiling height` *(broader)*, `TALL` *(domain)*, `soffit height` *(narrower)*, `clear height`, `head clearance`, `headway`, `overhead clearance`, `vertical clearance`

| Lang | Equivalents |
|---|---|
| DE | Durchgangshöhe, Kopffreiheit, lichte Höhe |
| FR | hauteur sous plafond, échappée, hauteur libre |
| ES | altura de paso, gálibo, altura libre |
| IT | altezza di passaggio, altezza libera |
| PT | pé-direito, altura livre |
| NL | doorloophoogte, vrije hoogte |
| SV | takhöjd, fri höjd |
| NO | takhøyde, fri høyde |
| DA | lofthøjde, fri højde |
| FI | kulkukorkeus, vapaa korkeus |
| JA | 天井高, 有効高さ |
| ZH | 净高, 净空高度 |
| KO | 천장고, 유효 높이 |

**Linked items:** E-01, I-04

### TERM-079 · mobility aid

Device supporting locomotion or transfer, setting the spatial envelope a route must accommodate

> **Scope:** TERM-016 is the person (wheelchair user); this is the equipment. Keep person and device distinct.

**English group:** `LMB` *(domain)*, `MOB` *(domain)*, `SCI` *(domain)*, `cane` *(narrower)*, `crutches` *(narrower)*, `mobility scooter` *(narrower)*, `powered wheelchair` *(narrower)*, `rollator` *(narrower)*, `walker` *(narrower)*, `walking frame` *(narrower)*, `wheelchair` *(narrower)*, `mobility device`, `walking aid`

| Lang | Equivalents |
|---|---|
| DE | Gehhilfe, Rollator, Rollstuhl, Mobilitätshilfe |
| FR | déambulateur, fauteuil roulant, aide à la mobilité |
| ES | andador, silla de ruedas, ayuda a la movilidad |
| IT | carrozzina, deambulatore, ausilio per la mobilità |
| PT | andarilho, cadeira de rodas, auxiliar de mobilidade |
| NL | rollator, rolstoel, mobiliteitshulpmiddel |
| SV | rollator, rullstol, förflyttningshjälpmedel |
| NO | rullator, rullestol, forflytningshjelpemiddel |
| DA | kørestol, rollator, ganghjælpemiddel |
| FI | pyörätuoli, rollaattori, liikkumisen apuväline |
| JA | 歩行器, 車椅子, 移動補助具 |
| ZH | 助行器, 轮椅, 助行器具 |
| KO | 보행기, 휠체어, 이동 보조기구 |

**Linked items:** E-01, E-04, E-08, E-12

## Communication

### TERM-025 · captioning

Real-time text display of speech

**English group:** `CART` *(narrower)*, `live subtitling`, `real-time captioning`

| Lang | Equivalents |
|---|---|
| DE | Echtzeit-Untertitel, Schriftdolmetschen, Untertitelung |
| FR | vélotypie, sous-titrage en temps réel |
| ES | subtítulos en directo, subtitulado, subtitulado en tiempo real |
| IT | sottotitolazione in tempo reale |
| PT | legenda em tempo real, legendagem |
| NL | schrijftolk, ondertiteling |
| SV | realtidstextning, skrivtolkning, textning |
| NO | sanntidsteksting, skrivetolking, teksting |
| DA | realtidsundertekster, skrivetolkning, undertekster |
| FI | kirjoitustulkkaus, reaaliaikainen tekstitys, tekstitys |
| JA | リアルタイム字幕, 字幕 |
| ZH | 同声字幕, 实时字幕 |
| KO | 실시간 자막, 자막 |

### TERM-026 · vibrotactile alert

Alerting system using vibration for deaf/deafblind users

**English group:** `bed shaker` *(narrower)*, `vibrating pager` *(narrower)*, `haptic alert`

| Lang | Equivalents |
|---|---|
| DE | Vibrationsalarm, vibrotaktiler Alarm |
| FR | alerte vibrotactile |
| ES | alarma por vibración, alerta vibrotáctil |
| IT | allarme vibrotattile |
| PT | alerta vibrotátil |
| NL | trilalarm |
| SV | vibrationsalarm |
| NO | vibrasjonsalarm |
| DA | taktil vibrationsalarm, vibrationsalarm |
| FI | värinähälytys, tärinähälytin |
| JA | 振動アラート, 振動式警報 |
| ZH | 触觉振动警报, 振动警报 |
| KO | 진동 경보, 진동 알림 |

### TERM-051 · AAC (augmentative and alternative communication)

Methods and devices supplementing or replacing speech for expressive communication

> **Scope:** Environmental relevance: mounting, power, acoustics, lighting and dwell space for AAC use.

**English group:** `communication board` *(narrower)*, `eye-gaze system` *(narrower)*, `speech-generating device` *(narrower)*, `symbol board` *(narrower)*, `augmentative and alternative communication`, `communication aid`

| Lang | Equivalents |
|---|---|
| DE | Kommunikationshilfe, Unterstützte Kommunikation |
| FR | aide à la communication, communication alternative et améliorée |
| ES | sistema de comunicación, comunicación aumentativa y alternativa |
| IT | comunicazione aumentativa alternativa |
| PT | comunicação aumentativa e alternativa |
| NL | communicatiehulpmiddel, ondersteunde communicatie |
| SV | alternativ och kompletterande kommunikation |
| NO | alternativ og supplerende kommunikasjon |
| DA | alternativ og supplerende kommunikation |
| FI | puhetta tukeva ja korvaava kommunikointi |
| JA | 拡大代替コミュニケーション |
| ZH | 辅助与替代沟通 |
| KO | 보완대체의사소통 |

**Linked items:** H-03, K-03

### TERM-086 · cognitive accessibility and easy read

Making information and environments usable without high literacy or processing demand

> **Scope:** Demand axis is TERM-037 (Information-access demand). 'Intellectual disability' and 'learning disability' are retrieval aliases only — never a population umbrella.

**English group:** `literacy` *(broader)*, `IntD` *(domain)*, `intellectual disability` *(domain)*, `learning disability` *(domain)*, `symbol support` *(narrower)*, `cognitive load`, `easy read`, `plain English`, `plain language`

| Lang | Equivalents |
|---|---|
| DE | kognitive Barrierefreiheit, Leichte Sprache |
| FR | FALC, accessibilité cognitive, facile à lire et à comprendre |
| ES | accesibilidad cognitiva, lectura fácil |
| IT | accessibilità cognitiva, lettura facilitata |
| PT | acessibilidade cognitiva, leitura fácil |
| NL | begrijpelijke taal, eenvoudige taal |
| SV | kognitiv tillgänglighet, lättläst |
| NO | kognitiv tilgjengelighet, lettlest |
| DA | kognitiv tilgængelighed, letlæst |
| FI | kognitiivinen saavutettavuus, selkokieli |
| JA | 認知的アクセシビリティ, わかりやすい情報 |
| ZH | 认知无障碍, 易读易懂 |
| KO | 인지 접근성, 읽기 쉬운 자료 |

**Linked items:** D-04, D-08, H-03

## Economics

### TERM-064 · home adaptation grant

Public funding instrument financing accessibility modification of an existing dwelling

> **Scope:** Jurisdiction-specific instruments; named schemes are NARROWER aliases, not equivalents.

**English group:** `DFG` *(narrower)*, `Disabled Facilities Grant` *(narrower)*, `accessibility grant`, `adaptation subsidy`, `home modification funding`, `housing adaptation scheme`, `retrofit funding`

| Lang | Equivalents |
|---|---|
| DE | Zuschuss für barrierefreien Umbau, Wohnungsanpassungszuschuss |
| FR | aide à l'adaptation, subvention d'adaptation du logement |
| ES | ayuda a la adaptación, subvención de adaptación de la vivienda |
| IT | contributo per l'adattamento dell'alloggio |
| PT | subsídio de adaptação da habitação |
| NL | woningaanpassingssubsidie |
| SV | bostadsanpassningsbidrag |
| NO | tilskudd til boligtilpasning |
| DA | boligindretningsstøtte |
| FI | asunnon muutostyöavustus |
| JA | 住宅改修助成 |
| ZH | 住宅无障碍改造补贴 |
| KO | 주택 개조 지원금 |

### TERM-065 · accessibility economics

Cost, benefit and value analysis applied to accessibility provision

> **Scope:** Doctrine caution: economic framing supports advocacy but never substitutes for rights obligations.

**English group:** `cost of inaction` *(narrower)*, `cost-benefit analysis` *(narrower)*, `lifecycle cost` *(narrower)*, `market value uplift` *(narrower)*, `return on investment` *(narrower)*, `willingness to pay` *(narrower)*, `business case`, `economic appraisal`

| Lang | Equivalents |
|---|---|
| DE | Kosten-Nutzen-Analyse, Wirtschaftlichkeit der Barrierefreiheit |
| FR | analyse coût-bénéfice, économie de l'accessibilité |
| ES | análisis coste-beneficio, economía de la accesibilidad |
| IT | analisi costi-benefici, economia dell'accessibilità |
| PT | análise custo-benefício, economia da acessibilidade |
| NL | kosten-batenanalyse, economie van toegankelijkheid |
| SV | kostnads-nyttoanalys, tillgänglighetens ekonomi |
| NO | kostnad-nytte-analyse, tilgjengelighetsøkonomi |
| DA | cost-benefit-analyse, tilgængelighedsøkonomi |
| FI | kustannus-hyötyanalyysi, esteettömyyden taloudellisuus |
| JA | 費用便益分析, アクセシビリティの経済性 |
| ZH | 成本效益分析, 无障碍经济性 |
| KO | 비용편익 분석, 접근성 경제성 |

### TERM-066 · construction cost

Capital expenditure to build or modify, used to quantify the incremental cost of accessibility

> **Scope:** The incremental-cost figure, not total build cost, is the advocacy-relevant quantity.

**English group:** `cost per square metre` *(narrower)*, `cost uplift` *(narrower)*, `incremental cost` *(narrower)*, `build cost`, `capital cost`, `construction budget`, `tender price`

| Lang | Equivalents |
|---|---|
| DE | Herstellungskosten, Baukosten |
| FR | coût des travaux, coût de construction |
| ES | coste de obra, coste de construcción |
| IT | costo di costruzione |
| PT | custo de construção |
| NL | bouwkosten |
| SV | byggkostnad |
| NO | byggekostnad |
| DA | byggeomkostninger |
| FI | rakennuskustannukset |
| JA | 工事費, 建設費 |
| ZH | 工程造价, 建造成本 |
| KO | 공사비, 건설 비용 |

## Education

### TERM-070 · school learning environment

Educational setting considered as a designed environment affecting access to learning

> **Scope:** Links item A-18 (RT60 in learning and listening spaces).

**English group:** `campus` *(broader)*, `classroom` *(narrower)*, `lecture hall` *(narrower)*, `educational setting`, `learning space`, `school building`, `teaching space`

| Lang | Equivalents |
|---|---|
| DE | Klassenzimmer, Schulgebäude, Lernumgebung |
| FR | salle de classe, établissement scolaire, environnement d'apprentissage |
| ES | aula, centro educativo, entorno de aprendizaje |
| IT | aula scolastica, ambiente di apprendimento |
| PT | sala de aula, ambiente de aprendizagem |
| NL | klaslokaal, schoolgebouw, leeromgeving |
| SV | klassrum, skolbyggnad, lärmiljö |
| NO | klasserom, skolebygg, læringsmiljø |
| DA | klasselokale, skolebygning, læringsmiljø |
| FI | koulurakennus, luokkahuone, oppimisympäristö |
| JA | 学校施設, 教室, 学習環境 |
| ZH | 教室, 校园建筑, 学习环境 |
| KO | 교실, 학교 시설, 학습 환경 |

**Linked items:** A-18, B-03, D-05

## Fire Safety

### TERM-013 · visual fire alarm

Strobe/flashing light fire alarm for deaf/HoH users

**English group:** `VAD`, `beacon alarm`, `strobe alarm`, `visual alarm device`

| Lang | Equivalents |
|---|---|
| DE | Alarmlicht, Blitzleuchte, optischer Feueralarm |
| FR | flash lumineux d'alarme, alarme incendie visuelle |
| ES | señal luminosa de alarma, alarma visual contra incendios |
| IT | segnalatore ottico di allarme, allarme antincendio visivo |
| PT | sinalizador luminoso, alarme visual de incêndio |
| NL | flitslichtalarm, optisch brandalarm |
| SV | blixtljuslarm, optiskt brandlarm |
| NO | blinklysbrannalarm, optisk brannalarm |
| DA | blinklysbrandalarm, lysalarm, optisk brandalarm |
| FI | optinen palohälytin, valohälytin, vilkkuva palohälytin |
| JA | 光警報装置, 視覚警報装置 |
| ZH | 光报警器, 闪光火灾报警器 |
| KO | 광경보기, 시각경보기 |

**Linked items:** B-10

## Functional Axis

### TERM-031 · Ambulant movement

ambulant walking mobility gait

> **Scope:** Functional axis AX-AMB (governance/functional-taxonomy.md); linked axis_code=AX-AMB

| Lang | Equivalents |
|---|---|
| DE | Gehfähigkeit |
| FR | mobilité à la marche |
| ES | marcha |
| JA | 歩行 |
| ZH | 步行能力 |
| KO | 보행 |

### TERM-032 · Arousal-safety demand

arousal regulation safety sensory

> **Scope:** Functional axis AX-ARO (governance/functional-taxonomy.md); linked axis_code=AX-ARO

| Lang | Equivalents |
|---|---|
| DE | Aktivierungsregulation |
| FR | régulation de l'éveil |
| ES | regulación de la activación |

### TERM-033 · Auditory access & alerting demand

auditory access hearing alerting

> **Scope:** Functional axis AX-AUD (governance/functional-taxonomy.md); linked axis_code=AX-AUD

| Lang | Equivalents |
|---|---|
| DE | auditive Zugänglichkeit |
| FR | accès auditif |
| ES | acceso auditivo |
| JA | 聴覚アクセス |
| ZH | 听觉可及性 |
| KO | 청각 접근 |

### TERM-034 · Balance & postural demand

balance postural equilibrium

> **Scope:** Functional axis AX-BAL (governance/functional-taxonomy.md); linked axis_code=AX-BAL

| Lang | Equivalents |
|---|---|
| DE | Gleichgewicht |
| FR | équilibre |
| ES | equilibrio |
| JA | 平衡 |
| ZH | 平衡 |
| KO | 균형 |

### TERM-035 · Airborne-exposure demand

airborne chemical exposure air quality

> **Scope:** Functional axis AX-CHM (governance/functional-taxonomy.md); linked axis_code=AX-CHM

| Lang | Equivalents |
|---|---|
| DE | Luftschadstoffbelastung |
| FR | exposition aux polluants atmosphériques |
| ES | exposición a contaminantes del aire |

### TERM-036 · Toileting-proximity demand

toileting proximity continence

> **Scope:** Functional axis AX-CNT (governance/functional-taxonomy.md); linked axis_code=AX-CNT

| Lang | Equivalents |
|---|---|
| DE | Toilettennähe |
| FR | accès aux toilettes |
| ES | acceso al aseo |

### TERM-037 · Information-access demand

information access cognitive easy-read

> **Scope:** Functional axis AX-COG-L (governance/functional-taxonomy.md); linked axis_code=AX-COG-L

| Lang | Equivalents |
|---|---|
| DE | Informationszugang |
| FR | accès à l'information |
| ES | acceso a la información |

### TERM-038 · Orientation demand

orientation wayfinding

> **Scope:** Functional axis AX-COG-O. The design-system term is TERM-028 (wayfinding); ko alias '길찾기' is shared between them.

| Lang | Equivalents |
|---|---|
| DE | Orientierung |
| FR | orientation |
| ES | orientación |
| JA | 道案内 |
| ZH | 寻路 |
| KO | 길찾기 |

### TERM-039 · Expressive-communication demand

expressive communication AAC

> **Scope:** Functional axis AX-COM-E (governance/functional-taxonomy.md); linked axis_code=AX-COM-E

| Lang | Equivalents |
|---|---|
| DE | unterstützte Kommunikation |
| FR | communication expressive |
| ES | comunicación expresiva |

### TERM-040 · Pain-load demand

pain load

> **Scope:** Functional axis AX-PAI (governance/functional-taxonomy.md); linked axis_code=AX-PAI

| Lang | Equivalents |
|---|---|
| DE | Schmerz |
| FR | douleur |
| ES | dolor |
| JA | 疼痛 |
| ZH | 疼痛 |
| KO | 통증 |

### TERM-041 · Reach & manipulation

reach manipulation dexterity

> **Scope:** Functional axis AX-REA (governance/functional-taxonomy.md); linked axis_code=AX-REA

| Lang | Equivalents |
|---|---|
| DE | Reichweite und Greifen |
| FR | portée et préhension |
| ES | alcance y manipulación |
| JA | 上肢リーチ・操作 |
| ZH | 伸取与操作 |
| KO | 손 뻗기·조작 |

### TERM-042 · Sensory-load demand

sensory load overload processing

> **Scope:** Functional axis AX-SEN. NOT the experienced event — that is TERM-020 (sensory overload). Shared non-EN aliases are expected; the axis is the demand layer.

| Lang | Equivalents |
|---|---|
| DE | sensorische Reizüberflutung |
| FR | surcharge sensorielle |
| ES | sobrecarga sensorial |
| JA | 感覚過負荷 |
| ZH | 感官负荷 |
| KO | 감각과부하 |

### TERM-043 · Sustained-exertion demand

sustained exertion fatigue post-exertional

> **Scope:** Functional axis AX-STA (governance/functional-taxonomy.md); linked axis_code=AX-STA

| Lang | Equivalents |
|---|---|
| DE | Belastungsintoleranz |
| FR | fatigue à l'effort |
| ES | fatiga por esfuerzo |

### TERM-044 · Thermal demand

thermal temperature regulation

> **Scope:** Functional axis AX-THR (governance/functional-taxonomy.md); linked axis_code=AX-THR

| Lang | Equivalents |
|---|---|
| DE | Temperaturregulation |
| FR | régulation thermique |
| ES | regulación térmica |
| JA | 体温調節 |
| ZH | 温度调节 |
| KO | 체온조절 |

### TERM-045 · Low-vision information demand

low vision partial sight

> **Scope:** Functional axis AX-VIS-L (governance/functional-taxonomy.md); linked axis_code=AX-VIS-L

| Lang | Equivalents |
|---|---|
| DE | Sehbehinderung |
| FR | basse vision |
| ES | baja visión |
| JA | ロービジョン |
| ZH | 低视力 |
| KO | 저시력 |

### TERM-046 · Non-visual information demand

non-visual blindness

> **Scope:** Functional axis AX-VIS-N (governance/functional-taxonomy.md); linked axis_code=AX-VIS-N

| Lang | Equivalents |
|---|---|
| DE | nicht-visuelle Zugänglichkeit |
| FR | accès non visuel |
| ES | acceso no visual |
| JA | 非視覚アクセス |
| ZH | 非视觉获取 |
| KO | 비시각 접근 |

### TERM-047 · Wheeled movement & transfer

wheelchair wheeled mobility transfer

> **Scope:** Functional axis AX-WHM (governance/functional-taxonomy.md); linked axis_code=AX-WHM

| Lang | Equivalents |
|---|---|
| DE | Rollstuhlmobilität |
| FR | mobilité en fauteuil roulant |
| ES | movilidad en silla de ruedas |
| JA | 車椅子移動 |
| ZH | 轮椅移动 |
| KO | 휠체어이동 |

## Hardware

### TERM-004 · lever handle

Door handle operable without grip/twist motion

**English group:** `accessible door handle` *(broader)*, `door lever`, `lever door handle`

| Lang | Equivalents |
|---|---|
| DE | Hebeltürgriff, Türklinke, Türdrücker |
| FR | béquille de porte, poignée à levier |
| ES | tirador de puerta, manilla tipo palanca |
| IT | maniglione, maniglia a leva |
| PT | maçaneta tipo alavanca |
| NL | hefboomgreep, deurkruk |
| SV | dörrhandtag, trycke |
| NO | vriderhåndtak, dørhåndtak |
| DA | dørgreb, vippegreb, greb |
| FI | oven painike, vipukahva, painike |
| JA | ドアレバー, レバーハンドル |
| ZH | 无障碍门把手, 杠杆门把手 |
| KO | 문 손잡이, 레버 핸들 |

**Linked items:** H-01, I-01

### TERM-005 · operating force

Maximum force required to operate hardware

**English group:** `opening force` *(narrower)*, `actuation force`

| Lang | Equivalents |
|---|---|
| DE | Betätigungskraft, Bedienkraft |
| FR | effort d'ouverture, force de manœuvre |
| ES | fuerza de accionamiento, fuerza de operación |
| IT | forza operativa, forza di azionamento |
| PT | força de operação |
| NL | openingskracht, bedieningskracht |
| SV | öppningskraft, manöverkraft |
| NO | åpningskraft, betjeningskraft |
| DA | åbningskraft, betjeningskraft |
| FI | avausvoima, käyttövoima |
| JA | 操作力 |
| ZH | 开启力, 操作力 |
| KO | 개폐력, 조작력 |

**Linked items:** H-01, H-02, I-01

### TERM-084 · laundry and utility room

Domestic utility space; appliance reach, transfer space and control access govern its usability

> **Scope:** Residential DAR-relevant: appliance height and front-loading are adaptation-sensitive.

**English group:** `appliance access height` *(narrower)*, `drying space` *(narrower)*, `front-loading appliance` *(narrower)*, `washing machine` *(narrower)*, `laundry`, `utility room`

| Lang | Equivalents |
|---|---|
| DE | Waschküche, Hauswirtschaftsraum |
| FR | local technique, buanderie |
| ES | cuarto de servicio, lavadero |
| IT | locale tecnico, lavanderia |
| PT | lavandaria |
| NL | bijkeuken, wasruimte |
| SV | grovkök, tvättstuga |
| NO | vaskerom |
| DA | vaskerum, bryggers |
| FI | pesutupa, kodinhoitohuone |
| JA | 家事室, 洗濯室 |
| ZH | 家务间, 洗衣房 |
| KO | 다용도실, 세탁실 |

**Linked items:** G-05, H-01, I-02

### TERM-088 · upper limb function and grip

Hand, wrist and arm capability governing operable force, grip type and one-handed use

> **Scope:** Demand axis is TERM-041 (Reach & manipulation). Operating force is TERM-005.

**English group:** `LMB` *(domain)*, `closed-fist operable` *(narrower)*, `pinch grip` *(narrower)*, `dexterity`, `grip strength`, `hand function`, `one-handed operation`, `upper limb`

| Lang | Equivalents |
|---|---|
| DE | Einhandbedienung, Greifkraft, Funktion der oberen Extremität |
| FR | force de préhension, utilisation à une main, fonction du membre supérieur |
| ES | fuerza de agarre, uso con una mano, función del miembro superior |
| IT | forza di presa, funzione dell'arto superiore |
| PT | força de preensão, função do membro superior |
| NL | eenhandige bediening, grijpkracht, functie van de bovenste extremiteit |
| SV | enhandsmanövrering, greppstyrka, övre extremitetens funktion |
| NO | enhåndsbetjening, gripestyrke, funksjon i overekstremitet |
| DA | enhåndsbetjening, gribestyrke, overekstremitetsfunktion |
| FI | puristusvoima, yhden käden käyttö, yläraajan toiminta |
| JA | 握力, 片手操作, 上肢機能 |
| ZH | 单手操作, 握力, 上肢功能 |
| KO | 악력, 한 손 조작, 상지 기능 |

**Linked items:** H-01, H-05, I-01, I-02

## Housing

### TERM-068 · accessible housing

Dwelling designed or adapted for full use by disabled occupants, not merely visitable

> **Scope:** Full-use standard; TERM-059 (visitability) is the lower threshold.

**English group:** `social housing` *(broader)*, `Co-1` *(domain)*, `supported housing` *(narrower)*, `wheelchair-accessible home` *(narrower)*, `accessible dwelling`, `adapted housing`, `barrier-free dwelling`, `residential accessibility`

| Lang | Equivalents |
|---|---|
| DE | rollstuhlgerechte Wohnung, barrierefreies Wohnen |
| FR | logement adapté, logement accessible |
| ES | vivienda adaptada, vivienda accesible |
| IT | abitazione adattata, alloggio accessibile |
| PT | habitação adaptada, habitação acessível |
| NL | aangepaste woning, toegankelijke woning |
| SV | anpassad bostad, tillgänglig bostad |
| NO | tilpasset bolig, tilgjengelig bolig |
| DA | tilpasset bolig, tilgængelig bolig |
| FI | muunneltava asunto, esteetön asunto |
| JA | 車椅子対応住宅, バリアフリー住宅 |
| ZH | 轮椅可达住宅, 无障碍住宅 |
| KO | 장애인 편의주택, 무장애 주택 |

## Legal

### TERM-067 · CRPD (Convention on the Rights of Persons with Disabilities)

UN human-rights treaty establishing accessibility and participation obligations

> **Scope:** Art. 9 (accessibility) and Art. 4.3 (participation) are the doctrinal anchors for Co-1 evidence.

**English group:** `disability rights treaty` *(broader)*, `Article 9` *(narrower)*, `General Comment No. 2` *(narrower)*, `accessibility obligation` *(narrower)*, `reasonable accommodation` *(narrower)*, `Convention on the Rights of Persons with Disabilities`, `UNCRPD`

| Lang | Equivalents |
|---|---|
| DE | UN-BRK, UN-Behindertenrechtskonvention |
| FR | CDPH, Convention relative aux droits des personnes handicapées |
| ES | CDPD, Convención sobre los Derechos de las Personas con Discapacidad |
| IT | Convenzione sui diritti delle persone con disabilità |
| PT | CDPD, Convenção sobre os Direitos das Pessoas com Deficiência |
| NL | VN-Gehandicaptenverdrag, VN-Verdrag handicap |
| SV | FN:s konvention om rättigheter för personer med funktionsnedsättning |
| NO | FN-konvensjonen om rettighetene til mennesker med nedsatt funksjonsevne |
| DA | FN's handicapkonvention |
| FI | YK:n vammaissopimus |
| JA | 障害者権利条約 |
| ZH | 残疾人权利公约 |
| KO | 장애인권리협약 |

### TERM-075 · jurisdictional accessibility standards

Nationally or regionally binding accessibility requirements in codes and standards

> **Scope:** Regulatory stratum (T4-T6). Code convergence is NOT evidence — see governance/tier-system.md.

**English group:** `ADA` *(domain)*, `EAA` *(domain)*, `Americans with Disabilities Act` *(narrower)*, `European Accessibility Act` *(narrower)*, `scope clarification` *(narrower)*, `accessibility regulation`, `building code`, `code provision`, `national standard`, `regulatory requirement`, `statutory requirement`, `technical standard`

| Lang | Equivalents |
|---|---|
| DE | Bauordnung, Barrierefreiheitsnormen |
| FR | réglementation de la construction, normes d'accessibilité |
| ES | código técnico, normativa de accesibilidad |
| IT | norme tecniche, normativa sull'accessibilità |
| PT | regulamento, normas de acessibilidade |
| NL | bouwbesluit, toegankelijkheidsnormen |
| SV | byggregler, tillgänglighetsregler |
| NO | byggteknisk forskrift, tilgjengelighetskrav |
| DA | bygningsreglement, tilgængelighedskrav |
| FI | rakentamismääräykset, esteettömyysmääräykset |
| JA | 建築基準, アクセシビリティ基準 |
| ZH | 建筑规范, 无障碍标准 |
| KO | 건축 기준, 접근성 기준 |

## Lighting

### TERM-018 · circadian lighting

Lighting designed to support human circadian rhythm

**English group:** `EML` *(narrower)*, `melanopic lighting` *(narrower)*, `biodynamic lighting`, `human-centric lighting`

| Lang | Equivalents |
|---|---|
| DE | Human Centric Lighting, biologisch wirksame Beleuchtung, zirkadiane Beleuchtung |
| FR | éclairage centré sur l'humain, éclairage circadien |
| ES | iluminación centrada en las personas, iluminación circadiana |
| IT | Human Centric Lighting, illuminazione circadiana |
| PT | iluminação centrada no ser humano, iluminação circadiana |
| NL | mensgerichte verlichting, circadiane verlichting |
| SV | människocentrerad belysning, dygnsrytmbelysning |
| NO | menneskesentrert belysning, døgnrytmebelysning |
| DA | biologisk effektiv belysning, menneskecentreret belysning, døgnrytmebelysning |
| FI | biologisesti vaikuttava valaistus, ihmiskeskeinen valaistus, vuorokausirytmivalaistus |
| JA | 概日リズム照明, サーカディアン照明 |
| ZH | 视黑素等效日光照度, 人因照明, 生物节律照明 |
| KO | 인간중심조명, 생체리듬 조명 |

**Linked items:** B-01, B-02

### TERM-024 · colour temperature

Warmth/coolness of light measured in Kelvin

**English group:** `CCT`, `correlated colour temperature`

| Lang | Equivalents |
|---|---|
| DE | Kelvin, Farbtemperatur |
| FR | température de couleur |
| ES | temperatura de color |
| IT | temperatura colore |
| NL | kleurtemperatuur |
| SV | färgtemperatur |
| NO | fargetemperatur |
| DA | farvetemperatur |
| FI | värilämpötila |
| JA | 色温度 |
| ZH | 光源色温, 色温 |
| KO | 조명 색온도, 색온도 |

## Medical

### TERM-015 · thermoregulation impairment

Inability to regulate body temperature (SCI, MS)

**English group:** `autonomic dysreflexia` *(narrower)*, `poikilothermia` *(narrower)*, `thermal dysregulation`

| Lang | Equivalents |
|---|---|
| DE | autonome Dysreflexie, Thermoregulationsstörung |
| FR | trouble de la thermorégulation |
| ES | alteración de la regulación térmica, deterioro de la termorregulación |
| IT | disturbo della termoregolazione |
| PT | distúrbio da termorregulação |
| NL | thermoregulatiestoornis |
| SV | termoregleringsrubbning |
| NO | termoreguleringsforstyrrelse |
| DA | nedsat temperaturregulering, termoreguleringsforstyrrelse |
| FI | lämpötilan säätelyn häiriö, lämmönsäätelyhäiriö |
| JA | 体温調節障害 |
| ZH | 温度感知障碍, 体温调节障碍 |
| KO | 온도 조절 장애, 체온조절장애 |

**Linked items:** I-03, K-05

### TERM-020 · sensory overload

Overwhelming sensory input causing distress/shutdown

> **Scope:** Content term: the experienced event of sensory overload. NOT the demand axis — the axis is TERM-042 (Sensory-load demand). Some non-EN aliases are shared; disambiguate by domain when expanding queries.

**English group:** `overstimulation`, `sensory flooding`, `sensory overwhelm`

| Lang | Equivalents |
|---|---|
| DE | sensorische Überlastung, Reizüberflutung |
| FR | hyperstimulation, surcharge sensorielle |
| ES | sobreestimulación, sobrecarga sensorial |
| IT | iperstimolazione, sovraccarico sensoriale |
| PT | hiperestimulação, sobrecarga sensorial |
| NL | sensorische overbelasting, prikkeloverbelasting |
| SV | sensorisk överbelastning, sinnesöverbelastning |
| NO | sanseoverbelastning, sanseoverstimulering |
| DA | sanseoverbelastning, sanseoverstimulering |
| FI | aistiylikuormitus, aistiärsykkeiden ylikuormitus, aistikuormitus |
| JA | 感覚過負荷 |
| ZH | 感觉过载, 感官超载 |
| KO | 감각 과민, 감각 과부하 |

**Linked items:** A-13, A-16, F-01, F-03

### TERM-053 · fatigue and post-exertional malaise

Reduced capacity for sustained activity, including symptom exacerbation following exertion

> **Scope:** Symptom/mechanism term, NOT a population label — do not use as an umbrella population code (see governance/functional-taxonomy.md §3.3). Demand axis is TERM-043.

**English group:** `OFS` *(domain)*, `PEM`, `energy limitation`, `exertion intolerance`, `fatigability`, `payback`, `post-exertional malaise`, `symptom crash`

| Lang | Equivalents |
|---|---|
| DE | Belastungsintoleranz, post-exertionelle Malaise, Fatigue |
| FR | intolérance à l'effort, malaise post-effort, fatigue |
| ES | intolerancia al esfuerzo, malestar post-esfuerzo, fatiga |
| IT | malessere post-sforzo, affaticamento |
| PT | mal-estar pós-esforço, fadiga |
| NL | inspanningsintolerantie, post-exertionele malaise, vermoeidheid |
| SV | ansträngningsutlöst försämring, uttröttbarhet |
| NO | anstrengelsesutløst sykdomsfølelse, utmattelse |
| DA | anstrengelsesudløst forværring, udtrætning |
| FI | rasituksen jälkeinen huonovointisuus, uupumus |
| JA | 労作後倦怠感, 疲労 |
| ZH | 劳累后不适, 疲劳 |
| KO | 운동 후 권태, 피로 |

**Linked items:** E-03, E-10, F-05

### TERM-054 · dysautonomia and orthostatic intolerance

Autonomic dysfunction producing symptoms on upright posture, including tachycardia and presyncope

> **Scope:** Environmental relevance: queueing, standing dwell time, seating availability, thermal load.

**English group:** `OFS` *(domain)*, `orthostatic hypotension` *(narrower)*, `presyncope` *(narrower)*, `syncope` *(narrower)*, `POTS`, `autonomic dysfunction`, `orthostatic intolerance`, `postural orthostatic tachycardia syndrome`

| Lang | Equivalents |
|---|---|
| DE | orthostatische Intoleranz, Dysautonomie |
| FR | intolérance orthostatique, dysautonomie |
| ES | intolerancia ortostática, disautonomía |
| IT | intolleranza ortostatica, disautonomia |
| PT | intolerância ortostática, disautonomia |
| NL | orthostatische intolerantie, dysautonomie |
| SV | ortostatisk intolerans, dysautonomi |
| NO | ortostatisk intoleranse, dysautonomi |
| DA | ortostatisk intolerans, dysautonomi |
| FI | ortostaattinen intoleranssi, dysautonomia |
| JA | 起立不耐症, 自律神経障害 |
| ZH | 直立不耐受, 自主神经功能障碍 |
| KO | 기립성 불내성, 자율신경 실조 |

**Linked items:** E-10, F-05, G-02

### TERM-055 · chronic pain

Pain persisting beyond expected healing time, or continuous/recurrent pain affecting function

> **Scope:** Symptom term. The demand axis is TERM-040 (Pain-load demand); keep the two distinct.

**English group:** `PAIN` *(domain)*, `musculoskeletal pain` *(narrower)*, `neuropathic pain` *(narrower)*, `nociplastic pain` *(narrower)*, `chronic primary pain`, `pain load`, `persistent pain`

| Lang | Equivalents |
|---|---|
| DE | Dauerschmerz, chronischer Schmerz |
| FR | douleur persistante, douleur chronique |
| ES | dolor persistente, dolor crónico |
| IT | dolore persistente, dolore cronico |
| PT | dor persistente, dor crónica |
| NL | aanhoudende pijn, chronische pijn |
| SV | kronisk smärta, långvarig smärta |
| NO | kronisk smerte, langvarig smerte |
| DA | kroniske smerter, langvarige smerter |
| FI | krooninen kipu, pitkäaikainen kipu |
| JA | 慢性痛, 慢性疼痛 |
| ZH | 持续性疼痛, 慢性疼痛 |
| KO | 지속성 통증, 만성 통증 |

**Linked items:** F-05, G-02, G-05

### TERM-056 · vestibular dysfunction

Impairment of the vestibular system affecting balance, gaze stability and spatial orientation

> **Scope:** Environmental relevance: floor pattern, visual flow, handrail continuity, lighting transitions. Demand axis is TERM-034 (Balance & postural demand).

**English group:** `VES` *(domain)*, `BPPV` *(narrower)*, `Ménière's disease` *(narrower)*, `vestibular hypofunction` *(narrower)*, `visually-induced vertigo` *(narrower)*, `balance disorder`, `dizziness`, `unsteadiness`, `vertigo`

| Lang | Equivalents |
|---|---|
| DE | Gleichgewichtsstörung, Schwindel, vestibuläre Störung |
| FR | trouble de l'équilibre, vertige, trouble vestibulaire |
| ES | trastorno del equilibrio, vértigo, disfunción vestibular |
| IT | vertigine, disfunzione vestibolare |
| PT | vertigem, disfunção vestibular |
| NL | duizeligheid, evenwichtsstoornis, vestibulaire stoornis |
| SV | balansstörning, yrsel, vestibulär dysfunktion |
| NO | balanseforstyrrelse, svimmelhet, vestibulær dysfunksjon |
| DA | balanceforstyrrelse, svimmelhed, vestibulær dysfunktion |
| FI | huimaus, tasapainohäiriö, vestibulaarinen häiriö |
| JA | めまい, 平衡障害, 前庭機能障害 |
| ZH | 平衡障碍, 眩晕, 前庭功能障碍 |
| KO | 어지럼증, 평형 장애, 전정 기능 장애 |

**Linked items:** B-05, C-03, C-06, E-07

### TERM-057 · tremor and involuntary movement

Involuntary motor activity affecting precision, control and sustained positioning

> **Scope:** Environmental relevance: control targets, hardware forces, dwell distances. Demand axis is TERM-041 (Reach & manipulation).

**English group:** `motor control` *(broader)*, `MOVE` *(domain)*, `ataxia` *(narrower)*, `athetosis` *(narrower)*, `dyskinesia` *(narrower)*, `dystonia` *(narrower)*, `essential tremor` *(narrower)*, `spasticity` *(narrower)*, `involuntary movement`

| Lang | Equivalents |
|---|---|
| DE | Ataxie, Spastik, unwillkürliche Bewegung, Tremor |
| FR | ataxie, mouvement involontaire, spasticité, tremblement |
| ES | ataxia, espasticidad, movimiento involuntario, temblor |
| IT | movimento involontario, spasticità, tremore |
| PT | espasticidade, movimento involuntário, tremor |
| NL | onwillekeurige beweging, spasticiteit, tremor |
| SV | ofrivillig rörelse, spasticitet, tremor |
| NO | spastisitet, ufrivillig bevegelse, tremor |
| DA | spasticitet, ufrivillig bevægelse, tremor |
| FI | spastisuus, tahaton liike, vapina |
| JA | 不随意運動, 痙縮, 振戦 |
| ZH | 不自主运动, 痉挛, 震颤 |
| KO | 경직, 불수의 운동, 진전 |

**Linked items:** H-01, H-05, I-01

### TERM-080 · neurological impairment

Impairment arising from nervous-system conditions, with variable and often fluctuating presentation

> **Scope:** Named conditions are NARROWER aliases for retrieval only — never a population umbrella (see CLAUDE.md §10, work from axes).

**English group:** `MOVE` *(domain)*, `MS` *(domain)*, `NEU` *(domain)*, `Parkinson's disease` *(narrower)*, `acquired brain injury` *(narrower)*, `cerebral palsy` *(narrower)*, `epilepsy` *(narrower)*, `motor neurone disease` *(narrower)*, `multiple sclerosis` *(narrower)*, `stroke` *(narrower)*, `neurological condition`

| Lang | Equivalents |
|---|---|
| DE | Multiple Sklerose, Schlaganfall, neurologische Beeinträchtigung |
| FR | AVC, sclérose en plaques, atteinte neurologique |
| ES | esclerosis múltiple, ictus, afectación neurológica |
| IT | ictus, sclerosi multipla, compromissione neurologica |
| PT | AVC, esclerose múltipla, comprometimento neurológico |
| NL | beroerte, multiple sclerose, neurologische aandoening |
| SV | multipel skleros, stroke, neurologisk funktionsnedsättning |
| NO | hjerneslag, multippel sklerose, nevrologisk funksjonsnedsettelse |
| DA | apopleksi, dissemineret sklerose, neurologisk funktionsnedsættelse |
| FI | MS-tauti, aivohalvaus, neurologinen toimintarajoite |
| JA | 多発性硬化症, 脳卒中, 神経系機能障害 |
| ZH | 多发性硬化, 脑卒中, 神经功能障碍 |
| KO | 뇌졸중, 다발성 경화증, 신경학적 장애 |

**Linked items:** A-13, B-04, E-03

## Methodology

### TERM-017 · universal design

Design usable by all people without adaptation

**English group:** `barrier-free design`, `design for all`, `inclusive design`

| Lang | Equivalents |
|---|---|
| DE | Design für Alle, barrierefreies Bauen, universelles Design |
| FR | conception pour tous, conception universelle |
| IT | design per tutti, progettazione universale |
| PT | design inclusivo, desenho universal |
| NL | Inclusief ontwerp, integrale toegankelijkheid, universeel ontwerp |
| SV | tillgänglighet, universell utformning |
| NO | tilgjengelighet, universell utforming |
| DA | tilgængeligt byggeri, tilgængelighed, universelt design |
| FI | Design for All, esteettömyys, esteetön suunnittelu |
| JA | バリアフリーデザイン, ユニバーサルデザイン |
| ZH | 无障碍设计, 通用设计 |
| KO | 보편적 설계, 유니버설 디자인 |

### TERM-030 · dementia-friendly design

Built environment design supporting cognitive impairment

**English group:** `cognitive accessibility` *(broader)*, `dementia-inclusive design`, `memory-friendly environment`

| Lang | Equivalents |
|---|---|
| DE | demenzfreundliche Gestaltung, demenzgerechtes Bauen |
| FR | environnement Alzheimer, conception adaptée à la démence |
| ES | diseño amigable con la demencia |
| IT | progettazione dementia-friendly |
| PT | design amigável para demência |
| NL | dementievriendelijk ontwerp |
| SV | demensvänlig design |
| NO | demensvennlig design |
| DA | demensvenlige omgivelser, demensvenligt byggeri, demensvenligt design |
| FI | dementiaystävällinen suunnittelu, muistiystävällinen ympäristö, muistisairauksiin sopiva suunnittelu |
| JA | 認知症にやさしいデザイン, 認知症対応設計 |
| ZH | 失智友善设计, 认知症友好设计 |
| KO | 치매 안심 환경, 치매 친화 설계 |

### TERM-059 · visitability

Minimum dwelling accessibility permitting a disabled visitor to enter and use a ground-floor WC

> **Scope:** A threshold standard, not full accessibility; distinct from TERM-068 (accessible housing).

**English group:** `accessible housing minimum`, `basic access`, `inclusive home standard`, `lifetime homes`, `visitable dwelling`

| Lang | Equivalents |
|---|---|
| DE | besuchbare Wohnung, Besuchbarkeit |
| FR | logement visitable, visitabilité |
| ES | vivienda visitable, visitabilidad |
| IT | alloggio visitabile, visitabilità |
| PT | habitação visitável, visitabilidade |
| NL | bezoekbare woning, bezoekbaarheid |
| SV | besökbar bostad, besökbarhet |
| NO | besøkbar bolig, besøkbarhet |
| DA | besøgbar bolig, besøgbarhed |
| FI | vierailtava asunto, vierailtavuus |
| JA | ビジタビリティ, 訪問可能性 |
| ZH | 可造访住宅, 可造访性 |
| KO | 방문 가능 주택, 방문가능성 |

**Linked items:** E-06, E-08, G-04

### TERM-060 · post-occupancy evaluation

Structured evaluation of a building in use against intended performance and occupant experience

> **Scope:** Primary route by which lived-experience (Co-1) evidence re-enters the specification.

**English group:** `occupant survey` *(narrower)*, `POE`, `building performance evaluation`, `building-in-use assessment`, `in-use evaluation`

| Lang | Equivalents |
|---|---|
| DE | Gebäudenachuntersuchung, Nutzungsnachbewertung |
| FR | évaluation en usage, évaluation post-occupation |
| ES | evaluación post-ocupación, evaluación posocupacional |
| IT | valutazione post-occupativa |
| PT | avaliação pós-ocupação |
| NL | post-occupancy evaluatie, gebruiksevaluatie |
| SV | brukarutvärdering, utvärdering efter inflyttning |
| NO | brukerevaluering, evaluering etter innflytting |
| DA | brugerevaluering, evaluering efter ibrugtagning |
| FI | käyttäjäarviointi, käytönaikainen arviointi |
| JA | 建物使用後評価 |
| ZH | 使用后评估 |
| KO | 사용 후 평가 |

### TERM-062 · body dimensions (anthropometrics)

Measured human body and reach dimensions used to derive spatial and reach provisions

> **Scope:** Population-mode inputs. Per doctrine, population data informs but does not bound the individual.

**English group:** `LPA` *(domain)*, `TALL` *(domain)*, `functional anthropometrics` *(narrower)*, `percentile dimensions` *(narrower)*, `reach envelope` *(narrower)*, `static anthropometry` *(narrower)*, `anthropometrics`, `anthropometry`, `body size`

| Lang | Equivalents |
|---|---|
| DE | Anthropometrie, Körpermaße |
| FR | anthropométrie, dimensions corporelles |
| ES | antropometría, dimensiones corporales |
| IT | antropometria, dimensioni corporee |
| PT | antropometria, dimensões corporais |
| NL | antropometrie, lichaamsmaten |
| SV | antropometri, kroppsmått |
| NO | antropometri, kroppsmål |
| DA | antropometri, kropsmål |
| FI | antropometria, kehon mitat |
| JA | 人体計測, 人体寸法 |
| ZH | 人体测量学, 人体尺寸 |
| KO | 인체 측정학, 인체 치수 |

**Linked items:** E-12, G-05, G-06, H-01

### TERM-071 · Design for Adaptable Readiness (DAR)

Designing so later accessibility adaptation is achievable without structural rework

> **Scope:** Mandatory at all three Design Modes per governance/conceptual-model.md.

**English group:** `adaptability`, `adaptable design`, `design for change`, `flexible design`, `future-proofing`, `provision for future adaptation`

| Lang | Equivalents |
|---|---|
| DE | anpassbare Gestaltung, Anpassungsfähigkeit |
| FR | adaptabilité, conception adaptable |
| ES | adaptabilidad, diseño adaptable |
| IT | adattabilità, progettazione adattabile |
| PT | adaptabilidade, projeto adaptável |
| NL | aanpasbaarheid, aanpasbaar ontwerp |
| SV | anpassningsbarhet, anpassningsbar utformning |
| NO | tilpasningsdyktighet, tilpasningsdyktig utforming |
| DA | tilpasningsevne, tilpasningsdygtigt design |
| FI | muunneltavuus, muunneltava suunnittelu |
| JA | 適応性, 可変性設計 |
| ZH | 适应性, 可适应性设计 |
| KO | 적응성, 가변성 설계 |

### TERM-076 · multilingual evidence convergence

Agreement of findings across literatures in different languages

> **Scope:** Methodology term. Convergence across LANGUAGES is not the same as convergence across CODES.

**English group:** `convergence across nations`, `language coverage`, `multi-language evidence`, `multilingual search`, `non-English literature`

| Lang | Equivalents |
|---|---|
| DE | mehrsprachige Evidenzkonvergenz |
| FR | convergence des données probantes multilingues |
| ES | convergencia de evidencia multilingüe |
| JA | 多言語エビデンスの収束 |
| ZH | 多语种证据收敛 |
| KO | 다국어 근거 수렴 |

### TERM-077 · cross-population design conflict

Situation where a provision benefiting one population creates a barrier for another

> **Scope:** Conflicts are recorded and adjudicated, never silently averaged away.

**English group:** `trade-off` *(broader)*, `conflict resolution` *(narrower)*, `access conflict`, `competing access needs`, `conflicting requirements`, `design tension`, `incompatible provision`

| Lang | Equivalents |
|---|---|
| DE | Zielkonflikt zwischen Bedarfsgruppen |
| FR | conflit de conception entre populations |
| ES | conflicto de diseño entre poblaciones |
| JA | 集団間の設計上の対立 |
| ZH | 跨人群设计冲突 |
| KO | 집단 간 설계 충돌 |

### TERM-078 · case study

Documented account of a specific built project or setting used as evidence or illustration

> **Scope:** Evidence tier depends on method, not on the case-study label alone.

**English group:** `demonstration project` *(narrower)*, `built example`, `case example`, `exemplar`, `precedent`, `worked example`

| Lang | Equivalents |
|---|---|
| DE | Praxisbeispiel, Fallstudie |
| FR | exemple, étude de cas |
| ES | caso práctico, estudio de caso |
| IT | studio di caso |
| PT | estudo de caso |
| NL | praktijkvoorbeeld, casestudie |
| SV | exempel, fallstudie |
| NO | eksempel, casestudie |
| DA | eksempel, casestudie |
| FI | esimerkkikohde, tapaustutkimus |
| JA | ケーススタディ, 事例研究 |
| ZH | 案例研究 |
| KO | 사례 연구 |

### TERM-081 · occupational therapy (OT)

Profession assessing person-occupation-environment fit and prescribing environmental adaptation

> **Scope:** Co-2 evidence stratum: OT professional-body CPGs are co-primary with T2 (governance/tier-system.md). Also the Person-mode co-design route.

**English group:** `clinical practice guideline` *(broader)*, `CPG` *(domain)*, `Co-2` *(domain)*, `OT` *(domain)*, `ADL assessment` *(narrower)*, `functional assessment` *(narrower)*, `home assessment` *(narrower)*, `occupational therapist`, `occupational therapy`

| Lang | Equivalents |
|---|---|
| DE | Ergotherapeut, Ergotherapie |
| FR | ergothérapeute, ergothérapie |
| ES | terapeuta ocupacional, terapia ocupacional |
| IT | terapia occupazionale |
| PT | terapia ocupacional |
| NL | ergotherapeut, ergotherapie |
| SV | arbetsterapeut, arbetsterapi |
| NO | ergoterapeut, ergoterapi |
| DA | ergoterapeut, ergoterapi |
| FI | toimintaterapeutti, toimintaterapia |
| JA | 作業療法士, 作業療法 |
| ZH | 职业治疗, 作业治疗 |
| KO | 작업치료사, 작업치료 |

**Linked items:** G-05, H-01, I-02

### TERM-082 · biophilic design

Design incorporating nature, natural materials, daylight and views to support wellbeing

> **Scope:** Claims here are frequently T3/grey — check tier before treating as evidence-based.

**English group:** `daylight access` *(narrower)*, `greenery` *(narrower)*, `planting` *(narrower)*, `views of nature` *(narrower)*, `natural elements`, `nature-based design`, `restorative environment`

| Lang | Equivalents |
|---|---|
| DE | Naturbezug, biophiles Design |
| FR | biophilie, conception biophilique |
| ES | biofilia, diseño biofílico |
| IT | progettazione biofilica |
| PT | design biofílico |
| NL | biofiel ontwerp |
| SV | biofil design |
| NO | biofil design |
| DA | biofilt design |
| FI | biofiilinen suunnittelu |
| JA | バイオフィリックデザイン |
| ZH | 亲生物设计 |
| KO | 바이오필릭 디자인 |

**Linked items:** B-09, D-11

### TERM-083 · trauma-informed design

Design reducing risk of re-traumatisation through control, sightlines, refuge and predictability

> **Scope:** Overlaps the arousal-safety axis (TERM-032) and retreat provision (TERM-074).

**English group:** `defensible space` *(narrower)*, `re-traumatisation` *(narrower)*, `sanctuary model` *(narrower)*, `perceived safety`, `psychological safety`, `trauma-informed care`

| Lang | Equivalents |
|---|---|
| DE | traumainformierte Gestaltung, traumasensibles Design |
| FR | conception tenant compte du traumatisme |
| ES | diseño informado por el trauma |
| IT | progettazione attenta al trauma |
| PT | design informado pelo trauma |
| NL | trauma-sensitief ontwerp |
| SV | traumamedveten utformning |
| NO | traumebevisst utforming |
| DA | traumebevidst design |
| FI | traumatietoinen suunnittelu |
| JA | トラウマインフォームドデザイン |
| ZH | 创伤知情设计 |
| KO | 트라우마 인지 디자인 |

**Linked items:** D-05, D-07, G-01

### TERM-087 · temporal accessibility and pacing

Time as an access dimension: dwell time, queueing, rest intervals and self-paced progression

> **Scope:** Named in item E-03. A route meeting every dimensional rule can still be inaccessible if it cannot be traversed at the user's own pace.

**English group:** `journey time` *(narrower)*, `queueing` *(narrower)*, `waiting time` *(narrower)*, `dwell time`, `pacing`, `self-paced`, `time pressure`, `timed access`

| Lang | Equivalents |
|---|---|
| DE | Verweildauer, Zeitdruck, zeitliche Barrierefreiheit |
| FR | rythme, temps d'attente, accessibilité temporelle |
| ES | ritmo, tiempo de espera, accesibilidad temporal |
| IT | ritmo, accessibilità temporale |
| PT | ritmo, acessibilidade temporal |
| NL | tempo, wachttijd, temporele toegankelijkheid |
| SV | tempo, väntetid, tidsmässig tillgänglighet |
| NO | tempo, ventetid, tidsmessig tilgjengelighet |
| DA | tempo, ventetid, tidsmæssig tilgængelighed |
| FI | odotusaika, tahti, ajallinen saavutettavuus |
| JA | ペース配分, 時間的アクセシビリティ |
| ZH | 节奏, 时间可达性 |
| KO | 속도 조절, 시간적 접근성 |

**Linked items:** E-03, E-10, H-03

## Population

### TERM-016 · wheelchair user

Person using manual or powered wheelchair for mobility

**English group:** `wheelchair-bound` *(deprecated)*, `chair user`

| Lang | Equivalents |
|---|---|
| DE | Rollstuhlnutzer, Rollstuhlfahrer |
| FR | personne en fauteuil roulant, utilisateur de fauteuil roulant |
| ES | persona en silla de ruedas, usuario de silla de ruedas |
| IT | persona in carrozzina, utilizzatore di sedia a rotelle |
| PT | usuário de cadeira de rodas, cadeirante |
| NL | rolstoelgebruiker |
| SV | rullstolsburna, rullstolsanvändare |
| NO | rullestolbruker |
| DA | kørestolsanvender, kørestolsbruger |
| FI | pyörätuolilla liikkuva, pyörätuolin käyttäjä |
| JA | 車椅子利用者, 車いす使用者 |
| ZH | 乘轮椅者, 坐轮椅者, 轮椅使用者 |
| KO | 지체장애인, 휠체어 사용자 |

**Linked items:** E-01, E-03, E-04, E-08, G-01, G-03, G-04

## Sensory

### TERM-012 · sensory room

Controlled-environment room for sensory regulation/recovery

**English group:** `multi-sensory environment` *(broader)*, `Snoezelen room` *(domain)*, `calm room`, `de-escalation space`, `quiet room`

| Lang | Equivalents |
|---|---|
| DE | Snoezelenraum, Reizarmer Raum, Ruheraum |
| FR | espace calme, salle sensorielle |
| ES | sala Snoezelen, espacio de calma, sala multisensorial, sala sensorial |
| IT | stanza Snoezelen, Spazio Calmo, stanza sensoriale |
| PT | sala Snoezelen, espaço de calma, sala multissensorial, sala sensorial |
| NL | prikkelarme ruimte, zintuiglijke ruimte, snoezelruimte |
| SV | Snoezelen-rum, vilorum, sinnesrum |
| NO | Snoezelen-rom, stillerom, sanserom |
| DA | Snoezelen-rum, hvilerum, roligt rum, sanserum |
| FI | Snoezelen-tila, aistisäätelytila, rauhoittumistila, aistihuone |
| JA | カームダウンスペース, 感覚室 |
| ZH | 安静室, 感官室 |
| KO | 감각통합실, 진정 공간, 감각실 |

**Linked items:** A-16, F-03

### TERM-073 · neurodivergent sensory environment

Environmental sensory conditions considered from neurodivergent access requirements

> **Scope:** References the existing NDV population codes; do NOT treat as a new population umbrella.

**English group:** `AUT` *(domain)*, `NDV` *(domain)*, `autism` *(domain)*, `autistic` *(domain)*, `quiet space` *(narrower)*, `autistic-friendly design`, `low-arousal environment`, `neuroinclusive design`, `sensory regulation`, `sensory sensitivity`, `sensory-friendly`, `stimulation density`, `stimulus level`

| Lang | Equivalents |
|---|---|
| DE | sensorisch angepasste Umgebung, reizarme Umgebung |
| FR | environnement sensoriellement adapté, environnement à faible stimulation |
| ES | entorno sensorialmente adaptado, entorno de baja estimulación |
| IT | ambiente a bassa stimolazione |
| PT | ambiente de baixa estimulação |
| NL | sensorisch vriendelijke omgeving, prikkelarme omgeving |
| SV | sinnesanpassad miljö, lågstimulimiljö |
| NO | sansetilpasset miljø, lavstimulimiljø |
| DA | sansetilpasset miljø, lavstimulusmiljø |
| FI | aistiystävällinen ympäristö, vähävirikkeinen ympäristö |
| JA | 低刺激環境, 感覚に配慮した環境 |
| ZH | 感官友好环境, 低刺激感官环境 |
| KO | 감각 친화 환경, 저자극 감각 환경 |

**Linked items:** A-16, D-05, F-01, F-03

### TERM-074 · retreat space and exit legibility

Provision of withdrawal space plus a legible, visible route out of it

> **Scope:** Links items A-16, D-05. Retreat without a legible exit fails the arousal-safety axis (TERM-032).

**English group:** `escape route legibility` *(narrower)*, `exit visibility` *(narrower)*, `calm space`, `quiet room`, `refuge`, `safe space`, `sensory retreat`, `withdrawal space`

| Lang | Equivalents |
|---|---|
| DE | Ruheraum, Rückzugsraum |
| FR | salle de repos, espace de retrait |
| ES | sala de calma, espacio de retiro |
| IT | stanza tranquilla, spazio di ritiro |
| PT | sala tranquila, espaço de recolhimento |
| NL | stilteruimte, terugtrekruimte |
| SV | tyst rum, reträttrum |
| NO | stillerom, tilbaketrekningsrom |
| DA | stillerum, tilbagetrækningsrum |
| FI | rauhoittumistila, vetäytymistila |
| JA | 静養室, 退避スペース |
| ZH | 静音室, 撤离空间 |
| KO | 정온실, 대피 공간 |

**Linked items:** A-16, D-05, E-13, F-03

### TERM-085 · fragrance-free policy

Operational and specification control of airborne fragrance and VOC exposure

> **Scope:** Links items F-02, F-06. Operational policy and material specification act together; specification alone does not deliver a fragrance-free environment.

**English group:** `chemical exposure` *(broader)*, `MCS` *(domain)*, `VOC` *(narrower)*, `low-VOC materials` *(narrower)*, `material disclosure` *(narrower)*, `off-gassing` *(narrower)*, `fragrance`, `fragrance-free`, `scent-free`

| Lang | Equivalents |
|---|---|
| DE | Duftstoffverzicht, duftfrei, duftstofffreie Richtlinie |
| FR | sans parfum, politique sans parfum |
| ES | sin fragancia, política libre de fragancias |
| IT | politica senza profumi |
| PT | política sem fragrâncias |
| NL | geurvrij, parfumvrij beleid |
| SV | doftfri, doftfri policy |
| NO | parfymefri, duftfri policy |
| DA | parfumefri, duftfri politik |
| FI | hajusteeton, hajusteeton käytäntö |
| JA | 無香料, 無香料方針 |
| ZH | 无香, 无香料政策 |
| KO | 무향료, 무향 정책 |

**Linked items:** F-02, F-04, F-06

## Thermal

### TERM-063 · thermal comfort

Occupant satisfaction with the thermal environment, as distinct from measured air temperature

> **Scope:** Links items F-07, F-08, K-05. Impairment side is TERM-015; demand axis is TERM-044.

**English group:** `thermal environment` *(broader)*, `PMV` *(narrower)*, `adaptive comfort` *(narrower)*, `operative temperature` *(narrower)*, `overheating` *(narrower)*, `predicted mean vote` *(narrower)*, `indoor temperature`, `thermal satisfaction`

| Lang | Equivalents |
|---|---|
| DE | Raumtemperatur, Überhitzung, thermische Behaglichkeit |
| FR | surchauffe, température opérative, confort thermique |
| ES | sobrecalentamiento, temperatura operativa, confort térmico |
| IT | temperatura operativa, comfort termico |
| PT | temperatura operativa, conforto térmico |
| NL | operatieve temperatuur, oververhitting, thermisch comfort |
| SV | operativ temperatur, termisk komfort |
| NO | operativ temperatur, termisk komfort |
| DA | operativ temperatur, termisk komfort |
| FI | operatiivinen lämpötila, ylilämpeneminen, lämpöviihtyvyys |
| JA | 作用温度, 温熱快適性 |
| ZH | 操作温度, 过热, 热舒适 |
| KO | 작용온도, 열쾌적성 |

**Linked items:** F-04, F-07, F-08, K-05

## Wayfinding

### TERM-010 · tactile walking surface indicator

Ground surface detectable by foot or cane for guidance/warning

**English group:** `truncated dome` *(narrower)*, `TWSI`, `detectable warning surface`, `tactile ground surface indicator`, `tactile paving`

| Lang | Equivalents |
|---|---|
| DE | Blindenleitsystem, taktile Bodenleitsysteme, Bodenindikatoren |
| FR | bande d'éveil de vigilance, bande podotactile |
| ES | baldosa podotáctil, franja señalizadora, pavimento podotáctil |
| IT | LOGES, guida a terra tattile, percorso podotattile |
| PT | piso podotátil, piso tátil |
| NL | noppen- en ribbeltegels, tactiele geleiding, geleidestrook |
| SV | ledstråk, varningsplattor, taktila ledstråk |
| NO | oppmerksomhetsfelt, taktile ledelinjer |
| DA | ledelinjer, følbare indikatorer, taktile ledelinjer |
| FI | kohokuvioidut laatat, tuntopinta, opaslaatta |
| JA | 点字ブロック, 視覚障害者誘導用ブロック |
| ZH | 触觉地面指示器, 盲道 |
| KO | 시각장애인유도블록, 점자블록 |

**Linked items:** E-09

### TERM-011 · LRV contrast

Light Reflectance Value difference between adjacent surfaces

**English group:** `colour contrast` *(broader)*, `visual contrast` *(broader)*, `luminance contrast`

| Lang | Equivalents |
|---|---|
| DE | visueller Kontrast, Helligkeitskontrast, Leuchtdichtekontrast |
| FR | contraste de luminance |
| ES | contraste visual, contraste de luminancia |
| IT | contrasto visivo, contrasto di luminanza |
| PT | contraste visual, contraste de luminância |
| NL | kleurcontrast, luminantiecontrast |
| SV | ljushetskontrast, luminanskontrast |
| NO | synlig kontrast, luminanskontrast |
| DA | farvekontrast, lyshedskontrast, luminanskontrast |
| FI | värikontrasti, luminanssikontrasti, tummuuskontrasti |
| JA | 明度差, 輝度コントラスト |
| ZH | 明暗对比, 亮度对比 |
| KO | 시각적 대비, 명도 대비, 휘도 대비 |

**Linked items:** C-04, C-05, D-03, D-06

### TERM-019 · pictogram signage

Simplified graphic symbols for wayfinding

**English group:** `icon-based signage`, `pictographic signage`, `symbol signage`

| Lang | Equivalents |
|---|---|
| DE | Bildzeichen, Piktogramm-Beschilderung |
| FR | pictogramme, signalétique pictographique |
| ES | pictograma, señalización con pictogramas |
| IT | pittogramma, segnaletica pittografica |
| PT | pictograma, sinalização pictográfica |
| NL | beeldtaal, pictogramborden |
| SV | symbolskyltning, piktogramskyltning |
| NO | symbolmerking, piktogramskilt |
| DA | symbolskiltning, piktogramskiltning |
| FI | kuvasymboli, symboliopaste, opastekuvake |
| JA | 絵文字サイン, ピクトグラム |
| ZH | 图标标识, 象形标识 |
| KO | 그림문자, 픽토그램 |

**Linked items:** D-08

### TERM-028 · wayfinding

System enabling navigation through built environment

> **Scope:** Content term: wayfinding as a design system. The demand axis is TERM-038 (Orientation demand); ko alias '길찾기' is shared between them.

**English group:** `navigation` *(broader)*, `orientation` *(broader)*, `spatial orientation`

| Lang | Equivalents |
|---|---|
| DE | Leitsystem, Orientierungssystem, Wegeleitsystem |
| FR | signalétique directionnelle, orientation spatiale |
| ES | señalización direccional |
| IT | segnaletica direzionale |
| NL | bewegwijzering |
| SV | vägvisning |
| NO | veivisning |
| DA | skiltning, orientering, vejvisning |
| FI | opastusjärjestelmä, suunnistautuminen, opastus |
| JA | サイン計画, 案内誘導 |
| ZH | 导向系统, 寻路系统 |
| KO | 안내 시스템, 길찾기 |

### TERM-069 · haptic affordance

Environmental feature conveying information or action possibility through touch

> **Scope:** Broader than TERM-010 (TWSI), which is one standardised instance of a haptic affordance.

**English group:** `affordance` *(broader)*, `handrail feedback` *(narrower)*, `kinaesthetic cue`, `tactile cue`, `tactile guidance`, `tactile landmark`, `texture cue`, `touch cue`

| Lang | Equivalents |
|---|---|
| DE | taktiler Hinweis, haptische Angebotsqualität |
| FR | repère tactile, affordance haptique |
| ES | señal táctil, affordance háptica |
| IT | riferimento tattile, affordance aptica |
| PT | pista tátil, affordance háptica |
| NL | tactiele aanwijzing, haptische affordantie |
| SV | taktil ledtråd, haptisk affordans |
| NO | taktilt holdepunkt, haptisk affordans |
| DA | taktilt spor, haptisk affordans |
| FI | tuntoon perustuva vihje, haptinen tarjouma |
| JA | 触知手がかり, 触覚的アフォーダンス |
| ZH | 触觉线索, 触觉可供性 |
| KO | 촉각 단서, 촉각 어포던스 |

**Linked items:** E-09, K-02, K-03

