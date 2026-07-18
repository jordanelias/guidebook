# L0 — Registry reconciliation & jurisdiction hygiene

*Deterministic pass, no external retrieval. Method: scan every `.md/.yaml/.json/.js/.jsx/.html` file in
the repo for `REF-\d{3,6}` tokens, diff against `evidence_sources.ref_id`, then classify each
cited-but-absent ref by where it is cited and whether the global reference registry
(`references/global-reference-registry.json`, 531 entries) knows it.*

## The "stranded refs" figure, corrected

The session summary carried "~37 stranded refs." The precise picture:

| bucket | count | meaning |
|---|---|---|
| cited-but-absent from `evidence_sources` | **53** | raw diff |
| — malformed / placeholder | **5** | `REF-404`, `REF-00999`, `REF-001`, `REF-002`, `REF-0557/0562` — not real refs |
| — well-formed `REF-#####` | **48** | of which… |
| — — cited in **live** provision/site content | **2** | `REF-00047` (in `_archived/…` — archived), `REF-00181` (live in `site/specs/f-07.html`) |
| — — cited only in **meta** (registry / audits / decisions / sessions) | **46** | the reconciliation backlog below |

So the **live** migration hole is ≈**1 ref** (`REF-00181`), not 37. The 46 meta-only refs are a
registry-reconciliation task, classified next.

## The 46 meta-only refs, classified

Cross-referencing the registry: **35 of 46 have a real registry entry** (title / DOI / URL) — genuine
evidence that was **registered but never migrated into `evidence_sources`**. **11 of 46 have no registry
entry** — cited only in session logs / decision records / audit manifests → **cruft** (session-internal
working ids), including the `REF-00999` placeholder.

**Bucket A — un-migrated genuine evidence (~35).** These carry real bibliographic data in the registry and
should be triaged for ingestion (verify → tier → language/jurisdiction-tag → link). **Priority within A =
the non-English and non-Anglophone-jurisdiction sources**, because they directly reduce the corpus skew the
equity mandate targets:

| ref | what the registry says | equity note |
|---|---|---|
| REF-00221 | 盲ろう者のコミュニケーション (deafblind communication) | **JP, Japanese** — un-migrated non-English |
| REF-00382 | GB 50763-2012 — 无障碍出入口 (accessible entrances) | **CN, Chinese** — un-migrated non-English |
| REF-00372 | Arrêté 20 avril 2017 + CEREMA — BIM accessibility | **FR, French** — "stricter threshold than baseline" |
| REF-00243 | Decree 241/2017 — Accessibility of the Built Env. | **FI, Finnish** |
| REF-00218 | DIN 18041:2016 — Hörsamkeit in Räumen | **DE** — *likely renumber-duplicate of DB `REF-00329`* (verify → registry stale, not a hole) |
| REF-00139 | Code on Accessibility 2025 ch.8 — wayfinding | "most comprehensive Asian wayfinding code" |
| REF-00184 / 00185 | CIBSE Guide A; CIE S 026/E:2018 | UK / international lighting metrology standards |
| REF-00154 / 00370 | BS 8300-2:2018; Approved Document M Vol 2 | UK access standards |
| REF-00001 / 00031 | room acoustics on speech; noise+reverberation SNR-50 at RT 0.3/0.6/0.8s | **acoustics — directly relevant to the A-18 pilot** |
| REF-00133 / 00253 / 00513 / 00232 / 00521 / 00490 / 00046 / 00183 | ME/CFS care guide; BATH-OUT; walking energetics; sensory-processing model; dementia cognition; MSE methods; melanopic EDI; wheelchair vibration | genuine clinical / grey primary — mixed jurisdictions |
| REF-00257 / 00455 | flagged **"[GREY — title unverified; DOI required before publication]"** | must clear verification before any use |
| REF-00052/00093/00106/00186/00369/00483/00504/00514/00529/00273/00182/00566-adjacent… | scoping reviews, cost data, grants, seating, hearing-loop governance, autism statutes | remainder of bucket A |

**Bucket B — cruft (~11):** `REF-00543, 00546, 00594, 00595, 00596, 00625, 00629, 00634, 00635, 00733,
00999`. No registry entry; cited only in session/decision/audit files. `REF-00999` is a known placeholder.
Approach: leave as historical session-internal ids; do **not** create evidence rows. (Verify none is a
typo'd real ref before final disposition.)

**The 1 live hole — `REF-00181`:** cited in `site/specs/f-07.html` (a live spec page) but absent from
`evidence_sources`; the registry has an entry. Approach: ingest/verify `REF-00181` and re-point the f-07
citation, **or** correct the citation if it is a typo. This is the only stranded ref touching rendered
content and should be resolved first.

## Jurisdiction hygiene (a real equity blocker)

`evidence_sources.jurisdiction` has **45 distinct values** with two defects that make the coverage matrix
uncountable until fixed:

1. **Seam:** `INT` (168) vs `INTL` (5) vs `EU` (5) — inconsistent codes for "international / supranational."
   Approach: normalize `INTL`→`INT`; keep `EU` distinct (it is a real supranational jurisdiction, not a
   synonym for global). Also `AU/NZ` (a compound tag) should be split or documented.
2. **19 null jurisdictions.** Approach: backfill from publisher/standard-number where determinable; where
   genuinely trans-national, tag `INT`; leave null only where truly unknown, and **record that** (S3).

These are proposed as a migration (`db/migrations/`), not applied here — L0 hygiene lands with the first
batch that depends on a countable coverage matrix.

## What this pass does NOT claim

Bucket assignment is by **registry presence + citation location**, not by per-ref re-retrieval. Whether each
bucket-A ref is truly un-migrated (vs. a renumber whose new id the registry didn't record, like the likely
REF-00218↔REF-00329 case) requires a per-ref verification during ingestion — that verification **is** the
migration work, and is owed, not done here.
