#!/usr/bin/env python3
"""Derive the WHOLE text of a source's held PDF or web page, registered under its ref_id.

WHY THIS EXISTS (catalogue-plan-v2 section 3.3 step 1; tooling T1, owner approval D8,
2026-10-09). The scan contract reads every admitted source against the whole parameter
list, and a reading can only be as complete as the text it reads. Batch 23 extracted text
by hand from PDFs it held whole -- REF-01027's derived text covers 4 of its 79 pages -- and
nothing could say how much of a document a reading had actually seen. A reading recorded
as `full` over four pages would make the catalogue imply "no code sets a requirement"
where nobody read the code (the GAP-061 shape). This derives ALL pages, in the page-marker
form the batch 23 texts already use (`[PDF page N of M]`), so `db.py record-scan` can
COMPUTE pages read against pages held instead of being told.

IT IS NOT A SECOND COPY OF THE LOG'S MECHANISMS. Which files belong to a source is
`retrieval_log.artefacts_for_source`; the manifest line is `retrieval_log.record_file`
(kind `text-extraction`, the kind batch 23 used); decoding a web page is
`retrieval_log.decode_artefact`. The derived text carries the source's ref_id, so quotes
read from it verify SCOPED (`retrieval_log.locate_quote`) -- which is what lets
`observe-term` refuse a quote found only in some other source's bytes.

NO NETWORK. It reads bytes already persisted under retrieval-log/. A source with no held
PDF or HTML has nothing to derive from, and the reading is recorded as partial, fragment
or abstract (or the document is retrieved first, R10).

    python3 scripts/research/full_text.py --ref-id REF-01027 --session <session>
    python3 scripts/research/full_text.py --ref-id REF-01027 --session <session> \\
        --artefact 1bc0a3fe0bdf78f2.pdf        # when the source holds several files

`--session` names the retrieval-log directory the derived text is written into: the
session doing the reading, not the one that fetched the PDF (the manifest line names the
PDF it was derived from). Prints pages read / pages total, the pages with no text layer
(render those with page_image.py and read them), the sha256, and the record-scan call.

Exit 0 written or already registered; 1 nothing derivable; 2 refused or ambiguous.
"""
import argparse
import hashlib
import html
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import retrieval_log                                                  # noqa: E402
import dbcore                                                         # noqa: E402

_DERIVABLE = (".pdf", ".html")
_SCRIPT_STYLE = re.compile(r"<(script|style|noscript)\b[^>]*>.*?</\1\s*>", re.I | re.S)
_BLOCK = re.compile(r"<\s*(br|/p|/div|/li|/tr|/h[1-6]|/td|/th|/section|/article)\b[^>]*>",
                    re.I)
_TAGS = re.compile(r"<[^>]+>")


def pdf_text(path):
    """(text, pages_total, empty_pages) -- every page, each headed by its marker.

    The join reproduces the batch 23 files byte-for-byte in shape: the marker line, the
    page's text as PyMuPDF returns it, and one blank line before the next marker.
    """
    import pymupdf
    with pymupdf.open(str(path)) as doc:
        n = doc.page_count
        parts, empty = [], []
        for i, page in enumerate(doc, start=1):
            t = page.get_text()
            if not retrieval_log.normalise_quote(t):
                empty.append(i)
            parts.append(f"[PDF page {i} of {n}]\n{t}")
    return "\n".join(parts), n, empty


def html_text(path, content_type=None):
    """Visible text of a saved web page (scripts and styles dropped, tags stripped)."""
    body, enc = retrieval_log.decode_artefact(Path(path).read_bytes(), content_type)
    if body is None:
        raise ValueError(f"{path.name}: bytes not decodable ({enc})")
    body = _SCRIPT_STYLE.sub(" ", body)
    body = _BLOCK.sub("\n", body)
    body = html.unescape(_TAGS.sub(" ", body))
    lines = [re.sub(r"[ \t ]+", " ", ln).strip() for ln in body.splitlines()]
    return "\n".join(ln for ln in lines if ln) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref-id", required=True)
    ap.add_argument("--session", required=True,
                    help="the reading session; the derived text is written into its log")
    ap.add_argument("--artefact", help="which held PDF/HTML to derive from, by file name")
    ap.add_argument("--dry-run", action="store_true",
                    help="derive and report, write nothing")
    args = ap.parse_args()
    ref = dbcore.fold_ref(args.ref_id)

    with dbcore.connect(readonly=True) as conn:
        row = conn.execute("SELECT url, superseded_by_ref_id FROM evidence_sources "
                           "WHERE ref_id = ?", (ref,)).fetchone()
    if row is None:
        print(f"REFUSING: {ref} is not an admitted source.", file=sys.stderr)
        return 2
    if row["superseded_by_ref_id"]:
        print(f"REFUSING: {ref} is superseded by {row['superseded_by_ref_id']} -- a "
              f"tombstone is never read again; derive the replacement's text instead.",
              file=sys.stderr)
        return 2

    held = retrieval_log.artefacts_for_source(ref, row["url"])
    cands = [h for h in held if not h["derived"] and h["exists"]
             and h["path"].suffix.lower() in _DERIVABLE]
    if args.artefact:
        pick = [h for h in cands if h["artefact"] == args.artefact]
        if not pick:
            print(f"REFUSING: --artefact {args.artefact!r} is not a PDF or HTML file saved "
                  f"for {ref}. Saved for it: "
                  f"{[h['artefact'] for h in held] or 'nothing'}", file=sys.stderr)
            return 2
        src = pick[0]
    else:
        pdfs = [h for h in cands if h["path"].suffix.lower() == ".pdf"]
        pages = [h for h in cands if h["path"].suffix.lower() == ".html"]
        if len(pdfs) == 1:
            src = pdfs[0]
        elif not pdfs and len(pages) == 1:
            src = pages[0]
        elif not cands:
            print(f"NOTHING TO DERIVE: no PDF or HTML is saved for {ref} "
                  f"(saved: {[h['artefact'] for h in held] or 'nothing'}). Record the "
                  f"reading at the scope the bytes allow, or retrieve the document (R10).",
                  file=sys.stderr)
            return 1
        else:
            print(f"AMBIGUOUS: {ref} holds several derivable files; name one with "
                  f"--artefact:", file=sys.stderr)
            for h in cands:
                print(f"  {h['artefact']}  ({h['via']}, {h['session']})", file=sys.stderr)
            return 2

    if src["path"].suffix.lower() == ".pdf":
        try:
            text, total, empty = pdf_text(src["path"])
        except ImportError:
            print("pymupdf is not installed: run .claude/hooks/ensure-deps.sh (it is the "
                  "research battery's declared reader).", file=sys.stderr)
            return 2
        how = (f"PyMuPDF text extraction, all {total} page(s), each headed "
               f"'[PDF page N of M]' (scripts/research/full_text.py)")
    else:
        text, total, empty = html_text(src["path"]), None, []
        how = ("HTML visible-text extraction, whole page (scripts/research/full_text.py: "
               "script/style dropped, tags stripped, html.unescape)")

    body = text.encode("utf-8")
    sha = hashlib.sha256(body).hexdigest()
    session = retrieval_log._session_stem(args.session)
    out_dir = retrieval_log.LOG_ROOT / session
    dest = out_dir / f"{Path(src['artefact']).stem}-full-text.txt"

    registered = [r for r in retrieval_log._manifest_records(session)
                  if r.get("artefact") == dest.name and r.get("ref_id") == ref
                  and r.get("sha256") == sha]
    if dest.exists() and hashlib.sha256(dest.read_bytes()).hexdigest() != sha:
        print(f"REFUSING: {dest} exists with different bytes. Artefacts are written once; "
              f"derive into another session's log instead.", file=sys.stderr)
        return 2

    print(f"source:      {ref} <- {src['session']}/{src['artefact']} ({src['via']})")
    if total is not None:
        print(f"pages read:  {total} of {total}")
        if empty:
            print(f"NO TEXT LAYER on {len(empty)} page(s): {empty[:20]}"
                  + (" ..." if len(empty) > 20 else "")
                  + " -- render them (scripts/research/page_image.py) and read the "
                    "images; a missing text layer is a fact about the layer, not the page")
    else:
        print("pages read:  not paged (a web page is read whole)")
    print(f"sha256:      {sha}")
    print(f"derived:     {dest}")
    if args.dry_run:
        print("DRY RUN: nothing written.")
        return 0
    if registered:
        print("ALREADY REGISTERED: this text is already in the log under this ref_id.")
    else:
        out_dir.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(body)
        retrieval_log.record_file(dest, session, src["artefact"], purpose=f"{how}; {ref}",
                                  ref_id=ref, kind="text-extraction")
        print("WROTE and registered under the ref_id (retrieval_log.record_file).")
    print("record the reading with:\n"
          f"  db.py record-scan --ref-id {ref} --mode catalogue --file-sha256 {sha} "
          f"--text-scope <full|partial|fragment|abstract> --method full-read "
          f"[--open-pass-done] --session {session}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
