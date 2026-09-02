# AGONIST BRIEF — research batch 05, slug `accessible-circulation-geometry`

**Session:** `session_2026-09-02-research-batch-05-circulation-icf`
**Role:** AGONIST — retrieve, vet, adjudicate. **Zero database writes.** All DB access `mode=ro`.
**Frame:** `scratchpad/session_2026-09-02-research-batch-05-circulation-icf/FRAME.md` (ICF-first, D-0187).
**Executed:** 2026-09-02. **14 searches** across **5 engines** + **1 deliberate non-search**.
**Screened:** ~78 records substantively. **Proposed admissions: 8.**

**Vocabulary confirmed read-only** from the live `search_executions` DDL (no `sqlite3` CLI; Python
`mode=ro`). `target_evidence_type` ∈ `clinical | sr_meta | standard_eb | national_fw | code | co1 |
co2 | grey`. `engine` ∈ `pubmed|crossref|scholar|biorxiv|medrxiv|consensus|web|registry|manual`.
`depth_method` ∈ `scoping|systematic`. `saturation_signal` ∈ `none|partial|saturated`.

**No item code and no item value entered any query.** Every search was framed on a construct
(demand on wheeled movement, joint load under gradient, manoeuvring footprint, crowd flow) and the
numbers were allowed to land where they landed. They landed somewhere the item names would not have
predicted — see §9.1.

---

## ⚠ THREE THINGS TO READ BEFORE USING THIS BRIEF

**1. `retrieval_log.fetch()` CANNOT LOG A PDF, AND THAT IS THE UNDIAGNOSED CAUSE OF D04-032.**
`scripts/research/retrieval_log.py:124` runs `subprocess.run(["curl","-sS",…], text=True)`. On any
binary body it raises `UnicodeDecodeError` **before** the artefact is written — I hit it live on the
Goodwin PDF. It also passes **no `-L`**, so a redirecting URL records a **0-byte artefact** (see
`e3b0c44298fc1c14.txt`, 0 bytes, for `ndownloader.figshare.com`). Consequence: the project's own
anti-fabrication logger is structurally incapable of logging the artefact class that Co-1 and T2
evidence overwhelmingly arrives in — DPO reports, OT guidelines, grey PDFs. Batch 04 saved its PDFs
by hand not out of carelessness but because `fetch()` cannot do it; D04-032's remedy ("use
`fetch()`") does not work for PDFs until this is fixed. **Recommended fix:** capture bytes
(`text=False`), add `-L`, sniff on `bytes` not `str`. Two-line change, and it closes the class.
**My two PDF payloads are therefore outside the manifest**, with sha256 recorded here (§3).

**2. The manifest exists and is populated — 33 lines, 32 artefacts** under
`retrieval-log/session_2026-09-02-research-batch-05-circulation-icf/manifest.jsonl`. Every
bibliographic field below traces to a payload in it. **No field was written from memory.**
`author_fidelity` will find subjects in this session.

**3. R9 hit.** `10.1016/j.apmr.2010.01.009` (Koontz 2010, **admission A1, the strongest source in the
batch**) is **already held as `REF-00784`** — `status='REFERENCE-ONLY'`, `title`/`authors`/`pub_year`/
`tier_claimed` all NULL. **One ref_id only, no duplicate-identity defect.** Do not mint a new
ref_id; upgrade REF-00784. Every other proposed admission is unheld in both `source_locators` (881
rows) and `evidence_sources` (0 rows). I re-confirmed the 32-DOI duplicate corruption is live but
touches none of my candidates.

---

## 1. QUERY LOG (R8 — verbatim, logged before screening, empties kept)

`slug` = `accessible-circulation-geometry` on every row. `depth_method` = `scoping` on every row
(this is a first pass on a slug with zero prior `search_executions`). `saturation_signal` = `none`
on every row — one pass on a zero-evidence slug is not saturation, and §9.3 says why.

| # | engine | tier | evidence_type | query (verbatim) | found | screened | R14 / note |
|---|---|---|---|---|---|---|---|
| 1 | `consensus` | Co-1 | `co1` | `co-produced participatory research with wheelchair users on experiences of building corridors doorways and level changes` | 10 | 10 | Yield: method papers + off-slug community mobility. See §9.2. |
| 2 | `scholar` | Co-1 | `co1` | `What do co-produced and participatory studies led by disabled people report about the experience of moving through building circulation routes — corridors, doorways, thresholds, ramps and vertical circulation?` | 20 passages / 14 unique | 14 | **Index caveat:** Scholar Gateway returned **only Wiley-published** items. That is a publisher-scoped index, not a field index — do not read its silence as absence. |
| 3 | `pubmed` | Co-1 | `co1` | `(photovoice OR participatory OR "co-design" OR "co-produced" OR "lived experience") AND (blind OR "visually impaired" OR "vision impairment" OR deafblind) AND (wayfinding OR navigation OR "built environment" OR indoor)` | 26 | 10 | **EFFECTIVELY EMPTY — KEPT. R14: query-shape failure AND wrong index.** PubMed's own `query_translation` expanded `blind` to `"blinded"[All Fields] OR "blinding"[All Fields]`, i.e. RCT masking, and returned Ethiopian SRH services, gender-affirming care, and a vaccination RCT protocol. **1 of 10 on-topic.** Compounding it: blind-navigation work lives in HCI/architecture venues PubMed does not index. |
| 4 | `web` | T2 | `grey` | `disabled people's organisation report barriers corridors doorways step-free routes inside buildings lived experience survey members` | 9 | 9 | **0 admitted. R14: genuine absence *of this genre*, not of the topic.** DPO output in this territory is about **supply and policy** (waiting lists, 10% wheelchair-home targets, SHMA data gaps), not about the demand a corridor places on a body. Notably the engine answered a DPO query with **academic** sources — Goodwin, Kapsalis. |
| 5 | `web` | Co-2 | `co2` | `"occupational therapy" professional body practice guideline environmental assessment wheelchair access home modification dimensions evidence RCOT WFOT AOTA` | 7 | 7 | **ZERO-YIELD — KEPT.** The engine itself concluded the results "do not specifically address detailed guidelines from RCOT…WFOT…AOTA…or dimensional specifications". |
| 6 | `web` | Co-1/T2 | `co1` | `Euan's Guide Access Survey disabled people venue accessibility findings report toilets steps entrances` | 9 | 9 | 0 admitted. Disability-led (charity SC045492) and a real annual survey, but the 2023 report URL `euansguide.com/files/final-23-euansguide-results-pdf.pdf` **returns HTML, not the PDF** (logged: `72c0fcb12f42614c.html`, 15,580 B). Content is also predominantly information/toilets/staff, not circulation. See §8. |
| 7 | `web` | Co-2 | `co2` | `Royal College of Occupational Therapists practice guideline falls prevention older adults environmental hazards thresholds handrails level changes recommendations` | 8 | 8 | **ZERO-YIELD for the guideline document — KEPT. R14: wrong index.** RCOT practice guidelines are member-gated; the web tier returns commentary about them, never their recommendation text. |
| 8 | `pubmed` | Co-2 | `co2` | `"Occupational Therapy Practice Guidelines"[Title] AND (vision OR "low vision" OR mobility OR "home modification" OR aging)` | 5 | 5 | **0 admitted. R14: GENUINE ABSENCE, and this one is a real finding.** All 5 retrieved and read at abstract level. See §2.1 — the Co-2 negative is structural, not a search artefact. |
| 9 | `pubmed` | T1 | `clinical` | `(wheelchair propulsion) AND (ramp OR slope OR incline OR gradient) AND (shoulder OR kinetics OR kinematics OR "muscle activity" OR "mechanical efficiency")` | **91** | 30 titles, 6 full metadata | Rich literature — the opposite of absence. Yielded A4 and A5. |
| 10 | `consensus` | T1 | `clinical` | `anthropometry of wheeled mobility device users clear floor area and turning space requirements in the built environment` | 9 | 9 | Yielded the Steinfeld/IDeA lineage and King 2011. |
| 11 | `consensus` | T1/T3 | `clinical` | `Bewegungsflächen Rollstuhl barrierefreies Bauen Flurbreite Türbreite Untersuchung` (**German**) | 10 | 10 | **THE HIGHEST-YIELD SEARCH IN THE BATCH.** Produced A1 (Koontz), A7 (Baba, Japanese). **Honesty note:** Consensus is a semantically English-centric index; a German query returned English-language results. The query was non-English; the *index* was not. That is why I ran #13. |
| 12 | `pubmed` | T3 | `clinical` | `(wheelchair OR "mobility scooter" OR "walking aid") AND (injury OR fall OR entrapment OR trauma) AND (door OR elevator OR lift OR threshold OR ramp OR "level change") AND (building OR indoor OR "built environment" OR home)` | 45 | 7 full metadata | **0 admitted. R14: query-shape failure.** MeSH expanded `lift`→`"lifting"[MeSH]`, `fall`→`Accidental Falls`, `trauma`→`Wounds and Injuries`, returning dry-beriberi physiotherapy, a BCI door opener, and SCI fracture epidemiology. **1 of 7 on-topic** (Thies 2023, staged §8). R7 harm is **not** reachable from PubMed by AND-chaining; see §9.3. |
| 13 | `manual` | T3 | `clinical` | `車椅子 廊下 幅員` via **J-STAGE WebAPI** (`api.jstage.jst.go.jp/searchapi/do?service=3`) — **genuine Japanese-language national academic index** | **49** | 20 returned, 12 inspected, 4 resolved | **THE R5 FINDING OF THE BATCH.** 49 Japanese academic papers on wheelchair × corridor × width in one national index. English-language engines surfaced **one** of them. Independently re-found A7 (Baba) as hit #2 — cross-index corroboration. See §9.4. |
| 14 | — | — | — | **DELIBERATE NON-SEARCH** | — | — | See below. |

### Row 14 — the deliberate non-search, with its reason (R6 `deferred_reason`)

**Not searched: vertical circulation (passenger lifts, platform lifts, evacuation lifts) as a
sub-construct.** The slug's scope as written includes "vertical circulation". I did not search it.

**Reason, and it is not that I ran out of budget.** Vertical circulation is the one part of this
slug where the determinative literature is **standards-and-conformity** (EN 81-70, EN 81-41, ISO
21542, ASME A18.1) rather than measured human demand, and the project's own **2026-08-12
REFERENCE-ONLY ruling** means those documents may be named as leads but not mined for values here.
An R1/T1 search on lift geometry would therefore have produced a list of standards I am forbidden to
quote, plus a thin scatter of entrapment case reports — high query cost, near-zero admissible yield,
and a standing risk of smuggling a code value into a research row (**exactly the D04-027 breach**).
**Findings are NOT smuggled into this cell: I make no claim about lift dimensions.** The owed action
is a `research_code_leads` pass on EN 81-70 / EN 81-41 / ASME A18.1, which is a different activity
from an evidence search and should be scoped as one.

---

## 2. SCREENING — what was rejected, and why

**~78 records screened substantively.** The rejections that carry information:

### 2.1 The entire AOTA Practice Guideline series — REJECTED, and the negative is structural

All five hits from search #8 retrieved and read at abstract level (PubMed payload):

| PMID | Guideline | Why rejected |
|---|---|---|
| 38306186 | Adults Living With Alzheimer's Disease and Related NCDs (AJOT 78(1), `10.5014/ajot.2024.078101`) | Recommends *reminiscence, exercise, cognitive therapy, sensory interventions, care-partner education*. Zero environmental-parameter content. |
| 37862268 | Adults With Stroke (AJOT 77(5), `10.5014/ajot.2023.077501`) | *Mirror therapy, task-oriented training, mental imagery, balance training, CBT.* Interventions delivered to a person. |
| 37624997 | Adults With Traumatic Brain Injury (AJOT 77(4), `10.5014/ajot.2023.077401`) | *Multimodal sensory stimulation, virtual reality, vision therapy.* Same shape. |
| 32204790 | Older Adults With Low Vision (AJOT 74(2), `10.5014/ajot.2020.742003`) | The closest candidate — and it recommends *low-vision rehabilitation, stand-based electronic magnification, visual skills training, adapted tango*. **Nothing about the environment the person moves through.** |
| 41923488 | Total Knee Replacement, Korean health system (`10.1155/oti/5583913`) | Out of scope. |

**This is not a search failure; it is a property of the genre.** AOTA Practice Guidelines are
organised around *interventions delivered to a person*, and the built environment appears — when at
all — as an unquantified setting. Batch 04 reached the same conclusion by a different route
(rejecting RCOT 2019, CAOT 2024, AOTA Home Modifications 2014 as "process framing"). **Two
independent search paths, three professional bodies, nine documents, one answer.** I therefore
propose the orchestrator record this as an **evidenced negative** rather than an unsatisfied R1 leg:
*the OT professional-body CPG literature does not carry circulation-geometry content, and further
Co-2 searching on this slug has a low expected yield.* The falsification condition is specific: a
Co-2 document that states an environmental dimension with a locator.

### 2.2 Goodwin et al. 2022 — **screened, ADMITTED, but NOT as Co-1.** The most important rejection in this brief

The paper is titled *"…A lived experience perspective"*. It is published by the Summer Foundation
and La Trobe's Living with Disability Research Centre. Every surface signal says Co-1.

**I read the full text (14 pp., 53,594 chars extracted). The only involvement of disabled people
beyond being respondents is one sentence:**

> *"Prior to distribution, the survey was piloted by three people with mobility impairment to check
> ease of completion."* (§2 Method)

That is **pilot usability testing, not co-production.** There is no advisory group, no
co-researcher, no self-advocacy partner, no statement of author disability, and the recruiting body
is an unnamed "advocacy association". Under
`decisions/DR-2026-08-31-co1-warrant-must-name-the-co-production.md` this **fails the Co-1 test**,
and it fails it in the precise way the DR was written to catch: *a lived-experience-titled paper
whose actual warrant is a survey*. It is `T3 clinical` (tier-system §1: "cross-sectional,
observational, qualitative"), which still maps to **● full band** under §8 — so nothing is lost by
grading it honestly. **Had this been admitted as Co-1 it would have been a repeat of the 2026-08-19
class of failure one field over: a tier asserted from a title rather than tested against the source.**

### 2.3 Kasem et al. 2026 — impeccable Co-1 warrant, **rejected as an admission for THIS slug**

`10.1111/jar.70275`, JARID 39(4):e70275, PMC13320296, CC-BY. Full text retrieved and searched
(132,974 B XML, artefact `addb54778e8bccd4.xml`).

**The warrant is real and I can name it:** author 2 is **Zarah Kaleem, affiliated to Cardiff People
First** — a self-advocacy organisation run by and for people with learning disabilities — and the
abstract states in its own words: *"The article is co-authored by academic researchers and a
co-researcher with lived experience of an intellectual disability."* Also *"collaboration with a
self-advocacy organisation, the involvement of a co-researcher with lived experience"*. The first
author declares dual positionality: *"As a non-disabled researcher, they entered the field as an
outsider… their employment within a local self-advocacy organisation created an insider position."*

**And it contains no circulation findings.** I counted occurrences in the full text: `corridor` **0**,
`signage` **0**, `crowd` **0**, `noise` **0**, `lift` **0**, `escalator` **0**, `seating` **0**,
`distance` **0**, `toilet` **0**. The paper says so itself: *"Rather than focusing solely on barriers
within the built environment, participants consistently highlighted the conditions that made the
research process itself inclusive."* The single built-environment trace is a supplementary figure
caption: *"Figure S3: One of the shopping centre's entrances featuring multiple doors without
labels."*

**Admitting it would be filling the Co-1 slot rather than finding evidence.** Staged with a specific
action (§8, C-1): the *doctoral study* behind it did generate shopping-centre barrier findings —
retrieve the thesis or the companion empirical paper. That is where the Co-1 circulation evidence is.

### 2.4 Other screened-and-rejected

- **Swan, Watchorn & Grant 2020** (`10.1111/ajag.12849`, Australas J Ageing) — *handrails in
  corridors*, exactly on-construct by title. **Rejected: the population is staff and design
  professionals, not disabled people.** A corridor study whose respondents are not the people the
  corridor fails. Verified via Crossref (`216a9f2b6312e3ed.json`).
- **Liebergesell, Vermeersch & Heylighen 2021** (`10.1111/joid.12192`) — *Urban Chandelier: How
  Experiences of Being Vision Impaired Inform Designing for Attentiveness*, J Interior Design
  46(1):73-92. Verified (`12e3cf45af196e3b.json`). Rejected for this batch: single-case design
  interpretation, not a circulation-demand study. Genuine Co-1-adjacent interest — staged §8.
- **van Hoven, Fisher & Munuera Garcia 2024** (`10.1080/15575330.2024.2310848`, Community Development
  55(6):842-857) — co-researchers with acquired brain injury, deafness, chronic neurological
  disorders. Verified via Crossref. **Rejected: method paper, city-scale, not building circulation.**
  Same shape as Kasem.
- **Fredericks, Visagie & van Niekerk 2024** (`10.4102/ajod.v13i0.1253`) — co-operative inquiry, real
  co-production. **Rejected as off-slug** (minibus-taxi and community mobility). Batch 04 reached the
  same disposition; I concur and do not re-litigate.
- **Hashempour et al. 2024** (`10.1002/fam.3209`) — children/adolescents' speed and flow over stairs
  and through exit doorways. Rejected: children studied for adult provision is PROXY at best (R13),
  and the construct is egress timing, not accessible circulation.
- **AJOT PMID 41923488, Biomimetics BCI door opener, dry-beriberi case report, SCI fracture
  epidemiology, wheelchair racing intra-cycle velocity, foot-propulsion seat height, SmartDrive power
  assist, geared wheels** — all off-construct; the last four are device studies where the
  independent variable is the wheelchair, not the building.
- **Ahosseini 2018** *"Maneuvering Area, Corridors and Lobbies for Wheeled Mobility Aid users"* —
  perfectly on-title. **Rejected: "Unknown Journal", no resolvable venue, no DOI surfaced.** An
  unverifiable venue is not admissible; noted as a lead only.

---

## 3. VETTED ADMISSIONS — 8

Every author list below is **byline order, complete, from a retrieved payload**. Where two payloads
render a name differently I say so rather than choosing silently.

---

### A1 · Koontz, Brindle, Kankipati, Feathers & Cooper (2010) — **T1 `clinical`** — the anchor
**⚠ R9: ALREADY HELD as `REF-00784`. Upgrade it; do not mint.**

- **Authors (byline order):** Koontz, Alicia M.; Brindle, Eric D.; Kankipati, Padmaja; Feathers,
  David; Cooper, Rory A. *(n=5; identical in Crossref and PubMed payloads)*
- **Title:** *Design Features That Affect the Maneuverability of Wheelchairs and Scooters*
- **Journal:** Archives of Physical Medicine and Rehabilitation **91(5):759–764** · 2010-05 · ISSN
  0003-9993 · Elsevier
- **DOI:** `10.1016/j.apmr.2010.01.009` · **PMID:** 20434614
- **R9:** `source_locators` **REF-00784**, `status='REFERENCE-ONLY'`, `title`/`authors`/`pub_year`/
  `tier_claimed` all NULL. **Exactly one ref_id — no duplicate-identity defect.** Absent from
  `evidence_sources` (0 rows).
- **Retrieval rung (R10):** DOI → **Crossref reference-resolution, rung 2, 200** (`753c7d7e2af6c6d4.json`)
  → **PubMed metadata, 200** → **Unpaywall: `is_oa: false`, `closed`** (`711b950e88d42b38.json`).
  **Full text NOT obtained.** `doi_resolution_outcome`: `resolved_crossref_pubmed_closed_access`.
- **Payloads:** `retrieval-log/session_2026-09-02-research-batch-05-circulation-icf/753c7d7e2af6c6d4.json`
  (Crossref), `711b950e88d42b38.json` (Unpaywall); PubMed metadata via MCP.
- **Tier test applied — stated, not assumed.** T1 requires *control on the parameter under design*
  (tier-system §1). Koontz **systematically manipulated the parameter itself**: "Passageway openings
  were increased in 5-cm increments until the user could successfully perform each task without
  hitting the walls," across four defined manoeuvres (L-turn, 360° turn in place, U-turn with and
  without a barrier), with a measured binary outcome. That is experimental control on passageway
  width. **The counter-argument, which I state rather than hide:** the paper self-labels its design
  "Case series" with a "sample of convenience," which is the T3 signature. **My ruling: T1**, because
  the tier turns on control over the design parameter, not over sampling — sampling bears on
  generalisability, which is a population-grading question and is graded below. **This dispute is
  immaterial to the marker:** T1 and T3-clinical both map to **● full** under §8. I flag it so the
  adversary can rule without re-deriving it.
- **Why it anchors:** n = **223 actual device users** (MWC 109, PWC 100, scooter 14) — not an expert
  operator, not able-bodied proxies, not a simulation.

### A2 · Dutta, King, Holliday, Gorski & Fernie (2011), part I — **T3 `clinical`**

- **Authors (byline order):** Dutta, Tilak; King, Emily C.; Holliday, Pamela J.; Gorski, Susan M.;
  Fernie, Geoff R. *(n=5; Crossref and PubMed agree)*
- **Title:** *Design of built environments to accommodate mobility scooter users: part I*
- **Journal:** Disability and Rehabilitation: Assistive Technology **6(1):67–76** · 2011 · ISSN
  1748-3107 / 1748-3115 · Informa UK
- **DOI:** `10.3109/17483107.2010.509885` · **PMID:** 20690862
- **R9:** NOT HELD (neither table).
- **Retrieval rung (R10):** DOI → **Crossref reference-resolution, rung 2, 200**
  (`561a06bbacd65f6b.json`) → **PubMed metadata, 200** → **Unpaywall: `is_oa: false`, `closed`**
  (`335163936366acde.json`). Full text NOT obtained.
- **Tier test:** an **expert driver**, not a scooter user, operated five devices through five
  configurations. The *device* is the unit of analysis and the *human* is uncontrolled-for. That is
  lower control on the person → **T3 `clinical`**, not T1. I decline to argue it up.
- **Why it belongs on this slug and not a device slug:** its five configurations are circulation
  geometry — *turning 180° in a corridor*, *U-turns around 50 mm and 1200 mm obstacles*, *turning 90°
  from a doorway*, *approaching a counter from the side*.

### A3 · King, Dutta, Gorski, Holliday & Fernie (2011), part II — **T3 `clinical`**

- **Authors (byline order):** King, Emily C.; Dutta, Tilak; Gorski, Susan M.; Holliday, Pamela J.;
  Fernie, Geoff R. *(n=5; Crossref and PubMed agree; note the byline order differs from part I)*
- **Title:** *Design of built environments to accommodate mobility scooter users: part II*
- **Journal:** Disability and Rehabilitation: Assistive Technology **6(5):432–439** · 2011 · ISSN
  1748-3107 / 1748-3115 · Informa UK
- **DOI:** `10.3109/17483107.2010.549898` · **PMID:** 21657823
- **R9:** NOT HELD.
- **Retrieval rung (R10):** as A2 — Crossref rung 2 (`561a06bbacd65f6b.json`, same query returned
  both parts) → PubMed → Unpaywall `closed` (`0d427d2018b202ed.json`).
- **Tier test:** same expert-driver design → **T3 `clinical`**.

> **⚠ A2 AND A3 ARE ONE RESEARCH PROGRAMME AND ARE NOT INDEPENDENT.** Same lab (Toronto Rehab), same
> five authors, same expert driver, same Styrofoam-wall method, sequential parts of one study.
> **They must not be counted as two converging confirmations.** This bears directly on the
> `convergence-independence` criterion the contract states over the judgment stage. I admit both
> because they answer different questions (corridor/doorway clearance vs. turning-space geometry),
> not because they agree.

### A4 · Marchiori, Gagnon & Pradon (2023) — **T1 `clinical`** — full text read

- **Authors (byline order):** Marchiori, Claire; Gagnon, Dany H.; Pradon, Didier *(n=3; Crossref and
  PubMed agree)*
- **Title:** *Quantification of the Risk of Musculoskeletal Disorders of the Upper Limb Using Fuzzy
  Logic: A Study of Manual Wheelchair Propulsion*
- **Journal:** Sensors **23(21):8659** · 2023-10-24 · ISSN 1424-8220 · MDPI · **CC-BY**
- **DOI:** `10.3390/s23218659` · **PMID:** 37960359 · **PMCID:** PMC10648130
- **R9:** NOT HELD.
- **Retrieval rung (R10):** DOI → **Crossref, 200** (`4062c068e5f7280f.json`) → **Unpaywall: gold,
  four OA locations** (`218fa2e92cca58bc.json`) → **HAL repository PDF, 200, full text read.**
- **Payloads:** Crossref `4062c068e5f7280f.json`, Unpaywall `218fa2e92cca58bc.json`. **Full PDF is
  outside the manifest** (see the `fetch()` defect above):
  `scratchpad/…/agonist/marchiori2023.pdf`, 1,733,995 B,
  **sha256 `61ee4e7a49bc91f1793f4d9c6d1beff6a064be621de0befbe9b725a0760327eb`**, from
  `https://hal.science/hal-04334565/file/sensors-23-08659.pdf`.
- **Tier test:** treadmill gradient systematically set to four levels with randomised order,
  instrumented wheels + 3D motion capture, biomechanical model. Control on the parameter under
  design (gradient), measured joint-load outcome → **T1**.
- **Read status:** **FULL TEXT READ.** Every number in §6 is first-hand from the PDF, not from an
  abstract or a summariser.

### A5 · Arnet, Veeger & de Vries (2025) — **T1 `clinical`** — the ramp-descent finding

- **Authors (byline order):** Arnet, Ursina; Veeger, Dirkjan H. E. J.; de Vries, Wiebe H. K. *(n=3)*
  — **name-rendering variance recorded:** Crossref renders author 2 as `Veeger, Dirkjan (H. E. J.)`,
  PubMed as `Veeger, Dirkjan H E J`. Same person, different punctuation. **Store PubMed's form.**
- **Title:** *Shoulder load during wheelchair-related activities of daily life*
- **Journal:** Journal of Electromyography and Kinesiology **84:103027** (article-number 103027;
  Crossref `page` is null — **do not write 103027 into `pages`**, that is the exact MISMATCH class
  `retrieval_log --verify-authors` flags) · 2025 · ISSN 1050-6411 · Elsevier
- **DOI:** `10.1016/j.jelekin.2025.103027` · **PMID:** 40602232
- **R9:** NOT HELD.
- **Retrieval rung (R10):** DOI → **Crossref, 200** (`125a5b31e7051cbf.json`) → PubMed metadata, 200.
  Full text not obtained (Elsevier).
- **Tier test:** activities systematically varied (speeds, inclines, ramp ascent **and descent**,
  weight-relief lift, material handling, desk work), upper-extremity kinematics and forces measured,
  Delft Shoulder and Elbow Model applied. Control on the parameter → **T1**.
- **⚠ Population:** **ten ABLE-BODIED participants.** Graded PROXY in §5, with the mismatch written.

### A6 · Goodwin, Davis, Winkler, Douglas, Wellecke, D'Cruz, Mulherin & Liddicoat (2022) — **T3 `clinical`** — **NOT Co-1**

- **Authors (byline order):** Goodwin, Isabella; Davis, Elise; Winkler, Di; Douglas, Jacinta;
  Wellecke, Cornelia; D'Cruz, Kate; Mulherin, Peter; Liddicoat, Stephanie *(n=8, Crossref)*.
  **Variance recorded:** the figshare deposit renders author 1 as `I Goodwin` and author 3 as
  `Dianne Winkler`; the published PDF byline reads `Isabella Goodwin` and `Di Winkler`. **Store the
  Crossref/published form.**
- **Title:** *Making homes more accessible for people with mobility impairment: A lived experience
  perspective*
- **Journal:** Australian Journal of Social Issues **57(4):956–969** · 2022-05-02 · ISSN 0157-6321 /
  1839-4655 · Wiley · **CC-BY**
- **DOI:** `10.1002/ajs4.214`
- **R9:** NOT HELD.
- **Retrieval rung (R10):** DOI → **Crossref, 200** (`9229bebb0f21a430.json`) → **publisher
  `onlinelibrary.wiley.com`, 403 Forbidden** → **Unpaywall, 200: hybrid, figshare repository**
  (`2ea166a5a419abd6.json`) → **figshare API, 200** (`9d7a0c26a3d40b41.json`) → **figshare file
  endpoint 302, `fetch()` recorded 0 bytes** (`e3b0c44298fc1c14.txt` — kept as proof of the failed
  rung) → **`curl -L`, 200, full published PDF.** `doi_resolution_outcome`:
  `resolved_crossref_publisher_403_repo_figshare_200`.
- **Payloads:** Crossref `9229bebb0f21a430.json`, Unpaywall `2ea166a5a419abd6.json`, figshare API
  `9d7a0c26a3d40b41.json`, 0-byte failed rung `e3b0c44298fc1c14.txt`. **Full PDF outside the
  manifest:** `scratchpad/…/agonist/goodwin2022.pdf`, 215,057 B,
  **sha256 `ec6f233f1b93156795a5a9a2c97a83a45bbed7d84b77a340e2c0d7872141fb34`**.
- **Tier test:** cross-sectional online survey with descriptive qualitative analysis of free text →
  tier-system §1 T3 ("cross-sectional, observational, qualitative"). **Co-1 tested and FAILED** —
  full reasoning in §2.2. `evidence_type`: `clinical`.
- **Read status:** **FULL TEXT READ** (14 pp.).

### A7 · Baba, Mori, Asaine, Futaduka & Hasegawa (2004) — **T3 `clinical`** — **non-English (R5)**

- **Authors (byline order):** BABA, Akio; MORI, Akiko; ASAINE, Wataru; FUTADUKA, Takeshi; HASEGAWA,
  Naoji *(n=5, Crossref)*
- **Title (verbatim from Crossref, typo and all):** *ACUTUAL FEATURES OF ORIENTATION TO LIFE TIME
  HOMES FROM VIEWPOINTS OF WHEEL CHAIR MOVEMENTS POSSIBILITY* — **"ACUTUAL" is the publisher's own
  spelling in the Crossref record.** Carry it verbatim; do not silently correct a stored title.
- **Journal:** Journal of Architecture and Planning (Transactions of AIJ) **69(577):33–39** · 2004 ·
  ISSN 1340-4210 / 1881-8161 · **Architectural Institute of Japan**
- **DOI:** `10.3130/aija.69.33_1`
- **R9:** NOT HELD.
- **Retrieval rung (R10):** **Crossref reference-resolution, rung 2, 200** (`e7c0b1f141ea4c1a.json`)
  → **direct DOI Crossref, 200** (`ac2a86db5cbeca4c.json`) → **Unpaywall: bronze OA, J-STAGE PDF**
  (`a0e41367085fcfb7.json`) → **J-STAGE English abstract page read** → **independently re-found as
  hit #2 of the J-STAGE Japanese-index search** (`d8217b8884ac188f.xml`). Five rungs, two indexes.
- **R5 status:** Architectural Institute of Japan Transactions is a **peer-reviewed academic**
  journal → **ACADEMIC, not grey.** Its absence from PubMed/Scopus-fed engines is an *indexing fact*.
- **⚠ UNVERIFIED:** **the language of the article body.** Title and abstract are available in
  English; AIJ Transactions publishes predominantly in Japanese. I did **not** open the PDF and I
  do **not** assert the body language. Record as `language: ja (UNCONFIRMED)`.
- **Read status:** **English abstract only. Everything I say about its content is bounded by that
  abstract.**

### A8 · Kapsalis, Jaeger & Hale (2022) — **T2 `sr_meta`** — the only confirmed synthesis

- **Authors (byline order):** Kapsalis, Efthimis; Jaeger, Nils; Hale, Jonathan *(n=3, Crossref)*
- **Title:** *Disabled-by-design: effects of inaccessible urban public spaces on users of mobility
  assistive devices – a systematic review*
- **Journal:** Disability and Rehabilitation: Assistive Technology **19(3):604–622** · Crossref
  `issued` **2022-08-19** (online) with issue in volume 19 (2024). **Record year 2022 with a note
  that the issue is 19(3); do not silently pick one.** ISSN 1748-3107 / 1748-3115 · Informa UK ·
  **CC-BY-NC-ND**
- **DOI:** `10.1080/17483107.2022.2111723`
- **R9:** NOT HELD (batch 04 proposed it; that batch was retracted and wrote nothing).
- **Retrieval rung (R10):** DOI → **Crossref, 200** (`1cfd192efd557b21.json`). **I did not re-use
  batch 04's payload** — CLAUDE.md §2(c) and this batch's own provenance hazard both say another
  agent's artefact is not my verification.
- **Tier test — the one that matters for §9 of the tier system:** `sr_meta` (T2) requires a defined
  method with **risk-of-bias appraisal and/or effect synthesis**. Kapsalis states it explicitly:
  three databases (Scopus, Web of Science, PubMed), 3,980 records screened to 48 included, and
  *"assessed their quality of evidence via the **Mixed Methods Appraisal Tool**"*. **Appraisal
  present → T2 `sr_meta` is sound.** Contrast with Bragança (§8, C-3), which I did **not** admit
  because I could not confirm appraisal.
- **Read status:** **abstract only.** Any claim about its 48 included studies beyond the abstract is
  a HYPOTHESIS and I do not make one.

---

## 4. POPULATION GRADING (R13) — population of STUDY vs population SERVED

The population served by this slug is **disabled people using the circulation of a building** —
principally `MOB`, `SCI`, `LMB`, `MS`, `PAIN`, `BAR`, `LPA`, `VES`, and (for the orientation and
sensory axes) `BLIND`, `DEAF`, `DEM`, `AUT`, `ID`. Per FRAME §2, applicability is an **output** of
synthesis, so these grades say what each study *measured*, never which populations the slug serves.

| # | Study population | Grade | Mismatch reason (written, not implied) |
|---|---|---|---|
| **A1** Koontz 2010 | 223 device users: MWC 109, PWC 100, scooter 14. Adults, both sexes, MeSH `Persons with Disabilities` absent but `Wheelchairs`/`Architectural Accessibility` present | **EXACT** for `MOB`/`SCI` | Convenience sample recruited partly at *a national wheelchair sport event* — likely skewed toward younger, fitter, more skilled users. **That skew biases the finding CONSERVATIVELY**: a more able sample failing code-compliant space understates the failure rate. Diagnosis not reported → cannot grade `MS`, `PAIN`, `LMB` separately. |
| **A2** Dutta 2011 | **Five scooters; ONE expert driver.** No scooter user participated. | **PROXY** | The human operator is an expert and (undeclared but implied) non-disabled. **All user-side variance is absent** — strength, trunk control, reach, spasticity, visual field, cognition, fatigue, confidence. Measures what a *device* can do, not what a *person* can do. `LPA`, `BAR`, `LMB`, `VES` entirely unrepresented. |
| **A3** King 2011 | As A2 — expert driver, two scooter models | **PROXY** | As A2. Additionally n=2 devices, so device-model variance is barely sampled. |
| **A4** Marchiori 2023 | 17 people with SCI, **C4–T12, AIS A/B/C**, MWC >4 h/day, 16 M / 1 W, mean age 39.8 ± 10.8 y, mean 6.8 ± 5.4 y post-injury (Table 1, p.4) | **EXACT** for `SCI`; **PARTIAL** for `MOB` | **Two mismatches, and the first is severe. (i) The inclusion criteria require "independent community mobility in the MWC, *including ascending an access ramp*" (§2.1). The study therefore SELECTS OUT exactly the people for whom ramps are already impassable** — the finding is a lower bound on population burden, structurally. (ii) **16 of 17 participants are men.** Shoulder anthropometry and strength are sexually dimorphic; a 94%-male sample cannot ground a claim about women wheelchair users. |
| **A5** Arnet 2025 | **Ten able-bodied participants** | **PROXY** | Stated plainly: **no wheelchair user took part.** Able-bodied participants have intact trunk control, no shoulder overuse history, no spinal-cord-injury-related muscle imbalance, and no chronic exposure — i.e. they lack the very condition (cumulative shoulder pathology) the study exists to inform. The absolute forces are indicative; **the ranking across activities is the transferable part**, and even that is a hypothesis for real users. |
| **A6** Goodwin 2022 | 145 respondents: **112 people with mobility impairment (77.2%) + 33 family members (22.7%)**; 72.5% under 65; 62.1% female; wheelchair use 39.3% manual / 4.1% manual-with-electric / 33.1% electric; walking stick 28.3%, frame 22.1%, scooter 16.6%, crutches 6.2%. Most common conditions: arthritis 28.9%, back problems 28.3%, general lack of mobility 25.5%, knee problems 24.1% | **PARTIAL** for `MOB`/`PAIN` | **Two written mismatches. (i) 22.7% of responses are PROXY VOICE** — a carer or relative completing on behalf of the disabled person. Under a Co-1 reading this alone would be disqualifying; under T3 it is a stated limitation. (ii) Australia-only, and the sample over-represents severe/profound impairment (the authors say so, comparing to 2.9% population base rate) and under-65s. **Not** graded for `BLIND`, `DEAF`, `AUT`, `ID`, `DEM` — those populations were not sampled. |
| **A7** Baba 2004 | Field survey of **newly built Japanese residences** (dwellings, not people) | **PROXY** | The unit of analysis is a *building*, not a person; wheelchair movement is assessed as a geometric possibility, not observed. Japanese dwelling stock and Japanese body/device dimensions may not transfer. **Grade is provisional on the English abstract only.** |
| **A8** Kapsalis 2022 | Synthesis of 48 studies of Mobility Assistive Device users | **PARTIAL** | The review states its own limitation: *"the reviewed studies mostly [f]ocused on wheelchair users residing in high-income countries."* So the synthesis inherits a high-income, wheelchair-centric skew and does not speak for `LMB`, `LPA`, `BAR`, or the Global South. |

### The endemic-PROXY pattern, stated plainly

**Three of eight admissions (A2, A3, A5) have no disabled participant at all**, and a fourth (A7)
has no human participant. The circulation-geometry evidence base is substantially built from
**expert operators, able-bodied volunteers, and measured buildings** standing in for disabled people.
That is not a defect of my selection — it is the shape of the literature, and searches #9 and #10
surfaced it repeatedly. **It should be recorded as a property of the corpus, because it directly
caps the strength of any determination made from it.**

---

## 5. HARM / FAILURE / INADEQUACY (R7) — first-class, with locators

### H-1 · CODE-COMPLIANT SPACE FAILS BETWEEN 10% AND 100% OF WHEELED-MOBILITY USERS. This is the batch's central harm finding.

> *"Between 10% and 100% of users would not be able to maneuver in spaces that meet current
> Accessibility Guidelines for Buildings and Facilities specifications."*
> — Koontz, Brindle, Kankipati, Feathers & Cooper 2010, `10.1016/j.apmr.2010.01.009`, **abstract
> Conclusions**, APMR 91(5):759–764. n = 223 device users. **[abstract-level locator; full text
> paywalled]**

**What this establishes:** compliance with the accessible-design standard is *not* evidence of
usability, and the gap is not marginal. **What it does not establish:** which manoeuvre produces
which failure rate, or the specific dimensions — **those are in the paper's tables, which I could
not obtain.** The 10–100% range is the paper's own summary across four manoeuvres and three device
classes; **any narrower claim is a HYPOTHESIS until the tables are read.** Highest-priority
full-text retrieval arising from this batch.

### H-2 · NO TESTED MOBILITY SCOOTER COULD COMPLETE ALL INDOOR MANOEUVRES WITHIN STANDARD-ALLOWED SPACE

> *"None of the scooters tested were capable of completing all manoeuvres within the space allowed by
> existing standards."*
> — Dutta, King, Holliday, Gorski & Fernie 2011, `10.3109/17483107.2010.509885`, **abstract
> Conclusions**, DRAT 6(1):67–76. Five scooters; configurations included *turning 180° in a
> corridor* and *turning 90° from a doorway*. **[abstract-level locator; full text paywalled]**

**Independent of H-1 in device class (scooters, which Koontz sampled at only n=14) but NOT
independent of H-3** (same programme). Bears on `AX-WHM`, and on `A-REACH` ("doorway/turning
clearance").

### H-3 · THE 1.5 m TURNING CIRCLE IS A MANUAL-WHEELCHAIR ARTEFACT AND UNDERSIZES SCOOTERS BY UP TO 223%

> *"Compared to the area required for a turning circle, 42–54% savings were achieved. Relative to
> existing requirements, **53–95% more space is required to accommodate the Celebrity-X; 173–223%
> increases are necessary for the Fortress-1700**."*
> — King, Dutta, Gorski, Holliday & Fernie 2011, `10.3109/17483107.2010.549898`, **abstract
> Results**, DRAT 6(5):432–439. **[abstract-level locator; full text paywalled]**

The paper's own framing of the mechanism: *"Accessibility standards for wheeled mobility devices
currently use a 1.5 m turning circle, **designed to accommodate manual wheelchairs**. Scooters are
less manoeuvrable than wheelchairs."* **The harm is that a single geometric primitive, derived from
one device class, is applied to a device population it does not fit.**

### H-4 · THE SHOULDER-LOAD PENALTY IS INCURRED BY THE EXISTENCE OF A SLOPE, NOT BY ITS STEEPNESS. This is the finding an item-value frame could not have produced.

**First-hand from the full PDF.** Marchiori, Gagnon & Pradon 2023, `10.3390/s23218659`:

- **Slopes tested (§2.2 Protocol, p.4):** *"the four treadmill slopes: 0°, 2.7°, 3.6° and 4.8°. The
  four slopes greater than 0° corresponded to slopes that increase from one unit of height to 20,
  16, 12 and 8 units of length, respectively."*
- **Table 3 (pp. 7–8), shoulder flexion/extension, PUSH phase, proportion at HIGH risk level:**
  **0° → 12.2% · 2.7° → 44.5% · 3.6° → 47.0% · 4.8° → 45.2%**
- **Table 5 (p.10), kinetic PUSH phase, proportion at HIGH risk:**
  **0° → 51.8% · 2.7° → 79.7% · 3.6° → 82.1% · 4.8° → 88.1%**
- **The authors' own reading (§4 Discussion, p.11):** *"There was no difference between the slopes…
  This suggests that **greater efforts are required to propulse the wheelchair from the smallest
  slope (2.7°), but that this effort does not increase further with the increasing slope**."*
- Focused ADI increase from 0° to slope: **wrist 29–36%, elbow 16–26%, shoulder 14–19%** (§4).
  Global ADI increase **18–20%** (§4).

**Why this matters for a determination:** the step change sits between *level* and *any ramp*. Making
a gradient shallower across the regulated range did **not** recover the joint load in this study.
A frame built from an item called "Ramp Gradient (≤1:20)" would have gone looking for the difference
between 1:20 and 1:12 and found the wrong question.

**⚠ AND A PUBLISHED ERROR I MUST FLAG.** The sentence quoted above says *"the four slopes greater
than 0°"* and then lists **four ratios (20, 16, 12, 8) for THREE non-zero slopes.** The arithmetic
settles it — arctan(1/20)=2.86°, arctan(1/16)=3.58°, arctan(1/12)=4.76° — so the mapping is
**2.7°≈1:20, 3.6°≈1:16, 4.8°≈1:12, and 1:8 WAS NOT TESTED.** Anyone citing this paper for a 1:8
result would be citing an error in the paper itself. **Record the mapping, not the sentence.**

### H-5 · RAMP *DESCENT* IS A HIGHER SHOULDER-LOAD EVENT THAN FAST PROPULSION, AND THE DISCOURSE IS ALL ABOUT ASCENT

> *"Highest mean glenohumeral contact forces were found during weight relief lift (**1363 ± 1204 N**),
> followed by **descending a ramp (997 ± 1043 N)** and fast propulsion (**802 ± 742 N**). The
> supraspinatus muscle generated the greatest force during weight relief lift (**327 ± 490 N**) and
> fast propulsion (**184 ± 205 N**)."*
> — Arnet, Veeger & de Vries 2025, `10.1016/j.jelekin.2025.103027`, **abstract Results**, J
> Electromyogr Kinesiol 84:103027. **[abstract-level locator; full text paywalled]**
> **⚠ Ten ABLE-BODIED participants — see A5 and §4. The absolute newtons do not transfer; the ORDERING
> is the claim, and it is a hypothesis for real users.**

Gradient regulation, propulsion research and the guidebook's own vocabulary are organised around
*going up*. This is the only source in my batch that measures *coming down*, and it puts descent
second out of seven activities. **Note also the standard deviations exceed or approach the means
(997 ± 1043 N) — the distribution is wildly dispersed and a mean is a poor summary. Do not write
997 N as a value.**

### H-6 · CIRCULATION FAILURE IS ALSO AN EGRESS AND EMERGENCY-ACCESS FAILURE, IN DISABLED PEOPLE'S OWN WORDS

> *"Another important aspect of safety in accessible design is emergency egress from the property.
> For people with mobility impairment, being able to get out of the property in a safe and timely
> manner is extremely important in the event of a fire or other emergency. **Access for emergency
> workers to get into the building is equally important, as doorways and passageways are often too
> narrow to allow sufficient access**."*
> — Goodwin et al. 2022, `10.1002/ajs4.214`, **§3.5**, AJSI 57(4), p.964. **[full text read]**

And the harm that is *not* about safety at all, which I include because it recurs in the data and is
invisible to every dimensional standard:

> *"Accessible design would reduce avoidable damage to the property, as mobility devices would be
> less likely to scrape wider doorways and corridors. **This response was particularly prevalent for
> people living in private rentals where modifications were not possible**."* … *"To be able to move
> about within your own home without damaging walls."* (Participant 66; 18–24 years old with a
> profound limitation)
> — Goodwin et al. 2022, **§3.6**, pp. 964–965. **[full text read]**

**An undersized corridor transfers a financial and tenancy risk onto the disabled tenant.** That is a
harm class with no dimensional expression and no code hook.

### H-7 · 71% OF A DISABLED SAMPLE WERE LIVING IN HOUSING THAT DID NOT MEET THEIR ACCESS NEEDS — AND IT WAS WORST FOR THE MOST DISABLED

> *"27.5 per cent of participants were living in accessible housing (including 18.6 per cent built
> accessible and 8.9 per cent modified fully accessible), while **71.0 per cent were living in
> housing that did not fully meet their accessibility needs** (including 38.6 per cent modified
> partly accessible and 32.4 per cent not built or modified accessible)."* … *"most people who
> reported having a severe or profound mobility impairment were currently living in inaccessible
> housing (**85.1 per cent and 59.6 per cent**, respectively; see Table 2)."*
> — Goodwin et al. 2022, **§3.1**, AJSI 57(4), pp. 960–961. **[full text read]**

### H-8 · A HARM CLASS I SEARCHED FOR AND DID NOT FIND — recorded as a gap, not a finding

I hunted deliberately (search #12) for **entrapment in automatic doors, injury at internal
thresholds and level changes, and entryphones inoperable by Deaf or blind people**. Search #12
returned **nothing usable** on any of the three, for the query-shape reason recorded in §1. **I make
no claim that these harms are rare. I claim only that a PubMed AND-chain cannot reach them**, and
that the right instrument is an injury-surveillance database (NEISS, EU-IDB) or a coroner/regulator
corpus, not a bibliographic index. **The Deaf/blind entryphone question in particular returned
nothing at all and is completely unevidenced in this batch.**

---

## 6. QUANTIFIED FINDINGS (R3) — every number with its locator

**Read-status legend:** **[FULL]** = I read the full text · **[ABS]** = abstract only, and the number
is in the abstract · **[UNVERIFIED-QUANT]** = number reported but not locatable to a source I read.

| Value | Locator | Read |
|---|---|---|
| Between **10% and 100%** of users cannot manoeuvre in ADAAG-compliant space | `10.1016/j.apmr.2010.01.009`, abstract Conclusions | **[ABS]** |
| n = **109** MWC, **100** PWC, **14** scooter users | `10.1016/j.apmr.2010.01.009`, abstract Participants | **[ABS]** |
| Passageway openings increased in **5-cm** increments | `10.1016/j.apmr.2010.01.009`, abstract Intervention | **[ABS]** |
| Three-point-turn rectangle vs turning circle: **42–54%** area saving | `10.3109/17483107.2010.549898`, abstract Results | **[ABS]** |
| Celebrity-X needs **53–95%** more space than existing requirements | `10.3109/17483107.2010.549898`, abstract Results | **[ABS]** |
| Fortress-1700 needs **173–223%** more space | `10.3109/17483107.2010.549898`, abstract Results | **[ABS]** |
| Current standard turning circle = **1.5 m**, "designed to accommodate manual wheelchairs" | `10.3109/17483107.2010.549898`, abstract Purpose | **[ABS]** |
| Obstacle sizes used in U-turn tests: **50 mm** and **1200 mm** | `10.3109/17483107.2010.509885`, abstract Method | **[ABS]** |
| Slopes tested: **0°, 2.7°, 3.6°, 4.8°** = **1:20, 1:16, 1:12** (see H-4 on the published 1:8 error) | `10.3390/s23218659`, §2.2 Protocol, p.4 | **[FULL]** |
| Shoulder flex/ext push, HIGH risk: **12.2% → 44.5% → 47.0% → 45.2%** | `10.3390/s23218659`, **Table 3, pp. 7–8** | **[FULL]** |
| Kinetic push, HIGH risk: **51.8% → 79.7% → 82.1% → 88.1%** | `10.3390/s23218659`, **Table 5, p.10** | **[FULL]** |
| Focused ADI increase: wrist **29–36%**, elbow **16–26%**, shoulder **14–19%**; global **18–20%** | `10.3390/s23218659`, §4 Discussion, p.11 | **[FULL]** |
| Kinetic focused ADI push-phase increase **22–29%** | `10.3390/s23218659`, §4 Discussion, p.11 | **[FULL]** |
| Mean self-selected propulsion speed **1.17 ± 0.18 m/s** (min 0.91, max 1.65) | `10.3390/s23218659`, §3 Results, p.6 | **[FULL]** |
| Trunk flexion rose **16→27°** (push) and **11→19°** (recovery) from 0° to slope | `10.3390/s23218659`, §3.1.4, p.7 | **[FULL]** |
| n = **17** SCI, **C4–T12**, AIS A/B/C, mean age **39.8 ± 10.8** y, **6.8 ± 5.4** y post-injury, **16 M / 1 W** | `10.3390/s23218659`, **Table 1, p.4** | **[FULL]** |
| Glenohumeral contact force: weight-relief lift **1363 ± 1204 N**, ramp descent **997 ± 1043 N**, fast propulsion **802 ± 742 N** | `10.1016/j.jelekin.2025.103027`, abstract Results | **[ABS]** |
| Supraspinatus force: weight-relief lift **327 ± 490 N**, fast propulsion **184 ± 205 N** | `10.1016/j.jelekin.2025.103027`, abstract Results | **[ABS]** |
| **71.0%** in housing not meeting access needs; **27.5%** accessible (18.6% built + 8.9% fully modified) | `10.1002/ajs4.214`, §3.1, p.960 | **[FULL]** |
| **85.1%** (severe) and **59.6%** (profound) living in inaccessible housing | `10.1002/ajs4.214`, §3.1 and Table 2, pp. 960–961 | **[FULL]** |
| Sample n = **145** (112 disabled, 77.2%; 33 family, 22.7%) | `10.1002/ajs4.214`, §3.1, p.960 | **[FULL]** |
| Mobility aids: manual WC **39.3%**, electric WC **33.1%**, stick **28.3%**, frame **22.1%**, scooter **16.6%**, crutches **6.2%** | `10.1002/ajs4.214`, §3.1, p.961 | **[FULL]** |
| Survey completion time **33.2 min (SD 38.5)** | `10.1002/ajs4.214`, §2, p.959 | **[FULL]** |
| "Enlargement in door openings and corridors by **more than thirty centimetres** is generally an actual resolution" | `10.3130/aija.69.33_1`, **English abstract** | **[ABS]** ⚠ **This is the paper's summary of a whole-stock survey, not a design recommendation. Do not read it as "+300 mm".** |
| 48 studies included from 3,980 screened, 3 databases, MMAT appraisal | `10.1080/17483107.2022.2111723`, abstract Methods | **[ABS]** |
| **49** Japanese academic records for 車椅子 × 廊下 × 幅員 in J-STAGE | J-STAGE WebAPI, `opensearch:totalResults`, artefact `d8217b8884ac188f.xml` | **[FULL]** — first-hand from the payload |

**No number in this brief was written from memory.** Every one traces to a payload path or a PDF
sha256 recorded above. **No code or standard value appears anywhere in §6** (R12 / 2026-08-12
REFERENCE-ONLY ruling); where a source characterises a standard (the 1.5 m turning circle, ADAAG
compliance), the value is *the source's own quoted finding about the standard*, which is an outcome
claim with a DOI locator, not a code value mined from a code.

---

## 7. CODE / STANDARD LEADS (R12) — checked against the 83 held

I derived the held set read-only: **83 distinct `(jurisdiction, standard_name)` pairs** —
US 19, GB 17, DE 10+, AU 11+, ISO 5, CA 1 (`CSA B651:2023`), JP 1 (`JIS T 9251:2014`).

**I propose ONE new lead, and I propose it hesitantly:**

| Jurisdiction | Standard name | Clause | Evidence | Caveat |
|---|---|---|---|---|
| **US** | **ADAAG — Americans with Disabilities Act Accessibility Guidelines for Buildings and Facilities** | **UNKNOWN — I do not have it** | Koontz et al. 2010 names this document verbatim as the specification its 223 users failed (`10.1016/j.apmr.2010.01.009`, abstract Conclusions). A 2010 study tests the **pre-2010** ADAAG, which is a different document from the 2010 ADA Standards. | **May be judged a duplicate** of the held `US · ADA / A117.1` or `US · ADA 2010`. The distinguishing fact is the **edition**, not the family. **Orchestrator's call; I do not assert it is distinct.** No clause because the paper is paywalled and I will not guess one. |

**Everything else I could name is already held.** A2/A3 compare against "existing standards" without
naming them (Toronto Rehab, so plausibly `CSA B651` — **held**; I do not assert this, the papers do
not say). A7's Japanese referent is not named in its English abstract. **I decline to invent leads to
fill the section** — a `research_code_leads` row that names a document nobody can point to is worse
than an empty section.

**One held-set observation worth passing on:** `JP` holds exactly **one** lead (`JIS T 9251:2014`,
tactile indicators) against **49** Japanese academic records on corridor width alone. The Japanese
regulatory instrument for this territory — the Barrier-Free Law and its building standards — is not
in the held set at all.

---

## 8. CANDIDATES TO STAGE (`search_candidates`, NOT admissions)

Every HYPOTHESIS label marks a description I have **not** confirmed by reading the source.

| id | Candidate | Disposition | Note |
|---|---|---|---|
| **C-1** | **Kasem, Menatalla; Kaleem, Zarah; Clark, Sam; Sakellariou, Dikaios** (2026). *(En)Abling Architectural Research: Co-Designing With People With Intellectual Disabilities.* JARID **39(4):e70275**. DOI `10.1111/jar.70275`. PMID 42381471, PMCID PMC13320296, CC-BY. **Crossref + Europe PMC + full-text XML all mine.** | **PENDING-VERIFICATION** — **highest-value staged item** | **The strongest Co-1 warrant found in this batch and it is verifiable**: Zarah Kaleem is affiliated to **Cardiff People First**, a self-advocacy organisation; the abstract states the article *"is co-authored by academic researchers and a co-researcher with lived experience of an intellectual disability."* **NOT a hypothesis — quoted from the retrieved full text.** Rejected as an admission only because it reports method, not buildings (§2.3). **The owed action is specific: retrieve the underlying Cardiff University doctoral study (Welsh School of Architecture, ethics refs SREC 2204, 22111, 23048), which the paper says generated "concrete, participant-led insights about sensory, spatial and navigational challenges."** That is where the `ID`/`AX-COG-O`/`AX-SPR` circulation evidence is. |
| **C-2** | **Tsuchiya, Shin'ichi; Furukawa, Yoko; Miyano, Yoshiyasu; Yoshida, Naoyuki; Hasemi, Yuji** (2003). *WALKING BEHAVIOR OF A CROWD INCLUDING WHEELCHAIR USERS.* Journal of Environmental Engineering (Transactions of AIJ) **68(571):1–7**. DOI `10.3130/aije.68.1_6`. **Crossref-verified, mine** (`428edda3e96de772.json`). | **PENDING-VERIFICATION** → then this slug | **Prior art, by sixteen years, to the work batch 04 called "the single highest-value staged item" (Geoerg 2019 on crowd flow with wheelchair users).** Japanese-language, AIJ, invisible to every English engine I ran. **HYPOTHESIS** that it contains quantified flow or width data — I have only the title. **If it does, the English-language crowd-dynamics literature has been rediscovering a 2003 result.** Requires a Japanese reader. |
| **C-3** | **Bragança, Sara; Castellucci, Ignacio; Costa, Eric; Arezes, Pedro; Carvalho, Miguel** (2019/2020). *Anthropometric data for wheelchair users: a systematic literature review.* Int J Occup Saf Ergon **26(1):149–172**. DOI `10.1080/10803548.2019.1567974`. **Crossref-verified, mine** (`9bc3f9ca8390f1ca.json`). | **PENDING-VERIFICATION** — **deliberately NOT admitted** | **The inadequacy anchor, if it survives one test.** Its finding is that wheelchair-user anthropometry — the data under every dimensional standard — is *"limited"*, with *"a lack of consistency between studies, regarding the measurements collected, samples used and methods applied."* 41 articles. **Not admitted because I could not confirm risk-of-bias appraisal or effect synthesis, and tier-system §9 makes that the difference between T2 `sr_meta` and T3.** T&F returned **403**. **The falsification test is one sentence long: does the method section contain a quality appraisal? If yes → T2 and it is a strong admission. If no → T3 mapping review.** I refuse to guess. |
| **C-4** | **Bharathy, Aravind; D'Souza, Clive** (2018). *Revisiting Clear Floor Area Requirements for Wheeled Mobility Device Users in Public Transportation.* Transportation Research Record **2672(8)**. DOI `10.1177/0361198118787082`. | **REHOME/PENDING** → this slug | n = **500** WhMD users, the updated IDeA Center dataset; its abstract states prior research indicates standard clear-floor dimensions *"are too small to accommodate the size of many occupied wheeled mobility devices, especially power chairs and scooters."* **Setting is transportation vehicles**, so it is on-construct for *footprint* but off-setting for *buildings* — that is why it is staged, not admitted. Batch 04 staged the same paper (its C-c); **I did not re-verify it through Crossref this session, so treat its bibliography as unconfirmed by me.** |
| **C-5** | **D'Souza, Clive; Steinfeld, Edward; Paquet, Victor; Feathers, David** (2010). *Space Requirements for Wheeled Mobility Devices in Public Transportation.* Transportation Research Record 2145. DOI `10.3141/2145-08` | **PENDING-VERIFICATION** | n = 369, the earlier IDeA dataset that C-4 supersedes. **Batch 04 admitted this as T1 and its own repair plan records that the T1 was "asserted on the same test the brief used to put Chang & Drury at T3" — i.e. the tier is contested by the project's own record.** Do not inherit that tier. R9: NOT HELD. |
| **C-6** | **Steinfeld, E. et al.** (2010). *Anthropometry and Standards for Wheeled Mobility: An International Comparison.* Assistive Technology. | **PENDING-VERIFICATION** | Compares four countries' research against their prevailing standards; abstract states US standards *"are based on research conducted in the 1970s"* and *"need to be updated."* **HYPOTHESIS** on all bibliographic detail — **I did not resolve a DOI and the Consensus rendering gave only "E. Steinfeld et al."** Do not store the author list from that rendering. |
| **C-7** | **Thies, Sibylle Brunhilde; Bevan, Susan; Wassall, Matthew; Shajan, Blessy Kurissinkal; Chowalloor, Lydia; Kenney, Laurence; Howard, Dave** (2023). BMC Geriatrics **23(1):734**. DOI `10.1186/s12877-023-04443-7`. Authors from the **PubMed payload**. | **MISCELLANEOUS** | Carries the one usable line from search #12: *"**Lifting of walking frames when crossing door thresholds or when turning has shown to reduce stability**, and certain design features drive the need to lift."* That is a threshold-harm mechanism for `AX-BAL`/`AX-AMB` — **but it is stated as background and attributed to prior work, so it is a citation-of-a-citation.** The study itself is a walking-frame development trial (9 healthy older adults + 9 frame users). **Mine the reference behind that sentence; do not cite this paper for it.** |
| **C-8** | **Huang, Yizhe et al.** (2025). *Measuring spatial accessibility for wheelchair users: A case study in a Chinese campus.* PLOS One. DOI `10.1371/journal.pone.0335663` (R9: NOT HELD) | **PENDING-VERIFICATION** | Reports mean travel speed **1.03 m/s assisted vs 0.67 m/s unassisted**, and that unassisted users could not pass curb ramps steeper than 1:5. **⚠ The abstract says "Thirty students with wheelchair experience" — which may mean able-bodied students in wheelchairs, i.e. SIMULATION → PROXY at best under R13.** Resolve that before use. **HYPOTHESIS on the full author list — I have only "Yizhe Huang et al." from Consensus and ran no Crossref lookup. Store nothing beyond the first author.** Batch 04 staged the same paper with the same warning. |
| **C-9** | **Flemmer, C.** (2022). *Improving the built environment for manual wheelchair users: A review.* IOP Conf. Series: Earth and Environmental Science. | **MISCELLANEOUS** | Narrative review → **T3 under tier-system §9**, never `sr_meta`. Useful for its three-part framing (intrinsic capability / non-compliant features / maintenance and obstruction) which maps cleanly onto the ICF person–environment split. Not an anchor. |
| **C-10** | **Akosile, C. et al.** (2025). *Wheelchair-Accessibility of Religious Places of Worship in Anambra State, Nigeria.* J Disability & Religion. | **PENDING-VERIFICATION** | Cross-sectional audit of **193 buildings**; reports **94.3%** of doorways and **94.8%** of routes accessible but only **4.2%** of ramps and **10.2%** of steps, and **0 of 61** buildings needing lifts had one — overall **3.6%** accessible. **Corrects the high-income skew Kapsalis names as its own limitation.** **HYPOTHESIS on full authorship and DOI — not resolved.** Note its accessibility criterion is ADAAG conformity, which H-1 shows is itself not a usability criterion. |
| **C-11** | **Liebergesell, Natalia Pérez; Vermeersch, Peter–Willem; Heylighen, Ann** (2021). *Urban Chandelier: How Experiences of Being Vision Impaired Inform Designing for Attentiveness.* J Interior Design **46(1):73–92**. DOI `10.1111/joid.12192`. **Crossref-verified, mine** (`12e3cf45af196e3b.json`). | **REHOME** → a wayfinding/sensory slug | Heylighen's group works from disabled people's spatial expertise. **HYPOTHESIS** that it contains circulation-geometry content. Relevant to `AX-VIS-L`/`AX-VIS-N`. |
| **C-12** | **Osakaya, Yoshiyuki** (1999), `10.3130/aijt.5.139`; **Baba, Akio; Mori, Akiko; Asaine, Wataru; Hasegawa, Naoji** (2002), `10.3130/aija.67.121_3` — both **Crossref-verified, mine**. Plus **~45 further J-STAGE records unexamined**. | **PENDING-VERIFICATION** (bulk) | The tail of the 49-record Japanese seam (§9.4). The 2002 Baba paper is *"A PROPOSAL ON EVALUATION METHOD FOR LIFETIME HOMES BASED ON BUILDING STANDARDS IN UNITED KINGDOM"* — a Japanese team evaluating **UK** Lifetime Homes standards, i.e. a cross-jurisdictional appraisal invisible to UK-language search. |
| **C-13** | **Euan's Guide Access Survey** (Euan's Guide, Scottish charity SC045492, disability-led) | **PENDING-VERIFICATION** | Genuinely disability-led with a decade of annual survey data (6,000+ respondents in 2023). **The 2023 report URL returns HTML, not the PDF** (logged, 15,580 B). Content skews to information, toilets and staff rather than circulation. **Retrieve the actual PDF before judging it**; if its circulation content is thin, say so and close it rather than leaving it open. |
| **C-14** | **"Accessibility of public buildings in the United States: a cross-sectional survey"**, Disability & Society, DOI `10.1080/09687599.2023.2239996` (R9: NOT HELD) | **PENDING-VERIFICATION** | n = 109 disabled respondents on **buildings** (not streets), *"largely reporting on accessibility barriers encountered in communal spaces."* Surfaced by search #4. **HYPOTHESIS on authors, year and all content — I ran no Crossref lookup. Nothing beyond the DOI and title should be stored.** |
| **C-15** | **King, Emily C. et al.** (2011) — *the other* mobility-scooter literature: **Bragança C-3's 41 included studies**, and the reference lists of A1–A3 | **PENDING-VERIFICATION** (R2 mining) | Backward citation mining on A1–A3 is the single cheapest next action: three papers, one lab lineage plus the IDeA Center lineage, and between them they cover every manoeuvre primitive in the slug. |

---

## 9. MY ADJUDICATION OF VALUE

### 9.1 What bears on a determination, and what is merely topical

**Bears on a determination about accessible circulation geometry:**

1. **A1 Koontz 2010** — the only source in the batch that tests *code-compliant space against real
   disabled users at scale* and reports a failure rate. Everything else in this brief either measures
   a device, models a body, or asks people what they want. **If one source from this batch is read in
   full before anything is written, it is this one, and the reason is that its tables — which I could
   not obtain — are the difference between "compliance fails users" and a stated dimension.**
2. **A4 Marchiori 2023** — because it locates the discontinuity in the *wrong place* relative to the
   regulatory frame (H-4). A determination about ramps that assumes the interesting variation lies
   between 1:20 and 1:12 is not supported by the only first-hand joint-load data I obtained.
3. **A2/A3 Dutta & King 2011** — because they identify *the geometric primitive itself* (a 1.5 m
   turning circle inherited from manual wheelchairs) as the defect, rather than its magnitude. That
   is a different and more useful kind of finding than "the number should be bigger."
4. **A6 Goodwin 2022** — because on the question *which circulation features do disabled people
   themselves rank first*, 112 disabled respondents answering an open "magic wand" question converge
   on **step-free entrance, wider internal doors and corridors, level access throughout** (§3.2 and
   §4, pp. 961, 965). That is a preference-and-priority claim, and no biomechanics paper can make it.

**Merely topical, and I say so rather than admitting it:**

- **A8 Kapsalis 2022** is the batch's weakest admission. It is a properly appraised systematic review
  (which is why it is admitted), but its unit of analysis is *urban public space* and its findings
  are at the level of "pathway characteristics, boarding ramps, entrance features, confined spaces
  and service surfaces were least accessible." **It establishes that the problem exists. It cannot
  determine a dimension.** Admit it as context and convergence, not as an anchor.
- **A7 Baba 2004** is admitted for what it *is* (a non-English academic source on exactly this
  construct, and the entry point to a 49-record seam) more than for what it currently *says* to me,
  since I have only its English abstract. **If it must be dropped to stay within an admission budget,
  drop it before A8 — but dropping it also drops the R5 leg, and §9.4 is why that would be a loss.**

### 9.2 The R1 pass ran first, and it came back nearly empty. That is a finding, not a failure.

I ran the Co-1 / T2 / Co-2 pass **first and before any T1 work**, as R1 requires — searches #1–#8,
across Consensus, Scholar Gateway, PubMed and web. **Of eight R1-targeted searches, zero produced an
admissible Co-1 source about circulation geometry.** What they produced instead falls into three
clean classes:

1. **Co-produced work about the research process, not the building** — Kasem 2026 (impeccable
   warrant, zero circulation content), van Hoven 2024, Huang 2024. The participatory-architecture
   literature is currently writing about *how to do the research*.
2. **Co-produced work about the right topic in the wrong setting** — Fredericks 2024 (community
   mobility, minibus taxis).
3. **Lived-experience-titled work that is not co-produced** — Goodwin 2022, which I caught (§2.2).

And the Co-2 leg is a **structural negative** (§2.1): nine OT professional-body documents across
three bodies and two independent search paths, none carrying environmental-parameter content.

**My recommendation: record R1 as EXECUTED WITH AN EVIDENCED NULL RESULT rather than as unsatisfied.**
The difference matters. "R1 not done" invites a future session to redo it. "R1 done, and here are the
eight queries, five engines and three failure classes" tells that session where *not* to look, and
points it at C-1 — the Cardiff doctoral study — which is the concrete place the Co-1 evidence for
this construct actually lives. **The honest headline is: for accessible circulation geometry, the
disabled-led evidence base on the geometry itself has not been written yet, or has not been written
where these engines can see it.**

### 9.3 What is genuinely absent, versus absent from my search

I have tried hard to keep these apart.

**Genuinely absent (well-formed query, right index, nothing there):**
- **Circulation-geometry content in OT professional-body CPGs.** Search #8 was a title-field query on
  the exact document class, returned all 5 hits, and I read every abstract. The genre does not carry
  it (§2.1).
- **Co-1 sources whose subject is corridor, door, threshold or ramp *geometry*.** Three engines, five
  queries. The co-produced literature exists and is growing; its subject is not geometry.

**Absent from my search only — do NOT read these as absence of evidence:**
- **Everything about vertical circulation.** I did not search it, on purpose (§1 row 14).
- **Automatic-door entrapment, internal-threshold injury, and entryphone inaccessibility for Deaf and
  blind people.** Search #12 was the wrong instrument, and I say so in H-8. The Deaf/blind entryphone
  question returned literally nothing and remains completely open.
- **Non-Anglophone literature other than Japanese.** I probed one national index. German (DIMDI /
  LIVIVO / TIB), Nordic (SwePub), Francophone (HAL, Cairn) and Chinese (CNKI) are untouched, and
  §9.4 gives strong reason to expect they are not empty.
- **The interior of A1, A2, A3, A5 and A8.** All five are paywalled and I read abstracts. **Every
  claim I make about them is bounded by an abstract, and I have marked each one `[ABS]` in §6.**
- **`AX-ARO`, `AX-CHM`, `AX-CNT`, `AX-COM-E`, `AX-THR`, `AX-SPR` as circulation demands.** The frame
  lists 17 axes as candidates to test. My searches meaningfully probed roughly six —
  `AX-WHM`, `AX-AMB`, `AX-BAL`, `AX-PAI`, `AX-STA`, and weakly `AX-COG-O`. **Thermal load in long
  "accessible" detours, sensory load in circulation, and toileting-proximity as a route-planning
  constraint are all untested, and the frame explicitly warns against inferring scope from the slug's
  name.** `saturation_signal` is `none` on every row precisely because of this.

### 9.4 The single most consequential thing I found is not a paper. It is a seam.

Search #13 — one query, `車椅子 廊下 幅員`, against J-STAGE — returned **49 Japanese academic records**
on wheelchair × corridor × width. Eleven English-language searches across four engines surfaced
**one** of them, and only because a *German-language* query happened to route through it.

Two things follow, and both are load-bearing:

1. **R5 is not a courtesy rule; it is a coverage rule.** The project's standing position is that
   non-English peer-reviewed work is academic and non-indexation is an indexing fact. Search #13
   converts that from a principle into a measurement: **on this construct, the ratio of visible to
   existing non-English academic work was roughly 1:49 in a single index and a single language.**
2. **It may already have cost the project a priority claim.** Batch 04 called Geoerg et al. 2019 (on
   crowd movement with wheelchair users in corridors and bottlenecks) "the single highest-value
   staged item in this batch." **Tsuchiya et al., *Walking Behavior of a Crowd Including Wheelchair
   Users*, was published in AIJ Transactions in 2003** (C-2). I have not read it and I make no claim
   about its content — but a guidebook whose purpose is *"to get people to ask the right questions"*
   should not present a 2019 result as the frontier without knowing what a 2003 one says.

**Recommendation: a non-English index sweep is worth more per unit of effort right now than another
English-language batch on this slug**, and it is cheap — the J-STAGE WebAPI is open, unauthenticated,
and took one call.

### 9.5 A note on this batch versus batch 04

Batch 04 covered adjacent ground and was retracted; `evidence_sources` is 0 and none of its
proposals is held, so there was no R9 collision to manage. **I deliberately did not re-use any batch
04 payload** — its own brief carries a provenance warning that files in the shared retrieval-log may
not belong to the agent citing them, and CLAUDE.md §2(c) makes verification an artefact I must
produce myself.

Where we overlap, I concur (Fredericks off-slug; Huang's population needs resolving; the OT-CPG
rejection). Where I differ: **six of my eight admissions are sources batch 04 did not find** — Koontz,
Dutta, King, Marchiori, Arnet, Baba — and the two strongest (Koontz, and the Marchiori gradient
result) both came from queries framed on the *construct*. **That is the ICF-first frame doing exactly
what D-0187 was for.** A frame carrying "Corridor Clear Width (≥1200 mm Minimum)" would have sent me
looking for 1200 mm; instead I found a study saying that between 10% and 100% of users fail the
standard *whatever* the number is, and another saying the ramp penalty does not scale with gradient.
Neither answers the question the item name would have asked.

---

## 10. WHAT I COULD NOT VERIFY — every unconfirmed field, named

| Item | Unconfirmed | Handling |
|---|---|---|
| **A1 Koontz 2010** | **All content beyond the abstract.** Minimum passageway widths per manoeuvre, per device class — the paper's actual tables. Closed access (Unpaywall `closed`, payload `711b950e88d42b38.json`). | The 10–100% figure is the only quantified claim I make. **Any specific dimension attributed to this paper is a HYPOTHESIS.** Highest-priority full-text retrieval. |
| **A2 / A3 Dutta & King 2011** | **All content beyond the abstracts.** Both closed access. The per-configuration minimum dimensions in part I ("Minimum space requirements for each scooter for five spatial configurations are given") are the whole point of the paper and I do not have them. | `[ABS]` on every figure in §6. |
| **A5 Arnet 2025** | **All content beyond the abstract**; whether the ramp gradient tested is stated anywhere (**the abstract does not give it** — "different speeds and inclines"). **This is a material gap: a ramp-descent load figure without the gradient it was measured at cannot ground a determination.** | Flagged. Do not use the descent finding quantitatively until the gradient is known. |
| **A5 Arnet 2025** | Author 2's name form — Crossref `Veeger, Dirkjan (H. E. J.)` vs PubMed `Veeger, Dirkjan H E J` | Store PubMed's; both payloads retained. |
| **A5 Arnet 2025** | `pages` — Crossref `page` is **null**, `article-number` is `103027` | **Write to `article_number`, not `pages`.** Writing 103027 into `pages` is the exact MISMATCH class that `--verify-authors` flags (the REF-00968 precedent). |
| **A6 Goodwin 2022** | Author 1 and 3 name forms across figshare vs published byline | Store the published/Crossref form; variance recorded in §3. |
| **A7 Baba 2004** | **The language of the article body.** Also every content claim beyond the English abstract; also whether "ACUTUAL" is corrected in the print version. | Record `language: ja (UNCONFIRMED)`. Carry the title verbatim including the typo. |
| **A8 Kapsalis 2022** | **All content beyond the abstract**, including which of the 48 studies bear on building (rather than urban) circulation. Also the year/issue split — Crossref `issued` 2022-08-19 against issue 19(3). | `[ABS]`. Record year 2022 with an issue note; do not silently choose. |
| **C-3 Bragança** | **Whether a risk-of-bias appraisal was performed** — the single fact that decides T2 vs T3. T&F returned 403. | Not admitted. The falsification test is written in §8. |
| **C-6 Steinfeld 2010** | **The entire author list** — I have only "E. Steinfeld et al." from a Consensus rendering, and ran **no** Crossref lookup. | **Store nothing beyond the first author.** The 2026-08-19 failure was exactly a fabricated author list downstream of an "et al." rendering. |
| **C-8 Huang 2025** | **The entire author list beyond "Yizhe Huang"**; and whether "students with wheelchair experience" means disabled students or able-bodied simulation. | Store nothing beyond the first author. Resolve the population before any use. |
| **C-10 Akosile 2025**, **C-14 US public buildings** | **Full author lists, years, DOIs (C-10), all content.** No Crossref lookup run on either. | Titles and the one DOI I have are all that may be stored. |
| **C-13 Euan's Guide** | Whether the report contains any circulation content; the correct PDF URL. The URL I tried returns HTML. | Retrieve before judging. |
| **My own two PDFs** | They are **not in the manifest**, because `fetch()` crashes on binary (see the top of this brief). | sha256 recorded in §3 for both: Goodwin `ec6f233f…fb34`, Marchiori `61ee4e7a…327eb`. Verifiable by re-download. |
| **R12** | The clause for the ADAAG lead; whether it duplicates a held US lead. | Proposed without a clause and with the duplication risk stated. |

---

## FILES

- `scratchpad/session_2026-09-02-research-batch-05-circulation-icf/agonist/BRIEF.md` — this file
- `…/agonist/r9check.py` · `vet.py` · `resolve.py` · `oa.py` — read-only helpers, reusable
- `…/agonist/goodwin2022.pdf` + `.txt` — sha256 `ec6f233f1b93156795a5a9a2c97a83a45bbed7d84b77a340e2c0d7872141fb34`
- `…/agonist/marchiori2023.pdf` + `.txt` — sha256 `61ee4e7a49bc91f1793f4d9c6d1beff6a064be621de0befbe9b725a0760327eb`
- `retrieval-log/session_2026-09-02-research-batch-05-circulation-icf/manifest.jsonl` — **33 lines, 32 artefacts**

**Database writes performed: ZERO.** All access `file:data/guidebook.db?mode=ro`. `scripts/db.py`,
`migrate_db.py` and `emit_data_migration.py` were not invoked. The canonical DB sha256 has not moved.
