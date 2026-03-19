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