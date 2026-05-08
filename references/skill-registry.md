# Skill Registry — Guidebook
**Built:** 2026-05-08 00:00 UTC · **Source:** auto-built from `skills/` + `workplan-orchestrator_SKILL.md` taxonomy
**Total skills:** 43 · **Active:** 27 · **Recent (30–90d):** 11 · **Deprecated:** 5

**This file is the source of truth for skill assignments.** PI §skills_assigned points here. Architecture v2.2 §reference_files_pattern requires it.

---

## Field definitions

- **Status** — `active` (commit ≤30 days) · `recent` (30–90 days) · `dormant` (>90 days) · `deprecated` (per orchestrator taxonomy or self-marked)
- **Classification** — from `workplan-orchestrator_SKILL.md` §Skill Index: `prose_only` · `hybrid` · `python_tool` · `infrastructure` · `deprecated`. `unclassified` = file exists in repo but absent from orchestrator's taxonomy (drift to be reconciled).
- **Model** — declared model in skill body; `(unspecified)` if absent.
- **Purpose** — first sentence of frontmatter `description`.
- **Triggers** — phrases extracted from `Trigger on:` markers in description. Up to 5 shown; full list in skill file.
- **Calls** — other skills referenced in this skill's body (by name match against repo). Approximate; not authoritative.
- **Flags** — `per-orchestrator-taxonomy`, `absorbs:<skill>`, `self-marked-deprecated`.

---

## Reconciliation drift (flag for resolution)

Items where the orchestrator taxonomy and the actual repo state disagree.

**Skills classified by orchestrator but missing from repo (8):**

- `bulk-renumber` — classed `python_tool`. Likely a Python script (not `*_SKILL.md`) — verify.
- `chunk-assembler` — classed `deprecated`. Likely never built; deprecated bucket implies retired before file existed.
- `evidence-marker` — classed `python_tool`. Likely a Python script (not `*_SKILL.md`) — verify.
- `file-splitter` — classed `deprecated`. Likely never built; deprecated bucket implies retired before file existed.
- `fix-linebreaks` — classed `deprecated`. Likely never built; deprecated bucket implies retired before file existed.
- `haiku-chunker` — classed `deprecated`. Likely never built; deprecated bucket implies retired before file existed.
- `vol2-item-formatter` — classed `deprecated`. Likely never built; deprecated bucket implies retired before file existed.
- `volii-validator` — classed `python_tool`. Likely a Python script (not `*_SKILL.md`) — verify.

**Skills in repo but unclassified by orchestrator (10):**

- `audit-consolidator` — last commit 2026-05-06, model Sonnet. Add to orchestrator taxonomy in next governance pass.
- `cell-curator` — last commit 2026-05-05, model Opus. Add to orchestrator taxonomy in next governance pass.
- `connection-scout` — last commit 2026-05-05, model Opus. Add to orchestrator taxonomy in next governance pass.
- `doctrine-recheck` — last commit 2026-05-05, model Opus. Add to orchestrator taxonomy in next governance pass.
- `economics-auditor` — last commit 2026-05-06, model Sonnet. Add to orchestrator taxonomy in next governance pass.
- `functional-deficit-auditor` — last commit 2026-05-06, model Sonnet. Add to orchestrator taxonomy in next governance pass.
- `item-audit-pipeline` — last commit 2026-05-06, model Sonnet. Add to orchestrator taxonomy in next governance pass.
- `question-author` — last commit 2026-05-05, model Opus. Add to orchestrator taxonomy in next governance pass.
- `relational-integrity-checker` — last commit 2026-05-05, model Sonnet. Add to orchestrator taxonomy in next governance pass.
- `version-diff` — last commit 2026-03-19, model Sonnet. Add to orchestrator taxonomy in next governance pass.

**PI standing-rule conflict:**
- PI v10.3 standing rule #3 invokes `toc-editor` for structural changes. `toc-editor` is on the orchestrator's deprecated list. Resolve in D.4 PI patch — either name the replacement skill or rewrite the rule.

---

## Skill index

## Prose Only (4)

### prose-style-checker
- **Purpose:** Audit and rewrite guidebook text to conform to the project prose register: soft imperative subjunctive ("to be", "to provide"), descriptive headings (no values in headings), qualitative sequencing (Ideal → Best Practice…
- **Status:** recent · **Model:** Sonnet 4.6 · **Last commit:** 2026-03-19
- **Location:** `skills/prose-style-checker_SKILL.md`
- **Triggers:** "check the style", "fix the writing", "apply the style guide", "too wordy", "too hedging" (+6 more)

### session-consolidator
- **Purpose:** End-of-session memory consolidation for the Accessible Built Environments Guidebook project.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/session-consolidator_SKILL.md`
- **Triggers:** "end of session", "wrap up", "consolidate findings", "update project knowledge"
- **Calls:** `connection-scout`, `github-filing`, `github-io`, `multilingual-research`

### voice-style
- **Status:** active · **Model:** Opus 4.6 · **Last commit:** 2026-05-04
- **Location:** `skills/voice-style_SKILL.md`
- **Triggers:** (no explicit "Trigger on:" list — see skill description)

### workplan-orchestrator
- **Purpose:** Orchestrate multi-skill workflows for the Accessible Built Environments Guidebook project.
- **Status:** active · **Model:** Opus 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/workplan-orchestrator_SKILL.md`
- **Triggers:** "start a review", "audit the guidebook", "begin work on", "what's the plan", "how should we approach" (+2 more)
- **Calls:** `github-io`, `session-consolidator`

## Hybrid (Claude judgment + Python validator) (15)

### citation-miner
- **Purpose:** Backward and forward citation mining for confirmed Tier 1–3 sources in the guidebook evidence base.
- **Status:** active · **Model:** Sonnet 4.6 + web search · **Last commit:** 2026-05-05
- **Location:** `skills/citation-miner_SKILL.md`
- **Triggers:** "citation mining", "mine references", "cited by", "backward citations"

### citation-verifier
- **Purpose:** Verify citations, evidence claims, and source credibility for accessibility and built environment documents.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-04-08
- **Location:** `skills/citation-verifier_SKILL.md`
- **Triggers:** "check citations", "verify sources", "audit references", "is this claim supported"

### connection-auditor
- **Purpose:** Query and validate existing connections in the SQLite connections table.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/connection-auditor_SKILL.md`
- **Triggers:** "audit connections", "what connections are pending", "check consumed-deferred", "validate connection robustness", "what hasn't been applied" (+1 more)

### connection-discovery
- **Purpose:** Identify new cross-item, cross-population, compound-interaction, and methodology connections from item specifications, BPC evidence, and published citation networks, and log them to the SQLite connections table via…
- **Status:** active · **Model:** Opus 4.6 · **Last commit:** 2026-05-06
- **Location:** `skills/connection-discovery_SKILL.md`
- **Triggers:** (no explicit "Trigger on:" list — see skill description)
- **Flags:** absorbs:connection-scout

### critique-report-writer
- **Purpose:** Produce structured critique reports for versions of the Accessible Built Environments Guidebook.
- **Status:** recent · **Model:** Sonnet 4.6 · **Last commit:** 2026-03-19
- **Location:** `skills/critique-report-writer_SKILL.md`
- **Triggers:** "critique", "review report", "assess this version", "write up findings", "generate critique" (+1 more)

### cross-population-conflict-mapper
- **Purpose:** Systematically identify and map where population-specific accessibility guidelines produce opposing specifications when applied to the same space.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-06
- **Location:** `skills/cross-population-conflict-mapper_SKILL.md`
- **Triggers:** "cross-population conflict", "competing access needs", "accommodation conflict", "which populations conflict here", "do these specs oppose" (+2 more)
- **Calls:** `connection-discovery`, `content-gap-analyzer`, `functional-deficit-researcher`, `item-audit-pipeline`, `item-specification-writer`, `multilingual-research`, `sensory-coherence-checker`

### economics-researcher
- **Purpose:** Research, verify, and draft economics content for the guidebook's economics volume — covering construction cost data, government funding programmes, property value evidence, cost-benefit analysis, retrofit cost tables,…
- **Status:** active · **Model:** Sonnet 4.6 + web search · **Last commit:** 2026-05-05
- **Location:** `skills/economics-researcher_SKILL.md`
- **Triggers:** "cost data", "grant programme", "economic case", "retrofit cost", "cost-benefit" (+7 more)
- **Calls:** `citation-miner`

### functional-deficit-researcher
- **Purpose:** Bottom-up OT intervention research by functional deficit.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/functional-deficit-researcher_SKILL.md`
- **Triggers:** "bottom-up search", "functional deficit", "OT intervention search", "what does the OT literature say about [specific functional task]", "search by function not population" (+1 more)
- **Calls:** `citation-miner`, `connection-scout`, `evidence-auditor`, `item-specification-writer`, `multilingual-research`

### item-consolidation-analyzer
- **Purpose:** Analyze design items in any Part or Section for consolidation — merging redundant items, splitting overloaded items, assigning typology scope.
- **Status:** recent · **Model:** Sonnet 4.6 · **Last commit:** 2026-03-19
- **Location:** `skills/item-consolidation-analyzer_SKILL.md`
- **Triggers:** "consolidate", "merge items", "reduce items", "split this item"

### item-specification-writer
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/item-specification-writer_SKILL.md`
- **Triggers:** (no explicit "Trigger on:" list — see skill description)

### jurisdiction-tracker
- **Purpose:** Track currency of accessibility standards by jurisdiction for the Accessible Built Environments Guidebook.
- **Status:** recent · **Model:** Sonnet 4.6 with web search. · **Last commit:** 2026-03-18
- **Location:** `skills/jurisdiction-tracker_SKILL.md`
- **Triggers:** "are these standards current", "check standard versions", "jurisdiction audit"

### literature-review-planner
- **Purpose:** Converts research outputs and gap registers into a structured literature review plan for the Accessible Built Environments Guidebook.
- **Status:** active · **Model:** Sonnet 4.6 + web · **Last commit:** 2026-05-05
- **Location:** `skills/literature-review-planner_SKILL.md`
- **Triggers:** "literature review plan", "research plan", "systematic review protocol"
- **Calls:** `citation-miner`, `multilingual-research`

### multilingual-research
- **Purpose:** Conduct accessibility research across 14 languages AND 24 jurisdictions using native-language conceptual vocabulary, Co-1/Tier 2 sources first, and companion network retrieval.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/multilingual-research_SKILL.md`
- **Triggers:** "research", "find evidence", "what does the literature say", "international standards", "review the evidence" (+1 more)
- **Calls:** `citation-miner`

### practice-note-generator
- **Purpose:** Generate practitioner-facing field tools from Accessible Built Environments Guidebook findings.
- **Status:** recent · **Model:** Sonnet 4.6 · **Last commit:** 2026-03-19
- **Location:** `skills/practice-note-generator_SKILL.md`
- **Triggers:** "write a practice note", "generate field tool", "create OT reference", "practitioner guidance", "site visit checklist" (+1 more)

### research-log-manager
- **Purpose:** SQLite-backed search log and Best Practices Compendium (BPC) manager.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/research-log-manager_SKILL.md`
- **Triggers:** "CHECK slug", "LOG results", "RETRIEVE BPC"

## Python Tool (7)

### bibliography-compiler
- **Purpose:** Generate formatted bibliography from the evidence_sources SQLite table.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/bibliography-compiler_SKILL.md`
- **Triggers:** "bibliography", "compile references", "source list", "citation list"

### content-gap-analyzer
- **Purpose:** Analyze accessibility guidebook sections for content gaps against a comprehensive evidence taxonomy covering all disability and neurological populations.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-06
- **Location:** `skills/content-gap-analyzer_SKILL.md`
- **Triggers:** "what's missing", "coverage gaps", "content review"

### cross-reference-resolver
- **Purpose:** Audit and repair all internal narrative cross-references across any guidebook volume — covering section number references, part references, appendix references, and supplementary volume references.
- **Status:** recent · **Model:** Sonnet 4.6 · **Last commit:** 2026-03-29
- **Location:** `skills/cross-reference-resolver_SKILL.md`
- **Triggers:** "check cross-references", "broken references", "stale section refs", "does this section still exist", "validate internal refs" (+5 more)
- **Calls:** `bibliography-compiler`

### evidence-auditor
- **Purpose:** Audit evidence stratification in accessibility guidebook sections — check whether confidence levels claimed match the actual evidence quality.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-06
- **Location:** `skills/evidence-auditor_SKILL.md`
- **Triggers:** "evidence audit", "overclaiming check", "stratification review", "is this evidence strong enough", "confidence level check" (+4 more)

### guidebook-auditor
- **Purpose:** Audit accessibility guidebook documents for format consistency, structural integrity, style compliance, and section-level quality.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-04
- **Location:** `skills/guidebook-auditor_SKILL.md`
- **Triggers:** (no explicit "Trigger on:" list — see skill description)
- **Calls:** `toc-editor`

### sensory-coherence-checker
- **Purpose:** Audit sensory environment consistency across room type matrices in the guidebook.
- **Status:** recent · **Model:** Sonnet 4.6 — cross-domain judgment required. · **Last commit:** 2026-03-28
- **Location:** `skills/sensory-coherence-checker_SKILL.md`
- **Triggers:** "sensory coherence", "sensory consistency", "room matrix audit", "do the sensory specs conflict", "acoustic vs visual check" (+1 more)
- **Calls:** `cross-reference-resolver`

### structure-auditor
- **Purpose:** Audit document heading hierarchy, section nesting, numbering sequences, and structural integrity in any technical guidebook or document.
- **Status:** recent · **Model:** Sonnet 4.6 — structural extraction and validation. · **Last commit:** 2026-03-29
- **Location:** `skills/structure-auditor_SKILL.md`
- **Triggers:** "check the structure", "heading hierarchy", "is the nesting right", "section numbering", "orphaned section" (+5 more)
- **Calls:** `guidebook-auditor`, `prose-style-checker`

## Infrastructure (2)

### github-filing
- **Purpose:** Move stale or superseded files to a deprecated/ subdirectory within the same GitHub directory.
- **Status:** recent · **Model:** Sonnet 4.6 — mechanical file operations. · **Last commit:** 2026-03-29
- **Location:** `skills/github-filing_SKILL.md`
- **Triggers:** "file into deprecated", "move to deprecated", "archive stale files", "clean up [directory]"

### github-io
- **Purpose:** Standardised GitHub read/write/list infrastructure for the guidebook project.
- **Status:** recent · **Model:** Sonnet 4.6 — pure I/O, no judgment required. · **Last commit:** 2026-03-31
- **Location:** `skills/github-io_SKILL.md`
- **Triggers:** (no explicit "Trigger on:" list — see skill description)

## Unclassified (in repo, missing from orchestrator taxonomy) (10)

### audit-consolidator
- **Purpose:** Collects all findings from an item audit pipeline run and produces a structured research brief at references/audit-briefs/{item_code}_brief.md.
- **Status:** active · **Model:** Sonnet 4.6 · effort 75 · extract · **Last commit:** 2026-05-06
- **Location:** `skills/audit-consolidator_SKILL.md`
- **Triggers:** "consolidate the audit", "produce the brief", "audit-consolidator"

### cell-curator
- **Purpose:** Populate evidence state per (specification × population) pair.
- **Status:** active · **Model:** Opus 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/cell-curator_SKILL.md`
- **Triggers:** "cell state"

### connection-scout
- **Purpose:** Identify connections in the evidence base not yet reflected in the guidebook.
- **Status:** active · **Model:** Opus 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/connection-scout_SKILL.md`
- **Triggers:** "find connections"

### doctrine-recheck
- **Purpose:** Periodic operational audit of doctrine-operations alignment.
- **Status:** active · **Model:** Opus 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/doctrine-recheck_SKILL.md`
- **Triggers:** "doctrine recheck", "periodic audit", "doctrine alignment"

### economics-auditor
- **Purpose:** Per-item checklist audit of economic framing at item-spec level.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-06
- **Location:** `skills/economics-auditor_SKILL.md`
- **Triggers:** "audit economic framing", "check economics", "is the cost case sound", "economics review", "do we have a cost note"

### functional-deficit-auditor
- **Purpose:** Per-item audit of functional deficit framing — checks whether an item's claimed populations, ICF codes, mechanism of action, and threshold values are correctly scoped before research is commissioned or atoms are…
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-06
- **Location:** `skills/functional-deficit-auditor_SKILL.md`
- **Triggers:** "audit this item's populations", "is the functional framing correct", "should this population be here", "check the mechanism of action", "does this need FDR research"

### item-audit-pipeline
- **Purpose:** Orchestrates the 8-step per-item audit pipeline sequence, tracking state in item_audit_runs across sessions.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-06
- **Location:** `skills/item-audit-pipeline_SKILL.md`
- **Triggers:** "run the audit pipeline on [item]", "audit item [code]", "item-audit-pipeline [code]", "run pipeline", "start the audit for [item]"
- **Calls:** `audit-consolidator`, `content-gap-analyzer`, `economics-auditor`, `evidence-auditor`, `functional-deficit-auditor`

### question-author
- **Purpose:** Generate question_heading atoms for Part 4 specification items.
- **Status:** active · **Model:** Opus 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/question-author_SKILL.md`
- **Triggers:** "question heading", "write the question", "question mode", "question for this spec"

### relational-integrity-checker
- **Purpose:** Systematic verification that item codes, population codes, and slug names referenced across gap register, connection register, BPC entries, Part 4 scaffold, and application matrices are internally consistent.
- **Status:** active · **Model:** Sonnet 4.6 · **Last commit:** 2026-05-05
- **Location:** `skills/relational-integrity-checker_SKILL.md`
- **Triggers:** "check integrity", "verify references", "orphan codes", "phantom items"
- **Calls:** `workplan-orchestrator`

### version-diff
- **Purpose:** Produce a semantic diff between two versions of the Accessible Built Environments Guidebook.
- **Status:** recent · **Model:** Sonnet 4.6 · **Last commit:** 2026-03-19
- **Location:** `skills/version-diff_SKILL.md`
- **Triggers:** "compare versions", "what changed between", "version diff", "track changes"

## Deprecated (5)

### find-and-replace
- **Purpose:** Systematic text substitution across any guidebook volume or section — covering exact-string replacement, terminology updates, heading corrections, cross-reference fixes, and code/label migrations.
- **Status:** deprecated · **Model:** Sonnet 4.6 · **Last commit:** 2026-03-29
- **Location:** `skills/find-and-replace_SKILL.md`
- **Triggers:** "replace all", "update everywhere", "rename", "find and replace", "change X to Y throughout" (+5 more)
- **Calls:** `cross-reference-resolver`, `evidence-auditor`, `structure-auditor`
- **Flags:** per-orchestrator-taxonomy

### markdown-formatter
- **Purpose:** Enforce consistent markdown heading hierarchy and formatting conventions throughout any guidebook volume — correcting heading levels, fixing escaped markdown artifacts, standardising bold/italic application, and…
- **Status:** deprecated · **Model:** Sonnet 4.6 — pattern matching and substitution. · **Last commit:** 2026-03-29
- **Location:** `skills/markdown-formatter_SKILL.md`
- **Triggers:** "fix heading levels", "heading hierarchy wrong", "markdown inconsistent", "escaped markdown", "H levels wrong" (+8 more)
- **Calls:** `guidebook-auditor`, `prose-style-checker`, `structure-auditor`
- **Flags:** per-orchestrator-taxonomy

### supplemental-integrator
- **Purpose:** Integrate a new supplementary volume into the Accessible Built Environments Guidebook suite.
- **Status:** deprecated · **Model:** Sonnet 4.6 · **Last commit:** 2026-03-29
- **Location:** `skills/supplemental-integrator_SKILL.md`
- **Triggers:** "integrate supplementary volume", "integrate supp vol", "relocate population code", "add new population code", "remove [code] from taxonomy" (+2 more)
- **Flags:** per-orchestrator-taxonomy

### table-formatter
- **Purpose:** Fix, standardize, and enforce consistent table formatting across all Accessible Built Environments Guidebook volumes.
- **Status:** deprecated · **Model:** Sonnet 4.6 · **Last commit:** 2026-03-29
- **Location:** `skills/table-formatter_SKILL.md`
- **Triggers:** "fix tables", "broken table", "table formatting", "standardize tables", "table audit" (+5 more)
- **Calls:** `guidebook-auditor`, `item-specification-writer`, `supplemental-integrator`
- **Flags:** per-orchestrator-taxonomy

### toc-editor
- **Purpose:** Edit the canonical Table of Contents (references/toc.md on GitHub) and generate a structured Change Order for the guidebook.
- **Status:** deprecated · **Model:** (unspecified) · **Last commit:** 2026-03-18
- **Location:** `skills/toc-editor_SKILL.md`
- **Triggers:** "remove", "rename", "move", "add", "relabel" (+3 more)
- **Calls:** `cross-reference-resolver`, `find-and-replace`
- **Flags:** per-orchestrator-taxonomy

---

## Maintenance

- **Rebuild trigger:** any commit to `skills/` or to `workplan-orchestrator_SKILL.md` §Skill Index. Auto-rebuild deferred until D.5 (`build-skill-registry` skill, not yet scheduled).
- **Manual edits:** acceptable but flag with `[MANUAL]` in the entry. Will survive next rebuild only if the rebuild script preserves manual annotations (not yet implemented).
- **Pruning rule** (per architecture v2.2 §skill_registry_pattern): skills `dormant` for >180 days with zero recent invocation in session logs → demote to deprecated.
