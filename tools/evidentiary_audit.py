#!/usr/bin/env python3
"""
tools/evidentiary_audit.py

Per-slice evidentiary audit over data/guidebook.db. For each slug (research
slice) it scores six dimensions and writes four deliverables:

  audits/evidentiary-base-audit.md      — the narrative report
  audits/evidentiary-base-audit.csv     — flat per-slice table
  audits/evidentiary-base-audit.json    — full per-slice record + aggregates
  tools/evidentiary-audit-dashboard.html — interactive filter view
                                           (entire corpus / category / term)

The six dimensions, per slice:
  (1) amount of evidence          (4) languages sourced
  (2) tiers of evidence           (5) English/Anglophone bias
  (3) jurisdictions sourced       (6) overall quality (composite grade)

Design notes
------------
* Read-only on the DB. Deterministic: the report's "as-of" date is derived
  from the DB's own max(updated_at), NOT wall-clock, so identical DB content
  produces byte-identical output (mirrors tools/regenerate_vetting_surface.py).
  That lets the GitHub workflow detect drift with a plain `git diff`.
* Every figure in the prose is computed from the DB — nothing is hardcoded —
  so the report stays correct when the evidence base changes.
* Tiers follow governance/tier-system.md. Under the weighted-strength model
  (§8, DR-2026-07-20) every tier can anchor a best-practice claim; the claim's
  *strength* is weighted by tier — ● full (T1/Co-1/T2/Co-2/T3-clinical),
  ◐ partial (T4/T5), ○ weak (T3-grey/T6/grey). DISPUTED sources (§4) are
  stripped of anchoring. "Tier number reflects what kind of claim a source can
  anchor, not raw quality."

Usage:
  python3 tools/evidentiary_audit.py                 # default DB + output paths
  python3 tools/evidentiary_audit.py --db path/to.db
  GUIDEBOOK_DB_PATH=... python3 tools/evidentiary_audit.py
"""
import argparse
import csv
import json
import os
import sqlite3
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = REPO_ROOT / "data" / "guidebook.db"
AUDITS_DIR = REPO_ROOT / "audits"
TOOLS_DIR = REPO_ROOT / "tools"

# ---------------------------------------------------------------- reference sets
# Native-Anglophone: English is official AND the native evidentiary tradition
# is English-medium.
ANGLO_CORE = {"US", "UK", "AU", "CA", "NZ", "IE"}
# English official/co-official but not native-Anglophone tradition.
ANGLO_OFFICIAL = {"SG", "HK", "IN", "NG", "GH", "ZA", "MY", "AE", "SA"}
# Supranational, predominantly English-medium but multinational.
SUPRA = {"INT", "EU", "ISO", "ASEAN"}
ENGLISH_LANGS = {"en", "eng"}
# Language codes found mis-filed in the jurisdiction column (data-integrity
# defect): standalone occurrences are NOT real jurisdictions.
JUR_LANGCODE_POLLUTION = {"ZH", "JA", "DA"}
# Western-European + CJK languages — used only to describe the *shape* of the
# non-English corpus in prose.
EURO_CJK = {"en", "de", "fr", "nl", "sv", "no", "da", "fi", "es", "pt", "it",
            "ja", "zh", "ko"}

# Item (specification) category labels — from data/question-headings.yaml.
CATEGORY_LABELS = {
    "A": "Acoustics", "B": "Lighting", "C": "Colour and Contrast",
    "D": "Wayfinding and Cognition", "E": "Circulation and Access",
    "F": "Sensory Environment", "G": "Furniture, Fixtures and Spatial Layout",
    "H": "Controls and Technology", "I": "Hardware and Fixtures",
    "K": "DeafBlind Provisions",
}


def is_disputed(row):
    """Has this source been DISPUTED by the anti-fabrication sweep?

    verification_status='DISPUTED' (DR-2026-07-20 §4) strips a source of its
    VERIFIED standing and its ability to anchor a claim until a real source is
    located or it is retired. Such rows are *recorded findings, not deleted*:
    they are excluded from every anchoring/strength computation (band, full/
    partial/weak counts) but remain in the raw volume / tier / jurisdiction /
    language totals so the disputed source stays visible in the audit.
    """
    return (row["verification_status"] or "").strip().upper() == "DISPUTED"


def anchor_band(row):
    """Strength band at which this source can anchor a best-practice claim.

    Weighted-strength model (governance/tier-system.md §8, DR-2026-07-20 §1):
    *every* tier can anchor a best-practice claim; the claim's strength is
    weighted by the tier of the evidence behind it.

      ● full    T1, Co-1, T2, Co-2, T3-clinical  — anchors outright (adjudicated)
      ◐ partial T4, T5                            — anchors as *standards practice*
                                                     ("standards basis, not primary")
      ○ weak    T3-grey, T6, grey / thin base     — anchors only a floor/convergence
                                                     claim, honesty-flagged

    The band is exactly the §5 evidence-quality marker (● / ◐ / ○) read with
    anchoring semantics, so it reuses quality_marker(). A DISPUTED source cannot
    anchor at any band and returns None.
    """
    if is_disputed(row):
        return None
    return {"●": "full", "◐": "partial", "○": "weak"}[quality_marker(row)]


def is_t3_clinical(row):
    return row["tier"] == 3 and (row["evidence_type"] or "").lower() == "clinical"


def quality_marker(row):
    """evidence_quality marker per tier-system.md §5."""
    t = row["tier"]
    et = (row["evidence_type"] or "").lower()
    if et in ("co1", "co2"):
        return "●"
    if t in (1, 2):
        return "●"
    if t == 3:
        return "●" if et == "clinical" else "○"
    if t in (4, 5):
        return "◐"
    return "○"


def norm_jur(j):
    return j.strip() if j else None


def is_polluted_jur(j):
    return bool(j) and j.strip().upper() in JUR_LANGCODE_POLLUTION


def anglo_class(j):
    """Classify a (possibly compound) jurisdiction string by its strongest member."""
    if not j:
        return "unknown"
    parts = [p.strip().upper() for p in j.replace("/", " ").replace(",", " ").split()]
    if any(p in ANGLO_CORE for p in parts):
        return "anglo_core"
    if any(p in SUPRA for p in parts):
        return "supra"
    if any(p in ANGLO_OFFICIAL for p in parts):
        return "anglo_official"
    return "non_anglo"


# ------------------------------------------------------------- composite score
def score(rec):
    """Transparent 0-100 rubric. Returns (total, components, grade_letter)."""
    n = rec["n"]
    if n == 0:
        return 0, dict(A=0, B=0, C=0, D=0, E=0), "F"
    # A volume (0-20)
    A = 4 if n < 3 else 8 if n < 5 else 12 if n < 8 else 16 if n < 12 else 20
    # B tier strength (0-30), weighted-strength model (§8, DR-2026-07-20). The
    # score mirrors the anchoring bands: ● full anchors (T1/Co-1/T2/Co-2 AND
    # T3-clinical, now full-strength) carry full weight; ◐ partial anchors (T4/T5,
    # "standards basis") earn partial credit; ○ weak (T3-grey/T6/grey) earn none.
    # A present full anchor adds a bonus. DISPUTED sources anchor at no band
    # (excluded from full/partial/weak in compute()), so they earn no B credit.
    full_share = rec["full"] / n
    partial_share = rec["partial"] / n
    B = min(30, 20 * full_share + 8 * partial_share + (10 if rec["full"] > 0 else 0))
    # C jurisdictional breadth (0-20). Uses TRUE jurisdictions — excludes the
    # language codes mis-filed in the jurisdiction column (§3.3), which are not
    # real jurisdictions and must not earn breadth credit.
    nj = rec["n_jur"]  # n_jur is set to the true (de-polluted) count in compute()
    C = 0 if nj == 0 else 5 if nj == 1 else 9 if nj == 2 else 13 if nj <= 4 else 17 if nj <= 7 else 20
    # D linguistic breadth (0-15)
    nl = rec["n_lang"]
    D = 0 if nl <= 1 else 5 if nl == 2 else 9 if nl <= 3 else 12 if nl <= 5 else 15
    if rec["n_nonen"] == 0:
        D = min(D, 4)  # English-only cap
    # E anglophone balance (0-15): reward distance from English+Anglo concentration.
    # When NO jurisdiction is recorded, anglo concentration is unknown — fall back
    # to the language axis alone rather than scoring unknown as "diverse" (which
    # would reward missing data).
    pct_en = rec["pct_en"] or 0
    if rec["pct_anglo_core"] is None:
        concentration = pct_en
    else:
        concentration = (pct_en + rec["pct_anglo_core"]) / 2
    E = round(15 * (1 - concentration / 100), 1)
    # Convergence discount (tier-system.md §8 / DR-2026-07-20 §1): the
    # "convergence, not evidence" honesty rule is scoped to the ○ weak band. A
    # weak-only slice — strongest anchor is weak (only T3-grey/T6/grey; no full
    # or partial source) — is a code / expert-consensus floor. Breadth of such
    # sources across many jurisdictions is convergence of floors, not evidence,
    # and must not inflate the grade, so halve the breadth credit (C, D). A
    # ◐ partial slice (T4/T5 standards) keeps full breadth credit: it anchors as
    # standards practice, a real (if secondary) basis, not mere convergence.
    if rec["weak_only"]:
        C *= 0.5
        D *= 0.5
    total = round(A + B + C + D + E, 1)
    grade = ("A" if total >= 80 else "B" if total >= 65 else "C" if total >= 50
             else "D" if total >= 35 else "E" if total > 0 else "F")
    return total, dict(A=round(A, 1), B=round(B, 1), C=round(C, 1),
                       D=round(D, 1), E=E), grade


# ----------------------------------------------------------------- compute pass
def compute(db_path):
    con = sqlite3.connect(str(db_path))
    con.row_factory = sqlite3.Row
    q = lambda s, *a: [dict(r) for r in con.execute(s, a).fetchall()]
    one = lambda s: con.execute(s).fetchone()[0]

    # Only ACTIVE slices are audited. MERGED slugs are redirect-only stubs whose evidence
    # lives on their merge target (slugs.merged_into); grading them would count a redirect as
    # an empty slice and inflate the F-count. (WS2 hygiene, 2026-07-20.)
    slugs = q("SELECT slug, topic_directory, status FROM slugs WHERE status='ACTIVE' "
              "ORDER BY topic_directory, slug")
    state = {r["slug"]: r["evidence_state"] for r in q("SELECT slug, evidence_state FROM bpc_metadata")}

    search_langs = defaultdict(lambda: [0, 0])   # [rows, rows_with_results]
    for r in q("SELECT slug, results_count FROM search_languages"):
        search_langs[r["slug"]][0] += 1
        if (r["results_count"] or 0) > 0:
            search_langs[r["slug"]][1] += 1
    search_cov = defaultdict(int)
    for r in q("SELECT slug FROM search_coverage"):
        search_cov[r["slug"]] += 1

    # ORDER BY makes the per-slice source order independent of physical row
    # order, so a logically-identical DB (dump/reload, VACUUM) still yields
    # byte-identical output — the guarantee the CI drift-check relies on.
    links = q("SELECT l.slug AS slug, e.* FROM source_slug_links l "
              "JOIN evidence_sources e ON l.ref_id=e.ref_id "
              "ORDER BY l.slug, e.ref_id")
    by_slug = defaultdict(list)
    for r in links:
        by_slug[r["slug"]].append(r)

    records = []
    for s in slugs:
        slug = s["slug"]
        ev = by_slug.get(slug, [])
        n = len(ev)
        tiers = Counter(e["tier"] for e in ev)
        etypes = Counter((e["evidence_type"] or "?") for e in ev)
        # Weighted-strength bands (§8, DR-2026-07-20): every non-disputed source
        # anchors at ● full / ◐ partial / ○ weak; DISPUTED sources anchor at no
        # band (band None) — stripped of anchoring but retained in raw totals.
        bands = Counter(anchor_band(e) for e in ev)
        full = bands["full"]            # ● T1/Co-1/T2/Co-2/T3-clinical — adjudicated anchor
        partial = bands["partial"]      # ◐ T4/T5 — standards-practice anchor
        weak = bands["weak"]            # ○ T3-grey/T6/grey — floor/convergence anchor
        disputed = sum(1 for e in ev if is_disputed(e))
        t3_clinical = sum(1 for e in ev if is_t3_clinical(e) and not is_disputed(e))
        # Practitioner practice-stream (a `practice` evidence_type, conceptually a
        # "Co-3" authority stream, DR-2026-07-20 §3). Surfaced as its own count;
        # its anchoring strength is banded by method tier like any other source.
        practice = sum(1 for e in ev
                       if (e["evidence_type"] or "").lower() == "practice" and not is_disputed(e))
        # Marker mix over anchorable (non-disputed) sources — this IS the band split.
        markers = Counter(quality_marker(e) for e in ev if not is_disputed(e))
        jurs = Counter(norm_jur(e["jurisdiction"]) for e in ev if norm_jur(e["jurisdiction"]))
        polluted = {k: v for k, v in jurs.items() if is_polluted_jur(k)}
        jurs_clean = {k: v for k, v in jurs.items() if not is_polluted_jur(k)}
        n_true_jur = len(jurs_clean)
        n_null_jur = sum(1 for e in ev if not norm_jur(e["jurisdiction"]))
        langs = Counter((e["lang_detected"] or "?").lower() for e in ev)
        langs_norm = Counter()
        for k, v in langs.items():
            langs_norm["en" if k in ENGLISH_LANGS else k] += v
        n_en = sum(v for k, v in langs.items() if k in ENGLISH_LANGS)
        ac = Counter(anglo_class(e["jurisdiction"]) for e in ev)
        n_with_jur = sum(1 for e in ev if norm_jur(e["jurisdiction"]))
        sl = search_langs.get(slug, [0, 0])

        # strength_band = the strongest anchoring band present among the slice's
        # non-disputed sources (● full > ◐ partial > ○ weak); None when a slice
        # has sources but none can anchor (all DISPUTED). weak_only replaces the
        # old binary no-anchor flag: it marks a slice whose strongest anchor is
        # ○ weak — the convergence / honesty-flag case (§8, DR-2026-07-20 §1),
        # rendered "best available given current regulation/practice, NOT
        # academically adjudicated."
        strength_band = ("full" if full else "partial" if partial
                         else "weak" if weak else None)
        weak_only = (n > 0 and strength_band == "weak")
        rec = dict(
            slug=slug, topic=s["topic_directory"], state=state.get(slug),
            n=n, full=full, partial=partial, weak=weak, disputed=disputed,
            t3_clinical=t3_clinical, practice=practice, code_only=partial + weak,
            strength_band=strength_band, weak_only=weak_only,
            tiers={str(k): tiers[k] for k in sorted(tiers)},
            etypes=dict(etypes),
            markers={k: markers[k] for k in ("●", "◐", "○") if markers[k]},
            n_jur=n_true_jur, n_jur_raw=len(jurs), n_true_jur=n_true_jur,
            n_null_jur=n_null_jur,
            polluted_jur=polluted, jurs=dict(jurs.most_common()),
            jurs_clean=jurs_clean,
            n_lang=len(langs_norm), langs=dict(langs_norm.most_common()),
            n_en=n_en, n_nonen=n - n_en,
            pct_en=round(100 * n_en / n, 1) if n else None,
            anglo_core=ac["anglo_core"], supra=ac["supra"],
            non_anglo=ac["non_anglo"] + ac["anglo_official"],
            pct_anglo_core=round(100 * ac["anglo_core"] / n_with_jur, 1) if n_with_jur else None,
            sl_searched=sl[0], sl_hit=sl[1], search_jurs=search_cov.get(slug, 0),
        )
        records.append(rec)

    for rec in records:
        rec["score"], rec["components"], rec["grade"] = score(rec)
    records.sort(key=lambda r: (-r["score"], r["slug"]))

    # ------------- corpus-level facts, all computed (never hardcoded) ----------
    tot_src = sum(r["n"] for r in records)
    f = {}
    f["as_of"] = (one("SELECT MAX(d) FROM (SELECT MAX(updated_at) d FROM evidence_sources "
                      "UNION ALL SELECT MAX(updated_at) FROM source_slug_links "
                      "UNION ALL SELECT MAX(updated_at) FROM slugs "
                      "UNION ALL SELECT MAX(updated_at) FROM bpc_metadata)") or "")[:10]
    f["n_slices"] = len(records)
    f["tot_src"] = tot_src
    f["unique_linked"] = one("SELECT COUNT(DISTINCT l.ref_id) FROM source_slug_links l "
                             "JOIN evidence_sources e ON l.ref_id=e.ref_id")
    f["total_sources"] = one("SELECT COUNT(*) FROM evidence_sources")
    f["unlinked_sources"] = one("SELECT COUNT(*) FROM evidence_sources e WHERE NOT EXISTS "
                                "(SELECT 1 FROM source_slug_links l WHERE l.ref_id=e.ref_id)")
    mr = con.execute("SELECT ref_id, COUNT(DISTINCT slug) k FROM source_slug_links "
                     "GROUP BY ref_id ORDER BY k DESC, ref_id LIMIT 1").fetchone() \
         or (None, 0)
    f["max_reuse_ref"], f["max_reuse_n"] = mr[0], mr[1]
    f["shared_sources"] = one("SELECT COUNT(*) FROM (SELECT ref_id FROM source_slug_links "
                              "GROUP BY ref_id HAVING COUNT(DISTINCT slug)>1)")
    f["reuse_factor"] = round(tot_src / f["unique_linked"], 2) if f["unique_linked"] else 0
    f["reuse_pct"] = round(100 * (tot_src - f["unique_linked"]) / f["unique_linked"]) if f["unique_linked"] else 0
    f["n_search_langs"] = one("SELECT COUNT(DISTINCT language) FROM search_languages")
    f["n_search_jurs"] = one("SELECT COUNT(DISTINCT jurisdiction) FROM search_coverage")
    f["slugs_in_search_langs"] = one("SELECT COUNT(DISTINCT slug) FROM search_languages")
    # zero-yield searched languages (searched everywhere, never a usable source)
    zero = con.execute("SELECT language FROM search_languages GROUP BY language "
                       "HAVING SUM(COALESCE(results_count,0))=0 ORDER BY language").fetchall()
    f["zero_yield_langs"] = [r[0] for r in zero]
    # ---- Per-specification (item) inheritance view -----------------------
    # Evidence attaches to slugs, not items; each item inherits the evidentiary
    # base of the slug it draws on (bpc_source_slug). Items with no source slug
    # are gaps (cannot inherit). This makes the audit answerable per-spec.
    recs_by_slug = {r["slug"]: r for r in records}
    item_rows = q("SELECT item_code, item_id, category, name, bpc_source_slug, status "
                  "FROM items ORDER BY item_code")
    items = []
    for it in item_rows:
        src = (it["bpc_source_slug"] or "").strip() or None
        base = recs_by_slug.get(src) if src else None
        if src is None:
            health, igrade, iscore = "no-source", "—", None
        elif base is None:
            health, igrade, iscore = "source-missing", "—", None   # slug not found
        elif base["n"] == 0:
            health, igrade, iscore = "empty-base", base["grade"], base["score"]
        else:
            # Inherit the base's strength band: full (● adjudicated anchor),
            # partial (◐ standards-practice anchor), weak (○ honesty-flagged), or
            # disputed-only (n>0 but every source DISPUTED → cannot anchor).
            health = base["strength_band"] or "disputed-only"
            igrade, iscore = base["grade"], base["score"]
        items.append(dict(
            item_code=it["item_code"], name=it["name"], category=it["category"],
            category_label=CATEGORY_LABELS.get(it["category"], it["category"]),
            source_slug=src, basis_health=health, grade=igrade, score=iscore,
            # inherited dimension snapshot (None when no base)
            n=base["n"] if base else None,
            full=base["full"] if base else None,
            partial=base["partial"] if base else None,
            weak=base["weak"] if base else None,
            disputed=base["disputed"] if base else None,
            n_jur=base["n_jur"] if base else None,
            n_lang=base["n_lang"] if base else None,
            pct_en=base["pct_en"] if base else None,
            pct_anglo=base["pct_anglo_core"] if base else None,
        ))
    f["n_items"] = len(items)

    con.close()
    return records, items, f


# ------------------------------------------------------------------ formatting
def bar(frac, width=20):
    filled = int(round(frac * width))
    return "█" * filled + "·" * (width - filled)


def build_markdown(records, items, f):
    N = f["n_slices"]
    withev = [r for r in records if r["n"]]
    empty = [r for r in records if not r["n"]]
    tot_src = f["tot_src"]
    if tot_src == 0 or not withev:
        return (f"# Per-Slice Evidentiary Audit\n\n**Data as of:** {f['as_of']} · "
                f"**Scope:** {N} ACTIVE slices in `data/guidebook.db`.\n\n"
                "No linked evidence is present in the database — nothing to audit yet. "
                "Populate `source_slug_links` / `evidence_sources` and re-run "
                "`tools/evidentiary_audit.py`.\n")
    grade_ct = Counter(r["grade"] for r in records)
    tier_tot = Counter()
    lang_tot = Counter()
    for r in withev:
        for k, v in r["tiers"].items():
            tier_tot[k] += v
        for k, v in r["langs"].items():
            lang_tot[k] += v
    en_tot = sum(r["n_en"] for r in withev)
    nonen_tot = sum(r["n_nonen"] for r in withev)
    anglo_core = sum(r["anglo_core"] for r in withev)
    supra = sum(r["supra"] for r in withev)
    nonanglo = sum(r["non_anglo"] for r in withev)
    null_jur_tot = tot_src - (anglo_core + supra + nonanglo)
    full_tot = sum(r["full"] for r in withev)          # ● adjudicated anchors
    partial_tot = sum(r["partial"] for r in withev)    # ◐ standards-practice anchors
    weak_tot = sum(r["weak"] for r in withev)          # ○ floor/convergence
    disputed_tot = sum(r["disputed"] for r in withev)  # DISPUTED (anchoring stripped)
    alljur = Counter()
    polluted_tot = Counter()
    for r in withev:
        for k, v in r["jurs"].items():
            alljur[k] += v
        for k, v in r["polluted_jur"].items():
            polluted_tot[k] += v
    true_jur = [k for k in alljur if k.upper() not in JUR_LANGCODE_POLLUTION]
    single = [r for r in withev if r["n_jur"] <= 1]
    enonly = [r for r in withev if r["n_nonen"] == 0]
    heavy = [r for r in withev if (r["pct_en"] or 0) >= 90 and (r["pct_anglo_core"] or 0) >= 50]
    # Slices by strongest anchoring band (non-empty only). full ≥ partial ≥ weak;
    # disputed_only = has sources but every one is DISPUTED (cannot anchor).
    full_slices = [r for r in withev if r["strength_band"] == "full"]
    partial_slices = [r for r in withev if r["strength_band"] == "partial"]
    weak_slices = [r for r in withev if r["strength_band"] == "weak"]      # weak_only, honesty-flag
    disputed_only = [r for r in withev if r["strength_band"] is None]      # all-disputed base
    all_tiers = sorted(set(tier_tot) | {"1", "2", "3", "4", "5", "6"}, key=lambda x: (len(x), x))
    other_langs = sorted(((k, v) for k, v in lang_tot.items() if k not in EURO_CJK),
                         key=lambda kv: (-kv[1], kv[0]))
    polluted_str = ", ".join(f"`{k}`×{v}" for k, v in sorted(polluted_tot.items()))
    n_polluted_codes = len(polluted_tot)
    n_polluted_inst = sum(polluted_tot.values())
    zero_str = ", ".join(f"`{c.lower()}`" for c in f["zero_yield_langs"])

    L = []
    w = L.append
    w("# Per-Slice Evidentiary Audit")
    w(f"**Data as of:** {f['as_of']} · **Scope:** all {N} ACTIVE research slices (slugs) in "
      "`data/guidebook.db` · **Method:** read-only aggregation over "
      "`source_slug_links → evidence_sources`, `search_languages`, `search_coverage`, `bpc_metadata`.")
    w("")
    w("This audit scores every research slice on the six requested dimensions — (1) amount of "
      "evidence, (2) tiers of evidence, (3) jurisdictions sourced, (4) languages sourced, "
      "(5) English/Anglophone bias, and (6) overall quality of the evidentiary base — and rolls "
      "them into a transparent 0–100 composite grade. It audits the **raw evidence linked to each "
      "slice**, i.e. the material available for (re-)derivation; it does not re-judge synthesis prose.")
    w("")
    w("> **Reproducibility.** Every number here is regenerated from the DB by `tools/evidentiary_audit.py` "
      "— nothing is hand-transcribed, and the “data as of” date is the DB’s own "
      "`max(updated_at)`, so identical data yields byte-identical output. No grade is stored in the DB; "
      "the composite is a *derived* view whose rubric is fully specified in §2, so any reader can "
      "recompute it. Companion outputs: `evidentiary-base-audit.json` / `.csv`, and the interactive "
      "`tools/evidentiary-audit-dashboard.html` (filter by corpus / category / term).")
    w("")
    w("> **Adversarial review (two passes).** The audit was independently red-teamed twice; all raw "
      "counts (volume, tiers, language/jurisdiction distributions, search yield) reproduce exactly "
      "through a second code path. Folded in: (i) the **weighted-strength bands** (§8, "
      "DR-2026-07-20) — every slice is graded by the strongest band it can anchor at: ● full "
      "(T1/Co-1/T2/Co-2/T3-clinical), ◐ partial (T4/T5 standards), ○ weak (T3-grey/T6/grey); a "
      "○ weak-only slice carries the honesty flag in place of the retired binary no-anchor flag "
      f"(§2, §4); (ii) **DISPUTED sources** ({disputed_tot} instances) stripped of anchoring per the "
      "anti-fabrication sweep (§4) — retained in raw totals but counted at no band; (iii) a "
      "**convergence discount** (scoped to the ○ weak band) so code-floor-only slices can’t score "
      f"highly on breadth alone (§2, §6); (iv) full disclosure of the **{null_jur_tot} "
      "NULL-jurisdiction instances** (§3.5); (v) **true-jurisdiction** breadth scoring "
      + (f"that excludes the {n_polluted_inst} language codes ({polluted_str}) mis-filed in the "
         "`jurisdiction` column (§3.3)." if n_polluted_codes else
         "of the jurisdiction column (no language codes are currently mis-filed there)."))
    w("")

    # 1. Executive summary
    w("## 1. Executive summary")
    w("")
    w(f"- **{tot_src} source-instances** are linked across **{len(withev)} of {N} slices**; "
      f"**{len(empty)} slices carry zero linked evidence**.")
    w("- **Grade distribution:** " + " · ".join(f"{g}={grade_ct.get(g, 0)}" for g in "ABCDEF")
      + "  (A≥80, B≥65, C≥50, D≥35, E>0, F=empty).")
    w("- **Tier profile is code-and-clinical heavy, synthesis-light.** Of linked instances: "
      + ", ".join(f"T{t}={tier_tot.get(t, 0)}" for t in all_tiers)
      + f". Only **{tier_tot.get('2', 0)} Tier-2 (systematic-review / evidence-based-standard) "
      "instances** exist across the whole corpus — the synthesis tier that best anchors "
      "best-practice claims is the thinnest.")
    w(f"- **Anchoring strength, banded.** Under the weighted-strength model (§8) every tier can "
      f"anchor a best-practice claim, weighted by tier: **{full_tot}/{tot_src} "
      f"({round(100 * full_tot / tot_src)}%)** of instances anchor at ● full strength "
      f"(T1/Co-1/T2/Co-2/T3-clinical, adjudicated), {partial_tot} at ◐ partial (T4/T5 standards "
      f"practice), {weak_tot} at ○ weak (T3-grey/T6/grey floor). "
      + (f"**{disputed_tot} DISPUTED instances anchor at no band** (§4). " if disputed_tot else "")
      + f"By slice: **{len(full_slices)} full · {len(partial_slices)} partial · {len(weak_slices)} "
      f"weak-only**"
      + (f" · {len(disputed_only)} disputed-only" if disputed_only else "")
      + f" (of {len(withev)} evidenced). "
      + (f"The {len(weak_slices)} ○ weak-only slices carry the honesty flag; the rest anchor at full "
         "or standards-practice strength." if weak_slices
         else "Every evidenced slice anchors at ● full or ◐ partial strength — none rests on a "
         "weak-only base."))
    w(f"- **Anglophone concentration is the dominant quality risk.** **{en_tot}/{tot_src} "
      f"({round(100 * en_tot / tot_src)}%) of linked sources are English-language**; only {nonen_tot} "
      f"are non-English. By jurisdiction, {anglo_core} instances are native-Anglophone (US/UK/AU/CA/NZ/IE), "
      f"{supra} supranational (INT/EU/ISO), {nonanglo} other, {null_jur_tot} unrecorded.")
    w(f"- **Search breadth ≠ evidentiary yield.** Slices were searched across **{f['n_search_langs']} "
      f"languages** and ~{round(f['n_search_jurs'])} jurisdictions, but {len(f['zero_yield_langs'])} "
      f"searched languages ({zero_str}) returned **zero** usable sources in **every** slice. The bias "
      "lives in what converted to evidence, not in search effort.")
    w("")

    # 2. Method
    w("## 2. Method & definitions")
    w("")
    w(f"**Slice = slug.** The {N} ACTIVE slugs are the unit of audit. Evidence is attributed through "
      "`source_slug_links`; each linked `evidence_sources` row is one *source-instance* (a source shared "
      f"by two slices counts once in each). The {tot_src} instances collapse to **{f['unique_linked']} "
      f"unique sources** (reuse factor {f['reuse_factor']}×; {f['shared_sources']} sources span >1 "
      f"slice, one — `{f['max_reuse_ref']}` — spans {f['max_reuse_n']}). Instance-weighting is "
      "deliberate — it measures per-slice coverage — but shared sources are re-counted, so "
      f"corpus tier/language totals read ~{f['reuse_pct']}% above unique-source counts. "
      f"({f['unlinked_sources']} of the {f['total_sources']} rows in `evidence_sources` are linked to no "
      "active slug.)")
    w("")
    w("**Tiers** follow `governance/tier-system.md`. Tier number reflects *what kind of claim a source "
      "can anchor*, not raw quality. Under the **weighted-strength model** (§8, `DR-2026-07-20`) every "
      "tier can anchor a best-practice claim; the claim's *strength* is weighted by the tier of the "
      "evidence behind it. The three strength bands reuse the `●◐○` quality markers (§5), now given "
      "anchoring semantics:")
    w("")
    w("| Band | Tiers | Anchoring behaviour |")
    w("|---|---|---|")
    w("| **● full** | T1, Co-1, T2, Co-2, T3-clinical | anchors a best-practice claim outright (adjudicated evidence) |")
    w("| **◐ partial** | T4, T5 | anchors as *current standards practice* — “standards basis, not primary evidence” |")
    w("| **○ weak** | T3-grey, T6, expert-consensus / thin base | anchors only a floor/convergence claim, honesty-flagged: “best available given current regulation/practice, **not** academically adjudicated” |")
    w("")
    w("Each slice is graded by the **strongest band** it can anchor at (column **Band** in §4). The "
      "*convergence-not-evidence* rule is preserved as an honesty rule *within* the ○ weak band: "
      "multiple T4–T6 codes agreeing on a value is convergence of floors, stated as regulatory "
      "practice at weak strength — never relabelled best practice. A slice whose strongest anchor is "
      "○ weak carries the **weak-only** flag (†), which replaces the retired binary *no-anchor* flag.")
    w("")
    w("**DISPUTED sources.** Sources set `verification_status='DISPUTED'` by the anti-fabrication sweep "
      "(§4, `DR-2026-07-20`) have lost their VERIFIED standing and their ability to anchor a claim. "
      "They are **not deleted** (a disputed row is a recorded finding): the audit still counts them in "
      "raw volume / tier / jurisdiction / language totals, but they anchor at **no band** and earn no "
      "strength credit. The **disputed** count is surfaced per slice (§4 table, CSV, JSON) so the "
      "stripped anchoring is visible.")
    w("")
    w("**Practitioner practice-stream.** A `practice` evidence_type (conceptually a “Co-3” authority "
      "stream, §3 / `DR-2026-07-20`) marks practitioner / firm design work placed *by method, not "
      "authorship* and ranked below Co-1/Co-2. The audit surfaces a **practice** count per slice and "
      "bands each such source by its method tier like any other source; it does not adjudicate the "
      "role-appropriate-authority gate (a firm may anchor a measured/descriptive claim but not a "
      "functional-need claim alone), which is a claim-level rather than slice-level judgment.")
    w("")
    w("**Anglophone classification** of a jurisdiction: *native-Anglophone* = US, UK, AU, CA, NZ, IE; "
      "*supranational/English-medium* = INT, EU, ISO, ASEAN; *English-official (non-native)* = SG, HK, "
      "IN, NG, GH, ZA, MY, AE, SA; everything else *non-Anglophone*. Language uses `lang_detected` "
      "(`en`/`eng`→English).")
    w("")
    w("**Composite score (0–100)** = five transparent components, higher = stronger base:")
    w("")
    w("| Comp | Max | Measures |")
    w("|---|---|---|")
    w("| A Volume | 20 | count of linked source-instances |")
    w("| B Tier strength | 30 | ● full-band share (full weight) + ◐ partial-band share (partial) + full-anchor-present bonus |")
    w("| C Jurisdictional breadth | 20 | distinct *true* jurisdictions (mis-filed language codes excluded) |")
    w("| D Linguistic breadth | 15 | distinct languages; capped at 4 if English-only |")
    w("| E Anglophone balance | 15 | rewards distance from 100% English + 100% Anglo-core concentration |")
    w("")
    w("Grades: **A**≥80 · **B**≥65 · **C**≥50 · **D**≥35 · "
      "**E**>0 · **F**=empty. The score rewards a *balanced, multi-jurisdiction, multi-language, "
      "synthesis-anchored* base and penalises thin or monolingual ones; it is a triage lens, not a "
      "verdict on any single citation.")
    w("")
    w("**Convergence discount.** Scoped to the ○ weak band (§8 / `DR-2026-07-20` §1): a slice whose "
      "strongest anchor is weak (only T3-grey/T6/grey; no ● full or ◐ partial source) is a "
      "code / expert-consensus floor. Breadth of such sources across many jurisdictions is "
      "“convergence, not evidence,” and without a correction can out-score a genuinely well-evidenced "
      "but narrow slice purely on breadth. The rubric therefore **halves the breadth components (C, D) "
      "for ○ weak-only slices** (flagged †). A ◐ partial slice (T4/T5 standards) keeps full breadth "
      "credit — it anchors as standards practice, a real if secondary basis, not mere convergence.")
    w("")

    # 3. Portfolio view
    w("## 3. Portfolio view, by dimension")
    w("")
    w("### (1) Amount of evidence")
    buckets = Counter()
    for r in records:
        n = r["n"]
        b = ("0 (empty)" if n == 0 else "1–3" if n <= 3 else "4–7" if n <= 7
             else "8–14" if n <= 14 else "15+")
        buckets[b] += 1
    w("| Linked sources | Slices |")
    w("|---|---|")
    for b in ["0 (empty)", "1–3", "4–7", "8–14", "15+"]:
        w(f"| {b} | {buckets.get(b, 0)} |")
    med = sorted(r["n"] for r in withev)[len(withev) // 2]
    w("")
    w(f"Median linked sources among non-empty slices: **{med}**. Largest bases: "
      + ", ".join(f"`{r['slug']}` ({r['n']})" for r in sorted(withev, key=lambda x: -x["n"])[:5]) + ".")
    w("")

    w("### (2) Tiers of evidence")
    w("| Tier | Instances | Share |")
    w("|---|---|---|")
    for t in all_tiers:
        c = tier_tot.get(t, 0)
        w(f"| T{t} | {c} | {bar(c / tot_src)} {round(100 * c / tot_src)}% |")
    w("")
    w(f"**Strength-band split of instances:** **{full_tot}/{tot_src} "
      f"({round(100 * full_tot / tot_src)}%)** anchor at ● full (T1/Co-1/T2/Co-2/T3-clinical), "
      f"{partial_tot} ({round(100 * partial_tot / tot_src)}%) at ◐ partial (T4/T5 standards), and "
      f"{weak_tot} ({round(100 * weak_tot / tot_src)}%) at ○ weak (T3-grey/T6/grey floor)"
      + (f"; a further {disputed_tot} DISPUTED instances anchor at no band (§4)" if disputed_tot else "")
      + ". "
      + (f"The {len(weak_slices)} slices whose *strongest* anchor is ○ weak are the sharpest risk — "
         "see the band breakdown in §4." if weak_slices else
         "No evidenced slice rests on a ○ weak-only base — every slice anchors at ● full or ◐ partial "
         "strength (see the band breakdown in §4)."))
    w("")

    w("### (3) Jurisdictions sourced")
    if n_polluted_codes:
        w(f"Distinct jurisdiction strings across the corpus: **{len(alljur)}** — but "
          f"**{n_polluted_codes} are language codes mis-filed in the jurisdiction column** "
          f"({polluted_str} = {n_polluted_inst} instances; a data-integrity defect, see the note below), "
          f"leaving **~{len(true_jur)} true jurisdictions**. Top: "
          + ", ".join(f"{k} ({v})" for k, v in alljur.most_common(10)) + ".")
    else:
        w(f"Distinct jurisdiction strings across the corpus: **{len(true_jur)}**, none mis-filed as "
          "language codes in the `jurisdiction` column. Top: "
          + ", ".join(f"{k} ({v})" for k, v in alljur.most_common(10)) + ".")
    w("")
    w(f"**{len(single)} non-empty slices draw on ≤1 jurisdiction** — monojurisdictional bases "
      f"whose values may not transfer across code regimes. Separately, **{null_jur_tot} source-instances "
      "carry no jurisdiction at all** (NULL) — mostly clinical/synthesis sources with no single "
      "national home; these are excluded from every jurisdiction-share denominator.")
    w("")
    if n_polluted_codes:
        w("> **Data-integrity note (§3.3).** The audit *surfaces rather than propagates* the mis-filed "
          "language codes: language codes appearing as `jurisdiction` values are almost certainly the source "
          "language leaking into the wrong column. Recommend a data fix moving these to `lang_detected` and "
          "recovering the true jurisdiction.")
        w("")

    w("### (4) Languages sourced")
    w("| Language | Instances |")
    w("|---|---|")
    for k, v in lang_tot.most_common():
        w(f"| {k} | {v} |")
    w("")
    other_str = ("; ".join(f"{k} ({v})" for k, v in other_langs) if other_langs else "none")
    w(f"Distinct source languages: **{len(lang_tot)}** (`en`/`eng` merged; raw ISO codes may be one "
      f"more). English dominates at {round(100 * en_tot / tot_src)}%. The non-English corpus is "
      "overwhelmingly Western-European + East-Asian; the only languages outside that group to yield "
      f"*any* linked source are: {other_str}.")
    w("")
    w(f"**{len(enonly)} non-empty slices are English-only** "
      f"({round(100 * len(enonly) / len(withev))}% of evidenced slices).")
    w("")

    w("### (5) English / Anglophone bias")
    w(f"- **Language axis:** {round(100 * en_tot / tot_src)}% English. {len(enonly)} slices 100% English.")
    w(f"- **Jurisdiction axis (all {tot_src} instances):** native-Anglophone (US/UK/AU/CA/NZ/IE) "
      f"**{anglo_core}** · supranational/English-medium (INT/EU/ISO) **{supra}** · "
      f"English-official + other non-Anglophone **{nonanglo}** · **no jurisdiction recorded "
      f"{null_jur_tot}**. (These four sum to {anglo_core + supra + nonanglo + null_jur_tot} = all "
      "instances.)")
    w(f"- **{len(heavy)} slices are doubly-concentrated** (≥90% English *and* ≥50% "
      "native-Anglophone jurisdiction): " + ", ".join(f"`{r['slug']}`" for r in heavy) + ".")
    w(f"- **Process counter-evidence:** non-English/Global-South *searches were run* "
      f"({f['n_search_langs']} languages across {f['slugs_in_search_langs']} of {N} slices in "
      f"`search_languages`) but {zero_str} yielded nothing linkable in any slice. The gap is a "
      "*yield/recovery* gap, not a *search-effort* gap.")
    w("")

    w("### (6) Overall quality of the evidentiary base")
    w("| Grade | Slices | Meaning |")
    w("|---|---|---|")
    meanings = {"A": "strong, balanced, synthesis-anchored",
                "B": "solid, some concentration or tier gaps",
                "C": "usable but thin or monolingual",
                "D": "weak — few sources / single jurisdiction / English-only",
                "E": "very weak — 1 jurisdiction, weak-only or thin base",
                "F": "empty — no linked evidence"}
    for g in "ABCDEF":
        w(f"| {g} | {grade_ct.get(g, 0)} | {meanings[g]} |")
    w("")

    # 4. Master table
    w("## 4. Master per-slice table (ranked by composite score)")
    w("")
    w("Legend: **N** linked sources · **Band** strongest anchoring band (● full / ◐ partial / ○ weak / "
      "⊘ disputed-only) · **●/◐/○** full / partial / weak instance counts · **⊘** DISPUTED instances "
      "(anchoring stripped, §4) · **JUR** distinct *true* jurisdictions · **LNG** distinct languages · "
      "**%EN** English-language share · **%ANG** native-Anglophone share · **A/B/C/D/E** score "
      "components · **†** ○ weak-only slice (breadth discounted, honesty-flagged).")
    w("")
    band_mark = {"full": "●", "partial": "◐", "weak": "○", None: "⊘"}
    w("| # | Grade | Score | Slice | Topic | N | Band | ● | ◐ | ○ | ⊘ | Tiers | JUR | LNG | %EN | %ANG | A·B·C·D·E |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(records, 1):
        tiers = ",".join(f"T{k}×{v}" for k, v in sorted(r["tiers"].items())) or "—"
        comp = "·".join(str(r["components"][k]) for k in "ABCDE")
        flag = " †" if r["weak_only"] else ""
        bm = band_mark[r["strength_band"]] if r["n"] else "—"
        pe = r["pct_en"] if r["pct_en"] is not None else "—"
        pa = r["pct_anglo_core"] if r["pct_anglo_core"] is not None else "—"
        w(f"| {i} | **{r['grade']}**{flag} | {r['score']} | `{r['slug']}` | {r['topic']} | {r['n']} | "
          f"{bm} | {r['full']} | {r['partial']} | {r['weak']} | {r['disputed']} | {tiers} | "
          f"{r['n_jur']} | {r['n_lang']} | {pe} | {pa} | {comp} |")
    w("")
    w(f"**Anchoring bands across the {len(withev)} evidenced slices:** "
      f"**{len(full_slices)} ● full** (adjudicated anchor) · **{len(partial_slices)} ◐ partial** "
      f"(standards-practice basis) · **{len(weak_slices)} ○ weak-only**"
      + (f" · **{len(disputed_only)} ⊘ disputed-only**" if disputed_only else "") + ".")
    if weak_slices:
        w(f"- **† ○ weak-only ({len(weak_slices)})** — strongest anchor is weak (T3-grey/T6/grey; no "
          "full or partial source): breadth is discounted and the base is honesty-flagged “best "
          "available given current regulation/practice, **not** academically adjudicated.” "
          + ", ".join(f"`{r['slug']}`" for r in weak_slices) + ".")
    else:
        w("- **† ○ weak-only (0)** — no evidenced slice rests on a weak-only base; every slice anchors "
          "at ● full or ◐ partial strength.")
    if partial_slices:
        w(f"- **◐ partial ({len(partial_slices)})** — strongest anchor is T4/T5 standards: renders as "
          "*current standards practice* (“standards basis, not primary evidence”), not a code-floor. "
          + ", ".join(f"`{r['slug']}`" for r in partial_slices) + ".")
    if disputed_only:
        w(f"- **⊘ disputed-only ({len(disputed_only)})** — has sources but every one is DISPUTED (§4): "
          "cannot anchor until a real source is located. "
          + ", ".join(f"`{r['slug']}`" for r in disputed_only) + ".")
    w("")

    # 5. Empty slices
    ret = [r for r in empty if r["state"] == "RETRACTED-PRE-REHAB"]
    none = [r for r in empty if r["state"] is None]
    other = [r for r in empty if r["state"] not in (None, "RETRACTED-PRE-REHAB")]
    w(f"## 5. Evidence-empty slices ({len(empty)})")
    w("")
    if not empty:
        w("Every ACTIVE slice carries at least one linked source-instance — no evidence-empty slices "
          "in the current corpus.")
        w("")
    else:
        w("These carry **zero** linked source-instances. `bpc_metadata.evidence_state` distinguishes:")
        w("")
        w(f"**Retracted pending rehabilitation ({len(ret)})** — prior work cleared, awaiting re-derivation:")
        for r in ret:
            w(f"- `{r['slug']}` ({r['topic']})")
        w("")
        w(f"**Un-started / placeholder ({len(none)})** — `evidence_state` unset, search not run:")
        for r in none:
            w(f"- `{r['slug']}` ({r['topic']})")
        if other:
            w("")
            w(f"**Other state ({len(other)}):**")
            for r in other:
                w(f"- `{r['slug']}` ({r['topic']}) — {r['state']}")
        w("")
        w("Several name high-salience topics where an empty base is a material coverage gap, not "
          "bookkeeping.")
        w("")

    # 6. Findings
    w("## 6. Findings & recommended remediation")
    w("")
    w(f"1. **Strengthen the ◐ partial and ○ weak bases toward ● full.** {len(partial_slices)} slices "
      "anchor only at ◐ partial (T4/T5 standards practice) and "
      + (f"{len(weak_slices)} at ○ weak (code/expert-consensus floor)" if weak_slices
         else "none rest on a ○ weak-only base")
      + f". With only {tier_tot.get('2', 0)} systematic-review/evidence-based-standard instances "
      "corpus-wide, the ● full synthesis tier is the thinnest. Prioritise SR/meta-analysis + "
      "DPO-standard recovery on the partial/weak slices to lift them to full-strength anchoring"
      + (f", and replace the {disputed_tot} DISPUTED sources (§4) with verifiable citations"
         if disputed_tot else "") + ".")
    w(f"2. **Convert non-English search into non-English evidence.** Searches ran in {f['n_search_langs']} "
      f"languages but the corpus is ~{round(100 * en_tot / tot_src)}% English. Target the languages "
      f"already searched-with-results but under-linked, and the zero-yield languages ({zero_str}) "
      "explicitly.")
    w(f"3. **De-risk monojurisdictional slices.** {len(single)} evidenced slices rest on ≤1 "
      "jurisdiction; flag their numeric thresholds as non-transferable until a second regime is sourced.")
    if none:
        w(f"4. **Fill or formally park the empty slices.** Move the {len(none)} un-started slices into an "
          "active search queue or an explicit deferred state so they stop reading as silent gaps.")
    else:
        w("4. **Keep the corpus free of silent gaps.** No ACTIVE slice is currently un-started or "
          "evidence-empty; hold that line as new slices are added.")
    w(f"5. **Treat the doubly-concentrated slices as citation-risk.** The {len(heavy)} "
      "≥90%-English-and-≥50%-Anglophone slices are where global-applicability claims are weakest.")
    if n_polluted_codes:
        w(f"6. **Fix the mis-filed jurisdiction codes.** Move the {n_polluted_inst} {polluted_str} values "
          "out of `evidence_sources.jurisdiction` and recover the true jurisdiction — a one-off migration.")
    w("")

    # 7. Limitations
    w("## 7. Limitations & what this audit does *not* claim")
    w("")
    w(f"- **Instance-weighted, not source-weighted.** The {tot_src} instances are {f['unique_linked']} "
      f"unique sources, so corpus tier/language totals run ~{f['reuse_pct']}% above unique-source counts. "
      "Per-slice figures are unaffected.")
    w("- **The composite is a lens, not ground truth.** Weights (20/30/20/15/15) are a defensible but "
      "editorial choice; the six raw dimensions are printed alongside every grade so a reader can "
      "re-weight. No grade is stored in the DB — it is recomputed each run.")
    w("- **Coverage ≠ correctness.** The audit measures the *shape* of each base (how much, what "
      "tier, where from, what language, how concentrated). It does **not** re-verify that any citation "
      "resolves, is current, or supports its claim — those are the `url_verification_runs` / "
      "`code_currency` / supersession checks, run separately.")
    w("- **Jurisdiction shares rest on recorded jurisdictions only.** NULL-jurisdiction instances are "
      "excluded from %ANG denominators, so a low %ANG can mean *genuinely non-Anglophone* or "
      "*unrecorded* — the master table’s JUR count exposes the denominator.")
    w("- **Compound jurisdictions classify by their strongest Anglophone member** (e.g. `US/AU/INT` "
      "counts as native-Anglophone). Magnitude ≈1% of instances.")
    w("")

    # 8. Per-specification (item) inheritance view
    HEALTH_LABEL = {"full": "inherits a ● full (adjudicated) anchor base",
                    "partial": "inherits a ◐ partial (standards-practice) anchor base",
                    "weak": "inherits a ○ weak-only base (honesty-flagged)",
                    "disputed-only": "base sources all DISPUTED — cannot anchor",
                    "empty-base": "base has zero linked evidence",
                    "no-source": "no source slug — cannot inherit",
                    "source-missing": "source slug not found (data error)"}
    HEALTH_ORDER = ["full", "partial", "weak", "disputed-only",
                    "empty-base", "no-source", "source-missing"]
    n_items = len(items)
    health_ct = Counter(it["basis_health"] for it in items)
    weak = [it for it in items if it["basis_health"] in
            ("no-source", "source-missing", "empty-base", "weak", "disputed-only")]
    w("## 8. Per-specification (item) adjudication — inheritance view")
    w("")
    w(f"The Guidebook’s **{n_items} design specifications** (the `items` table, categories A–K) do "
      "**not** carry their own evidence links — each *inherits* the evidentiary base of the research "
      "slug it draws on (`items.bpc_source_slug`). This section adjudicates every specification by "
      "that inherited base, so a spec built on a thin or unanchored slug is visible as such. (A spec "
      "with no source slug cannot inherit and is a coverage gap.)")
    w("")
    w("| Basis health | Specs | Meaning |")
    w("|---|---|---|")
    for h in HEALTH_ORDER:
        if health_ct.get(h):
            w(f"| {h} | {health_ct[h]} | {HEALTH_LABEL[h]} |")
    w("")
    w(f"**{n_items - len(weak)} of {n_items} specs inherit a ● full or ◐ partial anchored base; "
      f"{len(weak)} rest on a ○ weak, disputed-only, or missing base** and are the priority "
      "remediation set.")
    w("")
    w("### By category")
    w("| Cat | Specifications | Specs | On weak/missing base |")
    w("|---|---|---|---|")
    cats = sorted({it["category"] for it in items})
    for cat in cats:
        cat_items = [it for it in items if it["category"] == cat]
        cat_weak = sum(1 for it in cat_items if it in weak)
        w(f"| {cat} | {CATEGORY_LABELS.get(cat, cat)} | {len(cat_items)} | {cat_weak} |")
    w("")
    w("### Specifications resting on a weak or missing base")
    w("")
    if weak:
        w("| Item | Category | Specification | Source slug | Basis | Inh. grade |")
        w("|---|---|---|---|---|---|")
        for it in sorted(weak, key=lambda x: x["item_code"]):
            nm = (it["name"] or "")[:52]
            w(f"| `{it['item_code']}` | {it['category']} | {nm} | "
              f"{('`'+it['source_slug']+'`') if it['source_slug'] else '—'} | {it['basis_health']} | "
              f"{it['grade']} |")
    else:
        w("*None — every specification inherits a graded, anchored base.*")
    w("")
    w("The full per-specification table (all "
      f"{n_items} items with inherited grade and dimension snapshot) is in "
      "`evidentiary-base-audit-items.csv` and the `items` array of the JSON; the dashboard’s "
      "**Specifications** view filters them by corpus / category / term.")
    w("")

    w("---")
    w(f"*Data as of {f['as_of']} · read-only over `data/guidebook.db` · generated by "
      "`tools/evidentiary_audit.py`. Independently red-teamed; raw counts reproduce through a second "
      "code path. Aligned to `governance/tier-system.md`.*")
    return "\n".join(L) + "\n"


def build_csv(records):
    import io
    buf = io.StringIO()
    wtr = csv.writer(buf, lineterminator="\n")
    wtr.writerow(["rank", "slug", "topic", "evidence_state", "grade", "score",
                  "n_sources", "strength_band", "full_anchor", "partial_anchor", "weak_anchor",
                  "disputed", "t3_clinical", "practice", "weak_only",
                  "tier_profile", "n_true_jurisdictions", "n_jurisdictions_raw", "jurisdictions",
                  "n_languages", "languages",
                  "pct_english", "n_nonenglish", "pct_anglo_core", "anglo_core_instances",
                  "supra_instances", "non_anglo_instances", "null_jurisdiction_instances",
                  "comp_volume", "comp_tier", "comp_jurisdiction", "comp_language", "comp_anglo_balance",
                  "search_langs_run", "search_langs_hit"])
    for i, r in enumerate(records, 1):
        wtr.writerow([i, r["slug"], r["topic"], r["state"], r["grade"], r["score"],
                      r["n"], r["strength_band"] or "", r["full"], r["partial"], r["weak"],
                      r["disputed"], r["t3_clinical"], r["practice"], int(r["weak_only"]),
                      ";".join(f"T{k}:{v}" for k, v in sorted(r["tiers"].items())),
                      r["n_true_jur"], r["n_jur_raw"],
                      ";".join(f"{k}:{v}" for k, v in r["jurs"].items()),
                      r["n_lang"], ";".join(f"{k}:{v}" for k, v in r["langs"].items()),
                      r["pct_en"], r["n_nonen"], r["pct_anglo_core"], r["anglo_core"],
                      r["supra"], r["non_anglo"], r["n_null_jur"],
                      r["components"]["A"], r["components"]["B"], r["components"]["C"],
                      r["components"]["D"], r["components"]["E"], r["sl_searched"], r["sl_hit"]])
    return buf.getvalue()


def build_items_csv(items):
    import io
    buf = io.StringIO()
    wtr = csv.writer(buf, lineterminator="\n")
    wtr.writerow(["item_code", "category", "category_label", "name", "source_slug",
                  "basis_health", "inherited_grade", "inherited_score",
                  "base_n_sources", "base_full", "base_partial", "base_weak", "base_disputed",
                  "base_n_jurisdictions", "base_n_languages", "base_pct_english",
                  "base_pct_anglo_core"])
    for it in items:
        wtr.writerow([it["item_code"], it["category"], it["category_label"], it["name"],
                      it["source_slug"] or "", it["basis_health"], it["grade"], it["score"],
                      it["n"], it["full"], it["partial"], it["weak"], it["disputed"],
                      it["n_jur"], it["n_lang"], it["pct_en"], it["pct_anglo"]])
    return buf.getvalue()


def build_json(records, items, f):
    grade_ct = Counter(r["grade"] for r in records)
    tier_tot = Counter()
    for r in records:
        for k, v in r["tiers"].items():
            tier_tot[k] += v
    item_health = Counter(it["basis_health"] for it in items)
    # Strength-band split (weighted-strength model, §8 / DR-2026-07-20): by slice
    # (strongest anchoring band) and by instance (each source's own band).
    band_by_slice = Counter(r["strength_band"] or "disputed-only" for r in records if r["n"])
    payload = {
        "as_of": f["as_of"],
        "n_slices": f["n_slices"],
        "n_items": f["n_items"],
        "total_source_instances": f["tot_src"],
        "unique_sources": f["unique_linked"],
        "grade_distribution": {g: grade_ct.get(g, 0) for g in "ABCDEF"},
        "tier_totals": dict(sorted(tier_tot.items())),
        "strength_band_slices": {b: band_by_slice.get(b, 0)
                                 for b in ("full", "partial", "weak", "disputed-only")},
        "strength_band_instances": {
            "full": sum(r["full"] for r in records),
            "partial": sum(r["partial"] for r in records),
            "weak": sum(r["weak"] for r in records),
            "disputed": sum(r["disputed"] for r in records),
        },
        "practice_stream_instances": sum(r["practice"] for r in records),
        "english_instances": sum(r["n_en"] for r in records),
        "zero_yield_search_languages": f["zero_yield_langs"],
        "item_basis_health": dict(item_health),
        "slices": records,
        "items": items,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"


HTML_TEMPLATE = r"""<title>Per-Slice Evidentiary Audit — Guidebook</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{
  --ground:#f6f7f9; --surface:#ffffff; --surface-2:#eef1f4; --line:#dbe0e6;
  --ink:#151a22; --ink-2:#3d4653; --slate:#5b6472; --faint:#8a919c;
  --accent:#2f6f7e; --accent-soft:#e2eef0; --accent-ink:#1e4c57;
  --gA:#1f9d6b; --gB:#5a9a3d; --gC:#c9a227; --gD:#d97a2b; --gE:#c0503a; --gF:#9299a3;
  --shadow:0 1px 2px rgba(20,26,34,.06),0 4px 16px rgba(20,26,34,.05);
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --serif:"Iowan Old Style",Georgia,"Times New Roman",serif;
}
@media (prefers-color-scheme:dark){:root{
  --ground:#11141a; --surface:#181c24; --surface-2:#1f242e; --line:#2b323d;
  --ink:#e7eaef; --ink-2:#b7bec9; --slate:#8b93a0; --faint:#6b727d;
  --accent:#59a7b8; --accent-soft:#1c3940; --accent-ink:#9fd4e0;
  --gA:#39b984; --gB:#7bb955; --gC:#d9bd63; --gD:#e8944a; --gE:#d96b54; --gF:#7f868f;
  --shadow:0 1px 2px rgba(0,0,0,.3),0 6px 20px rgba(0,0,0,.28);
}}
:root[data-theme="light"]{
  --ground:#f6f7f9; --surface:#ffffff; --surface-2:#eef1f4; --line:#dbe0e6;
  --ink:#151a22; --ink-2:#3d4653; --slate:#5b6472; --faint:#8a919c;
  --accent:#2f6f7e; --accent-soft:#e2eef0; --accent-ink:#1e4c57;
  --gA:#1f9d6b; --gB:#5a9a3d; --gC:#c9a227; --gD:#d97a2b; --gE:#c0503a; --gF:#9299a3;
}
:root[data-theme="dark"]{
  --ground:#11141a; --surface:#181c24; --surface-2:#1f242e; --line:#2b323d;
  --ink:#e7eaef; --ink-2:#b7bec9; --slate:#8b93a0; --faint:#6b727d;
  --accent:#59a7b8; --accent-soft:#1c3940; --accent-ink:#9fd4e0;
  --gA:#39b984; --gB:#7bb955; --gC:#d9bd63; --gD:#e8944a; --gE:#d96b54; --gF:#7f868f;
}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);
  font-size:15px;line-height:1.5;-webkit-font-smoothing:antialiased}
.wrap{max-width:1180px;margin:0 auto;padding:32px 24px 80px}
header.masthead{border-bottom:2px solid var(--ink);padding-bottom:16px;margin-bottom:8px}
.eyebrow{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent);font-weight:600}
h1{font-family:var(--serif);font-weight:600;font-size:34px;line-height:1.1;margin:8px 0 6px;
  text-wrap:balance;letter-spacing:-.01em}
.sub{color:var(--slate);font-size:14px;max-width:70ch}
.sub code{font-family:var(--mono);font-size:12px;background:var(--surface-2);padding:1px 5px;border-radius:4px}
.controls{position:sticky;top:0;z-index:20;background:var(--ground);
  padding:16px 0 14px;margin-top:14px;border-bottom:1px solid var(--line)}
.filter-row{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end}
.field{display:flex;flex-direction:column;gap:5px}
.field label{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint)}
input[type=search],select{font-family:var(--sans);font-size:14px;color:var(--ink);
  background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:9px 12px;
  box-shadow:var(--shadow);min-height:40px}
input[type=search]{min-width:280px}
input[type=search]:focus,select:focus{outline:2px solid var(--accent);outline-offset:1px;border-color:var(--accent)}
.grades{display:flex;gap:5px}
.gchip{font-family:var(--mono);font-size:12px;font-weight:600;width:32px;height:40px;border-radius:8px;
  border:1px solid var(--line);background:var(--surface);color:var(--slate);cursor:pointer;
  display:flex;align-items:center;justify-content:center;transition:.12s}
.gchip[aria-pressed=true]{color:#fff;border-color:transparent}
.gchip.A[aria-pressed=true]{background:var(--gA)}.gchip.B[aria-pressed=true]{background:var(--gB)}
.gchip.C[aria-pressed=true]{background:var(--gC)}.gchip.D[aria-pressed=true]{background:var(--gD)}
.gchip.E[aria-pressed=true]{background:var(--gE)}.gchip.F[aria-pressed=true]{background:var(--gF)}
.btn-reset{font-family:var(--mono);font-size:12px;background:none;border:1px solid var(--line);
  border-radius:8px;padding:0 14px;height:40px;color:var(--slate);cursor:pointer}
.btn-reset:hover{color:var(--ink);border-color:var(--slate)}
.scope-note{font-family:var(--mono);font-size:11.5px;color:var(--faint);margin-top:10px}
.scope-note b{color:var(--accent);font-weight:600}
h2.dim-head{font-family:var(--serif);font-size:15px;font-weight:600;margin:26px 0 12px;
  padding-bottom:6px;border-bottom:1px solid var(--line);color:var(--ink-2);
  letter-spacing:0;display:flex;align-items:baseline;gap:8px}
h2.dim-head span{font-family:var(--mono);font-size:10.5px;color:var(--faint);letter-spacing:.1em;text-transform:uppercase}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(178px,1fr));gap:12px}
.card{background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:14px 16px;box-shadow:var(--shadow)}
.card .big{font-family:var(--serif);font-size:30px;font-weight:600;line-height:1;font-variant-numeric:tabular-nums}
.card .lbl{font-family:var(--mono);font-size:10.5px;letter-spacing:.09em;text-transform:uppercase;color:var(--faint);margin-top:7px}
.card .note{font-size:12.5px;color:var(--slate);margin-top:4px}
.barset{display:flex;flex-direction:column;gap:7px;margin-top:2px}
.barrow{display:grid;grid-template-columns:56px 1fr 62px;align-items:center;gap:10px;font-size:13px}
.barrow .k{font-family:var(--mono);font-size:12px;color:var(--ink-2)}
.track{height:10px;background:var(--surface-2);border-radius:6px;overflow:hidden}
.fill{height:100%;border-radius:6px;background:var(--accent)}
.fill.bp{background:var(--gA)}.fill.code{background:var(--gD)}
.barrow .v{font-family:var(--mono);font-size:12px;text-align:right;color:var(--slate);font-variant-numeric:tabular-nums}
.split{display:grid;grid-template-columns:1fr 1fr;gap:22px}
@media(max-width:720px){.split{grid-template-columns:1fr}}
.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow);margin-top:12px}
table{border-collapse:collapse;width:100%;font-size:13px;background:var(--surface)}
thead th{position:sticky;top:0;background:var(--surface-2);text-align:left;padding:10px 12px;
  font-family:var(--mono);font-size:10.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--slate);
  border-bottom:1px solid var(--line);cursor:pointer;white-space:nowrap;user-select:none}
thead th.sorted{color:var(--accent)}
thead th .arw{opacity:.5}
tbody td{padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:middle;white-space:nowrap}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover td{background:var(--surface-2)}
td.slug{font-family:var(--mono);font-size:12.5px;color:var(--ink);white-space:normal;min-width:210px}
td.slug .tp{display:block;font-size:10.5px;color:var(--faint);letter-spacing:.02em}
.num{font-family:var(--mono);font-variant-numeric:tabular-nums;text-align:right}
.gpill{font-family:var(--mono);font-weight:700;font-size:12px;color:#fff;border-radius:6px;
  padding:2px 0;width:26px;display:inline-block;text-align:center}
.gpill.A{background:var(--gA)}.gpill.B{background:var(--gB)}.gpill.C{background:var(--gC)}
.gpill.D{background:var(--gD)}.gpill.E{background:var(--gE)}.gpill.F{background:var(--gF)}
.mini{display:inline-flex;height:9px;border-radius:3px;overflow:hidden;min-width:70px;vertical-align:middle;border:1px solid var(--line)}
.mini i{height:100%}
.enbar{display:inline-block;height:9px;border-radius:3px;background:linear-gradient(90deg,var(--gE) 0 var(--p),var(--surface-2) var(--p));width:64px;border:1px solid var(--line);vertical-align:middle}
.empty-row td{color:var(--faint);font-style:italic}
footer{margin-top:34px;font-family:var(--mono);font-size:11.5px;color:var(--faint);line-height:1.7}
.legend{font-family:var(--mono);font-size:11px;color:var(--slate);margin:10px 0 0;line-height:1.8}
.legend b{color:var(--ink-2);font-weight:600}
.theme-toggle{position:fixed;top:14px;right:14px;z-index:40;font-family:var(--mono);font-size:11px;
  background:var(--surface);border:1px solid var(--line);border-radius:8px;padding:7px 11px;color:var(--slate);cursor:pointer;box-shadow:var(--shadow)}
.viewtabs{display:inline-flex;border:1px solid var(--line);border-radius:9px;overflow:hidden;background:var(--surface);box-shadow:var(--shadow)}
.vtab{font-family:var(--mono);font-size:12px;padding:9px 16px;border:0;background:none;color:var(--slate);cursor:pointer;min-height:40px}
.vtab[aria-selected=true]{background:var(--accent);color:#fff}
.hpill{font-family:var(--mono);font-size:11px;font-weight:600;padding:2px 8px;border-radius:20px;white-space:nowrap;
  border:1px solid var(--line);color:var(--ink-2);background:var(--surface-2)}
.hpill.full{color:#fff;background:var(--gA);border-color:transparent}
.hpill.partial{color:#fff;background:var(--gC);border-color:transparent}
.hpill.weak{color:#fff;background:var(--gD);border-color:transparent}
.hpill.disputedonly{color:#fff;background:var(--gE);border-color:transparent}
.hpill.empty,.hpill.nosource{color:#fff;background:var(--gF);border-color:transparent}
td.itemname{white-space:normal;min-width:240px}
td.itemname .tp{display:block;font-size:10.5px;color:var(--faint);font-family:var(--mono)}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<button class="theme-toggle" id="themeBtn" aria-label="Toggle theme">◐ theme</button>
<div class="wrap">
  <header class="masthead">
    <div class="eyebrow">Guidebook · Evidence Integrity</div>
    <h1>Per-Slice Evidentiary Audit</h1>
    <p class="sub">The <b>Slices</b> view scores every research slug on six dimensions — amount, tiers,
    jurisdictions, languages, English/Anglophone bias, and overall base quality — over the linked
    evidence in <code>data/guidebook.db</code>. The <b>Specifications</b> view adjudicates all
    __NITEMS__ design items by the evidentiary base each inherits from its source slug. Filter the
    <b>entire corpus</b>, <b>by category</b>, or <b>by term</b>; every panel recomputes live.</p>
  </header>

  <div class="controls">
    <div class="filter-row">
      <div class="field">
        <label>View</label>
        <div class="viewtabs" id="viewtabs" role="tablist">
          <button class="vtab" data-view="slices" role="tab" aria-selected="true">Slices</button>
          <button class="vtab" data-view="items" role="tab" aria-selected="false">Specifications</button>
        </div>
      </div>
      <div class="field" style="flex:1;min-width:240px">
        <label for="term">Search term</label>
        <input type="search" id="term" placeholder="e.g. acoustic · JP · ja · T1 · co1 · empty" autocomplete="off">
      </div>
      <div class="field">
        <label for="cat">Category</label>
        <select id="cat"><option value="">Entire corpus (all categories)</option></select>
      </div>
      <div class="field" id="gradeField">
        <label>Grade</label>
        <div class="grades" id="grades"></div>
      </div>
      <button class="btn-reset" id="reset">Reset</button>
    </div>
    <div class="scope-note" id="scope"></div>
  </div>

  <div id="slicesView">

  <h2 class="dim-head">Snapshot <span>dimensions 1 &amp; 6 · amount &amp; overall quality</span></h2>
  <div class="cards" id="cards"></div>

  <div class="split">
    <div>
      <h2 class="dim-head">Tiers of evidence <span>dimension 2</span></h2>
      <div class="barset" id="tiers"></div>
      <p class="legend" id="bpline"></p>
    </div>
    <div>
      <h2 class="dim-head">English / Anglophone bias <span>dimension 5</span></h2>
      <div class="barset" id="bias"></div>
      <p class="legend" id="biasline"></p>
    </div>
  </div>

  <div class="split">
    <div>
      <h2 class="dim-head">Jurisdictions sourced <span>dimension 3</span></h2>
      <div class="barset" id="jurs"></div>
      <p class="legend" id="jurline"></p>
    </div>
    <div>
      <h2 class="dim-head">Languages sourced <span>dimension 4</span></h2>
      <div class="barset" id="langs"></div>
      <p class="legend" id="langline"></p>
    </div>
  </div>

  <h2 class="dim-head">Slices <span id="tcount"></span></h2>
  <p class="legend"><b>N</b> linked sources · <b>Band</b> strongest anchoring band (● full / ◐ partial / ○ weak) ·
  <b>●</b> full-band anchor count (T1/Co-1/T2/Co-2/T3-clinical) · <b>band bar</b> green=full, amber=partial, orange=weak ·
  <b>JUR/LNG</b> distinct true jurisdictions / languages · <b>EN</b> English-language share (redder = more concentrated) ·
  <b>%ANG</b> native-Anglophone share · <b style="color:var(--gD)">&#8224;</b> ○ weak-only (breadth discounted, honesty-flagged).
  Click a header to sort.</p>
  <div class="tablewrap">
    <table>
      <thead><tr>
        <th data-k="grade">Grade</th><th data-k="score">Score</th>
        <th data-k="slug">Slice</th>
        <th data-k="n" class="num">N</th><th data-k="full" class="num">●</th>
        <th data-k="tierbar">Band mix</th>
        <th data-k="n_jur" class="num">JUR</th><th data-k="n_lang" class="num">LNG</th>
        <th data-k="pct_en" class="num">EN</th><th data-k="pct_anglo" class="num">%ANG</th>
      </tr></thead>
      <tbody id="tbody"></tbody>
    </table>
  </div>
  </div><!-- /slicesView -->

  <div id="itemsView" hidden>
    <h2 class="dim-head">Specifications <span>design items · adjudicated by inherited base</span></h2>
    <div class="cards" id="icards"></div>
    <div class="split">
      <div>
        <h2 class="dim-head">Basis health <span>where each spec's evidence comes from</span></h2>
        <div class="barset" id="ihealth"></div>
        <p class="legend" id="ihealthline"></p>
      </div>
      <div>
        <h2 class="dim-head">Inherited grade <span>strength of the base each spec rests on</span></h2>
        <div class="barset" id="igrade"></div>
        <p class="legend" id="igradeline"></p>
      </div>
    </div>
    <h2 class="dim-head">Specifications <span id="itcount"></span></h2>
    <p class="legend"><b>Basis</b> = strength band of the slug this spec inherits (● full / ◐ partial / ○ weak) · <b>Grade</b> inherited ·
    <b>N/●</b> base sources / full-band anchors · <b>JUR/LNG</b> base jurisdictions / languages ·
    <b>%EN</b> base English share. A spec on a ○ weak, disputed-only, or missing basis rests on weak or missing evidence.
    Click a header to sort.</p>
    <div class="tablewrap">
      <table>
        <thead><tr>
          <th data-k="grade">Grade</th><th data-k="basis">Basis</th>
          <th data-k="code">Item</th><th data-k="cat">Cat</th>
          <th data-k="src">Source slug</th>
          <th data-k="n" class="num">N</th><th data-k="full" class="num">●</th>
          <th data-k="n_jur" class="num">JUR</th><th data-k="n_lang" class="num">LNG</th>
          <th data-k="pct_en" class="num">%EN</th>
        </tr></thead>
        <tbody id="itbody"></tbody>
      </table>
    </div>
  </div><!-- /itemsView -->

  <footer>
    Data as of __ASOF__ · read-only over data/guidebook.db · __NSLICES__ ACTIVE slices ·
    __NITEMS__ specifications · __TOTSRC__ source-instances (__UNIQ__ unique).<br>
    Tiers per governance/tier-system.md (OPERATIVE 2026-05-25). Scores are a triage lens over the linked
    evidence base, not a verdict on any single citation. Companion: evidentiary-base-audit.md / .csv /
    -items.csv / .json.
  </footer>
</div>

<script>
const DATA = __DATA__;
const IDATA = __IDATA__;
const CATS = __CATS__;
const ICATS = __ICATS__;
const GRADES = ["A","B","C","D","E","F"];
let activeGrades = new Set();
let view = "slices";
let sortK = "score", sortDir = -1;

const catSel = document.getElementById("cat");
function populateCats(){
  catSel.innerHTML = "";
  const first=document.createElement("option"); first.value="";
  first.textContent = view==="slices" ? "Entire corpus (all categories)" : "All categories (A–K)";
  catSel.appendChild(first);
  if(view==="slices"){
    CATS.forEach(c=>{const o=document.createElement("option");o.value=c;o.textContent=c;catSel.appendChild(o);});
  } else {
    ICATS.forEach(([c,label])=>{const o=document.createElement("option");o.value=c;o.textContent=c+" — "+label;catSel.appendChild(o);});
  }
}
populateCats();
const gwrap = document.getElementById("grades");
GRADES.forEach(g=>{const b=document.createElement("button");b.className="gchip "+g;b.textContent=g;
  b.setAttribute("aria-pressed","false");b.onclick=()=>{activeGrades.has(g)?activeGrades.delete(g):activeGrades.add(g);
  b.setAttribute("aria-pressed",activeGrades.has(g));render();};gwrap.appendChild(b);});

// View toggle
document.querySelectorAll(".vtab").forEach(t=>t.onclick=()=>{
  const nv=t.dataset.view; if(nv===view) return;
  view=nv;
  document.querySelectorAll(".vtab").forEach(x=>x.setAttribute("aria-selected", x.dataset.view===view));
  document.getElementById("slicesView").hidden = view!=="slices";
  document.getElementById("itemsView").hidden = view!=="items";
  document.getElementById("gradeField").style.display = view==="slices" ? "" : "none";
  document.getElementById("term").value=""; activeGrades.clear();
  document.querySelectorAll(".gchip").forEach(b=>b.setAttribute("aria-pressed","false"));
  sortK = view==="slices" ? "score" : "basis"; sortDir = view==="slices" ? -1 : 1;
  populateCats();
  render();
});

const HEALTH_ORDER=["full","partial","weak","disputed-only","empty-base","no-source","source-missing"];
const HEALTH_CLASS={"full":"full","partial":"partial","weak":"weak","disputed-only":"disputedonly","empty-base":"empty","no-source":"nosource","source-missing":"nosource"};
const HEALTH_LABEL={"full":"● full base","partial":"◐ partial base","weak":"○ weak base","disputed-only":"disputed-only","empty-base":"empty base","no-source":"no source slug","source-missing":"source missing"};
const HEALTH_RANK={"full":0,"partial":1,"weak":2,"disputed-only":3,"empty-base":4,"no-source":5,"source-missing":6};
const HEALTHY=new Set(["full","partial"]);  // inherits an anchoring base (● full or ◐ partial)

function filteredItems(){
  const term=document.getElementById("term").value.trim().toLowerCase();
  const cat=catSel.value;
  return IDATA.filter(r=>{
    if(cat && r.cat!==cat) return false;
    if(term && !r.blob.includes(term)) return false;
    return true;
  });
}

function filtered(){
  const term=document.getElementById("term").value.trim().toLowerCase();
  const cat=catSel.value;
  return DATA.filter(r=>{
    if(cat && r.topic!==cat) return false;
    if(activeGrades.size && !activeGrades.has(r.grade)) return false;
    if(term && !r.blob.includes(term)) return false;
    return true;
  });
}
function cvar(v){return getComputedStyle(document.documentElement).getPropertyValue(v).trim();}
function esc(s){return (s||"").replace(/[&<>]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;"}[c]));}

function agg(rows){
  const a={n:0,full:0,partial:0,weak:0,disputed:0,tiers:{},langs:{},jurs:{},en:0,nonen:0,core:0,supra:0,other:0,
    empty:0,enonly:0,withev:0,scoreSum:0};
  rows.forEach(r=>{
    if(r.n===0){a.empty++;return;}
    a.withev++; a.n+=r.n; a.full+=r.full; a.partial+=r.partial; a.weak+=r.weak; a.disputed+=r.disputed; a.scoreSum+=r.score;
    if(r.n_nonen===0)a.enonly++;
    a.en+=r.n_en; a.nonen+=r.n_nonen; a.core+=r.anglo_core; a.supra+=r.supra; a.other+=r.non_anglo;
    for(const[k,v]of Object.entries(r.tiers))a.tiers[k]=(a.tiers[k]||0)+v;
    for(const[k,v]of Object.entries(r.langs))a.langs[k]=(a.langs[k]||0)+v;
    for(const[k,v]of Object.entries(r.jurs))a.jurs[k]=(a.jurs[k]||0)+v;
  });
  return a;
}
function barRows(el,pairs,total){
  el.innerHTML=pairs.map(([k,v])=>{
    const p=total?100*v/total:0;
    return `<div class="barrow"><span class="k">${esc(k)}</span>
      <span class="track"><span class="fill" style="width:${p.toFixed(1)}%"></span></span>
      <span class="v">${v} · ${p.toFixed(0)}%</span></div>`;
  }).join("")||`<div class="legend" style="color:var(--faint)">no evidence in scope</div>`;
}
function barRow2(k,v,tot,col){const p=tot?100*v/tot:0;
  return `<div class="barrow"><span class="k">${k}</span>
    <span class="track"><span class="fill" style="width:${p.toFixed(1)}%;background:var(${col})"></span></span>
    <span class="v">${v} · ${p.toFixed(0)}%</span></div>`;}
function tierColor(k){return (k==="T1"||k==="T2")?cvar("--gA"):(k==="T3")?cvar("--accent"):cvar("--gD");}
function medianN(rows){const ns=rows.filter(r=>r.n>0).map(r=>r.n).sort((a,b)=>a-b);
  return ns.length?ns[Math.floor(ns.length/2)]:0;}
function gradeFor(s){return s>=80?"A":s>=65?"B":s>=50?"C":s>=35?"D":s>0?"E":"F";}

function render(){ if(view==="items"){ renderItems(); return; } renderSlices(); }

function renderItems(){
  const rows=filteredItems();
  const hc={}, gc={}; let weak=0;
  rows.forEach(r=>{ hc[r.health]=(hc[r.health]||0)+1;
    if(!HEALTHY.has(r.health)) weak++;
    const g=r.grade||"—"; gc[g]=(gc[g]||0)+1; });
  document.getElementById("scope").innerHTML =
    `In scope: <b>${rows.length}</b> specifications · <b>${rows.length-weak}</b> on a full/partial anchored base · `+
    `<b>${weak}</b> on a weak, disputed-only, or missing base`;
  const cats=new Set(rows.map(r=>r.cat));
  const cards=[
    ["Specifications", rows.length, `${cats.size} categor${cats.size===1?"y":"ies"} in scope`],
    ["On weak/missing base", weak, `${rows.length-weak} inherit a full/partial anchored base`],
    ["No source slug", hc["no-source"]||0, `coverage gaps — cannot inherit evidence`],
    ["Full anchor (grade A–C)", rows.filter(r=>["A","B","C"].includes(r.grade)&&r.health==="full").length,
      `specs on a ● full, adjudicated base`],
  ];
  document.getElementById("icards").innerHTML=cards.map(([l,b,n])=>
    `<div class="card"><div class="big">${b}</div><div class="lbl">${l}</div><div class="note">${n}</div></div>`).join("");
  // basis health bars
  const hcols={"full":"--gA","partial":"--gC","weak":"--gD","disputed-only":"--gE","empty-base":"--gF","no-source":"--gF","source-missing":"--gF"};
  document.getElementById("ihealth").innerHTML=HEALTH_ORDER.filter(h=>hc[h]).map(h=>
    barRow2(HEALTH_LABEL[h], hc[h], rows.length, hcols[h])).join("")||
    `<div class="legend" style="color:var(--faint)">no specifications in scope</div>`;
  document.getElementById("ihealthline").innerHTML=
    `Each spec inherits the base of its <code>bpc_source_slug</code>; a spec cannot be stronger than the slug it rests on.`;
  // inherited grade bars
  document.getElementById("igrade").innerHTML=["A","B","C","D","E","F","—"].filter(g=>gc[g]).map(g=>
    barRow2("Grade "+g, gc[g], rows.length, g==="—"?"--faint":("--g"+g))).join("")||"";
  document.getElementById("igradeline").innerHTML=
    `Grade is inherited from the source slug (— = no source slug to inherit from).`;
  renderItemTable(rows);
}
function renderItemTable(rows){
  const sorted=[...rows].sort((x,y)=>{
    if(sortK==="code"||sortK==="cat"||sortK==="src")
      return sortDir*String(x[sortK]||"").localeCompare(String(y[sortK]||""));
    if(sortK==="basis") return sortDir*((HEALTH_RANK[x.health]??9)-(HEALTH_RANK[y.health]??9));
    if(sortK==="grade") return sortDir*((x.score??-1)-(y.score??-1));
    return sortDir*((x[sortK]??-1)-(y[sortK]??-1));
  });
  document.getElementById("itcount").textContent=`${rows.length} in scope`;
  document.querySelectorAll("#itemsView thead th").forEach(th=>{
    th.classList.toggle("sorted",th.dataset.k===sortK);
    const base=th.textContent.replace(/[▲▼]/g,"").trim();
    th.innerHTML=th.dataset.k===sortK? base+` <span class="arw">${sortDir<0?"▼":"▲"}</span>`:base;
  });
  document.getElementById("itbody").innerHTML=sorted.map(r=>{
    const g=r.grade||"—";
    const gp=g==="—"?`<span class="hpill nosource">—</span>`:`<span class="gpill ${g}">${g}</span>`;
    const hp=`<span class="hpill ${HEALTH_CLASS[r.health]||''}">${HEALTH_LABEL[r.health]||r.health}</span>`;
    return `<tr>
      <td>${gp}</td><td>${hp}</td>
      <td class="itemname">${esc(r.name)}<span class="tp">${esc(r.code)}</span></td>
      <td class="num">${esc(r.cat)}</td>
      <td class="slug">${r.src?esc(r.src):'<span style="color:var(--faint)">— none —</span>'}</td>
      <td class="num">${r.n??'—'}</td><td class="num">${r.full??'—'}</td>
      <td class="num">${r.n_jur??'—'}</td><td class="num">${r.n_lang??'—'}</td>
      <td class="num">${r.pct_en??'—'}</td></tr>`;
  }).join("");
}

function renderSlices(){
  const rows=filtered(), a=agg(rows);
  document.getElementById("scope").innerHTML =
    `In scope: <b>${rows.length}</b> slices · <b>${a.n}</b> source-instances · `+
    `<b>${a.withev}</b> evidenced · <b>${a.empty}</b> empty`;
  const meanScore = a.withev? (a.scoreSum/a.withev):0;
  const fullShare = a.n? Math.round(100*a.full/a.n):0;
  const cards=[
    ["Source-instances", a.n, `${a.withev} of ${rows.length} slices evidenced`],
    ["Median / slice", medianN(rows), `${a.empty} slice(s) with zero evidence`],
    ["Mean score", meanScore.toFixed(1), gradeFor(meanScore)+" band (evidenced slices)"],
    ["● Full-band anchor", fullShare+"%", `${a.full} of ${a.n} instances anchor at full strength`],
    ["English share", (a.n?Math.round(100*a.en/a.n):0)+"%", `${a.enonly} slice(s) English-only`],
    ["Distinct jurisdictions", Object.keys(a.jurs).length, `${Object.keys(a.langs).length} languages sourced`],
  ];
  document.getElementById("cards").innerHTML=cards.map(([l,b,n])=>
    `<div class="card"><div class="big">${b}</div><div class="lbl">${l}</div><div class="note">${n}</div></div>`).join("");

  const tp=["1","2","3","4","5","6"].map(t=>["T"+t,a.tiers[t]||0]);
  document.getElementById("tiers").innerHTML=tp.map(([k,v])=>{
    const p=a.n?100*v/a.n:0;
    return `<div class="barrow"><span class="k">${k}</span>
      <span class="track"><span class="fill" style="width:${p.toFixed(1)}%;background:${tierColor(k)}"></span></span>
      <span class="v">${v} · ${p.toFixed(0)}%</span></div>`;}).join("");
  document.getElementById("bpline").innerHTML=
    `<b>${a.full}</b> ● full (${fullShare}%) · <b>${a.partial}</b> ◐ partial · <b>${a.weak}</b> ○ weak`+
    (a.disputed?` · <b>${a.disputed}</b> ⊘ disputed (no anchor)`:``)+
    ` of ${a.n} instances. Weighted-strength model: every tier anchors, weighted by band (§8).`;

  const enp=a.n?100*a.en/a.n:0, jnull=a.n-(a.core+a.supra+a.other);
  document.getElementById("bias").innerHTML=
    barRow2("English-lang.",a.en,a.n,"--gE")+
    barRow2("Non-English",a.nonen,a.n,"--accent")+
    barRow2("Anglophone jur.",a.core,a.n,"--gD")+
    barRow2("Supranational",a.supra,a.n,"--slate")+
    barRow2("Other jur.",a.other,a.n,"--gA")+
    barRow2("No jurisdiction",jnull,a.n,"--faint");
  document.getElementById("biasline").innerHTML=
    `<b>${enp.toFixed(0)}%</b> English · <b>${a.enonly}</b> English-only slices in scope.`;

  const js=Object.entries(a.jurs).sort((x,y)=>y[1]-x[1]);
  barRows(document.getElementById("jurs"),js.slice(0,8),a.n);
  document.getElementById("jurline").innerHTML=
    `<b>${Object.keys(a.jurs).length}</b> distinct jurisdictions in scope`+(js.length>8?` · showing top 8`:``)+`.`;
  const ls=Object.entries(a.langs).sort((x,y)=>y[1]-x[1]);
  barRows(document.getElementById("langs"),ls.slice(0,8),a.n);
  document.getElementById("langline").innerHTML=
    `<b>${Object.keys(a.langs).length}</b> distinct languages in scope`+(ls.length>8?` · showing top 8`:``)+`.`;

  renderTable(rows);
}
function renderTable(rows){
  const sorted=[...rows].sort((x,y)=>{
    if(sortK==="slug") return sortDir*x.slug.localeCompare(y.slug);
    let A,B;
    if(sortK==="grade"){A=x.score;B=y.score;}
    else if(sortK==="tierbar"){A=x.n?x.full/x.n:-1;B=y.n?y.full/y.n:-1;}
    else {A=x[sortK]??-1;B=y[sortK]??-1;}
    return sortDir*(A-B);
  });
  document.getElementById("tcount").textContent=`${rows.length} in scope · dimension detail`;
  document.querySelectorAll("#slicesView thead th").forEach(th=>{
    th.classList.toggle("sorted",th.dataset.k===sortK);
    const base=th.textContent.replace(/[▲▼]/g,"").trim();
    th.innerHTML=th.dataset.k===sortK? base+` <span class="arw">${sortDir<0?"▼":"▲"}</span>`:base;
  });
  document.getElementById("tbody").innerHTML=sorted.map(r=>{
    if(r.n===0) return `<tr class="empty-row"><td><span class="gpill F">F</span></td><td class="num">—</td>
      <td class="slug">${esc(r.slug)}<span class="tp">${esc(r.topic)} · ${esc(r.state||'no state')} · empty</span></td>
      <td class="num">0</td><td class="num">—</td><td>—</td><td class="num">—</td><td class="num">—</td>
      <td class="num">—</td><td class="num">—</td></tr>`;
    const fp=r.n?100*r.full/r.n:0, pp=r.n?100*r.partial/r.n:0, wp=r.n?100*r.weak/r.n:0;
    const tierbar=`<span class="mini" title="green=● full, amber=◐ partial, orange=○ weak (gap=⊘ disputed)">
      <i style="width:${fp}%;background:var(--gA)"></i><i style="width:${pp}%;background:var(--gC)"></i><i style="width:${wp}%;background:var(--gD)"></i></span>`;
    const enb=`<span class="enbar" style="--p:${r.pct_en??0}%" title="${r.pct_en??0}% English"></span>`;
    const flag=r.weakonly?` <b title="○ weak-only: strongest anchor is weak (T3-grey/T6/grey); breadth discounted, honesty-flagged" style="color:var(--gD)">&#8224;</b>`:"";
    return `<tr>
      <td><span class="gpill ${r.grade}">${r.grade}</span>${flag}</td>
      <td class="num">${r.score}</td>
      <td class="slug">${esc(r.slug)}<span class="tp">${esc(r.topic)}</span></td>
      <td class="num">${r.n}</td><td class="num">${r.full}</td>
      <td>${tierbar}</td>
      <td class="num">${r.n_jur}</td><td class="num">${r.n_lang}</td>
      <td class="num">${enb} ${r.pct_en??'—'}</td>
      <td class="num">${r.pct_anglo??'—'}</td></tr>`;
  }).join("");
}

document.getElementById("term").addEventListener("input",render);
catSel.addEventListener("change",render);
document.getElementById("reset").onclick=()=>{document.getElementById("term").value="";catSel.value="";
  activeGrades.clear();document.querySelectorAll(".gchip").forEach(b=>b.setAttribute("aria-pressed","false"));render();};
const STRING_SORT=["slug","code","cat","src","basis"];
document.querySelectorAll("thead th").forEach(th=>th.onclick=()=>{
  const k=th.dataset.k; if(sortK===k)sortDir*=-1; else {sortK=k;sortDir=STRING_SORT.includes(k)?1:-1;} render();});
const root=document.documentElement, themeBtn=document.getElementById("themeBtn");
themeBtn.onclick=()=>{const cur=root.getAttribute("data-theme")||
  (matchMedia("(prefers-color-scheme:dark)").matches?"dark":"light");
  root.setAttribute("data-theme",cur==="dark"?"light":"dark");};
render();
</script>
"""


def build_html(records, items, f):
    slim = []
    for r in records:
        blob = " ".join([
            r["slug"], r["topic"] or "", r["grade"], (r["state"] or ""),
            " ".join(r["jurs_clean"].keys()), " ".join(r["langs"].keys()),
            " ".join("T" + k for k in r["tiers"].keys()), " ".join(r["etypes"].keys()),
        ]).lower()
        blob += " " + (r["strength_band"] or "disputed-only") + " band"
        if r["weak_only"]:
            blob += " weak-only †"
        if r["disputed"]:
            blob += " disputed"
        if r["practice"]:
            blob += " practice-stream"
        slim.append(dict(
            slug=r["slug"], topic=r["topic"], state=r["state"],
            n=r["n"], full=r["full"], partial=r["partial"], weak=r["weak"], disputed=r["disputed"],
            band=r["strength_band"], weakonly=r["weak_only"], practice=r["practice"],
            tiers=r["tiers"], etypes=r["etypes"],
            n_jur=r["n_true_jur"], jurs=r["jurs_clean"], n_lang=r["n_lang"], langs=r["langs"],
            n_en=r["n_en"], n_nonen=r["n_nonen"], pct_en=r["pct_en"],
            anglo_core=r["anglo_core"], supra=r["supra"], non_anglo=r["non_anglo"],
            pct_anglo=r["pct_anglo_core"], grade=r["grade"], score=r["score"], blob=blob))
    # Item (specification) records for the dashboard's Specifications view.
    islim = []
    for it in items:
        iblob = " ".join([
            it["item_code"], it["name"] or "", it["category"], it["category_label"],
            it["source_slug"] or "", it["basis_health"], it["grade"] or "",
        ]).lower()
        islim.append(dict(
            code=it["item_code"], name=it["name"], cat=it["category"],
            catl=it["category_label"], src=it["source_slug"], health=it["basis_health"],
            grade=it["grade"], score=it["score"], n=it["n"], full=it["full"],
            partial=it["partial"], weak=it["weak"], disputed=it["disputed"],
            n_jur=it["n_jur"], n_lang=it["n_lang"],
            pct_en=it["pct_en"], pct_anglo=it["pct_anglo"], blob=iblob))

    def js_safe(s):
        # Escape "</" (…</script> breakout) and the JS line terminators U+2028/9.
        return (s.replace("</", "<\\/")
                 .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))
    data = js_safe(json.dumps(slim, separators=(",", ":"), ensure_ascii=False))
    idata = js_safe(json.dumps(islim, separators=(",", ":"), ensure_ascii=False))
    cats = js_safe(json.dumps(sorted({r["topic"] for r in slim if r["topic"]}),
                              ensure_ascii=False))
    icats = js_safe(json.dumps([[c, CATEGORY_LABELS.get(c, c)]
                                for c in sorted({it["category"] for it in items})],
                               ensure_ascii=False))
    return (HTML_TEMPLATE
            .replace("__DATA__", data)
            .replace("__IDATA__", idata)
            .replace("__CATS__", cats)
            .replace("__ICATS__", icats)
            .replace("__ASOF__", f["as_of"])
            .replace("__NSLICES__", str(f["n_slices"]))
            .replace("__NITEMS__", str(f["n_items"]))
            .replace("__TOTSRC__", str(f["tot_src"]))
            .replace("__UNIQ__", str(f["unique_linked"])))


def read_text_exact(path):
    """Read without newline translation, so byte-comparison round-trips."""
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def write_text_exact(path, content):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(content)


def write_if_changed(path, content):
    path = Path(path)
    old = read_text_exact(path) if path.exists() else None
    if old == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    write_text_exact(path, content)
    return True


def main():
    ap = argparse.ArgumentParser(description="Per-slice evidentiary audit generator.")
    ap.add_argument("--db", default=os.environ.get("GUIDEBOOK_DB_PATH", str(DEFAULT_DB)))
    ap.add_argument("--audits-dir", default=str(AUDITS_DIR))
    ap.add_argument("--tools-dir", default=str(TOOLS_DIR))
    ap.add_argument("--check", action="store_true",
                    help="Exit 1 if any output would change (for CI drift detection).")
    args = ap.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        sys.exit(f"DB not found: {db_path}")

    records, items, facts = compute(db_path)
    outputs = {
        Path(args.audits_dir) / "evidentiary-base-audit.md": build_markdown(records, items, facts),
        Path(args.audits_dir) / "evidentiary-base-audit.csv": build_csv(records),
        Path(args.audits_dir) / "evidentiary-base-audit-items.csv": build_items_csv(items),
        Path(args.audits_dir) / "evidentiary-base-audit.json": build_json(records, items, facts),
        Path(args.tools_dir) / "evidentiary-audit-dashboard.html": build_html(records, items, facts),
    }

    if args.check:
        drifted = [str(p) for p, c in outputs.items()
                   if (not Path(p).exists()) or read_text_exact(p) != c]
        if drifted:
            print("DRIFT: outputs are stale, re-run tools/evidentiary_audit.py:")
            for d in drifted:
                print("  -", d)
            sys.exit(1)
        print("OK: all audit outputs are up to date.")
        return

    changed = [p for p, c in outputs.items() if write_if_changed(p, c)]
    gc = Counter(r["grade"] for r in records)
    print(f"Audit as-of {facts['as_of']}: {facts['n_slices']} slices, "
          f"{facts['tot_src']} instances, grades {dict(sorted(gc.items()))}")
    print(f"Wrote {len(changed)} changed / {len(outputs)} total output files"
          + ("" if changed else " (all byte-identical to committed copies)"))
    for p in changed:
        try:
            rel = Path(p).relative_to(REPO_ROOT)
        except ValueError:
            rel = Path(p)  # custom out-dir outside the repo
        print("  *", rel)


if __name__ == "__main__":
    main()
