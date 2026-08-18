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

## 5. Standing rule

Any future Fable-assigned task performed by another model is appended to §1 with the same columns,
and carries the same PART 3 requirement. A substitution that is not logged here has not been
disclosed, and an undisclosed substitution is a stronger defect than the independence loss itself —
it is the repository's own recurring failure mode (an obligation discharged in name, unrecorded)
applied to the review apparatus.
