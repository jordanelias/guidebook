---
name: citation-miner
description: >
  Backward and forward citation mining for confirmed Tier 1–3 sources in the guidebook
  evidence base. Runs in two modes: INLINE (triggered automatically by research skills
  when a source is confirmed) and BATCH (standalone pass over all unmined sources in a
  slug or globally). Depth-1 only — mine references of each source but never recurse
  into discovered sources within the same session. Tracks all mining in SQLite via
  db.py CLI. Produces bibliography-ready output. ALWAYS use when asked to: mine citations,
  find related sources, trace citation networks, expand evidence base, generate bibliography.
  Trigger on: "citation mining", "mine references", "cited by", "backward citations",
  "forward citations", "expand evidence base", "bibliography", "unmined sources".
---

**Model:** Sonnet-class + web search
**Connectors:** PubMed (required), Scholar Gateway (preferred for forward), Consensus (optional). CrossRef via web_fetch acceptable for backward when PubMed lacks the record. Activate for mining.
**SQLite:** `data/guidebook.db` via `scripts/db.py`

---

## 0. Connector availability (read BEFORE mining)

Before any mining pass, probe connector availability:

- **PubMed** — required for verification. If unavailable, ABORT the mining pass and log `[GAP — PubMed connector unavailable]`. Do NOT proceed with web-search-only verification (high fabrication risk per GAP-278).
- **Semantic Scholar Graph API** (via `web_fetch` to `api.semanticscholar.org/graph/v1/paper/DOI:{doi}/citations`) — **preferred for forward mining.** This is a genuine citation-graph "cited by" endpoint, public, no auth required. Use it as the default forward-mining method for any DOI-bearing anchor.
- **Scholar Gateway** — its `semanticSearch` tool is topical/semantic passage retrieval, **not a citation graph**. It does not reliably return actual citing papers (confirmed empirically 2026-07-20 — spot-checked results were topically similar but did not verifiably cite the anchor; see DR-2026-07-20-citation-mining-methodology-corrections.md). **Do not use it for forward mining.** It remains useful as a supplementary topic-context search, same caveats as PubMed `find_related_articles` below.
  If neither Semantic Scholar nor Scholar Gateway is reachable, mark `forward = 0` and populate `deferred_reason` with `"no citation-graph connector available — forward mining DEFERRED"`. **Do NOT substitute PubMed topic search for forward mining** — that is the topic-evidence vs claim-evidence anti-pattern PI standing rule #7 fights. PubMed `find_related_articles` is word-weighted similarity, not actual citers; it is not a forward-mining substitute.
- **Consensus** — optional supplement for backward mining when CrossRef ref list is empty (e.g., conference abstracts).
- **CrossRef** (via `web_fetch` to `api.crossref.org`) — preferred for backward mining when the source has a DOI. Authoritative for the reference list of any DOI-bearing publication.
- **Direct document fetch** (`web_fetch`/`curl`, DOI not required) — backward mining is **not gated on having a DOI or a connector**. It only requires the source document itself, read for its own reference list. This works identically regardless of language — see §2 non-DOI sub-protocol. Do not mark a non-DOI source `backward = 0`/deferred without first fetching the actual document.

**Partial-availability rule:** If only PubMed + CrossRef are available, complete backward mining and mark forward DEFERRED with the reason above. A citation_mining row with `backward = 1`, `forward = 0`, and `deferred_reason` set is a VALID partial-mining state. A row with `backward = 0` AND `forward = 0` AND no `deferred_reason` is a PROTOCOL VIOLATION (see GAP-283).

---

## 1. Two Modes

### INLINE mode (called from research skills)

When multilingual-research, functional-deficit-researcher, economics-researcher, or
literature-review-planner confirms a Tier 1–3 source:

1. Calling skill passes: `(slug, local_ref_id, doi)`
2. Citation-miner checks:
   ```bash
   python3 scripts/db.py is-mined --slug {slug} --ref {global_ref_id}   # GLOBAL REF-NNNNN, not the label
   ```
   Returns: `{"mined": false}` or `{"backward": 0/1, "forward": 0/1, ...}`
3. If already mined (both B+F) → skip, return
4. If unmined or partial → mine missing direction(s)
5. Log result:
   ```bash
   python3 scripts/db.py log-mining \
     --slug {slug} \
     --ref {global_ref_id} \
     --direction backward \
     --connections '["CON-NNNN","CON-NNNN"]' \   # the ids you actually created
     --session {session_filename}
   ```

   > **`--ref` TAKES THE GLOBAL `REF-NNNNN`, NOT THE PER-SLUG LABEL. CORRECTED
   > 2026-08-24, and this instruction is where the defect came from.** It read
   > `--ref {local_ref_id}`, so `log_mining` wrote a label into the pointer column
   > and left `global_ref_id` NULL. On 2026-08-23 a batch followed it and
   > `source_slug_links` ended up holding `RAP-06/09/10` while `citation_mining`
   > held `RAP-F61/F69/F70` for the same three sources — after which
   > `get_unmined_sources()` reported REF-00561, REF-00969 and REF-00970 as never
   > mined, and the next session would have re-mined finished work.
   >
   > `--doi` is **removed**. The DOI is reachable through the reference id; copying
   > it had already drifted 2 of 10 rows by case. The label is looked up from
   > `source_slug_links`, which owns it — never invented at the call site.
   Run once per direction (backward, then forward as separate calls).
6. Return discovered sources to calling skill

**Depth-1 enforced:** discovered sources are recorded but NOT mined in the same pass.

### BATCH mode (standalone)

When citation-miner is invoked directly:

1. Query unmined sources:
   ```bash
   # All slugs, Tier 1-3:
   python3 scripts/db.py unmined --tier-max 3
   # Single slug:
   python3 scripts/db.py unmined --slug {slug} --tier-max 3
   ```
2. For each: mine backward + forward, log both directions
3. After completing all sources in a slug:
   ```bash
   python3 scripts/db.py update-bpc --slug {slug} --citation-mining-complete 1 --session {session}
   ```
4. Report: total mined, new sources discovered, remaining unmined

**Depth-1 enforced:** discovered sources added to evidence_sources but NOT mined this run.

---

## 2. Mining Protocol

### Backward Mining (reference list)

**DOI-bearing sources:**
1. Retrieve reference list via DOI → CrossRef (preferred), PubMed, or Semantic Scholar
2. Filter for relevance (§3)
3. For each relevant reference:
   - Verify existence (CrossRef record / PubMed / Semantic Scholar lookup)
   - Classify evidence tier
   - Check if already in evidence_sources (dedup by DOI, case-insensitive)
   - If new: INSERT into evidence_sources + source_slug_links
   - discovery_method field: `backward_from:{local_ref_id}`

**Non-DOI sources (grey literature, standards, government/NGO documents — non-English or otherwise):**
Backward mining is **not blocked by the absence of a DOI**. It requires only the source document itself:
1. Fetch the source's URL. **If the URL resolves to an organisation homepage, product page, or other non-document landing page — browse the site** (publications/reports/research sections) before concluding there is nothing to mine. A landing page means you're one click from the real document, not that it doesn't exist. Confirmed this recovers real bibliographies in the majority of cases where it was tried (see DR-2026-07-20).
2. Fetch the actual document (report, handbook, guideline PDF, etc.) and read its own reference list / cited-sources section, in whatever language it's written. This is language-agnostic — a document's own citations are just as extractable in Norwegian or Japanese as in English.
   - If `web_fetch`'s markdown conversion fails on a binary PDF (returns a "binary content saved to..." message), download it directly (`curl`) and extract text locally with `pdfminer.six` or `pypdf`. If the sandbox's `cryptography`/`cffi` binding is broken (a `ModuleNotFoundError: _cffi_backend` / pyo3 panic), `pip install --force-reinstall cffi` resolves it.
3. Filter for relevance (§3), verify each candidate against whatever record exists for it (CrossRef if it later turns out to have a DOI; otherwise the citing document itself, plus one independent corroborating source where feasible — e.g. a web search confirming the cited report's real authorship/publisher), classify tier, dedup, insert.
4. If the document genuinely has no reference list of its own (a practice checklist, a statutory text, a product page) — that's a legitimate NULL RESULT once actually verified by fetching it, not a deferral. Deferral is for documents you could not access (paywall, 403, genuinely no mirror found), not for documents you haven't tried to fetch yet.
5. **Do not default `evidence_type` to `grey` because a source is non-English or non-DOI.** Grey literature is a publication-type classification (informally published, non-peer-reviewed), independent of language. Check the actual venue — a journal article, monograph, or dissertation in any language is not grey literature just because it isn't in CrossRef. Verify the publisher/journal/institution before assigning `evidence_type`.

### Forward Mining (cited by)
1. Semantic Scholar Graph API `citations` endpoint for the anchor's DOI (preferred — see §0). Scholar Gateway `semanticSearch` is not a substitute (topical, not citation-graph).
2. Filter for relevance (§3)
3. For each relevant citing paper: same protocol as backward, discovery_method: `forward_from:{local_ref_id}`
4. Non-DOI anchors generally cannot be forward-mined (no index to query "who cites this non-indexed document") — mark `forward` DEFERRED with that reason unless a citing relationship is found incidentally (e.g. a later document in the same domestic literature that names it).

---

## 3. Relevance Filter

**Include** if ANY:
- Same population + built environment element as input source
- OT clinical evidence (Tier 1) for same spec domain
- Lived experience data for same population
- Systematic review covering input topic

**Exclude** if ANY:
- Pure clinical without built environment application
- Duplicate: pre-check the DOI against `evidence_sources.doi` (rule R9 — if it
  exists, cross-file the existing `ref_id`, never duplicate). With no DOI, try the
  other stable identifiers (`pmid`, `pmcid`, `isbn`, `issn`, `handle`, `url`),
  then normalised title + `pub_year` + `v_evidence_authors.first_author_last`
  (the `evidence_sources` column of that name is a tombstone since migration 063
  and reads NULL — screen on the view or every source looks new).
  *There is no dedup-key column.* This line named `doi_less_key`, which was  <!-- [RETIRED-VOCAB-OK] -->
  dropped from the schema — as §4 of this same file already says, two screens
  down. Two answers to one question is the disease; the §4 note is the true one.

---

## 4. SQLite Schema Reference

### evidence_sources — `add-source` logical fields (current schema)
The `db.py add-source` CLI takes **logical** fields that map to the real columns:
`--year → pub_year`, `--title → pub_title`, plus
`--doi, --pmid, --tier, --evidence-type, --jurisdiction, --slug, --local-ref-id`.

**AUTHORS ARE ROWS, NOT A STRING — changed 2026-08-24, migration 063.** `--authors` no
longer maps to `author_display`; that column and its four companions
(`first_author_last`, `first_author_first`, `author_count`, `is_corporate_primary`) are
**writer-retired tombstones on `evidence_sources` and read NULL**. Who wrote a source has
one home, `evidence_source_authors`, and `v_evidence_authors` derives the display form
from it.

- `--author 'Payne|Sarah R.'` — **preferred**, repeatable, in byline order. Keeps the
  given name. `--author 'corp|World Health Organization'` for a corporate author.
- `--authors "Payne S; Galbrun L"` — still accepted and parsed into rows, but the display
  form holds initials where the row holds a given name, so it stores less. Anything it
  cannot split into surname + initials is **refused, not guessed at**, and nothing is
  written. Use `--author` for those.
- A source with no authors is refused outright. There is no display column left to write
  instead. If the work has no named author, file the issuing body as a corporate author.

**Note:** the live `evidence_sources` table has **no** `authors`/`year`/`title`/`doi_less_key`  <!-- [RETIRED-VOCAB-OK] -->
columns (it uses `pub_year`, `pub_title`, …). Run `.schema evidence_sources` for the full
layout. The `--year`/`--title` mapping was restored 2026-06-22 (audit F-17) — earlier it
crashed with "table evidence_sources has no column named authors".

### source_slug_links columns
`ref_id, slug, local_ref_id`

### citation_mining columns
`slug, local_ref_id, global_ref_id, doi, backward, forward, connections_produced, notes`

### Adding new sources
```bash
python3 scripts/db.py add-source \
  --ref-id {global_ref_id} \        # REF-NNNNN, from dbcore.next_ref_id(conn) -- the high-water mark is the UNION of every table holding a ref_id, NOT source_locators alone (CLAUDE.md §4)
  --author "{last}|{given}" \      # repeatable, byline order; 'corp|{name}' for a body
  # or, from a display string: --authors "{authors}"   (parsed into rows; refuses ambiguity)
  --year {year} \
  --title "{title}" \
  --tier {tier} \
  --doi {doi} \
  --jurisdiction {jur} \
  --lang-detected {iso_639_1_code} \
  --lang-detection-method {native_title_verified|journal_family_inference|citing_document_language} \
  --slug {slug} \
  --local-ref-id {local_ref_id} \   # the per-slug LABEL (RAP-04). A different thing.
  --session {session}
```

**`--ref-id` and `--local-ref-id` are not the same value, and this block said they were
until 2026-08-24.** It read `--ref-id {local_ref_id}`, which files the source under its
per-slug label: `evidence_sources.ref_id='RAP-04'`. There is no CHECK on that column, so
it inserts silently — and the row is then invisible to the `source_locators` high-water
mark, collides with the next slug that mints an `RAP-04`, and renders a citation keyed to
a label that means nothing outside one slug. `db.py add-source` now refuses a ref_id that
is not a global reference id, and names this confusion when it does.

- `--ref-id` is the **global** reference id, `REF-NNNNN`, unique across the repository.
  There is no allocator: `dbcore.next_ref_id(conn)` IS the rule — the high-water mark is the
  UNION of every table holding a ref_id, NOT `source_locators` alone (CLAUDE.md §4). Corrected
  2026-09-03: line 191 of this same file was swept on 2026-09-02 and this line, 24 lines below
  it, was not — so the file taught the superseded rule while citing the section that calls it
  wrong. Measured: `source_locators` tops out at REF-00970 and `evidence_sources` at REF-00978,
  so the old rule mints REF-00971, a live evidence row.
- `--local-ref-id` is the **per-slug label**, `RAP-04`, meaningful only inside `{slug}`.

This is the same copy-versus-pointer confusion that put `RAP-F61/F69/F70` in
`citation_mining` while `source_slug_links` held `RAP-06/09/10` for the same three
sources, and reported them UNMINED after they had been fully mined.

**`--lang-detected` is REQUIRED, not optional, for every `add-source` call — not just when the slug's focus is non-English.** Before 2026-07-20 this field was silently unsettable (missing from the CLI/column whitelist entirely), which meant no citation-mining discovery — including genuinely non-English ones — was taggable by language. That makes the source invisible to any future language-prioritized query, silently defeating the point of ever running a non-English-focused pass. Use `native_title_verified` when you've read the actual title/text in that language; `journal_family_inference` when inferring from publishing in the same venue as a confirmed-language source (lower confidence — say so); `citing_document_language` when extracted from a bibliography written in that language.

---

## 5. Bibliography Output

Query for bibliography generation:
```sql
SELECT es.ref_id, va.author_display, es.pub_year, es.pub_title, es.doi, es.tier,
       es.jurisdiction,
       GROUP_CONCAT(DISTINCT ssl.slug) as slugs,
       cm.backward, cm.forward
FROM evidence_sources es
LEFT JOIN v_evidence_authors va ON va.ref_id = es.ref_id
LEFT JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
-- On the REFERENCE ID, not local_ref_id: that per-slug label is copied into both tables
-- and has already drifted here (RAP-06/09/10 vs RAP-F61/F69/F70 for the same sources).
LEFT JOIN citation_mining cm ON cm.global_ref_id = es.ref_id AND cm.slug = ssl.slug
GROUP BY es.ref_id
ORDER BY va.first_author_last COLLATE NOCASE, es.pub_year
```

Format:
```
[{ref_id}] {authors} ({year}). {title}. DOI: {doi}
  Tier: {tier} | Jurisdiction: {jurisdiction}
  Slugs: {slugs} | Mining: B={backward} F={forward}
```

---

## 6. Depth-1 Rule (hard constraint)

Mine references OF the source ✓ · Mine citations OF the source ✓ · Record new sources ✓
Mine references of discovered sources ✗ NEVER · Mine citations of discovered sources ✗ NEVER

**Why (corrected 2026-07-20 — see DR-2026-07-20-citation-mining-methodology-corrections.md):**
Not fabrication risk — a discovery at hop 3 is exactly as verifiable against a real connector as one at hop 1, as long as it's actually checked. The real reasons are:
- **Branching factor.** Backward + forward mining of 10 anchors in one pass produced 62 new candidate sources. Recursing into those at the same rate compounds geometrically per hop, not incrementally.
- **Relevance drift.** Each hop away from the original anchor weakens the link between "real, verified paper" and "actually relevant evidence for the claim this slug needs" — the project's topic-evidence-vs-claim-evidence anti-pattern (rule #7), which gets worse with distance, not better.

Depth-1 is the boundary where verification, relevance, and (where applicable) language focus stay tractable together. Going deeper is a real option for a narrowly-scoped, explicitly-approved pilot — not a default.

---

## 6a. Citation-mining is not a substitute for multilingual-research (corrected 2026-07-20)

The DOI-connector half of this skill (CrossRef backward, Semantic Scholar forward) is **structurally English-dominant**, independent of where you start: researchers worldwide disproportionately publish their DOI-indexed, internationally-discoverable work in English specifically so it gets picked up by these indexes. Running this skill's connector-based mining on a non-English-tagged anchor will mostly surface English discoveries — not because the technique is broken, but because that's what the index looks like.

This does **not** mean citation-mining can't produce non-English discoveries — §2's non-DOI sub-protocol (fetch the actual document, read its own citations) is fully language-agnostic and works fine, demonstrated repeatedly 2026-07-20. But it means:
- Don't expect the automated connector path to do non-English discovery for you.
- For genuinely new non-English coverage (not just mining what's already in the DB), `multilingual-research`'s native-language search protocol — Keyword Compendium, direct Co-1/Tier-2/Co-2 publication-page retrieval in-language — is the primary tool, not this one.
- Run citation-miner on non-English sources *after* multilingual-research (or another skill) has surfaced them, using the §2 non-DOI fetch-and-read path.

## 7. Integration with Research Skills

All research skills MUST invoke citation-miner inline for every confirmed Tier 1–3 source:
1. Research skill confirms source + assigns tier
2. Calls citation-miner inline with `(slug, local_ref_id, doi)`
3. Citation-miner: `is-mined` check → mine if needed → `log-mining`
4. Returns new sources to research skill
5. Research skill includes new sources in LOG output

---

## 8. Session Report

```markdown
## Citation Mining Summary — {date}
**Mode:** {inline|batch}
**Sources processed:** {N}
**New sources discovered:** {N}
**Connections produced:** [{CON-IDs}]
**Slugs now fully mined:** [{list}]
**Remaining unmined (Tier 1–3):**
```sql
-- On the REFERENCE ID, not local_ref_id. This query joined on the per-slug label and
-- was missed by the 2026-08-24 sweep that corrected the other three in this file.
SELECT COUNT(*), ssl.slug FROM evidence_sources es
JOIN source_slug_links ssl ON es.ref_id = ssl.ref_id
LEFT JOIN citation_mining cm ON cm.slug = ssl.slug AND cm.global_ref_id = es.ref_id
WHERE es.tier IN (1,2,3) AND (cm.global_ref_id IS NULL OR cm.backward=0 OR cm.forward=0)
GROUP BY ssl.slug ORDER BY COUNT(*) DESC
```
