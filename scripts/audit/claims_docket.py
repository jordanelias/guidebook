#!/usr/bin/env python3
"""
scripts/audit/claims_docket.py — Mode-2 live claims docket (skills/integrity-protocol_SKILL.md).

Scans the working diff's added prose for claim-trigger patterns and maintains a
docket the author must annotate with a warrant before commit:

  generate [--base REF] [--docket PATH]   scan added lines in changed md files;
                                          append NEW triggered claims to the docket
                                          (existing annotations preserved)
  check    [--docket PATH]                exit 1 while any docket line lacks a
                                          warrant annotation
  --selftest                              mutation-test this scanner (fires on
                                          synthetic triggers; passes on clean text)

Docket line format (pipe-separated, one claim per line):
  <file>:<line> | <trigger-class> | <excerpt> | <ANNOTATION>
Valid annotations (Mode-1 warrant vocabulary):
  VERIFIED-BY: <command/artifact>   RECOUNTED: <command>   PREDICTED
  REPORTED-BY: <source>             N/A: <reason>
An empty fourth field = unannotated = check fails.

Empirical basis for the trigger classes: of the 41 adversarial-review findings
(2026-07-12/13), the recurring defect classes in prose were false absolutes/
totals, verification verbs outrunning artifacts, and unmarked quantities whose
caveats had been stripped. This scanner is a mechanical floor, not a proof:
a claim phrased outside the lexicon escapes it — additions belong here,
versioned.
"""
import argparse
import os
import re
import subprocess
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DEFAULT_DOCKET = os.path.join(REPO_ROOT, "working", "claims-docket.md")

TRIGGERS = [
    ("absolute", re.compile(
        r"\b(all|none|never|only|every|first|complete(?:ly)?|entire(?:ly)?|"
        r"nothing|nowhere|always|zero)\b", re.I)),
    ("total", re.compile(r"\b\d+\s*(?:of|/)\s*\d+\b|\ball\s+\*{0,2}\d+\*{0,2}\b", re.I)),
    ("verification-verb", re.compile(
        r"\b(verified|demonstrated|confirmed|preserved|proven|validated|"
        r"tested|re-?run|byte-identical|reproduc\w+|checks? pass\w*)\b", re.I)),
    ("quantity", re.compile(r"\b\d+(?:\.\d+)?\s*(?:mm|m|lux|dB|Hz|%|°C?|N(?:·m)?)\b")),
]
ANNOT_RE = re.compile(
    r"^(VERIFIED-BY:.+|RECOUNTED:.+|PREDICTED\b.*|REPORTED-BY:.+|N/A:.+)$")
SCAN_DIRS = ("decisions/", "governance/", "references/", "workplan/", "skills/",
             "sessions/", "audits/", "architecture/")


def changed_md_added_lines(base):
    """(file, new-lineno, text) for added lines in changed .md files vs base."""
    out = subprocess.run(
        ["git", "diff", "--unified=0", base, "--", "*.md"],
        capture_output=True, text=True, cwd=REPO_ROOT).stdout
    results, fname, lineno = [], None, 0
    for raw in out.splitlines():
        if raw.startswith("+++ b/"):
            fname = raw[6:]
        elif raw.startswith("@@"):
            m = re.search(r"\+(\d+)", raw)
            lineno = int(m.group(1)) if m else 0
        elif raw.startswith("+") and not raw.startswith("+++"):
            if fname and fname.startswith(SCAN_DIRS):
                results.append((fname, lineno, raw[1:]))
            lineno += 1
    return results


def scan(lines):
    """Yield (file, lineno, trigger-class, excerpt) for triggered claims."""
    for fname, lineno, text in lines:
        stripped = text.strip()
        if not stripped or stripped.startswith(("|--", "```", "<!--")):
            continue
        classes = [name for name, rx in TRIGGERS if rx.search(stripped)]
        if classes:
            excerpt = re.sub(r"\s+", " ", stripped)[:140]
            # Docket lines are themselves pipe-delimited (file:line | class | excerpt |
            # annotation); a source line that's a markdown table row carries its own "|"
            # characters, which would shift cmd_check's parts[3] lookup and misreport a
            # real annotation as missing (or, in principle, mis-parse a bogus one as
            # valid). Substitute a lookalike so the docket format's own delimiter stays
            # unambiguous regardless of what the scanned source line contains.
            excerpt = excerpt.replace("|", "¦")
            yield fname, lineno, "+".join(classes), excerpt


def load_docket(path):
    entries = {}
    if os.path.exists(path):
        for raw in open(path):
            parts = [p.strip() for p in raw.split("|")]
            if len(parts) >= 3 and ":" in parts[0] and not raw.startswith("#"):
                key = (parts[0], parts[2])
                entries[key] = parts[3] if len(parts) > 3 else ""
    return entries


def cmd_generate(base, docket_path):
    lines = changed_md_added_lines(base)
    existing = load_docket(docket_path)
    new = 0
    rows = []
    for fname, lineno, classes, excerpt in scan(lines):
        key = (f"{fname}:{lineno}", excerpt)
        annot = existing.get(key, "")
        # a matching excerpt at any location keeps its annotation (line drift)
        if not annot:
            for (loc, exc), a in existing.items():
                if exc == excerpt and a:
                    annot = a
                    break
        if not annot:
            new += 1
        rows.append(f"{fname}:{lineno} | {classes} | {excerpt} | {annot}")
    os.makedirs(os.path.dirname(docket_path), exist_ok=True)
    with open(docket_path, "w") as f:
        f.write("# Claims docket — Mode 2, skills/integrity-protocol_SKILL.md\n"
                "# Annotate the 4th field: VERIFIED-BY:/RECOUNTED:/PREDICTED/"
                "REPORTED-BY:/N/A: — `claims_docket.py check` gates on it.\n"
                + "\n".join(rows) + ("\n" if rows else ""))
    print(f"docket: {len(rows)} triggered claims ({new} unannotated) -> {docket_path}")
    return 0


def cmd_check(docket_path):
    if not os.path.exists(docket_path):
        print(f"no docket at {docket_path} — run generate first (or nothing to check)")
        return 0
    bad = []
    n = 0
    for raw in open(docket_path):
        if raw.startswith("#") or not raw.strip():
            continue
        n += 1
        parts = [p.strip() for p in raw.split("|")]
        annot = parts[3] if len(parts) > 3 else ""
        if not ANNOT_RE.match(annot):
            bad.append(f"  {parts[0]}: {parts[2][:80]}  [annotation: {annot!r}]")
    if bad:
        print(f"FAIL: {len(bad)}/{n} docket claims lack a valid warrant annotation:")
        print("\n".join(bad))
        return 1
    print(f"PASS: {n}/{n} docket claims carry warrant annotations")
    return 0


def selftest():
    """Mutation discipline: the scanner must FIRE on synthetic triggers and stay
    quiet on clean text; check must FAIL on unannotated and PASS on annotated."""
    ok = True
    synthetic = [
        ("decisions/x.md", 1, "This covers all 14 records, none omitted."),
        ("governance/y.md", 2, "The exclusion was verified by query and preserved."),
        ("references/z.md", 3, "Corridors of 2440 mm serve signing pairs."),
        ("references/z.md", 4, "A neutral sentence with no trigger words here."),
    ]
    hits = list(scan(synthetic))
    fired = {h[0] for h in hits}
    ok &= ("decisions/x.md" in fired)  # absolute + total
    ok &= ("governance/y.md" in fired)  # verification verbs
    ok &= any(h[0] == "references/z.md" and h[1] == 3 for h in hits)  # quantity
    ok &= not any(h[1] == 4 for h in hits)  # clean line stays quiet
    print(f"{'FIRED' if ok else '**MISSED**'}: scanner on synthetic triggers "
          f"({len(hits)} hits; clean line quiet)")
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
        f.write("# docket\n"
                "a.md:1 | absolute | all 14 records | \n"
                "b.md:2 | quantity | 2440 mm | VERIFIED-BY: sqlite query\n")
        p = f.name
    fail_fired = cmd_check(p) == 1
    print(f"{'FIRED' if fail_fired else '**MISSED**'}: check fails on unannotated line")
    with open(p, "w") as f:
        f.write("a.md:1 | absolute | all 14 records | RECOUNTED: grep -c PROPOSED decisions/\n"
                "b.md:2 | quantity | 2440 mm | VERIFIED-BY: sqlite query\n")
    pass_ok = cmd_check(p) == 0
    print(f"{'PASS' if pass_ok else '**FAIL**'}: check passes on annotated docket")
    os.unlink(p)
    ok &= fail_fired and pass_ok

    # Regression test for the table-row pipe-parsing bug: a scanned source line
    # that is itself a markdown table row carries its own "|" characters, which
    # (pre-fix) shifted cmd_check's pipe-delimited parts[3] lookup and made a
    # correctly-annotated claim misreport as unannotated. Adversarial-pass
    # finding, C2 execution register: the original selftest never exercised
    # this path, so a regression here would have shipped silently.
    table_row_source = [("workplan/t.md", 5, "| Q1 | some verified claim with all details | note |")]
    table_hits = list(scan(table_row_source))
    excerpt_clean = bool(table_hits) and "|" not in table_hits[0][3]
    print(f"{'FIRED' if excerpt_clean else '**MISSED**'}: table-row source line "
          f"produces a pipe-free docket excerpt")
    ok &= excerpt_clean
    if table_hits:
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write(f"# docket\nworkplan/t.md:5 | absolute | {table_hits[0][3]} | N/A: table row test\n")
            p2 = f.name
        table_row_annotated_ok = cmd_check(p2) == 0
        print(f"{'PASS' if table_row_annotated_ok else '**FAIL**'}: check correctly reads "
              f"the annotation on a table-row-sourced docket line")
        os.unlink(p2)
        ok &= table_row_annotated_ok

    print("SELFTEST:", "ALL FIRED" if ok else "FAILURE")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", nargs="?", choices=["generate", "check"])
    ap.add_argument("--base", default="origin/main")
    ap.add_argument("--docket", default=DEFAULT_DOCKET)
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(selftest())
    if args.command == "generate":
        sys.exit(cmd_generate(args.base, args.docket))
    if args.command == "check":
        sys.exit(cmd_check(args.docket))
    ap.print_help()


if __name__ == "__main__":
    main()
