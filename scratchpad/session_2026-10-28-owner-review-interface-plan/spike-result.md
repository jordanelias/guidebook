# Phase 1 spike result (2026-10-28): GO

Question: can the Artifact viewer run SQLite (sql.js 1.10.3, WebAssembly) on a database embedded in the page?

Answer: yes, on the owner's phone. The page (7.7 MB, database 5.1 MB embedded as base64, sql.js script from cdnjs, wasm embedded in the page because the contract blocks a library's runtime fetch) ran every step in the viewer and stored its own result in the artifact database (`spike/result`, read back with ArtifactData):

- viewer: Android WebView, Chrome 155, Claude app (user agent in the stored document)
- `WebAssembly.compile` permitted; `initSqlJs({wasmBinary})` works
- database opened in 19 ms; `PRAGMA user_version` 116; 57 tables, 22 views; `PRAGMA foreign_key_list` works
- the largest view (7,190 rows) evaluated in 4 ms
- an UPDATE in the in-browser copy changed `v_open_determination_gates` from 1 row to 0 (views recompute in the page)
- the `db` capability wrote the result document (the proposals queue is feasible)

Also observed locally: a CHECK constraint refused a test UPDATE that left `resolved_at` set without its two companion columns, so the browser copy enforces the table's own CHECKs.

Consequence: Phase 2 proceeds on in-page SQL. The owner is on a phone, so the design target is a phone screen (single column, list-and-detail navigation, no hover, no wide grids), not "also works at phone width".

Evidence: spike page built from `spike-build/` in the harness scratchpad (not committed; generated output). Artifact: https://claude.ai/artifact/CwZfTyennssgh7xavU6gmx
