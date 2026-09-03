#!/usr/bin/env python3
"""Copy this container's agent transcripts into transcripts/ before they are lost.

WHY THIS IS A SCRIPT AND NOT A HABIT. Agent transcripts live in ~/.claude/projects,
which is ephemeral container storage. A remote session clones the repository fresh, so
NOTHING a previous session left there survives. On 2026-09-02 an antagonist ran
read-only, wrote nothing itself, and its entire workings existed only there; they were
preserved because the owner asked whether they had been lost, while the container still
held them. Earlier the same day a container restart killed an antagonist mid-run and
most of that pass went with it.

The conclusions of an adversarial pass are not a substitute for its workings. A finding
you cannot trace is a finding you cannot correct, and correcting them is the point.

IDEMPOTENT. Safe to run repeatedly and safe to run mid-session; a transcript still being
written is copied as far as it has got, and the next run overwrites it with more.

    python3 scripts/preserve_transcripts.py            # copy, print what changed
    python3 scripts/preserve_transcripts.py --check    # report only, exit 1 if stale
"""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(os.environ.get("GUIDEBOOK_TRANSCRIPT_ROOT",
                           Path.home() / ".claude" / "projects"))
OUT = Path("transcripts")


def _role_of(path):
    """Read the role out of the agent's OWN brief, never out of a filename.

    'ANTAGONIST' CONTAINS THE SUBSTRING 'AGONIST'. A naive match calls every antagonist
    an agonist, which it did once here before being caught, and a mislabelled adversarial
    transcript is worse than an unlabelled one: it silently reassigns who checked whom.
    So antagonist is tested first and the order below is load-bearing.
    """
    with open(path, errors="replace") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except Exception:
                continue
            msg = rec.get("message") or {}
            c = msg.get("content")
            if isinstance(c, str):
                text = c
            elif isinstance(c, list):
                text = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
            else:
                continue
            if not text.strip():
                continue
            head = text[:260].upper()
            for needle, role in (("ANTAGONIST", "antagonist"),
                                 ("AGONIST", "agonist"),
                                 ("TRACER", "tracer"),
                                 ("ADVERSARIAL CRITIC", "adversarial-critic"),
                                 # Added 2026-09-03: Fable's planning pass for the
                                 # thirty-defect programme came back labelled "other",
                                 # which is honest but useless -- the index exists so a
                                 # reader can find "the planner run" without opening
                                 # 666 KB of JSONL. Tested AFTER the four above, so a
                                 # brief that merely mentions planning cannot outrank
                                 # its own declared role.
                                 ("YOU ARE PLANNING", "planner"),
                                 ("PLANNER", "planner")):
                if needle in head:
                    return role
            return "other"
    return "other"


def _started(path):
    with open(path, errors="replace") as fh:
        for line in fh:
            try:
                ts = json.loads(line).get("timestamp")
            except Exception:
                continue
            if ts:
                return ts[:19]
    return "0000-00-00T00-00-00"


def _sessions(project_root):
    """Every harness session in this container: (session_id, main.jsonl, subagent dir)."""
    for main in sorted(project_root.glob("*.jsonl")):
        yield main.stem, main, project_root / main.stem / "subagents"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="report only; exit 1 if anything is unpreserved or stale")
    args = ap.parse_args()

    roots = [p for p in ROOT.glob("*") if p.is_dir()] if ROOT.exists() else []
    if not roots:
        print(f"  no transcript root under {ROOT}")
        print("  EXAMINED: 0")
        print("\n  INDETERMINATE — nothing to preserve, or the harness stores them")
        print("  elsewhere. That is not a pass; find out which before relying on it.")
        return 1

    examined, written, stale, stale_labels = 0, [], [], []
    for project_root in roots:
        for sid, main, subdir in _sessions(project_root):
            dest = OUT / f"harness_{sid[:8]}"
            pairs = [(main, dest / "main.jsonl")]
            for f in sorted(subdir.glob("agent-*.jsonl")) if subdir.exists() else []:
                name = (f"{_started(f).replace(':', '-')}_{_role_of(f)}"
                        f"_{f.name[6:14]}.jsonl")
                pairs.append((f, dest / "subagents" / name))

            # A BETTER ROLE DERIVATION MUST NOT LEAVE AN ORPHAN. The destination name
            # encodes the role, so improving _role_of renames the file -- and a plain
            # copy would leave the old name beside the new one, silently doubling a
            # 666 KB transcript and putting two rows in the index for one agent. Keyed
            # on the agent id, which is the one part of the name that never changes.
            wanted = {d.name for _s, d in pairs}
            subdir_out = dest / "subagents"
            if subdir_out.is_dir():
                for old_dst in subdir_out.glob("*.jsonl"):
                    aid = old_dst.name.rsplit("_", 1)[-1]
                    if old_dst.name not in wanted and any(
                            d.name.endswith(aid) for _s, d in pairs):
                        if not args.check:
                            old_dst.unlink()
                            written.append(f"(removed stale label) {old_dst}")
                        else:
                            stale_labels.append(str(old_dst))

            index = []
            for src, dst in pairs:
                examined += 1
                fresh = dst.exists() and dst.stat().st_size == src.stat().st_size
                if not fresh:
                    stale.append(str(dst))
                    if not args.check:
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src, dst)
                        written.append(str(dst))
                if dst.name != "main.jsonl":
                    index.append({"started": _started(src), "role": _role_of(src),
                                  "bytes": src.stat().st_size,
                                  "agent_id_prefix": src.name[6:14], "file": dst.name})
            if index and not args.check:
                dest.mkdir(parents=True, exist_ok=True)
                (dest / "index.json").write_text(
                    json.dumps(sorted(index, key=lambda r: r["started"]), indent=2),
                    encoding="utf-8")

    print(f"  EXAMINED: {examined} transcript(s) in this container")
    if args.check:
        if stale_labels:
            print(f"  STALE ROLE LABELS: {len(stale_labels)} (rerun without --check)")
            for s_ in stale_labels[:6]:
                print(f"      {s_}")
        if stale or stale_labels:
            print(f"  UNPRESERVED OR STALE: {len(stale)}")
            for s in stale[:8]:
                print(f"      {s}")
            print("\n  These exist ONLY in ephemeral container storage. Run this script")
            print("  without --check, and COMMIT the result, before the session ends.")
            return 1
        print("  All container transcripts are preserved under transcripts/.")
        return 0
    print(f"  WROTE: {len(written)}")
    for w in written[:12]:
        print(f"      {w}")
    if written:
        print("\n  NOT DONE UNTIL COMMITTED. transcripts/ is the only home that")
        print("  survives container reclamation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
