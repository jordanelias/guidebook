# Implementer Z log (2026-11-26): B3, B4, B6, B8

No git writes. No DB or migration touched. Edit tool only.

## B3: DONE (with declines listed)
Derivation: `git grep -n -F 'workplan-co0007' -- . ':(exclude)transcripts' ':(exclude)sessions' ':(exclude)_archived'`
(the brief's `':!_archived'` form fails: git reads `!_` as pathspec magic; use `:(exclude)`).
`git ls-files | grep co0007`: every workplan-co0007-* file is under `workplan/_superseded/` only.

Repointed `workplan/workplan-co0007-` to `workplan/_superseded/workplan-co0007-` (path-form pointers only):
- architecture/storage-derivation.md:4
- governance/adversarial-use-framework.md:5
- governance/audience-priority.md:173,174
- governance/co1-operational.md:21,81
- governance/doctrine-recheck.md:5 (x2), :306
- governance/legal-regulatory.md:5, :13
- governance/migration-survival.md:4, :142
- governance/mission-PROVISIONAL.md:113, :175
- governance/mission-and-epistemics.md:126, :165
- governance/pre-stage-a-decisions.md:141
- governance/project-instructions-v10_14.md:112
- governance/workplan-adoption.md:16, :82, :126, :136
- workplan/a1-a2-iteration-plan.md:4, :53, :54
- workplan/a5-handoff.md:48, :140
- workplan/roadmap-2026-04-27.md:9
- workplan/bpc-rewrite-workplan-2026-05-11.md:502, :554-557
- workplan/workplan-item-audit-pipeline-co0009.md:526
Check: every new `workplan/_superseded/workplan-co0007-*.md` path resolves (`test -e`): audit, synthesis, v3, v3-amendments, v4 all OK.

Declined (live files, not edited):
- governance/pi-revision-co.md:76,80,121,132: quoted proposal text and a Decision-record template; repointing would alter a quoted proposal.
- governance/migration-survival.md:148: names `workplan-co0007-audit-1.md`, which exists under no path (only `workplan-co0007-audit.md`); not a repoint.
- Bare-name mentions with no path (citations by name, not pointers): architecture/d0139-amendment-2.md:4; data/adversarial_use/catalog.yaml:19,41,60; governance/adversarial-use-framework.md:17; governance/project-instructions-v10_14.md:13 (changelog); scripts/bootstrap.sh:101 (echo string; CLAUDE.md says do not run bootstrap); workplan/roadmap-2026-04-27.md:2; workplan/website-preparation.md:8; workplan/deprecated/website-preparation-stale-2026-05-08.md:4,9; workplan/workplan-item-audit-pipeline-co0009.md:534; workplan/workplan-reconciliation-2026-05-08.md (all, bare names in a dated status table).
- decisions/DR-2026-07-12-website-architecture-lock.md:13: bare name, and decisions/ needs an attestation (rule 2).
- data/guidebook.db (3 hits): DB, forbidden.
- scratchpad/* hits: session working files, not live documents.
- Not mine: governance/decision-protocol.md (other implementer).

## B4: DONE
- governance/mission-and-epistemics.md:99 before: "`evidence_type` (`clinical`, `co1`, `co2`, `sr_meta`, `standard_evidence_based`, `national_framework`, `code`) per Stage 0.5 Decision T-03"
  after: "`evidence_type` (the vocabulary `db.py add-source` admits: the keys of `TIER_MAP` in `schemas/tier_derivation.py`) per Stage 0.5 Decision T-03".
  REPORT CORRECTION: the adjudicator/antagonist-2 said `schemas/enums.py` is the vocabulary's only home. Not so: `db.py _ladder_evidence_types()` and add-source validate against `schemas/tier_derivation.TIER_MAP` keys (clinical, co1, co2, code, grey, national_fw, sr_meta, standard_eb), while `EvidenceType` also carries `unknown`. Two homes (a rule-5/8 finding, not fixed here); I pointed at the one the writer enforces. The Co-2 sentence after it is unchanged.
- governance/evidence-architecture.md:92 before: "but only 27 of 640 sources carry any `evidence_population_match` row" after: "but not every source carries an `evidence_population_match` row (compare `select count(distinct ref_id) from evidence_population_match` with `select count(*) from evidence_sources`)".
- :131 before: "With `source_value_extractions` empty, multi-axis cells are honestly" after: "Multi-axis cells are honestly" (clause contradicted :112).
- :155 before: "sixteen tests against a synthetic fixture and eight fault injections ... rather than by a determination that has reached `stated` — both live rows are `pending`, and one is retired-and-superseded." after: "tests against a synthetic fixture and fault injections ... rather than by a determination that has reached `stated` (derive the live states: `select state, retired_at is null, count(*) from specifications group by 1, 2`)."
  (Live today: no `stated` row, so the remaining claim holds; derive, do not trust.)
- Not touched: tiers, Co-2 wording, T3/T4 bands. Other numbers in the file (24 jurisdictions, 1500/1800/2440 mm, "selected 10/4") are research or test facts, not volatile counts; :153's dated narrative left as is.
- Atom check: no atom in workplan/pipeline-state-graph quotes any edited sentence. Pre-existing atom failures EVI-205, EVI-209 (evidence-architecture :143/:145, lines not edited).

## B6: DONE
- governance/conceptual-model.md: one line inserted as new line 5, directly under the Status line (no blank line, so it stays in the header block; no ⚠):
  "**Item layer removed (noted 2026-11-26):** the Item entity (ENT-08) and every relationship keyed on it in §2 and §2.1 were removed with the item layer (owner ruling 2026-09-01; `scripts/migrations/107_drop_item_layer_cluster.sql`); determinations are keyed on a parameter and at least one lens column (CLAUDE.md §6). Item codes (`[A-Z]-NN`, such as `E-08`) are prior-version content: never file a finding into one. §2.1's evidence-flow paragraph, which `governance/pipeline-contract.yaml` cites as the specification stage's anchor, is not affected."
- Migration derived: `git grep -l 'drop_item_layer' scripts/migrations` gives 107_drop_item_layer_cluster.sql only. Its header gives the 2026-09-01 deletion and RULINGS R36.
- The banner does not claim §1.1's schema files are gone (`schemas/evidence_source.py` exists; specification.py, bpc_metadata.py, connection.py, slug.py, gap.py are absent) and does not cite migration 071 for a populations array.
- FOR THE PIPELINE-CONTRACT OWNER: the insert moves the cited paragraph from line 90 to line 91. `governance/pipeline-contract.yaml:286` still reads `conceptual-model.md:90`; it should read `:91`. I did not edit pipeline-contract.yaml (not mine). Atom refs in workplan/pipeline-state-graph are quote-matched with a 3-line tolerance, so they do not break; verify_atoms on atoms-ent.jsonl reports only pre-existing ENT-255, ENT-378 (files not edited).
- Rest of the document unchanged. functional-taxonomy.md not touched.

## B8: PARTIAL (3 notes, 1 declined on judgment)
`git grep -l -E '\b[A-Z]-[0-9]{2}\b' -- skills` gives four files. `.claude/skills/{cross-reference-resolver,toc-editor}/SKILL.md` are symlinks (mode 120000) to skills/; voice-style and adversarial-research have no .claude/skills entry. Edited only skills/*.
Same one-line blockquote added at the top of the body of each:
"> **Item codes are prior-version content.** The item layer was deleted (owner ruling 2026-09-01; `scripts/migrations/107_drop_item_layer_cluster.sql`): an `[A-Z]-NN` code met below or in the corpus is never a container to file into (CLAUDE.md §7)."
- skills/cross-reference-resolver_SKILL.md (after frontmatter): PRESUPPOSES the item layer. :37 validates "see item G-03" against Part 4 item headings (categories A–K); :167-169 checks `part7_items`.
- skills/toc-editor_SKILL.md (under the H1): PRESUPPOSES. Item codes are TOC structural units (RECODE of item codes, :56 "remove J-01 only or all of Category J?", :89 "formerly J-01").
- skills/voice-style_SKILL.md (under the provenance line): example-only (:109 "evidence table for A-03", :252 sample sentence "(A-16)"), but the examples teach item codes as the way to name things in book prose, so the note is added.
- skills/adversarial-research_SKILL.md: DECLINED. Codes appear only as labels on historical worked cases (:294-312, "GAP-069 A-10" and so on). The skill does not file into or validate item codes. Does not presuppose the layer.

## Verify
- retired_vocabulary_audit.py (ran in about 26 s after ensure-deps; deps OK): rc=1, 344 hits corpus-wide (pre-existing). No hit falls on any line I edited. The project-instructions-v10_14.md hits are at :11, :81, :114, :148, :170-172, not at my edited :112. Full output: /tmp/claude-0/-home-user-guidebook/f8d4d6c2-8f72-53c6-8e31-d3258750c5f6/scratchpad/z-rva.txt
- Caller sweep for the mission :99 list: the only other copy is a scratchpad dossier (not live).

## git diff --stat (my files)
```
 architecture/storage-derivation.md              |  2 +-
 governance/adversarial-use-framework.md         |  2 +-
 governance/audience-priority.md                 |  4 ++--
 governance/co1-operational.md                   |  4 ++--
 governance/conceptual-model.md                  |  1 +
 governance/doctrine-recheck.md                  |  4 ++--
 governance/evidence-architecture.md             |  6 +++---
 governance/legal-regulatory.md                  |  4 ++--
 governance/migration-survival.md                |  4 ++--
 governance/mission-PROVISIONAL.md               |  4 ++--
 governance/mission-and-epistemics.md            |  6 +++---
 governance/pre-stage-a-decisions.md             |  2 +-
 governance/project-instructions-v10_14.md       |  2 +-
 governance/workplan-adoption.md                 |  8 ++++----
 skills/cross-reference-resolver_SKILL.md        |  2 ++
 skills/toc-editor_SKILL.md                      |  2 ++
 skills/voice-style_SKILL.md                     |  2 ++
 workplan/a1-a2-iteration-plan.md                |  6 +++---
 workplan/a5-handoff.md                          |  4 ++--
 workplan/bpc-rewrite-workplan-2026-05-11.md     | 10 +++++-----
 workplan/roadmap-2026-04-27.md                  |  2 +-
 workplan/workplan-item-audit-pipeline-co0009.md |  2 +-
 22 files changed, 45 insertions(+), 38 deletions(-)
```
