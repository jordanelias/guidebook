"""Build the proposed identity x access-need x ICF triples (T-145 research batch), third version.

Reads data/guidebook.db read-only; writes triples.json (rows to propose), withheld.json (rows held for an owner
question) and exclusions.json (need-map codes deliberately not attached, with the reason). Writes NOTHING to the DB.

JUDGED (PAIRS): which identity a need serves and why. DERIVED: every need-side environmental code (access_need_icf),
every activity code both maps hold, every quotation (must be a substring of a live record), every pointer (link ids).

Rules, each answering a finding of the two adversarial passes of this session:
  * No axis. The owner retired the axis layer (ledger 2026-08-24, 2026-09-13; migration 109): no warrant names an axis,
    an axis code, an axis status or the taxonomy's axis mapping, and an axis anchor is never a basis for a row.
  * A need-map environmental (e) code is attached to every judged pair, except where a stated exclusion applies.
  * A need-map activity or function (d, b) code is attached only where the identity's own map holds the same code.
  * A code held only by the identity's map is attached only with a GROUND: a word that appears in the identity's side
    (the mechanism of the links holding that code, or the code's recorded title) and in the need's side (registry text,
    obligation, notes, or the need's own ICF notes). The script verifies the word; the warrant names it.
  * Warrants copy no mutable cell: no mechanism, confidence, title, status or annotation text, and no sentence that
    review will make false. They say who the pair is, what the registry says, which codes and which link ids.
  * Not paired, and why: A-AT (registry note flags its scope for the owner); ALL (a scope marker, ledger OD-31);
    MOVE and VES (access needs by owner answer OD-37; base_taxonomy_identity still lists them active);
    SCI (same population as WHEEL by the seventh and eighth sets, retirement open as OI-77); ADHD x A-LOWLOAD carries
    only the need-side code.
  * Body-function (b) codes are WITHHELD for the owner (a recorded question): the identity map holds d codes only.
"""
import json, re, sqlite3, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
HERE = pathlib.Path(__file__).parent
MEMBER = " The named condition is one member of this identity, and the row is keyed on the whole identity."
FAMILY = " The named group is one member of this family identity, and the row is keyed on the whole identity."

# i, n; qn = quote from the need's records; qi = quote from the identity's records; why; ground = {code: word} for
# identity-map-only codes; skip = {code: reason}; withhold = {code: reason}; rec = [(path, substring)].
PAIRS = [
 dict(i="BLIND", n="A-NOSIGHT", qn="blindness, low vision", qi="blind and low-vision people",
      why="The need's registry text names blindness and low vision, and the identity is blind and low-vision people."),
 dict(i="DEAF", n="A-NOSOUND", qn="Deaf, hard of hearing, late-deafened", qi="Deaf, or late-deafened",
      why="The need's registry text names Deaf, hard-of-hearing and late-deafened people.", ground={"d310–d329": "alert"}),
 dict(i="DEAFBLIND", n="A-TACTILE", qn="DeafBlind (Protactile)", qi="Not VIS+DEAF",
      why="The need's registry text names DeafBlind (Protactile) access, and the identity's description says it is not blindness plus deafness."),
 dict(i="BRAIN", n="A-STABLE", qn="post-concussion", qi="post-concussion",
      why="The need's registry text names post-concussion, and the identity's description includes post-concussion." + MEMBER),
 dict(i="BRAIN", n="A-NOSPEECH", qn="aphasia", qi="stroke",
      why="The need's registry text names aphasia, and the identity's description includes stroke; the neurological and acquired brain injury profile in populations.json lists \"stroke sequelae (unilateral neglect, navigation impairment, aphasia, hemiplegia)\"." + MEMBER,
      rec=[("references/website/data/populations.json", "stroke sequelae (unilateral neglect, navigation impairment, aphasia, hemiplegia)")]),
 dict(i="ID", n="A-PLAIN", qn="intellectual disability", qi="people with intellectual disability",
      why="The need's registry text names intellectual disability, and the identity is people with intellectual disability."),
 dict(i="DEM", n="A-PLAIN", qn="dementia", qi="Alzheimer disease and related dementias",
      why="The need's registry text names dementia, and the identity is people living with dementia.", ground={"d460": "wayfinding"}),
 dict(i="BRAIN", n="A-PLAIN", qn="brain injury", qi="acquired brain injury",
      why="The need's registry text names brain injury, and the identity is people with acquired brain injury." + MEMBER),
 dict(i="MOB", n="A-REACH", qn="wheelchair users, ambulatory wheelchair users, cane/crutch users", qi="wheelchair users",
      why="The need's registry text names wheelchair users, ambulatory wheelchair users and cane/crutch users, and the identity is people with mobility needs including wheelchair users." + FAMILY,
      ground={"d465": "wheelchair", "d450": "ambul"}),
 dict(i="LMB", n="A-REACH", qn="limb difference", qi="upper-limb disabilities",
      why="The need's registry text names limb difference, and the identity is people with limb differences, upper-limb disabilities.",
      ground={"d440": "hand", "d445": "hand"},
      skip={"e120": "mobility products and technology; the owner placed this identity outside the mobility family (ledger, eighth set)"}),
 dict(i="MOB", n="A-SELFCARE", qn="bathing, dressing, toileting, eating", qi="wheelchair users",
      why="The need's registry text names bathing, dressing, toileting and eating, and the identity is people with mobility needs including wheelchair users." + FAMILY,
      ground={"d530": "toilet"}),
 dict(i="LMB", n="A-SELFCARE", qn="bathing, dressing, toileting, eating", qi="upper-limb disabilities",
      why="The need's registry text names bathing, dressing, toileting and eating, and the identity is people with limb differences, upper-limb disabilities."),
 dict(i="DEM", n="A-LOWLOAD", qn="dementia", qi="Alzheimer disease and related dementias",
      why="The need's registry text names dementia, and the identity is people living with dementia.", ground={"d460": "wayfinding"}),
 dict(i="ADHD", n="A-LOWLOAD", qn="ADHD", qi="ADHD",
      why="The need's registry text names ADHD, and the identity is people with ADHD."),
 dict(i="BRAIN", n="A-LOWLOAD", qn="brain injury", qi="acquired brain injury",
      why="The need's registry text names brain injury, and the identity is people with acquired brain injury." + MEMBER),
 dict(i="ID", n="A-LOWLOAD", qn="intellectual disability", qi="people with intellectual disability",
      why="The need's registry text names intellectual disability, and the identity is people with intellectual disability."),
 dict(i="COM", n="A-TIME", qn="brain fog impairs organizing time", qi="long COVID, MCAS, ME/CFS, POTS",
      why="The need's own ICF row (access_need_icf, A-TIME to b164) records the owner's rationale that brain fog impairs organizing time, and the identity's description lists long COVID and ME/CFS. That the identity carries brain fog is not stated in a project record: this pair is an inference." + MEMBER,
      withhold={"b164": "a body-function code on an identity; see the recorded owner question"}),
 dict(i="COM", n="A-EFFORT", qn="ME/CFS, Long COVID, POTS", qi="long COVID, MCAS, ME/CFS, POTS",
      why="The need's registry text names ME/CFS, Long COVID and POTS, and the identity's description lists the same conditions.",
      ground={"d450": "fatigue", "d455": "fatigue"}),
 dict(i="MS", n="A-EFFORT", qn="MS fatigue", qi="fatigue",
      why="The need's registry text names MS fatigue, and the identity's description names fatigue."),
 dict(i="PAIN", n="A-EFFORT", qn="pain", qi="sustained discomfort affecting endurance",
      why="The need's registry text names pain, and the identity's description says pain affects endurance.",
      ground={"d450": "fatigue", "d455": "fatigue"}),
 dict(i="AUT", n="A-STIMULUS", qn="autistic people", qi="Autism spectrum",
      why="The need's registry text names autistic people, and the identity is autistic people.", ground={"d230": "sensory"}),
 dict(i="NDV", n="A-STIMULUS", qn="sensory processing differences", qi="Broad neurodivergent category",
      why="The need's registry text names sensory processing differences, and the identity is the broad neurodivergent category; the owner retained it as an identity (ledger, third set).",
      ground={"d230": "sensory"}),
 dict(i="BRAIN", n="A-STIMULUS", qn="post-concussion", qi="post-concussion",
      why="The need's registry text names post-concussion, and the identity's description includes post-concussion." + MEMBER),
 dict(i="MH", n="A-STIMULUS", qn="PTSD", qi="trauma",
      why="The need's registry text names PTSD, and the identity's description names trauma." + MEMBER, ground={"d230": "sensory"}),
 dict(i="EPI", n="A-TRIGGER", qn="photosensitive epilepsy", qi="photosensitivity",
      why="The need's registry text names photosensitive epilepsy, and the identity's description names photosensitivity as a subtype.",
      skip={"e260": "air quality; the need's own annotation on e240 is flash/strobe, the photic row"}),
 dict(i="COM", n="A-TRIGGER", qn="MCAS", qi="MCAS",
      why="The need's registry text names MCAS, and the identity's description lists MCAS." + MEMBER,
      skip={"e240": "annotated flash/strobe in the need's own row, a photic trigger not tied to MCAS in any record"}),
 dict(i="MH", n="A-CALM", qn="anxiety, PTSD, psychiatric distress", qi="Mood, anxiety, trauma",
      why="The need's registry text names anxiety, PTSD and psychiatric distress, and the identity's description names mood, anxiety and trauma."),
 dict(i="AUT", n="A-CALM", qn="autistic people", qi="Autism spectrum",
      why="The need's registry text names autistic people, and the identity is autistic people."),
] + [
 dict(i=i, n="A-SIZE", qn=q, qi="Served by A-SIZE",
      why=f"The identity's description says it is served by this need, and the need's registry text names {q}.")
 for i, q in (("LPA", "little people"), ("TALL", "tall people"), ("BAR", "fat people"))
] + [
 dict(i="MOB", n="A-SIZE", qn="wheelchair seating height", qi="wheelchair users",
      why="The need's registry text names wheelchair seating height, and the identity is people with mobility needs including wheelchair users." + FAMILY,
      ground={"d465": "wheelchair"}),
]


def main():
    c = sqlite3.connect(f"file:{ROOT}/data/guidebook.db?mode=ro", uri=True)
    c.row_factory = sqlite3.Row
    idn = {r["identity_code"]: r for r in c.execute("select * from base_taxonomy_identity where status='active'")}
    need = {r["need_code"]: r for r in c.execute("select * from access_needs")}
    icf = {r["icf_code"]: r for r in c.execute("select * from base_icf")}
    imap = {}
    for r in c.execute("select * from identity_icf_map where retired_at is null order by link_id"):
        imap.setdefault((r["identity_code"], r["icf_code"]), []).append(r)
    nmap = {}
    for r in c.execute("select * from access_need_icf order by icf_code"):
        nmap.setdefault(r["need_code"], {})[r["icf_code"]] = r
    errors, triples, withheld, excluded, seen = [], [], [], [], set()
    for p in PAIRS:
        I, N = p["i"], p["n"]
        if I not in idn: errors.append(f"{I}: not an active identity"); continue
        if N not in need: errors.append(f"{N}: not a need"); continue
        ntexts = [need[N]["absorbs"], need[N]["design_obligation"], need[N]["notes"]] + [r["notes"] for r in nmap.get(N, {}).values()]
        ntext = " | ".join(filter(None, ntexts))
        itext = " | ".join(filter(None, [idn[I]["display_name"], idn[I]["description"]]))
        if p["qn"] not in " | ".join(filter(None, [need[N]["absorbs"], need[N]["notes"]] + [r["notes"] for r in nmap.get(N, {}).values()])):
            errors.append(f"{I}x{N}: need quote not found in the need's absorbs, notes or ICF notes: {p['qn']!r}")
        if p["qi"] not in itext: errors.append(f"{I}x{N}: identity quote not found in the identity's name or description: {p['qi']!r}")
        for path, sub in p.get("rec", []):
            if sub not in (ROOT / path).read_text(): errors.append(f"{I}x{N}: record {path} lacks {sub!r}")
        skip, ground = p.get("skip", {}), p.get("ground", {})
        plan = []   # (code, kind, text)
        for code, r in sorted(nmap.get(N, {}).items()):
            if code in skip: excluded.append(dict(identity=I, need=N, icf=code, reason=skip[code])); continue
            if code in p.get("withhold", {}): continue
            if code[0] == "e": plan.append((code, "need"))
            elif (I, code) in imap: plan.append((code, "both"))
            else: excluded.append(dict(identity=I, need=N, icf=code, reason=f"need-map {code[0]} code that {I}'s own map does not hold"))
        for code, word in ground.items():
            if code not in icf: errors.append(f"{I}x{N}x{code}: not in base_icf"); continue
            if (I, code) not in imap: errors.append(f"{I}x{N}x{code}: the identity's map does not hold it"); continue
            if (N, code) in nmap.get(N, {}): errors.append(f"{I}x{N}x{code}: the need's map holds it; no ground needed"); continue
            iside = " ".join([r["mechanism"] or "" for r in imap[(I, code)]] + [icf[code]["title"] or ""]).lower()
            if word.lower() not in iside: errors.append(f"{I}x{N}x{code}: ground {word!r} not in the identity side (link mechanism or recorded title)"); continue
            if word.lower() not in ntext.lower(): errors.append(f"{I}x{N}x{code}: ground {word!r} not in the need's own text"); continue
            plan.append((code, "ground"))
        for code, why in p.get("withhold", {}).items():
            withheld.append(dict(identity=I, need=N, icf=code, reason=why))
        for code, kind in plan:
            if (I, N, code) in seen: errors.append(f"{I}x{N}x{code}: listed twice"); continue
            seen.add((I, N, code))
            ids = "/".join(str(r["link_id"]) for r in imap.get((I, code), []))
            if kind == "need":
                tail = f"Code {code}: access_need_icf holds {N} -> {code}."
            elif kind == "both":
                tail = f"Code {code}: access_need_icf holds {N} -> {code}; identity_icf_map link {ids} holds it for {I}."
            else:
                tail = (f"Code {code}: identity_icf_map link {ids} holds it for {I}; the word \"{ground[code]}\" appears in that "
                        f"link's mechanism or in the code's recorded title and in the need's own text, which is the tie.")
            triples.append(dict(identity=I, need=N, icf=code, support=kind,
                                warrant=f"{p['why']} Need {N} registry text: \"{p['qn']}\". Identity {I}: \"{p['qi']}\". {tail}"))
    if errors:
        print("REFUSED:"); [print(" ", e) for e in errors]; sys.exit(1)
    for name, data in (("triples", triples), ("withheld", withheld), ("exclusions", excluded)):
        (HERE / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    from collections import Counter
    print(f"proposed: {len(triples)}  withheld: {len(withheld)}  excluded: {len(excluded)}  pairs: {len(PAIRS)}")
    print("by support:", dict(Counter(t["support"] for t in triples)))
    print("identities:", sorted({t['identity'] for t in triples}))
    print("needs:", sorted({t['need'] for t in triples}))
    print("AX- in any warrant:", sum("AX-" in t["warrant"] for t in triples), " max warrant length:", max(len(t["warrant"]) for t in triples))
    for e in excluded: print("  excluded:", e["identity"], e["need"], e["icf"], "-", e["reason"][:80])

main()
