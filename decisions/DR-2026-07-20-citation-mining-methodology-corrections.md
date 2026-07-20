# DR-2026-07-20 — Citation-Mining Methodology Corrections

**Status:** ACCEPTED (session-adopted; corrections applied directly to the skill during the same session that found them)
**Authored:** 2026-07-20 (session_2026-07-19-citation-mining-nonenglish — branch `claude/citation-mining-exhaustive-6t9y2f`)
**Doctrine SHA at authorship:** `373255e` (governance/mission-and-epistemics.md)
**Amends:** `skills/citation-miner_SKILL.md`
**Related:** `skills/multilingual-research_SKILL.md`, `scripts/db.py`

---

## Context

A citation-mining pass explicitly scoped to "non-English, Tier 1–3" surfaced five real methodology defects in `citation-miner_SKILL.md` and its supporting tooling — not data errors, but errors in what the skill told the operator to do. Each was caught by the requester questioning a specific claim or result during the session, not by internal review. All five are corrected in this DR and reflected in the skill file. Recorded here so the reasoning survives past this session, per this project's standing practice of not silently patching protocol.

---

## Corrections

### 1. The depth-1 rule's stated rationale was wrong

The skill said depth-1 exists because of "fabrication risk" on unverified chains. That doesn't hold: a source found at hop 3 is exactly as verifiable against a real connector as one found at hop 1. Verification quality does not degrade with depth as long as every discovery is checked against CrossRef / PubMed / a real citation-graph endpoint.

The real reasons to cap at depth-1 are cost and relevance drift, not fabrication:
- **Branching factor.** Mining 10 anchors both directions this session produced 62 new candidate sources. Recursing into those at the same rate is not incremental — it compounds geometrically per hop.
- **Topic dilution.** Every hop away from the original anchor weakens the link between "real, verified paper" and "actually relevant evidence for this guidebook's claims" — this is the project's own named topic-evidence-vs-claim-evidence anti-pattern (governance, rule #7), and it gets worse with distance, not better.

Corrected in §6.

### 2. Backward mining is not DOI-gated — it was being treated as if it were

The skill's backward-mining protocol (§2) reads "Retrieve reference list via DOI → CrossRef, PubMed, or Scholar Gateway," which was read (by this session, and probably by prior sessions) as "no DOI → not mineable." That's false. Backward mining only requires fetching the source document and reading its own reference list — completely language- and DOI-independent. Demonstrated directly this session: a Norwegian government guideline and a German KfW evaluation report, neither DOI-bearing, both yielded real, verified non-English discoveries once actually fetched and read.

The DOI→connector path is a *shortcut* available for indexed academic literature, not the only path. Corrected in §2 with an explicit non-DOI sub-protocol.

### 3. Landing pages were treated as dead ends instead of being browsed

When a source's URL resolved to an organisation homepage rather than a specific document, the session initially logged this as "not mineable" (deferred). Browsing the same sites for a publications/reports section found the actual cited document behind 4 of 5 homepages checked. A homepage is evidence you're one click from the real document, not evidence the document doesn't exist. Corrected in §2.

### 4. Non-English + non-DOI was being defaulted to `evidence_type = grey`

Grey literature is a publication-type classification (non-peer-reviewed, informally published) — it has nothing to do with language or DOI-indexing. A German dissertation, a peer-reviewed article in *Deutsches Ärzteblatt*, or a Japanese government research handbook are exactly as academic as an English-language, DOI-bearing equivalent; they're just not sitting in CrossRef. One source (a *Deutsches Ärzteblatt* article) was misclassified as `grey` this session before being caught and corrected. The fix is procedural: check the actual publishing venue (journal / publisher / institution) before assigning `evidence_type`, every time, regardless of language. Corrected in §3 (new relevance-and-classification note).

### 5. `lang_detected` was silently dropped on every new source

`scripts/db.py add-source` did not expose `lang_detected` / `lang_detection_method` in its CLI or column whitelist, so none of the sources discovered by this — or any prior — citation-mining session were taggable by language, even when the language was known with certainty. This makes any future "prioritize non-English" query blind to exactly the sources it should surface first. Fixed in `scripts/db.py` (CLI now accepts `--lang-detected`/`--lang-detection-method`); this session's 65 backfilled rows are corrected. Going forward this is a required field, not optional metadata. Corrected in §4.

### 6. Citation-mining's automated connectors are not a substitute for native-language search

Of 65 sources discovered this session via the automated CrossRef/Semantic-Scholar-connector path, only 2 were non-English — and those only because the anchor happened to sit inside a same-language domestic journal cluster (Japanese, Korean). Every other non-English discovery (Norway, Germany) came from manually fetching and reading an actual non-English *document*, not from any connector. This is structural: DOI-indexed citation graphs are English-dominant by construction, because that's the language researchers worldwide publish in when they want international indexing — independent of the paper's origin or the anchor's tagged language.

This doesn't make citation-mining useless for non-English work (correction #2 above shows backward mining works fine on any language once you have the document), but it does mean: **do not expect the DOI-connector half of this skill (CrossRef backward, Semantic-Scholar forward) to produce non-English discoveries on its own.** For genuine non-English coverage, `multilingual-research`'s native-language search protocol (Keyword Compendium, direct Co-1/Tier-2 publication-page retrieval) remains the primary tool; citation-miner should be run *opportunistically* on non-English sources multilingual-research surfaces, using the corrected fetch-and-read backward-mining path from correction #2. Corrected in §7 (integration note) and cross-referenced in `multilingual-research_SKILL.md`.

---

## Also fixed as part of this DR (tooling, not protocol)

- `scripts/db.py get_unmined_for_all_slugs()` queried a column (`es.title`) that hadn't existed since the schema migrated to `pub_title` — the unmined-sources backlog query was completely broken before this session. Fixed; also now sorts non-English sources first per the citation-mining priority ordering.
- Scholar Gateway's `semanticSearch` tool was being used for forward mining despite returning topical/semantic matches, not verified citing relationships — confirmed empirically this session (spot-checked results did not verifiably cite the anchor). Replaced with the public Semantic Scholar Graph API (`api.semanticscholar.org/graph/v1/paper/DOI:.../citations`), which is a genuine citation-graph endpoint. Scholar Gateway is downgraded to supplementary/topic-context use only; see §0 and §2.

---

## Non-decisions

This DR does not re-litigate the depth-1 cap itself (still in force — see corrected §6 rationale), and does not obligate a full re-run of prior citation-mining sessions' output. It corrects the skill going forward and documents that this session's own output (66 evidence_sources rows + 4 corrected classifications) was produced under the corrected understanding, not the original flawed one, except where explicitly noted (e.g. the two `journal_family_inference`-tagged sources, which are lower-confidence by design, not an error).
