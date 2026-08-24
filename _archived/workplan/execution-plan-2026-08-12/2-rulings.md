# Wave 2 — Rulings that gate everything after them

**Read `00-holistic-execution-plan.md` first.** **Precondition: L1 exists.**

**Nothing in this wave is executed by a session.** All three are decisions. D-A and D-B gate
Waves 3 and 4; D-C is now a configuration audit whose switch is already thrown.

**Doctrine SHA at HEAD: `0f2f525`** — matching the resolution plan's declaration. Re-derive with
`git rev-parse HEAD:governance/mission-and-epistemics.md | cut -c1-7`.

---

## D-A · Is value determination a machine stage or a human one? *(D-METH)*

### The question
No code path runs from N extracted values to one determined value. Is that a defect to fix, or
an undeclared boundary to declare?

### The evidence, re-derived at HEAD

| Fact | Location |
|---|---|
| The engine writes the literal `None, None, None` for `value_min, value_max, value_unit`, unconditionally, on every path | `assess_cell.py:559`; column list at `:566-567` |
| It is the **only corpus writer** of `specifications` | Writer sweep: `:570,:572` are the engine; the five other INSERT sites (`validate_verification_consistency.py:101`, three test fixtures, `jurisdictional_divergence.py:263`) all build their own fixture DDL |
| `source_value_extractions` has **zero writers** anywhere in non-legacy `.py` | Every mention is a read |
| Convergence status is hard-coded | `assess_cell.py:337`, under the comment at `:326-336`: *"no rule exists for grading value-level convergence, so nothing here can grade it"* |

### The W9.5 qualification — required, and it changes the framing

D-A's framing (*"no code path runs from N values to one"*) restates the pre-correction wording.
**The correct finding is that the Progressive Measurement Probe protocol exists, is unrun
(`spec_value_probes` = 0 rows), and is unwired.** The DR rules on the *judgment* step; PMP is the
measurement protocol upstream of it. Write it that way or the ruling mis-describes its own
subject.

### Recommendation: **human, declared**

Add to `governance/pipeline-contract.yaml` under the `judgment` stage (block begins `:68`;
`criteria:` currently ends at `:97-101`), following the file's own `check: null`
DECLARED-BUT-UNENFORCED convention defined at `:19-23`:

```yaml
      - id: value-determination-human
        kind: integrity
        criterion: >
          Value determination is a declared human judgment act, not a machine
          stage. A value row (value_min / value_max / value_unit on
          specifications) is written ONLY by data migration; ONLY onto a
          cell whose state is 'stated' or 'provisional' with non-empty
          governing_refs; and ONLY when every extraction the value rests on is
          reachable from the cell via specification_source_links. Acceptance:
          value_unit IS NOT NULL wherever value_min or value_max IS NOT NULL;
          value_min <= value_max. The writing migration names the cell and the
          doctrine_sha it was judged under.
        references: >
          DR-2026-08-XX-value-determination-is-human; assess_cell.py:559
          (engine writes NULLs by design); evidence-architecture.md §5;
          W9.5 (PMP is the measurement protocol upstream of this judgment)
        check: null
```

### The dependency, confirmed
**"An attestation naming the cell" is impossible today.**
`schemas/attestation.schema.json:13` constrains `artifact` to
`^(references/bpc-reasoning|references/connection-reasoning|decisions|sessions)/.+\.md$`.
Until W3.3 lands, the criterion must name **the migration file** as the attested artifact.

### Open sub-questions
1. The input contract's *"every extraction reachable via `specification_source_links`"* is not checkable
   until W3.5 gives that junction a writer.
2. Does the human act also grade convergence? `assess_cell.py:326-336` says grading is a judgment
   act — the DR should say **whose**.

### Falsifier
A code path is found that writes non-NULL `value_min/max/unit` from extractions. Then D-A's
premise fails and the ruling must be re-put.

---

## D-B · The derived-value marker — ratified, zero repository presence

### The question
Does a derived marker's **fill** inherit its input evidence's strength band, or cap one band
below?

### Presence, re-derived
`rg -l "▲|◭|△"` returns 7 files: 4 `workplan/` documents plus three that are **not the marker
scheme at all** — `tools/evidentiary_audit.py:1420-1421` and its dashboard use `▲▼` as table-sort
arrows, and `specs/e-08.html:374+` uses ▲ as a `sym-warn` glyph in the hand-authored mockup.

So the plan's claim — zero hits across `governance/`, `schemas/`, `scripts/`, `decisions/`,
`references/` — is **confirmed exactly as scoped**. `rg -n "derived-value|triangle" decisions/`
returns zero: **no DR records the scheme.** It exists only in workplan documents W7.12 proposes
to retire, so **the DR must quote the scheme definition, not cite it.**

**New constraint no prior document records: ▲ is already visually claimed by `sym-warn` in the
mockup.** The W3.1 renderer must not reuse that class or context.

### The two positions

**For inheritance.** The ratified scheme separates the dimensions — shape for derivation, fill
for strength — exactly parallel to ●/◐/○ (`governance/tier-system.md` §5 `:66-73`, band table
§8 `:95-99`). Capping encodes derivation twice and breaks the parallel.

**For capping.** `governance/evidence-architecture.md:170` states the directness layer *"**is**
GRADE's indirectness domain, applied bidirectionally"* — and GRADE downgrades one level for
indirectness. Repo precedent agrees: `assess_cell.py:35-38` caps any partially-assessed
dimension at DOWN-WEIGHTED, *"never silently full-match"* (mechanism restated `:81-84`).

### Recommended resolution — the vocabulary already supports it
Key fill behaviour to `synthesis_method_indicator`:

- `direct` → inherits;
- `inferred` → caps one band, with `inference_basis` **mandatory**;
- `consensus` → takes the band the convergence rules give the underlying set.

**The name is load-bearing.** `armature_v4_resolutions.md:104` reserves **`synthesis_method`**
for a *different* ratified vocabulary (`narrative`/`quantitative`/`mixed`, on BPCMetadata);
`:110-111` gives **`synthesis_method_indicator`** plus `inference_basis` for the specification
layer. Using the wrong one collides two ratified vocabularies.

### Composition constraint
Any cap rule must compose with `tier-system.md` §8 `:101` — a T4–T6-only cell already takes ○
regardless of derivation.

### Open sub-questions
1. A `consensus` over `inferred` inputs — the three-value vocabulary gives no composition rule.
2. Whether fill-band semantics are **DG-NON** (evidence-tier definitions are owner-only,
   CLAUDE.md §5). If so this is a proposal, not a D-METH ruling.

---

## D-C · Branch protection — **premise dead; a configuration audit remains**

### Re-verified live this session via the authenticated GitHub API

`main` is **protected: true** at `fd4c09d`, and is the **only protected branch of 36**. The
archive branch `archive/pre-reset-corpus-2026-08-06` at `4fc6304` is **unprotected** — which is
W9.6's finding, re-confirmed here.

**Six documents assert the opposite and are stale in the opposite direction from every prior
check:** `CLAUDE.md` §0 (`:23-24`) and §7 (`:321-322`), `check-registry.yaml`'s NB,
`references/tooling-register.md` F2 and §6.7 preamble (`:237`, `:335`, `:351`), and the
register's sequencing step 8. These corrections are Wave-8 class.

### What a session can and cannot see
`protected: true` is the whole of it. The required-check list, classic-vs-ruleset, and
admin-bypass flags are **not readable** without admin scope. The owner must read
Settings → Branches or `gh api repos/jordanelias/guidebook/branches/main/protection`.

### The three questions, with exact job-name strings

Required checks match on the **name string**, and `tooling-register.md:572-575` warns that
renaming a job silently wedges every PR. The twelve jobs in `.github/workflows/ci.yml`:

| job id | name string | line |
|---|---|---|
| `classify` | **`Classify change (work kinds → batteries)`** | `:54-55` |
| `syntax` | `Syntax (UTF-8, JSON, YAML)` | `:117-118` |
| `structure` | `Structure (BPC, cross-refs)` | `:129-130` |
| `data` | `Data layer (DB integrity, migration reproducibility, citation mining)` | `:141-142` |
| `db-integrity` | **`DB integrity (content checks)`** | `:153-154` |
| `tests` | `Tests (regression cover for the audit scripts)` | `:165-166` |
| `schema` | `Schema (entity YAML, evidence state, populations, jurisdictions)` | `:177-178` |
| `governance` | `Governance (decisions, doctrine recheck, adversarial use, contract)` | `:189-190` |
| `attestation` | `Attestations (presence, schema, evidence, verdict)` | `:201-202` |
| `research` | `Research contract (definition-of-done + its enforcers)` | `:218-219` |
| `render` | `Render (derived-output freshness, rendered-document integrity)` | `:230-231` |
| `commit-msg` | `Commit message + doctrine token` | `:244-245` — **push-only, can never be a PR required check** |

**Q1 — is `Classify change (work kinds → batteries)` required?** It must be. Battery jobs are
gated on classify's outputs via `if:` conditions, and **a GitHub job skipped by an `if:` reports
as passing for required-status purposes.** If only battery jobs are required, a broken
classifier greens every PR on checks that never ran.

**Q2 — is `DB integrity (content checks)` required?** It must **not** be — but the original
ground is dead. `test_db_integrity` is now **70/70 green** (run this session:
`RESULTS: 70/70 checks passed`), not red. **The replacement ground stands:** a large fraction of
the 70 reference only empty tables, so requiring it today locks in a vacuous green. It goes in
after R-15's vacuity-warrant work.

**Q3 — are reviews required?** On a single-author repo they must not be, or admin bypass must
stay on, else no PR ever merges.

### Retro-binding
The standing rule *"no check promotions in the same window as branch protection"* applies
**now** — the window is open. This constrains W0.1 and W7.10.

### Falsifier
The protection turns out to be an empty ruleset (require-PR only, zero required checks). Then
D-C collapses back into "choose the required set", using §6.7's list verbatim.

---

## Re-derivation notes

| Claim | Status | Evidence |
|---|---|---|
| `None, None, None` at `:559`; only corpus writer | **CONFIRMED** | writer sweep |
| `source_value_extractions` zero writers | **CONFIRMED** | sweep |
| `check: null` convention exists | **CONFIRMED** | `pipeline-contract.yaml:19-23`; two judgment criteria already use it |
| Attestation cannot name a cell | **CONFIRMED** | `attestation.schema.json:13` |
| Zero glyph presence in the five named trees | **CONFIRMED** | ◭ appears only in 4 workplan files |
| No DR records the triangle scheme | **CONFIRMED** | `decisions/` sweep |
| `synthesis_method` vs `synthesis_method_indicator` name split | **CONFIRMED** | `armature_v4_resolutions.md:104` vs `:110-111` |
| ▲ collides with an existing `sym-warn` glyph | **NEW** | `specs/e-08.html:374+`; recorded nowhere prior |
| `main` is protected; only protected branch | **CONFIRMED live** | API at `fd4c09d`, 1 of 36 |
| `test_db_integrity` 70/70 | **CONFIRMED** | run this session |
| "nine-job required set" | **REVISED** | §6.7 recommends 9 names; `ci.yml` has **12** jobs, deliberately omitting DB integrity, Tests, and the push-only commit-msg |
