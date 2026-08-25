# S6 — SUBSTRATE, HOOKS, GATES AND THE WRITE PATH

Session: session_2026-08-25-pipeline-smoke-test-mobility
Agent: S6
Started: 2026-08-25 18:19 UTC
sha256(data/guidebook.db) BEFORE: 30a106692ab4110fe4e2082018eb256a325b2884d5740d3f62445b52c07dceaf
Scratch DB: $SMOKE/s6-substrate.db (copy of committed DB)

---

## 1. Dependency truth (CLAUDE.md §5 inversion)

### 1a. `.claude/hooks/ensure-deps.sh`
INVOKED   : `bash .claude/hooks/ensure-deps.sh`
STAGE     : substrate
EXIT      : 0   RUNTIME: 0.25s
READS     : `governance/check-registry.yaml` (`batteries:` block, lines 157-177) via inline
            `python3 -c "import yaml; d=yaml.safe_load(...)"`; falls back to literal
            `"pydantic jsonschema"` (script comment: "Fallback only if the registry could
            not be read") only if that parse fails — confirmed no second copy of the dep
            list exists outside this fallback string.
WRITES    : NONE (would `pip install` on a miss; none needed here)
EXAMINED  : 2 deps (union of `batteries:*.deps` = {pydantic, jsonschema}; PyYAML is not a
            declared dep of any battery — it's needed merely to parse the registry itself,
            and is Debian-managed/pre-installed per CLAUDE.md)
OUTPUT    : (silent — no MISSING, so the script's echo branches never fire; confirmed by
            reading the script: `[ -z "$MISSING" ] && exit 0` at line ~54)
FINDING   : PASS
LOCATION  : `.claude/hooks/ensure-deps.sh:36-45` (registry parse + union), `:47` (fallback
            literal, single second-home candidate, correctly gated to parse-failure only)
NOTE      : Confirmed — one home for the dep list (`governance/check-registry.yaml`
            `batteries:*.deps`), read live every session start, no drifted duplicate.
            pydantic 2.13.4, jsonschema 4.26.0 already present in this container (not
            installed by this run).

### 1b. requirements.txt vs registry batteries: block — disagreement audit
INVOKED   : `grep -n "^batteries:" -A 40 governance/check-registry.yaml`; `cat -n requirements.txt`
STAGE     : substrate
EXIT      : n/a (read-only greps)
READS     : `governance/check-registry.yaml:157-177`, `requirements.txt:1-9`
WRITES    : NONE
EXAMINED  : 7 batteries (syntax, structure, data, db_integrity, tests, schema, governance,
            attestation, research, render — 10 rows, `deps:` populated on 4 of them) vs 2
            requirements.txt package lines
FINDING   : FAIL (documents disagree — exactly as CLAUDE.md itself already says, confirmed
            independently)
LOCATION  : Disagreement 1 — `requirements.txt:9` pins `PyYAML==6.0.3`; no battery in
            `governance/check-registry.yaml:157-177` declares `PyYAML`/`yaml` as a `deps:`
            entry anywhere (only `pydantic` at :173-174,176 and `jsonschema` at :175-176 are
            declared). `requirements.txt` names a package the registry's own dependency
            contract never asks for.
            Disagreement 2 — `governance/check-registry.yaml:175` (`attestation`) and `:176`
            (`research`) both declare `jsonschema` as a dep; `requirements.txt:1-9` never
            mentions `jsonschema` at all — it is entirely absent from the second home.
NOTE      : Both disagreements are the ones CLAUDE.md's §5 box already names, confirmed by
            direct inspection with line numbers rather than taken on faith. `requirements.txt`
            is inert in this container (installing from it is explicitly forbidden — PyYAML
            pin conflicts with the Debian-managed 6.0.1) so the drift is latent, not currently
            harmful, but it is a second, disagreeing home for a fact rule 5 says should have one.

### 1c. Blocking/advisory count WITH deps present (`scripts/run_checks.py --all --explain`)
INVOKED   : `python3 scripts/run_checks.py --all --explain`
STAGE     : substrate
EXIT      : 1   RUNTIME: 40.5s
READS     : `governance/check-registry.yaml` (all 63 non-quarantined checks), entire repo
            tree per-check
WRITES    : NONE (checks are read-only in this mode; `render_audit_browser`,
            `test_graph_audit` etc. write only to their own tmp dirs)
EXAMINED  : 63 of 63 registered checks (4 quarantined, never selected — matches header
            "selected 63 of 63 registered checks (4 quarantined, never selected)")
OUTPUT    :
```
PASS: 49   FAIL: 6   NONE(NOTHING-IN-SCOPE): 8
FAILED: validate_pydantic_schemas (advisory), retired_vocabulary (advisory),
        attestation_presence (BLOCKING), validate_reasoning (advisory),
        test_verification_pipeline (advisory), context_map_fresh (advisory)
NOTHING-IN-SCOPE (8): validate_evidence_state, validate_verification_consistency,
  attestation_schema, attestation_verdict, population_integrity_audit, pmp_audit,
  reasoning_doc_citations_audit, check_rendered_docs
  BLOCKING and vacuous (4): validate_evidence_state, validate_verification_consistency,
  attestation_schema, check_rendered_docs
BLOCKING failures (1): attestation_presence
RESULT: FAIL
```
FINDING   : FAIL — but with a load-bearing qualifier (see NOTE)
LOCATION  : `attestation_presence` blocking failure detail (output lines 119-126 of my
            captured run): `CHECK 0: missing attestation for
            sessions/session_2026-08-25-pipeline-smoke-test-mobility.md (expected
            attestations/sessions_session_2026-08-25-pipeline-smoke-test-mobility.json)`
NOTE      : **CLAUDE.md's own table ("with pydantic: 0 blocking, 4 advisory -> PASS, 50
            green", stamped `d6ef7e9`, 2026-08-25) is itself now drifted** — confirmed via
            `git merge-base --is-ancestor d6ef7e9 HEAD` (true) and
            `git rev-list --count d6ef7e9..HEAD` = **36** intervening commits on the same
            calendar day, including the ACT 1–3/2a-2c write-path consolidation. This is
            failure mode (b) from CLAUDE.md §2, caught in the file meant to warn against it.
            Of my 6 FAILs: the 1 BLOCKING one (`attestation_presence`) is a **correct, working
            gate** reacting to this smoke-test session's own untracked
            `sessions/session_2026-08-25-pipeline-smoke-test-mobility.md` (created by the
            session harness before this agent's first Bash call — confirmed present in the
            very first `git status --short` of this run) lacking an attestation — exactly
            what rule §0.2 requires it to catch, not a dependency or repo-health defect. The
            5 advisory FAILs (`validate_pydantic_schemas`, `retired_vocabulary`,
            `validate_reasoning`, `test_verification_pipeline`, `context_map_fresh`) are
            pydantic-present, i.e. **not** the §5-documented dependency-absence failure mode —
            they are ordinary content/freshness drift accumulated across the 36 commits since
            the table was written, and are advisory so do not block. Net: **dependency
            presence claim is confirmed correct** (no blocking failure traces to a missing
            package); the specific 0-blocking/4-advisory figures are stale within the same day.

