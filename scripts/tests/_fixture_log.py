"""A fixture retrieval-log root that a pre-admission fetch cannot reach (T-073).

A batch persists what it fetched under the id its source will take BEFORE `db.py add-source` admits the source, so between
the two the retrieval log holds an id the database does not. A fixture that mints a source through the writer takes the
database's next id, which is that folder's id, and inherits the saved text: a refusal case then goes red for a reason that
has nothing to do with what it tests. The fix is to isolate the ROOT, not to change the id: a real admission must still take
the id its folder was filed under.

`fixture_log_root(dest, db_path)` symlinks into `dest` each folder of the repository's retrieval log EXCEPT a folder whose
manifest names a ref_id above the high-water mark of the database at `db_path`, and prints one line for each it leaves out.
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
        ahead = set()
        if manifest.exists():
            for line in manifest.open(encoding="utf-8"):
                if line.strip():
                    ref = (json.loads(line).get("ref_id") or "").strip()
                    m = dbcore._MINTABLE.fullmatch(ref)
                    if m and int(m.group(1)) > high:
                        ahead.add(ref)
        if ahead:
            print(f"fixture root: left out {d.name} (holds {sorted(ahead)}, above the copy's high-water mark {high})")
            continue
        link = dest / d.name
        if not link.exists():
            link.symlink_to(d.resolve())
    return str(dest)
