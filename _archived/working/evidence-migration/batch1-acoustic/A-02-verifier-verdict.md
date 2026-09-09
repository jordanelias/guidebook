# A-02 — separate verifier verdict: **CONFIRMED** (2026-07-19)

An independent guilty-until-proven verifier re-checked the A-02 derivation against `data/guidebook.db`
(19 tool calls) and the web. All six load-bearing claims CONFIRMED; nothing fabricated or overclaimed.

| # | claim | verdict | key evidence the verifier retrieved |
|---|---|---|---|
| C1 | PMP walk converges NRC ≥ 0.90 (ceiling 0.935); only strict-pass row = REF-00563 | CONFIRMED | `PMP-A02-001-S2`, step_value 0.935, passes_strict=1, ref REF-00563; all other steps fail |
| C2 | REF-00563 is a Tier-4 CODE (ANSI/ASA S12.60) | CONFIRMED | tier=4, evidence_type=standard_eb, author=Acoustical Society of America |
| C3 | No T1/T2 source sets an NRC panel threshold | CONFIRMED | all 17 linked Tier≤2 sources are RT60/speech/effort **outcomes**; zero mention NRC/absorption; Iglehart extraction = RT60 0.3 s, not NRC |
| C4 | ◐/`regulatory_stratum_only` is correct (● would be laundering) | CONFIRMED | doctrine L163 "T4–6-only → ● = the convergence-laundering failure mode"; **live precedent cell E-06/MOB** (15 standards, flagged `regulatory_stratum_only`, "NOT an evidence-anchored best practice") |
| C5 | REF-00580 (Amlani 2016, T1) = real panel-backfire evidence | CONFIRMED | tier 1, PMID 27885976, JAAA 27(10):805–815, "Negative Effect of Acoustic Panels on Listening Effort" |
| C6 | no A-02 cell existed (held); item spec 0.85 < ANSI 0.90 floor | CONFIRMED | 0 A-02 rows pre-write; discrepancy real, already surfaced |

**Verdict: the ◐-not-● grade is CORRECT and doctrinally sound.** Written to canonical
`evidence_cell_state` as cell 9012 (state=provisional, regulatory_stratum_only=1, value 0.90–0.935 NRC,
governing REF-00563) + convergence 9012 (single_axis, code-only) — migration
`data_20260719003303`. Verified: FK-check clean, 35/35 integrity, rebuild-parity PASS.

**Data-hygiene note (flagged, not fixed here):** the A-02 PMP-walk rows are stored under slug
`school-environment-autism` while the item and source-links use `room-acoustic-performance` (both ACTIVE,
same topic directory; `item_code` is correctly A-02, so no claim is affected). This is one of the
slug↔item mapping seams the batch plan routes to the Stage-0 triage track — resolve there, not in a
grading migration.
