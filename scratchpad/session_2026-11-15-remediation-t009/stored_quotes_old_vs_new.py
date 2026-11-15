"""Does any stored quote change its locate_quote verdict between origin/main and the working tree?
Usage: python3 -I stored_quotes_old_vs_new.py   (run from the repository root; read-only)."""
import sqlite3, subprocess, sys, types
sys.path.insert(0, "scripts"); sys.path.insert(0, "scripts/research")
import retrieval_log as new
src = subprocess.run(["git", "show", "origin/main:scripts/research/retrieval_log.py"], capture_output=True, text=True, check=True).stdout
old = types.ModuleType("retrieval_log_old"); old.__file__ = str(new.__file__)
exec(compile(src, "retrieval_log_old", "exec"), old.__dict__)
con = sqlite3.connect("file:data/guidebook.db?mode=ro", uri=True)
total = changed = 0
for table, col in (("observed_terms", "context_quote"), ("source_value_extractions", "claim_text"),
                   ("extraction_relations", "quote"), ("search_candidates", "surfaced_quote")):
    rows = [r[0] for r in con.execute(f'SELECT "{col}" FROM "{table}" WHERE "{col}" IS NOT NULL AND trim("{col}")<>\'\'')]
    diff = [q for q in rows if old.locate_quote(q)[0] != new.locate_quote(q)[0]]
    total += len(rows); changed += len(diff)
    print(f"{table}.{col}: {len(rows)} quotes, verdict changed for {len(diff)}")
print(f"EXAMINED: {total} stored quote(s); changed: {changed}")
for q in ("the landlord's authority", "the landlord’s authority"):
    print(repr(q), "old", old.locate_quote(q)[0], "| new", new.locate_quote(q)[0])
for q in ("´", "ִ"):
    print(repr(q), "old", old.locate_quote(q)[0], "| new", new.locate_quote(q)[0])
