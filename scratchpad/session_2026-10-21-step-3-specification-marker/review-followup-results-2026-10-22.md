# Review follow-up, 2026-10-22: mutations and the two-way handshake checks

Measured in the session of 2026-10-22; re-run, do not cite. Harness: `review-followup-mutations.py` (applies one edit, runs the named test file, restores the file).

## Mutations of the new rules (each must turn a test red)
```
KILLED  MU1 confirmers read off the direction set: rc=1
KILLED  MU2 unverified finding/confirming sources not flagged: rc=1
KILLED  MU3 mixed supersession not named: rc=1
KILLED  MU4 staleness compares nothing: rc=1
KILLED  MU5 left-out findings not marked on the junction: rc=1
KILLED  MU6 amend-source engine-column guard removed: rc=1
KILLED  MU7 third junction removed: rc=1
KILLED  MU8 comparator not guarded: rc=1
```

## Bottom-up: a stored determination against the engine (`derivation_handshake_integrity --db`)

A scratch copy of the canonical database; the engine run on parameter 3 x MOB (`assess_cell.py --db <scratch> --emit-sql <out> --parameter-id 3 --slug <slug> --identity MOB --session <s> --stamp <t>`), which commits one live `pilot-4` determination. Then, on copies of that scratch database:

| mutation of an engine input after the answer was written | result |
|---|---|
| none | CLEAN; K01 and K02 each examined the row and passed |
| a governing row's comparator `<=` -> `>=` (the row carrying the winning bound) | FAIL: the engine now gives a different `value_min` |
| a governing source's `tier` 6 -> 1 | FAIL: the engine now gives a different `derivation_sha` |
| a governing source's `notes` | CLEAN (no false positive) |
| a source whose only finding row is skimmed demoted to UNVERIFIED | CLEAN (it was not an input of the answer) |

## Top-down: a rule-version label the dispatch has never seen

The same live row relabelled `pilot-5` with `derivation_sha` recomputed over the unchanged link-set payload: K01 and K02 each examined it and passed with no edit. The pre-follow-up dispatch (`IN ('pilot-3','pilot-4')`) would have read it as the legacy format and reported it stale (legacy recompute differs from the stored sha), and K02 would have examined nothing.

## Not claimed

C10 refuses the scratch determination, correctly: it rests on unverified governing sources. `validate_schema_cross_check` and `retired_vocabulary` are advisory and red as on main; neither cites a line this follow-up changed.
