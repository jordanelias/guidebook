#!/usr/bin/env python3
"""Stress script, round 2: COVERAGE. Every db.py verb, every audit/validate/research tool, every registry
battery, and a real-source chain through the verbs round 1 never reached (citation mining, relations, conflicts,
gates, supersession, cross-referencing, economics, case studies, amendments, merge/decline), all on scratch copies,
all logged with the round-1 harness (stress_run.Run): argv, rc, full stdout/stderr, row deltas, canonical hash.

    python3 -I stress_run2.py [--out DIR] [--parts sweep,tools,chain]

It does not judge. Arguments are built mechanically from each verb's own usage text (required options only) and
real values read from the DB, so a refusal here is as likely to be a semantic refusal (right or wrong) as a script
shortfall; the log keeps the exact argv so the auditor can tell. Where a verb has --dry-run, the sweep uses it on a
fresh copy; every other verb runs for real on its own fresh copy.
"""
import argparse, json, re, shutil, subprocess, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stress_run import Run, rows, sha, CANON, REPO, PY, SCRATCH, HERE  # noqa: E402


def usage_required(verb):
    p = subprocess.run([PY, "-I", "scripts/db.py", verb, "-h"], cwd=REPO, capture_output=True, text=True)
    txt = p.stdout
    m = re.search(r"usage:.*?(?:\n\n|\Z)", txt, re.S)
    u = " ".join(m.group(0).split()) if m else ""
    u = u.split(verb, 1)[1] if verb in u else u
    toks, depth, cur = [], 0, ""
    for ch in u:
        if ch == "[":
            depth += 1
        if ch == "]":
            depth -= 1
            continue
        if depth == 0:
            if ch == " ":
                if cur:
                    toks.append(cur)
                    cur = ""
            else:
                cur += ch
    if cur:
        toks.append(cur)
    req, i = [], 0
    while i < len(toks):
        t = toks[i]
        if t.startswith("--"):
            nxt = toks[i + 1] if i + 1 < len(toks) and not toks[i + 1].startswith("-") else None
            req.append((t, nxt))
            i += 2 if nxt else 1
        elif not t.startswith("-"):
            req.append((None, t))
            i += 1
        else:
            i += 1
    return req, "--dry-run" in txt


def ctx(db):
    q = lambda s, d=None: (rows(db, s) or [[d]])[0][0]
    return dict(
        ref=q("select ref_id from source_value_extractions order by extraction_id limit 1", "REF-00139"),
        ref2=q("select ref_id from evidence_sources order by ref_id desc limit 1", "REF-00139"),
        ext=q("select min(extraction_id) from source_value_extractions", 1),
        ext2=q("select max(extraction_id) from source_value_extractions", 2),
        claim=q("select claim_text from source_value_extractions order by extraction_id limit 1", "STRESS-FIXTURE"),
        obs=q("select min(observation_id) from observed_terms", 1),
        gap=q("select min(gap_id) from gaps", 1),
        cand=q("select min(candidate_id) from search_candidates", 1),
        exec=q("select min(exec_id) from search_executions", 1),
        spec=q("select min(specification_id) from specifications", 1),
        conn=q("select min(con_id) from connections", None) or "CON-1",
        slug=q("select slug from slugs order by slug limit 1", "x"),
        term=q("select term_id from terms order by term_id limit 1", "TERM-001"),
        param=q("select min(parameter_id) from base_parameters", 3),
        scan=q("select min(scan_id) from source_scans", 1),
        gate=q("select min(gate_id) from determination_gates", 1),
    )


def value_for(flag, meta, c, sess):
    f = (flag or "").lstrip("-")
    if meta and meta.startswith("{"):
        return meta.strip("{}").split(",")[0]
    table = [
        (("session",), sess), (("dry-run",), None),
        (("ref-id", "ref", "local-ref-id", "mined-ref-id", "root-ref-id", "superseded-ref", "new-ref"), c["ref"]),
        (("to-extraction", "echo-of"), str(c["ext2"])), (("extraction-id", "extraction", "from", "from-extraction"), str(c["ext"])),
        (("parameter-id", "target-parameter-id", "parameter", "into", "merge-into", "from-parameter"), str(c["param"])),
        (("term-id", "distinct-from"), c["term"]), (("observation-id", "from-observation"), str(c["obs"])),
        (("gap-id",), str(c["gap"])), (("candidate-id",), str(c["cand"])), (("exec-id",), str(c["exec"])),
        (("specification-id",), str(c["spec"])), (("gate-id",), str(c["gate"])), (("scan-id",), str(c["scan"])),
        (("con-id", "connection-id"), c["conn"]), (("conflict-id",), "1"),
        (("slug", "found-under-slug", "suggested-slug", "target-slug", "filed-in", "to-slug", "from-slug"), c["slug"]),
        (("identity", "population"), "MOB"), (("icf", "icf-code"), "d450"), (("needs",), "A-AT"),
        (("claim-text", "quote", "context-quote", "surfaced-quote"), c["claim"][:200]),
        (("file-sha256", "sha256"), "0" * 64), (("year",), "2020"), (("pages",), "1-2"),
        (("jurisdiction",), "UK"), (("language",), "en"), (("stamp",), "2026-11-12 00:00:00"),
        (("claimed-value",), "1"), (("claimed-unit",), "mm"),
    ]
    for keys, v in table:
        if f in keys:
            return v
    if meta and re.search(r"(ID|INT|N|YEAR|COUNT)$", meta):
        return "1"
    return "STRESS-FIXTURE"


def build_args(verb, c, sess):
    req, has_dry = usage_required(verb)
    args = []
    for flag, meta in req:
        if flag is None:
            args.append("STRESS-FIXTURE")
            continue
        v = value_for(flag, meta, c, sess)
        if v is None:
            continue
        args += [flag, v] if meta else [flag]
    return args, has_dry


def part_sweep(out):
    R = Run("sweep", out)
    src = (REPO / "scripts/db.py").read_text()
    verbs = sorted(set(re.findall(r'sub\.add_parser\(\s*"([\w-]+)"', src)))
    c = ctx(CANON)
    for v in verbs:
        args, has_dry = build_args(v, c, R.sess)
        fresh = R.scratch / f"v-{v}.db"
        shutil.copyfile(CANON, fresh)
        argv = [PY, "-I", "scripts/db.py", v, *args] + (["--dry-run"] if has_dry else [])
        R.step(f"verb.{v}", f"{v}: mechanically-built required args from real DB values; {'--dry-run' if has_dry else 'real run on a fresh copy'}", argv, db=fresh)
    R.note("sweep.coverage", "every db.py verb invoked", {"verbs": len(verbs), "invoked": len([x for x in R.index if '.verb.' in x[0]])})
    finish_(R)


def part_tools(out):
    R = Run("tools", out)
    before = subprocess.run(["git", "status", "--porcelain", "--", ".", ":!scratchpad", ":!transcripts"], cwd=REPO, capture_output=True, text=True).stdout
    audits = sorted(p for p in (REPO / "scripts/audit").glob("*.py"))
    for p in audits:
        R.step(f"audit.{p.stem}", f"{p.name} run bare on a scratch DB: examines something, or says what it needs", [PY, "-I", str(p.relative_to(REPO))], timeout=300)
    for p in sorted((REPO / "scripts").glob("validate_*.py")) + [REPO / "scripts/doctrine_recheck.py"]:
        R.step(f"validate.{p.stem}", f"{p.name} bare", [PY, "-I", str(p.relative_to(REPO))], timeout=300)
    for p in sorted((REPO / "scripts/research").glob("*.py")):
        R.step(f"research.{p.stem}.help", f"{p.name} --help", [PY, "-I", str(p.relative_to(REPO)), "-h"])
    R.step("research.mining_screen.compare", "citation-mining screens compared over deposited references", [PY, "-I", "scripts/research/mining_screen.py", "--all", "--compare"])
    R.step("registry.list", "registry + quarantine, runs nothing", [PY, "-I", "scripts/run_checks.py", "--list"])
    for b in ("syntax", "structure", "data", "db_integrity", "schema", "governance", "attestation", "research", "render", "tests"):
        R.step(f"registry.battery.{b}", f"battery {b} on the scratch DB", [PY, "-I", "scripts/run_checks.py", "--battery", b], timeout=900)
    R.step("registry.selftest", "selftest (where a rename fails)", [PY, "-I", "scripts/run_checks.py", "--selftest"], timeout=600)
    R.step("registry.changed-from-main", "diff-scoped gate against origin/main, explained", [PY, "-I", "scripts/run_checks.py", "--changed-from", "origin/main", "--explain"], timeout=900)
    after = subprocess.run(["git", "status", "--porcelain", "--", ".", ":!scratchpad", ":!transcripts"], cwd=REPO, capture_output=True, text=True).stdout
    R.note("tools.repo-tree-changed-by-tools", "no tool wrote into the repository tree outside scratchpad/transcripts", {"before": before, "after": after, "changed": before != after})
    finish_(R)


def part_chain(out):
    """A real held source through the verbs round 1 never reached, in one persistent scratch DB, ids re-read between steps."""
    R = Run("chain", out)
    S = R.sess
    ref = "REF-00139"
    sc = rows(R.db, "select file_sha256 from source_scans where ref_id=? and text_scope='full' limit 1", (ref,))
    ex = rows(R.db, "select extraction_id,parameter_id,claim_text,claimed_value,claimed_unit,claim_type from source_value_extractions where ref_id=? order by extraction_id limit 1", (ref,))
    R.note("chain.anchor", "a real held source with a full-text scan and extractions", {"ref": ref, "scan_sha": sc, "extraction": ex})
    if sc and ex:
        eid, pid, claim, val, unit, ctype = ex[0]
        R.dbpy("chain.record-scan-real", "a real full reading names bytes the retrieval log holds", "record-scan", "--ref-id", ref, "--mode", "catalogue", "--text-scope", "full",
               "--file-sha256", sc[0][0], "--method", "full-read", "--session", S)
        words = re.findall(r"[A-Za-z]{4,}", claim)
        if len(words) >= 2:
            R.dbpy("chain.observe-term-real", "a phrase observed verbatim from the held text", "observe-term", "--ref-id", ref, "--surface-form", " ".join(words[:2]), "--language", "en",
                   "--locator", "STRESS-FIXTURE locator", "--context-quote", claim[:200], "--session", S)
        R.dbpy("chain.add-extraction-second-row", "a dissenting/second row for an already extracted figure under another lens (D-0168 contest)", "add-extraction", "--ref-id", ref, "--parameter-id", str(pid),
               "--claim-type", ctype or "numerical", *(["--claimed-value", str(val)] if val is not None else []), *(["--claimed-unit", unit] if unit else []), "--claim-text", claim[:300],
               "--extraction-method", "full-read", "--identity", "DEAF", "--figure-role", "claim", "--relation", "none", "--session", S)
    c = ctx(R.db)
    for v in ("is-mined", "log-mining", "unmined", "add-locator", "update-locator", "link-source-slug", "link-admission", "unlink-admission", "add-population-match", "amend-population-match",
              "add-case-study", "add-economics-entry", "add-supersession-check", "supersede-source", "correct-source", "amend-source", "amend-extraction", "relate-extraction",
              "derive-extraction", "raise-follow-up", "resolve-follow-up", "add-conflict", "update-conflict", "conflicts", "connections", "update-connection", "delete-connection",
              "add-code-lead", "update-code-lead", "add-alias", "amend-term", "rename-term", "decline-parameter", "revoke-declination", "annotate-parameter", "set-parameter-direction",
              "merge-parameter", "raise-determination-gate", "resolve-determination-gate", "retire-specification", "record-adversarial-pass", "dispose-adversarial-finding",
              "close-adversarial-pass", "add-gap-mining", "close-gap", "amend-gap", "update-gap-addressability", "gaps", "next-id"):
        c = ctx(R.db)
        args, has_dry = build_args(v, c, S)
        R.step(f"chain.verb.{v}", f"{v} in sequence on the persistent chain DB with ids re-read from it", [PY, "-I", "scripts/db.py", v, *args])
    # determination after the chain, and the replay
    fresh = R.scratch / "chain-assess.db"
    shutil.copyfile(R.db, fresh)
    if ex:
        R.step("chain.assess-after-chain", "determine the anchor's parameter after the chain's additions", [PY, "-I", "scripts/assess/assess_cell.py", "--db", str(fresh), "--emit-sql", str(R.scratch / "chain.sql"),
               "--parameter-id", str(ex[0][1]), "--slug", "accessible-circulation-geometry", "--identity", "MOB", "--session", S, "--stamp", "2026-11-12 00:00:00",
               "--report-json", str(R.out / "chain-assess.json")], db=fresh)
    out_sql = R.scratch / "batch.sql"
    R.step("chain.emit-batch-sql", "capture everything the chain wrote", [PY, "-I", "scripts/research/emit_batch_sql.py", "--scratch", str(R.db), "--canonical", str(CANON), "--out", str(out_sql)])
    finish_(R)


def finish_(R):
    from stress_run import finish
    finish(R)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "results2"))
    ap.add_argument("--parts", default="sweep,chain,tools")
    a = ap.parse_args()
    s0 = sha(CANON)
    for part in a.parts.split(","):
        {"sweep": part_sweep, "chain": part_chain, "tools": part_tools}[part](a.out)
    print("canonical sha256 before/after:", s0, sha(CANON), "UNCHANGED" if s0 == sha(CANON) else "!!! MOVED !!!")


if __name__ == "__main__":
    main()
