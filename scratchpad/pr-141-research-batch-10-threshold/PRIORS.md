# PRIORS — batch 10, the threshold of acceptability for ramp gradient

**Written before the first query is run.** R8 / DR-2026-05-09: a prior recorded after seeing
results is a rationalisation wearing the field that prevents one. Committed before any
`log-search` call so the order is provable from git, not asserted here.

**Session:** `session_2026-09-17-research-batch-10-ramp-gradient-threshold` (bare stem; the same
id with `.md` for `emit_data_migration --session`, `citation_mining_completeness --session`, and
both pointer files — CLAUDE.md §7)
**Cell:** `parameter_id 3` (TERM-001 `ramp gradient`) × identity lens `MOB`, slug
`accessible-circulation-geometry` (continuing coverage — no owner decision needed; a *new* slug
would)
**Pass:** the **threshold half** named by the owner statement of 2026-09-16, ACTION (3): *"The
threshold half is a code value or an equivalent criterion, and `research_code_leads` names which
documents to fetch but deliberately holds no values … so it must be retrieved."*

---

## Why this batch exists, and the correction it starts from

Batch 08 measured the dose-response evidence. Batch 09 reached the Co-1 leg in Japanese and
brought back a lived-experience boundary (REF-00989: steeper than 1/8 and independent
self-propulsion is *"不可能に近い"*). Both batches left `parameter 3 × MOB` at `pending`, and the
owner's 2026-09-16 statement named why in substance: the dose-response curves are monotonic, so
"best outcomes therefore best range" resolves to 0°, which is not a ramp. A ramp exists to change
level, so the design question is the **maximum acceptable gradient**, and that needs a threshold
no admitted source supplies.

**THE MECHANICAL REASON THE CELL IS `pending` IS NOT THE ONE THE BATCH-09 RECORD GIVES, and
batch 10 is designed against the measured reason rather than the recorded one.** That record says
`specification_id 3` is `pending` with `refs=0` *"because `assess_cell.gather_sources()` gathers
`figure_role IN ('claim','derived')` and both Co-1 rows are `finding`"*. The first half is true and
the inference from it is wrong. Measured against the live DB on 2026-09-17, calling the engine's own
functions rather than reading them:

```
python3 - <<'PY'
import sys, sqlite3; sys.path.insert(0,'scripts'); sys.path.insert(0,'scripts/assess')
import assess_cell as A
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
s = A.gather_sources(con, 3)
print(len(s), [(r['ref_id'], r['tier'], r['jurisdiction']) for r in s])
print(A.regulatory_richness([r for r in s if r['tier'] in (4,5)],
                            [r for r in s if r['tier'] == 6]))
PY
```

`gather_sources` returns **two** rows, not zero — REF-00987 (T6, US, ADA 405.2, `claim`) and
REF-00988 (T5, DE, DGUV 6%, `claim`). The Co-1 findings being ungathered is real and is a separate
grievance. What actually holds the cell at `pending` is the next line: those two fall **below §2.3
regulatory richness**, so `determine()` never enters the branch that assigns `governing`, and
`refs=0` is a consequence of the empty assignment, not of an empty gather. Re-derive both figures
before relying on either; the command is above.

**This matters for the batch's design, not just for the record.** If the blocker were an empty
gather, more `claim` rows of any kind would move the cell. It is not, so the question "what would
move it" has a precise answer, and that answer selects the documents to retrieve.

---

## What I expect to find

1. **The paywall is the dominant obstacle, and it is a RETRIEVAL failure, not an absence.** Lead 84
   names AS 1428.1:2021 §15, BS 8300-1:2018 §10 and JIS T 9251:2014. All three are sold, not
   published. Batch 09 already hit this shape once (Habinteg's guide "sold via CAE, NO gradient in
   the retrieved bytes"). Prediction: I retrieve **catalogue and preview pages** for these three and
   **not the clause text**, and every one is logged R14 `RETRIEVAL FAILURE`, never as absence. A
   standards catalogue page is T3 navigation and evidences nothing about the clause.

2. **The freely-published statutory codes are where this batch actually lands.** Government
   publishes law; standards bodies sell standards. Prediction: the JP Barrier-Free Law
   (`research_code_leads` 85, e-Gov), the French *arrêté* (Légifrance) and the UK Approved Document
   M (gov.uk) are retrievable in full, in their own language, and state a gradient. These are
   `code` × `intrinsic` → **T6** by `derive_tier`, which I am not retyping —
   `python3 -c "import sys;sys.path.insert(0,'.');from schemas.tier_derivation import derive_tier;print(derive_tier('code','intrinsic'))"`.

3. **The codes will disagree, and the disagreement is the finding.** The corpus already holds 1:12
   (US, 8.33%) against 6% (DE) — a factor of about 1.4 on one parameter. Prediction: the spread
   widens rather than converges as jurisdictions are added, and no document states a *basis* for its
   own number. Batch 09 found exactly that in DGUV ("The document names no basis for its 6%, so none
   is recorded"). A code that states a figure and no warrant is evidence of what is required, never
   evidence of what is acceptable.

4. **The Flemish handbook is the highest-value document in this batch and the hardest to file.**
   Candidate 69 carries the rise-conditioned table *and* the acceptability criterion itself — *"Bij
   hellingen vormt de fysieke haalbaarheid van de (zelfstandige) rolstoelgebruiker het
   uitgangspunt"*. That sentence is the threshold half in prose: it says what the ceiling is FOR.
   Its blocker is narrow and known — the retrieved bytes carry no publication date, `add-source
   --year` is required, and inventing one is the §5(c) failure. Prediction: a dated carrier exists
   (a versioned PDF, a colophon page, a library record for the same edition) and the difficulty is
   locating it, not judging it.

5. **The Co-1 leg will again succeed in Japanese and struggle elsewhere.** Batch 09's owed list
   names five Co-1/Co-2 routes reached by nobody: APF France Handicap, CERMI/ONCE, PVA, DPI Japan,
   AOTA (member-gated), Foundations (HTTP 403). Prediction: DPI Japan is the likeliest of these to
   yield, because JA is the one language where the Co-1 leg has already worked, and because a
   Japanese DPO commenting on a Japanese statutory figure is the natural pairing for lead 85. For
   the European DPOs I expect the batch-09 result to repeat: the organisations exist, publish, and
   are not reachable through a general index.

6. **No source states a quantitative threshold of acceptability with a warrant that is not a code.**
   This was batch 09's prediction and it held. I am making it again, and if it holds twice the
   honest reading is that the threshold does not exist in the published literature and must be
   reasoned — a synthesis act under the owner's PROXY framing, not a retrieval one.

---

## What would surprise me

- **A code that states its own derivation.** Any of these documents explaining *why* its number is
  its number — a cited study, a stated ergonomic basis, a consultation record — would be the first
  such warrant in the corpus and would change the weight of the whole regulatory stratum.
- **A rise-conditioned table outside Flanders.** The Flemish handbook conditions gradient on rise
  (≤10cm→10%; 10–25cm→8,3%; 25–50cm→6,25%; >50cm→5%). If a second jurisdiction does the same, the
  parameter as this project holds it — a single scalar — is the wrong shape, and that is a finding
  about the schema, not about ramps.
- **A DPO stating a maximum acceptable gradient of its own.** Co-primary with T1 under CRPD Art 4.3
  and the single most valuable admission available on this cell.
- **ISO 21542:2021 retrievable in full.** It is `standard_eb` × `international` → T4, and one T4
  alone satisfies §2.3. I expect the paywall; I would be glad to be wrong.

---

## What I will not do

- **Not treat §2.3 richness as the objective.** One T4, or one T5 from a jurisdiction other than DE,
  or two more T6 from two new jurisdictions, each flips this cell from `pending` to `provisional`
  (measured; the probe is in `QUERY-PLAN.md`). Retrieving documents *because* they flip a gate is
  gate-farming, and §2.3's own falsification clause forbids reading the result as more than it is:
  *"It never becomes a best-practice claim by more codes agreeing."* I retrieve what the owner's
  ACTION (3) names. If the cell moves, that is a consequence to report, not a target to hit — and a
  regulatory floor claim is not an answer to the threshold question.
- **Not read a code ceiling as a threshold of acceptability.** A maximum permitted gradient says
  what is lawful. REF-00989 says what is climbable. These are different claims and the corpus must
  not merge them.
- **Not record a gradient for a source whose clause text I did not retrieve.** A catalogue entry, an
  abstract, a secondary summary or a consultancy page restating a standard is T3 navigation (rule:
  aggregator never evidences content). If I cannot reach the clause, the result is a logged
  retrieval failure and a candidate row.
- **Not invent a publication year, an edition or a clause number.** §5(c). The Flemish handbook's
  whole blocker is a missing date and the temptation is to supply a plausible one.
- **Not invent a `value_directness` grade.** STOP CONDITION 4 — none is ratified, and the
  2026-09-16 statement explicitly does not ratify one.
- **Not claim this batch fixes the engine.** The owner's ACTION (2) — that `assess_cell` must reach
  a determination from findings plus a threshold — is untouched by retrieval. After this batch the
  four T1 dose-response rows still contribute nothing to the cell, because they are `finding` rows
  and `gather_sources` does not gather them. Batch 10 supplies the threshold; it does not build the
  path from findings to a determination, and reporting otherwise would be the batch claiming the
  owner's action item on the strength of having worked nearby.
