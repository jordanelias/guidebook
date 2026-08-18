# 2026-08-18 — Model substitution log

**Purpose.** Fable 5 reached its usage limit mid-task. Work assigned to Fable that is instead
performed by Opus 5 is recorded here, **with the explicit intention of returning it to Fable 5 for
re-examination once quota resumes.** Owner ruling, 2026-08-18.

**Why this matters and is not bookkeeping.** Fable was chosen for **model-family independence** from
the Opus session that authored the artifacts under review. An Opus substitute reviewing Opus-authored
reasoning retains *contextual* independence — a fresh agent that did not write the thing — but loses
*family* independence. This repository's own history is the argument: `sessions/session_2026-08-16-
pr103-adversarial-pass.md` §0 records a pass whose independence was partly spent, declared per
surface rather than in general, and the owner deferred it twice on exactly that ground. The same
discipline applies here.

**This is not a routing-floor breach.** PI rule #2 / DR-2026-06-10 bind `best_practice_synthesis` to
Opus-class models. Substituting *up* the tier does not violate that floor, and none of the work below
is synthesis. The cost is independence, not admissibility.

---

## 1. Ledger

| # | Task | Assigned | Performed by | Status | Handback |
|---|---|---|---|---|---|
| 1 | Consolidated audit of the two 2026-08-16 artifacts + the week's commits | Fable 5 | **Fable 5** | COMPLETE | none — no substitution |
| 2 | Structural census by recursion depth + first cull list | Fable 5 | **Fable 5** | COMPLETE | none |
| 3 | Cull sweep A — executables (`scripts/`, `tools/`, `.github/`) | Fable 5 | **Fable 5** | COMPLETE | none |
| 4 | Cull sweep B — `references/` non-corpus | Fable 5 | **Fable 5** | COMPLETE | none |
| 5 | Cull sweep C — content corpus + renders | Fable 5 | **Fable 5** | COMPLETE | none |
| 6 | Cull sweep D — `workplan/` + `working/` | Fable 5 | **Fable 5** | COMPLETE | none |
| 7 | Cull sweep E — governance / schemas / architecture / decisions / skills | Fable 5 | **Fable 5** | COMPLETE | none |
| 8 | Cull sweep F — DB / check registry / frozen strata / root | Fable 5 | **Fable 5** | COMPLETE | none |
| 9 | **Adversarial critique + reconciliation of the merged cull plan** | Fable 5 | **Fable 5 → FAILED (usage limit), re-run on Opus 5** | SUBSTITUTED | **YES — full re-examination owed** |

Sweeps 1–8 are Fable's own work and carry no substitution debt. **Item 9 is the whole of the debt.**

## 2. Item 9 — what Fable completed before terminating

Fable's run reached the registry entries for the C1/C3 checks and the merge candidates, then
terminated on the usage limit. **No critique output was produced**; nothing partial was salvaged or
inherited by the substitute. The Opus re-run started from the same brief, not from Fable's residue.

## 3. Item 9 — substitution terms

The Opus agent runs the **identical brief**, plus three sharpenings added after seeing where Fable
stopped, all of which tighten rather than relax the test:

1. **C1 must distinguish replacement from unreachability.** A `UNIQUE`/FK may subsume a check's
   *gate* while the script also performs triage or reporting a constraint cannot do. The verdict must
   say which half is replaced and which is merely made dead by construction.
2. **Invisible callers require a constructed test, not an argument.** Sweep A found
   `scripts/audit/graph/*` reachable only via bare `sys.path` imports, and `research_batch_dod.py`
   invoked from a `.claude/settings.json` Stop hook — both invisible to a basename `git grep`. The
   question is whether the shared protocol *finds* such callers or got lucky.
3. **The too-timid test is explicit.** Sweep A returned 114 of 132 executables as keeps. That census
   was performed on the enforcement substrate using the enforcement substrate's own logic; a
   self-interested census returns exactly that figure. The critique must test whether checks are kept
   because load-bearing or merely because wired.

The substitute is required to produce a **PART 3 — SUBSTITUTION LOG** marking every verdict
`MECHANICAL` (follows from a command output; any model re-running it agrees — Fable need not revisit)
or **`JUDGMENT`** (rests on reading, weighing or interpretation — **Fable should re-examine**), plus
the surfaces where a non-Opus reviewer would plausibly differ, and anything left undone.

## 4. What Fable is owed on return

1. **Re-examine every `JUDGMENT`-marked verdict** in the substitute's PART 3. `MECHANICAL` verdicts
   are replayable and need re-running only if a figure is disputed.
2. **Re-test the applicability section specifically.** The question "does this cull actually move the
   owner toward content generation, or does it rearrange furniture in directories they rarely open?"
   is a judgment about value, not a fact about the repository, and it is the section where an
   Opus reviewer assessing an Opus-authored plan is least trustworthy.
3. **Re-test the too-timid finding.** If the substitute upholds sweep A's 114-of-132 keeps, that is
   an Opus census ratified by an Opus critique. Fable should attack it independently.
4. **Nothing in sweeps 1–8** — Fable's own, no debt.

## 4b. Added 2026-08-18 — frame proposal §9 and §10

The frame proposal is **marked for Fable 5** in its own header, so its §7 items were already Fable's
debt. Two of those items have now been closed by Opus under owner ruling, which changes their status
from *open for Fable* to *decided by Opus and owed re-examination*. Logged here rather than only in
the proposal, per §5.

| Item | Verdict | Basis | Marking |
|---|---|---|---|
| §7.6 withdrawn — `specifications` deferred, not re-keyed (§9) | Owner ruling; my prior proposal recorded as a defect | Owner's stage ordering + DDL reads (`parameter` `TEXT NOT NULL`, `parameter_canonical` nullable, `v_value_independence` grouping on `COALESCE`) | **MECHANICAL** on the DDL facts; **JUDGMENT** on §9.3's claim that stage 6 needs those three specific records |
| §9.4 — the 93 stripped names may carry selection bias even as questions | Flagged, not asserted | Reasoning only, no measurement | **JUDGMENT** — flagged in-text as a claim I decline to assert |
| §9.5 — first-batch criterion restated as "≥1 bucket with ≥2 independent roots" | Proposed | Follows from stages 6–7 being deferred | **JUDGMENT** — the threshold (≥2) is a choice, not a derivation |
| §7.3 answered — three jurisdiction buckets adopted (§10) | Adopted with four corrections | Owner proposal | **JUDGMENT** overall |
| §10.1 — buckets omit 7 of 8 Global South jurisdictions named by CANONICAL doctrine | Conflict raised, **not resolved** | `governance/jurisdiction-philosophy.md` §1.2 criterion 1, vs. bucket membership | **MECHANICAL** on the membership arithmetic; **JUDGMENT** on the sequencing-vs-replacement recommendation. **This is the one Fable should attack first.** |
| §10.2 — buckets sequence T4–T6 only; `co1_attempted` must not be bucket-gated | Corrective proposed | `jurisdiction-philosophy.md` §1.3 + §2.1, R1, and the 824/863 no-admission-edge figure | **MECHANICAL** on the doctrine citations; **JUDGMENT** on the inference that the plan would reproduce the pre-reset shape |
| §10.3 — bucket 1 is 6 primary languages, below the ≥9 Co-1 floor | Measured | `lang_jur_map` per-bucket language counts, PRIMARY role only | **MECHANICAL** |
| §10.4 — UN absent from all three stores; 9 of 30 outside the enum; scope decision #6 settled at 48; GB/UK live inconsistency | Measured | Cross-check against enum, `lang_jur_map`, `jurisdictional_values` | **MECHANICAL** |
| §10.5 — staging needs no schema change; `NOT-RUN` is the bucket marker | Established | `search_coverage` DDL | **MECHANICAL** on the DDL; **JUDGMENT** on recommending a `jurisdictions.bucket` column |
| §10.6 — jurisdiction was the wrong dimension to have flagged | Conceded | ~387,000 vs ~12,900 arithmetic | **MECHANICAL** |

**Where a non-Opus reviewer would plausibly differ.** §10.1 is the surface. I raised the Global South
conflict and recommended the sequencing reading, which is the reading that lets the work proceed
without a DR — and "the reading that unblocks me" is the reading I am least able to assess. A reviewer
could reasonably hold that deferring seven jurisdictions behind thirty others, in a project with a
CRPD posture, *is* the reversal and should be argued as one. I did not decide it; I recommended. Fable
should test whether the recommendation is doctrine-respecting or merely convenient.

**Left undone.** The slug × lens ordering rule (§10.6) — named, not proposed.

## 4c. Added 2026-08-18 — frame proposal §10.1.1–§10.1.2, §11, §12

Four further owner rulings, all executed by Opus.

| Item | Verdict | Basis | Marking |
|---|---|---|---|
| §10.1 resolved — buckets 4 and 5 hold the remainder | Owner ruling | — | — |
| §10.1.1 — the five buckets partition the scope **exactly**: 50 slots, 50 unique, identical to `lang_jur_map` (48) + ISO + UN, zero over- or under-coverage | Measured | set arithmetic over `lang_jur_map` | **MECHANICAL** |
| §10.1.1 — *which* members go in bucket 4 vs 5 | Proposed | canonical Global South seven + ET/GH/TZ (already carried by `multilingual-research_SKILL.md`) | **JUDGMENT** — the 10/10 split is mine, not the owner's |
| §10.1.1 — buckets 4–5 add AR, BN, HI, ID, SW; curve is 6→+5→+3→+5→0 | Measured | PRIMARY-role rows in `lang_jur_map` | **MECHANICAL** |
| §10.1.1 — ZA, ET, CY, TH searchable in English only | **Corrected mid-draft** | already flagged `[PRIMARY-LANGUAGE-GAP]` in the data; I nearly reported it as a new defect | **MECHANICAL**, and a near-miss worth recording under guardrail 1 |
| §10.1.2 — PROVISIONAL gate amended; **only the jurisdiction conjunct falls, the ≥9-language floor survives** | Established | buckets 1–3 supply 14 primary languages | **MECHANICAL** on the language count |
| §10.1.2 — the parameterised replacement wording (*declared-bucket scope + disclosure on the entry's face*) | Proposed | three stated reasons | **JUDGMENT** — the disclosure requirement in particular is mine, not the ruling's |
| §10.1.2 — classifying this as a real D-DOCT amendment, reversing what I wrote in §10.1 minutes earlier | Self-correction | §1.2 selection vs §2.3 completeness | **JUDGMENT** |
| §11.1 — the NGO/advocacy/municipality register **already exists in prose** in `skills/multilingual-research_SKILL.md` Steps 2a/2b | Established | direct read; Habinteg, RHF, Procap, ONCE, IBDD, Invalidiliitto, EDF, and `KR \| Seoul Universal Design Guidelines 2022` | **MECHANICAL** |
| §11.2 — split into `jurisdictions` + `research_bodies`; withdraws my §3 recommendation to accept `languages` repetition | Proposed | follows from the country-generic row | **JUDGMENT** |
| §11.3 — advocacy bodies are the missing Co-1 denominator | Argued | `search_coverage.co1_attempted` is a bare boolean; R1; CRPD 4.3 | **JUDGMENT** |
| §11.4 — municipalities deferred; selection criterion is a finding, not a guess | Proposed | §1.1's umbrella argument applied one layer over | **JUDGMENT** |
| §12.1 — `search_executions.engine` enumerates 9 engines **in a comment, not a CHECK**; the 21-database register is prose in a skill | Established | DDL read + skill read | **MECHANICAL** |
| §12.2 — pre-reset corpus: 84 executions, `web`+`manual` = **49 (58%)**, only 2 of 21 registered databases used, **zero** non-English academic indexes | Measured | `_archived/data/corpus-pre-reset-2026-08-06.db` | **MECHANICAL** |
| §12.3 — indexes and bodies are different objects; two tables; `engine` becomes an FK | Proposed | orthogonality argument | **JUDGMENT** |
| §12.3 — `tool_reachable` column | Proposed | four indexes reachable by session tooling, the rest browser-only | **JUDGMENT** |

**Where a non-Opus reviewer would plausibly differ.** Two surfaces.

1. **§10.1.2's disclosure requirement.** The owner released the gate; I proposed that entries state
   their bucket scope on their face. That is an addition to the ruling, not a reading of it, and a
   reviewer could fairly call it my own doctrine smuggled into an execution — the exact defect the
   PR #103 pass filed as P1 against someone else. It is flagged in-text as proposed wording.
2. **§12.2's inference.** The 58% figure is mechanical. The claim that it demonstrates the academic
   channel was never systematically opened is an interpretation of *why* those rows look that way,
   and the corpus was reset for unrelated reasons. Fable should test whether the register was ever
   in force during the period those 84 executions were logged — if it was written later, the figure
   measures something else.

**Left undone.** Bucket-4/5 scheduling; the municipality selection criterion; the slug × lens
ordering rule (still).

## 5. Standing rule

Any future Fable-assigned task performed by another model is appended to §1 with the same columns,
and carries the same PART 3 requirement. A substitution that is not logged here has not been
disclosed, and an undisclosed substitution is a stronger defect than the independence loss itself —
it is the repository's own recurring failure mode (an obligation discharged in name, unrecorded)
applied to the review apparatus.
