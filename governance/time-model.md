# Time Model
**Status:** CANONICAL — A9 Session 1
**Phase:** Stage A Phase 9 — Time model
**Created:** 2026-04-30 01:43 UTC
**Doctrinal basis:** Standing Rule 2 (`YYYY-MM-DD HH:MM` via `date -u`) · project-standards Core Doctrine (active version V9.0 2026-03-20) · A5 §1 (pre-launch operational reality, 2026-04-26) · A6 §1.1 (seven-tier evidence hierarchy) · A8 §3.1–3.2 (standards currency)

---

## 0. What this document governs and what it does not

This document covers temporal entities and relationships across the corpus: when something began applying, when it stopped applying, what superseded what, how stale evidence is allowed to be, and how date strings must be formatted. It does not govern git commit timestamps, CI run timestamps, or session operational timestamps that already round-trip through external systems. The boundary rule is simple: if the timestamp is a property of a guidebook entity (a rule, a standard, a source, a document version), it lives here; if the timestamp is a property of an external system (git, CI, the runtime clock), it does not.

The model has five axes, each addressed separately below: document version (§1), standards edition (§2), project-rule effective date (§3), source publication and verification (§4), launch phase (§5). Validators and converters that operationalise the model are specified in §6–§7.

---

## 1. Document version

### 1.1 Version tag format

A guidebook version tag has the shape `v{MAJOR}.{MINOR}` where MAJOR and MINOR are non-negative integers. Pre-launch the project uses tags v8.x and v9.x; the active tag at the time of this document is **v9.0** with effective date **2026-03-20**. The next prep version is v10.0 (in preparation under CO-0008 Stage A). Patch-level versioning (v9.0.1) is not used pre-launch — every version bump issues a new MAJOR.MINOR. Post-launch the policy may shift to MAJOR.MINOR.PATCH; that change requires a Change Order.

### 1.2 Filename convention

Released and prep document files live under `versions/{folder}/Guidebook_for_Accessible_Design_v{tag}_{YYYY-MM-DD}.md` where `{tag}` is the version tag without the leading `v` and with `.` replaced by `-` for filesystem friendliness (so `v9.0` → `v9-0`). The folder name is the bare version (e.g., `8.10`, `9.0`) or the literal `current` for the active document. Validator §6 enforces this pattern.

The 2026-03-20 active document is therefore `versions/current/Guidebook_for_Accessible_Design_v9-0_2026-03-20.md`. Its prep predecessor sits in `versions/8.10/Guidebook_for_Accessible_Design_v9-0-prep.md` — the prep file's name reflects what it was preparing toward, not its own version. Prep files are exempt from the `_{YYYY-MM-DD}` requirement because their effective date is undefined.

### 1.3 Bump policy

Pre-launch, MINOR bumps cover content additions, evidence updates, item additions, and any non-structural revision. MAJOR bumps cover structural changes that change Part numbering, item code prefixes, or the volume map. CO-0004 (volume merge, 13 → 12 Parts) was a MAJOR-class change executed during v9.x preparation; v10.0 will subsume the CO-0008 governance refactor as a MAJOR bump.

Post-launch policy is contingent on the launch model (§5) and is not specified in A9. The bump-policy table in §6.4 of the validator covers what is currently enforceable.

### 1.4 Supersedence

Each released version supersedes the prior released version at its effective date. The chain is recorded in `data/temporal/guidebook_versions/v{tag}.yaml` with a `supersedes:` field pointing to the prior tag. Cycles are forbidden; the validator (§6) checks acyclicity. The current version is whichever record has `status: ACTIVE`; exactly one record may carry `ACTIVE` at a time.

---

## 2. Standards edition

### 2.1 Relationship to A8 (jurisdiction philosophy)

A8 specified that `references/standards-registry.md` tracks the currency of all cited standards. A8's validator (`validate_jurisdiction.py`) checks the registry's structural integrity (required fields, valid status enum, date format, jurisdiction-code resolution). A9 does not re-do that work. A9 adds the supersedence relationship between editions of the same standard family — which the registry currently encodes implicitly via the `current_version` and `status` fields but does not expose as a typed link.

### 2.2 Standard family vs. edition

A *standard family* is the long-lived identifier (e.g., `AS 1428.1`, `DIN 18040-1`, `NEN 9120`). An *edition* is a specific dated release of that family (e.g., `AS 1428.1:2021`, `NEN 9120:2025`). The registry currently uses `standard_cited` as a free-text field that conflates the two; A9's converter (§7) splits them into `standard_family` and `edition` on the per-jurisdiction YAML output, leaving the source markdown registry unchanged for human readability.

### 2.3 Edition supersedence

When an edition supersedes a prior edition of the same family, the relationship is captured as a `SupersedenceLink` of `link_type: standard` (§4 of `schemas/temporal.py`). The link records the from-edition string, the to-edition string, the effective date of the supersession, and an optional rationale. Rationale is required when the supersession changes a value cited elsewhere in the guidebook (so the next edition pass knows which Part 4 specifications must be re-verified).

The standards-registry already records the textbook example: `NEN 1814:2001 → SUPERSEDED → NEN 9120:2025`. After retrofit (§7), this is also a typed link in `data/temporal/supersedence/`.

### 2.4 Transition periods

Some supersessions have transition periods during which both editions remain legally enforceable. The Sweden BFS 2024:12 / BBR transition (July 2025–June 2026) is the registry's worked example. The model handles this with `transition_until_date` on the SupersedenceLink — a date by which the prior edition is fully retired. During the transition, validator §6.5 emits a WARNING when guidebook prose cites the superseded edition without acknowledging the transition.

---

## 3. Project-rule effective date

### 3.1 Why project-standards needs a temporal model

`references/project-standards.md` accumulates RULE blocks over time. Each block carries a `DATE:` line in one of three formats: `YYYY-MM-DD HH:MM` (the standard), `YYYY-MM-DD` (older entries), or the literal string `Established — pre-session` (the oldest entries, predating the dated-rule convention). Rules supersede prior rules — sometimes explicitly ("supersedes the prior X rule"), sometimes implicitly (the new RULE replaces a now-removed older RULE on the same topic).

Without a temporal model, the rule history is opaque to mechanical analysis. A skill cannot ask "what was the rule on best-practice synthesis at 2026-03-25" or "which rules currently in effect are older than 90 days and should be reviewed". A9 adds the model; the converter (§7) extracts every RULE block and emits a YAML record per rule.

### 3.2 Rule record schema

A `ProjectRule` record carries:

| Field | Type | Required | Notes |
|---|---|---|---|
| `rule_id` | string | yes | Synthetic if not supplied — `RULE-{section_slug}-{seq}` |
| `rule_text` | string | yes | The full RULE: body |
| `condition` | string | optional | The CONDITION: line if present |
| `action` | string | optional | The ACTION: line if present |
| `effective_date` | string | yes | `YYYY-MM-DD HH:MM`, `YYYY-MM-DD`, or `pre-session` |
| `effective_date_normalized` | string | yes | Always `YYYY-MM-DD HH:MM` (pre-session normalises to `2026-03-15 00:00`, the convention floor date) |
| `section` | string | yes | The H2/H3 heading the rule sits under |
| `supersedes` | list[str] | optional | rule_ids superseded by this rule |
| `superseded_by` | string | optional | rule_id that supersedes this rule (back-reference) |
| `status` | enum | yes | `ACTIVE` (default), `SUPERSEDED`, `RETIRED` |

### 3.3 Supersedence detection

The converter detects supersedence in three ways. First, explicit textual cues — phrases like "supersedes", "replaces", "retires" followed by a description — are extracted as candidate links. Second, when a section is rewritten and an earlier rule on the same topic is no longer present in the file, the absent rule is marked `RETIRED` (not `SUPERSEDED`, because no successor rule was named). Third, manual annotation — a `SUPERSEDES:` line on a RULE block — is honoured as authoritative and overrides automatic detection.

The textual-cue detection is best-effort. Where ambiguous, the converter emits a warning and the link is stored with `status: PROVISIONAL` for human review. The validator does not treat PROVISIONAL links as errors.

### 3.4 Pre-session anchor

Rules dated `Established — pre-session` are normalised to effective date `2026-03-15 00:00` for ordering purposes only. This date is a convention, not a claim — it represents "the project was already running before structured date-stamping began". It must not be displayed to users or readers as the rule's authentic effective date; the unmodified `effective_date` field carries the original string. Mixing the two fields in displays is a validator-warned error.

---

## 4. Source publication and verification

### 4.1 Publication date

`EvidenceSource.year` (A6 schema) is currently `Optional[str]`. A9 does not break that field. It adds two optional companion fields: `publication_month` (1–12) and `publication_date_iso` (YYYY-MM-DD where known). The string `year` remains the canonical input field; the structured fields are populated when the converter can resolve them. Validator §6.7 flags inconsistency (e.g., year=2024 but publication_date_iso=2025-01-15).

### 4.2 Last-verified date

A new optional field `last_verified` (`YYYY-MM-DD HH:MM`) on EvidenceSource records when the source was most recently checked for accuracy. Validator §6.8 flags Tier 1–3 sources without a `last_verified` value, but does not error — the field is being populated incrementally.

### 4.3 Freshness windows

Per evidence tier, there is a guidance window after which a source should be re-verified:

| Tier | Evidence type | Window | Rationale |
|---|---|---|---|
| 1 | Clinical research | 7 years | Clinical evidence ages slowly but practice protocols update; 7 years aligns with typical Cochrane review refresh cycle |
| 1 | Co-1 | 5 years | Lived-experience research is more time-bound to social/legal context |
| 2 | NGO/DPO guidelines | 5 years | Guideline currency depends on issuing organization; 5y is a default |
| 2 | Co-2 (OT CPGs) | 5–7 years | Most OT bodies refresh CPGs on 5–7 year cycles |
| 3 | SR/meta-analyses | 5 years | Literature accumulates; SR coverage decays |
| 4 | International standards | edition-driven | Re-verify at edition release, not on a clock |
| 5 | National frameworks | edition-driven | Same as Tier 4 |
| 6 | Codes | edition-driven | Same |

These are guidance, not gates. A 10-year-old Tier 1 study with no contradicting newer evidence is still citable; the validator emits a WARNING (not ERROR) when the window is exceeded. The window applies from `last_verified` if present, otherwise from `year`.

### 4.4 Source supersedence

When a newer source supersedes an older one (e.g., a follow-up trial with longer follow-up; an updated systematic review), this is captured as a `SupersedenceLink` of `link_type: source`. The model accepts but does not require this; most sources are not formally superseded.

---

## 5. Launch phase

### 5.1 Three phases

The guidebook itself has a launch state machine. Per A5 RULE 2026-04-26 03:45, the project is currently **pre-launch**, defined by: solo authorship, no DPO collaborator infrastructure, Co-1 evidence engaged through the published corpus only, no resources for participatory synthesis. Two further phases are anticipated:

| Phase | Marker | Operational implications |
|---|---|---|
| `pre_launch` | current | Solo authorship; co1_provenance=published_corpus only; CS2 INOPERATIVE |
| `launched` | initial public release | Public access to V{N}.0; collaborator infrastructure may activate if resources allow |
| `maintained` | ongoing edition cycle | Versioned releases on a cadence; participatory synthesis may engage |

The transition from `pre_launch` to `launched` is gated on three triggers, all of which must be true: (1) the launch event itself; (2) resources to support the post-launch posture; (3) a co-designed recruitment specification per A5 §6 if Co-1 collaboration is to engage. None of the three is currently met.

### 5.2 Phase as a temporal entity

A `LaunchPhaseRecord` captures the current phase and any prior phase transitions. The record is a singleton — one record per repository — and is updated only when a phase transition occurs. The current record states `phase: pre_launch, since: 2026-04-26 03:45`. Validator §6.9 ensures exactly one record exists.

### 5.3 Effect on validation

Several A6/A8 rules behave differently across phases. The clearest case: `co1_provenance` validators currently require `published_corpus` for all Co-1 sources because the project is pre-launch (A5 §6.1). After launch, `participatory_synthesis` becomes valid. The launch-phase record drives this — validators read the singleton to determine which value set to accept. Pre-launch hard-codes published_corpus only.

---

## 6. Validator specification (`scripts/validate_temporal.py`)

### 6.1 Scope

The validator scans temporal entities across the corpus and checks them against the model. It runs in CI alongside the A6, A7, A8 validators. It does not duplicate checks already performed by other validators (date format on standards-registry is already in `validate_jurisdiction.py` and is not re-run here).

### 6.2 Check matrix

| ID | Check | Severity | Source |
|---|---|---|---|
| T-01 | Date string format | ERROR | All `data/temporal/*` YAML; all RULE DATE: lines |
| T-02 | No future dates | ERROR | Effective dates and last_verified |
| T-03 | Supersedence cycles | ERROR | All SupersedenceLink records |
| T-04 | Supersedence orphans (target missing) | ERROR | All SupersedenceLink records |
| T-05 | Version filename pattern | ERROR | `versions/**/*.md` |
| T-06 | Exactly one ACTIVE GuidebookVersion | ERROR | data/temporal/guidebook_versions/ |
| T-07 | Year/publication_date_iso consistency | WARNING | EvidenceSource records |
| T-08 | Tier 1–3 last_verified missing | WARNING | EvidenceSource records |
| T-09 | Exactly one LaunchPhaseRecord | ERROR | data/temporal/launch_phase.yaml |
| T-10 | Transition-period citation flag | WARNING | Markdown prose (best-effort) |
| T-11 | Freshness window exceeded | WARNING | EvidenceSource records |
| T-12 | Pre-session normalisation correctness | ERROR | ProjectRule records |

### 6.3 Date format

The accepted formats are `YYYY-MM-DD HH:MM` (canonical), `YYYY-MM-DD` (date-only — accepted on legacy entries, not on new), and the literal `pre-session` (only on ProjectRule.effective_date). Anything else is T-01 ERROR. The validator does not parse natural-language dates.

### 6.4 No-future check

A future date is one that exceeds `datetime.utcnow()` at the time the validator runs. The validator allows a 24-hour grace period for clock skew. Effective dates set deliberately in the future (e.g., a rule published with delayed effect) are not currently a use case; if needed, an explicit `--allow-future` flag can be added later.

### 6.5 Supersedence checks

For every SupersedenceLink, the validator confirms (a) the `from_id` resolves to an existing record of the matching link type, (b) the `to_id` resolves to an existing record of the matching link type, (c) the chain is acyclic (no record can supersede itself, transitively or otherwise). Implementation: build a directed graph of links per link_type; run cycle detection per type.

### 6.6 Version filename pattern

The regex is `^Guidebook_for_Accessible_Design_v\d+-\d+(_\d{4}-\d{2}-\d{2})?\.md$`. Files ending in `-prep.md` are accepted as prep files and exempt from the date suffix.

### 6.7–6.9

Specified inline in the table above. Implementation patterns follow A8's validator (`validate_jurisdiction.py`) — argparse, exit codes 0/1/2, errors-vs-warnings tuple return per check function.

---

## 7. Converter specification (`scripts/convert/version_retrofit.py`)

### 7.1 Scope

The retrofit reads existing markdown sources and emits per-entity YAML records under `data/temporal/`. It is idempotent — running it twice produces identical output. It does not modify any markdown source; the markdown remains the human-readable canonical form.

### 7.2 Inputs and outputs

| Input | Output directory | Records produced |
|---|---|---|
| `references/project-standards.md` | `data/temporal/rules/` | One per RULE block, named `RULE-{section_slug}-{seq}.yaml` |
| `references/standards-registry.md` | `data/temporal/standards/` | One per registry entry, named `{jurisdiction}_{family_slug}_{edition_slug}.yaml` |
| `versions/` | `data/temporal/guidebook_versions/` | One per version directory, named `v{tag}.yaml` |
| `sessions/session_*.md` | `data/temporal/sessions/` | One per session file, name matches source |
| (computed) | `data/temporal/supersedence/` | One per detected supersedence link |
| (singleton) | `data/temporal/launch_phase.yaml` | The launch-phase record |

### 7.3 Rule extraction

The parser walks `project-standards.md` line by line. State machine: idle → in_rule (after seeing `RULE:`) → in_condition (after `CONDITION:`) → in_action (after `ACTION:`) → resolved (after `DATE:`). The rule body accumulates across lines until the next marker is encountered. On `DATE:`, the record is finalised and emitted.

The current section is tracked via H2/H3 headings. Rule IDs are synthesised as `RULE-{section_slug}-{seq}` where `{seq}` is a per-section incrementing counter. Where a `RULE:` block has no `CONDITION:` or `ACTION:`, those fields are omitted from the output.

### 7.4 Standards extraction

Re-uses the YAML-block parser from A8's converter. Each block produces one record; the family and edition strings are split heuristically — the family is the part before the first colon or `(`, the edition is the full `current_version` string. Heuristic failure produces a record with `family: null` and a warning emitted to stderr.

### 7.5 Version directory walk

Each subdirectory under `versions/` other than `current` produces one record with `status: ARCHIVED`. The contents of `versions/current/` produces a record with `status: ACTIVE`. If the active document filename does not match the version pattern, the record is emitted with `effective_date: null` and a warning is logged.

### 7.6 Supersedence detection

Three sources of supersedence links: (1) the standards registry's SUPERSEDED entries — every such entry produces a link; (2) explicit "supersedes" / "replaces" phrases in rule body text — these produce PROVISIONAL links pending review; (3) the manual `SUPERSEDES:` annotation on rule blocks (currently not used; the field is reserved for future authoring).

### 7.7 Idempotency and dry-run

Two flags: `--dry-run` reports what would be written without touching disk; `--diff` writes to a sibling directory `data/temporal_new/` for comparison. The default mode overwrites; this is safe because the converter is a pure function of the markdown sources.

---

## 8. Status

| Field | Value |
|---|---|
| Created | 2026-04-30 01:43 UTC |
| Phase | Stage A Phase 9 (Time model) — Session 1 |
| Status | CANONICAL |
| Forward dependencies | `validate_temporal.py`, `version_retrofit.py` (this session); A13 doctrine-recheck |
| Supersedes | None — first temporal-model document |
| Schema dependencies | `schemas/temporal.py` (new), `schemas/enums.py` (extended) |

---

**End of A9 governance document.**
