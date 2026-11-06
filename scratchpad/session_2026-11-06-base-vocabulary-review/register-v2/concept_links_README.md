# Concept links and collapse proposal for register v2

These files answer the owner's request of 2026-11-06, "for the 560 concepts, you interrogate them for equivalencies/similarities and assign links accordingly", and the follow-up "as it stands, 560 concepts seems excessive". Nothing in them merges, deletes or relabels a row in `concepts.tsv`. They are a search plan and write nothing to the base (CLAUDE.md rule 10). Every warrant is copied from `concepts.tsv`, `sense_splits.tsv`, `forms.tsv`, `terminology-pass/SYNTHESIS.md` or a pass's `equivalents.tsv` / `reverse-harvest.tsv`. Where a link rests only on our reading, `warrant_kind` is JUDGMENT. The tables were printed by throwaway read-only scripts, which are not kept (minimise code).

## Files
- `concept_links.tsv` has the columns from_id, to_id, link_type, warrant_kind, warrant, confidence, carve_note and note. Each unordered pair appears once.
- `collapse_proposal.tsv` has one line per row: concept_id, kind, origin, conservative_parent, moderate_parent, justifying_link, confidence, parent_evidence, stays_distinct_because and descriptive_label_ours.

## Link vocabulary (the brief's, plus two proposed types)
| Type | Meaning | Direction stored |
|---|---|---|
| EQUIVALENT | A pass or source treats the two rows as one object | either |
| NEAR-EQUIVALENT | Same object family, carved differently; `carve_note` states the difference. "wording only" in the carve_note marks the moderate-fold cases | either |
| BROADER | to_id is the genus of from_id | specific → general |
| PART-OF | from_id is a component of to_id | part → whole |
| ALTERNATIVE-FOR-AIM | Different means, limits or measures for one aim (rise versus run, LRV versus luminance, cover versus heating) | either |
| SENSE-SIBLING | A shared word names different things. Mirrors `sense_splits.tsv`, or the register's own split note for R2-119/R2-120. Children are linked to the family's head row and to any child their test names, not pairwise | either |
| CONFLATED-IN | A source uses one form for both rows. Recorded, not settled | either |
| RELATED | Placed together by a source, a pass or a shared criterion, and none of the above fits. The note says why. This includes a trigger rule and the element it conditions | either |
| **ATTRIBUTE-OF** (proposed) | from_id is a quantity or property measured on the element to_id (tread depth of a stair, force of a door). PART-OF does not fit a quantity | quantity → element |
| **GRADE-BELOW** (proposed) | from_id is a defined lower grade or level of the same system as to_id. This answers the owner's point that graded levels are "defined grades, not synonyms" | lower → higher |

The NEAR-EQUIVALENT families have no parent concept. Hub rows (R2-507 deemed-to-satisfy, R2-513 equivalent facilitation, R2-516 hardship, R2-489 relief, R2-354 should, R2-439 public-building class) are a linking convenience. They are not a standard the other jurisdictions are measured against.

Warrant kinds: PASS (a pass's `equivalents.tsv` or `reverse-harvest.tsv`), REGISTER (`concepts.tsv` note or seed, `sense_splits.tsv`, register README), FORMS (`forms.tsv`), SYNTHESIS, and JUDGMENT (our reading alone, always with a stated reason).

## Coverage of the interrogation (2026-11-06; re-run from `register-v2/`, do not trust these figures)
- Links: `tail -n +2 concept_links.tsv | wc -l` → 479.
- By type: `tail -n +2 concept_links.tsv | cut -f3 | sort | uniq -c | sort -rn` → NEAR-EQUIVALENT 121, RELATED 102, PART-OF 86, BROADER 72, CONFLATED-IN 25, ATTRIBUTE-OF 25, SENSE-SIBLING 24, ALTERNATIVE-FOR-AIM 17, GRADE-BELOW 7, **EQUIVALENT 0**.
- By warrant and confidence: `tail -n +2 concept_links.tsv | cut -f4 | sort | uniq -c` and `cut -f6` on the same file.
- Rows with at least one link: `tail -n +2 concept_links.tsv | cut -f1,2 | tr '\t' '\n' | sort -u | wc -l` → 486 of 560.
- Rows examined and left with no link: `comm -23 <(tail -n +2 concepts.tsv | cut -f1 | sort) <(tail -n +2 concept_links.tsv | cut -f1,2 | tr '\t' '\n' | sort -u) | wc -l` → 74 (listed below).
- Non-English-origin rows with a link (to any row, then to an English-source row): `python3 -I -c "import csv;C={r['concept_id']:r for r in csv.DictReader(open('concepts.tsv'),delimiter='\t')};L=list(csv.DictReader(open('concept_links.tsv'),delimiter='\t'));s={x for r in L for x in (r['from_id'],r['to_id'])};ne=[c for c in C if C[c]['origin_phrase']];print(len(ne),sum(c in s for c in ne),len({a for r in L for a,b in ((r['from_id'],r['to_id']),(r['to_id'],r['from_id'])) if C[a]['origin_phrase'] and not C[b]['origin_phrase']}))"` → 180, 159, 104.

**No link is EQUIVALENT.** No pass recorded two register rows as one object. The passes filed same-object forms under an existing row as forms (`equivalents.tsv`), and v2 gave a non-English phrase its own row only where the carve differs (SYNTHESIS 3a–c) or where the relation was "not judged". The equivalence the owner describes is therefore already in the forms, not in the rows.

## Owner cross-checks
- **Parking**: the class is one row (R2-050) with its forms in `forms.tsv`. R2-051 is a SENSE-SIBLING (B651 9.4 against 9.5, one head noun). R2-405 is a criterion on the bay. ZH keeps one bay with a user order, and JA 優先駐車区画 is not judged.
- **Qualifier class**: the forms sit in R2-333. NEAR-EQUIVALENT rows carry the scope: R2-463 universell utforming (a defined level), R2-464 tilgjengelig (lower level), R2-424 移動等円滑化 (the Act's aim) and R2-402 (an SV register duplicate). CONFLATED-IN: R2-359 accessibilità (umbrella and top grade), R2-445 DA tilgængelig (open to the public) and R2-177 Universal washrooms (a room type). "Wheelchair friendly" has no row and stays a NARROWER owner-supplied form in `forms.tsv`.
- **Elevator and lift**: the owner's "an elevator is a lift" is a form of R2-163 (UK, AU, SG, IE sense), not a link. The links are R2-163–R2-168 CONFLATED-IN (US 410 against UK 3.17, AU, SV) and R2-163 CONFLATED-IN with R2-169, R2-170 and R2-173 (KO, DE, FI, SV). They also include R2-554 BROADER R2-163, and R2-169 and R2-170 BROADER R2-168.
- **Graded levels**: IT R2-359/360/361 PART-OF R2-482, with 360 and 361 GRADE-BELOW 359. NO R2-464 GRADE-BELOW 463. JA R2-466 GRADE-BELOW 467. DE R2-471 GRADE-BELOW R2-333, whose DE form is barrierefrei. ES R2-373 GRADE-BELOW 371 and 372. None of these is a synonym link.

## Examined, no link (74), by reason class
- **Generic quantity or technique; no source places it with another row** (16): R2-001, 002, 015, 019, 030, 033, 040, 041, 043, 044, 106, 107, 213, 219, 255, 352. The notes on 019, 044 and 106 name foreign phrases that are not rows.
- **Element with no equivalent, genus or whole in the register** (17): R2-054, 067, 068, 069, 082, 125, 126, 142, 195, 200, 222, 223, 239, 245, 249, 251, 265. R2-125 and R2-126 share only the word "display", and rule 2 forbids a link on a shared word.
- **Setting, B651 heading-level technique or drafting marker; sharing a section is not equivalence** (17): R2-261, 262 (B651 4.7 headings), 284, 288, 289, 294, 297, 298, 299, 300, 301, 310, 311, 312, 317, 323, and 356 (a B651 drafting marker with no counterpart read).
- **Member of a frame that is not a row** (7): R2-364, 365, 366, 367 (DALCO), 369 and 370 (ES cognitive criteria), and 374 (ES Validación, a co-production step with no counterpart row).
- **Generic trigger** (2): R2-337, 338.
- **Trigger or drafting row (14 non-English-origin, 1 English-variant); no pass or register note places another row with it** (15): R2-426, 438, 443, 448, 452 (AU), 457, 459, 461, 472, 492, 494, 506, 523, 526, 530.

## Collapse proposal (`collapse_proposal.tsv`)
**Rules.**
- **Conservative.** Fold only on EQUIVALENT links of high confidence, plus pure spelling or inflection variants held as separate rows. There are none of either: spelling variants such as manoeuvring and maneuvering are already inside one row.
- **Moderate.** Also fold a NEAR-EQUIVALENT row whose carve_note says the difference is wording only. Never fold where the difference is a different object, limit, grade, level or sense.

**Choice of parent.** The parent is chosen by evidence, never by language. It is the row under which the passes and `forms.tsv` file more forms; the count goes in `parent_evidence`. On a tie, the parent is the row whose source states the distinction, and the column says when that choice is arbitrary.

The four moderate folds are:

| Row folded | Parent | Evidence |
|---|---|---|
| R2-533 plan incliné | R2-083 | 22 forms against 0; the FR pass files the phrase there |
| R2-541 spazi di manovra | R2-021 | 3 forms against 0 |
| R2-402 tillgänglig och användbar | R2-333 | 221 against 1; the SV pass calls it a register duplicate |
| R2-528 É recomendável | R2-354 | tie at 0 |

Each folded row's phrase stays as a form. A descriptive label, if wanted, is marked "(descriptive label, ours)".

**Counts** (re-run from `register-v2/`):
- After conservative: `tail -n +2 collapse_proposal.tsv | cut -f4 | sort -u | wc -l` → 560.
- After moderate: `tail -n +2 collapse_proposal.tsv | cut -f5 | sort -u | wc -l` → 556.
- Upper bound if every "not judged" NEAR-EQUIVALENT link proved wording-only (23 links): `python3 -I -c "import csv;L=list(csv.DictReader(open('concept_links.tsv'),delimiter='\t'));P={}
f=lambda x: x if P.get(x,x)==x else f(P[x])
[P.__setitem__(f(r['from_id']),f(r['to_id'])) for r in L if r['link_type']=='NEAR-EQUIVALENT' and ('wording only' in r['carve_note'] or 'not judged' in (r['carve_note']+r['warrant']).lower())]
print(len({f(r[0]) for r in csv.reader(open('concepts.tsv'),delimiter='\t')}-{'concept_id'}))"` → 537. These pairs need a reading, not a fold.
- **Why rows stay distinct** (one class per row, strongest first): `tail -n +2 collapse_proposal.tsv | cut -f9 | sort | uniq -c | sort -rn` → carve or scope differs 125, component of another row 81, genus or species 78, related only 75, examined with no link 74, different limit, measure or means 27, not judged 23, different sense of a shared word 23, quantity of another row 20, conflated by a source but a different object 18, different grade or level 12, folded 4. The carve classes (carve or scope, limit or measure, grade, sense, conflation) total 205. They are the reason the rows cannot be forms of one another.
- **Composition of the 560 by origin**: `tail -n +2 collapse_proposal.tsv | cut -f3 | sed 's/ (.*//' | sort | uniq -c` → Canadian-English source 356, non-English origin 180, English-variant 18, base pointer 6. **By kind**: `tail -n +2 concepts.tsv | cut -f2 | sort | uniq -c` → element 216, quantity 72, drafting layer 67, setting 53, performance criterion 48, trigger rule 48, technique 38, outcome level 18.

**Reading.** Folding forms does not shrink the register much. The number falls only if the owner narrows what a row is. 214 rows are drafting layers, trigger rules, performance criteria or outcome levels, and 53 are settings, against 326 quantities, elements and techniques (the kind counts above). Removing a kind is a scope decision for the owner, not an equivalence finding.

## Self-attack
1. Most links (357 of 479) rest on REGISTER warrants. Many of those are seed co-occurrence (shared RHFAC or B651 clause numbers), which shows placement, not sense. Detect with `awk -F'\t' '$4=="REGISTER" && $5 ~ /seed/' concept_links.tsv | wc -l` (137 on 2026-11-06), then read the criteria.
2. NEAR-EQUIVALENT is the largest class, and 89 of its 121 links are low confidence. Several cross-jurisdiction families (exemption grounds, deemed-to-satisfy, independence) were linked from register glosses that are ours, not from a pass comparison.
3. The four "wording only" carves are our judgment for R2-541 and R2-528. R2-533 follows the brief's own example, although the FR pass shows the same object, which could equally justify EQUIVALENT.
4. PART-OF from heading position (B651 8.6, 8.7, RHFAC chapter 9) can file a cross-cutting element under one setting. The carve_note names other homes where we saw them, but not all of them.
5. The 74 "examined, no link" rows were judged from labels, notes and seeds, not from the instruments' text. A pass reading the FI, NL, ZH and PT triggers could find partners we missed.
