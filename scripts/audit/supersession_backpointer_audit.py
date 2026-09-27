#!/usr/bin/env python3
"""scripts/audit/supersession_backpointer_audit.py — currency lives at the superseded text.

WHY THIS EXISTS (RC3, DR-2026-09-26-recurring-defect-shapes-remediation.md section 4).
Binding text lives in more than five stores (DRs, the append-only ledger, the YAML
register, the `decisions` table, CLAUDE.md, the research contract and its SessionStart
copy, code comments, `sessions/*.md`), and a ruling superseding one of them was sometimes
left with no local mark: a reader who reaches the superseded sentence by grep meets it
with nothing saying it no longer holds. The fix is not a currency INDEX — that would be
the next store rule 5 forbids — it is a pointer at the text itself, anchored on quotes
that occur exactly once at both ends, checked with plain file I/O so `.ignore` cannot
hide the target (owner rulings live overwhelmingly in `sessions/`, which `.ignore` hides
from ripgrep and the Grep tool).

THE GRAMMAR, read from the ledger and from any DR using the same trailer:

    SUPERSEDES: <target path> :: "<verbatim quote from the target>"
      BY: references/project-standards.md :: "<verbatim quote from the superseding ruling>"

NORMALISATION (so a quote survives comment wrapping, YAML folding and Markdown
blockquotes): for each line, strip leading whitespace and one leading run of `#`, `>`,
`//` or `--`, join the lines with spaces, and collapse whitespace. Both quotes must
occur EXACTLY ONCE in their own file under this normalisation.

FAILS when: the target quote occurs 0 times (edited in place, which the append-not-edit
practice forbids) or more than once (ambiguous); the BY quote does not occur exactly
once in the ledger; or no line in the target quote's own paragraph, or in the paragraph
or blockquote immediately after it, both names SUPERSEDED or AMENDED and carries the BY
quote verbatim. `BY` is always required — `DATE:` lines in the ledger are not unique
(the most repeated closes thirteen entries), so a marker cannot be anchored on one.

EXAMINED counts `SUPERSEDES:` lines. Today there may be none in a fresh clone before the
first seed lands — that is NOTHING-IN-SCOPE, not a failure (CLAUDE.md section 5a): a
check with no subject must say so, not pass by finding nothing to check.
"""
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import dbcore                                                        # noqa: E402

LEDGER = REPO_ROOT / "references" / "project-standards.md"
DR_DIR = REPO_ROOT / "decisions"

# The grammar and normalisation are ONE home, scripts/dbcore.py (rule 5): this script and
# scripts/db.py's dispose-adversarial-finding (OWNER-RULED) both anchor on the same
# quotes and must count them the same way, or a ref that passes one refuses the other.
_SUPERSEDES_RE = dbcore.LEDGER_SUPERSEDES_RE
_MARKER_WORD = re.compile(r'\b(SUPERSEDED|AMENDED)\b')


def _paragraphs(text: str):
    """[(start_line, end_line, normalised_joined_text)], blank-normalised-line delimited.

    A blockquote's blank line is often `>` alone, which normalises to "" here too, so a
    blockquote paragraph is delimited the same way as a plain-prose one.
    """
    lines = text.split("\n")
    normed = [dbcore.strip_ledger_line_marker(l) for l in lines]
    paras, cur_start, cur = [], None, []
    for i, n in enumerate(normed):
        if n:
            cur_start = i if cur_start is None else cur_start
            cur.append(n)
        elif cur:
            paras.append((cur_start, i - 1, " ".join(cur)))
            cur_start, cur = None, []
    if cur:
        paras.append((cur_start, len(lines) - 1, " ".join(cur)))
    return paras, lines


def _find_paragraph(paras, quote_norm: str):
    for idx, (start, end, joined) in enumerate(paras):
        if quote_norm in joined:
            return idx
    return None


def _paragraph_has_marker(lines, start: int, end: int, by_quote: str) -> bool:
    raw = "\n".join(lines[start:end + 1])
    # The BY quote is checked under the SAME normalisation as everywhere else in this
    # script, via dbcore.count_ledger_quote, not as a raw substring: a marker paragraph
    # that wraps the quote across two comment lines (a leading `#`/`>` on the wrapped
    # line) would otherwise never match, and a correctly-authored marker would FAIL.
    return bool(_MARKER_WORD.search(raw)) and dbcore.count_ledger_quote(raw, by_quote) > 0


def _parse_supersedes(text: str):
    """[(target_path, target_quote, by_path, by_quote), ...] from one file's raw text."""
    return [(m.group(1), m.group(2), m.group(3), m.group(4))
            for m in _SUPERSEDES_RE.finditer(text)]


def main() -> int:
    sources = []
    if LEDGER.exists():
        sources.append(LEDGER)
    if DR_DIR.exists():
        sources.extend(sorted(DR_DIR.glob("*.md")))

    entries, text_cache = [], {}
    for src in sources:
        text = src.read_text(encoding="utf-8")
        text_cache[src] = text
        for target_path, target_quote, by_path, by_quote in _parse_supersedes(text):
            entries.append((src, target_path, target_quote, by_path, by_quote))

    examined = len(entries)
    print(f"SUPERSEDES lines found (ledger + decisions/*.md): {examined}")
    if examined == 0:
        print("VERDICT: PASS — NOTHING-IN-SCOPE (no SUPERSEDES line exists yet; "
              "correct until the first seed lands, per DR-2026-09-26 section 8).")
        print("EXAMINED: 0")
        return 0

    if not LEDGER.exists():
        print(f"[ERROR] no ledger at {LEDGER.relative_to(REPO_ROOT)}, but SUPERSEDES "
              f"lines were found. Cannot verify BY quotes.")
        print(f"EXAMINED: {examined}")
        return 2
    ledger_prose = dbcore.strip_supersedes_citations(text_cache[LEDGER])

    findings = []
    target_cache = {}  # target_rel -> (text, paragraphs, lines); several entries can share one target
    for src, target_rel, target_quote, by_path, by_quote in entries:
        where = f"{src.relative_to(REPO_ROOT)} (SUPERSEDES {target_rel!r})"
        if target_rel not in target_cache:
            target_file = REPO_ROOT / target_rel
            if not target_file.exists():
                target_cache[target_rel] = None
            else:
                text = target_file.read_text(encoding="utf-8")
                target_cache[target_rel] = (text, *_paragraphs(text))
        cached = target_cache[target_rel]
        if cached is None:
            findings.append(f"{where}: target file does not exist.")
            continue
        target_text, paras, lines = cached
        n_target = dbcore.count_ledger_quote(target_text, target_quote)
        if n_target != 1:
            findings.append(
                f"{where}: target quote occurs {n_target} time(s) in {target_rel} "
                f"(must be exactly 1) — {'edited in place' if n_target == 0 else 'ambiguous'}.")
            continue

        if by_path != "references/project-standards.md":
            findings.append(f"{where}: BY names {by_path!r}, not the ledger — only the "
                            f"ledger is a superseding-ruling home this audit verifies.")
            continue
        n_by = dbcore.count_ledger_quote(ledger_prose, by_quote)
        if n_by != 1:
            findings.append(
                f"{where}: BY quote occurs {n_by} time(s) in the ledger's substantive "
                f"prose, excluding SUPERSEDES citation lines (must be exactly 1).")
            continue

        quote_norm = dbcore.normalise_quote_text(target_quote)
        pidx = _find_paragraph(paras, quote_norm)
        if pidx is None:
            findings.append(f"{where}: could not locate the target quote's own paragraph "
                            f"in {target_rel} (internal inconsistency — the quote counted "
                            f"once but no paragraph contains it normalised).")
            continue
        candidates = [paras[pidx]] + ([paras[pidx + 1]] if pidx + 1 < len(paras) else [])
        marked = any(_paragraph_has_marker(lines, s, e, by_quote) for s, e, _ in candidates)
        if not marked:
            findings.append(
                f"{where}: no SUPERSEDED/AMENDED line carrying the BY quote verbatim sits "
                f"in the target quote's paragraph or the one immediately after it in "
                f"{target_rel}.")

    print(f"EXAMINED: {examined}")
    if findings:
        print("VERDICT: FAIL")
        for f in findings:
            print("  * " + f)
        return 1
    print("VERDICT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
