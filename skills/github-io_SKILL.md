---
name: github-io
description: >
  Standardised GitHub read/write/list infrastructure for the guidebook project. ALL skills
  that commit to GitHub MUST use github-io patterns. Primary API: GitHub GraphQL v4 for
  batch reads (aliased queries) and atomic multi-file commits (createCommitOnBranch mutation).
  REST fallback for directory listings and large-file filtered reads. Trigger on: any GitHub
  operation from any skill.
---

**Model:** Sonnet 4.6 — pure I/O, no judgment required.
**Repo:** `jordanelias/guidebook` · branch `main`
**PAT:** Provided in Project Instructions. Never hardcode. GraphQL uses `bearer` auth; REST uses `token` auth.
**API priority:** GraphQL first. REST only for LIST, APPEND, and files >1 MB.

---

## 1. BATCH READ — GraphQL (primary)

Read 1–20 files in a single API call using GraphQL aliases. Each alias maps to one file path.

```python
import urllib.request, json, base64

def graphql(query, variables, pat):
    """Execute a GraphQL query. Returns data dict or raises."""
    payload = json.dumps({"query": query, "variables": variables}).encode()
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=payload, method="POST",
        headers={"Authorization": f"bearer {pat}", "Content-Type": "application/json"}
    )
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    if "errors" in result:
        raise RuntimeError(f"GraphQL errors: {result['errors']}")
    return result["data"]

def batch_read(paths, pat):
    """Read multiple files in one call. Returns {path: content_string} dict.
    Missing files return None for that path."""
    fragments = []
    alias_map = {}
    for i, p in enumerate(paths):
        alias = f"f{i}"
        alias_map[alias] = p
        fragments.append(f'{alias}: object(expression:"main:{p}") {{ ... on Blob {{ text byteSize }} }}')

    query = "{ repository(owner:\"jordanelias\", name:\"guidebook\") {\n"
    query += "  head: defaultBranchRef { target { oid } }\n"
    query += "  " + "\n  ".join(fragments)
    query += "\n} }"

    data = graphql(query, {}, pat)
    repo = data["repository"]
    result = {}
    for alias, path in alias_map.items():
        obj = repo.get(alias)
        result[path] = obj["text"] if obj else None
    result["_head_oid"] = repo["head"]["target"]["oid"]
    return result
```

**Usage:** `batch_read(["skills/X.md", "skills/Y.md", "sessions/LATEST"], pat)`
**Limits:** ~20 files per call (GraphQL query complexity). Split into multiple calls if >20.
**Cost:** 1 API call + 1 rate-limit point regardless of file count.

---

## 2. BATCH COMMIT — GraphQL (primary)

Commit 1–50 file additions/deletions atomically in a single API call. No SHA management required — uses `expectedHeadOid` for optimistic concurrency.

```python
def batch_commit(additions, deletions, message, pat, head_oid=None):
    """Atomic multi-file commit.
    additions: list of {"path": str, "content": str}  (content = raw string, not base64)
    deletions: list of {"path": str}
    message: commit message string
    head_oid: from batch_read _head_oid, or None to auto-fetch
    Returns: commit OID string.
    """
    if head_oid is None:
        head_oid = _get_head_oid(pat)

    file_additions = [
        {"path": a["path"], "contents": base64.b64encode(a["content"].encode()).decode()}
        for a in additions
    ]

    mutation = """mutation($input: CreateCommitOnBranchInput!) {
      createCommitOnBranch(input: $input) {
        commit { oid changedFilesIfAvailable }
      }
    }"""

    variables = {"input": {
        "branch": {
            "repositoryNameWithOwner": "jordanelias/guidebook",
            "branchName": "main"
        },
        "message": {"headline": message},
        "fileChanges": {
            "additions": file_additions,
            "deletions": deletions or []
        },
        "expectedHeadOid": head_oid
    }}

    try:
        data = graphql(mutation, variables, pat)
        commit = data["createCommitOnBranch"]["commit"]
        return commit["oid"]
    except RuntimeError as e:
        if "Could not update" in str(e) or "expectedHeadOid" in str(e):
            # Head moved — retry once with fresh OID
            head_oid = _get_head_oid(pat)
            variables["input"]["expectedHeadOid"] = head_oid
            data = graphql(mutation, variables, pat)
            return data["createCommitOnBranch"]["commit"]["oid"]
        raise

def _get_head_oid(pat):
    data = graphql(
        '{ repository(owner:"jordanelias", name:"guidebook") { defaultBranchRef { target { oid } } } }',
        {}, pat
    )
    return data["repository"]["defaultBranchRef"]["target"]["oid"]
```

**Usage:**
```python
# Single file
batch_commit(
    additions=[{"path": "sessions/session_001.md", "content": yaml_content}],
    deletions=[],
    message="session-consolidator: session close [2026-03-29 03:00]",
    pat=PAT, head_oid=files["_head_oid"]
)

# Multi-file (16 skill updates in one commit)
batch_commit(
    additions=[{"path": f"skills/{s}_SKILL.md", "content": updated[s]} for s in skills],
    deletions=[],
    message="workplan-orchestrator: batch model assignment update [2026-03-29 03:00]",
    pat=PAT
)
```

**Limits:** GitHub's `createCommitOnBranch` handles up to ~100 files per commit. File contents must be UTF-8 and base64-encoded. Total payload <50 MB.
**Cost:** 1 API call. Atomic — all files commit or none do.

---

## 3. Optimal Workflow Pattern

```
1. Plan all changes in memory (/home/claude/)
2. batch_read() all files needed — single call
3. Edit locally — no API calls
4. batch_commit() all changes — single call
5. Report: "N files committed in 1 atomic commit: {oid}"
```

**Before (REST, 16 files):** 32 API calls, 16 commits, ~6,400 tokens of tool I/O overhead.
**After (GraphQL, 16 files):** 2 API calls, 1 commit, ~800 tokens of tool I/O overhead.

---

## 4. LIST — REST (no GraphQL equivalent needed)

```python
def github_list(path, pat):
    """Returns list of {name, type, path} dicts."""
    url = f"https://api.github.com/repos/jordanelias/guidebook/contents/{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {pat}", "Accept": "application/vnd.github.v3+json"
    })
    resp = urllib.request.urlopen(req)
    items = json.loads(resp.read())
    return [{"name": i["name"], "type": i["type"], "path": i["path"]} for i in items]
```

---

## 5. FILTERED READ — bash (large files)

For files >50 KB where only a subset of lines is needed. Avoids loading full content into context.

```bash
# Gap register — OPEN P1 items only
curl -sL -H "Authorization: token ${PAT}" \
  "https://api.github.com/repos/jordanelias/guidebook/contents/gap_register.md" \
  | python3 -c "import sys,json,base64; d=json.load(sys.stdin); c=base64.b64decode(d['content']).decode(); [print(l) for l in c.split('\n') if '| OPEN |' in l or '| P1 |' in l]"

# Connection register — PENDING HIGH only
curl -sL -H "Authorization: token ${PAT}" \
  "https://api.github.com/repos/jordanelias/guidebook/contents/references/connection-register-active.md" \
  | python3 -c "import sys,json,base64; d=json.load(sys.stdin); c=base64.b64decode(d['content']).decode(); [print(l) for l in c.split('\n') if 'HIGH' in l and 'PENDING' in l]"
```

---

## 6. APPEND — REST + retry (gap register, project-standards)

For files that must be read-modify-written (appending to an existing file). Uses REST because the operation requires the current SHA for optimistic locking.

```python
def github_append(path, new_content, commit_message, pat):
    """GET existing content via REST, append, PUT back."""
    url = f"https://api.github.com/repos/jordanelias/guidebook/contents/{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"token {pat}", "Accept": "application/vnd.github.v3+json"
    })
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    existing = base64.b64decode(data["content"]).decode()
    sha = data["sha"]

    updated = existing.rstrip("\n") + "\n" + new_content + "\n"
    encoded = base64.b64encode(updated.encode()).decode()
    payload = json.dumps({"message": commit_message, "content": encoded, "sha": sha}).encode()
    req = urllib.request.Request(url, data=payload, method="PUT", headers={
        "Authorization": f"token {pat}", "Content-Type": "application/json"
    })
    try:
        urllib.request.urlopen(req)
        return "success"
    except urllib.error.HTTPError as e:
        if e.code == 409:
            return "conflict"  # Caller should retry or use batch_commit
        raise
```

**Note:** Where possible, prefer batch_read → modify in memory → batch_commit over APPEND. APPEND exists for single-file incremental updates during a session (e.g., gap register entries between skill runs).

---

## 7. Commit Convention

All commits: `{skill-name}: {action} [{YYYY-MM-DD HH:MM}]`

Timestamp source: `date -u +"%Y-%m-%d %H:%M"`

---

## 8. Decision Matrix

| Scenario | Operation | Why |
|---|---|---|
| Read 1–20 files | `batch_read()` | 1 API call vs N |
| Read >20 files | Multiple `batch_read()` calls of 20 | GraphQL complexity limit |
| Read + filter large file | Filtered bash | Avoid loading full content into context |
| Write 1–50 files | `batch_commit()` | Atomic, 1 API call, 1 commit |
| Append to gap register mid-session | `github_append()` | Needs current SHA for read-modify-write |
| List directory contents | `github_list()` | REST is simpler for this |
| Delete files | `batch_commit(deletions=[...])` | Atomic with other changes |

---

## 9. Error Reporting

```
GITHUB-IO: {operation} — {error}
```

On unrecoverable failure: output full content as fenced code block + manual instructions. Never silently drop state.
