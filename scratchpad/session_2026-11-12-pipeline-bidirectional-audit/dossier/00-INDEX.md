# 00 — Dossier index

Regenerate everything with `python3 -I scratchpad/session_2026-11-12-pipeline-bidirectional-audit/build_dossier.py` and `…/build_owner_prose.py`. Every count lives in the generated files, none here (CLAUDE.md rule 7a).

| File | Holds | Provenance |
|---|---|---|
| `10-pipeline-itself.md` | spine, contract criteria (and which are unenforced), core pipeline code, migrations, check registry, skills/agents/commands | derived |
| `11-run-pipeline-skill.md` | the end-to-end orchestration skill, verbatim | verbatim |
| `12-db-verb-matrix.md` | every `db.py` verb → tables written/read → stage; tables no verb writes | derived (static analysis; read column can over-report) |
| `13-code-index.md` | every Python unit under `scripts/`, `schemas/`, `.claude/hooks/` → tables it writes → primary stage | derived |
| `20-stage-base.md` … `26-stage-render.md` | per stage: tables, views touching it, contract criteria, writers, readers, tests, checks, skills, prose homes | derived from `governance/stage-map.yaml` (judged by the owner's sessions) |
| `30-data-tables.md` | every table by stage with FKs, the views and the stages they span, the UNWRITABLE derivation, full DDL | derived / verbatim DDL |
| `40-owner-prose-index.md` | index of the owner's rulings in `references/project-standards.md`, keyword-tagged | derived (tags heuristic) |
| `41-owner-rulings-verbatim.md` | those rulings in full | verbatim |
| `42-doctrine-verbatim.md` | mission, ethos, jurisdiction philosophy, audience priority | verbatim |
| `43-owner-acts-elsewhere.md` | where else owner acts live (`sessions/`, `decisions/`…), located not copied | derived |

Not in the dossier because they are read directly: `CLAUDE.md` (Layer 0 rules and the five-layer ruling), `decisions/DR-2026-08-19-research-restart-operative-instrument.md`, `governance/pipeline-contract.yaml`, `governance/stage-map.yaml`, `governance/check-registry.yaml`, `scripts/` themselves, `data/guidebook.db` (open read-only).

Known limits of the collection, so no reader mistakes absence for fact:
- `stage-map.yaml` is JUDGED, not derived; it records one dispute (`gaps`).
- Code→stage attribution is by literal table names in source; dynamic SQL (f-strings building table names) is invisible to it.
- The `render` stage owns one table; its real surface is outside the database (`parts/`, `architecture/page-templates.md`, `scripts/generate/`). The dossier does not claim otherwise.
- The owner-prose index covers `references/project-standards.md` only; `sessions/` is located (43) but not copied.
