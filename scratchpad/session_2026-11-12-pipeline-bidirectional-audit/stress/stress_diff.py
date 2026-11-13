#!/usr/bin/env python3
"""Compare two stress-harness output folders step by step. The before/after proof for a behaviour-preserving change.

    python3 -I stress_diff.py <folder-A> <folder-B>

Each folder holds <part>/log.jsonl and <part>/scenarios.tsv (what stress_run.py / stress_run3.py write with --out).
A step is matched on (part folder, tag with its running counter `.NNN.` removed, occurrence number of that name within
the part): the counter shifts when a step is skipped, so the raw tag would report phantom differences. The ORDER of the
matched steps within a part is compared too (a swapped pair is one difference).

Compared, exactly: argv, rc, stdout, stderr, changed, canonical_moved.
Not compared: `expect` (prose written before the run), `at`, `seconds`, `cwd`, `db`, and `canonical_sha256` (the
sha of the tree under test: it legitimately differs between two branches when one carries a migration;
`canonical_moved`, whether the step moved it, is compared and is False on every step of a sound run).

Removed before comparing, exactly these and nothing else (there is no option to remove more; a difference is
reported, never normalised away):
  1. the output-folder prefix of each side's own argument, replaced by <OUT> (the path REMAINDER is kept, so a
     changed file name under it shows); and the temp-directory prefix (/tmp or tempfile.gettempdir()), replaced by
     <TMP> with the remainder kept
  2. 14-digit migration stamps (`20` followed by twelve digits), replaced by <STAMP>; only that token, so a
     changed name or extension around it shows
  3. the random part of a tool-chosen temp name, `reproducibility_<8 chars>.db` (mkstemp in migration_reproducibility)
  4. date-times YYYY-MM-DD HH:MM[:SS] (space or T) that fall inside the step's own run window, replaced by <NOW>: from
     two minutes before the part's first step to two minutes after the step's own `at` (UTC). These are the
     retired_at / created_at stamps the step itself writes. A date-time outside the window (a stored historical value,
     a --stamp argument) is compared as written.

Known limit: `changed` holds per-table ROW COUNTS (what stress_run.Run.step records), so an UPDATE, or a wrong value in
a column, is invisible unless the step's stdout or a later step echoes it. A per-table content digest would have to mask
the time-varying values in the rows, which is the very normalisation this tool keeps to two tokens.

A part that examined nothing is reported, never passed: `NOTHING-EXAMINED <part>: <reason>` when a side has no step that
ran a command (only read-only notes, e.g. a `.skip`), or when its log does not match its scenarios.tsv (the part died
or the log was cut). Exit codes: 0 identical; 1 differences; 2 no steps at all; 3 a part examined nothing (takes
priority over 1, differences are still printed).

Prints `DIFF <part> <step> [<field>]` with a few lines of unified diff per differing field, `DIFF <part> <step>: present
only in A|B` for an unmatched step, then `EXAMINED: <steps> step(s) in <parts> part(s); differing fields: <n>` (an
unmatched step, a changed order and a NOTHING-EXAMINED part each count as one).
"""
import calendar, difflib, json, os, re, sys, tempfile, time
from pathlib import Path

FIELDS = ("argv", "rc", "stdout", "stderr", "changed", "canonical_moved")
_TMP = "|".join(re.escape(p.rstrip("/")) for p in sorted({"/tmp", tempfile.gettempdir()}))
_TMP_PREFIX = re.compile(r"(?:%s)(?=/)" % _TMP)
_STAMP = re.compile(r"(?<!\d)20\d{12}(?!\d)")
_RAND = re.compile(r"reproducibility_[a-z0-9_]{8}\.db")
_DATETIME = re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?")
_SLACK = 120
_COUNTER = re.compile(r"^([^.]*)\.\d{3,}\.")
_NOTE_ARGV = ["<direct read-only query>"]


def utc(s):
    return calendar.timegm(time.strptime(s[:16].replace("T", " "), "%Y-%m-%d %H:%M"))


def norm(s, out_prefixes, window):
    for pre in out_prefixes:
        s = s.replace(pre, "<OUT>")
    s = _TMP_PREFIX.sub("<TMP>", s)
    s = _RAND.sub("reproducibility_<RAND>.db", s)
    s = _STAMP.sub("<STAMP>", s)
    return _DATETIME.sub(lambda m: "<NOW>" if window[0] <= utc(m.group(0)) <= window[1] else m.group(0), s)


def text(rec, field, out_prefixes, lo):
    v = rec.get(field)
    window = (lo - _SLACK, utc(rec["at"]) + 60 + _SLACK)  # `at` is the second the step ended; a minute-resolution stamp may read a minute early
    if field == "argv":
        return "\n".join(norm(str(x), out_prefixes, window) for x in (v or []))
    if field == "changed":
        return norm(json.dumps(v if v is not None else {}, sort_keys=True, ensure_ascii=False), out_prefixes, window)
    return norm(str(v if v is not None else ""), out_prefixes, window)


def load(folder):
    """({(part, name, occurrence): record}, {part: [keys in log order]}, {part: reason it examined nothing})."""
    recs, order, empty = {}, {}, {}
    for log in sorted(Path(folder).glob("*/log.jsonl")):
        part, seen, tags, ran, lo = log.parent.name, {}, [], 0, None
        order[part] = []
        for line in log.read_text().splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            tags.append(rec["tag"])
            ran += rec.get("argv") != _NOTE_ARGV
            name = _COUNTER.sub(r"\1.", rec["tag"], count=1)
            seen[name] = seen.get(name, 0) + 1
            lo = utc(rec["at"]) if lo is None else lo  # the part's first step
            rec["_lo"] = lo
            recs[(part, name, seen[name])] = rec
            order[part].append((part, name, seen[name]))
        tsv = log.parent / "scenarios.tsv"
        done = [l.split("\t", 1)[0] for l in tsv.read_text().splitlines()[1:]] if tsv.exists() else None
        if done is None:
            empty[part] = "no scenarios.tsv: the part did not finish"
        elif done != tags:
            empty[part] = "log does not match scenarios.tsv: the part died or the log was cut"
        elif not ran:
            empty[part] = "no step ran a command (only read-only notes)"
    return recs, order, empty


def label(key):
    part, name, k = key
    return f"{part} {name}" + (f" (occurrence {k})" if k > 1 else "")


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    pre = [sorted({str(Path(f)), os.path.join(os.getcwd(), f), os.path.abspath(f), str(Path(f).resolve())}, key=len, reverse=True) for f in sys.argv[1:3]]  # however the folder was spelled to the harness
    (a, oa, ea), (b, ob, eb) = load(sys.argv[1]), load(sys.argv[2])
    keys = sorted(set(a) | set(b))
    n = 0
    for key in keys:
        if key not in a or key not in b:
            print(f"DIFF {label(key)}: present only in {'A' if key in a else 'B'}")
            n += 1
            continue
        for f in FIELDS:
            x, y = text(a[key], f, pre[0], a[key]["_lo"]), text(b[key], f, pre[1], b[key]["_lo"])
            if x == y:
                continue
            n += 1
            print(f"DIFF {label(key)} [{f}]")
            d = list(difflib.unified_diff(x.splitlines(), y.splitlines(), "A", "B", lineterm="", n=0))
            for line in d[:10]:
                print("    " + line[:200])
            if len(d) > 10:
                print(f"    ... {len(d) - 10} more diff line(s)")
    for part in sorted(set(oa) & set(ob)):
        sa = [k for k in oa[part] if k in b]
        sb = [k for k in ob[part] if k in a]
        if sa != sb:
            n += 1
            print(f"DIFF {part}: step order differs")
            for line in list(difflib.unified_diff([label(k) for k in sa], [label(k) for k in sb], "A", "B", lineterm="", n=0))[:10]:
                print("    " + line[:200])
    bad = 0
    for side, e in (("A", ea), ("B", eb)):
        for part, why in sorted(e.items()):
            bad += 1
            n += 1
            print(f"NOTHING-EXAMINED {part} (side {side}): {why}")
    parts = {k[0] for k in keys}
    print(f"EXAMINED: {len(keys)} step(s) in {len(parts)} part(s); differing fields: {n}")
    sys.exit(2 if not keys else 3 if bad else 1 if n else 0)


if __name__ == "__main__":
    main()
