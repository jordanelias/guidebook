# Skill Registry — Guidebook

This file is the source of truth for skill assignments. PI `<skills_assigned>` points here. Conventions and the placeholder pattern are defined in `architecture/project-architecture-guidebook-v*.md` `<skill_registry_pattern>`.

---

## Identifier stability

Skill identifiers in this registry are STABLE. They are the canonical
strings referenced from `attestations/*.json` files (per PI v10.12 rule #11)
and from rule cross-references throughout the project.

Renaming a skill identifier is a governance event that requires:
1. A DR documenting the rename rationale and migration plan.
2. A timestamped data-migration script at
   `scripts/migrations/data_<YYYYMMDDHHMMSS>_rename-skill-<old>-to-<new>.sql`
   (or `.py`) that rewrites every existing `attestations/*.json` file
   to use the new identifier.
3. Lockstep update of any skill files, audit-script rule maps, and
   PI standing rules referencing the old name.

The audit script `scripts/audit/adherence_log_audit.py` check #3 validates
that every rule identifier in an attestation resolves to a stable identifier
listed in this registry **or** to the `EXTRA_RULE_IDS` set in that audit script.

`EXTRA_RULE_IDS` is the second, non-skill vocabulary of valid `rules_in_scope`
values — cross-cutting rule identifiers that name a PI standing rule or doctrine
commitment rather than an invocable skill (e.g. `adherence-logging-and-attestation`
= rule #11; `best-practice-synthesis-routing` = mission doctrine #2), plus a few
documented historical aliases of registered skills. It is the ratified extension
point for such identifiers (per
`decisions/DR-2026-07-13-attestation-rule-identifier-registry-gap.md`, RATIFIED
2026-07-21) and is distinct from the skill-rename governance process above: that
process governs renaming a skill going forward; `EXTRA_RULE_IDS` accepts a non-skill
or historical-alias identifier without rewriting past attestations.

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
citation-verifier                 evidence-metadata-rehabilitation prose-style-checker              table-formatter
connection-auditor                find-and-replace                 question-author                  toc-editor
connection-discovery              functional-deficit-auditor       reasoning-doc-citations          version-diff
content-gap-analyzer              functional-deficit-researcher    relational-integrity-checker     voice-style
critique-report-writer            gap-driven-mining                                                 workplan-orchestrator
cross-population-conflict-mapper  github-filing
                                  github-io
                                  guidebook-auditor
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
