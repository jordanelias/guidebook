# Delegated resolutions of the owner decision register (OD-01 to OD-30, the delegated twenty)

_Written 2026-11-12 (UTC) by an Opus-class model acting under the owner's delegation of 2026-11-12 (`grep -n -F "I guess opus can do it" references/project-standards.md`). These are **delegated resolutions, not the owner's words**. Each stands until the owner reverses it (delegation condition (b)). No task file, script, schema, governance file, skill or database row was changed in writing this; the only other write is one appended ledger entry per resolved decision in `references/project-standards.md`. Canadian English. Every figure is given as the command that produces it; re-run it, do not trust a number written here._

`sha256sum data/guidebook.db` before this pass: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`. After: the same (recorded again at the end of this file).

## Independent check (condition (d)) and what this file now says

[CORRECTED by review] The second, independent Opus-class review is `workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS-REVIEW.md`. Its verdicts, copied from its own table:

| Decision | Verdict | Contestability | The point that decides it |
|---|---|---|---|
| OD-01 | **CONFIRMED WITH CORRECTIONS** | low on the key; moderate on sub-national roll-up | Sound on the key and on conditions. One sentence ("Coverage and scope roll up through the parent") decides a coverage question that belongs to the reserved OD-04, and the list of known sub-national cases is wrong (four, not two). |
| OD-02 | **CONFIRMED WITH CORRECTIONS** | moderate | Defensible, but it does not engage the owner's own live objective to "render across a multitude of languages" (PS:5222), whose meaning the ledger records as the owner's (PS:5236); it must be labelled a reading under condition (c). It also narrows the 2026-11-06 anti-bias entry beyond its words. |
| OD-12 | **CONFIRMED WITH CORRECTIONS** | low on templates-plus-synthesis-discussion; moderate on "rebuilt" | Reconciles OW-1's "complete prose" rather than sidestepping it, and fits OR-6 and the 2026-10-30 posture. But it repeats a claim the 2026-10-30 Opus critic already falsified ("a rebuilt table has nothing to go stale"), does not say where the "table" lives, and its one-line label hides that model-written text reaches the page. |
| OD-14 | **REFER BACK (as written)** | high | Its decisive warrant is that a standing owner ruling (2026-08-25) lost its force because its reason was later removed. That reason is the recording session's gloss, not the owner's words; the owner actually chose between "fan" and "drop", not between fan-out and judging; and retiring an owner rule by implication is the move the delegation reserved (OD-13, condition (e)). It also collides with an open owner question (GAP-076, MOB or ALL). |

**What was done with it.** Every correction the review lists is applied, in the ledger by appended entries ("Correction 2026-11-12 — to the delegated resolution of OD-nn …"; existing lines are never edited) and in this file by the lines marked `[CORRECTED by review]`. **OD-14 is withdrawn and referred back**; no new resolution of it is issued. The review's "defect common to all four" (every task gate opened on the literal `OD-NN:`) is closed by a ledger convention: a status line and a check line per decision, read through one gate (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`). The plan was folded accordingly; see the build plan at the end of this file and `FOLD-LOG.md`.

**The gate, today, for every decision in the register** (run it; do not trust this sentence):

```
gate(){ s=$(grep -F "$1 STATUS:" references/project-standards.md | tail -1); c=$(grep -F "$1 CHECK:" references/project-standards.md | tail -1); case "$s" in *"ANSWERED BY THE OWNER"*) echo "$1 OPEN (owner)";; *"RESOLVED UNDER DELEGATION"*) case "$c" in *"not required"*|*confirmed*) echo "$1 OPEN (delegated; ${c#*CHECK: })";; *) echo "$1 CLOSED (check: ${c:-none})";; esac;; *) echo "$1 CLOSED (${s:-no status line})";; esac; }
for n in $(grep -o -E '^### OD-[0-9]+' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md | cut -c5-); do gate $n; done
```

## 0. Verdict

- [CORRECTED by review] **Resolved and standing: 18. Referred back: 2 (OD-10 in the first pass; OD-14 withdrawn on review).** Derive: `grep -c '^\*\*Status:\*\* RESOLVED' workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS.md` and `grep -c '^\*\*Status:\*\* REFERRED BACK' workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS.md`. The first pass's line follows, kept as written.
- **Resolved: 19. Referred back: 1 (OD-10).** Derive: `grep -c '^\*\*Status:\*\* RESOLVED' workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS.md` and `grep -c '^\*\*Status:\*\* REFERRED BACK' workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS.md`.
- **Resolved with a part referred back** (the resolved part stands; the named part is the owner's): OD-01 (whether a sub-national jurisdiction owes coverage of its own is OD-04's, reserved), OD-05 (whether a jurisdiction-neutral T1 to T3 study is "evidence from a jurisdiction" under the 2026-09-28 standing order), OD-14 (the wording for part-time wheelchair users), OD-22 (every open owner-queue prompt other than OR-10b).
- **Referred back whole:** OD-10. Two owner statements give `provisional` two different meanings (2026-09-09 evening, the engine computes it from tier arithmetic; 2026-10-30, "provisional means that we have to go back and review the source again"). Either register option would override one of them, which delegation condition (e) forbids.
- **Medium confidence:** OD-03, OD-12, OD-14, OD-22, OD-24 (the seed list of quantity kinds; the granularity rule itself is high), OD-25, OD-30. **Low confidence on one point:** OD-25's line between "similarity" and "commonality" (a reading of two words the owner gave together, without gloss).
- **The four that need the second, independent Opus-class check before they are relied on (condition (d)):** OD-01, OD-02, OD-12, OD-14. Their ledger entries say so.
- **Where this pass disagrees with the audit's labelled recommendation:** OD-29 (the audit said (b); the 2026-09-16 ruling reserves exceptions to the owner, so (a)); OD-14 (the audit said fan out code provisions and judge studies; this pass judges every row by the users it names and fans out only rows that name no one more specific); OD-18 (the audit said confirm as listed; this pass confirms with corrections that the other resolutions require); OD-25 (the audit merged similarity with commonality and added conflict and convergence; this pass keeps the owner's four and leaves conflict and convergence in the homes they already have); OD-03 (a stated combination, not (a) alone); OD-26 (agrees, but on a stronger ground the audit did not state).
- **Working assumption, stated where it bites:** the owner's numbering of the three criteria is their priority order (unratified; the delegation entry marks it). It decides OD-02, OD-12, OD-22 and OD-30, where criterion 2 or 3 pulls against criterion 1.

The criteria, verbatim: "(1) long-term integrity of project in terms of accuracy, academic rigour and provenance, (2) making information legible for different user types, and (3) ensuring comprehensive coverage across all disability lenses, ethical approaches and universal/population/individual design modes". Below they are C1, C2, C3.

**Searches behind every section.** Rulings were searched with `git grep` over `references/project-standards.md`, `decisions/`, `governance/` and `sessions/` (the Grep tool cannot see `sessions/`); the database was read only through `sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)` under `python3 -I`. Line numbers below are of `references/project-standards.md` (PS) at commit `316aef2` unless another file is named; re-find them with the quoted phrase.

---

## OD-01 — Jurisdiction in a determination; jurisdictions below the country; climate and culture

**Status:** RESOLVED (one sub-question referred to OD-04). **Confidence:** high on the key and the conditions; medium on sub-national parents. **Independent check (condition (d)):** required.

**The decision in one line.** One determination per parameter and lens set, with each jurisdiction's figure shown beside it as a spread; climate and cultural context recorded as typed conditions on figures; a sub-national instrument filed under its own code that names its country as parent.

**What I verified.**
- The determination key is ruled: parameter (PS:1317, owner 2026-08-26) and four lens columns (owner 2026-08-28; CLAUDE.md §6). `PRAGMA table_info(specifications)` shows `parameter_id` and the four lens columns and no jurisdiction or language column.
- The owner asked for a per-jurisdiction comparison beside the value, not for per-jurisdiction values: "for ramp gradient, i want there to also be an easy comparison master table where you just see what each jurisdiction has for the value" (PS:4844); "our guidebook doesn't take positions. it just presents what appears to be the most accommodating/gentle best practice … unless an academic article or some professional body improves upon germany's standard, that's identified as the best practice" (PS:4822), which names one best practice drawn across jurisdictions.
- Sub-national instruments are filed under their country today: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute(\"select ref_id, substr(pub_title,1,70), jurisdiction from evidence_sources where ref_id in ('REF-01013','REF-00995')\").fetchall())"` prints the Ontario Building Code under `CA` and a Flemish Government decree under `BE`.
- Climate and culture are already treated as conditions, not keys, in standing project rules: the hot-humid thermoregulation rule (PS:370-373, a provision required "in tropical or subtropical jurisdictions"); "ISO wayfinding specifications … transfer universally without cultural or climate adaptation" (PS:378); the Kawa / PAS 6463 rule "Specify the physics; flag the spatial model" (PS:381, PS:407-411); and `governance/armature_v4_resolutions.md` Q29 (lines 627-644): "Jurisdiction-linked cultural context notes, not a separate cultural dimension … They do not override specifications — they contextualize them." `specifications.cultural_claim_anchor` exists (`select sql from sqlite_master where name='specifications'`).
- Conditions become branches by ruling OR-2: "Branches, and an empty headline when all are conditioned" (PS:4616).
- No ruling on sub-national codes was found (`git grep -n -i -E "sub-national|subnational" -- references/project-standards.md governance decisions sessions`); `sessions/session_2026-11-06-pipeline-batch-2.md:102` lists "sub-national instruments (GAP-077)" as still the owner's, and this delegation now covers it.

**Three-criteria test.**
- C1 (integrity) favours, strongly, keeping the ruled key: a determination per jurisdiction (b) would change a key the owner ruled twice, and would turn a jurisdiction's adoption of a value into a separate "determination", which is the convergence-is-not-evidence trap in another form (`governance/evidence-architecture.md` I3). C1 also favours, strongly, sub-national codes with a parent: filing the Ontario code as Canada misstates the source's own issuing jurisdiction, a provenance error in every row that carries it. And C1 favours typed conditions over notes: a climate condition that changes a figure is a fact about the figure and belongs in a typed cell (owner, 2026-11-06: "we do NOT want to have data joined in cells", PS:4963).
- C2 (legibility) favours (a)/(c): designers and policy makers in a given jurisdiction see their own figure in the comparison table and the best practice above it; a per-jurisdiction determination would show a reader as many "best practices" as there are codes, which the owner rejected in PS:4822.
- C3 (coverage) favours (c): cultural context is one of the ethical approaches the project names (Kawa is "the cultural lens", PS:394-397), and climate decides some provisions for some groups (SCI tetraplegia and heat-sensitive MS in hot-humid climates, PS:370-373). Without typed conditions both vanish into prose.
- No conflict between the criteria. **Rejected:** (b), because it overrides the ruled key (delegation condition (e)) and because C1 and C2 both oppose it; "country level only", because it keeps a known provenance error in place and a page would have to apologise for it.

**Resolution.**
`OD-01: one determination, with typed climate and cultural conditions` and `OD-01: sub-national codes with a parent`, as one answer:
1. One live determination per parameter and lens set; each in-scope jurisdiction's figure is shown beside it in the comparison (T-036), pointing at the figure, never copied into the determination.
2. Where a source conditions a figure on climate or on cultural context, that condition is a typed condition on the figure (T-017's branches), so the determination branches by it; where a source states nothing of the kind but a cultural or climatic caveat is known from another source, it is a pointer note on the determination (`cultural_claim_anchor` or its successor), never a value.
3. A sub-national instrument carries its own code with its country as parent (ISO 3166-2 shape, held as a row in T-024's table). Coverage and scope roll up through the parent. **Referred to OD-04 (reserved):** whether a sub-national jurisdiction owes research coverage of its own, beyond being reached through its country.

[CORRECTED by review] (1) Item 3's sentence "Coverage and scope roll up through the parent" is withdrawn: **the parent is a provenance relation only. Whether a sub-national instrument counts toward its country's coverage, or owes coverage of its own, is OD-04's (reserved).** REF-01013 was admitted because the national standard was blocked (`sessions/session_2026-09-28-research-batch-22-selection.md:72`), so a roll-up would let a provincial code stand in for a country. (2) The warrant for branching by a climatic or cultural condition is OR-2 (PS:4616); the Kawa rule (PS:381) and Q29 warrant only "conditions, not keys", and Q29 is an Opus 4.6 resolution, not an owner ruling. A cultural condition that branches a figure keeps the Kawa rule's flag for Person Mode co-design. (3) Sub-national spelling follows ISO 3166-2 except under the project's `UK` convention (`governance/jurisdiction-philosophy.md` §3.3): England's code takes the `UK` prefix, never `GB`. (4) "Country level only" was understated: GAP-077 offered it as a scope note that costs no tooling and no migration; it was still rejected on C1, because the misfiling stays in every row.

**Reversal condition.** A source class whose values cannot be compared across jurisdictions on one scale for the same parameter and lens (not merely differing values), or the owner stating that the book must present a determination per jurisdiction. [CORRECTED by review: the clause on a parent roll-up misrouting a scope rule is withdrawn with the roll-up.]

**Unblocks.** T-024 (sub-national rows), T-036, and T-037 as far as OD-01 holds it.

**Implied task-file changes (described, not made).** [CORRECTED by review: four held cases, not two — REF-00992 (England, filed `UK`), REF-00995 (Flanders, `BE`), REF-01013 (Ontario, `CA`), REF-01029 (Madrid, `ES`), as GAP-077's row names them (`select description from gaps where gap_id='GAP-077'`).] T-024: seed sub-national rows only on contact, each with parent and admitting ledger entry; `evidence_sources.jurisdiction` for REF-01013 and REF-00995 is corrected forward in a research pull request, never in T-024's tooling PR (rule 10). T-017: name climate and cultural context as condition kinds a source may state, read from the condition vocabulary's one home, not typed in code. T-036: the view is the whole answer; no key change.

---

## OD-02 — The language of a page, and how a translated quotation is shown

**Status:** RESOLVED. **Confidence:** high on showing the original beside the translation; medium on English as the only page language for this edition. **Independent check (condition (d)):** required.

**The decision in one line.** Pages are in English for this edition, with every non-English quotation, term and clause shown in its own language and script with our marked translation beside it; the page language is a parameter of render, never baked into it.

**What I verified.**
- No ruling sets a page language: `git grep -n -i -E "page language|language of (the|a) page|pages in english|written in english" -- governance references/project-standards.md decisions sessions` finds nothing on point; `governance/audience-priority.md` names four audiences and no language.
- Quotations may be translated (ninth statement, PS:5358); a model's wording is never presented as a source's term (OR-17, PS:4713; eighth statement, PS:5209-5211); "English must not be the pivot that decides which concepts exist, what the standard form is, or how a non-English concept is described" (PS:5209).
- Accessibility is a precondition of every page (PS:4847-4848, 4858: WCAG 2.2 AA).

**Three-criteria test.**
- C1 favours showing the original beside the translation, strongly: the reader can check our rendering against the source's own words, and nothing of ours stands alone where the source's words should be. It disfavours (iii) (our wording first, original on request) and disfavours (ii) (many page languages) for now, because every fixed sentence of every page would then be unreviewed translated prose of our own.
- C2 pulls the other way on (ii): the project's audiences include readers in JP, KR, CN, DE, FR and the other P1+P2+P3 jurisdictions, who would read their own language more easily. **Conflict resolved by priority:** C1 outranks C2, and a multilingual reading surface multiplies the prose that must be reviewed before anyone may rely on it (see OD-30). C2 is kept in part: quotations appear in the reader's own language where that is the source's language, and the page language is a render parameter so (ii) remains a data change later, not a redesign.
- C3: avoiding English bias is a coverage concern; the original-beside rule keeps non-English evidence visible as itself rather than as an English paraphrase.
- English pages are not the "English bias" the owner ruled against: those rulings concern which concepts exist and which column is read first (PS:5209-5214), not the language of the reading surface. **Rejected:** (ii) now (C1), (iii) (C1).

**Resolution.** `OD-02: pages in English, originals with marked translations beside them`. Each translated passage is shown with the original first or alongside (never only on request), marked as a translation with its translator and review status (OD-30), and the original carries its language tag so assistive technology reads it in that language (WCAG 2.2 success criterion 3.1.2, Language of Parts). The page language is a parameter of the renderer with English the only value this edition.

[CORRECTED by review] (1) **This is a reading of the owner's own words under condition (c):** the owner's statement of 2026-11-12 asks that the pipeline "render across a multitude of languages and jurisdictions" (PS:5222), and its entry records the meaning of "render across languages" as open and the owner's (PS:5236). This resolution reads it, defensibly and not as what the owner meant, as met in this edition by showing each source's own language, tagged, beside our marked translation, with the page language a parameter. (2) The sentence above that the anti-bias rulings "concern which concepts exist and which column is read first, not the language of the reading surface" is withdrawn. It narrowed the 2026-11-06 entry: the owner's own words are "we are trying to avoid english BIAS", and the recorder's gloss includes "how a non-English concept is described". English pages are held to those rulings, by showing the original first or beside every translation, by never presenting our English as a source's term, and by keeping English one column of the matrix; they are not exempt from them. (3) The C2 bullet's "every fixed sentence of every page would then be unreviewed translated prose of our own" is withdrawn: under OD-12 fixed sentences are a bounded set of templates translatable once per language, and under OD-30 a translation is reviewed before display. English only rests on C1's priority over C2 (unratified), not on that cost. (4) The renderer must emit a page in a second language by data alone (a template set and a page-language value, no code edit), or the parameter is a hard-coded behaviour in effect (seventh statement, PS:5322). (5) T-112's target language is English **for display**; this resolution does not fix the language in which synthesis compares evidence (ninth statement left it open). (6) The audiences "include readers in JP, KR, CN, DE, FR" is an inference from the P1+P2+P3 scope, not a recorded audience.

**Reversal condition.** The owner names a reader community that does not read English as a primary audience, or reviewed translation capacity (OD-30) exists at the scale a second page language needs, or the owner reads "render across a multitude of languages" as pages in several languages.

**Unblocks.** T-037 (as far as OD-02 holds it); T-112 (target language: English).

**Implied task-file changes.** T-037: render the original with its `lang` attribute beside the translation; read the page language as a parameter. T-112: target language English; the NOT FOR SONNET line is revisited under OD-30.

---

## OD-03 — A concept that has no English name

**Status:** RESOLVED. **Confidence:** medium (the direction is clear; the display derivation is a design detail for T-028). **Independent check:** not required by condition (d).

**The decision in one line.** A concept's identity is its neutral id; its names are rows in a forms table (every attested form, any language, one row per occurrence); `canonical_en` is kept as our English descriptive label, never a form; the name shown is derived by the E1 rule, not typed.

**What I verified.**
- `terms.canonical_en TEXT NOT NULL` (`select sql from sqlite_master where name='terms'`); `term_aliases` holds forms keyed by term, alias and language (`pragma table_info(term_aliases)`), with no source or jurisdiction occurrence of its own.
- E1, confirmed by the owner by name ("e1 e3 e4; Appy yes", PS:5041): "A concept first met outside English is named by the instrument's own phrase, in its own language, until an English-language instrument of a P1+P2+P3 jurisdiction is observed naming the same concept" (PS:5049).
- The eighth clarification: an English descriptive label "marked as ours" is allowed; "English is one column of the matrix among others and is not read first, matched first or ranked first" (PS:5209-5214).
- The sixth statement: a concept is an equivalence class of forms, each with usage type and attestation (PS:5164-5170).
- The seventh statement left "how a concept first met outside English is held (`terms.canonical_en` is required)" to the owner's schema decision (PS:5194); this delegation covers it.
- A design exists and approves nothing: `scratchpad/session_2026-11-06-base-vocabulary-review/matrix-design/base-matrix-design.md` §3 (canonical_en as "OUR label … never a form"; forms in `term_forms`; label basis derived by a view).
- Such concepts are imminent, not hypothetical: the eighth clarification answers a report of "180 non-English-origin register rows" (PS:5202) awaiting minting.

**Three-criteria test.**
- C1 favours a forms table, strongly: every name carries where it was found, which is the provenance the sixth and seventh statements require; and it favours deriving the display name (rule 8) over a stored pointer that can disagree with the forms it points at.
- C2 favours keeping an English descriptive label on every concept, so an English page can say what the concept is, while showing the instrument's own phrase as its name (E1).
- C3 favours holding a concept English does not carve on equal footing; (b) alone would still identify it by an English gloss.
- No conflict. **Rejected:** (b) alone (the concept stays named by English: C1, C3, and E1); (c) (forces the decision under time pressure when the register is minted; the rows are waiting).

**Resolution.** `OD-03: forms table; canonical_en kept as our English descriptive label, never a form; the display name derived by E1` — that is, the register's option (a) without a stored display pointer, combined with the part of (b) that keeps an English label. The label's basis (an instrument's own term, or our descriptive label) is derived, not typed. The name shown is the origin instrument's phrase until an English-jurisdiction instrument attests an English form (E1); where several forms qualify, T-028 states the derivation, and a stored, warranted choice is used only where no derivation decides.

**Reversal condition.** T-028's design finds the display name cannot be derived without a judgment on most concepts (then a stored pointer with its warrant), or the owner reverses E1 or the eighth clarification.

**Unblocks.** T-028.

**Implied task-file changes.** T-028: take the matrix design's `term_forms` route (not a second forms home beside `term_aliases`); document `canonical_en` as label; add no label-kind column (derived). Its NOT FOR SONNET status stands.

---

## OD-05 — Evidence from outside the scope that citation mining surfaces

**Status:** RESOLVED (one question referred back). **Confidence:** high. **Independent check:** not required.

**The decision in one line.** Out-of-scope evidence surfaced by mining is staged as a lead with its origin and its jurisdiction, never admitted, until the slug's buckets 1 and 2 are exhausted as the standing order of 2026-09-28 defines; nothing is refused or discarded.

**What I verified.**
- Standing order, owner 2026-09-28: "do not research from countries other than Bucket 1 and Bucket 2 for any slug until those buckets are categorically exhausted"; ACTION (2): "Do not admit evidence from a jurisdiction outside buckets 1–2 for a slug that has not met that bar" (PS:4284-4352). Also 2026-10-30: "do not include countries outside of the major identified countries for now" (PS:4835), and OR-16 "Yes, read what we hold first" (PS:4683).
- Out-of-scope sources are already held: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select jurisdiction,count(*) from evidence_sources group by 1').fetchall())"` (BR, IN and UG appear; the 2026-09-28 ruling says batch 21's UG rows are not unwound).
- The 2026-09-28 ruling leaves the Global South / canonical-24 tension open (PS:4284-4352).

**Three-criteria test.**
- C1 favours not losing primary evidence (against (c)) and not admitting against a standing order (against (a), which delegation condition (e) also forbids). Staging is the only option that keeps the evidence and its origin and admits nothing the order excludes.
- C2: neutral.
- C3 favours staging over refusal: Global South and other non-bucket evidence is where several lenses and ethical approaches are thinnest, and a staged lead keeps it findable for the day the buckets are exhausted.
- **Rejected:** (a) (overrides the standing order), (c) (C1, C3), and the audit's rider "admit T1 to T3 on the owner's word", which is not a delegated answer but a request to the owner (below).

**Resolution.** `OD-05: stage as a lead`. The lead records the mined source it came from, its jurisdiction and its tier as claimed, and is eligible for admission by the ordinary route once the slug's buckets 1 and 2 are exhausted as the 2026-09-28 ruling defines, and subject to the scope OD-04 sets. **Referred back:** whether a study whose finding does not depend on jurisdiction (for example a laboratory study of wheelchair propulsion done in a non-bucket country) is "evidence from a jurisdiction" under the 2026-09-28 order at all. C1 would favour admitting such a T1 to T3 study; only the owner can narrow the order.

**Reversal condition.** The owner answers the referred question, or OD-04 widens the scope, or the buckets are exhausted for the slug.

**Unblocks.** No task; governs mining sessions (T-105 and the citation-miner skill).

**Implied task-file changes.** T-105: a mined out-of-scope candidate is written as a lead (search candidate or source locator) with its origin, never admitted. [CORRECTED in fold] No code is needed: `source_locators` already holds `jurisdiction`, `recovered_from` and `tier_claimed`, and `search_candidates.disposition` already admits `OUT-OF-SCOPE` (`select sql from sqlite_master where name='search_candidates'`). The resolution is carried by a convention in the two mining skills (task T-052): one lead row in the clue store, never a second row restating it.

---

## OD-06 — Which stage assigns the lenses

**Status:** RESOLVED. **Confidence:** high. **Independent check:** not required. *This is a reading of the owner's own words (delegation condition (c)): a defensible reading, not a statement of what the owner meant.*

**The decision in one line.** Judgment assigns the lens codes; evidence harvests the source's own words and concepts and assigns none.

**What I verified.**
- The 2026-11-06 sentence read: "evidence stage must carefully adjudicate sources to assignrelevant populations/access needs/ICF codes properly referenced" (PS:4987).
- The owner's own division of labour, 2026-08-27: "evidence is probably working by doing more cursory scans … listing out all concepts/topics/key words/phrases that appear in the source and then judgment phase will actually do the deep read on it to determine what can be derived from the source" (PS:2004-2006); "you research slugs, evidence research, judge evidence" (CLAUDE.md §3). CLAUDE.md §6: "The crossing is JUDGMENT's output".
- The lens carriers are judgment tables in the stage map: `source_value_extractions` and `evidence_population_match` map to `judgment` (`governance/stage-map.yaml`).

**Three-criteria test.** C1: a lens is a judgment about what a source's finding concerns, which needs the deep read the owner placed at judgment; at admission the source has not been read. C3: OR-1 requires every relevant model to be filled (PS:4614), which can only be done from the full reading. C2: neutral. "Adjudicate" is judgment's verb in the owner's spine. **Rejected:** (b), which would assign lenses before the reading that justifies them.

**Resolution.** `OD-06: judgment assigns the lenses`.

**Reversal condition.** The owner says the 2026-11-06 sentence meant admission-time tagging.

**Unblocks.** Informs T-106 (proceeds as written).

**Implied task-file changes.** None beyond citing the answer in T-106.

---

## OD-07 — What one synthesis row is

**Status:** RESOLVED. **Confidence:** high. **Independent check:** not required.

**The decision in one line.** Synthesis is a separable stage with its own rows (relations, conflicts, convergence, and any judged discussion text) that a determination points at; the engine may compute some of them, and a run may invoke synthesis from any stage, but what synthesis finds is kept.

**What I verified.**
- The spine names synthesis as a stage (CLAUDE.md §3; owner 2026-08-27, "synthesize judgments"). Synthesis-stage tables already exist and a determination already points at one: `specifications.convergence_id REFERENCES convergence_assessment` (`select sql from sqlite_master where name='specifications'`); `governance/stage-map.yaml` maps `convergence_assessment`, `convergence_sources`, `connections`, `connection_targets`, `conflicts` to synthesis. `best_practice_synthesis` no longer exists as a table (`select name from sqlite_master where name='best_practice_synthesis'` returns nothing).
- Owner 2026-11-06: "synthesis will ensure the use of cross referential analysis for table rows" (PS:4989); third statement 2026-11-12: synthesis finds equivalencies, adjacencies, similarities, commonalities "dynamically" (PS:5262); OR-14: the specifications pass is "adjudicating, deriving and synthesizing across rows of related evidence" (PS:4679).

**Three-criteria test.** C1 favours (b), strongly: a relation or a divergence approach that is not kept cannot be cited, checked or reversed, and the next run re-derives it without a record. C2 favours (b): the page's discussion can point at kept rows (OR-6's "note in discussion that it has been disputed", PS:4626). C3 favours (b): cross-lens conflicts and cross-parameter adjacencies are exactly the coverage findings that must persist. The OR-14 sentence is not against (b): the specification pass may call synthesis on demand; the rows it writes still belong to synthesis. **Rejected:** (a), which leaves a ruled stage holding nothing durable.

**Resolution.** `OD-07: separable, with its own rows`. Convergence stays computed by the engine and stored as it is now (a synthesis row the determination points at); relations (OD-25) and conflicts are judged rows; a determination points at the synthesis rows it rests on through a link table, never a list in a cell (PS:4972).

**Reversal condition.** Measured evidence that kept relation rows go stale faster than they are re-judged (a drift check finding most of them out of date), which would argue for recomputing on demand.

**Unblocks.** T-032 (with OD-25 and OD-29 below; OD-19 is reserved and still blocks T-032's engine part).

**Implied task-file changes.** T-032: the determination-to-synthesis link is a link table; relations are rows with judge and warrant.

---

## OD-08 — What an absent cell means

**Status:** RESOLVED. **Confidence:** high. **Independent check:** not required.

**The decision in one line.** No determination row is stored for a cell without a figure; a lens that is relevant and has no figure is recorded as an open, typed gap, and the three meanings of absence are derived.

**What I verified.**
- OR-1, owner 2026-10-29: "Do not store table rows for parameters when there is a missing lens … I expect each and every determination to only have rows for the actual relevant lens" (PS:4614). 2026-10-30: "we do not need to have rows for people where the value is just 'Not set.' that just means that it shouldn't be showing on the page" (PS:4845). The ledger's reading (unratified) of both: "the gaps table still records a missing figure for a lens that is relevant" (PS:4630) and "showing no row and stating the gap, with its link, in the page's Gaps section" (PS:4861).
- No live `pending` determination exists: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select state,count(*),sum(retired_at is null) from specifications group by 1').fetchall())"`.
- The gap carrier exists (`specifications.gap_register_id`, `gaps`) and T-013 types it by parameter.

**Three-criteria test.** C1 favours (a): a `pending` row is a non-determination stored in the determination table, which a view or a reader can mistake for a claim, and it duplicates what the gap already says (rule 5). C2 favours (a) with the gap: a reader is told "not relevant", "not yet researched" or "researched and empty", which a `pending` row cannot distinguish. C3 is the risk: without a row, a relevant lens with no evidence could become invisible. **Resolved by requiring the gap:** a lens judged relevant with no figure gets an open gap naming the parameter and lens, so absence is recorded, not silent. **Rejected:** (b), which keeps a row whose only content is the gap pointer.

**Resolution.** `OD-08: no row`, with the condition that a relevant lens with no figure is recorded as an open gap naming the parameter and the lens, judged at judgment and carried in the cross-stage gap register (OD-11).

**Reversal condition.** A reader-facing need that the cell-status answer (T-034) cannot meet from gaps, searches and readings; or the owner restoring stored `pending` cells.

**Unblocks.** T-019 (the sub-case), T-037 (as far as OD-08 holds it).

**Implied task-file changes.** T-019: in the sub-case, write no row and raise the typed gap (needs T-013 merged; it is Wave 0). The `pending` and `not_applicable` values of the `specifications.state` CHECK become unused by writers; whether to retire them from the CHECK is a later tooling question (rows that hold them are history and stay).

---

## OD-10 — `provisional`: strength of evidence, or a re-read owed

**Status:** REFERRED BACK. **Confidence:** — . **Independent check:** not applicable.

**Why it is referred back.** Two owner statements give the word two meanings, and each register option overrides one of them.
- 2026-09-09 (evening), PS:2684-2700: "you have to compute it", ruling that the cell state is computed by `assess_cell.py` from tier arithmetic, which the entry describes as including "T3-clinical-alone ⇒ provisional"; `governance/evidence-methodology.md` §2.3 (lines 138-160) defines `provisional` as a strength threshold.
- 2026-10-30, PS:4833: "provisional means that we have to go back and review the source again to confirm information accuracy" (the owner's answer 10 begins "stage."). The ledger's reading that this "matches `specifications.state`" and needs "no new field" (PS:4854) is marked `[ASSUMPTION]`, and the audit found it does not hold (`scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md` C-22).
- Option (a) ("strength only") overrides the 2026-10-30 statement; making `provisional` mean "re-read owed" rewrites the ratified state thresholds of `evidence-methodology.md` §2 (evidence-tier doctrine, owner-gated by CLAUDE.md §8); option (b) ("both") makes the state unreadable without the note, which C1 and C2 both oppose. Which the owner meant turns on the question his answer 10 replied to; the transcript that holds it (`session-export-1793395272333`) is not in the repository, and this pass could not read it.

**What would settle it, offered to the owner (not a resolution).** The criteria favour keeping one word for one meaning, and keeping both facts: the cell state keeps its computed strength meaning, and a reading that must be checked again is shown by its own status (an extraction that is `preliminary`, or a follow-up row), carried up to the cell by `has_unverified_sources`. That reading applies the 2026-10-30 sentence to readings, not to the cell state. Only the owner can say whether that is what the sentence meant. Answer forms as in the register.

**Blocks nothing.** The register says no task waits on it.

---

## OD-11 — Which stage owns the gap register

**Status:** RESOLVED. **Confidence:** high. **Independent check:** not required.

**The decision in one line.** The gap register is a cross-stage register; each gap names the stage that raised it (from the contract's stage ids) and what it is a gap in.

**What I verified.**
- `governance/stage-map.yaml` maps `gaps` to `synthesis` and records the dispute in its own words: "The honest answer is a cross-stage register with no single home" (its `disputed:` key).
- Writers across stages: every gap row carries a session (`select created_by_session, count(*) from gaps group by 1`), most of them research batches; the engine writes gaps (`assess_cell`); `evidence_population_match.gap_id` (judgment) and `specifications.gap_register_id` (specification) point into it (`pragma foreign_key_list` on each).
- The walkability instrument routes three research pairs through `gaps` today: `python3 workplan/pipeline-state-graph/walkability.py | grep -E "research<->(judgment|synthesis|specification)"` prints paths through `gap_mining - gaps`.

**Three-criteria test.** C1 favours (a): a gap is raised where it is found, and forcing all gaps through research would either forbid the engine's gap (OD-08 needs it) or misattribute who found it. C2: a gap that names its stage tells a reader where the work is owed. C3: gaps raised at judgment and specification are how a missing lens becomes visible (OD-08). **Rejected:** (b), which would forbid the engine's gaps and break OD-08's condition.

**Resolution.** `OD-11: cross-stage register`.

[CORRECTED in fold] The stage that raised a gap is not given a column now: nothing reads it yet, and `CLAUDE.md` §8 says nothing is added without naming its reader. It is added when the cell-status answer or render needs it. The stage-map change and the walkability run before and after are task T-051.

**Reversal condition.** The stage map gains a stage, or the owner assigns gaps to one.

**Unblocks.** No task was blocked; T-013 proceeds.

**Implied task-file changes.** T-013 (or the task that edits `governance/stage-map.yaml`): mark `gaps` as cross-stage, with the stage that raised each gap typed on the row from the contract's stage ids; **and run `walkability.py` before and after**, because the instrument skips tables it treats as unmapped or infrastructure, and if it treats a cross-stage table that way the three research paths above are lost (D-01 would worsen silently). The instrument must count a cross-stage register as a member of each stage it carries.

---

## OD-12 — How render's prose is produced, and whether it is stored

**Status:** RESOLVED. **Confidence:** medium. **Independent check (condition (d)):** required.

**The decision in one line.** Render assembles every sentence by templates, held in one place, from typed rows; it writes no prose of its own judgment. Any discussion that needs judgment (a divergence approach, a relation, a caveat) is a synthesis-stage row written at the Opus floor and quoted by pointer. The render table is rebuilt in full from its inputs at each build, carries the hash of its inputs, and is never edited or read as a source.

**What I verified.**
- OW-1, owner 2026-10-29: "I expect the render table to be one where the specification table rows have been converted into complete prose, bibliographic information etc accordingly from the preceding tables such that it can be displayed properly on the website repository" (PS:4729). 2026-10-30: "i want it to be coming from database directly in ideal world" (PS:4840); "simply PRESENTING information without claiming correctness myself" (PS:4888); DR-2026-07-21: "we never adjudicate a correct path or conclusion" (cited PS:4892). 2026-08-27: no committed file is a render (CLAUDE.md §3).
- The open prompts this answers: OW-1b and OW-1c (`governance/owner-browser.yaml`; both unanswered). OW-1b's own context: "Fixed templates … read stiffly where a claim is conditional or divergent. A model writes richer text, which can drift from the evidence … must be Opus-class … and needs a record of the inputs it was given and a review."
- Only Opus-class models write best-practice synthesis (CLAUDE.md §6). OR-6: the item's discussion notes a T2 dispute of a T1 value (PS:4626).

**Three-criteria test.**
- C1 favours templates, strongly: every sentence traces to a row; the same inputs give the same text; nothing written at render can drift from the evidence. It favours "rebuilt" over "stored and rewritten": a rebuilt table has nothing to go stale and is no second home of a fact (rule 5), and its input hash still lets a reader see what it was built from.
- C2 pulls toward model-written prose: a divergent or conditional cell reads better in written discussion. **Conflict resolved without giving up C1:** the judged discussion is written where judgment belongs, at synthesis, by an Opus-class model with its warrant, and stored there as a row the template quotes by pointer. The reader gets the richer text; render stays deterministic. This is the register's OW-1b "mixed" option with the model's prose moved from render to synthesis.
- C3: templates over typed lens and condition rows show every lens and branch the data holds; prose written per page can omit one.
- The owner's "render table" (OW-1) is honoured: the table exists and holds the complete prose; it is rebuilt, not maintained. **Rejected:** "written prose, stored" (C1; needs a parity check, which CLAUDE.md rule 5 says makes a dual home permanent); a model writing at render (moves judgment to the surface the owner says must only present).

**Resolution.** `OD-12: templates, rebuilt` — with these terms: (1) templates live in one home and are versioned; (2) judged discussion is a synthesis row at the Opus floor, quoted by pointer, never generated at render; (3) the render table is regenerated in full from the specification and preceding tables at each build, carries an input hash per row, and nothing reads it as a source of a fact; (4) translated passages appear only as OD-02 and OD-30 allow.

[CORRECTED by review] (1) **The label.** The one-line answer is now `OD-12: templates at render; judged discussion as Opus synthesis rows quoted by pointer, shown only once reviewed; render table rebuilt outside the database` (ledger correction). It is **OW-1b's "mixed" option**, with the model's text moved from render to synthesis and **without the owner's review** that both model-writing options offered; that removal is a delegated choice the owner may reverse. (2) In the C1 bullet, "a rebuilt table has nothing to go stale" is withdrawn: the 2026-10-30 critic showed it is untrue of the deployed copy a reader sees (`workplan/2026-10-30-ramp-spec-pages/RENDER-CONTRACT-parameters-3-and-12.md` §8 position 5). The cure is the per-row input hash, read by one named check that compares the deployed rows with their inputs now; without that reader the hash is not added (`CLAUDE.md` §8). (3) **Where the table lives:** a build product outside `data/guidebook.db`, because a table written into the database at every build would need a migration each time (rule 3), append-only and immutable. This departs from OW-1's recorded [ASSUMPTION] that the table lives in the database (an assumption, not owner words). Nothing generated is committed (2026-08-27). (4) A judged-discussion row carries its review status, and a reader is shown it only once an Opus-class instance other than its author has reviewed it, or the page states it is unreviewed. (5) OW-1b and OW-1c are marked "resolved under delegation (ledger, OD-12)", not "answered" — the implied change to T-003 below is corrected accordingly. (6) Both readings of OW-1b (how prose is produced; whether a source's sentence may be translated or rewritten) are answered: templates rewrite no source sentence; translations follow OD-02 and OD-30.

**Reversal condition.** A measured build cost that makes full regeneration impractical (then stored with an input-hash drift check, OW-1c's first option); or readers' testing showing template prose fails the 2026-10-30 legibility requirement ("ensure that minimalism does not come at the expense of readability/legibility", PS:4848) in a way synthesis-row discussion does not cure.

**Unblocks.** T-037 (with OD-02, OD-08, OD-30 above and below).

**Implied task-file changes.** T-037: templates in one home; render reads synthesis discussion rows by pointer; full regeneration with input hashes; no model call in the renderer. T-032: a synthesis row type for judged discussion text, at the Opus floor, with warrant. `governance/owner-browser.yaml` OW-1b and OW-1c are marked answered by pointer to the ledger (T-003's one home). [CORRECTED by review: marked "resolved under delegation (ledger, OD-12)", not "answered".]

---

## OD-14 — Carrying the rows written under `MOB` since the split was ratified

**Status:** REFERRED BACK (withdrawn on review). **Confidence:** — . **Independent check (condition (d)):** done; verdict REFER BACK.

[CORRECTED by review] **This resolution is withdrawn.** The review showed that its decisive argument lets a delegate retire an owner ruling by implication: the "reason" it says was removed (that judging would decide applicability before synthesis) was written by the session that recorded the 2026-08-25 ruling, not by the owner; the owner was asked "fan" or "drop" (`scratchpad/session_2026-08-25-pipeline-smoke-test-mobility/logs/F5-population-split-design.md` §8 item 2), not fan-out against judging; and retiring an owner rule where the later ruling does not name it is reserved (OD-13; condition (e)). It also presupposed the owner's answer to GAP-076 (MOB or ALL for a clause under a disability heading). No new resolution is issued. **The sound, narrower version the review describes, for the owner to take or refuse:** the 2026-08-25 ruling's operative words cover the 31 `item_population_links` rows of a dropped table; every `MOB` figure post-dates 2026-08-27 (`select min(created_at),max(created_at),count(*) from source_value_extractions where identity_code='MOB'`); the grade clause is kept in full; rows whose `MOB` tag rests on a heading wait on GAP-076; `evidence_population_match` has no retirement column (`PRAGMA table_info(evidence_population_match)`), so retiring grades needs a tooling change first; `base_taxonomy_identity.status` takes `deprecated`. Also corrected: "provisionally wrong for one of the two groups" below is the register's wording, not the ruling's (the ruling says the fan-out is "not a judgement that every demand applies equally to both"). The ledger records `OD-14 STATUS: WITHDRAWN, REFERRED BACK TO THE OWNER`; T-102 opens only on `ANSWERED BY THE OWNER`. The text below is the first pass's, kept as the record of what was withdrawn.

**The decision in one line.** Judge every `MOB` row by the users it names (a study by its participants, a provision by the users its text names) and tag it `AMB`, `WHEEL` or both through the link table; fan out to both, flagged as awaiting re-derivation, only the rows that name no one more specific than mobility; never fan out a grade of a study's own participants.

**What I verified.**
- The split, owner 2026-08-25: "yes, AMB and WHEEL to fan out" (PS:1291-1310). Its own reasons: fan-out is "a mechanical carry of the umbrella's union … the anti-erasure choice", because resolving by hand "would decide applicability by inference, before synthesis, which is what `DR-2026-08-24` §2.4 forbids"; and "Not fanned out, ever: `evidence_population_match.study_population` … A grade is a fact about a paper."
- That premise was overruled two days later: "`DR-2026-08-24` §2.4's deferral to synthesis is OVERRULED" (owner 2026-08-27, PS:1999-2000); the crossing is judgment's output (CLAUDE.md §6). OR-1 requires every relevant model filled (PS:4614); OR-1c rules a link table so one figure can carry several codes of one model without being copied (PS:4926, 4934).
- Live state (derive, do not quote): `python3 -I - <<'PY'` / `import sqlite3; c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)` / `print(c.execute("select s.evidence_type, count(*) from source_value_extractions x join evidence_sources s using(ref_id) where x.identity_code='MOB' group by 1").fetchall())` / `print(c.execute("select match_grade,count(*) from evidence_population_match where target_population='MOB' group by 1").fetchall())` / `print(c.execute("select count(*), sum(retired_at is null) from specifications where identity_code='MOB'").fetchall())` / `PY`. On 2026-11-12 this showed figures under `MOB` from codes, frameworks, grey, clinical, Co-1 and systematic-review sources; grades against `MOB`; and no live `MOB` determination. `select identity_code,status from base_taxonomy_identity where identity_code in ('MOB','AMB','WHEEL')` shows `MOB` active and neither new code present. One open determination gate is keyed `MOB` (`select gate_id, parameter_id, resolved_at from determination_gates where identity_code='MOB'`).
- Part-time wheelchair users: the axes are "alternatives, simultaneous for part-time wheelchair users" (PS:1128); the 2026-07-22 rule records that a "physically disabled/wheelchair users" umbrella "erased the ambulatory and part-time-wheelchair disabled" (PS:561) and that communities are "named on their own terms (co-produced)".

**Three-criteria test.**
- C1 favours judging wherever the row says whom it concerns: a fan-out row is, by the ruling's own words, "provisionally wrong for one of the two groups"; a provision that names wheelchair spaces, or a study whose participants are manual wheelchair users, is not about ambulant people. With a link table, judging costs no copy of the figure.
- C3 favours fan-out where the row names no one: dropping the identity tag (option (b)'s consequence) would erase both groups from a provision written for both.
- C2: a reader filtering by `WHEEL` or `AMB` sees figures that concern that group, flagged where the tag is a carry rather than a judgment.
- The 2026-08-25 ruling is not overridden: it governed the 31 item links (a table since dropped), chose fan-out for a reason the owner later removed, and its "never fan out a grade" clause is kept in full. Grades against `MOB` are re-graded against each new target where the study bears on it, as new rows (CLAUDE.md §4: `add-population-match` deliberately takes a second row), and the `MOB` grade rows are retired in place, not deleted.
- **Rejected:** (a) for every row (knowingly writes rows that are wrong for one group when the row says which); (c) as the audit framed it (a provision that names wheelchair users would still be fanned to ambulant people); (b) as framed (erases the unnamed rows).

**Resolution.** `OD-14: judge each row; fan out only rows that name neither group, flagged; never fan out a grade`. `MOB` is retired in place in `base_taxonomy_identity` (status), never deleted; the open gate keyed `MOB` is re-raised against the code its trigger concerns, with the old one resolved by pointer. **Referred back:** the owner's wording for part-time wheelchair users. Until the owner gives it, a gap that concerns them names both codes and states, as its condition, that the person uses both modes.

**Reversal condition.** The owner restating blanket fan-out; or the re-derivation finding that most judged rows needed revision anyway (then judging bought nothing over fan-out).

**Unblocks.** T-102 (and through it T-110), except the gap wording.

**Implied task-file changes.** T-102: the answer is a combination not in the register's three forms; the task must check for this ledger line and implement the rule above, through the link table of T-018, in an Opus-class session.

---

## OD-18 — What "all directions" covers

**Status:** RESOLVED. **Confidence:** high. **Independent check:** not required. *A reading of the owner's own words (condition (c)).*

**The decision in one line.** The entry and re-entry conditions of the top-down specification §3 are confirmed, with corrections that the other resolutions require; an earlier stage's row may record a change in its own state, never a later stage's fact.

**What I verified.** `scratchpad/session_2026-11-12-pipeline-bidirectional-audit/audit/td-requirements-and-interface-spec.md` §3 (lines 331-500 at writing), the three rules at its head ("Re-entry adds, it never rewrites", "A stage answers from its own tables and points for the rest", "An act that happened leaves a row"), §3.1-3.7 and the boundary table B1-B17. The objective (PS:5222); rule 5; the 2026-11-06 schema-shape ruling (PS:4963).

**Three-criteria test.** C1 favours confirming: the conditions are derived from ruled pointers and the write rule, and they keep re-entry additive (provenance). It requires the sub-question's answer to be "status yes, copies no": recording a downstream use on an upstream row (for example a "used in" list on a source) is a second home of the downstream pointer (rule 5); the upstream row's own state (verification standing, retired, superseded-by) is its own fact. C2 and C3: the cell-status answers of §3.9 tell every reader what is held, owed or refused, per lens. **Corrections required by consistency, not by the criteria alone:** (1) §3.6's "pending determination and a gap" becomes "no determination row; an open typed gap" (OD-08); (2) B11's "provisional reading" re-entry stands only as "a skimmed or preliminary reading" until OD-10 is answered; (3) §3.1's "an identity that is not an English string" is met by OD-03's neutral id and forms; (4) §3.5's synthesis rows are those of OD-07 and OD-25; (5) §3.7's render postconditions take OD-02, OD-08 and OD-12. **Rejected:** "confirm as listed" (it would write a `pending` row OD-08 forbids).

**Resolution.** `OD-18: confirm the entry and re-entry conditions of TD §3, with the five corrections in workplan/2026-11-12-bidirectional-pipeline/DELEGATED-RESOLUTIONS.md (OD-18); status updates on earlier rows allowed, copies of later facts forbidden`.

**Reversal condition.** The owner correcting a condition; or a re-entry the pipeline needs that no condition permits (found by T-022's after-test or a stress round).

**Unblocks.** T-022.

**Implied task-file changes.** T-022: write the corrected conditions into the contract; its answer check finds a corrected form, not the "as listed" form.

---

## OD-20 — The owner's edits

**Status:** RESOLVED. **Confidence:** high. **Independent check:** not required. *A reading of the owner's own words (condition (c)).*

**The decision in one line.** The owner's changes are proposals applied through the write path, each a migration carrying the owner's warrant; a computed value is changed by changing its input, never by editing it.

**What I verified.** Owner 2026-10-28: "some kind of interface where I can manually review and edit the different table values/information and have it propagate accordingly" (PS:4580); the ledger's reading that an edit is a proposal through the sanctioned path is `[ASSUMPTION]` (PS:4586). Owner 2026-09-09 (evening): "you have to compute it. I can't handle this load manually" (PS:2684-2700). CLAUDE.md rule 3 (migrations only).

**Three-criteria test.** C1 favours (a), strongly: every change keeps who made it and why, and is reproducible by rebuild. C2: the owner's edit "propagates" because the engine recomputes what depended on it (the ledger's reading of "propagate", PS:4586). C3: neutral. The computed-determination ruling adds one condition: an edit aimed at a determination's state, value or marker is not applied to the determination; it is applied to the figure, source or rule it was computed from, or recorded as a question on the cell (OD-21). **Rejected:** a direct write from the page (breaks rule 3 and the computed ruling; only the owner could order it, and has not).

**Resolution.** `OD-20: proposals through the write path`, with the owner named as the judge and the edit's reason recorded on the row it changes; edits aimed at a computed value are applied to its inputs or raised as an open question on the cell.

**Reversal condition.** The owner ordering a direct-write route.

**Unblocks.** T-039.

**Implied task-file changes.** T-039: route edits to determinations through their inputs or T-021's gate.

---

## OD-21 — A question about a published cell

**Status:** RESOLVED. **Confidence:** high. **Independent check:** not required.

**The decision in one line.** A reader's or the owner's objection to a published value is recorded in the database as an open gate that flags the cell until it is answered by re-derivation or by a recorded answer.

**What I verified.** `determination_gates` exists, has open/resolved columns and a verdict CHECK of four audit verdicts (`select sql from sqlite_master where name='determination_gates'`); one gate is open today. Owner 2026-10-30: "radically transparent for my audience as possible while simply PRESENTING information without claiming correctness myself" (PS:4888). The mission makes questions first-class data (`governance/mission-and-epistemics.md`; PS:4861 item 9(b)).

**Three-criteria test.** C1 favours (a): an objection kept only in a session file is lost provenance, and a value under question that stays up unmarked overstates its standing. C2 favours (a): the reader sees the cell is questioned. C3: objections from disabled readers about their own lens are Co-1-shaped input the book should not discard. The risk (a frivolous objection flags a cell) is bounded: the flag says "questioned", not "wrong", and closing it needs a recorded answer. **Rejected:** (b).

**Resolution.** `OD-21: yes, as an open gate`, the gate recording who raised it, the text of the objection and, when closed, the answer and its warrant.

**Reversal condition.** Gates raised faster than they can be answered, so that flags stop carrying information.

**Unblocks.** T-021.

**Implied task-file changes.** T-021: widen the verdict vocabulary by one question kind; the trigger tier columns, which are NOT NULL, need a value for a reader's question (the design must not invent a tier for it).

---

## OD-22 — Rounding direction for converted lengths, and the other open prompts

**Status:** RESOLVED for OR-10b; the other open prompts are dispositioned, not resolved. **Confidence:** medium. **Independent check:** not required.

**The decision in one line.** A converted figure is shown at the nearest quarter inch or 5 mm that does not state less protection than the source: a minimum never rounds below the source, a maximum never above it.

**What I verified.** OR-10, owner 2026-10-29: "Yes, convert and show both — Round to nearest 1/4" or 5mm." (PS:4667); the ledger kept the stored bound exact and put direction to the owner as OR-10b (PS:4693). OR-10b's own example: at least 30 in is 762 mm, whose nearest 5 mm is 760 mm, below what the source requires (`governance/owner-browser.yaml`). The open prompts: `python3 -I -c "import yaml;d=yaml.safe_load(open('governance/owner-browser.yaml'));print([q['id'] for q in d['decisions'] if 'answered' not in q])"`.

**Three-criteria test.** C1 favours the safe side, strongly: a shown 760 mm under "at least 30 in" misstates the source, and a reader who builds to the shown figure builds below the requirement. C2: the figure stays at the owner's increment and beside the source's own figure. C3: a minimum shown low harms exactly the users the minimum protects. **The ruling's word "nearest" is kept, not overridden:** among increments, the one chosen is the nearest that does not cross the source's bound; when the nearest is on the safe side it is chosen unchanged. The increment the owner set stands. I judge this within the ruling because the ledger itself recorded direction as unanswered (OR-10b) and the owner then delegated this exact question; if the owner reads "nearest" as excluding any direction rule, this resolution is reversed.

**Resolution.** `OD-22: round a minimum up and a maximum down` — stated as: the nearest quarter inch or 5 mm that does not fall on the wrong side of the source's bound; the stored bound stays exact, and the shown figure is marked as converted.

**The other open prompts** (named so the owner can see none was settled by the back door): OW-1b and OW-1c are answered by OD-12 above; OR-1c was answered by the owner on 2026-11-06 (PS:4926) and OR-17b by E4 on 2026-11-06 (PS:5052), so both need only T-003's "answered" mark. **Referred back, not resolved here:** OR-5b, OR-6c, OR-22b, OR-23b (each changes how a tier or marker is reached, which is evidence-tier doctrine, owner-gated by CLAUDE.md §8); OT-2 (a term's definition, which the owner's 2026-10-09 guard "Screen, then you approve" reserves); OR-14b and OR-25 (not resolved in this pass; OR-25's question may already be answered in substance by the read-once statement of 2026-11-12, PS:5226, which only the owner can confirm).

**Reversal condition.** The owner reading "nearest" as excluding a direction rule.

**Unblocks.** T-030.

**Implied task-file changes.** T-030: the rounding rule is held once, as a rule of the converter, read by the engine and the renderer; the stored value stays exact.

---

## OD-24 — How coarse a parameter is, and its quantity kinds

**Status:** RESOLVED. **Confidence:** high on granularity and element; medium on the seed list of kinds. **Independent check:** not required.

**The decision in one line.** Parameters are flat and coarse: one measured quantity, with every clause variation a typed condition and families reached by term pointers; two cases are two parameters only when they cannot be placed on one scale or their accessibility directions differ. A parameter states its quantity kind from a registry of kinds held as data; it need not belong to an element.

**What I verified.**
- Owner 2026-11-12 (second): "approach parameters from a higher level abstract vantage as too many clauses and subclauses means we may lose commonality and therefore can't unify then specify" (PS:5247); its ACTION (2), keep clause-level extractions and reach them by pointer (PS:5254). OR-2: conditions as branches (PS:4616). OR-14: element pages derived from "a typed term pointer to the live determinations of its parameters … never a container" (PS:4699). 2026-08-26: the judgment object is the canonical parameter (PS:1317). Seventh statement 2026-11-12: no hard-coded behaviours (PS:5322).
- Live parameters and their units: `python3 -I -c "import sqlite3;c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(c.execute('select p.parameter_id, t.canonical_en, p.accessibility_direction from base_parameters p join terms t using(term_id)').fetchall())"` and `... print(c.execute('select claimed_unit,count(*) from source_value_extractions group by 1 order by 2 desc').fetchall())`. Ramp gradient and ramp run length are separate parameters on different scales, which the split test keeps apart; many unit cells hold conditions as prose (the `claimed_unit` listing shows "where the height difference is …"), which T-016/T-017/T-108 move into conditions.

**Three-criteria test.**
- C1 favours (a): one parameter per quantity keeps one determination per question; a hierarchy (b) creates parent and child values that must agree (a dual home, rule 5); fine-grained (c) relies on equivalence groups being complete, and the owner's statement names exactly that failure. Clause-level precision is kept as conditions and by pointer, so nothing is lost.
- C2 favours (a): a reader meets one value with its conditions, not a tree.
- C3: the risk of a coarse grain is erasing a group-specific difference. It is met by lenses (a group's difference is a lens on the determination, not a separate parameter) and by the split test (opposite directions make two parameters).
- Element required: no. Requiring an element recreates the container the owner deleted (the item layer, CLAUDE.md §7), and some quantities are of a route, a room or an ambient condition rather than an element; elements reach parameters by typed term pointers, many to many (T-029). **Rejected:** (b), (c); "element required: yes".
- Kinds: rule 8 says derive; a kind is the physical dimension of the quantity, so the vocabulary is held as rows (with T-030's units, which convert only within a kind) and grows by data with a warrant (the seventh statement), not as a fixed CHECK list. The seed is what the live parameters need, derived from them, not invented.

**Resolution.** `OD-24: kinds = length; gradient (rise over run, in ratio, percentage or degrees as notations); force; time; luminous reflectance and its contrast (LRV); colour temperature — held as rows, extended by data with a warrant; element required: no` and `OD-24: flat and coarse`, with the split test above.

**Reversal condition.** A parameter whose cases share a scale and a direction but cannot be determined together without losing a group's difference that lenses and conditions cannot carry; or the add-by-data test (T-047) showing a kind cannot be added without a schema change.

**Unblocks.** T-020, T-109; through T-020, T-029, T-030, T-047.

**Implied task-file changes.** T-020 item 1 says "a CHECK holding exactly the owner's list"; under this answer the kinds are rows a parameter references (so T-047 covers adding one), and `add-parameter --quantity-kind` reads its choices from that table. T-109 assigns each live parameter its kind from the seed.

---

## OD-25 — Which relations synthesis records, and who may judge them

**Status:** RESOLVED. **Confidence:** medium overall; low on the line between similarity and commonality. **Independent check:** not required.

**The decision in one line.** Synthesis records the four relations the owner named, each defined by a test: equivalence, commonality, similarity, adjacency. Conflict and convergence keep the homes they already have. A recorded relation is judged by an Opus-class model or above, with its warrant; candidate relations may be found by any query.

**What I verified.** Owner 2026-11-12 (third): "very dynamic in finding equivalencies/adjacencies/similarities/commonalities so that it can discuss things properly" (PS:5262); second statement: commonality is what lets clauses be unified (PS:5247). Owner 2026-11-06 example of adjacency: "wheel chair swept path analyses for different wheel chairs would inform different space requirements" (PS:4989). Existing homes: `conflicts` and `convergence_assessment` (synthesis, `governance/stage-map.yaml`); `connections.connection_type` CHECK holds CROSS-POPULATION, CROSS-PARAMETER, COMPOUND-INTERACTION, METHODOLOGY (`select sql from sqlite_master where name='connections'`), which describe what is related, not how. The Opus floor for synthesis (CLAUDE.md §6) is untouched by the third statement (PS:5266).

**Three-criteria test.** C1 favours keeping the owner's four distinct, each with a test, because they license different acts: only equivalence and commonality may ground unification; similarity is a lead; adjacency is a constraint between distinct things. Merging similarity with commonality (the audit's list) would let a resemblance ground a unification. C1 also favours not recording conflict and convergence a second time (rule 5) and the Opus floor for a judgment that changes what the book unifies. C2: the discussion can say which relation it rests on. C3: adjacency across lenses and parameters is where compound and cross-population effects appear.
- Definitions (the reading of the owner's words, low confidence on the second and third): **equivalence**, the two name or measure the same thing and are interchangeable; **commonality**, they share an identified element (a quantity, a basis, a root) and differ in others, so they unify on that element with the differences kept as conditions; **similarity**, they resemble each other without an identified shared element, so the relation is a lead for judgment and never a ground to unify; **adjacency**, distinct things that bear on or constrain each other.
- **Rejected:** the audit's five-kind list (merges two of the owner's words; re-homes conflict and convergence); a lower judging class (a recorded relation decides what is unified).

**Resolution.** `OD-25: relations = equivalence, commonality, similarity, adjacency; judged by an Opus-class model or above; conflict and convergence stay in their existing tables; candidates by query at any class`.

**Reversal condition.** The owner glossing similarity and commonality otherwise; or judged relations showing the four cannot be told apart reliably (then merge similarity into commonality and say so).

**Unblocks.** T-032 (with OD-07 and OD-29; OD-19 is reserved and still blocks its engine part).

**Implied task-file changes.** T-032: the relation table carries one relation kind from a CHECK holding these four, a judge, a warrant and a status; T-033's candidates are read-only and never recorded without judgment. T-029's term-to-term pointers in base are not governed by this answer.

---

## OD-26 — An interim stage-pair gate before render exists

**Status:** RESOLVED. **Confidence:** high. **Independent check:** not required.

**The decision in one line.** Wait: no interim gate on a stored baseline; run the instrument as a command at the end of every wave, and before and after any change to the stage map.

**What I verified.** `python3 workplan/pipeline-state-graph/walkability.py | grep "NO PATH"` (run read-only on 2026-11-12, canonical hash unchanged): every NO PATH pair involves render; every pair not involving render has a path. OW-2 registers the instrument once views map to stages (PS:4731, 4761).

**Three-criteria test.** C1 favours waiting: a stored baseline is a curated list (rule 8) that can rot without going red (rule 7a), and while render does not exist no lost path can put a wrong thing into the book, which is CLAUDE.md §8's test for adding a check. C2 and C3: neutral. The one real risk found is OD-11's stage-map change, which could drop the research paths that run through `gaps`; it is covered by requiring that task to run the instrument before and after. **Rejected:** (b).

**Resolution.** `OD-26: wait`.

**Reversal condition.** A wave-end run finds a non-render path lost between waves; then an interim gate is warranted, with its exemption derived from the graph (for example "a stage with no path to any other"), never a stored list.

**Unblocks.** Nothing new; T-038 waits on T-037 as planned.

**Implied task-file changes.** None; OD-11's implied change above carries the before-and-after run.

---

## OD-29 — Does retire-in-place cover link rows?

**Status:** RESOLVED. **Confidence:** high. **Independent check:** not required. *A reading of the owner's own ruling (condition (c)). This disagrees with the audit's recommendation.*

**The decision in one line.** Both retire in place: a connection and an admission edge are data rows, and a delete of either is an exception only the owner rules on, case by case.

**What I verified.**
- The ruling, owner 2026-09-16: "retire in place then" (PS:3538-3590). "This ruling governs DATA ROWS AND IDENTIFIERS, where deleting destroys provenance the project cannot reconstruct … a deleted row loses the fact that it existed." ACTION (4): "Where a row MUST genuinely leave … that is an exception the owner rules on case by case, and it is recorded here." Execution condition: "No row is retired in place until every reader that could surface it filters on status."
- `delete_connection` hard-deletes a connection and its targets (`grep -n "def delete_connection" scripts/db.py`); `unlink_admission`, added 2026-09-26 (after the ruling), deletes the edge and keeps the removed edge as an appended dated note in `search_executions.findings_note` (`grep -n "def unlink_admission" scripts/db.py`; its docstring says so).
- `search_admissions` has a composite key and no status column; `connections.status` has no retired value (`select sql from sqlite_master where name in ('search_admissions','connections')`). Row counts: `select (select count(*) from connections), (select count(*) from search_admissions)`.
- Owner 2026-11-06: "we do NOT want to have data joined in cells … or have data stored in the wrong cell" (PS:4963); CLAUDE.md §4 names "a correction appended to a note" as data joined in a cell.

**Three-criteria test.** C1 favours (a), strongly: a wrong admission edge that is retired keeps the fact that the attribution was once claimed, when and why it was withdrawn; the current note is the very shape the 2026-11-06 ruling forbids. The ruling covers "data rows", and an edge is a data row; "and identifiers" adds identifiers, it does not limit the rule to rows that have one. C2 and C3: neutral. **Rejected:** (b), the audit's choice, because it creates the exception ACTION (4) reserves to the owner (delegation condition (e)); (c) for the same reason.

**Resolution.** `OD-29: both retire in place`. The connection gains a retired status in T-032's reshape; the admission edge gains retired-at, retired-by and reason columns, and a re-link after a retirement is a new row or an explicit un-retirement, decided in that task's design. The execution condition binds: every reader of either table filters on the retired mark before the first retirement (`v_source_admission`, the `results_admitted` arithmetic and the batch gates are the known readers to sweep).

**Reversal condition.** The owner ruling an exception for edges without an identifier.

**Unblocks.** T-032 (how `delete-connection` ends).

**Implied task-file changes.** T-032 as written for the connection. **A task is missing:** nothing in the plan gives `search_admissions` a retired mark or turns `unlink-admission` into a retire verb; it needs a tooling task (or an addition to T-040's sweep). T-006 stays valid as an interim fix of the silent no-op.

---

## OD-30 — Who may translate, and must a translation be reviewed before it is used

**Status:** RESOLVED. **Confidence:** medium. **Independent check:** not required by condition (d).

**The decision in one line.** Any model may draft a translation, recorded with its translator; synthesis may read an unreviewed translation only as an aid, with the Opus-class synthesizer checking every passage it relies on against the original; a reader is shown only a translation reviewed by an Opus-class instance other than its translator, beside the original.

**What I verified.** Ninth statement (PS:5358-5365) leaves translator class and review open; T-049's designed table already carries `translator_kind`, `translator_name`, `status` (`requested`, `translated`, `reviewed`, `rejected`) and reviewer columns (`workplan/2026-11-12-bidirectional-pipeline/tasks/T-049-translation-home.md` item 1). E10 (owner-approved 2026-11-06): "no named native-speaker reviewer is required" for attestation (PS:5058). "I can't handle this load manually" (PS:2684-2700). The figure guard: a translation that changes a figure is refused (AT-109, T-049). An unused second home exists: `evidence_sources.pub_title_en`, `translation_method` and `translation_reviewed` (`select translation_method, translation_reviewed, count(*), sum(pub_title_en is not null) from evidence_sources group by 1,2`).

**Three-criteria test.**
- C1 favours review before reliance and before display: a mistranslated clause can change what a determination says. It does not require the translator itself to be Opus-class, because the gate belongs where the translation is relied on (the audit's reasoning, which this pass accepts), and figures are checked mechanically.
- C3 favours cheap drafting: if translation is expensive, non-English evidence is read less, which is the English bias the owner has ruled against; drafting by any model lets every held language reach synthesis.
- C2 favours review before display: a reader cannot judge an unreviewed rendering, and the original stands beside it (OD-02).
- **Conflict:** C1 would prefer a person to review (option (c)); the project has no named native-speaker reviewer (E10) and the owner has said he cannot carry manual load, so (c) would stop translation altogether, which costs C3 heavily and does not serve C1 in practice. Resolved for an independent Opus-class review, recorded, with the original always shown.
- **Rejected:** (b) (spends the floor on drafting rather than where it protects); (c) (above).

**Resolution.** `OD-30: any model, review before a reader sees it`, the reviewer being an Opus-class instance other than the translator, recorded in the translation's reviewer columns; synthesis relies on a passage only after its Opus-class author has checked it against the original.

**Reversal condition.** A sample of reviewed translations checked by a fluent reader shows errors that change meaning; or the owner names human reviewers (then a person reviews what is shown for any cell whose determination turns on a translated passage).

**Unblocks.** T-112 (who runs it), T-037 (which translations a page may show).

**Implied task-file changes.** T-112: the NOT FOR SONNET line may be relaxed for drafting; review and reliance stay Opus-class. T-049: state the reviewer-class rule in its one home; absorb or point at the unused title-translation columns on `evidence_sources` so translations have one home (rule 5), or list them for T-040's deletion sweep.

---

## Record of this pass

- Delegation conditions applied: (a) every ledger entry says it is a delegated resolution and not the owner's words; (b) each states its reversal condition; (c) OD-06, OD-18, OD-20, OD-29 are labelled as readings; (d) OD-01, OD-02, OD-12, OD-14 say they await the independent check; (e) OD-10 is referred back because both options override an owner statement, and parts of OD-05, OD-14 and OD-22 are referred back for the same class of reason.
- Reserved decisions not touched: OD-04, OD-09, OD-13, OD-15, OD-17, OD-19, OD-23, OD-27, OD-28. Where a resolution meets one, it says so: OD-01 and OD-05 (OD-04), OD-07, OD-25 and OD-29 (OD-19 still blocks T-032's engine part).
- Not verified: the question the owner's answer 10 of 2026-10-30 replied to (OD-10; the transcript is outside the repository); whether `walkability.py` treats a cross-stage table as a member (OD-11; inferred from its output header, not read in its code); the full reader set of `search_admissions` (OD-29; names the known readers only).
- `sha256sum data/guidebook.db` after this pass: `c9ecb8461baf2d36ba73215d991f4b46ab97b25458b6b2e3b471e9b401ab7c4d`, equal to the value at the head of this file. The ledger change is append-only: `git diff references/project-standards.md | grep -c '^-[^-]'` printed 0.
- D-27 after the append: the loop in REMEDIATION-WORKPLAN.md §10 (D-27) prints 1 for each of the nineteen resolved decisions and 0 for OD-10 and the nine reserved ones.

---

## Build plan for the eighteen standing resolutions (added in the fold, 2026-11-12)

Each line says what is built, in which task, of which kind (CLAUDE.md rule 10: tooling merges before the research it unlocks, never in one pull request), what reads what is added, and the test that is red today. Order is by dependency, smallest change first (CLAUDE.md §8: do nothing, a convention, reuse, delete, and only then new code). Every task reads its decisions through the ledger gate (`grep -n -F "Convention 2026-11-12 — how a delegated resolution" references/project-standards.md`) and stops if it prints CLOSED. Tasks are in `tasks/`; dependencies are in each file's section 2 and in `REMEDIATION-PLAN.md` (generated).

| # | Decision | What is built, and why this size | Task (kind) | After | Reads it | Red today |
|---|---|---|---|---|---|---|
| 1 | OD-06 | **Nothing.** Lens assignment is already judgment's (owner 2026-08-27; `stage-map.yaml` puts the lens carriers at judgment). A note in the re-tagging task. | T-106 (RESEARCH) note only | T-019 | — | — |
| 2 | OD-26 | **Nothing.** No interim gate; the instrument runs as a command at each wave end and around stage-map changes (a convention in §6 of the workplan). | T-038 unchanged (after render) | T-037 | — | — |
| 3 | OD-05 | **A convention, no code.** One paragraph in each mining skill: stage an out-of-scope source once in the clue store with `add-locator`; never admit; never discard. The columns already exist. | T-052 (TOOLING, skills) | none | mining sessions; `skill_vocabulary_audit` | `grep -c -E 'OUT-OF-SCOPE\|outside the scope in force'` on the two skills prints 0 |
| 4 | OD-11 | **A governance edit, no column.** `gaps` marked `cross-stage` in the stage map; walkability run before and after; one-line repair to the owner's page builder if it does not know the value. | T-051 (TOOLING) | none | `walkability.py`; `owner_browser_build.py` | the map prints `synthesis` |
| 5 | OD-12, OD-22 (queue) | **Marks in one YAML file.** OW-1b, OW-1c, OR-10b marked "resolved under delegation", a key distinct from `answered`. | T-003 (TOOLING) | none | the owner's page | the three prompts show as open |
| 6 | OD-29 | **Three columns on two tables; two verbs change from DELETE to UPDATE; readers filter.** No new verb. The derived deletable set then refuses `--allow-delete` by itself. | **T-050 (TOOLING, new)** | T-006 | `v_source_admission`; `results_admitted`; the batch gates; T-032 | `unlink-admission` and `delete-connection` remove the row (on a scratch copy) |
| 7 | OD-30 | **One CHECK and a retirement of unused columns** inside the translations task: reviewer ≠ translator; title translations become `translations` rows; `pub_title_en` and its five siblings are writer-retired, reader-retired, NULL forward. | T-049 (TOOLING), then T-112 (RESEARCH, Sonnet drafting) | T-008; T-049 | render (only reviewed rows) | a translation reviewed by its own translator is accepted (once T-049's table exists, this is its first case) |
| 8 | OD-01 | **A parent column on the jurisdiction table T-024 already builds**, provenance only, UK spelling; then the four held cases re-filed as research. Coverage roll-up is not built (OD-04). | T-024 (TOOLING); **T-113 (RESEARCH, new)**; T-036 (TOOLING view) | —; T-024; T-024 and T-101 | the comparison view; render | four sources filed under their country (`D-34`) |
| 9 | OD-24 | **A kinds table and a foreign key, and a deletion:** the T-010 stop-gap (`NON_QUANTITY_DOMAINS` and its refusal) goes in the same pull request. Kinds are rows so a kind is added by data (T-047). | T-020 (TOOLING); T-109 (RESEARCH); T-047 (test) | T-010; T-020 | `add-parameter`; T-030; the engine | `grab bar` becomes a parameter (T-020 §3) |
| 10 | OD-22 | **One rounding rule in the converter**, inside the units-as-data task; the stored bound stays exact. | T-030 (TOOLING) | T-016, T-020 | the engine; render | 30 in as a minimum would show 760 mm (a new converter case) |
| 11 | OD-08 | **A deletion in the engine:** the path that keeps a `pending` row for a lens no figure carries goes; the gap is raised at judgment with T-013's columns. | T-019 (TOOLING) | T-016, T-017, T-018 | every determination | AT-52 |
| 12 | OD-18 | **One optional list field in the contract schema** and the ruled edges as data, written with the five corrections. | T-022 (TOOLING) | T-002, T-012, T-013 | `pipeline_contract_audit`; `/run-pipeline` | a `re_entry:` key is refused |
| 13 | OD-21 | **A widening of one table** (`determination_gates`): three lens columns, one verdict, a nullable tier for that verdict. | T-021 (TOOLING) | T-019 | the engine report; `v_open_determination_gates`; render | AT-72 |
| 14 | OD-03 | **Design first (one page), then one forms home**, from the 2026-11-06 matrix design; no label-kind column. | T-028 (TOOLING, NOT FOR SONNET) | T-026 | every writer that matches a name; render | AT-25 |
| 15 | OD-07, OD-25, OD-12, OD-29 | **A reshape of two tables that hold no rows**, a link table from determination to synthesis rows, and a judged-discussion row type with a review status. The engine part (OD-19) is split out. | T-032 (TOOLING, NOT FOR SONNET) | T-029, T-050 | T-033; render; the engine | AT-70 |
| 16 | OD-02, OD-08, OD-12, OD-30 | **The renderer:** templates in one home; a build product outside the database with input hashes and one named staleness check; originals tagged beside reviewed translations; a second page language by data alone. | T-037 (TOOLING, NOT FOR SONNET) | T-019, T-032, T-036, T-049 | the reader | AT-35 to AT-39 |
| 17 | OD-20 | **Edits as proposals through the write path**; an edit to a computed value goes to its inputs or to a question (T-021). | T-039 (TOOLING, NOT FOR SONNET) | T-021, T-037 | the owner | AT-42 |

**Sequenced behind decisions that are not delegated, and not built around:**
- **OD-04 (reserved):** T-101, and through T-036 the renderer (T-037) and everything after it (T-038, T-039); whether a sub-national instrument owes coverage.
- **OD-14 (referred back):** T-102 and through it T-110 (the first determinations); T-106 leaves mobility codes alone. Retiring grade rows would also need a tooling change first (`evidence_population_match` has no retirement column).
- **OD-19 (reserved):** T-053 (the engine part split from T-032). T-032 itself does not wait: the register always said OD-19 blocks only "T-032 (the engine part)".
- **OD-23 (reserved):** T-031, and T-105 where an inventory is chosen.
- **OD-10 (referred back):** no task; T-022 writes the B11 edge as a follow-up row and leaves the meaning of `provisional` alone.
- **OD-15, OD-28 (reserved):** T-103, T-023. **OD-09, OD-13, OD-17, OD-27 (reserved):** no task.
