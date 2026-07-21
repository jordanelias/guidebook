# DR-2026-07-21 — Rename entity codes `E-##` → `ENT-##` to end the item_code collision

**Status:** OPERATIVE — 2026-07-21.
**Decision by:** Owner directive 2026-07-21 ("that's bonkers … that needs to change. Fix it"), on finding A4 from this session's adjudication.
**Amends:** `governance/conceptual-model.md` (SIGNED OFF 2026-04-26) and the active governance/architecture/schema surfaces that reference entity codes.
**Closes:** finding A4 (entity-code vs item_code namespace collision).

---

## 1. The problem

The repo used `E-##` in **two unrelated numbering systems**:

- **Entity codes** (`governance/conceptual-model.md` §1): the 20 data-model *entity types*, `E-01`…`E-20`, where "E" meant **Entity**.
- **Item codes** (`items.item_code`): individual design parameters grouped into content categories **A–K**; category **E** is one of them, so its rows are `E-01`, `E-02`, … `E-15`.

The two collided across the whole 1–15 range. Worked examples:

| Code | Entity meaning | Item meaning |
|---|---|---|
| `E-01` | Specification (entity type) | Accessible Lift (parameter) |
| `E-02` | Evidence Source (core pipeline node) | Platform Lift |
| `E-08` | **Item** (entity type) | **Corridor Clear Width** — the flagship worked example (`evidence-architecture.md` §8.1) |
| `E-15` | Co-1 Collaborator (entity type) | Changing Places Facility |

`E-15` was *both* an entity code and a live item code, and `E-08` names both the Item entity and the corridor parameter that headlines the architecture doc — so a reader seeing `E-08` could not tell which namespace was meant. No mechanical breakage existed (the two live in different stores), but it is a standing trap for cross-referencing, querying, and any future website/API surface exposing these codes.

## 2. The decision

**Rename the entity-code namespace `E-## → ENT-##`.** Rationale for renaming *entities* rather than *items*:

- Entity codes are **documentation labels** in a bounded set of governance/architecture/schema files — not data keys.
- Item codes are **data keys** (`items.item_code`, foreign-keyed by `jurisdictional_values`, `item_bpc_links`, `item_population_links`, …) referenced across ~250 files (parts, site, references, sessions, data). Renaming them would be a high-risk data migration; renaming entities is a low-risk documentation change.

`ENT-##` is self-documenting ("ENT" = entity) and shares no prefix with any item category (A–K).

## 3. Scope applied (this DR)

Surgical, per-occurrence (entity refs only; every item_code left untouched — verified):

| File | Change |
|---|---|
| `governance/conceptual-model.md` | 53 entity codes → `ENT-##`; namespace note + amendment marker added |
| `governance/pipeline-contract.yaml` | spine string + collection anchor (`ENT-01/02/03/08`) |
| `governance/armature_v4_integration.md` | 11 entity refs (`ENT-12/19/20`) |
| `architecture/schema-spec.md` | `ENT-20` (Question) |
| `architecture/d0139-amendment-2.md` | `ENT-20` (Question, ×2) |
| `schemas/evidence_source.py` | docstring ref `(ENT-03)` |
| `schemas/room.py` | `Entity ENT-17` (line 9); item_code `E-06` on line 23 **left untouched** |
| `schemas/question.py` | docstring ref `(ENT-20)` |

**Caller sweep:** 0 residual entity `E-##` in the renamed active files; `schemas/item.py` / `schemas/room.py` item_codes confirmed intact.

## 4. Scope deliberately excluded (and why)

- **All `items.item_code` references, everywhere** — the collision is resolved by moving the *entity* side; item codes are correct as-is.
- **Append-only / historical records** — `sessions/`, `_archived/`, dated `references/audits/*` reports, and prior `decisions/` DRs are left exactly as written. Rewriting past records contradicts the repo's forward-only, immutable-record convention (the same principle `DR-2026-07-13-attestation-rule-identifier-registry-gap` invoked to refuse retroactive attestation edits). Their `E-##` mentions are frozen history read in their original context, not live references.

A future session may, if the owner wishes, sweep remaining *active* (non-historical) `E-##` entity mentions in `references/` that this DR did not reach; none are known to be load-bearing.

## 5. Consequences

- **No entity semantics changed.** Codes are relabelled; the entities, relationships, and statuses are identical.
- **No code behavior changed.** Entity codes are documentation labels, not data keys — no schema column, query, or migration depends on them. Item_code-driven behavior is untouched.
- The collision is eliminated at its definitional source and across active governance/architecture/schema surfaces; `conceptual-model.md` now carries a namespace note so the split is explicit going forward.
