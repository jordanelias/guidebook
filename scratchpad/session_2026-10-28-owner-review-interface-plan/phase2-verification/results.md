# Phase 2 acceptance run, 2026-10-28 05:50 UTC

Page built with: python3 scripts/generate/owner_browser_build.py --out <harness scratchpad>/ob/index.html --wasm <local copy of sql-wasm.wasm, sha256 verified by the build>
Driver: test_browser.js (this folder), headless Chromium via Playwright, 400x800 touch viewport, sql-wasm.js served from a local copy at the cdnjs URL.
expected.json is produced by a Python script from the same database (table counts, view list, queue counts, one CHECK vocabulary, user_version, sha256 prefix, foreign_key_check).

## Main run
  pass database opened and first screen rendered
  pass table list equals sqlite_master (56 tables)
  pass every table count equals select count(*)
  pass view list equals sqlite_master (22 views)
  pass stamp shows user_version and sha256 of the file
  pass no horizontal overflow at 400px: home
  pass queue counts equal the queries (4,17,3,1,0,0,11)
  pass nav label carries the total waiting count
  pass no horizontal overflow at 400px: waiting
  pass a queue row links to its row page
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
23 passed, 0 failed

## Added-table probe (a scratch copy with one extra table; the stamp line fails there only because expected.json holds the canonical sha256, and the page shows the copy's)
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
