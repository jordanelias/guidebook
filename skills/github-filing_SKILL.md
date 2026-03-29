---
name: github-filing
description: >
  Move stale or superseded files to a deprecated/ subdirectory within the same GitHub directory.
  Applies to any watched directory when a new file is committed that supersedes prior versions.
  Trigger on: "file into deprecated", "move to deprecated", "archive stale files", "clean up
  [directory]", any instruction to deprecate/archive GitHub files, or automatically when
  workplan-orchestrator or session-consolidator detect >1 active file in a watched directory.
---

**Model:** Sonnet 4.6 — mechanical file operations.
**Pattern:** GET source → PUT to target deprecated/ path → DELETE source → repeat

---

## Watched Directories

These directories are subject to automatic filing when >1 non-deprecated file is present:

| Directory | Active file rule |
|---|---|
| `workplan/` | Highest version number by filename |
| `versions/current/` | Most recent by filename date |
| `skills/` | All current `_SKILL.md` files are active; deprecated skills are explicitly named by the committer |

**Not watched** (accumulative — all files are permanent records):
- `sessions/` · `references/change-orders/` · `references/search-log/` · `references/bpc/`

**Trigger condition:** a new file was committed to a watched directory this session, OR >1 non-deprecated file is detected at session open/close.

---

## Protocol

### 1. Identify files to file
- List the target directory.
- Identify the active file per the directory's active file rule (above), or as directed by the caller.
- All other non-directory files → candidates for `deprecated/` subdirectory.
- Skip files already in `deprecated/`.
- Skip directory entries.
- Skip files explicitly marked as permanent by the caller.

### 2. For each candidate file:

**Step A — GET source**
```python
content, sha = github_get(source_path, PAT)
# e.g. source_path = "workplan/v10-2-integrated.md"
```

**Step B — PUT to deprecated/**
```python
# target_path e.g. "workplan/deprecated/v10-2-integrated.md"
existing, _ = github_get(target_path, PAT)
if existing is None:
    github_put(
        path=target_path,
        content_string=content,
        sha=None,  # new file
        commit_message=f"github-filing: archive {filename} [YYYY-MM-DD HH:MM]",
        pat=PAT
    )
# If existing is not None: already archived — skip to Step C (still delete source).
```

**Step C — DELETE source**
```python
def github_delete(path, sha, commit_message, pat):
    url = f"https://api.github.com/repos/jordanelias/guidebook/contents/{path}"
    payload = {"message": commit_message, "sha": sha}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={
            "Authorization": f"token {pat}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.v3+json"
        },
        method="DELETE"
    )
    urllib.request.urlopen(req)
```

### 3. Output
Report inline after completion:
- **Kept:** [filename] — reason (active version / permanent)
- **Archived:** [filename list]
- **Skipped:** [filename list] — reason

### Commit message format
`github-filing: archive {filename} [YYYY-MM-DD HH:MM]`

### Error handling
- 409 on PUT: re-GET SHA, retry once.
- File already in deprecated: skip PUT, still DELETE source if present there.
- Directory entries: skip silently.
- Any failure: report filename + HTTP status; continue with remaining files.
- Never abort mid-run — process all candidates before reporting errors.
