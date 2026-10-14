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

### Renames performed

| Former identifier | Current identifier | Date | Record |
|---|---|---|---|
| `cell-curator` | `specification-curator` | 2026-08-12 | `decisions/DR-2026-08-12-specification-curator-rename.md` |

*Note (2026-09-10): `specification-curator` — the "Current identifier" above — was itself deleted
this date (`skills/specification-curator_SKILL.md`, item-layer skill, subject retired by the
2026-09-01 owner ruling). This row is a historical record of the 2026-08-12 rename event, not a
pointer to a live skill; it stays, and is not rewritten, for the same reason the row below it
gives. `cell-curator`'s resolution via `EXTRA_RULE_IDS` for historical attestations is unaffected
by the later deletion.*

**Past attestations citing a former identifier are NOT rewritten.** Step 2 of the process above
calls for a migration that rewrites every `attestations/*.json`; that step is deliberately not taken
here, and the departure is recorded in the DR. Rewriting a committed adherence log to say a session
invoked a name that did not exist on its date would falsify the record — the same class of act as
editing a dated audit. The former identifier is instead registered in `EXTRA_RULE_IDS`
(`scripts/audit/adherence_log_audit.py`, Category B), which the file above already describes as the
ratified way to accept a historical identifier **without rewriting past attestations**. Check #3
therefore still resolves every existing citation.

---

## Conventions

- **Active** — skill file present in `skills/`.
- **PI placeholder** — skill name appears in PI `<skills_assigned>` but no skill file exists; reserved for future authoring or informational hook.

Triggers and protocols live in the skill file itself.

---

## All active skills

```
adversarial-research              cross-reference-resolver          gap-driven-mining                 research-log-manager
bibliography-compiler             doctrine-recheck                  github-io                         session-consolidator
citation-miner                    economics-researcher              integrity-protocol                supersession-audit
citation-verifier                 evidence-auditor                  jurisdiction-tracker              toc-editor
connection-discovery              evidence-metadata-rehabilitation  multilingual-research             voice-style
content-gap-analyzer              find-and-replace                  prose-style-checker               workplan-orchestrator
cross-population-conflict-mapper  functional-deficit-researcher
```

## Retired rule identifiers

Names that were skills and are still cited as rule identifiers by committed attestations. The attestations are append-only records and are not edited, so `scripts/audit/adherence_log_audit.py` reads this block together with the one above (RULINGS R45). Do not invoke these; no skill file exists.

```
audit-consolidator
connection-auditor
guidebook-auditor
relational-integrity-checker
structure-auditor
```

Use the skill file at `skills/<name>_SKILL.md` for trigger conditions and protocols.

---

## PI placeholders (named, no skill file)

| Name | Purpose |
|---|---|
| `bpc-curator` | Informational; BPC maintenance is ad-hoc Opus session work (`scripts/validate_bpc.py` was deleted in plan step 1.6) |
| `gap-register` | Informational; gaps live in the `gaps` table, accessed via `scripts/db.py` |
| `bpc-writer` | Informational; BPC synthesis is ad-hoc Opus session work |
| `opus-synthesis` | Informational; synonym for `bpc-writer` |
