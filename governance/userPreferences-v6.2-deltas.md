# userPreferences v6.2 — Adherence Logging Deltas

**Status:** repo-side reference copy. Live deployment: paste into claude.ai project settings.
**Source:** `workplan/adherence-attestation-build-2026-05-17.md` §4.2.
**Supersedes:** userPreferences-v6.1 (adds `<adherence_logging>` section; amends `<logging_tags>`).

---

## Delta 1: New tag in `<logging_tags>`

**Location:** `<logging_tags>` → under "Evidence trail" subsection.

**Add:**

```
- `[ADHERENCE-LOG — stage <N>: <name>]` (per-stage adherence record, multi-line; structure defined in `<adherence_logging>`)
```

---

## Delta 2: New section `<adherence_logging>`

**Location:** between `<audit_trail>` and `<token_reporting>`.

**Add the following section:**

```xml
<adherence_logging>
**Per-stage adherence record.** At every `<audit_trail>` stage boundary, emit an `[ADHERENCE-LOG]` block. This is the discipline log: structured, falsifiability-anchored, durable in the session record or relevant artifact (never chat-ephemeral).

**Entry format (≤10 lines per entry):**

[ADHERENCE-LOG — stage <N>: <name>]
  Rules in scope: <stable-id list, e.g. doctrine-check, adversarial-research, pmp>
  Per-rule: <id> <FIRED|NOT-FIRED|SKIPPED> — <one-line evidence or reason>
            <id> <...>
  Deviations: <explicit list with reason ≥20 chars, or "none">
  Bias direction: <one-line; how this report is likely shaded; ≥30 chars>
  Independent-reviewer counterclaim: <one-line; ≥30 chars>
  Verdict: <CLEAN | DEVIATION-LOGGED | NON-COMPLIANT>

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

---

## Owner deployment steps

1. Open claude.ai → Project Settings → User Preferences.
2. In `<logging_tags>`, under "Evidence trail", add the `[ADHERENCE-LOG]` tag line from Delta 1.
3. After `</audit_trail>` and before `<token_reporting>`, paste the full `<adherence_logging>` section from Delta 2.
4. Save. The version header should read `userPreferences-v6.2.md`.
5. New conversations in this project will pick up the changes; existing conversations retain v6.1 until refreshed.
