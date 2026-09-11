# ICD-11 ↔ our three lenses — the high-level correspondence, and what blocks it

**Owner ruling 2026-09-11:** *"Yes, use ICD-11."* · *"eg MB5 series of codes discussing paralytic
symptoms"* · *"we are looking through ICD-11 for how it corresponds to our existing
ICF/identities/access needs on a high level."*

That settles three things the adjudication had to guess at. **ICD-11 is the source**, resolving the
licensing hold on DG-NON item 7. **The grain is the block, not the entity** — MB5 is a block, and
"high level" says so outright; the adjudication's 29 disease-entity rows were the wrong shape.
**The purpose is correspondence**, not a clinical vocabulary: the lens exists to let a reader who
arrives with a diagnosis find the functional demand we hold.

## The join is principled, and derivable from data we already have

ICF and ICD-11 are complementary WHO classifications — ICD classifies the condition, ICF the
functioning. **Every one of our 17 axes already declares its ICF b-anchors**, so the route is:

    ICD-11 block  →  the ICF b-code it impairs  →  our axis  →  identities and needs already on it

Nothing in that chain is invented. Re-derive the index with:

```
python3 -c "
import sqlite3, collections
con = sqlite3.connect('file:data/guidebook.db?mode=ro', uri=True)
byb = collections.defaultdict(list)
for code, anch in con.execute('select axis_code, icf_b_anchors from axes'):
    for b in (anch or '').split(','):
        if b.strip(): byb[b.strip()].append(code)
for b in sorted(byb): print(b, sorted(byb[b]))"
```

24 distinct b-codes across 17 axes. Three are shared, which is where one ICD block reaches several
axes at once: **b210** → AX-VIS-L, AX-VIS-N · **b710** → AX-REA, AX-WHM · **b730** → AX-AMB, AX-REA,
AX-WHM.

## The owner's own example, worked — and the trap it exposes

MB5 (paralytic symptoms) impairs muscle power, **ICF b730**. b730 is declared by AX-AMB, AX-REA and
AX-WHM. Those three axes already carry nine identities: BAR, BRAIN, DEM, LMB, LPA, MOB, MS, SCI, TALL.

**And three of those nine are wrong.** BAR (fat people), LPA (little people) and TALL attach to
AX-REA/AX-WHM for **anthropometric** reasons — reach envelope, clearance — not muscle power. Run the
join naively and the map asserts that paralytic symptoms correspond to being tall.

**So the b-anchor route is a CANDIDATE GENERATOR, not an answer.** This is the same defect D-0184
measured when it made the lens a column instead of a traversal: a two-hop path through a shared key
manufactures inference. The route proposes; judgment prunes; the pruning reason goes in the row's
`note`. A map built by running the query and accepting the output would be exactly the traversal the
owner already rejected once.

`icf_medical_map.mapping_confidence` is where the surviving judgment is recorded, on the four-value
scale ratified 2026-07-21 — `high_predictive` for a block whose impairment IS the demand,
down to `minimal` where the correspondence is incidental.

## What the lens reaches that we currently do not

**`AX-COG-L` — Information-access demand (b117, b167) — carries ZERO identities.** It is the only
orphan axis of the seventeen. ICD-11's intellectual-development and language blocks land precisely
there. That is the strongest argument for the medical lens beyond reader choice, and it is a
measurement rather than an argument: the lens fills a hole our identity lens has.

Re-derive:

```
python3 -c "
import sqlite3; con=sqlite3.connect('file:data/guidebook.db?mode=ro',uri=True)
for r in con.execute('''select a.axis_code,a.name,a.icf_b_anchors from axes a
  left join population_axis_map m on m.axis_code=a.axis_code
  group by a.axis_code having count(m.population_code)=0'''): print(r)"
```

## BLOCKED: not one ICD-11 code can be verified from this container

Measured 2026-09-11, every authoritative route:

| Route | Result |
|---|---|
| `id.who.int/icd/release/11/2024-01/mms/codeinfo/MB50` | **401** |
| `id.who.int/icd/entity/search?q=paralysis` | **401** |
| `icdaccessmanagement.who.int/connect/token` | **400** — OAuth2 client credentials required |
| `icd.who.int/browse/2024-01/mms/en` | 200, but a **JavaScript application**: the HTML is an empty shell, 20,887 bytes containing no code and no term |
| `icd.who.int/browse/2024-01/mms/en/search?q=MB5` | **0 bytes** |

No WHO credentials exist in this environment (`env | grep -i icd` → nothing).

**So every anchor written today lands `icd11_verified_at` NULL, and that is what NULL is for.**
`db.py add-medical` sets it only from a payload under `retrieval-log/` that contains the code, and
refuses a payload that does not — so there is no path by which an unverified anchor can present as
verified. What there is no path to at all, right now, is a verified one.

**A near miss worth recording.** Grepping the retrieval log for "MB5" matched `manifest.jsonl` — not
because any payload contained the code, but because *my own `purpose` string* did. The verification
check reads the named artefact rather than the manifest, so it was never exposed; but it shows how
close a "verification" can come to reading back the query that asked for it.

## What unblocks it

WHO ICD-11 API access is free on registration at `icd.who.int/icdapi`, yielding a `client_id` and
`client_secret` for the OAuth2 client-credentials flow. Set both as environment variables on the
remote environment and `retrieval_log.fetch()` can persist real `codeinfo` responses, after which
`add-medical --icd11-payload` stamps `icd11_verified_at` from bytes.

Until then there are two honest options and they are the owner's to pick:

1. **Wait for credentials.** Nothing is written; the correspondence analysis above stands as the
   design. Costs a session.
2. **Write the correspondence now with `icd11_verified_at` NULL**, anchors carrying the owner's own
   instruction as their provenance in `notes`, and backfill verification when credentials exist. The
   check reports the unverified count on every run, so the debt is visible and cannot be mistaken
   for verified. Costs a backfill pass.

**What is NOT an option:** writing ICD-11 codes from my own recollection and calling them anchors.
That is `CLAUDE.md` §5(c) — a field written from memory while a payload was obtainable — with the
single difference that here the payload is not obtainable, which makes it worse rather than better.
