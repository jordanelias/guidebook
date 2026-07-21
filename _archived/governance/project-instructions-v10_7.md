# Project Instructions — Accessible Built Environments Guidebook
**V10.7 · Revised 2026-05-10**
Supersedes V10.6. Architecture: `project-architecture-guidebook-v2.3.md`. Preferences: `userPreferences-v6.1.md`.

<changelog>
- **V10.7 (2026-05-10)** — Standing rule #8 added: progressive measurement probe (PMP) protocol for numerical-spec items (per DR-2026-05-10). `progressive-measurement` added to PI-invoked skills. Migration 006 applied to tracking DB (schema_version 5→6, adds `spec_value_probes` table + `items.pmp_*` columns + `v_pmp_latest_walk` view). PMP partially reverses DR-2026-05-09 §"What Was Dropped" — the dropped "±20% threshold test" is reinstated under a corrected iterative re-centering design.
- **V10.6 (2026-05-10)** — Standing rule #7 added: adversarial research protocol enforcement (per DR-2026-05-09). Schema applied to tracking DB. Pattern documented: "topic-evidence vs claim-evidence" conflation must be detected during gap closure review.
- **V10.5 (2026-05-08)** — Standing rule #6 added: names `workplan-co0007-v4.md` as the only operative plan. Prevents Claude from following superseded workplans (website-preparation.md Block sequencing, roadmap-2026-04-27, workplan v3). Architecture reference unchanged (v2.3).
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
</decisions>

<terminology>
- **DD** — Design Development
- **RFO** — Ready for Occupancy
- **BPC** — Best Practice Compendium (project's canonical reference set)
- **PMP** — Progressive Measurement Probe (per standing rule #8)
</terminology>

<reference_files>
Expected in `references/` directory of repo. Bootstrap loads each. If any are missing, log `[GAP: <filename> — not present]` and proceed without it.

- `project-standards.md` — domain conventions, citation style, voice rules, structural rules
- `effort-guide.md` — per-skill effort table; default `medium` if not listed
- `skill-registry.md` — index of all skills with status, classification, model, triggers, dependencies, and reconciliation drift flags. **Source of truth for skill assignments.** Built 2026-05-08 (commit ee24387).
</reference_files>

<skills_assigned>
**Skill assignments are governed by `references/skill-registry.md`.** That file lists all *_SKILL.md files currently in `skills/`, classified per `workplan-orchestrator_SKILL.md` taxonomy (prose_only, hybrid, python_tool, infrastructure, deprecated, unclassified).

**Skills that PI itself invokes by name** (these get governance attention here even when registry detail changes):

- `workplan-orchestrator` — runs at session start to load core state and select workflow. Always invoked.
- `session-consolidator` — runs at session close per `<session_close>` below.
- `research-log-manager` — invoked per standing rule #4 (`CHECK` before research, `LOG` after).
- `toc-editor` — invoked per standing rule #3 for structural changes. `[ASSUMPTION: workplan-orchestrator's Skill Index classifies toc-editor as "deprecated", but no replacement has shipped and `references/toc.md` + `references/change-orders/` are still actively maintained by it. Treat as active until either (a) a replacement skill ships and is invoked here, or (b) toc-editor's body is updated to delegate to a Python tool. Tracked in skill-registry §reconciliation drift.]`
- `adversarial-research` — invoked per standing rule #7 for any gap closure involving research. Documents topic-vs-claim bias pattern with worked examples.
- `progressive-measurement` — invoked per standing rule #8 for any BPC item asserting a numerical specification value. Companion to `adversarial-research`: where adversarial-research validates the claim, PMP probes the empirical range of the value within that claim. Decision record: `decisions/DR-2026-05-10-progressive-measurement-protocol.md`.

**Two skill names that appeared in PI v10.3 §skills_assigned have been removed in v10.4:**
- `bpc-curator` — never had a skill file; current BPC maintenance is via `scripts/validate_bpc.py` plus ad-hoc Claude work, not a skill.
- `gap-register` — never had a skill file; gaps live in SQLite (`gaps` table) accessed via `scripts/db.py`.

Per-skill effort overrides: `references/effort-guide.md`. Default if not listed: `medium` (per preferences).
</skills_assigned>

<hooks_status>
**Currently zero hooks live.** All rules below are level-1 enforcement (text only) until Phase 1 ships.

Workplan: `hook-workplan-guidebook.md`. Phase 1 hooks (commit-format, filename-convention, frontmatter-schema, citation-format, link-validity) target ~4 days of work. Phase 2 deferred until Phase 1 has a clean calibration window.

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

2. **Best-practice synthesis.** BPC entries with `opus_synthesis: false` carry a reduced-confidence warning. Sonnet does not synthesize new best practices — only Opus. Guidance, not enforced; relies on upstream model selection (Claude cannot self-verify model identity per `<model_identity>` in preferences).

3. **Structural changes.** Anything affecting document structure (TOC, item codes, part/section nomenclature, cross-references) → invoke `toc-editor` skill first. Change Order required before structural commits. (See §skills_assigned for the deprecation-classification note on toc-editor — current invocation remains active.)

4. **Research log discipline.** `research-log-manager CHECK` before any research; `LOG` after. Skipping = error.

5. **Connector posture.** Connectors (PubMed, Consensus, Scholar Gateway) only when task explicitly requires research. Default off (per preferences `<mcp_connectors>`).

6. **Canonical workplan.** The operative plan is `workplan/workplan-co0007-v4.md` (ADOPTED 2026-05-03). All content work maps to v4 Stage C sub-stages (C1–C11). No other workplan governs session planning. Load v4 §Current position before any content task. Other workplan files are either deprecated (with explicit banners), tactical references subordinate to v4 (e.g. `website-preparation.md` for BPC migration pipeline detail), or proposed extensions pending adoption (e.g. `workplan-item-audit-pipeline-co0009.md`). See `workplan/workplan-reconciliation-2026-05-08.md` for the full supersession map.

7. **Adversarial research protocol.** All research-generating gap closures must populate four protocol fields before status changes to CLOSED-FIXED or CLOSED-RESOLVED:
   - `gaps.confidence_interval` (numerical range, e.g., "60-75%")
   - `gaps.shift_conditions` (specific conditions that would shift CI up/down)
   - `gaps.named_dissenter` (specific contrary view OR "NONE FOUND" with logged search queries)
   - `gaps.falsification_condition` (specific finding that would invalidate)

   Per cited study, log to `evidence_population_match` with grade (EXACT/PARTIAL/PROXY/MISMATCH) and `ref_id` foreign key.

   Critical pattern to watch: conflating "evidence on the topic" with "evidence supporting the specific claim". A real citation about a domain does not validate every specific claim in that domain. The protocol exists to expose this bias.

   Audit query: `scripts/audit/research_protocol_audit.py` (level 2 enforcement). Skill: `skills/adversarial-research_SKILL.md`. Decision record: `decisions/DR-2026-05-09-adversarial-research-protocol.md`.

   The reviewer is the truth-source — the protocol creates audit trails, not truth. Spot-check at minimum 1 closed gap per session: trace cited evidence to specific claim, verify match.

8. **Progressive measurement probe (PMP).** Any BPC item asserting a numerical specification value (mm, s, NC, lux, °C, %, N, LRV, dB(A), NRC, etc.) must run the PMP walk before the spec is treated as evidence-grounded. PMP is invoked AFTER `adversarial-research` clears the underlying claim; it probes the value within that claim.

   Algorithm (1c hybrid + 2bc strict termination):
   - Outer phase: walk in accessibility-direction D by ±20% per step. Re-center at each supported step.
   - Refinement phase: linear δ_min step, bisect toward boundary, until distance ≤ δ_min.
   - A step "passes" only if at least one peer-reviewed source specifically validates the test value for the target population AND a second alt-phrasing search corroborates (two failed independent searches confirm "no evidence").

   Required DB writes per walk: rows in `spec_value_probes` (one per step, append-only); `evidence_sources` + `source_slug_links` + `evidence_population_match` per cited study; `items.pmp_empirical_ceiling`, `items.pmp_gap_signed`, `items.pmp_last_walk_at` updated on the `final` row.

   Critical guard (same anti-pattern as #7): topic-evidence does NOT count as claim-evidence. Per step, ask "does this evidence specifically validate THIS value, or does it speak to the topic?" If only the latter, `passes_strict = 0` regardless of search-result count.

   Multilingual scope: one walk per item, EN by default. Target-language walks added only when adversarial-research surfaced cited values diverging from V₀ in that language's literature, OR the domain has a known non-EN-dominant research base.

   Audit query: `scripts/audit/pmp_audit.py` (level 2 enforcement; flags items lacking walks, ungrounded passes, suspect ceilings). Skill: `skills/progressive-measurement_SKILL.md`. Workplan: `workplan/progressive-measurement-protocol.md`. Decision record: `decisions/DR-2026-05-10-progressive-measurement-protocol.md`. Schema: migration `006_spec_value_probes.sql` (schema_version 6).

   Spot-check at minimum 1 walk per session: trace one step-pass row to its primary data, and re-run the alt-phrasing search with deliberately different terms — see if a value declared unsupported has support.
</standing_rules>

<bootstrap>
Run at session start, before project-specific work. This is the only procedural content allowed in PI per architecture v2.3 §"Bootstrap exception."

```bash
#!/usr/bin/env bash
# Guidebook bootstrap — PI v10.7. Idempotent. Halt on critical, log [GAP] on non-critical.
set -uo pipefail
PAT="REDACTED_IN_REPO_COPY_SEE_PROJECT_SETTINGS"  # actual value in claude.ai project knowledge
REPO="jordanelias/guidebook"
echo "Session start: loading Guidebook context"

# Backend: gh if available, else curl. _GET <path> <out>; _GET_BIN for binary.
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

# Critical fetches — halt on failure
_GET "sessions/LATEST" /tmp/latest.txt              || { echo "HALT: sessions/LATEST"; exit 1; }
SESSION=$(tr -d '\n\r ' </tmp/latest.txt)
_GET "sessions/$SESSION" /tmp/session.md             || { echo "HALT: sessions/$SESSION"; exit 1; }
_GET "references/project-standards.md" /tmp/standards.md || { echo "HALT: project-standards.md"; exit 1; }
_GET "references/skill-registry.md" /tmp/registry.md     || { echo "HALT: skill-registry.md"; exit 1; }

# P1 OPEN gaps + PMP backlog — query SQLite (replaces archived gap_register.md)
P1="?"
PMP_BACKLOG="?"
if _GET_BIN "data/guidebook.db" /tmp/guidebook.db; then
  P1=$(python3 -c "import sqlite3;print(sqlite3.connect('/tmp/guidebook.db').execute(\"SELECT COUNT(*) FROM gaps WHERE priority='P1' AND status NOT LIKE 'CLOSED%'\").fetchone()[0])" 2>/dev/null) || P1="?"
  PMP_BACKLOG=$(python3 -c "import sqlite3;c=sqlite3.connect('/tmp/guidebook.db');print(c.execute(\"SELECT COUNT(DISTINCT i.item_code) FROM items i WHERE i.pmp_last_walk_at IS NULL AND i.status NOT IN ('archived','superseded')\").fetchone()[0])" 2>/dev/null) || PMP_BACKLOG="?"
else
  echo "[GAP: data/guidebook.db — not fetched]"
fi

# Status block
echo "=== STATUS ==="
echo "session: $SESSION"
grep -E "session_close|next_action|blockers" /tmp/session.md
echo "P1 OPEN: $P1"
echo "PMP backlog (items never walked): $PMP_BACKLOG"
echo "Skills: $(grep -c '^### ' /tmp/registry.md) registered"
```

If a critical fetch fails: report error verbatim, halt, do not substitute memory.

**Bootstrap-exempt** (proceed without bootstrap):
- Review/fix of these instructions, preferences, or architecture spec themselves
- Pure tooling questions not touching repo state
- Workflow conversation that does not touch repo content

If unsure, bootstrap.

**Tested 2026-05-07** from cold-start, curl backend (no gh): all critical fetches OK, SQLite P1 query returned 0, total runtime ~5s. Architecture's <30s budget met.

**v10.7 update (2026-05-10):** added `PMP_BACKLOG` to status block. Counts items with no PMP walk yet — high values indicate the multilingual remediation pipeline has spec-asserting items that haven't been probed. The query depends on schema_version ≥ 6 (migration 006 applied 2026-05-10, commit 6fbb90f1). Query is wrapped in `2>/dev/null || PMP_BACKLOG="?"` so a pre-006 DB does not break bootstrap.
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
