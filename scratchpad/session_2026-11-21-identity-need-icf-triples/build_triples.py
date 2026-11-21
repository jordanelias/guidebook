"""Build the proposed identity x access-need x ICF triples (T-145 research batch), fourth version.

Reads data/guidebook.db read-only; writes triples.json (rows to propose), withheld.json (rows held for an owner
question) and exclusions.json (need-map codes deliberately not attached, with the reason). Writes NOTHING to the DB.

JUDGED (PAIRS): which identity a named need serves, and why. DERIVED: every code (the need's own rows in
access_need_icf), every quotation (must be a substring of a live record), every pointer.

What the batch is, and is not. It records WHICH identity each need serves, the identity-to-need link the database could
not answer, and attaches the ICF codes the need's own map already holds. It proposes NO identity-side activity or
function code: the identity's map holds codes that no record ties to a particular need, the ICF titles are mostly
NULL, and the OD-67 batch (T-128) is the task that fills identity-to-ICF rows from the WHO payloads. A need-map
activity or function (d, b) code is attached only where the identity's own map holds the same code.

Rules, each answering a finding of the three adversarial passes of this session:
  * No axis. The owner retired the axis layer (ledger 2026-08-24, 2026-09-13; migration 109): no warrant names an axis,
    an axis code or status, or the taxonomy's axis mapping.
  * Every need-map environmental (e) code is attached to a judged pair; no pair-specific exclusion is made.
  * A warrant is one fixed past-tense template ("As recorded when this row was written ... read: ..."), copies no mutable
    cell (no mechanism, confidence, title, status or annotation) and holds no sentence that review falsifies; the script
    refuses a present-tense verb outside the quotations.
  * Not paired, and why (recorded in the gaps of write_batch.py): A-AT (registry note flags its scope for the owner); ALL (a scope marker, ledger OD-31);
    MOVE and VES (access needs by owner answer OD-37); SCI (same population as WHEEL, retirement open as OI-77);
    MOB and LMB (the registry has not been split: T-102 and OI-49 give WHEEL, WALKAID, LLD and UPL, which do not exist
    yet, and a row keyed on the parent could leave only by an owner ledger entry); A-PRECISION (its only identity was MOVE).
  * Body-function (b) codes are WITHHELD for the owner (a recorded question): the identity map holds d codes only.
"""
import json, sqlite3, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent
BASIS = {
 "named": "The need's registry text named a group that the identity's name or description covered.",
 "served": "The identity's description named this need as serving it, and the need's registry text named the same group.",
 "member": "The need's registry text named a condition that the identity's description listed or included. The row was keyed on the whole identity, not only that condition.",
 "includes": "The identity's description said it included the member whose condition the need's registry text named, and the owner retained the identity (ledger, third set). The row was keyed on the whole identity, not only that member.",
 "inference": "No record read stated this link; it was recorded as an inference. The row was keyed on the whole identity.",
}
BRAINFOG = "The need's registry text named brain fog; the identity's description listed long COVID and ME/CFS; that the identity carried brain fog was not stated by the records read."
INCL = "includes AUT, ADHD, and others"

# i, n, kind (a BASIS key); qn = quote from the need's records; qi = quote from the identity's records; note = extra
# recorded reading; withhold = {code: reason}; rec = [(path, substring)] checked to exist.
PAIRS = [
 dict(i="BLIND", n="A-NOSIGHT", kind="named", qn="blindness, low vision", qi="blind and low-vision people"),
 dict(i="DEAF", n="A-NOSOUND", kind="named", qn="Deaf, hard of hearing, late-deafened", qi="Deaf, or late-deafened"),
 dict(i="DEAFBLIND", n="A-TACTILE", kind="named", qn="DeafBlind (Protactile)", qi="Not VIS+DEAF"),
 dict(i="BRAIN", n="A-STABLE", kind="member", qn="post-concussion", qi="post-concussion"),
 dict(i="BRAIN", n="A-NOSPEECH", kind="inference", qn="aphasia", qi="stroke",
      note="The need's registry text named aphasia; the identity's description listed stroke; that aphasia follows stroke was not stated by the identity's own description."),
 dict(i="ID", n="A-PLAIN", kind="named", qn="intellectual disability", qi="people with intellectual disability"),
 dict(i="DEM", n="A-PLAIN", kind="named", qn="dementia", qi="Alzheimer disease and related dementias"),
 dict(i="BRAIN", n="A-PLAIN", kind="named", qn="brain injury", qi="acquired brain injury"),
 dict(i="DEM", n="A-LOWLOAD", kind="named", qn="dementia", qi="Alzheimer disease and related dementias"),
 dict(i="ADHD", n="A-LOWLOAD", kind="named", qn="ADHD", qi="ADHD"),
 dict(i="NDV", n="A-LOWLOAD", kind="includes", qn="ADHD", qi=INCL),
 dict(i="BRAIN", n="A-LOWLOAD", kind="named", qn="brain injury", qi="acquired brain injury"),
 dict(i="ID", n="A-LOWLOAD", kind="named", qn="intellectual disability", qi="people with intellectual disability"),
 dict(i="COM", n="A-LOWLOAD", kind="inference", qn="brain fog", qi="long COVID, MCAS, ME/CFS, POTS", note=BRAINFOG),
 dict(i="COM", n="A-TIME", kind="inference", qn="brain fog impairs organizing time", qi="long COVID, MCAS, ME/CFS, POTS",
      note="The need's own ICF row (access_need_icf, A-TIME to b164) recorded the owner's rationale that brain fog impairs organizing time; the identity's description listed long COVID and ME/CFS; that the identity carried brain fog was not stated by the records read.",
      withhold={"b164": "a body-function code on an identity; see the recorded owner question"}),
 dict(i="COM", n="A-EFFORT", kind="member", qn="ME/CFS, Long COVID, POTS", qi="long COVID, MCAS, ME/CFS, POTS"),
 dict(i="MS", n="A-EFFORT", kind="named", qn="MS fatigue", qi="fatigue"),
 dict(i="PAIN", n="A-EFFORT", kind="named", qn="pain", qi="sustained discomfort affecting endurance"),
 dict(i="AUT", n="A-STIMULUS", kind="named", qn="autistic people", qi="Autism spectrum"),
 dict(i="NDV", n="A-STIMULUS", kind="includes", qn="autistic people", qi=INCL),
 dict(i="BRAIN", n="A-STIMULUS", kind="member", qn="post-concussion", qi="post-concussion"),
 dict(i="MH", n="A-STIMULUS", kind="member", qn="PTSD", qi="trauma", note="PTSD was read as falling under the description's \"trauma\"."),
 dict(i="EPI", n="A-TRIGGER", kind="member", qn="photosensitive epilepsy", qi="photosensitivity"),
 dict(i="COM", n="A-TRIGGER", kind="member", qn="MCAS", qi="MCAS"),
 dict(i="MH", n="A-CALM", kind="member", qn="anxiety, PTSD, psychiatric distress", qi="Mood, anxiety, trauma"),
 dict(i="AUT", n="A-CALM", kind="named", qn="autistic people", qi="Autism spectrum"),
 dict(i="NDV", n="A-CALM", kind="includes", qn="autistic people", qi=INCL),
] + [
 dict(i=i, n="A-SIZE", kind="served", qn=q, qi="Served by A-SIZE")
 for i, q in (("LPA", "little people"), ("TALL", "tall people"), ("BAR", "fat people"))
]

PRESENT = (" is ", " are ", " says ", " includes ", " names ", " lists ", " holds ", " has ", " carries ")


def main():
    c = sqlite3.connect(f"file:{ROOT}/data/guidebook.db?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    idn = {r["identity_code"]: r for r in c.execute("select * from base_taxonomy_identity where status='active'")}
    need = {r["need_code"]: r for r in c.execute("select * from access_needs")}
    imap = {(r["identity_code"], r["icf_code"]) for r in c.execute("select * from identity_icf_map where retired_at is null")}
    nmap = {}
    for r in c.execute("select * from access_need_icf order by icf_code"):
        nmap.setdefault(r["need_code"], {})[r["icf_code"]] = r
    errors, triples, withheld, excluded, seen = [], [], [], [], set()
    for p in PAIRS:
        I, N = p["i"], p["n"]
        if I not in idn: errors.append(f"{I}: not an active identity"); continue
        if N not in need: errors.append(f"{N}: not a need"); continue
        ntext = " | ".join(filter(None, [need[N]["absorbs"], need[N]["notes"]] + [r["notes"] for r in nmap.get(N, {}).values()]))
        itext = " | ".join(filter(None, [idn[I]["display_name"], idn[I]["description"]]))
        if p["qn"] not in ntext: errors.append(f"{I}x{N}: need quote not found in the need's absorbs, notes or ICF notes: {p['qn']!r}")
        if p["qi"] not in itext: errors.append(f"{I}x{N}: identity quote not found in the identity's name or description: {p['qi']!r}")
        for path, sub in p.get("rec", []):
            if sub not in (ROOT / path).read_text(): errors.append(f"{I}x{N}: record {path} lacks {sub!r}")
        for code, r in sorted(nmap.get(N, {}).items()):
            if code in p.get("withhold", {}): continue
            if code[0] != "e" and (I, code) not in imap:
                excluded.append(dict(identity=I, need=N, icf=code, reason=f"need-map {code[0]} code that {I}'s own map does not hold")); continue
            if (I, N, code) in seen: errors.append(f"{I}x{N}x{code}: listed twice"); continue
            seen.add((I, N, code))
            tail = f"Code {code}: access_need_icf held {N} -> {code}."
            if (I, code) in imap: tail += f" identity_icf_map also held {code} for {I}."
            warrant = (f"As recorded when this row was written: {BASIS[p['kind']]} Need {N} registry text read: \"{p['qn']}\". "
                       f"Identity {I} read: \"{p['qi']}\". " + (p.get("note", "") + " " if p.get("note") else "") + tail)
            outside = " ".join(warrant.split('"')[0::2])
            bad = [w for w in PRESENT if w in outside]
            if bad: errors.append(f"{I}x{N}x{code}: present-tense verb outside the quotations: {bad}"); continue
            triples.append(dict(identity=I, need=N, icf=code, support="both maps" if (I, code) in imap else "need map", warrant=warrant))
        for code, why in p.get("withhold", {}).items():
            withheld.append(dict(identity=I, need=N, icf=code, reason=why))
    if errors:
        print("REFUSED:"); [print(" ", e) for e in errors]; sys.exit(1)
    for name, data in (("triples", triples), ("withheld", withheld), ("exclusions", excluded)):
        (HERE / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    from collections import Counter
    print(f"proposed: {len(triples)}  withheld: {len(withheld)}  excluded: {len(excluded)}  pairs: {len(PAIRS)}")
    print("by support:", dict(Counter(t["support"] for t in triples)))
    print("identities:", sorted({t['identity'] for t in triples}))
    print("needs:", sorted({t['need'] for t in triples}))
    print("max warrant length:", max(len(t["warrant"]) for t in triples))
    for e in excluded: print("  excluded:", e["identity"], e["need"], e["icf"], "-", e["reason"][:70])

main()
