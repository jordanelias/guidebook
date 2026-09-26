#!/usr/bin/env python3
"""Update batch 20's attestation after the independent pass and the owner's rulings."""
import json
P = "attestations/sessions_session_2026-09-25-research-batch-20-audit-cluster-templer-fhwa.json"
with open(P, encoding="utf-8") as f:
    a = json.load(f)
prs = a["per_rule_status"]
prs["integrity-protocol"]["reason"] = (
    "Every database change went through the sanctioned path: a scratch copy under GUIDEBOOK_DB_PATH, db.py "
    "verbs only (driven by the scripts persisted in scratchpad/<session>/w01-w16), captured by "
    "emit_batch_sql.py, emitted by emit_data_migration.py, applied by migrate_db.py. Three data migrations "
    "-- the batch; a fix-forward from the self-administered adversarial pass; and a second fix-forward "
    "carrying the independent antagonist's sustained findings and the owner's four rulings of 2026-09-25 -- "
    "plus one schema migration (096, the EXHAUSTED disposition the owner ruled for, a table rebuild "
    "generated from the live DDL). No committed migration was edited. Where the CLI could not reach a "
    "column the corrections needed, the verb was added and a gap filed rather than hand SQL written: "
    "resolve-candidate --suggested-slug (GAP-045), link-admission (GAP-046), amend-population-match and "
    "amend-term (GAP-047), each closed fixed. migrate_db --rebuild reproduces every row this batch wrote; "
    "the only drift is the scheduled bot's direct writes to REF-01006 and pipeline_runs, which predate the "
    "branch. REF-01002's author correction remains blocked by a writer gap (GAP-044) and was not bypassed.")
# Guarded (2026-09-26 review): an attestation shaped differently would KeyError here.
alog = prs.setdefault("adherence-logging-and-attestation", {})
alog["reason"] = alog.get("reason", "") + (
    " P2b was first scored falsified; the independent pass showed Table 20's endorsement of 1:12 is "
    "qualified by curb height, so it is rescored as held.")
a["deviations"] = [
    {
        "rule": "adherence-logging-and-attestation",
        "reason": (
            "The /adversarial command requires an INDEPENDENT critic so that one model does not check its own "
            "work. This batch ran as a subagent without an agent-launching tool, so it first ran a "
            "self-administered pass (seven defects, six repaired). The independent antagonist was then "
            "dispatched by the coordinating session over PR #159; its transcript is "
            "transcripts/harness_34e8c762/subagents/2026-09-25T05-15-51_adversarial_a1efd54a.jsonl. It found "
            "defects the self-pass missed, among them: a qualified claim stated unqualified (footnote c "
            "'more permissive'); untested table cells typed as primary measurements; a true statement in "
            "GAP-037 'corrected' into a false one; a hand-typed independence count; and a provenance edge I "
            "reasoned my way out of writing. The sustained findings are repaired in the second fix-forward "
            "and listed in the session record's section 0b. The deviation stands as recorded: the batch's "
            "own close claimed more than the independent pass allowed.")
    },
    {
        "rule": "source-discipline",
        "reason": (
            "One Unpaywall request carried the owner's email address in its URL, following the project's "
            "earlier Unpaywall calls rather than asking first. It is disclosed in the session record and was "
            "not repeated. The owner has since ruled (2026-09-25) that no personal email goes to Unpaywall or "
            "any similar third-party API; the committed instances stay, since history is not rewritten.")
    },
    {
        "rule": "source-discipline",
        "reason": (
            "My pre-write quote checks called retrieval_log.quote_in_artefacts and tested the (found, detail) "
            "tuple for truth, which is always true, so those pre-checks were vacuous. Re-run correctly, every "
            "verbatim claim_text in the batch is found and only the declared verbatim-exempt transcriptions "
            "are not. db.py's own write-time check unpacks the tuple and was not affected.")
    },
]
a["independent_reviewer_counterclaim"] = (
    "The independent review has now happened, and it bore the counterclaim out: the claims I most wanted to "
    "be true were the ones it broke. It qualified the footnote-c inference that was the batch's headline; "
    "showed that the Table 20 cells I leaned on were untested recommendations sitting on the wrong side of the "
    "report's own acceptability line; and showed that I had described REF-01008 as a laboratory study while "
    "its Part II held field data on 1:12. What a reviewer could still say: the four points sent to the owner "
    "were ruled on, but the independence view still counts absences as roots (GAP-048), three minted terms "
    "carry open vocabulary questions (GAP-033), and REF-01008's curb-ramp rows are still filed on a parameter "
    "built on building ramps, which the setting field says and a reader skimming values will not see.")
# One write, closed by the context manager, trailing newline included -- not three
# unclosed handles that relied on CPython refcounting to flush.
with open(P, "w", encoding="utf-8") as f:
    f.write(json.dumps(a, indent=2, ensure_ascii=False) + "\n")
print("ok")
