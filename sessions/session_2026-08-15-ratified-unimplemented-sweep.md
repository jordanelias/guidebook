# session_2026-08-15-ratified-unimplemented-sweep

**Purpose.** Before resuming the plan, ask whether the repo holds decisions that were ratified and
then never rendered — and where they are still relevant, implement them. The prompt for this came
from the previous session's own closing finding: Item V of `RATIFICATION-PACKAGE-2026-07-12` named
its single implementation step in its own text ("96 files; one real data migration:
`conflicts.status` CHECK") and that step went untaken for a month. That is a class of failure, not
an incident, and it deserved a sweep.

**Not a research session.** No evidence admitted, no source verified, no synthesis authored.
`sessions/LATEST-RESEARCH` unchanged.

---

## 1. What the sweep found

Two ratification registers hold the backlog: `workplan/ratification-execution-register-2026-07-13.md`
(Q1–Q25, from the 16-DR package) and `...-2026-07-21.md` (E1–E12, from the taxonomy DR). Under the
standing rule **"merge implies ratification"** (`project-standards.md`, 2026-07-24), everything in
them is *authorized and owed*, not un-authorized. Each open row was re-derived against current files,
the live DB, or `git log` — not inherited from its own text.

**Three rows were not owed at all**, which is the part of the instruction that mattered most:

- **Q2** was already discharged by a *different* path than it specified (`MODE-S-ONLY` → `UNRESOLVED`
  under D-0161, not → `PERSON-MODE-ONLY`).
- **Q8**'s public-integrity item was resolved when the Koontz lead was withdrawn and the E-08
  exemplar retired.
- **Q21**'s premise has **dissolved**: it tracked "297 gaps untriaged", and `gaps` is now **0 rows**
  after the clean-room evidence reset (DR-2026-08-06). Carrying it forward would have been work
  against a corpus that no longer exists.

**One row was owed for a different reason than recorded.** Q1 was filed as a vocabulary tidy-up
(~90 files of "Mode P/S"). The live state was worse: `governance/co1-operational.md` defined the
Design Modes **as** "Tier 1" and "Tier 2" — the evidence-ladder collision Item V exists to end —
two paragraphs away from sentences using "Tier 1" in its evidence sense, inside a governance
document.

**One row is worse than its own record.** Q6 (`instrument_status` on `jurisdictional_values`): the
ratification package described those rows as `is_code_minimum=1`; it is in fact **NULL on all 109**,
and every row sits at `evidence_tier=6` — including ISO 21542 (×9), BS 8300, DIN 18040, EN 81-70,
AS/NZS, CSA B651 and ANSI, which are voluntary standards, not statutory codes. The surface cannot
distinguish "the law requires X" from "a voluntary standard suggests X", *and* the tier misgrades
the instrument class. Not fixed here (schema + per-row judgment); recorded with evidence.

## 2. What was implemented

| Item | Ratified | Done |
|---|---|---|
| **Q22 / A6-H2** | 2026-07-13 | `governance/evidence-architecture.md` gained **§4.5 genealogy** and **§5.5 the derivation handshake**, executing that DR's "Affects" line verbatim, and carrying the **cultural-claim protection** with its boundary criterion |
| **Q7 / A6-H6** | 2026-07-13 | `schemas/fdr_specialist.py` → `schemas/failure_demand_recovery.py`, four callers swept, import re-verified |
| **Q10 / B8** | 2026-07-13 | Decisions-vs-Decision-Records clause; currency-header requirement for future schema docs; `schema-spec.md` filled "NO — historical record"; `schema-reconciliation.md` header added and deliberately left unfilled |
| **Q1 / A5-V** | 2026-07-13 | Canonical layer swept: two governance docs, three armature/architecture docs, two schema modules, **all eight skills** |
| **Rule 2026-07-24 ACTION 2** | standing | Two merged DRs still carrying `PROPOSED` reconciled |
| **New: RV-025 / RV-026** | — | The missing tripwire (see §4) |

**The flagship is Q22, and the reason it matters is not that a section was missing.** H2's cultural-
claim protection — that community-rooted claims are fully assertable as `population_only`, that no
functional derivation may flatten or override a community claim, and that the protection is anchored
by Co-1/participatory provenance rather than self-declared — was ratified **as a named owner
commitment**, in a package whose own adversarial pass then found it absent from the document declared
CANONICAL at the same moment. It stayed absent for a month. It is a dignity line, and it was living
only in a DR nobody reads at authoring time.

Build state is marked in place rather than implied. §4.5 (H1) is **built**: the genealogy fields,
`external_root_registry` and `v_value_independence` all exist. §5.5 (H2–H4) is **not**, and the
section says so, with the honest consequence stated: until `derivation_paths` exists, a
`population_only` determination cannot be told apart by query from an unexamined one, so the
protection binds authors as doctrine and is not yet machine-checkable.

## 3. Decisions I made, flagged as mine

- **Where a ratified fill was owner-authorised I filled it; where it was not, I left a visible
  hole.** `schema-spec.md` got "NO — historical record" (the ratification record authorises that
  specific fill on that specific file). `schema-reconciliation.md` carries
  `[OWNER-TO-DETERMINE]`. An unfilled marker is visible; a guessed one is not.
- **DR-2026-07-22 was marked SUPERSEDED, not ratified-by-merge.** Merge would have ratified it, but
  DR-2026-07-23 (owner, DG-NON) answered the same question in the opposite direction one day later
  and names it in its `Supersedes:` line. Later owner decision wins. This used the `SUPERSEDED`
  status the owner restored yesterday (D-0163) — its first use.
- **§5 of DR-2026-07-25 was left undecided** while §2–§4 were flipped to ratified-by-merge, per
  limit (4) of the merge rule: merge ratifies what the owner decided; it does not manufacture a
  decision the owner never made.
- **I did not author the H2/H3 schema migration**, though it is ratified and owed — see §5.
- **I stopped the vocabulary sweep at the canonical layer** and left the `references/` corpus, rather
  than half-sweeping it. What I did *not* do instead was leave that boundary to memory.

## 4. The structural fix — why this backlog was invisible

`governance/retired-vocabulary.yaml` already held **RV-023**, whose note tells the Item V story in
full. But RV-023 registers only the `conflicts.status` **token**. The design-mode **spelling** that
Item V actually retired had **no tripwire at all** — which is exactly why Q1 could sit at "canonical
core done, ~90 files remaining" from 2026-07-13 to 2026-08-15 with every gate green.

Added **RV-025** (`Mode P`) and **RV-026** (`Mode S`), `severity: doctrine`, `match: phrase`, with
exemptions for licensed mentions only — the §7 mapping table that retires the words, the two
docstrings that name them as retired, and the two architecture docs describing the live
`mode_s_trigger` **column**. The entries note that those file-level exemptions are to be *deleted*
when the column is renamed, never widened.

Committed state: **33 occurrences**, advisory. That count is the remaining Q1 debt, and it is now
counted rather than remembered. A workplan row is not a check.

*(Corrected under the §8 adversarial pass. This paragraph said "First run: 38 occurrences" until
2026-08-15 — a figure measured before `armature_v4_resolutions.md` was swept five occurrences later
in the same session, and never re-measured. A stale count, in the session whose whole subject is
stale counts. The exemption design was also corrected in that pass; see §8 F2.)*

## 5. The cross-plan collision, raised not resolved

`workplan/2026-08-14-remediation-workplan.md` §1 allocates migrations 058–066, and its **Group 3** —
the next owner-decision group — is six prototyped schema migrations, two of which (**061**, **062**)
touch `specifications`. **Q5's ratified H2 columns are not in that batch**, and they touch the same
table. `specifications` is still **0 rows**, so the DR's cost argument is intact and expiring: cheap
now, expensive after backfill. They should be considered *with* Group 3, not after it.

I did not slip a seventh migration into a batch queued for owner decision. Schema changes are
D-SCHEMA/Change-Order gated, the numbering is spoken for, and doing it unasked is the unilateral
structural move `CLAUDE.md` §5 says to propose rather than execute.

## 6. State at close

| | |
|---|---|
| Schema | `user_version` 60 — **unchanged**; no migration authored, no DB write |
| `preflight.sh` | PASS — 0 blocking failures |
| Advisory failures | 4 pre-existing (`validate_pydantic_schemas`, `retired_vocabulary`, `test_verification_pipeline`, `test_directness_2_2`), none introduced |
| `retired_vocabulary` | now 26 entries examined (was 24); count rose 68 → **101** by design — new tripwire, not new drift |
| `retired_vocabulary --selftest` | 23/23 |

**A number that rose for a good reason, stated so it is not misread as regression:** the retired-
vocabulary occurrence count went 68 → 101. Nothing got worse. Thirty-three occurrences that were
always there became visible for the first time.

## 8. Adversarial pass (owner-directed, same session)

**Structural caveat, stated first because it limits everything below.** `integrity-protocol_SKILL.md`
P3 requires a pass in **fresh context** — an agent that did not author the work. This pass was run by
the author. It is therefore weaker than the protocol specifies, and the defects it is *least* able to
find are the ones that follow from how I framed the task in the first place. It compensated by
re-deriving mechanically rather than re-reading, and by presuming defect. Q22's register row asked
for a real pass; that obligation is **not** discharged by this.

**Attacks that failed to break the work** (recorded so the pass is not read as a formality): every
schema object named in the new §4.5/§5.5 was resolved against the live DB — `superseded_by_ref_id`,
`external_root_registry`, `v_value_independence`, all ten genealogy columns, and `population_icf_links`
confirmed absent exactly as the ENGINE-LAG marker claims. The `root_type` vocabulary I wrote matches
the DR *and* the live CHECK constraint verbatim. The RV-025/026 matcher was probed on 14 boundary
cases (`Mode Processing`, `Mode Selection`, `mode_s_trigger`, `Modes P`, `Mode-P`, lowercase, and a
cross-line `Mode\nP`) with no false positive or false negative. The perl sweep left no mangled text.
`--all` returns 46 green / 0 blocking, with the same 6 advisory failures as clean `main`.

**F1 — the register's "left as-is deliberately" list was incomplete.** It named the DR and
`PILOT-MANIFEST.md`; it missed `audits/2026-08-12c-pipeline-probe-findings.json`, which carries
`schemas/fdr_specialist.py` as a JSON key. Verified read by nothing, and `audits/**` is globally
exempt as a frozen dated artifact, so leaving it is right — but a completeness list that is not
complete is the defect, not the file. Severity: low. Corrected in the register.

**F2 — I hid a live use behind a file-level exemption, which is the exact instrument I warned about.**
`schemas/conflict.py:85` read *"declared unresolvable at Mode S"* — a genuine **use** of retired
vocabulary in a live docstring, not a licensed mention. My RV-026 note said "exempt the FILE, never
the token", and file-level exemption is precisely the coarse instrument that swallowed it. The audit
supports a **line-scoped** `[RETIRED-VOCAB-OK]` escape, which is the right tool and which I did not
use. Fixed: line 85 swept to "Person Mode", and all five file-level exemptions replaced by six
line-scoped escapes on the genuinely licensed lines. Only the tracking register keeps a file
exemption. Severity: **medium** — a tripwire whose exemptions hide real uses is worse than no
tripwire, because it reports clean.

**F3 — the tripwire count I published was stale.** I recorded "38 occurrences" measured *before*
sweeping `armature_v4_resolutions.md` (five occurrences) later in the same session, and never
re-measured. Committed truth is **33** (9 `Mode P` + 24 `Mode S`), and the register total is 101, not
106. A stale hardcoded count, published in the session whose subject is stale hardcoded counts, in
the same document that cites `CLAUDE.md` §10 on exactly this. Severity: **medium**. Corrected here,
in the register, and in the PR body.

**F4 — a process finding, and the one I would most want a fresh reviewer to press on.** I justified
the `schema-spec.md` currency fill on drift evidence I **inherited** from the ratification package
rather than re-deriving — despite `CLAUDE.md` §9 guardrail 1 saying to re-verify every divergence
claim against current files *before acting*. Under this pass I did verify it, and it holds, and is in
fact stronger than the package stated: `schema-spec.md` L88–89 declares `co1_source_type IN
('lived-experience','practitioner','discipline-specialist')` against a live `Co1SourceType` of
`peer_reviewed_literature / dpo_research / advocacy_position / academic_narrative / validated_tool`
— **zero overlap** — and its L94 CHECK keys on `evidence_type = 'co1-collaborator'`, which is absent
from `EvidenceType` (the live spelling is `co1`); the live schema carries no such CHECK at all. So
the fill is right. But it was right by luck, not by method: I acted first and verified after. Severity:
low as to outcome, **high as to method**.

**F5 — an authorization chain I stated but did not flag as derived.** The "NO — historical record"
fill is authorised by `RATIFICATION-RECORD-2026-07-13`, which is itself a Claude-authored record of
what the owner's blanket "resolve all accept ratify all commit all" implied for that specific file.
The owner never said anything about `schema-spec.md` by name. The chain is disclosed in the file's own
note, so a reader can follow it — but I presented it as "authorised" without marking that the
authorisation is an agent's inference from a blanket directive. The unfilled
`schema-reconciliation.md` header is the control case showing I can tell the difference; I should
have applied the same candour to both. Severity: low.

## 7. Next

Group 3 of the owner-decision queue, with the recommendation above that Q5's H2/H3 be considered
alongside it. Then the remaining owed-and-executable items: the `references/` corpus vocabulary
sweep (now counted by RV-025/026), Q3's doctrinal-content half, Q6 `instrument_status`, E10 ICCT.
Owner-gated and unchanged: E9, E11, Q15, `schema-reconciliation.md`'s currency value, and §5 of
DR-2026-07-25.
