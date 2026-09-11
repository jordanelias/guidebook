# ADJUDICATION — the report D-0188 cites

**This file arrived a day after three records cited it.** `data/decisions/decision_register.yaml`,
`decisions/DR-2026-09-11-adjudication-delegated-medical-lens-enforced.md` and the `decisions` table
row for **D-0188** all list `scratchpad/pr-134-repository-orientation/ADJUDICATION.md` in
`decision_artifacts`, and the path did not resolve. The table row is inside a committed data
migration and is therefore immutable (`CLAUDE.md` rule 3), so the citation could only be repaired
forward, by making the artefact exist. It is the same defect class as rule 4's unswept callers: a
reference that does not resolve, in a record no gate reads.

## Provenance — this is a transcript extract, not a rewrite

Everything below the rule is the adjudicator's final message, **verbatim**. Source bytes:

    transcripts/harness_94859b50/subagents/2026-09-11T00-54-46_other_a382a8ba.jsonl
    sha256 f3b537826a18410e…   ·   message timestamp 2026-09-11T01:16:03.220Z   ·   agentId a382a8ba8d41f5424

Reproduce it:

```
python3 - <<'PY'
import json
p='transcripts/harness_94859b50/subagents/2026-09-11T00-54-46_other_a382a8ba.jsonl'
recs=[json.loads(l) for l in open(p) if l.strip()]
final=[r for r in recs if r['type']=='assistant'][-1]
print("\n".join(b['text'] for b in final['message']['content'] if b.get('type')=='text'))
PY
```

It was not paraphrased, because the alternative was writing an owner-delegated adjudication from
memory a day later — which is failure mode (c) with the payload sitting in the repository.

The adjudicator was read-only by construction (the brief's first line: *"WRITE NOTHING, EDIT NOTHING,
COMMIT NOTHING"*), so its entire output is this one message. That is rule 6's case exactly: a
read-only subagent writes nothing at all, and its workings live only in ephemeral container storage
until someone copies them out.

## What a reader arriving from D-0188 needs to know first

**This is a record, not a live instruction sheet.** Four of its rulings were executed, one was
overtaken within hours, and one was not built. Derive the state rather than trusting this list:

| Report | Ruling | State, and how to check it |
|---|---|---|
| §1.2 | Two crossing tables, `medical↔needs` derived not stored | Executed — `scripts/migrations/074_medical_lens_crossings.sql` |
| §1.4 | `base_taxonomy_medical` has no writer; that is a coverage bug, not a licence | Executed — `db.py add-medical`, `grep -n 'add-medical' scripts/db.py` |
| §1.3 | Guardrails, and what failure looks like | Executed as a check — `scripts/audit/medical_lens_integrity.py` |
| §1.1 | The 29-row vocabulary | **Not written.** `select count(*) from base_taxonomy_medical` |
| §1.1 | *"ICD-11 anchor (expected — retrieval decides)"* | Overtaken the same day, in the direction the report allowed for: the anchors became verifiable against WHO's own bytes rather than expected. See `ICD11-VERIFIED.md` and `ICD11-CORRESPONDENCE.md` |
| §2.3 | A `source_locators_integrity` gate | **Not built.** `grep -rn 'source_locators_integrity' governance/check-registry.yaml` returns nothing; the corruption was measured and recorded, not repaired |

The §1.1 vocabulary is the one that matters and the one still owed. Its own falsification test is
reader-facing and still applies: *"a diagnosis a real reader would search that reaches nothing and is
not in the deferred list."*

---

All evidence is in hand. Two facts changed my reading of the brief and I state them first; everything else follows.

---

# ADJUDICATION REPORT — 2026-09-11, under live owner delegation

## 0. The delegation, its record, and corrections to the brief

**Supersession recorded here, to be written by W0 before anything mechanical runs** (rule 0, second sentence; `CLAUDE.md:44-47`). Owner, 2026-09-11, verbatim: *"Fable 5.1 to adjudicate and resolve all items that are presented to me. Opus to execute in agonist-antagonist method. Ensure that medical gets filled out."* On contact this supersedes the Delegation clauses of `D-0170` (`decisions/DR-2026-08-27-four-taxonomies-are-browsing-lenses.md:39-43`), `D-0169`, `D-0182`, and `governance/decision-protocol.md:73-84` §2.4 items 2–3 **as applied to the items enumerated in this report and no further**. It does not amend the DG-NON list generally. Record: (a) an appended ledger entry in `references/project-standards.md` (CONDITION/ACTION/DATE form, as `:2745-2848`); (b) register row **D-0188** in `data/decisions/decision_register.yaml` (next after D-0187 at `:6256`), category D-DOCT, `delegation: DG-NON`, `delegation_rationale` naming the live statement; (c) the matching `decisions` table INSERT — the DB table is a live dual home (187 rows, D-0187 present; the 2026-08-27 precedent `data_20260827194239` wrote both and says so). Every ruling below becomes a register row `decided_by: <executing session> under owner delegation D-0188`.

**Corrections to the brief (five; one is the item "already wrong once"):**

1. **"Rows alone do not discharge lens-switching; crossings are the mechanism."** That was D-0170's mechanism on 2026-08-27. Two later owner rulings replaced it: D-0184 measured that traversal manufactures inference (`DR-2026-09-01-the-lens-is-a-column…:25-34`) and made the lens a column — render is `WHERE medical_code = ?`; D-0182's notes make the crossing maps the *authoring aid* that suggests the other lens codes for a row (`DR-2026-09-01-a-link-states-at-least-one…:42-48`). So: rows carrying `medical_code` are what switch; the crossings are still required — for populating those rows without inference, and for coverage measurement — but not as render traversal. The design in §1 is built on that.
2. **REF-00037 worked example.** The DB-keyspace REF-00037 *is* the wheelchair-biomechanics review: `_archived/working/evidence-migration/audit-remediation-batch-b.md:34-41` (REF-00037 = Rouvier 2022, PLoS One; REF-VERIFIED-003 marked superseded by it) and `_archived/scripts/migrations/012_baseline_2026-05-15.sql:1220-1221` (authors Rouvier, Louessard on REF-00037). The **title** is the wrong side, not the DOI. R9b reusing REF-00037 for that DOI is therefore correct; the fabrication hazard is a session copying bibliography from the stash, and mis-screening leads by a wrong title. Ruling in §2 is shaped by that.
3. **"36 embed a DOI that differs."** 36 titles embed a DOI; **31 differ, 5 agree** (query in §2). The 5 agreeing rows matter — they prove the keyspaces partially coincide, so the defect is per-row, not a shift.
4. **"Selftest C9 catches the drift."** C9 lives in `scripts/decision_capture.py:230-258`, not `run_checks.py --selftest` (which has C1–C5, `:576-653`); it checks only that every DR file is cited by *some* register row (a warning), never content. And **no generator exists**: commit `06ceda8` hand-wrote the eight DR files beside the register edit. The "GENERATED from its register row" header is a claim with no script behind it. Consequence: a new decision costs three hand-written homes (register, DR file, `decisions` INSERT); say so in D-0188's notes rather than pretend otherwise.
5. The `access_need_icf → access_need_icf_codes` rename D-0169 ruled was never executed; the live table is `access_need_icf`; none of the §R8 tokens (`axis_code`, `population_axis_map`, `AX-`) is in `governance/retired-vocabulary.yaml` (tokens at `:154-812`; none match). New tables may reference `axes(axis_code)` without tripping the advisory audit, but must be *named* in the ruled lens vocabulary (`references/project-standards.md:2475`).

The item "already wrong once today" was `scratchpad/pr-134-repository-orientation/ORDER-OF-WORK.md:97-100` ("`base_taxonomy_medical` stays empty; the medical lens is explicitly deferred") — withdrawn; it contradicted D-0170.

---

## ITEM 1 — THE MEDICAL LENS

### Ruling 1.1 — what the vocabulary is (29 rows), and its bound

**The set is derived, not coined:** (identity-lens diagnoses expanded to ICD-11 entity/block grain inside the two ratified umbrellas COM and BRAIN and the de-facto umbrellas MOVE, MH, NDV) ∪ (the diagnosis-level profiles and named deferred candidates of `governance/functional-taxonomy.md` §4 `:282-315`). Nothing else. Every row is an ICD-11 entity or block; the project coins no medical cluster (that is `CLAUDE.md` §6's umbrella rule applied to this lens, and the 2026-07-23 design-equivalence exception at `references/project-standards.md:563` says explicitly it "does NOT license coining further umbrellas"). Admission rule for any future row: an ICD-11 anchor **and** at least one crossing.

**Size defended:** 29, one screen, beside 23/17/17. Larger would be a nomenclature; smaller would strand a diagnosis-thinking reader inside an umbrella they do not use (a POTS reader does not search "complex conditions").

Codes: `MD-` prefix, letters only, parallel to `AX-`/`A-`; no digit can ever match the `\b[A-Z]-[0-9]{2}\b` item-code trap (`CLAUDE.md:336`). `display_name` = community-preferred clinical name where doctrine states one (§4: "display ME/CFS per community preference"), else the ICD-11 title; `description` = definitional, never a restatement of the identity row's description (rule 5).

| code | display_name | ICD-11 anchor (expected — **retrieval decides**, see 1.4) | identity crossing (relationship) | icf crossings (role / confidence) |
|---|---|---|---|---|
| MD-AUTISM | Autism spectrum disorder | 6A02 | AUT `identity_first`; NDV `member_of` | SPR P/mod; ARO S; COM-E S |
| MD-ADHD | Attention deficit hyperactivity disorder | 6A05 | ADHD `names`; NDV `member_of` | SPR P/mod; COG-O S |
| MD-INTELLECTUAL | Disorders of intellectual development | 6A00 | ID `names` | COG-L P/**minimal**; COG-O S |
| MD-DEMENTIA | Dementia | 6D80–6D8Z | DEM `names` | COG-O P/low; ARO S; VIS-L S; AMB S |
| MD-EPILEPSY | Epilepsy or seizures | 8A60–8A6Z | EPI `names` | SPR SITUATIONAL/mod |
| MD-MS | Multiple sclerosis | 8A40 | MS `names` | THR P/low; STA S; AMB S; VIS-L S; CNT S |
| MD-PARKINSON | Parkinson disease | 8A00 | MOVE `member_of` | AMB S/low; BAL S; REA S |
| MD-DYSTONIA | Dystonia | 8A02 | MOVE `member_of` | REA S/low |
| MD-ESSENTIAL-TREMOR | Essential tremor | 8A04.1 | MOVE `member_of` | REA S/mod |
| MD-STROKE | Stroke (cerebrovascular disease) | 8B00–8B2Z | BRAIN `member_of` | COG-O P/low; AMB S; COM-E S; REA S; ARO S |
| MD-TBI | Traumatic brain injury (incl. concussion, post-concussion) | NA07 | BRAIN `member_of` | BAL P/low; COG-O P; SPR S; STA S |
| MD-APHASIA-DYSARTHRIA | Aphasia and dysarthria | MA80 (verify) | BRAIN `member_of` | COM-E P/mod |
| MD-SCI | Spinal cord injury | verify: traumatic (ch.22) + non-traumatic (ch.8) entities | SCI `names` | WHM P/**mod** (§4: high-predictive at complete lesions, note it); REA S; THR S; CNT S; PAI S |
| MD-ME-CFS | ME/CFS | 8E49 | COM `member_of` | STA P/mod |
| MD-POTS | Postural orthostatic tachycardia syndrome | 8D89.2 (verify) | COM `member_of` | STA P/mod; THR S; BAL SITUATIONAL |
| MD-MCAS | Mast cell activation syndrome | verify (may lack a stem code) | COM `member_of` | CHM P/mod |
| MD-LONG-COVID | Post COVID-19 condition | RA02 | COM `member_of` | STA P/low; THR S; COG-O S |
| MD-CHRONIC-PAIN | Chronic pain (incl. chronic primary pain, fibromyalgia) | MG30 | PAIN `names` | PAI P/mod |
| MD-VESTIBULAR | Disorders of vestibular function | AB30–AB3Z | VES `names` | BAL P/mod; SPR S |
| MD-HEARING-LOSS | Hearing loss | AB50–AB5Z | DEAF `identity_first` | AUD P/mod (infrastructure share only; DeafSpace/d340 held by the identity profile — `axes` AX-AUD notes) |
| MD-VISION-IMPAIRMENT | Vision impairment including blindness | 9D90 | BLIND `identity_first` | VIS-N P/mod; VIS-L P |
| MD-LIMB-DIFFERENCE | Limb loss or limb reduction | verify (congenital LB7-/LB8-; acquired ch.22) | LMB `identity_first` | REA P/mod |
| MD-SKELETAL-DYSPLASIA | Skeletal dysplasia (dwarfism) | LD24 (verify) | LPA `identity_first` | REA P/mod; AMB S |
| MD-ANXIETY | Anxiety or fear-related disorders | 6B00–6B0Z | MH `member_of` | ARO P/low; SPR S |
| MD-PTSD | Disorders specifically associated with stress | 6B40–6B4Z | MH `member_of` | ARO P/low; SPR S |
| MD-MOOD | Mood disorders | 6A60–6A8Z | MH `member_of` | ARO S/low; STA S |
| MD-PSYCHOSIS | Schizophrenia or other primary psychotic disorders | 6A20–6A2Z | MH `member_of` | ARO P/low; SPR S |
| MD-MIGRAINE | Migraine | 8A80 | — (§4 deferred candidate; no identity home) | SPR P/mod; BAL S |
| MD-IBD-OSTOMY | Inflammatory bowel disease (incl. ostomy) | DD70–DD7Z | — (§4 deferred candidate) | CNT P/mod |

ICF crossings are lifted from `population_axis_map` and functional-taxonomy §4 rows; where an identity umbrella deduped its members (COM, BRAIN — `references/project-standards.md:563` preserved only the *union*), the per-diagnosis signature comes back from §4's own rows (MS→THR, POTS→STA/THR/BAL, MCAS→CHM, PCS-TBI→BAL, LCOV→STA). Confidence is functional-taxonomy §3.2 (`:225-234`), ratified 2026-07-21 and **never landed in any table** — this is the table it was written for (diagnosis-to-axis).

**Excluded, stated:** BAR, TALL (body size is not a diagnosis; a medical row would re-medicalise what A-SIZE frames as "the environment wrongly normed"), MOB (functional group; reached via MD-SCI/MS/STROKE/PARKINSON), NDV (identity umbrella; reached via its members), ALL (qualifier), **DEAFBLIND** (no ICD-11 entity; identity lens only — the lens switch must show an explicit "no medical-lens entry; see identity lens", never a blank; D-0184 `:25-29`). **Deferred, named so absence is visible:** osteoarthritis/rheumatological (FA0-), cerebral palsy (8D20), neuromuscular (8C7-), Down syndrome (LD40), respiratory/oxygen dependency (ties to R8, closed 2026-07-21 as decomposed), cardiac.

*Cost if wrong:* rows are deprecable (`status` CHECK) and crossings deletable; nothing keys on them yet (0 extractions, 0 specifications). *Falsification:* a reader-facing test — a diagnosis a real reader would search that reaches nothing and is not in the deferred list.

### Ruling 1.2 — crossings: two map tables, medical↔needs derived

Build `identity_medical_map` and `icf_medical_map`. Do **not** build medical↔needs: no identity↔needs map exists either (D-0184 `:26-27`); needs are reached through the `axes` hub exactly as identity is today (`access_need_axis_map`). Parity, and §8's burden on adding apparatus. medical↔ICF is **not** derivable through identity: COM/BRAIN merged their members' signatures, so identity→ICF loses exactly what the medical lens exists to show.

Names follow the ruled lens vocabulary and the owner's own lens order identity/icf/needs/medical (`references/project-standards.md:2449-2452`), so no later rename touches them:

```sql
CREATE TABLE identity_medical_map (
  identity_code  TEXT NOT NULL REFERENCES populations(population_code),
  medical_code   TEXT NOT NULL REFERENCES base_taxonomy_medical(medical_code),
  relationship   TEXT NOT NULL CHECK (relationship IN ('names','member_of','identity_first')),
  note TEXT, created_at TEXT DEFAULT (datetime('now')), created_by_session TEXT,
  PRIMARY KEY (identity_code, medical_code));
CREATE TABLE icf_medical_map (
  icf_code       TEXT NOT NULL REFERENCES axes(axis_code),
  medical_code   TEXT NOT NULL REFERENCES base_taxonomy_medical(medical_code),
  role           TEXT NOT NULL CHECK (role IN ('PRIMARY','SECONDARY','SITUATIONAL')),
  mapping_confidence TEXT NOT NULL CHECK (mapping_confidence IN ('high_predictive','moderate','low','minimal')),
  note TEXT, created_at TEXT DEFAULT (datetime('now')), created_by_session TEXT,
  PRIMARY KEY (icf_code, medical_code));
ALTER TABLE base_taxonomy_medical ADD COLUMN icd11_anchors TEXT;      -- comma list, mirrors axes.icf_b_anchors
ALTER TABLE base_taxonomy_medical ADD COLUMN icd11_verified_at TEXT;  -- NULL until bytes are in hand
```

`relationship` semantics: `names` — same subject; `member_of` — identity row is a ratified umbrella containing this diagnosis; `identity_first` — the community does not describe itself by this diagnosis; the crossing is navigation only and **the identity display_name is what renders** (functional-taxonomy §3.3 `:238-245`: identity profiles carry no ICD anchor — that holds, because the anchor lives on the medical row and `populations` is untouched).

### Ruling 1.3 — guardrails, and what failure looks like

1. **Recording a diagnosis is evidence; determining by one is the frame.** `add-extraction` may take `--medical` alone (a paper that studied "people with MS" says so). **`assess_cell.py` refuses a cell whose only lens is `--medical`** (`scripts/assess/assess_cell.py:925-928` already takes the four): a determination keyed on a diagnosis alone is the medical model as the project's frame — D-0170's stated failure. D-0182's schema CHECK is untouched.
2. **Default-off.** No render surface shows the medical lens unless the reader selects it (D-0170 rationale, `:26-28`). No render exists yet; recorded as doctrine in D-0189 so the first render is built against it.
3. **No project-coined medical umbrellas** (rows are ICD-11 entities/blocks only) — §6's umbrella rule for this lens.
4. `_VALUE_BEARING` (`scripts/db.py:3061`) applies to `display_name`/`description`, imported not retyped. A diagnosis names the subject, not the determination, so it is compatible in principle — same status as `populations.MS`.
5. `identity_first` rows render the community's name.

**Failure, for the antagonist:** a `specifications` row whose only non-NULL lens is `medical_code`; a medical row with zero crossings; a render or skill that shows the medical lens unselected; an `identity_first` landing page headed by the diagnosis; a row anchored to nothing in ICD-11.

### Ruling 1.4 — naming, provenance, writer (the coverage bug)

`base_taxonomy_medical` is **absent from `dbcore.TABLES`** (`scripts/dbcore.py:467-546` — list ends at `specification_source_links`), and `db.py` has no writer for it (subcommand list has no `add-medical`). Sixth blindness; `CLAUDE.md:173-176` — fix, do not bypass.

`db.py add-medical` (row + ≥1 crossing in one act, the `add-term` precedent `:3064-3090`) refuses: code not matching `^MD-[A-Z]+(-[A-Z]+)*$`; value-bearing name/description; no crossing; `--identity ALL`; `--icd11` absent. `icd11_verified_at` is set **only** when `--icd11-payload` names a persisted file under `retrieval-log/` containing the code (`CLAUDE.md:239` extended to the vocabulary). Anchors above are *expected* codes; **none is written as verified from memory**. Retrieval: `scripts/research/retrieval_log.py:193 fetch(url, session, purpose)` takes any URL — use the WHO ICD-11 API (`id.who.int`, needs client credentials in env) or, failing that, the rows land with `icd11_verified_at NULL` and the check in 1.5 reports the count. `add-medical-crossing` adds further rows. `dbcore.TABLES` gains `base_taxonomy_medical` before `identity_medical_map`, `icf_medical_map`, and before `source_value_extractions` (FK order; `:530-545`). No Pydantic mirror: `validate_pydantic_schemas.py` MODEL_TABLE_MAP maps `populations` only (`:87`); `axes`/`access_needs` have none — record the consistency in 074's header.

### Ruling 1.5 — migration shape and record

One schema migration **`scripts/migrations/074_medical_lens_crossings.sql`** (next after 073; `user_version` 74; DDL above; edits `dbcore.TABLES` in the same change) plus one data migration emitted through the write path (scratch → `add-medical` ×29 → `emit_batch_sql` → `emit_data_migration --session` → `migrate_db`). One check, `medical_lens_integrity` in `governance/check-registry.yaml` (advisory until anchors verify, then blocking): EXAMINED = rows; red on a row with no crossing, a digit in a code, a value-bearing name, a medical-only `specifications` row; reports unverified anchors. Decision record: **register row D-0189** (D-DOCT), DR file, `decisions` INSERT, ledger entry — the register is the home; the file is a copy the header wrongly calls generated (correction 4).

**AGONIST (Opus for 074/writer/check/records; Sonnet for the 29-row seed and ICD retrieval).** Verify: `PRAGMA foreign_key_check` empty; `select count(*) from base_taxonomy_medical`=29; every code has ≥1 row in either map; `migrate_db.py --rebuild /tmp/rebuilt.db` byte-equal; a scratch delta of 29+N rows emits 29+N statements (the 32-vs-40 test, `dbcore.py:480-487`); `python3 scripts/run_checks.py --selftest` PASS; `schema_reference_audit` green.

**ANTAGONIST.** The claim to attack: *"no medical row is a rule-5 copy of an identity row."* Enumerate the 8 `names` rows; diff each `description` against `populations.description` for token overlap > 50%; any hit is a copy. Second: resolve three random `icd11_anchors` against WHO and count `icd11_verified_at IS NULL` — every NULL is a from-memory anchor the writer let through. Third: `grep -rn "medical" skills/ scripts/generate/` for anything rendering the lens unselected. Fourth: diff `icf_medical_map` rows for COM/BRAIN members against functional-taxonomy §4 `:298-304` — a signature not in doctrine was authored, and must say so in `note`.

---

## ITEM 2 — `source_locators`

### Findings (queries reproducible from the ro connection)

- 881 rows; `recovered_from`: 835 pre-reset corpus, 32 `.md` registry, 8 `.json`, 6 retracted (parked identities). 537 carry a title; 491 of those are pre-reset rows that received bibliography from the **fold** `data_20260823225142` (`UPDATE source_locators SET authors,pub_year,title,… = (SELECT … FROM reference_stubs rs WHERE rs.ref_id = source_locators.ref_id)`), where `reference_stubs` was loaded from `references/global-reference-registry.md` keyed on **that file's own REF-ids** (`data_20260823223839` header, "531 markdown citation records").
- **Mechanism: two ref-id keyspaces joined as one.** The offsets between a title's embedded DOI and the row that holds that DOI in `doi` are irregular — {−19, 3, 17, 26, 42, 74, …, 612} — so not a column shift; a keyspace collision, partially coincident (5/36 agree). The same divergence was recorded on 2026-07-13: *"six of six collide"* between page REF-IDs and DB rows (`sessions/session_2026-07-13-value-genealogy-mining-dossier.md:35`).
- **Which side is right:** identifiers (`doi/pmid/…`) are the DB keyspace — what `next_ref_id` continues, what manifests name, what the archived baseline's author rows agree with (correction 2). Bibliography is the `.md` keyspace. Second independent measure: of 9 titles embedding `PMID:` beside a non-NULL `pmid`, **6 disagree** (`REF-00010` pmid 32316862 vs title 27993606, etc.); 30 more embed a PMID beside a NULL column.
- **32 DOIs are held by 2–5 rows** (e.g. `10.31030/1803049` ×5; `10.4324/9781003564164` on REF-00054/00063/00148). `workplan/dedup-audit-same-doi-multi-refid-2026-07-21.md` adjudicated 29 groups/73 ids; DR-2026-08-19 §6 `:490-494` records that adjudication never reached the stash.
- **(e) Confined to the stash.** `evidence_sources` ∩ stash on ref_id = REF-00784 only, DOIs equal, stash title NULL, `PROMOTED`; zero evidence DOIs held under a different stash id; zero `pub_title` embedding a DOI; zero rows in `source_slug_links`, `search_admissions`, `evidence_population_match`, `observed_terms` citing a title-bearing stash id outside `evidence_sources`. **Urgency: medium** — nothing admitted is affected; the next R9b promotion is.
- **(d) No gate.** `grep -i locator governance/check-registry.yaml` → nothing. `source_locators_floor` (DR-2026-08-19 `:509`) was never registered.
- **(c) REF-VERIFIED-001…012 (11 rows)** are real leads from the May-2026 verified-sources registries, listed by name at `sessions/session_2026-05-08-co0009-phase3.md:39-44` (Schroeder & Steinfeld 1979 HUD; Koontz 2005 PMID 16320141; IEC 60118-4; ISO 23599; FIA GD-05-22…). A **closed namespace**: `dbcore.REF_ID_SHAPE` admits it (`:238`) and the mint never issues from it (`:581-582`). Not placeholders, not a failed import. Two are DOI twins (VERIFIED-003 ≡ REF-00037; VERIFIED-010 ≡ REF-00254, "D01 duplicate cluster … allowlisted", `sessions/session_2026-05-20-ato-rehab.md:1315`). Two carry prose in `standard_number` (VERIFIED-001, -007) — column misuse.

### Ruling 2.1 — R9b: **kept, with a guard**; not suspended

Suspending re-mints identities for DOIs the project holds — the defect R9 exists to stop (`research_batch_dod.py:468-486`). The guard, **R9c** in `scripts/audit/research_batch_dod.py` beside R9a/R9b: for every admitted row whose ref_id the stash holds with a non-NULL `title`, `_norm_title(stash.title)` vs `_norm_title(evidence_sources.pub_title)` (`retrieval_log.py:90`) must agree above threshold, else FAIL *"stash bibliography disagrees with the admitted identity — misfolded row or wrong admission; adjudicate before promoting."* Same comparison as a **Refusal** in `db.py add-source` when the stash title disagrees with `--pub-title`, overridable only with `--stash-title-override <reason>` that writes the reason to `source_locators.notes`. *Cost if wrong:* a false block costs one override. *Falsification:* the 5 agreeing rows must pass and the 31 disagreeing must fail at the chosen threshold.

### Ruling 2.2 — repair: re-attach by identifier, detach what cannot be re-homed

One compensating data migration, built by script, replayed through the CLI. Rule: recover `references/global-reference-registry.md` from git (deleted 2026-08-23); parse each entry's DOI/PMID; attach its bibliography to the stash row whose `doi`/`pmid` matches case-insensitively; an entry with no identifier attaches by ref_id **only** if the stash row also has no identifier (title-only on both sides, the 32 `.md`-origin rows); otherwise the six bibliography columns are NULLed and `notes` records *"bibliography detached 2026-09-xx: folded under a colliding ref-id keyspace by data_20260823225142; registry entry <id> carries no identifier to re-home by."* Mechanical for the 203 doi+title rows; per-row retrieval (Crossref title, persisted) settles the remainder. `update-locator` reaches only `status` (`db.py:1048-1053`) — **coverage bug**: extend it with the bibliography columns, `--notes`, `--detach-bibliography`; then the repair runs on a scratch through it. Twins: mark all but the survivor `RETIRED` with `notes='twin of REF-…'`, reusing the 2026-07-21 audit's survivor choices where they exist; VERIFIED-003→RETIRED twin of REF-00037; VERIFIED-010→twin of REF-00254. VERIFIED-001/-007: prose to `notes`, `standard_number` = `HUD-PDR-400` / `FIA GD-05-22`.

### Ruling 2.3 — gate: `source_locators_integrity`

Register `scripts/audit/source_locators_integrity.py`, EXAMINED = rows: (i) ref_id shape; (ii) DOI held by >1 non-RETIRED row; (iii) title-embedded DOI/PMID ≠ column; (iv) `standard_number` > 64 chars. **Advisory until 2.2 lands, then blocking** — registering it blocking today reddens every PR. What reaches the book without it: a misdescribed lead chased and admitted under a known id — `CLAUDE.md` §5(c) through the sanctioned door.

**AGONIST (Sonnet: measurement script, extent run, migration mechanics; Opus: the re-attach rule review and twin adjudication).** Verify: after 2.2, (ii)–(iv) = 0; `migration_reproducibility` green; R9c passes on the 9 live admissions.

**ANTAGONIST.** Attack *"identifiers are the DB keyspace and correct."* Take five pre-reset rows with `doi_resolution_outcome='RESOLVED'` and no title; compare Crossref's authors for that DOI with `_archived/scripts/migrations/012_baseline_2026-05-15.sql`'s `evidence_source_authors` for the same ref_id. Any mismatch means the identifier side is also misaligned and the re-attach rule is wrong. Then attack the extent: run the Crossref-title comparison over all 203 doi+title rows and report the true disagreement rate (31/36 is a lower bound on a subset). Then `grep -rn` `references/ sessions/` for prose citing a detached title under its old ref_id — rule 4 prose callers.

---

## ITEM 3 — WHAT `scope` DISCRIMINATES

I fetched the three disputed abstracts this session. According to PubMed — Koontz et al. 2010 [DOI](https://doi.org/10.1016/j.apmr.2010.01.009): *"Case series … convenience [sample] … manual wheelchair (n=109), power wheelchair (n=100), and scooter users (n=14) … Passageway openings were increased in 5-cm increments until the user could successfully perform each task … electromechanical probe … 1-way analysis of variance"*, four sites. Dutta et al. 2011 part I [DOI](https://doi.org/10.3109/17483107.2010.509885): *"five scooters … Free-standing styrofoam walls … An expert driver repeatedly manoeuvred the scooters … incrementally decreased the dimension"*. King et al. 2011 part II [DOI](https://doi.org/10.3109/17483107.2010.549898): *"two four-wheeled scooters … 'Room' size was decreased until our expert driver could no longer perform the manoeuvre"*. J-STAGE (fetched via the DOI redirect, `…/aija/69/577/69_KJ00004227047/_article/-char/en`): Baba et al. 2004 — a survey of newly constructed Japanese residences assessing "wheel chair movements possibility" geometrically. **None of these bytes is yet under `retrieval-log/`; the agonist persists them first.**

### Ruling 3.1 — the discriminator

**`high_control` = a controlled manipulation of the design parameter whose effect is measured on human participants — any participants.** Who they are is `evidence_population_match`'s job and never moves the tier (rule 5: one fact, one home — the ORDER-OF-WORK correction at `:177-194` is right on this). **`lower_control` = everything else `clinical`: observational, cross-sectional, qualitative, and device-only bench measurement with no participant.** Basis: `governance/tier-system.md:15` — T1 anchors *"claims that turn on physiological / behavioural / biomechanical mechanism"*; a device envelope measured with one operator has no human mechanism in it — the human is the apparatus. That fact already has its home in `source_value_extractions.measurement_paradigm` (`swept_path_dynamic`) and `device_class` (`scooter`). Option (c), a device-bench discriminator: **refused** — apparatus without a claim it would change. *Cost if wrong:* two rows at T3 that should be T1; one compensating migration; no cell lost. *Falsification:* a T1 exemplar anywhere in `tier-system.md`/`evidence-methodology.md` that is a device-only test.

### Ruling 3.2 — the four rows

- **REF-00784 → `high_control`; tier 1 stands.** The 2026-07-20 sweep (`audits/anchor-correctness-sweep-2026-07-20.md:287`) read PubMed's "Case series" as a design-control statement; it is a sampling statement. 223 users, a manipulated clearance in 5-cm steps, instrumented, four sites — D-E's clearance study at T1 (`governance/mission-and-epistemics.md:90`). Prose callers now wrong: `references/bpc/frameworks-and-methodology/manoeuvring-footprint-vs-turning-radius-methodology.md:71,130` ("Tier 3") — live (`.ignore` hides only `references/audits/`, `references/search-log/`), correct them; the 2026-07-20 audit and `sessions/…08-16…:203` are frozen — the ledger supersedes them.
- **REF-00971, REF-00972 → `lower_control`; tier 3 stands.**
- **REF-00976 → `lower_control`; tier 3 stands** — field survey of dwellings, geometric assessment; and the 2026-06-11 conservative default (`sessions/session_2026-06-11-artifacts/2.5-resolution-table.md:32`) cannot promote.

No tier changes; road-to-batch-06 STOP #2 is not tripped. `amend-source --field scope` accepts all four (each agrees with its stored tier).

### Ruling 3.3 — retrospective ratification: **GRANTED, no correction**

REF-00973 `high_control` (17 SCI participants, inclination varied), REF-00974 `high_control` (ten participants, instrumented — the match row holds the PROXY fact), REF-00975 `lower_control`, REF-00977/00978 `intrinsic`. Separately noted, not a scope matter: REF-00978's Co-1 warrant is unwarranted-pending under D-0178 until `co1_provenance` names the co-production.

**AGONIST (Opus rules the prose sweep; Sonnet the mechanics).** `retrieval_log.fetch` for PMID 20434614 efetch and the J-STAGE English page; four `amend-source --field scope` on a scratch, replacing the ESCALATED `notes` with a pointer to D-0190; emit → migrate; `python3 scripts/audit/adjudication_integrity.py` → **0 of 9**; update the quarantine reason at `governance/check-registry.yaml:1477` with the dated figure and **promote to advisory** (it is now non-vacuous and green); correct the methodology file's two "Tier 3"; register row **D-0190** (D-METH, application of existing methodology). This is ORDER-OF-WORK W1.

**ANTAGONIST.** Attack *"case series is a sampling label, not a design-control label."* `grep -rn "case series" governance/ decisions/` — if the ratified ladder names it as T3 anywhere, 3.2 falls. Then attack 3.1 with its strongest opponent: the rig controls the parameter more tightly than any survey — find one T1 exemplar in doctrine with no participant. Then run `check_tier_consistency` over all 9 → all True, and confirm B5a's anchoring set is 9.

---

## ITEM 4 — EVERYTHING ELSE SITTING ON THE OWNER

| # | Item, where | Ruling |
|---|---|---|
| 4.1 | ORDER-OF-WORK `:97-100` medical deferred | **Withdrawn** (Item 1). |
| 4.2 | ORDER-OF-WORK `:92-96, :196-208`; b5b §2, §6; audit-reconciliation TASK 3; BATCH-06-PLAN §7 option 3 | Resolved by Item 3. |
| 4.3 | **D-0184 `review_status: PENDING`** (register `:6139`) — owner review of lens-as-column | **Ratified.** Landed, live, and Item 1 is built on it. Set the register's reviewed value (derive from `schemas/enums.py`). |
| 4.4 | b5b §4 — "the ladder cannot see who was controlled" | **By design.** Tier × match grade composes in directness conditioning (`mission-and-epistemics.md:101-107`); no new apparatus. Record. |
| 4.5 | b5b §5 — `co1_source_type='dpo_annual_survey'` outside the enum; CHECK or free text | `co1_source_type` **stays closed and gets a SQLite CHECK** mirroring `Co1SourceType` (Layer 1 must state what Layer 2 may produce — the 2026-09-10 ruling's own failure family); REF-00978 amended to `dpo_research`, the survey nature stated in `co1_provenance` prose. Reason: G3 reads this column for grain — a new value silently changes weight. `co1_provenance` is **free text by ruling** (D-0178 requires a sentence that names the co-production). |
| 4.6 | `axes` AX-BAL "re-grade to PARTIAL PROPOSED … owner-gated" (notes, 2026-07-24) | **Refused as stale**: its 21 links were pre-reset corpus; coverage is re-derived from the live admitted set (0 today). STUB stands. |
| 4.7 | `access_needs` A-AT "digital — flagged for owner decision" | **In scope where the interface is a fixed part of the building** (kiosks, intercoms, lift controls, building apps); otherwise out. Recorded in D-0192; no table write (no writer exists — note it, do not fix here). |
| 4.8 | functional-taxonomy R6/R7/R8 "the owner adjudicates" | **Closed 2026-07-21** — `decisions/RATIFICATION-RECORD-2026-07-21.md:41-47` (R6 folded, R7 two axes, R8 decomposed). Nothing pending; respiratory is named as a deferred medical candidate. |
| 4.9 | functional-taxonomy §7 "`lang_jur_map` remains empty pending owner criteria" | **Stale** — 70 rows live. Annotate the doc (supersession note pattern already used at `:327-333`). |
| 4.10 | **Decision 8, the room stratum** (open since 2026-08-02; `governance/schema-reference-exemptions.yaml:26-33`) | **Closed by D-0171** (2026-08-27: building type / room type / element) and the same-day "Three tables" ruling (`project-standards.md:2440-2444`). `room_page.py` queries tables that never existed and the ruled shape differs → **delete** (code, §8); its four exemptions become STALE and go. Building the three tables is separate schema work, not scheduled here. |
| 4.11 | `question-author_SKILL.md` — "where question headings live is an open content question" (exemptions `:44-51`) | **Not adjudicated**: never presented with a decision shape; it is B3 navigation design (mission #6). Stays exempt. Flagged, not hidden. |
| 4.12 | Decision #5, verify-urls cron (road-to-batch-06 `:58, :91`) | Not presented; not touched. The B3 fix is the DoD predicate, as that file says. |
| 4.13 | "owner decision #2" (`DR-2026-08-14-tier-1-retirement-batch.md:27`) | Reference unresolved in this pass; Sonnet identifies it. Likely closed by DR-2026-07-13 (b) + the 2026-08-23 registry deletion; if not, re-present. |
| 4.14 | ORDER-OF-WORK `:151` — are SKILL files doctrine? | **Process apparatus** (Layer 2 tools; `CLAUDE.md` §8 lists code as deletable and names doctrine exhaustively — skills are not in it). Deletable on evidence, with the prose-caller sweep. |
| 4.15 | 2026-08-28 "`identity` … Confirmation pending — the rename is not applied" (`project-standards.md:2475-2478`); M1's six orphaned replacement names (`:2159-2166`) | **`identity` confirmed** as the lens name for links/codes (the owner's own D-0169 `base_item_icf_links` names the lens); `base_taxonomy_<lens>` for registries; pairwise maps `<lensA>_<lensB>_map` in the order identity/icf/needs/medical. The rename sweep itself is not scheduled here (rule 4 cost); the new tables already comply. |
| 4.16 | Supersede/re-determination design (runbook `:374`) | Not owner-gated (ORDER-OF-WORK `:108-112`); not mine. |

**Genuinely non-delegable even now:** none found. 4.11 is not non-delegable; it is un-presented.

---

## ORDER OF WORK, PARALLELISM, TIERS

```
W0  Record the delegation: ledger entry + D-0188 (register, DR, decisions INSERT)   OPUS   <- first; binds everything after
     parallel, no DB:
       P1  add-medical / add-medical-crossing writer + dbcore.TABLES + medical_lens_integrity   OPUS
       P2  source_locators_integrity.py + extent run (persisted Crossref payloads)               SONNET
       P3  R9c in research_batch_dod.py + add-source stash-title refusal                         SONNET
       P4  Item 4 records (D-0192), enum CHECK for co1_source_type, room_page deletion           SONNET
T1  Item 3: retrievals, 4 amend-source, migration, prose sweep, D-0190                          OPUS rules / SONNET mechanics   (DB)
T2  Item 1: 074 schema + seed data migration + D-0189                                            OPUS schema / SONNET seed      (DB, after T1)
T3  Item 2: repair migration, twins, update-locator extension, gate promotion, D-0191            OPUS join rule / SONNET run    (DB, after T2)
A1..A3  Antagonist passes, fresh read-only session after each of T1/T2/T3 commits                OPUS
```

DB-touching tracks are strictly serial (rule 3's cron conflict). Item 3 first because it is smallest and unblocks batch 07's anchors; Item 1 second because the owner named it; Item 2 third because its live blast radius is zero admitted rows and its measurement (P2) can run meanwhile.

### Critical Files for Implementation
- `/home/user/guidebook/scripts/db.py` — `add-medical`, `add-medical-crossing`, `update-locator` extension, stash-title refusal in `add-source`
- `/home/user/guidebook/scripts/dbcore.py` — `TABLES` gains `base_taxonomy_medical` and the two maps in FK order (`:467-546`)
- `/home/user/guidebook/scripts/migrations/074_medical_lens_crossings.sql` — new; DDL in Ruling 1.2
- `/home/user/guidebook/scripts/audit/research_batch_dod.py` — R9c guard beside R9a/R9b (`:468-540`)
- `/home/user/guidebook/data/decisions/decision_register.yaml` — D-0188…D-0192, plus `references/project-standards.md` ledger entries and `governance/check-registry.yaml` (two new checks, `adjudication_integrity` promotion)