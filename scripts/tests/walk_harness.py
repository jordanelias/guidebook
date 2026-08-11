#!/usr/bin/env python3
"""
scripts/tests/walk_harness.py — verbatim action/IO logger for structural walk tests.

Every action taken during the trial goes through this module so that the
transcript is a complete record: the exact command or SQL submitted, the exact
stdout/stderr returned, the exit code, and the row-count delta on every table
the action could have touched.

Nothing here writes outside the scratch tree.
"""
import io
import os
import subprocess
import sqlite3
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
CANONICAL_DB = REPO_ROOT / "data" / "guidebook.db"

# The selftest imports this module in subprocesses to prove the guards fire. It must
# therefore be able to load the file itself without tripping them — so the guards run at
# import for every normal use, and are deferred only for the `--selftest` entry point.
_SELFTEST_ENTRY = __name__ == "__main__" and "--selftest" in sys.argv


def _resolve_tree():
    """Resolve the walk tree, refusing anything that would write the real repository."""
    tree = os.environ.get("WALK_TREE")
    if not tree:
        raise RuntimeError(
            "WALK_TREE is not set. This harness runs a walk against a DISPOSABLE COPY of the "
            "repository and refuses to default to the working tree, because emit_and_apply() "
            "writes migrations into <tree>/scripts/migrations/ and applies them to "
            "<tree>/data/guidebook.db. Set WALK_TREE=/path/to/scratch/copy."
        )
    tree = Path(tree).resolve()
    if (tree / "data" / "guidebook.db") == CANONICAL_DB.resolve():
        raise RuntimeError(
            f"REFUSING: WALK_TREE resolves to the canonical repository ({REPO_ROOT}). "
            "CLAUDE.md §4: never write data/guidebook.db directly. Point WALK_TREE at a copy."
        )
    return tree


TREE = None if _SELFTEST_ENTRY else _resolve_tree()
DB = None if TREE is None else TREE / "data" / "guidebook.db"

TRANSCRIPT = None if TREE is None else Path(
    os.environ.get("WALK_TRANSCRIPT", TREE / "walk-transcript.md"))

_seq = 0


def _now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def _w(text):
    with open(TRANSCRIPT, "a", encoding="utf-8") as fh:
        fh.write(text)
        if not text.endswith("\n"):
            fh.write("\n")


def snapshot():
    """Row counts for every table, so any action's side effects are visible."""
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    out = {}
    for (name,) in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    ):
        out[name] = con.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone()[0]
    out["__user_version__"] = con.execute("PRAGMA user_version").fetchone()[0]
    con.close()
    return out


def _delta(before, after):
    keys = set(before) | set(after)
    rows = []
    for k in sorted(keys):
        b, a = before.get(k, "—"), after.get(k, "—")
        if b != a:
            rows.append((k, b, a))
    return rows


def header(stage, title):
    _w(f"\n\n---\n\n## {stage} — {title}\n")


def note(text):
    _w("\n" + textwrap.dedent(text).strip() + "\n")


def _fmt_output(label, s, limit=6000):
    s = s if s is not None else ""
    if not s.strip():
        return f"**{label}:** _(empty)_\n"
    trunc = ""
    if len(s) > limit:
        trunc = f"\n... [TRUNCATED — {len(s)} chars total, first {limit} shown] ..."
        s = s[:limit]
    return f"**{label}:**\n```\n{s.rstrip()}{trunc}\n```\n"


def run(cmd, label=None, cwd=None, env_extra=None, track=True):
    """Run a command, logging argv, cwd, env overrides, rc, stdout, stderr, deltas."""
    global _seq
    _seq += 1
    before = snapshot() if track else None
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run(
        cmd, cwd=str(cwd or TREE), capture_output=True, text=True, env=env
    )
    after = snapshot() if track else None

    _w(f"\n### [{_seq:03d}] {label or ' '.join(cmd)}   `{_now()}Z`\n")
    _w(f"**Type:** COMMAND\n")
    _w(f"**Argv:** `{cmd}`\n")
    _w(f"**Cwd:** `{cwd or TREE}`\n")
    if env_extra:
        _w(f"**Env overrides:** `{env_extra}`\n")
    _w(f"**Exit code:** `{proc.returncode}`\n")
    _w(_fmt_output("stdout", proc.stdout))
    if proc.stderr.strip():
        _w(_fmt_output("stderr", proc.stderr))
    if track:
        d = _delta(before, after)
        if d:
            _w("**Table deltas:**\n\n| table | before | after |\n|---|---|---|\n" +
               "\n".join(f"| `{k}` | {b} | {a} |" for k, b, a in d) + "\n")
        else:
            _w("**Table deltas:** none\n")
    return proc


def query(sql, params=(), label=None, expect=None):
    """Read-only query against the scratch DB, logging SQL and full result set."""
    global _seq
    _seq += 1
    con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    _w(f"\n### [{_seq:03d}] {label or 'query'}   `{_now()}Z`\n")
    _w("**Type:** QUERY (read-only)\n")
    _w(f"**SQL:**\n```sql\n{textwrap.dedent(sql).strip()}\n```\n")
    if params:
        _w(f"**Params:** `{params}`\n")
    try:
        cur = con.execute(sql, params)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
    except Exception as exc:
        _w(f"**RESULT: ERROR** — `{type(exc).__name__}: {exc}`\n")
        con.close()
        return None
    con.close()
    if not rows:
        _w("**Rows returned:** 0 _(empty result set)_\n")
    else:
        _w(f"**Rows returned:** {len(rows)}\n\n")
        _w("| " + " | ".join(cols) + " |")
        _w("|" + "|".join("---" for _ in cols) + "|")
        for r in rows[:60]:
            cells = ["" if v is None else str(v).replace("|", "\\|").replace("\n", " ")
                     for v in r]
            cells = [c if len(c) <= 220 else c[:220] + "…" for c in cells]
            _w("| " + " | ".join(cells) + " |")
        if len(rows) > 60:
            _w(f"\n_({len(rows) - 60} further rows omitted)_")
    if expect is not None:
        got = len(rows)
        verdict = "AS PREDICTED" if got == expect else "**NOT AS PREDICTED**"
        _w(f"\n**Predicted row count:** {expect} · **actual:** {got} → {verdict}\n")
    return rows


def emit_and_apply(session, summary, sql, label, expect_fail=False):
    """
    The sanctioned write path, exercised exactly as CLAUDE.md §4 documents it:
    emit_data_migration.py --input <file>  then  migrate_db.py.
    Logs the emitted migration file verbatim.
    """
    global _seq
    tmp = Path(__file__).resolve().parent / "payload.sql"
    tmp.write_text(sql)

    _w(f"\n### [{_seq + 1:03d}] {label} — EMIT\n")
    _w("**Type:** SQL-EMIT (sanctioned write path, step 1 of 2)\n")
    _w(f"**Payload submitted to `--input`:**\n```sql\n{sql.strip()}\n```\n")

    p1 = run(
        ["python3", "scripts/emit_data_migration.py",
         "--session", session, "--summary", summary, "--input", str(tmp)],
        label=f"{label} — emit_data_migration.py",
    )
    emitted = None
    for line in (p1.stdout + p1.stderr).splitlines():
        line = line.strip()
        if "scripts/migrations/data_" in line:
            for tok in line.replace("\t", " ").split():
                if "scripts/migrations/data_" in tok:
                    emitted = tok.strip().rstrip(":,")
                    break
    if emitted:
        path = TREE / emitted if not os.path.isabs(emitted) else Path(emitted)
        if path.exists():
            _w(f"\n**Emitted migration file:** `{emitted}`\n")
            _w(f"```sql\n{path.read_text()}\n```\n")

    p2 = run(["python3", "scripts/migrate_db.py"], label=f"{label} — migrate_db.py (apply)")
    if expect_fail:
        _w(f"\n**Expectation:** this write was expected to be REJECTED. "
           f"apply rc={p2.returncode} → "
           f"{'REJECTED as predicted' if p2.returncode != 0 else '**ACCEPTED — NOT AS PREDICTED**'}\n")
    return p1, p2


def finding(tag, verdict, text):
    _w(f"\n> **{tag} — {verdict}**\n>\n" +
       "\n".join(f"> {ln}" for ln in textwrap.dedent(text).strip().splitlines()) + "\n")


def _selftest():
    """Verify the guards and the logging path. Exits 0/1 per house convention.

    Run:  python3 scripts/tests/walk_harness.py --selftest
    """
    import subprocess as _sp
    here = Path(__file__).resolve()
    root = here.parent.parent.parent
    checks = []

    def _import_with(env):
        e = dict(os.environ); e.pop("WALK_TREE", None); e.update(env)
        return _sp.run([sys.executable, "-c",
                        f"import sys; sys.path.insert(0, {str(here.parent)!r}); import walk_harness"],
                       capture_output=True, text=True, env=e)

    r = _import_with({})
    checks.append(("refuses when WALK_TREE is unset",
                   r.returncode != 0 and "WALK_TREE is not set" in r.stderr))

    r = _import_with({"WALK_TREE": str(root)})
    checks.append(("refuses when WALK_TREE is the canonical repository",
                   r.returncode != 0 and "REFUSING" in r.stderr))

    import tempfile
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "data").mkdir()
        import sqlite3 as _s
        c = _s.connect(str(Path(td) / "data" / "guidebook.db"))
        c.execute("CREATE TABLE t (x INTEGER)"); c.commit(); c.close()
        r = _import_with({"WALK_TREE": td})
        checks.append(("accepts a disposable tree", r.returncode == 0))

    for name, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    bad = sum(1 for _, ok in checks if not ok)
    print(f"RESULTS: {len(checks) - bad}/{len(checks)} checks passed")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    sys.exit("walk_harness is a library; run a walk script that imports it, or --selftest")
