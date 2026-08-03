"""Stage 2.2 — tests for schemas/directness.py (rule-based directness model).

Validates the §1.7 bidirectional grain-match, §1.6 mode-asymmetry, the
consolidation rules, the primitive mappers against the LIVE vocabularies, and a
smoke pass over the real DB primitive rows. Pure-stdlib; exit 0 = pass.
"""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from schemas import directness as d  # noqa: E402

DB = os.environ.get("GUIDEBOOK_DB_PATH", "/tmp/work14.db")
fails = []


def check(name, cond):
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}")
    if not cond:
        fails.append(name)


# 1. Population-directness mapper: live vocab + rejection
check("match_grade EXACT/PARTIAL/PROXY map to themselves",
      all(d.population_directness_from_match_grade(g) == g for g in ("EXACT", "PARTIAL", "PROXY")))
check("match_grade NULL -> None", d.population_directness_from_match_grade(None) is None)
try:
    d.population_directness_from_match_grade("BOGUS"); check("unknown match_grade raises", False)
except ValueError:
    check("unknown match_grade raises", True)

# 2. Value-directness mapper: EXACT, PAYWALL->None, NULL->None, strict corroboration
check("value_match EXACT -> EXACT", d.value_directness("EXACT") == d.VAL_EXACT)
check("value_match PAYWALL -> None (ungradeable)", d.value_directness("PAYWALL") is None)
check("value_match NULL -> None", d.value_directness(None) is None)
check("passes_strict=1 corroborates", d.value_corroborated_by_strict(1) is True)
check("passes_strict=0/None does not", not d.value_corroborated_by_strict(0) and not d.value_corroborated_by_strict(None))

# 3. Scale-directness — §1.7 bidirectional grain-match (the new dimension)
check("AGGREGATE x POPULATION = DIRECT",
      d.scale_directness(d.GRAIN_AGGREGATE, d.SCALE_POPULATION) == d.SD_DIRECT)
check("AGGREGATE x PERSON = DOWN-WEIGHTED (too coarse for individual)",
      d.scale_directness(d.GRAIN_AGGREGATE, d.SCALE_PERSON) == d.SD_DOWN_WEIGHTED)
check("AGGREGATE x UNIVERSAL = ADJACENT",
      d.scale_directness(d.GRAIN_AGGREGATE, d.SCALE_UNIVERSAL) == d.SD_ADJACENT)
check("SPECIFIC x PERSON = DIRECT",
      d.scale_directness(d.GRAIN_SPECIFIC, d.SCALE_PERSON) == d.SD_DIRECT)
check("SPECIFIC x POPULATION (no generalization) = DIRECT",
      d.scale_directness(d.GRAIN_SPECIFIC, d.SCALE_POPULATION) == d.SD_DIRECT)
check("SPECIFIC x POPULATION (generalizes beyond measured) = DOWN-WEIGHTED",
      d.scale_directness(d.GRAIN_SPECIFIC, d.SCALE_POPULATION, generalizes_beyond_measured=True) == d.SD_DOWN_WEIGHTED)
check("CODE x UNIVERSAL = DIRECT (the floor)",
      d.scale_directness(d.GRAIN_CODE, d.SCALE_UNIVERSAL) == d.SD_DIRECT)
check("CODE x POPULATION = NON-ANCHORING (convergence-not-evidence)",
      d.scale_directness(d.GRAIN_CODE, d.SCALE_POPULATION) == d.SD_NON_ANCHORING)
check("CODE x PERSON = NON-ANCHORING",
      d.scale_directness(d.GRAIN_CODE, d.SCALE_PERSON) == d.SD_NON_ANCHORING)

# 4. Consolidation rules
check("scale NON-ANCHORING -> NON-ANCHORING",
      d.consolidate(d.POP_EXACT, d.VAL_EXACT, d.SD_NON_ANCHORING) == d.COND_NON_ANCHORING)
check("population MISMATCH -> DISCOUNTED",
      d.consolidate(d.POP_MISMATCH, d.VAL_EXACT, d.SD_DIRECT) == d.COND_DISCOUNTED)
check("value CONTRADICTED -> DISCOUNTED",
      d.consolidate(d.POP_EXACT, d.VAL_CONTRADICTED, d.SD_DIRECT) == d.COND_DISCOUNTED)
check("all full -> DIRECT",
      d.consolidate(d.POP_EXACT, d.VAL_EXACT, d.SD_DIRECT) == d.COND_DIRECT)
check("WITHIN-TOLERANCE + strict corroboration counts as full value",
      d.consolidate(d.POP_EXACT, d.VAL_WITHIN, d.SD_DIRECT, value_corroborated=True) == d.COND_DIRECT)
check("WITHIN-TOLERANCE w/o corroboration -> DOWN-WEIGHTED",
      d.consolidate(d.POP_EXACT, d.VAL_WITHIN, d.SD_DIRECT, value_corroborated=False) == d.COND_DOWN_WEIGHTED)
check("PARTIAL population -> DOWN-WEIGHTED",
      d.consolidate(d.POP_PARTIAL, None, d.SD_DIRECT) == d.COND_DOWN_WEIGHTED)
check("all-None -> None (nothing to condition on)",
      d.consolidate(None, None, None) is None)

# 5. Grain coverage for all 8 evidence types
check("grain map covers all 8 evidence types",
      set(d.GRAIN_FROM_EVIDENCE_TYPE) == {"clinical", "co1", "co2", "code", "grey", "national_fw", "sr_meta", "standard_eb"})
check("sr_meta=AGGREGATE, clinical=SPECIFIC, code=CODE",
      d.GRAIN_FROM_EVIDENCE_TYPE["sr_meta"] == d.GRAIN_AGGREGATE
      and d.GRAIN_FROM_EVIDENCE_TYPE["clinical"] == d.GRAIN_SPECIFIC
      and d.GRAIN_FROM_EVIDENCE_TYPE["code"] == d.GRAIN_CODE)

# 6. Scale<->RecommendationStrength reconciliation
check("SCALE_FROM_RECOMMENDATION maps the 3 strengths",
      d.SCALE_FROM_RECOMMENDATION == {"STRONG_UNIVERSAL": d.SCALE_UNIVERSAL,
                                      "CONDITIONAL_POPULATION": d.SCALE_POPULATION,
                                      "CONDITIONAL": d.SCALE_PERSON})

# 7. End-to-end: a Tier-2 SR cited for a person-specific claim is down-weighted
rec = d.directness_from_primitives(match_grade="PARTIAL", value_match="EXACT", passes_strict=1,
                                   evidence_type="sr_meta", claim_scale=d.SCALE_PERSON)
check("e2e SR->person claim: scale DOWN-WEIGHTED, conditioning DOWN-WEIGHTED",
      rec["scale_directness"] == d.SD_DOWN_WEIGHTED and rec["conditioning"] == d.COND_DOWN_WEIGHTED)
rec2 = d.directness_from_primitives(match_grade="EXACT", value_match="EXACT", passes_strict=1,
                                    evidence_type="clinical", claim_scale=d.SCALE_PERSON)
check("e2e T1 study->person claim: DIRECT",
      rec2["scale_directness"] == d.SD_DIRECT and rec2["conditioning"] == d.COND_DIRECT)
check("check_directness_record clean on a valid record", d.check_directness_record(rec) == [])

# 8. LIVE-DB smoke: consolidate every real population-match row without crashing
if os.path.exists(DB):
    db = sqlite3.connect(DB)
    n = bad = 0
    for (mg,) in db.execute("SELECT match_grade FROM evidence_population_match"):
        n += 1
        r = d.directness_from_primitives(match_grade=mg, claim_scale=d.SCALE_POPULATION,
                                         evidence_type="sr_meta")
        if d.check_directness_record(r):
            bad += 1
    db.close()
    check(f"live smoke: {n} evidence_population_match rows consolidated, 0 vocab violations", bad == 0 and n > 0)
else:
    print(f"  [SKIP] live smoke — {DB} absent")

print(f"\n{'ALL PASS' if not fails else 'FAILURES: ' + ', '.join(fails)}  ({'0' if not fails else len(fails)} failed)")
sys.exit(1 if fails else 0)
