"""Repair of the 104 translation reviews (OD-30) on a scratch copy, through db.py verbs only.
Run: python3 -I repair.py <scratch.db> <session-stem> <verdicts.json> <fixes.json>
verdicts.json: [{"id","verdict","reason"}] from the independent Opus reviewer (all 104 cells).
fixes.json:    [{"id","text","verdict","reason"}] corrected translations for the cells rejected for a wrong term,
               with the reviewer's verdict on each corrected text.
"""
import json
import os
import subprocess
import sys

DB, STEM, VERDICTS, FIXES = sys.argv[1:5]
ENV = {**os.environ, "GUIDEBOOK_DB_PATH": DB}
REVIEWER = "claude-opus-5-5 (independent reviewing instance)"
OK_REASON = ("Independent review against the original by a different Opus-class instance (OD-30): numbers, units, "
             "inequalities, conditions and technical terms checked. A blind second translation by claude-sonnet-5-5 "
             "was an aid, not the review. A model, not a person.")


def run(*args):
    p = subprocess.run([sys.executable, "scripts/db.py", *args, "--session", STEM], env=ENV, capture_output=True,
                       text=True)
    if p.returncode != 0:
        sys.exit(f"FAILED {args[:3]}: {(p.stdout + p.stderr)[-500:]}")
    try:
        return json.loads(p.stdout)
    except ValueError:
        return {}


import sqlite3  # noqa: E402

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
verdicts = {v["id"]: v for v in json.load(open(VERDICTS, encoding="utf-8"))}
fixes = {v["id"]: v for v in json.load(open(FIXES, encoding="utf-8"))}
current = {f"{r['source_table']}:{r['source_column']}:{r['source_row_key']}": r for r in con.execute(
    "SELECT * FROM translations WHERE status='reviewed' AND superseded_by_translation_id IS NULL")}
assert set(current) == set(verdicts), (len(current), len(verdicts))
con.close()

done = {"reviewed": 0, "rejected": 0, "fixed": 0}
for cell, old in current.items():
    ptr = ["--source-table", old["source_table"], "--source-column", old["source_column"],
           "--source-row-id", old["source_row_key"], "--target-language", old["target_language"],
           "--stage", "judgment"]
    new = run("record-translation", *ptr, "--text", old["translated_text"], "--translator-kind", "model",
              "--translator-name", old["translator_name"], "--supersedes", str(old["translation_id"]))
    v = verdicts[cell]
    if v["verdict"] == "reviewed":
        run("review-translation", "--translation-id", str(new["translation_id"]), "--verdict", "reviewed",
            "--reviewer-kind", "model", "--reviewer-name", REVIEWER, "--reason", OK_REASON)
        done["reviewed"] += 1
        continue
    run("review-translation", "--translation-id", str(new["translation_id"]), "--verdict", "rejected",
        "--reviewer-kind", "model", "--reviewer-name", REVIEWER, "--reason", v["reason"])
    done["rejected"] += 1
    if cell in fixes:
        f = fixes[cell]
        fresh = run("record-translation", *ptr, "--text", f["text"], "--translator-kind", "model",
                    "--translator-name", "claude-sonnet-5-5")
        if f["verdict"] == "reviewed":
            run("review-translation", "--translation-id", str(fresh["translation_id"]), "--verdict", "reviewed",
                "--reviewer-kind", "model", "--reviewer-name", REVIEWER, "--reason", OK_REASON)
        else:
            run("review-translation", "--translation-id", str(fresh["translation_id"]), "--verdict", "rejected",
                "--reviewer-kind", "model", "--reviewer-name", REVIEWER, "--reason", f["reason"])
        done["fixed"] += 1
print(json.dumps(done))
