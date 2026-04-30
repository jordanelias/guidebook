# Jurisdiction Philosophy
**Status:** CANONICAL — A8 Session 1
**Phase:** Stage A Phase 8 — Jurisdiction philosophy
**Created:** 2026-04-29 19:30 UTC
**Doctrinal basis:** project-standards Core Doctrine (L20–21) · jurisdiction-tracker SKILL.md · `schemas/enums.py` JurisdictionCode · project-standards L121

---

## 1. The 24-jurisdiction approach

### 1.1 Canonical jurisdictions

The guidebook's evidence base covers 24 countries plus 2 meta-jurisdictions. This list was confirmed at A3 and is encoded in `schemas/enums.py` JurisdictionCode.

| Code | Country | Region | Selection rationale |
|---|---|---|---|
| AU | Australia | Oceania | AS 1428 series; strong evidence base |
| BD | Bangladesh | South Asia | Global South representation; CRPD early signatory |
| BR | Brazil | South America | NBR 9050; largest LATAM market |
| CA | Canada | North America | NBC/CSA B651; strong OT profession |
| CH | Switzerland | Europe | SIA 500; multilingual context |
| CN | China | East Asia | GB 50763; largest population |
| DE | Germany | Europe | DIN 18040; aging population research |
| DK | Denmark | Scandinavia | BR18; universal design tradition |
| EG | Egypt | MENA | Egyptian Building Code; MENA representation |
| FR | France | Europe | CEREMA; detailed prescriptive standards |
| ID | Indonesia | Southeast Asia | Global South; largest SE Asian population |
| IE | Ireland | Europe | Part M; small-market model |
| IN | India | South Asia | Harmonised Guidelines; 1.4B population |
| JP | Japan | East Asia | Barrier-Free Law; aging society leader |
| KE | Kenya | East Africa | Sub-Saharan representation |
| KR | South Korea | East Asia | Barrier-Free Certification |
| NG | Nigeria | West Africa | Sub-Saharan representation |
| NL | Netherlands | Europe | Bouwbesluit/NEN 9120; progressive policy |
| NO | Norway | Scandinavia | TEK17/SINTEF; universal design policy |
| NZ | New Zealand | Oceania | NZS 4121; Pacific model |
| SE | Sweden | Scandinavia | BFS/ALM 2; Tier 5 evidence |
| SG | Singapore | Southeast Asia | BCA Code; compact-city model |
| UK | United Kingdom | Europe | BS 8300; Approved Document M |
| US | United States | North America | ADA 2010/ICC A117.1; largest evidence base |
| ZA | South Africa | Southern Africa | SANS 10400-S; middle-income model |

Meta-codes:

| Code | Scope |
|---|---|
| ISO | ISO international standards (ISO 21542, ISO 23599, IEC 60118-4) |
| EU | European Union directives and harmonized standards (EN 17210) |

### 1.2 Selection criteria

The 24 jurisdictions were selected to satisfy four coverage criteria:

1. **Geographic diversity** — all inhabited continents represented; Global South ≥8 jurisdictions
2. **Regulatory model diversity** — prescriptive codes (FR, SG), performance-based codes (AU, NZ), hybrid (UK, US), minimal/emerging (BD, KE, NG)
3. **Evidence-base strength** — jurisdictions with the strongest built-environment accessibility research (US, UK, AU, CA, JP, SE, NO, NL)
4. **Population scale** — the 24 jurisdictions collectively represent >5 billion people

### 1.3 What the 24-jurisdiction approach does NOT do

- **Does not claim these 24 are the "best" codes.** The selection is a coverage strategy, not a ranking.
- **Does not exclude other jurisdictions' evidence.** If Tier 1–3 clinical evidence comes from a non-canonical jurisdiction (e.g., Finland, Austria, Turkey), it is cited. The 24-jurisdiction requirement applies to code/standards research (Tier 4–6), not to clinical evidence.
- **Does not treat all 24 equally.** Per-jurisdiction tier coverage records track what evidence exists for each jurisdiction. Some jurisdictions will have rich standards evidence; others will have thin or no data for specific parameters.

---

## 2. Jurisdiction and evidence tier relationship

### 2.1 Codes are Tier 6

Per Core Doctrine: "Codes are Tier 6: the compliance floor, not the aspiration." This means:

- A code value establishes what the minimum legal standard is in that jurisdiction
- A code value does NOT establish best practice
- Code consensus (many jurisdictions agreeing on the same value) is stronger than a single code but weaker than Tier 4–5 standards or Tier 1–3 clinical evidence
- A BPC best_practice_synthesis derived solely from code consensus is in error (project-standards L20)

### 2.2 Standards are Tier 4–5

International standards (ISO, IEC, EN) with an evidence basis are Tier 4. National beyond-code frameworks (BS 8300-2 Annex G, SINTEF guidelines, NEN/NL WMO-keuken) are Tier 5. Both outrank codes but are below clinical evidence and Co-1/Co-2.

### 2.3 Per-jurisdiction tier coverage

Every BPC entry's jurisdiction-coverage section records the research status for each of the 24 jurisdictions:

| Field | Values | Meaning |
|---|---|---|
| `status` | SEARCHED, THIN, NO-DATA, NOT-RUN | Research status for this jurisdiction on this parameter |
| `co1_attempted` | bool | Whether Co-1 evidence was searched for this jurisdiction |
| `tier5_attempted` | bool | Whether Tier 5 (beyond-code framework) evidence was searched |
| `tier6_attempted` | bool | Whether Tier 6 (code) evidence was searched |

A BPC entry is PROVISIONAL until all 24 jurisdictions are recorded AND the Co-1 pass covers ≥9 languages.

---

## 3. Standards currency

### 3.1 Standards-registry

`references/standards-registry.md` tracks the currency of all cited standards. Each jurisdiction-standard pair has a YAML entry with status: CURRENT, UPDATED, SUPERSEDED, WITHDRAWN.

The jurisdiction-tracker skill (Sonnet 4.6, run once per edition) performs the currency check via web search of issuing bodies. The output validator (§5) ensures the entries are well-formed.

### 3.2 Standard supersession handling

| Status | Action |
|---|---|
| CURRENT | No action |
| UPDATED | Check figures still consistent with guidebook values; note newer edition in bibliography |
| SUPERSEDED | Must update citation and check for value changes before publication |
| WITHDRAWN | Author decision: find replacement standard or remove citation with rationale |

### 3.3 UK convention

The project uses `UK` instead of `GB` (ISO 3166-1 alpha-2) per project convention. This is documented in the JurisdictionCode enum docstring and enforced by the validator.

---

## 4. Validator specification

### 4.1 validate_jurisdiction.py scope

| Check | Severity | Description |
|---|---|---|
| Valid code | ERROR | Every jurisdiction code resolves to JurisdictionCode enum |
| UK not GB | ERROR | `GB` appearing as a jurisdiction code is rejected; must be `UK` |
| Standards-registry format | ERROR | Each entry in standards-registry.md has all required fields |
| Standards-registry status | WARNING | SUPERSEDED entries flagged for author action |
| BPC jurisdiction coverage | WARNING | BPC files with <24 jurisdiction records flagged |
| Source-jurisdiction consistency | WARNING | EvidenceSource.jurisdiction resolves to JurisdictionCode or is null |

### 4.2 convert_jurisdictions.py scope

Converts jurisdiction data from standards-registry.md YAML entries into validated entity records under `data/jurisdictions/`. Each record:

```yaml
jurisdiction: "AU"
standards:
  - standard_cited: "AS 1428.1:2021"
    current_version: "AS 1428.1:2021"
    status: "CURRENT"
    last_checked: "2026-03-18 23:30"
```

---

## 5. Jurisdiction-tracker output validator

Validates output from the jurisdiction-tracker skill before it is committed to standards-registry.md:

| Check | Severity | Description |
|---|---|---|
| Required fields | ERROR | Each entry has jurisdiction, standard_cited, current_version, status, last_checked |
| Status enum | ERROR | Status is one of CURRENT, UPDATED, SUPERSEDED, WITHDRAWN |
| Date format | ERROR | last_checked matches YYYY-MM-DD HH:MM |
| Jurisdiction code | ERROR | jurisdiction resolves to JurisdictionCode enum or is a full country name mappable to a code |
| Duplicate detection | WARNING | Same jurisdiction-standard pair appearing twice with different statuses |

---

## 6. Status

| Field | Value |
|---|---|
| Created | 2026-04-29 19:30 UTC |
| Phase | Stage A Phase 8 (Jurisdiction philosophy) — Session 1 |
| Status | CANONICAL |
| Forward dependencies | validate_jurisdiction.py, convert_jurisdictions.py (this session) |

---

**End of A8 governance document.**
