# Research Protocol — Anti-Consensus-Bias (Revised)
**v2 · 2026-05-09 · Replaces v1**

## What this fixes (and what it doesn't)

This protocol fixes ONE thing: it forces every research finding to produce specific, falsifiable outputs that a human reviewer can spot-check.

It does NOT make Claude genuinely adversarial. Claude's training data is the consensus; web search is filtered by indexing and ranking; the bias toward confirmation is structural, not procedural. No protocol Claude runs on itself can override that.

The protocol's actual mechanism is **DB enforcement plus scheduled human review**. Steps that depended on Claude being honest about its own bias have been dropped because they were performance theater.

## Required outputs per research finding

Every gap closure that involves research must populate these five fields. Gap closure is blocked at the DB level without them.

### 1. Prior statement
What Claude expected to find before searching, and why.

```
prior_expectation: "I expected to find that 22 N is well-supported because ADA, ISO 21542, and BS 8300 all converge on this value."
prior_basis: "Standards consensus from training data."
```

If the search result matches the prior exactly: that's a flag, not confirmation. The reviewer should treat exact-match findings as suspect.

### 2. Population match grade
For every cited study, grade how well its sample matches the guidebook's target population.

| Grade | Definition |
|---|---|
| EXACT | Same condition, same age range, same setting, sample size adequate |
| PARTIAL | Same condition, different age range OR different setting, sample size adequate |
| PROXY | Related condition (e.g., elderly with reduced grip → proxy for RA) OR small sample |
| MISMATCH | Different condition, generalization not justified |

Stored in `evidence_population_match` table (one row per study × target population).

**Rubric for reviewer:** if all match grades come back EXACT, the research is suspect. Real evidence rarely perfectly matches target populations.

### 3. Named dissenter
Specific researcher, paper, or institution with a contrary or qualifying view.

```
dissenter: "Björk et al. 1997 (PMID 9021280) — assessed grip force in 20 women with RA before/after pain; provides one data point but small sample, women only, does not directly test 22N threshold."

Note: Earlier draft of this protocol used "Chaffin et al. 2006" as the example. That citation was NOT verifiable when checked under the protocol itself. This is exactly the failure mode the protocol is designed to catch. Replaced with verified Björk 1997 example.
OR
dissenter: "NONE FOUND — searched [list queries]; no published dissent. Either consensus is genuine or search failed."
```

If "NONE FOUND," the search queries used must be logged. The reviewer can spot-check whether the queries were genuinely adversarial or just confirming.

### 4. Confidence interval + shift condition
```
confidence: "65-80%"
shift_to_low: "Would drop to 30-45% if a study with N>50 in active RA flare population showed grip capacity <15 N"
shift_to_high: "Would rise to 90% if dose-response data on grip force vs door-operation success existed"
```

Numerical ranges, not narrative ("moderate," "strong") because narrative is gameable.

### 5. Falsification condition
What specific finding would make this recommendation wrong.

```
falsification: "Recommendation would change if: (a) RCT with population matching guidebook target showed alternative threshold X; OR (b) post-marketing surveillance showed >5% failure rate at current threshold; OR (c) successor standard supersedes ISO 21542 with different value."
```

Stored in `gaps.falsification_condition`. Required for gap closure.

## DB schema

```sql
ALTER TABLE evidence_sources ADD COLUMN derivation_chain TEXT;
ALTER TABLE evidence_sources ADD COLUMN prior_expectation TEXT;
ALTER TABLE evidence_sources ADD COLUMN search_queries_used TEXT;

ALTER TABLE gaps ADD COLUMN falsification_condition TEXT;
ALTER TABLE gaps ADD COLUMN confidence_interval TEXT;
ALTER TABLE gaps ADD COLUMN shift_conditions TEXT;
ALTER TABLE gaps ADD COLUMN named_dissenter TEXT;

CREATE TABLE evidence_population_match (
    match_id TEXT PRIMARY KEY,
    source_ref TEXT NOT NULL,
    target_population TEXT NOT NULL,
    study_population TEXT,
    sample_size INTEGER,
    match_grade TEXT NOT NULL CHECK(match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH')),
    mismatch_note TEXT,
    created_at TEXT NOT NULL,
    created_by_session TEXT NOT NULL
);
```

Gap closure (status → CLOSED-FIXED, CLOSED-RESOLVED) requires all five fields populated. Enforce via pre-commit hook or scheduled audit query.

## Human spot-check schedule

The protocol works only if a human actually reviews. Without this, the fields become noise.

**Per session:**
- Pick 1 random gap closed in this session
- Ask: "Trace this threshold to primary data" (Claude must show the citation chain or admit it can't)
- Ask: "What would change your mind?" (must match falsification_condition exactly)

**Per 10 sessions:**
- Audit population_match grades — if >70% are EXACT, flag for review
- Pick 3 "NONE FOUND" dissenter entries — re-run with different query phrasing, see if dissenters appear

**Per 50 sessions:**
- External review: ask a domain expert (not Claude) to spot-check 5 closed gaps
- Compare expert's confidence interval to Claude's; flag systematic mismatches

## What was dropped from v1 and why

| Dropped step | Why |
|---|---|
| Trace to primary data | Circular — Claude can't critically evaluate citation chains, will declare "primary" at convenient stopping points |
| Adversarial search ("[X] critique" queries) | Performance theater — finds weak straw-men to dismiss |
| ±20% threshold test | Requires dose-response data Claude doesn't have access to |
| Recency check | Recent ≠ contradictory; same bias in different clothes |

These steps looked rigorous but produced false reassurance. Better to have fewer requirements that actually enforce.

## What this still won't fix

- Claude can fabricate citations. The named-dissenter requirement helps but doesn't prevent it.
- Confidence intervals can be miscalibrated.
- Population-match grades depend on rubric application, which is itself biased.
- The protocol creates audit trails; it doesn't create truth.

The reviewer is the truth-source. The protocol creates legible artifacts the reviewer can examine.

## Adoption

This is a proposal pending decision record. To adopt:

1. Decide whether the DB schema changes are acceptable
2. Decide whether to enforce via pre-commit hook (level 3) or audit query (level 2)
3. Decide who performs the human spot-checks and on what schedule
4. Add to `references/skill-registry.md` if a skill file is desired
5. Update `userPreferences` `<accuracy_and_uncertainty>` to reference this protocol for research tasks
