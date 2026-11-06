# Register v2: atomic concepts, four new row kinds, sense splits, equivalence skeleton

Proposal for SYNTHESIS decision 3 ("restructure the register", accepted by the owner). Search plan, not vocabulary: no row, alias or term is written; rows reach the base only through `observe-term` → `adjudicate-term` in a research PR after the tooling PR (CLAUDE.md rule 10). Governing: owner 2026-11-06 entries three to six, E1, E4/OR-17, 2026-10-29 (fifth) on "accessible route".

## What changed from v1, and why
- **Criterion statements collapsed into atomic concepts.** v1 seeded passes with 32 recurring RHFAC statements, bare 2.2 words and B651 headings; near-duplicates inflated FOUND (SYNTHESIS defect 4). v2 has one row per quantity, element, technique or setting. A criterion is now the set of rows whose `seed_sources` cite its code ("Surface is firm, stable and slip resistant" ×3 wordings → firm, stable, slip resistant, Floor or ground surfaces). Values, "Well-", "if", "where" and "throughout" clauses are dropped from concepts; the conditions become trigger-rule rows.
- **Four new kinds** (SYNTHESIS 3b): performance criterion, trigger rule, outcome level, drafting layer, seeded from RHFAC/B651 where English has them ("Easy to find", "expected usage", "Visitable", B651 "shall/should/may") and from the passes' reverse harvest.
- **Group (a) concepts and group (c) sense splits** added; each split child has its own id, `split_of` (the parent word) and a discriminating test; `sense_splits.tsv` cites the phrases. Conflation is recorded in `note`, never resolved.
- **E1.** A row first met outside English has `label_en` EMPTY and carries `origin_pair`, `origin_language`, `origin_phrase` verbatim from the pass TSV. English-instrument rows (EN-CA, EN-VARIANTS) carry the wording in `label_en`; `origin_phrase` is then empty so the phrase is not held twice. Every Canadian label is a verbatim substring of a cited criterion, heading or B651 3.1 term.
- **Base cross-reference without copying.** `base_term_id` only where the row is the held term's sense; otherwise empty, with the relation (NARROWER, compound) in `note`. Each of the 10 active parameters has one pointer; the six with no same-sense row get a `base` row with an empty label.

## Columns that need a word
`kind` ∈ quantity / element / technique / setting / performance criterion / trigger rule / outcome level / drafting layer. `discriminating_test` and `technique_tags` (the catalogue's tag vocabulary) are ours, judged, not derived. `place_tags` is empty where the place derives from `seed_sources` (RHFAC section prefix → the `setting` row seeded with that section); filled nowhere yet. `seed_sources`: `RHFAC <codes>`, `RHFAC section <n>`, `B651 <clauses>`, `B651 3.1 '<defined term>'`, or `<PAIR> obs|RH · <jurisdiction> · <instrument> · <locator>` ("(in quote)" when the phrase occurs only in a context quote).

## Counts (2026-11-06; re-run from `register-v2/`, do not trust these figures)
- Rows: `tail -n +2 concepts.tsv | wc -l` → 560. By kind: `tail -n +2 concepts.tsv | cut -f2 | sort | uniq -c` → element 216, drafting layer 67, quantity 72, setting 53, performance criterion 48, trigger rule 48, technique 38, outcome level 18.
- The collapse itself (EN-CA quantity/element/technique/setting): `awk -F'\t' 'NR>1 && $4=="EN-CA" && ($2=="quantity"||$2=="element"||$2=="technique"||$2=="setting")' concepts.tsv | wc -l` → 332, from 640 criteria and 232 headings.
- Loses nothing: `python3 -I -c "import csv,re;R=[r[0] for r in csv.reader(open('../rhfac-criteria.tsv'),delimiter='\t')][1:];s=' '.join(r[11] for r in csv.reader(open('concepts.tsv'),delimiter='\t'));g={c for m in re.findall(r'RHFAC ([0-9AB.,]+)',s) for c in m.split(',')};print([c for c in R if c not in g])"` → only 12.1A.4 and 12.1B.1–5 (user-group headings and a scoring chart) and 12.3.4 (page furniture). B651 headings unseeded: the family headings 4, 4.7, 5.7, 6 and the reference list E.1–E.3.
- Non-English origin (E1): `awk -F'\t' 'NR>1 && $6!=""' concepts.tsv | wc -l` → 180. English-variant origin: `awk -F'\t' 'NR>1 && $4=="EN-VARIANTS"' concepts.tsv | wc -l` → 18.
- Sense splits: `tail -n +2 sense_splits.tsv | wc -l` → 74 child rows; parents `cut -f2 sense_splits.tsv | tail -n +2 | sort -u | wc -l` → 15.
- Base pointers: `awk -F'\t' 'NR>1 && $9!=""' concepts.tsv | wc -l` → 28. Forms: `tail -n +2 forms.tsv | wc -l` → 78.

## forms.tsv (equivalence-class skeleton)
Pre-filled only with: the owner-supplied parking forms plus RHFAC "designated accessible spaces" and B651 "Designated accessible parking" (R2-050); the qualifier class with scope notes (R2-333); elevator/lift from the owner and EN-VARIANTS (R2-163, R2-168, R2-169); and pass forms where one pass recorded two or more distinct verbatim forms of one object, curated to noun forms without values, clauses or a second object (sense as the pass judged it, re-judged in the equivalents wave). Empty `usage_type` = not yet judged. Not copied as parking forms, against SYNTHESIS 3e: PT "lugares especialmente destinados a pessoas em cadeiras de rodas" is wheelchair spectator space (PT RH, Anexo 3.6.1); JA 優先駐車区画 is a second kind of bay (note on R2-051); ES "una plaza accesible por cada 33 plazas" carries a value; US "van accessible" is a narrower class.

## Adopting-instrument key (SYNTHESIS decision 6; proposed, not populated)
A coverage cell is keyed `(concept_id, pair, jurisdiction, adopting_instrument, layer_read)`:
- `pair`: the `lang_jur_map` language-and-jurisdiction pair (e.g. de/DE, fr/BE).
- `jurisdiction`: the adopting body's level, as an ISO 3166-1 country code or an ISO 3166-2 subdivision code where the adopter is sub-national: a German Land, a Spanish comunidad autónoma, an Italian regione, a UK nation, a US or Australian state or a Canadian province, beside the federal level.
- `adopting_instrument`: the instrument as titled, with its edition in force (the Bavarian BayTB adopting DIN 18040, not "DE").
- `layer_read`: regulation (binding) / guidance (deemed-to-satisfy or advice tier) / standard (referenced or voluntary), matching SYNTHESIS defect 6. Its vocabulary must come from the column's CHECK once it exists (rule 8), never from this list.
- Cell state as in catalogue section 5 (NOT-SEARCHED, SEARCHED-FOUND, SEARCHED-ABSENT, SEARCHED-QUERY-FAILED, NOT-OBTAINABLE), so ABSENT always names what was read.

## Deliberately not in v2
The other reverse-harvest rows (route: one instrument per review, SYNTHESIS 5); user and population carves (identity lens; RHFAC 12.1B); values and RHFAC point weights; RHFAC certification levels (no TSV phrase in hand); forms beyond the pre-fill; any cell of the key; a definition for any row. Built by printing from throwaway read-only scripts that are not kept (minimise code); the tables are the artefact.

## Self-attack
1. Seeds come from regexes over criterion text, so a broad row (Height, Seating, door) can carry a wrong code. Detect: read the criterion texts behind any row's `RHFAC` codes.
2. Some merges may settle a conflation by fiat (B651 Headroom into Height clearance, Floor area into Clear space, Dressing rooms into Change Rooms). Detect: `grep -c 'held here' concepts.tsv` and judge each.
3. Policy on cross-language candidates is uneven: some get their own row ("not judged equal"), others only a note. Detect: `grep -c 'not judged' concepts.tsv` and compare.
4. Pass-origin rows inherit the passes' sense judgments, hand-set locators (DA ES FR KO) and transcriptions (IT, PT, ZH). Detect: re-run each pass's `build.py` and read the context quote.
5. The kind of a pass-origin row is mine (IT adeguamento, NL rechtens verkregen niveau, KO 상시보조서비스 could each be trigger or drafting). Detect: compare with the pass's own kind column.

## Links and collapse (2026-11-06; re-run, do not trust these figures)
Typed links in `concept_links.tsv` and a fold proposal in `collapse_proposal.tsv`; method, vocabulary, examined-no-link list and self-attack in `concept_links_README.md`. Links: `tail -n +2 concept_links.tsv | cut -f3 | sort | uniq -c` (0 EQUIVALENT). Rows with a link: `tail -n +2 concept_links.tsv | cut -f1,2 | tr '\t' '\n' | sort -u | wc -l` → 486. Rows after the conservative fold: `tail -n +2 collapse_proposal.tsv | cut -f4 | sort -u | wc -l` → 560; after the moderate fold: `cut -f5` instead → 556. Why rows stay distinct: `tail -n +2 collapse_proposal.tsv | cut -f9 | sort | uniq -c | sort -rn`. Composition by origin: `tail -n +2 collapse_proposal.tsv | cut -f3 | sed 's/ (.*//' | sort | uniq -c` → EN-CA 356, non-English origin 180, EN-VARIANTS 18, base pointer 6.
