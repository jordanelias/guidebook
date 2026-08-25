# F1 — read-only doctrinal audit: evidence collection / judgment / render

**Model:** Fable 5, read-only. **Recorded by Opus** because the auditor's harness runs with file
creation disabled — a constraint I introduced by choosing a read-only agent type, and which the
agent correctly refused to work around. Its digest is reproduced below as returned; the corrections
it makes to my own log are actioned in `OPUS-runbook-drift.md` PART 9.

---

## B. Verification verdicts

1. **`db.py` has no `specifications` writer — CONFIRMED.** The only production
   `INSERT INTO specifications` is `assess_cell.py:572`; the rest are test fixtures.
2. **`assess_cell.py` is a hardcoded 7-cell pilot — CONFIRMED.** `PILOT_CELLS` :114–130; argparse
   takes only `--db` / `--emit-sql` / `--report-json`; refuses the canonical DB; `next_gap_id`
   emits un-padded `GAP-1`.
3. **NOT_ASSESSED / PARTIAL / PROXY → `COND_DOWN_WEIGHTED` and DOWN_WEIGHTED anchors — CONFIRMED**
   (`directness.py:225-234`; `assess_cell.py:248-250`; `:314` `if anchors: state="stated"`).
   *Doctrinal ruling:* the consolidation is exactly what G2 (evidence-architecture §4) mandates —
   "caps consolidation at DOWN-WEIGHTED". **The defect is one layer up:** G2 also says "flags the
   source for assessment", and `needs_population_assessment` is computed and **consumed by
   nothing**; and evidence-methodology §2.2's `stated` threshold reads "direct parameter relevance
   … **for the target population**". So **doctrine arguably already forbids an unassessed anchor**,
   and OPUS D-12's "needs an owner ruling" *understates the existing text*. D-12's withdrawal of the
   None-is-full-match claim is **CORRECT** (`assess_cell.py:191-195` never passes None;
   `directness_from_primitives` has only test callers).
4. **`scope` absent from `_ES_COLS` and argparse; VERIFIED never sets `verification_disposition`;
   I1 requires CLOSED — CONFIRMED.** *Nuance:* `test_db_integrity` is `level: blocking` but
   deliberately held in its own battery outside the merge-required set (registry :162-169), so
   S2's "will not pass CI" is mildly **OVERSTATED** — DR §12.3.5 still makes it batch-acceptance
   fatal. Canonical's 10 rows are VERIFIED/CLOSED only because a migration hand-set them.
5. **OD-5 — CONFIRMED.** `insert_evidence_source` dedups against `evidence_sources` only;
   `insert_locator` checks both tables, case-folded.
6. **`room_page.py:26,29` `FROM room` — CONFIRMED and UNDERSTATED.** It also queries `room_item`
   (live: `room_items`) — a second wrong name S5 missed.
7. **`index.html:7` "91 provisions, 661 evidence sources" vs live 93/10 — CONFIRMED** (Cat A 18 v
   19, Cat F 7 v 8 also verified).
8. **`pipeline-contract.yaml:126-129` — CONFIRMED FALSE.** `register_integrity_check.py` docstring
   (:10-13) and code (:231-252) enforce the *amended* I3; the contract's inline NB is stale prose
   in the spine file.
9. **`validate_jurisdiction` — CONFIRMED** (blocking, exit 0, `EXAMINED: 111`, zero sqlite
   references; 20 `GB` rows live, tied with DE/US at 20). **But OPUS D-6 is OVERSTATED as novel:**
   DR §3 item 6c already records both the rows ("Correct and blocked, not wrong", pending OD-G)
   *and* "its enforcer never opens the DB" verbatim. D-6's "rows the project's own rule forbids"
   **contradicts that ruling**.
10. **OPUS D-1 / D-2 / D-9 / D-10 / D-13 verified exactly** — D-10's 89 / 184 / 272 / 16 / 0 / 256
    recomputed to the digit.

## C. Doctrinal reading

**C1 — §4 acceptance.** The three stages permit an honest evidence base and a rendered honest
absence — never an answered question. The mobility question stops being answerable at the
evidence→judgment hinge: no sanctioned writer for the extracted value (`source_value_extractions`:
5 readers, 0 producers) and none for `specifications` at all; even a hand-written cell renders
uncited (`specification_source_links`: 0 rows, no writer). **§4 is unreachable by construction**,
and OPUS D-9 correctly shows the freeze released on the row-count proxy §4 was written to reject.

**C2 — Co-1 and CRPD Art 4.3.** The repository **cannot** honour its own warrant mechanically, and
the traces understated how completely. No CLI flag; the Pydantic rule never runs on DB rows; and the
only wired Co-1 validator (`validate_evidence_state.py:76-110`) reads `data/sources/*.yaml` — **a
directory that does not exist** — with a dormant `NameError` its own comment admits.
`co1_provenance` appears in exactly one executable file: `db.py`'s whitelist. Post-incident, the
author-fabrication arm was fixed and live-verified (S2's byte-identical retrieval chain); **the
co-production arm was never built.** For mobility, every Co-1 source admitted via the sanctioned
path enters provenance-NULL, then NOT_ASSESSED, then anchors indistinguishably from an unexamined
proxy — **erasure as the default output**, which CLAUDE.md §6 names the worst failure available.

**C3 — the honest banner.** The banner *is* the doctrine working: thinking-tool honesty, §2(b)
derivation, `generate_parts` refusing full mode. **But S5 graded the banner and never read the
`<h1>` above it:** `site/specs/e-08.html` headlines "Corridor Clear Width (≥1200 mm Minimum on All
Primary Routes)" — a pre-reset determination DR-2026-08-19 §1.2 explicitly names as the quarantine's
second vector, and one contradicting tier-system §3's own 2440 mm worked example. Honesty about the
machine; contamination from the corpus, still rendered.

**C4 — the ratio.** Derived live: 63 checks (4 quarantined); 30,494 executable LOC in
`scripts` + `tools`; **book-producing generators 2,630 LOC (~8.6%)**; **audit + tests 11,476
(~38%)**. *Real work:* `test_db_integrity` (1,999 inspections, caught 4/4 defects),
`validate_evidence_state` (7/7 designed violations, precisely attributed), `pmp_audit`, the
mutation-tested register checker, the retrieval-log artefact chain. *Wrong-subject apparatus:*
`validate_jurisdiction` (markdown, not the table), `population_integrity_audit` (three empty link
tables, not `evidence_population_match`), the Co-1 YAML validator over a nonexistent directory, the
contract lying about its own enforcer. **The gates are thickest around the DB and thinnest exactly
where the reader is:** `index.html`, `parts/v10`, `site/rooms` — unguarded, and two of three
measurably wrong today.

**C5 — the strongest objection.** The smoke test is itself the loop: seven agents, ~5,400 log lines,
zero evidence, zero determinations, in a repo whose instrument ruled adversarial passes may only
take data/synthesis diffs as subject and whose §4 says only research counts; several "findings"
rediscover recorded defects (OD-5, D-6/OD-G, render-freshness `check: null`). **It partially
holds** — the loop tax is real and the redundant findings prove it. **It fails as a dismissal**
because roughly half the headline findings are new, verified, and directly de-risk the ordered batch
(scope/I1 CLI dead-ends, NOT_ASSESSED-anchors, `parts/v10` measured stale, 256 stranded mobility
DOIs, the attestation window split) — and the freeze that would have forbidden it expired by its own
terms.

## D. Top three misses across the traces

1. **The §1.2 contamination live on the very pages S5 called honest** — all 93 `<h1>`s carry
   quarantined determinations.
2. **The Co-1 enforcement chain is triply dead**, including a wrong-subject vacuous gate — OPUS's
   own "species 2", which OPUS did not find.
3. **The advocacy delta** (evidence-architecture §6 G5) — the mobility advocate's key render output
   — is unbuildable end to end (`jurisdictional_values` values 0/109 by ruling, no extraction
   writer, I2 subject-less), and no trace assessed it.

*Also unasked:* the mission's own 8-question test, and tier-system §10's role-appropriate-authority
gate for firm sources.
