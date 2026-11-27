# Blind antagonist: T-117 and T-056 item 3a (PR B, blind-then-compare)

Written 2026-11-27 by the blind antagonist (read-only; the engine ran only on a scratch copy at
`/tmp/claude-0/-home-user-guidebook/943cc08d-9b18-5690-b0c6-54a354b936e3/scratchpad/ant/t.db`).
Canonical DB sha256 at start: `sha256sum data/guidebook.db` → `3d419efb…edb9`, unchanged by this
work. Every figure below carries the command that derives it; re-run it, do not trust the figure.
Probe scripts: `…/scratchpad/ant/probe.py` (engine on 3 and 12 for MOB and WHEEL) and
`…/scratchpad/ant/probe2.py` (which headline governing rows state the shown bound, plus the new
table's band for each).

---

## PHASE 1 (blind: written before opening `design-t117-t056.md`)

### 1.1 Gates verified, not trusted

| Gate | Command | Read 2026-11-27 |
|---|---|---|
| OD-57, OD-59, OD-64 answered | `for n in OD-57 OD-59 OD-64; do grep -F "$n STATUS:" references/project-standards.md \| tail -1; done` | all `ANSWERED BY THE OWNER` |
| OD-31, OD-48 answered | same for OD-31, OD-48 | both `ANSWERED BY THE OWNER` (OD-48: "whom it is for", line from `git grep -n -E '^OD-48:' references/project-standards.md`) |
| OD-110 confirmed | `grep -F "OD-110 CHECK:" references/project-standards.md \| tail -1` | `confirmed with corrections applied` |
| OD-92, OD-99, OD-100 referred back | `grep -F "OD-92 STATUS:"` etc. | `REFERRED BACK TO THE OWNER` (all three) |
| OD-95, OD-98, OD-101 delegated | same | `RESOLVED UNDER DELEGATION` |
| T-119 merged | `git log origin/main --format=%s \| grep -c T-119` | ≥1 |
| T-054 merged (T-056's precondition) | `git log origin/main --format=%s \| grep -F T-054` | present |
| T-117 §2 edited per OD-110 | `grep -n 'Revised 2026-11-27 by OD-110' …/T-117-marker-table-applied.md` | present |
| Register entries OD-90+ | `grep -n '^### OD-9[0-9]' workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md` | present |

**Scope facts confirmed from the ledger text** (`sed -n "$(grep -n '^## Delegated resolutions 2026-11-27' references/project-standards.md | cut -d: -f1),\$p" references/project-standards.md`):
- T-059 slice, including the OD-101 eligibility union, waits (OD-101 last bullet; OD-110 "What waits").
- OD-92 Meanwhile: "the engine refuses the cell and names this question. That blocks 3 × MOB, not 12 × MOB."
- OD-99 Meanwhile: retrieved-but-UNVERIFIED sources "are kept and may govern without a route"; "A cell whose shown value one of them states is refused, naming this question"; interim test for "could not be retrieved" is Q2(b); C10 "fails a live cell when a governing source fails the interim test and has no route, or when every governing source is non-VERIFIED or grey and the marker is a circle."
- OD-100 Meanwhile: (a), "shown and listed, but does not govern"; reaches REF-00997 only.
- OD-95: "do nothing now"; Meanwhile a route-less unretrievable T1–T3 source "does not anchor". No academic-route record is to be built.
- OD-98: `rests_on_proxy_inference` is not by itself thin; a value is thin by project inference "only when no source in the lens states it"; "T-117 derives thin from neither" (neither PROXY grade nor contextual lens).

### 1.2 Defects in the task files themselves (reported, per T-117's own header)

- **D1. T-117 item 4, T117-04 (PROXY half) and T117-08 are stale against OD-98.** They still build PROXY-thin and the parent-pointer extension of `population_match`. OD-98 and OD-110 ("T-102: it was needed only for PROXY-thin, which is not built") remove both. OD-110 named only the §2 edit as owed, so the stale body survives. Build neither; the `population_match` parent extension has no reader once PROXY-thin is gone.
- **D2. T-117 item 4 "unverified → ⚠" and item 4a's C10 rule contradict OD-99's Meanwhile.** The interim is: retrieved-unverified stating source → refuse the cell (not ⚠); unretrievable route-less source → excluded from governing (OD-100), not ⚠. Under the interim, **no path writes ⚠ for "unverified"**.
- **D3. T117-03's grey half cannot go green.** A grey-only cell is `pending` (engine `elif b["t3g"]` branch; OD-97 Meanwhile "such cells stay pending"), and a pending row carries no marker (the second marker CHECK). Grey is never in `governing` in any other branch (anchored: T1/Co-1/T2/Co-2; provisional: T3 clinical; G1: T4–T6). So **⚠-for-grey is unreachable on any engine path today**. T-117 §8 forbids changing state. A test "T3 grey only → ⚠" must be redefined (e.g. a unit test of the marker function given a grey stating source) or named as blocked by OD-97.
- **D4. "Thin" by project inference is effectively unreachable.** `compose_value` composes only from stated governing bounds; probe2 shows each headline value is stated by at least one row. A thin branch reads nothing on the corpus; build at most the definitional check "no in-lens governing row states the shown bound" and say it examined 0 live cases.
- **D5. Two tasks, one PR.** Both task files say "One task, one pull request". Shipping T-056 item 3a alone (items 1–3, 5 not built) with T-117 is a coordinator's choice that must be stated in the PR, and T-056 stays open.
- **D6. T-117 item 5's "AFTER_DATA is required" is over-claimed.** See 1.5.

### 1.3 What the PR may build today (my specification)

**T-117**
1. `band()`: T3 non-grey → PARTIAL; T5 → WEAK; T1/T2 (which carry Co-1/Co-2 by `TIER_MAP`: `grep -n -E '"co[12]"' schemas/tier_derivation.py`) FULL; T4 PARTIAL; T6 WEAK. Grey's band left as is, never displayed; docstring says so (OD-64).
2. Delete `if regulatory_stratum_only: source_bands = []` (`grep -n 'if regulatory_stratum_only:' scripts/assess/assess_cell.py`) and fix the "Option A section 2.3 … is weak" comment.
3. **The stating set (OD-59 "its own")**: the headline governing rows (not conditioned) whose own bound equals the selected bound. This is a derivation from the values `compose_value` already picks. It is not the T-059 selection. The marker = the band of the stating source(s), keeping the R39 / OR-22b confirmation lift (`governance/tier-system.md` §5, "A floor claim that a verified, retrieved study confirms by absence takes that study's marker"; code `_confirmed_bands`) for a confirmed code row.
4. **Interim refusals, which are owner-reserved, so each REFUSES and names its question:**
   - several stating sources whose markers differ → `Refusal` naming OD-92;
   - a stating source that is retrieved but stored non-VERIFIED → `Refusal` naming OD-99 Q1.
   These are the ledger's own Meanwhile words. Choosing option (a) of either would decide the owner's question.
5. ⚠ written only for a grey stating source, or for a "no in-lens row states the shown bound" value (D3, D4: no live subject today; say so). ⚠ = `"⚠"`, and the code asserts there is no U+FE0F.
6. `EvidenceMarker`: add ⚠ such that `floor_mean` never averages it. `floor_mean` keeps callers (`_confirmed_bands`; the derived-figure rule in tier-system §5), so it is not deleted. Either ⚠ sits outside the ordinal-bearing members, or `floor_mean` refuses a ⚠ input, because "how ⚠ enters a derived figure" is "Not yet ruled (owner)" (tier-system §5). Note: appending a fourth member shifts every ordinal by +1 (`len(EvidenceMarker) - index`). For circle-only inputs `floor(mean+1) = floor(mean)+1`, so outputs are unchanged, but the docstring and tier-system's "● 3, ◐ 2, ○ 1" would be false.
7. **C10** becomes OD-99's Meanwhile rule, not T-117 item 4a's. It fails a live cell if (i) a governing source fails the interim test, or (ii) every governing source is non-VERIFIED or grey and the marker is a circle. Its subject stays the live published cells. **That subject is 0 on the canonical DB** (`select count(*) from specifications where state in ('stated','provisional') and retired_at is null` → 0), so every C10 red test must run on a seeded scratch fixture.
8. **Not built**: PROXY-thin, the `population_match` parent extension, any academic-route record or refusal (OD-95: "do nothing now"), the eligibility union (OD-101), and the engine-side exclusion of unretrievable sources from `governing` (OD-100). That exclusion changes the governing set and `derivation_sha`, which T-117 §8 forbids ("only the marker"); it is a selection or eligibility rule (T-059 slice). C10 is where OD-99's interim reaches it.
9. **The interim test for "could not be retrieved"** (needed only by C10): `verification_method IN ('corroborated-not-retrieved','citing-bibliography')`, or `retrieval_log.manifest_lines_for(...)` empty. C3's own warning ("the log does not type whether a line is the document, an index record or a probe") means the manifest half cannot certify that "the document" was retrieved. It can only certify "nothing at all was logged". That is a lower bound, and it is honest only because the `verification_method` clause catches REF-01002's index records. If the engine marker read the manifest, it would put a non-DB, non-hashed input into a value `derivation_sha` does not cover, and the engine's "pure function over the DB" claim would break. Keep it in C10 or out.

**T-056 item 3a**
10. The G1 line stops setting `design_scale = SCALE_UNIVERSAL` from the stratum. `design_scale` = `universal` iff `lens.identity_code` is None, else `population`, set once for every branch, not only G1. `regulatory_stratum_only` stays the stratum's one home. `RULE_VERSION` is bumped once for both changes (`derivation_sha` hashes it: `grep -n 'RULE_VERSION)' scripts/assess/assess_cell.py`).
11. Callers whose truth changes: the G1 docstring line (`grep -n 'G1  T4' scripts/assess/assess_cell.py`); `schemas/directness.py:51`'s comment "universal / code-compliant (Universal Mode)", which is the reading OD-48 rejected. It is a prose caller in code; the directness logic is untouched, because `determine` always passes `SCALE_POPULATION` to `assess_source`. Also `test_assess_cell_pilot.py` "T6-only => design_scale universal" (`grep -n 'design_scale universal' scripts/tests/test_assess_cell_pilot.py`), and prose callers OD-111 lists (`governance/evidence-methodology.md` l.144, `evidence-architecture.md` l.121, atom EVI-331). Those prose callers are T-120's, listed, not edited.
12. Retired rows keep their historical `design_scale` (no data rewrite; rule 3).

### 1.4 Probe: what the live-able cells and the 8 rows become

Commands: `python3 …/ant/probe.py …/ant/t.db` and `python3 …/ant/probe2.py …/ant/t.db` (run from the repo root).

| Cell | Engine today | Stating rows of the shown bound (probe2) | Under my spec |
|---|---|---|---|
| 3 × MOB | provisional, ≤ 5 %, proxy=1, rso=0, `universal`, **○** | ext 25 REF-00992 (T6 VERIFIED → ○), ext 28 REF-00994 (T4 **UNVERIFIED**, 3 manifest lines → ◐), ext 30 REF-00995 (T6 VERIFIED → ○) | **Refused**, naming OD-92 (○ vs ◐) and OD-99 Q1 (REF-00994). No row. Matches OD-92/OD-99 "blocks 3 × MOB". Not thin (OD-98: sources state it). |
| 12 × MOB | provisional, ≤ 6000 mm, rso=1, `universal`, **○** (by the override) | ext 116 REF-00988 (T5 VERIFIED, `600 cm`) only; 17 governing rows conditioned | **○** (T5 → WEAK; the override is gone, same glyph). `design_scale` → **`population`** (identity MOB). `has_unverified_sources`=1 stays (REF-01016 governs but does not state). |
| 3 × WHEEL, 12 × WHEEL | `Refusal`: no figure stated in this lens | none | unchanged (T-102/T-127 territory) |
| `specifications` (8 rows) | `select specification_id,state,marker,design_scale,regulatory_stratum_only,retired_at is null from specifications` → all 8 retired, marker NULL, rule_version pilot-3 | — | copied verbatim by the rebuild; every row satisfies the widened CHECK. No live row, so live-data comparison has 0 live subjects. |

Unretrievable test today (C2 + `manifest_lines_for`): REF-00997 0 lines (fails, OD-100: excluded); REF-01002 8 lines but `corroborated-not-retrieved` (fails); REF-00994, 01013, 01014, 01016, 01019, 01026 have ≥1 line (retrieved-unverified: may govern; refuse if stating).

### 1.5 Migration (my spec)

- Number: `ls scripts/migrations | grep -E '^[0-9]{3}_' | sort | tail -1` (→ 167) plus one; `user_version` likewise (`pragma user_version` → 167).
- Rebuild set, derived by transitive closure over `sqlite_master` (word-boundary match, views over views): the table, 2 indexes (`idx_spec_row_identity`, `idx_spec_retired`), 1 trigger (`trg_spec_retire_needs_reason`), 7 views (`v_best_practice`, `v_determination_provenance`, `v_divergence`, `v_gap_subject`, `v_item_provenance`, `v_pending`, `v_source_reach_all`); no view-of-view beyond those. Inbound FKs from `specification_source_links`, `specification_extraction_links`, `determination_gates` resolve by name after DROP+RENAME. The self-FK stays textual `specifications`.
- `sqlite_sequence` captured and restored as max (`select seq from sqlite_sequence where name='specifications'` → 8).
- CHECK: `marker IS NULL OR (marker IN ('●','◐','○','⚠') AND (regulatory_stratum_only = 0 OR marker <> '●'))`. **Strictly wider** than today's: any old-valid row (rso=1 ⇒ ○) passes. So no committed data migration can fail against it.
- **AFTER_DATA is not required.** Every data migration writing `specifications` (`git grep -l -E 'INTO\s+"?specifications|UPDATE\s+"?specifications' -- 'scripts/migrations/data_*' | sort | tail -1` → `data_20260918201549…`) is before the last existing cutoff (`grep -h -E '^--\s*AFTER_DATA:' scripts/migrations/*.sql | sort | tail -1` → `20261106053823`, at 146). Those rows exist before 168 runs and are copied, and no column is dropped (rule 5's clause does not apply). A marker is harmless if its cutoff ≥ that value, but it is not "required"; saying so is a prose error.
- Prove: `migrate_db.py --rebuild`, `migration_reproducibility.py --deep`, `PRAGMA foreign_key_check` empty, UNWRITABLE derivation unchanged.

### 1.6 Red tests that can go red and have a subject

- Unit tests on `band()` (T3 clinical, T5) and on the marker of a stating set: subject = the cases, red on today's code.
- Engine fixtures (as T-017's `_t017_cell`): T4-only → ◐ (red: ○); T1 stating + T6 non-stating → ● (red if floor mean); two stating sources of different bands → `Refusal` naming OD-92 (red: no refusal); a retrieved-UNVERIFIED stating source → `Refusal` naming OD-99 (red). The grey case is a unit test of the marker function only (D3).
- Migration: on a scratch copy, INSERT ⚠ accepted, ● with rso=1 refused, ◐ with rso=1 accepted (red before).
- C10: seeded live cell on a scratch copy (canonical subject is 0).
- T-056 3a: an identity-keyed G1 cell gives `population` (red: `universal`); an ICF-only cell gives `universal`.
- Seeded defects: restore the override; T5 → PARTIAL; ⚠ with U+FE0F; ⚠ admitted to `floor_mean`.

### 1.7 What reaches the guidebook if this goes wrong

A T4-only value shown ○ (understated); a T3 clinical figure shown ● (overstated, against OD-57); 3 × MOB shown ○ while REF-00994's unverified ◐ states it (the owner's open question decided by code); a code-only value labelled "universal" read as "for everyone" when it names MOB (OD-48).

---

## PHASE 2 (compare: `design-t117-t056.md` opened only after Phase 1 was written)

The blind spec and the design agree on most of the build. Both build: the table in `band()`, the override deleted, a stating set from `compose_value`, refusals naming OD-92 and OD-99, no PROXY-thin, no AFTER_DATA, the same rebuild closure, and the same T-056 3a rule. They diverge on five points:
- the design's engine **reads the retrieval log and re-gates the governing set** (OD-100 exclusion);
- an engine refusal for unretrieved T1–T3 sources (OD-95);
- the no-value path;
- the comment edit in `directness.py`;
- the `tier-system.md:81` departure.

### 2.1 Claim by claim

**Claim 1 (12×MOB publishes with no owner answer: ○, `population`, C10 green). SUSTAINED as an engine fact, overstated as "publishes".**
- Probe2: the only stating row is ext 116 (REF-00988, T5, VERIFIED). T5 becomes WEAK, so ○.
- REF-01016 (`manifest_lines_for` gives 2 archive.org lines of the NZS PDF) is retrieved, so neither C10 (i) nor (ii) fires.
- *Overstatement:* OD-91's basis reads "[ASSUMPTION: neither ramp cell may therefore be keyed on MOB]" (RULE 1184, "separate out … to start"). Writing a live row is a research batch (rule 10). The page still waits on OD-90, OD-104 and OD-112.
- Write "the engine composes and C10 admits", not "publishes".
- *If wrong:* a MOB-keyed ramp value reaches a page against a not-to-be-relitigated RULE.

**Claim 2 (3×MOB refused naming OD-99 and OD-92). SUSTAINED.**
- My probe2 gives the same stating rows: 25, 28 (REF-00994 UNVERIFIED with 3 manifest lines), and 30.
- *Defect in the sketch:* `if None in marks…: raise Refusal("OD-99…")` returns before the OD-92 test, so the text names only OD-99.
- OD-91's condition 2 reads which open questions a refusal names. Both block the cell, so name both: collect the reasons, then raise once.

**Claim 3 (thin needs no branch). SUSTAINED.**
- `_compose_headline` takes `min`/`max` over the parsed bounds (`grep -n 'vmax = min(his)' scripts/assess/assess_cell.py`).
- `_lo_from`/`_hi_from` already find the stating units by exact equality, so a shown bound is always some row's bound.
- *Residual, owner's meaning, not built:* an interval whose minimum comes from source A and maximum from source B. Each bound is stated, but the pair is no single source's. The OD-92 refusal catches it when the markers differ, and nothing catches it when they agree. Name it in the PR.

**Claim 4 (refusal is the only non-deciding interim). SUSTAINED.** It applies the ledger's own words: OD-92 "Meanwhile: the engine refuses the cell"; OD-99 "A cell whose shown value one of them states is refused".

**Claim 5 (refuse an unretrieved T1–T3 source, naming OD-95/OD-99). SUSTAINED that it decides nothing; it should not be built.**
- The design is right that applying OD-95's "route-less … does not anchor" needs a route definition OD-95 withholds ("settled then, or put to the owner"). Under the unratified 4758 reading, `corroborated-not-retrieved` *is* a route.
- (i) It mis-cites "OD-99 (Question 2)". Q2 is how non-retrieval is *recorded*, and interim (b) already answers it. The route question is OD-95's.
- (ii) It has no live subject. REF-01002 is the only such source, and it is gathered by no composing cell (OD-95 first bullet; the design's own §0).
- (iii) It duplicates C10 (i), which already fails a live cell whose governing source is unretrieved with route "not True".
- (iv) OD-95's heading is "do nothing now". §8's first option is to do nothing and say why. Drop the engine refusal and T117-10.
- *If wrong:* nothing reaches the book today, but a future T1 cell is wholly blocked where OD-95's interim would only withhold one anchor.

**Claim 6 (one home `dbcore.not_retrieved`, read by engine and C10). REFUTED: the cost is understated.**
- (i) `retrieval_log.LOG_ROOT = Path(os.environ.get("GUIDEBOOK_RETRIEVAL_LOG", "retrieval-log"))` is **cwd-relative** (`grep -n '^LOG_ROOT' scripts/research/retrieval_log.py`). The design's own probe had to `chdir`. `db.py` documents the same trap and works around it (`grep -n 'LOG_ROOT is cwd-relative' scripts/db.py`).
- Run from any other cwd, the engine sees no manifest. Every non-VERIFIED source then reads "not retrieved": REF-00994 is excluded or marked ⚠ instead of refused.
- That reaches beyond the marker. Exclusion changes `recs`, then `governing`, then the links, `derivation_sha`, and possibly state and value.
- (ii) The "already a CACHE" defence covers DB facts (verification, grading, edges). The manifest is outside the DB, and the engine header promises determinism over "same evidence + same rule_version".
- (iii) C3's own warning holds. An empty manifest certifies only "nothing logged", not "the document was not retrieved". Only the `verification_method` clause rescues REF-01002.
- *Simpler route (deletion-first):*
  - The engine reads no log. Any **non-VERIFIED stating source** raises one `Refusal` naming OD-99 (Q1) and OD-100, which decides nothing and is DB-pure.
  - Non-stating non-VERIFIED governing sources are left as today (OD-99 Meanwhile bullet 1).
  - `not_retrieved`/`route_shown` live in C10 only, which the registry runs from the repo root (resolve the root there anyway, as `db.py` does).
  - This deletes the engine exclusion, the routed-⚠ arm (no live reach: REF-00997 has `standard_number` NULL; REF-01002 is T1), T117-04, T117-10 and most of `synth_db`'s widening.
- *Scope, coordinator's call:* the OD-100 exclusion decides who may **govern**. That is eligibility, the subject of the T-059 slice and the OD-101 union that OD-110 defers. T-117 §8 says "only the marker".
- *If wrong:* a cwd-dependent governing set and marker.

**Claim 7 (keep the ● guard; set rso 0 under confirmation). SUSTAINED, with a fix.**
- OR-22's words support rso 0: "it is a confirmed claim, not a regulation-only floor".
- *Missed:* the proxy-branch precedent moves `tier_basis` with rso "because register_integrity_check cross-checks the two" (`grep -n 'tier_basis marker moves with it' scripts/assess/assess_cell.py`).
- `validate_evidence_state` treats a `tier_basis` ending `(regulatory_stratum_only)` as rso (`grep -n 'endswith("(regulatory_stratum_only)")' scripts/validate_evidence_state.py`), and `adjudication_integrity` counts rso=1 as "excluded from best-practice". So the "one line" is two, and it moves best-practice inclusion, not only the marker.
- No live reach: `select relation_id,to_extraction_id,to_label is not null from extraction_relations where relation='confirms'` gives 3 rows, all label referents. Either build it with `tier_basis`, or drop it and let the CHECK refuse loudly until a confirmed row exists.

**Claim 8 (no AFTER_DATA; 168 free; rebuild closure). SUSTAINED.** It matches my 1.5 independently:
- the closure is 7 views, 2 indexes, 1 trigger;
- inbound FKs are only the two link tables plus the self-reference (`pragma foreign_key_list` over every table; `determination_gates` has none, which corrects T-117 item 5);
- the last data writer of `specifications` comes before the last cutoff;
- the CHECK is strictly wider.

Note: 168 must be re-derived at build time. OD-110 records uncommitted `db.py` work in the tree that may claim a migration first.

**Claim 9 (3a changes design_scale on six cells, no code reader breaks). SUSTAINED, with two corrections.**
- `…/ant/probe3.py` reproduces 3, 4, 5, 6, 9, 11 and 12 × MOB as `universal` today; 3 is refused after, leaving six.
- (i) "Nothing else" is loose. The `RULE_VERSION` bump changes every cell's `derivation_sha` (`sha(...)` hashes `RULE_VERSION`). That is intended, but it is a change.
- (ii) §1.5's comment edit to `schemas/directness.py:51` ("names no group (OD-48)") makes that file contradict itself and `scripts/audit/matrix_consistency.py`:
  - line 51 would say one thing;
  - the scale-directness docstring and constants say "CODE … DIRECT only at Universal (it IS the floor)" (`grep -n -E 'Universal' schemas/directness.py`);
  - `matrix_consistency.py:24` encodes `("code","universal"): "DIRECT"`.
- The directness token still carries the Universal-Mode meaning OD-48 rejected for `specifications.design_scale`. A comment cannot settle that, and OD-111 did not list it.
- Drop §1.5, and list `directness.py` and `matrix_consistency.py` for T-120 as a second home of the token's meaning.
- Also: ALL-keyed cells stay `population` (probe3: 4–11 × ALL), against OD-31's universal, until T-056 items 1–3 and T-115 land. Interim; name it.

**Claim 10 (no-value branch: R7 floor mean; refuse a ⚠/circle mix as OD-92). REFUTED in part.**
- Keeping R7 for a cell with no shown value is the status quo, and OD-59 is silent there. That part stands.
- The sketch's `if None in marks.values(): raise Refusal("OD-99 …")` runs **before** the `value_shown` split. So on a no-value cell, any retrieved-UNVERIFIED *governing* source refuses the cell.
- OD-99's Meanwhile refuses only "a cell whose shown value one of them states". Bullet 1 says such sources "are kept and may govern without a route". This stretches OD-99 past its words, which is worse than the stretch the agonist flagged.
- The ⚠/circle-mix refusal decides nothing. Its warrant is the 2026-11-14 entry's "What it does not decide: How a cell resting on a grey or unverified source together with others is marked" (`grep -n -F 'How a cell resting on a grey or unverified source together with others' references/project-standards.md`), not OD-92, which is about stating sources.
- Fix: in the no-value path, keep today's rule (unverified left out of the floor mean) and refuse only on a ⚠ mix, citing that entry. No live reach (probe3: every composing cell shows a value).

**Claim 11 (grey arm unit-tested, read later). SUSTAINED, with a test defect.**
- `select tier, evidence_type, count(*) from evidence_sources group by 1,2` shows grey only at T3 (6 rows). Grey never governs (`grep -n 'elif b\["t3g"\]' scripts/assess/assess_cell.py`).
- *Defect:* `own()` is sketched as a closure inside `determine`, so T117-03 cannot call it. Lift it to a module-level function taking `(rec, confirmed_band)`.
- "read after the T-059 slice" is [UNVERIFIED]: OD-97, a grey-only cell shown ⚠, is the other reader, and it is referred.

**Claim 12 (four T-117 statements unbuildable). SUSTAINED.** It agrees with my D1, D2 and D3, and adds T117-06's T1+T6 fixture (`if anchors:` makes `governing` the anchors only).
- *Add:* T117-03's engine-level grey half (D3).
- *Procedural:* the delegated entry's ACTION (1) requires the task-file edits before acting on OD-90 to OD-113. The design's own §6 stop condition makes this blocking, which is right.

**Departure (§4): delete `governance/tier-system.md:81` here. REFUTED.**
- The line reads "Until T-117 lands, … `band()` and the … CHECK implement the earlier table; the table above governs". After T-117 lands it is *spent*, not false: it never asserts the post-landing state.
- T-117 item 6 forbids the edit, and lists such lines for T-120, which rewrites §5 anyway. No exception is needed, so list it and follow item 6.

### 2.2 The red tests: can each go red, and does each have a subject?

| Test | Goes red on the named defect? | Subject | Finding |
|---|---|---|---|
| T117-01 | yes (○ from the override; one T4 is rich: `grep -n '">=1 T4' scripts/assess/assess_cell.py`) | fixture | ok |
| T117-02 | yes (unit) | case | ok |
| T117-03 | circle half yes; grey half **cannot run** (closure, claim 11) | case | fix: module-level `own` |
| T117-04 | yes as designed | fixture | drop if claim 6's simpler route is taken |
| T117-05 | yes | scratch DDL | ok |
| T117-06 | yes (○ from the override, against ◐) | fixture (T4 makes it rich) | ok |
| T117-07 | **only if the fixture is provisional**. "states the value alone" with one T6 is below §2.3 richness (≥3 T6 in ≥3 jurisdictions, `regulatory_richness`), so it is pending before and after: no ○ today, no refusal after | fixture | fix: ≥3 VERIFIED T6 jurisdictions, or a T4, beside it |
| T117-08 | yes (T4 makes it rich) | fixture | ok |
| T117-09 | **same richness trap** with two T6 sources | fixture | fix as T117-07 |
| T117-10 | yes, but the behaviour is dropped (claim 5) | fixture | out |
| T117-11 | (a), (b), (c) yes. **(d) is red for the wrong reason on an unmigrated copy:** seeding `⚠` fails the live CHECK (IntegrityError) before C10 runs | seeded live cells; canonical C10 subject is 0 (`select count(*) from specifications where state in ('stated','provisional') and retired_at is null`) | fix: seed (d) on the migrated copy; print C10's EXAMINED for the seeded copy |
| T117-12 | yes | case | ok |
| T056-01/03/04 | yes | fixture | ok |
| T056-02 | [UNVERIFIED]: whether an ICF-only cell can be *anchored* (identity None makes directness NOT_ASSESSED and caps it at DOWN-WEIGHTED, G2) | fixture | build the fixture first and show it is `stated`/`provisional` |

### 2.3 What the design missed

1. M1: the cwd-relative `LOG_ROOT` in the engine (claim 6).
2. M2: the two meanings of `universal` in `directness.py` and `matrix_consistency.py` (claim 9).
3. M3: the OD-99 refusal on no-value cells (claim 10).
4. M4: the richness trap in T117-07 and T117-09, and T117-11(d) going red for the wrong reason.
5. M5: `tier_basis` and best-practice inclusion move with the rso flip (claim 7).
6. M6: the refusal names only the first question (claim 2).
7. M7: the two-tasks-in-one-PR departure from both files' "One task, one pull request". State it, and leave T-056 open for items 1–3 and 5.
8. M8: `own()` duplicates `_verified` with a literal `"VERIFIED"`. Use `_verified` (rule 8, one home).
9. M9: the min-from-A, max-from-B interval (claim 3 residual).

### 2.4 Verdict table

| Claim | Verdict | Severity | SPLIT |
|---|---|---|---|
| 1 | SUSTAINED (overstated "publishes") | note | build now |
| 2 | SUSTAINED (name both questions) | fix in design | build now |
| 3 | SUSTAINED | note | build now |
| 4 | SUSTAINED | note | build now |
| 5 | SUSTAINED (decides nothing) but redundant, mis-cited, no subject | fix in design (drop) | out |
| 6 | **REFUTED** (cwd-relative log in engine; governing set, not only marker; eligibility scope) | **blocks build** as designed | engine half: wait for owner (OD-99 Q2/OD-100) or coordinator; C10 half: build now |
| 7 | SUSTAINED (move `tier_basis`; no live reach) | fix in design | build now with the fix, or out |
| 8 | SUSTAINED | note (re-derive 168) | build now |
| 9 | SUSTAINED (drop the §1.5 comment edit; sha note) | fix in design | build now |
| 10 | **REFUTED in part** (OD-99 stretched on no-value cells; wrong cite) | fix in design | status-quo R7: build now; the ⚠ mix: wait for owner |
| 11 | SUSTAINED (lift `own`) | fix in design | build now |
| 12 | SUSTAINED (+ T117-03 grey half) | **blocks build** until the task file is edited (ACTION (1)) | build after the edit |
| §4 departure (tier-system:81) | REFUTED (spent, not false) | fix in design | out (list for T-120) |
