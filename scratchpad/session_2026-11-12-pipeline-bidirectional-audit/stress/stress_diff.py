#!/usr/bin/env python3
"""Compare two stress-harness output folders step by step. The before/after proof for a behaviour-preserving change.

    python3 -I stress_diff.py <folder-A> <folder-B>

Each folder holds <part>/log.jsonl (what stress_run.py / stress_run3.py write with --out). A step is matched on
(part folder, tag with its running counter `.NNN.` removed, occurrence number of that name within the part): the counter
shifts when a step is skipped, so the raw tag would report phantom differences.

Compared, exactly: argv, rc, stdout, stderr, changed. Not compared: `expect` (prose written before the run), `at`,
`seconds`, `canonical_sha256`, `cwd`, `db`.

Removed before comparing, exactly three things and nothing else (there is no option to remove more; a difference is
reported, never normalised away):
  1. absolute paths under /tmp/ or tempfile.gettempdir()
  2. date-times YYYY-MM-DD HH:MM[:SS] (space or T separator): created_at values and --stamp echoes
  3. 14-digit migration stamps (`20` followed by twelve digits)

Prints `DIFF <part> <step> [<field>]` with a few lines of unified diff per differing field, or
`DIFF <part> <step>: present only in A|B`, then `EXAMINED: <steps> step(s) in <parts> part(s); differing fields: <n>`
(an unmatched step counts as one). Exit 0 when n is 0, 1 when it is not, 2 when nothing was examined.
"""
import difflib, json, re, sys, tempfile
from pathlib import Path

FIELDS = ("argv", "rc", "stdout", "stderr", "changed")
_TMP = "|".join(re.escape(p.rstrip("/")) for p in sorted({"/tmp", tempfile.gettempdir()}))
_PATH = re.compile(r"(?:%s)/[^\s\"'\\,;:()\[\]{}<>|]*" % _TMP)
_DATETIME = re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?")
_STAMP = re.compile(r"(?<!\d)20\d{12}(?!\d)")
_COUNTER = re.compile(r"^([^.]*)\.\d{3}\.")


def norm(s):
    s = _PATH.sub("<TMP>", s)
    s = _DATETIME.sub("<DATETIME>", s)
    return _STAMP.sub("<STAMP>", s)


def text(rec, field):
    v = rec.get(field)
    if field == "argv":
        return "\n".join(norm(str(x)) for x in (v or []))
    if field == "changed":
        return norm(json.dumps(v if v is not None else {}, sort_keys=True, ensure_ascii=False))
    return norm(str(v if v is not None else ""))


def load(folder):
    """{(part, name, occurrence): record} for every <part>/log.jsonl under folder."""
    out = {}
    for log in sorted(Path(folder).glob("*/log.jsonl")):
        seen = {}
        for line in log.read_text().splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            name = _COUNTER.sub(r"\1.", rec["tag"], count=1)
            seen[name] = seen.get(name, 0) + 1
            out[(log.parent.name, name, seen[name])] = rec
    return out


def label(key):
    part, name, k = key
    return f"{part} {name}" + (f" (occurrence {k})" if k > 1 else "")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    a, b = load(sys.argv[1]), load(sys.argv[2])
    keys = sorted(set(a) | set(b))
    n = 0
    for key in keys:
        if key not in a or key not in b:
            print(f"DIFF {label(key)}: present only in {'A' if key in a else 'B'}")
            n += 1
            continue
        for f in FIELDS:
            x, y = text(a[key], f), text(b[key], f)
            if x == y:
                continue
            n += 1
            print(f"DIFF {label(key)} [{f}]")
            d = list(difflib.unified_diff(x.splitlines(), y.splitlines(), "A", "B", lineterm="", n=0))
            for line in d[:10]:
                print("    " + line[:200])
            if len(d) > 10:
                print(f"    ... {len(d) - 10} more diff line(s)")
    parts = {k[0] for k in keys}
    print(f"EXAMINED: {len(keys)} step(s) in {len(parts)} part(s); differing fields: {n}")
    sys.exit(2 if not keys else (1 if n else 0))


if __name__ == "__main__":
    main()
