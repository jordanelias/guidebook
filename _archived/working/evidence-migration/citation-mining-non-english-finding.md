# Citation mining for non-English sources — scoping finding and result

*Session: `session_2026-07-19-non-english-research-recovery-batch9`. Companion to `equity-dashboard.md`,
`global-south-finding.md`. Prompted by a direct request to "consider performing citation mining for all
non-English sources" after the Global-South leads closed out in batch 7. Migration:
`data_20260719192627_..._batch9.sql`.*

## What "citation mining" means in this project, concretely

This is not a loose phrase — the DB already has a `citation_mining` table and a working script
(`scripts/probes/citation_mining_pipeline.py`) that define the method precisely: for a source with a DOI,
query **CrossRef** for its reference list (`backward` mining — what this source cites) and **OpenAlex**
for its cited-by count (`forward` mining — what cites this source), then use the aggregated reference pool
to find and verify new candidate sources. 107 rows already exist from earlier sessions (7 slugs), with real
CrossRef/OpenAlex query results recorded in their `notes` fields (e.g. REF-00001's row: "BACKWARD: CrossRef
(refs=66...) FORWARD: OpenAlex cites:W2003033699 (168 cited_by_count...)").

That precision matters for scoping this task honestly: **citation mining requires a DOI.** It is not a
generic "search for related work" step — it is a specific, DOI-keyed, API-driven method.

## Scope: how much of the non-English corpus is actually eligible

Of the corpus's **161 non-English `evidence_sources` rows** (by `lang_detected`), only **21 carry a DOI at
all**:

| category | count |
|---|---|
| Non-English, DOI-bearing (eligible for this method) | 21 |
| Non-English, no DOI (structurally ineligible — see below) | 140 |

The 140 without a DOI break down by `evidence_type` as: `code` 60, `national_fw` 49, `standard_eb` 16,
`grey` 6, `clinical` 5, `co1` 4. This is expected and not a data-quality problem: national building codes,
government standards, and ministerial regulations — which is most of what this whole non-English recovery
effort has been adding across batches 1-8 — are not journal literature and are essentially never assigned
DOIs or indexed by CrossRef/OpenAlex. Citation-graph mining doesn't apply to a building code any more than
it applies to a statute; there is no "reference list" or "cited-by count" for a regulation in these
databases. Inserting 140+ `citation_mining` rows that all say "not applicable, no identifier" would be
mechanical padding, not a real finding — recorded here as a documented scope statement instead.

Of the 21 DOI-bearing rows, **4 were already handled in earlier sessions**: REF-00107 and REF-00493 have
completed backward+forward CrossRef/OpenAlex mining (`backward=1, forward=1`); REF-00700 and REF-00702 are
already deferred with `DEFERRED-T3: Tier 3 mining is not mandatory`. That left **17 DOI-bearing refs (22
slug-links, since some refs are linked to multiple slugs)** genuinely untouched.

## What happened when this session tried to mine them

Before writing off the remaining 17, this session tested actual network reachability to the 3 services the
established method depends on — not just assumed the WebFetch outage would also apply:

```
curl https://api.crossref.org/works/...        -> CONNECT tunnel failed, response 403
curl https://api.openalex.org/works/doi:...     -> CONNECT tunnel failed, response 403
curl https://api.semanticscholar.org/graph/...  -> CONNECT tunnel failed, response 403
```

Cross-checked against the environment's own proxy-status endpoint (`$HTTPS_PROXY/__agentproxy/status`),
each attempt is logged as a `recentRelayFailures` entry: `"kind": "connect_rejected", "detail": "gateway
answered 403 to CONNECT (policy denial or upstream failure)"` for all 3 hosts. This is the **same root
cause** as the `WebFetch` outage documented in every batch of this recovery effort (`global-south-finding.md`,
`equity-dashboard.md`) — a session-wide outbound-network-policy block, not a per-source or per-service
problem. It is consistent with the corpus's own history: REF-00107 and REF-00493's existing `citation_mining`
rows show CrossRef/OpenAlex calls *did* succeed in an earlier session (`session_2026-05-23...`), so this is
specifically a **this-session** infrastructure condition, not a permanently broken method.

**No citation mining was performed or approximated this session.** A `WebSearch`-based substitute (e.g.
searching for a paper's title plus "cited by") was deliberately not used as a stand-in — it would not
reproduce the table's established `backward`/`forward` semantics (a real CrossRef reference count vs. an
OpenAlex cited-by count) and risks recording something that looks like real citation-graph data but isn't,
which is exactly the kind of category error the project's anti-fabrication discipline exists to prevent.

## What this migration actually did

Added 22 honestly-deferred `citation_mining` rows (one per slug-link of the 17 untouched DOI-bearing refs),
each carrying the source's real DOI and a `deferred_reason` explaining precisely what was tested, what
failed, and why (`DEFERRED-NETWORK-BLOCKED`). This mirrors the existing convention already used by most of
the table's 107 pre-existing rows (real, specific `deferred_reason` text rather than silence) and gives a
future session with working egress an exact, ready-to-run list rather than having to rediscover it.

## Recommendation

- **For a future session:** confirm `api.crossref.org` / `api.openalex.org` reachability first (the same
  control-URL discipline already used for `WebFetch` in this effort), then re-run
  `scripts/probes/citation_mining_pipeline.py` against the 17 refs listed in this migration's `notes`.
  Given DIN standards' DOIs resolve through Beuth Verlag's registered `10.31030` prefix, several of the
  17 (the DIN 18040-series rows) are plausible real CrossRef records, not just journal articles — worth
  prioritizing.
- **Escalate the network-egress block itself**, not just the `WebFetch` symptom of it — this session's
  finding (CrossRef/OpenAlex/Semantic Scholar all blocked, in addition to arbitrary `WebFetch` targets)
  suggests the block is a general outbound-HTTPS policy rather than anything specific to the `WebFetch`
  tool, which changes what "fixed" would look like for whoever investigates it.
- **Don't expand citation-mining `citation_mining` rows to the 140 no-DOI sources mechanically.** If a
  future session wants blanket coverage recorded, a single aggregate note (as in this document) is more
  honest and useful than 140 near-identical migration rows; the real path to more non-English coverage for
  those sources is fresh primary research (per `research-handoff-non-english.md`'s pipeline), not citation
  mining, which doesn't apply to them by construction.
