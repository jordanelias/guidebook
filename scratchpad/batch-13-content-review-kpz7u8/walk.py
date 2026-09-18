#!/usr/bin/env python3
"""Re-derive every figure in workplan/2026-09-18-pipeline-content-review-and-walkability.md.

Read-only. Run:  python3 scratchpad/batch-13-content-review-kpz7u8/walk.py
"""
import sqlite3, json, os, sys

db = os.environ.get('GUIDEBOOK_DB_PATH', 'data/guidebook.db')
con = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
c = con.cursor()
one = lambda q, *a: c.execute(q, a).fetchone()[0]

print(f"user_version = {one('PRAGMA user_version')}\n")

print("== §1 the walk ==")
print(f"1 base->research      {one('select count(*) from search_executions se join slugs s on se.slug=s.slug')}"
      f"/{one('select count(*) from search_executions')} execs keyed")
print(f"2 research->evidence  {one('select count(distinct ref_id) from search_admissions')}"
      f"/{one('select count(*) from evidence_sources')} sources keyed")
print(f"3 evidence internal   {one('select count(*) from source_value_extractions where ref_id is not null')}"
      f"/{one('select count(*) from source_value_extractions')} extractions keyed")
print(f"4 evidence->judgment  {one('select count(distinct ref_id) from evidence_population_match')}"
      f"/{one('select count(*) from evidence_sources')} sources graded")
print(f"5 judgment->synthesis FKs on convergence_assessment = "
      f"{len(list(c.execute('PRAGMA foreign_key_list(convergence_assessment)')))}   <-- the break")
print(f"6 synth->specification {one('select count(*) from specifications where convergence_id is not null')}"
      f"/{one('select count(*) from specifications')} specs keyed")
print(f"7 spec->render        site/ files = {sum(len(f) for _,_,f in os.walk('site'))}   <-- no pages")
print(f"foreign_key_check violations = {len(list(c.execute('PRAGMA foreign_key_check')))}\n")

# The LIVE determination, derived -- never a literal id. Batch 15 retired spec 7
# and created spec 8, and a script pinned to 7 would have gone on measuring a
# retired row while reporting it as the determination.
LIVE = one("select specification_id from specifications where retired_at is null "
           "order by specification_id desc limit 1")
CONV = one("select convergence_id from specifications where specification_id=?", LIVE)
print(f"live specification_id = {LIVE} (derived); its convergence_id = {CONV}\n")

print("== F2 convergence carries refs as JSON, not pointers ==")
# ALL FIVE ref-id columns, not four: down_weighted_sources is also a JSON array
# of REF-IDs and omitting it undercounts the moment anything is down-weighted.
# Every one is nullable, and json.loads(None) raises, so coalesce first.
CONV_COLS = ["clinical_sources", "co1_sources", "co2_sources",
             "down_weighted_sources", "discounted_sources"]
row = c.execute(f"select {','.join(CONV_COLS)} from convergence_assessment "
                f"where convergence_id=?", (CONV,)).fetchone()
allr = sum(len(json.loads(x or "[]")) for x in row)
print(f"ref_ids in convergence_id={CONV} JSON across {len(CONV_COLS)} columns: {allr}\n")

print("== F3 rule 5: same fact, two homes ==")
gr = sorted(json.loads(one("select governing_refs from specifications where specification_id=?", LIVE) or "[]"))
lk = sorted(r[0] for r in c.execute(
    "select ref_id from specification_source_links where specification_id=? and role='governing'", (LIVE,)))
print(f"governing_refs == specification_source_links : {gr == lk}")
fb = sorted(x['icf_code'] for x in json.loads(one("select functional_basis from specifications where specification_id=?", LIVE) or "[]"))
pil = sorted(r[0] for r in c.execute("select icf_code from population_icf_links where population_code='MOB'"))
print(f"functional_basis == population_icf_links[MOB] : {fb == pil}\n")

print("== F4 supersession chain ==")
for r in c.execute("select specification_id, retired_at is not null, superseded_by_specification_id from specifications order by 1"):
    print(f"  spec {r[0]}  retired={'YES' if r[1] else 'no '}  superseded_by={r[2]}")
print()

print("== F5 sources with no admission edge ==")
print([r[0] for r in c.execute("select ref_id from evidence_sources where ref_id not in (select ref_id from search_admissions)")])

print("\n== F6 sources with no population match ==")
print([r[0] for r in c.execute(
    "select ref_id from evidence_sources where ref_id not in (select ref_id from evidence_population_match where ref_id is not null)")])

print(f"\n== F7 observed_terms={one('select count(*) from observed_terms')} "
      f"term_adjudications={one('select count(*) from term_adjudications')}")

print("\n== F8 structured locators ==")
loc = [x[1] for x in c.execute('PRAGMA table_info(source_value_extractions)')
       if x[1].startswith('loc_') or x[1] == 'locator_scheme']
pop = sum(1 for col in loc if one(f'select count(*) from source_value_extractions where {col} is not null'))
print(f"{len(loc)} structured columns, {pop} populated; source_section populated on "
      f"{one('select count(*) from source_value_extractions where source_section is not null')}"
      f"/{one('select count(*) from source_value_extractions')}")

print("\n== F9 lang_detected vs canonical (lang_jur_map is UPPERCASE) ==")
canon = {x[0] for x in c.execute("select distinct language from lang_jur_map")}
for v, n in c.execute("select coalesce(lang_detected,'<NULL>'),count(*) from evidence_sources group by 1 order by 1"):
    print(f"  {v:<8} n={n}  canonical={v in canon}")

print("\n== F10 staged candidates ==")
for r in c.execute("select disposition,count(*) from search_candidates group by 1 order by 2 desc"):
    print(f"  {r[0]:<22} {r[1]}")

print("\n== §3 R8 priors by session ==")
for r in c.execute("""select created_by_session,
    sum(case when prior_expectation is null or prior_expectation='' then 1 else 0 end), count(*)
    from search_executions group by 1 order by min(exec_id)"""):
    print(f"  {r[0][:55]:57} missing {r[1]}/{r[2]}")
