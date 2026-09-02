# session_2026-09-02-owed-repairs

**This record covers four session ids, and that is itself a defect it records.** The
migrations applied today name:

- `session_2026-09-02-refid-highwater-repair`
- `session_2026-09-02-restore-research-code-leads`
- `session_2026-09-02-owner-rulings-restore-sweep-strike`
- `session_2026-09-02-owed-repairs`

They are **one working session**. Minting a fresh id per migration looked tidy and is
wrong: CLAUDE.md §7 makes the session id the thing gates scope to, so four ids fragment
one session's work across four scopes, none of which is the whole. The ids are listed
above so a reader grepping any of them reaches this file. Do not repeat it — one session,
one id.

---

## What was decided, and by whom

Three owner rulings, recorded at contact as **D-0185/0186/0187** with DRs and attestations:

1. **Restore the 83 code leads as `research_code_leads`** — *executing* D-0181, not
   superseding it.
2. **Finish the render sweep** — archive the site surfaces still publishing the deleted
   item layer.
3. **Strike DR-2026-08-19 §12.1 step 2** — the item-frame pull that contradicted §1.4.

## What was repaired

**The P1 that did not block.** `next_ref_id()` returned `REF-00965`. Deleting
`evidence_sources` dropped the union high-water mark from 970 to 964, while 26 surviving
research rows still named those ids. Nothing refused it — R9a/R9b cannot fire below
REF-00964 — so the next `add-source` would have run green and minted a live identifier for
a different paper. Six identities parked as research-stage leads; mark restored to 971.

**Three backfills.**
- The **retrieval manifest**: `--backfill` could never have done this, because its input is
  `evidence_sources` and that is exactly what a retraction empties. Added
  `--reconstruct-manifest`; 21 lines rebuilt, every one marked `reconstructed=true`, URLs
  derived from each payload's own `message.DOI` rather than its filename. The provenance
  half is weaker than a contemporaneous line and the docstring says so.
- The **mining anchors**: the register's proposed fix (write the DOI) was **wrong** and was
  corrected rather than followed — it would have reversed a deliberate rule-5 removal. The
  real defect was a foreign key asserting that an anchor must be admitted evidence. It need
  not be. Migration 067 drops it; all ten pointers restored.
- **Seven research rows**: `results_admitted` restored, and **H05 deleted**. That gate did
  not detect drift — it *caused* a research record to be rewritten so a duplicate would
  agree with it.

## Defects I introduced and then found

Recorded because a session that only reports its successes is not a record.

- **`validate_schema`**: my empty-registry `return 0` made the cross-check structurally
  unreachable. Fixed, and the cross-check then had to be repointed and its EXAMINED line
  unified before the vacuity guard would read it correctly.
- **A duplicate YAML key** on `validate_schema_cross_check` meant reasoning I reported as
  "recorded in the registry" was silently discarded on parse. It was not recorded.
- **A silent-drop bug** in the Co-1 warrant fix: the flag parsed, the refusal passed, and
  the value never reached the row. Caught on the probe, not by reasoning.
- **Four session ids** where one was correct — see the top of this file.
- **A commit message eaten by backticks**, amended with force-with-lease on my own branch.
- **93 rendered pages deleted outright** on 2026-09-01 when `_archived/` is the home for
  retired content; restored there.

## Still owed, and why it was not done

- **`jurisdictional_values` is empty, not dropped.** `v_code_floor_only` reads it, and
  CLAUDE.md holds a cross-stage view to be the most protected object in the schema. That
  view joins on `item_code`, which no longer exists, so what it *becomes* is its own
  question — an owner one.
- **Two archived pages** (`[cross-cutting].html`, `[unassigned].html`) appear nowhere in
  git history. Kept because they are content; no mechanism invented for how they arrived.
- **Root `index.html`** still states *"Corridor Clear Width (≥1200 mm Minimum on All
  Primary Routes)"* as fact. Rewriting the landing page's framing is mission content.
- **Item codes remain** in `terms.scope_note` (7), `axes.design_domains` (17),
  `search_candidates.title` (13). The "pared" ruling is not fully executed; the text edits
  are content judgements.
- **No jurisdiction vocabulary** to constrain `research_code_leads.jurisdiction`.
  `lang_jur_map` lacks two of the twelve values restored, so a CHECK would have been a
  second home for a vocabulary that has no single one.

## Gate state

`run_checks --changed-from origin/main` **PASS**, 43 green, 0 blocking, 8 advisory — the
pre-existing set. `--selftest` PASS. `test_db_integrity` 72/72.
`migration_reproducibility` PASS. `LATEST` moves here; **`LATEST-RESEARCH` does not**, for
the reason given in the 2026-09-01 record.
