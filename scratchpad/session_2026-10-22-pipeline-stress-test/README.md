# Session 2026-10-22: pipeline stress test, question register, resolution report

Written after PR #200 and PR #201 (step 3 specification, the marker and its review follow-up) merged. This folder holds a stress test of the pipeline in every direction with an attempt to render, the owner's questions that followed it, a read-only reasoning pass (Fable 5.1, high effort) on how to resolve them, and a report with exact instructions (Opus) built from that pass.

**Read in this order.**
1. `question-register-2026-10-22.md` : every question since the stress test, verbatim, with the answer given, by pipeline stage; the extrapolated questions E0 to E13; the open owner rulings.
2. `resolution-report-2026-10-22.md` : the report. Section 2 is the owner decision sheet (answer it before the plan); section 3 the tooling PRs in order; section 4 the research-data procedures; section 6 the verification matrix and a scripted re-run of the stress test; Appendix A lists where it departs from the reasoning pass.
3. `fable-resolution-reasoning-2026-10-22.md` : the reasoning pass the report was built from. Treat it as reasoning, not authority; the report corrects 19 of its statements.
4. `slugs-and-parameters-2026-10-22.md` : the slugs, parameters and terms as the database held them, with the mint-time value screen applied.

**Evidence.**
- `stress/` : the scripts and outputs of the stress test (`conflicts.py` conflicting-value fixtures G1 to G13; `cells.sh` the engine over every parameter and four lenses; `render_attempt.py`; `listing.py`; walkability output on the canonical and a populated scratch database).
- `report-probes/` : the report writer's probes and its scripted re-run (`regress_2026-10-22.sh`, `fixtures_g1_g13.py`, `notation_probe.py`), and their outputs.

**Paths inside the documents.** They were written against the session's scratchpad (`/tmp/claude-0/.../scratchpad/`, ephemeral). The same files are here: `stress/` and `report-probes/` map one to one; the four documents sit at this folder's top level.

**Not committed, by design.** Scratch databases, the sparse repository clone used to run the write path, and the generated outputs of the as-printed regression run (re-create them with the scripts). The captured outputs of `run_checks.py --all` on the canonical and the populated database were dropped: each quotes the retired-vocabulary audit's own findings and so adds hits to that audit. Re-create them with `python3 scripts/run_checks.py --all` (with `GUIDEBOOK_DB_PATH` set for the populated run).

**State when written.** `data/guidebook.db` at `PRAGMA user_version` 116, sha256 prefix `4b3cfb03d41d8a98`; every figure in the documents is a result measured on 2026-10-22: re-run, do not quote (CLAUDE.md rule 7a). Nothing in the repository's code, schema or data was changed by this work.
