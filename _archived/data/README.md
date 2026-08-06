# Pre-reset corpus — archived database

`corpus-pre-reset-2026-08-06.db` is `data/guidebook.db` exactly as it stood
immediately before the 2026-08-06 clean-room reset.

**It is not named `guidebook.db`, and that is deliberate.** Nothing in the
toolchain resolves this path: `GUIDEBOOK_DB_PATH` defaults to
`data/guidebook.db`, no script globs for `*.db`, and `_archived/` is covered by
the root `.ignore`, so ripgrep and agent search skip it. It is reachable only by
naming it — which is what an archive should require.

## What it holds

The full evidence corpus produced before the reset: 863 `evidence_sources`,
1,478 author rows, 1,011 source-slug links, 183 `citation_mining` rows, 84
logged searches, 64 population matches, 15 determined cells, 109
`jurisdictional_values`, 313 gaps, 273 connections, and the two frozen search
grids.

## Why it was set aside

Not because the work was bad — because the corpus could not show its work. 824
of 863 sources had no recorded admission, 15 of 2,139 cells were determined, 3
governing references out of 61 links carried a population grade, and no
published best practice could be walked back to the search that found its
sources. A corpus that cannot show its work is reference: useful to consult,
not ours to assert.

## Also archived in git

Branch `archive/pre-reset-corpus-2026-08-06` holds the same state as a full
commit, including this database at `data/guidebook.db`. That branch is the
authoritative archive; this file is the convenience copy, so the corpus can be
queried without checking anything out:

```python
import sqlite3
con = sqlite3.connect(
    'file:_archived/data/corpus-pre-reset-2026-08-06.db?mode=ro', uri=True)
```

A matching tag could not be pushed — the session integration returns 403 on tag
creation. Adding `archive/pre-reset-corpus-2026-08-06` as a tag, and protecting
the branch, are owner actions in repo settings.
