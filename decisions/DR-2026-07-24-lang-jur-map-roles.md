# DR-2026-07-24 — `lang_jur_map` role definitions + population (PROPOSAL, owner-to-decide)

- Status: **PROPOSED — DG-NON. Owner decides; this agent proposes only.** No register entry
  is added (a proposal is not a made decision; the register holds decisions, status ∈
  {ACTIVE, SUPERSEDED, RETIRED}). No data migration is emitted and `data/guidebook.db` is
  **not** touched. This file is the proposal artifact the owner ratifies or amends.
- Date: 2026-07-24
- Category: **D-METH** (the role *taxonomy* — how PRIMARY/SECONDARY are defined) with a
  **D-DOCT/DG-NON** core (the *population* of the map assigns which of the 19 languages are
  in-scope for which of the 48 jurisdictions — decision-protocol §2.4 items **#4 inclusion/
  exclusion of jurisdictions** and, by extension, of the language axis per jurisdiction).
- Delegation: **DG-NON** (upgraded from the D-METH default per §2.3, because the map fixes
  jurisdiction/language scope, an always-DG-NON matter).
- Prepared by: Claude (Opus), operationalizing Phase 0a of
  `workplan/research-matrix-completion-execution-plan-2026-07-24.md`.
- Affects (only if the owner ratifies): a future `data_*.sql` populating `lang_jur_map`;
  the coverage-loop priority queue (which cells are *required* vs *not-applicable*).
- Related & **binding precedent**: `DR-2026-06-11-remove-colonial-role` (which **withdrew a
  prior auto-population of this exact table as fabrication**), migration `023_lang_jur_map.sql`
  (created the table empty, deferred population "pending role definitions — owner/spec input"),
  `025_drop_colonial_role.sql` (tightened role CHECK to `{PRIMARY, SECONDARY}`),
  `DR-2026-07-22-work-from-axes` (no armchair umbrellas), the multilingual-research skill
  (19 languages × 48 jurisdictions axes).

## Why this is a proposal and not a migration (the precedent that governs it)

The last time `lang_jur_map` was populated (`data_20260611224657`), the rows were **withdrawn
and the ledger row deleted** (DR-2026-06-11) because roles — then including an undefined
`COLONIAL` — were assigned **without project-ratified definitions**, contradicting the workplan's
own examples. Migration 023's header is explicit: *"Assigning ~60–100 PRIMARY/SECONDARY/COLONIAL
rows without the project's role definitions would be fabrication. The table is created empty; a
companion data migration populates it once the role taxonomy is defined (owner / spec input)."*

That definition has never been ratified. Therefore the correct governance act now is **not** to
re-populate the table — it is to **propose the missing definitions for owner ratification** and,
only after that, to populate. Populating first would repeat the exact fabrication DR-2026-06-11
reversed. This DR supplies the definitions and a *candidate* population **for the owner to
ratify, amend, or reject.**

## Proposed role definitions (the piece migration 023 said was missing)

The `role` CHECK admits only `PRIMARY` / `SECONDARY` (post-DR-2026-06-11). Proposed meanings,
anchored to the workplan A.3 examples ((EN,US,PRIMARY), (EN,IN,SECONDARY), (EN,ZA,SECONDARY)):

- **PRIMARY** — the language is a **de jure or de facto official/administrative language in
  which the jurisdiction authors its own statutes, building codes, and standards**. Evidence
  produced *in* this language for this jurisdiction is first-party. (EN→US, DE→DE, JA→JP,
  ES→MX, PT→BR, ZH→CN, KO→KR, AR→EG, FR→FR, …)
- **SECONDARY** — the language is **used for law/administration/higher-education in the
  jurisdiction but is not its primary authoring language** — the workplan's colonial-legacy
  case (EN→IN, EN→ZA, EN→NG, EN→KE, EN→GH, EN→TZ, EN→PH) **and** genuine co-official / major
  regional languages that are not the dominant authoring tongue. Evidence in this language is
  real first-party evidence for the jurisdiction, but the PRIMARY language must also be searched.

**Not a role, recorded as a gap, never a row:** a jurisdiction whose primary authoring language
is **outside the 19** (Thai→TH, Amharic→ET, Tagalog/Filipino→PH-alongside-EN, Greek→CY,
Khmer/…). For these, the map may carry EN (or another in-scope language) as SECONDARY *and* the
proposal flags a **`[PRIMARY-LANGUAGE-GAP]`** so the loop records honestly that the jurisdiction's
own-language corpus is under-reachable — surfaced, not silently dropped (mission transparency).

**Cell semantics for the loop.** A (slug, jurisdiction, language) cell is **required** iff the
(language, jurisdiction) pair has a `lang_jur_map` row (PRIMARY or SECONDARY); otherwise it is
**NOT-APPLICABLE** and never counted against coverage. This is the bridge the empty table
currently denies the priority queue.

## Candidate population — approach, sourcing standard, and scope (for owner sign-off)

- **Sourcing standard (no armchair, no fabrication).** Every row's role is grounded in a
  **verifiable official-language fact** about the jurisdiction (constitutional/official-language
  status; the language building codes and standards are published in), recorded in the row's
  `notes` with its basis. Official-language status of a country is a checkable public fact, not a
  judgment call — this is what distinguishes a defensible map from the withdrawn one. Edge cases
  (co-official ranking, regional languages) are flagged for owner adjudication rather than
  resolved unilaterally.
- **Scope.** 48 jurisdictions × the subset of the 19 languages with an official/administrative
  role in each — an estimated ~70–110 rows (most jurisdictions map to 1 PRIMARY + 0–2 SECONDARY).
  The candidate row set is **not** emitted here; on ratification of the definitions above it is
  produced as a single reviewable `data_*.sql`, each row carrying its sourcing note, for a second
  owner pass before it lands.
- **Work-from-axes (DR-2026-07-22).** Roles attach to *jurisdiction × language* facts, never to
  population umbrellas; the map does not coin or collapse any community categories.

## Adversarial pass (one pass, this version — R2 / DR-2026-05-09)

- **Objection (the strongest): this is the withdrawn fabrication in new clothes.** DR-2026-06-11
  reversed exactly this. **Answer:** three material differences name why this is not that: (1)
  `COLONIAL` — the undefined role that caused the withdrawal — is gone from the CHECK and from
  this proposal; (2) this DR **defines** PRIMARY/SECONDARY before any row is proposed, closing the
  "no definitions" defect migration 023 named; (3) **no rows are committed** — this is a proposal
  for owner ratification, whereas `data_20260611224657` was an *applied* migration. If the owner
  does not ratify, nothing was written and there is nothing to withdraw.
- **Objection: PRIMARY/SECONDARY is a colonial framing by another name.** Marking EN as SECONDARY
  for India/South Africa could be read as either honoring or erasing the local-language corpus.
  **Answer:** the `[PRIMARY-LANGUAGE-GAP]` flag makes the erasure risk *visible and counted* — the
  map's job is to route search effort honestly, and flagging that (e.g.) Hindi/Bengali or isiZulu
  coverage is the real first-party target is the anti-erasure move. This is precisely the kind of
  call that is **DG-NON**: the owner, not the agent, ratifies how the axis is framed.
- **Objection: why not just treat all 19×48 as required?** **Answer:** that inflates the
  denominator with cells that are genuinely not-applicable (searching Korean sources for a Moroccan
  code), making honest completion impossible and diluting effort away from required cells — the
  opposite of the mission's transparent-adjudication aim.
- **Refutation test:** each proposed row is falsifiable against the jurisdiction's published
  official-language status and the language its building code is authored in; a row whose `notes`
  basis cannot be verified is dropped, not asserted (`source-discipline`).

## What this DR does NOT do

- Does **not** write any `lang_jur_map` row or emit any migration — proposal only.
- Does **not** re-introduce `COLONIAL` or any third role.
- Does **not** decide jurisdiction/language scope — that is the owner's (DG-NON); this supplies
  the definitions + candidate approach for that decision.
- Does **not** coin, merge, or map any population/community category (work-from-axes).
