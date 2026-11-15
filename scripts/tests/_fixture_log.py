"""A fixture retrieval-log root that a pre-admission fetch cannot reach (T-073).

A batch persists what it fetched under the id its source will take BEFORE `db.py add-source` admits the source, so between
the two the retrieval log holds an id the database does not. A fixture that mints a source through the writer takes the
database's next id, which is that folder's id, and inherits the saved text: a refusal case then goes red for a reason that
has nothing to do with what it tests. The fix is to isolate the ROOT, not to change the id: a real admission must still take
the id its folder was filed under.

`fixture_log_root(dest, db_path)` symlinks into `dest` each folder of the repository's retrieval log EXCEPT a folder whose
manifest names a ref_id above the high-water mark of the database at `db_path`; such a folder is linked file by file with
only the lines and artefacts of those ids left out, and one line is printed for each.
"""
import json
import pathlib
import re
import sqlite3
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "scripts"))
import dbcore  # noqa: E402


def fixture_log_root(dest, db_path, source=None):
    dest, source = pathlib.Path(dest), pathlib.Path(source or REPO / "retrieval-log")
    dest.mkdir(parents=True, exist_ok=True)
    ro = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    try:
        high = dbcore.ref_id_high_water(ro)
    finally:
        ro.close()
    for d in sorted(source.iterdir()):
        if not d.is_dir():
            continue
        manifest = d / "manifest.jsonl"
        keep, ahead, stems = [], set(), set()
        if manifest.exists():
            for line in manifest.open(encoding="utf-8"):
                if not line.strip():
                    continue
                rec = json.loads(line)
                ref = (rec.get("ref_id") or "").strip()
                m = dbcore._MINTABLE.fullmatch(ref)
                if m and int(m.group(1)) > high:
                    ahead.add(ref)
                    if rec.get("artefact"):
                        stems.add(pathlib.Path(rec["artefact"]).stem)
                else:
                    keep.append(line)
        if not ahead:
            link = dest / d.name
            if not link.exists():
                link.symlink_to(d.resolve())
            continue
        # A batch files several sources into one folder and admits them one at a time: leave out only the lines (and the
        # files) of the ids above the mark, not the artefacts of the sources already admitted (T-073 critic, 2026-11-15).
        print(f"fixture root: left out {sorted(ahead)} from {d.name} (above the copy's high-water mark {high})")
        out = dest / d.name
        out.mkdir(exist_ok=True)
        (out / "manifest.jsonl").write_text("".join(keep), encoding="utf-8")
        for f in d.iterdir():
            if f.name != "manifest.jsonl" and not any(f.name.startswith(st) for st in stems) and not (out / f.name).exists():
                (out / f.name).symlink_to(f.resolve())
    return str(dest)
