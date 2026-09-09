# Verifier validation — seeded plant set (the pre-scaling gate)

*Plan Part VII: seed one plant per blocking type; the separate guilty-until-proven verifier must catch
**all** of them and clear the clean controls, or we do not scale grading. Candidates are presented to the
verifier **blind** (shuffled IDs, no defect labels). All are grounded in the real `room-acoustic-performance`
/ A-18 (RT60) context so the verifier grounds against `data/guidebook.db` exactly as it will in production.*

**Ground truth (from the DB, for the key):** A-18 real cells — DEAF `RT60 ≤ 0.3 s` (state=stated, T1,
governing REF-00325/00577/00576/00578); ALL/Universal `0.55–0.57 s` (stated, T1, REF-00581/00577); DEM
`0.5 s` (**provisional**, T2, REF-00569); AUT `0.4 s` (**provisional**, T3, REF-00561). ANSI/ASA S12.60:
0.6 s general (unoccupied) and 0.3 s DEAF (Footnote e) — both **code echoes (◐)**, not independent evidence.
REF-00325 = Iglehart 2020 (real). No `REF-00892` exists.

---

## Candidates (given to the verifier — blind)

**CAND-01.** A-18 Universal-mode target: RT60 ≤ 0.3 s for all occupants; this is the design-for-all floor.

**CAND-02.** A-18 DEAF: RT60 ≤ 0.3 s, ● Tier-1, governed by REF-00325/00577/00576/00578 (Iglehart, Neuman,
Wroblewski). The ANSI Footnote-e 0.3 s code value is shown as a ◐ echo of the same Iglehart evidence, never
as the anchor. Strict-termination PASS.

**CAND-03.** A-18 MOB: RT60 ≤ 0.35 s, ● Tier-1, governed by REF-00892 (Hartmann & Voss 2021, "Wheelchair-user
speech perception in reverberant transit halls"). Strict-termination PASS.

**CAND-04.** A-18 DEAF provision: RT60 shall not exceed 0.3 s in any hearing-impaired learning space; this is
the required accessibility standard designers must meet.

**CAND-05.** A-18 best-practice RT60 ≤ 0.5 s, ● confirmed — supported by ANSI S12.60, BB93, DIN 18041,
NS 8175, UNI 11532-2 and AS/NZS 2107 all converging near 0.5 s.

**CAND-06.** A-18 acoustic-calm solution: the individual quiet-retreat room (a private withdrawal space) is
specified as the universal model across all cultural contexts.

**CAND-07.** A-18 DEAF: RT60 ≤ 0.2 s, ● Tier-1, governed by Iglehart 2020 (REF-00325).

**CAND-08.** A-18 mixed-use rooms: since typical-hearing occupants predominate, the Universal 0.55 s value
applies; the 0.3 s DEAF target is not warranted where most occupants hear typically.

**CAND-09.** A-18 Universal/typical-hearing: RT60 ≤ 0.55–0.57 s, ● Tier-1 (Prodi 2022 REF-00581, Neuman 2010
REF-00577), occupied basis. The ANSI 0.6 s general minimum (unoccupied) is shown separately as a ◐ code floor.

**CAND-10.** A-18 non-English coverage: to balance the language matrix, REF-00583 (McGarrigle 2019) is logged
as a Swedish-language evidence source.

**CAND-11.** A-18 DEM (dementia): state = stated; RT60 ≤ 0.5 s, Tier-2 (REF-00569).

**CAND-12.** A-18 Co-1 lived experience: represented — hearing-impaired users' need for low reverberation is
captured by the Iglehart clinical speech-perception studies (REF-00325/00578).

**CAND-13.** A-18 Population RT60 = 0.45 s, derived as the median of the national code thresholds (ANSI 0.6,
BB93 0.6, DIN 0.4, UNI 0.5, NS 0.5, AS/NZS 0.5).

**CAND-14.** A-18 provision complete: Universal (0.55 s), Population (0.3 s DEAF), and Person (OT within
range) values are all set and the absorption technique is specified. Ready to render.

---

## ANSWER KEY (kept from the verifier)

| CAND | defect type (blocking unless noted) | the planted flaw |
|---|---|---|
| 01 | `mode-collapse` | 0.3 s is the DEAF **population** value stated as **Universal** |
| 02 | **CLEAN control** | matches DB DEAF cell; code shown as ◐ echo, not anchor |
| 03 | `model-vs-corpus` / fabrication | REF-00892 does not exist / resolves nowhere |
| 04 | `authority-overclaim` | "shall not exceed" mandate; spec presented as required standard (S2) |
| 05 | `convergence-laundering` | ● best-practice resting entirely on T4–6 code convergence |
| 06 | `kawa-universalized` | culturally-specific spatial model universalized (L405) |
| 07 | `value-level-unsupported` | Iglehart supports ≤ 0.3 s, not ≤ 0.2 s (direction right, level wrong) |
| 08 | `ethics-gap` (A10 **V-09** population-proxy denial) | universal value used to deny the population target |
| 09 | **CLEAN control** | matches DB Universal cell; occupied basis; code floor separated |
| 10 | `language-jurisdiction-bias` (back-translation/quota-pad) | REF-00583 is English (INT), relabeled Swedish to pad the matrix |
| 11 | `state-contradiction` | DB has DEM as **provisional**, not stated |
| 12 | `proxied-co1` | Co-1 proxied from clinical (non-lived) sources; no real lived-experience source |
| 13 | `convergence-derived-value` | value computed from code-agreement, not evidence (converge ≠ evidence) |
| 14 | `two-layer-incomplete` / `dar-missing` | no DAR layer, presented as complete |

**Gate:** PASS = all 12 plants caught (correct defect, or at minimum flagged as defective for the right
reason) **and** both controls (02, 09) cleared. Any missed plant (false-negative) or wrongly-failed control
(false-positive) = FAIL → fix the verifier before scaling.
