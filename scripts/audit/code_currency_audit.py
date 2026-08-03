#!/usr/bin/env python3
"""
Code-currency audit for Tier 4–6 evidence_sources.

Per governance/tier-system.md §4: when a BPC cites a T4–T6 source, the citation
must confirm that the cited edition is the current legally-in-force edition.
The metadata-quality gate verifies the row parses; this audit verifies the
*edition* is current.

Lessons recorded 2026-05-25:
- NZS 4121:2001 — speculated as superseded from age alone; web verification
  confirmed it remains the NZ Building Act §119 / D1/AS1 Acceptable Solution.
  Age does NOT predict supersession.
- DIN 18040-1:2010 — still legally in force per MVV TB 2024/1 (German Model
  Administrative Regulation Technical Building Regulations 2024/1, published
  August 2024), but supersedable by DIN EN 17210:2021 (European harmonised
  standard) and E DIN 18040-1:2023 (German draft revision). Older citations
  still legal but may not reflect current evidence.

The audit fires per-tier age thresholds and lists rows for jurisdiction-tracker
review. Suppression criteria:
1. code_currency_status IN ('VERIFIED-CURRENT','PERMANENT-FRAMEWORK') AND
   code_currency_verified_at within last 365 days
2. supersession_check row with outcome IN ('current_best','co1_addition_logged',
   'refined_by') within last 365 days (any slug)
3. pub_year within tier-specific freshness threshold (T4: 7 years; T5/T6: 5 years)

Run before each session close on slugs that cite T4–T6 sources. Promotion to
Level 3 (CI-warning) deferred per architecture v2.3 enforcement-spectrum
demotion/promotion path — first 6 months at Level 2 to calibrate thresholds.
"""
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
DB = Path(__import__("os").environ.get("GUIDEBOOK_DB_PATH", str(REPO / "data" / "guidebook.db")))

# Tier-specific freshness thresholds (years).
# T4 international standards revise on ~7-10 year cycles (EN/ISO/IEC).
# T5 national frameworks revise on ~5-7 year cycles.
# T6 statutory codes vary wildly (ADA 15+ years stable; NZBC frequent revisions).
# Threshold chosen as "review-trigger age", not "presumed-stale age".
THRESHOLDS = {4: 7, 5: 5, 6: 5}

# Valid code_currency_status enum (enforced at audit level — DB CHECK
# constraint requires SQLite table-rebuild).
VALID_STATUS = {
    None,
    "VERIFIED-CURRENT",
    "PERMANENT-FRAMEWORK",
    "SUPERSEDED-PENDING-REPLACEMENT",
    "UNVERIFIED-CHECK-DEFERRED",
}


def audit():
    db = sqlite3.connect(str(DB))
    db.row_factory = sqlite3.Row
    issues = []
    now_year = datetime.now(timezone.utc).year
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    cutoff_365 = datetime.now(timezone.utc).strftime("%Y-%m-%d")  # used as ISO compare baseline

    print(f"code_currency_audit.py — run {today}")
    print(f"  DB: {DB}")
    print(f"  current year for age calc: {now_year}")
    print(f"  tier thresholds (years): T4={THRESHOLDS[4]}, T5={THRESHOLDS[5]}, T6={THRESHOLDS[6]}")
    print(f"  365-day suppression cutoff: rows with code_currency_verified_at OR")
    print(f"    supersession_check.checked_at >= today minus 365 days suppressed")
    print()
    print("=" * 70)

    # ────────────────────────────────────────────────────────────────────
    # CHECK 1: enum validation on code_currency_status
    # ────────────────────────────────────────────────────────────────────
    bad_status = db.execute("""
        SELECT ref_id, code_currency_status FROM evidence_sources
         WHERE code_currency_status IS NOT NULL
           AND code_currency_status NOT IN
               ('VERIFIED-CURRENT','PERMANENT-FRAMEWORK',
                'SUPERSEDED-PENDING-REPLACEMENT','UNVERIFIED-CHECK-DEFERRED')
    """).fetchall()
    print(f"\n[CHECK 1] code_currency_status enum validity: {len(bad_status)} invalid")
    for r in bad_status[:5]:
        print(f"  ✗ {r['ref_id']}: status='{r['code_currency_status']}'")
    if bad_status:
        issues.append(("CHECK 1", len(bad_status), "invalid code_currency_status values"))

    # ────────────────────────────────────────────────────────────────────
    # CHECK 2: T4–T6 cited rows older than tier threshold, not currency-verified
    # ────────────────────────────────────────────────────────────────────
    # A row needs currency review if:
    #   - tier IN (4,5,6) AND in source_slug_links AND pub_year < (now - threshold)
    #   AND NOT (code_currency_status='VERIFIED-CURRENT' or 'PERMANENT-FRAMEWORK'
    #            AND code_currency_verified_at >= today-365 days)
    #   AND NOT (supersession_check.checked_at >= today-365 days AND outcome in current_best set)
    suppression_sql = """
        (es.code_currency_status IN ('VERIFIED-CURRENT','PERMANENT-FRAMEWORK')
         AND es.code_currency_verified_at IS NOT NULL
         AND es.code_currency_verified_at >= date('now','-365 days'))
        OR
        EXISTS (
            SELECT 1 FROM supersession_check sc
             WHERE sc.ref_id = es.ref_id
               AND sc.outcome IN ('current_best','co1_addition_logged','refined_by')
               AND sc.checked_at >= date('now','-365 days')
        )
    """
    flagged_query = f"""
        SELECT es.ref_id, es.tier, es.pub_year, es.jurisdiction,
               es.first_author_last, es.pub_title, es.code_currency_status,
               es.code_currency_verified_at,
               (SELECT GROUP_CONCAT(ssl.slug)
                  FROM (SELECT DISTINCT slug FROM source_slug_links WHERE ref_id = es.ref_id) ssl) as slugs
          FROM evidence_sources es
         WHERE es.tier IN (4, 5, 6)
           AND es.pub_year IS NOT NULL
           AND es.pub_year < CASE es.tier
                              WHEN 4 THEN {now_year - THRESHOLDS[4]}
                              WHEN 5 THEN {now_year - THRESHOLDS[5]}
                              WHEN 6 THEN {now_year - THRESHOLDS[6]}
                             END
           AND EXISTS (SELECT 1 FROM source_slug_links ssl WHERE ssl.ref_id = es.ref_id)
           AND NOT ({suppression_sql})
         ORDER BY es.tier, es.pub_year, es.jurisdiction
    """
    flagged = db.execute(flagged_query).fetchall()
    print(f"\n[CHECK 2] T4–T6 cited rows past freshness threshold, not currency-verified: "
          f"{len(flagged)}")
    if flagged:
        # Group by tier × jurisdiction for compact triage output
        by_tier = {}
        for r in flagged:
            by_tier.setdefault(r["tier"], []).append(r)
        for tier in sorted(by_tier):
            print(f"\n  Tier {tier} ({len(by_tier[tier])} rows):")
            for r in by_tier[tier][:15]:
                age = now_year - r["pub_year"]
                title = (r["pub_title"] or "")[:60]
                slugs = (r["slugs"] or "")[:50]
                print(f"    age={age:2d}y {r['ref_id']} {r['jurisdiction'] or '?':4s} "
                      f"{r['first_author_last'] or '?':25s} {r['pub_year']}")
                print(f"      title: {title}")
                if slugs:
                    print(f"      slugs: {slugs}")
            if len(by_tier[tier]) > 15:
                print(f"    ... and {len(by_tier[tier]) - 15} more")
        issues.append(("CHECK 2", len(flagged), "rows need code-currency review"))

    # ────────────────────────────────────────────────────────────────────
    # CHECK 3: T4–T6 rows explicitly marked SUPERSEDED-PENDING-REPLACEMENT
    # ────────────────────────────────────────────────────────────────────
    superseded = db.execute("""
        SELECT ref_id, tier, pub_year, jurisdiction, first_author_last, pub_title,
               code_currency_notes
          FROM evidence_sources
         WHERE code_currency_status = 'SUPERSEDED-PENDING-REPLACEMENT'
    """).fetchall()
    print(f"\n[CHECK 3] Rows explicitly marked SUPERSEDED-PENDING-REPLACEMENT: {len(superseded)}")
    for r in superseded[:10]:
        title = (r["pub_title"] or "")[:55]
        print(f"  ⚠ T{r['tier']} {r['ref_id']} {r['jurisdiction']} {r['first_author_last']} "
              f"{r['pub_year']} — {title}")
        if r["code_currency_notes"]:
            print(f"      note: {r['code_currency_notes'][:80]}")
    if superseded:
        issues.append(("CHECK 3", len(superseded), "rows pending replacement"))

    # ────────────────────────────────────────────────────────────────────
    # CHECK 4: code_currency_verified_at present but no status
    # ────────────────────────────────────────────────────────────────────
    orphan_verified = db.execute("""
        SELECT ref_id, code_currency_verified_at FROM evidence_sources
         WHERE code_currency_verified_at IS NOT NULL
           AND code_currency_status IS NULL
    """).fetchall()
    print(f"\n[CHECK 4] code_currency_verified_at set but code_currency_status NULL: "
          f"{len(orphan_verified)}")
    for r in orphan_verified[:5]:
        print(f"  ✗ {r['ref_id']}: verified_at={r['code_currency_verified_at']} but status=NULL")
    if orphan_verified:
        issues.append(("CHECK 4", len(orphan_verified), "verified_at without status"))

    # ────────────────────────────────────────────────────────────────────
    # CHECK 5: VERIFIED-CURRENT older than 365 days (re-verification overdue)
    # ────────────────────────────────────────────────────────────────────
    overdue = db.execute("""
        SELECT ref_id, code_currency_verified_at, first_author_last, pub_year, pub_title
          FROM evidence_sources
         WHERE code_currency_status = 'VERIFIED-CURRENT'
           AND code_currency_verified_at IS NOT NULL
           AND code_currency_verified_at < date('now','-365 days')
    """).fetchall()
    print(f"\n[CHECK 5] VERIFIED-CURRENT rows overdue for re-verification (>365 days): "
          f"{len(overdue)}")
    for r in overdue[:10]:
        print(f"  ⚠ {r['ref_id']} verified {r['code_currency_verified_at']} — re-check due")
    if overdue:
        issues.append(("CHECK 5", len(overdue), "VERIFIED-CURRENT re-verification overdue"))

    # ────────────────────────────────────────────────────────────────────
    # Summary
    # ────────────────────────────────────────────────────────────────────
    print("\n" + "=" * 70)
    total_issues = sum(n for _, n, _ in issues)
    print(f"TOTAL ISSUES: {total_issues}")
    if issues:
        for check, n, desc in issues:
            print(f"  {check}: {n} {desc}")
        print()
        print("Reminder: this audit creates a triage queue, not a verdict.")
        print("Tier 6 statutory codes commonly persist 15+ years and remain current")
        print("(NZS 4121:2001 is a documented worked example). Old age does not predict")
        print("supersession either way — each flagged row requires direct jurisdiction-")
        print("source check. Mark resolved rows with code_currency_status =")
        print("VERIFIED-CURRENT (with verified_at), PERMANENT-FRAMEWORK, or")
        print("SUPERSEDED-PENDING-REPLACEMENT to suppress future audit fires.")
        return 1
    else:
        print("Audit clean. All cited T4–T6 rows within freshness thresholds OR")
        print("explicitly currency-verified within the last 365 days.")
        return 0


if __name__ == "__main__":
    sys.exit(audit())
