#!/usr/bin/env python3
"""The typed home for translations (T-049): AT-107, AT-108, AT-109, each shown to fire and to pass.

WHAT REACHES THE GUIDEBOOK WITHOUT THESE CASES. A session that meets a Japanese or Dutch quotation either translates
in its head and loses the translation, or writes an English paraphrase where the source's words should be and a
later reader takes it for the source's. A translation that adds, drops or changes a figure passes every gate that asks
only whether a translation EXISTS. A translation shown beside a quotation that has since changed. A stage name
written into a verb's code, so that moving the default is a code change.

AT-107  from the stage judgment, request and record a translation of a non-English figure's claim_text by the verbs
        alone: the original cell is byte-identical, the current-translations view joins back to it by its pointer,
        requested_at_stage is judgment, and the verbs change no file under scripts/ or schemas/.
AT-108  with the contract as committed a request with no --due-stage is listed at the contract's default stage; with
        a temporary copy of the contract naming another stage it is listed there and not at the first, and a request
        that names its own due stage is listed there under both; no file is changed; no stage id is written as a
        string constant inside the verbs.
AT-109  a translation that changes a figure of the original is refused; one that drops a figure is refused; one that
        keeps every figure is accepted; one of a quote that spells its number in words, stating the numeral of the
        row's claimed_value, is accepted; one of a quote in CJK numerals, stating them as Arabic numerals, is
        accepted. A pointer to a table, column or row that does not exist, or into a table whose key has several
        columns, is refused; the original cannot be retyped; a cell changed since the request is refused; review
        needs a reviewer other than the translator and a reason to reject; the schema holds the review rules itself;
        --supersedes retires the translation it names and refuses what it should.

Every probe is chosen by query. Anything written goes to a COPY of the database (rows marked TASK-FIXTURE); a state
the verbs cannot build is made by SQL on a second copy and marked HAND. A case that needs a state the live data does
not offer prints SKIPPED-NO-FIXTURE (counted apart), never silently passes.
"""
import ast
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
os.chdir(REPO)
TMP = tempfile.mkdtemp(prefix="guidebook-t049-")
DB = os.path.join(TMP, "guidebook.db")
shutil.copy(REPO / "data" / "guidebook.db", DB)
os.environ["GUIDEBOOK_DB_PATH"] = DB
sys.path.insert(0, str(REPO / "scripts"))
sys.path.insert(0, str(REPO))
import db                                                              # noqa: E402
import dbcore                                                          # noqa: E402
from dbcore import Refusal                                             # noqa: E402
from schemas.pipeline_contract import PipelineContract                 # noqa: E402

S = "session_test-translations"
CONTRACT_FILE = REPO / "governance" / "pipeline-contract.yaml"
results, skipped = [], []


def record(tid, name, passed, details=""):
    results.append(bool(passed))
    print(f"  [{'✓' if passed else '✗'}] {tid}: {name}")
    if details and not passed:
        print(f"      {str(details)[:500]}")


def skip(tid, why):
    skipped.append(tid)
    print(f"  [-] {tid}: SKIPPED-NO-FIXTURE: {why}")


def refused_for(part, fn, *a, **k):
    """True when `fn` refuses AND the refusal says `part`: refused for the reason under test, not another."""
    try:
        fn(*a, **k)
    except Refusal as exc:
        return part in str(exc)
    except Exception as exc:  # noqa: BLE001
        print(f"      DEFECT (not a refusal): {type(exc).__name__}: {exc}")
    return False


def cli(*args, path=None):
    p = subprocess.run([sys.executable, "scripts/db.py", *args], capture_output=True, text=True,
                       env={**os.environ, "GUIDEBOOK_DB_PATH": path or DB})
    return p.returncode, p.stdout, p.stderr


def finish():
    print(f"\nEXAMINED: {len(results)} cases")
    print(f"SKIPPED-NO-FIXTURE: {len(skipped)}")
    ok = bool(results) and all(results)
    if ok:
        shutil.rmtree(TMP, ignore_errors=True)
    else:
        print(f"FAILED: {results.count(False)}   (scratch kept: {TMP})")
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


def tracked_state():
    return subprocess.run(["git", "status", "--porcelain", "scripts", "schemas"], capture_output=True,
                          text=True).stdout


con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
q = lambda sql, *p: con.execute(sql, p).fetchall()  # noqa: E731

# --- the schema and the verbs exist: absent, every case below is red by name ---------------------------------------
have = q("SELECT count(*) FROM sqlite_master WHERE name IN ('translations', 'v_translations_current')")[0][0] == 2
verbs = all(hasattr(db, f) for f in ("request_translation", "record_translation", "review_translation",
                                     "translations_due"))
record("T049-01", "the translations table, its current view and the four verbs exist", have and verbs,
       f"table+view: {have}, verbs: {verbs}")
if not (have and verbs):
    finish()

CONTRACT = PipelineContract.load(CONTRACT_FILE)
STAGES = [st.id for st in CONTRACT.stages]
DEFAULT = CONTRACT.translation.default_stage if CONTRACT.translation else None
record("T049-02", "the contract holds a translation rule naming one of its own stages", DEFAULT in STAGES, DEFAULT)
JUDGMENT = next((s for s in STAGES if s == "judgment"), None)     # the stage AT-107 asks from; ids come from the contract
OTHER = next(s for s in STAGES if s != DEFAULT)
THIRD = next(s for s in STAGES if s not in (DEFAULT, OTHER))

# --- probes, chosen by query ----------------------------------------------------------------------------------------
NUM = re.compile(r"\d+(?:[.,]\d+)?")
FIGS = q("SELECT x.extraction_id AS id, x.claim_text AS text, x.claimed_value AS cv, upper(e.lang_detected) AS lang "
         "FROM source_value_extractions x JOIN evidence_sources e USING (ref_id) "
         "WHERE upper(coalesce(e.lang_detected, 'EN')) <> 'EN' AND x.claim_text IS NOT NULL ORDER BY x.extraction_id")
CJK_DIGIT = re.compile(r"[０-９〇零一二三四五六七八九十百千]")
# a figure whose numbers are plain integers, each once and none in CJK, so that a changed or dropped one is unambiguous
plain = next((r for r in FIGS if (t := NUM.findall(r["text"])) and all(x.isdigit() for x in t)
              and len(set(t)) == len(t) and not CJK_DIGIT.search(r["text"])), None)
# a figure whose quote states a number in CJK numerals: its text changes under the converter the verb uses
cjk = next((r for r in FIGS if db._cjk_to_arabic(r["text"]) != r["text"] and NUM.findall(db._cjk_to_arabic(r["text"]))),
           None)
LANGS = [r[0] for r in q("SELECT DISTINCT language FROM lang_jur_map ORDER BY language")]


def langs_for(fig, n):
    """n languages lang_jur_map holds other than the figure's own, in a stable order, none used before for it."""
    return [lg for lg in LANGS if lg != fig["lang"]][:n]


def ptr(fig, lang, column="claim_text"):
    return ["--source-table", "source_value_extractions", "--source-column", column,
            "--source-row-id", str(fig["id"]), "--target-language", lang]


def cell(fig):
    return q("SELECT claim_text FROM source_value_extractions WHERE extraction_id=?", fig["id"])[0][0]


def hand_copy(name):
    path = os.path.join(TMP, name)
    shutil.copy(DB, path)
    return path


def hand_sql(path, sql, *params):
    h = sqlite3.connect(path)
    h.execute(sql, params)
    h.commit()
    h.close()


# === AT-107 ===============================================================================================
if not plain or not JUDGMENT:
    skip("T049-10", f"no non-English figure with plain integers (plain={bool(plain)}, judgment={bool(JUDGMENT)})")
else:
    L1, L2, L3, L4 = langs_for(plain, 4)
    before_cell, before_tree = cell(plain), tracked_state()
    text = "TASK-FIXTURE " + " ".join(NUM.findall(plain["text"]))
    rc1, out1, err1 = cli("request-translation", *ptr(plain, L1), "--stage", JUDGMENT, "--session", S)
    tid = json.loads(out1)["translation_id"] if rc1 == 0 else None
    listed_default = [r["translation_id"] for r in json.loads(cli("translations", "--due-at", DEFAULT)[1] or "[]")]
    rc2, out2, err2 = cli("record-translation", "--translation-id", str(tid), "--text", text,
                          "--translator-kind", "model", "--translator-name", "test-translator", "--session", S)
    record("T049-10", "AT-107 request and record by the verbs alone", rc1 == 0 and rc2 == 0, err1 + err2)
    record("T049-11", "AT-107 the original cell is byte-identical", cell(plain) == before_cell)
    joined = q("SELECT v.translation_id, v.translated_text FROM v_translations_current v "
               "JOIN source_value_extractions x ON v.source_table='source_value_extractions' "
               "AND v.source_column='claim_text' AND v.source_row_key=CAST(x.extraction_id AS TEXT) "
               "WHERE x.extraction_id=? AND x.claim_text=?", plain["id"], before_cell)
    record("T049-12", "AT-107 the current view joins back to that cell by its pointer",
           [tuple(r) for r in joined] == [(tid, text)], joined)
    record("T049-13", "AT-107 requested_at_stage is judgment",
           q("SELECT requested_at_stage FROM translations WHERE translation_id=?", tid)[0][0] == JUDGMENT)
    record("T049-14", "AT-107 the verbs changed no file under scripts/ or schemas/ (the porcelain is the same "
                      "before and after them)", tracked_state() == before_tree)

    # === AT-108 ===========================================================================================
    record("T049-20", "AT-108 an unforced request is listed at the contract's default stage while it is open",
           tid in listed_default, listed_default)
    rq = db.request_translation("source_value_extractions", "claim_text", str(plain["id"]), L2, JUDGMENT, session=S)
    rq_due = db.request_translation("source_value_extractions", "claim_text", str(plain["id"]), L3, JUDGMENT,
                                    due_stage=THIRD, session=S)
    alt = Path(TMP) / "contract-alt.yaml"
    alt.write_text(re.sub(r"(?m)^(  default_stage: ).*$", rf"\g<1>{OTHER}", CONTRACT_FILE.read_text(encoding="utf-8")))
    nokey = Path(TMP) / "contract-no-rule.yaml"
    d = yaml.safe_load(CONTRACT_FILE.read_text(encoding="utf-8"))
    del d["translation"]
    nokey.write_text(yaml.safe_dump(d, sort_keys=False))
    tree = tracked_state()
    ids = lambda stage, **k: [r["translation_id"] for r in db.translations_due(stage, **k)]  # noqa: E731
    record("T049-21", "AT-108 the open request is listed at the default stage and at no other",
           rq["translation_id"] in ids(DEFAULT) and rq["translation_id"] not in ids(OTHER), ids(DEFAULT))
    record("T049-22", "AT-108 a copy of the contract naming another stage lists it there and not at the first",
           rq["translation_id"] in ids(OTHER, contract_path=alt) and rq["translation_id"] not in
           ids(DEFAULT, contract_path=alt), (ids(OTHER, contract_path=alt), ids(DEFAULT, contract_path=alt)))
    record("T049-23", "AT-108 a request with its own --due-stage is listed there under both contracts, not at the "
                      "default",
           all(rq_due["translation_id"] in ids(THIRD, contract_path=c) for c in (CONTRACT_FILE, alt))
           and rq_due["translation_id"] not in ids(DEFAULT) + ids(OTHER, contract_path=alt))
    record("T049-24", "AT-108 moving the default changed no file under scripts/ or schemas/",
           tracked_state() == tree)
    record("T049-25", "the lister refuses when the contract holds no translation rule",
           refused_for("no translation rule", db.translations_due, DEFAULT, contract_path=nokey))
    record("T049-26", "the lister refuses a stage the contract does not hold",
           refused_for("is not a stage id", db.translations_due, "no-such-stage-t049"))
    bad = dict(d, translation={"default_stage": "no-such-stage-t049"})
    try:
        PipelineContract.model_validate(bad)
        refused_model = False
    except ValueError:
        refused_model = True
    record("T049-27", "the contract model refuses a default stage that is not one of its own stages", refused_model)
    record("T049-28", "a stage that is not a stage id is refused as --stage and as --due-stage",
           refused_for("is not a stage id", db.request_translation, "source_value_extractions", "claim_text",
                       str(plain["id"]), L4, "no-such-stage-t049", session=S)
           and refused_for("is not a stage id", db.request_translation, "source_value_extractions", "claim_text",
                           str(plain["id"]), L4, JUDGMENT, due_stage="no-such-stage-t049", session=S))

# no stage id is a string constant inside the verbs: the block this task adds to db.py, from its header to the end
src = Path(db.__file__).read_text(encoding="utf-8")
header = src.index("# --- translations (T-049)")
head_line = src.count("\n", 0, header) + 1
fns = [n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.lineno > head_line]
literal = [(fn.name, n.value) for fn in fns for n in ast.walk(fn)
           if isinstance(n, ast.Constant) and isinstance(n.value, str) and n.value in STAGES]
record("T049-29", "AT-108 no stage id is a string constant in the translation verbs and their helpers",
       {"request_translation", "record_translation", "review_translation", "translations_due"}
       <= {fn.name for fn in fns} and not literal, literal)

# === AT-109 ===============================================================================================
KW = dict(translator_kind="model", translator_name="test-translator", session=S)
if not plain:
    skip("T049-30", "no non-English figure with plain integers")
else:
    nums = NUM.findall(plain["text"])
    changed = "TASK-FIXTURE " + " ".join([str(int(nums[0]) + 1000003)] + nums[1:])
    dropped = "TASK-FIXTURE " + " ".join(nums[1:]) if len(nums) > 1 else "TASK-FIXTURE no figure at all"
    kept = "TASK-FIXTURE " + " ".join(reversed(nums))
    LB = langs_for(plain, 8)[4]
    P = dict(source_table="source_value_extractions", source_column="claim_text", source_row_key=str(plain["id"]),
             target_language=LB, stage=JUDGMENT)
    record("T049-30", "AT-109 a translation that changes a figure is refused",
           refused_for("does not state the original's numbers", db.record_translation, changed, **P, **KW))
    record("T049-31", "AT-109 a translation that drops a figure is refused",
           refused_for("does not state the original's numbers", db.record_translation, dropped, **P, **KW))
    record("T049-32", "AT-109 a refused translation left no row behind",
           q("SELECT count(*) FROM translations WHERE target_language=? AND source_row_key=?", LB,
             str(plain["id"]))[0][0] == 0)
    r = db.record_translation(kept, **P, **KW)
    record("T049-33", "AT-109 a translation that keeps every figure is accepted", r["status"] == "translated", r)
    tid = r["translation_id"]
    record("T049-34", "AT-109 a pointer to a table that does not exist is refused",
           refused_for("is not a table", db.request_translation, "no_such_table_t049", "claim_text", "1", LB,
                       JUDGMENT, session=S))
    record("T049-35", "AT-109 a pointer to a column that does not exist is refused",
           refused_for("has no column", db.request_translation, "source_value_extractions", "no_such_column_t049",
                       str(plain["id"]), LB, JUDGMENT, session=S))
    record("T049-36", "AT-109 a pointer to a row that does not exist is refused",
           refused_for("has no row", db.request_translation, "source_value_extractions", "claim_text", "-1", LB,
                       JUDGMENT, session=S))
    record("T049-37", "AT-109 a pointer to a cell that is not text is refused",
           refused_for("not text", db.request_translation, "source_value_extractions", "extraction_id",
                       str(plain["id"]), LB, JUDGMENT, session=S))
    multi = next(((t, c[1]) for (t,) in q("SELECT name FROM sqlite_master WHERE type='table'")
                  for pk in [[c for c in con.execute(f'PRAGMA table_info("{t}")') if c[5]]]
                  if len(pk) > 1 for c in con.execute(f'PRAGMA table_info("{t}")')
                  if c[2].upper() == "TEXT" and not c[5] and
                  con.execute(f'SELECT 1 FROM "{t}" WHERE typeof("{c[1]}")=\'text\' LIMIT 1').fetchone()), None)
    if multi:
        record("T049-38", "AT-109 a pointer into a table whose primary key has several columns is refused, "
                          "never by rowid", refused_for("no single-column primary key", db.request_translation,
                                                        multi[0], multi[1], "1", LB, JUDGMENT, session=S))
    else:
        skip("T049-38", "no table with a multi-column primary key and a text column")
    sig_names = set()
    for fn in (db.request_translation, db.record_translation, db.review_translation):
        sig_names |= set(fn.__code__.co_varnames[:fn.__code__.co_argcount + fn.__code__.co_kwonlyargcount])
    helps = cli("record-translation", "--help")[1] + cli("request-translation", "--help")[1]
    record("T049-39", "AT-109 the original cannot be retyped: no verb argument and no flag carries it",
           not ({"original", "source_text", "original_text"} & sig_names) and "--original" not in helps
           and "--source-text" not in helps)
    record("T049-40", "AT-109 review requires a reviewer",
           refused_for("--reviewer-name is required", db.review_translation, tid, "reviewed", "model", "", session=S))
    record("T049-41", "AT-109 the reviewer is never the translator (compared case-insensitively)",
           refused_for("is the translator", db.review_translation, tid, "reviewed", "model", "TEST-Translator",
                       session=S))
    record("T049-42", "AT-109 a rejection needs its reason",
           refused_for("--reason is required", db.review_translation, tid, "rejected", "model", "test-reviewer",
                       session=S))
    record("T049-43", "AT-109 the verdict is one of the two statuses a review sets",
           refused_for("reviewed or rejected", db.review_translation, tid, "requested", "model", "test-reviewer",
                       session=S))
    ok = db.review_translation(tid, "reviewed", "model", "test-reviewer", session=S)
    record("T049-44", "AT-109 a different reviewer reviews it", ok["status"] == "reviewed", ok)
    record("T049-45", "AT-109 a reviewed translation is not reviewed twice",
           refused_for("only a translated", db.review_translation, tid, "reviewed", "model", "test-reviewer2",
                       session=S))

    # --supersedes
    record("T049-50", "a cell that already has a current translation into the language is refused, naming --supersedes",
           refused_for(f"--supersedes {tid}", db.request_translation, "source_value_extractions", "claim_text",
                       str(plain["id"]), LB, JUDGMENT, session=S))
    other_cell = next((f for f in FIGS if f["id"] != plain["id"]), None)
    other_old = db.record_translation("TASK-FIXTURE " + " ".join(NUM.findall(other_cell["text"])),
                                      **dict(P, source_row_key=str(other_cell["id"]),
                                             target_language=langs_for(other_cell, 1)[0]), **KW) if other_cell else None
    record("T049-51", "--supersedes is refused for a translation of another cell",
           other_old is not None and refused_for("different cell or language", db.record_translation,
                                                 "TASK-FIXTURE " + " ".join(nums), **dict(P, target_language=langs_for(plain, 9)[5]),
                                                 **KW, supersedes=other_old["translation_id"]))
    LC = langs_for(plain, 9)[8]
    record("T049-52", "--supersedes is refused for a translation of another language",
           refused_for("different cell or language", db.record_translation, "TASK-FIXTURE " + " ".join(nums),
                       **dict(P, target_language=LC), **KW, supersedes=tid))
    record("T049-53", "--supersedes is refused for a row that is not a current translation (a request)",
           refused_for("is not a current translation", db.record_translation, "TASK-FIXTURE " + " ".join(nums),
                       **P, **KW, supersedes=rq["translation_id"]))
    fixed = db.record_translation("TASK-FIXTURE " + " ".join(nums), **P, **KW, supersedes=tid)
    cur = [x[0] for x in q("SELECT translation_id FROM v_translations_current WHERE source_row_key=? "
                           "AND target_language=?", str(plain["id"]), LB)]
    record("T049-54", "--supersedes retires the translation in place: the old row leaves the current view and the "
                      "new one enters it", cur == [fixed["translation_id"]]
           and q("SELECT superseded_by_translation_id FROM translations WHERE translation_id=?", tid)[0][0]
           == fixed["translation_id"], cur)
    record("T049-55", "--supersedes is refused for a translation already retired",
           refused_for("is not a current translation", db.record_translation, "TASK-FIXTURE " + " ".join(nums),
                       **P, **KW, supersedes=tid))
    dup = db.request_translation("source_value_extractions", "claim_text", str(plain["id"]), LC, JUDGMENT, session=S)
    again = db.request_translation("source_value_extractions", "claim_text", str(plain["id"]), LC, JUDGMENT,
                                   session=S)
    record("T049-56", "a second open request for the same cell, hash and language returns the open one",
           again["translation_id"] == dup["translation_id"] and dup["created"] and not again["created"])
    record("T049-57", "record-translation takes the request or the pointer, never both and never neither",
           refused_for("never both", db.record_translation, kept, translation_id=dup["translation_id"],
                       **{k: v for k, v in P.items() if k != "stage"}, **KW)
           and refused_for("or the whole pointer", db.record_translation, kept, **KW))

    # a cell changed since the request: HAND, on a second copy
    HAND = hand_copy("hand.db")
    os.environ["GUIDEBOOK_DB_PATH"] = HAND
    try:
        rq2 = db.request_translation("source_value_extractions", "claim_text", str(plain["id"]), langs_for(plain, 8)[7],
                                     JUDGMENT, session=S)
        hand_sql(HAND, "UPDATE source_value_extractions SET claim_text = claim_text || ' TASK-FIXTURE' "
                       "WHERE extraction_id=?", plain["id"])                                              # HAND
        record("T049-60", "AT-109 recording against a cell changed since the request is refused",
               refused_for("has changed since", db.record_translation, "TASK-FIXTURE " + " ".join(nums),
                           translation_id=rq2["translation_id"], **KW))
        hand_sql(HAND, "UPDATE translations SET status='translated', translator_kind='model', translator_name='x', "
                       "translated_text='TASK-FIXTURE' WHERE translation_id=?", rq2["translation_id"])   # HAND
        # a reviewed verdict on a cell that has changed is refused; the audit reads the same change as red
        record("T049-61", "a reviewed verdict on a cell changed since it was translated is refused",
               refused_for("no longer matches", db.review_translation, rq2["translation_id"], "reviewed", "model",
                           "test-reviewer", session=S))
        p = subprocess.run([sys.executable, "scripts/audit/translation_pointer_audit.py"], capture_output=True,
                           text=True, env={**os.environ, "GUIDEBOOK_DB_PATH": HAND})
        record("T049-62", "translation_pointer_audit goes red on a stale pointer (a seeded defect on a copy)",
               p.returncode == 1 and "has changed since" in p.stdout, p.stdout + p.stderr)
    finally:
        os.environ["GUIDEBOOK_DB_PATH"] = DB

# a quote that spells its number in words: the numeral of the row's claimed_value may be stated
words = next((r for r in FIGS if r["cv"] and r["cv"].isdigit() and r["cv"] not in NUM.findall(r["text"])
              and not CJK_DIGIT.search(r["text"])), None)
if not words:
    skip("T049-70", "no non-English figure whose claimed_value is a numeral its quote does not state")
else:
    others = NUM.findall(words["text"])
    LW = langs_for(words, 14)[12:]      # languages the earlier cases did not use for any figure
    pw = dict(source_table="source_value_extractions", source_column="claim_text", source_row_key=str(words["id"]),
              target_language=LW[0], stage=JUDGMENT)
    w = db.record_translation("TASK-FIXTURE " + " ".join([words["cv"]] + others), **pw, **KW)
    record("T049-70", "AT-109 a number spelled in words is accepted when the translation states the numeral of the "
                      "row's claimed_value", w["status"] == "translated", w)
    record("T049-71", "AT-109 a number that is neither the quote's nor the claimed_value is still refused",
           refused_for("does not state", db.record_translation,
                       "TASK-FIXTURE " + " ".join([str(int(words["cv"]) + 1000003)] + others),
                       **dict(pw, target_language=LW[1]), **KW))
    record("T049-72", "the claimed_value allowance reaches only a claim_text: the same numeral is refused for another "
                      "text cell of the row",
           db.translation_claimed_value(con, "source_value_extractions", "claim_text", str(words["id"])) == words["cv"]
           and db.translation_claimed_value(con, "source_value_extractions", "setting", str(words["id"])) is None)

# a quote in CJK numerals, stated as Arabic numerals
if not cjk:
    skip("T049-73", "no non-English figure whose quote changes under the CJK converter")
else:
    arabic = NUM.findall(db._cjk_to_arabic(cjk["text"]))
    LJ = langs_for(cjk, 12)[10:]
    pj = dict(source_table="source_value_extractions", source_column="claim_text", source_row_key=str(cjk["id"]),
              target_language=LJ[0], stage=JUDGMENT)
    r = db.record_translation("TASK-FIXTURE " + " ".join(arabic), **pj, **KW)
    record("T049-73", "AT-109 a quote in CJK numerals, translated with Arabic numerals, is accepted",
           r["status"] == "translated", r)
    record("T049-74", "a CJK quote's translation that changes the figure is still refused",
           refused_for("does not state", db.record_translation,
                       "TASK-FIXTURE " + " ".join([str(int(arabic[0]) + 1000003)] + arabic[1:]),
                       **dict(pj, target_language=LJ[1]), **KW))

# the schema's own CHECKs (the review rules are held by the table, not only by the verb), the capture set, the audit
COLS = ("source_table, source_column, source_row_key, source_sha256, target_language, requested_at_stage, "
        "created_at, created_by_session, updated_at, updated_by_session")
VALS = ("'t', 'c', '1', '" + "0" * 64 + "', 'EN', 'judgment', 'now', 's', 'now', 's'")


def insert_refused(extra_cols, extra_vals):
    c = sqlite3.connect(DB)
    try:
        c.execute(f"INSERT INTO translations ({COLS}, {extra_cols}) VALUES ({VALS}, {extra_vals})")
        return False
    except sqlite3.IntegrityError:
        return True
    finally:
        c.rollback()
        c.close()


TRANSLATED = "status, translated_text, translator_kind, translator_name"
record("T049-80", "the schema refuses a rejected row with no review_reason",
       insert_refused(f"{TRANSLATED}, reviewed_by_kind, reviewed_by_name, reviewed_at",
                      "'rejected', 'x', 'model', 'a', 'model', 'b', 'now'"))
record("T049-81", "the schema refuses a requested row that holds a review_reason",
       insert_refused("status, review_reason", "'requested', 'because'"))
record("T049-82", "the schema refuses a reviewer who is the translator",
       insert_refused(f"{TRANSLATED}, reviewed_by_kind, reviewed_by_name, reviewed_at",
                      "'reviewed', 'x', 'model', 'same', 'model', 'same', 'now'"))
record("T049-83", "the schema refuses a translation with no translator and a requested row with text",
       insert_refused("status, translated_text", "'translated', 'x'")
       and insert_refused("status, translated_text", "'requested', 'x'"))
record("T049-84", "a rejected row WITH its reason is accepted by the schema (the CHECK does not refuse everything)",
       not insert_refused(f"{TRANSLATED}, reviewed_by_kind, reviewed_by_name, reviewed_at, review_reason",
                          "'rejected', 'x', 'model', 'a', 'model', 'b', 'now', 'why'"))
record("T049-85", "translations is in the captured set the writers derive", "translations" in dbcore.writable_tables(con))
# the refusals of request/record that the first cases did not hold (found by seeding each away: the suite stayed green)
if not plain or plain["lang"] not in LANGS or len(langs_for(plain, 8)) < 6:
    skip("T049-87..T049-90", "no non-English figure whose language the map holds, or too few other languages")
else:
    LC = langs_for(plain, 8)[5]
    cellp = ("source_value_extractions", "claim_text", str(plain["id"]))
    record("T049-87", "a request in the pointed row's own language is refused: there is nothing to translate",
           refused_for("nothing to translate", db.request_translation, *cellp, plain["lang"], JUDGMENT, session=S))
    record("T049-88", "a blank --session is refused by the request and by the record",
           refused_for("--session is required", db.request_translation, *cellp, LC, JUDGMENT, session="  ")
           and refused_for("--session is required", db.record_translation, "TASK-FIXTURE x", source_table=cellp[0],
                           source_column=cellp[1], source_row_key=cellp[2], target_language=LC, stage=JUDGMENT,
                           translator_kind="model", translator_name="t", session=" "))
    record("T049-89", "a target language the map does not hold is refused",
           refused_for("is not a language lang_jur_map holds", db.request_translation, *cellp, "ZZ-NOT-A-LANGUAGE",
                       JUDGMENT, session=S))
    kinds = sorted(dbcore.check_values(con, "translations", "translator_kind"))
    try:
        db.record_translation("TASK-FIXTURE x", source_table=cellp[0], source_column=cellp[1], source_row_key=cellp[2],
                              target_language=LC, stage=JUDGMENT, translator_kind="zz_not_a_kind",
                              translator_name="t", session=S)
        said = ""
    except Refusal as exc:
        said = str(exc)
    record("T049-90", "a translator kind outside the column's CHECK is refused, naming the kinds the CHECK holds",
           bool(kinds) and all(k in said for k in kinds), said)

audit = subprocess.run([sys.executable, "scripts/audit/translation_pointer_audit.py"], capture_output=True, text=True,
                       env={**os.environ, "GUIDEBOOK_DB_PATH": DB})
n_current = q("SELECT count(*) FROM v_translations_current")[0][0]
record("T049-86", "translation_pointer_audit passes with EXAMINED equal to the current translations the test left",
       audit.returncode == 0 and f"EXAMINED: {n_current}\n" in audit.stdout and n_current > 0,
       audit.stdout + audit.stderr)
finish()
