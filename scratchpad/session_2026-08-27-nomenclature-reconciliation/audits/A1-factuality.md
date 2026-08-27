# A1 — Factuality audit of NOMENCLATURE.md and the two 2026-08-27 RULE entries

Auditor: adversarial factuality pass, 2026-08-27. Every number below recomputed from
`data/guidebook.db` (`mode=ro`, `user_version` 64) or from the tree. 78 discrete claims checked:
**5 refuted outright, 6 more overstated or internally inconsistent, 1 unverifiable, 66 confirmed.**
Replay commands are inline; DB queries were run via python3 `sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)`
with a fresh cursor per query.

## WRONG

### W1. "Nine of 93 item names carry a quantified determination" (Part L.3, and K.2's framing) — REFUTED. The true count is ≥23.
The claimed nine (E-08, E-01, E-04, E-05, G-05, G-06, B-05, D-11, H-01) are exactly the names whose
unit is a metre or millimetre. The scan missed every non-length unit and the ratio form:

- A-02 `NRC ≥0.85` · A-03 `STC ≥35` · A-06 `NRC ≥0.70` · A-08 `NC-25 Maximum` · A-14 `STC ≥50`
- A-16 `≥8 m², one per floor or per 500 m² GFA` · B-01 `≥150 EML` · B-06 `≥300 Lux Range`
- B-08 `≤30 Gloss Units` · B-11 `≤2700 K After 19:00` · C-04 `LRV ≥30` · E-03 `≤1:20` (the ratio)
- E-07 `PTV ≥36` · I-01 `≤22 N` · borderline: F-04 `MERV 13+`

Replay: `SELECT item_code, name FROM items` then any regex covering `≥≤`, `\d+[:×–-]\d+`,
`\d+\s*(mm|m|m²|lux|dB|K|N|EML|%)`, `1:\d+`. 23 clear hits + F-04. Standard designations
(B-04 `IEEE 1789-2015`, E-09 `ISO 23599:2019`) excluded. Consequence: L.3's "nine parameters are
asserted in the book with no determination behind them" understates its own finding ~2.6×, and the
proposed vocabulary check "would fire on nine rows today" is wrong — it would fire on ~23-24.

### W2. "41 foreign keys cross a stage boundary; 39 stay inside one" — reproduces ONLY under the superseded five-stage map. It does not survive the document's own six-stage assignment.
Recomputed from `PRAGMA foreign_key_list` over all 66 tables: 80 FK constraints total.
- Under the 2026-08-25 five-stage map (STAGE-TABLE-MAP.md, substrate counted as its own layer):
  **41 cross / 39 same** — arithmetic and the seven-column landing table all reproduce exactly
  (slug 14, item_code 10, population_code 7, evidence_sources.ref_id 6, gaps 2, exec_id 1,
  citation_id 1; per-stage attributions res 6·evi 3·jud 1·syn 3·ren 1 etc. all verified).
- Under NOMENCLATURE's OWN Part E six-stage assignment (evidence_population_match→judgment,
  conflicts/convergence_assessment→synthesis, specifications/spec_value_probes/
  probe_population_links/specification_source_links→specification): **43 cross / 37 same**, landing
  on **EIGHT** columns. The two additions: `evidence_population_match.ref_id → evidence_sources`
  (judgment→evidence) and `specifications.convergence_id → convergence_assessment`
  (specification→synthesis).
- Under the five-stage map with its own three declared judgement calls flipped
  (jurisdictional_values→render, weighting_profile→synthesis, supersession_check→synthesis):
  **42 cross / 38 same**.

Part C carries a parenthetical hedge; but the 2026-08-27 `-item` RULE in project-standards.md and
CLAUDE.md's pipeline section both assert "All **41**" flatly inside a six-stage frame, where the
measured figure is 43. A number that changes when the document's own ruling is applied to it should
not be stated as "measured 2026-08-27" without the frame.

### W3. "source_value_extractions' sixteen loc_* columns" (Part E, res_items note) — REFUTED: 15.
`PRAGMA table_info(source_value_extractions)` → loc_ columns are 7 start + 7 `_end` + `loc_note` =
**15**. Sixteen is reached only by counting `locator_scheme`, which does not match `loc_*`.

### W4. "`jurisdiction`, on 9 tables" (C.3) — REFUTED: 11 tables.
Column named exactly `jurisdiction` exists on: evidence_sources, search_coverage, term_aliases,
lang_jur_map, jurisdictional_values, search_executions, economics_entries, source_value_extractions,
reasoning_doc_citations, reference_stubs, source_locators. Replay: `PRAGMA table_info` per table.

### W5. "retired population codes … live only in 12 skill files" (I.5) — REFUTED: 17 live skill files.
The 12 retired codes are from `scripts/validate_population.py:79` RETIRED_CROSSWALK. Token-boundary
grep (`grep -lE '(^|[^A-Za-z0-9_-])CODE([^A-Za-z0-9_-]|$)' skills/*_SKILL.md`) per code:
VIS 12 · OFS 10 · DBL 8 · NEU 6 · UPL 5 · SENS 4 · PCS 3 · MCAS 3 · POTS 3 · EXH 2 · CFS 0 · LCOV 0.
**Union = 17 files.** "12" is the VIS-only figure (or the count of retired codes), copied from
WALK-REPAIR-PLAN P0.4 without re-derivation. The other half — "0 in the database" — is confirmed:
exact-match of all 12 codes against every population-code-bearing column returns 0.

## OVERSTATED / INTERNALLY INCONSISTENT (number right or nearly right, statement not)

### O1. Part I's per-stage row table contradicts Part E's own stage moves.
Part I: research 1,087 · evidence 92 · judgment 0 · synthesis 0 · render 17 · substrate 4,122 ·
total 5,318 — every figure reproduces **only if `evidence_population_match` (25 rows) stays in
evidence**. Part E of the same document moves it to judgment (‡), under which evidence = 67 and
judgment = **25, not 0**. "The three stages being redesigned contain no data at all" is false under
the document's own assignment: judgment would carry 25 graded rows that DO need migrating.

### O2. "Not one foreign key in the schema lands on any stage's hand-off object" (Part B; repeated in the RULE) — contradicted by its own table three lines later.
Two FKs land on hand-off objects: `extraction_population_links → source_value_extractions` and
`specification_source_links → specifications` (both same-stage, as the table itself shows: 1 and 1).
The defensible claim is "no cross-stage FK lands on a hand-off object" — which is confirmed
(source_locators 0 inbound, bpc_metadata 0 inbound, the other two 1 same-stage each).

### O3. "named in six governance documents" (K.1) — undercounted; enumeration wrong.
`grep -rl best_practice_synthesis governance/` → **8 files**: 6 .md (adversarial-use-framework,
doctrine-recheck, evidence-methodology, jurisdiction-philosophy, **migration-survival**,
project-instructions-v10_14) + 2 .yaml (pipeline-contract, research-contract). "Six" holds only if
"document" excludes the two YAML contracts; the prose enumeration omits migration-survival.md —
the heaviest user (78-BPC survival table) — while repo-wide the token appears in ~100 files.
"It is not a column" in any of the 66 tables: CONFIRMED.

### O4. "All three modes … require a non-`[\w-]` character after the token" (08-26 register RULE, checked because its line-cites were in scope) — false for `literal` mode.
`retired_vocabulary_audit.py:102`: literal's lookahead is `(?![\w])`, hyphen allowed. The
conclusion ("`AX-` cannot be expressed at all") survives, since `A` in `AX-AMB` is `\w`.

### O5. Six-stage RULE: "CLAUDE.md's pipeline section … all state five and must state six" — stale for CLAUDE.md.
CLAUDE.md:25 now states the six-stage arrow. Still five: `governance/pipeline-contract.yaml`
(stages: research, evidence-collection, judgment, synthesis, render — no specification) and
`tools/pipeline_completeness.py:37` STAGES. One of the three named surfaces has already moved.

### O6. "seven cross-stage views" (Part H) — correct only under an unstated convention.
Parsing all 18 view SQLs with nested-view resolution: the seven listed views are exactly those
whose base tables span more than one bucket **when substrate counts as a bucket** — the same
convention the FK count uses, so the figure is coherent. But `v_item_extractions`
(sve+evidence_sources+items) and `v_coverage_priority` (search_executions+slugs+lang_jur_map) span
one stage plus substrate only; under stage-to-stage crossing the count is **5**. The convention is
never stated, and Part H's own caveat that the spans are owed a six-stage re-derivation is right:
under Part E, `v_divergence` becomes cross-stage (confirmed: it reads exactly `specifications` +
`convergence_assessment`, nothing else).

## UNVERIFIABLE
- J.1's "a separate OpenAlex pass found 272 mobility DOIs of which 256 are in neither store" —
  external measurement, not reproducible from the repository. (The adjacent figures ARE
  reproducible and check out: 138 distinct DOIs in `citation_mining.connections_produced`, of
  which 4 appear in `source_locators.doi`.)
- K.2's "23 / 14 / 11 literal-string lines": replicates exactly with the authoring session's own
  command (`grep -cE '^\s*(f?"""|f?"[^"]{40,})'`, from commands.jsonl) — but the metric is a grep
  hit-count of the precise kind RULE 2026-08-22 forbids reporting as a finding. Confirmed as
  measured; meaningless as stated ("literal-string lines" is undefined in the document).

## CONFIRMED (command → result)

1. `PRAGMA user_version` → 64. Tables excluding sqlite_* → **66**. Views → **18**.
2. Zero-row tables → **33 of 66** ✓ (list verified).
3. Per-stage rows (five-stage/Part I assignment): research **1,087** · evidence **92** · judgment
   **0** · synthesis **0** · render **17** (all `rooms`) · substrate **4,122** · total **5,318** ✓
   (subject to O1).
4. FK inbound on hand-off objects: source_locators **0** · source_value_extractions **1**
   (same-stage) · specifications **1** (same-stage) · bpc_metadata **0** ✓.
5. Seven-column landing table and every per-stage attribution in Part C ✓ under the five-stage map;
   arithmetic 14+10+7+6+2+1+1 = 41 ✓ (subject to W2).
6. `item_bpc_links` FKs → slugs.slug + items.item_code, never bpc_metadata ✓. `spec_value_probes`
   FKs → evidence_sources.ref_id, items.item_code, slugs.slug, never source_value_extractions ✓.
7. AX- census, `GLOB '*AX-*'` per cell over every column of every table: **288** total; **249** in
   the four `axis_code` columns (axes 17, access_need_axis_map 21, item_axis_links 158,
   population_axis_map 53); **39** across exactly **twelve** other columns ✓ (exact).
8. `python3 scripts/generate/build_site.py --check` → `FRESH: 93 page(s) match a fresh render.` /
   `EXAMINED: 93`, exit 0 ✓. `ls site/specs/*.html | wc -l` → 93; items → 93 ✓.
9. `grep -o tools scripts/regenerate_derived.sh | wc -l` → **7**; `parts`/`site`/`audits` → **0/0/0** ✓.
10. `ls skills/*_SKILL.md | wc -l` → **49** (plus `skills/deprecated/` holding 12, correctly excluded) ✓.
11. Clue store: source_locators **875** (all distinct) · evidence_sources **10** · intersection
    **4** (REF-00325, -00561, -00578, -00607) · admitted-with-no-clue-row **6** (REF-00965…-00970)
    · malformed **11** `REF-VERIFIED-*` ids (001–012 with -008 absent) · `MAX(ref_id)` =
    REF-VERIFIED-012 ✓ all exact. Numbered maxima REF-00964 (locators) / REF-00970 (sources) ✓.
12. Part J groups: leads 875+109+60+0 = **1,044** over 4 tables ✓; acts = 7 tables, 39 rows ✓;
    population junctions = 6 tables, 372 rows, **5 of 6 empty** ✓.
13. `v_divergence` reads exactly `specifications` + `convergence_assessment` ✓ (sqlite_master SQL).
14. File:line citations, all opened: `057_baseline_2026-08-12.sql` — v_value_independence at
    6692–6701, `GROUP BY COALESCE(parameter_canonical, parameter), population_code` at :6701, no
    item_code ✓; `tools/pipeline_completeness.py:42` = `def stage_label` ✓ (STAGES at :37, still
    five ✓); `retired_vocabulary_audit.py:93-108` = the three mode branches ✓ (see O4);
    `conceptual-model.md:90` = "BPC synthesis produces specifications" ✓; `pipeline-map.yaml:78` =
    the re-entrancy sentence ✓ and `:160` = the citation_mining self-loop line ✓;
    `schemas/source_value_extraction.py:89` = `# normalized for join (lowercase, hyphens)` ✓;
    `evidence-methodology.md:312` = "the best_practice_synthesis section of the BPC file" ✓;
    `build_site.py:14` = the stale "six items … including A-18" comment ✓ (and it is indeed stale:
    0 missing pages today ✓).
15. Schema details: bpc_metadata **16 columns**, PK `slug` ✓; epm PK `match_id` only, no other
    UNIQUE, **25 rows across 10 sources** ✓; sve carries no UNIQUE index at all (so none on
    (ref_id, parameter)) ✓; search_executions **23 columns** incl. `mining_direction`,
    `jurisdiction`, `language`, `slug` ✓; source_locators has no origin column, nearest is
    `recovered_from` ✓; `conflicts.pop_a/pop_b` free text, only FK is item_code ✓;
    `specifications.gap_register_id` keyed vs `conflicts.gap_id` unkeyed ✓; `slugs.serves_axes`,
    `situations.attaches_axes`, `source_locators.used_in_bpcs` exist ✓; the six named surrogate
    INTEGER PKs (exec_id, candidate_id, jv_id, specification_id, convergence_id, extraction_id) ✓;
    `search_admissions` PK (exec_id INTEGER, ref_id TEXT) ✓; `term_aliases` PK
    (term_id, alias, language) ✓; `local_ref_id` on exactly 3 tables, holding `RAP-01` etc. ✓;
    the seven singular ref-id column names all exist ✓ (note: two packed-plural variants the doc
    does not list also exist — `search_executions.admitted_ref_ids`,
    `supersession_check.superseding_ref_ids`); no diagram/figure/caption/alt-text column anywhere ✓;
    `specifications` has no rationale column ✓ (though the "only …" enumeration omits `tier_basis`);
    jurisdictional_values 109 rows, 0 non-null value_text/value_numeric ✓; MOB
    item_population_links = **31** ✓; `db.py` has no extraction writer (`grep source_value_extractions scripts/db.py` → nothing) ✓.
16. Registry/gates: `pipeline_completeness_fresh` blocking ✓, `evidentiary_audit_fresh` blocking ✓,
    `site_pages_fresh` advisory, cmd = build_site.py --check ✓, no caller outside the registry
    (grep over scripts/, tools/, .github/, .claude/) ✓ — though "nothing calls it" elides that
    `run_checks.py` does execute registry checks; the accurate form is "no regeneration script or
    workflow invokes build_site.py".
17. `site/specs/e-08.html`: `<h1>` with ≥1200 mm at :53 over "not yet computed" banner at :92 ✓;
    the value sits in `items.name` for E-08 ✓; `site/index.html:7` exists and carries prose claims ✓.
18. Part I mechanics: 057 header quote exact ("collided with 19 of them … AFTER_DATA, schema 056") ✓;
    live data migrations `ls scripts/migrations/data_* | wc -l` → **33** ✓;
    `_archived/scripts/migrations/` → **359** files ✓; `data_migrations` table **352** rows ✓;
    `references/bpc-reasoning/` → **2** files ✓; `migration_reproducibility` blocking ✓.
19. K.4/K.1 satellite: the one real reasoning doc (room-acoustic-performance.md) cites 11 distinct
    REF- ids of which **8** are not in evidence_sources ✓; `reasoning_doc_citations` holds 0 rows ✓;
    `slugs.bpc_path` exists ✓. Skill quote in L.1 matches
    `skills/item-specification-writer_SKILL.md:7-9` ✓.
20. Part A: `stage_id[:3]` yields six distinct prefixes (res evi jud syn spe ren) ✓.

## Confidence notes (right numbers, stronger claims than the evidence)
- The "41" is the headline of both RULE entries and CLAUDE.md, always without the five-stage
  qualifier Part C carries. Under the ruling those very documents record, it is 43 (W2).
- Part H presents "seven, not four" as a boundary-crossing fact; it is a convention-dependent fact
  (O6), and the document that scolds the old list for mis-deriving does not state its convention.
- C.1's "REF-VERIFIED-001 … -012" reads as 12 ids; there are 11 (-008 absent). The count claimed
  is 11 and is right, but the range notation invites the wrong count.
- L.3's gate proposal inherits W1: a check sized to "nine rows" is sized to the wrong regex, not
  to the vocabulary defect it names.
- I.3's "78% substrate" = 4,122/5,318 ✓ arithmetic — but only under the epm-stays-in-evidence
  assignment (O1).

## Digest
78 claims checked · 5 refuted (W1–W5) · 6 overstated/inconsistent (O1–O6) · 1 unverifiable · 66 confirmed.
