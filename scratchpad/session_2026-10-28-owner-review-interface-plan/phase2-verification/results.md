# Phase 2 acceptance run, 2026-10-29 05:28 UTC (decisions as prompts; rows and decisions the ledger rules on listed as ruled)

Page built with: python3 scripts/generate/owner_browser_build.py --out <harness scratchpad>/ob/index.html --wasm <local copy of sql-wasm.wasm; the build verifies its sha256>
Drivers (this folder): test_browser.js and test_prompts.js (the answer flow against an in-memory stand-in for the page's store; it picks its prompts from what is open). Headless Chromium via Playwright, 400x800 touch viewport; sql-wasm.js served from a local copy at the cdnjs URL. expected.json is produced by a Python script from the same database and the YAML.

## Main run
  pass database opened and first screen rendered
  pass table list equals sqlite_master (56 tables)
  pass every table count equals select count(*)
  pass view list equals sqlite_master (22 views)
  pass stamp shows user_version and sha256 of the file
  pass no horizontal overflow at 400px: home
  pass prompt groups equal the decisions file (open gating, other open, ruled) and the queries (3,9,39,4,17,0,1,0,0,6)
  pass one card per decision and per row, waiting or ruled (79)
  pass nav label carries the number of open prompts (40)
  pass with no store the page says saving is unavailable and offers Copy
  pass no horizontal overflow at 400px: waiting
  pass a decision prompt carries why, context, what it holds up, options and a recommendation
  pass Save is disabled when the view has no store
  pass no horizontal overflow at 400px: waiting, a prompt open
  pass an answered decision shows the owner's words and what it changes, from the ledger entry
  pass an answered decision offers no options
  pass a database row the ledger rules on is listed as ruled, with the owner's words, and offers no options
  pass ruled rows are not also listed as waiting
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
33 passed, 0 failed

## Answer flow (mocked store)
  pass starts with nothing answered and saving available (40 open)
  pass Save is enabled when the view has a store
  pass choosing an option marks it
  pass the line to send in chat names the prompt and the choice
  pass the answer is stored with choice, note, prompt id and the database stamp
  pass the chip shows the answer
  pass the count updates
  pass an option that asks for words is refused without them and nothing is stored (OR-1c)
  pass a row prompt is stored as list-and-id (withheld_findings-3)
  pass no console errors
  pass a later visit shows the saved answers
  pass the saved choice and note come back
  pass Clear removes the answer and updates the count
13 passed, 0 failed
