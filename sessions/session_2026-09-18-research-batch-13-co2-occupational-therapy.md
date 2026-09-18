# Batch 13 — the Co-2 pass, and a status claim that was false

**Session:** `session_2026-09-18-research-batch-13-co2-occupational-therapy`
**Parameter:** 3 (TERM-001, ramp gradient) · **Slug:** `accessible-circulation-geometry`
**Priors:** `scratchpad/batch-13-co2-occupational-therapy/PRIORS.md`, committed at `3db5769` before the
first query, corrected at `323b716` before the first screening.

---

## 1. The batch began on a false premise, and the premise was in a merged PR

PRIORS.md was written to run the Co-2 pass "for the first time". That framing was wrong. Derived —
not remembered — from `search_executions`:

```
select count(*) from search_executions where target_evidence_type='co2'   ->  2 (before this batch)
```

Both are batch 09's (`session_2026-09-16-research-batch-09-ramp-gradient-co1`): an RCOT search that
**read *Adaptations without Delay* in full and found no gradient anywhere**, and an AOTA search that
hit a member gate and was recorded as an R14 retrieval failure. Neither admitted anything.

**The propagation chain is worth naming, because only the last link is an error.** Batch 12's
attestation says Co-2 is "untouched **across three batches**" — true of batches 10, 11 and 12.
PR #144's body compressed that to "Still owed: **Co-2 (untouched)**", dropping the qualifier and
turning a scoped observation into a false absolute. I then read the PR body as live state instead of
deriving it. That is CLAUDE.md rule 7 in three steps: a true scoped claim, a lossy restatement, and a
reader who trusted the restatement.

What survived the correction: **zero Co-2 rows in `evidence_sources`** — right before this batch and
right after it. What changed is *why*. Not an unrun pass; a pass that ran, ran well, and admitted
nothing.

## 2. What was retrieved, and what the retrieval overturned

Four searches, all logged verbatim with the pre-committed prior (exec 54–57).

### Foundations — the hypothesis batch 09 staged is falsified

Candidate 72 described the Foundations *Guidance For Ramp Adaptations* as "the apparent source of the
1:15/1:12 length-conditioned figures the search index shows". The search index still says so: a
snippet this session received reads *"for ramps up to 10m long, the gradient should not be steeper
than 1 in 15, and for ramps up to 5m long, 1 in 12"*.

The live page returns 403 (Cloudflare). The R10 ladder reached a Wayback snapshot — 2023-12-07,
HTTP 200, 69,711 bytes, `sha256 b201d3be…`. **The retrieved document contains zero instances of
1:15, 1:12, 10m or 5m.** What it states is a *boundary*, not a ceiling:

> For a walkway to be considered accessible, the gradient (slope) must not be steeper than 1:20. A
> gradient steeper than 1:20 would be considered a ramp and require all associated ramped
> requirements such as handrails and kerbs.

For ramp design it **delegates** — to a Charnwood Borough Council guide and to Approved Document M,
already held as REF-00992. Resolved OUT-OF-SCOPE for parameter 3: its 1:20 defines when a walkway
becomes a ramp, and filing that as a ramp maximum is the copy rule 5 forbids.

**This is the batch's clearest vindication of R10.** The snippet was plausible, specific, numerate
and wrong, and admitting on it would have produced a fabricated attribution with a real URL attached.
Batch 09 saw the same snippet and correctly declined; this batch went and looked.

*Caveat, stated because it limits the finding:* the falsification holds against the 2023-12-07
snapshot. The live page is blocked and therefore unverified.

### The GB delegation chain terminates outside the profession

Composing batch 09's RCOT reading with this batch's Foundations reading:

    RCOT, Adaptations without Delay  ──delegates ramp design to──▶  Foundations
    Foundations, Guidance For Ramp Adaptations  ──delegates to──▶  Approved Document M (REF-00992)

**No OT-discipline warrant appears at any link.** The UK OT professional body's effective position on
ramp gradient is the building regulator's, reached through an intermediary that also defers to the
building regulator. That is a finding about where dimensional authority sits, and it is stronger than
either half alone.

### REF-00997 — admitted, and deliberately not Co-2

**SA DCSI Equipment Program, *Equipment Program Clinical Considerations for Prescribers — Home
Modifications: Ramps*, February 2013.** Live URL 403; R10 ladder to Wayback, HTTP 200, 159,744 bytes,
`application/msword`, `sha256 1d4ebe3d…`.

| Extraction | Value | Role | Why |
|---|---|---|---|
| 34 | `1:14` `<=` | **claim** | The general rule, rise >190mm |
| 35 | `1:8` `<=` | **finding** | The small-rise branch, rise <190mm — see §3a |
| 33 | — | **finding** | The individualisation duty |

> Assess the client's/carer's ability to propel the wheelchair over this gradient as some clients may
> require a less steep gradient.

**This is the second criterion-of-acceptability statement in the corpus and the first to put the duty
on a named clinician.** REF-00996 states the criterion as a design principle — physical feasibility
for the independently self-propelling wheelchair user is the starting point. This states it as an
*operational duty*: the tabulated gradient is a default, and a prescriber must test it against this
client, with authority to depart from AS 1428.1 on documented clinical reasoning.

### 3a. The 1:8 row was filed wrong first, and two blocking gates said so

It was written `condition`, by analogy to REF-00990 extraction 23 — the Japanese ただし書 proviso
relaxing the 1:12 ceiling to 1:8 where the rise is ≤16 cm. **The analogy was wrong twice.**

*Substantively:* 00990's row is a proviso **excepting** a stated ceiling. REF-00997's two sentences
are **parallel branches** of one rule split at a rise threshold — the shape Approved Document M's
gradient table and the IPC's two grades already have. Both of those are filed `finding`, with no
edges (extractions 26 and 29). The closer precedent wins.

*Procedurally:* `extraction_relations_integrity` (blocking) fails any `condition` that qualifies
nothing, and the edge could not be written — see GAP-007 below.

Caught by `extraction_relations_integrity` and `test_db_integrity` C04 **after** a first migration had
already been applied. Nothing was committed, so both were fixed at source and the migration re-emitted
rather than papered over with a compensating migration. The replay is
`scratchpad/batch-13-co2-occupational-therapy/replay.sh`, which is the batch as a re-runnable script.

### 3b. GAP-007 — a latent trap in the write path

`add-extraction` has `--verbatim-exempt` for an artefact the verbatim checker cannot decode.
`relate-extraction` **has no equivalent**, and requires `--quote`. So for any non-UTF-8 payload — a
PDF, a legacy `.doc` — a `figure_role='condition'` can be *written* but never *related*, and the
blocking check then fails it. Three individually correct rules make one state unreachable.

This batch was not blocked by it (the precedent-correct role turned out to be `finding` anyway), so
it is registered as latent rather than live. **The next genuine proviso extracted from a PDF hits it.**

**Tiered T5 `national_fw`, not Co-2.** A state government equipment programme is not an OT
professional body, and the document grounds itself in AS 1428.1 — the 2026-09-13 ruling puts
value-restating material in the regulatory stratum. T2/Co-2 would have been the flattering call for
the one admission of a batch whose whole purpose was to find a Co-2 source.

## 3. The determination: recomputed, unchanged

Specification 5 retired (new evidence, not a wrong value); specification 6 determined.

```
param 3×MOB   provisional   max 5 %   ·   max 1:20      refs 7 -> 8
              both stated by a source · both exact · neither chosen
```

`1:14` is 7.14%, steeper than 5%, so the gentlest-ceiling selection is untouched. **The batch adds a
governing source and does not move the number** — which is what a prior worth writing down predicted,
and is recorded as a result rather than buried as a non-event. `rests_on_proxy_inference` stays 1;
REF-00997 is T5 and supplies no direction at an anchoring tier.

## 4. Still zero Co-2, now for a third recorded reason

| Body | Jurisdiction | Outcome |
|---|---|---|
| RCOT | GB | Read in full (batch 09). No gradient anywhere. **Genuine absence.** |
| AOTA | US | Member-gated. **Retrieval failure**, three ladder rungs still untried (candidate 85). |
| OT Australia / WFOT / CAOT | AU / INT / CA | **Not reached.** The AU search surfaced state equipment programmes, not the professional body. |

The AU pass found prescriber-facing clinical guidance, which is close to the register Co-2 occupies —
but published by a state government, not a professional college. **The honest statement is that Co-2
remains unadmitted and only partly searched**, and that the corpus keeps meeting the same shape:
institutions stating figures on behalf of disabled people.

## 5. Owed after this batch

- **Co-2 proper**: OT Australia, WFOT, CAOT — never searched at all.
- **Candidate 85**: AOTA ladder rungs (WorldCat, Google Books, archived NGC summary) — ISBN 9781569003572.
- **Candidate 84**: SWEP Victoria manual — dead link returning HTTP 200 with body `File does not exist.`
- **GAP-002** (P1) names its own closing condition as "a code value or an equivalent criterion". Batches
  11–12 supplied both and this batch supplied a second criterion. **It looks closeable and was left
  open**: closing it is a judgment this batch did not stop to make, and `close-gap`'s vocabulary defect
  (PR #144, recorded-not-fixed) is unresolved.
- **GAP-007** (P2, raised here): give `relate-extraction` the `--verbatim-exempt` that
  `add-extraction` already has.
- **GAP-001/003/004** assert causes that the batch-08-era engine produced and the 086 fix corrected.
  They are stale. Not touched here.
