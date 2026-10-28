# Phase 2 acceptance run, 2026-10-28 06:02 UTC (after the decision prompts were added)

Page built with: python3 scripts/generate/owner_browser_build.py --out <harness scratchpad>/ob/index.html --wasm <local copy of sql-wasm.wasm; the build verifies its sha256>
Drivers (this folder): test_browser.js (screens, counts, pointers, vocabularies, prompts as read-only) and test_prompts.js (the answer flow against an in-memory stand-in for the page's store). Headless Chromium via Playwright, 400x800 touch viewport; sql-wasm.js served from a local copy at the cdnjs URL.
expected.json is produced by a Python script from the same database and the YAML (table counts, view list, queue counts, number of decisions, one CHECK vocabulary, user_version, sha256 prefix, foreign_key_check).

## Main run
  pass database opened and first screen rendered
  pass table list equals sqlite_master (56 tables)
  pass every table count equals select count(*)
  pass view list equals sqlite_master (22 views)
  pass stamp shows user_version and sha256 of the file
  pass no horizontal overflow at 400px: home
  pass prompt groups equal the decisions file and the queries (6,25,4,17,3,1,0,0,11)
  pass one prompt per decision and per waiting row (67)
  pass nav label carries the number of open prompts
  pass with no store the page says saving is unavailable and offers Copy
  pass no horizontal overflow at 400px: waiting
  pass a decision prompt carries why, context, what it holds up, options and a recommendation
  pass Save is disabled when the view has no store
  pass no horizontal overflow at 400px: waiting, a prompt open
  pass a row prompt links to its row page
  pass the row's long text is shown in full (153 characters)
  pass table page shows 40 cards first
  pass show more extends to 80
  pass search narrows the list (11)
  pass no horizontal overflow at 400px: table
  pass tapping a card opens its row page
  pass no horizontal overflow at 400px: row
  pass a foreign-key value is a link to the referenced row
  pass the link opens the referenced source
  pass pointed-to-by opens the table filtered to this row
  pass field note lists the column's own CHECK values (4)
  pass a view page opens
  pass no horizontal overflow at 400px: wide table (97 columns), columns open
  pass no console errors
29 passed, 0 failed

## Answer flow (mocked store)
  pass starts with nothing answered and saving available
  pass Save is enabled when the view has a store
  pass choosing an option marks it
  pass the line to send in chat names the prompt and the choice
  pass the answer is stored with choice, note, prompt id and the database stamp
  pass the chip shows the answer
  pass the count updates
  pass an option that asks for words is refused without them and nothing is stored
  pass a row prompt is stored as list-and-id (withheld_findings-3)
  pass no console errors
  pass a later visit shows the saved answers
  pass the saved choice and note come back
  pass Clear removes the answer and updates the count
13 passed, 0 failed

## Added-table probe (a scratch copy with one extra table; the stamp line fails there only because expected.json holds the canonical sha256 while the page shows the copy's)
owner_browser_build: table with no gloss: zz_probe
owner_browser_build: table with no stage: zz_probe
  pass database opened and first screen rendered
  pass table list equals sqlite_master (57 tables)
  pass every table count equals select count(*)
  pass view list equals sqlite_master (22 views)
  FAIL stamp shows user_version and sha256 of the file
  pass no horizontal overflow at 400px: home
  pass a table added to a copy appears with no code change (listed as unmapped)
6 passed, 1 failed

canonical sha256 before: 4b3cfb03d41d8a983c8d58119f408d7054c6a6f388fb0d90c7a519f1bbf66037
canonical sha256 after:  4b3cfb03d41d8a983c8d58119f408d7054c6a6f388fb0d90c7a519f1bbf66037
