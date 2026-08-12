# DR-2026-08-12 — Rename the skill `cell-curator` → `specification-curator`

**Status:** OPERATIVE — 2026-08-12.
**Decision by:** Owner instruction 2026-08-12 ("correct skill file"), following the schema rename
recorded in `DR-2026-08-12-specification-rename-and-replay-order` (D-0158).
**Category:** D-OP. **Delegation:** DG-NON — owner-directed; captured, not originated.
**Amends:** `references/skill-registry.md`, `references/effort-guide.md`,
`scripts/audit/adherence_log_audit.py`, `governance/retired-vocabulary.yaml`.

---

## 1. The decision

`skills/cell-curator_SKILL.md` → `skills/specification-curator_SKILL.md`, and the skill identifier
`cell-curator` → `specification-curator`.

The skill exists to populate the per-(item × population) record. That record is now a
**specification** (D-0158); the skill naming it a "cell" was the last live surface teaching the
retired word as an instruction rather than as history.

## 2. The departure from the registry's own rename process — stated plainly

`references/skill-registry.md` §"Identifier stability" specifies three steps. Steps 1 and 3 are
performed: this record, and lockstep updates to the skill file, the effort guide, the audit rule
map and the vocabulary register.

**Step 2 is deliberately not performed.** It calls for a timestamped migration that *rewrites every
existing `attestations/*.json`* to use the new identifier. Two committed attestations cite
`cell-curator`:

- `attestations/sessions_session_2026-08-12-commit-91-review-and-corridor-walk.json`
- `attestations/sessions_handoff-next-session.json`

Rewriting them would make a committed adherence log claim a session invoked a name that did not
exist on its date. That is the same class of act as editing a dated audit — and this session was
pulled up for exactly that earlier today, having overwritten
`audits/2026-08-12-pipeline-probe-log.md` with a false as-of stamp. A rule that requires falsifying
the record to stay green is the rule that should bend.

**The registry already provides the alternative and names it as such.** `EXTRA_RULE_IDS` in
`scripts/audit/adherence_log_audit.py` is described in the registry as the ratified extension point
that "accepts a non-skill or historical-alias identifier **without rewriting past attestations**."
`cell-curator` is registered there as **Category C — renamed predecessors**, a new category added
here because Categories A (cross-cutting rules) and B (variant aliases, "NOT renamed") both
mis-describe it. Check #3 resolves both existing citations; verified by running the audit.

The registry's §"Renames performed" table now records the rename and this departure, so the next
session reads the exception rather than re-deriving it.

## 3. Alternatives considered and refused

1. **Follow step 2 as written.** Refused above.
2. **Leave the skill named `cell-curator`.** Refused: it is an instruction file. A skill telling the
   next session to write "cell records" produces a query against a table that does not exist —
   which is precisely the failure the retired-vocabulary register exists to prevent.
3. **Rename the file but keep the identifier.** Refused: the identifier is the thing cited, and a
   file whose name and `name:` field disagree is a new trap rather than a fix.
4. **Amend the registry's step 2 to make attestation-rewriting optional in general.** Not done here
   — that is a broader governance change about record immutability, and it deserves its own record
   rather than being smuggled in as a side effect of one rename. This DR takes the exception for
   this rename only.

## 4. Verification

`python3 scripts/audit/adherence_log_audit.py` → **No issues** (check #3 resolves `cell-curator`
via `EXTRA_RULE_IDS`; check #4 resolves every evidence path).

## 5. Reversal

By a new dated Decision Record and a forward change, never by rewriting this one or the two
attestations that cite the former identifier.
