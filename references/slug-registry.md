# Slug Registry
**Managed by:** research-log-manager  
**GitHub path:** `references/slug-registry.md`  
**Last updated:** 2026-03-18  
**Coverage:** All canonical population codes (main taxonomy + supplementary volume). Each slug represents the broadest usefully bounded evidence domain. Sub-findings are surfaced within the run.

---

## Design Convention

**Format:** `{domain-descriptor}|{POPULATION-CODE}` — infrastructure key, not a conceptual claim.  
**Map quality:** `CLEAN` = close conceptual match. `PARTIAL` = meaningful mismatch; see `concept_boundary_warnings`.  
**Priority:** P1 = before next research phase. P2 = next phase. P3 = horizon.

---

## Population Code Index

| Code | Slug(s) | Priority |
|---|---|---|
| MOB | `mobility-built-environment\` | P1 |
| VIS | `visual-impairment-built-environment\` | P1 |
| DEAF | `deaf-spatial-design\` · `deaf-acoustic-built-environment\` | P1 |
| NEU | `neurological-built-environment\` | P1 |
| DEM | `dementia-built-environment\` | P1 |
| NDV | `neurodivergence-built-environment\` | P1 |
| NDV/MH | `mental-health-built-environment\` | P2 |
| PAIN | `chronic-pain-built-environment\` | P2 |
| DBL | `deafblind-built-environment\` | P1 |
| OFS | `OFS-built-environment\` | P1 |
| IntD | `intellectual-disability-built-environment\` | P2 |
| ALL | `critical-disability-studies-architecture\` · `OT-built-environment-interface\` · `intersectionality-disability-design\` · `assistive-technology-built-environment\` · `post-occupancy-evaluation-disability\` | P1/P2 |
| CHD (Supp.) | `children-disability-built-environment\` | P2 |
| LPA (Supp.) | `little-people-built-environment\` | P2 |
| EXH (Supp.) | `exceptional-height-built-environment\` | P3 |
| BAR (Supp.) | `large-body-size-built-environment\` | P2 |

---

## Full Slug Entries

---

### `mobility-built-environment`
**Domain:** Wheelchair circulation; ambulant accessibility; reach ranges; ramp and step design; door hardware; transfer space; grab bar provision; floor surfaces; vertical circulation; powered mobility; upper limb impairment provisions

| Language | Native term | Map |
|---|---|---|
| SV | *rörelsehinder / tillgänglighet för rörelsehindrade / hjälpmedelsanpassning* | CLEAN |
| NO | *bevegelseshemming / universell utforming for bevegelseshemmede / rullestoltilgjengelighet* | CLEAN |
| DA | *bevægelseshandicap / tilgængelighed for bevægelseshæmmede / kørestolstilgængelighed* | CLEAN |
| FI | *liikuntavamma / esteettömyys liikuntavammaisille / pyörätuolitilat* | CLEAN |
| FR | *handicap moteur / accessibilité pour personnes à mobilité réduite (PMR) / fauteuil roulant* | PARTIAL |
| DE | *Mobilitätseinschränkung / Barrierefreiheit für Rollstuhlnutzer / Bewegungsbehinderung* | CLEAN |
| ZH | *肢体残疾 (zhītǐ cánjí) / 无障碍设施 / 轮椅使用者* | CLEAN |
| JA | *肢体不自由 (shitai fujiyū) / 車いす使用者 / バリアフリー移動* | PARTIAL |
| NL | *motorische beperking / rolstoeltoegankelijkheid / lichamelijke beperking* | CLEAN |
| ES | *discapacidad motora / accesibilidad para usuarios de silla de ruedas / movilidad reducida* | CLEAN |
| PT | *deficiência motora / acessibilidade para cadeirantes / mobilidade reduzida* | CLEAN |
| KO | *지체장애 (jiché jangae) / 휠체어 접근성 / 이동 편의시설* | CLEAN |
| IT | *disabilità motoria / accessibilità per utenti di sedia a rotelle / mobilità ridotta* | CLEAN |

**Concept boundary warnings:**
- FR: *PMR* (personne à mobilité réduite) is the statutory term but broader than MOB — includes pregnancy, temporary injury. Filter to disability-specific provisions.
- JA: *肢体不自由* includes upper limb impairment separately from lower limb/mobility — distinguish MOB/AMB from MOB/UPL in findings.

---

### `visual-impairment-built-environment`
**Domain:** Wayfinding for blind and low vision users; tactile walking surface indicators; colour and luminance contrast; lighting levels; tactile signage; Braille; audio description; guide dog access; low vision interior design

| Language | Native term | Map |
|---|---|---|
| SV | *synnedsättning / synskada / tillgänglighet för synskadade / ledstråk* | CLEAN |
| NO | *synshemming / blindhet / tilgjengelighet for synshemmede / taktile ledelinjer* | CLEAN |
| DA | *synsnedsættelse / blindhed / tilgængelighed for synshandicappede / taktile ledelinjer* | CLEAN |
| FI | *näkövamma / sokeus / esteettömyys näkövammaisille / ohjaavat pintarakenteet* | CLEAN |
| FR | *déficience visuelle / cécité / malvoyance / accessibilité pour déficients visuels* | CLEAN |
| DE | *Sehbehinderung / Blindheit / Barrierefreiheit für Sehbehinderte / taktile Bodenleitsysteme* | CLEAN |
| ZH | *视觉障碍 (shìjué zhàng'ài) / 盲 (máng) / 低视力 / 盲道 (mángdào)* | PARTIAL |
| JA | *視覚障害 (shikaku shōgai) / 全盲 / 弱視 / 点字ブロック (tenji burokku)* | CLEAN |
| NL | *visuele beperking / blindheid / slechtziendheid / geleidetegels* | CLEAN |
| ES | *discapacidad visual / ceguera / baja visión / pavimento táctil* | CLEAN |
| PT | *deficiência visual / cegueira / baixa visão / piso tátil* | CLEAN |
| KO | *시각장애 (sigak jangae) / 전맹 / 저시력 / 점자블록* | CLEAN |
| IT | *disabilità visiva / cecità / ipovisione / percorso tattile* | CLEAN |

**Concept boundary warnings:**
- ZH: *盲道* is often used generically for all VIS accessibility provisions — search by specific provision type (contrast, lighting, tactile) as well.

---

### `deaf-spatial-design`
**Domain:** Signing space; corridor width; sightlines; visual access; wayfinding; lip-reading lighting; visual fire alerting; visual communication zones; spatial grammar of signed languages

| Language | Native term | Map |
|---|---|---|
| SV | *teckenutrymme / visuellt kommunikationsutrymme* | CLEAN |
| NO | *tegnrom / kommunikasjonsavstand* | PARTIAL |
| DA | *tegnsprogrum / kommunikationsafstand* | CLEAN |
| FI | *viittomistila / visuaalinen kommunikointitila* | CLEAN |
| FR | *espace de signe / espace proxémique pour la LSF* | CLEAN |
| DE | *Gebärdenraum / Kommunikationszone* | CLEAN |
| ZH | *手语交流空间 (shǒuyǔ jiāoliú kōngjiān)* | PARTIAL |
| JA | *手話空間 (shuwa kūkan)* | PARTIAL |
| NL | *gebarenruimte* | PARTIAL |
| ES | *espacio signante* | CLEAN |
| PT | *espaço signante* | CLEAN |
| KO | *수어 공간 (sueo gonggan)* | PARTIAL |
| IT | *spazio segnante* | CLEAN |

**Concept boundary warnings:**
- NO: TEK17 bundles spatial+acoustic — search together; log under both `deaf-spatial-design` and `deaf-acoustic-built-environment`.
- ZH: GB 50763 organises by 无障碍 category, not Deaf-specific spatial concept — search by standard section; map post-retrieval.
- JA: MLIT Barrier-Free Law bundles spatial+acoustic+signage by building type — search by law section; log under both slugs.
- NL: NGT proxemics undefined in NL standards — expect grey literature (Dovenschap) or NO-DATA.
- KO: 한국수어 signing-space evidence likely absent — search broader 청각장애인 spatial provisions; flag THIN.

---

### `deaf-acoustic-built-environment`
**Domain:** Reverberation time; background noise; speech intelligibility; hearing loop placement; room geometry; acoustic zoning; cochlear implant acoustic environment; Auracast/Bluetooth LE Audio

| Language | Native term | Map |
|---|---|---|
| SV | *hörslinga / akustisk tillgänglighet / teleslinga / rumsakustik för hörselskadade* | CLEAN |
| NO | *teleslynge / hørselstilgjengelighet / romakustikk for hørselshemmede* | PARTIAL |
| DA | *teleslynge / høretilgængelighed / rumakustik for hørehæmmede* | CLEAN |
| FI | *induktiosilmukka / akustinen esteettömyys / kuuntelijasilmukka* | CLEAN |
| FR | *BIM (boucle à induction magnétique) / accessibilité acoustique* | CLEAN |
| DE | *Induktionsschleife / Höranlage / akustische Barrierefreiheit* | CLEAN |
| ZH | *感应线圈 (gǎnyìng xiànquān) / 声学无障碍 / 助听环境* | CLEAN |
| JA | *磁気誘導ループ (jiki yūdō rūpu) / 音響バリアフリー* | PARTIAL |
| NL | *ringleiding / akoestische toegankelijkheid / hoorlus* | CLEAN |
| ES | *bucle magnético / accesibilidad acústica* | CLEAN |
| PT | *loop de indução / acessibilidade acústica* | CLEAN |
| KO | *자기유도루프 / 음향 접근성* | CLEAN |
| IT | *anello ad induzione / accessibilità acustica* | CLEAN |

**Concept boundary warnings:**
- NO: TEK17 bundles spatial+acoustic — as per `deaf-spatial-design`.
- JA: MLIT bundles acoustic with spatial and signage — search by law section.

---

### `neurological-built-environment`
**Domain:** ABI/TBI design; post-concussion syndrome environment; cognitive fatigue in spatial navigation; lighting and noise sensitivity; orientation and wayfinding; predictable low-stimulus environments; NEU/PCS provisions

| Language | Native term | Map |
|---|---|---|
| SV | *förvärvad hjärnskada / neurologisk funktionsnedsättning / kognitiv tillgänglighet* | CLEAN |
| NO | *ervervet hjerneskade / nevrologisk funksjonsnedsettelse / kognitiv tilgjengelighet* | CLEAN |
| DA | *erhvervet hjerneskade / neurologisk funktionsnedsættelse / kognitiv tilgængelighed* | CLEAN |
| FI | *hankittu aivovaurio / neurologinen toimintarajoite / kognitiivinen esteettömyys* | CLEAN |
| FR | *lésion cérébrale acquise / handicap neurologique / accessibilité cognitive* | CLEAN |
| DE | *erworbene Hirnschädigung / neurologische Behinderung / kognitive Barrierefreiheit* | CLEAN |
| ZH | *获得性脑损伤 (huòdé xìng nǎo sǔnshāng) / 神经系统障碍 / 认知无障碍* | PARTIAL |
| JA | *後天性脳損傷 (kōtennsei nōsonshou) / 神経障害 / 認知的バリアフリー* | PARTIAL |
| NL | *verworven hersenletsel / neurologische beperking / cognitieve toegankelijkheid* | CLEAN |
| ES | *lesión cerebral adquirida / discapacidad neurológica / accesibilidad cognitiva* | CLEAN |
| PT | *lesão cerebral adquirida / deficiência neurológica / acessibilidade cognitiva* | CLEAN |
| KO | *후천성 뇌손상 / 신경장애 / 인지적 접근성* | CLEAN |
| IT | *lesione cerebrale acquisita / disabilità neurologica / accessibilità cognitiva* | CLEAN |

**Concept boundary warnings:**
- ZH/JA/KO: *cognitive accessibility* (认知无障碍 / 認知的バリアフリー / 인지적 접근성) often refers to intellectual disability in East Asian regulatory contexts — distinguish NEU from IntD in findings.

---

### `dementia-built-environment`
**Domain:** Dementia-specific design; orientation and wayfinding; landmark-based navigation; circadian lighting; colour contrast for dementia; safe wandering routes; care home and domestic design; Dementia Design Audit Tool

| Language | Native term | Map |
|---|---|---|
| SV | *demensanpassad miljö / demensdesign / kognitiv tillgänglighet för demenssjuka* | CLEAN |
| NO | *demenstilpasset miljø / demensdesign* | CLEAN |
| DA | *demensvenlighed / demensdesign / kognitiv tilgængelighed for demente* | CLEAN |
| FI | *muistisairausystävällinen ympäristö / dementiapotilaan ympäristö* | CLEAN |
| FR | *environnement adapté aux personnes atteintes de démence / architecture pour Alzheimer* | CLEAN |
| DE | *demenzgerechte Umgebung / Demenzdesign / Wohnraumanpassung bei Demenz* | CLEAN |
| ZH | *痴呆症友好环境 (chīdāizhèng yǒuhǎo huánjìng) / 认知障碍适老化设计* | CLEAN |
| JA | *認知症に配慮した環境 / 認知症対応設計* | CLEAN |
| NL | *dementievriendelijke omgeving / dementiegerichte architectuur* | CLEAN |
| ES | *entorno adaptado para demencia / diseño para personas con Alzheimer* | CLEAN |
| PT | *ambiente amigável para demência / design para pessoas com Alzheimer* | CLEAN |
| KO | *치매 친화적 환경 / 인지장애 대응 설계* | CLEAN |
| IT | *ambiente demenzia-friendly / design per Alzheimer* | CLEAN |

---

### `neurodivergence-built-environment`
**Domain:** AUT sensory design (ASPECTSS, PAS 6463); ADHD spatial design; sensory processing disorder; dyscalculia/dyslexia wayfinding; OCD environmental triggers; Tourette's spatial exposure; sensory zoning; NDV/SENS provisions

| Language | Native term | Map |
|---|---|---|
| SV | *neurodiversitet / autismvänlig miljö / sensorisk tillgänglighet / ADHD-anpassad miljö* | CLEAN |
| NO | *nevrodiversitet / autismevennlig miljø / sensorisk tilgjengelighet* | CLEAN |
| DA | *neurodiversitet / autismevenligt miljø / sensorisk tilgængelighed* | CLEAN |
| FI | *neurodiversiteetti / autismiystävällinen ympäristö / aistillinen esteettömyys* | CLEAN |
| FR | *neurodiversité / environnement adapté à l'autisme / accessibilité sensorielle* | CLEAN |
| DE | *Neurodiversität / autismusgerechte Umgebung / sensorische Barrierefreiheit* | CLEAN |
| ZH | *神经多样性 (shénjīng duōyàng xìng) / 自闭症友好设计 / 感觉统合设计* | PARTIAL |
| JA | *神経多様性 (shinkei tayōsei) / 自閉症スペクトラム対応設計 / 感覚統合環境* | CLEAN |
| NL | *neurodiversiteit / autismevriendelijke omgeving / sensorische toegankelijkheid* | CLEAN |
| ES | *neurodiversidad / entorno amigable para autismo / accesibilidad sensorial* | CLEAN |
| PT | *neurodiversidade / ambiente amigável para autismo / acessibilidade sensorial* | CLEAN |
| KO | *신경다양성 / 자폐 친화적 환경 / 감각 접근성* | CLEAN |
| IT | *neurodiversità / ambiente autism-friendly / accessibilità sensoriale* | CLEAN |

**Concept boundary warnings:**
- ZH: *感觉统合* (sensory integration) is a clinical therapy term — distinguish from sensory design in built environment.
- All languages: ADHD, SPD, OCD, Tourette's severely underexplored vs. AUT in all languages — flag non-AUT NDV evidence as THIN if found.

---

### `mental-health-built-environment`
**Domain:** Trauma-informed design; Sanctuary Model; SAMHSA guidelines; psychiatric unit design; PTSD environmental triggers; safety, control, and choice in shared spaces; de-escalation design; sensory rooms

| Language | Native term | Map |
|---|---|---|
| SV | *traumainformerad design / psykisk hälsa och byggd miljö* | CLEAN |
| NO | *traumeinformert design / psykisk helse og bygd miljø* | CLEAN |
| DA | *traumainformeret design / psykisk sundhed og det byggede miljø* | CLEAN |
| FI | *traumainformoitu suunnittelu / mielenterveys ja rakennettu ympäristö* | CLEAN |
| FR | *conception tenant compte des traumatismes / santé mentale et environnement bâti* | CLEAN |
| DE | *traumasensibles Design / psychische Gesundheit und gebaute Umwelt* | CLEAN |
| ZH | *创伤知情设计 (chuāngshāng zhīqíng shèjì) / 精神健康与建筑环境* | CLEAN |
| JA | *トラウマインフォームドデザイン / 精神保健と建築環境* | CLEAN |
| NL | *traumageïnformeerd ontwerp / geestelijke gezondheid en gebouwde omgeving* | CLEAN |
| ES | *diseño informado por trauma / salud mental y entorno construido* | CLEAN |
| PT | *design informado por trauma / saúde mental e ambiente construído* | CLEAN |
| KO | *트라우마 인폼드 디자인 / 정신건강과 건축 환경* | CLEAN |
| IT | *design trauma-informed / salute mentale e ambiente costruito* | CLEAN |

---

### `chronic-pain-built-environment`
**Domain:** Fibromyalgia and chronic pain design; central sensitisation environmental triggers; rest and activity pacing; thermal comfort for PAIN users; tactile surface sensitivity; fatigue/pain interaction with spatial design

| Language | Native term | Map |
|---|---|---|
| SV | *kronisk smärta / fibromyalgi / smärtsensitiv miljö* | CLEAN |
| NO | *kronisk smerte / fibromyalgi / smertesensitivt miljø* | CLEAN |
| DA | *kronisk smerte / fibromyalgi / smertesensitivt miljø* | CLEAN |
| FI | *krooninen kipu / fibromyalgia / kipuherkälle suunniteltu ympäristö* | CLEAN |
| FR | *douleur chronique / fibromyalgie / environnement adapté à la douleur chronique* | CLEAN |
| DE | *chronischer Schmerz / Fibromyalgie / schmerzarme Umgebungsgestaltung* | CLEAN |
| ZH | *慢性疼痛 (mànxìng téngtòng) / 纤维肌痛 / 疼痛敏感环境设计* | CLEAN |
| JA | *慢性疼痛 (mansei tōtsū) / 線維筋痛症 / 痛み配慮の環境設計* | CLEAN |
| NL | *chronische pijn / fibromyalgie / pijnsensitieve omgeving* | CLEAN |
| ES | *dolor crónico / fibromialgia / diseño para sensibilidad al dolor* | CLEAN |
| PT | *dor crônica / fibromialgia / design para sensibilidade à dor* | CLEAN |
| KO | *만성통증 / 섬유근통 / 통증 민감 환경* | CLEAN |
| IT | *dolore cronico / fibromialgia / ambiente per sensibilità al dolore* | CLEAN |

**Concept boundary warnings:**
- All languages: No built environment design vocabulary exists for PAIN in most languages — strategy is derivation from clinical pain management and OT activity pacing literature. Expect THIN; flag and derive.

---

### `deafblind-built-environment`
**Domain:** Tactile infrastructure; protactile spatial requirements; vibrotactile alerting; intervener service space; haptic landmark design; tactile navigation; tactile mapping; long cane + guide dog co-navigation space

| Language | Native term | Map |
|---|---|---|
| SV | *dövblind / kombinerad syn- och hörselskada / taktil kommunikation / vibrationslarm* | CLEAN |
| NO | *døvblind / kombinert sansetap / taktil kommunikasjon / vibrasjonsvarsel* | CLEAN |
| DA | *døvblind / kombineret høre- og synstab / taktilkommunikation / vibrationssignal* | CLEAN |
| FI | *kuurosokea / kuulonäkövammainen / taktiilikommunikaatio / tärinähälytys* | CLEAN |
| FR | *sourdaveugle / surdicécité / communication tactile / alerte vibrotactile* | CLEAN |
| DE | *taubblind / Hörsehbehinderung / taktile Kommunikation / Vibrationssignalisierung* | CLEAN |
| ZH | *聋盲 (lóngmáng) / 双重感官障碍 / 触觉交流 / 振动报警* | PARTIAL |
| JA | *盲ろう者 (mōrōsha) / 触手話 (shoku-shuwa) / 振動警報* | CLEAN |
| NL | *doofblind / gecombineerde zintuigelijke beperking / tactiele communicatie / trillingsalarm* | CLEAN |
| ES | *sordociego / comunicación táctil / Lorm / alerta vibrotáctil* | CLEAN |
| PT | *surdocego / LIBRAS tátil / alerta vibrotátil* | CLEAN |
| KO | *시청각장애인 / 농맹인 / 촉각 의사소통 / 진동 경보* | CLEAN |
| IT | *sordocieco / comunicazione tattile / Malossi / allarme vibrotattile* | CLEAN |

**Concept boundary warnings:**
- ZH: *聋盲* is rare in Chinese discourse — *双重感官障碍* is more searchable. No GB standard addresses DBL vibrotactile provisions — expect NO-DATA; derive from AT product literature.
- All languages: No jurisdiction has a built environment standard specifically addressing vibrotactile alerting for DBL — flag all as NO-DATA for that provision.

---

### `OFS-built-environment`
**Domain:** Energy conservation; rest seating intervals and route length; thermal environment; surface heights for POTS; air quality and chemical sensitivity for MCAS; exertion economy in spatial planning; activity pacing

| Language | Native term | Map |
|---|---|---|
| SV | *ME/CFS / kroniskt trötthetssyndrom / ortostatisk intolerans / energikonservering* | PARTIAL |
| NO | *ME/CFS / kronisk utmattelsessyndrom / ortostatisk intoleranse / aktivitetspacing* | PARTIAL |
| DA | *ME/CFS / kronisk træthedssyndrom / ortostatisk intolerance / aktivitetspacing* | PARTIAL |
| FI | *ME/CFS / krooninen väsymysoireyhtymä / ortostaattinen intoleranssi* | PARTIAL |
| FR | *ME/SFC / syndrome de fatigue chronique / intolérance orthostatique* | PARTIAL |
| DE | *ME/CFS / Chronisches Erschöpfungssyndrom / orthostatische Intoleranz* | PARTIAL |
| ZH | *慢性疲劳综合征 / 体位性心动过速综合征 (POTS) / 能量保存策略* | PARTIAL |
| JA | *筋痛性脳脊髄炎 / 慢性疲労症候群 / 起立性頻脈症候群 (POTS)* | PARTIAL |
| NL | *ME/CVS / chronisch vermoeidheidssyndroom / orthostatische intolerantie* | PARTIAL |
| ES | *SFC / EM / intolerancia ortostática* | PARTIAL |
| PT | *SFC / EM/SFC / intolerância ortostática* | PARTIAL |
| KO | *만성피로증후군 / 기립성빈맥증후군 (POTS)* | PARTIAL |
| IT | *SFC / EM / intolleranza ortostatica* | PARTIAL |

**Concept boundary warnings:**
- All languages: All aliases are PARTIAL — these are clinical terms, not design terms. No built environment OFS design vocabulary exists in any language. Strategy is derivation from clinical environment-function data. REHADAT (DE) workplace adaptation literature is in scope. Do not search for "OFS built environment design" directly.

---

### `intellectual-disability-built-environment`
**Domain:** Intellectual disability and built environment; cognitive accessibility; Easy Read / FALC signage; predictable spatial layouts; support worker co-navigation space; Makaton-compatible design; sensory environments for IntD

**Note:** All IntD specifications carry `[TIER 4-5; no quantified architectural standard in any jurisdiction; March 2026]`. Expect THIN across all languages.

| Language | Native term | Map |
|---|---|---|
| SV | *intellektuell funktionsnedsättning / kognitiv tillgänglighet / lättläst information* | CLEAN |
| NO | *intellektuell funksjonsnedsettelse / kognitiv tilgjengelighet / lettlest* | CLEAN |
| DA | *intellektuel funktionsnedsættelse / kognitiv tilgængelighed / letlæst* | CLEAN |
| FI | *kehitysvamma / kognitiivinen esteettömyys / selkokieli* | CLEAN |
| FR | *déficience intellectuelle / accessibilité cognitive / FALC (facile à lire et à comprendre)* | CLEAN |
| DE | *geistige Behinderung / kognitive Barrierefreiheit / Leichte Sprache* | CLEAN |
| ZH | *智力残疾 (zhìlì cánjí) / 认知无障碍 / 易读信息* | PARTIAL |
| JA | *知的障害 (chiteki shōgai) / 認知的バリアフリー / やさしい日本語* | PARTIAL |
| NL | *verstandelijke beperking / cognitieve toegankelijkheid / begrijpelijke informatie* | CLEAN |
| ES | *discapacidad intelectual / accesibilidad cognitiva / lectura fácil* | CLEAN |
| PT | *deficiência intelectual / acessibilidade cognitiva / leitura fácil* | CLEAN |
| KO | *지적장애 / 인지 접근성 / 쉬운 정보* | CLEAN |
| IT | *disabilità intellettiva / accessibilità cognitiva / facile lettura* | CLEAN |

**Concept boundary warnings:**
- ZH: *认知无障碍* conflates IntD and NEU — distinguish carefully.
- JA: *認知的バリアフリー* conflates IntD and DEM in policy — filter findings.

---

### `critical-disability-studies-architecture`
**Domain:** Misfits theory; crip theory; normate body; social model grounding for specification writing; architectural history of exclusion; ableism and built form; Universal Design theory critique; disability justice and architecture

| Language | Native term | Map |
|---|---|---|
| SV | *normkritik / normkropp / social modell för funktionsnedsättning* | CLEAN |
| NO | *normkritisk perspektiv / normkroppen / sosial modell for funksjonshemming* | CLEAN |
| DA | *normalitetskritik / normkrop / social model for handicap* | CLEAN |
| FI | *normikritiikki / normatiivinen keho / vammaisuuden sosiaalinen malli* | CLEAN |
| FR | *validisme / corps normé / modèle social du handicap* | CLEAN |
| DE | *Ableismus / Normkörper / soziales Modell von Behinderung* | CLEAN |
| ZH | *能力主义 (néng lì zhǔyì) / 标准身体 / 残障社会模式* | PARTIAL |
| JA | *能力主義 (nōryokushugi) / 標準的な身体 / 障害の社会モデル* | CLEAN |
| NL | *validisme / normatief lichaam / sociaal model van handicap* | CLEAN |
| ES | *capacitismo / normocuerpo / modelo social de la discapacidad* | CLEAN |
| PT | *capacitismo / corpo normativo / modelo social da deficiência* | CLEAN |
| KO | *비장애중심주의 / 표준 신체 / 장애의 사회적 모델* | CLEAN |
| IT | *abilismo / corpo normativo / modello sociale della disabilità* | CLEAN |

**Concept boundary warnings:**
- ZH: CDS discourse less developed; policy uses ICF model. Search both *残障社会模式* (academic) and *ICF框架* (policy). Each language has a native CDS tradition — search native terms independently; do not presuppose engagement with EN theory.

---

### `OT-built-environment-interface`
**Domain:** OT interprofessional design practice; AOTA/CAOT/RCOT/COTEC evidence; OT housing literature; COPM applied to built environment; home modification evidence; OT involvement at design stage; AT-environment codependence

| Language | Native term | Map |
|---|---|---|
| SV | *arbetsterapi och byggd miljö / bostadsanpassning / ergoterapeut i planering* | CLEAN |
| NO | *ergoterapi og bygd miljø / boligtilpasning / ergoterapeut i planlegging* | CLEAN |
| DA | *ergoterapi og det byggede miljø / boligtilpasning* | CLEAN |
| FI | *toimintaterapia ja rakennettu ympäristö / asunnon muutostyöt* | CLEAN |
| FR | *ergothérapie et environnement bâti / adaptation du logement* | CLEAN |
| DE | *Ergotherapie und gebaute Umwelt / Wohnraumanpassung* | CLEAN |
| ZH | *作业治疗与建筑环境 (zuòyè zhìliáo yǔ jiànzhú huánjìng) / 住宅改造* | CLEAN |
| JA | *作業療法と建築環境 (sagyō ryōhō to kenchiku kankyō) / 住宅改修* | CLEAN |
| NL | *ergotherapie en gebouwde omgeving / woningaanpassing* | CLEAN |
| ES | *terapia ocupacional y entorno construido / adaptación del hogar* | CLEAN |
| PT | *terapia ocupacional e ambiente construído / adaptação da moradia* | CLEAN |
| KO | *작업치료와 건축 환경 / 주택 개조* | CLEAN |
| IT | *terapia occupazionale e ambiente costruito / adattamento abitativo* | CLEAN |

---

### `intersectionality-disability-design`
**Domain:** Disability + gender; disability + race/ethnicity; disability + age; Indigenous accessible design; culturally responsive accessible design; compound barrier analysis; disability justice framework

| Language | Native term | Map |
|---|---|---|
| SV | *intersektionalitet och funktionsnedsättning / kulturellt anpassad tillgänglighet* | CLEAN |
| NO | *interseksjonalitet og funksjonshemming / kulturelt tilpasset tilgjengelighet* | CLEAN |
| DA | *intersektionalitet og handicap / kulturelt tilpasset tilgængelighed* | CLEAN |
| FI | *intersektionaalisuus ja vammaisuus / kulttuurisesti mukautettu esteettömyys* | CLEAN |
| FR | *intersectionnalité et handicap / accessibilité culturellement adaptée* | CLEAN |
| DE | *Intersektionalität und Behinderung / kulturell angepasste Barrierefreiheit* | CLEAN |
| ZH | *交叉性与残障 / 文化适应性无障碍设计* | CLEAN |
| JA | *インターセクショナリティと障害 / 文化的配慮のバリアフリー* | CLEAN |
| NL | *intersectionaliteit en handicap / cultureel aangepaste toegankelijkheid* | CLEAN |
| ES | *interseccionalidad y discapacidad / diseño accesible culturalmente adaptado* | CLEAN |
| PT | *interseccionalidade e deficiência / design acessível culturalmente adaptado* | CLEAN |
| KO | *교차성과 장애 / 문화적으로 적응된 접근성 설계* | CLEAN |
| IT | *intersezionalità e disabilità / accessibilità culturalmente adattata* | CLEAN |

---

### `assistive-technology-built-environment`
**Domain:** AT-environment codependence (AT2030); power wheelchair circulation; AAC device sightlines; cochlear implant acoustics as AT-environment interface; AT enabling vs. built environment barriers

| Language | Native term | Map |
|---|---|---|
| SV | *hjälpmedel och byggd miljö / tekniska hjälpmedel och tillgänglighet* | CLEAN |
| NO | *hjelpemidler og bygd miljø / tekniske hjelpemidler og tilgjengelighet* | CLEAN |
| DA | *hjælpemidler og det byggede miljø / tekniske hjælpemidler og tilgængelighed* | CLEAN |
| FI | *apuvälineet ja rakennettu ympäristö / teknologiset apuvälineet ja esteettömyys* | CLEAN |
| FR | *aides techniques et environnement bâti / interfaces entre AT et accessibilité* | CLEAN |
| DE | *Hilfsmittel und gebaute Umwelt / technische Hilfsmittel und Barrierefreiheit / REHADAT* | CLEAN |
| ZH | *辅助技术与建筑环境 (fǔzhù jìshù yǔ jiànzhú huánjìng) / 无障碍与辅具接口* | CLEAN |
| JA | *福祉用具と建築環境 / 補助技術とバリアフリーの界面* | CLEAN |
| NL | *hulpmiddelen en gebouwde omgeving / technische hulpmiddelen en toegankelijkheid* | CLEAN |
| ES | *tecnología de apoyo y entorno construido / interfaz AT y accesibilidad* | CLEAN |
| PT | *tecnologia assistiva e ambiente construído / interface TA e acessibilidade* | CLEAN |
| KO | *보조기술과 건축 환경 / 보조공학과 접근성 인터페이스* | CLEAN |
| IT | *tecnologia assistiva e ambiente costruito / interfaccia AT e accessibilità* | CLEAN |

---

### `post-occupancy-evaluation-disability`
**Domain:** POE methodology adapted for accessible design; Brazilian APO tradition; COPM as POE proxy; HERD journal; user satisfaction measurement; building performance for accessibility

| Language | Native term | Map |
|---|---|---|
| SV | *brukaruppföljning / uppföljning av tillgänglighet* | CLEAN |
| NO | *brukererfaring / evaluering etter innflytting for tilgjengelighet* | CLEAN |
| DA | *brugerevaluering / evaluering efter indflytning for tilgængelighed* | CLEAN |
| FI | *käyttäjäpalaute / esteettömyyden arviointi rakennuksessa* | CLEAN |
| FR | *évaluation post-occupation (EPO) / performance d'accessibilité* | CLEAN |
| DE | *Nutzerbewertung / Barrierefreiheitsbewertung nach Bezug* | CLEAN |
| ZH | *使用后评价 (shǐyòng hòu píngjià) / 无障碍使用后评估* | CLEAN |
| JA | *使用後評価 (shiyōgo hyōka) / バリアフリー性能評価* | CLEAN |
| NL | *gebruiksevaluatie / nagevaluatie voor toegankelijkheid* | CLEAN |
| ES | *evaluación post-ocupación (EPO) / rendimiento de accesibilidad* | CLEAN |
| PT | *avaliação pós-ocupação (APO) / desempenho de acessibilidade* | CLEAN |
| KO | *거주 후 평가 / 접근성 성능 평가* | CLEAN |
| IT | *valutazione post-occupazione (VPO) / performance di accessibilità* | CLEAN |

---

### `children-disability-built-environment`
**Domain:** Paediatric accessible design; child-height reach ranges; paediatric healthcare design; sensory-appropriate school environments; children's wheelchair turning space; CHD anthropometric data  
**Priority:** P2 (Supplementary Volume)

| Language | Native term | Map |
|---|---|---|
| SV | *barn med funktionsnedsättning och byggd miljö / barnvänlig tillgänglighet* | CLEAN |
| NO | *barn med funksjonsnedsettelse og bygd miljø / barnvennlig universell utforming* | CLEAN |
| DA | *børn med funktionsnedsættelse og det byggede miljø / børnevenlig tilgængelighed* | CLEAN |
| FI | *vammaiset lapset ja rakennettu ympäristö / lapsiystävällinen esteettömyys* | CLEAN |
| FR | *enfants handicapés et environnement bâti / accessibilité adaptée aux enfants* | CLEAN |
| DE | *Kinder mit Behinderungen und gebaute Umwelt / kindgerechte Barrierefreiheit* | CLEAN |
| ZH | *残疾儿童与建筑环境 / 儿童无障碍设计* | CLEAN |
| JA | *障害のある子どもと建築環境 / 子ども向けバリアフリー設計* | CLEAN |
| NL | *kinderen met een beperking en gebouwde omgeving / kindvriendelijke toegankelijkheid* | CLEAN |
| ES | *niños con discapacidad y entorno construido / accesibilidad adaptada para niños* | CLEAN |
| PT | *crianças com deficiência e ambiente construído / acessibilidade adaptada para crianças* | CLEAN |
| KO | *장애 아동과 건축 환경 / 아동 친화적 접근성 설계* | CLEAN |
| IT | *bambini con disabilità e ambiente costruito / accessibilità adattata per bambini* | CLEAN |

---

### `little-people-built-environment`
**Domain:** Little people / short stature accessible design; LPA-specific reach range; anthropometric data; counter and surface heights; ATM and kiosk access for LPA  
**Priority:** P2 (Supplementary Volume)

| Language | Native term | Map |
|---|---|---|
| SV | *kortvuxna / liten kroppsbyggnad / tillgänglighet för kortvuxna* | CLEAN |
| NO | *lavvokste / liten kroppsbygning / tilgjengelighet for lavvokste* | CLEAN |
| DA | *lavtvoksne / lav kropsbygning / tilgængelighed for lavtvoksne* | CLEAN |
| FI | *lyhytkasvuinen / pienikokoinen / esteettömyys lyhytkasvuisille* | CLEAN |
| FR | *personnes de petite taille / nanisme / accessibilité pour personnes de petite taille* | CLEAN |
| DE | *Kleinwüchsige / Minderwuchs / Barrierefreiheit für Kleinwüchsige* | CLEAN |
| ZH | *矮小症 (ǎixiǎo zhèng) / 身材矮小 / 无障碍设计为矮小人群* | CLEAN |
| JA | *低身長 (teishinchou) / 低身長者のためのバリアフリー* | CLEAN |
| NL | *kleine gestalte / dwerggroei / toegankelijkheid voor mensen met kleine gestalte* | CLEAN |
| ES | *talla baja / enanismo / accesibilidad para personas de talla baja* | CLEAN |
| PT | *baixa estatura / nanismo / acessibilidade para pessoas de baixa estatura* | CLEAN |
| KO | *저신장 (jeosinjang) / 왜소증 / 저신장인을 위한 접근성 설계* | CLEAN |
| IT | *bassa statura / nanismo / accessibilità per persone di bassa statura* | CLEAN |

---

### `exceptional-height-built-environment`
**Domain:** Exceptional/tall stature; door clearance height; overhead hazard detection; EXH-specific clearance provisions  
**Priority:** P3 (Supplementary Volume)

| Language | Native term | Map |
|---|---|---|
| SV | *exceptionell kroppshöjd / mycket lång / tillgänglighet för långa* | CLEAN |
| NO | *eksepsjonell høyde / svært høy / tilgjengelighet for høyvokste* | CLEAN |
| DA | *exceptionel højde / meget høj / tilgængelighed for høje* | CLEAN |
| FI | *poikkeuksellinen pituus / erittäin pitkä / esteettömyys pitkäksvuisille* | CLEAN |
| FR | *grande taille exceptionnelle / accessibilité pour personnes de grande taille* | CLEAN |
| DE | *außergewöhnliche Körperhöhe / Barrierefreiheit für große Personen* | CLEAN |
| ZH | *异常高身材 / 超高人群的无障碍设计* | CLEAN |
| JA | *異常な身長 / 高身長者のためのバリアフリー* | CLEAN |
| NL | *uitzonderlijke lengte / toegankelijkheid voor lange mensen* | CLEAN |
| ES | *estatura excepcional / accesibilidad para personas de gran estatura* | CLEAN |
| PT | *estatura excepcional / acessibilidade para pessoas de grande estatura* | CLEAN |
| KO | *예외적 신장 / 고신장인을 위한 접근성 설계* | CLEAN |
| IT | *statura eccezionale / accessibilità per persone di alta statura* | CLEAN |

---

### `large-body-size-built-environment`
**Domain:** Bariatric design provisions; large body size spatial requirements; seating and fixture load ratings; turning and transfer space; dignity-centred large body design  
**Priority:** P2 (Supplementary Volume — Supp. Part 4 only. BAR is not a main taxonomy code.)

| Language | Native term | Map |
|---|---|---|
| SV | *bariatrisk design / stor kroppsstorlek / överviktsanpassad miljö* | CLEAN |
| NO | *bariatrisk design / stor kroppsstørrelse / tilgjengelighet for stor kroppsstørrelse* | CLEAN |
| DA | *bariatrisk design / stor kropsstørrelse / tilgængelighed for stor kropsstørrelse* | CLEAN |
| FI | *bariatrinen suunnittelu / suuri kehon koko / ylipainoisille sopiva ympäristö* | CLEAN |
| FR | *design bariatrique / grande corpulence / accessibilité pour les personnes obèses* | PARTIAL |
| DE | *bariatrisches Design / große Körpergröße / adipositasgerechte Gestaltung* | CLEAN |
| ZH | *大体型无障碍设计 / 肥胖症设计* | CLEAN |
| JA | *バリアトリックデザイン / 大きな体格 / 肥満者のためのバリアフリー設計* | CLEAN |
| NL | *bariatrisch ontwerp / grote lichaamsbouw / toegankelijkheid voor grote lichaamsbouw* | CLEAN |
| ES | *diseño bariátrico / gran corpulencia / accesibilidad para personas con gran tamaño corporal* | CLEAN |
| PT | *design bariátrico / grande porte corporal / acessibilidade para pessoas de grande porte* | CLEAN |
| KO | *비만 설계 / 대형 체형 접근성* | CLEAN |
| IT | *design bariatrico / grande corporatura / accessibilità per persone con grande corporatura* | CLEAN |

**Concept boundary warnings:**
- FR: French terminology tends toward stigmatising framing (*obèse*, *surpoids*) — use *grande corpulence* or *grande taille corporelle*; filter for dignity-centred evidence.
- All languages: Search using dignity-centred terms, not clinical obesity terminology.

---

## Citation-Mining Targets

| Source | Action |
|---|---|
| Hamraie (2017) *Building Access* | Backward + forward mining |
| Young et al. (2019) OT interprofessional design | Backward + forward mining |
| Zallio & Clarkson (2021) IDEA framework | Backward + forward mining |
| Bauman — DeafSpace guidelines | Seek via RIT InfoGuides / Gallaudet; backward mining |
| Keall et al. (2015, Lancet) NZ HIPI RCT | Backward + forward mining |

---

## Retired Slugs

| Retired slug | Maps to |
|---|---|
| `signing-space-corridor\` | `deaf-spatial-design\` |
| `BSL-signing-space-dimensions\` | `deaf-spatial-design\` |
| `cochlear-implant-acoustic-environment\` | `deaf-acoustic-built-environment\` |
| `protactile-haptic-infrastructure\` | `deafblind-built-environment\` |
| `ME-CFS-environment-built\` | `OFS-built-environment\` |
| `POTS-orthostatic-environment\` | `OFS-built-environment\` |
| `misfits-theory-built-environment\` | `critical-disability-studies-architecture\` |
| `building-access-hamraie-2017\` | Citation-mining target only |
| `OT-interprofessional-design-teams\` | `OT-built-environment-interface\` |
| `ADHD-built-environment-design\` | `neurodivergence-built-environment\` |
| `trauma-informed-design\` | `mental-health-built-environment\` |
| `disability-intersectionality-built-environment\` | `intersectionality-disability-design\` |
| `assistive-technology-built-environment-interface\` | `assistive-technology-built-environment\` |

- fatigue-spectrum-built-environment
- hearing-impairment-built-environment

---

# Slug Registry — Additions
**Appended:** 2026-03-19
**Scope:** Design library throughlines (Categories A–H) + residential rooms (R-ENT · R-GAR · R-LAU · R-BED · R-BA · R-LIV · R-KIT · R-HAL · R-STA)
**Method:** Throughline analysis — each slug covers a conceptual evidence domain spanning multiple items, not a one-to-one item mapping.
**Ageing-in-place:** Used as a generic cross-population search lens on all residential slugs and on applicable design-library slugs. Not a population code. Surfaces home-modification, Lifetime Homes, Visitability, and Nordic age-friendly housing evidence that is otherwise siloed from disability-specific literature.

---

## Design Library — Population Code Index (additions)

| Code | New slug(s) | Priority |
|---|---|---|
| DEAF | `assistive-listening-systems` | P1 |
| DEAF · NEU · NDV · DEM | `room-acoustic-performance` | P1 |
| NDV · NEU · MH · OFS | `sensory-relief-space-design` | P1 |
| NEU · NDV · DEM · VIS | `therapeutic-lighting-design` | P1 |
| VIS · DEAF | `visual-alerting-and-wayfinding-light` | P1 |
| VIS · DEM · NDV | `luminance-contrast-and-pattern` | P1 |
| DEM · NEU · NDV · VIS | `cognitive-wayfinding-design` | P1 |
| MOB · OFS | `accessible-circulation-geometry` | P1 |
| MOB · OFS · ALL | `threshold-and-level-access` | P1 |
| MOB · MOB/UPL · VIS · DEAF | `reach-range-and-accessible-controls` | P1 |

## Residential — Population Code Index (additions)

| Code | New slug(s) | Priority |
|---|---|---|
| MOB · MOB/UPL | `accessible-bathroom-and-grab-bar` | P1 |
| MOB · MOB/UPL · LPA | `residential-kitchen-and-task-surfaces` | P1 |
| MOB · OFS · DEM · ALL | `residential-entry-and-threshold` | P1 |
| MOB · DEM · OFS | `residential-internal-circulation` | P1 |
| MOB · OFS · DEM | `residential-bedroom-living-ot` | P2 |

---

## Full Slug Entries — Design Library Throughlines

---

### `room-acoustic-performance`
**Domain:** Room acoustic performance for disability populations; reverberation time (RT60); background noise levels (NC/NR); sound transmission class (STC); noise reduction coefficient (NRC); HVAC acoustic specification; flutter echo; partition performance; acoustic absorption materials. Serves DEAF (speech intelligibility), NEU (noise sensitivity, cognitive fatigue), NDV (sensory overload), DEM (acoustic calm).
**Covers items:** A-01 · A-02 · A-03 · A-04 · A-05 · A-06 · A-07 · A-08 · A-09 · A-14
**Governing compendium concept group:** CG 9

| Language | Native term | Map |
|---|---|---|
| SV | *Rumsakustik / efterklangstid / RT60 / ljuddämpning / bullerdämpning* | CLEAN |
| NO | *Romakustikk / etterklangstid / RT60 / lyddemping / NS 8175* | CLEAN |
| DA | *Rumakustik / efterklangstid / RT60 / lydabsorption / støjdæmpning* | CLEAN |
| FI | *Huoneakustiikka / jälkikaiunta-aika / RT60 / äänenvaimennus* | CLEAN |
| FR | *Acoustique intérieure / temps de réverbération / RT60 / isolation acoustique / arrêté acoustique* | CLEAN |
| DE | *Raumakustik / Nachhallzeit / RT60 / Schallabsorption / DIN 18041* | CLEAN |
| ZH | *室内声学 (shìnèi shēngxué) / 混响时间 / RT60 / 隔声性能* | CLEAN |
| JA | *室内音響 (shitsunai onkyō) / 残響時間 / RT60 / 吸音性能* | CLEAN |
| NL | *Ruimteakoestiek / nagalmtijd / RT60 / geluidsabsorptie / NEN-EN ISO 3382* | CLEAN |
| ES | *Acústica de recintos / tiempo de reverberación / TR60 / absorción acústica / CTE HR* | CLEAN |
| PT | *Acústica de ambientes / tempo de reverberação / TR60 / absorção sonora / NBR 10151* | CLEAN |
| KO | *실내 음향 / 잔향 시간 / RT60 / 흡음 성능 / 학교 시설 기준* | CLEAN |
| IT | *Acustica degli ambienti / tempo di riverberazione / TR60 / assorbimento acustico / UNI 11532* | CLEAN |

**Concept boundary warnings:**
- FR: French acoustic regulation (*arrêté relatif à l'acoustique des bâtiments*) governs residential performance separately from ERP — search both regulatory tracks. *Arrêté 2014* covers PMR spatial provisions; acoustic performance is a separate instrument.
- DE: DIN 18041:2016 is the definitive German standard for room acoustics in disability contexts; it supersedes DIN 18041:2004 and explicitly addresses DEAF and NEU populations — this is a primary source.
- JA: MEXT school acoustic standard and MLIT barrier-free law treat acoustic performance separately — search both. *文部科学省* governs schools; *国土交通省* governs barrier-free performance.
- KO: The Korean *편의증진법* does not specify RT60 values — KS (Korean Standards) and school facility standards govern. Search KS F ISO 3382 implementation and *학교시설 환경개선 5개년 계획* (school facility improvement plan) separately.

---

### `assistive-listening-systems`
**Domain:** Assistive listening system installation and performance; induction hearing loop (ILS) geometry and field strength; IEC 60118-4 / BS EN 60118-4 compliance; counter loop placement; room perimeter loop; Auracast / Bluetooth LE Audio as successor technology; ITU-T H.series development; cochlear implant telecoil interface; loop coverage mapping.
**Covers items:** A-10 · A-10b · A-11 · A-12
**Governing compendium concept group:** CG 3.3
**Distinct from:** `deaf-acoustic-built-environment` (which covers room acoustic performance for DEAF users, not ALS technology installation)

| Language | Native term | Map |
|---|---|---|
| SV | *Hörslinga / teleslinga / induktionsslinga / hörseltekniska hjälpmedel* | CLEAN |
| NO | *Teleslynge / hørselsslyfe / induktiv slyfe / hørselstekniske hjelpemidler* | CLEAN |
| DA | *Teleslynge / induktionssløjfe / hørehjælpemidler / høreslyfeanlæg* | CLEAN |
| FI | *Induktiosilmukka / kuuntelusilmukka / teleslinga / kuulonapuväline* | CLEAN |
| FR | *Boucle à induction magnétique (BIM) / boucle magnétique / système d'aide à l'audition* | CLEAN |
| DE | *Induktionsschleife / Höranlage / Hörschleife / DIN VDE 0834 / EN 60118-4* | CLEAN |
| ZH | *感应线圈 (gǎnyìng xiànquān) / 磁感应助听系统 / 助听环境设施* | CLEAN |
| JA | *磁気誘導ループ (jiki yūdō rūpu) / ヒアリングループ / 補聴援助システム* | PARTIAL |
| NL | *Ringleiding / inductielus / hoorlus / hoorassistentiesysteem* | CLEAN |
| ES | *Bucle magnético / bucle de inducción / sistema de ayuda a la audición* | CLEAN |
| PT | *Loop de indução / sistema de indução magnética / sistema de assistência auditiva* | CLEAN |
| KO | *자기유도루프 / 청각장애인 보조청취시스템 / 유도루프 시스템* | CLEAN |
| IT | *Anello ad induzione magnetica / sistema di ausilio all'udito / cappio magnetico* | CLEAN |

**Concept boundary warnings:**
- JA: *磁気誘導ループ* is the technical term but Japanese barrier-free policy predominantly uses *補聴援助システム* (hearing assistance system) generically — search both. Auracast has no Japanese standardisation yet; search under *Bluetooth LE Audio* + *補聴器*.
- All languages: Auracast / Bluetooth LE Audio infrastructure readiness (A-12) has no standard in any jurisdiction as of March 2026. Evidence base is manufacturer white papers and ITU-T H.series drafts only — flag all as THIN; rely on IEC 60118-4 loop evidence for specification grounding.
- DE: Standard corrected from DIN VDE 0828-1 to DIN VDE 0834 / EN 60118-4 (per compendium v2.0 audit finding).

---

### `sensory-relief-space-design`
**Domain:** Quiet room and sensory room provision; low-stimulation enclosure design; sensory gradient from entry to occupation; olfactory control and fragrance-free zones; graduated re-entry from sensory room to general space; no-sound-masking requirement for NEU populations; sensory decompression space evidence; ASPECTSS design principles in non-school settings; trauma-informed spatial decompression.
**Covers items:** A-13 · A-16 · A-17 · D-05 · F-01 · F-02 · F-03
**Governing compendium concept group:** CG 5 (emerging vocabulary)

| Language | Native term | Map |
|---|---|---|
| SV | *Sensorisk fristad / avlastningsrum / stimulusreducerat rum / sensorisk gradient* | PARTIAL |
| NO | *Sanseavlastningsrom / stimulusredusert rom / rolig rom / sensorisk gradient* | PARTIAL |
| DA | *Sensorisk fristed / stimulusreduceret rum / roligt rum / sensorisk gradient* | PARTIAL |
| FI | *Aistirauhoittumistila / viriketön tila / hiljainen huone / sensorinen gradientti* | PARTIAL |
| FR | *Espace de décharge sensorielle / espace snoezelen / salle apaisante / salle de retrait sensoriel* | PARTIAL |
| DE | *Snoezelen-Raum / Rückzugsraum / reizarmer Raum / Sensorikraum / Ruheraum* | CLEAN |
| ZH | *感觉减压空间 (gǎnjué jiǎnyā kōngjiān) / 感统训练室 / 安静室 / 感官中性空间* | PARTIAL |
| JA | *感覚調整室 (kankaku chōsei shitsu) / 静穏室 / 刺激軽減空間 / スヌーズレン* | PARTIAL |
| NL | *Snoezelen-ruimte / prikkelarme ruimte / rustige ruimte / sensorische terugtrektruimte* | CLEAN |
| ES | *Sala de descompresión sensorial / sala snoezelen / espacio de baja estimulación / sala tranquila* | PARTIAL |
| PT | *Sala de descompressão sensorial / sala snoezelen / espaço de baixa estimulação* | PARTIAL |
| KO | *감각 감압 공간 / 감각통합 훈련실 / 정온 공간 / 스누젤렌룸* | PARTIAL |
| IT | *Spazio di decompressione sensoriale / stanza snoezelen / ambiente a bassa stimolazione / stanza tranquilla* | PARTIAL |

**Concept boundary warnings:**
- All languages: *Snoezelen* is the dominant native term in most languages but originated as a therapeutic multi-sensory stimulation concept (Hulsegge and Verheul, 1987), not a low-stimulation relief space. The two concepts are opposed: Snoezelen adds sensory stimulation; sensory relief spaces reduce it. Searches using *snoezelen* will surface stimulation-room evidence (relevant for DEM) not decompression evidence (relevant for NDV/NEU). Distinguish explicitly in synthesis.
- ZH: *感统训练室* (sensory integration training room) is a clinical therapy term — distinguish built environment provision from therapy room design.
- All languages: This is the thinnest evidence base in the design library. NDV quiet room provision is well-supported for school settings (ASPECTSS) but residential and workplace evidence is sparse. Flag THIN outside school context; derive from school evidence base cautiously.

---

### `therapeutic-lighting-design`
**Domain:** Circadian lighting and melanopic equivalent daylight illuminance (EML/EDI); flicker-free LED specification (IEEE 1789-2015); individual dimming and user control; indirect and cove lighting; warm colour temperature for evening (CCT ≤2700 K); elimination of fluorescent overhead lighting; maximisation of natural light; lighting as DEM orientation support; NEU photosensitivity mitigation.
**Covers items:** B-01 · B-03 · B-04 · B-06 · B-07 · B-09 · B-11
**Ageing-in-place lens:** Age-related contrast sensitivity decline, scotopic vision loss, and increased glare sensitivity make therapeutic lighting a primary ageing-in-place design factor. Search *éclairage adapté au vieillissement* (FR), *altersgerechte Beleuchtung* (DE), *高齢者照明環境* (JA), *äldreboende belysning* (SV) in addition to disability-specific terms.

| Language | Native term | Map |
|---|---|---|
| SV | *Ljusterapi / dygnsrytmbelysning / bländfri belysning / flimmerfri belysning / äldreboende belysning* | CLEAN |
| NO | *Døgnrytmbelysning / terapeutisk belysning / blendingsfri belysning / flimmerfri belysning* | CLEAN |
| DA | *Døgnrytmebelysning / terapeutisk belysning / blændfri belysning / flimmerfri belysning* | CLEAN |
| FI | *Vuorokausirytmivalaistus / terapeuttinen valaistus / häikäisemätön valaistus / välkkymätön valaistus* | CLEAN |
| FR | *Éclairage circadien / éclairage thérapeutique / éclairage sans éblouissement / éclairage adapté au vieillissement* | CLEAN |
| DE | *Circadiane Beleuchtung / therapeutische Beleuchtung / blendfreie Beleuchtung / altersgerechte Beleuchtung / flimmerfreie LED* | CLEAN |
| ZH | *昼夜节律照明 (zhòuyè jiélǜ zhàomíng) / 治疗性照明 / 无眩光照明 / 老年人照明环境* | CLEAN |
| JA | *サーカディアン照明 (sākadian shōmei) / 治療的照明 / 高齢者照明環境 / フリッカーフリー照明* | CLEAN |
| NL | *Circadiaanse verlichting / therapeutische verlichting / verblindingsvrije verlichting / ouderenverlichting* | CLEAN |
| ES | *Iluminación circadiana / iluminación terapéutica / iluminación sin deslumbramiento / iluminación para el envejecimiento* | CLEAN |
| PT | *Iluminação circadiana / iluminação terapêutica / iluminação sem ofuscamento / iluminação para envelhecimento* | CLEAN |
| KO | *일주기 리듬 조명 / 치료적 조명 / 눈부심 없는 조명 / 고령자 조명 환경* | CLEAN |
| IT | *Illuminazione circadiana / illuminazione terapeutica / illuminazione senza abbagliamento / illuminazione per anziani* | CLEAN |

**Concept boundary warnings:**
- All languages: EML/EDI (melanopic equivalent daylight illuminance) is a recently standardised metric (CIE S 026:2018). Most non-English regulatory standards have not yet adopted it — expect CLEAN conceptual match but THIN standard-value evidence outside EN/DE. Derive from EN and CIE guidance; flag jurisdiction-specific values as absent.
- DE: *altersgerechte Beleuchtung* is a well-developed German evidence base — search separately via KDA and Kuratorium Deutsche Altershilfe publications.

---

### `visual-alerting-and-wayfinding-light`
**Domain:** Visual fire alarm (VAD/strobe) placement and performance; LRV contrast at critical junctions as wayfinding support; glare and reflectance as navigation barrier; lighting transition zone design at major illuminance changes; lip-reading and sign language illumination (shadow-free face illumination).
**Covers items:** B-02 · B-05 · B-08 · B-10
**Governing compendium concept group:** CG 8 (luminance contrast) + CG 2.1 (DEAF signing space)
**Distinct from:** `luminance-contrast-and-pattern` (which covers surface and material LRV) and `therapeutic-lighting-design` (which covers spectrum and circadian quality)

| Language | Native term | Map |
|---|---|---|
| SV | *Visuell brandlarm / blixtsignal / kontrastbelysning / bländskyddsbelysning* | CLEAN |
| NO | *Visuelt brannvarsel / blitsvarsel / kontrastbelysning / TEK17 lys* | CLEAN |
| DA | *Visuel brandmelding / blixtsignal / kontrastbelysning / BR18 lys* | CLEAN |
| FI | *Visuaalinen palohälytin / salamahälytin / kontrastivälivalaistus* | CLEAN |
| FR | *Détecteur visuel d'incendie / flash stroboscopique d'évacuation / signalisation lumineuse d'alarme / éclairage de contraste* | CLEAN |
| DE | *Optischer Feueralarm / Blitzleuchte / visuelles Warnsystem / DIN VDE 0833 / Kontrastbeleuchtung* | CLEAN |
| ZH | *视觉火灾报警 (shìjué huǒzāi bàojǐng) / 频闪报警器 / 对比度照明 / 视觉疏散指示* | CLEAN |
| JA | *光警報装置 (hikari keihō sōchi) / 視覚的火災警報 / コントラスト照明 / 視覚誘導照明* | CLEAN |
| NL | *Visueel brandalarm / stroboscoopalarm / contrastverlichting / waarschuwingsverlichting* | CLEAN |
| ES | *Alarma visual de incendio / flash estroboscópico / iluminación de contraste / señalización luminosa de emergencia* | CLEAN |
| PT | *Alarme visual de incêndio / flash estroboscópico / iluminação de contraste / sinalização luminosa de emergência* | CLEAN |
| KO | *시각 화재 경보 / 점멸 경보기 / 대비 조명 / 시각적 피난 유도* | CLEAN |
| IT | *Allarme visivo antincendio / lampeggiatore stroboscopico / illuminazione di contrasto / segnalazione luminosa d'emergenza* | CLEAN |

**Concept boundary warnings:**
- DE: DIN VDE 0833 governs fire alarm systems including visual alerting — primary source. Contrast between visual alarm and visual wayfinding lighting is not always clearly distinguished in German regulatory guidance; synthesise both.
- All languages: Lip-reading illumination (B-02) is addressed almost exclusively in Deaf-community and DeafSpace literature, not general lighting standards. Expect THIN in standards-based searches; rely on Co-1/Tier 2 sources (Gallaudet / NDCS / national Deaf associations) for this item.

---

### `luminance-contrast-and-pattern`
**Domain:** Luminance contrast (LRV differential) at critical junctions; colour palette selection for disability populations; pattern avoidance on flooring and walls; DEM inverse contrast rule (floor perceived as drop); plain low-contrast flooring for DEM; colour-coded wayfinding zones; tactile surface differentiation for VIS.
**Covers items:** C-01 · C-02 · C-03 · C-04 · C-05 · C-06
**Governing compendium concept group:** CG 8
**Ageing-in-place lens:** Age-related contrast sensitivity decline makes LRV specification a primary ageing-in-place factor. *Contraste de luminance et vieillissement* (FR), *Leuchtdichtekontrast im Alter* (DE) surface age-specific evidence distinct from disability evidence.

| Language | Native term | Map |
|---|---|---|
| SV | *Luminanskontrast / LRV-differens / kontrastmarkering / mönsterundvikande / demensanpassad färgsättning* | CLEAN |
| NO | *Luminanskontrast / reflektansverdier / kontrastmarkering / mønsterunngåelse / demensvennlig fargesetting* | CLEAN |
| DA | *Luminanskontrast / LRV-differens / kontrastmarkering / mønsterunddragelse / demensvenlighed farver* | CLEAN |
| FI | *Luminanssikontrasti / LRV-ero / kontrastivärimerkintä / kuvioiden välttäminen / dementiapotilaan väriympäristö* | CLEAN |
| FR | *Contraste de luminance / facteur de luminance / marquage de contraste / évitement des motifs / CEREMA* | PARTIAL |
| DE | *Leuchtdichtekontrast / Kontrast K / DIN 32975 / Kontrastmarkierung / Musterfreiheit / demenzgerechte Farbgebung* | CLEAN |
| ZH | *亮度对比度 / LRV差值 / 对比标记 / 避免图案 / 失智症友善色彩* | CLEAN |
| JA | *輝度比 / 明度差 / コントラストマーキング / パターン回避 / 認知症対応色彩* | CLEAN |
| NL | *Luminantiecontrast / reflectiewaarde / contrastmarkering / patroonvermijding / dementievriendelijke kleurstelling* | CLEAN |
| ES | *Contraste de luminancia / diferencial LRV / marcado de contraste / evitación de patrones / CTE SUA* | CLEAN |
| PT | *Contraste de luminância / diferencial LRV / marcação de contraste / evitação de padrões / NBR 9050* | CLEAN |
| KO | *휘도 대비 / LRV 차이 / 대비 표시 / 패턴 회피 / 치매 친화적 색채* | CLEAN |
| IT | *Contrasto di luminanza / differenziale LRV / marcatura di contrasto / evitazione dei motivi / DM 236/89* | CLEAN |

**Concept boundary warnings:**
- FR: French standard uses *facteur de luminance* expressed as a percentage ratio (≥70%), not LRV differential (≥30 points). These are different measurement conventions — do not conflate in synthesis. CEREMA guidance must be read to convert.
- JA: Japanese standard uses *輝度比* (luminance ratio ≥ 3:1), not LRV differential. Conversion required for specification reconciliation.
- ES: CTE SUA uses percentage (≥70%) — same conversion issue as FR.
- DEM inverse contrast rule (C-05): evidence is almost exclusively Anglo-Scottish (DSDC, Stirling) and German (KDA). Other language traditions have minimal evidence on this specific provision — flag THIN and derive from those primary sources.

---

### `cognitive-wayfinding-design`
**Domain:** Cognitive wayfinding design; loop circulation preventing dead ends; single primary route simplicity; toilet visibility without navigation; landmarks at decision points; sightline design; no blind corners; pictogram and single-word signage; transparent glazed panels for orientation; consistent furniture layout. Applies across DEM, NEU, NDV, and VIS populations with different but convergent rationales.
**Covers items:** D-01 · D-02 · D-03 · D-04 · D-07 · D-08 · D-09 · D-10
**Governing compendium concept group:** CG 10 (dementia design) + CG 5 (emerging vocabulary)
**Ageing-in-place lens:** Cognitive wayfinding evidence in residential contexts comes substantially from ageing-in-place and dementia care literature. *高齢者向けワイファインディング* (JA), *orientierung im Alter* (DE), *Leve hele livet* wayfinding component (NO) are targeted search terms.

| Language | Native term | Map |
|---|---|---|
| SV | *Kognitiv orientering / demensvänlig orientering / orienteringsanvisningar / bildpiktogram / möblering och orienteringslandmärken* | CLEAN |
| NO | *Kognitiv orientering / demensvennlig orientering / orienteringsskilt / piktogrammer / møblering og landemerker* | CLEAN |
| DA | *Kognitiv orientering / demensvenlighed orientering / orienteringsskiltning / piktogrammer / møblering og vartegn* | CLEAN |
| FI | *Kognitiivinen orientoituminen / dementiaystävällinen orientoituminen / kuvasignalisaatio / huonekalujen johdonmukaisuus* | CLEAN |
| FR | *Orientation cognitive / repères visuels / balisage pictogramme / cohérence du mobilier / cheminement intuitif* | CLEAN |
| DE | *Kognitive Orientierung / demenzgerechte Orientierung / Leitzeichensystem / Piktogramme / Orientierungslandmarken / KDA* | CLEAN |
| ZH | *认知导航 (rènzhī dǎoháng) / 失智症友善空间指引 / 图文标识 / 标志性导向元素* | CLEAN |
| JA | *認知的案内 (ninchiteki annai) / 認知症対応ウェイファインディング / ピクトグラム / 家具レイアウトの一貫性* | CLEAN |
| NL | *Cognitieve oriëntatie / dementievriendelijke oriëntatie / pictogramborden / meubilairsconsistentie / herkenningspunten* | CLEAN |
| ES | *Orientación cognitiva / señalización pictográfica / diseño para demencia / coherencia del mobiliario / referencias visuales* | CLEAN |
| PT | *Orientação cognitiva / sinalização pictográfica / design para demência / coerência do mobiliário / referências visuais* | CLEAN |
| KO | *인지적 길 찾기 / 치매 친화적 공간 안내 / 그림 표지판 / 가구 일관성* | CLEAN |
| IT | *Orientamento cognitivo / progettazione per la demenza / segnaletica pittografica / coerenza dell'arredamento / punti di riferimento* | CLEAN |

**Concept boundary warnings:**
- DE: KDA (*Kuratorium Deutsche Altershilfe*) and *Deutsche Alzheimer Gesellschaft* are primary sources for German-language DEM wayfinding evidence — retrieve directly before academic database search.
- JA: Japanese group home (*グループホーム*) design standards contain specific wayfinding provisions for DEM — search MHLW facility standards (*老人福祉施設*) directly.
- All languages: NDV (particularly AUT) and DEM wayfinding evidence uses different rationales but often converges on similar provisions. Distinguish underlying evidence carefully in synthesis; do not merge AUT and DEM findings.

---

### `accessible-circulation-geometry`
**Domain:** Accessible lift minimum car dimensions; platform lift provision; corridor clear width (minimum and best practice); rest seating intervals on circulation routes; automatic sliding door provision; turning circle/manoeuvring space dimensions; wheelchair circulation routes.
**Covers items:** E-01 · E-02 · E-08 · E-09 · E-10 · E-11
**Governing compendium concept group:** CG 6 (turning radius) + CG 7 (door width) + CG 3.1 (corridor width)
**Ageing-in-place lens:** Rest seating interval evidence and lift provision evidence derives substantially from ageing-in-place literature. *Aldersvennlig bolig* (NO), *generationengerechtes Wohnen* (DE), *住み続けられる住宅* (JA) all address this evidence domain. Search in parallel with disability-specific sources.

| Language | Native term | Map |
|---|---|---|
| SV | *Hissbredd / korridor fribredd / vilplatser / snusyta / automatiska dörrar / tillgänglig hiss* | CLEAN |
| NO | *Hissdimensjoner / korridor friareal / hvilebenker / snusrom / automatiske dører / aldersvennlig sirkulasjon* | CLEAN |
| DA | *Elevatordimensioner / korridor fribredde / hvilepladser / vendeplads / automatiske døre* | CLEAN |
| FI | *Hissin mitat / käytävän vapaa leveys / levähdyspaikat / kääntymistila / automaattiovet* | CLEAN |
| FR | *Dimensions d'ascenseur / largeur libre de couloir / aires de repos / espace de retournement / portes automatiques* | CLEAN |
| DE | *Aufzugmaße / Flurbreite / Ruhebänke / Bewegungsfläche / automatische Türen / DIN 18040* | CLEAN |
| ZH | *电梯尺寸 / 走廊净宽 / 休息座椅 / 轮椅回转空间 / 自动门* | CLEAN |
| JA | *エレベーター寸法 / 廊下有効幅員 / 休憩ベンチ / 車いす転回スペース / 自動ドア / バリアフリー法施行令* | CLEAN |
| NL | *Liftafmetingen / gangbreedte / rustplaatsen / draaicirkel / automatische deuren / NEN 9120* | CLEAN |
| ES | *Dimensiones de ascensor / anchura libre de pasillo / zonas de descanso / espacio de giro / puertas automáticas / CTE SUA* | CLEAN |
| PT | *Dimensões de elevador / largura livre de corredor / áreas de descanso / espaço de giro / portas automáticas / NBR 9050* | CLEAN |
| KO | *엘리베이터 치수 / 복도 유효 폭 / 휴식 공간 / 휠체어 회전공간 / 자동문 / 편의시설 설치 기준* | CLEAN |
| IT | *Dimensioni ascensore / larghezza netta corridoio / aree di sosta / spazio di manovra / porte automatiche / DM 236/89* | CLEAN |

**Concept boundary warnings:**
- All languages: Rest seating interval evidence (E-10) is almost entirely derived from OFS/ME-CFS clinical literature and OT energy conservation research rather than built environment standards — no jurisdiction specifies a seating interval in its building code. Expect NO-DATA from standards searches; rely on OT clinical literature and Tiresias / ME Association guidance.
- KO: Korean *편의시설 설치 기준* specifies corridor width and turning space values that are more granular than ADA in several categories (per compendium S-08 finding) — retrieve directly; do not assume ADA values are representative.

---

### `threshold-and-level-access`
**Domain:** Level (zero-step) entry provision; ramp gradient specification; ramp design for OFS/MS fatigue; accessible parking dimensions and location; weather protection at entry; slip resistance (PTV/pendulum value) for wet surfaces; threshold design as DAR trigger.
**Covers items:** E-03 · E-04 · E-05 · E-06 · E-07
**Ageing-in-place lens:** Level entry and ramp provision are the highest-frequency home modification interventions in ageing-in-place literature across all jurisdictions. This slug will surface Lifetime Homes criterion 5 (level or gently sloping approach), Visitability (one zero-step entry), HAFI (Canada), and Nordic *aldersvennlig bolig* evidence. Search *adaptation du logement pour le maintien à domicile* (FR), *Wohnraumanpassung Schwellensenkung* (DE), *住宅改修段差解消* (JA) in addition to disability-specific terms.

| Language | Native term | Map |
|---|---|---|
| SV | *Nolltröskel / tillgänglig entré / rampgradient / halkfria ytor / parkeringsbredd / väderskyddad entré* | CLEAN |
| NO | *Nullterskel / tilgjengelig inngang / rampegradient / sklisikre flater / parkeringsbredde / aldersvennlig adkomst* | CLEAN |
| DA | *Nultærskel / tilgængelig indgang / rampegradient / skridsikre overflader / parkeringsbredde* | CLEAN |
| FI | *Tasainen kynnys / esteetön sisäänkäynti / luiskan kaltevuus / liukuestepinnat / pysäköintileveys* | CLEAN |
| FR | *Seuil nul / entrée accessible / pente de rampe / revêtement antidérapant / largeur de stationnement / maintien à domicile* | CLEAN |
| DE | *Schwellenfreiheit / barrierefreier Eingang / Rampengefälle / rutschhemmender Belag / Wohnraumanpassung / DIN 18040-2* | CLEAN |
| ZH | *无障碍入口 / 坡道坡度 / 防滑地面 / 停车位宽度 / 住宅改造* | CLEAN |
| JA | *段差解消 (dansakaishō) / バリアフリー玄関 / スロープ勾配 / 滑り止め / 住宅改修 / バリアフリー法* | CLEAN |
| NL | *Drempelvrij / toegankelijke entree / hellingshoekingang / antislipvloer / parkeerplaatsbreedte / woningaanpassing* | CLEAN |
| ES | *Entrada sin escalón / acceso a nivel / pendiente de rampa / pavimento antideslizante / ancho de aparcamiento / CTE SUA* | CLEAN |
| PT | *Entrada sem degrau / acesso nivelado / inclinação de rampa / piso antiderrapante / largura de estacionamento / NBR 9050* | CLEAN |
| KO | *단차 없는 입구 / 무장애 출입구 / 경사로 기울기 / 미끄럼 방지 바닥 / 주차 폭 / 편의증진법* | CLEAN |
| IT | *Ingresso senza gradini / accesso livellato / pendenza rampa / pavimento antiscivolo / larghezza parcheggio / DM 236/89* | CLEAN |

**Concept boundary warnings:**
- All languages: Ageing-in-place home modification evidence (住宅改修, Wohnraumanpassung, adaptation du logement) runs in parallel to disability-specific evidence and frequently uses different terminology. Both tracks must be searched; findings should be synthesised but provenance distinguished.
- JA: *段差解消* (step elimination) is the primary Japanese term for level access in both the barrier-free and ageing-in-place literature — it is the correct primary search term for this slug in Japanese, preferable to any translation of "level entry."

---

### `reach-range-and-accessible-controls`
**Domain:** Accessible height zone for controls and switches (400–1100 mm AFF); operable force limits for switches and hardware (≤22 N); individual environmental control (IEC) for lighting and temperature; visual paging and real-time captioning provision; accessible intercom and video door entry; adjustable-height work surface range; reception counter accessible height section.
**Covers items:** G-05 · G-06 · H-01 · H-02 · H-03 · H-04
**Governing compendium concept group:** CG 7 (door width / operating force)
**Ageing-in-place lens:** Reach range and operable force evidence derives heavily from ageing-in-place and OT home modification literature. Age-related strength loss (grip, pinch), reduced ROM, and upper limb changes are primary evidence sources — search *controls accessibilité personnes âgées* (FR), *Bedienelemente Barrierefreiheit Alter* (DE) in addition to disability terms.

| Language | Native term | Map |
|---|---|---|
| SV | *Betjeningshöjd / åtkomsthöjd / manöverkraft / individuell miljökontroll / visuellt pagingsystem / bildtelefon* | CLEAN |
| NO | *Betjeningshøyde / rekkevidde / manøvreringskraft / individuell miljøstyring / visuell varsling* | CLEAN |
| DA | *Betjeningshøjde / rækkevidde / betjeningskraft / individuel miljøstyring / visuel varsling* | CLEAN |
| FI | *Käyttökorkeusalue / ulottuvuusalue / käyttövoima / yksilöllinen ympäristönhallinta / visuaalinen hälytys* | CLEAN |
| FR | *Hauteur de commande / zone de portée / effort de manœuvre / contrôle environnemental individuel / système de page visuel* | CLEAN |
| DE | *Bedienhöhe / Greifbereich / Betätigungskraft / individuelle Umgebungssteuerung / visuelles Rufsystem / DIN 18040* | CLEAN |
| ZH | *操控高度 / 可及范围 / 操控力 / 个人环境控制系统 / 可视对讲系统* | CLEAN |
| JA | *操作高さ / リーチレンジ / 操作力 / 個別環境制御システム / 視覚的呼び出しシステム* | CLEAN |
| NL | *Bedieningshoogte / bereikzone / bedieningskracht / individuele omgevingsbeheersing / visueel oproepsysteem* | CLEAN |
| ES | *Altura de mando / zona de alcance / fuerza de maniobra / control ambiental individual / sistema de llamada visual / DALCO* | CLEAN |
| PT | *Altura de comando / zona de alcance / força de manobra / controle ambiental individual / sistema de chamada visual / NBR 9050* | CLEAN |
| KO | *조작 높이 / 도달 범위 / 조작력 / 개인 환경 제어 / 시각적 호출 시스템 / 편의증진법* | CLEAN |
| IT | *Altezza di comando / zona di portata / forza di manovra / controllo ambientale individuale / sistema di chiamata visiva / DM 236/89* | CLEAN |

**Concept boundary warnings:**
- All languages: Individual environmental control (H-02) evidence is primarily from AT and smart home literature, not building standards — building codes do not address IEC provision. Expect NO-DATA from standards databases; search AT product evidence, OT smart home literature, and NDV/OFS patient organisation publications.
- ES: Spanish *DALCO* accessibility criterion (*Aprehensión*) specifically addresses operable force — this is the correct primary regulatory reference for ES reach range and force evidence.

---

## Full Slug Entries — Residential Rooms

---

### `accessible-bathroom-and-grab-bar`
**Domain:** Accessible wet room configuration (zero threshold, no shower tray); grab bar clinical positioning (bilateral, oblique, horizontal, vertical); grab bar geometry and load rating; transfer space at WC; turning circle at bathroom entry; anti-scald provision for MOB/UPL; shower seat provision; residential versus institutional bathroom design differences; home bathroom modification evidence.
**Covers items:** G-03 · G-04 · I-03 · R-BA (R-BA-01 through R-BA-05)
**Governing compendium concept group:** CG 3.5 (accessible toilet/wet room) + CG 6 (turning radius)
**Ageing-in-place lens:** Bathroom modification is the single most-evidenced home adaptation intervention in the ageing-in-place literature across all jurisdictions. *Wohnraumanpassung Bad* (DE), *adaptation salle de bain maintien à domicile* (FR), *浴室改造 / 住宅改修* (JA), *badkameraaanpassing* (NL), *boligtilpasning bad* (NO), *badrumsanpassning* (SV) are all rich evidence sources. Search in parallel with disability-specific sources; synthesis must distinguish ageing-evidence from disability-specific evidence where the two diverge (particularly on grab bar positioning, where OT evidence for disability populations is more specific than ageing-in-place guidance).

| Language | Native term | Map |
|---|---|---|
| SV | *Tillgängligt badrum / duschutrymme utan tröskel / handtag / stödhandtag / duschsits / badrumsanpassning / snusyta i badrum* | CLEAN |
| NO | *Tilgjengelig bad / terskelfrittdusj / støttehåndtak / dusjsete / boligtilpasning bad / snusrom i bad* | CLEAN |
| DA | *Tilgængeligt badeværelse / tærskelfridt brusebad / støttegreb / brusesæde / boligtilpasning badeværelse* | CLEAN |
| FI | *Esteetön kylpyhuone / kynnyksetön suihku / tukikahva / suihkuistuin / asunnon muutostyöt kylpyhuone* | CLEAN |
| FR | *Salle de bain accessible / douche à l'italienne / barre d'appui / siège de douche / adaptation salle de bain maintien à domicile* | CLEAN |
| DE | *Barrierefreies Bad / ebenerdige Dusche / Haltegriff / Duschsitz / Wohnraumanpassung Bad / DIN 18040-2* | CLEAN |
| ZH | *无障碍浴室 / 零坎位淋浴 / 扶手安装 / 沐浴椅 / 浴室改造 / 住宅改修* | CLEAN |
| JA | *バリアフリーバスルーム / 段差なしシャワー / 手すり設置 (てすりせっち) / シャワーチェア / 浴室改修* | CLEAN |
| NL | *Toegankelijke badkamer / drempelvrije douche / beugel / douchestoel / badkameraanpassing / NEN 9120* | CLEAN |
| ES | *Baño accesible / ducha a nivel / barra de apoyo / asiento de ducha / adaptación de baño para mayores / CTE SUA* | CLEAN |
| PT | *Banheiro acessível / box sem degrau / barra de apoio / assento de banho / adaptação de banheiro para idosos / NBR 9050* | CLEAN |
| KO | *접근 가능한 욕실 / 턱 없는 샤워 / 안전 손잡이 설치 / 샤워 의자 / 욕실 개조 / 편의시설 설치 기준* | CLEAN |
| IT | *Bagno accessibile / doccia a filo pavimento / maniglione / sedile doccia / adattamento del bagno per anziani / DM 236/89* | CLEAN |

**Concept boundary warnings:**
- All languages: Grab bar positioning evidence from ageing-in-place research tends to recommend fewer and less precisely positioned bars than OT clinical evidence for disability populations. Distinguish evidence provenance in synthesis; OT clinical evidence (Co-1/Tier 1) takes precedence over ageing-in-place guidance for specification of grab bar position.
- KO: Korean *편의시설 설치 기준* specifies grab bar positioning in more detail than ADA in several scenarios — retrieve directly.

---

### `residential-kitchen-and-task-surfaces`
**Domain:** Residential kitchen accessibility; adjustable-height worktop range; knee clearance under counter for wheelchair users; one-handed kitchen operation; appliance placement and reach range; sink and hob height; storage at accessible height; pull-out shelving; accessible tap and control specification; cooktop safety (anti-scald); laundry appliance height.
**Covers items:** I-02 · G-05 · R-KIT · R-LAU (partially)
**Ageing-in-place lens:** Kitchen modification evidence is the second most common home adaptation category in ageing-in-place literature. *Küchenanpassung für Senioren* (DE), *adaptation cuisine maintien à domicile* (FR), *キッチン改修 高齢者* (JA) are primary search terms. Height-adjustable kitchen evidence base (Neff, Blum) is primarily European; North American evidence emphasises knee clearance.

| Language | Native term | Map |
|---|---|---|
| SV | *Tillgängligt kök / höjdjusterbar bänkskiva / knäfrirum under diskbänk / envändskök / hushållsmaskinhöjd* | CLEAN |
| NO | *Tilgjengelig kjøkken / høydejusterbar benkeplate / kneklaringsrom / envhåndskjøkken / boligtilpasning kjøkken* | CLEAN |
| DA | *Tilgængeligt køkken / højdejusterbar bordplade / knæfrirum / enkelhåndskøkken / boligtilpasning køkken* | CLEAN |
| FI | *Esteetön keittiö / korkeussäädettävä työtaso / polvitila / yhden käden käyttö / asunnon muutostyöt keittiö* | CLEAN |
| FR | *Cuisine accessible / plan de travail réglable en hauteur / espace libre sous le plan / cuisine adaptée maintien à domicile* | CLEAN |
| DE | *Barrierefreie Küche / höhenverstellbare Arbeitsfläche / Kniefreiheit / Einhandküche / Wohnraumanpassung Küche / DIN 18040-2* | CLEAN |
| ZH | *无障碍厨房 / 可调高度台面 / 轮椅膝部净空 / 单手操作厨房 / 厨房改造* | CLEAN |
| JA | *バリアフリーキッチン / 高さ調整可能ワークトップ / 膝下クリアランス / 片手操作 / キッチン改修* | CLEAN |
| NL | *Toegankelijke keuken / in hoogte verstelbaar werkblad / knieholte-vrije ruimte / eenhandig koken / keukenadaptatie* | CLEAN |
| ES | *Cocina accesible / encimera regulable en altura / espacio libre bajo encimera / operación con una mano / adaptación cocina mayores* | CLEAN |
| PT | *Cozinha acessível / bancada regulável em altura / espaço livre sob a bancada / operação com uma mão / adaptação cozinha para idosos* | CLEAN |
| KO | *접근 가능한 주방 / 높이 조절 가능 조리대 / 무릎 여유 공간 / 한 손 조작 주방 / 주방 개조* | CLEAN |
| IT | *Cucina accessibile / piano di lavoro regolabile in altezza / spazio libero sotto il piano / utilizzo con una mano / adattamento cucina anziani* | CLEAN |

**Concept boundary warnings:**
- All languages: Height-adjustable worktop evidence (ISO/EN motor-driven and manual systems) is primarily industrial/workplace ergonomics literature. Residential kitchen applications are less well-evidenced; derive from workplace ergonomics and OT home modification sources. Knoll, Neff, and Blum (European kitchen system manufacturers) have published specification evidence — flag as grey literature Tier 5 / manufacturer-source.
- LPA note: LPA kitchen evidence (LPA-08 in Supplementary Volume) is a distinct and thinner evidence base than MOB kitchen evidence. Distinguish LPA-specific reach-range requirements from wheelchair-user knee clearance requirements in synthesis.

---

### `residential-entry-and-threshold`
**Domain:** Residential entry accessibility; zero-step threshold at principal entrance; covered approach and weather protection; accessible parking adjacent to dwelling; door hardware at entry (lever handle, operable force); video door entry with visual feedback; threshold as DAR trigger; accessible approach route from parking to entry; garage to dwelling access.
**Covers items:** R-ENT · R-GAR · E-06 (residential application)
**Ageing-in-place lens:** Entry threshold and approach route modifications are the highest-frequency interventions in home modification programmes across all jurisdictions. This slug will be the primary entry point for Lifetime Homes criterion 1–4 (approach and entry), Visitability (one zero-step entry), HAFI programme evidence (Canada), *MaPrimeAdapt* (FR), *Wohnraumanpassung Eingang* (DE), and Nordic *aldersvennlig bolig* entry criteria. The ageing-in-place evidence base for this slug exceeds the disability-specific evidence base in volume — search both; distinguish in synthesis.

| Language | Native term | Map |
|---|---|---|
| SV | *Tillgänglig entré / nolltröskel / väderskyddat entreeutrymme / tillgänglig parkering / dörrhandtag / bostadens entré* | CLEAN |
| NO | *Tilgjengelig inngang / nullterskel / vær­beskytt inngang / tilgjengelig parkering / dørgrep / aldersvennlig adkomst* | CLEAN |
| DA | *Tilgængelig indgang / nultærskel / vejrbeskyttet indgang / tilgængelig parkering / dörgreb / ældrevenlig adgang* | CLEAN |
| FI | *Esteetön sisäänkäynti / tasainen kynnys / sään suojaama sisäänkäynti / esteetön pysäköinti / ovenkahva / asunnon muutostyöt sisäänkäynti* | CLEAN |
| FR | *Entrée accessible / seuil nul / abri d'entrée / stationnement accessible / poignée de porte / maintien à domicile entrée / MaPrimeAdapt* | CLEAN |
| DE | *Barrierefreier Eingang / Schwellenfreiheit / Witterungsschutz Eingang / barrierefreier Stellplatz / Türgriff / Wohnraumanpassung Eingang / DIN 18040-2* | CLEAN |
| ZH | *无障碍入口 / 零台阶 / 遮蔽入口 / 无障碍停车位 / 住宅改修入口 / 适老化改造入口* | CLEAN |
| JA | *バリアフリー玄関 / 段差解消 / 雨よけ / 車いす駐車スペース / レバーハンドル / 住宅改修玄関 / 高齢者向け玄関改修* | CLEAN |
| NL | *Toegankelijke entree / drempelvrij / overdekte entree / toegankelijk parkeren / deurkruk / woningaanpassing entree* | CLEAN |
| ES | *Entrada accesible / sin escalón / protección contra la intemperie / aparcamiento accesible / manilla de puerta / adaptación de acceso mayores* | CLEAN |
| PT | *Entrada acessível / sem degrau / proteção contra intempéries / estacionamento acessível / maçaneta / adaptação de acesso para idosos* | CLEAN |
| KO | *접근 가능한 입구 / 단차 없는 현관 / 기상 보호 입구 / 접근 가능한 주차 / 레버형 손잡이 / 노인 주택 현관 개조* | CLEAN |
| IT | *Ingresso accessibile / senza gradino / protezione dalle intemperie / parcheggio accessibile / maniglia a leva / adattamento accesso anziani / DM 236/89* | CLEAN |

**Concept boundary warnings:**
- All languages: The ageing-in-place and disability-specific evidence bases often converge on the same provision (zero-step threshold) for different reasons — stumbling prevention (ageing) versus wheelchair access (disability). Both rationales support the specification, but the evidence quality differs. OT clinical evidence for wheelchair users (Co-1/Tier 1) provides the strongest specification basis; ageing-in-place evidence reinforces the population breadth.

---

### `residential-internal-circulation`
**Domain:** Residential hallway and internal corridor clear widths; turning circle at doorways and in hallways; stair design (rise, going, pitch); stair handrail provision (bilateral, continuous, extended); stair nosing luminance contrast; circulation-route grab bar provision; stair as DAR trigger (future lift provision); hallway width as wheelchair passing space.
**Covers items:** R-HAL · R-STA
**Governing compendium concept group:** CG 6 (turning radius) + CG 7 (door width) + CG 3.1 (corridor width)
**Ageing-in-place lens:** Stair modification (handrail retrofitting, nosing marking, lift provision) and hallway width are primary Lifetime Homes and ageing-in-place criteria. *Treppengeländer Barrierefreiheit* (DE), *main courante escalier maintien à domicile* (FR), *手すり取り付け 階段* (JA), *trappegelender boligtilpasning* (NO), *trapräcke bostadsanpassning* (SV) all surface rich evidence. Lifetime Homes criterion 15 (stair potential lift provision) and criterion 11 (turning area at doorways) are directly relevant.

| Language | Native term | Map |
|---|---|---|
| SV | *Korridor fribredd / snusyta vid dörröppning / trappdesign / trappled / ledstång / trapprätcke / bostadsanpassning trappa* | CLEAN |
| NO | *Korridor friareal / snusrom ved døroppning / trappdesign / trappegelender / boligtilpasning trapp / aldersvennlig sirkulasjon* | CLEAN |
| DA | *Korridor fribredde / vendeplads ved døroppning / trappdesign / trappegelænder / boligtilpasning trappe* | CLEAN |
| FI | *Käytävän vapaa leveys / kääntymistila ovella / portaan suunnittelu / portaan kaide / asunnon muutostyöt portaat* | CLEAN |
| FR | *Largeur libre couloir / espace de manœuvre à la porte / conception escalier / main courante / maintien à domicile escalier* | CLEAN |
| DE | *Flurbreite / Bewegungsfläche an Türen / Treppengestaltung / Handlauf / Wohnraumanpassung Treppe / DIN 18040-2* | CLEAN |
| ZH | *走廊净宽 / 门口转弯空间 / 楼梯设计 / 扶手安装 / 住宅改修楼梯 / 适老化改造楼梯* | CLEAN |
| JA | *廊下有効幅員 / 扉前転回空間 / 階段設計 / 手すり設置 (てすりせっち) / 住宅改修階段 / 高齢者階段手すり* | CLEAN |
| NL | *Gangbreedte / manoeuvreerruimte bij deuren / trappenontwerp / trapleuning / woningaanpassing trap / NEN 9120* | CLEAN |
| ES | *Anchura libre pasillo / espacio de maniobra en puerta / diseño escalera / pasamanos / adaptación escalera mayores / CTE SUA* | CLEAN |
| PT | *Largura livre corredor / espaço de manobra na porta / projeto de escada / corrimão / adaptação escada para idosos / NBR 9050* | CLEAN |
| KO | *복도 유효 폭 / 문 앞 회전 공간 / 계단 설계 / 손잡이 설치 / 주택 계단 개조 / 고령자 계단 손잡이* | CLEAN |
| IT | *Larghezza netta corridoio / spazio di manovra alle porte / progettazione scala / corrimano / adattamento scala anziani / DM 236/89* | CLEAN |

**Concept boundary warnings:**
- All languages: Stair handrail evidence from ageing-in-place literature is strong and consistent (bilateral, continuous grip) but less specific about geometry than OT clinical evidence. Use ageing-in-place evidence to confirm broad provision; OT clinical evidence for grip diameter, end configuration, and extension beyond nosing.
- DE: DIN 18040-2 (residential barrier-free design) is the primary standard — covers both hallway widths and stair provisions in a single instrument; retrieve before other DE sources.

---

### `residential-bedroom-living-ot`
**Domain:** OT home modification evidence in residential bedroom, living room, and laundry contexts; hoist and ceiling track provision (bedroom); transfer space at bed; bed height and adjustability; living room seating height variety; reach to controls and sockets in living room and bedroom; laundry appliance height and reach; home modification programme evidence (HAFI, Disabled Facilities Grant, ANAH MaPrimeAdapt, *bostadsanpassningsbidrag*, *boligtilpasningsstøtte*); post-occupancy evaluation of home modifications.
**Covers items:** R-BED · R-LIV · R-LAU
**Routing note:** Evidence for this slug is most efficiently surfaced via `OT-built-environment-interface` (already registered) supplemented by residential-specific and ageing-in-place terms below. When both slugs are available in BPC, retrieve `OT-built-environment-interface` first and use this slug for residential-specific depth where evidence is thin.
**Ageing-in-place lens:** Home modification programme evidence (grants, OT assessment, installation) is the primary evidence vehicle for bedroom and living room provisions in all jurisdictions. Search grant programme evaluations as primary evidence source: *bostadsanpassningsbidrag* (SE), *boligtilpasningsstøtte* (NO), Disabled Facilities Grant (UK), HAFI (CA), *MaPrimeAdapt* (FR), *住宅改修費支給* (JA).

| Language | Native term | Map |
|---|---|---|
| SV | *Sovrum tillgänglighet / taklyft / sänghöjd / transferyta vid säng / bostadsanpassningsbidrag / vardagsrum tillgänglighet* | CLEAN |
| NO | *Soverom tilgjengelighet / taklift / senghøyde / transferareal ved seng / boligtilpasningsstøtte / stue tilgjengelighet* | CLEAN |
| DA | *Soveværelse tilgængelighed / loftslifte / sengehøjde / transferareal ved seng / boligtilpasningsstøtte / stue tilgængelighed* | CLEAN |
| FI | *Makuuhuone esteettömyys / kattonosturi / sängyn korkeus / siirtymätila sängyn vieressä / asunnon muutostyötuki / olohuone esteettömyys* | CLEAN |
| FR | *Chambre accessible / lève-personne plafond / hauteur de lit / espace de transfert lit / MaPrimeAdapt / séjour accessible* | CLEAN |
| DE | *Barrierefreies Schlafzimmer / Deckenlift / Betthöhe / Transferfläche am Bett / Wohnraumanpassung Schlafzimmer / barrierefreies Wohnzimmer* | CLEAN |
| ZH | *无障碍卧室 / 吊顶式升降机 / 床高调节 / 床边转移空间 / 住宅改修卧室 / 无障碍起居室* | CLEAN |
| JA | *バリアフリー寝室 / 天井走行リフト / ベッド高さ調整 / ベッドサイド移乗スペース / 住宅改修費支給 / バリアフリーリビング* | CLEAN |
| NL | *Toegankelijke slaapkamer / plafondlift / bedhoogte / transferruimte bij bed / woningaanpassingsteun / toegankelijke woonkamer* | CLEAN |
| ES | *Dormitorio accesible / grúa de techo / altura de cama / espacio de transferencia cama / adaptación dormitorio mayores / salón accesible* | CLEAN |
| PT | *Quarto acessível / elevador de teto / altura da cama / espaço de transferência cama / adaptação quarto para idosos / sala acessível* | CLEAN |
| KO | *접근 가능한 침실 / 천장 리프트 / 침대 높이 / 침대 옆 이동 공간 / 주택 침실 개조 / 접근 가능한 거실* | CLEAN |
| IT | *Camera da letto accessibile / sollevatore da soffitto / altezza letto / spazio di trasferimento letto / adattamento camera anziani / soggiorno accessibile* | CLEAN |

**Concept boundary warnings:**
- All languages: Ceiling hoist/track evidence (R-BED hoist provision) is primarily from care home and rehabilitation settings, not residential home modification. Residential hoist installation evidence is thinner; derive from care home evidence and flag residential application as extrapolated (Tier 3 derivation).
- All languages: Laundry provisions (R-LAU — appliance height, front-loading, controls) have almost no dedicated accessible design research literature in any language. Evidence is derived from OT energy conservation and upper limb impairment literature. Flag as THIN across all languages; source from AT product guidance and OT clinical resource guides.

---

## Retired Slugs (additions)

*(None at this time — all new entries above are net additions.)*

---

## Citation-Mining Targets (additions)

| Source | Action |
|---|---|
| Keall et al. (2015, Lancet) NZ HIPI RCT | Already listed — confirm grab bar + bathroom evidence captured |
| KDA *Wohnkonzepte für Menschen mit Demenz* | Backward + forward mining for DEM wayfinding + residential slugs |
| HAFI programme evaluation (BC Housing, Canada) | Forward mining for residential entry + threshold slug |
| Lifetime Homes 16 Criteria (Habinteg 2010) | Backward mining for all residential slugs |
| DSDC Dementia Design Audit Tool (Stirling) | Forward mining for cognitive wayfinding + DEM room evidence |
| Mostafa ASPECTSS studies (2014, 2024) | Forward mining for sensory relief space slug |
| *편의시설 설치 기준* (Korean installation standards) | Direct retrieval for all MOB residential slugs; values more granular than ADA |
| KDA / Kuratorium Deutsche Altershilfe publications | Direct retrieval for DEM wayfinding, therapeutic lighting, residential slugs |
