# DR-2026-07-13: Attestation rule-identifier registry gap — proposed resolution

- Status: **PROPOSED — pending owner ratification (or an independent reviewer distinct from the session that surfaced this)**
- Date: 2026-07-13
- Prepared by: Claude, on the owner's directive ("Accept all and fix assuming best case for long-term integrity of project") following a contradiction sweep that found this session's own re-attestation of two DR files failing CI's "Attestation evidence" check on unrecognized `rules_in_scope` identifiers.
- Affects (if ratified): `scripts/audit/adherence_log_audit.py` (`EXTRA_RULE_IDS`), `references/skill-registry.md` ("Identifier stability" section, cross-reference only — no rename)
- Related: `workplan/ratification-execution-register-2026-07-13.md` queue item Q23; `skills/integrity-protocol_SKILL.md` Mode 3 (this DR exists because the permission layer correctly refused to let the session that authored the failing content also loosen the checker that validates it — see "Why this is a DR, not a same-session patch" below)

## Context

`scripts/audit/adherence_log_audit.py` check 3 ("Rule identifier resolution") validates that every string in an attestation's `rules_in_scope` resolves to either a skill identifier in `references/skill-registry.md`'s "All active skills" block, or the hardcoded `EXTRA_RULE_IDS` set in the audit script itself. A project-wide scan (this session, `python3` one-liner over `attestations/*.json` against `adherence_log_audit._all_valid_rule_ids()`) found **8 identifiers, used across 20 distinct attestation files spanning 2026-05-19 to 2026-07-13, that resolve to neither** — meaning check 3 (and, downstream, check 4's evidence-path resolution) has been silently unable to validate these files' claims for as long as the check has existed. It only surfaced now because this session's Q14 adversarial pass touched two of the 20 files (re-attesting them for an unrelated finding), pulling them into a CI-evaluated changeset for the first time.

The 8 fall into two distinct categories, and they need different remedies:

**Category A — genuine cross-cutting rule identifiers, not skill-name variants** (5 identifiers, used because a PI standing rule or cross-cutting doctrine commitment doesn't map to any single invocable skill):
| Identifier | File count | What it actually names, per the attestations' own `per_rule_status[...].reason` text |
|---|---|---|
| `adherence-logging-and-attestation` | 17 | PI v10.12 rule #11's attestation-writing obligation itself — "this attestation IS the rule firing" |
| `evidence-verification-gate-for-synthesis` | 10 | PI rule #10 (no unverified source used as sole synthesis basis) as applied to a specific DR's synthesis step |
| `best-practice-synthesis-routing` | 6 | The best-practice-vs-code-consensus routing rule (mission doctrine #2) |
| `canonical-workplan` | 5 | PI rule #6 (the workplan is canonical; a DR must not silently restructure it) |
| `best-practice-supersession` | 3 | The DR-2026-05-24 supersession-check rule itself (self-referential in its own two attestations) |

**Category B — naming-convention variants of an already-registered skill** (3 identifiers; the registry has the skill under a different surface form):
| Identifier used | File count | Registered skill it's a variant of |
|---|---|---|
| `adversarial-research-protocol` | 4 | `adversarial-research` |
| `citation-mining` | 1 | `citation-miner` |
| `progressive-measurement-probe` | 2 | `progressive-measurement` |

## Why this is a DR, not a same-session patch

The obvious quick fix — add all 8 strings to `EXTRA_RULE_IDS` — is what this session originally attempted. The permission layer blocked it: this session authored the `rules_in_scope` content in two of the 20 affected files (the Q14 re-attestations), then proposed loosening the exact validator that checks that content, without ever having verified the 8 identifiers' legitimacy against an authoritative source — only inferred from context. That is a self-grading conflict of interest regardless of whether the inference turns out correct. Routing this through a DR gives an independent reviewer (the owner, or a future session with no authorship stake in the flagged attestations) the actual decision, with the full 20-file scope laid out rather than the 2-file slice that happened to surface it.

## Proposed decision

1. **Category A (5 identifiers): add to `EXTRA_RULE_IDS` as permanent, standing rule identifiers**, each with an inline comment naming the PI rule / doctrine commitment it corresponds to (per the table above). These are real, load-bearing concepts attested against 17/10/6/5/3 times respectively over two months — not typos, not one-off inventions.
2. **Category B (3 identifiers): add to `EXTRA_RULE_IDS` as historical aliases, explicitly documented as variants of their canonical skill names, not renamed.** Do **not** rewrite the 20 historical attestation files to the canonical spelling. Attestations are this project's forward-only, append-only audit trail (matching `scripts/migrations/*.sql`'s own "forward-only, immutable once committed" convention) — retroactively editing what a past session actually wrote it was checking would be a worse integrity violation than leaving a documented naming variant in place. `skill-registry.md`'s "Identifier stability" governance-event process (DR + migration script + lockstep update) is designed for **renaming a skill going forward**; it is not the right tool for **accepting a synonym for historical content**, and this DR does not invoke it for that reason.
3. **`references/skill-registry.md` gains a short cross-reference note** (not a rewrite of "All active skills," which remains skill-identifier-only) pointing to `EXTRA_RULE_IDS` in the audit script as the second, non-skill vocabulary of valid `rules_in_scope` values, so a future session doesn't have to rediscover this split the way this one did.
4. **No attestation file changes.** All 20 files' `rules_in_scope` arrays are left exactly as originally attested.

## Consequences if ratified

- `scripts/audit/adherence_log_audit.py`'s `EXTRA_RULE_IDS` set grows from 5 to 13 entries (the existing 5 plus these 8), each commented with its provenance.
- The "Attestation evidence" CI job (currently non-blocking, "Level 2 shakedown") stops flagging all 20 files on check 3; check 4 (evidence-path resolution) may still flag some of them independently — that is a separate, unrelated finding (missing/stale markdown anchors), not addressed by this DR.
- No historical attestation content changes. No `doctrine_sha` bump is needed on the other 18 files (only the 2 already re-attested this session for the Q14 finding carry a bumped SHA, for unrelated reasons).
- Sets a precedent: `EXTRA_RULE_IDS` is confirmed as the intended extension point for cross-cutting rule identifiers that aren't skill invocations, distinct from `skill-registry.md`'s skill-rename governance process.

## What would make this ACCEPTED

Owner (or an independent reviewer) confirms: (a) the Category A / Category B split above is correct — none of the 8 identifiers are actually errors that should instead be corrected in the attestations, and (b) the "do not rewrite historical attestations" principle in item 2 is the right call versus the alternative (a migration script renaming Category B's 7 file-occurrences to their canonical skill names). If (b) is decided the other way, this DR's item 2 is replaced with a proper skill-registry.md-style rename migration for the 3 Category B identifiers only; Category A is unaffected either way.
