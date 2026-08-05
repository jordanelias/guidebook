---
name: question-author
description: >
  Generate question_heading atoms for Part 4 specification items. Each question heading
  is the question form of a specification — answerable by yes/no from building inspection,
  referencing the lived experience the spec addresses. ALWAYS use when: authoring question
  headings for new specs, reviewing existing headings, or populating the question_heading
  field in specification records. Trigger on: "question heading", "write the question",
  "question mode", "question for this spec", or when item-specification-writer creates a
  new spec that needs a question_heading.
---

**Model:** Opus-class (questions must be epistemically tested)
**SQLite:** `data/guidebook.db`

> ## ⚠ INOPERATIVE — every SQL statement below targets a table that does not exist
>
> **Checked 2026-08-05 against all 67 tables and views in `data/guidebook.db`:
> there is no `specification` table, and no column named `question_heading`
> anywhere in the database.**
>
> This skill's §3 and §4 issue four statements — one `UPDATE specification SET
> question_heading`, three `SELECT … FROM specification` — and each raises
> `sqlite3.OperationalError: no such table: specification`. The C10 validation it
> cites ("every active specification MUST have a non-null `question_heading`")
> cannot run either. There is no partial path: the skill has no other output.
>
> **Where the table went.** It was never built here. `specification` appears only
> in `scripts/migrate/init_database.py` and `scripts/db/init_db.py`, which
> initialise `data/db/guidebook.db` — the *legacy* file CLAUDE.md §7 flags as "a
> different, legacy file", and which does not exist on disk. `schemas/specification.py`
> still models the table, `question_heading` and all, so this is also a live
> schemas↔SQLite mirror gap: a Pydantic model with no table behind it (CLAUDE.md
> §10 — that drift is a bug, not a convention).
>
> **What would make this operative**, in order: a schema migration creating the
> table (or adding `question_heading` to whatever table should own it — a
> D-SCHEMA decision, Change-Order gated); reconciling `schemas/specification.py`
> against it; then rewriting §3–§4 to route writes through
> `scripts/emit_data_migration.py`, since the canonical DB takes writes only
> through migrations (CLAUDE.md §0 rule 4) and a direct `UPDATE` would be wrong
> even once the table exists.
>
> **The question-heading STANDARD in §1–§2 is unaffected and still good.** It is
> editorial doctrine about what makes a question answerable from inspection, and
> it does not depend on where the answer is stored. Read it; do not run the SQL.
>
> Not retired, because retirement is owner-gated (CLAUDE.md §9 guardrail 4) and
> the standard is worth keeping. Banner-first, per the correction
> `item-specification-writer_SKILL.md` §6 already carries for the same table.

---

## 1. Question Heading Standard

A good question heading:
- Is answerable by yes/no from physical inspection of the built environment
- References the lived experience or functional outcome the spec addresses
- Does NOT repeat the spec title verbatim as a question
- Is short enough to scan (typically 8–15 words)

### Examples
| Item | Spec title | Question heading |
|---|---|---|
| E-08 | Corridor Clear Width ≥1200mm | Can two power wheelchairs pass each other? |
| A-02 | Acoustic Ceiling Panels (NRC ≥0.85) | Can people understand speech without straining? |
| G-03 | Grab Bars in All Accessible Bathrooms | Can someone transfer safely without assistance? |
| B-01 | Circadian Lighting (≥150 EML) | Does the lighting support the body's day-night cycle? |

### Anti-patterns
- "Is the corridor width ≥1200mm?" — restates the spec, doesn't reference lived experience
- "Are acoustic panels installed?" — yes/no but doesn't convey WHY
- "What is the NRC rating?" — not yes/no answerable

---

## 2. Workflow

### For new specs
1. Read the spec's `summary`, `evidence_summary`, `why_md` from SQLite
2. Identify the primary lived experience outcome
3. Draft question heading
4. Test: could an architect answer this at a site visit? Does it make the spec's purpose obvious?
5. Write to SQLite:
   ```sql
   UPDATE specification SET question_heading = '{question}'
   WHERE spec_id = '{spec_id}'
   ```

### For batch authoring
1. Query specs missing question headings:
   ```sql
   SELECT spec_id, item_code, title, summary FROM specification
   WHERE question_heading IS NULL OR question_heading = ''
   ```
2. Author each heading per the standard above
3. Commit batch update

### For review
1. Query all question headings:
   ```sql
   SELECT item_code, title, question_heading FROM specification
   WHERE question_heading IS NOT NULL
   ORDER BY item_code
   ```
2. Check each against the standard
3. Flag anti-patterns for revision

---

## 3. Quality gate

Per C10 validation: every active specification MUST have a non-null question_heading.
```sql
SELECT COUNT(*) FROM specification
WHERE status = 'active' AND (question_heading IS NULL OR question_heading = '')
```
Result must be 0 at C10 gate.
