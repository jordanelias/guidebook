"""Write the matrix batch into a scratch copy of the database through db.py (never the canonical DB).
Usage: python3 -I write_batch.py <scratch.db>   (the scratch copy must be a fresh copy of data/guidebook.db)
Reads triples.json (build_triples.py output). Files the four gaps of the batch. No figure is typed: each gap
carries the command that derives it."""
import json, os, subprocess, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent
S = "session_2026-11-21-identity-need-icf-triples"
env = dict(os.environ, GUIDEBOOK_DB_PATH=sys.argv[1])

def db(*a):
    p = subprocess.run(["python3", "scripts/db.py", *a], cwd=ROOT, env=env, capture_output=True, text=True)
    if p.returncode: sys.exit(f"FAILED {a[:3]}\n{p.stdout[-400:]}{p.stderr[-400:]}")
    return p.stdout

triples = json.loads((HERE / "triples.json").read_text())
for r in triples:
    db("propose-identity-need-icf", "--identity", r["identity"], "--need", r["need"], "--icf-code", r["icf"],
       "--warrant", r["warrant"], "--session", S)
print("proposed", len(triples))
D = f"scratchpad/{S}"
GAPS = [
 ("DEC", "P1", None,
  "OWNER QUESTION: may a disability identity be linked to an ICF body-function (b) code? identity_icf_map holds activity (d) codes only. Records on the question: governance/functional-taxonomy.md lines 38-41 (a b-code anchor serves findability and is never a description of any person); the ledger's seventh-set ACTION (4) and OI-48 (an injury and its level 'held in ICF b-codes'), whose premise the 2026-11-16 correction narrowed, and OI-77, still open. The matrix therefore proposes no b-code row. Rows withheld that the project's own records support: python3 -I -c \"import json;[print(r['identity'],r['need'],r['icf']) for r in json.load(open('" + D + "/withheld.json'))]\". Body-function rows that would have rested on the retired axis layer were not proposed and are not offered: the owner ruled the layer retired (ledger 2026-08-24 and 2026-09-13; migration 109). The work that fills identity-to-ICF rows for identities with no activity code is the OD-67 batch (MAPPING-DESIGN.md section 5, T-128), which fetches the WHO payloads."),
 ("DEC", "P2", "A-AT",
  "OWNER QUESTION: is A-AT (work with assistive technology; programmatically-determinable structure) inside the built-environment scope? Its registry note says 'Digital — may be out of built-environment scope; flagged for owner decision'. No identity-need-ICF triple was proposed for it. Derive the needs with no triple: select need_code from access_needs where need_code not in (select need_code from identity_need_icf). A-TIME is unpaired for a different reason at filing: its only support is the withheld b-code row (see the b-code question)."),
 ("EG", "P2", None,
  "COVERAGE of the identity, access-need and ICF table. (1) Identities with no triple: select identity_code from base_taxonomy_identity where status='active' and identity_code not in (select identity_code from identity_need_icf where retired_at is null). At filing these are ALL (a scope marker, not an identity: OD-31), MOVE and VES (access needs by the owner's answer OD-37, which base_taxonomy_identity still lists as active identities) and SCI (the same population as WHEEL by the seventh and eighth sets; its retirement waits on OI-77). (2) Most rows are need-side environmental codes attached to every judged pair: select substr(icf_code,1,1), count(*) from identity_need_icf group by 1. They say how the need is met for that identity and are not an identity-specific link, so an identity that has them is not thereby covered. Derive the identities with no activity code: select identity_code from base_taxonomy_identity where status='active' and identity_code not in (select identity_code from identity_need_icf where substr(icf_code,1,1)<>'e'). (3) Need-map codes deliberately not attached, with the reason: " + D + "/exclusions.json. (4) ICF titles are NULL on most codes (GAP-ICF-TITLES): an activity-code row rests on a word verified in both the identity's and the need's own records, named in its warrant, never on a title. (5) db.py lens-crosswalk --uncovered lists identities with no REVIEWED triple, so it lists every identity until the owner reviews."),
 ("SW", "P2", None,
  "adversarial_pass_recorded (governance/check-registry.yaml) reads the tables the 2026-08-19 RULE names, and identity_need_icf is not among them: grep -rl identity_need_icf scripts/audit prints nothing, so a session that fills the table owes no recorded pass by that check. Derive the subject tables from the writers (dbcore.writable_tables), as rule 8 requires, in a tooling pull request and not in a batch. Also: record-adversarial-pass allows one pass per session, and this batch was attacked by three read-only passes; only the first is in adversarial_passes, and its subject commit holds an earlier version of the rows. The later two, which attacked the migration itself, are in " + D + "/adjudication.md and the committed transcripts. The table's trigger identity_need_icf_no_edit forbids any change to a triple's keys or warrant, so a wrong warrant is corrected only by retiring the row under an owner ledger entry."),
]
for cat, pri, need, desc in GAPS:
    a = ["add-gap", "--category", cat, "--priority", pri, "--session", S, "--description", desc]
    if need: a += ["--needs", need]
    print(json.loads(db(*a))["gap_id"])
