# R2 — Ruling precedence audit: what the owner actually has standing, 2026-08-24 → 2026-08-27

Adversarial auditor (Fable 5), read-only, lens: precedence after all supersessions. Read in full:
`references/project-standards.md:804-2125` (every entry 2026-08-24 onward),
`references/owner-notes/2026-08-27-architecture-note.md`,
`decisions/DR-2026-08-24-scaffolding-is-phase-specific.md`, `CLAUDE.md` rule 0 / §6 / pipeline
section, `scratchpad/session_2026-08-27-hook-audit/RENAME-MAP.md`, `WALKABILITY-PLAN.md` Parts
14–16, both named session records, plus git history 08-24→now and the DB read-only
(`user_version` 64). Mid-audit, three fresh owner rulings landed
(`references/project-standards.md:2046-2125`, commit `36f23c0`); they are audited in §4 as
instructed rather than adjudicated.

---

## 1. The precedence ledger, in date order

Legend: **STANDS** = operative now · **SUP** = superseded · **PART** = partly superseded.
"Recorded at" binds each to its record.

| # | date | ruling (owner wording abbreviated; quotes verbatim in the cited record) | supersedes | status now |
|---|---|---|---|---|
| 1 | 08-23/24 R1 | morning ".md→table" was never a ruling; evening clue ruling holds (*"the evening one holds"*) — DR §1 R1 | the false attribution in migrations 061/062 | **STANDS** |
| 2 | 08-23/24 R2 | store in columns/fields, not text strings — DR §1 R2 | the clues-back-to-markdown proposal | **STANDS** |
| 3 | 08-23/24 R8 | *"I don't want axis to be used!!!!"* / *"Axis is a term that we should be able to use freely"* — axis is descriptive English, never a domain identifier; axis route struck — DR §1 R8, ledger:804-815 | `DR-2026-07-22-work-from-axes`, `DR-2026-07-23` retention clause, standards:563-566 | **STANDS** in substance; replacement noun twice re-ruled (see #11, #27) |
| 4 | 08-23/24 R7 | scaffolding is phase-specific; *"only the data in tables can hop from stage to stage"* — DR §1 R7 | D-1 (generalises it) | **STANDS** |
| 5 | 08-24 §2.1 | *"It is better to have a table cell point to another table cell than to rewrite"* — rule 5 — DR §2.1, ledger:862-875 | inference I2 | **STANDS** (scoped reading of the 08-27 overrule; owner confirmation sought at ledger:2040-2042) |
| 6 | 08-24 §2.2 | pointer discipline: each stage's tables hold only its own data — DR §2.2, ledger:879-899 | inference I4 | **PART**: discipline STANDS; its embedded stage list superseded twice (#10, #16-adjacent) |
| 7 | 08-24 §2.3 | *"The clues table is a historical artifact… exists to be copied out of"* — DR §2.3, ledger:903-922 | inference I3 | **STANDS** (and item #3 non-adoption at ledger:1911 leaves the clue store un-re-homed) |
| 8 | 08-24 §2.4 | full cross-product research frame; connections defined *"until we have finished our syntheses"* — DR §2.4, ledger:926-946 | the linked-populations research frame; D-0165-as-blocker | **PART**: cross-product frame STANDS (re-affirmed by `research.matrix`, note + Part 14.8); the **deferral-to-synthesis half is OVERRULED** by #24 |
| 9 | 08-25 | scratchpads committed at every break — ledger:972-996 | — | **STANDS** |
| 10 | 08-25 | pipeline is FIVE stages — ledger:1000-1048 | the 08-24 §2.2 stage list | **SUP** by #16 (six stages) |
| 11 | 08-25 | demand layer named `icf_demands`; fold into `access_needs` REFUSED — ledger:1097-1136 | §R8's replacement wording "ICF-anchored access needs" | **PART**: the noun `icf_demands` **SUP** by #27 (`base_taxonomy_icf`); the anti-fold **STANDS** |
| 12 | 08-25 ×2 | two scoped commissioning supersessions of the 08-19 adversarial-review RULE — ledger:1052-1093, 1140-1174 | that RULE, for two sessions only | **SPENT** — expired by their own scope; the 08-19 RULE is unamended |
| 13 | 08-25 | *"separate out into 'ambulatory' and 'wheelchair user' to start"*; then *"yes, AMB and WHEEL to fan out"* (31→62) — ledger:1178-1224, 1285-1307 | `MOB` as a code | **STANDS** (its "pending **synthesis** re-derivation" justification now reads *judgment* under #24 — unrecorded ripple, D7 below) |
| 14 | 08-25 | *"specifications as a synthesis should be keying from a judgment item… cross-referencing itself against… all three modes"* — ledger:1228-1281 | the `(item × population)` grain of DR-2026-08-12 | **PART**: three-junction requirement STANDS; the keying-from-judgment is in unrecorded tension with #16's fan-in (M3 below) |
| 15 | 08-26 (PR #120) | judgment object is the **canonical parameter**; `items` demoted to the Part-4 render rollup — ledger:1311-1374 | `items`-as-identity; `specifications.item_code` NOT NULL | **STANDS**, confirmed by #26 |
| 16 | 08-27 | pipeline is **SIX stages**: *"you research slugs, evidence research, judge evidence, synthesize judgments, specify syntheses, and render specifications"* — ledger:1445-1482 | #10 and the "specifications is a table, not a stage" wording | **STANDS** |
| 17 | 08-26 (PR #121) | §R8 rename executes together with a retired-vocabulary register entry; rename-then-register — ledger:1378-1441 | — | **STANDS**, noun swapped by #27 |
| 18 | 08-27 | hand-off object is `<stage>_items` — *"we don't need to iterate different words for item — we just append '-item'"*; cardinality fan-out/fan-in; *"the rename creates the spine"* — ledger:1486-1586 | the per-table nouns of the nomenclature audit | **PART**: naming and fan-out/fan-in STAND; the middle clause (*"each row of evidence provides one row for judgment"*, 1:1) **SUP** same day by #21; ACTION (3) "`judgment_items` is a NEW table" refuted by #21/#22 |
| 19 | 08-27 | E-08 *"doesn't exist… ruled a million times"* — ledger:1590-1639 | (re-affirms a standing negative) | **STANDS** |
| 20 | 08-27 | the architecture note is *"not complete, and not definitive — just a thought document"* / *"just a proposal for what tables to make and why"* — Part 14 header; owner-notes Status | the note's brief promotion to a ruling | **STANDS** — governs the note's status |
| 21 | 08-27 | **adopt item #1**: evidence→judgment is **1:N** (*"one evidence source may provide many rows of judgment"*) — ledger:1836-1870 | #18's 1:1 clause; Q1 **CLOSED** (ledger:1861) | **STANDS** |
| 22 | 08-27 | **adopt item #2**: evidence item = the SOURCE; judgment item = the extracted, tiered value; `source_value_extractions` re-homed to judgment — ledger:1874-1922 | pre-08-27 stage maps for that table | **STANDS** |
| 23 | 08-27 | items **#3 and #4 NOT adopted** — clues not moved to substrate; ~825 not pursued — ledger:1911-1914 | — | **STANDS** |
| 24 | 08-27 | *"overrule Aug 24 DR. we go evidence>judgment>synthesis"* — concept vocabulary harvested at evidence, adjudicated at judgment — ledger:1993-2042 | §2.4's deferral (#8, second half); `CLAUDE.md` §6's two sentences | **STANDS**; scope question open by design (§6 below) |
| 25 | 08-27 | medical model IN; four taxonomies are user-selectable browsing lenses — ledger:1926-1954 · `base.sources` is a TARGET registry — ledger:1956-1989 · relevance is adjudicated at collection (Part 15.6) · *"yes, we need parent columns"* (Part 16.7) | the "pure log" reading; the sources-duplication finding | **STANDS** (all four) |
| 26 | 08-27 (fresh) | `base_building` is three levels — building type · room type · construction element — *"are what I wanted for that table"*; `items` is none of them — ledger:2046-2077 | closes C-1: the note never reached `items` | **STANDS** |
| 27 | 08-27 (fresh) | *"we have multiple taxonomies. respect that. base_taxonomy_icf, base_taxonomy_medical etc"* — ledger:2081-2114 | #11's noun `icf_demands` | **STANDS** |
| 28 | 08-27 (fresh) | *"yeah use underscore then"* — separator is `_`, full-word namespaces — ledger:2117-2125 | the dotted grammar; the `[:3]` prefix proposal | **STANDS** |

## 2. THE SURVIVING SET (owner rulings operative now)

R1 · R2 · R8-substance (axis retired as identifier; descriptive use free; seven register
identifiers; rename-then-register) · R7 · §2.1 rule 5 · §2.2 pointer discipline · §2.3 clue store ·
§2.4 **cross-product frame only** · scratchpad commits · **six stages** · anti-fold ·
AMB/WHEEL + fan-out · three cross-reference junctions · canonical-parameter key + `items` as Part-4
rollup · rename-with-register-entry · `<stage>_items` naming + fan-out/fan-in (evidence→judgment
**1:N**) · "the rename creates the spine" · E-08 bar · note = thought document · adoptions #1, #2 ·
non-adoptions #3, #4 · harvest-at-evidence/adjudicate-at-judgment · browsing lenses (medical in) ·
target registry · relevance-at-collection · parent columns · `base_building` three levels ·
`base_taxonomy_*` parallel names · underscore separator.

**Dead:** five stages (twice over) · `icf_demands` as the noun · evidence→judgment 1:1 ·
`(item × population)` spec grain · `MOB` · §2.4's deferral-to-synthesis · "axis" as identifier ·
`ren_items`/`render_manifest` · the two 08-25 commissioning supersessions (spent).

---

## 3. C-1 and C-2 — now owner-resolved; the resolutions verified

**C-1 (`items`).** The fresh ruling (ledger:2046-2077) settles it the way this audit's own reading
was heading: the note's `base.building` member never reached `items`. Verified against the DB:
`A-03 = "Acoustic Door (STC ≥35) at All Sensitive Space Boundaries"` is a design provision *about*
a door, not a door; `rooms` holds 17 rows and every code the entry cites (`R-KIT`, `R-ENT`, `R-BA`,
`R-WC`, `R-BED`, `R-COR`) exists; `items` is 93 rows; `items.category` is bare letters (A–K, 10
values, no J) with no name column — the entry's claims reproduce exactly. Independently, the note
could never have superseded #15: it is a thought document (#20), and the on-contact adoptions were
itemised (#21-23) with `base.building` not among them. **#15 stands unamended; correctly recorded.**

**C-2 (the ICF layer's name).** Before the fresh ruling, the correct answer was "the note renames
nothing" — thought-document status plus the naming grammar being explicitly *"not ruled"*
(ledger:1914-1916). The owner's live statement now rules the name **against** `icf_demands`, and
the ledger records the supersession on contact without arguing it (ledger:2093-2095) — rule 0
executed correctly in form. The recording's *content* has one real defect (M1, §4a).

---

## 4. Audit of the three fresh recordings (ledger:2046-2125)

### (a) "§R8's substance survives in full… remain exactly as ruled" — HALF RIGHT, and the half that is wrong matters

**The register half checks out.** The seven entries (`axes`, `axis_code`, `item_axis_links`,
`population_axis_map`, `access_need_axis_map`, `serves_axes`, `attaches_axes`, ledger:2100-2102)
name **what is retired, not what replaces it** — verified against the 08-26 RULE's own
matcher-derived list (ledger:1403-1406) and `governance/retired-vocabulary.yaml`'s entry shape
(entries carry `retired_by`/`replacement` fields; the retired token is the key). A replacement-noun
change cannot touch them. Rename-then-register (admission test 2) is also noun-independent.
**Claim (a) holds for the seven entries.**

**M1 (MAJOR) — but "survives in full… exactly as ruled" overclaims.** The 08-25 ruling did not
select one noun; it selected a **derived family**: *"`icf_demands` (`icf_demands.demand_code`, and
correspondingly `item_demand_links`, `population_demand_map`, `access_need_demand_map`,
`slugs.serves_demands`, `situations.attaches_demands`)"* (ledger:1099-1101). The owner's new words
supply exactly one name — `base_taxonomy_icf` — and say nothing about the column or the five
companion objects. With the root noun superseded, `demand_code` / `item_demand_links` / etc. are
**orphaned, not surviving**: they were derived from a name that no longer exists. The fresh entry
(2081-2114) neither carries them forward nor flags them reopened. A session executing §R8 tomorrow
reads "only the replacement noun changes" and has no ruled name for six of the seven objects being
renamed. **The entry must mark the companion names as reopened (owner-owed or derivation-owed),
or the rename migration will invent them silently.**

### (b) The "etc" expansion to `base_taxonomy_identity` / `base_taxonomy_needs` — FAIR READING, unlabeled

The owner's own architecture note enumerates all four members verbatim: `base.taxonomy_medical`,
`base.taxonomy_identity`, `base.taxonomy_icf`, `base.taxonomy_needs` (owner-notes, Verbatim
section). *"base_taxonomy_icf, base_taxonomy_medical etc"* names two of the four and closes with
"etc"; the only list in evidence for "etc" to complete is the owner's own, and the underscore is
separately ruled (#28). **Completion, not invention** — this is not the 531-row-table class of
fabrication. **DEFECT (D1):** the two completed rows commit renames of two live tables
(`populations`, 23 rows, `population_code` carrying 7 inbound FKs; `access_needs`, 17) on the
strength of "etc", and the table at ledger:2088-2092 presents all four rows flatly under the owner
banner. Post-A4-B3 discipline requires the two inferred rows be labeled *completed from the note's
enumeration* — one clause would do it.

### (c) "'Respect that' is a bar on folding" — DEFENSIBLE IMPLICATURE, but the generalisation is the expansion

The reading itself survives attack: *"we have multiple taxonomies. respect that"* — folding two
taxonomies into one is failing to respect that there are multiple; the anti-fold is a natural
entailment, not an import. And the operative bar does not depend on this reading at all: the 08-25
anti-fold ruling (#11, ledger:1136) was never superseded and carries the measured b/d-vs-e
justification. **DEFECT (D2), two parts:** (i) the entry states the reading as a bolded section of
the ruling (ledger:2104) rather than as a reading — the safe citation was the standing 08-25 RULE,
which the entry only offers as "consistent with"; (ii) the ACTION generalises to *"Do not fold
**any** taxonomy into another"* (ledger:2112), which exceeds both texts — the 08-25 ruling barred
one specific fold (demand layer ↛ `access_needs`), and "respect that" supports pairwise separation
only by the same implicature now doing double duty. Probably what the owner means; not yet what
the owner said. Mark it derived.

**One more in the same batch — D3 (DEFECT):** the `base_building` ACTION reads *"Create three
tables, not one"* (ledger:2073) while the owner's quote says the three levels *"are what I wanted
for **that table**"* — singular. Three tables is likely the right normalisation, but it inverts the
quoted word without recording why. Same shape as A4-B3, caught here at the ACTION clause.

---

## 5. Audit of my caller's earlier recording (the standing task)

### Attribution expansion — did A4-B3 repeat?

The A4-B3 instance itself was properly caught and recorded (ledger:1779-1786; `CLAUDE.md` now
labels the KEY SHAPES as *"not the owner's words"*). But the pattern **partially recurred in the
three post-lesson RULEs written the same day**:

- **M5 (MAJOR) — the harvest RULE (ledger:1993-2042).** The overrule sentence is firm; the
  mechanism sentence is hedged — *"evidence is **probably** working by doing more cursory scans"* —
  yet the RULE headline states the mechanism categorically ("HARVESTED at evidence and ADJUDICATED
  at judgment"), and the entry embeds pure agent design under the owner banner with no derived
  label: the `observed_terms` / `term_adjudications` DDL (mirrored from Part 16.4),
  "saturation becomes the stopping rule", and the seed-problem argument. The quotes are present, so
  a careful reader can see the hedge — but A4-B3's remedy was *labeling*, and these are unlabeled.
- **D4 (DEFECT) — the browsing-lens RULE (ledger:1926-1954).** The owner said two sentences; the
  "four views of one substrate", the CRPD Art 4.3 resolution of the DG-NON objection, and the
  crossing-maps structural consequence are agent doctrine-work under the ruling banner, unlabeled.
- **D8 (DEFECT) — item #1 RULE ACTION (1)** (ledger:1866-1868) proposes a registered check
  justified as "so the ruling cannot regress silently" — an argument about the apparatus, which §1
  explicitly rejects; the book-facing harm (a silent UNIQUE would abolish the ruled fan-out and the
  dissent contest, corrupting future syntheses) is available and unstated. Same class as A4's
  finding 7, repeated after it.

### Rulings recorded as superseded that were NOT

**None found.** I attacked every "supersedes" claim in the ledger from 08-24 on: five→six stages
(both directions recorded, ledger:1010, 1451), 1:1→1:N (ledger:1841, resting explicitly on the
adoption instruction, not the note's status — correct), `icf_demands`→`base_taxonomy_icf`
(ledger:2093), §2.4's deferral (ledger:1994), the `(item × population)` grain (ledger:1233-1235),
`MOB` (ledger:1291). Each supersession has a live owner statement behind it and none strikes more
than the statement touches — with the single overclaim being M1's "survives in full" (which is the
inverse error: preserving too much, not superseding too much).

### Rulings MISSED superseding, and stale operative surfaces

- **M2 (MAJOR) — `CLAUDE.md` was not swept after adoptions #1/#2 and the harvest overrule.** The
  file every session loads currently asserts, against the three newest rulings: *"the
  evidence→judgment shape is **reopened**"* (`CLAUDE.md:56` — closed at ledger:1861);
  *"`judgment_items` is a NEW table, not a rename"* (`CLAUDE.md:66` — refuted at ledger:1857-1859,
  1888: `source_value_extractions` re-homed, "no new table and no new key"); the stage table gives
  evidence collection "verification and **extraction**" (`CLAUDE.md` pipeline table — extraction is
  now judgment's, ledger:1888); and §6 still carries *"applicability is an OUTPUT of synthesis"*
  and *"Zero `item_population_links`… correct pre-synthesis state"* (`CLAUDE.md:426,431` — superseded
  per ledger:2035-2037, where the correction is flagged owed but is not done). Four stale doctrine
  points on the highest-traffic surface.
- **M3 (MAJOR) — #14 vs #16, unreconciled.** The 08-25 ruling keys a specification *"from a
  judgment item"* (ledger:1229); the six-stage spine has specification consuming
  **synthesis-items** through `spe_synthesis_links` (ledger:1455-1462, 1545-1551), and the
  canonical-parameter ACTION still ships the junctions *"unchanged from the 2026-08-25 ruling"*
  (ledger:1362-1363). No entry records whether keying-from-judgment is superseded by the
  interposed synthesis stage or survives as the key while the junction carries lineage. A P1.0
  implementer meets both with equal authority.
- **M4 (MAJOR — REPAIRED MID-AUDIT, one residual) — the owner-notes transcription header re-armed
  the promotion.** As committed at `2bda17b` (09:34) the Status paragraph quoted *"just a
  proposal"* and in the same breath asserted *"per `CLAUDE.md` rule 0 its rulings supersede prior
  records on contact"* — three hours after the retraction (`15fc1b6`, 06:20). While this audit
  ran, the header was rewritten: Status now opens *"It is NOT a governing document"*, carries the
  adoption/non-adoption table with each adopted item resting *"on that instruction rather than on
  the note"*, and records the correction rather than overwriting it — the right shape. **Residual
  (DEFECT):** the Provenance sentence at `owner-notes:5` still reads *"it is now the governing
  statement on the pipeline's shape"* — the very phrase the correction block below it names as the
  first version's error — so the file contradicts itself in its opening paragraph.
- **B1 (BLOCKER — REPAIRED MID-AUDIT, residuals remain) — `RENAME-MAP.md` directed a rename
  against a recorded owner refusal.** As committed at `fa2dc51` (09:21), `RENAME-MAP.md:23`
  (*"Rule 0 makes the architecture note the latest statement"*) and the original §2 (*"The note
  wins on rule 0"*) re-homed `source_locators` → *"`base.clues` — SUBSTRATE"* — **after** item #3
  was recorded NOT adopted (ledger:1911, commit `9177084`, 06:48) and after the thought-document
  demotion (06:20). While this audit ran, a CORRECTED block landed (`RENAME-MAP.md:36-52`)
  retracting the premise, marking #1/#2 RULED and #3 NOT ADOPTED, and recording what executing the
  original premise would have done (reversing the `DR-2026-08-06` wall). **The repair is
  substantively right.** Residuals, DEFECT-level: `RENAME-MAP.md:23-24` still states the false
  premise uncorrected above the correction; §3's C-1/C-2/C-3 (`:56-69`) are still posed as open
  conflicts though all three are now owner-ruled (ledger:2046-2125), and `:98` still says
  *"RE-DERIVE the map under the architecture note"* where the governing basis is now the
  adoption record plus the three fresh rulings.
- **D5 (DEFECT) —** `WALKABILITY-PLAN.md:2110` (15.3) and `:2184-2186` (15.6) still cite §2.4's
  *"applicability is an OUTPUT of synthesis"* as live authority; Part 16.6 recorded the overrule
  but only 16.5's denominator note reached back into Part 15. 15.6's relevance/applicability table
  now has the wrong stage in its second row (synthesis → judgment).
- **D6 (DEFECT) —** `WALKABILITY-PLAN.md` Part 14.1 (*"Q1 STAYS OPEN"*, ~:1870-1885) is
  contradicted by ledger:1861 (*"Q1 is CLOSED"*); correct at 06:20, stale since 06:48, unflagged.
- **D7 (DEFECT) —** the fan-out RULE's *"pending **synthesis** re-derivation"* (ledger:1296-1299)
  and the AMB/WHEEL rationale citing §2.4 now point at a superseded locus; re-derivation happens at
  judgment under #24. Unrecorded ripple, cheap to note.

### The scoping question — "overrule Aug 24 DR" read as scoped to §2.4's deferral

**Defensible — and on the evidence, compelled. This is not narrowing to protect a liked rule.**

1. **Rule 0's own trigger is scope-bearing**: a live statement supersedes every prior record *"it
   touches."* What it touches is fixed by its content, and the second sentence — *"we go
   evidence>judgment>synthesis"* — states what is being overruled: **where adjudication sits in the
   stage order**. Inside DR-2026-08-24, only §2.4's deferral is about that.
2. **The whole-DR reading is a reductio.** It would strike R8 (axis retirement — which the owner
   re-affirmed 08-25, 08-26 *and again today* via `base_taxonomy_icf` replacing only the
   replacement noun), R1 (the correction of a fabricated attribution), §2.3 (whose clue-store
   treatment the owner re-touched today by *refusing* item #3), and §2.1 — whose content is the
   owner's own quoted words. One sentence cannot coherently un-say four unrelated rulings the same
   owner kept re-affirming through the same week. The narrow reading is the only one consistent
   with the rest of the record.
3. **The extension to population applicability is textually grounded, not smuggled.** I attacked
   ACTION (1)'s claim that *"the crossing is judgment's output"* as possibly exceeding an
   aporia about *concepts* — and it survived: §2.4's own deferral sentence names the deferred
   object as *"cross-referencing against our **populations/access needs/ICFs** … define these
   connections."* Overruling the deferral moves exactly those connections.
4. **The remaining fault is completeness, not bias (D9, DEFECT).** The SCOPE note
   (ledger:2040-2042) names only §2.1 as surviving. A scoped supersession of a multi-ruling DR
   should state the **full survival set** — R1, R2, R7, R8, §2.1, §2.2's discipline, §2.3, and
   §2.4's own cross-product half — precisely so the next session cannot run the whole-DR reading.
   And seeking owner confirmation is the right closure: determining scope is *reading* a ruling,
   not *weighing* paperwork against it.

---

## 6. What I attacked and could NOT break

- **Every "supersedes" claim in the ledger 08-24→08-27**: each rests on a quoted live owner
  statement; no supersession strikes more than its statement touches (M1 is the inverse defect).
- **Quote fidelity**: every owner quote I cross-checked is byte-identical across its DR, ledger,
  session-record and `CLAUDE.md` appearances (R8's four sentences, §2.1-2.4, the six-stage
  formulation, the cardinality sentence, the overrule, the three fresh quotes).
- **The append-only discipline**: the ledger corrects only by appending; the four correction
  passes name their own errors including a rule-0 violation, and the A4-B3 attribution expansion
  was caught, recorded, and repaired on `CLAUDE.md` with derived-parts labels.
- **The fresh C-1 recording's measurements**: A-03's name, all six cited room codes, 93 items,
  17 rooms, bare-letter categories — all reproduced read-only.
- **The 1:N recording's provenance**: it explicitly rests on the adoption instruction, not the
  note's status (ledger:1843-1845) — exactly right after the thought-document demotion.
- **The register-half of claim (a)**: seven retired-side entries genuinely noun-independent.
- **The "etc" completion's source**: the four-member list is the owner's own verbatim enumeration.

## 7. Findings ranked

| rank | id | finding | where |
|---|---|---|---|
| BLOCKER | B1 | RENAME-MAP declares "the note wins on rule 0" and re-homes `source_locators` to substrate **after** the owner refused exactly that (item #3) and demoted the note | `RENAME-MAP.md:23,36,§2`; ledger:1911; commits 15fc1b6/9177084/fa2dc51 |
| MAJOR | M1 | "§R8's substance survives in full / only the noun changes" leaves six companion replacement names (`demand_code`, `item_demand_links`…) orphaned and unflagged | ledger:2095-2102 vs 1099-1101 |
| MAJOR | M2 | `CLAUDE.md` stale on four points against adoptions #1/#2 and the overrule | `CLAUDE.md:56,66`, pipeline table, `:426,431` |
| MAJOR | M3 | #14 (spec keys from judgment item) vs #16 (spec consumes synthesis-items) — no reconciliation recorded | ledger:1229 vs 1455-1462, 1362 |
| MAJOR | M4 | owner-notes header asserts rule-0 supersession-on-contact for a document the owner called a proposal | `references/owner-notes/2026-08-27-architecture-note.md` Status |
| MAJOR | M5 | harvest RULE: hedged owner mechanism ("probably") stated categorically; unlabeled agent design (two-table DDL, saturation rule) under owner banner | ledger:1993-2042 |
| DEFECT | D1 | "etc"-completed taxonomy rows unlabeled as completion | ledger:2088-2092 |
| DEFECT | D2 | "respect that = bar on folding" stated as ruling content; generalised to all pairwise folds beyond both texts | ledger:2104-2112 |
| DEFECT | D3 | "Create three tables, not one" inverts the owner's singular "that table" without recording why | ledger:2073 |
| DEFECT | D4 | browsing-lens RULE: CRPD/DG-NON resolution is agent doctrine-work under owner banner | ledger:1926-1954 |
| DEFECT | D5 | WALKABILITY 15.3/15.6 still cite §2.4's superseded deferral as live | `WALKABILITY-PLAN.md:2110,2184-2186` |
| DEFECT | D6 | Part 14.1 "Q1 STAYS OPEN" vs ledger "Q1 is CLOSED" | `WALKABILITY-PLAN.md` 14.1; ledger:1861 |
| DEFECT | D7 | fan-out's "pending synthesis re-derivation" now points at a superseded locus | ledger:1296-1299 |
| DEFECT | D8 | item #1 ACTION's check justified apparatus-first, §1 burden unpaid in book terms | ledger:1866-1868 |
| DEFECT | D9 | overrule SCOPE note names only §2.1 surviving; full survival set unstated | ledger:2040-2042 |

---

**DIGEST**
1. Surviving set stated (§2); every ledger supersession 08-24→08-27 is backed by a live quote — none over-struck; C-1 and C-2 now owner-resolved and the resolutions correctly recorded in substance.
2. BLOCKER: RENAME-MAP still says "the note wins on rule 0" and re-homes clues to substrate — written after the owner refused item #3 and demoted the note; re-derive it before any rename migration.
3. Fresh recordings: (a) register-half true, but "survives in full" orphans six companion names (M1); (b) "etc"→identity/needs is fair completion of the owner's own list, unlabeled (D1); (c) anti-fold reading defensible but the all-pairwise generalisation exceeds the text (D2).
4. Attribution expansion partially recurred post-A4-B3 in the harvest and lens RULEs (unlabeled agent design under owner banners, M5/D4); `CLAUDE.md` is stale on four points against the three newest rulings (M2); #14-vs-#16 spec keying is an unrecorded conflict (M3).
5. The §2.4-only scoping of "overrule Aug 24 DR" is defensible and compelled by reductio (whole-DR would strike rulings the owner re-affirmed this same day); the defect is only that the SCOPE note doesn't enumerate the full survival set (D9).
