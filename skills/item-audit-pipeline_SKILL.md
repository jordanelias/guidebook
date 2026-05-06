---
name: item-audit-pipeline
description: >
  Orchestrates the 8-step per-item audit pipeline sequence, tracking state in
  item_audit_runs across sessions. Runs each skill in order, passes context between
  steps, enforces the citation-miner relevance rule, and hands off cleanly on context
  pressure. Each step can also be invoked individually. Trigger on: "run the audit
  pipeline on [item]", "audit item [code]", "item-audit-pipeline [code]",
  "run pipeline", "start the audit for [item]".
  Decision: D-0150, 2026-05-05.
---

# Item Audit Pipeline (Wrapper)

**Model:** Sonnet 4.6 (routing/orchestration) · delegates to member skill models
**Inputs:**
  - `item_code` (required) — e.g. `I-01`
  - `session` (required) — current session filename
  - `skip_steps` (optional list) — step names already complete in a prior run;
    consolidator reads prior output from DB. Skip only if step appears in
    `steps_complete` of a prior run for this item. Skipping a never-run step → abort.
  - `force_rerun` (optional list) — step names to re-run even if previously complete.
    Deletes current-run-only findings for those steps before re-running.
    Mutually exclusive with `skip_steps` for the same step name.
**Output:** `references/audit-briefs/{item_code}_brief.md` via audit-consolidator
**State:** `item_audit_runs` table in tracking DB

---

## Pipeline Steps (canonical names)

| # | Step name | Skill | Model | Skip if |
|---|---|---|---|---|
| 1 | `connection-discovery-spec` | connection-discovery `--mode spec` | Opus | No BPC slug AND no spec connections |
| 2 | `connection-discovery-evidence` | connection-discovery `--mode evidence` | Opus | `bpc_source_slug IS NULL` for item |
| 3 | `conflict-mapper` | cross-population-conflict-mapper | Sonnet/Opus | Fewer than 2 applicable_groups |
| 4 | `content-gap-analyzer` | content-gap-analyzer | Sonnet/Opus | — |
| 5 | `evidence-auditor` | evidence-auditor | Sonnet/Opus | — |
| 6 | `functional-deficit-auditor` | functional-deficit-auditor | Sonnet/Opus | — |
| 7 | `economics-auditor` | economics-auditor | Sonnet | — |
| 8 | `audit-consolidator` | audit-consolidator | Sonnet | Never skip — always runs last |

Step 8 always runs regardless of skip_steps — it reads whatever is in the DB.

---

## Pre-flight Protocol

### PF-1: Validate item exists

```bash
python3 scripts/db.py items | python3 -c "
import sys, json
items = json.load(sys.stdin)
item = next((i for i in items if i['item_code']=='{item_code}'), None)
if not item:
    print('ERROR: item_code not found in items table')
    sys.exit(1)
print('FOUND:', item['item_code'], '—', item['name'])
print('applicable_groups:', item['applicable_groups'])
print('bpc_source_slug:', item['bpc_source_slug'])
"
```

### PF-2: Check for prior run (resume or fresh start)

```bash
python3 scripts/db.py audit-runs --item {item_code}
```

If a prior run exists with status `IN-PROGRESS` or `HANDED-OFF`:
- Load `steps_complete` and `steps_started` from that run
- Any step in `steps_started` but not `steps_complete` → mid-step failure → re-run that step
- Use the prior run's `run_id` (do not create a new run record)

If no prior run exists: create one:
```bash
python3 scripts/db.py add-audit-run \
  --item-code {item_code} \
  --session {session} \
  --spec-hash {MD5 of normalised spec text}
```

### PF-3: Validate skip_steps and force_rerun

For each step in `skip_steps`:
- Confirm it appears in `steps_complete` of a prior run for this item
- If not found → abort with: `ABORT: {step} in skip_steps but not in any prior steps_complete for {item_code}`

For each step in `force_rerun`:
- Confirm it does not also appear in `skip_steps` for this run
- If conflict → abort with: `ABORT: {step} appears in both skip_steps and force_rerun`

### PF-4: Spec hash check (on resume)

```python
import hashlib, re

def spec_hash(text):
    text = text.strip()
    text = '\n'.join(line.rstrip() for line in text.split('\n'))
    text = re.sub(r'^---\n.*?---\n', '', text, flags=re.DOTALL)  # strip frontmatter
    return hashlib.md5(text.encode()).hexdigest()
```

On resume: recompute hash of current spec. Compare to `spec_hash` in `item_audit_runs`.
If mismatch:
```
WARN: Spec has changed since last run for {item_code}.
  Stored hash:  {stored}
  Current hash: {current}
Options:
  [R] Restart pipeline (re-run all steps against new spec)
  [C] Continue with stale-state flag in brief
```
Prompt user. Do not continue silently. Record choice in session notes.

---

## Execution Protocol

For each step in order (1 through 7):

### Before step begins

```bash
# Record step as started (before any work)
python3 scripts/db.py update-audit-run \
  --run-id {run_id} \
  --session {session} \
  --steps-started '{json array including this step}'
```

### If step is in skip_steps

- Do not invoke the step skill
- Log: `SKIP {step_name}: prior output in DB`
- Proceed to next step

### If step is in force_rerun

Delete current-run findings for this step before re-running:
```python
# Delete gaps created by this skill in current run
conn.execute(
    "DELETE FROM gaps WHERE skill=? AND created_by_session=? AND section=?",
    (SKILL_NAME[step], current_session, item_code)
)
# Delete connections created this run with this source_skill
conn.execute(
    "DELETE FROM connections WHERE source_skill='connection-discovery' "
    "AND created_by_session=?", (current_session,)
)
# For conflict-mapper: delete conflicts created this run
conn.execute(
    "DELETE FROM conflicts WHERE item_code=? AND created_by_session=?",
    (item_code, current_session)
)
conn.commit()
```
Then invoke step as normal.

### Invoke step skill

Each step is invoked by loading and running the corresponding SKILL.md protocol.
Key inputs passed to each step:
- `item_code`
- `session` (current session name)
- `item` object (from items table — applicable_groups, bpc_source_slug, name)
- Prior step outputs where relevant (e.g. Step 5 evidence-auditor results → Step 6 FDA)

**Step 2 auto-skip:** If `item.bpc_source_slug IS NULL`, skip step 2 automatically and
log `SKIP connection-discovery-evidence: no BPC slug for {item_code}`.

**Step 3 auto-skip:** If applicable_groups has fewer than 2 distinct populations after
normalisation (`[p.strip() for p in ag.split(',')]`), skip conflict-mapper and log
`SKIP conflict-mapper: fewer than 2 populations`.

**Step 3 multi-run (>3 active domains):**
Invoke conflict-mapper iteratively in batches of 3 domains. After each batch, query
`conflicts WHERE item_code=?` and pass already-resolved domain codes to the next run
as context to skip. Conflicts table UNIQUE index on (item_code, domain, pop_a, pop_b)
prevents duplicates across batches.

**Citation-miner inline (Steps 1–7):**
When any step encounters a new source:
1. Check `is-mined` for the slug+ref
2. If not mined: mine one depth (backward + forward)
3. Relevance check: does the source's topic/slug overlap with `item_code`'s applicable_groups
   or ICF codes? If YES → include in current audit findings. If NO → log with
   `deferred_reason='not-relevant-to-{item_code}'`.
4. Hard depth-1: never mine sources discovered during mining.

### After step completes

```bash
python3 scripts/db.py update-audit-run \
  --run-id {run_id} \
  --session {session} \
  --steps-complete '{json array including this step}'
```

### Context pressure handling

After each step, estimate remaining context. If >85% of context window used:
1. Complete the current step fully
2. Update `steps_complete` and `steps_started` in DB
3. Commit DB to GitHub
4. Set run status to `HANDED-OFF`:
   ```bash
   python3 scripts/db.py update-audit-run \
     --run-id {run_id} \
     --session {session} \
     --status HANDED-OFF
   ```
5. Print handoff note:
   ```
   HANDOFF: {item_code} audit paused at context limit.
   Completed steps: {steps_complete}
   Next step: {next_step_name}
   Resume command: "resume item-audit-pipeline {item_code}"
   Run ID: {run_id}
   ```

---

## Step 8 — audit-consolidator

Always runs last regardless of skip_steps.

```bash
python3 scripts/audit_consolidator.py \
  --item {item_code} \
  --session {session}
```

Updates `item_audit_runs` status → `COMPLETE` with `brief_path` set.

---

## Final commit

After Step 8 completes:

```bash
# Commit DB
# Message: item-audit-pipeline: {item_code} pipeline COMPLETE {steps_complete} [YYYY-MM-DD HH:MM]
```

---

## Output summary (inline after pipeline completes)

```
ITEM-AUDIT-PIPELINE COMPLETE
Item: {item_code} — {item_name}
Run ID: {run_id}
Steps completed this session: {list}
Steps skipped (prior output): {list}
Steps force-rerun: {list}

Total gaps: N (AUDT: N · RP: N · EC: N · EG: N · CONF: N · other: N)
Total conflicts: N (UNRESOLVED: N · RESOLVED: N)
Total connections (PENDING): N
FDR trigger: YES/NO
Economics trigger: YES/NO

Brief: references/audit-briefs/{item_code}_brief.md
```

---

## Rules

1. `steps_started` is written BEFORE each step; `steps_complete` AFTER. Both must be
   updated atomically — never defer until end of session.
2. A step in `steps_started` but not `steps_complete` on resume = mid-step failure.
   Wrapper re-runs that step from the beginning (steps are idempotent via INSERT OR IGNORE
   and UNIQUE constraints).
3. Skip a step only if it appears in a prior run's `steps_complete`. Never skip a
   never-run step.
4. force_rerun deletes current-session-only findings before re-running. Prior session
   findings are preserved.
5. Citation-miner is always depth-1. deferred_reason is always set for non-relevant sources.
6. Step 8 (audit-consolidator) is never in skip_steps. It always runs.
7. Spec hash normalisation: strip trailing whitespace per line, normalise line endings to
   LF, strip frontmatter timestamps. Whitespace-only changes must not trigger staleness.
8. Conflict-mapper multi-run: each batch ≤3 domains. Wrapper manages domain batching and
   deduplication — each conflict-mapper run is unaware of prior batches.
9. All DB writes must be committed before moving to the next step.
10. On HANDED-OFF: next session resumes by loading the run_id, checking steps_complete,
    and continuing from the first step not in steps_complete.
