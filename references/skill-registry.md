# Skill Registry — Guidebook
**Refreshed:** 2026-05-13 (session_2026-05-13b; full reconciliation pass)
**Source:** auto-derived from `skills/` directory listing and PI `<skills_assigned>`
**Active skills:** 44 · **Deprecated:** 12 · **PI placeholders (named, no file):** 5

This file is the source of truth for skill assignments. PI `<skills_assigned>` points here. Architecture v2.3 `<reference_files_pattern>` and `<skill_registry_pattern>` define what belongs in this file.

---

## Conventions

- **Active** — skill file present in `skills/` and not flagged deprecated.
- **Deprecated** — skill file in `skills/deprecated/`. Do not invoke; superseded or retired.
- **PI placeholder** — skill name appears in PI `<skills_assigned>` but no skill file exists; reserved for future authoring or informational hook.

Each active skill's effort level is in `references/effort-guide.md`. Triggers and protocols live in the skill file itself.

---

## PI-invoked skills (per PI v10.10 `<skills_assigned>`)

| Skill | File | Status | Invoked by PI rule |
|---|---|---|---|
| workplan-orchestrator | `skills/workplan-orchestrator_SKILL.md` | active | session start |
| session-consolidator | `skills/session-consolidator_SKILL.md` | active | `<session_close>` |
| research-log-manager | `skills/research-log-manager_SKILL.md` | active | rule #4 |
| toc-editor | `skills/toc-editor_SKILL.md` | active | rule #3 |
| adversarial-research | `skills/adversarial-research_SKILL.md` | active | rule #7 |
| progressive-measurement | `skills/progressive-measurement_SKILL.md` | active | rule #8 |
| multilingual-research | `skills/multilingual-research_SKILL.md` | active | rule #9 |
| citation-miner | `skills/citation-miner_SKILL.md` | active | BPC workplan Phase B.11 |
| reasoning-doc-citations | — | **placeholder** | rule #10 sub-rules 2/3 (DR-2026-05-13); file to be authored |

---

## All active skills

Listed alphabetically. Effort levels in `references/effort-guide.md`.

```
adversarial-research              cross-reference-resolver         literature-review-planner        research-log-manager
audit-consolidator                doctrine-recheck                 markdown-formatter               sensory-coherence-checker
bibliography-compiler             economics-auditor                multilingual-research            session-consolidator
cell-curator                      economics-researcher             practice-note-generator          structure-auditor
citation-miner                    evidence-auditor                 progressive-measurement          supplemental-integrator
citation-verifier                 find-and-replace                 prose-style-checker              table-formatter
connection-auditor                functional-deficit-auditor       question-author                  toc-editor
connection-discovery              functional-deficit-researcher    relational-integrity-checker     version-diff
content-gap-analyzer              github-filing                                                     voice-style
critique-report-writer            github-io                                                         workplan-orchestrator
cross-population-conflict-mapper  guidebook-auditor
                                  item-audit-pipeline
                                  item-consolidation-analyzer
                                  item-specification-writer
                                  jurisdiction-tracker
```

44 active skills. Use the skill file at `skills/<name>_SKILL.md` for trigger conditions and protocols.

---

## Deprecated skills

In `skills/deprecated/`. Listed for archaeological reference; do not invoke.

| Skill | Reason / supersession |
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

## Skills named in PI but with no file (placeholders)

| Name | Purpose | Action |
|---|---|---|
| `reasoning-doc-citations` | Track 3 of DR-2026-05-13; per-cell verification during Phase E.1 | Author in Phase A parallel-track |
| `bpc-curator` | Informational only; current work via `scripts/validate_bpc.py` + Opus sessions | Stays placeholder |
| `gap-register` | Informational only; gaps live in `gaps` table accessed via `scripts/db.py` | Stays placeholder |
| `bpc-writer` | Informational only; BPC synthesis is ad-hoc Opus work per workplan §1/§2 | Stays placeholder |
| `opus-synthesis` | Informational only; synonym for `bpc-writer` | Stays placeholder |

---

## Skills referenced by other governance docs

The orchestrator's skill index (embedded in `skills/workplan-orchestrator_SKILL.md` §Skill Index) classifies skills by execution shape: `prose_only` / `hybrid` / `python_tool` / `infrastructure` / `deprecated` / `unclassified`. The orchestrator taxonomy was last refreshed before 2026-05-08 and contains drift relative to the current `skills/` state:

- The orchestrator classifies `toc-editor` as `deprecated`. Per PI v10.10 rule #3, `toc-editor` is **active** and required for structural changes. The skill file is maintained. Next orchestrator-taxonomy refresh should remove the deprecated tag.
- The orchestrator's "Skills classified but missing from repo" list (`bulk-renumber`, `chunk-assembler`, `evidence-marker`, `file-splitter`, `fix-linebreaks`, `haiku-chunker`, `vol2-item-formatter`, `volii-validator`) — all of these are now in `skills/deprecated/` rather than absent. Update the orchestrator's expectation.
- The orchestrator does not yet classify the 11 newer skills: `adversarial-research`, `audit-consolidator`, `cell-curator`, `doctrine-recheck`, `economics-auditor`, `functional-deficit-auditor`, `item-audit-pipeline`, `progressive-measurement`, `question-author`, `relational-integrity-checker`, `version-diff`. Next orchestrator-taxonomy refresh should add these.

---

## Refresh history

- **2026-05-13** (session_2026-05-13b) — full refresh after audit. Body restructured. Active count confirmed at 44; deprecated at 12; PI placeholders enumerated. Architecture pointer updated from v2.2 (never committed) → v2.3.
- **2026-05-10** — `progressive-measurement` skill added per DR-2026-05-10.
- **2026-05-08** — initial registry built (per session_2026-05-08-c1-migration-fix); referenced "Architecture v2.2" (never committed).
