# Skill Registry — Guidebook

This file is the source of truth for skill assignments. PI `<skills_assigned>` points here. Conventions and the placeholder pattern are defined in `architecture/project-architecture-guidebook-v*.md` `<skill_registry_pattern>`.

---

## Conventions

- **Active** — skill file present in `skills/` and not flagged deprecated.
- **Deprecated** — skill file in `skills/deprecated/`. Do not invoke; superseded or retired.
- **PI placeholder** — skill name appears in PI `<skills_assigned>` but no skill file exists; reserved for future authoring or informational hook.

Each active skill's effort level is in `references/effort-guide.md`. Triggers and protocols live in the skill file itself.

---

## All active skills

```
adversarial-research              cross-reference-resolver         literature-review-planner        research-log-manager
audit-consolidator                doctrine-recheck                 markdown-formatter               sensory-coherence-checker
bibliography-compiler             economics-auditor                multilingual-research            session-consolidator
cell-curator                      economics-researcher             practice-note-generator          structure-auditor
citation-miner                    evidence-auditor                 progressive-measurement          supplemental-integrator
citation-verifier                 find-and-replace                 prose-style-checker              table-formatter
connection-auditor                functional-deficit-auditor       question-author                  toc-editor
connection-discovery              functional-deficit-researcher    reasoning-doc-citations          version-diff
content-gap-analyzer              github-filing                    relational-integrity-checker     voice-style
critique-report-writer            github-io                                                         workplan-orchestrator
cross-population-conflict-mapper  guidebook-auditor
                                  item-audit-pipeline
                                  item-consolidation-analyzer
                                  item-specification-writer
                                  jurisdiction-tracker
```

Use the skill file at `skills/<name>_SKILL.md` for trigger conditions and protocols.

---

## Deprecated skills

In `skills/deprecated/`. Listed for archaeological reference; do not invoke.

| Skill | Supersession / reason |
|---|---|
| bibliography-updater | Superseded by `bibliography-compiler` + `citation-miner` pipeline |
| bulk-renumber | One-time migration tool; retired |
| chunk-assembler | Pre-DB era; SQLite assembly handles this |
| connection-scout | Superseded by `connection-discovery` |
| evidence-marker | Pre-DB era; tier marks now live in `evidence_sources.tier` column |
| file-splitter | One-time migration tool |
| fix-linebreaks | One-time conversion tool |
| haiku-chunker | Model-specific pre-Sonnet helper; retired |
| keyword-lookup | Superseded by `multilingual-research` keyword compendiums |
| neufert-image-analyzer | Image-extraction tool; retired |
| vol2-item-formatter | Pre-DB era formatter |
| volii-validator | Pre-DB era validator; superseded by `validate_bpc.py` |

---

## PI placeholders (named, no skill file)

| Name | Purpose |
|---|---|
| `bpc-curator` | Informational; current BPC maintenance is via `scripts/validate_bpc.py` and ad-hoc Opus sessions |
| `gap-register` | Informational; gaps live in the `gaps` table, accessed via `scripts/db.py` |
| `bpc-writer` | Informational; BPC synthesis is ad-hoc Opus session work |
| `opus-synthesis` | Informational; synonym for `bpc-writer` |
