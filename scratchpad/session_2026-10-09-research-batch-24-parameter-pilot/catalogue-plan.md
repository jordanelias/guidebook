# From parameters to a catalogue: what we hold, and a plan to derive items and categories

Prepared 2026-10-09 in the batch 24 session. This is a working paper in the session folder. It proposes; it decides nothing and records no ruling. Every figure below was derived on 2026-10-09; the commands at the end recompute them (CLAUDE.md rule 7a: re-run, do not trust).

---

# Part A. What we hold, organised

## A1. Where the project stands

| Stage | State today |
|---|---|
| Vocabulary (base) | 94 terms. 10 of them are now parameters: ramp gradient (older) plus nine promoted this session from the existing terms. The 17 `functional_axis` terms are deliberately left alone. |
| Research | 191 logged searches. 147 candidate sources staged, 110 still waiting for verification. 49 open gaps (19 of them top priority). |
| Evidence | 53 admitted sources: 11 first-tier (7 studies, 4 co-produced by disabled people's organisations), 2 reviews, 11 third-tier (6 studies, 5 grey), 29 codes, standards and national frameworks. 47 verified, 6 not. |
| Judgment | 101 extracted figures, **all about ramp slope** for wheelchair users. 54 are still preliminary. |
| Synthesis | 5 convergence records, all pending assessment. |
| Specification | 8 determinations, **all retired, none live**. The ramp-slope cell cannot be re-determined: the one strong source (a 2009 study) is only held as an abstract, and you ruled on 2026-09-25 that unreachable sources are given up for now. |
| Render | `parts/v10` is a stale stub of the old book. `site/` holds no pages. No determination is published anywhere. |

Why only ramp slope: the system can only file a figure against a parameter that exists, and until today one did. That is the problem the parameter list solves.

## A2. Your rulings that shape this work (plain words)

| Date | Ruling | What it means here |
|---|---|---|
| 2026-08-06 | The old corpus is a lead list, not evidence. | Old registries tell us what to fetch. Nothing is used until re-fetched and admitted. |
| 2026-08-19 | The 93 old items are leads, not topics. No item name becomes a topic. No old value crosses. | The catalogue's items cannot be copied from the old item list. |
| 2026-08-26 | The thing a determination is about is the **parameter**. The item is only a roll-up for display, computed from specifications. | A catalogue item must be derived, never stored as a key. |
| 2026-09-01 | The item layer was deleted: a container whose name states its answer biases every finding. | Names must be free of values and answers. The database refuses a name with a number or a min/max word. |
| 2026-09-09 | Parameters sit in the base vocabulary. Names are minted only from a phrase a source actually uses (`add-term`). "For now." | I cannot coin parameter names. You marked this as yours to revisit. |
| 2026-09-25 | If a source cannot be reached from anywhere, give up on it for now. | No retrieval tasks for unreachable documents. |
| 2026-09-28 | Research scope is buckets 1 and 2 only until each is exhausted for a slug. | Bucket 1: UN, ISO, Canada, USA, UK, Germany, Norway, Sweden, Japan, Australia. Bucket 2: EU, Singapore, New Zealand, Ireland, France, Spain, Portugal, Finland, Netherlands, South Korea. |
| 2026-10-01 | Remediation plan approved (D1 to D4). | The research-contract rules R16 and the rest of last week's tooling are in force. |

## A3. What we already hold (the "outdated but correct" material)

| Resource | Where | Size | Use under the rules |
|---|---|---|---|
| Standards registry: code body, current version, status, issuing-body URL, as of 2026-03-18 | `references/standards-registry.md` | 111 entries, 76 in buckets 1 and 2 plus international | Lead list for which codes to fetch |
| Verified code and framework sources | `references/tier456-verified-sources.json` | 249 | Lead list |
| Advocacy and lived-experience bodies | `references/co1-verified-sources.json` | 25 | Lead list |
| Occupational-therapy professional bodies | `references/co2-verified-sources.json` | 15 | Lead list |
| Code leads in the database | `research_code_leads` | 96 | Lead list |
| Pre-reset corpus | `_archived/data/corpus-pre-reset-2026-08-06.db` | 863 sources | Lead list; also 20 old per-item value files, not to be used for values |
| Combined worklist built today | `major-sources-worklist.md` (this folder) | 76 + 96 + 25 + 15 | Starting point for acquisition |
| Frames for grouping | `axes` (17 functional demands), `access_needs` (17, in 5 families), `rooms` (17 spaces), `base_icf` (72 ICF codes), `terms.domain` (18 values) | live | Candidate vocabularies for categories and overlays |

Limits found today:
- Full text is saved for only 14 of the 53 sources (batch 23's), and only in part: the Spanish building code 4 of 79 pages, the Madrid paper 6 of 68, the French guide 5 of 65. The other sources would be fetched again.
- EN 17210 is paywalled and the CSA B651 fetch was refused (batch 22 and 23 records). ISO 21542, BS 8300, DIN 18040 and AS 1428.1 are expected to be paywalled as well [UNVERIFIED: not yet tried]. Any that cannot be read remain leads; names cannot be taken from text we cannot read.
- Four batch 23 scans were stopped. Two finished (52 items) and sit unused in the harness scratchpad.

## A4. Decisions you gave this session, and what is recorded

| You said | Status |
|---|---|
| Keep the WP12 rule (R7 floor removed, R5 re-aimed) | Not yet in the ledger |
| Use the existing terms registry as the seed | Applied for nine terms. Not in the ledger |
| A skimmed (preliminary) figure may set a published value if tagged for follow-up | **Provisional reading.** Not in the ledger. Does not clear the check that blocks unverified sources |
| Option A: turn the 94 terms into measurable quantities | Cannot be done by invention; superseded by the next line |
| Pull from the major codes, literature and advocacy of major countries; an exhaustive dated bibliography exists | Worklist built. Nothing fetched or admitted yet |

These should go into `references/project-standards.md` as one dated owner-ruling entry, in the research PR that carries the work (a ledger entry is not tooling).

## A5. Corrections to my earlier reports

- I said specification 8 "stands at 5%". All 8 are retired; nothing is live.
- I recommended fetching the 2009 study's full text. The 2026-09-25 ruling closes that.
- I estimated roughly a dozen measurable quantities among the 94 terms. The conservative count was nine, giving ten parameters with ramp gradient. The rest of the terms are objects, conditions, people or methods.
- I started scanning batch 23's sources as if they could seed a general list. They cannot: one search, six countries' building rules, partial text.

---

# Part B. Plan: derive items and categories for a catalogue

## B1. Words used

- **Parameter**: a measurable design quantity with a value-free name, such as "ramp gradient" or "doorway clear width". The unit a determination is about.
- **Element**: the thing the quantity belongs to (ramp, door, handrail, lift). Some are already terms (ramp, circulation route, grab bar).
- **Item**: a catalogue entry that bundles the parameters of one element so a reader meets them together. **Derived, never stored as a key**.
- **Category**: a browsing group of items (for example "Openings and doors").
- **Catalogue**: the Part 4-style library of items with categories, the render of all this.

## B2. What the first catalogue shows (Release 0)

The guidebook's doctrine is to help people ask the right questions. So Release 0 does not wait for determinations. For each item it shows:

1. the parameters (the questions to ask);
2. which jurisdictions' codes set a requirement, attributed and marked as regulatory only (◐), never as a determination;
3. the evidence state of each parameter (no determination, determined, disputed);
4. which access needs and rooms it touches, **only where a determination already says so**.

Values from codes appear only as attributed code content. Anything unmarked is an error (existing rule).

## B3. Derivation rules

Each grouping is computed from something with provenance, and the person or step that judges is named (CLAUDE.md rule 8).

| Step | Derives | From | Judge |
|---|---|---|---|
| D1 | Parameter names | Phrases the admitted sources use, scanned in full text, quote checked against the text by script | Session proposes; owner reviews list in the PR |
| D2 | Element of each parameter | The clause or chapter the phrase sits in (locator), reconciled to an element term | Session; reason recorded per row |
| D3 | Item | One item per element with at least one parameter. Name = the element's term name | Computed (a view) |
| D4 | Category | Candidate list computed from `terms.domain` and the chapter groupings of the admitted codes; **you approve the final list once** (about 12 to 15 names) | Owner, once. Membership then computed |
| D5 | Order | A journey sequence: approach, entry, horizontal movement, vertical movement, rooms and fixtures, controls, wayfinding and communication, environmental conditions | Owner approves the sequence; items sort by it |
| D6 | Who it serves | `specifications` lens columns only (identity, access need, ICF, medical) | Judgment stage, per existing ruling. Empty until determinations exist |
| D7 | Where it applies | A room-by-element relation, derived from clause scope; the 17 live `rooms` | Session with source warrant; later phase |

Coverage check (after D1 to D4 are frozen): compare against the archived old item index and list topics we missed, by name only, never importing a name or value. This follows the "blind first" rule.

## B4. Phases

Rule 10: tooling ships separately and first. Rule 9: open each PR last and do not watch it.

| Phase | What | PR | Gate | Size |
|---|---|---|---|---|
| P0 | Your decisions in B7 | none | your answers | small |
| P1 | Re-fetch the free major codes, bucket 1 then bucket 2, admit them properly, save full text | research | normal batch gate; adversarial pass (these are research tables) | large |
| P2 | Scan the admitted texts for quantity names; script checks every quote; session adjudicates; mint terms; promote parameters; you review the table before anything is written | research | R16, `test_db_integrity`, review | large |
| P3 | Tooling: an element relation (the only new base table), the derived item and category views, a catalogue generator, completeness checks; re-key or remove the dead item-dependent tables (`room_items`, `item_taxonomy_links` and others are currently unwritable) after a caller sweep | tooling | `schema_reference_audit`, selftest, sweep | medium |
| P4 | Data: element assignments (D2), approved category vocabulary (D4), sequence (D5) | research | completeness checks | medium |
| P5 | Render: item and category pages, the room matrices, regenerated derived outputs | render | fresh-render checks | medium |
| P6 | Ongoing: each slug's research scans every source for **all** parameters; the catalogue updates itself | research | per batch | continuing |
| P7 | Acceptance: at least one item answers one question with a determination, published | none | DR section 4 criterion | depends on P6 |

P1 and P2 can overlap by source. P3 can start any time, since it needs no research rows.

## B5. Checks (derived, not curated)

- Every parameter has exactly one element, or is listed as unassigned.
- Every item has at least one parameter; every category at least one item.
- No parameter, item or category name contains a digit, a comparator or a min/max word, or an `A-01` style code.
- Item count and category count are queries, never typed.
- Every parameter name traces to an observation with a quoted phrase in an admitted source.
- A category cannot be created by editing; it comes from the approved vocabulary.

## B6. Risks and containment

| Risk | Containment |
|---|---|
| The list mirrors what regulations measure, not what disabled people need | Add literature and advocacy sources in P1; keep the lens overlay empty until judgment fills it; run the coverage check against the ICF and access-need frames, not only the old items |
| The old container bias returns through names | Names come from source phrases and are checked for values; the old item index is consulted only after freezing |
| Paywalled major codes are missing | They are listed as leads in the catalogue's evidence-state column, not silently absent |
| A parameter is later judged wrong; no verb retires one | Promote conservatively; add a retire verb in P3 if needed |
| Large scans produce unreviewable output | Table for your review before writing; no adversarial pass is required for vocabulary tables, so your review is the check |
| The catalogue looks empty | Release 0 is defined as questions plus evidence state, stated up front |

## B7. Decisions needed from you

1. **Acquisition.** Go ahead with fetching and admitting the free major codes, bucket 1 first? *Recommend yes.*
2. **What an item is.** A derived roll-up of one element's parameters, computed by a view, no stored item table? *Recommend yes.*
3. **Category vocabulary.** I propose the candidate list from the vocabulary and the codes' own chapters; you approve about a dozen names once. *Recommend yes.*
4. **Tooling first.** Allow a separate tooling PR for the element relation, views, generator and the dead-table clean-up before the data goes in? *Recommend yes.*
5. **Release 0.** Publish the question catalogue (parameters, code attributions, evidence state) before any determination exists? *Recommend yes.*
6. **Record today's decisions** in the ledger in the next research PR, using your words, with the "preliminary figure" wording marked provisional until you correct it? *Recommend yes.*

---

## Commands that recompute the figures

```
python3 - <<'PY'
import sqlite3; c = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
for q in ("select count(*) from terms", "select count(*) from base_parameters",
          "select count(*) from evidence_sources", "select count(*) from source_value_extractions",
          "select count(*) from specifications where retired_at is null",
          "select count(*) from specifications", "select count(*) from gaps where status='OPEN'",
          "select count(*) from research_code_leads", "select count(*) from rooms",
          "select count(*) from axes", "select count(*) from access_needs", "select count(*) from base_icf",
          "select count(distinct domain) from terms", "select count(*) from search_executions"):
    print(q, c.execute(q).fetchone()[0])
PY
python3 scripts/run_checks.py --list          # the checks named above
grep -c '^jurisdiction:' references/standards-registry.md   # registry entries (includes the template)
```
