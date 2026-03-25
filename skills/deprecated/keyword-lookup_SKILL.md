---
name: keyword-lookup
description: >
  Return native-language search terms for a given accessibility concept slug and language set.
  ALWAYS use this skill at the start of any multilingual-research run (Step 0), before generating
  search queries. Returns terms of art used by practitioners, researchers, and regulators in each
  jurisdiction — not English translations. Trigger on: "keyword lookup", "native terms for",
  "search terms in [language]", or automatically when multilingual-research Step 0 runs.
---

**Model:** Haiku 4.5 (lookup only; no judgment required)
**Source:** Research Meta-Analysis & Multilingual Keyword Compendium (project file)
**Output:** Compact table of native-language terms per language per concept

---

## Step 1 — Resolve Slug to Concept Group

Map the incoming slug to its concept group(s) in the Keyword Compendium:

| Slug pattern | Concept Groups |
|---|---|
| `*corridor*`, `*width*`, `*clearance*` | CG 3.1 Corridor Width |
| `*signing*`, `*sign-language*`, `*deaf-space*` | CG 2.1 Deaf terms; CG 2.2 Signing Space |
| `*hearing-loop*`, `*induction-loop*` | CG 3.3 Hearing Loop |
| `*tactile*`, `*TWSI*`, `*TGSI*` | CG 3.2 Tactile Walking Surfaces |
| `*deafblind*`, `*haptic*`, `*protactile*`, `*vibrotact*` | CG 2.3 DeafBlind; CG 3.4 Vibrotactile |
| `*visual-impair*`, `*blindness*`, `*low-vision*` | CG 2.4 Visual Impairment |
| `*OFS*`, `*ME-CFS*`, `*POTS*`, `*fatigue*` | CG 2.5 OFS |
| `*toilet*`, `*wet-room*`, `*bathroom*` | CG 3.5 Accessible Toilet |
| `*social-model*`, `*barrier-free*`, `*accessibility*` | CG 1.1–1.3 Core Concepts |
| `*universal-design*` | CG 1.2 Universal Design |

---

## Step 2 — Return Native Terms Table

For each language requested, return:
- The native-language term of art (not a translation of the English term)
- The governing standard or organisation that uses this term (where known)
- A flag if the concept has no direct equivalent in that language

**Output format:**

```
KEYWORD LOOKUP: {slug} | {population codes}
Concept groups matched: {CG list}

| Language | Native term(s) | Governing source | Note |
|---|---|---|---|
| SV | ... | BBR/Boverket | — |
| NO | ... | TEK17 | — |
...
```

**Always include IE and SG** — these are standing jurisdictions:
- IE: Use CEUD "Building for Everyone" terminology and Building Regulations Part M:2010 terms
- SG: Use BCA Accessibility Code 2019 terms and SgEnable terminology

---

## Step 3 — Flag No-Equivalent Concepts

Where a native concept has no English equivalent, output:

```
⚠ NO-EQUIVALENT: [Language] — "{native term}" has no direct English equivalent.
  Closest EN: "{approximate}"
  Explanation: {1–2 sentence explanation of the conceptual distinction}
  Action: Preserve native concept in synthesis output. Do not flatten to English.
```

Examples to always flag:
- DE: *Barrierefreiheit* (wider than "accessibility" — encompasses all barriers including attitude/communication)
- NO: *Universell utforming* (statutory rights-based concept; not merely a design philosophy)
- FI: *Esteettömyys* vs *saavutettavuus* (physical barrier-free vs. broader accessibility including cognitive/digital)
- JA: *バリアフリー* vs *ユニバーサルデザイン* (two separate, co-existing policy frameworks; not synonymous)
- ZH: *无障碍* vs *通用设计* vs *包容性设计* (three distinct concepts used in different policy contexts)

---

## Fallback

If the slug does not match any concept group: return the closest group(s) and flag:
```
⚠ PARTIAL MATCH: Slug "{slug}" not directly mapped. Returning terms for related concept(s): {list}
  Recommendation: Supplement with manual term generation using native-language disability discourse for this topic.
```
