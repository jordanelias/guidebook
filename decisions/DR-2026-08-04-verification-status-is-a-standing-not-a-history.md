# DR-2026-08-04 — `verification_status` is a standing, not a history

- Status: **PROPOSED** — owner decision required. Nothing in this DR is executed until it is
  ratified. The three checks it unblocks (B01, B02, B05 in `test_db_integrity.py`) stay red
  until then, which is the correct state for an unratified vocabulary.
- Date: 2026-08-04
- Category: **D-SCHEMA** (controlled vocabulary + column semantics). Change-Order gated per
  `schemas/enums.py` header. Touches what "verified" *means*, so it is **DG-NON-adjacent**:
  prepared for the owner, not decided here.
- Prepared by: Claude, at owner direction, after the owner rejected the premise of the
  question they were originally asked.
- Affects: `evidence_sources.verification_status` (863 rows), `metadata_quality`,
  `source_type`; `schemas/enums.py:265-279`; `scripts/tests/test_db_integrity.py` B01/B02/B05;
  `governance/co1-operational.md` §203/§398/§445; `governance/evidence-methodology.md` §48/§204.
- Related: DR-2026-05-19 (manual-track explicit-cause states), DR-2026-07-20
  (tier-model enshrinement; coined `DISPUTED`), migration `041_value_overflow_columns.sql`
  (the same disease, diagnosed and fixed for a different set of columns).

---

## 1. The question this DR was going to ask, and why it was the wrong one

The `DB integrity` check B01 rejects four `verification_status` values that are live in the
corpus: `VERIFIED-2` (71 rows), `DISPUTED` (7), `VERIFIED-WITH-CORRECTION` (2), `VERIFIED-1` (1).
Each was coined by a session migration with a disclosed rationale. The obvious DR was
therefore: *ratify the coined vocabulary and amend the check.*

The owner rejected that framing on all three counts:

> "if we have things like VERIFIED-1 or VERIFIED-2 as alternatives to verified…then they're not
> verified properly or there's an issue with our process for what qualifies as verified"
>
> "UNVERIFIED-1 is a problem too"
>
> "VERIFIED-WITH-CORRECTION is meaningless. it's merely verified"

That is the correct reading, and the evidence below supports it in every particular. Ratifying
these values would have entrenched a category error the repo has already diagnosed and fixed
once, in a different column.

## 2. The diagnosis: one column holding three different things

`verification_status` currently encodes three orthogonal facts at once:

| Fact | Encoded as | Where it actually belongs |
|---|---|---|
| **Standing** — is this source established? | `VERIFIED` / `UNVERIFIED-…` | `verification_status` |
| **Method** — how was it established? | the `-1` / `-2` suffix | a `verification_method` column (does not exist) |
| **History** — how many attempts, what happened? | `-1` suffix, `WITH-CORRECTION` | `verification_attempt_count` and `verification_note` (**both already exist**) |

This is precisely the conflation migration 041 was written to end, in its own words: *"A column
must hold one domain. Several here hold two: a value AND the prose qualifying it."* 041 fixed
`author_display`, `publisher` and `standard_number`. `verification_status` has the same disease
and was not in scope.

### 2.1 The encoded history is not merely redundant — it is false

`verification_attempt_count` already exists and is populated across the corpus (0–5). Compare it
against the `-1` suffix that claims to mean "one search attempt, not yet retried"
(`governance/evidence-methodology.md` §204):

| `UNVERIFIED-1` rows | actual `verification_attempt_count` |
|---|---|
| **25** | **0** |
| 5 | 1 |
| 1 | 3 |

**26 of 31 rows are contradicted by the column that actually tracks attempts.** A status value
that disagrees with its own dedicated column in 84% of cases is not a refinement; it is a second,
worse copy of a fact already recorded properly.

**And nobody agrees what the suffix means.** `governance/evidence-methodology.md` §204 defines it
as *"one search attempt, not yet retried."* Reading the same value cold during the preparation of
this DR, the owner inferred the opposite direction — *"verification-1 probably means a second
attempt was made."* Both readings are reasonable from the string alone; the string is why they
diverge. When the project's own owner cannot recover the intended meaning of a value from its
name, and the corpus contradicts the documented reading in 25 of 31 rows anyway, the encoding has
failed on both counts at once — it is ambiguous *and* wrong. An integer column is neither.

### 2.2 `VERIFIED-1` collides with `UNVERIFIED-1` and means the opposite

`UNVERIFIED-1` is canonical (`schemas/enums.py:276`, three governance documents). `VERIFIED-1`
was coined in July, appears in **no** governance document, and differs from the canonical value
by two characters while meaning its opposite. One row carries it. This is a defect waiting to
happen in any hand-written query, filter, or migration `WHERE` clause.

### 2.3 `VERIFIED-WITH-CORRECTION` describes an event, not a standing

Two rows. Both were verified; during verification, metadata was corrected. The correction is an
audit-trail fact, and both rows already carry it in `verification_note`. Their *standing* is
simply verified. The owner's phrasing — "it's merely verified" — is exactly right, and the
value's continued existence forces every consumer to remember a synonym.

### 2.4 `VERIFIED-2` is honest about its method and wrong about its standing

These 71 rows are the substantive case, and the sessions that created them were scrupulous, not
sloppy. A representative note, verbatim:

> "Direct WebFetch of the registry URL returned HTTP 403 (site blocks the fetch tool; confirmed
> not a proxy failure). Verified instead via 3 independent WebSearch retrievals returning
> consistent title, publisher, and content detail — **real retrieval, not fabrication, but one
> step removed from a direct render**; verification_status set to VERIFIED-2 (not VERIFIED-1) to
> record that distinction honestly."

The author was trying to avoid overclaiming and had no vocabulary to do it in, so they invented a
grade. But **the document was never obtained.** Existence and metadata were corroborated across
independent sources; the artefact itself was not read. Calling that a *grade of verified* buries
the distinction inside a value that sorts, filters and reads as verified — which is the failure
mode the note was trying to prevent.

**Safety fact, measured:** **zero** published cells cite a `VERIFIED-2` source
(`cell_source_links` ⋈ `evidence_sources`). No best-practice determination depends on one, so
correcting their standing changes no cell state and no rendered page.

## 3. What "verified" should mean

The repo has never written this down. That absence is the root cause: three sessions each
invented a local answer. Proposed definition, for ratification:

> **VERIFIED** — the source document itself was obtained, and the metadata recorded here was read
> from it. Not from a citing bibliography, not from a search-result summary, not from a
> publisher's landing page describing it.

Everything short of that is not a weaker grade of verified. It is **not verified**, plus a
recorded reason.

### 3.1 What "the document" is for a Co-1 source

The definition above is written for documentary sources and would, read literally, demote every
Co-1 source in the corpus. That would be an error of doctrine, not of bookkeeping: **Co-1 —
lived experience and participatory design — is co-primary with T1** under CRPD Art. 4.3
(`governance/tier-system.md`), and its verification channel is deliberately manual
(DR-2026-05-19). Measured: **41 rows** carry `verified_by_tool = 'co1-manual-pre-pipeline'` at
status `VERIFIED`, and `test_db_integrity.py:236` (C04) already carves out `co1%` explicitly.
A first draft of this DR omitted Co-1 entirely; that omission is corrected here.

For a Co-1 source the artefact being obtained is the **attestation** — the recorded testimony,
co-production record, or participatory-design output — not a publication. The bar is unchanged in
substance: what is recorded must have been read from the thing itself, by someone who obtained it.

> **VERIFIED (Co-1)** — the attestation itself was obtained, and what is recorded here was taken
> from it. Method `co1-attestation` (§4.3).

This is not a weaker verification. It is the same standard applied to a different kind of
artefact, which is what co-primacy requires.

## 4. Proposed vocabulary — three columns, owner-specified

The owner's decomposition, adopted:

> "CLOSED seems like it should be its own column paired with VERIFIED/UNVERIFIED/PARTIAL and then
> OPEN/CLOSED. UNVERIFIED+OPEN would call for a return pass but UNVERIFIED+CLOSED would mean that
> it can't be verified after effort spent."
>
> "attempt count is the third column for that set."
>
> "PARTIAL no longer exists because that doesn't really mean anything."

The last of those arrived after the first draft of this section had kept `PARTIAL`, and it is
right: once disposition exists, `PARTIAL` is `UNVERIFIED` + `OPEN` said longer. Applying the same
test to the one value this DR had reserved judgment on retires `DISPUTED` as well (§4.4).

| Column | Values | Answers |
|---|---|---|
| `verification_status` | `VERIFIED` · `UNVERIFIED` | **Is it established?** |
| `verification_disposition` | `OPEN` · `CLOSED` | **Is more effort owed?** |
| `verification_attempt_count` | integer — **already exists** | **How much effort was spent?** |

Three orthogonal facts, three columns. The suffixes disappear because there is nothing left for
them to smuggle.

**The status column is binary.** Every intermediate value proposed for it — `PARTIAL`,
`DISPUTED`, and the six retired suffixes — turns out to be one of the other two columns wearing a
disguise (§4.4). A source is established or it is not; how far anyone got, and whether they are
coming back, are separate questions with their own columns.

### 4.1 The matrix

|  | `OPEN` | `CLOSED` |
|---|---|---|
| **`VERIFIED`** | **⚠ ERROR STATE.** Verification is finished or it did not happen; there is no "verified but still owed". A row here is a defect to investigate, not a condition to occupy. | Verified and settled. The resting state of a good source. |
| **`UNVERIFIED`** | Not established; a return pass is owed. Everything previously called `PARTIAL`, `UNVERIFIED-1`, `IS-PAYWALL` or `DEFERRED-V2-AUTOMATED` lands here, distinguished by its reason and its attempt count rather than by its name. | Not established **after effort spent**. Terminal, earned, and reasoned. |

Four cells, one of which is a defect detector. Nothing else is needed.

A re-check falling due — a superseding edition, code currency — is **not** `VERIFIED` + `OPEN`.
That is a different question with its own columns (`code_currency_status`,
`code_currency_verified_at`). Letting it occupy this cell would put the matrix's one diagnostic
signal back to work as a legitimate state, and lose it.

### 4.2 The tuple audits itself

Because the three facts are now separate columns, they can be checked against each other. Four
invariants follow directly, and each one catches something no current check can see:

> **I1** — `status = 'VERIFIED'` ⟹ `disposition = 'CLOSED'`.
> No "verified but still owed". (§4.1)
>
> **I2** — `status = 'VERIFIED'` ⟹ `attempt_count ≥ 1`.
> The owner's question: *how could there be no attempt made?* Verification **is** an attempt. A
> verified row with zero attempts means nobody recorded doing the thing that verified it.
>
> **I3** — `disposition = 'CLOSED'` **and** `status ≠ 'VERIFIED'` ⟹ `attempt_count ≥ 2`
> **and** `verification_closure_reason IS NOT NULL`.
> "Can't be verified **after effort spent**" — closure has to be earned and reasoned, not asserted.
>
> **I4** — `disposition = 'OPEN'` ⟹ the row is in the return queue.
> Nothing is parked silently.

**I2 measured against today's corpus — 360 of 824 VERIFIED-family rows (43%) carry zero recorded
attempts:**

| status | attempts = 0 | total |
|---|---|---|
| `VERIFIED` | 289 | 750 |
| `VERIFIED-2` | 68 | 71 |
| `VERIFIED-WITH-CORRECTION` | 2 | 2 |
| `VERIFIED-1` | 1 | 1 |

135 of those 360 carry a `verified_by_tool` — so the tool established them and never incremented
the counter, which is a tool defect. 321 hold a locator. The rest are unexplained.

This is what the three-column model is *for*. Under the old vocabulary the claim and its evidence
were the same string: `UNVERIFIED-1` asserted an attempt count in its own name and was **wrong in
26 of 31 rows** (§2.1), and nothing could catch it. Split into peer columns, the corpus reports
its own inconsistency on day one — 43% of it.

**Where a row evidences its own verification, I2 is satisfied by backfill, not adjudication** —
if they really were verified, the attempt simply went unrecorded. Splitting the 360 by what the
row itself already proves:

| | Rows | Disposition |
|---|---|---|
| `verified_by_tool` set | **135** | **Backfill.** A tool established these and failed to increment the counter — a tool defect, not a data lie. Fix the counter, and fix `resolve_dois`/`verify_urls` so it stops happening. |
| No tool, but `doi_resolution_outcome = 'RESOLVED'` | 83 | Probably backfillable. The DOI dereferenced, which is an attempt. Confirm the resolution is real before counting it. |
| Neither | **142** | **Adjudicate.** Nothing in the row evidences that anyone tried. These are where I2 earns its keep: either the attempt happened and went entirely unrecorded, or the row should never have said `VERIFIED`. |

So I2 is a check that *sorts* rather than condemns: 135 are a bookkeeping fix, 83 are near-certain,
and 142 are the real question. Only that last group needs judgment, and it cannot be batch-decided.

**I3 needs its own column, and reusing an existing one would repeat this DR's own diagnosis.**
An earlier draft pointed closure at `processing_blocked_reason`. That column already has a
CHECK-constrained vocabulary bound to a *different* domain — data capture and mining deferral:
`no-full-text`, `paywalled`, `no-doi`, `not-indexed`, `language`, `no-quantified-claims`,
`superseded`, `out-of-scope`, `tier-not-required` (`040_source_processing_state.sql:70-80`). Three
of the terminal reasons below are not in that CHECK, so the ratification migration would have
violated the constraint outright; and loading verification closure into a capture-status column is
precisely the one-column-two-domains failure §2 is about. A DR that diagnosed the disease and then
reproduced it would deserve to be rejected.

So: a new `verification_closure_reason` column, its own controlled set — `paywalled`,
`print-only`, `access-denied-persistent`, `withdrawn`, `not-found-after-search`.

### 4.3 `verification_method` — a fourth column for *how*

Orthogonal again, and the home for what the `-1`/`-2` suffixes were really carrying:

| Value | Meaning |
|---|---|
| `direct-render` | The document was fetched and read. The only method compatible with `VERIFIED`. |
| `corroborated-not-retrieved` | ≥2 independent retrievals agree on title/publisher/content; document not obtained. **Never `VERIFIED`.** |
| `citing-bibliography` | Existence attested only by another work's reference list. **Never `VERIFIED`.** |
| `tool` | Established by `resolve_dois` / `verify_urls`; `verified_by_tool` names which. |
| `co1-attestation` | The attestation itself was obtained and read (§3.1). Compatible with `VERIFIED`. Covers the 41 `co1-manual-pre-pipeline` rows, which have no home under the other four. |

> `verification_status = 'VERIFIED'` **⟹** `verification_method` ∈
> {`direct-render`, `co1-attestation`} **or** `verified_by_tool IS NOT NULL`.

This replaces B01's string-list matching with a rule that means something.

### 4.4 Three values that were never verification standings

An earlier draft of this DR kept `PARTIAL` and reserved judgment on `DISPUTED`. Both were wrong,
and the same test that condemned the suffixes condemns them.

**`PARTIAL` — retired.** It does not survive contact with its own rows. It lives in
`metadata_quality`, and it cross-cuts verification entirely: its 5 rows are `VERIFIED-2` (1),
`VERIFIED` (1) and `UNVERIFIED-1` (3). A value that appears on both sides of the verification
line is not describing verification. Read as a standing it means "some of it confirmed, more
owed" — which is `UNVERIFIED` + `OPEN`, said longer. The owner's condition for keeping it (*"so
long as it is flagged for a return"*) is now discharged structurally by the disposition column, so
the value has nothing left to carry.

**`DISPUTED` — retired.** It fails on its own numbers. DR-2026-07-20 justified it as sources that
"could not be located by two independent agents (verify + adversarial refuter) via real
retrieval". Against `verification_attempt_count`:

| DISPUTED rows | attempts recorded |
|---|---|
| 3 | **0** |
| 4 | 1 |
| **0** | **≥2** |

Not one of the seven records the two attempts its own justification claims. This is precisely the
`UNVERIFIED-1` failure (§2.1) in a different value: a status asserting an effort level that the
column tracking effort contradicts. It also conflates a standing with a *usage rule* — the
anchor-suspension consequence is bolted onto the status — and that consequence is already implied,
because an `UNVERIFIED` source should never anchor a determination in the first place. Confirmed
in the data: DISPUTED rows anchor **0** cells today.

`DISPUTED` becomes `UNVERIFIED` + `CLOSED` + reason `not-found-after-search`, with the attempt
count carrying what the name was asserting. The 0-and-1 attempt counts are a **finding, not an
obstacle**: the sweep's two independent retrievals were real work that was never recorded. Under
I3 those rows cannot be written `CLOSED` until the count reflects them — which is the invariant
doing its job on the first migration that meets it.

**`SUPERSEDED` — retired.** A row-lifecycle fact, not a standing, and *already* recorded by
`superseded_by_ref_id` being non-null. Keeping it in the status column is the same conflation one
layer out. The pointer is the record.

### 4.5 `metadata_quality` — `PARTIAL` retired from here too

`PARTIAL`'s 5 rows are re-expressed as `UNVERIFIED` + `OPEN` with the outstanding item named in
the reason (§4.4). Its former home has no return mechanism at all — nothing in the codebase queues
a `PARTIAL` row for completion, so "partial" has in practice meant "parked indefinitely,
silently." The disposition column makes that impossible: a row is `OPEN` and owed a return pass,
or `CLOSED` with an earned attempt count and a stated terminal reason. There is no third option
and nowhere to sit between them.

Separately, not a vocabulary question: 4 rows hold `high` / `medium`, confidence words written
into the wrong column by a 2026-07-25 batch. Junk data, remediated by migration.

### 4.6 `source_type` — `code` ratified

16 rows, every one `tier=6` (French *arrêtés*, Italian DPCM, Japanese ministerial standards).
Mirrors `EvidenceType.CODE` at `schemas/enums.py:208`. Used consistently; uncontroversial.
`grey_literature` (2 rows) is a spelling variant of canonical `grey` and is normalised by
migration; `magazine_article` (1 row) is a single-row judgment recorded in its note.

## 5. Migration mapping, if ratified

| From | Rows | status | disposition | method | Notes |
|---|---|---|---|---|---|
| `VERIFIED` | 750 | `VERIFIED` | `CLOSED` | `tool` / `direct-render` | Method backfilled from `verified_by_tool` and the note. Where the note evidences no render, the row becomes `UNVERIFIED` + `citing-bibliography` + `OPEN`. This will reclassify some of the 750, and that is the point. |
| `VERIFIED-1` | 1 | `VERIFIED` | `CLOSED` | `direct-render` | Meets the §3 bar. |
| `VERIFIED-WITH-CORRECTION` | 2 | `VERIFIED` | `CLOSED` | `direct-render` | Correction already in `verification_note`. |
| `VERIFIED-2` | 71 | `UNVERIFIED` | `OPEN`, or `CLOSED` where the block is permanent | `corroborated-not-retrieved` | **The material change.** No cell is affected (§2.4). 13 record HTTP 403 and are candidates for `CLOSED` + `access-denied-persistent`; each needs adjudicating, not batch-closing. |
| `UNVERIFIED-1` | 31 | `UNVERIFIED` | `OPEN` | per note | Attempt count already carries the truth and corrects the name for 26 rows: 25 have **0** attempts, so they are `OPEN` with nothing yet spent — which is exactly what they should have said all along. |
| `DISPUTED` | 7 | `UNVERIFIED` | `CLOSED` once attempts are recorded, else `OPEN` | `corroborated-not-retrieved` / per note | Reason `not-found-after-search`. None of the 7 currently records the ≥2 attempts its own justification claims, so under I3 they cannot be written `CLOSED` until that work is recorded (§4.4). |
| `PARTIAL` (metadata_quality) | 5 | `UNVERIFIED` | `OPEN` | per note | Outstanding item named in the reason. Cross-cuts three different statuses today, which is why it was never a standing (§4.4). |
| `SUPERSEDED` | 1 | — | — | — | Retired; `superseded_by_ref_id` is the record (§4.4). |

No row may be written `CLOSED` by this migration without satisfying §4.2. Where effort was not in
fact spent, the row lands `OPEN` with `attempt_count = 0` — an honest queue entry rather than a
quiet burial.

### 5.1 The pipeline writes this column too, and must be changed in the same act

Retiring vocabulary from a column that a **weekly job writes** is not complete when the rows are
remapped. `scripts/resolve_dois.py` declares in its own header that it writes `verification_status`
values `VERIFIED` and `NO-MATCH`; B01's current list also admits `NO-MATCH`, `NEEDS-HUMAN`,
`REVERTED`, `PROBABILISTIC`, `IS-PAYWALL` and `DEFERRED-V2-AUTOMATED` — zero rows each today, which
is exactly why they are easy to overlook. If B01 narrows to `{VERIFIED, UNVERIFIED}` and the jobs
are left alone, **the next scheduled run can write a value the check now forbids** and paint the
gate red without a human touching anything.

The ratification migration therefore ships with an audit and update of the write vocabulary in
`scripts/resolve_dois.py` and `scripts/verify_urls.py`, in the same change. A vocabulary decision
that does not reach the code that writes the column has not been made, only announced.

**Consequence the owner should weigh explicitly:** the corpus's "verified" count drops by at
least 71 (~8%), and §5's first row may push it further. Nothing is lost — the same sources, the
same notes, the same real work — but the headline number falls because it was overstated. That
is the DR working, not failing.

## 6. What this DR does not decide

- Whether any individual `VERIFIED-2` row is terminal or returnable (§4.3) — research, under R10.
- Whether the 750 `VERIFIED` rows individually evidence a render. §5 row 1 proposes the rule; the
  audit that applies it is separate work and may reclassify more rows.
- The `standard_eb` vs `national_fw` classification of UN treaty-body instruments, recorded as an
  open conflict by the 2026-08-04 dedup merge.
- Whether any specific formerly-`DISPUTED` source in fact exists. Retiring the value re-expresses
  their standing; it does not adjudicate the underlying question, which is research under R10.

## 7. If not ratified

B01, B02 and B05 stay red. That is the honest outcome: the check would be asserting a vocabulary
the project has not agreed to. The alternative — adding the coined values to the check's list —
would make the suite green by ratifying, silently and without a decision record, the position the
owner has explicitly rejected.
