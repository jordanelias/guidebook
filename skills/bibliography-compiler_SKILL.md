---
name: bibliography-compiler
description: >
  Compile, deduplicate, and assemble a master bibliography from distributed BPC entries, existing bibliography files, and guidebook inline citations. Use this skill whenever asked to build, rebuild, or update the project bibliography, reconcile citations, find orphan references, or produce bibliography-v{N}.md. Triggers: "compile bibliography", "build bibliography", "update bibliography", "reconcile citations", "orphan citations", "bibliography audit".
---
<!-- GOVERNED BY PROJECT INSTRUCTIONS — execution copy only. PI definition governs on conflict. -->

# bibliography-compiler

## Purpose

Produces a single deduplicated APA 7th bibliography from all project citation sources. Outputs `references/bibliography-v{N}.md` on GitHub.

## When to Use

- Edition boundary bibliography build (WS-6D equivalent)
- Post-research-batch bibliography update
- Citation orphan audit (guidebook body vs. bibliography)

## Inputs

| Source | Location | What to extract |
|---|---|---|
| Existing bibliography | `/mnt/project/bibliography-v8.md` or GitHub `references/bibliography-v{N-1}.md` | Full entries — already APA-formatted |
| BPC slug files | GitHub `references/bpc/{topic}/{slug}.md` | `### Key sources` sections |
| BPC population files | GitHub `references/bpc/{POP}.md` | `### Key sources` sections |
| Cross-ref compendium | `/mnt/project/cross-reference-bibliography-compendium-*.md` | Gap entries flagged as missing |
| Economics sources | GitHub `references/economics-sources.md` | If populated |
| Guidebook body | `/mnt/project/Guidebook_for_Accessible_Design_*.md` | Inline `(Author, Year)` citations for orphan check |

## Execution — Three Phases

### Phase 1: Extract (Python script)

Run `scripts/bib-extract.py`. The script:

1. GETs `references/slug-registry.md` from GitHub → builds slug→path map
2. For each BPC path (slug files + population top-level files):
   - GET file from GitHub API
   - Extract lines between `### Key sources` and next `###` or `---` or EOF
   - Parse each numbered line into: `{origin_slug, raw_line, tier_tag}`
3. Parses existing bibliography file into same normalized format: `{origin: "bib-v8", raw_line, section}`
4. Writes `working/bib-raw-extraction.md` — flat file, one source per line

**Script location:** `/home/claude/scripts/bib-extract.py`
**Output:** `/home/claude/working/bib-raw-extraction.md`

### Phase 2: Deduplicate + Normalize

Two sub-steps:

**2a. Fuzzy dedup (Python script `scripts/bib-dedup.py`):**
- Extracts author surname(s) + year from each raw line using regex
- Groups by `(first_author_surname, year)`
- Within each group: flags duplicates, selects longest/most-complete entry as canonical
- Writes `working/bib-dedup-groups.md` with cluster IDs

**2b. Sonnet judgment pass (inline — not scripted):**
For each dedup cluster:
- Confirm entries are truly the same source (not surname+year collision)
- Select or compose the best APA 7th citation
- Classify into section: A (Standards/Codes, Tier 4–6), B (DPO/Advocacy, Co-1/Tier 2), C (Research, Tier 1/3), D (OT Frameworks, Co-2), E (Economics)
- Assign verification flag: ✅ (confirmed real) / ⚠ (requires DOI/URL verification) / ❌ (audit flag)
- Assign evidence tier

Output: `working/bib-normalized.md`

### Phase 3: Assemble + Commit

1. Sort entries alphabetically within each section (A–E)
2. Add editorial key header (from bibliography-v8 format)
3. Add GAPS table (carried from v8 + any new unverified entries)
4. Add metadata header: version, date, entry count, source count by section
5. Commit to GitHub at `references/bibliography-v{N}.md`

**Cross-check (orphan audit):**
- Parse guidebook body for all `(Author, Year)` and `(Author et al., Year)` patterns
- Match each against bibliography entries
- Report: orphan citations (in body, not in bibliography) and unused entries (in bibliography, not cited in body)
- Unused entries are NOT errors — BPC evidence supports specifications without always being parenthetically cited

## Output Format

```markdown
# Bibliography — v{N}
## Guidebook for Accessible Design
**Version:** v{N} | **Date:** {YYYY-MM-DD HH:MM} | **Format:** APA 7th edition
**Entries:** {total} | **Sources by section:** A: {n} · B: {n} · C: {n} · D: {n} · E: {n}
**Compiled from:** bibliography-v{N-1} ({n} entries) + {n} BPC slug files + {n} BPC population files

---

## Editorial Key

| Symbol | Meaning |
|---|---|
| ✅ | Independently verified |
| ⚠ | Requires DOI or full citation verification before formal publication |
| ❌ | Citation audit flag: see note |
| [translated from X] | Translated from non-English source |

---

## A — Standards and Codes

{entries}

## B — DPO and Advocacy Sources

{entries}

## C — Research

{entries}

## D — OT Frameworks

{entries}

## E — Economics and Grant Programmes

{entries}

---

## GAPS — Citations Requiring Verification

| Citation as used | Location | Gap type | Status |
|---|---|---|---|

---

## Orphan Audit

### Cited in body, not in bibliography
| Citation pattern | Guidebook line(s) |
|---|---|

### In bibliography, not cited in body (informational — not errors)
| Entry | Section | Note |
|---|---|---|
```

## Token Rules

- Phase 1 is entirely scripted — zero Sonnet tokens except error handling
- Phase 2a is scripted — zero Sonnet tokens
- Phase 2b: budget ~40 tokens per source × estimated 250 unique sources = ~10,000 tokens
- Phase 3: ~3,000 tokens for assembly and commit
- Cross-check: ~2,000 tokens
- **Total Sonnet budget: ~15,000 tokens across 1–2 sessions**

## Session Boundary

If Phase 1 extraction yields >300 unique sources after dedup: split Phase 2b across two sessions (A–C in session 1, D–E + cross-check in session 2). Checkpoint after Phase 2a with cluster count.

## Dependencies

- GitHub API access (PAT)
- Python 3 with `json`, `base64`, `re`, `collections` (all stdlib)
- Existing bibliography file in `/mnt/project/` or on GitHub
- Slug registry on GitHub
