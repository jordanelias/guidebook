# Rehearsal: one admitted source read against other parameters (2026-10-21)

Scratch only. `data/guidebook.db` and `retrieval-log/` are byte-unchanged (`git diff --quiet HEAD -- data/guidebook.db retrieval-log`). Working copies are in the session scratchpad: `rehearse.db`, `rl/` (a copy of one retrieval-log session directory), `rehearse_batch.sql`, `mig_out/`.

**Subject.** REF-01008 (Templer et al., FHWA-RD-79-3 Vol. 3), filed under slug `accessible-circulation-geometry`, with 9 extractions, all on parameter 3 (ramp gradient). The question: can the pipeline, unprompted by the slug, read it against the other nine catalogue parameters and file what it finds?

## What ran, in order

| step | command | result |
|---|---|---|
| 0 | `observe-term` on "ramp length" with the quote I first chose | REFUSED: the surface form was not inside its own quote |
| 0b | same, with the table heading as the quote | REFUSED: the quote was found only in an UNSCOPED artefact (the manifest line for the held `.txt` has `ref_id: null`) |
| 1 | `scripts/research/full_text.py --ref-id REF-01008` (to a copy of the log) | 332 of 332 pages derived, with page markers; "NO TEXT LAYER on 3 page(s): [20, 329, 330]" printed |
| 2 | `observe-term` "Ramp Length", PDF p.37 | observation 91, verbatim `scoped` |
| 3 | `adjudicate-term` NAMES-EXISTING TERM-091 (ramp run length) | accepted |
| 4 | `add-extraction` parameter 12, finding, `--relation none`, from PDF p.300 | refused once (a `--stated named` label not in its quote); written on the second try (extraction 115) |
| 5 | `record-scan --mode catalogue --text-scope full` | accepted: pages read 332 of 332 |
| 6 | `record-scan ... --text-scope partial`, same source, same version | accepted as a second row |
| 7 | `raise-follow-up` on extraction 115 | accepted |
| 8 | `assess_cell.py --parameter-id 12 --identity MOB` | `pending`, no marker; GAP text correctly says one source, every row a finding, no threshold |
| 9 | `emit_batch_sql` then `emit_data_migration`, applied to a copy of canonical | 6 inserts across 5 tables; applied; `foreign_key_check` empty |
| 10 | `observe-term` "sidewalk width"; `add-term --from-observation`; `add-parameter` | TERM-095 and parameter 13 in three calls |
| 11 | `scan_debt` before and after | 459 pairs after step 5; 511 after parameter 13 was minted; 510 after a targeted scan of REF-01008 for it |

## What broke or was blind, worst first

1. **The batch gate cannot see a re-read of an admitted source.** `research_batch_dod --session` reports every R16 rule, R11-harvest and R17 as `EXAMINED: 0 ... asserts nothing`, because each is scoped to the session's admissions and this session admitted none. The observation, adjudication, extraction, two scans and follow-up were all invisible to it. Only `scan_debt` (advisory) counts them. A Phase 5 batch that re-reads the 53 held sources would pass the gate while reading nothing.
2. **`record-scan --text-scope full` accepted a PDF with three pages that have no text layer**: 332 of 332 pages read. The guard counts page markers, and the markers exist for blank-layer pages. `full_text.py` prints the warning to the terminal and records it nowhere.
3. **Scans cannot be corrected.** `record-scan` is the only scan verb. A later `partial` sat beside the earlier `full` as a second row for the same source and catalogue version, and `scan_debt` kept the source as read.
4. **The cross-slug follow-up is voluntary.** `add-extraction` did not ask for one, and `extraction_follow_up_audit` passes while no live determination rests on the figure. "Cross-slug" cannot be computed (parameters carry no slug), so the tag rests on a human saying so.
5. **Definition fit is unchecked.** TERM-091 is the horizontal length of a single flight between landings; the source's "Ramp Length" is a test ramp's dimension and may be measured along the slope. NAMES-EXISTING was accepted with no check against the term's definition. The rationale had to carry the doubt.
6. **Catalogue growth multiplies debt.** One new parameter added 52 pairs (459 to 511), one per held source. Nine parameters over 53 sources is the 468 the plan quotes; each addition is another 53. `--open-pass-done` is a boolean: quantities a reading found that the catalogue lacks are recorded only if someone also runs `observe-term` for them.

## What worked

The two verbatim refusals (the quote must contain the phrase; the quote must come from this source's own registered bytes) fired on real mistakes. The register-then-observe-then-adjudicate-then-extract chain, the one-step mint of a term from an observation, and the capture and replay onto a canonical copy all held. The engine's gap text for a finding-only parameter was accurate.

## Yield, for scale

Of the nine other parameters, this source gave one statable figure (ramp run length, a finding, doubtful definition match) and one quantity the catalogue lacks (sidewalk width: a site description, not a recommendation). Width, turning, force, door and headroom terms were absent or were equipment dimensions. A pedestrian-facility report is a poor test of breadth; a building code would be a better one.

## Not a finding

`observation_verbatim_audit` reported "missing 82 > baseline 17" in the rehearsal because the rehearsal's retrieval-log copy held one session directory. That is the copy, not the pipeline.
