# Ramp run length (parameter 12) and the 2026-10-29 ramp work, rebuilt on main

**Session id:** `session_2026-10-30-ramp-spec-pages-rebuild`
**Branch:** `claude/session-handoff-setup-e3hujd`
**Session kind:** research (rows only). No schema, script or check change. The render contract and any page are tooling and ship apart (CLAUDE.md rule 10).
**Pointers:** `sessions/LATEST-RESEARCH` moves to this session.

**Derive every figure.** Re-run the command beside a number rather than trust the sentence.

## 1. What this session did

The 2026-10-29/30 session's work was built on a base 2,203 commits behind main, with a static page generator main has since deleted (RULINGS R1). Its content was re-expressed through main's own writers. Brief: `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md`.

- Of the 14 sources the old batch listed, four were already on main (Chow 2009 = REF-00979, Bertocci 2018 = REF-00983, Sanford 1997 = REF-00980, Irish TGD M 2022 = REF-01018). Four group studies were admitted (REF-01033 to REF-01036); the Singapore Code on Accessibility 2025 was admitted as **REF-00139**, the id the identifier stash already held for that URL. The rest were not admitted; the reasons are in the notes of search 193 and in candidates 148 and 149.
- Parameter 12 (TERM-091, ramp run length) had no rows when this session started. While this branch was open, PR #209 (`session_2026-10-30-rest-landing-parameter`) merged parameter 12's direction and its DE, UK and BE run limits. At the merge this batch dropped its own direction and its own DE and UK 10 m rows (duplicates, rule 5) and kept the rest: run limits from IE, SG, NZ, ES, PT and FR, the UK Table 1 tiers (5 m and 2 m) and the IE Table 2 tiers, each conditioned on the gradient it applies at by a `condition_on` edge to a parameter 3 row.
- Catalogue rows for the Singapore Code on parameters 4, 5, 6, 8, 9 and 11.

Counts: `select parameter_id, count(*) from source_value_extractions where created_by_session = 'session_2026-10-30-ramp-spec-pages-rebuild' group by 1`.

## 2. The adversarial pass and what it changed

Pass 7, a read-only Fable 5.1 critic against commit `1e926814`. It sustained eleven findings; all are disposed REPAIRED by the replacement migration. The substantive ones: the first commit was red on two blocking checks (an orphan condition row; two sources marked mined with a deferred row); the UK and Irish tables were recorded unlike the Singapore one; `claimed_unit` carried prose the engine cannot compose; the Hashizume abstract does report results for the cervical-SCI group; Liu 2023's participants are not described as having an impairment. The reviewed migrations were removed from the tree and the batch was rebuilt from main's database; after PR #209 merged it was rebuilt again on top of main's new database (migration names and every extraction id moved). The reviewed state stays in git history.

**The pass is not closed.** `close-adversarial-pass` refuses because finding 140's artefact names the deleted first migration, a path that no longer exists. Closing it needs the owner or a tooling change.

## 3. Disclosures

- Five searches are backfilled (logged after the retrievals); each says so and its prior is post hoc.
- The scans are `pre-screen` over a derived text that holds every page; none was read end to end. The Singapore Code was searched per parameter and its Tables 3, 4, 5 checked against the page image.
- All literature readings are abstract-level. The Lenker PDF link returned a 5.6 kB stub.
- Forward citation mining was not done (OpenAlex HTTP 429); two backward passes ran, two were deferred for want of a reference list. The mining status column cannot say "backward mined, forward deferred" (GAP-015/GAP-022), so those sources read `deferred`.
- `journal_name` and `publisher` are NULL on the four literature rows: `add-source` has no flag for them (GAP-073).
- Not done: rise-based landing spacing and landing dimensions. PR #209 filed the same gaps (GAP-070, GAP-071), so this batch filed none of its own and appended to GAP-071 (a Singapore source now exists) and GAP-072 (this batch's length rows state metres or millimetres). This batch's one gap is the `add-source` writer gap (GAP-073).
- The previous session's classification vocabulary, page generator, data file and accessibility records were not carried; the generator and page are not restored (R1).

## 4. For the owner

1. Whether an element page for a ramp is to be rendered from `parameter 3` and `parameter 12` through the owner browser or a new renderer (workplan T-5, T-7). Nothing here renders.
2. The three DEFERRED adjudications (observations 92, 94, 95) and the two NAMES-EXISTING with an [ASSUMPTION] (91, 93).
3. The doctrine record the earlier handoff asks for (the mission document's wall on T4 to T6 against "the gentlest value in practice is best practice"): OR-4 and OR-20 of 2026-10-29 already rule most of it; no record was written here.
