# Batch 12 — the criterion, and what four Co-1 passes have now established

**Session id:** `session_2026-09-17-research-batch-12-acceptability-criterion`
**Branch:** `claude/research-preparation-joue00` · **PR** #144
**Cell:** `parameter_id 3` (TERM-001 `ramp gradient`) × `MOB`

> **CLOSED.** Two searches, one source admitted (`REF-00996`), three extractions, one candidate
> resolved and one registered. DoD COMPLIANT (19/19); `test_db_integrity` 71/71;
> `extraction_relations_integrity` CLEAN. Canonical DB moved once: `8b6114fc…` → `0915c34b…`.

This batch ran one target: the acceptability criterion, identified in batch 10, named in batch 11's
record as the highest-value thing left, and **deferred twice because other documents were easier to
retrieve.** Batch 11's own attestation says that in as many words. This is that charge answered.

## The criterion, and it is not bare

> *Hoe groter het hoogteverschil, hoe zachter (kleiner hellingspercentage) de helling moet zijn,
> omdat men gedurende een langere tijd een inspanning moet leveren, en het dus voor iedereen
> haalbaar moet blijven de volledige helling te nemen.*
> **Bij hellingen vormt de fysieke haalbaarheid van de (zelfstandige) rolstoelgebruiker het
> uitgangspunt.**

Both sentences are contiguous in the persisted bytes. The prior was right that the criterion exists
and wrong twice over:

- **Wrong on location.** The page batch 10's plan pointed at (`Regelgeving › Verduidelijking bij
  art. 19`) carries only the decree's explanatory memorandum and contains `fysieke haalbaarheid`
  **zero** times. Retrieved and persisted, so the negative is evidenced. The criterion lives on the
  Handboek proper, `Handboek › Niveauverschillen › Helling`.
- **Wrong that it would be bare.** It arrives with its **mechanism** — greater height means effort
  sustained *longer*, so the gradient must fall for the whole ramp to stay feasible — and with its
  **design case**: the *self-propelling* wheelchair user, with assistants, prams, trolleys and
  rollators named as the *reference* rather than the criterion.

### Why the mechanism matters beyond this cell

Every other row for this parameter is a ceiling with no stated warrant. This is the first statement
of what the number is *for*. It also supplies the term that stops a regress the owner identified on
2026-09-16: dose-response curves that are monotonic with no plateau resolve to 0°, which is not a
ramp. **Feasibility is about effort sustained over the run**, so the acceptable gradient falls as
the run lengthens rather than tending to zero. That is the same direction the two admitted studies
measure, stated in prose by a regulator.

### What it is not

A Flemish public agency asserting what wheelchair users can manage: no participants, no
measurement, no citation. **Not Co-1.** Tiered `national_fw`/T5 rather than `grey`/T3 deliberately —
the 2026-09-13 ruling puts value-restating grey in the regulatory stratum, and T3 would let a
handbook anchor more strongly than the decree it explains.

## Four Co-1 passes, four well-formed zeroes — and that is the finding

| Batch | Co-1 target | Result |
|---|---|---|
| 10 | DPI Japan | Mandatory standard judged inadequate **as a whole**; 勾配 zero times |
| 11 | PVA (US) | No gradient guidance on the free surface at all; expertise behind a book |
| 11 | APF France Handicap | Rights and enforcement, not design; `pente` zero times |
| 12 | Flemish lived-experience media | Ramp **provision**, not gradient; `steil` zero times |

Every pass produced material about whether access exists, is enforced, or is adequate overall. **Not
one stated a gradient figure or threshold.** Meanwhile four regulators and a sports federation state
gradients freely, and the only criterion of acceptability the corpus holds is a government agency
speaking *on behalf of* wheelchair users.

**That asymmetry is a fact about the evidence base, not a gap in the searching.** The people the
parameter is for are published on whether they can get in; the people who set the number are
published on what the number is. Recorded so a later reader does not mistake four well-formed
zeroes for insufficient effort.

The best remaining prospect is a different *kind* of source: **Ramp Up Iceland** (candidate 83), a
disabled-founded project that has installed several hundred permanent ramps. An organisation that
has built ramps hundreds of times has decided a gradient hundreds of times.

## Still not recomputed

The determination stays retired. This batch strengthens the case for ACTION (2) rather than
weakening it: the corpus now holds a criterion, a mechanism and two measurements — and the
measurements still cannot reach the cell, because `gather_sources` takes `claim` and `derived` only
and all three of this batch's rows are `finding`.
