---
name: jurisdiction-tracker
description: >
  Track currency of accessibility standards by jurisdiction for the Accessible Built Environments
  Guidebook. Check whether cited standards have been superseded, updated, or revised since the
  guidebook was last edited. ALWAYS use this skill when asked to: check if standards are current,
  verify standard versions, track jurisdiction-specific updates, check if cited regulations are
  still in force, or audit the standards cited for each jurisdiction.
  Trigger on: "are these standards current", "check standard versions", "jurisdiction audit",
  "has this been updated", "standard superseded check". Run once per edition — not per draft.
---

**Model:** Sonnet 4.6 with web search.
**Run schedule:** once per edition.
**Intake:** standards list required. Full document → haiku-chunker Mode C first.
**Storage:** `references/standards-registry.md` on GitHub — one YAML entry per jurisdiction-standard pair.
GET + SHA before writing. Append or update entries. PUT back. Never overwrite other jurisdictions' entries.

Storage entry:
```yaml
jurisdiction: DE
standard_cited: "DIN 18040-2:2011"
current_version: ""
status: CURRENT|UPDATED|SUPERSEDED|WITHDRAWN
key_changes: ""
last_checked: YYYY-MM-DD HH:MM
source_url: ""
```

## Jurisdictions in scope (§4.7.3)
Germany (DIN 18040) · Belgium · Norway (TEK17/SINTEF) · France (CEREMA) · Brazil (NBR 9050) · Japan (MLIT/Barrier-Free Law) · Canada (NBC/CSA B651) · Switzerland · Australia (AS 1428) · UK (BS 8300) · USA (ADA 2010) · EU (EN 17210) · ISO 21542 · Singapore (BCA) · Sweden (BFS) · Denmark (BR18) · Finland (F1 decree)

## Steps
1. List all jurisdiction–standard pairs in scope: `Jurisdiction | Standard cited | Year cited`
2. Web search each standard's issuing body for current version. Note superseding standard or amendment and substantive changes affecting accessibility dimensions.
3. Classify:
   - CURRENT: cited version is current
   - UPDATED: newer edition exists; cited version still valid
   - SUPERSEDED: cited version replaced — must update
   - WITHDRAWN: no replacement — author decision required
4. Output:

| Jurisdiction | Cited | Current | Status | Key Changes | Action |

Update priority: SUPERSEDED → update before publication · UPDATED → check figures still consistent · WITHDRAWN → author decision
Persist all entries to `references/standards-registry.md` on GitHub (GET + SHA + append/update + PUT).
