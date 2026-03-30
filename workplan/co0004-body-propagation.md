# CO-0004 Body Text Propagation Workplan
**Created:** 2026-03-29 16:56
**Source:** Session 4 structural audit (GAP-CR-05 diagnosis)
**Workflow:** Renumbering → cross-reference-resolver → structure-auditor

---

## Scope

Propagate CO-0004 (2026-03-29) structural changes from canonical ToC to body text of `Guidebook_for_Accessible_Design_v9-0_2026-03-20.md` (6,683 lines).

## Pre-requisites

- CO-0004 Part Map (in `workplan/P1-D2-D3-co0004-remapping.md`) — confirmed available
- Canonical ToC (`references/toc.md`) — confirmed CO-0004 compliant

## Phase 1: Volume Dissolution (3→2)

| Step | Action | Lines affected |
|---|---|---|
| 1a | Replace `# Volume I: Foundations, Categories, Synthesis` → `# Volume I: Accessible Design — Principles, Specifications and Application` | L144 |
| 1b | Remove `# Volume II: Application Manual and Engineering` heading (L785) — content continues in Vol I | L785 |
| 1c | Replace `# Volume III: DAR, Economics, Evidence and Appendices` → `# Volume II: Evidence, Economics and Case Studies` | L5392 |
| 1d | Update front matter Volume map (L31–L89) to 2-volume structure | L31–89 |

## Phase 2: Part Renumbering

| Old Part # | New Part # | Body heading line | §-prefix change | Notes |
|---|---|---|---|---|
| Part 3 | Part 3 | L705 | §3.x → §3.x (no change) | Title change: "Designing for Multiple…" → "Synthesis, Sequencing and the Co-Occurrence Framework" |
| Part 4 | *(merge into Part 3)* | L901 | §4.x → §3.x (renumber) | Old Part 4 content (synthesis, worked examples, §4.1–§4.8) merges into Part 3 as §3.5–§3.12 |
| Part 5 | Part 6 | L1236 | §6.x stays §6.x | Part heading number changes only |
| Part 6 | Part 7 | L1769 | §7.x stays §7.x | Part heading number changes only |
| Part 7 | Part 4 | L2042 | No §-prefix (item codes A-K) | Part heading number changes only |
| *(new)* | Part 5 | *(create)* | §5.x | Building-Level Co-Occurrence Resolution — stub with §5.1–§5.4 per ToC. Content depends on GAP-CONF-01/02 |
| Part 9 | Part 8 | L4817 | §9.x → §8.x | Full §-prefix renumber |
| Part 10 | Part 9 | L5142 | §10.x/§9.x → §9.x | Mixed numbering in body — normalize |
| Part 11 | Part 10 | L5396 | §11.x → §10.x | |
| Part 12 | Part 11 | L5495 | §12.x → §11.x | |
| Part 13 | Part 12 | L6024 | §12.xx case study refs → §12.xx (keep) | Part heading renumber; case study §-numbers already match |

## Phase 3: Content Fixes (combine with renumber pass)

| Fix | Lines | Action |
|---|---|---|
| Remove §2.12 IntD | L679–L704 | Delete section (proxied through DEM/NDV per project-standards) |
| Remove duplicate E-06–E-09 | L3688–L3793 | Delete second copies (keep first at L3545–L3635) |
| Relocate B-12 | L2855–L2882 | Move above `## CATEGORY C` heading (L2850) |
| Relocate E-12, E-13 | L3861–L3918 | Move above `## CATEGORY F` heading (L3856) |
| Relocate G-08, G-09 | L4361–L4426 | Move above `## CATEGORY H` heading (L4358) |
| Create Part 5 stub | *(new)* | Insert between Part 4 (items) and Part 6 (residential matrices) |

## Phase 4: Cross-Reference Resolution

After renumbering, run `cross-reference-resolver` on full document:
- All `§9.x` → `§8.x` (engineering refs)
- All `§10.x` → `§9.x` (consultant refs)
- All `§11.x` → `§10.x` (DAR refs)
- All `Part 12 §12.x` economics refs → `Part 11 §11.x`
- All `Part 7` item library refs → `Part 4`
- Narrative refs to "Volume II" / "Volume III" updated
- ~200+ cross-references estimated

## Phase 5: J-Code Purge (GAP-CR-03 partial)

Delete all J-01–J-08 references from Vol I–II body per BAR project-standards rule. Affected areas:
- Entry path matrix (L854)
- NOT-RETROFITTABLE table (L883)
- Worked examples (L919, L1130, L1137)
- Bathroom matrix rows (L1485)
- Non-residential matrices (L1781, L1807, L1842, L1846, L1856, L1885, L1919, L1953, L1994, L2019)

## Phase 6: Verification

- `structure-auditor` on result
- `guidebook-auditor` Mode A
- Line count delta report

## Estimated effort

3–4 dedicated sessions (Sonnet). Primarily mechanical find-and-replace with cross-reference verification. Content creation minimal (Part 5 stub only — full content depends on GAP-CONF-01/02).

## Dependencies

- GAP-CONF-01 (cross-population conflict evidence) — blocks Part 5 full content
- GAP-CONF-02 (Part 5 §5.2 conflict resolution) — blocks Part 5 full content
- Part 5 stub can be created without these; full content is separate workstream

---

## Execution Log

### 2026-03-30 05:15 — Phase 4 executed (GAP-CR-05 partial close)

**Pre-execution audit finding:** Phases 1–3 and 5 were already complete in the document.
- Phase 1 (Volume headings): already CO-0004 compliant
- Phase 2 (Part renumbering): all 12 Parts correct
- Phase 3 (content fixes): §2.12 deleted, duplicate E-items removed, all items in correct positions, Part 5 stub exists
- Phase 5 (J-code purge): zero J-codes in document

**Phase 4 executed — 15 corrections in 13 change operations:**

| # | Location | Change |
|---|---|---|
| 1 | L128 change log | §8.4.4 → Part 5 XREF-PENDING annotation |
| 2 | L137 change log | §8.4.10–12 → Part 5 XREF-PENDING annotation |
| 3 | L139 deferred items | "Part 8 Cross-Population Conflict Resolutions" → "Part 5 §5.2–§5.4" |
| 4–5 | L514, L719 | "See Part 8, §8.4.4." × 2 → Part 5 XREF-PENDING |
| 6 | L612 | "See Part 8, §8.4.4 for temperature conflict" → Part 5 XREF-PENDING |
| 7 | L686 | "see Part 8 for conflict resolution" → Part 5 XREF-PENDING |
| 8 | L739 | "see Part 8 §8.4.4 for resolution protocol" → Part 5 XREF-PENDING |
| 9 | L907 | "conflict register in Part 8" → Part 5 |
| 10 | L921 | "standard conflicts from Part 8" → Part 5 |
| 11 | L990 | "resolution documented in Part 8" → Part 5 |
| 12 | L1343–1345 | Broken "See Part VIII §8.4.1." (line-break artefact) → Part 5 XREF-PENDING |
| 13 | L2459–2461 | Orphaned "§8.4.1." → XREF-PENDING block |
| 14 | L2836 | "Part 8 §8.4.6 (TWSI vs DEM)" → Part 5 XREF-PENDING |
| 15 | L368 | Nav footer "Part 8 (Conflict Resolutions)" → Part 5 |
| 16 | L371 | "Part 8 for conflict resolutions" → Part 5 |

**XREF-PENDING tag:** All §8.4.x replacements carry `[XREF-PENDING: §5.x — GAP-CONF-01/02]`. These will be resolved when Part 5 §5.2–§5.4 are written (Sessions 17, blocked on GAP-CONF-01/02).

**Commit:** aba32a3d0cd75a5084e045a06a114b864acdb4b3

**Status:** GAP-CR-05 Phase 4 COMPLETE. No further mechanical propagation work remains. Remaining work on GAP-CR-05 is content-dependent (Part 5 full content — GAP-CONF-01/02 blocker).
