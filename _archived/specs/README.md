# Archived hand-authored specification pages

## `e-08.html` — Corridor Clear Width, retired 2026-08-12

Owner instruction: *"specs/e-08.html this shouldn't exist anymore."* Frozen and archived here
rather than deleted, mirroring its origin path (`specs/`).

### What it was

A 135 KB **hand-authored** page — not generated from the database. It was the v10.5 exemplar that
`architecture/page-templates.md` §Facet-sequence reconciled Template 1 against, and the four "door"
entry points on the root `index.html` all opened it.

### Why it could not stay

`references/methodology/value-genealogy-worked-example-corridor-width.md` §7 audited it and found
the page **rests on an unregistered anchor**:

- It cites "Koontz 2017, DOI 10.1080/17483107.2016.1278470, n=42 two-pass corridor" plus a
  metabolic-cost claim that is **absent from `evidence_sources` and from the entire corpus** — the
  registered Koontz rows are propulsion-biomechanics papers.
- **All six** of its REF-IDs collide with unrelated canonical rows: REF-00237 "Koontz 2017" is
  Boverket BFS 2024:12 in the database; REF-00500 "ISO 21542" is a Korean daylighting paper;
  REF-00114 "BS 8300-2" is CAN/ASC 2.8:2025; REF-00200 "CSA B651-18" is IEC 60118-4; REF-00610
  "NBR 9050" is Property Council AU; REF-00390 "Steinfeld & Maisel 2012" is Lord 1993.
- It claims sourcing from `data/specifications/e-08.yaml`, **which does not exist**.

**That question is closed, and closing it is the point of the clean slate.** An earlier draft of
this README kept "is Koontz 2017 real?" as a queued lead. That was wrong. The corpus starts empty;
every source enters through the research contract, which pre-checks the DOI (R9) and re-retrieves
every locator (R10). A citation inherited from a retired, unprovenanced page is not a lead — it is
the unprovenanced artifact the reset exists to remove, and carrying it forward would let a deleted
page seed the new corpus. If a passing-width cohort study exists, an honest search finds it on its
own evidence. If it does not, we should not be holding a note that half-implies it does.

The page was the project's most prominent public surface while carrying values whose provenance had
already been shown not to resolve. The same document records **four coexisting "Guidebook values" for E-08**
(2440 best practice · 1800 divergence-matrix target · ≥1200 live item name · ≥1200/1500 on this
page), each with a different genealogy.

The 2026-08-06 clean-room reset then emptied the evidence corpus entirely, so nothing on the page
had a live source behind it at all.

### What replaced it

`site/specs/e-08.html` — generated from the database by `scripts/generate/build_site.py`, carrying
honest "not yet computed" banners instead of unsourced values. The six links on the root
`index.html` and the link templates in `scripts/generate/population_page.py` were repointed to it,
and the population pages regenerated.

`specs/e-08-brief.html` is a different file and is **not** retired here — the instruction named one
page. Note that `scripts/audit/check_rendered_docs.py` globs `specs/*.html` and currently reports
`EXAMINED: 0`, since `specs/` has been reference-only since the reset.

### What still points here

`architecture/page-templates.md` cites `site/specs/e-08.html` (the generated page), not this one.
`references/methodology/value-genealogy-worked-example-corridor-width.md` names this page as its
subject; that is the retirement's paper trail and is left as written, with a status note added. Its
§7 finding stands as a record of what the page contained — not as a research lead.

### Reading this directory

`_archived/**` is hidden from ripgrep by the root `.ignore` (`DR-2026-08-06-cold-storage-search-scope`).
`ls`, `Glob`, `git grep` and every Python tool see it normally.
