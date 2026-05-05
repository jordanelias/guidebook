---
name: doctrine-recheck
description: >
  Periodic operational audit of doctrine-operations alignment. Runs every 25 working
  sessions or at each major phase transition. Checks: evidence-tier inversion,
  single-source violations, Co-1 representation drift, doctrine-operations alignment,
  model-routing compliance. ALWAYS use at phase transitions or when triggered by
  session count. Trigger on: "doctrine recheck", "periodic audit", "doctrine alignment",
  "phase transition check", or automatically per CS1 cadence.
---

**Model:** Opus 4.6 (doctrine assessment requires judgment)
**SQLite:** `data/guidebook.db`
**Script:** `scripts/doctrine_recheck.py` (automated checks)

---

## 1. Automated Checks (via script)

Run `python3 scripts/doctrine_recheck.py` which checks:

1. **Evidence-tier inversion:** specs claiming high confidence with only low-tier evidence
2. **Single-source violations:** specs backed by only one source
3. **Co-1 representation:** per-population Co-1 source count vs target
4. **Temporal staleness:** sources older than 10 years without supersession check
5. **Mining coverage:** percentage of Tier 1–3 sources with citation mining complete

---

## 2. Manual Checks (Opus judgment)

After automated checks, Opus assesses:

1. **Doctrine-operations alignment:** Do current skills and workflows still serve the mission?
2. **Epistemic defense:** Could an external critic find evidence-tier overclaiming?
3. **Voice consistency:** Has prose drifted from voice-style standards?
4. **Decision freshness:** Are any PROVISIONAL decisions overdue for resolution?
   ```sql
   SELECT * FROM decisions WHERE status = 'PROVISIONAL'
   AND created_at < date('now', '-30 days')
   ```

---

## 3. Cadence

- Every 25 working sessions (count from session files)
- At every stage transition (B→C, C3→C4, etc.)
- When explicitly requested
- After any major architectural change

---

## 4. Output

```markdown
## Doctrine Recheck — {date}
**Trigger:** {cadence|phase_transition|manual}
**Sessions since last recheck:** {N}

### Automated findings
{script output}

### Manual assessment
{Opus judgment on alignment, drift, freshness}

### Actions required
{list of corrections, ordered by priority}
```
