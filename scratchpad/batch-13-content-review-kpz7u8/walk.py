#!/usr/bin/env python3
"""Re-derive every figure in workplan/2026-09-18-pipeline-content-review-and-walkability.md.

Read-only. Run:  python3 scratchpad/batch-13-content-review-kpz7u8/walk.py

THIS IS A PROBE, NOT A GATE. Several sections below re-ask questions that
registered checks already own, and where they do, the check is cited so a reader
goes to the enforced one rather than trusting this. A /simplify pass found that
three of the original re-implementations silently asked a DIFFERENT question from
the check they duplicated -- reporting unverified rows, and counting searches from
before db.py refused a prior-less log-search. Both are fixed here. It lives under
scratchpad/, which schema_reference_audit SKIPs, so a table rename sweeps every
other reader and leaves this file silently broken: see GAP-013.
"""
import sqlite3, json, os

db = os.environ.get('GUIDEBOOK_DB_PATH', 'data/guidebook.db')
con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
c = con.cursor()
one = lambda q, *a: c.execute(q, a).fetchone()[0]

print(f"user_version = {one('PRAGMA user_version')}\n")

# Bound once: these are the denominators several sections share, and issuing the
# same count twice invites a reader to check that two literals still agree.
SOURCES = one("select count(*) from evidence_sources")
EXTRACTIONS = one("select count(*) from source_value_extractions")

print("== §1 the walk ==")
for label, mech, num, den in [
    ("1 base->research     ", "slugs.slug <- search_executions.slug",
     one("select count(*) from search_executions se join slugs s on se.slug=s.slug"),
     one("select count(*) from search_executions")),
    ("2 research->evidence ", "search_admissions(exec_id, ref_id)",
     one("select count(distinct ref_id) from search_admissions"), SOURCES),
    ("3 evidence internal  ", "source_value_extractions.ref_id",
     one("select count(*) from source_value_extractions where ref_id is not null"), EXTRACTIONS),
    ("4 evidence->judgment ", "evidence_population_match.ref_id",
     one("select count(distinct ref_id) from evidence_population_match"), SOURCES),
    ("6 synth->specification", "specifications.convergence_id",
     one("select count(*) from specifications where convergence_id is not null"),
     one("select count(*) from specifications")),
]:
    print(f"{label} {mech:<42} KEYED  {num}/{den}")
print(f"5 judgment->synthesis  convergence_assessment                      "
      f"*** {len(list(c.execute('PRAGMA foreign_key_list(convergence_assessment)')))} FKs -- the break ***")
print(f"7 spec->render         site/ files = {sum(len(f) for _, _, f in os.walk('site'))}   <-- no pages")
print(f"foreign_key_check violations = {len(list(c.execute('PRAGMA foreign_key_check')))}\n")

# The LIVE determination and everything read off it, in ONE query. Never a literal
# id: batch 15 retired spec 7, and a script pinned to 7 would have gone on
# measuring a retired row while calling it the determination.
LIVE, CONV, GOVERNING, FUNCTIONAL = c.execute(
    "select specification_id, convergence_id, governing_refs, functional_basis "
    "from specifications where retired_at is null "
    "order by specification_id desc limit 1").fetchone()
print(f"live specification_id = {LIVE} (derived); its convergence_id = {CONV}\n")

print("== F2 convergence carries refs as JSON, not pointers ==")
# ALL FIVE ref-id columns. down_weighted_sources is also a JSON array of REF-IDs
# and omitting it undercounts the moment anything is down-weighted. Every column
# is nullable and json.loads(None) raises, so coalesce.
CONV_COLS = ["clinical_sources", "co1_sources", "co2_sources",
             "down_weighted_sources", "discounted_sources"]
row = c.execute(f"select {','.join(CONV_COLS)} from convergence_assessment "
                f"where convergence_id=?", (CONV,)).fetchone()
print(f"ref_ids in convergence_id={CONV} JSON across {len(CONV_COLS)} columns: "
      f"{sum(len(json.loads(x or '[]')) for x in row)}\n")

print("== F3 rule 5: same fact, two homes ==")
print("   (ENFORCED ELSEWHERE: scripts/tests/test_db_integrity.py H01/H02 check the")
print("    governing_refs parity in both directions across ALL specs, and H06/H07 the")
print("    non-array and repeated-entry cases this equality silently passes.)")
gr = sorted(json.loads(GOVERNING or "[]"))
lk = sorted(r[0] for r in c.execute(
    "select ref_id from specification_source_links where specification_id=? and role='governing'", (LIVE,)))
print(f"governing_refs == specification_source_links : {gr == lk}")
print("   (ENFORCED ELSEWHERE: scripts/audit/derivation_handshake_integrity.py check 4,")
print("    which keys each spec against ITS OWN identity_code; the MOB below is hardcoded.)")
fb = sorted(x['icf_code'] for x in json.loads(FUNCTIONAL or "[]"))
pil = sorted(r[0] for r in c.execute(
    "select icf_code from population_icf_links where population_code='MOB'"))
print(f"functional_basis == population_icf_links[MOB] : {fb == pil}\n")

print("== F4 supersession chain ==")
for r in c.execute("select specification_id, retired_at is not null, "
                   "superseded_by_specification_id from specifications order by 1"):
    print(f"  spec {r[0]}  retired={'YES' if r[1] else 'no '}  superseded_by={r[2]}")

for heading, sub, note in [
    ("F5 sources with no admission edge",
     "select ref_id from search_admissions", ""),
    ("F6 sources with no population match",
     "select ref_id from evidence_population_match where ref_id is not null",
     "   (scoped to VERIFIED, matching scripts/audit/research_protocol_audit.py CHECK 2,\n"
     "    which is the enforced home. An unscoped NOT IN reports unverified rows too.)"),
]:
    print(f"\n== {heading} ==")
    if note:
        print(note)
    print("  ", [r[0] for r in c.execute(
        f"select ref_id from evidence_sources where verification_status='VERIFIED' "
        f"and ref_id not in ({sub})")])

print(f"\n== F7 observed_terms={one('select count(*) from observed_terms')} "
      f"term_adjudications={one('select count(*) from term_adjudications')}")

print("\n== F8 structured locators ==")
# One aggregate rather than one scan per column.
loc = [x[1] for x in c.execute('PRAGMA table_info(source_value_extractions)')
       if x[1].startswith('loc_') or x[1] == 'locator_scheme']
sums = c.execute("select " + ",".join(f"sum({col} is not null)" for col in loc)
                 + ", sum(source_section is not null) from source_value_extractions").fetchone()
print(f"{len(loc)} structured columns, {sum(1 for v in sums[:len(loc)] if v)} populated; "
      f"source_section populated on {sums[-1]}/{EXTRACTIONS}")

print("\n== F9 lang_detected vs canonical (lang_jur_map is UPPERCASE) ==")
canon = {x[0] for x in c.execute("select distinct language from lang_jur_map")}
for v, n in c.execute("select coalesce(lang_detected,'<NULL>'),count(*) "
                      "from evidence_sources group by 1 order by 1"):
    print(f"  {v:<8} n={n}  canonical={v in canon}")

print("\n== F10 staged candidates ==")
for r in c.execute("select disposition,count(*) from search_candidates group by 1 order by 2 desc"):
    print(f"  {r[0]:<22} {r[1]}")

print("\n== §3 R8 priors by session ==")
# db.py did not refuse a prior-less log-search until this date, so searches logged
# before it were NOT REQUIRED to carry a prior and are not a compliance gap.
# search_executions is append-only under R8 and they cannot be backfilled.
# Constant and rationale: scripts/audit/research_protocol_audit.py CHECK 7.
PRIOR_REFUSAL_LANDED = "2026-09-03"
for r in c.execute("""select created_by_session,
    sum(case when prior_expectation is null or prior_expectation='' then 1 else 0 end), count(*),
    min(created_at)
    from search_executions group by 1 order by min(exec_id)"""):
    era = "pre-writer" if (r[3] or "") < PRIOR_REFUSAL_LANDED else "REQUIRED"
    print(f"  {r[0][:52]:54} missing {r[1]}/{r[2]}  [{era}]")
print(f"  (rows marked pre-writer predate {PRIOR_REFUSAL_LANDED}; they were never "
      f"required to carry a prior.)")
