# T-102 design — the mobility family decomposed by device

_Written 2026-11-12 by an Opus-class designer under the owner's instruction "Opus to write design files that must be written first". Plan document: it changes no script, schema, row or ruling, and it **decides no taxonomy**: every code, name and edge below is **PROPOSED (owner confirms)** through the report of section 10, which the T-102 executor appends to the ledger before any row is written. Every count is a command; re-run it. Canadian English._

## 0. Verdict

**Keep `MOB` as the active parent and add three children by device, each with `parent_code = 'MOB'`:**

| Code | Display name (PROPOSED) | Whom it names |
|---|---|---|
| `WHEEL` | wheelchair users | people who use a wheelchair for some or all of their mobility, ambulatory wheelchair users included |
| `PROSTH` | people who use a lower-limb prosthesis | people with lower-limb loss or difference who walk or stand with a prosthesis |
| `WALKAID` | people who use walking aids | people who walk with a cane or stick, crutches, a walking frame or a rollator |

`MOB` is renamed from "disabled people with mobility needs; wheelchair users" (two things in one cell) to **"disabled people with mobility needs"**. A provision that names no device stays on `MOB`; a person with a mobility need who uses no aid is reached through `MOB` and the ICF d4 codes and access needs, with no child. Wheelchair drive stays in `device_class` and never becomes a code; impairment level (paraplegia, quadriplegia) stays out of the identity lens (medical lens when a source names it, ICF b-codes for the function it changes). `device_class` gains three values: `lower_limb_prosthesis`, `crutches`, `cane`. Five edges are reported as open, each with a recommendation: the 2026-08-25 `AMB`, scooter users, ambulatory wheelchair users, the prosthesis code's overlap with `LMB`, and people with a mobility need who use no aid.

**Confidence.** High (about 85%) that the children should be device-defined with drive and level as descriptors: the owner's words, the memo's evidence (no retrieved organisation is constituted by drive or by level) and rule 5 agree. Medium (about 65%) on `WHEEL` including ambulatory wheelchair users and on scooter users staying on the parent. Medium (about 60%) on restricting the prosthesis child to lower-limb prostheses. Low to medium (about 50%) on the display names of `PROSTH` and `WALKAID`: no organisation of prosthesis users or of walking-aid users was retrieved (memo §3.3), so those names are descriptive, not self-chosen, and the report says so.

**The owner's calls** (each answerable in one line, section 10): the three codes and their names; `MOB`'s new name; `AMB`; scooter users; the wording and placement of ambulatory wheelchair users; the scope of the prosthesis child; the proposed ICF crossings of the children. Already the owner's and not reopened: MOB decomposes by device (OD-14, third set); MOB stays as a parent and a provision naming no one under a mobility heading stays on it (OD-31, fourth set: the selected option names "the parent MOB with no child"); MOVE and VES are needs, LMB unchanged (OD-37).

## 1. The rulings this rests on (read, not restated)

| Ruling | Find it with | What it fixes for this design |
|---|---|---|
| 2026-08-25 split "to start", and its ratification | `grep -n -E 'MOB. is split\|mobility split is ratified' references/project-standards.md` | `WHEEL` is the owner's word; "to start" means extendable; grades never fanned out; `MOB` failed the design-equivalence test on ramp gradient; part-time wheelchair users and balance users owed |
| Thirteenth statement | `grep -n -F 'Owner statement 2026-11-12 (thirteenth)' references/project-standards.md` | MOB divides by aid, by drive, by level; a device or level division has one home |
| Fourteenth statement | `grep -n -F 'Owner statement 2026-11-12 (fourteenth)' references/project-standards.md` | disabled people's own organisations are the lens; record the provenance of a grouping; the owner chooses |
| OD-14 and OD-37 (third set) | `grep -n -F 'OD-14: MOB is decomposed by device' references/project-standards.md` | "wheelchair user, prosthetic device user, other mobility aids (or something like that)"; codes and edges proposed here and reported |
| OD-31 (fourth set) | `grep -n -F 'OD-31: a provision that names no one' references/project-standards.md` | the heading's group: under a mobility heading `MOB` with no child; under a general heading no identity, only ICF and needs; `ALL` leaves the identity lens |
| Second statement 2026-11-12 | `grep -n -F 'Owner statement 2026-11-12 (second)' references/project-standards.md` | commonality kept at an abstract level: a parent determination gathers its children |
| Design-equivalence exception (2026-07-23) | `grep -n -E '^RULE: Design-equivalence' references/project-standards.md` | a parent keys a determination only if its members' demands are not opposed |
| T-018 design | `tasks/T-018-design.md` | figures carry codes as live links in `extraction_lens_links`; a judged link replaces a carried one in one call |

The memo (`POPULATION-UMBRELLAS-MEMO.md`) is advisory and was not adopted wholesale (OD-37); this design uses its retrieved evidence, cited by row number of its table §2.2.

## 2. The codes (PROPOSED, owner confirms), with provenance

Written with T-025's identity verb (section 9). Category `mobility`; `is_compound` 0; status `active`.

**`MOB` — disabled people with mobility needs** (renamed; description unchanged: `select description from base_taxonomy_identity where identity_code='MOB'`). The parent of the device children; a figure that names no device stays here. Provenance: the owner's OD-31 option ("the parent MOB with no child"). It is a family for navigation and commonality, **not** a community: the memo found no organisation that names itself by "mobility" (§2.3 item 1), and the report says so. "Disabled people" is the identity-first form ENIL and UPIAS use (memo rows 13, 14); "mobility needs" keeps the registry's functional wording, which matches the ICF d4 chapter rather than claiming a community.

**`WHEEL` — wheelchair users.** Description: "People who use a wheelchair for some or all of their mobility, including ambulatory wheelchair users. The chair itself is recorded on the figure, never as a code." Provenance: the owner's own word, ratified 2026-08-25; United Spinal Association, "represents our nation's 5.5 million wheelchair users", membership "open to all wheelchair users" (memo row 16, https://unitedspinal.org/our-story/); its peer group Walking Rollers, "a space for ambulatory wheelchair users" (row 17). The description deliberately names no drive (test (5), section 8).

**`PROSTH` — people who use a lower-limb prosthesis.** Description: "People with lower-limb loss or limb difference who walk or stand with a prosthesis. Limb loss and limb difference as a community is `LMB`." Provenance: the owner's "prosthetic device user"; the nearest self-named community is the Amputee Coalition, "people who have limb loss and limb difference" (memo row 18, https://www.amputee-coalition.org/about-us/; not confirmed as led by disabled people). **No organisation of prosthesis users as such was retrieved** (memo §3.3): the name is descriptive, person-first after the Amputee Coalition's convention. Code string: not an initialism of any organisation.

**`WALKAID` — people who use walking aids.** Description: "People who walk with a cane or stick, crutches, a walking frame or a rollator for some or all of their mobility. The aid is recorded on the figure, never as a code." Provenance: the owner's "other mobility aids"; the registry's own access need `A-REACH` already names "cane/crutch users" among those it absorbs (`select absorbs from access_needs where need_code='A-REACH'`). **No organisation of walking-aid users was retrieved** (memo §3.3); descriptive name. The owner's "other mobility aids" is read as the aids used while walking; a scooter is the open edge E2.

**Not given a parent:** `SCI` (people with spinal cord injuries) and `LMB` (people with limb differences; upper-limb disabilities) stay as they are, category `mobility`, no parent (OD-37 leaves `LMB` unchanged; `SCI` is a condition community whose members include ambulatory people, memo §3.4, Martin Ginis et al.). Giving them `parent_code = 'MOB'` would make every `SCI` figure feed a `MOB` determination; that is a further owner question, not asked here.

## 3. The open edges (reported, not decided)

| Edge | Proposal (recommended) | Alternatives the owner may choose | Evidence |
|---|---|---|---|
| **E1 `AMB` (2026-08-25)** | **Not minted.** The device decomposition absorbs it: an ambulant person using an aid → `WALKAID` or `PROSTH`; an ambulant person using none → `MOB` with ICF d450 Walking / d455 Moving around and the needs `A-EFFORT` (cost little energy) and `A-STABLE` (hold the visual reference still; handrails, rest points) | (b) mint `AMB` — ambulatory disabled people — as a child of `MOB`, with `WALKAID` and `PROSTH` under it (a three-level family); (c) mint `AMB` beside the three children | The owner's 2026-11-12 answer widens the 2026-08-25 split to a division by device and "does not by itself say that the 2026-08-25 ruling is withdrawn" (third-set entry, item 1); so `AMB` is the owner's to retire. Memo §7 item 3: "ambulatory" appears as a community word only in "ambulatory wheelchair users" |
| **E2 scooter users** | **Stay on `MOB`**, with `device_class = 'scooter'` (the value exists) and no child | (b) `WHEEL` (the wheeled-device family: Koontz et al. 2010 and D'Souza et al. 2010 study wheelchairs and scooters together, and turning and floor space depend on the device's footprint); (c) `WALKAID` (the owner's "other mobility aids"; many scooter users walk); (d) a child of their own | Jang et al. 2019: scooter users experience "liminality", partly from their "ambulatory status" (memo §3.4). Placing them under `WHEEL` names them by a device they do not use; under `WALKAID` puts a seated, wheeled footprint into a walking-aid determination |
| **E3 ambulatory and part-time wheelchair users** | **Inside `WHEEL`** (its description says "some or all of their mobility"); the community's own wording "ambulatory wheelchair users" is used in a gap or a note; a figure whose text names both a chair and a walking aid links `WHEEL` and `WALKAID` | (b) a child of their own (code `AWU`, "ambulatory wheelchair users"); (c) the withdrawn OD-14 resolution's interim: both codes with a stated condition | United Spinal opens membership to "all wheelchair users" and hosts Walking Rollers within it (memo rows 16, 17); first-person accounts of stigma ("faking") (memo §2.3 item 4). The 2026-08-25 entry left their wording to the owner |
| **E4 `PROSTH` and `LMB`** | **`PROSTH` is lower-limb only, parent `MOB`.** Upper-limb prosthesis users stay with `LMB` and the needs `A-REACH` / `A-PRECISION` and ICF d440 Fine hand use / d445 Hand and arm use; no `device_class` value for an upper-limb prosthesis (it is not a mobility device). A figure is linked to `LMB` only where its words name limb loss or limb difference as the group; to `PROSTH` where they name a prosthesis | (b) `PROSTH` for any prosthesis; (c) `PROSTH` with parent `LMB` instead of `MOB` (a registry row has one parent) | The owner said "prosthetic device user" without qualification; OD-37 leaves `LMB` (itself two things in one cell, memo §6) unchanged. Today no `MOB` figure names a prosthesis (the heuristic of section 6) |
| **E5 a mobility need with no aid** | **No child.** `MOB` plus the ICF d4 codes and the needs `A-EFFORT`, `A-STABLE`, `A-REACH` (be physically reachable) | a child, only if the owner names a self-named community | none retrieved (memo §2.3) |

## 4. Descriptors, one home each (rule 5)

| Division (thirteenth statement) | Home | Never |
|---|---|---|
| aid type: wheelchair / prosthesis / walking aid | the child code | a `device_class` value standing in for the person's group |
| wheelchair drive and frame: manual self-propelled, attendant-propelled, power, bariatric | `source_value_extractions.device_class` (existing values: `manual_self_propelled`, `manual_attendant`, `power_chair`, `bariatric_manual`, `bariatric_power`) | a code (`POWER`, `MANUAL`) |
| walking aid kind | `device_class`: existing `walker_rollator`; **new** `crutches`, `cane` (a cane or walking stick) | a code |
| prosthesis | `device_class`: **new** `lower_limb_prosthesis` | — |
| scooter | `device_class = 'scooter'` (existing) | a code, unless the owner chooses E2 (d) |
| several devices in one figure | `device_class = 'mixed'` (existing) | — |
| paraplegia / quadriplegia (tetraplegia) | the medical lens when a source names it and `base_taxonomy_medical` holds a code (T-103 fills it; empty today: `select count(*) from base_taxonomy_medical`); ICF b-codes for the function it changes (b730 Muscle power functions, b710 Mobility of joint functions are in `base_icf`); the participants' words in `root_population_note` | an identity code; a description of a mobility-family code |

The vocabulary T-055 adds is exactly `lower_limb_prosthesis`, `crutches`, `cane`, kept as the column's CHECK (read by `dbcore.check_values`), not a table (section 12, alternative F).

**The one consistency a reviewer checks.** The child and the device can disagree only by error. The family of each value, for the pull request's review query and nowhere in code: `WHEEL` ← `manual_self_propelled`, `manual_attendant`, `power_chair`, `bariatric_manual`, `bariatric_power`; `WALKAID` ← `walker_rollator`, `crutches`, `cane`; `PROSTH` ← `lower_limb_prosthesis`; `MOB` ← `scooter` (under E2's proposal); any ← `mixed`, `not_device_scoped`, NULL.

## 5. Commonality at the parent (T-055 builds it)

A determination keyed on `MOB` gathers figures linked to `MOB` or to any code whose `parent_code` chain reaches it (`tasks/T-018-design.md` §4, the recursive `family` CTE). A child's determination gathers only that child. A `MOB` determination is written only for a parameter that passes the design-equivalence test of 2026-07-23 (T-110): for ramp gradient it does not (2026-08-25: manual wheelchair users and ambulant people with fatigue want opposed gradients), so ramp gradient is determined per child.

## 6. Carrying the rows filed under `MOB`

**What is there** (re-run; do not trust): figures linked to `MOB` after T-018's carry: `select count(*) from v_live_lens_links where identity_code='MOB'`; their `device_class`: `select x.device_class, count(*) from v_live_lens_links k join source_value_extractions x using(extraction_id) where k.identity_code='MOB' group by 1`; grades: `select count(*) from evidence_population_match where target_population='MOB'`; headings of the rows: `select x.source_section, count(*) from v_live_lens_links k join source_value_extractions x using(extraction_id) where k.identity_code='MOB' group by 1 order by 2 desc`. What each row names, by a keyword heuristic in the P1+P2+P3 languages (a row may name several; a pointer for the judge, never the judgment):

```
python3 -I - "$SCRATCH/s.db" <<'PY'
import sqlite3, sys, re, collections
c = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
D = {"wheelchair": r"wheel ?chair|rollstuhl|fauteuil roulant|silla de ruedas|rullstol|rullestol|kørestol|pyörätuoli|rolstoel|sedia a rotelle|carrozzina|cadeira de rodas|車いす|車椅子|휠체어|轮椅",
     "power/scooter": r"power(ed)? (wheel)?chair|electric (wheel)?chair|elektrorollstuhl|scooter|電動車いす|전동휠체어|电动轮椅",
     "manual": r"manual (wheel)?chair|self-propel|pushrim|handrim|attendant-propel",
     "walking aid": r"walking aid|walking frame|walker|rollator|crutch|\bcanes?\b|walking stick|gehhilfe|béquille|déambulateur|muleta|andador|kryck|krykke|rollaattori|stampella|bengala|杖|지팡이|拐杖",
     "prosthesis/amputation": r"prosthe|amput|prothes|protes|義足|의족|假肢",
     "level": r"parapleg|tetrapleg|quadri?pleg|quadraplegi"}
rows = c.execute("select x.extraction_id, coalesce(x.claim_text,'')||' '||coalesce(x.source_section,'')||' '||coalesce(x.root_population_note,'') from v_live_lens_links k join source_value_extractions x using(extraction_id) where k.identity_code='MOB'").fetchall()
cnt = collections.Counter(k for _, t in rows for k, p in D.items() if re.search(p, t, re.I))
print("EXAMINED:", len(rows)); print(dict(cnt)); print("names none:", sum(1 for _, t in rows if not any(re.search(p, t, re.I) for p in D.values())))
PY
```

On 2026-11-12, run against the canonical database's `identity_code` column (before T-018), most rows named no division and most of the rest named a wheelchair with the drive unstated; none named a prosthesis (DECISION-CLOSURE §5 records the run). So the held evidence places most rows on `MOB` or under a general heading, and the rest mostly on `WHEEL`.

**The rule, row by row, by judgment (the executor reads each figure's own words, and the source's saved text where the heading is not in the row):**

| The figure's own words (or, for a study, its participants) name | Action | `basis` of the new link |
|---|---|---|
| wheelchair users (any drive) | `add-lens-link --identity WHEEL`; drive, if stated and `device_class` is NULL, by `amend-extraction --field device_class` (T-055 makes it amendable); `retire-lens-link` the `MOB` link, reason "carried to WHEEL; MOB reaches it by parent_code" | `named_in_text` or `study_participants` |
| a lower-limb prosthesis | `PROSTH`, `device_class lower_limb_prosthesis`; retire `MOB` | same |
| a cane, crutches, a frame or a rollator | `WALKAID`, the matching `device_class`; retire `MOB` | same |
| several of these | one link per child; `device_class mixed`; retire `MOB` | same |
| ambulatory or part-time wheelchair users | `WHEEL`, and `WALKAID` if an aid is named (E3) | same |
| scooter users only | keep `MOB` (judged link replaces the carried one); `device_class scooter` (E2) | `named_in_text` |
| amputees or limb difference, no prosthesis | `LMB`; retire `MOB` only if the words name no mobility group; list the row in the pull request (E4) | `named_in_text` |
| a mobility group, no device ("people with reduced mobility") | keep `MOB`, judged | `named_in_text` |
| no one; the heading names a mobility group | keep `MOB`, judged | `heading`, the heading's words |
| no one; the heading names no group or "persons with disabilities" | retire `MOB` **after** the figure has a live ICF or need link (T-106 fills them; the executor may add one where the words name the function or need). If none can be warranted, keep the carried `MOB` link and list the row: a figure is never left with no lens | — |
| `ALL` | never; universality is `design_scale` (OD-31) | — |

`add-lens-link` on a code whose live link is `carried` replaces it in one call (T-018 design §6), so a `MOB` row that stays on `MOB` gets its judged warrant without a second link.

**Grades are never fanned out** (2026-08-25: "Not fanned out, ever"). Every `MOB` grade stays as the parent-level grade, untouched; a new grade against a child is written with `add-population-match` only where the study's own participants are that child, naming them in `--study-population`. No grade is retired, so `evidence_population_match` needs no retirement column.

**The retired determinations.** `select specification_id, parameter_id, identity_code, design_scale, retired_at is not null from specifications` shows every determination keyed on `MOB`, all retired, most at `design_scale = 'universal'`. They are history and are not edited: their `specification_extraction_links` point at extraction ids, which do not change. They show the defect T-056 removes (a universal-scale determination keyed on an identity). New determinations are T-110's, keyed on a child where its figures are for that child.

## 7. What T-102 writes (one research batch, after T-018, T-025, T-055 merge)

Rows only, through the write path of CLAUDE.md §4 (scratch copy → `db.py` → `emit_batch_sql.py` → `emit_data_migration.py` → `migrate_db.py`); no schema migration, no code.

1. The report of section 10 appended to `references/project-standards.md`, **before any row**. If the owner's reply changes a code, a name or an edge, this design is corrected first, then the rows follow the correction.
2. `base_taxonomy_identity`: three children (T-025's add verb, `--parent MOB`, with the ledger pointer to the report's heading); `MOB`'s display name (T-025's amend verb, the replaced value recorded as that verb records it).
3. **PROPOSED (owner confirms) in the report, written only if confirmed:** the children's ICF crossings with `add-population-icf-link`, `--mapping-confidence moderate_contextual`, provenance "T-102 design and report": `WHEEL` → d465 Moving around using equipment, d420 Transferring oneself, d410 Changing basic body position; `PROSTH` → d450 Walking, d455 Moving around; `WALKAID` → d450 Walking, d465 Moving around using equipment. (The memo flags `MOB`'s nine `high_predictive` crossings as overstated; this design does not touch them.)
4. `extraction_lens_links`: the judged links and retirements of section 6.
5. `source_value_extractions.device_class`: where the figure's words state the device and the cell is NULL.
6. `evidence_population_match`: new child grades only as section 6 allows.

## 8. After-tests (on the migrated database; each was red or absent before)

1. The children exist with their parent and `MOB` stays active: `select identity_code, display_name, parent_code, status from base_taxonomy_identity where identity_code='MOB' or parent_code='MOB'` prints `MOB` active with the new name and the confirmed children with `parent_code = 'MOB'`.
2. The report precedes the rows: `grep -n -F "the mobility codes as designed (T-102)" references/project-standards.md` prints a line, and its commit precedes the data migration's (`git log --format=%H -1 -S "the mobility codes as designed (T-102)" -- references/project-standards.md` is an ancestor of the commit adding the `data_*` file).
3. **No figure still linked to `MOB` names a wheelchair, a prosthesis or a walking aid in its own words** — read through the link table, not the retired column (the task file's original query reads `identity_code`, which T-018 NULLs, so it would print 0 having examined nothing): `python3 -I -c "import sqlite3,re;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);P=re.compile(r'wheel ?chair|rollstuhl|fauteuil roulant|silla de ruedas|rullstol|pyörätuoli|rolstoel|carrozzina|cadeira de rodas|車いす|車椅子|휠체어|轮椅|prosthe|crutch|\\bcanes?\\b|walking (aid|frame|stick)|walker|rollator',re.I);R=c.execute(\"select coalesce(x.claim_text,'')||' '||coalesce(x.source_section,'') from v_live_lens_links k join source_value_extractions x using(extraction_id) where k.identity_code='MOB'\").fetchall();print('EXAMINED:',len(R));print(sum(1 for (t,) in R if P.search(t)))"` prints a non-zero `EXAMINED` and then 0, or a number equal to the rows the pull request lists with their reasons (a row that mentions a chair without naming its users, for example).
4. No grade was fanned out: `select count(*) from evidence_population_match where target_population='MOB'` is unchanged, and `select target_population, study_population from evidence_population_match where target_population in (select identity_code from base_taxonomy_identity where parent_code='MOB')` shows each new grade's participants.
5. No division is held twice: `select identity_code, display_name, description from base_taxonomy_identity where identity_code='MOB' or parent_code='MOB'` contains none of `power`, `manual`, `parapleg`, `tetrapleg`, `quadri` (case-insensitive). (`SCI`'s description names levels of the condition; it is outside this family and reported, not changed.)
6. Every judged: `select count(*) from extraction_lens_links where identity_code in ('MOB','WHEEL','PROSTH','WALKAID') and basis='carried' and retired_at is null` prints 0, or the listed rows of section 6's last-but-one line.
7. No figure lost its lens: T-018's integrity case passes (`test_db_integrity`, the "every figure has a live lens link" case, `[✓]` with a non-zero subject).
8. Device and child agree: the review query of section 4, run in the pull request, lists no figure linked to a child whose `device_class` belongs to another child's family.

Plus the research gate (`research_batch_dod.py --session "$STEM"`) and `migration_reproducibility.py --deep`, as the task file says, each with its `EXAMINED:` line.

## 9. What T-102 needs from the tooling tasks (names fixed here)

- **T-018:** `add-lens-link --extraction-id N --identity C --basis {named_in_text,heading,study_participants} --basis-text "<words>"`, `retire-lens-link --link-id N --reason`, `v_live_lens_links`.
- **T-025:** an add verb for `base_taxonomy_identity` taking `--code --display-name --category --description --parent --ledger-pointer` and an amend of the display name taking `--code --display-name --ledger-pointer --reason`; the names are T-025's to choose (`add-identity`, `amend-identity` proposed). The ledger pointer is checked to occur once in the ledger; **the provenance of each code is held once, in the report of section 10** (the fourteenth statement's ACTION 2), which the pointer names. No provenance column is added: nothing would read it until render cites a community's source (T-037 may add one then).
- **T-055:** the three `device_class` values of section 4, exactly; `device_class` added to `amend-extraction`'s amendable fields (today it is not: `grep -n '_AMENDABLE_SVE_FIELDS =' -A3 scripts/db.py`), so that a stated drive or aid can be recorded on an existing figure; the parent gather of section 5.

## 10. The post-design OWNER REPORT (draft; the T-102 executor appends it, adjusted only for facts re-derived on the day, before any row is written)

Append to the end of `references/project-standards.md`, replacing `YYYY-MM-DD` with `date -u +%F`. It carries no status line. Do not append it from this design pass.

```
## Report YYYY-MM-DD — the mobility codes as designed (T-102)

A report to the owner by the session executing task T-102, before any row is written, as the owner's answer to OD-14 asks ("the exact codes and edges are settled by the design of T-102 and reported to the owner"). Design: `workplan/2026-11-12-bidirectional-pipeline/tasks/T-102-design.md`. **This is a report, not an owner statement, and it decides nothing.** Evidence about how disabled people organise is from `workplan/2026-11-12-bidirectional-pipeline/POPULATION-UMBRELLAS-MEMO.md` (pages retrieved 2026-11-12, an English-language sample; none is an admitted source).

**Proposed codes** (each in the identity registry, category mobility, active):

| Code | Name shown | Parent | Whom it names | Provenance |
|---|---|---|---|---|
| MOB | disabled people with mobility needs (was "disabled people with mobility needs; wheelchair users") | — | the family; a figure that names no device stays here | the owner's OD-31 answer ("the parent MOB with no child"); no organisation names itself by "mobility" (memo §2.3) |
| WHEEL | wheelchair users | MOB | people who use a wheelchair for some or all of their mobility, ambulatory wheelchair users included | the owner's word (2026-08-25); United Spinal Association, "all wheelchair users" (https://unitedspinal.org/our-story/); its peer group Walking Rollers, "ambulatory wheelchair users" |
| PROSTH | people who use a lower-limb prosthesis | MOB | people with lower-limb loss or difference who walk or stand with a prosthesis | the owner's "prosthetic device user"; nearest community: Amputee Coalition, "people who have limb loss and limb difference" (https://www.amputee-coalition.org/about-us/). No organisation of prosthesis users was found: the name is descriptive |
| WALKAID | people who use walking aids | MOB | people who walk with a cane or stick, crutches, a walking frame or a rollator | the owner's "other mobility aids"; no organisation of walking-aid users was found: the name is descriptive |

**Held as descriptors, never as codes.** Wheelchair drive and frame (manual self-propelled, attendant-propelled, power, bariatric) and the walking aid or prosthesis are recorded on each figure (device_class), which gains three values: lower_limb_prosthesis, crutches, cane. Paraplegia and quadriplegia go to the medical lens when a source names them, and to the ICF body-function codes for what they change; no organisation retrieved divides itself by drive or by level.

**Commonality.** A determination for MOB gathers its children; one for a child gathers only that child. MOB is used as a key only where its members' demands are not opposed (2026-07-23 test); ramp gradient is opposed (2026-08-25), so it is determined per child.

**Rows.** Each figure filed under MOB is judged by the users its own words, or its study's participants, name, and linked to the child it names; a figure naming no one stays on MOB under a mobility heading, and under a general heading carries only its ICF and access-need lenses (OD-31). Grades are never fanned out.

**Open edges, each with a recommendation:**
1. AMB (2026-08-25). Recommended: not minted; an ambulant person with an aid is WALKAID or PROSTH, without one is MOB with the ICF codes d450 Walking and d455 Moving around and the needs A-EFFORT and A-STABLE. Alternatives: AMB as a child of MOB above WALKAID and PROSTH; AMB beside the three.
2. Scooter users. Recommended: stay on MOB, with the scooter recorded on the figure. Alternatives: WHEEL; WALKAID; a child of their own. (Scooter users are described as between categories: Jang et al. 2019.)
3. Ambulatory and part-time wheelchair users. Recommended: inside WHEEL, named in their own words, "ambulatory wheelchair users"; a figure naming a chair and a walking aid carries WHEEL and WALKAID. Alternative: a child of their own.
4. PROSTH and LMB. Recommended: PROSTH covers lower-limb prostheses only, under MOB; upper-limb prosthesis users stay with LMB (people with limb differences; upper-limb disabilities), which is unchanged. Alternatives: PROSTH for any prosthesis; PROSTH under LMB.
5. A mobility need with no aid. Recommended: no child; MOB with the ICF codes and access needs.
6. Proposed ICF crossings (moderate_contextual): WHEEL to d465, d420, d410; PROSTH to d450, d455; WALKAID to d450, d465. Written only if confirmed.

**Answer in one line** (any part may be answered alone):
`T-102: codes as proposed` · `T-102: rename <code> to "<name>"` · `T-102: AMB not minted | AMB above WALKAID and PROSTH | AMB beside` · `T-102: scooter on MOB | WHEEL | WALKAID | own code` · `T-102: ambulatory wheelchair users in WHEEL | own code` · `T-102: PROSTH lower-limb only | any prosthesis | under LMB` · `T-102: ICF crossings as proposed | none`

Until the owner answers, the session writes the rows on the recommended options and lists in its pull request every row an alternative would place differently.

CONDITION: any session tagging, splitting or carrying the mobility identity before the owner answers this report.
ACTION: (1) Use the codes and edges above as proposals, not rulings. (2) If the owner's answer differs, correct the T-102 design first and re-place the listed rows.
DATE: YYYY-MM-DD — report by the T-102 session, not an owner statement.
```

**[ASSUMPTION, for the executor and the owner]** The report's last paragraph lets rows be written on the recommended options before the owner answers, with every row an alternative would move listed. If the owner wants rows to wait for the answer, the executor stops after appending the report; the task file's item 2 ("Write no row until it is appended") requires only the appending.

## 11. Caller sweep (prose; a research task changes no code)

For each of `MOB`, `WHEEL`, `PROSTH`, `WALKAID`, `AMB` and the old display string `disabled people with mobility needs; wheelchair users`:
`git grep -n -F -e "<value>" -- governance architecture CLAUDE.md references skills ':(exclude)references/project-standards.md' ':(exclude)references/search-log'`. Expected callers: `governance/population-taxonomy.md` (its list of identity codes and any sentence that calls `MOB` "superseded" or names `AMB`/`WHEEL` as the split), and the other governance files the grep for `MOB` lists (on 2026-11-12, `git grep -l -F MOB -- governance` named `functional-taxonomy.md`, `evidence-methodology.md`, `owner-browser.yaml` and several frozen armature records among others; judge each hit as caller or mention); no skill named `MOB` on that date (`git grep -l -F MOB -- skills` printed nothing); `references/` pages naming the old display string. A sentence the rows make false is corrected in the pull request if correcting it is not doctrine; a change to `governance/population-taxonomy.md` beyond a one-line pointer to the report is the owner's and is listed, not made.

## 12. Alternatives rejected

- **A. Retire `MOB` and key nothing on mobility (the memo's recommendation).** The owner decomposed `MOB` and, in OD-31, kept it as the parent.
- **B. `AMB` / `WHEEL` only (2026-08-25 as written).** Widened by the owner's answer; leaves prosthesis users and walking-aid users unnamed and puts ambulatory wheelchair users on both sides.
- **C. Codes for drive (`POWER`, `MANUAL`).** A second home of `device_class` (rule 5); no organisation retrieved is constituted by drive (memo §2.3 item 3).
- **D. Codes for level (`PARA`, `QUAD`).** Same; impairment level is a medical or body-function fact, and the spinal cord injury organisations retrieved do not divide by it.
- **E. Fan a row that names no one out to every child.** OD-31 sends it to the parent or to ICF and needs; fan-out would tag groups the text excludes.
- **F. `device_class` as a table with a foreign key.** More flexible, but a larger tooling change than T-055 is scoped for (T-055 stops if asked for it); three values are added by CHECK now, and the table remains a separate proposal.
- **G. `PROSTH` under `LMB`.** Keeps limb loss together but removes prosthesis users from the mobility family's gather, against the owner's decomposition of `MOB` by device. Offered to the owner as an alternative.
- **H. A provenance column on `base_taxonomy_identity`.** No reader yet; the report holds the provenance once and the ledger pointer names it.
