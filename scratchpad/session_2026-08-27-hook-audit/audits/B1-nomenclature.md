# B1 — Nomenclature and grammar correctness: WALKABILITY-PLAN.md

**Adversarial audit, 2026-08-27.** Lens: is the proposed naming system correct and executable by a
Sonnet/Opus session, or does it produce ambiguity, collisions, or an underivable schema.

**Version audited.** `scratchpad/session_2026-08-27-hook-audit/WALKABILITY-PLAN.md` at commit
`186641a`, **1,312 lines**. The subject grew mid-audit: `186641a` (author-time 04:18, message
timestamp `[04:42]`) appended **196 lines — the whole of PART 10** — after this audit began against
the 1,116-line `4f38fd8`. Pure append (196 insertions, 0 deletions; verified
`git show --stat 186641a`), so line citations ≤1073 are stable across both versions. Everything
below is stated against `186641a`.

**Conventions, stated per §2(b).** DB figures from `data/guidebook.db` at `user_version` 64,
read-only (`sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)`). "Key-shaped" = column
name suffix in {`_id`,`_code`,`_ref`,`_key`} — the plan's own 10.1 convention. "Junction side":
*near* = the stage-internal table the junction hangs off; *far* = the table it points at.
Cross-checked against `NOMENCLATURE.md` Parts A–L, audits A1–A4, `CLAUDE.md`, and
`references/project-standards.md` from :1440.

**Verdict up front.** The grammar's closed set is sound for records, runs and registries, the
Part 6.2 map is complete over all 66 tables, and the plan's own measurements reproduce exactly.
But the plan is **an audit trail wearing a runbook's clothes**: its executable surfaces (the 6.2
map, T-A2's DDL, T-A3's acceptance queries, the ⛔ GATE, the T-B task list) are all left
contradicting Part 9's and Part 10's own corrections, held together only by "Part 9 wins"
(:862) with no consolidated final map; and Part 10's five laws, run as written, turn red on the
very spine Part 10 orders minted. A Sonnet executing this document as tasks will build refuted
work; an Opus must first re-do the reconciliation this plan says it already did.

---

## BLOCKERS

### B1-1 · The executable surfaces are stale against the plan's own corrections, and no operative map exists

The plan's rule — *"Where Part 9 and an earlier part disagree, Part 9 wins. The earlier text is
left in place"* (:862–863) — is a record-keeping choice imposed on an execution plan. The stale
sites an executing session will actually read:

| executable site | says | refuted by | refutation site |
|---|---|---|---|
| 6.2 map :385, T-A2 :735, §6.3 queries :493–495 | `evi_items.research_item_id NOT NULL` | K1: key belongs on `evi_sources` | :916 |
| T-A3 acceptance 1 :786 | walk `res_items → evi_items` "using only hand-off keys" | unsatisfiable under K1 — no such key on `evi_items` | :916 |
| 6.2 :394, jud row :399, T-A2 columns :750–753 | fold `evidence_population_match` into `jud_items` | X4: refused on grain; satellite `jud_population_grades` | :872 |
| GATE Q1 :703–708 | sends the 25-grades measurement, "Confirm (b)" | X3: "the measurement does not reach the question… no false measurement attached" | :871, :883–897 |
| GATE Q2 :710 | "does `item_code` rename with `items`" | 9.6: "Q2 should be re-put in those terms" (re-grain registry) | :1009 |
| T-B.5 :807, 6.2 :389 | retire `search_admissions` | 9.5: "moves… to KEEP" | :968 |
| T-A2 junction spec :737–738 | `syn_judgment_links (≥1)`, no UNIQUE | 9.2 recommends (d): `UNIQUE(judgment_item_id)` | :895–897 |
| T-A2 :743–760 (`jud_items` columns) | one column set | second set at §10.3 :1212, third implied by X4; 10.5 orders "the §10.3 spine **exactly**" | :1212, :1253 |

**What breaks:** a Sonnet given "execute T-A2" transcribes :735–760 — the wrong key host, the
refuted fold, no UNIQUE decision — because nothing in Part 7 says it is superseded. The failure
scenario is the exact one the plan diagnoses in NOMENCLATURE (A3-F1: "Part E is the table a
migration-writer will transcribe DDL from").
**Smallest fix:** one consolidated PART 11 — final map + final task list — that supersedes 6.2 and
Part 7 row-by-row, with the GATE text rewritten. Nothing else in B1-1 needs new decisions; it is
collation the plan already owes.

### B1-2 · `evidence_population_match` (the only live-data cross-stage table) has three incompatible dispositions and its successor appears in no map or task

Fold into `jud_items` (:314, :394, :399, columns :750–753) · one of the "10 renames" in the Track-B
sweep (:291) · satellite `jud_population_grades` (:872, and §10.3 :1212 assumes it). The operative
answer per Part 9 is the satellite — but **`jud_population_grades` is absent from the 6.2 map, from
every T-task, and from the arithmetic at :629–635 and :976–986** (the fold's `−1` survives at :631
and :978 even after X4 refuted the fold — so 9.5's own corrected arithmetic still counts a table
the same Part un-deleted). Derivation command for the row's stakes:
`SELECT COUNT(*), COUNT(DISTINCT ref_id) FROM evidence_population_match` → 25, 10 — the only rows
with live data anywhere in stages 3–6.
**What breaks:** the one table whose migration touches reasoned content has no executable
destination; whichever a session picks, another part of the plan calls it wrong.
**Smallest fix:** add `jud_population_grades` to the judgment map and to T-A2 or T-B by name, and
correct both arithmetics (the fold's −1 becomes ±0).

### B1-3 · Part 10's laws, run as written, flag the spine Part 10 orders minted — the checker is born red against its own target schema

10.4 specifies `wiring_grammar` "reading only `sqlite_master`" (:1234), and 10.5 orders T-A2 to
"mint the five hand-off objects with the §10.3 spine **exactly**" (:1253). Measured:

- **Law 2** (:1156–1160, test `col == singular(target)+"_id"`): every proposed hand-off column
  fails it. `research_item_id REFERENCES res_items` → required name `res_item_id`;
  `evidence_item_id` → `evi_item_id`; likewise `judgment_/synthesis_/specification_item_id`,
  `dissent_of_judgment_item_id` (:1212), `parent_research_item_id` (:1210). `singular(res_items)`
  is `res_item`, and a checker reading only `sqlite_master` cannot expand `res_` to `research`
  without `pipeline-contract.yaml`. The §10.3 TOPIC block fails too: `slug`, `item_code`,
  `population_code` ≠ `slug_id`/`item_id`/`population_id`. On the current schema the mechanical
  test fails **75 of 80** FK columns (command below) while 10.1 claims **6** mis-named (:1101) —
  the law's formal test and its own baseline measurement disagree 12×.
- **Law 1** (:1149–1152, test `keyish(col) XOR (isPK ∨ isFK)` empty): flags **31** PK/FK columns
  that are not key-shaped — including `slug` (12 tables), `lang_jur_map.jurisdiction/language`,
  `term_aliases.alias/language`, `access_duration.code` — while 10.1's "13 liars" counts only the
  other direction. The 13 reproduces exactly under (keyish ∧ ¬PK ∧ ¬FK); the XOR form yields
  13+31=44. And §10.3's own spine declares `slug TEXT REFERENCES slugs(slug)` (:1198) — a column
  Law 1's stated test flags.
- **Law 5** (:1176–1180): "a script that reads only table and column NAMES can decide whether a
  key points forward" — false: the lexical order of the prefixes is
  `evi < jud < ren < res < spe < syn`, not the pipeline order; the order lives only in the
  contract, which the checker is told not to read.
- **Law 3** (:1163–1165): its second test ("no reference column's values contain a delimiter")
  requires reading **data**, contradicting "reading only `sqlite_master`" twice stated
  (:1147, :1234).

```python
# Law-2 failures on current schema (75/80), Law-1 XOR flags (31):
import sqlite3
c=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
ts=[r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]
sing=lambda t: t[:-1] if t.endswith('s') else t
print(sum(1 for t in ts for r in c.execute(f"PRAGMA foreign_key_list('{t}')") if r[3]!=sing(r[2])+'_id'))
keyish=lambda x: x.endswith(('_id','_code','_ref','_key'))
print(sum(1 for t in ts
  for col in ({r[1] for r in c.execute(f"PRAGMA table_info('{t}')") if r[5]>0}
             |{r[3] for r in c.execute(f"PRAGMA foreign_key_list('{t}')")})
  if not keyish(col)))
```

**What breaks:** T-0 builds `wiring_grammar` advisory (:1256) → it reports ~106 findings, not the
13+7+6 promised; T-C promotes it blocking (:1260) "once T-B has cleared its findings" — but T-A2's
freshly minted spine is itself among the findings, so either the checker is quietly rewritten at
the keyboard (the invented-regex failure class, standards :1640s) or it never promotes.
**Smallest fix:** (a) define `singular()` over stage prefixes via the contract and say the checker
reads the contract; (b) exempt substrate code-keys explicitly — a mint-side `_code`/`slug` PK and
its FK copies are legitimate key shapes on both ends; (c) re-derive 10.1's baseline from the laws'
formal tests so the check's first report matches its spec.

### B1-4 · 9.3-K1 silently destroys C5's partition, T-A2's "no AFTER_DATA", and the document's headline

The headline (:9–11) and Track A's charter (:294, :653, :728–730) rest on "the spine touches only
zero-row tables with zero replay collisions… No baseline. No `AFTER_DATA`." K1 (:916) moves the
research→evidence key to **`evi_sources` = `evidence_sources`**: 10 live rows, and **14** data
migrations executing DML against it under the plan's own operative definition (:1050–1058; replay
command in the Appendix). Adding a NOT NULL FK column there is a create-copy-swap **with data**,
needs the six no-lead sources backfilled with `res_items` rows (A3-F3's own fix), and a data
migration INSERTing into `evidence_sources` without the new NOT NULL column fails on replay unless
the migration is `AFTER_DATA`-ordered or the column carries a default. **Nobody re-ran the C5
partition after K1**; Track A now contains exactly the collision-bearing table C5 quarantined into
Track B.
**What breaks:** `migrate_db.py --rebuild` (T-A2's own acceptance, :770) fails on the first of the
14 colliding files, or the key ships nullable-in-effect via a default — §2(a) wearing DDL.
**Smallest fix:** re-run the C5 measurement with `evidence_sources` in Track A; the honest
statement is "one ordinary migration **plus one `AFTER_DATA` marker plus a six-row backfill**",
which is still cheap — the claim just has to say it.

---

## MAJORS

### B1-5 · The grammar did not "survive the audit": three filed grammar defects are unfixed and unacknowledged

:340 claims "The grammar — carried forward unchanged, it survived the audit." A2 filed D1–D5
against grammar application; the plan's Part 9 never cites the D-series (grep `A2-D|mass noun`
over the plan → only :342/:353, the grammar's own text):

- **D1 unfixed** — `search_executions → res_searches` (:374) on the taste note "the row is a
  search", while the run test (:351, "a record of an act performed, carrying a timestamp and an
  outcome") matches it verbatim: `PRAGMA table_info(search_executions)` → `executed_at`,
  `results_found/screened/admitted`. By the closed set's own test the name is `res_search_runs`;
  `citation_mining`, the equally act-shaped table, gets `_runs` (:375). The suffix is being
  assigned by taste, which is precisely what :351's "decided by a test… rather than by taste"
  forbids.
- **D2 unfixed** — `syn_convergence` (:409): mass noun, violates ":342 head noun always plural".
- **D3 unfixed and worsened** — junction subject-side is unpredictable: far-side named
  (`evi_slug_links` :388, `syn_item_links` :407, `syn_judgment_links`), near-side only with the
  far side dropped (`ren_room_links` :433, `ren_case_study_links` :435, `ren_economics_links`
  :438 — the two rows flagged "named for the specification, foreign-keyed to `items`" get a fix
  that names **neither**), both sides (`language_jurisdiction_links` :455,
  `access_need_icf_links` :457). The grammar states no side rule, so a reader cannot predict
  which junction a name denotes.

**Smallest fix:** state the junction side rule once (recommend: far side, near side only when the
stage has >1 junction to the same far table), rename the three render junctions to carry their far
side, `res_searches → res_search_runs` or amend the run test, and give `syn_convergence` a plural
head (`syn_convergences` or fold per J.4).

### B1-6 · The 6.2 net arithmetic is wrong under every reading, and the document carries four end-states

:470 — "Net: 66 → 61 tables (5 deletions, 3 creations, 1 fold, 1 retirement)". Derived from the
map's own rows (command in my worklog; re-runnable by grepping the 6.2 block for `⊘`/`*(n`):
existing-table deletions = **4** (`search_coverage`, `search_languages`, `reference_stubs`,
`situations`; the fifth ⊘ is `ren_items`, which never existed), creations = **4** (`jud_items`,
`syn_judgment_links`, `syn_synthesis_links`, `spe_synthesis_links`; the parenthetical says 3).
The parenthetical's own arithmetic gives 66−5−1−1+3 = **62**; the map's rows give 66−4−1−1+4 =
**64**; neither is 61. Elsewhere: 66→48 (:338, :599), 66→49 (:638), 52–63 (:989). Four terminal
counts, none derived, in a document whose §0 quotes §2(b)'s ban on hand-written counts at itself.
**Smallest fix:** delete every net figure except 9.5's range, and derive that range from the map
programmatically in the appendix.

### B1-7 · The retired word is relocated into the new spine, not dissolved

The `-item` ruling's stated reason: "the word was the ambiguity" (CLAUDE.md, standards :1607).
Under this plan a reader still meets the retired sense in: `jud_items.item_code` — **minted new**
at :747, NOT NULL; §10.3's TOPIC block putting `item_code` on **all five** hand-off objects
(:1199); four junction names (`item_population_links`, `item_demand_links`, `term_item_links`
re-pointed unchanged :443–451, plus coined `syn_item_links` :407); and 9.6's re-grained registry —
which is the right remedy but **is never given a name** (:996–1009 specifies `code` PK +
`canonical_label` UNIQUE and no table name), so the most-referenced substrate table's post-plan
name is undefined and `syn_item_links`' far side dangles with it. Q2's GATE wording (:710,
"table-only now, column later") does not match 9.6's re-put (:1009), so even the owner question
that governs this is stale. **Verdict on the brief's question 2: 9.6 dissolves the
recreated-registry problem and relocates the word problem — partly into the spine itself.**
**Smallest fix:** name the registry (grammar-compliant: a registry mints a code and takes no
suffix — `parameters`), decide `item_code`'s successor name in the same breath, and rewrite GATE
Q2 in 9.6's terms.

### B1-8 · The reference-ID grammar (§6.4) has no tasks, and T-A2 contradicts it

§6.4 mandates minted `<STAGE>-NNNNN` codes (:528) and makes the 11 `REF-VERIFIED-*` re-mints a
precondition — "before the per-stage allocators are written" (:543–544). No T-phase contains
either: grep `re-mint|NNNNN|allocator` over Part 7 → nothing. Meanwhile T-A2's DDL keys the spine
on the surrogate §6.4 condemns — `evidence_item_id … REFERENCES evi_items(extraction_id)` (:746),
`extraction_id` being one of the four INTEGER PKs listed as defects at :522. §10.3 then asserts
TEXT PKs `RES-00001/EVI-00001/…` (:1191–1193) with no re-key task for `evi_items`/`spe_items`
anywhere. And the namespace question is never answered: `res_items` holds 875 ids **already
minted as `REF-`** — do they re-mint to `RES-` (an 875-row id rewrite touching the shared
`REF-` space that `evidence_sources` also uses, C.1), or does research keep `REF-` (leaving the
id grammar inconsistent across stages and :528's `RES-NNNNN` wrong)? A Sonnet cannot decide this;
an Opus is given no criterion.
**Smallest fix:** one T-A2 sub-task: "PK kind per hand-off object, the REF-vs-RES decision, and
the 11 re-mints, before DDL" — plus align :746 with whichever wins.

### B1-9 · The 9.7-H drift check is a real gap correctly identified but not specified enough to build

The one sentence (:1022) leaves undefined: **(a) scope** — which tables are exempt. Measured false
positive: post-plan substrate keeps **`icf_demands`** (:459, already ruled), which matches
`^[a-z]{3}_` with a non-stage prefix; a naive checker flags a ruled name, and the exemption list
is a substrate allowlist whose home the plan does not name — hardcoded in the check it reproduces
the exact defect T-0.1 exists to fix (:667). **(b) Direction** — orphaned prefixes vs stage ids is
stated; missing-stage and view exclusion (`v_*`) are not. **(c) §2(a) instrumentation** — no
`EXAMINED:` and no `min_items`, the same omission A4-B11 filed against the vocabulary check.
**(d)** Its motivating figure "stored in 60+ table names" is a hand count: the 6.2 map yields
**~43** stage-prefixed names (7 res + 9 evi + 2 jud + 10 syn + 5 spe + 10 ren, before 9.5's
deletions), not 60+. The check should also own Law 5's ordering source (see B1-3) since both need
the contract.
**Smallest fix:** three sentences in 9.7-H: scope = tables matching `^(res|evi|jud|syn|spe|ren)_`
plus an assertion that no *other* table matches `^[a-z]{3}_` except a named allowlist kept in the
check-registry entry's config; compares against `stage_id[:3]` derived live from
`pipeline-contract.yaml`; prints `EXAMINED: <tables scanned>`, `min_items` = current stage-table
count. *(What holds: T-A1.6's selftest distinctness assertion (:692) is the right home for the
collision half, and `stage_id[:3]` is collision-free on the six ruled ids — `res evi jud syn spe
ren`, verified trivially.)*

---

## DEFECTS

- **B1-10 · `figures` vs `ren_figures`.** :587 and the 9.5 arithmetic (:984) create unprefixed
  `figures`; 9.3-K4 (:919) requires "a stage prefix (`ren_`)". Both are post-correction sections;
  under Part A's rule "no prefix means not a stage", the unprefixed form asserts substrate — the
  substrate-points-downstream inversion the plan itself flags (:463). Pick one; fix the
  arithmetic's label.
- **B1-11 · `connections`/`connection_targets`.** "open (J.2)" at :411 vs Tier-1 "delete now" at
  :954; no T-task deletes them (T-B.5 :807 lists four tables only). The 9.5 range arithmetic
  (−6 Tier 1, :977) silently includes a deletion no task performs.
- **B1-12 · 9.2's option (d) misdescribes itself.** "(d) … keeps every guarantee the junction was
  chosen for" (:895–897) — false: the junction was chosen partly because a back-pointer would
  "forbid one judgment feeding two syntheses" (standards :1568–1571, carried at 6.1). (d)'s
  `UNIQUE(judgment_item_id)` forbids exactly that; its only remaining advantage over a
  back-pointer is write direction. Recommending (d) may still be right — the ruling is N:1 — but
  the sentence selling it is wrong, and an owner shown (d) on that description is being shown a
  false prospectus.
- **B1-13 · The `<prefix>_population_links` derivability pitch fails its own map.** 6.1 (:359–361)
  sells "six predictable names… a reader who knows the rule never has to look any of them up";
  the map contains **zero** tables literally named `<prefix>_population_links` — every one embeds
  a different near-side noun (`evi_item_`, `spe_probe_`, `syn_citation_`, `ren_case_study_`,
  `ren_economics_`), and render needs two, so the uniform scheme is impossible as sold.
- **B1-14 · Near-side ambiguity on satellites.** `evi_slug_links` (:388): a grammar-reader
  predicts evi_items×slugs; the actual near side is `evi_sources`. Same class:
  `evi_admission_links` (:389) names the *event*. The grammar has no way to say which
  stage-internal table a junction hangs off; with `evi_item_population_links` (:390)
  disambiguating and `evi_slug_links` not, the reader cannot tell whether an absent noun means
  "the hand-off" or "the sources satellite".
- **B1-15 · Column-name drift inside the plan.** `parent_item_id` (:379 note, J.1) vs
  `parent_research_item_id` (:1210); `dissent_of` (:757) vs `dissent_of_judgment_item_id`
  (:1212); `item_code`/`population_code` NOT NULL at :747–748 vs nullable in §10.3's TOPIC block
  (:1199–1200). 10.5's "exactly" (:1253) resolves none of these because T-A2 stands unpatched.
- **B1-16 · `res_code_leads`** (:373): not derivable — nothing in the grammar or the note produces
  "code" (it means *building-code* lead; the word collides with `item_code`'s sense of code). A
  legal record-kind name, but a reader who knows the rule cannot predict it; one clarifying word
  in the map note fixes it.

**Answer to the brief's question 4 — names a rule-knowing reader cannot predict or parse:**
`res_searches` (fails the run test), `res_code_leads`, `syn_convergence` (number), `evi_slug_links`
and `evi_admission_links` (near side unstated), `ren_room_links`, `ren_case_study_links`,
`ren_economics_links` (+ subject truncated vs `ren_economics_entries`), `syn_item_links` (retired
sense; far table unnamed after 9.6), `figures`-vs-`ren_figures`, the unnamed parameter registry,
and — under the plan's own Law 2 — every hand-off FK column as currently spelled.

---

## Attacked and held

- **Coverage:** all 66 tables appear in the 6.2 map — zero omissions. Command: extract the 6.2
  block, diff backticked names against
  `SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'` → `[]`.
- **Collisions:** no two current tables map to one proposed name; no proposed name collides with
  an existing table or view (checked against all 66 + 18 `v_*`). The `_items` suffix reservation
  is actually enforced by the map: the only current non-hand-off `*_items` table, `room_items`,
  is renamed away (:433).
- **Prefix derivation:** `stage_id[:3]` over the six ruled ids yields six distinct codes,
  including `specification`→`spe` and hyphenated `evidence-collection`→`evi`.
- **10.1's measurements:** 876 columns, 480 distinct names, and exactly the 13 listed liars all
  reproduce under the stated convention (commands in my worklog; liar test =
  keyish ∧ ¬PK ∧ ¬FK). The convention is stated in the document — the first section in this
  saga to do so unprompted.
- **9.9's DML-only replay convention** is stated, defensible, and explains the A3-F9 divergence
  honestly.
- Ruled renames match their rulings: `icf_demands`, the three `*_demand_links`, plural fixes
  `weighting_profiles`/`access_durations`, `term_aliases` withdrawal reasoning (payload test).

## Digest

Checked: the full 1,312-line plan (incl. the 196-line Part 10 appended mid-audit), every Part 6.2
row against the grammar's own tests, all four prior audits, and 14 measurements re-derived from
the DB/tree. Refuted: "the grammar survived the audit" (:340 — A2's D1–D3 stand unfixed); the 6.2
net arithmetic (61 vs derived 62/64, four end-states); "no AFTER_DATA" for Track A after K1;
Part 10's laws as executable ("6 mis-named" vs 75/80 under its own test; Law 1 XOR flags 31 more
incl. §10.3's own `slug`; Law 5's order not name-derivable). Overstated: "60+ prefixed names"
(~43); 9.2(d) "keeps every guarantee". Confirmed: complete 66-table coverage, zero name
collisions, distinct prefixes, 876/480/13 exact, DML-only convention sound. Net: **4 BLOCKER
(stale executable surface; epm's three destinations; laws-vs-spine contradiction; K1-vs-C5), 5
MAJOR, 7 DEFECT** — the naming *scheme* is salvageable in one consolidation pass; the *document*
is not executable as ordered.
