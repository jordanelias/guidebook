# research-log-manager

**Defined in Project Instructions only. Call by name; execute inline.**
**Model:** Sonnet 4.6
**GitHub backend:** `jordanelias/guidebook` · `main` · Protocol → Project Instructions §GitHub API
**Files managed:** `references/search-log.md` · `references/best-practices-compendium.md`

---

## Actions

### CHECK
1. Normalise slug: lowercase, spaces→hyphens, `|<population-code>` suffix (e.g. `grab-bar-height|MOB`).
2. GET `references/search-log.md`. Parse YAML entries. Find matching slug.
3. Return:
   - **COMPLETE** — all 9 core languages `SEARCHED`, <90 days → provide source IDs + BPC slug; call RETRIEVE inline.
   - **PARTIAL** — list languages with status `NOT-SEARCHED`.
   - **STALE** — entry >90 days old.
   - **NOT FOUND** — no entry.
4. If PARTIAL/STALE/NOT FOUND: proceed to `multilingual-research`.

### LOG
Triggered after every `multilingual-research` run. Do not skip.
1. Normalise slug.
2. GET `references/search-log.md` + SHA. Locate or append slug entry. Write entry per schema. PUT back.
3. GET `references/best-practices-compendium.md` + SHA. Locate or append `## {slug}` section. Write entry per schema. PUT back.
4. Confirm: `✓ Logged: {slug}`

### RETRIEVE
1. Normalise slug.
2. GET `references/best-practices-compendium.md`. Locate `## {slug}`. Return inline.
3. If not found: `NOT FOUND — run multilingual-research for this slug.`

---

## Search Log Entry Schema

```yaml
---
slug: grab-bar-height|MOB
query: "grab bar height mobility impairment accessibility"
last_searched: YYYY-MM-DD HH:MM
early_close_triggered: false
languages:
  EN: {status: SEARCHED, results: 12, db: [PubMed, Consensus, SG, web]}
  SV: {status: SEARCHED, results: 6, db: [web]}
  NO: {status: SEARCHED, results: 3, db: [web]}
  DA: {status: SEARCHED, results: 3, db: [web]}
  FI: {status: SEARCHED, results: 2, db: [web]}
  FR: {status: SEARCHED, results: 4, db: [web]}
  DE: {status: SEARCHED, results: 5, db: [web]}
  ZH: {status: THIN, results: 1, db: [web], note: "GB 50763 only"}
  JA: {status: SEARCHED, results: 4, db: [web]}
  NL: {status: NOT-RUN, results: 0, db: [], note: "early-close gate triggered"}
  ES: {status: NOT-RUN, results: 0, db: [], note: "early-close gate triggered"}
  PT: {status: NOT-RUN, results: 0, db: [], note: "early-close gate triggered"}
  KO: {status: NOT-RUN, results: 0, db: [], note: "early-close gate triggered"}
  IT: {status: NOT-RUN, results: 0, db: [], note: "early-close gate triggered"}
top_sources: [REF-042, REF-088, REF-091, REF-107]
bpc_ref: "grab-bar-height|MOB"
thin_flags: [ZH]
no_data_flags: []
---
```

**Status values:** `SEARCHED` · `THIN` (below threshold) · `NO-DATA` (zero results) · `NOT-RUN` (early-close gate) · `NOT-SEARCHED` (PARTIAL returns only)

---

## BPC Entry Schema

```markdown
## grab-bar-height|MOB
**Updated:** YYYY-MM-DD HH:MM  **Evidence tier:** 1–2
**Consensus finding:** [one sentence]
**Range:** [values] (Tier 1 median: [value])
**Jurisdictions confirmed:** [list]
**Early-close:** yes/no  **Thin/No-data:** [list with reason]
**Key sources:** [REF-IDs]
**Divergent findings:** [jurisdiction · standard · value, or —]
```

---

## Rules
- **Staleness:** entries >90 days → STALE on CHECK. Re-run `multilingual-research` for any STALE entry in an active section.
- **Scope gate:** 3+ independent searches returning `NO-DATA` for the same language across different topics → log P3 item in `gap_register.md`: `SCOPE-GATE-CANDIDATE | Lang: XX | Evidence: N/N NO-DATA | Recommend: move to extended set`. Never permanently exclude a language.
