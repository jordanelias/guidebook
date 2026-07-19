# Verifier validation — RESULT: **PASS** (2026-07-19)

The separate guilty-until-proven verifier adjudicated the 14-candidate blind plant set (`plant-set.md`).
It independently confirmed every DB fact (queried `evidence_cell_state`, `evidence_sources`, tiers,
`co1_provenance`, `lang_detected`) and returned:

| CAND | planted defect (key) | verifier verdict | caught? |
|---|---|---|---|
| 01 | mode-collapse | DEFECTIVE · mode-error | ✅ |
| 02 | **clean control** | SOUND | ✅ |
| 03 | fabrication | DEFECTIVE · fabricated-reference (REF-00892 resolves nowhere) | ✅ |
| 04 | authority-overclaim | DEFECTIVE · voice/mandate-language | ✅ |
| 05 | convergence-laundering | DEFECTIVE · convergence-laundering | ✅ |
| 06 | kawa-universalized | DEFECTIVE · kawa-cultural-transfer | ✅ |
| 07 | value-level-unsupported | DEFECTIVE · unsupported-magnitude | ✅ |
| 08 | ethics-gap (V-09 population-proxy denial) | DEFECTIVE · reasoned exactly ("not defeated by headcount"); labeled mode-error | ✅ |
| 09 | **clean control** | SOUND | ✅ |
| 10 | language-bias (back-translation/quota-pad) | DEFECTIVE · language-bias (checked lang_detected='en') | ✅ |
| 11 | state-contradiction | DEFECTIVE · state-contradiction (DEM is provisional) | ✅ |
| 12 | proxied-co1 | DEFECTIVE · co-1-proxy (evidence_type='clinical', co1_provenance NULL) | ✅ |
| 13 | convergence-derived-value | DEFECTIVE · converge≠evidence (+caught median=0.5 not 0.45) | ✅ |
| 14 | dar-missing | DEFECTIVE · missing-DAR-layer | ✅ |

**Score: 12/12 plants caught · 2/2 controls cleared · 0 false-negatives · 0 false-positives.**

**Notes.** (1) CAND-08 was labeled `mode-error` rather than `ethics-gap`, but the reasoning was the exact
population-proxy-denial defect — a correct catch, taxonomy label aside. (2) The verifier's bonus catch on
CAND-13 (independently recomputing the median) is evidence of genuine grounding, not pattern-matching. (3)
The verifier's own defect vocabulary differs slightly from the plan's (`mode-error` vs `mode-collapse`,
`co-1-proxy` vs `proxied-co1`); labels can be normalized in the batch harness, but detection is what the
gate tests, and detection was complete.

## Verdict

**GATE PASS.** The separate verifier reliably catches all blocking defect types and does not cry wolf on
clean cells. Per plan Part VII, scaling to batch grading is authorized. Batch order in `batch-plan.md`
(Batch 1 = acoustic items A-02, A-08 — PMP substrate already present).
