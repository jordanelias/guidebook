#!/usr/bin/env python3
"""Render decisions/DR-*.md from their register rows.

A DR is a VIEW of its register row, not a second copy of it (rule 5). Hand-writing one
is how the two drift; C9 exists because they did. Pass the decision ids and the slugs.
"""
import sys, textwrap, yaml

def wrap(t, width=96):
    out = []
    for para in str(t).split("\n"):
        out.append("\n".join(textwrap.wrap(para, width)) if para.strip() else "")
    return "\n".join(out)

def render(d, slug):
    owner = d["delegation"] == "DG-NON" and d["decided_by"] == "jordanelias"
    if owner:
        status = (
            "**Status:** **RATIFIED ON CONTACT** — this is an owner ruling, and `CLAUDE.md` rule 0 holds that\n"
            "a live owner statement supersedes every prior ratified record it touches **on contact**. Owner\n"
            "rulings do not await ratification; this record exists so the ruling is citable by the machine and\n"
            "findable by a reader, not to confer validity it already has."
        )
    else:
        status = (
            "**Status:** **ADOPTED, REVIEW PENDING** — a `DG-REVIEW` decision taken by a session under\n"
            "`CLAUDE.md` §1, which places code and tables outside the owner gate. It is landed and live; the\n"
            "review it awaits is the owner's, and `review_status` in the register is `PENDING` until then."
        )
    arts = [a for a in d["decision_artifacts"] if not a.startswith("decisions/DR-")]
    L = [
        f"# DR-{slug} — {d['summary']}", "", status, "",
        f"**Register row:** `{d['decision_id']}` · category `{d['category']}` · delegation `{d['delegation']}` ·",
        f"decided by `{d['decided_by']}` on {d['decision_date']} · `data/decisions/decision_register.yaml`", "",
        "> **This file is GENERATED from its register row.** Edit the register, not this file — two",
        "> hand-maintained copies of one decision is the dual home rule 5 forbids, and C9 exists to catch",
        "> exactly that drift.", "",
        "## Outcome", "", wrap(d["outcome"]), "",
        "## Rationale", "", wrap(d["rationale"]), "",
        "## Alternatives considered", "",
    ]
    for a in d["alternatives_considered"]:
        L.append(textwrap.fill(a, 96, initial_indent="- ", subsequent_indent="  "))
    L += ["", "## Notes, and what remains owed", "", wrap(d["notes"]), "",
          "## Delegation", "", wrap(d["delegation_rationale"]), "",
          "## Artifacts", ""]
    L += [f"- `{a}`" for a in arts]
    return "\n".join(L) + "\n"

if __name__ == "__main__":
    reg = yaml.safe_load(open("data/decisions/decision_register.yaml"))
    by = {d["decision_id"]: d for d in reg["decisions"]}
    for pair in sys.argv[1:]:
        did, slug = pair.split("=", 1)
        p = f"decisions/DR-{slug}.md"
        open(p, "w").write(render(by[did], slug))
        print("wrote", p)
