# Synthesis of the terminology wave, session_2026-11-06-base-vocabulary-review

Read-only synthesis of 14 pass records (DA-DK DE-DE EN-VARIANTS ES-ES FI-FI FR-FR IT-IT JA-JP KO-KR NL-NL NO-NO PT-PT SV-SE ZH-CN). **SV-SE was used**: its rerun wrote `pass-record.md` at 09:54 UTC, before these counts were taken. Governing entries: the six "Owner statements 2026-11-06" entries in `references/project-standards.md`, with the sixth (equivalence classes, conflation) applied throughout. No row, commit or pass-folder edit was made. Every count below is dated 2026-11-06 and gives the command that derives it. Run each from the repository root with `T=scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass`, and re-run rather than trust the figure.

## 1. Verdict

The wave shows that the Canadian English register misses the axes most non-English instruments are built on: performance criteria, trigger and use-class switching, defined outcome levels, and drafting layers with equivalent-effect routes. It also shows that the register's object concepts split or merge differently in every pair, and it yields 2 624 distinct verbatim phrases whose quotes verify in saved text. The wave does not establish absence or equivalence. No pair's technical layer was read (DIN 18040, NEN 9120, GB 50763, AS 1428.1, JIS T 9251, DS/ISO 21542, NS 11001, the regional codes). Three passes verified against a transcription rather than the artefact. FOUND rests on a hand-judged, one-form-per-concept sense match over a register whose near-duplicate rows inflate it. The change that most improves the next round is to restructure the register before running it: collapse the criterion statements into concepts, add row kinds for criterion, trigger, level and drafting layer, and make each concept an equivalence class (`equivalents.tsv`) whose forms are judged by sense, occurrence by occurrence.

## 2. Method defects across passes, ranked by what reaches the guidebook

Failure modes (CLAUDE.md section 5): (a) a gate examines nothing; (b) prose contradicts the data; (c) a false attestation passes green. "n" is the number of passes. Where a grep is given, n is the number of pass records that mention the defect: `grep -liE '<pattern>' $T/*/pass-record.md | wc -l`, run 2026-11-06. Without a grep, n is a list counted from reading the records' defect and count sections, and the list is given. Fix order follows the ruling of 2026-11-06 (first entry): do nothing, then rule, then reuse, then delete, then code.

| # | Defect | Mode | Passes (n) | Smallest fix | Class |
|---|---|---|---|---|---|
| 1 | Held-alias presence was measured by substring (`in`), so compounds and other senses read as hits ("greb" in "brugerbegreb", "gang" in "toegang", "käytävä" in "porraskäytävä", 有効幅 inside 有効幅員). Inflection also hid true hits. | c | grep `substring`: DA DE ES FI FR JA NL NO PT SV ZH (11) | **Rule.** A substring count is never reported as attestation and is dropped from the pass-record template. A form is attested only through `observe-term` quote plus `adjudicate-term` sense, which T3's pointer already requires. No code. | protocol |
| 2 | A text match was taken for a sense match. FOUND and FOUND-PARTIAL are hand-set (`PARTIAL` dicts). The 2.2 quantity words are English lemmas, not concepts. There is no field for the carve relation. | c, b | DE EN ES FR IT JA NL NO PT ZH (10, read). Every self-attack names its own sense judgments (grep `sense judg\|mapping is mine`: 13; FR words it as "my judgment") | **Reuse.** Each coverage cell carries a relation drawn from `term_aliases.alias_type`'s own CHECK (SYNONYM / NARROWER / BROADER, via `dbcore.check_values`), plus a note. Replace bare 2.2 words with sense-qualified concepts (section 3c). | register + protocol |
| 3 | Quotes were verified against our own extraction or transcription. `locate_quote` cannot see into compressed PDFs, HTML entities or XML tags, and no field marks a text as OCR. | a, c | grep `locate_quote\|quote_in_artefacts`: 12 (all but DE NO). Transcription or secondary copy: IT (Normattiva drops a "non", M1), PT (portaria from an aggregator), ZH (OCR of an image-only PDF; 把手 drift) (3) | **Rule:** add a `text_kind` column (extracted / transcribed / OCR-corrected). Require a second witness where two texts exist (IT M1) and a character diff against raw OCR (ZH M2). Under the fifth ruling, extracted text is not committed, so a raw-byte check of a compressed PDF stays impossible by design; record the extraction's sha256. **Smallest code:** `html.unescape` before matching in `locate_quote`, which fixes the IT and DA entity misses. | protocol + tooling (own PR, rule 10) |
| 4 | Near-duplicate register rows (three slip-surface statements, two lighting, two level-landing, two contrast-strip) share observations and inflate FOUND. | b | grep `near-duplicate\|not atomic\|criterion-shaped`: DE EN FR IT JA KO NL NO ZH (9) | **Delete the cause.** Collapse catalogue 2.1's 32 statements into concepts before seeding. No code. | register |
| 5 | The FOUND/ABSENT test was one form per concept. Every equivalent form beyond the first went unrecorded, and a held alias absent from the text was reported as an error. The sixth entry says such a form is "not attested by these texts". | b | all 14 by construction: `ls $T/*/equivalents.tsv 2>/dev/null \| wc -l` gives 0. The alias-wrong framing occurs in grep `word-for-word\|word for word`: ES FI FR IT KO SV ZH (7) | **Rule (already in BRIEF.md).** Equivalence-class discovery is a standing step for every concept. Each form is judged per occurrence by the sense its source gives it. Where a source conflates two concepts, record a conflation note with its locator and do not settle it by fiat (sixth entry, item 5). No code. | protocol |
| 6 | "Absent" covers only what was read, but the status column carries no read layer. Guidance and advice tiers count as FOUND. A paywalled principal layer makes ABSENT meaningless. | b | Paywalled or blocked principal layer: DA DE EN JA NL ZH (6). Advice counted: grep `allmänt råd\|Guidance is counted\|Advice counted`: FI NO SV (3). | **Reuse** NOT-OBTAINABLE and NOT-READ at layer level. **Rule:** each cell names its instrument and tier (binding / deemed-to-satisfy / advice). | protocol |
| 7 | HTTP 200 returned a JavaScript shell (Retsinformation, Incapsula, Finlex HTML, law.go.kr iframe, DR, rinfo listing). | a | grep `shell`: DA EN FI KO PT SV (6) | **Rule:** check extracted length before any reading (DA D2 already did). No code. | protocol |
| 8 | A pass record's counts drift from its own TSVs. EN states 62/11/9 and 257 phrases; `cut -f3 $T/EN-VARIANTS/coverage.tsv \| sort \| uniq -c` gives 63/12/7, and `awk -F'\t' 'NR>1{print $2}' $T/EN-VARIANTS/observations.tsv \| sort -u \| wc -l` gives 258. JA uses status values outside the brief's set ("FOUND (shared with C16)", "grep-located"). | b | EN, JA (2; found here) | **Rule 7a:** a record gives the command, and the status vocabulary is the brief's five values only. | protocol |
| 9 | Priors were written after the call (R14). | b | grep `after the (fact\|run\|results\|calls)`: DA ES KO NO SV (5) | **Convention:** the prior line is appended to `search-log.md` by the same shell command, before `fetch()`. No code. | protocol |
| 10 | Orthographic, spacing and extraction variants: soft hyphens (DE), ruby (JA), 蹴上げ/けあげ (JA), spacing (KO), pdftotext hyphen joins (ES), flattened cells (KO, NL). | c | grep `variant\|spacing varies\|inflection`: DE EN FI JA KO SV ZH (7) | **Rule:** quote the printed form. Record each variant as a form in `equivalents.tsv` (usage type: regional variant / orthographic). No folding code. | protocol |
| 11 | Register size differs: 60 concepts (DE FR IT JA), 75 (nine passes), 82 (EN). | b | ES IT NO note it (3); `wc -l $T/*/coverage.tsv` | **Rule:** compare only on `register_source`; the next round adds the 15 B651 rows to DE FR IT JA. | protocol |
| 12 | The instrument list could not be derived from the base: 0 `research_code_leads` for most pairs. | — | grep `not derivable\|could not be derived\|base gave nothing\|partly derivable`: EN ES FI FR KO NL PT SV ZH (9), plus DA D1 and IT by reading (11) | **Reuse:** record each pair's list as `research_code_leads` rows in the research PR. No code. | research rows |
| 13 | `references/standards-registry.md` is stale (FR links the 2014 text; GB 55019 is missing; NEN 9120 URL gives 404; SE entries contradict; FI "F1"). | b | grep `standards-registry`: FI FR JA KO SV ZH (6); NL D2 and PT D1 by reading (8) | **Prose fix** in the research PR, sweeping prose callers (rule 7a). | prose |
| 14 | Sub-national layers have no slot in the cell key (DE Länder via BayTB, ES autonomous communities, IT regions, "UK" = England). | b | DE EN ES IT (4) | **Rule after owner ruling** (decision 3): the cell key carries the adopting instrument. | register |
| 15 | No Wayback or mirror provenance field (DE D8, FR D5); FI's guide came from a municipal mirror (D5). | — | DE FR FI (3) | **Do nothing:** the manifest URL already shows `web.archive.org`. Name the mirror in `instruments.tsv`. | none |
| 16 | Held aliases carry NULL or narrow jurisdiction tags. | — | grep: EN FI PT SV (4) | **Do nothing.** Under the sixth entry this is not a defect of the form, and `add-alias` reads jurisdiction from the source at attestation. | none |
| 17 | Currency cannot be closed when the portal blocks (Lovdata 405, Finlex `fin@` trap, PGDL lag, rinfo shells). | b | FI NO PT SV (4) | **Do nothing** beyond recording the expression date (R4). | none |
| 18 | A 60 MB PDF was stored under `retrieval-log/` (JA 7). | — | JA (1) | **Settled** by the fifth ruling: keep the manifest line, do not commit the file. | none |

Only #3's `html.unescape` is code. Everything else is a rule in `BRIEF.md`, a register edit, or research rows.

**Standing protocol additions, all protocol changes with no code.** (i) Run equivalence-class discovery for every concept: every form, its usage type (code term / colloquial / regional variant / outdated or disfavoured / product name) and its attestation (instrument phrase with locator / other source with URL and locator / owner-supplied / unattested seed). (ii) Equivalence is not identity. Judge each occurrence by the sense its source gives it; where a source conflates two concepts, write a conflation note with the locator. (iii) Keep disfavoured forms with a usage note.

## 3. Register changes the carves demand

Every phrase below is copied from the named pair's `observations.tsv` or `reverse-harvest.tsv`. Each was checked with `cat $T/<P>/observations.tsv $T/<P>/reverse-harvest.tsv | grep -cF '<phrase>'` (≥1 on 2026-11-06). "(in quote)" marks a phrase found only inside a context quote. Glosses are ours.

**(a) New concepts for the register (12)**
| Concept (instrument's phrase, E1) | Pair |
|---|---|
| ostomy toilet: オストメイト用設備を有する便房 (the statute hides it in a 水洗器具 clause) | JA |
| stepped ramp: Escadarias em rampa | PT |
| visitability, a graded outcome: visitabilità, visitabilità condizionata | IT |
| cognitive-accessibility frame: DALCO; Control de los estímulos sensoriales; Lectura fácil / Lenguaje claro / Lenguaje sencillo; Validación | ES |
| permitted pinch point: Estrechamientos puntuales | ES |
| climate in the geometry: katettu, sulanapidetty, kinostumiselta | FI |
| hazard field versus attention field: farefelt, oppmerksomhetsfelt | NO |
| touch contrast: tuntokontrasti | FI |
| WC handedness: kätisyys | FI |
| information and communication facilities as a class: 无障碍信息交流设施; maintenance duty: 维护责任人 | ZH |
| use after a fall: 跌倒在地面; function dispersal across cubicles: 機能分散 | ZH, JA |
| staffing as a compliance state: visitabilità condizionata (IT), 상시보조서비스 (KO), 案内所 (JA); infant and nursing rooms: 수유실, 기저귀교환대 (KO) | IT KO JA |

**(b) New kinds of row (4)**
| Kind | Phrases (pair) |
|---|---|
| Performance criterion | Wahrnehmbarkeit, Zwei-Sinne-Prinzip, "auffindbar, zugänglich und nutzbar" (DE); tillgänglig och användbar (SV) |
| Trigger / zone / use-class switch | toegankelijkheidssector, gebruiksfunctie, aansturingsartikel (NL); 特別特定建築物 (JA); 바닥면적의 합계, 기존시설 (KO); uso restringido (ES) |
| Defined outcome level | accessibilità / visitabilità / adattabilità (IT); Universell utforming / Tilgjengelig boenhet (NO); varustettava vs varustettavissa (FI); 誘導基準 (JA); adaptabilité, logements évolutifs, réversibilité (FR) |
| Drafting layer and compliance route | Usages attendus / Caractéristiques minimales, effet équivalent (FR); soluzioni tecniche conformi, soluzioni alternative, adeguamento (IT); funksjonskrav / preakseptert ytelse (NO); Bestemmelsen anses som opfyldt, dispensation (DA); gelijkwaardige maatregel, maatwerkvoorschrift, rechtens verkregen niveau (NL); ajustes razonables (ES); 권장사항, 적용의 완화 (KO); 替代性措施, 既有建筑改造或改建 (ZH); Deemed-to-Satisfy (AU), Acceptable Solution (NZ), Functional Intent (SG), Equivalent Facilitation (US) |

**(c) Sense splits of existing concepts (7)**
| Concept | Split, with phrases (pair) |
|---|---|
| ramp | Schrägrampen vs "Rampe gemäß DIN 18040-1" (DE); plan incliné vs rampe amovible (FR); Vados peatonales vs ramps defined by slope thresholds ("exceda del 4%" in DB-SUA, "superior al 6%" in TMA) (ES); 轮椅坡道 vs 缘石坡道 (ZH); rampa vs "rampa di scale" (IT); US "Ramp. A walking surface that has a running slope steeper than 1:20." (106.5) |
| unit of limit for a ramp run (rise vs run) | 高さ七十五センチメートル以内ごとに (JA); 높이 0.75미터 이내마다 (KO); 提升高度 (ZH); luiskan korkeusero (FI); for hver 1,0 m høydeforskjell (NO); hoogte van niet meer dan 1 m (NL); 0,60 m stigning (DA); projecção horizontal (PT). Parameter 12 assumes run. |
| level | Level (UK 0.26 definition), predominantly level (UK 3.14 d); dénivellation, écart de niveau (FR); trinnfri (NO); hoogteverschil groter dan 0,02 m (NL) |
| washroom / lavatory | separate-sex toilet washrooms, lavatory accommodation (UK); accessible individual washroom (SG); sanitary compartment (AU); toilet room, "Lavatories and Sinks" 606 (US); restrooms only in 28 CFR 35.151 (US); 便所 vs 便房 (JA); 无障碍厕位 vs 无障碍厕所 (ZH) |
| tread / going | going, going of each step (UK); largeur du giron (FR); 디딤판 (KO); profundidade (cobertor) vs Comprimento (cobertor) (PT); etenemä (FI); grund (DA) |
| corridor | circulations intérieures horizontales (FR); gemeenschappelijke verkeersruimte (NL); kulkuväylä (FI); kommunikationsutrymme (SV); 복도 및 통로 (KO); gangatkomst vs Kommunikasjonsvei (NO); 通行净宽 with no 走廊 (ZH) |
| door width, turning, contrast | largeur nominale vs largeur de passage utile (FR); "reducida por el grosor de la hoja" (ES); öppningsmåttet för fri passage, vändmåttet av en cirkel (SV); Bewegungsfläche, Unterfahrbarkeit (DE); "inversione di marcia" (IT); 활동공간 (KO); luminanskontrast (NO); tummuuskontrasti (FI); 色の明度、色相又は彩度の差 (JA); reflectância (PT) |

**(d) Register names no instrument read uses (4)** — reported as "not attested by these texts", not as wrong. A statute, a signage manual, municipal or advocacy guidance, or the paid technical layer could attest them. "Turning circle" as a circle: KO square 활동공간, DE Bewegungsfläche, IT spazi di manovra. "LRV contrast" (parameter 8): fits UK and IE only, per EN carve 9. "Truncated domes": NO names fields, not domes. "Ramp run length" (parameter 12): see (c). Separately, seeds that point at the wrong object: 水栓 for the ostomy fixture (JA), "maçaneta tipo alavanca" for PT, where "puxadores em forma de maçaneta" are prohibited, "stigning" as ramp gradient (DA), and the "accessibility" seed "tilgængelighed", which misses the chapter titled Adgangsforhold (DA). These are seed defects, not alias defects.

**(e) Equivalences (5 worked classes + conflations)**

*Parking.* Instrument terms carry a locator; owner-supplied forms are seeds until a source attests them (sixth entry, item 4). Held aliases are from `select alias,alias_type,language,jurisdiction from term_aliases where lower(alias) like '%park%'`.
| Form | Source | Attestation |
|---|---|---|
| accessible parking stall, barrier free parking, accessibility parking | owner | owner-supplied |
| handicapped parking | owner; held en/US DEPRECATED | owner-supplied; not attested by the ADA text read (EN D5); disfavoured, kept with a usage note |
| disabled parking | owner; held en/UK SYNONYM | not attested by these texts |
| designated accessible spaces | RHFAC 1.1.1–1.1.3 (`rhfac-criteria.tsv`) | rating-instrument term (CA) |
| Designated accessible parking | CSA/ASC B651:23 9.4 (`b651-headings.tsv`) | code heading (CA) |
| parking bay designated for disabled people | EN-UK ADM 1.18 a | code term |
| accessible vehicle parking lots | EN-SG 3.3.1.1 | code term |
| van accessible | EN-US 502.6 | code term (narrower class) |
| parkeringsplasser for forflytningshemmede | NO § 8-8 (1) | code term |
| parkeringsplatser för rörelsehindrade med särskilt tillstånd | SV HIN 17 § (binding sentence) | keyed to a permit. [CORRECTION 2026-11-06: this row first read "HIN 12 § (allmänt råd) … advice-tier term"; the Swedish equivalents pass found the form in the binding sentence of 17 §, not in advice text] |
| et passende antal parkeringspladser; handicapegnede køretøjer | DA § 401 stk. 1 | code term; keyed to the vehicle |
| Plazas de aparcamiento reservadas para personas con movilidad reducida; una plaza accesible por cada 33 plazas | ES TMA anexo art. 35; SUA 9 1.2.3.2 b) | code terms (two orders, two forms) |
| lugares especialmente destinados a pessoas em cadeiras de rodas; número de lugares reservados | PT Anexo 3.6.1; 2.8.1 | code terms |
| speciale contrassegno | IT DPR 503 art. 12 c. 1 | code term (permit) |
| autopaikan … liikkumisesteisen henkilön tunnuksella | FI 241/2017 2 § mom. 3 | code term (by symbol) |
| 車椅子使用者用駐車施設; 優先駐車区画 | JA 政令379 Art.18(1); design standard p.52 (grep-located) | code term; guidance term |
| 장애인전용주차구역 | KO R1 제4호 | code term |
| 无障碍机动车停车位 (in quote) | ZH 2.9.5, 2.9 heading | code term |
| DE, FR, NL | — | [GAP]: no parking phrase in these TSVs |

Carve under a barrier-free umbrella, observed in these rows only. Where the code's umbrella word is not "accessible", its parking form usually names a user group, a permit or a vehicle rather than the umbrella word: DE umbrella "barrierefrei erreichbar" (BayBO Art. 48 Abs. 1) with no parking form; FI esteettömän but liikkumisesteisen; KO 장애물 없는 생활환경 인증 but 장애인전용; JA 移動等円滑化 but 車椅子使用者用; NO Universell utforming but forflytningshemmede; SV tillgänglig och användbar but rörelsehindrade. ZH is the exception: 无障碍 prefixes both.

*Qualifier class* (the adjective in "… parking / washroom / entrance"). Owner-supplied: accessible, barrier free, inclusive, universal, wheelchair friendly (no TSV row for "wheelchair friendly"). Instrument forms: Accessible route (NZ Definitions); "Wheelchair accessible unisex WC" (IE 1.4.5); "unisex wheelchairaccessible toilet" (UK 3.14 h); Universal Design (IE 0.1); "barrier-free" (SG 2.4.3, in quote); carte "mobilité inclusion" (FR art. 3, I); cheminement accessible (FR art. 2, I); barrierefrei erreichbar (DE BayBO Art. 48 Abs. 1); esteettömän kulkuväylän (FI 2 § mom. 1); Adgangsforhold (DA kap. 2) versus "offentligt tilgængelige bygninger" (DA § 214, where tilgængelig means open to the public) and universelt design (DA brugerbegreb 2.0.0); accessibilità / visitabilità / adattabilità (IT art. 2 G–I); integraal toegankelijke toiletruimte (NL 4.187 lid 2); Universell utforming / tilgjengelig (NO ch. 12); tillgänglig och användbar (SV 1 kap. 5 §); itinerario accesible (ES anejo A); símbolo internacional de acessibilidade (PT art. 1.º, 3); 移動等円滑化 (JA Art.2(1)(2)) and 心のバリアフリー (JA pdf p.5); 편의시설 (KO 제2조 제2호); 无障碍通行设施 (ZH 1.0.3(4)). FR "PMR" and ES "accesibilidad universal" are not in these TSVs (`grep -c PMR $T/FR-FR/*.tsv` gives 0). **Scope flag:** "wheelchair friendly" (also "wheelchair accessible") is NARROWER than accessible. "Universal" and "inclusive" are wider outside this project; here they always mean inclusion of persons with disabilities (CLAUDE.md section 9). NO "universell utforming" and IT "visitabilità" are defined levels, not synonyms (group b). The owner's reading is an unratified [ASSUMPTION] in the sixth entry.

*Lift / elevator.* The owner supplied "an elevator is a lift". Elevators (US 407.1) and Limited-Use/Limited-Application Elevators (US 408), but Platform Lifts (US 410); passenger lift (UK 3.17; AU Sch 1 E3.6); Passenger Lifts (SG 4.8); platform lift (IE 1.1.3); personhiss (SV 2 kap. 5 §); hoistway (US 407.2.3); "liftway" occurs only in our gloss, not as an instrument phrase. Sense split: in RHFAC (3.5 Elevators, 3.8 Platform Lifts) and B651 (5.6.1 Elevators, 5.6.2 Platform lifts), "lift" names the narrower platform device in CA and the US, while in the UK, AU, SG and IE it is the ordinary passenger lift. Equivalent only in the UK sense.

*Other within-language classes from the TSVs:* kerb ramp (NZ, AU, SG), dropped kerb (UK), Curb Ramp (US); maneuvering (US) and manoeuvring (UK, AU, NZ, SG); faucet (US) and tap; Detectable warnings (US) and tactile ground surface indicators (AU, SG); International Symbol of Access (UK, AU, SG) and International Symbol of Accessibility (US); meseta (DB-SUA) and rellano (TMA), one object in two Spanish orders; balansstöd as the class, ledstång one form (SV). Across jurisdictions of one language: DE/AT/CH, FR/BE/CH/CA and PT/BR are **[GAP]**, because no AT, CH, BE, CA (FR) or BR instrument was read. The only cross-border evidence is NL Bbl "hoogteverschil" against the Flemish "niveauverschil" behind TERM-090 (NL record), and the BR-tagged held seed "maçaneta tipo alavanca" (PT record).

*Conflations* (one form, several concepts; record a conflation note, never settle by fiat).
| Form | Concepts it is used for | Evidence |
|---|---|---|
| lift | passenger lift vs platform lift | US 410 vs UK 3.17 (above) |
| lavatory | washbasin vs toilet room | US 606 "Lavatories and Sinks" vs UK 4.14 "lavatory accommodation", 4.8 "lavatories" |
| washroom | multi-WC room vs single accessible room | UK 5.5 "separate-sex toilet washrooms" vs SG 5.1.1 "accessible individual washroom" |
| going | tread depth vs ramp flight length | UK 1.33 m "going of each step" vs 1.26 b "going" |
| kerb / curb | street edge vs ramp upstand vs shower lip | UK 1.26 m "kerb on the open side of any ramp", US 405.9.2 "Curb or Barrier", NZ/AU/SG "kerb ramp" |
| stigning | riser height vs ramp rise | DA § 57 nr. 2 "stigning (lodrette højde på trinnet)" vs § 56 nr. 4 "vandret repos for hver 0,60 m stigning" |
| rampa | ramp vs stair flight | IT "rampa di scale" |
| 손잡이 / 扶手 / corrimano | handrail vs grab bar vs door handle | KO 제7호 다목 (2), 수평손잡이 제8호 라목 (2); ZH 2.5.4(2) and 2.8.1; IT 4.1.10 and "maniglioni e corrimano" 8.1.6 |
| tilgængelig | accessible vs open to the public | DA § 214 |
| accessible / universal / inclusive / barrier-free / wheelchair-friendly | five scopes used as one | qualifier class above |

Group totals: (a) 12, (b) 4, (c) 7, (d) 4, (e) 5 worked classes and 10 conflations.

## 4. Coverage reality

Status counts: `cut -f3 $T/<P>/coverage.tsv | sort | uniq -c` (JA and ZH: `cut -f4`; the JA "FOUND (…)" variants are summed into FOUND). Reverse harvest: `tail -n +2 $T/<P>/reverse-harvest.tsv | wc -l`. Register size: `tail -n +2 $T/<P>/coverage.tsv | wc -l`. Pilots used 60 concepts, the later passes 75, and EN 82. **Absent means absent from what was read**, nothing more.

| Pair | Reg. | Read in full | Not obtainable | F / FP / ABS | RH | Largest unread layer |
|---|---|---|---|---|---|---|
| DA-DK | 75 | BR18 nine chapters, 3 vejledninger | DS Håndbog 186, DS/ISO 21542 | 38/14/23 | 69 | DS Håndbog 186; BR18 kap. 4 and 14 |
| DE-DE | 60 | ASR V3a.2, BayBO Art. 48, BayTB A 4, BGG § 4 | DIN 18040-1/-2 bodies | 53/0/7 | 90 | DIN 18040; other Länder |
| EN | 82 | UK ADM V2, SG Code 2025, AU Premises Std, NZ D1/AS1 | AS 1428.1 | 63/12/7 | 167 | AS 1428.1; US ch. 2, 8, 10; IE image-only lists; AD K/T |
| ES-ES | 75 | DB-SUA, RD 505/2007, TMA/851/2021 | none attempted (UNE) | 56/12/7 | 90 | autonomous-community codes |
| FI-FI | 75 | 241/2017, 1007/2017, YM guide 2018 | none attempted | 38/19/18 | 69 | 796/2017 (sound); RT cards |
| FR-FR | 60 | Arrêtés 20 avril 2017, 24 déc. 2015 | none attempted (AFNOR) | 50/6/4 | 100 | existing-ERP arrêté 2014; voirie |
| IT-IT | 60 | DM 236/1989, DPR 503/1996 (text only) | none attempted (UNI 11532-2) | 39/15/6 | 85 | regional laws; 7 graphic parts |
| JA-JP | 60 | 政令379, 省令114 | JIS T 9251, JIS Z 8210 | 58/0/2 | 53 | MLIT 建築設計標準 (about 40 of 260 pp read) |
| KO-KR | 75 | Rule 별표 1, Decree 별표 2 | none attempted | 45/16/14 | 106 | 장애물 없는 생활환경 인증 criteria; KS |
| NL-NL | 75 | Bbl accessibility parts | NEN 9120:2025 (geo-block, DRM) | 27/26/22 | 48 | NEN 9120; Regeling |
| NO-NO | 75 | TEK17 §1-3, ch. 8, 12 + DiBK guidance | FOR-2026-06-12-1085; NS 11001 not tried | 48/18/9 | 87 | NS 11001-1/-2; amendment 2026 |
| PT-PT | 75 | DL 163/2006 consolidated | none attempted | 50/13/12 | 85 | official Portaria 301/2019; DL 95/2019 |
| SV-SE | 75 | BFS 2024:12, 2024:9, 2024:13, HIN | none attempted | 40/20/15 | 100 | BFS 2024:10 (noise); ALM 2 |
| ZH-CN | 75 | GB 55019-2021 (OCR), 2023 law | GB 50763-2012 (egress) | 47/17/11 | 95 | GB 50763-2012; GB 50096 |

## 5. What may be promoted to the base, and how

Computed on 2026-11-06 by the appendix script, case-folded and NFC-normalised, matched per language against `term_aliases`:

| Class | Count |
|---|---|
| Distinct (language, phrase) candidates in observations ∪ reverse harvest | **2 624** (2 617 case-folded) |
| Would attest an existing held alias in place (exact match; T3 pointer) | **65** (50 observations + 15 reverse harvest) |
| Observed under an active-parameter concept, no held alias (new alias on a held term) | **206** |
| Observed under a register concept that is not yet a term (needs the concept's term first) | **1 129** |
| Reverse-harvest phrases with no English term, named by their own phrase (E1, NAMES-NEW) | **1 224** |

The 65 includes sense-unchecked hits (defect 1). "banco" (PT) and "Synlig kontrast" (NO) need the sense judged before any pointer is attached.

**Equivalence-class view.** Per pass, register concepts with at least one form: 820. Concepts with two or more distinct forms in one language and jurisdiction: 538 (appendix). Splitting EN by jurisdiction and pooling labels gives 1 002 concept × jurisdiction cells, 545 of them with two or more forms. The pooled figure is an approximation, because DE prefixes its labels ("2.1 …") and JA and ZH use ids. On the one-phrase view, a cell counts once as FOUND. On the class view, the same evidence already gives 538 multi-form classes, before any non-instrument source has been read.

**Route and order.** `observe-term` (verbatim, locator, quote) → `adjudicate-term` (NAMES-EXISTING with relation, or NAMES-NEW) → `add-alias` (attaches the observation pointer to a held alias, T3) or `add-term --from-observation`. All of this runs in a research PR after the T1–T4 tooling PR merges (rule 10). Order: (1) the 65 in-place attestations, sense-checked; (2) the 206 parameter aliases; (3) collapse the register (section 3), then the 1 129; (4) the 1 224 NAMES-NEW, one instrument at a time. **Review unit: one instrument per review**, its observations and reverse harvest together, so that sense and carve are judged against one text. **Every quote must re-verify at write time.** ZH (OCR of an image-only PDF), IT (Normattiva transcription, with a known dropped "non") and PT (Portaria 301/2019 from an aggregator) verified against a transcription or extracted text, not the artefact's bytes. Their rows carry `text_kind`, and IT rows wait for a second witness.

## 6. Decisions for the owner

1. **Which pairs run next?** Recommended: FR/BE, NL/BE, FR/CH, DE/CH, IT/CH, FR/CA and EN/IE proper, the pairs where the same language already has a reading, so the equivalence view across jurisdictions gets data. Then the ES, IT and DE regional codes, then ZH/SG and the Taiwan form. Recommended path: the [GAP] in 3(e) closes first. Alternative, regional codes first: absence gets closer to true in three pairs, but there is no cross-border equivalence data yet.
2. **Obtain the paid or blocked standards (DIN 18040, NEN 9120, GB 50763, AS 1428.1, JIS T 9251, DS/ISO 21542, NS 11001, UNI 11532-2, UNE 41500)?** Recommended: yes, through the owner or a library route, holding manifest lines only (fifth ruling). Yes: ABSENT becomes meaningful for 9 pairs. No: every ABSENT in those pairs stays "absent from the regulation layer".
3. **Restructure the register before the next round?** Recommended: yes. Collapse the 32 statements, add the 4 row kinds, the sense splits and equivalence classes, and the adopting-instrument key. Yes: one edit, and the counts become comparable. No: the next round reproduces defects 2, 4, 5, 11 and 14 in every pair.
4. **Add the `equivalents.tsv` step to the 13 finished pairs** (as a second reading of the same texts plus non-instrument sources)? Recommended: yes, in the same session as decision 3. Yes: it uses texts already in hand, at low cost. No: the finished pairs stay one-form-per-concept, and their FOUND is not comparable with new pairs.
5. **Which sources attest colloquial forms per jurisdiction?** Recommended: statutes, then road-sign and signage manuals, then municipal guidance, then disabled people's organisations' guides (Co-1), each admitted as a source. Alternative: ordinary public usage, such as a news corpus. That gives wider forms but weaker provenance, and it needs a rule on what counts as attestation.
6. **Sub-national instruments:** key cells by adopting instrument (Land, comunidad autónoma, regione, UK nation)? Recommended: yes. Yes: DE, ES, IT and UK coverage becomes honest. No: "DE" stays one cell and hides 16 Länder.
7. **Licensing of retrieved PDFs:** settled by the fourth and fifth 2026-11-06 rulings (the project may hold them, and for large files keeps the URL and sha256 only). Open: may the book render or quote a standard's text? Recommended: quote only short verbatim phrases with a locator, as the observations do. The alternative, no quotation, leaves the reverse harvest unrenderable.
8. **The qualifier reading** (sixth entry [ASSUMPTION]: "wheelchair friendly" is narrower; "universal" and "inclusive" mean disabled people's inclusion here). Recommended: confirm. If you correct it, the qualifier class in 3(e) is regrouped.

## 7. Self-attack

1. **Defect counts measure mentions.** A grep hit is a record that names the defect, not one that suffered it (the Wayback pattern hits successes too). Detect: read the matched lines with `grep -niE '<pattern>' $T/*/pass-record.md`.
2. **The 65 / 206 / 1 129 / 1 224 split rests on exact-string matching** across inflecting and agglutinating languages (defect 1 in reverse), and on DE concepts mapped to "parameter" through DA's labels. Detect: re-run the appendix script with lemma-aware matching for FI, SV and DE and compare.
3. **Group (a) to (e) items may be one pass's sense judgment presented as an instrument fact.** Detect: for each phrase, read its context quote and note in the TSV. A note saying "PARTIAL" or "my reading" demotes it.
4. **SV-SE is a rerun of a cut-off attempt** whose priors were written after results (SV D6), and other passes may also have been regenerated after their records were written (as EN was). Detect: compare each record's stated counts with the commands in section 4.
5. **Locators in 3(e) are copied from TSV locator fields**, which several passes assigned by hand (DA, ES, FR, KO self-attack 4). Detect: grep each phrase in the pair's `text/` file and read the surrounding article number.

## Appendix: derivation script (read-only; run from the repository root with `python3 -I`)

```python
import csv,os,sqlite3,unicodedata as u
from collections import Counter,defaultdict
T='scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass'
R=lambda p:list(csv.reader(open(p,encoding='utf-8'),delimiter='\t'))
N=lambda s:u.normalize('NFC',s).casefold().strip()
db=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True); al=defaultdict(set)
for a,l in db.execute('select alias,language from term_aliases where alias is not null and language is not null'): al[l.lower()[:2]].add(N(a))
P={r[0] for r in R(f'{T}/DA-DK/coverage.tsv')[1:] if r[1]=='base_parameters'}
c=Counter(); eq=Counter()
for p in sorted(d for d in os.listdir(T) if os.path.isfile(f'{T}/{d}/pass-record.md')):
    L='en' if p.startswith('EN') else p[:2].lower(); cv=R(f'{T}/{p}/coverage.tsv'); h=cv[0]
    s=[i for i,x in enumerate(h) if 'source' in x]; src={r[0]:(r[s[0]] if s else ('base_parameters' if r[0] in P else '')) for r in cv[1:]}
    o=R(f'{T}/{p}/observations.tsv'); oh=o[0]; pi=next(i for i,x in enumerate(oh) if x.startswith('phrase'))
    ci=next(i for i,x in enumerate(oh) if x.startswith('concept_id')) if any(x.startswith('concept_id') for x in oh) else next(i for i,x in enumerate(oh) if x.startswith('concept'))
    obs=defaultdict(set); fc=defaultdict(set)
    for r in o[1:]:
        for k in r[ci].split('|'): obs[r[pi].strip()].add('param' in src.get(k.strip(),'')); fc[k.strip()].add(r[pi].strip())
    for ph,f in obs.items(): c['held' if N(ph) in al[L] else ('param' if True in f else 'register')]+=1
    rh=R(f'{T}/{p}/reverse-harvest.tsv'); ri=next(i for i,x in enumerate(rh[0]) if x.startswith('phrase'))
    for ph in {r[ri].strip() for r in rh[1:]}-set(obs): c['rh-held' if N(ph) in al[L] else 'rh-new']+=1
    eq['concepts with a form']+=len(fc); eq['concepts with >=2 forms']+=sum(len(v)>1 for v in fc.values())
print(dict(c),sum(c.values()),dict(eq))
```
2026-11-06 09:57 UTC output: `{'register': 1129, 'held': 50, 'param': 206, 'rh-new': 1224, 'rh-held': 15} 2624 {'concepts with a form': 820, 'concepts with >=2 forms': 538}`.
