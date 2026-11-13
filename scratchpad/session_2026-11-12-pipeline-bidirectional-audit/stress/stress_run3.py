#!/usr/bin/env python3
"""Stress script, round 3: DEPTH. Fixes the round-1/2 script faults the audit named (hs-stress-audit.md §4, W-1..W-11) and
runs its seven further scenarios on a REAL held source (REF-00139): read to the end, evidenced cells across lenses with the
gates, the write path with a determination compared by content, parallel batches at capture, the fidelity guards through
the writers, the parameter life cycle, and backward/re-entry in rows. Plus every registry battery run correctly.

    python3 -I stress_run3.py --out DIR [--parts real,guards,batches,lifecycle,reentry,batteries,probes]

Scratch copies only; the canonical DB is never written (hash recorded around every step). It does not judge.
Faults it corrects: the observed phrase is a CONTIGUOUS bigram of the quote; every extraction carries a locator;
batteries run as `--battery <name> --all`; no placeholder arguments on the steps that matter; engine runs share ONE
database per scenario so the gates and views see the determination.
"""
import argparse, json, re, shutil, sqlite3, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stress_run import Run, rows, sha, CANON, REPO, PY, SCRATCH, HERE, counts  # noqa: E402
from stress_run2 import ctx, build_args, finish_  # noqa: E402

REF = "REF-00139"
SLUG = "accessible-circulation-geometry"


def anchor(db):
    sc = rows(db, "select file_sha256 from source_scans where ref_id=? and text_scope='full' limit 1", (REF,))
    ex = rows(db, "select extraction_id,parameter_id,claim_text,claimed_value,claimed_unit,claim_type,source_section,comparator from source_value_extractions where ref_id=? order by extraction_id limit 1", (REF,))
    return (sc[0][0] if sc else None), (ex[0] if ex else None)


def bigram(claim):
    m = re.search(r"([A-Za-z]{4,}) ([A-Za-z]{4,})", claim)
    return m.group(0) if m else None


def loc_args(db):
    """The structured locator of the anchor extraction, as add-extraction flags (a tier-6 row needs one)."""
    cols = ["locator_scheme", "loc_division", "loc_part", "loc_section", "loc_subsection", "loc_paragraph", "loc_clause", "loc_subclause"]
    r = rows(db, "select " + ",".join(cols) + " from source_value_extractions where ref_id=? order by extraction_id limit 1", (REF,))
    out = []
    if r:
        for c, v in zip(cols, r[0]):
            if v:
                out += ["--" + c.replace("_", "-"), str(v)]
    return out


def cmp_args(ex):
    """The anchor row's comparator as an add-extraction flag, when it has one (a value-supplying numerical row needs it)."""
    return ("--comparator", ex[7]) if ex[7] else ()


def free_lens(db, ex):
    """The first active identity code on which the anchor's source and parameter hold no extraction yet (derived, not typed)."""
    r = rows(db, "select identity_code from base_taxonomy_identity i where status='active' and not exists (select 1 from source_value_extractions e where e.ref_id=? and e.parameter_id=? and e.identity_code=i.identity_code) order by identity_code limit 1", (REF, ex[1]))
    return r[0][0] if r else None


def has_cell(db, ex, lens):
    return bool(rows(db, "select 1 from source_value_extractions where ref_id=? and parameter_id=? and identity_code=? limit 1", (REF, ex[1], lens)))


def add_ext(R, tag, ex, lens, value=None, unit=None, expect="a correctly cited second row under another lens is accepted", db=None, extra=()):
    eid, pid, claim, val, u, ctype, sect, _cmp = ex
    extra = (*loc_args(db or R.db), *cmp_args(ex), *extra)
    return R.dbpy(tag, expect, "add-extraction", "--ref-id", REF, "--parameter-id", str(pid), "--claim-type", ctype or "numerical",
                  "--claimed-value", str(value if value is not None else val), "--claimed-unit", (unit if unit is not None else u) or "",
                  "--claim-text", claim[:300], "--source-section", sect or "STRESS table", "--extraction-method", "full-read", "--identity", lens,
                  "--figure-role", "claim", "--relation", "none", "--session", R.sess, *extra, db=db)


def gates(R, tag, db):
    for name, cmd in (("test_db_integrity", ["scripts/tests/test_db_integrity.py"]), ("validate_evidence_state", ["scripts/validate_evidence_state.py"]),
                      ("derivation_handshake", ["scripts/audit/derivation_handshake_integrity.py"]), ("medical_lens", ["scripts/audit/medical_lens_integrity.py"]),
                      ("verified_scan", ["scripts/audit/verified_scan_integrity.py"]), ("judgment_handoff", ["scripts/audit/judgment_handoff_shape.py"])):
        R.step(f"{tag}.gate.{name}", f"{name} on the database holding the determination: does it examine it, and does it go red on a wrong-lens/unverified one?", [PY, "-I", *cmd], db=db, timeout=600)


def part_real(out):
    R = Run("real", out)
    S = R.sess
    sha_, ex = anchor(R.db)
    R.note("real.anchor", "held source with a full-text scan and an extraction", {"ref": REF, "sha": sha_, "extraction": ex})
    if not (sha_ and ex):
        return finish_(R)
    claim = ex[2]
    R.dbpy("real.record-scan", "a full reading naming held bytes", "record-scan", "--ref-id", REF, "--mode", "catalogue", "--text-scope", "full", "--file-sha256", sha_, "--method", "full-read", "--open-pass-done", "--session", S)
    bg = bigram(claim)
    if bg:
        R.dbpy("real.observe-term", "a contiguous phrase observed verbatim with locator and quote", "observe-term", "--ref-id", REF, "--surface-form", bg, "--language", "en",
               "--locator", ex[6] or "STRESS locator", "--context-quote", claim[:200], "--session", S)
        obs = rows(R.db, "select max(observation_id) from observed_terms")[0][0]
        term = rows(R.db, "select t.term_id from base_parameters p join terms t using(term_id) where p.parameter_id=?", (ex[1],))[0][0]
        R.dbpy("real.adjudicate-names-existing", "the observation names the existing parameter's term", "adjudicate-term", "--observation-id", str(obs), "--outcome", "NAMES-EXISTING", "--term-id", term,
               "--rationale", "STRESS-FIXTURE: the phrase names the existing parameter", "--session", S)
    for lens in ("MOB", "SCI", "MS", "ALL"):
        if has_cell(R.db, ex, lens):
            R.note(f"real.add-extraction.{lens}.skipped", "the anchor (or an earlier step) already carries this cell: a repeat is refused as a byte-identical copy, which proves nothing", {"lens": lens, "parameter_id": ex[1]})
            continue
        add_ext(R, f"real.add-extraction.{lens}", ex, lens)
    e = rows(R.db, "select extraction_id from source_value_extractions where ref_id=? order by extraction_id desc limit 2", (REF,))
    if len(e) == 2:
        R.dbpy("real.relate-extraction", "a condition edge between two rows of the same source", "relate-extraction", "--from", str(e[0][0]), "--relation", "condition_on", "--to-extraction", str(e[1][0]), "--stated", "inferred", "--quote", ex[2][:120], "--session", S)
    R.dbpy("real.add-population-match", "grade population-of-study vs population-served (R13)", "add-population-match", "--ref-id", REF, "--target-population", "MOB", "--match-grade", "PROXY",
           "--mismatch-note", "STRESS-FIXTURE: study population not stated", "--session", S)
    # engine on the SAME database, several lenses; gates and views after each
    icf = rows(R.db, "select icf_code from base_icf where icf_code like 'd4%' order by 1 limit 1")[0][0]
    need = rows(R.db, "select need_code from access_needs order by 1 limit 1")[0][0]
    for kind, code in (("identity", "MOB"), ("identity", "SCI"), ("identity", "MS"), ("identity", "ALL"), ("icf", icf), ("needs", need)):
        R.step(f"real.assess.p{ex[1]}.{kind}.{code}", f"determine parameter {ex[1]} under {kind}={code} on the SAME database that holds the extractions", [PY, "-I", "scripts/assess/assess_cell.py", "--db", str(R.db),
               "--emit-sql", str(R.scratch / f"assess-{kind}-{code}.sql"), "--parameter-id", str(ex[1]), "--slug", SLUG, f"--{kind}", code, "--session", S, "--stamp", "2026-11-12 00:00:00",
               "--report-json", str(R.out / f"assess-{kind}-{code}.json")])
    R.sql("real.determinations", "determinations written", "select specification_id,parameter_id,identity_code,icf_code,needs_code,state,marker,value_min,value_max,value_unit from specifications where created_by_session=?", (S,))
    R.sql("real.render-views", "render views over the determination", "select (select count(*) from v_best_practice), (select count(*) from v_determination_provenance)")
    gates(R, "real", R.db)
    # write path with a determination, compared by content
    out_sql = R.scratch / "batch.sql"
    canon_copy = R.scratch / "canonical-copy.db"
    shutil.copyfile(CANON, canon_copy)
    R.step("real.emit-batch-sql", "capture the judgment + specification delta", [PY, "-I", "scripts/research/emit_batch_sql.py", "--scratch", str(R.db), "--canonical", str(canon_copy), "--out", str(out_sql)])
    clone = R.scratch / "clone"
    shutil.rmtree(clone, ignore_errors=True)  # a reused clone keeps the previous run's migration
    R.step("real.clone", "local clone", ["git", "clone", "--quiet", str(REPO), str(clone)])
    if out_sql.exists() and out_sql.stat().st_size:
        R.step("real.emit-data-migration", "migration file in the clone", [PY, "-I", "scripts/emit_data_migration.py", "--session", S + ".md", "--summary", "STRESS-FIXTURE real chain", "--input", str(out_sql),
               "--output-dir", str(clone / "scripts/migrations")], cwd=clone, db=canon_copy)
        R.step("real.migrate-rebuild", "rebuild from history in the clone", [PY, "-I", "scripts/migrate_db.py", "--rebuild", str(R.scratch / "rebuilt.db")], cwd=clone, db=canon_copy, timeout=600)
        if (R.scratch / "rebuilt.db").exists():
            a, b = counts(R.db), counts(R.scratch / "rebuilt.db")
            R.note("real.rebuilt-vs-scratch-counts", "rebuilt equals scratch by row count", {t: [a.get(t), b.get(t)] for t in sorted(set(a) | set(b)) if a.get(t) != b.get(t)} or {"differences": 0})
            R.step("real.migration-reproducibility-deep", "content comparison, every row (advisory)", [PY, "-I", "scripts/audit/migration_reproducibility.py", "--deep"], cwd=clone, db=R.scratch / "rebuilt.db", timeout=900)
    # backward from the live determination
    R.sql("real.backward.provenance", "determination -> sources by the provenance view", "select * from v_determination_provenance limit 40")
    finish_(R)


def part_guards(out):
    R = Run("guards", out)
    S = R.sess
    sha_, ex = anchor(R.db)
    if not (sha_ and ex):
        return finish_(R)
    lens = free_lens(R.db, ex)
    if not lens:
        R.note("guards.skip", "an active lens with no extraction on the anchor's source and parameter exists", {"parameter_id": ex[1]})
        return finish_(R)
    R.note("guards.lens", "the lens the guard cases use, derived by query", {"lens": lens})
    base = R.scratch / "guards-base.db"
    shutil.copyfile(R.db, base)
    R.dbpy("guards.record-scan", "scan recorded so the writer reaches its fidelity guards", "record-scan", "--ref-id", REF, "--mode", "catalogue", "--text-scope", "full", "--file-sha256", sha_, "--method", "full-read", "--session", S, db=base)
    cases = [("control-exact", ex[3], ex[4]), ("digit-substring", "1:1", ex[4]), ("decimal-shift", "1.2", ex[4]), ("extra-digit", "1:120", ex[4]), ("drop-colon", "112", ex[4]),
             ("number-in-words", "twelve", ex[4]), ("fullwidth-digits", "１：１２", ex[4]), ("unit-in-prose", ex[3], "mm per metre of rise (stated 1:12)")]
    for name, v, u in cases:
        fresh = R.scratch / f"g-{name}.db"
        shutil.copyfile(base, fresh)
        add_ext(R, f"guards.{name}", ex, lens, value=v, unit=u, expect=f"claimed value {v!r} against a quote holding {ex[3]!r}: control accepted, mismatches refused", db=fresh)
    # quote variants: a mark-only edit, a mixed-script substitution
    for name, q in (("quote-extra-space", claim_variant(ex[2], lambda s: s.replace(" ", "  ", 1))), ("quote-homoglyph", claim_variant(ex[2], lambda s: s.replace("a", "а", 1))),
                    ("quote-truncated", ex[2][: max(40, len(ex[2]) // 2)])):
        fresh = R.scratch / f"g-{name}.db"
        shutil.copyfile(base, fresh)
        R.dbpy(f"guards.{name}", "a quote altered only by whitespace/homoglyph is judged against the held text", "add-extraction", "--ref-id", REF, "--parameter-id", str(ex[1]), "--claim-type", "numerical",
               "--claimed-value", str(ex[3]), "--claimed-unit", ex[4] or "", "--claim-text", q[:300], "--source-section", ex[6] or "STRESS", "--extraction-method", "full-read", "--identity", lens,
               "--figure-role", "claim", "--relation", "none", "--session", S, *loc_args(R.db), *cmp_args(ex), db=fresh)
    finish_(R)


def claim_variant(s, f):
    return f(s)


def part_batches(out):
    """Two independently captured batches against ONE history: does capture catch the collision, and what does it say?"""
    R = Run("batches", out)
    a, b = SCRATCH / "acoustics" / "topic.db", SCRATCH / "reach" / "topic.db"
    if not (a.exists() and b.exists()):
        R.note("batches.skip", "round-1 scratch DBs present", {"missing": [str(p) for p in (a, b) if not p.exists()]})
        return finish_(R)
    canon_a = R.scratch / "canon-with-A.db"
    shutil.copyfile(CANON, canon_a)
    R.step("batches.capture-A", "capture batch A against canonical", [PY, "-I", "scripts/research/emit_batch_sql.py", "--scratch", str(a), "--canonical", str(CANON), "--out", str(R.scratch / "A.sql")], db=canon_a)
    if (R.scratch / "A.sql").exists():
        con = sqlite3.connect(canon_a)
        try:
            con.executescript((R.scratch / "A.sql").read_text())
            con.commit()
        except Exception as e:  # noqa
            R.note("batches.apply-A", "batch A applies to canonical's copy", {"error": repr(e)})
        finally:
            con.close()
    R.step("batches.capture-B-against-A", "capture batch B against a history that already holds A: refused at capture, collided, or silently accepted?", [PY, "-I", "scripts/research/emit_batch_sql.py",
           "--scratch", str(b), "--canonical", str(canon_a), "--out", str(R.scratch / "B.sql")], db=canon_a)
    finish_(R)


def part_lifecycle(out):
    R = Run("lifecycle", out)
    S = R.sess
    sha_, ex = anchor(R.db)
    t = rows(R.db, "select t.term_id from terms t where t.canonical_en like 'thermal comfort' and not exists (select 1 from base_parameters p where p.term_id=t.term_id)")
    if not (t and sha_):
        R.note("lifecycle.skip", "an unparameterised term and a held scan exist", {"term": t, "sha": sha_})
        return finish_(R)
    R.sql("lifecycle.ledger-before", "v_scan_ledger distribution before", "select status,count(*) from v_scan_ledger group by 1")
    R.dbpy("lifecycle.add-parameter", "define a parameter dynamically", "add-parameter", "--term-id", t[0][0], "--session", S)
    new = rows(R.db, "select max(parameter_id) from base_parameters")[0][0]
    R.sql("lifecycle.ledger-after-define", "every source now owes the new parameter", "select status,count(*) from v_scan_ledger group by 1")
    R.dbpy("lifecycle.targeted-scan", "read ONE source against the new parameter", "record-scan", "--ref-id", REF, "--mode", "targeted", "--target-parameter-id", str(new), "--text-scope", "full", "--file-sha256", sha_, "--method", "full-read", "--session", S)
    R.sql("lifecycle.ledger-after-targeted", "that source's pair is discharged, the rest stay owed", "select status,count(*) from v_scan_ledger group by 1")
    into = rows(R.db, "select parameter_id from base_parameters p where status='active' and parameter_id<>? and not exists (select 1 from determination_gates g where g.parameter_id=p.parameter_id and g.resolved_at is null) order by parameter_id limit 1", (new,))
    if not into:
        R.note("lifecycle.skip-merge", "an active parameter with no open gate exists to merge into", {"new": new})
        return finish_(R)
    into = into[0][0]
    R.dbpy("lifecycle.merge-parameter", "merge the new parameter into another with no open gate (a change of grain)", "merge-parameter", "--from", str(new), "--into", str(into), "--reason", "STRESS-FIXTURE: change of grain", "--session", S)
    R.sql("lifecycle.ledger-after-merge", "what a change of grain did to completed scans", "select status,count(*) from v_scan_ledger group by 1")
    R.dbpy("lifecycle.retire-parameter", "retire a parameter with no open gate", "retire-parameter", "--parameter-id", str(into), "--reason", "STRESS-FIXTURE", "--session", S)
    R.sql("lifecycle.ledger-after-retire", "ledger after retire", "select status,count(*) from v_scan_ledger group by 1")
    finish_(R)


def part_reentry(out):
    R = Run("reentry", out)
    S = R.sess
    sha_, ex = anchor(R.db)
    if not (sha_ and ex):
        return finish_(R)
    R.dbpy("reentry.record-scan", "scan", "record-scan", "--ref-id", REF, "--mode", "catalogue", "--text-scope", "full", "--file-sha256", sha_, "--method", "full-read", "--session", S)
    if has_cell(R.db, ex, "MOB"):
        R.note("reentry.add-extraction.skipped", "the anchor already carries the MOB cell: a repeat is refused as a byte-identical copy, which proves nothing", {"lens": "MOB", "parameter_id": ex[1]})
    else:
        add_ext(R, "reentry.add-extraction", ex, "MOB")
    R.step("reentry.assess-1", "determine", [PY, "-I", "scripts/assess/assess_cell.py", "--db", str(R.db), "--emit-sql", str(R.scratch / "a1.sql"), "--parameter-id", str(ex[1]), "--slug", SLUG,
           "--identity", "MOB", "--session", S, "--stamp", "2026-11-12 00:00:00"])
    spec = rows(R.db, "select max(specification_id) from specifications")[0][0]
    c = ctx(R.db)
    for v in ("raise-determination-gate", "resolve-determination-gate", "raise-follow-up", "resolve-follow-up"):
        args, _ = build_args(v, ctx(R.db), S)
        if v == "raise-determination-gate":
            args += ["--trigger-ref-id", REF]  # the pointer: tier and evidence type are read from the held source
        R.dbpy(f"reentry.{v}", f"{v} on the live determination's data", v, *args)
    R.dbpy("reentry.retire-specification", "retire the determination in place", "retire-specification", "--specification-id", str(spec), "--reason", "STRESS-FIXTURE re-entry", "--session", S)
    R.step("reentry.assess-2-same-cell", "re-determine the same cell after retirement: allowed, and does the new row point back at the retired one?", [PY, "-I", "scripts/assess/assess_cell.py", "--db", str(R.db),
           "--emit-sql", str(R.scratch / "a2.sql"), "--parameter-id", str(ex[1]), "--slug", SLUG, "--identity", "MOB", "--session", S, "--stamp", "2026-11-12 00:00:01"])
    R.sql("reentry.supersession-pointer", "retired -> superseding pointer", "select specification_id,state,retired_at,superseded_by_specification_id from specifications where parameter_id=? and identity_code='MOB'", (ex[1],))
    R.sql("reentry.gaps-after", "gaps raised by the engine and the follow-up", "select gap_id,category,priority,status,substr(description,1,100) from gaps order by gap_id desc limit 5")
    finish_(R)


def part_batteries(out):
    R = Run("batteries", out)
    for b in ("syntax", "structure", "data", "db_integrity", "tests", "schema", "governance", "attestation", "research", "render"):
        R.step(f"battery.{b}", f"battery {b} run as the runner requires (--all)", [PY, "-I", "scripts/run_checks.py", "--battery", b, "--all"], timeout=1500)
    finish_(R)


def part_probes(out):
    R = Run("probes", out)
    pairs = {  # strings that differ ONLY by a vowel sign / tone mark / voicing mark / point / diacritic / decimal point / digit script
        "deva-i": "कि", "deva-ii": "की", "deva-e": "के", "deva-ai": "कै",
        "thai-mai-ek": "ไม่", "thai-mai-tho": "ไม้", "thai-plain": "ไม",
        "heb-pointed": "שָׁלוֹם", "heb-plain": "שלום",
        "ara-vowelled-1": "كَتَبَ", "ara-vowelled-2": "كُتُبٌ", "ara-plain": "كتب",
        "kana-ka": "か", "kana-ga": "が", "kana-ha": "は", "kana-pa": "ぱ",
        "hangul-ga": "가", "hangul-gag": "각",
        "dec-0.6": "0.6 s", "dec-6.0": "6.0 s", "dec-comma": "0,6 s", "dec-fullwidth": "０．６ ｓ", "dec-arabic-indic": "٠٫٦ ث", "dec-devanagari": "०.६ से",
        "indian-grouping": "₹1,50,000", "swiss-grouping": "12 500 CHF", "german-grouping": "1.234,56 €",
    }
    R.step("probes.script-pairs", "normalise_quote and name screens on mark-only / decimal-only / digit-script pairs: collisions are defects", [PY, "-I", str(HERE / "lang_probe.py"), json.dumps(pairs, ensure_ascii=False)])
    finish_(R)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)  # no default: Run() empties each log.jsonl it opens, and RETAINED.md keeps those logs
    ap.add_argument("--parts", default="probes,real,guards,batches,lifecycle,reentry")  # batteries is callable by name; it runs run_checks.py --all
    a = ap.parse_args()
    s0 = sha(CANON)
    fns = {"real": part_real, "guards": part_guards, "batches": part_batches, "lifecycle": part_lifecycle, "reentry": part_reentry, "batteries": part_batteries, "probes": part_probes}
    for p in a.parts.split(","):
        try:
            fns[p](a.out)
        except Exception:
            import traceback
            print("PART FAILED", p, traceback.format_exc())
    print("canonical sha256 before/after:", s0, sha(CANON), "UNCHANGED" if s0 == sha(CANON) else "!!! MOVED !!!")


if __name__ == "__main__":
    main()
