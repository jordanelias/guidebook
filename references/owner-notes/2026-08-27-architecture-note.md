# Owner architecture note — 2026-08-27

**Provenance.** Supplied by the owner as a document (`.docx`/`.pdf`) during
`session_2026-08-27-hook-audit`, and transcribed here **verbatim, structure preserved**, because it
is now the governing statement on the pipeline's shape and existed nowhere in the repository.

**Status.** The owner has stated its nature explicitly: *"these nonexistent tables are because the
document is just a proposal for what tables to make and why."* It is a **proposal for structure**,
not a census of what exists — and per `CLAUDE.md` rule 0 its rulings supersede prior records on
contact.

**It stops at Judgment.** Synthesis, specification and render are not in it. That is not a retraction
of the 2026-08-27 six-stage ruling; the note is simply partial.

---

## Verbatim

- Base
  - base.models
    - catalogues models and frameworks for disability like Kawa Model for occupational therapy or Convention on the Rights of Persons with Disabilities
  - base.building
    - lists all building typologies
    - lists all architectural and design elements involved in buildings
  - base.topics
    - exhaustive list of topics in accessibility ranging from categories like circulation and acoustics to more specific elements like ramp slopes, grab bar heights, hearing loops, contrast strips
  - base.taxonomy_medical
    - defining lived experience of disability by medical model
  - base.taxonomy_identity
    - defining lived experience of disability by social identity
  - base.taxonomy_icf
    - defining lived experience of disability by ICF codes for functional impairments
  - base.taxonomy_needs
    - defining lived experience of disability by access needs
  - base.clues
    - the ~825 DOI without correct metadata
  - base.sources
    - countries, international organizations like EU and UN, international standards like ISO
    - academic journals, research publishing bodies
    - professional practice, clinical guidelines
    - advocacy organizations
  - base.multilingual
    - terminology for all project-related definitions across all languages in jurisdictions
    - localizations and vernacular must be incorporated–direct English translations are insufficient
  - base.sources
    - lists all academic sources across many languages
- Research
  - research.matrix
    - works from an expansive matrix whereby searches are performed in manners akin to
      - base.taxonomy_x * base.building * base.jurisdictions
      - base.taxonomy_x * base.building * base.multilingual
      - base.topics * base.jurisdictions
      - base.topics * base.multilingual
      - base.clues
  - research.logs
    - logs all sources searched, failures to find, etc
- Evidence
  - logs all relevant items found in search with a unique reference ID, DOI/PMID and other codes if available, type of source (academic, code, professional practices, etc)
- Judgment
  - delivers a verdict on an evidence item for what tier of evidence hierarchy it belongs to (1, 2…6)
  - one evidence source may provide many rows of judgment (eg a code document like Canada's NBC 3.8)
  - determines category of judgment item, derives value/process/figure/goal for it

---

## Clarifications the owner gave on it the same day, each quoted

**On `base.sources` — it is a TARGET registry, not a corpus and not a defect:**

> *"academic publishing institutions, research journals, university publications, books and articles,
> etc are all 'sources' for finding evidence sources. so too are countries, codes and standards,
> professional organizations, clinical bodies, and advocacy groups. none of these are evidence, and
> none of these are research. they are all prompts for research to target such that they can find
> evidence"*

**On the medical model — it is ruled IN, as a user-selectable browsing lens:**

> *"yes we include the medical model too. we give our users the choice of what model they want to use
> to browse the site."*

**On relevance — it is an adjudication, not a property:**

> *"evidence states relevant items, and relevancy is something that must be adjudicated against a
> topic/category/concept"*

**On the aporia, and the overrule:**

> *"we have a fundamental issue where we do not want to presuppose
> categories/concepts/approaches/elements/techniques/practices by defining them all at the start of
> the project. however, we also can't perform our research properly if we don't presuppose all of
> those. so how do we go around this aporia?"*
>
> *"overrule Aug 24 DR. we go evidence>judgment>synthesis."*
>
> *"evidence is probably working by doing more cursory scans and grep/regex or whatever rather than
> line by line analysis, so it's probably just getting all required metadata for apa standards and
> listing out all concepts/topics/key words/phrases that appear in the source and then judgment phase
> will actually do the deep read on it to determine what can be derived from the source"*

**On parent columns:**

> *"yes, we need parent columns or however this would work with SQL terminology."*

---

## Measured against the live database, 2026-08-27 (`user_version` 64, read-only)

| note member | live table | rows |
|---|---|---|
| `base.models` | — | **absent** |
| `base.building` (typologies) | `rooms` | 17 |
| `base.building` (elements) | `items` | 93 |
| `base.topics` | `slugs` | 106 — **flat, no parent column** |
| `base.taxonomy_medical` | — | **absent** |
| `base.taxonomy_identity` | `populations` | 23 |
| `base.taxonomy_icf` | `axes` (→ `icf_demands`, §R8) | 17 |
| `base.taxonomy_needs` | `access_needs` | 17 |
| `base.clues` | `source_locators` | 875 — of which **448** carry a DOI, **251** a DOI with no title/authors |
| `base.sources` (targets) | — | **absent**; nearest is free-text `search_executions.engine` |
| `base.multilingual` | `term_aliases` (+ `terms`) | 2,382 (+88) |
| `base.jurisdictions` | — | **absent**; `jurisdiction` is an inert enum on 11 tables |
| `research.matrix` | — | no table; `v_coverage_priority` (7,208 rows) is one cross of it |
| `research.logs` | `search_executions` | 28 — **one distinct topic of 106** |
| Evidence | `evidence_sources` | 10 — **30 APA-shaped columns incl. `_en` variants** |
| Judgment | — | **absent**; `source_value_extractions` (0 rows) is its candidate |

**The `~825` does not reconcile with any live figure** — 875 clue rows, 448 with a DOI, 251 with a
DOI and no metadata. Recorded as a discrepancy, not resolved.
