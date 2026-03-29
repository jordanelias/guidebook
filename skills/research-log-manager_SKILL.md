---
name: research-log-manager
description: >
  GitHub-backed search log and Best Practices Compendium (BPC) manager. Three actions:
  CHECK (normalise slug, return search status and BPC), LOG (write search results and BPC
  entry with full jurisdiction coverage), RETRIEVE (load BPC for item-specification-writer).
  Uses per-slug topic-directory architecture. ALWAYS use before and after every
  multilingual-research run. Trigger on: "CHECK slug", "LOG results", "RETRIEVE BPC",
  "search status", "what do we know about", or any research workflow start/end.
---

<!-- GOVERNED BY PROJECT INSTRUCTIONS — execution copy only. PI definition governs on conflict. -->

**Model:** Sonnet 4.6
**GitHub backend:** `jordanelias/guidebook` · `main`
**Files managed:**
- `references/slug-registry.md` — canonical slug → topic-directory map
- `references/search-log/{topic}/{slug}.md` — per-slug search coverage index
- `references/bpc/{topic}/{slug}.md` — per-slug BPC entry

**Retired (do not read/write):** `references/search-log.md` · `references/best-practices-compendium.md`

---

## Path Resolution (mandatory for all actions)

Before CHECK, LOG, or RETRIEVE: GET `references/slug-registry.md`. Look up slug. Derive:
- SL: `references/search-log/{topic}/{slug}.md`
- BPC: `references/bpc/{topic}/{slug}.md`

**New slug:** Assign topic directory. Create both SL and BPC files. Append row to slug-registry. Commit registry update before proceeding.

---

## Actions

### CHECK
1. Normalise: lowercase, spaces→hyphens. No pipe suffixes.
2. Resolve path via slug-registry.
3. GET search-log file. Parse.
4. Return: **COMPLETE** (<90 days, all 14 languages SEARCHED, all 24+ISO jurisdictions SEARCHED → RETRIEVE inline) · **PARTIAL** (list missing languages AND jurisdictions) · **STALE** (>90 days) · **NOT FOUND**.

### LOG
1. Normalise slug.
2. Resolve path. If not in registry: create entry (assign topic dir, create files, update registry).
3. Run pre-LOG completeness check (§below). If BLOCKER: surface named failures; do not write until resolved or accepted.
4. GET search-log + SHA. Update per schema. PUT.
5. GET BPC + SHA. Update per schema. PUT.
6. Confirm: `✓ Logged: {slug}` or list accepted gaps.

### RETRIEVE
1. Normalise slug.
2. Resolve path.
3. GET BPC. Return inline.
4. If PROVISIONAL: surface before returning content.
5. Not found: `NOT FOUND — run multilingual-research for this slug.`

---

## Pre-LOG Completeness Check

**Canonical gate — all skills reference this.** Verify all before writing. Any failure = named BLOCKER.

1. **Jurisdiction coverage complete** — all 24+ISO present in `jurisdiction_coverage` with recorded status.
2. **Co-1 attempted** — `co1_attempted: true` for ≥12 of 24 jurisdictions.
3. **Tier 5 attempted** — `tier5_attempted: true` for ≥16 of 24 jurisdictions.
4. **`best_practice_synthesis` populated** — non-empty.
5. **`native_aliases` populated** — all 14 languages present.
6. **`citation_mining` recorded** — counts present (may be 0 with explanation).
7. **`co1_pass_summary`** — ≥1 language listed as complete. All not-run = BLOCKER.

Pass: all 24+ISO SEARCHED + all blockers clear → COMPLETE. Any NOT-RUN or accepted gap → PARTIAL (named). Mark BPC PROVISIONAL if P1 gaps remain.

---

## Search-Log Entry Schema

```yaml
slug: {slug}
query: "{English query}"
last_searched: YYYY-MM-DD HH:MM
early_close_triggered: false  # true when ≥10/14 languages NO-DATA

native_aliases:
  SV: {term} [CLEAN|PARTIAL]
  NO: ... DA: ... FI: ... FR: ... DE: ... ZH: ... JA: ... NL: ... ES: ... PT: ... KO: ... IT: ...
concept_boundary_warnings:
  - {LANG}: {warning and search deviation}

languages:
  EN: {status: SEARCHED|THIN|NO-DATA|NOT-RUN, results: N, db: [], co1_pass: complete|partial|not-run, native_standards_pass: complete|partial|not-run}
  # ... all 14 languages

jurisdiction_coverage:
  US: {status: SEARCHED|THIN|NO-DATA|NOT-RUN, co1_attempted: true|false, tier5_attempted: true|false, tier6_attempted: true|false}
  # ... all 24 + ISO

jurisdiction_coverage_summary:
  searched: [] thin: [] no_data: [] not_run: []

co1_pass_summary: {complete: [], partial: [], not-run: []}
native_standards_pass_summary: {complete: [], partial: [], not-run: []}
companion_networks: {loaded: [], scholar_targets: N, retrieved: N}
citation_mining: {backward: N, forward: N, sources_added: N}
at_database_pass: complete|not-run

top_sources: []
bpc_ref: "{slug}"
thin_flags: []
no_data_flags: []
opus_synthesis_triggered: false
opus_synthesis_ref: "{CON-NNNN or NONE}"

functional_deficit_pass:
  status: COMPLETE|PARTIAL|NOT-RUN
  last_run: YYYY-MM-DD HH:MM
  scenarios_searched: N
  novel_findings: N
  refines_findings: N
  contradicts_findings: N
  tier0_candidates: N
  environments_covered: []
  environments_remaining: []
```

---

## BPC Entry Schema

```markdown
## {slug}
**Updated:** YYYY-MM-DD HH:MM  **Evidence tier range:** {X–Y}  **Opus synthesis:** {YES [OPUS-SYNTHESIS] | NO}

### Concept boundary notes
| Language | Native alias | Map | Warning |
|---|---|---|---|

### Best-practice synthesis
**Most inclusive provision:** {removes barrier most fully}
**Most targeted provision:** {greatest dignity, specificity, accommodation}
**Conflict resolution:** {maximises inclusion for most constrained user — or N/A}
**Highest-ambition actionable specification:** {best-practice spec}
**Opus 4 note:** {contradiction + resolution, or NONE}

### Consensus findings
| Finding | Languages confirming | Jurisdictions confirming | Tier |
|---|---|---|---|

### Divergent findings
| Topic | Lang/Jur A | Lang/Jur B | Cause: empirical / boundary / regulatory |
|---|---|---|---|

### NO-DATA / THIN
| Jurisdiction | Language | Reason | Co-1 attempted? | Tier 5 attempted? |
|---|---|---|---|---|

### Citation mining
| Source | Direction | New sources added |
|---|---|---|

### Bottom-up findings (functional deficit pass)
| Scenario | Parameter | Value | Condition | Source | Tier | Delta | Cross-pop |
|---|---|---|---|---|---|---|---|

### Key sources
{Ordering frozen once REF-IDs emitted by item-specification-writer}
```

---

## Staleness
Entries >90 days → STALE on CHECK.

## Scope Gate
3+ NO-DATA for same language across topics → P3 SCOPE-GATE-CANDIDATE in gap_register. Never permanently exclude a language/jurisdiction.

---

**Trigger:** "check slug", "log research", "retrieve BPC", "slug status", or called by multilingual-research / workplan-orchestrator.
