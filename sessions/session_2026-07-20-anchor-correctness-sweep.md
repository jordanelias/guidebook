# Session — anchor-correctness sweep + first safe corrections (2026-07-20)

Branch: `claude/evidence-base-state-slug-lz8up0`

## Ask

Owner: "you may need to check every single reference for correctness." Scoped (owner) to **anchors-first**:
the 233 T1/T2/Co-1/Co-2 rows that carry best-practice claims.

## Method

Multi-agent workflow `scripts/workflows/anchor-correctness-sweep.js` (60 agents, 786 tool calls, ~2.9M
tokens): each of the 233 anchor rows re-retrieved via a real tool call (WebSearch/WebFetch/PubMed), every
flagged defect independently adversarially refuted. Full findings: `audits/anchor-correctness-sweep-2026-07-20.md`.

## Findings (256 defects flagged)

- **165 confirmed, model-independent** (identity/language/jurisdiction/clear type errors).
- **71 confirmed, tier-model-dependent** (need GAP-298/GAP-299/weighted-strength first).
- **20 refuted** by the adversarial pass.
- **3 unretrievable this session** (REF-00045, REF-00111, REF-00140).
- **~1 in 7 anchor rows carries a confirmed defect** — systematic metadata debt, as the owner suspected.
- **Serious:** 7 anchor sources are unverifiable / possibly non-existent (e.g. REF-00055 "no RCOT
  publication with this title", REF-00058 "no such COTEC+WFOT statement", REF-00111/00152 "no identifiable
  source"). Held for owner decision (flag DISPUTED vs deep re-investigation).

## Applied this session (conservative first pass)

Because the agents' `proposed_value` fields are *descriptive strings*, they cannot be blind-applied. This
migration applies only the **44 unambiguous scalar/code corrections** where the true value is crisp:
`lang_detected` (langdetect fixes, both directions), `jurisdiction` (author-origin corrections),
`pub_year`, `author_count`, `grey_flag` (clears the stale flags on REF-00097/00240 from the PR #32 SRs),
and 2 clean `doi` + 2 `journal_name` fixes. Each carries the sweep evidence in `verification_note`. No tier
or anchor-structure change in this pass.

## Held for reviewed passes (NOT applied)

- **~76 author_display / pub_title corrections** — string transcription; need careful per-row application.
- **~44 tier / evidence_type reclassifications** — drop mis-typed rows OUT of the anchor set (e.g. REF-00009
  co1→clinical, REF-00021 standard_eb→news/grey); consequential for the audit, some overlap the pending
  tier-model decisions.
- **7 unverifiable sources** — owner decision pending.
- **71 model-dependent defects** — blocked on GAP-298/GAP-299/weighted-strength.

## Integrity

`PRAGMA foreign_key_check` / `integrity_check` clean; audit regenerated. Corrections are forward-only and
reversible.
