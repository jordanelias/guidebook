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
  * Every need-map environmental (e) code is attached to a judged pair, except where a stated exclusion applies.
  * A warrant is written in the past tense of its own recording ("As recorded when this row was written"), copies no
    mutable cell (no mechanism, confidence, title, status or annotation), and holds no sentence that review falsifies.
  * Not paired, and why: A-AT (registry note flags its scope for the owner); ALL (a scope marker, ledger OD-31);
    MOVE and VES (access needs by owner answer OD-37); SCI (same population as WHEEL, retirement open as OI-77);
    MOB and LMB (the registry has not been split: T-102 and OI-49 give WHEEL, WALKAID, LLD and UPL, which do not exist
    yet, and a row keyed on the parent could leave only by an owner ledger entry); A-PRECISION (its only identity was MOVE).
  * Body-function (b) codes are WITHHELD for the owner (a recorded question): the identity map holds d codes only.
"""
import json, sqlite3, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent
MEMBER = " The named condition is one member of this identity, and the row is keyed on the whole identity."
NDV = "The identity's description says it includes AUT, ADHD and others; the owner retained it as an identity (ledger, third set)."

# i, n; qn = quote from the need's records; qi = quote from the identity's records; why; skip = {code: reason};
# withhold = {code: reason}; rec = [(path, substring)].
PAIRS = [
 dict(i="BLIND", n="A-NOSIGHT", qn="blindness, low vision", qi="blind and low-vision people",
      why="The need's registry text named blindness and low vision, and the identity is blind and low-vision people."),
 dict(i="DEAF", n="A-NOSOUND", qn="Deaf, hard of hearing, late-deafened", qi="Deaf, or late-deafened",
      why="The need's registry text named Deaf, hard-of-hearing and late-deafened people."),
 dict(i="DEAFBLIND", n="A-TACTILE", qn="DeafBlind (Protactile)", qi="Not VIS+DEAF",
      why="The need's registry text named DeafBlind (Protactile) access, and the identity's description said it is not blindness plus deafness."),
 dict(i="BRAIN", n="A-STABLE", qn="post-concussion", qi="post-concussion",
      why="The need's registry text named post-concussion, and the identity's description included post-concussion." + MEMBER),
 dict(i="BRAIN", n="A-NOSPEECH", qn="aphasia", qi="stroke",
      why="The need's registry text named aphasia, and the identity's description included stroke; the neurological and acquired brain injury profile in references/website/data/populations.json listed \"stroke sequelae (unilateral neglect, navigation impairment, aphasia, hemiplegia)\"." + MEMBER,
      rec=[("references/website/data/populations.json", "stroke sequelae (unilateral neglect, navigation impairment, aphasia, hemiplegia)")]),
 dict(i="ID", n="A-PLAIN", qn="intellectual disability", qi="people with intellectual disability",
      why="The need's registry text named intellectual disability, and the identity is people with intellectual disability."),
 dict(i="DEM", n="A-PLAIN", qn="dementia", qi="Alzheimer disease and related dementias",
      why="The need's registry text named dementia, and the identity is people living with dementia."),
 dict(i="BRAIN", n="A-PLAIN", qn="brain injury", qi="acquired brain injury",
      why="The need's registry text named brain injury, and the identity is people with acquired brain injury."),
 dict(i="DEM", n="A-LOWLOAD", qn="dementia", qi="Alzheimer disease and related dementias",
      why="The need's registry text named dementia, and the identity is people living with dementia."),
 dict(i="ADHD", n="A-LOWLOAD", qn="ADHD", qi="ADHD",
      why="The need's registry text named ADHD, and the identity is people with ADHD."),
 dict(i="NDV", n="A-LOWLOAD", qn="ADHD", qi="includes AUT, ADHD, and others",
      why="The need's registry text named ADHD. " + NDV + MEMBER),
 dict(i="BRAIN", n="A-LOWLOAD", qn="brain injury", qi="acquired brain injury",
      why="The need's registry text named brain injury, and the identity is people with acquired brain injury."),
 dict(i="ID", n="A-LOWLOAD", qn="intellectual disability", qi="people with intellectual disability",
      why="The need's registry text named intellectual disability, and the identity is people with intellectual disability."),
 dict(i="COM", n="A-TIME", qn="brain fog impairs organizing time", qi="long COVID, MCAS, ME/CFS, POTS",
      why="The need's own ICF row (access_need_icf, A-TIME to b164) recorded the owner's rationale that brain fog impairs organizing time, and the identity's description listed long COVID and ME/CFS. That the identity carries brain fog is not stated in a project record: this pair is an inference." + MEMBER,
      withhold={"b164": "a body-function code on an identity; see the recorded owner question"}),
 dict(i="COM", n="A-EFFORT", qn="ME/CFS, Long COVID, POTS", qi="long COVID, MCAS, ME/CFS, POTS",
      why="The need's registry text named ME/CFS, Long COVID and POTS, and the identity's description listed the same conditions."),
 dict(i="MS", n="A-EFFORT", qn="MS fatigue", qi="fatigue",
      why="The need's registry text named MS fatigue, and the identity's description named fatigue."),
 dict(i="PAIN", n="A-EFFORT", qn="pain", qi="sustained discomfort affecting endurance",
      why="The need's registry text named pain, and the identity's description said pain affects endurance."),
 dict(i="AUT", n="A-STIMULUS", qn="autistic people", qi="Autism spectrum",
      why="The need's registry text named autistic people, and the identity is autistic people."),
 dict(i="NDV", n="A-STIMULUS", qn="autistic people", qi="includes AUT, ADHD, and others",
      why="The need's registry text named autistic people and sensory processing differences. " + NDV + MEMBER),
 dict(i="BRAIN", n="A-STIMULUS", qn="post-concussion", qi="post-concussion",
      why="The need's registry text named post-concussion, and the identity's description included post-concussion." + MEMBER),
 dict(i="MH", n="A-STIMULUS", qn="PTSD", qi="trauma",
      why="The need's registry text named PTSD, and the identity's description named trauma." + MEMBER),
 dict(i="EPI", n="A-TRIGGER", qn="photosensitive epilepsy", qi="photosensitivity",
      why="The need's registry text named photosensitive epilepsy, and the identity's description named photosensitivity as a subtype.",
      skip={"e260": "air quality; the need's own annotation on e240 is flash/strobe, the photic row"}),
 dict(i="COM", n="A-TRIGGER", qn="MCAS", qi="MCAS",
      why="The need's registry text named MCAS, and the identity's description listed MCAS." + MEMBER,
      skip={"e240": "annotated flash/strobe in the need's own row, a photic trigger not tied to MCAS in any record"}),
 dict(i="MH", n="A-CALM", qn="anxiety, PTSD, psychiatric distress", qi="Mood, anxiety, trauma",
      why="The need's registry text named anxiety, PTSD and psychiatric distress, and the identity's description named mood, anxiety and trauma."),
 dict(i="AUT", n="A-CALM", qn="autistic people", qi="Autism spectrum",
      why="The need's registry text named autistic people, and the identity is autistic people."),
 dict(i="NDV", n="A-CALM", qn="autistic people", qi="includes AUT, ADHD, and others",
      why="The need's registry text named autistic people. " + NDV + MEMBER),
] + [
 dict(i=i, n="A-SIZE", qn=q, qi="Served by A-SIZE",
      why=f"The identity's description said it is served by this need, and the need's registry text named {q}.")
 for i, q in (("LPA", "little people"), ("TALL", "tall people"), ("BAR", "fat people"))
]


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
        skip = p.get("skip", {})
        for code, r in sorted(nmap.get(N, {}).items()):
            if code in skip: excluded.append(dict(identity=I, need=N, icf=code, reason=skip[code])); continue
            if code in p.get("withhold", {}): continue
            if code[0] != "e" and (I, code) not in imap:
                excluded.append(dict(identity=I, need=N, icf=code, reason=f"need-map {code[0]} code that {I}'s own map does not hold")); continue
            if (I, N, code) in seen: errors.append(f"{I}x{N}x{code}: listed twice"); continue
            seen.add((I, N, code))
            tail = f"Code {code}: access_need_icf held {N} -> {code}."
            if (I, code) in imap: tail += f" identity_icf_map also held {code} for {I}."
            triples.append(dict(identity=I, need=N, icf=code, support="both maps" if (I, code) in imap else "need map",
                                warrant=f"As recorded when this row was written: {p['why']} Need {N} registry text read: \"{p['qn']}\". Identity {I} read: \"{p['qi']}\". {tail}"))
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
