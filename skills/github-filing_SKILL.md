---
name: github-filing
description: >
  Move stale or superseded files to a designated deprecated/ subdirectory within the same
  GitHub directory. Trigger on: "file into deprecated", "move to deprecated", "archive workplan",
  "outdated workplan", "clean up workplan folder", "file stale files", or any instruction to
  deprecate/archive GitHub files within this project. Operates on any directory; workplan/
  is the primary use case. Determines the current active file, moves all others to deprecated/.
---

**Model:** Haiku (mechanical file operations, no judgment required)
**Pattern:** GET source → PUT to target path (sha=None for new) → DELETE source → repeat

---

## Protocol

### 1. Identify files to file
- List the target directory (e.g. `workplan/`).
- Identify the current active file (highest version number, latest date, or as directed).
- All other non-directory files → move to `deprecated/` subdirectory.
- Never touch files already in `deprecated/`.
- Never move directories.

### 2. For each file to move:

**Step A — GET source**
```python
content, sha = github_get(source_path, PAT)
```

**Step B — PUT to deprecated/**
```python
# Check if target already exists first; skip if so.
existing, _ = github_get(target_path, PAT)
if existing is None:
    github_put(
        path=target_path,
        content_string=content,
        sha=None,  # new file
        commit_message=f"github-filing: archive {filename} [YYYY-MM-DD HH:MM]",
        pat=PAT
    )
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
After all moves, list:
- **Kept:** [filename] — active version
- **Archived:** [filename list]
- **Skipped:** [filename list] — already in deprecated or is a directory

### Commit message format
`github-filing: archive {filename} [YYYY-MM-DD HH:MM]`

### Error handling
- 409 on PUT: re-GET sha, retry once.
- File already in deprecated: skip silently, list under Skipped.
- Directory entries: skip silently.
- Any failure: report file name + HTTP status; continue with remaining files.
