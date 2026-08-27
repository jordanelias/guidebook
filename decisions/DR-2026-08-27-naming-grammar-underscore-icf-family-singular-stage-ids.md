# DR-2026-08-27 — The naming grammar: underscore separator, `base_` prefix, parallel `base_taxonomy_*` names, the `icf_*` family, and singular stage ids

**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that
a live owner statement supersedes every prior ratified record it touches **on contact**. Owner
rulings do not await ratification; this record exists so the ruling is citable by the machine and
findable by a reader, not to confer validity it already has.

**Register row:** `D-0169` · category `D-SCHEMA` · delegation `DG-NON` ·
decided by `jordanelias` on 2026-08-27 13:52 · `data/decisions/decision_register.yaml`

> **This file is GENERATED from its register row.** Edit the register, not this file — two
> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch
> exactly that drift.

## Outcome

ADOPTED by owner selections 2026-08-27. Supersedes the dotted namespace of the architecture
note, the three-character stage_id[:3] prefix scheme, and the §R8 `demand_*` replacement family.

## Rationale

Underscore because SQLite has no schemas: a dot in an identifier collides with schema.table
syntax and would need quoting at every use site forever. Full-word prefixes also retire the
collision hazard found against three-character prefixes. The taxonomies keep parallel names
because the owner ruled "we have multiple taxonomies. respect that", which is also a bar on
folding. The ICF family takes icf_* throughout AND access_need_icf (43 rows) is renamed
access_need_icf_codes, because access_need_icf maps needs to ICF e-codes while the axes table
holds b/d codes -- leaving them one letter apart would recreate the `items` ambiguity
deliberately. The stage id is singular against the owner's own plural wording, so the prefix
matches the other six and the hand-off reads specification_items.

## Alternatives considered

- Keep the §R8 demand_* family -- rejected: it was derived from `icf_demands`, a noun the owner
has replaced, so the derivation no longer holds.
- icf_* without renaming access_need_icf -- rejected by the owner as inheriting a known
collision.
- Plural stage id `specifications_` as the owner first wrote it -- rejected for prefix
consistency; the plural remains the recorded wording of the spine ruling.

## Notes, and what remains owed

§R8's seven RETIRED tokens (axes, axis_code, item_axis_links, population_axis_map,
access_need_axis_map, serves_axes, attaches_axes) are unaffected -- they name what is retired,
not what replaces it.

## Delegation

Owner ruling. The pipeline shape, the project vocabulary and the research methodology are
judgements about the book, which governance/decision-protocol.md places in the DG-NON class and
CLAUDE.md rule 0 makes non-delegable.

## Artifacts

- `references/project-standards.md (entries dated 2026-08-27)`
