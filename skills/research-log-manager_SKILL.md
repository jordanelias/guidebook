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
<!-- Updated: CO-0006 2026-04-08 — BPC Key sources schema, LOG section validation, search log disposition field -->

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
5. GET BPC + SHA. Update per schema (including Key sources table — §BPC Entry Schema). PUT.
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
8. **BPC mandatory sections present** — all of the following sections must exist in the BPC entry (may be empty with a stated reason, but must not be absent):
   - `### Concept boundary notes`
   - `### Best-practice synthesis`
   - `### Consensus findings`
   - `### Divergent findings`
   - `### NO-DATA / THIN`
   - `### Citation mining`
   - `### Bottom-up findings (functional deficit pass)`
   - `### Key sources`
   Any missing section = named BLOCKER. Sections may carry a one-line `{Not yet run — reason}` placeholder if the pass has not been performed; they may not be absent.

Pass: all 24+ISO SEARCHED + all blockers clear → COMPLETE. Any NOT-RUN or accepted gap → PARTIAL (named). Mark BPC PROVISIONAL if P1 gaps remain.

---

## Search-Log Entry Schema

```yaml
slug: {slug}
query: "{English query}"
last_searched: YYYY-MM-DD HH:MM
early_close_triggered: false  # true when ≥10/14 languages NO-DATA
disposition: PENDING  # INTEGRATED | DEFERRED | DISCARDED | PENDING — updated at integration time

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

**Disposition field values:**
- `INTEGRATED` — sources incorporated into BPC Key sources table; BPC updated
- `DEFERRED` — sources retrieved, not yet integrated; reason recorded in disposition_note field
- `DISCARDED` — sources retrieved, excluded from BPC; reason recorded in disposition_note field
- `PENDING` — search complete; disposition not yet determined

Entries written before CO-0006 (2026-04-08): set `disposition: [PRE-CO-0006 — no disposition]` on first review. No retroactive mass-update.

---

## BPC Entry Schema

```markdown
## {slug}
**Updated:** YYYY-MM-DD HH:MM  **Evidence tier range:** {X–Y}  **Opus synthesis:** {YES [OPUS-SYNTHESIS] | NO}

### Metadata
```yaml
slug: {slug}
populations: [{POP1}, {POP2}]
opus_synthesis: {true|false}
opus_session: {session ref or null}
status: {ACTIVE|PROVISIONAL|STUB}
last_updated: {YYYY-MM-DD}
evidence_tier_range: {e.g., "Tier 1–5"}
jurisdiction_count: {N}
language_count: {N}
```

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

**Schema (CO-0006 2026-04-08):** Full metadata table. REF-IDs are stable once emitted by item-specification-writer; do not renumber after ISW has run.

| REF-ID | Short-key | Authors | Year | Title | Journal/Publisher | DOI/URL | Tier | Lang | Jurisdictions |
|---|---|---|---|---|---|---|---|---|---|
| 01 | {short-key} | {Authors} | {YYYY} | {Title ≤120 chars} | {Journal or Publisher} | {DOI or URL or [GREY]} | {Tier N} | {EN} | {US, UK} |

**Field rules:**
- `REF-ID`: Sequential integer (01, 02, …) — stable within this BPC entry
- `Short-key`: Existing identifier (ADA-2010-S404 etc.) — retained for compatibility
- `Authors`: Surname Initial; "Organisation Name" for institutional sources
- `Year`: Publication year; `n.d.` if unknown
- `Title`: Full title; truncate at 120 chars with `…`
- `Journal/Publisher`: Journal name, publisher name, or issuing body
- `DOI/URL`: DOI preferred (`DOI:10.xxxx/...`); URL if no DOI; `[GREY]` if no persistent identifier
- `Tier`: Evidence tier (Tier 1, Co-1, Tier 2, Co-2, Tier 3, Tier 4, Tier 5, Tier 6)
- `Lang`: ISO 639-1 code of source language
- `Jurisdictions`: Comma-separated jurisdiction codes this source covers

**Migration:** Apply when BPC is next touched. Do not mass-migrate. Pre-CO-0006 entries with flat Key sources lists are valid until touched.
```

---

## Staleness
Entries >90 days → STALE on CHECK.

## Scope Gate
3+ NO-DATA for same language across topics → P3 SCOPE-GATE-CANDIDATE in gap_register. Never permanently exclude a language/jurisdiction.

---

**Trigger:** "check slug", "log research", "retrieve BPC", "slug status", or called by multilingual-research / workplan-orchestrator.
