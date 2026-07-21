# Project Instructions — Accessible Built Environments Guidebook
**V10.8 · Revised 2026-05-11**
Supersedes V10.7. Architecture: `project-architecture-guidebook-v2.3.md`. Preferences: `userPreferences-v6.1.md`.

<changelog>
- **V10.8 (2026-05-11)** — Standing rule #6 rewritten: adopts `audits/bpc-rewrite-workplan-2026-05-11.md` (ce266114ef97) as the new operative plan; supersedes `workplan-co0007-v4.md`. Standing rules #9 (9-step synthesis rule) and #10 (evidence verification gate) added. Reference files extended to include `references/bpc-reasoning/`, `references/connection-reasoning/`, `references/keyword-compendiums/`. Bootstrap status block extended with Phase B progress and reasoning-doc coverage. Adopted per user decision 2026-05-11 in session_2026-05-11h-bpc-rewrite-workplan-design. Disability-centric framing locked: "inclusive," "accessible," "universal" all refer to inclusion of persons with disabilities.
- **V10.7 (2026-05-10)** — Standing rule #8 added: progressive measurement probe (PMP) protocol for numerical-spec items (per DR-2026-05-10). `progressive-measurement` added to PI-invoked skills. Migration 006 applied to tracking DB (schema_version 5→6, adds `spec_value_probes` table + `items.pmp_*` columns + `v_pmp_latest_walk` view). PMP partially reverses DR-2026-05-09 §"What Was Dropped" — the dropped "±20% threshold test" is reinstated under a corrected iterative re-centering design.
- **V10.6 (2026-05-10)** — Standing rule #7 added: adversarial research protocol enforcement (per DR-2026-05-09). Schema applied to tracking DB. Pattern documented: "topic-evidence vs claim-evidence" conflation must be detected during gap closure review.
- **V10.5 (2026-05-08)** — Standing rule #6 added: names `workplan-co0007-v4.md` as the only operative plan. SUPERSEDED by v10.8.
- **V10.3 (2026-05-07)** — D.1: bootstrap rewritten with gh-or-curl backend; step 4 replaced (gap_register.md is archived → query SQLite at `data/guidebook.db`); broken regex (`^\| (OPEN|P1)`) removed. D.3: `references/canonical-sources.md` removed from declared reference files.
- **V10.2 (prior)** — Original.
</changelog>

<project_identity>
**Project:** Accessible Built Environments Guidebook — a reference document on architecture, accessibility, and built environment standards.
**Repo:** `jordanelias/guidebook` · branch `main`
**Surface:** claude.ai chat with Code Interpreter (per architecture v2.3).
**PAT handling:** inline in the LIVE project-settings copy of this PI (claude.ai project knowledge). Redacted in the repo-side copy below per GitHub secret-scanning push protection. Source of truth is the live copy in project settings.

`[REDACTED — see live PI in claude.ai project settings; PAT pattern: github_pat_11ACSEXD...]`

If repo scope expands or another collaborator joins, migrate PAT to file-based pattern.
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
Expected in `references/` directory of repo. Bootstrap loads each. If any are missing, log `[GAP: <filename> — not present]` and proceed without it.

- `project-standards.md` — domain conventions, citation style, voice rules, structural rules
- `effort-guide.md` — per-skill effort table; default `medium` if not listed
- `skill-registry.md` — index of all skills with status, classification, model, triggers, dependencies, and reconciliation drift flags. **Source of truth for skill assignments.** Built 2026-05-08 (commit ee24387).

**New directories per BPC rewrite workplan (created in Phase A):**
- `bpc-reasoning/<slug>.md` — per-BPC reasoning documents per workplan §2 template (Phase A.7).
- `connection-reasoning/<con-id>.md` — per-connection reasoning documents per workplan §3 template (Phase A.8).
- `keyword-compendiums/<lang>.md` — per-language native-vocabulary compendiums for AR/HI/ID/SW/BN per workplan §A.11.
</reference_files>

<skills_assigned>
**Skill assignments are governed by `references/skill-registry.md`.** That file lists all *_SKILL.md files currently in `skills/`, classified per `workplan-orchestrator_SKILL.md` taxonomy (prose_only, hybrid, python_tool, infrastructure, deprecated, unclassified).

**Skills that PI itself invokes by name** (these get governance attention here even when registry detail changes):

- `workplan-orchestrator` — runs at session start to load core state and select workflow. Always invoked.
- `session-consolidator` — runs at session close per `<session_close>` below.
- `research-log-manager` — invoked per standing rule #4 (`CHECK` before research, `LOG` after).
- `toc-editor` — invoked per standing rule #3 for structural changes. `[ASSUMPTION: classified "deprecated" by workplan-orchestrator skill index, but no replacement has shipped and `references/toc.md` + `references/change-orders/` are still actively maintained by it. Treat as active until either (a) a replacement skill ships and is invoked here, or (b) toc-editor's body is updated to delegate to a Python tool.]`
- `adversarial-research` — invoked per standing rule #7 for any gap closure involving research.
- `progressive-measurement` — invoked per standing rule #8 for any BPC item asserting a numerical specification value.
- `multilingual-research` — invoked per standing rule #9 for cross-jurisdictional synthesis work (19 langs × 46 jurisdictions per skill protocol).
- `citation-miner` — invoked per BPC rewrite workplan Phase B.11 for every BPC with ≥1 source. Closes GAP-283 (P1).

**Skill names that have NO corresponding skill file (informational):**
- `bpc-curator` — never had a skill file; current BPC maintenance is via `scripts/validate_bpc.py` plus ad-hoc Claude work.
- `gap-register` — never had a skill file; gaps live in SQLite (`gaps` table) accessed via `scripts/db.py`.
- `bpc-writer` / `opus-synthesis` — no skill file exists for BPC synthesis. Per BPC rewrite workplan, synthesis remains ad-hoc Opus session work guided by workplan §1 (9-step rule) and §2 (reasoning-document template). A `bpc-writer` skill may be authored in a future phase but is not yet specified.

Per-skill effort overrides: `references/effort-guide.md`. Default if not listed: `medium` (per preferences).
</skills_assigned>

<hooks_status>
**Currently zero hooks live.** All rules below are level-1 enforcement (text only) until Phase 1 ships.

Workplan: `hook-workplan-guidebook.md`. Phase 1 hooks (commit-format, filename-convention, frontmatter-schema, citation-format, link-validity) target ~4 days of work. Phase 2 deferred until Phase 1 has a clean calibration window.

**v10.8 note:** BPC rewrite workplan Phase A.9 adds `scripts/validate_reasoning.py` — a level-2 validator for the new reasoning-document format. Promotion to enforced hook status follows Phase 1 calibration.

Architecture spec §"Enforcement spectrum" applies — do not promote rules to "enforced" status until the corresponding hook exists and tests pass.
</hooks_status>

<override_clauses>
This project does not currently override any user preferences.

To add an override later:
> Override `<preference-tag>` for scope `<scope>`: `<new-rule>`. Reason: `<why>`.
</override_clauses>

---

<standing_rules>
Project-specific rules. Apply throughout every session. Preference-level rules (tone, logging, output, etc.) are not restated here — they live in `userPreferences-v6.1.md`.

1. **Source discipline.** Sources confirmed real. "I don't know" > invention. 2 failed searches → mark `CLOSED-DELETED`. Specific to this project's evidence-heavy nature.

2. **Best-practice synthesis routing.** Sonnet does NOT write `best_practice_synthesis` — only Opus. Sonnet produces evidence inventories, reasoning-document drafts, and per-population logging; Sonnet queues for Opus synthesis per BPC rewrite workplan §Phase E.2f. Existing BPCs with `opus_synthesis: false` carry a reduced-confidence warning. (Modified v10.8 to integrate with workplan Phase E pipeline.)

3. **Structural changes.** Anything affecting document structure (TOC, item codes, part/section nomenclature, cross-references) → invoke `toc-editor` skill first. Change Order required before structural commits.

4. **Research log discipline.** `research-log-manager CHECK` before any research; `LOG` after. Skipping = error.

5. **Connector posture.** Connectors (PubMed, Consensus, Scholar Gateway) only when task explicitly requires research. Default off (per preferences `<mcp_connectors>`).

6. **Canonical workplan.** The operative plan is `audits/bpc-rewrite-workplan-2026-05-11.md` (ADOPTED 2026-05-11 in session_2026-05-11h-bpc-rewrite-workplan-design, commit ce266114ef97). All work maps to its seven phases: A (Foundation), B (Evidence rehabilitation), C (Coverage axis expansion to 19×46), D (Connection rehabilitation), E (Per-BPC rewrite), F (Items pipeline), G (Output regeneration).

   `workplan/workplan-co0007-v4.md` is **SUPERSEDED** by this workplan. Its Stage C1–C11 content work is replaced by the BPC rewrite workplan's Phase E. Stage A/B foundation work in co0007-v4 (~43 sessions consumed) remains validly completed and is not invalidated — only the content-stage scoping is replaced.

   **Phase ordering is STRICT SEQUENTIAL B before E.** No BPC may be rewritten until its formally-linked sources have completed Phase B verification (metadata_quality ≥ COMPLETE; verification_status ∈ {VERIFIED, UNVERIFIED-1}). Phases A and D may run in parallel with B for their independent tasks per workplan §Appendix B.

   **Aggregate effort:** ~2300 hours (~55 weeks sustained full-time; ~2.3 years session-based).

   Load workplan §0 Executive summary and §Appendix D Decisions log before any content task.

7. **Adversarial research protocol.** All research-generating gap closures must populate four protocol fields before status changes to CLOSED-FIXED or CLOSED-RESOLVED:
   - `gaps.confidence_interval` (numerical range, e.g., "60-75%")
   - `gaps.shift_conditions` (specific conditions that would shift CI up/down)
   - `gaps.named_dissenter` (specific contrary view OR "NONE FOUND" with logged search queries)
   - `gaps.falsification_condition` (specific finding that would invalidate)

   Per cited study, log to `evidence_population_match` with grade (EXACT/PARTIAL/PROXY/MISMATCH) and `ref_id` foreign key.

   Critical pattern to watch: conflating "evidence on the topic" with "evidence supporting the specific claim". A real citation about a domain does not validate every specific claim in that domain.

   Audit query: `scripts/audit/research_protocol_audit.py` (level 2 enforcement). Skill: `skills/adversarial-research_SKILL.md`. Decision record: `decisions/DR-2026-05-09-adversarial-research-protocol.md`.

   Spot-check at minimum 1 closed gap per session: trace cited evidence to specific claim, verify match.

8. **Progressive measurement probe (PMP).** Any BPC item asserting a numerical specification value (mm, s, NC, lux, °C, %, N, LRV, dB(A), NRC, etc.) must run the PMP walk before the spec is treated as evidence-grounded. PMP is invoked AFTER `adversarial-research` clears the underlying claim; it probes the value within that claim.

   Algorithm (1c hybrid + 2bc strict termination):
   - Outer phase: walk in accessibility-direction D by ±20% per step. Re-center at each supported step.
   - Refinement phase: linear δ_min step, bisect toward boundary, until distance ≤ δ_min.
   - A step "passes" only if at least one peer-reviewed source specifically validates the test value for the target population AND a second alt-phrasing search corroborates.

   Required DB writes per walk: rows in `spec_value_probes` (append-only); `evidence_sources` + `source_slug_links` + `evidence_population_match` per cited study; `items.pmp_empirical_ceiling`, `items.pmp_gap_signed`, `items.pmp_last_walk_at` updated on the `final` row.

   Critical guard (same anti-pattern as #7): topic-evidence does NOT count as claim-evidence. Per step, ask "does this evidence specifically validate THIS value, or does it speak to the topic?"

   Audit query: `scripts/audit/pmp_audit.py` (level 2 enforcement). Skill: `skills/progressive-measurement_SKILL.md`. Decision record: `decisions/DR-2026-05-10-progressive-measurement-protocol.md`.

   Spot-check at minimum 1 walk per session.

9. **Cross-jurisdictional synthesis — 9-step rule.** For each parameter where ≥3 jurisdictions specify different values, every BPC reasoning document must apply the locked 9-step rule (see `audits/bpc-rewrite-workplan-2026-05-11.md` §1):

   1. **Parameter declaration** — name, units, accessibility direction (LOWER / HIGHER / POPULATION-DEPENDENT).
   2. **Per-population worst-case user** — list every affected population; for each, name the most-constrained user. **Do NOT arbitrate cross-population conflicts inline** — log per-population separately.
   3. **Jurisdiction comparison table** — every surveyed jurisdiction's value evaluated at its code's worst-case point. Comparison-only purpose. Includes `scope` column ∈ {statutory-code / national-framework / international-standard / national-recommended / provincial-local}.
   4. **Lowest-barrier code(s) per population** — jurisdiction-evaluated worst-case value closest to access direction.
   5. **Tier 1 / Co-1 / Tier 2 / Co-2 / Tier 3 evidence cited** — sources supporting or exceeding the lowest-barrier code. **Tier 4 (international standards) and Tier 5 (national frameworks) excluded at this step** — they belong to the jurisdiction comparison in step 3.
   6. **Guidebook chosen value per population** — may match or exceed the lowest-barrier code.
   7. **Rationale** — historical context of permissive codes; clinical basis for chosen value.
   8. **Trade-offs** — cost, retrofit feasibility, named cross-population conflicts.
   9. **Cross-population conflict flag** — if multiple populations have different chosen values, queue for `cross-population-conflict-resolutions` BPC arbitration.

   Reasoning documents that do not apply all 9 steps to a parameter are incomplete and fail `scripts/validate_reasoning.py` (Phase A.9).

   Multilingual coverage required: 19 languages × 46 jurisdictions per `multilingual-research_SKILL.md`. AR/HI/ID/SW/BN flagged `[UNVERIFIED-TERMS]` until keyword compendiums validated per workplan Phase A.11.

10. **Evidence verification gate for synthesis.** No BPC synthesis claim may cite a source with `metadata_quality = AUTHOR-TITLE-ONLY` or `verification_status = NULL`. Required minimum: `metadata_quality = COMPLETE` AND `verification_status ∈ {VERIFIED, UNVERIFIED-1}`. Sources with `verification_status ∈ {UNVERIFIED-CLOSED, CLOSED-DELETED}` are excluded from all synthesis.

    Current state at v10.8 adoption (per audit in session_2026-05-11h):
    - 567/661 sources are AUTHOR-TITLE-ONLY (86%) — INELIGIBLE for synthesis
    - 647/661 sources have `verification_status = NULL` (98%) — INELIGIBLE for synthesis
    - 14/661 sources VERIFIED (2%)

    Phase B of the operative workplan rehabilitates these sources. Until Phase B is complete for a given BPC's formally-linked sources, that BPC's rewrite (Phase E) is BLOCKED.

    All BPCs currently bearing `opus_synthesis: YES [OPUS-SYNTHESIS]` from the 2026-03-30 round (~30 BPCs) carry a `synthesis_validity: PRE-REHABILITATION — RETRACTED PENDING REVERIFICATION` banner per workplan §Phase B.0. The banner remains until Phase E.2g overwrites the synthesis sections with rehabilitated evidence. Downstream consumers must not cite the retracted syntheses.

    Audit query: `scripts/audit_evidence_metadata.py` (to be written in Phase A.10, level 2 enforcement).
</standing_rules>

<bootstrap>
Run at session start, before project-specific work. This is the only procedural content allowed in PI per architecture v2.3 §"Bootstrap exception."

```bash
#!/usr/bin/env bash
# Guidebook bootstrap — PI v10.8. Idempotent. Halt on critical, log [GAP] on non-critical.
set -uo pipefail
PAT="REDACTED_IN_REPO_COPY_SEE_PROJECT_SETTINGS"  # actual value in claude.ai project knowledge
REPO="jordanelias/guidebook"
echo "Session start: loading Guidebook context"

# Backend: gh if available, else curl.
if command -v gh >/dev/null 2>&1; then
  echo "$PAT" | gh auth login --with-token 2>/dev/null || true
  _GET()     { gh api "repos/$REPO/contents/$1" --jq .content 2>/dev/null | base64 -d >"$2" 2>/dev/null; [ -s "$2" ]; }
  _GET_BIN() { gh api "repos/$REPO/contents/$1" -H "Accept: application/vnd.github.raw" >"$2" 2>/dev/null; [ -s "$2" ]; }
else
  echo "[ASSUMPTION: gh CLI unavailable — using curl]"
  AUTH="Authorization: Bearer $PAT"
  _GET()     { curl -fsSL -H "$AUTH" "https://api.github.com/repos/$REPO/contents/$1" 2>/dev/null \
                 | python3 -c "import sys,json,base64;sys.stdout.buffer.write(base64.b64decode(json.load(sys.stdin)['content']))" >"$2" 2>/dev/null; [ -s "$2" ]; }
  _GET_BIN() { curl -fsSL -H "$AUTH" -H "Accept: application/vnd.github.raw" "https://api.github.com/repos/$REPO/contents/$1" -o "$2" 2>/dev/null; [ -s "$2" ]; }
fi

# Critical fetches
_GET "sessions/LATEST" /tmp/latest.txt                || { echo "HALT: sessions/LATEST"; exit 1; }
SESSION=$(tr -d '\n\r ' </tmp/latest.txt)
_GET "sessions/$SESSION" /tmp/session.md               || { echo "HALT: sessions/$SESSION"; exit 1; }
_GET "references/project-standards.md" /tmp/standards.md || { echo "HALT: project-standards.md"; exit 1; }
_GET "references/skill-registry.md" /tmp/registry.md     || { echo "HALT: skill-registry.md"; exit 1; }
_GET "audits/bpc-rewrite-workplan-2026-05-11.md" /tmp/workplan.md || { echo "HALT: bpc-rewrite-workplan"; exit 1; }

# State queries — SQLite
P1="?"; PMP_BACKLOG="?"; ATT_ONLY="?"; UNVERIFIED="?"; REASONING_BPC="?"; REASONING_CON="?"
if _GET_BIN "data/guidebook.db" /tmp/guidebook.db; then
  P1=$(python3 -c "import sqlite3;print(sqlite3.connect('/tmp/guidebook.db').execute(\"SELECT COUNT(*) FROM gaps WHERE priority='P1' AND status NOT LIKE 'CLOSED%'\").fetchone()[0])" 2>/dev/null) || P1="?"
  PMP_BACKLOG=$(python3 -c "import sqlite3;print(sqlite3.connect('/tmp/guidebook.db').execute(\"SELECT COUNT(DISTINCT i.item_code) FROM items i WHERE i.pmp_last_walk_at IS NULL AND i.status NOT IN ('archived','superseded')\").fetchone()[0])" 2>/dev/null) || PMP_BACKLOG="?"
  ATT_ONLY=$(python3 -c "import sqlite3;print(sqlite3.connect('/tmp/guidebook.db').execute(\"SELECT COUNT(*) FROM evidence_sources WHERE metadata_quality='AUTHOR-TITLE-ONLY'\").fetchone()[0])" 2>/dev/null) || ATT_ONLY="?"
  UNVERIFIED=$(python3 -c "import sqlite3;print(sqlite3.connect('/tmp/guidebook.db').execute(\"SELECT COUNT(*) FROM evidence_sources WHERE verification_status IS NULL OR verification_status=''\").fetchone()[0])" 2>/dev/null) || UNVERIFIED="?"
else
  echo "[GAP: data/guidebook.db — not fetched]"
fi

# Reasoning-doc coverage (new in v10.8)
REASONING_BPC=$(gh api "repos/$REPO/contents/references/bpc-reasoning" --jq 'length' 2>/dev/null || echo 0)
REASONING_CON=$(gh api "repos/$REPO/contents/references/connection-reasoning" --jq 'length' 2>/dev/null || echo 0)

# Status block
echo "=== STATUS ==="
echo "session: $SESSION"
grep -E "session_close|next_action|blockers" /tmp/session.md
echo "P1 OPEN: $P1"
echo "PMP backlog: $PMP_BACKLOG"
echo "Evidence AUTHOR-TITLE-ONLY: $ATT_ONLY / 661  (ineligible for synthesis per rule #10)"
echo "Evidence verification_status NULL: $UNVERIFIED / 661"
echo "BPC reasoning docs: $REASONING_BPC / 95  (Phase E target)"
echo "Connection reasoning docs: $REASONING_CON / 245  (Phase D target)"
echo "Skills: $(grep -c '^### ' /tmp/registry.md) registered"
echo "Workplan: bpc-rewrite-workplan-2026-05-11 (LIVE) | superseded: workplan-co0007-v4"
```

If a critical fetch fails: report error verbatim, halt, do not substitute memory.

**Bootstrap-exempt** (proceed without bootstrap):
- Review/fix of these instructions, preferences, or architecture spec themselves
- Pure tooling questions not touching repo state
- Workflow conversation that does not touch repo content

If unsure, bootstrap.

**v10.8 update notes:**
- New critical fetch: `audits/bpc-rewrite-workplan-2026-05-11.md` (operative plan per standing rule #6).
- Status block extended with evidence-base health metrics (AUTHOR-TITLE-ONLY count, verification_status NULL count).
- Status block extended with reasoning-doc coverage (Phase E / Phase D progress indicators).
- v10.8 inherits v10.7 PMP bootstrap query.
- Tested: not yet (v10.8 freshly authored). First session under v10.8 should validate bootstrap timing and SQLite query correctness.
</bootstrap>

<session_close>
Trigger at ~85% context or natural conclusion. Do not start a new stage.

1. Complete current stage.
2. Commit pending work using commit convention (below).
3. Invoke `session-consolidator` skill.
4. Produce bullet-point handoff: docs touched, where stopped, next action, blockers.
</session_close>

<commit_convention>
Format: `{skill-name}: {action} [{YYYY-MM-DD HH:MM}]`

Timestamp via `date -u`. Skill-name lowercase, hyphenated. Action concise, imperative.

Example: `toc-editor: add accessibility section to chapter 4 [2026-05-07 14:30]`

For governance work (PI revisions, architecture revisions, skill-registry builds) where no specific skill applies, use `governance` as the skill-name.

Example: `governance: build skill-registry.md (D.2) [2026-05-08 00:01]`

Phase 1 hook `commit-format` (see `hook-workplan-guidebook.md`) will enforce this once shipped.
</commit_convention>
