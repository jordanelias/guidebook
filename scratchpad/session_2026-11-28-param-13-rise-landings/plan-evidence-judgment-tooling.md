# Plan: evidence records, judgment classifies (tooling only)

Opus, read-only, 2026-11-28. Input: `rulings-evidence-and-judgment.md` ("row N", "C1"–"C12") and GAP-388. This plan decides nothing that belongs to the owner. Counts are given as commands.

## 1. How to read each conflict

- **C1, C2, C11.** D-0182's "at least one" applies to the judged link and to the determination, not to recording.
  - The extraction stays a judgment-stage row (row 9), and it may be recorded with no lens and no domain.
  - The `context` tier refusal stays. It blocks nothing once a lens-less path exists, and lifting it would invite guessed groups.
- **C3, C4.** Relevance to a topic is settled at evidence (D-0174 stands). Admissibility for a determination is decided at judgment. After Q4, CLAUDE.md §3 and the contract's judgment `entry:` each get a one-line edit.
- **C5, C6.** The two rules combine. A judged group wins. A figure with no group reaches its parameter's domain groups through a derived view. This supersedes OR-1 for lens-less figures only.
- **C7.** The mapping is doctrine. A session proposes each row with a warrant and the owner reviews it, the same way `identity_need_icf` works.
- **C8, C12.** These do not block building. Keep OD-48's engine rule and OD-73.
- **C9.** The coordinator retires the workaround after PR3.
- **C10.** The verification, scan and verbatim refusals all stay.

**Owner questions, each with a recommended default:**

1. **May a figure be recorded with no group and get its groups at judgment?** Default: yes. "At least one group" binds the judged link and the determination, not recording. *This unblocks PR1 and every refusal in GAP-388.*
2. **When a figure names no group, does it take its parameter's domain groups automatically, and does a group the figure's own words name win?** Default: yes to both.
3. **Who writes the domain-to-group rows?** Default: a session proposes each one with its warrant, and you review them in batches, as you do the matrix.
4. **At evidence, does "admitted" now mean recorded and relevant to a topic, with "admissible for a determination" decided at judgment?** Default: yes.
5. **Does "not refused" cover only missing classifications, and not the checks that a source was retrieved, read and quoted?** Default: only classifications.
6. **Does universal/population/individual stay as the engine sets it now, until you rule on the scope chain?** Default: yes.

## 2. What gets a typed home, and what stays as guidance

**Built explicitly**, one value per cell, using pointers:

- **Figure → group.** `extraction_lens_links` (exists), written with `add-lens-link` plus basis and warrant.
- **Parameter → domain.** `terms.domain` (exists), set with `amend-term --field domain --reason`.
- **Domain → group.** New table `domain_lens_links`, modelled on `identity_need_icf`.
  - **Columns:** `domain`, plus exactly one of `identity_code`/`icf_code`/`needs_code` (real FKs), and `warrant NOT NULL`.
  - **Also:** `ref_id`, provenance only (row 38); `state` (`pending`/`stated`); `review_ref LIKE 'Owner%'`; retirement columns.
  - **The writer refuses:**
    - a domain that no live term carries (the list is derived from `terms.domain`, rule 8);
    - any domain in `dbcore.NON_QUANTITY_DOMAINS`;
    - `ALL`.
  - **The proposing verb** prints candidates from `v_lens_crosswalk` and `identity_proposals`, so the session judges rather than guesses.
- **Derived, never stored:**
  - `v_parameter_groups` = parameter → `terms.domain` → reviewed, live `domain_lens_links` rows.
  - `v_figure_lens` = `v_live_lens_links`, plus, for a live figure with no live link, its parameter's `v_parameter_groups` rows, with `basis='domain'`.

**Guidance only:** which domain a parameter belongs to, which groups a domain serves, what counts as salient, the "typically wheelchair users" defaults, and scope pairing.

## 3. Tooling PRs in merge order (rule 10)

**PR1: lens optional at recording (after Q1 and Q5). About 70 lines.**
- **Reads:** `add-extraction`'s guard, blocking T018-05, `code_value_identity_audit.py`.
- **Changes:**
  - Drop the guard. Run `_require_lens_warrant` only when a lens is given.
  - Add `v_judgment_queue` (§4).
  - T018-05 becomes "every extraction a specification links as governing or conditioning has a live lens".
  - Add audit list (v) for lens-less figures. Its EXAMINED count covers only linked figures, so lens-less code values would otherwise be invisible.
  - Invert T018-09 and T126-07.
  - Edit the run-pipeline skill (both copies).
- **Without it:** evidence is refused, or recorded under a false MOB.
- **Why nothing breaks silently:** `_lens_clause` already skips lens-less figures [UNVERIFIED by test].
- **After-test:**
  - A lens-less add writes 1 figure and 0 links.
  - The figure appears in the queue.
  - A MOB cell does not gather it.
  - A hand-inserted governing link to it turns T018-05 red.

**PR2: the domain home (after Q3). About 170 lines.**
- **Changes:** a migration, `propose-domain-lens` and `review-domain-lens` (mirroring `propose_identity_need_icf` and `review_identity_need_icf`), and `v_parameter_groups`.
- **Without it:** a ramp figure reaches no group.
- **After-test:**
  - `functional_axis` is refused.
  - A domain no term carries is refused.
  - A pending row is absent from the view; once reviewed, it is present.
  - Two lens codes on one row fail the CHECK.

**PR3: derived reach (after Q2). About 40 lines.**
- **Changes:** add `v_figure_lens`. Point the four `_lens_clause` sites, the audit, T018-05 and the queue at it.
- **Replaces:** the `context` MOB workaround.
- **After-test:**
  - A lens-less circulation figure reaches a WCU cell only once a reviewed circulation→WCU row exists.
  - A figure with a judged BLIND link does not reach the WCU cell.

**PR4: governance text (after Q4). About 30 lines.** CLAUDE.md §3, the pipeline contract's judgment `entry:`, and the guidelines named in §4.

**The provisional MOB rows**
- **Where they are:** in the canonical DB, `select count(*) from extraction_lens_links where basis='context' and identity_code='MOB'`. The brief's 127 are in the session scratch DB [UNVERIFIED].
- **What the checks do today:** each row carries a judged MOB identity, so `code_value_identity_audit` passes them and drops them from its queue. The gate passes over a false subject.
- **What they conflict with:** the MOB split (row 3) and OD-91.
- **What to do:**
  - After PR3 and a reviewed circulation mapping, retire them with `retire-lens-link`, found by session, basis and MOB, in a research PR.
  - Left in place, they block domain inheritance, because the figure's own link wins.

## 4. What judgment can do with unclassified evidence

- **Queue.** `v_judgment_queue` holds one row per (extraction_id, missing), derived and never flagged by hand.
  - `missing='group'`: the figure has no row in `v_figure_lens`.
  - `missing='domain'`: the parameter's term has a blank domain.
- **Verbs, each with a warrant in named columns:**
  - `amend-term --field domain --reason`
  - `add-lens-link --basis --basis-text [--basis-reason]`
  - `propose-domain-lens --warrant` / `review-domain-lens --approval-ref` (new)
  - `retire-extraction --reason` (a figure judged not salient)
- **Admissible** is derived, not stored: the figure is live, its source is VERIFIED, and it has at least one `v_figure_lens` row. No new table or column.
- **Guidelines:**
  - A section "Judgment: classifying recorded figures" in `.claude/skills/run-pipeline/SKILL.md` and `skills/run-pipeline_SKILL.md`.
  - A section "Domains and the groups they serve" in `governance/functional-taxonomy.md`: how to choose a domain, how to read the crosswalk proposals, and that a judged group outranks a domain group.

## 5. Risks and the rule-4 sweep

- **Rulings this breaks:**
  - PR3 breaks OR-1 ("only through the lens tags written on that figure"). It needs Q2's yes and a recorded supersession (rule 0).
  - D-0184 (not the owner's) needs a SUPERSEDES line.
- **Inference without review:** domain rows are the only route, and an unreviewed row reaches nothing.
- **`medical` domain:** it remains on some terms (`select count(*) from terms where domain='medical'`) even though the medical layer was deleted. It is in `NON_QUANTITY_DOMAINS`, so it is refused.
- **Callers swept:**
  - `v_live_lens_links` readers: `assess_cell` (4 sites), the audit, and T018-05, plus tests in `test_assess_cell_pilot.py`, `test_run_pipeline_refusals.py` and `test_db_amend_writers.py`.
  - The run-pipeline skill (both copies), and registry entries `test_db_integrity` (blocking) and `code_value_identity_audit`.
  - Untouched: `v_item_provenance`, `evidence_state.py`, and the `specifications` CHECK.
  - Not swept: prose in `governance/` and `references/` [UNVERIFIED].
