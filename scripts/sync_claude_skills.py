#!/usr/bin/env python3
"""Make skills/ loadable by the harness, by POINTING rather than copying.

WHAT IS BROKEN WITHOUT THIS. This repository carries 47 active skills as
`skills/<name>_SKILL.md`. Claude Code discovers skills at
`.claude/skills/<name>/SKILL.md` and nowhere else, so not one of them is
loadable: they are found only when an agent chooses to read them. That is the
exact failure `.claude/settings.json` blames for the 2026-07-24 research run --
"the rules did not fail; PROSE failed -- an agent must choose to load it, and
attention degrades as context fills" -- reproduced at the scale of 47 files.

WHY SYMLINKS AND NOT GENERATED COPIES. CLAUDE.md rule 5, owner ruling
2026-08-24: "It is better to have a table cell point to another table cell than
to rewrite." A generated copy of a skill body is the same fact in a second home;
it drifts the first time someone edits one side, and a parity check would only
make the dual home survivable, therefore permanent. A relative symlink has one
home and cannot drift. `skills/<name>_SKILL.md` stays the source of truth.

WHAT THIS SCRIPT WILL NOT DO. It never writes a `description`. A skill's
description is what the harness matches a task against, so a wrong one is worse
than a missing one -- it fires the skill on the wrong work. CLAUDE.md rule 8:
where judgment is genuinely required the script ASKS for it, constrained and
recorded, and never invents a value. Skills missing `name` or `description` are
reported by name with the line to add, and are not linked.

Usage:
    python3 scripts/sync_claude_skills.py            # create/refresh the links
    python3 scripts/sync_claude_skills.py --check    # exit 1 if out of sync
"""

import os
import pathlib
import re
import sys

SRC = pathlib.Path("skills")
DST = pathlib.Path(".claude/skills")


def frontmatter(text):
    """The YAML block between the opening '---' and the next '---', or ''."""
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    return text[3:end] if end > 0 else ""


def field(fm, key):
    """Value of a top-level scalar or folded key, '' when absent.

    Handles `description: >` and `description: >-` folded blocks, which four of
    these files use, by taking the indented continuation lines.
    """
    m = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
    if not m:
        return ""
    head = m.group(1).strip()
    if head not in (">", ">-", "|", "|-"):
        return head
    body, started = [], False
    for line in fm[m.end():].splitlines():
        if not line.strip():
            if started:
                break
            continue
        if line[:1] in (" ", "\t"):
            body.append(line.strip())
            started = True
        else:
            break
    return " ".join(body)


def survey():
    """(linkable, skipped) — skipped carries the reason, never a guess."""
    linkable, skipped = [], []
    for path in sorted(SRC.glob("*_SKILL.md")):
        stem = path.name[: -len("_SKILL.md")]
        fm = frontmatter(path.read_text(errors="ignore"))
        name, desc = field(fm, "name"), field(fm, "description")
        if not fm:
            skipped.append((stem, "no YAML frontmatter at all"))
        elif not desc:
            skipped.append((stem, "frontmatter carries no `description:`"))
        elif name and name != stem:
            skipped.append((stem, f"frontmatter name `{name}` != filename stem `{stem}`"))
        else:
            linkable.append((stem, path))
    return linkable, skipped


def main():
    check = "--check" in sys.argv
    if not SRC.is_dir():
        print(f"no {SRC}/ — nothing to do")
        return 0

    linkable, skipped = survey()
    stale = []
    DST.mkdir(parents=True, exist_ok=True)

    for stem, path in linkable:
        link = DST / stem / "SKILL.md"
        # Relative so the tree stays valid in any clone and in any container.
        target = os.path.relpath(path.resolve(), link.parent.resolve())
        current = os.readlink(link) if link.is_symlink() else None
        if current == target:
            continue
        stale.append(stem)
        if check:
            continue
        link.parent.mkdir(parents=True, exist_ok=True)
        if link.is_symlink() or link.exists():
            link.unlink()
        link.symlink_to(target)

    # A link whose source has gone is worse than no link: the skill lists a name
    # the harness cannot open.
    live = {stem for stem, _ in linkable}
    dangling = [d.name for d in sorted(DST.glob("*")) if d.is_dir() and d.name not in live]
    for name in dangling:
        if check:
            continue
        link = DST / name / "SKILL.md"
        if link.is_symlink() and not link.resolve().exists():
            link.unlink()
            link.parent.rmdir()

    print(f"EXAMINED: {len(linkable) + len(skipped)} skill file(s) in {SRC}/")
    print(f"  linked:  {len(linkable)}")
    print(f"  skipped: {len(skipped)}")
    for stem, why in skipped:
        print(f"    - {stem}: {why}")
    if skipped:
        print("\n  These are NOT a script bug. Each needs one line written by a human in")
        print("  skills/<name>_SKILL.md, inside the frontmatter, saying when the harness")
        print("  should reach for it:")
        print("      description: <when to use this skill, in one or two sentences>")
        print("  A wrong description fires the skill on the wrong work, so it is not derived.")
    if dangling:
        print(f"  dangling link(s): {', '.join(dangling)}")

    if check and (stale or dangling):
        print(f"\nOUT OF SYNC: {len(stale)} link(s) missing or wrong, {len(dangling)} dangling.")
        print("Run: python3 scripts/sync_claude_skills.py")
        return 1
    if check:
        print("\nIN SYNC.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
