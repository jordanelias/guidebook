# Adjudication of the governing documents — conflicts and staleness

Written 2026-11-26 by a read-only Opus-class adjudicator. Repository state read: `origin/main` at `71b7c58` (merge of PR 246), schema `PRAGMA user_version` read live (derive: `python3 -c "import sqlite3;print(sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True).execute('pragma user_version').fetchone()[0])"`). The clone is shallow (`git rev-parse --is-shallow-repository` prints `true`), so commits older than the clone's depth cannot be shown; where that matters it is marked [UNVERIFIED].

**Nothing here is applied.** Every item goes to the owner. Framing (owner, typed, 2026-11-26, relayed by the coordinator): *"our goal for Opus is to deliberately and cleanly reorganize our ecosystem so that it is unified and consistent and easily findable for each session as per claude.md"*. Each reconciliation therefore prefers, in order: no change; a pointer; deleting a dead sentence; an appended dated note (the repo's append-not-edit practice for ratified text); and only then rewording. Edits to `decisions/` need an attestation (CLAUDE.md rule 2). Line numbers are as read at `71b7c58` and drift; locate by the quoted text.

Approval classes: **OWNER-ONLY** (decision-protocol §2.4, or a mechanism the schema binds to an "Owner" ledger entry); **DELEGABLE** (within the 2026-11-25 grant as bounded by OD-79); **ALREADY-SETTLED-BY-OWNER-WORDS** (the owner has ruled; only the record lags). Doctrine files remain the owner's to merge even where the ruling is settled.

## Summary table

| ID | Verdict (one line) | Approval class |
|---|---|---|
| ADJ-01 | The axis layer was retired by owner rulings (2026-08-18, 2026-08-24, 2026-09-13) and executed by migration 109; most of functional-taxonomy.md is superseded or history; a short list of principles survives | ALREADY-SETTLED-BY-OWNER-WORDS (owner merges the annotation, per R35) |
| ADJ-02 | conceptual-model.md's Item entity, relationship map and file inventory are dead; one header note stops a session treating them as live | ALREADY-SETTLED-BY-OWNER-WORDS |
| ADJ-03 | Mission's "population" language uses the word in a permitted sense and does not conflict with the lens ruling; one owner question remains on "median as default" | (a) no change; (b) OWNER-ONLY |
| ADJ-04 | No document states the true authority order; the DR overstates its own supremacy and CLAUDE.md §9 routes "what to do now" to it | DELEGABLE (wording); content settled by owner words |
| ADJ-05 | The rule-10 suspension covered one pull request (PR 243), which merged 2026-11-20; it has expired and rule 10 stands | ALREADY-SETTLED-BY-OWNER-WORDS; no change |
| ADJ-06 | Rule 9 governs over any default-subscribe instruction; its enforcement sentence is stale and the deny entries may not match live tool names | DELEGABLE (CLAUDE.md sentence); owner applies settings.json |
| ADJ-07 | The CLAUDE.md rewrite proposal is live but unapproved, and partly carried out (goal section, two deletions) through merges the owner made; five sentences in current CLAUDE.md contradict owner words or rulings | Proposal: OWNER-ONLY; contradictions: see ADJ-09 |
| ADJ-08 | Open owner questions checked: GAP-379's e120 part open; class-C rows rejected under delegation but not retired (owner mechanism); OD-67 answered as to method and moot; OD-77 resolved under delegation; OD-83 (SCI) added | OWNER-ONLY for the state changes; none blocks work |
| ADJ-09 | Twelve further proven conflicts and stale or hand-typed statements, mostly already scheduled under T-120 | Mixed; listed per sub-item |
| ADJ-10 | Facts with more than one home (rule 5 violations in prose) | DELEGABLE (pointers) except where doctrine |

---

## ADJ-01 — The axis layer: what retired it, and what in functional-taxonomy.md still binds

**Verdict.** The axis layer is retired by owner words in three rulings and executed in one schema act. functional-taxonomy.md was explicitly left unedited for an owner merge. Its axis register, the axis half of §3.3, §4's dispositions, §5's axis and item clauses, §6–§8 and §9.2–§9.8 are superseded or history; §0.5, §3.1, the diagnosis-optional and naming parts of §3.3, §5.5 (assisted and collective use) and §9.1 (Co-1 openness) are not touched by those rulings.

**What retired it (evidence).**
- Owner ruling R3, 2026-08-18, recorded under "standing decisions, do not relitigate": `workplan/2026-08-18-handoff-next-session.md:68` and `:89-92` — "R3 — "axes" is a bad coined term; use ICF codes directly … `axes` and `item_axis_links` are retired; `population_axis_map` is re-derived mechanically as population↔ICF."
- Owner ruling 2026-08-24, ledger: `references/project-standards.md:797-816` (find: `git grep -n -F "I don't want axis to be used" -- references/project-standards.md`) — RULE "Axis" is descriptive vocabulary, not a domain identifier; "**Ratified documents that use the old term are superseded by this ruling, not authorities against it**".
- Owner ruling 2026-09-13, ledger `:3398-3399` (find: `git grep -n -F "for ICF should never ever exist anywhere" -- references/project-standards.md`) — "'AX-' for ICF should never ever exist anywhere."
- Delegated ruling R35 (`workplan/pipeline-state-graph/RULINGS.md:248`: "Ruled retired; executed as one act … sentences in D-0170, D-0184, functional-taxonomy and the instrument that treat axes as live are stale"), adopted by the owner's delegation of 2026-10-14 (ledger heading "Owner delegation 2026-10-14 — the simplification plan's §4 items are resolved by the assistant", `:4425`).
- Execution: `scripts/migrations/109_drop_axes.sql` drops `access_need_axis_map`, `population_axis_map`, `axes`, `situations` and `slugs.serves_axes`; its header (`:13-15`): "the documents R35 declares stale (D-0170, D-0184, functional-taxonomy) are not edited here and stay an owner merge." Verified: none of those objects is in `sqlite_master` today.
- The population layer in §4 was replaced earlier still: ledger `:575` "RULE: Population-scheme ledger reconciliation — supersessions from DR-2026-07-23-population-schema-replace", which made the scheme a flat set and dropped the slash sub-codes §4 is built on (find: `git grep -n -F "Population-scheme ledger reconciliation" -- references/project-standards.md`).

**Part by part.**

| Part of functional-taxonomy.md | Status | Evidence |
|---|---|---|
| Header, `:3-10` ("Doctrine OPERATIVE; DB execution staged and gated per §9"; staged schema `working/taxonomy/staged_schema_functional_axes.sql`) | Stale; the staged file does not exist (`test -e` fails) | migration 109 |
| §0, §0.5 items 1–4, the owner adjudication `:109-115` ("something is better than nothing…") | Not touched by the retirement: the irreducibility principle and "never a portrait" read on any lens. §0.5(2) names `population_axis_map`, now dropped | owner words 2026-07-21 are quoted in the file |
| §0.5(5) "curated in the `situations` entity (§5.4)" | Superseded as to `situations` (dropped, migration 109); Co-1 testimony as the home of the remainder survives | migration 109 |
| `:38-41` "an ICF `b`-code anchor … never serves as a description of any person" | Amended: an identity (a group, not a person) may be tied to a b-code | "Owner answer 2026-11-21 (third)" ("1 yes b is seeing therefore ties into blind etc") |
| §1 representations table | History | — |
| §2 axis register, §2.2, §2.3 | Superseded | R3, 2026-08-24, 2026-09-13, migration 109 |
| §3.1 emergence guarantee | Survives (Co-1 never subordinated; mission commitment 3) | — |
| §3.2 mapping confidence | Axis half superseded; the confidence idea survives as `identity_icf_map.mapping_confidence` (column verified by `PRAGMA table_info`) | — |
| §3.3 diagnosis-optional, ICD-11 negative commitment, naming | Survive; reinforced by the medical-lens deletion ("Owner instruction 2026-11-16", `:7688`) | — |
| §3.3 "Work from axes — no armchair umbrellas" (`:252-271`) | Axis half superseded (CLAUDE.md §6 `:378`: "ICF/access-need frame with codes AND names, never bare axis codes, never population umbrellas"); anti-umbrella half survives as amended by the design-equivalence exception (ledger `:567`, 2026-07-23, "COM and BRAIN are ratified") and the advocacy-group lens ("Owner statement 2026-11-12 (fourteenth)", `:5927`) | — |
| §4 disposition table and admitted profiles | Superseded (flat scheme 2026-07-23; then identity rulings of 2026-11-12, sets seven to ten) | ledger `:575`, `:6111-6163` |
| §5.1 (c) item parameter, (d) situation; §5.2 attachment to axes, items, situations | Superseded as to axes, items and situations | migrations 107, 109 |
| §5.3 (already struck 2026-09-03) | History. Its annotation rests on DR-2026-08-24 §2.4, which the owner overruled on 2026-08-27 (ledger `:2040-2043`), and quotes "1 of 106" (`:333-334`), a hand-typed count of a column that no longer exists | migration 109 |
| §5.4 situations entity | Superseded (table dropped) | migration 109 |
| §5.5 assisted and collective use | Survives as doctrine; "every axis carries" no longer has a referent | — |
| §5.6 non-DOI intake | Not adjudicated against the research contract [UNVERIFIED: whether `governance/research-contract.yaml` R10 now governs this route was not checked] | — |
| §5.7 strength semantics | Superseded by the owner's circle table (OD-57, OD-59, OD-64; see ADJ-09a) | — |
| §5.8 coverage semantics (axis queries) | Superseded | — |
| §6, §7, §8 | History (codes, item codes A–K, STUB axes all gone) | — |
| §9.1 Co-1 openness, owner directive 2026-07-21 | Survives (owner words quoted at `:421-422`) | — |
| §9.2–§9.8 | Dead (staged DDL absent; `serves_axes` dropped; axis queries meaningless) | migration 109 |

**Proposed reconciliation (append, do not rewrite).** Insert immediately after line 10 of `governance/functional-taxonomy.md`:

> **⚠ SUPERSEDED IN PART 2026-11-26 — APPENDED, NOT EDITED.** The axis layer this document is built on is retired: owner rulings 2026-08-18 (R3, `workplan/2026-08-18-handoff-next-session.md`), 2026-08-24 and 2026-09-13 (`references/project-standards.md`: `git grep -n -F "I don't want axis to be used"` and `git grep -n -F "should never ever exist anywhere"`), executed by `scripts/migrations/109_drop_axes.sql` (axes, both axis maps, `situations`, `slugs.serves_axes`). The population codes of §4 were replaced on 2026-07-23 (`git grep -n -F "Population-scheme ledger reconciliation" -- references/project-standards.md`) and by later identity rulings. Read §2, the axis half of §3.3, §4, §5.1–§5.4, §5.7, §5.8, §6–§8 and §9.2–§9.8 as history. Not touched by those rulings: §0.5 (but `situations` no longer exists), §3.1, §3.3's diagnosis-optional and naming paragraphs, §5.5 and §9.1. The live frame is three lenses, identity, ICF and access need (CLAUDE.md §6). An identity may carry a body-function code ("Owner answer 2026-11-21 (third)").

Pair: correct CLAUDE.md §9 `:542`, which routes "Entity model, ICF frame" to this file and to conceptual-model.md (both stale): replace the row with `| ICF frame and the three lenses | CLAUDE.md §6; `python3 scripts/db.py icf-glossary`; `governance/functional-taxonomy.md` (history, see its 2026-11-26 note) |`.

**Approval.** ALREADY-SETTLED-BY-OWNER-WORDS for the supersession; the annotation lands in a doctrine file left for an owner merge by R35 and migration 109, so the owner merges it. [CONFIDENCE: high — every ruling and the migration were read; the survivor list is my reading and is phrased as "not touched", not as a re-ratification.]

---

## ADJ-02 — conceptual-model.md: the item layer is dead there

**Verdict.** ENT-08 Item, the relationship map routed through Item, the `item_code` and `populations` encodings, and the schema/converter inventory are dead. The rest is A3-phase history. One header note suffices.

**Evidence.**
- `governance/conceptual-model.md:25` "ENT-08 | **Item** | — | — | ~90 | DEFERRED to A6"; `:71` "Item (ENT-08) ◄──── Conflict (ENT-09)"; `:81` "Connection (ENT-04) ──── links ──── Item × Item"; `:92` "The `item_code` field on Specification already encodes this. Item is the Part 4 organizing unit."; `:100` "The `populations` array on Specification encodes this."
- `scripts/migrations/107_drop_item_layer_cluster.sql:2-6`: "the item layer is dropped from the schema (plan step 1.2; RULINGS R36). THE OWNER'S REASON. The item layer was deleted from the database on 2026-09-01 because a container named for its answer … biases every finding". Owner words: *"if E-08 already exists then the work is predisposed to filing into a container that already exists, and that biases every finding"* (`_archived/references/README.md:22-23`, CLAUDE.md §7). The cited commit `befaa29` is not reachable in this shallow clone [UNVERIFIED as a commit; the quote is in two repository records].
- `specifications` has no `item_code` or `population_code` column (`PRAGMA table_info(specifications)` read); CLAUDE.md §6 `:397` (migration 071).
- `:35` "ENT-11 | **Population** | DONE (enum)": `PopulationCode` was retired (R44, adopted by the 2026-10-14 delegation); the lens ruling of 2026-08-28 replaced population keys with three lens columns.
- `:18-24` schema files `specification.py`, `bpc_metadata.py`, `connection.py`, `slug.py`, `gap.py` exist nowhere (`git ls-files` finds none); the converters are under `_archived/scripts/convert/`.
- `:26` ENT-09 Conflict "DEFERRED to A6": `conflicts` exists and is keyed on a parameter (CLAUDE.md §7: migration 121; `add-conflict --parameter-id`).
- Note: the same 2026-11-06 owner statement (ledger `:5005`) admits the 93 old item *subjects*, value-stripped, as candidate names — never as containers. That does not revive ENT-08.

**Proposed reconciliation.** Insert after line 4 of `governance/conceptual-model.md`:

> **⚠ SUPERSEDED IN PART 2026-11-26 — APPENDED, NOT EDITED.** The item layer is deleted (owner, 2026-09-01; `scripts/migrations/107_drop_item_layer_cluster.sql`): ENT-08, every relationship through it in §2, and §2.1's `item_code` sentence are history; determinations are keyed on a parameter and three lens columns (CLAUDE.md §6). ENT-11's enum is retired and the `populations` array is gone (migration 071). The schema and converter files of §1.1 no longer exist (the converters are under `_archived/scripts/convert/`), and §1.1's record counts are of 2026-04-26. Treat this document as the A3 sign-off record, not as the live entity model; the live model is `sqlite_master` (CLAUDE.md §4).

Plus the CLAUDE.md §9 `:542` row change in ADJ-01.

**Approval.** ALREADY-SETTLED-BY-OWNER-WORDS (owner deletion, executed). [CONFIDENCE: high.]

---

## ADJ-03 — Mission and "population": consistent, with one owner question

**(a) Verdict: no conflict.** Mission uses "population" for groups of disabled people and for the design scale, never for the retired `population_code` key. The owner still uses the word that way: "populations still get coded" ("Owner statement 2026-11-14 (sixteenth set, last)", `:7536`), "disability identities/populations" (2026-11-22, `:8405`). The lens ruling governs determinations' keys (CLAUDE.md §6 `:386-391`); mission says nothing about keys.

Evidence: `governance/mission-and-epistemics.md:40` "Population codes are organizing scaffolding, not a description of any individual within the population" — a caution that holds for identity codes; `:62` Person Mode ("that population neither bounds nor defines the person"); `:78` "Population-level specifications … are necessary but insufficient". No mention of the medical lens, items or axes in a live sense (the "two orthogonal axes of coverage" at `:101-103` is ordinary English, which the 2026-08-24 RULE keeps free: "Axis is a term that we should be able to use freely").

Reconciliation: **no change.** [CONFIDENCE: high.]

**(b) One tension, for the owner.** `mission-and-epistemics.md:61` "Population Mode | Population-Informed Inclusive Design | Ranges; median as default" (repeated at `governance/evidence-architecture.md:55` and ledger `:14`). Owner words 2026-11-14: "we just have minimum, mode, median, maximum" (`:6796`) and best = "most accommodating" (U1 in "Unification 2026-11-14", `:7864`). The unification entry supersedes the ledger's "median as default" only "[ASSUMPTION … as to the median as the default figure]" (`:7958`), an unratified recorder reading. Mission is doctrine (decision-protocol §2.4 item 1).

Plain question: *Population Mode's table says "median as default". Since 2026-11-14 you have said the guidebook shows four figures (minimum, mode, median, maximum) and showcases the most accommodating value. Is the median still the default value shown for Population Mode?*
- **No** (the median is one of four figures; the showcased value is the most accommodating): one appended note on mission `:61` and evidence-architecture `:55` pointing at the unification entry. Cost: one sentence each.
- **Yes**: the selection rule of T-059 (most accommodating) and the mission disagree on what is shown first; T-059 would need a rule for when the median is shown over the best. Cost: a design change in T-059.

**Approval.** OWNER-ONLY (mission). [CONFIDENCE: medium — whether "median as default" was ever a render rule or a description of ranges is not settled by the record.]

---

## ADJ-04 — The authority order

**Verdict.** The working order is set by owner words (rule 0 and the delegation grants), but no text states all of it. The DR states its own supremacy in terms the owner's later practice has overtaken; CLAUDE.md states the owner-over-DR-over-CLAUDE.md part correctly and nothing below it; decision-protocol.md states none of it and does not mention delegated resolutions.

**Evidence of the wrong or missing statements.**
- DR `:3` "**THIS DOCUMENT SUPERSEDES ALL OTHER PLANNING DOCUMENTS IN THIS REPOSITORY.**"; `:17-25` "Two documents remain live alongside this one … Everything else is superseded."; `:563` "A fresh session reads exactly four."; `:578` "**No fifth document may join this set.**"; `:48` the 2026-08-22 master plan is "**OPERATIVE** — the live execution document".
- Against it: DR `:636-641` (its own §11 property 3) is "SPENT … A successor plan is no longer build-rejected"; the owner names a different live plan: "i just want to get this remediation plan done asap" (2026-11-25, `:8483`, read as `workplan/2026-11-12-bidirectional-pipeline/REMEDIATION-WORKPLAN.md` at `:8491`); and "fold the term-resolution plan into the remediation plan … this newest plan having priority in conflicts" (2026-11-14, `:7243`).
- DR `:323-329` still reads "**← THIS IS THE NEXT ACT**" for OD-A…OD-G of 2026-08-22, and `:89-92` "The remaining owner decisions OD-2 through OD-12 are **still open**" although OD-10 is signed (`:593`, `:601`) and OD-2 was partly ruled on 2026-09-28 (ledger `:4284-4300`).
- CLAUDE.md `:20-23` (correct as far as it goes): "Where it disagrees with [the DR], that instrument wins … unless a live owner ruling has superseded the instrument itself, per rule 0". CLAUDE.md `:538` routes "What to do now" to the DR, contradicting its own rule 7 ("Derive every volatile fact — … the active plan — from the live repo").
- Delegated resolutions have a rank only in ledger ACTION lines ("Owner statements 2026-11-25", `:8496`; OD-79, `:8503`; "(sixth)", `:8562`). decision-protocol.md §2 knows DG-NON/DG-REVIEW/DG-AUTO only.
- Recorder readings marked [ASSUMPTION] are, by every entry's own ACTION, "unratified except where the owner's words state them" — a rank no governing document records.

**The order, as the record supports it (highest first).**
1. The owner's own words, live or quoted verbatim in a ledger entry; a later statement supersedes every earlier record it touches (rule 0). A recorder's [ASSUMPTION] reading is not the owner's words.
2. Owner answers and ratifications (`ANSWERED BY THE OWNER`; "Ratify all", 2026-11-19), and the merge of a pull request whose body names a change as the owner's to approve by merging.
3. Delegated resolutions (`RESOLVED UNDER DELEGATION` with a `confirmed` check), within the grant's recorded reach (OD-79, widened for the named questions by "Owner statements 2026-11-25 (sixth)"); never a row the schema binds to an "Owner" entry; reversed by any later owner word.
4. Ratified records — decision records, ledger RULEs, canonical governance documents — as amended by their appended supersession notes; between two, the one ratified later on the point wins. DR-2026-08-19 sits here: it outranks CLAUDE.md and planning documents, not later rulings or later DRs that amend it.
5. CLAUDE.md, the process map; each rule carries the authority of the owner words it quotes, not of the file.
6. Plans and task files; the active plan is the one the newest ledger ACTION lines name.
7. Frozen records (sessions, transcripts, `_archived/`, superseded workplans): evidence of what was ruled when; they bind nothing by themselves.

**Proposed reconciliation (smallest set).**
1. CLAUDE.md: replace `:20-23`'s sentence with — "Authority runs: the owner's words (rule 0; a recorder's [ASSUMPTION] reading is not one) > owner answers and ratifications > delegated resolutions within their recorded reach > ratified records, the later on a point winning (`decisions/DR-2026-08-19-…` outranks this file and every plan) > this file > plans > frozen records." (One sentence; replaces one; adds no rule.)
2. CLAUDE.md `:538`: replace the row with `| What to do now | the ACTION lines of the newest entries at the tail of `references/project-standards.md`, and the plan they name |`.
3. DR: append after `:25` (append, attestation required) — "**⚠ SUPERSEDED IN PART 2026-11-26 — APPENDED, NOT EDITED.** The four-document read-set (§8), "Everything else is superseded" (§A) and §B's "OPERATIVE" rows are spent: §11 property 3 already says so, and the owner has since named the remediation plan as the work (`references/project-standards.md`, "Owner statements 2026-11-25"). §3 step 4a is not the next act; OD-10 is signed and OD-2 is partly ruled (2026-09-28). This DR's OD-1 to OD-12 are a separate numbering from the remediation register's OD-01 onward (both have an OD-10 and an OD-11); cite these as "DR-2026-08-19 OD-n". What still binds here: §1.4 (items as leads), §7 (adversarial review on data), the write-path discipline of §12.0 as amended, and §4's acceptance criterion."
4. decision-protocol.md: no new section. Append one line under §2.1: "Delegated resolutions and their statuses are recorded in the ledger (convention of 2026-11-12; grants of 2026-11-13, 2026-11-19 and 2026-11-25; reach: OD-79). They never reach §2.4 except where the owner's words name the question."

**Approval.** The order restates owner words: ALREADY-SETTLED-BY-OWNER-WORDS as to content; the wording in CLAUDE.md, the DR note and the decision-protocol pointer are DELEGABLE (D-OP). Rule 0's own text is not touched. [CONFIDENCE: high for the evidence; medium for the exact placing of rank 4 versus canonical doctrine, because mission doctrine is DG-NON and a later DR cannot change it without the owner — the sentence "the later on a point winning" assumes the later record was itself owner-ratified.]

---

## ADJ-05 — Rule 10 versus "one big pull request"

**Verdict.** The suspension covered exactly one pull request, PR 243, which merged on 2026-11-20. It has expired. Rule 10 stands for all other work, and later owner-era records apply it.

**Evidence.**
- Ledger `:8223` "no, just do a big pull request so i don't have to waste time"; reading `:8231` "[ASSUMPTION: the owner's words supersede, for this one pull request and on contact (rule 0), the separation … the rule stands for every other pull request …]"; ACTION `:8235` "(1) Ship that work as one pull request, with the matrix excluded".
- That pull request is PR 243: it carries the commits recording these statements (`9fa3307`, `74e6458`) and the work they name (translations, verification, the CLAUDE.md goal edit), and merged as `4f12d50` on 2026-11-20 (`git log origin/main --merges`).
- Rule 10 was left intact by the 2026-11-15 stacking instruction (`:7584` "Whether CLAUDE.md rule 10 … is relaxed: it is not") and is applied after PR 243 by the delegated resolutions of 2026-11-23 (`:8468` "tooling-only pull request (rule 10), with no rows") and the owner's ratification of 2026-11-19 (`:8035` ACTION (2) "ship research separately (rule 10)").

**Reconciliation.** No change. Do not add the exception to CLAUDE.md (it would be narrative, which `:25-27` forbids).

**Approval.** ALREADY-SETTLED-BY-OWNER-WORDS. [CONFIDENCE: high. The scope reading is marked [ASSUMPTION] in the ledger; the owner's merge of PR 243 ratifies its shape in fact.]

---

## ADJ-06 — Rule 9 versus a default-subscribe instruction

**Verdict.** Rule 9 governs: it is the user's own instruction, and CLAUDE.md is loaded as instructions that "OVERRIDE any default behavior" (the harness reminder that injects it). One sentence of rule 9 is stale, and the deny entries it relies on may not match the tool names exposed in cloud sessions.

**Evidence.**
- CLAUDE.md `:196-212`. `:208-211`: "→ **PARTLY ENFORCED** once the owner adds both `subscribe_pr_activity` tools, `send_later` and `create_trigger` to `permissions.deny` in `.claude/settings.json`". The owner has added them: `.claude/settings.json:43-46` lists `mcp__github__subscribe_pr_activity`, `mcp__Claude_Code_Remote__subscribe_pr_activity`, `mcp__Claude_Code_Remote__send_later`, `mcp__Claude_Code_Remote__create_trigger`.
- In this session the same tools are named `mcp__claude-code-remote__subscribe_pr_activity`, `mcp__claude-code-remote__send_later` and `mcp__claude-code-remote__create_trigger` (lower case, hyphenated). If the deny list matches names exactly, these entries do not cover them. [UNVERIFIED: whether permission matching normalises server names; whether other surfaces expose the `Claude_Code_Remote` spelling.]
- The harness text the rule calls "default-subscribe" is not visible to this subagent; this session's `subscribe_pr_activity` description says only "Use this when asked to autofix, monitor, watch, or babysit a PR". [UNVERIFIED: the main session's wording.] The owner's words of 2026-09-23 that rule 9 cites are not in the ledger (`git grep -n -i subscri -- references/project-standards.md` finds nothing) [UNVERIFIED as verbatim words; the rule's text is the record].

**Proposed reconciliation.**
1. CLAUDE.md `:208-211`, replace the enforcement sentence with: "→ **PARTLY ENFORCED** by `permissions.deny` in `.claude/settings.json`, which stops explicit subscription and polling only if its names match the tools the session exposes (check the session's tool list); it does not stop the subscription PR creation makes, so the unsubscribe step is yours. Never deny `unsubscribe_pr_activity`."
2. Owner, in `.claude/settings.json` (harness configuration; an agent cannot apply it): add `mcp__claude-code-remote__subscribe_pr_activity`, `mcp__claude-code-remote__send_later`, `mcp__claude-code-remote__create_trigger` beside the existing entries.

**Approval.** Rule 9's operative text unchanged. Sentence 1: DELEGABLE. Settings: owner applies. [CONFIDENCE: high that rule 9 governs; medium on the name mismatch's effect.]

---

## ADJ-07 — The CLAUDE.md rewrite proposal of 2026-11-20 (third)

**Verdict.** Live but unapproved, and partly carried out through merges the owner made. Not dead and not superseded: the owner's 2026-11-25 words ("Remember that this project is simple!!!"; "build as little machinery as possible") support its aim without approving its content. Its ACTION still binds: no move of rules 0, 1, 4, 5, 6, 9, 10, §3, §7, §8 to a working-rules file until the owner approves.

**Evidence.**
- Ledger `:8196` "**This is a proposal. The owner has not approved it**"; ACTION `:8214` "(1) Do not rewrite `CLAUDE.md` until the owner approves the content above".
- Carried out: commit `94dbaed` (goal section; Layer-0 preamble deleted; `stage_label()` clause deleted; "Proposed wording: the owner approves it by merging"; "No rule or section is renumbered or moved") merged in PR 243; commit `53ada81` (the "simple project" sentence, from "Owner statement 2026-11-25 (seventh)", `:8571`) merged in PR 246. Both are ancestors of `origin/main`.
- Not carried out: the working-rules file, deletion of rule 7, the "Proof" narratives, the six-verb list, the size target (`:8207`).

**Contradictions of owner words or rulings in current CLAUDE.md** (each proven in ADJ-09 or above): §6 `:381-382` "Only Opus-class models write `best_practice_synthesis`" (ADJ-09b); §6 `:372` the ○ gloss (ADJ-09a); §9 `:538` and `:542` routes (ADJ-04, ADJ-01); rule 9 `:208` (ADJ-06); §8 `:501-503` sign-off list narrower than decision-protocol §2.4 (ADJ-09i). None is fixed by the rewrite proposal as recorded; each is a one-sentence change.

**Reconciliation.** Proposal: no action until the owner says yes or no. Plain question: *The rewrite recorded on 2026-11-20 would move most rules out of CLAUDE.md into a working-rules file and cut CLAUDE.md to a quarter of its size. Approve, reject, or leave it?* Approve: one tooling PR, with the rule-number sweep of script comments the audit names (`:8207`). Reject: delete the proposal's ACTION by a later ledger line. Leave: no cost; the five one-sentence fixes above go ahead regardless.

**Approval.** OWNER-ONLY for the proposal (the ledger reserves it). [CONFIDENCE: high.]

---

## ADJ-08 — Open owner questions, verified against the end of the ledger and the database

The owner wrote on 2026-11-25: "I don't want to answer these right now so just make it happen" (`:8549`), and ACTION (sixth) says the questions are not to be put again before the work goes on. The items below are therefore stated for the owner's convenience. None blocks the plan. Only the ones whose effect needs a mechanism the schema binds to an "Owner" entry (`stated`, retirement) need the owner's words at all.

**ADJ-08a — GAP-379, the `e120` row on LPA, TALL and BAR. Still open.**
Evidence: `gaps` row GAP-379 status `OPEN` (read live). OD-85 (`:8592`): "the `e120` and A-SIZE question for LPA, TALL and BAR (GAP-379's other open part) stays open." The gap's own last correction says the opposite ("answered by keeping the rows … the coordinator's reading, to be confirmed at review") — the gap text and the ledger disagree; the ledger is later and governs. Rows (derive: `select triple_id, identity_code, icf_code, state from identity_need_icf where need_code='A-SIZE' and icf_code='e120'`) are `pending`. `access_need_icf` lists e120 for A-SIZE; `base_icf` titles e120 "mobility products & technology" (title source `access_need_icf.note`, not WHO).
Plain question: *The access need "fit the range of bodies" (A-SIZE) lists the ICF code for mobility products and technology. Should little people, tall people and fat people each count that code as part of their ICF coverage?*
- Yes: three reviews to `stated` citing your entry. Cost: three writer calls.
- No: three retirements citing your entry. Cost: three writer calls; each identity keeps its other A-SIZE codes, so none becomes uncovered (derive: `select identity_code, icf_code from identity_need_icf where need_code='A-SIZE' and retired_at is null`).
- Leave: no cost; nothing reads `identity_need_icf` for a gather, determination or gate (D-0184; OD-85); GAP-379 stays open.
Approval: OWNER-ONLY (a group's need is §2.4 item 2; `stated` and retirement are bound to an Owner entry). [CONFIDENCE: high.]

**ADJ-08b — The two class-C pairs. Rejected under delegation; not retired.**
Evidence: OD-85 (`:8592`): "Class C, BRAIN with A-NOSPEECH and COM with A-LOWLOAD … rejected, under delegation, **with no row changing state**". Rows live and `pending` (derive: `select triple_id, identity_code, need_code, icf_code, state from identity_need_icf where (identity_code,need_code) in (values ('BRAIN','A-NOSPEECH'),('COM','A-LOWLOAD')) and retired_at is null`); each warrant reads "No record read stated this link". Registry text, read live: A-NOSPEECH absorbs "aphasia, dysarthria, stammering, non-speaking people, AAC users…"; A-LOWLOAD absorbs "ADHD, dementia, brain injury, brain fog, intellectual disability…"; BRAIN's description "Incl. post-concussion, stroke, TBI"; COM's "dysautonomia, long COVID, MCAS, ME/CFS, POTS".
Plain question: *Two pairings were proposed with no source behind them: people with acquired brain injury with "never require speech", and people with complex conditions with "keep memory demand low". Retire them, or keep them for review?*
- Retire: one retirement per row citing your entry; matches your rejection of TRIPLE-65 on the same ground. Cost: the row count printed by the query above.
- Keep pending: no cost to the pipeline; T-127 does not propose them (OD-85).
- Accept: needs a recorded basis first (2026-11-21 (third) ACTION (2) by analogy).
Approval: OWNER-ONLY. [CONFIDENCE: high.]

**ADJ-08c — OD-67. Answered as to method; the list has never been put; moot while T-128 is withdrawn.**
Evidence: "OD-67: yes, one answer on the full list, VES withheld" / "OD-67 STATUS: ANSWERED BY THE OWNER" (`:8012-8013`). OD-87 (`:8600`): "OD-67 is not resolved here … and is moot while T-128 is withdrawn; if T-128 is reinstated its list is owed again." The plan's own record claimed T-128 was "HELD on OD-67 though OD-67's gate is open (the confirmation of its list is still owed)" (`:8535`).
Plain question (only if T-128 returns): *Confirm T-128's full list of identity-to-ICF rows in one answer.* Cost now: none.
Approval: OWNER-ONLY when it arises. [CONFIDENCE: high.]

**ADJ-08d — OD-77, which mapping the owner doubted. Resolved under delegation.**
Evidence: OD-77 (`:8596`): "The table `identity_icf_map` is taken as the mapping meant, as a delegated reading that rests on the range codes"; check confirmed. OD-79 (`:8503`) had said the grant does not reach "what the owner meant by the owner's own words"; the owner's sixth statement named "which mapping" among the questions handed over (reading `:8555-8556`, itself [ASSUMPTION]).
Plain question: *When you wrote "I don't think the mapping is correct" on 2026-11-22, did you mean (A) the list tying each identity to ICF activity codes, which holds ranges such as b750–b789, or (B) the identity–need–ICF rows of PR 245?*
- A (the delegated reading): no change; additions to `identity_icf_map` stay frozen; T-102 writes only your OI-03 crossings.
- B: the hold moves to `identity_need_icf`; its rows would need your review, and retirements need your entry. Cost: a review pass.
Approval: OWNER-ONLY to confirm the meaning (owner meaning); the delegated reading stands meanwhile. [CONFIDENCE: medium — the reading is reasonable but by the ledger's own rule it is not the owner's words.]

**ADJ-08e (added) — OD-83, SCI retires into WHEEL. Resolved under delegation; one-way.**
Evidence: OD-83 (`:8608`) rests on the owner's "SCI is the same as WHEELCHAIR basically" (2026-11-12, seventh set) and "only SCI is the same as WHEEL" (eighth-set heading); "The retirement is one-way through the sanctioned verbs". The correction of 2026-11-16 (`:7713-7727`) had put it to the owner as OI-77 because the earlier acceptance rested on the medical lens. GAP-111 is `OPEN`; SCI is `active` and WHEEL does not exist in `base_taxonomy_identity` (read live). Population codes are §2.4 item 2.
Smallest course: no question now. The owner's merge of T-102's pull request, whose body names the retirement, is the confirmation (rank 2 of ADJ-04). Cost of a wrong guess: a compensating migration.
Approval: OWNER-ONLY in substance; satisfied by merge. [CONFIDENCE: medium.]

---

## ADJ-09 — Other proven conflicts, stale statements and hand-typed figures

**ADJ-09a — The owner's circle table is answered but not applied in five homes.**
Owner: "OD-57: yes" (`:7327`) to applying "● T1, T2, Co-1, Co-2; ◐ T3, T4; ○ T5, T6; ⚠ in place of the circle for a grey, unverified or thin basis … and replacing the ○ gloss in `CLAUDE.md` §6" (`:7265`); "T4 only half circle" (`:7195`); "OD-64: triangle for every grey basis" (`:7424`).
Stale: `governance/tier-system.md:64-66` (§5: T3 clinical ●, T5 ◐, T3 grey and unverified ○); `:90-94` (§8 band table); `:98` ("T3-clinical alone is full band … T3-grey alone is weak band"); `:100` ("a cell whose entire basis is T4–T6 takes ○ even where T4/T5 sources are present"); `:113` (firm guidance "T3-grey (○ weak)"); `governance/evidence-architecture.md:82` ("any `regulatory_stratum_only` cell renders at ○ weak even where T4/T5 sources are present"); `governance/mission-and-epistemics.md:136` ("○ (grey, thin, or unverified …)"); CLAUDE.md `:372`; `schemas/tier_derivation.py:102-114` (`band()`).
Reconciliation: no new text. T-120 item 2a (doctrine, CLAUDE.md) and T-117 (code) already carry exactly this (`workplan/2026-11-12-bidirectional-pipeline/tasks/T-120-doctrine-amendments-and-deletions.md` §4 item 2a). Recommend running T-120. Interim, if T-120 waits: one line under tier-system §5's heading — "Amended by the owner 2026-11-14 (OD-57, OD-64; ledger "Unification 2026-11-14", U7): the table below is stale until T-120 lands." Approval: ALREADY-SETTLED-BY-OWNER-WORDS. [CONFIDENCE: high.]

**ADJ-09b — "Only Opus-class models write `best_practice_synthesis`" contradicts the owner and names a dead table.**
CLAUDE.md `:381-382`. Owner directive 2026-07-25: "best_practice_synthesis can be fable as well" (ledger `:609`); decision-protocol `:150` "`fable` is a synthesis-capable tier alongside `opus`". No object named `best_practice_synthesis` exists in `sqlite_master`. T-120 item 3 renames the table only, leaving "Only Opus-class".
Reconciliation: replace with "Only a synthesis-capable class (`opus` or `fable`, decision-protocol §4.2) writes a determination (`specifications`)." Approval: ALREADY-SETTLED-BY-OWNER-WORDS. [CONFIDENCE: high.]

**ADJ-09c — Best practice and Universal Mode in doctrine versus the owner's 2026-11-14 definitions and OD-48.**
`mission-and-epistemics.md:42-46` (commitment 2: "Best practice is graded by the evidence hierarchy — code consensus anchors it only at the weak band") and `:177` (test 3: "treating code consensus as the weak (○) band") against U1 ("best practice IS the same as ideal IS the same as most accommodating") and U2 ("convergence is not evidence of best practice but most common practice"), "Unification 2026-11-14" `:7864`. T-120 item 1 names mission commitment 2 as the home; test 3 is not named there [UNVERIFIED that T-120 reaches it — read only its §4 items 1–6].
`evidence-architecture.md:121` "A determination whose entire basis is the regulatory stratum … is a **Universal-Mode regulatory determination**" against OD-48, answered by the owner 2026-11-19: "whom it is for" (`:7995`), whose adjudicated sense is that "rests on codes" is read from `regulatory_stratum_only`, not from `design_scale` (`workplan/2026-11-12-bidirectional-pipeline/OPEN-DECISIONS-ADJUDICATION-3.md:136`). Mission commitment 5 (`:66-68`, "Universal design is co-extensive with code compliance") is in tension with the same answer.
Reconciliation: let T-120 carry commitment 2, test 3 and evidence-architecture `:121`, with a pointer to OD-48. Ask the owner only about commitment 5: *Does "Universal design is co-extensive with code compliance" still hold now that "universal" means whom a value is for?* Approval: ALREADY-SETTLED for commitment 2 and `:121`; OWNER-ONLY for commitment 5. [CONFIDENCE: medium.]

**ADJ-09d — decision-protocol pins model versions against its own rule.**
`governance/decision-protocol.md:5` "Sonnet 4.6 conversational; Opus 4.6 best-practice synthesis … (Opus 4.6 primary)" against `:144-149` "Any version number encountered in model-routing text is stripped on touch (owner directive 2026-07-25)". Reconciliation: delete the four version numbers. Approval: ALREADY-SETTLED-BY-OWNER-WORDS. [CONFIDENCE: high.]

**ADJ-09e — Broken pointers.**
`mission-and-epistemics.md:126` and `:165` cite `workplan/workplan-co0007-v3-amendments.md`; `decision-protocol.md:5` and `:126` cite `workplan/workplan-co0007-v3.md`. Both now live only under `workplan/_superseded/` (`git ls-files`), which `.ignore` hides. `functional-taxonomy.md:9` cites a staged schema that does not exist. Reconciliation: correct the four paths (pointer fix); the fifth is covered by ADJ-01's note. Approval: DELEGABLE. [CONFIDENCE: high.]

**ADJ-09f — Hand-typed figures (rule 7a).**
- `evidence-architecture.md:92` "only 27 of 640 sources carry any `evidence_population_match` row" — a pre-reset figure.
- `evidence-architecture.md:131` "With `source_value_extractions` empty" — contradicts `:112` of the same file, which says the table "holds neither 0 nor any number this sentence may state".
- `evidence-architecture.md:155` "both live rows are `pending`, and one is retired-and-superseded" and "sixteen tests … eight fault injections" — the paragraph above (`:153`) says the count grew several-fold.
- `functional-taxonomy.md:333-334` "populated on 1 of 106 rows" (column dropped).
- `conceptual-model.md:18-29` record counts (dated 2026-04-26; covered by ADJ-02's note).
- DR `:305` "`slugs` 106, `term_aliases` 2,382, `axes`/`access_needs` and their 232 mapping rows" (DR is a dated record; covered by ADJ-04's note).
Reconciliation: delete the counts at `:92`, `:131` (the clause), `:155`, replacing each with the derivation command or nothing; they are dated narrative in a canonical index. Approval: DELEGABLE. [CONFIDENCE: high.]

**ADJ-09g — The DR's internal staleness and the OD-number collision.** Covered by ADJ-04 item 3. Evidence of the collision: DR `:593` "OD-10 | The close-out DR of §10" and `:594` "OD-11 | G6/I-45 — the Universal/Population doctrine tension"; ledger `:5971` "Owner answers 2026-11-12 (second set) — OD-28, OD-10 …" and `:5520` "Delegated resolution 2026-11-12 — OD-11 which stage owns the gap register". Approval: DELEGABLE. [CONFIDENCE: high.]

**ADJ-09h — Mission's evidence-type vocabulary is out of date.**
`mission-and-epistemics.md:99` names `standard_evidence_based`, `national_framework` and omits `grey`; the vocabulary home (`schemas/enums.py:112-120`, `EvidenceType`) holds `standard_eb`, `national_fw`, `grey`, `unknown`. Reconciliation: replace the list with a pointer — "per `schemas/enums.py` `EvidenceType`". Approval: DELEGABLE (schema vocabulary, not doctrine). [CONFIDENCE: high.]

**ADJ-09i — CLAUDE.md §8's owner-sign-off list is narrower than decision-protocol §2.4.**
CLAUDE.md `:501-503` lists "mission, audience, CRPD posture, population taxonomy, evidence-tier definitions, jurisdiction, licensing, trajectory"; decision-protocol `:73-84` also reserves major work-products (item 5), the Co-1 source corpus (item 6), adversarial-use catalogue retirement (item 9) and counsel-review queue resolution (item 10). Reconciliation: replace CLAUDE.md's list with a pointer: "Owner sign-off is required for content and doctrine only — the list in `governance/decision-protocol.md` §2.4. Code is not." Approval: DELEGABLE. [CONFIDENCE: high.]

**ADJ-09j — CLAUDE.md §6 misstates T3.** `:369` "**T3** grey primary"; tier-system `:19`: T3 is "Clinical primary research at lower control level … plus grey-literature primary research". Reconciliation: "**T3** lower-control primary (clinical or grey)" — or let T-120 carry it with ADJ-09a. Approval: DELEGABLE. [CONFIDENCE: high.]

**ADJ-09k — "Highest-numbered" PI file is ambiguous.** CLAUDE.md `:467`. `ls governance/project-instructions-v*.md | tail -1` prints `v10_9` (lexical); numerically the highest is `v10_14`. Reconciliation: append "(derive: `ls governance/project-instructions-v*.md | sort -V | tail -1`)". Approval: DELEGABLE. [CONFIDENCE: high.]

**ADJ-09l — The `decisions` table is a frozen second home no governing document names.** Its newest row is D-0188 of 2026-09-11 (derive: `select max(decision_id), max(decision_date) from decisions`), and rows such as D-0170 stay `ACTIVE` although superseded in part (medical lens, "Owner instruction 2026-11-16"). R30 (`workplan/pipeline-state-graph/RULINGS.md:72`): "table frozen as infrastructure residual; ledger the single home". decision-protocol `:11` names the ledger and `decisions/` but not the table. Reconciliation: append to decision-protocol §0: "The `decisions` table is frozen (R30); its `status` column is not maintained; the ledger is the single home of decisions." Deleting the table is the cleaner end-state but is a schema act needing a caller sweep (rule 4). Approval: DELEGABLE. [CONFIDENCE: medium.]

**Looked for, nothing found.**
- [NULL: tier-system.md, decision-protocol.md — examined for axes, items and the medical lens presented as live; nothing found.]
- [NULL: mission-and-epistemics.md — examined for the medical lens or items as live; nothing found. "Axes" there is ordinary English, which the 2026-08-24 RULE keeps free.]
- [NULL: evidence-architecture.md — examined for the medical lens and four lens columns; nothing found (it reads three lens columns at `:116`).]
- [NULL: CLAUDE.md — examined for the medical lens as live; nothing found (`:388` records its deletion).]

---

## ADJ-10 — Facts with more than one home (rule 5 in prose)

Scope (owner, 2026-11-26: "it IS conflict reconciliation"): this table lists only duplicates that caused or carry a conflict found above, as the standard each reconciliation is judged by. It proposes no reorganisation beyond the moves already in ADJ-01 to ADJ-09; where the copies agree today, the move is "no change".

| Fact | Homes found | Move |
|---|---|---|
| The marker table | tier-system §5 and §8; evidence-architecture `:82`, `:121`; mission `:136`; CLAUDE.md `:372`; `band()`; the evidence-auditor skill (T-120 lists it) | T-120 makes tier-system §5 the one home; the rest point to it |
| The tier ladder | tier-system §1; mission evidence hierarchy `:86-97`; evidence-architecture §2; CLAUDE.md `:367-370` | Conflict only in CLAUDE.md's T3 gloss (ADJ-09j) and mission's type list (ADJ-09h); fix those; otherwise no change |
| The Design Modes table | mission `:56-62`; evidence-architecture `:50-56`; ledger `:14` | evidence-architecture already "restates with citation" (`:249`); no move beyond ADJ-03(b) |
| The authority statement | DR `:3`, `:17-25`, `:563-578`; CLAUDE.md `:20-23` and rule 0 | ADJ-04: one sentence in CLAUDE.md, the DR note points to it |
| The owner-only decision list | decision-protocol §2.4; CLAUDE.md §8 `:501-503`; OD-79 | ADJ-09i: CLAUDE.md points to §2.4 |
| Decisions | the ledger; `decisions/`; the frozen `decisions` table | ADJ-09l |
| Open owner questions | ledger status lines; `gaps` rows (GAP-379's text disagrees with OD-85); remediation-plan register; OPEN-ITEMS-PLAN | the ledger status line governs; a gap whose text conflicts with a later ledger line should carry a pointer to it, not its own answer |
| "What to do now" | DR §3; DR §B; CLAUDE.md `:538`; the remediation plan | ADJ-04 item 2 |

---

## Not reached, or not verified

- The verbatim owner words of 2026-09-23 behind rule 9 (not in the ledger; transcripts not searched in full).
- The harness's default-subscribe wording in the main session (ADJ-06).
- Whether functional-taxonomy §5.6 (non-DOI intake) is superseded by the research contract.
- Whether T-120 reaches mission test 3 (`:177`) and tier-system §10.
- `governance/population-taxonomy.md`, `governance/evidence-methodology.md`, `governance/armature_v4.md`: cited by the nine documents but outside the brief; they likely carry the same axis, item and marker staleness and were not read.
- DR §12.0 to §12.5 were read, not adjudicated line by line; §12.1 is already marked superseded (2026-09-10).
- The owner's merge of PR 243 and PR 246 is treated as approval of the CLAUDE.md goal edits on the commit messages' own terms ("the owner approves it by merging"); no separate owner statement says so.
