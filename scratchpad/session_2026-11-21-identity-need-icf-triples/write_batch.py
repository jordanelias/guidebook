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
W = f"scratchpad/{S}/withheld.json"
GAPS = [
 ("DEC", "P1", None,
  "OWNER QUESTION: may a disability identity be linked to an ICF body-function (b) code? identity_icf_map holds only activity (d) codes, and governance/functional-taxonomy.md 0.5 says axes describe specifications, never a portrait of a person. Triples whose code is a b-code were therefore WITHHELD, not written: they rest on an axis anchor or on the need's own ICF row (derive the list: python3 -I -c \"import json;[print(r['identity'],r['need'],r['icf']) for r in json.load(open('" + W + "'))]\"). Sharp cases: DEAF with a hearing-function code and BLIND with a seeing-function code (the pass's finding F4 names both), and COM with b164 (an inference as well). Until answered, ADHD and the need A-TIME have no triple. If yes, the withheld rows are proposed in a later batch; if no, an identity with no activity code stays on its need-side environmental codes."),
 ("DEC", "P2", "A-AT",
  "OWNER QUESTION: is A-AT (work with assistive technology; programmatically-determinable structure) inside the built-environment scope? Its registry note says 'Digital — may be out of built-environment scope; flagged for owner decision'. No identity-need-ICF triple was proposed for it, while A-TIME, A-CALM and A-NOSPEECH, whose obligations also mention digital interaction (session timeouts, dark patterns, voice-only authentication), were paired. Derive the unpaired needs: select need_code from access_needs where need_code not in (select need_code from identity_need_icf)."),
 ("EG", "P2", None,
  "COVERAGE: the identity, access-need and ICF table was filled from the project's own records only, and a pair or code those records do not support is absent. Derive the identities and needs with no proposed triple: python3 scripts/db.py lens-crosswalk --uncovered. Derive the identities that carry only need-side environmental codes (no activity code recorded for them in any map): select identity_code, group_concat(icf_code) from identity_need_icf group by 1. At filing these include LPA, TALL, BAR, DEAFBLIND, EPI and MS; for body size the ICF has no code recorded at all. Derive the identity_icf_map links that back no triple: select count(*) from identity_icf_map m where retired_at is null and not exists (select 1 from identity_need_icf t where t.identity_code=m.identity_code and t.icf_code=m.icf_code and t.retired_at is null); a link backs none where no need names the identity's condition. ICF titles are NULL on most codes (GAP-ICF-TITLES), so no relevance judgment here rests on a title."),
 ("SW", "P2", None,
  "adversarial_pass_recorded (governance/check-registry.yaml) reads the tables the 2026-08-19 RULE names, and identity_need_icf is not among them: grep -rl identity_need_icf scripts/audit prints nothing. A session that fills the table owes no recorded pass by that check, and a wrong sentence in a warrant cannot be edited after review (trigger identity_need_icf_no_edit; retirement needs an owner ledger quote). Derive the subject tables from the writers (dbcore.writable_tables), as rule 8 requires, in a tooling pull request and not in a batch."),
]
for cat, pri, need, desc in GAPS:
    a = ["add-gap", "--category", cat, "--priority", pri, "--session", S, "--description", desc]
    if need: a += ["--needs", need]
    print(json.loads(db(*a))["gap_id"])
