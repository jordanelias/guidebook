<!-- BPC CANONICAL TEMPLATE — CO-0006 2026-04-08 -->
<!-- Apply when creating new BPC entries or when migrating existing entries on first-touch. -->
<!-- All sections are MANDATORY. Sections not yet run must carry a one-line placeholder — not be absent. -->
<!-- research-log-manager LOG will BLOCKER on any missing section. -->

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
| {LANG} | {native term} | {DIRECT / APPROXIMATE / PARTIAL} | {boundary note or —} |

### Best-practice synthesis
**If `opus_synthesis: false`: this section carries REDUCED-CONFIDENCE — Sonnet draft only; Opus review pending.**

**Most inclusive provision:** {removes barrier most fully}
**Most targeted provision:** {greatest dignity, specificity, functional accommodation}
**Conflict resolution:** {maximises inclusion for most constrained user — or N/A}
**Highest-ambition actionable specification:** {best-practice spec}
**Opus 4 note:** {contradiction + resolution, or NONE}

### Consensus findings
| Finding | Languages with evidence | Jurisdictions confirming | Tier |
|---|---|---|---|
| {finding} | {N languages} | {N jurisdictions} | {tier} |

### Divergent findings
| Topic | Lang/Jur A | Lang/Jur B | Cause: empirical / boundary / regulatory |
|---|---|---|---|
| {topic} | {position A} | {position B} | {cause} |

### NO-DATA / THIN
| Jurisdiction | Language | Reason | Co-1 attempted? | Tier 5 attempted? |
|---|---|---|---|---|
| {JUR} | {LANG} | {reason} | {Yes/No} | {Yes/No} |

### Citation mining
| Source | Direction | New sources added |
|---|---|---|
| {source} | {backward/forward} | {N} |

*If no Tier 1–2 sources found: `{Not run — no Tier 1–2 sources confirmed in this slug}`*

### Bottom-up findings (functional deficit pass)
| Scenario | Parameter | Value | Condition | Source | Tier | Delta | Cross-pop |
|---|---|---|---|---|---|---|---|
| {scenario} | {parameter} | {value} | {condition} | {source} | {tier} | {delta vs Universal Mode} | {populations} |

*If FDR pass not yet run: `{Not yet run — schedule functional deficit pass}`*

### Key sources

| REF-ID | Short-key | Authors | Year | Title | Journal/Publisher | DOI/URL | Tier | Lang | Jurisdictions |
|---|---|---|---|---|---|---|---|---|---|
| 01 | {short-key} | {Authors} | {YYYY} | {Title ≤120 chars} | {Journal or Publisher} | {DOI or URL or [GREY]} | {Tier N} | {EN} | {US, UK} |

*REF-IDs are stable once emitted by item-specification-writer. Do not renumber after ISW has run.*
*Pre-CO-0006 flat Key sources lists are valid until this BPC is next touched.*
