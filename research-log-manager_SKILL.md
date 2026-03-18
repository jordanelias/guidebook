# research-log-manager

**Defined in Project Instructions only. No /mnt/project/ file. Call by name; execute inline.**

**Model:** Sonnet 4.6  
**Backend:** GitHub REST API — `jordanelias/guidebook` · branch `main`  
**Files managed:**
- `references/search-log.md`
- `references/best-practices-compendium.md`

---

## GitHub Read/Write Protocol

All CHECK, LOG, and RETRIEVE operations read from and write to GitHub via the REST API.  
**Never read from or write to local filesystem for these files.**

### PAT
Stored as session variable. If not present in session context, prompt user:
> "Please provide your GitHub PAT to continue."

### Read a file
```
GET https://api.github.com/repos/jordanelias/guidebook/contents/references/{filename}
Authorization: token {PAT}
```
Response: `content` field is base64-encoded. Decode before parsing.  
Capture `sha` from response — required for any subsequent write to the same file.

### Write a file
```
PUT https://api.github.com/repos/jordanelias/guidebook/contents/references/{filename}
Authorization: token {PAT}
Body: { "message": "{commit message}", "content": "{base64-encoded content}", "sha": "{current sha}" }
```
`sha` must match the current file SHA or the write will be rejected (409 conflict).  
Always GET before PUT to obtain current content + SHA.

### Commit message convention
```
research-log-manager: {ACTION} {slug}  [{YYYY-MM-DD HH:MM}]
```

---

## Actions

### CHECK

1. Normalise query to slug: lowercase, spaces→hyphens, append `|<population-code>`  
   Example: `grab-bar-height|MOB`
2. GET `references/search-log.md` from GitHub. Decode base64. Parse YAML entries.
3. Search for matching slug.
4. Return one of:
   - **`COMPLETE`** — all 9 core languages `SEARCHED`, entry <90 days old → provide source IDs and BPC reference slug.
   - **`PARTIAL`** — entry exists; list languages with status `NOT-SEARCHED`.
   - **`STALE`** — entry exists but `last_searched` >90 days ago.
   - **`NOT FOUND`** — no matching slug.
5. If `COMPLETE`: call RETRIEVE and return BPC section inline.
6. If `PARTIAL` / `STALE` / `NOT FOUND`: proceed to `multilingual-research`.

---

### LOG

Triggered after every `multilingual-research` run. Do not skip.

1. Normalise slug from query.
2. GET `references/search-log.md` — capture content + SHA.
3. Locate existing slug entry or append new one.
4. Write/overwrite entry using schema below.
5. PUT updated file back to GitHub with SHA.
6. GET `references/best-practices-compendium.md` — capture content + SHA.
7. Locate existing topic section (`## {slug}`) or append new one.
8. Write/overwrite BPC entry using schema below.
9. PUT updated BPC file back to GitHub with SHA.
10. Confirm: `✓ Logged: {slug} — search-log updated, BPC updated.`

---

### RETRIEVE

1. Normalise slug from query.
2. GET `references/best-practices-compendium.md` from GitHub. Decode.
3. Locate section `## {slug}`.
4. Return section content inline.
5. If not found: return `NOT FOUND — suggest running multilingual-research for this slug.`

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
no_data_flags: []
thin_flags: [ZH]
---
```

**Status values:**
| Value | Meaning |
|---|---|
| `SEARCHED` | Searched; produced usable results |
| `THIN` | Searched; results below best-practice threshold |
| `NO-DATA` | Searched; zero meaningful results |
| `NOT-RUN` | Skipped by early-close gate (≥8 Tier 1–2 sources confirmed) |
| `NOT-SEARCHED` | Not yet attempted (used in PARTIAL returns only) |

---

## Best Practices Compendium Entry Schema

```markdown
## grab-bar-height|MOB
**Updated:** YYYY-MM-DD HH:MM  **Evidence tier:** 1–2
**Consensus finding:** [one-sentence summary]
**Range:** [values] (Tier 1 median: [value])
**Jurisdictions confirmed:** [list]
**Early-close:** [yes/no]
**Thin/No-data:** [list with reason]
**Key sources:** [REF-IDs]
**Divergent findings:** [if any — jurisdiction, standard, value]
**Notes:** —
```

---

## Staleness Rule

Entries older than 90 days are `STALE` on CHECK. Re-run `multilingual-research` for any `STALE` entry in an active guidebook section.

---

## Scope Gate Inference

After 3+ independent searches return `NO-DATA` (not `NOT-RUN`) for the same language across different topics, log a scope gate candidate in `gap_register.md` as P3:

```
SCOPE-GATE-CANDIDATE | Lang: XX | Evidence: N/N topics returned NO-DATA | Recommend: move to extended language set
```

A confirmed scope gate moves the language from core to extended; it is never permanently excluded.

---

## Error Handling

| Error | Action |
|---|---|
| 409 Conflict on PUT | Re-GET to refresh SHA; retry PUT once |
| 404 on GET | File missing — recreate scaffold; retry |
| PAT missing from session | Prompt user before proceeding |
| Rate limit (403/429) | Wait 60s; retry once; report to user if still failing |
