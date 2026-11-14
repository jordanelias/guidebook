# Adjudication summary: area E (references/)

(Written by the coordinator from the adjudicator's report: the harness blocked the subagent from writing this file. The counts are re-derivable from `adjudication-E-references.jsonl`.)

## 1. Counts (re-derive, do not trust)
`python3 -c "import json,collections as C;R=[json.loads(l) for l in open('adjudication-E-references.jsonl')];[print(k,dict(C.Counter(r[k] for r in R))) for k in ('verdict','status','resolution','unify')]"`

At writing: 65 records. Verdict CONFLICT 54, NOT-CONFLICT 9, HELD 2. Status frozen-record 45, operative 13, data 3, quoted-for-rejection 2, label 1, other 1. Resolution SUPERSEDE 43, LEAVE 9, AMEND 6, DELETE 5, OWNER-Q 2.

Most SUPERSEDEs need only three ledger entries: one naming `references/audits/bpc-audit-pass0` and `pass2` (2026-05-10); one naming `references/connections/` (prior-version CON files; the `connections` table is empty); one naming the rules at `references/project-standards.md` lines 17, 20, 26, 172 and 355. The ledger is append-only, so its operative rules are superseded, not edited.

The 6 AMENDs are `references/methodology-evidence-hierarchy-mapping.md` lines 33, 39, 58, 165 and 182, plus `references/methodology/economics-methodology-core.md:22`.

The 5 DELETEs move dead files to `_archived/`: `references/connections/application-queue.md` (a queue of tasks for the item-specification-writer skill, which no longer exists, against the dropped item layer; no live reader) and `references/website/data/populations.json` (read only by `_archived` scripts), among others in the jsonl.

## 2. Canonical sentences (passages governed)
- **U5 (24):** "we are showing data, not determining": show each value with its citation; never call it acceptable, adequate, required, mandatory or recommended unless a source says so, and then attribute it.
- **U1 (18):** best = ideal = most accommodating: the identified value that "best responds to an ICF/access need/identity within whatever context"; a source that "simply asserts the value" makes it eligible.
- **U2 (10):** "convergence is not evidence of best practice but most common practice"; a jurisdiction count names the mode, never the best.
- **U6 (8):** "if the only values are from code then code determines the ideal/best", with "the empty circle" carrying that it is not academically or clinically derived.
- **U3 (3):** "the minimum is a factual data point", taken from the code stratum: shown, never rejected or forbidden.
- **U4 (1):** "the minimum in some contexts may be the highest allowable number": order values by accessibility direction.
- **U8 (1):** every value is shown with its citation.

## 3. Owner decisions needed
- In a cell holding both research and code values, where a T4–T6 value is more accommodating than every T1/Co-1/T2/Co-2 value, is the code value the best? This affects `references/project-standards.md` lines 4689 and 4706 (OR-4).
- Which circle a T4/T5-only basis takes (line 26; the mapping file's line 165) is HELD with the circle table.

## 4. Rulings in tension
- OR-4 (best chosen within the anchoring tiers) pulls against the 2026-11-14 "simply asserts the value" statement; "if the only values are from code" can be read either way.
- Line 3611 ("MAXIMUM ACCEPTABLE gradient") pulls against "acceptable isn't relevant"; the direction ruling reframes it: the steepest allowed gradient is the minimum.

## 5. Not flagged by the sweeps, but contradicted by the rulings
- `references/project-standards.md:23`: "Universal design is co-extensive with code compliance — the floor": the owner treats fully universal design as a design mode, and the floor as its own figure.
- `references/project-standards.md:14`: Population Mode has "median as default": a default is a verdict; the median is one of four data points.
- `references/methodology/economics-methodology-core.md:21-23`: the design modes are mislabelled "Tier 0/1/2".
- `governance/mission-and-epistemics.md:46` (area A) carries the same code-consensus-as-best clause as line 20.
- In the LRV connections, the 65% figure is Michelson contrast, a different quantity from the 50% LRV figure; the readers wrongly treated 65% as the more accommodating value.
