# Research Protocol — Anti-Consensus-Bias
**Proposal for project adoption. Requires decision record.**

## The Problem

Claude's default research mode is consensus confirmation:
1. Holds a training-data prior
2. Searches for supporting evidence
3. Stops at first confirmation
4. Accepts cited populations as matching target populations
5. Treats threshold values as facts rather than traceable derivations

## Proposed Protocol: 7-Step Adversarial Research

For every specification value or claim under research:

### Step 1: State the prior
Before any search, state: "My training-data expectation is X because Y."
This makes the bias visible. If the search returns exactly X, that's a flag, not confirmation.

### Step 2: Trace the threshold
For any numerical specification: trace the citation chain back to PRIMARY DATA.
- Where did this number first appear?
- What study, what sample size, what population?
- How many citation hops between that study and the current standard?
- Is the original study's population the same as the guidebook's target population?

Log to DB: `evidence_sources.derivation_chain` (new field needed)

### Step 3: Adversarial search
Construct at least 2 queries designed to find CONTRADICTORY evidence:
- "[specification] critique"
- "[specification] limitations"  
- "[specification] insufficient OR inadequate"
- "[alternative approach] [same domain]"

Log adversarial queries to `search_coverage.notes` with prefix `ADV:`

### Step 4: Population matching
For every cited study: does its sample population match the guidebook's target?
- Sample size
- Age range
- Specific condition (not just "wheelchair users" — C5 SCI vs L1 paraplegia vs elderly ambulant wheelchair user are completely different populations)
- Setting (laboratory vs real-world)
- Was the study powered to detect the effect claimed?

Log to DB: new table `evidence_population_match`
| source_ref | target_population | study_population | match_grade | mismatch_note |

### Step 5: Alternative threshold analysis
For every threshold value: what would happen at ±20%?
- Is 22N meaningfully different from 18N or 26N?
- What does the dose-response curve look like?
- Is there a cliff-edge or a gradient?
- Would a different value achieve the same clinical outcome?

This prevents accepting a value because it's "standard" when the standard may have been set arbitrarily.

### Step 6: Recency and supersession check
- Is this the most RECENT evidence, or the most CITED?
- Has anything published in the last 3 years contradicted or refined this finding?
- Has the population's assistive technology changed (e.g., power-assist wheelchairs changing ramp capacity)?

### Step 7: State what would change the recommendation
Before closing any research gap: "This recommendation would change if [specific condition]. The evidence does NOT currently show [specific thing]. The weakest link in the evidence chain is [specific study/assumption]."

Log to `gaps.falsification_condition` (new field needed)

## DB Schema Changes Required

```sql
-- New field on evidence_sources
ALTER TABLE evidence_sources ADD COLUMN derivation_chain TEXT;
-- "ISO 21542 → Schroeder 1979 → grip force study N=34 elderly women"

-- New field on gaps  
ALTER TABLE gaps ADD COLUMN falsification_condition TEXT;
-- "Would change if SCI C5 grip force study (N>50) showed capacity >22N"

-- New table
CREATE TABLE evidence_population_match (
    match_id TEXT PRIMARY KEY,
    source_ref TEXT NOT NULL,
    target_population TEXT NOT NULL,
    study_population TEXT,
    sample_size INTEGER,
    match_grade TEXT CHECK(match_grade IN ('EXACT','PARTIAL','PROXY','MISMATCH')),
    mismatch_note TEXT,
    created_at TEXT NOT NULL,
    created_by_session TEXT NOT NULL
);
```

## Enforcement

This protocol cannot be enforced by text rules (level 1).
Options:
1. **Skill file** — `adversarial-research_SKILL.md` that wraps all research actions
2. **Pre-commit check** — grep for "My training-data expectation" in research log entries
3. **DB constraint** — `evidence_population_match` required before gap closure

## What This Does NOT Solve

- Claude still can't genuinely "not know" something. The prior exists.
- Claude can't assess its own confidence calibration.
- Adversarial searching can become performative (finding weak objections to dismiss).
- The user must spot-check: "Show me the adversarial query results" periodically.

## What The User Should Do

1. **Ask "what would change your mind?" before accepting any finding.** If Claude can't answer specifically, the research is shallow.
2. **Spot-check threshold derivations.** Pick a random threshold value and ask "trace this to primary data." If it dead-ends at "standard X says so," the derivation is incomplete.
3. **Require population-match grades.** If all match grades are EXACT, something is wrong — real evidence rarely perfectly matches target populations.
4. **Watch for the dismiss pattern.** When Claude finds contradictory evidence and explains why it doesn't apply — that's the consensus bias operating. The contradiction should be logged, not dismissed.
