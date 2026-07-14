# SKILL: integrity-protocol — three-mode implementation of the adversarial-review lessons
**Status:** ACTIVE — ratified by owner directive 2026-07-13 (`decisions/RATIFICATION-RECORD-2026-07-13.md`; DR ACCEPTED)
**Derived from:** the two adversarial passes of 2026-07-12/13 (41 findings — RECOUNTED: 18 in `decisions/DR-2026-07-12-evidence-architecture-unification.md`'s revision history + 23 in `decisions/DR-2026-07-13-value-genealogy-and-derivation-handshake.md`'s — across work that had passed its authors' own checks; fix-by-fix records in those same revision histories). The empirical base: REPORTED-BY: the two DRs' own revision-history summaries — defects clustered at the seam between claims and artifacts, more often than in the artifacts themselves (this document has not independently re-tallied all 41 to confirm zero pure-artifact defects; treat "never" from the original phrasing as the source DRs' characterization, not a re-verified absolute).
**Applies to:** every session producing synthesis-path artifacts (decisions/, governance/, references/ methodology or BPC content, workplan commitments) and every session requesting owner ratification.

---

## Mode 1 — Preventative prior structuring (before authoring)

Make the recurring defect classes structurally hard to write, rather than hoping to catch them later.

1. **Typed assertions.** Every checkable claim in a deliverable is authored with its warrant class, using these markers inline or in a closing Assertions Inventory:
   - `VERIFIED-BY: <command/artifact path>` — was actually run/read this session; the warrant must exist.
   - `PREDICTED` — an expected outcome; must name what falsifies it and who wins on divergence (per the worked example's §8 rule: divergence is a finding against the predicting document).
   - `REPORTED-BY: <source>` — relayed, not verified; the caveat travels with the claim (a value without its confidence marker is a different, false claim).
   - `RECOUNTED: <command>` — for every absolute/total (*all, none, never, only, every, first, complete, N of M*): the mechanical recount that was run, not a recollection. Absolutes are cheap to check and disproportionately wrong (REPORTED-BY: the source DRs' revision histories name three false-absolute findings among the 41; not independently re-tallied here — see Self-application below for a same-session, independently-verified instance of this exact failure mode).
2. **Caveats welded to values at the schema level.** No template or schema may carry a value field without its confidence/caveat field beside it (the determination-tuple and REGISTER_MAP pattern). Distillation strips caveats by default; structure must make the caveat part of the value.
3. **Verifiers are born with selftests.** Any new checker/validator ships with a mutation harness in the same commit; "passes" is meaningless until "fires on tampered input" is demonstrated. A verifier that has only ever passed is unverified.
4. **Self-application clause.** Any document proposing a rule or discriminator must contain a section applying it to (a) the document itself and (b) its flagship example — the two adversarial rounds' most instructive catches were reflexive (a register map violating its own invariant; a genealogy headline failing its own independence query).
5. **Source preservation before distillation.** Agent dossiers and research-sweep outputs are committed (sessions/, with attestation) *before* the distillation is authored, so every distilled claim is auditable against a fixed source — never against a transient message.

## Mode 2 — Live rules-processing docket (during authoring)

A running docket processed as work happens — the failure mode of end-of-session review is that the author no longer remembers which claims were verified.

1. **Mechanical docket:** `scripts/audit/claims_docket.py generate` scans the working diff's prose for trigger patterns (absolutes/totals; verification verbs — *verified, demonstrated, confirmed, preserved, proven, tested, all checks pass*; quoted quantities) and emits a docket file with one line per triggered claim. `claims_docket.py check` exits 1 while any line lacks an annotation from the Mode-1 warrant vocabulary. The docket commits alongside the work — it is the audit trail Mode 3 consumes.
2. **Docket cadence:** processed at every phase commit, not at session end. A phase commit with unannotated docket lines is not ready.
3. **Live triggers beyond the scanner** (author-processed, docket-logged):
   - Favouring a conclusion → log the strictest test applied *to the favoured conclusion specifically* (scrutiny allocation inverts naturally; invert it back — the MEXT-root lesson).
   - Quoting any figure from the corpus → grep for retraction/UNVERIFIED markers on that figure before it travels (the De Hogeweyk lesson: the retraction lived elsewhere in the corpus and the distiller picked the unretracted rendering).
   - Touching decisions/ or synthesis-path files → attestation authored in the same commit; `[DOCTRINE: <sha>]` token on every commit that will be PR HEAD.
4. **No silent fixes:** every mid-session correction of one's own earlier claim lands in a changelog/revision-history entry as it happens. Corrections are integrity capital only if visible.

## Mode 3 — Post-processing integrity check (before any ratification request)

1. **The mechanical battery** (all pre-existing; run as a unit): `validate_evidence_state.py --states-only --db`, `register_integrity_check.py --selftest --db`, `matrix_consistency.py`, `test_assess_cell_pilot.py`, `schema_reference_drift_audit.py`, `doctrine_recheck.py`, attestation schema validation, `claims_docket.py check`. Blocking CI is the owner's C3 decision; until then the battery is self-run and its results logged with commands and outputs (never summarized from memory).
2. **The adversarial pass — structural independence, not attitudinal:** a fresh agent context with (a) a brief to BREAK, (b) the stated presumption that ≥1 real defect exists, (c) instructions to re-run everything from scratch and trust no report, and (d) enumerated attack lines, minimally: claims-vs-artifacts inventory; self-application of every new rule; absolutes recount; verifier-bypass construction; strictest-test-on-favoured-conclusions; caveat-survival through distillation; ethics/CRPD lens; **and an audit of the author's statements to the owner in chat** — overclaims live in conversation as much as in files.
3. **Findings discipline:** every finding → fixed or explicitly rebutted; the fix-by-fix record lands in the target document's revision history; attestations gain `DEVIATION-LOGGED` entries where the review contradicted an attested claim. The correction record ships to the owner *with* the work.
4. **The gate:** no ratification request, no "done", and no PR marked ready while adversarial findings are unapplied. Timing is the economics — both historical rounds cost ~one agent-hour and pre-empted ratification on false premises; the same findings post-backfill cost migrations.

## Self-application

Per Mode 1 rule 4, checked against (a) this document itself and (b) `claims_docket.py` as the flagship Mode-2 tool — added missing 2026-07-13, an omission that was itself a Mode-1-rule-4 violation (this section did not exist), caught by a later Q14 adversarial pass on the ratification execution that first created this skill.

**(a) This document.** The two checkable absolutes in the header — "41 findings" and "three false absolutes" — previously carried no warrant markers, the exact defect class rule 1 exists to prevent. Fixed above: "41 findings" is RECOUNTED (18 + 23 = 41, verified by reading the two named DRs' revision histories directly); "three false absolutes" is marked REPORTED-BY rather than RECOUNTED, because re-tallying it would require re-reading all 41 findings in full, which this fix did not do — the honest thing is to say so, not to relabel an unverified number as verified.

**(b) `claims_docket.py`, flagship example, same-session evidence:** this tool violated Mode 1 rule 3 ("verifiers are born with selftests... a verifier that has only ever passed is unverified") twice in the same session, both caught by independent adversarial passes rather than by the tool's own author noticing:
- The C2 adversarial pass (2026-07-13) found the tool's pipe-delimited docket format broke on any scanned source line containing a literal `|` (e.g. a markdown table row), misreporting correctly-annotated claims as unannotated — and that the fix for a *previous* bug (an earlier adversarial-pass finding) had shipped with no regression test exercising the bug it claimed to fix. Both were fixed with selftest coverage that FIREs when manually reverted (confirmed by reverting each fix in a scratch copy and re-running `--selftest`, which correctly failed).
- Building the Q16 fix (a new `count` trigger class for bare-integer claims like "59 changed files") independently repeated the same failure mode at smaller scale: the first regex draft was written and never checked against the real example it was meant to catch, and — per rule 3 — the new selftest case caught it immediately (`**MISSED**: scanner on synthetic triggers`) before the fix was corrected and re-verified.

The pattern across all three instances: this session's own author (Claude, same protocol, same session) did not catch any of them at write-time despite following Mode 1/2 discipline throughout — each was caught only by Mode 3 (an independent pass, or the verifier's own selftest catching the verifier's own author). This is the skill's stated limit, evidenced rather than merely asserted: see "What this skill does not do," below.

## What this skill does not do

It does not make the model rigorous — the project's own audit line stands: "protocol makes bias visible, not Claude rigorous." All three modes are visibility machinery; the correction loop (Mode 3 findings → Mode 1 structure improvements) is where rigour accumulates. Nor does it replace owner judgment: Mode 3's output is an input to ratification, never a substitute for it.
