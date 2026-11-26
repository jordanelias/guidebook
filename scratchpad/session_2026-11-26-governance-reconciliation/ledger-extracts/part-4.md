# Current-state extract — references/project-standards.md, slice L3685-L4921

Read-only extract. Owner words are verbatim. "[unratified reading]" marks a recorder's [ASSUMPTION]. "[OPEN]" marks an unanswered question. "[CHECK]" marks a sentence that may be history or rule, or a possible interaction with a later or outside entry that the source does not state.

---

### 2026-09-18 — UK canonical; BE, ES, HR, IT, INT admitted to JurisdictionCode [L3685-L3729]
Owner words: "UK is canonical, add BE HR INT ES IT to the enum"
In force:
- UK, never GB. `scripts/audit/jurisdiction_db_vocabulary.py` enforces it on the database (table list derived from the live schema; rejected spellings parsed from `governance/jurisdiction-philosophy.md`).
- BE, ES, HR, IT, INT are members of `JurisdictionCode`.
- INT is not ISO: `ISO` = an ISO-published standard; `INT` = a work spanning jurisdictions without being one (examples REF-00994, REF-00977).
- Codes live only in `lang_jur_map` (a reference map of places the project may expand into, not held evidence) are NOT admitted; admitting one is a scope decision, not a vocabulary repair. The check exempts that table.
- CONDITION: any session admitting a source whose jurisdiction is not declared, or proposing an addition to `JurisdictionCode`.
- ACTION: (1) Derive what is live before proposing a code, and name which tables carry it (corpus or reference). (2) Never write `GB`. (3) Do not admit a `lang_jur_map`-only code without a scope ruling.
Open:
- [OPEN] `term_aliases.jurisdiction` anomalies: `TW` (Taiwan, undeclared) and `colloquial` on TERM-027 "place handicapé" (a register label in the jurisdiction column). Owed a decision; reported non-blocking.

### 2026-09-18 — executed is `mined`; a deferral is legitimate if it eventually runs [L3731-L3820]
Owner words: "executed is 'mined'" … "deferred is okay so long as it runs eventually"
In force:
- `evidence_sources.citation_mining_status` is the execution signal: `mined` = the pass ran; `deferred` = it did not. `log_mining` derives it.
- `citation_mining.backward` / `.forward` record that a pass was logged, not that it ran. Do not split them into attempted/executed pairs (refused: second home of one fact, rule 5). Read both.
- A deferral is not a defect (depth-1 constraint, `citation-miner` §6).
- `citation_mining_completeness` counts row presence and must be changed to read `citation_mining_status`; until changed, treat its percentage as an overstatement wherever quoted. [CHECK: whether the check has since been changed is outside this slice.]
- Derivation (derives both the presence figure and the execution figure; never quote the numbers):
```
python3 - <<'PY'
import sqlite3
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
SLUG = 'accessible-circulation-geometry'

# FIGURE 1 -- what citation_mining_completeness reports: T1-2 sources with a mining ROW,
# over T1-2 sources in scope. It counts PRESENCE, which is the defect.
rows = con.execute("""
    select es.ref_id,
           (select count(*) from citation_mining c where c.global_ref_id = es.ref_id) has_row,
           es.citation_mining_status
    from evidence_sources es
    where es.tier in (1, 2)""").fetchall()
present = sum(1 for _, h, _ in rows if h)
print(f"as the check reports it : {present}/{len(rows)} T1-2 'mined' "
      f"= {100.0 * present / len(rows):.1f}%   <- PRESENCE, the overstatement")

# FIGURE 2 -- what actually ran on the slug: status='mined' is the execution signal.
slug_rows = con.execute("""
    select es.citation_mining_status
    from evidence_sources es
    join source_slug_links l on l.ref_id = es.ref_id
    where l.slug = ? and exists
          (select 1 from citation_mining c
            where c.global_ref_id = es.ref_id and c.slug = l.slug)""", (SLUG,)).fetchall()
executed = sum(1 for (st,) in slug_rows if st == 'mined')
print(f"as execution reports it : {executed} of {len(slug_rows)} on {SLUG}")

for st in ('mined', 'deferred', 'pending'):
    n = con.execute("select count(*) from evidence_sources "
                    "where citation_mining_status = ?", (st,)).fetchone()[0]
    print(f"  corpus-wide {st:<9}: {n}")
PY
```
- CONDITION: any session logging a mining pass, reading the mining register, reporting mining coverage, or proposing a schema change to `citation_mining`.
- ACTION: (1) Read `citation_mining_status` as the execution signal; build no second home. (2) Do not split the direction columns. (3) Treat `citation_mining_completeness`'s percentage as an overstatement until it reads status. (4) The "runs eventually" obligation needs a measure (age or backlog count of undischarged deferrals). (5) Do not record a deferral as a defect.
Open:
- [OPEN] No measure of the "runs eventually" obligation exists (no ageing, no backlog count, no failing check).

### 2026-09-18 — RULE: a retraction is a claim [L3824-L3836]
Recorder/delegate entry — not owner words.
In force:
- RULE: a retraction is held to the standard of the claim it retracts.
- CONDITION: a session withdraws a result and offers a replacement (corrected count, re-ranking, different instrument, revised cause).
- ACTION: re-derive the whole comparison, not only the challenged part, and name the instrument. Self-correction is not self-verifying.
Open: none.

### 2026-09-18 — RULE: a yield is derived from a named, versioned screen [L3838-L3850]
Recorder/delegate entry — not owner words.
In force:
- CONDITION: any count of how many references are relevant (mining pass, prediction, gap, cross-batch comparison).
- ACTION: name a screen from `governance/mining-screens.yaml` and derive the figure: `python3 scripts/research/mining_screen.py --ref <REF-NNNNN> --compare`. Record the screen name and version beside any yield kept. Never edit a screen in place (it re-scores every yield recorded under its name); add a new name. Never use an inline regex.
Open: none.

### 2026-09-18 — RULE: when the CLI cannot reach a column, add the verb; never claim the write [L3852-L3862]
Recorder/delegate entry — not owner words.
In force:
- CONDITION: a correction that requires writing a column no `db.py` subcommand exposes.
- ACTION: never record a claim that a write happened when it did not. Add the verb, add the edge the check needs, add the check, then make the claim. Exemplar of the sequence: `reattribute-candidate`, `resolved_ref_id`, integrity check S01. [CHECK: exemplar named as illustration.]
Open: none.

### 2026-09-18 — ERIC is a repository worth remembering [L3864-L3923]
Owner words: "ERIC is a valuable repository to remember"
In force:
- ERIC indexes government and institutional reports with no DOI, PMID or Crossref deposit; many full texts at a predictable URL:
  - `https://api.ies.ed.gov/eric/?search=<query>&format=json&rows=25` (record; gives ED number)
  - `https://files.eric.ed.gov/fulltext/<ED-number>.pdf` (full text, often present)
- Derive what the corpus holds by engine, never quote: `python3 -c "import sqlite3;con=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True);print(list(con.execute(\"select engine,count(*) from search_executions group by 1 order by 2 desc\")))"`
- `books.googleapis.com` returns HTTP 429 (daily quota exceeded) in this environment: a Google Books query here is not asked; treat a 429 as an unfired query, never as a null.
- ERIC's scope is education and rehabilitation-adjacent research; a miss in ERIC is a miss in that index only; an R14 query-shape-versus-wrong-index diagnosis must still be made.
- `catalog.hathitrust.org` returned a 403 carrying a Cloudflare "Just a moment…" interstitial: nothing is established about what HathiTrust holds. Read the body, not the status, in both directions.
- CONDITION: any session searching for a pre-1995 report, an institutional or government research report, or any source with no DOI from Crossref.
- ACTION: (1) Try ERIC before recording a zero-yield as genuine absence (a pre-1995 grey report absent from PubMed and Crossref is an indexing fact until ERIC has been asked). (2) Retrieve through `retrieval_log.fetch`, never `WebFetch` (GAP-034). (3) Read the body before believing a 200.
Open:
- [OPEN] Sibling routes owed and untried: NTIS (federal technical reports) and Jisc Library Hub Discover (UK institutional reports).

### 2026-09-18 — 1979 work is historical grounding, not a current standard [L3925-L3970]
Owner words: "I don't think 1979 work is great for today standards but it's great for historical grounding"
In force:
- Overrides the tier the ladder would produce on study design alone. Steinfeld, Schroeder and Bishop 1979 (HUD-PDR 397) is admitted as `evidence_type='grey'`, `scope='intrinsic'` → T3, marker ○, by ruling; design facts recorded in `verification_note` and the extractions.
- The refusal is about currency, not design quality: the anchoring band (T1 / Co-1 / T2 / Co-2) says "best practice today".
- The source is not retired, its findings are not false, and it may sit in a determination's supporting set; it is barred from being the anchor for a present-day building parameter.
- Not a general rule that old work is weak. For a historical claim (what the evidence said when a code was written) such a source is primary and first-class.
- CONDITION: any session admitting a source published before roughly 1990, or weighing an old but methodologically strong study for an anchoring tier.
- ACTION: (1) Judge age as currency, separately from study design; a strong method does not carry an old source into the anchoring band. (2) Record the design facts anyway, so the T3 reads as a ruling. (3) Historical-provenance claims are a different claim type; old primary work anchors those at full strength.
Open:
- [CHECK] Parameter 3 × MOB undetermined; determination gate 1 open; C10 refuses (GAP-020, GAP-024) — stated as state at the time; re-derive.

### 2026-09-25 — the unreachable is given up for now; four relayed points [L3972-L4030]
Owner words: "if we can't access something from anywhere then we have to give up on it for now"
(Points 2-5 were relayed by a coordinating session and are recorded in that session's words, not as owner quotations.)
In force:
- (1) An item with no route from anywhere this project can reach is not queued for anyone; no interlibrary-loan, document-delivery or author-contact task is drafted for the owner. "For now" is revisable, not a finding about the item. Applied: REF-01002, Walter 1971 (candidate 109), 1957 Illinois dissertation (candidate 110); GAP-016 NOT-ADDRESSABLE; GAP-026 CLOSED-DECIDED.
- (2) [relayed] The disposition is typed: `search_candidates.disposition = 'EXHAUSTED'`. Not for an item behind a possibly transient barrier (bot check, Cloudflare interstitial) an ordinary browser gets past; such an item stays PENDING-VERIFICATION with a note (e.g. candidate 123, Garg 2024).
- (3) [relayed] A facility audit's population grade does not turn on whether its auditors were disabled; that is a Co-1 question. REF-01007 re-graded PROXY → PARTIAL, matching REF-01006. Supersedes, as applied to a facility audit, the research-contract R13 summary line "Children/general-population/no-participants = PROXY".
- (4) [relayed] The vocabulary does not pre-decide an open scope question. TERM-089 (`ramp`) is narrowed to exclude the running slope of paths, walkways and trails (no longer answers GAP-033's ramp-versus-route question). Covers TERM-089 only.
- (5) [relayed] No personal email to third-party APIs (Unpaywall or similar). Where an API tolerates it, omit the contact parameter; where it requires one, stop and ask; never substitute a guess. Committed manifests are not rewritten.
- ACTION: 1. Type an unreachable item EXHAUSTED; do not queue it or draft a request. 2. Keep EXHAUSTED for no-route items only; a transient barrier stays PENDING-VERIFICATION with a note. 3. Grade population directness on who is served and what was measured, never on the auditors' disability. 4. Leave an open scope question open in the vocabulary. 5. Send no personal email to any third-party API.
Open:
- [OPEN] Whether the research contract's R13 wording should change is the owner's call (wording not edited).
- [OPEN] On GAP-033: TERM-094's universalised scope note, TERM-093's foreclosure of a separate criterion term, TERM-092's dangling reference.

### 2026-09-26 — `results_admitted` raise-only after insert; a proxy provenance edge is repaired before merge [L4032-L4076]
Recorder/delegate entry — owner rulings relayed by a coordinating session, not quoted. "The owner confirmed it as the answer, not a stopgap."
In force:
- (1) `search_executions.results_admitted` is raise-only after insert: `log-search` sets it from the search's own edges at insert; `db.py link-admission` raises it to max(count, edges); `db.py unlink-admission` lowers it by one, never below the edges that remain. The count is never lowered to force agreement with the edges. One home: `_results_admitted_after` in `scripts/db.py`. Supersedes, for post-insert writes, DR-2026-08-19 step 7's "the count must agree exactly" and the H05 note's "nothing updates it thereafter". H05 stays deleted; no parity check returns; historical counts restored above their edges stay.
- (2) A proxy provenance edge is repaired, not merged: 1. log each real discovery step as a backfill search (`log-search --backfill 1`, a prior that states its own absence, an honest `query_text`); 2. move candidates with `reattribute-candidate`; 3. move edges with `unlink-admission` and `link-admission`. An ad hoc lookup is logged as what it was.
- ACTION: 1. Never lower `results_admitted` to meet the edges; let the two verbs move it. 2. When a candidate's search is a proxy, backfill the real step and move the candidate and its edge; never leave the proxy or re-describe the proxy search as the source.
Open: none.

### 2026-09-27 — back-pointers for the results_admitted ruling [L4078-L4123]
Recorder/delegate entry — not owner words (built under DR-2026-09-26 §4, owner nod on the DR).
In force:
- Live SUPERSEDES pairs (verified by `supersession_backpointer_audit.py` against live text, never by re-reading this entry):
  - `decisions/DR-2026-08-19-research-restart-operative-instrument.md :: "the junction rows and the count must agree exactly"` BY `references/project-standards.md :: "`search_executions.results_admitted` IS RAISE-ONLY AFTER INSERT."`
  - `scripts/tests/test_db_integrity.py :: "nothing updates it thereafter"` BY the same.
- The DR-2026-08-19 target still describes insert time correctly; "must agree exactly" no longer holds as a standing invariant.
- ACTION: (1) Treat the two target sites as superseded in part, per the callouts at each. (2) Do not edit the 2026-09-25 or 2026-09-26 entries to add these pointers; this entry holds them. (3) Verify a SUPERSEDES/BY pair with the audit, not by reading this entry.
Open: none.

### 2026-09-27 — DR-2026-09-26 ratified [L4125-L4181]
Owner words: "Owner nod." / "Build out all phases in their entirety using agonist-antagonist methodology with antagonist ensuring plan fidelity and adherence to code architecture and layer conformance. As required, use /code-review, /simplify, /layer-conformance and then a comprehensive adversarial critique that sweeps and propagates code implications then audits both top-down holistic and bottom-up granular requiring handshakes to resolve all issues." / "we do not have layer conformance skill; we just need a code architecture compliance"
In force:
- DR-2026-09-26 is RATIFIED. "Layer conformance" is checked against CLAUDE.md's own Layer 0-4 model and seven-stage spine directly, not a separate tool.
- [unratified reading] "build out all phases in their entirety" adopts each OQ's own Recommended answer:
  - OQ-1: require a different model where available; record and report where not (reported only, not a refusal).
  - OQ-3: yes (RC6 latency accepted; §12.2 callout).
  - OQ-4: yes (relayed/backfill SUPERSEDES lines, forward only plus the two seeds).
  - OQ-6: a SUPERSEDED marker in injected text does not count as rewording; seed 3 (R13) not shipped pending the owner's wording call.
  - OQ-7: a non-planned discovery cannot discharge R1, can discharge R2 (design assumption for phase-2 writer refusals).
- Does not retire `data/decisions/decision_register.yaml` or the `decisions` table; does not widen `adversarial_pass_recorded`; does not reword R13. Construction proceeds per DR-2026-09-26 §7 phase order.
- ACTION: (1) Treat the DR as ratified with these dispositions. (2) Do not re-ask OQ-1, OQ-3, OQ-4, OQ-6 (seeds 1-2), OQ-7. (3) Do not build against OQ-5 or OQ-8 without a fresh owner answer or a concrete sweep plan.
Open:
- [OPEN] OQ-5: retire the `decisions` table / YAML register and name the ledger the single home (recommended; not executed; readers `scripts/doctrine_recheck.py`, `scripts/decision_capture.py` unswept).
- [OPEN] OQ-6 wording half: R13 rewording is the owner's.
- [OPEN] OQ-8: widen RC4's scope beyond limb-(a) tables (recommended; no design; `connection_targets` has no session column).

### 2026-09-27 (second) — exec 77 executed per DR-2026-09-26 §5.2(d); pass 1 tooling stood down [L4183-L4237]
Owner words: "Execute as ratified? Proceed all."
In force:
- Further tooling to force `adversarial_passes` pass_id=1 closed is forbidden ("a pass on a pass is forbidden"); pass 1 stays OPEN; no `amend-adversarial-finding` verb is built. The artefact-shape mismatch behind findings 9-12 (`.claude/agents/antagonist.md` prose spec vs `close-adversarial-pass` single-file check) is named for the next tooling PR.
- Exec 77 carries `origin='incidental'`, `target_tier`/`target_evidence_type`/`target_scope` NULL (executed, not proposed). Finding 2 disposed OWNER-RULED.
- `amend-search --clear-target` nulls all three target columns together and is the sanctioned way to null them before an origin change; never hand-edit them.
- Finding 7 disposed REJECTED (the bare `||` is a nested separator inside `|| CORRECTED 2026-09-27:`).
- GAP-053 (audit blind spot: `search_executions`/`search_candidates` lacking `updated_by_session`): see the 2026-09-28 entry below for the resulting state of `search_candidates`. [CHECK: whether `search_executions` also gained the pair is not stated in this slice.]
- ACTION: (1) Treat exec 77 as `origin='incidental'`. (2) Do not chase pass 1 closed as its own effort. (3) GAP-053 is the one record of the blind spot; do not re-file it. (4) Use `amend-search --clear-target`; never hand-edit target columns.
Open: none.

### 2026-09-28 — back-pointer for GAP-053's fix (search_candidates updated_* pair) [L4239-L4282]
Recorder/delegate entry — not owner words.
In force:
- `search_candidates` carries `updated_at`/`updated_by_session`, stamped by the writer from the same `audit(session)` call that writes the narrative note (the two homes are written together, so not the shape rule 5 forbids).
- The objection in `reattribute_candidate`'s original comment is answered for the machine-reader purpose (RC4 scope matching on `_by_session` columns) only; a third home of the same fact for the human-narrative purpose is not licensed.
- Live SUPERSEDES pairs, both BY `references/project-standards.md :: "The fix folds into phase 2b's tooling PR (DR-2026-09-26 §7) when that lands."`:
  - `scripts/db.py :: "the column does not exist, and adding one to record a repair would be a second home for a fact the note already holds."`
  - `scripts/db.py :: "search_candidates has no updated_* pair, so the dated, attributed line IS the audit record of the resolution (the literal RESOLVED is R15's predicate)."`
- ACTION: (1) Treat the objection as answered for GAP-053's purpose, not retracted in general. (2) Do not edit `reattribute_candidate`'s original comment; the marker beside it records this. (3) Verify SUPERSEDES/BY pairs with `supersession_backpointer_audit.py`.
Open: none.

### 2026-09-28 — jurisdiction scope: buckets 1-2 exhausted before reaching further, for any slug [L4284-L4351, including the same-session correction L4339-L4351]
Owner words: "Uganda ... is not a great country to hone in on." / "Please focus on the tiers 1 and 2 countries" / "Uganda is not part of the 24 jurisdiction list" / "Standing order: do not research from countries other than Bucket 1 and Bucket 2 for any slug until those buckets are categorically exhausted."
In force:
- RULE: for every slug, research jurisdiction scope is Bucket 1 and Bucket 2 only, until both are categorically exhausted for that slug.
- "Categorically exhausted" = a search-coverage status exists for every bucket-1 and bucket-2 jurisdiction against the slug's parameters, not merely that some bucket-1/2 evidence was found.
- Bucket membership is derived, never re-typed: `sed -n '420,424p' workplan/2026-08-18-research-frame-proposal.md`. (As read at authoring time: Bucket 1 = UN, ISO, Canada, USA, UK, Germany, Norway, Sweden, Japan, Australia; Bucket 2 = EU, Singapore, New Zealand, Ireland, France, Spain, Portugal, Finland, Netherlands, South Korea. Re-derive.)
- Does not ratify buckets 4/5 or resolve fill order beyond bucket 2.
- Mechanism (as corrected same session): `search_coverage` is frozen (`db.py upsert-coverage` refuses). A jurisdiction's status for a slug is read off `search_executions.jurisdiction` via `v_coverage_jurisdiction` / `v_coverage_language` (deferred searches mark a jurisdiction deliberately not searched).
- CONDITION: any session selecting a jurisdiction to search for any slug, or asking why a non-bucket-1/2 jurisdiction was reached.
- ACTION: (1) Confirm exhaustion by querying `v_coverage_jurisdiction` (or `search_executions` directly) for every bucket-1/2 jurisdiction against the slug; close any gap with `db.py log-search --jurisdiction <code> ... --deferred-reason "..."` for a jurisdiction deliberately not searched, or a real logged search otherwise. Do not infer exhaustion from a partial pass. (2) Do not admit evidence from outside buckets 1-2 for a slug that has not met the bar (not retroactive: PR #165's Uganda rows are not unwound). (3) The Global South / canonical-24 tension is left open. (4) [superseded within slice by 2026-10-01: `UN` is now a `JurisdictionCode` member — see that entry.]
Open:
- [OPEN] Buckets 1-2 omit seven of the eight Global South jurisdictions in the canonical-24 list (Bangladesh, Egypt, Indonesia, India, Kenya, Nigeria, South Africa; `governance/jurisdiction-philosophy.md` §1.1). Not resolved.
- [CHECK] OR-8 (2026-10-29 second, below) judges exhaustion per parameter and per bucket member (a jurisdiction-and-language pair); this entry states the bar per slug against the slug's parameters. The later entry does not state its relation to this one.
- [CHECK] 2026-10-30 (below): "do not include countries outside of the major identified countries for now" / P1+P2+P3 scope for a page; relation to buckets 1-2 not stated.

### 2026-09-28 — correction to the jurisdiction-scope entry [L4339-L4351]: folded into the entry above (mechanism: `search_executions` + `v_coverage_jurisdiction`, not frozen `search_coverage`).

### 2026-10-01 — process-gap remediation plan D1-D4 approved; JurisdictionCode PT, FI, UN, UG [L4353-L4373]
Owner words: "approve all"
In force:
- D2: `JurisdictionCode` (`schemas/enums.py`) admits `PT`, `FI` and `UN` (executing the 2026-09-28 ruling), and `UG` with the comment "declared for PR #165's rows, which are not unwound; outside research scope by the 2026-09-28 ruling".
- ACTION: (1) This entry is the authority for `UG`, `PT`, `FI`, `UN` as members. (2) Declaring `UG` licenses no research; the 2026-09-28 ruling, not the enum, sets research scope.
- [CHECK] D1, D3, D4 concerned PR #166 sequencing behind the tooling PR, go-ahead for the plan's branches, and agent edits to `.claude/settings.json`; content not restated here.
Open: none.

### 2026-10-09 — every source scanned for every parameter; parameter list seeded from terms; catalogue plan, critique, tooling [L4375-L4423]
Owner words:
- "note that while we search by slug, we scan each source for any and all applicable parameters. we may need to just prepopulate a parameters list."
- "Perform Fable 5.1 read-only adversarial critique of the above. Interrogate quality, logic, sequencing and flexibility of pipeline all directions as well as all gates, reads, writes, conditionals. Ensure that all of our terms/parameters in catalogued will be leveraged in such a way where we can scrape information across any parameter if it appears in any source no matter the slug. Slugs guide our searches, but they do not guide what we derive and mine from sources! Our terms/parameter catalogue will, which means I expect harvesting across multiple terms if a source discusses multiple terms. Ensure that we can add and expand parameter catalogue as required based on new information we come across. Pass off to Opus to rewrite plan judiciously and exhaustively."
- On the terms registry as seed: "1 yes"
- On preliminary/skim governing a published cell: "2 ..yes? like, one pulled from another slug? should be yes, but we still tag it for follow up later"
- On WP12 / R7 floor: "3 don't know what is" then "keep wp12 rule"
- "populate a parameters table" / "we need like the 90+ cleaned parameters without values"
- "A" (to option A: the existing terms turned into measurable quantities with proposed names)
- "... why would you develop a parameter database for coverage of all accessible design terms possible by using batch 23 that came from a specific slug"
- "pull from the major codes, literature and advocacy from major countries" / "there should be an exhaustive bibliography that is outdated but correct that has info on each jurisdiction code bodies and major groups"
- "D1: yes figure from source filed by another slug allowed. skimmed values are not publishable"
- "D2 yes, D3 keep the rule, D8 approve tooling"
- "D3 for parameter terms? it can be pulled from previous catalogues of entries for prepopulating"
- Selected options (not typed): catalogues "Code and standards registries" and "Old corpus terms" (old Part 4 item names offered and NOT selected); guard "Screen, then you approve"; "Yes, second branch".
In force:
- WP12: the R7 floor stays removed and R5 stays re-aimed at admitted sources.
- Scan contract: every admitted source is read against the whole parameter list whatever slug it was filed under. Slugs plan and log searches; they do not decide what is taken from a source. One source can yield many parameters. Arguments and qualitative findings are mined as well as figures.
- Seed: the parameter list is seeded from the existing terms registry. Parameters 4 to 12 (corridor width, turning circle, operating force, reverberation time, LRV contrast, door width, colour temperature, headroom clearance, ramp run length) are kept (D2).
- Names (D3): a name from research is minted only from a phrase an admitted source uses, through `db.py add-term --from-observation`, never by hand, never bearing a value. For prepopulation only, names may be pulled from the code and standards registries (`references/standards-registry.md`, `references/tier456-verified-sources.json`, `references/co1-verified-sources.json`, `references/co2-verified-sources.json`) and the pre-reset corpus terms (`_archived/data/corpus-pre-reset-2026-08-06.db`); never the old Part 4 item names. Guard: every candidate is screened (no digit, comparator or min/max word, no old item code) and listed in one table with its catalogue and entry, for owner approval before any is minted. The minting route `insert_term` lacks goes to the owner on the T1 PR.
- D1: a figure from a source filed under another slug may be extracted and may set a published value, tagged for follow-up. Skimmed values are not publishable. ("Skimmed" = `extraction_method = 'skim'`: ruled 2026-10-29 by OR-24, below.)
- D1c (whether a full-read figure still `preliminary` may set a value): resolved later in slice — see 2026-10-14 delegation and OR-11b (2026-10-29 second): it may, flagged.
- Tooling (D8): the first tooling PR is `catalogue-plan-v2.md` §4.2 items 1-5, on its own branch, merged before the research PR (rule 10). What T1 carries beyond those items is for the owner to accept or strike on the T1 PR.
- The owner-commissioned critique of the catalogue plan supersedes, for that plan only, the 2026-08-19 clause that plans, critiques and handoffs are not adversarial-pass subjects (this paragraph is the mark).
- Pilot scope (batch 24 pilot in `process-gap-remediation-plan.md` §7): its scope (judgment-stage re-read of batch 23's sources) is replaced by the scan contract; observation is not limited to phrases carrying a figure; its new-parameter budget is superseded to the extent of the owner's direction. Live SUPERSEDES pairs against `scratchpad/session_2026-10-01-research-batch-23/process-gap-remediation-plan.md`: "The pilot is a judgement-stage re-read of batch 23's 14 admitted sources." / "New parameters ≤ 4." / "Do this for every concept phrase the source states a figure for".
- ACTION: (1) Scan every admitted source for every parameter; never limit a reading to the filing slug. (2) Take names from observed phrases; mint nothing by hand; for prepopulation, names from the registries and pre-reset corpus terms, screened and owner-approved in one table first. (3) A skimmed figure is not publishable; a cross-slug figure is allowed and tagged. (4) First tooling PR on its own branch off `main` before any bulk promotion. (5) The pilot's scope, new-parameter budget and figure-only step do not bind; its extraction cap is NOT lifted. (6) A critique of a plan needs the owner's fresh commission; this one covered the catalogue plan only.
- The batch 23 scan outputs are not data. `catalogue-plan-v2.md` §10 recommendations stand unapproved.
Open:
- [OPEN] Whether the pilot's extraction cap (twice batch 23's) carries over to the scan contract; whether the review unit is one source (recommendation only).
- [OPEN] As listed unanswered in this entry: D4 (exhaustion judged per parameter and jurisdiction), D5 (who reviews vocabulary in bulk), D6 (an item is one parameter), D7 (the category list), D9 (publish Release 0), D10 (read what is held before fetching), D11 (read out-of-bucket sources already held), D12, D13 (two finished batch 23 scans as test material). [CHECK: later entries in this slice may answer some under different labels — OR-8 (exhaustion per parameter and bucket member), OR-17 (bulk vocabulary approval), OR-16 (read held sources, inside and outside buckets 1-2, before fetching), OR-15 (batch 23 material for the inter-rater test), OR-14 (element pages derived, not containers). The source does not map D-labels to OR-labels.]
- [OPEN] "1. slug by slug / 2. you seed it" choice never answered (queued message crossed it).

### 2026-10-14 — owner delegation: simplification plan §4 items resolved by the assistant, including slugless searches [L4425-L4443]
Owner words: "design 15a for me so long as it makes sense with system" / "§4, including the nullable-slug question. / no idea what these are, but resolve them for me in a logical manner"
In force:
- Every item in §4 of `workplan/2026-10-12-simplification-workplan.md` is delegated to the assistant; resolutions with premises are in `workplan/pipeline-state-graph/RULINGS.md` section (G) (pointed to, not copied). In short: R1-R42 adopted as amended by rehearsals; R12's language conjunct survives; the bytes pointer takes the `retrievals` shape (rehearsed before built); `case_studies` and `economics_entries` not folded; a full-read figure marked preliminary may set a value when tagged; a search may be recorded without a slug when it names a parameter or a mined source (R43); `PopulationCode` retired (R44); retired rule identifiers stay readable (R45); frozen coverage verbs and register text deleted (R46, R47); marker readings fixed (R48); R3's five row-bearing drops, R14 (M4) names, R24 root key and R25 columns confirmed (R49).
- R24: `source_value_extractions.root_id` references `external_root_registry` and nothing else; an in-corpus root is named by `root_ref_id`.
- Executes nothing by itself; each step lands in its own PR read by the owner. The owner can overturn any resolution by a later statement.
- ACTION: (1) Treat §4 items as resolved by RULINGS.md (G); do not ask the owner to re-answer them. (2) Execute the plan one step per PR, opened last, with each owner-merge edit in its own step's diff. (3) Drop a row-bearing table only in steps 1.4 and 1.5, after `--rebuild` shows rows reproduced or the record of survival applies. (4) Rehearse R43 before building it. (5) A later owner override wins.
Open: none.

### 2026-10-14 — recording: a `root_id` references the root registry and nothing else [L4445-L4457]
Recorder/delegate entry — not owner words (records RULINGS R24 under the delegation).
In force:
- `source_value_extractions.root_id` carries a foreign key to `external_root_registry`.
- Live SUPERSEDES pair: `governance/evidence-architecture.md :: "a `root_id` must resolve either to a `root_ref_id` in `evidence_sources` or to a registered external-root stub"` BY `references/project-standards.md :: "the rule becomes that `source_value_extractions.root_id` references `external_root_registry` and nothing else"`. Overtaken in its first alternative only.
- CONDITION: any session asking what a `root_id` may name, or reading the "Root registry" discipline in `governance/evidence-architecture.md`.
Open: none.

### 2026-10-20 — recording: identity registry and ICF map take their lens names [L4459-L4466]
Recorder/delegate entry — not owner words (authority: 2026-10-14 delegation; RULINGS R14, R49(c)).
In force:
- `populations` is `base_taxonomy_identity`; `population_icf_links` is `identity_icf_map`; `population_code` is `identity_code` in both. LED-127's "Confirmation pending — the rename is not applied" is no longer true of the database.
- Register step: executed for `population_icf_links` only (`governance/retired-vocabulary.yaml` RV-027); `populations` fails admission test 4; `population_code` held back per that file's deferred entry.
- CONDITION: any session asking whether the identity registry is renamed, its key column name, or whether LED-127's confirmation is pending.
Open:
- [OPEN] `evidence_population_match` and its `target_population` / `study_population` columns keep their names; LED-127 names them `served_group` / `study_group`. Still the owner's.

### 2026-10-21 — which findings count, who may confirm, what a marker needs [L4468-L4489] (resulting state after L4491-L4574)
Owner words:
- (1) skimmed or `absent` findings supply direction for a proxy determination? — "no. skimmed findings cue tools for a dedicated pass."
- (2) can an `absent` finding confirm a code's value? — "no" (read by the owner's clarification of the same day, below, as about a finding that says nothing about any value)
- (3) does an unverified source cap the marker? — "must be verified"
- (4) is one confirmed clause enough to confirm a whole code? — "no"
In force (engine `scripts/assess/assess_cell.py`):
- A finding row counts for direction (`gather_findings`) only if it is not skimmed and not `claim_type='absent'`. A skimmed finding is left out and reported (`skimmed_findings`, naming `db.py record-scan --mode targeted`) as owing a dedicated reading. Narrows (does not overturn) the 2026-09-16 ruling that findings supply direction. [unratified reading: "cue tools" = the report names the tool for the owed pass; no row is written.]
- Confirmation: a skimmed row confirms nothing; an `absent` row may confirm through an explicit `confirms` edge (per the owner clarification and 2026-10-22 correction, below).
- Unverified source (answer 3, reading as replaced 2026-10-21 correction item 2): left out of the marker (earns no band, cannot confirm); a cell with no verified governing source is weak (○, per 2026-10-21 third); `has_unverified_sources` flags it. [unratified reading: "must be verified" means a band needs a verified source; capping the whole cell at weak is not applied.]
- Code weighing (answer 4, reading as replaced 2026-10-21 correction item 3): a code takes the floor of the mean of its rows' bands, an unconfirmed row being weak; the stacked branch's any-clause rule is what "no" excludes. [unratified reading]
- Re-derive the effect, never quote: copy the DB to a scratch path and run `GUIDEBOOK_DB_PATH=<scratch> python3 scripts/assess/assess_cell.py --db <scratch> --emit-sql <out.sql> --parameter-id 3 --slug <slug> --identity MOB --session <session> --stamp <timestamp>`.
- ACTION: (1) Count a finding for direction only if neither skimmed nor `absent`; report a skimmed one as owing a dedicated reading; an `absent` finding may confirm. (2) Give an unverified source no band. (3) Weigh a code by the floor of its rows. (4) Do not treat the [unratified reading] marks as ruled.
Open:
- [OPEN] The function from sources to a cell's marker: floor of the mean is the owner's for a derived figure's inputs (2026-09-13); its use for a determination's governing sources is RULINGS R7 as amended by R49(a), not put to the owner at this level.

### 2026-10-21 — correction to the four-answer entry [L4491-L4502]
Recorder/delegate entry — not owner words.
In force:
- Item 2 reading (unverified source left out of the marker; cell with no verified governing source weak; flagged) — folded into the entry above.
- Item 3 reading (code = floor of mean of its rows' bands; stacked any-clause rule excluded) — folded into the entry above.
- Superseded within slice: item 1 (REF-00980 no longer confirms) by the owner clarification 2026-10-21; item 4 (`RULE_VERSION` stays `pilot-3`; unguarded routes) by 2026-10-21 third and 2026-10-22 item 3. Also: answers 1-2 narrow the 2026-09-13 statement that an `insufficient` finding "anchors direction at its own source's tier" — a skimmed or `absent` one no longer does.
Open: none.

### 2026-10-21 (second correction) — to the correction above [L4504-L4515]: nothing in force (history only: unguarded-route list replaced by 2026-10-22 item 3; ○-over-unverified question ruled by 2026-10-21 third; wording corrections).

### 2026-10-21 — owner clarification: an absence found at the tested value confirms it [L4517-L4534]
Owner words: "Reading A... but the issue is that there ARE values, which are the existing ones that were tested. The "absence" of the findings is actually research support for that tested code value, so it's actually a supplemental document that supports those code values"
In force:
- The 2026-09-13 ruling stands: REF-00980 is a clear case of confirmation. An absence found at a tested value is support for it; the earlier "no" is read as about a finding that says nothing about any value.
- Engine (`_confirmed_bands`): a `confirms` edge from an `absent` finding row confirms the code row it points at (the edge needs a row referent and a quote). A skimmed row confirms nothing. An `absent` row supplies no direction. [unratified reading: the clarification speaks to confirmation only; the direction rule of answer 1 is left as given.]
- Before REF-00980 counts (research data, separate change under rule 10): 1. the dedicated full reading is owed (extraction 48 is `skim`, `preliminary`); 2. its `confirms` edge (`relation_id` 29) points at a label and must be repointed with `db.py repoint-extraction-relation` at the extraction of the tested requirement; 3. only the code rows the study tested are confirmed by it. (Further steps added by OR-22, 2026-10-29 third: backward mining to identify the tested values.)
- ACTION: (1) Let an `absent` finding confirm through an explicit `confirms` edge to a code row, once read in full. (2) Do not let it supply direction. (3) Do the data steps in a research change, not a tooling change.
Open: none beyond the data steps.

### 2026-10-21 (third) — an unretrievable source cannot be top tier; rule edition pilot-4 [L4536-L4550] (as amended 2026-10-22)
Owner words: "if we can't retrieve a study, then we can't verify it as a primary source, which means that we can't claim it as a top tier. add unverified in this context where something can't be retrieved to the empty circle alongside grey or thin" / "pilot 4 I guess"
In force:
- ○ stands for grey, thin, or unverified because the source could not be retrieved. Such a cell reads ○ (not left at its band and flagged). Stated in `governance/tier-system.md` §§5 and 8, `governance/mission-and-epistemics.md` (marker line; atom MIS-03), `CLAUDE.md` §6, and the comment on `EvidenceMarker.WEAK` (not the `band` docstring). The 2026-09-13 reading of ○ as "no research backing" is widened to include "not retrieved": a hedge on the source, not a finding about the evidence.
- Blocking check C10 (`scripts/tests/test_db_integrity.py`) refuses a published (live stated or provisional) cell whose governing sources are not all verified.
- `RULE_VERSION` is `pilot-4` on new determinations. K01 and K02 read every version but the closed legacy set (`pilot-2`) (2026-10-22 item 7). The `derivation_sha` payload is unchanged from pilot-3.
- ACTION: (1) Read ○ as grey, thin or unverified-because-not-retrieved. (2) Never claim a top tier for a source that could not be retrieved. (3) Write `pilot-4` on new determinations.
Open: none.

### 2026-10-22 — correction after two review passes [L4552-L4574]
Recorder/delegate entry — not owner words. Each superseded ACTION line above carries a one-line mark pointing here.
In force:
- (1) Confirming sources are read on their own (`gather_confirmers`), assessed through the same gates; a band is taken only from a verified one (an absent-only study confirms).
- (2) Floor claim confirmed by an all-absent study: answered by OR-22 (2026-10-29 third, below).
- (3) For a live determination `db.py` refuses: an `amend-source` change to any engine-read source column (`dbcore.ENGINE_SOURCE_COLUMNS`) by whichever junction the determination reaches the source (governing links, convergence, extraction links); supersession of such a source; an `amend-extraction` change to an engine-read row column (`dbcore.ENGINE_EXTRACTION_COLUMNS`; of those `figure_role`, `comparator`, `extraction_method` are amendable); a `confirms` edge to a governing row of a live proxy determination. Not refused by design: a finding row added after the answer (K02 reports it), a data migration, the verification cron. These and any unforeseen route are detected by `assess_cell.stale_determinations`, run by `derivation_handshake_integrity` (re-runs the engine on each live determination of the current `RULE_VERSION`). This list replaces the lists in the two 2026-10-21 corrections. Re-derive the columns: `python3 -c "import sys; sys.path.insert(0, 'scripts'); import dbcore; print(dbcore.ENGINE_SOURCE_COLUMNS, dbcore.ENGINE_EXTRACTION_COLUMNS)"`.
- (4) ○ prose swept: `governance/tier-system.md` §8 (an unretrievable source keeps its tier and may still anchor, earns no band above ○, flagged unverified in place of the regulation/practice flag), `skills/evidence-auditor_SKILL.md`, `references/methodology-evidence-hierarchy-mapping.md` §7.1, atoms CLM-038, EVI-047, EVI-055, EVI-056. [unratified reading: that an unretrievable source keeps its tier and may still anchor is engine behaviour since D-0157, not put to the owner] — conditioned by OR-23 (2026-10-29 third): only with a valid academic route. `governance/grounds.md`'s "includes" for ○ is non-exhaustive and unchanged.
- (5) Migration 116's ALTER fails if a live stated or provisional row exists; re-derive: `select count(*) from specifications where retired_at is null and state in ('stated', 'provisional')` (pending and not_applicable rows carry no marker). Readers of the marker column: render step 3.R (not built) beside `has_unverified_sources`; until then the two CHECKs, C10 and `stale_determinations`. [CHECK]
- (6) `has_unverified_sources` covers every live finding and confirming source of an answer resting on the regulatory stratum.
- (7) K01 and K02 name the closed legacy set (`pilot-2`).
- ACTION: (1) Treat item 3's routes as guarded or detected. (2) Let an `absent` finding confirm through its edge on a proxy determination. (3) Read ○ per `tier-system.md` §§5 and 8 as amended; never claim a top band for an unretrieved source. (4) Treat the marks on earlier ACTION lines as binding.
Open: none (item 2 answered by OR-22; OR-22b open there).

### 2026-10-28 — an interface to review and edit the tables; name the code exception [L4576-L4590]
Owner words: "I need there to be some kind of interface where I can manually review and edit the different table values/information and have it propagate accordingly. At the moment, everything in the database is opaque to me." / (to the code-budget question) "Name the exception"
In force:
- Plan: `scratchpad/session_2026-10-28-owner-review-interface-plan/interface-plan.md` (pointed to, not restated).
- A rendered page is generated to `$TMPDIR` and published privately, never committed.
- [unratified reading] "edit" = a proposal reaching the database only through the sanctioned path (scratch copy → `db.py` verb → `emit_batch_sql.py` → `emit_data_migration.py` → `migrate_db.py`); a page edit changes an in-browser copy and a change set, applied by the assistant through the verbs in its own data PR. An immediate-write edit would be a ruling against rule 3 and is the owner's to make.
- [unratified reading] "propagate" = views recompute on read; a determination is recomputed only by an engine re-run.
- ACTION: (1) Build the interface per the plan: read-only browser and owner queue first, then edits as proposals. (2) No page writes the database; ship every change through the verbs in a data PR apart from tooling. (3) State in each tooling PR "no offset, N lines added" and cite this entry. (4) "Name the exception" is not a ruling on any other PR's line count.
Open:
- [CHECK] ACTION (3) answers the net-negative requirement, which the 2026-11-06 ruling (below) removes; the later entry does not mention this one.

### 2026-10-28 (second) — owner decisions are prompts with full context, on a phone [L4592-L4606]
Owner words: "I'm on mobile tho" / "waiting on me decisions need to be prompts with full context"
In force:
- Owner-facing pages are designed for a phone screen first.
- Each item waiting on the owner is a prompt: the question, why it is the owner's, full context in plain words, the options with what each does, and a recommendation only where a source states one. The decisions of the resolution report's decision sheet and workplan §4 (OR-1 to OR-25 with sub-parts, OW-1, OW-2) are written so in `governance/owner-browser.yaml`, each naming its source; the database-row lists are shown as prompts with the whole row.
- An answer saved on the page is a choice, not a ruling, until a ledger entry quotes it in the owner's words.
- [unratified reading] "decisions waiting on me" = those decisions and the rows the lists name; list membership is the assistant's judgment, for owner confirmation.
- [unratified reading] each prompt's plain-language context is the assistant's rewriting and may misstate a source; the sources, not the prompts, are the record.
- ACTION: (1) Put every decision to the owner as a prompt with full context and options, never as a bare row or a code such as OR-n. (2) Design owner-facing surfaces for a phone first. (3) Write the ledger entry quoting the owner before work depending on a saved answer. (4) Correct a prompt that misstates its source, and say so in the commit.
Open: none.

### 2026-10-29 — OR-1, OR-2, OR-3, OR-5, OR-6 answered [L4608-L4649]
Owner words:
- OR-1: "A parameter does not require a lens for each and every disability population or access need. Do not store table rows for parameters when there is a missing lens for a disability population or access need, i.e. for when the parameter is not relevant. In other words, I expect each and every determination to only have rows for the actual relevant lens. Ensure that all relevant codes/identification/lenses are filled out as required, i.e. a determination should never be limited to only one lens because we have different models for discussing disability (ICF, population identity, access needs)--we need to have each model filled out accordingly."
- OR-2: "Branches, and an empty headline when all are conditioned"
- OR-3: "Yes, reformat in place"
- OR-5: "Co-1 figures may set a value insofar as the source is academically sound. Otherwise, they set the direction, not the number."
- OR-6: "Stated and divergent, with a synthesis approach — We make the dispute transparent. We will provide the T1 source as the stated value, but we will note in discussion of the item that it has been disputed by the T2 source."
In force:
- OR-1: a figure reaches a determination only through the lens tags written on that figure (D-0184 stands). No row is stored for a parameter and lens the parameter is not relevant to, and none for a lens no figure carries; the `not_applicable` state as a stored assertion is overtaken. Every determination, and every figure under it, names each relevant model (identity, ICF code, access need [CHECK: the entry also says "and medical when its registry is filled"; CLAUDE.md §6 records the medical lens deleted 2026-11-16, outside this slice]); D-0182's "ideally many" becomes a requirement for determinations. The CHECK stays at "at least one". Crossing maps suggest codes; judgment confirms them; lens tagging (D-2) fills every relevant model. [unratified reading: relevance is shown by the figures that carry a lens; the gaps table still records a missing figure for a relevant lens.] [unratified reading: "never limited to only one lens" = one determination carries the codes of every relevant model, as `assess_cell.lens_key` allows.]
- OR-2: T-2 built as written; narrows the 2026-07-21 most-accommodating selection to unconditioned claims only.
- OR-3: reformatting a figure's value, unit or empty setting in place (same digits and quote, old text kept in notes) is allowed; narrows D-0168's "a wrong claimed_value ... is a SECOND ROW" for reformatting only. T-1 step 8 widens the amend verb; D-1 repairs rows.
- OR-5: a Co-1 figure sets a value when its source is academically sound, only the direction otherwise. Amends `references/methodology-evidence-hierarchy-mapping.md` §6.4 ("not co-primary for dimensional values" now holds only for a Co-1 source not academically sound); T-4 step 3 leaves out only Co-1 rows whose source is not academically sound. [unratified reading: "academically sound" is not a database field; re-derive held Co-1 sources: `select ref_id, co1_source_type, source_type, grey_flag from evidence_sources where evidence_type = 'co1'`.]
- OR-6: `governance/evidence-methodology.md` §3.3 stands: determination `stated`, convergence `divergent`, synthesis approach supplied. For T1 against T2: the T1 figure is the stated value and the item's discussion says the T2 source disputes it. [unratified reading: the approach is cited by pointer to this entry, not written by the engine; applies to claims that cannot all hold.]
- Live SUPERSEDES pairs:
  - `governance/evidence-methodology.md :: "A cell is `not_applicable` when the parameter genuinely has no design implication for the population."` BY `"Do not store table rows for parameters when there is a missing lens for a disability population or access need"`
  - `references/methodology-evidence-hierarchy-mapping.md :: "which require T1/T2/T3 evidence (or regulatory citation for the code minimum)"` BY `"Co-1 figures may set a value insofar as the source is academically sound."`
- ACTION: (1) Store no row for a parameter and lens it is not relevant to, and none for a lens no figure carries. (2) Fill every relevant model on a determination and its figures; the CHECK's "at least one" is not the aim. (3) Build T-2 as written, and T-1 step 8 and D-1 with in-place reformatting. (4) Let a Co-1 figure set a value only when its source is academically sound; settle OR-5b before T-4 step 3. (5) For T1 vs T2 divergence, state the T1 figure and note the dispute in the item's discussion, citing this entry. (6) Treat every [unratified reading] as unratified.
Open:
- [OPEN] OR-1c: one figure holds one code per model, while a fact can concern several (e.g. d450 and d465). [CHECK: the heading of the next ledger entry at L4922 (outside this slice) says OR-1c answered 2026-11-06.]
- [OPEN] OR-5b: how academic soundness is established.
- [OPEN] OR-6c: whether the approach covers every divergence or only T1 vs T2; whether §3.3's design range still takes in the disputing figure.
- [OPEN] Marks owed (need attestation, left to workplan H-0): DR-2026-09-01-a-link-states-at-least-one-lens-ideally-many.md, DR-2026-07-21 §5.2, DR-2026-08-27, architecture document lines 41 and 122. Prose still listing `not_applicable` (`governance/evidence-architecture.md` lines 26, 116; `governance/mission-and-epistemics.md` line 118; `CLAUDE.md` §6) is swept in the T-3 tooling change. [CHECK: line numbers as cited at the time.]

### 2026-10-29 (second) — OR-8, OR-1b, OR-4, OR-6b, OR-7, OR-9, OR-10, OR-11a, OR-11b, OR-12a, OR-12b, OR-13, OR-14, OR-15, OR-16 answered [L4651-L4707]
Owner words:
- OR-8: "Yes, per parameter and bucket so long as the bucket is not just jurisdiction but associated language."
- OR-1b: "No, ALL reaches only an ALL determination"
- OR-4: "Yes, the most accommodating value wins"
- OR-6b: "No, the spread is printed in the note"
- OR-7: "Yes, show it flagged — Empty circle."
- OR-9: "None yet"
- OR-10: "Yes, convert and show both — Round to nearest 1/4" or 5mm."
- OR-11a: "Yes, require a full-scope scan"
- OR-11b: "Yes, flagged for follow up."
- OR-12a: "Yes, scope them out for now"
- OR-12b: "Yes, flagged — With that said, I expect that the model will be using real terms that are actually in use within a jurisdiction."
- OR-13: "From the codes held"
- OR-14: "Yes, derive it — This derivation is what I expect the specifications pass to be doing--adjudicating, deriving and synthesizing across rows of related evidence."
- OR-15: "Yes, use batch 23's material"
- OR-16: "Yes, read what we hold first"
In force:
- OR-8: exhaustion is judged per parameter, per bucket member; the bucket list is entered once as a table (T-6b steps 4-5). A bucket member is a jurisdiction together with its associated language, never the jurisdiction alone. [unratified reading: pairs as `lang_jur_map` records them; a jurisdiction with several languages is several members; the bucket table points at those pairs with an approval reference per row, not restating languages.] Which pairs belong to buckets 1-2 is proposed by T-6b for owner approval.
- OR-1b: a figure tagged identity ALL reaches only a determination whose identity is ALL.
- OR-4: within T1, Co-1, T2, Co-2 the most accommodating value wins, whichever stated it; governs differing figures that can all be met. [unratified reading: OR-5 applies first.]
- OR-6b: anchoring floors that differ but can all be met are not divergent; the spread is printed in the value note; no synthesis approach needed.
- OR-7: a regulation-only determination (T6, `code_floor_only = 1`) appears in the best-practice view flagged ○; T-5 step 2 drops the `code_floor_only = 0` filter. Option A (tier-system §8; architecture document line 121) confirmed.
- OR-9: no search indices named; T-6 step 6 (search-indices table) not built; coverage not measured by index.
- OR-10: compose across exact linear units (in/ft with mm/m), convert and show both, converted figure rounded to the nearest quarter inch or 5 mm. Amends ACTION (4) of the 2026-09-17 "PRESENT BOTH notations" ruling for exact linear units; its ACTION (3) (never round a derived figure into the position of a stated figure) still holds. [unratified reading: rounding applies to what is shown; the stored bound stays exact.]
- OR-11a: an extraction marked `verified` requires a recorded full-scope `source_scans` reading covering the row's parameter (T-1 step 10); the renderer prints each row's status.
- OR-11b: a figure read in full but still `preliminary` may set a published value, flagged. [unratified reading: the flag says the figure awaits review; no per-figure follow-up record.]
- OR-12a: Arabic, Bengali, Hindi and Swahili are scoped out by the bucket table until buckets 1 and 2 are exhausted; their aliases are not research debt now.
- OR-12b: a model-generated alias may be used for a search if the search is flagged; generate only terms actually in use in the jurisdiction (R11 applied). [unratified reading: no stricter gate; `python3 scripts/audit/alias_provenance_audit.py` lists them.] (Vocabulary governed by the stricter OR-17, 2026-10-29 third.)
- OR-13: the list of quantities is seeded by an open-pass scan of the bucket 1-2 codes already held, not slug by slug (D-8; needs D-3, T-6b, OR-17).
- OR-14: a book page for an element is derived from a typed term pointer to the live determinations of its parameters (one parameter the degenerate case), never a container rows are filed into (T-7, D-6). The specifications pass is "adjudicating, deriving and synthesizing across rows of related evidence".
- OR-15: the inter-rater test uses held batch-23 material (one code with a step table, one T1 paper with findings; D-5).
- OR-16: sources already held, inside and outside buckets 1-2, are read before more are fetched; D-3 covers every source not superseded.
- ACTION: (1)-(15) as above. (16) Treat the [unratified reading] marks as unratified.
Open:
- [OPEN] OR-10b: which way a rounded minimum or maximum moves.
- [OPEN] OR-14b: whether the specifications pass itself writes an element-level determination.

### 2026-10-29 (third) — OR-17 to OR-24, OW-1, OW-2, D-0139, D-0140, D-0165, observed_terms 65, 68, 70, 71, 73 [L4709-L4780]
Owner words:
- OR-17: "Yes, bulk, with me reading the PR — Ensure that these phrases/names/aliases are all present in their prescribed jurisdiction/language. It is not acceptable for the model to generate its own phrases/names/aliases."
- OR-18: "Transcripts suffice"
- OR-19: "Yes, presume an echo"
- OR-20: "No — We don't need to mine backwards for T4 to T6--whatever is given to us by them is what we accept as a matter of fiat. We are not interested in their history itself."
- OR-21: "Yes, when it first arises"
- OR-22: "Something else — This is why we use backwards citation mining and contextual clues. If we are unable to find the actual parameters/values under discussion, then the source itself has no value. If we are able to find the actual parameters/values under discussion, then the absence of findings--i.e. the lack of prescribed change to that parameter/value--is simply a confirmation of the validity of those parameters/values."
- OR-23: "Confirm -- This applies only when the source is properly cited in an academic context, i.e. there is a valid academic route to the source."
- OR-24: "Confirm"
- OW-1: "Yes, map views to a stage — I expect the rendering to occur on the basis of whatever specification has been synthesized accordingly, and I expect the render table to be one where the specification table rows have been converted into complete prose, bibliographic information etc accordingly from the preceding tables such that it can be displayed properly on the website repository."
- OW-2: "Yes, register it"
- D-0139: "Ratify it (active)"
- D-0140: "Ratify it (active)"
- D-0165: "Ratify it (active) — ...room acoustics is PIVOTAL for deaf and hard-of-hearing people. Room acoustics were literally developed with these persons in mind."
- observed_terms 65: "It names a term we have — All it does is tell where the ramp slope is to be calculated from, i.e. the middle of the ramp. The gradient is another for the slope."
- observed_terms 68: "It names something new — Barrier-free path of travel is not limited to ramps, but the entire procession throughout a building."
- observed_terms 70: "It names a term we have — ramped access route = ramp. access route is about procession throughout a building"
- observed_terms 71: "It names a term we have — refers to barrier-free path of travel" — superseded as to what observation 71 names by 2026-10-29 (fifth), below.
- observed_terms 73: "It names a term we have — it is a ramp, and the access route refers to the barrier-free path of travel insofar as it concerns navigating a building"
In force:
- OR-17: the assistant approves vocabulary in bulk (D-4, D-8); the owner reads the PR. Every phrase, name and alias must be present in its prescribed jurisdiction and language; the model may not generate its own. The later, stricter statement governs vocabulary over OR-12b. [unratified reading: "present in" = attested by a retrieved source of that jurisdiction and language (an observed phrase with its source), carried in each approving PR.]
- OR-18: preserved transcripts (model and effort per message) are the telemetry; D-5 derives model and effort from them; session records need no `Model:` / `Effort:` lines.
- OR-19: a grey (T3) source repeating a code's value is presumed, rebuttably, to echo the code, without re-tiering (T-8 step 3).
- OR-20: T4-T6 anchors are not mined backward for root tracing; what a regulation, standard or national framework states as its own requirement is accepted as given. R2 unchanged; D-7 gets no mining pass. [unratified reading: "fiat" covers the figure stated as the source's own rule; it does not lift the T4-T6 walling-off from full-strength anchoring, nor retrieval/verification (or reading as ○).]
- OR-21: when a direction is contested, a direction is recorded per lens when the case first arises; nothing built now.
- OR-22: a study whose rows are all absence findings confirms the value it tested, provided the actual parameters and values can be found by backward citation mining and contextual clues; if they cannot, the source has no value (given no role, flagged). Answers 2026-10-22 item 2: such a cell is a confirmed claim, not a regulation-only floor. Not in conflict with OR-20 (that concerns a regulation's history; this mines a study's citations). [unratified reading: the confirmed floor claim takes its confirming study's band (`_confirmed_bands`), so migration 116's CHECK holding a regulation-only cell at ○ must not apply to it.]
- OR-23: an unretrievable source keeps its tier and may still anchor a determination, earning no band above ○, only when properly cited in an academic context (a valid academic route). Live SUPERSEDES pair: `governance/tier-system.md :: "An unretrievable source keeps its tier and may still anchor a determination (D-0157: a return pass is owed)"` BY `"This applies only when the source is properly cited in an academic context, i.e. there is a valid academic route to the source."` [unratified reading: a valid route = a resolving DOI or index record, or a citing bibliography (the `verification_method` values); a source with no route keeps no tier claim and does not anchor. Re-derive held unverified sources: `select ref_id, tier, verification_method, doi from evidence_sources where verification_status = 'UNVERIFIED'`.]
- OR-24: "skimmed" means `extraction_method = 'skim'` (ruled).
- OW-1: a view mapped to a stage counts as a member of that stage in the walkability check; `governance/stage-map.yaml` gains a `views:` key. Rendering is done from whatever specification has been synthesized; the render table holds specification rows converted into complete prose with bibliographic information from the preceding tables, displayable by the website repository as it stands. Re-opens T-5. [unratified reading: the render table lives in the database and the site reads it (2026-08-27 "no committed file is a render" holds); each render row points at its specification and records a hash of its inputs so staleness is detectable.]
- OW-2: `workplan/pipeline-state-graph/walkability.py` is registered as the stage-pair gate by one registry entry that fails when a stage pair has no path. [unratified reading: added once OW-1's views key has landed.]
- D-0139 ratified (active): `architecture/schema-spec.md` as the SQL specification for the SQLite storage form. Its hold reason stays on the record: the document describes tables not in the database. [unratified reading: ratified as the B1 session's specification of record, without asking the document to be brought into line.] The `decisions` row stays PROPOSED until the table has a `db.py` verb; the ledger is the record meanwhile; the missing verb is a coverage gap to file in a tooling PR, never closed by hand edit.
- D-0140 ratified (active): the repository stays one repository with the SQLite database inside it (`governance/repo-strategy-revision-co.md`). [unratified reading: the follow-on edit to `governance/repo-strategy.md` waits for the owner's word; applying the Change Order must correct its stale paths `data/db/guidebook.db` (retired, RV-008) and `scripts/migrate/` to `data/guidebook.db` and `scripts/migrations/`.] `decisions` row stays PROPOSED until a verb exists.
- D-0165 ratified (active): deaf and hard-of-hearing people belong on room-acoustic-performance; supersedes the deferral's "No population is added to or removed from room-acoustic-performance" for them; the slug's first determination is not held by D-0165 for them. [unratified reading: lens = identity DEAF, ICF hearing codes b230, d115, d310, access need A-NOSOUND, tagged where relevant under OR-1; the A-18 item-layer block lapses for this question; other groups not ruled.] `decisions` row stays DEFERRED until a verb exists.
- observed_terms 65: NAMES-EXISTING → TERM-001 (ramp gradient); rationale: the phrase only locates where the slope is taken (middle of the ramp); gradient is another word for slope. [unratified reading: TERM-001 is the term meant — basis: its definition "Slope of an accessible ramp expressed as ratio or percentage".]
- observed_terms 68: NAMES-NEW ("barrier-free path of travel"), after the new term's definition is owner-approved (OT-1/OT-2).
- observed_terms 70: NAMES-EXISTING → TERM-089 (ramp); an access route is the route through a building, no part of the term. [unratified reading: the "=" makes the phrase's head ramp.]
- observed_terms 73: NAMES-EXISTING → TERM-089 like 70, with the access-route reading in its rationale. Any other held observation of "ramped access route" takes the same judgment unless the owner says otherwise.
- All adjudications go through `db.py adjudicate-term` in a data PR.
- Tagging held room-acoustic figures with DEAF, the ICF hearing codes and A-NOSOUND is research data work for its own PR (D-2), after the lens change (T-3).
- ACTION: (1)-(15) as above; (16) treat every [unratified reading] as unratified.
Open:
- [OPEN] OR-17b: whether a flagged search may still use a recalled term; what becomes of model-generated aliases already stored (`python3 scripts/audit/alias_provenance_audit.py`).
- [OPEN] OR-22b: which marker a floor claim confirmed by an all-absent study reads.
- [OPEN] OR-23b: whether a code or standard (not cited in academic literature) has a valid route through a registry citation. The engine change for the empty-circle rule waits on it.
- [OPEN] OW-1b: how the render prose is produced (also: whether and by whom a source's sentence may be translated or rewritten — per 2026-10-30 radical-transparency entry).
- [OPEN] OW-1c: whether the render table is stored or rebuilt.
- [OPEN] The ruling on OR-23 does not say what becomes of held sources without a valid academic route.
- [OPEN] OT-1 (answered in the fourth entry); observation 71 (see fifth entry).

### 2026-10-29 (fourth) — OT-1 answered: "barrier-free path of travel" [L4782-L4796] (as amended by the fifth entry)
Owner words: OT-1: "Barrier-free path of travel. It is a circulation route that is specific to people in wheelchairs/mobility devices."
In force:
- The new term for the whole route through a building (observation 68) is named "barrier-free path of travel": a circulation route (in the sense of TERM-048) specific to people who use wheelchairs or other mobility devices, narrower than TERM-048. The `terms` table has no parent column, so the relation is stated in the new term's definition and scope note, which the owner approves first (OT-2).
- ACTION: (1) Add the term (canonical name "barrier-free path of travel") only after its definition and scope note are owner-approved (OT-2); then adjudicate observation 68 NAMES-NEW. Its aliases are the phrases sources use (e.g. "access route"), each with its in-language source; none the model writes (R11, OR-17). Not observation 71 and not "accessible route" (fifth entry). (2) Treat every [unratified reading] as unratified.
Open:
- [OPEN] OT-2: owner approval of the definition and scope note wording.

### 2026-10-29 (fifth) — observed_terms 71 (revised): accessible route is not barrier-free path of travel [L4798-L4812]
Owner words: observed_terms 71 (revised): "good point. accessible route is not the exact same as barrier-free path of travel, ie accessible route must be able to be navigated by someone who is blind"
In force:
- "Accessible route" is not the same as barrier-free path of travel: an accessible route must be navigable by someone who is blind.
- Observation 71 is not adjudicated NAMES-EXISTING pointing at barrier-free path of travel, and "accessible route" is not an alias of it. The draft OT-2 definition drops "accessible route" from its source phrases. Observation 71 is adjudicated only on the owner's answer to its prompt.
- [unratified reading: the statement settles that it is not the same term, not what it is — it may name a held term, a new one, or neither.]
- ACTION: (1) as above. (2) Treat every [unratified reading] as unratified.
Open:
- [OPEN] What "accessible route" (observation 71) names; returns to the owner's waiting list.
- [OPEN] Whether the existing alias "accessible route" on TERM-048 (circulation route), written by an earlier synonym-grouping build, stays.

### 2026-10-30 — best practice, the specification page and rendering (ramp-slope session) [L4814-L4867] (with 2026-10-30 second)
Owner words (statements of 2026-10-29 and 2026-10-30, recorded on the owner's instruction of 2026-10-30):
- "best practice = the best way to do something according to how it benefits the intended group"
- "best practice =/= most common or agreed upon. we have been through this a million times"
- "remember that our guidebook doesn't take positions. it just presents what appears to be the most accommodating/gentle best practice for anything... so unless an academic article or some professional body improves upon germany's standard, that's identified as the best practice"
- "the gentlest value is the gentlest value. the evidence is that it exists in practice. there does not need to be academic studies or anything because they are not always going to be available"
- "i don't want us to highlight the steepest slope allowed in codes read"
- "You do not need to find evidence for why 1:12 was the code floor--just accept the 1:12 as a baseline to work from. Lots of the code stuff we are dealing with is like this--there is not open available research behind it"
- "We are interested in what are best practices NOW, and that means we do not need to interrogate the history of anything but rather the current state of everything"
- "specification in book and item pages now are the same idea in that it tells you the correct way to design something"
- "the critical methodology comes from synthesis/adjudication/specifications, not from evidence collection"
- "...covered means that the source that has been listed in the database has been read and had information extracted from it then verified"
- "provisional means that we have to go back and review the source again to confirm information accuracy" (answer 10 reads "stage. provisional means that we have to go back and review the source again to confirm information accuracy")
- "how on earth do we have evidence outside the library? we either have evidence or we do not have evidence. our library is just what we have recorded"
- "Yes it is P1+P2+P3" / "do not include countries outside of the major identified countries for now"
- "I think the issue is not the slope of the ramp, but the lack of a rest landing." / (to making rest-landing spacing a second headline parameter) "Yes, next session"
- "i want it to be coming from database directly in ideal world"
- "There is an audience lens (the four audiences) and a disability lens (population, ICF, access needs)"
- "Filter the page by one of three lenses: population vs ICF code vs access need, and then when you select which lens do you see the pills pop up wit the more specific case for further filtering"
- "the filters have to precede the information"
- "for ramp gradient, i want there to also be an easy comparison master table where you just see what each jurisdiction has for the value"
- "we do not need to have rows for people where the value is just "Not set." that just means that it shouldn't be showing on the page"
- "the question beneath the title is irrelevant"
- "note: all work must comply with website accessibility standards and best practices"
- "ensure that minimalism does not come at the expense of readability/legibility especially as it pertains to accessibility practices for website navigation"
- "refer to swiss graphic design"
- (Q1-Q7 of the design-requirements file) "Use my defaults"
In force:
- (1) Best practice is the most accommodating value found in practice, in the parameter's recorded direction (`base_parameters.accessibility_direction`; ramp gradient: lower is better), unless a study or professional body improves on it. Not the modal or agreed value; the steepest code value is not highlighted. No study is needed for a value to be named; a T4-T6 value is accepted as a baseline without tracing its history. A determination resting on T4-T6 alone keeps the ○ band and the weak, code-derived flag with the convergence-not-evidence caveat (`governance/tier-system.md` §8, `governance/evidence-architecture.md` I3); such a value is not marked ●. (Ratified by the owner 2026-10-30 second, below.) No SUPERSEDES line.
- (2) A reading is provisional until its source has been read again and the information confirmed; a source is covered only when read, extracted and verified. A page says "read, none yet verified" while no reading is verified, and lists jurisdictions whose sources are not yet read as not yet read. [unratified reading: matches `specifications.state` (`pending`, `provisional`, `stated`) and `has_unverified_sources`; no new field.]
- (3) An item page is the specification; rendered from the database. [unratified reading: read with OW-1 and the 2026-08-27 ruling; a static generator emitting committed HTML is not restored.]
- (4) Two lenses: an audience lens (designer, disabled person, occupational therapist, policy maker; `governance/audience-priority.md`) and a disability lens (population, ICF code, access need). More specific options appear only after a lens is chosen; controls come before the information.
- (5) A master comparison table: one row per in-scope jurisdiction, alphabetical, standard and edition under the row, detail one click from the value. Rows with no value are not shown. Evidence listed alphabetically by first author's last name and regrouped by the chosen lens. One sans typeface, few sizes, no decoration. Working requirements with acceptance tests: `workplan/2026-10-30-ramp-spec-pages/reports/spec-page-design-requirements-2026-10-29.md`; owner took the defaults for Q1-Q7. [unratified reading: that file is a working baseline, not a ratified specification.]
- (6) Accessibility is a precondition: WCAG 2.2 level AA wins over aesthetics; navigation legibility is not traded for minimalism. Compliance is never self-certified: a page is described as having passed the tests run, on the date and build recorded.
- (7) Jurisdictions shown are the major identified countries, P1+P2+P3 of the jurisdiction ranking, current editions only. [unratified reading: the ranking in `workplan/2026-10-30-ramp-spec-pages/HANDOFF.md` §3.]
- (8) Rest-landing spacing is the second headline parameter for ramp gradient; its best practice follows item 1 (shortest run between rests found). The ramp session's figure (Germany, 6 m, from a secondary source) is unverified.
- ACTION: (1) Name as best practice the most accommodating value found in the recorded direction, never the commonest, never highlighting the steepest code value; keep the ○ band and flag for T4-T6-only determinations; do not mark ●. (2) Provisional until a second reading confirms; covered only when read, extracted and verified. (3) Render a specification page from the database, not a committed file; take the element-to-table mapping from the render contract (`workplan/2026-10-30-ramp-spec-pages/RENDER-DECISIONS-AND-PIPELINE.md` §3); do not restore a static generator. (4) Offer the audience and disability lenses; write nothing as accessible that has not passed a recorded test. (5) Show only in-scope jurisdictions and no row without a value, stating the gap under Gaps. (6) Mint rest-landing spacing as a parameter through the sanctioned CLI in its own data PR, direction recorded from an admitted source, not hand-set. (7) Treat every [unratified reading] as unratified.
Open:
- [OPEN] 9(a): a row with no value is not shown vs `governance/mission-and-epistemics.md`'s requirement that a pending cell display `[BEST-PRACTICE-PENDING]` with a gap link. [unratified reading: met by showing no row and stating the gap with its link in the page's Gaps section.]
- [OPEN] 9(b): "the question beneath the title is irrelevant" vs the mission document's questions as first-class data. [unratified reading: refers to the single question line the ramp page carried; how questions appear on a specification page is left to the owner.]
- [OPEN] OW-1b, OW-1c (render table storage and prose production).
- [CHECK] (7) "P1+P2+P3" page scope vs the 2026-09-28 bucket 1-2 research floor: relation not stated.

### 2026-10-30 (second) — keep the ○ band and flag for a gentlest code value [L4869-L4882]
Owner words: "Yes, keep the ○ band and flag"
In force:
- A determination resting on T4-T6 alone keeps the weak band (○) and the weak, code-derived flag with the convergence-not-evidence caveat, whichever value is named; not marked ●. The best-practice statements decide which value is named, not the band or flag. Nothing superseded.
- The [ASSUMPTION] on item 1 of the previous entry is ratified by this entry (the "keep" confirms item 1 in full, including no ●); the others in that entry stay unratified.
- ACTION: (1) Keep the ○ band and flag on a T4-T6-only determination; do not mark it ●.
Open: OW-1b, OW-1c and item 9(b) of the previous entry still wait on the owner.
(Entry has no DATE line; date from heading.)

### 2026-10-30 — radical transparency; present, do not claim correctness [L4884-L4900]
Owner words: "i don't know how to resolve the questions for me at this point, but please know that i want to be as radically transparent for my audience as possible while simply PRESENTING information without claiming correctness myself" / the questions "may mean that you need an opus antagonist adjudication round to resolve these things"
In force:
- Restates the ratified posture of `decisions/DR-2026-07-21-product-posture-thinking-tool-not-authority.md`: every determination is rendered as a figure for thought, "radically transparent about its evidence, its derivation, its disagreements, and its strength flag"; "we never adjudicate a correct path or conclusion". `governance/held-tensions.md` T5 binding: no session may resolve a held tension.
- No supersession claimed. [unratified reading: reaffirms the posture; does not retire ratified texts that use "best practice" with a marker (`governance/evidence-architecture.md` §6, the Core Doctrine marker rule in this file, `governance/mission-and-epistemics.md`). Reaching those would need a decision record.]
- The statement is a deferral, not a delegation: the assistant's positions in `workplan/2026-10-30-ramp-spec-pages/RENDER-CONTRACT-parameters-3-and-12.md` §8 are unratified proposals bound to nothing. The audience lens is answered by the 2026-10-30 entry (item 4).
- CONDITION: any session writing or reviewing the wording of a rendered page, render record, or template turning a specification or extraction into prose; any session asking whether a page may recommend, endorse or call a value correct.
- ACTION: (1) Describe and attribute; show the derivation, the strength flag and the disagreements; never adjudicate a correct path. (2) Treat the contract's §8 positions as proposals and every [unratified reading] as unratified.
Open:
- [OPEN] OW-1b: whether and by whom a source's sentence may be translated or rewritten.
- [OPEN] OW-1c.
- [OPEN] The remaining render-contract questions (deferred, not delegated).

### 2026-11-06 — minimise code; no net-negative requirement [L4902-L4920]
Owner words: (question) "net negative rule? that is supposed to be reserved for minimizing code infrastructure?" / "we want to MINIMIZE code wherever possible. we don't require a net negative because the extreme of that means we end up with no code" / "we want the bare essentials in the most code efficient manner possible so that we are agile and lean"
In force:
- The standing constraint is minimal code (bare essentials, written as efficiently as possible), not a shrinking total. The net-negative requirement (a PR touching `scripts/`, `schemas/`, `.github/` or `skills/` may not raise their line total without naming the exception) is not required. [unratified reading: the net-negative bullet was about code infrastructure only, never research rows, owner decisions, doctrine or prose.]
- What stays (CLAUDE.md §8 tests needing no count): before adding a check, script or table, state what wrong thing reaches the guidebook without it; nothing is added without naming what reads it. [unratified reading: "wherever possible" is a standing preference weighed case by case, not a gate; a defect reaching the guidebook is still fixed with the smallest code that closes it.]
- CLAUDE.md §8's net-negative bullet is rewritten in place; no SUPERSEDES pair. Where `workplan/2026-10-12-simplification-workplan.md` W3 and the "net-negative" item of `workplan/2026-10-23-pipeline-resolution-workplan.md` differ, this ruling governs.
- CONDITION: any PR touching `scripts/`, `schemas/`, `.github/` or `skills/`, or a question whether a change must reduce the line total.
- ACTION: (1) Do not require or claim a net-negative total; name what the added code reads, what wrong thing reaches the guidebook without it, and any code it replaces or makes deletable. (2) Try, in order: do nothing and say why; change a rule or convention; reuse what exists; delete the cause; only then add the smallest code that closes the defect. (3) Treat every [unratified reading] as unratified.
Open: none.

---

Slice stats: entries read 37; entries reduced to nothing in force 2 (L4339-L4351 correction, folded into its parent; L4504-L4515 second correction); entries tagged [STATUS UNCERTAIN] 0 (cross-slice and unstated interactions are tagged [CHECK] instead: OR-1c vs L4922 heading, medical lens, OR-8 vs per-slug floor, P1+P2+P3 vs buckets, D-labels vs OR-labels, 2026-10-28 ACTION (3) vs 2026-11-06); lines read 3685-4921.
