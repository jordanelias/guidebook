# Slug Registry
**Managed by:** research-log-manager
**Purpose:** Canonical list of all research slugs. Authoritative for CHECK/LOG/RETRIEVE path resolution.

---

## Slug → Topic Directory Map

| Slug | Topic directory | SL path | BPC path | Status |
|---|---|---|---|---|
| `pain-ofs-built-environment-design` | `health-and-symptom-management` | `references/search-log/health-and-symptom-management/pain-ofs-built-environment-design.md` | `references/bpc/health-and-symptom-management/pain-ofs-built-environment-design.md` | ACTIVE |
| `threshold-door-hardware` | `entrances-and-circulation` | `references/search-log/entrances-and-circulation/threshold-door-hardware.md` | `references/bpc/entrances-and-circulation/threshold-door-hardware.md` | ACTIVE |

---

## Topic Directory Index

| Directory | Anticipated slugs |
|---|---|
| `entrances-and-circulation` | threshold-door-hardware, door-width-clearance, corridor-width, ramp-gradient, step-nosing |
| `health-and-symptom-management` | pain-ofs-built-environment-design, retreat-reset-room, thermal-regulation |
| `bathrooms-and-wet-areas` | shower-bathing-geometry, grab-bar-configuration, toilet-transfer-clearance |
| `kitchens-and-workspaces` | kitchen-counter-height, sink-clearance, workspace-ergonomics |
| `wayfinding-and-signage` | (VIS, DEAF, DEM, DBL slugs) |
| `seating-and-rest` | seating-interval, rest-points, recline-seating |
| `sensory-environment` | lighting, acoustics, olfactory |
| `communication-and-alerts` | (DEAF, DBL slugs) |

---

## Instructions for research-log-manager

**CHECK:** Normalise slug → look up in table above → GET path from SL path column → parse status.  
**LOG:** Normalise slug → look up topic dir → PUT to SL path and BPC path → update this registry if new slug.  
**RETRIEVE:** Normalise slug → look up BPC path → GET → return inline.  
**New slug:** Add row to table. Assign topic dir. Create both SL and BPC files. Update this registry.

**Flat files retired:** `references/search-log.md` and `references/best-practices-compendium.md` are frozen archives. Do not read or write them.
