# Equivalents pass: shared brief

You run the SECOND pass for one language-and-jurisdiction pair of the Accessible Built Environments Guidebook (`/home/user/guidebook`): equivalence-class discovery over the restructured register. The first pass (your pair's folder `terminology-pass/<PAIR>/`) found the phrases the principal instruments use. This pass finds the OTHER forms that name the same things.

Read first, in full: `CLAUDE.md` (rules 0, 5, 7a, 8, 10; sections 5, 7, 8); the third to sixth entries headed "Owner statements 2026-11-06" in `references/project-standards.md` (English first as search plan; model translations are flagged seeds; the log-the-URL ruling; and the SIXTH: a concept is an equivalence class of forms, equivalence is judged per occurrence by sense, conflation is recorded and not resolved, disfavoured forms are kept with a usage note); `terminology-pass/BRIEF.md` (Equivalence classes and the lessons from the French pilot); `terminology-pass/SYNTHESIS.md` (sections 2, 3 and 6); your pair's `pass-record.md`, `observations.tsv`, `reverse-harvest.tsv`, `coverage.tsv`; and `register-v2/README.md`, `concepts.tsv`, `forms.tsv`.

## The task
For the register-v2 concepts, record every surface form that names the concept in YOUR language and jurisdiction, with its usage type and its attestation. Owner examples of what an equivalence class looks like (English; do not translate them): "accessible parking stall", "handicapped parking", "barrier free parking", "accessibility parking", "disabled parking", RHFAC "designated accessible spaces", B651 "Designated accessible parking" are one concept; "elevator" and "lift"; and the qualifiers accessible / barrier-free / inclusive / universal / wheelchair friendly (equivalent as usage, unequal in scope). Find the analogues in your own language: the code's term, colloquial and signage forms, regional variants, outdated or disfavoured forms (keep them with a usage note), product names, the umbrella qualifier the jurisdiction uses (for example barrierefrei, universell utforming, esteetön, PMR, バリアフリー, 无障碍, accessibilidad universal).

## Sources, in this order (owner decision 5; record which tier each form came from)
1. A second reading of the instruments already read in your first pass (their extracted texts may exist locally under `terminology-pass/<PAIR>/text/`; they are not committed; if absent, re-fetch from the URL in `instruments.tsv`). Look for variant forms of the same concept: synonyms the instrument itself uses, defined terms, alternate spellings.
2. Other statutes and regulations of the jurisdiction that touch the same objects (road and traffic law for parking and kerb ramps, transport and consumer law, planning law).
3. Road-sign, signage and wayfinding manuals of the jurisdiction.
4. Municipal and public-body guidance and public service pages (parking permit pages, accessibility pages of a city, transport operator, public library).
5. Disabled people's organisations' guides (Co-1 sources) in the language: how the community names things, and which forms it rejects.
Do not use news corpora or general web forums as attestation. A model-generated form goes in only as `unattested seed`, flagged, few, and never as a finding. Do not translate the owner's English forms into your language.

## Scope and budget
Prioritise the register-v2 concepts of kinds `quantity`, `element` and `setting` that your first pass marked FOUND or FOUND-PARTIAL, then the `performance criterion` / `outcome level` / `trigger rule` rows your pair originated, then the rest. Breadth over depth: declare in your record how many concepts you attempted and which, and stop when budget ends; do not pretend to cover all 560 rows. Always cover the three owner classes in your language: parking, the umbrella qualifier, and the vertical-transport word(s) (elevator/lift/platform lift).

## Judging equivalence
Per occurrence, by the sense the source gives the form. Two forms are equivalent for a concept only if a source uses them for that concept. Where a source uses one form for two concepts, or treats two forms as one, add a CONFLATION note with locator; do not settle it. Where a form is narrower or wider than the concept, say so in `scope_note`.

## Files to write, under `scratchpad/session_2026-11-06-base-vocabulary-review/terminology-pass/<PAIR>/`
- `equivalents.tsv`: concept_id (from register-v2/concepts.tsv), concept_label, form (verbatim), language, jurisdiction, usage_type (code term / colloquial / regional variant / outdated or disfavoured / product name / qualifier / unattested seed), scope_note, attestation_tier (1 to 5 above, or seed), source (title as written, issuer, URL), locator (page number and, where needed, line, or article/clause), quote (verbatim, at most 25 words), conflation_note.
- `equivalents-search-log.md`: every query and fetch verbatim, with a prior expectation written BEFORE the result, the result, and a note on query shape; keep empties.
- `equivalents-record.md` (at most 40 lines, verdict first): concepts attempted vs not, forms found by usage type and tier (counts by command), the owner classes in your language, conflations, what you could not obtain, and a five-line self-attack.
Retrieve every document through `retrieval_log.fetch` run from the repository ROOT (`cd /home/user/guidebook && python3 -c "import sys; sys.path.insert(0,'scripts/research'); import retrieval_log as r; r.fetch(URL, session='session_2026-11-06-base-vocabulary-review', purpose='equivalents <PAIR>: <what>')"`); the manifest line (URL, hash) is the persistence the owner wants; the file itself is not committed. Use the Wayback `if_` route for blocks (CLAUDE.md section 7). Locators are page number and, if need be, line.

## Prohibitions
Do not write `data/guidebook.db`, run `db.py` write verbs or migrations, commit or push; write nothing outside your `terminology-pass/<PAIR>/` folder and the retrieval log. Invent no citation, URL, locator or quotation; every quote must come from bytes you retrieved. No pre-reset item codes (letter, hyphen, two digits). Canadian English in your own prose; objective tone.

Reply in at most 10 lines: verdict, concepts attempted, forms by tier, the three owner classes in your language (one line each), the most surprising conflation, and what blocked you.
