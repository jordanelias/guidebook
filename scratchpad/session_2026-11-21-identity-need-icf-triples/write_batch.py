"""Write the matrix batch into a scratch copy of the database through db.py (never the canonical DB).
Usage: python3 -I write_batch.py <scratch.db>   (the scratch copy must be a fresh copy of data/guidebook.db)
Reads triples.json (build_triples.py output). Files the gaps of the batch. No figure is typed: each gap
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
  "OWNER QUESTION: may a disability identity be linked to an ICF body-function (b) code? identity_icf_map holds activity (d) codes only. Records on the question: governance/functional-taxonomy.md (grep -n -F 'never serves as a description of any person' governance/functional-taxonomy.md: a b-code anchor serves findability); the ledger's seventh-set ACTION (4) and OI-48 (an injury and its level 'held in the medical lens and ICF b-codes'), whose premise the 2026-11-16 correction narrowed, and OI-77, still open. The matrix therefore proposes no b-code row. The rows withheld are an inference pair (python3 -I -c \"import json;[print(r['identity'],r['need'],r['icf']) for r in json.load(open('" + D + "/withheld.json'))]\"). Body-function rows that would have rested on the retired axis layer were not proposed and are not offered: the owner ruled the layer retired (ledger 2026-08-24 and 2026-09-13; migration 109). Identity-to-ICF rows for identities with no activity code are the OD-67 batch (MAPPING-DESIGN.md section 5, T-128), which fetches the WHO payloads."),
 ("DEC", "P1", None,
  "OWNER QUESTION: do need-side environmental rows count as an identity's ICF rows? Every row of the identity, need and ICF table is a judged identity-need pair crossed with the codes the need's own access_need_icf rows hold (derive: select substr(icf_code,1,1), count(*) from identity_need_icf group by 1); no identity-side activity code is proposed (see the b-code question and T-128). Reviewed as stated, such a row removes its identity from db.py lens-crosswalk --uncovered, while the entry 'Owner statements 2026-11-20 — translation runs before judgment', ACTION (3), reads an identity with no ICF code as a gap to close. Derive the identities that hold a row with an activity code: select distinct identity_code from identity_need_icf where substr(icf_code,1,1)<>'e' (empty at filing). If the answer is no, the owner rejects the rows at review, or keeps them as the identity-to-need link they record."),
 ("DEC", "P2", None,
  "OWNER QUESTION: may a member's need be keyed on its umbrella identity? Rows whose warrant says the row was keyed on the whole identity: select identity_code, need_code, count(*) from identity_need_icf where warrant like '%keyed on the whole identity%' group by 1,2. The ledger ratified union carry for COM and BRAIN (grep -n -F 'Always preserve the union of member axis signatures on the umbrella' references/project-standards.md) and retained MH, NDV and TALL as identity codes (third set); it does not say that a member's need carries to NDV, and v_lens_crosswalk reads the key, not the qualifier. At filing the NDV rows equal the AUT and ADHD rows on the same need code for code. Rows recorded as inferences (no record read states the link): select identity_code, need_code from identity_need_icf where warrant like '%recorded as an inference%'. Also open: the need's e120 row (mobility products and technology) is attached to LPA, TALL and BAR through A-SIZE's own row, identities of category general, while the owner placed LMB outside the mobility family; and A-TRIGGER's e240 and e260 rows are attached to both EPI and COM, where the need's own note splits them by retired vocabulary."),
 ("DEC", "P2", "A-AT",
  "OWNER QUESTION: is A-AT (work with assistive technology; programmatically-determinable structure) inside the built-environment scope? Its registry note says 'Digital — may be out of built-environment scope; flagged for owner decision'. No identity-need-ICF triple was proposed for it. Derive the needs with no triple: select need_code from access_needs where need_code not in (select need_code from identity_need_icf). At filing the others are unpaired for these reasons: A-TIME, its only support is the withheld b-code row; A-PRECISION, its only identity was MOVE, an access need by OD-37; A-REACH, its identities MOB and LMB wait on the registry change that T-102 and the execution of OI-49 make (WHEEL, WALKAID, LLD and UPL are not yet registry rows); A-SELFCARE, its registry text names activities and no group, and the only candidates by the maps were MOB, LMB and SCI."),
 ("EG", "P2", None,
  "COVERAGE of the identity, access-need and ICF table. (1) Identities with no triple: select identity_code from base_taxonomy_identity where status='active' and identity_code not in (select identity_code from identity_need_icf where retired_at is null). At filing: ALL (a scope marker, not an identity: OD-31); MOVE and VES (access needs by the owner's answer OD-37, which base_taxonomy_identity still lists as active identities); SCI (the same population as WHEEL by the seventh and eighth sets; retirement waits on OI-77); MOB and LMB (the owner's rulings give WHEEL, WALKAID, LLD and UPL, which are not yet registry rows, and a row keyed on the parent can leave only by an owner ledger entry: propose these rows after T-102). (2) ICF titles are NULL on most codes (GAP-ICF-TITLES); no activity code is proposed here. (3) db.py lens-crosswalk --uncovered lists identities with no REVIEWED triple, so it lists every identity until the owner reviews."),
 ("SW", "P2", None,
  "adversarial_pass_recorded (governance/check-registry.yaml) reads the tables the 2026-08-19 RULE names, and identity_need_icf is not among them: grep -rl identity_need_icf scripts/audit prints nothing, so a session that fills the table owes no recorded pass by that check. Derive the subject tables from the writers (dbcore.writable_tables), as rule 8 requires, in a tooling pull request and not in a batch. Also: record-adversarial-pass allows one pass per session, and this batch was attacked by four read-only passes; only the first is in adversarial_passes, and its subject commit holds the first version of the rows (adversarial_pass_audit.py prints NOTHING-IN-SCOPE for it). The final version of the rows had no pass of its own. All the passes' findings and the author's dispositions are in " + D + "/adjudication.md; the transcripts are under transcripts/harness_de695d5a/subagents. The table's trigger identity_need_icf_no_edit forbids any change to a triple's keys or warrant, so a wrong warrant is corrected only by retiring the row under an owner ledger entry."),
]
for cat, pri, need, desc in GAPS:
    a = ["add-gap", "--category", cat, "--priority", pri, "--session", S, "--description", desc]
    if need: a += ["--needs", need]
    print(json.loads(db(*a))["gap_id"])
