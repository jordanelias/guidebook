# Project Instructions — Accessible Built Environments Guidebook
**V10.14 · Revised 2026-05-20**
Supersedes V10.13. Architecture: `architecture/project-architecture-guidebook-v2.3.md`. Preferences: `userPreferences-v6.3.md`.

<changelog>
- **V10.14 (2026-05-20)** — Two changes, after which future bootstrap drift no longer requires PI bumps. (1) **Standing rule #11 sub-(a) explicit token placement**: `[DOCTRINE: <7-char-sha>]` placed BEFORE the trailing `[YYYY-MM-DD HH:MM]` timestamp because `scripts/ci_helpers/check_commit_msg.py` requires the timestamp as the LAST bracket on the line. Six governance commits in session 2026-05-19 silently failed the format check by placing the token after the timestamp. Canonical form: `{skill}: {action} [DOCTRINE: <sha>] [YYYY-MM-DD HH:MM]`. (2) **Bootstrap extracted to scripts/bootstrap.sh**: the inline bash block in the bootstrap section is replaced with a 6-line thin caller that pulls the script from the repo and pipes it to bash. The script derives the evidence_sources numerator from the DB at runtime (no more hardcoded /661 or /670 drift), reads the session-record section grep from a stable pattern matching the post-architecture-split format, and is editable via normal commits to main. Future bootstrap-content changes (status-block formatting, new state queries, mechanic updates) ship as ordinary commits without requiring a PI version bump or owner paste. Preferences pointer bumped to userPreferences-v6.3.md. No standing-rule semantic changes beyond rule #11(a) clarification; no skills_assigned changes.
- **V10.13 (2026-05-18)** — Standing rule #10 eligibility predicate amended per DR-2026-05-18 (statutory metadata completeness). Adds `COMPLETE-STATUTORY` as a peer value to `COMPLETE` for the existence gate, reflecting that statutory documents (standards, guidelines) carry issuing-body / edition-year / jurisdiction / standard-number fields that complete them without academic fields (DOI, PMID, named authors, journal, pagination). Both values clear the gate; they remain queryably distinct for audits. Minimal patch — no other rule changes, no `<skills_assigned>` changes, no bootstrap changes, no structural rename or removal. Closes the rule-vs-code drift surfaced in `decisions/PI-update-needed.md` (code in `scripts/audit_evidence_metadata.py` already updated; this PI text now ratifies that change).
- **V10.12 (2026-05-15)** — Bootstrap pattern bug fix. The status-block line `echo "Skills: $(grep -c '^### ' /tmp/registry.md) registered"` matched the registry's pre-v10.6 shape (per-skill `### ` headings) and returned 0 against the current registry, which uses `##` sections plus a code-block listing. Replaced with `_GH_SKILLS()` helper that counts `skills/*_SKILL.md` files via the GitHub contents API (excludes `skills/deprecated/`). Helper added to both gh and curl backend blocks. Label changed `registered` → `active` to reflect what is now counted. No standing-rule changes; no other content changes. Anomaly discovered and resolved in `sessions/session_2026-05-15a-governance-reconciliation.md`.
- **V10.12 amend (2026-05-17)** — Standing rule #11 added: adherence logging and attestation. Per `workplan/adherence-attestation-build-2026-05-17.md` §4.3 (Session 2). Bundles with the bootstrap fix under the v10.12 version label per workplan literal spec; version-hygiene note that v10.12 now contains two distinct content changes. Preferences pointer also bumped to `userPreferences-v6.2.md` (adds `<adherence_logging>` section).
- **V10.11 (2026-05-15)** — `reasoning-doc-citations` promoted from skill placeholder to active skill. Skill file `skills/reasoning-doc-citations_SKILL.md` authored; registered in `references/skill-registry.md`. Placeholder line removed from `<skills_assigned>`. No standing-rule changes; rule #10 sub-rules 2/3 unchanged.
- **V10.10 (2026-05-13)** — Conciseness pass per `<migration_and_growth>` of architecture v2.3 (PI growth target 200 lines). v10.9 was 307 lines; v10.10 is ~190. State content (current AUTHOR-TITLE-ONLY counts, retraction banners, session-specific commentary) moved to DR-2026-05-13 and the DB. Standing rules trimmed to rule-only — supporting detail lives in the cited DR or skill. `<hooks_status>` rewritten to reference the actual CI workflows that exist (`ci.yml`, `audit.yml`) instead of the phantom `hook-workplan-guidebook.md`. Architecture pointer corrected to v2.3 (was v2.3 in PI v10.9 already, but the file is now present in repo).
- **V10.9 (2026-05-13)** — Standing rule #10 sharpened per DR-2026-05-13 (adopted session_2026-05-13b). Distinguishes existence verification from claim verification by claim type. Migrations 010 (FK integrity) and 011 (`reasoning_doc_citations`) applied. user_version 9→11. Track 1 versioning backfill initiated. `reasoning-doc-citations` skill placeholder added.
- **V10.8 (2026-05-11)** — Standing rule #6 rewritten: adopts `audits/bpc-rewrite-workplan-2026-05-11.md` as the new operative plan; supersedes `workplan-co0007-v4.md`. Standing rules #9 (9-step synthesis rule) and #10 (evidence verification gate) added. Disability-centric framing locked.
- **V10.7 (2026-05-10)** — Standing rule #8 added: PMP protocol (per DR-2026-05-10). Migration 006 added `spec_value_probes` table.
- **V10.6 (2026-05-10)** — Standing rule #7 added: adversarial research protocol enforcement (per DR-2026-05-09).
- **V10.5 (2026-05-08)** — Standing rule #6 added (workplan named). SUPERSEDED by v10.8.
- **V10.3 (2026-05-07)** — Bootstrap rewritten with gh-or-curl backend; `canonical-sources.md` removed from reference files.
- **V10.2 and earlier** — Pre-architecture-split iterations.
</changelog>

<project_identity>
**Project:** Accessible Built Environments Guidebook — a reference document on architecture, accessibility, and built environment standards.
**Repo:** `jordanelias/guidebook` · branch `main`
**Surface:** claude.ai chat with Code Interpreter (per architecture v2.3 `<identity>`).
**PAT handling:** inline in the LIVE project-settings copy of this PI (claude.ai project knowledge). Redacted in the repo-side copy below per GitHub secret-scanning push protection.

`[REDACTED — see live PI in claude.ai project settings; PAT pattern: github_pat_11ACSEXD...]`
</project_identity>

<decisions>
Always make decisions and plans that serve the long-term health and integrity of the project.

**Disability-centric framing:** all references to "inclusive," "accessible," or "universal" in this project refer to inclusion of persons with disabilities. No universal-design-for-everyone framing. (Locked 2026-05-11 in session_2026-05-11h.)
</decisions>

<terminology>
- **DD** — Design Development
- **RFO** — Ready for Occupancy
- **BPC** — Best Practice Compendium (project's canonical reference set)
- **PMP** — Progressive Measurement Probe (per standing rule #8)
- **Lowest-barrier code** — synonymous with "most inclusive code" per BPC rewrite workplan §1: the jurisdiction-level regulatory standard that imposes the lowest barrier to access for the most-constrained user in the parameter's target population, evaluated at the worst-case point in the code's structure.
- **9-step rule** — locked operational rule for cross-jurisdictional synthesis per standing rule #9.
</terminology>

<reference_files>
Per architecture v2.3 `<reference_files_pattern>`. Bootstrap loads `project-standards.md` and `skill-registry.md`. Others are read on demand. Missing files are logged `[GAP: <filename> — not present]` and the session proceeds without them.

Active reference files:
- `references/project-standards.md` — required, bootstrap-loaded
- `references/skill-registry.md` — required, bootstrap-loaded; source of truth for skill assignments
- `references/effort-guide.md` — read on demand; default `medium` if skill not listed
- `references/bpc-reasoning/<slug>.md` — per-BPC reasoning documents (Phase E.1)
- `references/connection-reasoning/<con-id>.md` — per-connection reasoning documents (Phase D)
- `references/keyword-compendiums/<lang>.md` — per-language native-vocabulary compendiums (Phase A.11)
</reference_files>

<skills_assigned>
Skill assignments are governed by `references/skill-registry.md`. Skills that PI itself invokes by name:

- `workplan-orchestrator` — runs at session start; selects workflow
- `session-consolidator` — runs at session close per `<session_close>` below
- `research-log-manager` — per standing rule #4 (`CHECK` before research, `LOG` after)
- `toc-editor` — per standing rule #3 for structural changes
- `adversarial-research` — per standing rule #7 for any gap closure involving research
- `progressive-measurement` — per standing rule #8 for any BPC item asserting a numerical specification value
- `reasoning-doc-citations` — per standing rule #10 sub-rules 2/3 for jurisdiction-comparison cells, qualitative claims, and definitional claims in BPC reasoning documents
- `multilingual-research` — per standing rule #9 for cross-jurisdictional synthesis work
- `citation-miner` — per BPC rewrite workplan Phase B.11

**Skill placeholders** (named here but no skill file yet, per architecture v2.3 `<skill_registry_pattern>`):
- `bpc-curator`, `gap-register`, `bpc-writer`, `opus-synthesis` — informational hooks; current work uses scripts (`scripts/validate_bpc.py`) or ad-hoc Opus session work guided by workplan §1 / §2.

Per-skill effort overrides: `references/effort-guide.md`. Default: `medium` (per preferences).
</skills_assigned>

<hooks_status>
Per architecture v2.3 `<enforcement_spectrum>`. The earlier `hook-workplan-guidebook.md` referenced in v10.5–v10.9 was superseded by actual CI infrastructure; treat the workflow files themselves as the spec.

**Live enforcement (level 4, blocking on push/PR):**
- `.github/workflows/ci.yml` — 6 jobs: syntax, structure (BPC + cross-refs + thresholds), commit-msg format, schema validation, db_integrity (35 checks), governance (A10/A12/A13).
- `.github/workflows/audit.yml` — 3 blocking checks: source_slug_links duplicates, citation-mining completeness, migration reproducibility (GAP-290).

**Level 2 (audit scripts, manual or scheduled):**
- `scripts/audit/pmp_audit.py` — rule #8 + rule #10 sub-rule 1
- `scripts/audit/reasoning_doc_citations_audit.py` — rule #10 sub-rules 2/3
- `scripts/audit/research_protocol_audit.py` — rule #7
- `scripts/audit_evidence_metadata.py` — rule #10 existence gate

**Level 5 (pre-commit hooks, local):** none installed; deferred per architecture `<scope_assumptions>`.
</hooks_status>

<override_clauses>
This project does not currently override any user preferences.

To add an override later:
> Override `<preference-tag>` for scope `<scope>`: `<new-rule>`. Reason: `<why>`.
</override_clauses>

<standing_rules>
Project-specific rules. Preference-level rules (tone, logging, output format, etc.) are not restated here — they live in `userPreferences-v6.1.md`.

1. **Source discipline.** Sources confirmed real. "I don't know" > invention. 2 failed searches → mark `CLOSED-DELETED`.

2. **Best-practice synthesis routing.** Sonnet does NOT write `best_practice_synthesis` — only Opus. Sonnet produces evidence inventories, reasoning-document drafts, and per-population logging; Sonnet queues for Opus synthesis per BPC rewrite workplan Phase E.2f. Existing BPCs with `opus_synthesis: false` carry a reduced-confidence warning.

3. **Structural changes.** Anything affecting document structure (TOC, item codes, part/section nomenclature, cross-references) → invoke `toc-editor` skill first. Change Order required before structural commits.

4. **Research log discipline.** `research-log-manager CHECK` before any slug-keyed research; `LOG` after. Project-meta research (e.g., methodology surveys for DRs) is logged inline in the session record.

5. **Connector posture.** Connectors (PubMed, Consensus, Scholar Gateway) only when task explicitly requires research and web sources are insufficient. Default off (per preferences `<mcp_connectors>`).

6. **Canonical workplan.** Operative plan: `audits/bpc-rewrite-workplan-2026-05-11.md` (ADOPTED 2026-05-11 in session_2026-05-11h-bpc-rewrite-workplan-design, commit ce266114ef97). All work maps to its seven phases A–G. `workplan/workplan-co0007-v4.md` is SUPERSEDED — its Stage A/B foundation work (~43 sessions) remains valid; only the content-stage scoping is replaced.

   Phase ordering is STRICT SEQUENTIAL B before E. No BPC may be rewritten until its formally-linked sources have completed Phase B verification (`metadata_quality ≥ COMPLETE`; `verification_status ∈ {VERIFIED, UNVERIFIED-1}`). Phases A and D may run in parallel with B per workplan Appendix B.

   Load workplan §0 (Executive summary) and §Appendix D (Decisions log) before any content task.

7. **Adversarial research protocol.** Per DR-2026-05-09. All research-generating gap closures must populate four fields before status changes to CLOSED-FIXED or CLOSED-RESOLVED: `gaps.confidence_interval`, `gaps.shift_conditions`, `gaps.named_dissenter`, `gaps.falsification_condition`. Per cited study, log to `evidence_population_match` with grade (EXACT/PARTIAL/PROXY/MISMATCH) and `ref_id` FK.

   Anti-pattern to watch: conflating "evidence on the topic" with "evidence supporting the specific claim".

   Skill: `skills/adversarial-research_SKILL.md`. Audit: `scripts/audit/research_protocol_audit.py`. Spot-check ≥1 closed gap per session.

8. **Progressive measurement probe (PMP).** Per DR-2026-05-10. Any BPC item asserting a numerical specification value (mm, s, NC, lux, °C, %, N, LRV, dB(A), NRC, etc.) must run the PMP walk before the spec is treated as evidence-grounded. PMP runs AFTER `adversarial-research` clears the underlying claim.

   Algorithm: 1c hybrid (proportional 20% outer phase; linear δ_min refinement) + 2bc strict termination (peer-reviewed source validates value for target population AND alt-phrasing search corroborates). Required DB writes per walk: rows in `spec_value_probes`; `evidence_sources` + `source_slug_links` + `evidence_population_match` per cited study; `items.pmp_*` columns updated on the `final` row.

   Anti-pattern (same as #7): topic-evidence ≠ claim-evidence.

   Skill: `skills/progressive-measurement_SKILL.md`. Audit: `scripts/audit/pmp_audit.py`. Spot-check ≥1 walk per session.

9. **Cross-jurisdictional synthesis — 9-step rule.** Per BPC rewrite workplan §1 (locked). For each parameter where ≥3 jurisdictions specify different values, every BPC reasoning document must apply the 9-step rule:

   1. Parameter declaration (name, units, accessibility direction)
   2. Per-population worst-case user (no inline cross-population arbitration)
   3. Jurisdiction comparison table (every surveyed jurisdiction's value at worst-case point; `scope` column)
   4. Lowest-barrier code(s) per population
   5. Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence (Tier 4 international / Tier 5 national-recommended excluded at this step)
   6. Guidebook chosen value per population
   7. Rationale (historical context + clinical basis)
   8. Trade-offs
   9. Cross-population conflict flag → queue for arbitration BPC

   Multilingual coverage required: 19 languages × 46 jurisdictions per `multilingual-research_SKILL.md`. AR/HI/ID/SW/BN flagged `[UNVERIFIED-TERMS]` until keyword compendiums validated per workplan Phase A.11.

   Validator: `scripts/validate_reasoning.py` (level 2).

10. **Evidence verification gate for synthesis.** Per DR-2026-05-13, amended per DR-2026-05-18. No BPC synthesis claim may cite a source with `metadata_quality = AUTHOR-TITLE-ONLY` or `verification_status = NULL`. Required minimum: `metadata_quality ∈ {COMPLETE, COMPLETE-STATUTORY}` AND `verification_status ∈ {VERIFIED, UNVERIFIED-1}`. The `COMPLETE-STATUTORY` value (introduced 2026-05-18 per DR-2026-05-18) certifies that a statutory document (standard, guideline) carries the metadata fields appropriate to its source type — issuing body, edition year, jurisdiction, and standard number or publisher — rather than the academic-publication fields (DOI, journal, page range, named authors) the unqualified `COMPLETE` requires. Both values clear the existence gate; they remain queryably distinct for audit purposes. Sources with `verification_status ∈ {UNVERIFIED-CLOSED, CLOSED-DELETED}` excluded.

    **`VERIFIED` confirms source existence, not content.** Additional content-verification by claim type:

    1. **Numerical-spec claims**: must additionally cite a `spec_value_probes` walk passing strict termination (rule #8), or logged `pmp_waiver`.
    2. **Jurisdiction-comparison cells (rule #9 step 3)**: must have a `reasoning_doc_citations` row with `value_match ∈ {EXACT, WITHIN-TOLERANCE}` from a re-read of the cited section. `PAYWALL` requires downgrade or non-paywalled corroboration.
    3. **Qualitative and definitional claims**: must have a `reasoning_doc_citations` row with `claim_match ∈ {SUPPORTED, PARTIAL}`. `CONTRADICTED` invalidates the claim.

    **Track 3 pilot mandate.** First BPC entering Phase E.1 under the `reasoning_doc_citations` workflow runs as a formal pilot with inline review before scaling. Cochrane gold-standard dual-reviewer is structurally unavailable to a single-reviewer project; pilot is the partial mitigation.

    BPCs bearing `opus_synthesis: YES [OPUS-SYNTHESIS]` from the 2026-03-30 round carry a `synthesis_validity: PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION` banner until Phase E.2g overwrites. Live state counts queryable via bootstrap status block; not restated in PI.

    Audits: `scripts/audit_evidence_metadata.py` (existence gate); `scripts/audit/pmp_audit.py` (sub-rule 1); `scripts/audit/reasoning_doc_citations_audit.py` (sub-rules 2/3).

11. **Adherence logging and attestation.** Per `userPreferences-v6.2.md` `<adherence_logging>`. At every `<audit_trail>` stage boundary, emit `[ADHERENCE-LOG]` per the defined structure.

    Commits modifying `references/bpc-reasoning/`, `references/connection-reasoning/`, `decisions/`, or synthesis-bearing files under `sessions/` MUST:
    (a) Include `[DOCTRINE: <7-char-sha>]` in the commit message, where the SHA matches `HEAD:governance/mission-and-epistemics.md`. The token MUST be placed BEFORE the trailing `[YYYY-MM-DD HH:MM]` timestamp because `scripts/ci_helpers/check_commit_msg.py` requires the timestamp as the LAST bracket on the line. Canonical form: `{skill}: {action} [DOCTRINE: <sha>] [YYYY-MM-DD HH:MM]`. Exempt when the commit itself modifies `governance/mission-and-epistemics.md`; in that case, affected downstream artifacts must be re-attested within RE_ATTESTATION_WINDOW (default 5) commits or by next session close, whichever first.
    (b) Add or update `attestations/<artifact-slug>.json` validating against `schemas/attestation.schema.json`. Backfill-on-touch: existing artifacts grandfather; first edit creates the attestation.

    CI enforcement:
    - `ci.yml` `commit-msg` job — doctrine-SHA token validation (Level 4 blocking from day one).
    - `audit.yml` `attestation_schema` — JSON schema validation (Level 4 blocking).
    - `audit.yml` `attestation_evidence` — cross-reference rule-status to commit content (Level 2 → 4 after 7-day shakedown meeting the gate in workplan §8).
    - `audit.yml` `attestation_verdict` — NON-COMPLIANT count surfaced as PR comment / commit annotation; never blocking.

    Audit script: `scripts/audit/adherence_log_audit.py` (Level 2). Skipping adherence logging while authoring synthesis content is a methodology-grade failure on the same severity as skipping rule #7 (adversarial-research) or rule #8 (PMP).
</standing_rules>

<bootstrap>
Run at session start, before project-specific work. PI declares the trigger; bootstrap mechanics live in `scripts/bootstrap.sh` in the repo and update via ordinary commits per architecture v2.3 `<bootstrap_pattern>` extraction guidance.

```bash
#!/usr/bin/env bash
# Guidebook bootstrap thin caller — PI v10.14. Loads scripts/bootstrap.sh from main.
set -uo pipefail
PAT=$(sed -E 's/^`//; s/`$//' /mnt/project/GitHub_pat | tr -d '\n')
export PAT REPO="jordanelias/guidebook"
curl -fsSL -H "Authorization: Bearer $PAT" \
  "https://raw.githubusercontent.com/${REPO}/main/scripts/bootstrap.sh" | bash
```

**Bootstrap-exempt** (proceed without bootstrap):
- Review/fix of these instructions, preferences, or architecture spec themselves
- Pure tooling questions not touching repo state
- Workflow conversation that does not touch repo content

If unsure, bootstrap.
</bootstrap>

<session_close>
Trigger at ~85% context or natural conclusion. Do not start a new stage.

1. Complete current stage.
2. Commit pending work using commit convention below.
3. Invoke `session-consolidator` skill.
4. Produce bullet-point handoff: docs touched, where stopped, next action, blockers.
</session_close>

<commit_convention>
Format: `{skill-name}: {action} [{YYYY-MM-DD HH:MM}]`

Timestamp via `date -u`. Skill-name lowercase, hyphenated. Action concise, imperative. For governance work (PI revisions, architecture revisions, skill-registry builds) where no specific skill applies, use `governance` as the skill-name.

Examples:
- `toc-editor: add accessibility section to chapter 4 [2026-05-07 14:30]`
- `governance: adopt DR-2026-05-13 evidence verification methodology [2026-05-13 02:15]`

CI workflow `commit-msg` (per `.github/workflows/ci.yml`) enforces this on push.
</commit_convention>
