# Citation-Mining Protocol Violation Memo
**Date:** 2026-05-11
**Session:** session_2026-05-11g-citation-mining.md
**Status:** for owner review, decisions pending

## Headline

The `citation_mining` table contained **zero rows across 661 evidence_sources** at the start of this session. citation-miner skill §7 mandates inline invocation by every research skill ("All research skills MUST invoke citation-miner inline for every confirmed Tier 1–3 source"). The mandate is being silently violated in every research session.

Standards RULE 124 (`references/project-standards.md`): "Forward + backward citation mining mandatory for every confirmed Tier 1-2 source." Active backlog: 163 Tier 1-2 sources without citation_mining rows; 386 Tier 1-3.

## Three concrete patterns observed in the 36-h window

### Pattern A: Inline citation-miner not called
Sessions 2026-05-09 through 2026-05-11 (decision-capture, multilingual-search, adversarial-research) added 7 new Tier 2-3 evidence_sources rows. Zero citation_mining rows were created. Skill text alone is not enforcing.

### Pattern B: Named-but-not-promoted standards
session_2026-05-10f BPC-note updates name 8+ standards (JGJ 450-2018, Folkhälsomyndigheten guidance, DIN EN 54-23, DIN VDE 0833-2, NF S 61-931, NF S 61-936, GB 50116-2013, NOU 2001:22, Statsbygg, Loi du 11 février 2005) without [REF:slug:NN] markers, violating RULE 143 (Source Propagation). Will recur every multilingual session unless caught.

### Pattern C: Schema-level dedup failure
source_slug_links has duplicate (slug, local_ref_id) pairs. `accessibility-feature-market-value-uplift-framing` has 19 local_ref_ids each duplicated. `school-environment-autism` has SEA-01 mapping to 4 different ref_ids. There is no UNIQUE constraint blocking these.

## Recommendations

### Hook additions to `hook-workplan-guidebook.md` Phase 1

Two new hooks should be added *ahead of* the existing Phase 1 set (commit-format, filename-convention, frontmatter-schema, citation-format, link-validity), because the actual-violation-rate evidence for these is documented (this memo) whereas the existing Phase 1 hooks address mostly-cosmetic concerns.

#### Hook P1.6 — `citation-mining-row-on-source-add`

**Trigger:** any commit that touches `data/guidebook.db` with an INSERT to `evidence_sources` of a row with `tier IN (1, 2)`.

**Check:** for each new Tier 1-2 ref_id, verify a matching row exists in `citation_mining` with `global_ref_id = ref_id`. If `backward = 1`, accept (mining is done). If `backward = 0 AND deferred_reason IS NOT NULL`, accept (explicit deferral). Otherwise: warning at commit time, block at session-close time.

**Enforcement level:** warn first month, block thereafter.

**Implementation hint:** parse the commit diff for evidence_sources INSERTs (or run a pre-session-close validation script). Could be a `scripts/audit/citation_mining_completeness.py`.

#### Hook P1.7 — `orphan-source-name-in-bpc-prose`

**Trigger:** any commit touching `references/bpc/**/*.md`.

**Check:** scan the diff for patterns matching `(DIN|EN|NF|JIS|GB|BS|ISO|JGJ|NOU|MLIT|FDMA|MHLW|Loi (du|n°)|décret)\s+[A-Z]?-?\s*\d` in added lines. For each match, search the same file for a `[REF:` marker referencing it. If absent: warn.

**Enforcement level:** warn always; never block (false-positive risk too high for blanket blocking).

**Implementation hint:** simple regex + grep. Could be 30 lines of Python. The false-positive cost is low because the warning surfaces only on add-not-link patterns.

### Skill update: `citation-miner_SKILL.md`

Add to §header:
> **Connector availability:** PubMed required (CrossRef via web_fetch is acceptable fallback). Scholar Gateway preferred for forward mining; if unavailable, mark `forward = 0` and populate `deferred_reason` with "Scholar Gateway unavailable" — do NOT substitute PubMed topic search (that is the topic-evidence vs claim-evidence anti-pattern per PI standing rule #7).

### Skill update: research skills must call citation-miner

`multilingual-search_SKILL.md`, `multilingual-research_SKILL.md`, `functional-deficit-researcher_SKILL.md`, `economics-researcher_SKILL.md`, `literature-review-planner_SKILL.md`: each needs an explicit LOG-phase step that calls `python3 scripts/db.py is-mined` for each newly-added Tier 1-3 source, and if `mined: false`, invokes citation-miner before session close. This is the most concrete enforcement available without code-level hooks.

### Schema migration: source_slug_links UNIQUE constraint

Migration 007 spec:
1. Audit script lists all duplicate (slug, local_ref_id) pairs with their ref_id targets.
2. Per-duplicate resolution decision: merge ref_ids (if true duplicate evidence_sources rows) or renumber local_ref_ids (if distinct sources accidentally collided).
3. Apply `ALTER TABLE source_slug_links ADD UNIQUE (slug, local_ref_id)` after cleanup. (SQLite alternative: create new table, copy, swap.)

### PI v10.6 considered: no change recommended

Standing rule #4 (research-log-manager CHECK) already exists. Standing rule #7 (adversarial protocol with topic-vs-claim-evidence anti-pattern) covers the forward-mining-via-topic-search risk. Adding a standing rule #N "all evidence_sources Tier 1-3 must have citation_mining row" duplicates RULE 124 in project-standards. The fix belongs at the hook + skill-update layer, not at the PI layer.

## What this session DID NOT do (declared scope)

- Did not backward-mine the 5 T3 sources within window (T3 mining is not mandatory; queued for batch pass)
- Did not promote the 8 named standards from session_2026-05-10f to evidence_sources (filed as GAP-284)
- Did not resolve the source_slug_links duplicate dataset (filed as GAP-285)
- Did not run forward mining for either T2 source (Scholar Gateway unavailable, GAP-286)
- Did not invoke adversarial-research protocol on the PROBABILISTIC matches (would inflate scope; flagged for owner spot-check instead)

`[CONFIDENCE: high]` — pattern documentation. The 0-row citation_mining table is direct, unambiguous evidence of inline-invocation failure.
`[CONFIDENCE: medium]` — hook spec proposals. Need owner review for false-positive tolerance.
`[SELF-AUTHORED — bias risk]` — this memo. An independent reviewer might propose that GAP-283 should be P0 ("project-critical: every research session is silently violating a stated must"), not P1.
