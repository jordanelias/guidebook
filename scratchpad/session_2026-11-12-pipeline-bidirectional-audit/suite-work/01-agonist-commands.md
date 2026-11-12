# 01 agonist commands log
Started 2026-11-12 02:55 UTC; HEAD 4afe1dd

```
$ sha256sum data/guidebook.db; git rev-parse --short HEAD; python3 -I -c "import sqlite3;c=sqlite3.connect(\"file:data/guidebook.db?mode=ro\",uri=True);print(c.execute(\"pragma user_version\").fetchone())"
c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d  data/guidebook.db
4afe1dd
(125,)
[exit 0]
```

```
$ grep -o -E "^\| (REQ-[0-9]{3}|HS-A[0-9]{2}) \| \*\*[A-Z]+\*\*" scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-handshake-matrix.md | awk "{print \$NF}" | sort | uniq -c
      8 **CONTRADICTED**
      9 **MET**
     61 **PARTIAL**
     33 **UNMET**
      7 **UNPROVEN**
[exit 0]
```

```
$ python3 workplan/pipeline-state-graph/walkability.py; echo EXIT=$?
tables 56  views 23  fk 90

STAGE-PAIR MATRIX (tables in later stage that reach an earlier stage / tables in earlier stage that reach later; skip = reach without crossing the intermediate stages)
pair                           up  down  skip  recvFK  sendFK  views
base->research                  5     7  None       9       0  v_coverage_priority
base->evidence                  3     3     3       3       2  v_item_provenance,v_source_reach_all,v_value_independence,v_
base->judgment                  4     7     4       7       0  v_value_independence,v_determination_provenance,v_unregister
base->synthesis                 5     7     5       9       0  
base->specification             4     7     4       7       0  v_code_floor_only,v_item_provenance,v_source_reach_all,v_det
base->render                    0     0     0       0       0  
research->evidence              0     0  None       0       3  v_source_admission
research->judgment              0     0     0       0       0  
research->synthesis             0     0     0       0       1  
research->specification         0     0     0       0       0  
research->render                0     0     0       0       0  
evidence->judgment              5     3  None       5       0  v_value_independence,v_determination_provenance,v_unregister
evidence->synthesis             5     2     5       3       0  v_convergence_sources
evidence->specification         4     2     4       2       0  v_item_provenance,v_source_reach_all,v_determination_provena
evidence->render                0     0     0       0       0  
judgment->synthesis             1     1  None       1       2  
judgment->specification         1     1     1       1       0  v_determination_provenance
judgment->render                0     0     0       0       0  
synthesis->specification        3     3  None       2       0  v_divergence,v_pending
synthesis->render               0     0     0       0       0  
specification->render           0     0  None       0       0  

ZIGZAG WALK between non-base stages (shortest undirected path over FKs and view co-reads, not passing through base, infrastructure or unmapped tables; - is a foreign key, ~v~ a view that reads both):
  research<->evidence            search_admissions - evidence_sources
  research<->judgment            gap_mining - gaps - evidence_population_match
  research<->synthesis           gap_mining - gaps
  research<->specification       gap_mining - gaps - specifications
  research<->render              NO PATH
  evidence<->judgment            evidence_sources - evidence_population_match
  evidence<->synthesis           evidence_sources - convergence_sources
  evidence<->specification       evidence_sources - determination_gates
  evidence<->render              NO PATH
  judgment<->synthesis           evidence_population_match - gaps
  judgment<->specification       source_value_extractions - specification_extraction_links
  judgment<->render              NO PATH
  synthesis<->specification      convergence_assessment - specifications
  synthesis<->render             NO PATH
  specification<->render         NO PATH

ZIGZAG, POPULATED EDGES ONLY (an FK counts if some child row has a non-NULL pointer; a view if it returns a row):
  research<->evidence            search_admissions - evidence_sources
  research<->judgment            search_admissions - evidence_sources - evidence_population_match
  research<->synthesis           search_admissions - evidence_sources - convergence_sources
  research<->specification       search_admissions - evidence_sources - determination_gates
  research<->render              NO PATH
  evidence<->judgment            evidence_sources - evidence_population_match
  evidence<->synthesis           evidence_sources - convergence_sources
  evidence<->specification       evidence_sources - determination_gates
  evidence<->render              NO PATH
  judgment<->synthesis           evidence_population_match - evidence_sources - convergence_sources
  judgment<->specification       source_value_extractions - specification_extraction_links
  judgment<->render              NO PATH
  synthesis<->specification      convergence_assessment - specifications
  synthesis<->render             NO PATH
  specification<->render         NO PATH

LATERAL (components of same-stage tables joined through a shared parent or child)
  base            tables 18 components  6  isolated: access_duration, access_stakes, lang_jur_map, life_stage_modifiers, rooms
  research        tables  8 components  4  isolated: gap_mining, research_code_leads, source_locators
  evidence        tables  8 components  1  isolated: 
  judgment        tables  5 components  2  isolated: term_adjudications
  synthesis       tables  8 components  1  isolated: 
  specification   tables  4 components  1  isolated: 
  render          tables  1 components  1  isolated: weighting_profile
  infrastructure  tables  4 components  3  isolated: data_migrations, decisions

RE-ENTRANT FK edges (child stage earlier than parent stage):
  evidence_population_match.gap_id -> gaps  non-null rows 0
  term_aliases.observation_id -> observed_terms  non-null rows 0
  gap_mining.gap_id -> gaps  non-null rows 0
  search_admissions.ref_id -> evidence_sources  non-null rows 61
  base_parameters.direction_ref_id -> evidence_sources  non-null rows 0
  search_executions.mined_ref_id -> evidence_sources  non-null rows 11
  search_candidates.resolved_ref_id -> evidence_sources  non-null rows 7
  source_value_extractions.promoted_to_rdc_id -> reasoning_doc_citations  non-null rows 0

ORPHANS (no FK in/out, no view reads): access_duration, access_stakes, data_migrations, decisions, life_stage_modifiers, research_code_leads, rooms, source_locators, weighting_profile

unFK id columns:

VIEWS spanning >1 stage: 12
  v_code_floor_only: base + specification
  v_convergence_sources: evidence + synthesis
  v_coverage_priority: base + research
  v_determination_provenance: base + evidence + judgment + specification
  v_divergence: synthesis + specification
  v_item_provenance: base + evidence + specification
  v_pending: synthesis + specification
  v_scan_ledger: base + evidence + judgment
  v_source_admission: research + evidence
  v_source_reach_all: base + evidence + specification
  v_unregistered_roots: base + evidence + judgment
  v_value_independence: base + evidence + judgment
views confined to one stage or none: v_best_practice, v_coverage_branch, v_coverage_jurisdiction, v_coverage_language, v_coverage_lens, v_derived_figure_check, v_evidence_authors, v_open_determination_gates, v_registry_duplicate_descriptions, v_research_scope, v_root_id_conflicts
EXIT=0
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/q.py
Q1
[(8, 0, 'pilot-3', '3xMOB')]
v_best_practice (0,)
v_determination_provenance (0,)
v_item_provenance (0,)
v_pending (0,)
v_divergence (0,)
v_code_floor_only (0,)
Q5
[(196, 7, 11, 0, 0, 203)]
[('adversarial-pass', 1), ('incidental', 4), ('lead-index', 3), ('planned', 195)]
Q9
[(59, 57, 11, 1)]
Q32
[(70, 19, 48, 0)]
[(70,)]
Q33
[(2382, 0, 15, 249)]
[('BROADER', 70), ('DEPRECATED', 2), ('DOMAIN', 49), ('NARROWER', 146), ('SYNONYM', 1119), ('TRANSLATION', 996)]
[exit 0]
```

```
$ python3 -I -c "
import sys; sys.path.insert(0,\".\")
from schemas.enums import JurisdictionCode as J
print(len(list(J)))
import sqlite3
c=sqlite3.connect(\"file:data/guidebook.db?mode=ro\",uri=True)
enum={j.value for j in J}
rows=c.execute(\"select language,jurisdiction from v_research_scope\").fetchall()
bad=[r for r in rows if r[1] not in enum]
print(len(bad), sorted({r[1] for r in bad}), len({r[1] for r in bad}))
"
36
19 ['AR', 'AT', 'CL', 'CO', 'CR', 'CY', 'EC', 'ET', 'GH', 'GT', 'MA', 'MX', 'PE', 'PH', 'TH', 'TZ', 'UY'] 17
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect(\"file:data/guidebook.db?mode=ro\",uri=True)
for (n,) in c.execute(\"select name from sqlite_master where type=\x27table\x27 and (name like \x27base%\x27 or name like \x27%need%\x27 or name like \x27%icf%\x27 or name like \x27%medical%\x27) order by 1\"):
    print(n, c.execute(f\"select count(*) from {n}\").fetchone()[0])
print(c.execute(\"select need_code from access_needs where need_code like \x27A-R%\x27\").fetchall())
"
access_need_icf 43
access_needs 17
base_icf 72
base_parameters 10
base_taxonomy_identity 23
base_taxonomy_medical 0
icf_medical_map 0
identity_icf_map 61
identity_medical_map 0
[('A-REACH',)]
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect(\"file:data/guidebook.db?mode=ro\",uri=True)
print(c.execute(\"select identity_code, count(*) from source_value_extractions group by 1\").fetchall())
print(c.execute(\"select sum(identity_code is not null), sum(icf_code is not null), sum(needs_code is not null), sum(medical_code is not null), count(*) from source_value_extractions\").fetchall())
print(c.execute(\"select identity_code, status from base_taxonomy_identity where identity_code in (\x27AMB\x27,\x27WHEEL\x27)\").fetchall())
print(c.execute(\"select count(*) from base_taxonomy_identity\").fetchall())
"
[(None, 2), ('ALL', 34), ('BLIND', 3), ('MOB', 170), ('MS', 2), ('SCI', 3)]
[(212, 1, 3, 0, 214)]
[]
[(23,)]
[exit 0]
```

```
$ grep -n -E "\bAMB\b|\bWHEEL\b" references/project-standards.md | cut -c1-150
567:RULE: Design-equivalence exception to the anti-umbrella rule (amends 2026-07-22 "work from axes"; does NOT repeal it). An umbrella population code
1127:orthogonal scalar dimension. `AX-AMB` (ambulant movement) and `AX-WHM` (wheeled movement) are not
1158:does not assert it; it *connotes* it. The substantive point stands — `AX-AMB` and `AX-WHM` are
1291:RULE: The mobility split is ratified as `AMB` / `WHEEL`, and the 31 links fan out to both. Owner
1292:ruling 2026-08-25: *"yes, AMB and WHEEL to fan out."* Settles the two questions the split design
1295:**The codes.** `AMB` — ambulatory disabled people. `WHEEL` — wheelchair users, in the owner's own
1299:`with-upper-limb-involvement`, across 28 items) become **62** rows — one `AMB` and one `WHEEL` per
1411:  non-`[\w-]` character after the token, so `AX-` never matches `AX-AMB`. There is no prefix mode.
2926:power); b730 is declared by AX-AMB, AX-REA and AX-WHM; those axes carry nine identities including
3446:**TWO THINGS REMAIN UNDECIDED AND ARE NOT GUESSED HERE.** (1) The replacement code shape — `DM-AMB`
3460:character after the token, so `AX-` never matches `AX-AMB`; that is a matcher fact recorded on
[exit 0]
```

```
$ grep -n -E '(^|[^A-Za-z_-])(AMB|WHEEL)([^A-Za-z_-]|$)' references/project-standards.md | cut -c1-140
1291:RULE: The mobility split is ratified as `AMB` / `WHEEL`, and the 31 links fan out to both. Owner
1292:ruling 2026-08-25: *"yes, AMB and WHEEL to fan out."* Settles the two questions the split design
1295:**The codes.** `AMB` — ambulatory disabled people. `WHEEL` — wheelchair users, in the owner's own
1299:`with-upper-limb-involvement`, across 28 items) become **62** rows — one `AMB` and one `WHEEL` per
[exit 0]
```

```
$ grep -n -i -E 'ambulatory|wheelchair user|mobility split|MOB. (is|was)|split.*MOB|MOB.*split' references/project-standards.md | awk -F: '$1>1299' | cut -c1-200
5168:4. **The umbrella adjective is itself a class.** "Accessible", "barrier-free", "inclusive", "universal" and "wheelchair friendly" are offered as interchangeable qualifiers of the same noun ("… 
[exit 0]
```

```
$ git grep -n -E '(^|[^A-Za-z_-])(AMB|WHEEL)([^A-Za-z_-]|$)' -- sessions decisions governance data/decisions workplan | cut -c1-200
governance/functional-taxonomy.md:123:| Canonical governance taxonomy | `governance/population-taxonomy.md` (CANONICAL, A7) | 11 top-level codes + sub-codes (MOB/AMB, MOB/UPL, NDV/AUT, NDV/ADHD, NDV/S
governance/functional-taxonomy.md:284:| MOB | MOB (+MOB/AMB, MOB/UPL) | AXIS-ALIAS | AX-AMB + AX-WHM | Canonical sub-codes already split ambulant/upper-limb; axis layer completes it |
governance/functional-taxonomy.md:291:| DEM | DEM | PROFILE (diagnostic; low-predictive) | COG-O primary; ARO, VIS-L, AMB | Emergent corpus: dementia-friendly design |
governance/functional-taxonomy.md:296:| NEU | NEU | PROFILE (umbrella; low-predictive) | COG-O, AMB, ARO, COM-E | FDA term `ABI` resolves here |
governance/functional-taxonomy.md:298:| MS | (sub-code proposal: NEU/MS) | PROFILE (diagnostic; **low-predictive** per armature) | **THR primary** (Uhthoff); STA, AMB, VIS-L, CNT | Re-homed by mechani
governance/population-taxonomy.md:34:| MOB | Mobility & Strength | MOB/AMB (ambulatory mobility), MOB/UPL (upper-limb / dexterity) | §2.1 |
governance/population-taxonomy.md:75:- **Evidence inheritance:** a sub-code inherits all evidence from its parent. MOB/AMB inherits all MOB evidence. NDV/AUT inherits all NDV evidence.
governance/population-taxonomy.md:76:- **Evidence addition:** a sub-code may have additional evidence specific to the specialization. MOB/AMB may have evidence about ambulatory gait that does not appl
governance/population-taxonomy.md:77:- **Specification narrowing:** a sub-code's specification range is always a subset of (or equal to) its parent's range. If MOB specifies grab bar diameter 32–38 
governance/population-taxonomy.md:81:- **BPC research:** always uses the most specific applicable code. If evidence addresses ambulatory mobility specifically, the BPC slug uses MOB/AMB, not MOB.
governance/population-taxonomy.md:82:- **Specification records:** use the parent code unless the sub-code produces a meaningfully different range or recommendation. A specification that applies identi
governance/population-taxonomy.md:91:- MOB/AMB — ambulatory mobility impairment (gait, balance, lower-limb function)
governance/population-taxonomy.md:131:The slash notation for sub-codes (MOB/AMB) is distinct from the slash notation for multi-population spaces. Context disambiguates: sub-codes are defined in the ta
sessions/_archive/session_2026-03-17-1730.md:8:  - multilingual-research (S1-A: MOB/AMB + MOB/UPL)
sessions/_archive/session_2026-03-17-1730.md:13:  - MOB/AMB turning space standards based on pre-2000 anthropometry; only CSA B651:23 current
sessions/_archive/session_2026-03-17-1730.md:14:  - MOB/AMB walker users not differentiated from wheelchair users in any standard
sessions/session_2026-08-25-rulings-incorporation-and-pipeline-sweep.md:40:- **`MOB` splits into `AMB` and `WHEEL`, and the 31 links fan out to 62.** The fan-out is a
workplan/2026-09-10-b5b-scope-owner-escalation.md:181:ORIENTATION TO LIFE TIME HOMES FROM VIEWPOINTS OF WHEEL CHAIR MOVEMENTS POSSIBILITY"* (2004, AIJ).
workplan/deprecated/8.8_to_9.0.md:335:| MOB/AMB walker users not differentiated from wheelchair users in ramp/gradient standards |
workplan/pipeline-state-graph/ATOMS.tsv:517:ENT-122	ACTIVE	EQUATES	RATIFIED_DOC	2026-07-21	governance/functional-taxonomy.md:291	base	DEM disposition	DEM is a diagnostic profile with low-predictive ma
workplan/pipeline-state-graph/ATOMS.tsv:522:ENT-127	ACTIVE	EQUATES	RATIFIED_DOC	2026-07-21	governance/functional-taxonomy.md:296	base	NEU disposition	NEU is an umbrella profile with low-predictive map
workplan/pipeline-state-graph/ATOMS.tsv:524:ENT-129	ACTIVE	EQUATES	RATIFIED_DOC	2026-07-21	governance/functional-taxonomy.md:298	base	MS disposition	MS is a low-predictive diagnostic profile re-homed 
workplan/pipeline-state-graph/ATOMS.tsv:620:ENT-226	SUPERSEDED	CARDINALITY	RATIFIED_DOC	2026-04-29	governance/population-taxonomy.md:88	base	sub-code enumeration	The sub-codes are MOB/AMB, MOB/UPL, ND
workplan/pipeline-state-graph/ATOMS.tsv:1388:LED-089	ACTIVE	MUST	OWNER_QUOTED	2026-08-25	references/project-standards.md:1288	base	AMB/WHEEL fan-out	MOB links fan out to both AMB and WHEEL; MOB is sup
workplan/pipeline-state-graph/atoms/atoms-ent.jsonl:113:{"id": "ENT-115", "source": "governance/functional-taxonomy.md:284", "quote": "| MOB | MOB (+MOB/AMB, MOB/UPL) | AXIS-ALIAS | AX-AMB + AX-WHM |"
workplan/pipeline-state-graph/atoms/atoms-ent.jsonl:120:{"id": "ENT-122", "source": "governance/functional-taxonomy.md:291", "quote": "| DEM | DEM | PROFILE (diagnostic; low-predictive) | COG-O primar
workplan/pipeline-state-graph/atoms/atoms-ent.jsonl:125:{"id": "ENT-127", "source": "governance/functional-taxonomy.md:296", "quote": "| NEU | NEU | PROFILE (umbrella; low-predictive) | COG-O, AMB, AR
workplan/pipeline-state-graph/atoms/atoms-ent.jsonl:127:{"id": "ENT-129", "source": "governance/functional-taxonomy.md:298", "quote": "| MS | (sub-code proposal: NEU/MS) | PROFILE (diagnostic; **low-p
workplan/pipeline-state-graph/atoms/atoms-ent.jsonl:223:{"id": "ENT-226", "source": "governance/population-taxonomy.md:88", "quote": "The current sub-code taxonomy is:", "modality": "CARDINALITY", "su
workplan/pipeline-state-graph/atoms/atoms-ent.jsonl:232:{"id": "ENT-235", "source": "governance/population-taxonomy.md:131", "quote": "The slash notation for sub-codes (MOB/AMB) is distinct from the s
workplan/pipeline-state-graph/atoms/atoms-led2.jsonl:40:{"id": "LED-089", "quote": "yes, AMB and WHEEL to fan out.", "modality": "MUST", "subject": "AMB/WHEEL fan-out", "claim": "MOB links fan out to 
[exit 0]
```

```
$ git grep -l -i -E 'mobility split|AMB / WHEEL|AMB/WHEEL' -- . ':!transcripts' | head -30
references/project-standards.md
scratchpad/session_2026-08-25-pipeline-smoke-test-mobility/logs/F5-population-split-design.md
scratchpad/session_2026-08-25-rulings-incorporation-and-pipeline-sweep/commands.jsonl
scratchpad/session_2026-08-27-hook-audit/WALKABILITY-PLAN.md
scratchpad/session_2026-08-27-hook-audit/audits/R2-ruling-precedence.md
scratchpad/session_2026-08-27-hook-audit/commands.jsonl
scratchpad/session_2026-10-12-pipeline-simplification/commands.jsonl
scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-adversarial-findings.md
scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-improvement-programme.md
scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/hs-sonnet-writing-brief.md
scratchpad/session_2026-11-12-pipeline-bidirectional-audit/commands.jsonl
scratchpad/session_2026-11-12-pipeline-bidirectional-audit/dossier/44-project-standards-remainder-verbatim.md
workplan/pipeline-state-graph/AMBIGUITIES.tsv
workplan/pipeline-state-graph/ATOMS.tsv
workplan/pipeline-state-graph/atoms/atoms-led2.jsonl
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect(\"file:data/guidebook.db?mode=ro\",uri=True)
cols=[r[1] for r in c.execute(\"pragma table_info(source_value_extractions)\")]
print([x for x in cols if \"creat\" in x or \"date\" in x or \"stamp\" in x or \"session\" in x])
cols2=[r[1] for r in c.execute(\"pragma table_info(specifications)\")]
print([x for x in cols2 if \"creat\" in x or \"date\" in x or \"stamp\" in x or \"session\" in x or \"retire\" in x])
"
['created_at', 'created_by_session', 'updated_at', 'updated_by_session']
['created_at', 'created_by_session', 'updated_at', 'updated_by_session', 'retired_at', 'retired_by_session', 'retirement_reason']
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect(\"file:data/guidebook.db?mode=ro\",uri=True)
print(c.execute(\"select identity_code, min(created_at), max(created_at), count(*) from source_value_extractions group by 1\").fetchall())
print(c.execute(\"select min(created_at), max(created_at), min(retired_at), max(retired_at) from specifications\").fetchall())
"
[(None, '2026-10-31 05:26', '2026-10-31 05:26', 2), ('ALL', '2026-11-06 02:51', '2026-11-06 04:56', 34), ('BLIND', '2026-11-06 02:51', '2026-11-06 02:51', 3), ('MOB', '2026-09-16 04:58', '2026-11-06 04:56', 170), ('MS', '2026-10-31 05:26', '2026-10-31 05:26', 2), ('SCI', '2026-10-31 05:26', '2026-10-31 05:26', 3)]
[('2026-09-16 00:00:00', '2026-09-18 05:00:00', '2026-09-16 06:01', '2026-09-18 20:12')]
[exit 0]
```

```
$ cd /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1 && python3 -I runsum.py
p3_DEAF (9, 3, 'DEAF', None, 'provisional', '○', 'universal', 'pilot-4', None) gov_by_lens [('MOB', 35)] links 122 gov_src 27 sha 4177fbdf644f
p3_MOB (9, 3, 'MOB', None, 'provisional', '○', 'universal', 'pilot-4', None) gov_by_lens [('MOB', 35)] links 122 gov_src 27 sha f9331c6d7d54
p3_BLIND (9, 3, 'BLIND', None, 'provisional', '○', 'universal', 'pilot-4', None) gov_by_lens [('MOB', 35)] links 122 gov_src 27 sha 65e54d87affa
p3_ALL (9, 3, 'ALL', None, 'provisional', '○', 'universal', 'pilot-4', None) gov_by_lens [('MOB', 35)] links 122 gov_src 27 sha 7d48dc03e56a
p3_AREACH (9, 3, None, 'A-REACH', 'provisional', '○', 'universal', 'pilot-4', None) gov_by_lens [('MOB', 35)] links 122 gov_src 27 sha 12468aa459cf
p12_MOB (9, 12, 'MOB', None, 'provisional', '○', 'universal', 'pilot-4', None) gov_by_lens [('MOB', 20)] links 21 gov_src 10 sha 6d98f4f7f93e
p7_DEAF (9, 7, 'DEAF', None, 'pending', None, 'population', 'pilot-4', 'GAP-103') gov_by_lens [] links 0 gov_src 0 sha 01d7cb63f433
[exit 0]
```

```
$ python3 -I -c "
import sqlite3
c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute('select parameter_id, identity_code, count(*) from source_value_extractions where identity_code in (\'ALL\',\'BLIND\') group by 1,2').fetchall())
"
python3 -I -c "
import json
for n in ['p3_DEAF','p12_MOB','p7_DEAF']:
    d=json.load(open('/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/'+n+'.json'))
    print(n, {k:(v if not isinstance(v,(list,dict)) else '...') for k,v in d.items()})
"
[(4, 'ALL', 11), (5, 'ALL', 2), (6, 'ALL', 3), (8, 'ALL', 1), (8, 'BLIND', 3), (9, 'ALL', 12), (11, 'ALL', 5)]
Traceback (most recent call last):
  File "<string>", line 5, in <module>
    print(n, {k:(v if not isinstance(v,(list,dict)) else '...') for k,v in d.items()})
                                                                           ^^^^^^^
AttributeError: 'list' object has no attribute 'items'
[exit 1]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/p3_DEAF.db python3 scripts/validate_evidence_state.py; echo EXIT=$?
OK cell-state machine: 9 cells, 6 convergence rows validated from p3_DEAF.db

PASS: 15 records checked, 0 errors, 0 warnings
EXAMINED: 15
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/p3_DEAF.db python3 scripts/audit/derivation_handshake_integrity.py; echo EXIT=$?
======================================================================
derivation_handshake_integrity
======================================================================

  determinations: 1  gates: 1 (1 open)  distinct (population, ICF code) pairs: 56
EXAMINED: 2
VERDICT: CLEAN
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/p3_DEAF.db python3 scripts/audit/extraction_follow_up_audit.py; echo EXIT=$?
extraction_follow_up_audit — open follow-ups; live values resting on one
EXAMINED: 1
  follow-ups: 0 raised, 0 open
  live determinations: 1
PASS: no live determination rests on an open follow-up or a skimmed figure
EXIT=0
[exit 0]
```

```
$ python3 -I -c "
import sqlite3
c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute('select b.parameter_id, t.canonical_en from base_parameters b join terms t using(term_id) where b.parameter_id in (3,7,12)').fetchall())"
[(3, 'ramp gradient'), (7, 'reverberation time'), (12, 'ramp run length')]
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db python3 scripts/validate_evidence_state.py; echo EXIT=$?
OK cell-state machine: 8 cells, 5 convergence rows validated from live.db

PASS: 13 records checked, 0 errors, 0 warnings
EXAMINED: 13
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db python3 scripts/audit/derivation_handshake_integrity.py; echo EXIT=$?
======================================================================
derivation_handshake_integrity
======================================================================
  specifications holds 0 rows.
  NOT a check with nothing to say: it is the corpus state. `specifications`
  cannot accept a row until a parameter is minted (CLAUDE.md §4), and none
  has been since the 2026-09-13 circulation clear. Every subject here is
  therefore unreachable today — which is why this check is advisory and why
  its own failure paths are exercised by fault injection against a scratch
  copy rather than by the live corpus.

  determinations: 0  gates: 1 (1 open)  distinct (population, ICF code) pairs: 56
EXAMINED: 1
VERDICT: CLEAN
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db python3 scripts/audit/extraction_follow_up_audit.py; echo EXIT=$?
extraction_follow_up_audit — open follow-ups; live values resting on one
EXAMINED: 0
  follow-ups: 0 raised, 0 open
  live determinations: 0 -- none exists, so the second half examines nothing
PASS: no live determination rests on an open follow-up or a skimmed figure
EXIT=0
[exit 0]
```

```
$ sed -n '240,252p' scripts/validate_evidence_state.py
    # migration-027 schema; select it where present, marker-check `tier_basis`
    # everywhere (pre-027 DBs stay validatable).
    have_rso = any(r[1] == "regulatory_stratum_only"
                   for r in conn.execute("PRAGMA table_info(specifications)"))
    cols += ",tier_basis" + (",regulatory_stratum_only" if have_rso else "")
    n = 0
    for row in conn.execute(f"SELECT {cols} FROM specifications"):
        (specification_id, parameter_id,
         identity_code, icf_code, needs_code, medical_code,
         state, design_scale, conv_id,
         cdp, cda, csb, gap_id, na_rat,
         governing_refs, code_floor_only, tier_basis) = row[:17]
        rso = row[17] if have_rso else 0
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/yml.py
stages ['base', 'research', 'evidence', 'judgment', 'synthesis', 'specification', 'render']
base entry 1 criteria 9 check-null 1 ['base-direction-from-source']
research entry 1 criteria 1 check-null 0 []
evidence entry 1 criteria 2 check-null 0 []
judgment entry 1 criteria 5 check-null 2 ['convergence-independence', 'comparator-recorded']
synthesis entry 1 criteria 1 check-null 1 ['opus-routing']
specification entry 1 criteria 5 check-null 0 []
render entry 1 criteria 2 check-null 1 ['register-invariants']
status PROPOSED False
checks 75 Counter({'advisory': 43, 'blocking': 30, 'informational': 2}) 5
migration_reproducibility blocking None None
alias_provenance_audit blocking None None
scan_debt advisory None None
verified_scan_integrity advisory None None
extraction_follow_up_audit advisory None None
claude_md_spine blocking None None
validate_evidence_state blocking None None
research_dod_session blocking True None
metadata_integrity_audit advisory None None
judgment_handoff_shape blocking None None
identifier_floor_audit blocking None None
derivation_handshake_integrity advisory None None
adjudication_integrity blocking None None
stage-map keys ['version', 'judged_by', 'judged_on', 'judged_against', 'tables', 'disputed']
[exit 0]
```

```
$ grep -c walkability governance/check-registry.yaml; grep -n -i 'STILL OWED' governance/stage-map.yaml | head; grep -n '^views' governance/stage-map.yaml
0
31:# STILL OWED: the 20 views. §8 specifies a `pointer:` list naming the stages each
[exit 1]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 300 python3 scripts/audit/claude_md_spine.py; echo EXIT=$?
EXAMINED: 7 contract stage(s) against 1 SPINE line
PASS: SPINE matches governance/pipeline-contract.yaml — base -> research -> evidence -> judgment -> synthesis -> specification -> render
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 300 python3 scripts/audit/identifier_floor_audit.py; echo EXIT=$?
EXAMINED: 3 identifier floor(s) against 226 committed migration file(s)
  ref_id            historical REF-01036   live REF-01036
  base_parameters   historical 12            live 12  (sqlite_sequence)
  specifications    historical 8             live 8  (sqlite_sequence)
VERDICT: CLEAN
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 300 python3 scripts/audit/adjudication_integrity.py; echo EXIT=$?
======================================================================
adjudication_integrity.py — evidence-adjudication substrate
======================================================================
[1] PASS: all 59 evidence_sources are tier-consistent (stored tier == derive_tier(evidence_type, scope)).

[readiness] determination-field coverage (honest; not a pass/fail):
    specifications: 8 determination(s)
        state distribution: {'pending': 3, 'provisional': 5}
        excluded from best-practice: regulatory_stratum_only=2, code_floor_only=1
    source_value_extractions: 214 row(s) — value-directness assessable
    convergence_assessment: {'pending_assessment': 5}

[siblings] authoritative §10 enforcers (not re-run here):
    matrix_consistency.py (grain×scale matrix) · validate_evidence_state.py (per-cell state machine)

======================================================================
EXAMINED: 59
VERDICT: PASS   (tier inconsistencies=0)
======================================================================
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 300 python3 scripts/audit/judgment_handoff_shape.py; echo EXIT=$?
EXAMINED: 3 invariant(s) of the evidence->judgment hand-off
  - source_value_extractions.ref_id NOT NULL
  - no UNIQUE index on source_value_extractions
  - source_value_extractions.ref_id -> evidence_sources(ref_id)
PASS: shape holds (source_value_extractions currently 214 rows — shape is checked, not content).
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 300 python3 scripts/audit/alias_provenance_audit.py; echo EXIT=$?
==========================================================================
alias_provenance_audit.py — controlled-vocabulary provenance
==========================================================================
database: /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db
aliases:  2382
EXAMINED: 2382

lang    total  verified  attested  model-gen  curated  code  UNKNOWN
--------------------------------------------------------------------
da        157         0         0         80        0     0       77
de        191         0         0        115        0     0       76
en        415         0         0          0      304    20       91
es        171         0         0        110        0     0       61
fi        160         0         0         82        0     0       78
fr        170         0         0        113        0     0       57
id         15        15         0          0        0     0        0
it        121         0         0         70        0     0       51
ja        150         0         0         92        0     0       58
ko        157         0         0         92        0     0       65
nl        140         0         0         86        0     0       54
no        132         0         0         79        0     0       53
pt        114         0         0         70        0     0       44
sv        134         0         0         81        0     0       53
zh        155         0         0         93        0     0       62
--------------------------------------------------------------------
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 300 python3 scripts/audit/jurisdiction_db_vocabulary.py; echo EXIT=$?
Rejected spellings, read from governance/jurisdiction-philosophy.md: {'GB': 'UK'}
Declared codes in JurisdictionCode: 36
Tables with a jurisdiction column (derived, 1 exempt, 1 candidate-only): 8
REPORTED (base vocabulary, not blocking -- owner decision):
  term_aliases.jurisdiction: 1 row(s) hold 'TW', which JurisdictionCode does not declare. Either it is a real jurisdiction the owner should admit to the enum, or it is not a jurisdiction at all and the value is mis-filed.
  term_aliases.jurisdiction: 1 row(s) hold 'colloquial', which JurisdictionCode does not declare. Either it is a real jurisdiction the owner should admit to the enum, or it is not a jurisdiction at all and the value is mis-filed.
EXAMINED: 114 (table x rejected-spelling pair)
VERDICT: PASS
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 300 python3 scripts/audit/scan_debt.py 2>&1 | tail -12; echo EXIT=${PIPESTATUS[0]}
  NOT-READ            417
  full readings nothing counted (text_scope 'full', pages_read NULL): 4 -- the operator's claim, not a count
  parameter 4 (corridor width): 47 not read, 4 read only partially -- REF-00977, REF-00979, REF-00980, REF-00983, REF-00984, REF-00985, REF-00986, REF-00988, REF-00989, REF-00990, REF-00991, REF-00993, REF-00994, REF-00995, REF-00996, REF-00997, REF-00998, REF-00999, REF-01000, REF-01001 ...
  parameter 5 (turning circle): 47 not read, 5 read only partially -- REF-00977, REF-00979, REF-00980, REF-00983, REF-00984, REF-00985, REF-00986, REF-00988, REF-00989, REF-00990, REF-00991, REF-00993, REF-00994, REF-00995, REF-00996, REF-00997, REF-00998, REF-00999, REF-01000, REF-01001 ...
  parameter 6 (operating force): 47 not read, 4 read only partially -- REF-00977, REF-00979, REF-00980, REF-00983, REF-00984, REF-00985, REF-00986, REF-00988, REF-00989, REF-00990, REF-00991, REF-00993, REF-00994, REF-00995, REF-00996, REF-00997, REF-00998, REF-00999, REF-01000, REF-01001 ...
  parameter 7 (reverberation time): 47 not read, 5 read only partially -- REF-00977, REF-00979, REF-00980, REF-00983, REF-00984, REF-00985, REF-00986, REF-00988, REF-00989, REF-00990, REF-00991, REF-00993, REF-00994, REF-00995, REF-00996, REF-00997, REF-00998, REF-00999, REF-01000, REF-01001 ...
  parameter 8 (LRV contrast): 47 not read, 5 read only partially -- REF-00977, REF-00979, REF-00980, REF-00983, REF-00984, REF-00985, REF-00986, REF-00988, REF-00989, REF-00990, REF-00991, REF-00993, REF-00994, REF-00995, REF-00996, REF-00997, REF-00998, REF-00999, REF-01000, REF-01001 ...
  parameter 9 (door width): 47 not read, 4 read only partially -- REF-00977, REF-00979, REF-00980, REF-00983, REF-00984, REF-00985, REF-00986, REF-00988, REF-00989, REF-00990, REF-00991, REF-00993, REF-00994, REF-00995, REF-00996, REF-00997, REF-00998, REF-00999, REF-01000, REF-01001 ...
  parameter 10 (colour temperature): 47 not read, 5 read only partially -- REF-00977, REF-00979, REF-00980, REF-00983, REF-00984, REF-00985, REF-00986, REF-00988, REF-00989, REF-00990, REF-00991, REF-00993, REF-00994, REF-00995, REF-00996, REF-00997, REF-00998, REF-00999, REF-01000, REF-01001 ...
  parameter 11 (headroom clearance): 47 not read, 5 read only partially -- REF-00977, REF-00979, REF-00980, REF-00983, REF-00984, REF-00985, REF-00986, REF-00988, REF-00989, REF-00990, REF-00991, REF-00993, REF-00994, REF-00995, REF-00996, REF-00997, REF-00998, REF-00999, REF-01000, REF-01001 ...
  parameter 12 (ramp run length): 41 not read, 3 read only partially -- REF-00977, REF-00979, REF-00980, REF-00983, REF-00984, REF-00985, REF-00986, REF-00989, REF-00990, REF-00991, REF-00993, REF-00994, REF-00996, REF-00997, REF-00998, REF-00999, REF-01000, REF-01001, REF-01002, REF-01003 ...
DEBT: 457 pair(s). Read each source against the whole list and record it (db.py record-scan; scripts/research/full_text.py derives a held PDF's text), or a targeted reading for one new parameter (record-scan --mode targeted).
EXIT=1
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 300 python3 scripts/audit/verified_scan_integrity.py 2>&1 | tail -12; echo EXIT=${PIPESTATUS[0]}
    REF-01020: 4 row(s) (parameter, extraction): [(3, 84), (3, 85), (3, 86), (3, 106)]
    REF-01021: 2 row(s) (parameter, extraction): [(3, 87), (3, 88)]
    REF-01022: 1 row(s) (parameter, extraction): [(3, 112)]
    REF-01023: 1 row(s) (parameter, extraction): [(3, 90)]
    REF-01024: 2 row(s) (parameter, extraction): [(3, 113), (3, 114)]
    REF-01025: 2 row(s) (parameter, extraction): [(3, 93), (3, 94)]
    REF-01026: 3 row(s) (parameter, extraction): [(3, 95), (3, 96), (3, 97)]
    REF-01027: 3 row(s) (parameter, extraction): [(3, 98), (3, 99), (12, 141)]
    REF-01029: 2 row(s) (parameter, extraction): [(3, 101), (3, 102)]
    REF-01030: 7 row(s) (parameter, extraction): [(3, 103), (3, 104), (3, 105), (3, 128), (3, 129), (12, 145), (12, 146)]
    remedy: record the reading (db.py record-scan)
FAIL: 140 (row, class) pair(s) across 212 live extraction(s); each class above names its remedy.
EXIT=1
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 300 python3 scripts/audit/metadata_integrity_audit.py 2>&1 | tail -12; echo EXIT=${PIPESTATUS[0]}
[2] INFO: 30 / 50 eligible rows lack a cross-check record (60.0% — pre-DR-2026-05-20 legacy)
    These rows cleared rule #10's existence gate but predate the cross-check
    protocol. Future synthesis claims on these rows should run cross-check first.

[3] INFO: Owner-review queue (metadata_integrity_status NOT IN ('OK','RESOLVED',NULL))
    Total: 24 rows
      CORRECTED                 24

======================================================================
VERDICT: FAIL
EXAMINED: 59
======================================================================
EXIT=1
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 300 python3 scripts/audit/medical_lens_integrity.py 2>&1 | tail -12; echo EXIT=${PIPESTATUS[0]}
  base_taxonomy_medical holds 0 rows.
  NOT an unexecuted ruling: D-0170 adopted the lens 2026-08-27. And NOT
  licensing — the owner ruled 'use ICD-11' on 2026-09-11, which this message
  went on claiming for an hour after the fact (swept 2026-09-11, rule 4:
  prose callers are the ones no gate covers).
  The lens is populated by CORRESPONDENCE from the identity and axis
  registries, bounded at roughly 15-20 rows, plus on demand thereafter.
  See references/project-standards.md, the 2026-09-11 entries.

  unverified anchors: 0 of 0
EXAMINED: 0
VERDICT: CLEAN
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 300 python3 scripts/audit/skill_vocabulary_audit.py 2>&1 | tail -12; echo EXIT=${PIPESTATUS[0]}
  skills/functional-deficit-researcher_SKILL.md: COMPOUND-CONFLICTS, COMPOUND-NOVEL, COMPOUND-REFINES, FDR-RRC-01, TIER-0-CANDIDATE, connection-scout, functional_deficit_pass, item-specification-writer
  skills/gap-driven-mining_SKILL.md: CLOSED-FIXED, FIRED, THIN-BASE, UNVERIFIED-1, candidate-dois, co1_zero_jurisdictions, cross_population_invisibility, evidence_path, numerical_spec_uncited, qualitative_uncited, rules_in_scope, standards_not_promoted, thin_base_primary_clinical, update-gap-research-fields, web_fetch
  skills/github-io_SKILL.md: web_fetch
  skills/integrity-protocol_SKILL.md: DEVIATION-LOGGED, PREDICTED, UNVERIFIED-1, schema_reference_drift_audit.py
  skills/multilingual-research_SKILL.md: DISCARDED, INTEGRATED, best_practice_synthesis, co1_pass_summary, jurisdiction_coverage, native_aliases, not-run
  skills/run-pipeline_SKILL.md: CO1-NOT-APPLICABLE
  skills/session-consolidator_SKILL.md: concurrent_sessions, connection-scout, last_searched, multilingual_research_adaptations, multilingual_research_run_count, next_action, session_, session_083.md, session_084.md
  skills/supersession-audit_SKILL.md: bpc_metadata, supersession_check.checked_at
  skills/toc-editor_SKILL.md: DELETE, REDIRECT
  .claude/commands/batch-done.md: record_file
  .claude/agents/antagonist.md: min_items
FAIL: 76 token(s) in 18 file(s) name a value, column or code the repository holds nowhere. Correct the sentence (rule 4: prose is a caller), or give the value a typed home first.
EXIT=1
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 300 python3 scripts/audit/schema_reference_audit.py 2>&1 | tail -12; echo EXIT=${PIPESTATUS[0]}
EXAMINED: 1125 SQL identifier references in 188 files against 80 live tables and views
  KNOWN: evidence_sources_v1_legacy  (2 site(s)) — Guarded reference. scripts/tests/test_db_integrity.py reads it only after SELECT COUNT(*) FROM sqlite_master WHERE name='evidence_sources_v1_legacy' returns non-zero -- the parity check runs only while the legacy table exists.
  KNOWN: items  (1 site(s)) — Deliberate reference to the PRE-RESET corpus, not the live schema. scripts/db.py (_item_subject) opens _archived/data/corpus-pre-reset-2026-08-06.db read-only and immutable and reads its `items.name`, the 93 item subjects the owner admitted as a basis on 2026-11-06 (ledger: "Owner statements 2026-11-06"). The live database has no `items` table (migration drop_item_layer_cluster) and a rebuild does not restore one.
  KNOWN: no_such_table  (1 site(s)) — Selftest fixture in scripts/audit/graph_audit.py, same purpose as zzz_phantom.
  KNOWN: real_table  (1 site(s)) — Selftest fixture in scripts/audit/graph/extract_code.py, proving the extractor distinguishes a real CREATE TABLE from a mention of one.
  KNOWN: zzz_phantom  (1 site(s)) — Selftest fixture in scripts/audit/graph_audit.py -- a table name chosen BECAUSE it does not exist, to prove the audit reports a phantom.
RESULT: PASS — every table and view a caller names exists
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db python3 scripts/audit/scan_debt.py | head -12
scan_debt — (source x active parameter) pairs not yet read in full
EXAMINED: 580
  EXTRACTED           94
  STATED-ABSENT       7
  BLOCKED             0
  READ-NOTHING-FOUND  22
  READ-PARTIAL        40
  NOT-READ            417
  full readings nothing counted (text_scope 'full', pages_read NULL): 4 -- the operator's claim, not a count
  parameter 4 (corridor width): 47 not read, 4 read only partially -- REF-00977, REF-00979, REF-00980, REF-00983, REF-00984, REF-00985, REF-00986, REF-00988, REF-00989, REF-00990, REF-00991, REF-00993, REF-00994, REF-00995, REF-00996, REF-00997, REF-00998, REF-00999, REF-01000, REF-01001 ...
  parameter 5 (turning circle): 47 not read, 5 read only partially -- REF-00977, REF-00979, REF-00980, REF-00983, REF-00984, REF-00985, REF-00986, REF-00988, REF-00989, REF-00990, REF-00991, REF-00993, REF-00994, REF-00995, REF-00996, REF-00997, REF-00998, REF-00999, REF-01000, REF-01001 ...
  parameter 6 (operating force): 47 not read, 4 read only partially -- REF-00977, REF-00979, REF-00980, REF-00983, REF-00984, REF-00985, REF-00986, REF-00988, REF-00989, REF-00990, REF-00991, REF-00993, REF-00994, REF-00995, REF-00996, REF-00997, REF-00998, REF-00999, REF-01000, REF-01001 ...
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db python3 scripts/audit/metadata_integrity_audit.py | head -22
======================================================================
metadata_integrity_audit.py (per DR-2026-05-20)
======================================================================

[1] FAIL: 20 COMPLETE/COMPLETE-STATUTORY rows with open integrity flag
    REF-00139  mq=COMPLETE-STATUTORY vs=VERIFIED   mis=CORRECTED
      detail: 2026-10-31 verification_note CORRECTED (R9a asks for the held id to be reused; the row must say what
    REF-00977  mq=COMPLETE           vs=VERIFIED   mis=CORRECTED
      detail: 2026-09-18 jurisdiction CORRECTED (Filed NULL in batch 15. INT rather than a country code: a systema
    REF-00992  mq=COMPLETE-STATUTORY vs=VERIFIED   mis=CORRECTED
      detail: 2026-09-18 jurisdiction CORRECTED (Normalised GB->UK. governance/jurisdiction-philosophy.md line 127
    REF-00999  mq=COMPLETE           vs=VERIFIED   mis=CORRECTED
      detail: 2026-09-18 jurisdiction CORRECTED (Filed NULL in batch 15 though determinable and known at admission
    REF-01000  mq=COMPLETE           vs=VERIFIED   mis=CORRECTED
      detail: 2026-09-18 jurisdiction CORRECTED (Filed NULL in batch 15 though determinable: the study is of Londo
    REF-01002  mq=COMPLETE           vs=UNVERIFIED mis=CORRECTED
      detail: 2026-09-18 verification_status CORRECTED (I4 CAUGHT A GRADING ERROR AND THE CHECK IS RIGHT. I4 asser
    REF-01005  mq=COMPLETE           vs=VERIFIED   mis=CORRECTED
      detail: 2026-09-19 doi_resolution_outcome CORRECTED (R9/R10 DOI pre-check RUN AND RECORDED, which it had not
    REF-01006  mq=COMPLETE           vs=VERIFIED   mis=CORRECTED
      detail: 2026-09-20 source_type CORRECTED (Wrote Crossref's spelling 'journal-article' at admission; the voca
    REF-01009  mq=COMPLETE           vs=VERIFIED   mis=CORRECTED
Traceback (most recent call last):
  File "/home/user/guidebook/scripts/audit/metadata_integrity_audit.py", line 117, in <module>
    sys.exit(audit())
             ~~~~~^^
  File "/home/user/guidebook/scripts/audit/metadata_integrity_audit.py", line 62, in audit
    print(f"      detail: {(r[4] or '')[:100]}")
    ~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
BrokenPipeError: [Errno 32] Broken pipe
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute('select status,count(*) from v_scan_ledger group by 1').fetchall())
print(c.execute('select mode,text_scope,method,open_pass_done,count(*),count(distinct ref_id) from source_scans group by 1,2,3,4').fetchall())
print(c.execute('select count(*) from evidence_sources').fetchall())
"
[('EXTRACTED', 94), ('NOT-READ', 417), ('READ-NOTHING-FOUND', 22), ('READ-PARTIAL', 40), ('STATED-ABSENT', 7)]
[('catalogue', 'abstract', 'pre-screen', 0, 4, 4), ('catalogue', 'full', 'pre-screen', 0, 12, 6), ('catalogue', 'partial', 'pre-screen', 0, 2, 1)]
[(59,)]
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute(\"select sql from sqlite_master where name='source_scans'\").fetchone()[0])
print(c.execute(\"select sql from sqlite_master where name='v_scan_ledger'\").fetchone()[0])
"
CREATE TABLE source_scans (
    -- AUTOINCREMENT, as 076 did for the other ids a record names: a scan_id is cited by
    -- session records and must never come to mean a different reading.
    scan_id             INTEGER PRIMARY KEY AUTOINCREMENT,
    ref_id              TEXT    NOT NULL REFERENCES evidence_sources(ref_id),
    -- catalogue: every active parameter up to catalogue_version.
    -- targeted:  one parameter, target_parameter_id (a back-fill reading).
    mode                TEXT    NOT NULL CHECK (mode IN ('catalogue', 'targeted')),
    catalogue_version   INTEGER NOT NULL CHECK (catalogue_version >= 1),
    target_parameter_id INTEGER REFERENCES base_parameters(parameter_id),
    -- full: the whole document. partial: some pages of it. fragment: one page or clause
    -- of a larger instrument. abstract: an abstract or metadata record only.
    text_scope          TEXT    NOT NULL CHECK (text_scope IN
                                ('full', 'partial', 'fragment', 'abstract')),
    pages_read          INTEGER CHECK (pages_read IS NULL OR pages_read >= 0),
    pages_total         INTEGER CHECK (pages_total IS NULL OR pages_total >= 1),
    -- Which saved file was read, by checksum: the manifest's own sha256 of the bytes.
    file_sha256         TEXT    NOT NULL CHECK (length(file_sha256) = 64),
    -- Whether the open pass (quantities the catalogue lacks, plan section 3.4) was done
    -- in this reading.
    open_pass_done      INTEGER NOT NULL DEFAULT 0 CHECK (open_pass_done IN (0, 1)),
    -- full-read: the text was read against the list. pre-screen: only a script listed
    -- where catalogue terms occur -- weaker, and v_scan_ledger says which it was.
    method              TEXT    NOT NULL CHECK (method IN ('full-read', 'pre-screen')),
    notes               TEXT,
    created_at          TEXT    NOT NULL,
    created_by_session  TEXT    NOT NULL,
    updated_at          TEXT,
    updated_by_session  TEXT,
    CHECK ((mode = 'targeted' AND target_parameter_id IS NOT NULL)
        OR (mode = 'catalogue' AND target_parameter_id IS NULL)),
    CHECK (pages_read IS NULL OR pages_total IS NULL OR pages_read <= pages_total),
    -- "full" over a paged text means every page; a reading of fewer pages is partial.
    CHECK (text_scope <> 'full' OR pages_read IS NULL OR pages_read = pages_total)
)
CREATE VIEW v_scan_ledger AS
-- v_scan_ledger: one row per (source in scope) x (active parameter).
--
--   source in scope   evidence_sources with superseded_by_ref_id IS NULL. A tombstone is
--                     never read again; its replacement is.
--   active parameter  base_parameters.status = 'active'. Retired and merged parameters
--                     leave the ledger (their extractions stay, as history).
--
-- STATUS PRECEDENCE, first match wins:
--   1 EXTRACTED          a non-absent extraction exists for the pair (any figure_role).
--   2 STATED-ABSENT      only claim_type 'absent' extractions exist: the source addresses
--                        the quantity and sets nothing -- a positive statement.
--   3 READ-NOTHING-FOUND a FULL-scope reading covers the pair and found no row.
--   4 BLOCKED            no full reading covers the pair AND the source carries an obstacle
--                        processing_blocked_reason (below): the full text could not be
--                        obtained or read, so the pair is not reading debt until a full
--                        reading is recorded. Any partial / fragment / abstract reading of
--                        the pair is still named in scan_id / text_scope / method.
--   5 READ-PARTIAL       only partial / fragment / abstract readings cover it, and no
--                        obstacle stands: the full text is obtainable and unread -- debt.
--   6 NOT-READ           no reading covers it.
-- WHY THIS ORDER (it is derived from what each fact proves; 122 ranked BLOCKED above every
-- reading and 123 below every reading, both guesses): a FULL reading proves the obstacle
-- gone, since the whole text was read, so 3 outranks 4. A partial, fragment or abstract
-- reading proves nothing about the full text, so under a standing obstacle 4 outranks 5.
-- A reading COVERS a pair when it is catalogue-mode with catalogue_version >= parameter_id
-- (the parameter existed when the reading was made), or targeted at that parameter. Rows 1
-- and 2 win over readings because a row written is stronger evidence than a reading
-- recorded; 3 wins over the rest because a full reading supersedes a partial one.
--
-- THE BLOCKED CASE BELOW IS THE ONE HOME of "the text could not be obtained or read", and
-- this header is the ONE HOME of the classification of every processing_blocked_reason
-- value (evidence_sources CHECK, migration 091); each value appears here as a bare token
-- under exactly one head, and a test derives the CHECK and fails on a value this header
-- does not name. The writers and gates read this view's status, never the column. NOTHING
-- CLEARS THE COLUMN: it is the retrieval record and stays as history; the ledger alone says
-- whether a pair is still blocked.
--   obstacle to the text (BLOCKED, above):  no-full-text, paywalled, language.
--   copy of a typed fact (not an obstacle; the writers refuse it by pointer -- the judgement
--     lives in db.py _BLOCK_REASON_COPIES): no-quantified-claims -> a recorded full reading;
--     superseded -> superseded_by_ref_id.
--   pending owner question 8 of the round-3 adjudication, treated as NULL (the source owes
--     its reading): out-of-scope, tier-not-required (they say no text was unobtainable);
--     no-doi, not-indexed (migration 091's comments describe discovery -- "no resolvable
--     identifier for automated paths", "absent from the indexes the pipeline queries" --
--     not an obstacle to a text in hand, and a URL-only report admitted without a DOI can
--     be read).
--
-- scan_id / text_scope / method name the STRONGEST covering reading (full scope first,
-- then full-read before pre-screen, then the latest), so a READ-NOTHING-FOUND resting on
-- a pre-screen only is visible as such. NULL when no reading covers the pair.
WITH pairs AS (
    SELECT e.ref_id, p.parameter_id, e.processing_blocked_reason
      FROM evidence_sources e
     CROSS JOIN base_parameters p
     WHERE e.superseded_by_ref_id IS NULL
       AND p.status = 'active'
),
best AS (
    SELECT pr.ref_id, pr.parameter_id, pr.processing_blocked_reason,
           (SELECT s.scan_id FROM source_scans s
             WHERE s.ref_id = pr.ref_id
               AND ((s.mode = 'catalogue' AND s.catalogue_version >= pr.parameter_id)
                 OR (s.mode = 'targeted' AND s.target_parameter_id = pr.parameter_id))
             ORDER BY (s.text_scope = 'full') DESC, (s.method = 'full-read') DESC,
                      s.scan_id DESC
             LIMIT 1) AS scan_id
      FROM pairs pr
)
SELECT b.ref_id,
       b.parameter_id,
       CASE
         WHEN EXISTS (SELECT 1 FROM source_value_extractions x
                       WHERE x.ref_id = b.ref_id AND x.parameter_id = b.parameter_id
                         AND x.claim_type <> 'absent') THEN 'EXTRACTED'
         WHEN EXISTS (SELECT 1 FROM source_value_extractions x
                       WHERE x.ref_id = b.ref_id AND x.parameter_id = b.parameter_id
                         AND x.claim_type = 'absent') THEN 'STATED-ABSENT'
         WHEN s.text_scope = 'full' THEN 'READ-NOTHING-FOUND'
         WHEN b.processing_blocked_reason IN
              ('no-full-text', 'paywalled', 'language') THEN 'BLOCKED'
         WHEN s.scan_id IS NOT NULL THEN 'READ-PARTIAL'
         ELSE 'NOT-READ'
       END AS status,
       b.scan_id,
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/b1.py
REQ-013 governing_refs [(8, 5, 8)]
REQ-021 absence_class [(203, 0)]
REQ-028 obs/adj [(96, 90)]
REQ-029 params/adj [(10, 6)]
REQ-029 declined ERR no such column: parameter_declined_reason
REQ-029 adj outcomes [('DEFERRED', 24), ('NAMES-EXISTING', 46), ('NAMES-NEW', 6), ('NOT-OURS', 14)]
REQ-030 followups [(0,)]
REQ-036 mining [(38, 13)]
REQ-040 gaps cols [('gap_id,category,priority,status,skill,section,description,created_at,created_by_session,updated_at,updated_by_session,falsification_condition,confidence_interval,shift_conditions,named_dissenter,mining_addressability',)]
REQ-040 gaps [('NOT-ADDRESSABLE', 4), ('NULL', 106)]
REQ-040 gap_mining [(0,)]
REQ-042 rooms [(17,)]
REQ-043 [(0, 0, 0)]
REQ-047 loc status [('PROMOTED', 1), ('REFERENCE-ONLY', 879), ('RETIRED', 13)]
REQ-047 blocked reason [('NULL', 59)]
REQ-049 [(38, 13)]
REQ-051 Q7 [(12,)]
REQ-053 langs [(13, 2)]
REQ-053 slugs [(106,)]
REQ-055 canonical_en [("CREATE TABLE terms (\n    term_id             TEXT PRIMARY KEY,\n    canonical_en        TEXT NOT NULL,\n    definition          TEXT,\n    domain              TEXT,\n    scope_note          TEXT,\n    created_at          TEXT NOT NULL,\n    created_by_session  TEXT NOT NULL,\n    updated_at          TEXT NOT NULL,\n    updated_by_session  TEXT NOT NULL\n, catalogue TEXT\n    CHECK (catalogue IN ('references/standards-registry.md', 'references/tier456-verified-sources.json', 'references/co1-verified-sources.json', 'references/co2-verified-sources.json', '_archived/data/corpus-pre-reset-2026-08-06.db')), catalogue_entry_ref TEXT, catalogue_approval_ref TEXT\n    CHECK ((catalogue IS NULL AND catalogue_entry_ref IS NULL AND catalogue_approval_ref IS NULL)\n        OR (catalogue IS NOT NULL\n            AND catalogue_entry_ref IS NOT NULL AND length(trim(catalogue_entry_ref)) > 0\n            AND catalogue_approval_ref IS NOT NULL AND length(trim(catalogue_approval_ref)) > 0)))",)]
REQ-057 Q40 [('TERM-001', 'hellingbaan', 'nl', 'SYNONYM'), ('TERM-001', '傾斜路', 'ja', 'SYNONYM')]
REQ-057 adj [(9, '傾斜路', 'JA', 'NAMES-EXISTING', 'TERM-089'), (76, 'hellingbaan', 'NL', 'NAMES-EXISTING', 'TERM-089'), (77, 'hellingbaan', 'NL', 'NAMES-EXISTING', 'TERM-089')]
REQ-061 Q39 [(94, 0)]
REQ-064 scope [(70, 0)]
REQ-064 langs [('AR', 2), ('BN', 1), ('DA', 2), ('DE', 5), ('EN', 20), ('ES', 11), ('FI', 2), ('FR', 6), ('HI', 1), ('ID', 1), ('IT', 3), ('JA', 1), ('KO', 1), ('NL', 3), ('NO', 1), ('PT', 3), ('SV', 3), ('SW', 2), ('ZH', 2)]
REQ-064 scoped-out in scope view [(6,)]
REQ-066 [(0, 'clinical', 13), (0, 'co1', 2), (0, 'code', 4), (0, 'grey', 3), (0, 'national_fw', 2), (0, 'sr_meta', 1), (0, 'standard_eb', 2), (1, 'clinical', 4), (1, 'co1', 2), (1, 'code', 17), (1, 'grey', 3), (1, 'national_fw', 5), (1, 'sr_meta', 1)]
REQ-067 [(0, 0)]
REQ-067 supersession_check [(0,)]
REQ-069 Ontario [('REF-01013', 'CA', 'Ontario Building Code — O. Reg. 163/24, s.3.8.3.4 Ramps (barrier-free path of travel)')]
REQ-071 [(0, 8, 59)]
REQ-073 lens [(212, 1, 3, 214)]
REQ-075 med [(0, 0, 0)]
REQ-079 [(214,)]
REQ-086 weighting [(5,)]
REQ-089 marker [(8, 0)]
REQ-092 verbexempt [(29, 214)]
REQ-094 passes [(9, 193)]
REQ-097 locator_scheme [(None, 44), ('page', 17), ('section', 153)]
REQ-097 sve cols loc [(15,)]
REQ-097 ex relations [('audited_against', 8), ('condition_on', 31), ('confirms', 3), ('exceeds', 1), ('insufficient', 4), ('tested_at', 10)]
REQ-099 base_parameters [('parameter_id,term_id,status,merged_into,notes,created_at,created_by_session,updated_at,updated_by_session,direction_rationale,accessibility_direction,direction_ref_id',)]
REQ-099 claimed_unit [(32, 41, 122)]
REQ-100 conn types [("CREATE TABLE connections (\n    con_id              TEXT PRIMARY KEY,\n    status              TEXT NOT NULL\n                        CHECK(status IN (\n                            'PENDING','CONSUMED','CONSUMED-DEFERRED','CLOSED'\n                        )),\n    confidence          TEXT NOT NULL\n                        CHECK(confidence IN ('HIGH','MODERATE')),\n    connection_type     TEXT\n                        CHECK(connection_type IN (\n                            'CROSS-POPULATION','CROSS-PARAMETER',\n                            'COMPOUND-INTERACTION','METHODOLOGY'\n                        )),\n    filed_in            TEXT NOT NULL REFERENCES slugs(slug),\n    description         TEXT,\n    source_skill        TEXT,\n    opus_reviewed       INTEGER NOT NULL DEFAULT 0 CHECK(opus_reviewed IN (0,1)),\n    created_at          TEXT NOT NULL,\n    created_by_session  TEXT NOT NULL,\n    updated_at          TEXT NOT NULL,\n    updated_by_session  TEXT NOT NULL\n)",)]
REQ-100 rows [(0, 0, 0, 5)]
HS-A04 engine [(21,)]
HS-A05 tables [('base_taxonomy_identity,rooms,base_taxonomy_medical,base_parameters,base_icf',)]
HS-A18 scale [('population', 1), ('universal', 7)]
HS-A12 cultural [(8, 0)]
HS-A11 freshness [(1,)]
orphan-ish: research_code_leads [(96,)]
orphan-ish: econ/case [(1, 0)]
Q13 [(18, 29, 214)]
Q8 [(105,)]
Q15 [(32, 17, 0)]
Q34 [('DE', 2), ('EN', 112), ('ES', 13), ('FI', 1), ('FR', 8), ('HR', 1), ('IT', 1), ('JA', 1), ('KO', 7), ('NL', 13), ('NO', 2), ('PT', 6), ('SV', 15), ('en', 13), ('fr', 2), ('ja', 3), ('nl', 3)]
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/b2.py
grey nonEN [('REF-01022', 'grey', 'nl', 'NL', 'Internetconsultatie verzamelbesluit Bbl 2024 (reactie van Ie'), ('REF-01025', 'grey', 'sv', 'SE', 'Yttrande över Boverkets remiss ang. Revidering av Boverkets '), ('REF-01029', 'grey', 'es', 'ES', 'Metodología para la evaluación e implementación de Accesibil')]
lang_detected values [(None, 8), ('EN', 6), ('FI', 1), ('de', 1), ('en', 21), ('es', 3), ('fr', 1), ('ja', 4), ('ko', 2), ('nl', 5), ('no', 1), ('pt', 3), ('sv', 3)]
decline [('term_aliases',), ('terms',), ('term_adjudications',), ('determination_gates',), ('parameter_declinations',), ('observed_terms',)]
decline2 ERR no such table: term_declinations
walk table list [(56,)]
views [(23,)]
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute('select count(*) from parameter_declinations').fetchall())"
grep -n '_VALUE_BEARING_NAME\|def _name_tokens\|def _near_terms\|def normalise_quote' scripts/db.py scripts/research/retrieval_log.py | head -20
[(1,)]
scripts/db.py:6406:# and gains nothing; every NAME field uses `_VALUE_BEARING_NAME`.
scripts/db.py:6407:_VALUE_BEARING_NAME = re.compile(
scripts/db.py:6412:def _name_tokens(name: str) -> frozenset:
scripts/db.py:6419:def _near_terms(conn, name: str) -> list:
scripts/db.py:6467:    vb = _VALUE_BEARING_NAME.search(canonical_en)
scripts/db.py:6620:    for field, val, rx in (("--display-name", display_name, _VALUE_BEARING_NAME),
scripts/db.py:6830:        vb = _VALUE_BEARING_NAME.search(term["canonical_en"])
scripts/db.py:7343:    vb = _VALUE_BEARING_NAME.search(new)
scripts/db.py:7714:    for flag, val, rx in (("--canonical-en", canonical_en, _VALUE_BEARING_NAME),
scripts/research/retrieval_log.py:605:def normalise_quote(text):
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/fn.py /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db
--- _VALUE_BEARING_NAME
'最小幅' False
'Mindestbreite' False
'largeur minimale' False
'幅１２００' False
'١٢٠٠ مم' False
'minimum width' True
'width 1200' True
'width ≥ 1200 mm' True
'最小幅 1200' True
--- _name_tokens
'勾配' frozenset()
'ramp gradient' frozenset({'gradient', 'ramp'})
'傾斜路' frozenset()
'पथ ढलान' frozenset()
'ลาดชัน' frozenset()
'منحدر' frozenset()
'שיפוע' frozenset()
'경사로' frozenset()
'κλίση' frozenset()
'слон' frozenset()
--- normalise_quote
'スロープ' 'スローフ' 'スローフ' 'スローフ' True
'スローブ' 'スローフ' 'スローフ' 'スローフ' True
'スロープ' 'スローフ' 'スローブ' 'スローフ' True
'が' 'か' 'か' 'か' True
'ばん' 'はん' 'はん' 'はん' True
'१२०० मिमी ढलान रेखा' '१२००ममढलनरख'
'ढलान रेखा' 'ढलनरख'
'ลาดชัน ๑๒๐๐' 'ลาดชน๑๒๐๐'
'ลาดชัน 1200' 'ลาดชน1200'
'١٢٠٠ مم' '١٢٠٠مم'
'1200 مم' '1200مم'
'ὁ λόγος' 'ολογος'
'ο λογος' 'ολογος'
'שִׁיפּוּעַ' 'שיפוע'
'שיפוע' 'שיפוע'
'１２００' '1200'
'1200' '1200'
[exit 0]
```

```
$ grep -n -E 'UPDATE +search_candidates|UPDATE +source_locators|resolved_ref_id *=|status *= *.PROMOTED|SET +status' scripts/db.py | head -30
260:            "UPDATE connections SET status=?, updated_at=?, updated_by_session=? WHERE con_id=?",
296:            "UPDATE gaps SET status=?, updated_at=?, updated_by_session=? "
4651:                "UPDATE search_candidates SET surfaced_in=?, surfaced_quote=? "
4668:                    "UPDATE search_candidates SET notes=?, updated_at=?, "
4700:        conn.execute("UPDATE search_candidates SET exec_id=?, notes=?, updated_at=?, "
5246:        conn.execute("UPDATE search_candidates SET disposition=?, notes=?, "
5247:                     "resolved_ref_id=COALESCE(?, resolved_ref_id), suggested_slug=?, "
5352:            "AND resolved_ref_id=? AND disposition='ADMITTED'", [exec_id, ref])]
5357:                f"(exec_id = {exec_id}, resolved_ref_id = {ref}, disposition ADMITTED). An "
5453:            "AND resolved_ref_id=?", [exec_id, ref])]
6188:            "UPDATE source_locators SET status=?, screened_reason=?, "
[exit 0]
```

```
$ grep -n -E 'INSERT.*search_admissions|INSERT INTO term_aliases|UPDATE +base_parameters' scripts/db.py | head
930:                "INSERT INTO search_admissions "
5368:            conn.execute(f"INSERT INTO search_admissions ({','.join(edge)}) "
7037:        conn.execute("UPDATE base_parameters SET " + ", ".join(sets)
7154:        conn.execute("UPDATE base_parameters SET " + ", ".join(f"{k} = ?" for k in sets)
7249:        conn.execute("UPDATE base_parameters SET " + ", ".join(f"{k} = ?" for k in sets)
7276:        conn.execute("UPDATE base_parameters SET " + ", ".join(f"{k} = ?" for k in sets)
7414:            conn.execute(f"INSERT INTO term_aliases ({','.join(arow)}) "
7529:        conn.execute(f"INSERT INTO term_aliases ({','.join(row)}) "
[exit 0]
```

```
$ grep -n 'GAP-053' references/project-standards.md | cut -c1-200 | head
4219:mechanism ratified 2026-09-27 to end it) but is filed as **GAP-053**, not fixed now: the same
4222:is disposed `PROVISIONAL-DISPUTED`, pointing at GAP-053.
4230:CONDITION: any session reading pass 1, exec 77's origin, GAP-053, or asking why pass 1 is still
4234:open. (3) GAP-053 is the one record of the audit's blind spot until phase 2b; do not re-file it.
4239:CORRECTION — 2026-09-28. **A back-pointer for GAP-053's fix, built during DR-2026-09-26 phase 2b;
4240:the GAP-053 entry above stands as written, per this ledger's append-not-edit practice.**
4249:`created_by_session` made every UPDATE this writer issues invisible to that scope — GAP-053's
4268:A "SUPERSEDED IN PART" marker naming this entry and GAP-053, carrying the BY quote verbatim, has
4275:ACTION: (1) Treat the objection as answered for GAP-053's specific (machine-reader) purpose, not
4281:DATE: 2026-09-28 — built per DR-2026-09-26 §§1 and 6 (RC4/GAP-053 and RC6), during phase 2b
[exit 0]
```

```
$ sed -n '5240,5242p;5244,5246p' scripts/db.py | head -3; grep -n 'resolved_ref_id' scripts/migrations/088*.sql | head -5
        # pair now exists, for a different reader than the one that paragraph addressed:
        # see reattribute_candidate's own SUPERSEDED note for the full reasoning (same
        # fact, same fix, sibling function). Both the note and the pair are written below,
24:    ADD COLUMN resolved_ref_id TEXT REFERENCES evidence_sources(ref_id);
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/quotes.py
NOTFOUND REQ-002 PS:1454-1455; PS:2302-2303 | base is a stage insofar as it supplies the base information 
NOTFOUND REQ-008 MEM `project-end-goal.md:15` | every pipeline stage needs rigorous, portable, transparent d
NOTFOUND REQ-010 PS:1538-1540 | research produces many rows of evidence from one slug. each 
NOTFOUND REQ-014 PS:870-872 | So long as each table has a row with a column that shares th
NOTFOUND REQ-015 PS:898-899; PS:902-903 | Reference IDs carry from table to table across stages. Data 
NOTFOUND REQ-015 PS:898-899; PS:902-903 | For rendering a citation, then, we point towards the evidenc
NOTFOUND REQ-016 MEM `contract-traceability-invariant.md:10`; ME:181 | EVERY handshake / contract / handoff / exchange / input-outp
NOTFOUND REQ-025 PS:2690-2691; EA:116 | oh. you have to compute it. I can't handle this load manuall
NOTFOUND REQ-032 PS:943-945 | Every research slug gets cross-referenced against a populati
NOTFOUND REQ-033 PS:2002; PS:2004-2007 | listing out all concepts/topics/key words/phrases that appea
NOTFOUND REQ-063 PS:4295-4297; PS:4835 | Standing order: do not research from countries other than Bu
NOTFOUND REQ-078 PS:1885-1886; RC:270 | delivers a verdict on an evidence item for what tier of evid
rows 96 fragments 149 notfound 12
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/quotes.py
rows 96 fragments 149 notfound 0
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/quotes.py | sed -n '/--- line check/,$p'
--- line check
FALLBACK REQ-001 OBJ | ensure that our pipeline can be run in all directions at any -> ('PS*', 5222)
FALLBACK REQ-008 MEM `project-end-goal.md:15` | every pipeline stage needs rigorous, portable, transparent d -> ('MEM1*', 15)
FALLBACK REQ-016 MEM `contract-traceability-invariant.md:10`; ME:181 | EVERY handshake / contract / handoff / exchange / input-outp -> ('MEM2*', 10)
LINE? REQ-031 RUL:305; PS:4433 | no idea what these are, but resolve them for me in a logical -> ('RUL', 295)
LINE? REQ-060 PS:5182; PS:5184; PS:5188 | base grounds itself -> ('PS', 5176)
line mismatches 5
[exit 0]
```

```
$ cd /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1 && python3 -I runsum2.py p9_MOB p9_BLIND p9_ALL
p9_MOB (9, 'MOB', 'pending', None) governing []
p9_MOB (9, 'MOB', 'pending', None) conditioning []
p9_MOB (9, 'MOB', 'pending', None) excluded [('ALL', 12), ('MOB', 4)]
p9_BLIND (9, 'BLIND', 'pending', None) governing []
p9_BLIND (9, 'BLIND', 'pending', None) conditioning []
p9_BLIND (9, 'BLIND', 'pending', None) excluded [('ALL', 12), ('MOB', 4)]
p9_ALL (9, 'ALL', 'pending', None) governing []
p9_ALL (9, 'ALL', 'pending', None) conditioning []
p9_ALL (9, 'ALL', 'pending', None) excluded [('ALL', 12), ('MOB', 4)]
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute('select identity_code,count(*) from source_value_extractions where parameter_id=9 group by 1').fetchall())"
[('ALL', 12), ('MOB', 4)]
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute('select parameter_id,identity_code,count(*) from source_value_extractions where parameter_id in (4,5,6,11) group by 1,2').fetchall())"; cd /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1 && python3 -I runsum2.py p4_MOB p4_DEAF p4_ALL
[(4, 'ALL', 11), (4, 'MOB', 13), (5, 'ALL', 2), (5, 'MOB', 6), (6, 'ALL', 3), (6, 'MOB', 8), (11, 'ALL', 5), (11, 'MOB', 2)]
p4_MOB (4, 'MOB', 'pending', None) governing []
p4_MOB (4, 'MOB', 'pending', None) conditioning [('ALL', 2)]
p4_MOB (4, 'MOB', 'pending', None) excluded [('ALL', 9), ('MOB', 13)]
p4_DEAF (4, 'DEAF', 'pending', None) governing []
p4_DEAF (4, 'DEAF', 'pending', None) conditioning [('ALL', 2)]
p4_DEAF (4, 'DEAF', 'pending', None) excluded [('ALL', 9), ('MOB', 13)]
p4_ALL (4, 'ALL', 'pending', None) governing []
p4_ALL (4, 'ALL', 'pending', None) conditioning [('ALL', 2)]
p4_ALL (4, 'ALL', 'pending', None) excluded [('ALL', 9), ('MOB', 13)]
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/ast_refs.py freshness_window_years FRESHNESS_WINDOWS
<unknown>:65: SyntaxWarning: invalid escape sequence '\.'
freshness_window_years [('schemas/temporal.py', 417, 'FunctionDef')]
FRESHNESS_WINDOWS [('schemas/temporal.py', 405, 'Name'), ('schemas/temporal.py', 422, 'Name')]
[exit 0]
```
$ python3 matrix.py (derived 7x7 from walkability.py --json)
[{"child": "evidence_population_match", "parent": "gaps", "col": "gap_id", "rows": 0}, {"child": "term_aliases", "parent": "observed_terms", "col": "observation_id", "rows": 0}, {"child": "gap_mining", "parent": "gaps", "col": "gap_id", "rows": 0}, {"child": "search_admissions", "parent": "evidence_sources", "col": "ref_id", "rows": 61}, {"child": "base_parameters", "parent": "evidence_sources", "col": "direction_ref_id", "rows": 0}, {"child": "search_executions", "parent": "evidence_sources", "col": "mined_ref_id", "rows": 11}, {"child": "search_candidates", "parent": "evidence_sources", "col": "resolved_ref_id", "rows": 7}, {"child": "source_value_extractions", "parent": "reasoning_doc_citations", "col": "promoted_to_rdc_id", "rows": 0}]
rows=entered, cols=reached:
               base          research      evidence      judgment      synthesis     specification render       
base           =             j             R             j             j             j             -            
research       P             =             R             z             R             z             -            
evidence       P             v             =             j             j             j             -            
judgment       P             z             P             =             R             j             -            
synthesis      P             z             P             P             =             j             -            
specification  P             z             P             P             P             =             -            
render         -             -             -             -             -             -             =            

base->research {'up': 5, 'down': 7, 'skip': None, 'direct_fk': 9, 'send_fk': 0} 1
base->evidence {'up': 3, 'down': 3, 'skip': 3, 'direct_fk': 3, 'send_fk': 2} 6
base->judgment {'up': 4, 'down': 7, 'skip': 4, 'direct_fk': 7, 'send_fk': 0} 4
base->synthesis {'up': 5, 'down': 7, 'skip': 5, 'direct_fk': 9, 'send_fk': 0} 0
base->specification {'up': 4, 'down': 7, 'skip': 4, 'direct_fk': 7, 'send_fk': 0} 4
base->render {'up': 0, 'down': 0, 'skip': 0, 'direct_fk': 0, 'send_fk': 0} 0
research->evidence {'up': 0, 'down': 0, 'skip': None, 'direct_fk': 0, 'send_fk': 3} 1
research->judgment {'up': 0, 'down': 0, 'skip': 0, 'direct_fk': 0, 'send_fk': 0} 0
research->synthesis {'up': 0, 'down': 0, 'skip': 0, 'direct_fk': 0, 'send_fk': 1} 0
research->specification {'up': 0, 'down': 0, 'skip': 0, 'direct_fk': 0, 'send_fk': 0} 0
research->render {'up': 0, 'down': 0, 'skip': 0, 'direct_fk': 0, 'send_fk': 0} 0
evidence->judgment {'up': 5, 'down': 3, 'skip': None, 'direct_fk': 5, 'send_fk': 0} 4
evidence->synthesis {'up': 5, 'down': 2, 'skip': 5, 'direct_fk': 3, 'send_fk': 0} 1
evidence->specification {'up': 4, 'down': 2, 'skip': 4, 'direct_fk': 2, 'send_fk': 0} 3
evidence->render {'up': 0, 'down': 0, 'skip': 0, 'direct_fk': 0, 'send_fk': 0} 0
judgment->synthesis {'up': 1, 'down': 1, 'skip': None, 'direct_fk': 1, 'send_fk': 2} 0
judgment->specification {'up': 1, 'down': 1, 'skip': 1, 'direct_fk': 1, 'send_fk': 0} 1
judgment->render {'up': 0, 'down': 0, 'skip': 0, 'direct_fk': 0, 'send_fk': 0} 0
synthesis->specification {'up': 3, 'down': 3, 'skip': None, 'direct_fk': 2, 'send_fk': 0} 2
synthesis->render {'up': 0, 'down': 0, 'skip': 0, 'direct_fk': 0, 'send_fk': 0} 0
specification->render {'up': 0, 'down': 0, 'skip': None, 'direct_fk': 0, 'send_fk': 0} 0

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/b3.py
REQ-072 spec DDL checks [('CREATE TABLE "specifications" (\n    -- AUTOINCREMENT (076): never reissue a specification_id. See the header.\n    specification_id                INTEGER PRIMARY KEY AUTOINCREMENT,\n    -- THE SUBJECT (owner 2026-08-26). Was item_code NOT NULL into an emptied table,\n    -- which is why no determination could be written at all.\n    parameter_id                    INTEGER NOT NULL REFERENCES base_parameters(parameter_id),\n    -- THE FOUR LENSES (owner 2026-08-28; CHECK relaxed by D-0182). population_code is\n    -- retired in favour of these. NULL in a lens means "this determination is not\n    -- stated in that lens", which is legitimate; stating several at once is the ideal.\n    identity_code                   TEXT REFERENCES "base_taxonomy_identity"(identity_code),\n    icf_code                        TEXT REFERENCES base_icf(icf_code),\n    needs_code                      TEXT REFERENCES access_needs(need_code),\n    medical_code                    TEXT REFERENCES base_taxonomy_medical(medical_code),\n    state                           TEXT NOT NULL\n                                    CHECK (state IN (\'stated\', \'provisional\',\n                                                     \'pending\', \'not_applicable\')),\n    design_scale                    TEXT\n                                    CHECK (design_scale IN (\'universal\', \'population\', \'person\')),\n    convergence_id                  INTEGER REFERENCES convergence_assessment(convergence_id),\n    confidence_dimensions_present   TEXT,   -- JSON array\n    confidence_dimensions_absent    TEXT,   -- JSON array\n    confidence_synthesis_basis      TEXT,\n    gap_register_id                 TEXT REFERENCES gaps(gap_id),\n    not_applicable_rationale        TEXT,\n    tier_basis                      TEXT,\n    governing_refs                  TEXT CHECK (governing_refs IS NULL OR json_valid(governing_refs)),\n    rule_version                    TEXT,\n    derivation_sha                  TEXT,\n    code_floor_only                 INTEGER NOT NULL DEFAULT 0\n                                    CHECK (code_floor_only IN (0, 1)),\n    value_min                       REAL,\n    value_max                       REAL,\n    value_unit                      TEXT,\n    falsification_condition         TEXT,\n    has_unverified_sources          INTEGER NOT NULL DEFAULT 0\n                                    CHECK (has_unverified_sources IN (0, 1)),\n    all_sources_disqualified        INTEGER NOT NULL DEFAULT 0\n                                    CHECK (all_sources_disqualified IN (0, 1)),\n    regulatory_stratum_only         INTEGER NOT NULL DEFAULT 0\n                                    CHECK (regulatory_stratum_only IN (0, 1)),\n    created_at                      TEXT,\n    created_by_session              TEXT,\n    updated_at                      TEXT,\n    updated_by_session              TEXT, value_note TEXT, functional_basis TEXT, derivation_rationale TEXT, cultural_claim_anchor TEXT\n    CHECK (cultural_claim_anchor IS NULL OR json_valid(cultural_claim_anchor)), derivation_paths TEXT\n    CHECK (derivation_paths IS NULL\n        OR (derivation_paths = \'dual\')\n        OR (derivation_paths = \'function_only\' AND derivation_rationale IS NOT NULL)\n        OR (derivation_paths = \'population_only\'\n            AND (derivation_rationale IS NOT NULL OR cultural_claim_anchor IS NOT NULL))), retired_at TEXT, retired_by_session TEXT, retirement_reason TEXT, superseded_by_specification_id INTEGER\n    REFERENCES specifications(specification_id), rests_on_proxy_inference INTEGER NOT NULL DEFAULT 0\n  CHECK (rests_on_proxy_inference IN (0, 1)), value_notations TEXT, marker TEXT\n  CHECK (marker IS NULL OR (marker IN (\'●\', \'◐\', \'○\')\n                            AND (regulatory_stratum_only = 0 OR marker = \'○\')))\n  CHECK (retired_at IS NOT NULL OR (state IN (\'stated\', \'provisional\')) = (marker IS NOT NULL)),\n    -- D-0182, mechanised: absence in a lens is fine, absence in ALL of them is not.\n    CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)\n)',)]
REQ-072 idx [('idx_spec_row_identity', "CREATE UNIQUE INDEX idx_spec_row_identity ON specifications(\n    parameter_id,\n    COALESCE(identity_code, ''), COALESCE(icf_code, ''),\n    COALESCE(needs_code, ''),    COALESCE(medical_code, '')\n) WHERE retired_at IS NULL"), ('idx_spec_retired', 'CREATE INDEX idx_spec_retired ON specifications(retired_at)')]
REQ-092 json cols [('weighting_profile', 'tier_weights'), ('specifications', 'value_notations'), ('search_executions', 'terms_used')]
REQ-096 bps cols []
REQ-071 en cols [('pub_title_en',), ('pub_subtitle_en',), ('chapter_title_en',), ('journal_name_en',), ('translation_method',), ('translation_reviewed',)]
REQ-010 conv [("CREATE TABLE convergence_sources (\n    convergence_id  INTEGER NOT NULL\n                    REFERENCES convergence_assessment(convergence_id),\n    ref_id          TEXT    NOT NULL\n                    REFERENCES evidence_sources(ref_id),\n    -- The weighing is a property of the pairing, so it lives here. Vocabulary in the\n    -- column's own CHECK, read by dbcore.check_values() rather than retyped by a caller.\n    role            TEXT    NOT NULL\n                    CHECK (role IN ('clinical', 'co1', 'co2',\n                                    'down_weighted', 'discounted')),\n    created_at          TEXT,\n    created_by_session  TEXT,\n    PRIMARY KEY (convergence_id, ref_id, role)\n)",)]
B13 locator cols [('term_id,alias,language,alias_type,jurisdiction,notes,created_at,created_by_session,updated_at,updated_by_session,observation_id',)]
REQ-054 icf english [('icf_code,component,is_range,title,title_source,notes,created_at,created_by_session',)]
REQ-060 term_aliases notes sample [(2382, 1526)]
REQ-070 identity cols [('identity_code,display_name,category,description,parent_code,is_compound,status,created_at,updated_at',)]
REQ-045 term rel tables [('term_aliases',), ('terms',), ('term_adjudications',), ('determination_gates',), ('observed_terms',)]
REQ-045 terms col domain [('acoustic', 5), ('bathroom', 5), ('circulation', 16), ('communication', 4), ('economics', 3)]
REQ-065 enum jur search_exec [(24,)]
REQ-067 cols [('edition,code_currency_status,code_currency_verified_at,code_currency_verified_by_session,code_currency_notes',)]
REQ-025 gap ids [('GAP-ICF-TITLES',)]
spec ids [(8,)]
REQ-040 gaps desc sample []
v_research_scope comment [('CREATE VIEW v_research_scope AS\n-- v_research_scope: the (language, jurisdiction) pairs the research scope OWES a search for.\n--\n-- The ONE home of "what is owed": every lang_jur_map row not recorded `scoped-out`. A NULL scope_status is owed --\n-- an unrecorded scope never shrinks the requirement (on 2026-11-06 marking four languages `scoped-out` left every\n-- other row NULL, and `coverage` read required 0/0, complete true). The fill of scope_status is a data migration\n-- after owner question 5; until then the requirement is the whole map, less what is recorded `scoped-out`.\n-- Readers: v_coverage_priority, `db.py coverage`.\nSELECT language, jurisdiction, role\n  FROM lang_jur_map\n WHERE COAL',)]
lang_jur_map ddl [('CREATE TABLE "lang_jur_map" (\n    language            TEXT NOT NULL,\n    jurisdiction        TEXT NOT NULL,\n    role                TEXT NOT NULL\n                        CHECK (role IN (\'PRIMARY\', \'SECONDARY\')),\n    notes               TEXT,\n    created_at          TEXT,\n    created_by_session  TEXT, scope_status TEXT\n    CHECK (scope_status IS NULL OR scope_status IN (\'in-scope\', \'scoped-out\')),\n    PRIMARY KEY (language, jurisdiction)\n)',)]
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/red/r11.db python3 scripts/audit/judgment_handoff_shape.py; echo EXIT=$?
EXAMINED: 3 invariant(s) of the evidence->judgment hand-off
  - source_value_extractions.ref_id NOT NULL
  - no UNIQUE index on source_value_extractions
  - source_value_extractions.ref_id -> evidence_sources(ref_id)

FAIL: the ruled 1:N hand-off shape has regressed.
  * UNIQUE index present on source_value_extractions: ['zz_probe']. The owner ruled one evidence source may provide MANY judgment rows (NBC 3.8). A UNIQUE on ref_id abolishes that fan-out and the DR-2026-08-19 §7 dissent contest.
EXIT=1
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/red/r19.db python3 scripts/audit/identifier_floor_audit.py; echo EXIT=$?
EXAMINED: 3 identifier floor(s) against 226 committed migration file(s)
  ref_id            historical REF-01036   live REF-01036
  base_parameters   historical 12            live 12  (sqlite_sequence)
  specifications    historical 8             live 8  (sqlite_sequence)
VERDICT: CLEAN
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/red/r19.db python3 scripts/audit/identifier_floor_audit.py; echo EXIT=$?
EXAMINED: 3 identifier floor(s) against 226 committed migration file(s)
  ref_id            historical REF-01036   live REF-01033
  base_parameters   historical 12            live 12  (sqlite_sequence)
  specifications    historical 8             live 8  (sqlite_sequence)
VERDICT: FAIL
  * ref_id floor REGRESSED: the committed migrations have already minted REF-01036, but the live high-water is REF-01033, so the next mint would be REF-01034 -- an identifier permanent records already attribute to something else. Retain the retired ids (RETIRED rows in source_locators carrying their own DOI, so a re-admission cross-files to the original under R9) rather than letting them be reissued.
EXIT=1
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/red/rchk.py
REQ-031 search with no subject REFUSED: CHECK constraint failed: COALESCE(slug, parameter_id, mined_ref_id) IS NOT NULL
REQ-072 spec with no lens REFUSED: CHECK constraint failed: COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL
REQ-082 reg-stratum stated/marker REFUSED: CHECK constraint failed: marker IS NULL OR (marker IN ('●', '◐', '○')
                            AND (regulatory_stratum_only = 0 OR marker
REQ-082b reg-stratum with marker ◐ REFUSED: CHECK constraint failed: marker IS NULL OR (marker IN ('●', '◐', '○')
                            AND (regulatory_stratum_only = 0 OR marker
REQ-072 dup live row REFUSED: UNIQUE constraint failed: index 'idx_spec_row_identity'
   TEXT CHECK (governing_refs IS NULL OR json_valid(governing_refs)),
    rule_version                    TEXT,
    derivation_sha                  TEXT,
    code_floor_only                 INTEGER NOT NULL DEFAULT 0
                                    CHECK (code_floor_only IN (0, 1)),
    value_min                       REAL,
    value_max                       REAL,
    value_unit                      TEXT,
    falsification_condition         TEXT,
    has_unverified_sources          INTEGER NOT NULL DEFAULT 0
                                    CHECK (has_unverified_sources IN (0, 1)),
    all_sources_disqualified        INTEGER NOT NULL DEFAULT 0
                                    CHECK (all_sources_disqualified IN (0, 1)),
    regulatory_stratum_only         INTEGER NOT NULL DEFAULT 0
                                    CHECK (regulatory_stratum_only IN (0, 1)),
    created_at                      TEXT,
    created_by_session              TEXT,
    updated_at                      TEXT,
    updated_by_session              TEXT, value_note TEXT, functional_basis TEXT, derivation_rationale TEXT, cultural_claim_anchor TEXT
    CHECK (cultural_claim_anchor IS NULL OR json_valid(cultural_claim_anchor)), derivation_paths TEXT
    CHECK (derivation_paths IS NULL
        OR (derivation_paths = 'dual')
        OR (derivation_paths = 'function_only' AND derivation_rationale IS NOT NULL)
        OR (derivation_paths = 'population_only'
            AND (derivation_rationale IS NOT NULL OR cultural_claim_anchor IS NOT NULL))), retired_at TEXT, retired_by_session TEXT, retirement_reason TEXT, superseded_by_specification_id INTEGER
    REFERENCES specifications(specification_id), rests_on_proxy_inference INTEGER NOT NULL DEFAULT 0
  CHECK (rests_on_proxy_inference IN (0, 1)), value_notations TEXT, marker TEXT
  CHECK (marker IS NULL OR (marker IN ('●', '◐', '○')
                            AND (regulatory_stratum_only = 0 OR marker = '○')))
  CHECK (retired_at IS NOT NULL OR (state IN ('stated', 'provisional')) = (marker IS NOT NULL)),
    -- D-0182, mechanised: absence in a lens is fine, absence in ALL of them is not.
    CHECK (COALESCE(identity_code, icf_code, needs_code, medical_code) IS NOT NULL)
)
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/red/r82.db python3 scripts/validate_evidence_state.py; echo EXIT=$?
FAIL specifications machine (r82.db):
  cell 2 (param 3×MOB): state 'stated' requires a convergence assessment (≥1 source axis, §2.2)
  cell 2 (param 3×MOB): state 'stated' but code_floor_only=1 — a Tier-6-only cell can never be 'stated' (best-practices-assessment-system.md §3)
  cell 2 (param 3×MOB): state 'stated' but the cell is regulatory-stratum-only (T4-6 basis) — never 'stated' (G1b, unification DR ACCEPTED)
  cell 2 (param 3×MOB): state 'stated' requires at least one governing source in specification_source_links (anti-hallucination gate)

FAIL: 13 records checked, 4 errors, 0 warnings
EXAMINED: 13
EXIT=1
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/red/rdb.db python3 scripts/db.py add-parameter --term-id TERM-001 --session session_2026-11-12-ag1-stress --dry-run; echo EXIT=$?
REFUSING: TERM-001 is already parameter 3 (status active). One parameter per term — a second row is the dual home rule 5 forbids.
Key the determination on parameter_id 3.
EXIT=1
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/red/rdb.db python3 scripts/db.py add-parameter --term-id TERM-NOPE --session session_2026-11-12-ag1-stress --dry-run; echo EXIT=$?
REFUSING: 'TERM-NOPE': no such term. A parameter points at a term, and the term comes from an observed phrase:
  db.py observe-term ...   then   db.py add-term --from-observation N --canonical-en '...' --rationale '...'
EXIT=1
[exit 0]
```

```
$ python3 -I -c "
import sys; sys.path.insert(0,'scripts')
import dbcore
try:
    with dbcore.connect() as c: print('OPENED (unexpected)')
except BaseException as e: print('REFUSED', type(e).__name__, str(e)[:150])
"; sha256sum data/guidebook.db
REFUSED Refusal dbcore.connect: refusing to open the CANONICAL database read-write (/home/user/guidebook/data/guidebook.db). CLAUDE.md rule 3 -- migrations only. Copy
c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d  data/guidebook.db
[exit 0]
```

```
$ sed -n '6406,6440p' scripts/db.py
# and gains nothing; every NAME field uses `_VALUE_BEARING_NAME`.
_VALUE_BEARING_NAME = re.compile(
    _VALUE_BEARING.pattern + r"|\bthan\b|\bat (least|most)\b|\bno (more|less|fewer|greater)\b"
    r"|\bnot exceeding\b|\bexceed(s|ing)?\b", re.I)


def _name_tokens(name: str) -> frozenset:
    """The content tokens of a name, lower-cased, a trailing plural 's' dropped -- the
    one normalisation `_near_terms` compares on. 'Ramp runs' -> {ramp, run}."""
    toks = re.findall(r"[a-z0-9]+", (name or "").lower())
    return frozenset(t[:-1] if len(t) > 3 and t.endswith("s") else t for t in toks)


def _near_terms(conn, name: str) -> list:
    """Terms whose canonical name or English alias shares a token set with `name` one way
    or the other (subset or superset): 'ramp runs' beside 'ramp run length', 'reverberations'
    beside 'reverberation time'. The equivalence search the skill tells an operator to do
    before minting, done by the writer and refused unless each is named --distinct-from.
    Exact matches are _name_holder's; this is the near miss nothing checked (2026-11-06)."""
    want = _name_tokens(name)
    if not want:
        return []
    out, seen = [], set()
    for term_id, held in conn.execute(
            "SELECT term_id, canonical_en FROM terms UNION ALL "
            "SELECT term_id, alias FROM term_aliases WHERE upper(language)='EN'"):
        have = _name_tokens(held)
        # Near: the new name's tokens sit inside an existing name's ('ramp runs' in 'ramp run
        # length'), or an existing name of TWO OR MORE tokens sits inside the new one. A
        # one-token term ('ramp') inside every compound that mentions it is not a near match,
        # or no compound could ever be minted (measured on the replay, 2026-11-06).
        near = have and have != want and (want <= have or (have <= want and len(have) >= 2))
        if near and term_id not in seen:
            seen.add(term_id)
            out.append((term_id, held))
[exit 0]
```

```
$ sed -n '128,131p;245,262p' scripts/assess/assess_cell.py
)

RULE_VERSION = "pilot-4"  # pilot-4 (2026-10-21, owner: "pilot 4 I guess"): the engine writes a
#   marker, and the rules for which findings count, who may confirm and what a marker needs changed
    cols = [f"e.{c}" if _has_column(conn, "evidence_sources", c) else "NULL"
            for c in dbcore.ENGINE_SOURCE_COLUMNS]
    return [dict(zip(("ref_id", *dbcore.ENGINE_SOURCE_COLUMNS), r))
            for r in conn.execute(
                f"SELECT DISTINCT e.ref_id, {', '.join(cols)} FROM source_value_extractions x "
                f"JOIN evidence_sources e ON e.ref_id = x.ref_id {join} "
                f"WHERE x.parameter_id = ? AND e.superseded_by_ref_id IS NULL AND {where} "
                f"ORDER BY e.ref_id", params)]


def gather_sources(conn, parameter_id):
    """The sources holding an EXTRACTION FOR THIS PARAMETER. Not the slug's sources.

    THE DEFECT THIS CLOSES, measured 2026-09-10. This function took a `slug` and
    joined `source_slug_links`, so the governing set was "everything admitted to this
    topic". `parameter_id` was carried through determine()'s signature, sha(), the
    report dict and validate_parameter() and never reached the evidence at all -- the
    071 re-key was cosmetic at the exact point where the engine decides. The visible
[exit 0]
```

```
$ sed -n '1775,1800p' scripts/assess/assess_cell.py


def stale_determinations(conn):
    """The live determinations this engine wrote (`RULE_VERSION`) whose stored answer is no longer
    the one `determine` gives, as (specification_id, [the fields that differ]).

    THE STORED MARKER IS A CACHE. It is read off the sources' verification and tier, the rows'
    grading and comparators, and the `confirms` edges, and `derivation_sha` hashes none of them
    (K01 verifies only the stored junction, K02 only that it is complete). `db.py` refuses the
    routes it knows (a regrading, an edge, a source's engine-read columns); a data migration, the
    verification cron or a route not yet thought of does not pass through it. This is what
    notices, whichever route moved the input. The remedy is the one the refusals name: retire the
    specification, re-determine."""
    cols = ("specification_id", "parameter_id", *LENS_ORDER, *STORED_ANSWER)
    out = []
    for sid, pid, *rest in conn.execute(
            f"SELECT {', '.join(cols)} FROM specifications WHERE retired_at IS NULL "
            f"AND rule_version = ? ORDER BY specification_id", (RULE_VERSION,)).fetchall():
        lens = dict(zip(LENS_ORDER, rest))
        det = determine(conn, pid, lens, "", "recomputed")
        diff = [f for f, was in zip(STORED_ANSWER, rest[len(LENS_ORDER):]) if det[f] != was]
        if diff:
            out.append((sid, diff))
    return out
[exit 0]
```

```
$ grep -n 'def gather_sources\|def stale_determinations\|^RULE_VERSION' scripts/assess/assess_cell.py; ls site specs 2>&1 | head -3; ls scripts/generate; ls scripts/audit | grep -i -E 'render|doc'; ls workplan | head -30
130:RULE_VERSION = "pilot-4"  # pilot-4 (2026-10-21, owner: "pilot 4 I guess"): the engine writes a
255:def gather_sources(conn, parameter_id):
1777:def stale_determinations(conn):
ls: cannot access 'site': No such file or directory
ls: cannot access 'specs': No such file or directory
context_map.py
owner_browser.html
owner_browser_build.py
research_contract_hook.py
claims_docket.py
2026-08-02-architecture-decision-and-execution-plan.md
2026-08-05-archive-fork-execution.md
2026-08-09-locator-hierarchy-and-enforcement-probes.md
2026-08-11-reconciled-findings-register.md
2026-08-11-remediation-and-pipeline-anatomy.md
2026-08-12-commit-91-adversarial-review.md
2026-08-12-pipeline-phase-state-map.md
2026-08-12-pipeline-walk-trial-log.md
2026-08-12-step-R-rename-execution-record.md
2026-08-12-work-log-audit-four-directions.md
2026-08-13-writer-plan.md
2026-08-14-execution-plan.md
2026-08-14-remediation-workplan.md
2026-08-15-adversarial-brief-pr103.md
2026-08-16-adversarial-critique-and-execution-plan.md
2026-08-17-consolidated-action-plan.md
2026-08-18-cull-execution-plan.md
2026-08-18-handoff-next-session.md
2026-08-18-model-substitution-log.md
2026-08-18-research-frame-proposal.md
2026-08-18-research-restart-plan.md
2026-08-18-structural-census-and-cull-list.md
2026-08-19-adversarial-critique-research-restart.md
2026-08-20-adversarial-adjudication-a18-aut.md
2026-08-20-provenance-walk-execution-plan.md
2026-08-21-reasoning-doc-digestion.md
2026-08-22-agonist-antagonist-execution-plan.md
2026-08-22-master-execution-plan.md
2026-08-24-pointer-discipline-queue.md
2026-09-10-audit-reconciliation-execution.md
[exit 0]
```

```
$ grep -n -i 'render apparatus was deleted' workplan/2026-10-30-ramp-spec-pages/HANDOFF.md | cut -c1-300; grep -n -i -E 'status|DRAFT|unratified' workplan/2026-10-30-ramp-spec-pages/RENDER-CONTRACT-parameters-3-and-12.md | head -8 | cut -c1-200; python3 workplan/pipeline-state-graph/walkability.py | grep -c 'NO PATH'; python3 workplan/pipeline-state-graph/walkability.py | grep -c 'NO PATH' 
18:- **The render apparatus was deleted** (`ea8b9635`, RULINGS R1, 2026-10-14): the owner's target is **dynamic rendering from the
3:**Status: DRAFT, unratified.** Written 2026-10-30 by the session `session_2026-10-30-ramp-spec-pages-rebuild`, revised after an adversarial round (a read-only Opus critic, in `transcripts/harness_fc
23:- **C3. A displayed determination has its marker.** Unmarked is an error (CLAUDE.md section 6); the marker lives on `specifications.marker`. A row read straight from `source_value_extractions` is s
26:- **C5. State is shown as stored.** `extraction_status` and the source's verification print as they are, with the flag OR-11b requires for a `preliminary` figure. OR-11a says `verified` requires a 
36:Statuses are those the probe returned on the day of writing, not asserted for a later day. **POPULATED** means the inputs exist, not that the element is correct.
38:| Id | Element (requirement) | Required data → table.column | Selection and ordering | Empty-state rule | Status today and why |
42:| E2 | Master comparison: one row per jurisdiction in scope, each cell listing every claim row | `source_value_extractions`: `jurisdiction`, `claim_type`, `figure_role`, `comparator`, `claimed_valu
44:| E3 | Detail: what the source says, where, in what state | `claim_text` (verbatim, in the source's language), `source_section`, `loc_*`, `extraction_status`, `extraction_method`, `figure_role`; `r
53:| E11 | State of each reading | `extraction_status`; `source_scans.text_scope`, `source_scans.method` | per C5 | n/a | **EMPTY for its second input.** `source_scans` holds too few full readings to 
10
10
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/retained.py; sed -n '53p' .gitignore; git check-ignore -v retrieval-log | head -3
58 48 23 10
retrieval-log/session_2026-11-06-base-vocabulary-review/*
[exit 0]
```

```
$ grep -c -i -E 'INSERT|UPDATE|DELETE|executescript' scripts/generate/owner_browser_build.py; grep -n -i -E 'answered' governance/owner-browser.yaml | head -3 | cut -c1-120; sed -n '/id: OR-1c/,/source:/p' governance/owner-browser.yaml | head -8 | cut -c1-160; sed -n '4918,4924p' references/project-standards.md | cut -c1-260
1
117:    answered: {on: '2026-10-29', ledger: "Owner rulings 2026-10-29 — "}
140:    answered: {on: '2026-10-29', ledger: "Owner rulings 2026-10-29 (second)"}
188:    answered: {on: '2026-10-29', ledger: "Owner rulings 2026-10-29 — "}
  - id: OR-1c
    gates: true
    title: How does a figure or a determination carry several codes of one model?
    question: "A figure holds one code for each model, yet a fact can concern several codes of one model, such as two ICF codes. How should figures and determin
    why_yours: "Your answer to OR-1 requires every relevant model to be filled out, and the present columns cannot hold more than one code per model. The choice
    context: |-
      Each figure read from a source has four lens columns: identity group, ICF code, access need and medical condition. Each holds one code. A determination ha

CONDITION: any session writing or reviewing a PR that touches `scripts/`, `schemas/`, `.github/` or `skills/`, or asked whether a change must reduce the line total.
ACTION: (1) Do not require or claim a net-negative total. Name what the added code reads and what wrong thing reaches the guidebook without it, and name any code it replaces or makes deletable. (2) Try, in order: do nothing and say why; change a rule or conven
DATE: 2026-11-06 — owner statements, quoted above.

## Owner rulings 2026-11-06 (second) — OR-1c, the identity lens ALL, and the type of a government report

Given in this session (https://claude.ai/code/session_01Ub36iMkXnQsEwzR9oaTqn1), in reply to the first three questions of the owner-decision sheet in `scratchpad/session_2026-11-06-pipeline-batch-2/resolution-analysis-GAP-074-096.md` (section B), and recorded 
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/b4.py
link-ish tables [('icf_medical_map',), ('identity_icf_map',), ('identity_medical_map',), ('lang_jur_map',), ('source_slug_links',), ('specification_extraction_links',), ('specification_source_links',)]
cm global_ref_id [('global_ref_id', 'TEXT', 0)]
cm fks [('slug', 'slugs')]
follow-up reason [("CREATE TABLE extraction_follow_ups (\n    follow_up_id        INTEGER PRIMARY KEY AUTOINCREMENT,\n    extraction_id       INTEGER NOT NULL REFERENCES source_value_extractions(extraction_id),\n    reason              TEXT    NOT NULL CHECK (reason IN ('read-outside-admitting-purpose')),\n    warrant             TEXT    NOT NULL CHECK (length(trim(warrant)) > 0),\n    raised_at           TEXT    NOT NULL,\n    raised_by_session   TEXT    NOT NULL,\n    resolved_at         TEXT,\n    resolved_by_session TEXT,\n    resolution          TEXT,\n    CHECK ((resolved_at IS NULL AND resolved_by_session IS NULL AND resolution IS NULL)\n        OR (resolved_at IS NOT NULL AND resolved_by_session IS NOT NULL\n            AND resolution IS NOT NULL AND length(trim(resolution)) > 0))\n)",)]
gaps fks []
spec fks [('superseded_by_specification_id', 'specifications'), ('gap_register_id', 'gaps'), ('convergence_id', 'convergence_assessment'), ('medical_code', 'base_taxonomy_medical'), ('needs_code', 'access_needs'), ('icf_code', 'base_icf'), ('identity_code', 'base_taxonomy_identity'), ('parameter_id', 'base_parameters')]
conflicts cols [('conflict_id,domain,pop_a,pop_b,status,resolution,evidence,gap_id,source_skill,created_at,created_by_session,updated_at,updated_by_session,parameter_id',)]
conflicts fks [('parameter_id', 'base_parameters'), ('gap_id', 'gaps'), ('pop_b', 'base_taxonomy_identity'), ('pop_a', 'base_taxonomy_identity')]
connection_targets cols [('target_id,con_id,parameter_id,slug,identity_code,extraction_id,methodology',)]
gap_mining cols [('gap_mining_id,gap_id,created_at,created_by_session,search_strategy_record,candidates_returned,candidates_reviewed,outcome,discoveries_logged,candidate_dois,check_method,notes',)]
search_exec cols [('exec_id,slug,parameter_id,jurisdiction,language,target_tier,target_evidence_type,target_scope,query_text,terms_used,engine,depth_method,mining_direction,results_found,results_screened,results_admitted,saturation_signal,admitted_ref_ids,deferred_reason,backfill,created_by_session,created_at,findings_note,harm_finding,prior_expectation,origin,mined_ref_id,origin_pass_id,updated_at,updated_by_session,identity_code,icf_code,needs_code,medical_code,absence_class',)]
sve KNOWN RESIDUAL [(2122,)]
sve cols with obs []
adversarial_findings subj [('finding_id,pass_id,lens,subject_table,subject_key,claim_attacked,method,artefact,verdict,severity,disposition,disposition_ref,disposed_by_session,disposed_at,created_by_session,created_at',)]
determination_gates [('gate_id,parameter_id,identity_code,verdict,trigger_ref_id,trigger_tier,trigger_evidence_type,detail,raised_at,raised_by_session,resolved_at,resolved_by_session,resolution_rationale',)]
retirement_trigger [('trg_spec_retire_needs_reason',)]
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute('select sum(pub_title_en is not null), sum(pub_subtitle_en is not null), sum(chapter_title_en is not null), sum(journal_name_en is not null), sum(translation_method is not null), sum(translation_reviewed is not null), count(*) from evidence_sources').fetchall())
print(c.execute('select ref_id, lang_detected, pub_title, pub_title_en from evidence_sources where pub_title_en is not null limit 3').fetchall())
print(c.execute('select count(*) from v_evidence_authors').fetchall())
"; grep -rn 'pub_title_en' scripts/db.py | head -3 | cut -c1-140
[(0, 0, 0, 0, 0, 59, 59)]
[]
[(59,)]
4169:    pub_title_en, so the verifier compares a SET of columns where this writer targets one).
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute('select translation_reviewed, count(*) from evidence_sources group by 1').fetchall())
print([r for r in c.execute('pragma table_info(evidence_sources)') if r[1] in ('translation_reviewed','translation_method')])
"
[(0, 59)]
[(20, 'translation_method', 'TEXT', 0, None, 0), (21, 'translation_reviewed', 'INTEGER', 0, '0', 0)]
[exit 0]
```
gap_mining rows=0 migrations_inserting=0
reasoning_doc_citations rows=0 migrations_inserting=0
access_duration rows=3 migrations_inserting=1
access_stakes rows=3 migrations_inserting=1
life_stage_modifiers rows=2 migrations_inserting=1
rooms rows=17 migrations_inserting=1
weighting_profile rows=5 migrations_inserting=1
research_code_leads rows=96 migrations_inserting=8
connections rows=0 migrations_inserting=1
conflicts rows=0 migrations_inserting=0
case_studies rows=0 migrations_inserting=0
economics_entries rows=1 migrations_inserting=1
supersession_check rows=0 migrations_inserting=0

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/ast_refs.py gap_mining 2>/dev/null | head -3; grep -c 'add_parser(' scripts/db.py
gap_mining None
72
[exit 0]
```

```
$ grep -n -E '\bAMB\b|\bWHEEL\b' references/project-standards.md | awk -F: '$1>1299' | cut -c1-110
1411:  non-`[\w-]` character after the token, so `AX-` never matches `AX-AMB`. There is no prefix mode.
2926:power); b730 is declared by AX-AMB, AX-REA and AX-WHM; those axes carry nine identities including
3446:**TWO THINGS REMAIN UNDECIDED AND ARE NOT GUESSED HERE.** (1) The replacement code shape — `DM-AMB`
3460:character after the token, so `AX-` never matches `AX-AMB`; that is a matcher fact recorded on
[exit 0]
```

```
$ git diff --stat 186defb 4afe1dd -- . ':(exclude)scratchpad' ':(exclude)transcripts' | tail -3; git log --oneline 186defb..HEAD
4afe1dd governance: handshake matrix, adversarial findings, improvement programme, Sonnet brief [2026-11-12 02:53]
[exit 0]
```

```
$ python3 -c "b=set('UN ISO CA US UK DE NO SE JP AU EU SG NZ IE FR ES PT FI NL KR'.split());p=set('US UK AU CA DE NO SE ISO EU FR CH NL DK FI BE IE ES IT PT JP SG NZ KR CN'.split());print(sorted(b-p),sorted(p-b))"
['UN'] ['BE', 'CH', 'CN', 'DK', 'IT']
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 120 python3 scripts/audit/adherence_log_audit.py 2>&1 | tail -8; echo EXIT=${PIPESTATUS[0]}
============================================================
adherence_log_audit -- check_filter=all
changed files: 460; attestations: 2; synthesis: 3
============================================================
No issues.
============================================================
EXIT=0
[exit 0]
```

```
$ timeout 120 python3 scripts/audit/research_tooling_separation.py 2>&1 | tail -10; echo EXIT=${PIPESTATUS[0]}
  scripts/migrations/124_ledger_blocked_precedence.sql
  scripts/migrations/125_alias_observation_pointer.sql
  scripts/research/retrieval_log.py
  scripts/tests/test_db_amend_writers.py
  scripts/tests/test_evidence_cell_state_2_3.py
  scripts/tests/test_run_pipeline_refusals.py
  scripts/tests/test_scan_contract.py
  scripts/validate_parameters.py
EXAMINED: 460
VERDICT: FAIL — this changeset carries both research data and tooling. RC6 (DR-2026-09-26-recurring-defect-shapes-remediation.md section 6): they ship apart, so a writer gap found mid-batch cannot be patched with hand SQL disguised as a schema fix.
EXIT=1
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 120 python3 scripts/audit/supersession_backpointer_audit.py 2>&1 | tail -6; echo EXIT=${PIPESTATUS[0]}
SUPERSEDES lines found (ledger + decisions/*.md): 11
EXAMINED: 11
VERDICT: PASS
EXIT=0
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/b5.py
ext_root_registry [(0,)]
v_value_independence [(1,)]
saturation [(None, 76), ('none', 60), ('partial', 40), ('saturated', 27)]
admitted_ref_ids sample [('[]',), ('[]',), ('[]',)]
downstream tables 18 bibliographic-like columns [('supersession_check', 'superseding_dois')]
[exit 0]
```

```
$ grep -n -o -E 'add_parser\(\s*.(delete-connection|unlink-admission|add-alias|resolve-candidate|update-locator|add-gap-mining|record-scan)' scripts/db.py
1594:add_parser("resolve-candidate
1628:add_parser("unlink-admission
1723:add_parser("update-locator
1933:add_parser("add-alias
2750:add_parser("delete-connection
2798:add_parser("add-gap-mining
[exit 0]
```

```
$ sed -n '14,18p' skills/run-pipeline_SKILL.md | cut -c1-400
session record `sessions/<STEM>.md` (with `attestations/sessions_<STEM>.json`, validated against
`schemas/attestation.schema.json`, CLAUDE.md rule 2), and commit both at the next natural break (rule 6). The
database holds no marker for a return; the record and `scratchpad/<STEM>/commands.jsonl` are the trace. `session-consolidator` is a prior-version procedure and is not
run. Derive every figure; paste no counts.
[exit 0]
```

```
$ grep -n -i -E 'INSERT|UPDATE|DELETE|executescript' scripts/generate/owner_browser_build.py | cut -c1-200
36:sys.path.insert(0, os.path.join(REPO, "scripts"))
[exit 0]
```

```
$ grep -n 'OW-1b\|OW-1c' governance/owner-browser.yaml | head -4; sed -n '4694,4697p' references/project-standards.md | cut -c1-420; sed -n '5026,5030p' references/project-standards.md | cut -c1-300
913:  - id: OW-1b
940:  - id: OW-1c
8. **OR-11a.** The prompt's recommended option: an extraction marked `verified` requires a recorded full-scope `source_scans` reading that covers the row's parameter. T-1 step 10 is built, and the renderer prints the status of each row. No ratified text changes.
9. **OR-11b.** The prompt's recommended option: a figure read in full but still `preliminary` may set a published value, flagged. No engine change, and the renderer (T-5) shows the flag. [ASSUMPTION: "for follow up" asks that the flag say the figure still awaits review; it does not by itself raise a follow-up record for each figure.]
10. **OR-12a.** The prompt's recommended option: Arabic, Bengali, Hindi and Swahili, which `lang_jur_map` requires and for which the project has no aliases, are scoped out by the bucket table until buckets 1 and 2 are exhausted, so building their aliases is not research debt now. [ASSUMPTION: with OR-8's bucket member as a jurisdiction-and-language pair, their pairs are not bucket members until then.]
11. **OR-12b.** The prompt's recommended option: a model-generated alias may be used for a search if the search is flagged. The owner adds an expectation, and it is an instruction to the model: generate only terms actually in use in the jurisdiction, not word-for-word translations of English terms. That is research rule R11 (no back-translation; every alias carries its in-language source or is marked unverified) appl
4. **The language scope is P1+P2+P3.** The base tables, aliases, native terms and translations must work across every language those jurisdictions require. [ASSUMPTION: the set is the one recorded in `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md` section 3 (US UK AU CA DE NO SE ISO EU; FR CH NL DK
5. **Opus plans.** An Opus-class planner writes a strategy to populate the base tables and to address the review's listed issues (the parameter list at ten rows, the unverified and English-biased alias layer, the English-only ICF, identity, need and room tables, the empty medical lens, the missing t

CONDITION: any session asking whether the 93 old item names may seed parameters, whether item subjects are still excluded as a source, whether the base vocabulary must cover the P1+P2+P3 languages, or who plans the population of the base tables.
ACTION: (1) Treat the pre-reset item subjects, value-stripped and with their codes removed, as a permitted source of candidate names, never as containers. (2) Mint no name from them before a tooling pull request adds the catalogue route and the owner approves the screened table in a dated entry. (3)
[exit 0]
```

```
$ grep -c -i -E 'equivalen|adjacen|similarit|commonalit' skills/connection-discovery_SKILL.md skills/cross-population-conflict-mapper_SKILL.md; grep -n 'cross-population-conflict-mapper' scratchpad/session_2026-11-12-pipeline-bidirectional-audit/commands.jsonl | head -0; GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db python3 scripts/audit/skill_vocabulary_audit.py | grep -E 'cross-population|connection-discovery' | cut -c1-250
skills/connection-discovery_SKILL.md:0
skills/cross-population-conflict-mapper_SKILL.md:1
  skills/cross-population-conflict-mapper_SKILL.md: DBL, MCAS, NEU, OFS, POTS, SENS, VIS
[exit 0]
```

```
$ grep -n 'cultural_claim_anchor' scripts/assess/assess_cell.py scripts/db.py | head -3 | cut -c1-120
scripts/assess/assess_cell.py:1622:    functional_basis, derivation_paths, derivation_rationale, cultural_claim_anchor, 
scripts/assess/assess_cell.py:1752:        "cultural_claim_anchor": cultural_claim_anchor,
scripts/assess/assess_cell.py:2321:                det["derivation_rationale"], det["cultural_claim_anchor"],
[exit 0]
```

```
$ grep -rn -i 'saturation' --include=*.py scripts | grep -v 'scripts/tests' | cut -c1-150 | head -12
scripts/db.py:677:               results_admitted: int = 0, saturation_signal: str = None,
scripts/db.py:829:        "saturation_signal": saturation_signal,
scripts/db.py:2510:    p_ls.add_argument("--saturation-signal", choices=dbcore.schema_choices("search_executions", "saturation_signal"))
scripts/db.py:2977:            saturation_signal=args.saturation_signal,
[exit 0]
```

```
$ sed -n '2740,2742p' scripts/db.py | cut -c1-200; python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute('select sum(saturation_signal is not null), count(*) from search_executions').fetchall())"

    # conflicts
    p_confs = sub.add_parser("conflicts", help="Query conflict records")
[(127, 203)]
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 250 python3 scripts/audit/migration_reproducibility_deep.py 2>&1 | tail -6; echo EXIT=${PIPESTATUS[0]}
python3: can't open file '/home/user/guidebook/scripts/audit/migration_reproducibility_deep.py': [Errno 2] No such file or directory
EXIT=2
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 280 python3 scripts/audit/migration_reproducibility.py --deep 2>&1 | tail -8; echo EXIT=${PIPESTATUS[0]}

  --- deep comparison: every table, every row ---
  (56 tables identical, not listed)
  EXAMINED: 56

======================================================================
  PASS: the committed DB matches what the migration history produces.
VERDICT: PASS
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/runs/live.db timeout 280 python3 scripts/tests/test_db_integrity.py 2>&1 | tail -8; echo EXIT=${PIPESTATUS[0]}

======================================================================
RESULTS: 56/56 checks passed

PASSED HAVING EXAMINED NOTHING (10): B04, I3, I3b, B09, C10, C05, D02, G03, K01, K02
  Their scope is empty. They are not evidence that the thing they check is true.
EXAMINED: 3659 subject-inspections across 46 instrumented check(s) of 56
======================================================================
EXIT=0
[exit 0]
```

```
$ python3 -I /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/b1.py 2>&1 | grep -E 'REQ-097|REQ-099'
REQ-097 locator_scheme [(None, 44), ('page', 17), ('section', 153)]
REQ-097 sve cols loc [(15,)]
REQ-097 ex relations [('audited_against', 8), ('condition_on', 31), ('confirms', 3), ('exceeds', 1), ('insufficient', 4), ('tested_at', 10)]
REQ-099 base_parameters [('parameter_id,term_id,status,merged_into,notes,created_at,created_by_session,updated_at,updated_by_session,direction_rationale,accessibility_direction,direction_ref_id',)]
REQ-099 claimed_unit [(32, 41, 122)]
[exit 0]
```

## Commands run before the logging wrapper existed (re-stated; outputs as observed)
```
$ git rev-parse --short HEAD  ->  4afe1dd   (brief and HS leg name 186defb; git diff --stat 186defb 4afe1dd outside scratchpad and transcripts is empty)
$ sha256sum data/guidebook.db  ->  c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d (start)
$ verdict distribution over hs-handshake-matrix.md (118 requirement rows; 8 CONTRADICTED, 9 MET, 61 PARTIAL, 33 UNMET, 7 UNPROVEN); boundaries: 1 MET, 9 PARTIAL, 7 UNMET
$ grep -c "^| REQ-" td-requirements-and-interface-spec.md -> 96
$ python3 quotes.py (warrant resolver): 96 rows, 149 fragments, 0 not found; 5 flagged for line/file, all explained (see doc X23)
$ python3 check_doc_quotes.py (this document): 143 fragments checked; unresolved are MEM-prefixed refs (verified separately) and first-occurrence heading artefacts
$ python3 -I runsum.py / runsum2.py (engine run summaries) -> see X17 in the document
$ python3 -I matrix.py (derived 7x7) -> output copied into section 5
$ red tests (judgment_handoff_shape UNIQUE index; identifier_floor_audit; CHECK refusals; validate_evidence_state) -> see X21
$ dbcore.connect() refusal; add-parameter refusals -> X24, X31
$ migration_reproducibility (+ --deep), test_db_integrity, schema_reference_audit, claude_md_spine, adherence_log_audit, research_tooling_separation -> X20, X27
$ document checks: X02b/X02c verdict-diff (only HS-A13 differs), column-count check of every table (0 bad)
```

## End of work
```
$ sha256sum data/guidebook.db
c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d  data/guidebook.db
$ git status --short
 M scratchpad/session_2026-11-12-pipeline-bidirectional-audit/commands.jsonl
?? scratchpad/session_2026-11-12-pipeline-bidirectional-audit/suite-work/
?? workplan/2026-11-12-bidirectional-pipeline/
```


# ROUND 2: resolution of antagonist objections (re-runs of the antagonist's evidence)

c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d  data/guidebook.db

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/r2/upd.db python3 scripts/audit/migration_reproducibility.py 2>&1 | tail -3; echo EXIT=${PIPESTATUS[0]}
======================================================================
  PASS: the committed DB matches what the migration history produces.
VERDICT: PASS
EXIT=0
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/r2/upd.db python3 scripts/audit/migration_reproducibility.py --deep 2>&1 | tail -5; echo EXIT=${PIPESTATUS[0]}
  seven core invariants cannot see, because an UPDATE changes no COUNT:
    evidence_sources
  Those writes owe a data migration; this check reports the divergence
  rather than choosing.
VERDICT: FAIL (deep)
EXIT=1
[exit 0]
```

```
$ grep -n -B2 -A6 'id: migration_reproducibility' governance/check-registry.yaml | grep -E 'id:|level' 
246:- id: migration_reproducibility
258:- id: migration_reproducibility_deep
[exit 0]
```

```
$ grep -n -i 'COUNTS only\|row COUNTS' CLAUDE.md | cut -c1-160
88:→ Enforced by `migration_reproducibility` (blocking), **which compares row COUNTS only** — an UPDATE
117:generation date and a drift warning. Derive every volatile fact — row counts, schema version, CI
[exit 0]
```

```
$ grep -n -E "'conditioning'|\"conditioning\"" scripts/assess/assess_cell.py | head -20 | cut -c1-170
468:            role, why = "conditioning", None
1096:        "population_directness": pop, "value_directness": val, "conditioning": cond,
1139:    return [r for r in recs if r["conditioning"] not in (COND_NON_ANCHORING, COND_DISCOUNTED)]
1338:    down_weighted = [r["ref_id"] for r in recs if r["conditioning"] == COND_DOWN_WEIGHTED]
1340:                  if r["conditioning"] in (COND_DISCOUNTED, COND_NON_ANCHORING)]
2398:                                              "population_directness", "conditioning",
[exit 0]
```

```
$ sed -n '340,352p;422,430p;462,470p' scripts/assess/assess_cell.py | cut -c1-170

#: Which figure_role values supply a value to a determination. ONE HOME (migration 077).
#: `gather_sources` filters on it, `gather_extraction_links` grades on it, and K01
#: recomputes the sha from the links this produces -- so the three cannot disagree.
#: Before 077 the predicate lived only inside gather_sources' SQL while the sha hashed an
#: UNFILTERED count, which is how re-grading a row could flip a cell from `stated` to
#: `pending` without moving its attestation.
VALUE_SUPPLYING_ROLES = ("claim", "derived")
CONDITIONING_ROLES = ("condition",)
#: Rows that report something ABOUT the parameter without asserting a value for it.
#: They supply DIRECTION, never value (owner ruling 2026-09-13), and since the owner
#: statement of 2026-09-16 they may also carry a determination as a PROXY -- see
#: `gather_findings` and the proxy branch in `determine()`.
    Returns one dict per extraction, with `role` in:

      governing     figure_role supplies a value AND the row's source survived the tier,
                    verification and supersession gates -- i.e. its ref_id is in the
                    governing set this determination actually used.
      conditioning  figure_role='condition'. Qualifies a governing row. Carried onto the
                    determination so a slope arrives with its run length attached.
      excluded      everything else, with a MANDATORY reason. This is the row that makes
                    a `pending` cell legible: "examined, and here is why it did not
                f"extraction_method={method!r}: a skimmed figure is not publishable "
                f"(owner ruling 2026-10-09, 'skimmed values are not publishable'); it is "
                f"recorded and shown, never set as the value")
        elif frole in VALUE_SUPPLYING_ROLES and ref in gov:
            role, why = "governing", None
        elif frole in CONDITIONING_ROLES:
            role, why = "conditioning", None
        elif frole in VALUE_SUPPLYING_ROLES:
            # Value-supplying, but its source did not survive the anchoring gates.
[exit 0]
```

```
$ cd /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1 && python3 -I runsum2.py p4_MOB p4_DEAF p4_ALL
p4_MOB (4, 'MOB', 'pending', None) governing []
p4_MOB (4, 'MOB', 'pending', None) conditioning [('ALL', 2)]
p4_MOB (4, 'MOB', 'pending', None) excluded [('ALL', 9), ('MOB', 13)]
p4_DEAF (4, 'DEAF', 'pending', None) governing []
p4_DEAF (4, 'DEAF', 'pending', None) conditioning [('ALL', 2)]
p4_DEAF (4, 'DEAF', 'pending', None) excluded [('ALL', 9), ('MOB', 13)]
p4_ALL (4, 'ALL', 'pending', None) governing []
p4_ALL (4, 'ALL', 'pending', None) conditioning [('ALL', 2)]
p4_ALL (4, 'ALL', 'pending', None) excluded [('ALL', 9), ('MOB', 13)]
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute('select x.identity_code, x.figure_role, count(*) from source_value_extractions x where parameter_id=4 and identity_code=\'ALL\' group by 1,2').fetchall())
print(c.execute('select p.parameter_id,t.canonical_en from base_parameters p join terms t using(term_id) where p.parameter_id in (4,9)').fetchall())"
[('ALL', 'claim', 9), ('ALL', 'condition', 2)]
[(4, 'corridor width'), (9, 'door width')]
[exit 0]
```

```
$ cd /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1 && python3 -I runsum2.py p5_DEAF p6_DEAF p8_DEAF p11_DEAF
p5_DEAF (5, 'DEAF', 'pending', None) governing []
p5_DEAF (5, 'DEAF', 'pending', None) conditioning []
p5_DEAF (5, 'DEAF', 'pending', None) excluded [('ALL', 2), ('MOB', 6)]
p6_DEAF (6, 'DEAF', 'pending', None) governing []
p6_DEAF (6, 'DEAF', 'pending', None) conditioning []
p6_DEAF (6, 'DEAF', 'pending', None) excluded [('ALL', 3), ('MOB', 8)]
p8_DEAF (8, 'DEAF', 'pending', None) governing []
p8_DEAF (8, 'DEAF', 'pending', None) conditioning []
p8_DEAF (8, 'DEAF', 'pending', None) excluded [('ALL', 1), ('BLIND', 3), ('MOB', 1)]
p11_DEAF (11, 'DEAF', 'pending', None) governing []
p11_DEAF (11, 'DEAF', 'pending', None) conditioning []
p11_DEAF (11, 'DEAF', 'pending', None) excluded [('ALL', 5), ('MOB', 2)]
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute('select parameter_id,identity_code,figure_role,count(*) from source_value_extractions where parameter_id in (5,6,8,11) group by 1,2,3').fetchall())"
[(5, 'ALL', 'claim', 2), (5, 'MOB', 'claim', 4), (5, 'MOB', 'finding', 2), (6, 'ALL', 'claim', 2), (6, 'ALL', 'finding', 1), (6, 'MOB', 'claim', 8), (8, 'ALL', 'finding', 1), (8, 'BLIND', 'claim', 3), (8, 'MOB', 'finding', 1), (11, 'ALL', 'claim', 5), (11, 'MOB', 'claim', 2)]
[exit 0]
```

```
$ cd /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1 && sed -i 's#file:r2/{name}.db#file:r2/{name}.db#' runsum2.py && python3 -I runsum2.py p3_allfig_DEAF
p3_allfig_DEAF (3, 'DEAF', 'provisional', '○') governing [('ALL', 35)]
p3_allfig_DEAF (3, 'DEAF', 'provisional', '○') conditioning [('ALL', 21), ('SCI', 1)]
p3_allfig_DEAF (3, 'DEAF', 'provisional', '○') excluded [(None, 1), ('ALL', 60), ('MS', 2), ('SCI', 2)]
[exit 0]
```

```
$ sed -n '255,300p' scripts/assess/assess_cell.py | cut -c1-150
def gather_sources(conn, parameter_id):
    """The sources holding an EXTRACTION FOR THIS PARAMETER. Not the slug's sources.

    THE DEFECT THIS CLOSES, measured 2026-09-10. This function took a `slug` and
    joined `source_slug_links`, so the governing set was "everything admitted to this
    topic". `parameter_id` was carried through determine()'s signature, sha(), the
    report dict and validate_parameter() and never reached the evidence at all -- the
    071 re-key was cosmetic at the exact point where the engine decides. The visible
    result was `param 1 x MOB -> stated basis=T1+CO1+T2` anchored on all 10 sources
    linked to `accessible-circulation-geometry`, 8 of which the engine's own report
    flagged `tier_inconsistent`, and every one of the 10 DOWN-WEIGHTED.

    The cause was one absent table-writer, not a bad query: `db.py` held ZERO
    references to `source_value_extractions`, so no parameter->evidence edge existed
    and the slug was the only join available. `db.py add-extraction` (migration 073,
    same change as this) creates the edge; this query uses it.

    DISTINCT IS LOAD-BEARING, not tidiness. Evidence to judgment is 1:N (D-0168): one
    code document yields many clause-level extractions for one parameter. Without
    DISTINCT, NBC 3.8's clauses would each add a copy of the same source to the
    governing set, and a single document would look like corroboration of itself --
    the independence failure `v_value_independence` exists to detect, manufactured
    inside the engine.

    A CONSEQUENCE WORTH STATING, because it is stop condition 6 of the operative
    plan ("any `stated` cell whose governing set includes a source with no extraction
    for that parameter -- do not merge the migration"): after this change that cell is
    not merely forbidden, it is unconstructible. Every ref_id in the governing set
    came out of this query, and this query returns only sources that hold an
    extraction for the parameter being determined.

    ONLY VALUE-SUPPLYING ROWS GOVERN (added 2026-09-13, migration 075's whole point).
    Holding an extraction for the parameter was never enough. Measured on the live
    corpus the day the grading landed: specification 1 was `stated` at T1 -- the
    strongest claim this project makes -- on four rows of which TWO WERE CONDITIONS
    (the slopes a treadmill was set to; the ADA range a study tested) and two were
    findings, one of them `claim_type='absent'`, asserting nothing whatever. Not one
    governing row was a claim. Specification 2 was the same shape.

    So the predicate is `figure_role IN ('claim','derived')`:

      claim     -- the row states a value for the parameter. Governs.
      derived   -- the row's value was computed from other rows. Governs; its band
                   is the floored mean of its inputs' (owner ruling 2026-09-13).
      finding   -- the row reports something ABOUT the parameter without asserting a
                   value: "code-compliant width fails 10-100% of users". Supplies
[exit 0]
```

```
$ sed -n '1240,1256p' scripts/db.py | cut -c1-160; sed -n '5395,5445p' scripts/db.py | cut -c1-160
    with connect(readonly=True) as conn:
        rows = [dict(r) for r in conn.execute(q, params).fetchall()]
    if summary:
        from collections import Counter
        return dict(Counter(r["status"] for r in rows))
    return rows


def delete_connection(con_id: str, session: str, dry_run: bool = False):
    """Hard-delete a connection and its targets. Use sparingly — for data corrections only."""
    with connect(dry_run) as conn:
        conn.execute("DELETE FROM connection_targets WHERE con_id=?", [con_id])
        conn.execute("DELETE FROM connections WHERE con_id=?", [con_id])


# --- CLI ---



def unlink_admission(exec_id: int, ref_id: str, reason: str, session: str,
                     dry_run: bool = False):
    """Remove an admission edge that is wrong. The corrective half of link-admission.

    ADDED 2026-09-26. db.py had no DELETE or UPDATE on search_admissions at all, so a
    wrong edge -- however it got there: a mis-typed --admitted-ref-id, or a
    link-admission that faithfully copied a candidate's wrong exec_id -- could not be
    corrected through any sanctioned path. Shaped like reattribute_candidate: the move
    needs a reason, and the removed edge is kept in the search's findings_note, because
    the junction row itself is gone.

    results_admitted drops by the edge removed, never below the edges that remain (the
    rule _results_admitted_after states). It does not touch the candidate
    row: if the candidate's own exec_id is what was wrong, correct it with
    reattribute-candidate as well -- the result names any candidate that still points
    at this search, so the second half is not forgotten.

    CAPTURING IT. This is a DELETE, and the capture path is additive by default: run
    emit_batch_sql.py with --allow-delete search_admissions, which renders the removed
    row as a keyed DELETE (only for a table a writer here deletes from). Found the first
    time the verb was used for real (GAP-050's repair, 2026-09-26): emit refused the
    scratch, correctly, until that opt-in existed.
    """
    reason = dbcore.require_reason(
        reason, f"exec {exec_id} -> {ref_id}",
        "Removing a provenance edge without saying why erases an attribution without "
        "a trace of what replaced it.")
    with connect(dry_run) as conn:
        ref = dbcore.fold_ref(ref_id)
        ex = conn.execute("SELECT exec_id, findings_note, results_admitted "
                          "FROM search_executions WHERE exec_id=?", [exec_id]).fetchone()
        if ex is None:
            raise Refusal(f"exec {exec_id}: no such search execution.")
        if not conn.execute("SELECT 1 FROM search_admissions WHERE exec_id=? AND ref_id=?",
                            [exec_id, ref]).fetchone():
            raise Refusal(f"exec {exec_id} -> {ref}: no such admission edge to remove.")
        conn.execute("DELETE FROM search_admissions WHERE exec_id=? AND ref_id=?",
                     [exec_id, ref])
        edges = conn.execute("SELECT COUNT(*) FROM search_admissions WHERE exec_id=?",
                             [exec_id]).fetchone()[0]
        was = ex["results_admitted"] or 0
        count = _results_admitted_after(was, edges, linked=False)
        detail = f"{ref}: {reason}"
        if count != was:
            detail += f" results_admitted {was} -> {count}."
        # One stamp for both the note's date and updated_at (GAP-053, migration 100),
        # so they cannot disagree -- link_admission's own pattern.
        stamp = dbcore.now()
        conn.execute("UPDATE search_executions SET results_admitted=?, findings_note=?, "
[exit 0]
```

```
$ sed -n '3540,3562p;3576,3584p' references/project-standards.md | cut -c1-300
> **"retire in place then"**

Given in answer to the proposal `scripts/migrations/076_never_reuse_identifiers.sql` named and
declined to smuggle in: *"The single rule that would make both unnecessary is `retire in place,
never hard-delete`, for which the mechanism is already half-built (`evidence_sources.superseded_by_ref_id`,
`base_parameters.status = 'retired'`, `source_locators.status = 'RETIRED'`) … That is a doctrine
change and an owner decision, so it is named here and not smuggled in."* It is now made. Recorded on
contact per `CLAUDE.md` rule 0; the paperwork below is what the ruling CHANGES, never an argument
against it.

**WHAT IT SUPERSEDES.** 076's framing of the two floors as permanent; any future data migration that
hard-deletes rows to retract them; and `assess_cell`'s re-determination refusal keying on NOT EXISTS,
which the same comment says "could key on NOT RETIRED" under this rule — that is now the design, not
a hypothetical.

**WHAT IT DOES NOT TOUCH, stated because the boundary is easy to over-read.** `CLAUDE.md` §8's
"Code, checks, scripts, dead tables and views: delete them" stands unchanged. This ruling governs
DATA ROWS AND IDENTIFIERS, where deleting destroys provenance the project cannot reconstruct. Git
history genuinely is the archive for code, so a deleted script loses nothing; a deleted row loses
the fact that it existed. The two are different objects and §8's removal-friendly posture on
apparatus is not weakened.

**WHY IT WAS RULED, in the owner's own framing:** *"This is a recurring provenance and data
that could surface it filters on status**, and that sweep is rule 4's ("a VIEW IS a caller") applied
to this ruling.

CONDITION: Any session about to delete a data row, retract a source, clear a corpus, or design a
supersede path; and any migration that would empty a table.
ACTION: (1) Retire in place — set the status the table already carries — never hard-delete. (2)
Before the first retirement, sweep every reader that could surface a retired row and make it filter;
a view that does not is the defect. (3) Re-key `assess_cell`'s re-determination refusal on NOT
RETIRED rather than NOT EXISTS. (4) Where a row MUST genuinely leave (owner-ordered destruction,
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
no=[];yes=[]
for (n,s) in c.execute(\"select name,sql from sqlite_master where type='table' and name<>'sqlite_sequence'\").fetchall():
    cols=[r for r in c.execute(f'pragma table_info(\"{n}\")') if r[5]==1]
    if len(cols)==1 and cols[0][2].upper()=='INTEGER':
        (yes if 'AUTOINCREMENT' in s.upper() else no).append(n)
print('AUTOINC',len(yes),yes);print('ROWID-REUSE',len(no),no)"
AUTOINC 10 ['gap_mining', 'evidence_source_authors', 'extraction_relations', 'base_parameters', 'determination_gates', 'specifications', 'identity_icf_map', 'source_scans', 'extraction_follow_ups', 'source_value_extractions']
ROWID-REUSE 14 ['convergence_assessment', 'specification_source_links', 'search_admissions', 'research_code_leads', 'term_adjudications', 'specification_extraction_links', 'convergence_sources', 'adversarial_passes', 'search_execution_artefacts', 'observed_terms', 'search_executions', 'search_candidates', 'adversarial_findings', 'connection_targets']
[exit 0]
```

```
$ grep -n -i 'rowid' scripts/audit/identifier_floor_audit.py | head -5 | cut -c1-160
10:(`dbcore.ref_id_high_water`), and `parameter_id` / `specification_id` are rowid aliases that
100:        # No AUTOINCREMENT: SQLite will reissue MAX(rowid)+1, so the live floor is
105:        seqs[table] = ("max(rowid) — NO AUTOINCREMENT", mx)
146:                "%s has no AUTOINCREMENT, so SQLite reissues MAX(rowid)+1 and emptying the "
[exit 0]
```

```
$ GUIDEBOOK_DB_PATH=/tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/r2/addp.db python3 scripts/db.py add-parameter --term-id TERM-004 --session session_2026-11-12-ag1-r2 2>&1 | tail -12
{
  "parameter_id": 13,
  "term_id": "TERM-004",
  "canonical_en": "lever handle",
  "status": "active",
  "provenance": "base-vocabulary",
  "adjudicated_by": null,
  "outcome": null,
  "dry_run": false
}
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute(\"select count(*) from term_adjudications where term_id='TERM-004'\").fetchall(), c.execute(\"select count(*) from observed_terms where observation_id in (select observation_id from term_adjudications where term_id='TERM-004')\").fetchall())
print(c.execute('select count(*) from observed_terms o where not exists (select 1 from term_adjudications a where a.observation_id=o.observation_id)').fetchall())
print(c.execute('select p.parameter_id,p.term_id,(select count(*) from term_adjudications a where a.term_id=p.term_id) from base_parameters p').fetchall())
"
[(0,)] [(0,)]
[(8,)]
[(3, 'TERM-001', 18), (4, 'TERM-002', 0), (5, 'TERM-003', 1), (6, 'TERM-005', 0), (7, 'TERM-007', 0), (8, 'TERM-011', 0), (9, 'TERM-021', 0), (10, 'TERM-024', 0), (11, 'TERM-061', 0), (12, 'TERM-091', 2)]
[exit 0]
```

```
$ sed -n '5186,5194p' references/project-standards.md | cut -c1-420
> "the only thing that we need to do is ensure that our matrix works properly so that we have proper coverage across all these languages and jurisdictions"

> "so long as we can confirm that we have correct coverage, we are fine"

**What this decides.**
1. **The base is the matrix and is self-grounding.** A base cell (a concept, a language, a jurisdiction, a form) carries where it was found, in the base's own columns: the source's URL and, if need be, page and line (this extends the fifth entry of the same day: "just record page number and line if need be"). It does not point into the evidence stage, and nothing in the base waits on a source being admitted, a quote 
2. **This supersedes, for base vocabulary only,** the route the 2026-10-09 ledger entry and migration 125 set up: an attested alias reached through `observed_terms` and `evidence_sources` (`db.py add-alias` requires an adjudicated observation whose quote verifies in a file saved for its source). That route stays for evidence-stage reading of a source for a parameter (the scan contract); it is no longer the way a base
3. **The acceptance test is confirmed coverage.** The matrix is accepted when coverage across every language and jurisdiction can be confirmed as correct, which means a coverage measure derived from the base itself (concept by language-and-jurisdiction column), not a list kept beside it. [ASSUMPTION: "correct coverage" is read as a derivable measure that distinguishes a cell that has a form, a cell searched with none
4. **Consequences left open for the owner's schema decision:** whether the base cell's source columns go on `term_aliases` or on a new matrix table; what happens to `term_aliases.observation_id` (migration 125); and how a concept first met outside English is held (`terms.canonical_en` is required). A design is being prepared (`scratchpad/session_2026-11-06-base-vocabulary-review/matrix-design/`); it approves nothing.
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute(\"select name from sqlite_master where type='table' and (name like 'syn_%' or name like 'spe_%' or name like '%judgment%' or name like 'jud_%')\").fetchall())"
[('specification_source_links',), ('specification_extraction_links',), ('specifications',)]
[exit 0]
```

```
$ sed -n '1815,1820p;1750,1756p' references/project-standards.md | cut -c1-300
**3. The hand-off keys are not sound as written.**
- **Part E contradicts Part B.** Part E §4 and §5 still say `syn_items` "gains `judgment_item_id NOT
  NULL`" and `spe_items` "gains `synthesis_item_id NOT NULL`" — the single back-pointer that Part B
  and the RULE above explicitly reject. Part B was corrected after the owner's cardinality question;
  **Part E was never updated to match.**
- **`evi_items.research_item_id` is on the wrong table.** It is a per-*source* fact placed on every
  *extraction*, so two extractions from one paper can name different leads and both pass. It is also
`272/256` mined DOIs, the 12-skill-file count) and are unverifiable as written.

**7. Burden of proof unpaid.** §1 requires naming *what wrong thing reaches the guidebook* if a new
object does not exist. `jud_items`, `syn_judgment_links` and `spe_synthesis_links` were justified by
spine integrity — an argument **about the apparatus**, which §1 explicitly rejects. `figures`, the
vocabulary check and the `site_pages_fresh` promotion do pay it. The promotion also ignores the
[exit 0]
```

```
$ sed -n '915,932p' scripts/db.py | cut -c1-150
        # rewrite" — a fact written into two tables is drift waiting to happen,
        # and a parity check does not prevent that, it makes it survivable and
        # therefore permanent. Nothing ever READ the JSON: it was write-only
        # data guarded by a test. The junction is the record, and it carries its
        # own created_at.
        for ref_id in ids:
            if not conn.execute("SELECT 1 FROM evidence_sources WHERE ref_id=?",
                                [ref_id]).fetchone():
                # Named, not a bare FOREIGN KEY constraint failed. The whole
                # transaction rolls back, execution row included.
                raise Refusal(
                    f"--admitted-ref-id {ref_id} is not in evidence_sources. "
                    f"File the source first (`db.py add-source`), then log the "
                    f"search that admitted it.")
            conn.execute(
                "INSERT INTO search_admissions "
                "(exec_id, ref_id, created_at, created_by_session) "
                "VALUES (?, ?, ?, ?)", [exec_id, ref_id, ts, session])
[exit 0]
```

```
$ sed -n '5290,5302p' scripts/db.py | cut -c1-150
        incomplete record is not rewriting what the search found").

    The one place the rule lives; its cases are L03, L06 and U03 in
    scripts/tests/test_db_amend_writers.py.
    """
    was = was or 0
    return max(was, edges) if linked else max(edges, was - 1)


def link_admission(exec_id: int, ref_id: str, reason: str, session: str,
                   dry_run: bool = False):
    """Record that an EXISTING search admitted a source, when a resolved candidate says so.
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
a={r[1] for r in c.execute('pragma table_info(v_item_provenance)')}
b={r[1] for r in c.execute('pragma table_info(v_determination_provenance)')}
print('only item',sorted(a-b));print('only det',sorted(b-a))
import re
for v in ('v_item_provenance','v_determination_provenance'):
    s=c.execute('select sql from sqlite_master where name=?',(v,)).fetchone()[0]
    print(v, sorted(set(re.findall(r'(?:FROM|JOIN)\s+(\w+)',s,re.I))))
"
only item ['author_display', 'cell_state', 'jurisdiction', 'lens_code', 'parameter_domain', 'pub_title', 'pub_year', 'regulatory_stratum_only', 'source_role', 'source_tier', 'tier_basis']
only det ['claim_text', 'claimed_unit', 'claimed_value', 'comparator', 'exclusion_reason', 'extraction_id', 'figure_role', 'lens', 'role', 'state', 'tier']
v_item_provenance ['base_parameters', 'evidence_sources', 'terms', 'v_evidence_authors']
v_determination_provenance ['base_parameters', 'evidence_sources', 'source_value_extractions', 'specification_extraction_links', 'specifications', 'terms']
[exit 0]
```

```
$ grep -n -i 'migration 064\|v_item_provenance' CLAUDE.md | cut -c1-200
94:*Proof: migration 064 exists because 063 swept eight Python readers and six skills and missed
95:`v_item_provenance`; a byte-exact diff proved it clean because the view rendered 0 rows.*
[exit 0]
```

```
$ grep -n 'slug' scripts/assess/assess_cell.py | sed -n '1,40p' | cut -c1-150
22:cell's IDENTITY; the engine still gathered its EVIDENCE by slug, so `parameter_id` reached
36:`--slug` survives as the topic a determination is RECORDED under. It no longer selects
156:#   gap descriptions are PARAMETER-scoped as of 2026-09-10 (they were slug-scoped, and
158:#   is not corpus-level absence, and is not the same absence a missing slug-link is);
256:    """The sources holding an EXTRACTION FOR THIS PARAMETER. Not the slug's sources.
258:    THE DEFECT THIS CLOSES, measured 2026-09-10. This function took a `slug` and
259:    joined `source_slug_links`, so the governing set was "everything admitted to this
269:    and the slug was the only join available. `db.py add-extraction` (migration 073,
1299:def determine(conn, parameter_id, lens, slug, note):
1310:    # for THIS parameter (B4c); `slug` no longer selects evidence and is carried only
1410:                    basis=f"Qualified synthesis from {len(t3c)} T3-clinical sources on {slug}")
1572:        # Before B4c the same cell came out `stated` on the slug's evidence, none of
1732:        "slug": slug, "note": note,
1824:                  "to the slug and still have been read for no parameter at "
1963:def validate_slug(conn, slug):
1967:    the gap description, and a row naming a topic that is not in `slugs` points at nothing.
1968:    Existence only: a MERGED slug still names the topic its work was done under.
1970:    if not conn.execute("SELECT 1 FROM slugs WHERE slug=?", (slug,)).fetchone():
1972:            f"slug {slug!r}: no such slug. The slug is the topic this determination is "
1973:            f"recorded under (--slug); it does not select evidence. Name an existing one "
1974:            f"(SELECT slug, status FROM slugs); db.py has no slug writer (derive: "
1975:            f"grep -n 'INSERT INTO slugs' scripts/db.py is empty), so a new slug is a "
1976:            f"migration (see how the last one landed: grep -ln 'INSERT INTO slugs' "
2076:        f"or in --identity/--icf/--needs/--medical. --slug is not part of the cell's "
2137:    # NO LONGER "the slug to gather from" -- B4c gathers by parameter_id. This is the
2141:    ap.add_argument("--slug", required=True,
2206:    for (parameter_id, lens, slug, note) in [(args.parameter_id, lens, args.slug, args.note)]:
2208:        validate_slug(conn, slug)
2213:        det = determine(conn, parameter_id, lens, slug, note)
2218:            # It used to read "no evidence is linked via slug '<slug>' ... This
2219:            # records absence of a slug-link" and point at the item_bpc_links
2226:                    f"{parameter_id}×{lens_key(lens)}; recorded while working slug "
2227:                    f"'{slug}'. Remedy: {remedy}. Determination pending per §2.4.")
2383:                        "parameter_id", "lens", "lens_key", "slug", "note", "state", "design_scale",
[exit 0]
```

```
$ python3 -I -c "
import yaml;sm=yaml.safe_load(open('governance/stage-map.yaml'))['tables']
for t in ('source_locators','data_migrations','decisions','research_code_leads'): print(t, sm.get(t))"
source_locators research
data_migrations infrastructure
decisions infrastructure
research_code_leads research
[exit 0]
```

```
$ cd /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/r2/tree && python3 scripts/audit/claude_md_spine.py; echo EXIT=$?
EXAMINED: 7 contract stage(s) against 1 SPINE line
FAIL: CLAUDE.md's SPINE line disagrees with the contract, which is the single home.
  CLAUDE.md : research -> base -> evidence -> judgment -> synthesis -> specification -> render
  governance/pipeline-contract.yaml: base -> research -> evidence -> judgment -> synthesis -> specification -> render
  Correct CLAUDE.md, or change the contract first if the spine itself was re-ruled.
EXIT=1
[exit 0]
```

```
$ cd /tmp/claude-0/-home-user-guidebook/4a95df3b-fb51-5352-bc12-be9e9394a981/scratchpad/ag1/r2/tree && cp /home/user/guidebook/CLAUDE.md CLAUDE.md && python3 scripts/audit/claude_md_spine.py; echo EXIT=$?
EXAMINED: 7 contract stage(s) against 1 SPINE line
PASS: SPINE matches governance/pipeline-contract.yaml — base -> research -> evidence -> judgment -> synthesis -> specification -> render
EXIT=0
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
print(c.execute(\"select name from sqlite_master where sql like '%saturation_signal%'\").fetchall())"
git grep -n saturation_signal -- scripts schemas governance skills ':!scripts/migrations' | cut -c1-140 | head -8
[('search_executions',), ('v_coverage_jurisdiction',)]
scripts/db.py:677:               results_admitted: int = 0, saturation_signal: str = None,
scripts/db.py:829:        "saturation_signal": saturation_signal,
scripts/db.py:2510:    p_ls.add_argument("--saturation-signal", choices=dbcore.schema_choices("search_executions", "saturation_signal"))
scripts/db.py:2977:            saturation_signal=args.saturation_signal,
[exit 0]
```

```
$ sed -n '1,12p' scripts/audit/research_batch_dod.py >/dev/null; grep -n 'v_coverage_jurisdiction' scripts/audit/research_batch_dod.py | head -3 | cut -c1-140; grep -n 'v_coverage_jurisdiction' skills/research-log-manager_SKILL.md | head -2 | cut -c1-140
1123:    # coverage record at all (v_coverage_jurisdiction reads search_executions) and no
100:   > Coverage is derived from the log (`v_coverage_jurisdiction` / `v_coverage_language` / `v_coverage_lens`); read it with
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
for r in c.execute('select slug, exec_id, target_tier, target_evidence_type, origin, backfill, created_at from search_executions where slug is not null order by slug, exec_id limit 400'):
    pass
import collections
d=collections.defaultdict(list)
for r in c.execute('select slug, exec_id, target_tier, target_evidence_type, origin, backfill from search_executions where slug is not null order by slug, exec_id'): d[r[0]].append(r[1:])
for k,v in d.items(): print(k, [(x[0],x[1],x[2],x[3],x[4]) for x in v][:12], len(v))
"
accessible-circulation-geometry [(29, 1, 'co1', 'planned', 0), (30, 2, 'sr_meta', 'planned', 0), (31, 1, 'clinical', 'planned', 0), (32, 1, 'clinical', 'planned', 0), (33, 2, 'co1', 'planned', 0), (34, 2, 'co2', 'planned', 0), (35, 2, 'co1', 'planned', 0), (36, 2, 'co2', 'planned', 0), (37, 2, 'co1', 'planned', 0), (38, 5, 'national_fw', 'planned', 0), (39, 2, 'co1', 'planned', 0), (40, 2, 'co1', 'planned', 0)] 168
room-acoustic-performance [(1, 1, 'co1', 'planned', 0), (2, 1, 'co1', 'planned', 0), (3, 2, 'sr_meta', 'planned', 0), (4, 5, 'national_fw', 'planned', 0), (5, 1, 'clinical', 'planned', 0), (6, 1, 'clinical', 'planned', 0), (7, 2, 'sr_meta', 'planned', 0), (8, 1, 'co1', 'planned', 0), (9, 1, 'co1', 'planned', 0), (10, 1, 'co1', 'planned', 0), (11, 1, 'co1', 'planned', 0), (12, 1, 'co1', 'planned', 0)] 28
[exit 0]
```

```
$ sed -n '60,66p' governance/research-contract.yaml | cut -c1-200
  - id: R1
    phase: before-admitting
    title: "Co-1 / T2 / Co-2 pass FIRST"
    hook: >-
      Co-1 / T2 / Co-2 pass FIRST - no exceptions (Co-1 co-primary w/ T1, CRPD 4.3)
    anchor: "skills/multilingual-research_SKILL.md Step 1; CRPD Art. 4.3; governance/tier-system.md"
    enforcer: R1
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
for r in c.execute('select s.slug, a.exec_id, a.ref_id, e.evidence_type, e.tier from search_admissions a join search_executions s using(exec_id) join evidence_sources e using(ref_id) order by s.slug, a.exec_id, a.ref_id'): print(r)
" | head -70
(None, 203, 'REF-00468', 'grey', 3)
('accessible-circulation-geometry', 30, 'REF-00984', 'sr_meta', 2)
('accessible-circulation-geometry', 31, 'REF-00983', 'clinical', 1)
('accessible-circulation-geometry', 31, 'REF-00985', 'clinical', 1)
('accessible-circulation-geometry', 31, 'REF-00986', 'clinical', 1)
('accessible-circulation-geometry', 38, 'REF-00988', 'national_fw', 5)
('accessible-circulation-geometry', 42, 'REF-00989', 'co1', 1)
('accessible-circulation-geometry', 43, 'REF-00990', 'code', 6)
('accessible-circulation-geometry', 43, 'REF-00991', 'code', 6)
('accessible-circulation-geometry', 45, 'REF-00992', 'code', 6)
('accessible-circulation-geometry', 46, 'REF-00993', 'co1', 1)
('accessible-circulation-geometry', 49, 'REF-00994', 'standard_eb', 4)
('accessible-circulation-geometry', 51, 'REF-00995', 'code', 6)
('accessible-circulation-geometry', 52, 'REF-00996', 'national_fw', 5)
('accessible-circulation-geometry', 57, 'REF-00997', 'national_fw', 5)
('accessible-circulation-geometry', 59, 'REF-00998', 'national_fw', 5)
('accessible-circulation-geometry', 62, 'REF-00999', 'clinical', 3)
('accessible-circulation-geometry', 64, 'REF-00977', 'sr_meta', 2)
('accessible-circulation-geometry', 64, 'REF-01000', 'clinical', 3)
('accessible-circulation-geometry', 65, 'REF-01001', 'clinical', 3)
('accessible-circulation-geometry', 70, 'REF-00979', 'clinical', 1)
('accessible-circulation-geometry', 70, 'REF-00980', 'clinical', 1)
('accessible-circulation-geometry', 70, 'REF-01002', 'clinical', 1)
('accessible-circulation-geometry', 77, 'REF-01003', 'clinical', 3)
('accessible-circulation-geometry', 77, 'REF-01004', 'clinical', 1)
('accessible-circulation-geometry', 78, 'REF-01005', 'grey', 3)
('accessible-circulation-geometry', 91, 'REF-01006', 'co1', 1)
('accessible-circulation-geometry', 93, 'REF-01009', 'co1', 1)
('accessible-circulation-geometry', 95, 'REF-01011', 'clinical', 3)
('accessible-circulation-geometry', 99, 'REF-01007', 'clinical', 3)
('accessible-circulation-geometry', 100, 'REF-01008', 'grey', 3)
('accessible-circulation-geometry', 105, 'REF-01029', 'grey', 3)
('accessible-circulation-geometry', 114, 'REF-01015', 'code', 6)
('accessible-circulation-geometry', 115, 'REF-01016', 'code', 6)
('accessible-circulation-geometry', 116, 'REF-01015', 'code', 6)
('accessible-circulation-geometry', 117, 'REF-01016', 'code', 6)
('accessible-circulation-geometry', 118, 'REF-01017', 'code', 6)
('accessible-circulation-geometry', 119, 'REF-01017', 'code', 6)
('accessible-circulation-geometry', 125, 'REF-01012', 'code', 6)
('accessible-circulation-geometry', 126, 'REF-01013', 'code', 6)
('accessible-circulation-geometry', 127, 'REF-01014', 'standard_eb', 4)
('accessible-circulation-geometry', 128, 'REF-01018', 'code', 6)
('accessible-circulation-geometry', 132, 'REF-01019', 'code', 6)
('accessible-circulation-geometry', 140, 'REF-01026', 'code', 6)
('accessible-circulation-geometry', 147, 'REF-01020', 'code', 6)
('accessible-circulation-geometry', 148, 'REF-01021', 'national_fw', 5)
('accessible-circulation-geometry', 157, 'REF-01025', 'grey', 3)
('accessible-circulation-geometry', 159, 'REF-01023', 'code', 6)
('accessible-circulation-geometry', 164, 'REF-01030', 'national_fw', 5)
('accessible-circulation-geometry', 166, 'REF-01027', 'code', 6)
('accessible-circulation-geometry', 169, 'REF-01028', 'code', 6)
('accessible-circulation-geometry', 171, 'REF-01029', 'grey', 3)
('accessible-circulation-geometry', 182, 'REF-01022', 'grey', 3)
('accessible-circulation-geometry', 183, 'REF-01024', 'national_fw', 5)
('accessible-circulation-geometry', 186, 'REF-01031', 'code', 6)
('accessible-circulation-geometry', 189, 'REF-01032', 'code', 6)
('accessible-circulation-geometry', 192, 'REF-00139', 'code', 6)
('accessible-circulation-geometry', 193, 'REF-01033', 'clinical', 1)
('accessible-circulation-geometry', 193, 'REF-01034', 'clinical', 1)
('accessible-circulation-geometry', 193, 'REF-01035', 'clinical', 3)
('accessible-circulation-geometry', 193, 'REF-01036', 'clinical', 1)
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
cols=[r[1] for r in c.execute('pragma table_info(evidence_sources)')]
print([x for x in cols if 'grey' in x or 'warrant' in x or 'note' in x or 'type' in x or 'peer' in x])
for r in c.execute(\"select ref_id, evidence_type, source_type, grey_flag, substr(coalesce(verification_note,''),1,200), substr(pub_title,1,70) from evidence_sources where ref_id in ('REF-01022','REF-01025','REF-01029')\"): print(r)
print('NO sources:')
for r in c.execute(\"select ref_id, lang_detected, substr(pub_title,1,80), publisher from evidence_sources where jurisdiction='NO'\"): print(r)
"
['source_type', 'pub_year_note', 'evidence_type', 'co1_source_type', 'bpc_note', 'grey_flag', 'grey_reason', 'verification_note', 'notes', 'subtype', 'code_currency_notes', 'standard_number_note', 'author_display_note', 'publisher_note']
('REF-01022', 'grey', 'letter', 1, '', 'Internetconsultatie verzamelbesluit Bbl 2024 (reactie van Ieder(in), 9')
('REF-01025', 'grey', 'grey', 1, '', 'Yttrande över Boverkets remiss ang. Revidering av Boverkets byggregler')
('REF-01029', 'grey', 'report', 1, '', 'Metodología para la evaluación e implementación de Accesibilidad Unive')
NO sources:
('REF-01012', 'no', 'Byggteknisk forskrift (TEK17) — § 12-16. Rampe', None)
[exit 0]
```

```
$ python3 -I -c "
import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
for r in c.execute(\"select ref_id, grey_reason from evidence_sources where ref_id in ('REF-01022','REF-01025','REF-01029')\"): print(r)
"
('REF-01022', "consultation reply (internetconsultatie reactie) by a national umbrella organisation, dated 9 November 2023 and signed by its director; not peer-reviewed; no DOI. CO-1-ADJACENT AND NOT CLAIMED AS CO-1 (D-0178): the letter calls its author 'het netwerk van mensen met een beperking of chronische ziekte', but its governance (who controls the network) was not retrieved -- iederin.nl pages answered with a bot-challenge stub (HTTP 202) -- and no individual disabled author or consulted member is named.")
('REF-01025', "consultation reply (remissvar) to a government agency by a rights organisation, dated Stockholm 2007-01-10; not peer-reviewed; no DOI; hosted on the organisation's own site")
('REF-01029', "report authored by a disability-sector umbrella platform (CERMI Comunidad de Madrid), dated 'Madrid, diciembre de 2018', with municipal support credited on the last page ('Con el apoyo de'); not peer-reviewed; no DOI; hosted on the Ayuntamiento de Madrid site")
[exit 0]
```

## Round 2 (antagonist objections): commands not logged by the wrapper, and final checks
```
$ read 01-antagonist-objections.md and 01-antagonist-blind.md; re-ran for each blocking and material objection (outputs above in this log): migration_reproducibility with a value-only edit and with --deep (REQ-090); parameter 4 x MOB/DEAF/ALL roles and parameters 5, 6, 8, 11 x DEAF (REQ-077); counterfactual: re-tag parameter 3 MOB figures ALL, determine x DEAF -> governing [(ALL,35)]; delete_connection / unlink_admission source and PS:3540-3590 (REQ-018); AUTOINCREMENT derivation (REQ-019); add-parameter --term-id TERM-004 (REQ-029/033); syn_/spe_ table existence, PS:1786-1791, db.py:915-932 (REQ-012); WP lines 78,79,127,135,139,141,143,150; PS:583-586 and RATIFICATION-RECORD 115-134 (HS-A06); view column sets (v_item_provenance); claude_md_spine red test on a scratch tree; search and admission order per slug (REQ-052); grey_reason of the three non-English grey sources (REQ-066); saturation_signal view (HS-A13); PS:368-382, PS:5041-5046, PS:588-592, PS:170-173.
$ python3 -I accept.py (marks vs evidence, top/bottom side, prose lines):
rows 118 mark-bad 0 side-gaps 0
prose lines (whole file) 75
$ X02c diff HS1 vs final -> HS-A06, HS-A09, HS-A13, REQ-017, 018, 019, 029, 033, 038, 052, 064, 066, 074, 090, 098 differ (boundaries B9, B12 changed separately)
$ resolution table tallies (grep -c on the table): upheld 95, amended 48 (includes the section 1.1 header row), withdrawn 1, not attacked 39; referred markers: 9 rows
```

## End of round 2
```
c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d  data/guidebook.db
```
