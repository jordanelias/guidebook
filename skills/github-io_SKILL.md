---
name: github-io
description: >
  Standardised GitHub read/write/list infrastructure for the guidebook project. ALL skills
  that commit to GitHub MUST call github-io instead of inline curl/python. Eliminates
  duplicate commit boilerplate, provides consistent retry logic, SHA conflict resolution,
  and commit logging. ALWAYS use this skill when any other skill needs to: GET a file from
  GitHub, PUT/update a file on GitHub, list a directory on GitHub, or create a new file on
  GitHub. Trigger on: any GitHub operation from any skill, "commit", "push to GitHub",
  "save to GitHub", "update state file", "write session log", "append to gap register".
  Every GitHub operation in the project goes through this skill — no exceptions.
---

**Model:** Any — no judgment required; pure I/O.
**Repo:** `jordanelias/guidebook` · branch `main`
**PAT:** Provided in Project Instructions §GitHub API. Never hardcode.

---

## Operations

### GET (read file)

```python
import urllib.request, json, base64

def github_get(path, pat):
    """Returns (content_string, sha) or (None, None) on 404."""
    url = f"https://api.github.com/repos/jordanelias/guidebook/contents/{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    })
    try:
        resp = urllib.request.urlopen(req)
        # Handle redirects (GitHub returns 302 for some paths)
        data = json.loads(resp.read().decode())
        content = base64.b64decode(data["content"]).decode("utf-8")
        return content, data["sha"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None, None
        raise
```

**Redirects:** Always use `urlopen` which follows redirects, or `curl -sL`. Raw `curl -s` without `-L` fails on this repo.

### PUT (write/update file)

```python
def github_put(path, content_string, sha, commit_message, pat):
    """
    Write file to GitHub. sha=None for new files.
    Returns True on success, raises on failure.
    """
    url = f"https://api.github.com/repos/jordanelias/guidebook/contents/{path}"
    payload = {
        "message": commit_message,
        "content": base64.b64encode(content_string.encode("utf-8")).decode("ascii")
    }
    if sha:
        payload["sha"] = sha
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="PUT", headers={
        "Authorization": f"token {pat}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.v3+json"
    })
    try:
        urllib.request.urlopen(req)
        return True
    except urllib.error.HTTPError as e:
        if e.code == 409:
            # SHA conflict — re-GET and retry once
            return None  # Signal caller to retry
        raise
```

### PUT with Retry (standard wrapper — use this, not raw PUT)

```python
def github_write(path, content_string, commit_message, pat):
    """
    Full write cycle: GET → PUT → retry on 409 → fallback.
    Returns: "success" | "fallback"
    """
    existing, sha = github_get(path, pat)
    result = github_put(path, content_string, sha, commit_message, pat)
    if result is None:
        # 409 SHA conflict — re-GET and retry once
        _, sha = github_get(path, pat)
        result = github_put(path, content_string, sha, commit_message, pat)
    if result is None:
        # Second failure — fallback
        return "fallback"
    return "success"
```

**Fallback protocol:** On `"fallback"` return, output content as fenced code block with manual paste instructions. Never silently drop state.

### LIST (directory contents)

```python
def github_list(path, pat):
    """Returns list of {name, type, path} dicts."""
    url = f"https://api.github.com/repos/jordanelias/guidebook/contents/{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {pat}",
        "Accept": "application/vnd.github.v3+json"
    })
    resp = urllib.request.urlopen(req)
    items = json.loads(resp.read().decode())
    return [{"name": i["name"], "type": i["type"], "path": i["path"]} for i in items]
```

### APPEND (append to existing file — gap register, project-standards, etc.)

```python
def github_append(path, new_content, commit_message, pat):
    """GET existing content, append new_content, PUT back."""
    existing, sha = github_get(path, pat)
    if existing is None:
        # File doesn't exist — create with new_content only
        return github_write(path, new_content, commit_message, pat)
    updated = existing.rstrip("\n") + "\n" + new_content + "\n"
    result = github_put(path, updated, sha, commit_message, pat)
    if result is None:
        _, sha = github_get(path, pat)
        existing, sha = github_get(path, pat)
        updated = existing.rstrip("\n") + "\n" + new_content + "\n"
        result = github_put(path, updated, sha, commit_message, pat)
    if result is None:
        return "fallback"
    return "success"
```

---

## Commit Convention

All commits follow: `{skill-name}: {action} [{YYYY-MM-DD HH:MM}]`

Examples:
- `session-consolidator: session close [2026-03-25 14:30]`
- `workplan-orchestrator: append GAP-CR-17 [2026-03-25 14:30]`
- `research-log-manager: log slug mobility-grab-bars [2026-03-25 14:30]`

---

## Collision Prevention

When two skills write to the same file in one session (e.g., `workplan-orchestrator` and `session-consolidator` both writing `gap_register.md`):

1. Always GET immediately before PUT — never cache SHA across operations.
2. If a skill performs multiple writes to the same file within a session, each write must GET fresh SHA.
3. Never batch multiple file changes into one PUT — one file per PUT operation.

---

## Bash Shorthand

For inline bash calls (where Python overhead is excessive):

```bash
# GET
curl -sL -H "Authorization: token ${PAT}" \
  "https://api.github.com/repos/jordanelias/guidebook/contents/${PATH}" \
  | python3 -c "import sys,json,base64; d=json.load(sys.stdin); print(base64.b64decode(d['content']).decode())"

# Note: always use -sL (follow redirects). Plain -s fails on this repo.
```

---

## Error Reporting

On any GitHub operation failure, report to calling skill:
```
GITHUB-IO: {operation} {path} — {status_code} {error_message}
```

On fallback: output full content as fenced code block + instructions:
```
⚠ GITHUB WRITE FAILED after retry. Manual action required:
File: {path}
Content follows — paste manually into GitHub.
```

---

## Calling Convention

All skills that previously performed inline GitHub operations must instead describe the operation and execute using the patterns above. Skills do not import `github-io` — they execute the same Python/bash patterns documented here. The skill serves as the single source of truth for how GitHub operations are performed.

**Skills that write to GitHub:** session-consolidator, research-log-manager, workplan-orchestrator, toc-editor, jurisdiction-tracker, and any ad-hoc session work.
