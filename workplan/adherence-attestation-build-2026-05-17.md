# Adherence Attestation System — Build Workplan

**Target repo path:** `workplan/adherence-attestation-build-2026-05-17.md`
**Authored:** 2026-05-17
**Status:** PROPOSED — pre-execution; first artifact lands in Session 1 of the next chat.
**Source:** consolidated from the multi-turn design cycle on 2026-05-17 (Pass 2a artifact specs, Pass 2b corrections + test matrix + execution gates, Pass 3 verdict + findings A/B/C).
**Relation to prior plan:** addresses the structural weakness in Layer 2 of `audits/_archived/remediation-plan_session_2026-05-15a.md` (level-1 text-rule doctrine-check skill, which the prior plan's own enforcement-spectrum makes "low reliability") by replacing it with cryptographic doctrine-SHA token + structured attestation file + audit-script enforcement at GitHub Actions level 4.

This workplan IS the spec. The source chat's design cycle is complete; no further design is needed; only execution.

---

## §0. Failure surface

| Origin | Item | Defense |
|---|---|---|
| `session_2026-05-15a` F1 | doctrine non-read | Layer B doctrine-SHA token (cryptographic; can't be pattern-matched) |
| F2 | near-overwrite of canonical doctrine | Bootstrap inventory line (governance edit, not in this workplan) + attestation schema validation |
| F3 | review-boundary confusion | Governance edit (not in this workplan) |
| F4 | read-without-integrate | Layer A `[ADHERENCE-LOG]` per stage + Layer B cross-reference validation |
| F5 | PMP-independence misread | Governance edit (not in this workplan) |
| Audit #1 | Layer 2 reproduces failure mechanism | Layer B cryptographic attestation (this workplan's central move) |
| Audit #2 | violates promotion path | Level 4 from day 0 on commit-msg + schema; level 2→4 shakedown gate on evidence check |
| Audit #3 | bootstrap-load insufficient | Attestation file + cross-reference validation |
| Audit #5 | no mid-execution checkpoint | Layer A `[ADHERENCE-LOG]` at every audit-trail stage boundary |
| Audit #7 | discipline-logging unaddressed | Layer A is the answer |
| Audit #9 | fuzzy trigger | Path-based triggers (synthesis-path regex), not category labels |
| Audit #10 | no success metric | Audit script + level-4 CI fail-rate signal |
| Audit #12 | compliance theater | Counterclaim Levenshtein uniqueness check + cross-reference validation |

Audit findings #4, #6, #8, #11 are governance edits to the prior remediation plan and are out of scope for this workplan.

---

## §1. Architecture — two layers

**Layer A — Discipline logging.** A preferences-level `[ADHERENCE-LOG]` tag and `<adherence_logging>` section in `userPreferences-v6.2.md`. Fires at every `<audit_trail>` stage boundary. Output durable in the session record or reasoning doc, never chat-ephemeral. Provides the structured self-evaluation record requested in the source chat ("a discipline logging protocol where Claude can evaluate itself in terms of adherence, not just a self-bias flag").

**Layer B — GitHub enforcement.** Four CI checks across two workflows:

| Check | Workflow | Level day 0 | Promotion |
|---|---|---|---|
| `commit-msg` doctrine-SHA token | `ci.yml` | 4 blocking | n/a |
| `attestation_schema` | `audit.yml` | 4 blocking | n/a |
| `attestation_evidence` | `audit.yml` | 2 (`continue-on-error: true`) | → 4 at Day 7 if gate met |
| `attestation_verdict` | `audit.yml` | annotation-only | never blocking |

**Composition.** Layer A produces the per-stage record during work; Layer B requires that record to materialize as a versioned attestation file at commit time. They are complementary, not redundant: Layer A catches in-session drift via in-context tagging; Layer B catches at-commit drift via cryptographic attestation. Mid-session work between commits is unprotected — stated limit in §3.

---

## §2. Policy decisions (locked)

| Issue | Decision | Reason |
|---|---|---|
| Doctrine self-modification SHA reference | Exempt token on doctrine-touching commits; require re-attestation of affected artifacts within `RE_ATTESTATION_WINDOW` commits (default 5) or by next session close, whichever first | The doctrine IS the read at that moment; what matters is downstream re-grounding |
| Scope | Triggers on `references/bpc-reasoning/`, `references/connection-reasoning/`, `decisions/`, and synthesis-bearing files under `sessions/` | Narrower scope produces Failure-4 pattern; broader is more honest |
| Backfill | Backfill-on-touch | Forward-only creates permanent two-tier corpus; full-backfill is unjustified tax against past work |
| NON-COMPLIANT semantics | Log-not-block. Self-reported NON-COMPLIANT generates PR comment / audit log entry; does NOT fail CI | Hard-failing the honest path incentivizes the dishonest path |
| Rule identifiers | Stable strings (e.g. `adversarial-research`, `pmp`), not numbers; rename = governance event with migration script | Avoids brittle hardcoding when PI rules renumber |

---

## §3. What this does NOT solve

Stated explicitly. Listed for traceability.

1. **Doctrine read but not integrated.** Token proves version-reference, not content engagement. Layer A discipline is the only defense; that defense degrades over long sessions per the meta-applicability rule in `<persistence_safeguards>`.
2. **Mid-session work between commits.** GitHub fires at commit boundaries; drafting before commit is unprotected.
3. **Single-author judgment quality.** Counterclaim self-check is partial; cross-author review is out of scope per architecture v2.3 `<scope_assumptions>`. Will need re-evaluation if contributor count grows past 1.
4. **Doctrine itself being wrong.** Adherence ≠ correctness. Session 6's doctrine-quality-review process is the orthogonal layer for this.
5. **Schema-satisfying but content-blind attestations.** Counterclaim Levenshtein check is partial; full mitigation requires periodic owner review (recommended cadence: §11).
6. **Compound gaming vulnerability — the irreducible limit.** A sufficiently lazy Claude can game the entire system in three coordinated moves: (a) run `git rev-parse HEAD:governance/mission-and-epistemics.md` to fetch the SHA without opening the file content; (b) write a Levenshtein-distinct but content-blind counterclaim that satisfies the min-length check without semantic engagement; (c) self-report `verdict: CLEAN` when the underlying work was doctrine-blind. None of the three is caught by any CI check. Owner spot-review of attestations is the irreducible mitigation.
7. **Cross-session memory failure.** Session N+1 inherits no in-context memory of session N's drift unless attestations and adherence logs are actively loaded at bootstrap. The system stores it durably; Claude must read it.

The honest framing: GitHub gives you the best non-human enforcement available. It does not replace owner review. The system makes adherence cryptographically attestable; only owner review makes adherence true.

---

## §4. Spec — 9 artifacts

### §4.1 `schemas/attestation.schema.json`

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Adherence Log Attestation",
  "type": "object",
  "required": [
    "schema_version", "session", "artifact", "doctrine_sha",
    "rules_in_scope", "per_rule_status", "deviations",
    "bias_direction", "independent_reviewer_counterclaim", "verdict"
  ],
  "properties": {
    "schema_version": { "type": "string", "pattern": "^\\d+\\.\\d+$" },
    "session":   { "type": "string", "pattern": "^session_\\d{4}-\\d{2}-\\d{2}[a-z]?(-.*)?$" },
    "artifact":  { "type": "string", "pattern": "^(references/bpc-reasoning|references/connection-reasoning|decisions|sessions)/.+\\.md$" },
    "doctrine_sha": { "type": "string", "pattern": "^[a-f0-9]{7}$" },
    "rules_in_scope": {
      "type": "array", "minItems": 1,
      "items": { "type": "string", "pattern": "^[a-z][a-z0-9-]+$" },
      "description": "Stable rule identifiers per references/skill-registry.md, not rule numbers"
    },
    "per_rule_status": {
      "type": "object",
      "patternProperties": {
        "^[a-z][a-z0-9-]+$": {
          "type": "object", "required": ["status"],
          "properties": {
            "status":        { "enum": ["FIRED","NOT-FIRED","SKIPPED"] },
            "evidence_path": { "type": "string" },
            "reason":        { "type": "string", "minLength": 10 }
          },
          "allOf": [
            { "if": { "properties": { "status": { "const": "SKIPPED" } } },
              "then": { "required": ["reason"] } },
            { "if": { "properties": { "status": { "const": "FIRED" } } },
              "then": { "required": ["evidence_path"] } }
          ]
        }
      },
      "additionalProperties": false
    },
    "deviations": {
      "type": "array",
      "items": {
        "type": "object", "required": ["rule","reason"],
        "properties": {
          "rule":   { "type": "string", "pattern": "^[a-z][a-z0-9-]+$" },
          "reason": { "type": "string", "minLength": 20 }
        }
      }
    },
    "bias_direction":                    { "type": "string", "minLength": 30 },
    "independent_reviewer_counterclaim": { "type": "string", "minLength": 30 },
    "verdict": { "enum": ["CLEAN","DEVIATION-LOGGED","NON-COMPLIANT","REVERT"] }
  },
  "additionalProperties": false
}
```

Files at `attestations/<artifact-slug>.json`. Slug derived from artifact path: e.g., `references/bpc-reasoning/room-acoustic-performance.md` → `attestations/bpc-reasoning_room-acoustic-performance.json`.

### §4.2 `userPreferences-v6.2.md` deltas

**Add to `<logging_tags>` under "Evidence trail":**

```
- `[ADHERENCE-LOG — stage <N>: <name>]` (per-stage adherence record, multi-line; structure defined in `<adherence_logging>`)
```

**New section, placed between `<audit_trail>` and `<token_reporting>`:**

```
<adherence_logging>
**Per-stage adherence record.** At every `<audit_trail>` stage boundary, emit an `[ADHERENCE-LOG]` block. This is the discipline log: structured, falsifiability-anchored, durable in the session record or relevant artifact (never chat-ephemeral).

**Entry format (≤10 lines per entry):**
```
[ADHERENCE-LOG — stage <N>: <name>]
  Rules in scope: <stable-id list, e.g. doctrine-check, adversarial-research, pmp>
  Per-rule: <id> <FIRED|NOT-FIRED|SKIPPED> — <one-line evidence or reason>
            <id> <...>
  Deviations: <explicit list with reason ≥20 chars, or "none">
  Bias direction: <one-line; how this report is likely shaded; ≥30 chars>
  Independent-reviewer counterclaim: <one-line; ≥30 chars>
  Verdict: <CLEAN | DEVIATION-LOGGED | NON-COMPLIANT>
```

**Falsifiability anchors.** Bias-direction and independent-reviewer-counterclaim are non-optional. Empty or boilerplate ("no significant counterclaim", "minimal bias") fail the spirit if not the letter — the audit script checks for text-similarity against prior commits' fields and flags duplicates.

**Verdict semantics.**
- CLEAN — all rules in scope fired, zero deviations.
- DEVIATION-LOGGED — one or more rules deviated; deviation explicit and reasoned.
- NON-COMPLIANT — one or more rules silently skipped, discovered post-hoc.
- REVERT — used only on commits that revert prior synthesis work.

NON-COMPLIANT does NOT auto-fail CI. Logged for owner review. Honest reporting must not be punished worse than dishonest reporting.

**Mid-session drift protection.** When draft work spans many stages before commit, the log accumulates. The commit later materializes a derived attestation file (`attestations/<artifact-slug>.json`) per PI standing rule. The audit log and the attestation are the same data at two granularities — the log is the running record, the attestation is the snapshot.

**Composition with `[SELF-AUTHORED — bias risk]`.** Self-authored flag is per-document. Adherence log is per-stage. Both apply; they serve different scales.
</adherence_logging>
```

### §4.3 `governance/project-instructions-v10_12.md` new standing rule #11

```
11. **Adherence logging and attestation.** Per `userPreferences-v6.2.md` `<adherence_logging>`. At every `<audit_trail>` stage boundary, emit `[ADHERENCE-LOG]` per the defined structure.

Commits modifying `references/bpc-reasoning/`, `references/connection-reasoning/`, `decisions/`, or synthesis-bearing files under `sessions/` MUST:
   (a) Include `[DOCTRINE: <7-char-sha>]` in the commit message, where the SHA matches `HEAD:governance/mission-and-epistemics.md`. Exempt when the commit itself modifies `governance/mission-and-epistemics.md`; in that case, affected downstream artifacts must be re-attested within RE_ATTESTATION_WINDOW (default 5) commits or by next session close, whichever first.
   (b) Add or update `attestations/<artifact-slug>.json` validating against `schemas/attestation.schema.json`. Backfill-on-touch: existing artifacts grandfather; first edit creates the attestation.

CI enforcement:
   - `ci.yml` `commit-msg` job — doctrine-SHA token validation (Level 4 blocking from day one).
   - `audit.yml` `attestation_schema` — JSON schema validation (Level 4 blocking).
   - `audit.yml` `attestation_evidence` — cross-reference rule-status to commit content (Level 2 → 4 after 7-day shakedown meeting the gate in §8 of workplan).
   - `audit.yml` `attestation_verdict` — NON-COMPLIANT count surfaced as PR comment / commit annotation; never blocking.

Audit script: `scripts/audit/adherence_log_audit.py` (Level 2). Skipping adherence logging while authoring synthesis content is a methodology-grade failure on the same severity as skipping rule #7 (adversarial-research) or rule #8 (PMP).
```

### §4.4 `.github/workflows/ci.yml` commit-msg extension

Add as a new step in the existing `commit-msg` job:

```yaml
- name: Doctrine-SHA token validation
  if: ${{ github.event_name == 'push' }}
  run: |
    set -euo pipefail
    CHANGED=$(git diff --name-only "${{ github.event.before }}" "${{ github.sha }}")
    SYNTHESIS_RE='^(references/bpc-reasoning|references/connection-reasoning|decisions|sessions)/'

    if ! echo "$CHANGED" | grep -qE "$SYNTHESIS_RE"; then
      echo "No synthesis paths touched — doctrine token not required."
      exit 0
    fi

    # Exempt: doctrine self-modification (re-attestation window opens; enforced by audit.yml)
    if echo "$CHANGED" | grep -q '^governance/mission-and-epistemics\.md$'; then
      echo "Doctrine commit — token exempt. Re-attestation required within RE_ATTESTATION_WINDOW commits."
      exit 0
    fi

    # Exempt: bot / automation authors
    AUTHOR=$(git log -1 --format=%ae "${{ github.sha }}")
    case "$AUTHOR" in
      *dependabot*|*github-actions*|*-bot@*) echo "Bot commit ($AUTHOR) — exempt."; exit 0 ;;
    esac

    # Exempt: merge commits
    PARENTS=$(git log -1 --format=%P "${{ github.sha }}" | wc -w)
    if [ "$PARENTS" -gt 1 ]; then
      echo "Merge commit — exempt."
      exit 0
    fi

    MSG=$(git log -1 --format=%B "${{ github.sha }}")
    TOKEN=$(echo "$MSG" | grep -oE '\[DOCTRINE: [a-f0-9]{7}\]' | grep -oE '[a-f0-9]{7}' | head -1 || true)
    EXPECTED=$(git rev-parse "HEAD:governance/mission-and-epistemics.md" | cut -c1-7)

    if [ -z "$TOKEN" ]; then
      echo "FAIL: commit touches synthesis paths; commit message must contain [DOCTRINE: <7-char-sha>]"
      echo "Expected token: [DOCTRINE: $EXPECTED]"
      exit 1
    fi
    if [ "$TOKEN" != "$EXPECTED" ]; then
      echo "FAIL: doctrine token [$TOKEN] does not match HEAD:governance/mission-and-epistemics.md ($EXPECTED)"
      echo "The doctrine has been updated since this commit was authored. Re-read and update the token."
      exit 1
    fi
    echo "PASS: doctrine token $TOKEN matches HEAD."
```

Re-attestation window is enforced by the audit script (§4.5 check #7), which derives the doctrine-change SHA from git history directly — no sidecar state file. This was a Pass 2b correction to the original Pass 2a design.

### §4.5 `scripts/audit/adherence_log_audit.py` — module spec

```python
"""adherence_log_audit.py — Level 2 audit for attestation files.

Checks performed (per PI v10.12 rule #11):

0. Attestation presence. For every synthesis-path file in the changeset,
   verify a corresponding `attestations/<slug>.json` is either also in the
   changeset OR already exists in the repo (backfill-on-touch).

1. Schema validation. Every file in attestations/ in the changeset
   validates against schemas/attestation.schema.json. Audit script reads
   attestation.schema_version and dispatches to the matching check suite.

2. Doctrine-SHA consistency. attestation.doctrine_sha matches the
   commit-message [DOCTRINE: ...] token of the commit that introduced
   or last modified the attestation.

3. Rule identifier resolution. Every key in rules_in_scope and
   per_rule_status resolves to a known stable identifier per
   references/skill-registry.md.

4. Evidence-path resolution. For per_rule_status entries with
   status=FIRED, evidence_path resolves to an extant file or
   git-ref. Path may be a file relative to repo root or a token of
   form db://<table>/<id-pattern> for DB-backed evidence.

5. Cross-reference per-rule evidence inference. For rules with
   automatable inference (rule 'pmp' → row in spec_value_probes;
   rule 'adversarial-research' → four gap fields populated for cited
   sources; rule 'jurisdictional-synthesis' → reasoning_doc_citations
   row per cell), verify that FIRED claims correspond to actual
   repository state.

6. Counterclaim uniqueness. bias_direction and
   independent_reviewer_counterclaim fields compared via normalized
   Levenshtein ratio against the same fields in the previous 10
   attestations. Ratio > 0.85 flags as suspected boilerplate.

7. Re-attestation window. Read git history for last commit touching
   governance/mission-and-epistemics.md (no sidecar state file).
   Count commits since that SHA. If > RE_ATTESTATION_WINDOW and any
   synthesis artifact has not been re-attested (attestation
   last-modified-SHA postdates last_doctrine_sha), FAIL.

8. Verdict-evidence consistency. verdict=CLEAN requires zero
   deviations and all rules_in_scope status=FIRED.
   verdict=DEVIATION-LOGGED requires at least one non-FIRED status
   or non-empty deviations array. verdict=NON-COMPLIANT is logged
   but does NOT exit non-zero (log-not-block per PI rule #11).

Exit codes: 0 = pass (or NON-COMPLIANT verdicts present but logged);
           1 = any other check failed.
DB path: data/guidebook.db (override via GUIDEBOOK_DB_PATH).
Repo root: resolved relative to __file__.
Constants: RE_ATTESTATION_WINDOW = 5 (default; configurable per workplan §5).
"""
```

Single `audit()` function, each check as a numbered routine. Reports formatted with `=` separators per the audit-script style convention (architecture v2.3 `<enforcement_spectrum>`). Selectable subset via `--check <name>` for use by individual CI jobs.

### §4.6 `.github/workflows/audit.yml` three new jobs

```yaml
attestation_schema:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - run: pip install jsonschema
    - name: Validate all changed attestations + presence
      run: |
        set -euo pipefail
        python scripts/audit/adherence_log_audit.py --check presence
        python scripts/audit/adherence_log_audit.py --check schema

attestation_evidence:
  runs-on: ubuntu-latest
  needs: attestation_schema
  continue-on-error: true   # Level 2 during shakedown; flip to false after Day-7 gate met
  steps:
    - uses: actions/checkout@v4
    - run: python scripts/audit/adherence_log_audit.py --check evidence

attestation_verdict:
  runs-on: ubuntu-latest
  needs: attestation_schema
  continue-on-error: true   # Never blocking by design
  steps:
    - uses: actions/checkout@v4
    - name: Surface NON-COMPLIANT verdicts
      run: |
        python scripts/audit/adherence_log_audit.py --check verdict > /tmp/verdict.txt || true
        if grep -q NON-COMPLIANT /tmp/verdict.txt; then
          echo "::warning::NON-COMPLIANT verdict present in attestation — see /tmp/verdict.txt"
          cat /tmp/verdict.txt
        fi
```

### §4.7 `references/skill-registry.md` — identifier-stability amendment (Pass 3 Finding A)

Add a new section at the top of the skill registry:

```
## Identifier stability

Skill identifiers in this registry are STABLE. They are the canonical
strings referenced from `attestations/*.json` files (per PI v10.12 rule #11)
and from rule cross-references throughout the project.

Renaming a skill identifier is a governance event that requires:
1. A DR documenting the rename rationale and migration plan.
2. A timestamped data-migration script at
   `scripts/migrations/data_<YYYYMMDDHHMMSS>_rename-skill-<old>-to-<new>.sql`
   (or `.py`) that rewrites every existing `attestations/*.json` file
   to use the new identifier.
3. Lockstep update of any skill files, audit-script rule maps, and
   PI standing rules referencing the old name.

The audit script `scripts/audit/adherence_log_audit.py` check #3 validates
that every rule identifier in an attestation resolves to a stable identifier
listed in this registry.
```

### §4.8 `.github/CODEOWNERS` — Pass 3 Finding C

```
# CODEOWNERS — owner sign-off required on changes to enforcement substrate.
# Single-author repo today; this file enforces a deliberateness gate
# regardless of contributor count.

/governance/                @jordanelias
/schemas/                   @jordanelias
/scripts/audit/             @jordanelias
/scripts/migrations/        @jordanelias
/.github/workflows/         @jordanelias
/.github/CODEOWNERS         @jordanelias
/references/skill-registry.md @jordanelias
```

### §4.9 Session 6 trio — doctrine-quality-review process

**`governance/doctrine-quality-review-process.md`** — defines:
- Triggers (any one fires): (a) 12 months since last review; (b) ≥3 attestations flag the same doctrinal commitment as ambiguous; (c) ≥10 commits to `governance/mission-and-epistemics.md` since last review; (d) owner discretion.
- Scope: are the seven commitments still right and complete? Does the eight-point test catch what it claims? Internal consistency on edge cases? Predictive validity against actual BPC work?
- Claude's role: structured-input only. On trigger, run `scripts/doctrine_review_input.py` to generate an input packet. Format defined in advance so Claude cannot shape input toward a preferred conclusion.
- Output: DR documenting findings; verdict `CLEAN | AMEND | REWRITE`; owner authors the verdict and any doctrine edit; frontmatter `last_quality_review` updates on close.
- Process: owner-led; Claude prepares input on trigger; owner reviews on cadence; DR closes the loop.
- Caveat: the trigger numbers (12 months, ≥3, ≥10) are first-pass; revisit after one review cycle with actual data.

**`scripts/doctrine_review_input.py`** — input-packet generator:
- Sample N recent attestations (default 20), weighted toward DEVIATION-LOGGED, NON-COMPLIANT, and Levenshtein-flagged.
- Enumerate cases where reasoning docs cited doctrinal ambiguity (regex scan for `[DOCTRINE-AMBIGUOUS]` or similar markers).
- Surface candidate self-contradictions via automated scan against the seven commitments.
- Output a structured packet at `audits/doctrine-review-input_<YYYY-MM-DD>.md` for owner consumption.

**`governance/mission-and-epistemics.md` frontmatter amendment** — add field:

```yaml
last_quality_review: 2026-05-17  # Initial value: set to adoption date
```

---

## §5. Configurable constants

| Constant | Default | Defined in | Revisit |
|---|---|---|---|
| `RE_ATTESTATION_WINDOW` | 5 commits | `scripts/audit/adherence_log_audit.py` | After 60 days of observed commit cadence; DR at adoption justifying default |
| Levenshtein boilerplate threshold | 0.85 ratio | audit script check #6 | After 100+ attestations accumulate |
| Levenshtein comparison window | previous 10 attestations | audit script check #6 | Year 2; consider embedding-based similarity replacement |
| Schema version | `"1.0"` | `schemas/attestation.schema.json` | When schema evolves; DR-class change |
| Owner attestation spot-review rate | 1-in-20 | governance practice, not encoded | After first full review cycle |

The first three are unjustified first-pass numbers per Pass 3 Finding B. Document this honestly in the adoption DR. Adjustment is cheap; the default lets execution proceed.

---

## §6. Build plan — 6 sessions

Each session is bounded, single-layer, independently verifiable. One chat per session is the recommended topology; Sessions 2 and 3 can batch if context permits.

### Session 1 — Foundation

**Artifacts:** §4.1 schema · §4.2 userPreferences deltas · §4.7 skill-registry amendment.

**Commits (3):**
1. `governance: add schemas/attestation.schema.json [TS]`
2. `governance: amend skill-registry.md with identifier-stability clause [TS]`
3. `governance: deploy userPreferences-v6.2.md adherence-logging section [TS]` (repo-side copy; live deployment is paste into claude.ai project settings)

**Verification:**
- `python -c "import json; json.load(open('schemas/attestation.schema.json'))"` succeeds.
- `jsonschema --validate` against a hand-rolled minimal example produces no errors.
- `references/skill-registry.md` contains the new "Identifier stability" section.
- Next session's bootstrap successfully loads the new preferences.

**Gate to Session 2:** all three artifacts committed cleanly; no CI failures.

### Session 2 — PI bump + audit script (Level 2) + CODEOWNERS

**Artifacts:** §4.3 PI rule #11 · §4.5 audit script · §4.8 CODEOWNERS.

**Commits (3):**
1. `governance: add .github/CODEOWNERS [TS]`
2. `governance: ship scripts/audit/adherence_log_audit.py at Level 2 [TS]`
3. `governance: deploy PI v10.12 with standing rule #11 [TS]` (repo-side copy; live deployment is paste into claude.ai project settings)

**Verification:**
- `python scripts/audit/adherence_log_audit.py --check schema` against an empty `attestations/` directory exits 0.
- `python scripts/audit/adherence_log_audit.py --check presence` against a no-synthesis-change diff exits 0.
- CODEOWNERS pattern resolves (GitHub UI shows the protected paths).
- PI v10.12 is the operative project-instructions document in claude.ai project settings.

**Gate to Session 3:** audit script runs without errors against current repo state; PI live.

### Session 3 — CI commit-msg layer (Level 4 from day 0)

**Artifacts:** §4.4 ci.yml extension.

**Commits (1):**
1. `governance: add commit-msg doctrine-token check [TS]` — this commit itself touches no synthesis paths, so it lands token-free.

**Verification:**
- A test commit on a side branch that touches `references/bpc-reasoning/<any>.md` WITHOUT the token fails CI at `commit-msg`.
- Same commit WITH a correct `[DOCTRINE: <7-char>]` token passes.
- Doctrine-only commit (touches `governance/mission-and-epistemics.md` only) is exempt from the token requirement.

**Gate to Session 4:** commit-msg check correctly blocks and allows per the test scenarios above. Revert test commits before proceeding.

### Session 4 — Audit workflow (Level 2 shakedown for evidence check)

**Artifacts:** §4.6 audit.yml three jobs.

**Commits (1):**
1. `governance: add attestation_schema + attestation_evidence + attestation_verdict jobs [TS]`

**Verification:**
- `attestation_schema` blocking from day 0; no false positives on the introducing commit (which touches no attestation files).
- `attestation_evidence` runs with `continue-on-error: true`; emits report but does not block.
- `attestation_verdict` runs as annotation-only.
- A test commit creating a minimal valid attestation file passes all three.
- A test commit creating a schema-invalid attestation file fails `attestation_schema`.

**Gate to Session 5:** Day-7 shakedown window begins. Track commits during the window.

### Session 5 (Day 7+) — Promotion gate review

**Process:** Walk the four criteria from §8 of this workplan. Pass all four → flip `attestation_evidence` to `continue-on-error: false` (blocking). Fail any → DR documenting miss + 7-day extension; loop.

**Commits (1 if pass, 1 if extension):**
- Pass: `governance: promote attestation_evidence to Level 4 blocking [TS]` + `decisions/DR-YYYY-MM-DD-attestation-promotion.md`.
- Extension: `decisions/DR-YYYY-MM-DD-attestation-shakedown-extension-N.md`.

**Verification:**
- All four criteria evaluated against the actual commit log of the shakedown window.
- DR cites specific evidence per criterion.

**Re-open trigger:** three consecutive extensions without promotion → re-open the design via a new DR-class workplan. Schema or audit logic has a problem.

### Session 6 — Doctrine quality review process

**Artifacts:** §4.9 trio.

**Commits (3):**
1. `governance: add doctrine-quality-review-process.md [TS]`
2. `governance: add scripts/doctrine_review_input.py [TS]`
3. `governance: amend mission-and-epistemics.md frontmatter with last_quality_review [TS]` — note: this commit modifies the doctrine, triggering the re-attestation window if any attestations exist by this point.

**Verification:**
- `python scripts/doctrine_review_input.py --dry-run` generates a packet to stdout without errors.
- Frontmatter parses (YAML validates).
- Re-attestation window correctly opens (audit script's check #7 reports the window).

**Gate:** none — this is the final session of the build. Subsequent doctrine-quality reviews run on trigger per §4.9, not as part of this build workplan.

---

## §7. Total scope

| Session | Commits | Layer |
|---|---|---|
| 1 | 3 | Foundation |
| 2 | 3 | Audit substrate |
| 3 | 1 | CI commit-msg |
| 4 | 1 | CI audit jobs |
| 5 | 1 (or extension cycles) | Promotion |
| 6 | 3 | Doctrine quality |
| **Total** | **~12** | |

---

## §8. Day-7 promotion gate criteria (Session 5)

All four must hold to flip `attestation_evidence` to blocking:

1. **Zero false-positive blocks** against legitimate commits during the 7-day window. (Since the job runs `continue-on-error: true`, "block" here means the job reports failure on a commit that should have passed; verify the report content, not the exit status.)
2. **`schemas/attestation.schema.json` unchanged** for the full 7 days. Any emergency schema revision restarts the clock.
3. **At least 5 commits** exercised the synthesis path during the window. Fewer commits = insufficient signal.
4. **Audit script caught at least one real skip attempt OR produced clean output across all 5+ commits.** Either result is acceptable; the criterion fails only if the audit script crashed, produced ambiguous output, or behaved inconsistently across commits.

If any criterion misses: extend shakedown by 7 days, document in `decisions/DR-YYYY-MM-DD-attestation-shakedown-extension-N.md`, repeat Session 5 a week later.

If three consecutive extensions: re-open the design. Schema or audit logic has a structural problem; new DR-class workplan needed.

---

## §9. Bootstrap and backfill handling

**Bootstrap commit (Session 1's first commit).** Touches only `schemas/`, no synthesis paths. Lands token-free. The very next commit touching a synthesis path (likely not until well after Session 4 when the system is live) is the first real exercise.

**Backfill posture.** Existing reasoning docs, connection-reasoning docs, decisions, and session records grandfather. The audit script does NOT walk extant artifacts at install time. The first edit to an existing artifact triggers attestation creation at that point. Commits that touch an existing artifact's frontmatter only (no claim changes) still require the minimum-scope attestation: `verdict: CLEAN, rules_in_scope: ["doctrine-check"]`.

**First-real-exercise expectations.** Until a synthesis-path commit lands, none of the CI checks fire on substantive paths. The first commit touching a synthesis path is the first real test of the entire stack — expect surprises and budget time for them.

---

## §10. Handoff to next chat

1. Open new chat in this project (`jordanelias/guidebook`).
2. Bootstrap will load `project-standards.md` and `skill-registry.md` per PI v10.11.
3. First message: paste this workplan in full, or reference it as `workplan/adherence-attestation-build-2026-05-17.md` if you commit it to the repo before opening the new chat (recommended).
4. Instruct: `Execute Session 1.` Session 1 is bounded at 3 commits and fits comfortably in one chat with context to spare.
5. Subsequent sessions: one chat per session is the safe default. Sessions 2 and 3 can batch if context after Session 2 is comfortably under 50%.

**Recommended pre-Session-1 step:** commit THIS workplan to the repo at `workplan/adherence-attestation-build-2026-05-17.md` before opening the Session 1 chat. That way the next chat's bootstrap picks it up naturally and the spec is versioned, not chat-only.

When Session 5 promotion lands and `attestation_evidence` flips to blocking, the system is fully operational. Session 6 (doctrine-quality-review) is the orthogonal layer for doctrine quality and can run on its own cadence after that.

---

## §11. Open questions remaining for owner

Decisions deferred to owner, not blockers — sessions can execute with the defaults and adjust via DR.

1. **`RE_ATTESTATION_WINDOW` initial value.** Default 5 is first-pass per Pass 3 Finding B. Adopt with explicit caveat that the number is unjustified; revisit after 60 days of observed commit cadence and author a DR justifying the final value.
2. **Doctrine-quality-review trigger numbers** (12 months, ≥3 ambiguity flags, ≥10 doctrine commits). Also unjustified first-pass. Revisit after one review cycle with actual data.
3. **Schema versioning meta-process.** Schema changes are DR-class governance events. Cadence for proactive schema review (annual? on event?) is unspecified by this workplan; raise as a separate governance question if it becomes relevant.
4. **Owner attestation spot-review cadence.** Recommended 1-in-20 spot check plus 100% of NON-COMPLIANT and Levenshtein-flagged. Confirm or revise. This is the irreducible mitigation for the compound gaming vulnerability per §3 #6.
5. **Doctrine quality cadence vs. content.** Session 6 builds the *process* for doctrine-quality review. It does not schedule the first review. Decide separately when the first cycle runs (suggestion: 6 months after adoption, to accumulate enough attestation data for the input packet to be useful).

---

## §12. Why this workplan exists in its current form

The source chat drifted into seven turns of nested governance design before the user surfaced the alarm that NO build plan had been authored. The design itself was sound — but the absence of a sessioned, actionable execution plan made the entire design feel like ceremony rather than work.

This workplan is the spec-to-execution bridge that should have been the natural endpoint of the design cycle. It exists as one durable artifact precisely so future Claude in a new chat does not need to re-derive any of the design from the source chat's transcript — paste this, execute Session 1, proceed.

The honest meta-note: design without an execution plan is the failure mode every PI standing rule and architectural pattern in this project is trying to avoid. Calling that out explicitly here so the next chat does not repeat it.
