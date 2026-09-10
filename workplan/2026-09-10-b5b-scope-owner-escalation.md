# B5(b) — `evidence_sources.scope`: what is escalated to the owner, and why

**Written 2026-09-10.** Every figure below was measured on that date against
`data/guidebook.db` at sha256 `1101acd0d225da28e642988d477781d48ede4795ab73d242e1bd2a0a2e368f29`,
`PRAGMA user_version 73` — the state *before* this note's own compensating migration
(`scripts/migrations/data_20260910080002_2026-09-10-project-status-overview.sql`) wrote the four
`notes` records described below and moved the sha. **These are dated measurements, not standing
facts** — re-derive before relying on any of them (CLAUDE.md rule 7). Reproduce with
`python3 scripts/audit/adjudication_integrity.py` and the queries named in each section.

**What happened.** All nine `evidence_sources` rows carried `scope = NULL`, so
`schemas/tier_derivation.py` could derive no tier for any of them: every stored tier was asserted
with its own derivation input missing. B5(b) re-derived `scope` **blind from the retrieval-log
payloads**, applied five, and left four NULL. The proof that the derivation was blind is
`scratchpad/pr-131-project-status-overview/b5-DERIVED-BEFORE-TIER.txt` and its companion
`b5-derivation-independence.md` — read those first; the migration alone cannot establish it.

**No tier was changed and none is proposed here.** Tier is adjudicated judgment and its definitions
are owner-gated (CLAUDE.md §8). This note asks for four rulings and supplies the strongest version
of each side.

---

## 1. REF-00784 is a **documented tier dispute**, not a gap · HIGHEST

**Koontz AM, Brindle ED, Kankipati P, Feathers D, Cooper RA (2010),** *Design features that affect
the maneuverability of wheelchairs and scooters*, Arch Phys Med Rehabil 91(5):759–64,
doi `10.1016/j.apmr.2010.01.009`, PMID `20434614`. Live row as measured: `tier 1`,
`evidence_type clinical`, `scope NULL`, `notes NULL`, `derivation_chain NULL` — `notes` now carries
the record this section produced. **This is the batch's own declared T1 anchor** —
the retrieval-log manifest line says so in its `purpose` field: *"R2 backward mining of REF-00784
(Koontz 2010), the batch's declared T1 anchor"*.

B5(b) recorded it as a **gap**: *"Design not established by any payload in hand."* That sentence is
**true of the payloads and false of the repository.** Three records, all already committed, state
the design and dispute the tier. None is visible to the Grep tool — `.ignore` hides `audits/` and
`sessions/`; `grep -r` and `git grep` find them instantly (CLAUDE.md §7).

1. **`audits/anchor-correctness-sweep-2026-07-20.md:287`** — current tier 1, proposed 3:
   > *"PubMed (PMID 20434614, DOI 10.1016/j.apmr.2010.01.009) abstract explicitly states design
   > **'Case series.'** with convenience sample (MWC n=109, PWC n=100, scooter n=14). Not an
   > RCT/controlled experiment; **T1 is wrong.** T3 destination relies on internal mapping but
   > study-type…"*

   The DOI and PMID in that audit row are **byte-identical** to the live row's.

2. **`references/bpc/frameworks-and-methodology/manoeuvring-footprint-vs-turning-radius-methodology.md`**
   (lines 71, 130, 162) — records REF-00784 as **Tier 3** in running prose, in the citation-correction
   note, and in the source table, with the protocol quoted: *"widening the passageway in 5-cm
   increments until each task could be completed without hitting the walls"*, n = 109 / 100 / 14.

3. **`sessions/session_2026-08-16-pr103-adversarial-pass.md:203`** — *"Koontz **2010** (`REF-00784`,
   **Tier 3**, VERIFIED, with DOI and PMID)"*.

**So the repository has said since 2026-07-20 that T1 is wrong, with the design quoted, and nothing
was done.** Two of the three records call the row Tier 3 in prose while the database says Tier 1 —
CLAUDE.md §5(b), prose contradicting the database, live on the project's declared anchor.

**And the batch never retrieved the paper.** PMID `20434614` appears in **zero bytes** anywhere under
`retrieval-log/` (`grep -rl 20434614 retrieval-log/` returns nothing). The same batch *did* run PubMed
efetch for PMID 20690862 (REF-00971), 21657823 (REF-00972) and 40602232 (REF-00974), and a PMC
full-text efetch for PMC10648130 (REF-00973). The three payloads logged for REF-00784 — Crossref work
`09d0c286f7de90f9.json`, Unpaywall `711b950e88d42b38.json`, Crossref search `753c7d7e2af6c6d4.json` —
carry bibliographic identity only; the Crossref record has no `abstract` key. The one efetch that
would have settled the design was the one not made, on the one source the batch called its anchor.
**No retrieval was performed for this note either** — the network is out of scope here, and the
absence is the finding, not a task.

**Action taken:** none to the data beyond the record. `scope` stays NULL; the tier is untouched. The
dated note is written to `evidence_sources.notes` for REF-00784 through
`db.py amend-source`, which ledgers it into `metadata_integrity_detail` — the surface
`metadata_integrity_audit` puts in front of the owner.

**OWNER RULING SOUGHT (1 of 4).** Two questions, in order:
  (a) Does the 2026-07-20 sweep's finding stand — is REF-00784's tier 1 wrong? A ruling of *yes*
      makes `scope = lower_control` and `tier = 3` a mechanical consequence, not a judgment call.
  (b) If the answer turns on reading the abstract, authorise a retrieval of PMID 20434614 into
      `retrieval-log/`. It should have been the batch's first fetch and it was never made.

---

## 2. REF-00971 / REF-00972 — the escalation is right; the reasoning that reached it is not · HIGH

**Dutta T, King EC, Holliday PJ, Gorski SM, Fernie GR (2011),** *Design of built environments to
accommodate mobility scooter users: **part I***, doi `10.3109/17483107.2010.509885`, PMID 20690862 —
REF-00971. **King EC**, Dutta T, Gorski SM, Holliday PJ, Fernie GR (2011), ***part II***,
doi `10.3109/17483107.2010.549898`, PMID 21657823 — REF-00972.

**Part II's first author is King EC, not Dutta.** Byline order is reversed between the two papers;
`evidence_source_authors` holds both orders correctly. Anywhere this pair has been written as
"Dutta 2011 part II" or "Dutta/King", the part-II attribution is wrong and is corrected here.

Both rows are stored **tier 3**. The blind derivation returned **`high_control`**, which derives
**T1** — a contradiction with the stored tier, so both were left NULL and escalated. **That decision
is correct.** The argument offered for it is not, and the owner should not rule on it as written.

### The reasoning that was offered, and why it fails

The derivation concluded `high_control` and quoted *"an expert driver"* **on the same line**. That
phrase is the refutation, not the warrant.

`governance/tier-system.md` §1 defines T1 as *"Primary research with **intervention-level or
biomechanical control on the parameter under design**"*, anchoring claims that turn on a
*"physiological / behavioural / biomechanical mechanism"*. `schemas/tier_derivation.py` renders
`high_control` as *"intervention / RCT / biomechanical / sensory-threshold studies"*. **Every
exemplar in that vocabulary is an experimental design on people.** REF-00971/972 are bench tests:
free-standing styrofoam walls, five scooter models (part I) and two (part II), dimensions decreased
until the manoeuvre failed. Byte-quoted from the logged payloads —

> *"Free-standing styrofoam walls were used to define each configuration. **An expert driver**
> repeatedly manoeuvred the scooters through each configuration while we incrementally decreased the
> dimension of interest until it was no longer possible to complete the manoeuvre."*
> — payload `38b8b76bb0e8214d.xml` (PubMed efetch, PMID 20690862), part I

> *"Moveable Styrofoam walls defined each 'room' … 'Room' size was decreased until **our expert
> driver** could no longer perform the manoeuvre."*
> — payload `3d7ad150db8ba472.xml` (PubMed efetch, PMID 21657823), part II

PubMed's own `PublicationType` tags are *Journal Article*, *Research Support, Non-U.S. Gov't*
(part I) and *Comparative Study*, *Journal Article* (part II). **No human-subject design tag on
either.**

**And the repository had already settled this, in the database, on 2026-09-02.**
`evidence_population_match` for REF-00971 holds `match_grade = 'PROXY'`, `sample_size = 1`,
`study_population = "five scooters operated by ONE expert driver; **no scooter user participated**"`,
with the note:

> *"The human operator is an expert and, undeclared but implied, non-disabled. All user-side variance
> is absent — strength, trunk control, reach, spasticity, visual field, cognition, fatigue,
> confidence. **It measures what a DEVICE can do, not what a PERSON can do.** LPA, BAR, LMB and VES
> are entirely unrepresented."*

REF-00972's row adds: *"as part I: expert driver, two scooter models … Not independent of REF-00971:
same lab, same five authors, same driver, same method."*

A row whose own population grade says *no member of the population participated* cannot be the
high-control-on-people design the T1 rung describes. **The stored tier 3 looks right and the
derivation looks wrong.**

### The case for the other side, stated at its strongest

It should not be dismissed. The measurement **is** instrumented and the independent variable **is**
systematically manipulated under laboratory control — passage width decreased in controlled
increments until failure, in a purpose-built rig. If `high_control` is read as *control over the
parameter under design* (and the tier-system phrase is literally *"control on the parameter under
design"*), a swept-path bench test controls that parameter far more tightly than any
cross-sectional survey of wheelchair users does. On that reading the T3 rung — *"cross-sectional,
observational, qualitative, single-centre"* — plainly does not describe these papers either, and
forcing them into it is as much a stretch as calling them T1.

The genuine disagreement is therefore about **what `high_control` controls**: the *parameter* (rig
geometry) or the *participant* (physiology, behaviour, biomechanics). The ladder's exemplars say
participant; the ladder's own wording says parameter. **That ambiguity is the thing to rule on**,
and it will recur on every device-bench source the corpus admits.

### A third option, with in-repo precedent

Neither T1 nor a contested T3 is the only move. `sessions/session_2026-06-11-artifacts/2.5-resolution-table.md:32`
records the precedent:

> *"**high- vs lower-control** for the clinical rows (`00611/612/613/712/718`) defaulted to
> **lower_control** (conservative; keeps recorded tier where it was T3). If any is an
> RCT/experimental design it would be high_control→T1 — confirm against abstracts in Phase E."*

Applied here, `scope = lower_control` **agrees with the stored tier 3**, creates no contradiction,
needs no tier change, is expressly conservative, and would clear two of the four remaining
`adjudication_integrity` inconsistencies without an owner ruling at all. It is a defensible default
precisely because it never promotes.

**OWNER RULING SOUGHT (2 of 4).** Does `high_control` mean control over the *parameter* or over the
*participant*? Then either (a) `lower_control` on both, conservative, per the 2026-06-11 precedent,
or (b) `high_control` on both, which **promotes two rows from T3 to T1** and would make a
one-expert-driver styrofoam bench test co-equal with participant studies, or (c) a new discriminator
for device-bench measurement, which is a change to the tier system and squarely owner-gated.

---

## 3. REF-00976 — the design is asserted in the database with **no artefact behind it** · MEDIUM

Row: `tier 3`, `clinical`, `scope NULL`, doi `10.3130/aija.69.33_1`, *"ACUTUAL FEATURES OF
ORIENTATION TO LIFE TIME HOMES FROM VIEWPOINTS OF WHEEL CHAIR MOVEMENTS POSSIBILITY"* (2004, AIJ).

B5(b) called it a **gap**, and **as to the payloads that is exactly right**: Crossref
`ac2a86db5cbeca4c.json` has no `abstract` key, Unpaywall `a0e41367085fcfb7.json` has no abstract, and
the J-STAGE search response `d8217b8884ac188f.xml` is an Atom index carrying title, authors, volume,
pages and DOI — **no abstract element of any kind**. The J-STAGE full text was never retrieved.

**But the database already describes the design.** `evidence_population_match` for REF-00976, written
2026-09-02, `match_grade = 'PROXY'`, `sample_size = 0`:

> `study_population`: *"**field survey of newly built Japanese residences** — dwellings, not people"*
> `mismatch_note`: *"The unit of analysis is a BUILDING, not a person. **Wheelchair movement is
> assessed as a geometric possibility, never observed.** Japanese dwelling stock and Japanese body and
> device dimensions may not transfer. **Grade is provisional on the English abstract only, per R15.**"*

**That English abstract is in no logged payload.** So the record now says "design not established"
in one place and describes the design in another, and the second rests on bytes that were never
persisted — the same shape as the self-assertion B5(b) was fixing.

It matters which way it cuts. *Field survey of dwellings, geometric assessment, never observed*
implies `lower_control` → **T3**, which **agrees with the stored tier**. A characterisation with no
artefact behind it that happens to confirm the stored value is the least trustworthy kind, and it
is the kind CLAUDE.md §5(c) exists for.

**Action taken:** the collision is stated on the row rather than resolved — both the payload gap and
the population-match description, and the fact that the abstract behind the second is unlogged.
`scope` stays NULL.

**OWNER RULING SOUGHT (3 of 4).** Either authorise retrieving the J-STAGE record so the design rests
on bytes, or rule that `evidence_population_match`'s description is itself sufficient warrant — in
which case `scope = lower_control` follows and the row stops being underivable. **What must not
happen is the current state**, where one row of the database contradicts another and both are green.

---

## 4. The ladder cannot see **who was controlled** · record only

Not a defect in B5(b); a limit of the discriminator, surfaced because B5(b) is the first pass to
write `scope` from designs rather than from tiers.

- **REF-00974** is a written **T1 anchor** (`scope = high_control`, applied 2026-09-10) whose
  population row states: *"Stated plainly: **NO WHEELCHAIR USER TOOK PART.** Able-bodied
  participants have intact trunk control, no shoulder overuse history, no SCI-related muscle
  imbalance and no chronic exposure — they lack the very condition the study exists to inform."*
  Ten able-bodied participants; the derivation is correct on its own terms — the payload records
  instrumented biomechanical measurement — and the ladder has no way to record who was measured.
- **REF-00973**, also written `high_control` → **T1**, has an EXACT population row that says the
  inclusion criteria *"require independent community mobility in the MWC **INCLUDING ASCENDING AN
  ACCESS RAMP**, so the study structurally **SELECTS OUT** exactly the people for whom ramps are
  already impassable; the finding is a lower bound on population burden"*, and that **16 of 17
  participants are men** where *"shoulder anthropometry and strength are sexually dimorphic"*.

**`scope` discriminates control; it never records who was controlled.** So two rows now anchor at T1
while the database separately records that one enrolled no disabled participant and the other
excluded the worst-affected by design. The population grades are doing that work and nothing joins
them to the tier. This is a doctrine question — the tier system and the CRPD posture are owner-gated
(CLAUDE.md §8) — and it is recorded here rather than acted on.

---

## 5. Two sweeps owed, recorded not executed

- **REF-00978 `co1_source_type = 'dpo_annual_survey'` is not in the enum.** `schemas/enums.py`
  `Co1SourceType` admits `peer_reviewed_literature`, `dpo_research`, `advocacy_position`,
  `academic_narrative`, `validated_tool` — not `dpo_annual_survey`. `Co1Provenance` admits
  `published_corpus` and `participatory_synthesis`; the live `co1_provenance` is free prose. **Neither
  column carries a SQLite CHECK**, so nothing refused either value and nothing reports them.
  The prose is *correct* under **D-0178**
  (`decisions/DR-2026-08-31-co1-warrant-must-name-the-co-production.md`), which requires the warrant
  to name the co-production. **The enum is the stale caller of a ratified ruling** — CLAUDE.md rule 4,
  unswept ten days on. Owed: sweep `schemas/enums.py` (and any reader of it) to D-0178, and decide
  whether these columns get CHECKs or are declared free text on purpose. Not executed here.
- **`adjudication_integrity` quarantine reason was stale.** It read *"1 tier-derivation inconsistency
  of 5 checked"* (dated 2026-08-22, so rule-7-compliant, and wrong today). Measured 2026-09-10 by
  hand: **4 of 9, VERDICT FAIL** — REF-00784, REF-00971, REF-00972, REF-00976, all `scope NULL`. The
  registry reason is updated with the measured figure and its date. **It stays quarantined**;
  `run_checks` never selects it, and promotion is owner-gated.

---

## 6. TASK 3's owner gate — stated, not argued away

`workplan/2026-09-10-audit-reconciliation-execution.md` **TASK 3** marks this work
**OWNER DECISION, then SONNET**, with: *"evidence-tier definitions are owner-gated (CLAUDE.md §8).
The mechanism is safe; the authorisation is not mine."* **No authorising ruling was found.**
`grep -r` over `sessions/`, `decisions/` and `references/project-standards.md` — the paths `.ignore`
hides from the Grep tool — produced none, and no session record of this branch records one.

The distinction that likely saves the work is narrow and worth stating exactly, because it is not a
general licence:

> TASK 3 gated **the back-fill-from-tier route** — *"`clinical` tier 1 → `high_control`; tier 3 →
> `lower_control`"*, i.e. deriving `scope` **from** the adjudicated tier. B5(b) did the opposite: it
> derived `scope` **from the payloads**, blind, and then compared. **No tier moved.** Where the blind
> derivation contradicted the stored tier it wrote nothing and escalated — which is what an
> owner gate on tier definitions is *for*.

That is a distinction, not an authorisation. It is recorded in TASK 3 itself so the next reader meets
it there. **OWNER RULING SOUGHT (4 of 4):** ratify (or refuse) the five applied `scope` values
retrospectively. They are in the DB now, under
`scripts/migrations/data_20260910071239_2026-09-10-project-status-overview.sql`; a refusal is a
compensating migration away.

---

## 7. What was fixed in code, and what it revealed

`scripts/research/retrieval_log.py --verify-authors` — the repository's only artefact-diffing
verifier, and the direct remedy for CLAUDE.md §5(c) — **could not see the Co-1 source and reported
CLEAN.** `verify_authors()` selected `WHERE COALESCE(doi,'') <> ''`; **REF-00978 has no DOI** (it is
a PDF URL), so it was filtered out before the loop and never reached the `unlogged` list either. The
one source whose warrant CLAUDE.md §6 calls *"the worst failure available here"* sat silently outside
the verifier's scope, under a CLEAN verdict, with no denominator printed to make the shortfall
visible.

Fixed: every `evidence_sources` row is now considered, a row without a DOI is located by whatever
locator it has (URL/PMID/PMCID) against the manifest, and a payload this module cannot author-diff
is **reported as UNEXAMINABLE with its reason** instead of vanishing. The EXAMINED line now states
its denominator, and the closing verdict cannot read as a bare CLEAN while anything is unexaminable.

The same run now states what its ingester drops. `_logged_payloads()` accepts only bytes that
`json.loads` cleanly, so **every XML and PDF payload is invisible to it** — including the PubMed
abstracts behind REF-00971/972/974 and the PMC full text behind REF-00973, which are exactly the
bytes that carry the **design** that `scope` is derived from. Adding a PubMed-XML adapter was
declined as out of proportion (measured 2026-09-10: every DOI-bearing row already indexes through a
richer Crossref or Unpaywall payload, so an adapter would newly examine nothing and could displace
richer records). **The blind spot is now printed rather than fixed**, and it is recorded here as
owed work.
