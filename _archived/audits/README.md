# Archived audits — the superseded pipeline probe logs

**Retired by:** owner approval of 2026-08-14 ("APPROVE WHOLE TIER-1 BATCH"), against
`workplan/2026-08-14-remediation-workplan.md` §6, which lists "the duplicate probe logs" as safe to
retire and holds the newest one back.

## What is here

| File | Size |
|---|---|
| `2026-08-12-pipeline-probe-findings.json` | 1.2 MB |
| `2026-08-12-pipeline-probe-log.md` | 821 KB |
| `2026-08-12b-pipeline-probe-findings.json` | 1.2 MB |
| `2026-08-12b-pipeline-probe-log.md` | 823 KB |

Three probe runs happened on the same day — the unsuffixed one, `b`, and `c`. Each re-walked the
whole pipeline and each superseded its predecessor's findings. Carrying all three meant a session
grepping for a probe result got three answers of differing vintage with nothing in the filename
saying which was current, which is the same failure the root `.ignore` exists to prevent.

## What stayed live, and why

**`audits/2026-08-12c-pipeline-probe-log.md` and its findings JSON are NOT here.** The newest run is
the current one, and it is cited by a live plan: `workplan/2026-08-13-writer-plan.md:189` quotes it
verbatim **by line number** (`audits/2026-08-12c-pipeline-probe-log.md:12147`). Archiving it would
have broken a pinpoint citation in a plan that has not been executed yet.

That citation is also why nothing in this directory may be renumbered, reflowed, or edited: these are
dated records, frozen at their date, and the line-anchored citation into their sibling shows exactly
how a "tidy-up" edit turns a precise reference into a wrong one.
