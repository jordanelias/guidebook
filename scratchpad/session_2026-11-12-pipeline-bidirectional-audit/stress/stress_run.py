#!/usr/bin/env python3
"""Deterministic stress script: run the pipeline base -> render, then backward, cold-entry, lateral
and adversarial, for three unrelated topics, on SCRATCH copies, logging every command.

    python3 -I stress_run.py [--topics acoustics,reach,thermal] [--out DIR]

Nothing here judges. Every step records an EXPECTATION (written before the run), the command, rc,
full stdout/stderr, and the row-count change on the scratch DB, to <out>/<topic>/log.jsonl. A later
audit (Fable) reads the logs. A step that raises inside this script is logged as SCRIPT-ERROR and the
run continues. The canonical DB is never written (sha256 recorded around every step); steps that write
into a source tree (emit_data_migration, migrate_db) run in a local clone.

Fixtures are marked STRESS-FIXTURE and live only in the scratch DBs.
"""
import argparse, hashlib, json, os, re, shutil, sqlite3, subprocess, sys, tempfile, time, traceback
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]  # the scripts live inside the checkout they test; their location is the fact
CANON = REPO / "data/guidebook.db"
HERE = Path(__file__).resolve().parent
SCRATCH = Path(tempfile.gettempdir()) / "guidebook-stress"
PY = sys.executable

TOPICS = {
    "acoustics": dict(
        slug="deaf-classroom-reverberation-time", param_term_like="reverberation%", lenses_identity=["DEAF", "ALL", "MOB", "BLIND"],
        lang="de", jur="DE", strings={
            "de": "Die Nachhallzeit in Unterrichtsräumen soll höchstens 0,6 s betragen.",
            "fi": "Luokkahuoneen jälkikaiunta-ajan tulee olla enintään 0,6 sekuntia.",
            "ja-kana": "教室の残響時間は0.6秒以下とする。",
            "ja-kana-b": "教室の残響時間は0.8秒以下とする。",
            "ar": "يجب ألا يتجاوز زمن الصدى في الفصل 0.6 ثانية.",
            "hi": "कक्षा में प्रतिध्वनि समय 0.6 सेकंड से अधिक नहीं होना चाहिए।",
            "hi-b": "कक्षा में प्रतिध्वनि समय 0.8 सेकंड से अधिक नहीं होना चाहिए।",
            "th": "เวลาก้องในห้องเรียนต้องไม่เกิน 0.6 วินาที",
            "he": "זמן הדהוד בכיתה לא יעלה על 0.6 שניות",
            "fullwidth-digits": "残響時間 ０．６ ｓ",
        }),
    "reach": dict(
        slug="reach-range-and-accessible-controls", param_term_like="Reach%", lenses_identity=["MOB", "LMB", "TALL", "ALL"],
        lang="ko", jur="KR", strings={
            "ko": "조작부의 높이는 바닥에서 1,200 mm 이하로 한다.",
            "ko-b": "조작부의 높이는 바닥에서 1,100 mm 이하로 한다.",
            "zh": "操作装置的高度不应超过地面以上1200毫米。",
            "ja": "操作部の高さは床から1.2m以下とする。",
            "ar": "ارتفاع عناصر التحكم لا يزيد عن 120 سم.",
            "en-imperial": "Controls shall be mounted no higher than 48 in (1220 mm) above the floor.",
            "en-mixed-units": "Reach 1.2 m / 120 cm / 1200 mm / 47.2 in",
            "number-in-words": "kuusikymmentä senttiä lattiasta",
            "hi": "नियंत्रण की ऊँचाई फर्श से 120 सेमी से अधिक नहीं होनी चाहिए।",
            "hi-b": "नियंत्रण की ऊँचाई फर्श से 110 सेमी से अधिक नहीं होनी चाहिए।",
        }),
    "thermal": dict(
        slug="thermal-comfort-older-adults-care-settings", param_term_like="thermal comfort", lenses_identity=["MS", "ALL", "DEM", "MOB"],
        lang="nl", jur="NL", strings={
            "nl": "De binnentemperatuur in zorgruimtes dient tussen 22 en 26 °C te liggen.",
            "de": "Die Raumtemperatur soll zwischen 20 °C und 24 °C liegen.",
            "ja": "室温は22〜26℃を保つこと。",
            "ru": "Температура в помещении должна быть от 22 до 26 °C.",
            "th": "อุณหภูมิห้องควรอยู่ระหว่าง 22 ถึง 26 องศาเซลเซียส",
            "he": "הטמפרטורה בחדר תהיה בין 22 ל-26 מעלות",
            "en-F": "Maintain 72-79 °F (22-26 °C).",
            "hi": "कमरे का तापमान 22 से 26 डिग्री सेल्सियस के बीच रहना चाहिए।",
            "hi-b": "कमरे का तापमान 20 से 24 डिग्री सेल्सियस के बीच रहना चाहिए।",
        }),
    "luminance": dict(
        slug="luminance-contrast-lrv-evidence-base", param_term_like="LRV%", lenses_identity=["BLIND", "VES", "ALL", "AUT"], lang="ja", jur="JP", strings={
            "ja": "床と壁の輝度比（LRV）の差は30ポイント以上とする。",
            "ja-b": "床と壁の輝度比（LRV）の差は20ポイント以上とする。",
            "de": "Der Leuchtdichtekontrast soll mindestens 0,4 betragen.",
            "en": "A difference of at least 30 LRV points between adjacent surfaces.",
            "ko": "인접 표면의 LRV 차이는 30점 이상이어야 한다.",
            "ar": "يجب ألا يقل فرق معامل الانعكاس عن 30 نقطة.",
            "hi": "आसन्न सतहों के बीच LRV का अंतर कम से कम 30 अंक होना चाहिए।",
            "hi-b": "आसन्न सतहों के बीच LRV का अंतर कम से कम 20 अंक होना चाहिए।",
            "th": "ค่าความแตกต่าง LRV ต้องไม่น้อยกว่า 30 จุด",
        }),
    "circadian": dict(
        slug="circadian-lighting-melanopic-edi", param_term_like="colour temperature", lenses_identity=["DEM", "ALL", "AUT", "BLIND"], lang="sv", jur="SE", strings={
            "sv": "Korrelerad färgtemperatur bör vara mellan 2700 och 4000 K.",
            "de": "Die Farbtemperatur soll 3000 K nicht überschreiten.",
            "ja": "色温度は3000K以下とする。",
            "zh": "色温不应超过3000开尔文。",
            "ru": "Цветовая температура не должна превышать 3000 К.",
            "ar": "ينبغي ألا تتجاوز درجة حرارة اللون 3000 كلفن.",
            "hi": "रंग तापमान 3000 K से अधिक नहीं होना चाहिए।",
            "hi-b": "रंग तापमान 4000 K से अधिक नहीं होना चाहिए।",
        }),
    "flash": dict(
        slug="flash-threshold-photosensitive-safety", param_term_like="flash%", lenses_identity=["EPI", "ALL", "AUT", "MS"], lang="en", jur="UK", strings={
            "en": "No more than three flashes in any one-second period.",
            "fr": "Pas plus de trois éclats par période d'une seconde.",
            "de": "Nicht mehr als drei Blitze pro Sekunde.",
            "ja": "1秒間に3回を超える点滅をしてはならない。",
            "ja-b": "1秒間に4回を超える点滅をしてはならない。",
            "ar": "لا أكثر من ثلاث ومضات في الثانية الواحدة.",
            "hi": "प्रति सेकंड तीन से अधिक झिलमिलाहट नहीं होनी चाहिए।",
            "hi-b": "प्रति सेकंड चार से अधिक झिलमिलाहट नहीं होनी चाहिए।",
            "th": "ไม่เกินสามครั้งต่อวินาที",
        }),
    "grabbar": dict(
        slug="fold-down-grab-bar-specification", param_term_like="grab%", lenses_identity=["MOB", "LMB", "SCI", "ALL"], lang="fr", jur="CA", strings={
            "en": "Grab bars shall resist a load of 1.33 kN (300 lbf).",
            "fr": "La barre d'appui doit résister à une charge de 1,33 kN.",
            "de": "Haltegriffe: Durchmesser 30 bis 40 mm.",
            "ja": "手すりの直径は32mm以上36mm以下とする。",
            "ja-b": "手すりの直径は28mm以上32mm以下とする。",
            "zh": "扶手直径应为30至40毫米。",
            "ko": "손잡이의 지름은 30mm 이상 40mm 이하로 한다.",
            "hi": "ग्रैब बार का व्यास 30 से 40 मिमी होना चाहिए।",
            "hi-b": "ग्रैब बार का व्यास 20 से 30 मिमी होना चाहिए।",
        }),
    "cost": dict(
        slug="construction-cost-data", param_term_like="cost%", lenses_identity=["ALL", "MOB"], lang="en", jur="CA", strings={
            "en-CAD": "Retrofit cost of CAD 12,500 per door opening.",
            "ja-yen": "改修費は1戸あたり120万円とする。",
            "de-eur": "Kosten von 4.200 € je Rampe (1.234,56 € Nebenkosten).",
            "ar-sar": "تكلفة 5000 ريال لكل مدخل.",
            "hi-inr": "लागत ₹1,50,000 प्रति इकाई।",
            "hi-inr-b": "लागत ₹1,20,000 प्रति इकाई।",
            "fr-ch": "Coût de 12 500 CHF par rampe.",
            "number-in-words": "twelve thousand five hundred dollars",
        }),
    "method": dict(
        slug="jurisdiction-matrix-accessibility-standards", param_term_like="jurisdiction%", lenses_identity=["ALL"], lang="fr", jur="CA", strings={
            "fr-QC": "Code de construction du Québec, chapitre I, section 3.8.",
            "en-ON": "Ontario Building Code, O. Reg. 332/12, Section 3.8.",
            "de-NRW": "Landesbauordnung Nordrhein-Westfalen, § 49.",
            "es": "Código Técnico de la Edificación, DB-SUA, Anejo A.",
            "ja": "建築基準法施行令第126条の2。",
            "it": "D.M. 236/1989, art. 4.1.",
            "ar": "الكود السعودي للبناء، الفصل 2.",
            "hi": "राष्ट्रीय भवन संहिता, भाग 3।",
        }),
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def ro(db):
    return sqlite3.connect(f"file:{db}?mode=ro", uri=True)


def counts(db):
    c = ro(db)
    try:
        return {t: c.execute(f'select count(*) from "{t}"').fetchone()[0]
                for (t,) in c.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")}
    finally:
        c.close()


def rows(db, q, a=()):
    c = ro(db)
    try:
        return c.execute(q, a).fetchall()
    finally:
        c.close()


class Run:
    def __init__(self, topic, out):
        self.topic, self.out = topic, Path(out) / topic
        self.out.mkdir(parents=True, exist_ok=True)
        self.log = self.out / "log.jsonl"
        self.log.write_text("")
        self.scratch = SCRATCH / topic
        self.scratch.mkdir(parents=True, exist_ok=True)
        self.db = self.scratch / "topic.db"
        shutil.copyfile(CANON, self.db)
        self.sess = f"session_2026-11-12-stress-{topic}"
        self.n = 0
        self.index = []

    # one logged step -------------------------------------------------------------------------
    def step(self, tag, expect, argv, db=None, cwd=REPO, timeout=300, stdin=None):
        db = Path(db or self.db)
        assert db.resolve() != CANON.resolve()
        self.n += 1
        tag = f"{self.topic}.{self.n:03d}.{tag}"
        s0, b = sha(CANON), counts(db)
        env = dict(os.environ, GUIDEBOOK_DB_PATH=str(db))
        t0 = time.time()
        try:
            p = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout, input=stdin)
            rc, so, se = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as e:
            rc, so, se = "TIMEOUT", "", "timeout"
        except Exception as e:  # noqa
            rc, so, se = "SCRIPT-ERROR", "", traceback.format_exc()
        dt = round(time.time() - t0, 2)
        try:
            a = counts(db)
        except Exception as e:  # noqa
            a = {"__unreadable__": str(e)}
        ch = {t: [b.get(t), a.get(t)] for t in set(b) | set(a) if b.get(t) != a.get(t)}
        s1 = sha(CANON)
        rec = dict(tag=tag, expect=expect, argv=argv, cwd=str(cwd), db=str(db), rc=rc, seconds=dt, stdout=so, stderr=se,
                   changed=ch, canonical_moved=(s0 != s1), canonical_sha256=s1, at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        with open(self.log, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        first = (so.strip().splitlines() or [""])[0][:140] if so else (se.strip().splitlines() or [""])[-1][:140]
        self.index.append((tag, rc, dt, len(ch), expect, first))
        print(f"{tag} rc={rc} {dt}s changed={len(ch)}", flush=True)
        return rc, so, se

    def note(self, tag, expect, result):
        """Log a read-only fact taken directly from the DB (no subprocess)."""
        self.n += 1
        tag = f"{self.topic}.{self.n:03d}.{tag}"
        rec = dict(tag=tag, expect=expect, argv=["<direct read-only query>"], rc=0, stdout=json.dumps(result, ensure_ascii=False, default=str),
                   stderr="", changed={}, at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        with open(self.log, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        self.index.append((tag, 0, 0, 0, expect, json.dumps(result, ensure_ascii=False, default=str)[:140]))
        return result

    def dbpy(self, tag, expect, *args, **kw):
        return self.step(tag, expect, [PY, "-I", "scripts/db.py", *args], **kw)

    def sql(self, tag, expect, q, a=()):
        try:
            r = rows(self.db, q, a)
            return self.note(tag, expect, {"sql": q, "params": list(a), "rows": r[:200], "nrows": len(r)})
        except Exception as e:  # noqa
            return self.note(tag, expect, {"sql": q, "error": repr(e)})


def pass1_forward(R, T):
    slug = T["slug"]
    S = R.sess
    # ---------------- BASE
    R.sql("base.slug", "slug row exists", "select * from slugs where slug=?", (slug,))
    R.sql("base.params-for-topic", "topic parameters (by term name) listed with extraction counts",
          "select p.parameter_id,t.term_id,t.canonical_en,(select count(*) from source_value_extractions e where e.parameter_id=p.parameter_id) from base_parameters p join terms t using(term_id) where t.canonical_en like ?", (T["param_term_like"],))
    R.sql("base.terms-for-topic", "terms matching topic exist, with parameter status",
          "select t.term_id,t.canonical_en,(select count(*) from base_parameters p where p.term_id=t.term_id) is_param from terms t where t.canonical_en like ?", (T["param_term_like"],))
    R.sql("base.alias-language-census", "aliases by language across the whole vocabulary (non-English share)",
          "select language,count(*) from term_aliases group by 1 order by 2 desc")
    R.sql("base.lang-jur", "language-jurisdiction rows for the topic's language", "select * from lang_jur_map where language=? limit 20", (T["lang"],))
    R.sql("base.scope-status", "scope_status populated?", "select scope_status,count(*) from lang_jur_map group by 1")
    R.dbpy("base.coverage", "coverage report for the topic slug", "coverage", "--slug", slug)
    # dynamic parameter definition: real term if it exists unparameterised
    tid = rows(R.db, "select t.term_id from terms t where t.canonical_en like ? and not exists (select 1 from base_parameters p where p.term_id=t.term_id) limit 1", (T["param_term_like"],))
    if tid:
        R.dbpy("base.add-parameter-existing-term", "promote an existing term to a parameter (dynamic parameter definition)",
               "add-parameter", "--term-id", tid[0][0], "--notes", "STRESS-FIXTURE: dynamic parameter definition", "--session", S)
    else:
        R.note("base.add-parameter-existing-term", "n/a: topic term already a parameter or absent", {"skipped": "no unparameterised matching term"})
    # fixture observation -> new term -> new parameter (the observe/adjudicate/add-term/add-parameter chain)
    cand = rows(R.db, "select e.ref_id,e.claim_text from source_value_extractions e where length(e.claim_text)>60 order by e.extraction_id limit 8")
    obs_id = None
    obs_surface = None
    for ref, claim in cand:
        words = re.findall(r"[A-Za-z]{4,}", claim)
        if len(words) < 3:
            continue
        surface = " ".join(words[:2])
        if surface not in claim:
            continue
        before = rows(R.db, "select coalesce(max(observation_id),0) from observed_terms")[0][0]
        rc, so, se = R.dbpy("base.observe-term", "observe a phrase verbatim from a held source (expect: refused unless the quote is found in a saved file for that source)",
                            "observe-term", "--ref-id", ref, "--surface-form", surface, "--language", "en", "--locator", "STRESS-FIXTURE locator",
                            "--context-quote", claim[:200], "--notes", "STRESS-FIXTURE", "--session", S)
        after = rows(R.db, "select coalesce(max(observation_id),0) from observed_terms")[0][0]
        if after > before:
            obs_id = after
            obs_surface = surface
            break
    if obs_id:
        R.dbpy("base.adjudicate-names-new", "NAMES-NEW via adjudicate-term is refused by design", "adjudicate-term", "--observation-id", str(obs_id),
               "--outcome", "NAMES-NEW", "--rationale", "STRESS-FIXTURE", "--session", S)
        R.dbpy("base.add-term-value-bearing", "a value-bearing canonical name is refused", "add-term", "--from-observation", str(obs_id),
               "--canonical-en", "STRESS-FIXTURE concept not above 0.6 s", "--rationale", "STRESS-FIXTURE value-bearing test", "--session", S)
        nterms = rows(R.db, "select count(*) from terms")[0][0]
        R.dbpy("base.add-term-new", "mint a new term from the observation (name must lie inside the observed phrase)", "add-term", "--from-observation", str(obs_id),
               "--canonical-en", obs_surface, "--rationale", "STRESS-FIXTURE: dynamic term definition from the observed phrase", "--session", S)
        if rows(R.db, "select count(*) from terms")[0][0] > nterms:
            newt = rows(R.db, "select term_id from terms order by rowid desc limit 1")
            R.dbpy("base.add-parameter-new-term", "promote the new term to a parameter", "add-parameter", "--term-id", newt[0][0], "--session", S)
        else:
            R.note("base.add-parameter-new-term", "n/a: add-term created no term", {"skipped": "add-term refused or wrote nothing"})
    else:
        R.note("base.observe-chain", "observation chain not completed", {"skipped": "no observation was accepted by observe-term across candidates tried"})
    # read-once: what the system says about already-read sources once the parameter list grew
    R.step("judgment.scan-debt-after-new-parameter", "scan debt now includes the new parameter(s) for every already-read source", [PY, "-I", "scripts/audit/scan_debt.py", "--limit", "5"])
    R.sql("judgment.scan-ledger-by-status", "v_scan_ledger status distribution after the parameter list grew",
          "select status,count(*) from v_scan_ledger group by 1")
    R.sql("judgment.scan-ledger-columns", "ledger columns", "select name from pragma_table_info('v_scan_ledger')")
    # ---------------- RESEARCH
    R.dbpy("research.log-search-fixture", "log a non-English search with a prior expectation", "log-search", "--slug", slug, "--language", T["lang"],
           "--query-text", "STRESS-FIXTURE: " + list(T["strings"].values())[0][:60], "--engine", "stress-script", "--depth-method", "scoping",
           "--prior-expectation", "STRESS-FIXTURE expects zero results", "--results-found", "0", "--results-screened", "0", "--results-admitted", "0",
           "--absence-class", "query_shape_failure", "--jurisdiction", T["jur"], "--session", S)
    ex = rows(R.db, "select max(exec_id) from search_executions")[0][0]
    R.dbpy("research.add-candidate-fixture", "stage a candidate", "add-candidate", "--exec-id", str(ex), "--found-under-slug", slug, "--disposition", "PENDING-VERIFICATION",
           "--title", "STRESS-FIXTURE candidate", "--surfaced-in", "STRESS-FIXTURE", "--surfaced-quote", "STRESS-FIXTURE quote", "--session", S)
    R.dbpy("research.log-search-wrong-session-form", "a '.md' session id scopes a gate to nothing; expect refusal or a silent accept", "log-search", "--slug", slug, "--language", "en",
           "--query-text", "STRESS-FIXTURE wrong session form", "--engine", "stress-script", "--depth-method", "scoping", "--prior-expectation", "STRESS-FIXTURE expects zero results", "--session", S + ".md")
    R.dbpy("research.unmined-gaps", "gap-driven mining entry point lists gaps", "unmined-gaps")
    # ---------------- EVIDENCE
    doi = rows(R.db, "select doi from evidence_sources where doi is not null and doi<>'' limit 1")
    if doi:
        R.dbpy("evidence.add-source-duplicate-doi", "R9: a duplicate DOI cross-files or is refused", "add-source", "--doi", doi[0][0], "--year", "2020",
               "--title", "STRESS-FIXTURE duplicate doi", "--authors", "Fixture A", "--source-type", "report", "--evidence-type", "grey", "--session", S)
    R.dbpy("evidence.add-source-fixture", "add a minimal fixture source (expect: refused for lacking retrieval/verification fields, or written UNVERIFIED)", "add-source",
           "--year", "2020", "--title", "STRESS-FIXTURE source", "--authors", "Fixture A", "--source-type", "report", "--slug", slug,
           "--verification-status", "UNVERIFIED", "--evidence-type", "grey", "--lang-detected", T["lang"], "--jurisdiction", T["jur"], "--session", S)
    # ---------------- JUDGMENT
    anyref = rows(R.db, "select ref_id from source_value_extractions order by extraction_id limit 1")[0][0]
    pid = (rows(R.db, "select parameter_id from base_parameters order by parameter_id desc limit 1") or [[3]])[0][0]
    R.dbpy("judgment.add-extraction-unfound-quote", "an extraction whose quote is in no saved file is refused", "add-extraction", "--ref-id", anyref, "--parameter-id", str(pid),
           "--claim-type", "numerical", "--claimed-value", "0.6", "--claimed-unit", "s", "--claim-text", "STRESS-FIXTURE sentence found in no file",
           "--extraction-method", "full-read", "--identity", "ALL", "--figure-role", "claim", "--relation", "none", "--session", S)
    R.dbpy("judgment.record-scan-bogus-sha", "a scan without a held file hash is refused", "record-scan", "--ref-id", anyref, "--mode", "catalogue", "--text-scope", "full",
           "--file-sha256", "0" * 64, "--method", "full-read", "--session", S)
    # ---------------- SYNTHESIS
    pids = [r[0] for r in rows(R.db, "select parameter_id from base_parameters order by parameter_id desc limit 2")]
    if len(pids) == 2:
        R.dbpy("synthesis.add-connection-fixture", "typed cross-parameter link between two parameters", "add-connection", "--confidence", "MODERATE",
               "--connection-type", "CROSS-PARAMETER", "--filed-in", slug, "--description", "STRESS-FIXTURE adjacency", "--source-skill", "stress-script",
               "--parameter", str(pids[0]), "--parameter", str(pids[1]), "--session", S)
    R.dbpy("synthesis.add-gap-reentry-fixture", "re-entry: a judgment-stage finding becomes a research gap", "add-gap", "--category", "CD", "--priority", "P3",
           "--description", "STRESS-FIXTURE re-entry from judgment: source insufficient", "--session", S)
    R.sql("synthesis.gaps-columns", "does a gap carry parameter/lens/jurisdiction/language?", "select name from pragma_table_info('gaps')")
    R.sql("synthesis.synthesis-table-counts", "synthesis tables' row counts",
          "select 'connections',count(*) from connections union all select 'connection_targets',count(*) from connection_targets union all select 'conflicts',count(*) from conflicts union all select 'convergence_assessment',count(*) from convergence_assessment")
    # ---------------- SPECIFICATION (each run on a FRESH copy: the engine writes its --db and refuses reruns)
    params = rows(R.db, "select p.parameter_id,t.canonical_en from base_parameters p join terms t using(term_id) where t.canonical_en like ? or t.canonical_en like 'STRESS-FIXTURE%' or p.parameter_id in (select max(parameter_id) from base_parameters) order by 1", (T["param_term_like"],))
    if not params:
        params = [(7, "reverberation time")]
    icf = rows(R.db, "select icf_code from base_icf where icf_code like 'd4%' order by 1 limit 1") or rows(R.db, "select icf_code from base_icf limit 1")
    need = rows(R.db, "select need_code from access_needs order by 1 limit 1")
    lenses = [("identity", c) for c in T["lenses_identity"]] + [("icf", icf[0][0])] + [("needs", need[0][0])]
    (R.out / "determinations").mkdir(exist_ok=True)
    for pid_, pname in params[:3]:
        for kind, code in lenses:
            fresh = R.scratch / f"assess-{pid_}-{kind}-{code}.db"
            shutil.copyfile(R.db, fresh)
            rj = R.out / "determinations" / f"p{pid_}-{kind}-{code}.json"
            R.step(f"specification.assess.p{pid_}.{kind}.{code}", f"engine determines parameter {pid_} ({pname}) under {kind}={code}; compare across lenses",
                   [PY, "-I", "scripts/assess/assess_cell.py", "--db", str(fresh), "--emit-sql", str(R.scratch / f"assess-{pid_}-{kind}-{code}.sql"),
                    "--parameter-id", str(pid_), "--slug", slug, f"--{kind}", code, "--session", S, "--stamp", "2026-11-12 00:00:00", "--report-json", str(rj)], db=fresh)
    # ---------------- RENDER
    R.sql("render.views-with-rows", "determination views' row counts after the run",
          "select 'v_best_practice',count(*) from v_best_practice union all select 'v_determination_provenance',count(*) from v_determination_provenance")
    wk = list(REPO.glob("workplan/pipeline-state-graph/walkability.py"))
    if wk:
        R.step("render.walkability", "stage-pair walk: which pairs reach render", [PY, "-I", str(wk[0])])
    R.step("render.owner-browser-build", "the only HTML generator: build to scratch", [PY, "-I", "scripts/generate/owner_browser_build.py", "--out", str(R.scratch / "owner_browser.html"), "--db", str(R.db)])
    R.step("render.ls-render-surfaces", "what render surfaces exist on disk", ["bash", "-c", "ls -d site specs parts 2>&1; ls scripts/generate; find parts -maxdepth 2 -type f | head -20"])


def pass2_backward(R, T):
    R.sql("backward.extraction-funnel", "extraction -> source -> locator -> search_candidate -> search_execution reach, all parameters",
          """select p.parameter_id,
                  count(distinct e.extraction_id) ext,
                  count(distinct s.ref_id) src,
                  count(distinct l.ref_id) with_locator,
                  count(distinct sc.candidate_id) with_candidate,
                  count(distinct se.exec_id) with_exec
             from base_parameters p
             left join source_value_extractions e on e.parameter_id=p.parameter_id
             left join evidence_sources s on s.ref_id=e.ref_id
             left join source_locators l on l.ref_id=s.ref_id
             left join search_candidates sc on sc.resolved_ref_id=s.ref_id
             left join search_executions se on se.exec_id=sc.exec_id
            group by 1""")
    R.sql("backward.spec-to-source-walk", "retired specifications -> links -> extractions -> sources",
          """select sp.specification_id, sp.state, sp.retired_at is not null retired,
                  (select count(*) from specification_source_links l where l.specification_id=sp.specification_id) src_links,
                  (select count(*) from specification_extraction_links l where l.specification_id=sp.specification_id) ext_links
             from specifications sp""")
    R.sql("backward.render-question-table", "is there any table that can hold a render/reader question?",
          "select name from sqlite_master where type='table' and (name like '%question%' or name like '%render%' or name like '%reader%')")
    R.sql("backward.retrieval-log-manifests-on-disk", "do source_locators carry a sha256 that exists as a payload", "select count(*), sum(sha256 is not null) from source_locators") \
        if rows(R.db, "select 1 from pragma_table_info('source_locators') where name='sha256'") else R.note("backward.locator-sha", "no sha256 column on source_locators", {})


def pass3_cold(R, T):
    probes = [
        ("base", "add-term-without-observation", ["add-term", "--canonical-en", "STRESS cold", "--rationale", "x", "--session", R.sess]),
        ("research", "log-search-without-slug", ["log-search", "--language", "en", "--query-text", "x", "--engine", "x", "--depth-method", "scoping", "--prior-expectation", "STRESS-FIXTURE", "--session", R.sess]),
        ("evidence", "add-source-minimal", ["add-source", "--year", "2020", "--title", "STRESS cold", "--authors", "Fixture A", "--evidence-type", "grey", "--session", R.sess]),
        ("judgment", "add-extraction-absent-ref", ["add-extraction", "--ref-id", "REF-99999", "--parameter-id", "7", "--claim-type", "numerical", "--claim-text", "x", "--extraction-method", "skim", "--figure-role", "claim", "--relation", "none", "--session", R.sess]),
        ("synthesis", "add-connection-absent-parameter", ["add-connection", "--confidence", "HIGH", "--connection-type", "CROSS-PARAMETER", "--filed-in", T["slug"], "--description", "x", "--source-skill", "stress", "--parameter", "9999", "--session", R.sess]),
    ]
    for stage, tag, args in probes:
        R.dbpy(f"cold.{stage}.{tag}", f"cold entry at {stage} with no upstream work: refuse with a reason, or write", *args)
    fresh = R.scratch / "cold-assess.db"
    shutil.copyfile(CANON, fresh)
    R.step("cold.specification.assess-cell-zero-evidence", "determine a parameter with zero extractions: expect pending/gap, not a value",
           [PY, "-I", "scripts/assess/assess_cell.py", "--db", str(fresh), "--emit-sql", str(R.scratch / "cold.sql"), "--parameter-id", "7", "--slug", T["slug"],
            "--identity", "ALL", "--session", R.sess, "--stamp", "2026-11-12 00:00:00", "--report-json", str(R.out / "determinations" / "cold-p7-ALL.json")], db=fresh)
    R.sql("cold.render.best-practice-for-parameter-without-spec", "render view for a parameter with no determination", "select count(*) from v_best_practice where parameter_id=7")


def pass4_lateral(R, T):
    probe = HERE / "lang_probe.py"
    R.step("lateral.script-probe", "per-script quote normalisation and name screens: do distinct strings collide? are marks lost?",
           [PY, "-I", str(probe), json.dumps(T["strings"], ensure_ascii=False)])
    R.sql("lateral.jurisdictions-in-db-vs-lang-jur", "jurisdictions named by lang_jur_map but absent from evidence_sources vocabulary",
          "select distinct jurisdiction from lang_jur_map except select distinct jurisdiction from evidence_sources")
    R.sql("lateral.evidence-by-language", "held sources by detected language", "select lang_detected,count(*) from evidence_sources group by 1 order by 2 desc")


def pass4b_vocab(R, T):
    base = ["--year", "2020", "--title", "STRESS-FIXTURE jurisdiction probe", "--authors", "Fixture A", "--source-type", "report", "--evidence-type", "grey", "--session", R.sess]
    for j in ("UK", "CA-ON", "DE-NW", "XX"):
        R.dbpy(f"lateral.add-source-jurisdiction-{j}", f"jurisdiction vocabulary behaviour for {j}: national accepted, sub-national and unknown refused or accepted?", "add-source", "--jurisdiction", j, *base)
    for lg in ("zh-Hant", "zh", "ZZ", "ar"):
        R.dbpy(f"lateral.log-search-language-{lg}", f"language-code vocabulary behaviour for {lg}", "log-search", "--slug", T["slug"], "--language", lg, "--query-text", "STRESS-FIXTURE language probe",
               "--engine", "stress-script", "--depth-method", "scoping", "--prior-expectation", "STRESS-FIXTURE", "--session", R.sess)


def pass6_determinism(R, T):
    outs = []
    for k in ("a", "b"):
        fresh = R.scratch / f"det-{k}.db"
        shutil.copyfile(CANON, fresh)
        sqlp, rj = R.scratch / f"det-{k}.sql", R.scratch / f"det-{k}.json"
        R.step(f"determinism.assess-{k}", "the same cell on two fresh copies is byte-identical (engine docstring promises it)",
               [PY, "-I", "scripts/assess/assess_cell.py", "--db", str(fresh), "--emit-sql", str(sqlp), "--parameter-id", "3", "--slug", "accessible-circulation-geometry", "--identity", "ALL",
                "--session", R.sess, "--stamp", "2026-11-12 00:00:00", "--report-json", str(rj)], db=fresh)
        outs.append((sqlp, rj))
    same = [(outs[0][i].exists() and outs[1][i].exists() and outs[0][i].read_bytes() == outs[1][i].read_bytes()) for i in (0, 1)]
    R.note("determinism.compare", "emit-sql and report-json byte-identical across two fresh runs", {"sql_identical": same[0], "report_identical": same[1]})
    # idempotence: the same cell twice on ONE copy
    one = R.scratch / "det-once.db"
    shutil.copyfile(CANON, one)
    for k in (1, 2):
        R.step(f"determinism.assess-same-db-run{k}", "a re-run for the same cell on the same DB is refused by the row-identity index",
               [PY, "-I", "scripts/assess/assess_cell.py", "--db", str(one), "--emit-sql", str(R.scratch / f"det-once{k}.sql"), "--parameter-id", "3", "--slug", "accessible-circulation-geometry",
                "--identity", "ALL", "--session", R.sess, "--stamp", "2026-11-12 00:00:00"], db=one)


def pass5_adversarial(R, T):
    # a parameter that has extractions and no open gate, so the retire meets its own rule, not the gate's
    tgt = rows(R.db, "select p.parameter_id from base_parameters p where p.status='active' and exists (select 1 from source_value_extractions e where e.parameter_id=p.parameter_id) "
               "and not exists (select 1 from determination_gates g where g.parameter_id=p.parameter_id and g.resolved_at is null) order by p.parameter_id limit 1")
    if tgt:
        tgt = tgt[0][0]
        rc, _, _ = R.dbpy("adversarial.retire-parameter-with-extractions", "retire a parameter that has extractions and no open gate: expect refusal or cascade", "retire-parameter", "--parameter-id", str(tgt),
                          "--reason", "STRESS-FIXTURE", "--session", R.sess)
        st = rows(R.db, "select (select count(*) from source_value_extractions where parameter_id=?), (select status from base_parameters where parameter_id=?)", (tgt, tgt))[0]
        R.note("adversarial.post-retire-state", "the state agrees with the retire's outcome: rc 0 -> retired, refused -> active; extractions kept either way",
               {"parameter_id": tgt, "retire_rc": rc, "extractions": st[0], "status": st[1], "consistent": (rc == 0) == (st[1] == "retired")})
    else:
        R.note("adversarial.skip-retire", "an active parameter with extractions and no open gate exists", {})
    ref = rows(R.db, "select ref_id from source_value_extractions order by extraction_id limit 1")[0][0]
    par = rows(R.db, "select l.parameter_id from v_scan_ledger l join base_parameters p using(parameter_id) where l.ref_id=? and l.status='NOT-READ' and p.status='active' order by 1 limit 1", (ref,))
    R.dbpy("adversarial.number-in-words-claim", "an extraction whose number is written in words", "add-extraction", "--ref-id", ref, "--parameter-id", str(par[0][0] if par else 0), "--claim-type", "numerical",
           "--claimed-value", "sixty", "--claimed-unit", "cm", "--claim-text", T["strings"].get("number-in-words", "STRESS-FIXTURE"), "--extraction-method", "skim", "--identity", "ALL", "--figure-role", "claim", "--relation", "none", "--session", R.sess)


def writepath_replay(R, T):
    clone = R.scratch / "clone"
    shutil.rmtree(clone, ignore_errors=True)  # a reused clone keeps the previous run's migration
    R.step("writepath.clone", "local clone for write-path replay", ["git", "clone", "--quiet", str(REPO), str(clone)])
    canon_copy = R.scratch / "canonical-copy.db"
    shutil.copyfile(CANON, canon_copy)
    out_sql = R.scratch / "batch.sql"
    R.step("writepath.emit-batch-sql", "capture the scratch DB's delta as SQL", [PY, "-I", "scripts/research/emit_batch_sql.py", "--scratch", str(R.db), "--canonical", str(canon_copy), "--out", str(out_sql)])
    if out_sql.exists() and out_sql.stat().st_size:
        R.step("writepath.emit-data-migration", "turn the delta into a data migration file inside the CLONE", [PY, "-I", "scripts/emit_data_migration.py", "--session", R.sess + ".md",
               "--summary", "STRESS-FIXTURE replay", "--input", str(out_sql), "--output-dir", str(clone / "scripts/migrations")], cwd=clone, db=canon_copy)
        rebuilt = R.scratch / "rebuilt.db"
        shutil.copyfile(CANON, rebuilt)  # placeholder path must exist for the harness; migrate_db --rebuild writes its own target
        R.step("writepath.migrate-rebuild", "rebuild a DB from migration history in the clone", [PY, "-I", "scripts/migrate_db.py", "--rebuild", str(R.scratch / "rebuilt-out.db")], cwd=clone, db=rebuilt, timeout=600)
        if (R.scratch / "rebuilt-out.db").exists():
            a, b = counts(R.db), counts(R.scratch / "rebuilt-out.db")
            R.note("writepath.rebuilt-vs-scratch", "rebuilt DB equals the scratch DB table-for-table",
                   {t: [a.get(t), b.get(t)] for t in sorted(set(a) | set(b)) if a.get(t) != b.get(t)} or {"differences": 0})
    else:
        R.note("writepath.nothing-captured", "the forward pass wrote something that capture sees", {"batch_sql_bytes": out_sql.stat().st_size if out_sql.exists() else None})


def finish(R):
    with open(R.out / "scenarios.tsv", "w") as f:
        f.write("tag\trc\tseconds\ttables_changed\texpectation\tfirst_line\n")
        for r in R.index:
            f.write("\t".join(str(x).replace("\t", " ").replace("\n", " ") for x in r) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topics", default="acoustics,reach,thermal,luminance,circadian,flash,grabbar,cost,method")
    ap.add_argument("--out", required=True)  # no default: Run() empties each log.jsonl it opens, and RETAINED.md keeps those logs
    a = ap.parse_args()
    s0 = sha(CANON)
    for name in a.topics.split(","):
        R = Run(name, a.out)
        for fn in (pass1_forward, pass2_backward, pass3_cold, pass4_lateral, pass4b_vocab, pass5_adversarial, pass6_determinism, writepath_replay):
            try:
                fn(R, TOPICS[name])
            except Exception:  # a script bug is logged, not fatal
                R.note(f"SCRIPT-ERROR.{fn.__name__}", "script runs", {"traceback": traceback.format_exc()})
        finish(R)
    # cross-topic: two independently captured deltas applied to one history (id allocation collisions)
    try:
        names = a.topics.split(",")
        R = Run("crosstopic", a.out)
        clone = R.scratch / "clone"
        shutil.rmtree(clone, ignore_errors=True)  # a reused clone keeps the previous run's migration
        R.step("clone", "local clone", ["git", "clone", "--quiet", str(REPO), str(clone)])
        made = 0
        for nm in names[:3]:
            sqlp = SCRATCH / nm / "batch.sql"
            if sqlp.exists() and sqlp.stat().st_size:
                rc, so, se = R.step(f"emit-migration-from-{nm}", f"apply topic {nm}'s independent delta to the same history", [PY, "-I", "scripts/emit_data_migration.py", "--session", f"session_2026-11-12-stress-{nm}.md",
                       "--summary", f"STRESS-FIXTURE {nm}", "--input", str(sqlp), "--output-dir", str(clone / "scripts/migrations"), "--force-timestamp", f"2026111208000{made}"], cwd=clone)
                made += 1
        R.step("rebuild-with-all-deltas", "rebuild from history plus the independently captured deltas: collisions on ids / unique keys surface here",
               [PY, "-I", "scripts/migrate_db.py", "--rebuild", str(R.scratch / "rebuilt-all.db")], cwd=clone, timeout=900)
        finish(R)
    except Exception:
        print("crosstopic failed:", traceback.format_exc())
    print("canonical sha256 before/after:", s0, sha(CANON), "UNCHANGED" if s0 == sha(CANON) else "!!! MOVED !!!")


if __name__ == "__main__":
    main()
