# Archived prior-version working material

**Owner ruling 2026-09-09**, same ruling and same mechanics as `_archived/references/README.md` —
read that file for what archiving does and does not buy, and for why origin paths are mirrored.

## What is here

The v9 mobile-app prototype, the July pilot, the May evidence-migration workings, and two
per-item complete-provision drafts. All are keyed on or built around the item layer the owner
deleted on 2026-09-01.

## One live caller was repointed rather than retired

`scripts/audit/register_integrity_check.py` defaulted to `working/pilot/pilot-renderings.html`.
Its `DEFAULT_DOC` now points here. The check asserts the **I1–I5 register invariants**
(`governance/evidence-architecture.md` §6), which are live doctrine, and the pilot is still their
**only** subject — `specifications` holds 0 rows, so nothing else renders a determination yet.
When real render output exists, point `--html` at that instead: a check whose only subject is
archived content is one step from vacuous (`CLAUDE.md` §5a).

## What deliberately did NOT move

`claims-docket.md` — live, and the subject of the `claims_docket` check.
