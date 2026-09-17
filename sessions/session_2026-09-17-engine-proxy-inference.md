# ACTION (2) — a determination may now rest on findings plus a threshold

**Session id:** `session_2026-09-17-engine-proxy-inference`
**Branch:** `claude/research-preparation-joue00` · **PR** #144
**Owner statement:** 2026-09-16, `references/project-standards.md`

> **CLOSED.** Migration 086, one engine change, one ratchet, one decision gap. The cell
> `parameter 3 × MOB` is determined for the first time on evidence rather than on codes alone.
> `test_assess_cell_pilot` 18 new assertions, all passing; `test_db_integrity` 71/71;
> `validate_evidence_state` 5/5; battery PASS with no blocking failures. Canonical DB
> `0915c34b…` → `fc481b3c…`, schema 85 → 86.

## What was broken

ACTION (2) named it exactly: *"`assess_cell` must be able to reach a determination from findings
plus a threshold, not only from `claim` rows — today it cannot, and that is why batch 08 reads
`refs=0`."*

`gather_sources()` filters `figure_role IN ('claim','derived')`. A `finding` — a source that
**measured the effect** of the parameter without stating a value — contributed nothing, however
much it had measured. Two studies measuring articular discomfort rising 14→36% and pushrim force
more than doubling were, to the engine, absent.

By the time this ran, batches 10–12 had retrieved the threshold half, so the cell no longer read
`refs=0` — it read **`T4-6-only(regulatory_stratum_only)`**, a pure floor claim whose
`confidence_dimensions_absent` said **"No Tier 1 clinical"** over a parameter with four T1/T2
sources and a Co-1 source. *An assertion of absence across evidence that exists* — the reading the
owner called wrong, wearing different clothes.

## What changed

| Piece | What it does |
|---|---|
| `gather_findings()` | The direction set: sources holding a `finding` for the parameter, through the same tier and disqualification gates as the value set |
| the proxy branch | Threshold from the regulatory stratum + direction from anchoring-tier findings → a determination |
| migration 086 | `specifications.rests_on_proxy_inference` — the mark ACTION (1) requires |
| `compose_value` | Now **reports** governing claims it could not parse, instead of composing from a subset in silence |
| gap cause | A findings-only parameter no longer told the next session its sources had been superseded |

### The result

```
param 3×MOB  provisional  basis=T4-6-only-threshold+T1+CO1+T2-direction(proxy_inference)
             value_max=5.0%  proxy=1  rso=0  supporting=6 findings
```

**5% is the gentlest stated ceiling** — the three-way 1:20 convergence batch 11 found, now selected
by rule rather than noticed by a reader.

### What it deliberately does not do

- **`state` stays `provisional`, never `stated`.** ACTION (1): marked as a proxy, never as a stated
  value.
- **A finding never governs.** `governing` is unchanged; findings land in `supporting`. Stop
  condition 6 and migration 075 both turn on that.
- **No `value_directness` scale was invented.** ACTION (4) and stop condition 4. The column still
  sits at `NOT_ASSESSED` and still has no ratified rule. `rests_on_proxy_inference` records one
  fact with no gradations, which is what the owner's own word — *proxy* — supports.
- **No determination was recomputed beyond this cell**, and the value is not treated as an answer to
  what a wheelchair user can climb. It is what the threshold permits, chosen at the end the measured
  evidence favours.

## Two things the work exposed

**1. The engine cannot read a ratio, and that silently narrows every gradient determination.**
`parse_bound` returns `None` for `1:12` by explicit design, so the interval was composed from **2 of
7** governing claims — the two stating a percentage. As of 086 it says so. **It is harmless today
only by luck:** 1:20 *is* 5%, so the dropped row agrees with the winner. If the only source stating
the gentlest ceiling wrote it as a ratio, the engine would return the **steeper** figure and call it
most-accommodating. Whether an exact notation change is a "conversion" is doctrine — raised as a
`DEC` gap, not decided here.

**2. A check that asserted its own subject was empty.** `validate_verification_consistency` carried
`no_floor: empty-by-decision`. The first live determination gave it `EXAMINED: 1` and `run_checks`
C9 refused the pair. Ratcheted to `min_items: 1` — rule 7a's enforcer catching a claim that went
stale the moment the corpus filled, which is the ratchet CLAUDE.md asks for, arriving on its own.

## Prerequisite recorded on the way

`parameter 3` had no `accessibility_direction`, so `compose_value` could return no interval at all.
Set to `lower_is_better`, **derived from four admitted sources across three strata** — REF-00996's
mechanism, the ADA's own advisory, the IPC's best-practice framing, and the T1 dose-response rows —
none contradicted, and no admitted source names a population for whom a steeper ramp is better.
