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

**Model:** Opus 4.6 (questions must be epistemically tested)
**SQLite:** `data/guidebook.db`

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
