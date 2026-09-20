#!/usr/bin/env python3
"""Render a page of a persisted PDF to an image, so a session can LOOK at the scan.

WHY THIS EXISTS, AND IT IS A DEFECT REPORT ON BATCH 19 RATHER THAN A FEATURE NOTE.

Batch 19 mined REF-01005's bibliography out of a scanned 1979 microfiche. The PDF's OCR
text layer is badly damaged, so the batch:

  * recorded "no OCR engine is available in this environment (no tesseract, no
    pdftotext), so this text layer is the best that exists here";
  * transcribed 38 entries with per-entry damage flags, marking authors "illegible" and
    years "not resolvable";
  * built a floor/ceiling BAND into scripts/research/mining_screen.py to bound how much
    the damage might be hiding;
  * and wrote all of that into a session record, an attestation, three candidates, two
    extractions and an amendment to a filed gap.

EVERY ONE OF THOSE CLAIMS WAS WRONG, AND THE DOCUMENT WAS LEGIBLE THE WHOLE TIME. The
pages are JBIG2 images inside the PDF. Rendering one and looking at it takes a second and
reads plainly: "Templer, J.A. Stair shape and human movement, Unpublished doctoral
dissertation. New York: Columbia University, 1974." -- transcribed by the batch as
"[?] [Un]iversity". "Walter, F. ... Disabled Living Foundation, 1971." -- the batch called
the initial unexplained and the year unreadable, and built a candidate trail on it.

THE MISTAKE WAS NOT THE BAD TRANSCRIPTION. It was reasoning about the LIMITS OF A TEXT
LAYER as though they were the limits of the DOCUMENT. `pypdf.extract_text()` returning
mush means the text layer is mush; it says nothing about the page. Nothing in this
repository offered the second route, so the session concluded the document was unreadable
and then wrote a great deal of careful prose about the consequences of that -- CLAUDE.md
5(a) one level up: not a gate that passed having examined nothing, but a SESSION that
concluded having looked at nothing.

So: when a text layer is damaged, RENDER THE PAGE AND READ IT. The image is persisted as a
derived artefact beside the payload it came from, so a later reader can check the
transcription against the same bytes rather than re-rendering and hoping.

    python3 scripts/research/page_image.py --artefact <sha16>.pdf --pages 167-169 \\
        --session <session> [--dpi 130]

Prints the written paths. Read them with the Read tool -- that is the point; the renderer
does not interpret anything.
"""
import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG_ROOT = ROOT / "retrieval-log"


def _parse_pages(spec):
    """'167', '167-169', '3,167-169' -> sorted unique zero-based indices as given.

    NO OFF-BY-ONE TRANSLATION IS DONE HERE, and the reason is a real defect: batch 19
    recorded a locator as "page 57" meaning the 1-based PDF page, while the printed page
    number on that sheet is 54. A reader with the physical report is sent to the wrong
    page. This tool speaks ONLY in zero-based pypdf/pymupdf indices, the same ones
    extract_text() uses, and says so in its output, so a locator derived from it is
    unambiguous about which numbering it means.
    """
    out = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.update(range(int(a), int(b) + 1))
        else:
            out.add(int(part))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--artefact", required=True,
                    help="the persisted PDF's filename inside the session log, "
                         "or a path to it")
    ap.add_argument("--session", required=True,
                    help="retrieval-log session holding the artefact; images are "
                         "written beside it")
    ap.add_argument("--pages", required=True,
                    help="ZERO-BASED page indices: '167' or '167-169' or '3,167-169'")
    ap.add_argument("--dpi", type=int, default=130,
                    help="130 is legible for 1970s microfiche; raise it for small type")
    ap.add_argument("--ref-id", default=None,
                    help="evidence_sources.ref_id these pages belong to; recorded on each "
                         "manifest line so a render is scoped to its source")
    ap.add_argument("--out-session", default=None,
                    help="write images into a DIFFERENT session's log (default: the "
                         "session the artefact came from)")
    args = ap.parse_args()

    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import retrieval_log
    try:
        import pymupdf
    except ImportError:
        print("pymupdf is not installed. It is declared in "
              "governance/check-registry.yaml's `batteries:` and installed by "
              ".claude/hooks/ensure-deps.sh — run that first. Never "
              "`pip install -r requirements.txt` (CLAUDE.md §1).", file=sys.stderr)
        return 2

    src_dir = LOG_ROOT / args.session
    pdf = Path(args.artefact)
    if not pdf.is_file():
        pdf = src_dir / args.artefact
    if not pdf.is_file():
        print(f"no such artefact: {pdf}", file=sys.stderr)
        return 2

    out_dir = LOG_ROOT / (args.out_session or args.session)
    out_dir.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(pdf)
    wrote = []
    for i in _parse_pages(args.pages):
        if not (0 <= i < len(doc)):
            print(f"  page index {i} is outside this document (0..{len(doc) - 1})",
                  file=sys.stderr)
            continue
        # Named for the SOURCE artefact and the page, not hashed: this is a rendering of
        # bytes already in the log, and a reader checking a transcription needs to find it
        # by the page it is a picture of.
        dest = out_dir / f"{pdf.stem}.p{i:04d}.png"
        doc[i].get_pixmap(dpi=args.dpi).save(dest)
        # ATTEST IT. A file written into an evidence log with no manifest line records
        # nothing -- not its sha256, not what it was rendered from, not when. It would be
        # invisible to _manifest_records, _unparsed_payloads and _failed_retrievals, and
        # this module's own promise that "a later reader can check the transcription
        # against the same bytes" would rest on unattested files.
        sha = retrieval_log.record_file(
            dest, args.out_session or args.session, pdf.name,
            purpose=f"page render, zero-based index {i}, {args.dpi} dpi",
            ref_id=args.ref_id, kind="page-render")
        wrote.append(dest)
        print(f"  {dest}  sha256 {sha[:16]}")
    doc.close()

    print(f"EXAMINED: {len(wrote)} page(s) rendered from {pdf.name} at {args.dpi} dpi, "
          f"ZERO-BASED indices")
    print("These are RENDERINGS of a persisted payload, not retrievals. Read them, then "
          "transcribe from what you SEE — a damaged text layer is a fact about the text "
          "layer, never about the document.")
    return 0 if wrote else 1


if __name__ == "__main__":
    sys.exit(main())
